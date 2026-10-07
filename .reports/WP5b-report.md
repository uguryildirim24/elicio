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
