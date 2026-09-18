# Open questions after each round

Numbered items raised by round reviews of the fabrication plan
(`plan.md`, signed off at `0c5d0eb`). The plan stays the spec. Each item
records the reading the build follows until Rolf rules otherwise, who
closes it, and its status. New items append; numbers never change.

## Round 1 (review `tasks/reviews/code-r1.md`, merged 2026-09-17)

| # | Question | Reading the build follows | Closes it | Status |
|---|---|---|---|---|
| Q1 | Chord gate `>` (plan §3.3 table) or `≥` (plan §1, §2 row 17, §10) | `M1 ≥ TOTAL_CHORD + 3`; a 0.01 mm difference is below caliper resolution; the script and `measure.md` use ≥ | plan erratum, coordinator | decided |
| Q2 | HOOK_RADIUS: plan writes `M8 + HOOK_DIA/2 + 1.0` but quotes 13.5 at M8 = 11, which needs `+ 0.75`; the plan's form fails its own `< M8 + 1` bound | `M8 + HOOK_DIA/2 + 0.75`, strict `<`; 13.5 is the number every other document was built on | plan erratum, coordinator | decided |
| Q3 | Hook joint fillet 2.0 (§3.5 step 9) does not build: 1.5 on full p15, 1.75 on thin p15 and full p25, less at high bow | Largest radius that builds, recorded per body in `manifest.json` notes and on the WP3 drawing; it is strain relief, not a fit feature | Rolf may override at render approval | decided, provisional |
| Q4 | Lip root fillet 0.5 (§3.5 step 7) overlaps the seated body by 0.045 mm³ | 0.2 mm; E5 is an experiment the closure test decides | closure test (3.7 item 7) | decided |
| Q5 | Hook start at −5° sat inside the battery cavity; the reviewer cuts it back (4.6 mm³ at bow 3, about 20 at bow 8) | Cut it: the cavity is air by definition; the hook root outside is unchanged | none | decided |
| Q6 | Nut metal inside the cavity. Plan §4 allows plated steel or tinned copper; no plated-steel DIN 439 M2.5 found; 18-8 stainless is nickel-bearing and outside the text; titanium DIN 934 has zero stack margin at wall +0.3 | No purchase happens before S1, so nothing is blocked. Before S1, WP5 part 2 looks for a brass or tinned-brass DIN 439 M2.5 thin nut (nickel-free, stocked) as a candidate inside the plan's spirit, and shows its drawing. Rolf picks the metal | **Rolf** (interface §12 V2-3) | open |
| Q7 | Dome dimensions have no SKU drawing (interface §12 V2-1) | CAD keeps 4.7 × 1.35; the internal stack does not depend on the dome; a purchased SKU's drawing becomes interface v2 or v3 | WP5 part 2, before S1 | open |
| Q8 | LID_EDGE 0.8 not applied on the top edge at the lip so the lip keeps its full joint | Accept | none | decided |
| Q9 | Plan §3.1's single-variant command writing into `v1/` is refused by the stale-part guard | Keep the guard; single-variant builds go to a separate `--out` as the README says | plan erratum, coordinator | decided |
| Q10 | Lid emboss bytes depend on the Arial that OCCT finds on the machine | Vendor an open-licence font in the repo and point the emboss at it, so regeneration is machine-independent; WP3 (lane w2, round 2) does it | WP3 | assigned |
| Q11 | Emboss 0.8 reaches below the lid underside into the 0.4 mm module headroom (plan §5) | Fine for the gauge. WP6 records the lid-underside constraint in interface v2; WP8 makes the order 2 emboss 0.4 or moves it over the battery zone | WP6 records, WP8 builds | assigned |
| Q12 | Carried: packing shortfall (interface §12 V2-4) and requirement 5 wording (stainless versus titanium) | Packing is WP6's round 2 package; requirement 5 is Rolf's, outside the plan | WP6; **Rolf** | open |

## Round 2 (review `tasks/reviews/code-r2.md`, merged 2026-09-17)

The reviewer numbered its decisions 13 to 19; these are Q13 to Q19.

| # | Question | Reading the build follows | Closes it | Status |
|---|---|---|---|---|
| Q13 | Signal lug tab "3 × 7 × 1.5 from the cylinder toward the pad" (interface §3.1): read literally the tab runs past its own pad, through the side wall for CONTACT_2, and into other nets' margins; free area 69.4 mm² literal versus 87.0 if the tab ends under its pad | The tab ends under its own pad; its real length and direction come from the lug drawing (TE 31428 or the SKU WP5 picks), which WP5 part 2 supplies. WP6 round 3 lays out on that reading | WP5 part 2 drawing; **Rolf** confirms or keeps 7 mm | decided, provisional |
| Q14 | What plan §5's "≥ 5 mm from the battery" measures: module body 4.70 (cell packed to the hook) or 4.30 (on the rib); antenna no-copper zone 16.70 | The rule protects the antenna, so it passes; "cell packed to the hook end, foam toward the rib" becomes an interface rule | none | decided |
| Q15 | Packing escalation (plan §10 Open for Rolf item 6, reopened): VQFN-32 plus two diode arrays need 79.3 mm² against 69.4 free; no array site within 10 mm of its pads | Rolf's choice by the plan. Under Q13's reading, WP6 round 3 lays out options B (+3.5 mm length), C (+3 mm width) and E (passives on the lateral face outside the module, not in plan §5) with areas, pad and tab positions, and a recommendation; no shell change until Rolf sees that sheet | **Rolf**, after WP6 round 3 | open |
| Q16 | Plan §3.3 LEAD_PADS SIG1 s 26.5 breaks its own 0.5 mm margin (pad edge 4.00 against 4.05 required) | 26.6 per interface v2 (plan §10 gives WP6 the final pads); plan erratum; likely moot after round 3 | plan erratum, coordinator | decided |
| Q17 | Reference site against M6: at the default M6 = 15, CONTACT_REF lands about 6.5 mm in front of the mastoid bump if the body's front edge sits in the crease | Rolf's gauge wear answers it: montage §2.2 step 6 records whether the mark is on bone and the M6 offset. If not on bone, CONTACT_REF moves by the measured offset as an interface change before order 2 | gauge wear (plan §3.7 item 9), then interface v3 | open, waits on order 1 |
| Q18 | Cell pack: no published 501015 pack fits folded; the DNK in-line pack is 17 ± 1 long and its drawing is preliminary; the plan's hand fold has 0.3 to 0.5 mm for PCM and Kapton | The plan's fold on the lateral face stands as the design. One cell is bought with the Stage A parts and its folded thickness measured; the +2.4 mm pocket is WP8's fallback and moves the M1 gate, which the interface states. No cell purchase on a preliminary drawing | measurement on a real cell; **Rolf** buys it | open |
| Q19 | The PROPOSED numbers in `montage.md` §3 (5 µV RMS, 45 µV, 3:1 flex, 10:1 clench, 70 % ratio, 100 ms dropout, ±0.5 V at the INA128 output, 9 of 10, 0.20 per minute eating, 0 talking and walking, the yawn and smile counts) | Frozen as proposed. The file's own rule allows one revision from Stage A gel data before the first dry recording, with a dated row. Rolf may edit them earlier | **Rolf**, before S1 | open |

## Round 3 (review `tasks/reviews/code-r3.md`, merged 2026-09-17)

The reviewer numbered its decisions 20 to 23; these are Q20 to Q23.

| # | Question | Reading the build follows | Closes it | Status |
|---|---|---|---|---|
| Q20 | Packing: on the real TE 31428 lug with leads that can leave their barrels, only option C closes (BODY_WIDTH 17 → 20, board 19 × 15.5), with the lead pads moved to SIG1 (7.5, 29.35), SIG2 (13.5, 21.35), REF (5.5, 29.35) and one reference-over-SIG1 wire crossing on the floor where nothing sits above it | Rolf's pick from `docs/fab/packing-options.md`. Coordinator's reading: C, with the crossing (the plan does not forbid one; the alternative is a 2 mm lead bend against the plan's 3). WP8 starts on the line "I pick C". Closes Q15 | **Rolf** | open |
| Q21 | Reference lug in the tail pocket: TE 31428 upright is 1.96 thick against the plan's 1.5 envelope, reaches about y 8.2 against the lid at 8.0 when bent at the ring edge, and its wire would leave pointing at the lid | Before order 2, bend the tab toward the axis over the Kapton at a smaller radius and check it as installed geometry (plan §10 already requires that check); WP8 sizes the pocket to the real lug. Changing KEEPOUT_REF in plan §3.3 is Rolf's | **Rolf** (plan §3.3), before order 2 | open |
| Q22 | Signal lug barrel height: 1.96 mm across against the plan's 1.5 mm tab envelope; the barrel tops at y 3.46 under the board at 4.3 | Plan erratum: the flat-tab envelope height becomes 2.0 for WP8's keep-out solids; the placement already keeps parts and copper off the barrel strip, so option C does not change. Rolf may instead ask WP5 for a flatter barrel | plan erratum, coordinator; Rolf may override | decided |
| Q23 | 28 AWG wire in TE 31428's 26 to 22 AWG barrel (carried from round 1) | Fold the strip and solder the crimp, as the assembly sheet says; acceptable for a bench prototype. WP5 keeps looking for a 28 AWG barrel of similar length at purchase time | Rolf accepts, or WP5 at purchase time | open, low |

## Round 4 (review `tasks/reviews/code-r4.md`, merged 2026-09-17)

The reviewer numbered its decisions 24 to 27; these are Q24 to Q27. None
blocks the merge; all sit before WP8 proper (order 2).

| # | Question | Reading the build follows | Closes it | Status |
|---|---|---|---|---|
| Q24 | CABLE_EXIT at plan §3.3's s 36 removes 0.99 mm³ of the inferior posterior board pad (s 36.4 to 37.9) in packings A and C | Plan erratum: CABLE_EXIT_S 35.0, which clears the pad by 0.4 mm; the provisional Stage B file already uses it. Rolf may prefer a smaller exit or inset pads | plan erratum, coordinator | decided |
| Q25 | With CLOSURE_PASSED true, the lid's E1 web and tongue root sit 2.48 mm³ inside the Ø7.5 reference pocket and the body's web pocket and tongue slot break the 1.0 mm wall band around it | Order 2 without E1 (plan §3.6, interface item 6) unless the closure test passes and CONTACT_REF moves about 1 mm toward −s, which Q17 may require anyway. Decide after the gauge is worn, together with Q21 and Q17 | **Rolf**, with Q17 and Q21, after order 1 | open |
| Q26 | WP7a's contact coordinates need the placement search re-run before WP8: pads, tab angles and the reference route were searched for the plan §3.3 sites, and the shell now refuses other sites | Sequencing: WP8 proper is WP7a sites → WP6's `search_tab_degrees` on those sites (interface v3) → the shell build. Recorded in HANDOFF.md | coordinator | decided |
| Q27 | A thin Stage B body (LID_Y 6.0) cannot hold the cell: the cell plus foam tops out at 7.2 on the 1.5 floor | Order 2 builds full bodies only. If Rolf picks thin after plan §3.7 item 8, a thinner cell or a longer pocket (Q18's fallback) comes first | **Rolf**, with plan §3.7 item 8 and Q18 | open |

## Round 5 (Rolf's answer sheet, 2026-09-17)

| # | Question | Reading the build follows | Closes it | Status |
|---|---|---|---|---|
| Q28 | Rolf's answers of 2026-09-17: right ear first; renders approved; packing C; nut metal "you decide"; fold-and-solder accepted; frozen protocol accepted; requirement 5 to titanium; body thin (answered before any wear); tail mark "on bone" (answered before any wear); the tail pocket may grow (KEEPOUT_REF is free to change); E1 dropped | Recorded as his decisions. Nut: brass DIN 439 M2.5 (Bossard BN 147 class), nickel-free and stocked, the coordinator's pick under his "you decide". Thin is a requirement of plan v2. "On bone" is a preference given before any fit check and stays unverified until one exists. Requirement 5 is edited to titanium in the next docs package | Q6, Q12 (requirement 5 half), Q17 provisional, Q19, Q20, Q21, Q23, Q25, plan §10 item 3 | decided |
| Q29 | "I literally don't have the financial means to order several versions": the plan's sequence (order 1 gauge, then order 2 shell) is off; every physical thing is ordered once | Plan v2: one print order (the final shell), one board order, one hardware order. Fit comes from his measurements plus a 1:1 paper template cut from the drawing and held to the ear, not from a printed gauge. Plan §1, §3.7 and §9 S0 to S1 are superseded when plan v2 is signed off; until then nothing is ordered | plan v2 (`docs/fab/plan-v2.md`, turns under `tasks/plan-v2/turns/`) | open, drives plan v2 |
| Q30 | "I need want this to look prettier": the gauge is a functional block. Rolf, 2026-09-17 evening: "pretty is something that wouldn't look out of whack if i wore it outside" | The target is a stranger's glance: it reads as a normal hearing aid or earbud, never as a printed project. Plan v2 §7 rules serve that: continuous curvature, hidden seam, nothing outside but the three domes (and a capped port if D-5 says so), matte, dark or grey, as small as the battery allows. Colour and a reference photo still welcome on the sheet | plan v2 §7; Rolf may add colour | answered in his words |
| Q31 | "No we design it properly custom order it": the Stage A breadboard bench (plan §9 rows 7a and S1, `docs/STAGE_A_PARTS.md`) is replaced by a custom board ordered assembled | Plan v2: a board designed in the repo (KiCad, scripted, ERC and DRC run headless) and assembled once by JLCPCB; that board with gel electrodes is the bench that gives the contact sites (WP7a part 2 runs on it) before the shell prints. Bare module (Raytac MDBT50Q) versus a Seeed XIAO nRF52840 carrier is a plan v2 decision on first-spin risk. Firmware becomes a phase of its own | WP10 research; plan v2 | open |
| Q32 | The thin body cannot close with the 501015 cell (Q27) and Rolf picked thin | A thinner cell, 3.2 mm or less with its protection circuit, is a plan v2 requirement; WP10 finds the candidates. If none is stocked, plan v2 says so and the thin body carries a longer, lower pocket | WP10; plan v2 | open |
| Q33 | Budget: no number given | Plan v2 designs to the minimum order set and quotes an estimated total per order with pages; a ceiling is asked on the sheet | Rolf on the sheet | open, **Rolf** |
| Q34 | M1 and the other measurements are blank on the sheet. Rolf, evening: "i have big ears" | Nothing prints before M1. A big ear clears the chord gate (about 51; the reference ear is 52) but the number still sets body length and the hook radius (M8). Plan v2 keeps the chord gate and the measurement table; the paper template checks them | Rolf, a ruler | open, **Rolf** |
| Q35 | "this will come put together right?": Rolf expects a finished device; no vendor assembles a printed shell, a board, screws and a cell into one piece | Plan v2 rule: final assembly by Rolf with a small screwdriver only. No soldering, no glue, no crimping. The contact screws press onto board pads (spring fingers or pogo pins over the nut ends), the cell has a plug, the lid snaps, firmware loads over USB by drag and drop. This favours a Seeed XIAO carrier over a bare module | plan v2 | decided, coordinator's reading |
| Q36 | "do we actually have to get it from china?": JLC3DP and JLCPCB are in China; the plan chose them on price and speed for quantity one | No. Plan v2 quotes JLC and one non-China alternative per order (print: Craftcloud, Sculpteo, i.materialise or Xometry; assembled board: Aisler or Eurocircuits in Europe, MacroFab or Screaming Circuits in the US) with prices from pages. JLC stays the default until Rolf says "not China". His country is needed for shipping and duties and is asked | Rolf in chat | open, **Rolf** |

## Round 5b (plan v2 signed off, 2026-09-17 evening)

`docs/fab/plan-v2.md` was signed off by GPT-6 Pro at turn 10 (`tasks/plan-v2/turns/10-pro.md`, "SIGNED OFF WITH EDITS"); turn 11 applied the edits (`ef369bd`). Its decisions D-1 to D-8 and the gates become the questions below. Coordinator readings are what the build follows; rows marked **Rolf** wait for him.

| # | Question | Reading the build follows | Owner |
|---|---|---|---|
| Q37 | Which plan governs which package | Plan v2 governs WP11 to WP17 and supersedes the v1 sections it names (orders and their sequence, the contact joint, the board and bench, the states and the ledger). Every other v1 section stands, and `tasks/phase1-common.md`'s rule "the plan wins" now means plan v2 for those packages | Coordinator |
| Q38 | D-1 thickness: Rolf picked thin | Thin (4.5 cavity) is expected to fail with the board on standoffs (stack 6.0 to 7.3 over the module before clearance); the body lands between 9.0 and 9.8 outer, WP11's table says where. The build follows the table; Rolf accepts the number when he sees the renders | **Rolf** (informed by WP11) |
| Q39 | D-3 contact joint | Interface I, the board pulled onto three standoff tops by its own screws with 8 × 8 gold pads, under the §5.3 acceptance contract; an unqualified candidate until G7 (WP12 drawing and analysis, WP14 datum chain); interface II (flex under the standoffs) is the fallback; SMD spring contacts are research only (C16) | Coordinator |
| Q40 | D-4 cell and charger | DTP301120 (SparkFun PRT-25270) with a BQ25100 4.20 V variant at about 20 mA, termination and timers active, TS fixed 10 kΩ to VSS, the 0 to 45 °C window by procedure. The connector family (JST-SH per the page, JST-PH per the legacy drawing) is G1b: WP17 verifies, WP12 places SH and keeps PH as an alternate | Coordinator; G1b open |
| Q41 | D-5 R7 as rewritten | Battery-only while worn or gelled; charging on a desk from a power bank not itself plugged in or a Class II adapter; 220 kΩ per path is a per-path bound only; the supply gate is an inhibit, proved or withdrawn; residual exposure named. This is a proposal Rolf must accept in writing before S1; the answer sheet v3 will state it in plain words | **Rolf** |
| Q42 | Radio module A or B | WP11's table decides on envelope. Until then WP12's schematic is designed for the Raytac MDBT50Q-1MV2 footprint with the E73-2G4M08S1C footprint in the library and its pin mapping documented, not placed | Coordinator |
| Q43 | Standoff height and part | Default candidate 4.0 mm Harwin R25-1000402 (manufacturer drawing DRG-01991, DigiKey 952-2175-ND showed stock on 2026-09-17); alternative 3.0 mm Spacer Express LAI-FF-M2.5-SW5-L3-100 sold per 100; 3.5 mm is sourcing-open. Both are nickel-plated brass; the pressure pair is nickel on gold, to be qualified under G7 | Coordinator |
| Q44 | Board vendor and quantity; China or not (Q36) | Until Rolf answers Q36: JLCPCB standard PCBA, 4-layer 1.0 mm ENIG, the smallest assembled quantity its page allows (WP17 quotes the page), spare bare boards if the panel gives them; JLC3DP for the shell; DDP checkout figures in the ledger. WP17 lists US alternatives with catalogue prices, no quote requests | **Rolf** for the country; coordinator for the rest |
| Q45 | Firmware base | WP13 chooses between the Adafruit nRF52 Arduino core built with arduino-cli and Zephyr, both free and installable without sign-up, with the reason in its report; the Adafruit UF2 bootloader is the factory image either way; the frame contract v2 is written before code | Coordinator |
| Q46 | Tools installed on Rolf's Mac | The board lane installs KiCad 10.0.6 by Homebrew cask (about 1.5 GB) and the firmware lane installs its toolchain the same way; both free software, no accounts. Rolf can veto and the lanes record what they installed | **Rolf** (veto), coordinator otherwise |
| Q47 | Objectives order and residual risks | After the gates: height, then Rolf's burden, then cost (plan v2 §4); the §10 residual-risk list is accepted before S1 | **Rolf** |
| Q48 | First load: factory or kit | The kit (Tag-Connect TC2030-IDC-NL and the Raspberry Pi Debug Probe, $45.95 listed) unless WP17 finds JLC's programming service catalogue-priced without a quote request; completion time is recorded at the first off-body execution, not promised | Coordinator |
| Q49 | Requirement 5 | Titanium (Rolf, Q28); WP16 edits `docs/EARPIECE_DESIGN.md` requirement 5 and records the v2 decisions once each | Coordinator |
| Q50 | WP11's first table (`lane/w1` at `43a982a`): interface I (board on standoff tops) closes in 0 of 288 runs at the anatomical sites; the cell under the board collides with the SIG1 standoff and neither cell fits under a 3.0 or 3.5 standoff; interface II closes in four layouts, all Raytac + 501015 in series, width 20, standoff 3.0, LID_Y 7.0 to 9.0 | Plan v2 §5.3: when I fails, II is the fallback with its own qualification and budget. The build switches to interface II: a 2-layer flex board with FR4 stiffeners, three flex tabs with ring pads clamped under the brass standoffs (C7: JLC flex assembly acceptance and fixture fee). WP12 was redirected mid-package; interface I stays in `board-v2.md` as the rejected candidate with the reason. Note 4 (standoff 4.0, floor recess) still runs on w1 and cannot undo the floor-plan collision | Coordinator; Rolf can override |
| Q51 | The closing layouts put the USB-C on the hook-end end face, not the medial face (plan v2 §5.4 fallback), and the body is 20 wide with LID_Y 8.0 (outer 9.0, the v1 full body) once the order-1 foam allowance is kept | The end-face fallback changes only the ergonomic deterrent of R7; the disconnection procedure and G2 stand; the position goes on the residual-risk list. Thin is closed: 9.0 outer at width 20 is the smallest body that closes (Q38) | Coordinator; Q38 stays **Rolf** |
| Q52 | WP13 chose the Adafruit nRF52 Arduino core with arduino-cli over Zephyr (Q45); plan v2 §6 still names the nRF Connect SDK | Arduino is confirmed for S0 to S2: the Adafruit UF2 bootloader is the factory image either way, BLE NUS is built in, and no Nordic account is needed. The §6 wording is an erratum of the signed plan, recorded here, not edited there. A Zephyr port is not required unless S2 shows a problem the core cannot fix. V_STOP and V_START stay placeholders (2700 and 2800 mV) until WP12 computes them | Coordinator |
| Q53 | WP13 installed about 3.8 GB on Rolf's Mac: arduino-cli (25 MB), the Adafruit nRF52 core (1.3 GB under `~/Library/Arduino15`), the Arm GNU Toolchain cask (1.0 GB), an unused `arm-none-eabi-gcc` formula (540 MB) and binutils, and Rosetta 2 for the core's x86_64 tools | Q46 covered tool installs; this is larger than the brief implied. The unused `arm-none-eabi-gcc` formula can be removed with `brew uninstall arm-none-eabi-gcc`; no agent removes it. Rolf decides whether Rosetta 2 stays | **Rolf** (informational) |
| Q54 | WP17 (`lane/w5` at `f395e70`): the Raytac MDBT50Q-1MV2 is out of stock in JLCPCB's parts library (C5142646, extended/consigned) while the Ebyte E73 is stocked; WP11's only closing layouts use the Raytac (the E73 is larger and closes nowhere) | The board is designed for the Raytac. Its sourcing route is a ledger line, not a design change: JLC global sourcing if the part is quotable there without a request, else consignment (Rolf buys the modules at DigiKey or Mouser and ships them to JLC, one more parcel and JLC's consignment fee, both quoted from pages). The reviewer checks WP12 carries both routes in `board-v2.md` | Coordinator |
| Q55 | WP11's closing layouts use the 501015 cell of plan v1, whose single-unit purchase was never verified (Q18; WP10 found only inquiry-form vendors for that size); the buyable DTP301120 (22 mm long) closes in no layout at v1 length | G1 gates the cell: before S0, either a 501015-class pack with a page price, stock and a drawing in ones, or a re-run of WP11 with the body 1.5 and 3.0 mm longer (the brief's arc-plus, skipped because something closed) for the DTP in series under interface II. The next packing package (WP11b) runs the arc-plus cases regardless so the decision has numbers | Coordinator; Rolf sees the length trade in the renders |

## For Rolf

Plan §10 "Open for Rolf" items 1 to 10 stand. From round 1, in addition:

- Q6 nut metal (before S1, not before order 1).
- Q3 accept the built hook fillets when approving the renders.
- Requirement 5 wording (Q12).
- Buying the Stage A parts (`docs/STAGE_A_PARTS.md`) gates WP7a part 2 and
  order 2; add one 501015 cell to that order for Q18.
- Q13 confirm the short lug tab, or keep 7 mm and the pads move.
- Q20 pick the packing option from `docs/fab/packing-options.md` (only C closes); this closes Q15.
- Q21 the reference lug in the tail pocket, before order 2; Q25 (E1 over that pocket) and Q27 (a thin body cannot hold the cell) go with it once the gauge has been worn.
- Q23 accept fold-and-solder for the 28 AWG lead in the 26 to 22 AWG barrel.
- Q17 after wearing the gauge: is the reference mark on bone.
- Q19 accept the frozen protocol numbers, or edit them before Stage A data.
- Q33 a budget ceiling for board, shell and small parts together.
- Q34 M1 and the other measurements; nothing prints before M1.
- Q30 what "prettier" means: look, colour, a reference photo or link.
- Q36 China or not, and which country he is in.
- Q38 accept the body height WP11 measures (thin does not close with a board on standoffs).
- Q41 accept R7 as rewritten (battery-only while worn; charging on a desk).
- Q44 with Q36: China (JLC) or a US board house at a higher price.
- Q46 veto, if you want, KiCad and a firmware toolchain being installed on your Mac.
- Q47 the order of objectives after the gates, and the residual-risk list in plan v2 §10.
