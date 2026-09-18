# WP16 — Record v2: requirement 5, the v2 decisions, the ledger skeleton (lane w9)

Read `tasks/phase1-common.md` first (for this package "the plan" is
`docs/fab/plan-v2.md`, signed off at `ef369bd`), then plan v2 §0, §1, §9,
§10, §11 row 16, §13; `docs/fab/open-questions.md` Q28 to Q49;
`docs/EARPIECE_DESIGN.md` in full. Lane `w9`, worktree
`/home/user/projects/elicio/.worktrees/w9`, branch `lane/w9`. Start
line (coordinator restarts you by copy-paste):

    herdr agent start w9 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

First: `git merge --ff-only main` in your worktree (your branch is behind).

Why: Rolf answered requirement 5 with "titanium" (Q28, Q49) and plan v2
made decisions that the design record must carry once each, so that no
later reader rebuilds them from the turn files. The ledger of §9 needs a
file that every later order sheet fills in. Docs only; no code, no CAD, no
orders, no vendor contact, no new research.

Owns: `docs/EARPIECE_DESIGN.md` (edits), `docs/fab/orders-v2.md` (new).
Nothing else.

Deliver:

1. `docs/EARPIECE_DESIGN.md`: requirement 5 reads titanium (ISO 7380 M2.5
   Grade 5 button heads as the skin contacts, per plan v2 §5.7 and Rolf's
   answer of 2026-09-17), with the old stainless wording gone from the
   requirement and the change dated in the file's history section. A new
   section "Plan v2 decisions (2026-09-17)" carrying D-1 to D-8 and Q37 to
   Q49 once each, one paragraph per decision in plain prose, each with the
   reading the build follows and, where Rolf still owes an answer, the
   words "waits for Rolf". Anything in the file that plan v2 superseded
   (the gauge-first sequence, the breadboard bench, the lug and wire
   contact, the 501015 cell as the only cell) is marked superseded in
   place with a pointer, not deleted.
2. `docs/fab/orders-v2.md`: the ledger skeleton of §9 and R8: one table
   per order (1 board, 2 shell, 3 small parts, conditional kit) with the
   columns item, quantity, status (quoted / catalogue / allowance), unit
   price as displayed, source URL and date, shipping, tax, import
   collection, delivered line total; every line from plan v2 §9 and §12
   filled with what the plan and its cited pages already state (marked
   with their status) and the rest left as named blanks; a rules section
   stating that no all-in total is claimed until every line is quoted or
   catalogue, that the shell's delivered maximum is reserved before order
   1 is paid, that Massachusetts use tax is 6.25 % where not collected,
   and that duties are a configured DDP figure or a documented reserve.
   Plain prose outside the tables; no number without a source or the word
   allowance.

Gates: `.venv/bin/python -m unittest discover -s tests -v` green (nothing
you touch is tested, run it anyway); each decision appears once in
`EARPIECE_DESIGN.md` (grep your own headings); `git status --short` empty.
Commit in steps; the last commit is `record(v2): requirement 5 titanium,
plan v2 decisions, ledger skeleton`. Report `.reports/WP16-report.md`
(untracked): what changed, the gate results, "Needs a decision", the final
sha. Closing steps per the common file with `<PKG>` = `WP16`, `<lane>` =
`w9`. A mid-package prompt from the coordinator runs after your DONE as a
new turn; push another DONE for it.
