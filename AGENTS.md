# Repository Guidelines

## Project Overview

Elicio is a safety boundary between personal gesture events and local AI tools. The intended flow is:

```text
body sensor -> personal decoder -> gesture event -> safety harness -> AI tools
```

The stable decoder event is `(symbol, confidence, timestamp)`. The product slice is a deterministic
software harness with a harmless local-marker action. It is not an end-to-end biological-input
product: no hardware or personal sensor recording exists. See `docs/CLAUDE_SCIENCE_HANDOFF.md`
before changing the engineering slice.

## Architecture & Data Flow

### Product slice

- `src/elicio/cli.py` provides `demo` and `replay-demo` through `argparse`.
- `demo` creates a scripted `GestureEvent`; `replay-demo` generates a seeded synthetic recording,
  replays it through `ContractionDetector`, and emits a `wrist_down` event.
- Both paths call `Harness.feed`, which validates the command and confidence floor, records an
  audit intent, executes an injected adapter, then records the result.
- `LocalMarkerAdapter` writes a fixed payload atomically. Events cannot choose a path or shell
  command. `JsonlAuditLog` appends fsynced JSONL records.
- Approved actions emit schema-version-2 `intent` and `result` records sharing `audit_id`; other
  decisions emit one `decision` record.

Audit is fail-closed before execution: if the intent record cannot be written, the adapter is not
called. If result auditing fails after execution, the completed adapter result is preserved and
reported with the audit error.

Dangerous commands require two events. A first event creates pending state; a separate
`jaw_clench` with confidence at least `0.85` must arrive within `3.0` seconds. Reversed timestamps,
late confirmations, low-confidence confirmations, rest, and unknown symbols do not run actions.

### Research pipeline

`src/elicio/pipeline/` is the migrated GRABMyo sEMG research pipeline:

```text
prepare -> WFDB records -> windows/features -> subject_NN.npz
train/evaluate -> cross_session_split -> classical/neural models -> CSV results
```

`elicio-emg prepare` fetches public PhysioNet/WFDB records, windows them, and computes MAV, WL,
ZC, SSC, and RMS features. `train` evaluates baseline models plus Temporal CNN, GRU, and
Transformer models. `evaluate` scores a six-best-gestures-plus-rest subset.

All training/evaluation splits must use `cross_session_split` and
`assert_no_session_leakage`. Never add a same-session split as evaluation proof.

## Key Directories

| Path | Purpose |
| --- | --- |
| `src/elicio/harness/` | Event contract, risk policy, adapters, audit sinks, and harness state machine |
| `src/elicio/signal/` | Standard-library replay fixtures and contraction detector |
| `src/elicio/pipeline/` | GRABMyo preparation, feature extraction, splitting, models, and CLI |
| `tests/` | Class-based stdlib `unittest` suite |
| `docs/` | Engineering handoff and research provenance ledger |

`.elicio-demo/`, `.elicio-replay-demo/`, `results/`, `.venv/`, `__pycache__/`, and `*.egg-info/`
are generated or local artifacts. `.elicio-demo/` and `*.egg-info/` are gitignored.

## Development Commands

Create an isolated environment and install the package:

```bash
python3.11 -m venv .venv
.venv/bin/python -m pip install -e .
```

Install the optional research dependencies only when working on the pipeline:

```bash
.venv/bin/python -m pip install -e '.[research]'
```

Run the software demos:

```bash
.venv/bin/python -m elicio.cli demo --state-dir .elicio-demo
.venv/bin/python -m elicio.cli replay-demo --state-dir .elicio-replay-demo
```

Run research commands with the pipeline module:

```bash
.venv/bin/python -m elicio.pipeline.cli prepare --subjects 1 2 3 --out-dir results
.venv/bin/python -m elicio.pipeline.cli train --data-dir results --subjects 1 2 3 --epochs 20 --out results/train_results.csv
.venv/bin/python -m elicio.pipeline.cli evaluate --data-dir results --subjects 1 2 3 --epochs 20 --out results/six_best_rest.csv
```

`prepare` writes compressed `subject_NN.npz` files. `train` and `evaluate` read those files and
write CSVs. These are research workloads; do not run multi-subject training casually.

## Code Conventions & Common Patterns

### Product slice

- Use `from __future__ import annotations` and modern built-in generics/unions.
- Use PascalCase for classes, `snake_case` for functions, and `UPPER_SNAKE_CASE` for constants.
- Keep value objects immutable: dataclasses use `frozen=True, slots=True`.
- Validate constructor inputs at boundaries with built-in `TypeError`/`ValueError`; there are no
  custom exception classes in the product slice.
- Return typed result objects for policy and adapter failures instead of raising during normal
  action processing.
- Inject dependencies through constructors: `Harness(router, audit_log, commands=...)`,
  `AdapterRouter(mapping)`, `LocalMarkerAdapter(marker_path)`, and `JsonlAuditLog(path)`.
- Use `Protocol` for adapter and audit extension points. Keep the harness and signal packages
  standard-library-only.
- Keep state per instance. Shared command tables are immutable mappings; audit files are append-only.
- Preserve atomic marker writes (`tempfile.mkstemp` + `fsync` + `os.replace`) and audit fsyncs.
- All current execution APIs are synchronous. Do not introduce async patterns without a clear need.

### Research pipeline

The pipeline intentionally preserves migrated research implementations. Avoid changing model
architectures, feature formulas, windowing, channel selection, or gesture selection during routine
engineering work.

- Configuration is supplied by module constants in `pipeline/config.py`, not a config object.
- Use NumPy array contracts: signals are float32 `[n_samples, n_channels]`, labels are int32,
  features are float32, and neural inputs are channel-first `(batch, channels, timesteps)`.
- Research type hints are partial and shape validation commonly uses assertions. Do not copy those
  looser conventions into the harness.
- Optional imports are deliberate: `load.py` guards WFDB; model modules require scikit-learn and/or
  PyTorch. Keep `features.py` and `splits.py` usable with the base NumPy dependency.
- Pipeline README documentation has a stale reference to `train.py`; the actual module is
  `train_and_eval.py`.

## Important Files

- `pyproject.toml`: setuptools build configuration, dependencies, `src/` package discovery, and
  `elicio` / `elicio-emg` console scripts.
- `src/elicio/cli.py`: product demos, JSON summaries, marker verification, and exit status.
- `src/elicio/harness/events.py`: validated immutable `GestureEvent` contract.
- `src/elicio/harness/policy.py`: risk levels, confidence floors, commands, and confirmation constants.
- `src/elicio/harness/harness.py`: policy state machine and intent/result/decision audit records.
- `src/elicio/harness/adapters.py`: adapter protocol, router, console simulation, and atomic marker.
- `src/elicio/harness/audit.py`: append-only JSONL and in-memory audit sinks.
- `src/elicio/signal/detector.py` and `src/elicio/signal/replay.py`: detection and deterministic fixtures.
- `src/elicio/pipeline/config.py`: shared research defaults.
- `src/elicio/pipeline/splits.py`: session-leakage guard.
- `src/elicio/pipeline/README.md`: pipeline workflow and data shapes.
- `docs/CLAUDE_SCIENCE_HANDOFF.md`: safety, authority, and scope constraints.
- `docs/RESEARCH_PROVENANCE.md`: migrated-artifact provenance and verification evidence.

## Runtime/Tooling Preferences

- Python `>=3.11`.
- Use the repository's `.venv` and `pip`; there is no uv/Poetry lockfile or `requirements.txt`.
- Build backend: `setuptools>=77` with packages discovered under `src`.
- Base dependency: `numpy>=2.0`.
- Optional `research` dependencies: `scikit-learn>=1.5`, `torch>=2.4`, and `wfdb>=4.1`.
- After editable installation, use the `elicio` and `elicio-emg` console scripts; the equivalent
  `python -m elicio.cli` and `python -m elicio.pipeline.cli` module forms also work.
- No formatter, linter, type checker, pre-commit configuration, Makefile, or CI workflow is
  configured. Match surrounding style and verify behavior with the existing commands.

## Testing & QA

The suite uses stdlib `unittest`, not pytest. There are no `conftest.py`, `pytest.ini`, `tox.ini`,
`setup.cfg`, `.coveragerc`, or `noxfile.py` files.

```bash
.venv/bin/python -m unittest discover -s tests -v
```

The five test modules cover event validation/serialization, confidence floors, dangerous-action
confirmation and timeout behavior, rest handling, audit failure modes, atomic marker output,
deterministic signal replay/detection, feature windowing, and cross-session leakage rejection.
The suite needs only the base NumPy dependency; it has no optional-dependency skip logic.

Use `tempfile.TemporaryDirectory()` for filesystem tests. Keep tests deterministic with explicit
fixtures and timestamps. Use `unittest.TestCase`, `subTest`, and small local test doubles rather
than adding a pytest or mocking framework. Do not write tests into `.elicio-demo/`.

For changes to untested CLI or pipeline paths, run the corresponding demo or command with a small,
controlled output directory. A demo is successful only when it exits 0 and prints `"verified": true`.
Synthetic replay is not hardware or biological end-to-end validation.
