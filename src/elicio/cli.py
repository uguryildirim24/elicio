"""Command-line entry point for the verified local vertical slice."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import time

from .harness.adapters import AdapterRouter, ConsoleAdapter, LocalMarkerAdapter
from .harness.audit import JsonlAuditLog
from .harness.harness import Harness
from .harness.policy import DecisionStatus
from .harness.simulated import REAL_ACTION_DEMO, events_from_script


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
    succeeded = (
        outcome.decision.status == DecisionStatus.APPROVED
        and outcome.result is not None
        and outcome.result.success
        and marker_path.is_file()
    )
    summary = {
        "verified": succeeded,
        "event": outcome.event.to_dict(),
        "decision": outcome.decision.to_dict(),
        "result": outcome.result.to_dict() if outcome.result else None,
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
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "demo":
        return run_demo(args.state_dir)
    raise AssertionError(f"unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
