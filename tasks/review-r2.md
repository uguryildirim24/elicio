# Code review + fix — Phase 1 round 2 (WP3, WP6, WP7a part 1) on branch review/r2 (Claude Opus 5, high)

You are the reviewer for this round, herdr agent `rev2`. Three lanes
finished their packages. You merge them into one candidate, inspect it,
**fix what is wrong yourself**, run every gate, and write one verdict. You
never push by hand, never merge into `main`, never touch another worktree,
never edit `docs/fab/plan.md` or `docs/fab/open-questions.md`.

Worktree `/home/user/projects/elicio/.worktrees/review`, branch
`review/r2` from `main`. Private environment inside this worktree:
`python3.13 -m venv .venv && .venv/bin/python -m pip install -e '.[cad]'`
(build123d 0.11.1, trimesh, matplotlib, pypdf all have 3.13 wheels; the
lanes used matplotlib 3.11.2 and pypdf 6.19.0).

## Steps

1. Read `tasks/phase1-common.md`, `docs/fab/open-questions.md`, the three
   briefs `tasks/WP3-renders.md`, `tasks/WP6-packing.md`,
   `tasks/WP7a-protocol.md`, the round 1 verdict `tasks/reviews/code-r1.md`
   (so you do not undo its fixes), and `docs/fab/plan.md` §3.3, §3.5, §3.6,
   §4, §5, §6, §9, §10.
2. Merge, in this order, resolving conflicts yourself: `lane/w5`, `lane/w2`,
   `lane/w1`. Each lane's diff against `main` shows `HANDOFF.md` and
   `HANDOFF.json` as deleted only because `main` gained them after the lanes
   branched; keep them.
3. Gates, all on the merged tree:
   - `.venv/bin/python -m unittest discover -s tests -v` passes with the CAD
     tests running, not skipped.
   - Reference build twice into two temp dirs: all fifteen solids identical
     to each other and to `docs/fab/cad/v1/`; the twelve non-lid hashes
     equal the ones in `main`'s manifest; the three lid hashes changed only
     in the font commit `66b5564`.
   - `scripts/cad/render.py` twice: PNGs and PDF byte-identical and equal to
     the committed ones.
   - `scripts/cad/manifest.py --check-bytes docs/fab/cad/v1/manifest.json`
     passes; a manifest with one key removed fails.
   - WP6's placement drawing regenerates byte-identical.
   - `git diff main -- src/ docs/fab/plan.md docs/fab/open-questions.md` is
     empty.
4. Adversarial review: the seams below first, then the attack points per
   package. Look at the images yourself (Read the PNGs; for the PDF, add a
   debug PNG export of the drawing page to `render.py` if there is no other
   way to see it, and keep it if it is useful). Rolf approves order 1 from
   these pictures; a picture that misleads him is a High defect.
5. Fix every defect yourself, in separate commits on `review/r2` with
   messages starting `review(WPn):`. The repo's post-commit hook pushes on
   commit; do not run `git push` yourself.
6. What cannot be fixed without changing the plan goes under "Needs a
   decision" with your reading, numbered on from the round 1 verdict's
   twelve (start at 13).

## Seams, from the reports and the coordinator's own look at the renders

## Seams noted from WP7a's report (lane w5, e0ea395)
- Every criterion cites a quoted passage: verify each quote exists verbatim in L3, the design record, the science handoff or policy.py (baseline ≤ 5 µV RMS "L3 §3.1"; flex ≥ 45 µV pk-pk "L3 §1 r2"; clench ≥ 150 µV and SNR ≥ 10:1 "L3 §2.3"; SNR ≥ 3:1 "DESIGN r60"; 9/10 on three days "Stage B exit criteria"; talking and walking 0 events/min "DESIGN FP budget").
- "HANDOFF M1" cited as a source: HANDOFF.md is not on lane/w5; find what it means or strike it.
- Tolerance window s1 ∈ [20.0, 24.0] mm for the coordinate freeze: not in the plan; source or PROPOSED tag.
- "L3's horizontal PAM pair requires u ≥ 21 mm, exceeding shell width": check the arithmetic against L3 and BODY_WIDTH 17.
- Bench chain (INA128 G=10, HPF 19.4 Hz, TL072 G 11–101, Sallen-Key 490 Hz, ADS1115 860 SPS, ESP32 UART 115200) must match the design record's Stage A section number for number.
- Bench acceptance rule "≥ 70 % amplitude of the horizontal ceiling" is a new number: source or PROPOSED.
- Two PROPOSED items (DC shift ≤ ±50 mV, eating ≤ 0.20 events/min): rationale present; reviewer checks they are tagged in the file, not only in the report.
- LaTeX `$...$` in a Markdown Rolf reads on GitHub and Obsidian: acceptable if it renders in both; plain text preferred where a unit suffices.
- Tests: 67 OK with 4 skipped (CAD tests skip in w5's venv); the r2 reviewer runs them with build123d installed.

## Seams noted from WP3's report (lane w2, a325a63; font commit 66b5564)
- `drawing.pdf` is 3.7 MB for one page: vector STL triangulations embedded. Check it opens quickly on a phone; rasterize the shaded views inside the PDF if not, keeping the tables and section vectors. Any change must stay byte-identical on regeneration.
- `commit` in the manifest is now "last commit that changed a hashed solid", `views_commit` copies it; check `tests/test_cad.py` and `manifest.py` agree, and that a regeneration on a later HEAD does not fail on it.
- Lid solids changed in the font commit only (Liberation Sans, OFL). Confirm the other twelve solid hashes equal main's manifest; confirm the OFL file and the font path are what `bte_fit_shell.py` loads (no fallback to a system font when the file is missing: it must fail).
- Starburst tessellation around the mock caps in the STL: the lane left the solid. Reviewer decides whether a tighter STL export tolerance (deterministic, all fifteen files regenerated, one commit) is worth it before Rolf sees the renders; otherwise the drawing must say the pattern is tessellation, not geometry.
- PNG and PDF metadata pinned to 2026-09-16; matplotlib 3.11.2 and pypdf 6.19.0 unpinned in `pyproject.toml` (`matplotlib>=3.8`, `pypdf>=5`): hashes may drift with a different matplotlib. State the tested versions in the README and manifest, or pin.
- File names: `measure.md` and `order1.md` name `render_medial.png`, `render_lateral.png`, `drawing.pdf`; confirm they match and that `order1.md`'s checkout reads the new manifest keys without breaking.
- 70 tests OK in w2's venv (build123d present).
- Coordinator looked at both PNGs. (a) The medial view is orthographic and head-on, so the full 9.0 and thin 7.0 bodies look identical; thickness is depth in that view. The brief asked that Rolf sees the difference: add an edge-on strip (superior or posterior view of both bodies at the same scale) or a three-quarter view. (b) The starburst triangles around each cap dominate the medial face. Render from a finer tessellation of the STEP (render-only, shipped STL untouched) or tighten the STL export for all fifteen files in one deterministic commit; either way Rolf must not be approving a picture of tessellation. (c) In the lateral view a rectangular tab of the lid sticks out past the body outline at the hook end, roughly 5 × 1.5 mm at the scale bar, and a smaller one at the tail end. Check against plan §3.5 step 7 and the §3.6 pairs (web, tongue, lip): a lid feature outside the body outline is a defect unless the plan puts it there. (d) The commit label in the corner is the font commit, fine; the images carry no date.

## Seams from WP6's report (lane w1)

- **Four files edited by both w2 and w1**: `scripts/cad/bte_fit_shell.py`,
  `tests/test_cad.py`, `scripts/cad/README.md`, `pyproject.toml`. Expect
  conflicts; keep both lanes' additions (WP3: font path, `views`, the
  `commit` definition, validator hook; WP6: coupon-mapping docstring,
  `placement.svg` allowed next to the gauge files). One matplotlib
  constraint (`>=3.9` satisfies both), plus `pypdf`.
- **`.reports/WP6-report.md` is tracked on `lane/w1`** although `.reports/`
  is ignored. `git rm --cached` it in the merge; the file stays on disk.
- **SIG1 pad moved from (5.9, 26.5) to (5.9, 26.6).** Plan §3.3 lists 26.5.
  Check the round 1 `keepout_clearances` check in `bte_fit_shell.py` and
  `manifest.json` use the same pad the interface freezes; if the script
  still says 26.5 they disagree. If the 0.1 mm was needed for the 0.5
  margin, that is a plan erratum for "Needs a decision"; if not, revert it.
- **ADS1292 in VQFN-32 (RSM) and one BAV199S-Q array** replace TQFP-32 and
  three SOT-23 clamps. Verify on the TI datasheet that the RSM package
  exists for the ADS1292 (not only the ADS1292R) and its courtyard; verify
  the diode array part exists and that plan §6 and release state S2 ("three
  separately protected paths") still hold with one package: three
  independent pairs, no shared pin between contact paths.
- **Cell: no published folded pack fits `5.2 × 10.4 × 15.6`.** Plan §5
  already prescribes "PCM folded on the lateral face under Kapton", a hand
  step, not a purchased configuration. Check interface §5 states the fold's
  thickness against the pocket depth 6.0 (cell 5.0 to 5.2 plus PCM) and
  whether decision 1's 18.4 mm pocket is needed at all; if the pocket grows
  2.4 mm, the body and the M1 gate grow with it, and the interface must
  say so.
- **RF zone to battery: 5.00 mm with the cell packed to the hook end, 4.60
  on the rib.** Plan §5 wants ≥ 5 mm, so the cell position becomes a rule
  (where the foam goes); check the interface writes it as one.
- **`placement.svg`** (5,396 lines) is referenced from `interface.md`, opens
  in a browser, and carries a scale, the frame axes and a commit label.
  Decide with WP3's schema whether it joins the manifest `views` map (it is
  a view of the design, not a solid); keep the schema consistent either way.
- 76 tests OK in w1's venv with the CAD regen test passing.

## Attack points per package

- **WP3**: `render.py` runs from a clean venv by the README command; the
  drawing's dimensions come from the §3.3 constants, not pixels, and match
  `manifest.json`; the M1–M8 table marks M6 and M7 as recorded, not CAD
  drivers; E1–E5 nominal and fitted minimum equal §3.6; the title block
  carries VARIANT, HOOK_PRELOAD, CREASE_BOW, TOTAL_CHORD, the chord gate,
  commit and date; the closure section shows the fillets round 1 made real
  (Q3, Q4 values per body); the font commit is the only change to lid
  solids; `manifest.py`'s schema lists every key the manifest has and the
  validator is used by the tests; `pyproject.toml` versions.
- **WP6**: every new number has a From cell with page and date; the cell
  SKU's folded maximum fits `5.2 × 10.4 × 15.6` or the escalation is stated
  in §10's terms; the RF zone is the Raytac drawing's, at the inferior board
  edge, 5 mm from the battery; the packing sum uses courtyards, not body
  sizes; the flat-board sagitta is computed and the pad heights or chord
  placement keep the underside above KEEPOUT_SIGNAL top 4.13 everywhere
  (`interface.md` §6.1 gaps 0.152/0.110/0.263 at bows 3/1/8 came from the
  pads only); the lead pads clear keep-outs plus 0.5 and the antenna zone;
  the reference route is drawn at Ø1.3 with the 3 mm bend radius; the
  version header bumped to 2 with a change-log row; Q6 status and Q11 lid
  underside constraint present; interface §12 V2 items resolved or carried
  by name; nothing in CAD or the manifest changed.
- **WP7a**: every quoted passage exists verbatim where the file says
  (`docs/fab/L3-contacts.md`, `docs/EARPIECE_DESIGN.md`,
  `docs/CLAUDE_SCIENCE_HANDOFF.md`, `src/elicio/harness/policy.py`); every
  number without a quote is tagged PROPOSED in the file itself; the Stage A
  chain matches the design record's "Stage A circuit design" section number
  for number; the Results section has headings only; the session rules match
  plan §6 and §9 (S3 ≤ 4 h/day, only prescribed sessions); the coordinates
  section outputs exactly what S1 needs; no purchase, no results, no plan or
  design-record edits.

## Output

1. `tasks/reviews/code-r2.md`: a three-line verdict (MERGE /
   MERGE-AFTER-DECISION / REJECT), the gate results with commands, a table
   of defects (severity, file:line, what was wrong, what you changed, commit
   hash), and "Needs a decision" numbered from 13. Commit it on `review/r2`.
2. `.reports/review-r2-report.md` in this worktree: what you merged, what
   you changed, the final commit sha.
3. Then, in order:

       herdr pane report-metadata "$HERDR_PANE_ID" --source lane --token lane=review-r2 --token done=1
       herdr notification show "review r2 done" --body "reviewer rev2" --sound done
       herdr agent prompt elicio "DONE review-r2 .reports/review-r2-report.md <final commit sha>" || herdr agent prompt elicio "DONE review-r2 .reports/review-r2-report.md <final commit sha>"

Your turn must end with that push, including if the verdict is REJECT.

## The worker reports, verbatim

### WP7a report (lane `w5`, branch `lane/w5`)

````md
# WP7a Work Package Report: Montage Bench Procedure & Frozen Test Protocol (Part 1)

**Package:** WP7a — Montage bench procedure and frozen dry-test protocol (Part 1)  
**Lane:** w5  
**Worktree:** `/home/user/projects/elicio/.worktrees/w5`  
**Branch:** `lane/w5`  
**Date:** 2026-09-17  
**Final Commit SHA:** `e0ea395c50756d5300dce85e38470f875622f4d6`

---

## 1. What Was Built

Created `docs/fab/montage.md` satisfying all requirements of `tasks/WP7a-protocol.md` and `tasks/phase1-common.md`:

1.  **Status Line:**
    *   Formally declared protocol frozen on 2026-09-17 before the acquisition of any dry-electrode data.
    *   Confirmed zero empirical bench or dry-contact experimental data exists in the repository.
    *   Gated Part 2 execution on Stage A hardware acquisition.
2.  **Montage Bench Procedure:**
    *   **Landmarks & Skin Marking:** Defined retroauricular crease arc $s$ from hook root ($s = 0$), ear root length $M_1$, crease arc length $M_2$, mid-concha level $M_7$ ($s = 22.0\text{ mm}$), and mastoid offset $M_6$ ($s = 43.0\text{ mm}$).
    *   **Contact Skin Coordinates:** Derived Contact 1 $(u=5.9,\, s=22.0)$, Contact 2 $(u=10.4,\, s=33.1)$, and Reference $(u=8.5,\, s=43.0)$ with verified center-to-center pitch of 12.0 mm at 22° inclination.
    *   **Montage Comparison:** Compared the Plan's 22° angled pair (fits within 17 mm BTE shell cavity span) against L3's strictly horizontal PAM pair (requires $u \ge 21\text{ mm}$, exceeding shell width). Prescribed bench acceptance rule ($\ge 70\%$ amplitude of horizontal ceiling).
    *   **Stage A Bench Hardware Settings:** Specified analog front-end chain (INA128 $G=10$, passive RC HPF $f_c = 19.4\text{ Hz}$, TL072 non-inverting gain $G = 11\text{ to } 101$, Sallen-Key LPF $f_c = 490\text{ Hz}$, ADS1115 16-bit ADC at 860 SPS, ESP32 streaming ASCII integer counts over USB UART at 115200 baud).
    *   **Per-Trial Recording:** Mandated pre/post impedance check, permanent JSON session capture via `.venv/bin/elicio capture`, and amplitude logging across rest, deliberate flexes, clenches, and dynamic disturbances.
    *   **Coordinate Derivation for S1 Entry:** Documented nominal coordinate freeze for CAD release and tolerance window ($s_1 \in [20.0,\, 24.0\text{ mm}]$).
3.  **Frozen Dry-Test Protocol and Criteria (All Quantitative & Numeric):**
    *   Baseline resting noise floor $\le 5.0\text{ }\mu\text{V RMS}$ (Quoted: L3 §3.1).
    *   Voluntary auricular flex amplitude $\ge 45.0\text{ }\mu\text{V pk-pk}$ (Quoted: L3 §1 r2).
    *   Voluntary auricular flex SNR $\ge 3.0:1$ (9.54 dB) (Quoted: DESIGN r60).
    *   Voluntary teeth clench amplitude $\ge 150.0\text{ }\mu\text{V pk-pk}$ (Quoted: L3 §2.3).
    *   Voluntary teeth clench SNR $\ge 10.0:1$ (20.0 dB) (Quoted: L3 §2.3).
    *   Clench-to-flex amplitude ratio $\ge 3.0:1$ (Quoted: DESIGN §2 r9).
    *   Zero dropouts under jaw motion across 10 cycles (Quoted: DESIGN Stage B exit criteria); maximum input DC shift $\le \pm 50.0\text{ mV}$ (`PROPOSED`).
    *   Three-day re-donning stability: $\ge 9/10$ deliberate contractions detected on each of 3 separate days at fixed threshold (Quoted: DESIGN Stage B exit criteria, HANDOFF M1).
    *   False-positive rate for eating: $\le 0.20\text{ events/min}$ (`PROPOSED`).
    *   False-positive rate for talking: $0.0\text{ events/min}$ (Quoted: DESIGN FP budget).
    *   False-positive rate for walking: $0.0\text{ events/min}$ (Quoted: DESIGN FP budget).
    *   Cross-talk rejection for yawning: 0 unconfirmed actions executed (Quoted: DESIGN FP budget, `policy.py`).
    *   Cross-talk rejection for facial mimicry: $\le 1/5$ reps for NONE, 0 for REVERSIBLE/DANGEROUS (Quoted: L3 §2.3, DESIGN FP budget).
4.  **Operational Safety and Session Rules:**
    *   Wear duration limits per release state: S0 passive progression, S1 order gate (zero wear), S2 bench electrical/chemical screen (zero skin wear), S3 validation wear $\le 4.0\text{ h/day}$, S4 routine use.
    *   Skin inspection pre/post wear and stop rule: halt immediately on pain, numbness, or erythema persisting $> 15.0\text{ min}$ (Quoted: plan §3.7 item 3).
    *   Hygiene: 70% isopropanol wipe after every wear session; solvent prohibition (Quoted: plan §6).
    *   Electrical safety interlocks: isolated DC battery power only, never charge while worn, host laptop on battery during serial debug, lead series protection $220\text{ k}\Omega$ (Quoted: plan §6).
5.  **Results Section:**
    *   Headings only (5.1 to 5.10); binding rule stating empirical data waits for Part 2 and criterion relaxation voids S1 gate.
6.  **Inputs to Other Packages:**
    *   To WP7b: test protocol for validation wear.
    *   To WP8: confirmed contact body-frame coordinates.
    *   To WP6: board packing and lead pad alignment confirmation.

---

## 2. Acceptance Verification (Plan §9 Row WP7a and Common Gates)

### Gate 1: Test Suite
*   **Command:** `.venv/bin/python -m unittest discover -s tests -v`
*   **Result:** Ran 67 tests in 0.027s. Result: **OK (skipped=4)**. 0 failures.

### Gate 2: Clean Git Working Tree
*   **Command:** `git status --short`
*   **Result:** Clean. Untracked file `.reports/WP7a-report.md` is gitignored.

### Gate 3: Protocol Frozen Before Dry Data
*   **Verification:** Section 1 explicitly declares criteria frozen on 2026-09-17 before dry data. Zero empirical data exists in the repository. Section 5 contains headings only and mandates that changing criteria after seeing data voids S1 entry.
*   **Result:** **PASS**.

### Gate 4: Numeric Criteria Completeness & Traceability
*   **Verification:** Every single test parameter in Section 3 has an explicit numeric threshold. Every threshold cites a quoted passage from existing documentation (`docs/fab/L3-contacts.md`, `docs/EARPIECE_DESIGN.md`, `docs/CLAUDE_SCIENCE_HANDOFF.md`, or `src/elicio/harness/policy.py`) or is tagged `PROPOSED:` with engineering rationale and what source would settle it.
*   **Result:** **PASS**.

---

## 3. What Was Not Done

1.  **Stage A Hardware Acquisition & Bench Measurement:** Per the WP7a brief, bench measurements constitute Part 2 and are blocked on hardware procurement by Rolf (`docs/STAGE_A_PARTS.md`). Part 1 delivers the frozen protocol and procedure.
2.  **No Hardware Purchasing or Quotes:** Per `tasks/phase1-common.md`, no purchase orders were placed, carts filled, or vendors contacted.
3.  **No Modification of Baseline Specifications:** `docs/fab/plan.md` and `docs/EARPIECE_DESIGN.md` remain untouched per task instructions.

---

## 4. Needs a Decision

1.  **Confirmation of Proposed Bounds:**
    *   `PROPOSED:` Maximum input DC shift during jaw motion bounded at $\le \pm 50.0\text{ mV}$. (Keeps INA128 input within linear common-mode operating range at $G=10$ on $\pm 9\text{ V}$ rails).
    *   `PROPOSED:` Eating false-positive rate bounded at $\le 0.20\text{ events/min}$ (allows at most 3 benign `RiskLevel.NONE` marker triggers during a 15-minute meal).
2.  **Part 2 Trigger:**
    *   Part 2 bench testing will run when Rolf acquires the Stage A parts cataloged in `docs/STAGE_A_PARTS.md`.

---

## 5. Final Commit SHA

*   `e0ea395c50756d5300dce85e38470f875622f4d6`
````

### WP3 report (lane `w2`, branch `lane/w2`)

````md
# WP3 report — renders, drawing, manifest schema

Lane `w2`. Branch `lane/w2`. Font commit `66b5564151991f4fd5f6a6457f798839d349b1d9`. Final commit `a325a635f790d73875d2045ae475189f2708cfd4`.
Python 3.13.15, build123d 0.11.1, matplotlib 3.11.2, pypdf 6.19.0, trimesh 5.x.

## What was built

- `scripts/cad/fonts/LiberationSans-Regular.ttf` and `OFL.txt` (SIL OFL 1.1, Liberation Fonts 2.1.5). Lid emboss uses that file, not Arial. Own commit `66b5564`.
- `scripts/cad/render.py` — headless medial and lateral PNG, one-page `drawing.pdf`.
- `scripts/cad/manifest.py` — schema 1 validator. Fails on a missing key.
- `docs/fab/cad/v1/render_medial.png`, `render_lateral.png`, `drawing.pdf`.
- `views` map on `manifest.json` with SHA-256. The fifteen solid hashes in `files` are unchanged since the font commit (twelve body/coupon files unchanged since main; three lid files changed only in `66b5564`).
- `commit` is the last git commit that changed a hashed solid under `docs/fab/cad/v1` (`*.step`, `*.stl`, `*.3mf`). It is not HEAD. Artwork does not move it. `views_commit` copies that same value.
- Tests and README commands. `cad` extra now also has `matplotlib>=3.8` and `pypdf>=5`.

Renderer: matplotlib Agg, orthographic shaded STL triangulation (no GUI, no GPU). PDF: matplotlib figure, then pypdf to pin CreationDate, ModDate, Producer, and `/ID` to 2026-09-16. PNG `tIME`/`tEXt` dates are rewritten the same way. Chosen because this lane is headless and the hashes must match on a second run.

## Plan §9 acceptance (WP3)

| Item | How | Result |
|---|---|---|
| Two renders, one page | files in `docs/fab/cad/v1/` | `render_medial.png`, `render_lateral.png`, `drawing.pdf` |
| Medial and lateral faces | PNGs | Medial: full p15 with caps, tail, hook, thin p15 beside it. Lateral: lid seated, hook. Scale bar 10 mm, labels, commit `66b5564`. |
| Closure section | drawing.pdf three zooms | lip/bump/groove (E5), nubs (E3), web/tongue/slot (E1). Sizes from §3.3 constants, not pixels. |
| M1–M8 | drawing table and leaders | All eight named with §3.3 values. M6 and M7 marked recorded, not CAD drivers. |
| E1–E5 | drawing table | Nominal and fitted minimum from §3.6. |
| ±0.3 general | title block | "±0.3 mm under 100 mm, JLC MJF PA12" |
| Open item 3 | validator | `.venv/bin/python scripts/cad/manifest.py --check-bytes docs/fab/cad/v1/manifest.json` → `schema 1 ok` |

## Gates

| Gate | Command | Result |
|---|---|---|
| Unit tests | `.venv/bin/python -m unittest discover -s tests -v` | 70 tests OK |
| Render twice | `scripts/cad/render.py --out` two temp dirs | PNG and PDF SHA-256 identical, and identical to `docs/fab/cad/v1/` |
| Fourteen / solid hashes | compare `files` to commit `66b5564` | No solid hash changed after the font commit. Lid STEP/STL/3MF changed only in `66b5564`. The other twelve solid files match main. The brief said fourteen; lid is three files, so twelve others stay put. |

## What Rolf can judge from the images

- Overall shape of the hook and body, tail, three mock caps, and that the lid sits on the lateral face.
- Thickness difference full 9.0 mm vs thin 7.0 mm (medial PNG, same scale).
- Glasses flat on the hook (lateral PNG).
- Closure layout: lip, bump, groove, nubs, web, tongue, slot, with the plan sizes.
- M1–M8 values and E1–E5 minima as tables.

## What he cannot judge from the images

- Print quality, surface finish, or true hidden-line edges. This is a shaded STL, not a vendor drawing.
- Fillet radii and the inside emboss. The emboss is on the lid underside.
- Exact millimetre distances by counting pixels. Use the tables and the (s, y) section.
- Whether the starburst on the medial face around each cap is a print defect. That pattern is the STL tessellation of the sphere-cap boolean. The solid was not changed.

## What was not done

- No order, upload, quote, or vendor contact.
- Solids other than the lid font were not edited.
- `docs/fab/plan.md`, `measure.md`, `order1.md`, `interface.md` were not edited.
- Open questions file was not edited. Q10 is done in this package.

## Needs a decision

1. **Medial-face starburst at the mock caps.** The STL of the body shows long triangles around each Ø4.7 cap where the sphere meets the medial face. The renderer offsets faces 0.03 mm along the normal; the stars remain. Reading: leave the solid. A later tessellation or a cap cut that does not boolean against the face would clean the picture. Not a wall or fit fail.

2. **Brief said fourteen solid hashes.** Order-1 is five parts × three formats = fifteen hashes. Lid is three of those. Twelve non-lid hashes were unchanged. Confirm that reading.

## Final commit

`a325a635f790d73875d2045ae475189f2708cfd4`
````

### WP6 report (lane `w1`, branch `lane/w1`)

````md
# WP6 report — Packing proof and interface v2

Lane `w1`, branch `lane/w1`, worktree
`/home/user/projects/elicio/.worktrees/w1`. Package `WP6`.
Plan commit `0c5d0eb`. Interpreter: Python 3.13.15 (`.venv`).
`cad` extra now includes matplotlib (3.10.8 in this venv).

## What was built

1. `docs/fab/interface.md` version 2, with a change-log row. v1 numbers
   that did not change are kept. New numbers have a From cell.
2. `scripts/cad/placement.py`: headless matplotlib, Agg, deterministic
   SVG in the body-frame `(u, s)` plane. Coupon-to-parameter mapping is
   in this docstring, in `bte_fit_shell.py`, and in `scripts/cad/README.md`.
3. `docs/fab/cad/v1/placement.svg`, courtyards at maximum dimensions.
4. `tests/test_placement.py`: packing maths plus byte-identical regen.
5. `pyproject.toml` `cad` extra: `matplotlib>=3.9`.
6. `tests/test_cad.py` allows `placement.svg` next to the gauge files.

No CAD solid and no `manifest.json` was edited. No purchase, quote, or
vendor contact.

## Plan §9 acceptance (WP6)

Acceptance: confirmed, or v2 with the escalation for Rolf; placement at
max dims; cell named; RF zone; lead pads.

| Item | Result | How verified |
|---|---|---|
| Confirmed or escalation | **Confirmed with a named non-shell change.** ADS1292 VQFN-32 (RSM) and one BAV199S-Q array. Free 101.53 mm², required 72.17, spare 29.36. TQFP-32 does not fit (largest empty rectangle 4.55 × 10.20). Options B (+3.5 mm length) and C (+3 mm width) are not needed for packing; the numbers each buys are in interface §8.2 | `placement.py` raster and `tests.test_placement.PlacementMathTests` |
| Placement at max dims | `docs/fab/cad/v1/placement.svg` | Regen test, hash below |
| Cell named | DNK 501015 from the fpbattery drawing (page 2, cell art 2022-12-10). **No published folded pack fits 5.2 × 10.4 × 15.6.** In-line BL 17 ± 1. WP8 pocket length 16.0 → 18.4 along s if that pack is kept | Datasheet URL and date in interface §5 and §11 |
| RF zone | 12.4 × 3.8 mm no-copper at the inferior board edge, Spec K pages 9 and 13, issued 2022-07-01. Overlaps keep-out 2. Battery gap 5.00 mm with the cell packed to the hook; 4.60 mm if the cell sits on the rib | Spec K; `budget().rf_keepout2_overlap` True |
| Lead pads | Frozen (5.9, 26.6), (5.5, 30.0), (4.0, 29.0). SIG1 moved +0.1 mm in s. All outside keep-outs + 0.5 and outside the antenna. Clamp distances 1.69–1.73 mm. Reference route drawn Ø1.3, 3 mm bend, Kapton wrap at s 37 | `pad_keepout_gap`, `clamp_distance`, drawing |

## Gates

### Unit tests

```
.venv/bin/python -m unittest discover -s tests -v
```

Result: 76 tests, OK, 10.407 s. Python 3.13.15. Includes 9 placement
tests. CAD regen still matches committed gauge hashes.

### Drawing regen

```
.venv/bin/python scripts/cad/placement.py --out docs/fab/cad/v1/placement.svg
```

SHA-256 `3ca2268c0d0696b000045b8d9b05e04504ba06e3a8c6f74c8fe1643ad8f73aa9`.
Two writes in one process and a write to a temp dir match this hash
(`PlacementRegenTests`).

## What was not done

- No gauge CAD change (forbidden). The +2.4 mm pocket, if chosen, is WP8.
- Q6 nut metal: recorded in interface §12 V2-3, not decided.
- Q11: lid-underside constraint written; WP8 builds 0.4 mm or moves the
  emboss over the battery zone.
- No layout (traces, planes). This is courtyards only.
- Spec L PDF from raytac.com returned HTTP 403; Spec K (same keep-out
  drawing, issued 2022-07-01) was used.

## Needs a decision

1. **Cell pack (interface decision 2).** No SKU on a dated page shows a
   folded pack ≤ 5.2 × 10.4 × 15.6. Pick: (a) WP8 lengthens the pocket
   to 18.4 mm along s for the published DNK in-line pack, or (b) wait
   for a drawing that shows a fold inside the present envelope. Do not
   buy on a custom fold with no drawing.
2. **Packing (plan §10 Open for Rolf item 6).** Closed as option D plus
   the array. Rolf does not need to pick +3.5 mm length or +3 mm width
   for area. Those options still do not fit TQFP-32 at Nominal
   courtyards (empty width 4.55 mm; +3 mm width gives ~7.55 vs 7.60).
3. **Q6 nut metal.** Still Rolf's. Candidates in §12 V2-3. Not a WP6
   decision.
4. **Q11 emboss.** WP8: 0.4 mm over the board, or move the string over
   the battery zone.

## Plan vs brief

The plan wins. The brief asked for a 501015 SKU whose folded pack fits
the envelope. The plan's envelope is unchanged. No such published SKU
was found; that is written in interface v2 rather than silent CAD.

## Final commit

`a3d8599` on `lane/w1`.
````

