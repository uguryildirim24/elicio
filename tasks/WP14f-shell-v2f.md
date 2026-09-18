# WP14f — shell v2f: the lid boss and the long screw (Q89), then the wall-mounted charging pads per §5e (Q90, Q93) (lane w1)

Read `tasks/phase1-common.md`, your `.reports/WP14e-report.md`, the
verdict `tasks/reviews/code-r7.md` (defects 1 to 3 and 10, Seams "Shell
sections" and "Stamp vs HEAD", decisions 89, 90, 93),
`docs/fab/open-questions.md` Q89 to Q97 with the Round 7 verdict notes,
the merged shell on main (the reviewer's `a83e13b`: holes instead of
domes, `V2_CLOSURE` measuring `lid_engagement`), and
`tasks/WP11g-flat-pattern-v3.md` (what lane w3 is producing for you).
Lane `w1`, worktree `/Users/rolfie/projects/elicio/.worktrees/w1`, branch
`lane/w1-r6`, already at main `facb0c1`; `git merge main` first anyway.
Start line (coordinator restarts you by copy-paste):

    herdr agent start w1 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Why: the review measured that the M2.5×4 from the medial well ends at
y 5.55 inside the body's own tail while the lid underside is at 8.00,
so only the hinge lip holds the lid and the shell exits 3 (Q89); and the
charging pads leave the skin face for the far side wall (Q90), clamped
like the EMG heads so the charger cannot lift them (Q93). Nothing is
ordered.

Owns: as WP14e. Not the packing, not the board, not plan v2, not
open-questions, not order 1.

Deliver:

1. **Q89 now.** A lid boss dropping from the lid underside (y 8.00)
   into a tail pocket, the screw from the medial well through the
   body's tail boss into the lid boss with ≥ 3.0 mm of thread in the
   lid boss; state the resulting standard length (M2.5×8 or ×10,
   titanium button head as Q71) and the head position; pilot Ø2.10, boss
   OD ≥ 5.0, walls ≥ 1.4 around both bosses; `V2_CLOSURE` measures
   `lid_engagement` ≥ 3.0 and passes; hinge lip unchanged; lateral face
   unbroken; shell exit 0 again. Commit it.
2. **WAITING.** Unless the coordinator has sent the line "flat pattern
   v3" plus a sha, push `herdr agent prompt coordinator "WAITING WP14f
   flat pattern v3"` with the pane token per the common file and stop.
3. **On the prompt:** P4/P5 as clamped button heads in the side wall
   per §5e's wall-site table: Ø2.7 holes through the wall, standoff
   wells on the wall's inner face into the free bay, heads outside like
   P1–P3; the medial floor holes, the rib slot and the drop channel
   removed unless §5e keeps one; `V2_CHARGE_pads` re-specified for the
   wall (outer face open, ≥ 1.5 of wall around each seat, clearance to
   the cell pocket and the hinge lip, nylon ≥ 3.0 between heads);
   `V2_WALL_minima` probes the seats; the medial face carries P1–P3 and
   the well only; renders with the far side wall visible (a third view
   or an inset) so Rolf sees the pads; stamp = `manifest.commit` =
   solids commit; `shell-v2.md` §2, §4, §5; the before/after table.

Gates: as WP14e, plus shell exit 0 (`LC_ALL=C LANG=C .venv/bin/python -m
unittest discover -s tests -v` exit 0, the shell class, order 1
byte-identical, two consecutive shell runs identical, `manifest.py
--check-bytes`, `git status --short` empty). Commit in steps; the last
commit message describes the state reached. Report
`.reports/WP14f-report.md` (untracked). Closing steps per the common
file with `<PKG>` = `WP14f`, `<lane>` = `w1`, also when you fail.
