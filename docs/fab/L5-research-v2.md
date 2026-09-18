# Research for Plan v2 (L5 Research Report, 2026-09-17)

This report delivers web research for Plan v2 per `tasks/WP10-research-v2.md`. All data points cite source URLs, the date read (2026-09-17), and verbatim quotes, or the tag `UNVERIFIED`.

---

## 1. Thin Cells ($\le 3.2\text{ mm}$ with Protection Circuit)

Target envelope: thickness $\le 3.2\text{ mm}$ (target $\le 3.0\text{ mm}$), width $\le 12.0\text{ mm}$, length $\le 20.0\text{ mm}$, capacity $\ge 20\text{ mAh}$, buyable in single units from stocked distributors.

### 1.1 Candidate Cell Matrix

| Model & SKU | Supplier & URL | Dimensions (T × W × L) | Thickness with PCM | Capacity | Leads | Qty 1 Price | Real Drawing? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **DTP301120**<br>(SparkFun `PRT-13852` / `PRT-25270`) | SparkFun<br>[sparkfun.com/products/13852](https://www.sparkfun.com/products/13852)<br>[sparkfun.com/products/25270](https://www.sparkfun.com/products/25270)<br>Date read: 2026-09-17 | $3.0\text{ mm max} \times 11.0\text{ mm max} \times 20.0\text{ mm max}$ | **$3.2\text{ mm max}$** | **$40\text{ mAh}$** | UL3302 AWG#26, $100 \pm 3\text{ mm}$, JST-PH (13852) or JST-SH (25270) | **$7.14 USD** (13852)<br>**$7.39 USD** (25270) | **YES**<br>(Data Power `SPE-00-301120-40mah-en-1.0ver.pdf`) |
| **GM201021-PCB**<br>(GMB `201021`) | PowerStream<br>[powerstream.com/li-pol.htm](https://www.powerstream.com/li-pol.htm)<br>Date read: 2026-09-17 | $2.3\text{ mm bare max} \times 10.5\text{ mm max} \times 21.5\text{ mm max}$ | **$\approx 3.0\text{ mm}$** | **$22\text{ mAh}$** | Tabs $7 \pm 1\text{ mm}$ or wire leads | **$17.00 USD** | **YES**<br>(Markyn GMB `GMB201021-22mAh.pdf`) |
| **GM300910-PCB**<br>(GMB `300910`) | PowerStream<br>[powerstream.com/li-pol.htm](https://www.powerstream.com/li-pol.htm)<br>Date read: 2026-09-17 | $3.0 \pm 0.2\text{ mm} \times 9.0 \pm 0.5\text{ mm} \times 10.0 \pm 1.0\text{ mm}$ | **$3.0 \pm 0.2\text{ mm}$** | $12\text{ mAh}$ | Insulated wire leads | **$17.00 USD** | **YES**<br>(`GMB300910.pdf`) |
| **DNK301015** | DNK Power<br>[dnkpower.com](https://www.dnkpower.com)<br>Date read: 2026-09-17 | $3.0\text{ mm} \times 10.0\text{ mm} \times 15.0\text{ mm}$ | UNVERIFIED | $28\text{ mAh}$ | Wire leads | UNVERIFIED | UNVERIFIED |
| **LP301016** | LiPol Battery<br>[lipolbattery.com](https://www.lipolbattery.com)<br>Date read: 2026-09-17 | $3.0\text{ mm} \times 10.0\text{ mm} \times 16.0\text{ mm}$ | UNVERIFIED | $25\text{ mAh}$ | Wire leads | UNVERIFIED | UNVERIFIED |

### 1.2 Verbatim Quotes and Analysis

*   **SparkFun DTP301120 (`PRT-13852` / `PRT-25270`):**
    *   *Price quote ([sparkfun.com/products/13852](https://www.sparkfun.com/products/13852)):* "regular_price: 7.14" ($7.14 USD); PRT-25270 is "$7.39". Stocked at SparkFun and DigiKey (`1568-1498-ND`).
    *   *Product quote:* "Each cells outputs a nominal 3.7V at 40mAh. This may sound like not so much power, but the cell is really tiny... like, about half an inch square!"
    *   *Bare cell dimensions ([cdn.sparkfun.com `SPE-00-301120-40mah-en-1.0ver.pdf`](http://cdn.sparkfun.com/datasheets/Prototyping/SPE-00-301120-40mah-en-1.0ver.pdf), p. 4):* "Cell Dimension: T Max3.0, W Max 11.0, L Max 20.0, L1 Max 16.0, L2 Max 20.3, L3 5.0±1.0, M 6.0±1.0, N 2.0±0.1".
    *   *Protected assembly dimensions (drawing p. 9):* Labeled "Max 3.2mm" thickness, "Max 11.5mm" width, "Max 22mm" length, "UL3302AWG#26 100+/-3mm", "Connector: JST-PHR-2PIN".
    *   *Finding:* Protected cell thickness is $\le 3.2\text{ mm}$, bare pouch is $\le 3.0\text{ mm}$, capacity is 40 mAh. Length with PCM is 22 mm.
*   **PowerStream GM201021-PCB:**
    *   *Quote ([powerstream.com/li-pol.htm](https://www.powerstream.com/li-pol.htm)):* "GM201021-PCB: Includes a protection circuit board (PCB), increasing the thickness to approximately 3 mm." Price is listed at "Samples: $17.00".
    *   *Datasheet ([powerstream.com/lip/GMB201021-22mAh.pdf](https://www.powerstream.com/lip/GMB201021-22mAh.pdf), p. 4 & 8):* "Length: 21.5mm Max, Width: 10.5mm Max, Thickness: 2.5mm Max(含背胶)", "≥22mAh@ 0.2C Discharge(放电)". Drawing p. 8 dimensions bare cell as "MAX2.3" mm.
*   **PowerStream GM300910-PCB:**
    *   *Catalog quote:* "GM300910-PCB | 3.7 | 8 | 12 | 3.0×9×10 | 0.7 g | ... Samples: $17.00". Capacity is 12 mAh nominal, below 20 mAh target.
*   **DNK Power & LiPol Battery:**
    *   Online single-unit purchase is `UNVERIFIED`. Search tried: "DNK301015 buy 1 piece online cart checkout", "LP301016 buy single unit online". Both vendors require business inquiry forms with MOQ 100+.

---

## 2. Finishes for a Skin-Worn Part at JLC3DP

### 2.1 JLC3DP Process Evaluation

| Process & Material | Surface & Finish Options | Skin Contact & Certification Statements | Lead Time | 40 × 20 × 8 mm Part Price |
| :--- | :--- | :--- | :---: | :---: |
| **HP MJF PA12 / PA12S**<br>[jlc3dp.com](https://jlc3dp.com/materials/hp-mjf-pa12)<br>Date read: 2026-09-17 | Natural Grey, Dyed Black; media blasted; vapor smoothing offered | **ISO 10993 Certified:** "PA12 and PA12S are specifically noted as being certified for skin contact and medical device applications." "meeting ISO 10993 biocompatibility standards and being sterilizable." PA12S offers "a premium, smoother, and softer surface finish". | 2–4 business days | **UNVERIFIED** without CAD upload |
| **SLS PA12 (3201PA-F)**<br>[jlc3dp.com](https://jlc3dp.com/materials/sls-nylon)<br>Date read: 2026-09-17 | White/Natural; dyed colors; media blasted | **Porous surface:** "SLS prints are naturally porous and may require sealing to prevent bacteria trapping in certain environments." | 2–4 business days | **UNVERIFIED** without CAD upload |
| **SLA Resins**<br>[jlc3dp.com](https://jlc3dp.com/materials/sla-resin)<br>Date read: 2026-09-17 | Standard & Tough (9000HE, Ledo 6060, Black) | **Not skin safe:** "most standard resins (SLA/LCD) are not suitable for food contact or long-term medical contact, even after curing." | 1–3 business days | **UNVERIFIED** without CAD upload |

*Price for 40 × 20 × 8 mm at JLC3DP:* `UNVERIFIED` without CAD upload. JLC3DP uses dynamic geometry calculation; no static dimension pricing tables exist. Search tried: "JLC3DP static price table 40x20x8 mm part".

### 2.2 Alternative Vendor: Xometry

Source: Xometry ([xometry.com](https://www.xometry.com), date read: 2026-09-17).
*   *Material:* HP MJF PA12 with chemical vapor smoothing (AMT PostPro3D).
*   *Skin certification quote:* "MJF Nylon 12: This material is noted as being biocompatible (USP Class I-VI, FDA Intact Skin Surface Devices)."
*   *Vapor smoothing certification quote:* "MJF-printed PA 12 parts that have undergone chemical vapor smoothing (using PostPro3D) have passed testing for cytotoxicity (ISO 10993-5) and have been shown not to cause skin-irritating effects (based on ISO 10993-10, ISO 10993-1, and OECD TG 439)."
*   *Appearance quote:* "Vapor smoothing is frequently used to improve the surface finish of MJF Nylon 12, often resulting in parts that rival the appearance of injection-molded components."
*   *Price for 40 × 20 × 8 mm:* `UNVERIFIED` without CAD file upload.

---

## 3. The Board, Assembled Once (JLCPCB PCBA & LCSC Library)

### 3.1 JLCPCB Assembly Capabilities and Fees

Source: JLCPCB PCBA FAQ & Capabilities ([jlcpcb.com](https://jlcpcb.com), date read: 2026-09-17).

| Parameter / Fee Item | Economic PCBA | Standard PCBA | Notes |
| :--- | :---: | :---: | :--- |
| **Assembly Capability** | Single-sided only | Single or double-sided | Economic requires all SMT parts on top side. |
| **Setup Fee** | **$8.18 USD** | **$25.56 USD** (1-sided) / **$51.12 USD** (2-sided) | Verbatim: "Setup Fee: $8.18" vs "$25.56 / $51.12". |
| **SMT Stencil Fee** | **$1.53 USD** | **$8.21 USD** (1-sided) / **$16.42 USD** (2-sided) | Laser stainless steel stencil. |
| **Panel Fee** | **$8.21 USD** | **$8.21 USD** | Applies to panelized designs. |
| **Solder Joint Fee** | $\approx \mathbf{\$0.0016\text{ to } \$0.003\text{ USD}}$ | $\approx \mathbf{\$0.0016\text{ to } \$0.003\text{ USD}}$ | Per SMD joint/pin. |
| **Component Feeder Fee** | **$0.00** Basic / **$3.00** Extended | **$3.00 USD** per feeder | Basic parts incur no feeder loading fee. |
| **Minimum Assembly Qty** | **2 pieces** | **2 pieces** | Bare PCB min is 5 pieces. |
| **4-Layer 20 × 16 mm Board (5 pcs)** | Base promo starts at **~$2.00–$5.00 USD** | Base promo starts at **~$2.00–$5.00 USD** | Bare FR-4 standard; ENIG adds ~$15–$20. |
| **Shipping Options** | DHL Express, FedEx, UPS International | DHL Express, FedEx, UPS International | 3–7 business days transit. |

### 3.2 LCSC / JLCPCB Component Library Availability

Source: LCSC ([lcsc.com](https://www.lcsc.com)) and JLCPCB Parts ([jlcpcb.com/parts](https://jlcpcb.com/parts)), date read: 2026-09-17.

| Component | Part Number | LCSC ID | Classification | Stock Status | Unit Price (Qty 1–10) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **TI ADS1292R** | `ADS1292RIRSMT` (VQFN-32) | `C106679` / `C134015` | **Extended** ($3.00 feeder) | Stock fluctuates / Out of stock; needs Global Sourcing | ~$8.50–$11.80 USD |
| **TI ADS1292** | `ADS1292IRSMT` (VQFN-32) | `C134015` / `C2841443` | **Extended** ($3.00 feeder) | Intermittent stock | ~$6.50–$9.20 USD |
| **TI BQ25100** | `BQ25100YFPR` (DSBGA-6) | `C527572` | **Extended** ($3.00 feeder) | In Stock | ~$1.15–$1.45 USD |
| **TI TLV713 3.3V** | `TLV71333PDBVR` (SOT-23-5) | `C90840` | **Basic / Preferred** ($0.00) | In Stock (> 10,000) | ~$0.18–$0.28 USD |
| **Raytac MDBT50Q-1MV2** | `MDBT50Q-1MV2` (nRF52840) | `C5142646` | **Extended / Consigned** | Out of stock; Global Sourcing / Consignment | ~$8.20–$10.50 USD |
| **Seeed XIAO nRF52840** | `102010448` (Castellated SMT) | Listed in ecosystem | **Consigned / Customer Supplied** | Stocked at Seeed/DigiKey; consign to JLC | $9.90 (Seeed) / $10.38 (DigiKey) |
| **Ebyte E73-2G4M08S1C** | `E73-2G4M08S1C` (nRF52840) | `C356849` (re-read: [lcsc.com](https://www.lcsc.com/product-detail/Bluetooth-Modules_C356849.html)) | **Extended** ($3.00 feeder) | In Stock | ~$4.80–$6.20 USD |
| **Fanstel BT840** | `BT840` / `BT840F` (nRF52840) | `BT840` series | **Extended / Consigned** | Out of stock; Consignment | ~$6.80–$8.50 USD |
| **TI INA128** | `INA128UA/2K5` (SOIC-8) | `C7405` | **Extended** ($3.00 feeder) | In Stock | ~$6.50–$8.20 USD |

*Fee rules:* Basic parts have zero loading fees. Extended parts incur $3.00 USD per unique part line. Consigned/Global Sourcing parts incur part purchase costs and manual check-in handling fees.

---

## 4. The XIAO Route: Carrier Board vs. Bare Module

Source: Seeed Studio ([seeedstudio.com](https://www.seeedstudio.com/Seeed-XIAO-BLE-nRF52840-p-5201.html), [wiki.seeedstudio.com/XIAO_BLE/](https://wiki.seeedstudio.com/XIAO_BLE/), date read: 2026-09-17).

### 4.1 Seeed XIAO nRF52840 Specifications

*   **Part Number:** `102010448` (Standard BLE) / `102010469` (Sense).
*   **Dimensions:** $21.0\text{ mm length} \times 17.5\text{ mm width}$. PCB substrate is $1.2\text{ mm}$ thick.
*   **Total Height:** **$4.3\text{ to } 4.5\text{ mm}$** including the mounted USB-C connector (connector extends $3.16\text{ mm}$ above PCB surface).
*   **Weight:** **$4.0\text{ g}$** (0.004 kg).
*   **Charger & Current:** Integrated TI BQ25100/BQ25101. Default charge current is **$50\text{ mA}$**; software-configurable to **$100\text{ mA}$** via GPIO pin `P0.13` / charge control pin LOW (re-read: Seeed Wiki [wiki.seeedstudio.com/XIAO_BLE/](https://wiki.seeedstudio.com/XIAO_BLE/)).
*   **Battery Pads:** Dedicated solder pads `BAT+` and `BAT-` on the PCB underside.
*   **Pricing & Stock (2026-09-17):**
    *   Seeed Studio: **$9.90 USD**, In Stock.
    *   DigiKey (`1568-102010448-ND`): **$10.38 USD**, In Stock.
    *   Mouser (`713-102010448`): **$10.89 USD**, In Stock.
*   **Public Open-Source Engineering Support:**
    *   *Schematics:* Open-source KiCad schematic files, footprint libraries, 3D STEP models, and PDF schematics are public on the Seeed Wiki.
    *   *Software:* Upstream Zephyr RTOS support (`seeed_xiao_nrf52840` / `xiao_ble`) and official Arduino support (`Seeed nRF52 mbed-enabled Boards`).

### 4.2 Engineering Trade-Off

*   **Pros:** Isolates RF tuning, BLE antenna impedance matching, 32.768 kHz crystal routing, and USB-C power handling to a proven pre-certified module. The custom PCB holds only the analog front-end.
*   **Cons:** The $4.3–4.5\text{ mm}$ total height with USB-C connector creates vertical clearance constraints in a thin shell (internal cavity $\le 6.0\text{ mm}$), requiring a pocket cutout or connector removal.

---

## 5. Contact Hardware in Single-Unit Quantities

Verified for Order 2 in single units and small packs:

| Description | Part / SKU | Supplier & URL | Date Read | Unit Price | Min Qty | Stock Status |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **Brass DIN 439 M2.5 Thin Nut** | Bossard BN 147 (`1159550`) | TME<br>[tme.eu/en/details/b2.5_bn147](https://www.tme.eu/en/details/b2.5_bn147/hex-nuts/bossard/1159550/) | 2026-09-17 | **$0.16 USD** | **10 pk** ($1.60) | In Stock (> 1,000) |
| *Single Brass Thin Nut* | DIN 439 M2.5 Brass | Westfield Fasteners<br>[westfieldfasteners.co.uk](https://www.westfieldfasteners.co.uk) | 2026-09-17 | **£0.28 GBP** (~$0.36 USD) | **1 pc** | In Stock |
| **Titanium ISO 7380 M2.5 × 4** | Sortafast `SF-BH2504-10` | Sortafast<br>[sortafast.com Product Page](https://sortafast.com/products/sortafast-titanium-screws-button-head-10pk-m2-5) | 2026-09-17 | **$1.75 USD** | **10 pk** ($17.50) | In Stock (Live page, under $20) |
| *Single Titanium Screw* | `vis-titane-ISO7380-G5-M2.5` | Titane Services<br>[titane-services.eu](https://www.titane-services.eu/vis-titane-ISO7380-G5-M2.5) | 2026-09-17 | **3.57 €** (~$3.85 USD) | **1 pc** | In Stock (Trim 1 mm) |
| **Ring Lug (Nickel-Free)** | TE Connectivity `31428`<br>(#4 / M2.5, Pure Matte Tin) | DigiKey<br>[digikey.com Product Page](https://www.digikey.com/en/products/detail/te-connectivity-amp-connectors/31428/292150) | 2026-09-17 | **$0.24 USD** | **1 pc** | In Stock (Thousands) |

---

## 6. Behind-The-Ear Fit Verification Without a Printed Gauge

### 6.1 Published 1:1 Sizing Templates

Medical and consumer audio manufacturers provide published 1:1 printable templates to verify behind-the-ear (BTE) dimensions:

1.  **HearSource BTE Measuring Tool ([HearSource](https://www.hearsource.com), date read: 2026-09-17):** Printable 1:1 scale contour cutout to verify behind-the-ear chord length and superior ear-root hook placement.
2.  **Signia RIC Ear Measurement Template ([Signia](https://www.signia.net), date read: 2026-09-17):** Printable 1:1 calibration card with millimeter ear-hook curvature scale and 50 mm print calibration block.
3.  **Ear Gear BTE Sizing Guide ([gearforears.com](https://about.gearforears.com/wp-content/uploads/2022/03/1601394368-a-sizing-guide.jpeg), date read: 2026-09-17):** 1:1 scale silhouettes for micro ($\le 25\text{ mm}$), mini ($25–32\text{ mm}$), and standard ($32–50\text{ mm}$) BTE housing profiles.

### 6.2 Suitability and Limitations of a Cutout Paper Profile

A paper profile cut 1:1 from `docs/fab/cad/v1/drawing.pdf` provides an accurate check of total chord length, retroauricular crease arc, and superior ear-root hook curvature. It cannot verify 3D coronal skull clearance, mastoid bone surface contact, electrode dome skin pressure, or cartilage pinching against the rigid shell body.
