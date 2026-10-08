# Elicio

Elicio is an unfinished ear-muscle EMG earpiece that is intended to turn a deliberate contraction into a gated event before an AI acts.

Rolf chose a discreet physical input rather than an always-active command channel. The sensor should propose an event. Policy should decide whether that event can act. Sensing, permission and execution remain separate.

```text
ear-muscle EMG -> decoder -> (symbol, confidence, timestamp) -> policy -> action
```

**The board is not finished, has not been ordered and is unmeasured.** No physical earpiece, real ear-muscle recording or end-to-end biological action has been validated. The runnable demonstrations use synthetic input. Only a harmless local file action is real. No AI execution adapter is implemented.

## What exists

| Part | Files and present evidence |
| --- | --- |
| Flex board | [KiCad schematic](hardware/board/elicio-v4.kicad_sch), [routed PCB](hardware/board/elicio-v4.kicad_pcb), project rules and generation/routing scripts. Design files are not manufacturing approval. |
| Scripted shell | [Selected snap-shell exports](docs/fab/cad/v4-snap/) include STEP, STL, 3MF and a nominal-check manifest. No print, fit or retention result. |
| Firmware | [Arduino stream firmware](firmware/elicio_stream/elicio_stream.ino) and C sources for ADS1292 acquisition, binary BLE frames and undervoltage handling. The product Arduino variant is missing. |
| Receiver | Binary frame decoding, dropout/loss records and session files. Committed synthetic transport fixtures run without a radio. |
| Action gate | Confidence policy, confirmation state, intent/result auditing and an atomic local marker write. Other action names are console simulations. |
| Research pipeline | Public forearm sEMG preparation and cross-session evaluation code. No result CSVs, checkpoints or measured accuracy reports are bundled. |

![Selected snap-shell CAD preview, not a physical device](docs/fab/cad/v4-snap/render_closure.png)

The snap manifest records **106 passing nominal geometry checks**. These cover simplified board courtyards, a folded-flap envelope, seated overlap, key clearance and opposing tolerance offsets. They do not prove printed fit, latch fatigue, component loads, electrical safety or RF range. The nominal body is 18 mm wide and 8.1 mm thick, not the complete hook bounding box. See [shell limits](docs/fab/shell-v4.md) and [board blockers](docs/fab/board-v4-design.md).

## Run from a clean clone

Run these commands from the repository root on macOS or Linux. Use Python **3.11 or newer**. The base install requires NumPy. No credentials or hardware are needed for the demos.

```bash
python3 --version
python3 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/elicio demo --state-dir .elicio-demo
.venv/bin/elicio replay-demo --state-dir .elicio-replay-demo
```

Each demo must exit 0 and print `"verified": true`. It writes a marker under `actions/` and linked `intent` and `result` records in `audit.jsonl` inside its ignored state directory. The replay fixture is seeded synthetic data, not an EMG recording or a hardware test.

### Binary receiver without hardware

```bash
.venv/bin/elicio receive --simulate tests/fixtures/receiver_v2/normal.json \
    --out recordings/synthetic-session
.venv/bin/elicio receive-check recordings/synthetic-session
```

`receive` writes `samples.npz`, `sidecar.json` and `meta.json`. `receive-check` reports acquisition statistics and criterion status; the normal fixture exits 0 with `"ok": true`. Its gesture criteria are `not_scored`, not passed. This is transport validation, not gesture decoding or a connection to the action gate.

The intended radio path uses binary frame-v2 messages over Nordic UART Service, not ASCII serial samples. Live reception requires the optional BLE dependency and future functioning hardware:

```bash
.venv/bin/python -m pip install -e '.[ble]'
.venv/bin/elicio receive --device ELICIO --seconds 10 --out recordings/bench-session
.venv/bin/elicio receive-check recordings/bench-session
```

The live commands are not usable or validated with this unfinished board. The firmware deliberately rejects a Feather pin variant. See [firmware limits](docs/fab/firmware-v2.md), [frame format](docs/fab/frame-v2.md) and [receiver contract](docs/fab/receiver-v2.md).

The separate `scope`, `capture` and `replay-recording` tools accept one ASCII sample per line from a file, stdin or an already configured serial device. They are bench utilities, not the binary BLE path. Store captures under ignored `recordings/`, for example `--out recordings/session.json`. Run `elicio capture --help` for the sample-rate, offset and gain arguments.

### Existing tests

```bash
.venv/bin/python -m unittest discover -s tests -v
```

The scope review ran the base install, both synthetic action demos and the normal receiver fixture in the worktree with Python 3.13.15. They exited 0. Both demos reported `verified: true`; the receiver check reported `ok: true` with gesture criteria unscored.

The full existing suite was attempted but stopped at a 180-second command limit while setting up the restored packing checks. A historical document wording assertion failed before that point. Its expected reference wording was restored, and that existing test passed when rerun alone. The documented `bte_fit_shell.py --checks-only` reference check and `elicio capture --help` also passed. No complete suite pass is claimed. The original tests and historical-byte comparisons remain unchanged. No tests or CI were added.

Optional dependency groups are `research`, `ble`, `cad` and `sheets`. Install an extra with, for example, `.venv/bin/python -m pip install -e '.[cad]'`. Native C checks use a compiler when available. KiCad/pcbnew, firmware tooling, Blender or SceneKit are separate toolchains. Optional CAD exports, rendering, KiCad release validation, firmware flashing and live acquisition were not rerun during the scope review. Research downloads and training were skipped as substantial workloads.

## Research and local data

The research package fetches public PhysioNet/WFDB GRABMyo records. It studies forearm gestures, not auricular decoding. From the repository root:

```bash
.venv/bin/python -m pip install -e '.[research]'
.venv/bin/elicio-emg prepare --subjects 1 2 3 --out-dir results
.venv/bin/elicio-emg train --data-dir results --subjects 1 2 3 \
    --epochs 20 --out results/train_results.csv
.venv/bin/elicio-emg evaluate --data-dir results --subjects 1 2 3 \
    --epochs 20 --out results/six_best_rest.csv
```

These are download and training workloads, not quick demos. They were not rerun during cleanup. Training is not fully seeded. Evaluation uses separate recording sessions and a leakage guard. Earlier imported accuracy summaries lack supporting result artifacts here and are not claimed as repository results. See the [pipeline instructions](src/elicio/pipeline/README.md) and [provenance limits](docs/RESEARCH_PROVENANCE.md).

Keep raw recordings in `recordings/`, research outputs in `results/`, anatomy parameters in `measurements/` and generated CAD/release output in `.reports/`. These directories, environments, checkpoints, secrets and runtime state are ignored. Tracked binary fixtures are synthetic. No completed personal ear measurements or purchase records are included. Do not put delivery addresses, checkout details or credentials in public examples.

## Limits and next steps

- Confidence thresholds are policy settings, not calibrated biological probabilities.
- The timed `jaw_clench` confirmation rule checks symbols, confidence and timestamps. The event tuple cannot prove that command and confirmation came from independent muscle groups. That is an unvalidated upstream requirement.
- Intent audit failure blocks execution. A result-audit failure after execution is reported without hiding the completed action.
- There is no trained ear-muscle decoder, real signal-to-action result or AI execution adapter.
- The circuit, cell, charging protection, RF keep-out, programming path and manufacturing acceptance remain open. CAD and a clean DRC claim cannot establish on-body safety.
- This is not a medical device or a finished wearable. Do not wear or charge unvalidated electronics on a body.

Next: resolve electrical and fabrication blockers, implement the product firmware variant, validate passive printed fit and repeated latch retention, then record a real signal and demonstrate one harmless audited action. See [design status](docs/EARPIECE_DESIGN.md) and [open gates](docs/fab/open-questions.md).

## Project layout

| Path | Purpose |
| --- | --- |
| `src/elicio/harness/` | Events, policy, adapters and audit |
| `src/elicio/signal/` | Synthetic replay, detection and ASCII capture |
| `src/elicio/frame_v2.py`, `receiver_v2.py` | Binary BLE transport and session reception |
| `src/elicio/pipeline/` | Public-data research pipeline |
| `hardware/board/` | KiCad sources, custom footprints and board scripts |
| `firmware/` | Acquisition, framing and power-state sources |
| `scripts/cad/`, `scripts/sheets/` | Parametric CAD, previews and reference templates |
| `docs/fab/cad/v4-snap/` | Selected shell candidate and nominal evidence |
| `tests/` | Existing unit checks and synthetic transport fixtures |
| `docs/` | Design limits, provenance and engineering references |

Older v1/v2 geometry, packing tables, layout searches, board-edit scripts and their existing checks remain. They are reference inputs and development tools, not active ordering instructions. `placement.py` still supports `--packing-doc`, `--layout-v2` and `--layout-v2c`. Some older readers use pinned Git revisions. They are not independent of repository history, and history scrubbing can invalidate those references. The technical L1 to L8 source surveys remain with historical notices. The [reference index](docs/fab/references.md) lists key public sources. Task and review dialogue is omitted.

The rejected M1.6 closure remains as diagnostic code and evidence in `docs/fab/cad/v4-m16/`. It is not suitable for printing. The snap candidate is still untested physically. Private agent diaries, personal parameter scaffolding and superseded shopping sheets were removed. Historical budgets are estimates, not quotes or personal spending statements.

## How this was built

AI coding agents did much of the research migration, harness and receiver implementation, firmware, CAD and board work under Rolf's direction. Rolf set the physical-gating goal, chose the earpiece form, titanium contacts, limited final assembly and off-ear-only charging, and reviewed design previews. The checks reported here are automated software and nominal geometry checks. Agent-written engineering claims are not independent electrical review or physical measurements. No hardware result has been measured.

## License and citation

Original project code, hardware design files and documentation are offered under [MIT](LICENSE). The bundled Liberation Sans font is separate: SIL Open Font License 1.1, with Google and Red Hat attribution in [the font notice](scripts/cad/fonts/OFL.txt). External datasets, dependencies and vendor materials retain their own terms.

No Elicio paper or preprint is included in this repository. Public engineering source pointers are in [references](docs/fab/references.md).
