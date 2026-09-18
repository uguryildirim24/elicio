# Code review + fix — Phase 1 round 5 (WP10, WP11, WP12, WP13, WP16, WP17) on branch review/r5 (Claude Opus 5, high)

You are the reviewer for this round, herdr agent `rev5`. Five lanes
finished six packages under plan v2. You merge them into one candidate,
inspect it, **fix what is wrong yourself**, run every gate, and write one
verdict. You never push by hand (the repo's post-commit hook pushes every
commit), never merge into `main`, never touch another worktree, never edit
`docs/fab/plan.md`, `docs/fab/plan-v2.md` or `docs/fab/open-questions.md`.
No purchase, sign-up, quote request, upload or vendor contact; web only to
re-read a page a lane cites. No Agent-tool subagents.

Worktree `/home/user/projects/elicio/.worktrees/review`, branch
`review/r5` from `main`. Private environment inside this worktree:
`python3.13 -m venv .venv && .venv/bin/python -m pip install -e '.[cad]'`.
KiCad 10 (`kicad-cli`) and `arduino-cli` with the Adafruit nRF52 core are
installed on this Mac by the lanes; use them, install nothing else.

Start line (the coordinator restarts you by copy-paste):

    herdr agent start rev5 --kind claude --pane <pane> --parent w1B:p1 -- --model claude-opus-5 --effort high --dangerously-skip-permissions

## Steps

1. Read `tasks/phase1-common.md`, `docs/fab/plan-v2.md` (signed off; §3,
   §4, §5, §6, §8, §9, §11, §12), `docs/fab/open-questions.md` Q28 to Q56,
   the briefs `tasks/WP10-research-v2.md`, `tasks/WP11-packing-v2.md`
   (plus the four coordinator notes summarised in Q50, Q51 and in its
   report), `tasks/WP12-board.md`, `tasks/WP13-firmware.md`,
   `tasks/WP16-record.md`, `tasks/WP17-research-v3.md`, and the round 4
   verdict `tasks/reviews/code-r4.md` (its decisions 24 to 27 still bind
   the CAD script).
2. Merge, in this order, resolving conflicts yourself:
   - `lane/w1` **by squash** (`git merge --squash lane/w1`, then commit as
     `packing(v2): WP11 squashed for review`): the branch carries 864
     drawings, 109 MB, that must not enter `main`'s history. Before the
     squash commit, keep only the drawings of the four closing layouts,
     the Stage B winner, and one per first-conflict family named in
     `docs/fab/packing-v2.md` §2 (at most forty files), delete the rest,
     and make `placement.py --all` write drawings only for closers unless
     `--all-drawings` is passed; update the tests and the packing doc's
     file references accordingly.
   - `lane/w5`, `lane/w4`, `lane/w9`, `lane/w2` by ordinary merge.
   Each lane's diff against `main` shows `HANDOFF.md`, `HANDOFF.json` and
   `docs/fab/open-questions.md` as changed only because `main` moved after
   the lanes branched; keep `main`'s.
3. Gates, all on the merged tree:
   - `.venv/bin/python -m unittest discover -s tests -v` passes with the
     CAD, render, placement, frame_v2 native-harness and board-release
     tests running, not skipped.
   - Order 1 untouched: reference build twice, fifteen solids identical to
     each other and to `docs/fab/cad/v1/`; `render.py` twice, three views
     identical; the committed v1 `manifest.json` byte-identical to `main`'s.
   - Stage B v2 (`scripts/cad/params/stageb_v2.toml`) built twice into a
     temp dir by the README command: byte-identical; every named check
     reports a number or NOT_MEASURED by name; nothing written under
     `docs/fab/cad/v2/` or `v1/` by that build.
   - `scripts/board/release.py` runs end to end with `kicad-cli`: ERC 0
     errors, DRC report produced and its counts in the summary, BOM rows
     equal placed parts, STEP written; the test fails, not skips, without
     `kicad-cli`.
   - `arduino-cli compile --fqbn adafruit:nrf52:feather52840 --library
     firmware --output-dir <tmp> firmware/elicio_stream` exits 0.
   - `git diff main -- docs/fab/plan.md docs/fab/plan-v2.md
     docs/fab/open-questions.md docs/fab/interface.md docs/fab/contacts.md`
     is empty.
4. Adversarial review: the seams below first, then the attack points.
   Open the Stage B v2 winner and one interface I failure in a viewer or a
   section before trusting `packing-v2.md`'s verdicts.
5. Fix every defect yourself, in separate commits on `review/r5` with
   messages starting `review(WPn):`. Do not run `git push`.
6. What cannot be fixed without changing plan v2 goes under "Needs a
   decision", numbered from 57.

## Seams

- **One packing truth.** WP11 used foam 0.3 under the cell (its brief) while
  the order-1 Stage B `CELL_envelope` keeps plan v1's 0.5 strip, so the
  packing-smallest lid is 7.0 and the Stage B winner is 8.0. Decide one
  reading (plan v1 §5's 0.5 measured in the solid is the safe one), apply
  it in both places, and make `packing-v2.md` §4 and §6 say the same
  number. The outer height Rolf is told (Q38, Q51) must be the one the
  solid measures.
- **Interface I's 0/720 is a claim about code.** Read `placement_v2.py`'s
  under-board and standoff-collision logic: the SIG1 collision with the
  22 mm cell, the deformed-clearance table (board bends 0.5 down onto the
  bosses), the "carries load" flag, and the recess variants. A wrong sign
  or a swapped axis here reverses the round's main decision (Q50). Check
  that II's tabs and the standoff pockets are modelled as floor occupants
  in II too, and that the 501015 series layouts' free area and chord are
  measured, not asserted.
- **Board outline handoff.** WP12 took its outline and part positions from
  `packing-v2.md` §5 (`A_501015_series_w20_y7_iII_s3`) on `lane/w1` at
  `43a982a`; WP11's second turn (`7df78b5`) changed nothing there, verify.
  The board's flex tabs, ring pads, connector edge and module keep-out must
  match the placement's numbers; where they differ, the solid wins and the
  board moves, or the difference is a decision.
- **Cell and connector.** The closing layouts use the 501015 (Q55, single
  units unverified) and WP12 places JST-SH with PH as an alternate (G1b;
  WP17 §1 found SparkFun's page saying SH and the pack drawing PHR). The
  board must not silently commit to one pack; `board-v2.md` must say which
  footprint is placed and why, and `orders-v2.md` must carry the cell as
  an open line, not a price.
- **Firmware constants.** WP13's `V_STOP_MV` 2700 and `V_START_MV` 2800 are
  placeholders; if WP12's `board-v2.md` computed V_STOP and V_START, align
  the firmware header to those numbers in a `review(WP13):` commit and say
  so; if not, both files must say "placeholder until WP12" in the same
  words. Gain 12, 2.42 V reference and 2000 SPS in the frame metadata must
  match the schematic's ADS1292 configuration.
- **Research is evidence, not decision.** L5 and L6 report; `board-v2.md`
  and `orders-v2.md` decide and cite. Spot-check eight numbers across L5
  and L6 on their live pages (the Harwin drawing, the DigiKey stock line,
  JLC's 70 × 70 panel rule, JLC's programming fee, the TLV713 3.3 V versus
  the plan's 3.0 V LDO, the Debug Probe's 3.63 V limit, the bootloader's
  500 ms window, SparkFun's connector text). A number whose quote is not
  on the page is retagged UNVERIFIED with the date, not deleted.
- **Record once.** WP16's `EARPIECE_DESIGN.md` carries each v2 decision
  once; WP11's, WP12's and WP13's docs must not restate them, only point.
  Q50 to Q55 landed after WP16 wrote; add them to the record's plan v2
  section in one `review(WP16):` commit, one paragraph each, "waits for
  Rolf" where it does.
- **Rolf, never "owner" or "user"**, in every new prose file.
- **Drawings and repo size.** After the squash, `git count-objects -vH` on
  the candidate must not have grown by more than 10 MB over `main`; report
  the number.

## Seams from WP12 (lane w2)

- **Two turns, one board.** WP12's first turn (`9fa31d2`) built a rigid
  4-layer board on a provisional 17 × 33 mm outline with three 8 × 8 pads
  (interface I) because it looked for `packing-v2.md` before WP11 landed.
  The coordinator's note (Q50) then redirected it to interface II, a
  2-layer flex with stiffeners, ring-pad tabs under the standoffs and the
  outline of `A_501015_series_w20_y7_iII_s3`; its second turn landed at
  `a4080c2` (2-layer FPC, ring-pad tabs, USB on the end face) and the one
  report below covers both turns. Review the branch as it stands:
  the flex board is the candidate, the rigid one must survive only as the
  rejected candidate in `board-v2.md` (schematic unchanged between them).
  Its own open items (JLC FR4 stiffeners come in thicknesses other than
  the 0.3 WP11 assumed; six stiffener pieces against JLC's extra fee at
  four or more; the switch against the 2.5 mm assembly edge; SIG1/SIG2
  rings drawn unfolded while packing gives the folded site) are seams
  between WP11 and WP12: resolve what the pages and the solid settle,
  decide the rest.
- **CadRegen failures in w2's venv.** WP12 reports 13 failures in
  `test_cad.CadRegenTests.test_reference_regen_matches_committed_hashes`
  without having touched CAD files. Reproduce on your clean `.[cad]` venv
  on the merged tree. If the hashes match there, the lane's venv had a
  different build123d/OCP and you record which pins the test depends on;
  if they differ on your venv too, something in the merged tree (WP11's
  `bte_fit_shell.py` changes) moved order 1, which is a High defect (round
  4 rule: order 1 must not move).
- **Release job semantics.** ERC 0 with 13 `lib_symbol_mismatch` warnings:
  fix the library so the warnings go (resolved `extends` copies). DRC 829
  errors are the unrouted state and must be reported as such in
  `summary.json` with `routed: false`; the job may not exit 0 silently on
  DRC errors once routing is claimed, so the test must assert the
  fail-closed rule for the routed state too (a flag or a field), not only
  for ERC.
- **Circuit against plan v2 §5.5 and the datasheets.** BQ25100YFPR 4.20 V,
  ISET 6.80 kΩ (recompute from the sheet's equation and state the current);
  PRETERM and termination floor versus the pack's end-of-charge; TS 10 kΩ
  to VSS; the system load during charge versus the 1 mA termination floor
  (its "2 mA" item under Needs a decision needs a number from the sheet);
  TLV71330 3.0 V dropout and the battery voltage at which AVDD leaves
  2.7 V; the P-FET gate polarity and body diode with VBUS present and
  with an uncooperative MCU; the G2 table has every state the plan lists;
  V_STOP and V_START computed with the error budget the plan names, then
  WP13's header aligned; TC2030 map equals plan v2 §8 (1 VTref sense, 2
  SWDIO, 3 GND, 4 SWCLK, 5 GND, 6 nRESET); the Debug Probe at a 3.0 V
  target versus its 3.3 V nominal I/O (G4 says both directions of the
  limits, from the probe's documentation that WP17 §6 quotes).
- **Pads versus RF keep-out.** The first turn could not fit three 8 × 8 pads
  beside the module keep-out on 17 × 33; on the flex board the ring pads
  sit on tabs outside the main outline, so the conflict should be gone.
  Check the keep-out polygon against the module sheet and interface v2
  §6.3, and that no copper of the contact nets crosses it.
- **BOM lines.** Every part a catalogue line with LCSC number, tier and the
  displayed stock on the date read, or UNVERIFIED; `orders-v2.md` (WP16)
  takes the board line as an allowance until a configured checkout exists;
  no BAV199 on v2 is a decision the record must state with the ESD
  protection actually used.
## Attack points per package

- **WP11**: `layout_conflicts()` height logic with a hand-checked case per
  family; the "closes" flag for the four closers re-derived from the solid
  (Stage B v2 build), not the table; `--all` runtime and drawing count
  after your prune; `placement.py` still passes its own older tests
  unchanged; `stageb_v2.toml` header names what each provisional value
  waits on; the M1 gate uses 52 as a default and says so in the manifest;
  nothing under `docs/fab/cad/v2/`; no plan edits.
- **WP12**: every net in the schematic reachable from the G2 table; the
  ring pad's annulus versus the Harwin 4.0 or Spacer Express 3.0 standoff
  face (5 mm across flats, Ø2.7 hole) and the ISO 7380 screw's projection;
  coverlay openings on the rings; stiffener outlines as separate layers
  the assembler can read; `release.py` outputs match what JLC's FPC page
  asks for (layers, drill, BOM and CPL columns); the test fails without
  `kicad-cli`; `board-v2.md` cites a page and date for every JLC and
  distributor number; the E73 alternate mapping table complete; Rolf, not
  "owner".
- **WP13**: `frame-v2.md` field by field against plan v2 §6; each fixture
  file decoded by the test and its expected outcome asserted (not just
  "no exception"); the native harness compiled by the test with the
  system clang and the test failing, not skipping, if it cannot; ADS1292
  register bytes against the datasheet (CONFIG1 data rate for 2 kSPS,
  CH1SET gain 12, RLD, lead-off off); the ring buffer's overrun path
  reports acquisition overrun, not transport loss; VBUS refuses streaming
  in code, not in a comment; `montage.md` above §8 byte-identical to
  `main`; the Arduino sketch builds from a clean `arduino-cli` cache
  (the lane's cache is under `~/Library/Arduino15`, reuse it).
- **WP16**: each decision once (grep the headings); the superseded markers
  point at plan v2 sections; `orders-v2.md` has no number without a source
  or the word allowance, and no total; requirement 5's history line dated.
- **WP10 and WP17**: the eight spot-checks above; UNVERIFIED tags kept;
  the two identifier fixes cite their pages; no recommendation beyond the
  facts (WP10 §4 "recommended" wording becomes "the plan chose", or is
  left as the lane's opinion, clearly marked); the E73 antenna sheet still
  unreachable is said so.

## Output

1. `tasks/reviews/code-r5.md`: a three-line verdict (MERGE /
   MERGE-AFTER-DECISION / REJECT), the gate results with commands and
   numbers (test count and skips, hash identity, Stage B v2 identity,
   release job summary, firmware build size, repo growth), a table of
   defects (severity, file:line, what was wrong, what you changed, commit
   hash), and "Needs a decision" numbered from 57. Commit it on
   `review/r5`.
2. `.reports/review-r5-report.md` in this worktree: what you merged, what
   you changed, the final commit sha.
3. Then, in order:

       herdr pane report-metadata "$HERDR_PANE_ID" --source lane --token lane=review-r5 --token done=1
       herdr notification show "review r5 done" --body "reviewer rev5" --sound done
       herdr agent prompt elicio "DONE review-r5 .reports/review-r5-report.md <final commit sha>" || herdr agent prompt elicio "DONE review-r5 .reports/review-r5-report.md <final commit sha>"

Your turn must end with that push, including if the verdict is REJECT. If
you must stop for something outside yourself, push
`WAITING review-r5 <what>` instead. If you start a helper lane, close its
tab before you push.

## The worker reports, verbatim

### WP10 (lane w5)

````markdown
# WP10 Work Package Report: Research for Plan v2

**Package:** WP10 — Research for plan v2  
**Lane:** w5  
**Worktree:** `/home/user/projects/elicio/.worktrees/w5`  
**Branch:** `lane/w5`  
**Date:** 2026-09-17  
**Final Commit SHA:** `832ef2835fb1e76006b3177e5764c85060fdf77c`  

---

## 1. What Was Built

Created `docs/fab/L5-research-v2.md` satisfying all requirements of `tasks/WP10-research-v2.md` and `tasks/phase1-common.md`:

1.  **Section 1: Thin Cells ($\le 3.2\text{ mm}$ with Protection Circuit)**
    *   Found SparkFun `PRT-13852` / `PRT-25270` (`DTP301120`): bare cell $\le 3.0\text{ mm} \times 11.0\text{ mm} \times 20.0\text{ mm}$, protected assembly $\le 3.2\text{ mm} \times 11.5\text{ mm} \times 22.0\text{ mm}$, $40\text{ mAh}$, $7.14–$7.39 USD, in stock in single units at SparkFun and DigiKey (`1568-1498-ND`). Real engineering drawing verified (`SPE-00-301120-40mah-en-1.0ver.pdf`).
    *   Found PowerStream `GM201021-PCB` (`GMB 201021`): bare cell $\le 2.3\text{ mm} \times 10.5\text{ mm} \times 21.5\text{ mm}$, with PCB $\approx 3.0\text{ mm}$, $22\text{ mAh}$, $17.00 USD sample price. Real engineering drawing verified (`GMB201021-22mAh.pdf`).
    *   Found PowerStream `GM300910-PCB`: $3.0 \pm 0.2\text{ mm} \times 9.0 \pm 0.5\text{ mm} \times 10.0 \pm 1.0\text{ mm}$, $12\text{ mAh}$, $17.00 USD. Capacity below 20 mAh target.
    *   Documented DNK Power (`DNK301015`, 28 mAh) and LiPol Battery (`LP301016`, 25 mAh).
2.  **Section 2: Finishes for a Skin-Worn Part at JLC3DP**
    *   MJF PA12 and PA12S: media blasted, dyed black, vapor smoothing options. Quoted JLC3DP certification: meets ISO 10993 biocompatibility standards, certified for skin contact, sterilizable; lead time 2–4 business days.
    *   SLS nylon: porous surface warning quoted.
    *   SLA resin: JLC3DP explicit warning quoted that standard resins are not suitable for skin contact.
    *   Alternative vendor Xometry: MJF PA12 certified biocompatible (USP Class I-VI, FDA Intact Skin Surface Devices). AMT PostPro3D chemical vapor smoothing certified ISO 10993-5 (cytotoxicity) and ISO 10993-10 (skin irritation).
3.  **Section 3: The Board, Assembled Once (JLCPCB PCBA & LCSC Library)**
    *   Economic PCBA vs Standard PCBA: Economic is single-sided only ($8.18 setup fee, $1.53 stencil fee, $0 for basic parts, $3.00 for extended parts). Standard supports double-sided ($25.56/$51.12 setup, $8.21/$16.42 stencil, $3.00/feeder). Solder joints $\approx \$0.0016–\$0.003$ per joint. Min assembly qty 2 pieces.
    *   Base prototype 4-layer 20 × 16 mm board (5 pcs) starts at ~$2.00–$5.00 USD promotional tier (bare FR-4). Shipping: DHL, FedEx, UPS (3–7 days).
    *   Component library verified for 9 parts: TI ADS1292R (`C106679`/`C134015`, Extended, out of stock/intermittent, ~$8.50–$11.80), TI ADS1292 (`C134015`/`C2841443`, Extended, ~$6.50–$9.20), TI BQ25100 (`C527572`, Extended, in stock, ~$1.15–$1.45), TI TLV713 3.3V (`C90840`, Basic/Preferred, in stock >10,000, ~$0.18–$0.28), Raytac MDBT50Q-1MV2 (`C5142646`, Extended/Consigned, out of stock, ~$8.20–$10.50), Seeed XIAO nRF52840 (`102010448`, Consigned, $9.90–$10.38), Ebyte E73-2G4M08S1C (`C474779`, Extended, in stock, ~$4.80–$6.20), Fanstel BT840 (`BT840`, Extended/Consigned, out of stock), TI INA128 (`C7405`, Extended, in stock, ~$6.50–$8.20).
4.  **Section 4: The XIAO Route**
    *   Seeed Studio XIAO nRF52840 (`102010448`): $21.0 \times 17.5\text{ mm}$, PCB thickness 1.2 mm, total height with USB-C connector $4.3–4.5\text{ mm}$, weight ~4.0 g.
    *   Integrated TI BQ25100/1 charger (default 50 mA, pin P0.17 configurable to 100 mA), bottom `BAT+` and `BAT-` solder pads.
    *   Price and stock: $9.90 at Seeed, $10.38 at DigiKey, $10.89 at Mouser; fully in stock at all three distributors.
    *   Open-source support: public KiCad schematics, footprints, 3D models; upstream Zephyr (`seeed_xiao_nrf52840`) and Arduino support.
    *   Trade-off: carrier board eliminates RF/power design risk; trades off vertical height ($4.3–4.5\text{ mm}$ USB-C shell).
5.  **Section 5: Contact Hardware in Ones**
    *   Brass DIN 439 M2.5 thin nut: Bossard BN 147 at TME (`1159550`, $0.16/ea in 10pk, MOQ 10); Westfield Fasteners (£0.28, MOQ 1).
    *   Titanium ISO 7380 M2.5 × 4: Sortafast `SF-BH2504-10` ($17.50 / 10pk, $1.75/ea, MOQ 10, page live); Titane Services (3.57 €, MOQ 1).
    *   TE Connectivity 31428 ring lug: DigiKey (`31428`, $0.24, MOQ 1).
6.  **Section 6: Fit Without a Printed Gauge**
    *   Documented published 1:1 paper/card templates from HearSource, Signia, and Ear Gear.
    *   Included exactly two sentences on `docs/fab/cad/v1/drawing.pdf` 1:1 paper cutout suitability (checks chord length, hook curve, crease arc; cannot check 3D coronal bow clearance, mastoid bone contact, electrode skin pressure, or cartilage pinching).
7.  **Format Constraints:**
    *   Word count: 2,090 words (verified strictly under 2,500 words).
    *   Verbatim quotes, URLs, and dates read (2026-09-17) provided for all numbers, or tagged `UNVERIFIED`.

---

## 2. Acceptance Verification and Gates

### Gate 1: Test Suite
*   **Command:** `.venv/bin/python -m unittest discover -s tests -v`
*   **Result:** Ran 129 tests in 15.377s. **OK (skipped=22)**. 0 failures.

### Gate 2: Clean Git Working Tree
*   **Command:** `git status --short`
*   **Result:** Clean. Untracked file `.reports/WP10-report.md` is gitignored.

### Gate 3: Deliverable Commit
*   **Command:** `git log -1 --oneline`
*   **Result:** `832ef28 docs(fab): L5 research for plan v2`

---

## 3. What Was Not Done / UNVERIFIED Items

1.  **Vendor Purchasing, Carts, or Contact:**
    *   Zero purchase orders, cart actions, account signups, or vendor inquiries were initiated per safety instructions.
2.  **UNVERIFIED Items Cataloged:**
    *   `DNK301015` single-unit price / checkout: `UNVERIFIED` (search: "DNK301015 buy 1 piece online cart checkout"). Vendor requires business inquiry form with MOQ 100+.
    *   `LP301016` single-unit price / checkout: `UNVERIFIED` (search: "LP301016 buy single unit online"). Vendor requires inquiry form.
    *   JLC3DP static catalog price for 40 × 20 × 8 mm part: `UNVERIFIED` without CAD file upload (search: "JLC3DP static price table 40x20x8 mm part"). Dynamic pricing engine requires geometry upload.
    *   Xometry static catalog price for 40 × 20 × 8 mm part: `UNVERIFIED` without CAD file upload. Dynamic instant-quoting engine requires CAD geometry upload.

---

## 4. Needs a Decision for Plan v2

1.  **Primary Cell Selection:**
    *   *Option A (Recommended):* SparkFun `PRT-13852` / `PRT-25270` (`DTP301120`). Thickness is $\le 3.2\text{ mm}$ with PCM (bare cell $\le 3.0\text{ mm}$), delivers $40\text{ mAh}$ (almost double the $22\text{ mAh}$ of GM201021), costs $7.14 USD, and is fully stocked at SparkFun and DigiKey with verified engineering drawings. Length with PCM is 22.0 mm max (requires 22 mm longitudinal cavity length).
    *   *Option B:* PowerStream `GM201021-PCB`. $\approx 3.0\text{ mm}$ with PCB, $22\text{ mAh}$, $21.5\text{ mm}$ length, but sample unit cost is $17.00 USD.
2.  **MCU / Assembly Architecture:**
    *   *Option A (Carrier Board with Seeed XIAO nRF52840):* Solder the pre-assembled XIAO ($9.90, fully in stock) as a surface-mount daughterboard onto a 2-layer or 4-layer custom carrier PCB holding only the ADS1292 AFE. Lowest spin risk; requires accommodating $4.3–4.5\text{ mm}$ USB-C height.
    *   *Option B (Single Integrated Board via JLCPCB Standard PCBA):* Assemble bare nRF52840 module (`Ebyte E73-2G4M08S1C` or `MDBT50Q-1MV2`) directly on the main board. Lower profile ($\le 2.0\text{ mm}$), but higher RF layout risk and component availability hurdles at LCSC.
3.  **Shell 3D Print Finish:**
    *   *Option A (JLC3DP MJF PA12 / PA12S dyed black):* Lowest cost, ISO 10993 certified biocompatibility for skin contact.
    *   *Option B (Xometry MJF PA12 with PostPro3D chemical vapor smoothing):* Injection-molded cosmetic appearance, ISO 10993-5 cytotoxicity and ISO 10993-10 skin irritation certified.

---

## 5. Final Commit SHA

`832ef2835fb1e76006b3177e5764c85060fdf77c`
````

### WP11 (lane w1)

````markdown
# WP11 report — packing v2, turn 09 (fourth DONE)

Lane `w1`, branch `lane/w1`, package WP11. Coordinator note 4 / plan v2
turn 09: standoffs 3.0, 3.5 and 4.0; cell under the board only with
positive nominal clearance; board bends 0.5 onto the bosses; 0.5 floor
recess at 3.5 and 4.0 (web 1.0); cell carries no load; report module
stack and outer height. The plan file was not edited.

## What was built

864 runs (720 Interface I including recess variants, 144 Interface II).
Table and sources: `docs/fab/packing-v2.md`.

### DTP 3.2 + foam 0.3 = 3.5 under the board

| standoff | recess | nominal | deformed | under-board | load |
|---|---:|---:|---:|---|---|
| 3.0 | 0 | −0.5 | −1.0 | no | carries load |
| 3.5 | 0 | 0.0 | −0.5 | no | carries load |
| 4.0 | 0 | +0.5 | 0.0 | yes | carries load |
| 3.5 | 0.5 | +0.5 | 0.0 | yes | carries load |
| 4.0 | 0.5 | +1.0 | +0.5 | yes | no load |

Turn 09: 4.0 with no recess, deformed clearance 0.0. 3.5 with no recess, deformed −0.5.
Only DTP + 4.0 + recess 0.5 has positive deformed clearance. It still hits SIG1 (22 mm cell from s 1.5). 501015 packed 5.5 never has positive clearance.

### Module stack (standoff + board 1.0 + module) and outer at zero added clearance

Floor 1.5 + lid 1.0.

| arch | standoff | stack | outer0 |
|---|---:|---:|---:|
| A | 3.0 | 6.3 | 8.8 |
| A | 3.5 | 6.8 | 9.3 |
| A | 4.0 | 7.3 | 9.8 |
| B | 3.0 | 6.0 | 8.5 |
| B | 3.5 | 6.5 | 9.0 |
| B | 4.0 | 7.0 | 9.5 |

outer@lid in the run table is LID_Y + 1.0. Module-to-lid is packing, not a solid probe. C15 residual web is NOT_MEASURED.

Interface I: 0/720 close. Interface II: same four A 501015 series w20 closers. Stage B toml unchanged (`A_501015_series_w20_y8_iII_s3`).

## Gates

`.venv/bin/python -m unittest discover -s tests -v` — OK (full suite after 864 drawings). Order 1 identity and two consecutive Stage B still green from CadRegenTests / CadStageBV2BuildTests in that run.

## Needs a decision

1. Interface I still does not close: clearance/load, outer 9.3–9.8 on 3.5/4.0 for A, and DTP vs SIG1.
2. G5/G7 must still prove worst-case clearance to the deformed board. WP11 numbers are packing arithmetic.
3. C15 does not approve the 0.5 recess.
4. USB remains hook-end end face (fallback).

## Final commit sha

`7df78b5`
````

### WP13 (lane w4)

````markdown
# WP13 report — Firmware v2

Lane `w4`. Branch `lane/w4`. Final commit `28b284c1908760c946971ae1bd66f3c1feee4e70`.
Worktree `/home/user/projects/elicio/.worktrees/w4`.

Host-only. No hardware was programmed or measured.

## What was built

- `docs/fab/frame-v2.md`: versioned little-endian NUS fragment format (HELLO, STREAM, BATTERY), 16-bit `acq_index` (DRDY count, wrap 32.768 s), CRC-32/ISO-HDLC, fragment reassembly, overrun vs transport loss, reconnect, VBUS and undervoltage flags, nominal scale as metadata.
- `src/elicio/frame_v2.py`: Python framer, decoder, reassembler.
- `tests/test_frame_v2.py` and `tests/fixtures/frame_v2/`: golden bytes for normal, wrap, fragment, reorder, loss, overrun, partial, reconnect, bad CRC, version mismatch; Python vs clang native framer.
- `firmware/`: portable C framer, ADS1292 worn register set (2000 SPS, gain 12, internal 2.42 V, RLD on, lead-off off, non-R), undervoltage machine with `V_STOP_MV` / `V_START_MV` marked from WP12, Feather stand-in pin header, `elicio_stream` Arduino sketch (BLE NUS, MTU request 247, DRDY ring 256, battery every 10 s, VBUS refuses streaming, acquisition continues while disconnected).
- `docs/fab/firmware-v2.md`: build, flash, bootloader 0.11.0 URL (no download), flash map, USB identity, G4 tests, what was not run.
- `docs/fab/montage.md` §8: protocol v2 mapping table. Nothing above that heading was edited.

## Gates

1. `.venv/bin/python -m unittest discover -s tests -v`

   Result: exit 0. `Ran 142 tests in 15.102s` `OK (skipped=22)`. Skips are existing CAD/render tests that need build123d or matplotlib, not this package. All 13 `test_frame_v2` cases passed, including the native clang harness.

2. Target firmware compiles.

   Command (Adafruit gcc 9-2019q4, core default, Rosetta):

   ```bash
   arduino-cli compile --fqbn adafruit:nrf52:feather52840 \
     --library firmware \
     --output-dir /tmp/elicio-firmware-build \
     firmware/elicio_stream
   ```

   Result: exit 0. Sketch uses 133276 bytes (16 %) of 815104. Global variables 18472 bytes (7 %) of 237568.

   Same sketch with Arm GNU 15.3.1 (`compiler.path=/Applications/ArmGNUToolchain/15.3.rel1/arm-none-eabi/bin/`): exit 0, 125408 bytes (15 %), 18764 bytes RAM (7 %).

3. `git status --short` empty after the last commit.

## Plan v2 acceptance

- §11 row 13 "builds in CI; bench-tested at S2": no CI workflow exists in this repo. The host unittest and the two `arduino-cli compile` commands above are what ran. Bench at S2 was not run (no board).
- G6 (protocol v2 table): written as `montage.md` §8. 3.1–3.3 revised (same numbers on the ADS path, named filter and windows). 3.4 revised (dropout 200 sample intervals; ± 50 mV input-referred; transport loss beside dropout). 3.5–3.10 same criterion. Input and common-mode headroom: open: needs S2 data. Start-up exclusions named. No dry data was scored.
- G4 pieces this package owns (merged image identity, application layout, USB ids, update and recovery tests): documented in `firmware-v2.md`. Not executed on hardware.

## What was installed

| Item | How | Size |
|---|---|---|
| arduino-cli 1.5.1 | Homebrew | 25 MB |
| Adafruit nRF52 1.7.0 | `arduino-cli core install adafruit:nrf52` | 892 MB under `~/Library/Arduino15/packages/adafruit`; Arduino15 total 1.3 GB |
| Arm GNU Toolchain 15.3.rel1 | Homebrew cask `gcc-arm-embedded` | 1019 MB |
| `arm-none-eabi-gcc` 16.2.0 | Homebrew formula | 540 MB; unused (no newlib/libstdc++) |
| `arm-none-eabi-binutils` 2.47 | Homebrew formula | 19 MB |
| Rosetta 2 | `softwareupdate --install-rosetta --agree-to-license` | required for x86_64 ctags and Adafruit gcc 9 |

Q45 choice: Arduino-cli + Adafruit nRF52 core, not Zephyr. Reason: stand-in FQBN, `BLEUart` NUS, Adafruit UF2 bootloader either way, no Nordic account, smaller install. Zephyr/`west` was not installed.

## What was not done

No Feather, Debug Probe, Tag-Connect, ADS1292, cell, or BLE peer. pyOCD and OpenOCD were not installed. Bootloader 0.11.0 hex was not downloaded. First-load, UF2 update, double-press recovery, VBUS on a cable, 2000 SPS on air, and pack undervoltage were not run. Product pin map and computed V_STOP/V_START wait on WP12. Plan v2 §6 names Zephyr; this tree is Arduino.

A local unversioned `post-commit` hook ran `git push` after each commit on `lane/w4`. This lane did not invoke `git push`. The user rule was never push.

## Needs a decision

1. Plan v2 §6 says nRF Connect SDK (Zephyr). Q45 told this lane to choose Arduino or Zephyr. Arduino was chosen. Confirm or require a Zephyr port before S0.
2. `V_STOP_MV` 2700 and `V_START_MV` 2800 are placeholders (ADS1292 AVDD min, plus 100 mV). Replace with WP12's computed pack millivolts.
3. Feather USB identity and bootloader board id stand in for the product module. WP12's board needs its own 0.11.0 hex when that PCB exists.
4. Montage §8 input and common-mode headroom: open until S2 data.

## Final sha

`28b284c1908760c946971ae1bd66f3c1feee4e70`
````

### WP16 (lane w9)

````markdown
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
````

### WP17 (lane w5)

````markdown
# WP17 Work Package Report: Research v3 for the Build Rounds

**Package:** WP17 — Research v3 for the build rounds  
**Lane:** w5  
**Worktree:** `/home/user/projects/elicio/.worktrees/w5`  
**Branch:** `lane/w5`  
**Date:** 2026-09-17  
**Final Commit SHA:** `f395e70dee97cab5ffac3dfc9f6fb98f32c7a6d9`  

---

## 1. What Was Built

1.  **Updated `docs/fab/L5-research-v2.md`:**
    *   Corrected E73-2G4M08S1C LCSC part number to `C356849` (was C474779) and cited the re-read LCSC product page (`https://www.lcsc.com/product-detail/Bluetooth-Modules_C356849.html`).
    *   Corrected Seeed XIAO nRF52840 charge-current configuration pin to `P0.13` (was P0.17) and cited the re-read Seeed Studio Wiki documentation (`https://wiki.seeedstudio.com/XIAO_BLE/`).
    *   Committed at `c902ed0 docs(fab): fix E73 LCSC number and XIAO charge pin in L5 report`.
2.  **Created `docs/fab/L6-research-v3.md`:**
    *   **Section 1 (Cell harness, Gate G1b):**
        *   Documented discrepancy on SparkFun `PRT-25270`: product title/description states "Polymer Lithium Ion Battery - 40mAh (JST-SH)" with "standard 2-pin JST-SH connector", but linked Data Power engineering drawing `SPE-00-301120-40mah-en-1.0ver.pdf` page 9 labels "Connector: JST-PHR-2PIN", wire gauge "UL3302AWG#26", and lead length "100+/-3mm". JST-PH is 2.0 mm pitch; JST-SH is 1.0 mm pitch.
        *   Found in-stock JST SH and PH 2-pin receptacles at LCSC:
            *   JST SH (1.0 mm) SMT right-angle `SM02B-SRSS-TB(LF)(SN)`: LCSC `C160402`, 82,450 in stock, $0.133 USD.
            *   JST SH (1.0 mm) SMT vertical `BM02B-SRSS-TB(LF)(SN)`: LCSC `C694384`, 12,300 in stock, $0.145 USD.
            *   JST PH (2.0 mm) SMT vertical `B2B-PH-SM4-TB(LF)(SN)`: LCSC `C160352`, 6,820 in stock, $0.182 USD.
            *   JST PH (2.0 mm) SMT right-angle `S2B-PH-SM4-TB(LF)(SN)`: LCSC `C295747`, 4,150 in stock, $0.210 USD.
            *   JST PH (2.0 mm) THT vertical `B2B-PH-K-S(LF)(SN)`: LCSC `C131337`, 54,200 in stock, $0.068 USD.
    *   **Section 2 (Standoffs, Claim C14):**
        *   Harwin `R25-1000402`: DigiKey `952-2175-ND` (3,847 in stock, $0.57 at 1, $0.478 at 10, hex 5.00 mm / 0.197"); Mouser `855-R25-1000402` (in stock, $0.41 at 1, $0.319 at 10, hex 4.9 mm).
        *   Inspected Harwin manufacturer drawing `R25-100XX02` / `DRG-01991`: hex "5.00 A/F MAX", length $L_1 = 4.00 \pm 0.10\text{ mm}$, material "CW614N brass", finish "NICKEL". The drawing does not state a numerical nickel plating thickness. There is no dedicated top-face flatness or perpendicularity tolerance (governed by general ±5° angular and ±0.10 mm length tolerance).
        *   Spacer Express `LAI-FF-M2.5-SW5-L3-100` (€91.08 ex VAT per 100): shipping to USA is `UNVERIFIED` on public pages without account checkout.
        *   Searched across all major distributors for a stocked 3.5 mm M2.5 female brass hex standoff (5 mm across flats): `UNVERIFIED` / NONE FOUND (standard metric lengths jump 3.0 to 4.0 mm).
    *   **Section 3 (Contact alternatives, Claim C16, Research Only):**
        *   Tabulated Harwin `S1791-42R` (free 4.0 mm, working 3.0 mm, travel 1.0 mm, force 1.00 N, gold plating, DigiKey 4,210 in stock), Harwin `S1751-46R` (free 3.5 mm, working 2.5–3.0 mm, force 0.85 N), Harwin `S7121-42R` (free 1.7 mm, working 1.5 mm, force 0.70 N, DigiKey 8,100 in stock).
        *   Tabulated Würth `WE-SECF` (331031321515 and 331011452020: working heights 1.1–1.7 mm, forces 0.65–0.80 N, CuBe gold plated, in stock at DigiKey).
    *   **Section 4 (Assembler facts, Gates G3 and G8):**
        *   JLCPCB Standard PCBA: min assembled qty 2 pcs; min board size 70 × 70 mm (rails required if smaller).
        *   Stackup JLC7628 / JLC2313 for 4-layer 1.0 mm ENIG: 1 oz outer, 0.5 oz inner, 7628 prepreg, ±10% thickness tolerance.
        *   Component library status: TI ADS1292IRSMR (`C2841443`/`C134015`, Extended, ~$6.50–$9.20), TI BQ25100 (`C527572`, Extended, in stock, ~$1.15–$1.45), TI TLV71333 (`C90840`, Basic, in stock, ~$0.18–$0.28), Raytac MDBT50Q-1MV2 (`C5142646`, Extended/Consigned, out of stock), Ebyte E73-2G4M08S1C (`C356849`, Extended, in stock, ~$4.80–$6.20).
        *   Programming service: performed after soldering; fee structure is "$7.86 engineering fee plus $7.86 per hour of labor". Fixed published price per board is `UNVERIFIED`.
        *   DDP tariff FAQ: duties collected at checkout, refunded or adjusted if rate discrepancy > ±10% and impact > $10 USD.
        *   US alternatives: MacroFab (instant online quoting, North American facilities, 10 days to 5 weeks), Screaming Circuits (quick-turn 10/20-day assembly, online multiline quotes), OSH Park ($10/sq inch 4-layer prototype, bare boards only, hand assembly).
    *   **Section 5 (Shell finish, Claim C1):**
        *   JLC3DP MJF PA12: grey, dyed black, chemical vapor smoothing. Quoted skin statements: meets ISO 10993 biocompatibility, certified for skin contact, sterilizable. Prices dynamic per geometry, static price `UNVERIFIED` without upload.
        *   Xometry: MJF PA12 with PostPro3D chemical vapor smoothing certified USP Class I-VI, passed ISO 10993-5 (cytotoxicity) and ISO 10993-10 (skin irritation).
    *   **Section 6 (First load, Gate G4):**
        *   Raspberry Pi Debug Probe: nominal 3.3 V I/O, no active level shifters, 0.0 V to 3.63 V target limit, connect GND first warning quoted.
        *   Tag-Connect TC2030-IDC-NL: 6-pin "No Legs" Plug-of-Nails™, 1.27 mm pitch, 0.78–0.80 mm pads, three 0.99 mm alignment pin holes, no solder paste rule quoted.
        *   Adafruit nRF52840 bootloader: double-reset entering DFU within 500 ms window via magic token at `0x20007F7C`; custom boards configured in `src/boards/<name>/` via `board.h`.
    *   **Section 7 (Materials, Requirement R3):**
        *   Sortafast Grade 5 Titanium M2.5 × 4 ISO 7380 button head screws: $17.50 for 10-pack ($1.75/ea), in stock. Alternative: Titane Services (France) at 3.57 €/ea, in stock.
        *   HP PA12 MJF material page: quoted "HP 3D High Reusability (HR) PA 12, enabled by Evonik, meets USP Class I-VI standards and U.S. FDA guidance for Intact Skin Surface Devices regarding biocompatibility" (tested per ISO 10993-5 and ISO 10993-10).

---

## 2. Acceptance Verification and Gates

### Gate 1: Test Suite
*   **Command:** `.venv/bin/python -m unittest discover -s tests -v`
*   **Result:** Ran 129 tests in 15.547s. **OK (skipped=22)**. 0 failures.

### Gate 2: Clean Git Working Tree
*   **Command:** `git status --short`
*   **Result:** Clean. Untracked file `.reports/WP17-report.md` is gitignored.

### Gate 3: Commit History on `lane/w5`
*   `c902ed0 docs(fab): fix E73 LCSC number and XIAO charge pin in L5 report`
*   `f395e70 research(v3): facts for the build rounds`

---

## 3. What Stayed UNVERIFIED

1.  **Spacer Express US Shipping:** `UNVERIFIED` on public storefront without customer checkout/account.
2.  **3.5 mm M2.5 Female Brass Hex Standoff (5 mm A/F):** `UNVERIFIED` / NONE FOUND across distributor catalogs (commercial standards are 3.0 mm and 4.0 mm).
3.  **JLCPCB Fixed Per-Board Programming Cost:** `UNVERIFIED` as a static per-unit catalog price (FAQ specifies $7.86 setup + $7.86/hour labor).
4.  **JLC3DP / Xometry Static Shell Price Tables:** `UNVERIFIED` without CAD file upload due to dynamic geometry-based quoting engines.
5.  **MacroFab / Screaming Circuits Static Assembly Price Tables:** `UNVERIFIED` without CAD/BOM upload.

---

## 4. Needs a Decision for Plan v2 Build Rounds

1.  **Standoff Height Freeze (3.0 mm vs. 4.0 mm):**
    *   Since 3.5 mm standoffs are non-standard and unavailable off-the-shelf, Plan v2 must select either 3.0 mm (`Spacer Express LAI-FF-M2.5-SW5-L3-100`, if EU shipment is arranged) or 4.0 mm (`Harwin R25-1000402`, stocked at DigiKey and Mouser in thousands).
2.  **Battery Connector Freeze (Gate G1b):**
    *   SparkFun's PRT-25270 product page text claims "JST-SH", but the linked Data Power engineering drawing specifies "JST-PHR-2PIN" (2.0 mm pitch, 26 AWG). If PRT-25270 physically arrives with JST-SH (1.0 mm), board layout needs LCSC `C160402`; if it arrives with JST-PH (2.0 mm), it needs LCSC `C160352`. S0 board design should include dual footprints or confirm physical pack samples.
3.  **Radio Module Selection (Raytac vs. Ebyte):**
    *   Ebyte `E73-2G4M08S1C` is in stock at LCSC (`C356849`, Extended part, ~$4.80–$6.20). Raytac `MDBT50Q-1MV2` is out of stock in JLCPCB's immediate library, requiring Global Sourcing or consignment.

---

## 5. Final Commit SHA

`f395e70dee97cab5ffac3dfc9f6fb98f32c7a6d9`
````

### WP12 (lane w2, both turns)

````markdown
# WP12 report — Board v2 (lane w2)

Worktree: `/home/user/projects/elicio/.worktrees/w2`
Branch: `lane/w2`
Package: WP12 (coordinator follow-up: interface II)
Date: 2026-09-17

## What was built

First pass (HEAD was `9fa31d2`): schematic, 4-layer 17 × 33 mm interface I, release job, G2/G4.

This follow-up, after WP11 `lane/w1` `43a982a` `docs/fab/packing-v2.md`:

- PCB is now a **2-layer FPC**, PI 0.11 mm, FR4 stiffener 0.3 mm under parts (Eco1.User) and 0.2 mm at the three tabs (Eco2.User).
- Outline and part centres from winner **`A_501015_series_w20`** (`packing-v2.md` §4–§5). USB-C on the hook-end end face.
- Three flex tabs, ring pad Ø5.0 / hole Ø2.7, ENIG, clamped under the brass standoff. Footprint `elicio:RING_PAD_D5_H2.7`.
- Interface I 8 × 8 B.Cu pads recorded as the rejected candidate in `docs/fab/board-v2.md` §11a. Reason: I closes 0 runs at the anatomical sites (coordinator 0/288; packing §2: 720 I runs, none close). Cell under the board hits SIG1; neither cell fits under 3.0 or 3.5 mm with the load rule.
- Schematic contract unchanged (nets, values, G2/G4). P1–P3 still `elicio:PAD_8x8` symbols; footprint is the ring.
- JLC FPC capabilities, coverlay, stiffener list, flex fixture fee, and FPC assembly acceptance quoted in `board-v2.md`. No request, no upload, no quote.
- `scripts/board/release.py` gerbers are F.Cu/B.Cu plus Eco/Dwgs/Cmts (stiffener and bend notes). No inner layers.

Nothing ordered, quoted or uploaded. No vendor contact.

## WP11 numbers used

From `git show lane/w1:docs/fab/packing-v2.md` (report file is untracked).

- Closer: Raytac MDBT50Q-1MV2, 501015 series, width 20, standoff 3.0, LID_Y 7.0–9.0 (8.0 with order-1 foam).
- Hand-off layout: `A_501015_series_w20_y7_iII_s3` with Stage B using y8 for foam 0.5.
- USB-C hook-end end face (plan v2 §5.4 fallback).

## Install

Unchanged from the first pass: KiCad 10.0.6, `kicad-cli`, cask about 5.5 GB, 57 s.

## Gates

### 1. Unittest

```text
.venv/bin/python -m unittest tests.test_board_release -v
```

Result: **OK** (2 tests). ERC 0. BOM rows = placed parts = 59.

```text
.venv/bin/python -m unittest discover -s tests -v
```

Result: 131 tests, **13 FAIL**, all `test_cad.CadRegenTests` v1 solid hashes (`body_full_p15`, `body_full_p25`, `body_thin_p15`, `lid`). This lane did not edit CAD. Same 13 as the first WP12 close-out.

### 2. Release job

```text
.venv/bin/python scripts/board/release.py
```

| Field | Value |
|---|---|
| erc_errors | 0 |
| erc_warnings | 13 (same extends/lib warnings as before) |
| drc_errors | 893 |
| drc_warnings | 33 |
| unconnected_items | 0 |
| bom_rows | 59 |
| placed_parts | 59 |
| exit | 0 |

Gerbers include User_Eco1, User_Eco2, User_Drawings, User_Comments. No In1/In2.

### 3. git status at DONE

Must be empty of owned files after the commit. `.reports/WP12-report.md` is gitignored.

## What was not done

- Layout routing.
- Folded-tab solid (SIG1/SIG2 Gerber rings are unfolded; packing XY is the folded site).
- Factory programming quote (G4 quote-only, Rolf).
- Live re-open of every 0402 LCSC stock page at close-out.
- Confirmation of E73-2G4M08S1C and YFP0006 lands against the drawings.
- Physical G2 leakage measurement.
- Any JLC order, cart, quote, or upload.

## Needs a decision

See `docs/fab/board-v2.md` §19. Short list: G1b JST-SH vs PH plus 501015 harness 100 ± 3 mm; JLC FR4 has no 0.3 mm (WP11 assumed 0.3); six stiffener pieces vs extra-fee at ≥4; SW1 vs 2.5 mm assembly edge; SIG1/SIG2 unfold vs packing XY; ISET LED; system load vs 2 mA termination; Debug Probe at 3.0 V; E73/YFP lands; no BAV199; BQ25100 stock; protective ADC cadence.

## Final commit sha

`a4080c23e738237d6234e1736e2f0e43d22c1f43` (`board(v2): flex layout for interface II from WP11 winner`)

A repository post-commit hook pushed `lane/w2` to origin after the commit. This lane did not run `git push`. The package brief said never push.
````
