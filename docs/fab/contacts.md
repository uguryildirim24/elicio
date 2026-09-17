# Elicio Stage B Earpiece — Contacts Kit: Sourcing, Stack Verification, and Assembly

This document specifies the skin-contact hardware, internal terminations, material verification, screening protocol, and assembly procedures for the Elicio Stage B behind-the-ear (BTE) earpiece.

This specification serves the requirements in `docs/EARPIECE_DESIGN.md` and `docs/fab/plan.md` (§2 rows 3–4, §3.3 CONTACT_*, §4, §6, §7 Order 2, §8 claims 8–9, 16, §9 row WP5).

---

## 1. Verified Component SKUs and Sourcing

All source pages and catalog specifications were inspected on 2026-09-16. Prices are recorded with vendor URLs and access dates. Any unverified parameter is marked UNVERIFIED.

Review r1 note (2026-09-17). Where the URL recorded for a price is a site's home page or a distributor's front page, not the product page, the price is marked UNVERIFIED: plan §9 row WP5 asks for a page per price. Head and nut dimensions quoted without a drawing page are marked UNVERIFIED the same way. The reviewer did not re-read any vendor page.

### 1.1 Contact Screws: ISO 7380 M2.5 Button-Head Titanium Screws

The three skin-contact electrodes require ISO 7380 M2.5 button-head screws in Grade 2 commercially pure titanium (ASTM F67) or Grade 5 titanium alloy (Ti-6Al-4V, ASTM F136 / ASTM F1472). No plating or coating is permitted on the skin-contact surface.

#### Supplier Sourcing Analysis

*   **McMaster-Carr:** NOT STOCKED in M2.5 titanium. McMaster-Carr stocks Grade 2 and Grade 5 titanium screws in metric sizes starting at M3 socket-head cap screws. McMaster-Carr does not stock metric button-head screws in titanium in any size. (Verified at [mcmaster.com](https://www.mcmaster.com/products/screws/material~titanium/) on 2026-09-16).
*   **Bolt Depot:** NOT STOCKED in titanium. Bolt Depot carries metric fasteners only in steel and stainless steel. (Verified at [boltdepot.com](https://www.boltdepot.com/) on 2026-09-16).
*   **Titanium Fasteners Specialists:** Multiple verified options exist in Grade 2 (TA2) and Grade 5 (TA6V / 6Al-4V).

#### Verified Sourcing Options

| Item | Primary Option: RJXHOBBY Grade 2 | Specialist Option: Titane Services Grade 5 | Alternative Option: Sortafast Grade 5 |
| :--- | :--- | :--- | :--- |
| **Supplier** | RJXHOBBY | Titane Services (France / EU) | Sortafast Industries (US) |
| **Product Name** | RJX 50pcs M2.5 4-20mm TA2 Button Head Titanium screws | Vis titane tête bombée ISO 7380 BHC Titane Gr5 M2.5 | M2.5 Titanium Button Head Screws (Grade 5) |
| **Part / Model No.** | `RJX3995-M2.5X4mm` | `vis-titane-ISO7380-G5-M2.5` | `SF-M2.5-BH-TI` |
| **Product Page URL** | [rjxhobby.com](https://www.rjxhobby.com/) | [titane-services.eu](https://www.titane-services.eu/vis-titane-ISO7380-G5-M2.5) | [sortafast.com](https://sortafast.com) |
| **Date Read** | 2026-09-16 | 2026-09-16 | 2026-09-16 |
| **Material Grade** | Grade 2 Titanium (TA2 / CP Titanium, ASTM F67 equivalent) | Grade 5 Titanium (TA6V / Ti-6Al-4V, ASTM F136 equivalent) | Grade 5 Titanium (6Al-4V) |
| **Price** | $33.99 USD — UNVERIFIED: the URL above is the home page, not the product page | 3.57 € (approx. $3.85 USD) | $17.50 USD — UNVERIFIED: the URL above is the home page |
| **Pack Size** | Pack of 50 ($0.68 / each) | 1 piece (bulk tiers available) | Pack of 10 ($1.75 / each) |
| **Thread Size** | M2.5 × 0.45 mm pitch | M2.5 × 0.45 mm pitch | M2.5 × 0.45 mm pitch |
| **Length under head ($L$)** | 4.0 mm nominal | 4.0 mm nominal | 4.0 mm nominal (or 6.0 mm trimmed) |
| **Head Style / Standard** | ISO 7380 Button Head | ISO 7380 Button Head | ISO 7380 Button Head profile |
| **Head Diameter ($d_k$)** | UNVERIFIED; the listing range quoted was 4.40–4.70 mm, no drawing page | UNVERIFIED; no drawing page cited | UNVERIFIED; no drawing page cited |
| **Head Crown Height ($k$)**| UNVERIFIED; the listing range quoted was 1.20–1.36 mm, no drawing page | UNVERIFIED; no drawing page cited | UNVERIFIED; no drawing page cited |
| **Drive Style** | Hex Socket, 1.5 mm Allen key | Hex Socket, 1.5 mm Allen key | Hex Socket, 1.5 mm Allen key |

The head numbers above equal the plan's CAD reservation (dome Ø4.7, crown 1.35), but none is read from a drawing. `docs/fab/interface.md` §2.2 note D1 cites a manufacturer ISO 7380 M2.5 row of dk max 4.5, k max 1.5, and RJXHOBBY's own range reaches 4.40. A 4.4–4.5 mm dome changes the contact area (17.3 mm² at 4.7, 15.9 at 4.5, 15.2 at 4.4) and the crown the gauge prints. This is interface v2 item V2-1 in `interface.md`; the gauge keeps 4.7 × 1.35 until a drawing is on file.

Plan §7 order 2 allows $20 for one screw pack. The RJXHOBBY pack ($33.99, UNVERIFIED) is over that line; the order 2 gate ($160) still holds.

---

### 1.2 Retaining Thin Nuts: DIN 439 / ISO 4035 M2.5

The internal retaining nut secures the screw and ring lug against the internal face of the 1.5 mm PA12 medial wall.

#### Stocking Status: Titanium vs. Conventional Thin Nuts

*   **Titanium M2.5 Thin Nuts (DIN 439 / ISO 4035):** NOT STOCKED off-the-shelf by standard retail distributors (McMaster-Carr, Bolt Depot, Accu). Fastenright ([fastenright.com](https://www.fastenright.com)) manufactures DIN 439 M2.5 titanium half nuts in Grade 2 and Grade 5 upon request, but pricing is UNVERIFIED without a formal commercial quotation.
*   **What the plan allows inside:** Plan §4 says: *"Nut and lug may be plated steel or tinned copper; they sit under the lid and never see skin."* That allowance names plated steel and tinned copper. It does not name stainless steel, and plan §1 item 4 (the contacts line, which lists the thin nut) ends "no stainless". A plated carbon-steel DIN 439 M2.5 thin nut (zinc-plated, not nickel-plated) is the plan's nut. **No plated-steel SKU is verified in this file: UNVERIFIED**, to be closed with a product page, date and price before order 2.
*   **Stainless (18-8 / A2) thin nuts** fit the same stack and are listed below because they are the stocked option found, but they sit outside the plan text. Using one is Rolf's decision (see "Needs a decision" in `tasks/reviews/code-r1.md`).
*   **Alternative Option (Standard Full Nut DIN 934 in Titanium):** Standard-height DIN 934 M2.5 hex nuts in titanium have a nominal height of 2.0 mm (versus 1.6 mm for DIN 439).

#### Verified Sourcing Options for Thin Nuts

| Item | Outside plan text (stainless): McMaster-Carr 18-8 Thin Nut | Outside plan text (stainless): Accu A2 Thin Nut | Bespoke Titanium Option: Fastenright DIN 439 |
| :--- | :--- | :--- | :--- |
| **Supplier** | McMaster-Carr | Accu (UK / US) | Fastenright Ltd |
| **Product Name** | Metric 18-8 Stainless Steel Thin Hex Nut | M2.5 Thin Hexagon Nuts (DIN 439) | Titanium Half Nuts (DIN 439) |
| **Part / Model No.** | `90710A025` | `HNU-M2-5-A2` | UNVERIFIED (`M2.5-DIN439-TI` is not shown on a product page) |
| **Product Page URL** | [mcmaster.com](https://www.mcmaster.com/90710A025/) | [accu.co.uk](https://www.accu.co.uk/thin-nuts/36829-HNU-M2-5-A2) | [fastenright.com](https://www.fastenright.com) (home page) |
| **Date Read** | 2026-09-16 | 2026-09-16 | 2026-09-16 |
| **Material** | 18-8 Stainless Steel (AISI 304) | Stainless Steel A2 (AISI 304) | Grade 2 or Grade 5 Titanium |
| **Price** | $2.50 USD | £0.38 to £0.91 GBP (~$0.50–$1.20 USD) | UNVERIFIED (requires supplier quote) |
| **Pack Size** | Pack of 50 ($0.05 / each) | 1 piece (tiered quantity discounts) | Custom batch |
| **Standard** | DIN 439B / ISO 4035 | DIN 439 / ISO 4035 | DIN 439 |
| **Thread Size** | M2.5 × 0.45 mm pitch | M2.5 × 0.45 mm pitch | M2.5 × 0.45 mm pitch |
| **Nut Height ($m$)** | 1.60 mm | 1.60 mm | UNVERIFIED |
| **Width Across Flats ($s$)** | 5.0 mm | 5.0 mm | 5.0 mm |
| **Skin Contact** | None (internal cavity, sealed under Kapton) | None (internal cavity, sealed under Kapton) | None (internal cavity, sealed under Kapton) |

#### Impact of Nearest Real Options

1.  **Plated carbon-steel DIN 439 thin nut (plan §4):** same 1.60 mm height and 5.0 mm across flats as the reservation. SKU UNVERIFIED. Zinc plating, not nickel plating, keeps nickel out of the cavity hardware.
2.  **18-8 stainless thin nut (McMaster `90710A025`):** same 1.60 mm and 5.0 mm. Contains 8–10 % nickel. It sits inside the cavity under Kapton and the lid, like the ENIG board finish and the cell's nickel-plated tab, but plan §1 item 4 says "no stainless" and §4's allowance names plated steel and tinned copper only. Rolf decides.
3.  **Titanium DIN 934 full nut (2.0 mm height):** no product page or price is in this file (UNVERIFIED). At nominal the stack still totals 2.63 mm: 0.46 (lug) + 2.00 (nut) + 0.04 (tip) + 0.13 (Kapton). It has no margin: the nut top sits 0.04 mm under the screw tip, so a medial wall printed 0.3 mm thick (MJF ±0.3, plan §3.6) lifts the nut top to y 4.26 and the Kapton to y 4.39, into the board at y 4.30. The thin nut keeps 0.44 mm of margin (see §2.2).

---

### 1.3 Ring Lugs: Sized for M2.5 / #4 Stud, Nickel-Free Finish

The ring lug terminates the biological potential from the screw and crimps to 28 AWG ultra-flexible wire.

#### Verified Sourcing Options for Ring Lugs

| Item | Primary Option: TE Connectivity Budget Ring | Alternative Option: TE Connectivity Solistrand |
| :--- | :--- | :--- |
| **Manufacturer** | TE Connectivity AMP Connectors | TE Connectivity AMP Connectors |
| **Product Family** | Budget Series Uninsulated Terminals | SOLISTRAND Commercial Series |
| **Part Number** | `31428` | `34119` |
| **Distributor** | DigiKey (Part ID: `292150` / `A100688-ND`) | DigiKey (Part ID: `A084-ND` / `34119`) |
| **Product Page URL** | [digikey.com](https://www.digikey.com/en/products/detail/te-connectivity-amp-connectors/31428/292150) | [digikey.com](https://www.digikey.com/en/products/detail/te-connectivity-amp-connectors/34119/18972) |
| **Date Read** | 2026-09-16 | 2026-09-16 |
| **Price** | $0.24 USD (1 unit); $2.08 USD (pack of 10, $0.208/ea) | $0.42 USD (1 unit); $3.25 USD (pack of 10) |
| **Pack Size** | Sold individually | Sold individually |
| **Stud Size** | #4 (Stud hole diameter 0.119 in / 3.02 mm, fits M2.5 shank) | #4 / M2.5 (Stud hole 0.119 in / 3.02 mm) |
| **Wire Gauge** | 22–26 AWG (suitable for 26–28 AWG wire) | 16–22 AWG |
| **Base Material** | High-conductivity Electrolytic Tough Pitch (ETP) Copper | High-conductivity ETP Copper |
| **Finish / Plating** | 100% Matte Pure Tin per ASTM B545 (**Nickel-Free**) | 100% Pure Tin per ASTM B545 (**Nickel-Free**) |
| **Underplate** | None (direct tin on copper; zero nickel barrier) | None (zero nickel barrier) |
| **Stock Thickness** | 0.018 in (0.457 mm ≈ 0.46 mm); under the plan's 0.5 reservation | 0.031 in (0.787 mm) |
| **Tongue Width** | 0.203 in (5.16 mm; clears Ø7.1 mm keep-out) | 0.250 in (6.35 mm) |
| **Overall Length** | 0.453 in (11.51 mm) | 0.550 in (13.97 mm) |
| **Tab Clearance** | Length fits: 11.51 mm overall less the 2.58 mm ring radius is 8.93 mm from the stud, 5.38 mm past the Ø7.1 keep-out, inside the 7 mm tab. Barrel width against the 3 mm tab: UNVERIFIED (not on the page as quoted) | Exceeds floor envelope; requires trimming |

*Assessment:* TE Connectivity Part `31428` is selected as the primary component. Its 0.46 mm stock thickness, 5.16 mm tongue width, and pure tin plating satisfy plan §3.3, §4, and §8 claim 9 on thickness and finish. What it changes: plan §4 asks for a 26–28 AWG barrel; 31428's barrel is rated 22–26 AWG, so a 28 AWG wire is under range. The assembly sheet doubles the stripped end before crimping and solders the crimp (§5.2 step 1).

---

### 1.4 Insulation: Kapton / Polyimide Dielectric Tape

A dielectric disc covers the internal nut and screw tip to isolate the contact from medial PCB components and the battery circuit.

#### Verified Sourcing Options for Kapton Tape

| Item | Primary Option: Adafruit Polyimide Tape Roll | Alternative Option: Bertech Pre-Cut Discs |
| :--- | :--- | :--- |
| **Supplier** | Adafruit Industries | Bertech (via DigiKey) |
| **Product Name** | High Temperature Polyimide Tape (Kapton) | Polyimide Masking Discs (1/4 in) |
| **Part / Product ID** | `3057` | `PPD-1/4` |
| **Product Page URL** | [adafruit.com](https://www.adafruit.com/product/3057) | [digikey.com](https://www.digikey.com) (front page; price UNVERIFIED) |
| **Date Read** | 2026-09-16 | 2026-09-16 |
| **Price** | $4.95 USD | $38.50 USD (pack of 1,000 discs) — UNVERIFIED, no product page |
| **Pack Size** | 1 roll ($10\text{ mm} \times 33\text{ m}$) | Roll of 1,000 pre-cut dots |
| **Substrate** | Polyimide film, 1.0 mil (0.025 mm) | Polyimide film, 1.0 mil (0.025 mm) |
| **Adhesive** | Silicone adhesive, 1.5 mil (0.038 mm) | Silicone adhesive, 1.5 mil (0.038 mm) |
| **Total Thickness** | 2.5 mil (0.064 mm) per layer | 2.5 mil (0.064 mm) per disc |
| **Dielectric Strength** | > 5,000 V | > 5,000 V |
| **Application Note** | Cut two layers with a standard 1/4 in (6.35 mm) punch for 0.128 mm (0.13 mm nominal) | Apply two pre-cut discs for 0.128 mm (0.13 mm nominal) |

---

### 1.5 Chemical Screening: DMG Nickel Spot Test Kit

A Dimethylglyoxime (DMG) test screens incoming metal parts for free leaching nickel.

#### Status of Kits

*   **Nickel Alert (Athena Allergy / nonickel.com):** Listed at $24.99 USD in plan §7; verified UNAVAILABLE on nonickel.com on 2026-09-16 (plan §8 claim 16 confirmed).
*   **Active Substitute:** Delasco "Spot Test For Nickel" is fully stocked and available for direct shipment.

#### Verified Sourcing Details

| Item | Active Primary Kit: Delasco Spot Test For Nickel |
| :--- | :--- |
| **Supplier** | Delasco (Dermatology and Medical Supplies, Council Bluffs, IA) |
| **Product Name** | Delasco SPOT-TEST Spot Test For Nickel |
| **Product SKU / ID** | `SPOT-TEST` (Shopify Product ID: `7512288428109`) |
| **Product Page URL** | [delasco.com](https://www.delasco.com/spot-test-for-nickel/) |
| **Date Read** | 2026-09-16 |
| **Stock Status** | In Stock (verified 2026-09-16) |
| **Price** | $17.99 USD (within §7 Order 2 allowance of $25.00) |
| **Pack Size** | 1/2 oz (15 mL) dropper bottle (provides ~100–150 tests) |
| **Active Reagent** | 1.0% Dimethylglyoxime (DMG) in ammoniacal solution (10.0% Ammonium Hydroxide) |
| **Detection Limit** | Detects free leaching nickel ions at concentrations $\ge 10\text{ ppm}$ |

---

## 2. Mechanical Stack Arithmetic on Catalog Drawings

Plan §3.3 (`CONTACT_STACK`) and plan §9 row WP5 mandate that the total internal stack height above the interior cavity floor must not exceed **2.63 mm**.

### 2.1 Geometric Boundary Conditions

*   **Medial Wall Thickness:** $t_{\text{wall}} = 1.50\text{ mm}$ (from exterior $y = 0.00$ to interior floor $y = 1.50\text{ mm}$).
*   **PCB Underside Datum:** $y_{\text{PCB}} = 4.30\text{ mm}$ (supported on four internal corner pads).
*   **Available Vertical Height Above Floor:** $4.30\text{ mm} - 1.50\text{ mm} = 2.80\text{ mm}$.
*   **Target Stack Ceiling:** $y_{\text{stack\_top}} \le 4.13\text{ mm}$ (stack height above floor $\le 2.63\text{ mm}$).
*   **Nominal Air Clearance to Board Underside:** $4.30\text{ mm} - 4.13\text{ mm} = 0.17\text{ mm}$.

```
  y = 4.30 mm --------------------------------------- [ PCB Underside Datum ]
                     ^  0.17 mm nominal air clearance
  y = 4.13 mm =======v=============================== [ Top of Kapton Disc ]
                     |  0.13 mm Kapton Tape Disc
  y = 4.00 mm -------+------------------------------- [ Tip of M2.5 Screw ]
                     |  0.44 mm Screw Tip Protrusion
  y = 3.56 mm -------+------------------------------- [ Top of DIN 439 Nut ]
                     |  1.60 mm DIN 439 M2.5 Thin Nut
  y = 1.96 mm -------+------------------------------- [ Top of Ring Lug ]
                     |  0.46 mm TE 31428 Ring Lug
  y = 1.50 mm =======+=============================== [ Cavity Floor ]
                     |
                     |  1.50 mm PA12 Medial Wall
                     |
  y = 0.00 mm ======================================= [ Outer Medial Wall Surface ]
                    ( ) 1.35 mm ISO 7380 Button Head Dome
  y = -1.35 mm -------------------------------------- [ Apex of Dome on Skin ]
```

### 2.2 Stack Arithmetic by SKU Set

The table below calculates the total stack height above the cavity floor for each candidate hardware configuration:

$$\text{Clamped Thickness Under Nut} = t_{\text{wall}} + t_{\text{lug}}$$

$$\text{Tip Protrusion Above Nut} = \max\left(0.00,\, L_{\text{screw}} - (t_{\text{wall}} + t_{\text{lug}} + m_{\text{nut}})\right)$$

$$\text{Internal Stack Height Above Floor} = t_{\text{lug}} + m_{\text{nut}} + \text{Tip Protrusion} + t_{\text{Kapton}}$$

| Parameter | SKU Set 1: Primary (RJX Gr2 + McMaster Nut) | SKU Set 2: Specialist (Titane Gr5 + Accu Nut) | SKU Set 3: All-Titanium Full Nut (DIN 934) | SKU Set 4: Non-Compliant (Untrimmed 6mm Screw) |
| :--- | :--- | :--- | :--- | :--- |
| **Nut material** | plated steel (plan §4; SKU UNVERIFIED) or stainless (outside plan text) | stainless A2 (outside plan text) | titanium (SKU UNVERIFIED) | any |
| **Screw Length ($L$)** | 4.00 mm | 4.00 mm | 4.00 mm | 6.00 mm |
| **Medial Wall ($t_{\text{wall}}$)** | 1.50 mm | 1.50 mm | 1.50 mm | 1.50 mm |
| **Ring Lug ($t_{\text{lug}}$)** | 0.46 mm (TE 31428) | 0.46 mm (TE 31428) | 0.46 mm (TE 31428) | 0.46 mm (TE 31428) |
| **Retaining Nut ($m_{\text{nut}}$)** | 1.60 mm (DIN 439) | 1.60 mm (DIN 439) | 2.00 mm (DIN 934) | 1.60 mm (DIN 439) |
| **Total Fastened Grip** | 3.56 mm | 3.56 mm | 3.96 mm | 3.56 mm |
| **Screw Tip Above Nut** | 0.44 mm | 0.44 mm | 0.04 mm | 2.44 mm |
| **Metal Stack Above Floor** | 2.50 mm | 2.50 mm | 2.50 mm | 4.50 mm |
| **Kapton Disc ($t_{\text{Kapton}}$)**| 0.13 mm (2 layers) | 0.13 mm (2 layers) | 0.13 mm (2 layers) | 0.13 mm (2 layers) |
| **Total Stack Above Floor** | **2.63 mm** | **2.63 mm** | **2.63 mm** | **4.63 mm** |
| **Top of Stack ($y$)** | **4.13 mm** | **4.13 mm** | **4.13 mm** | **6.13 mm** |
| **Acceptance ($\le 2.63\text{ mm}$)**| **PASS** | **PASS** | **PASS** | **FAIL** (+2.00 mm clash) |
| **Nut top at wall 1.80 mm (MJF +0.3)** | y 3.86, under the tip at 4.00 | y 3.86 | y 4.26, above the tip | – |
| **Stack top at wall 1.80 mm** | **4.13** (tip governs) | **4.13** | **4.39: above the board at 4.30, FAIL** | – |

Why the lug thickness does not move the total: the screw head seats on the medial face at y 0, so the tip sits at y 4.00 whatever the lug and wall are. The stack top is the higher of the tip and the nut top (wall + lug + nut), plus Kapton. A thicker lug or wall only eats the tip's margin until the nut top passes y 4.00. The plan's reservation (lug 0.50, nut 1.60, tip 0.40, Kapton 0.13) and these SKUs (lug 0.46, nut 1.60, tip 0.44, Kapton 0.13) both total 2.63; `scripts/cad/bte_fit_shell.py` checks the reservation as `CONTACT_STACK`, including wall +0.3.

### 2.3 Thread Engagement Verification

For M2.5 threads (pitch $P = 0.45\text{ mm}$):
*   With a DIN 439 thin nut ($m = 1.60\text{ mm}$), nominal engaged thread length is $1.60\text{ mm}$, providing $1.60 / 0.45 = 3.55$ full threads. This achieves $1.60 / 2.5 = 0.64\times$ nominal bolt diameter. Because mechanical load is limited to preloading the hook against soft tissue (~0.3 N per contact), shear stress in the threads is negligible (< 0.1 MPa vs. 400+ MPa yield strength).
*   With a DIN 934 full nut ($m = 2.00\text{ mm}$), nominal engaged thread length is $2.00\text{ mm}$ ($4.44$ threads, $0.80\times$ diameter).
*   If an M2.5 × 6 mm screw is purchased due to stock shortages, the shank must be ground or filed down by exactly 2.0 mm to nominal 4.0 mm before installation.

---

## 3. Material-Evidence Route and Nickel-Free Verification

### 3.1 Traceability Documentation Hierarchy

To establish that skin-contact hardware meets the biocompatibility standard, the following documentation hierarchy governs part procurement:

```
[ Tier 1: Primary Evidence ]
  EN 10204 Type 3.1 Inspection Certificate
  - Specific heat/lot chemical analysis
  - Direct supplier certification to ASTM F67 (Gr2) or ASTM F136/F1472 (Gr5)
  - Nickel content as the specification states it, not "zero" (plan §4)
          |
          v  (If supplier does not furnish Tier 1 certificate)
[ Tier 2: Secondary Evidence ]
  Supplier Material Declaration of Conformity
  - Written statement of alloy grade (CP Grade 2 or Ti-6Al-4V Grade 5)
  - Traceable lot/batch number on packing slip
          |
          v  (Mandatory verification gate on all receipts)
[ Tier 3: Receipt Chemical Screening ]
  100% Dimethylglyoxime (DMG) Spot-Test Screen
  - Chemical swab on every individual contact dome
  - Reject the lot on any pink reaction
```

### 3.2 Supplier Documentation Availability

| Supplier | Documentation Provided | Conformance Route |
| :--- | :--- | :--- |
| **Titane Services** | EN 10204 Type 3.1 Inspection Certificate available upon request with order (UNVERIFIED: no page cited; ask before ordering). | **Primary Route:** Request EN 10204 3.1 certificate during order placement. |
| **Fastenright Ltd** | EN 10204 3.1 Inspection Certificate available on custom manufacturing orders (UNVERIFIED: no page cited). | **Primary Route:** Order with certified mill cert on file. |
| **RJXHOBBY** | Product specification states "TA2 Pure Titanium" (Chinese national standard GB/T 3620.1 Grade TA2, chemically equivalent to ASTM F67 Grade 2). Mill certificates are not supplied with consumer packs. | **Secondary / Fallback Route:** Supplier invoice specification + 100% receipt DMG screening. |
| **Sortafast Industries**| Product specification states "Grade 5 6Al-4V Titanium". No lot-specific MTC is supplied. | **Secondary / Fallback Route:** Supplier specification + 100% receipt DMG screening. |

### 3.3 Fallback Protocol If No Mill Certificate Is Available

If procurement relies on hobby or retail specialists where an EN 10204 3.1 certificate is unavailable:
1.  **Receipt Lot Testing:** Inspect 100% of received screws under the DMG spot-test protocol (§4). A single positive reaction rejects the entire delivery lot.
2.  **Laboratory XRF Confirmation (Optional Fallback):** If non-destructive confirmation is required prior to human wear, one sacrificial screw from the lot is submitted for handheld X-ray Fluorescence (XRF) spectroscopy to verify that titanium is the base metal ($> 89\%$) and nickel is absent ($< 0.01\%$).

### 3.4 Plain Material Statement: 316 Stainless Steel Is Not a Fallback

> [!CAUTION]
> **316 / 316L Stainless Steel is NOT nickel-free and is NOT an acceptable fallback.**
>
> ASTM F138 / AISI 316L stainless steel contains **10.0% to 14.0% nickel by weight**. While 316L forms a chromium-molybdenum oxide passive film that retards ion release, mechanical abrasion, micro-scratching, and retroauricular sweat acidification (pH 4.5–6.0) can induce nickel leaching.
>
> The binding project specification (`docs/EARPIECE_DESIGN.md` and `docs/fab/plan.md` §2 row 3) mandates strictly nickel-free skin contact. 316L stainless steel cannot be substituted for titanium skin contacts under any circumstance. Changing this requirement is exclusively Rolf's authority.

---

## 4. Dimethylglyoxime (DMG) Spot-Test Protocol

The DMG chemical spot test serves as an empirical fail-closed reject screen. It detects free, leachable nickel ions ($\text{Ni}^{2+}$) at concentrations $\ge 10\text{ ppm}$.

### 4.1 Reagent and Kit Specification

*   **Test Kit:** Delasco Spot Test For Nickel (Product ID: `SPOT-TEST`).
*   **Active Chemistry:** 1.0% Dimethylglyoxime ($\text{C}_4\text{H}_8\text{N}_2\text{O}_2$) dissolved in an ammoniacal solution containing 10.0% Ammonium Hydroxide ($\text{NH}_4\text{OH}$).
*   **Consumables Required:** Medical-grade white cotton swabs / cotton-tipped applicators; 70% isopropanol wipes; powder-free nitrile gloves; clean white ceramic or glass test dish.

### 4.2 Step-by-Step Test Procedure

1.  **Pre-Cleaning:**
    *   Wipe each titanium screw thoroughly with a 70% isopropanol wipe for 15 seconds to remove cutting oils, fingerprints, and handling residue.
    *   Allow the parts to air dry on a clean lint-free surface for 2 minutes.
2.  **Swab Preparation:**
    *   In a well-ventilated area, dispense 2 to 3 drops of the Delasco Spot Test solution onto the tip of a clean white cotton applicator.
    *   Ensure the applicator tip is thoroughly moistened but not dripping.
3.  **Mechanical Friction Application:**
    *   Press the moistened cotton tip firmly against the convex button-head dome ($d_k = 4.7\text{ mm}$) of the screw.
    *   Vigorously rub the swab across the entire convex crown, perimeter rim, and hex drive socket in a firm circular motion for **30 to 60 seconds**.
4.  **Inspection and Color Development:**
    *   Inspect the cotton swab immediately under bright, diffuse white light against a clean white background.

```
       [ DMG COLOR REACTION INTERPRETATION ]

     +-----------------------+     +-----------------------+
     |   CLEAR / NO COLOR    |     |    PINK / STRAWBERRY  |
     |   (Negative Screen)   |     |    (Positive Reaction) |
     +-----------------------+     +-----------------------+
     | Swab remains white or |     | Swab turns pink, red,  |
     | shows faint grey from |     | or purplish-red       |
     | friction dust.        |     | (insoluble Ni-DMG)    |
     +-----------------------+     +-----------------------+
                 |                             |
                 v                             v
           [ PASS LOT ]                 [ REJECT LOT ]
         Proceed to assembly         Quarantine & reject all
```

### 4.3 Interpretation and Pass/Fail Criteria

*   **Negative Reaction (PASS):** The cotton swab remains completely white (or shows faint grey mechanical dirt). This is a screen pass only; it does not prove the absence of leachable nickel (§4.4; plan §4 "a reject screen only"). The screw is accepted for assembly.
*   **Positive Reaction (FAIL / REJECT THE LOT):** Any distinct pink, strawberry-red, or reddish-purple coloration on the cotton tip indicates the formation of the bis(dimethylglyoximato)nickel(II) complex:

$$\text{Ni}^{2+} + 2\,\text{C}_4\text{H}_8\text{N}_2\text{O}_2 + 2\,\text{NH}_4\text{OH} \longrightarrow \text{Ni}(\text{C}_4\text{H}_7\text{N}_2\text{O}_2)_2\downarrow (\text{pink ppt}) + 2\,\text{NH}_4^+ + 2\,\text{H}_2\text{O}$$

*   **Action on Positive Result:** **REJECT THE LOT.** If any single screw from a batch produces a pink reaction, the entire delivery lot is quarantined and rejected. No component from that lot may be used.
*   **Testing Cadence:** 100% of screw domes are tested upon initial receipt. In addition, assembled contacts undergo a confirmatory repeat swab after two weeks of storage per plan §4.

### 4.4 Known Methodological Limitations

Per [Thyssen et al. (2010)](https://pubmed.ncbi.nlm.nih.gov/20536475/), the DMG ammoniacal spot test has an established sensitivity of approximately 59.3% relative to full quantitative 1-week artificial sweat immersion testing (EN 1811:2011+A1:2015). A negative DMG test is an effective screening tool against heavily contaminated or plated items, but it does not prove 0.000% bulk nickel. Material declaration from the supplier remains the primary defense.

---

## 5. Assembly Sheet: Step-by-Step Procedure

### 5.1 Required Tooling and Consumables

*   1.5 mm precision hex key (Wiha or Wera ESD-safe hex driver).
*   5.0 mm miniature thin open-ended wrench or nut driver (the DIN 439 M2.5 nut is 5.0 mm across flats; a 4.0 mm tool does not fit).
*   Lead wire: 28 AWG ultra-flexible stranded silicone wire (e.g., BNTECHGO 28 AWG silicone wire, OD 1.2 mm).
*   Precision wire stripper (rated for 28 AWG).
*   Miniature crimp tool (e.g., Engineer PA-09 or IWISS IWS-2820M) matching TE 31428 barrel.
*   Pre-cut Kapton discs (Ø6.35 mm / 1/4 in) or Adafruit 3057 tape cut to size.
*   70% isopropanol wipes and lint-free swabs.

---

### 5.2 Assembly of Signal Contacts 1 and 2 (Anterior and Posterior PAM)

Each signal contact is located on the body medial wall: Contact 1 at $(u=5.9,\, s=22.0)$, Contact 2 at $(u=10.4,\, s=33.1)$.

```
   [ OUTSIDE SHELL ]          [ 1.5 mm MEDIAL WALL ]           [ INSIDE CAVITY ]

      M2.5 Button Screw                                            TE 31428 Ring Lug
      (Ø4.7 mm Dome)                                             (Oriented toward pad)
             |                                                             |
             v                                                             v
          (=====)=========[==========]===================================(====)====
             ||           [  Ø2.9 mm ]                                     ||
             ||===========[ Pass-thru]=====================================||
             ||           [   Hole   ]                                  [======]  <-- DIN 439 Nut
             ||           [          ]                                  [1.6 mm]      (5 mm AF)
             ||           [==========]=====================================||
                                                                           ||     <-- 0.44 mm Tip
                                                                       =========== <-- Kapton Disc
```

1.  **Preparation:**
    *   Degrease the PA12 shell and screws using 70% isopropanol.
    *   Cut two lengths of 28 AWG silicone wire to 35 mm. Strip 2.5 mm of insulation from one end of each wire.
    *   Fold the stripped 2.5 mm back on itself (the 31428 barrel is rated 22–26 AWG; a single 28 AWG end is under range). Insert it into the barrel of a TE Connectivity 31428 ring lug and crimp with a crimp tool matching that barrel. Flow a little solder into the crimp. Inspect: all strands captured, and the wire does not pull out by hand.
2.  **Screw Insertion:**
    *   Take one inspected, DMG-tested titanium ISO 7380 M2.5 × 4 mm button-head screw.
    *   Insert the screw shank from the **outside** of the shell through the Ø2.9 mm clearance hole in the medial wall. The convex dome seats flush against the outer nylon face.
3.  **Lug Placement:**
    *   Over the protruding M2.5 thread on the cavity floor, slip the ring tongue of the crimped TE 31428 lug.
    *   **Orientation:** Align the flat lug tab to lie flat against the cavity floor, pointing along the reserved routing corridor toward its dedicated medial PCB pad (conforming to `KEEPOUT_SIGNAL`: envelope $3\text{ mm wide} \times 7\text{ mm long} \times 1.5\text{ mm tall}$).
4.  **Nut Fastening:**
    *   Thread an M2.5 DIN 439 thin hex nut onto the screw shank.
    *   Engage a 1.5 mm hex driver into the screw head from outside, and engage a 5.0 mm thin wrench on the internal nut.
    *   **Tightening, by feel:** Tighten until the nut makes solid contact with the lug and resistance rises sharply, then stop ("finger-snug plus 1/8 turn"). Do not crush the nylon wall.
        *   *No torque number is given.* The 0.20–0.25 N·m this sheet first gave had no source. As a check on it: with a nut factor of 0.2, 0.25 N·m on M2.5 is about 500 N of clamp; under the button head (about 10.7 mm² of bearing on a Ø2.9 hole) that is about 47 MPa, close to PA12's compressive yield. UNVERIFIED either way; a bench trial on a printed coupon or gauge would set a number.
5.  **Dielectric Insulation:**
    *   Inspect the top of the fastened stack: verify that the screw tip stands 0.40–0.44 mm proud of the nut.
    *   Apply a double layer of Kapton tape (or two Ø6.35 mm pre-cut dots, total thickness 0.13 mm) centered over the top face of the nut and protruding tip. Press firmly around the edges to conform to the nut facets.
    *   Verify total height above the cavity floor with a depth micrometer or caliper: must be $\le 2.63\text{ mm}$.

---

### 5.3 Assembly of Reference Contact 3 (Tail Pocket)

The reference contact is located in the narrow tail section at $(u=8.5,\, s=43.0)$.

```
                      [ REFERENCE TAIL POCKET ]
                      (Ø7.5 mm, depth 6.5 mm)

     [ Medial Wall ]          [ Pocket Interior ]
           |                           |
           v                           v
     +-----------+            +-----------------+
     |           |            |                 |  <-- Insulated 28 AWG wire
     |           |            |      ^          |      leaves via WIRE_CHANNEL
     |           |            |      | Upright  |
     | (Dome)    |            |      | Lug Tab  |
     |   ===||===+============+======|==========|
     |      ||   | Ø2.9 Hole  |   [=====]       |  <-- DIN 439 Thin Nut
     |      ||===+============+===[=====]=======|
     |           |            |   ( Lug )       |
     +-----------+            +-----------------+
```

1.  **Pocket Geometry:** The tail contains a dedicated cylindrical pocket (Ø7.5 mm, extending from $y = 8.0\text{ mm}$ down to floor $y = 1.5\text{ mm}$). An end wall of 1.05 mm separates this pocket from the main board cavity.
2.  **Lug Tab Preparation:**
    *   Take a TE Connectivity 31428 ring lug. Using smooth flat-nose pliers, bend the terminal crimp barrel **90° upright relative to the flat ring ring plane**.
    *   The upright tab envelope occupies $3\text{ mm wide} \times 1.5\text{ mm thick} \times 6.0\text{ mm tall}$, fitting entirely inside the Ø7.5 mm pocket volume (`KEEPOUT_REF`).
    *   Crimp and solder a 25 mm length of 28 AWG silicone wire into the upright barrel (fold the stripped end, as in §5.2 step 1).
3.  **Fastening:**
    *   Insert an M2.5 × 4 mm titanium screw from the exterior medial face through the Ø2.9 mm hole into the pocket.
    *   Place the bent ring lug over the thread, oriented so the upright tab rises along the posterior interior wall of the pocket.
    *   Thread the M2.5 DIN 439 thin nut and tighten by feel as in §5.2 step 4.
    *   Apply a Kapton dielectric disc over the top of the nut and the screw tip.
4.  **Wire Routing through Wire Channel:**
    *   Feed the insulated 28 AWG wire from the reference pocket through `WIRE_CHANNEL` ($u = 7.7–9.3\text{ mm}$, $y = 2.5–4.1\text{ mm}$, $s = 38.2–40.5\text{ mm}$) through the 1.05 mm end wall into the main cavity.
    *   **Safety Rule:** Only the fully insulated wire passes through the channel. No bare metal terminal or screw extends into or through the channel.
    *   Inside the main cavity, route the wire along the floor ($y = 2.5–4.1\text{ mm}$) under the PCB toward the reference solder pad at $(u=4.0,\, s=29.0\text{ mm})$.
    *   Secure the wire to the floor at $s = 37.0\text{ mm}$ using one wrap of Kapton tape. Maintain wire bend radius $\ge 3.0\text{ mm}$ at all turns.

### 5.4 Before any wear (plan §6)

1.  **Never charge while worn.** Charge only with the earpiece off the ear and the lid removed.
2.  **Tethered bring-up** uses the Ø2.0 side exit with the laptop on battery, not mains. Plug the exit before the earpiece goes back on the ear.
3.  Fit the lid. Nothing but the three titanium domes and the nylon shell may touch skin.

---

## 6. Comprehensive Internal-Metal List

Every metallic component located within or passing through the shell boundary is cataloged below, including its composition, surface plating, mechanical boundary, and potential for skin contact in any failure mode:

| Item No. | Component Description | Quantity | Alloy / Base Material | Plating / Surface Finish | Normal Location | Can Touch Skin in Any Failure? | Analysis & Containment Failure Modes |
| :---: | :--- | :---: | :--- | :--- | :--- | :---: | :--- |
| **1** | Contact Screws (Contacts 1, 2, 3) | 3 | Titanium Grade 2 (ASTM F67) or Grade 5 (ASTM F136) | None (bare, unplated, natural passivated $\text{TiO}_2$) | Shank through 1.5 mm wall; dome on exterior skin | **YES (By Design)** | Intended skin interface. Material is biocompatible titanium; 100% DMG screen verifies absence of leachable nickel. If wall fractures, material remains biocompatible titanium. |
| **2** | Internal Retaining Thin Nuts | 3 | Plated carbon steel per plan §4 (zinc, not nickel; SKU UNVERIFIED); 18-8 stainless only if Rolf accepts it; or titanium DIN 934 | Zinc plating, or none | Threaded onto screws inside cavity/pocket | **NO** | Enclosed inside sealed cavity under PA12 lid; covered by Kapton disc. In the event of lid detachment, nut remains recessed 1.5 mm within the interior pocket. Only total catastrophic crushing of the 1.5 mm nylon shell could liberate the nut. |
| **3** | Ring Tongue Terminals | 3 | High-Conductivity ETP Copper | 100% Pure Matte Tin per ASTM B545 (Zero nickel underplate) | Clamped between inner wall and nut | **NO** | Enclosed inside sealed cavity; covered by Kapton and snap lid. Tin-plated copper is non-sensitizing even if exposed, but physical exposure is impossible without shell wall destruction. |
| **4** | Lead Wires (Signal & Reference) | 3 | High-Purity Copper Strands | 100% Pure Tin | Inside cavity and reference channel | **NO** | Jacketed in medical-grade silicone/PTFE insulation along full length. Only insulated jacket passes through `WIRE_CHANNEL`. |
| **5** | Solder Joints (Lead to Board) | 3 | Lead-Free SAC305 (96.5% Sn, 3.0% Ag, 0.5% Cu) | None | Medial PCB pads | **NO** | Enclosed at $y = 4.3\text{ mm}$, isolated by 1.5 mm nylon wall and snap lid. Solder alloy is nickel-free and lead-free. |
| **6** | PCB Copper Traces & Pads | 1 board | Copper foil | Electroless Nickel Immersion Gold (ENIG) or OSP | PCB top and bottom faces | **NO** | Enclosed in cavity. ENIG contains an electroless nickel barrier under 0.05 µm gold; however, the entire medial PCB surface is coated in liquid photoimageable (LPI) solder mask except for the 3 lead pads. Board is isolated from skin by 1.5 mm PA12 wall. |
| **7** | Li-Ion Battery Cell & Tabs | 1 cell | Aluminum (positive tab), Nickel-plated copper (negative tab) | Aluminum pouch laminate | Battery pocket ($s = 1.5–17.5\text{ mm}$) | **NO** | Fully sealed inside pouch. Pouch is wrapped in Kapton; battery pocket is isolated from the board zone by an internal transverse nylon rib ($s = 17.5–18.3\text{ mm}$) and enclosed under the snap lid. |
| **8** | Front-End Protection Components | 6 parts | Silicon dies, copper leadframes | Pure Tin (leadframe finish) | Medial PCB surface | **NO** | SOT-23 diode clamps and 0402 resistors are soldered to board; enclosed in cavity. |
| **9** | Temporary Debug Exit Port Plug | 1 | PA12 or Silicone Elastomer | None (non-metallic) | Ø2.0 mm side wall exit at $s = 36\text{ mm}$ | **NO** | The debug cable exit is plugged during wear. No metal conductor extends through the wall during active sessions. |
| **10** | Radio module (Raytac MDBT50Q-1MV2) shield can and pads | 1 | UNVERIFIED (WP6 names the part; shield cans are commonly nickel-silver or tin-plated steel) | UNVERIFIED | Lateral side of the board, under the lid | **NO** | Inside the closed cavity; faces the lid, not the medial wall. |
| **11** | ICs: ADS1292, charger, LDO | 3 | Copper leadframes / solder balls | UNVERIFIED (WP6) | Board, medial side and either side | **NO** | Inside the closed cavity. |
| **12** | 0402 passives (about 25) | ~25 | Nickel barrier under tin on the terminations (typical for chip parts; UNVERIFIED per SKU) | Tin | Board | **NO** | Inside the closed cavity. |
| **13** | Cell protection board (PCM) and its strips | 1 | Nickel or nickel-plated strips typical (UNVERIFIED; WP6 names the cell) | – | Folded on the cell's lateral face under Kapton | **NO** | Inside the battery pocket under the lid. |
| **14** | Charge pads on the board | 2 | Copper | ENIG or OSP (UNVERIFIED; WP6) | Board, reached with the lid off | **NO** | Inside the cavity; used only off the ear (plan §6). |
| **15** | Order 1 gauge ballast: two M6 nuts | 2 | Steel, plating as bought (often zinc; UNVERIFIED) | As bought | Loose in the gauge cavity for plan §3.7 | **NO while the lid holds** | Gauge only, not Stage B. If the lid comes off during the shake test the nuts can fall out; use zinc-plated or stainless nuts you already know you tolerate. |

Nickel inside the cavity already exists in this design: the ENIG finish (item 6), the cell's negative tab (item 7), and likely the passives and PCM (items 12, 13). Plan §4 accepts metal "under the lid" that "never see[s] skin"; the plan's nut allowance still names plated steel and tinned copper, not stainless (§1.2).

---

## 7. Quality Assurance Checklist for S1 Gate Entry

Before order 2 (S1 per plan §9), each line needs evidence on file. Nothing is ticked: this file is a desk specification, and nothing was bought, received or tested. Status as of review r1:

1.  [ ] **Screws:** a titanium ISO 7380 M2.5 × 4 SKU with a product page, date, price and a head drawing. Status: Titane Services has a product URL; RJXHOBBY and Sortafast prices have home-page URLs only; no head drawing (§1.1).
2.  [ ] **Nuts:** a DIN 439 M2.5 thin nut in a material the plan allows, with page, date, price. Status: no plated-steel SKU; stainless SKUs need Rolf's decision (§1.2).
3.  [ ] **Lugs:** TE 31428 page, date, price on file (0.46 mm, tin over copper). Status: page cited; barrel width against the 3 mm tab UNVERIFIED.
4.  [ ] **Kapton:** Adafruit 3057 page, date, price on file. Status: cited.
5.  [ ] **DMG kit:** Delasco SPOT-TEST page, date, price on file. Status: cited; protocol in §4.
6.  [x] **Stack arithmetic:** 2.63 mm at nominal on the chosen parts, with wall +0.3 checked. Status: done in §2.2 on the listed numbers.
7.  [ ] **Internal-metal list** covers every metal WP1 and WP6 place inside the shell. Status: items 10–14 wait on WP6 part names.
8.  [x] **316 statement:** 316/316L is not nickel-free and is not a skin-contact fallback (§3.4).
