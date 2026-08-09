"""Safety harness migrated from the Claude Science milestone-0 simulation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Mapping
from uuid import uuid4

from .adapters import ActionResult, AdapterRouter
from .audit import AuditSink
from .events import GestureEvent
from .policy import (
    Command,
    CONFIDENCE_FLOORS,
    CONFIRM_CONFIDENCE_FLOOR,
    CONFIRM_SYMBOL,
    CONFIRM_WINDOW_S,
    DEFAULT_COMMANDS,
    DecisionStatus,
    PolicyDecision,
    REST_SYMBOL,
    RiskLevel,
)


@dataclass(frozen=True, slots=True)
class HarnessOutcome:
    audit_id: str
    event: GestureEvent
    decision: PolicyDecision
    result: ActionResult | None
    action_event: GestureEvent | None = None
    audit_error: str | None = None


@dataclass(frozen=True, slots=True)
class _PendingAction:
    event: GestureEvent
    command: Command


class Harness:
    """Consumes gesture events, applies policy, routes actions, and audits."""

    def __init__(
        self,
        router: AdapterRouter,
        audit_log: AuditSink,
        commands: Mapping[str, Command] = DEFAULT_COMMANDS,
    ) -> None:
        self._router = router
        self._audit_log = audit_log
        self._commands = dict(commands)
        self._pending: _PendingAction | None = None

    def feed(self, event: GestureEvent) -> HarnessOutcome:
        if event.symbol == REST_SYMBOL:
            return self._finish(
                event,
                PolicyDecision(DecisionStatus.IGNORED, "rest produces no action"),
            )

        if event.symbol == CONFIRM_SYMBOL:
            return self._confirm(event)

        command = self._commands.get(event.symbol)
        if command is None:
            return self._finish(
                event,
                PolicyDecision(DecisionStatus.REJECTED, "unknown symbol"),
            )

        floor = CONFIDENCE_FLOORS[command.risk]
        if event.confidence < floor:
            return self._finish(
                event,
                PolicyDecision(
                    DecisionStatus.REJECTED,
                    f"confidence {event.confidence:.2f} is below {floor:.2f}",
                    command,
                ),
            )

        if command.risk == RiskLevel.DANGEROUS:
            if self._pending is not None:
                return self._finish(
                    event,
                    PolicyDecision(
                        DecisionStatus.REJECTED,
                        "another dangerous command is awaiting confirmation",
                        command,
                    ),
                )
            self._pending = _PendingAction(event, command)
            return self._finish(
                event,
                PolicyDecision(
                    DecisionStatus.CONFIRMATION_REQUIRED,
                    (
                        f"dangerous action requires {CONFIRM_SYMBOL!r} within "
                        f"{CONFIRM_WINDOW_S:.1f} seconds"
                    ),
                    command,
                ),
            )

        return self._execute(event, event, command, confirmed=False)

    def _confirm(self, event: GestureEvent) -> HarnessOutcome:
        pending = self._pending
        if pending is None:
            return self._finish(
                event,
                PolicyDecision(
                    DecisionStatus.REJECTED,
                    "confirmation received with no pending action",
                ),
            )

        if event.confidence < CONFIRM_CONFIDENCE_FLOOR:
            return self._finish(
                event,
                PolicyDecision(
                    DecisionStatus.REJECTED,
                    (
                        f"confirmation confidence {event.confidence:.2f} is below "
                        f"{CONFIRM_CONFIDENCE_FLOOR:.2f}"
                    ),
                    pending.command,
                ),
                action_event=pending.event,
            )

        age = event.timestamp - pending.event.timestamp
        if age < 0.0:
            return self._finish(
                event,
                PolicyDecision(
                    DecisionStatus.REJECTED,
                    "confirmation timestamp precedes the pending event",
                    pending.command,
                ),
                action_event=pending.event,
            )
        if age > CONFIRM_WINDOW_S:
            self._pending = None
            return self._finish(
                event,
                PolicyDecision(
                    DecisionStatus.REJECTED,
                    f"confirmation arrived after {age:.3f} seconds and timed out",
                    pending.command,
                ),
                action_event=pending.event,
            )

        self._pending = None
        return self._execute(event, pending.event, pending.command, confirmed=True)

    def _execute(
        self,
        audit_event: GestureEvent,
        action_event: GestureEvent,
        command: Command,
        *,
        confirmed: bool,
    ) -> HarnessOutcome:
        audit_id = uuid4().hex
        decision = PolicyDecision(
            DecisionStatus.APPROVED,
            "policy approved the action",
            command,
            confirmed=confirmed,
        )
        intent = self._entry(
            audit_id=audit_id,
            record_type="intent",
            event=audit_event,
            action_event=action_event,
            decision=decision,
            result={"status": "pending"},
        )
        try:
            self._audit_log.record(intent)
        except Exception as exc:
            error = self._audit_error("intent", exc)
            blocked_result = ActionResult(
                success=False,
                adapter=command.adapter,
                details={"audit_id": audit_id},
                error=f"{error}; action blocked",
            )
            return HarnessOutcome(
                audit_id=audit_id,
                event=audit_event,
                decision=decision,
                result=blocked_result,
                action_event=action_event,
                audit_error=error,
            )

        result = self._router.execute(command, action_event)
        result_entry = self._entry(
            audit_id=audit_id,
            record_type="result",
            event=audit_event,
            action_event=action_event,
            decision=decision,
            result=result.to_dict(),
        )
        audit_error = None
        try:
            self._audit_log.record(result_entry)
        except Exception as exc:
            audit_error = self._audit_error("result", exc)
        return HarnessOutcome(
            audit_id=audit_id,
            event=audit_event,
            decision=decision,
            result=result,
            action_event=action_event,
            audit_error=audit_error,
        )

    def _finish(
        self,
        event: GestureEvent,
        decision: PolicyDecision,
        result: ActionResult | None = None,
        *,
        action_event: GestureEvent | None = None,
    ) -> HarnessOutcome:
        audit_id = uuid4().hex
        entry = self._entry(
            audit_id=audit_id,
            record_type="decision",
            event=event,
            action_event=action_event,
            decision=decision,
            result=result.to_dict() if result else {"status": "not_run"},
        )
        audit_error = None
        try:
            self._audit_log.record(entry)
        except Exception as exc:
            audit_error = self._audit_error("decision", exc)
        return HarnessOutcome(
            audit_id=audit_id,
            event=event,
            decision=decision,
            result=result,
            action_event=action_event,
            audit_error=audit_error,
        )

    @staticmethod
    def _audit_error(record_type: str, exc: Exception) -> str:
        return f"{record_type} audit write failed: {type(exc).__name__}: {exc}"

    @staticmethod
    def _entry(
        *,
        audit_id: str,
        record_type: str,
        event: GestureEvent,
        action_event: GestureEvent | None,
        decision: PolicyDecision,
        result: Mapping[str, object],
    ) -> dict[str, object]:
        return {
            "schema_version": 2,
            "record_type": record_type,
            "audit_id": audit_id,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "event": event.to_dict(),
            "action_event": action_event.to_dict() if action_event else None,
            "decision": decision.to_dict(),
            "result": dict(result),
        }
