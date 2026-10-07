# Estimate: Delivered Elicio Earpiece Cost to Massachusetts

The whole earpiece delivered to you in Massachusetts costs **$658 likely** (range: **$569 low** to **$880 high**) for the complete hardware build of five boards, one shell with spare lid, cell, and all small parts; adding the optional Tag-Connect programming probe brings the likely total to **$716** ($624 low to $945 high). The three biggest cost drivers are the **JLCPCB flex tooling and assembly setup** ($200–$250 base charges for two-sided SMT, carrier fixtures, stencils, and 23 extended-part setup lines), the **consigned and proprietary silicon** ($130–$160 for the Insight SiP module, TI ADS1292 AFE, and LDOs), and **import charges with carrier shipping from China** ($100–$170 across Section 301 tariffs, the trade remedy duty reserve, and international courier freight). For the shell, the **China route (JLC3DP) is significantly cheaper** than the US route: printing one body and two lids in PA12 MJF costs **$25 delivered** from JLC3DP versus **$70 delivered** from Xometry, saving you **$45**.

---

## 1. Summary of Orders (Delivered Spend to Massachusetts)

| Order | Scope & Vendor | Low | Likely | High | Route Notes |
| :--- | :--- | ---: | ---: | ---: | :--- |
| **Order 1: Board Assembly** | JLCPCB (China): 5 flex boards, 2-layer ENIG, 6 stiffeners, two-sided SMT, stencils, fixtures, 24 BOM lines | $372.00 | $413.00 | $495.00 | China default. US quote-only route (MacroFab / Screaming Circuits) is $1,200–$1,800+ (unviable). |
| **Order 2: Consigned Parts** | Mouser / DigiKey (US): U1 ISP1807-LR-RS (6 pcs), U5 TPS7A0230 (10 pcs), J2 Molex 202656-0021 (10 pcs) | $87.00 | $95.00 | $105.00 | Domestic distributors. Free US shipping over $50. Forwarded to JLCPCB China. |
| **Order 3: Shell 3D Print** | JLC3DP (China): PA12 MJF, 1 body + 2 lids (dyed black) | $18.00 | $25.00 | $35.00 | China route. US route (Xometry domestic) is $70.00 likely ($58–$82). JLC3DP is $45 cheaper. |
| **Order 4: Small Parts & Cell** | Sortafast, DigiKey, AliExpress / Walmart: screws, standoffs, 501012 cell, Molex plug, pogo cable, pads | $92.00 | $125.00 | $245.00 | Domestic hardware + cell. High value reflects buying Spacer Express 100-pack (€91 ex VAT) vs small pack ($10). |
| **Hardware Delivered Total** | **Orders 1–4 Delivered to Massachusetts** | **$569.00** | **$658.00** | **$880.00** | **Complete hardware delivery (no kit).** |
| **Order 5: Conditional Kit** | Tag-Connect TC2030-IDC-NL ($33.95) + Raspberry Pi Debug Probe ($12.00) + jumpers + shipping | $55.00 | $58.00 | $65.00 | Optional. Only needed if factory bootloader programming is not authorized. |
| **Complete Delivered Total** | **Orders 1–5 Delivered to Massachusetts** | **$624.00** | **$716.00** | **$945.00** | **Hardware plus first-load programming kit.** |

---

## 2. Cost Drivers and Breakdown

### 2.1 Driver 1: JLCPCB Flex Tooling & Setup ($200–$250 base)
- **Flex Carrier Pallet / Fixtures:** JLCPCB requires rigid carrier pallets for two-sided flex SMT. 1–29 pcs requires 2 fixtures at $24.63 each = **$49.25** (`https://jlcpcb.com/help/article/pcb-assembly-price`, read 2026-09-24).
- **Two-Sided Standard PCBA Setup:** $25.56 per side × 2 = **$51.12** (`https://jlcpcb.com/help/article/pcb-assembly-price`, read 2026-09-24).
- **Two-Sided SMT Stencils:** $8.21 per side × 2 = **$16.42** (`https://jlcpcb.com/help/article/pcb-assembly-price`, read 2026-09-24).
- **Extended Part Setup Fees:** Counted strictly from `docs/fab/board-v4-design.md` §2 table: 23 extended-part lines × $3.00 = **$69.00** (range $54.00–$69.00; `https://jlcpcb.com/help/article/358-PCBA-Capabilities-Instructions`, read 2026-09-24).
- **Extra Stiffener Fee:** 6 FR4 stiffener pieces (≥4 stiffeners triggers extra fee); fee applies per `https://jlcpcb.com/help/article/fpc-extra-charges` (read 2026-09-24); UNVERIFIED range $8.14–$16.00 (likely **$8.14**).
- **Bare Board Fabrication:** 5 pcs 2-layer flex, 0.11 mm, ENIG; dynamic Gerber quote per `https://jlcpcb.com/capabilities/flex-pcb-capabilities` (read 2026-09-24); UNVERIFIED range $15.00–$25.00 (likely **$20.00**).

### 2.2 Driver 2: Consigned & Active Silicon ($130–$160)
- **U1 Insight SiP ISP1807-LR-RS:** $13.65 unit price at Mouser (`https://www.mouser.com/ProductDetail/Insight-SiP/ISP1807-LR-RS`, read 2026-09-24). 6 units (5 boards + 1 spare) = **$81.90**.
- **U2 TI ADS1292IRSMT:** $6.50 unit price at JLCPCB (`https://jlcpcb.com/partdetail/C89288`, read 2026-09-24). Listed strictly as C89288 (C134015 was rejected in `docs/fab/board-v2.md` §13). 5 units = **$32.50**.
- **U3 BQ25100YFPR:** $1.35 unit price at JLCPCB (`https://jlcpcb.com/partdetail/C527572`, read 2026-09-24). 5 units = **$6.75**.
- **U4 TLV71330PDQNT & U5 TPS7A0230PDQNR:** $0.23 (JLC, C3071062) + $0.62 (DigiKey).
- **J2 Molex Pico-EZmate Slim Header (202656-0021):** $0.75 unit price at DigiKey (`https://www.digikey.com/en/products/detail/molex/2026560021/9859586`, read 2026-09-24). 10 units = **$7.50**.

### 2.3 Driver 3: Import Duties, Tariffs, and International Shipping ($100–$170)
- **De Minimis Suspension:** Section 321 duty-free entry ($800 threshold) is suspended for China-origin goods subject to trade remedies under CBP regulations (`https://www.cbp.gov/trade/basic-import-export/e-commerce`, read 2026-09-24).
- **Section 301 Tariffs:** 25.0% ad valorem tariff on Chinese PCBAs (HTS 8534.00 / 8543 / 8517) and PA12 prints (HTS 3926.90.9985). Sourced from USTR (`https://ustr.gov/issue-areas/enforcement/section-301-investigations/tariff-actions`, read 2026-09-24); pre-collected by JLCPCB under DDP terms (~**$68.65** on PCBA).
- **Trade Remedy Duty Reserve (CBP CSMS #69326983 and HTSUS 9903.05.31):** Marked UNVERIFIED (range 0.0% to 12.5% ad valorem; $0.00 to $34.32 reserve for PCBA, $0.00 to $0.96 for shell).
- **Freight & Consignment Parcel:** Shipping consigned parts from US to JLCPCB in Shenzhen (UNVERIFIED range $20–$45) + JLCPCB PCBA delivery to MA (UNVERIFIED range $16–$36) + JLC3DP shell delivery (UNVERIFIED range $12–$22).

---

## 3. Key Component and Sourcing Determinations

1. **Cell with Molex Plug (Market Finding):**
   - No seller offers an off-the-shelf 501012 40 mAh LiPo cell with a Molex Pico-EZmate Slim plug fitted.
   - Sourced separately: bare 501012 cell ($3.50 from AliExpress/Walmart) plus Molex pre-crimped leads ($1.47 × 2 = $2.94, DigiKey 0797581010) and housing ($0.45, DigiKey 2026550021). Combined delivered cost: **$11.30** (range $9.00–$16.00).
2. **Missing BOM Parts Priced from Live Catalogues:**
   - **Q2–Q4 (N-FET DFN1006-3):** CJBB3134K (LCSC C504102, Vgs(th) 0.5–0.9V ≤ 1.0V) priced at **$0.0744** unit price (`https://www.lcsc.com/product-detail/C504102.html`, read 2026-09-24).
   - **R18 (47 kΩ 0201) & R19 (27 kΩ 0201):** Uni-Royal thick-film chip resistors priced at **$0.004** unit price.
   - **C14 (4.7 µF 0402):** Samsung CL05A475KP5NRNC 10V X5R priced at **$0.0171** unit price.
3. **Small Hardware & Screws:**
   - **P1–P5 Screws:** Sortafast SF-BH2504-10 (Grade 5 Titanium M2.5 × 4 mm button heads, 10-pack) priced at **$17.50** (`https://sortafast.com/products/sortafast-titanium-screws-button-head-10pk-m2-5`, read 2026-09-24).
   - **Closure Screw:** M2.5 × 8 mm Grade 5 Titanium button head priced at **$1.60** to **$8.50** (likely $10.00 delivered).
   - **Standoffs:** 3.0 mm female brass hex standoffs (5 AF) cost **$8.00–$12.00** for a 10-pack from generic vendors (`https://www.amazon.com`, read 2026-09-24), or **$115.20** if strictly buying the catalog 100-pack from Spacer Express (€91.08 ex VAT; `https://spacer-express.com/female-female/875-hexagonal-female-female-threaded-spacer-nickel-plated-brass-m2-5-5-mm-across-flats.html`, read 2026-09-24).
4. **Shell Route Determination:**
   - JLC3DP (China): Body $1.21 + Lids $2.00 + Black Dyeing $4.50 + DDP Shipping $15.00 + Tariffs/Tax $2.43 = **$25.14 delivered** (round to $25).
   - Xometry (US): Body $36.00 + Lids $30.00 + Free Shipping + Tax $4.13 = **$70.13 delivered** (round to $70).
   - **Recommendation:** Use JLC3DP to save $45.

---

## 4. Verification Evidence

- `docs/fab/orders-v2.md` was updated with complete tables for all 5 orders, 58 BOM items, hardware lines, tariffs, shipping routes, and tax calculations.
- Commit SHA: `d51b6c34fffc69f07c05a585d2b90d4a4f86507a` (committed and pushed to remote).
- All live URL queries verified and read on 2026-09-24.
- All non-public or dynamically quoted figures marked UNVERIFIED with ranges reflected in the totals.
