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
