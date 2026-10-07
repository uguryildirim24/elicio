# WP11g report — flat pattern v3, posterior-wall pads (lane w3)

Lane `w3`, branch `lane/w3`, package WP11g.
Merge of `main`: `4f82c6b` (WP12i first half; Q98). Round 7 was already on this
lane (`facb0c1`). Plan for this package: `docs/fab/plan-v2.md`. Analysis only.
The plan was not edited. Order 1 was not touched. No order. No vendor contact.
Board files, the shell, and `docs/fab/open-questions.md` were not edited.

Python 3.13 venv in this worktree.

## Which wall is posterior

The posterior side wall is **u 20.50–22.00** (width 22, wall 1.50).

Lines used:

- `docs/fab/montage.md` §2.1: u is the posterior offset from the body's
  anterior edge (u = 0). High u is posterior.
- `docs/fab/shell-v2.md` / plan: the hook root sits at low u on the hook-end
  face. `HOOK_ROOT_X` default 4.0. packing-v2.md: the hook root occupies u up
  to 6.39. The hook curves forward over the top of the ear.
- `docs/fab/interface.md`: CABLE_EXIT is a cylinder through the posterior side
  wall (high-u wall).

The far wall from the hook root is the posterior edge hidden behind the ear.
P4/P5 go there (Q90). The anterior wall u 0–1.50 is not used. The hook-end
end-face fallback is not used.

## What was built

P4 (CHARGE_VBUS) and P5 (CHARGE_GND) are RING_PAD_D5_H2.7 clamped button-heads
in that wall's inner face, in the free bay beside the cell:

| pad | folded (u, s, y) | head | nylon | wall around seat |
|---|---|---|---|---|
| P4 | (20.50, 4.35, 4.35) | +u | 3.00 | 1.50 vs floor and hook-end s |
| P5 | (20.50, 12.35, 4.35) | +u | 3.00 | 1.50 vs floor and hook-end s |

Head through the 1.50 wall. Ring on the inner face. 3.0 standoff into the bay.
Clear of the hinge lip, the cell pocket (u 1.80–11.90), and pocket-island SMT.
The CHARGE tab leaves the pocket island's high-u edge, folds 90° at R 1.5
(allowance πR/2 = 2.36 mm plus wall run 0.46 mm). Flat centres: P4 (23.32,
4.35), P5 (23.32, 12.35). Pad-to-outline ≥ 0.30. The rib slot and the drop
channel are unused; they stay in the shell extras list.

J2 (JST-SH) sits inside the cavity at (15.15, 11.35) rot 0 on the pocket
island beside the cell. J3 sits on a break-off tab at (28.41, 26.80), neck
2.5 mm, cut line at u = 22.25. Assembly step: Remove the J3 break-off tab
after programming and before closing the shell.

R9 and R10 are out of the no-receptacle BOM (Q95). Pin table v3 has 66 rows
(64 parts plus H1/H2).

Cavity test: every courtyard and hang is inside the cavity or on a declared
exterior (SIG strips before folding; J3 break-off tab). Q97: no other
courtyard inside a land 7 × 7. Hole keep 3.30. Second-side height ≤ 3.31.

§5d keeps the frozen pin table v2.1 (68 rows) so the board and shell parsers
still read that section. Live numbers are §5e.

Drawing: `docs/fab/cad/v2c/placement_v2c_process_norec_w22_c47.90_two.svg`
(four drawings in `docs/fab/cad/v2c/`, Q56).

## Addendum — Q98 channels and the WP14f well

Merge of `main` for this turn: `665578e`. Q98 is on main.

H1/H2 keep-out gap was 1.20 mm (two Default tracks already in it). It is now
1.42 mm: 0.12 more plus 0.10 mm margin. H1 (13.23, 17.70), H2 (17.95, 17.70).
Three Default tracks need 0.70 mm of empty channel. The shell bosses follow
those sites.

J4 moved east to (16.52, 24.60) rot 90. Via slot on the west face of J4,
east of the locked SIG2 run at u 13.50: u 13.775–14.525, s 21.10–28.10,
width 0.75 mm (via pad 0.55 plus Default clearance). West of SIG2 is U1
copper, so the slot cannot sit there.

R16 and the east 0402 row stay out of that approach and out of the J4 holes.
A 0.6 mm channel stays free on both sides around U2, U3 and J4 (U2/SW1 may
share XY on opposite faces). `PlacementWP11gTests.test_q98_routing_channels`
checks the gap, the via slot, and `q98_hits`.

§5e publishes the keep-out list: HOLE_CH, U2_CH, U3_CH, J4_CH, J4_VIA_SLOT,
J4_APPROACH_EAST.

Medial M2.5 well (WP14f `89279c2`): head at (16.50, 41.00), screw M2.5×8,
tail boss OD 9.94 mm. The live §5e extras row states that. The frozen §5d
prose that still named the Ø5 screw head now says (16.50, 41.00).

## Gates

`LC_ALL=C .venv/bin/python -m unittest discover -s tests -v`

`Ran 257 tests in 432.093s OK` (exit 0).

`write_packing_doc` twice: `docs/fab/packing-v2.md` is byte-identical
(`cksum 2928348090 295832`). Drawings = 4. Order 1 not touched.
`git status --short` is empty after the last commit (the report file is
untracked and gitignored).

Plan §9 packing slice: Q98 channels in pin table v3; well at 16.50.
Verified by `PlacementWP11gTests` and the regenerated §5e.

## What was not done

The board was not edited. WP12i consumes pin table v3 and the Q98 table.
The shell was not edited. WP14 follows H1/H2 and the well site in §5e.
USB-C cells still hang J2 off the pocket; that variant is not the build (Q81).
Nothing was ordered.

## Needs a decision

None for this lane. Q98 follows the Round 8 reading. The via slot is east of
SIG2 (west face of J4) because west of SIG2 is U1 copper.

## Commits (do not push; the hook still pushes)

- `665578e` Merge of `origin/main` (Q98 on main).
- `28f2a24` packing(v3): Q98 channels, H1/H2 gap, J4 via slot, well at 16.50
- `ab9ce95` packing(v3): pin table v3 Q98 keep-outs, H1/H2 1.42 mm gap, well at 16.50

Tip: `ab9ce9588d55aff5143828f6dd88f5d22ed8223c`. `git status --short` is empty except this report.
