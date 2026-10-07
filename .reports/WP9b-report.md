# WP9b report — Design record after rounds 1 to 3

Lane `w9`, branch `lane/w9`, worktree
`/home/user/projects/elicio/.worktrees/w9`. Interpreter: Python 3.13.15
in a worktree-local `.venv` (already present; not recreated). No
optional-dependency group was added; this package touched no code.

Started from `aecfba4` (main, round 4 briefs). Round 1 reviewer defects
29 and 30 were already on that tree: row 9 matches the plan, and
question 3 was left open until WP6.

## What was built

`docs/EARPIECE_DESIGN.md`, inside "Fabrication plan, 2026-09-16" only:
a subsection "Phase 1, rounds 1 to 3 (2026-09-17)". It names what exists
now (order 1 solids, renders and drawing in `docs/fab/cad/v1/`,
interface version 2, measurement and order sheets, contacts kit with
drawings, frozen protocol, packing sheet), that later decisions live in
`docs/fab/open-questions.md` with the reading-the-build-follows rule,
and these three facts once each:

- A crimp ring lug does not end under its pad (`docs/fab/contacts.md` §8).
- Only the 3 mm wider body closes packing on that lug, pending Rolf
  (`docs/fab/packing-options.md`).
- No published cell pack fits folded; the plan's hand fold stands until
  a cell is measured (`docs/fab/interface.md` §5).

Open questions 3 and 4 now carry a 2026-09-17 status, with no
strikethrough. Question 3: WP6 ran packing on the real lug; the pick is
Rolf's (Q20). Question 4: plan §3.3 defaults stand until WP7a part 2
(waits on Stage A parts, `montage.md` §1); the reference site is checked
when the gauge is worn (Q17).

Nothing above "Fabrication plan, 2026-09-16" changed. Requirements 1 to
7 were not edited. History was not removed. New prose uses "Rolf".

`docs/fab/L2-vendors.md`: one dated erratum line under the title. The
"no bureau prints conductive TPU" finding was superseded the same day
(Palmiga prints it; plan §2 row 5). The plan does not use conductive
TPU. Nothing else in that report changed.

`plan.md`, `open-questions.md`, `AGENTS.md`, `README.md`, and the rest
of `docs/fab/` were not edited.

## Plan §9 acceptance

Row WP9: each §2 decision appears once.

Command:

```bash
rg -n '^[0-9]+\. \*\*(Battery|Envelope|Contact metal|Contact size|Conductive TPU|Lid closure|Gauge material|Montage|Contact count|Suspension|Ear capture|Shipping|Shells and PCB|Hook|Gasket|Charging|Short ears)\.\*\*' docs/EARPIECE_DESIGN.md
```

Result: seventeen hits, one per heading, lines 275–319. No duplicates.

Three facts once:

```bash
rg -n 'does not end under its pad|3 mm wider body|No published cell pack' docs/EARPIECE_DESIGN.md
```

Result: three hits, lines 358, 361, 364. One each.

Questions 3 and 4: each has a "Status 2026-09-17" sentence (question 3
wraps the date onto the next line).

## Gates

### Unit tests

Command:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

Result: Ran 98 tests in 14.379s. OK (skipped=8). Skips are CAD/render
tests that need `.[cad]` (build123d, matplotlib, trimesh). This lane
does not own CAD and did not install that extra. Tests were not
changed.

### WP9 acceptance row

See the grep results above.

## What was not done

- No CAD extras were installed, so eight tests skipped. They were
  already skippable without `.[cad]`.
- Question 1 still uses strikethrough from 2026-08-13. This package
  was told not to strike questions 3 and 4; question 1 was left as
  history.
- This lane did not run `git push`. A post-commit hook pushed
  `lane/w9` to origin after each commit. The common file says never
  push.

## Needs a decision

None new from this package. Q20 (packing option C) and Q17 (reference
on bone after gauge wear) remain Rolf's, already in
`docs/fab/open-questions.md`. Requirement 5 versus titanium remains
Rolf's (Q12).

## Final commit sha

`40fe97ce950e18946b7cee9060b5d221610cb5e9`

That commit is `docs(fab): erratum L2 conductive-TPU finding` on
`lane/w9`. The design-record commit under it is `94f0f40`.
