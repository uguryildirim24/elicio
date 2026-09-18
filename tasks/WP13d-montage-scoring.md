# WP13d — montage lines 3.1–3.3 are scored by the pipeline, not by receive-check (Q96) (lane w4)

Read `tasks/phase1-common.md`, your `.reports/WP13c-report.md`, the
verdict `tasks/reviews/code-r7.md` (defect 8, decision 96),
`docs/fab/open-questions.md` Q96, `docs/fab/receiver-v2.md` and the
montage file its tests parse (§8). Lane `w4`, worktree
`/Users/rolfie/projects/elicio/.worktrees/w4`, branch `lane/w4`, already
at main `facb0c1`; `git merge main` first anyway. Start line
(coordinator restarts you by copy-paste):

    herdr agent start w4 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Deliver: one sentence in `receiver-v2.md` and one in montage §8 saying
that lines 3.1 to 3.3 (noise, flex and clench numbers) are scored by the
analysis pipeline after the session and that `receive-check` stops only
on the same-criterion lines 3.5 to 3.10; the reviewer's §8 walk test
(`tests/test_receiver_v2.py`) still passes; nothing else changes. No
order. Gates: `.venv/bin/python -m unittest discover -s tests -v` green
(CAD tests may skip by name); `git status --short` empty. Commit
`receiver(v2): montage 3.1–3.3 scored by the pipeline, not receive-check
(Q96)`. Report `.reports/WP13d-report.md` (untracked). Closing steps per
the common file with `<PKG>` = `WP13d`, `<lane>` = `w4`, also when you
fail.
