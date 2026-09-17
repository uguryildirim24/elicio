# Code review + fix — Phase 1 round 1 (WP1, WP2, WP4, WP5, WP9) on branch review/r1 (Claude Opus 5, high)

You are the reviewer for this round, herdr agent `rev1`. Five lanes finished
their packages. You merge them into one candidate, inspect it, **fix what is
wrong yourself**, run every gate, and write one verdict. You never push by
hand, never merge into `main`, never touch another worktree.

Worktree `/home/user/projects/elicio/.worktrees/review`, branch
`review/r1` from `main` (`11b4786`). Private environment: inside this
worktree, `python3.13 -m venv .venv && .venv/bin/python -m pip install -e .`
and, after merging `lane/w2`, `.venv/bin/python -m pip install -e '.[cad]'`
(WP2 built on Python 3.13.15 with build123d 0.11.1; no 3.12 fallback needed).

## Steps

1. Read `tasks/phase1-common.md`, the five briefs `tasks/WP1-interface.md`,
   `tasks/WP2-gauge.md`, `tasks/WP4-sheets.md`, `tasks/WP5-contacts.md`,
   `tasks/WP9-record.md`, and `docs/fab/plan.md` (signed off at `0c5d0eb`)
   sections 2, 3, 4, 5, 6, 9 and 10.
2. Merge, in this order, resolving conflicts yourself: `lane/w9`, `lane/w1`,
   `lane/w4`, `lane/w5`, `lane/w2`. `main` gained
   `tasks/review-code-template.md` after the lanes branched; keep it. The
   lanes' diffs against `main` show it as deleted only for that reason.
3. Gates, all on the merged tree:
   - `.venv/bin/python -m unittest discover -s tests -v` passes, and
     `tests/test_cad.py` must actually run, not skip: install build123d.
   - Run WP2's reference build twice into two temp dirs and compare hashes;
     regeneration must be byte-identical. STEP writers often embed a
     timestamp; if the hash rule silently excludes files or the test only
     hashes some of them, that is a defect.
   - Verify any "pre-existing failure" claim on an untouched `main` checkout
     before accepting it.
4. Adversarial review: the cross-lane seams below first, then the attack
   points per package. Two documents that disagree on one dimension is a
   defect. A sentence Rolf cannot follow with a caliper is a defect. A
   check the plan names that the script does not run is a defect.
5. Fix every defect yourself, in separate commits on `review/r1` with
   messages starting `review(WPn):`. Keep the workers' structure unless it
   is wrong. The repo's post-commit hook pushes branches on commit; that is
   not you pushing, but do not run `git push` yourself.
6. What cannot be fixed without changing `docs/fab/plan.md` goes under
   "Needs a decision" with your reading. Do not edit `plan.md`.

## Cross-lane seams (from the reports)

- **Chord gate direction.** Plan §3.3 literally writes `TOTAL_CHORD > M1 − 3`,
  which fails the default ear; §1, §2 row 17, §10 item 1 and turn 07 state
  `M1 ≥ TOTAL_CHORD + 3` (about 50.9 mm at bow 3, 51.3 at bow 1). WP4's
  sheets implement the latter; WP2 was told mid-package to do the same.
  Check the script, `measure.md` and `order1.md` agree to the decimal.
- **Nut material.** WP1 followed the plan (DIN 439 / ISO 4035 thin nut,
  1.6 mm; the WP1 brief's "ISO 4032" was my error and would not fit). WP5
  found no titanium thin nut at retail and recommends 18-8 stainless, a
  nickel-bearing alloy, inside the sealed cavity under Kapton, citing an
  "internal allowance" in plan §4. Decide from the plan text whether such
  an allowance exists. Check WP5's internal-metal list, WP1's insulation
  section and WP9's record of requirement 5 tell one story. If the plan
  does not allow it, the fix is in the documents (option C, a titanium
  DIN 934 nut at 2.0 mm, is WP5's own alternative; check its stack).
- **Dome dimensions.** Interface v1 carries the plan's 4.7 × 1.35 mm dome;
  ISO 7380-1 has no M2.5 row and WP5's verified heads may read 4.5 × 1.5.
  Check WP1's dome row, WP5's SKU drawings and WP2's `CONTACT_DOME` agree.
  If they cannot, record it as an interface v2 item in `interface.md`;
  never silently change the CAD constant.
- **Lug thickness and the stack.** WP1 flagged 0.5 mm UNVERIFIED; WP5
  found TE 31428 at 0.46 mm. Check lug + nut + screw tip + Kapton ≤ 2.63 mm
  in `interface.md`, `contacts.md` and the script's `CONTACT_STACK`, with
  the same component numbers in all three.
- **Pad-to-keep-out 0.09 mm** (WP1 §7). Does WP2's script check it, and does
  the reference build pass it?
- **Packing shortfall** (105 versus 111 mm²): recorded consistently in
  `interface.md` and left to WP6 and Rolf. Not yours to solve; yours to
  keep consistent.
- **Hook test placement.** WP4 put the 100 g test in `order1.md` per plan
  §9 and §10, not §3.7 as its brief said. Fine if the pass band and the
  procedure match the plan.
- **WP9 counted seventeen §2 rows** where the briefs said sixteen; the plan
  wins. Diff the record's "Conflicts resolved" against plan §2 for drift.
- **WP2 fillets the plan cannot have.** The lane reports §3.5 step 2's
  4.0 mm tip round holds at most 1.60 mm next to the 1.5 medial fillet, and
  step 9's 2.0 mm hook joint fillet cannot sit on a Ø3.5 tube. Reproduce
  both claims in the script (try the lane's own alternatives: a tail
  section without the medial fillet; the joint fillet in the body frame
  before the rotate). If a construction order makes the plan's number
  work, that is a fix. If not, it is a plan change under "Needs a
  decision", and the manifest and `order1.md` must say what was printed.
- **CREASE_BOW default versus computed.** Default M1=52, M2=58 compute a bow
  of 11.00, clamped to 8, while the reference build uses CREASE_BOW=3.0 from
  `default.toml`. `measure.md`'s gate table (50.9 at bow 3, 51.3 at bow 1)
  and the manifest's clamped bow must describe the same build. Check the
  overlay rule (Rolf's file computes the bow only when CREASE_BOW is omitted)
  is written down in the README and `measure.md`, or Rolf's first
  measurement build silently changes the shape.
- **One lid file.** Only the full-body lid is exported; thin has LID_Y=6.0.
  Plan §3.6 lists one lid, so this is per plan, but `order1.md` must not
  promise a lid that closes the thin body.
- **Contact caps Ø4.7 × 1.35** (MOCK_CONTACTS) tie back to the dome seam
  above.
- **Coupon mapping** (open item 2) lives only in the script docstring and
  README. WP1 owns `interface.md`; add the mapping there as an interface v2
  note yourself (it is a documentation seam, not a CAD change).
- **WP2 report says 15 CAD files** (five parts × STEP, STL, 3MF) where plan
  §3.6 says five files, six parts. Check the naming in `manifest.json`,
  `order1.md` and `measure.md` agrees on what Rolf uploads (the STL or 3MF
  per part) and that the quantities table sums to six printed parts.
- **File names.** `order1.md` and `measure.md` name files under
  `docs/fab/cad/v1/`; they must match what WP2 actually wrote and what
  `manifest.json` lists.

## Attack points per package

- **WP2** (the only code): all four matrix variants build and anything
  outside the matrix fails before export; every check §3.3 and §3.6 name is
  present by name in the code and fails loudly with the parameter and the
  number; `MOCK_CONTACTS` behaviour; `WIRE_CHANNEL` opening reported per
  open item 4; `manifest.json` carries the parameter set, per-file SHA-256,
  check results, E1 to E5, interference values and the clamped
  `CREASE_BOW`; `docs/fab/cad/v1/` holds exactly the five files and six
  parts §3.6 names and nothing else large; `README.md` commands work from a
  clean venv; `tests/test_cad.py` asserts identical hashes and the failing
  cases fail; nothing in `src/elicio/` changed.
- **WP1**: every numeric row has a From cell that resolves; the RF zone
  comes from the module datasheet; each UNVERIFIED item names an owner;
  version header and change-log rule present; coordinates match plan §3.3.
- **WP4**: Rolf can do `measure.md` alone with a caliper and tape, one number
  per step; the gate table matches the script; `order1.md`'s "do not order
  if" list; DDP selected; allowances per line match plan §7 and mark
  UNVERIFIED where the plan does; `orders.md` is an empty template.
- **WP5**: every price has a URL and a date; every SKU's drawing numbers are
  the ones used in the stack; the DMG kit page exists; assembly order
  matches WP1's stack and the keep-outs; the internal-metal list covers
  every metal WP1 and WP2 place inside the shell; "nearest real option"
  claims are honest about what changes.
- **WP9**: no history removed; requirements 1 to 7 untouched; the new
  section states each plan §2 decision once; `AGENTS.md` changed only in the
  two lists; older "the owner" text untouched.

## Output

1. `tasks/reviews/code-r1.md`: a three-line verdict (MERGE /
   MERGE-AFTER-DECISION / REJECT), the gate results with commands, a table
   of defects (severity, file:line, what was wrong, what you changed, commit
   hash), and "Needs a decision". Commit it on `review/r1`.
2. `.reports/review-r1-report.md` in this worktree: what you merged, what
   you changed, the final commit sha.
3. Then, in order:

       herdr pane report-metadata "$HERDR_PANE_ID" --source lane --token lane=review-r1 --token done=1
       herdr notification show "review r1 done" --body "reviewer rev1" --sound done
       herdr agent prompt elicio "DONE review-r1 .reports/review-r1-report.md <final commit sha>" || herdr agent prompt elicio "DONE review-r1 .reports/review-r1-report.md <final commit sha>"

Your turn must end with that push, including if the verdict is REJECT.

## The worker reports, verbatim

### WP9 report (lane `w9`, branch `lane/w9`)

````md
# WP9 report — Design record update

Lane `w9`, branch `lane/w9`, worktree
`/home/user/projects/elicio/.worktrees/w9`. Interpreter: Python 3.13.15
in a worktree-local `.venv`. No optional-dependency group was added;
this package touched no code.

## What was built

`docs/EARPIECE_DESIGN.md` now carries a dated section, "Fabrication plan,
2026-09-16", in the record's voice. It records the decision (CAD in
build123d, JLCPCB MJF PA12-HP, three titanium M2.5 dome contacts, the
provisional gauge first, release states S0 to S4), each plan §2 decision
once with its reason, and pointers to `docs/fab/plan.md` as the Phase 1
contract and `tasks/plan/turns/` as the review record.

The "Fabrication without a 3D printer" section is kept. A superseded note
at its top says: outsourced printing survived (now JLCPCB); stainless
contacts became titanium, and Palmiga conductive TPU remains available
but is not chosen for Stage B; hand-shaped PCL was dropped.

Open question 3 now points at `docs/fab/L4-pod.md` (Raytac MDBT50Q-1MV2 /
nRF52840 and TI ADS1292) and `docs/fab/interface.md` (WP1 then WP6).
Open question 4 is answered by the plan's §3.3 and §4, with the WP7a
montage test still ahead.

`AGENTS.md` Key Directories gained `docs/fab/`. Important Files gained
`docs/fab/plan.md`. Nothing else in that file changed.

Requirements 1 to 7 and the Stage A circuit material were not edited.
The 2026-08-13 history was not removed. New prose uses "Rolf"; older
prose still uses "the owner".

`README.md` status table was left alone. "Sensor hardware | Not
purchased" and "Personal recording | Does not exist" remain true.

## Plan §9 acceptance

Row WP9: "record updated; each §2 decision appears once."

The plan's §2 table has **seventeen** rows, not sixteen as the WP9 brief
said. The plan wins. All seventeen appear once in "Conflicts resolved"
in `docs/EARPIECE_DESIGN.md` (battery, envelope, contact metal, contact
size, conductive TPU, lid closure, gauge material, montage, contact
count, suspension, ear capture, shipping, shells and PCB, hook, gasket,
charging, short ears).

Verified by reading that section after the edit. No command prints a
count; the rows are the check.

## Gates

### Unit tests

Command:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

Result: Ran 42 tests in 0.010s. OK. (Python 3.13.15, worktree `.venv`.)
No code was changed.

### WP9 acceptance row

See above. Each §2 decision appears once. The README status table was
not run as a gate; no row was wrong.

## What was not done

- `docs/fab/interface.md` is not on this branch. Open question 3 points
  at the path WP1 owns; it was not created here.
- Requirement 5 still names carbon-TPU or stainless steel. The
  fabrication section records titanium as the Stage B pick and does not
  rewrite the requirement.
- README was not edited.
- This lane did not run `git push`. A post-commit hook on this
  worktree pushed `lane/w9` to origin after each commit. The common
  file says never push. The hook, not this lane, contacted origin.

## Needs a decision

- Requirement 5 versus titanium. The plan's §2 row 3 and §10 item 9
  already say changing the nickel-free wording is Rolf's, outside the
  plan. The record now states both the old requirement and the new
  pick. Leave them until Rolf edits the requirement.
- The WP9 brief said "sixteen" §2 rows. The signed-off plan has
  seventeen (row 17, short ears). This lane recorded all seventeen.
  No further pick is needed unless a later brief wants row 17 omitted.

## Final commit sha

`fce354ecda32424e3562402393e98ff20f2743f8`

That commit is `docs(agents): index the fabrication plan in the agent
maps` on `lane/w9`. The design-record commit immediately under it is
`ddd7cd8`.
````

### WP1 report (lane `w1`, branch `lane/w1`)

````md
# WP1 report — Interface v1

Lane `w1`, branch `lane/w1`, worktree
`/home/user/projects/elicio/.worktrees/w1`. Package `WP1`.
Plan commit `0c5d0eb`. Interpreter: Python 3.13.15 (`.venv`).

## What was built

`docs/fab/interface.md` version 1. It is the mechanical contract
between the shell (WP2/WP8), the contact hardware (WP5), and the
Stage B board (WP6). Tables with units and a "From" column cover:

1. Contact coordinates in the body frame, hole, dome, and the stack
   above the floor (lug, nut, tip, Kapton) totalling 2.63 mm.
2. Keep-outs: KEEPOUT_SIGNAL, KEEPOUT_REF, RIB, walls, lid recess.
3. Lead route: WIRE_CHANNEL, lug tabs, LEAD_PADS candidates,
   CABLE_EXIT, and the rule that only insulated wire leaves the
   reference pocket.
4. 501015-class cell envelope, PCM fold, pocket, identity left to WP6.
5. Board outline, heights by zone, RF rules from the module datasheet,
   ADS1292 and charger placement rules.
6. Mechanical insulation and safety: Kapton, three separate paths, no
   charging port, cable exit plugged in Stage B.
7. Packing budget 105 mm² available vs 111 mm² required, and the four
   WP6 escalations with the area each one buys.
8. Version header and the change-log rule (bump, re-run WP2, repeat
   affected §3.7 items).

No product code was changed. No CAD was added. Optional extra
dependencies were not needed.

A `post-commit` hook pushed `lane/w1` to `origin`. This lane did not
run `git push`. The common file forbids a push; the hook did it.

## Plan §9 acceptance (WP1)

Acceptance: every dimension traced to a standard, a datasheet, or the
plan; versioned.

| Item | How verified | Command / result |
|---|---|---|
| Versioned | File header is version 1 with a change-log rule matching plan §9 | Read `docs/fab/interface.md`. Not a command. |
| Traced | Every numeric row has a From cell. Eight claims that cannot be closed from a public table are listed UNVERIFIED with an owner | Read the same file, sections 2–8 and 10. Not a command. |

Web pages used for standards and datasheets are listed in section 11
of the interface file, with URL and date 2026-09-16.

## Gates

### Unit tests

```
.venv/bin/python -m unittest discover -s tests -v
```

Result: 42 tests, OK, 0.010 s. Python 3.13.15. This lane touched no
code.

### Package acceptance

See the table above. Both items pass as a document check. There is no
second executable gate for WP1.

## What was not done

- WP2 CAD and §3.3 geometry checks (channel opening, pad-to-keep-out).
- WP5 SKU drawings (dome 4.7/1.35, lug 0.5 mm, stack inside Ø7.1).
- WP6 named cell, RF polygon from Spec L §2.3, final lead pads.
- No purchase, upload, or vendor contact.

## Needs a decision

None that block version 1. The plan already decides these; later
packages close them:

1. Brief named ISO 4032. Plan names DIN 439 / ISO 4035 (m = 1.6 mm).
   This file follows the plan. ISO 4032 M2.5 (m = 2.0 mm) does not
   fit the y 4.13 keep-out.
2. Dome Ø4.7 / crown 1.35 is the CAD contract. ISO 7380-1:2022 has no
   M2.5 row. Catalog M2.5 is 4.5 / 1.5. WP5 names the SKU; mismatch
   is interface v2.
3. Lug 0.5 mm is UNVERIFIED. Catalog #4/M2.5 lugs read 0.71–0.79 mm.
   WP5 must find a drawing ≤ 0.5 mm or bump the stack.
4. Packing shortfall ≈ 6 mm². Rolf chooses longer, wider, or a
   smaller front end after WP6 (plan Open for Rolf item 6).
5. Superior low-u board pad is 0.09 mm from KEEPOUT_SIGNAL 1. WP2
   checks it.

Design-record stainless contacts and L4 skin-side charge pads lose to
the plan. Recorded in interface section 9. Not silent CAD changes.

## Final commit sha

`a9be8874ce689aa0f380930ff82a51192a00fc2b`
(`docs(fab): add Stage B mechanical interface v1`)
````

### WP4 report (lane `w4`, branch `lane/w4`)

````md
# WP4 report

Lane `w4`, worktree `/home/user/projects/elicio/.worktrees/w4`, branch
`lane/w4`. Package WP4. Python 3.13.15 in `.venv`. No extra optional
dependency group. No code change.

Final commit: `fcd2b2a7fed769a29f57c9cd43bf29b833458f0a`

## What was built

Three phone sheets, all new:

- `docs/fab/measure.md` — M1 first, chord-gate formula and a two-line table
  for bow 1, 3 and 8, stop rule, then M2–M8 in plan §3.4 order (tool,
  landmark, picture in words, typical range, write-in box). Defaults line
  if only M1 is measured. Ear default right.
- `docs/fab/order1.md` — do-not-order list, five §3.6 STL names and
  quantities, JLC MJF / PA12-HP / natural grey / DDP, checkout gate with
  §7 allowances and the stop rule if a live price is outside them,
  UNVERIFIED lines to copy at checkout, 100 g hook test, then §3.7 wear
  and the thickness / preload / back-view boxes.
- `docs/fab/orders.md` — empty log template. No row filled.

Commits: `b808992`, `d5d8518`, `fcd2b2a`.

JLC pages read 2026-09-16 (no quote, no upload, no account):

- https://jlcpcb.com/3d-printing — process label MJF(Nylon)
- https://jlc3dp.com/help/article/pa12-hp-nylon — updated 2026-07-30;
  colour label Natural gray; price “from $1.00”
- https://jlcpcb.com/help/article/us-tariff-policy-faq — updated 2026-09-09;
  US individuals ship DDP. The extracted page did not show a 40 % plastics
  line.

## Plan §9 row WP4

Acceptance: no step needs a question. Gate: unit tests green.

| Item | Command | Result |
|---|---|---|
| Unit tests | `.venv/bin/python -m unittest discover -s tests -v` | `Ran 42 tests in 0.010s` / `OK` |
| M1-first sheet, checkout gate, empty order log, 100 g hook test | files exist on `lane/w4` | written; not a human trial |
| No step needs a question | review of the three sheets | each step is an instruction with one write-in; not run with Rolf |

Nothing in this package was claimed verified that was not run. The sheets
were not walked with a caliper or a JLC cart.

## What was not done

- No purchase, no JLC account, no upload, no quote request.
- CAD files under `docs/fab/cad/v1/` were not created (WP2 / WP3).
- M1–M8 were not measured. The hook test was not run (no printed part).
- `docs/fab/plan.md` was not edited.
- I did not run `git push`. A post-commit hook pushed `lane/w4` to origin
  after each commit.

## Needs a decision

1. Plan §3.3 writes the script check as `TOTAL_CHORD > M1 − 3`. That fails
   the default ear (47.9 > 49 is false). Plan §1, §2 row 17, §10 item 1,
   and turn 07 state the gate as M1 at least TOTAL_CHORD + 3 (50.9 mm at
   bow 3, 51.3 mm at bow 1). The sheets implement that §10 reading. WP2
   should not code the `>` as written.
2. Brief WP4 says the 100 g hook test sits in §3.7. Plan §3.7 does not
   list it. Plan §9 row WP4 and §10 interface item 3 do. Plan wins. The
   test is in `order1.md` after receipt, on `body_full_p15`. Force at
   1.5 mm preload is `0.98 N × 1.5 mm / drop`. 100 g = 0.98 N is standard
   gravity, not a plan number. Pass 0.5 N to 1.5 N. Outside that band, WP6
   decides HOOK_DIA.
3. The 40 % import collection stays UNVERIFIED. The tariff FAQ read
   2026-09-16 still does not give that plastics rate as a usable line.
   Rolf copies the live tariff line at checkout.
````

### WP5 report (lane `w5`, branch `lane/w5`)

````md
# WP5 Work Package Report: Contacts Kit

**Package:** WP5 — Contacts kit: verified sourcing and assembly  
**Lane:** w5  
**Worktree:** `/home/user/projects/elicio/.worktrees/w5`  
**Branch:** `lane/w5`  
**Date:** 2026-09-16  
**Final Commit SHA:** `a28df06ee149c13f56038584420c9c2823b8d98a`

---

## 1. What Was Built

Created `docs/fab/contacts.md` providing the complete, verified specification for the Stage B earpiece contacts kit:

1.  **Verified SKUs and Sourcing:**
    *   **Contact Screws:** Verified ISO 7380 M2.5 button-head screws in Grade 2 titanium (RJXHOBBY `RJX3995-M2.5X4mm`, $33.99/50pk) and Grade 5 titanium (Titane Services `vis-titane-ISO7380-G5-M2.5`, 3.57 €/ea; Sortafast `SF-M2.5-BH-TI`, $17.50/10pk). Confirmed McMaster-Carr and Bolt Depot do not stock M2.5 titanium screws.
    *   **Retaining Thin Nuts:** Verified DIN 439 / ISO 4035 M2.5 thin hex nuts (1.60 mm height, 5.0 mm AF). Documented that titanium thin nuts are not stocked off-the-shelf at retail; sourced nearest real compliant options (McMaster-Carr `90710A025` in 18-8 stainless steel, $2.50/50pk; Accu `HNU-M2-5-A2` in A2 stainless steel) per plan §4 internal allowance.
    *   **Ring Lugs:** Verified TE Connectivity AMP Budget Series Part `31428` (#4 / M2.5 stud, 22–26 AWG, $0.24/ea at DigiKey). Verified 100% pure matte tin finish over ETP copper (zero nickel underplate) and stock thickness of 0.018 in (0.46 mm).
    *   **Kapton Tape:** Verified Adafruit Product ID `3057` (10 mm × 33 m roll, $4.95) and Bertech pre-cut 1/4 in dots (`PPD-1/4`). Two layers provide 0.13 mm dielectric barrier.
    *   **DMG Spot Test Kit:** Verified Delasco Spot Test For Nickel (Product SKU `SPOT-TEST`, $17.99 USD in stock) as the active substitute for the unavailable Nickel Alert ($24.99).
2.  **Stack Arithmetic on Catalog Drawings:**
    *   Calculated exact component stacks against catalog drawings.
    *   Demonstrated that a 4.0 mm screw through a 1.50 mm PA12 medial wall with TE 31428 lug (0.46 mm), DIN 439 thin nut (1.60 mm), protruding tip (0.44 mm), and Kapton (0.13 mm) totals exactly **2.63 mm** above the cavity floor (top at $y = 4.13\text{ mm}$), leaving 0.17 mm nominal air clearance beneath the PCB datum at $y = 4.30\text{ mm}$.
3.  **Material-Evidence Route:**
    *   Defined documentation tiers (EN 10204 3.1 MTC, ASTM F67/F136 compliance declaration, supplier invoice/declaration, and 100% receipt DMG testing).
    *   Stated unequivocally that 316/316L stainless steel contains 10–14% nickel, is not nickel-free, and is not an acceptable fallback.
4.  **DMG Chemical Screening Protocol:**
    *   Specified 4-step protocol using Delasco `SPOT-TEST` (1% DMG, 10% ammonium hydroxide).
    *   Defined fail-closed rejection rule: any pink coloration ($\ge 10\text{ ppm}$ leaching nickel) rejects the entire delivery lot.
5.  **Assembly Sheet:**
    *   Detailed step-by-step assembly for Signal Contacts 1 and 2 (lug flat along floor per `KEEPOUT_SIGNAL`) and Reference Contact 3 (upright lug tab in tail pocket per `KEEPOUT_REF`, with insulated 28 AWG wire routed through `WIRE_CHANNEL`).
    *   Supplied torque specification: 0.20 to 0.25 N·m (firm hand-snug with 1.5 mm hex driver avoiding PA12 boss yield).
6.  **Internal-Metal Inventory:**
    *   Enumerated all 9 metallic items inside or traversing the shell boundary, their alloys/platings, containment boundaries, and confirmed zero skin contact in any single-point mechanical failure.

---

## 2. Acceptance Verification (Plan §9 Row WP5 and Common Gates)

### Gate 1: Test Suite
*   **Command:** `.venv/bin/python -m unittest discover -s tests -v`
*   **Result:** Ran 42 tests in 0.012s. Result: **OK (green)**.

### Gate 2: Acceptance Item 1 — Every price has a page and date
*   **Verification:**
    *   RJXHOBBY `RJX3995-M2.5X4mm`: $33.99 USD per 50pk, URL `https://www.rjxhobby.com/`, date read 2026-09-16.
    *   Titane Services `vis-titane-ISO7380-G5-M2.5`: 3.57 € each, URL `https://www.titane-services.eu/vis-titane-ISO7380-G5-M2.5`, date read 2026-09-16.
    *   Sortafast `SF-M2.5-BH-TI`: $17.50 USD per 10pk, URL `https://sortafast.com`, date read 2026-09-16.
    *   McMaster-Carr `90710A025` (DIN 439 thin nut): $2.50 USD per 50pk, URL `https://www.mcmaster.com/90710A025/`, date read 2026-09-16.
    *   Accu `HNU-M2-5-A2` (DIN 439 thin nut): £0.38 to £0.91 GBP each, URL `https://www.accu.co.uk/thin-nuts/36829-HNU-M2-5-A2`, date read 2026-09-16.
    *   TE Connectivity `31428` (ring terminal): $0.24 USD each ($2.08/10pk), URL `https://www.digikey.com/en/products/detail/te-connectivity-amp-connectors/31428/292150`, date read 2026-09-16.
    *   Adafruit `3057` (Kapton tape): $4.95 USD per roll, URL `https://www.adafruit.com/product/3057`, date read 2026-09-16.
    *   Delasco `SPOT-TEST` (nickel spot test kit): $17.99 USD each, URL `https://www.delasco.com/spot-test-for-nickel/`, date read 2026-09-16.
*   **Result:** **PASS**. Every price is accompanied by its source URL and date.

### Gate 2: Acceptance Item 2 — Stack is at most 2.63 mm on catalog drawings
*   **Verification:**
    *   Nominal Fastened Grip: Wall ($1.50\text{ mm}$) + Lug ($0.46\text{ mm}$) = $1.96\text{ mm}$.
    *   Nut: DIN 439 thin nut ($1.60\text{ mm}$).
    *   Screw: ISO 7380 M2.5 × 4.0 mm ($L = 4.00\text{ mm}$).
    *   Tip Protrusion Above Nut: $4.00 - (1.50 + 0.46 + 1.60) = 0.44\text{ mm}$.
    *   Internal Stack Height Above Floor: $0.46\text{ mm (lug)} + 1.60\text{ mm (nut)} + 0.44\text{ mm (tip)} = 2.50\text{ mm}$.
    *   Kapton Disc: $0.13\text{ mm}$ (two layers 2.5 mil tape).
    *   Total Stack: $2.50\text{ mm} + 0.13\text{ mm} = \mathbf{2.63\text{ mm}}$.
*   **Result:** **PASS**. Exactly satisfies the $2.63\text{ mm}$ upper bound.

---

## 3. What Was Not Done

1.  **No Purchasing or Vendor Contact:** Per `tasks/phase1-common.md` rules and `docs/CLAUDE_SCIENCE_HANDOFF.md`, no purchase orders were placed, quotes requested, carts filled, or vendors contacted.
2.  **No Direct Material Testing:** Physical DMG testing and XRF spectroscopy remain to be conducted upon part receipt at Stage S1/S2 per plan §9.

---

## 4. Needs a Decision

1.  **Internal Retaining Nut Material Selection (Order 2):**
    *   *Option A (Recommended per Plan §4):* Use off-the-shelf 18-8 stainless steel DIN 439 thin nuts (McMaster-Carr `90710A025`, $2.50 for pack of 50). They reside inside the sealed cavity under Kapton and cannot contact skin.
    *   *Option B:* Request a bespoke quotation from Fastenright for Grade 2 / Grade 5 titanium DIN 439 thin nuts if 100% titanium BOM is required inside the cavity.
    *   *Option C:* Use off-the-shelf DIN 934 titanium full-height nuts (2.0 mm height). Stack height is verified compliant ($2.50\text{ mm} + 0.13\text{ mm} = 2.63\text{ mm}$, with flush tip).
2.  **Screw Length at Purchase:**
    *   If 4.0 mm titanium screws are temporarily backordered and 6.0 mm screws are purchased (e.g. from Sortafast), the assembly sheet mandates grinding down screw shanks by 2.0 mm prior to insertion to prevent interference with the PCB.

---

## 5. Final Commit SHA

*   `a28df06ee149c13f56038584420c9c2823b8d98a`
````

### WP2 report (lane `w2`, branch `lane/w2`)

````md
# WP2 report — gauge script and order 1 files

Lane `w2`. Branch `lane/w2`. Final commit `47749e19619a9063a5a226b4b4edf6415e64f26b`.
Python 3.13.15 with build123d 0.11.1. No 3.12 fallback was needed.

## What was built

- `scripts/cad/bte_fit_shell.py` — build123d generator for the §3 fit gauge.
- `scripts/cad/params/default.toml` — reference-ear defaults.
- `scripts/cad/params/rolf.toml` — measurement overlay (empty keys take defaults and mark REF).
- `scripts/cad/README.md` — install, reference build, measurement build, checks.
- `cad` optional-dependency group in `pyproject.toml` (`build123d>=0.7`, `trimesh>=4`).
- `docs/fab/cad/v1/` — five files, each STEP + STL + 3MF: `body_full_p15`, `body_thin_p15`, `body_full_p25`, `lid`, `coupon`.
- `docs/fab/cad/v1/manifest.json` — parameters, clamped CREASE_BOW, chord gate, WIRE_CHANNEL openings, E1–E5, §3.6 fits, interference, SHA-256, quantities.
- `tests/test_cad.py` — math, matrix/M1 failures, identical regeneration.

The path `P(u,s,y)` uses the signed-off formula from turn 06. CREASE_BOW from M1/M2 is clamped 1–8 (open item 1). The chord gate is M1 ≥ TOTAL_CHORD + 3. MOCK_CONTACTS is true: gauge bodies carry Ø4.7 × 1.35 caps on −Y and do not cut holes, pocket, or channel.

A post-commit hook pushed `lane/w2` to origin. The lane brief said never push. The hook did it. This lane did not run `git push`.

## Plan §9 acceptance (WP2)

| Item | How | Result |
|---|---|---|
| All §3.3 checks | `.venv/bin/python scripts/cad/bte_fit_shell.py --checks-only` and the `checks` array in `manifest.json` (60 entries) | All passed. Matrix, walls, E1–E5 minima, M1 gate 50.9005 mm, hook inner radius, WIRE_CHANNEL openings at bows 1/3/8, one solid per part, seated lid/body overlap 0 mm³, STL watertight after vertex merge, contact caps on −Y. |
| Exceptions and interference in the manifest | Read `docs/fab/cad/v1/manifest.json` | E1–E5 present. `lid_body_overlap_mm3` = 0.0. Fit table from §3.6 present. SPAN = 10.35 vs M3 = 11. Pinna displacement = 0. |
| Identical regeneration | Export to `docs/fab/cad/v1` then to a temp dir; `tests.test_cad.CadRegenTests.test_reference_regen_matches_committed_hashes` | All 15 CAD files matched SHA-256. STEP timestamp pinned. 3MF UUIDs rewritten after Lib3MF write. |

## Gates

| Gate | Command | Result |
|---|---|---|
| Unit tests | `.venv/bin/python -m unittest discover -s tests -v` | 53 tests OK, including 11 CAD tests. |
| Script twice | `.venv/bin/python scripts/cad/bte_fit_shell.py --out docs/fab/cad/v1/` then `--out /tmp/elicio-cad-regen3` | 15/15 hashes identical. |

Failing cases (parameter and number in the message):

- `VARIANT=medium` → `CHECK FAIL: VARIANT=medium: must be full or thin`
- `HOOK_PRELOAD=3` → `CHECK FAIL: matrix: ... HOOK_PRELOAD=3.0`
- `M1=40` → `CHECK FAIL: M1_gate: ... (M1=40.0, TOTAL_CHORD=47.9005, gate=50.9005)`

## What was not done

- Renders and `drawing.pdf` — WP3 owns those.
- No order, upload, quote, or vendor contact.
- Stage B holes, reference pocket, WIRE_CHANNEL cut, and CABLE_EXIT — MOCK_CONTACTS is true for order 1. The script can cut them when MOCK_CONTACTS is false. Stage B keep-out and Ø1.3 wire-envelope containment were not run on solids.
- `body_thin_p25` — allowed by the matrix, not in the §3.6 order-1 file list.
- Coupon-to-parameter mapping was not written into `docs/fab/interface.md` (WP1 owns that file). The mapping is in the script docstring and README.

## Needs a decision

1. **Tip round 4.0 (§3.5 step 2).** The two vertical tip edges take at most 1.60 mm on the full bodies (medial fillet 1.5 already occupies the same corner). Thin: no valid tip fillet. Closest geometry: lofted tail to width 10, fillet 1.60 where it holds. Reading: 4.0 mm needs a tail section without the medial fillet, or a plan-view cap built as its own solid.

2. **Hook joint fillet 2.0 (§3.5 step 9).** HOOK_DIA/2 is 1.75 mm, so a 2.0 mm fillet cannot sit on the tube. No stable intersection-loop edges were found. Closest geometry: hook union with the rotated body, no joint fillet. Reading: drop the radius below 1.75 mm, or fillet in the body frame before rotate.

3. **§3.3 gate wording.** The table says `TOTAL_CHORD > M1 − 3`. The signed-off rule is M1 ≥ TOTAL_CHORD + 3 (50.9 at bow 3, 51.3 at bow 1). This lane implemented the latter. Confirm that reading.

4. **Default CREASE_BOW vs M1/M2.** Default M1=52 and M2=58 give a computed bow of 11.00, clamped to 8. The reference build keeps CREASE_BOW=3.0 from `default.toml`. Rolf's file computes bow only when CREASE_BOW is omitted. Confirm that split.

5. **One lid file.** Exported lid is VARIANT=full, HOOK_PRELOAD=1.5. Thin has LID_Y=6.0. Order 1 quantities are lid ×2 for the full-body closure test. Confirm thin does not need its own lid file.

6. **Open item 2 (coupon mapping).** Holes Ø1.7 / 2.9 / 3.4; slots 0.9 and 0.4; rib 0.4. CONTACT_HOLE is 2.9. Slot 0.9 is TONGUE_SLOT height. E4 is the 0.4 rib. WP1/WP6 should copy this into the interface v2 note.

7. **Open item 4.** Physical opening at u=9.3 is 0.938 mm at bow 3, 1.089 at bow 1, 0.537 at bow 8. All positive. End section at s=40.5 is inside the pocket (distance 2.84 mm < 3.75). Stage B containment of the Ø1.3 wire envelope is still due when MOCK_CONTACTS is false.

## Final commit

`47749e19619a9063a5a226b4b4edf6415e64f26b`
````

