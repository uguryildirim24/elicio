# Elicio fabrication plan v2 — draft, turn 03 (2026-09-17)

Status: DRAFT in spec dialogue (`tasks/plan-v2/turns/`); turn 02 (Pro)
returned fifteen findings, all answered in turn 03 and folded in here.
When signed off it supersedes the named sections of `docs/fab/plan.md`
(`0c5d0eb`); every other v1 section stands. Until sign-off nothing is
ordered, quoted or uploaded. Inputs: plan v1; `docs/fab/open-questions.md`
Q1–Q36; rounds 1 to 4 on main; `docs/fab/L5-research-v2.md` on `lane/w5`
(`832ef28`, unreviewed, two of its identifiers already corrected by turn
02: the E73 is LCSC C356849 and the XIAO charge pin is P0.13); turn 02's
live-source ledger. Rolf is the client.

## 0. What Rolf asked and what v2 does about it

| His words (2026-09-17) | v2 |
|---|---|
| "I literally don't have the financial means to order several versions" | One assembled board order, one shell order, one small-parts order. No gauge. A failed first assembly stops spending until Rolf decides; it does not start a hidden second round. §1, §9, §10 |
| "I need want this to look prettier" / "wouldn't look out of whack if i wore it outside" | The test is a stranger's glance: a normal hearing aid or earbud, never a printed project. §7 |
| "No we design it properly custom order it" | A rigid board designed in the repo, assembled by a vendor, no breadboard; the board on a desk stand with gel electrodes is the bench. §4–§6 |
| "Body thickness: thin" | Kept as a live case. The turn 01 arithmetic excluded the stacks it tried, not every layout; WP11 now tests thin, medium and full with complete envelopes and reports which close. Rolf picks from measured results. D-1 |
| "this will come put together right?" | No vendor delivers that. Final assembly is Rolf's, eight steps, one 1.5 mm hex key, no soldering, glue or crimping; every other tool he needs is listed in §8 and priced in §9. |
| "do we actually have to get it from china?" | No. JLC is a candidate, not a winner; each order carries one like-for-like US route as quote-only. His earlier documents name a Massachusetts destination; that is the planning assumption until he confirms. D-8, §9 |

## 1. Decision summary v2

1. Orders: board, then bench on the board, then shell; each once (§10).
   Nothing is bought, quoted or uploaded by an agent.
2. Body height: decided by WP11's measured layouts, not by this text.
   Width 20 unless a narrower body closes.
3. Contacts: three Grade 5 titanium ISO 7380 M2.5×4 button heads through
   a 1.5 mm medial wall (v1 §4), captive brass DIN 439 M2.5 nuts in
   printed hex pockets inside, turned from outside with the 1.5 mm hex
   key. Wires and crimp lugs are gone; the board meets the nuts by spring
   contacts (interface I) or, if I fails its gate, by clamped flex tabs
   (interface II). D-3.
4. Cell: Data Power DTP301120 protected pack (40 mAh; 3.2 × 11.5 × 22
   maximum with protection; maximum continuous charge 40 mA per its sheet
   page 4, turn 02 C3) charged by the board's own BQ25100 set to 20 mA.
   The harness revision and connector are a gate (G1b), not an assumption.
5. Radio: a module with the RF inside it, on the custom board: A Raytac
   MDBT50Q-1MV2 or B Ebyte E73-2G4M08S1C. The Seeed XIAO route (turn 01
   candidate C) is dropped: its charger is fixed at about 50 or 100 mA
   against the cell's 40 mA, and its USB port cannot sit where §2 R7
   needs it.
6. Charging: USB-C receptacle opening in the medial face, the face that
   lies against the head. A plugged device cannot be worn; that is the
   physical interlock. Firmware VBUS inhibit is secondary. D-5.
7. Acquisition contract: ADS1292 at 2000 SPS, gain 12, internal 2.42 V
   reference, one differential channel, bias on the reference contact,
   220 kΩ series protection on every contact path. The frozen protocol's
   criteria are restated input-referred for this chain (§6). D-6.
8. First firmware load: the factory programs a UF2 bootloader over SWD
   if the assembler accepts the job (quote-only gate G4); else Rolf does
   it once with the two tools named in §8. Elicio firmware then loads by
   drag and drop over USB, lid on, device off the ear.
9. Look: §7; new dimensioned closure and hook; matte; colour per Rolf.
10. Budget: §9 gives dated planning allowances per order, not a delivered
    total; a checkout-page gate closes each before Rolf pays.

## 2. Requirements v2 (each testable)

- R1 One order per physical thing. A second board or shell is not a step
  of this plan; if first-assembly validation fails, routine use is
  withheld and no further spend happens without Rolf's decision.
- R2 Final mechanical assembly by Rolf: at most eight steps, one 1.5 mm
  hex key, no soldering, glue, crimping or wire stripping (§8).
- R2b Every other thing Rolf must do or own, before or after assembly,
  is listed with its tool and price: measuring, template, first firmware
  load if the factory does not, bench leads, USB cable. Nothing hides.
- R3 Skin-side materials: titanium domes and the printed shell material
  with the finish actually ordered. Before the shell order, the ordered
  process has a live vendor statement of skin-contact testing for that
  process and finish, or Rolf accepts in writing the material claim that
  exists instead (turn 02 C1, C8). Every other material in the device is
  named with where it sits and what covers it (§5 materials table).
- R4 Body height and width are what WP11's measured layouts close, at
  the smallest height that passes; Rolf's thin preference is the first
  objective after the gates (§4).
- R5 Look rules of §7 pass as script checks where checkable; Rolf
  approves two renders before the shell order.
- R6 First-pass success is the objective, not a promised result. The
  order gates (§10 S0) are non-skipped, versioned checks: ERC and DRC in
  a release job that installs the pinned tools and fails closed;
  geometry checks on the built solid; the acquisition contract; the
  joint drawing; the delivered price. The residual first-assembly risks
  are written down (§10) and accepted by Rolf before he pays.
- R7 Worn acquisition and bench acquisition run on the battery with no
  cable connected. The port's position makes a worn, plugged
  configuration physically impossible (§5.4). Every contact path,
  including the bias path, carries its own ≥ 220 kΩ series protection
  before any exposed conductor (v1 §6). Off-body electrical checks come
  before the first skin connection.
- R8 The sum of the three orders at checkout-page prices, delivered to
  Rolf's address, stays under his ceiling (Q33).

## 3. Packaging inputs (corrected) and what WP11 tests

Facts on file, corrected per turn 02 finding 5: v1 full body outer 9.0,
floor 1.5, lid at 8.0, cavity 6.5; an 8.5 body has a 6.0 cavity; thin
(lid 6.0) has 4.5. Side walls 1.5, so cavity width is BODY_WIDTH − 3.0
(17.0 at 20). Contact stack inside the wall: screw projects 2.5 beyond
the wall (4.0 under head − 1.5); nut m = 1.6 sits on the wall, tip 0.9
proud of the nut. Modules: Raytac 10.5 × 15.5, reserve 2.3 high (v1 §5);
E73 13 × 18 × 2.0 (its antenna keep-out is a gate, G3c). Cell: DTP301120
protected 22.0 × 11.5 × 3.2 plus its connector and 100 ± 3 mm leads,
which WP11 reserves as a routed volume. Board: rigid 1.0 mm, 4 layers.
Spring contact (interface I) compressed height 1.5 (gate G7 names the
part). USB-C receptacle 8.9 × 7.3 × 3.2 plus the opening in the medial
wall and a plug clearance volume outside it, which only exists off the
ear.

Turn 01's sums showed that its four stacks exceed 4.5; they did not show
that every layout does. WP11 now lays out A and B with interfaces I and
II, series and stacked, at lid heights 6.0, 6.5, 7.0, 8.0, 8.5 and 9.0
and widths 18 to 20, with the complete envelopes above, and measures on
the built solid. Only a passing layout supports a thickness; a thin
result that fails is reported with its first conflict, and Rolf then
chooses between thicker, longer, wider, or stopping.

## 4. Architecture: gates first, then objectives

Candidates: A (Raytac, consigned from DigiKey because LCSC shows none)
and B (E73, in JLC's library as extended, standard-only, X-ray). Each on
a rigid 4-layer board, one-sided assembly, with interface I or II.

Gates, each pass/fail with evidence, none waived:

- G1 Cell and charger: charger worst-case current including tolerance
  ≤ the pack's maximum continuous charge current; termination, cut-off
  and temperature per the pack sheet. G1b: one exact pack revision with
  its drawing, connector part number, polarity and lead length, and a
  shipping route to Rolf's address.
- G2 Electrical boundary: R7 as designed, shown on a connection and state
  diagram (powered, off, reset, fault, plugged); the port position
  proven on the built solid; the bench stand keeps the board off the
  body's cable.
- G3 Assembler acceptance: every part in the assembler's library with
  stock on the order day, or a consignment plan counted as a Rolf
  shipment; the board tier accepted (standard, one-sided, X-ray where
  required); G3c the module's antenna keep-out from its own document.
- G4 First load: the assembler accepts programming the UF2 bootloader
  over SWD at a stated price (quote-only), or Rolf's two tools are in
  order 3 and the step is in R2b.
- G5 Geometry: closes on the built solid; the contact-site workspace of
  §5.3 demonstrated.
- G6 Acquisition contract of §6 covers 20–490 Hz and every protocol
  criterion has its input-referred equivalent.
- G7 Contact joint drawing with its tightening limit, support, insulation
  and continuity test (§5.3).
- G8 Delivered price of the three orders under Rolf's ceiling at the
  checkout gate.

Among survivors, objectives in order, proposed for Rolf's approval:
(1) smallest body height, (2) fewest Rolf tools and steps, (3) lowest
delivered price. If no candidate survives, the plan reports "no eligible
architecture" and stops; there is no fallback pick.

## 5. The board (WP12)

5.1 Repository and rules. `hardware/board/`, a KiCad project committed
as files. ERC and DRC run with `kicad-cli` against the assembler's
published capability rules. Developer runs may skip when the tool is
absent; the release job installs the pinned KiCad and fails closed.

5.2 Construction. Rigid FR4, 4 layers, 1.0 mm, ENIG. One-sided assembly.
Two M2.5 mounting holes onto printed bosses, fastened with the same
ISO 7380 M2.5 screws and the same hex key (self-forming into PA12 pilot
holes; the boss design is WP14's, the pull-out test is S4's).

5.3 Contact interface I (default): three SMD spring contacts on the
board's underside, each landing on the top face of a brass nut. The nut
face is Ø5.0 across flats; a site may move ± 2.0 mm from nominal before
the contact leaves the nut, so the bench (S2) may choose sites inside
that workspace without a new board. A site outside it is a stop, not a
shell-only change. The joint drawing (G7) gives: nut pocket hex size and
depth with the nut captive against rotation, pad annulus, spring part
number with free and compressed heights and force, board height over the
floor set by the bosses, the screw tip clearance under the board, the
tightening limit for the hex key ("stop when the head seats; no further
turn"), and the continuity check after assembly (LED self-test in
firmware plus a 1 kΩ-scale resistance check on the bench boards). Path:
skin → titanium dome → screw thread → brass nut → gold-plated spring →
board. Interface II (fallback if G7 fails for I): a flex with FR4
stiffeners and three ring pads clamped under the nuts, with the same
drawing content plus bend radius, strain relief and the assembler's flex
acceptance and fixture price.

5.4 Charging port. USB-C 16-pin receptacle with 5.1 kΩ CC pull-downs,
mounted so its opening is in the medial face near the hook end. With the
device on the ear the medial face lies against the head; a plug cannot be
inserted or remain inserted. Off the ear the device lies medial side up
on a desk to charge. A silicone plug covers the opening when worn (skin
side material: silicone; the receptacle shell never touches skin). If
WP11 cannot place the opening on the medial face for a candidate, that
candidate fails G2.

5.5 Front end and power. ADS1292 (non-R) with AVDD = DVDD = 3.0 V from
a TLV713 3.0 V LDO on the battery (AVDD minimum 2.7 V per the datasheet;
the pack's protection cuts off below that); internal 2.42 V reference;
SIG1 and SIG2 to one channel at gain 12, 2000 SPS; the reference contact
to the RLD output through its own 220 kΩ; SIG1 and SIG2 each through
220 kΩ before the input filter (v1 §6); lead-off detection off in the
worn state. BQ25100 charger with ISET for 20 mA, TS disabled or a fixed
resistor per its datasheet, VBUS only from the receptacle. The module's
own regulator is not used for the front end. WP12 documents every rail
and path, the states of G2, input offset headroom, and the off-body
acceptance tests (rail voltages, charge current with a meter in series
on the bench, RLD stability, leakage through each contact path with the
device powered and with VBUS present and no one wearing it).

5.6 Bench connection. A 3-pin 2.54 mm right-angle header (SIG1, SIG2,
REF) at the board edge, behind 220 kΩ, for pre-made snap-electrode leads
with pin sockets (order 3). No stripping, no clips onto bare copper.

5.7 Materials table (R3): titanium screw (skin, Grade 5, uncoated; the
ISO 7380 head geometry and a lot certificate are G3 evidence, Sortafast's
page states grade only); PA12 shell (skin); silicone port plug (skin);
brass nut (inside, under the spring); ENIG pads and gold-plated spring
contacts (inside; nickel under the gold, covered); E73 or Raytac module
shield (inside, tin-plated steel); receptacle shell (inside the wall
opening, behind the plug); cell pouch and PCM (inside, in the pocket, on
a 0.3 foam pad). The cavity is not sealed; it is closed by the lid and
the plug, and nothing inside it is meant to touch skin.

## 6. Acquisition, firmware and the protocol mapping (WP13)

Firmware: nRF Connect SDK. ADS1292 over SPI at 2000 SPS, 24-bit signed
samples; BLE Nordic UART Service carrying frames of 20 samples with a
sequence number, so loss is visible; scale published as V per LSB from
gain and reference; battery voltage every 10 s; LED for state; VBUS
present → front end held in power-down and streaming refused (secondary
to R7). The laptop pipeline receives raw frames; decoding stays there.

First load: a UF2 bootloader image built for this board, programmed once
over SWD (factory or Rolf per G4); the device then appears as a drive
over USB, off the ear, and takes Elicio firmware by file copy. Recovery
is the same drive via the reset pin brought to a pad under the lid.

Protocol mapping: `docs/fab/montage.md` §3 was written for an INA128
chain. Its numbers stay as accepted (Q28); WP13 publishes a versioned
"protocol v2 for the ADS1292 chain" table before any dry data, mapping
each criterion to this chain: noise 20–490 Hz measured on the 2000 SPS
stream after a digital band-pass (the ADS1292 −3 dB point at 2000 SPS is
about 524 Hz); amplitudes input-referred in µV; the INA128 output-shift
criterion restated as an input-referred DC shift using the INA128 gain
that file states; dropout as frames lost or samples at rail. This is the
one revision the file's own rule allows, dated, before the first dry
recording. The bench montage procedure (§2 of that file) is re-targeted
to the board on its stand with the §5.6 leads.

## 7. Look (WP14)

- The test: a stranger sees a hearing aid or an earbud. No visible
  screws, no visible seam wider than 0.3 mm, no text outside, no
  printed-layer look (media-blasted matte; vapour smoothing only from a
  vendor whose page states skin-contact testing of the smoothed part).
- Surfaces: one continuously curved lateral shell; no planar facet over
  3 mm; outside edges R ≥ 1.0 except the medial skin face (flat, R0.5).
- Closure: a new dimensioned closure, designed by WP14, replacing v1's
  experimental tongue, web and lip (E1 dropped, Q28): either a cantilever
  snap with stated beam dimensions, strain, insertion and retention
  forces, or one concealed screw at the tail end plus a hinge lip; the
  drawing and a first-assembly retention check (lid holds a 20 N pull by
  hand; nothing rattles) are S0 and S4 items. Nothing is inherited from
  the gauge.
- Hook: elliptical section with stated major and minor axes at root and
  tip, blended with a stated fillet; the radius from M8.
- Tail: blended; reference dome per Q17 (his "on bone" stands
  provisionally, checked on the paper template and at S2).
- Colour: grey or dyed black per Rolf (Q30); his photo or link, if any,
  is the reference.
- Approval: two renders and one drawing page; his yes before the shell
  order.

## 8. Rolf's part, all of it (R2, R2b)

Before ordering: M1 to M8 with a ruler and calipers per
`docs/fab/measure.md`; print `template.pdf` at 100 %, check its 50 mm
bar, cut, hold behind the ear, report fit; approve renders; approve the
architecture objectives order and the residual-risk list; pay three
checkouts against their gates.

Final assembly, eight steps, one 1.5 mm hex key:

1. Peel the pre-cut foam pad and lay the cell in its pocket; route its
   lead in the channel to the connector.
2. Push the three titanium screws through the dome holes from outside.
3. Drop a brass nut into each hex pocket inside; turn each screw with the
   hex key until the head seats. Stop.
4. Set the board on its two bosses, spring contacts over the nuts.
5. Turn the two board screws with the hex key until they seat.
6. Plug the cell connector in (polarity marked on the board; the plug
   only fits one way).
7. Snap or screw the lid per WP14's closure.
8. Lay the device medial side up, plug USB-C in, watch the LED.

Firmware: copy the UF2 file to the drive that appears. If G4's factory
programming is refused: once, before step 4, press the Tag-Connect
TC2030-NL pogo cable onto the board's footprint with a Raspberry Pi
Debug Probe attached and run one command from `docs/fab/assemble.md`
(about 30 s); both tools are in order 3 under that condition.

Bench (S2): board on its stand, cell plugged, three snap leads to gel
electrodes per `montage.md` §2, no cable, laptop receiving.

## 9. Orders and planning allowances (not quotes; checkout gates close them)

Destination: Massachusetts, USA, as a planning assumption (turn 02)
until Rolf confirms; duties on China-origin goods apply and are part of
the checkout number.

| Order | Contents | Route (default / US quote-only) | Published components on 2026-09-17 | Planning allowance |
|---|---|---|---|---|
| 1 Board | 2 to 5 assembled boards, standard one-sided PCBA, 4-layer ENIG, X-ray if the module needs it, bootloader programming if accepted | JLCPCB / MacroFab or Screaming Circuits | setup $25.56, stencil $8.21, feeder $1.53 each, extended parts $3.07 each (JLC schedule); boards, parts, X-ray, programming, freight, duties unpriced | $150–220 |
| 2 Shell | body, lid, spare lid; MJF PA12; grey or black; finish per R3 | JLC3DP / Xometry | JLC "from $1.00, 72 h" is a starting price only | $50–90 |
| 3 Small parts | 10 titanium screws (Sortafast $17.50), 10 brass nuts (TME, UNVERIFIED $1.60), cell (SparkFun $7.39), 1.5 mm hex key, USB-C cable, pre-cut foam pads, silicone port plugs, three snap-electrode leads with pin sockets, gel electrodes, a nickel test kit or Rolf's written waiver (the named kit shows unavailable), and if G4 falls to Rolf: TC2030-NL cable and a Raspberry Pi Debug Probe | US sellers | screws and cell page-priced; the rest allowances | $80–130, plus about $60 with the programming tools |

Sum of allowances: $280–440 before duties on order 1 and 2 if they come
from China, and before the programming tools. Not a verified delivered
total; R8 is judged at the three checkout gates with the real numbers,
and Rolf sees them before paying. Named cuts if R8 fails: grey instead
of dyed, no spare lid, two boards instead of five.

## 10. Release states v2 and residual risk

| State | Entry requires |
|---|---|
| S0 files approved | WP11 winner with all gates G1–G7 passed and evidenced; WP12 ERC/DRC clean in the release job and reviewed against the ADS1292, BQ25100 and module reference designs; WP14 checks on the built solid; renders approved; paper template and chord gate pass on M1; residual-risk list accepted by Rolf |
| S1 board and parts ordered | S0; checkout gate G8 shown to Rolf; he pays orders 1 and 3 |
| S2 bench | boards arrive; factory or Rolf first load; off-body checks of §5.5; firmware streams; gel montage on the stand gives three sites inside the §5.3 workspace; protocol v2 table published before this data |
| S3 shell ordered | S2 sites into interface v3; WP14 re-run; renders re-approved if the shape changed; checkout gate; Rolf pays order 2 |
| S4 assembled | §8 done; retention check; continuity self-test; DMG nickel screen on the domes if a kit exists, else the waiver |
| S5 validation wear | protocol v2 as v1's S3, ≤ 4 h/day |
| S6 routine use | all criteria pass |

Residual risks accepted before S1, in writing: analog noise and antenna
performance on the head are first measured at S2 and S5; comfort and
skin pressure are first felt at S4; a failed S5 leaves a bench device and
no further spend without Rolf's decision (R1).

## 11. Work packages v2

| WP | Owns | Output | Acceptance |
|---|---|---|---|
| 11 Packing v2 | `placement.py`, Stage B of `bte_fit_shell.py`, `docs/fab/packing-v2.md` | A and B, interfaces I and II, series and stacked, lids 6.0–9.0, widths 18–20, complete envelopes incl. harness, receptacle opening on the medial face, workspace ± 2 mm; the §4 gates that geometry can answer | measured on the built solid; the table says which close and why the rest fail |
| 12 Board | `hardware/board/`, `docs/fab/board.md` | KiCad project, ERC/DRC, BOM with assembler codes, STEP, joint drawing, G2 diagram | traced values; release job passes; reviewed against reference designs |
| 13 Firmware | `firmware/`, protocol v2 table in `montage.md` | bootloader image, streaming firmware, receiver | builds in CI; bench-tested at S2 |
| 14 Shell v2 | `scripts/cad/`, `docs/fab/cad/v2/` | body, lid, closure and hook drawings, renders, manifest | §7 checks; Stage B checks on the built solid; identical regeneration |
| 15 Rolf's sheets v2 | `measure.md`, `template.pdf`, `order-board.md`, `order-shell.md`, `order-parts.md`, `assemble.md` | sheets with pictures, three checkout gates, the §8 steps | no step needs a question |
| 16 Record | `docs/EARPIECE_DESIGN.md`, requirement 5 | v2 decisions once each; requirement 5 to titanium | each decision appears once |

## 12. Claims still open (turn 02 ledger)

C1 a certificate or test report tying JLC's ordered process and finish to
skin contact, or Rolf's waiver (R3); C5 E73 stock count, price and
antenna keep-out from Ebyte's manual; C6 the assembler's price and
acceptance for nRF52840 SWD programming (quote-only, Rolf-authorized);
C7 only if interface II is needed; C9 the screw's ISO 7380 conformity and
a nut page; C10 non-R ADS1292 stock at an accepted source on the order
day; new C11 the spring contact part (height, force, plating, stock);
C12 the DTP301120 SH-harness drawing (SparkFun's page and the PH drawing
disagree); C13 duties on China-origin PCBA and prints delivered to
Massachusetts.

## 13. Decisions for the dialogue, then Rolf

- D-1 Thickness: Rolf's thin stays a live case until WP11's table; he
  picks from measured results.
- D-2 Gates G1–G8 then objectives (height, Rolf's burden, price).
- D-3 Interface I (spring contacts on nut tops, ± 2 mm workspace) with II
  as the fallback.
- D-4 Cell DTP301120 with the board's BQ25100 at 20 mA; XIAO dropped.
- D-5 Port in the medial face as the physical interlock; VBUS inhibit
  secondary; bench battery-only.
- D-6 Streaming firmware with the §6 data contract; UF2 bootloader as the
  factory image; protocol v2 mapping before dry data.
- D-7 Board and parts first, bench, then shell; sites only inside the
  workspace; no simultaneous shell order.
- D-8 JLC as candidate with US quote-only routes; Massachusetts assumed.

Open for Rolf: M1–M8, the ceiling (Q33), colour (Q30), country and
China-or-not (Q36), the objectives order of §4, and the residual-risk
list of §10.
