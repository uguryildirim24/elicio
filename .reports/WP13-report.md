# WP13 report — Firmware v2

Lane `w4`. Branch `lane/w4`. Final commit `28b284c1908760c946971ae1bd66f3c1feee4e70`.
Worktree `/home/user/projects/elicio/.worktrees/w4`.

Host-only. No hardware was programmed or measured.

## What was built

- `docs/fab/frame-v2.md`: versioned little-endian NUS fragment format (HELLO, STREAM, BATTERY), 16-bit `acq_index` (DRDY count, wrap 32.768 s), CRC-32/ISO-HDLC, fragment reassembly, overrun vs transport loss, reconnect, VBUS and undervoltage flags, nominal scale as metadata.
- `src/elicio/frame_v2.py`: Python framer, decoder, reassembler.
- `tests/test_frame_v2.py` and `tests/fixtures/frame_v2/`: golden bytes for normal, wrap, fragment, reorder, loss, overrun, partial, reconnect, bad CRC, version mismatch; Python vs clang native framer.
- `firmware/`: portable C framer, ADS1292 worn register set (2000 SPS, gain 12, internal 2.42 V, RLD on, lead-off off, non-R), undervoltage machine with `V_STOP_MV` / `V_START_MV` marked from WP12, Feather stand-in pin header, `elicio_stream` Arduino sketch (BLE NUS, MTU request 247, DRDY ring 256, battery every 10 s, VBUS refuses streaming, acquisition continues while disconnected).
- `docs/fab/firmware-v2.md`: build, flash, bootloader 0.11.0 URL (no download), flash map, USB identity, G4 tests, what was not run.
- `docs/fab/montage.md` §8: protocol v2 mapping table. Nothing above that heading was edited.

## Gates

1. `.venv/bin/python -m unittest discover -s tests -v`

   Result: exit 0. `Ran 142 tests in 15.102s` `OK (skipped=22)`. Skips are existing CAD/render tests that need build123d or matplotlib, not this package. All 13 `test_frame_v2` cases passed, including the native clang harness.

2. Target firmware compiles.

   Command (Adafruit gcc 9-2019q4, core default, Rosetta):

   ```bash
   arduino-cli compile --fqbn adafruit:nrf52:feather52840 \
     --library firmware \
     --output-dir /tmp/elicio-firmware-build \
     firmware/elicio_stream
   ```

   Result: exit 0. Sketch uses 133276 bytes (16 %) of 815104. Global variables 18472 bytes (7 %) of 237568.

   Same sketch with Arm GNU 15.3.1 (`compiler.path=/Applications/ArmGNUToolchain/15.3.rel1/arm-none-eabi/bin/`): exit 0, 125408 bytes (15 %), 18764 bytes RAM (7 %).

3. `git status --short` empty after the last commit.

## Plan v2 acceptance

- §11 row 13 "builds in CI; bench-tested at S2": no CI workflow exists in this repo. The host unittest and the two `arduino-cli compile` commands above are what ran. Bench at S2 was not run (no board).
- G6 (protocol v2 table): written as `montage.md` §8. 3.1–3.3 revised (same numbers on the ADS path, named filter and windows). 3.4 revised (dropout 200 sample intervals; ± 50 mV input-referred; transport loss beside dropout). 3.5–3.10 same criterion. Input and common-mode headroom: open: needs S2 data. Start-up exclusions named. No dry data was scored.
- G4 pieces this package owns (merged image identity, application layout, USB ids, update and recovery tests): documented in `firmware-v2.md`. Not executed on hardware.

## What was installed

| Item | How | Size |
|---|---|---|
| arduino-cli 1.5.1 | Homebrew | 25 MB |
| Adafruit nRF52 1.7.0 | `arduino-cli core install adafruit:nrf52` | 892 MB under `~/Library/Arduino15/packages/adafruit`; Arduino15 total 1.3 GB |
| Arm GNU Toolchain 15.3.rel1 | Homebrew cask `gcc-arm-embedded` | 1019 MB |
| `arm-none-eabi-gcc` 16.2.0 | Homebrew formula | 540 MB; unused (no newlib/libstdc++) |
| `arm-none-eabi-binutils` 2.47 | Homebrew formula | 19 MB |
| Rosetta 2 | `softwareupdate --install-rosetta --agree-to-license` | required for x86_64 ctags and Adafruit gcc 9 |

Q45 choice: Arduino-cli + Adafruit nRF52 core, not Zephyr. Reason: stand-in FQBN, `BLEUart` NUS, Adafruit UF2 bootloader either way, no Nordic account, smaller install. Zephyr/`west` was not installed.

## What was not done

No Feather, Debug Probe, Tag-Connect, ADS1292, cell, or BLE peer. pyOCD and OpenOCD were not installed. Bootloader 0.11.0 hex was not downloaded. First-load, UF2 update, double-press recovery, VBUS on a cable, 2000 SPS on air, and pack undervoltage were not run. Product pin map and computed V_STOP/V_START wait on WP12. Plan v2 §6 names Zephyr; this tree is Arduino.

A local unversioned `post-commit` hook ran `git push` after each commit on `lane/w4`. This lane did not invoke `git push`. The user rule was never push.

## Needs a decision

1. Plan v2 §6 says nRF Connect SDK (Zephyr). Q45 told this lane to choose Arduino or Zephyr. Arduino was chosen. Confirm or require a Zephyr port before S0.
2. `V_STOP_MV` 2700 and `V_START_MV` 2800 are placeholders (ADS1292 AVDD min, plus 100 mV). Replace with WP12's computed pack millivolts.
3. Feather USB identity and bootloader board id stand in for the product module. WP12's board needs its own 0.11.0 hex when that PCB exists.
4. Montage §8 input and common-mode headroom: open until S2 data.

## Final sha

`28b284c1908760c946971ae1bd66f3c1feee4e70`
