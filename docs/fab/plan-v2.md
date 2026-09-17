# Elicio fabrication plan v2 — draft, turn 09 (2026-09-17)

Status: DRAFT in spec dialogue (`tasks/plan-v2/turns/`). Turn 02 (Pro)
returned findings 1–15, turn 04 findings 16–22, turn 06 findings 23–25
with conditions on the rest; turn 07 answered them (the plan rewrite
landed at `2fbad34`, one commit after the turn file at `dba5552`); turn
08 returned findings 26 (the rewrite was missing at `dba5552`) and 27
(an acceptance contract for the direct-contact joint) and a C14 result;
turn 09 folds them in, Pro's replacement paragraphs verbatim. When
signed off
it supersedes the named sections of `docs/fab/plan.md` (`0c5d0eb`); every
other v1 section stands. Until sign-off nothing is ordered, quoted or
uploaded. Inputs: plan v1; `docs/fab/open-questions.md` Q1–Q36; rounds 1
to 4 on main; `docs/fab/L5-research-v2.md` on `lane/w5` (`832ef28`,
unreviewed; turn 02 corrected two identifiers: E73 is LCSC C356849, the
XIAO charge pin is P0.13); the live-source ledgers of turns 02 and 04.
Rolf is the client.

## 0. What Rolf asked and what v2 does about it

| His words (2026-09-17) | v2 |
|---|---|
| "I literally don't have the financial means to order several versions" | One assembled-board order, one shell order, one small-parts order. No gauge. Before the first payment he sees the whole-project delivered budget, with a reserved maximum for the shell. A failed first assembly stops spending until he decides. §1, §9, §10 |
| "I need want this to look prettier" / "wouldn't look out of whack if i wore it outside" | The test is a stranger's glance: a normal hearing aid or earbud, never a printed project. §7 |
| "No we design it properly custom order it" | A rigid board designed in the repo, assembled by a vendor, no breadboard; the board on a desk stand with gel electrodes is the bench. §4–§6 |
| "Body thickness: thin" | A live case. WP11 lays out thin, medium and full with complete envelopes and reports which close; Rolf picks from measured results. D-1 |
| "this will come put together right?" | No accepted, priced turnkey delivery route has been established for this build. Final assembly is Rolf's: eight steps, one 1.5 mm hex key; every other thing he must do or own is listed in §8 and priced in §9. |
| "do we actually have to get it from china?" | No. JLC is a candidate, not a winner; each order carries one US route as quote-only. Delivery: Massachusetts, USA (`docs/fab/order1.md`), assumed until he confirms. D-8, §9 |

## 1. Decision summary v2

1. Orders: board and small parts, then bench on the board, then shell;
   each once (§10). No agent buys, quotes or uploads.
2. Body height: whatever WP11's measured layouts close, smallest first.
   Width 20 unless narrower closes.
3. Contacts: three Grade 5 titanium ISO 7380 M2.5×4 button heads through
   the 1.5 mm medial wall (v1 §4). Inside, each screw threads into a
   brass female hex standoff (M2.5, 5 mm across flats, 3.0 mm long) that
   sits captive in a printed hex pocket; the standoff is the nut and the
   landing. The board is pulled down onto the three standoff tops by its
   own mounting screws and meets each top with a large gold pad
   (interface I, §5.3, an unqualified direct-contact candidate until G7
   passes; the board itself supplies the compliance); flex tabs are the
   fallback (interface II). No discrete spring contacts, no wires, no
   lugs, no solder by Rolf. D-3.
4. Cell: Data Power DTP301120 protected pack (40 mAh; 3.2 × 11.5 × 22
   maximum with protection; maximum continuous charge 40 mA; charge
   0–45 °C; over-discharge protection at 2.4 V, all from its sheet). The
   exact harness revision is gate G1b. Charger: BQ25100-class on the
   board at a 20 mA setpoint with termination and timers active (§5.5).
5. Radio: a module with the RF inside it: A Raytac MDBT50Q-1MV2 or B
   Ebyte E73-2G4M08S1C. The XIAO is out (turn 02 findings 1 and 2).
6. Charging and the electrode boundary: R7 as rewritten below. This
   proposed circuit has no galvanic isolation between USB-connected
   circuitry and its electrode paths; v2 says so, states what the 220 kΩ
   does and does not bound, and asks Rolf to accept a procedural rule.
   D-5.
7. Acquisition contract: ADS1292 at 2000 SPS, gain 12, internal 2.42 V
   reference, one differential channel, bias on the reference contact,
   220 kΩ on every contact path; protocol v2 table before dry data. D-6.
8. First firmware load: an Adafruit-style UF2 bootloader with SoftDevice
   as the factory image (or Rolf's exact kit, G4); application firmware
   by file copy over USB, off the ear. D-6.
9. Look: §7; new dimensioned closure and hook; matte; colour per Rolf.
10. Budget: §9 planning allowances per order plus a duties-and-tax
    ledger and a whole-project gate before the first payment.

## 2. Requirements v2 (each testable)

- R1 One order per physical thing. A second board or shell is not a
  step; if first-assembly validation fails, routine use is withheld and
  no further spend happens without Rolf's decision.
- R2 Final mechanical assembly by Rolf: at most eight steps, one 1.5 mm
  hex key, no soldering, glue, crimping or wire stripping (§8).
- R2b Everything else Rolf does or owns, with tool and price: measuring,
  template, the first firmware load if the factory does not do it,
  entering recovery, bench leads and stand, USB cable, charging source.
- R3 Skin-side materials: titanium domes, the printed shell in the finish
  actually ordered, and the silicone port plug. Before the shell order,
  the ordered process has a live vendor statement of skin-contact
  testing for that process and finish, or Rolf's written acceptance,
  which records the limits of the evidence: it is not a test
  certificate, does not establish nickel-free plating, and does not
  waive the electrical boundary. Every other material is in §5.7 with
  where it sits and what covers it.
- R4 Body height and width are what WP11 closes, smallest first; Rolf's
  thin preference is the first objective after the gates.
- R5 Look rules of §7 pass as script checks where checkable; Rolf
  approves two renders before the shell order.
- R6 First-pass success is the objective, not a promised result. Order
  gates are non-skipped, versioned checks in a release job that installs
  pinned tools and fails closed; the residual first-assembly risks are
  written (§10) and accepted by Rolf before he pays.
- R7 Electrode boundary and charging, a proposed change to v1's rule for
  Rolf's acceptance. This proposed circuit has no galvanic isolation
  between USB-connected circuitry and its electrode paths. All
  skin-connected use, including the gel bench, is battery-only with
  external power, data and debug connections disconnected. The 220 kΩ
  protection on every electrode path, including the bias path, provides a
  per-path bound only for the specified intact circuit and maximum
  applied voltage; 23 µA is the 5 V calculation for one intact path, not
  a total patient-current, adapter-leakage or single-fault safety claim.
  G2 records the other return paths (electrode to electrode, electrode
  to earth-referenced source, receptacle shell, a failed resistor) and
  the foreseeable connection errors. The USB-C opening in the medial face
  is an ergonomic exclusion that makes worn charging impractical, not a
  proven impossibility. Charging only from a battery power bank that is
  not itself plugged in, or a listed Class II 5 V adapter, with the
  device lying medial side up on a desk, per Rolf's sheet. The VBUS
  hardware gate on the front end's supply is a separately verified
  functional inhibit, not isolation; WP12 proves it in the complete
  circuit, including digital I/O, all AFE supplies and possible
  back-power paths, or removes the claimed power-removal credit; no
  powered-off pin may be driven outside its allowed conditions. Residual
  USB- or earth-referenced exposure can arise without simultaneous
  failure of every rule and remains the reason to prohibit skin
  connection while charging or debugging. Gel-bench procedure: remove
  all three skin leads before attaching USB, the debug probe or any test
  equipment, and unplug those before attaching electrodes; every
  gel-header path is protected by its own 220 kΩ, checked on the board,
  not assumed from a drawing; the folded-card stand serves S2 (a printed
  stand cannot, it is not ordered yet). Every leakage or fault check in
  this plan is an off-body test.
- R8 The whole-project delivered budget (three orders, programming,
  every shipment, import collection, Massachusetts use tax) stays under
  Rolf's ceiling (Q33), shown before the first payment with a reserved
  maximum for the shell and updated at every later checkout.

## 3. Packaging inputs (corrected) and what WP11 tests

v1 full body outer 9.0, floor 1.5, lid at 8.0, cavity 6.5; an 8.5 body
has 6.0; thin (lid 6.0) has 4.5. Side walls 1.5, cavity width
BODY_WIDTH − 3.0. Contact stack inside the wall: the screw projects 2.5
beyond the wall; the standoff is 3.0 long, so the screw tip sits 0.5
below the standoff's top face, which is a flat brass face 5 mm across
flats with a Ø2.5 threaded hole; the landing height is 3.0 above the
floor (3.0, 3.5 and 4.0 are run; the standoff SKU per height is C14: turn
08 verified a 3.0 catalogue part, Spacer Express LAI-FF-M2.5-SW5-L3-100,
leaded nickel-plated brass, sold per 100, and a 4.0 part, Harwin
R25-1000402, nickel plated, neither with a verified on-hand count or a
landing drawing; no 3.5 part was found). Interface I has no discrete
spring contacts: the board's underside pad rests on the standoff top, so
the board underside is at the standoff height across the whole board
(rigid, before deformation), and the cell may lie under the board only
where no standoff or boss stands and where the cell top plus foam sits
below the board's deformed underside with positive clearance: cell 3.2 +
foam 0.3 = 3.5 leaves −0.5 under a 3.0 standoff and 0.0 under 3.5, so the
cell-under-board arrangement needs the 4.0 standoff or a 0.5 recess in
the floor under the cell (floor web ≥ 1.0 there; JLC's minimum wall is
C15), and the cell must carry no load. The module sits on the board's
top; nothing taller than the module anywhere. The prior review did not
authenticate a pin meeting the complete low-height specification
(Mill-Max 0900 works at 3.80, 0919 at 8.13); this plan elects not to use
pins.
Modules: Raytac 10.5 × 15.5, reserve 2.3; E73 13 × 18 × 2.0 (antenna
keep-out is gate G3c). Cell: 22.0 × 11.5 × 3.2 plus its connector and
100 ± 3 mm leads reserved as a routed volume; foam 0.3. Board: rigid
1.0, 4 layers. USB-C receptacle 8.9 × 7.3 × 3.2 with its medial opening
and plug volume (§5.4). Bench header 7.6 × 2.5 × 2.5. Recovery button
1.6 tall.

Turn 01's sums excluded the stacks they tried, not every layout. WP11
lays out A and B with interfaces I and II, series and stacked, at lid
heights 6.0, 6.5, 7.0, 8.0, 8.5 and 9.0 and widths 18 to 20, with the
complete envelopes above, and measures on the built solid. Only a
passing layout supports a thickness. Expectation, not result: with the
board on 3.0–4.0 standoffs, a 1.0 board and a 2.0–2.3 module, the stack
over the module is 6.0–7.3 before clearance, deformation and lid
variation (outer 8.5–9.8 with the 1.5 floor and 1.0 lid, zero added
clearance), so thin (4.5) is expected to fail and full (6.5) is marginal;
the table says which, from the deformed maximum board envelope and a
positively cleared, unloaded cell envelope, with verified envelopes
only.

## 4. Architecture: gates first, then objectives

Candidates: A (Raytac, consigned from DigiKey; LCSC shows none) and B
(E73, JLC library C356849, extended, standard-only, X-ray). Each on a
rigid 4-layer board with interface I or II. Assembly sides follow the
released placement and are priced accordingly (interface I's pins are
on the underside, so two-sided is the working assumption).

Gates, each pass/fail with evidence, none waived:

- G1 Cell and charger: charger worst-case current including ISET
  tolerance ≤ the pack's 40 mA; termination and safety timers active
  (TS is never floated; the pack has no thermistor, so TS gets the fixed
  network its datasheet defines and the charging temperature window
  0–45 °C is enforced by Rolf's sheet, recorded as such); the
  termination profile recorded with its acceptance for the exact pack
  (this charger's floor is 1 mA against the sheet's 0.4 mA end-of-charge);
  any change in delivered capacity or runtime is unknown until
  characterised, no numerical capacity-loss claim is inferred from the
  termination current alone; the temperature limit is an operating
  restriction, not automatic cell-temperature protection; the exact
  ordering code (4.20 V variant) and the ISET, PRETERM and TS networks
  named; the LED's meaning stated from the circuit's actual pins. G1b: one exact pack revision with its drawing,
  connector part number, pin numbering, polarity, lead length and a
  shipping route to Massachusetts; SparkFun's page says JST-SH and the
  linked drawing says JST-PHR, so no footprint is frozen until one
  document settles it.
- G2 Electrode boundary: R7 shown on a connection and state diagram
  (powered, off, reset, an uncooperative MCU, fault, VBUS present, bench),
  all three paths and the other return paths R7 names, the switched
  rails with switch orientation and body diode, VBUS detection, default
  gate state, SPI and control-pin states, pull-ups, protection paths,
  rail discharge and start-up, and the off-body checks of §5.5.
- G3 Assembler acceptance: every part in the assembler's library with
  stock on the order day or a consignment plan counted as a Rolf
  shipment; tier, sides, X-ray and any handling panel accepted; G3c the
  module's antenna keep-out from its own document; G3d the screw's
  ISO 7380 head geometry and material record, and a nut/standoff page.
- G4 First load: an accepted factory SWD programming-and-verification job
  at a stated price (quote-only, Rolf-authorized), or the exact kit of
  §8 with the numbered net map in `docs/fab/assemble.md`, ground-first
  connection, and both directions of the probe/target I/O limits
  verified at the actual powered target voltage (if the selected rails do
  not meet the limits, the programming voltage arrangement changes or a
  qualified interface is added; compatibility is never inferred from
  nominal voltages); plus the board-specific merged bootloader image,
  application and linker layout, USB identity and the update and
  recovery tests from WP13.
- G5 Geometry: closes on the built solid with verified part envelopes
  (no provisional boxes); the per-site adjustment region of §5.3 computed
  from the actual pad and landing geometry with tolerances and stated as
  a number per site; no region is granted by argument.
- G6 Acquisition contract of §6 with the protocol v2 table.
- G7 Contact joint drawing: standoff SKU with thread depth, finish and
  landing face; hex pocket; pad geometry and plating; the datum chain
  from the printed floor through the standoff to the board and the
  bosses with tolerances, both heights from one datum with the actual
  supported relative tolerance; the nominal boss offset, screw
  coordinates and tightening sequence; acceptable retained contact at
  all three sites across the permitted site region, the assembly
  sequence and the tolerance cases (low contact with high boss, high
  contact with low boss), with a contact allowed to open in the analysis
  rather than assigned a tensile reaction; bounded strain on the
  populated board and its components, board-fastener and boss loads and
  the pull-out margin in PA12; positive clearance from the cell and
  unrelated conductors; retained preload after the specified mechanical
  checks; insulation envelope around each contact net; and the off-body
  contact-stability test of §5.3 with a declared low-level electrical
  acceptance. Interface I is an unqualified candidate until this passes.
  Before G3d/G7 passes, each standoff length actually used has an exact
  supplier SKU, current availability and purchase quantity, a
  dimensional/landing drawing, thread-depth and tolerance information,
  actual base material and finish, and a supported delivered cost; a
  near-match or generic brass family is not accepted as the selected
  part, and no part is machined or shortened in Rolf's steps.
- G8 Whole-project delivered budget under Rolf's ceiling (R8).

Among survivors, objectives in order, proposed for Rolf's approval:
(1) smallest body height, (2) fewest Rolf tools and steps, (3) lowest
delivered cost. If none survives, the plan reports "no eligible
architecture" and stops.

## 5. The board (WP12)

5.1 Repository and rules. `hardware/board/`, a KiCad project committed
as files. ERC and DRC against the assembler's published rules; developer
runs may skip when the tool is absent; the release job installs pinned
KiCad and fails closed.

5.2 Construction. Rigid FR4, 4 layers, 1.0 mm, ENIG. Sides per
placement. Two (or four, if G7's load asks) M2.5 mounting holes onto
printed bosses, fastened with ISO 7380 M2.5 screws and the same hex key
into printed pilot holes; the boss and pilot design is WP14's, the
pull-out margin is G7's, the check is S4's.

5.3 Contact interface I (default candidate). Contract, before the
mechanism: interface I is an unqualified direct-contact candidate. The
released drawing names the standoff and actual top-face finish, exposed
PCB pad geometry, separate board-fastener positions, nominal boss offset
and its full tolerance chain. G7 demonstrates acceptable retained
contact at all three sites across the permitted site region, assembly
sequence and tolerance cases, with bounded PCB/component strain,
board-fastener and boss loads, and positive clearance from the cell and
unrelated conductors. G5 computes the permitted region from both
geometric containment and those mechanical limits; no ± 1 mm workspace is
promised beforehand. WP11 uses the deformed maximum board envelope and a
positively cleared, unloaded battery envelope. Off-body
contact-stability and post-assembly mechanical checks remain release
requirements; static calculations do not replace them. If these
conditions fail, interface I is not eligible and interface II requires
its own complete qualification and budget.

The candidate mechanism: each standoff (female M2.5, 5 mm across flats;
3.0 or 4.0 per C14, nickel-plated brass on both verified pages, so the
pressure pair is nickel on gold, qualified as that pair) stands captive
in its hex pocket on the floor with the titanium screw threaded into it
from outside, the tip below the top at worst-case screw length, wall,
standoff length and face tilt (nominal 0.5 for the 3.0 part, 1.5 for the
4.0 part). The board carries on its underside one exposed gold pad per
site (ENIG or hard gold, nominal 8 × 8, its net kept clear of all other
copper) and is fastened to two or more printed bosses by ISO 7380 M2.5
screws. The bosses are designed lower than the standoff tops by a
nominal offset the drawing states (0.5 is the starting value; two
independent ± 0.3 heights can differ adversely by 0.6, so the offset is
justified from the datum chain, not from one tolerance figure). The
populated board is the spring: it bends over the offset when the screws
seat, and G7 shows the resulting reaction at every standoff for every
tolerance case, not only that a pad touches first. Contact: the
standoff's top annulus against the pad. Site region: the pad-containment
bound for a 5 mm hexagon in an 8 mm exposed pad is a ≤ 4 − 5/√3 − e =
1.113 − e per axis, e the complete adverse allowance for pad opening,
standoff size and orientation, board-to-shell placement, pocket fit and
edge margin; the released region is G5's output after intersection with
G7's mechanical limits and the clearances, stated per site. A site
outside it is a stop. Path: skin → titanium dome → screw thread →
standoff → gold pad → board. Landing states G7 must show acceptable: pad
fully on the annulus, pad edge over the hole with the tip clear, standoff
at the pad's edge, edge contact on a tilted face. Off-body test:
continuity per site under finger pressure on the shell, a 30 s motion
test on the bench with the trace inspected at the µV scale against a
declared acceptance, repeated after the closure and drop checks of §5.4
and WP14. Interface II (fallback if G7 fails for I): a flex with FR4
stiffeners and three ring pads clamped under the standoffs, with the
same drawing content plus bend radius, strain relief and the assembler's
flex acceptance and fixture price. A third candidate is recorded for the
research lane only, not for the plan: SMD grounding spring contacts on
the board underside (Harwin S17xx/S7121, Würth WE-GSC class) with their
actual travel, force and landing footprint (C16); it enters the plan
only through a turn that qualifies it.

5.4 Charging port. USB-C 16-pin receptacle with 5.1 kΩ CC pull-downs,
its mating axis normal to the medial face near the hook end, opening
about 9.0 × 3.5 with corner radii, the receptacle face recessed ≥ 1.0
below the skin face, ligaments ≥ 1.5 to the hook root and to the nearest
contact pocket, and a silicone plug (a skin-side part, §5.7) that sits
flush when installed. WP11 reports the wall cut and the plug clearance
volume (12 × 6.5 × 15 in front of the opening); WP14 designs the local
wall. Lost plug: the recess keeps the receptacle shell off the skin;
wearing continues only after a spare plug is fitted (three spares in
order 3). Fallback position if the medial face cannot carry the opening
in a closing layout: the hook-end end face, which weakens R7 (ii) to
"awkward" and is said so in the residual-risk list.

5.5 Front end and power. ADS1292 (non-R): AVDD = DVDD from a low-dropout
regulator on the battery (3.0 V nominal candidate; WP12 fixes the LDO
and computes the battery threshold at which AVDD leaves 2.7 V under the
worst-case load, dropout and radio transients), internal 2.42 V
reference, gain 12, 2000 SPS, SIG1/SIG2 to one channel through 220 kΩ
each, the reference contact to the RLD output through its own 220 kΩ,
lead-off detection off when worn. Undervoltage: inhibit acquisition when
the monitored voltage falls to V_STOP, chosen with sensing error,
response latency, regulator and load transients and the pack's normal
discharge endpoint so the AFE remains valid until shutdown; resume only
above V_START > V_STOP after the specified rail and reference settling
checks; report invalid samples and the stop/restart reason; the
10-second battery telemetry cadence is not the protective monitoring
cadence; the pack's 2.4 V protection is cell protection only. Supply
gate: a P-channel switch removes the front end's supply when VBUS is
present, proven per R7 and G2 in the complete circuit or the credit is
withdrawn. BQ25100
family charger: ordering code, ISET (about 6.8 kΩ for 20 mA), PRETERM,
TS network, timers and the parallel system load fixed by WP12 (G1).
Off-body acceptance tests, all before any skin contact: rail voltages
over the battery range, charge current with a meter in series on the
bench, termination observed, RLD stability, leakage through each contact
path to the port shell with the device powered and with VBUS present,
continuity per §5.3.

5.6 Bench connection. A 3-pin 2.54 mm right-angle header (SIG1, SIG2,
REF) at the board edge behind the 220 kΩ, for pre-made snap-electrode
leads with 2.54 mm pin sockets (order 3), on a desk stand (a printed
part in the shell order or a folded card; WP15 says which).

5.7 Materials table (R3): titanium screw (skin; Grade 5 uncoated per the
seller; ISO 7380 conformity and a material record are G3d); PA12 shell
(skin; R3 evidence or acceptance); silicone port plug (skin; material
statement in order 3); nickel-plated brass standoff (inside, under the
board; the pressure pair with the pad is nickel on gold); ENIG pads
(inside, covered by the board and lid);
module shield (inside); receptacle shell (recessed, behind the plug);
cell pouch and PCM (inside, on foam); recovery switch (inside). The
cavity is closed by the lid and the plug, not sealed; nothing inside is
meant to touch skin.

## 6. Acquisition, firmware and the protocol mapping (WP13)

Firmware: nRF Connect SDK (Zephyr) application linked for the Adafruit
nRF52 bootloader's layout (bootloader plus SoftDevice S140 as the factory
image; application at the layout's start address; USB identity and flash
map frozen by WP13 with the bootloader build for this board). ADS1292
over SPI at 2000 SPS. Transport: BLE Nordic UART Service. Before S0, WP13 freezes a
byte-level versioned format containing session/epoch identification,
frame sequence, an acquisition index tied to conversions rather than
only to successful reads, sample count and payload length,
gain/reference/rate metadata, defined ADS status handling, and fragment
identification and reassembly rules; it specifies counter wrap (a 16-bit
index at 2000 SPS wraps every 32.768 s), reconnect and reset,
partial-frame rejection and separate acquisition-overrun versus
transport-loss reporting; receiver fixtures cover all of those cases. N
may adapt to the negotiated payload, with its meaning transmitted or
fixed by the version. Nominal scale 2.42 V / (12 × (2^23 − 1)) ≈ 24.0 nV
per code, differential full scale about ± 201.7 mV, nominal only.
Battery voltage every 10 s; LED state
from the circuit's actual signals; VBUS present → front end off (hardware)
and streaming refused (firmware). Recovery: a tactile switch on the board
under the lid; double-press enters the bootloader (the bootloader's own
mechanism); a bad application image leaves the bootloader drive reachable
the same way; R2b lists it.

Protocol v2 table (before S0, versioned, the one revision the file's rule
allows): for each `montage.md` §3 criterion, the measurement path on this
chain: noise and amplitudes on a digital band-pass (20–490 Hz, filter
named, window named) in input-referred µV; the INA128 output-shift
criterion restated as ± 50 mV input-referred (± 0.5 V at gain 10) on the
DC-preserving path before the high-pass; input and common-mode headroom
separately; dropout kept as the original rule (rail or a flat trace
> 100 ms, defined as more than 200 sample intervals at 2000 SPS) measured
on the acquisition stream, with transport loss reported beside it, not
instead of it; start-up exclusions named. Each line says "same
criterion" or "revised: why", and applying an old amplitude criterion to
this transfer function is an explicit per-line decision, never an
assertion that unit scaling makes the chains identical; no dry data is
judged against an unmapped line. The bench montage procedure (§2 of that file)
is re-targeted to the board on its stand with the §5.6 leads.

## 7. Look (WP14)

- The test: a stranger sees a hearing aid or an earbud. No visible
  screws, no visible seam wider than 0.3 mm, no text outside, no
  printed-layer look (media-blasted matte; vapour smoothing only from a
  vendor whose page states skin-contact testing of the smoothed part).
- Surfaces: one continuously curved lateral shell; no planar facet over
  3 mm; outside edges R ≥ 1.0 except the medial skin face (flat, R0.5).
- Closure: a new dimensioned closure replacing v1's experimental
  tongue, web and lip (E1 dropped, Q28): a cantilever snap with beam
  dimensions, strain, insertion and retention forces, or one concealed
  screw at the tail end plus a hinge lip. Acceptance at S0: the drawing
  and its calculation; at S4: a qualitative hand-retention check (the
  lid does not open under a firm two-finger pull) and a 0.5 m drop onto
  a wooden table with the lid staying closed, both labelled qualitative.
- Hook: elliptical section with stated axes at root and tip, blended
  with a stated fillet; the radius from M8.
- Tail: blended; reference dome per Q17 (his "on bone" stands
  provisionally, checked on the paper template and at S2).
- Colour: grey or dyed black per Rolf (Q30).
- Approval: two renders and one drawing page; his yes before the shell
  order.

## 8. Rolf's part, all of it (R2, R2b)

Before ordering: M1 to M8 per `docs/fab/measure.md`; print `template.pdf`
at 100 %, check its 50 mm bar, cut, hold behind the ear, report; approve
renders; approve the objectives order (§4), R7 as rewritten, and the
residual-risk list (§10); pay the checkouts against their gates.

First load, only if G4 falls to him (once, before assembly; completion
time measured at WP15's rehearsal, not promised): Tag-Connect
TC2030-IDC-NL cable ($33.95 listed; its contacts 1–6 map one-for-one to
the IDC 1–6 per its Rev. B drawing) on the board's footprint in the
keyed orientation, the Raspberry Pi Debug Probe ($12 listed; 3.3 V
nominal I/O) on its supplied male 0.1" breakout, ground connected first.
Proposed net map, to be made true by the released schematic and
verified under G4: IDC 1 target-voltage sense (no probe lead, never a
power feed); 2 SWDIO to the probe's yellow SD; 3 GND to black; 4 SWCLK
to orange SC; 5 GND; 6 nRESET, shared with the recovery switch. The
target runs from its own cell, off-body, electrodes disconnected; one
command from `docs/fab/assemble.md` writes the merged bootloader image;
the drive appearing over USB is the check.

Final assembly, eight steps, one 1.5 mm hex key:

1. Peel the pre-cut foam pad and lay the cell in its pocket; route its
   lead in the channel to the connector.
2. Push the three titanium screws through the dome holes from outside.
3. Drop a brass standoff into each hex pocket inside; turn each screw
   with the hex key until the head seats. Stop.
4. Set the board on the three standoff tops, pads down, holes over the
   bosses.
5. Turn the board screws with the hex key until they seat.
6. Mate only the G1b-qualified pack and connector revision. Before
   plugging it in, verify electrical polarity at the identified connector
   contacts with the sheet's off-body method (a multimeter on the
   connector's contacts, or the supplier's documented test); neither
   keying nor insulation colour proves polarity (the legacy drawing even
   labels black as positive). The meter is in R2b and order 3.
7. Close the lid per WP14's closure.
8. Lay the device medial side up on the desk, plug USB-C from a power
   bank or a listed adapter, read the LED as the sheet defines it.

Firmware: copy the UF2 file to the drive that appears. Recovery: lid
off, double-press the small switch, copy again.

Bench (S2): board on its stand, cell plugged, port capped, no cable,
three snap leads to gel electrodes per `montage.md` §2, laptop receiving.

## 9. Orders, planning allowances and the delivered-spend ledger

Not quotes. Destination Massachusetts, USA, assumed until Rolf confirms.

| Order | Contents | Route (default / US quote-only) | Published components on 2026-09-17 | Allowance |
|---|---|---|---|---|
| 1 Board | 2 to 5 boards, standard PCBA, sides per placement (two-sided assumed), 4-layer ENIG, X-ray for the module, bootloader programming if accepted | JLCPCB / MacroFab or Screaming Circuits | standard setup $25.56 one side or $51.12 two sides; stencil $8.21 or $16.42; feeder $1.53 per part line (standard tier only, not the economic $3.07); X-ray $1.64 per inspected part in the 1–10 bracket; two-fixture $16.42 where applicable | $160–240 |
| 2 Shell | body, lid, spare lid, stand if printed; MJF PA12; finish per R3 | JLC3DP / Xometry | JLC "from $1.00, 72 h" is a starting price only | $50–90, reserved as a maximum before order 1 is paid |
| 3 Small parts | 10 titanium screws (Sortafast $17.50), M2.5 standoffs (Spacer Express 3.0 sold per 100, €91.08 ex VAT for 100 on its page, delivery 5–10 working days, shipping to Massachusetts unverified; Harwin R25-1000402 4.0 at a distributor, small-quantity price unverified), cell (SparkFun $7.39), 1.5 mm hex key, USB-C cable, pre-cut foam pads, three silicone port plugs, three snap-electrode leads with pin sockets, gel electrodes, a nickel test kit or Rolf's written waiver | US sellers, several parcels | screws and cell page-priced; the rest allowances | $80–130 |
| Conditional | first-load kit: TC2030-IDC-NL $33.95 + Debug Probe $12.00 listed, plus jumpers, shipping | US sellers | listed prices, not a complete kit price | $50–70 |

Ledger before the first payment (R8): the selected population and
assembly services, every shipment, applicable Massachusetts sales or use
tax (6.25 % where the seller does not collect it) and the complete import
collection for each China-origin order, taken from a configured DDP
checkout or from a documented classification-based reserve; a percentage
for one trade-remedy component is not the total import reserve (CBP's
2026-07-24 guidance adds 12.5 % under 9903.05.31 for China-origin goods
and JLC's FAQ lists Section 301 at 25 % and its own advance collection;
none of that is a product-level total). Each line is marked quoted,
catalogue-priced or allowance, with included freight, duty and tax
identified so nothing is counted twice. The conditional programming kit
and a multimeter are in when needed. The shell's complete delivered
maximum is reserved before the board is paid; if an adequate supported
reserve cannot be established, G8 is not passed. Base allowances sum to
$290–460, plus $50–70 for the kit if needed; no all-in figure is claimed
until this ledger reproduces one. Named cuts if R8 fails: grey instead
of dyed, no spare lid, two boards instead of five, no programming kit if
the factory programs.

## 10. Release states v2 and residual risk

| State | Entry requires |
|---|---|
| S0 files approved | WP11 winner with G1–G7 evidenced; WP12 ERC/DRC clean in the release job and reviewed against the ADS1292, charger and module reference designs; WP14 checks on the built solid; renders approved; template and chord gate pass on M1; R7 and the residual-risk list accepted by Rolf; whole-project ledger under his ceiling |
| S1 board and parts ordered | S0; the ledger shown; he pays orders 1 and 3 (and the kit if G4 needs it) |
| S2 bench | boards arrive; first load; off-body checks of §5.5; firmware streams with the §6 contract; gel montage on the stand gives three sites inside the §5.3 region; protocol v2 table published before this data |
| S3 shell ordered | S2 sites into interface v3; WP14 re-run; renders re-approved if the shape changed; the ledger updated; he pays order 2 within its reserved maximum |
| S4 assembled | §8 done; retention and drop checks; continuity per site; nickel screen on the domes if a kit exists, else the waiver |
| S5 validation wear | protocol v2 as v1's S3, ≤ 4 h/day |
| S6 routine use | all criteria pass |

Residual risks accepted before S1, in writing: no galvanic isolation
between USB-connected circuitry and the electrode paths, with R7's
procedural rule and its stated limits (the 220 kΩ per-path bound is not
a total or single-fault bound; the supply gate is an inhibit, not
isolation; exposure can arise from one broken rule); analog noise and antenna behaviour
on the head are first measured at S2 and S5; comfort and skin pressure
are first felt at S4; a lost port plug exposes a recessed receptacle
shell; a failed S5 leaves a bench device and no further spend without
Rolf's decision.

## 11. Work packages v2

| WP | Owns | Output | Acceptance |
|---|---|---|---|
| 11 Packing v2 | `placement.py`, Stage B of `bte_fit_shell.py`, `docs/fab/packing-v2.md` | A and B, interfaces I and II, series and stacked, lids 6.0–9.0, widths 18–20, verified envelopes only (standoffs 3.0, 3.5 and 4.0, the deformed board envelope on them, the cell under the board only with positive clearance and no load, or beside it, harness, medial opening and plug volume, bench header, switch); the per-site region from pad containment, pending G7's mechanical limits | measured on the built solid; the table says which close and why the rest fail |
| 12 Board | `hardware/board/`, `docs/fab/board.md` | KiCad project, ERC/DRC, BOM with assembler codes, STEP, joint drawing, G2 diagram, charger and undervoltage calculations | traced values; release job passes; reviewed against reference designs |
| 13 Firmware | `firmware/`, protocol v2 table in `montage.md` | bootloader build and layout, streaming firmware with the §6 frame, receiver | builds in CI; bench-tested at S2 |
| 14 Shell v2 | `scripts/cad/`, `docs/fab/cad/v2/` | body, lid, closure and hook drawings, port wall, bosses, pockets, renders, manifest | §7 checks; Stage B checks on the built solid; identical regeneration |
| 15 Rolf's sheets v2 | `measure.md`, `template.pdf`, `order-board.md`, `order-shell.md`, `order-parts.md`, `assemble.md` | sheets with pictures, the ledger, three checkout gates, the §8 steps, the first-load pin map, the polarity check | no step needs a question; the first-load procedure rehearsed on paper |
| 16 Record | `docs/EARPIECE_DESIGN.md`, requirement 5 | v2 decisions once each; requirement 5 to titanium | each decision appears once |

## 12. Claims still open

C1 process-and-finish skin evidence or Rolf's acceptance (R3); C5 E73
stock, price and antenna keep-out; C6 assembler programming acceptance
and price (quote-only); C7 only for interface II; C9 screw conformity and
a standoff page; C10 non-R ADS1292 stock on the order day; C11 closed
by turn 06 (no stocked spring-loaded SMD pin at a 2.0–2.5 working
height; the pins are gone); C12 the harness drawing; C13 the complete
import collection for China-origin PCBA and prints delivered to
Massachusetts (CBP CSMS 69326983 is primary evidence for a 12.5 %
component, not a product total); C14 the standoff per height actually
used, with exact SKU, on-hand availability and purchase quantity,
landing drawing, thread depth, tolerances, base material and finish and
delivered cost (turn 08: Spacer Express LAI-FF-M2.5-SW5-L3-100 at 3.0 and
Harwin R25-1000402 at 4.0 exist as catalogue pages, nickel plated, no
stock count or landing drawing; nothing at 3.5); C15 JLC MJF PA12
minimum wall for a 0.5 floor recess under the cell; C16 an SMD grounding
spring contact with verified travel, force and footprint, research only.

## 13. Decisions for the dialogue, then Rolf

- D-1 Thickness: from WP11's table; thin live.
- D-2 Gates G1–G8, then objectives height, Rolf's burden, cost.
- D-3 Interface I: board pulled onto standoff tops by its own screws,
  gold pads, the board as the spring, under the §5.3 contract; an
  unqualified candidate until G7; standoff 3.0 or 4.0 per C14; II as
  fallback.
- D-4 Cell DTP301120 with a BQ25100-class charger at 20 mA, termination
  and timers active, TS fixed network, temperature window by procedure.
- D-5 R7 as rewritten with Pro's limits: a procedural rule for Rolf's
  informed acceptance; per-path bound only; inhibit, not isolation;
  medial-face exclusion; gel-bench disconnect procedure.
- D-6 Streaming firmware with the §6 frame contract; Adafruit-style
  bootloader plus SoftDevice as factory image; protocol v2 table.
- D-7 Board and parts, bench, then shell; sites only inside the stated
  region; no simultaneous shell order.
- D-8 JLC as candidate with US quote-only routes; Massachusetts assumed.

Open for Rolf: M1–M8, the ceiling (Q33), colour (Q30), country and
China-or-not (Q36), the objectives order (§4), R7 as rewritten, and the
residual-risk list (§10).
