# WP11f — J4's real hole sites, R24 folded back, pin table v2.1 (lane w3)

Read `tasks/phase1-common.md`, your `.reports/WP11e-report.md`,
`docs/fab/open-questions.md` Q85 to Q87 and the Round 7 notes (main),
and w2's report and log on `lane/w2`
(`/home/user/projects/elicio/.worktrees/w2/.reports/WP12e-report.md`,
`/home/user/projects/elicio/.worktrees/w2/hardware/board/route.md` §9,
"Hole nudges" and "Zero-track DRC"). Lane `w3`, worktree
`/home/user/projects/elicio/.worktrees/w3`, branch `lane/w3` on top of
`408a476`; `git merge main` first. Start line (coordinator restarts you
by copy-paste):

    herdr agent start w3 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Why: §5d's J4 NPTH keep-out sits at (16.25, 22.06), (17.27, 27.14),
(15.23, 27.14); KiCad's `Tag-Connect_TC2030-IDC-NL` at the pinned
(16.25, 24.60) rot 90 puts them at (16.25, 27.14), (15.234, 22.06),
(17.266, 22.06): the pair and the single are swapped along s, so R24
on B.Cu lands on a real hole. The board lane moves R24 now (WP12f,
Q87); the table must stop being wrong. Nothing is ordered.

Owns: as WP11e. Not the board, not the shell, not plan v2, not
open-questions.

Deliver:

1. J4's hole centres computed from the KiCad footprint file at the
   pinned position and rotation (parse `hardware/board/…` footprint or
   `git show 30ca79d:hardware/board/elicio-v2.kicad_pcb`), not from a
   hand model; a test that the three centres equal KiCad's within 0.01.
2. Re-run the build cell with the corrected both-side keep-out; if R24
   (or any part) moves, take the smallest move that meets every rule
   and note where the board lane's own move (route.md §10 on `lane/w2`,
   when it exists; else its zero-track DRC) differs; the reviewer
   reconciles within 0.1 mm, the board being the truth for copper.
3. Pin table v2.1 in §5d (same 68 rows; the folded-site table and the
   flat pattern unchanged unless a rule forces it, then say so), the
   drawing regenerated, packing doc byte-identical twice.

Gates: unittest green; drawings ≤ 4; order 1 untouched; `git status
--short` empty. Last commit `packing(v2f): J4 hole sites from the KiCad
footprint, pin table v2.1`. Report `.reports/WP11f-report.md`
(untracked). Closing steps per the common file with `<PKG>` = `WP11f`,
`<lane>` = `w3`, also when you fail.
