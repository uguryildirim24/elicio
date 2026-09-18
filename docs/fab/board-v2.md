# Board v2 — schematic, G2/G4 records, release job

Status: design record for WP12b. Not for order, quote or upload.
Date: 2026-09-17.
KiCad: 10.0.6 (`kicad-cli`).
Interface: **II** (plan v2 §5.3 fallback). WP11 packing winner `A_501015_series_w20_y8_iII_s3` (`packing-v2.md` §5). USB-C sits on the hook-end end face (plan v2 §5.4 fallback). LID_Y 8.0. Standoff 3.0 mm on a 0.31 ring: board underside y 4.81, top y 5.32. Cell 501015 in series, foam 0.5. Board width 20 mm body, board zone u 2.25–17.75, s 18.60–37.60.

Project: `hardware/board/elicio-v2.kicad_pro`.
The schematic contract is the review-r5 sheet plus WP12b Q68 (10 µF + 0.1 µF on AVDD and on DVDD). The land is a 2-layer flex with two FR4 0.4 stiffeners and three ring-pad tabs.

Packing (u, s) = PCB (x, y). Named SMT centres follow `packing-v2.md` §5 (within 0.1 mm; `tests/test_board_release.py`). SIG1/SIG2 rings are unfolded off the island so the Gerber is flat. WP11b `lane/w3` §5 REF tab search (Q59) left the packing tab unchanged (`along_floor` (8.50, 43.00) → (8.50, 36.80)). This board uses that path. SMT centres match merged `packing-v2.md` §5.

| Item | PCB centre (u, s) | `packing-v2.md` §5 centre | Size / note |
|---|---|---|---|
| Board zone | u 2.25–17.75, s 18.60–37.60 | same | PI 0.11 + FR4 0.4 at parts. Packing and the shell take the rings as PI 0.11 + FR4 0.2 = 0.31; this Gerber has no ring FR4 (§12), so its rings are 0.11. Review r6 decision 72 |
| Module U1 | (10.00, 32.35) rot 90° | (10.00, 32.35) | 15.50 × 10.50 × 2.3, length along u; 0 pads in the RF box |
| Antenna keep-out | u 2.25–6.05, s 26.15–38.55 | same | no extra copper; module pads allowed |
| ADS1292 U2 | (4.90, 21.25) | (4.90, 21.25) | VQFN-32 4×4 courtyard in a 5×5 packing box |
| BQ25100 U3 | (3.45, 24.85) | (3.45, 24.85) | YFP-6 |
| TLV71330 U4 | (9.45, 20.20) | (9.45, 20.20) | SOT-23-5 |
| SW1 | (10.10, 24.20) | (10.10, 24.20) | 4.5 × 4.5 × 1.6 |
| J3 bench | (14.05, 22.60) | (14.05, 22.60) | 2.5 × 7.6 × 2.5 |
| USBLC6 U5 | (14.05, 3.10) | (14.05, 3.10) | pocket |
| PESD D1 | (13.50, 5.30) | (13.50, 5.30) | pocket |
| JST-SH J2 | (14.40, 9.15) | (14.40, 9.15) | pocket |
| USB-C J1 | (10.00, −2.15) | (10.00, −2.15) | hook-end end face |
| TC2030 J4 | (15.10, 5.40) rot 90° | SWD proxies were 1.0 mm pads | real Tag-Connect land on the pocket/neck, not the 1 mm packing dots |
| Cell 501015 | (7.00, 9.30) | (7.00, 9.30) | not on the flex |
| R1 220 kΩ | tab midpoint SIG1 | — | past the 4 mm strain-relief window |
| R2 220 kΩ | tab midpoint SIG2 | — | same |
| R3 220 kΩ | tab midpoint REF | — | same |

Leftover 0402/0603/SOT parts sit on B.Cu under the module and under the USB tongue so the front island matches the packing. Q68 0603 caps C6/C7/C8/C15 sit on B.Cu under the ADS.

## 1. Block diagram

```text
USB-C 16P --5.1k CC-- ESD(D+/D-/VBUS) -- VBUS
                                      |
                                      +--> nRF VBUS, VBUS_DET divider (P0.24)
                                      +--> BQ25100YFPR IN
                                      +--> Q2 (VBUS present) --|  hardware
                                                                |  inhibit
JST-SH BAT+ --> VBAT --> BQ25100 OUT, nRF VDDH, Q1 source      |
                 |                                              v
                 +--> P-FET Q1 -- AFE_VIN --> TLV71330PDBVR --> +3V0 --> ADS1292
                 +--> 1M/1M divider to GND (always on) --> VBAT_SENSE (P0.02 AIN0)

VBUS --1k--> LED D2 --> Q4 (gate LED_EN, P0.04, 10k pull-down) --> GND

SIG1 --220k--> ADS IN1P
SIG2 --220k--> ADS IN1N          RLD --220k--> REF pad
bench header J3 is behind the 220 kΩ (same nets as the pads)

Tag-Connect TC2030-NL: 1 +VDD sense, 2 SWDIO, 3 GND, 4 SWDCLK, 5 GND, 6 nRESET
SW1: nRESET to GND. R26 10k nRESET to +VDD.
```

The Raytac MDBT50Q-1MV2 is placed. The E73-2G4M08S1C footprint is in `hardware/board/lib/elicio.pretty` and is not placed.

## 2. Net summary

| Net | Role |
|---|---|
| VBAT | Pack positive. nRF VDDH, charger OUT, P-FET source |
| VBUS | USB 5 V. Charger IN, nRF VBUS, inhibit sense |
| +VDD | nRF REG0 output (DCCH inductor). Logic and SWD VTref |
| AFE_VIN | Switched pack rail after Q1 |
| +3V0 | TLV71330 3.0 V. ADS1292 AVDD and DVDD |
| GND | Common |
| SIG1, SIG2, REF | Contact pads and bench header, each through 220 kΩ |
| AFE_IN1P, AFE_IN1N | ADS channel 1 after 220 kΩ |
| RLD_FB, RLDINV | RLD loop (1 MΩ + 1.5 nF) |
| AFE_SCLK/MOSI/MISO/CS/DRDY | SPI plus DRDY, 10 kΩ series at the AFE |
| AFE_START, AFE_RESET | START and PWDN/RESET, 100 kΩ pulldown |
| ISET, PRETERM, TS | Charger programming |
| CHG_MON | ISET through R25 10 kΩ onto P0.31 AIN7 (high impedance; review r5 moved R28 off this node) |
| LED_EN | P0.04 (module pin 20) to Q4 gate, R28 10 kΩ pull-down |
| VBUS_DET | 47 kΩ / 27 kΩ onto P0.24 |
| VBAT_SENSE | 1 MΩ / 1 MΩ divider to GND, always connected. Q5 is DNP (BAT_MEAS_EN on P0.03 is unused) |
| SWDIO, SWDCLK, nRESET | First-load and recovery |

ADS1292 pin 15 is PWDN (power-down / reset). There is no separate RESET pin on the non-R device. AFE_RESET is that pin. **Deviates from a two-GPIO RESET+PWDN reading: the silicon has one pin.**

## 3. Gate G2 — electrode boundary states

R7 (plan v2): no galvanic isolation between USB-connected circuitry and the electrode paths. Skin-connected use is battery-only. The P-FET is an inhibit of the front-end supply when VBUS is present, not isolation.

Default hardware with an uncooperative MCU: R15 pulls Q3's gate up, Q3 pulls Q1's gate down against R14, so the P-FET is **on** and the AFE is powered whenever the pack is in and VBUS is absent. Q2 turns on when VBUS is present and holds AFE_EN_HW low, so Q3 turns off and R14 holds Q1 **off**. R23/R24 hold ADS PWDN and START low, so an AFE powered with no MCU help sits in reset. (Review r5: the lane's sentence said the P-FET is off by default; the table rows below already had it on.)

| State | Rails | Gate Q1 | SPI / control | Pull-ups | Protection | Back-power | Discharge / start-up |
|---|---|---|---|---|---|---|---|
| Powered, battery, no VBUS, MCU cooperative | VBAT, +VDD, AFE_VIN, +3V0 | On (Q3 on via R15) | Firmware drives SPI; PWDN high; START as needed | R26 nRESET to +VDD | 220 kΩ per path; RLD 1 MΩ + 1.5 nF | None intended | LDO 1 µF in/out; ADS 100 nF + 1 µF on +3V0; VREFP 10 µF; VCAP1 1 µF; VCAP2 100 nF |
| Off (pack removed) | All down | Off (no VBAT) | Hi-Z | None | 220 kΩ still in series if a pad is touched | None | Caps discharge through loads |
| Reset (SW1 or nRESET) | VBAT and +VDD stay if the pack is in | Unchanged by reset | nRF in reset; AFE PWDN pulled down | R26 | Same 220 kΩ | MCU pins Hi-Z; the 10 kΩ series parts only matter if the AFE is unpowered (Q1 off) | AFE held in reset by R23 |
| Uncooperative MCU, no VBUS | VBAT, +VDD; AFE may be on (R15/Q3) | On | GPIO Hi-Z; AFE PWDN/START low | R26 | 220 kΩ | Idle | AFE stays in reset if PWDN is low |
| Uncooperative MCU, VBUS present | VBAT, VBUS, +VDD; AFE_VIN off | **Off** (Q2) | GPIO may still be 3 V | R26 | 220 kΩ | 10 kΩ series from nRF into unpowered ADS pins (SCLK, MOSI, CS, MISO, DRDY, START, PWDN). Bound ≈ (3.0 − 0.4) / 10 kΩ ≈ 260 µA per line. **This is residual exposure, not isolation.** | AFE rail discharges through the LDO and load |
| Fault (short on +3V0) | LDO current-limit | Q1 may still be on | — | — | 220 kΩ | — | UNVERIFIED thermal |
| VBUS present, MCU cooperative | AFE_VIN off | Off | Firmware puts SCK, MOSI, CS, PWDN and START in high-Z (`elicio_stream.ino`, review r5) | R26 | 220 kΩ; leakage test is an off-body G2 check | Same 10 kΩ bound if firmware fails | Charge path is BQ25100; AFE off |
| Bench (gel, battery, no USB) | Same as powered, no VBUS | On | Acquisition | R26 | J3 is behind the 220 kΩ; same bound as the pads | USB disconnected | Same start-up |

Q1 is P-channel, source = VBAT, drain = AFE_VIN, gate pulled to VBAT (off). Body diode conducts from drain to source, so it does **not** feed VBAT from AFE_VIN. It would conduct from AFE_VIN toward VBAT only if AFE_VIN were higher than VBAT, which this circuit does not create.

Paths that can still reach the electrodes with VBUS present (inhibit credited only if G2 is proved on the built board):

1. SIG1/SIG2/REF copper → 220 kΩ → ADS inputs/RLD → AVSS/AVDD clamps inside the ADS (unpowered) → residual on +3V0/AFE_VIN.
2. SPI/control 10 kΩ into ADS ESD diodes → same.
3. Gel header J3 shares SIG1/SIG2/REF after the 220 kΩ, not before.
4. USB shell / VBUS ESD to GND; GND is common with the electrode returns.

Lead-off: R29 and R30 (10 MΩ IN1x to RLD) are on the schematic as DNP. Firmware lead-off is off when worn (plan §5.5). **Per reference** for “off by default”; the 10 MΩ parts are present as DNP, not stuffed.

ESD actually on this board: the electrode paths have the 220 kΩ series resistors and the ADS1292's own input clamps, nothing else. The only discrete ESD parts are USBLC6-2SC6 (U5) on D+/D− and PESD5V0L1UL (D1) on VBUS, at the USB. There is no BAV199: plan v2 §5.5 names the 220 kΩ, not a diode array. interface.md §6.4 is v1's record and still lists BAV199; `packing-v2.md` reserves the USB parts, not BAV199.

## 4. Gate G4 — first-load net map

Target runs from its own cell, off-body, electrodes disconnected. TC2030-IDC-NL keyed orientation. Raspberry Pi Debug Probe, 3.3 V I/O, ground first. +VDD is 3.0 V only once firmware has written UICR REGOUT0 = 3.0 V: an erased nRF52840 in high-voltage mode starts REG0 at 1.8 V, so on first load the target is at 1.8 V (`firmware-v2.md`). The probe's 3.3 V high into a 1.8 V or 3.0 V target is above or at the nRF52840's VDD + 0.3 V pin limit. Compatibility is **not** inferred; G4 has to verify both directions at the powered target's actual voltage. The probe's documentation page states only "The probe operates at 3.3V nominal I/O voltage." (raspberrypi.com/documentation/microcontrollers/debug-probe.html, re-read 2026-09-17); it gives no target-voltage limit in either direction, so WP17's 0–3.63 V is UNVERIFIED and not used here.

| IDC | TC2030 pin | Net | Probe (proposed) | Rule |
|---|---|---|---|---|
| 1 | 1 | +VDD | VTref sense only | No power feed, no probe lead on this pin |
| 2 | 2 | SWDIO | yellow SD | Module pin 51 |
| 3 | 3 | GND | black | Ground first |
| 4 | 4 | SWDCLK | orange SC | Module pin 53 |
| 5 | 5 | GND | GND | |
| 6 | 6 | nRESET | reset | Module pin 40 (P0.18), shared with SW1 |

SW1 is 4.5 × 4.5 × 1.6 (XKB TS-1187A). Double-press recovery is WP13's.

Q64 — REGOUT0 and first-load. L7-research-v4.md §1 (lane/w5, 2026-09-17) quotes nRF52840 Product Specification v1.7, https://infocenter.nordicsemi.com/pdf/nRF52840_PS_v1.7.pdf:

- Verbatim: "Output voltage from the REG0 regulator stage. The voltage is only applied when the high voltage (HV) operating conditions are supplied to the device." Default: "0: 1.8 V (default)". An erased part is **1.8 V** on first power-up.
- Verbatim, Absolute maximum ratings: "VI/O VDD ≤ 3.6 V -0.3 V VDD + 0.3 V". At VDD = 1.8 V that is **2.1 V**.
- The board offers **VTref on TC2030 pin 1 from the actual +VDD rail**. It does not feed the target from the probe.
- A 3.3 V probe high into an erased 1.8 V pin exceeds 2.1 V by 1.2 V. This board **cannot** take a 3.3 V probe on first load. Kit/level-shifter choice is WP17b. This land does not add a shifter.

## 5. Charger calculations (G1)

Part: **BQ25100YFPR**, 4.20 V variant, YFP DSBGA-6. LCSC C527572 (extended). Datasheet SLUSA09C, https://www.ti.com/lit/ds/symlink/bq25100.pdf, read 2026-09-17 (Rev. C text).

There is **no /CHG pin** on BQ25100. Charge status is read from ISET on CHG_MON (AIN7). The LED is firmware's (LED_EN). **Per the actual pins.**

| Item | Value | From |
|---|---|---|
| KISET typical | 135 A·Ω | Electricals, 5 mA < IOUT < 20 mA and 20 mA < IOUT < 250 mA |
| RISET | 6.80 kΩ (E96) | 135 / 0.020 = 6750 Ω. Review r5: the lane also hung R25 + R28 (10 k + 10 k to GND) on ISET, so RISET was 6.8 k ∥ 20 k = 5.07 kΩ and IOUT about 26.6 mA. R28 now pulls down LED_EN instead; R25 alone feeds the high-impedance ADC |
| IOUT typical | 19.85 mA | 135 / 6800 |
| IOUT at KISET 125 / 145 | 18.38 / 21.32 mA | Same equation |
| Pack max continuous charge | 40 mA on the old DTP sheet | Cell is now 501015 (G1b). 21.32 mA vs DTP 40 mA is not a 501015 proof |
| ISET capacitor | 10 nF to GND | Required for IOUT < 50 mA |
| KTERM typical (10–50 %) | 600 Ω/% | RPRETERM 6 kΩ–30 kΩ |
| RPRETERM | 6.04 kΩ | 10 % × 600 Ω/% = 6.00 kΩ |
| %TERM / ITERM | 10.07 % / 2.00 mA | 6040/600. L7 §4.3 verbatim (SLUSBA8 §9.3.7): "The termination current threshold, ITERM, is user-programmable from 1 mA to 50 mA with an external resistor connected to the PRETERM pin." |
| Precharge | ITERM (≈ 2.00 mA) | L7 §4.3 verbatim (SLUSBA8 §9.3.6): "The pre-charge current, IPRECHG, is also programmed through the PRETERM pin and is equal to the termination current threshold (IPRECHG = ITERM)." Not 2 × ITERM. |
| TS | 10 kΩ to VSS | Pack has no thermistor; TS is never floated. 0–45 °C is Rolf's sheet, not automatic cell protection |
| Fast-charge safety timer | 10 h class | L7 §4.3 verbatim (SLUSBA8 §9.3.1): "A system load can be placed in parallel with the battery, as long as the average system load does not prevent the battery from charging fully within the 10-hour safety timer limit." Sheet typical 38800 s remains the electricals row. |
| Precharge timer | typical 1940 s | Internal; always on |
| Termination floor vs pack | 2.0 mA vs sheet 0.4 mA EOC | Plan G1: this charger's floor is 1 mA; capacity effect unknown until characterised |

LED (review r5): anode from VBUS through R22 1 kΩ, cathode at Q4's drain, Q4's gate on LED_EN (P0.04, module pin 20) with R28 10 kΩ to GND. It can light only with USB present, draws nothing from VBAT or the charger output, and firmware sets it from CHG_MON. The lane's LED hung Q4's gate on ISET (about 1 V, below a 2N7002's worst-case threshold) and took about 2 mA from VBAT, the same order as ITERM, through the charger output.

Parallel system load during charge (Q65), sheets read 2026-09-17:

| Load | Charge-time state | Current |
|---|---|---|
| nRF52840 System OFF | firmware must hold this while VBUS is present | 0.4 µA typ at 3 V (PS v1.11) |
| nRF52840 System ON idle, no radio | not the charge policy | 1.5 µA typ at 3 V |
| nRF CPU/USB idle | if firmware stays awake | milliamps, **above** ITERM |
| TLV71330 Iq | LDO EN=IN but AFE_VIN is off (Q1 off on VBUS), so the LDO is unpowered | 0. L7 §4.4 verbatim (SBVS195 Features): "Low IQ: 50 µA" and "Shutdown current: 0.1 µA (typical)". Those apply only when AFE_VIN is up. Dropout line from the same Features list: "Low dropout: 230 mV at 150 mA". |
| ADS1292 | unpowered (AFE_VIN off) | 0 |
| VBAT 1 MΩ/1 MΩ divider | always on | 4.2 V / 2 MΩ ≈ 2.1 µA |
| Gate leakage Q1–Q4 | nA class | ignore vs 1 mA |
| BQ25100 ITERM floor | typical 10 % of 19.85 mA | 2.0 mA (min 1 mA) |

I_sys in System OFF + divider ≈ 3 µA, margin vs 1 mA ITERM ≈ 1000×. Average I_sys at 3 µA also leaves the 10-hour safety timer (L7 §4.3) intact at ~20 mA charge. If firmware leaves the CPU or USB up, I_sys exceeds ITERM and termination may not occur. **Firmware must hold System OFF (or equivalent) while charging.** The LED draws from VBUS through R22, not from VBAT, so it is not in I_sys.

C3 1 µF on IN, C4 1 µF on OUT: **per typical application**.

## 6. Undervoltage (V_STOP, V_START)

Named constants for WP13:

| Constant | Value | Meaning |
|---|---|---|
| `V_STOP_V` | 3.00 | Inhibit acquisition at or below this pack voltage |
| `V_START_V` | 3.20 | Resume only above this after rail and reference settling |

Derivation:

- ADS1292 AVDD minimum 2.7 V (SBAS502C).
- TLV71330 3.0 V LDO. Dropout 230 mV max at 150 mA (SBVS195). AFE load is about 1–2 mA; dropout at that current is not a table value. **UNVERIFIED interpolation: 50 mV typical, 150 mV used as a conservative bound.**
- Q1 Rds(on) drop at 2 mA is < 1 mV (negligible).
- Battery voltage at which AVDD leaves 2.7 V: 2.7 + 0.15 = **2.85 V** (conservative dropout). Typical: 2.7 + 0.05 = **2.75 V**.
- Pack protection 2.4 V is cell protection only and sits below the AFE valid window.
- Sense: 1 MΩ / 1 MΩ (1 %) to GND, always connected (2.1 µA at 4.2 V). SAADC on P0.02 (AIN0). With 0.6 V reference and gain 1/6, full scale is 3.6 V; a 4.2 V pack reads 2.1 V at the pin. Source 500 kΩ: use the 40 µs acquisition time. LSB at the pack is about 7 mV. Resistor error about 2 % of VBAT (60 mV near 3.0 V). Review r5: the lane's Q5 low-side switch left P0.02 at VBAT through 1 MΩ whenever Q5 was off, above the pin's VDD + 0.3 V limit; Q5 is DNP with its drain on GND.
- 10 s telemetry is **not** the protective cadence. Firmware must sample at the protective rate whenever acquisition is enabled.
- V_STOP = 3.00 V includes sense error, a 50 mV radio/load transient, and margin above 2.85 V.
- V_START = 3.20 V hysteresis so the rail and 2.42 V reference can settle before samples are marked valid.

## 7. LDO

**TLV71330PDBVR**, 3.0 V, SOT-23-5, LCSC C2863702 (extended when last read). EN tied to AFE_VIN (always on when the P-FET is on). Pin 4 NC.

Iq: **50 µA** typical when powered (L7 §4.4, SBVS195 "Low IQ: 50 µA"). Dropout 230 mV at 150 mA (same Features line). AVDD = DVDD = +3V0. **Per ADS1292 typical** (single analog/digital 3.0 V, internal 2.42 V reference, C9 10 µF on VREFP).

## 8. Module, RF keep-out, USB, cell connector

- Module: Raytac MDBT50Q-1MV2, footprint `RF_Module:Raytac_MDBT50Q`, LCSC **C5118826** (C5142646 was 404). HV mode: VDDH = VBAT, 10 µH DCCH → +VDD **per Raytac spec 8.1**. Centre **(10.00, 32.35)** mm in packing (u, s). Body 15.50 × 10.50, length along u. KiCad rotation 90° so that 15.5 mm lies on u, which puts the footprint's antenna end at low u.
- Module sourcing (Q54, review r5): two routes, no design change. (1) JLC global sourcing, if the part is quotable in JLC's library without a request; (2) consignment: Rolf buys the modules at DigiKey or Mouser and ships them to JLC, which adds one parcel and JLC's consignment fee, both to be quoted from pages at G3. The LCSC number is **UNVERIFIED (2026-09-17)**: this lane read C5118826 and says C5142646 was 404; WP17 lists C5142646 as extended/consigned and out of stock. Neither page was re-read by the review. `orders-v2.md` carries the Raytac line.
- RF no-copper: rule area u 2.25–6.05, s 26.15–38.55 (3.8 × 12.4) on every copper layer. U1 rot 90°: 0 pads in that box.
- USB-C: 16-pin HRO TYPE-C-31-M-12 land, LCSC C223907, 5.1 kΩ on CC1 and CC2, USBLC6-2SC6 on D+/D−, PESD5V0L1UL on VBUS (cathode to VBUS). Centre **(10.00, −2.15)** mm. It hangs off the **hook-end end face** (plan v2 §5.4 fallback). Recess 1.0, ligaments 1.5, plug volume 12 × 6.5 × 15. The medial opening is not cut on the order-1 solid.
- Cell: JST-SH SM02B-SRSS-TB placed in the pocket at **(14.40, 9.15)** mm (SparkFun PRT-25270 page, 2026-09-17; that page's “2 mm pitch” text is wrong — SH is 1.00 mm). Silkscreen `J2 BAT+ pin1` is against the connector contacts, not a wire colour. JST-PH S2B-PH-SM4-TB is in `lib/` as the G1b alternate, unplaced. Cell 501015 10.4 × 15.6 × 5.2 plus foam 0.5, centre (7.00, 9.30); the flex neck stays to the right of that pocket. The 501015 harness length 100 ± 3 mm is **NOT_MEASURED** as a solid (`packing-v2.md` §7). **G1b.**

## 9. G4 / firmware GPIO map (MDBT50Q pin → nRF)

WP12b publishes this map as the input for WP13b `firmware/src/board_pins.h`. Pin numbers are from the schematic netlist on this board (Raytac MDBT50Q-1MV2). Do not remap them in firmware.

| Function | Module pin | nRF |
|---|---|---|
| AFE SCLK | 24 | P0.08 |
| AFE MOSI | 22 | P0.06 |
| AFE MISO | 39 | P0.15 |
| AFE CS | 37 | P0.13 |
| AFE DRDY | 41 | P0.17 |
| AFE START | 44 | P0.20 |
| AFE PWDN/RESET | 46 | P0.22 |
| VBUS_DET | 48 | P0.24 |
| CHG_MON | 12 | P0.31 AIN7 |
| VBAT_SENSE | 11 | P0.02 AIN0 |
| BAT_MEAS_EN (Q5 DNP, unused) | 9 | P0.03 |
| LED_EN | 20 | P0.04 |
| nRESET | 40 | P0.18 |
| SWDIO | 51 | SWDIO |
| SWDCLK | 53 | SWDCLK |

## 10. E73-2G4M08S1C alternate (unplaced)

Footprint `elicio:E73-2G4M08S1C` is copied from KiCad `E73-2G4M04S` pad geometry. **UNVERIFIED against the M08S1C drawing.** LCSC C356849 (extended, standard-only, X-ray) from plan v2 header. Do not stuff this footprint on the Raytac board.

Proposed net map if WP11 selects B (same functions; different module pin numbers):

| Function | Raytac MDBT50Q pin | E73-2G4M08S1C pin (Ebyte numbering in the symbol) |
|---|---|---|
| GND | 1, 2, 15, 33, 55 | 5, 21, 24 |
| VDD | 28 | 19 |
| VDDH | 30 | 23 |
| DCCH | 31 | 25 |
| VBUS | 32 | 27 |
| D− / D+ | 34 / 35 | 29 / 31 |
| SWDIO / SWDCLK | 51 / 53 | 37 / 39 |
| nRESET (P0.18) | 40 | 26 |
| P0.08 SCLK | 24 | 16 |
| P0.06 MOSI | 22 | 14 |
| P0.15 MISO | 39 | 28 |
| P0.13 CS | 37 | 33 |
| P0.17 DRDY | 41 | 30 |
| P0.20 START | 44 | 32 |
| P0.22 PWDN | 46 | 34 |
| P0.24 VBUS_DET | 48 | 35 |
| P0.31 CHG_MON | 12 | 10 |
| P0.02 VBAT_SENSE | 11 | 7 |
| P0.03 BAT_MEAS_EN | 9 | 3 |
| P0.04 LED_EN | 20 | not mapped |

A board that uses B is a different placement, not a stuffing option on this land pattern.

## 11. Contacts — interface II (this board)

The whole board is a 2-layer polyimide flex with FR4 stiffeners under the parts. Three flex tabs each end in a ring pad Ø5.0 mm with a Ø2.7 mm hole. The ring is ENIG on both copper layers. The brass standoff bottom face is the contact. An ISO 7380 M2.5×4 screw from outside passes the 1.5 floor and the ring into the standoff's female thread and clamps the ring between floor and standoff. No nut (plan v2 §5.3). Stack: floor 1.5 + ring 0.31 (PI 0.11 + FR4 0.2) + standoff 3.0 = y 4.81 in packing and the shell. Review r6: this Gerber draws no ring FR4 (§12), so as drawn the ring is 0.11, the standoff top lands at 4.61 and the island hangs 0.2 above it; either three FR4 0.2 ring pieces (count 5, over JLC's extra-fee threshold of 4) or a shell 0.2 lower closes it (decision 72 in `tasks/reviews/code-r6.md`). With the 0.31 ring, where the board island rests on the standoff tops; the screw projects 2.5 past the floor and ends 0.81 below the standoff top (`packing-v2.md` §5, Stage B `V2_CONTACT_STACK`). The lane's DIN 439 nut stack (2.50) was v1's.

| Pad | Net | Folded site (packing) | Packing attach | Unfolded ring (this Gerber) |
|---|---|---|---|---|
| P1 | SIG1 | (5.90, 22.00) | (5.90, 29.00) | (−4.75, 22.00) |
| P2 | SIG2 | (10.40, 33.10) | (10.40, 26.10) | (24.75, 33.10) |
| P3 | REF | (8.50, 43.00) | (8.50, 36.80) | (8.50, 43.00) |

SIG1 and SIG2 packing XY sit under the parts island. A flat Gerber cannot place a ring and the module in the same XY. Those two tabs leave the left and right board edges with packing strip length 7.0 mm. REF already leaves the tail; its Gerber matches packing (`along_floor`). WP11b found no in-cavity REF route; WP14 cuts `REF_end_wall_slot`. Assembly folds SIG1 and SIG2 onto the packing sites before the cell goes in. WP14 owns the fold.

Tab strip width 2.5 mm. Outline cap radius 3.0 mm around the Ø5.0 pad (JLC copper-to-edge ≥ 0.3 mm). Strain relief: 4 mm of flex at each tab root has no via, no part, and no stiffener. Neck s 12.0–18.6 is the drop from the board island (underside y 4.81) to the pocket; same rule.

Bend radius: packing R ≥ 1.0 mm. JLC 2-layer static bend ≥ 10 × finished thickness. Finished PI 0.11 mm → 1.1 mm. This file states **R = 1.5 mm**. Dynamic bend is not the use. No vias or pads in the bend windows.

Each ring has a 7.0 × 7.0 mm other-net keep-out (1.0 mm beyond the Ø5.0 land). Pads themselves are allowed.

There are no separate M2.5 boss holes. The ring holes are the fasteners. Review r6: the shell still carries two printed bosses with pilots at (14.85, 21.50) and (14.85, 28.10), under J3 and under U1; nothing on this board can screw into them, and P3 (s 43.00) is past the island's end (s 37.60), so the island rests on two standoffs. Retention of the island is decision 73.

Fold (review r6): SIG1 and SIG2 leave the island edges on 7.0 mm strips and fold 180° at R 1.5 to reach the packing sites. A 180° fold at R 1.5 stands about 1.6 mm outside the edge, and the island edge is 0.75 mm from the cavity wall; the flat length from the edge to the ring centre is about 8.5, not 7.0. P1's packing attach (5.90, 29.00) is inside the antenna keep-out. Decision 74.

G7 joint inputs (this board):

| Item | Number | Source |
|---|---|---|
| Ring copper | Ø5.0 mm, both layers, tied | footprint `elicio:RING_PAD_D5_H2.7` |
| Coverlay opening | ≥ Ø5.2 mm (0.1 mm expansion one-sided) | JLC FPC coverlay, read 2026-09-17 |
| ENIG | 1 u" or 2 u" (order tick) | JLC FPC page, read 2026-09-17; HASL is not on FPC |
| Tab bend | R = 1.5 mm static | 10 × 0.11 mm = 1.1 mm min; packing R ≥ 1.0 |
| Strain relief | 4 mm tab root: no via, no part, no stiffener | this drawing, Dwgs.User |
| Datum ring hole → outline | cap radius 3.0 mm around the hole; copper-to-edge ≥ 0.3 | outline in `elicio-v2.kicad_pcb` |
| Printed seat and well (shell) | ring seat Ø6.4 (Ø6.0 outline + 0.10 + 0.3 print); hex well AF 5.30 (5.00 A/F max + 0.3), locks below 5.77 across corners; collar AF 8.4, 2.0 tall | `shell-v2.md` §3, `V2_STANDOFF`, `V2_RING_seat` (review r6) |
| Capture | ISO 7380 M2.5×4 from outside into standoff female thread; ring between floor and standoff; **no nut** (Q58) | packing-v2.md §5 |
| STEP | `release/elicio-v2.step` models the tabs **flat**. Fold of SIG1/SIG2 onto packing XY is WP14's. | release job |

### 11a. Rejected candidate — interface I (8 × 8 pads)

WP11 at `43a982a`, `docs/fab/packing-v2.md` §2 and §3: interface I (board on standoff tops, 8 × 8 ENIG pad per site) **closes in 0 of 720 runs** at the anatomical sites (review r5 matrix). Neither cell (DTP packed 3.7 mm, 501015 packed 5.7 mm with foam 0.5) fits under a 3.0 or 3.5 mm standoff with positive nominal clearance and no load after the 0.5 mm boss drop, and in every run the REF site (s 43) is past the rigid board's end and SIG1's 8 × 8 pad overhangs the board edge. Plan v2 §5.3 makes II the fallback when I fails.

The first WP12 pass placed three 8 × 8 mm B.Cu pads on a provisional 17 × 33 mm 4-layer board: P1 (8.5, 6.0), P2 (8.5, 16.0), P3 (8.5, 26.0), each with a 10 × 10 mm keep-out. P3 overlapped the RF keep-out. Footprint `elicio:PAD_8x8_ENIG` remains in `hardware/board/lib/elicio.pretty` and the schematic still draws `elicio:PAD_8x8` (one passive pin per net). Those lands are **not** on this PCB. Do not stuff them. Do not order the 4-layer rigid outline.

## 12. Stackup and DRC rules (JLC FPC)

Assembler candidate: JLCPCB 2-layer FPC, ENIG. Nothing ordered. Nothing quoted. No vendor contact.

Source: https://jlcpcb.com/capabilities/flex-pcb-capabilities read 2026-09-17. Same numbers on https://jlcpcb.com/pcb-fabrication/flexible-pcb.

| Rule | Value | Source (read 2026-09-17) |
|---|---|---|
| Layers | F.Cu, B.Cu | 2-layer FPC. Rigid-flex is not supported on that page |
| Finished PI | 0.11 mm (2-layer, 25 µm dielectric options 0.11 / 0.12 / 0.2) | WP11 assumed 0.11 |
| Finish | ENIG 1 u" / 2 u" | FPC page; HASL is not on FPC |
| Min track / space | 3/3 mil (0.076 mm) at 12 µm copper; 3.5/3.5 mil at 18 µm; **4/4 mil (0.10 mm) at 1 oz / 35 µm** | Encoded 0.10 / 0.10 as the 1 oz regular limit |
| Coverlay opening | expansion 0.1 mm one-sided; opening-to-trace ≥ 0.15 mm | Encoded pad-to-mask 0.1 mm |
| Coverlay colour | Yellow recommended | Yellow / black / white / transparent |
| Via (regular 2-layer) | 0.30 mm hole / 0.70 mm pad | JLC 0.30/0.55; this board uses 0.70 so annular ≥ 0.18 |
| PTH annular ring | ≥ 0.25 mm recommended, 0.18 mm absolute | Ring pad (5.0 − 2.7) / 2 = 1.15 mm |
| Copper to outline | ≥ 0.30 mm (laser) | Encoded as DRC min copper-edge clearance |
| Outline tolerance | ±0.10 mm | ±0.05 mm on request; not requested |
| Bend | 2-layer ≥ 10 × thickness (static) | 1.1 mm at 0.11; this board uses 1.5 mm |
| Passives | 0402 minimum | Plan |
| Stiffener at parts | FR4 0.4 mm on Eco1.User (packing: 0.11 + 0.4 = 0.51, review r5) | JLC FR4 list is 0.1 / 0.2 / 0.4, no 0.3 |
| Stiffener at tabs | none drawn (Q58 clamp; Q60 merge). Packing, the shell and §11's stack take FR4 0.2 at the rings; decision 72 | JLC FR4 0.2 mm exists; Eco2.User unused |

PI stiffener catalogue: 0.1 / 0.15 / 0.20 / 0.225 / 0.25 mm. Stainless 0.1 / 0.2 / 0.3 mm. FR4 0.1 / 0.2 / 0.4 / 0.6 / 0.8 / 1.0 / 1.2 / 1.6 mm. WP11's 0.3 mm FR4 is **not** on that list; review r5 took 0.4 and moved the packing numbers with it. No request was sent.

Stiffener drawings: Eco1.User = two FR4 0.4 pieces (parts island + USB/pocket). Eco2.User is unused (no tab FR4: Q58 clamp). Cmts.User = neck bend window. Count = **2** (under JLC's extra-fee threshold of 4). JLC's "other EDA" note: put stiffener outlines on their own layer and set thickness by hand at order. Gerbers include those layers. Nothing uploaded.

Encoded in the board design settings and in `elicio-v2.kicad_pro`.

## 13. BOM (placed, in-BOM, not DNP)

Release job writes `hardware/board/release/bom.csv` (gitignored). LCSC numbers were re-read on JLC/LCSC pages on 2026-09-17 after L7-research-v4.md §4.1 (`git show lane/w5:docs/fab/L7-research-v4.md`). Take L7 only where the page still shows that MPN. Stock and unit price on JLC partdetail pages were often not displayed (tier label only). LCSC.com did show some qty-1 prices.

U1: **C5118826** is MDBT50Q-1MV2 Extended, X-ray (https://jlcpcb.com/partdetail/C5118826, 2026-09-17). **C5142646** is a GOOSVN screw terminal GS034-3.81-02P (https://jlcpcb.com/partdetail/C5142646). L7 §4.1's "C5142646 is LCSC catalog code" for the Raytac module does **not** match the page. This board uses C5118826.

L7 §4.1 SKUs that **fail** today's pages (not used):

| L7 SKU | L7 claim | Page 2026-09-17 |
|---|---|---|
| C134015 | ADS1292RIRSMT | SN65C1168EPW RS-485 TSSOP-16 (JLC and LCSC) |
| C2841443 | ADS1292IRSMR | CPDH3V3UP-TP ESD SOD-523 |
| C132291 | TLV71330PDBVR | FUSB302BMPX USB-C controller |
| C18001 | 220 kΩ 0402 Basic | 240 kΩ 1206 |
| C25768 | 220 kΩ 0402 Basic | 22 kΩ 0402 Basic |
| C25744 | 100 kΩ 0402 Basic | 10 kΩ 0402 Basic (used here for the 10 kΩ lines) |
| C15609 | 1 MΩ 0402 Basic | empty JLC partdetail |
| C15672 | 1 kΩ 0402 Basic | empty JLC partdetail |
| C89288 "invalid" | — | ADS1292IRSMT VQFN-32, LCSC 70 in stock, $6.50 qty 1 |
| C2863702 "invalid" | — | TLV71330PDBVR SOT-23-5, LCSC 190 in stock |

U2 stays **C89288** ADS1292IRSMT non-R (PWDN on pin 15). The R-device is a different pinout.

J2: L7 and the page agree. C160404 is SM04B-SRSS-TB **4P**. C160402 is SM02B-SRSS-TB **2P**. This board now uses C160402.

Blanked / corrected lines from the same day's pages:

| Ref | Value | LCSC | Tier (page) | Note |
|---|---|---|---|---|
| C2 | 10 nF 0402 | C1524 | Extended | L7 §4.1. Page: 10 nF X7R 0402. Not Basic. |
| C6, C8, C9 | 10 µF 0603 | C19702 | — | Q68 10 µF; stay 0603 |
| C7, C15 | 100 nF 0603 | C14663 | — | Q68 0.1 µF at the ADS pins. L7's C1525 is the 0402 100 nF used on C11/C12. |
| C11, C12 | 100 nF 0402 | C1525 | Basic | L7 §4.1. Page: CL05B104KO5NNNC 100 nF. |
| R1–R3 | 220 kΩ 1% 0402 | C881401 | Extended | Page: 220 kΩ 0402. L7 C18001/C25768 fail. |
| R4, R17, R20, R21 | 1 MΩ 0402 | C26083 | Basic | Page: 0402WGF1004TCE 1 MΩ. L7 C15609 empty. |
| R5–R8, R13, R25–R28 | 10 kΩ 0402 | C25744 | Basic | Page: 10 kΩ. Old C25792 is 47 kΩ. |
| R14–R16, R23, R24 | 100 kΩ 0402 | C25741 | Basic | Page: 100 kΩ. L7 C25744 is 10 kΩ. |
| R18 | 47 kΩ 0402 | C25792 | Basic | VBUS_DET. Old C25780 is 348 kΩ. |
| R19 | 27 kΩ 0402 | C25771 | Extended | Page: 27 kΩ. |
| R22 | 1 kΩ 0402 | C11702 | Basic | Page: 1 kΩ. L7 C15672 empty. |
| R11 | 6.80 kΩ 0402 | C25917 | Extended | Page: 6.8 kΩ 0402. Old C25848 is 8.2 kΩ 0201. |
| R12 | 6.04 kΩ 0402 | C966759 | Extended | Page: 6.04 kΩ 0402. Old C25841 is 2.2 kΩ 0201. |

| Ref | MPN / value | LCSC | Tier (when read) | Notes |
|---|---|---|---|---|
| U1 | MDBT50Q-1MV2 | C5118826 | Extended | Not C5142646 |
| U2 | ADS1292IRSMT | C89288 | Extended | Non-R, VQFN-32. L7 replacements fail the page. |
| U3 | BQ25100YFPR | C527572 | Extended | |
| U4 | TLV71330PDBVR | C2863702 | Extended | L7 C132291 is FUSB302. Keep C2863702. |
| U5 | USBLC6-2SC6 | C7519 | — | USB ESD |
| Q1 | AO3401A | C15127 | — | P-FET |
| Q2–Q4 | 2N7002 | C2128 | Basic typical | Inhibit, LED (Q5 DNP) |
| D1 | PESD5V0L1UL | C24109 | — | VBUS ESD |
| D2 | 0402 LED | C72043 | — | Firmware LED on LED_EN |
| J1 | TYPE-C-31-M-14 | C223907 | Extended | 16P USB2 |
| J2 | SM02B-SRSS-TB | C160402 | Extended | 2P SH. Was C160404 4P. |
| J3 | 1×03 RA 2.54 | C49257 | — | Bench |
| SW1 | TS-1187A | C318884 | — | 4.5 × 4.5 × 1.6 |
| L1 | 10 µH 0603 | C1045 | — | nRF DCCH |
| R9, R10 | 5.1 kΩ | C25905 | Basic | CC. Page: 5.1 kΩ 0402. |

Displayed JLC stock and unit price: **UNVERIFIED** on partdetail widgets. LCSC.com qty-1 seen today: U2 C89288 $6.50 (70); U4 C2863702 from $0.23 (190). Not in BOM: J4 TC2030-NL, P1–P3 ring pads, R29–R30 DNP 10 MΩ (LCSC C26082 for the 10 MΩ land, not stuffed), Q5 DNP, power flags.

## 14. Reference-circuit check (each choice)

| Choice | Verdict |
|---|---|
| ADS1292 3.0 V AVDD=DVDD, internal ref, 10 µF VREFP, 1 µF VCAP1, 100 nF VCAP2 | Per typical (SBAS502C) |
| Supply bypass 10 µF + 0.1 µF on AVDD and on DVDD (C6+C7, C8+C15, 0603) | L7 §4.2 verbatim (SBAS502C §11.1): "Each supply pin (AVDD and DVDD) should be bypassed using both a 10-µF and a 0.1-µF ceramic capacitor." And: "To achieve the best performance, it is recommended that the capacitors be placed as close to the device as possible." Caps on B.Cu under the ADS. |
| RLD 1 MΩ + 1.5 nF | Per typical |
| 220 kΩ on SIG1, SIG2, REF | Per plan v2 §5.5, not a TI typical value |
| Unused IN2 tied to +3V0 | Per SBAS502C ("connect unused analog inputs to AVDD"); firmware powers CH2 down with its input shorted (CH2SET 0x81) |
| CLKSEL to +3V0 (internal clock), CLK NC | Per typical for internal clock |
| PWDN/START pulldowns | Deviates toward fail-safe reset; TI typical often leaves them to the host |
| 10 kΩ SPI series | Deviates: current limit for an unpowered AFE, not a TI typical |
| BQ25100 6.80 kΩ ISET, 6.04 kΩ PRETERM, 10 kΩ TS, 10 nF ISET, 1 µF IN/OUT | Per equations / typical |
| No /CHG LED from a CHG pin | Per BQ25100 pinout; the LED is a firmware output from VBUS (review r5) |
| TLV713 EN to IN | Per typical “always on” |
| nRF HV inductor 10 µH | Per Raytac 8.1 |
| USB CC 5.1 kΩ, 16P, ESD | Per USB-C USB2 device |
| P-FET inhibit | Plan R7/G2, not a TI typical |
| Interface II ring pads Ø5.0 / hole Ø2.7, ENIG, clamped under standoff | Plan §5.3 fallback after WP11 I = 0/720 |
| 8 × 8 mm ENIG pads | Rejected; see §11a |

## 15. What DRC says

Command: `kicad-cli pcb drc --format json` via `scripts/board/release.py`.

WP12b placed from packing §5 and assigned every schematic net. Tracks exist. Freerouting v2.1.0 hung in this environment; a B.Cu bus fallback connects leftover nets. That copper still shorts and violates clearance. **Order release is not green.**

Run 2026-09-17 (this lane, after the packing place; `release.py --routed` to `/tmp/wp12b-release`):

| Item | Result |
|---|---|
| DRC errors | 1290 (clearance, shorting, mask bridge, hole, tracks crossing, copper-to-edge) |
| DRC warnings | 25 |
| Unconnected items | 31 (GND pads vs zone fill, including C8 under the ADS) |
| Pads without a net | 0 |
| pcb_tracks | 465 |
| Routing | tracks > 0; `"routed": true` only when `--routed` is passed |

`release.py --routed` still fails closed on DRC errors and unconnected items (Q62). The non-`--routed` job still exits 0 if ERC is 0 and outputs exist.

## 16. ERC

`kicad-cli sch erc --format json`: **0 errors, 0 warnings** (review r5, still true after Q68 C15).

## 17. Release job

`scripts/board/release.py` runs ERC, DRC, JLC-column BOM, JLC CPL (SMD only), gerbers+drill, STEP, and `release/summary.json`. Non-zero exit on any ERC error or any missing output; with `--routed`, also on DRC errors, unconnected items, pads without a net, or no tracks.

`tests/test_board_release.py` asserts ERC 0, BOM rows = placed parts, `"routed": false` without the flag, `--routed` still refused on this copper, pcb_tracks > 0, and named SMT centres within 0.1 mm of packing §5. If `kicad-cli` is missing the tests fail with `brew install --cask kicad`.

## 18. Assembler consequences and C7 (quote only)

JLC flex assembly uses a fixture. Page https://jlcpcb.com/help/article/pcb-assembly-price read 2026-09-17, last updated 2026-09-09:

| Item | Number on that page |
|---|---|
| Fixture (Flexible PCB) unit | $24.63 / fixture |
| 1–29 pcs | 2 fixtures → $49.25 |
| 30–99 pcs | 3 fixtures → $73.88 |
| 100–199 pcs | 5 fixtures → $123.13 |

No quote was requested. Ledger input only.

FPC assembly acceptance, quoted, no request:

- https://jlcpcb.com/help/article/terms-and-conditions-of-jlcpcb-assembly-service (read 2026-09-17, last updated 2026-09-09): footprints and gaps IPC-7351B medium or low density; component body to board edge ≥ 2.5 mm; tooling holes, edge rails and fiducials required for assembly; high density is not supported; no power-on test.
- https://jlcpcb.com/blog/fpc-panelization-design-standards (read 2026-09-17): FPC+SMT minimum panel 70 × 70 mm; below that, panelise or add process edges. FPC does not use V-cut or mouse bites; bridge tabs 0.7–1.0 mm.
- https://jlcpcb.com/blog/design-guidelines-flex-pcb-panels and https://jlcpcb.com/blog/fast-turn-flex-pcb (read 2026-09-17): 5 mm process edges; 2 mm board spacing (3 mm with metal stiffeners); SMT fiducials 1 mm at 3.85 mm from the panel edge; tooling holes 2 mm; local fiducial beside each unit; carrier / SMT pallet for flex.

https://jlcpcb.com/help/article/fpc-extra-charges (re-read 2026-09-17, last updated 2026-09-09), same wording as L7 §3.1:

- Prototype: "For prototype orders, when there are 4 or more stiffeners on the board, an extra fee is required."
- Small batch / mass: "when there are 4pcs or more stiffeners on the board, or the total stiffener area on both sides is no less than 90% of the board area, extra cost is required."
- Stacked: "When you need to stack up stiffeners in the same location, there will be an additional cost of $8.14+$24.44/m² for every extra stiffener."

This drawing has **two** FR4 0.4 pieces (Eco1.User: island + USB/pocket). No tab FR4 (Q58 clamp). Count = 2, under the extra-stiffener rule. Review r6: packing and the shell assume FR4 0.2 at the three rings; drawing them makes the count 5, which is over the threshold (decision 72).

L7 §3.1 also lists FR4 **0.3 mm** on the stiffener catalogue. This land still uses 0.4 mm (review r5 / packing). A 0.3 mm change is WP11/WP14.

Q67 Raytac routes. L7 §3.3–§3.4 quotes (pages named there, 2026-09-17). The same JLC help URLs returned only the chat widget when this lane fetched them today, so live page text is **UNVERIFIED here**; the sentences below are L7's quotes:

- Consignment overseas handling: "2% of the declared value, with a minimum charge of USD 10 per shipment".
- Pickup: "Fewer than 20 component types: USD 30 service fee. More than 20 component types: USD 30 service fee + an additional USD 1 per extra component type."
- Storage: "There is no inventory cost for consigned parts."
- Global sourcing estimate: "This estimated price is for reference only and is determined by the JLCPCB purchasing department based on data evaluation." "Because component prices can be volatile, estimated prices do not update in real-time."
- Extended feeder: "JLCPCB charges a $3 fee per extended component type".

LCSC C5118826 is the part this BOM names. Nothing was ordered.

Packing SW1 centre is now (10.10, 24.20). The old 0.3 mm-to-outline conflict was the pre-r5 site (4.80, 21.15). The new site is inward of the left edge.

## 19. Needs a decision

1. **G1b** — SparkFun's pack page says JST-SH; a linked drawing has said JST-PHR. SH is placed; PH is in the library. Cell is **501015** with a 100 ± 3 mm harness (**NOT_MEASURED**).
2. **SIG1/SIG2 unfold** — Gerber rings are off the island; packing XY is the folded site. WP14 must fold them before the cell is fitted.
3. **Order route** — `--routed` is still fail-closed: bus copper shorts and GND zone islands remain. A human or a working autorouter must finish the 2-layer flex before G3.
4. **3.3 V probe vs 1.8 V first-load** — Q64: this board cannot set REGOUT0 through a 3.3 V probe. WP17b kit.
5. **E73 land** — pad geometry copied from E73-2G4M04S; confirm M08S1C drawing before any B build.
6. **YFP0006 land** — copied from KiCad DSBGA-6 0.40 mm; confirm TI 4223410/A before order.
7. **BQ25100YFPR stock** — extended; G3 is not this package.
8. **Protective monitor cadence** — V_STOP is a firmware constant; the divider is always connected; firmware must sample at the protective cadence.
9. **Displayed LCSC stock/price** — JLC partdetail widgets often hide qty. G3 re-reads. L7 §4.1 SKUs that fail today's pages stay unused (C134015, C2841443, C132291, C18001, C25768).
10. **JLC assembly edge 2.5 mm** — several packing centres (U3, tab 220 kΩ) sit closer than 2.5 mm to an outline. WP14/panel.
