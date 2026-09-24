# Delivered-spend ledger v2 — working estimate, not an order budget

Destination assumed: Massachusetts, USA (plan v2 D-8). No vendor has been asked
for a quote or sent design files. No purchase has been authorized. Prices below
are catalogue observations or **planning inputs**, not delivered quotes. A
supplier's general capabilities page is not a price for these particular
files. R8/G8 **does not pass** on this ledger: Rolf has not set the ceiling,
and the complete shipped, taxed, assembled device does not yet have a bounded
price.

The earlier $569–$880 hardware / $658 likely and $624–$945 with kit are **not
reproducible delivered totals**. In particular, the consignment row subtotal
was lower than the sum of its displayed line items, tariffs on the shell were
counted twice in its detail, and several required services had no price. Do
not use those numbers as a spending authorization.

## Configuration being costed

- Five 2-layer ENIG flex PCBAs, both sides populated, with six 0.2 mm FR4
  stiffeners and three consigned parts (U1, U5, J2), per
  `docs/fab/board-v4-design.md` §2–§4. The v4 board still has **10 open
  connections** (§9.4); it is not an orderable board. Its 0201-on-flex,
  module X-ray, two-sided assembly and tooling need assembler acceptance.
- One PA12 MJF body and two lids. The available
  `docs/fab/cad/v2/manifest.json` is a **provisional 22 mm-wide v2 shell**,
  with `closure_passed: false`. The v4 18 mm-wide body needs a new solid;
  neither print price nor the US-vs-China comparison can be quoted from the
  v2 mesh for the final earpiece.
- One protected 501012-class cell *with a factory-fitted, polarity-verified
  Molex Pico-EZmate Slim plug*, three electrodes, the five skin/charge screws,
  mating charging cable and the assembly tools. The exact cell revision and
  fitting vendor are open (G1b / Q69). Rolf's assembly rule is **no soldering,
  crimping or wire stripping** (`docs/fab/plan-v2.md` R2). Buying a bare cell,
  loose pre-crimps and a housing does **not** make a fitted, safe battery.
- A programming kit if first-load programming is not supplied by the board
  assembler. A multimeter is included if Rolf does not already own one.

## Board: catalogue inputs and non-catalogue costs

The following is **one five-board planning worksheet**, not a JLCPCB quote.
Prices for fixed services are from
https://jlcpcb.com/help/article/pcb-assembly-price (previously read
2026-09-17, rechecked by the lane 2026-09-24); extended-line fee from
https://jlcpcb.com/help/article/pcb-assembly-basic-parts-vs-extended-parts
(previously read 2026-09-17). Supplier acceptance, stock and the order's
actual pricing remain open. The part count comes from
`hardware/board/v4_parts.py` and `docs/fab/board-v4-design.md` §2; 24
non-consigned types, only C15525 marked Basic, hence up to 23 extended
setups. The electronics line is the lane's five-board **unit-price
calculation**, not a checkout price; minimum buy/feeder quantities and stock
are not included.

| Board charge | Five-board input (USD) | Status / basis |
| --- | ---: | --- |
| Bare 0.11 mm flex, ENIG | 20.00 | UNVERIFIED assumption, dynamic Gerber quote; https://jlcpcb.com/capabilities/flex-pcb-capabilities (lane read 2026-09-24) gives capabilities, not this price |
| Extra fee for six stiffeners | 8.14 | UNVERIFIED assumption; https://jlcpcb.com/help/article/fpc-extra-charges (lane read 2026-09-24) says ≥4 incur a fee but does **not** price this case; $8.14 is cited for *stacked* stiffeners, not a quote for six pieces |
| Two-sided standard assembly setup | 51.12 | Catalogue, $25.56 × 2; acceptance of this flex job open |
| Two stencils | 16.42 | Catalogue, $8.21 × 2 |
| Flex carrier fixtures | 49.25 | Catalogue example, two at $24.63 (rounded vendor total) |
| SMD solder joints | 2.80 | Estimate: 1,750 joints × $0.0016; actual placements/joint count unconfirmed |
| J3 through-hole labor/joints | 3.83 | Estimate: $3.58 + 15 × $0.017; whether JLC accepts this tab/header open |
| Extended setup | 69.00 | Estimate: 23 types × $3; tier and accepted stock to check |
| Consignment handling | 10.00 | Minimum fee assumption; https://jlcpcb.com/help/article/consigned-parts-service-introduction (lane read 2026-09-24); loose parts, feeder stock and parcel count need confirmation |
| JLC/LCSC component unit prices | 44.38 | Estimate from §2 of lane revision `d51b6c3`; Q2–Q4, R18, R19 and C14 lack confirmed assembler codes; U4 had zero JLC stock in board-v4-design §2 |
| **Worksheet subtotal before international freight, import and tax** | **274.94** | Arithmetic only; contains unverified charges and excludes the three consigned parts |

U2 is ADS1292IRSMT **C89288**, not the rejected C134015
(`docs/fab/board-v2.md` §13). U1 ISP1807-LR-RS is consigned, not a JLC
library component. X-ray for five modules would be $8.20 **if** JLC accepts
five at the plan v2 §9 catalogue $1.64/inspected-part bracket; it is not
included in the $274.94. Panel rails, any tooling changes, stencil/feeder
acceptance, consigned-part attrition and factory programming also need a
quote. Do not treat a generic US flex assembler's home page as a $1,200
quote.

## Consigned parts and forwarding (separate from board worksheet)

Catalogues cited by the lane (2026-09-24):
https://www.mouser.com/ProductDetail/Insight-SiP/ISP1807-LR-RS and
https://www.digikey.com/en/products/detail/texas-instruments/TPS7A0230PDQNR/9995577 .
Molex header stock and price are uncertain; the manufacturer part is
202656-0021 (board-v4-design §2). These are **component costs only**, not
free-delivered-to-China costs.

| Part | Count | Assumed unit | Extended USD |
| --- | ---: | ---: | ---: |
| U1 ISP1807-LR-RS | 6 | $13.65 | $81.90 |
| U5 TPS7A0230PDQNR | 10 | $0.62 | $6.20 |
| J2 202656-0021 | 10 | $0.75 (UNVERIFIED stock) | $7.50 |
| **Parts before tax/shipping** | | | **$95.60** |

If all three lines are taxed at Massachusetts 6.25%, tax is $5.98 and
subtotal **$101.58**, not $95. Direct export to China may be taxed
*differently*; do not add Massachusetts use tax automatically to items
shipped directly abroad. Domestic delivery to a forwarding address,
international forwarding, and JLC's consignment rules must be priced for
the actual parcel(s). The board worksheet does not include these parts.

## Shell, small parts and optional first-load kit

| Purchase | Observed input / calculation | Still missing |
| --- | --- | --- |
| Shell: body + two lids | v2 mesh-only illustration: $1.21 + $2.00 printing + $4.50 black dye = $7.71; assumed 25% duty $1.93 **once**, assumed freight $15, assumed MA use tax $0.50 → **$25.14 illustrative**, not a v4 quote | v4 printable solid and checkout; finish and skin-contact approval, vendor acceptance, freight, actual classification and complete import collection. https://jlc3dp.com/help/article/pa12-hp-nylon (lane read 2026-09-24) lists process information, not a price for final files. Xometry price, free shipping and alleged $45 saving are unverified; https://www.xometry.com/capabilities/3d-printing/hp-mjf/ did not provide a quote. |
| Skin/closure screws | Sortafast M2.5×4 10-pack $17.50 catalogue: https://sortafast.com/products/sortafast-titanium-screws-button-head-10pk-m2-5 (lane read 2026-09-24); separate closure screw cost UNVERIFIED | Shipping, material confirmation, v4 closure design and screw length (v2 CAD has a failed closure check) |
| Three 3.0 mm standoffs | Spacer Express LAI-FF-M2.5-SW5-L3-100: **€91.08 ex VAT for 100**, not $8–$12 for three. https://spacer-express.com/female-female/875-hexagonal-female-female-threaded-spacer-nickel-plated-brass-m2-5-5-mm-across-flats.html (2026-09-17) | Export freight/currency/taxes; exact 5 AF, thread/landing qualification and stock. A generic Amazon pack is **not** a qualified substitute (plan v2 G7). |
| Cell and fitted plug | Bare cell ~$3.50 and loose Molex parts ~$3.84 were lane assumptions, **not** a priced fitted pack. Cell listing and protection drawing unverified (board-v4-design §1, open questions Q69). | Factory-fit labor, PCM, drawing, pinout/polarity, insulated lead routing, shipping and vendor acceptance. No claim that none exists; sourcing is open. |
| Charging cable | The lane's generic 8 mm-pitch two-pin pogo cable at $8.99 has no qualified mating drawing | Correct P4/P5 pitch, polarity, retention, safe insulation and delivered price; board-v4-design §4.4 puts pads 7.75 mm apart in s. |
| Other small parts | Hex key, pre-cut 0.5 mm foam, electrode leads and gel, nickel kit or Rolf's written waiver | Pack quantities, postage, a multimeter if needed; existing `docs/fab/order-parts.md` lists unresolved parts (including obsolete USB/port-plug rows) and is not a priced v4 shopping list. |
| First-load kit, *if* needed | Tag-Connect $33.95 + Raspberry Pi Debug Probe $12.00 + jumpers $1.95 = **$47.90 parts only** (plan v2 §9; https://www.tag-connect.com/product/tc2030-idc-nl , https://www.adafruit.com/product/5699 , lane read 2026-09-24) | Tax, **both** vendors' postage, J4/probe electrical verification and factory programming alternative (G4). |

## Import and whole-project gate

For China-origin parcels, classification, applicable duty components, DDP
terms, carrier disbursement and state sales/use tax must be established for
each checkout. Plan v2 §9/§12 C13 explicitly warns that **25% Section 301
alone is not the whole import reserve**; CBP CSMS 69326983 names an
additional 12.5% component. The lane's 0%–12.5% trade-remedy range and
"likely $0 with DDP" have no evidence that JLC's DDP includes it.
General guidance: https://www.cbp.gov/trade/basic-import-export/e-commerce ,
https://ustr.gov/issue-areas/enforcement/section-301-investigations/tariff-actions ,
https://jlcpcb.com/help/article/u-s-tariff-policy-faq , and
https://www.mass.gov/guides/sales-and-use-tax (lane read 2026-09-24).
No HTS classification or duty rate for *this assembly* or these prints has
been confirmed. A DDP checkout is not proof that only one tariff applies.

**No credible all-in low/likely/high exists yet.** To see the scale, the
board-only worksheet $274.94 + an *assumed* 25% of that entire amount
($68.74) + assumed US→China forwarding $30 + assumed China→MA delivery
$22 + assumed MA tax $17.50 = **$413.18 illustrative**. This incorrectly
assumes all services, materials and tools share one tariff/tax basis and
**omits X-ray, uncovered setup/handling, qualified battery fitting and
assembly, tooling, the shell redesign, and possibly more duties**. It is
not a ceiling or a delivered order amount. The old $413 board figure was
obtained this way, not from a checkout.

Before any payment, regenerate the v4 shell, finish and get assembler
acceptance, select a qualified fitted cell and charger cable, collect actual
order-level shipping/fees/tax/import totals for every parcel (and the
programming kit/multimeter if needed), reserve the shell's **delivered
maximum**, compare the full amount to Rolf's ceiling, and show him the
ledger. Until then G8 is open and no one should order from this sheet.
