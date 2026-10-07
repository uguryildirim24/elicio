# WP11d report — layout grid v2c (Q78–Q83)

Lane `w3`, branch `lane/w3`, package WP11d.
First merge of `main`: `57c03ad` (Q78–Q80).
Addendum merge of `main`: `037c4c4` `merge main: Q81-Q83 onto lane/w3 for WP11d addendum`.
Third addendum merge: `0b5c838` `merge main: Q81 settled no-receptacle onto lane/w3 for WP11d addendum`.
Plan for this package: `docs/fab/plan-v2.md`. Analysis only.
The plan was not edited. Order 1 was not touched. No order. No vendor contact.
Board files, the shell, and `docs/fab/open-questions.md` were not edited.

Python 3.13 venv in this worktree. Install: `.venv/bin/python -m pip install -e '.[cad]'`.

## What was built

`scripts/cad/layout_v2c.py` searches a 32-cell grid on the 501012 pack only (Q69).
16 cells keep J1 and U5 (BOM 66). 16 cells drop them (Q81, BOM 64) and put two
charging contact pads on the tail end. Fixed: Contact variant A (Q79), J4
TC2030 on the leftover (Q80), three FR4 0.2 ring pieces (Q72), two Ø2.7
island holes where courtyards allow with keep 3.30 (Q82), neck-end fold
unless remaining wall ≥ 1.0 (Q83), SW1 under the lid, module keep-out empty,
copper-to-edge 0.30, courtyard-to-courtyard ≥ 0 with 0.10 mask.

Vary: process-edge vs body-to-outline 2.5 mm; width 20 and 22; TOTAL_CHORD
47.90 vs 49.00; one-sided vs two-sided; receptacle present vs absent.

`--layout-v2c` on `scripts/cad/placement.py` writes `docs/fab/packing-v2.md`
§5c and at most four drawings in `docs/fab/cad/v2c/`.

## Second addendum — WP12d pin table that meets every rule

The pin table WP12d takes must pass every rule it is checked against.
The placer now keeps pad-to-outline ≥ 0.30 on the island and on the
pocket. D1, C3, C10, C11 and C12 sit inward. The two Ø2.7 holes stay at
the Q82 sites (13.45, 17.70) and (17.95, 17.70), keep 3.30, not under U1.
SW1 stays in the lid recess.

Smallest all-66 with receptacle: process-edge, width 22, chord 47.90,
two sides, fold neck, 66/66, first rule "—". That is the WP12d pin table
in §5c, with the side column.

No no-receptacle cell at width 20 places the full BOM under every rule
(process 20, 47.90, two: 52/64; J4 does not place).

## Third addendum — no-receptacle pin table the build carries (Q81)

Q81 is settled: the build carries no receptacle. §5c now has a second pin
table, same format and rules as the USB table (side column, pad-to-outline
≥ 0.30, Q82 holes, SW1 in the lid recess, Contact A).

Smallest all-64 with no receptacle: process-edge, width 22, chord 47.90,
two sides, fold neck, 64/64, first rule "—". J1 and U5 are absent.

| item | value |
|---|---|
| holes (Q82) | (13.45, 17.70); (17.95, 17.70) |
| SIG1 strip (Q83) | 10.71 mm |
| SIG2 strip (Q83) | 21.81 mm |
| P4 CHARGE_VBUS | floor, (0.75, 44.00), RING_PAD_D5_H2.7 courtyard 6.40 × 6.40 |
| P5 CHARGE_GND | floor, (21.25, 44.00), RING_PAD_D5_H2.7 courtyard 6.40 × 6.40 |

Drawing `docs/fab/cad/v2c/placement_v2c_process_norec_w22_c47.90_two.svg`
was regenerated. Geometry matches the committed file.

Named centres on the USB width-22 table:

| ref | side | u | s | rot |
|---|---|---:|---:|---:|
| D1 | top | 3.95 | 16.75 | 0 |
| C3 | top | 19.06 | 32.01 | 90 |
| C10 | top | 17.41 | 13.71 | 0 |
| C11 | top | 18.56 | 8.56 | 90 |
| C12 | top | 18.56 | 10.56 | 90 |

## Q81 — grow the body to M1 58.3, or drop the receptacle

M1 58.3 is the USB-inside length (Q70). It is not a closer for 66 footprints
on width 20. Dropping J1 and U5 also does not close width 20 two-sided.

| cell | USB (66) | no receptacle (64) |
|---|---|---|
| process, 20, 47.90, two | 53/66 | 52/64 |
| process, 22, 47.90, two | 66/66 | 64/64 |
| body 2.5 mm, 22, 47.90, two | 32/66 | 31/64 |

Width 20 two-sided with no receptacle still has J4 unplaced.
The first rule that cannot be met is copper-to-edge 0.30 (board-v2.md §12).
The USB-C receptacle is not that first fail. Growing the body to M1 58.3
does not change width 20 island area. Closing 66 or 64 under every rule
needs width 22.

No-receptacle cells have no J1 and no U5. Two `RING_PAD` parts P4 and P5
sit on the tail at (0.75, 44.0) and (width−0.75, 44.0).

## Q82 — hole sites the shell can follow

Holes are reserved after SW1, before J4 and the passives. RING_* boxes are
not hole blockers. SW1 keeps the lid-recess leftover site. If SW1 sits on
the leftover, the two Ø2.7 holes prefer the island.

Process-edge width 22, chord 47.90, two sides (the closer, USB or no USB):

- (13.45, 17.70)
- (17.95, 17.70)

WP14d can move the bosses to those sites. Keep from courtyard is 3.30.

## Q83 — neck-end fold is the default

`wall_left = WALL(1.5) − (FOLD_STAND_OUT 1.6 − SIDE_CLEAR 0.75) = 0.65` mm
at width 20 and at width 22. The extra 2 mm at width 22 is island, not wall.
Every cell in this grid uses neck-end strips. No cell uses side-wall pockets.

## 16 cells with USB-C receptacle (BOM 66)

| edge | width | chord | sides | fold | placed / N | first rule that cannot be met | island mm² | leftover mm² | holes | extra u | extra s | second side |
|---|---:|---:|---|---|---:|---|---:|---:|---|---:|---:|---|
| process | 20 | 47.90 | top | neck | 28/66 | J4 TC2030 on the leftover (Q80) | 334.8 | 74.7 | (13.45, 17.70); (15.40, 21.65) | +0.00 | +0.00 | — |
| process | 20 | 47.90 | two | neck | 53/66 | J4 TC2030 on the leftover (Q80) | 334.8 | 74.7 | (13.45, 17.70); (15.40, 21.65) | +0.00 | +0.00 | U2, Q1, Q2, Q3, Q4, C7, C8, C9, C15, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19 |
| process | 20 | 49.00 | top | neck | 19/66 | J4 TC2030 on the leftover (Q80) | 351.7 | 91.5 | (15.45, 23.84); (15.45, 28.34) | +0.00 | +1.09 | — |
| process | 20 | 49.00 | two | neck | 52/66 | J4 TC2030 on the leftover (Q80) | 351.7 | 91.5 | (15.45, 23.84); (15.45, 28.34) | +0.00 | +1.09 | Q1, Q2, Q3, Q4, Q5, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13, C14, C15, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17 |
| process | 22 | 47.90 | top | neck | 26/66 | every required footprint placed | 378.0 | 84.4 | (13.45, 17.70); (17.95, 17.70) | +2.00 | +0.00 | — |
| process | 22 | 47.90 | two | neck | 66/66 | — | 378.0 | 84.4 | (13.45, 17.70); (17.95, 17.70) | +2.00 | +0.00 | U5, Q1, Q2, Q3, Q4, Q5, C6, C7, C8, C9, C13, C14, C15, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30 |
| process | 22 | 49.00 | top | neck | 29/66 | every required footprint placed | 397.0 | 103.3 | (15.45, 23.84); (15.45, 28.34) | +2.00 | +1.09 | — |
| process | 22 | 49.00 | two | neck | 66/66 | — | 397.0 | 103.3 | (15.45, 23.84); (15.45, 28.34) | +2.00 | +1.09 | Q1, Q2, Q3, Q4, Q5, C8, C9, C13, C14, C15, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30 |
| body | 20 | 47.90 | top | neck | 14/66 | J4 TC2030 on the leftover (Q80) | 334.8 | 43.9 | — | +0.00 | +0.00 | — |
| body | 20 | 47.90 | two | neck | 25/66 | J4 TC2030 on the leftover (Q80) | 334.8 | 43.9 | — | +0.00 | +0.00 | U2, U3, U4, D1, L1, C4, C5, C6, C10, C11, C12 |
| body | 20 | 49.00 | top | neck | 14/66 | J4 TC2030 on the leftover (Q80) | 351.7 | 60.7 | (13.40, 17.65) | +0.00 | +1.09 | — |
| body | 20 | 49.00 | two | neck | 24/66 | J4 TC2030 on the leftover (Q80) | 351.7 | 60.7 | (13.40, 17.65) | +0.00 | +1.09 | U2, U3, U4, D1, L1, C4, C5, C10, C11, C12 |
| body | 22 | 47.90 | top | neck | 14/66 | J4 TC2030 on the leftover (Q80) | 378.0 | 49.6 | — | +2.00 | +0.00 | — |
| body | 22 | 47.90 | two | neck | 32/66 | J4 TC2030 on the leftover (Q80) | 378.0 | 49.6 | — | +2.00 | +0.00 | U2, U4, U5, Q1, C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13, C14 |
| body | 22 | 49.00 | top | neck | 14/66 | J4 TC2030 on the leftover (Q80) | 397.0 | 68.5 | (13.40, 17.65); (17.90, 17.65) | +2.00 | +1.09 | — |
| body | 22 | 49.00 | two | neck | 32/66 | J4 TC2030 on the leftover (Q80) | 397.0 | 68.5 | (13.40, 17.65); (17.90, 17.65) | +2.00 | +1.09 | U2, U4, U5, Q1, C1, C2, C3, C4, C5, C6, C7, C8, C10, C11, C12, C13, C14, R4 |

## 16 cells with no receptacle (BOM 64)

| edge | width | chord | sides | fold | placed / N | first rule that cannot be met | island mm² | leftover mm² | holes | extra u | extra s | second side |
|---|---:|---:|---|---|---:|---|---:|---:|---|---:|---:|---|
| process | 20 | 47.90 | top | neck | 26/64 | J4 TC2030 on the leftover (Q80) | 334.8 | 74.7 | (13.45, 17.70); (15.40, 21.65) | +0.00 | +0.00 | — |
| process | 20 | 47.90 | two | neck | 52/64 | J4 TC2030 on the leftover (Q80) | 334.8 | 74.7 | (13.45, 17.70); (15.40, 21.65) | +0.00 | +0.00 | U2, Q2, Q3, Q4, Q5, C8, C9, C13, C14, C15, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19 |
| process | 20 | 49.00 | top | neck | 23/64 | J4 TC2030 on the leftover (Q80) | 351.7 | 91.5 | (15.45, 23.84); (15.45, 28.34) | +0.00 | +1.09 | — |
| process | 20 | 49.00 | two | neck | 56/64 | J4 TC2030 on the leftover (Q80) | 351.7 | 91.5 | (15.45, 23.84); (15.45, 28.34) | +0.00 | +1.09 | Q1, Q2, Q3, Q4, Q5, C6, C7, C8, C9, C12, C13, C14, C15, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23 |
| process | 22 | 47.90 | top | neck | 25/64 | every required footprint placed | 378.0 | 84.4 | (13.45, 17.70); (17.95, 17.70) | +2.00 | +0.00 | — |
| process | 22 | 47.90 | two | neck | 64/64 | — | 378.0 | 84.4 | (13.45, 17.70); (17.95, 17.70) | +2.00 | +0.00 | Q1, Q2, Q3, Q4, Q5, C6, C7, C8, C9, C13, C14, C15, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30 |
| process | 22 | 49.00 | top | neck | 29/64 | every required footprint placed | 397.0 | 103.3 | (15.45, 23.84); (15.45, 28.34) | +2.00 | +1.09 | — |
| process | 22 | 49.00 | two | neck | 64/64 | — | 397.0 | 103.3 | (15.45, 23.84); (15.45, 28.34) | +2.00 | +1.09 | Q2, Q3, Q4, Q5, C8, C9, C13, C14, C15, R4, R5, R6, R7, R8, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30 |
| body | 20 | 47.90 | top | neck | 13/64 | J4 TC2030 on the leftover (Q80) | 334.8 | 43.9 | — | +0.00 | +0.00 | — |
| body | 20 | 47.90 | two | neck | 24/64 | J4 TC2030 on the leftover (Q80) | 334.8 | 43.9 | — | +0.00 | +0.00 | U2, U3, U4, D1, L1, C4, C5, C6, C10, C11, C12 |
| body | 20 | 49.00 | top | neck | 13/64 | J4 TC2030 on the leftover (Q80) | 351.7 | 60.7 | (13.40, 17.65) | +0.00 | +1.09 | — |
| body | 20 | 49.00 | two | neck | 23/64 | J4 TC2030 on the leftover (Q80) | 351.7 | 60.7 | (13.40, 17.65) | +0.00 | +1.09 | U2, U3, U4, D1, L1, C4, C5, C10, C11, C12 |
| body | 22 | 47.90 | top | neck | 13/64 | J4 TC2030 on the leftover (Q80) | 378.0 | 49.6 | — | +2.00 | +0.00 | — |
| body | 22 | 47.90 | two | neck | 31/64 | J4 TC2030 on the leftover (Q80) | 378.0 | 49.6 | — | +2.00 | +0.00 | U2, U4, Q1, Q2, C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13, C14 |
| body | 22 | 49.00 | top | neck | 13/64 | J4 TC2030 on the leftover (Q80) | 397.0 | 68.5 | (13.40, 17.65); (17.90, 17.65) | +2.00 | +1.09 | — |
| body | 22 | 49.00 | two | neck | 31/64 | J4 TC2030 on the leftover (Q80) | 397.0 | 68.5 | (13.40, 17.65); (17.90, 17.65) | +2.00 | +1.09 | U2, U4, Q1, Q2, C1, C2, C3, C4, C5, C6, C7, C8, C10, C11, C12, C13, C14, R4 |

## Geometry that does not vary with the receptacle

Island (process-edge, leftover 3.9 mm, Q80):

| width | chord | island u×s | leftover mm² | extra u | extra s |
|---|---|---|---|---|---|
| 20 | 47.90 | 17.50 × 21.60 = 334.8 | 74.7 | +0.00 | +0.00 |
| 20 | 49.00 | 17.50 × 22.69 = 351.7 | 91.5 | +0.00 | +1.09 |
| 22 | 47.90 | 19.50 × 21.60 = 378.0 | 84.4 | +2.00 | +0.00 |
| 22 | 49.00 | 19.50 × 22.69 = 397.0 | 103.3 | +2.00 | +1.09 |

Body-to-outline 2.5 mm shrinks leftover to 43.9 / 60.7 / 49.6 / 68.5 mm².
J4 6.0×16.0 does not fit that leftover. First fail on every body-edge cell
is `J4 TC2030 on the leftover (Q80)`.

Under-board air on 501012: 3.31 mm. Second-side parts need body height ≤ 3.31 mm.
V2C_ARC_PLUS_M1 at chord 49.00 is 1.0883 mm. Box is frozen with slots.

## Drawings (four, `docs/fab/cad/v2c/`)

- `placement_v2c_process_usb_w22_c47.90_two.svg` — 66/66
- `placement_v2c_process_norec_w22_c47.90_two.svg` — 64/64
- `placement_v2c_body_usb_w22_c47.90_two.svg` — 32/66
- `placement_v2c_body_norec_w22_c47.90_two.svg` — 31/64

`docs/fab/cad/v1/` still has the 14 `placement_v2_*.svg` files from WP11c.

## Tests

`.venv/bin/python -m unittest discover -s tests -v`

`Ran 222 tests in 200.223s OK`

`PlacementWP11dTests` covers 32 cells, Q81 skip of J1/U5 plus P4/P5,
Q83 neck-end on every cell, winning process-edge USB overlaps, regions,
Contact A, copper-to-edge ≥ 0.30 on both pin tables, hole keep versus
U1, SW1 and the bottom edge, and the no-receptacle cell (P4/P5 RING_PAD
courtyards, Q82 sites, SIG1/SIG2 strip lengths).

## Commits (do not push; the hook still pushes)

- `57c03ad` merge main: round 7 onto lane/w3 for WP11d
- `d4d2e6f` packing(v2c): search the 16-cell layout grid under both edge readings
- `e2a0e01` packing(v2c): layout grid, edge rule both ways, two sides
- `037c4c4` merge main: Q81-Q83 onto lane/w3 for WP11d addendum
- `6c945e1` packing(v2c): Q81 no-receptacle cells, Q82 courtyard holes, Q83 neck-end fold
- `e1f1d6f` packing(v2c): publish §5c for Q81-Q83
- `eebe871` packing(v2c): pin table meets copper-to-edge; holes not under U1
- `ae19850` packing(v2c): publish the WP12d pin table that meets every rule
- `0b5c838` merge main: Q81 settled no-receptacle onto lane/w3 for WP11d addendum
- `e1ebea7` packing(v2c): publish the Q81 no-receptacle pin table WP12d takes
- `c6bd2fe` packing(v2c): §5c second pin table for the no-receptacle cell

Tip: `c6bd2fe`. `git status --short` is empty.

## What this does not decide

WP12d does not get a pin table from width 20. Body-to-outline 2.5 mm
does not place J4. Width 20 no-receptacle does not place J4 either.
The board lane pins both width-22 tables. The build carries the
no-receptacle table (Q81). The shell lane moves bosses to the Q82 sites.
