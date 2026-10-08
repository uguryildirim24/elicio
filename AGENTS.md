# Repository guidelines

Rolf directs Elicio. Coding agents do not commit, push, purchase parts or contact vendors.

## Scope

Elicio is an unfinished and unordered ear-muscle EMG earpiece with a runnable synthetic software gate. No real recording, physical wearable validation or AI execution adapter exists. Preserve that distinction in code and documentation.

## Architecture

- `src/elicio/harness/`: validated events, confidence policy, timed confirmation, adapters and audit records.
- `src/elicio/signal/`: synthetic replay, contraction detection and ASCII stream capture.
- `src/elicio/frame_v2.py`, `receiver_v2.py`: binary BLE framing and session reception.
- `src/elicio/pipeline/`: public GRABMyo preparation and cross-session model evaluation.
- `hardware/board/`, `firmware/`, `scripts/cad/`: unfinished hardware and implementation sources.

Only `LocalMarkerAdapter` performs a real action. Its target is fixed at construction. Intent audit failure blocks execution. Result audit failure must not hide a completed action. Distinct gesture symbols do not establish independent muscle sources.

## Development

Use Python >=3.11. Install with `python3 -m venv .venv` and `.venv/bin/python -m pip install -e .`. The root README gives the demo, receiver and existing unittest commands. Optional extras are `research`, `ble`, `cad` and `sheets`. Do not add smoke tests, compatibility layers or fallback paths.

Keep research splitting in `cross_session_split` with `assert_no_session_leakage`. Do not report a within-session score as cross-session performance. Preserve model formulas during unrelated cleanup.

Use immutable event value objects, explicit boundary validation, dependency injection and per-instance state. Preserve atomic marker writes and fsynced audit records. The current execution APIs are synchronous.

## Files and output

Use ignored `.reports/` for regeneration and release work, `results/` for research output, `recordings/` for acquisition, and `measurements/` for anatomy parameters. Do not publish raw personal measurements, recordings, checkout information, private agent diaries or credentials.

Selected snap-shell assets are in `docs/fab/cad/v4-snap/`. The hinge-only base and v1/v2 references remain because the generator and existing checks use them. They are not manufacturing approval. Avoid overwriting tracked exports during routine checks.
