# Delivered-spend ledger v2

Delivered-spend ledger for plan v2 §9 and whole-project gate (R8, G8), updated for the v4 board and the current shell.
Destination: Massachusetts, USA.
Read date for all current live queries: 2026-09-24.
No agent buys, quotes, uploads files, or contacts any vendor. Every figure here is catalogue-quoted from a public page with URL and read date, or marked UNVERIFIED with a documented range and rationale.

Columns: item; quantity; status (`quoted` / `catalogue` / `allowance` / `UNVERIFIED`); unit price as displayed on cited page; source URL and read date; shipping; tax; import collection / tariffs; delivered line total.

## 1. Trade Remedies, Tariffs, and Import Rules (China to Massachusetts)

1. **De Minimis Status (Section 321):**
   - The U.S. duty-free de minimis exemption ($800 threshold under 19 U.S.C. § 1321) has been suspended for China-origin shipments subject to Section 301 trade remedies under executive orders and CBP regulations.
   - Source: U.S. Customs and Border Protection (CBP), E-Commerce Trade Guidance: https://www.cbp.gov/trade/basic-import-export/e-commerce , read 2026-09-24 ("CBP published interim final rules suspending the de minimis exemption for international mail and setting new requirements for collecting duties on mail shipments"); Federal Register Notice portal: https://www.federalregister.gov/ , read 2026-09-24.
   - Consequence: All shipments from China, regardless of declared value, must undergo formal/informal entry with 10-digit HTSUS classification and payment of duties.

2. **Section 301 Tariffs on PCBAs and 3D Printed Parts:**
   - **PCBA / Circuit Boards (HTS 8534.00.00 / 8543.70 / 8517.62):** 25.0% ad valorem duty under Section 301 (List 1 / List 2). Source: Office of the United States Trade Representative (USTR) Tariff Actions: https://ustr.gov/issue-areas/enforcement/section-301-investigations/tariff-actions , read 2026-09-24; confirmed pre-collected under JLCPCB DDP terms in JLCPCB U.S. Tariff Policy FAQ: https://jlcpcb.com/help/article/u-s-tariff-policy-faq , read 2026-09-24.
   - **3D Printed PA12 Plastic Parts (HTS 3926.90.9985):** 25.0% ad valorem duty under Section 301 (List 3). Source: Office of the United States Trade Representative (USTR) Tariff Actions: https://ustr.gov/issue-areas/enforcement/section-301-investigations/tariff-actions , read 2026-09-24.
   - **Trade Remedy Duty Reserve (CBP CSMS #69326983 and HTSUS 9903.05.31):** Marked `UNVERIFIED: range 0.0% to 12.5% ad valorem`. The direct message text for CSMS #69326983 cannot be retrieved via public HTTP on https://www.cbp.gov/trade/automated/cargo-systems-messaging-service (checked 2026-09-24). Standard DDP clearance pre-collects only the 25.0% Section 301 rate ($0.00 additional reserve). A 12.5% duty reserve is included in the high scenario ($34.32 for PCBA, $0.96 for shell).

3. **Carrier Brokerage & Disbursement Fees:**
   - **JLCPCB Global Standard Direct Line (DDP):** Pre-collects the 25% Section 301 tariff and customs clearance fee at checkout, avoiding separate carrier disbursement fees. Source: https://jlcpcb.com/help/article/u-s-tariff-policy-faq , read 2026-09-24.
   - **DHL Express:** $17.00 minimum disbursement fee (or 2% of advanced duties/taxes). Source: https://www.dhl.com , read 2026-09-24.
   - **FedEx Express:** $13.50 minimum advancement fee (or 2%). Source: https://www.fedex.com , read 2026-09-24.

4. **Massachusetts Sales and Use Tax:**
   - 6.25% ad valorem use tax under Massachusetts General Laws (M.G.L. c. 64H, § 2 and c. 64I, § 2) on tangible personal property for storage, use, or consumption in Massachusetts where sales tax was not collected by the seller.
   - Source: Massachusetts Department of Revenue Sales and Use Tax Guide: https://www.mass.gov/guides/sales-and-use-tax , read 2026-09-24.

---

## 2. Order 1 — Board Fabrication and Assembly (JLCPCB, China)

Contents: 5 assembled flex boards, 2-layer polyimide (0.11 mm finished), ENIG finish, 6 FR4 0.2 mm stiffeners, two-sided standard PCBA assembly, flex carrier fixtures, stencils, SMT joint soldering, extended part setup fees, 24 BOM part lines supplied by JLC, consignment handling, and courier shipping to Massachusetts.

### 2.1 JLCPCB Fabrication and Assembly Charges

| Item | Quantity | Status | Unit price as displayed | Source URL and date | Shipping | Tax | Import collection | Delivered line total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2-layer polyimide flex PCB, 0.11 mm, ENIG, 5 pcs | 5 | UNVERIFIED | range $15.00 – $25.00 (likely $20.00; dynamic Gerber quote) | https://jlcpcb.com/capabilities/flex-pcb-capabilities , read 2026-09-24 | part of parcel | — | 25% DDP: $5.00 | $20.00 – $30.00 (likely $25.00) |
| FPC extra-stiffener fee (≥4 stiffeners; v4 board has 6) | 1 order | UNVERIFIED | range $8.14 – $16.00 (likely $8.14; engineering quote) | https://jlcpcb.com/help/article/fpc-extra-charges , read 2026-09-24 | part of parcel | — | 25% DDP: $2.04 | $10.18 – $20.00 (likely $10.18) |
| Standard PCBA setup, two sides | 1 order | catalogue | $51.12 ($25.56 per side × 2) | https://jlcpcb.com/help/article/pcb-assembly-price , read 2026-09-24 | part of parcel | — | 25% DDP: $12.78 | $63.90 |
| SMT stencils, two sides | 1 order | catalogue | $16.42 ($8.21 per side × 2) | https://jlcpcb.com/help/article/pcb-assembly-price , read 2026-09-24 | part of parcel | — | 25% DDP: $4.11 | $20.53 |
| Flex SMT carrier fixtures (1–29 pcs requires 2) | 2 | catalogue | $24.63 each ($49.25 for 2 fixtures) | https://jlcpcb.com/help/article/pcb-assembly-price , read 2026-09-24 | part of parcel | — | 25% DDP: $12.31 | $61.56 |
| SMT solder joint fees (~350 SMD joints × 5 boards) | 1,750 joints | catalogue | $0.0016 per joint ($2.80 total) | https://jlcpcb.com/help/article/pcb-assembly-price , read 2026-09-24 | part of parcel | — | 25% DDP: $0.70 | $3.50 |
| Hand / wave soldering labor fee (J3 3-pin THT header × 5) | 1 order | catalogue | $3.58 labor + $0.017/joint × 15 ($3.83 total) | https://jlcpcb.com/help/article/pcb-assembly-price , read 2026-09-24 | part of parcel | — | 25% DDP: $0.96 | $4.79 |
| Extended part setup fees (23 unique extended lines) | 23 lines | catalogue | $3.00 per extended line ($69.00 total; range $54.00–$69.00) | https://jlcpcb.com/help/article/358-PCBA-Capabilities-Instructions , read 2026-09-24; https://jlcpcb.com/help/article/pcb-assembly-price , read 2026-09-24 | part of parcel | — | 25% DDP: $17.25 | $86.25 |
| JLC Overseas Consignment Handling Fee | 1 order | catalogue | $10.00 (2% declared value, minimum $10 per shipment) | https://jlcpcb.com/help/article/358-PCBA-Capabilities-Instructions , read 2026-09-24 | part of parcel | — | 25% DDP: $2.50 | $12.50 |

### 2.2 BOM Lines Supplied by JLCPCB / LCSC (5 boards)

The v4 BOM has 58 total component positions across 27 unique parts (`hardware/board/v4_parts.py`, `docs/fab/board-v4-design.md` §2 and §10).
3 parts (U1, U5, J2) are consigned in Order 2. The remaining 24 unique parts (55 positions) are assembled by JLCPCB.
In the v4 parts table (`docs/fab/board-v4-design.md` §2), only **C15525 (10 µF 0402)** is marked `(Basic)`. The remaining **23 unique lines are extended parts** ($69.00 total setup).
U2 (ADS1292IRSMT) is listed strictly as **C89288** ($6.50; C134015 was rejected in `docs/fab/board-v2.md` §13 as an RS-485 transceiver).

| BOM Item | Refs & Footprint | Qty (5 bds) | Status | Unit price as displayed | Source URL and read date | Extended Fee | Total Parts Cost |
| --- | --- | ---: | --- | ---: | --- | ---: | ---: |
| U2 ADS1292IRSMT | U2 (RSM-32) | 5 | catalogue | $6.50 (C89288, qty 1–10) | https://jlcpcb.com/partdetail/C89288 , 2026-09-24 | $3.00 (in §2.1) | $32.50 |
| U3 BQ25100YFPR | U3 (DSBGA-6) | 5 | catalogue | $1.35 (C527572, qty 1) | https://jlcpcb.com/partdetail/C527572 , 2026-09-24 | $3.00 (in §2.1) | $6.75 |
| U4 TLV71330PDQNT | U4 (X2SON-4) | 5 | catalogue | $0.23 (C3071062, qty 1) | https://jlcpcb.com/partdetail/C3071062 , 2026-09-24 | $3.00 (in §2.1) | $1.15 |
| Q1 WPM3027-3/TR | Q1 (DFN1006-3) | 5 | catalogue | $0.05 (C240195, qty 1) | https://jlcpcb.com/partdetail/C240195 , 2026-09-24 | $3.00 (in §2.1) | $0.25 |
| Q2–Q4 NMOS (DFN1006-3) | Q2, Q3, Q4 (DFN1006-3) | 15 | UNVERIFIED | $0.0744 (CJBB3134K C504102; range $0.05–$0.10) | https://www.lcsc.com/product-detail/C504102.html , 2026-09-24 | $3.00 (in §2.1) | $1.12 |
| D1 PESD5V0L1UL | D1 (SOD-523) | 5 | catalogue | $0.03 (C24109, qty 1) | https://jlcpcb.com/partdetail/C24109 , 2026-09-24 | $3.00 (in §2.1) | $0.15 |
| D2 LED 0402 Green | D2 (0402 LED) | 5 | catalogue | $0.02 (C72043, qty 1) | https://jlcpcb.com/partdetail/C72043 , 2026-09-24 | $3.00 (in §2.1) | $0.10 |
| J3 HDR-3-RA | J3 (1×3 2.54mm RA) | 5 | catalogue | $0.08 (C49257, qty 1) | https://jlcpcb.com/partdetail/C49257 , 2026-09-24 | $3.00 (in §2.1) | $0.40 |
| SW1 HRO 1TS015A | SW1 (3.0×2.0×0.6) | 5 | catalogue | $0.12 (C398746, qty 1) | https://jlcpcb.com/partdetail/C398746 , 2026-09-24 | $3.00 (in §2.1) | $0.60 |
| R1–R3, R31–R33 (220 kΩ 0402 1%) | R1–R3, R31–R33 | 30 | catalogue | $0.002 (C881401, 0402) | https://jlcpcb.com/partdetail/C881401 , 2026-09-24 | $3.00 (in §2.1) | $0.06 |
| R4, R17, R20, R21 (1 MΩ 0201 1%) | R4, R17, R20, R21 | 20 | catalogue | $0.003 (C473482, 0201WMF1004TEE) | https://jlcpcb.com/partdetail/C473482 , 2026-09-24 | $3.00 (in §2.1) | $0.06 |
| R5–R8, R13, R25, R27, R28 (10 kΩ 0201 1%) | R5–R8, R13, R25, R27, R28 | 40 | catalogue | $0.003 (C473048, 0201WMF1002TEE) | https://jlcpcb.com/partdetail/C473048 , 2026-09-24 | $3.00 (in §2.1) | $0.12 |
| R11 (6.8 kΩ 0201 1%) | R11 | 5 | catalogue | $0.012 (C4104700, ERJ-1GNF6801C) | https://jlcpcb.com/partdetail/C4104700 , 2026-09-24 | $3.00 (in §2.1) | $0.06 |
| R12 (6.04 kΩ 0201 1%) | R12 | 5 | catalogue | $0.005 (C270341, 0201WMF6041TEE) | https://jlcpcb.com/partdetail/C270341 , 2026-09-24 | $3.00 (in §2.1) | $0.03 |
| R14–R16, R23, R24 (100 kΩ 0201 1%) | R14–R16, R23, R24 | 25 | catalogue | $0.003 (C270364, 0201WMF1003TEE) | https://jlcpcb.com/partdetail/C270364 , 2026-09-24 | $3.00 (in §2.1) | $0.08 |
| R18 (47 kΩ 0201 1%) | R18 | 5 | UNVERIFIED | $0.004 (code unverified in v4 table; Uni-Royal 0201) | https://jlcpcb.com/capabilities/pcb-assembly-capabilities , 2026-09-24 | $3.00 (in §2.1) | $0.02 |
| R19 (27 kΩ 0201 1%) | R19 | 5 | UNVERIFIED | $0.004 (code unverified in v4 table; Uni-Royal 0201) | https://jlcpcb.com/capabilities/pcb-assembly-capabilities , 2026-09-24 | $3.00 (in §2.1) | $0.02 |
| R22 (1 kΩ 0201 1%) | R22 | 5 | catalogue | $0.003 (C270365, 0201WMF1001TEE) | https://jlcpcb.com/partdetail/C270365 , 2026-09-24 | $3.00 (in §2.1) | $0.02 |
| C1 (1.5 nF 0201 50V) | C1 | 5 | catalogue | $0.008 (C285104, 0201B152K500NT) | https://jlcpcb.com/partdetail/C285104 , 2026-09-24 | $3.00 (in §2.1) | $0.04 |
| C2 (10 nF 0201 50V) | C2 | 5 | catalogue | $0.004 (C43380, 0201B103K500NT) | https://jlcpcb.com/partdetail/C43380 , 2026-09-24 | $3.00 (in §2.1) | $0.02 |
| C3–C5, C10, C13, C16 (1 µF 0201 6.3V) | C3–C5, C10, C13, C16 | 30 | catalogue | $0.015 (C5142566, TCC0201X5R105K6R3ZT) | https://jlcpcb.com/partdetail/C5142566 , 2026-09-24 | $3.00 (in §2.1) | $0.45 |
| C6, C8, C9 (10 µF 0402 6.3V) | C6, C8, C9 | 15 | catalogue | $0.015 (C15525, CL05A106MQ5NUNC; Basic) | https://jlcpcb.com/partdetail/C15525 , 2026-09-24 | $0.00 (Basic) | $0.23 |
| C7, C11, C12, C15 (100 nF 0201 10V) | C7, C11, C12, C15 | 20 | catalogue | $0.003 (C307380, CL03A104KO3NNNC) | https://jlcpcb.com/partdetail/C307380 , 2026-09-24 | $3.00 (in §2.1) | $0.06 |
| C14 (4.7 µF 0402 10V) | C14 | 5 | UNVERIFIED | $0.0171 (code unverified in v4 table; Samsung CL05A475) | https://jlcpcb.com/capabilities/pcb-assembly-capabilities , 2026-09-24 | $3.00 (in §2.1) | $0.09 |
| **Subtotal JLC Components** | **55 positions** | **5 boards** | **catalogue / UNVERIFIED** | — | — | — | **$44.38** |

### 2.3 Shipping, Import, and Order 1 Delivered Total

| Item | Route | Status | Amount | Source URL and read date | Delivered line total |
| --- | --- | --- | ---: | --- | ---: |
| Shipping: Consigned parts from US to JLCPCB (Shenzhen, China) | Mouser / DigiKey direct to JLC warehouse (or USPS Int'l Priority forward) | UNVERIFIED | range $20.00 – $45.00 (likely $30.00) | https://www.mouser.com/services/shippingrates , read 2026-09-24; USPS International Priority Flat Rate Envelope, https://postcalc.usps.com , read 2026-09-24 | $20.00 – $45.00 (likely $30.00) |
| Shipping: Assembled boards from JLCPCB to Massachusetts | JLCPCB Global Standard Direct Line (DDP) / DHL Express | UNVERIFIED | range $16.00 – $36.00 (likely $22.00 DDP / $35.00 Express) | https://jlcpcb.com/help/article/shipping-methods , read 2026-09-24 | $16.00 – $36.00 (likely $22.00) |
| Section 301 Tariff on PCBA (HTS 8534.00 / 8543 / 8517) | 25.0% ad valorem tariff (DDP advance collection on ~$255–$287 export value) | legal rate / catalogue | $63.65 – $71.86 (likely $68.65) | https://ustr.gov/issue-areas/enforcement/section-301-investigations/tariff-actions , read 2026-09-24; https://jlcpcb.com/help/article/u-s-tariff-policy-faq , read 2026-09-24 | $63.65 – $71.86 (likely $68.65) |
| Trade Remedy Reserve (CBP CSMS #69326983 HTSUS 9903.05.31) | 0.0% to 12.5% ad valorem duty reserve | UNVERIFIED | range 0.0% ($0.00) to 12.5% ($34.32) | UNVERIFIED: CSMS text not public via HTTP; range shown in totals | $0.00 – $34.32 (likely $0.00 DDP) |
| Massachusetts Use Tax (6.25%) | 6.25% where not collected | legal rate | $16.00 – $18.50 (likely $17.50) | M.G.L. c. 64I, § 2, https://www.mass.gov/guides/sales-and-use-tax , read 2026-09-24 | $16.00 – $18.50 (likely $17.50) |
| **Order 1 Delivered Total (China route, 5 assembled boards)** | **JLCPCB DDP Route** | **catalogue + quote + UNVERIFIED** | — | — | **Low: $372.00 / Likely: $413.00 / High: $495.00** |
| *US Route Comparison: MacroFab / Screaming Circuits* | *US domestic quick-turn flex PCBA* | *quoted estimate* | *$1,200.00 – $1,800.00* | *Plan v2 §9; Screaming Circuits quick-turn flex minimum, https://www.screamingcircuits.com , read 2026-09-24. US route is ~4× higher.* | *Unviable ($1,200+)* |

---

## 3. Order 2 — Consigned Parts (Mouser / DigiKey)

Contents: Customer-supplied components not stocked in the JLCPCB parts library, purchased in the US and consigned to JLCPCB in Shenzhen, China. Quantities include assembly attrition / spare units (6 units for U1, 10 units for U5 and J2).

| Item | MPN / Description | Quantity | Status | Unit price as displayed | Source URL and read date | Shipping | Tax | Delivered line total |
| --- | --- | ---: | --- | ---: | --- | ---: | ---: | ---: |
| U1 Insight SiP BLE module | ISP1807-LR-RS (nRF52840, LGA) | 6 (5 bd + 1 spare) | catalogue | $13.65 (qty 1) | https://www.mouser.com/ProductDetail/Insight-SiP/ISP1807-LR-RS , read 2026-09-24 | included ($0 on >$50) | MA 6.25%: $5.12 | $87.02 |
| U5 TI Nanopower LDO | TPS7A0230PDQNR (X2SON-4) | 10 (cut tape) | catalogue | $0.62 (qty 10; $0.84 at 1) | https://www.digikey.com/en/products/detail/texas-instruments/TPS7A0230PDQNR/9995577 , read 2026-09-24 | $0.00 (combined) | MA 6.25%: $0.39 | $6.59 |
| J2 Molex Pico-EZmate Slim Header | 202656-0021 (SMD, vertical) | 10 (cut tape) | catalogue / UNVERIFIED | $0.75 ($0.66–$1.30 range; EOL, distributor stock / broker) | https://www.digikey.com/en/products/detail/molex/2026560021/9859586 , read 2026-09-24; https://www.mouser.com/ProductDetail/Molex/202656-0021 , read 2026-09-24 | $0.00 (combined) | MA 6.25%: $0.47 | $7.97 |
| Domestic shipping to Rolf (if consolidated) | FedEx Ground / USPS Ground Advantage | 1 parcel | catalogue | $0.00 – $7.99 (Free on Mouser orders ≥$50) | https://www.mouser.com/services/shippingrates , read 2026-09-24 | — | — | $0.00 |
| **Order 2 Delivered Total (Consigned parts)** | — | — | **catalogue** | — | — | — | — | **Low: $87.00 / Likely: $95.00 / High: $105.00** |

---

## 4. Order 3 — Shell 3D Print (PA12 MJF, Body + Lid + Spare Lid)

Contents: Behind-the-ear wearable shell on packing §5d (22 mm wide, LID_Y 8.0 mm, thickness 9.0 mm, chord 47.90 mm). Geometry from `docs/fab/cad/v2/manifest.json`:
- Body solid (`body_full_p15.stl`): volume 4,357 mm³ (4.36 cm³), mass ~4.40 g, bounding box 46.8 × 9.7 × 67.3 mm.
- Lid solid (`lid.stl`): volume 1,749 mm³ (1.75 cm³), mass ~1.77 g, bounding box 24.8 × 3.2 × 56.1 mm.
- Total quantity: 1 Body + 2 Lids (1 primary + 1 spare lid). Combined volume: 7,855 mm³ (7.86 cm³), combined mass: ~7.93 g.

### 4.1 China Route: JLC3DP

| Item | Quantity | Status | Unit price as displayed | Source URL and read date | Shipping | Tax | Import collection | Delivered line total |
| --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: |
| MJF PA12 Body (4.36 cm³) | 1 | catalogue | $1.21 ($0.275/g at 4.40 g; $1.00 min) | https://jlc3dp.com/help/article/pa12-hp-nylon , read 2026-09-24 | part of parcel | — | 25% tariff: $0.30 | $1.51 |
| MJF PA12 Lids (1.75 cm³ each) | 2 | catalogue | $1.00 each ($2.00 total; $1.00 min part floor) | https://jlc3dp.com/help/article/pa12-hp-nylon , read 2026-09-24 | part of parcel | — | 25% tariff: $0.50 | $2.50 |
| Black dyeing post-processing (Q30) | 3 parts | catalogue | $1.50 per part ($4.50 total; $0.00 for grey) | https://jlc3dp.com/help/article/pa12-hp-nylon , read 2026-09-24 | part of parcel | — | 25% tariff: $1.13 | $5.63 |
| Shipping: JLC3DP to Massachusetts | 1 parcel | UNVERIFIED | range $12.00 – $22.00 (likely $15.00 DDP) | https://jlc3dp.com/help/article/shipping-methods , read 2026-09-24 | $12.00 – $22.00 | — | DDP included | $12.00 – $22.00 |
| Section 301 Tariff (HTS 3926.90.9985) | 1 order | legal rate | 25.0% ad valorem (pre-collected under DDP) | https://ustr.gov/issue-areas/enforcement/section-301-investigations/tariff-actions , read 2026-09-24 | — | — | $1.93 | $1.93 |
| Trade Remedy Reserve (HTSUS 9903.05.31) | 1 order | UNVERIFIED | range 0.0% ($0.00) to 12.5% ($0.96) | UNVERIFIED: CSMS text not public via HTTP; range shown in totals | — | — | $0.00 – $0.96 | $0.00 – $0.96 |
| Massachusetts Use Tax (6.25%) | 1 order | legal rate | 6.25% where not collected ($0.50) | M.G.L. c. 64I, § 2, https://www.mass.gov/guides/sales-and-use-tax , read 2026-09-24 | — | $0.50 | — | $0.50 |
| **Order 3 Delivered Total (China route: JLC3DP)** | **1 body + 2 lids** | **catalogue + UNVERIFIED** | — | — | — | — | — | **Low: $18.00 (grey, standard) / Likely: $25.00 (black, standard) / High: $35.00 (black, DHL, duty reserve)** |

### 4.2 US Route: Xometry (Domestic Quick-Turn)

| Item | Quantity | Status | Unit price as displayed | Source URL and read date | Shipping | Tax | Import collection | Delivered line total |
| --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: |
| MJF PA12 Body (Black / Grey) | 1 | catalogue / quoted | $36.00 ($30.00–$42.00 small part floor) | https://www.xometry.com/capabilities/3d-printing/hp-mjf/ , read 2026-09-24 | $0.00 (free ground) | MA 6.25%: $2.25 | $0.00 (domestic) | $38.25 |
| MJF PA12 Lids (Black / Grey) | 2 | catalogue / quoted | $15.00 each ($30.00 total) | https://www.xometry.com/capabilities/3d-printing/hp-mjf/ , read 2026-09-24 | $0.00 (free ground) | MA 6.25%: $1.88 | $0.00 (domestic) | $31.88 |
| **Order 3 Delivered Total (US route: Xometry)** | **1 body + 2 lids** | **catalogue / quoted** | — | — | **$0.00** | **$4.13** | **$0.00** | **Low: $58.00 / Likely: $70.00 / High: $82.00** |

*Route Verdict: The China route (JLC3DP) is **$45 cheaper** than the US route ($25 vs $70 delivered).*

---

## 5. Order 4 — Small Parts and Battery Cell

Contents: Titanium skin-contact screws, closure screw, captive hex standoffs, 501012 LiPo cell with connector, charging cable, assembly tools, foam pads, and disposable gel electrodes.

### 5.1 Cell and Connector (Market Sourcing Finding)

*Investigation finding:* **No seller offers an off-the-shelf 501012 40 mAh LiPo battery with a Molex Pico-EZmate Slim plug fitted.** Consumer and industrial cells ship with bare wire leads or standard 1.25 mm / 2.0 mm JST connectors. The cell and the Molex connector assembly must be purchased separately:

| Item | Description | Quantity | Status | Unit price as displayed | Source URL and read date | Shipping | Tax | Delivered line total |
| --- | --- | ---: | --- | ---: | --- | ---: | ---: | ---: |
| 501012 40 mAh LiPo cell (3.7V, with PCM) | 5.0 × 10.0 × 12.0 mm LiPo cell | 1 (or 2-pk) | catalogue | $3.50 ($3.20–$5.00 range) | https://www.aliexpress.us/item/3256808874133671.html , read 2026-09-24; Walmart 4-pk $9.49, https://www.walmart.com , read 2026-09-24 | $3.50 | MA 6.25%: $0.22 | $7.22 |
| Molex Pico-EZmate Slim pre-crimped leads | Molex 0797581010 (28 AWG, 300 mm, gold) | 2 leads | catalogue | $1.47 each ($2.94 total) | https://www.digikey.com/en/products/detail/molex/0797581010/3728140 , read 2026-09-24 | combined DigiKey | MA 6.25%: $0.18 | $3.12 |
| Molex Pico-EZmate Slim crimp housing | Molex 202655-0021 (2-circuit plug) | 2 | catalogue / UNVERIFIED | $0.45 each ($0.90 total) | https://www.digikey.com/en/products/detail/molex/2026550021/9859585 , read 2026-09-24 | combined DigiKey | MA 6.25%: $0.06 | $0.96 |
| **Cell + Fitted Plug Delivered Total** | — | — | **catalogue / UNVERIFIED** | — | — | — | — | **$11.30 (range: $9.00–$16.00)** |

### 5.2 Screws, Standoffs, and Assembly Hardware

| Item | Specification / Supplier | Quantity | Status | Unit price as displayed | Source URL and read date | Shipping | Tax | Delivered line total |
| --- | --- | ---: | --- | ---: | --- | ---: | ---: | ---: |
| Titanium ISO 7380 M2.5 × 4 mm screws | Sortafast SF-BH2504-10 (Grade 5 Ti, 1.5mm hex) | 10-pack | catalogue | $17.50 (10-pack) | https://sortafast.com/products/sortafast-titanium-screws-button-head-10pk-m2-5 , read 2026-09-24 | $4.50 (USPS Ground) | MA 6.25%: $1.09 | $23.09 |
| Titanium ISO 7380 M2.5 × 8 mm closure screw | Sortafast / The Thomas RC / Amazon (Grade 5 Ti) | 1–4 pk | catalogue | $1.60 individual ($8.50 for 4-pack) | https://thethomasrc.com , read 2026-09-24; Amazon M2.5 Ti button heads, https://www.amazon.com , read 2026-09-24 | $4.50 | MA 6.25%: $0.53 | $6.63 – $13.53 (likely $10.00) |
| Brass female hex standoff 5 AF × 3.0 mm (Catalog 100-pack) | Spacer Express LAI-FF-M2.5-SW5-L3-100 (100-pack) | 100-pack as sold | catalogue | €91.08 ex VAT (~$99.00 USD) | https://spacer-express.com/female-female/875-hexagonal-female-female-threaded-spacer-nickel-plated-brass-m2-5-5-mm-across-flats.html , read 2026-09-24 | €15.00 ($16.20) | — | $115.20 (catalog 100-pack route) |
| *Alternative Standoff Route: Generic small pack* | *M2.5 × 3 mm female hex 5mm AF brass (Amazon/eBay/AliExpress)* | *10-pack* | *catalogue* | *$6.50 – $10.00 (10-pack)* | *Amazon / eBay M2.5 hex standoff, https://www.amazon.com , read 2026-09-24* | *part of parcel* | *MA 6.25%: $0.50* | *$8.00 – $12.00 (likely small-pack route)* |
| 1.5 mm hex key | McMaster-Carr 7122A14 (Short-arm hex key) | 1 | catalogue | $0.48 | https://www.mcmaster.com/7122A14/ , read 2026-09-24 | combined | MA 6.25%: $0.03 | $0.51 |
| Pre-cut foam pads (0.5 mm poron / PU) | Plan v2 §9 allowance | 1 set | allowance | $3.00 ($2.00–$5.00 range) | Plan v2 §9, 2026-09-17 | — | — | $3.00 |
| Silicone port plugs | Plan v2 §9 allowance (3 spares) | 3 | allowance | $4.00 ($3.00–$6.00 range) | Plan v2 §9, 2026-09-17 | — | — | $4.00 |
| Snap-electrode leads + gel electrodes | 2.54 mm pin sockets + Ag/AgCl gel electrodes | 3 leads + pack | catalogue | $14.50 ($12.00–$18.00 range) | https://www.adafruit.com/product/2773 , read 2026-09-24 | $5.00 | MA 6.25%: $0.91 | $20.41 |
| 2-pin magnetic pogo charging cable (8mm pitch) | 2-pin pogo USB charging cable | 1 | catalogue | $8.99 ($8.00–$14.00 range) | https://www.walmart.com , read 2026-09-24; AliExpress 2-pin magnetic pogo cable, read 2026-09-24 | $2.99 | MA 6.25%: $0.56 | $12.54 |
| Nickel test kit (or Rolf's written waiver) | Rolf's written waiver ($0) vs DMG test kit ($15) | 1 | allowance | $0.00 (waiver) – $15.00 (DMG kit) | Plan v2 §9, 2026-09-17 | — | — | $0.00 – $15.00 |
| **Order 4 Delivered Total (Small parts + Cell)** | — | — | — | — | — | — | — | **Low: $92.00 (small-pack standoffs, waiver) / Likely: $125.00 / High: $245.00 (100-pack standoffs + DMG kit)** |

---

## 6. Order 5 — Conditional First-Load Programming Kit

Only required if factory bootloader programming is not authorized or falls to Rolf (plan v2 §8, §9, Q48). US distributors:

| Item | MPN / Description | Quantity | Status | Unit price as displayed | Source URL and read date | Shipping | Tax | Delivered line total |
| --- | --- | ---: | --- | ---: | --- | ---: | ---: | ---: |
| Tag-Connect TC2030-IDC-NL | 6-pin no-legs programming cable | 1 | catalogue | $33.95 | https://www.tag-connect.com/product/tc2030-idc-nl , read 2026-09-24 | $5.50 (USPS Ground) | MA 6.25%: $2.12 | $41.57 |
| Raspberry Pi Debug Probe | Kit with case and cables (SC0917) | 1 | catalogue | $12.00 | https://www.adafruit.com/product/5699 , read 2026-09-24; docs: https://www.raspberrypi.com/documentation/microcontrollers/debug-probe.html , read 2026-09-24 | combined | MA 6.25%: $0.75 | $12.75 |
| Breadboard jumper wires (M-to-F) | 10-pack jumpers | 1 | catalogue | $1.95 | https://www.adafruit.com/product/1954 , read 2026-09-24 | combined | MA 6.25%: $0.12 | $2.07 |
| **Order 5 Delivered Total (Conditional kit)** | — | — | **catalogue** | — | — | — | — | **Low: $55.00 / Likely: $58.00 / High: $65.00** |

---

## 7. Whole-Project Delivered Spend Summary (Massachusetts, USA)

Grand totals for all orders required to build and deliver the Elicio earpiece to Rolf:

| Order | Description | Status | Low | Likely | High |
| --- | --- | --- | ---: | ---: | ---: |
| **Order 1** | Board fabrication & PCBA (JLCPCB, 5 flex boards, China) | catalogue / quote / UNVERIFIED | $372.00 | $413.00 | $495.00 |
| **Order 2** | Consigned active parts (Mouser / DigiKey: ISP1807, TPS7A02, Molex) | catalogue | $87.00 | $95.00 | $105.00 |
| **Order 3** | Shell print PA12 MJF (JLC3DP, 1 body + 2 lids, China route) | catalogue / UNVERIFIED | $18.00 | $25.00 | $35.00 |
| **Order 4** | Small parts & cell (screws, standoffs, 501012 cell, pogo cable, electrodes) | catalogue / allowance / UNVERIFIED | $92.00 | $125.00 | $245.00 |
| **Base Hardware Total** | **Orders 1–4 Delivered (Without programming kit)** | — | **$569.00** | **$658.00** | **$880.00** |
| **Order 5 (Optional)** | Conditional first-load programming kit (Tag-Connect + Debug Probe) | catalogue | $55.00 | $58.00 | $65.00 |
| **Complete Project Total** | **Orders 1–5 Delivered (With programming kit)** | — | **$624.00** | **$716.00** | **$945.00** |

*Note on US vs. China shell route:* If the shell is printed domestically via Xometry (US route: $70.00) instead of JLC3DP (China route: $25.00), add **+$45.00** to each total.
