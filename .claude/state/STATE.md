# State: Elicio hardware selection and ingestion path

Updated: 2026-08-12 17:00 · Branch: main · Status: in progress

## Goal

Pick a sEMG sensor the owner can actually buy and wear, then build the ingestion
path that turns its samples into the harness's `(symbol, confidence, timestamp)`
event. Done looks like: one real muscle contraction, decoded on the owner's own
arm, completing one real harness action. Not there yet — no hardware purchased.

## Current position

The software boundary works and is committed. This session went to hardware
selection and to repairing several claims of mine that turned out to be wrong. No
device ordered. Next executable action is the `SampleSource` protocol plus a
simulated source, which is useful whichever sensor wins.

## Done

- `docs/VISION.md` — band survey against four gates (raw access, >=500 Hz,
  offline, US shipping). No device under $500 clears all four. Commit `fe2bf69`.
- `.venv` rebuilt. It had silently ignored `.pth` files, so the editable install
  never reached `sys.path` and both console scripts were broken. Now: 26 tests
  pass with the bare documented command, both demos print `"verified": true`.
- `.gitignore` — added `.claude/state/` and `.elicio-replay-demo/`.

## Not committed, and why

`.claude/state/fusion_3dc_imu.py` and `..._results.txt` — an exploratory run on
the public 3DC Armband dataset. **These are not project evidence and must not
enter `docs/RESEARCH_PROVENANCE.md`.** AGENTS.md requires every evaluation split
to use `cross_session_split` with `assert_no_session_leakage` and forbids
same-session splits as proof. 3DC trains and tests five minutes apart with the
band never removed, so it has no session dimension and cannot be rerun under the
mandated split. I initially wrote these results into the provenance ledger; that
was a rule violation and was reverted before pushing.

What the run suggests, as a directional hint for purchasing only, never as an
accuracy claim: separability tracks vocabulary size more than channel count, and
IMU fusion with absolute orientation hurts while delta-only encoding is roughly
neutral. Both would need cross-session data on the owner's own arm to mean
anything.

## Next steps

1. Write `SampleSource` protocol + simulated source, behind which windowing,
   offset removal and recording sit. Transport-agnostic — MyoWare is BLE/ESP32,
   NPG Lite is BLE/serial, and the winning transport gets added last.
2. Add a recording mode so sessions on different days can be captured. This is
   the only route to the cross-session answer no public dataset can give.
3. Email Wearable Devices (raw SNC per-channel Hz; RawData license cost for an
   individual) and Crowd Supply (real NPG Lite ship date, warehouse country).
4. Only then buy.

## Key decisions

- sEMG over EEG, on amplitude grounds. Recorded rationale, not settled physics —
  see `docs/VISION.md`.
- Rebuilding the 3DC Armband rejected: custom ASIC unobtainable, MSP430F5328IZQE
  at Last Time Buy, ICM-20948 EOL, nRF24 NRND, and its PMU rails are too low for
  every candidate replacement AFE. That is a redesign, not a rebuild.
- Buy nothing until the two vendor questions are answered.

## Gotchas and context

- **Three corrections this session, all mine.** (1) I claimed
  `CLAUDE_SCIENCE_HANDOFF.md` requires laptop-on-battery operation. It does not —
  its safety section is lines 92-99 and says nothing of the kind; that rule came
  from Upside Down Labs' docs. (2) A laptop on battery is *not* isolation: USB
  still galvanically ties skin electrodes to the computer. Wear the sensor on its
  own battery over BLE; USB for bench programming only, never while worn.
  (3) I wrote same-session results into the evidence ledger, against an explicit
  AGENTS.md rule. Reverted.
- Neither MyoWare nor NPG Lite is a wristband. Both are boards. Strap, lead
  routing and dry-electrode integration remain hardware work either way.
- Best sEMG signal is upper forearm, not the wrist — the muscles driving wrist
  flexion and extension sit 5-10 cm below the elbow.
- MyoWare DEV-21265 is retired; the live SKU is DEV-27924. Its stock BLE example
  streams *envelope* as ASCII strings in a free-running loop with no timestamps,
  so it is unusable for this pipeline. RAW is reachable on ESP32 pin A4.
- GRABMyo accuracy figures will not transfer to either device: that data is
  2048 Hz, MyoWare RAW is bandpassed 20-500 Hz, NPG Lite runs 500 Hz.
- Pipeline training is unseeded, so `train`/`evaluate` do not reproduce exactly.
- Run tests with `.venv/bin/python -m unittest discover -s tests` — pytest is not
  used and there is no conftest.
- System clock reads 2026-08-12; earlier session context said 2026-08-10. Dated
  claims in `docs/VISION.md` say "verified 2026-08-10" and are off by two days.

## Open questions

- Mudra Link: raw SNC per-channel sample rate, and RawData license cost for an
  individual. Blocked on the vendor.
- NPG Lite: true ship date and warehouse country. Crowd Supply lead times on the
  page are stale — one pack advertises a date already past.
- Cross-session stability on the owner's own arm. Unanswerable without hardware.

## Pointers

- `docs/VISION.md` — band survey, electrode evidence, hardware rationale.
- `docs/RESEARCH_PROVENANCE.md` — migrated-artifact provenance. Cross-session
  evidence only.
- `docs/CLAUDE_SCIENCE_HANDOFF.md` — authority limits; line 94 forbids publishing
  without explicit approval.
- Remote `git@github.com:uguryildirim24/elicio.git`, verified private.

## Checkpoint Log

- 2026-08-12 17:00 — Band survey committed; venv repaired; same-session fusion
  results kept out of the evidence ledger; two safety/attribution claims retracted.
