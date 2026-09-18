# Board v2 — schematic, G2/G4 records, release job

Status: design record for WP12. Not for order, quote or upload.
Date: 2026-09-17.
KiCad: 10.0.6 (`kicad-cli`).
Outline: provisional **17 × 33 mm**. `git show lane/w1:docs/fab/packing-v2.md` does not exist on this worktree, so USB-C sits at the y = 0 board edge and the three 8 × 8 mm pads sit on B.Cu at the positions below. Final outline and pad sites are WP11/G5.

Project: `hardware/board/elicio-v2.kicad_pro`.

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
                 +--> 1M/1M divider (Q5 enable) --> VBAT_SENSE (P0.02 AIN0)

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
| CHG_MON | ISET divider onto P0.31 AIN7 |
| VBUS_DET | 47 kΩ / 27 kΩ onto P0.24 |
| VBAT_SENSE, BAT_MEAS_EN, BAT_MEAS_LO | 1 MΩ / 1 MΩ divider, Q5 bottom switch |
| SWDIO, SWDCLK, nRESET | First-load and recovery |

ADS1292 pin 15 is PWDN (power-down / reset). There is no separate RESET pin on the non-R device. AFE_RESET is that pin. **Deviates from a two-GPIO RESET+PWDN reading: the silicon has one pin.**

## 3. Gate G2 — electrode boundary states

R7 (plan v2): no galvanic isolation between USB-connected circuitry and the electrode paths. Skin-connected use is battery-only. The P-FET is an inhibit of the front-end supply when VBUS is present, not isolation.

Default hardware with an uncooperative MCU: R14 holds Q1 gate at VBAT (P-FET **off**). Q2 turns on when VBUS is present and holds AFE_EN_HW low, so Q3 cannot pull the P-FET on. R23/R24 hold ADS PWDN and START low.

| State | Rails | Gate Q1 | SPI / control | Pull-ups | Protection | Back-power | Discharge / start-up |
|---|---|---|---|---|---|---|---|
| Powered, battery, no VBUS, MCU cooperative | VBAT, +VDD, AFE_VIN, +3V0 | On (Q3 on via R15) | Firmware drives SPI; PWDN high; START as needed | R26 nRESET to +VDD | 220 kΩ per path; RLD 1 MΩ + 1.5 nF | None intended | LDO 1 µF in/out; ADS 100 nF + 1 µF on +3V0; VREFP 10 µF; VCAP1 1 µF; VCAP2 100 nF |
| Off (pack removed) | All down | Off (no VBAT) | Hi-Z | None | 220 kΩ still in series if a pad is touched | None | Caps discharge through loads |
| Reset (SW1 or nRESET) | VBAT and +VDD stay if the pack is in | Unchanged by reset | nRF in reset; AFE PWDN pulled down | R26 | Same 220 kΩ | MCU pins Hi-Z; 10 kΩ series into an unpowered AFE if Q1 is on | AFE held in reset by R23 |
| Uncooperative MCU, no VBUS | VBAT, +VDD; AFE may be on (R15/Q3) | On | GPIO Hi-Z; AFE PWDN/START low | R26 | 220 kΩ | Idle | AFE stays in reset if PWDN is low |
| Uncooperative MCU, VBUS present | VBAT, VBUS, +VDD; AFE_VIN off | **Off** (Q2) | GPIO may still be 3 V | R26 | 220 kΩ | 10 kΩ series from nRF into unpowered ADS pins (SCLK, MOSI, CS, MISO, DRDY, START, PWDN). Bound ≈ (3.0 − 0.4) / 10 kΩ ≈ 260 µA per line. **This is residual exposure, not isolation.** | AFE rail discharges through the LDO and load |
| Fault (short on +3V0) | LDO current-limit | Q1 may still be on | — | — | 220 kΩ | — | UNVERIFIED thermal |
| VBUS present, MCU cooperative | AFE_VIN off | Off | Firmware must Hi-Z or drive low the AFE GPIOs | R26 | 220 kΩ; leakage test is an off-body G2 check | Same 10 kΩ bound | Charge path is BQ25100; AFE off |
| Bench (gel, battery, no USB) | Same as powered, no VBUS | On | Acquisition | R26 | J3 is behind the 220 kΩ; same bound as the pads | USB disconnected | Same start-up |

Q1 is P-channel, source = VBAT, drain = AFE_VIN, gate pulled to VBAT (off). Body diode conducts from drain to source, so it does **not** feed VBAT from AFE_VIN. It would conduct from AFE_VIN toward VBAT only if AFE_VIN were higher than VBAT, which this circuit does not create.

Paths that can still reach the electrodes with VBUS present (inhibit credited only if G2 is proved on the built board):

1. SIG1/SIG2/REF copper → 220 kΩ → ADS inputs/RLD → AVSS/AVDD clamps inside the ADS (unpowered) → residual on +3V0/AFE_VIN.
2. SPI/control 10 kΩ into ADS ESD diodes → same.
3. Gel header J3 shares SIG1/SIG2/REF after the 220 kΩ, not before.
4. USB shell / VBUS ESD to GND; GND is common with the electrode returns.

Lead-off: R29 and R30 (10 MΩ IN1x to RLD) are on the schematic as DNP. Firmware lead-off is off when worn (plan §5.5). **Per reference** for “off by default”; the 10 MΩ parts are present as DNP, not stuffed.

v1 BAV199 clamps are **not** on this board. Plan v2 §5.5 names 220 kΩ, not the diode array. Recorded as a deviation from interface.md §6.4 (v1 packing).

## 4. Gate G4 — first-load net map

Target runs from its own cell, off-body, electrodes disconnected. TC2030-IDC-NL keyed orientation. Raspberry Pi Debug Probe, 3.3 V I/O, ground first. +VDD is about 3.0 V (nRF REG0). Compatibility of the probe at 3.0 V target is **not** inferred; G4 still has to verify both directions at the powered target.

| IDC | TC2030 pin | Net | Probe (proposed) | Rule |
|---|---|---|---|---|
| 1 | 1 | +VDD | VTref sense only | No power feed, no probe lead on this pin |
| 2 | 2 | SWDIO | yellow SD | Module pin 51 |
| 3 | 3 | GND | black | Ground first |
| 4 | 4 | SWDCLK | orange SC | Module pin 53 |
| 5 | 5 | GND | GND | |
| 6 | 6 | nRESET | reset | Module pin 40 (P0.18), shared with SW1 |

SW1 is 4.5 × 4.5 × 1.6 (XKB TS-1187A). Double-press recovery is WP13's.

## 5. Charger calculations (G1)

Part: **BQ25100YFPR**, 4.20 V variant, YFP DSBGA-6. LCSC C527572 (extended). Datasheet SLUSA09C, https://www.ti.com/lit/ds/symlink/bq25100.pdf, read 2026-09-17 (Rev. C text).

There is **no /CHG pin** on BQ25100. Charge status is from ISET (and the LED/Q4 circuit). **Per the actual pins.**

| Item | Value | From |
|---|---|---|
| KISET typical | 135 A·Ω | Electricals, 5 mA < IOUT < 20 mA and 20 mA < IOUT < 250 mA |
| RISET | 6.80 kΩ (E96) | 135 / 0.020 = 6750 Ω |
| IOUT typical | 19.85 mA | 135 / 6800 |
| IOUT at KISET 125 / 145 | 18.38 / 21.32 mA | Same equation |
| Pack max continuous charge | 40 mA | DTP301120 sheet; 21.32 < 40 |
| ISET capacitor | 10 nF to GND | Required for IOUT < 50 mA |
| KTERM typical (10–50 %) | 600 Ω/% | RPRETERM 6 kΩ–30 kΩ |
| RPRETERM | 6.04 kΩ | 10 % × 600 Ω/% = 6.00 kΩ |
| %TERM / ITERM | 10.07 % / 2.00 mA | 6040/600; min ITERM is 1 mA |
| Precharge | 2 × termination ≈ 4.0 mA | PRETERM programs both |
| TS | 10 kΩ to VSS | Pack has no thermistor; TS is never floated. 0–45 °C is Rolf's sheet, not automatic cell protection |
| Fast-charge safety timer | typical 38800 s (about 10.8 h) | Internal; always on |
| Precharge timer | typical 1940 s | Internal; always on |
| Termination floor vs pack | 2.0 mA vs sheet 0.4 mA EOC | Plan G1: this charger's floor is 1 mA; capacity effect unknown until characterised |

LED: ISET drives Q4 (2N7002). LED anode to VBAT through R22 1 kΩ, cathode at Q4 drain. The LED is on only if V_ISET exceeds Q4 Vgs(th) (0.8–2.5 V, UNVERIFIED on this ISET node, which is about 1 V in TI's examples). Treat the LED as an informal indicator. Firmware reads CHG_MON (ISET divided 10 kΩ / 10 kΩ onto P0.31 AIN7).

Parallel system load during charge: nRF + REG0 from VBAT while VBUS is present. Current is UNVERIFIED (order-of-magnitude 1–15 mA depending on radio and USB). If I_sys > ITERM, termination may not occur. The datasheet requires the average system load not to prevent a full charge inside the 10 h timer. **Needs a decision** if firmware must sleep the radio while charging.

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
- Sense: 1 MΩ / 1 MΩ (1 %), Q5 bottom enable on P0.03. SAADC on P0.02 (AIN0). With 0.6 V reference and gain 1/6, full scale is 3.6 V; a 4.2 V pack reads 2.1 V at the pin. LSB at the pack is about 7 mV. Resistor error about 2 % of VBAT (60 mV near 3.0 V).
- 10 s telemetry is **not** the protective cadence. Firmware must sample with Q5 on at the protective rate whenever acquisition is enabled.
- V_STOP = 3.00 V includes sense error, a 50 mV radio/load transient, and margin above 2.85 V.
- V_START = 3.20 V hysteresis so the rail and 2.42 V reference can settle before samples are marked valid.

## 7. LDO

**TLV71330PDBVR**, 3.0 V, SOT-23-5, LCSC C2863702 (extended when last read). EN tied to AFE_VIN (always on when the P-FET is on). Pin 4 NC.

Iq: tens of µA class (SBVS195). Dropout as in §6. AVDD = DVDD = +3V0. **Per ADS1292 typical** (single analog/digital 3.0 V, internal 2.42 V reference, C9 10 µF on VREFP).

## 8. Module, RF keep-out, USB, cell connector

- Module: Raytac MDBT50Q-1MV2, footprint `RF_Module:Raytac_MDBT50Q`, LCSC **C5118826** (C5142646 was 404). HV mode: VDDH = VBAT, 10 µH DCCH → +VDD **per Raytac spec 8.1**.
- RF no-copper: rule area 17.0 × 3.8 mm at y = 29.2–33.0 on every copper layer (interface.md §6.3: 12.4 × 3.8, widened to the 17 mm board). Extra top-layer feed notch is **not** cut; WP14/layout.
- USB-C: 16-pin HRO TYPE-C-31-M-12 land, LCSC C223907, 5.1 kΩ on CC1 and CC2, USBLC6-2SC6 on D+/D−, PESD5V0L1UL on VBUS (cathode to VBUS). Recessed medial placement is WP14; this file places it at the provisional y = 0 edge.
- Cell: JST-SH SM02B-SRSS-TB placed (SparkFun PRT-25270 page, 2026-09-17; that page's “2 mm pitch” text is wrong — SH is 1.00 mm). Silkscreen `J2 BAT+ pin1` is against the connector contacts, not a wire colour. JST-PH S2B-PH-SM4-TB is in `lib/` as the G1b alternate, unplaced.

## 9. G4 / firmware GPIO map (MDBT50Q pin → nRF)

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
| BAT_MEAS_EN | 9 | P0.03 |
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

A board that uses B is a different placement, not a stuffing option on this land pattern.

## 11. Contacts and mounting

Three 8 × 8 mm ENIG pads on B.Cu, nets SIG1, SIG2, REF. Each pad has a 10 × 10 mm rule area (1.0 mm copper keep-out beyond the pad, pads themselves allowed). Provisional centres on the 17 × 33 mm outline: P1 (8.5, 6.0), P2 (8.5, 16.0), P3 (8.5, 26.0) mm. P3 overlaps the RF keep-out. **Final positions are WP11/G5.** Interface.md candidate 1 × 1 mm sites are not these 8 × 8 mm pads.

Two M2.5 NPTH holes at (1.8, 1.8) and (15.2, 31.2) mm for printed bosses.

## 12. Stackup and DRC rules

Assembler candidate: JLCPCB, 4-layer FR4, 1.0 mm, ENIG. Nothing ordered.

| Rule | Value | Source (read 2026-09-17) |
|---|---|---|
| Layers | F.Cu, In1.Cu, In2.Cu, B.Cu | Plan §5.2 |
| Thickness | 1.0 mm | Plan §5.2 |
| Finish | ENIG | Plan §5.2; https://jlcpcb.com/capabilities/ |
| Min track / clearance | 0.09 / 0.09 mm | Multilayer 1 oz, same URL |
| Preferred via | 0.20 mm hole / 0.45 mm pad | Preferred min hole 0.20 mm; via pad ≥ hole + 0.15 mm |
| Copper to edge | 0.25 mm | Encoded as DRC min copper-edge clearance |
| Passives | 0402 minimum | Plan |

The impedance page https://jlcpcb.com/impedance lists 1.0 mm as a 4-layer thickness. The named tables on that page dump as **JLC04161H** (1.6 mm) in the static HTML. Core thickness for 1.0 mm is **UNVERIFIED** on the static page. Outer 1 oz / inner 0.5 oz and 7628 prepreg ≈ 0.210 mm are the usual JLC 4-layer construction.

Encoded in the board design settings and in `elicio-v2.kicad_pro`.

## 13. BOM (placed, in-BOM, not DNP)

Release job writes `hardware/board/release/bom.csv` (gitignored). 59 rows = 59 placed parts. LCSC numbers for ICs and connectors were read on JLCPCB/LCSC pages on 2026-09-17 in this lane. 0402 passives use catalogue-typical basic/extended line codes and are **UNVERIFIED** as live stock on the close-out of this package.

| Ref | MPN / value | LCSC | Tier (when read) | Notes |
|---|---|---|---|---|
| U1 | MDBT50Q-1MV2 | C5118826 | — | Consignment candidate; LCSC page existed |
| U2 | ADS1292IRSMT | C89288 | — | Non-R, VQFN-32. L5's C134015/C2841443 were wrong parts |
| U3 | BQ25100YFPR | C527572 | Extended | OOS / high when last read |
| U4 | TLV71330PDBVR | C2863702 | Extended | Stock existed |
| U5 | USBLC6-2SC6 | C7519 | — | USB ESD |
| Q1 | AO3401A | C15127 | — | P-FET |
| Q2–Q5 | 2N7002 | C2128 | Basic typical | Inhibit, LED, divider enable |
| D1 | PESD5V0L1UL | C24109 | — | VBUS ESD |
| D2 | 0402 LED | C72043 | — | Charge indicator, UNVERIFIED Vgs |
| J1 | TYPE-C-31-M-14 | C223907 | Extended | 16P USB2 |
| J2 | SM02B-SRSS-TB | C160404 | — | JST-SH |
| J3 | 1×03 RA 2.54 | C49257 | — | Bench |
| SW1 | TS-1187A | C318884 | — | 4.5 × 4.5 × 1.6 |
| L1 | 10 µH 0603 | C1045 | — | nRF DCCH |
| R1–R3 | 220 kΩ 0402 | C25803 | — | Per-path bound |
| R11 | 6.80 kΩ | C25848 | — | ISET |
| R12 | 6.04 kΩ | C25841 | — | PRETERM |
| R13, R25, R26, R28 | 10 kΩ | C25792 | — | TS, CHG_MON, nRESET |
| R9, R10 | 5.1 kΩ | C25905 | — | CC |
| others | see BOM | — | — | Decoupling **per ADS1292 / BQ25100 / TLV713 typical** |

Not in BOM: J4 TC2030-NL, P1–P3 pads, H1–H2 holes, R29–R30 DNP 10 MΩ, power flags.

## 14. Reference-circuit check (each choice)

| Choice | Verdict |
|---|---|
| ADS1292 3.0 V AVDD=DVDD, internal ref, 10 µF VREFP, 1 µF VCAP1, 100 nF VCAP2, 1 µF+100 nF on +3V0 | Per typical (SBAS502C) |
| RLD 1 MΩ + 1.5 nF | Per typical |
| 220 kΩ on SIG1, SIG2, REF | Per plan v2 §5.5, not a TI typical value |
| Unused IN2 tied to +3V0 | Deviates: unused channel biased to AVDD rather than shorted inputs; recorded |
| CLKSEL to +3V0 (internal clock), CLK NC | Per typical for internal clock |
| PWDN/START pulldowns | Deviates toward fail-safe reset; TI typical often leaves them to the host |
| 10 kΩ SPI series | Deviates: current limit for an unpowered AFE, not a TI typical |
| BQ25100 6.80 kΩ ISET, 6.04 kΩ PRETERM, 10 kΩ TS, 10 nF ISET, 1 µF IN/OUT | Per equations / typical |
| No /CHG LED from a CHG pin | Per BQ25100 pinout; LED from ISET is a deviation and UNVERIFIED |
| TLV713 EN to IN | Per typical “always on” |
| nRF HV inductor 10 µH | Per Raytac 8.1 |
| USB CC 5.1 kΩ, 16P, ESD | Per USB-C USB2 device |
| P-FET inhibit | Plan R7/G2, not a TI typical |
| 8 × 8 mm ENIG pads | Plan §5.3 |

## 15. What DRC says

Command: `kicad-cli pcb drc --format json` via `scripts/board/release.py`.

This round does not route. Placement is a packed provisional 17 × 33 mm floorplan so that footprints exist for CPL/gerbers/STEP.

| Item | Result (one release run, 2026-09-17) |
|---|---|
| Unconnected items | 0 (no ratsnest items in the JSON) |
| DRC errors | 829 (courtyard overlap, silk overlap, silk over copper, clearance, items in keep-out, mask bridge, hole/edge clearance) |
| DRC warnings | 21 |
| Routing | Not done |

The error count is expected until WP11's outline and a real layout pass. The release job **does not** fail on DRC errors. It fails closed on ERC errors and missing files.

## 16. ERC

`kicad-cli sch erc --format json`: **0 errors**.

Warnings (explain):

- `lib_symbol_mismatch` on extends parts (AO3401A, 2N7002, TLV71330PDBV, USBLC6-2SC6, PESD5V0L1UL) and on custom `elicio` symbols. The sheet embeds a resolved copy (parent graphics, child name) so KiCad 10 will load it. The cache copy then differs from the .kicad_sym parent.
- `footprint_link_issues` for `Connector_PinHeader_2.54` when `kicad-cli` does not attach the project table. The footprint file is KiCad's `Connector_PinHeader_2.54mm.pretty`.

## 17. Release job

`scripts/board/release.py` runs ERC, DRC, JLC-column BOM, JLC CPL, gerbers+drill, STEP (`--board-only`), and `release/summary.json`. Non-zero exit on any ERC error or any missing output.

`tests/test_board_release.py` asserts ERC 0, summary present, BOM rows = placed parts. If `kicad-cli` is missing the test fails with `brew install --cask kicad`.

## 18. Needs a decision

1. **G1b** — SparkFun's pack page says JST-SH; a linked drawing has said JST-PHR. SH is placed; PH is in the library. Freeze one revision with polarity and lead length.
2. **WP11 outline** — 17 × 33 mm is provisional. Three 8 × 8 mm pads with 1 mm keep-out do not pack with the module RF zone on this outline; P3 overlaps the RF keep-out.
3. **Charge LED from ISET** — Vgs(th) vs ISET voltage is UNVERIFIED. AIN7 is the firmware status path.
4. **System load vs termination** — if nRF current while charging exceeds ~2 mA, BQ25100 may not terminate.
5. **Probe I/O at 3.0 V target** — G4 must measure; do not infer from 3.3 V nominal.
6. **E73 land** — pad geometry copied from E73-2G4M04S; confirm M08S1C drawing before any B build.
7. **YFP0006 land** — copied from KiCad DSBGA-6 0.40 mm; confirm TI 4223410/A before order.
8. **No BAV199 clamps** — plan v2 §5.5 does not name them; v1 interface still does.
9. **BQ25100YFPR stock** — last read was extended and weak; G3 is not this package.
10. **Protective monitor cadence** — V_STOP is a firmware constant; Q5 must be on at that cadence, not only every 10 s.
