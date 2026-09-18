# WP11g — flat pattern v3 and pin table v3: charging pads in the far side wall (Q90), J2 inside, J3 a break-off tab (Q91, Q92), R9/R10 out (Q95), a cavity test for everything (lane w3)

Read `tasks/phase1-common.md`, your `.reports/WP11f-report.md`, the
verdict `tasks/reviews/code-r7.md` (Seams "One packing truth" and
"Charging pads", Attack points "J2 and J3", decisions 89 to 97),
`docs/fab/open-questions.md` Q89 to Q97 with the Round 7 verdict notes,
`docs/fab/shell-v2.md` §1 and §2 (cavity, walls, the hook root on the
hook-end face, the hinge lip), and `docs/fab/board-v2.md` §11 and §12
(RING_PAD footprint, the 7 × 7 zone). Lane `w3`, worktree
`/home/user/projects/elicio/.worktrees/w3`, branch `lane/w3`, already
at main `facb0c1` (round 7 merged); `git merge main` first anyway. Start
line (coordinator restarts you by copy-paste):

    herdr agent start w3 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Why: the round 7 review found the charging pads bare on the skin face (a
0 Ω skin-to-ground path against the plan's 220 kΩ per-path rule, Q90),
J2 and J3 with their hangs outside the body (Q91), the CHARGE tab rooted
outside the body against §5d's prose (Q92), unclamped rings (Q93) and two
useless resistors (Q95). The packing owns the sites and the flat
pattern; the shell and the board follow. Nothing is ordered.

Owns: as WP11f (`scripts/cad/layout_v2c.py`, `placement_v2.py`,
`placement.py` flags, `tests/test_placement.py`, `docs/fab/packing-v2.md`
regenerated, drawings under `docs/fab/cad/v2c/`, four at most). Not the
board, not the shell, not plan v2, not open-questions.

Deliver:

1. **Which wall.** From the shell's own geometry (the hook root sits at
   low u on the hook-end face and the hook curves forward over the top
   of the ear), state which side wall, u 0–1.50 or u 20.50–22.00, is
   the posterior edge hidden behind the ear, with the lines you used. If
   the wall far from the hook root is the posterior one, the pads go
   there (Q90); if not, use Q90's fallback, the hook-end end face beside
   the hook root, and say so with numbers.
2. **P4/P5 in that wall.** Two RING_PAD_D5_H2.7 seats on the wall's
   inner face in the free bay beside the cell (u 11.90–20.50, s
   1.50–14.90, floor 1.50 to board underside 4.81), the same clamped
   button-head construction as P1–P3 turned sideways: head through the
   1.50 wall, ring on the inner face, a 3.0 standoff into the bay; y and
   s such that nylon ≥ 3.0 between the heads, ≥ 1.5 of wall around each
   seat (Q93), clear of the hinge lip at the hook-end wall, the cell
   pocket and the pocket island's parts; the charge tab from the pocket
   island's edge folding 90° at R 1.5 onto the wall's inner face with
   flat coordinates and allowance; the CHARGE rectangle in the flat
   pattern; the rib slot and the drop channel leave the shell extras if
   nothing uses them.
3. **J2 inside, J3 a break-off tab (Q91, Q92).** J2's courtyard and hang
   inside the cavity with the cell's connector reachable; J3 on a
   break-off tab of the flat pattern joined by a ≤ 2.5 mm neck with a
   drawn cut line, removed before closing (the assembly sheet is not
   yours; name the step). A **cavity test**: every courtyard, hang and
   region of the folded board lies inside the cavity or on a declared
   exterior (the strips before folding, the break-off tab).
4. **R9/R10 out (Q95)**: 64 parts plus H1/H2 = 66 rows.
5. **Pin table v3 in §5e** (flat coordinates, side, rotation), the shell
   table with P1–P3's floor sites (unchanged) and P4/P5's wall sites
   (u, s, y, the wall named, head axis direction), the shell extras
   list; every rule re-checked (courtyards on both sides, pad-to-outline
   ≥ 0.30, Q97's 7 × 7 zones with no other courtyard inside, hole keep
   3.30, second-side height ≤ 3.31, no second-side part over a standoff
   or seat, wall ≥ 1.5 around each seat); tests for each; the drawing
   regenerated (≤ 4 files).

Gates: `LC_ALL=C .venv/bin/python -m unittest discover -s tests -v`
green; `packing-v2.md` byte-identical on a second run; drawings ≤ 4;
order 1 untouched; `git status --short` empty. Commit in steps; the last
is `packing(v3): flat pattern v3, charging pads in the far side wall, J2
inside, J3 break-off tab, R9/R10 out, pin table v3` only if every gate
passed. Report `.reports/WP11g-report.md` (untracked) with the wall
you chose and why. Closing steps per the common file with `<PKG>` =
`WP11g`, `<lane>` = `w3`, also when you fail.
