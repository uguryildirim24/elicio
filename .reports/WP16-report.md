# WP16 report — Record v2

Lane `w9`, branch `lane/w9`, worktree
`/home/user/projects/elicio/.worktrees/w9`. Interpreter: Python
3.13.15 in a worktree-local `.venv`. `git merge --ff-only main` was
already up to date at `401f92d`. Docs only; no CAD extras installed.

## What changed

`docs/EARPIECE_DESIGN.md`:

- Requirement 5 is titanium: ISO 7380 M2.5 Grade 5 button heads (plan
  v2 §5.7; Rolf, 2026-09-17). The stainless and carbon-TPU wording is
  gone from the requirement. The change is dated under History.
- New section "Plan v2 decisions (2026-09-17)" with D-1 to D-8 and Q37
  to Q49 once each. Paragraphs that still need Rolf say waits for Rolf
  (D-1/Q38, D-2/Q47, D-5/Q41, D-8/Q44 country, Q46).
- Gauge-first sequence, breadboard bench, lug-and-wire joint, and
  501015 as the only cell are marked superseded in place with a
  pointer. History was not deleted.

`docs/fab/orders-v2.md`: ledger skeleton for §9 and R8. Four order
tables (board, shell, small parts, conditional kit) plus a
whole-project gate row. Catalogue lines take prices already in plan v2
§9 and §12. The rest are named blanks. Rules: no all-in total until
every line is quoted or catalogue; shell delivered maximum reserved
before order 1 is paid; Massachusetts use tax 6.25 % where not
collected; duties are a configured DDP figure or a documented reserve.

`plan.md`, `plan-v2.md`, and `open-questions.md` were not edited.

## Plan v2 §11 row 16

Acceptance: v2 decisions once each; requirement 5 to titanium.

Command:

```bash
rg -n '^### (D-[1-8]|Q3[7-9]|Q4[0-9])' docs/EARPIECE_DESIGN.md
```

Result: 16 headings, one each. D-1 to D-8 all present. Q37 to Q49 each
appear once (Q38, Q39, Q40, Q41, Q44, Q47 sit in the matching D
heading). Requirement 5 titanium at line 89.

## Gates

### Unit tests

Command:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

Result: Ran 129 tests in 15.009s. OK (skipped=22). Skips need `.[cad]`.
This lane does not own CAD and did not install that extra. Tests were
not changed.

### git status

`git status --short` empty after the two commits (report untracked
under `.reports/`, gitignored).

## What was not done

- No CAD extras, so 22 tests skipped.
- No vendor pages were fetched. Ledger URLs are only those already in
  plan v2 §12 C14. Sortafast, SparkFun, and JLC setup prices are
  catalogue from plan v2 §9 with URL blank.
- This lane did not run `git push`. A post-commit hook pushed
  `lane/w9` to origin after each commit.

## Needs a decision

None new. Already open for Rolf and named waits for Rolf in the
record: Q38 body height after WP11, Q41 R7, Q44/Q36 country, Q46 tool
install veto, Q47 objectives and residual risks, Q33 ceiling (ledger
ceiling row blank).

## Final commit sha

`cc22134f72b6041c41a43131ec518f01730822f2`

Message: `record(v2): requirement 5 titanium, plan v2 decisions, ledger skeleton`.
The design-record commit under it is `385fa14`.
