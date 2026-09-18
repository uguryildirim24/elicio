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

   The exit code says what it found (table below). 3.5 to 3.10 stay
   `not_scored` until a detector log is written into `sidecar.json`.

Without a board, use the same commands with a fixture:

`.venv/bin/python -m elicio.cli receive --simulate tests/fixtures/receiver_v2/normal.json --out /tmp/elicio-recv`

`.venv/bin/python -m elicio.cli receive --simulate-live --out /tmp/elicio-recv-live`

`--simulate-live` feeds the Python framer through a fake NUS with
fragmentation (MTU 20), one dropped frame, reordered fragments, and a
HELLO reconnect.

## Exit codes of `receive-check`

Montage §8's table marks only lines 3.5 to 3.10 "same criterion". Line
3.4 is marked "revised"; its dropout half keeps the original rule (rail
or flat for more than 200 sample intervals, counted on the acquisition
stream). The tool follows the table: a same-criterion failure and a 3.4
dropout get different codes. Whether a 3.4 dropout stops S2 is an open
decision in `tasks/reviews/code-r6.md`; until it is taken, treat code 3
as a stop and write the agent one line.

| Code | Meaning |
|---:|---|
| 0 | No dropout; no scored same-criterion line failed |
| 1 | A scored same-criterion line (3.5 to 3.10) is not `pass` (wins over 3) |
| 2 | Not a session folder (`samples.npz`, `sidecar.json` or `meta.json` missing) |
| 3 | A line 3.4 dropout: rail or flat for more than 200 sample intervals |

Not scored for dropout (montage §8 start-up exclusions): samples flagged
INVALID, the 200 conversions after each RESTART flag, and OVERRUN gaps
(a gap in `acq_index` ends a run). A gap in `frame_seq` is transport
loss; it is counted beside dropout, never as dropout.

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
