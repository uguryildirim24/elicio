# Elicio earpiece — fabrication plan

Phase 0 synthesis and Phase 1 specification for the Stage B behind-the-ear
shell. Draft, turn 01, 2026-09-16. Author `fable`, reviewer `pro`. Inputs:
`docs/fab/brief.md`, `docs/EARPIECE_DESIGN.md`, `docs/fab/L1-cad.md` (L1),
`docs/fab/L2-vendors.md` (L2), `docs/fab/L3-contacts.md` (L3),
`docs/fab/L4-pod.md` (L4). Lane reports are evidence, not law; where they
disagree, section 2 picks and says why. Nothing here buys anything.

**For Rolf, in short.** We script the shell in Python (build123d), not
Blender, from eight caliper numbers you take at home, with defaults that
print a plausible shell if you take none. JLCPCB prints it in nylon (MJF
PA12) and ships to Massachusetts with duties prepaid; the first order is
three shells and two lids for about $33. The skin contacts are three small
titanium domes you screw in yourself. The first shell is a fit gauge with no
electronics: you wear it for four hours and answer the checklist in section
3.7. The second shell, with real contact holes, is ordered only after that
check and after the bench amplifier has told us where the contacts belong.

## 1. Decision summary

1. Tool: build123d, headless Python, native STEP; script
   `scripts/cad/bte_fit_shell.py`. Blender only if a scan ever appears.
2. Geometry: no scan and no impression for order 1. A generic behind-the-ear
   shell from L1's seven caliper measurements plus one (helix rise), all with
   defaults.
3. Vendor and material: JLCPCB 3D printing (JLC3DP), HP Multi Jet Fusion
   PA12 nylon, dyed black, DDP shipping. Resin is rejected for any part worn
   on skin.
4. Contacts: three. Grade 2 titanium M3 button-head screws as 5.7 mm domes,
   each floating on a silicone-foam washer with a thin nut and ring lug
   inside; 316 stainless as fallback; nothing gold-plated.
5. Electronics envelope: one 36 × 12.5 × 6.9 mm cavity, battery (501015,
   50 mAh) at the top end, an 18 × 12.5 × 3.3 mm board stack at the bottom
   end over the two signal contacts; reference contact on a 10 mm tail.
   Outer body 38 × 15 × 9.2 mm plus hook. A 7.6 mm "thin" body is printed
   only as a gauge of what a hearing-aid-class thickness would feel like.
6. Order 1: three bodies and two lids, PA12, JLC3DP, about $33 all-in with
   slow DDP shipping, placed by Rolf after he approves the renders.
7. Order 2, after the fit check and the Stage A montage test: two Stage B
   bodies with real contact holes, titanium hardware from McMaster-Carr, and
   a nickel spot-test kit, about $105 total.
8. No agent purchases, uploads, quotes, or contacts anyone.

## 2. Conflicts resolved

| # | Topic | Lanes said | Pick | Why |
|---|---|---|---|---|
| 1 | Battery | L2 assumed 110 mAh; L4 picked 501015 50 mAh (7.3 h streaming) over 401030 100 mAh (30 mm long) | 501015, 50 mAh, 5.0 × 10 × 15 mm | 7 h covers any session; the 100 mAh cell spans the whole body and forces stacking above 10 mm thick; 110 mAh was L2's pricing placeholder |
| 2 | Envelope | L4 33 × 10.5 × 6.8; L2 35 × 20 × 12; L1 34–38 × 7.5–8.2 × 8.5–10 | Body 38 × 15 × 9.2 plus 10 mm tail and hook; thin gauge 7.6 | L4's box cannot hold its own parts: two 16 × 9.5 islands cannot carry a 15.5 × 10.5 module, and a 17 mm battery pocket plus 16 mm of boards in tandem exceed 33 mm. L2's box was for quoting. L1's width assumes no contact hardware. Section 5 derives the number from parts |
| 3 | Contact metal | L3 titanium or 316L domes; L2 316L or gold-plated 4 mm snaps; L4 316L discs | Grade 2 titanium; 316 fallback; gold-plated rejected | Design record says nickel-free. 316L is 10–14 % nickel (release-compliant, not free). Gold flash over a nickel barrier wears through (L3 §5.1.2). Titanium costs about $1.60 more per contact |
| 4 | Contact diameter | L1 3 mm mock studs; L2 4 mm snaps; L3 7–9 mm domes but its concrete parts are M3 (5.7 mm head) | 5.7 mm, ISO 7380 M3 button head | L3's own per-contact force (0.3–0.4 N) over a 7 mm dome is 8–10 kPa, under its own 10–25 kPa window; over 5.7 mm it is 12–16 kPa. M3 hardware intrudes 3.6 mm into the cavity, M4 over 4 mm |
| 5 | Conductive TPU | Design record cites Palmiga; L2 and L3: no bureau prints it; L4 lists it | Dropped for Stage B | No print service will make it; metal domes need no large area (L3 §7.1.4). Revisit only if Rolf owns an FDM printer |
| 6 | Lid closure | L2 M1.6 heat-set inserts; L1 PA12 cantilever snaps at 1.46 % strain | Snap lid: two tabs in the battery zone, tongue at the tail end | Insert bosses (5.3 mm footprint) eat cavity; PA12 elongation supports snaps; no hardware to buy |
| 7 | Fit-check material | L2 9000R resin ($1.50–2.50); L1 resin or nylon | MJF PA12 | The fit check is four hours on skin; unreacted acrylates are an irritant risk (L2 summary 3); same material as order 2 so snap and feel are real; costs $2–3 more per part |
| 8 | Contact montage | L3 horizontal PAM pair 12–15 mm behind the crease, reference at the mastoid tip; L1/L4 a narrow pod in the crease | Pair on the body's medial face, 12 mm pitch, 30° off the body axis; reference on a 10 mm tail over the mastoid surface; all positions parametric; Stage A with gel electrodes fixes them before order 2 | A 15 mm wide pod cannot hold a horizontal 12 mm pair; the mastoid tip sits about 55 mm below the hook root, beyond any behind-the-ear body |
| 9 | Contact count | L4 asks whether to fit 5 (two channels); design record and L3 say 3 | 3 | Clench is 3–5× larger than a flex on the same pair (L3 §2.3); one channel plus reference; the ADS1292's second channel stays spare |
| 10 | Suspension | L3 floating stud plus foam, 0.3–0.4 N each; L4 shell preload only, 0.5 N total | Both: 1.5 mm hook preload (about 0.9 N, estimated) and foam washers | Rigid mounts lose contact under jaw motion (L3 §7.2); the cost is 3.6 mm of cavity depth under the signal contacts, which is why the body is 9.2 mm |
| 11 | Ear capture | L1 putty impression plus photogrammetry ($12–15) versus generic | Generic for order 1; impression deferred to Stage C | L1 §4.3: generic shells fit most adults; the canal tip needs an impression anyway |
| 12 | Shipping | L2 Global Standard DDP $6–10, 10–14 d; DHL DDP $22–28, 3–5 d | Standard for order 1 (Rolf may upgrade); DHL for order 2 | Order 1 is not on the critical path while Stage A is unbuilt |
| 13 | Shell and PCB in one parcel | L2 Q5 | Separate shipments | Different tariff lines; the board is another work package |
| 14 | Hook | L4 flexible silicone/TPU hook; L1 solid 13.5 mm nylon hook | PA12 hook, one piece with the body | One part, one material; PA12 flex supplies the preload at about 0.5 % strain |
| 15 | Lid gasket | L1 Q4 | None; conformal coating on the board | A gasket adds a part and a groove for nothing the prototype needs |
| 16 | Charging port | L4 wants pads on the skin face so charging while worn is impossible | No port in order 1; optional 6 × 3 mm medial window in order 2, off by default | The board decides its charging path; the shell reserves the window (section 5) |

## 3. Fit-check shell specification

### 3.1 Tool and files

- Tool: build123d 0.7+ (Apache-2.0) under `uv`; `uv add build123d trimesh`.
  Reason over Blender: exact booleans, native STEP, deterministic regeneration
  from a parameter file, no GUI. Blender is the fallback only if a scan mesh
  ever needs shrink-wrapping.
- Script: `scripts/cad/bte_fit_shell.py`. Parameters live in
  `scripts/cad/params/default.toml`; Rolf's numbers go in
  `scripts/cad/params/rolf.toml`, which overrides defaults key by key.
- Invocation: `uv run scripts/cad/bte_fit_shell.py --params
  scripts/cad/params/rolf.toml --variant full --preload 1.5 --out
  docs/fab/cad/v1/`. Outputs are committed so Rolf can fetch them on his
  phone.
- Units: millimetres everywhere. Right ear is built; `SIDE=left` mirrors the
  finished solid across the YZ plane.

### 3.2 Frame

Origin at the hook root: the point on the skin where the top of the body meets
the hook, at the superior attachment of the ear. X posterior, Y lateral (away
from the skull), Z superior. The skull is approximated by the plane Y = 0; the
hook preload absorbs the real curvature. `s` is distance down the body's
centre path from the origin.

### 3.3 Parameters

Every parameter has a default; a shell built from defaults alone is a valid
order. "Maps to" names the caliper measurement from 3.4.

| Parameter | Default | Unit | Maps to | Note |
|---|---|---|---|---|
| SIDE | right | – | Rolf's choice | mirror for left |
| VARIANT | full | – | – | full = 9.2 thick, thin = 7.6 |
| BODY_LENGTH | 38.0 | mm | check ≤ 0.8 × M1 | set by contents, not by ear |
| BODY_WIDTH | 15.0 | mm | check vs M6 | set by contents |
| BODY_THICK | 9.2 (thin 7.6) | mm | check ≤ M3 − 1 | covertness gauge |
| CREASE_BOW | 3.0 | mm | M1, M2 | posterior bow at mid-length; from arc–chord if measured, else default |
| TAIL_LENGTH | 10.0 | mm | check BODY_LENGTH + TAIL ≤ M1 − 3 | carries the reference contact |
| TAIL_THICK | 4.8 | mm | – | 1.2 wall + 3.6 pocket |
| TAIL_TIP_WIDTH | 9.0 | mm | – | tapers from BODY_WIDTH |
| WALL_MEDIAL | 1.2 | mm | – | carries contacts |
| WALL_SIDE | 1.25 | mm | – | |
| WALL_END | 1.0 | mm | – | |
| LID_THICK | 1.0 | mm | – | |
| LID_CLEAR | 0.3 | mm | – | MJF mating clearance |
| CAVITY_LENGTH | 36.0 | mm | – | derived: BODY_LENGTH − 2 × WALL_END |
| CAVITY_WIDTH | 12.5 | mm | – | derived |
| CAVITY_DEPTH | 6.9 (thin 5.4) | mm | – | derived: BODY_THICK − WALL_MEDIAL − LID_THICK − 0.1 |
| BATTERY_POCKET | 16.8 × 10.6 × 5.4 | mm | – | superior end, centred in width |
| BOARD_ZONE | 18.0 × 12.5 × full depth | mm | – | inferior end |
| RIB | 0.8 × 3.0 | mm | – | between pockets, thickness × height |
| HOOK_RADIUS | 13.5 | mm | M8 + HOOK_DIA/2 + 1.0 | centre-line radius |
| HOOK_ANGLE | 145 | deg | – | L1 |
| HOOK_DIA | 3.5 | mm | – | round section |
| HOOK_Y | 3.0 | mm | M4 / 2 | lateral offset of the hook plane |
| HOOK_PRELOAD | 1.5 | mm | – | body tilted so the tail tip sits this far medial of Y = 0 |
| GLASSES_RELIEF | 2.5 | mm | M5 (0 = none) | 45° chamfer, lateral-superior edge of hook crest and body top |
| CONTACT_DIA | 5.7 | mm | – | ISO 7380 M3 head |
| CONTACT_CROWN | 1.65 | mm | – | dome height |
| CONTACT_STANDOFF | 0.6 | mm | – | compressed foam washer |
| CONTACT_HOLE | 3.4 | mm | – | Stage B only |
| CONTACT_POCKET | Ø7.5 × 3.6 | mm | – | nut, lug, travel; Stage B only |
| FOAM_OD | 7.0 | mm | – | washer footprint |
| CONTACT_1 | X 4.5, s 22.5 | mm | s = M7, clamped 19.5–22.8 | signal + |
| CONTACT_PITCH | 12.0 | mm | – | L3 IED 12–15 |
| PAIR_ANGLE | 30 | deg | – | from body axis toward posterior; contact 2 = contact 1 + pitch × (sin, −cos) |
| CONTACT_REF | X 7.5, s 43.5 | mm | X = min(M6, 7.5) | on the tail |
| MOCK_CONTACTS | true | – | – | fit check prints domes; Stage B cuts holes |
| CABLE_EXIT_DIA | 2.0 | mm | – | inferior end wall; 0 = none |
| LEAD_CHANNEL | 1.5 × 1.5 | mm | – | cavity to tail pocket |
| CHARGE_WINDOW | false | – | – | 6 × 3 mm medial window at s 5–11, X 7.5 |
| FILLET_LATERAL | 3.0 | mm | – | lateral long edges |
| FILLET_MEDIAL | 1.0 | mm | – | medial long edges |
| TIP_ROUND | 4.0 | mm | – | tail tip |
| MESH_CHORD | 0.02 | mm | – | STL export |
| MESH_ANGLE | 5 | deg | – | STL export |

Derived checks the script must print and fail on: dome crowns of contacts 1
and 2 inside the medial face by ≥ 1.0 mm margin; ref dome inside the tail;
BODY_LENGTH + TAIL_LENGTH ≤ M1 − 3; the lid tabs clear the battery pocket by
≥ 0.25 mm.

### 3.4 Caliper protocol for Rolf

Ten minutes with a digital caliper and a piece of string. Enter numbers in
`rolf.toml`; skip any and the default stands. L1's M1–M7 plus M8.

| No. | Measure | How | Typical | Feeds |
|---|---|---|---|---|
| M1 | Ear root length | Caliper, top attachment to bottom attachment, straight | 45–58 | length checks |
| M2 | Crease arc length | String along the crease bottom, same endpoints | 50–65 | CREASE_BOW |
| M3 | Sulcus clearance | Depth rod, skull to helix rim at mid-height | 8–14 | thickness check |
| M4 | Helix root thickness | Jaws across the cartilage bridge at the top, no squeeze | 4.5–7.5 | HOOK_Y |
| M5 | Glasses temple thickness | Jaws on the temple where it passes the ear | 1.8–3.2, or 0 | GLASSES_RELIEF |
| M6 | Mastoid offset | Crease to the bony bump behind the lower ear | 12–18 | CONTACT_REF X |
| M7 | Crease top to mid-concha | Along the crease, top fold to the level of the canal opening | 18–26 | CONTACT_1 s |
| M8 | Helix rise | Top attachment point up to the highest point of the ear rim | 8–14 | HOOK_RADIUS |

### 3.5 Construction (what the script does, in order)

1. Path: three-point arc in the XZ plane from (0, 0, 0) through
   (CREASE_BOW, 0, −BODY_LENGTH/2) to (0, 0, −BODY_LENGTH). Extend by
   TAIL_LENGTH on the same arc.
2. Body: sweep a rounded rectangle BODY_WIDTH × BODY_THICK (X from 0 to
   BODY_WIDTH, Y from 0 to BODY_THICK; medial corners FILLET_MEDIAL, lateral
   corners FILLET_LATERAL) along the body part of the path. Sweep a second
   section for the tail: width tapering to TAIL_TIP_WIDTH, thickness
   TAIL_THICK, tip rounded TIP_ROUND. Union.
3. Cavity: from the lateral face, cut CAVITY_LENGTH × CAVITY_WIDTH ×
   CAVITY_DEPTH, ends WALL_END from the body ends. Leave the RIB at
   s = WALL_END + 16.8 from the medial floor. Battery pocket is the space
   above the rib; board zone is below it (inferior). Four corner pads
   1.5 × 1.5 × 3.6 in the board zone hold the board off the floor.
4. Lid rebate: from the lateral face cut a pocket (CAVITY_LENGTH + 1.0) ×
   (CAVITY_WIDTH + 1.5) × LID_THICK, leaving a ledge 0.75 on the long sides
   and 0.5 at the ends. Windows for the snap tabs: two 0.5 deep × 2.0 tall
   × 6.0 long recesses in the long walls, centred at s = 9, starting 6.0
   below the ledge. Tongue slot at the inferior end wall: 2.0 wide × 0.6
   deep × 1.0 tall under the ledge.
5. Lid: plate (CAVITY_LENGTH + 1.0 − 2 × LID_CLEAR) × (CAVITY_WIDTH + 1.5 −
   2 × LID_CLEAR) × LID_THICK. Two cantilever tabs on the long edges at
   s = 9: 1.0 thick, 6.0 long, 6.0 wide, 0.35 outward bump, 0.5 root fillet
   (L1 §5.2: 1.46 % strain). Tongue 2.0 × 0.5 at the inferior end.
   Fingernail notch 6 × 1.5 × 0.5 at the superior end of the lid. Emboss
   `ELICIO V1 R FULL P15` 0.5 mm high on the inside.
6. Hook: circle HOOK_DIA swept along an arc of radius HOOK_RADIUS, angle
   HOOK_ANGLE, in the plane Y = HOOK_Y, centre (−HOOK_RADIUS, HOOK_Y, 0),
   starting tangent +Z at the origin, going up and over anteriorly. Blend
   into the body top with a 2.0 fillet. Glasses relief: 45° chamfer of
   GLASSES_RELIEF along the lateral-superior edge over the top 90° of the
   hook and the top 12 mm of the body's lateral-superior edge.
7. Preload: rotate the body and tail (not the hook) about the X axis through
   the origin so the tail tip moves −HOOK_PRELOAD in Y.
8. Contacts: if MOCK_CONTACTS, add a cylinder Ø CONTACT_DIA × CONTACT_STANDOFF
   topped by a spherical cap of height CONTACT_CROWN at each contact position
   on the medial face (Y = 0, standing to −Y). Else cut Ø CONTACT_HOLE
   through the wall and a Ø7.5 × 3.6 pocket into the cavity floor (ref: into
   the tail from the lateral side), plus LEAD_CHANNEL from the ref pocket to
   the cavity and CABLE_EXIT_DIA through the inferior end wall.
9. Export per 3.6; run the checks in 3.3; write `manifest.json` with every
   parameter, git commit, and file hashes.

### 3.6 Design rules (JLC3DP MJF PA12, from L1 §5.1; UNVERIFIED against the live page)

| Rule | Value | Applied as |
|---|---|---|
| Minimum wall | 0.8 (recommend 1.0–1.2) | walls 1.0–1.25, medial 1.2 |
| Mating clearance | 0.25–0.35 | 0.3 |
| Minimum hole | 1.0 | smallest hole 1.5 (lead channel) |
| Tolerance | ±0.15 | lid and tabs sized for it |
| Snap fit | allowed, strain ≤ 3 % | 1.46 % |
| Powder escape | any closed void needs an opening | cavity is open; no closed voids |
| Emboss | ≥ 0.5 mm | 0.5 |

Outputs: `body_full_p15.step/.stl/.3mf`, `body_thin_p15.*`,
`body_full_p25.*`, `lid.*`, `render_side.png`, `render_iso.png`,
`drawing.pdf` (one page: side, top and section views with M1–M8 and the
critical dimensions: cavity +0.2/−0.0, contact positions ±0.2), and
`manifest.json`. STL must be watertight (trimesh `is_watertight`), chord
0.02, angle 5°.

### 3.7 Acceptance: what Rolf checks wearing it

Weight the cavity with about 4 g (two M6 nuts or fishing split-shot) before
the retention tests. Do the list with the full body first, then the thin one,
then the 2.5 mm preload body.

1. Goes on and comes off one-handed in under five seconds without pulling
   the ear.
2. Stays put through ten head shakes, five hard jaw clenches, three yawns,
   one flight of stairs.
3. One hour: no pain, no pinch at the hook.
4. Four hours: no red mark under a dome lasting more than 15 minutes after
   removal, no numbness.
5. Photos: front, side, back, with and without glasses. Front: nothing
   visible. Side: no more than a hearing aid shows. Back: his call.
6. All three domes touch skin: a strip of paper slid under each dome is
   pinched, with the head turned left, right, and chin down.
7. Glasses on and off ten times; the shell does not lift.
8. Lid snaps on and off ten times with a fingernail, no cracks.
9. Which thickness is acceptable, and which preload is comfortable.
10. After removal, mark the three dome positions on the skin with a pen and
    photograph; this is the input to the Stage A montage test.

## 4. Contacts specification

Count: three. Two signal contacts on the body's medial face, one reference on
the tail (positions in 3.3, final positions from the Stage A montage test).

| Item | Spec |
|---|---|
| Material | Grade 2 commercially pure titanium (ASTM F67), 0 % nickel. Fallback: 316 stainless (nickel release below EN 1811 limit per L3, but not nickel-free). Gold-plated snaps, pogo pins, and bare ENIG pads rejected: nickel under the gold |
| Geometry | ISO 7380 M3 button head: dome Ø5.7, crown 1.65, 2 mm hex socket in the crown (accepted; it is 1 mm deep). Screw length 6 mm |
| Pressure | Target 10–25 kPa per L3. At 0.3–0.4 N per contact and 25.5 mm² dome area: 12–16 kPa |
| Suspension | Silicone foam washer Ø7.0 × Ø3.4 × 1.0 mm under the head, outside the wall; inside: M3 crimp ring lug then M3 thin nut (DIN 439, 1.8 mm). The nut sets the outward stop; skin pressure compresses the foam and the nut lifts into the Ø7.5 × 3.6 pocket. Travel about 0.5 mm. Plus 1.5 mm hook preload for gross clamping |
| Mounting | Through Ø3.4 hole in the 1.2 mm medial wall (body) or tail. No adhesive on the skin side. Assembly by Rolf with a 2 mm hex key and a 5.5 mm nut driver |
| Leads | 28 AWG silicone-insulated stranded wire, ≤ 40 mm each, twisted, crimped to the ring lug. Reference lead runs through the LEAD_CHANNEL into the cavity. Board end: three pads or a 3-pin 1.0 mm connector, the board package decides. The 220 kΩ series resistor and clamps are on the board within 10 mm of the pads (L4 §5.1) |
| Cleaning | Wipe domes with 70 % isopropanol; replace foam washers when soiled |

Sourcing candidates. Prices are from L3 unless marked; none was checked
against a live page.

| Part | Source | Price | Status |
|---|---|---|---|
| Grade 2 Ti M3 × 6 button head, pack of 10 | McMaster-Carr 93625A110 | $18.65 | UNVERIFIED (L3 §5.1.3) |
| 316 M3 × 6 button head, pack of 50 (fallback) | McMaster-Carr 92095A178 | $11.20 | UNVERIFIED (L3 §5.1.1) |
| ASTM F136 titanium flat-back labret studs (alternate dome) | bodyartforms.com | $4.50–7.00 each | UNVERIFIED (L3 §5.1.3); post is 1.2 mm, no lug possible |
| M3 thin nuts, 316 or titanium, pack | McMaster-Carr | ≈ $6 | UNVERIFIED, no part number yet |
| M3 ring terminals, 22–26 AWG, pack | McMaster-Carr or DigiKey | ≈ $8 | UNVERIFIED |
| Silicone foam sheet 1 mm (Rogers Bisco HT-800 or equivalent) | McMaster-Carr | ≈ $12 | UNVERIFIED (L3 names the material, not a source) |
| Dimethylglyoxime nickel spot test (Nickel Alert) | nonickel.com | ≈ $18 | UNVERIFIED (L3 §7.3 names it, no price) |

Nickel verification, in order: (1) buy only parts sold as Grade 2 or Grade 5
titanium (or 316 for the fallback) and keep the order page; McMaster
certificates on request are UNVERIFIED. (2) On receipt, DMG swab every dome
and nut for 60 s; any pink means reject the lot. (3) Repeat the swab after
two weeks of wear. EN 1811 lab testing is out of scope.

## 5. Electronics envelope handoff

The board is out of scope. The shell reserves the following; the board
designer confirms fit against `docs/fab/cad/v1/envelope.step` (WP5) before
order 2.

| Feature | Reserved | Note |
|---|---|---|
| Cavity | 36.0 × 12.5 × 6.9 mm (L × W × depth from lid underside to floor) | thin variant 5.4, gauge only |
| Battery pocket | 16.8 × 10.6 × 5.4 at the superior end, centred | 501015 cell 5.0 × 10 × 15 plus tabs; PCM strip folded over the top |
| Rib | 0.8 thick, 3.0 high | flex bridge or wires pass over it |
| Board zone | 18.0 × 12.5 mm floor, usable height 3.3 above the corner pads | pads at 3.6 from the floor clear the contact pockets; FR4 1.0 plus 2.1 of components on the lateral side; medial side of the board component-free |
| Contact keep-outs | two cylinders Ø7.5 × 3.6 rising from the floor at CONTACT_1 and CONTACT_2 | nut and lug travel |
| Lead entry | ref lead via LEAD_CHANNEL at the inferior end wall; signal leads rise beside the board | three pads or one 3-pin connector on the board edge |
| Antenna | module antenna toward the lateral-superior corner of the board zone, ≥ 5 mm from the battery | Raytac MDBT50Q 15.5 × 10.5 × 2.05 sets the 12.5 width; L4's 9.5 mm islands are too narrow |
| Retention | no screws; a 1 mm foam pad under the lid presses board and battery | |
| Charging | no port in order 1; optional 6 × 3 mm window on the medial face at s 5–11 for skin-side pads (L4 §5.3) | CHARGE_WINDOW |
| Debug | Ø2.0 cable exit at the inferior end wall, plugged in Stage B | tethered bring-up |

## 6. Skin, safety, hygiene

Material: MJF PA12 is chosen because sintered polyamide 12 has no residual
monomer, tolerates isopropanol, and is the safest uncertified polymer the
bureaus offer (L2 summary 3). HP states its PA12 powder meets USP Class VI
and intact-skin contact guidance; that claim is UNVERIFIED and section 8
lists it. Resin parts never touch skin. Skin-facing metal is titanium only.
Foam washers are silicone. No paint, glue, or coating on the skin side. The
black dye's skin record is UNVERIFIED; if the four-hour wear shows redness
away from the domes, reorder in natural grey.

Cleaning: wipe the medial face and domes with 70 % isopropanol after each
wear and let it dry; never acetone. Washers are consumables.

Battery-only rule as shell constraints: the shell has no power connector and
no mains-capable opening; its only openings are the contact holes, the
optional skin-side charge window (charging while worn is then physically
blocked, L4 §5.3), and a 2 mm debug exit that is plugged in Stage B.
Tethered debugging goes through that exit only with the laptop on battery.

Series-protection rule as shell constraints: leads are the only conductors
between skin and board; each is ≤ 40 mm and lands on a pad that has its
220 kΩ resistor and clamp within 10 mm. Nothing in the shell path can
stimulate: no metal touches skin except the three domes, and the domes
connect only to those pads.

## 7. Orders

Price sources: JLC3DP ranges from L2 §1.1 (jlcpcb.com/3d-printing, read
2026-09-16), tariff from L2 §2.2 (jlcpcb.com/help/article/us-tariff-faq,
dated 2026-03-17). All are ranges, not quotes; the exact price appears only
after Rolf uploads the files. No line item exceeds $200.

### Order 1: fit-check shell

| Item | Value |
|---|---|
| Vendor, process, material | JLCPCB 3D printing (JLC3DP), HP MJF, PA12-HP, dyed black |
| Parts | body_full_p15, body_thin_p15, body_full_p25 (1 each); lid (2) |
| Files | the five STL files from `docs/fab/cad/v1/` (STEP also uploadable) |
| Parts cost | 3 bodies at $3.50–5.50, 2 lids at about $2: $16–21 (L2 range) |
| Tariff | 40 % of parts, collected at checkout, DDP: $6.50–8.50 (L2, UNVERIFIED rate) |
| Shipping | Global Standard DDP $6–10, 10–14 days; or DHL DDP $22–28, 3–5 days |
| All-in | about $33 standard, about $49 DHL |
| Lead time | 48–72 h production plus transit: 12–17 days standard, 5–8 days DHL |

What Rolf does, and only after he has approved the two renders:
1. Download the five STL files from the repo.
2. jlcpcb.com/3d-printing, "Add 3D files", upload all five.
3. Per file: MJF, PA12-HP, black; quantity 2 for the lid; no post-processing.
4. Read the automatic DFM warnings; anything about wall thickness goes back
   to WP1 before ordering.
5. Shipping to Massachusetts; pick a DDP option; confirm the tariff line is
   on the invoice. Never CPT.
6. Pay; paste the order number and total into `docs/fab/orders.md`.

### Order 2: Stage B shell and contact hardware

Placed only after 3.7 passes, the Stage A montage test has set the contact
positions, and the board designer has signed the envelope.

| Item | Value |
|---|---|
| Shell | JLC3DP, MJF PA12-HP black, 2 bodies (Stage B variant: real holes and pockets, MOCK_CONTACTS false) + 2 lids; DHL DDP. Parts $11–15, tariff $4.50–6, shipping $22–28: about $42 |
| Hardware | McMaster-Carr: Ti M3 × 6 button heads $18.65, M3 thin nuts ≈ $6, ring terminals ≈ $8, silicone foam ≈ $12; nickel test kit ≈ $18. About $63, prices UNVERIFIED |
| All-in | about $105 |
| Lead time | shell 5–8 days; McMaster 1–2 days to Massachusetts |
| Rolf | same upload steps; one McMaster cart; one nonickel.com cart; DMG-test every metal part on arrival; assemble per WP4's sheet |

## 8. Claims to verify before ordering

| # | Claim | Source | Verified by |
|---|---|---|---|
| 1 | JLC3DP collects a 40 % advance tariff on 3D-printed plastics under DDP | L2 §2.2, tariff FAQ 2026-03-17 | nobody yet |
| 2 | De minimis suspended for China parcels; DDP needed | L2 §2.1 | nobody yet |
| 3 | MJF PA12-HP one-off price $3.50–5.50 for a 35 mm shell | L2 §1.1 | nobody yet |
| 4 | Global Standard DDP $6–10 offered for 3D parts to the US | L2 §1.1 | nobody yet |
| 5 | MJF PA12 rules: wall 0.8 min, clearance 0.25–0.35, tolerance ±0.15, snaps allowed | L1 §5.1 (jlc3dp.com guideline) | nobody yet |
| 6 | HP PA12 (MJF) meets USP Class VI and intact-skin contact guidance | not in any lane; author's recollection | UNVERIFIED |
| 7 | JLC black dye is skin-tolerable | none | UNVERIFIED |
| 8 | McMaster 93625A110 is Grade 2 Ti M3 × 6 button head, $18.65 per 10 | L3 §5.1.3 | UNVERIFIED |
| 9 | ISO 7380 M3 head: Ø5.7, height 1.65 | standard; L3 quotes the same for 92095A178 | nobody yet |
| 10 | 316L nickel release < 0.03 µg/cm²/week under EN 1811 | L3 §5.1.1, no page | UNVERIFIED |
| 11 | Dry-contact pressure window 10–25 kPa | L3 §7.2, no page | UNVERIFIED |
| 12 | Raytac MDBT50Q-1MV2 is 15.5 × 10.5 × 2.05 mm | L4 §1.1, raytac.com | nobody yet |
| 13 | 501015 LiPo is 5.0 × 10 × 15 mm, 50 mAh, with a PCM strip | L4 §1.4, no page | UNVERIFIED |
| 14 | Hook preload 1.5 mm gives about 0.9 N in PA12 (E ≈ 1.7 GPa, Ø3.5, 40 mm) | author's cantilever estimate | measured on the printed part (WP3) |
| 15 | Generic BTE shells fit most adult ears without a scan | L1 §4.3 | tested by 3.7 |

## 9. Phase 1 work packages

One worker each, one to three days, in this order. WP1 and WP2 deliver the
order 1 files first.

| WP | Owns | Inputs | Outputs | Acceptance |
|---|---|---|---|---|
| 1 Shell script | `scripts/cad/`, `docs/fab/cad/v1/*.step .stl .3mf`, `manifest.json` | section 3 | all five parts, both variants, preload 1.5 and 2.5 | runs headless under `uv run`; checks in 3.3 pass; STLs watertight; regenerates byte-identical from `manifest.json` |
| 2 Renders and drawing | `docs/fab/cad/v1/render_*.png`, `drawing.pdf` | WP1 outputs | two renders, one-page drawing | renders show medial and lateral faces with domes; drawing carries M1–M8 and the tolerances in 3.6; readable on a phone |
| 3 Rolf's sheets | `docs/fab/measure.md`, `docs/fab/order1.md`, `docs/fab/orders.md` | 3.4, 3.7, section 7 | measurement sheet, order checklist, order log; a preload test (hang 100 g from the tail tip, measure deflection) | phone-readable, no step needs a question |
| 4 Contacts kit | `docs/fab/contacts.md` | section 4 | bill of materials with verified prices and part numbers, DMG protocol, assembly sheet with torque and lead lengths | every price has a live page and date; assembly fits the 3.6 mm pocket in a paper mock-up |
| 5 Envelope handoff | `docs/fab/envelope.md`, `docs/fab/cad/v1/envelope.step` | section 5, WP1 | keep-out solid and sheet for the board designer | board designer's written confirmation, or a listed change to section 5 |
| 6 Montage test | `docs/fab/montage.md` | section 2 row 8, L3 §2.2, Stage A bench | protocol: gel electrodes at the plan's positions versus L3's horizontal pair, three sessions, SNR table | blocked until Stage A parts are bought; ends with three coordinates for `rolf.toml` |
| 7 Stage B shell | `scripts/cad/` (variant), `docs/fab/cad/v2/` | 3.7 results, WP5, WP6 | order 2 files | same checks as WP1 plus hole and pocket dimensions on the drawing |
| 8 Fold into design record | `docs/EARPIECE_DESIGN.md` | signed-off plan | design record updated | every decision in section 2 appears there once |

## 10. Open items and Open for Rolf

Open items (carried; each names the package and the check that closes it):

1. Contact hardware intrusion: 3.6 mm assumed. WP4 measures a real M3 nut,
   lug and screw tip stack; if over 3.6, WP1 deepens the pockets and
   BODY_THICK grows by the difference.
2. Board zone 18 × 12.5 × 3.3: WP5 closes it with the board designer's
   confirmation.
3. PA12 skin claim and black dye (claims 6, 7): pro or WP4 finds the HP
   material page; otherwise order 1 in natural grey.
4. Hook preload force: WP3's 100 g test; if under 0.5 N or over 1.5 N,
   HOOK_DIA changes for order 2.
5. Tariff and shipping ranges (claims 1–4): closed by the JLC checkout page
   on order 1; Rolf records the real numbers in `docs/fab/orders.md`.
6. Charge window: WP5 decides with the board designer; default off.
7. CREASE_BOW from M1/M2: WP1 writes the arc–chord formula and clamps it to
   1–8 mm.
 8. Total length 48 mm needs M1 ≥ 51. If Rolf's M1 is smaller, WP1 shortens
   the tail to 8 mm and the battery pocket to 16 mm and moves the reference
   to s = 41.5.

Open for Rolf (only he can decide):

1. Take the eight measurements in 3.4, or say "defaults" and order the
   generic shell.
2. Which ear first (default right).
3. Approve the renders, then place order 1; pick standard or DHL shipping.
4. Thickness: after 3.7, accept the 9.2 mm class or ask for the electronics
   to be squeezed toward 7.6 (thinner cell, no per-contact suspension).
5. Titanium (plan) or 316 stainless (cheaper) for the domes.
6. Black or natural grey nylon.
7. Whether to take a silicone impression now ($12–15, L1) or wait for
   Stage C. The plan says wait.
8. Buy the Stage A parts (`docs/STAGE_A_PARTS.md`), which gates WP6 and
   therefore order 2.
