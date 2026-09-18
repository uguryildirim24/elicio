# WP13c — Q75: a montage line 3.4 dropout reports and does not stop S2 (lane w4)

Read `tasks/phase1-common.md`, `docs/fab/open-questions.md` Q75,
`docs/fab/receiver-v2.md` (the exit-code table and the paragraph around
"Whether a 3.4 dropout stops S2 is open"), `docs/fab/montage.md` §8 line
3.4, and the WP13b part of `tasks/reviews/code-r6.md` with its decision
75. Lane `w4`, worktree `/home/user/projects/elicio/.worktrees/w4`,
branch `lane/w4` at `110a79b` (main after the round 6 merge). Start line
(coordinator restarts you by copy-paste):

    herdr agent start w4 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Why: the round 6 reviewer left one question on your receiver open,
whether a line 3.4 dropout (rail or flat for more than 200 sample
intervals) stops session S2. The coordinator's reading is Q75: it does
not. A dropout is reported, counted and written into the session record;
S2 continues. Lines 3.5 to 3.10 keep their stop (exit 1). Nothing else
about the tool changes.

Owns: `src/elicio/receiver_v2.py`, the CLI module that registers
`receive` and `receive-check` (the `receive-check` command only),
`tests/test_receiver_v2.py` and its fixtures, `docs/fab/receiver-v2.md`,
and the one sentence in `docs/fab/assemble.md` that tells Rolf what to do
when the check reports a dropout (w9 is idle; touch nothing else in that
sheet). Not `docs/fab/montage.md` (its table stays; the reading lives in
open-questions and receiver-v2), not the firmware, not the board, not
`docs/fab/plan-v2.md` or `docs/fab/open-questions.md`.

Deliver:

1. `receive-check`: exit 3 stays the distinct code for "no scored line
   failed, but a 3.4 dropout occurred". Its output names the dropout
   count, the longest run in sample intervals and where it began, and
   ends with the line `S2 continues (Q75); dropout count goes in the
   session note`. A same-criterion failure with dropouts is still exit 1
   by its own rule, with the dropout count printed beside it. Exit codes
   0, 1 and 2 keep their meaning. Whatever the tool writes for the session
   record (a summary line, a JSON, a note file; follow what WP13b built)
   carries the dropout count.
2. `docs/fab/receiver-v2.md`: the exit-code table says exit 3 is a report,
   not a stop, and cites Q75; the sentence that calls it open goes.
3. `docs/fab/assemble.md`: at a reported dropout, Rolf notes the count and
   continues; he stops only on exit 1 or 2. One sentence, in the sheet's
   voice.
4. Tests for the three cases: dropout only (exit 3, the "continues" line
   present); failure plus dropout (exit 1, the count printed); clean (exit
   0). Regenerate a fixture only if an existing one cannot show the case.
   `elicio receive --simulate-live` still exits 0.

Gates: `.venv/bin/python -m unittest discover -s tests -v` green with the
`ble` extra installed in your venv; `elicio receive-check` on each fixture
exits as the table says (paste the three runs in the report); `git
status --short` empty. One commit, `receiver(v2c): a 3.4 dropout reports,
S2 continues (Q75)`. Report `.reports/WP13c-report.md` (untracked).
Closing steps per the common file with `<PKG>` = `WP13c`, `<lane>` =
`w4`, also when you fail.
