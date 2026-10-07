# WP11b report — DTP arc-plus and the REF tab route

Lane `w3`, branch `lane/w3`, package WP11b.
Plan for this package: `docs/fab/plan-v2.md` at `ef369bd`.
Analysis only. The plan was not edited. Order 1 was not touched.
No order. No vendor contact.

## What was built

`scripts/cad/placement_v2.py` now runs the DTP301120 series under interface II
at `--arc-plus 1.5` and `3.0`, the Jauch LP501218JH series at BODY_ARC and
arc-plus, and three REF tab routes on the 501015 winner board.
`scripts/cad/placement.py` accepts `--dtp-arc`, `--jauch`, `--buyable-ext`,
`--pack-cells`, and `--cell` `jauch|pack501015|pack501012`.
`docs/fab/packing-v2.md` was regenerated, not hand-edited. Round-5 packing tabs
are unchanged, so Stage B still measures the straight floor REF path.
Jauch and the L7 packs are not in the 864-run matrix. Round 5 tests stay as they were.
The 864-run table and the Stage B winner row were not rewritten.

The 501012 pack closes on 8 bodies. Those drawings were not added under
`docs/fab/cad/v1/`: 14 + 8 would exceed the WP11b Q56 cap of 20, and the
round-5 kept-set test pins `placement_v2_*.svg` to the 864-run 14-file set.

Python 3.13 venv in this worktree. Install: `.venv/bin/python -m pip install -e '.[cad]'`.

## L7 packs (note 3, L7 §7 and §7.8)

144 runs (2 cells × 3 widths × 4 lids × 2 standoffs × 3 arcs). Round-5 checker.
Foam 0.5. Series. Interface II. BODY_ARC and arc-plus 1.5 and 3.0.

The winner body with the real 17.0 mm pack does not close.
First conflict: `BQ25100 overlaps header`. Board s 20.0–37.6 (bare cell was 18.6–37.6).
0 of 72 501015-pack runs close. No first-conflict family is on every run.
On the winner body, +1.5 mm of arc clears the overlap and then fails M1 (49.42 > 49.00).

8 of 72 501012-pack runs close. Smallest closer: `A_pack501012_series_w19_y8_iII_s3`.
TOTAL_CHORD 47.90. Outer 9.0. Width 19 (−1 mm vs the 501015 winner). Same chord. Same outer.

| cell | size (L × W × T) | packed | smallest closer | width | lid | outer | TOTAL_CHORD |
|---|---|---:|---|---:|---:|---:|---:|
| 501015 (bare, 864-run winner) | 15.6 × 10.4 × 5.2 | 5.7 | `A_501015_series_w20_y8_iII_s3` | 20 | 8 | 9.0 | 47.90 |
| 501015 pack | 17.0 × 10.0 × 5.0 | 5.5 | none | — | — | 9.0 | 47.90 |
| 501012 pack | 13.0 × 10.1 × 5.1 | 5.6 | `A_pack501012_series_w19_y8_iII_s3` | 19 | 8 | 9.0 | 47.90 |

Sources: L7-research-v4.md §7 and §7.8. Full table: `docs/fab/packing-v2.md` §1e.

## DTP301120 arc-plus (Q55)

DTP301120 22.0 × 11.5 × 3.2, foam 0.5 (Q57), series, interface II, architecture A.
Widths 18 to 20, LID_Y 7 to 9, standoffs 3.0 and 4.0. Same round-5 conflict logic.
48 runs. 0 close at +1.5. 0 close at +3.0. There is no DTP body that closes.

Winner stays `A_501015_series_w20_y8_iII_s3`. TOTAL_CHORD 47.9005.

| arch | standoff | width | lid | arc+ | closes | first conflict | TOTAL_CHORD | M1 gate |
|---|---:|---:|---:|---:|---|---|---:|---:|
| A | 3 | 18 | 7 | 1.5 | no | module top 7.62 > LID_Y 7 | 49.42 | 52.42 |
| A | 3 | 18 | 7 | 3 | no | module top 7.62 > LID_Y 7 | 50.93 | 53.93 |
| A | 4 | 18 | 7 | 1.5 | no | module top 8.62 > LID_Y 7 | 49.42 | 52.42 |
| A | 4 | 18 | 7 | 3 | no | module top 8.62 > LID_Y 7 | 50.93 | 53.93 |
| A | 3 | 18 | 8 | 1.5 | no | JST_SH top 8.22 > LID_Y 8 | 49.42 | 52.42 |
| A | 3 | 18 | 8 | 3 | no | JST_SH top 8.22 > LID_Y 8 | 50.93 | 53.93 |
| A | 4 | 18 | 8 | 1.5 | no | module top 8.62 > LID_Y 8 | 49.42 | 52.42 |
| A | 4 | 18 | 8 | 3 | no | module top 8.62 > LID_Y 8 | 50.93 | 53.93 |
| A | 3 | 18 | 8.5 | 1.5 | no | module 10.50×15.50 at (7.50,31.35) outside the board | 49.42 | 52.42 |
| A | 3 | 18 | 8.5 | 3 | no | module overlaps ADS1292_RSM | 50.93 | 53.93 |
| A | 4 | 18 | 8.5 | 1.5 | no | module top 8.62 > LID_Y 8.5 | 49.42 | 52.42 |
| A | 4 | 18 | 8.5 | 3 | no | module top 8.62 > LID_Y 8.5 | 50.93 | 53.93 |
| A | 3 | 18 | 9 | 1.5 | no | module 10.50×15.50 at (7.50,31.35) outside the board | 49.42 | 52.42 |
| A | 3 | 18 | 9 | 3 | no | module overlaps ADS1292_RSM | 50.93 | 53.93 |
| A | 4 | 18 | 9 | 1.5 | no | JST_SH top 9.22 > LID_Y 9 | 49.42 | 52.42 |
| A | 4 | 18 | 9 | 3 | no | JST_SH top 9.22 > LID_Y 9 | 50.93 | 53.93 |
| A | 3 | 19 | 7 | 1.5 | no | module top 7.62 > LID_Y 7 | 49.42 | 52.42 |
| A | 3 | 19 | 7 | 3 | no | module top 7.62 > LID_Y 7 | 50.93 | 53.93 |
| A | 4 | 19 | 7 | 1.5 | no | module top 8.62 > LID_Y 7 | 49.42 | 52.42 |
| A | 4 | 19 | 7 | 3 | no | module top 8.62 > LID_Y 7 | 50.93 | 53.93 |
| A | 3 | 19 | 8 | 1.5 | no | JST_SH top 8.22 > LID_Y 8 | 49.42 | 52.42 |
| A | 3 | 19 | 8 | 3 | no | JST_SH top 8.22 > LID_Y 8 | 50.93 | 53.93 |
| A | 4 | 19 | 8 | 1.5 | no | module top 8.62 > LID_Y 8 | 49.42 | 52.42 |
| A | 4 | 19 | 8 | 3 | no | module top 8.62 > LID_Y 8 | 50.93 | 53.93 |
| A | 3 | 19 | 8.5 | 1.5 | no | module 10.50×15.50 at (7.50,31.35) outside the board | 49.42 | 52.42 |
| A | 3 | 19 | 8.5 | 3 | no | module overlaps ADS1292_RSM | 50.93 | 53.93 |
| A | 4 | 19 | 8.5 | 1.5 | no | module top 8.62 > LID_Y 8.5 | 49.42 | 52.42 |
| A | 4 | 19 | 8.5 | 3 | no | module top 8.62 > LID_Y 8.5 | 50.93 | 53.93 |
| A | 3 | 19 | 9 | 1.5 | no | module 10.50×15.50 at (7.50,31.35) outside the board | 49.42 | 52.42 |
| A | 3 | 19 | 9 | 3 | no | module overlaps ADS1292_RSM | 50.93 | 53.93 |
| A | 4 | 19 | 9 | 1.5 | no | JST_SH top 9.22 > LID_Y 9 | 49.42 | 52.42 |
| A | 4 | 19 | 9 | 3 | no | JST_SH top 9.22 > LID_Y 9 | 50.93 | 53.93 |
| A | 3 | 20 | 7 | 1.5 | no | module top 7.62 > LID_Y 7 | 49.42 | 52.42 |
| A | 3 | 20 | 7 | 3 | no | module top 7.62 > LID_Y 7 | 50.93 | 53.93 |
| A | 4 | 20 | 7 | 1.5 | no | module top 8.62 > LID_Y 7 | 49.42 | 52.42 |
| A | 4 | 20 | 7 | 3 | no | module top 8.62 > LID_Y 7 | 50.93 | 53.93 |
| A | 3 | 20 | 8 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| A | 3 | 20 | 8 | 3 | no | ADS1292_RSM in the antenna keep-out | 50.93 | 53.93 |
| A | 4 | 20 | 8 | 1.5 | no | module top 8.62 > LID_Y 8 | 49.42 | 52.42 |
| A | 4 | 20 | 8 | 3 | no | module top 8.62 > LID_Y 8 | 50.93 | 53.93 |
| A | 3 | 20 | 8.5 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| A | 3 | 20 | 8.5 | 3 | no | ADS1292_RSM in the antenna keep-out | 50.93 | 53.93 |
| A | 4 | 20 | 8.5 | 1.5 | no | module top 8.62 > LID_Y 8.5 | 49.42 | 52.42 |
| A | 4 | 20 | 8.5 | 3 | no | module top 8.62 > LID_Y 8.5 | 50.93 | 53.93 |
| A | 3 | 20 | 9 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| A | 3 | 20 | 9 | 3 | no | ADS1292_RSM in the antenna keep-out | 50.93 | 53.93 |
| A | 4 | 20 | 9 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| A | 4 | 20 | 9 | 3 | no | ADS1292_RSM in the antenna keep-out | 50.93 | 53.93 |

At +1.5 mm of arc, TOTAL_CHORD 49.4157 against M1−3 = 49.00 (M1 = 52, Q34 blank, `default.toml`).
That chord already fails the M1 gate.
At +3.0 mm of arc, TOTAL_CHORD 50.9301. Excess versus M1−3 is 1.9301 mm.
Length cost versus the 501015 winner chord 47.9005 is +3.0295 mm of chord.
That is not a closer.

Nearest packing layout to the winner (width 20, LID_Y 8, standoff 3.0):
- +1.5 first conflict: `cell to antenna zone 4.15 < 5 mm`
- +3.0 first conflict: `ADS1292_RSM in the antenna keep-out`

Standoff 4.0 under interface II puts the module top at 8.62, so LID_Y 7 to 9 never closes.

## Coordinator note — Jauch LP501218JH (L7 §2)

L7-research-v4.md §2 (lane/w5) found no 501015-class cell sold in ones.
Buyable packs with page price, stock and a drawing: SparkFun DTP301120 and
Jauch LP501218JH+PCM (5.4 × 12.5 × 20.0 mm, 60 mAh, DigiKey
`1908-LP501218JH+PCM+2WIRE50MM-ND`, bare 2-wire leads).

72 interface-II series runs. Widths 18 to 20, LID_Y 7 to 9, standoffs 3.0 and 4.0,
BODY_ARC and +1.5 and +3.0. Foam 0.5. Packed height 5.9. Cell top 7.40.
**0 close.** There is no smallest Jauch body.

Bare 2-wire leads (28 AWG, 50 ± 3 mm, no connector) per L7 §2. Plan v2 R2:
Rolf solders nothing. This cell is a packing candidate only if the assembler
or the seller terminates the leads.

Nearest winner-like runs (width 20, standoff 3.0):
- LID_Y 8, BODY_ARC: first conflict `JST_SH top 8.22 > LID_Y 8`; also `cell to antenna zone 4.65 < 5 mm`
- LID_Y 8.5, BODY_ARC: first conflict `cell to antenna zone 4.65 < 5 mm`; TOTAL_CHORD 47.90
- LID_Y 7: `cell top 7.40 > LID_Y 7`

At +3.0 mm of arc, TOTAL_CHORD 50.93 (+3.03 mm versus the 501015 winner). That is not a closer.

### Smallest body per cell

| cell | sold in ones | smallest closer | width | lid | standoff | arc+ | TOTAL_CHORD | vs 501015 winner |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 501015 | no (L7 §2) | `A_501015_series_w20_y8_iII_s3` | 20 | 8 | 3 | 0 | 47.90 | — |
| DTP301120 | yes, SparkFun PRT-25270 | none | — | — | — | — | — | no closer |
| LP501218JH | yes, DigiKey (bare leads; needs a terminator) | none | — | — | — | — | — | no closer |

Full Jauch first-conflict table: `docs/fab/packing-v2.md` §1c.

## Coordinator note 2 — bigger lid and width

108 runs. DTP301120 and LP501218JH only. Series, interface II, standoffs 3.0 and 4.0, foam 0.5, BODY_ARC and +1.5 and +3.0. LID_Y 9.5, 10.0 and 10.5. Widths 20, 21 and 22. Same round-5 checker. 0 close. 0 pack if the ≤9×20 cap is set aside. No new drawing (Q56, closers only).

| cell | box | smallest closer | width | lid | outer | TOTAL_CHORD | height vs winner | chord vs winner | never-clears family |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 501015 | ≤9×20 | `A_501015_series_w20_y8_iII_s3` | 20 | 8 | 9.0 | 47.90 | — | — | — |
| DTP301120 | lid 9.5–10.5, w 20–22 | none | — | — | 11.5 | — | +2.5 mm still open | +0 / +3.03 mm, no closer | `SIG# tab crosses boss_# courtyard`, `cell overlaps standoff_SIG#` |
| LP501218JH | lid 9.5–10.5, w 20–22 | none | — | — | 11.5 | — | +2.5 mm still open | +0 / +3.03 mm, no closer | `cell overlaps standoff_SIG#` |

DTP at width 20, LID_Y 9.5, standoff 3, BODY_ARC: first conflict `cell to antenna zone 2.65 < 5 mm`. Outer 10.5. The 22 mm cell still hits SIG1 on every bigger-box run. Arc-plus +3.0 is TOTAL_CHORD 50.93 vs M1−3 = 49.00.

A buyable cell does not pack at +2.5 mm outer height or +3.03 mm chord. The 501015 winner stays the only closer.

Full table: `docs/fab/packing-v2.md` §1d.

## REF tab route (Q59)

Winner board `A_501015_series_w20_y8_iII_s3`. Tail site CONTACT_REF (8.50, 43.00).
Flex at the tab 0.31 (PI 0.11 + FR4 0.2). Bend R 1.5 (`board-v2.md` §11).

| name | y | points | length | added | min wall | side wall | end wall | in cavity | bend R 1.5 |
|---|---|---|---:|---:|---:|---:|---|---|---|
| `along_floor` | 1.50–1.81 | (8.50, 43.00) → (8.50, 36.80) | 6.20 | +0.00 | 0.00 | 5.75 | s 38.20–39.25 at u 8.50 | no | yes |
| `along_lateral_wall` | 1.50–1.81 | (8.50, 43.00) → (2.75, 43.00) → (2.75, 36.80) → (8.50, 36.80) | 17.70 | +11.50 | 0.00 | 0.00 | s 38.20–39.25 at u 2.75 | no | yes |
| `over_pocket_air` | 7.30–7.61 | (8.50, 43.00) → (8.50, 36.80) | 6.20 | +0.00 | 0.00 | 5.75 | s 38.20–39.25 at u 8.50 | no | yes |

No in-cavity route exists. The cavity ends at s 38.20. The Ø7.5 tail pocket starts at s 39.25.
1.05 mm of nylon sits between them. Every searched path crosses that wall.
`best_ref_tab_route()` is none.

WP14 cuts a slot that contains the straight floor tab:

| item | number |
|---|---|
| name | `REF_end_wall_slot` |
| u | 7.25–9.75 (centre 8.50) |
| s | 38.20–39.25 (centre 38.73) |
| y | 1.50–1.81 |
| width | 2.50 |
| through (s) | 1.05 |
| height (y) | 0.31 |
| volume (rect) | 0.814 mm³ |

Default packing REF tab is still (8.50, 43.00) → (8.50, 36.80).

## Plan §9 acceptance (WP11 row)

Plan v2 §11 row 11: packing table on the built solid; which close and why the rest fail.

| item | command | result |
|---|---|---|
| Round 5 864-run table still present | regenerated `docs/fab/packing-v2.md` §1 | 3 closers, all 501015 series w20 iII s3. Winner unchanged. |
| DTP arc-plus table | `.venv/bin/python scripts/cad/placement.py --dtp-arc` (and `--arc-plus 1.5\|3.0`) | 48 runs, 0 close. First conflict per run in §1b. |
| Jauch series table | `.venv/bin/python scripts/cad/placement.py --jauch` | 72 runs, 0 close. First conflict per run in §1c. Compare table next to DTP and 501015. |
| Bigger-box table (note 2) | `.venv/bin/python scripts/cad/placement.py --buyable-ext` | 108 runs, 0 close, 0 pack. §1d. |
| L7 pack cells (note 3) | `.venv/bin/python scripts/cad/placement.py --pack-cells` | 144 runs, 8 close (all 501012 pack). Winner body + 17.0 mm pack does not close (`BQ25100 overlaps header`). Smallest 501012 closer `A_pack501012_series_w19_y8_iII_s3`, TOTAL_CHORD 47.90, outer 9.0. §1e. |
| REF tab route table | packing generator §5 | no in-cavity route; slot numbers for WP14. |
| DTP / REF measured on a new solid | not run | WP11b is packing analysis. Stage B solids stay with WP14. Round 5 already measured `V2_TAB_envelope` fail (REF_body_mm3 1.194) on the winner solid. |
| Order 1 identity | `CadRegenTests` / `CadStageBV2BuildTests` in the full suite | pass. Order 1 files not edited. |

## Gates

Command: `.venv/bin/python -m unittest discover -s tests -v`

Result: Ran 182 tests in 166.175s. OK. 0 failures. 0 errors.

Round 5 placement tests were not rewritten. They passed in that run.
`packing-v2.md` matches a fresh generator write (`test_packing_doc_regenerates_byte_identical` and `test_packing_doc_has_dtp_and_ref_tables`).

`git status --short` is empty. `.reports/WP11b-report.md` is gitignored.

A post-commit hook on this worktree pushed `lane/w3` to origin. This lane did not run `git push`.

## What was not done

- No purchase, quote, or vendor contact (Q55 stays a research question).
- No edit of `plan-v2.md` or `open-questions.md`.
- No file under `docs/fab/cad/v2/`.
- No change to `bte_fit_shell.py`, `render.py`, `manifest.py`, or `tests/test_cad.py`.
- No new committed SVG (8 of 72 501012-pack runs close; 14 + 8 exceeds Q56's 20-file cap, and round-5 tests pin the v1 glob).
- No solid probe of a lid-to-wall gap for the REF tab.

## What could not be measured

- DTP arc-plus on a built solid. Packing arithmetic only.
- REF tab lid-to-wall gap. Packing treats the cavity end wall as solid from floor 1.5 to LID_Y 8.0.
- A 501015 pack in ones: none found (L7-research-v4.md §2). DNK/Benzo sheets give 17 × 10 × 5.0 with PCM (L7 §7 and §7.8). The 17.0 mm pack was packing arithmetic only. The 501012 13.0 × 10.1 × 5.1 figure is an eBay marketplace quote (L7 §7), not a manufacturer sheet. This package does not order. Jauch leads were not terminated.
- M1 on Rolf. Q34 blank. Default 52 used for the gate.
- Harness 100 ± 3 mm. Routed length, not a solid.
- Same Stage B NOT_MEASURED rows as round 5 (`V2_ADJUSTMENT`, `V2_BOSS`, `V2_RECESS`, `V2_USB_medial`, `TAB_envelope_air`).

## Numbers taken as given

| Item | Number | Source |
|---|---|---|
| DTP301120 | 22 × 11.5 × 3.2 | SparkFun PRT-25270 drawing p.9, L5-research-v2.md §1 |
| 501015 | 15.6 × 10.4 × 5.2 | v1 CELL_BODY_MAX (plan v1 §3.3); this is a bare cell (L7 §7) |
| 501015 pack (with PCM) | 17.0 × 10.0 × 5.0 | DNK Power DNK501015; Benzo; L7-research-v4.md §7 and §7.8 |
| 501012 pack (with PCM) | 13.0 × 10.1 × 5.1 | eBay quote 'approx 13.0mm x 10.1mm x 5.1mm', 40 mAh; L7-research-v4.md §7 |
| LP501218JH | 20.0 × 12.5 × 5.4 | L7-research-v4.md §2; DigiKey 1908-LP501218JH+PCM+2WIRE50MM-ND |
| Foam on the cell | 0.5 | plan v1 §5 and order-1 CELL_envelope; plan v2 §3 says 0.3 (decision 57 / Q57) |
| Flex at rings | 0.31 (PI 0.11 + FR4 0.2) | JLC FPC stiffener list, WP12 2026-09-17 |
| Flex tab bend for this search | R 1.5 | board-v2.md §11 |
| Round-5 packing bend floor | R 1.0 | existing `BEND_R` (unchanged) |
| CONTACT_REF | (8.5, 43.0) | packing-v2.md §5 |
| Cavity end / pocket start | s 38.2 / 39.25 | packing-v2.md §5 / Q59 |
| M1 | 52 | default.toml; Q34 blank |
| BODY_ARC | 48.4 | coordinator note 1 |
| Antenna keep-out | 12.4 × 3.8 | Raytac Spec K p.9/p.13, interface §6.3 |
| Floor | 1.5 | v1 |

Full source table: `docs/fab/packing-v2.md` §7.

## Needs a decision

1. The buyable DTP301120 does not close at +1.5 or +3.0 mm of arc. Keep the 501015 winner, or change M1 / body length / cell. +1.5 already fails M1 ≥ TOTAL_CHORD + 3 (49.42 > 49.00).
2. The buyable Jauch LP501218JH does not close at BODY_ARC, +1.5 or +3.0. Packed height 5.9. Antenna gap 4.65 mm at the winner width. Bare leads need a terminator (plan v2 R2).
3. No REF tab route stays inside the cavity. WP14 cuts `REF_end_wall_slot` (2.50 × 1.05 × 0.31 at u 7.25–9.75, s 38.20–39.25, y 1.50–1.81), or another path is chosen.
4. A bigger lid (9.5–10.5, outer 10.5–11.5) and width (20–22) still does not pack DTP or Jauch. The family that never clears is `cell overlaps standoff_SIG#` (DTP also keeps `SIG# tab crosses boss_# courtyard`). Keep the 501015 winner, or change the cell / antenna / standoff layout.
5. Q55: a 501015 pack in ones is not sold (L7 §2). This package did not order.
6. The real 17.0 mm 501015 pack does not close on the winner body or on any body in this grid. First conflict on the winner body: `BQ25100 overlaps header` (the pocket is longer, the board starts at s 20.0 instead of 18.6). Arc-plus +1.5 on that body clears the overlap and then fails M1 (49.42 > 49.00). The 501012 pack (marketplace listing) closes at width 19, LID_Y 8, standoff 3, BODY_ARC, TOTAL_CHORD 47.90, outer 9.0. Keep the bare-501015 Stage B winner, switch the candidate to the 501012 listing, or change the board/pocket for a 17 mm pack.

## Final commit sha

`bcecc831ac9ff3ab0a5ba5af4e1eccb8f30485b3`
