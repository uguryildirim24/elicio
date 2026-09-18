# WP11d — layout v2c: the edge rule both ways, two widths, two sides (lane w3)

Read `tasks/phase1-common.md`, your `docs/fab/packing-v2.md` §5b and
`.reports/WP11c-report.md`, `docs/fab/open-questions.md` Q69, Q70, Q72,
Q73, Q74 and the new Q78, Q79, Q80 (main), the round 6 verdict
`tasks/reviews/code-r6.md` "To WP12c", and `docs/fab/board-v2.md` §12
(the JLC terms sentence). Lane `w3`, worktree
`/home/user/projects/elicio/.worktrees/w3`, branch `lane/w3` on top of
`1897df0`. First `git merge main` (keep both sides; main has the round 6
merge and the reviewer's §5 cell record), then work. Start line
(coordinator restarts you by copy-paste):

    herdr agent start w3 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Why: §5b says no layout closes, with "JLC assembly edge 2.5 mm" read as
component body to the board's own outline, single-sided. The JLC sentence
also requires edge rails, so the coordinator's reading (Q78) is that the
2.5 mm is measured from the panel's rail edge; a research lane is reading
the pages in parallel. You give the numbers under both readings so the
decision is arithmetic when the page answer lands. Nothing is ordered.

Owns: `scripts/cad/placement_v2.py`, `scripts/cad/placement.py` flags,
`tests/test_placement.py`, `docs/fab/packing-v2.md` (regenerated, never
hand-edited; §5b stays, add §5c), at most four new drawings under
`docs/fab/` (Q56). Not the board files, not the shell, not order 1, not
plan v2, not open-questions.

Fixed inputs (do not vary): the 501012 pack only (Q69's record cell; the
17.0 pack waits for Rolf); contact sites as in §5; Contact rule per Q79
(R1–R3 on the island at the tab roots, one Contact trace per 2.5 mm tab,
no other part on a tab); J1 USB-C on the hook-end face with its receptacle
body as an occupant and J4 (TC2030) on the leftover with its keep-out as a
board no-part zone (Q80); three FR4 0.2 ring pieces (Q72); two Ø2.7 island
holes at the boss sites (Q73); the tab fold pockets variant (Q74); SW1
under the lid recess; module keep-out empty; copper-to-edge 0.30;
courtyard-to-courtyard ≥ 0 with the 0.10 mask margin.

Vary, as a full grid:

1. Edge rule: (a) process-edge reading: courtyard inside the outline,
   copper-to-edge 0.30, nothing else; (b) 2.5 mm from component body to
   the board's own outline.
2. Body width 20 (the shell as built) and 22 (island 2 mm wider; give the
   new island and leftover sizes from the same packing arithmetic).
3. TOTAL_CHORD 47.90 (as built) and 49.00 (the M1 gate at M1 = 52; give
   the added island or leftover length).
4. Sides: top only, and top plus the second side of the island and the
   leftover for parts whose body height fits the measured clearance under
   the board. Compute that clearance from the stack (standoff, board
   thickness, foam, cell top, the pocket) and state it with its source
   rows; parts on the second side never sit over a ring seat, a boss, a
   standoff or a tab root.

For each of the 16 cells: footprints placed of 66, the first rule that
cannot be met, island and leftover fill, which parts went to the second
side. Then the smallest configuration under each edge reading that places
all 66 (or the statement that none does, with the shortfall in mm² and the
parts left over). One table, one paragraph per reading, generated into
`packing-v2.md` §5c. If the process-edge reading at width 20, chord 47.90
places all 66 on two sides, that is the layout WP12d takes: publish its
placement table in §5c in the §5 format (ref, side, centre u/s, rotation,
courtyard) so the board lane can pin it.

Tests: the courtyard read-back test stays; add one that the §5c winning
layout (if any) has zero courtyard overlaps, every part inside its region,
no second-side part over a seat, boss, standoff or tab root, and the
Contact rule met.

Gates: `.venv/bin/python -m unittest discover -s tests -v` green; §5c
byte-identical on a second `--packing-doc` run; order 1 untouched; at most
four new drawings; `git status --short` empty. Commit in steps; the last
is `packing(v2c): layout grid, edge rule both ways, two sides`. Report
`.reports/WP11d-report.md` (untracked) with the 16-cell table pasted.
Closing steps per the common file with `<PKG>` = `WP11d`, `<lane>` = `w3`,
also when you fail.
