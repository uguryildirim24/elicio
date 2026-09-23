# Board v4 — design note (smaller body)

Draft. **Not routed**: every net but GND is routed with 0 DRC errors; GND is in 37 pieces (§9).
Date: 2026-09-23. Lane t-0012.

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
| J3 | HDR-3-RA, C49257 | same, on a break-off tab | keep | Q91. Pin order reversed: J3.1 REF, J3.2 SIG2, J3.3 SIG1, so the three branches reach it without crossing |
| J4 | TC2030-NL | same | keep | Not in BOM |
| SW1 | TS-1187A, C318884 | HRO 1TS015A, C398746 | change | 3.0 × 2.0 × 0.6 |
| P1–P3 | RING_PAD_D5_H2.7 | same | keep | |
| P4, P5 | RING_PAD_D5_H2.7 on the CHARGE tab | RING_1S_D4.6_NPTH2.7, copper on B only | change | Wall rings (Q90) |
| H1, H2 | island holes Ø2.7 | — | **remove** | Stops nothing electrical. Lid posts hold the island (§5.3) |
| R1–R3 | 220 kΩ 0402, C881401 | same | keep | Contact, not shrunk |
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

v4 placement: 56 parts plus P1–P5. On the island, 22 are on F (J4 included) and 33 on B; J3 is on the tab. J4 and P1–P5 are not in the BOM, which leaves 55 lines.

**No removal changes function.** Every removed part was DNP, or is replaced by the SiP (L1), by the lid posts (H1/H2) or by the nRF's own reset pull-up (R26). The charger, charge interlock, AFE supply gate, VBUS_DET, VBAT_SENSE, CHG_MON, LED, SW1, J3 and J4 all stay.

## 3. Layers against the JLC flex rules

Source: https://jlcpcb.com/capabilities/flex-pcb-capabilities, read 2026-09-23 (research §7.1), unless another date is given. JLC does not build rigid-flex ("JLCPCB currently does not support Rigid-Flex PCBs"). So this is a 2-layer flex with FR4 stiffeners, the same construction as v2.

### 3.1 ISP1807 land on two layers

- The land is the datasheet pattern (§4.2 of the datasheet). All used pads are on the outer rows, except pad 13 (nRESET).
- nRESET leaves through a locked F.Cu 0.10 channel between pads 25 and 26. The path in module coordinates: pad 13 → (3.025, 2.7625) → (6.80, 2.7625) → (6.80, 3.05) → (8.35, 3.05).
- The RF bridge from pad 20 to pad 22 is F.Cu 0.25 (net RF_ANT).
- VSS 21 → 23 → 25 and 24 → 25 are bridged at 0.12 inside the module field.
- VSS pads 14, 16 and 18 are left **unconnected on purpose**. They sit on the row at u 6.65 beside the RF band and can't be reached without via-in-pad or copper in the band.
  - The datasheet says every VSS pad "Should be connected to ground plane on application PCB".
  - The claim that the module ties all VSS pads together inside is **UNVERIFIED** (not quoted in the datasheet).
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

- Neck: s 19.9–22.4. Tab: u 19.6–32.4 × s 16.55–25.75. Cut line: u 16.20.
- Pins, THT Ø1.5 (pin order reversed, §2): REF J3.1 (21.35, 18.61), SIG2 J3.2 (21.35, 21.15), SIG1 J3.3 (21.35, 23.69).
- Traces cross the neck at s 20.30 (SIG2, F), 20.65 (SIG1, F) and 21.20 (REF, B). Edge gap 0.325 on the −s side.
- The tab is cut before closing (Q91). The assembly sheet must show the cut line.

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

Gaps: u 4.76, s 0.95, box distance 4.85. **J2 clears P5 by ≥ 4.76 in u (≥ 0.3 ✓)**, provided the shell's well doesn't reach past the standoff end at u 13.19 in −u. The shell must hold that.

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

The J3 branches of SIG1 and SIG2 run on **F** along the −s edge and up the +u side. That leaves B free for both charge nets to cross the joint, and the charger sits on B. The first layout had the branches on B and the charge nets on F, which boxed the charger's nets in at the joint corner.

| Net | Layer | Path |
|---|---|---|
| SIG1 | B | P1 → zone exit (5.90, 8.89) → (5.90, 16.40) → R1.1 |
| SIG1 branch | B → F | (5.90, 16.40) → via (6.75, 16.60) → F (7.20, 17.05) → (14.35, 17.05) → (14.35, 20.65) → (20.00, 20.65) → (20.00, 23.69) → J3.3 |
| SIG2 | F | P2 → zone exit (10.40, −2.21) → via (10.40, 16.50). B: via → R2.1 |
| SIG2 branch | F | via (10.40, 16.50) → (14.70, 16.50) → (14.70, 20.30) → (20.60, 20.30) → (20.60, 21.15) → J3.2 |
| REF | B | P3 → zone exit (8.50, 39.40) → (8.50, 37.20) → (15.35, 37.20) → (15.35, 21.20) → (20.05, 21.20) → (20.05, 18.61) → J3.1. Branch (15.35, 25.60) → R3.1 |

- SIG2's strip copper is on F because P2 is plated. Each strip carries one net on one layer; the two Contact vias are on the island at the strip roots, not in a strip.
- SIG2's branch runs outside SIG1's (u 14.70 against 14.35, s 16.50 against 17.05), so they never cross.

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
| Q97(d) R1–R3's pads the only exposed Contact copper on the island | ✓ until the J3 cut; see below |
| Q97 "away from U1's antenna edge" | ✓: SIG1's branch runs at s ≤ 17.05 west of u 14.35 and the RF band starts at 21.8; REF runs at u ≥ 8.5 |

**Flag, stated once:** cutting J3 at u 16.20 leaves three Contact trace ends exposed on the stub (u 15.75–16.20), inside the cavity: SIG2 and SIG1 on F 0.20 apart, REF on B. That is Contact copper exposed beyond R1–R3 (Q97(d)). The cut edge needs a cover or a drawn exception.

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
| Closure | M2.5×8 at (u 16.50, s 41.00) | Must move (shell change) | On the W18 cavity wall (u ≤ 16.5) |
| Rib | s 14.9–15.7 | Needs a slot for the P4/P5 flap (shell change) | §4.4 |
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

- Every net except GND is routed: 961 track segments and 45 vias, locked pre-routes included.
- The two GND pours (F and B, over the whole island) are filled and saved.
- DRC (kicad-cli 10.0.6, `--schematic-parity`):
  - 0 shorts, 0 clearance errors.
  - 13 `starved_thermal` errors, all on GND pads.
  - 36 unconnected items, all GND.
  - Warnings: 21 `lib_footprint_mismatch`, 1 `via_dangling` (a +VDD pre-route via at (7.60, 36.70)), and 2 parity warnings (J2's MP pad has no schematic pin).
- `release.py --routed` was not run. It would refuse on the unconnected count.

### 9.1 What each router did

| Router | Placement | Result |
|---|---|---|
| Freerouting 2.4.1 on OpenJDK 25, `-Xmx4g`, locked Contact copper exported as fixed wires (`scripts/board/route_v4.py --route`) | W18 as placed at 9fc962b | 18 connections open; it never closed them. Its analytics and telemetry flags were passed off; I didn't confirm the effect |
| `v4_route_pf.py`: negotiated congestion (PathFinder) on a 0.025 grid. 0.10 tracks, 0.40/0.15 vias, rule areas and locked copper kept, GND skipped | Reliefs 1–3 (§9.2) | Nets still in conflict at the last round: 13 → 9 → 5 → 2 (AFE_VIN and VBAT) |
| Same | Relief 4 (C14 turned) | 0 conflicts at round 30, 926 items, about 6 minutes |
| `v4_route_fix.py`: drops the unlocked copper named in DRC clearance and short errors, reconnects with A*, then does local rip-up | Output of each run above | Reliefs 1–3: one net left open each time (AFE_VIN, then Q2_G). Relief 4: nothing left to do |

Freerouting stalled at this density: 0.10/0.10 rules, locked Contact copper, and B mostly keep-out. That's why I built my own router. Early on, the negotiated router lets nets share cells; overlap and history costs then rise until the nets separate. When nets still fight at the end, the fight points at a placement block, and the four reliefs below came from reading those points.

### 9.2 Placement reliefs that made it route

1. **Via column at u 10.72 beside U1's east pads** (pads at u 10.14). R7 and R27 moved, R18/R20/R21 went to u 11.80, and R19 and Q2 were re-placed.
2. **Crossings removed:**
   - C9 and C10 swapped (VREFP and VCAP1 crossed).
   - R12 turned 180° (PRETERM needed a via).
   - R15 turned 180° (VBAT hops on F).
   - C14 and R19 turned.
3. **Q2_G cluster.** R16 and R17 moved beside Q2's gate.
4. **C14 turned so its VBAT pad faces east.** With the pad facing west, VBAT ran R14 → Q1 → C14 → R20 on B. That walls off AFE_VIN's path from U4 to C5 and Q1.3, so neither net could close without crossing the other.

### 9.3 Open connections (all GND)

GND is in 37 pieces. Pour islands join through stitching vias. Lone pads need a short track or a via. Piece list, from the board text with fills counted as copper:

| Piece | Copper | GND pads in it |
|---|---|---|
| 0 | F pour, u 6.5–7.4 × s 30.7–34.0 | U1.21, U1.23, U1.24, U1.25 |
| 1 | F + B pours and 1 via, u 6.5–12.1 × s 26.8–37.6 | J4.3, J4.5 |
| 2 | B pour, u 12.5–15.1 × s 16.3–18.1 | — |
| 3 | B pour, u 2.6–5.0 × s 17.1–21.8 | C12.2, C13.2, U5.2, U5.5 |
| 4 | F pour, u 9.9–13.4 × s 20.5–24.0 (under U2) | U2.10, U2.13, U2.24, U2.33 |
| 5 | B pour, u 11.6–12.3 × s 21.2–22.1 | U4.2, U4.5 |
| 6 | F pour, u 12.1–15.4 × s 27.5–32.4 | Q4.2, SW1.2 |
| 7 | B pour, u 11.2–15.1 × s 27.5–36.9 | Q2.2, R17.2 |
| 8 | B pour, u 10.3–11.8 × s 16.0–17.6 | C2.2, R11.2 |
| 9 | F pour, u 11.4–14.1 × s 17.3–18.7 | R12.2 |
| 10 | F pour, u 12.3–14.1 × s 18.8–20.2 | R13.2 |
| 11 | F pour sliver at (14.1, 25.15) | C15.2 |
| 12 | F pour, u 12.5–13.7 × s 25.8–27.9 | R28.2 |
| 13 | F pour, u 7.1–7.8 × s 18.8–19.2 | J2.2 |
| 14 | F pour, u 2.6–7.9 × s 16.0–21.8 | J2.MP (one of two) |
| 15 | F pour, u 8.0–11.0 × s 17.3–18.6 | C9.2 |
| 16 | F pour, u 8.9–10.8 × s 24.5–25.9 | U1.1 |
| 17 | B pour, u 11.8–13.1 × s 19.4–20.6 | D1.2 |
| 18 | B pour sliver, u 11.1–11.3 × s 23.2–23.6 | C14.2 |
| 19 | B pour, u 6.3–6.9 × s 17.4–17.8 | C4.2 |
| 20 | B pour, u 11.1–11.8 × s 24.6–25.3 | C11.2 |
| 21 | B pour, u 13.8–15.1 × s 18.7–19.8 | C3.2 |
| 22 | B pour, u 10.6–11.4 × s 21.6–22.8 | C8.2 |
| 23 | B pour, u 12.9–14.3 × s 25.9–27.2 | R19.2 |
| 24 | B pour, u 4.3–5.6 × s 16.0–17.1 | C16.2 |
| 25–36 | Lone pads, no pour reaches them | C7.2, J2.MP (the other), R23.2, C6.2, C10.2, U1.7, U1.31, C5.2, Q3.2, R24.2, U3.C2, R21.2 |

KiCad's 36 unconnected items are the 36 joins between those pieces. Sixteen are pour island to pour island at 0.00 mm (an F island over a B island; one via each). The other 20 name a pad:

| From | To | Gap mm |
|---|---|---:|
| C12.2 (B) at (2.78, 18.30) | J2.MP (F) at (3.42, 20.80) | 2.58 |
| GND_POUR_B island | C4.2 (B) at (6.93, 17.45) | — |
| U1.7 (F) at (6.85, 25.56) | R23.2 (F) at (7.63, 24.10) | 1.66 |
| GND_POUR_F island | U1.7 (F) at (6.85, 25.56) | — |
| GND_POUR_F island | U1.31 (F) at (9.94, 32.54) | — |
| J2.2 (F) at (7.45, 19.50) | C10.2 (F) at (9.10, 18.28) | 2.05 |
| J2.2 (F) at (7.45, 19.50) | C4.2 (B) at (6.93, 17.45) | 2.11 |
| C7.2 (F) at (8.78, 22.34) | C6.2 (F) at (7.75, 22.18) | 1.04 |
| GND_POUR_F island | C10.2 (F) at (9.10, 18.28) | — |
| R24.2 (B) at (9.08, 24.65) | C5.2 (B) at (9.63, 23.75) | 1.05 |
| R24.2 (B) at (9.08, 24.65) | R23.2 (F) at (7.63, 24.10) | 1.55 |
| U2.13 (F) at (9.93, 22.28) | C5.2 (B) at (9.63, 23.75) | 1.50 |
| GND_POUR_F island | C7.2 (F) at (8.78, 22.34) | — |
| U1.1 (F) at (9.94, 25.56) | R24.2 (B) at (9.08, 24.65) | 1.25 |
| J4.3's locked GND stub (F) | U1.31 (F) at (9.94, 32.54) | 3.50 |
| Q3.2 (B) at (10.30, 21.12) | U2.10 (F) at (9.93, 21.08) | 0.38 |
| C11.2 (B) at (11.33, 24.60) | GND_POUR_B island | — |
| R28.2 (F) at (13.35, 27.38) | R21.2 (B) at (11.48, 27.20) | 1.88 |
| U3.C2 (B) at (13.50, 17.55) | R12.2 (F) at (12.28, 18.15) | 1.36 |
| GND_POUR_B island | U3.C2 (B) at (13.50, 17.55) | — |

"—": KiCad reports a pour at its outline's first corner, so a pad-to-pour distance has no meaning here. The gap is a straight line, not a routable width.

Starved thermals (fewer than 2 spokes reach the pour): C2.2, C4.2, C8.2, C11.2, C13.2 (B); U5.5, U4.5 (B, exposed pads); C15.2, J2.2, J2.MP, U2.10, U2.13, U2.24 (F).

### 9.4 Next, in order

1. **Stitch GND.** Run `v4_route_fix.py --nets GND --ripup 4` on the filled board; it reads filled pours as copper, but I haven't tried it on GND. Otherwise place vias by hand where F and B islands overlap. Vias stay out of LAND_P1/LAND_P2 (R 3.2) and the RF band; the finisher reads those rule areas.
2. **Refill and DRC** (`kicad-cli pcb drc --refill-zones --save-board`). The release DRC doesn't refill, so the board must be saved filled.
3. **Starved thermals.** Allow 1 spoke on GND pads with a custom rule (`min_resolved_spokes`), and give U2's and U4's exposed pads a solid connection. Keep reliefs on the 0201s so they don't tombstone. The alternative is a track to each of those pads.
4. **Q97 on the filled board.** `tests/test_board_v4.py` checks for foreign pour in each land zone.
5. **Release.** `scripts/board/release.py --board elicio-v4 --routed` writes Gerbers, BOM, CPL and STEP; only a pass makes them order files.
6. **§10.2** folded table.

### 9.5 Rebuild and re-route

```bash
cd hardware/board
KP=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3
W=/path/to/scratch            # DRC needs <stem>.kicad_pro and <stem>.kicad_dru beside each board copy
$KP build_v4.py               # placed board, locked pre-routes, GND pour outlines -> elicio-v4.kicad_pcb (overwrites the routed one)
cp elicio-v4.kicad_pcb $W/in.kicad_pcb
for s in a b c; do cp elicio-v4.kicad_pro $W/$s.kicad_pro; cp elicio-v4.kicad_dru $W/$s.kicad_dru; done
../../.venv/bin/python -u v4_route_pf.py --pcb $W/in.kicad_pcb --out $W/a.kicad_pcb --fresh --skip GND --rounds 45 --debug $W/conf.json
kicad-cli pcb drc --format json --severity-error --schematic-parity -o $W/drc_a.json $W/a.kicad_pcb
../../.venv/bin/python -u v4_route_fix.py --pcb $W/a.kicad_pcb --drop-drc $W/drc_a.json --skip GND --ripup 4 --out $W/b.kicad_pcb
cp $W/b.kicad_pcb $W/c.kicad_pcb
kicad-cli pcb drc --refill-zones --save-board --format json --schematic-parity -o $W/drc_c.json $W/c.kicad_pcb
```

The committed board is `c` from this sequence; the finisher found nothing to do on `a`. Freerouting instead: `scripts/board/route_v4.py --work DIR --route`. It needs one run at a time and `-Xmx4g`.

## 10. Flat and folded tables

### 10.1 Flat PCB coordinates (u, s)

From `python3 hardware/board/v4_tables.py --pads` on the committed board. Part centres, then pad by pad for the connectors, rings, J4 and SW1. The Gerber carries these (PCB x, y = u, s).

| ref | side | x (u) | y (s) | rot | footprint |
|---|---|---:|---:|---:|---|
| C1 | bottom | 13.30 | 23.65 | 90 | `Capacitor_SMD:C_0201_0603Metric` |
| C2 | bottom | 11.95 | 17.55 | 180 | `Capacitor_SMD:C_0201_0603Metric` |
| C3 | bottom | 14.40 | 19.95 | 90 | `Capacitor_SMD:C_0201_0603Metric` |
| C4 | bottom | 7.25 | 17.45 | 180 | `Capacitor_SMD:C_0201_0603Metric` |
| C5 | bottom | 9.95 | 23.75 | 180 | `Capacitor_SMD:C_0201_0603Metric` |
| C6 | top | 7.75 | 22.66 | 90 | `Capacitor_SMD:C_0402_1005Metric` |
| C7 | top | 8.78 | 22.66 | 90 | `Capacitor_SMD:C_0201_0603Metric` |
| C8 | bottom | 11.65 | 22.55 | 180 | `Capacitor_SMD:C_0402_1005Metric` |
| C9 | top | 10.20 | 18.50 | 90 | `Capacitor_SMD:C_0402_1005Metric` |
| C10 | top | 9.10 | 18.60 | 90 | `Capacitor_SMD:C_0201_0603Metric` |
| C11 | bottom | 11.65 | 24.60 | 180 | `Capacitor_SMD:C_0201_0603Metric` |
| C12 | bottom | 3.10 | 18.30 | 180 | `Capacitor_SMD:C_0201_0603Metric` |
| C13 | bottom | 4.60 | 18.30 | 180 | `Capacitor_SMD:C_0201_0603Metric` |
| C14 | bottom | 11.65 | 23.60 | 180 | `Capacitor_SMD:C_0402_1005Metric` |
| C15 | top | 13.60 | 25.15 | 0 | `Capacitor_SMD:C_0201_0603Metric` |
| C16 | bottom | 4.70 | 17.15 | 90 | `Capacitor_SMD:C_0201_0603Metric` |
| D1 | bottom | 12.60 | 19.70 | 180 | `Diode_SMD:D_SOD-523` |
| D2 | top | 14.65 | 26.10 | 0 | `LED_SMD:LED_0402_1005Metric` |
| J2 | top | 5.45 | 18.90 | -90 | `Connector_Molex:Molex_Pico-EZmate_Slim_202656-0021_1x02-1MP_P1.20mm_Vertical` |
| J3 | top | 21.35 | 18.61 | 0 | `Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Horizontal` |
| J4 | top | 10.00 | 35.40 | 0 | `Connector:Tag-Connect_TC2030-IDC-NL_2x03_P1.27mm_Vertical` |
| P1 | top | 5.90 | 5.29 | 0 | `elicio:RING_PAD_D5_H2.7` |
| P2 | top | 10.40 | -5.81 | 0 | `elicio:RING_PAD_D5_H2.7` |
| P3 | top | 8.50 | 43.00 | 0 | `elicio:RING_PAD_D5_H2.7` |
| P4 | bottom | 16.51 | 4.35 | 180 | `elicio:RING_1S_D4.6_NPTH2.7` |
| P5 | bottom | 16.51 | 12.10 | 180 | `elicio:RING_1S_D4.6_NPTH2.7` |
| Q1 | bottom | 9.95 | 22.80 | 180 | `Package_TO_SOT_SMD:SOT-883` |
| Q2 | bottom | 13.35 | 27.60 | 180 | `Package_TO_SOT_SMD:SOT-883` |
| Q3 | bottom | 9.95 | 20.90 | 180 | `Package_TO_SOT_SMD:SOT-883` |
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
| R14 | bottom | 9.95 | 21.85 | 180 | `Resistor_SMD:R_0201_0603Metric` |
| R15 | bottom | 9.95 | 19.95 | 0 | `Resistor_SMD:R_0201_0603Metric` |
| R16 | bottom | 14.60 | 27.10 | -90 | `Resistor_SMD:R_0201_0603Metric` |
| R17 | bottom | 14.60 | 28.55 | -90 | `Resistor_SMD:R_0201_0603Metric` |
| R18 | bottom | 11.80 | 25.60 | 180 | `Resistor_SMD:R_0201_0603Metric` |
| R19 | bottom | 13.30 | 26.52 | 0 | `Resistor_SMD:R_0201_0603Metric` |
| R20 | bottom | 11.80 | 26.40 | 180 | `Resistor_SMD:R_0201_0603Metric` |
| R21 | bottom | 11.80 | 27.20 | 180 | `Resistor_SMD:R_0201_0603Metric` |
| R22 | top | 14.60 | 27.02 | 180 | `Resistor_SMD:R_0201_0603Metric` |
| R23 | top | 7.95 | 24.10 | 180 | `Resistor_SMD:R_0201_0603Metric` |
| R24 | bottom | 9.40 | 24.65 | 180 | `Resistor_SMD:R_0201_0603Metric` |
| R25 | bottom | 11.95 | 18.35 | 180 | `Resistor_SMD:R_0201_0603Metric` |
| R27 | top | 12.45 | 25.50 | -90 | `Resistor_SMD:R_0201_0603Metric` |
| R28 | top | 13.35 | 27.70 | 90 | `Resistor_SMD:R_0201_0603Metric` |
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
| J3.1 | thru_hole | REF | 21.35 | 18.61 |
| J3.2 | thru_hole | SIG2 | 21.35 | 21.15 |
| J3.3 | thru_hole | SIG1 | 21.35 | 23.69 |
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

Not generated yet; `v4_tables.py` prints only the flat table. The fold sites and cavity tests exist by numbers in §4.4 (P4/P5 plate), §4.5 (strips and rings), §4.8 (cavity tests) and §4.9 (J2 against the P5 well). A generated table with a cavity test for every courtyard, hang and tab root is still owed.

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
