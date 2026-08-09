from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from elicio.harness.adapters import (
    ActionResult,
    AdapterRouter,
    LocalMarkerAdapter,
)
from elicio.harness.audit import JsonlAuditLog, MemoryAuditLog
from elicio.harness.events import GestureEvent
from elicio.harness.harness import Harness
from elicio.harness.policy import DecisionStatus


class RecordingAdapter:
    name = "recording"

    def __init__(self) -> None:
        self.calls: list[tuple[str, GestureEvent]] = []

    def execute(self, command, event) -> ActionResult:
        self.calls.append((command.name, event))
        return ActionResult(
            success=True,
            adapter=self.name,
            details={"call_count": len(self.calls)},
        )


def recording_harness() -> tuple[Harness, RecordingAdapter, MemoryAuditLog]:
    adapter = RecordingAdapter()
    audit = MemoryAuditLog()
    harness = Harness(
        AdapterRouter(
            {
                "console": adapter,
                "local_marker": adapter,
            }
        ),
        audit,
    )
    return harness, adapter, audit


class HarnessPolicyTests(unittest.TestCase):
    def test_each_confidence_floor_rejects_below_and_accepts_boundary(self) -> None:
        cases = (
            ("wrist_up", 0.599, 0.60, DecisionStatus.APPROVED),
            ("index_pinch", 0.749, 0.75, DecisionStatus.APPROVED),
            ("fist", 0.849, 0.85, DecisionStatus.CONFIRMATION_REQUIRED),
        )
        for symbol, below, boundary, accepted_status in cases:
            with self.subTest(symbol=symbol, case="below"):
                harness, adapter, _ = recording_harness()
                outcome = harness.feed(GestureEvent(symbol, below, 10.0))
                self.assertEqual(outcome.decision.status, DecisionStatus.REJECTED)
                self.assertEqual(adapter.calls, [])

            with self.subTest(symbol=symbol, case="boundary"):
                harness, adapter, _ = recording_harness()
                outcome = harness.feed(GestureEvent(symbol, boundary, 10.0))
                self.assertEqual(outcome.decision.status, accepted_status)
                expected_calls = 1 if accepted_status == DecisionStatus.APPROVED else 0
                self.assertEqual(len(adapter.calls), expected_calls)

    def test_dangerous_action_needs_a_second_event(self) -> None:
        harness, adapter, audit = recording_harness()

        first = harness.feed(GestureEvent("fist", 0.90, 10.0))

        self.assertEqual(first.decision.status, DecisionStatus.CONFIRMATION_REQUIRED)
        self.assertEqual(adapter.calls, [])
        self.assertEqual(audit.entries[0]["result"], {"status": "not_run"})

    def test_confirmation_at_timeout_boundary_runs_once(self) -> None:
        harness, adapter, _ = recording_harness()
        harness.feed(GestureEvent("fist", 0.90, 10.0))

        outcome = harness.feed(GestureEvent("jaw_clench", 0.90, 13.0))

        self.assertEqual(outcome.decision.status, DecisionStatus.APPROVED)
        self.assertTrue(outcome.decision.confirmed)
        self.assertEqual(len(adapter.calls), 1)
        self.assertEqual(adapter.calls[0][1].symbol, "fist")

    def test_late_confirmation_drops_pending_action(self) -> None:
        harness, adapter, _ = recording_harness()
        harness.feed(GestureEvent("fist", 0.90, 10.0))

        late = harness.feed(GestureEvent("jaw_clench", 0.90, 13.001))
        second = harness.feed(GestureEvent("jaw_clench", 0.90, 13.1))

        self.assertEqual(late.decision.status, DecisionStatus.REJECTED)
        self.assertIn("timed out", late.decision.reason)
        self.assertEqual(second.decision.status, DecisionStatus.REJECTED)
        self.assertEqual(adapter.calls, [])

    def test_low_confidence_confirmation_can_be_retried_in_time(self) -> None:
        harness, adapter, _ = recording_harness()
        harness.feed(GestureEvent("fist", 0.90, 10.0))

        low = harness.feed(GestureEvent("jaw_clench", 0.84, 11.0))
        accepted = harness.feed(GestureEvent("jaw_clench", 0.90, 12.0))

        self.assertEqual(low.decision.status, DecisionStatus.REJECTED)
        self.assertEqual(accepted.decision.status, DecisionStatus.APPROVED)
        self.assertEqual(len(adapter.calls), 1)

    def test_out_of_order_confirmation_does_not_run(self) -> None:
        harness, adapter, _ = recording_harness()
        harness.feed(GestureEvent("fist", 0.90, 10.0))

        outcome = harness.feed(GestureEvent("jaw_clench", 0.90, 9.0))

        self.assertEqual(outcome.decision.status, DecisionStatus.REJECTED)
        self.assertIn("precedes", outcome.decision.reason)
        self.assertEqual(adapter.calls, [])

    def test_rest_is_audited_without_an_action(self) -> None:
        harness, adapter, audit = recording_harness()

        outcome = harness.feed(GestureEvent("rest", 0.99, 10.0))

        self.assertEqual(outcome.decision.status, DecisionStatus.IGNORED)
        self.assertEqual(adapter.calls, [])
        self.assertEqual(len(audit.entries), 1)
        self.assertEqual(audit.entries[0]["event"]["symbol"], "rest")
        self.assertEqual(audit.entries[0]["result"], {"status": "not_run"})


class LocalActionAuditTests(unittest.TestCase):
    def test_one_event_writes_real_marker_and_complete_audit_entry(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            state_dir = Path(temporary_dir)
            marker_path = state_dir / "actions" / "demo-marker.json"
            audit_path = state_dir / "audit.jsonl"
            harness = Harness(
                AdapterRouter(
                    {"local_marker": LocalMarkerAdapter(marker_path)}
                ),
                JsonlAuditLog(audit_path),
            )

            outcome = harness.feed(GestureEvent("wrist_down", 0.92, 25.0))

            self.assertEqual(outcome.decision.status, DecisionStatus.APPROVED)
            self.assertIsNotNone(outcome.result)
            self.assertTrue(outcome.result.success)
            marker = json.loads(marker_path.read_text(encoding="utf-8"))
            self.assertEqual(marker["event"]["symbol"], "wrist_down")
            self.assertEqual(
                marker["action"],
                "record a local demonstration marker",
            )

            lines = audit_path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 1)
            entry = json.loads(lines[0])
            self.assertEqual(entry["event"]["symbol"], "wrist_down")
            self.assertEqual(entry["decision"]["status"], "approved")
            self.assertEqual(entry["result"]["status"], "completed")
            self.assertTrue(entry["result"]["success"])
            self.assertEqual(entry["result"]["adapter"], "local_marker")
            self.assertEqual(
                entry["result"]["details"]["path"],
                str(marker_path.resolve()),
            )

    def test_missing_adapter_failure_is_audited(self) -> None:
        audit = MemoryAuditLog()
        harness = Harness(AdapterRouter({}), audit)

        outcome = harness.feed(GestureEvent("wrist_down", 0.92, 25.0))

        self.assertEqual(outcome.decision.status, DecisionStatus.APPROVED)
        self.assertFalse(outcome.result.success)
        self.assertEqual(audit.entries[0]["result"]["status"], "failed")
        self.assertIn("not registered", audit.entries[0]["result"]["error"])


if __name__ == "__main__":
    unittest.main()
