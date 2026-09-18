# WP13 — Firmware v2: frame contract, receiver fixtures, streaming firmware (lane w4)

Read `tasks/phase1-common.md` first (for this package "the plan" is
`docs/fab/plan-v2.md`, signed off at `ef369bd`), then plan v2 §5.5
(undervoltage), §6 in full, §8 (first load), §11 row 13, §12;
`docs/fab/open-questions.md` Q37 to Q49; `docs/fab/montage.md` (the
protocol v1 lines); `tasks/plan/protocol.md`; the existing `elicio`
package and its tests (they stay green). Lane `w4`, worktree
`/Users/rolfie/projects/elicio/.worktrees/w4`, branch `lane/w4`. Start
line (coordinator restarts you by copy-paste):

    herdr agent start w4 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

First: `git merge --ff-only main` in your worktree (your branch is behind).

Why: plan v2 §6 requires a byte-level frame contract frozen before S0,
receiver fixtures for every failure case, and firmware that streams the
ADS1292 at 2000 SPS over BLE NUS with that frame. No hardware exists yet;
everything here is built, compiled and tested on the host. You order
nothing and contact nobody.

Owns: `firmware/` (new), `docs/fab/frame-v2.md` (new),
`docs/fab/firmware-v2.md` (new), `elicio/frame_v2.py` (new decoder module),
`tests/test_frame_v2.py` (new), and the protocol v2 mapping table appended
to `docs/fab/montage.md` under a new heading (nothing above it changes).

Toolchain (Q45, Q46): choose between the Adafruit nRF52 Arduino core built
with `arduino-cli` (Homebrew, then the Adafruit board index; the Feather
nRF52840 Express variant as the build target with our pin map in one
header, stated as such) and Zephyr with `west` (larger). Free software, no
accounts. Say in the report which you chose, why, what you installed and
how big it was. If the install fails, push WAITING with the error.

Deliver:

1. `docs/fab/frame-v2.md`: the versioned byte-level format per §6: session
   or epoch id, frame sequence, an acquisition index tied to ADS
   conversions (DRDY count), not to successful reads; sample count and
   payload length; gain, reference and rate metadata; ADS status handling;
   fragment identification and reassembly for the negotiated MTU; counter
   width and wrap (a 16-bit index at 2000 SPS wraps every 32.768 s; if you
   choose wider, say why); reconnect and reset behaviour; partial-frame
   rejection; acquisition overrun reported separately from transport loss;
   a CRC; battery telemetry every 10 s as its own message; the invalid
   sample and stop/restart reason fields for the undervoltage rule; the
   nominal scale 2.42 V / (12 × (2^23 − 1)) per code as metadata only.
2. `elicio/frame_v2.py`: a decoder and reassembler for that format, plus a
   Python framer that produces frames from a sample source (the model of
   the firmware's framer). `tests/test_frame_v2.py`: golden byte vectors
   committed under `tests/fixtures/frame_v2/` for every case (normal, wrap,
   fragment, reorder, loss, overrun, partial frame, reconnect, bad CRC,
   version mismatch), the decoder against the Python framer, and a
   round-trip test against the firmware framer compiled natively (item 3).
3. `firmware/`: the application: ADS1292 SPI driver (register set for 2000
   SPS, gain 12, internal reference, RLD on, lead-off off, non-R), DRDY
   interrupt into a ring buffer, the framer as a portable C module with no
   hardware dependency (compiled and unit-tested on the host with clang in
   `tests/` through a small harness, and used by the target build), NUS
   transport with MTU negotiation, the undervoltage state machine with
   V_STOP and V_START as named constants marked "from WP12" and the
   derivation cross-referenced, "VBUS present → streaming refused", battery
   telemetry every 10 s, the recovery path documented as the Adafruit
   bootloader's own double-reset. The target build compiles with the
   command in `firmware-v2.md` (output in the report). No hardware claim.
4. `docs/fab/firmware-v2.md`: build and flash commands (the Debug Probe
   with pyOCD or OpenOCD, documented, not installed unless needed), the
   merged bootloader image plan (which Adafruit bootloader release, its
   URL, flash layout, USB identity; no download needed this round), the
   update and recovery tests WP13 owes G4, and what could not be exercised
   without hardware, in plain words.
5. The protocol v2 mapping table in `montage.md`: every v1 criterion line
   mapped "same criterion" or "revised: why" per §6 (input-referred µV,
   the INA128 shift criterion restated as ± 50 mV input-referred, dropout as
   more than 200 sample intervals, transport loss beside it), with start-up
   exclusions named. Where a line cannot be mapped yet, say "open: needs
   S2 data", never a silent guess.

Gates: `.venv/bin/python -m unittest discover -s tests -v` green including
the new tests and the native framer harness; the target firmware compiles;
`git status --short` empty. Commit in steps; the last commit is
`firmware(v2): frame contract, receiver, streaming app`. Report
`.reports/WP13-report.md` (untracked): what was built, each gate with
command and result, what was installed, what was not done, "Needs a
decision", the final sha. Closing steps per the common file with `<PKG>` =
`WP13`, `<lane>` = `w4`. A mid-package prompt from the coordinator runs
after your DONE as a new turn; push another DONE for it.
