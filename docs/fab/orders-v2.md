# Earpiece delivered-cost worksheet — v4, Massachusetts

**Planning total, not a quote: $730 low / $1,268 likely / $2,983 high (USD).** This includes five assembled boards, one shell body and two lids, purchased packs of small parts, one factory-fitted protected cell and the *conditional* first-load kit. The three largest likely cost drivers are board fabrication/assembly and its import ($491), small parts including the fitted cell and 100-pack of standoffs ($483), and consigned components/forwarding ($175). The ranges remain wide because the board is not orderable, the narrower shell has no printable solid, the fitted cell has no published price, freight is checkout-dependent, and tariff classification and carrier collection are unresolved. **The high column is a scenario allowance, not a guaranteed ceiling. Do not buy against it.** The v2 `order-board.md`, `order-shell.md` and `order-parts.md` sheets still specify the older board, USB-C charging, cell and $50–90 shell reserve; they are **not v4 checkout instructions**. Do not use those sheets to pay for this design.

All web pages below were read or attempted **2026-09-25** unless an earlier observation date is stated. USD, quantities as purchased, not per usable earpiece. `UNVERIFIED` means a planning interval, *not* a seller offer. Low/likely/high are three separate scenarios; no unpriced item is silently zeroed except optional ownership/waiver choices explicitly described. No quote request, upload, account or purchase was made. The earlier $569–$880 / $658 figures were withdrawn by review: they omitted services and incorrectly subtotaled consignment and shell duty.

## Scope and public-page key

Five two-layer ENIG flex PCBAs, both sides assembled, six FR4 stiffeners and 58 placements of 27 types (`hardware/board/v4_parts.py`; `docs/fab/board-v4-design.md` §2–4). Three types (U1, U5, J2) are consigned; 24 proposed JLC types, only C15525 identified Basic, hence **23 potential Extended type fees**. Four proposed JLC types have no selected library code; U4 stock was zero. V4 still has ten open connections (§9.4). X-ray, 0201-on-flex, J3 through-hole, consignment, fixtures and two-sided assembly require acceptance. One 18 × 8.1 mm PA12 MJF body and two lids are *intended*, but the only built solid is the older 22 mm-wide v2f reference (`docs/fab/cad/v2/manifest.json`); its J2/P5 hardware gap is −4.93 mm and it is not a v4 shell. One protected 501012-class ~40 mAh cell with factory-fitted **polarity-verified Molex Pico-EZmate Slim mating plug** is mandatory; bare cell + loose pre-crimps violate `plan-v2.md` R2 (no soldering/crimping/stripping).

- **J** [JLC PCBA price](https://jlcpcb.com/help/article/pcb-assembly-price), [Basic/Extended](https://jlcpcb.com/help/article/pcb-assembly-basic-parts-vs-extended-parts), [FPC extra charges](https://jlcpcb.com/help/article/fpc-extra-charges), [consignment](https://jlcpcb.com/help/article/consigned-parts-service-introduction), [flex capability](https://jlcpcb.com/capabilities/flex-pcb-capabilities): public schedule read 2026-09-24, PCBA page re-read 2026-09-25. The FPC page does **not** quote six ordinary stiffeners; $8.14 is for stacked stiffeners. No Gerber/assembly checkout exists.
- **P** [JLC3DP PA12 information](https://jlc3dp.com/help/article/pa12-hp-nylon), [US MJF alternative, Xometry](https://www.xometry.com/capabilities/3d-printing/hp-mjf/): capabilities, not a price for these files. Older mesh *illustration* from the prior worksheet (2026-09-24): $1.21 material + $2 process + $4.50 black dye = $7.71 before freight. The $3.21 undyed print is an **old-shell upper comparator for size alone**, not a proven upper bound on the changed v4 geometry or an accepted file.
- **D** [Mouser U1 ISP1807-LR-RS](https://www.mouser.com/ProductDetail/Insight-SiP/ISP1807-LR-RS), [DigiKey U5 TPS7A0230PDQNR](https://www.digikey.com/en/products/detail/texas-instruments/TPS7A0230PDQNR/9995577): access denied / 403 on this machine. [LCSC search U1](https://www.lcsc.com/search?q=ISP1807-LR-RS) loaded but produced no verified U1 unit price. No public maker checkout located for [Molex 202656-0021](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/202/202656/2026560021_sd.pdf). Former $13.65/$0.62/$0.75 unit inputs (2026-09-24) therefore remain **UNVERIFIED**, not newly page-read prices.
- **S** [Sortafast M2.5×4 titanium ten-pack](https://sortafast.com/products/sortafast-titanium-screws-button-head-10pk-m2-5) **$17.50 for 10**, page read 2026-09-24, sold out; length and closure material unresolved. [Spacer Express LAI-FF-M2.5-SW5-L3-100](https://spacer-express.com/female-female/875-hexagonal-female-female-threaded-spacer-nickel-plated-brass-m2-5-5-mm-across-flats.html) **€91.08 ex VAT for 100**, read 2026-09-17; not $8–12 for three. The 3 mm height is still unqualified; changing height changes SKU/cost.
- **B** [PKCELL custom packs](https://www.pkcell.com/product-category/custom-battery-pack/) advertises protection and low MOQ without a numeric MOQ or this connector's price; [EEMB custom battery service](https://www.eemb.com/service/7) has no posted fitted-501012 price. Read 2026-09-25. [Bare 501012 comparison](https://www.aliexpress.us/item/3256804164251088.html), previously read 2026-09-23, ~$3.50–5, **not** a protected fitted pack. No one-unit custom-connector offer or setup fee established; a battery-pack assembler must certify insulation, PCM, pinout and polarity. Battery shipping may need a separate parcel.
- **K** [Tag-Connect TC2030-IDC-NL](https://www.tag-connect.com/product/tc2030-idc-nl) $33.95 and [Adafruit Raspberry Pi Debug Probe](https://www.adafruit.com/product/5699) $12, read 2026-09-24, plus unverified $1.95 jumpers. Two sellers, not one free-shipped kit. The probe's fixed 3.3 V I/O is **not safe for first load of the erased 1.8 V v2 module** (`order-parts.md`); v4 instead supplies U1 at 3.0 V from U5 at power-up (`board-v4-design.md` §7). J4 wiring, measured target voltage and probe compatibility still require G4 verification before selecting the v4 kit; if a different probe is needed, reprice it.

## Orders and delivered amounts

Each dollar interval below is explicitly **UNVERIFIED planning** unless identified as a public catalogue input above. For mixed catalogue and uncertain work the *whole row* is UNVERIFIED; a known unit price is not a known delivered bill. Low uses a favorable checkout/owned tool/waiver, likely reserves typical separate parcels, high reserves scarce stock, extra tooling and entry fees. These are *not* vendor-defined upper limits. Import is broken out below and counted once. Each table's subtotal is the sum of its displayed columns.

### 1 — JLC China board order (five assembled boards; excludes consigned purchase)

| Charge / basis | Low | Likely | High |
| --- | ---: | ---: | ---: |
| UNVERIFIED bare ENIG flex, five; dynamic Gerber price (J) | 15 | 20 | 70 |
| UNVERIFIED six ordinary stiffeners (J; not stacked-fee quote) | 8 | 20 | 70 |
| UNVERIFIED two-sided setup; J schedule $25.56 × 2 = $51.12 if accepted | 51.12 | 51.12 | 80 |
| UNVERIFIED two stencils; J $8.21 × 2 = $16.42 if accepted | 16.42 | 16.42 | 40 |
| UNVERIFIED two flex carriers; J example $24.63 each, rounded $49.25 | 49.25 | 49.25 | 120 |
| UNVERIFIED joints; 1,750 × J $0.0016 = $2.80 provisional | 2.80 | 2.80 | 10 |
| UNVERIFIED J3 through-hole; J $3.58 + 15 × $0.017 ≈ $3.83 | 3.83 | 3.83 | 25 |
| UNVERIFIED Extended setup; 23 types × J $3 = $69 if all accepted | 69 | 69 | 90 |
| UNVERIFIED consignment handling, parcel/feeder terms (J) | 10 | 20 | 50 |
| UNVERIFIED 24 JLC component types; earlier calculated $44.38 for five, four codes open | 44.38 | 55 | 110 |
| UNVERIFIED module X-ray; $1.64 × 5 = $8.20 plan v2 §9, acceptance open | 8.20 | 8.20 | 40 |
| UNVERIFIED rails, tooling, feeder attrition, factory image (no price) | 0 | 30 | 150 |
| UNVERIFIED JLC → Massachusetts international shipping, one small protected parcel | 18 | 35 | 85 |
| UNVERIFIED US import duties on board **including consigned value** (classification below) | 0 | 70 | 220 |
| UNVERIFIED carrier brokerage/disbursement on board import (below) | 0 | 20 | 65 |
| UNVERIFIED MA sales/use tax on taxable portions, subject to credit | 0 | 20 | 45 |
| **Order 1 delivered** | **296.00** | **490.62** | **1,270.00** |

Board duty allowance is *not* 25% of the whole assembly invoice as an asserted legal rule. Likely $70 roughly represents a China-origin goods basis around $280 at 25%; high $220 reserves a larger customs value including the consigned components and layered rates. Tax and duty bases differ; neither freight nor a DDP label automatically cancels duties. $0 low duty is the alternate heading/exclusion or already-paid DDP **incremental checkout** case, not de-minimis exemption.

### 1a — buy and forward three consigned part types to JLC (direct-export route)

| Charge / basis | Low | Likely | High |
| --- | ---: | ---: | ---: |
| UNVERIFIED U1, six × former $13.65 = $81.90 (D; price blocked) | 81.90 | 100 | 150 |
| UNVERIFIED U5, ten × former $0.62 = $6.20 (D; 403) | 6.20 | 8 | 18 |
| UNVERIFIED J2, ten × former $0.75 = $7.50 (D; no maker price) | 7.50 | 12 | 32 |
| UNVERIFIED US distributor/forwarder → JLC China, tracked parts parcel | 20 | 40 | 90 |
| UNVERIFIED export forwarding/China customs handling if charged | 0 | 15 | 50 |
| **Order 1a (direct export)** | **115.60** | **175.00** | **340.00** |

The parts alone total **$95.60 low**; US tax is *not* added to a genuine direct export. If a US distributor must instead ship first to a Massachusetts forwarder, add **UNVERIFIED $0/$12/$25 domestic freight and $6/$9/$15 possible MA tax**, then keep China forwarding as above: order 1a becomes **$121.60/$196/$380**. Do not count both routes. Board import duty above includes the consigned value once; this table has no second US duty on it.

### 2 — shell, China print route (one body + two lids)

| Charge / basis | Low | Likely | High |
| --- | ---: | ---: | ---: |
| UNVERIFIED PA12 print; old 22 mm mesh was $3.21 undyed (P); 18 mm v4 rework unknown | 3 | 3.21 | 25 |
| UNVERIFIED black finish; old mesh $4.50, optional in low (P) | 0 | 4.50 | 15 |
| UNVERIFIED JLC3DP → Massachusetts separate parcel | 12 | 22 | 55 |
| UNVERIFIED China duties on shell goods, not freight (below) | 0 | 2 | 12 |
| UNVERIFIED carrier entry/advance fee, only if separate bill (below) | 0 | 15 | 50 |
| UNVERIFIED MA sales/use tax, subject to credit | 0 | 1 | 3 |
| **Order 2 China delivered** | **15.00** | **47.71** | **160.00** |

A US-printed MJF alternative **exists** (P) but cannot be priced without the new solid; *alternative*, not added to China total: UNVERIFIED print/finish **$30/$100/$250**, US freight **$0/$18/$40**, MA tax **$2/$8/$20** → **$32/$126/$310 delivered**, with $0 US import duty and brokerage for a US-made print. Switching shell route alone changes the overall total to **$747/$1,346.52/$3,133**. US manufacture, material and dye must be confirmed; a US vendor reselling a Chinese print is not this route.

### 3 — small parts (purchased packs, not only pieces consumed)

| Charge / basis | Low | Likely | High |
| --- | ---: | ---: | ---: |
| UNVERIFIED five skin/charge screws plus any v4 closure fastener; Sortafast M2.5×4 $17.50/10 sold out (S), closure length/route and alternate qualification open | 17.50 | 25 | 50 |
| UNVERIFIED three 3.0 mm hex standoffs bought as **100** (S); €91.08 ex VAT; illustrative USD conversion/stock allowance | 100 | 115 | 155 |
| UNVERIFIED **one factory-fitted protected** 501012 cell; custom pack maker, possible setup/MOQ (B), not bare cell | 35 | 90 | 250 |
| UNVERIFIED mating insulated charge cable for P4/P5 (7.75 mm pad spacing), no qualified drawing | 10 | 25 | 60 |
| UNVERIFIED three electrode leads, snap electrodes and gel, multiple packs | 15 | 35 | 80 |
| UNVERIFIED pre-cut foam, 1.5 mm hex key, insulated plugs/consumables | 10 | 25 | 50 |
| UNVERIFIED nickel screening kit, or Rolf's written waiver (low $0) | 0 | 25 | 55 |
| UNVERIFIED multimeter if not already owned (low/likely assume owned) | 0 | 0 | 30 |
| UNVERIFIED fitted-cell parcel freight/regulated handling to MA | 12 | 25 | 70 |
| UNVERIFIED EU standoff parcel to MA (separate supplier) | 20 | 40 | 90 |
| UNVERIFIED other US small-parts seller parcels combined | 15 | 40 | 100 |
| UNVERIFIED standoff import duty + carrier entry/advance fee (origin, classification open) | 0 | 20 | 60 |
| UNVERIFIED MA tax on taxable items, credit any seller-collected tax | 8 | 18 | 40 |
| **Order 3 delivered** | **242.50** | **483.00** | **1,090.00** |

$35/$90/$250 for the pack is a **scenario**, not a manufacturer's published MOQ: low presumes a one-off protected custom termination, high allows minimum pack quantity/setup. If the actual maker requires more than this, even the high total fails. Rolf must not fit a loose connector. Battery imports, if sent directly from China rather than a US-stocked pack seller, can add tariff/entry costs not proven covered by the small-parts interval; resolve origin/route before ordering. The €91.08 line's USD range is a conversion and FX/stock allowance, **not** a verified exchange rate.

### 4 — conditional first-load kit, assumed needed in all totals

| Charge / basis | Low | Likely | High |
| --- | ---: | ---: | ---: |
| UNVERIFIED cable; Tag-Connect $33.95 catalogue (K), stock/variant open | 33.95 | 33.95 | 45 |
| UNVERIFIED v4 probe; Adafruit $12 catalogue (K), J4/target-voltage fit and stock open | 12 | 12 | 20 |
| UNVERIFIED jumpers, former $1.95 estimate | 1.95 | 1.95 | 5 |
| UNVERIFIED two US-seller postage charges to MA | 10 | 20 | 45 |
| UNVERIFIED MA sales/use tax | 3 | 4 | 8 |
| **Order 4 delivered if needed** | **60.90** | **71.90** | **123.00** |

If the assembler supplies and verifies the factory image, subtract this order: **$669.10/$1,196.33/$2,860** on the China-shell direct-export scenario. This is a conditional saving, not a promise that programming is included.

## Import method and freight evidence (not free under $800)

[Executive Order 14324](https://www.whitehouse.gov/presidential-actions/2025/07/suspending-duty-free-de-minimis-treatment-for-all-countries/) suspends duty-free de minimis for all countries from 2025-08-29; [CBP guidance](https://content.govdelivery.com/accounts/USDHSCBP/bulletins/41fa7f0) confirms the suspension. Read 2026-09-25. A small parcel is **not** automatically free. [USITC HTS search](https://hts.usitc.gov/reststop/search?keyword=8517.62), [9018.19](https://hts.usitc.gov/reststop/search?keyword=9018.19), [3926.90.99](https://hts.usitc.gov/reststop/search?keyword=3926.90.99), read 2026-09-25: candidate board headings **8517.62.00** (data transmitter, general **Free**) or **9018.19.95** (EEG/EMG apparatus subline .35, general **Free**; .75 printed circuit assemblies for parameter acquisition modules also Free). Candidate PA12 shell **3926.90.99** (other plastic article, general **5.3%**). These are hypotheses, *not* a binding classification of an unfinished board/shell. General rates alone do not give the landed rate.

[USTR List 3 notice (83 FR 47974)](https://ustr.gov/sites/default/files/enforcement/301Investigations/83%20FR%2047974.pdf), read 2026-09-25, explicitly lists **8517.62.00** in note 20(g) **except statistical suffix .0090**; the other 8517.62 entries appear in the notice's list. [USTR's modification to 25%](https://ustr.gov/sites/default/files/enforcement/301Investigations/84_FR_20459.pdf) and [List 3 index](https://ustr.gov/issue-areas/enforcement/section-301-investigations/section-301-china/200-billion-trade-action) establish that a matching China-origin List 3 item can face **+25%**. [USTR List 4 notice](https://ustr.gov/sites/default/files/enforcement/301Investigations/Notice_of_Modification_%28List_4A_and_List_4B%29.pdf), read 2026-09-25, lists **3926.90.99** in the 9903.88.15 group; [current USITC 9903.88.15 entry](https://hts.usitc.gov/reststop/search?keyword=9903.88.15) shows **+7.5%**. The precise board statistical suffix, whether it is instead 9018.19, and product-specific exclusions remain unverified. Model board China Section 301 **0–25%**; *if* the shell classifies at 3926.90.99 with no exclusion, its general 5.3% plus List 4 **7.5% = 12.8%** (if another heading/exclusion is confirmed, revise), not 25% merely because it is Chinese. Board general 0% yields **0–25%** before other measures. Plan v2 §9/§12 mentions CBP CSMS 69326983 and a potential **12.5%** separate measure, but its applicability to either parcel has **not been established** here; the [CBP bulletin above](https://content.govdelivery.com/accounts/USDHSCBP/bulletins/41fa7f0) concerns de minimis, **not this rate**. Reserve **0–12.5% only as an UNVERIFIED contingency** until an applicable primary notice is identified; it is not a charge claimed due. Thus possible modeled stacks are board **0–37.5%**, shell **12.8–25.3% under the candidate heading** of the applicable declared *goods* value, not the freight/entire service invoice. US-made shell: no US import. No exemption claimed for EU standoffs. Before checkout, get written classification/origin, applicable Chapter 99 lines, declared goods values (including U1/U5/J2), and DDP tax/fee breakout from sellers/carrier.

Freight cannot be retrieved without package mass, origin, service and a real checkout: [JLC shipping methods](https://jlcpcb.com/help/article/shipping-methods) and [JLC US tariff FAQ](https://jlcpcb.com/help/article/u-s-tariff-policy-faq) were read 2026-09-25 but display **no price** for this board. The board's $18–85 assumes a small China→MA express parcel, US distributor→JLC $20–90 assumes tracked consigned components, shell $12–55 assumes a *separate* light JLC3DP→MA parcel. Do not combine parcels unless checkout explicitly does. US shell freight $0–40 assumes pickup/free shipping possible but unconfirmed. [UPS import-fees page](https://www.ups.com/us/en/shipping/international-shipping/import-fees.page) returned **Access Denied** and [FedEx ancillary-clearance page](https://www.fedex.com/en-us/ancillary-clearance-service.html) returned **System Down / permission denied** here (2026-09-25); DHL public customs page also timed out. Therefore the carrier's actual disbursement/entry schedule is **UNVERIFIED**, not $0 by default: board **$0/$20/$65**, separate shell **$0/$15/$50**, imported EU standoffs included in their **$0/$20/$60** combined duty-and-fee row. Zero only if seller prepays *and* confirms no bill on delivery. These are per-parcel allowances, not claimed UPS/FedEx/DHL posted tariffs. Massachusetts 6.25% sales/use tax is modeled on plausible taxable purchases; tax line ranges allow exemptions, vendor collection and credit, **not** a universal rate on import duty plus shipping.

## Reconciliation and stop rule

**China shell + direct-export consignment + first-load kit:** low **$296 + $115.60 + $15 + $242.50 + $60.90 = $730**; likely **$490.62 + $175 + $47.71 + $483 + $71.90 = $1,268.23**; high **$1,270 + $340 + $160 + $1,090 + $123 = $2,983**. Substituting the US shell or the MA-forwarder amounts above changes exactly that order, not the other columns. A US flex-assembler path exists in principle but no publicly priced *equivalent* five-board service including fixtures, 0201, consignment and X-ray was found. For comparison **only**, replace orders 1 **and** 1a with an entirely **UNVERIFIED** US assembly/fabrication interval **$800/$1,600/$4,000** (one job, five populated flex boards, tooling and inspection provisionally included), consigned U1/U5/J2 **$95.60/$120/$200** (D), US distributor→assembler postage **$0/$15/$40**, assembler→MA freight **$15/$35/$90**, MA sales/use tax **$56/$110/$260** (6.25% of a provisional taxable goods/services basis): **$966.60/$1,880/$4,590 delivered**. No US customs duty or brokerage for a verified US-made board; merely using a US mailing address would not qualify. With the **China shell** and orders 3–4 unchanged, this alternative is **$1,285/$2,482.61/$5,963**. These numbers are scenario allowances, *not* a verified quote, source-certified domestic origin, or proof an assembler will build it. Do not present a generic US assembler page as a $1,200 offer. No manual final assembly labor, new CAD/board design labor, failed-board retry, medical certification or skin approval is included.

### Live G8 record — not yet filled

The scenario tables above are **not** a checkout ledger or a reserved delivered maximum. The old plan's $50–90 shell allowance cannot reserve the unbuilt v4 shell: even the unverified China-shell high scenario is $160. Record a supported, complete delivered shell maximum **before** paying for a board or parts. Write v4 order sheets against the released files; the v2 sheets named above cannot close G8 for v4.

| Required live entry (USD unless stated) | Route / SKU, quantity, evidence date | Goods + services | Freight | Import duty + carrier fees | MA sales/use tax (collected or payable) | Delivered maximum |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Board, including tooling, programming or first-load route, and consignment handling | pending | pending | pending | pending | pending | pending |
| Consigned U1/U5/J2, including any MA forwarding and export handling; **one** direct-export or MA-forwarder route | pending | pending | pending | pending | pending | pending |
| V4 body + lids, selected finish, **reserved before board payment** | pending | pending | pending | pending | pending | pending |
| Small parts: each seller/parcel, including a qualified fitted cell and charge cable (add rows per parcel) | pending | pending | pending | pending | pending | pending |
| First-load kit if needed; each seller/parcel (or documented factory programming included in board) | pending | pending | pending | pending | pending | pending |
| **Whole project: sum of delivered maxima including the shell reserve** | — | — | — | — | — | **pending** |
| **Rolf's ceiling (Q33)** | **pending — Rolf supplies it** | — | — | — | — | **pending** |

A catalogue part price alone cannot fill a delivered maximum; get a checkout/quote or a documented reserve that covers the still-open charges. Count consigned value in board customs value without repurchasing the parts in the board row; include tax collected at checkout or payable later, but never both for the same taxable amount; count DDP duties and carrier fees only once. Mark not-needed entries explicitly with the reason, never silently as $0. If the shell maximum cannot be supported or the summed maximum exceeds Rolf's ceiling, G8 fails. Recalculate after each checkout; don't substitute the low/likely/high scenarios for these entries.

Before **any** payment, finish the board's ten connections and v4 shell solid/closure; verify maker accepts this assembly, custom cell, charge cable and standoff length; obtain actual basket quantities, shipping, customs classification, import fees and tax per parcel. Compare the resulting full delivered maximum to the ceiling **Rolf sets**. Until then plan v2 G8 remains open; neither $2,983 nor the alternative high is an authorization to order.
