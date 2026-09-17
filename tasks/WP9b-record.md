# WP9b — Design record after rounds 1 to 3, and one lane-report erratum (lane w9)

Read `tasks/phase1-common.md` first, then `docs/fab/open-questions.md`.
Lane `w9`, worktree `/Users/rolfie/projects/elicio/.worktrees/w9`, branch
`lane/w9`, fast-forwarded to `main` (round 3 merged at `1170b2a`). Start
line (coordinator restarts you by copy-paste):

    herdr agent start w9 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Spec: plan §9 row WP9 ("each §2 decision appears once"), §10.
`tasks/reviews/code-r1.md` defects 29 and 30 (what the round 1 reviewer
changed in your section and why open question 3 was reopened),
`code-r2.md` and `code-r3.md` verdict lines, `docs/fab/packing-options.md`,
`docs/fab/contacts.md` §8, `docs/fab/montage.md` §1.

Owns: `docs/EARPIECE_DESIGN.md` (the fabrication section you wrote and the
open questions; nothing above "Fabrication plan, 2026-09-16" changes; no
history removed; requirements 1 to 7 untouched), and one erratum line at
the top of `docs/fab/L2-vendors.md`.

Deliver:

1. In the fabrication section, a short dated subsection "Phase 1, rounds 1
   to 3 (2026-09-17)" in the record's voice: what exists now (order 1
   solids, renders, drawing, interface v2, measurement and order sheets,
   contacts kit with drawings, frozen protocol, packing sheet), the one
   place decisions after the plan live (`docs/fab/open-questions.md`, with
   the reading-the-build-follows rule), and the three facts that changed the
   design's shape: no crimp ring lug ends under its pad; only the 3 mm
   wider body closes the packing on the real lug, pending Rolf; no
   published cell pack fits folded, so the plan's hand fold stands until a
   cell is measured. Each fact once, each pointing at the file that holds
   the numbers. No numbers the files do not have.
2. Open questions in the record: question 3 (electronics fit) says what
   WP6 found and that the pick is Rolf's (Q20); question 4 (contact
   positions) says the plan §3.3 defaults stand until WP7a part 2, which
   waits on the Stage A parts, and that the reference site is checked when
   the gauge is worn (Q17). Do not strike anything through; state the
   status.
3. `docs/fab/L2-vendors.md`: one line under its title, dated, saying that
   its "no bureau prints conductive TPU" finding was superseded the same
   day (Palmiga prints it; plan §2 row 5), and that the plan does not use
   conductive TPU. Nothing else in that report changes.

Do not edit `plan.md`, `open-questions.md`, `AGENTS.md`, `README.md`,
anything under `docs/fab/` except the one L2 line. New prose says "Rolf".

Acceptance: plan §9 row WP9 still holds (each §2 decision appears once;
grep for duplicates); the new subsection states each of the three facts
once; questions 3 and 4 carry a status. Gates: unit tests unchanged and
green.

Report: `.reports/WP9b-report.md` (keep it untracked). Closing steps per
the common file with `<PKG>` = `WP9b`, `<lane>` = `w9`.
