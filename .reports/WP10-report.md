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
