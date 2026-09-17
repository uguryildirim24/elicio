# Elicio earpiece — fabrication plan

Phase 0 synthesis and Phase 1 specification for the Stage B behind-the-ear
shell. Revision 2, turn 03, 2026-09-16. Author `fable`, reviewer `pro`.
Inputs: `docs/fab/brief.md`, `docs/EARPIECE_DESIGN.md`, lane reports L1–L4
in `docs/fab/`, and `tasks/plan/turns/02-pro.md`. Lane reports are evidence,
not law; section 2 picks and says why. Nothing here buys anything.

**For Rolf, in short.** The shell is scripted in Python (build123d), not
Blender, from eight caliper numbers with defaults for any you skip. JLCPCB
prints it in nylon (MJF PA12, natural grey) and ships with duties prepaid.
The first order is a passive fit gauge: three bodies, two lids, one test
coupon, allowance about $40. It tests your ear, not the electronics; the
electronics fit is proved on paper (WP6) before the second order. Measure M1
(ear root length) first: the default shell needs 52 mm or more; below that
the reference contact moves to the hook tip. Contacts are three titanium
domes you screw in; there is no stainless option because the brief says
nickel-free. Nothing is ordered until you approve the renders.

## 1. Decision summary

1. Tool: build123d, headless, native STEP; `scripts/cad/bte_fit_shell.py`.
2. Geometry: no scan, no impression; a generic shell from L1's M1–M7 plus M8
   (helix rise), each with a published default; a defaults-only build is a
   provisional gauge, not a personal fit.
3. Vendor: JLC3DP, HP MJF PA12-HP, natural grey, DDP. Resin never touches
   skin.
4. Contacts: three Grade 2 or Grade 5 titanium ISO 7380 M2.5 button heads
   (4.7 mm domes), rigidly mounted through a 1.5 mm wall with a ring lug and
   thin nut inside; hook preload supplies clamping. Per-contact suspension is
   deferred to the active-contact gate. No stainless fallback.
5. Envelope: cavity 36.7 × 14.0 × 6.5 mm; battery (501015, 50 mAh) at the top,
   a 19 × 12.5 mm board zone at the bottom over the two signal contacts;
   reference in a 10.2 mm tail. Body 48.4 × 17.0 × 9.0 mm plus hook, with a
   7.0 mm thin gauge. These are design values pending WP6's packing proof.
6. Order 1: gauge set, provisional, allowance $30–41 standard shipping.
7. Order 2: two Stage B bodies plus verified titanium hardware and a nickel
   test kit, allowance about $120, after the fit check, the montage test,
   and the packing proof.
8. No agent purchases, uploads, quotes, or contacts anyone.

## 2. Conflicts resolved

| # | Topic | Lanes said | Pick | Why |
|---|---|---|---|---|
| 1 | Battery | L2 assumed 110 mAh; L4 picked 501015 50 mAh over 401030 100 mAh | 501015 | 7 h streaming covers a session; 30 mm cell forces stacking past 10 mm thick; 110 was a pricing box |
| 2 | Envelope | L4 33 × 10.5 × 6.8; L2 35 × 20 × 12; L1 34–38 × 7.5–8.2 × 8.5–10 | 48.4 × 17 × 9.0, derived in §5 | L4's 16 × 9.5 islands cannot carry a 15.5 × 10.5 module; L2's box was for quoting; L1 assumes no contact hardware. Length is set by battery, module, and three contact keep-outs, width by module plus front-end parts |
| 3 | Contact metal | L3 Ti or 316L; L2 316L or gold-plated snaps; L4 316L | Titanium only | Brief and design record say nickel-free; 316L is 10–14 % Ni; gold flash over nickel wears through (L3 §5.1.2). Changing the requirement is Rolf's, outside this plan |
| 4 | Contact size | L1 3 mm; L2 4 mm; L3 7–9 mm, concrete part M3 | ISO 7380 M2.5, 4.7 mm dome; M3 is a parameter switch (+2.4 mm length) | L3's 0.3–0.4 N over 7 mm is 8–10 kPa, under its own window; over 4.7 mm it is 17–23 kPa. Every millimetre of nut keep-out costs body length; pressure numbers are exploratory (§4) |
| 5 | Conductive TPU | Design record cites Palmiga; L2/L3 say bureaus do not print it | Titanium primary; Palmiga's service kept as a conditional alternative | Palmiga offers conductive TPU printing (turn 02, finding 12). Titanium wins on assembly into nylon, small area, and no third supplier; TPU needs 12–16 mm pads the face cannot spare |
| 6 | Lid closure | L2 heat-set inserts; L1 PA12 snaps | External snap lip at the top, tongue at the tail tip, two nubs; nylon screw as fallback | Nothing inside the cavity; JLC says ±0.3 mm and > 1.5 mm for snap features, so the coupon in order 1 tests the lip |
| 7 | Gauge material | L2 resin; L1 either | MJF PA12 | Hours on skin; same material as order 2 |
| 8 | Montage | L3 horizontal PAM pair, reference at mastoid tip; L1/L4 narrow pod | Pair at 22° off the body axis, 12 mm pitch; reference on a tail over the mastoid surface, or on the hook tip for short ears; Stage A gel test fixes positions | 17 mm face cannot hold a horizontal pair; the mastoid tip is beyond any BTE body |
| 9 | Contact count | L4 asks 5; design record and L3 say 3 | 3 | Clench is 3–5× a flex on the same pair |
| 10 | Suspension | L3 floating stud plus foam; L4 shell preload only | Rigid mount, hook preload 1.5 mm; suspension deferred | A floating M3 stack does not fit under the board (turn 02, finding 4); skin compliance and preload first, measured at the active gate |
| 11 | Ear capture | L1 putty impression versus generic | Generic gauge; impression at Stage C | Gauge is $40 and tests the real ear |
| 12 | Shipping | L2 standard DDP versus DHL DDP | Standard for order 1, DHL for order 2 | Order 1 is not on the critical path |
| 13 | Shells and PCB in one parcel | L2 Q5 | Separate | Different tariff lines |
| 14 | Hook | L4 flexible TPU; L1 nylon | PA12, one piece | One material; preload from PA12 flex, measured in WP4 |
| 15 | Gasket | L1 Q4 | None | Prototype |
| 16 | Charging | L4 skin-side pads | No port, no window; charge pads inside the closed cavity, lid off to charge | Pad placement alone is not an interlock (turn 02, finding 10) |

## 3. Fit-check shell specification

### 3.1 Tool and files

- build123d 0.7+ under `uv` (`uv add build123d trimesh`). Blender only if
  a scan mesh ever needs shrink-wrapping.
- Script `scripts/cad/bte_fit_shell.py`; defaults in
  `scripts/cad/params/default.toml`; Rolf's numbers in
  `scripts/cad/params/rolf.toml`, key-by-key override; a missing key takes
  the default and the manifest lists it as `default`.
- `uv run scripts/cad/bte_fit_shell.py --params rolf.toml --variant full
  --preload 1.5 --out docs/fab/cad/v1/`. Outputs are committed.
- Millimetres. Right ear built; `SIDE=left` mirrors every output solid
  across the plane X = 0, after which +X is anterior. Parameters keep their
  right-ear meaning.

### 3.2 Frames

Shell frame: origin O at the hook root reference on the top face of the
body; X posterior, Y lateral, Z superior. The hook and the final assembly
live here. The ear's skull surface is the plane Y = 0 in this frame when
the hook rests on the ear.

Body frame: the shell frame rotated about the X axis through O by −θ,
θ = atan(HOOK_PRELOAD / TOTAL_LENGTH) = 1.78° at defaults, so the tail tip
sits HOOK_PRELOAD medial of Y = 0. Body, tail, cavity, pockets, rib, pads,
contact holes, lid features, and the lid itself are built in the body
frame, where the medial face is the plane Y = 0 and every contact axis is
−Y. They are then transformed into the shell frame as one group. The lid
receives the identical transform.

Path coordinates: the body path is a planar arc in the body frame's XZ
plane; `s` is arc length from O, `u` is offset along the section's in-plane
normal on the posterior side, `y` is lateral height. Chord and arc differ:
BODY_CHORD is the endpoint separation, arc length is derived and reported.
A helper `P(u, s, y)` maps path coordinates to body-frame points; all
feature placements use it.

### 3.3 Parameters (defaults are the reference-ear build)

| Parameter | Default | Unit | From | Note |
|---|---|---|---|---|
| SIDE | right | – | Rolf | |
| VARIANT | full | – | – | full 9.0, thin 7.0 |
| REF_SITE | tail | – | M1 | tail if M1 ≥ 52, else hook_tip |
| BODY_CHORD | 48.4 (hook_tip 38.2) | mm | – | set by contents |
| BODY_WIDTH | 17.0 | mm | – | set by contents |
| BODY_THICK | 9.0 / 7.0 | mm | – | |
| CREASE_BOW | 3.0 | mm | M1, M2 | posterior bow at mid-chord; from arc–chord when both measured, clamped 1–8 |
| WALL_MEDIAL | 1.5 | mm | – | carries fasteners |
| WALL_SIDE | 1.5 | mm | – | |
| WALL_END | 1.5 | mm | – | both ends of the cavity |
| LID_THICK | 1.0 | mm | – | |
| CLEAR_FIT | 0.4 | mm | – | nominal mating clearance; ±0.3 print tolerance |
| CAVITY | s 1.5–38.2, u 1.5–15.5, y 1.5 up through the lateral face; lid underside at 8.0 (thin 6.0) | mm | – | swept along the path |
| BATTERY_POCKET | s 1.5–17.5, u 3.1–13.9, y 1.5–7.5 | mm | – | cell max 5.2 × 10.4 × 15.6 plus PCM folded on the face |
| RIB | s 17.5–18.3, y 1.5–4.5 | mm | – | full width |
| BOARD_ZONE | s 18.3–37.9, u 1.5–15.5 | mm | – | four pads 1.5 × 1.5 at y 1.5–4.3 in the corners |
| CONTACT_SIZE | M2.5 | – | – | M3 alternative: dome 5.7, keep-out Ø8.1, +2.4 length |
| CONTACT_DOME | 4.7 dia, 1.35 crown | mm | – | ISO 7380 M2.5 |
| CONTACT_HOLE | 2.9 | mm | – | through the medial wall |
| CONTACT_STACK | 2.5 | mm | – | lug 0.5 + nut 1.6 + tip 0.4 above the floor, screw ×4 |
| KEEPOUT | Ø7.1, y 1.5–4.0 | mm | – | nut across corners 5.8, lug 5.5, plus CLEAR_FIT; nothing enters it |
| CONTACT_1 | u 5.9, s 22.0 | mm | – | fixed by keep-out against rib and wall |
| CONTACT_PITCH | 12.0 | mm | – | L3 range 12–15 |
| PAIR_ANGLE | 22 | deg | – | contact 2 = contact 1 + pitch × (sin, +cos): u 10.4, s 33.1 |
| CONTACT_REF | u 8.5, s 42.5 (tail) | mm | M6 recorded | tail pocket Ø6.5 from the lateral face to y 1.5, open to the lid |
| TAIL | s 38.2–48.4, width tapers 17 → 10 from s 38.2 | mm | – | tip round 4.0 |
| HOOK_ROOT | X 4.0, Y 3.0, Z 0 | mm | M4 → Y = M4/2 | on the top face, shell frame |
| HOOK_RADIUS | 13.5 | mm | M8 + 2.75 | centre-line |
| HOOK_ANGLE | 145 | deg | – | arc from −5° (inside the body) to 145° |
| HOOK_DIA | 3.5 | mm | – | |
| HOOK_PRELOAD | 1.5 | mm | – | variants 1.5 and 2.5 |
| GLASSES_FLAT | 0.8 (0 if M5 = 0) | mm | M5 | flat on the hook's lateral-superior side, 30°–120° |
| LID_LIP | u 8–14, 1.0 thick, 5.0 long, 0.4 bump | mm | – | external, on the top face; groove 0.5 × 1.2 at y BODY_THICK − 5.6 to − 4.4 (3.4–4.6 full) |
| LID_TONGUE | 6 wide, 0.5 thick, 1.4 long | mm | – | slot 0.9 × 1.6 under a 1.0 lip at the tail tip |
| LID_NUBS | 0.8 cube at s 17.9, u 1.9 and 15.1 | mm | – | hang 0.8, locate against the walls |
| EMBOSS | 0.8 | mm | – | `ELICIO V1 R FULL P15 REF` inside the lid; REF marks a defaults-only build |
| MOCK_CONTACTS | true | – | – | gauge prints domes; Stage B cuts holes |
| CABLE_EXIT | Ø2.0 at the inferior end wall, u 4 | mm | – | lead exit for tethered bring-up, plugged in Stage B |
| FILLET_MEDIAL | 1.5 | mm | – | medial long edges |
| LID_EDGE | 0.8 | mm | – | lid outer edge fillet |
| MESH | chord 0.02, angle 5° | – | – | STL export |

Reference-ear measurement defaults, used for any key Rolf leaves out: M1 52,
M2 58, M3 11, M4 6.0, M5 2.5, M6 15, M7 22, M8 11.

Checks the script prints and fails on. Design checks (always): one connected
solid per part; every wall from the analytic table ≥ 1.0 and a ray-cast
thickness sample over the medial face, walls, lip, and tail ≥ 1.0; lid and
body intersect empty at nominal and at −0.3 on every mating pair; keep-outs
intersect nothing but air; contact axes equal −Y in the body frame; STLs
watertight. Ear checks (reported, fail only where stated): TOTAL_LENGTH ≤
M1 − 3 (fail); SPAN = BODY_THICK + crown = 10.35 versus M3, reported as
pinna displacement; hook inner rise versus M8 (fail if under).

### 3.4 Caliper protocol for Rolf

Digital caliper and string, ten minutes. Enter in `rolf.toml`; any key left
out takes the reference value above and the build is marked REF.

| No. | Measure | How | Typical | Feeds |
|---|---|---|---|---|
| M1 | Ear root length | Top attachment to bottom attachment, straight | 45–58 | REF_SITE, length check; measure this first |
| M2 | Crease arc | String along the crease, same endpoints | 50–65 | CREASE_BOW |
| M3 | Sulcus clearance | Depth rod, skull to helix rim at mid-height | 8–14 | span report |
| M4 | Helix root thickness | Jaws across the top cartilage bridge, no squeeze | 4.5–7.5 | HOOK_ROOT Y |
| M5 | Glasses temple thickness | Jaws on the temple at the ear, 0 if none | 1.8–3.2 | GLASSES_FLAT |
| M6 | Mastoid offset | Crease to the bony bump behind the lower ear | 12–18 | recorded for WP7 |
| M7 | Crease top to mid-concha | Along the crease to the canal-opening level | 18–26 | recorded for WP7 |
| M8 | Helix rise | Top attachment up to the ear rim's highest point | 8–14 | HOOK_RADIUS |

### 3.5 Construction, in order (body frame unless stated)

1. Path: three-point arc in the XZ plane through (0, 0, 0),
   (CREASE_BOW, 0, −BODY_CHORD/2), (0, 0, −BODY_CHORD). Report arc length.
   Define `P(u, s, y)`: the point at arc length s, offset u along the in-plane
   normal (posterior), height y.
2. Body: sweep the section (u 0–17, y 0–BODY_THICK, medial corners
   FILLET_MEDIAL 1.5, lateral corners sharp) along s 0–38.2 with the
   binormal fixed to Y. Tail: sweep on s 38.2–48.4 with width tapering 17 → 10
   and the same thickness; round the tip 4.0. Union. The medial face is the
   plane y = 0.
3. Cavity: sweep the rectangle (u 1.5–15.5, y 1.5–9.0) along s 1.5–38.2 and
   subtract, leaving the wall tops at y BODY_THICK − 1.0. Add back the rib (s 17.5–18.3, y 1.5–4.5, full width) and four
   pads (1.5 × 1.5, y 1.5–4.3) at the board-zone corners. The battery pocket
   is the space above the rib; it needs no further cut. Flat parts see the
   plan-view bow: 0.32 mm over 16 mm, 0.46 over 19 mm, absorbed by the width
   clearances.
4. Contacts: if MOCK_CONTACTS, at each of P(5.9, 22.0, 0), P(10.4, 33.1, 0),
   P(8.5, 42.5, 0) add a spherical cap Ø4.7, height 1.35, standing to −y.
   Else cut Ø2.9 through the wall at each, cut the tail pocket (Ø6.5 from
   the lateral face down to the inner wall face y 1.5 at the reference), and cut CABLE_EXIT through the
   inferior end wall at u 4, y 3.
5. Lid features on the body: groove for the lip across the top face: cut
   0.5 into the body at s 0–0.5, u 7.5–14.5, y BODY_THICK − 5.6 to
   BODY_THICK − 4.4 (3.4–4.6 on the full body). Slot for the
   tongue at the tail tip: s 46.8–48.4, y BODY_THICK − 2.0 to BODY_THICK − 1.1, u centred, 7 wide,
   under the 1.0 mm lip left at the lateral face. The lateral face of the tail outside the
   pocket and slot stays solid.
6. Lid: plate y BODY_THICK − 1.0 to BODY_THICK with the body's plan outline over s −0.2 to 46.8,
   outer edge fillet 0.8, minus CLEAR_FIT on the outline. Lip: from the
   top end, a tab u 8–14, 1.0 thick, hanging 5.0 from the lid top at
   s −1.2 to −0.2, with a 0.4 bump toward +s at its tip; root fillet 0.5
   (strain 2.4 %). Tongue: 6 wide, 0.5 thick, its top 0.3 below the lid underside,
   extending s 46.8–48.2. Nubs: 0.8 cubes at s 17.9, u 1.9 and 15.1, hanging 0.8 below the lid underside.
   Emboss inside. Nothing else enters the cavity.
7. Hook (shell frame): circle Ø3.5 swept along the arc centred
   (−9.5, 3.0, 0) in the plane Y = 3.0, radius 13.5, from −5° to 145°,
   angle 0 at (4.0, 3.0, 0) with tangent +Z, increasing toward −X. Glasses
   flat: cut 0.8 off the lateral-superior side between 30° and 120°.
8. Assembly: rotate body and lid from the body frame into the shell frame
   about the X axis through O by −θ; union hook and body; fillet the joint
   2.0. Left side: mirror all outputs across X = 0.
9. Run the checks in 3.3; export; write `manifest.json` (parameters, which
   were defaults, git commit, file hashes, part quantities).

### 3.6 Print rules and outputs

JLC3DP MJF PA12-HP, from the pages `pro` checked on 2026-09-16
(jlc3dp.com/help/article/pa12-hp-nylon, updated 2026-07-30;
jlc3dp.com/help/article/3d-printing-design-guideline): tolerance ±0.3 mm
under 100 mm; wall 1 mm listed; snap and fastener features over 1.5 mm;
emboss 0.8 mm; assembly clearance 0.2–0.4 mm. Applied: walls 1.5; nominal
clearances 0.4 with a stated worst case of −0.2 interference on the lip
bump and tongue, which the coupon and hand fitting absorb; drawing
tolerances are ±0.3 general with no tighter callouts.

Coupon: a 12 × 12 × 3 block with holes Ø1.7, Ø2.9, Ø3.4, a 0.9 slot, a 0.4
slot, and a 0.4 rib, printed with order 1 to measure the process before
order 2.

Outputs in `docs/fab/cad/v1/`: `body_full_p15`, `body_thin_p15`,
`body_full_p25`, `lid`, `coupon`, each as `.step`, `.stl`, `.3mf`;
`render_medial.png`, `render_lateral.png`; `drawing.pdf` (side, medial, and
section views; M1–M8; closure section; contact positions); `manifest.json`.
Order manifest: body files ×1 each, lid ×2, coupon ×1: six parts, five files.

### 3.7 Passive fit acceptance

The gauge is provisional: it checks Rolf's ear, comfort, and covertness. It
does not prove electronics fit (WP6) or dry-contact signal (WP7). Put about
4 g in the cavity first (two M6 nuts). Order: full/1.5, thin/1.5, full/2.5.

1. On and off one-handed in under five seconds without pulling the ear.
2. Stays put through ten head shakes, five hard clenches, three yawns, one
   flight of stairs.
3. Wear 15 minutes, inspect the skin; then one hour; then four hours. Remove
   at once on pain, numbness, or any skin reaction, and record it. A red mark
   lasting over 15 minutes after removal is a fail for that variant.
4. Photos: front, side, back, with and without glasses. Front: nothing
   visible. Side: no more than a hearing aid shows. Back: his call.
5. Paper strip under each dome is pinched with the head turned left, right,
   and chin down.
6. Glasses on and off ten times; no lift.
7. Lid on and off ten times; lip and tongue intact; nubs seat.
8. Which thickness and which preload he accepts. These are observations,
   not biocompatibility evidence.
9. Mark the dome positions on the skin, photograph; input to WP7.

## 4. Contacts specification

Three contacts: two signal on the body's medial face, one reference on the
tail (or hook tip). Final positions come from WP7.

| Item | Spec |
|---|---|
| Material | Titanium, Grade 2 (ASTM F67) or Grade 5 (ASTM F1472/F136), bought with the supplier's material statement or mill certificate kept on file. No plating. Nickel content is what the supplier's specification states, not "zero" |
| Geometry | ISO 7380 M2.5 × 4 button head: dome Ø4.7, crown 1.35, 1.5 mm hex socket. Rigid mount through the 1.5 mm wall |
| Inside stack | ring lug (#4 or M2.5, crimped to 28 AWG silicone-insulated wire, 26–28 AWG barrel) 0.5, DIN 439 M2.5 thin nut 1.6, screw tip 0.4: 2.5 mm above the floor. Nut and lug may be plated steel or tinned copper; they never see skin and sit under the lid, with a 0.13 mm Kapton disc over each stack |
| Clamping | hook preload 1.5 mm, estimated 0.9 N total, measured in WP4. Nominal 0.3 N per contact over 17 mm² is 17 kPa. These are exploratory targets, not comfort or performance bounds |
| Leads | ≤ 40 mm each, twisted, to three pads on the board's superior edge; each pad feeds its own 220 kΩ resistor and clamp within 10 mm (L4 §5.1) |
| Cleaning | 70 % isopropanol wipe after each wear; nothing on the skin side but titanium and nylon |
| Hook-tip variant | Ø7 × 4 mm foot at the hook end with the same stack in a lateral pocket, potted with silicone adhesive after assembly; lead in a 1.2 × 1.2 groove along the hook's medial side |

Sourcing is by specification; WP5 finds and verifies part numbers with
live pages before any purchase. L3's McMaster-Carr 93625A110 is an M8
stainless locknut (turn 02, finding 11) and is struck. Candidate routes,
all UNVERIFIED: McMaster-Carr titanium screws category (L3 source 9);
titanium fastener vendors selling ISO 7380 GR5 M2.5; ASTM F136 body-jewelry
disc tops as an alternative dome (L3 §5.1.3, post too thin for a lug).
Verification kit: dimethylglyoxime spot test (Nickel Alert, nonickel.com,
$24.99, listed unavailable on 2026-09-16; WP5 finds a substitute).

Nickel evidence, in order: (1) supplier material statement for the exact
lot or SKU; (2) DMG swab on every dome on receipt and after two weeks of
wear as a reject screen only; it does not prove absence (Thyssen 2010,
turn 02, finding 8). Every other metal part is inside the closed cavity or
potted.

## 5. Electronics envelope handoff and packing budget

The board is out of scope. The shell reserves the volumes below; WP6
produces the placement drawing at maximum part dimensions and either
confirms or raises interface v2. Until then 9.0 mm is a design value.

| Feature | Reserved |
|---|---|
| Cavity | s 1.5–38.2 × u 1.5–15.5 × y 1.5–8.0: 36.7 × 14.0 × 6.5 |
| Battery pocket | 16.0 × 10.8 × 6.0 at the top; cell body ≤ 5.2 × 10.4 × 15.6, PCM folded on the lateral face under Kapton, tabs toward the rib; 0.5 mm foam under the lid |
| Rib | 0.8 × 3.0, full width; leads pass over it |
| Board | one board 19.0 × 12.5 × 1.0, underside at y 4.3 on four pads, 0.75 side and 0.3 end clearance; retained by pads, lid, and a 0.5 foam strip over its superior 3 mm |
| Lateral side | Raytac MDBT50Q-1MV2 15.8 × 10.8 × 2.3 max, antenna end at the inferior board edge, ≥ 5 mm from the battery; height budget 4.3 + 1.0 + 2.3 = 7.6, lid underside 8.0 |
| Medial side | components ≤ 1.2 tall; two Ø7.1 keep-outs plus 0.5 copper-free margin at contact 1 and 2; the module's antenna no-copper zone overlaps keep-out 2 |
| Medial packing budget | board 237 mm²; minus keep-out 1 (49 on board), minus keep-out 2 ∪ antenna zone (≈ 68), minus 0.3 rim (≈ 15): ≈ 105 available. Required at max dims: ADS1292 TQFP-32 7 × 7 (49), three SOT-23 clamp arrays (30), charger DSBGA and LDO (7), about 25 passives 0402 (25): ≈ 111. Feasible only with tighter courtyards or a diode array; WP6 decides |
| Insulation | pre-resistor conductors: the three stacks (Kapton discs) and leads (silicone); board medial side solder-masked except the three pads |
| Debug and charge | charge pads on the board inside the cavity, reached with the lid off; Ø2 lead exit for tethered bring-up, plugged in Stage B |

If WP6 cannot pack the medial side, the options are, in order: a smaller
protection arrangement; +3.5 mm board zone (total length 51.9, REF_SITE
hook_tip for most ears); +3 mm width. That choice goes to Rolf.

## 6. Skin, safety, hygiene

Material: HP states its MJF PA12 meets USP Class I–VI and FDA intact-skin
guidance, based on preliminary testing of representative printed parts
(hp.com materials page, checked by `pro` 2026-09-16). That covers the
powder, not JLC's finishing or a dye, so order 1 is natural grey; black
only after a process statement exists. Skin side: PA12 and titanium only.
Cleaning: 70 % isopropanol wipe, air dry; no acetone. Wear progression is
in 3.7; observations are recorded as observations.

Battery-only: the shell has no connector and no port. Charging happens off
the ear with the lid removed, at the board's pads; the harness rule "never
charge while worn" is procedural and stated on the assembly sheet, because
no shell feature can enforce it. Tethered bring-up uses the lead exit with
the laptop on battery, and the plug goes back in before wear.

Series protection: each skin contact reaches the board only through its own
lead and its own resistor-plus-clamp; no pre-resistor conductor may touch
the battery, charge pads, or any other copper. The shell reserves the Kapton
discs, the solder-mask rule, and the lead route in §5. Active wear is gated
on a reviewed schematic, an assembled inspection, and a battery-powered
bench leakage check; an ordinary mains meter is not used on the body.

## 7. Orders

All figures are planning allowances dated 2026-09-16, not quotes. Sources:
JLC3DP ranges from L2 §1.1; DDP policy from jlcpcb.com/help/article/
us-tariff-policy-faq (updated 2026-09-09, verified by `pro`); the 40 %
plastics collection rate is from L2 and UNVERIFIED; destination shipping
ranges are from L2 and UNVERIFIED. No line exceeds $200.

### Order 1: fit gauge, provisional

| Line | Allowance |
|---|---|
| JLC3DP, MJF PA12-HP natural grey: 3 bodies, 2 lids, 1 coupon | $17–24 |
| Import collection at checkout, 40 % of parts (rate UNVERIFIED) | $7–10 |
| Shipping, Global Standard DDP 10–14 d (UNVERIFIED), or DHL DDP 3–5 d | $6–10, or $22–28 |
| Total | $30–44 standard; $46–62 DHL |
| Lead | 72 h build plus transit |
| Rework if WP6 changes thickness or width | one more gauge, about $20 |

What Rolf does, after approving both renders: download the five files from
`docs/fab/cad/v1/`; upload at jlcpcb.com/3d-printing; per file MJF,
PA12-HP, natural, quantities per the manifest; read the DFM warnings and
send any wall warning back to WP2; ship to Massachusetts on a DDP option.
Checkout gate: stop and report if any of these fail: parts and finish match
the manifest, a DDP or tariff line is shown, a delivered total is shown and
is at most $55 standard or $75 DHL, an expected delivery date is shown.
Record order number and total in `docs/fab/orders.md`.

### Order 2: Stage B shell and hardware

After 3.7 passes, WP6 confirms interface v2, and WP7 sets positions.

| Line | Allowance |
|---|---|
| JLC3DP, 2 Stage B bodies, 2 lids, DHL DDP, collection included | $38–49 |
| Titanium M2.5 × 4 ISO 7380 screws, one pack (SKU by WP5) | $20 |
| M2.5 thin nuts, ring lugs, Kapton discs, 28 AWG silicone wire | $20 |
| DMG nickel test kit (Nickel Alert $24.99, unavailable 2026-09-16, or substitute) | $25 |
| Hardware shipping, two suppliers (UNVERIFIED) | $15 |
| Massachusetts sales tax on hardware, 6.25 % | $5 |
| Total | $123–134; gate $160 |

Rolf: same upload steps; one cart per hardware supplier; DMG-swab every
dome on arrival; assemble per WP5's sheet; never charge worn.

## 8. Claims to verify before ordering

| # | Claim | Source | Status |
|---|---|---|---|
| 1 | JLC collects 40 % on 3D-printed plastics at checkout | L2 §2.2 | UNVERIFIED (rate table image failed, turn 02) |
| 2 | US orders ship DDP at JLC | tariff FAQ 2026-09-09 | verified by `pro` |
| 3 | PA12-HP price range $3.50–5.50 per shell | L2 §1.1; JLC page says "from $1.00" | not a quote; checkout closes it |
| 4 | Standard DDP $6–10, DHL $22–28 to Massachusetts | L2 §1.1 | UNVERIFIED |
| 5 | PA12-HP ±0.3 mm, 1 mm wall; snaps > 1.5; emboss 0.8; clearance 0.2–0.4 | JLC pages 2026-07-30 | verified by `pro` |
| 6 | HP MJF PA12 meets USP Class I–VI and intact-skin guidance, preliminary testing | hp.com materials page | verified by `pro`, scope limited |
| 7 | JLC finishing or dye is skin-tolerable | none | UNVERIFIED; grey default |
| 8 | A titanium ISO 7380 M2.5 × 4 with material evidence is purchasable | none yet | WP5 |
| 9 | ISO 7380 M2.5: dk 4.7, k 1.35; DIN 439 M2.5 nut 5 AF × 1.6 | standards tables | nobody yet |
| 10 | Ring lug 0.5 thick, OD ≤ 5.5, 26–28 AWG | catalog | WP5 |
| 11 | Raytac MDBT50Q-1MV2 15.5 × 10.5 × 2.05 nominal, toleranced, antenna keep-out | Raytac spec L | verified by `pro` |
| 12 | ADS1292 TQFP-32 5 × 5 body | TI datasheet rev C | verified by `pro` |
| 13 | 501015 cell 5.0 × 10 × 15, 50 mAh, PCM strip | L4 §1.4 | UNVERIFIED; WP6 names a cell |
| 14 | Hook preload 1.5 mm gives about 0.9 N | cantilever estimate | measured in WP4 |
| 15 | Palmiga prints conductive TPU on request | palmiga.com/3d-printing | verified by `pro`; job acceptance unknown |
| 16 | Dry-contact pressure window 10–25 kPa | L3 §7.2 | exploratory, no source |
| 17 | Nickel Alert $24.99, unavailable | nonickel.com | verified by `pro` |

## 9. Phase 1 work packages

One worker each, one to three days, in this order. WP1 precedes any
production-intent geometry; WP2 and WP3 deliver the order 1 files.

| WP | Owns | Inputs | Outputs | Acceptance |
|---|---|---|---|---|
| 1 Interface v1 | `docs/fab/interface.md` | §§3.3, 4, 5 | contact coordinates and stacks, keep-outs, cell envelope, board outline and heights, RF zone, insulation, packing budget | every dimension traced to a standard table, datasheet, or this plan; versioned |
| 2 Gauge script | `scripts/cad/`, `docs/fab/cad/v1/*.step .stl .3mf`, `manifest.json` | §3, interface v1 | five files, six parts | all §3.3 checks pass; regenerates identically from the manifest |
| 3 Renders, drawing | `docs/fab/cad/v1/render_*.png`, `drawing.pdf` | WP2 | two renders, one-page drawing | shows medial and lateral faces, closure section, M1–M8, ±0.3 general; phone-readable |
| 4 Rolf's sheets | `docs/fab/measure.md`, `order1.md`, `orders.md` | §§3.4, 3.7, 7 | measurement sheet with M1 first, checkout gate, order log, hook test (100 g at the tail tip, deflection recorded) | no step needs a question |
| 5 Contacts kit | `docs/fab/contacts.md` | §4 | verified SKUs with live pages and dates, material-evidence route, DMG protocol, assembly sheet, internal-metal isolation list | every price has a page and date; stack measured on catalog drawings ≤ 2.5 mm |
| 6 Packing proof | `docs/fab/interface.md` v2, placement drawing | §5, WP1 | placement at max dims, cell named, RF zone drawn | confirmed, or v2 with the escalation option for Rolf |
| 7 Montage and active gate | `docs/fab/montage.md` | §2 row 8, L3 §2.2, Stage A bench | gel-electrode montage protocol; bench force, travel, continuity test of the real stack; active gate: baseline, SNR, dropout under jaw motion, three-day re-donning at a fixed threshold | blocked until Stage A parts exist; ends with three coordinates and pass criteria |
| 8 Stage B shell | `scripts/cad/` variant, `docs/fab/cad/v2/` | 3.7 results, interface v2, WP7 | order 2 files | §3.3 checks; positions from WP7; wear only after the WP7 gate passes |
| 9 Design record | `docs/EARPIECE_DESIGN.md` | signed-off plan | record updated | each §2 decision appears once |

Interface rule: any change to contact coordinates, stack height, cell,
board outline, or thickness bumps the interface version, re-runs WP2's
checks, and repeats any 3.7 item whose input changed; a changed gauge is a
reprint, not an inherited pass.

## 10. Open items, interface decisions, Open for Rolf

Open items (single-package, carried):

1. CREASE_BOW from M1 and M2: WP2 writes the arc–chord formula, clamps
   1–8 mm, and reports it.
2. Coupon feature list and how each result maps to a parameter: WP2.
3. Manifest schema and hash rule: WP3.

Interface decisions pending (cross-package, decided at interface v2):

1. Medial-side packing: fits, or +3.5 mm length, or +3 mm width (WP6).
2. Cell identity and maximum dimensions (WP6).
3. Hook stiffness measured versus estimate; HOOK_DIA if outside 0.5–1.5 N
   (WP4 measures, WP6 decides).
4. Contact size M2.5 versus M3 after WP7 (WP7 recommends, WP8 applies).

Open for Rolf:

1. Measure M1 first. Below 52 mm the reference moves to the hook tip; below
   41 mm this layout does not fit and the plan comes back.
2. The other seven measurements, or "defaults" for a REF gauge.
3. Which ear first (default right).
4. Approve the renders, then place order 1 under the checkout gate.
5. After 3.7: which thickness and preload he accepts, and whether the back
   view is acceptable.
6. If WP6 escalates: longer, wider, or a smaller front end.
7. Black nylon later, only with a finishing statement; grey until then.
8. Buy the Stage A parts (`docs/STAGE_A_PARTS.md`); WP7 and order 2 wait
   on them.
9. Any change to the nickel-free requirement is his to make, outside this
   plan.
