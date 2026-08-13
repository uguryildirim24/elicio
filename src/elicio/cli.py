"""Command-line entry point for the verified local vertical slice."""

from __future__ import annotations

import argparse
import contextlib
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import time

from .harness.adapters import AdapterRouter, ConsoleAdapter, LocalMarkerAdapter
from .harness.audit import JsonlAuditLog
from .harness.harness import Harness
from .harness.policy import DEFAULT_COMMANDS, DecisionStatus
from .harness.simulated import REAL_ACTION_DEMO, events_from_script
from .signal.capture import (
    TrailingEnvelope,
    collect_samples,
    load_recording,
    render_meter,
    save_recording,
    stream_samples,
)
from .signal.detector import ContractionDetector
from .signal.replay import DEFAULT_SAMPLE_RATE_HZ, Recording, ReplaySource, build_synthetic_recording


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


@contextlib.contextmanager
def _open_input(source: str):
    """Yield an iterable of lines from a file path or ``-`` for stdin."""

    if source == "-":
        yield sys.stdin
        return
    with open(source, "r", encoding="utf-8", errors="replace") as handle:
        yield handle


def run_capture(args) -> int:
    """Capture a live sample stream into one replayable recording file."""

    max_samples = args.samples
    if args.seconds is not None:
        by_seconds = int(round(args.seconds * args.sample_rate))
        max_samples = by_seconds if max_samples is None else min(max_samples, by_seconds)

    with _open_input(args.input) as lines:
        samples = collect_samples(
            lines,
            offset=args.offset,
            gain=args.gain,
            max_samples=max_samples,
        )

    if not samples:
        print(json.dumps({"verified": False, "error": "no samples captured"}, indent=2))
        return 1

    recording = Recording(tuple(samples), sample_rate_hz=args.sample_rate)
    meta = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "source": args.input,
        "site": args.site,
        "note": args.note,
        "offset": args.offset,
        "gain": args.gain,
    }
    out_path = save_recording(recording, args.out, meta=meta)
    summary = {
        "verified": True,
        "recording": str(out_path.resolve()),
        "samples": len(samples),
        "sample_rate_hz": recording.sample_rate_hz,
        "duration_seconds": recording.duration_seconds,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


def run_scope(args) -> int:
    """Live terminal envelope meter with detection events, for biofeedback."""

    detector = ContractionDetector(
        symbol=args.symbol,
        sample_rate_hz=args.sample_rate,
        onset_threshold=args.threshold,
    )
    envelope = TrailingEnvelope(window=detector.envelope_window)
    event_count = 0
    with _open_input(args.input) as lines:
        try:
            for timestamp, sample in stream_samples(
                lines,
                sample_rate_hz=args.sample_rate,
                offset=args.offset,
                gain=args.gain,
            ):
                level = envelope.update(sample)
                event = detector.process_sample(timestamp, sample)
                meter = render_meter(
                    level, args.threshold, width=args.width, peak=args.peak
                )
                print("\r" + meter, end="", flush=True)
                if event is not None:
                    event_count += 1
                    print(
                        f"\nevent {event_count}: {event.symbol} "
                        f"confidence={event.confidence:.2f} t={event.timestamp:.3f}s",
                        flush=True,
                    )
        except KeyboardInterrupt:
            pass
    print(f"\nstream ended; {event_count} event(s) detected")
    return 0


def run_recording_replay(recording_path: Path, state_dir: Path) -> int:
    """Replay one captured recording through detection, policy, and action."""

    state_dir = Path(state_dir)
    marker_path = state_dir / "actions" / "recording-marker.json"
    audit_path = state_dir / "audit.jsonl"
    recording = load_recording(recording_path)
    events = ContractionDetector(
        sample_rate_hz=recording.sample_rate_hz
    ).detect(ReplaySource(recording))
    harness = Harness(
        AdapterRouter({"local_marker": LocalMarkerAdapter(marker_path)}),
        JsonlAuditLog(audit_path),
    )
    outcomes = [harness.feed(event) for event in events]

    approved = [
        outcome
        for outcome in outcomes
        if outcome.decision.status == DecisionStatus.APPROVED
        and outcome.result is not None
        and outcome.result.success
    ]
    audit_entries = _read_audit_entries(audit_path)
    audit_pairs_intact = all(
        sorted(
            entry.get("record_type")
            for entry in audit_entries
            if entry.get("audit_id") == outcome.audit_id
        )
        == ["intent", "result"]
        for outcome in approved
    )
    last_event = approved[-1].action_event if approved else None
    marker_verified = _verify_replay_marker(marker_path, last_event)
    succeeded = (
        len(events) >= 1
        and len(approved) >= 1
        and all(outcome.audit_error is None for outcome in outcomes)
        and audit_pairs_intact
        and marker_verified
    )
    summary = {
        "verified": succeeded,
        "recording": str(Path(recording_path).resolve()),
        "samples": len(recording.samples),
        "duration_seconds": recording.duration_seconds,
        "events_emitted": len(events),
        "approved_action_count": len(approved),
        "decisions": [
            {
                "symbol": outcome.event.symbol,
                "status": outcome.decision.status.value,
                "reason": outcome.decision.reason,
            }
            for outcome in outcomes
        ],
        "audit_pairs_intact": audit_pairs_intact,
        "marker_verified": marker_verified,
        "marker": str(marker_path.resolve()),
        "audit_log": str(audit_path.resolve()),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if succeeded else 1


def _add_stream_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--input",
        required=True,
        help="stream source: a file path, a configured serial device, or - for stdin",
    )
    parser.add_argument(
        "--sample-rate",
        type=float,
        default=DEFAULT_SAMPLE_RATE_HZ,
        help="declared samples per second of the stream",
    )
    parser.add_argument(
        "--offset",
        type=float,
        default=0.0,
        help="raw value subtracted from every sample, e.g. an ADC mid-rail bias",
    )
    parser.add_argument(
        "--gain",
        type=float,
        default=1.0,
        help="multiplier applied after the offset, to land signals near 0..1",
    )


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
    capture = subparsers.add_parser(
        "capture",
        help="save a live one-channel sample stream as a replayable recording",
    )
    _add_stream_arguments(capture)
    capture.add_argument(
        "--out",
        type=Path,
        required=True,
        help="path of the recording JSON file to write",
    )
    capture.add_argument(
        "--samples",
        type=int,
        default=None,
        help="stop after this many samples",
    )
    capture.add_argument(
        "--seconds",
        type=float,
        default=None,
        help="stop after this many seconds of samples at the declared rate",
    )
    capture.add_argument(
        "--site",
        default="",
        help="electrode or sensor site, recorded in the file's meta block",
    )
    capture.add_argument(
        "--note",
        default="",
        help="free-form provenance note, recorded in the file's meta block",
    )
    scope = subparsers.add_parser(
        "scope",
        help="live terminal envelope meter with detection events, for biofeedback",
    )
    _add_stream_arguments(scope)
    scope.add_argument(
        "--threshold",
        type=float,
        default=0.20,
        help="detector onset threshold shown as the meter's marker",
    )
    scope.add_argument(
        "--symbol",
        default="wrist_down",
        help="gesture symbol emitted for detected contractions",
    )
    scope.add_argument(
        "--width",
        type=int,
        default=40,
        help="meter width in characters",
    )
    scope.add_argument(
        "--peak",
        type=float,
        default=1.0,
        help="envelope value that fills the whole meter",
    )
    replay_recording = subparsers.add_parser(
        "replay-recording",
        help="replay a captured recording through detection, policy, and action",
    )
    replay_recording.add_argument(
        "--recording",
        type=Path,
        required=True,
        help="recording JSON file produced by the capture command",
    )
    replay_recording.add_argument(
        "--state-dir",
        type=Path,
        default=Path(".elicio-recording-replay"),
        help="directory for the marker and JSONL audit log",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "demo":
        return run_demo(args.state_dir)
    if args.command == "replay-demo":
        return run_replay_demo(args.state_dir)
    if args.command == "capture":
        return run_capture(args)
    if args.command == "scope":
        return run_scope(args)
    if args.command == "replay-recording":
        return run_recording_replay(args.recording, args.state_dir)
    raise AssertionError(f"unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
