# Elicio

Elicio is a personal biological-input layer for an AI work environment.

The intended flow is:

    body sensor -> personal decoder -> gesture event -> safety harness -> AI tools

The stable decoder event is:

    (symbol, confidence, timestamp)

## Verified engineering slice

The first software-only vertical slice is now runnable. One simulated
wrist_down event passes the event validator and confidence policy, then an
explicit local-marker adapter atomically writes a harmless JSON file. For an
approved action, the harness writes an `intent` audit record before calling the
adapter and a linked `result` record after it. Both records use schema version
2 and the same audit ID. Other decisions use one `decision` record.

Run the verified demonstration from the repository root:

    PYTHONPATH=src python3 -m elicio.cli demo --state-dir .elicio-demo

A successful run prints a JSON summary with verified set to true. It writes:

    .elicio-demo/actions/demo-marker.json
    .elicio-demo/audit.jsonl

The event cannot select a file path or run a shell command. The adapter receives
a fixed path when the harness is built.

The audit is fail closed for approved actions. If the intent record cannot be
written, the adapter is not called and the outcome reports that the action was
blocked. If the result record cannot be written after the adapter runs, the
outcome keeps the adapter result and reports the audit error instead of hiding
the completed action. The demo checks the two records for its own audit ID, so
old records in an appended `.elicio-demo/audit.jsonl` do not count.

## Replayable signal demo

Run the deterministic one-channel signal fixture through replay, contraction
detection, the harness, and the fixed local marker adapter:

    PYTHONPATH=src .venv/bin/python -m elicio.cli replay-demo --state-dir .elicio-replay-demo

The fixture contains seeded rest-level noise, one elevated burst, and more
rest. A successful JSON summary has `verified` set to true only when exactly
one `wrist_down` event is emitted, the expected replay marker exists, and this
run's linked intent/result audit pair is complete. The JSONL audit file remains
append-only; earlier runs do not count toward the current pair.

This is a synthetic software replay. It is not a personal recording, does not
validate a sensor or hardware path, and does not establish biological
end-to-end operation.

## Safety behavior

Confidence floors rise with command risk: 0.60 for harmless actions, 0.75 for
reversible edits, and 0.85 for dangerous actions. A dangerous action never runs
from one event. It requires a separate jaw_clench event with at least 0.85
confidence within three seconds. Rest, unknown symbols, low-confidence events,
late confirmations, and out-of-order confirmations do not run actions. Every
decision is audited.

Only the local marker action is real. The other migrated milestone-0 actions
remain explicit console simulations.

## Research pipeline

The final Claude Science emg_pipeline package now lives under
src/elicio/pipeline. Imports were made package-relative, shared settings come
from config.py, and both training entry points now use the session-leakage
guard in splits.py.

Install the base package in an isolated environment:

    python3.11 -m venv .venv
    .venv/bin/python -m pip install -e .

The research commands also need the optional scientific packages:

    .venv/bin/python -m pip install -e '.[research]'
    .venv/bin/elicio-emg prepare --subjects 1 2 3 --out-dir results
    .venv/bin/elicio-emg train --data-dir results --subjects 1 2 3
    .venv/bin/elicio-emg evaluate --data-dir results --subjects 1 2 3

Training and evaluation remain research workloads. They were not rerun locally
for this engineering slice.

## Tests

Run the contract and safety suite with:

    .venv/bin/python -m unittest discover -s tests -v

The suite covers event validation, each confidence floor, rest handling,
dangerous-action confirmation and timeout behavior, JSONL audit records, the
real local marker effect, and cross-session leakage rejection.

## Current limits

Claude Science completed the first research phase, but Elicio is not an
end-to-end biological-input product. No hardware has been purchased. No
personal sensor recording exists. A real sensor signal has not been decoded or
used to complete a harness action.

See docs/CLAUDE_SCIENCE_HANDOFF.md for the research handoff and
docs/RESEARCH_PROVENANCE.md for the exact migrated artifacts.
