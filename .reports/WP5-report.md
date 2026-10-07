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
