# Elicio

Elicio is a meeting point between a person and a language model in the physical
world.

A deliberate muscle contraction becomes an explicit event. A safety harness
decides what that event is allowed to do. Only then does a model act.

```text
body sensor -> personal decoder -> gesture event -> safety harness -> AI tools
```

The harness is the product. Codex, Claude, and other models are replaceable
reasoning engines behind it. The stable interface between the body and everything
downstream is one small tuple:

```text
(symbol, confidence, timestamp)
```

For the idea, the origin, the research evidence, and the open design questions,
read [`docs/VISION.md`](docs/VISION.md).

## Status

The software boundary is real and runs today. Everything upstream of the event is
still synthetic.

| Part | State |
| --- | --- |
| Safety harness, policy, audit | Real, tested |
| Local marker action | Real, atomic file write |
| Other actions in the alphabet | Console simulations |
| Signal replay and contraction detection | Real, deterministic fixtures |
| Sensor hardware | Not purchased |
| Personal recording | Does not exist |

No real sensor signal has been recorded, decoded, and used to complete a harness
action. Elicio is not an end-to-end biological-input product and should not be
described as one.

## Run it

```bash
python3.11 -m venv .venv
.venv/bin/python -m pip install -e .
```

One simulated event through policy into a real local file:

```bash
.venv/bin/elicio demo --state-dir .elicio-demo
```

The deterministic signal fixture through replay, detection, policy, and action:

```bash
.venv/bin/elicio replay-demo --state-dir .elicio-replay-demo
```

Both print a JSON summary. A run succeeded only when it exits 0 and reports
`"verified": true`. Each writes a marker under `actions/` and appends to
`audit.jsonl` in the state directory.

The replay fixture is seeded synthetic data built with the standard library. It is
not a personal recording and does not validate any hardware path.

## Safety behavior

Confidence floors rise with consequence: 0.60 for harmless actions, 0.75 for
reversible edits, 0.85 for dangerous ones.

A dangerous action never runs from one event. It requires a separate `jaw_clench`
event at 0.85 or higher within three seconds, sourced from a different muscle group
so one twitch cannot produce both. Rest, unknown symbols, low-confidence events,
late confirmations, and out-of-order confirmations do not run actions.

An event selects a command. It never selects a file path or a shell string; the
adapter's target is fixed when the harness is built.

Auditing is fail closed. The intent record is written before the adapter runs, and
if that write fails the action is blocked. If the result record fails after the
action ran, the outcome reports the real result alongside the audit error rather
than hiding either.

## Tests

```bash
.venv/bin/python -m unittest discover -s tests -v
```

26 tests covering the event contract, every confidence floor, dangerous-action
confirmation and timeout behavior, rest handling, audit failure modes, the real
local marker effect, deterministic replay and detection, and cross-session leakage
rejection. Stdlib `unittest`; no pytest. The suite needs only the base install.

## Research pipeline

`src/elicio/pipeline/` is the migrated sEMG decoding pipeline from the Claude
Science project. It prepares public GRABMyo recordings, trains gesture decoders,
and scores them across sessions.

```bash
.venv/bin/python -m pip install -e '.[research]'
.venv/bin/elicio-emg prepare --subjects 1 2 3 --out-dir results
.venv/bin/elicio-emg train --data-dir results --subjects 1 2 3
.venv/bin/elicio-emg evaluate --data-dir results --subjects 1 2 3
```

Every reported number must be cross-session: train on one recording day, test on
another. Within-session accuracy on this data reads 98 to 99 percent and is
meaningless. `splits.py` is the only split API on purpose.

Training and evaluation are research workloads and were not rerun for the
engineering slice.

## Repository map

| Path | Contents |
| --- | --- |
| `src/elicio/harness/` | Event contract, risk policy, adapters, audit sinks |
| `src/elicio/signal/` | Replay fixtures and contraction detector |
| `src/elicio/pipeline/` | GRABMyo research pipeline |
| `docs/VISION.md` | Idea, origin, evidence, open questions |
| `docs/CLAUDE_SCIENCE_HANDOFF.md` | Scope, safety, and authority rules |
| `docs/RESEARCH_PROVENANCE.md` | Migration ledger and checksums |
| `AGENTS.md` | Engineering conventions for code assistants |
