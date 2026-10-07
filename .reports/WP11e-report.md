# WP11e report — flat pattern, pin table v2, J4 NPTH keep-out (lane w3)

Lane `w3`, branch `lane/w3`, package WP11e.
Merge of `main`: `c88eaf9` (HANDOFF only). Earlier merge `a1fe352` brought
the WP11e brief and Q84/Q85.
Plan for this package: `docs/fab/plan-v2.md`. Analysis only.
The plan was not edited. Order 1 was not touched. No order. No vendor contact.
Board files, the shell, and `docs/fab/open-questions.md` were not edited.

Python 3.13 venv in this worktree.

## What was built

`docs/fab/packing-v2.md` §5d publishes the flat pattern for the build cell
(process-edge, width 22, chord 47.90, two sides, fold neck, no receptacle).

WP12d pinned §5c literally. P2 at the folded site (10.40, 33.10) sits inside
U1's courtyard. A flex board is drawn flat. Pin table v2 gives PCB coordinates.
The shell keeps a separate folded-site table.

### Flat pattern

| item | value |
|---|---|
| exit | neck-end (Q83). Side-wall pockets stay refused (wall 0.65 mm). |
| fold | 180° at inner R 1.5 mm, stack 0.31 mm (PI 0.11 + FR4 0.2) |
| arc | πR = 4.71 mm (Q83). Midplane π(R + t/2) = 5.20 mm is not used for L_flat. |
| SIG1 | attach (5.90, 16.00); flat ring (5.90, 5.29); L_flat 10.71 mm; folded run 6.00 mm |
| SIG2 | attach (10.40, 16.00); flat ring (10.40, −5.81); L_flat 21.81 mm; folded run 17.10 mm |
| REF | attach (8.50, 37.60); flat ring (8.50, 43.00); along the floor through the end-wall slot; no 180° fold |
| P4 / P5 | (14.70, 4.30) and (17.70, 11.72); hook-end medial floor; flat = folded |
| 2D check | no self-overlap; no strip crosses a leftover or pocket part; P1–P3 flat centres outside every other courtyard |

Mapping: each SIG strip leaves the island neck toward −s. After the 180° fold
the ring sits on the floor at the contact site.

Drawing: `docs/fab/cad/v2c/placement_v2c_process_norec_w22_c47.90_two.svg`
(four drawings in `docs/fab/cad/v2c/`, Q56).

### Pin table v2

68 rows (66 footprints including P4/P5, plus H1 and H2). Side column. Pad-to-outline
≥ 0.30. Q82 holes (13.45, 17.70) and (17.95, 17.70). SW1 in the lid recess.
Contact variant A. P1 and P2 are flat centres, not the folded sites.

### Folded sites for the shell (u, s, y)

| pad | net | u | s | y |
|---|---|---:|---:|---:|
| P1 | SIG1 | 5.90 | 22.00 | 1.50 |
| P2 | SIG2 | 10.40 | 33.10 | 1.50 |
| P3 | REF | 8.50 | 43.00 | 1.50 |
| P4 | CHARGE_VBUS | 14.70 | 4.30 | 1.50 |
| P5 | CHARGE_GND | 17.70 | 11.72 | 1.50 |

y is the ring seat on the inner floor.

### J4 NPTH keep-out (Q85)

KiCad footprint `Tag-Connect_TC2030-IDC-NL` has three NPTH, drill 0.9906 mm.
`elicio-v2.kicad_pro` min_hole_clearance 0.20 mm. Keep diameter 1.39 mm.
No B.Cu part in that zone on the no-receptacle cell. Same-face courtyard
keep-out on F.Cu stands.

| hole | u | s |
|---|---:|---:|
| J4-NPTH1 | 16.25 | 22.06 |
| J4-NPTH2 | 17.27 | 27.14 |
| J4-NPTH3 | 15.23 | 27.14 |

## Addendum 1 — P4/P5 off the side walls (superseded)

§5c had P4 at (0.75, 44.00) and P5 at (21.25, 44.00) in the 1.5 mm walls.
Addendum 1 moved them to (5.05, 49.50) and (16.95, 49.50). Those sites are
off the body (TOTAL_CHORD 47.90, loft s 45.5, Ø5 copper to s 52.0). Do not
use them.

## Addendum 2 — hook-end medial floor

Two Ø5 pads cannot sit on the tail with the rules in this pass.

Tail window: copper after `REF_end_wall_slot` (s ≥ 39.25 + r) and ahead of
the loft (s + r ≤ 45.5). For Ø5, s ∈ [41.75, 43.00]. Edge-to-edge ≥ 2.0 to
the REF Ø6.4 dome (8.50, 43.00) needs centre distance ≥ 7.7 mm. Edge-to-edge
≥ 2.0 to the Ø5 screw head (14.50, 41.00) needs centre distance ≥ 7.0 mm.
Cavity u with pad-to-outline 0.30 is u ∈ [4.30, 17.70]. That set is empty
for one Ø5 pad, so it is empty for a pair. Largest pair that fits on that
tail is Ø2.1.

Hook-end sites (width 22), beside the 501012 cell (u 1.80–11.90, s 1.50–14.50):

| pad | net | folded (u, s, y) |
|---|---|---|
| P4 | CHARGE_VBUS | (14.70, 4.30, 1.50) |
| P5 | CHARGE_GND | (17.70, 11.72, 1.50) |

Checks that pass:

- cavity u 1.50–20.50; Ø5 copper inside the cavity
- pad-to-outline ≥ 0.30 vs the hook-end lobe and vs the cavity
- whole Ø5 copper ahead of loft 45.5 (P4 copper to s 6.80; P5 copper to s 14.22)
- copper not in `REF_end_wall_slot` s 38.20–39.25
- nylon between pads ≥ 3.0 mm (copper edge-to-edge)
- REF dome edge-to-edge ≥ 2.0 mm
- screw head edge-to-edge ≥ 2.0 mm
- no courtyard overlap with P3
- cell still 64/64, every rule met

Extra channel for the shell: Ø5 holes through the medial floor at these
sites. `REF_end_wall_slot` is unchanged. The pocket island already sits
there (SW1, U2). If that island cannot carry the rings, the shell also
needs a rib slot at s 14.90–15.70, u 11.90–20.50, height 0.31, for a
floor tab from leftover s 16.

Shell lane: stop using (0.75, 44.00), (21.25, 44.00), (5.05, 49.50), and
(16.95, 49.50). Follow the §5d folded table. P1–P3 are unchanged.

The cell is marked in §5d and in the rule
`P4/P5 on the hook-end medial floor (Q81)`: tail Ø5 impossible, max tail
pair Ø2.1.

## Addendum 3 — P4/P5 flat path (Q85 on the Q86 sites)

The hook-end folded sites stand: P4 (14.70, 4.30), P5 (17.70, 11.72),
y 1.50. They share XY with SW1 (16.25, 4.45) and U2 (15.13, 10.28) on the
pocket island. Those parts sit at board height. The pads sit on the floor.
A flex board is drawn flat, so flat = folded is refused.

Fold picked: leftover s=16.00 through the rib slot (s 14.90–15.70,
u 11.90–20.50, height 0.31). The cell-side drop at u 11.90 is refused
because SIG2's flat strip occupies u 9.15–11.65 through that s.

| item | value |
|---|---|
| drop height | 3.31 mm (underside 4.81 to floor 1.50) |
| bend | two 90° at inner R 1.5 mm |
| allowance | πR + 0.31 vertical = 5.02 mm, plus 1.00 mm past J2 |
| flat map | 90° at leftover corner: 3D −s → +u |
| P4 flat | (37.47, 2.80) |
| P5 flat | (30.05, 5.80) |
| CHARGE rectangle | centre (33.02, 4.30), 14.50 × 8.60 |

2D check: no self-overlap. No pad or strip over a courtyard on either
side. Cell still 64/64.

Shell extras (folded sites stay in the shell table):

- Ø5 floor holes at (14.70, 4.30) and (17.70, 11.72)
- rib slot s 14.90–15.70, u 11.90–20.50, height 0.31
- drop channel at leftover s=16.00, u 11.90–20.50, two 90° at R 1.5,
  drop 3.31 mm, vertical 0.31 mm

Pin table v2 P4/P5 rows are the flat centres with `FLAT PCB (Q85)`.

## Gates

`.venv/bin/python -m unittest discover -s tests -v`

`Ran 231 tests in 193.250s OK`

`scripts/cad/placement.py --packing-doc` twice: `docs/fab/packing-v2.md` is
byte-identical. Drawings = 4. Order 1 not touched. `git status --short` empty
after the last commit (the report file is untracked).

Plan §9 acceptance for this packing slice: the pin table the board pins is
flat; the shell table equals §5 contact sites for P1–P3 and the hook-end
P4/P5 sites; P4/P5 flat centres are distinct from those folded sites; J4
holes are a both-side keep-out. Verified by `PlacementWP11eTests`
(including `test_floor_pad_sharing_xy_with_top_has_distinct_flat_centre`)
and the regenerated §5d.

## What was not done

USB-C cells do not get the both-side J4 NPTH keep-out in the search. That
variant is not the build (Q81). Applying it there left R28–R30 unplaced.
The no-receptacle cell is the one WP12e pins.

Q84 (Contact rule by area) is the board lane.

The shell solids were not edited. WP14 must keep the hook-end Ø5 holes,
add the rib slot, and add the drop channel named above.

Nothing was ordered.

## Needs a decision

None that blocks WP12e. The KiCad TC2030 footprint has three NPTH, not two.
The keep-out uses all three from the file.

## Commits (do not push; the hook still pushes)

- `c88eaf9` Merge remote-tracking branch `origin/main` into `lane/w3`
- `5dc642c` packing(v2e): flat pattern in PCB coordinates and J4 NPTH keep-out
- `723e74c` packing(v2e): flat pattern, tab pads in PCB coordinates, J4 keep-out both sides, pin table v2
- `bf9f3f6` packing(v2e): move P4/P5 onto the flex tail inside the cavity
- `303be75` packing(v2e): move P4/P5 to the hook-end medial floor
- `c53ddd6` Merge remote-tracking branch `origin/main` into `lane/w3` (Q86)
- `408a476` packing(v2e): give P4/P5 Q85 flat centres through the rib-slot fold

Tip: `408a476`. `git status --short` is empty except this report.
