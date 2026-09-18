# WP11b — Packing follow-ups: the longer body for the buyable cell, the REF tab route (lane w3)

Read `tasks/phase1-common.md` first (for this package "the plan" is
`docs/fab/plan-v2.md`, signed off at `ef369bd`), then plan v2 §3, §4,
§5.3 (interface II), §11 row 11; `docs/fab/open-questions.md` Q50 to
Q68 (Q55, Q57, Q58, Q59 govern you); `docs/fab/packing-v2.md` in full;
`tasks/reviews/code-r5.md` defects 1 to 9 and decisions 57 to 59, 66;
`scripts/cad/placement_v2.py` and `tests/test_placement.py` as they are
on `main`. Lane `w3`, worktree `/home/user/projects/elicio/.worktrees/w3`,
branch `lane/w3` from `main`. Start line (coordinator restarts you by
copy-paste):

    herdr agent start w3 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Why: round 5's closers all use the 501015 cell, which nobody has verified
can be bought in ones (Q55). The buyable DTP301120 is 22 mm long and
closed nowhere at the v1 body length; the brief allowed a longer body
(+1.5, +3.0 mm of arc) only if nothing closed, so those runs never
happened. Separately the REF tab crosses the cavity end wall (Q59) and the
shell lane needs to know whether a route inside the cavity exists before
it cuts a slot. Analysis only; you change no plan, order nothing, contact
nobody.

Owns: `scripts/cad/placement_v2.py`, `scripts/cad/placement.py`,
`tests/test_placement.py`, `docs/fab/packing-v2.md` (generated: extend the
generator, do not hand-edit), the drawings the generator keeps under
`docs/fab/cad/v1/` (closers only, at most 20 files in total, Q56).
Not yours: `bte_fit_shell.py`, `render.py`, `manifest.py`, `tests/test_cad.py`,
anything under `docs/fab/cad/v2/` (WP14 on lane w1 owns them this round).

Deliver:

1. `placement.py --arc-plus 1.5|3.0` runs for the DTP301120 (22.0 × 11.5
   × 3.2, foam 0.5 per Q57) in series under interface II, widths 18 to
   20, LID_Y 7.0 to 9.0, standoffs 3.0 and 4.0, with the same measured
   conflict logic as the round 5 code (no new constants; the review's
   fixes 1 to 6 stay). Report the smallest body that closes for the DTP,
   its TOTAL_CHORD against the M1 gate (M1 52 default, Q34), and the
   length cost in millimetres against the 501015 winner. If nothing
   closes at +3.0, say so with the first conflict per run.
2. The REF tab route: with the 501015 winner's board and the tail site
   from `packing-v2.md` §5, search tab routes that stay inside the cavity
   (along the floor, along the lateral wall, or over the cell pocket's
   free air) with the flex 0.31 (0.11 + 0.2) at the tab, bend radius from
   `board-v2.md` §11, and report each route's minimum wall distance,
   crossing of the end wall (yes/no, where), and the length added to the
   tab. Publish the best route as a named layout in `packing-v2.md` and
   as numbers WP14 can cut (`docs/fab/packing-v2.md` §5 gets a "REF tab
   route" table); if no in-cavity route exists, say so and give the slot
   position and size that the wall would need (WP14 cuts it).
3. Tests for both: a failing test per new check with a parameter and a
   number; the generated doc compared in the test as round 5 does.

Gates: `.venv/bin/python -m unittest discover -s tests -v` green (your
venv needs `.[cad]` for the test that rebuilds the doc); `placement.py`'s
round 5 tests unchanged and passing; `packing-v2.md` regenerated, not
edited; order 1 untouched; `git status --short` empty. Commit in steps;
the last commit is `packing(v2b): arc-plus runs for the DTP and the REF
tab route`. Report `.reports/WP11b-report.md` (untracked): the two
result tables, what could not be measured, numbers taken as given with
sources, "Needs a decision", the final sha. Closing steps per the common
file with `<PKG>` = `WP11b`, `<lane>` = `w3`. A mid-package prompt from the
coordinator runs after your DONE as a new turn; push another DONE for it.
