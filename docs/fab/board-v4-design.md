# Board v4 — design note (smaller body)

Draft. **Routed, not a complete ESD fix**: DRC 0 errors and 0 unconnected after a zone refill, and `scripts/board/release.py --board elicio-v4 --routed` passes (§9). U3 now has DC-bias-characterized IN/TS/OUT capacitors meeting the numerical IEC rating conditions, but D1 still clamps at the far end of VBUS and the nearest OUT bulk is 9.3 mm from U3; the conditional IC rating is not a contact-level test (§2.1). Rolf chose off-ear-only charging with fixed TS and a two-wire J2 (no cell NTC); the antenna keep-out still needs his decision (§4.2). The later built snap shell is a print-trial solid, not a verified fit; see `shell-v4.md`. §11.1 lists what is still UNVERIFIED.
Date: 2026-09-25. Lanes t-0012 (Opus 5.5: design and first routing), t-0014 (Fable 5.1: routed to 10 open), t-0016 (Fable 5.1: pass-2 placement), t-0019 (Opus 5.5: passes 3–6 and the first routed board), t-0036 (charger ESD capacitor changes and reroute).

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
| L7 | Q1–Q4 SOT-23 → DFN1006-3. U4 SOT-23-5 → X2SON-4 | area about 57 mm² | 0 | 0 | Nothing | Q2–Q4 are PMZ290UNE2 (C478155, §2.1 item 4). U4 C3071062 has 0 stock at JLC | Q1 WPM3027-3 C240195. The rest UNVERIFIED | **Yes** |
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
| Q2–Q4 | 2N7002 SOT-23, C2128 | Nexperia PMZ290UNE2YL DFN1006-3 (SOT883), C478155 | change | Refcheck t-0023 (§2.1). Pin 1 G, 2 S, 3 D, as the SOT-883 land |
| Q5 | 2N7002, DNP | — | **remove** | Stops nothing: DNP, BAT_MEAS_EN was never driven |
| D1 | PESD5V0L1UL SOD-523, C24109 | same part on Nexperia's SOD882 land (KiCad `D_SOD-882`) | change land | Refcheck t-0023 (§2.1). VBUS TVS, pad 1 cathode on VBUS |
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
| R5–R8, R13, R25, R27, R28 | 10 kΩ 0402, C25744 | 0201, C473048 | change | R13 stays a fixed 10 kΩ on TS: no flex copper touches the cell for an NTC (§2.1) |
| — | — | R34, R35 10 kΩ 0201, C473048 | **add** | U2 GPIO1/GPIO2 to GND (refcheck t-0023, §2.1) |
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
| C3 | 1 µF 0402, C15849 | 10 µF 0402 X5R 10 V, Murata GRM155R61A106ME18, consigned | change | IN effective 2.277 µF at 5 V (§2.1) |
| C4–C5, C10, C13 | 1 µF 0402, C15849 | 0201, C5142566 | change | |
| C6, C8, C9 | 10 µF 0603, C19702 | 0402, C15525 (Basic) | change | |
| C7, C15 | 100 nF 0603, C14663 | 0201, C307380 | change | |
| C11 | 100 nF 0402, C1525 | 1 µF 0201, C5142566 | change | VCAP2 (refcheck t-0023, §2.1) |
| C12 | 100 nF 0402, C1525 | 0201, C307380 | change | |
| — | — | C17 100 nF 0201, C307380 | **add** | VREFP local bypass beside C9 (refcheck t-0023, §2.1) |
| C14 | 4.7 µF 0402, C19675 | 10 µF 0402 X5R 10 V, Murata GRM155R61A106ME18, consigned | change | OUT (VBAT) effective 2.781 µF at 4.2 V (§2.1); 9.3 mm from U3 |
| — | — | C18 10 µF 0402 X5R 10 V, Murata GRM155R61A106ME18, consigned | **add** | TS to GND, 2.55 mm from U3.B1; fixed R13 unchanged |
| — | — | C19 10 µF 0402 X5R 10 V, Murata GRM155R61A106ME18, consigned | **add** | Extra OUT (VBAT) bulk; temperature margin, but far from U3 |

J1 (USB-C) and USBLC6 were already absent in v2 (Q81).

v4 placement: 64 parts plus P1–P5. On the island, 25 are on F (J4 included) and 35 on B; J3, R31 and R33 are on the tab and R32 on its neck. J4 and P1–P5 are not in the BOM, which leaves 63 lines.

**No removal changes function.** Every removed part was DNP, or is replaced by the SiP (L1), by the lid posts (H1/H2) or by the nRF's own reset pull-up (R26). The charger, charge interlock, AFE supply gate, VBUS_DET, VBAT_SENSE, CHG_MON, LED, SW1, J3 and J4 all stay.

### 2.1 Refcheck t-0023 changes

The circuit check (`docs/fab/board-v4-refcheck.md` on the t-0023 branch, datasheets read 2026-09-25) named six order blockers. Five are fixed in the schematic and on the board, and the schematic ERC is clean. The NTC doesn't fit (item 6). The antenna keep-out (13 mm against 18) stays as it is; it's on Rolf's list (§4.2).

1. **D1 land.** PESD5V0L1UL is made in Nexperia's SOD882 (DFN1006-2): "leadless ultra small plastic package; 2 terminals; body 1.0 × 0.6 × 0.5 mm" (datasheet Table 4). v2's SOD-523 land was another package.
   - Pinning (Table 3): pin 1 cathode, marked by the bar; pin 2 anode. Pad 1 is on VBUS, pad 2 on GND.
   - Land: KiCad `D_SOD-882`, pads 0.4 × 0.7 at 0.70 pitch, gap 0.30. Nexperia's reflow land (Fig. 13) is 0.3 × 0.6 at 0.60 pitch, gap 0.30. Same gap; KiCad's pads reach 0.10 further out on each side.
   - D1 **remains** on B at (14.30, 28.60), cathode (14.65, 28.60); U3.A2 is (14.30, 17.55), so even the straight-line lower bound is 11.06 mm before the clamp (the copper path is longer). Trials of D1 by U3 ran into the 15.09 notch, R16/R17, U2's courtyard and the input-crossing channels. Beside U2, the F-side u strip 14.48–15.75 is 1.27 mm wide against D1's rotated courtyard width 1.30 mm (0.03 mm overlap); the B-side candidate (14.43–15.73, 19.70–21.40) overlapped the then-R17 courtyard (13.75–15.15, 20.50–21.20) and, after moving R17, the RLD vias. The final B-side TS cap occupies (14.61–15.53, 19.79–21.61), so this pocket cannot also hold D1. Putting the 0402 TS cap on F produced three persistent router conflicts (AFE_IN1N, AFE_IN1P, GND_B). The clean route instead has C18 on B at (15.07, 20.70) and adds C19 OUT bulk on F at (14.10, 34.20). This is not an ESD-interception layout. **The numerical fallback is U3's own conditional 8 kV contact / 15 kV air IEC 61000-4-2 IN rating** (SLUSBV8C §7.2), with C3/C18/(C14+C19) satisfying its 1/1/2 µF effective minimum at the specified biases, calculated below; it does *not* prove a surge at P4, where no contact-level IEC test was run. C24109's listing for D1's SOD882 package remains UNVERIFIED.
2. **C11 (VCAP2) 1 µF.** TI shows 1 µF at VCAP2 (SBAS502C Fig. 73); v2 had 100 nF. Now 1 µF 0201 (C5142566), its pad 0.6 from pin 27 on a locked F track. The effective value at VCAP2's DC bias is UNVERIFIED (an 0201 X5R loses capacitance under bias).
3. **GPIO1/GPIO2 pull-downs.** SBAS502C §8.5.1.7: the GPIO pins default to inputs and must not float. R34 (GPIO1, pin 26) and R35 (GPIO2, pin 25) are 10 kΩ to GND on B, each one via away from its pin. Firmware leaves both as inputs.
4. **Q2–Q4 PMZ290UNE2.** Nexperia PMZ290UNE2YL, DFN1006-3 (SOT883), LCSC C478155. The older PMZ290UNE is end-of-life. Datasheet Rev. 1 (2015):
   - Pins (Table 2): 1 G, 2 S, 3 D, the order of the SOT-883 land.
   - VGS(th) 0.45–0.95 V at ID 250 µA; RDSon ≤ 1.19 Ω at VGS 1.5 V; IDSS ≤ 1 µA at 20 V (Table 7). VDS 20 V, VGS ±8 V (Table 5).
   - Gate drive: Q2 from R16/R17 (VBUS × 1/1.1: 4.5 V at 5.0 V, 5.0 V at 5.5 V); Q3 from AFE_EN_HW (VBAT through R15, 3.0–4.2 V); Q4 from LED_EN (3.0 V). Each is at least 3× VGS(th) max and under the 8 V gate limit.
   - Off state: without VBUS, R17 holds Q2's gate at 0 V, and 1 µA of IDSS drops 0.1 V across R15. With VBUS, Q2 holds AFE_EN_HW near 0 V (42 µA through ≤ 1.19 Ω), so Q3 is off.
   - Drains see VBAT (≤ 4.2 V) or, for Q4, the LED cathode below VBUS (≤ 5.5 V), against 20 V.
   - Still for the bench (refcheck): the Q2 charge interlock with a low cell.
5. **C17 VREFP 100 nF.** SBAS502C Fig. 73 shows 10 µF + 0.1 µF at VREFP. C17 (100 nF 0201) sits on F beside C9, its VREFP pad next to C9's.
6. **U3 TS: R13 stays; no NTC.** C18 is a TS-to-GND *bypass*, not a temperature sensor and not a change in the TS network decision. TI designs TS for "a 10-k NTC β = 3370 ... connected from the TS pin to VSS" and says to "use a 10-k NTC thermistor in the battery pack (103AT)" (SLUSBV8C §8.3.8, §9.2.2.1.3). An NTC only helps where it touches the cell, and no flex copper does:
   - The cell sits in its pocket at s 1.5–14.9. The island starts at s 16.0 behind the rib (s 14.9–15.7), at least 1.1 from the cell's end through air and plastic.
   - In the cell section the flex is only the SIG1/SIG2 strips and the P4/P5 plate. The strips are Contact copper, one net each (Q97), so no TS track can ride on them. The plate folds against the wall at u 16.19–16.30 behind the standoffs, 4.3 from the cell's side (u 11.9); it would read the charge standoffs.
   - An NTC on the island next to U3 would read the board and stop charge on the board's temperature. That looks like protection and isn't.
   - A cell NTC would need a third J2 contact and a different cell order (L4). Rolf chose to keep the released two-wire J2 and fixed R13 instead, with charging **only off the ear**. The 0–45 °C charge window is a procedural check, not automatic protection (board-v2 §5); bench verification and approval of that residual risk are still required.

7. **Charger IEC capacitor check (t-0036).** TI BQ25100 SLUSBV8C §7.2 rates IN for **8 kV contact / 15 kV air** only when effective capacitance is ≥ 1 µF IN, ≥ 1 µF TS and ≥ 2 µF OUT, X5R or better. Murata SimSurfing **C-DC bias / Capacitance**, 25 °C, 0.1 Vrms, read **2026-09-25**: [online characteristics viewer](https://ds.murata.com/simsurfing/mlcc.html?lcid=en-us); product record [GRM155R61A106ME18](https://www.murata.com/en-global/products/productdetail?partno=GRM155R61A106ME18). Reproducible maker graph data: [10 µF graph](https://ds.murata.com/simserve/characteristics?callback=nothing&ReqType=Characteristics&ReqChara=%5B%7B%22partnumber%22%3A%22GRM155R61A106ME18%22%2C%22chara_type%22%3A%22c_dcbias_capacitance%22%2C%22parameter%22%3A%7B%22tc%22%3A%2225%22%2C%22ac%22%3A%220.1%22%7D%2C%22WorkInfo%22%3A%7B%7D%7D%5D&WorkInfo=test). Both are **0402, 10 V, X5R, ±20%**, per the maker's SimSurfing `mlcc.csv` product rows. Values below are graph µF, then graph × 0.8 (extra tolerance allowance); no nominal-value arithmetic or uncharacterized C16 is counted.

   | Pin, part | DC bias | Maker graph | ×0.8 | IEC minimum | Margin after ×0.8 |
   |---|---:|---:|---:|---:|---:|
   | IN, C3 10 µF GRM155R61A106ME18 | 5.0 V | 2.277 µF | 1.821 µF | 1 µF | +0.821 µF |
   | TS, C18 10 µF GRM155R61A106ME18 | 5.5 V upper bound (at or below VBUS) | 2.034 µF | 1.627 µF | 1 µF | +0.627 µF |
   | OUT/VBAT, C14+C19 (2 × 10 µF GRM155R61A106ME18) | 4.2 V | 5.562 µF | 4.449 µF | 2 µF | +2.449 µF |

   At 5.5 V IN the 10 µF curve is 2.034 µF (×0.8 = 1.627 µF). C3's VBUS pad is (14.40,16.72), 0.84 mm straight-line from IN ball U3.A2 (14.30,17.55). C18's TS pad is (15.07,20.22), 2.55 mm from U3.B1 (13.90,17.95). **C14's OUT pad is (13.67,27.20), 9.27 mm from U3.A1 (14.30,17.95)**; C19's OUT pad is (14.10,34.68), 16.73 mm away. Their DC capacitance is on VBAT but these lengths are not local high-frequency ESD bypasses. Multiplying again by 0.85 for the X5R ±15% temperature envelope gives IN 1.383 µF at 5.5 V, TS 1.383 µF at 5.5 V, OUT 3.782 µF at 4.2 V: all above 1/1/2 µF *by this independent allowance*, not by measured temperature/bias joint curves. Actual aging, mounted tolerances and contact-level response remain unmeasured. The parts are marked CONSIGNED in the BOM because a JLC supply code for this exact MPN was not verified. There is no claim of a P4 IEC test.

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
| AFE decoupling, RESET pull-down | F | u 7.75–11.1 × s 18.5–24.10 | C6, C7, C9, C10, C17 (VREFP 100 nF beside C9), R23 |
| Charger pulls | F | (12.60, 18.15), (13.25, 18.97) | R12 (PRETERM), R13 (TS). R13 sits 0.65 east so AFE_IN1N and IN1P's branch drop between C17 and R12 to U2 pins 3 and 4 (§9.2) |
| VCAP2 | F | (15.10, 23.20) rot 270 | C11, beside U2's east row, its pad toward pin 27 |
| CS/DRDY series, pad-23 decoupling, charge LED | F | u 11.05–14.65 × s 25.15–28.0 | R7, R27, C15, D2, R22, Q4, R28. R7 at u 11.05 and R27 turned so MOSI and CS leave U2's south row without a via (§9) |
| SPI series | F | u 11.40 × s 29.6–32.6 | R6, R5, R8 in U2's pad order |
| SW1 | F | (14.45, 31.10) rot 180 | Top 5.72 |
| J4 TC2030-NL, extra OUT bulk | F | J4 (10.00, 35.40); C19 (14.10, 34.20) | Just outside the RF band (u ≥ 6.455); C19 is remote from U3 |
| U5 and caps | B | u 3.1–4.7 × s 17.1–18.3 | Under J2. U5, C16, C12, C13 |
| Contact resistors R1, R2, C4 | B | s 17.25–17.45 | At the strip roots |
| Charger | B and F | U3 (13.90, 17.75) B rot 90 | U3, R11, C2, R25 on B; C3 on F (14.40,17.20), C18 TS on B (15.07,20.70). Both charge nets arrive on B; OUT bulk C14/C19 is remote |
| AFE gate and charge interlock | B | u 9.85–14.45 × s 18.6–23.9 | R15, Q3, R14, Q1, C5 (the west stack at u 9.85–10.80); Q2, R16, R17 beside the charger, so AFE_EN_HW is one short hop from Q2.3 to Q3.1 (§9.2) |
| AFE LDO and RLD network | B | u 11.45–13.3 × s 21.25–24.7 | U4, C8, R4, C1, R24 (START pull-down) |
| GPIO pull-downs | B | (14.95, 23.22), (14.40, 24.55) | R34, R35 (§2.1 item 3) |
| REF resistor, dividers, VBAT bulk, TVS | B | u 12.40–14.55 × s 25.6–29.3 | R3, R20, R21, R18, R19 (u 12.40, U1-side pads west), C14 10 µF, D1 far from charger (§2.1) |

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

### 4.8 Prebuild cavity tests (by numbers; the later built shell is checked in `shell-v4.md`)

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
| AFE_IN1P | F, 0.10 | R31.1 (21.89, 16.80) → (20.50, 16.80) → (20.50, 20.40) → (15.40, 20.40); the router joins it to the end of the locked trunk at (11.95, 16.66), and the trunk and its branch reach R1.2 and U2 pad 4 (§9.2, pass 5) |
| AFE_IN1N | F, 0.10 | R32.1 (17.49, 21.15) → (15.40, 21.15); the router joins it to U2 pad 3, and a locked run joins pad 3 to R2.2 (§9.2, pass 5) |
| RLD_FB | F, 0.10 | R33.1 (21.89, 27.10) → (20.90, 27.10) → (20.90, 21.90) → (15.40, 21.90); the router joins it to R3.2 and U2 pads 29/30 |

- SIG2's strip copper is on F because P2 is plated. Each strip carries one net on one layer; the one Contact via is on the island at SIG2's strip root, not in a strip. SIG1 and REF have no via.
- With the tab on (bench use), a gel lead on J3.n sees pin → 0.15 track → 220 kΩ (R31–R33) → AFE node, and the dome on the same node sees dome → strip → 220 kΩ (R1–R3) → AFE node: two independent 220 kΩ per node. The bench nets are in the Contact netclass (0.15/0.20) and R31–R33 sit at u ≥ 17.49, east of the cut.
- The cut at u 16.20 crosses only the three AFE-side 0.10 runs.

Charge copper, 0.20 track. It is only where skin can't reach: plate, flap and joint.

| Net | Path |
|---|---|
| P5 GND | B: ring → (17.95, 13.30) → (17.95, 15.75) [zone exit] → (17.95, 16.90) → (14.84, 16.90) → (14.35, 16.39) → (11.80, 16.39) → R11.2 along the top edge (0.10, locked, pass 6), then the B pour |
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
- Placed at W18 (t-0012's placement, before the refcheck parts): F parts 155.0 mm² (22 parts), B parts 45.7 mm² (33 parts). J3 and the rings are off the island.

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

**VSS 14/16/18.** Connected to the B-side GND pour through two vias between the pads (§3.1). Whether the module ties them inside is UNVERIFIED and not relied on.

**VBUS (pad 12) and D± (8/10) are unconnected.**

- The module never sees USB.
- `firmware/elicio_stream/elicio_stream.ino` reads VBUS through `NRF_POWER->USBREGSTATUS`. It must switch to the VBUS_DET GPIO (R18/R19 divider).

**First load.** VDD is 3.0 V from U5 from power-up, so v2's REGOUT0 1.8 V first-load issue is gone. A 3.3 V probe sits at VDD + 0.3, not over it. G4 still verifies.

**AFE inputs while +3V0 is off or ramping (firmware lane t-0022).** SBAS502C §10.1: "Before device power-up, all digital and analog inputs must be low. At the time of power-up, all of these signals should remain low until the power supplies have stabilized". The MCU runs from U5 all the time, but +3V0 is off whenever VBUS is present (Q2 → Q3 → Q1, §5.4 interlock). So while a charger is on, the MCU's lines to U2 face an unpowered chip. U2's inputs have no pull resistors of their own; the limits are digital input ≤ DVDD + 0.3 and ±10 mA continuous per pin (§6.1).

- **CS, SCLK, MOSI** reach U2 through R7, R6, R5 (10 kΩ). A line left high into an unpowered U2 feeds at most (3.0 − 0.3) / 10 kΩ ≈ 0.27 mA into its clamp: no harm, but it lifts +3V0 partway and spoils the power-up. Firmware releases them (output low, or input disconnected) and they carry nothing. **No pull-downs needed.** A pull-down on U2's side would cost 30 µA per line at 100 kΩ while CS idles high.
- **RESET and START** are wired straight to U2, with R23 and R24 (100 kΩ) already pulling them low. Released, they sit low as §10.1 wants. There's no series resistor, so RESET held high by mistake would back-feed U2 through its clamp. Once C8 is charged the current is U2's own supply draw, under the ±10 mA limit. No part change; this is a firmware rule.
- **Firmware rule.** While VBUS_DET is high, and from boot until +3V0 has been up for tPOR (2¹² tMOD, Table 29), drive CS, SCLK, MOSI, START and RESET low or disconnect them; never high. VBUS_DET rises with VBUS (R18/R19), while +3V0 falls only after Q2, Q3 and Q1 have switched; a few milliseconds of overlap are harmless at these currents. After VBUS goes away, +3V0 comes back once R17 has drained Q2's gate. Then wait tPOR, pulse RESET and configure. MISO and DRDY are inputs at the MCU behind R8 and R27 and need nothing.

**CHG_MON range (t-0022).** CHG_MON is ISET seen through R25 (10 kΩ) on P0.30/AIN6. The BQ25100 regulates ISET against a 1.5 V fast-charge reference (SLUSBV8C §8.2 block diagram; the table has no V_ISET row, so UNVERIFIED as a number), and less than that in precharge and taper. Without VBUS the charger is "dead" with every pin high impedance (§8.4.1), and R11 holds ISET at 0 V. So CHG_MON stays at 1.5 V or below, inside U1's VDD 3.0 (VI/O ≤ VDD + 0.3, nRF52840 PS Table 185). If R11 fails open, ISET's voltage isn't specified (UNVERIFIED); its absolute maximum is 7 V (§7.1), and even at 7 V R25 limits the current into U1's clamp to ≤ 0.4 mA. The SAADC sees about 17 kΩ of source (R25 plus R11), so firmware sets its acquisition time for that.

## 9. Routing status

**Routed again (t-0036 ESD-cap revision).** `hardware/board/elicio-v4.kicad_pcb`:

- 1047 track segments (210 locked pre-routes) and 56 vias (28 locked). Every connection is closed. D1 remains at the far end; see §2.1 for the conditional IEC rating and residual ESD risk.
- The two GND pours (F and B, over the whole island) are filled and saved; the release DRC does not refill.
- DRC (kicad-cli 10.0.6, project rules `elicio-v4.kicad_dru`, `--refill-zones --schematic-parity`, on the committed file in place), verbatim: `Found 28 violations`, `Found 0 unconnected items`, `Found 2 schematic parity issues`.
  - Errors: 0: no short, no clearance error, no starved thermal (§9.3). Unconnected: 0.
  - Warnings: 27 `lib_footprint_mismatch`, 1 `via_dangling`. `build_v4.py` strips footprint silkscreen and hides fields, so the placed footprints differ from KiCad's library copies. `via_dangling` is the +VDD pre-route via at (7.60, 36.70), used on F only. The parity warnings are J2's two MP pads, which have no schematic pin.
- `scripts/board/release.py --board elicio-v4 --routed`: exit 0, `routed: true`. ERC 0 errors and 0 warnings; DRC 0 errors, 28 warnings, 0 unconnected; 63 BOM rows and 63 CPL rows, no BOM line without a CPL row; 17 files in `gerbers/` (14 layers, PTH and NPTH drill, job file); STEP written without models for 5 footprints (Molex Pico-EZmate Slim, Texas DSBGA-6, Texas RSM0032, Texas X2SON-4, SOT-883). The outputs are in `hardware/board/release/elicio-v4/`; they're not committed, and the command writes them again.
- Unchanged: two copper layers, 0.10/0.10 track and clearance, 0.40/0.15 vias, the Contact class and the Q84/Q88/Q97 rule areas. The folded body is still 18 × 8.1 (§10.2).

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
| `v4_route_pf.py --fresh --skip GND --rounds 80`, GND in regional nets (t-0016 run 2) | pass 2 (§9.2 relief 6) | 7 knots, all north of s 25 |
| same (t-0019 run 1) | pass 3: refcheck parts, U2's GND core locked (relief 7) | 15 nets in conflict after 60 rounds, round U2's north side and the charger |
| same (t-0019 run 2), then `v4_finish.sh` | pass 4: placement at the knots and the corner pre-routes (relief 8) | 2 nets in conflict after 80 rounds (AFE_IN1P, AFE_IN1N). Finished: DRC 0 errors, 1 open: AFE_IN1N, 0.51 mm at U2 pins 3/4. The two inputs must cross once, which no routing order avoids |
| same (t-0019 run 3) | pass 5: the IN1P/IN1N crossing locked, R13 moved (relief 9) | 2 nets in conflict after 80 rounds (AFE_IN1P, GND_B): U3.C2's GND boxed in. Not finished |
| same (t-0019 run 4), then `v4_finish.sh` | pass 5b: a GND via for U3.C2's corner (relief 9) | 0 conflicts at round 16. Finished: DRC 0 errors, 2 open, both GND islands 0.40 mm from the main GND (P5's run north of U3; Q4.2's F pocket) |
| same (t-0019 run 5), then `v4_finish.sh` | pass 6: two locked GND links (relief 10) | 0 conflicts at round 16. Finished: DRC 0 errors, 0 open. Previous board |
| t-0036 first trial (router only) | C3 F, C18 F, D1 unchanged | 3 conflicts at round 79 (AFE_IN1N, AFE_IN1P, GND_B) near (15.2,20.7); not finished |
| t-0036 second trial, `v4_finish.sh` | C18 B, R17 moved west to u 13.70, C3 F and C14 larger; D1 unchanged | 0 conflicts at round 79, GND_C reported failed; finisher: DRC 0 errors, 0 unconnected; intermediate board |
| t-0036 final trial, `v4_finish.sh` | C18 increased to 10 µF and C19 10 µF added at F (14.10,34.20); D1 unchanged | 0 conflicts at round 79, GND_C reported failed; finisher: DRC 0 errors, 0 unconnected, routed release passes. Current board |

Freerouting stalled at this density: 0.10/0.10 rules, locked Contact copper, and B mostly keep-out (t-0012). The negotiated router lets nets share cells early and raises the price of shared cells each round until the nets separate; when nets still fight at round 80 the fight points at the placement. GND is the hard net: the pours reach only what the signal routing leaves open, so GND has to be in the negotiation from the start, but as one net it is too big to negotiate (it touches every part). What closed it: three regional GND nets, with locked copper at every knot that kept coming back (U2's GND core, the +3V0 hub, the charger corner, the IN1P/IN1N crossing). With those locked, the router converges in 16 rounds and the finisher joins the three GND regions through the pours.

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
6. **Pass 2 (t-0016).** R20, R21, R18 and R19 went one row east to u 12.40 with their U1-side pads west, so U1's east pads get a second via column at u 11.3, and s 25.05–26.5 stays free for AFE_DRDY's hop to R27 on B. The interlock (Q2, R16, R17) moved north beside the charger, and Q3 and R15 turned so Q2.3 faces R15.2 across the corridor's north end: AFE_EN_HW runs R15.2/Q3.1 → Q2.3, not to U1 (t-0016's finding), and is now one short hop that no longer crosses CHG_MON. Q1 and R14 turned (AFE_VIN east toward U4), C8 turned, C14 to the east pocket beside R20.1, C11 to F beside U2's east row, C3 closed up to U3.A2 (t-0019 only; t-0036 puts it on F).
7. **Pass 3 (t-0019): refcheck parts and U2's GND core.** C17, R34, R35 and D1's SOD882 land (§2.1). U2's GND pads 10, 13 and 24 are tied to the exposed pad, and one exposed-pad via reaches U4.5, U4.2 and C8.2. VCAP2 runs to C11, GPIO1 and GPIO2 hop to R34 and R35. `v4_gnd_split.py` now joins locked GND copper to the region of the pad it touches.
8. **Pass 4 (t-0019): placement at the knots and locked corner routes.** R13 and R4 turned, R16 0.35 south, C5 turned and 0.15 south, R24 to (11.45, 24.70), D1 to (14.30, 28.60) (§2.1 item 1). Locked in `u2_core_pre_routes` (`build_v4.py`):
   - U2's GND core: the exposed-pad via, Q2.S and Q3.S vias into the pad, an exit through pin 24 to C15.2 and C11.2 on F, and the east pocket's GND down the B edge lane.
   - The +3V0 hub on B from U4.1 over C8.1, with arms to U2's four sides; the west via sits outside LAND_P1's 3.4 mm circle. This is t-0014's first proposed pre-route.
   - VBAT's row south of U3 to R15; ISET, TS, PRETERM and CHG_MON; VBUS to C3 and R16; Q2_G; AFE_EN_HW, AFE_GATE (through Q1's pad gap) and AFE_VIN; AFE_START and AFE_RESET out of U2's south-west corner; the RLD_FB and RLDINV vias and B links.

   t-0014's second proposal, AFE_EN_HW across the P1 landing to U1, wasn't needed: after relief 6 AFE_EN_HW is a short B hop with no copper in LAND_P1's 7 × 7 zone, so Q97(c) is untouched.
9. **Passes 5 and 5b (t-0019): the IN1P/IN1N crossing.** The two inputs must cross once: at the J3 neck IN1P lies north of IN1N, at the strips R1 (IN1P) lies west of R2 (IN1N). Locked in `in1_pre_routes`: IN1P crosses over R2 on F, and IN1N leaves R2 by a via just west of it. IN1P's trunk (along the top edge, toward the neck) and its branch (back east to pin 4) wrap round that via. VBUS, the trunk, IN1N and the branch pass the SIG2 root 0.105 apart and 0.21 from the SIG2 via (Contact class 0.20). R13 moved 0.65 east so IN1N and the branch drop between C17 and R12 to pins 3 and 4. Pass 5b: past the SIG2 root, VBUS and the trunk rise to s 16.45 and 16.66, and a locked GND via at (11.67, 17.15) on the R11.2–C2.2 link reaches R12.2 and U3.C2's via on F, since ISET and VBAT box U3.C2 in on B.
10. **Pass 6 (t-0019): two GND links the finisher couldn't find.** P5's charge-return run ends on B north of U3, where ISET and VBUS box it in and the IN1P/VBUS pair holds the F edge: a locked B track takes it along the top edge, north of R11.1, to R11.2 (§5.4). Q4.2 (the charge-LED switch source) sat in an F pocket between LED_EN and VBUS: a locked GND via at (13.50, 28.58) beside D1.2 joins it to B.
11. **t-0036 ESD caps:** C3 grew from 0201 1 µF to 0402 10 µF and moved to F (14.40,17.20), with its VBUS pad 0.84 mm from U3.A2. C14 grew from 0402 4.7 µF to 0402 10 µF at its previous site. C18 0402 10 µF TS/GND sits on B (15.07,20.70), 2.55 mm from U3.B1; R17 moved west 0.75 to leave its courtyard and GND return free. C19 0402 10 µF OUT bulk sits on F (14.10,34.20) for temperature margin. The F-side C18 trial conflicted with the IN1P/IN1N crossing; D1 stayed at the far VBUS end. The router did not finish GND_C, but `v4_finish.sh` closed it and the secondary LED_EN open with DRC 0 (§9.1).

### 9.3 Thermal connections (the starved-thermal decision)

DRC's starved-thermal check stays at KiCad's default: a GND pad with a thermal relief needs two spokes. No `min_resolved_spokes` rule; that would be a waiver, and the r12 review asked for zero errors under the project rules.

- **Exposed pads and mounting pads connect solid** (`elicio-v4.kicad_dru`, rule "GND exposed and mounting pads solid"): U2 pad 33, U4 pad 5, U5 pad 5 and J2's two MP pads. They are reflowed, not hand-soldered, sit under their part and want the copper. A relief has no job there.
- **Reliefs stay on every 0201 and 0402 pad** so nothing tombstones.
- **Second connections are copper:** where the pour reaches a pad from one side only (its other sides are 0.10 routing), a 0.10 GND track runs from inside the pad through the 0.15 thermal gap into the pour, placed by `v4_thermal_stubs.py` and checked by DRC like any track. 5 such tracks on the t-0036 board:
  - U1.1 F.Cu: stub (9.550, 25.700) -> (9.350, 25.700) 0.200 mm
  - U1.14 F.Cu: stub (6.550, 28.600) -> (6.550, 28.825) 0.225 mm
  - U1.18 F.Cu: stub (6.550, 29.500) -> (6.550, 29.275) 0.225 mm
  - R21.2 B.Cu: stub (12.950, 27.600) -> (13.150, 27.575) 0.202 mm
  - C19.2 F.Cu: stub (14.400, 33.900) -> (14.600, 33.950) 0.206 mm
- U2's pads 10, 13 and 24 had stubs in t-0014's state. They are now tied to the exposed pad by locked copper (§9.2 relief 7), and DRC finds no starved thermal on them.

No Contact, creepage or clearance rule changed; the three Q84 rules are as in v2.

### 9.4 The open connections, closed

t-0014 left 10 connections open (5 GND, 2 AFE_VIN, 1 AFE_DRDY, 1 CHG_MON, 1 VBUS_DET). All are closed on the committed board. What changed at each spot (reliefs in §9.2):

| t-0014 open piece | What changed |
|---|---|
| AFE_DRDY: U1.46 to R27, across AFE_MOSI on F | The dividers at u 12.40 leave s 25.05–26.5 free for DRDY's hop to R27 on B (relief 6) |
| AFE_VIN: B tracks at u 8.30–10.62 × s 19.50–19.93, across AFE_EN_HW | AFE_EN_HW is a short hop to Q2.3 after the interlock moved north (relief 6); AFE_VIN is locked (relief 8) |
| AFE_VIN: U4.3, U4.4 to Q1.3, across VBAT and AFE_GATE | Q1 turned so AFE_VIN faces U4 (relief 6); AFE_GATE is locked through Q1's pad gap (relief 8) |
| CHG_MON: U1.44, across AFE_EN_HW on B | AFE_EN_HW no longer runs south past U1 (relief 6); CHG_MON is locked (relief 8) |
| VBUS_DET: R18.2, R19.1 to U1, across CHG_MON on B | U1's east pads have a second via column at u 11.3 (relief 6) |
| GND: U2.10, U2.13, U2.24, U2.33 inside U2's pad ring | Pads 10, 13 and 24 are tied to the exposed pad, which has its own via (relief 7) |
| GND: U4.2, U4.5 | The exposed-pad via reaches them on B (relief 7) |
| GND: C14.2, C8.2 | C8.2 is on the exposed-pad via (relief 7); C14 moved to the east pocket beside R20.1 (relief 6) |
| GND: C11.2 | C11 moved to F; pin 24's exit reaches C11.2 and C15.2 (reliefs 6, 8) |
| GND: P5's run, 0.37 from U3.C2 across ISET | The top-edge link from P5's run to R11.2 (relief 10) and the GND via for U3.C2's corner (relief 9) |

The opens that came up on the way were AFE_IN1N's forced crossing (run 2) and two GND islands (run 4). Reliefs 9 and 10 closed them. On t-0036 the finisher additionally closed an LED_EN open at (12.40,29.77) to R28.1, then joined the GND island it displaced at C6.2; no opens remain.

### 9.5 Rebuild and re-route

The current board came from this sequence (scratch copies in `$W`; DRC needs `<stem>.kicad_pro`, `.kicad_dru` and `.kicad_sch` beside each copy; one router or KiCad batch at a time):

```bash
cd hardware/board
KP=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3
PY=../../.venv/bin/python
python3 gen_v4_sch.py                                   # schematic and project (netclasses); ERC must be clean
$KP build_v4.py --out $W/new.kicad_pcb                  # placed board, locked pre-routes, pour outlines (no fill); "keep-out problems 0"
$PY v4_gnd_split.py $W/new.kicad_pcb $W/news.kicad_pcb \
    GND_A:C6.2,C7.2,C9.2,C10.2,C17.2,C19.2,R23.2,U1.1,U1.7 \
    GND_B:C2.2,C3.2,C18.2,C4.2,J2.2,R11.2,R12.2,R13.2,U3.C2,P5.1 \
    GND_C:U2.10,U2.13,U2.24,U2.33,U4.2,U4.5,C8.2,C5.2,Q2.2,Q3.2,C15.2,C11.2,R17.2,R34.2,R35.2,R24.2,R19.2,R21.2,R28.2,D1.2,Q4.2
$PY -u v4_route_pf.py --pcb $W/news.kicad_pcb --out $W/r.kicad_pcb --fresh --skip GND --rounds 80 --debug $W/r_conf.json
zsh v4_finish.sh $W/r.kicad_pcb f                       # finisher (below) → $W/f_final.kicad_pcb, saved with filled zones
cp $W/f_final.kicad_pcb elicio-v4.kicad_pcb
cd ../.. && .venv/bin/python -m unittest discover -s tests -q && .venv/bin/python scripts/board/release.py --board elicio-v4 --routed
```

The three GND regions are the west plus C19 (GND_A), the charger corner with P5 plus C3/C18 (GND_B), and U2's core with every pad the locked GND copper touches (GND_C). On the t-0036 pass the router at round 79 had zero conflicts but reported `failed ['GND_C']`; the finisher joined its missing pieces. `v4_finish.sh` drops the conflicting copper and reconnects every net with the GND regions still live, restores the GND name, refills, runs the GND finisher with the pours as copper and the stitcher twice, adds thermal stubs, runs the soft-fill finisher on whatever is still open, and ends with a DRC with `--schematic-parity`. On t-0019 run 5 the finisher added 66 items and joined GND_A near C6.2. On t-0036 the finisher needed a soft-fill LED_EN reroute and then rejoined GND near C6.2; its final DRC has 0 errors and 0 opens and places the 5 thermal stubs of §9.3.

`build_v4.py` overwrites the PCB, routing included, so route in scratch copies. `v4_pieces.py PCB NET` lists a net's pieces with their gaps; `v4_route_pf.py --debug` writes the conflict cells, which show where a knot is. Freerouting instead: `scripts/board/route_v4.py --work DIR --route`, one run at a time, `-Xmx4g`.

## 10. Flat and folded tables

### 10.1 Flat PCB coordinates (u, s)

From `python3 hardware/board/v4_tables.py --pads` on the t-0036 routed board. Part centres, then pad by pad for the connectors, rings, J4 and SW1. The Gerber carries these (PCB x, y = u, s).

| ref | side | x (u) | y (s) | rot | footprint |
|---|---|---:|---:|---:|---|
| C1 | bottom | 13.30 | 23.65 | 90 | `Capacitor_SMD:C_0201_0603Metric` |
| C2 | bottom | 11.95 | 17.55 | 180 | `Capacitor_SMD:C_0201_0603Metric` |
| C3 | top | 14.40 | 17.20 | -90 | `Capacitor_SMD:C_0402_1005Metric` |
| C4 | bottom | 7.25 | 17.45 | 180 | `Capacitor_SMD:C_0201_0603Metric` |
| C5 | bottom | 9.85 | 23.90 | 0 | `Capacitor_SMD:C_0201_0603Metric` |
| C6 | top | 7.75 | 22.66 | 90 | `Capacitor_SMD:C_0402_1005Metric` |
| C7 | top | 8.78 | 22.66 | 90 | `Capacitor_SMD:C_0201_0603Metric` |
| C8 | bottom | 11.65 | 22.55 | 180 | `Capacitor_SMD:C_0402_1005Metric` |
| C9 | top | 10.20 | 18.50 | 90 | `Capacitor_SMD:C_0402_1005Metric` |
| C10 | top | 9.10 | 18.60 | 90 | `Capacitor_SMD:C_0201_0603Metric` |
| C11 | top | 15.10 | 23.20 | -90 | `Capacitor_SMD:C_0201_0603Metric` |
| C12 | bottom | 3.10 | 18.30 | 180 | `Capacitor_SMD:C_0201_0603Metric` |
| C13 | bottom | 4.60 | 18.30 | 180 | `Capacitor_SMD:C_0201_0603Metric` |
| C14 | bottom | 14.15 | 27.20 | 0 | `Capacitor_SMD:C_0402_1005Metric` |
| C15 | top | 13.60 | 25.15 | 0 | `Capacitor_SMD:C_0201_0603Metric` |
| C16 | bottom | 4.70 | 17.15 | 90 | `Capacitor_SMD:C_0201_0603Metric` |
| C17 | top | 11.10 | 18.60 | 90 | `Capacitor_SMD:C_0201_0603Metric` |
| C18 | bottom | 15.07 | 20.70 | -90 | `Capacitor_SMD:C_0402_1005Metric` |
| C19 | top | 14.10 | 34.20 | 90 | `Capacitor_SMD:C_0402_1005Metric` |
| D1 | bottom | 14.30 | 28.60 | 180 | `Diode_SMD:D_SOD-882` |
| D2 | top | 14.65 | 26.10 | 0 | `LED_SMD:LED_0402_1005Metric` |
| J2 | top | 5.45 | 18.90 | -90 | `Connector_Molex:Molex_Pico-EZmate_Slim_202656-0021_1x02-1MP_P1.20mm_Vertical` |
| J3 | top | 22.40 | 19.40 | 0 | `Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Horizontal` |
| J4 | top | 10.00 | 35.40 | 0 | `Connector:Tag-Connect_TC2030-IDC-NL_2x03_P1.27mm_Vertical` |
| P1 | top | 5.90 | 5.29 | 0 | `elicio:RING_PAD_D5_H2.7` |
| P2 | top | 10.40 | -5.81 | 0 | `elicio:RING_PAD_D5_H2.7` |
| P3 | top | 8.50 | 43.00 | 0 | `elicio:RING_PAD_D5_H2.7` |
| P4 | bottom | 16.51 | 4.35 | 180 | `elicio:RING_1S_D4.6_NPTH2.7` |
| P5 | bottom | 16.51 | 12.10 | 180 | `elicio:RING_1S_D4.6_NPTH2.7` |
| Q1 | bottom | 9.85 | 22.80 | 0 | `Package_TO_SOT_SMD:SOT-883` |
| Q2 | bottom | 12.50 | 19.55 | 180 | `Package_TO_SOT_SMD:SOT-883` |
| Q3 | bottom | 10.65 | 19.90 | 180 | `Package_TO_SOT_SMD:SOT-883` |
| Q4 | top | 14.60 | 28.00 | 0 | `Package_TO_SOT_SMD:SOT-883` |
| R1 | bottom | 5.90 | 17.30 | -90 | `Resistor_SMD:R_0402_1005Metric` |
| R2 | bottom | 9.39 | 17.25 | 180 | `Resistor_SMD:R_0402_1005Metric` |
| R3 | bottom | 14.55 | 25.60 | 180 | `Resistor_SMD:R_0402_1005Metric` |
| R4 | bottom | 13.30 | 22.15 | -90 | `Resistor_SMD:R_0201_0603Metric` |
| R5 | top | 11.40 | 31.12 | 90 | `Resistor_SMD:R_0201_0603Metric` |
| R6 | top | 11.40 | 29.63 | 90 | `Resistor_SMD:R_0201_0603Metric` |
| R7 | top | 11.05 | 25.50 | 90 | `Resistor_SMD:R_0201_0603Metric` |
| R8 | top | 11.40 | 32.61 | 90 | `Resistor_SMD:R_0201_0603Metric` |
| R11 | bottom | 12.00 | 16.75 | 180 | `Resistor_SMD:R_0201_0603Metric` |
| R12 | top | 12.60 | 18.15 | 180 | `Resistor_SMD:R_0201_0603Metric` |
| R13 | top | 13.25 | 18.97 | 180 | `Resistor_SMD:R_0201_0603Metric` |
| R14 | bottom | 9.85 | 21.85 | 0 | `Resistor_SMD:R_0201_0603Metric` |
| R15 | bottom | 10.80 | 18.60 | -90 | `Resistor_SMD:R_0201_0603Metric` |
| R16 | bottom | 13.75 | 19.70 | -90 | `Resistor_SMD:R_0201_0603Metric` |
| R17 | bottom | 13.70 | 20.85 | 0 | `Resistor_SMD:R_0201_0603Metric` |
| R18 | bottom | 12.40 | 28.50 | 180 | `Resistor_SMD:R_0201_0603Metric` |
| R19 | bottom | 12.40 | 29.30 | 0 | `Resistor_SMD:R_0201_0603Metric` |
| R20 | bottom | 12.40 | 26.90 | 180 | `Resistor_SMD:R_0201_0603Metric` |
| R21 | bottom | 12.40 | 27.70 | 0 | `Resistor_SMD:R_0201_0603Metric` |
| R22 | top | 14.60 | 27.02 | 180 | `Resistor_SMD:R_0201_0603Metric` |
| R23 | top | 7.95 | 24.10 | 180 | `Resistor_SMD:R_0201_0603Metric` |
| R24 | bottom | 11.45 | 24.70 | 0 | `Resistor_SMD:R_0201_0603Metric` |
| R25 | bottom | 11.95 | 18.35 | 180 | `Resistor_SMD:R_0201_0603Metric` |
| R27 | top | 12.45 | 25.50 | -90 | `Resistor_SMD:R_0201_0603Metric` |
| R28 | top | 13.35 | 27.70 | 90 | `Resistor_SMD:R_0201_0603Metric` |
| R31 | top | 22.40 | 16.80 | 0 | `Resistor_SMD:R_0402_1005Metric` |
| R32 | top | 18.00 | 21.15 | 0 | `Resistor_SMD:R_0402_1005Metric` |
| R33 | top | 22.40 | 27.10 | 0 | `Resistor_SMD:R_0402_1005Metric` |
| R34 | bottom | 14.95 | 23.22 | -90 | `Resistor_SMD:R_0201_0603Metric` |
| R35 | bottom | 14.40 | 24.55 | 0 | `Resistor_SMD:R_0201_0603Metric` |
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

From `python3 hardware/board/v4_tables.py --folded` on the t-0036 routed board. These are the prebuild board-to-shell targets, not measured clearances in the later built snap solid; see `shell-v4.md` for those checks. Shell u, s = flat u, s for everything that stays flat (the island and its parts); y comes from the thickness chain (§1.2) and the fold math (§4.4). Courtyards are line-centre boxes from the footprint text (the drawn line is 0.05 wide). The original v4 target body was the r9 shell (branch `hp/elicio/t-0001-finish-the-earpiece-shell-v2f-wp14f-from`, 252afbb, not merged) with §7's changes on paper: walls u 1.5/16.5, floor 1.5, LID_Y 7.1, rib s 14.9–15.7 (y ≤ 4.5), bay s 15.7–38.2, EMG hex collars AF 8.4 (top y 3.5) at the P1/P2 sites, standoff landings R 3.2, lid posts Ø2.0, r9's SIG fold pockets and REF end-wall slot. Margins are in mm; a row passes when every margin is ≥ 0. F parts stand on the island top (y 5.12) under the lid; B parts hang from the island underside (y 5.01) over the collar top (3.5) where a collar box is below them, else over the floor (1.5). Heights are maxima from the sources in the table; the ones marked UNVERIFIED are package maxima (§11.1). The P2 lid post on U1 is by design (§5.3).

#### Courtyards on the island (flat u, s = shell u, s; y from the fold math)

| ref | side | courtyard u | courtyard s | h (source) | y | wall u | rib/end s | lid or floor y | lid post | landing | test |
|---|---|---:|---:|---|---|---:|---:|---:|---:|---:|---|
| C1 | bottom | 12.95-13.65 | 22.95-24.35 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 2.85 | 7.25 | 3.16 (floor) | - | 3.91 | ok |
| C2 | bottom | 11.25-12.65 | 17.20-17.90 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 3.85 | 1.50 | 3.16 (floor) | - | 3.54 | ok |
| C3 | top | 13.94-14.86 | 16.29-18.11 | 0.60 (0402 C max, UNVERIFIED) | 5.12-5.72 | 1.64 | 0.59 | 1.38 (lid) | 8.41 | - | ok |
| C4 | bottom | 6.55-7.95 | 17.10-17.80 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 5.05 | 1.40 | 1.16 (collar) | - | 1.05 | ok |
| C5 | bottom | 9.15-10.55 | 23.55-24.25 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 5.95 | 7.85 | 1.16 (collar) | - | 0.40 | ok |
| C6 | top | 7.29-8.21 | 21.75-23.57 | 0.60 (0402 C max, UNVERIFIED) | 5.12-5.72 | 5.79 | 6.05 | 1.38 (lid) | 0.39 | - | ok |
| C7 | top | 8.43-9.13 | 21.96-23.36 | 0.35 (0201 max, UNVERIFIED) | 5.12-5.47 | 6.93 | 6.26 | 1.63 (lid) | 1.53 | - | ok |
| C8 | bottom | 10.74-12.56 | 22.09-23.01 | 0.60 (0402 C max, UNVERIFIED) | 4.41-5.01 | 3.94 | 6.39 | 2.91 (floor) | - | 1.64 | ok |
| C9 | top | 9.74-10.66 | 17.59-19.41 | 0.60 (0402 C max, UNVERIFIED) | 5.12-5.72 | 5.84 | 1.89 | 1.38 (lid) | 4.26 | - | ok |
| C10 | top | 8.75-9.45 | 17.90-19.30 | 0.35 (0201 max, UNVERIFIED) | 5.12-5.47 | 7.05 | 2.20 | 1.63 (lid) | 3.67 | - | ok |
| C11 | top | 14.75-15.45 | 22.50-23.90 | 0.35 (0201 max, UNVERIFIED) | 5.12-5.47 | 1.05 | 6.80 | 1.63 (lid) | 7.85 | - | ok |
| C12 | bottom | 2.40-3.80 | 17.95-18.65 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 0.90 | 2.25 | 1.16 (collar) | - | 0.75 | ok |
| C13 | bottom | 3.90-5.30 | 17.95-18.65 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 2.40 | 2.25 | 1.16 (collar) | - | 0.20 | ok |
| C14 | bottom | 13.24-15.06 | 26.74-27.66 | 0.60 (0402 C max, UNVERIFIED) | 4.41-5.01 | 1.44 | 10.54 | 2.91 (floor) | - | 2.94 | ok |
| C15 | top | 12.90-14.30 | 24.80-25.50 | 0.35 (0201 max, UNVERIFIED) | 5.12-5.47 | 2.20 | 9.10 | 1.63 (lid) | 6.23 | - | ok |
| C16 | bottom | 4.35-5.05 | 16.45-17.85 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 2.85 | 0.75 | 1.16 (collar) | - | 1.04 | ok |
| C17 | top | 10.75-11.45 | 17.90-19.30 | 0.35 (0201 max, UNVERIFIED) | 5.12-5.47 | 5.05 | 2.20 | 1.63 (lid) | 5.10 | - | ok |
| C18 | bottom | 14.61-15.53 | 19.79-21.61 | 0.60 (0402 C max, UNVERIFIED) | 4.41-5.01 | 0.97 | 4.09 | 2.91 (floor) | - | 5.52 | ok |
| C19 | top | 13.64-14.56 | 33.29-35.11 | 0.60 (0402 C max, UNVERIFIED) | 5.12-5.72 | 1.94 | 3.09 | 1.38 (lid) | 3.40 | - | ok |
| D1 | bottom | 13.50-15.10 | 28.00-29.20 | 0.50 (Nexperia SOD882 body 0.5) | 4.51-5.01 | 1.40 | 9.00 | 1.01 (collar) | - | 1.78 | ok |
| D2 | top | 13.72-15.58 | 25.63-26.57 | 0.55 (0402 LED, UNVERIFIED) | 5.12-5.67 | 0.92 | 9.93 | 1.43 (lid) | 6.02 | - | ok |
| J2 | top | 2.34-8.38 | 16.15-21.65 | 1.20 (§1.2 mated) | 5.12-6.32 | 0.84 | 0.45 | 0.78 (lid) | 0.35 | - | ok |
| J3 | top | 20.63-32.94 | 17.63-26.25 | 0.00 (no height: UNVERIFIED) | cut off with the tab (Q91) | - | - | - | - | - | exterior |
| J4 | top | 6.50-13.50 | 33.40-37.40 | 0.00 (pads only) | 5.12-5.12 | 3.00 | 0.80 | 1.98 (lid) | 0.30 | - | ok |
| Q1 | bottom | 9.15-10.55 | 22.30-23.30 | 0.40 (DFN1006 max, UNVERIFIED) | 4.61-5.01 | 5.95 | 6.60 | 1.11 (collar) | - | 0.06 | ok |
| Q2 | bottom | 11.80-13.20 | 19.05-20.05 | 0.40 (DFN1006 max, UNVERIFIED) | 4.61-5.01 | 3.30 | 3.35 | 3.11 (floor) | - | 3.01 | ok |
| Q3 | bottom | 9.95-11.35 | 19.40-20.40 | 0.40 (DFN1006 max, UNVERIFIED) | 4.61-5.01 | 5.15 | 3.70 | 1.11 (collar) | - | 1.15 | ok |
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
| R13 | top | 12.55-13.95 | 18.62-19.32 | 0.35 (0201 max, UNVERIFIED) | 5.12-5.47 | 2.55 | 2.92 | 1.63 (lid) | 6.60 | - | ok |
| R14 | bottom | 9.15-10.55 | 21.50-22.20 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 5.95 | 5.80 | 1.16 (collar) | - | 0.05 | ok |
| R15 | bottom | 10.45-11.15 | 17.90-19.30 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 5.35 | 2.20 | 3.16 (floor) | - | 2.09 | ok |
| R16 | bottom | 13.40-14.10 | 19.00-20.40 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 2.40 | 3.30 | 3.16 (floor) | - | 4.47 | ok |
| R17 | bottom | 13.00-14.40 | 20.50-21.20 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 2.10 | 4.80 | 3.16 (floor) | - | 3.94 | ok |
| R18 | bottom | 11.70-13.10 | 28.15-28.85 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 3.40 | 9.35 | 1.16 (collar) | - | 1.24 | ok |
| R19 | bottom | 11.70-13.10 | 28.95-29.65 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 3.40 | 8.55 | 1.16 (collar) | - | 0.49 | ok |
| R20 | bottom | 11.70-13.10 | 26.55-27.25 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 3.40 | 10.85 | 3.16 (floor) | - | 2.79 | ok |
| R21 | bottom | 11.70-13.10 | 27.35-28.05 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 3.40 | 10.15 | 3.16 (floor) | - | 2.01 | ok |
| R22 | top | 13.90-15.30 | 26.67-27.37 | 0.35 (0201 max, UNVERIFIED) | 5.12-5.47 | 1.20 | 10.83 | 1.63 (lid) | 5.53 | - | ok |
| R23 | top | 7.25-8.65 | 23.75-24.45 | 0.35 (0201 max, UNVERIFIED) | 5.12-5.47 | 5.75 | 8.05 | 1.63 (lid) | 0.54 | - | ok |
| R24 | bottom | 10.75-12.15 | 24.35-25.05 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 4.35 | 8.65 | 3.16 (floor) | - | 2.19 | ok |
| R25 | bottom | 11.25-12.65 | 18.00-18.70 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 3.85 | 2.30 | 3.16 (floor) | - | 3.09 | ok |
| R27 | top | 12.10-12.80 | 24.80-26.20 | 0.35 (0201 max, UNVERIFIED) | 5.12-5.47 | 3.70 | 9.10 | 1.63 (lid) | 5.46 | - | ok |
| R28 | top | 13.00-13.70 | 27.00-28.40 | 0.35 (0201 max, UNVERIFIED) | 5.12-5.47 | 2.80 | 9.80 | 1.63 (lid) | 4.16 | - | ok |
| R31 | top | 21.47-23.33 | 16.33-17.27 | 0.45 (0402 R max, UNVERIFIED) | cut off with the tab (Q91) | - | - | - | - | - | exterior |
| R32 | top | 17.07-18.93 | 20.68-21.62 | 0.45 (0402 R max, UNVERIFIED) | cut off with the tab (Q91) | - | - | - | - | - | exterior |
| R33 | top | 21.47-23.33 | 26.63-27.57 | 0.45 (0402 R max, UNVERIFIED) | cut off with the tab (Q91) | - | - | - | - | - | exterior |
| R34 | bottom | 14.60-15.30 | 22.52-23.92 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 1.20 | 6.82 | 3.16 (floor) | - | 5.52 | ok |
| R35 | bottom | 13.70-15.10 | 24.20-24.90 | 0.35 (0201 max, UNVERIFIED) | 4.66-5.01 | 1.40 | 8.50 | 3.16 (floor) | - | 4.90 | ok |
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
- **LCSC codes missing:** ISP1807, TPS7A0230 and Molex 202656 (none in the JLC library); 47 kΩ and 27 kΩ 0201. The exact Murata C3/C14/C18/C19 ESD capacitor MPN has no verified JLC supply code; those lines are marked CONSIGNED.
- **P4 ESD not demonstrated:** D1 is ≥ 11.06 mm straight-line from U3.A2 and behind it on the VBUS trunk; U3's conditional 8 kV contact / 15 kV air IN rating has the three effective capacitors numerically at 25 °C, but the nearest OUT bulk C14 is 9.27 mm away (C19 is 16.73 mm), no P4 contact-level IEC test was done, and bias/temperature/aging/assembly variation is not measured (§2.1). Do not equate the routed release with ESD proof.
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
- **P4/P5 keying walls and the closure** (§7): the r9 shell was not rebuilt; the later `v4-snap` trial solid includes these features, but its physical latch, keying-wall retention and print tolerance remain UNVERIFIED (`shell-v4.md`).

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
| TI TLV713P (SBVS195F), TPS7A02 (SBVS277C), ADS1292 (SBAS502C), BQ25100 (SLUSBV8C §7.2) | 2026-09-23; BQ25100 ESD conditions revisited 2026-09-25 |
| Murata SimSurfing C-DC bias graph GRM155R61A106ME18, 25 °C, AC 0.1 Vrms (reproducible links in §2.1); maker CSV `https://ds.murata.com/simsurfing_data/data/mlcc.csv` (X5R, 10 V, 0402, ±20%) | 2026-09-25 |
| Repo: `docs/fab/board-v2.md`, `plan-v2.md`, `open-questions.md`, `packing-v2.md`, `shell-v2.md`, `docs/EARPIECE_DESIGN.md`, `hardware/board/v4_parts.py`, `build_v4.py`, `make_v4_lib.py` | 2026-09-23 |
