# Elicio fabrication plan v2 — draft, turn 01 (2026-09-17)

Status: DRAFT in spec dialogue (`tasks/plan-v2/turns/`). When signed off it
supersedes the named sections of `docs/fab/plan.md` (signed off at
`0c5d0eb`); every other section of v1 stands. Until sign-off nothing is
ordered. Inputs: plan v1; `docs/fab/open-questions.md` Q1–Q36; the merged
code of rounds 1 to 4 (`scripts/cad/`, `docs/fab/interface.md` v2,
`docs/fab/packing-options.md`, `docs/fab/contacts.md` §8,
`docs/fab/montage.md`); the research `docs/fab/L5-research-v2.md` on
`lane/w5` at `832ef28`, unreviewed, its numbers to be verified in this
dialogue. Rolf is the client; "Rolf" throughout.

## 0. What Rolf asked on 2026-09-17, and what v2 does about it

| His words | v2 |
|---|---|
| "I literally don't have the financial means to order several versions" | One shell, one assembled board, one bag of small parts, each ordered once. No gauge order. Fit is gated by his measurements, a 1:1 paper template from the drawing, and the existing check suite. §1, §9 |
| "I need want this to look prettier" | A design language with rules a script can check, two renders he approves before the one order. §7 |
| "No we design it properly custom order it" | A board designed in the repo, assembled by the vendor, no breadboard. The assembled board with gel electrodes is the bench that gives the contact sites. §4–§6 |
| "Body thickness: thin" | Not possible with any radio module and any battery, by arithmetic in §3. v2 builds the smallest body that closes, expected 8.5 to 9.0 mm, and says so to him plainly. Decision D-1 |
| "this will come put together right?" | No vendor does that. v2 makes final assembly a screwdriver job of eight steps, no soldering, glue or crimping: the board's own flex tabs are clamped under the contact nuts, the cell plugs in, the lid snaps. §8 |
| "do we actually have to get it from china?" | No. JLC is the default on price; each order names one non-China alternative with page prices. His country decides shipping and duties. D-8, §9 |

## 1. Decision summary v2

1. Orders: three, each once, in the order board → bench on the board →
   shell. §9, §10. Nothing is bought by an agent.
2. Body: full-height class, the minimum that closes; thin is dropped
   with the arithmetic in §3 (D-1). Width 20 (Q20, option C) unless WP11
   closes at less.
3. Contacts: unchanged from v1 §4: three Grade 2/5 titanium ISO 7380
   M2.5×4 button heads through a 1.5 mm medial wall, thin nuts inside.
   Nut metal brass DIN 439 M2.5 (Q28). The TE 31428 ring lug and the 28 AWG
   lead are replaced by the board's own flex tabs (D-3); Q23 becomes moot
   if D-3 holds.
4. Cell: Data Power DTP301120, 40 mAh, 3.2 × 11.5 × 22 mm with its
   protection circuit, JST-SH leads (SparkFun PRT-25270), if its drawing
   allows the charger's current (claim C3); else v1's 501015.
5. Electronics: TI ADS1292 (non-R) analog front end as v1 §5 and L4; the
   radio is one of three candidates chosen by the §4 rule after WP11:
   Seeed XIAO nRF52840 carrier, Ebyte E73-2G4M08S1C module, or Raytac
   MDBT50Q-1MV2 module.
6. Charging: USB-C. Where the port sits and what stops charging while
   worn is D-5.
7. Firmware: a streaming firmware only (SPI in, BLE out), the decoder
   stays on the laptop where it already lives. §6.
8. Look: §7 rules; media-blasted matte; colour per Rolf (Q30); vapour
   smoothing only from a vendor with a skin-contact statement for the
   smoothed part.
9. Vendors: JLC3DP and JLCPCB by default; alternatives per order in §9;
   Rolf's country needed (Q36).
10. Budget: estimated $200–260 for everything at page prices, §9; his
    ceiling (Q33) caps it.

## 2. Requirements v2 (each testable)

- R1 One order per physical thing. A second print or a second board is a
  failure of this plan, not a step in it.
- R2 Final assembly by Rolf: at most eight steps, one small screwdriver,
  no soldering, glue, crimping or wire stripping. §8 is the list.
- R3 Skin-side materials as v1 §6: titanium domes, PA12 with a
  skin-contact certificate for the finish actually ordered, no resin.
- R4 The body is the smallest that closes every WP11 check on the built
  solid with the chosen architecture. No fixed thickness is promised.
- R5 Look rules of §7 pass as script checks where they can be checked
  (curvature continuity, no visible fasteners, seam width), and Rolf
  approves two renders before the order.
- R6 Works first try: every electrical function follows a manufacturer
  reference design or lives inside a proven module; every geometry check
  runs on the built solid; the board passes ERC and DRC against the
  assembler's rules; the paper template and the chord gate pass on his
  measurements. Nothing is ordered with a failing check.
- R7 No charging while worn, by a physical interlock or by a firmware
  interlock plus a covered port, decided in D-5.
- R8 The sum of the three orders at page prices stays under Rolf's
  ceiling (Q33).

## 3. Packaging arithmetic (why thin is out)

Facts on file: v1 full body outer 9.0 with floor 1.5 and lid at 8.0, cavity
height 6.5; thin body lid at 6.0, cavity 4.5 (Q27). Contact stack inside
the wall ≤ 2.63 on catalog drawings (v1 WP5). Modules: E73 13 × 18 × 2.0;
Raytac 10.5 × 15.5 × 2.0; XIAO 21 × 17.5 × 4.5 with its USB-C. Cells:
501015 5.4 thick (v1); DTP301120 3.2 thick with protection. Board: flex
0.11 plus stiffener, 0.4 total where parts sit. Foam under a cell 0.3.

- Cell over a module: 0.4 + 2.0 + 3.2 + 0.3 = 5.9. Fits 6.5, not 4.5.
- Cell over the contact region: 2.63 + 0.2 tab + 3.2 + 0.3 = 6.3. Fits
  6.5, not 4.5, and leaves no room for the front end there.
- Thinnest conceivable: an unprotected 22 mAh cell (2.3) over a module,
  0.4 + 2.0 + 2.3 = 4.7. Still over 4.5, and unprotected cells are out
  (v1 §6).
- Side by side in width: 13 + 11.5 = 24.5 against a 17.6 cavity. Out.

So a thin body cannot hold a radio and a battery. The full body can, and
may come down to about 8.5 if WP11 finds the stack has slack. The
alternative that would make thin work is no battery in the body at all
(a wired pod), which the design record rejects. D-1 asks Rolf to accept
this.

## 4. Architecture candidates and the rule that picks one

| | A. Raytac MDBT50Q-1MV2 | B. Ebyte E73-2G4M08S1C | C. Seeed XIAO nRF52840 |
|---|---|---|---|
| Footprint, height | 10.5 × 15.5 × 2.0 | 13 × 18 × 2.0 | 21 × 17.5 × 4.5 (USB-C) |
| Stock for the assembler | out at LCSC; buy at DigiKey and consign (a Rolf shipment) | in stock at LCSC, extended | not at LCSC; consign, or a non-China assembler that buys from DigiKey |
| First firmware load | SWD once: assembler's programming service if it exists (C6), else Rolf with a pogo clip and a $6 debug probe | same | none: UF2 bootloader on board, drag and drop over USB |
| Charger | BQ25100 on the board, current set by one resistor to the cell's limit | same | on the XIAO, fixed 50 mA (100 mA by pin), cannot be lowered (C3) |
| USB | own USB-C receptacle on the board | same | the XIAO's own |
| Packing | v1 option C closes as is (series layout, 501015) | needs about +1.5 mm length or the stacked layout | needs the stacked layout and a 4.5 mm zone; open |
| RF risk | none inside the module; antenna keep-out from its sheet | same | none |
| Rolf steps beyond §8 | consignment shipment, one SWD session or none | one SWD session or none | none |

Rule, applied by WP11's report: (1) it closes in a body ≤ 9.0 high and
20 wide with every check on the built solid and TOTAL_CHORD ≤ M1 − 3;
(2) every part is orderable from the assembler's library or from a
distributor that assembler accepts, consignment counted as a Rolf step
and a shipment; (3) fewest Rolf steps; (4) lowest page price. Ties go to
A. Reading before WP11 runs: C if it closes and the cell's sheet allows
50 mA; else B with the programming service; else A.

## 5. The board (WP12)

- Repository: `hardware/board/` as a KiCad project committed as files;
  ERC and DRC run headless with `kicad-cli` against the assembler's
  capability rules in CI (`tests/` gains a board test that skips when
  `kicad-cli` is absent and fails on any DRC error when present).
- Construction: one flex board (polyimide, two copper layers) with FR4
  stiffeners under the module and the front end, and three bare flex tabs
  ending in tinned ring pads that the contact nuts clamp (D-3). No wires,
  no lugs, no solder by Rolf. Fallback if the assembler cannot assemble
  flex at this size: rigid 4-layer board plus three short flex jumpers
  soldered by the assembler at one end and clamped at the other.
- Front end: ADS1292 per L4 and v1 §5; SIG1, SIG2 to one differential
  channel at gain 12, 500 SPS; the reference contact to the bias (RLD)
  output; input protection per the ADS1292 datasheet's reference schematic;
  the 2.5 V/3.3 V rails from the module's regulator or a TLV713.
- Connectors: JST-SH receptacle for the cell; USB-C 16-pin receptacle with
  the two 5.1 kΩ CC resistors (A, B); SWD and UART test pads at the edge.
- Finish: immersion tin or OSP if the flex process offers it, ENIG
  otherwise; nickel inside the sealed cavity is on v1 §4's internal-metal
  list, never skin-side.
- Outputs: Gerbers, BOM with LCSC numbers, placement file, 3D STEP of the
  populated board for the shell's checks, `docs/fab/board.md` with every
  design value traced to a datasheet page.

## 6. Firmware (WP13, after the board arrives)

nRF Connect SDK (Zephyr); for C also an Arduino path. Functions, all
minimal: ADS1292 over SPI at 500 SPS; BLE Nordic UART Service streaming
raw samples; battery voltage; LED state; VBUS present → front end off and
a refusal to stream (part of D-5). The existing laptop pipeline receives
and decodes; `docs/fab/montage.md` §2 is re-targeted from the breadboard
to this board: gel electrodes on the board's flex tabs with a clip, sites
found on Rolf's head before the shell prints. §3 of that file (frozen
protocol, accepted Q28) is unchanged.

## 7. Look (WP14, shell v2 in build123d on the existing builder)

- Surfaces: the lateral shell is one continuously curved surface, G2
  where build123d can make it, no planar facets larger than 3 mm, no
  visible edge sharper than R1.0 except the medial face that meets the
  skin (flat, R0.5 edges).
- Parting: the lid becomes the whole lateral shell; the seam runs along
  the perimeter at mid-height as a 0.4 mm feature groove, tongue and lip
  inside it (v1 §3.6 closure without E1, Q25).
- Nothing on the outside but the three titanium domes and the USB port
  if D-5 puts it outside; no text outside; a version mark inside the lid.
- Hook: elliptical section tapering toward the tip; blended into the body
  with the largest fillet that builds (Q3).
- Tail: blended, no step; the reference dome centred on the bone per Q17
  (his "on bone" stands provisionally).
- Finish: media-blasted matte; grey or dyed black per Q30; vapour
  smoothing only where the vendor's page states skin-contact testing of
  the smoothed part (C8).
- Approval: two renders and one drawing page, his yes before the order.

## 8. Final assembly by Rolf, eight steps

1. Peel the backing off the cell's foam pad, lay the cell in its pocket.
2. Lay the board in; its tabs fall over the three holes.
3. Push each titanium screw through its dome hole from outside.
4. Inside, drop a brass nut over each screw tip through the ring pad;
   tighten with the small screwdriver from outside until snug.
5. Plug the cell into the board.
6. Snap the lid on.
7. Plug in USB-C; the LED shows charging.
8. Copy the firmware file to the drive that appears (C), or nothing (A/B,
   already programmed).

A step that needs a tool other than the screwdriver fails R2.

## 9. Orders v2 and budget (page prices from L2, L5, v1 §7; verify C1–C10)

| Order | Contents | Default vendor | Non-China alternative | Estimate |
|---|---|---|---|---|
| 1 Board | 2 to 5 assembled boards (assembler's minimum), spares stay spares | JLCPCB economic PCBA: setup $8.18, stencil $1.53, extended feeders ~$3 each, parts ~$20–35 per board, boards ~$5, shipping ~$20–25 | Aisler (EU) or MacroFab / Screaming Circuits (US), parts from DigiKey/Mouser, no consignment; expect 2–4× | $90–140 |
| 2 Shell | body, lid, spare lid, MJF PA12 | JLC3DP, DDP | Xometry (skin-tested vapour smoothing), Craftcloud, Sculpteo, i.materialise | $40–70 |
| 3 Small parts | 10 titanium screws (Sortafast $17.50), 10 brass nuts (TME $1.60), cell ($7.39), foam, nickel test kit, shipping | Sortafast, TME, SparkFun/DigiKey | same, they are not in China | $55–75 |

Total $185–285 at page prices, before Rolf's country's duties. If R8
fails against his ceiling, the first cuts are: economic instead of
standard assembly (already assumed), grey instead of dyed, no spare lid.

## 10. Release states v2

| State | Entry requires |
|---|---|
| S0 files approved | WP11 closes; WP12 ERC/DRC clean and reviewed against the reference schematics; WP14 checks pass on the built solid; renders approved by Rolf; paper template and chord gate pass on his M1; budget under ceiling |
| S1 board ordered | S0; Rolf places order 1 (and order 3 parts) |
| S2 bench | boards arrive; firmware streams; gel-electrode montage on the board gives the three sites; continuity and leakage checks; DMG nickel screen on the domes |
| S3 shell ordered | S2 sites in interface v3; WP14 re-run on them; renders re-approved only if the shape changed; Rolf places order 2 |
| S4 assembled, validation wear | §8 done; the frozen protocol of `montage.md` §3 run as v1 S3 |
| S5 routine use | all protocol criteria pass |

D-7 asks whether the shell may be ordered with S1 instead of after S2, at
the risk of one reprint if the sites move.

## 11. Work packages v2

| WP | Owns | Output | Acceptance |
|---|---|---|---|
| 11 Packing v2 | `scripts/cad/placement.py`, `bte_fit_shell.py` Stage B, `docs/fab/packing-v2.md` | A, B, C laid out with the real module, cell and flex tabs, stacked and series, at widths 18–20 and heights 8.0–9.0; the §4 rule applied; the winner's interface v3 draft | every number measured on the built solid; the report says which close and at what M1 gate |
| 12 Board | `hardware/board/`, `docs/fab/board.md` | KiCad project, ERC/DRC clean, BOM, STEP | every value traced; DRC against the assembler's rules; reviewed against the ADS1292 and module reference designs |
| 13 Firmware | `firmware/` | streaming firmware, build in CI | builds; bench-tested at S2 |
| 14 Shell v2 | `scripts/cad/`, `docs/fab/cad/v2/` | body, lid, renders, drawing, manifest | §7 checks; all Stage B checks on the built solid; byte-identical regeneration |
| 15 Rolf's sheets v2 | `docs/fab/measure.md`, `order-board.md`, `order-shell.md`, `assemble.md`, `template.pdf` | measurement sheet, 1:1 template with a 50 mm calibration bar, two checkout gates, the §8 steps with pictures | no step needs a question |
| 16 Record | `docs/EARPIECE_DESIGN.md`, requirement 5 | v2 decisions once each; requirement 5 to titanium (Q28) | each decision appears once |

One round each for 11 and 12 in parallel, then 14 and 15, then 16; 13
after S1. Fresh reviewer per round, as before.

## 12. Claims to verify in this dialogue

- C1 JLC3DP MJF PA12/PA12S skin-contact and ISO 10993 statements, verbatim
  on a live page (L5 §2.1).
- C2 JLCPCB economic PCBA fees and the two-piece minimum (L5 §3.1).
- C3 DTP301120 maximum charge current on its drawing, against 50 mA.
- C4 XIAO nRF52840 height with USB-C 4.3–4.5 and charge current fixed at
  50/100 mA (L5 §4).
- C5 E73-2G4M08S1C in stock at LCSC as an extended part, and its antenna
  keep-out.
- C6 Whether JLCPCB (or the alternative assembler) programs an nRF52840
  over SWD as a service, and at what price.
- C7 JLCPCB flex PCB assembly at ~40 × 20 mm with stiffeners: offered,
  minimum, price.
- C8 A vendor page stating skin-contact testing of vapour-smoothed PA12
  (Xometry, L5 §2.2) and JLC's equivalent, if any.
- C9 Sortafast titanium ISO 7380 M2.5×4 grade and page; TME BN 147 page.
- C10 ADS1292 (non-R) availability at LCSC or DigiKey today.

## 13. Decisions for the dialogue, then Rolf

- D-1 Accept "smallest body that closes" (8.5–9.0) in place of "thin".
  Reading: yes; §3 leaves no alternative with a battery inside.
- D-2 Architecture rule of §4 and its pre-WP11 reading (C, else B, else A).
- D-3 Flex tabs under the nuts replace lugs and wires. Reading: yes.
- D-4 Cell DTP301120 (40 mAh, 3.2) or keep 501015 (50 mAh, 5.4). Reading:
  DTP301120 if C3 allows the charger; the height saved is the whole point.
- D-5 Charging interlock: (a) USB-C in the end wall under a silicone cap,
  firmware refuses to run the front end while VBUS is present; (b) port
  inside the cavity, lid off to charge, as v1. Reading: (a) for C, (b)
  for A/B where the receptacle can face the cavity; Pro to attack.
- D-6 Firmware scope: streaming only. Reading: yes.
- D-7 Shell order after the bench (S3) or with the board (S1). Reading:
  after; three weeks against a reprint Rolf cannot afford.
- D-8 Vendors: JLC default, alternatives named; Rolf's country needed.

Open for Rolf, on the answer sheet: M1 and the other measurements (Q34),
the budget ceiling (Q33), the look and colour (Q30), China or not and his
country (Q36), and D-1 in his own words.
