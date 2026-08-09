# Elicio

Elicio is a personal biological-input layer for an AI work environment.

The intended flow is:

    body sensor -> personal decoder -> gesture event -> safety harness -> AI tools

The stable decoder event is:

    (symbol, confidence, timestamp)

## Verified engineering slice

The first software-only vertical slice is now runnable. One simulated
wrist_down event passes the event validator and confidence policy, then an
explicit local-marker adapter atomically writes a harmless JSON file. The
harness appends the event, policy decision, and adapter result to a JSONL audit
log.

Run the verified demonstration from the repository root:

    PYTHONPATH=src python3 -m elicio.cli demo --state-dir .elicio-demo

A successful run prints a JSON summary with verified set to true. It writes:

    .elicio-demo/actions/demo-marker.json
    .elicio-demo/audit.jsonl

The event cannot select a file path or run a shell command. The adapter receives
a fixed path when the harness is built.

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
