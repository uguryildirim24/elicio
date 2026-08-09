"""Command-line entry point for the verified local vertical slice."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import time

from .harness.adapters import AdapterRouter, ConsoleAdapter, LocalMarkerAdapter
from .harness.audit import JsonlAuditLog
from .harness.harness import Harness
from .harness.policy import DEFAULT_COMMANDS, DecisionStatus
from .harness.simulated import REAL_ACTION_DEMO, events_from_script
from .signal.detector import ContractionDetector
from .signal.replay import ReplaySource, build_synthetic_recording


def run_demo(state_dir: Path) -> int:
    state_dir = Path(state_dir)
    marker_path = state_dir / "actions" / "demo-marker.json"
    audit_path = state_dir / "audit.jsonl"
    harness = Harness(
        AdapterRouter(
            {
                "console": ConsoleAdapter(),
                "local_marker": LocalMarkerAdapter(marker_path),
            }
        ),
        JsonlAuditLog(audit_path),
    )

    outcomes = [
        harness.feed(event)
        for event in events_from_script(
            REAL_ACTION_DEMO,
            start_timestamp=time.monotonic(),
        )
    ]
    outcome = outcomes[-1]
    run_audit_records = []
    if audit_path.is_file():
        for line in audit_path.read_text(encoding="utf-8").splitlines():
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(entry, dict) and entry.get("audit_id") == outcome.audit_id:
                run_audit_records.append(entry)
    audit_record_types = [entry.get("record_type") for entry in run_audit_records]
    audit_verified = (
        len(run_audit_records) == 2
        and set(audit_record_types) == {"intent", "result"}
        and all(entry.get("schema_version") == 2 for entry in run_audit_records)
    )
    succeeded = (
        outcome.decision.status == DecisionStatus.APPROVED
        and outcome.result is not None
        and outcome.result.success
        and marker_path.is_file()
        and outcome.audit_error is None
        and audit_verified
    )
    summary = {
        "verified": succeeded,
        "event": outcome.event.to_dict(),
        "decision": outcome.decision.to_dict(),
        "result": outcome.result.to_dict() if outcome.result else None,
        "audit_error": outcome.audit_error,
        "audit_id": outcome.audit_id,
        "audit_record_types": audit_record_types,
        "marker": str(marker_path.resolve()),
        "audit_log": str(audit_path.resolve()),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if succeeded else 1


def _read_audit_entries(audit_path: Path) -> list[dict[str, object]]:
    if not audit_path.is_file():
        return []
    entries: list[dict[str, object]] = []
    for line in audit_path.read_text(encoding="utf-8").splitlines():
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(entry, dict):
            entries.append(entry)
    return entries


def _verify_replay_audit_pair(
    audit_path: Path,
    audit_id: str | None,
    event,
    marker_path: Path,
) -> tuple[list[object], bool]:
    if not audit_id or event is None:
        return [], False
    matching = [
        entry
        for entry in _read_audit_entries(audit_path)
        if entry.get("audit_id") == audit_id
    ]
    record_types = [entry.get("record_type") for entry in matching]
    if len(matching) != 2 or set(record_types) != {"intent", "result"}:
        return record_types, False
    intent = next(entry for entry in matching if entry.get("record_type") == "intent")
    result = next(entry for entry in matching if entry.get("record_type") == "result")
    common_fields = ("schema_version", "audit_id", "event", "action_event", "decision")
    if any(intent.get(field) != result.get(field) for field in common_fields):
        return record_types, False
    if intent.get("schema_version") != 2 or intent.get("event") != event.to_dict():
        return record_types, False
    if intent.get("result") != {"status": "pending"}:
        return record_types, False

    result_payload = result.get("result")
    if not isinstance(result_payload, dict):
        return record_types, False
    details = result_payload.get("details")
    result_verified = (
        result_payload.get("status") == "completed"
        and result_payload.get("success") is True
        and result_payload.get("adapter") == "local_marker"
        and isinstance(details, dict)
        and details.get("path") == str(marker_path.resolve())
    )
    return record_types, result_verified


def _verify_replay_marker(marker_path: Path, event) -> bool:
    if not marker_path.is_file() or event is None:
        return False
    try:
        marker = json.loads(marker_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    command = DEFAULT_COMMANDS.get(event.symbol)
    if command is None:
        return False
    return marker == {
        "schema_version": 1,
        "action": command.name,
        "event": event.to_dict(),
    }


def run_replay_demo(state_dir: Path) -> int:
    """Run the deterministic signal fixture through the local safety slice."""

    state_dir = Path(state_dir)
    marker_path = state_dir / "actions" / "replay-marker.json"
    audit_path = state_dir / "audit.jsonl"
    recording = build_synthetic_recording()
    events = ContractionDetector(
        sample_rate_hz=recording.sample_rate_hz
    ).detect(ReplaySource(recording))
    harness = Harness(
        AdapterRouter({"local_marker": LocalMarkerAdapter(marker_path)}),
        JsonlAuditLog(audit_path),
    )
    outcomes = [harness.feed(event) for event in events]
    event = events[0] if len(events) == 1 else None
    outcome = outcomes[0] if len(outcomes) == 1 else None
    audit_id = outcome.audit_id if outcome is not None else None
    audit_record_types, audit_verified = _verify_replay_audit_pair(
        audit_path, audit_id, event, marker_path
    )
    marker_verified = _verify_replay_marker(marker_path, event)
    approved_action_count = sum(
        1
        for item in outcomes
        if item.decision.status == DecisionStatus.APPROVED
        and item.result is not None
        and item.result.success
    )
    succeeded = (
        len(events) == 1
        and len(outcomes) == 1
        and approved_action_count == 1
        and outcome is not None
        and outcome.audit_error is None
        and marker_verified
        and audit_verified
    )
    summary = {
        "verified": succeeded,
        "events_emitted": len(events),
        "event": event.to_dict() if event is not None else None,
        "decision": outcome.decision.to_dict() if outcome is not None else None,
        "result": outcome.result.to_dict() if outcome and outcome.result else None,
        "approved_action_count": approved_action_count,
        "marker_exists": marker_path.is_file(),
        "marker_verified": marker_verified,
        "audit_error": outcome.audit_error if outcome is not None else None,
        "audit_id": audit_id,
        "audit_record_types": audit_record_types,
        "audit_verified": audit_verified,
        "marker": str(marker_path.resolve()),
        "audit_log": str(audit_path.resolve()),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if succeeded else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="elicio")
    subparsers = parser.add_subparsers(dest="command", required=True)
    demo = subparsers.add_parser(
        "demo",
        help="run one simulated event through policy into a local marker file",
    )
    demo.add_argument(
        "--state-dir",
        type=Path,
        default=Path(".elicio-demo"),
        help="directory for the marker and JSONL audit log",
    )
    replay_demo = subparsers.add_parser(
        "replay-demo",
        help="replay the deterministic signal fixture through the safety harness",
    )
    replay_demo.add_argument(
        "--state-dir",
        type=Path,
        default=Path(".elicio-replay-demo"),
        help="directory for the replay marker and JSONL audit log",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "demo":
        return run_demo(args.state_dir)
    if args.command == "replay-demo":
        return run_replay_demo(args.state_dir)
    raise AssertionError(f"unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
