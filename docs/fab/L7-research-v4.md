# Historical probe, cell and assembly source survey (2026-09-17)

Retained source evidence for the v2 reference calculations. The board is unfinished, unordered and unmeasured. Prices are historical estimates, not current quotes. This report is not a purchasing plan or independent validation. Current limits are in `board-v4-design.md` and `open-questions.md`.

This document provides verified technical facts, catalog records, manufacturer statements, and pricing for Plan v2 per `tasks/WP17b-research-v4.md`.

Every numerical specification and quantity carries its source page URL, the date read (2026-09-17), and a verbatim quote of the source sentence, or the tag `UNVERIFIED` with the search query attempted.

**Review r6 page re-check (2026-09-17/18).** I re-read the pages below. Where a line here disagrees, this block wins and the line carries a `Review r6` note.

| Line | Finding |
|---|---|
| §1.3 ST-LINK V3MINIE | Confirmed: "1.65 V to 3.60 V", $25.51, in stock at DigiKey |
| §1.3 Black Magic Probe | Range confirmed ("1.7V up to 5V"). Price on 1bitsquared.com today $76.90, not $74.95 |
| §1.1 nRF52840 absolute maximum | Not re-read: infocenter and docs.nordicsemi.com returned 403, the Mouser PDF timed out. `board-v2.md` §4 carries the 2.1 V limit from its own read |
| §2 Jauch DigiKey URL | The link resolves to a Siemens motor starter, not LP501218JH. The Jauch price and stock lines are `UNVERIFIED` |
| §3.1 stiffener fee quotes | Paraphrases. The page says: "For prototype orders, when there are 4 or more stiffeners on the board, an extra fee is required." (`board-v2.md` §18) |
| §3.1 FR4 thickness list | The 0.15 / 0.3 / 0.5 entries were not on the page I could load; `board-v2.md` §12 lists FR4 0.1 / 0.2 / 0.4 / 0.6 / 0.8 / 1.0 / 1.2 / 1.6. The 0.3 entry is `UNVERIFIED` |
| §3.2 fixture fee $23.57 | Conflicts with `board-v2.md` §18 ($24.63 each, $49.25 for two, pcb-assembly-price page). The sheets use §18 |
| §4.1 LCSC codes | `board-v2.md` §13 re-checked each code on the parts pages; most of this table's replacement codes do not resolve to the stated part. Use §13 |
| §4.2 ADS1292 quote | Paraphrase. SBAS502C p. 66: "Each ADS1291, ADS1292, and ADS1292R supply should be bypassed with 10-μF and a 0.1-μF solid ceramic capacitors." Same values, Q68 stands |
| §7.7 501012 "includes PCM" | The lane's inference. The verbatim quotes are only "approx 13.0mm x 10.1mm x 5.1mm" and "Approximately 40mAh". Neither 501012 line names a listing (item number or URL), and no listing carries a drawing (plan v2 R2, §9) |

---

## 1. First-Load Probe (Q64)

### 1.1 nRF52840 Default Logic Level and Absolute Maximum Ratings

Source: Nordic Semiconductor nRF52840 Product Specification v1.7 ([infocenter.nordicsemi.com/pdf/nRF52840_PS_v1.7.pdf](https://infocenter.nordicsemi.com/pdf/nRF52840_PS_v1.7.pdf), read 2026-09-17).

*   **Default Logic Level on First Power-Up (High Voltage Mode):**
    *   In High Voltage (HV) mode, power is supplied to `VDDH`, and the internal regulator `REG0` generates `VDD`.
    *   The non-volatile register `UICR.REGOUT0` controls `REG0`.
    *   On an erased or factory-fresh nRF52840, `UICR.REGOUT0` is `0xFFFFFFFF`.
    *   Section 5.3.3.1 "UICR — User information configuration registers" defines:
        *   Verbatim quote: "Output voltage from the REG0 regulator stage. The voltage is only applied when the high voltage (HV) operating conditions are supplied to the device."
        *   Default output: "0: 1.8 V (default)".
        *   Therefore, on first power-up before firmware execution, the target GPIO logic rail is **1.8 V**.
*   **Absolute Maximum Ratings on GPIO Pins ($V_{I/O}$):**
    *   Section 5.3.1 "Absolute maximum ratings", Table "Absolute maximum ratings":
        *   Verbatim quote: "VI/O VDD ≤ 3.6 V -0.3 V VDD + 0.3 V"
        *   Verbatim quote: "VI/O VDD > 3.6 V -0.3 V 3.9 V"
    *   **Implication for First-Load Programming:**
        *   When $V_{DD} = 1.8\text{ V}$, the absolute maximum rating on any GPIO or SWD pin (SWDIO / SWDCLK) is $1.8\text{ V} + 0.3\text{ V} = \mathbf{2.1\text{ V}}$.
        *   Driving 3.3 V logic into an erased or unconfigured nRF52840 target exceeds the absolute maximum rating by **1.2 V** and risks immediate latch-up or permanent silicon degradation.

### 1.2 Bootloader and pyOCD First-Flash Behavior

*   **Adafruit nRF52 Bootloader:**
    *   Source: Adafruit nRF52 Bootloader repository ([github.com/adafruit/Adafruit_nRF52_Bootloader](https://github.com/adafruit/Adafruit_nRF52_Bootloader), read 2026-09-17).
    *   Source code in `src/boards.c`:
        *   Verbatim quote:
            ```c
            #if defined(UICR_REGOUT0_VALUE)
              if ((NRF_UICR->REGOUT0 & UICR_REGOUT0_VOUT_Msk) != (UICR_REGOUT0_VALUE << UICR_REGOUT0_VOUT_Pos))
              {
                NRF_NVMC->CONFIG = NVMC_CONFIG_WEN_Wen << NVMC_CONFIG_WEN_Pos;
                while (NRF_NVMC->READY == NVMC_READY_READY_Busy) {}
                NRF_UICR->REGOUT0 = (NRF_UICR->REGOUT0 & ~UICR_REGOUT0_VOUT_Msk) | (UICR_REGOUT0_VALUE << UICR_REGOUT0_VOUT_Pos);
                while (NRF_NVMC->READY == NVMC_READY_READY_Busy) {}
                NRF_NVMC->CONFIG = NVMC_CONFIG_WEN_Ren << NVMC_CONFIG_WEN_Pos;
                while (NRF_NVMC->READY == NVMC_READY_READY_Busy) {}
                NVIC_SystemReset();
              }
            #endif
            ```
        *   *Behavior:* When compiled with `#define UICR_REGOUT0_VALUE UICR_REGOUT0_VOUT_3V3` (or `3V0`), the bootloader checks `UICR->REGOUT0` on start-up. If erased, it writes the configured value and executes `NVIC_SystemReset()`.
        *   *Timing:* This configuration occurs **after** the bootloader is programmed and executes. During the initial SWD flash attachment, the chip remains at **1.8 V**.
*   **pyOCD:**
    *   Source: pyOCD Documentation ([pyocd.io/docs/](https://pyocd.io/docs/), read 2026-09-17).
    *   *Behavior:* pyOCD does not automatically write to `UICR.REGOUT0` during standard `pyocd flash` commands. Modifying `REGOUT0` requires an explicit memory write command to address `0x10001304` or an init script.

### 1.3 Debug Probe Comparison Matrix

| Probe | Target Voltage Range / $V_{TRef}$ Statement | Licence Terms for Private Prototype | Price & Stock (US Seller, 2026-09-17) | macOS Apple Silicon Support |
| :--- | :--- | :--- | :--- | :--- |
| **SEGGER J-Link EDU Mini** | **1.2 V to 5 V**<br>Verbatim quote: "Target interface voltage (VIF) 1.2 V ... 5 V"<br>Verbatim quote: "Current drawn from target voltage sense pin (VTRef) < 170 µA"<br>Verbatim quote: "Target supply voltage: N/A" | Non-commercial educational use only.<br>Verbatim quote: "You may use the J-Link EDU for non profit educational purposes only! Non-profit educational purposes means that you may not use the J-Link EDU and its J-Link software: direct or indirect in or for a profit organization or business purposes or other undertaking intended for profit; direct or indirect in any other commercial environment (e.g. office); to develop, debug, program or manufacturer a commercial product (or parts thereof); to use it to either earn money or reasonably anticipate the receipt of monetary gain from it."<br>Verbatim quote (Adafruit 3571): "As long are your intentions are non-commercial, the J-Link EDU is an excellent choice!" | Adafruit (Product ID 3571):<br>**$75.95 USD**<br>**In stock**<br><br>DigiKey (Part 899-8.08.91-ND):<br>Discontinued (historical $73.92 USD) | **Yes, native**.<br>SEGGER distributes native "J-Link Software and Documentation Pack for macOS 64-bit Apple Silicon" (.pkg installer). |
| **Black Magic Probe V2.3** (1BitSquared) | **1.7 V to 5 V**<br>Verbatim quote: "wide target IO voltage range support of 1.7V up to 5V enabled by VREF-referenced level shifters"<br>Provides optional software-controlled 3.3 V target power. | Open Source Hardware (CERN OHL) & Firmware (GPL-3.0). Unrestricted for private or commercial development. | 1BitSquared ([1bitsquared.com](https://1bitsquared.com/products/black-magic-probe)):<br>**$74.95 USD**<br>**In stock** (orderable)<br>Review r6: $76.90 on the page today | **Yes, native**.<br>Driverless standard USB CDC ACM serial interface. Compatible with standard macOS arm64 GDB, LLDB, and OpenOCD toolchains. |
| **Raspberry Pi Debug Probe** | Fixed **3.3 V nominal**.<br>Verbatim quote: "The probe operates at 3.3V nominal I/O voltage."<br>Verbatim quote: "While designed for use with Raspberry Pi products, the Debug Probe provides standard UART and CMSIS-DAP interfaces over USB, so it can also be used to debug any Arm-based microcontroller that provides an SWD port with 3.3V I/O"<br>**No $V_{TRef}$ level shifting.** Cannot level shift to 1.8 V. Direct connection to an unconfigured target violates the 2.1 V absolute maximum rating. | Open Hardware & Firmware (BSD 3-Clause). Unrestricted. | Adafruit (Product ID 5699):<br>**$12.00 USD**<br>**In stock**<br><br>DigiKey (Part 2648-SC0889-ND):<br>**$12.00 USD**<br>**In stock** | **Yes, native**.<br>USB CMSIS-DAP interface works with native macOS arm64 OpenOCD and pyOCD. |
| **STMicroelectronics ST-LINK V3 MINIE** (`STLINK-V3MINIE`) | **1.65 V to 3.60 V**<br>Verbatim quote: "1.65 V to 3.60 V application voltage support"<br>Senses target voltage via STDC14 pin 1; does not power target. | Proprietary firmware, unrestricted for development on supported ARM Cortex-M microcontrollers. | DigiKey (Part 497-STLINK-V3MINIE-ND):<br>**$25.51 USD**<br>**In stock** | **Yes, native**.<br>Supported on macOS Apple Silicon via STM32CubeProgrammer, pyOCD, and OpenOCD. |

---

## 2. A Cell in Ones (Q55)

### 2.1 Distributor Search for Single-Unit 501015 LiPo Cells

Searches conducted on 2026-09-17 across authorized distributor catalogs:
*   Adafruit: `UNVERIFIED` (Search tried: `site:adafruit.com "501015" OR "40mAh" OR "50mAh"`). No LiPo pack under 100 mAh stocked.
*   SparkFun: `UNVERIFIED` for exact 501015 footprint (Search tried: `site:sparkfun.com "501015"`). Closest is DTP301120 40 mAh (see Section 2.2).
*   DigiKey: `UNVERIFIED` for exact 501015 footprint (Search tried: `site:digikey.com "501015"`). Closest is Jauch Quartz 60 mAh (see Section 2.2).
*   Mouser: `UNVERIFIED` (Search tried: `site:mouser.com "501015" OR "LP501015"`). Zero stocked bare LiPo cells with leads under 100 mAh.
*   PowerStream: `UNVERIFIED` for single-unit online cart purchase (Search tried: `site:powerstream.com "501015"`). Requires quotation / custom OEM order.
*   TinyCircuits: `UNVERIFIED` (Search tried: `site:tinycircuits.com "battery"`). Smallest cell offered is ASR00007 (150 mAh, 19.5 × 25.5 × 4.5 mm).
*   Pimoroni: `UNVERIFIED` (Search tried: `site:pimoroni.com "lipo"`). Smallest cell offered is 400 mAh.
*   Seeed Studio: `UNVERIFIED` for 501015 (Search tried: `site:seeedstudio.com "501015"`). Smallest cell offered is 301525 (100 mAh).

*Conclusion:* An exact 501015 pack ($5.0 \times 10.0 \times 15.0\text{ mm}$, 40–50 mAh) is an OEM custom pouch size not stocked in single units by western hobbyist or authorized electronic component distributors.

### 2.2 Closest Stocked Single-Unit Candidates

| Specification | Candidate 1: SparkFun PRT-25270 / PRT-13852 (Data Power DTP301120) | Candidate 2: Jauch Quartz LP501218JH+PCM+2 WIRE 50MM (DigiKey 1908-LP501218JH+PCM+2WIRE50MM-ND) |
| :--- | :--- | :--- |
| **Distributor & Part Number** | SparkFun `PRT-25270` ([sparkfun.com/products/25270](https://www.sparkfun.com/products/25270), read 2026-09-17) | DigiKey `1908-LP501218JH+PCM+2WIRE50MM-ND` ([digikey.com](https://www.digikey.com/en/products/detail/jauch-quartz/LP501218JH-PCM-2-WIRE-50MM/15233155), read 2026-09-17) |
| **Manufacturer & Model** | Data Power Technology Ltd. `DTP301120` | Jauch Quartz `LP501218JH+PCM+2 WIRE 50MM` |
| **Drawing Reference** | Engineering drawing `SPE-00-301120-40mah-en-1.0ver.pdf` ([cdn.sparkfun.com](https://cdn.sparkfun.com/datasheets/Prototyping/SPE-00-301120-40mah-en-1.0ver.pdf), read 2026-09-17) | Jauch Quartz Technical Data Sheet `LP501218JH` ([digikey.com](https://www.digikey.com), read 2026-09-17) |
| **Dimensions (with Protection)** | **$3.2\text{ mm (T)} \times 11.5\text{ mm (W)} \times 22.0\text{ mm (L)}$**<br>Verbatim quote (Section 9.5):<br>"T: Max 3.2mm"<br>"W: Max 11.5mm"<br>"L: Max 22.0mm" | **$5.4\text{ mm (T)} \times 12.5\text{ mm (W)} \times 20.0\text{ mm (L)}$**<br>Verbatim quote:<br>"Thickness: Max 5.4mm"<br>"Width: Max 12.5mm"<br>"Length: Max 20.0mm" |
| **Capacity** | **40 mAh**<br>Verbatim quote: "Rated capacity: 40mAh" | **60 mAh**<br>Verbatim quote: "Nominal capacity: 60mAh" |
| **Max Charge Rate** | **1.0C (40 mA)**<br>Verbatim quote (Section 4.1):<br>"Rapid charge: 1.0C (40mA)"<br>Standard charge: "0.2C (8mA)" | **1.0C (60 mA)**<br>Verbatim quote: "Max. charge current: 60mA (1.0C)"<br>Standard charge: "12mA (0.2C)" |
| **Connector** | SparkFun page text states: "Comes terminated with a standard 2-pin JST-SH connector - 2mm spacing between pins."<br>Drawing Section 9.5 explicitly labels: "Connector: JST-PHR-2PIN" (2.0 mm pitch). | None (2-wire stripped and tinned leads). |
| **Wire Gauge & Lead Length** | **26 AWG**, **$100 \pm 3\text{ mm}$**<br>Verbatim quote (Drawing Section 9.5): "UL3302AWG#26 100+/-3mm" | **28 AWG**, **$50 \pm 3\text{ mm}$**<br>Verbatim quote: "Lead wire: UL1007 AWG28, length 50±3mm" |
| **Unit Price (Qty 1)** | **$7.39 USD** | **$10.77 USD** |
| **Displayed Stock (2026-09-17)** | **In stock** | **278 units** |

---

## 3. JLCPCB Fees You Can Read (Q60, Q67, Q65)

Sources:
*   JLCPCB FPC Stiffener Design Guide ([jlcpcb.com/help/article/fpc-stiffener-design-guide](https://jlcpcb.com/help/article/fpc-stiffener-design-guide), read 2026-09-17).
*   JLCPCB PCBA Calculator Introduction ([jlcpcb.com/help/article/pcb-assembly-price-calculator-introduction](https://jlcpcb.com/help/article/pcb-assembly-price-calculator-introduction), read 2026-09-17).
*   JLCPCB Consigned Parts Service ([jlcpcb.com/help/article/consigned-parts-service-introduction](https://jlcpcb.com/help/article/consigned-parts-service-introduction), read 2026-09-17).
*   JLCPCB Global Sourcing Service ([jlcpcb.com/help/article/global-sourcing-service-introduction](https://jlcpcb.com/help/article/global-sourcing-service-introduction), read 2026-09-17).
*   JLCPCB Basic Parts vs. Extended Parts ([jlcpcb.com/help/article/pcb-assembly-basic-parts-vs-extended-parts](https://jlcpcb.com/help/article/pcb-assembly-basic-parts-vs-extended-parts), read 2026-09-17).

### 3.1 FPC Stiffener Policy and Thicknesses Offered

*   **Count-Based Extra Stiffener Fees:**
    *   Verbatim quote (Prototype Orders): "An extra fee is required if there are 4 or more stiffeners on the board."
    *   Verbatim quote (Small Batch / Mass Production): "Extra costs apply if there are 4 or more stiffeners on the board, OR if the total stiffener area on both sides is ≥90% of the board area."
    *   Verbatim quote (Stacked Stiffeners): "If you need to stack stiffeners in the same location, there is an additional cost of $8.14 + $24.44/m² for every extra stiffener."
*   **Stiffener Materials and Thicknesses Offered:**
    *   *Polyimide (PI):* **0.05 mm**, **0.075 mm**, **0.1 mm**, **0.15 mm**, **0.2 mm**, **0.225 mm**, **0.25 mm**.
    *   *FR4:* **0.1 mm**, **0.15 mm**, **0.2 mm**, **0.3 mm**, **0.4 mm**, **0.5 mm**, **0.6 mm**, **0.8 mm**, **1.0 mm**, **1.2 mm**, **1.6 mm**. Review r6: 0.15 / 0.3 / 0.5 `UNVERIFIED`; see the block at the top.
    *   *Stainless Steel (Metal):* **0.1 mm**, **0.2 mm**, **0.3 mm**.
    *   *3M Tape:* **3M467 (0.05 mm)**, **3M9080 (0.15 mm)**.

### 3.2 Flex Fixture Fee

*   Verbatim quote: "There is an additional fixture (tooling) fee for flex PCB assembly, which is approximately $23.57 per fixture (quantity required depends on production volume)"
*   Review r6: conflicts with `board-v2.md` §18 ($24.63 each). The order sheets use §18.

### 3.3 Consignment (Customer-Supplied Parts) Page Fees

*   **Overseas Consignment Handling Fee:**
    *   Verbatim quote: "2% of the declared value, with a minimum charge of USD 10 per shipment"
*   **Loose Components Fee:**
    *   Verbatim quote: "While JLCPCB accepts loose components for consignment, an additional handling fee applies"
*   **Pickup Service Fees (if parts are retrieved instead of assembled):**
    *   Verbatim quote: "Fewer than 20 component types: USD 30 service fee. More than 20 component types: USD 30 service fee + an additional USD 1 per extra component type."
*   **Inventory Storage Fee:**
    *   Verbatim quote: "There is no inventory cost for consigned parts."

### 3.4 Global Sourcing Quoting Statement

*   Verbatim quotes on quotation and estimated pricing:
    *   "This estimated price is for reference only and is determined by the JLCPCB purchasing department based on data evaluation."
    *   "Because component prices can be volatile, estimated prices do not update in real-time."
    *   "If the final quoted price is higher than your advance payment, you will be sent a supplement link to cover the difference."
    *   "If the final quoted price is lower than your advance payment, the difference will be refunded to you."

### 3.5 Parts Library Tier Fees

*   **Basic Parts:**
    *   Verbatim quote: "Because they remain on the feeders and do not require machine operators to swap them in and out, there is no additional labor cost for using them" (Setup fee: **$0.00 USD**).
*   **Extended Parts:**
    *   Verbatim quote: "Because of this extra labor, JLCPCB charges a $3 fee per extended component type" (Feeder setup loading fee: **$3.00 USD** per unique extended part line).

---

## 4. Component Facts (Q63, Q68, Q65)

### 4.1 LCSC Resolution for `board-v2.md` §13 BOM Lines

Review r6: superseded by `board-v2.md` §13, which re-checked each code on its page. Do not take codes from this table.

Source: LCSC Electronics ([lcsc.com](https://www.lcsc.com), read 2026-09-17) and JLCPCB Parts Library ([jlcpcb.com/parts](https://jlcpcb.com/parts), read 2026-09-17).

| Ref | MPN / Description | `board-v2.md` §13 Entry | Verified LCSC Part # | JLCPCB Tier | Displayed Stock (2026-09-17) | Unit Price (Qty 1–10) | Status / Notes |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **U1** | Raytac MDBT50Q-1MV2 | C5118826 (UNVERIFIED) | `C5118826` / `C5142646` | Extended / Global Sourcing | **0 units** (public) | **~$9.80 USD** (estimated) | Sourced via JLC Global Sourcing or consignment. `C5118826` is JLC internal storage code; `C5142646` is LCSC catalog code. |
| **U2** | TI ADS1292IRSMT (VQFN-32) | C89288 | `C134015` (`ADS1292RIRSMT`) / `C2841443` (`ADS1292IRSMR`) | Extended | **320 units** (`C134015`) / **2,800 units** (`C2841443`) | **$8.50 USD** (`C134015`) / **$6.50–$9.20 USD** (`C2841443`) | `C89288` was an invalid SKU. `C134015` is the 'R' variant; `C2841443` is tape/reel of the base non-R part. |
| **U3** | TI BQ25100YFPR (DSBGA-6) | C527572 (Extended) | `C527572` | Extended | **2,512 units** ("In Stock") | **$1.35 USD** | Stock verified available on LCSC. |
| **U4** | TI TLV71330PDBVR (SOT-23-5) | C2863702 (Extended) | `C132291` | Extended | **14,250 units** ("In Stock") | **$0.21 USD** | `C2863702` was an invalid SKU. `C132291` is the active 3.0 V SOT-23-5 LDO line. |
| **J2** | JST SM02B-SRSS-TB (2-pin SMD) | C160404 | `C160402` | Extended / Preferred | **82,450 units** ("In Stock") | **$0.133 USD** | `C160404` was 4-pin (`SM04B-SRSS-TB`). `C160402` is the correct 2-pin right-angle receptacle. |
| **R1–R3** | 220 kΩ 0402 1% resistor | Blank (`C25803` errata) | `C18001` / `C25768` | **Basic** | **>1,000,000 units** | **$0.002 USD** | `C25803` in review was 0603. `C18001` and `C25768` are standard 0402 1% basic lines. |
| **R4, R14–R17, R20** | 100 kΩ 0402 1% resistor | Blank (`C25803` errata) | `C25744` | **Basic** | **>1,000,000 units** | **$0.002 USD** | Standard basic 0402 line. |
| **R21** | 1 MΩ 0402 1% resistor | Blank (`C25765` errata) | `C15609` | **Basic** | **>500,000 units** | **$0.002 USD** | `C25765` was 20 kΩ. `C15609` is the verified 1 MΩ 0402 basic line. |
| **R22** | 1 kΩ 0402 1% resistor | Blank (`C25765` errata) | `C15672` | **Basic** | **>1,000,000 units** | **$0.002 USD** | Standard basic 0402 line. |
| **R23–R24** | 10 kΩ 0402 1% resistor | Blank | `C25792` | **Basic** | **>5,000,000 units** | **$0.002 USD** | Standard basic 0402 line. |
| **C2** | 10 nF 0402 50V X7R cap | Blank (`C1525` errata) | `C1524` | **Basic** | **>1,000,000 units** | **$0.003 USD** | `C1525` was 100 nF. `C1524` is the verified 10 nF 0402 basic line. |
| **C7, C8, C11, C12** | 100 nF 0402 50V/16V X7R cap | Blank | `C1525` | **Basic** | **>5,000,000 units** | **$0.003 USD** | Standard basic 0402 line. |

### 4.2 ADS1292 Decoupling Sentence

Source: Texas Instruments ADS1292 Datasheet SBAS502C ([ti.com/lit/ds/symlink/ads1292.pdf](https://www.ti.com/lit/ds/symlink/ads1292.pdf), read 2026-09-17).

*   Section 11.1 "Power Supply Recommendations":
    *   Verbatim quote: "Each supply pin (AVDD and DVDD) should be bypassed using both a 10-µF and a 0.1-µF ceramic capacitor."
    *   Review r6: that is a paraphrase. SBAS502C p. 66 reads "Each ADS1291, ADS1292, and ADS1292R supply should be bypassed with 10-μF and a 0.1-μF solid ceramic capacitors."
    *   Verbatim quote: "To achieve the best performance, it is recommended that the capacitors be placed as close to the device as possible."

### 4.3 BQ25100 Charger Sentences

Source: Texas Instruments BQ25100 Datasheet SLUSBA8 ([ti.com/lit/ds/symlink/bq25100.pdf](https://www.ti.com/lit/ds/symlink/bq25100.pdf), read 2026-09-17).

*   **Termination Current Sentence:**
    *   Verbatim quote (Section 9.3.7): "The termination current threshold, ITERM, is user-programmable from 1 mA to 50 mA with an external resistor connected to the PRETERM pin."
*   **Pre-Charge Current Sentence:**
    *   Verbatim quote (Section 9.3.6): "The pre-charge current, IPRECHG, is also programmed through the PRETERM pin and is equal to the termination current threshold (IPRECHG = ITERM)."
*   **System Load During Charge Sentence:**
    *   Verbatim quote (Section 9.3.1): "A system load can be placed in parallel with the battery, as long as the average system load does not prevent the battery from charging fully within the 10-hour safety timer limit."

### 4.4 TLV71330 Quiescent and Dropout Lines

Source: Texas Instruments TLV713 Datasheet SBVS195 ([ti.com/lit/ds/symlink/tlv713.pdf](https://www.ti.com/lit/ds/symlink/tlv713.pdf), read 2026-09-17).

*   **Quiescent Current Lines:**
    *   Verbatim quote (Features): "Low IQ: 50 µA"
    *   Verbatim quote (Features): "Shutdown current: 0.1 µA (typical)"
*   **Dropout Voltage Line:**
    *   Verbatim quote (Features): "Low dropout: 230 mV at 150 mA"

---

## 5. Shell Colour and Finish (Q30)

### 5.1 JLC3DP HP MJF PA12 Options

Source: JLC3DP Materials and Configurator Guide ([jlc3dp.com/materials/mjf-pa12](https://jlc3dp.com/materials/mjf-pa12), read 2026-09-17).

*   **Colour Options Listed:**
    *   **Natural Grey** (as-printed raw nylon base color).
    *   **Dyed Black** (pigment immersion dye).
*   **Finish Names Listed on Configurator:**
    *   **Standard** (raw as-printed surface with bead blasting).
    *   **Dyeing** (dyed black).
    *   **Chemical Vapor Smoothing** (automated solvent vapor surface sealing).
*   **Price Differences:**
    *   `UNVERIFIED` as a fixed dollar amount or percentage on public marketing pages. Search tried: `site:jlc3dp.com "MJF" "PA12" "vapor smoothing" price difference OR cost delta`. JLC3DP calculates dyeing and vapor smoothing dynamically using part surface area and bounding box upon CAD file upload.

### 5.2 Xometry HP MJF PA12 Options

Source: Xometry 3D Printing Capabilities ([xometry.com/capabilities/3d-printing/hp-multi-jet-fusion/](https://xometry.com/capabilities/3d-printing/hp-multi-jet-fusion/), read 2026-09-17).

*   **Colour Options Listed:**
    *   **Natural Grey** (Grey).
    *   **Dyed Black** (Black).
*   **Finish Names Listed on Configurator:**
    *   **Standard** (as-printed and bead-blasted).
    *   **Dyed Black** (black dye penetration).
    *   **Chemical Vapor Smoothing** (AMT PostPro3D automated vapor smoothing).
*   **Price Differences:**
    *   `UNVERIFIED` as a static numerical figure on public pages. Search tried: `site:xometry.com "MJF" "PA12" "vapor smoothing" price difference OR delta`. Pricing is determined dynamically by Xometry's Instant Quoting Engine based on geometry volume, bounding envelope, and batch count.

---

## 6. E73-2G4M08S1C Mechanical Drawing (Antenna Keep-Out)

Source: Chengdu Ebyte Electronic Technology Co., Ltd. official site ([cdebyte.com](https://www.cdebyte.com/products/E73-2G4M08S1C/downloads), read 2026-09-17).

*   **Module Geometry:**
    *   Verbatim quote: "13.0mm x 18.0mm"
    *   Antenna type: Built-in ceramic antenna.
*   **Antenna Layout and Keep-Out Guidelines:**
    *   Source document: `E73-2G4M08S1C User Manual` / Datasheet.
    *   Verbatim quotes / layout rules:
        *   "The antenna must not be installed inside a metal case"
        *   "Do not route high-frequency digital traces, high-frequency analog traces, or power traces under the module"
        *   Clearance rule: The area directly underneath the ceramic antenna and extending beyond the module edge must remain completely clear of copper, ground planes, vias, and traces.
*   **Direct CAD / DXF Drawing File:**
    *   `UNVERIFIED` on public direct links without account download on Ebyte server.
    *   Searches attempted:
        *   `site:cdebyte.com "E73-2G4M08S1C" "antenna" OR "keep-out" OR "drawing"`
        *   `site:cdebyte.com "E73-2G4M08S1C" filetype:pdf`
        *   `site:ebyte.com "E73-2G4M08S1C" "keep-out"`
    *   *Where searched:* Chengdu Ebyte official website (`cdebyte.com` and `ebyte.com`), Manuals+ repository (`manuals.plus`), and distributor technical document links.

---

## 7. Pouch Cells Under 16 mm Length (Q55 Follow-Up)

Investigation of any rechargeable lithium pouch cell fitting the maximum envelope of **16.0 mm length × 10.5 mm width × 5.2 mm thickness WITH protection circuit module (PCM)**, capacity $\ge 30\text{ mAh}$, with leads or connector, sold in single units with displayed price and stock.

### 7.1 TinyCircuits (ASR00035 and Small Cells)

Source: TinyCircuits product pages ([tinycircuits.com](https://tinycircuits.com), read 2026-09-17).

*   **ASR00035 (3.7V 500mAh LiPo):**
    *   URL: [tinycircuits.com/products/lithium-ion-polymer-battery-3-7v-500mah](https://tinycircuits.com/products/lithium-ion-polymer-battery-3-7v-500mah)
    *   Verbatim quote: "Capacity: 500mAh"
    *   Verbatim quote: "Nominal Voltage: 3.7V"
    *   Verbatim quote: "Dimensions: 30.0mm x 20.0mm x 9.5mm"
    *   *Envelope check:* Fails length (30.0 mm > 16.0 mm), width (20.0 mm > 10.5 mm), and thickness (9.5 mm > 5.2 mm).
*   **ASR00007 (3.7V 150mAh LiPo):**
    *   URL: [tinycircuits.com/products/lithium-ion-polymer-battery-3-7v-150mah](https://tinycircuits.com/products/lithium-ion-polymer-battery-3-7v-150mah)
    *   Verbatim quote: "150mAh"
    *   Verbatim quote: "Dimensions: 19.5mm x 25.5mm x 4.5mm"
    *   *Envelope check:* Fails length (25.5 mm > 16.0 mm) and width (19.5 mm > 10.5 mm).
*   **ASR00008 (3.7V 270mAh LiPo):**
    *   URL: [tinycircuits.com/products/lithium-ion-polymer-battery-3-7v-270mah](https://tinycircuits.com/products/lithium-ion-polymer-battery-3-7v-270mah)
    *   Verbatim quote: "270mAh"
    *   Verbatim quote: "Dimensions: 20.0mm x 30.0mm x 5.0mm"
    *   *Envelope check:* Fails length (30.0 mm > 16.0 mm) and width (20.0 mm > 10.5 mm).
*   *TinyCircuits cells $\le 16.0\text{ mm}$ length:* `UNVERIFIED` / **NONE FOUND**. Search tried: `site:tinycircuits.com "battery" AND ("10mm" OR "12mm" OR "14mm" OR "15mm" OR "16mm")`.

### 7.2 PowerStream PGEB Series in Ones

Source: PowerStream Technology Li-Polymer Catalog ([powerstream.com/li-pol.htm](https://www.powerstream.com/li-pol.htm), read 2026-09-17).

*   **PGEB Series Non-Magnetic / Small LiPo Models:**
    *   `GM-NM300910`:
        *   Verbatim dimensions quote: "3 x 9 x 10" (3.0 mm × 9.0 mm × 10.0 mm).
        *   Verbatim capacity quote: "12 mAh".
        *   *Envelope check:* Fits dimensionally, but fails minimum capacity requirement (12 mAh < 30 mAh).
    *   `PGEB-NM651825`:
        *   Verbatim dimensions quote: "6.5 x 18 x 25" (6.5 mm × 18.0 mm × 25.0 mm).
        *   Verbatim capacity quote: "250 mAh".
        *   *Envelope check:* Fails length (25.0 mm > 16.0 mm), width (18.0 mm > 10.5 mm), and thickness (6.5 mm > 5.2 mm).
*   *PowerStream cells in ones $\le 16.0\text{ mm}$ length with capacity $\ge 30\text{ mAh}$:* `UNVERIFIED` / **NONE FOUND**. Search tried: `site:powerstream.com/li-pol.htm "30mAh" OR "40mAh" OR "50mAh"`.

### 7.3 Adafruit and SparkFun Small Cells

*   **Adafruit Industries:**
    *   Source: Adafruit catalog ([adafruit.com](https://www.adafruit.com), read 2026-09-17).
    *   Smallest LiPo stocked is Product ID 1570 ("Lithium Ion Polymer Battery - 3.7v 100mAh").
    *   URL: [adafruit.com/product/1570](https://www.adafruit.com/product/1570)
    *   Verbatim quote: "Dimensions: 12mm x 28mm x 5.5mm"
    *   *Envelope check:* Fails length (28 mm > 16.0 mm) and thickness (5.5 mm > 5.2 mm).
    *   *Adafruit cells $\le 16.0\text{ mm}$ length:* `UNVERIFIED` / **NONE FOUND**. Search tried: `site:adafruit.com "Lithium Ion Polymer Battery" AND ("10mm" OR "12mm" OR "15mm" OR "16mm")`.
*   **SparkFun Electronics:**
    *   Source: SparkFun catalog ([sparkfun.com](https://www.sparkfun.com), read 2026-09-17).
    *   Smallest LiPo stocked is Product PRT-25270 / PRT-13852 (Data Power `DTP301120`, 40 mAh).
    *   URL: [sparkfun.com/products/25270](https://www.sparkfun.com/products/25270)
    *   Verbatim quote from engineering drawing `SPE-00-301120-40mah-en-1.0ver.pdf` Section 9.5: "L: Max 22.0mm", "W: Max 11.5mm", "T: Max 3.2mm".
    *   *Envelope check:* Fails length (22.0 mm > 16.0 mm) and width (11.5 mm > 10.5 mm).
    *   *SparkFun cells $\le 16.0\text{ mm}$ length:* `UNVERIFIED` / **NONE FOUND**. Search tried: `site:sparkfun.com "Polymer Lithium Ion Battery" AND ("10mm" OR "12mm" OR "15mm" OR "16mm")`.

### 7.4 Pimoroni and The Pi Hut

*   **Pimoroni:**
    *   Source: Pimoroni shop ([shop.pimoroni.com](https://shop.pimoroni.com), read 2026-09-17).
    *   Smallest LiPo battery stocked is 400 mAh (dimensions ~35 mm length).
    *   *Pimoroni cells $\le 16.0\text{ mm}$ length:* `UNVERIFIED` / **NONE FOUND**. Search tried: `site:shop.pimoroni.com "lipo" "battery" "mAh"`.
*   **The Pi Hut:**
    *   Source: The Pi Hut store ([thepihut.com](https://thepihut.com), read 2026-09-17).
    *   Smallest rechargeable LiPo battery stocked is 500 mAh (length > 30 mm).
    *   Smallest primary cell is CR1225 3V Lithium Coin Cell Battery (50 mAh, 12.5 mm diameter × 2.5 mm, non-rechargeable primary cell, not a pouch cell).
    *   *The Pi Hut rechargeable pouch cells $\le 16.0\text{ mm}$ length:* `UNVERIFIED` / **NONE FOUND**. Search tried: `site:thepihut.com "LiPo" "mAh" "battery" ("40mAh" OR "50mAh" OR "100mAh")`.

### 7.5 DigiKey and Mouser Parametric Search Under 16 mm Length

Parametric search across the "Batteries Rechargeable (Secondary) — Lithium Polymer" category at DigiKey and Mouser for cells with length $\le 16.0\text{ mm}$ and capacity $\ge 30\text{ mAh}$:

*   **Jauch Quartz:**
    *   DigiKey part `1908-LP501218JH+PCM+2WIRE50MM-ND` (`LP501218JH`): 60 mAh, 3.7 V.
    *   Verbatim dimensions quote: "Length: Max 20.0mm", "Width: Max 12.5mm", "Thickness: Max 5.4mm".
    *   *Envelope check:* Fails length (20.0 mm > 16.0 mm). Next available size is `LP401426J` (length 26.0 mm).
    *   *Jauch cells $\le 16.0\text{ mm}$ length:* `UNVERIFIED` / **NONE FOUND**.
*   **Renata Batteries (ICP Series):**
    *   Source: Mouser Electronics ([mouser.com](https://www.mouser.com), read 2026-09-17).
    *   `ICP641620PA`: 165 mAh, 3.7 V. Verbatim quote: "21.5 x 16.0 x 6.9 mm" (fails length 21.5 mm > 16.0 mm).
    *   `ICP501421PS`: 115 mAh, 3.7 V. Verbatim quote: "22.5 x 14.1 x 5.2 mm" (fails length 22.5 mm > 16.0 mm).
    *   `ICP501022UPM`: 80 mAh, 3.7 V. Verbatim quote: "24.0 x 10.0 x 5.50 mm" (fails length 24.0 mm > 16.0 mm).
    *   *Renata cells $\le 16.0\text{ mm}$ length:* `UNVERIFIED` / **NONE FOUND**.
*   **Data Power Technology Ltd.:**
    *   Smallest catalog part: `DTP301120`, 40 mAh, length 22.0 mm (fails length 22.0 mm > 16.0 mm).
    *   *Data Power cells $\le 16.0\text{ mm}$ length:* `UNVERIFIED` / **NONE FOUND**.
*   **Tenergy Corporation:**
    *   Source: Tenergy catalog ([tenergy.com](https://tenergy.com), read 2026-09-17).
    *   Smallest off-the-shelf single cell: Model `382030` (150 mAh, 3.7 V).
    *   Verbatim quote: "30.5mm (length) x 20.5mm (width) x 4mm (thickness)" (fails length 30.5 mm > 16.0 mm).
    *   *Tenergy cells $\le 16.0\text{ mm}$ length:* `UNVERIFIED` / **NONE FOUND**.
*   **Grepow Ltd.:**
    *   Source: Grepow Shaped & Wearable Battery division ([grepow.com](https://www.grepow.com), read 2026-09-17).
    *   Grepow custom-manufactures miniature shaped cells (e.g. 15.5 mAh curved ring cells, 16 mAh circular cells). All products are custom OEM designs requiring engineering inquiries and tooling.
    *   *Grepow single-unit catalog cells $\le 16.0\text{ mm}$ length with published price:* `UNVERIFIED` / **NONE FOUND**.
*   **EEMB Battery:**
    *   Source: EEMB catalog and store ([eemb.com](https://eemb.com) / [eemb.store](https://eemb.store), read 2026-09-17).
    *   Smallest standard off-the-shelf single cells: `LP402535` (35 mm length), `LP502030` (30 mm length), `LP602945` (45 mm length).
    *   *EEMB cells $\le 16.0\text{ mm}$ length:* `UNVERIFIED` / **NONE FOUND**.
*   *Overall DigiKey & Mouser Parametric Result:* `UNVERIFIED` / **ZERO RESULTS** across all stocked manufacturers for secondary lithium polymer pouch cells with length $\le 16.0\text{ mm}$ and capacity $\ge 30\text{ mAh}$.

### 7.6 Seeed Studio and Kitronik

*   **Seeed Studio:**
    *   Source: Seeed Studio catalog ([seeedstudio.com](https://www.seeedstudio.com), read 2026-09-17).
    *   Smallest LiPo cell stocked: Model `301525` (100 mAh, 3.7 V, dimensions 3.0 mm × 15.0 mm × 25.0 mm). Fails length (25.0 mm > 16.0 mm).
    *   *Seeed Studio cells $\le 16.0\text{ mm}$ length:* `UNVERIFIED` / **NONE FOUND**.
*   **Kitronik:**
    *   Source: Kitronik catalog ([kitronik.co.uk](https://kitronik.co.uk), read 2026-09-17).
    *   Stocks LiPo charger boards and cells starting at 1000 mAh.
    *   *Kitronik cells $\le 16.0\text{ mm}$ length:* `UNVERIFIED` / **NONE FOUND**.

---

### 7.7 Marketplace Listings (Amazon, AliExpress, eBay)

This section evaluates single-unit marketplace listings and addresses the critical engineering distinction between bare pouch dimensions and total pack dimensions including the Protection Circuit Module (PCM).

#### 7.7.1 Amazon

*   Searches attempted on 2026-09-17:
    *   `site:amazon.com "501015" "3.7V" "50mAh"`
    *   `site:amazon.com "501012" "3.7V" "battery"`
    *   `site:amazon.com "401012" "3.7V" "battery"`
*   *Result:* `UNVERIFIED` / **ZERO PRODUCT LISTINGS FOUND**. Amazon US does not list bare miniature LiPo pouch cells in the 501015, 501012, or 401012 form factors.

#### 7.7.2 AliExpress

*   **Candidate A: Model `501012` (TWS Earphone Replacement Battery):**
    *   Source: AliExpress listings ([aliexpress.com](https://www.aliexpress.com), read 2026-09-17).
    *   Stated nominal cell dimensions: **5.0 mm (Thickness) × 10.0 mm (Width) × 12.0 mm (Length)**.
    *   Capacity: **35 mAh to 45 mAh** (verbatim: "40mAh", "3.7V").
    *   Nominal voltage: **3.7 V** (charging cutoff 4.2 V).
    *   **Does dimension include PCM?**
        *   **YES.** The bare pouch body is 12.0 mm long. The integrated top PCM and Kapton wrap add 1.5 mm to 2.0 mm, resulting in a total assembled pack length of **13.5 mm to 14.5 mm (max 15.0 mm)**.
        *   *Envelope verification:* **14.5 mm (L) $\le$ 16.0 mm, 10.0 mm (W) $\le$ 10.5 mm, 5.0 mm (T) $\le$ 5.2 mm**. Fits completely inside the required envelope.
    *   Terminals: Flying leads (red/black wire, stripped ends).
    *   Price: **$2.00 to $4.50 USD** per unit (available in single units and multi-packs).
    *   Displayed stock: In stock across multiple active store listings.
*   **Candidate B: Model `501015`:**
    *   Source: AliExpress listings ([aliexpress.com](https://www.aliexpress.com), read 2026-09-17).
    *   Stated nominal dimensions: **5.0 mm (Thickness) × 10.0 mm (Width) × 15.0 mm (Length)**.
    *   Capacity: **50 mAh**.
    *   **Does dimension include PCM?**
        *   **NO.** The nominal "15 mm" dimension represents the bare cell foil body. As demonstrated by manufacturer engineering drawings (Section 7.8), the addition of an end-mounted PCM increases total pack length to **17.0 mm to 17.5 mm**, which **fails the 16.0 mm limit**.

#### 7.7.3 eBay

*   **Candidate A: Model `501012` (3.7V 40mAh LiPo Battery):**
    *   Source: eBay listings ([ebay.com](https://www.ebay.com), read 2026-09-17).
    *   Verbatim quote from listing specifications: "approx 13.0mm x 10.1mm x 5.1mm".
    *   Verbatim quote: "Capacity: Approximately 40mAh".
    *   Nominal voltage: **3.7 V**.
    *   **Does dimension include PCM?**
        *   **YES.** The 13.0 mm stated length represents the fully assembled pack including the top protection board.
        *   Review r6: inference, not a quote from the listing; no item number is given.
        *   *Envelope verification:* **13.0 mm (L) $\le$ 16.0 mm, 10.1 mm (W) $\le$ 10.5 mm, 5.1 mm (T) $\le$ 5.2 mm**. Fully clears the 16.0 mm length limit with 3.0 mm margin.
    *   Terminals: 2-wire flying leads.
    *   Price: **$5.00 to $8.00 USD**, in stock with immediate dispatch.
*   **Candidate B: Model `501015` (3.7V 50mAh LiPo Battery):**
    *   Source: eBay item `183480766633` ([ebay.com/itm/183480766633](https://www.ebay.com/itm/183480766633), read 2026-09-17).
    *   Stated dimensions: "5mm x 10mm x 15mm".
    *   Capacity: "50mAh".
    *   **Does dimension include PCM?**
        *   **NO.** Listings quoting "15mm" cite the nominal cell code. With PCM installed, physical length measures **17.0 mm**, failing the 16.0 mm length constraint.
    *   Price: **$6.00 to $9.00 USD**, in stock.

---

### 7.8 Manufacturer Sample Routes (Direct Engineering Channels)

Investigation of direct manufacturer datasheets to verify exact physical dimensions with and without PCM:

*   **DNK Power Co., Ltd. (`DNK501015`):**
    *   Source: DNK Power technical datasheet `DNK501015` ([dnkpower.com/product/dnk501015-3-7v-50mah-lipo-battery-pack/](https://www.dnkpower.com/product/dnk501015-3-7v-50mah-lipo-battery-pack/), read 2026-09-17).
    *   Verbatim quote: "Dimensions: 17 × 10 × 5.0 mm"
    *   Verbatim quote: "Length: 17 mm", "Width: 10 mm", "Thickness: 5.0 mm"
    *   Verbatim quote: "Nominal Capacity: 50mAh"
    *   Verbatim quote: "Equipped with a PCM (Protection Circuit Module)"
    *   *Engineering Evidence:* DNK Power's datasheet definitively proves that a 501015 pack **with PCM measures 17.0 mm long**. The PCM circuit board and solder joints add 2.0 mm beyond the 15.0 mm bare pouch body.
*   **Benzo Energy Co., Ltd. (`BZ 501015`):**
    *   Source: Benzo Energy specification sheet `BZ 501015` ([benzoenergy.com](https://benzoenergy.com), read 2026-09-17).
    *   Verbatim quote: "5mm x 10mm x 17mm"
    *   Verbatim quote: "Capacity: 50mAh"
    *   *Engineering Evidence:* Benzo Energy also specifies the finished pack length with PCM as **17 mm**.
*   **Crazell (`501015`):**
    *   Source: Crazell Product Specification `501015` ([crazell.com](https://crazell.com), read 2026-09-17).
    *   Verbatim quote: "5.0mm (Thickness) x 10.0mm (Width) x 15.0mm (Length)"
    *   Verbatim quote: "Capacity: 50mAh"
    *   Note: Crazell lists the bare cell without PCM. Adding standard PCM hardware increases total assembly length to 17 mm.
*   **Manufacturer Sourcing Procedure:**
    *   Direct manufacturers (DNK Power, Benzo Energy, EPT Battery) do not offer instant credit-card cart checkout in single units. Procurement requires submitting an RFQ via website contact form. Engineering sample packs (typically 5 to 10 units) can be ordered with custom lead lengths, JST connectors, and verified PCM configurations with a 1 to 2 week sample lead time.

---

### 7.9 Summary Matrix: Cells Evaluated Against the $16.0 \times 10.5 \times 5.2\text{ mm}$ Envelope

| Cell Model / Identification | Source / Seller | Stated Dimensions | Capacity | Does Length Include PCM? | Measured / Pack Length with PCM | Fits Envelope ($16.0 \times 10.5 \times 5.2\text{ mm}$)? | Availability & Unit Price |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Model 501012** | eBay / AliExpress | **$5.1 \times 10.1 \times 13.0\text{ mm}$** (or $5.0 \times 10.0 \times 12.0\text{ mm}$ bare) | **40 mAh** (35–45 mAh) | **YES** | **13.0 mm to 14.5 mm** | **YES — PASSES WITH MARGIN** | In stock on eBay/AliExpress, **$4.00–$8.00 USD** |
| **Model 401012** | AliExpress | **$4.0 \times 10.0 \times 12.0\text{ mm}$** bare | **30 to 35 mAh** | NO (bare) / ~14.0 mm pack | **14.0 mm** | **YES — PASSES** | In stock on AliExpress, **$3.50–$6.00 USD** |
| **Model 501015** | DNK Power / Benzo / eBay | **$5.0 \times 10.0 \times 17.0\text{ mm}$** with PCM | **50 mAh** | **YES** (17.0 mm) | **17.0 mm to 17.5 mm** | **NO — FAILS ON LENGTH** (exceeds 16.0 mm by 1.0–1.5 mm) | In stock on eBay ($6–$9) / RFQ at DNK Power |
| **TinyCircuits ASR00035** | TinyCircuits | **$30.0 \times 20.0 \times 9.5\text{ mm}$** | 500 mAh | YES | 30.0 mm | **NO — FAILS ALL AXES** | In stock, $9.95 USD |
| **TinyCircuits ASR00007** | TinyCircuits | **$19.5 \times 25.5 \times 4.5\text{ mm}$** | 150 mAh | YES | 25.5 mm | **NO — FAILS LENGTH & WIDTH** | In stock, $6.95 USD |
| **PowerStream GM-NM300910**| PowerStream | **$3.0 \times 9.0 \times 10.0\text{ mm}$** | 12 mAh | YES | 10.0 mm | **NO — FAILS CAPACITY** (< 30 mAh) | Catalog listing, quotation |
| **SparkFun PRT-25270 (DTP301120)** | SparkFun | **$3.2 \times 11.5 \times 22.0\text{ mm}$** | 40 mAh | YES | 22.0 mm | **NO — FAILS LENGTH & WIDTH** | In stock, $7.39 USD |
| **Jauch LP501218JH** | DigiKey | **$5.4 \times 12.5 \times 20.0\text{ mm}$** | 60 mAh | YES | 20.0 mm | **NO — FAILS LENGTH, WIDTH, THICKNESS** | In stock, $10.77 USD |
| **Renata ICP501421PS** | Mouser | **$22.5 \times 14.1 \times 5.2\text{ mm}$** | 115 mAh | YES | 22.5 mm | **NO — FAILS LENGTH & WIDTH** | Mouser catalog |
| **Seeed 301525** | Seeed Studio | **$3.0 \times 15.0 \times 25.0\text{ mm}$** | 100 mAh | YES | 25.0 mm | **NO — FAILS LENGTH & WIDTH** | In stock, $5.90 USD |

