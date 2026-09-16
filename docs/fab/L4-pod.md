# L4 — Stage B Pod Electronics, Envelope, and One-Off PCB Fabrication

This report evaluates electronic components, enclosure envelope, PCB manufacturing, safety architecture, and streaming firmware for the Elicio Stage B behind-the-ear (BTE) pod.

---

## 1. Smallest Sensible Stage B Electronics

Stage B migrates the single-channel breadboard amplifier into a self-contained, battery-powered wearable pod placed in the retroauricular sulcus. The electronics support 1–2 biopotential channels (auricular flex and jaw clench confirmation), BLE streaming, power management, and input protection in an unobtrusive shell.

### 1.1 BLE Microcontroller Modules

The MCU must provide a 2.4 GHz BLE radio, hardware SPI for biopotential ADC acquisition, DMA for jitter-free sampling, and sub-10 µA sleep modes.

| Module | Core & Radio | Footprint (mm) | Active / Sleep Current | Unit Price (Qty 1) | 2026 Stock & Source | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Seeed XIAO nRF52840** | nRF52840, Cortex-M4F @ 64 MHz, BLE 5.0 | 21.0 × 17.5 × 1.5 | TX: 4.8 mA (0 dBm, DC/DC); Sleep: <5 µA | $9.90 (Base) / $15.40 (Sense) | In stock (>1,000 units), [DigiKey 102010469](https://www.digikey.com/en/products/detail/seeed-technology-co-ltd/102010469/16652880) | **Best for prototype bring-up**: Integrated BQ25100 charger, USB-C, battery pads, and antenna. |
| **Raytac MDBT50Q-1MV2** | nRF52840, Cortex-M4F @ 64 MHz, BLE 5.2 | 15.5 × 10.5 × 2.05 | TX: 4.8 mA (0 dBm, DC/DC); Sleep: <2 µA | ~$8.50 - $11.20 | In stock, [DigiKey MDBT50Q-1MV2](https://www.digikey.com/en/products/detail/raytac-corporation/MDBT50Q-1MV2/10492121) | **Best for custom PCB**: Ultra-compact footprint, pre-certified chip antenna, castellated pads. |
| **u-blox NINA-B302** | nRF52840, Cortex-M4F @ 64 MHz, BLE 5.0 | 14.0 × 10.0 × 3.8 | TX: 4.8 mA; Sleep: <3 µA | ~$12.50 | In stock, [DigiKey NINA-B302](https://www.digikey.com/en/products/detail/u-blox/NINA-B302-00B/9659345) | Viable alternative; slightly taller package. |
| **Seeed XIAO ESP32-C3** | ESP32-C3, RISC-V @ 160 MHz, BLE 5.0 | 21.0 × 17.5 × 1.5 | BLE TX: 25–30 mA; Deep Sleep: 44 µA | $5.40 | In stock, [DigiKey 102010388](https://www.digikey.com/en/products/detail/seeed-technology-co-ltd/102010388/16652878) | **Reject**: Active RF current (25–30 mA) drains 50 mAh battery in <2 hours. |
| **Seeed XIAO ESP32-C6** | ESP32-C6, RISC-V @ 160 MHz, BLE 5.3 | 21.0 × 17.5 × 1.5 | BLE TX: ~30 mA; Deep Sleep: 15 µA | $7.20 | In stock, [DigiKey 102010620](https://www.digikey.com/en/products/detail/seeed-technology-co-ltd/102010620/22119934) | **Reject**: Excessive active modem power consumption. |

**Selection Verdict:** The **Nordic nRF52840** is the definitive choice. Its DC/DC buck converter maintains active radio current under 5 mA at 0 dBm. The **Seeed XIAO nRF52840** accelerates breadboard bring-up; the **Raytac MDBT50Q** reduces board area by 42% for the final custom wearable PCB.

---

### 1.2 Biopotential Front Ends (AFE)

The front end must provide CMRR > 100 dB, input impedance > 100 MΩ, and input noise < 10 µV RMS across 20–500 Hz.

| Front End IC | Ch | ADC & Sample Rate | Power Consumption | Package (mm) | Price (Qty 1) | 2026 Stock Status | Evaluation |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TI ADS1292 / ADS1292R** | 2 | 24-bit Delta-Sigma; 125 SPS–8 kSPS | 335 µW / ch (740 µW @ 3 V) | 32-TQFP (5.0 × 5.0 × 1.0) | $13.51 | In stock (54 at [DigiKey 296-30137-5-ND](https://www.digikey.com/en/products/detail/texas-instruments/ADS1292IPBS/3089408); active on LCSC) | **Strongly Recommended**: 2 channels (auricular flex + jaw clench). 24-bit ADC eliminates gain trimmers. Integrated RLD suppresses common-mode noise. |
| **TI ADS1291** | 1 | 24-bit Delta-Sigma; 125 SPS–8 kSPS | 335 µW total | 32-TQFP (5.0 × 5.0 × 1.0) | $11.54 | In stock (>3,100 at [DigiKey 296-30136-5-ND](https://www.digikey.com/en/products/detail/texas-instruments/ADS1291IPBS/3089407)) | Identical package to ADS1292; saves $1.97 but prevents a second confirmation channel. |
| **TI ADS1299-4** | 4 | 24-bit Delta-Sigma; 250 SPS–16 kSPS | 5 mW / ch (24 mW total) | 64-TQFP (10.0 × 10.0 × 1.2) | $44.99 | In stock (>2,600 at [DigiKey 296-45228-1-ND](https://www.digikey.com/en/products/detail/texas-instruments/ADS1299-4PAGR/6231267)) | **Reject for Stage B**: Excessive power (32× higher than ADS1292), 4× larger area (100 mm²), and high cost ($44.99). Suitable for Stage D+ lab EEG. |
| **ADI AD8232** | 1 | Analog out; 0.5–40 Hz ECG bandpass | 360 µA (1.2 mW @ 3.3 V) | 20-LFCSP (4.0 × 4.0 × 0.85) | $5.49 | In stock (>3,000 at [DigiKey AD8232ACPZ-R7](https://www.digikey.com/en/products/detail/analog-devices-inc/AD8232ACPZ-R7/3770451)) | Requires modifying external RC network for 20–500 Hz EMG. Outputs analog voltage only; requires external ADC. |
| **Maxim MAX30003** | 1 | Internal ADC; max 512 SPS | 85 µW | 28-TQFN (5.0 × 5.0) | $16.63 | In stock at [DigiKey MAX30003CTI+T](https://www.digikey.com/en/products/detail/analog-devices-inc-maxim-integrated/MAX30003CTI-T/6211417) | **Reject**: Maximum 512 SPS violates the 1000 SPS Nyquist requirement for raw sEMG signals. |
| **Discrete (INA333 + TLV9002)** | 1 | Analog out to ADS1115 or MCU | ~120 µA (400 µW @ 3.3 V) | INA333: 8-VSSOP (3.0 × 3.0); Op-Amp: SOT-23-8 | INA333: $6.74 ([DigiKey INA333AIDGKT](https://www.digikey.com/en/products/detail/texas-instruments/INA333AIDGKT/1884488)); Op-Amp: $0.60 | In stock (>2,500 units) | Micro-miniaturization of Stage A. Requires 12+ external passives, consuming more PCB area than the ADS1292. |

**Selection Verdict:** The **TI ADS1292** replaces the instrumentation amplifier, gain stages, active filter op-amps, and external ADC. Its 24-bit delta-sigma ADC with internal reference provides sub-0.1 µV resolution, eliminating hardware gain trimmers. Channel 1 captures auricular flex; Channel 2 captures masseter clench confirmation on a single 5 × 5 mm IC.

---

### 1.3 Sample Rate and Resolution Requirements

Surface EMG frequency content spans **20 Hz to 500 Hz**, with peak power between **50 Hz and 150 Hz** ([De Luca et al., 2010](https://doi.org/10.1016/j.jelekin.2010.03.008)).

* **Raw Waveform Nyquist Limit:** Capturing raw sEMG without aliasing requires at least $2 \times 500\text{ Hz} = 1000\text{ SPS}$.
* **Stage A Baseline:** ADS1115 runs at **860 SPS** with 16-bit resolution. With a Sallen-Key low-pass filter ($f_c \approx 490\text{ Hz}$), it provides clean envelope tracking.
* **Stage B Target:** The ADS1292 provides programmable output rates of **500, 1000, and 2000 SPS**. Operating at **1000 SPS** satisfies raw sEMG Nyquist fidelity. The 24-bit dynamic range (~144 dB) accommodates microvolt-level twitches up to millivolt-level clenches without clipping or gain adjustments.

---

### 1.4 Power Architecture, Battery Chemistry, and Charging

The pod runs entirely on an internal battery, completely isolated from AC mains power.

#### Battery Chemistry Comparison

| Battery Model | Dimensions (mm) | Voltage | Capacity | Max Discharge | $R_{int}$ | Evaluation |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **LiPo 501015** | 5.0 × 10.0 × 15.0 | 3.7 V (4.2 V max) | 50 mAh | 1C–2C (50–100 mA) | <150 mΩ | **Optimal**: Narrow rectangular bar fits retroauricular sulcus; low $R_{int}$; weighs 1.2 g. |
| **LiPo 401030** | 4.0 × 10.0 × 30.0 | 3.7 V (4.2 V max) | 100 mAh | 1C (100 mA) | <120 mΩ | Long run time (~15 hours); length (30 mm) occupies the full vertical ear height. |
| **LIR2032** | 20.0 dia × 3.2 ht | 3.6 V / 3.7 V | 40–45 mAh | 1C (40 mA) | 300–500 mΩ | Circular 20 mm disk is too wide to conceal flush behind the ear pinna. |
| **CR2032** | 20.0 dia × 3.2 ht | 3.0 V nominal | 220–240 mAh | 3–5 mA continuous | 10–30 Ω | Non-rechargeable. High $R_{int}$ causes voltage brownout during BLE TX pulses without large buffer capacitors. |

#### Power Management ICs

1. **Charger IC:**
   - **TI BQ25100:** 6-DSBGA package (**1.60 × 0.90 × 0.5 mm**, [DigiKey BQ25100YFPR](https://www.digikey.com/en/products/detail/texas-instruments/BQ25100YFPR/4934524), $2.08). Programmable charge current 10–250 mA (set to 25–50 mA for 50 mAh cell). Reverse leakage <75 nA. Integrated on the Seeed XIAO nRF52840.
   - **Microchip MCP73831T-2ACI/OT:** SOT-23-5 (**2.9 × 1.6 × 1.1 mm**, [DigiKey MCP73831T-2ACI/OTCT-ND](https://www.digikey.com/en/products/detail/microchip-technology/MCP73831T-2ACI-OT/1979802), $0.76). Industry standard; larger footprint.
2. **Protection IC (PCM):**
   - 501015 pouch cells typically include an integrated **DW01A** micro-PCM strip with dual MOSFET for over-charge (4.28 V), over-discharge (2.40 V), and short-circuit protection.
   - For board-level protection on a custom PCB, the **TI BQ2970** in 6-WSON (**1.50 × 1.50 × 0.75 mm**, [DigiKey BQ29700DSET](https://www.digikey.com/en/products/detail/texas-instruments/BQ29700DSET/4934538), $1.19) provides precision cell protection.

#### Run Time per Charge

Power budget during continuous biopotential acquisition and BLE streaming:
* **TI ADS1292 (2 ch @ 1000 SPS):** $0.67\,\text{mW}$ ($\approx 0.20\,\text{mA}$ at 3.3 V).
* **Nordic nRF52840 (CPU @ 64 MHz + internal DC/DC):** $\approx 3.3\,\text{mA}$.
* **BLE 5.0 Radio (TX @ 0 dBm, 29 pkts/sec, 15 ms interval):** $\approx 2.2\,\text{mA}$.
* **Passives and regulator quiescent current:** $\approx 0.1\,\text{mA}$.
* **Total Operating Current:** $I_{avg} \approx \mathbf{5.8\,\text{mA}}$.

$$\text{Run Time (50 mAh LiPo)} = \frac{50\text{ mAh} \times 0.85}{5.8\text{ mA}} \approx \mathbf{7.3\text{ hours continuous streaming}}$$

$$\text{Run Time (100 mAh LiPo)} = \frac{100\text{ mAh} \times 0.85}{5.8\text{ mA}} \approx \mathbf{14.6\text{ hours continuous streaming}}$$

In System ON IDLE sleep mode, average current drops to **<15 µA**, providing over 120 days of standby shelf life.

---

## 2. Reference Designs and Open-Source Precedents

Several open-source platforms provide hardware references for ear-level biopotentials.

### 2.1 OpenEarable 2.0
* **Developers:** TU Darmstadt, University of Bath, and KIT ([GitHub OpenEarable](https://github.com/OpenEarable/open-earable-2), MIT License).
* **Architecture:** Form factor modeled on Apple AirPods Pro, seated in the concha. Integrates dual-core ARM Cortex-M33, ADI ADAU1860 DSP, 9-axis IMU, ear-canal pressure sensor, inward/outward microphones, and BLE 5.2 ([KIT Research Record](https://teco.edu)).
* **Relevance:** Demonstrates high-density sensing and BLE in an earable. However, OpenEarable sits *inside the concha*, which is externally visible and occludes the canal. Elicio places the pod *behind the ear* to preserve covertness and unblocked hearing.

### 2.2 OpenBCI Ganglion and Cyton (Why They Are Too Large)
* **Ganglion:** 4-channel AFE (MCP3912 + Simblee/nRF51 BLE). Dimensions: **61.2 × 61.2 mm** (2.41 × 2.41 in) octagonal board ([OpenBCI Ganglion Docs](https://docs.openbci.com/Ganglion/GanglionDataFormat/)).
* **Cyton:** 8-channel AFE (ADS1299 + PIC32MX). Dimensions: **61.2 × 61.2 mm** ([OpenBCI Cyton Docs](https://docs.openbci.com/Cyton/CytonDataFormat/)).
* **Why Unsuitable:** The retroauricular sulcus provides 35–45 mm vertical height and only 8–12 mm width. At 61 × 61 mm, Ganglion and Cyton are 5× wider than the space behind the ear. They are benchtop or headband tools, not ear-level wearables.

### 2.3 cEEGrid Ear-EEG Arrays and Adapters
* **Design:** Developed by Bleichner & Debener (Oldenburg), the cEEGrid is a flexible printed Ag/AgCl array adhering around the ear for EEG/EMG recording ([Bleichner & Debener, 2017](https://doi.org/10.3389/fnins.2017.00212)).
* **Interface Hardware:** The open-source **nEEGlace** ([GitHub T-PsyOl/nEEGlace](https://github.com/T-PsyOl/nEEGlace)) houses the amplifier in a neck-worn collar.
* **Takeaway:** Confirms that the retroauricular space provides high signal quality. Elicio replaces cEEGrid's gelled contacts and external collar by integrating dry contacts, amplifier, battery, and BLE radio into a single behind-ear pod.

### 2.4 EarSwitch and EarRumble Hardware
* **EarRumble (CHI 2021):** Tobias Röddiger et al. (KIT) demonstrated voluntary tensor tympani contraction detection using a **Bosch BME280 pressure sensor** at 32 Hz in a custom earbud ([ACM CHI 2021](https://doi.org/10.1145/3411764.3445543)), achieving 95% accuracy.
* **EarSwitch (JNER 2024):** Nick Gompertz et al. validated in-ear barometry and PPG for assistive motor neurone disease switches ([JNER 2024](https://doi.org/10.1186/s12984-024-01490-8)).
* **Takeaway:** Provides the engineering basis for Elicio's **Stage C** canal tip. Stage B focuses on auricular and masseter EMG.

### 2.5 Open-Source EMG Hardware
* **Upside Down Labs BioAmp EXG Pill:** Biopotential front end measuring **25.4 × 10.0 mm** ([GitHub upsidedownlabs/BioAmp-EXG-Pill](https://github.com/upsidedownlabs/BioAmp-EXG-Pill), CERN-OHL-S-2.0). Uses a TI TL074 quad op-amp in an analog instrumentation topology; outputs analog signal only.
* **Upside Down Labs ADS1292R Breakout:** Open-source KiCad design for the ADS1292R with standard passives ([GitHub upsidedownlabs/ADS1292R-Breakout](https://github.com/upsidedownlabs/ADS1292R-Breakout), CERN-OHL-S-2.0), providing layout reference for analog/digital plane isolation.
* **ProtoCentral ADS1292R Breakout:** Proven Arduino/C++ drivers for configuring the ADS1292 registers via SPI ([GitHub Protocentral/ADS1292rShield_Breakout](https://github.com/Protocentral/ADS1292rShield_Breakout), CERN-OHL-P v2).

---

## 3. Physical Envelope and Mechanical Integration

The retroauricular sulcus forms an anatomical crescent between the ear cartilage and cranium.

### 3.1 Dimensions: Rigid Board vs Rigid-Flex

#### Option A: Single Rigid PCB
* **Layout:** Components populated on a single 4-layer FR4 board (30.0 × 11.5 × 1.0 mm).
* **Stacked Arrangement:** Stacking the 501015 LiPo battery (5.0 mm thick) produces:
  - PCB + components: ~2.5 mm
  - Battery: 5.0 mm
  - Shell walls (0.8 mm × 2): 1.6 mm
  - **Total Pod Envelope:** **34.0 mm (L) × 13.0 mm (W) × 9.1 mm (H)**.
* **Evaluation:** At 9.1 mm thick, the pod pushes the auricle slightly outward, reducing visual covertness.

#### Option B: Two-Board Rigid-Flex PCB (Recommended)
* **Layout:** Two rigid islands connected by a 0.1 mm polyimide flex bridge:
  - **Top Board (16.0 × 9.5 mm):** Raytac MDBT50Q BLE module, 32.768 kHz crystal, and outward-facing chip antenna.
  - **Flex Bridge (6.0 × 6.0 mm):** Carries SPI and power buses.
  - **Bottom Board (16.0 × 9.5 mm):** TI ADS1292 AFE, 220 kΩ protection network, and BQ25100 charger.
  - **Battery Placement:** 501015 cell positioned in tandem or nested between sections.
* **Total Pod Envelope:** **Curved crescent profile, 33.0 mm chord length × 10.5 mm width × 6.8 mm thickness**.
* **Evaluation:** At 6.8 mm thick, the pod sits flush within the retroauricular crease, matching commercial hearing aids.

### 3.2 Benchmark Comparisons

| Category | Benchmark Product | Envelope (L × W × H mm) | Weight | Visual Subtlety |
| :--- | :--- | :--- | :--- | :--- |
| **BTE / RIC Hearing Aid** | Phonak Audéo Lumity / Oticon Real | 29.5 × 8.2 × 6.6 | 2.4 g | **High**: Concealed behind ear pinna. |
| **Bone-Conduction Pod** | Shokz OpenRun Pro | 36.0 × 11.0 × 8.5 | ~6.5 g (pod) | **Moderate**: Visible hook and higher profile. |
| **TWS Ear Hook** | FiiO UTWS5 / Shure RMCE-TW2 | 54.0 × 20.2 × 10.4 | 8.5 g | **Low**: Bulky consumer battery pod. |
| **Elicio Stage B Pod** | Custom 3D Shell + Rigid-Flex | **33.0 × 10.5 × 6.8** | **~6.4 g** | **High**: Replicates BTE hearing aid footprint. |

### 3.3 Attachment and Weight Distribution

1. **Anatomical Ear Hook:** A 1.2 mm flexible silicone or TPU hook loops over the superior auricular sulcus, carrying **80% of the device weight**.
2. **Contact Preload:** The curved shell exerts a mild inward spring force (~0.5 N) across the sulcus to maintain dry electrode skin contact.
3. **Adhesive Assist:** For vigorous movement, medical double-sided tape ([3M 1522](https://www.3m.com)) secures the inner face to mastoid skin.
4. **Weight Breakdown:** Shell (~2.4 g) + PCB (~1.8 g) + 50 mAh battery (~1.4 g) + contacts (~0.8 g) = **~6.4 grams total**. Weight sits directly over the cranial root of the helix, avoiding downward drag on the pinna.

---

## 4. One-Off PCB Fabrication and Assembly in China

Fabricating a prototype batch (2 to 5 boards) requires surface-mount assembly, fine trace pitch, and specific parts library support.

### 4.1 JLCPCB PCBA Capabilities

JLCPCB provides automated SMT assembly in Shenzhen, linked to the [LCSC Catalog](https://www.lcsc.com).

* **Parts Library Status (2026):**
  - **Passives:** 0402 and 0603 1% resistors and C0G/X7R capacitors are Basic Parts ($0 loading fee).
  - **TI ADS1292 / ADS1292R:** Listed in LCSC/JLCPCB library (LCSC Part # `C126131` for ADS1292RIPBS, TQFP-32) as an Extended Part ($3.00 setup fee).
  - **Microcontroller:** Bare Nordic `nRF52840-QIAA` (`C155523`) is stocked. Pre-certified modules like the Raytac MDBT50Q are **not in the standard assembly feeder library**; they require JLCPCB Global Sourcing or user consignment.
  - **Charger & Diodes:** Microchip MCP73831 (`C14663`) and low-leakage diode array **BAV199** (`C2561`, SOT-23) are actively stocked.
* **Order Parameters:** Minimum 5 PCBs fabricated; minimum 2 boards assembled.
* **Cost Estimate (5 PCBs Fabricated, 2 Assembled with ADS1292 + Passives):**
  - 4-layer FR4 fabrication (≤50 × 50 mm): $2.00
  - SMT Setup Base Fee: $8.00; Stencil: $1.50; Placement Fee: ~$4.00
  - Extended Part Setup Fees (~4 parts @ $3.00): $12.00
  - Component Costs (ADS1292, charger, LDO, passives): ~$32.00
  - **PCBA Subtotal:** **~$59.50 USD**.
  - Express Shipping to Massachusetts (DHL/FedEx): ~$22.00.
  - **Total Delivered Cost:** **~$81.50 USD**.
* **Lead Time:** 4–6 business days for assembly + 3–5 business days transit to Massachusetts (**8–11 calendar days total**).

### 4.2 PCBWay Turnkey Assembly

* **Capabilities:** [PCBWay Turnkey](https://www.pcbway.com) sources directly from DigiKey, Mouser, and Arrow.
* **Component Sourcing:** PCBWay can order the Raytac MDBT50Q-1MV2 directly from DigiKey and mount it with the ADS1292.
* **Cost (5 Fabricated, 2 Assembled Turnkey):** Fabrication ($5.00) + Setup & Tooling (~$50.00) + Components (~$65.00) = **~$135.00–$160.00 USD** (excluding shipping).
* **Evaluation:** PCBWay costs more than JLCPCB (~$150 vs ~$82), but eliminates consignment shipping for the Raytac BLE module.

### 4.3 Flex PCB (FPC) Options for Electrode Carriers

Both vendors fabricate 1-layer and 2-layer FPCs on polyimide (PI) down to **0.07–0.11 mm thickness** (5 prototypes: **$15.00–$25.00** at JLCPCB).

* **Critical Requirement 5 Compliance (Nickel-Free):**
  - Standard flex PCB surface finish is **ENIG** (Electroless Nickel Immersion Gold), containing a 3–5 µm electroless nickel underlayer.
  - *Warning:* Bare ENIG pads worn against skin can expose nickel through microscopic pores or abrasion, causing contact dermatitis.
  - *Mitigation:* The flex PCB must **not** expose bare ENIG to the skin. Instead, medical-grade **316L stainless steel discs** (or 3D-printed Palmiga conductive carbon-TPU pads) are bonded over the flex pads using anisotropic conductive tape ([3M 9703](https://www.3m.com/3M/en_US/p/d/b00016623/)). This ensures **zero nickel touches the skin**.

### 4.4 Required Manufacturing Files and KiCad 9 Scripting

Fabrication requires four file sets exported from EDA software:
1. **Gerbers (RS-274X):** Copper, Mask, Silk, Paste, and Edge Cuts layers.
2. **Drill Files (Excellon):** `.drl` plated and non-plated drill files.
3. **BOM:** CSV with `Designator`, `Value`, `Package`, `LCSC Part #`.
4. **CPL:** CSV with `Designator`, `Mid X`, `Mid Y`, `Layer`, `Rotation`.

KiCad 9 automates these exports via Python `pcbnew`:

```python
import pcbnew

board = pcbnew.LoadBoard("elicio_stage_b.kicad_pcb")
pctl = pcbnew.PLOT_CONTROLLER(board)
popt = pctl.GetPlotOptions()
popt.SetOutputDirectory("fabrication_output/")
popt.SetPlotFrameRef(False)

for layer in [pcbnew.F_Cu, pcbnew.B_Cu, pcbnew.F_Mask, pcbnew.Edge_Cuts]:
    pctl.SetLayer(layer)
    pctl.OpenPlotfile(board.GetLayerName(layer), pcbnew.PLOT_FORMAT_GERBER)
    pctl.PlotLayer()
pctl.ClosePlot()
```

---

## 5. Safety Architecture in a Wireless Wearable Pod

Because electrodes make direct skin contact, failure modes are evaluated under **IEC 60601-1** principles as an engineering design guideline (not a formal regulatory compliance claim).

### 5.1 Single-Fault Current Limits and Protection Network

1. **Current-Limiting Resistors:**
   - Every electrode trace incorporates a permanent **220 kΩ, 1%, 0402 resistor** placed adjacent to the skin contact pad.
   - Under a worst-case single fault where the 4.2 V battery rail shorts directly to the input:

$$I_{fault,max} = \frac{4.2\text{ V}}{220\text{ k}\Omega} = \mathbf{19.09\,\mu\text{A}}$$

2. **Transient and ESD Clamping:**
   - Following the 220 kΩ resistor, each lead connects to a **BAV199** ultra-low-leakage diode pair ([Nexperia BAV199](https://www.nexperia.com/products/diodes/general-purpose-diodes/BAV199.html)) clamping to 3.3 V and GND.
   - Typical leakage is **<5 pA**, avoiding signal attenuation while shunting ESD events up to ±8 kV.

### 5.2 IEC 60601-1 Patient Leakage Benchmarks

| Condition | Type BF Limit (DC) | Type CF Limit (DC) | Elicio Stage B Circuit | Margin |
| :--- | :--- | :--- | :--- | :--- |
| **Normal Condition (NC)** | 10 µA | 10 µA | **<0.001 µA** (ADS1292 bias current is ~200 pA) | >10,000× below limit |
| **Single Fault Condition (SFC)** | 500 µA | 50 µA | **19.09 µA** (Limited by 220 kΩ @ 4.2 V) | **2.6× below Type CF limit**; 26× below Type BF limit |

The 19.1 µA hardware fault ceiling is below human perception (~1 mA) and strictly within medical-grade single-fault limits.

### 5.3 Physical Isolation and the "Never Charge While Worn" Rule

1. **Galvanic Isolation:** The worn pod runs exclusively on its internal 3.7 V LiPo cell with zero connection to AC mains or earth ground.
2. **Physical Interlock:**
   - Charging pads (magnetic pogo pins) are located on the **inner, skin-facing surface of the pod**.
   - When worn, the charging pads are pressed against the mastoid skin, making it **physically impossible to connect a charging cable while worn**. The user must remove the pod to dock it.

---

## 6. Firmware Architecture and Wireless Streaming

The pod streams biopotential data conforming to the protocol in `docs/EARPIECE_DESIGN.md`: one ASCII sample value per line.

### 6.1 Nordic UART Service (NUS) Profile

* **Service UUID:** `6E400001-B5A3-F393-E0A9-E50E24DCCA9E`
* **RX Characteristic (Write):** `6E400002-B5A3-F393-E0A9-E50E24DCCA9E`
* **TX Characteristic (Notify):** `6E400003-B5A3-F393-E0A9-E50E24DCCA9E`

The pod advertises as `Elicio-Pod-B` and streams sample notifications to the host.

### 6.2 Throughput, MTU, and Packetization

* **ASCII Data Rate:** At 1000 SPS, an ASCII line (e.g., `"-1842\n"`) averages ~7 bytes, requiring $1000 \times 7 = \mathbf{7,000\text{ bytes/sec}\;(56.0\text{ kbps})}$.
* **BLE MTU:** Under BLE 5.0 Data Length Extension (DLE), negotiated ATT MTU is **247 bytes** (payload **244 bytes**).
* **Batching:** Each 244-byte notification holds $\lfloor 244 / 7 \rfloor = \mathbf{34\text{ ASCII samples}}$.
* **Packet Rate:** $1000 / 34 \approx \mathbf{29.4\text{ packets/second}}$. At a 15–20 ms connection interval (50–66 events/sec), transmitting ~30 pkts/sec consumes **~7% of BLE 1M PHY capacity**, ensuring zero packet loss.
* **Binary Alternative:** Transmitting 16-bit binary integers (2 bytes/sample) requires only $2,000\text{ bytes/sec}$ (**71% reduction in RF airtime**). The host Python bridge unpacks binary data and emits ASCII to stdout, preserving the pod's battery while keeping `elicio scope` standard-library-only.

### 6.3 Latency Analysis

* **Packetization Delay (34 samples @ 1000 SPS):** 34.0 ms (or 17.0 ms with 17 samples/packet).
* **BLE Airtime & OS Stack Delay:** ~5–8 ms.
* **Detector Processing in `elicio scope`:** <2 ms.
* **Total Latency:** **~24 to 42 ms**, well below the 50–70 ms threshold for interactive biofeedback.

### 6.4 Host Bridge Script

```python
#!/usr/bin/env python3
"""scripts/ble_bridge.py - Bridges Elicio BLE NUS stream to stdout."""
import asyncio, sys
from bleak import BleakClient

NUS_TX_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

def notification_handler(sender, data: bytearray):
    sys.stdout.write(data.decode("utf-8", errors="ignore"))
    sys.stdout.flush()

async def main(address: str):
    async with BleakClient(address) as client:
        await client.start_notify(NUS_TX_UUID, notification_handler)
        while client.is_connected:
            await asyncio.sleep(1.0)

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1]))
```

Piping into the existing harness:
```bash
python scripts/ble_bridge.py "XX:XX:XX:XX:XX:XX" | \
    .venv/bin/elicio scope --input - --sample-rate 1000 --offset 2048 --gain 0.001
```

### 6.5 Firmware Frameworks

| Framework | Toolchain | Driver Ecosystem | Power Optimization | Recommendation |
| :--- | :--- | :--- | :--- | :--- |
| **Adafruit nRF52 Arduino Core** | PlatformIO | Excellent (`Adafruit_BluefruitLE`, SPI, ADS1292 libraries) | Moderate (FreeRTOS tickless idle) | **Recommended for Phase 1 bring-up**: Rapid bring-up in 1–2 days. |
| **Zephyr RTOS (nRF Connect SDK)** | Nordic / CMake | Native Nordic HAL, DMA buffers | Superior (System ON idle <2 µA) | **Recommended for Production Stage B**: Best battery endurance. |
| **CircuitPython** | Interpreted | Python | Poor (GC pauses cause FIFO dropouts at 1000 SPS) | **Reject**: High sampling jitter. |
| **Nordic nRF5 SDK (v17)** | Makefile | Legacy | Good | **Reject**: Deprecated since 2021. |

---

## 7. Open Questions for the Synthesis

1. **Module vs Discrete MCU on First PCB:**
   Should the first custom PCB mount a pre-certified **Raytac MDBT50Q** module ($10.50, integrated antenna/crystal) or attempt a discrete **nRF52840-QIAA** layout? *(Recommendation: Raytac module to avoid RF tuning and impedance matching risks).*
2. **Contact Count on First Shell:**
   The ADS1292 provides 2 differential channels (5 contact sites total). Should Stage B fabricate all 5 contacts on the shell immediately for simultaneous auricular flex and masseter confirmation, or start with 3 contacts (1 channel + reference) to simplify initial CAD modeling?
3. **Rigid Board with Wire Leads vs Rigid-Flex FPC:**
   Rigid-flex PCB tooling costs ~$40–$60 more than rigid FR4. Should the first prototype shell use a small rigid board with wired external contact discs, or proceed directly to an integrated polyimide flex carrier?
4. **Binary Protocol Support:**
   Should the Elicio protocol formally permit 16-bit binary integer streams over BLE/serial pipes to save 71% radio power, with host-side translation to ASCII?
5. **Electrode Material Sourcing:**
   Will the nickel-free contacts use CNC-turned 316L medical stainless steel discs or outsourced 3D-printed conductive carbon-TPU (Palmiga PI-ETPU)?

---

## 8. Top 10 Sources

1. **Texas Instruments — ADS1292 Low-Power 2-Channel 24-Bit Biopotential AFE Datasheet**  
   *URL:* [https://www.ti.com/product/ADS1292](https://www.ti.com/product/ADS1292)  
   *Description:* Primary specification for front-end IC: 335 µW/channel power, integrated PGA, RLD, and SPI registers.
2. **Nordic Semiconductor — nRF52840 Product Specification**  
   *URL:* [https://www.nordicsemi.com/Products/nRF52840](https://www.nordicsemi.com/Products/nRF52840)  
   *Description:* Authoritative hardware documentation for Cortex-M4F SoC: DC/DC efficiency, BLE 5.0 TX profile (4.8 mA @ 0 dBm), and sleep modes.
3. **OpenEarable 2.0 Research Platform**  
   *URL:* [https://github.com/OpenEarable/open-earable-2](https://github.com/OpenEarable/open-earable-2)  
   *Description:* Open-source multi-sensor earable platform by TU Darmstadt, University of Bath, and KIT (MIT License).
4. **Bleichner, M. G., & Debener, S. (2017) — Concealed, Unobtrusive Ear-Centered EEG Acquisition: cEEGrids**  
   *URL:* [https://doi.org/10.3389/fnins.2017.00212](https://doi.org/10.3389/fnins.2017.00212)  
   *Description:* Peer-reviewed study demonstrating biopotential acquisition from the retroauricular space using flexible printed arrays.
5. **Röddiger, T. et al. (CHI 2021) — EarRumble: Discreet Input by Voluntary Tensor Tympani Contraction**  
   *URL:* [https://doi.org/10.1145/3411764.3445543](https://doi.org/10.1145/3411764.3445543)  
   *Description:* In-ear barometric sensing of middle-ear muscle contraction using a Bosch BME280 sensor (95% accuracy).
6. **Gompertz, N. et al. (JNER 2024) — Exploring the 'EarSwitch' Concept**  
   *URL:* [https://doi.org/10.1186/s12984-024-01490-8](https://doi.org/10.1186/s12984-024-01490-8)  
   *Description:* Clinical study on ear-canal barometric deflection and optical sensing for voluntary assistive HCI.
7. **Upside Down Labs — BioAmp EXG Pill Repository**  
   *URL:* [https://github.com/upsidedownlabs/BioAmp-EXG-Pill](https://github.com/upsidedownlabs/BioAmp-EXG-Pill)  
   *Description:* CERN-OHL-S-2.0 open hardware design for a 25.4 × 10 mm analog biopotential front end.
8. **Raytac Corporation — MDBT50Q-1MV2 nRF52840 Module Specification**  
   *URL:* [https://www.raytac.com/product/ins.php?index_id=89](https://www.raytac.com/product/ins.php?index_id=89)  
   *Description:* Mechanical dimensions (15.5 × 10.5 mm), antenna layout guidelines, and pinout definitions.
9. **JLCPCB — SMT Assembly Capabilities & Parts Library**  
   *URL:* [https://jlcpcb.com/parts](https://jlcpcb.com/parts)  
   *Description:* Catalog verifying stock and component categories for the TI ADS1292, MCP73831, BAV199, and SMT passives.
10. **DigiKey Electronics — Parametric Inventory & Pricing (September 2026)**  
    *URL:* [https://www.digikey.com](https://www.digikey.com)  
    *Description:* Verified stock and unit pricing for the ADS1292IPBS ($13.51), ADS1291IPBS ($11.54), ADS1299-4PAGR ($44.99), BQ25100 ($2.08), and Seeed XIAO nRF52840 ($15.40).
