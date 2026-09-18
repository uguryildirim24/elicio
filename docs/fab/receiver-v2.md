# Receiver v2 (WP13b)

Host tool for S2. It records a frame v2 BLE NUS stream on the Mac, or
replays a fixture through the same path. No radio and no board were
used in this package.

Loader: `elicio.receiver_v2.load_receiver_session`. It returns
`elicio.pipeline.load.Recording` (float32 signal from int32 ADS codes,
labels, sample rate 2000, channels `ADS_CH1` and `ADS_CH2`). The
nominal scale is not applied.

## Pair, record, check

1. Install the BLE extra once: `.venv/bin/python -m pip install -e '.[ble]'`.
2. Put the board in range. Firmware advertises `elicio-v2`.
3. Record:

   `.venv/bin/python -m elicio.cli receive --device elicio-v2 --out recordings/s2-gel`

   You can pass a BLE address instead of the name. Stop with Ctrl+C, or
   pass `--seconds`.
4. Check:

   `.venv/bin/python -m elicio.cli receive-check recordings/s2-gel`

   Exit 0 only when there is no rail or flat stretch longer than 200
   sample intervals (montage §8 dropout rule) and no scored
   same-criterion line has failed. 3.5 to 3.10 stay `not_scored` until
   a detector log is written into `sidecar.json`.

Without a board, use the same commands with a fixture:

`.venv/bin/python -m elicio.cli receive --simulate tests/fixtures/receiver_v2/normal.json --out /tmp/elicio-recv`

`.venv/bin/python -m elicio.cli receive --simulate-live --out /tmp/elicio-recv-live`

`--simulate-live` feeds the Python framer through a fake NUS with
fragmentation (MTU 20), one dropped frame, reordered fragments, and a
HELLO reconnect.

## Output files

| File | Contents |
|---|---|
| `samples.npz` | int32 `codes` `[n, 2]`, `status`, extended `acq_index`, `flags`, `labels`, `sample_rate`, `subject`, `session`, `channel_names` |
| `sidecar.json` | overrun, transport-loss, wrap and reconnect counts; decode errors; HELLO/VBUS/undervoltage events; battery messages |
| `meta.json` | format name, loader name, MTU, session id |

## Pin map

`firmware/src/board_pins.h` matches `docs/fab/board-v2.md` §9. A test
parses both. The streaming sketch still compiles for the Feather FQBN.
Those nRF numbers are not Feather silkscreen pins.

## What was not exercised

No BLE adapter session, no board, no ADS1292, no gel montage. `receive
--device` was not run on air. pyOCD and a Debug Probe were not used.
Same-criterion lines 3.5 to 3.10 need detector events and were not
scored.
