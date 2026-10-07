# WP13b report — Receiver v2

Lane `w4`. Branch `lane/w4`. Final commit `e7c366a8191bf6abb26ab20045fabb5e70e23452`.
Worktree `/home/user/projects/elicio/.worktrees/w4`.

Host-only. No radio and no board were used.

## What was built

- `src/elicio/receiver_v2.py`: NUS packet ingest through `frame_v2.Reassembler`, session writer, `load_receiver_session` (returns `elicio.pipeline.load.Recording`), `receive-check`, fake transports. Loader name: `elicio.receiver_v2.load_receiver_session`.
- `elicio receive --device|--simulate|--simulate-live --out DIR` and `elicio receive-check DIR` in `src/elicio/cli.py`.
- `tests/test_receiver_v2.py` and `tests/fixtures/receiver_v2/`: every `frame-v2.md` case plus dropout, undervoltage, VBUS, and simulate-live. No BLE adapter.
- `firmware/src/board_pins.h` aligned to `docs/fab/board-v2.md` §9. The same table on `lane/w2` matches (w2 added a sentence above the table; pin numbers did not move).
- `docs/fab/receiver-v2.md`. One dated heading in `docs/fab/firmware-v2.md`.
- `pyproject.toml` optional extra `ble` (`bleak>=0.22`). Required by the brief; not on the Owns list otherwise.

Session files: `samples.npz` (int32 codes `[n,2]` plus metadata), `sidecar.json` (overrun, transport loss, wrap, reconnect, VBUS and undervoltage events), `meta.json`.

## Gates

1. `.venv/bin/python -m unittest discover -s tests -v`

   Result: exit 0. `Ran 179 tests in 84.407s` `OK (skipped=21)`. On a clean tree without matplotlib, 18 existing `PlacementV2Tests` SVG cases error (`matplotlib is not installed`). matplotlib 3.x was installed in this venv so those inherited tests run. They are not WP13b files.

2. `arduino-cli compile --fqbn adafruit:nrf52:feather52840 --library firmware --output-dir /tmp/elicio-firmware-build firmware/elicio_stream`

   Result: exit 0. Sketch uses 134012 bytes (16 %) of 815104. Global variables 18472 bytes (7 %) of 237568.

3. `git status --short` empty after the last commit.

Plan v2 §11 row 13 "builds in CI; bench-tested at S2": no CI in the repo. Host unittest and the compile above ran. S2 bench was not run (no board).

## What was installed

| Item | How | Size / version |
|---|---|---|
| bleak 3.0.2 | `.venv/bin/python -m pip install -e '.[ble]'` | 1.3 MB in site-packages |
| matplotlib | pip, so inherited placement SVG tests do not error | needed by `tests/test_placement.py` on this main, not by the receiver |

## What was not exercised

`receive --device` was not run on air. No Feather, no product board, no ADS1292, no gel montage. Same-criterion lines 3.5–3.10 stay `not_scored` without a detector log. The Feather FQBN compile treats nRF P0.n values as Arduino digital numbers; that is not a product wiring run.

A local unversioned `post-commit` hook ran `git push` after each commit on `lane/w4`. This lane did not invoke `git push`.

## Needs a decision

1. `receive-check` fails on montage §8 dropout (rail or flat > 200 sample intervals) even though table line 3.4 is marked "revised". 3.5–3.10 only fail when scored in the sidecar. Confirm that split for S2.
2. Product pin numbers in `board_pins.h` are not a Feather silkscreen map. A product variant or a `#ifdef` is still needed before a Feather is used as a wired stand-in.

## Final sha

`e7c366a8191bf6abb26ab20045fabb5e70e23452`
