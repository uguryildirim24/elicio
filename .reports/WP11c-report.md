# WP11c report — real courtyards and layout v2 (round-6 rules 70–74)

Lane `w3`, branch `lane/w3`, package WP11c.
On top of `bcecc83`. Round 6 merges that commit only. These commits are round 7.
Plan for this package: `docs/fab/plan-v2.md`. Analysis only.
The plan was not edited. Order 1 was not touched. No order. No vendor contact.
Board files and the shell were not edited.

Python 3.13 venv in this worktree. Install: `.venv/bin/python -m pip install -e '.[cad]'`.

This report covers the first WP11c close and the coordinator amendment
(round 6 verdict `tasks/reviews/code-r6.md` decisions 70–74).

## What was built

`scripts/cad/placement_v2.py` reads every footprint from
`git show 845bac7:hardware/board/elicio-v2.kicad_pcb` (WP12b after the shorting
copper was dropped). The part table holds F.CrtYd, pad extent, and the round-5
packing size as a second column. Keep-out zones from that file are listed
(RF_NO_COPPER, RF_FEED_NOTCH, ring clears, J4 USB-C keep-out).
Contact netclass clearance is 1.0 mm (WP12b `elicio-v2.kicad_pro`, nets
SIG1/SIG2/REF).

`scripts/cad/placement.py --layout-v2` runs the search on the 501012 w20 × y8
body and on the 17.0 mm 501015 pack at +1.5 mm of arc.
`docs/fab/packing-v2.md` §5b was regenerated, not hand-edited.
The 864-run table, the Stage B winner row, and the round-5 tests were not
rewritten. No extra `placement_v2_*.svg` was added (Q56; 14 files remain).

The amendment adds layout rules 70, 72, 73 and 74 from `code-r6.md`.
Each rule is cited by decision number in §5b.

## Size differences (KiCad courtyard vs round 5)

| ref | courtyard | round-5 packing | Δw | Δh |
|---|---|---|---:|---:|
| U1 | 11.50 × 16.50 | 10.50 × 15.50 | +1.00 | +1.00 |
| U2 | 5.26 × 5.26 | 5.00 × 5.00 | +0.26 | +0.26 |
| U3 | 2.96 × 3.50 | 2.10 × 1.40 | +0.86 | +2.10 |
| U4 | 4.10 × 3.40 | 3.30 × 2.90 | +0.80 | +0.50 |
| U5 | 4.10 × 3.40 | 3.30 × 2.90 | +0.80 | +0.50 |
| SW1 | 7.50 × 5.60 | 4.50 × 4.50 | +3.00 | +1.10 |
| J1 | 10.64 × 9.42 | 8.90 × 7.30 | +1.74 | +2.12 |
| J2 | 5.80 × 6.56 | 4.00 × 6.00 | +1.80 | +0.56 |
| J3 | 12.31 × 8.62 | 7.60 × 2.50 | +4.71 | +6.12 |
| D1 | 2.50 × 1.40 | 2.20 × 1.00 | +0.30 | +0.40 |
| R1–R3 | 1.86 × 0.94 | 1.80 × 0.90 | +0.06 | +0.04 |
| J4 | 7.00 × 4.00 | (not packed) | — | — |

66 footprints. The test re-reads the KiCad file and fails if a courtyard disagrees by more than 0.05 mm.

## Rules the search must meet

| rule | source | 501012 w20 y8 | 17 mm pack +1.5 |
|---|---|---|---|
| JLC FPC assembly edge 2.5 mm | board-v2.md §12 / L6 | **no** (first) | no |
| copper-to-edge 0.30 | board-v2.md §12 | no (U1 pad 0.15) | no |
| courtyard-to-courtyard ≥ 0, mask margin 0.10 | DRC 0.05 × 2 | yes (placed parts) | yes (placed parts) |
| Contact netclass 1.0 mm | WP12b kicad_pro | no (0402 pad gap 0.48) | no |
| module keep-out empty | Raytac Spec K | yes | yes |
| J4 on hook-end with plug volume | plan v2 §5.4 | no (USB courtyard fills that face) | no |
| SW1 under lid recess | packing-v2.md §5 | no (HOLE_M1 takes that leftover site) | no |
| J3 and TC2030 reachable | WP11c brief | yes | no (J3 unplaced) |
| every WP12b footprint placed | WP11c brief | no | no |
| USB-C body inside outline | code-r6.md decision 70 | no | no |
| three FR4 0.2 ring pieces; ring 0.31 stays | code-r6.md decision 72 | yes | yes |
| two Ø2.7 boss-site holes, courtyard-clear | code-r6.md decision 73 | no (U1 covers 14.85, 28.10) | no |
| SIG1/SIG2 180° fold at R 1.5, shared numbers | code-r6.md decision 74 | yes (both variants numbered) | yes |
| M1 ≥ TOTAL_CHORD + 3 | Q34; 17 mm only if M1 ≥ 52.5 | (BODY_ARC, not applied) | **no** (first) |

Contact sites were not moved: SIG1 (5.90, 22.00), SIG2 (10.40, 33.10), REF (8.50, 43.00).
REF tab (8.50, 43.00) → (8.50, 36.80). `REF_end_wall_slot` stays cut.

## Round 6 decision 70 — USB-C body

The USB-C land on 845bac7 is J1 (`USB_C_Receptacle_HRO_TYPE-C-31-M-12`).
J4 is TC2030. The real body is the J1 courtyard 10.64 × 9.42 × 3.2
(height from packing `USB` / plan v2 §5.4; board-v2.md §12 is the stackup).

Packing hangs the receptacle 4.80 mm past the outer face s=−1.00.
The courtyard hangs 5.86 mm (J1 s0=−6.86).
The hook root occupies u up to 6.39 on that face.
The opening starts at u=5.50 (overlap 0.89 mm).
A 2.4 mm posterior hook-root move clears the opening and the 1.5 mm ligament.
It does not pull the body inside the outline.

A longer body that seats the body behind the face needs +7.32 mm of arc
with the cell moved back. Chord 55.29. M1 ≥ 58.29 against default.toml M1=52.

**What closes it: nothing.**

## Round 6 decision 72 — ring stiffeners

Three FR4 0.2 ring stiffener pieces exist on the tabs (SIG1, SIG2, REF).
Ring stack 0.31 stays (PI 0.11 + FR4 0.2).
Island Eco1 still has 2 pieces of FR4 0.4.
FR4 piece count 5 (JLC extra-fee threshold 4).

## Round 6 decision 73 — island mounting holes

Two holes in the island at the shell boss sites:
(14.85, 21.50) and (14.85, 28.10), Ø2.7, courtyard keep 3.30 mm.
HOLE_M1 and HOLE_M2 are reserved on leftover.
U1's courtyard covers (14.85, 28.10).
HOLE_M1 takes the leftover SW1 site, so SW1 is not placed.

## Round 6 decision 74 — SIG1/SIG2 fold

180° fold at R 1.5 (arc 4.71 mm, stand-out 1.6 mm).
The same number is used for the PCB, the packing table and the shell.

| pack | variant | SIG1 strip | SIG2 strip | pocket |
|---|---|---:|---:|---|
| 501012 BODY_ARC | neck-end | 10.71 | 21.81 | s 14.40–16.00, 3.50 × 3.00 (neck drop; no side-wall cut) |
| 501012 BODY_ARC | side-wall pockets | 8.36 | 12.06 | 0.85 deep × 3.50 along s × 3.00 along y; wall left 0.65 |
| 501015 +1.5 mm arc | neck-end | 6.71 | 17.81 | s 18.40–20.00, 3.50 × 3.00 (neck drop; no side-wall cut) |
| 501015 +1.5 mm arc | side-wall pockets | 8.36 | 12.06 | 0.85 deep × 3.50 along s × 3.00 along y; wall left 0.65 |

## The two layouts

**501012 pack, w20 × y8, interface II, standoff 3 (the shell as built).**
TOTAL_CHORD 47.90. Island u 2.25–17.75, s 16.00–37.60.
**First rule that cannot be met:** JLC FPC assembly edge 2.5 mm.
U1 at the packing pose (long along u) sits 0.00 mm from the island edge.
Turning U1 long-along-s needs a 15.5 × 20.5 island; this island is 15.50 × 21.60,
so U1 can meet 2.5 mm on the short sides only if nothing else shares that 10.5 mm
strip. U2 courtyard 5.26 cannot sit beside U1 under that rule.

U2 sits on the pocket island. J1 hangs on the hook-end. J2 hangs off the
pocket high-u wall. J3 hangs off the high-u outline. SW1 is not placed
(decision 73 HOLE_M1).

**501015 pack 17.0 × 10.0 × 5.0 at +1.5 mm of arc.**
TOTAL_CHORD 49.42. Need M1 ≥ 52.42. default.toml M1 = 52.
**First rule that cannot be met:** M1 ≥ TOTAL_CHORD + 3 (valid only if M1 ≥ 52.5).

## Contact 1.0 mm on a 2.5 mm tab

An 0402 across a Contact net has pad gap 0.48 mm. That cannot hold 1.0 mm
(SIG1–AFE_IN1P, SIG2–AFE_IN1N, REF–RLD_FB).

- Variant A: R1/R2/R3 on the island at the tab root; each tab carries one Contact trace.
- Variant B: widen each tab to 4.0 mm. The 0402 pad gap 0.48 mm still violates
  Contact-to-Default 1.0 mm; that needs a larger package or a DRC exception.

The reviewer and the board lane pick.

## Plan §9 acceptance

This package has no row of its own in plan §9. The software gate was run:

```text
.venv/bin/python -m unittest discover -s tests -v
```

191 tests. Result: OK.

`packing-v2.md` regenerated with `scripts/cad/placement.py --packing-doc`.
Byte-identical to a fresh `packing_markdown` of the 864-run matrix.
14 `placement_v2_*.svg` files (the round-5 kept set). Order 1 untouched.

## What was not done

No plan edit. No order. No board edit. No shell edit. No new v1 drawings.
No layout that meets every rule on this shell: JLC 2.5 mm cannot hold U1 and U2
on the 15.5 mm island. Decision 70 does not close the USB-C body inside the
outline. Decision 73 does not clear U1 from the high-s boss hole.

## Needs a decision

1. JLC FPC assembly edge 2.5 mm vs a 15.5 mm island that already holds U1 at
   15.5 mm along u. A waiver, a wider island, or U1 off the leftover (module
   only) is required before WP12d can meet that rule.
2. Contact netclass 1.0 mm: variant A (0402 on the island, one trace on the
   2.5 mm tab) or variant B (4.0 mm tab) plus a larger package or a DRC
   exception for the 0.48 mm pad gap.
3. 17 mm 501015 pack at +1.5 mm: raise M1 to ≥ 52.5 or drop that pack.
4. J4 cannot share the hook-end with USB-C (courtyard 10.64 × 9.42). Place J4
   on leftover (as in this table) or move USB.
5. Decision 70: USB-C inside the outline does not close on this M1=52 shell
   (`code-r6.md` decision 70). Longer body needs M1 ≥ 58.29. Hook-root shift
   2.4 mm clears the opening only.
6. Decision 73: U1 covers (14.85, 28.10). Move U1, move the boss, or drop
   that hole. HOLE_M1 also removes the leftover SW1 site.
7. Decision 74: neck-end vs side-wall pockets. Side-wall remaining wall is
   0.65 mm (under 1.0 mm). The reviewer, the board lane and the shell pick
   one pair of strip lengths from the table.

## Final commit

`5f864bf` `packing(v2c): apply round-6 layout rules 70-74`
Parent: `1897df0` `packing(v2c): real courtyards, layout v2 for the board`.
Round 6 reviewer merges `bcecc83` only.
