# Elicio earpiece — fabrication plan

Phase 0 synthesis and Phase 1 specification for the Stage B behind-the-ear
shell. Revision 3, turn 05, 2026-09-16. Author `fable`, reviewer `pro`.
Inputs: `docs/fab/brief.md`, `docs/EARPIECE_DESIGN.md`, lane reports L1–L4
in `docs/fab/`, and `tasks/plan/turns/02-pro.md`, `04-pro.md`. Lane reports
are evidence, not law; section 2 picks and says why. Nothing here buys
anything.

**For Rolf, in short.** A Python-scripted nylon shell from eight caliper
numbers, printed by JLCPCB with duties prepaid. Order 1 is a passive fit
gauge, about $40, testing your ear, not the electronics. Measure M1 (ear
root length) first: this release needs 51 mm or more. Contacts are three
titanium domes; no stainless, because the brief says nickel-free. Nothing
is ordered until you approve the renders.

## 1. Decision summary

1. Tool: build123d, headless, native STEP; `scripts/cad/bte_fit_shell.py`.
2. Geometry: no scan, no impression; a generic shell from L1's M1–M7 plus M8
   (helix rise), each with a published default; a defaults-only build is a
   provisional gauge, not a personal fit. This release supports one layout:
   reference contact on a tail, M1 ≥ 51.
3. Vendor: JLC3DP, HP MJF PA12-HP, natural grey, DDP. Resin never touches
   skin.
4. Contacts: three titanium ISO 7380 M2.5 button heads (4.7 mm domes),
   rigidly mounted through a 1.5 mm wall with a ring lug and thin nut inside;
   hook preload supplies clamping. No stainless fallback.
5. Envelope: cavity 36.7 × 14.0 × 6.5 mm; battery (501015, 50 mAh) at the top,
   a 19 × 12.5 mm board zone at the bottom over the two signal contacts;
   reference in a 10.2 mm tail. Body arc 48.4 (chord 47.9) × 17.0 × 9.0 mm
   plus hook, with a 7.0 mm thin gauge. Design values pending WP6.
6. Order 1: gauge set, provisional, allowance $30–44 standard shipping.
7. Order 2: two Stage B bodies plus verified titanium hardware and a nickel
   test kit, allowance about $130, after the release gates in §9.
8. No agent purchases, uploads, quotes, or contacts anyone.

## 2. Conflicts resolved

| # | Topic | Lanes said | Pick | Why |
|---|---|---|---|---|
| 1 | Battery | L2 assumed 110 mAh; L4 picked 501015 50 mAh over 401030 100 mAh | 501015 | 7 h streaming covers a session; a 30 mm cell forces stacking past 10 mm; 110 was a pricing box |
| 2 | Envelope | L4 33 × 10.5 × 6.8; L2 35 × 20 × 12; L1 34–38 × 7.5–8.2 × 8.5–10 | 48.4 × 17 × 9.0, derived in §5 | L4's 16 × 9.5 islands cannot carry a 15.5 × 10.5 module; L2's box was for quoting; L1 assumes no contact hardware |
| 3 | Contact metal | L3 Ti or 316L; L2 316L or gold-plated; L4 316L | Titanium only | Brief and design record say nickel-free; 316L is 10–14 % Ni; gold flash over nickel wears through. Changing the requirement is Rolf's, outside this plan |
| 4 | Contact size | L1 3 mm; L2 4 mm; L3 7–9 mm, concrete part M3 | ISO 7380 M2.5, 4.7 mm dome; other sizes are an interface v2 change | L3's 0.3–0.4 N over 7 mm is 8–10 kPa, under its own window; over 4.7 mm it is 17–23 kPa; every millimetre of nut keep-out costs body length; pressure numbers are exploratory |
| 5 | Conductive TPU | Design record cites Palmiga; L2/L3 say bureaus do not print it | Titanium primary; Palmiga's service a conditional alternative | Palmiga prints conductive TPU (turn 02, finding 12). Titanium wins on assembly, small area, no third supplier |
| 6 | Lid closure | L2 heat-set inserts; L1 PA12 snaps | External snap lip at the top, tongue with web at the tail tip, two nubs; tape as the passive fallback | Nothing inside the cavity; the first lid is the snap test article (§3.6) |
| 7 | Gauge material | L2 resin; L1 either | MJF PA12 | Hours on skin; same material as order 2 |
| 8 | Montage | L3 horizontal PAM pair, reference at the mastoid tip; L1/L4 narrow pod | Pair at 22° off the body axis, 12 mm pitch; reference on the tail over the mastoid surface; WP7a fixes positions | A 17 mm face cannot hold a horizontal pair; the mastoid tip is beyond any BTE body |
| 9 | Contact count | L4 asks 5; design record and L3 say 3 | 3 | Clench is 3–5× a flex on the same pair |
| 10 | Suspension | L3 floating stud plus foam; L4 shell preload only | Rigid mount, hook preload 1.5 mm | A floating stack does not fit under the board (turn 02, finding 4); measured at the active gate |
| 11 | Ear capture | L1 putty impression versus generic | Generic gauge; impression at Stage C | Gauge costs $40 and tests the real ear |
| 12 | Shipping | L2 standard DDP versus DHL | Standard for order 1, DHL for order 2 | Order 1 is not on the critical path |
| 13 | Shells and PCB in one parcel | L2 Q5 | Separate | Different tariff lines |
| 14 | Hook | L4 flexible TPU; L1 nylon | PA12, one piece | One material; preload measured in WP4 |
| 15 | Gasket | L1 Q4 | None | Prototype |
| 16 | Charging | L4 skin-side pads | No port; pads inside the closed cavity, lid off to charge | Pad placement is not an interlock (turn 02, finding 10) |
| 17 | Short ears | Turn 04 finding 16: specify the hook-tip branch or reject | Reject M1 < 51 in this release | A second branch needs its own schedule and closure; it is an interface v2 item, not a silent shrink |

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

### 3.2 Frames and path

Shell frame: origin O at the hook root reference on the top face of the
body; X posterior, Y lateral, Z superior. The hook and the final assembly
live here; the skull is the plane Y = 0 when the hook rests on the ear.

Body frame: the shell frame rotated about the X axis through O by −θ,
θ = atan(HOOK_PRELOAD / TOTAL_CHORD), 1.79° at defaults, so the tail tip
sits HOOK_PRELOAD medial of Y = 0. Body, tail, cavity, pockets, rib, pads,
holes, lid features, and the lid are built in the body frame, where the
medial face is the plane y = 0 and every contact axis is −y, then moved
into the shell frame as one group; the lid gets the identical transform.

Path: a circular arc in the body frame's XZ plane through O, bowing
posteriorly by CREASE_BOW at mid-length, with arc length BODY_ARC. The
script solves the chord numerically (R = C²/8b + b/2, arc = 4R·atan(2b/C));
at defaults the chord is 47.9. `s` is arc length from O and runs 0 to
BODY_ARC; the path is extended tangentially 2 mm beyond O for features at
negative s. `u` is offset along the in-plane normal, posterior; `y` is
lateral height. `P(u, s, y)` maps to body-frame points; every placement
uses it. TOTAL_CHORD is the straight line from O to the tail tip (47.9);
it is what M1, the straight ear-root length, is compared with.

### 3.3 Parameters (defaults are the reference-ear build)

Supported generation matrix: VARIANT ∈ {full, thin} × HOOK_PRELOAD ∈
{1.5, 2.5}, tail reference, M2.5 hardware. Anything else fails before
export. Numbers below are for the full body; thin values follow from
BODY_THICK where a formula is given.

| Parameter | Default | Unit | From | Note |
|---|---|---|---|---|
| SIDE | right | – | Rolf | |
| VARIANT | full | – | – | full 9.0, thin 7.0 |
| BODY_ARC | 48.4 | mm | – | arc length O to tail tip; chord 47.9 derived |
| BODY_WIDTH | 17.0 | mm | – | set by contents |
| BODY_THICK | 9.0 / 7.0 | mm | – | |
| CREASE_BOW | 3.0 | mm | M1, M2 | from arc–chord when both measured, clamped 1–8 |
| WALL_MEDIAL, WALL_SIDE, WALL_END | 1.5 | mm | – | |
| LID_THICK | 1.0 | mm | – | lid underside at LID_Y = BODY_THICK − 1.0 (8.0 / 6.0) |
| CLEAR_FIT | 0.4 | mm | – | nominal mating clearance; policy in 3.6 |
| CAVITY | s 1.5–38.2, u 1.5–15.5, y 1.5 to LID_Y | mm | – | swept along the path |
| BATTERY_POCKET | s 1.5–17.5, u 3.1–13.9, y 1.5–7.5 | mm | – | cell max 5.2 × 10.4 × 15.6, PCM folded on the face |
| RIB | s 17.5–18.3, y 1.5–4.5 | mm | – | full width; exception E2 |
| BOARD_ZONE | s 18.3–37.9, u 1.5–15.5 | mm | – | pads 1.5 × 1.5, y 1.5–4.3, at the corners |
| TAIL | s 38.2–48.4, width 17 → 10 linear, tip round 4.0 | mm | – | full thickness, then recessed under the lid |
| LID_RECESS | s 0–46.8 within the lid's plan outline, y above LID_Y removed | mm | – | lowers wall tops and the tail's lateral face to LID_Y |
| CONTACT_DOME | 4.7 dia, 1.35 crown | mm | – | ISO 7380 M2.5 |
| CONTACT_HOLE | 2.9 through the medial wall | mm | – | |
| CONTACT_STACK | 2.5 above the floor plus 0.13 Kapton | mm | – | lug 0.5, nut 1.6, tip 0.4; top at y 4.13 |
| KEEPOUT | Ø7.1, y 1.5–4.13, plus LUG_TAB 3 × 7 × 1.5 from the centre toward its pad | mm | – | checked only when MOCK_CONTACTS is false |
| CONTACT_1 | u 5.9, s 22.0 | mm | – | keep-out clears rib and wall |
| CONTACT_PITCH | 12.0 | mm | – | L3 12–15 |
| PAIR_ANGLE | 22 | deg | – | contact 2 = contact 1 + pitch × (sin, +cos): u 10.4, s 33.1 |
| CONTACT_REF | u 8.5, s 43.0 | mm | M6 recorded | pocket Ø7.5 from LID_Y down to y 1.5; end wall 1.05 to the cavity |
| LEAD_CHANNEL | u 7.75–9.25, y 2.5–4.0, s 38.2–39.25 | mm | – | through the inferior end wall, floor kept |
| LEAD_PADS | medial side of the board, outside keep-outs + 0.5 and the antenna zone; suggested (u, s) 5.9/26.5, 5.5/30.0, 4.0/29.0 | mm | – | reference lead 15 mm, all ≤ 40 |
| CABLE_EXIT | Ø2.0 through the posterior side wall at s 36, y 3 | mm | – | tethered bring-up; plugged in Stage B |
| HOOK_ROOT | X 4.0, Y = M4/2 (3.0), Z 0 | mm | M4 | on the top face, shell frame |
| HOOK_RADIUS | M8 + HOOK_DIA/2 + 1.0 (13.5) | mm | M8 | centre-line |
| HOOK_ANGLE | 145 | deg | – | arc from −5° (inside the body) to 145° |
| HOOK_DIA | 3.5 | mm | – | |
| HOOK_PRELOAD | 1.5 | mm | – | variants 1.5 and 2.5 |
| GLASSES_FLAT | 0.8 if M5 > 0, else no cut | mm | M5 | hook lateral-superior side, 30°–120° |
| LID_LIP | u 8–14, 1.0 thick, 5.5 long, bump 0.5 out × 0.6 tall at the tip | mm | – | external; exception E5 |
| LIP_GROOVE | s 0–0.5 into the top face, u 7.5–14.5, y LID_Y − 4.7 to LID_Y − 3.7 | mm | – | 3.3–4.3 full |
| TONGUE_SLOT | s 46.8–48.4, u 5–12, y LID_Y − 1.0 to LID_Y − 0.1; web pocket s 45.4–46.8, same u and y, open above | mm | – | 1.1 mm lip left above the slot |
| LID_TONGUE | web s 45.6–46.4 × y LID_Y − 0.8 to LID_Y; tongue s 46.4–48.0 × y LID_Y − 0.8 to − 0.3; both 6 wide | mm | – | exception E1; one solid with the plate |
| LID_NUBS | 0.8 cubes at s 17.5–18.3, u 1.9–2.7 and 14.3–15.1, y LID_Y − 0.8 to LID_Y | mm | – | exception E3 |
| EMBOSS | 0.8 | mm | – | `ELICIO V1 R FULL P15 REF` inside the lid |
| MOCK_CONTACTS | true | – | – | gauge prints domes; Stage B cuts holes, pocket, channel |
| FILLET_MEDIAL, LID_EDGE | 1.5, 0.8 | mm | – | |
| MESH | chord 0.02, angle 5° | – | – | STL export |

Reference-ear values for any key Rolf leaves out: M1 52, M2 58, M3 11,
M4 6.0, M5 2.5, M6 15, M7 22, M8 11.

Checks the script prints. Design checks, fail on any: generation matrix;
one connected solid per part; walls ≥ 1.0 except exceptions E1–E5 at their
own minimum (3.6); body and lid interiors disjoint in the seated state at
nominal; keep-outs and the lead channel contain only air and the channel
joins pocket to cavity (Stage B builds only); contact axes −y; STLs
watertight; regeneration identical. Reported, not failed: adverse-tolerance
interference per 3.6; SPAN = BODY_THICK + crown = 10.35 versus M3 as pinna
displacement. Ear checks, fail: TOTAL_CHORD > M1 − 3 (at defaults M1 below
50.9; the plan quotes 51); HOOK_RADIUS − HOOK_DIA/2 < M8 + 1.

### 3.4 Caliper protocol for Rolf

Digital caliper and string, ten minutes. Any key left out takes the
reference value and the build is marked REF.

| No. | Measure | How | Typical | Feeds |
|---|---|---|---|---|
| M1 | Ear root length | Top attachment to bottom attachment, straight | 45–58 | length gate; measure first |
| M2 | Crease arc | String along the crease, same endpoints | 50–65 | CREASE_BOW |
| M3 | Sulcus clearance | Depth rod, skull to helix rim at mid-height | 8–14 | span report |
| M4 | Helix root thickness | Jaws across the top cartilage bridge, no squeeze | 4.5–7.5 | HOOK_ROOT Y |
| M5 | Glasses temple thickness | Jaws on the temple at the ear, 0 if none | 1.8–3.2 | GLASSES_FLAT |
| M6 | Mastoid offset | Crease to the bony bump behind the lower ear | 12–18 | recorded for WP7a |
| M7 | Crease top to mid-concha | Along the crease to the canal-opening level | 18–26 | recorded for WP7a |
| M8 | Helix rise | Top attachment up to the ear rim's highest point | 8–14 | HOOK_RADIUS |

### 3.5 Construction, in order (body frame unless stated)

1. Path per 3.2, extended 2 mm before O. Define `P(u, s, y)`.
2. Body: sweep the section (u 0–17, y 0–BODY_THICK, medial corners
   FILLET_MEDIAL, lateral corners sharp) along s 0–38.2, binormal fixed to
   Y. Tail: sweep s 38.2–48.4 with width tapering 17 → 10, same thickness;
   round the tip 4.0. Union. The medial face is y = 0.
3. Lid recess: remove everything above LID_Y over s 0–46.8 across the full
   plan outline. Wall tops and the tail's lateral face now sit at LID_Y; the
   lip zone s 46.8–48.4 keeps full thickness.
4. Cavity: sweep the rectangle (u 1.5–15.5, y 1.5–BODY_THICK) along
   s 1.5–38.2 and subtract. Add the rib and the four pads. The battery
   pocket is the space above the rib. Flat parts see the plan-view bow,
   0.32 mm over 16 mm and 0.46 over 19 mm, absorbed by width clearance.
5. Contacts. If MOCK_CONTACTS: at P(5.9, 22.0, 0), P(10.4, 33.1, 0),
   P(8.5, 43.0, 0) add spherical caps Ø4.7, height 1.35, standing to −y;
   nothing else. Else: cut Ø2.9 through the wall at each; cut the reference
   pocket Ø7.5 from LID_Y down to y 1.5 at P(8.5, 43.0); cut LEAD_CHANNEL
   through the inferior end wall, floor intact; cut CABLE_EXIT.
6. Lid features on the body: LIP_GROOVE 0.5 into the top face; TONGUE_SLOT
   under the 1.1 mm lip at the tip, with the web pocket open above it.
7. Lid: plate y LID_Y to LID_Y + 1.0 over s −0.2 to 46.4, the body's plan
   outline inset CLEAR_FIT, edge fillet 0.8. Lip: tab u 8–14, 1.0 thick,
   hanging 5.5 from the plate's top edge at s −1.2 to −0.2, bump 0.5 toward
   +s over its lowest 0.6, root fillet 0.5. Web: s 45.6–46.4, y LID_Y − 0.8
   to LID_Y, 6 wide, joined to the plate's inferior end. Tongue: s 46.4–48.0,
   y LID_Y − 0.8 to LID_Y − 0.3, 6 wide, joined to the web. Nubs per 3.3.
   Emboss inside. Plate, lip, web, tongue, nubs are one solid.
8. Hook (shell frame): circle HOOK_DIA swept along the arc of radius
   HOOK_RADIUS centred (HOOK_ROOT.X − HOOK_RADIUS, HOOK_ROOT.Y, 0) in the
   plane Y = HOOK_ROOT.Y, angle 0 at HOOK_ROOT with tangent +Z, increasing
   toward −X, from −5° to HOOK_ANGLE. If M5 > 0, cut GLASSES_FLAT off the
   lateral-superior side between 30° and 120°. Defaults: centre (−9.5, 3, 0),
   radius 13.5.
9. Assembly: rotate the body group and the lid from the body frame into the
   shell frame by −θ about X through O; union hook and body; fillet the
   joint 2.0. Left side: mirror all outputs across X = 0.
10. Run the checks in 3.3; export; write `manifest.json` (parameters, which
    were defaults, exceptions E1–E5 present, adverse-interference report,
    commit, hashes, part quantities).

Closing: top end raised, slide +s so the tongue enters under the lip,
lower the top, and the bump rides over the top edge into the groove
(deflection 0.3, strain 1.5 %). Opening: fingernail under the lip, pull −s
0.3, lift, slide −s. Seated, the interiors are disjoint: plate on the
recess, web and tongue in their pockets, nubs and lip in air.

### 3.6 Print rules, acceptance policy, outputs

JLC3DP MJF PA12-HP, pages checked by `pro` on 2026-09-16
(jlc3dp.com/help/article/pa12-hp-nylon, 2026-07-30;
jlc3dp.com/help/article/3d-printing-design-guideline, 2026-08-24):
tolerance ±0.3 mm under 100 mm; wall 1 mm; over 1.5 mm recommended for
protrusions, locating features, snaps, and fasteners; emboss 0.8;
assembly clearance 0.2–0.4.

One policy. Walls (enclosing walls, floor, end walls, lip zone, tail, hook)
≥ 1.0, a fail. Experimental exceptions, each with its own minimum, listed
in the manifest and on the drawing: E1 tongue 0.5 (≥ 0.4 after fitting);
E2 rib 0.8 (locating only); E3 nubs 0.8 (≥ 0.6); E4 coupon rib 0.4
(measurement feature); E5 lip cantilever 1.0 with a 0.5 bump (≥ 0.2 after
fitting), below JLC's 1.5 recommendation on purpose. Order 1 may use all
five. Order 2 keeps E1, E3, E5 only if the order 1 lid passes the closure
test; otherwise interface v2 replaces the closure. Tolerance: every mating
pair has 0.4 nominal clearance, a fail if less; the as-printed range is
−0.2 to +1.0; interference up to 0.2 at the adverse limit is permitted and
reported, not failed. Material may be removed by hand only from the lid's
tongue, web, nubs, and lip bump, never from the body, down to the minima
above. Final assembled acceptance is 3.7 item 7. Any unintended nominal
overlap is a fail.

Closure test article: the first lid on the first full body, ten cycles,
then retained through 3.7 item 2 with the 4 g load. The coupon, a
12 × 12 × 3 block with holes Ø1.7, 2.9, 3.4, slots 0.9 and 0.4, and a 0.4
rib, measures the process only and feeds interface v2. Passive fallback if
the lip fails: two wraps of paper medical tape around body and lid at s 10
and s 40 for the remaining gauge items, recorded as such.

Outputs in `docs/fab/cad/v1/`: `body_full_p15`, `body_thin_p15`,
`body_full_p25`, `lid`, `coupon`, each `.step`, `.stl`, `.3mf`;
`render_medial.png`, `render_lateral.png`; `drawing.pdf` (side, medial,
closure section, M1–M8, exceptions, ±0.3 general); `manifest.json`. Order
manifest: body files ×1 each, lid ×2, coupon ×1: six parts, five files.

### 3.7 Passive fit acceptance

The gauge is provisional: it checks ear, comfort, covertness, and closure,
not electronics fit (WP6) or dry-contact signal (WP7). Put about 4 g in the cavity (two M6 nuts). Order: full/1.5,
thin/1.5, full/2.5.

1. On and off one-handed in under five seconds without pulling the ear.
2. Stays put through ten head shakes, five hard clenches, three yawns, one
   flight of stairs.
3. Wear 15 minutes, inspect the skin; then one hour; then four hours.
   Remove at once on pain, numbness, or any skin reaction, and record it. A
   red mark lasting over 15 minutes after removal fails that variant.
4. Photos: front, side, back, with and without glasses. Front: nothing
   visible. Side: no more than a hearing aid shows. Back: his call.
5. Paper strip under each dome is pinched with the head left, right, and
   chin down.
6. Glasses on and off ten times; no lift.
7. Closure: lid on and off ten times; lip, web, tongue, nubs intact;
   retained through item 2 weighted. Fail: tape fallback for the rest,
   recorded.
8. Which thickness and preload he accepts; observations, not
   biocompatibility evidence.
9. Mark the dome positions on the skin, photograph; input to WP7a.

## 4. Contacts specification

Three contacts: two signal on the body's medial face, one reference on the
tail. Final positions come from WP7a.

| Item | Spec |
|---|---|
| Material | Titanium, Grade 2 (ASTM F67) or Grade 5 (ASTM F1472/F136), bought with the supplier's material statement or mill certificate on file. No plating. Nickel content is what the supplier's specification states, not "zero" |
| Geometry | ISO 7380 M2.5 × 4 button head: dome Ø4.7, crown 1.35, 1.5 mm hex socket. Rigid mount through the 1.5 mm wall |
| Inside stack | ring lug (#4 or M2.5, crimped to 28 AWG silicone wire, 26–28 AWG barrel) 0.5, DIN 439 M2.5 thin nut 1.6, screw tip 0.4, Kapton disc 0.13 on top: 2.63 above the floor. Nut and lug may be plated steel or tinned copper; they sit under the lid and never see skin |
| Clamping | hook preload 1.5 mm, about 0.9 N total by estimate, measured in WP4. Nominal 0.3 N per contact over 17 mm² is 17 kPa. Exploratory targets, not comfort or performance bounds |
| Leads | ≤ 40 mm each, twisted, to the three medial-side pads in §5; each pad feeds its own 220 kΩ resistor and clamp within 10 mm (L4 §5.1) |
| Cleaning | 70 % isopropanol wipe after each wear; nothing on the skin side but titanium and nylon |

Sourcing is by specification; WP5 verifies part numbers with live pages
before any purchase. L3's McMaster-Carr 93625A110 is an M8 stainless
locknut (turn 02, finding 11), struck. Routes, UNVERIFIED: McMaster-Carr's
titanium screw category; ISO 7380 GR5 M2.5 from titanium fastener vendors.
Kit: dimethylglyoxime spot test (Nickel Alert, nonickel.com, $24.99,
unavailable 2026-09-16; WP5 finds a substitute).

Nickel evidence, in order: (1) supplier material statement for the exact
SKU or lot; (2) DMG swab on every dome on receipt and after two weeks of
wear, a reject screen only, not proof of absence (Thyssen 2010, turn 02,
finding 8). Every other metal part is inside the closed cavity.

## 5. Electronics envelope handoff and packing budget

The board is out of scope. The shell reserves the volumes below; WP6
produces the placement drawing at maximum part dimensions and either
confirms or raises interface v2. Until then 9.0 mm is a design value.

| Feature | Reserved |
|---|---|
| Cavity | s 1.5–38.2 × u 1.5–15.5 × y 1.5–8.0: 36.7 × 14.0 × 6.5 |
| Battery pocket | 16.0 × 10.8 × 6.0 at the top; cell body ≤ 5.2 × 10.4 × 15.6, PCM folded on the lateral face under Kapton, tabs toward the rib; 0.5 foam under the lid |
| Rib | 0.8 × 3.0, full width; battery leads pass over it |
| Board | 19.0 × 12.5 × 1.0, underside at y 4.3 on four pads, 0.75 side and 0.3 end clearance; retained by pads, lid, and a 0.5 foam strip over its superior 3 mm |
| Lateral side | Raytac MDBT50Q-1MV2 15.8 × 10.8 × 2.3 max, antenna end at the inferior board edge, ≥ 5 mm from the battery; 4.3 + 1.0 + 2.3 = 7.6 under a lid at 8.0 |
| Medial side | components ≤ 1.2 tall; keep-outs Ø7.1 plus lug tabs plus 0.5 copper-free margin at contacts 1 and 2; the antenna no-copper zone overlaps keep-out 2; three lead pads at the §3.3 positions |
| Packing budget | 237 mm² minus keep-out 1 on board (49), minus keep-out 2 ∪ antenna zone (≈ 68), minus rim (≈ 15): ≈ 105 available. Required at max dims: ADS1292 TQFP-32 7 × 7 (49), three SOT-23 clamps (30), charger and LDO (7), about 25 passives 0402 (25): ≈ 111. Feasible only with tighter courtyards or a diode array; WP6 decides |
| Reference route | tail pocket Ø7.5 → LEAD_CHANNEL (u 7.75–9.25, y 2.5–4.0) through the 1.05 end wall → under the board at y 2.5–4.0 → pad at (4.0, 29.0); 15 mm; one Kapton wrap to the floor at s 37 as strain relief; clear of battery, charge pads, and the lid |
| Insulation | pre-resistor conductors: the three stacks under Kapton, lug tabs on the floor, silicone leads; board medial side solder-masked except the three pads |
| Debug and charge | charge pads on the board inside the cavity, reached with the lid off; Ø2 exit in the posterior side wall for tethered bring-up, plugged in Stage B |

If WP6 cannot pack the medial side: a smaller protection arrangement,
+3.5 mm board zone (raises the M1 gate), or +3 mm width; Rolf chooses.

## 6. Skin, safety, hygiene

Material: HP states its MJF PA12 meets USP Class I–VI and FDA intact-skin
guidance, based on preliminary testing of representative printed parts
(hp.com materials page, checked by `pro` 2026-09-16). That covers the powder, not JLC's finishing or dye, so order 1 is
natural grey; black only after a process statement exists. Skin side: PA12
and titanium. Cleaning: 70 % isopropanol, air dry; no acetone.

Battery-only: no connector, no port. Charging happens off the ear with
the lid removed; "never charge while worn" is procedural, on the assembly
sheet, because no shell feature enforces it. Tethered bring-up uses the side exit with the laptop on
battery; the plug goes back in before wear.

Series protection: each skin contact reaches the board only through its own
lead and its own resistor plus clamp; no pre-resistor conductor may touch
the battery, charge pads, or other copper. The shell reserves the Kapton
discs, the lug-tab and channel volumes, the solder-mask rule, and the lead
route in §5. Active wear follows the release states in §9: reviewed
schematic, assembled inspection, and a battery-powered bench leakage and
continuity check; no mains meter on the body.

## 7. Orders

Planning allowances dated 2026-09-16, not quotes. JLC3DP ranges from L2
§1.1; DDP policy from jlcpcb.com/help/article/us-tariff-policy-faq
(2026-09-09, verified by `pro`); the 40 % plastics collection rate and the
destination shipping ranges are from L2 and UNVERIFIED. No line exceeds
$200.

### Order 1: fit gauge, provisional

| Line | Allowance |
|---|---|
| JLC3DP MJF PA12-HP natural grey: 3 bodies, 2 lids, 1 coupon | $17–24 |
| Import collection at checkout, 40 % of parts (UNVERIFIED) | $7–10 |
| Global Standard DDP 10–14 d (UNVERIFIED), or DHL DDP 3–5 d | $6–10, or $22–28 |
| Total | $30–44 standard; $46–62 DHL |
| Rework if WP6 changes thickness or width | one more gauge, about $20 |

Rolf, after approving both renders: download the five files from
`docs/fab/cad/v1/`; upload at jlcpcb.com/3d-printing; per file MJF,
PA12-HP, natural, quantities per the manifest; send any DFM wall warning
back to WP2; ship to Massachusetts on a DDP option. Checkout gate, stop on
any miss: parts and finish match the manifest; a DDP or tariff line is
shown; the delivered total is shown and at most $55 standard or $75 DHL; a
delivery date is shown. Record order number and total in
`docs/fab/orders.md`.

### Order 2: Stage B shell and hardware

Placed only at release state S1 (§9).

| Line | Allowance |
|---|---|
| JLC3DP, 2 Stage B bodies, 2 lids, DHL DDP, collection included | $38–49 |
| Titanium M2.5 × 4 ISO 7380 screws, one pack (SKU by WP5) | $20 |
| M2.5 thin nuts, ring lugs, Kapton, 28 AWG silicone wire | $20 |
| DMG nickel test kit (Nickel Alert $24.99, unavailable 2026-09-16, or substitute) | $25 |
| Hardware shipping, two suppliers (UNVERIFIED) | $15 |
| Massachusetts sales tax on hardware, 6.25 % | $5 |
| Total | $123–134; gate $160 |

## 8. Claims to verify before ordering

| # | Claim | Source | Status |
|---|---|---|---|
| 1 | JLC collects 40 % on printed plastics at checkout | L2 §2.2 | UNVERIFIED |
| 2 | US orders ship DDP at JLC | tariff FAQ 2026-09-09 | verified by `pro` |
| 3 | PA12-HP $3.50–5.50 per shell | L2; JLC page "from $1.00" | not a quote; checkout closes it |
| 4 | Standard DDP $6–10, DHL $22–28 to Massachusetts | L2 §1.1 | UNVERIFIED |
| 5 | PA12-HP ±0.3, 1 mm wall; > 1.5 for snaps; emboss 0.8; clearance 0.2–0.4 | JLC pages 2026-07-30, 2026-08-24 | verified by `pro` |
| 6 | HP MJF PA12: USP Class I–VI, intact-skin guidance, preliminary testing | hp.com | verified by `pro`, scope limited |
| 7 | JLC finishing or dye is skin-tolerable | none | UNVERIFIED; grey default |
| 8 | A titanium ISO 7380 M2.5 × 4 with material evidence is purchasable | none yet | WP5 |
| 9 | ISO 7380 M2.5 dk 4.7, k 1.35; DIN 439 M2.5 nut 5 AF × 1.6; #4 ring lug 0.5 thick, tab ≤ 7 | standards and catalog tables | WP5 |
| 10 | Raytac MDBT50Q-1MV2 15.5 × 10.5 × 2.05, toleranced, antenna keep-out | Raytac spec L | verified by `pro` |
| 11 | ADS1292 TQFP-32 5 × 5 body | TI datasheet rev C | verified by `pro` |
| 12 | 501015 cell 5.0 × 10 × 15, 50 mAh, PCM strip | L4 §1.4 | UNVERIFIED; WP6 names a cell |
| 13 | Hook preload 1.5 mm gives about 0.9 N | cantilever estimate | measured in WP4 |
| 14 | Palmiga prints conductive TPU on request | palmiga.com/3d-printing | verified by `pro`; job acceptance unknown |
| 15 | Dry-contact pressure window 10–25 kPa | L3 §7.2 | exploratory, no source |
| 16 | Nickel Alert $24.99, unavailable | nonickel.com | verified by `pro` |

## 9. Phase 1 work packages and release states

One worker each, one to three days, in this order. WP1 precedes any
production-intent geometry; WP2 and WP3 deliver the order 1 files.

| WP | Owns | Outputs | Acceptance |
|---|---|---|---|
| 1 Interface v1 | `docs/fab/interface.md` | contact coordinates and stacks, keep-outs, lead route, cell envelope, board outline and heights, RF zone, insulation, packing budget | every dimension traced to a standard, datasheet, or this plan; versioned |
| 2 Gauge script | `scripts/cad/`, `docs/fab/cad/v1/*`, `manifest.json` | five files, six parts | all §3.3 checks; exceptions and interference in the manifest; identical regeneration |
| 3 Renders, drawing | `render_*.png`, `drawing.pdf` | two renders, one page | medial and lateral faces, closure section, M1–M8, E1–E5, ±0.3 general |
| 4 Rolf's sheets | `docs/fab/measure.md`, `order1.md`, `orders.md` | M1-first measurement sheet, checkout gate, order log, hook test (100 g at the tail tip) | no step needs a question |
| 5 Contacts kit | `docs/fab/contacts.md` | verified SKUs with pages and dates, material-evidence route, DMG protocol, assembly sheet, internal-metal list | every price has a page and date; stack ≤ 2.63 on catalog drawings |
| 6 Packing proof | `interface.md` v2, placement drawing | placement at max dims, cell named, RF zone, lead pads | confirmed, or v2 with the escalation for Rolf |
| 7a Montage and protocol | `docs/fab/montage.md` | gel-electrode montage on the Stage A bench at the plan's positions versus L3's pair; three coordinates; frozen dry-test protocol with numeric pass criteria for baseline, SNR, dropout under jaw motion, three-day fixed-threshold re-donning, and eating, talking, walking false-positive rates | blocked until Stage A parts exist; criteria frozen before any dry data |
| 7b Validation | `docs/fab/validation.md` | bench force, travel, continuity of the real stack; controlled validation wear per 7a; results | pass or fail against 7a's criteria only |
| 8 Stage B shell | `scripts/cad/` variant, `docs/fab/cad/v2/` | order 2 files | §3.3 checks; positions from 7a; E1/E3/E5 only if the closure test passed |
| 9 Design record | `docs/EARPIECE_DESIGN.md` | record updated | each §2 decision appears once |

Release states:

| State | Allowed | Entry requires |
|---|---|---|
| S0 gauge | passive wear per 3.7 | Rolf's approval of renders; order 1 gate |
| S1 order 2 | purchase of shells and hardware | WP5 verified spec; interface v2 accepted; 7a coordinates and frozen protocol; 3.7 items re-run for any changed input; closure test result |
| S2 assembled | bench only | reviewed schematic with three separately protected paths; assembled inspection; battery-powered leakage and continuity check; DMG screen |
| S3 validation wear | only the sessions 7a prescribes, ≤ 4 h/day | S2 pass; protocol unchanged since S1 |
| S4 routine use | daily wear; decoder mapping promotion per the design record | all 7a criteria pass, including three days and background activities |

Fail at S3: rework, return to S2; changed contacts, coordinates, or shell
void the affected S0 and S3 observations. Interface rule: any change to
contact coordinates, stacks, cell, board outline, closure, or thickness
bumps the version, re-runs WP2's checks, and repeats any 3.7 item whose
input changed.

## 10. Open items, interface decisions, Open for Rolf

Open items (single-package, carried): (1) CREASE_BOW formula, clamp, and
report, WP2; (2) coupon-to-parameter mapping, WP2; (3) manifest schema and
hash rule, WP3.

Interface v2 decisions (cross-package): (1) medial-side packing: fits,
+3.5 mm length, or +3 mm width (WP6); (2) cell identity and maximum
dimensions (WP6); (3) hook stiffness measured versus estimate, HOOK_DIA
if outside 0.5–1.5 N (WP4 measures, WP6 decides); (4) a short-ear branch
with its own path, end wall, reference site, lead route, and closure; (5)
contact size other than M2.5; (6) closure replacement if the lip fails.

Open for Rolf: (1) measure M1 first; below 51 this release stops and the
plan returns with item 4 above; (2) the other seven measurements, or
"defaults" for a REF gauge; (3) which ear first (default right); (4)
approve the renders, then place order 1 under the checkout gate; (5) after
3.7, which thickness and preload, and whether the back view is acceptable;
(6) if WP6 escalates: longer, wider, or a smaller front end; (7) black
nylon only with a finishing statement; (8) buy the Stage A parts
(`docs/STAGE_A_PARTS.md`), which gate 7a and order 2; (9) any change to the
nickel-free requirement is his, outside this plan.
