# Code review + fix — Phase 1 round 4 (WP8-prep, WP9b) on branch review/r4 (Claude Opus 5, high)

You are the reviewer for this round, herdr agent `rev4`. Two lanes
finished their packages. You merge them into one candidate, inspect it,
**fix what is wrong yourself**, run every gate, and write one verdict. You
never push by hand, never merge into `main`, never touch another worktree,
never edit `docs/fab/plan.md` or `docs/fab/open-questions.md`.

Worktree `/home/user/projects/elicio/.worktrees/review`, branch
`review/r4` from `main`. Private environment inside this worktree:
`python3.13 -m venv .venv && .venv/bin/python -m pip install -e '.[cad]'`.

## Steps

1. Read `tasks/phase1-common.md`, `docs/fab/open-questions.md` (Q5, Q11,
   Q18, Q20 to Q23 govern WP8-prep), the two briefs
   `tasks/WP8-prep-stageb.md` and `tasks/WP9b-record.md`, the verdicts
   `tasks/reviews/code-r1.md` (defects 1 to 13 and decision 5 on the script;
   defects 29 and 30 on the record), `code-r2.md` and `code-r3.md`
   (decisions 20 to 23), and `docs/fab/plan.md` §3.3, §3.5, §3.6, §5, §6,
   §9 row WP8, §10 open item 4.
2. Merge, in this order, resolving conflicts yourself: `lane/w9`, `lane/w2`.
   Each lane's diff against `main` shows `HANDOFF.md` and `HANDOFF.json` as
   changed only because `main` moved after the lanes branched; keep
   `main`'s.
3. Gates, all on the merged tree:
   - `.venv/bin/python -m unittest discover -s tests -v` passes with the CAD,
     render and placement tests running, not skipped.
   - Order 1 untouched: reference build twice, fifteen solids identical to
     each other and to `docs/fab/cad/v1/`; `render.py` twice, three views
     identical; `manifest.json` under `docs/fab/cad/v1/` equal to `main`'s
     byte for byte (WP8-prep may bump the schema only for Stage B builds;
     if the v1 manifest changed, that is a defect unless the brief's schema
     rule forced it, in which case the validator, tests and README all say
     so).
   - The provisional Stage B build from the README command into a temp
     dir, twice: byte-identical; every named Stage B check reports; the
     checks that must fail today (Q21 reference lug against the lid or
     pocket wall) fail with their numbers and the tests assert exactly
     that.
   - `MOCK_CONTACTS = false` without the Stage B checks present is still
     refused (round 1 decision 5 guard lifted only by the checks).
   - `git diff main -- src/ docs/fab/plan.md docs/fab/open-questions.md
     docs/fab/interface.md docs/fab/packing-options.md docs/fab/contacts.md`
     is empty; nothing exists under `docs/fab/cad/v2/`.
4. Adversarial review: the seams below first, then the attack points.
   Build one Stage B body yourself with `PACKING = C` and look at it (a
   quick render or section through the contact holes and the tail pocket)
   before trusting the checks.
5. Fix every defect yourself, in separate commits on `review/r4` with
   messages starting `review(WPn):`. The repo's post-commit hook pushes on
   commit; do not run `git push` yourself.
6. What cannot be fixed without changing the plan goes under "Needs a
   decision", numbered from 24.

## Seams

- **Order 1 must not move.** WP8-prep touches the same script that builds
  the order 1 solids. Any change in the fifteen hashes or the three views
  is a High defect, whatever the reason.
- **Pads shared, not copied.** The brief requires the option C pads to be
  read from one place shared with `placement.py`. A second copy of the pad
  table in `bte_fit_shell.py` is a defect; check the refactor is the
  smallest one and that `placement.py`'s own tests still pass unchanged.
- **Real lug envelopes.** Flat tab 1.96 wide, height 2.0 (Q22), from the
  Ø7.1 edge to 8.85 from the contact centre (C-31428: 8.788 max, 8.85 kept
  as conservative), per-contact angle; the reference lug upright with 0.46
  stock and a 1.96 barrel per `contacts.md` §5.3 and §8.1. The Q21
  collision (about y 8.2 against the lid at 8.0, or the pocket wall at
  3.75) must be reported by name, not resolved silently.
- **Stage B checks are measured, not constants** (round 1 defect 4 all over
  again is the risk): hole through the 1.5 wall only; keep-outs and tab
  envelopes are air; board underside 4.3 above stack tops 4.13 and barrels
  3.46; the Ø1.3 reference wire envelope at bend radius 3 contained in
  cavity air and clear of the battery pocket, charge pads and lid (open
  item 4); CABLE_EXIT meets the cavity only; the cell envelope with 0.5
  foam fits; E1/E3/E5 present or absent by `CLOSURE_PASSED`.
- **Packing switch.** C: BODY_WIDTH 20, board 19 × 15.5, option C pads,
  the wire crossing where nothing sits above it; B: BODY_ARC +3.5 with the
  tail, channel and wrap moved (round 3 defect 5); A: plan shell. The
  manifest names the option and `provisional: true`.
- **Provisional file header** lists which open question each provisional
  value waits on; the README says what is and is not decided; nothing
  claims order 2 files exist.
- **WP9b**: the record's diff removes 41 lines. Verify nothing above
  "Fabrication plan, 2026-09-16" changed, requirements 1 to 7 are intact,
  no history bullet is gone, and the removed lines are the old open
  question 3 and 4 text now replaced by status sentences. The three facts
  appear once each and point at the files that hold the numbers; each §2
  decision still appears once (the lane's grep); the L2 erratum is one
  line under the title and nothing else in that report moved.
- 98 tests OK with 8 skipped in w9's venv (no cad extra); WP8-prep's own
  count from its report.

## Seams from WP8-prep's report (lane w2, 39a62d9)

- **Two builders.** The report says order 1 "still uses the previous gauge
  builder, so the fifteen solids stay byte-identical", which reads as a
  second construction path for Stage B beside the gauge path. Decide
  whether the Stage B path shares the §3.5 construction (path map, body,
  tail, hook, fillets, hook-in-cavity cut, lid) with only the cuts and
  envelopes added, or forks it. A fork that will drift from the gauge is a
  defect unless the hash constraint truly forced it; if so, the shared
  parts must be shared functions and the README must say what is common.
- **`--parts` flag.** The provisional build used
  `--parts body_full_p15,lid,coupon`. Check the flag is documented, that a
  Stage B build without it does something sensible, and that the stale-part
  guard from round 1 still holds for `--out` directories.
- **Q21 recorded as a failing check that does not stop the write.** That is
  what the brief asked for, but the manifest must then say the build does
  not pass (a `passed: false` or equivalent at the top level), the exit
  code must not be 0 without saying why, and the tests must assert the
  numbers (lug top 8.23 against lid 8.0; barrel outer 4.54 against pocket
  radius 3.75).
- **Pads from `placement.py`.** Check `bte_fit_shell.py` imports
  `PADS_BY_OPTION` / `get_layout` without pulling matplotlib into the CAD
  build at import time (lazy import or a data-only module), and that
  `placement.py` is byte-identical to `main`.
- **Cell check foam reading.** Foam only as the superior lid-face strip
  (plan §5); clearances 0.3 / 0.4 / 0.4 mm on the 5.2 × 10.4 × 15.6 envelope.
  Confirm against plan §5 and interface §5, and that Q18's provisional
  status is in the manifest.
- **Schema.** Stage B manifest stays schema 1 with added keys validated only
  when `stage` is B; the committed v1 manifest must validate unchanged and
  `render.py`'s reading of the manifest must not break on the new keys.
- 111 tests OK in 39.6 s in w2's venv.


## Attack points per package

- **WP8-prep**: the guard from round 1 decision 5 is lifted only when the
  Stage B checks run; each check has a failing test with a parameter and a
  number; `stageb_provisional.toml` builds into a temp dir by the README
  command and never into `v1/` or `v2/`; the manifest for a Stage B build
  validates under the (possibly bumped) schema and the v1 manifest still
  validates under its own; `manifest.py`, `render.py` and
  `tests/test_cad.py` agree on the schema; the README's provisional command
  runs from a clean venv; no vendor, no order, no upload.
- **WP9b**: the record's voice; "Rolf" not "the owner" in new prose; no
  numbers the cited files do not have; the erratum line is dated and cites
  plan §2 row 5.

## Output

1. `tasks/reviews/code-r4.md`: a three-line verdict (MERGE /
   MERGE-AFTER-DECISION / REJECT), the gate results with commands, a table
   of defects (severity, file:line, what was wrong, what you changed, commit
   hash), and "Needs a decision" numbered from 24. Commit it on `review/r4`.
2. `.reports/review-r4-report.md` in this worktree: what you merged, what
   you changed, the final commit sha.
3. Then, in order:

       herdr pane report-metadata "$HERDR_PANE_ID" --source lane --token lane=review-r4 --token done=1
       herdr notification show "review r4 done" --body "reviewer rev4" --sound done
       herdr agent prompt elicio "DONE review-r4 .reports/review-r4-report.md <final commit sha>" || herdr agent prompt elicio "DONE review-r4 .reports/review-r4-report.md <final commit sha>"

Your turn must end with that push, including if the verdict is REJECT. If
you start a helper lane, close its tab before you push.

## The worker reports, verbatim

### WP9b report (lane `w9`, branch `lane/w9`)

````md
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
````

### WP8-prep report (lane `w2`, branch `lane/w2`)

````md
# WP8-prep report (lane w2)

Stage B path in the gauge script, with provisional inputs. No files under
`docs/fab/cad/v1/` or `docs/fab/cad/v2/`.

## What was built

- `scripts/cad/bte_fit_shell.py`: `MOCK_CONTACTS = false` now builds. It
  cuts CONTACT_HOLE Ø2.9 through the 1.5 mm wall, KEEPOUT_REF Ø7.5, WIRE_CHANNEL,
  CABLE_EXIT Ø2.0, and reserved-air TE 31428 tab envelopes (1.96 × 2.0, Ø7.1
  to 8.85). Order 1 (`MOCK_CONTACTS = true`) still uses the previous gauge
  builder, so the fifteen solids stay byte-identical.
- `PACKING = A | B | C` (default C). Pad coordinates and tab angles come from
  `placement.py` (`PADS_BY_OPTION` / `get_layout`). `placement.py` was not
  edited.
- Named Stage B checks: `CONTACT_HOLE_wall`, `KEEPOUT_SIGNAL_air`,
  `KEEPOUT_REF_air`, `TAB_envelope_air`, `BOARD_underside_clear`,
  `REF_WIRE_envelope`, `CABLE_EXIT_cavity`, `CELL_envelope`, `Q21_REF_lug`,
  `CLOSURE_PASSED`. Q21 records a fail with numbers and does not stop the
  write. The other named checks fail loudly with the number.
- `scripts/cad/params/stageb_provisional.toml`: PACKING C, MOCK_CONTACTS
  false, CLOSURE_PASSED false, plan §3.3 contact sites, TAB_HEIGHT 2.0. Header
  lists the open question for each value. `--out` of `v1/` or `v2/` is refused.
- Stage B manifest stays schema 1 and adds `stage`, `provisional`, `packing`,
  `closure_passed`, `contact_source`, `stage_b`. `scripts/cad/manifest.py`
  validates those keys when `stage` is `B`.
- README section "Stage B (provisional)" with the build command.
- Tests for the lifted guard, packing A/B/C, each named failing case, Q21
  numbers, CLOSURE_PASSED, v1/v2 refuse, and a two-process regen of the
  provisional build.

## Plan §9 / brief acceptance

| Item | Command | Result |
|---|---|---|
| Full suite | `.venv/bin/python -m unittest discover -s tests -v` | 111 tests, OK, 39.6 s |
| Order 1 solids and views vs main | compare `docs/fab/cad/v1/manifest.json` `files` and `views` to `main` | equal; `commit` `66b5564…` |
| Order 1 regen | `tests.test_cad.CadRegenTests` | OK |
| Provisional Stage B build | `.venv/bin/python scripts/cad/bte_fit_shell.py --params scripts/cad/params/stageb_provisional.toml --out <tmp> --parts body_full_p15,lid,coupon` | exit 0; Q21 fail `lug_top_y=8.23` vs `lid_y=8.0`, `barrel_outer=4.54` vs `pocket_r=3.75`; other named Stage B checks pass |
| Stage B regen | two fresh processes, same command | `files` maps equal |
| Manifest schema | validator on the Stage B temp manifest and on committed v1 | both OK |

## What was not done

- No order 2 solids under `docs/fab/cad/v2/`.
- Contact sites are still plan §3.3 defaults (WP7a).
- E1/E3/E5 stay off (`CLOSURE_PASSED = false`).
- No purchase, no upload.

## Needs a decision

- Q20 packing: this path defaults to C. A and B are switches. Rolf has not
  picked.
- Q21 reference lug: TE 31428 upright collides with the lid (8.23 vs 8.0)
  and the pocket wall (4.54 vs 3.75). The check reports it. It does not hide
  the lug.
- Q18 cell pack: the pocket check uses 5.2 × 10.4 × 15.6 with 0.5 mm foam on
  the lid face (clearances 0.3 / 0.4 / 0.4 mm). A real folded pack may not
  match.
- Closure test: `CLOSURE_PASSED` is a flag. This package does not decide it.
- Foam on all cell faces would not fit the 10.8 mm pocket in u (10.4 + 2×0.5).
  The check treats foam as the superior lid-face strip in plan §5.

## Final commit

`39a62d9f6f7aaa1c8e32902e5a55e3e8cdf17b6b`
````

