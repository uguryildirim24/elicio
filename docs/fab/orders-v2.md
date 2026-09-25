# Earpiece delivered-cost worksheet — routed v4 + built 18 mm shell, Massachusetts

**Planning total, USD: $750.09 low / $1,338.99 likely / $3,176.23 high.** The three largest likely drivers are the board delivered ($536.09), small parts including the custom fitted cell and 100-pack of spacers ($483), and purchase/forwarding of consigned parts ($190). Board fabrication/acceptance, unselected or unavailable parts, the custom fitted cell, PA12 print/finish, freight, import and tax **remain ranges**: none is a complete delivered checkout price. High is an allowance, **not** a guaranteed delivered maximum or a quote. The board has 63 placed components of 27 types after the charger-ESD change; the selected shell is the *built* 18 mm snap trial, not the older 22 mm mesh. Rolf requested the estimate without setting a spending ceiling. **No order** until the other fit, electrical, supplier and delivered-price checks below are complete.

Public pages were read **2026-09-25**, in USD unless stated otherwise. No upload, account, quote request, vendor contact or purchase was made. `UNVERIFIED` denotes an explicit planning interval rather than a vendor price. The v2 `order-board.md`, `order-shell.md`, and `order-parts.md` remain instructions for an older design, **not** a v4 checkout. No manual final assembly labor, failed-board rerun, new engineering labor, medical certification or skin approval is included.

## Built evidence and price-source key

`hardware/board/v4_parts.py` and the released `hardware/board/elicio-v4.kicad_pcb` have **63 BOM placements, 27 types**, 4 consigned types (U1, U5, J2, **C3/C14/C18/C19**), 23 proposed JLC types: 1 Basic, 22 potential Extended (18 currently valid coded Extended, 2 blank, 2 stale/unavailable coded). J4 and P1–P5 are copper/contact footprints, not purchased parts; J3 is the only through-hole placement. Parsing the released board footprints for all 63 BOM references yields **341 SMT pads + 3 through-hole pads per board**, i.e. 1,705 SMT joints and 15 manual joints for five boards. These are *pad-based* estimates, not an assembly acceptance or an assertion every pad is billable. Both sides assembled on two-layer ENIG flex; six FR4 stiffeners still require JLC approval. The bare-board fabrication cost is dynamic, not obtainable from a public fixed-price schedule without submitting files.

- **J**, all read 2026-09-25: [JLC PCBA public schedule](https://jlcpcb.com/help/article/pcb-assembly-price) (Standard PCBA: double-side setup $51.12, double stencil $16.42, flexible-PCB two fixtures $49.25 at 1–29 pcs, pre-reflow $0.016/joint, SMT $0.0016/joint, manual $0.0164/joint and $3.58 hand-solder labor, feeder loading **$1.53 per Basic/Extended type**, confirmation $0.45, packing $0.50 plus area), [Basic vs Extended](https://jlcpcb.com/help/article/pcb-assembly-basic-parts-vs-extended-parts), [flex charges](https://jlcpcb.com/help/article/fpc-extra-charges), [consignment terms](https://jlcpcb.com/help/article/consigned-parts-service-introduction), [flex capability](https://jlcpcb.com/capabilities/flex-pcb-capabilities). The $8.14 stacked-stiffener fee is **not** a quote for these six ordinary stiffeners. JLC does not promise to assemble the consigned parts or 0201-on-flex at these rates.
- **P**, read 2026-09-25: [JLC3DP PA12-HP MJF](https://jlc3dp.com/help/article/pa12-hp-nylon) advertises **from $1.00**, tolerance ±0.3 mm (under 100 mm), minimum wall 1 mm, *not* a price for this body or either lid. [US MJF alternative](https://www.xometry.com/capabilities/3d-printing/hp-mjf/) has no public matching delivered price. Prior v2 mesh illustration ($1.21 material + $2 process + $4.50 dye, read 2026-09-24) is **not** a quote or upper bound for v4.
- **D/S/B/K**, source status: [Mouser U1](https://www.mouser.com/ProductDetail/Insight-SiP/ISP1807-LR-RS), [DigiKey U5](https://www.digikey.com/en/products/detail/texas-instruments/TPS7A0230PDQNR/9995577) blocked/403 on 2026-09-25; [Molex J2 drawing](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/202/202656/2026560021_sd.pdf) has no unit offer. U1 $13.65/U5 $0.62/J2 $0.75 are **old unverified comparators**, not newly page-read prices. [Sortafast M2.5×4 ten-pack](https://sortafast.com/products/sortafast-titanium-screws-button-head-10pk-m2-5) $17.50/10, sold out (read 2026-09-24); [Spacer Express LAI-FF-M2.5-SW5-L3-100](https://spacer-express.com/female-female/875-hexagonal-female-female-threaded-spacer-nickel-plated-brass-m2-5-5-mm-across-flats.html) **€82.80 ex VAT/100**, refreshed 2026-09-25 (the former €91.08 figure changed; product page structured offer shows €82.80). [PKCELL custom packs](https://www.pkcell.com/product-category/custom-battery-pack/) and [EEMB custom service](https://www.eemb.com/service/7), rechecked 2026-09-25, offer no one-unit fitted 501012 price. [Tag-Connect TC2030-IDC-NL](https://www.tag-connect.com/product/tc2030-idc-nl) $33.95 and [Adafruit Debug Probe](https://www.adafruit.com/product/5699) $12 (read 2026-09-24); jumper $1.95 remains an unverified estimate.

### Part basket (one board ×5; JLC public catalogue unit prices)

Each linked **JLC part page**, read **2026-09-25**, supplies the displayed 1-piece tier (except as marked), library class and observed warehouse stock; quantity in the `×5` column is five boards' *placements*, **not** a confirmed minimum purchase, feeder waste or order price. Prices are USD per component. `0` or `<qty` stock is flagged; warehouse figures change. Every `CONSIGNED` row is **not** assigned a JLC price, even if a similarly named catalogue entry exists. Code and placement grouping reflect the merged `v4_parts.py`, not a substituted design.

| Refs / value | JLC/LCSC code; class | Qty ×5 | Public unit tier; stock | Evidence |
| --- | --- | ---: | --- | --- |
| U1 ISP1807-LR-RS | CONSIGNED; n/a | 5 | UNVERIFIED $13.65 prior comparator; six purchased for attrition | D |
| U2 ADS1292IRSMT | C89288; Extended | 5 | $6.4422 (1–9); 97 | [part](https://jlcpcb.com/partdetail/C89288) |
| U3 BQ25100YFPR | C527572; Extended | 5 | $2.4912 (1–9); **0, out of stock** | [part](https://jlcpcb.com/partdetail/C527572) |
| U4 TLV71330PDQNT | C3071062; **unverified/stale code** | 5 | Page resolves `null`, no catalogue price or class | [attempted](https://jlcpcb.com/partdetail/C3071062) |
| U5 TPS7A0230PDQNR | CONSIGNED; n/a | 5 | UNVERIFIED $0.62 prior comparator; ten purchased | D |
| Q1 WPM3027-3/TR | C240195; Extended | 5 | $0.0400 (1–199); 9,846 | [part](https://jlcpcb.com/partdetail/C240195) |
| Q2–Q4 PMZ290UNE2YL | C478155; Extended | 15 | $0.0553 (1–49); 2,712 | [part](https://jlcpcb.com/partdetail/C478155) |
| D1 PESD5V0L1UL | C24109; **WRONG code, not priced** | 5 | Page names *TLV320AIC3204IRHBR*, not a PESD diode; **do not buy this code** | [part](https://jlcpcb.com/partdetail/C24109) |
| D2 LED 19-217/GHC-YR1S2/3T | C72043; Extended | 5 | $0.0238 (1–499); **1, insufficient** | [part](https://jlcpcb.com/partdetail/C72043) |
| J2 202656-0021 | CONSIGNED; n/a | 5 | UNVERIFIED $0.75 prior comparator; ten purchased | D |
| J3 2.54-1*3PPin | C49257; Extended | 5 | $0.0275 (1–199); 225,607 | [part](https://jlcpcb.com/partdetail/C49257) |
| SW1 1TS015A-1200-0600-CT | C398746; Extended | 5 | $0.0835 (1–49); 233 | [part](https://jlcpcb.com/partdetail/C398746) |
| R1–R3, R31–R33 220k 0402 | C881401; Extended | 30 | $0.0012 (1–999); 9,884 | [part](https://jlcpcb.com/partdetail/C881401) |
| R4,R17,R20,R21 1M 0201 | C473482; Extended | 20 | $0.0015 (1–999); 373,564 | [part](https://jlcpcb.com/partdetail/C473482) |
| R5–R8,R13,R25,R27,R28,R34,R35 10k 0201 | C473048; Extended | 50 | $0.0014 (1–999); 10,110,616 | [part](https://jlcpcb.com/partdetail/C473048) |
| R11 6.8k 0201 | C4104700; Extended | 5 | $0.0087 (1–9); **0, out of stock** | [part](https://jlcpcb.com/partdetail/C4104700) |
| R12 6.04k 0201 | C270341; Extended | 5 | $0.0014 (1–999); 149,721 | [part](https://jlcpcb.com/partdetail/C270341) |
| R14–R16,R23,R24 100k 0201 | C270364; Extended | 25 | $0.0015 (1–999); 623,686 | [part](https://jlcpcb.com/partdetail/C270364) |
| R18 47k 0201 | **no code; proposed Extended** | 5 | UNVERIFIED; no selected MPN/code | [part list](../../hardware/board/v4_parts.py) |
| R19 27k 0201 | **no code; proposed Extended** | 5 | UNVERIFIED; no selected MPN/code | [part list](../../hardware/board/v4_parts.py) |
| R22 1k 0201 | C270365; Extended | 5 | $0.0013 (1–999); 1,874,512 | [part](https://jlcpcb.com/partdetail/C270365) |
| C1 1.5nF 0201 | C285104; Extended | 5 | $0.0014 (1–999); 26,543 | [part](https://jlcpcb.com/partdetail/C285104) |
| C2 10nF 0201 | C43380; Extended | 5 | $0.0011 (1–999); **10, very thin stock** | [part](https://jlcpcb.com/partdetail/C43380) |
| C3,C14,C18,C19 GRM155R61A106ME18 10uF 0402 | CONSIGNED; n/a | 20 | UNVERIFIED: cap selected for DC-bias/ESD; no verified JLC code or public purchased-pack price | [part list](../../hardware/board/v4_parts.py) |
| C4,C5,C10,C11,C13,C16 1uF 0201 | C5142566; Extended | 30 | $0.0052 (1–499); 347,988 | [part](https://jlcpcb.com/partdetail/C5142566) |
| C6,C8,C9 10uF 0402 | C15525; **Basic** | 15 | $0.0255 (1–999); 8,670,930; **different MPN from ESD caps** | [part](https://jlcpcb.com/partdetail/C15525) |
| C7,C12,C15,C17 100nF 0201 | C307380; Extended | 20 | $0.0061 (1–999); 995,525 | [part](https://jlcpcb.com/partdetail/C307380) |

**Four proposed JLC types cannot be closed from this release:** R18 and R19 have no chosen MPN/library code; U4's listed C3071062 returns a null catalogue page; D1's C24109 is a different IC. Selecting a lookalike footprint without electrical/assembly qualification would change the board BOM, which this task cannot edit. Three *additional* coded types have supply blockers (U3 and R11 at zero, D2 one piece). The four GRM capacitors are a **fourth consigned type**, not one of the four proposed JLC blanks/stale types. Nineteen valid coded JLC types' five-board 1-piece-tier extensions sum **$47.274** (includes U3/R11/D2 *as if restocked*). The $55/$85/$165 board-basket scenarios below include **UNVERIFIED** $7.73/$37.73/$117.73 for the four unpriced types, stock substitutions, minimum buys and attrition; $47.274 alone cannot buy a working set. Do not infer an order can currently be placed.

## Delivered order estimates (USD)

Each row marked UNVERIFIED remains a range even where its cited public schedule supplies one input. Column sums below count all services and parcels once. Public schedule J is **Standard**, not the Economic-only $3.07 Extended feeder charge. For a five-board assembly, 27 types × $1.53 = $41.31 is an *illustration* if all 27 (including four consigned types) incur feeder loading; if JLC applies a different classification, reprice. The X-ray count assumes U1 only; other leadless packages could increase it. J3 manual assembly is 15 pads × $0.0164 + $3.58 = $3.83 rounded. JLC may refuse consignment, thin-stock passives, through-hole header or 0201 flex; acceptance is open.

### 1 — China JLC board order, five two-sided assembled flex boards

| Charge, source and arithmetic (UNVERIFIED unless public schedule explicitly says fixed) | Low | Likely | High |
| --- | ---: | ---: | ---: |
| ENIG two-layer flex fabrication ×5; J dynamic/no files submitted | 15 | 25 | 90 |
| Six ordinary FR4 stiffeners; J no price for this geometry | 8 | 20 | 70 |
| Standard double-side assembly setup; J $51.12 | 51.12 | 51.12 | 80 |
| Double-side stencil; J $16.42 | 16.42 | 16.42 | 40 |
| Two flexible carriers/fixtures; J $24.63 ×2 = $49.25 schedule | 49.25 | 49.25 | 120 |
| Pre-reflow; 1,705 pads × J $0.016 = $27.28 | 27.28 | 27.28 | 27.28 |
| SMT assembly; 1,705 pads × J $0.0016 = $2.728 | 2.73 | 2.73 | 10 |
| J3 manual pads + hand-solder labor; 15 × J $0.0164 + $3.58 ≈ $3.83 | 3.83 | 3.83 | 25 |
| Standard feeder; 27 types × J $1.53 = $41.31 (consigned applicability open) | 41.31 | 41.31 | 90 |
| JLC handling of four consigned types; J terms not a handling quote | 12 | 30 | 75 |
| Basket above, including four unpriced/stock-blocked JLC types | 55 | 85 | 165 |
| U1 X-ray; 5 × J $1.64 = $8.20, more packages may qualify | 8.20 | 8.20 | 40 |
| J part-placement confirmation $0.45 + packing at least $0.50 | 0.95 | 0.95 | 0.95 |
| Rails, tooling, feeder attrition, factory image (unpriced) | 0 | 30 | 150 |
| [JLC shipping methods](https://jlcpcb.com/help/article/shipping-methods), no MA price; parcel range | 18 | 35 | 85 |
| China→US board duty on declared goods **including consigned value**, headings open (import section) | 0 | 70 | 220 |
| Carrier entry/disbursement, no verified schedule for this parcel | 0 | 20 | 65 |
| MA sales/use tax on taxable portion, less collected tax credit | 0 | 20 | 45 |
| **Order 1 delivered** | **309.09** | **536.09** | **1,398.23** |

### 1a — buy and directly forward four consigned types to JLC China

| Charge (all UNVERIFIED; D; purchased units not only fitted) | Low | Likely | High |
| --- | ---: | ---: | ---: |
| U1 six × old $13.65 comparator = $81.90 | 81.90 | 100 | 150 |
| U5 ten × old $0.62 comparator = $6.20 | 6.20 | 8 | 18 |
| J2 ten × old $0.75 comparator = $7.50 | 7.50 | 12 | 32 |
| GRM155R61A106ME18 ESD caps, minimum supply/attrition not quoted | 5 | 15 | 40 |
| Tracked US distributor → JLC parcel | 20 | 40 | 90 |
| Export forwarding/China customs | 0 | 15 | 50 |
| **Order 1a direct export** | **120.60** | **190.00** | **380.00** |

If shipment must first go to a Massachusetts forwarder instead, **add** domestic freight $0/$12/$25 and possible MA tax $6/$9/$15, all UNVERIFIED: order 1a **$126.60/$211/$420**; choose one route. Board customs may include the value of these components but the board order does **not** repurchase them. No second US duty on a genuine direct export.

### 2 — built 18 mm PA12 snap shell, one body + two lids

Measured with repo CAD environment (`uv venv .venv; uv pip install --python .venv/bin/python 'build123d==0.11.1' 'cadquery-ocp-novtk==7.9.3.1.1'`) and `build123d.import_step`, on the 2026-09-25 `v4-snap` solids **before the three local component reliefs**. These volumes are a historical estimate, not measurements of the current STEP files; remeasure before requesting a print quote. Units mm, mm³; axis-aligned STEP boxes include hook/hinge, not merely the nominal W18 × T8.1 package. The reliefs do not change the outer bounds.

| Solid | Pre-relief STEP volume | Bounding min (x,y,z) | Bounding max (x,y,z) | Box size |
| --- | ---: | --- | --- | --- |
| Body | 3,340.434 mm³ | (−21.787, −1.554, −51.346) | (21.000, 7.235, 15.344) | 42.787 × 8.789 × 66.690 mm |
| Lid, each ×2 | 900.197 mm³ | (0.096, 1.764, −49.925) | (20.850, 8.234, 4.408) | 20.754 × 6.470 × 54.333 mm |
| **One body + two lids** | **5,140.828 mm³ = 5.141 cm³** | — | — | Three separate printed parts |

This is the `v4-snap` *print-trial candidate* with Rolf's preferred flat 1 mm lid; no lid screw is bought. The 1.5 mm hex key below remains for releasing the latch. Keep the current body length for this estimate: Rolf cannot measure his ear now and wants big ears to fit too. A shorter body is not a replacement unless the fit study shows it still clears the big-ear gate; **this line prices only the current solid and may change after that evidence**. `docs/fab/shell-v4.md` reports **0.42 mm minimum nominal free chip-to-shell clearance** after the reliefs (U1 deliberately seats on P2); the published ±0.3 mm print tolerance still calls for physical clearance checks, and latch, retention and fit are not proven. No solid was uploaded to a print vendor for a quote. P only offers **from $1**, not a formula for minimum processing, orientation, dye, three-part packing or chargeable bounding volume. The old v2 $3.21 undyed illustration is a scale comparator, not this shell's price; $5/$12/$45 print is a reasoned **UNVERIFIED** low/likely/high for 5.14 cm³ and three small parts, not a JLC3DP unit rate. Low omits optional black finish; likely includes it.

| Charge, P or import section; all UNVERIFIED | Low | Likely | High |
| --- | ---: | ---: | ---: |
| PA12 MJF print, one body + two lids (P from $1 per part only) | 5 | 12 | 45 |
| Black finish; old-shell $4.50 comparator, optional in low | 0 | 5 | 15 |
| Separate JLC3DP→MA parcel; no public case price | 12 | 22 | 55 |
| China-origin shell duty on goods, heading open | 0 | 3 | 16 |
| Separate carrier brokerage if billed | 0 | 15 | 50 |
| MA tax less any seller-collected tax | 0 | 1 | 4 |
| **Order 2 delivered** | **$17** | **$58** | **$185** |

A US-printed shell is an **alternative**, not added to China route: print/finish $30/$100/$250, freight $0/$18/$40, MA tax $2/$8/$20, all UNVERIFIED (P US alternative page): **$32/$126/$310 delivered** if actually US-made. It would replace order 2 and have no US import duty/brokerage.

### 3 — small parts, purchased packs (not pieces consumed)

All delivered rows UNVERIFIED even when a catalogue price is cited. **S** and **B** source key above; other items have no selected SKU, so the row states why it is a range. The snap lid has **no lid screw**; the five skin/charge screws remain, with length/source to qualify. The 1.5 mm hex key is kept for the latch. 3.0 mm standoff height is not qualified. Charging is **off the ear only**; the released board retains fixed R13 10k on TS and a **two-wire J2**, so the priced cell requires **no temperature sensor or thermistor**. A factory-fitted **protected** ~40 mAh 501012-class two-wire cell with polarity-verified Pico-EZmate Slim mating plug is mandatory; bare cell plus loose pre-crimps are not acceptable. Battery shipping may require a separate regulated parcel.

| Charge and basis | Low | Likely | High |
| --- | ---: | ---: | ---: |
| Skin/charge screws, S $17.50 ten-pack sold out; substitute needed | 17.50 | 25 | 50 |
| Three standoffs bought as **100**, S €82.80 ex VAT; FX/stock/freight uncertainty remains | 100 | 115 | 155 |
| Factory-fitted protected **two-wire, no temperature-sensor** cell; B no one-unit offer/setup/MOQ | 35 | 90 | 250 |
| Insulated P4/P5 charge cable, spacing 7.75 mm; drawing/source open | 10 | 25 | 60 |
| Electrode leads, snaps, gel; unselected packs | 15 | 35 | 80 |
| Pre-cut foam, 1.5 mm hex key, insulated consumables; no SKU | 10 | 25 | 50 |
| Nickel screen or Rolf's written waiver (low = waiver) | 0 | 25 | 55 |
| Multimeter if not owned (low/likely assume owned) | 0 | 0 | 30 |
| Protected-cell separate parcel/regulated handling, unknown origin | 12 | 25 | 70 |
| EU spacer parcel to MA, separate supplier | 20 | 40 | 90 |
| Other US small-parts parcels combined | 15 | 40 | 100 |
| Spacer import duty + carrier fees, origin/classification unconfirmed | 0 | 20 | 60 |
| MA tax on taxable parts less collected tax credit | 8 | 18 | 40 |
| **Order 3 delivered** | **$242.50** | **$483** | **$1,090** |

If the custom maker requires more than the high cell allowance, this worksheet's high is exceeded. Cell country of origin and import treatment are not proved covered by the small-parts interval; resolve before ordering.

### 4 — conditional first-load kit (included in totals)

**K** key above, read date as stated there; all delivered amounts UNVERIFIED. J4 wiring and measured v4 target voltage/probe suitability require verification before purchase; do not apply a fixed-3.3 V probe to the erased 1.8 V v2 module. The v4 has a 3.0 V U5 supply at power-up but this is **not** approval of the kit.

| Charge and basis | Low | Likely | High |
| --- | ---: | ---: | ---: |
| Tag-Connect cable, K $33.95 catalogue, stock/variant open | 33.95 | 33.95 | 45 |
| Adafruit probe, K $12 catalogue, J4/voltage approval open | 12 | 12 | 20 |
| Jumpers, old unverified $1.95 estimate | 1.95 | 1.95 | 5 |
| Two separate US-seller parcels | 10 | 20 | 45 |
| MA tax less seller-collected tax | 3 | 4 | 8 |
| **Order 4 if needed** | **$60.90** | **$71.90** | **$123** |

Only if the assembler supplies and verifies the factory image can order 4 be removed; that changes the direct-export/China-shell total to **$689.19/$1,267.09/$3,053.23**. This is not a claim factory programming is included.

## Import, freight and stop rule

[Executive Order 14324](https://www.whitehouse.gov/presidential-actions/2025/07/suspending-duty-free-de-minimis-treatment-for-all-countries/) and [CBP guidance](https://content.govdelivery.com/accounts/USDHSCBP/bulletins/41fa7f0) (read 2026-09-25) suspend duty-free de minimis from 2025-08-29; being below $800 does **not** make a parcel automatically duty-free. [USITC candidates 8517.62](https://hts.usitc.gov/reststop/search?keyword=8517.62), [9018.19](https://hts.usitc.gov/reststop/search?keyword=9018.19) (board, general Free) and [3926.90.99](https://hts.usitc.gov/reststop/search?keyword=3926.90.99) (plastic shell, general 5.3%) were read 2026-09-25; none is a binding product classification. [USTR List 3](https://ustr.gov/sites/default/files/enforcement/301Investigations/83%20FR%2047974.pdf) lists 8517.62.00 **except suffix .0090**; [25% modification](https://ustr.gov/sites/default/files/enforcement/301Investigations/84_FR_20459.pdf). [USTR List 4](https://ustr.gov/sites/default/files/enforcement/301Investigations/Notice_of_Modification_%28List_4A_and_List_4B%29.pdf) and [USITC 9903.88.15](https://hts.usitc.gov/reststop/search?keyword=9903.88.15) show 7.5% on candidate shell heading 3926.90.99. Read 2026-09-25. Model board 0–25% potential Section 301 and shell candidate 5.3% + 7.5% = 12.8% on applicable *goods* values, plus an **UNVERIFIED 0–12.5% contingency** for any other applicable measure until primary notice and origin/classification are confirmed; do **not** charge all rates as facts. Board duty includes declared consigned value once. Low $0 duty models a confirmed alternate heading/exclusion or a fully prepaid DDP *incremental* charge, not de minimis. Actual tariff stacks, seller DDP terms, MA 6.25% taxable base and carrier fees remain unsettled.

[JLC shipping methods](https://jlcpcb.com/help/article/shipping-methods) and [US tariff FAQ](https://jlcpcb.com/help/article/u-s-tariff-policy-faq), read 2026-09-25, provide no MA freight price for this board. Board $18–85, shell $12–55, US distributor→JLC $20–90 and EU spacers $20–90 are separate parcel allowances, **not** shipping offers. [UPS fees](https://www.ups.com/us/en/shipping/international-shipping/import-fees.page) and [FedEx ancillary clearance](https://www.fedex.com/en-us/ancillary-clearance-service.html) were blocked on this machine (2026-09-25); board $0/$20/$65, shell $0/$15/$50 and spacer combined duty/fee $0/$20/$60 are unverified per-parcel reserves, $0 only when confirmed prepaid/no bill. No freight or tax is silently waived by a DDP label; apply credit for tax already collected once.

**Column arithmetic, China snap shell + direct-export consignment + first-load kit:**

| Delivered order | Low | Likely | High |
| --- | ---: | ---: | ---: |
| 1 board | 309.09 | 536.09 | 1,398.23 |
| 1a consigned parts | 120.60 | 190.00 | 380.00 |
| 2 snap shell | 17.00 | 58.00 | 185.00 |
| 3 small parts | 242.50 | 483.00 | 1,090.00 |
| 4 first load | 60.90 | 71.90 | 123.00 |
| **Sum** | **$750.09** | **$1,338.99** | **$3,176.23** |

Low **309.09 + 120.60 + 17 + 242.50 + 60.90 = 750.09**; likely **536.09 + 190 + 58 + 483 + 71.90 = 1,338.99**; high **1,398.23 + 380 + 185 + 1,090 + 123 = 3,176.23**. Replacing China shell only with the unverified US-made alternative gives **$765.09/$1,406.99/$3,301.23**. No row is a final checkout ledger. The shell remains a print trial, not a qualified wearable release; confirmed printed fit, latch strength and any revised CAD may change its price.

### Live G8 delivered-cost record — **open; do not order**

Rolf has seen this estimate and sets **no spending ceiling**. This record is for real route-specific costs once choices and checkout evidence exist; the planning high above does not fill it. Reserve a supported, complete shell delivered amount before paying for boards or parts.

| Required delivered amount (USD) | SKU/route, quantity, dated evidence | Goods + services | Freight | Import/carrier | MA tax | Delivered amount |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Board, tooling, programming, consignment handling | pending | pending | pending | pending | pending | pending |
| Four consigned types, one forward route | pending | pending | pending | pending | pending | pending |
| Snap body + two lids, print finish, **reserved before board payment** | pending | pending | pending | pending | pending | pending |
| Small parts by seller including fitted cell/charge cable | pending | pending | pending | pending | pending | pending |
| First load by seller or documented factory inclusion | pending | pending | pending | pending | pending | pending |
| **Sum of route-specific delivered amounts** | — | — | — | — | — | **pending** |

Before *any* payment: confirm the board release/ESD and fixed-TS off-ear charging arrangement, resolve wrong/missing codes and depleted inventory, obtain assembly acceptance for flex, 0201, both sides, consignment and X-ray, prove the physical snap fit, cell insulation/PCM/polarity, charge cable and standoff height, and document actual route-specific shipping, import and tax. Rolf has seen this estimate; **there is no spending-ceiling comparison**. If a complete shell delivered reserve cannot be supported, or any safety/fit/supplier check remains open, G8 fails. The v2 order sheets cannot close G8 for v4.
