# t-0019: v4 board routed

The v4 board is routed, and the routed release passes. After a zone refill, DRC shows 0 errors, 0 unconnected items and 0 shorts, on two copper layers at the 0.10/0.10 floor. No rule or layer changed, and the only part changes are the refcheck t-0023 fixes. The body is still 18 × 8.1 mm. The files are ready to order. Two decisions are still yours, and both were already on your list: the TS/NTC question (a 3-way J2 with a cell that has its own NTC, or keep R13 and watch the charge temperature yourself) and the antenna keep-out (13 mm against 18; range risk). One new trade-off: to free routing room, D1 (the VBUS TVS) moved to the far end of the VBUS trunk. A surge from P4 now reaches the charger before the clamp.

## Result

| | |
|---|---|
| Final commit | `6f653a1` (merge of `origin/main`, pushed). Routed board `3df3305`, design note `5d797d8` |
| Board | `hardware/board/elicio-v4.kicad_pcb`: 773 track segments (213 locked), 49 vias (28 locked), GND pours filled and saved |
| Body | 18 × 8.1, unchanged (§10.2: all rows pass except the flap-rib cut already in §7). J2 clears the P5 well by 4.81 mm (needs ≥ 0.3) |
| Rules | Unchanged: 2 layers, 0.10/0.10, 0.40/0.15 vias, Contact class, Q84/Q88/Q97 areas |
| Parts | Only the refcheck t-0023 changes (D1 SOD882 land, C11 1 µF, C17, R34/R35, Q2–Q4 PMZ290UNE2; design note §2.1, schematic ERC 0). The J3 and VSS fixes are untouched. U1's pad nets match the old board, and `tests/test_firmware_pins_v4.py` passes after the merge |
| Tests | `.venv/bin/python -m unittest discover -s tests -q`: `Ran 283 tests`, `OK (skipped=28)` after the merge. The Contact-safety tests (220 kΩ per path, one Contact net per strip, no foreign via or pour in a land zone, R1–R3 the only exposed Contact copper) all pass on the routed board |

## Final DRC (verbatim)

`kicad-cli pcb drc --format json --refill-zones --schematic-parity -o … hardware/board/elicio-v4.kicad_pcb`, KiCad 10.0.6, project rules, on the committed file at `6f653a1`:

```
Found 25 violations
Found 0 unconnected items
Found 2 schematic parity issues
```

- 0 errors, so 0 shorts, 0 clearance errors and 0 starved thermals.
- The 25 are warnings:
  - 24 `lib_footprint_mismatch`: the build strips footprint silkscreen and hides fields.
  - 1 `via_dangling`: the documented +VDD via at (7.60, 36.70).
- The 2 parity issues are J2's two MP pads, which have no schematic pin (documented).

## Release outputs

`.venv/bin/python scripts/board/release.py --board elicio-v4 --routed` exits 0. From `summary.json`: `"routed": true`, `"refused": {}`, `"erc_errors": 0`, `"erc_warnings": 0`, `"drc_errors": 0`, `"drc_warnings": 25`, `"unconnected_items": 0`, `"pcb_pads_without_net": 0`, `"bom_rows": 61`, `"cpl_rows": 61`, `"bom_refs_without_cpl": []`.

All files are in `hardware/board/release/elicio-v4/`. They're gitignored, so re-running the command above writes them again.

- `summary.json`, `erc.json`, `drc.json`
- `bom.csv` (61 rows), `pos.csv`, `cpl.csv` (61 rows)
- `elicio-v4.step`. It has no 3D models for 5 footprints: Molex Pico-EZmate Slim, Texas DSBGA-6 (U3), Texas RSM0032 (U2), Texas X2SON-4 (U4/U5) and SOT-883 (Q1–Q4).
- `gerbers/` (17 files): the Gerbers `elicio-v4-{F,B}_{Cu,Mask,Paste,Silkscreen}.gbr` and `elicio-v4-Edge_Cuts.gbr`, the User layers `elicio-v4-User_{1,Comments,Drawings,Eco1,Eco2}.gbr`, the drill files `elicio-v4-PTH.drl` and `elicio-v4-NPTH.drl`, and the job file `elicio-v4-job.gbrjob`.

## How it closed

I made five router runs and finished three of them, well inside the six-run budget.

| Run | Input | Result |
|---|---|---|
| 1 | Pass 3: refcheck parts, U2's GND core locked | Router only: 15 nets in conflict after 60 rounds |
| 2 | Pass 4: knot placement plus corner pre-routes (+3V0 hub, U2 GND core, charger corner, AFE gate) | 1 open: AFE_IN1N, 0.51 mm at U2 pins 3/4. The two inputs must cross once |
| 3 | Pass 5: IN1P/IN1N crossing locked, R13 0.65 east | Router only: AFE_IN1P against GND_B. U3.C2 was boxed in |
| 4 | Pass 5b: GND via at (11.67, 17.15) for U3.C2's corner | 2 open, both GND islands 0.40 mm from the main GND: P5's run north of U3, and Q4.2's F pocket |
| 5 | Pass 6: locked P5 → R11.2 top-edge track, GND via (13.50, 28.58) for Q4.2 | 0 open. This is the committed board |

Run 4 went from 1 open to 2. Different spots: the crossing closed, and two GND islands appeared. Under the stop rule, run 5 was the last try before stopping, and it closed everything.

t-0014's second proposed pre-route (AFE_EN_HW across the P1 landing to U1) wasn't needed. AFE_EN_HW goes to Q2.3, and after t-0016's pass 2 it's a short B hop with no copper in LAND_P1's zone. Design note §9.2 (reliefs 6–10) and §9.4 map each of t-0014's ten opens to what closed it.

## Design note

`docs/fab/board-v4-design.md`:

- Status line and date.
- §2.1: D1's new site, and the ESD cost stated once.
- §4.3 block table, §5.4 (IN1P/IN1N and P5 GND paths), §6 (area numbers marked as t-0012's placement).
- §9 rewritten: routed state, verbatim DRC, release result, router runs, reliefs 6–10, 3 thermal stubs, the rebuild recipe with the new GND regions.
- §10.1/§10.2 regenerated with `v4_tables.py`.
- §11.1: the D1 item added and the stale "Q2–Q4 not chosen" entry removed.

I didn't touch `plan-v2.md` or `open-questions.md`.

## For you

1. **TS/NTC** (§2.1 item 6): 3-way J2 plus a cell with an NTC, or R13 as is.
2. **Antenna keep-out** (§4.2): 13 mm against 18. The risk is range.
3. **D1 placement** (§2.1 item 1): it's at (14.30, 28.60), at least 11 mm of VBUS track past U3's VBUS ball. Moving it back beside U3 would reopen the east-column knot and need another route. It's worth it if U3's own ESD rating turns out not to cover the surge (UNVERIFIED).

The rest of §11.1 is supply and fit: ISP1807 consignment, the cell with the Pico-EZmate plug, 0201 on FPC, and U4 stock at 0. The §7 shell changes are needed for the body, not for the board order.

## Lessons

- A negotiated router can't resolve a forced topological crossing. IN1P/IN1N, and AFE_EN_HW against CHG_MON, show up as the same 2-net conflict every round. Find the crossing in the `--debug` conflict cells and lock it by hand.
- After locking GND copper, check every GND pad against the split groups. A pad left out, or a pocket the pours can't reach, finishes as a 0.40 mm island. One locked link or via fixes it; more finisher rounds don't.
- Router-only runs are cheap diagnostics. Only run the finisher when the router is at 0–2 conflicting nets.
- A DRC on a scratch copy reports `lib_footprint_issues`, because the library isn't found there. Take the final DRC lines from the committed file in place, where the same warnings show as `lib_footprint_mismatch`.
- unittest prints its summary to stderr. Capture `2>&1` into a file before grepping for `OK`.
