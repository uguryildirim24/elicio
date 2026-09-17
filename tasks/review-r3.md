# Code review + fix — Phase 1 round 3 (WP6b, WP5b) on branch review/r3 (Claude Opus 5, high)

You are the reviewer for this round, herdr agent `rev3`. Two lanes
finished their packages. You merge them into one candidate, inspect it,
**fix what is wrong yourself**, run every gate, and write one verdict. You
never push by hand, never merge into `main`, never touch another worktree,
never edit `docs/fab/plan.md` or `docs/fab/open-questions.md`.

Worktree `/home/user/projects/elicio/.worktrees/review`, branch
`review/r3` from `main`. Private environment inside this worktree:
`python3.13 -m venv .venv && .venv/bin/python -m pip install -e '.[cad]'`.

## Steps

1. Read `tasks/phase1-common.md`, `docs/fab/open-questions.md` (Q6, Q7,
   Q13 to Q16 are what this round answers), the two briefs
   `tasks/WP6b-packing-options.md` and `tasks/WP5b-drawings.md`, the round 2
   verdict `tasks/reviews/code-r2.md` (defects 21 to 31, decisions 13 to 15,
   so you do not undo its fixes), and `docs/fab/plan.md` §4, §5, §6, §7,
   §9, §10.
2. Merge, in this order, resolving conflicts yourself: `lane/w5`, `lane/w1`.
   Each lane's diff against `main` shows `HANDOFF.md` and `HANDOFF.json` as
   changed or deleted only because `main` moved after the lanes branched;
   keep `main`'s.
3. Gates, all on the merged tree:
   - `.venv/bin/python -m unittest discover -s tests -v` passes with the CAD,
     render and placement tests running, not skipped.
   - `scripts/cad/placement.py` for every `--option` twice into temp dirs:
     byte-identical and equal to the committed drawings; the default
     regenerates `placement.svg` unchanged from `main`.
   - `layout_conflicts()` is exercised for every option in the tests.
   - Reference build and renders unchanged: the fifteen solids and the three
     views equal `main`'s manifest (this round touches no CAD).
   - `git diff main -- src/ docs/fab/plan.md docs/fab/open-questions.md
     docs/fab/cad/v1/manifest.json` is empty.
4. Adversarial review: the seams below first, then the attack points. Read
   `docs/fab/packing-options.md` as Rolf will, on a phone: if he cannot
   pick from it in two minutes, that is a High defect. Look at every
   option drawing (render the SVGs to PNG and Read them).
5. Fix every defect yourself, in separate commits on `review/r3` with
   messages starting `review(WPn):`. The repo's post-commit hook pushes on
   commit; do not run `git push` yourself.
6. What cannot be fixed without changing the plan goes under "Needs a
   decision", numbered from 20.

## Seams

## Seams from WP5b's report (lane w5, f5ae1e4)
- The Q13 short-tab reading is not buildable with a crimp ring lug: TE 31428 barrel end 8.85 mm from ring centre (6.27 from ring edge), barrel width 1.96 max; alternatives longer. Check WP6b's sheet was redone on the real lug after the coordinator's mid-package note (tab 1.96 + 0.5 margin, 6.27 long, direction free or upright per contacts.md §5.3); the short-tab row must be marked not buildable.
- Bossard BN 146 zinc-plated carbon steel DIN 439 M2.5 (TME 1090798) is inside plan §4's "plated steel" and nickel-free (trivalent zinc passivation): verify the page says trivalent/zinc and not nickel-zinc; verify m 1.60 from the drawing. Brass BN 147 as the nickel-free alternative outside the literal text. Titanium DIN 934 collides by +0.09 mm at wall +0.3: check the arithmetic against interface §2.3 (reservation vs SKU columns).
- Dome: Westfield dk 4.50 max, k 1.50 max; Accu dk 4.70, k 1.50; RJX 4.40 to 4.70 / 1.20 to 1.36. Check contacts.md says the internal stack is unaffected by k (screw seats on the outside) and that interface V2-1 stays open until a lot drawing exists. Contact area numbers (17.35, 15.90, 15.21 mm²) are arithmetic on dk; check.
- Prices: Sortafast 10-pack $17.50 (under the $20 line), RJX 50-pack $33.99 (flagged); kit totals $44.12 to $48.82 marked estimate against the plan §7 $60 contacts line: verify plan §7 actually gives $60 for contacts (the plan says order 2 about $105 including hardware and the DMG kit).
- Every price and drawing number needs URL and date; TME, Fastenright, Titanium Webshop, Westfield, Accu, Sortafast, RJXHOBBY, Titane Services pages: spot-check that the URLs resolve to the SKU named (reviewer may use a read-only agy lane as r2 did).
- LaTeX math again in a Markdown file; plain units preferred.
- Tests: 83 OK, 7 skipped in w5's venv (no build123d); the reviewer runs them with the cad extra.

## Seams from WP6b's report (lane w1)

- **Tab length in three passes.** Pass 1 (2531ff0) put the barrel end at
  8.85 mm from the contact centre (ring radius 2.58 + 6.27 from the ring
  edge, C-31428 rev D4: 0.348 in) and option A closed for the named ICs.
  Pass 2 (15f572f) measured 6.27 from the Ø7.1 keep-out edge instead,
  barrel end 9.82, and A stopped closing; that wording was the
  coordinator's error. Pass 3 was asked to restore a1 = 8.85 (5.30 beyond
  the Ø7.1 edge). Verify the final `placement.py` uses 8.85 with a From row
  quoting the drawing, and that every number on the sheet was regenerated
  from that geometry, not hand-carried from a previous pass.
- **"Closes" must mean every part has a site.** The final sheet says option
  A closes with `layout_conflicts("A")` empty, free 83.23 mm², spare 3.93,
  and 10 of 25 0402 courtyards placed; the report says the other 15 "have
  no 1.80×0.90 courtyard on this board" and E absorbs only 2 of them.
  Fifteen passives with no site is not a closed layout, and the sheet
  recommends A anyway. Make the sheet say per option how many parts have a site and
  what happens to the rest (C places all 25; E puts two on the lateral
  face). Re-examine the recommendation (A) on that basis; if A only closes
  for the named ICs, the sheet must say so in its first line.
- **SIG2 tab at 180° (−u).** CONTACT_2 sits at u 10.4; ring radius 2.58 plus
  barrel 6.27 puts the barrel end near u 1.55, at the low-u side wall
  (u 1.5) with no 0.5 margin. Check the tab-to-wall clearance in
  `layout_conflicts()` and the drawing; a tab in the wall is a High defect.
- **Tab direction search**: confirm the direction is a searched parameter
  with a test, not two hand-picked angles; confirm the "upright does not
  fit" arithmetic (keep-out air 4.13 − 1.5 = 2.63 versus 0.46 + 6.27 = 6.73)
  and that the reference lug's upright envelope in the tail pocket
  (contacts.md §5.3) is consistent with WP5b's drawing.
- **Two passes.** The lane relaid out after the coordinator's note and may
  have run a second pass on the follow-up prompt; the report you get is the
  last one. Check `placement.svg` equals `placement_A.svg`, the four option
  drawings match their `--option` runs, and the `mode="q13"` mask is used
  only for the budget row and tests.
- `.reports/WP6b-report.md` tracked on `lane/w1`: `git rm --cached` if the
  lane did not.
- Clamp distances (1.68 / 1.76 / 4.60 mm) within the 10 mm rule; arrays'
  line map keeps three separately protected paths (plan §6, S2).
- Q14 numbers on the sheet must match interface §6.3; B's chord and gate
  numbers (51.43 / 54.43) by the same formula as `bte_fit_shell.py`.

## Attack points per package

- **WP6b**: the sheet has one row per option with free versus required
  area, the pad positions and tab geometry used, the conflict list (empty
  or explained), what shell parameters change and by how much, the effect
  on TOTAL_CHORD and the M1 gate, and what Rolf gives up; one
  recommendation with reasons; one line saying exactly what Rolf answers.
  Option E's height budget comes from plan §5's lateral row (board top to
  lid underside minus the foam strip, outside the module footprint) with a
  From cell. The two diode arrays keep three separately protected paths
  (plan §6, S2) in every option. The interface changed only by an errata
  row and a §12 pointer; the frozen pads in §4 are untouched. Nothing in
  CAD or the manifest changed.
- **WP5b**: every number in `contacts.md` §8 traces to a drawing or page
  with URL and date; the lug statement is plain (no crimp lug ends under
  its pad) and gives the numbers WP6 needs; the nut table makes no
  recommendation and says for each row whether it is inside plan §4's text
  and nickel-free; the dome section says the internal stack is unaffected
  by head height; §1 and §7 updates agree with §8; the $20 line flags are
  right; no stack number in §2 changed.

## Output

1. `tasks/reviews/code-r3.md`: a three-line verdict (MERGE /
   MERGE-AFTER-DECISION / REJECT), the gate results with commands, a table
   of defects (severity, file:line, what was wrong, what you changed, commit
   hash), and "Needs a decision" numbered from 20. Commit it on `review/r3`.
2. `.reports/review-r3-report.md` in this worktree: what you merged, what
   you changed, the final commit sha.
3. Then, in order:

       herdr pane report-metadata "$HERDR_PANE_ID" --source lane --token lane=review-r3 --token done=1
       herdr notification show "review r3 done" --body "reviewer rev3" --sound done
       herdr agent prompt elicio "DONE review-r3 .reports/review-r3-report.md <final commit sha>" || herdr agent prompt elicio "DONE review-r3 .reports/review-r3-report.md <final commit sha>"

Your turn must end with that push, including if the verdict is REJECT. If
you start a helper lane, close its tab before you push.

## The worker reports, verbatim

### WP5b report (lane `w5`, branch `lane/w5`)

````md
# WP5b Work Package Report: Lug, Nut, and Dome Drawings for Q13, Q6, and Q7

**Package:** WP5b — Lug, nut, and dome drawings for open questions Q13, Q6, and Q7  
**Lane:** w5  
**Worktree:** `/home/user/projects/elicio/.worktrees/w5`  
**Branch:** `lane/w5`  
**Date:** 2026-09-17  
**Final Commit SHA:** `f5ae1e438c300211005d016124419d3d04fa6fef`

---

## 1. What Was Built

Updated `docs/fab/contacts.md` satisfying all requirements of `tasks/WP5b-drawings.md` and `tasks/phase1-common.md`:

1.  **Ring Lug Technical Drawing and Pad Distance Analysis (Open Question Q13, §8.1):**
    *   **TE Connectivity 31428 Drawing Specifications:** Inspected TE Customer Drawing C-31428 rev D4 (date read: 2026-09-17). Recorded exact dimensions:
        *   Material: Copper ASTM B-152, plated with 100% matte pure tin per ASTM B-545 ($\ge 0.00254\text{ mm}$, nickel-free).
        *   Stock thickness: $0.018 \pm 0.002\text{ in}$ ($0.457 \pm 0.051\text{ mm}$, nominal 0.46 mm), satisfying plan §3.3 reservation ($\le 0.50\text{ mm}$).
        *   Stud hole: $0.119 \pm 0.003\text{ in}$ ($3.02 \pm 0.08\text{ mm}$) for #4 / M2.5 stud.
        *   Ring outer diameter / tongue width: $0.203 \pm 0.008\text{ in}$ ($5.16 \pm 0.20\text{ mm}$, max 5.36 mm; radius nominal 2.58 mm).
        *   Distance from ring center to barrel end: $0.348\text{ in}$ ($8.85\text{ mm}$ nominal / max).
        *   Distance from outer ring edge to barrel end: $6.27\text{ mm}$.
        *   Overall length: $0.450\text{ in}$ max ($11.43\text{ mm}$ max).
        *   Barrel outer diameter / width: $0.077\text{ in}$ max ($1.96\text{ mm}$ max), fitting inside the 3.0 mm tab envelope.
        *   Wire range: 26–22 AWG ($0.10–0.41\text{ mm}^2$).
    *   **Two Alternative Ring Terminals Evaluated:**
        *   *Panduit P22-4R-C:* Customer Drawing 102215 (read: 2026-09-17). Thickness 0.51 mm, ring OD 5.20 mm, center-to-barrel-end 10.61 mm (edge-to-barrel-end 8.01 mm), barrel OD 2.03 mm, 26–22 AWG, tin-plated copper.
        *   *Nichifu R0.3-3:* Catalog 2023 p. 6 (read: 2026-09-17). Thickness 0.50 mm, ring OD 5.20 mm, center-to-barrel-end 9.40 mm (edge-to-barrel-end 6.80 mm), barrel OD 2.20 mm, 24–20 AWG, tin-plated copper.
    *   **Pad Distance Comparison & Plain Statement:**
        *   Contact centers to pad centers: SIG1 = 4.60 mm, SIG2 = 5.80 mm.
        *   Outer ring edge (radius 2.58 mm) to pad centers: SIG1 = 2.02 mm, SIG2 = 3.22 mm.
        *   **Plain Statement:** No off-the-shelf crimp ring terminal allows the tab to end under its own pad. TE 31428 is the shortest available crimp terminal in the industry (8.85 mm from center). If laid flat toward its pad, TE 31428 overshoots SIG1 pad center by +4.25 mm and SIG2 pad center by +3.05 mm. WP6 cannot assume a flat tab terminating under the pad; WP6 needs this exact 8.85 mm center-to-barrel-end (6.27 mm edge-to-barrel-end) dimension.
2.  **Nut Candidates Comparison Table (Open Question Q6, §8.2):**
    *   Evaluated DIN 439 / ISO 4035 M2.5 thin nuts in plated steel, plain brass, tinned brass, titanium, and DIN 934 titanium full nut fallback.
    *   *Plated Carbon Steel DIN 439:* Bossard BN 146 (TME Order No. `1090798`, read 2026-09-17, $0.063 USD/ea, $6.30/100pk). $m = 1.60\text{ mm}$, $s = 5.0\text{ mm}$, $e = 5.45\text{ mm}$. Inside plan §4 text ("plated steel"): **YES**. Nickel-free: **YES** (zinc trivalent blue passivation).
    *   *Plain Brass DIN 439:* Bossard BN 147 (TME Order No. `1159550`, read 2026-09-17, $0.16 USD/ea, $1.60/10pk). $m = 1.60\text{ mm}$, $s = 5.0\text{ mm}$, $e = 5.45\text{ mm}$. Inside plan §4 text: **NO** (copper-zinc alloy). Nickel-free: **YES** (unplated bare brass).
    *   *Tinned Brass DIN 439:* Drawing standard $m = 1.60\text{ mm}$, $s = 5.0\text{ mm}$. Distributor stock is plain or nickel-plated; pure tin over brass is a custom OEM run. Sourcing & price: **UNVERIFIED**. Inside plan §4 text: **NO**. Nickel-free: **YES**.
    *   *Titanium DIN 439:* Fastenright `M2.5-DIN439-TI` (read 2026-09-17). $m = 1.60\text{ mm}$, $s = 5.0\text{ mm}$, $e = 5.45\text{ mm}$. Grade 2/5, 3.1 cert available. Bespoke quote required; price: **UNVERIFIED**. Inside plan §4 text: **NO**. Nickel-free: **YES**.
    *   *Titanium DIN 934 Fallback:* Titanium Webshop SKU `663701003` (read 2026-09-17, €0.87/ea ≈ $0.95 USD). Grade 2 titanium. Drawing DIN 934: $m = 2.00\text{ mm}$, $s = 5.0\text{ mm}$, $e = 5.77\text{ mm}$. Inside plan §4 text: **NO**. Nickel-free: **YES**. Stack analysis: 2.0 mm nut height leaves zero margin; at wall tolerance +0.3 mm (wall 1.80 mm), nut top reaches $y = 4.26\text{ mm}$ and Kapton disc reaches $y = 4.39\text{ mm}$, colliding with the medial PCB at $y = 4.30\text{ mm}$ by **+0.09 mm**.
    *   *No Recommendation:* Per brief instructions, no recommendation is made; Rolf picks.
3.  **Titanium Dome Drawings and Plan Differences (Open Question Q7, §8.3):**
    *   Inspected technical drawings from Westfield Fasteners (Drawing M2.5 ISO 7380-1, read 2026-09-17) and Accu Group (ISO 7380-1 specification, read 2026-09-17).
    *   Retail SKUs compared: Sortafast `SF-BH2504-10` ($17.50/10pk, Grade 5), RJXHOBBY `RJX3995-M2.5X4mm` ($33.99/50pk, Grade 2), Titane Services `vis-titane-ISO7380-G5-M2.5` (€3.57/ea, Grade 5, 5 mm length requires trimming).
    *   Quantitative differences from Plan CAD reservation ($d_k = 4.70\text{ mm}$, $k = 1.35\text{ mm}$, hex socket $s = 1.50\text{ mm}$):
        *   Head diameter $d_k$: Westfield specifies 4.50 mm max ($-0.20\text{ mm}$ diff); Accu specifies 4.70 mm max ($0.00\text{ mm}$ diff); RJXHOBBY listing text quotes 4.40–4.70 mm ($0.00\text{ to } -0.30\text{ mm}$ diff).
        *   Crown height $k$: Westfield and Accu specify 1.50 mm max ($+0.15\text{ mm}$ taller dome); RJXHOBBY quotes 1.20–1.36 mm ($-0.15\text{ to } +0.01\text{ mm}$).
        *   Hex socket size: 1.50 mm across flats on all options ($0.00\text{ mm}$ diff).
    *   Consequences per `interface.md` §2.2 Note D1:
        *   Electrode contact area decreases from $17.35\text{ mm}^2$ (at 4.7 mm) to $15.90\text{ mm}^2$ at 4.5 mm (an 8.3% decrease), or $15.21\text{ mm}^2$ at 4.4 mm (a 12.3% decrease).
        *   External dome height increases by $+0.15\text{ mm}$ if $k = 1.50\text{ mm}$, increasing mastoid skin indentation pressure slightly.
        *   Internal cavity stack is completely unaffected: head seats on the exterior medial face; shank length $L = 4.0\text{ mm}$ through 1.5 mm wall leaves $2.5\text{ mm}$ inside regardless of $k$.
        *   Fit gauge model keeps $4.70\text{ mm} \times 1.35\text{ mm}$ per interface item V2-1 until a purchased lot drawing is frozen.
4.  **Verified Prices and Kit Total Estimate (§8.4):**
    *   Every price quoted with product page URL and date read (2026-09-17 or 2026-09-16).
    *   Sortafast screw 10-pack ($17.50 USD) is under the $20 limit.
    *   RJXHOBBY screw 50-pack ($33.99 USD) is flagged as exceeding the $20 line per plan §9.
    *   Total kit estimate for cheapest nickel-free combination:
        *   Baseline Kit (Plan §4 compliant, Bossard BN 146 plated steel nuts): **$48.82 USD (estimate)**.
        *   Alternative Kit (Bossard BN 147 plain brass nuts): **$44.12 USD (estimate)**.
        *   Fallback Kit (Titanium Webshop DIN 934 full nuts): **$45.37 USD (estimate)**.
        *   All combinations conform to the plan §7 Order 2 contacts budget of **$60.00 USD**.
5.  **Superseded Section Updates in `docs/fab/contacts.md`:**
    *   Updated §1.1 table and text with verified product URLs and prices for Sortafast and RJXHOBBY (2026-09-17).
    *   Updated §1.2 table and text with Bossard BN 146 zinc-plated carbon steel, Bossard BN 147 plain brass, and Titanium Webshop DIN 934 full nut.
    *   Updated §1.3 Tab Clearance row and assessment with verified barrel width ($1.96\text{ mm}$ max from C-31428 rev D4) and barrel length ($8.85\text{ mm}$ from center).
    *   Updated §7 QA checklist items 1, 2, and 3.

---

## 2. Acceptance Verification (Plan §9 Row WP5 and Common Gates)

### Gate 1: Test Suite
*   **Command:** `.venv/bin/python -m unittest discover -s tests -v`
*   **Result:** Ran 83 tests in 0.398s. Result: **OK (skipped=7)**. 0 failures, 0 errors.

### Gate 2: Clean Git Working Tree
*   **Command:** `git status --short`
*   **Result:** Clean after commit `f5ae1e438c300211005d016124419d3d04fa6fef`. Untracked file `.reports/WP5b-report.md` is gitignored.

### Gate 3: Q13 Lug Drawing & Pad Distance Statement
*   **Verification:** Section 8.1 quotes thickness, ring OD, hole, center-to-barrel-end, barrel width, wire range from TE Customer Drawing C-31428 rev D4 with URL and date read. Quotes two alternatives (Panduit P22-4R, Nichifu R0.3-3). Formally states no off-the-shelf crimp lug ends under its pad, and quantifies TE 31428 overshoot (+4.25 mm at SIG1, +3.05 mm at SIG2).
*   **Result:** **PASS**.

### Gate 4: Q6 Candidate Nut Table with Drawings & Conformance
*   **Verification:** Section 8.2 presents comparison table for DIN 439 M2.5 thin nuts in plated steel, plain brass, tinned brass, titanium, and DIN 934 titanium full nut fallback. Includes vendor URLs, dates, prices, cert availability, $m$, $s$, $e$ from drawings. Evaluates plan §4 text conformance and nickel-free status. Makes no recommendation.
*   **Result:** **PASS**.

### Gate 5: Q7 Dome Drawings and Plan Differences
*   **Verification:** Section 8.3 evaluates Westfield and Accu drawings against plan CAD reservation ($d_k = 4.70\text{ mm}$, $k = 1.35\text{ mm}$). Quantifies differences and analyzes consequences per interface §2.2 Note D1.
*   **Result:** **PASS**.

### Gate 6: Pricing, Line Limits, and Kit Total
*   **Verification:** Every price has vendor URL and date read or is UNVERIFIED. RJXHOBBY ($33.99) flagged as over $20 line. Complete kit estimate computed at $44.12 to $48.82 USD (under $60 allowance) and marked estimate.
*   **Result:** **PASS**.

---

## 3. What Was Not Done

1.  **No Purchasing, Quoting, Carts, or Vendor Contact:** Per `tasks/phase1-common.md`, no purchase orders were placed, carts filled, quote requests submitted, accounts created, or vendors contacted.
2.  **No Modification of Non-Owned Files:** `plan.md`, `open-questions.md`, `interface.md`, `montage.md`, and `packing-options.md` were not edited.
3.  **No Change to Stack Numbers in §2:** The 2.63 mm stack arithmetic in `docs/fab/contacts.md` §2 remains unchanged.

---

## 4. Needs a Decision

1.  **Open Question Q6 (Nut Material Choice):**
    *   Bossard BN 146 zinc-plated carbon steel DIN 439 thin nut ($0.063/ea, TME) is strictly inside plan §4 text and nickel-free.
    *   Bossard BN 147 plain brass DIN 439 thin nut ($0.16/ea, TME) is nickel-free, but outside literal plan text (copper-zinc alloy).
    *   Titanium DIN 934 full nut (Titanium Webshop, €0.87/ea) is nickel-free, but has zero stack margin and fails tolerance stack by +0.09 mm at wall +0.3 mm.
    *   *Rolf decides which nut metal to order for S1.*
2.  **Open Question Q13 (Lug Tab Routing in WP6):**
    *   TE 31428 crimp barrel extends 8.85 mm from ring center (6.27 mm from ring edge).
    *   Because pad centers are 4.6 mm (SIG1) and 5.8 mm (SIG2) from contact centers, a flat tab directly toward the pad overshoots by +4.25 mm and +3.05 mm.
    *   *WP6 must lay out around the 8.85 mm length (e.g. angling the lug away from walls/nets or bending the tab upright as in §5.3).*
3.  **Open Question Q7 (Screw SKU Selection):**
    *   Sortafast `SF-BH2504-10` (10pk, Grade 5) is verified at $17.50 USD (under $20 line).
    *   RJXHOBBY `RJX3995-M2.5X4mm` (50pk, Grade 2) is verified at $33.99 USD (over $20 line, though unit price is $0.68/ea).
    *   *Rolf decides whether to order Sortafast (under $20 line) or approve the RJXHOBBY $33.99 pack.*

---

## 5. Final Commit SHA

*   `f5ae1e438c300211005d016124419d3d04fa6fef`
````

### WP6b report (lane `w1`, branch `lane/w1`)

````md
# WP6b report — third pass (TE 31428 a1 8.85 from centre)

Lane `w1`, branch `lane/w1`, package WP6b. Third pass: coordinator wording “6.27 from the Ø7.1 edge” was wrong. C-31428 rev D4 (contacts.md §8.1) puts 6.27 mm from the ring outer edge. Ring radius 2.58 mm. Barrel end **8.85 mm** from the contact centre (0.348 in). Ø7.1 already covers the ring (3.55 > 2.58). Tab beyond the keep-out is 8.85 − 3.55 = **5.30 mm**. Working span: a0 3.55, a1 8.85. Direction search, Q13 “not buildable” row, answer line, and untracked report stay from the second pass.

## What was built

- `tab_span` mode `real` returns `(KEEPOUT_R, LUG_A1)` = (3.55, 8.85). First relayout `2531ff0` had a1 8.85; this pass keeps that a1 and keeps a0 at the keep-out edge (3.55), not at RING_R.
- Direction search stays: `legal_tab_degrees` / `search_tab_degrees`. Tests assert 355°/170° and 0°/180° are legal, and search matches `TAB_DEG_BY_OPTION` for A and C.
- Signal tabs are **flat**. Upright does not fit (need 6.73 mm, have 2.63 mm). Reference stays upright in the tail pocket (contacts.md §5.3).
- Q13 short tab stays one sheet row, marked **not buildable with a crimp lug (WP5b)**. The answer line does not offer “wait for the lug drawing”.
- Option A: closes. Empty `layout_conflicts`. SIG1 355°, SIG2 170°, HIGH_U wire. VQFN (9.90, 23.15). Arrays (4.50, 27.10) and (7.15, 26.75). Clamp 1.68 / 1.76 / 4.60 mm. Free 83.23, spare 3.93. **10 of 25** 0402s have a medial site. The other 15 have no 1.80×0.90 courtyard on this board; they sit on C (27 sites).
- Option B: closes. SIG1 355°, SIG2 120°, INFERIOR wire. Arrays (4.50, 27.10) and (2.65, 30.50). TOTAL_CHORD 47.90 → 51.43. M1 50.90 → 54.43. **15 of 25** 0402s. The other 10 sit on C.
- Option C: closes. SIG1 0°, SIG2 180°, HIGH_U wire. **25 of 25** 0402s (max 27, 2 spare). TOTAL_CHORD unchanged. You give up 3 mm of width.
- Option E: closes. Same tabs/wire as A. ICs medial. **12 of 25** 0402s (10 medial + 2 lateral). The other 13 have no site. Lateral takes only 2 of A’s leftover 15.
- Drawings regenerated. `placement.svg` equals `placement_A.svg` (sha256 `044db94711e3fb3b32b5aa73c066ae98935ef7e3a04a72f40f6bd8167f7f7ca3`).
- Sheet recommends **A**. Pick C only if you need all 25 of the 0402 courtyards.
- `.reports/WP6b-report.md` is untracked (`.reports/` is gitignored).

CAD solids, `manifest.json`, `plan.md`, `open-questions.md`, `contacts.md`, and `montage.md` were not edited. Interface version stays 2. Pads in §4 stay.

## Plan §9 acceptance

WP6: "confirmed, or v2 with the escalation for Rolf".

| Item | Command | Result |
|---|---|---|
| Full suite | `.venv/bin/python -m unittest discover -s tests -v` | 93 tests OK |
| Drawings twice | `placement.py --option A\|B\|C\|E` then regen tests | A/B/C/E regenerate byte-identical |
| Escalation sheet | `docs/fab/packing-options.md` | Q13 not buildable (WP5b). A, B, C and E close. Recommend A. |

Packing is not confirmed until Rolf picks.

## What was not done

- No CAD solid change (WP8 after Rolf picks).
- Pads in interface §4 were not moved.
- Signal tabs were not bent upright.

## Needs a decision

Rolf picks from `docs/fab/packing-options.md`: `I pick C` or `I pick B` or `I pick E` or `I pick A`. Recommendation: **A**. Pick C only if you need all 25 of the 0402 courtyards.

## Final commit sha

`c6cbd45`
````

