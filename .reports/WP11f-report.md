# WP11f report — J4 hole sites from KiCad, pin table v2.1 (lane w3)

Lane `w3`, branch `lane/w3`, package WP11f.
Merge of `main`: `f514b14` (HANDOFF, Q87, WP11f brief).
Plan for this package: `docs/fab/plan-v2.md`. Analysis only.
The plan was not edited. Order 1 was not touched. No order. No vendor contact.
Board files, the shell, and `docs/fab/open-questions.md` were not edited.

Python 3.13 venv in this worktree.

## What was built

§5d J4 NPTH centres now come from the KiCad footprint
`Tag-Connect_TC2030-IDC-NL` in `git show 30ca79d:hardware/board/elicio-v2.kicad_pcb`.
Pad locals are parsed from that file. The world map uses KiCad canvas Y-down
(positive rot CCW on that canvas). At the pinned J4 (16.25, 24.60) rot 90
the three centres equal KiCad within 0.01:

| hole | u | s |
|---|---:|---:|
| J4-NPTH1 | 16.250 | 27.140 |
| J4-NPTH2 | 15.234 | 22.060 |
| J4-NPTH3 | 17.266 | 22.060 |

Pin table v2 had the pair and the single swapped along s
((16.25, 22.06), (17.27, 27.14), (15.23, 27.14)). That put R24 on a real hole.

Q85 keep-out on B.Cu is pad vs the circle of radius drill/2 + min_hole_clearance
(0.6953 mm). That matches KiCad hole_clearance. Courtyard vs a square keep
could not clear R24 and R26 without a large move or a copper-edge fail.

The no-receptacle build cell was re-run. The J4-side cluster was folded back
to pin table v2, then nudged by the smallest 0.01 mm step (both 0402 rotations)
that keeps pads out of the three holes and keeps copper-to-edge 0.30.

### Pin table v2.1

68 rows. Folded-site table unchanged. Flat P4/P5 unchanged.

| ref | pin table v2 | pin table v2.1 | delta |
|---|---|---|---|
| R23 | (18.28, 21.17) rot 0 | (18.32, 21.10) rot 0 | +0.04 u, −0.07 s |
| R24 | (18.28, 22.37) rot 0 | (18.49, 22.57) rot 90 | +0.21 u, +0.20 s |
| R26 | (14.22, 21.63) rot 90 | (14.21, 21.63) rot 90 | −0.01 u |

WP12e zero-track DRC (`route.md` §9 on `lane/w2`) asked R24 +0.46 u at rot 0.
`route.md` §10 was not on `lane/w2` at this pass. Packing cannot take +0.46 u
at rot 0: pad-to-outline falls below 0.30. Rot 90 plus a 0.29 mm step clears
the hole and the copper rule. Distance from the WP12e +0.46 site (18.74, 22.37)
to (18.49, 22.57) is 0.32 mm, past the 0.1 mm pin. Q87: the reviewer
reconciles within 0.1 mm; the board is copper truth.

WP12e also nudged R23 +0.09 u and R26 −0.05 u for the *wrong* hole pair.
Those nudges are not used. The real-hole moves are the rows above.

Drawing: `docs/fab/cad/v2c/placement_v2c_process_norec_w22_c47.90_two.svg`
(four drawings in `docs/fab/cad/v2c/`, Q56).

## Gates

`.venv/bin/python -m unittest discover -s tests -v`

`Ran 233 tests in 203.484s OK` (LC_ALL=C).

`scripts/cad/placement.py --packing-doc` twice: `docs/fab/packing-v2.md` is
byte-identical (`cksum 2573139946 281403`). Drawings = 4. Order 1 not touched.
`git status --short` empty after the last commit (the report file is untracked
and gitignored).

Plan §9 acceptance for this packing slice: J4 hole sites equal the KiCad
footprint at the pinned pose; pin table v2.1 has 68 rows; B.Cu pads stay out
of the three holes. Verified by `PlacementWP11fTests` and the regenerated §5d.

## What was not done

USB-C cells do not get the both-side J4 NPTH fold. That variant is not the
build (Q81). Applying the restore there broke courtyard rules on the USB cell.

The board was not edited. WP12f still owns R24 on copper and `route.md` §10.

The shell was not edited. Folded sites are unchanged.

Nothing was ordered.

## Needs a decision

R24: packing v2.1 is (18.49, 22.57) rot 90. WP12e's named copper move was
+0.46 u at rot 0. They differ by 0.32 mm and by rotation. Q87 says the board
is copper truth; the reviewer reconciles within 0.1 mm. No stop for this lane.

## Commits (do not push; the hook still pushes)

- `f514b14` Merge remote-tracking branch `origin/main` into `lane/w3` (Q87, WP11f)
- `e4b857c` packing(v2f): J4 hole sites from the KiCad footprint, pin table v2.1

Tip: `e4b857c`. `git status --short` is empty except this report.
