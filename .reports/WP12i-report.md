# WP12i — board v3 (WIP, stopped)

Lane: `w2` (`lane/w2`). Pane: `w1B:pB`.
Stopped on Rolf's PAUSE: machine out of memory; CAD failing. No tests, builds, renders or router after that line.

## What was built

### Phase A (before pin table v3) — `03f031c`

- U2 land vs ADS1292 4219108/B: pitch 0.40 mm (Q98 0.50 was wrong). Pads 0.55 × 0.20, C 3.85, EP 2.8. Footprint `elicio:Texas_RSM0032`.
- U3 YFP kept. Balls escape radially. No BOM swap.
- Q95: R9/R10 DNP; off PCB, BOM and CPL.
- Q94: nine stiffener drawings. Extra fee UNVERIFIED.
- Q97 tests: one Contact net per strip; no foreign via in a land 7 × 7; island exposed Contact is R1–R3.
- §5e parser and `vendor_pin_table`.

### Step 3 on prompt `pin table v3 ab9ce95` — `0da86a0` then this WIP commit

- `git merge origin/main` (never rebase). `docs/fab/packing-v2.md` on this tree still has no §5e. Source of truth: `ab9ce95` / lane w3.
- Vendored §5e into `hardware/board/packing_v2_flat.md` (66 rows, R9/R10 out, Q98 boxes).
- Re-pin on v3: H1 (13.23, 17.70), H2 (17.95, 17.70), J4 (16.52, 24.60) rot 90, J2 (15.15, 11.35) rot 0, J3 (28.41, 26.80), P4 (23.32, 4.35), P5 (23.32, 12.35), U2 B.Cu under SW1.
- Flat outline: charge tab from pocket high-u (20.50); J3 break-off neck 2.5 mm; cut line u=22.25 on Dwgs.User and F.Fab. J3 north edge grown so pad 3 meets copper-to-edge 0.30.
- Q98 named rule areas on the PCB: HOLE_CH, U2_CH, U3_CH, J4_CH, J4_VIA_SLOT, J4_APPROACH_EAST.
- Zero-track DRC: **0 errors** (144 unconnected).
- Locked Contact: SIG1 ring → strip → R1; SIG2 and REF ring → strip to the island edge only. After that lock: DRC **0 errors**, 143 unconnected, 11 segments (`0da86a0`).
- `hand_route.py`: DRC-revert by file copy (pcbnew `Remove` leaked SWIG and broke `GetTracks`). VBUS P4 sort key uses u > 22.

## What failed / was not done

- Island SIG2 → R2 and REF → R3: hand A* produced DRC (shorts, crossings, edge). Not kept. **Failed.**
- J3 SIG1/SIG2/REF A*: every kept pair raised DRC. A first run left 9 DRC errors because revert by `Remove` did not restore; board was put back to the strips PCB. **Failed.**
- `hand_route.py --group vbus` then `j4` then `u2`: started; Rolf PAUSE interrupted the loop. The owned PCB now has extra VBUS and nRESET segments from that run. DRC was **not** re-run after the interrupt (PAUSE: no tests, builds, renders or router).
- Freerouting: **not run.**
- DRC 0 with 0 unconnected: **not reached.**
- `release.py --routed` with `routed: true`: **not run.**
- Gerbers, BOM, CPL after a closed route: **not done.**
- `docs/fab/board-v2.md` §15 and `hardware/board/route.md` §13 for a closed route: **not written.**
- Board unittest suite after the interrupt: **not run** (PAUSE).

`routed`: false.

## Named geometry (island Contact)

R2 pad 1 SIG2 (19.070, 33.340) rot 90 and R3 pad 1 REF (19.070, 31.340) sit on the same u. U4 pad 5 (+3V0) occupies u 17.13–18.45 at s 34.65. Island east edge is 19.75 (Contact centre must stay ≤ 19.375 for 0.30 copper-to-edge). A* could not join those pads on one layer without a short or a crossing. J3 PTH pads at (28.41, 26.80 / 29.34 / 31.88) also failed A* DRC.

## Needs a decision

None new. Packing v3 (`ab9ce95`) is vendored. Resume is: discard or DRC the interrupted VBUS/nRESET copper, then Freerouting with locked strips, or name remaining pads and stop.

## Final commit sha

`3a27ffd1420d64d34bff676a970edd96d3455830` (`wip(WP12i): v3 land locked; hand_route interrupted`).
