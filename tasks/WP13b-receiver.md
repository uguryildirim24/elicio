# WP13b — Receiver: record a stream on the Mac, and the pin map (lane w4)

Read `tasks/phase1-common.md` first (for this package "the plan" is
`docs/fab/plan-v2.md`, signed off at `ef369bd`), then plan v2 §6, §10
(S2), §11 row 13; `docs/fab/open-questions.md` Q45, Q52, Q57 to Q68;
`docs/fab/frame-v2.md`, `docs/fab/firmware-v2.md`, `src/elicio/frame_v2.py`,
`docs/fab/board-v2.md` §9 (the GPIO map, which WP12b may revise on
`lane/w2`; read `git show lane/w2:docs/fab/board-v2.md` before you finish
and take the newest map); `tasks/reviews/code-r5.md` defects 10 to 14.
Lane `w4`, worktree `/Users/rolfie/projects/elicio/.worktrees/w4`, branch
`lane/w4` (fast-forwarded to `main` at the round 5 merge). Start line
(coordinator restarts you by copy-paste):

    herdr agent start w4 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Why: S2 (the bench) needs something on Rolf's Mac that connects to the
board, records the stream with its loss and overrun accounting, and
writes files the existing pipeline reads. The decoder exists; the
receiver does not. The firmware's pin header must follow the board's
final map. No hardware exists; everything is tested against the Python
framer and a simulated BLE source.

Owns: `src/elicio/receiver_v2.py` (new), the `elicio` CLI's new
subcommand(s) in the existing entry point, `tests/test_receiver_v2.py`
(new), `tests/fixtures/receiver_v2/` (new), `firmware/src/board_pins.h`
(the map only), `docs/fab/receiver-v2.md` (new), one dated line in
`docs/fab/firmware-v2.md` under a new heading when the pin header
changes. Nothing else in `firmware/`.

Deliver:

1. `elicio receive --device <name|address> --out <dir>`: BLE central with
   `bleak` (add it as an optional dependency group `ble`), NUS
   subscription, MTU as negotiated, frame v2 reassembly through
   `frame_v2.py`, a session file per connection (samples as int32 codes
   plus the metadata, in the format the existing pipeline's loaders read;
   name the loader you target and add a reader test), a sidecar with
   acquisition-overrun and transport-loss counts, reconnects, the
   undervoltage and VBUS flags surfaced as events; `--simulate <fixture>`
   replays a recorded fragment stream through the same code path without
   a radio, and `--simulate-live` feeds the Python framer through a fake
   transport with injected loss, reorder, fragmentation and reconnect.
   Tests cover every case of `frame-v2.md` through the receiver, not only
   the decoder.
2. `elicio receive-check <session dir>`: prints sample count, duration
   from acquisition indices, wraps, overruns, losses, flat or railed
   stretches by the montage §8 dropout rule (more than 200 sample
   intervals), and exits non-zero on a criterion the montage table marks
   "same criterion" that fails; that is the S2 dry-check tool.
3. `firmware/src/board_pins.h` aligned to `board-v2.md` §9 (newest map on
   `lane/w2` if it moved), with a test that parses both and compares; the
   sketch still compiles (`arduino-cli compile`, command and output in
   the report).
4. `docs/fab/receiver-v2.md`: how Rolf runs it at S2 in plain prose (pair,
   record, check), what each output file is, what was not exercised
   (no radio, no board).

Gates: `.venv/bin/python -m unittest discover -s tests -v` green (the BLE
tests must not need a radio: the transport is an interface with the
fake in tests); `arduino-cli compile` exit 0; `git status --short`
empty. Commit in steps; the last commit is `receiver(v2): record and
check a stream on the Mac`. Report `.reports/WP13b-report.md`
(untracked): what was built, each gate with command and result, what
was installed (bleak), what was not exercised, "Needs a decision", the
final sha. Closing steps per the common file with `<PKG>` = `WP13b`,
`<lane>` = `w4`. A mid-package prompt from the coordinator runs after your
DONE as a new turn; push another DONE for it.
