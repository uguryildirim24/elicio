# Board v4 — design note (smaller body)

Draft. **Not routed**: DRC 0 errors with the project rules, but 10 connections are still open (5 GND, 2 AFE_VIN, 1 AFE_DRDY, 1 CHG_MON, 1 VBUS_DET); §9.4 lists them with pads and gaps.
Date: 2026-09-23. Lanes t-0012 (Opus 5.5: design and first routing) and t-0014 (this state).

## 1. Size levers

Frame: u = width (anterior 0 → posterior), s = arc from the hook end, y = thickness from the skin face. All sizes in mm. Flat PCB (x, y) = (u, s).

Baseline v2: W 22, T 9.0 (LID_Y 8.0 + lid 1.0), chord 47.90. The M1 gate is M1 ≥ chord + 3 = 50.9. Default M1 is 52 (Q34, not measured; Rolf: "i have big ears").

"W/L/T saved" is the body dimension saved. Where a lever only frees board area, the area is given instead, as courtyard mm². The area levers together are what let the island shrink from 17.5 to 13.5 wide.

### 1.1 Lever table

| # | Lever | W saved | L saved | T saved | What Rolf gives up | Risk | Cost change | Taken |
|---|---|---|---|---|---|---|---|---|
| L1 | Clear the pocket beside the cell. U2, SW1 and J2 move onto the island. P4/P5 become one-face wall rings on a plate that folds 90° beside the cell (§4.4) | **4.0** (22 → 18) | 0 | 0 | Nothing electrical. Shell changes: a slot in the rib for the flap, and the closure screw moves (§7) | The 90° fold at R 1.1 is exactly JLC's 10× limit. Plate top 6.895 against LID_Y 7.1 | Shell reprint (needed anyway). Board: UNVERIFIED | **Yes** |
| L2 | ISP1807-LR SiP (8 × 8 × 1.0) replaces the Raytac MDBT50Q (15.5 × 10.5 × 2.3) | makes L1's 13.5-wide island possible (courtyard 190 → 74 mm²) | 0 | **0.62** (a Raytac on the v4 island would need T ≈ 8.72) | RF margin: about 13 mm of metal-free edge against the 18 recommended (§4.2). Not in the JLC library, so it must be consigned. No VDDH, so U5 is added | Range is UNVERIFIED until a range test. 0.65-pitch LGA on flex | $14.01 (-ST) / $13.65 (-RS) qty 1, Mouser, https://www.mouser.com/ProductDetail/Insight-SiP/ISP1807-LR-ST, read 2026-09-23. Raytac price UNVERIFIED. Consignment fee UNVERIFIED | **Yes** |
| L3 | Island stiffener FR4 0.4 → 0.2 (one B-side piece under U1, the P2 landing and J4) | 0 | 0 | **0.28** | Nothing | Less stiffness under the lid posts and at the LGA. G7 load not computed | None expected. Stiffener fee: §3.3 | **Yes** |
| L4 | J2: JST-SH (mated 2.95) → Molex Pico-EZmate Slim 202656-0021 (mated 1.20, top entry) | lets J2 sit on the island (part of L1) | 0 | lets J2 fit under LID_Y 7.1 (top 6.32; SH would reach 8.07) | The cell must come with a Pico-EZmate Slim plug fitted by a vendor. R2 forbids Rolf crimping. This changes the G1b/Q69 purchase route | Supply of a cell with that plug is UNVERIFIED | Header and plug prices UNVERIFIED. Not in the JLC library | **Yes** |
| L5 | SW1: TS-1187A (4.5 × 4.5 × 1.6) → HRO 1TS015A (3.0 × 2.0 × 0.6) | area about 42 → 11 mm² | 0 | 0 (top 5.72) | Nothing (1.2 N press) | Low | C398746, 25,177 in stock (https://jlcpcb.com/partdetail/C398746, read 2026-09-23). Price UNVERIFIED | **Yes** |
| L6 | Non-Contact R and C 0402 → 0201. 10 µF 0603 → 0402 | area about 40 mm² (35 parts) | 0 | 0 | Nothing | JLC lists FPC assembly and a 0201 minimum separately. That the two combine on FPC is UNVERIFIED | +$3.00 per new extended part number (L8 §2.2, read 2026-09-18). About 6–12 new lines gives +$18–36 (UNVERIFIED) | **Yes** |
| L7 | Q1–Q4 SOT-23 → DFN1006-3. U4 SOT-23-5 → X2SON-4 | area about 57 mm² | 0 | 0 | Nothing | The Q2–Q4 part is not chosen (UNVERIFIED). U4 C3071062 has 0 stock at JLC | Q1 WPM3027-3 C240195. The rest UNVERIFIED | **Yes** |
| L8 | Lid posts replace the two board screws and bosses (H1/H2 go) | area about 17 mm² | 0 | 0 | Nothing. Assembly step 5 ("Turn the board screws") goes | The P2 post presses on U1's top. Force not computed (G7) | None | **Yes** |
| L9 | Drop the DNP parts and the part the SiP makes redundant (Q5, R9, R10, R29, R30, L1) | area about 21 mm² | 0 | 0 | The option to fit R29/R30 lead-off bias later | None | None | **Yes** |
| L10 | Drop R26 (nRESET 10 kΩ pull-up). P0.18 set as RESET has its own pull-up (PS v1.11 §5.3.8.3 tPINR = 5 × 13 kΩ × C; §7.3 reference circuits have no reset resistor) | area about 0.6 mm² and one via | 0 | 0 | Nothing. Firmware must set UICR PSELRESET (§8) | Low | −1 BOM line | **Yes** |
| L11 | Via 0.45/0.20 → 0.40/0.15 (JLC flex standard: hole ≥ 0.15, pad ≥ 0.35, 0.40 recommended) | routing room, not courtyard | 0 | 0 | Nothing | Low: still the standard via | None expected | **Yes** |
| N1 | W16: ISO 4032 M2.5 nuts (m 2.0) replace the 3.0 P4/P5 standoffs | 2.0 (18 → 16.01) | 0 | 0 | Routability. The island would be 11.5 wide | High: W17 already fails to place (N14) | Nut price UNVERIFIED | No |
| N2 | 401012 cell (4.2 × 10.2 × 13.5, 40 mAh) replaces the 501012 | 0 | −0.5 (chord 48.40, M1 ≥ 51.4) | 0.5 (T ≈ 7.6) | 0.5 of length. Same capacity | LID_Y 6.6 is set by the P4/P5 hex (AF 5.0 between floor 1.5 and lid, 0.05 spare each side) and by J2 (6.32 + 0.28). The plate needs a re-cut (plate top 6.895 > 6.6), putting the ring at y ≈ 4.05. The shell must confirm. The cell has flying leads, so the plug must be fitted | €2.74 qty 1, https://ampul.eu/en/battery/6411-li-pol-battery-40mah-37v-401012, read 2026-09-23. Compare 501012 ~$3.50–5.00, https://www.aliexpress.us/item/3256804164251088.html, read 2026-09-23 | Rolf's option |
| N3 | 301012 cell (3.2 × 10.2 × 13.5, 25–30 mAh) | 0 | −0.5 | 0.5 (still 7.6: the hex and J2 set LID_Y) | 10–15 mAh (§1.3) | As N2 | $3.20, https://www.aliexpress.us/item/3256808874133671.html, read 2026-09-23 | No: a pure loss against N2 |
| N4 | 401010 cell (4.2 × 10.2 × 11.5, 30 mAh) | 0 | **1.5** (chord 46.40, M1 ≥ 49.4) | 0.5 (T ≈ 7.6) | 10 mAh (§1.3) | As N2 | $10.00, https://lipolybatteries.com/product/30mah-lipo-battery-lp401010-4mm-thickness-3-7-v-battery, read 2026-09-23 | Only if M1 < 50.9 |
| N5 | T ≈ 7.4: M2 P4/P5 hardware, Hirose DF58 J2 (mated 1.00) and a cell ≤ 4.2 | 0 | per cell | about 0.7 | A second hex key, which breaks plan R2 | New hardware and connector sourcing | UNVERIFIED | No (R2) |
| N6 | Foam 0.5 → 0.3 (plan v2 §3's number; decision 57 chose 0.5) | 0 | 0 | 0.2 (T 7.9) | Cushion under the cell | Plate top 6.895 against LID_Y 6.9: needs a plate re-cut | None | No (decision 57 stands) |
| N7 | 2.0 standoffs at P4/P5 | 0 | 0 | 0 on its own | — | SKU UNVERIFIED (plan §3 verified only 3.0 and 4.0) | UNVERIFIED | No |
| N8 | Full 18 mm antenna keep-out | 0 | **−5** (M1 +5) | 0 | 5 mm of body length | — | — | No: range test instead |
| N9 | ADS1291 (1 channel) | 0 | 0 | 0 | Channel 2: **changes function** | Same RSM 4 × 4 package, so no size gain | C2651548 $12.3149, 1 in stock, https://jlcpcb.com/partdetail/C2651548, read 2026-09-23 | No |
| N10 | MAX30003 (2.74 × 2.93 WLP) | area only | 0 | 0 | 512 SPS max, 18-bit: **changes function** | — | DigiKey page in research §3.3 | No |
| N11 | nRF52840 on the board, not in a module (WLCSP 3.544 × 3.607) | area only | 0 | 0 | The module's certification (FCC ID) | Antenna, crystals and matching on the board. The Johanson 2450AT18A100 needs a 9.5 × 6.2 ground clearance | — | No |
| N12 | u-blox ANNA-B402 (6.5 × 6.5 × 1.2, nRF52833) | area only; needs a host antenna strip and a 32 kHz crystal | 0 | −0.2 against the ISP1807 | Moves from nRF52840 to nRF52833 | The antenna strip takes back the area | $7.22 qty 1, https://www.digikey.com/en/products/detail/u-blox/ANNA-B402-00B/13684241, read 2026-09-23 | No |
| N13 | 4-layer flex | 0 | 0 | 0 | — | 0.20+ thick breaks the R 1.1 and R 1.5 folds (static bend ≥ 10× thickness) | — | No |
| N14 | W17 (the first pick) | 1.0 (18 → 17) | 0 | 0 | Nothing electrical | **Tried; it doesn't place.** B-side room is the limit, not total area (§1.4) | — | No |

### 1.2 Thickness chain

| y top | v2 | v4 (501012) |
|---|---|---|
| Floor | 1.50 | 1.50 |
| Ring (PI 0.11 + FR4 0.2) | 1.81 | 1.81 |
| Standoff 3.0 top = island underside | 4.81 | 4.81 |
| Island stiffener | FR4 0.4 → 5.21 | FR4 0.2 → 5.01 |
| Island PI top | 5.32 | 5.12 |
| Module top | 7.62 (Raytac 2.3) | 6.12 (ISP1807 1.0) |
| J2 mated top | pocket beside the cell | 6.32 (1.20 on the island) |
| SW1 top | pocket | 5.72 |
| Cell: floor 1.5 + foam 0.5 + cell | 7.10 (501012) | 7.10 (501012) |
| LID_Y | 8.00 | **7.10** (set by the cell) |
| T = LID_Y + lid 1.0 | 9.0 | **8.1** |

A Raytac on the v4 island would top out at 7.42. With 0.3 clearance that is T ≈ 8.72, so the ISP1807 saves 0.62 and the thinner stiffener the other 0.28.

### 1.3 Hours of wear (estimate, UNVERIFIED)

`docs/EARPIECE_DESIGN.md` says a 501015 at 50 mAh gives "Seven hours of streaming". That implies about 7 mA average. Nothing here was measured.

| Cell | mAh | Hours at ~7 mA |
|---|---|---|
| 501012 / 401012 | 40 | ≈ 5.7 |
| 401010 | 30 | ≈ 4.3 |
| 301012 | 25–30 | ≈ 3.6–4.3 |

Montage S3 wear is ≤ 4 h/day.

### 1.4 The pick

**W 18, T 8.1, chord 47.90 with the 501012 cell. Needs M1 ≥ 50.9.**

- **W 18** is the narrowest width I could place with every part and a via escape for each B-side net (§6).
  - **W17 was the first pick and failed at placement.** Total fill looked fine (71.4%), but the B side is mostly keep-out: the P1 landing (R 3.2), the U1/P2/J4 stiffener (no B parts) and the RF band (all layers). What's left at W17 is a 3.4 × 4.85 pocket, the area under U2 and a strip along the −s edge. The seven divider and interlock parts (R16, R18–R21, Q2, C14) didn't fit there with room for their vias.
  - The extra 1.0 goes to the posterior column, u 14.75–15.75. That holds R3, R16, the charger on B and the Contact/J3 corridor.
  - W16 needs nuts in place of the P4/P5 standoffs and has less room than W17 (N1).
  - The contacts alone set W ≥ 15.0: the P2 well at u 10.4, plus 3.06, plus a 1.5 wall.
- **T 8.1** is set by the cell stack (1.5 + 0.5 + 5.1 = LID_Y 7.1). Nothing on the island is taller than 6.32.
- **L** is unchanged, so the default M1 52 clears with 1.1 to spare.
- **Against v2:** W −4.0 (−18%), T −0.9 (−10%).

**Options for Rolf:**

- **W16/W17:** not offered. W17 doesn't place; W16 has less room still.
- **Thinner cell (401012):** T ≈ 7.6, chord 48.40, M1 ≥ 51.4, €2.74 against ~$3.50–5.00. Gives up 0.5 of length and all but 0.05 of the P4/P5 hex margin. Needs a plate re-cut and shell confirmation. Same 40 mAh.
- **301012:** the same T 7.6 with 10–15 mAh less. Not worth it.
- **401010:** T ≈ 7.6 and L −1.5 (M1 ≥ 49.4) for 30 mAh at $10.00. Only if M1 turns out < 50.9.

## 2. Parts: keep, change, remove

v2 list from the v2 netlist (board-v2.md G2/BOM). v4 list from `hardware/board/v4_parts.py`.

| v2 | v2 part | v4 | Action | Note |
|---|---|---|---|---|
| U1 | MDBT50Q-1MV2, C5118826 | ISP1807-LR-RS | change | Same nRF52840. Antenna, crystals and DC/DC inside. No LCSC code: consign |
| U2 | ADS1292IRSMT, C89288 | same | keep | ADS1291 considered: same package, loses channel 2 |
| U3 | BQ25100YFPR, C527572 | same, courtyard cut to ±0.8 × ±1.06 (`Texas_YFP0006_V4`) | keep | |
| U4 | TLV71330PDBVR SOT-23-5, C2863702 | TLV71330PDQNT X2SON-4, C3071062 | change | 0 stock at JLC (2026-09-23). TPS7A0230PDQNR fits the same land (same DQN pin map) |
| — | — | U5 TPS7A0230PDQNR, X2SON-4 | **add** | +VDD 3.0 V from VBAT (the SiP has no VDDH). 25 nA Iq. No LCSC code |
| — | — | C16 1 µF 0201 on VBAT | **add** | U5 input |
| L1 | 10 µH 0603, C1045 | — | **remove** | Stops nothing: DCCH is not brought out; the SiP carries its own DC/DC parts |
| Q1 | AO3401A SOT-23, C15127 | WPM3027-3 DFN1006-3, C240195 | change | Vgs(th) max −1.0, 800 mΩ max at −2.5 V |
| Q2–Q4 | 2N7002 SOT-23, C2128 | N-FET DFN1006-3 (SOT-883 land) | change | Part UNVERIFIED (Vgs(th) ≤ 1.0 needed) |
| Q5 | 2N7002, DNP | — | **remove** | Stops nothing: DNP, BAT_MEAS_EN was never driven |
| D1 | PESD5V0L1UL SOD-523, C24109 | same | keep | VBUS TVS |
| D2 | LED 0402, C72043 | same | keep | Charge LED |
| J2 | SM02B-SRSS-TB, C160402 | Molex 202656-0021 Pico-EZmate Slim | change | Mated 1.20. Not in the JLC library. The cell needs the matching plug (L4) |
| J3 | HDR-3-RA, C49257 | same, on a break-off tab behind R31–R33 | keep | Q91. Pin order as v2 (J3.1 SIG1 side, J3.2 SIG2, J3.3 REF). Each pin has its own 220 kΩ on the tab (§5.4) |
| J4 | TC2030-NL | same | keep | Not in BOM |
| SW1 | TS-1187A, C318884 | HRO 1TS015A, C398746 | change | 3.0 × 2.0 × 0.6 |
| P1–P3 | RING_PAD_D5_H2.7 | same | keep | |
| P4, P5 | RING_PAD_D5_H2.7 on the CHARGE tab | RING_1S_D4.6_NPTH2.7, copper on B only | change | Wall rings (Q90) |
| H1, H2 | island holes Ø2.7 | — | **remove** | Stops nothing electrical. Lid posts hold the island (§5.3) |
| R1–R3 | 220 kΩ 0402, C881401 | same | keep | Contact, not shrunk |
| — | — | R31–R33 220 kΩ 0402, C881401 | **add** | The bench header's own 220 kΩ per pin (R7), on the break-off tab; they leave with it |
| R4, R17, R20, R21 | 1 MΩ 0402, C26083 | 0201, C473482 | change | |
| R5–R8, R13, R25, R27, R28 | 10 kΩ 0402, C25744 | 0201, C473048 | change | |
| R26 | 10 kΩ 0402, nRESET pull-up | — | **remove** | Stops nothing: P0.18 as RESET has its own pull-up (L10). Firmware sets UICR PSELRESET (§8) |
| R9, R10 | 5.1 kΩ, DNP | — | **remove** | Stops nothing: USB-C CC with no receptacle (Q81, Q95) |
| R11 | 6.80 kΩ 0402, C25917 | 0201, C4104700 | change | ISET unchanged (≈ 19.85 mA) |
| R12 | 6.04 kΩ 0402, C966759 | 0201, C270341 | change | |
| R14–R16, R23, R24 | 100 kΩ 0402, C25741 | 0201, C270364 | change | |
| R18 | 47 kΩ 0402, C25792 | 0201 | change | Code UNVERIFIED. VBUS_DET is now the only VBUS sense |
| R19 | 27 kΩ 0402, C25771 | 0201 | change | Code UNVERIFIED |
| R22 | 1 kΩ 0402, C11702 | 0201, C270365 | change | |
| R29, R30 | 10 MΩ, DNP | — | **remove** | Stops nothing now: lead-off stays firmware-off (plan §5.5). The land to fit them later is gone |
| C1 | 1.5 nF 0402, C1548 | 0201, C285104 | change | |
| C2 | 10 nF 0402, C1524 | 0201, C43380 | change | |
| C3–C5, C10, C13 | 1 µF 0402, C15849 | 0201, C5142566 | change | |
| C6, C8, C9 | 10 µF 0603, C19702 | 0402, C15525 (Basic) | change | |
| C7, C15 | 100 nF 0603, C14663 | 0201, C307380 | change | |
| C11, C12 | 100 nF 0402, C1525 | 0201, C307380 | change | |
| C14 | 4.7 µF 0402, C19675 | 4.7 µF 0402 | keep size | Code UNVERIFIED (v2's C19675 was never checked in board-v2) |

J1 (USB-C) and USBLC6 were already absent in v2 (Q81).

v4 placement: 59 parts plus P1–P5. On the island, 22 are on F (J4 included) and 33 on B; J3, R31 and R33 are on the tab and R32 on its neck. J4 and P1–P5 are not in the BOM, which leaves 58 lines.

**No removal changes function.** Every removed part was DNP, or is replaced by the SiP (L1), by the lid posts (H1/H2) or by the nRF's own reset pull-up (R26). The charger, charge interlock, AFE supply gate, VBUS_DET, VBAT_SENSE, CHG_MON, LED, SW1, J3 and J4 all stay.

## 3. Layers against the JLC flex rules

Source: https://jlcpcb.com/capabilities/flex-pcb-capabilities, read 2026-09-23 (research §7.1), unless another date is given. JLC does not build rigid-flex ("JLCPCB currently does not support Rigid-Flex PCBs"). So this is a 2-layer flex with FR4 stiffeners, the same construction as v2.

### 3.1 ISP1807 land on two layers

- The land is the datasheet pattern (§4.2 of the datasheet). All used pads are on the outer rows, except pad 13 (nRESET).
- nRESET leaves through a locked F.Cu 0.10 channel between pads 25 and 26. The path in module coordinates: pad 13 → (3.025, 2.7625) → (6.80, 2.7625) → (6.80, 3.05) → (8.35, 3.05).
- The RF bridge from pad 20 to pad 22 is F.Cu 0.25 (net RF_ANT).
- VSS 21 → 23 → 25 and 24 → 25 are bridged at 0.12 inside the module field.
- VSS pads 14, 16 and 18 sit on the row at u 6.65 beside the RF band. No track reaches them (the inner-row gaps are 0.25 against the 0.30 a 0.10 track needs, and the band is to the west). They are tied to the B pour by two locked GND vias **between** the pads, at (6.70, 28.725) and (6.70, 29.375): 0.40/0.15, drill in the 0.25 gap between neighbouring pads, ring edge at u 6.50, 0.05 outside the band (u ≤ 6.45). On F each ring overlaps the two pads beside it (same net), so 14, 16 and 18 are one piece; on B the rings land in the pour, which reaches u 6.45 there. Every VSS pad is on GND, as the datasheet asks ("Should be connected to ground plane on application PCB"), with no copper in the band.
  - Not via-in-pad: the drills are between pads. The coverlay window over the U1 land and solder wicking into the two 0.15 holes at reflow are UNVERIFIED (§11.1).
  - The claim that the module ties all VSS pads together inside stays UNVERIFIED and is no longer needed.
- VBUS (pad 12) and D+/D− (8/10) sit on the same row and stay unconnected (§8).
- No via-in-pad. The datasheet allows "a small number of internal pads … by placing normal vias in the centre of the device … vias tented". v4 doesn't need it.

### 3.2 Stack-up and rules

| Item | JLC | v4 |
|---|---|---|
| Layers | 2-layer 0.11 / 0.12 / 0.20; 4-layer 0.20–0.45 | 2-layer, finished 0.11 |
| Copper | 3/3 mil at 12 µm, 3.5/3.5 mil at 18 µm; 4/4 mil at 1 oz (board-v2, read 2026-09-17) | 0.10 / 0.10 default |
| Contact class (SIG1, SIG2, REF) | ≥ 0.10 | 0.15 track / 0.20 clearance (unchanged from v2) |
| Charge track | — | 0.20 |
| Via | standard hole ≥ 0.15, pad ≥ 0.35 (0.40 recommended); extreme 0.10 / 0.30 at extra cost | 0.40 / 0.15 (standard, annular 0.125) |
| Copper to edge | ≥ 0.30 (board-v2) | 0.30 |
| Hole clearance / hole-to-hole / annular | — | 0.20 / 0.25 / 0.12 |
| Courtyards overlap | — | error |
| Finish | ENIG (board-v2) | ENIG |
| Assembly | two-sided FPC assembly (L8 §2.1); "Min. Component Size: 0201", "Min. IC Pin Spacing: 0.35mm", "Min. BGA Spacing: 0.3mm" (https://jlcpcb.com/capabilities/pcb-assembly-capabilities, read 2026-09-23) | Both sides. 0201 on FPC: UNVERIFIED |

v2 used 0.30 / 0.55 vias. The 0.40 / 0.15 via is JLC's recommended standard via and frees room on the island (L11).

### 3.3 Stiffeners

JLC offers FR4 0.10–1.60, PI 0.10–0.25 and SUS 0.10–0.30. v4 uses FR4 0.2 only, 6 pieces (v2 had 9):

| Layer | Piece | Where |
|---|---|---|
| Eco2.User (B side) | `STIFF_U1_B` polygon | Under U1, the P2 landing and J4 |
| Eco2.User (B side) | P1 landing circle | (5.90, 22.00), R 3.2 |
| Eco1.User (F side) | 3 ring pieces | P1–P3, R 2.9 |
| Eco1.User (F side) | Wall plate | P4/P5 plate, inset 0.3 |

- **Fee:** "when there are 4 or more stiffeners on the board, an extra fee is required" (https://jlcpcb.com/help/article/fpc-extra-charges, re-read 2026-09-18 per board-v2). The amount is UNVERIFIED.
- **Holes not drawn:** the outlines have no holes. The Ø2.7 ring holes and J4's TC2030-NL guide holes must pass through them. How JLC drills stiffeners is UNVERIFIED; the order note must say so.

### 3.4 Bends

- Static bend ≥ 10× thickness gives R ≥ 1.1 at 0.11.
- SIG strips: 180° at R 1.5 (v2's Q83 fold).
- P4/P5 joint: 90° at R 1.1, exactly at the limit.
- A 4-layer flex (≥ 0.20) would need R ≥ 2.0 at both folds, so it is out.

## 4. Floor plan

### 4.1 Frame, cavity and width chain

- Body W 18: cavity u 1.5–16.5.
- Island: u 2.25–15.75 × s 16.0–37.6, minus a relief notch at u 15.09–15.75 × s 16.0–19.6. Area 289.2 mm².
- Cell pocket: s 1.5–14.9. The cell is not under the island.

Width chain in the cell section:

| Item | u |
|---|---|
| Wall | 0 – 1.5 |
| Gap | 0.3 |
| Cell 501012 (pocket) | 1.8 – 11.9 (10.1) |
| Gap | 1.29 |
| P4/P5 standoff 3.0 | 13.19 – 16.19 |
| Ring 0.31 | 16.19 – 16.50 |
| Wall | 16.5 – 18.0 |

The cell section alone would allow W17 (gap 0.29). The island's B side is what needs the 1.0 (§1.4).

### 4.2 Module and RF band

- **Placement:** ISP1807 at KiCad rot 270. Mapping: u = 10.45 − Y, s = MOD_S0 + X, with MOD_S0 25.05.
  - Body: u 2.45–10.45 × s 25.05–33.05.
  - Courtyard: u 2.155–10.745 × s 24.755–33.345.
  - The antenna edge faces −u, toward the anterior board edge.
- **RF band:** u 2.25–6.45 × s 21.8–37.6. No copper on any layer, and no part except U1.
  - Depth 4.2 against the datasheet's 4.0 ("no metal, no traces and no components on any application PCB layer except mechanical LGA pads", 18.0 mm min).
  - The P1 standoff under the island is metal up to s 24.5. That leaves about **13 mm** of metal-free edge (s 24.5–37.6) against the 18 recommended.
  - The RF risk is UNVERIFIED and needs a range test. Full compliance costs about 5 of L (N8).
- **GPIO pads** face +u toward the posterior strip u 10.75–15.75, at s 26.5–31.7 (§8).

### 4.3 Island blocks (as placed)

The full table is `PLACE` in `hardware/board/build_v4.py`; §10 lists every part.

| Block | Side | Centre (u, s) | Content |
|---|---|---|---|
| U1 ISP1807 | F | (6.45, 29.05) rot 270 | Module |
| U2 ADS1292 | F | (11.85, 22.08) rot 270 | AFE |
| J2 Pico-EZmate Slim | F | (5.45, 18.90) rot 270 | Courtyard u 2.29–8.43 × s 16.11–21.70. Cell leads come in at u < 8.43 |
| AFE decoupling, RESET pull-down | F | u 7.75–10.2 × s 18.45–24.10 | C6, C7, C9, C10, R23 |
| Charger pulls | F | (12.60, 18.15), (12.60, 18.95) | R12 (PRETERM), R13 (TS) |
| CS/DRDY series, pad-23 decoupling, charge LED | F | u 11.05–14.65 × s 25.15–28.0 | R7, R27, C15, D2, R22, Q4, R28. R7 at u 11.05 and R27 turned so MOSI and CS leave U2's south row without a via (§9) |
| SPI series | F | u 11.40 × s 29.6–32.6 | R6, R5, R8 in U2's pad order |
| SW1 | F | (14.45, 31.10) rot 180 | Top 5.72 |
| J4 TC2030-NL | F | (10.00, 35.40) | Just outside the RF band (u ≥ 6.455) |
| U5 and caps | B | u 3.1–4.7 × s 17.1–18.3 | Under J2. U5, C16, C12, C13 |
| Contact resistors R1, R2, C4 | B | s 17.25–17.45 | At the strip roots |
| Charger | B | U3 (13.90, 17.75) rot 90 | U3, R11, C2, R25, C3, D1 at the joint. Both charge nets arrive on B |
| AFE gate | B | u 9.4–9.95 × s 19.95–24.65 | R15, Q3, R14, Q1, C5, R24 |
| AFE LDO and bulk | B | u 11.65–13.3 × s 21.25–24.6 | U4, C8, C14, C11, R4, C1. C14's VBAT pad faces east (§9) |
| REF resistor, dividers, interlock | B | u 11.45–14.60 × s 25.6–28.6 | R3, R16–R21, Q2. Kept east of u 11.1 so a via column at u 10.72 fits beside U1's east pads; R16/R17 sit at Q2's gate (§9) |

The same features seen from the Contact side are in §5: landings P1 (5.9, 22.0) and P2 (10.4, 33.1), R 3.2; lid posts at (5.9, 23.0) and (9.4, 32.1).

### 4.4 P4/P5 joint, flap, plate and wall rings

| Part | Flat u | Flat s |
|---|---|---|
| Joint bend | 15.090–16.904 | 16.3–19.3 |
| Flap | 16.904–19.114 | 14.85–19.3 |
| Plate | 13.914–19.114 | 1.75–14.85 |

Fold math:

- 90° fold at inner R 1.1. Neutral radius 1.155 (PI mid-plane). Arc = π/2 × 1.155 = 1.814 = 16.904 − 15.09.
- Folded plane: PI mid-plane at u 16.245 (PI u 16.19–16.30). FR4 0.2 lies on the wall side, u 16.30–16.50.
- Folded y = 3.905 + (16.904 − u_flat). The plate spans y 6.895 (u_flat 13.914) down to 1.695 (u_flat 19.114).
  - Clear of the lid at 7.1 by 0.205.
  - Clear of the floor at 1.5 by 0.195.
- Ring sites:

| Ring | Flat (u, s) | Folded wall site |
|---|---|---|
| P4 VBUS | (16.514, 4.35) | u 16.245, s 4.35, y 4.295 |
| P5 GND | (16.514, 12.10) | u 16.245, s 12.10, y 4.295 |

- P5 moves from s 12.35 to 12.10 so the flap clears the rib (s 14.9–15.7). The rib needs a slot for the flap (shell change).
- Standoffs sit at u 13.19–16.19 on the ring axis. The hex AF 5.0, centred at y 4.30, spans y 1.80–6.80.
- The wall rings (`RING_1S_D4.6_NPTH2.7`) carry copper on B only, facing the standoff end. The screw passes the NPTH Ø2.7.
- The plate is 2.26 from the SIG2 strip (13.914 − 11.65).

### 4.5 SIG/REF strips and rings

All strips are 2.5 wide with cap R 3.2, one Contact net each.

| Strip | Strip u | Flat ring | Copper | Folded site |
|---|---|---|---|---|
| SIG1 | 4.65–7.15 | (5.90, 5.29) | B | P1 (5.9, 22.0) |
| SIG2 | 9.15–11.65 | (10.40, −5.81) | F (P2 is plated) | P2 (10.4, 33.1) |
| REF | 7.25–9.75 | (8.50, 43.00) | B | P3 (8.5, 43.0) |

- SIG strips leave the island at s 16.0 and fold 180° at R 1.5 under it (v2's Q83 fold).
- REF leaves the island at s 37.6 through the end-wall slot (s 38.20–39.25).

### 4.6 J3 break-off tab

- Neck: u 15.75–20.10 × s 19.9–22.4. Tab: u 20.10–33.40 × s 16.0–28.0. Cut line: u 16.20. The tab's west edge is 0.99 from the P4/P5 flap (flap u ≤ 19.114).
- Pins, THT Ø1.5, order as v2: J3.1 BENCH_SIG1 (22.40, 19.40), J3.2 BENCH_SIG2 (22.40, 21.94), J3.3 BENCH_REF (22.40, 24.48).
- Bench 220 kΩ (0402, C881401), pad 1 (west) on the AFE side: R31 (22.40, 16.80) north of the header, R33 (22.40, 27.10) south of it, R32 (18.00, 21.15) on the neck.
- Three AFE-side runs cross the neck on F, 0.10 wide, 0.75 apart: AFE_IN1P at s 20.40, AFE_IN1N 21.15, RLD_FB 21.90. Edge gap 0.50 on both sides.
- The tab is cut before closing (Q91). The assembly sheet must show the cut line. After the cut the stub (u 15.75–16.20) carries the three bare AFE-side ends and no Contact copper (§5.4).

### 4.7 Stiffener map

See §3.3. No B-side part sits on `STIFF_U1_B` (the build script checks this). The P1 landing circle carries no B part.

### 4.8 Cavity tests (by numbers; the shell solid is not built)

| Test | Result |
|---|---|
| Island courtyards inside the cavity walls | All ≥ 0.75 inside (build check: 0 courtyards off the island). U1 overhangs the island by 0.095 and is still 0.655 inside |
| F parts under LID_Y 7.1 | Tallest J2 6.32 (0.78 spare). Module 6.12, SW1 5.72 |
| B parts over the collars (top 3.5) | B parts ≤ about 0.7 tall, so bottoms ≥ 4.31. P1 collar u 1.7–10.1 × s 17.15–26.85; P2 collar u 6.2–14.6 × s 28.3–37.95 |
| J3 stub after the cut | u 15.75–16.20, inside 16.5 |
| Wall plate | y 1.695–6.895 inside floor 1.5 and lid 7.1 |
| Cell leads | Run at u < 8.43 to J2 |

### 4.9 J2 against the P5 hex well (need ≥ 0.3)

| Item | u | s | y |
|---|---|---|---|
| J2 courtyard | 2.29–8.43 | 16.11–21.70 | 5.12–6.32 |
| P5 standoff | 13.19–16.19 | centred 12.10 | 1.80–6.80 |
| P5 well (AF 5.30, corner r 3.06) | from 13.19 | 9.04–15.16 | — |

Gaps: u 4.76, s 0.95, box distance 4.85 (courtyard outer edge; on the line-centre box of §10.2 and the test, u 4.81 and s 0.99). **J2 clears P5 by ≥ 4.76 in u (≥ 0.3 ✓)**, provided the shell's well doesn't reach past the standoff end at u 13.19 in −u. The shell must hold that.

## 5. Contact safety

### 5.1 Island and cavity boundary

- The island (u 2.25–15.75 × s 16.0–37.6) and everything on it sits inside the cavity (u 1.5–16.5), under coverlay except part pads.
- Skin reaches only the P1–P3 titanium domes and the P4/P5 screw heads in the posterior wall (Q90).

### 5.2 220 kΩ per electrode path, R7/G2

- R1 (SIG1 → AFE_IN1P), R2 (SIG2 → AFE_IN1N) and R3 (REF → RLD_FB): 220 kΩ 0402, C881401. Unchanged (Q79, R7).
- The G2 boundary-state circuit is unchanged (board-v2 §3). With VBUS present, R16/R17 turn Q2 on, AFE_EN_HW goes low, Q3 turns off, R14 pulls AFE_GATE to VBAT and Q1 turns off. The AFE is unpowered while charging.
- Only the packages changed (Q1–Q3 DFN1006-3, R14–R17 0201).

### 5.3 Landings and lid posts

- **Landings:** the P1 and P2 standoff tops (SIG1 and SIG2 metal) press on the island's B face at P1 (5.9, 22.0) and P2 (10.4, 33.1), R 3.2.
  - Inside a landing: no via, no B part. B tracks are allowed only under the FR4 0.2 stiffener, which insulates them from the standoff.
- **Lid posts** replace plan §5.2's board screws and bosses:
  - P1 post at (5.9, 23.0), Ø2.0, nylon, with an F part keep-out of r 1.3 (it sits in the RF band).
  - P2 post at (9.4, 32.1) presses on U1's top. The force is not computed (G7).
- The island is clamped between the standoff tops and the lid posts. There are no island holes.

### 5.4 Contact corridor and charge copper (as built, locked)

Contact runs are 0.15 track at 0.20 clearance. Each strip run is split at the zone exit, site ± (3.5 + 0.10). So the Q84 1.0 mm rule covers only the land segment, and the rest of the strip is under the 0.20 strip rule (Q88).

Contact copper stays on the island: each Contact net ends at its 220 kΩ (R1–R3) and nothing Contact goes to the tab. J3's pins carry the bench nets BENCH_SIG1, BENCH_SIG2 and BENCH_REF (Contact class) and reach the AFE nodes through their own 220 kΩ, R31–R33, on the tab side of the cut (R7: every gel-header path is protected by its own 220 kΩ). What crosses the neck and the cut is AFE-side copper only. Opus's first layout ran SIG1/SIG2/REF branches to J3 and left their ends bare on the stub after the cut; that is gone.

| Net | Layer | Path |
|---|---|---|
| SIG1 | B | P1 → zone exit (5.90, 8.89) → (5.90, 16.40) → R1.1 |
| SIG2 | F | P2 → zone exit (10.40, −2.21) → via (10.40, 16.50). B: via → R2.1 |
| REF | B | P3 → zone exit (8.50, 39.40) → (8.50, 37.20) → (15.35, 37.20) → (15.35, 25.60) → R3.1 |
| BENCH_SIG1 | F, 0.15 | J3.1 (22.40, 19.40) → (22.91, 18.30) → R31.2 (22.91, 16.80) |
| BENCH_SIG2 | F, 0.15 | J3.2 (22.40, 21.94) → (21.61, 21.15) → R32.2 (18.51, 21.15) |
| BENCH_REF | F, 0.15 | J3.3 (22.40, 24.48) → (22.91, 25.58) → R33.2 (22.91, 27.10) |
| AFE_IN1P | F, 0.10 | R31.1 (21.89, 16.80) → (20.50, 16.80) → (20.50, 20.40) → (15.40, 20.40); the router joins it to R1.2 and U2 pad 4 |
| AFE_IN1N | F, 0.10 | R32.1 (17.49, 21.15) → (15.40, 21.15); the router joins it to R2.2 and U2 pad 3 |
| RLD_FB | F, 0.10 | R33.1 (21.89, 27.10) → (20.90, 27.10) → (20.90, 21.90) → (15.40, 21.90); the router joins it to R3.2 and U2 pads 29/30 |

- SIG2's strip copper is on F because P2 is plated. Each strip carries one net on one layer; the one Contact via is on the island at SIG2's strip root, not in a strip. SIG1 and REF have no via.
- With the tab on (bench use), a gel lead on J3.n sees pin → 0.15 track → 220 kΩ (R31–R33) → AFE node, and the dome on the same node sees dome → strip → 220 kΩ (R1–R3) → AFE node: two independent 220 kΩ per node. The bench nets are in the Contact netclass (0.15/0.20) and R31–R33 sit at u ≥ 17.49, east of the cut.
- The cut at u 16.20 crosses only the three AFE-side 0.10 runs.

Charge copper, 0.20 track. It is only where skin can't reach: plate, flap and joint.

| Net | Path |
|---|---|
| P5 GND | B: ring → (17.95, 13.30) → (17.95, 15.75) [zone exit] → (17.95, 16.90) → (14.84, 16.90), then the router and the B pour |
| P4 VBUS | B: ring → via (16.514, 7.55) → F → (18.40, 8.55) → (18.40, 15.75) [zone exit] → via (18.40, 17.00) → B → (18.40, 18.40) → (14.65, 18.40) → U3 VBUS ball |

- P4's via is its own net inside its own 7 × 7 zone, which is allowed.
- VBUS passes P5 on F, where P5 has no copper (B-only ring). Both charge runs split at s 15.75, so only the in-zone segments carry the 1.0 mm rule.
  - On F, VBUS runs 0.44 from P5's NPTH hole edge. The hole clearance rule is 0.20, so this passes. P5's screw is GND.
- The VBUS flap via is 1.03 edge to edge from GND's in-zone segment (≥ 1.0).

### 5.5 Q84 / Q88 / Q97 check

| Rule | v4 |
|---|---|
| Q84/Q88 `tabs` 7 × 7 at P1–P3, 1.0 | Kept; the land segment only |
| `tail_pads` 7 × 7 at P4/P5, 1.0 | Kept |
| Strips: 0.20, foreign-net keep-out | Kept |
| Island: Contact class 0.20 | Kept |
| Q97(a) one Contact net per strip, one layer | ✓ (SIG2 on F, SIG1 and REF on B) |
| Q97(b) class clearance under coverlay | ✓ |
| Q97(c) no foreign via or pour inside a land's zone | ✓ (P4's own-net via only) |
| Q97(d) R1–R3's pads the only exposed Contact copper on the island | ✓: Contact nets end at R1–R3; J3 carries bench nets behind R31–R33; the stub after the cut carries AFE-side copper only (§5.4). `tests/test_board_v4.py` checks that Contact nets sit only on P1–P3 and R1–R3 and that no Contact copper lies east of u 15.75 |
| Q97 "away from U1's antenna edge" | ✓: SIG1 stays at u 5.90, s ≤ 16.40; SIG2 at u 10.40, s ≤ 16.50; REF runs along s 37.20 (u 8.5–15.35) and u 15.35. None of it is in the RF band (u ≤ 6.45, s 21.8–37.6) |

The r12 flag (Contact ends bare on the stub after the cut) is closed by R31–R33: no Contact copper crosses the cut, so no cover and no drawn exception is needed.

## 6. Target W / T / L

Area check (courtyards):

- Courtyard bounding boxes from the placed board, text parse. U1 counts only outside the RF band.
- F usable = island minus the RF band minus the P1 post keep-out.
- B usable = island minus the RF band, the landings and `STIFF_U1_B`.
- Placed at W18: F parts 155.0 mm² (22 parts), B parts 45.7 mm² (33 parts). J3 and the rings are off the island.

| W | Island u | Island mm² | F usable | B usable | F fill | B fill | Result |
|---|---|---|---|---|---|---|---|
| 16 | 2.25–13.75 | 246.0 | 178.3 | 83.4 | 87% | 55% | Not tried (needs nuts) |
| 17 | 2.25–14.75 | 267.6 | 199.9 | 104.6 | 78% | 44% | **Tried, doesn't place** |
| **18** | 2.25–15.75 | 289.2 | 221.5 | 126.2 | **70%** | **36%** | **Placed: 0 keep-out problems** |

B fill looks low, but B usable is scattered: most of it lies in the P1 landing's shadow, under the stiffener, or in thin strips. At W17 the seven divider/interlock parts had no block of B area with room for their vias (§1.4). Area alone doesn't decide this; the placed board does.

Body per cell (T and L don't depend on W):

| Cell | T | Chord | M1 ≥ | mAh |
|---|---|---|---|---|
| 501012 (pick) | **8.1** | **47.90** | **50.9** | 40 |
| 401012 | ≈ 7.6 | 48.40 | 51.4 | 40 |
| 301012 | ≈ 7.6 | 48.40 | 51.4 | 25–30 |
| 401010 | ≈ 7.6 | 46.40 | 49.4 | 30 |
| v2 reference (W22) | 9.0 | 47.90 | 50.9 | 40 |

W16 needs M2.5 nuts at P4/P5 (m 2.0, W 16.01). W18 needs nothing new.

## 7. Plan-v2 clauses that block a smaller body

I didn't edit plan-v2. Each clause below is one v4 departs from, or one that stops a smaller step.

| Clause | Text | v4 | Why |
|---|---|---|---|
| §3 | "The module sits on the board's top; nothing taller than the module anywhere." | J2 mated 1.20 > module 1.0 | The lowest verified 2-pin connector in the local research that R2 allows is 1.20. DF58 (1.00) needs crimping or a pre-crimped lead. J2 still sits under LID_Y with 0.78 spare |
| §3 module envelopes | "Modules: Raytac 10.5 × 15.5, reserve 2.3; E73 13 × 18 × 2.0" | ISP1807 8 × 8 × 1.0 | Both listed modules are too big for W18 |
| §1 item 5 / §4 | Candidates A (Raytac) or B (E73) | Neither | As above |
| G3 | Module sourcing | Consignment or global sourcing | ISP1807 is not in the JLC library |
| G3c | The module's antenna keep-out from its own document | About 13 mm metal-free against 18 | Full compliance costs about 5 of L. Needs a range test |
| §5.2 | "Rigid FR4, 4 layers, 1.0 mm … M2.5 mounting holes onto printed bosses" | 2-layer flex (already interface II in v2), lid posts, no board screws | Screws and bosses cost island area and a step. A 4-layer flex breaks the folds |
| §8 step 4 | "holes over the bosses" | No holes. The island sits on the P1/P2 standoff tops under the lid posts | |
| §8 step 5 | "Turn the board screws with the hex key until they seat." | Step removed | Lid posts |
| §8 step 8 | USB-C | Already gone (Q81) | — |
| R2 | "one 1.5 mm hex key, no soldering, glue, crimping or wire stripping" | Kept | Blocks M2 P4/P5 hardware (N5) and J2 solder tabs. Requires the cell to come with the Pico-EZmate Slim plug fitted (G1b/Q69) |
| §5.5 supply gate | — | Kept | Refused as a lever |
| §5.6 bench header | — | Kept on the break-off tab | Q91 |
| Q90 P5 site | s 12.35 | s 12.10 | Flap clears the rib at s 14.9 |
| Closure | M2.5×8 at (u 16.50, s 41.00) | Redesign, not a move (shell change) | At W18 the tail is u 0–18. Beside the Ø7.5 REF pocket (u 4.75–12.25) a Ø5.0 head well with 1.0 walls needs 7.0 of u: 12.25 + 1.0 + 5.0 + 1.0 = 19.25 > 18 on the +u side, and 4.75 − 7.0 < 0 on the −u side. So either the well goes past the pocket into the tail loft (centre s ≥ 43 + 3.75 + 1.0 + 2.5 = 50.25, which is beyond the loft start 45.5 and needs the tongue slot moved) or the closure becomes a latch |
| Rib | s 14.9–15.7 | Slot for the P4/P5 flap (shell change) | Cut the rib back 0.50 from the posterior wall over its full height: remove u 16.00–16.50 × s 14.90–15.70 × y 1.50–4.50. The flap (0.31 thick on the wall face, y 1.695–3.905) then has 0.19 of air (§4.4, §10.2) |
| P4/P5 wall collars | r9: hex sockets 2.08 proud of the wall face, wells 3.28 deep | Must go (shell change) | The plate lies on the wall face (u 16.19–16.50 × s 1.75–14.85 × y 1.695–6.895); a socket proud of the face would sit on the plate. Key each standoff instead with two floor-standing walls: u 13.19–16.19, s = site ± (2.65 + 0.15) outward, 1.0 thick, y 1.50–4.30 (up to the hex axis; AF 5.0). The standoff's −u end stays open; the cell (u ≤ 11.90) is 1.29 away |
| Lid posts | none | Two posts on the lid (shell change) | Ø2.0 at (5.90, 23.00), 1.98 long onto the island's F face at y 5.12; and at (9.40, 32.10), 0.98 long onto U1's top at 6.12 (§5.3) |
| LID_Y | 8.0 | 7.1 | Set by the cell (§1.2); T 8.1 |
| Cavity width | u 1.5–20.5 (W22) | u 1.5–16.5 (W18) | §4.1. Everything else of the r9 shell (SIG fold pockets, REF slot, hinge, hook) is used unchanged in §10.2 |
| Foam 0.5 (decision 57; plan §3 says 0.3) | — | 0.5 kept | 0.3 would give T 7.9 with a plate re-cut (N6) |

## 8. Firmware pin map (for WP13)

Pin map A (as built). Every fast SPI line is on a full-speed pin; the low-frequency pins carry only slow or analog signals.

| Signal | v2 nRF | v4 nRF | ISP1807 pad | Note |
|---|---|---|---|---|
| AFE_SCLK | P0.08 | P0.06 | 34 | |
| AFE_MOSI | P0.06 | P0.05 | 36 | |
| AFE_MISO | P0.15 | P0.08 | 32 | Full-speed pin (see below) |
| AFE_CS | P0.13 | P0.28 | 48 | LF-only; toggles once per frame |
| AFE_DRDY | P0.17 | P0.29 | 46 | LF-only; one pulse per sample |
| AFE_START | P0.20 | P0.10 / NFC2 | 4 | NFC pin as GPIO; static |
| AFE_RESET (PWDN) | P0.22 | P0.26 | 6 | |
| CHG_MON | P0.31 AIN7 | P0.30 AIN6 | 44 | Analog |
| VBAT_SENSE | P0.02 AIN0 | P0.31 AIN7 | 42 | Analog |
| VBUS_DET | P0.24 | P0.02 | 40 | Digital input; slow |
| LED_EN | P0.04 | P0.03 | 38 | Slow |
| BAT_MEAS_EN | P0.03 | — | — | removed (Q5) |
| nRESET | P0.18 | P0.18 | 13 | Pad channel (§3.1). No external pull-up (R26 removed) |
| SWDIO / SWDCLK | SWDIO / SWDCLK | same | 28 / 30 | J4 |
| +VDD | module REGOUT0 | VCC_nRF from U5 | 26 | 3.0 V |

**Low-frequency pins.** In the nRF52840 PS v1.11 pin table, P0.28, P0.29, P0.30, P0.31, P0.02, P0.03, P0.09 and P0.10 say "Standard drive, low frequency I/O only". Footnote 322: "Low frequency I/O is a signal with a frequency up to 10 kHz." The footnote doesn't exempt inputs.

- The first draft put AFE_MISO on P0.29, an LF-only pin, carrying SPI data at the SCLK rate. Pin map A moves SCLK, MOSI and MISO to P0.06, P0.05 and P0.08 (pads 34, 36, 32), which are full-speed.
- CS, DRDY, START, LED_EN, VBUS_DET, CHG_MON and VBAT_SENSE are slow or analog, so they're fine on LF pins.

**Reset pin.** R26 is gone. Firmware must configure P0.18 as RESET: UICR PSELRESET[0] and [1] = 18 (Zephyr `CONFIG_GPIO_AS_PINRESET`). Until that is written, P0.18 is a plain GPIO and SW1 does nothing. The pin's own pull-up does the job. PS v1.11 §5.3.8.3 gives tPINR as 32.5 ms at 500 nF and 650 ms at 10 µF, which is 5 × 13 kΩ × C: my reading is an internal pull-up of about 13 kΩ. The §7.3 reference circuits show no external reset resistor. A factory-fresh module is programmed over SWD (J4), which does not need the reset pin.

**NFC pins as GPIO.** Set UICR NFCPINS.PROTECT = Disabled (Zephyr `CONFIG_NFCT_PINS_AS_GPIOS`). PS §6.14.3: "some increased leakage current between the two pins is to be expected if they are used in GPIO mode, and are driven to different logical values. To save power, the two pins should always be set to the same logical value whenever entering one of the device power saving modes". INFC_LEAK is 1–10 µA. Pad 2 (P0.09/NFC1) is left open. Firmware should drive it to START's level before sleep.

**Isolated VSS 14/16/18.** Unconnected on purpose (§3.1). Whether the module ties them inside is UNVERIFIED.

**VBUS (pad 12) and D± (8/10) are unconnected.**

- The module never sees USB.
- `firmware/elicio_stream/elicio_stream.ino` reads VBUS through `NRF_POWER->USBREGSTATUS`. It must switch to the VBUS_DET GPIO (R18/R19 divider).

**First load.** VDD is 3.0 V from U5 from power-up, so v2's REGOUT0 1.8 V first-load issue is gone. A 3.3 V probe sits at VDD + 0.3, not over it. G4 still verifies.

## 9. Routing status

**Not routed. Don't order this board.** `hardware/board/elicio-v4.kicad_pcb` as committed:

- 1457 track segments and 53 vias (69 of them locked pre-routes and vias). 10 connections are still open (5 GND, 2 AFE_VIN, 1 AFE_DRDY, 1 CHG_MON, 1 VBUS_DET); they are listed with their pads and gaps in §9.4.
- The two GND pours (F and B, over the whole island) are filled and saved; the release DRC does not refill.
- DRC (kicad-cli 10.0.6, project rules `elicio-v4.kicad_dru`, `--schematic-parity`), verbatim: `Found 75 violations`, `Found 10 unconnected items`, `Found 2 schematic parity issues`.
  - Errors: 0: no short, no clearance error, no starved thermal (§9.3). Unconnected: 10.
  - Warnings: 64 `lib_footprint_issues`, 10 `track_dangling`, 1 `via_dangling`. `via_dangling` is the +VDD pre-route via at (7.60, 36.70), used on F only. `track_dangling` marks the free ends of the open connections in §9.4. The parity warnings are J2's two MP pads, which have no schematic pin.
- `scripts/board/release.py --board elicio-v4 --routed` refused: exit 1, `routed release refused: {"unconnected_items": 10}`. `release.py --board elicio-v4` without `--routed` then wrote the review outputs with `routed: false`: ERC 0 errors, DRC 0 errors, 58 BOM rows, 58 CPL rows, 17 Gerber files, STEP without models for 5 footprints (Molex, Texas, Texas, Texas, SOT-883.step). Review files, not order files.

### 9.1 What each router did

| Router | Input | Result |
|---|---|---|
| Freerouting 2.4.1 on OpenJDK 25, `-Xmx4g`, locked Contact copper as fixed wires (`scripts/board/route_v4.py --route`; t-0012) | W18 as placed at 9fc962b | 18 connections open; it never closed them |
| `v4_route_pf.py` (negotiated congestion on a 0.025 grid, 0.10 tracks, 0.40/0.15 vias, rule areas and locked copper kept), GND skipped (t-0012) | reliefs 1–4 (§9.2) | 0 conflicts at round 30: 815ca29, every net but GND routed, GND in 37 pieces |
| `v4_route_fix.py --nets GND --ripup 4` with the pours filled and read as copper (t-0014) | 815ca29's routing plus the tab and the VSS vias | 37 → 15 GND pieces; the last 14 sat in the power corner and under U2, boxed in on both layers by the other nets. GND cannot be added afterwards at this density; it has to be routed with the rest |
| `v4_route_pf.py` with GND as one live net: warm start on 815ca29, then `--fresh` | same | did not converge: 13 nets in conflict after 35 rounds, 15 after 21 |
| `v4_route_pf.py --fresh --skip GND` with the 28 GND pads the pours cannot reach renamed to one net `GND_T` (`v4_gnd_split.py`) | fresh build | 15 nets in conflict after 30 rounds: one GND tree across the island fights like the net itself |
| `v4_route_pf.py --fresh --skip GND`, nothing renamed | fresh build with the tab | 0 conflicts at round 39, but GND then in 33 pieces that neither the finisher nor `v4_stitch.py` could join: the routed nets leave no GND corridors |
| `v4_route_pf.py --fresh --skip GND --rounds 80` with those GND pads in three regional nets, `GND_A` (west stack and U1's north pads), `GND_B` (power corner and north row) and `GND_C` (R19, R21, R28, C15) | reliefs 1–4 | 7 nets in conflict after 70 rounds (h1) |
| same | relief 5 without the Q3/R15 turn and the VCAP1 pre-route | 10 nets in conflict after 80 rounds, six knots (h3) |
| same | relief 5 complete | 8 nets in conflict after 80 rounds, six knots (h5): AFE_EN_HW/CHG_MON on B at (8.3–8.7, 25.1–25.5), AFE_DRDY/AFE_MOSI on F at (11.0–11.4, 30.2–30.5), AFE_VIN/VBAT on B at (10.6–10.9, 20.0–20.3), CHG_MON/VBUS_DET on B at (10.3–10.6, 26.4–26.7), AFE_EN_HW/AFE_VIN on B at (8.0–8.3, 19.5–19.8), GND_B/CHG_MON on F at (10.5, 17.5) |
| same with `--all-after 40` (every net re-routed each round from round 40) | as h3 | 12 nets in conflict after 60 rounds (h4) |
| same with `--rip-near h5_conf.json --radius 1.2` (every net with copper within 1.2 mm of a knot ripped and re-routed together) | h5 | 13 nets in conflict after 45 rounds (h6): a knot needs a placement change, not a third net moved |
| Finishing sequence (§9.5) on h3 and h5: `v4_route_fix.py --drop-drc --ripup 4` (drops the conflicting copper, reconnects every net, the GND groups included), GND names restored, refill, `--nets GND --ripup 4`, `v4_stitch.py`, again, `v4_thermal_stubs.py` | h3 → m, h5 → n | m: 0 DRC errors, 9 open (3 GND pieces, VBAT, VBUS_DET ×2, VCAP1, AFE_VIN, AFE_GATE). n: 0 DRC errors, 10 open (5 GND pieces, AFE_DRDY, AFE_VIN ×2, CHG_MON, VBUS_DET) |
| `v4_route_fix.py --ripup 12 --pen 6` on the unfilled m and n boards | m1, n1 | m: 4 signal opens left (VBAT, VBUS_DET ×2, VCAP1); n: 5 nets still open, AFE_EN_HW and CHG_MON trading places every round |
| `v4_route_fix.py --soft-fills --ripup 8 --pen 6` on the filled n board: a pour blocks only its own net, every other net routes through it as if unfilled (the pour yields on refill), then GND finisher, stitching, stubs | n | the same 10 open connections: the rip-up moves each blocker and finds no other home for it; on GND it rips eight ISET items four rounds running and reverts each time |

Freerouting stalled at this density: 0.10/0.10 rules, locked Contact copper, and B mostly keep-out (t-0012). The negotiated router lets nets share cells early and raises the price of shared cells each round until the nets separate; when nets still fight at round 80 the fight points at the placement. GND is the hard net: the pours reach only what the signal routing leaves open, so GND has to be in the negotiation from the start, but as one net it is too big to negotiate (it touches every part). Three regional GND nets was the best compromise found; the remaining knots are between signal nets in the two B corridors of the island.

### 9.2 Placement reliefs that made it route

1. **Via column at u 10.72 beside U1's east pads** (pads at u 10.14). R7 and R27 moved, R18/R20/R21 went to u 11.80, and R19 and Q2 were re-placed.
2. **Crossings removed:**
   - C9 and C10 swapped (VREFP and VCAP1 crossed).
   - R12 turned 180° (PRETERM needed a via).
   - R15 turned 180° (VBAT hops on F).
   - C14 and R19 turned.
3. **Q2_G cluster.** R16 and R17 moved beside Q2's gate.
4. **C14 turned so its VBAT pad faces east.** With the pad facing west, VBAT ran R14 → Q1 → C14 → R20 on B. That walls off AFE_VIN's path from U4 to C5 and Q1.3, so neither net could close without crossing the other.
5. **West stack 0.10 west, GND pads turned east, VCAP1 pre-routed (t-0014).** The west stack (R15, Q3, R14, Q1, C5) sits at u 9.85 (815ca29: 9.95) and R24 at 9.30 (9.40), as far west as R14's and Q1's courtyards clear LAND_P1 (`check_keepouts` in `build_v4.py`). C8, C14 and C11 are turned so their GND pads face east, under U2's exposed pad; the B corridor between the two stacks beside Q1 grows from 0.42 to 0.52 mm and carries no GND. Q3 and R15 are turned so GND and AFE_EN_HW face west, away from that corridor, and AFE_GATE east. VCAP1 (C10 to U2.11) is a locked F pre-route west of U2's west row, because every router put +3V0's hop from B across that line. Relief 4 is reversed: C14's VBAT pad faces west again, one hop from Q1.2; with C14's GND pad east it no longer walls off AFE_VIN.

### 9.3 Thermal connections (the starved-thermal decision)

DRC's starved-thermal check stays at KiCad's default: a GND pad with a thermal relief needs two spokes. No `min_resolved_spokes` rule; that would be a waiver, and the r12 review asked for zero errors under the project rules.

- **Exposed pads and mounting pads connect solid** (`elicio-v4.kicad_dru`, rule "GND exposed and mounting pads solid"): U2 pad 33, U4 pad 5, U5 pad 5 and J2's two MP pads. They are reflowed, not hand-soldered, sit under their part and want the copper. A relief has no job there.
- **Reliefs stay on every 0201 and 0402 pad** so nothing tombstones.
- **Second connections are copper:** where the pour reaches a pad from one side only (its other sides are 0.10 routing), a 0.10 GND track runs from inside the pad through the 0.15 thermal gap into the pour, placed by `v4_thermal_stubs.py` and checked by DRC like any track. 9 such tracks:
  - C5.2 B.Cu: stub (9.300, 23.850) -> (9.100, 23.875) 0.202 mm
  - U1.14 F.Cu: stub (6.550, 28.600) -> (6.550, 28.825) 0.225 mm
  - C13.2 B.Cu: stub (4.150, 18.500) -> (4.125, 18.700) 0.202 mm
  - U1.18 F.Cu: stub (6.550, 29.500) -> (6.550, 29.275) 0.225 mm
  - R24.2 B.Cu: stub (8.850, 24.450) -> (8.825, 24.250) 0.202 mm
  - U2.10 F.Cu: stub (10.200, 21.050) -> (10.400, 21.050) 0.200 mm
  - U2.13 F.Cu: stub (10.200, 22.250) -> (10.400, 22.250) 0.200 mm
  - U2.24 F.Cu: stub (13.175, 23.750) -> (13.100, 23.550) 0.214 mm
  - R28.2 F.Cu: stub (13.250, 27.150) -> (13.225, 26.950) 0.202 mm

No Contact, creepage or clearance rule changed; the three Q84 rules are as in v2.

### 9.4 Open connections

10 connections are open (5 GND, 2 AFE_VIN, 1 AFE_DRDY, 1 CHG_MON, 1 VBUS_DET). Each row is one piece that does not reach its net's main piece, the copper it would have to reach, and the straight-line gap between them on the layer named (0.10 track plus clearance needs 0.30 of free width, so a 0.4 mm gap holds one foreign track):

| Net | Open piece | Nearest main copper | Layer | Gap mm |
|---|---|---|---|---:|
| AFE_DRDY | U1.46 | F track (11.38, 30.40)–(11.35, 30.40) of the main piece (50 items) | F | 0.47 |
| AFE_VIN | B tracks only, u 8.30–10.62 × s 19.50–19.93 | B track (8.00, 19.82)–(7.97, 19.80) of the main piece (18 items) | B | 0.34 |
| AFE_VIN | U4.3, U4.4 | Q1.3 of the main piece (18 items) | B | 1.50 |
| CHG_MON | U1.44 | B track (8.07, 25.00)–(8.10, 25.02) of the main piece (101 items) | B | 0.54 |
| GND | U2.10, U2.13, U2.24, U2.33 | F pour u 6.6–13.8 × s 16.9–22.2 of the main piece (310 items) | F | 0.35 |
| GND | P5 | U3.C2 of the main piece (310 items) | B | 0.37 |
| GND | U4.2, U4.5 | B pour u 11.1–13.7 × s 18.9–20.6 of the main piece (310 items) | B | 0.41 |
| GND | C14.2, C8.2 | B pour u 14.7–15.8 × s 19.8–25.1 of the main piece (310 items) | B | 0.40 |
| GND | C11.2 | B pour u 9.9–10.9 × s 23.5–25.1 of the main piece (310 items) | B | 0.87 |
| VBUS_DET | R19.1, R18.2 | B track (10.25, 26.68)–(10.22, 27.35) of the main piece (16 items) | B | 0.34 |

Where they sit and what is in the way (measured on the committed board with `v4_pieces.py` and the finisher's grid):

- **GND inside U2's pad ring (the F pour with the exposed pad and pads 10, 13, 24):** 0.35 mm from U2.13 to the main F pour west of it, with +3V0's F track (eight segments along U2's west row) between. A via from the exposed pad to the B pour underneath has 578 candidate cells; every one is inside the clearance of +3V0's B track in the corridor, of C8.1 or C14.1 (+3V0 and VBAT on B) or of U2's own west-row pads.
- **GND islands on B under U2 (U4.2 with U4.5; C8.2 with C14.2; C11.2 alone):** 0.41 mm from U4.5 to the main B pour north of it across U4.1 (+3V0) and its track; 0.40 mm from the C8/C14 island's east edge to the east B pour across VBUS's track at u 14.5; 0.87 mm from C11.2 to the pour west of it across +3V0's B track and C11.1. No F pour lies over any of them (U2's pads and exposed pad are above), so no via can join them.
- **GND in the north-east corner (the P5 charge run's B island, u 12.55–15.1 × s 16.3–18.15):** 0.37 mm from U3.C2 across ISET's track from C2.1 to U3.B2, which has to pass north of U3.C2 because the 0.4 mm ball pitch leaves no other way to B2. 103 cells of the island lie under the main F pour; all are inside the clearance of ISET (B) or AFE_IN1P (F).
- **AFE_VIN (U4.3/U4.4 to Q1.3 and C5.1), two gaps on B:** 0.39 mm at (8.0–8.3, 19.5–19.8) across AFE_EN_HW's track (R15.2 and Q3.1 down to U1), and the corridor crossing from U4's pads to Q1.3, 1.50 mm across VBAT's pad and track, AFE_GATE's track and the GND pour. SOT-883 puts pins 1 and 2 on one side and 3 on the other, so Q1 and Q3 each force AFE_VIN to cross VBAT or AFE_GATE locally.
- **CHG_MON (U1.44 to R20/R21):** 0.59 mm on B at (8.1–8.7, 25.0–25.25) across AFE_EN_HW's track.
- **VBUS_DET (R18.2/R19.1 to U1):** 0.39 mm on B at (10.25–10.57, 26.4–26.7) across CHG_MON's track. CHG_MON, VBUS_DET, AFE_DRDY and VBAT_SENSE leave U1's east pads on F, drop to B in one via column at u 10.6–10.8 and fan out east to R18/R20/R21, R19 and Q2; the last two to arrive cross.
- **AFE_DRDY (U1.46 to R27):** 0.52 mm on F at (11.0–11.35, 29.95–30.40) across AFE_MOSI's track and pad. The four SPI_AFE lines run on F from U1 to U2's south row at u 10.4–12.5, AFE_DRDY has to cross one of them, and the B side below is inside LAND_P2's via ban.

+3V0 is in the way of three of the five GND pieces and AFE_EN_HW of two signal opens; the rest are ISET, VBUS, CHG_MON, AFE_MOSI and VBAT. The finisher's rip-up (up to 12 rounds, with and without the pours as obstacles) moves the blocker and finds no other home for it: both layers of both corridors are full.

What would close it, cheapest first; none is tried:

1. **Locked pre-routes for the two common blockers, then a fresh route** (one router run plus `v4_finish.sh`, about two hours): +3V0 from U4.1 over C8.1 to U2's supply pads on B, kept east of the corridor, and U1's supply from the F side; AFE_EN_HW from Q3.1 to a via at about (9.0, 21.0), just outside LAND_P1, then on F across the P1 landing (tracks are allowed there) to U1's pad.
2. **Placement:** R18, R20, R21 and R19 one row further east (u 12.4 and beyond) so U1's east pads get a second via column; Q1 turned so AFE_VIN's pin faces U4; C11 moved out from under U2 so the B pour can reach C8/C14 from the south. Then a fresh route.
3. **Rules:** 0.075 track and clearance in the two corridors only would give each one more track. JLC's floor for two-layer flex is 0.10/0.10 (§3.2), so this needs their confirmation first, and no vendor contact was allowed in this lane.
4. **A third copper layer:** closes it for certain and changes the stack-up and the thickness chain (§1.2).

### 9.5 Rebuild and re-route

The committed board came from this sequence (scratch copies in `$W`; DRC needs `<stem>.kicad_pro`, `.kicad_dru` and `.kicad_sch` beside each copy; one router or KiCad batch at a time):

```bash
cd hardware/board
KP=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3
PY=../../.venv/bin/python
python3 gen_v4_sch.py                                   # schematic and project (netclasses); ERC must be clean
$KP build_v4.py --out $W/new.kicad_pcb                  # placed board, locked pre-routes, pour outlines (no fill); "keep-out problems 0"
$PY v4_gnd_split.py $W/new.kicad_pcb $W/news.kicad_pcb \
    GND_A:C5.2,C6.2,C7.2,C9.2,C10.2,Q3.2,R23.2,R24.2,U1.1,U1.7 \
    GND_B:C2.2,C3.2,C4.2,D1.2,J2.2,R11.2,R12.2,R13.2,U3.C2 \
    GND_C:C15.2,R19.2,R21.2,R28.2
$PY -u v4_route_pf.py --pcb $W/news.kicad_pcb --out $W/h.kicad_pcb --fresh --skip GND --rounds 80 --debug $W/h_conf.json
kicad-cli pcb drc --format json -o $W/h0_drc.json $W/h.kicad_pcb
$PY -u v4_route_fix.py --pcb $W/h.kicad_pcb --drop-drc $W/h0_drc.json --ripup 4 --out $W/h1.kicad_pcb
$PY v4_gnd_split.py --back $W/h1.kicad_pcb $W/h2.kicad_pcb
kicad-cli pcb drc --refill-zones --save-board --format json -o $W/h2_drc.json $W/h2.kicad_pcb
$PY -u v4_route_fix.py --pcb $W/h2.kicad_pcb --nets GND --ripup 4 --out $W/h3.kicad_pcb
$PY v4_stitch.py $W/h3.kicad_pcb GND $W/h4.kicad_pcb 1.5
kicad-cli pcb drc --refill-zones --save-board --format json -o $W/h4_drc.json $W/h4.kicad_pcb
$PY -u v4_route_fix.py --pcb $W/h4.kicad_pcb --nets GND --ripup 4 --out $W/h5.kicad_pcb
$PY v4_stitch.py $W/h5.kicad_pcb GND $W/h6.kicad_pcb 1.5
kicad-cli pcb drc --refill-zones --save-board --format json -o $W/h6_drc.json $W/h6.kicad_pcb
$PY v4_thermal_stubs.py $W/h6.kicad_pcb $W/h6_drc.json $W/h7.kicad_pcb 0.8
kicad-cli pcb drc --refill-zones --save-board --format json --schematic-parity -o $W/h7_drc.json $W/h7.kicad_pcb
# while connections stay open: the soft-fill finisher, then GND again
$PY -u v4_route_fix.py --pcb $W/h7.kicad_pcb --soft-fills --ripup 8 --pen 6 --out $W/p1.kicad_pcb
kicad-cli pcb drc --refill-zones --save-board --format json -o $W/p1_drc.json $W/p1.kicad_pcb
$PY -u v4_route_fix.py --pcb $W/p1.kicad_pcb --soft-fills --nets GND --ripup 4 --pen 6 --out $W/p2.kicad_pcb
$PY v4_stitch.py $W/p2.kicad_pcb GND $W/p3.kicad_pcb 1.5
kicad-cli pcb drc --refill-zones --save-board --format json -o $W/p3_drc.json $W/p3.kicad_pcb
$PY v4_thermal_stubs.py $W/p3.kicad_pcb $W/p3_drc.json $W/p4.kicad_pcb 0.8
kicad-cli pcb drc --refill-zones --save-board --format json --schematic-parity -o $W/p4_drc.json $W/p4.kicad_pcb
cp $W/p4.kicad_pcb elicio-v4.kicad_pcb                  # saved with filled zones
cd ../.. && .venv/bin/python -m unittest discover -s tests -q && .venv/bin/python scripts/board/release.py --board elicio-v4 --routed
```

`hardware/board/v4_finish.sh` runs the part after the router. `build_v4.py` overwrites the PCB, routing included, so route in scratch copies. `v4_pieces.py PCB NET` lists a net's pieces with their gaps. Freerouting instead: `scripts/board/route_v4.py --work DIR --route`, one run at a time, `-Xmx4g`.

## 10. Flat and folded tables

### 10.1 Flat PCB coordinates (u, s)

From `python3 hardware/board/v4_tables.py --pads` on the committed board. Part centres, then pad by pad for the connectors, rings, J4 and SW1. The Gerber carries these (PCB x, y = u, s).

| ref | side | x (u) | y (s) | rot | footprint |
|---|---|---:|---:|---:|---|
| C1 | bottom | 13.30 | 23.65 | 90 | `Capacitor_SMD:C_0201_0603Metric` |
| C2 | bottom | 11.95 | 17.55 | 180 | `Capacitor_SMD:C_0201_0603Metric` |
| C3 | bottom | 14.40 | 19.95 | 90 | `Capacitor_SMD:C_0201_0603Metric` |
| C4 | bottom | 7.25 | 17.45 | 180 | `Capacitor_SMD:C_0201_0603Metric` |
| C5 | bottom | 9.85 | 23.75 | 180 | `Capacitor_SMD:C_0201_0603Metric` |
| C6 | top | 7.75 | 22.66 | 90 | `Capacitor_SMD:C_0402_1005Metric` |
| C7 | top | 8.78 | 22.66 | 90 | `Capacitor_SMD:C_0201_0603Metric` |
| C8 | bottom | 11.65 | 22.55 | 0 | `Capacitor_SMD:C_0402_1005Metric` |
| C9 | top | 10.20 | 18.50 | 90 | `Capacitor_SMD:C_0402_1005Metric` |
| C10 | top | 9.10 | 18.60 | 90 | `Capacitor_SMD:C_0201_0603Metric` |
| C11 | bottom | 11.65 | 24.60 | 0 | `Capacitor_SMD:C_0201_0603Metric` |
| C12 | bottom | 3.10 | 18.30 | 180 | `Capacitor_SMD:C_0201_0603Metric` |
| C13 | bottom | 4.60 | 18.30 | 180 | `Capacitor_SMD:C_0201_0603Metric` |
| C14 | bottom | 11.65 | 23.60 | 0 | `Capacitor_SMD:C_0402_1005Metric` |
| C15 | top | 13.60 | 25.15 | 0 | `Capacitor_SMD:C_0201_0603Metric` |
| C16 | bottom | 4.70 | 17.15 | 90 | `Capacitor_SMD:C_0201_0603Metric` |
| D1 | bottom | 12.60 | 19.70 | 180 | `Diode_SMD:D_SOD-523` |
| D2 | top | 14.65 | 26.10 | 0 | `LED_SMD:LED_0402_1005Metric` |
| J2 | top | 5.45 | 18.90 | -90 | `Connector_Molex:Molex_Pico-EZmate_Slim_202656-0021_1x02-1MP_P1.20mm_Vertical` |
| J3 | top | 22.40 | 19.40 | 0 | `Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Horizontal` |
| J4 | top | 10.00 | 35.40 | 0 | `Connector:Tag-Connect_TC2030-IDC-NL_2x03_P1.27mm_Vertical` |
| P1 | top | 5.90 | 5.29 | 0 | `elicio:RING_PAD_D5_H2.7` |
| P2 | top | 10.40 | -5.81 | 0 | `elicio:RING_PAD_D5_H2.7` |
| P3 | top | 8.50 | 43.00 | 0 | `elicio:RING_PAD_D5_H2.7` |
| P4 | bottom | 16.51 | 4.35 | 180 | `elicio:RING_1S_D4.6_NPTH2.7` |
| P5 | bottom | 16.51 | 12.10 | 180 | `elicio:RING_1S_D4.6_NPTH2.7` |
| Q1 | bottom | 9.85 | 22.80 | 180 | `Package_TO_SOT_SMD:SOT-883` |
| Q2 | bottom | 13.35 | 27.60 | 180 | `Package_TO_SOT_SMD:SOT-883` |
| Q3 | bottom | 9.85 | 20.90 | 0 | `Package_TO_SOT_SMD:SOT-883` |
| Q4 | top | 14.60 | 28.00 | 0 | `Package_TO_SOT_SMD:SOT-883` |
| R1 | bottom | 5.90 | 17.30 | -90 | `Resistor_SMD:R_0402_1005Metric` |
| R2 | bottom | 9.39 | 17.25 | 180 | `Resistor_SMD:R_0402_1005Metric` |
| R3 | bottom | 14.55 | 25.60 | 180 | `Resistor_SMD:R_0402_1005Metric` |
| R4 | bottom | 13.30 | 22.15 | 90 | `Resistor_SMD:R_0201_0603Metric` |
| R5 | top | 11.40 | 31.12 | 90 | `Resistor_SMD:R_0201_0603Metric` |
| R6 | top | 11.40 | 29.63 | 90 | `Resistor_SMD:R_0201_0603Metric` |
| R7 | top | 11.05 | 25.50 | 90 | `Resistor_SMD:R_0201_0603Metric` |
| R8 | top | 11.40 | 32.61 | 90 | `Resistor_SMD:R_0201_0603Metric` |
| R11 | bottom | 12.00 | 16.75 | 180 | `Resistor_SMD:R_0201_0603Metric` |
| R12 | top | 12.60 | 18.15 | 180 | `Resistor_SMD:R_0201_0603Metric` |
| R13 | top | 12.60 | 18.95 | 0 | `Resistor_SMD:R_0201_0603Metric` |
| R14 | bottom | 9.85 | 21.85 | 180 | `Resistor_SMD:R_0201_0603Metric` |
| R15 | bottom | 9.85 | 19.95 | 180 | `Resistor_SMD:R_0201_0603Metric` |
| R16 | bottom | 14.60 | 27.10 | -90 | `Resistor_SMD:R_0201_0603Metric` |
| R17 | bottom | 14.60 | 28.55 | -90 | `Resistor_SMD:R_0201_0603Metric` |
| R18 | bottom | 11.80 | 25.60 | 180 | `Resistor_SMD:R_0201_0603Metric` |
| R19 | bottom | 13.30 | 26.52 | 0 | `Resistor_SMD:R_0201_0603Metric` |
| R20 | bottom | 11.80 | 26.40 | 180 | `Resistor_SMD:R_0201_0603Metric` |
| R21 | bottom | 11.80 | 27.20 | 180 | `Resistor_SMD:R_0201_0603Metric` |
| R22 | top | 14.60 | 27.02 | 180 | `Resistor_SMD:R_0201_0603Metric` |
| R23 | top | 7.95 | 24.10 | 180 | `Resistor_SMD:R_0201_0603Metric` |
| R24 | bottom | 9.30 | 24.65 | 180 | `Resistor_SMD:R_0201_0603Metric` |
| R25 | bottom | 11.95 | 18.35 | 180 | `Resistor_SMD:R_0201_0603Metric` |
| R27 | top | 12.45 | 25.50 | -90 | `Resistor_SMD:R_0201_0603Metric` |
| R28 | top | 13.35 | 27.70 | 90 | `Resistor_SMD:R_0201_0603Metric` |
| R31 | top | 22.40 | 16.80 | 0 | `Resistor_SMD:R_0402_1005Metric` |
| R32 | top | 18.00 | 21.15 | 0 | `Resistor_SMD:R_0402_1005Metric` |
| R33 | top | 22.40 | 27.10 | 0 | `Resistor_SMD:R_0402_1005Metric` |
| SW1 | top | 14.45 | 31.10 | 180 | `elicio:SW_HRO_1TS015A` |
| U1 | top | 6.45 | 29.05 | -90 | `elicio:InsightSiP_ISP1807` |
| U2 | top | 11.85 | 22.08 | -90 | `elicio:Texas_RSM0032` |
| U3 | bottom | 13.90 | 17.75 | 90 | `elicio:Texas_YFP0006_V4` |
| U4 | bottom | 11.65 | 21.25 | 180 | `Package_SON:Texas_X2SON-4_1x1mm_P0.65mm` |
| U5 | bottom | 3.30 | 17.10 | 180 | `Package_SON:Texas_X2SON-4_1x1mm_P0.65mm` |

| pad | kind | net | x (u) | y (s) |
|---|---|---|---:|---:|
| J2.1 | smd | VBAT | 7.45 | 18.30 |
| J2.2 | smd | GND | 7.45 | 19.50 |
| J2.MP | smd | GND | 3.42 | 17.00 |
| J2.MP | smd | GND | 3.42 | 20.80 |
| J3.1 | thru_hole | BENCH_SIG1 | 22.40 | 19.40 |
| J3.2 | thru_hole | BENCH_SIG2 | 22.40 | 21.94 |
| J3.3 | thru_hole | BENCH_REF | 22.40 | 24.48 |
| J4.1 | connect | +VDD | 8.73 | 36.03 |
| J4.2 | connect | SWDIO | 8.73 | 34.77 |
| J4.3 | connect | GND | 10.00 | 36.03 |
| J4.4 | connect | SWDCLK | 10.00 | 34.77 |
| J4.5 | connect | GND | 11.27 | 36.03 |
| J4.6 | connect | nRESET | 11.27 | 34.77 |
| P1.1 | thru_hole | SIG1 | 5.90 | 5.29 |
| P2.1 | thru_hole | SIG2 | 10.40 | -5.81 |
| P3.1 | thru_hole | REF | 8.50 | 43.00 |
| P4.1 | smd | VBUS | 14.59 | 4.35 |
| P5.1 | smd | GND | 14.59 | 12.10 |
| SW1.1 | smd | nRESET | 14.45 | 32.73 |
| SW1.2 | smd | GND | 14.45 | 29.48 |

### 10.2 Folded shell sites (u, s, y)

From `python3 hardware/board/v4_tables.py --folded` on the committed board. Shell u, s = flat u, s for everything that stays flat (the island and its parts); y comes from the thickness chain (§1.2) and the fold math (§4.4). Courtyards are line-centre boxes from the footprint text (the drawn line is 0.05 wide). The v4 target body is the r9 shell (branch `hp/elicio/t-0001-finish-the-earpiece-shell-v2f-wp14f-from`, 252afbb, not merged) with §7's changes on paper: walls u 1.5/16.5, floor 1.5, LID_Y 7.1, rib s 14.9–15.7 (y ≤ 4.5), bay s 15.7–38.2, EMG hex collars AF 8.4 (top y 3.5) at the P1/P2 sites, standoff landings R 3.2, lid posts Ø2.0, r9's SIG fold pockets and REF end-wall slot. Margins are in mm; a row passes when every margin is ≥ 0. F parts stand on the island top (y 5.12) under the lid; B parts hang from the island underside (y 5.01) over the collar top (3.5) where a collar box is below them, else over the floor (1.5). Heights are maxima from the sources in the table; the ones marked UNVERIFIED are package maxima (§11.1). The P2 lid post on U1 is by design (§5.3).

#### Courtyards on the island (flat u, s = shell u, s; y from the fold math)

| ref | side | courtyard u | courtyard s | h (source) | y | wall u | rib/end s | lid or floor y | lid post | landing | test |
|---|---|---:|---:|---|---|---:|---:|---:|---:|---:|---|
| C1 | bottom | 12.95-13.65 | 22.95-24.35 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 2.85 | 7.25 | 3.16 (floor) | - | 3.91 | ok |
| C2 | bottom | 11.25-12.65 | 17.20-17.90 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 3.85 | 1.50 | 3.16 (floor) | - | 3.54 | ok |
| C3 | bottom | 14.05-14.75 | 19.25-20.65 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 1.75 | 3.55 | 3.16 (floor) | - | 5.06 | ok |
| C4 | bottom | 6.55-7.95 | 17.10-17.80 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 5.05 | 1.40 | 1.16 (collar) | - | 1.05 | ok |
| C5 | bottom | 9.15-10.55 | 23.40-24.10 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 5.95 | 7.70 | 1.16 (collar) | - | 0.34 | ok |
| C6 | top | 7.29-8.21 | 21.75-23.57 | 0.60 (0402 C max, UNVERIFIED) | 5.12-5.72 | 5.79 | 6.05 | 1.38 (lid) | 0.39 | - | ok |
| C7 | top | 8.43-9.13 | 21.96-23.36 | 0.35 (0201 max, UNVERIFIED) | 5.12-5.47 | 6.93 | 6.26 | 1.63 (lid) | 1.53 | - | ok |
| C8 | bottom | 10.74-12.56 | 22.09-23.01 | 0.60 (0402 C max, UNVERIFIED) | 4.41-5.01 | 3.94 | 6.39 | 2.91 (floor) | - | 1.64 | ok |
| C9 | top | 9.74-10.66 | 17.59-19.41 | 0.60 (0402 C max, UNVERIFIED) | 5.12-5.72 | 5.84 | 1.89 | 1.38 (lid) | 4.26 | - | ok |
| C10 | top | 8.75-9.45 | 17.90-19.30 | 0.35 (0201 max, UNVERIFIED) | 5.12-5.47 | 7.05 | 2.20 | 1.63 (lid) | 3.67 | - | ok |
| C11 | bottom | 10.95-12.35 | 24.25-24.95 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 4.15 | 8.55 | 3.16 (floor) | - | 2.33 | ok |
| C12 | bottom | 2.40-3.80 | 17.95-18.65 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 0.90 | 2.25 | 1.16 (collar) | - | 0.75 | ok |
| C13 | bottom | 3.90-5.30 | 17.95-18.65 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 2.40 | 2.25 | 1.16 (collar) | - | 0.20 | ok |
| C14 | bottom | 10.74-12.56 | 23.14-24.06 | 0.60 (0402 C max, UNVERIFIED) | 4.41-5.01 | 3.94 | 7.44 | 2.91 (floor) | - | 1.77 | ok |
| C15 | top | 12.90-14.30 | 24.80-25.50 | 0.35 (0201 max, UNVERIFIED) | 5.12-5.47 | 2.20 | 9.10 | 1.63 (lid) | 6.23 | - | ok |
| C16 | bottom | 4.35-5.05 | 16.45-17.85 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 2.85 | 0.75 | 1.16 (collar) | - | 1.04 | ok |
| D1 | bottom | 11.35-13.85 | 19.00-20.40 | 0.80 (SOD-523 max, UNVERIFIED) | 4.21-5.01 | 2.65 | 3.30 | 2.71 (floor) | - | 2.48 | ok |
| D2 | top | 13.72-15.58 | 25.63-26.57 | 0.55 (0402 LED, UNVERIFIED) | 5.12-5.67 | 0.92 | 9.93 | 1.43 (lid) | 6.02 | - | ok |
| J2 | top | 2.34-8.38 | 16.15-21.65 | 1.20 (§1.2 mated) | 5.12-6.32 | 0.84 | 0.45 | 0.78 (lid) | 0.35 | - | ok |
| J3 | top | 20.63-32.94 | 17.63-26.25 | 0.00 (no height: UNVERIFIED) | cut off with the tab (Q91) | - | - | - | - | - | exterior |
| J4 | top | 6.50-13.50 | 33.40-37.40 | 0.00 (pads only) | 5.12-5.12 | 3.00 | 0.80 | 1.98 (lid) | 0.30 | - | ok |
| Q1 | bottom | 9.15-10.55 | 22.30-23.30 | 0.40 (DFN1006 max, UNVERIFIED) | 4.61-5.01 | 5.95 | 6.60 | 1.11 (collar) | - | 0.06 | ok |
| Q2 | bottom | 12.65-14.05 | 27.10-28.10 | 0.40 (DFN1006 max, UNVERIFIED) | 4.61-5.01 | 2.45 | 10.10 | 3.11 (floor) | - | 2.28 | ok |
| Q3 | bottom | 9.15-10.55 | 20.40-21.40 | 0.40 (DFN1006 max, UNVERIFIED) | 4.61-5.01 | 5.95 | 4.70 | 1.11 (collar) | - | 0.10 | ok |
| Q4 | top | 13.90-15.30 | 27.50-28.50 | 0.40 (DFN1006 max, UNVERIFIED) | 5.12-5.52 | 1.20 | 9.70 | 1.58 (lid) | 4.76 | - | ok |
| R1 | bottom | 5.43-6.37 | 16.37-18.23 | 0.45 (0402 R max, UNVERIFIED) | 4.56-5.01 | 3.93 | 0.67 | 1.06 (collar) | - | 0.57 | ok |
| R2 | bottom | 8.46-10.32 | 16.78-17.72 | 0.45 (0402 R max, UNVERIFIED) | 4.56-5.01 | 6.18 | 1.08 | 1.06 (collar) | - | 1.79 | ok |
| R3 | bottom | 13.62-15.48 | 25.13-26.07 | 0.45 (0402 R max, UNVERIFIED) | 4.56-5.01 | 1.02 | 9.43 | 3.06 (floor) | - | 4.53 | ok |
| R4 | bottom | 12.95-13.65 | 21.45-22.85 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 2.85 | 5.75 | 3.16 (floor) | - | 3.85 | ok |
| R5 | top | 11.05-11.75 | 30.42-31.82 | 0.35 (0201 max, UNVERIFIED) | 5.12-5.47 | 4.75 | 6.38 | 1.63 (lid) | 0.67 | - | ok |
| R6 | top | 11.05-11.75 | 28.93-30.33 | 0.35 (0201 max, UNVERIFIED) | 5.12-5.47 | 4.75 | 7.87 | 1.63 (lid) | 1.42 | - | ok |
| R7 | top | 10.70-11.40 | 24.80-26.20 | 0.35 (0201 max, UNVERIFIED) | 5.12-5.47 | 5.10 | 9.10 | 1.63 (lid) | 4.13 | - | ok |
| R8 | top | 11.05-11.75 | 31.91-33.31 | 0.35 (0201 max, UNVERIFIED) | 5.12-5.47 | 4.75 | 4.89 | 1.63 (lid) | 0.65 | - | ok |
| R11 | bottom | 11.30-12.70 | 16.40-17.10 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 3.80 | 0.70 | 3.16 (floor) | - | 4.09 | ok |
| R12 | top | 11.90-13.30 | 17.80-18.50 | 0.35 (0201 max, UNVERIFIED) | 5.12-5.47 | 3.20 | 2.10 | 1.63 (lid) | 6.50 | - | ok |
| R13 | top | 11.90-13.30 | 18.60-19.30 | 0.35 (0201 max, UNVERIFIED) | 5.12-5.47 | 3.20 | 2.90 | 1.63 (lid) | 6.05 | - | ok |
| R14 | bottom | 9.15-10.55 | 21.50-22.20 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 5.95 | 5.80 | 1.16 (collar) | - | 0.05 | ok |
| R15 | bottom | 9.15-10.55 | 19.60-20.30 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 5.95 | 3.90 | 1.16 (collar) | - | 0.47 | ok |
| R16 | bottom | 14.25-14.95 | 26.40-27.80 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 1.55 | 10.40 | 3.16 (floor) | - | 3.35 | ok |
| R17 | bottom | 14.25-14.95 | 27.85-29.25 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 1.55 | 8.95 | 1.16 (collar) | - | 2.24 | ok |
| R18 | bottom | 11.10-12.50 | 25.25-25.95 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 4.00 | 9.55 | 3.16 (floor) | - | 2.93 | ok |
| R19 | bottom | 12.60-14.00 | 26.17-26.87 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 2.50 | 10.47 | 3.16 (floor) | - | 3.41 | ok |
| R20 | bottom | 11.10-12.50 | 26.05-26.75 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 4.00 | 10.35 | 3.16 (floor) | - | 3.19 | ok |
| R21 | bottom | 11.10-12.50 | 26.85-27.55 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 4.00 | 10.65 | 3.16 (floor) | - | 2.39 | ok |
| R22 | top | 13.90-15.30 | 26.67-27.37 | 0.35 (0201 max, UNVERIFIED) | 5.12-5.47 | 1.20 | 10.83 | 1.63 (lid) | 5.53 | - | ok |
| R23 | top | 7.25-8.65 | 23.75-24.45 | 0.35 (0201 max, UNVERIFIED) | 5.12-5.47 | 5.75 | 8.05 | 1.63 (lid) | 0.54 | - | ok |
| R24 | bottom | 8.60-10.00 | 24.30-25.00 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 6.50 | 8.60 | 1.16 (collar) | - | 0.35 | ok |
| R25 | bottom | 11.25-12.65 | 18.00-18.70 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 3.85 | 2.30 | 3.16 (floor) | - | 3.09 | ok |
| R27 | top | 12.10-12.80 | 24.80-26.20 | 0.35 (0201 max, UNVERIFIED) | 5.12-5.47 | 3.70 | 9.10 | 1.63 (lid) | 5.46 | - | ok |
| R28 | top | 13.00-13.70 | 27.00-28.40 | 0.35 (0201 max, UNVERIFIED) | 5.12-5.47 | 2.80 | 9.80 | 1.63 (lid) | 4.16 | - | ok |
| R31 | top | 21.47-23.33 | 16.33-17.27 | 0.45 (0402 R max, UNVERIFIED) | cut off with the tab (Q91) | - | - | - | - | - | exterior |
| R32 | top | 17.07-18.93 | 20.68-21.62 | 0.45 (0402 R max, UNVERIFIED) | cut off with the tab (Q91) | - | - | - | - | - | exterior |
| R33 | top | 21.47-23.33 | 26.63-27.57 | 0.45 (0402 R max, UNVERIFIED) | cut off with the tab (Q91) | - | - | - | - | - | exterior |
| SW1 | top | 13.20-15.70 | 28.95-33.25 | 0.60 (§1.2) | 5.12-5.72 | 0.80 | 4.95 | 1.38 (lid) | 2.80 | - | ok |
| U1 | top | 2.20-10.70 | 24.80-33.30 | 1.00 (§1.2) | 5.12-6.12 | 0.70 | 4.90 | 0.98 (lid) | -1.00 (post on the part) | - | ok |
| U2 | top | 9.22-14.48 | 19.45-24.71 | 1.00 (TI RSM) | 5.12-6.12 | 2.02 | 3.75 | 0.98 (lid) | 2.32 | - | ok |
| U3 | bottom | 12.84-14.96 | 16.95-18.55 | 0.63 (TI YFP, UNVERIFIED) | 4.38-5.01 | 1.54 | 1.25 | 2.88 (floor) | - | 4.55 | ok |
| U4 | bottom | 10.74-12.56 | 20.50-22.00 | 0.40 (TI DQN) | 4.61-5.01 | 3.94 | 4.80 | 3.11 (floor) | - | 1.64 | ok |
| U5 | bottom | 2.39-4.21 | 16.35-17.85 | 0.40 (TI DQN) | 4.61-5.01 | 0.89 | 0.65 | 1.11 (collar) | - | 1.28 | ok |

Smallest courtyard margin: 0.45 mm.

#### Rings, strip roots and tab roots

| item | flat (u, s) | folded site (u, s, y) | body feature | margin | test |
|---|---|---|---|---|---|
| P1 ring (SIG1) | (5.90, 5.29) | (5.90, 22.00), floor 1.50-1.81 under the P1 standoff | standoff R 3.2 landing under the island | site as §4.5 | ok |
| SIG1 root | u 4.65-7.15 at s 16.00 | 180° fold R 1.5 under the island, stand-out to s 14.40, drop 3.31 | r9 fold pocket u 4.15-7.65 × s 14.40-16.00 × 3.00 tall (decision 74) | u 0.50 each side, s 0.00 at the island, stand-out 0.00 | ok |
| P2 ring (SIG2) | (10.40, -5.81) | (10.40, 33.10), floor 1.50-1.81 under the P2 standoff | standoff R 3.2 landing under the island | site as §4.5 | ok |
| SIG2 root | u 9.15-11.65 at s 16.00 | 180° fold R 1.5 under the island, stand-out to s 14.40, drop 3.31 | r9 fold pocket u 8.65-12.15 × s 14.40-16.00 × 3.00 tall (decision 74) | u 0.50 each side, s 0.00 at the island, stand-out 0.00 | ok |
| P3 ring (REF) | (8.50, 43.00) | (8.50, 43.00), floor 1.50-1.81 in the REF pocket | REF pocket Ø7.5 | site as §4.5 | ok |
| REF root | u 7.25-9.75 at s 37.60 | drops 3.20 to the floor in the 0.60 gap before the end wall (bare PI, v2 geometry) | r9 end-wall slot u 7.05-9.95 × s 38.20-39.25 × y 1.50-1.96 | u 0.20 each side, y 0.15 over the 0.31 ring stack | ok (drop UNVERIFIED) |
| P4 ring (VBUS) | (16.51, 4.35) | (16.245, 4.35, 4.295), copper on B facing the standoff | wall face u 16.19-16.50, standoff u 13.19-16.19 | plate y 1.695-6.895: lid 0.205, floor 0.195 | ok |
| P5 ring (GND) | (16.51, 12.10) | (16.245, 12.10, 4.295), copper on B facing the standoff | wall face u 16.19-16.50, standoff u 13.19-16.19 | plate y 1.695-6.895: lid 0.205, floor 0.195 | ok |
| P4/P5 joint root | u 15.09-16.904, s 16.30-19.30 | bend to u 16.30 (outer), y 3.80-5.12 | wall face 16.50; rib s 14.90-15.70 | wall 0.20 (FR4 side on the wall by design), rib 0.60 | ok |
| P4/P5 flap | u 16.904-19.114, s 14.85-19.30 | on the wall face, y 1.695-3.905 | crosses the rib s 14.90-15.70 (rib y 1.50-4.50) | none without a slot: cut the rib back 0.50 from the wall (u 16.00-16.50, full rib height) | shell change (§7) |
| J2 against the P5 well | courtyard u 2.34-8.38, s 16.15-21.65 | y 5.12-6.32 | standoff end u 13.19, well s 9.04-15.16 | u 4.81, s 0.99 (need ≥ 0.3) | ok |
| J3 stub after the cut | u 15.75-16.20, s 19.90-22.40 | island plane y 5.01-5.12 | wall face 16.50 | u 0.30; no Contact copper on the stub (§5.4) | ok |
| Island edges | u 2.25-15.75, s 16.00-37.60 | y 4.81-5.12 on the P1/P2 standoffs | walls u 1.50/16.50, rib face 15.70, end wall 38.20 | u 0.75/0.75, s 0.30/0.60 | ok |
| Lid post P1 | (5.90, 23.00) Ø2.0 | from the lid 7.10 onto the island F face 5.12 (1.98 long) | over the P1 standoff | see the lid-post column above | ok |
| Lid post P2 | (9.40, 32.10) Ø2.0 | from the lid 7.10 onto U1 (top 6.12, 0.98 long; load UNVERIFIED) | over the P2 standoff | see the lid-post column above | ok |

Shell changes this table needs, with numbers (all in §7): the rib cut back 0.50 from the posterior wall (u 16.00–16.50 × s 14.90–15.70 × y 1.50–4.50) for the flap; the P4/P5 wall sockets replaced by floor-standing keying walls (u 13.19–16.19, 1.0 thick, y 1.50–4.30); the closure moved off the W18 tail side or changed to a latch; two lid posts; LID_Y 7.1; cavity u 1.5–16.5. J2 clears the P5 well by 4.81 in u (need ≥ 0.3), provided the well does not reach past the standoff end at u 13.19 in −u.

## 11. UNVERIFIED and sources

### 11.1 UNVERIFIED

- **Hours of wear:** about 7 mA, inferred from EARPIECE_DESIGN.md "Seven hours of streaming" on 50 mAh. Not measured.
- **Prices:** MDBT50Q; Molex 202656-0021 header and 202655 plug; HRO 1TS015A; M2.5 nuts (W16).
- **Consignment fee** for the ISP1807.
- **LCSC codes missing:** ISP1807, TPS7A0230 and Molex 202656 (none in the JLC library); Q2–Q4 N-FET (no part chosen); 47 kΩ and 27 kΩ 0201; 4.7 µF 0402.
- **Library tier** of several v2 lines, and of the new 0201 lines beyond those read. The extended setup estimate of +$18–36.
- **Assembly:** 0201 on FPC as a combination.
- **Stiffeners:** the fee amount for ≥ 4 pieces; how JLC drills stiffeners (ring holes, J4 guide holes).
- **RF:** range with about 13 mm of metal-free edge against 18.
- **ISP1807:** "the module ties every VSS pad inside" (not in the datasheet).
- **Area:** W16/W18 fill (island scaled, parts not placed).
- **Shell:** P4/P5 hex well geometry in the W17 shell (not built); the J2 clearance holds only if the well stays at u ≥ 12.19.
- **Loads:** P2 lid-post force on U1; island stiffness at FR4 0.2 (G7).
- **ADS1292 frame size** (72 bits), used in the MISO argument.
- **Measures:** the SOT-23, SOT-23-5, TS-1187A, JST SH and 0603 courtyards are line-centre measures from footprint text, not pcbnew courtyards.
- **Cell with plug:** supply of a 501012 with the Pico-EZmate Slim plug fitted.
- **Part heights** in §10.2 beyond U1, J2, SW1 (§1.2) and the TI outlines: package maxima, no page read.
- **U1 VSS vias:** the coverlay window over the U1 land and solder wicking into the two 0.15 holes between pads 14/16/18 at reflow (§3.1).
- **REF drop:** the strip's descent from the island (y 5.01) to the end-wall slot (y 1.50–1.96) inside the 0.60 gap is v2's geometry, not re-derived here.
- **P4/P5 keying walls and the closure** (§7): proposals by numbers; the r9 shell has not been rebuilt with them.

### 11.2 Sources

| Source | Read |
|---|---|
| ISP1807 datasheet R19, https://www.insightsip.com/fichiers_insightsip/pdf/ble/ISP1807/isp_ble_DS1807.pdf | 2026-09-23 |
| Mouser ISP1807-LR-ST, https://www.mouser.com/ProductDetail/Insight-SiP/ISP1807-LR-ST | 2026-09-23 |
| nRF52840 Product Specification v1.11 (pin table, footnote 322, §6.14.3) | 2026-09-23 |
| JLC flex capabilities, https://jlcpcb.com/capabilities/flex-pcb-capabilities | 2026-09-23 (board-v2: 2026-09-17/18) |
| JLC PCBA capabilities, https://jlcpcb.com/capabilities/pcb-assembly-capabilities | 2026-09-23 |
| JLC FPC extra charges, https://jlcpcb.com/help/article/fpc-extra-charges | 2026-09-18 (board-v2) |
| L8 research v5 §2.1–2.3 (extended fee $3.00, two-sided FPC) | 2026-09-18 |
| Cells: ampul.eu 401012, AliExpress 501012 and 301012, lipolybatteries 401010 (URLs in §1.1) | 2026-09-23 |
| JLC part pages: C398746, C240195, C15525, C5142566, C2651548, C3071062 and the 0201 codes in `v4_parts.py` | 2026-09-23 |
| Molex 202656-0021 sales drawing, https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/202/202656/2026560021_sd.pdf | 2026-09-23 |
| Hirose DF58 catalogue, https://www.hirose.com/en/product/series/DF58 | 2026-09-23 |
| DigiKey ANNA-B402-00B, https://www.digikey.com/en/products/detail/u-blox/ANNA-B402-00B/13684241 | 2026-09-23 |
| TI TLV713P (SBVS195F), TPS7A02 (SBVS277C), ADS1292 (SBAS502C), BQ25100 (SLUSBV8C) | 2026-09-23 |
| Repo: `docs/fab/board-v2.md`, `plan-v2.md`, `open-questions.md`, `packing-v2.md`, `shell-v2.md`, `docs/EARPIECE_DESIGN.md`, `hardware/board/v4_parts.py`, `build_v4.py`, `make_v4_lib.py` | 2026-09-23 |
