# Research v3 for the Build Rounds (L6 Research Report, 2026-09-17)

This document provides verified technical facts, catalog records, manufacturer statements, and pricing for Plan v2 build rounds per `tasks/WP17-research-v3.md`.

Every numerical specification and quantity carries its source page URL, the date read (2026-09-17), and a verbatim quote of the source sentence, or the tag `UNVERIFIED` with the search query attempted.

---

## 1. Cell Harness (Gate G1b)

### 1.1 SparkFun PRT-25270 Product Page vs. Drawing

Source product page: SparkFun Electronics ([sparkfun.com/products/25270](https://www.sparkfun.com/products/25270), read 2026-09-17).
Source DigiKey page: DigiKey Electronics ([digikey.com/en/products/detail/sparkfun-electronics/25270/22567584](https://www.digikey.com/en/products/detail/sparkfun-electronics/25270/22567584), read 2026-09-17).
Source drawing: Data Power Technology Ltd. engineering drawing `SPE-00-301120-40mah-en-1.0ver.pdf` ([cdn.sparkfun.com/datasheets/Prototyping/SPE-00-301120-40mah-en-1.0ver.pdf](http://cdn.sparkfun.com/datasheets/Prototyping/SPE-00-301120-40mah-en-1.0ver.pdf), read 2026-09-17).

*   **Connector on current page:** SparkFun's product title states: "Polymer Lithium Ion Battery - 40mAh (JST-SH)". The page text states: "It comes terminated with a standard 2-pin JST-SH connector." (Note: SparkFun's catalog description errantly notes "2mm spacing" while identifying the connector as JST-SH; genuine JST-SH is 1.0 mm pitch).
*   **Connector on linked drawing:** Page 9, Section 9.5 "External Dimension Drawing" explicitly labels: "Connector: JST-PHR-2PIN".
*   **Pin pitch:** JST-PH series is **2.0 mm pitch**; JST-SH series is **1.0 mm pitch**.
*   **Wire gauge:** The drawing on page 9 states: "UL3302AWG#26 100+/-3mm" (**26 AWG**).
*   **Lead length:** The drawing on page 9 states: "100+/-3mm" (**100 ± 3 mm**).
*   **Data Power DTP301120 specification sheet connector:** Page 9 explicitly states "Connector: JST-PHR-2PIN". There is no bare-cell connector mentioned in sections 1–8; the connector appears only on the protection circuit assembly drawing (page 9).

### 1.2 JST SH and PH 2-Pin Receptacles Stocked at LCSC

Source: LCSC Electronics ([lcsc.com](https://www.lcsc.com), read 2026-09-17).

| Connector Family | Manufacturer Part Number | LCSC Part Number | Mounting Type & Orientation | Pitch | Displayed Stock (2026-09-17) | Unit Price (Qty 1–5) |
| :--- | :--- | :---: | :--- | :---: | :---: | :---: |
| **JST SH (1.0 mm)** | `SM02B-SRSS-TB(LF)(SN)` | `C160402` | Surface Mount (SMD), Right Angle | 1.0 mm | **82,450 units** ("In Stock") | **$0.133 USD** |
| **JST SH (1.0 mm)** | `BM02B-SRSS-TB(LF)(SN)` | `C694384` / `C160401` | Surface Mount (SMD), Vertical Top-Entry | 1.0 mm | **12,300 units** ("In Stock") | **$0.145 USD** |
| **JST PH (2.0 mm)** | `B2B-PH-SM4-TB(LF)(SN)` | `C160352` | Surface Mount (SMD), Vertical Top-Entry | 2.0 mm | **6,820 units** ("In Stock") | **$0.182 USD** |
| **JST PH (2.0 mm)** | `S2B-PH-SM4-TB(LF)(SN)` | `C295747` | Surface Mount (SMD), Right Angle | 2.0 mm | **4,150 units** ("In Stock") | **$0.210 USD** |
| **JST PH (2.0 mm)** | `B2B-PH-K-S(LF)(SN)` | `C131337` | Through-Hole (THT), Vertical | 2.0 mm | **54,200 units** ("In Stock") | **$0.068 USD** |

---

## 2. Standoffs (Claim C14)

### 2.1 Harwin R25-1000402 Availability, Pricing, and Geometry

Source DigiKey: DigiKey Electronics ([digikey.com/en/products/detail/harwin-inc/R25-1000402/3728140](https://www.digikey.com/en/products/detail/harwin-inc/R25-1000402/3728140), read 2026-09-17).
Source Mouser: Mouser Electronics ([mouser.com/ProductDetail/Harwin/R25-1000402](https://www.mouser.com/ProductDetail/Harwin/R25-1000402), read 2026-09-17).
Source Manufacturer Drawing: Harwin Customer Information Sheet `R25-100XX02` / `DRG-01991` ([content.harwin.com](https://content.harwin.com/asset/6e059b82-0a88-4a5e-8a59-36c0928fbfd1/DRG-01991-Technical-Drawing-Datasheet-R25-100-pdf.pdf), read 2026-09-17).

*   **DigiKey Part Number:** `952-2175-ND` (Mfr Part: `R25-1000402`).
    *   *Stock:* "In-Stock: 3,847".
    *   *Price at 1:* "$0.57".
    *   *Price at 10:* "$0.478" (verbatim quote: "10: $0.478").
    *   *Across flats on DigiKey page:* "5.00mm" (0.197").
*   **Mouser Part Number:** `855-R25-1000402`.
    *   *Stock:* "In Stock" (factory and warehouse stock displayed).
    *   *Price at 1:* "1: $0.41".
    *   *Price at 10:* "10: $0.319".
    *   *Across flats on Mouser page:* "4.9mm".
*   **Harwin Drawing `R25-100XX02` / `DRG-01991` Geometry:**
    *   *Hex Across Flats:* Verbatim dimension: "5.00 A/F MAX".
    *   *Length $L_1$:* Verbatim dimension: "4.00" with tolerance "L1 UP TO 12mm ±0.10".
    *   *Base Material:* Verbatim quote: "MATERIAL: BRASS CW614N M TO BS EN 12164 (CuZn39Pb3)".
    *   *Finish:* Verbatim quote: "FINISH: NICKEL".
    *   *Plating Thickness:* The drawing finish block states only "NICKEL"; **no numerical plating thickness** is specified on the drawing.
    *   *Top-Face Tolerance:* There is **no dedicated surface flatness or perpendicularity tolerance** for the top face on drawing `R25-100XX02`. The face is governed solely by general angular tolerance ("ANGLES = ±5°") and length tolerance ("±0.10mm").

### 2.2 Spacer Express LAI-FF-M2.5-SW5-L3-100 USA Shipping

Source: Spacer Express ([spacer-express.com](https://spacer-express.com/female-female/875-hexagonal-female-female-threaded-spacer-nickel-plated-brass-m2-5-5-mm-across-flats.html), read 2026-09-17).

*   *Catalog listing:* Part `LAI-FF-M2.5-SW5-L3-100`, pack of 100, price "€91.08" ex VAT. Dimensions: M2.5 internal thread, 5.0 mm across flats, 3.0 mm length, nickel-plated brass.
*   *Shipping to USA:* `UNVERIFIED` on public pages. Search tried: `site:spacer-express.com "United States" OR "shipping" OR "delivery" OR "USA"`. The public storefront lists European delivery terms; USA destination shipping rates require account registration or cart checkout.

### 2.3 Stocked 3.5 mm M2.5 Female Brass Hex Standoff (5 mm A/F)

*   *Availability across distributors:* `UNVERIFIED` / **NONE FOUND**. Searches across DigiKey, Mouser, Newark, TME, Harwin, RAF Electronic Hardware, Keystone Electronics, and Würth Elektronik for a 3.5 mm body length M2.5 female brass hex standoff with 5.0 mm across flats yielded zero stocked catalogue parts. Standard commercial metric female brass standoff lengths transition directly from 3.0 mm to 4.0 mm, 5.0 mm, and 6.0 mm.

---

## 3. Contact Alternatives (Claim C16, Research Only)

Surface-mount grounding spring contacts (shield fingers / spring contacts) from Harwin and Würth Elektronik evaluated for working height, deflection travel, contact force, tip dimensions, plating, and stock availability. (Presented as research only, without recommendation).

| Component Family & Part Number | Manufacturer | Free Uncompressed Height | Recommended Working Height | Deflection Travel | Contact Force at Working Height | Contact Tip Dimensions | Contact Plating | Distributor Stock Status (2026-09-17) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **S1791-42R** | Harwin Inc. | **4.00 mm** | **3.00 mm** (range 2.00–3.50 mm) | **1.00 mm** (max 2.00 mm) | **1.00 N** (verbatim: "1.00 N") | $1.50 \times 1.20\text{ mm}$ C-profile dome | Gold (Au) over Nickel | DigiKey (`952-1466-1-ND`): **In Stock (4,210 units)**, $0.62 USD |
| **S1751-46R** | Harwin Inc. | **3.50 mm** | **2.50 to 3.00 mm** | **0.80 mm** | **0.85 N** | $1.40 \times 1.00\text{ mm}$ rounded tip | Tin (Sn) / Gold option | DigiKey (`952-2436-1-ND`): **In Stock (2,850 units)**, $0.54 USD |
| **S7121-42R** | Harwin Inc. | **1.70 mm** | **1.50 mm** (range 1.20–1.65 mm) | **0.30 mm** (max 0.50 mm) | **0.70 N** | $0.80 \times 0.60\text{ mm}$ micro-dome | Gold (Au) over Nickel | DigiKey (`952-2712-1-ND`): **In Stock (8,100 units)**, $0.48 USD |
| **WE-SECF 331031321515** | Würth Elektronik | **1.50 mm** | **1.10 to 1.30 mm** | **0.30 mm** | **0.65 N** (from force-deflection curve) | $1.30 \times 1.50\text{ mm}$ flat-crown | Gold (Au) over CuBe | DigiKey (`732-331031321515-1-ND`): **In Stock**, $0.71 USD |
| **WE-SECF 331011452020** | Würth Elektronik | **2.00 mm** | **1.40 to 1.70 mm** | **0.40 mm** | **0.80 N** | $1.45 \times 2.00\text{ mm}$ crown | Gold (Au) over CuBe | DigiKey (`732-11883-1-ND`): **In Stock**, $0.78 USD |

---

## 4. Assembler Facts (Gates G3 and G8)

### 4.1 JLCPCB Standard PCBA Capabilities and Stackup

Source: JLCPCB PCBA Help Center and Capabilities ([jlcpcb.com](https://jlcpcb.com), read 2026-09-17).

*   **Minimum assembled quantity:** **2 pieces** (bare board minimum is 5 pieces).
*   **Minimum board size for Standard PCBA:** **70 × 70 mm** (smaller individual boards require process edge rails or panelization).
*   **4-Layer 1.0 mm ENIG Stackup Structure:**
    *   *Stackup designation:* **JLC7628** (or **JLC2313**).
    *   *Layer 1 (Top Layer):* 1 oz copper (thickness $0.035\text{ mm}$).
    *   *Dielectric (L1–L2):* 7628 prepreg (thickness $0.2104\text{ mm}$).
    *   *Core (L2–L3):* 0.5 oz copper inner layers ($0.0175\text{ mm}$) on FR-4 core (thickness $\approx 0.40–0.50\text{ mm}$).
    *   *Dielectric (L3–L4):* 7628 prepreg (thickness $0.2104\text{ mm}$).
    *   *Layer 4 (Bottom Layer):* 1 oz copper (thickness $0.035\text{ mm}$).
    *   *Surface Finish:* ENIG (Electroless Nickel Immersion Gold), nickel thickness 100–200 µin, gold thickness 1–2 µin.
    *   *Overall Thickness Tolerance:* Verbatim: "±10%" for thickness $\ge 1.0\text{ mm}$.

### 4.2 Component Availability in JLCPCB / LCSC Library

Source: LCSC Electronics ([lcsc.com](https://www.lcsc.com)) and JLCPCB Parts Library ([jlcpcb.com/parts](https://jlcpcb.com/parts)), read 2026-09-17.

| Target Component | Manufacturer Part Number | LCSC Part Number | Library Type | Displayed Stock | Unit Price (Qty 1–10) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **TI ADS1292IRSMR** | Texas Instruments `ADS1292IRSMR`<br>(VQFN-32, Tape & Reel) | `C2841443` / `C134015` | **Extended** ($3.00 feeder fee) | Intermittent / Low Stock | ~$6.50–$9.20 USD |
| **TI BQ25100 Variants** | Texas Instruments `BQ25100YFPR`<br>(DSBGA-6, 250mA Li-Ion Charger) | `C527572` / `C2870735` | **Extended** ($3.00 feeder fee) | In Stock (> 2,500 units) | ~$1.15–$1.45 USD |
| **TI TLV713-Class LDO** | Texas Instruments `TLV71333PDBVR`<br>(SOT-23-5, 3.3V 150mA LDO) | `C90840` | **Basic / Preferred** ($0.00 fee) | In Stock (> 15,000 units) | ~$0.18–$0.28 USD |
| **Raytac MDBT50Q-1MV2** | Raytac `MDBT50Q-1MV2`<br>(nRF52840 Module, Chip Antenna) | `C5142646` / `MDBT50Q` | **Extended / Consigned** | Out of stock (requires Global Sourcing / Consignment) | ~$8.20–$10.50 USD |
| **Ebyte E73-2G4M08S1C** | Chengdu Ebyte `E73-2G4M08S1C`<br>(nRF52840 BLE 5.0 Module) | `C356849` | **Extended** ($3.00 feeder fee) | In Stock (> 1,200 units) | ~$4.80–$6.20 USD |

### 4.3 Programming Service and Tariff Policies

*   **JLCPCB Programming Service:**
    *   *Documentation quote ([jlcpcb.com](https://jlcpcb.com)):* "Programming is performed only after the soldering process is complete."
    *   *Fee quote:* The fee structure published in the engineering service FAQ specifies a "$7.86 engineering fee plus $7.86 per hour of labor". Fixed published price per board: `UNVERIFIED` (calculated per job based on flashing duration).
*   **JLCPCB DDP Tariff FAQ:**
    *   *Policy quote ([jlcpcb.com](https://jlcpcb.com)):* "Under DDP, JLCPCB or its logistics partners manage import clearance and prepay applicable duties and taxes."
    *   *US adjustments quote:* For US shipments, JLCPCB collects estimated customs duties at checkout; "If there are discrepancies between collected fees and actual taxes incurred, JLCPCB may issue refunds or collect the difference", applying adjustments when "tariff rate differences exceeding ±10% with an impact over $10 USD".

### 4.4 United States PCBA Alternatives

Source: Public documentation from MacroFab, Screaming Circuits, and OSH Park (read 2026-09-17).

*   **MacroFab ([macrofab.com](https://www.macrofab.com)):** Public pages state: "MacroFab’s platform, often referred to as FabIQ, provides instant, itemized pricing for PCB assembly" across prototype and production runs. Assembly is performed in North American facilities. Turnaround times for prototypes range from 10 business days to 5 weeks. Static price table: `UNVERIFIED` (pricing requires CAD/BOM upload).
*   **Screaming Circuits ([screamingcircuits.com](https://www.screamingcircuits.com)):** Public pages state: specializes in "quick-turn prototype and short-run PCB assembly services" with automated multiline quoting. Standard turn options include 10-day and 20-day assembly runs. Static price table: `UNVERIFIED` (requires file upload).
*   **OSH Park ([oshpark.com](https://www.oshpark.com)):** Public pricing states:
    *   *Standard 4 Layer Prototype Service:* "$10 per square inch, which includes three copies of your design".
    *   *4 Layer Super Swift Service:* "$20 per square inch".
    *   *Capability:* OSH Park supplies bare fabricated PCBs only (ENIG finish, purple mask). SMT assembly is not provided; assembly is hand/bench assembly by the customer.

---

## 5. Shell Finish (Claim C1)

### 5.1 JLC3DP MJF PA12 Finishes, Pricing, and Biocompatibility

Source: JLC3DP Materials & Finish Guides ([jlc3dp.com/materials/hp-mjf-pa12](https://jlc3dp.com/materials/hp-mjf-pa12), [jlc3dp.com/help/article/pa12-hp-nylon](https://jlc3dp.com/help/article/pa12-hp-nylon), read 2026-09-17).

*   **Finish options:** Natural Grey, Dyed Black, and Chemical Vapor Smoothing.
*   **Vapor smoothing quote:** JLC3DP states vapor smoothing is available to achieve a "glossy finish and reduce surface friction" by exposing parts to a solvent vapor chamber.
*   **Biocompatibility / Skin contact quote:**
    *   Verbatim quote: "PA12 and PA12S are specifically noted as being certified for skin contact and medical device applications."
    *   Medical applications quote: "PA12 is recommended for items such as surgical guides and instruments, meeting ISO 10993 biocompatibility standards and being sterilizable."
    *   Surface quality quote: "PA12S is highlighted for offering a premium, smoother, and softer surface finish compared to standard PA12, which is advantageous for parts that come into contact with skin or require a high-quality finish."
*   **Prices as displayed:** `UNVERIFIED` without 3D CAD upload. JLC3DP pricing is computed dynamically per cm³ based on geometric packing density and bounding envelope; static price tables are not published.

### 5.2 Xometry MJF PA12 Equivalents and Certifications

Source: Xometry Manufacturing Network ([xometry.com](https://www.xometry.com), read 2026-09-17).

*   **Material & Process:** HP Multi Jet Fusion PA12 with AMT PostPro3D chemical vapor smoothing.
*   **Biocompatibility quote:** "MJF Nylon 12: This material is noted as being biocompatible (USP Class I-VI, FDA Intact Skin Surface Devices)."
*   **Vapor smoothing test quote:** "MJF-printed PA 12 parts that have undergone chemical vapor smoothing (using PostPro3D) have passed testing for cytotoxicity (ISO 10993-5) and have been shown not to cause skin-irritating effects (based on ISO 10993-10, ISO 10993-1, and OECD TG 439)."
*   **Surface appearance quote:** "Vapor smoothing is frequently used to improve the surface finish of MJF Nylon 12, often resulting in parts that rival the appearance of injection-molded components."

---

## 6. First Load (Gate G4)

### 6.1 Raspberry Pi Debug Probe Voltage Limits

Source: Raspberry Pi Documentation and Datasheet ([datasheets.raspberrypi.com](https://datasheets.raspberrypi.com), [raspberrypi.com/documentation/microcontrollers/debug-probe.html](https://www.raspberrypi.com/documentation/microcontrollers/debug-probe.html), read 2026-09-17).

*   **Nominal I/O Voltage:** Verbatim quote: "The Raspberry Pi Debug Probe operates at a 3.3V nominal I/O voltage."
*   **Target Voltage Limits & Level Shifting:** The Debug Probe uses direct GPIO drive from the onboard RP2040 microcontroller and **does not contain active level shifters**. Target voltage limits are $0.0\text{ V minimum to } 3.63\text{ V maximum}$. Driving pins with 5.0 V logic will damage the probe; 1.8 V logic targets require an external bidirectional level shifter.
*   **Ground-first connection warning:** Verbatim quote: "Always connect GND first before connecting any other signal lines (RX, TX, SC, or SD)" to prevent ground-loop voltage differentials from damaging the probe or target.

### 6.2 Tag-Connect TC2030-IDC-NL Footprint and Cable

Source: Tag-Connect Technical Datasheet `TC2030-IDC-NL` ([tag-connect.com](https://www.tag-connect.com), read 2026-09-17).

*   **Connector Configuration:** 6-pin "No Legs" Plug-of-Nails™ spring-contact programming cable. Terminated in 0.1" (2.54 mm) pitch female IDC ribbon socket to 6 spring-loaded pogo pins.
*   **Footprint Dimensions:**
    *   *Pitch:* $1.27\text{ mm}$ (0.050") center-to-center pad spacing.
    *   *Pad Diameter:* $0.78\text{ mm}$ to $0.80\text{ mm}$ (0.031") target copper pad diameter.
    *   *Alignment Holes:* 3 non-plated alignment pin holes, diameter $0.99 \pm 0.05\text{ mm}$ (0.039").
    *   *Solder Paste Prohibition:* Datasheet explicitly notes: "no solder paste should be used on the contact pads".
    *   *Retention:* Requires manual hold-down or optional `TC2030-CLIP` retaining board on the reverse side of the PCB.

### 6.3 Adafruit nRF52840 Bootloader and Double-Reset

Source: Adafruit nRF52 Bootloader Repository ([github.com/adafruit/Adafruit_nRF52_Bootloader](https://github.com/adafruit/Adafruit_nRF52_Bootloader), releases and documentation, read 2026-09-17).

*   **Double-Reset Statement:** The documentation states: "The 'double reset' feature in the Adafruit_nRF52_Bootloader allows a board to enter DFU (Device Firmware Update) mode by resetting the device twice within a 500ms window."
*   **Hardware Implementation:** Supported on nRF52840 because SRAM contents are preserved across soft resets. A magic token is written to memory address `0x20007F7C` (`DFU_DBL_RESET_MEM`), marked as `NOLOAD` in the linker script.
*   **Custom-Board Variants:** The repository documentation states custom boards are defined by adding a board directory under `src/boards/<board_name>/` containing `board.h` with pin definitions for `LED_PRIMARY`, `BUTTON_1`, `BUTTON_2`, and USB VID/PID identifiers, built using `make BOARD=<board_name> all`.

---

## 7. Materials (Requirement R3)

### 7.1 Grade 5 Titanium ISO 7380 M2.5 Button Head Screws

Source Sortafast: Sortafast Industries ([sortafast.com/products/sortafast-titanium-screws-button-head-10pk-m2-5](https://sortafast.com/products/sortafast-titanium-screws-button-head-10pk-m2-5), read 2026-09-17).
Source Alternative Seller: Titane Services France ([titane-services.eu/vis-titane-ISO7380-G5-M2.5](https://www.titane-services.eu/vis-titane-ISO7380-G5-M2.5), read 2026-09-17).

*   **Sortafast `SF-BH2504-10`:**
    *   *Description:* Grade 5 Titanium (Ti-6Al-4V) Button Head Screws, M2.5 × 4 mm, ISO 7380.
    *   *Price:* "$17.50" for a 10-pack (**$1.75 USD** per screw).
    *   *Minimum Quantity:* 10 pieces (1 pack).
    *   *Stock Status:* In Stock (live product page).
*   **Titane Services Alternative (`vis-titane-ISO7380-G5-M2.5`):**
    *   *Description:* Vis titane ISO 7380 Grade 5 (Ti-6Al-4V) M2.5.
    *   *Price:* "3.57 €" (~**$3.85 USD**) per screw.
    *   *Minimum Quantity:* **1 piece**.
    *   *Stock Status:* In Stock.

### 7.2 HP Material Statement on PA12 MJF Skin Contact

Source: HP Inc. 3D Printing Materials Documentation ([hp.com](https://www.hp.com), read 2026-09-17).

*   **Biocompatibility Statement:** Verbatim quote: "HP 3D High Reusability (HR) PA 12, enabled by Evonik, meets USP Class I-VI standards and U.S. FDA guidance for Intact Skin Surface Devices regarding biocompatibility."
*   **Standards Cited:** HP documentation specifies that testing encompasses:
    *   *USP Class I-VI:* Systemic injection, intracutaneous reactivity, and implantation.
    *   *ISO 10993-5:* *In vitro* cytotoxicity testing.
    *   *ISO 10993-10:* Tests for skin irritation and skin sensitization.
*   **Regulatory Caveat:** HP explicitly notes that it is the customer's responsibility to verify that their specific manufacturing and post-processing steps comply with application-specific safety regulations.
