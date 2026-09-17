# Elicio earpiece — mechanical interface

Version **2**. Date 2026-09-17. Plan revision 5, commit `0c5d0eb`.

This file is the mechanical contract between the shell (WP2/WP8), the
contact hardware (WP5), and the Stage B board (WP6). All coordinates
are millimetres in the **body frame** of plan §3.2, using path
coordinates `(u, s, y)` and the map `P(u, s, y)`. Contact axes are
−y. The medial face is y = 0.

Defaults in this file are the reference-ear full body: `VARIANT=full`,
`BODY_THICK=9.0`, `LID_Y=8.0`, `HOOK_PRELOAD=1.5`, `CREASE_BOW=3.0`,
`BODY_ARC=48.4`, `BODY_WIDTH=17.0`. Thin-body y limits use
`BODY_THICK=7.0` and `LID_Y=6.0`. Cartesian (x, z) follows from the
path; WP2 computes `P`.

A "From" cell names a plan section, a standard, or a datasheet. A row
that cannot be traced is marked **UNVERIFIED** and says what would
verify it.

## Version and change-log rule

This file starts at version 1. Any change to a dimension, keep-out,
route, envelope, height, or safety reservation in this file:

1. Bumps the version in this header and adds a dated row to the
   change log below.
2. Re-runs WP2's §3.3 checks.
3. Repeats the affected plan §3.7 items (plan §9).

A change of contact size, nut style, cell identity, board outline,
lead pads, or RF zone is an interface v2 item (plan §10). Do not
edit those numbers in CAD without bumping this file.

| Version | Date | What changed |
|---|---|---|
| 1 | 2026-09-16 | First issue. Numbers from plan §3.2–§3.3, §3.5, §4–§6, §9–§10. |
| 1 | 2026-09-17 | Review r1 errata; no dimension, keep-out, route, envelope or height changed. Stack derivation (§2.3, note D2, the ISO 4032 paragraph) corrected; WP5 SKU column added; pad gap given in the body frame (§6.1); nut material rule (§7); diode-array area marked UNVERIFIED (§8.2); §10 list updated; pending v2 notes added (§12). |
| 2 | 2026-09-17 | WP6 packing. Cell named (no published folded pack fits; pocket change for WP8). RF no-copper 12.4 × 3.8 traced. Lead pads frozen. Courtyards at max dims; packing confirmed with VQFN-32 and BAV199S, not a shell change. Flat-board sagitta and lid-underside constraint recorded. |
| 2 | 2026-09-17 | Review r2. No shell or keep-out number changed. The reference wire route (§4) changed under the board; WP2's Stage B wire-envelope check is not built yet (MOCK_CONTACTS=false is refused), so it runs on this route when it is. Board-side corrections: lug-tab envelopes counted in the free mask; VQFN courtyard at the RSM body maximum (4.60); two BAV199S-Q (one package has two independent pairs, three lines need three); SOT-23 occupied area 3.3 × 2.9; reference wire rerouted round keep-out 2; RF distance at the reserved 15.8 module. Packing withdrawn to **not confirmed** (§8.2); lead pads not frozen (§4). |

## 1. Frames and path

| Item | Value | Unit | From |
|---|---|---|---|
| Shell origin O | Hook root on the body's top face | – | plan §3.2 |
| Shell axes | X posterior, Y lateral, Z superior; skull at Y = 0 | – | plan §3.2 |
| Body frame | Shell frame rotated about X through O by −θ | – | plan §3.2 |
| θ | atan(HOOK_PRELOAD / TOTAL_CHORD); 1.79 at defaults | deg | plan §3.2 |
| Path | Circular arc in the body-frame XZ plane through O | – | plan §3.2 |
| CREASE_BOW | 3.0 at defaults; posterior bow at mid-length | mm | plan §3.3 |
| BODY_ARC | 48.4; chord 47.9 at defaults | mm | plan §3.3 |
| s | Arc length from O, 0 to BODY_ARC; −2 allowed for features | mm | plan §3.2 |
| u | Posterior offset along the in-plane normal | mm | plan §3.2 |
| y | Lateral height; medial face y = 0 | mm | plan §3.2 |
| P(u, s, y) | Maps path coordinates to body-frame points | – | plan §3.2 |

## 2. Contacts

Positions are centre-lines at the medial face. Final wear positions
come from WP7a (plan §4). Until then these coordinates are the CAD
and packing contract.

### 2.1 Coordinates

CONTACT_2 is CONTACT_1 plus pitch in the (u, s) plane:

`Δu = CONTACT_PITCH · sin(PAIR_ANGLE)`, `Δs = CONTACT_PITCH · cos(PAIR_ANGLE)`.

At the defaults: sin 22° = 0.3746, cos 22° = 0.9272, so Δu = 4.50,
Δs = 11.13, and CONTACT_2 = (u 10.4, s 33.1).

| Feature | u | s | y at face | Unit | From |
|---|---|---|---|---|---|
| CONTACT_1 | 5.9 | 22.0 | 0 | mm | plan §3.3 |
| CONTACT_PITCH | – | 12.0 centre-to-centre | – | mm | plan §3.3; L3 §2.2 band 12–15 |
| PAIR_ANGLE | 22 | – | – | deg | plan §3.3 |
| CONTACT_2 | 10.4 | 33.1 | 0 | mm | plan §3.3, from pitch and angle |
| CONTACT_REF | 8.5 | 43.0 | 0 | mm | plan §3.3; M6 recorded for WP7a |

### 2.2 Dome, hole, and screw

| Feature | Value | Unit | From |
|---|---|---|---|
| Screw | ISO 7380-style M2.5 × 4 button head, titanium Grade 2 or 5 | – | plan §4 |
| Thread pitch | 0.45 | mm | ISO 261 coarse M2.5; Westfield ISO 7380 table, read 2026-09-16 |
| CONTACT_DOME diameter | 4.7 | mm | plan §3.3, §4. See note D1 |
| CONTACT_DOME crown | 1.35 | mm | plan §3.3, §4. See note D1 |
| Hex socket | 1.5 | mm | plan §4; manufacturer M2.5 column s nom. 1.5, Westfield, read 2026-09-16 |
| CONTACT_HOLE | Ø2.9 through the 1.5 mm medial wall | mm | plan §3.3; ISO 273:1979 medium series for M2.5 = 2.9, read 2026-09-16 at fastenerchart.com/clearance-hole-chart |
| Wall thickness at hole | 1.5 | mm | plan §3.3 WALL_MEDIAL |
| Screw length | 4 | mm | plan §4 (M2.5 × 4) |
| MOCK_CONTACTS | true on the gauge: spherical caps only, no holes | – | plan §3.3, §3.5 step 5 |

Note D1. ISO 7380-1:2022 tables start at M3 (dk max 5.70, k max 1.65).
M2.5 is a manufacturer extension. Westfield's ISO 7380 table, read
2026-09-16 (https://www.westfieldfasteners.co.uk/Standards/ScrewBolt-SHBtn-M.html),
gives M2.5 dk max 4.5 and k max 1.5, not 4.7 and 1.35. The CAD contract
stays at the plan's 4.7 / 1.35 until WP5 names a SKU drawing. If the
SKU is 4.5 / 1.5, this file becomes v2. WP5 named SKUs but no head
drawing; pending as V2-1 (§12).

### 2.3 Stack above the floor

Floor of the cavity is y = 1.5. The stack sits on that floor. Order
from the floor: lug, nut, screw tip, Kapton disc. The reservation is the
plan's; the SKU column is `docs/fab/contacts.md` §2.2 set 1.

| Layer | Reservation | SKU (WP5) | y span, reservation (full body) | Unit | From |
|---|---|---|---|---|---|
| Cavity floor | – | – | 1.50 | mm | plan §3.3 CAVITY |
| Ring lug | 0.50 | 0.46 (TE 31428) | 1.50–2.00 | mm | plan §3.3, §4; contacts.md §1.3. See note D2 |
| Thin nut | 1.60 | 1.60 (DIN 439 M2.5) | 2.00–3.60 | mm | plan §4 DIN 439; ISO 4035 M2.5 m max 1.6, s max 5, e min 5.45, read 2026-09-16 at https://www.fasteners.eu/standards/iso/4035/ |
| Screw tip past nut | 0.40 | 0.44 | 3.60–4.00 | mm | 4.0 − 1.5 − lug − nut |
| Kapton disc | 0.13 | 0.13 (two layers Adafruit 3057, 0.064 each) | 4.00–4.13 | mm | plan §3.3, §4; contacts.md §1.4. See note D3 |
| Metal stack (lug+nut+tip) | 2.50 | 2.50 | 1.50–4.00 | mm | plan §3.3 CONTACT_STACK |
| Total above floor | 2.63 | 2.63 | 1.50–4.13 | mm | plan §4; 2.50 + 0.13 |
| Keep-out top | – | – | 4.13 | mm | plan §3.3 KEEPOUT_SIGNAL |

The screw head seats on the medial face at y 0, so the screw tip is at
y 4.00 for a 4 mm screw whatever the lug and wall are. The stack top is
the higher of the tip and the nut top (wall + lug + nut), plus Kapton.
Lug or nut thickness therefore does not raise the stack until wall + lug
+ nut passes 4.00: at the nominal 1.5 wall that is lug + nut ≤ 2.50, at a
wall printed 0.3 thick (plan §3.6 ±0.3) lug + nut ≤ 2.20. The reservation
(2.10) and the SKU set (2.06) meet both. WP2's script checks this as
`CONTACT_STACK`.

Note D2. Plan §8 row 9 assigns the lug thickness and tab ≤ 7 mm to WP5.
WP5 found TE 31428 at 0.46 mm (contacts.md §1.3), which closes the
thickness; its barrel width against the 3 mm tab is still UNVERIFIED. The
thicker catalog lugs read on 2026-09-16 (Molex 0193230001 0.71 mm, TE
34157 0.79 mm) would not raise the stack at nominal (lug + nut 2.31 and
2.39 ≤ 2.50) but break the wall +0.3 case (> 2.20).

Note D3. Plan 0.13 mm Kapton is met two ways: two layers of 2.5 mil
tape (WP5's SKU, 0.064 mm each including adhesive) or one disc of DuPont
Kapton 500HN, 5.00 mil, 127 µm nominal, tolerance 122–130 µm (QE-10167, https://www.qnityelectronics.com/content/dam/electronics/amer/us/en/electronics/public/documents/en/QE-10167-Kapton-General-Specifications.pdf,
read 2026-09-16).

Do not use ISO 4032 for this nut. ISO 4032 M2.5 is a style-1 nut,
m max 2.00 mm (https://www.fasteners.eu/standards/ISO/4032/, read
2026-09-16). With a 0.5 lug its top sits at y 4.00, level with the screw
tip: the stack still totals 2.63 at nominal but has no margin, and a wall
printed 0.3 thick puts the Kapton at y 4.43, into the board at 4.30. The
brief named ISO 4032; the plan names DIN 439 / ISO 4035. The plan wins.

## 3. Keep-outs

Keep-outs are air in the body frame after placement through `P`.
WP2 checks them only when `MOCK_CONTACTS` is false, except walls and
the lid recess, which exist on the gauge. Lug-tab envelopes are part
of the keep-out.

### 3.1 Contact keep-outs

| Feature | Shape | Coordinates | Unit | From |
|---|---|---|---|---|
| KEEPOUT_SIGNAL (CONTACT_1) | Cylinder, axis −y through P(5.9, 22.0, 0) | Ø7.1, y 1.5–4.13 | mm | plan §3.3 |
| KEEPOUT_SIGNAL (CONTACT_2) | Cylinder, axis −y through P(10.4, 33.1, 0) | Ø7.1, y 1.5–4.13 | mm | plan §3.3 |
| Signal lug tab, CONTACT_1 | Box on the floor, toward its pad | 3 × 7 × 1.5; from the cylinder toward pad (5.9, 26.6) | mm | plan §3.3 |
| Signal lug tab, CONTACT_2 | Box on the floor, toward its pad | 3 × 7 × 1.5; from the cylinder toward pad (5.5, 30.0) | mm | plan §3.3 |
| Copper-free margin | Extra 0.5 around each signal keep-out and tab, on the board | 0.5 | mm | plan §5 |

Tab reading used on the board (`placement.py` `tab_corners`): 3 wide,
7 long from the Ø7.1 edge along the contact-to-pad line, plus 0.5. The
pads sit 4.6 (SIG1) and 5.8 (SIG2) from their contact centres, so a 7 mm
tab runs past its own pad, and the CONTACT_2 tab reaches u 0.68, through
the low-u side wall at u 1.5. Whether the tab may be shorter (ending
under its pad) is open for Rolf (review r2 question 13).
| KEEPOUT_REF | The reference pocket itself | Cylinder Ø7.5, axis −y through P(8.5, 43.0, 0), y 1.5 to LID_Y | mm | plan §3.3 |
| Reference lug tab | Envelope inside the pocket, bent up | 3 × 1.5 × 6 tall | mm | plan §3.3 |
| End wall, pocket to cavity | Remaining nylon | 1.05 at defaults (s 38.2 to the Ø7.5 circle) | mm | plan §3.3 CONTACT_REF |

Ø7.1 is a reserved envelope, not a fastener standard. An ISO 4035
M2.5 nut has s max 5.0 and across-corners 5.77. The extra diameter
covers the lug ring, Kapton, and tool. WP5 must show the assembled
lug + nut + Kapton inside Ø7.1.

### 3.2 Rib, walls, lid recess

| Feature | Shape | Coordinates | Unit | From |
|---|---|---|---|---|
| WALL_MEDIAL (floor) | Box | y 0–1.5 under the whole plan outline | mm | plan §3.3 |
| WALL_SIDE, main body | Two boxes | s 0–38.2, u 0–1.5 and u 15.5–17.0, y 1.5 to LID_Y after recess | mm | plan §3.3, §3.5 |
| WALL_END, hook end | Box | s 0–1.5, u 0–17.0, y 1.5 to LID_Y | mm | plan §3.3 CAVITY start s 1.5 |
| Tail walls | Tapered shell | s 38.2–48.4, width 17 → 10 linear, same thickness, tip round 4.0; walls 1.5 except the 1.05 pocket-to-cavity web | mm | plan §3.3 TAIL, §3.5 |
| RIB | Box, full cavity width | s 17.5–18.3, u 1.5–15.5, y 1.5–4.5; 0.8 thick (exception E2) | mm | plan §3.3, §3.6, §5 |
| LID_RECESS | Cut | s 0–46.8 within the lid plan outline; all material y > LID_Y removed. Lip zone s 46.8–48.4 keeps full thickness | mm | plan §3.3, §3.5 step 3 |
| LID_Y | 8.0 full / 6.0 thin | mm | plan §3.3 |
| Lid solid | Plate | y LID_Y to LID_Y + 1.0, s −0.2 to 46.4, plan outline inset CLEAR_FIT 0.4 | mm | plan §3.5 step 7 |
| Cavity (air) | Swept box | s 1.5–38.2, u 1.5–15.5, y 1.5 to LID_Y; 36.7 × 14.0 × 6.5 | mm | plan §3.3, §5 |

RIB is locating only. Battery leads may pass over it. The rib occupies
s 17.5–18.3. BOARD_ZONE starts at s 18.3. They share that plane. WP2
must not let the rib occupy s > 18.3, where the superior pads sit.

## 4. Lead route

Only the insulated wire leaves the reference pocket (plan §3.3
KEEPOUT_REF, §5). The bare tab stays inside the pocket.

| Feature | Shape / rule | Coordinates | Unit | From |
|---|---|---|---|---|
| WIRE_CHANNEL | Box through the end wall into the pocket | u 7.7–9.3, y 2.5–4.1, s 38.2–40.5 | mm | plan §3.3 |
| Channel opening at u 9.3 | Reported by the script; must stay positive | 0.94 at bow 3; 1.09 at bow 1; 0.54 at bow 8 | mm | plan §3.3; WP2 geometry report |
| Wire envelope | Cylinder swept at 3 mm bend radius | Ø1.3 from each terminal to its pad | mm | plan §3.3 checks, §5 |
| Wire type | 28 AWG silicone, 26–28 AWG barrel | OD nom. 1.2, band 1.1–1.3 | mm | plan §4; BNTECHGO 28 AWG silicone OD 1.2 ± 0.1, read 2026-09-16 at https://bntechgo.com/28-awg-silicone-wire-stranded-tinned-copper-wire-1-feet-11-colors-optional/ |
| Reference wire length | 15 | mm | plan §3.3, §5 |
| All leads | ≤ 40, twisted | mm | plan §4 |
| Signal lug tabs | On the floor, under Kapton | 3 × 7 × 1.5 toward the pads | mm | plan §3.3 |
| LEAD_PADS (candidate, not frozen) | Three pads, medial board copper | (u, s) = (5.9, 26.6) SIG1, (5.5, 30.0) SIG2, (4.0, 29.0) REF | mm | plan §3.3 candidates; SIG1 s 26.5 → 26.6 so a 1.0 × 1.0 pad stays outside keep-out 1 plus 0.5 (`scripts/cad/placement.py`). They conflict with the lug tabs (§8.2) |
| Reference pad | The (4.0, 29.0) pad | Route centre-line (u, s): (8.5, 40.5) → (8.5, 38.2) → wrap (8.5, 37.0) → (5.0, 34.6) → (4.0, 29.0), under the board at y 2.5–4.1; Ø1.3; 3 mm bend; Kapton wrap at s 37. Clears keep-out 2 by 0.09 (`wire_keepout_gap`); crosses both signal lug tabs at the 7 mm reading | mm | plan §5; drawn in `docs/fab/cad/v1/placement.svg`. The round-1 straight run from s 37 to the pad entered keep-out 2 by 0.63 |
| Strain wrap | One Kapton wrap to the floor | at s 37 | mm | plan §5 |
| CABLE_EXIT | Cylinder through the posterior side wall (high-u wall) | Ø2.0 at s 36, y 3; plugged in Stage B | mm | plan §3.3, §5, §6 |

Pad rule: each pad sits on the medial side of the board, outside
keep-outs plus 0.5 mm and outside the antenna no-copper zone. Each
pad feeds its own 220 kΩ resistor and clamp within 10 mm (L4 §5.1,
plan §4). Each line needs its own series diode pair; one BAV199S-Q has
two, so three lines need two packages. With the tabs counted, neither
array has a legal site within 10 mm of its pads (§8.2).

## 5. Cell envelope

The cell is a 501015-class pouch. WP6 names the SKU below. No published
folded pack fits the plan's 5.2 × 10.4 × 15.6 mm envelope. The pocket
size in CAD does not change in this version; WP8 applies the pocket
change in the table if Rolf keeps the in-line DNK pack.

| Feature | Value | Unit | From |
|---|---|---|---|
| Class | 501015, 50 mAh, 3.7 V | – | plan §1, §5; L4 §1.4 |
| Named SKU | DNK 501015 (fpbattery drawing, file A/FP1015-12293, page 2) | – | https://www.fpbattery.com/wp-content/uploads/2024/06/fpbattery-501015-3.7V-50mAh-Lithium-Polymer-Battery-Specification.pdf, read 2026-09-17. Drawing date on the cell art: 2022-12-10. The drawing is marked "PRELIMINARY", so its dimensions need the vendor's released drawing before a cell is bought |
| Cell body (drawing) | T 5, W 10, L 15 | mm | same page |
| Pack as drawn | PCM in-line; BL 17 ± 1, so 16–18 long × 10 wide × 5 thick | mm | same page, items BL, W, T |
| Folded pack ≤ 5.2 × 10.4 × 15.6 | **No published SKU** | mm | DNK in-line BL max 18. JP501015 cell 5.0 × 10 × 15 Max with "PCB: customized" and no folded envelope (https://www.jx-battery.com/consumer-electronic-battery/li-polymer-battery/headset-battery-li-polymer-battery-jp501015.html, read 2026-09-17) |
| PCM on this drawing | In-line on the length; tabs (M = 10) at the BL end | – | DNK page 2 |
| Tab exit for this shell | Tabs toward the rib; cell packed toward the hook (low-s) | – | plan §5; RF distance in §6.3 |
| Cell body maximum (plan envelope) | 5.2 thick × 10.4 wide × 15.6 long | mm | plan §3.3, §5. Unchanged. Not met by the DNK pack as drawn |
| BATTERY_POCKET | s 1.5–17.5, u 3.1–13.9, y 1.5–7.5 | mm | plan §3.3 |
| Pocket size (gauge, unchanged) | 16.0 × 10.8 × 6.0 | mm | plan §5 |
| Foam under the lid | 0.5 | mm | plan §5 |
| WP8 pocket change if the DNK in-line pack is kept | Pocket length 16.0 → 18.4 along s (BL max 18 plus 0.4 leftover, same leftover the plan gave 15.6 in 16.0). BOARD_ZONE start moves from 18.3 to 20.7 unless BODY_ARC grows 2.4. Rib can stay 0.8 thick. | mm | DNK BL 17 ± 1; plan leftover 0.4 |

Plan §5 prescribes the fold as a hand step: "PCM folded on the lateral face
under Kapton". In thickness that leaves the pocket depth 6.0 minus the 0.5
foam, 5.5, for the cell (T 5 on the DNK drawing, 5.2 plan maximum) plus the
folded PCM and its Kapton: 0.5 at T 5, 0.3 at T 5.2. The DNK drawing gives
no PCM board thickness, so that fold is UNVERIFIED. If WP8 instead
lengthens the pocket 2.4 mm by growing BODY_ARC, TOTAL_CHORD grows by about
the same and the M1 gate (`gate` = TOTAL_CHORD + 3 in `bte_fit_shell.py`;
plan §3.3) rises with it;
that is a shell change and re-runs plan §3.7.

A custom fold of the DNK PCM onto the 10 mm face is not on the datasheet.
That fold would be about 10 + PCM thick, which already uses the 10.8 mm
pocket width and breaks the 10.4 mm envelope. Do not buy a cell on a
custom fold until Rolf accepts either the +2.4 mm pocket or a drawing
that shows a pack ≤ 5.2 × 10.4 × 15.6.

### 5.1 Flat board on the curved floor

The floor follows PATH_RADIUS 97.1025 mm (`manifest.json`). A 19.0 mm
flat board is a chord of that arc.

| Feature | Value | Unit | From |
|---|---|---|---|
| PATH_RADIUS | 97.1025 | mm | manifest `PATH_RADIUS`; WP2 `make_path(48.4, 3.0)` |
| Board length (chord) | 19.0 | mm | plan §5 |
| Sagitta (arc to chord at mid-s) | 0.466 | mm | h = R − sqrt(R² − (c/2)²); `placement.py` `sagitta_mm` |
| Direction | Path plane (body XZ / −u), not Y | – | `p_xyz` passes y through as Cartesian Y |
| Pad placement | Chord: four pads equal height y 1.5–4.3 | mm | plan §5 underside y 4.3; staggering pad heights would tilt the board in Y |
| Board underside Y | 4.3 everywhere | mm | planar PCB at constant Y |
| KEEPOUT_SIGNAL top Y | 4.13 | mm | plan §3.3 |
| Y clearance, whole board | 0.17 | mm | 4.3 − 4.13. Holds at mid-s, not only at the pads |
| Arc-to-chord gap at keep-out 1 | 0.274 | mm toward −u | `chord_gap_at(6.1)` from board mid-s 28.1 |
| v1 §6.1 0.09 mm figure | Developed (u, s) nylon-pad gap; not a Y clearance | mm | superseded for Y by this 0.17 mm; body-frame pad gap remains WP2 0.152 / 0.110 / 0.263 |

The 0.17 mm Y gap survives the sagitta. Do not raise the board. Mid-s the
board sits 0.47 mm toward −u of the developed rectangle; keep copper 0.5 mm
in from the low-u edge at mid-s. WP8 does not change the gauge for this.

### 5.2 Lid underside (Q11, order 2)

The 0.8 mm lid emboss is from the lid underside into the cavity. Module
top is y 7.6; lid underside is y 8.0; headroom 0.4. An 0.8 stamp reaches
y 7.2 and enters the module envelope.

| Rule for order 2 | Value | From |
|---|---|---|
| Over BOARD_ZONE (s 18.3–37.9) | Emboss depth ≤ 0.4 mm, so the stamp stays at y ≥ 7.6 | plan §5 stack; Q11 |
| Preferred | Move the string over BATTERY_POCKET (s 1.5–17.5), still ≤ 0.4 mm, into the 0.5 foam | same |
| Gauge (order 1) | 0.8 mm remains; no module in the gauge | Q11 reading |

WP8 builds one of those two. Do not keep 0.8 mm over the module.

## 6. Board

The board is out of scope for trace layout. This section is the envelope
the named pack meets.

### 6.1 Outline and supports

| Feature | Value | Unit | From |
|---|---|---|---|
| BOARD_ZONE | s 18.3–37.9, u 1.5–15.5 | mm | plan §3.3 |
| Board outline | 19.0 × 12.5 × 1.0 | mm | plan §5 |
| Underside | y 4.3 on four pads | mm | plan §5 |
| Side clearance | 0.75 | mm | plan §5 |
| End clearance | 0.3 | mm | plan §5 |
| Retention | Pads, lid, and a 0.5 foam strip over the superior 3 mm of the board | mm | plan §5 |
| Corner pads | 1.5 × 1.5, y 1.5–4.3 | mm | plan §3.3 |

Pad boxes at the BOARD_ZONE corners (full body):

| Pad | u | s | y | Unit |
|---|---|---|---|---|
| Superior, low-u | 1.5–3.0 | 18.3–19.8 | 1.5–4.3 | mm |
| Superior, high-u | 14.0–15.5 | 18.3–19.8 | 1.5–4.3 | mm |
| Inferior, low-u | 1.5–3.0 | 36.4–37.9 | 1.5–4.3 | mm |
| Inferior, high-u | 14.0–15.5 | 36.4–37.9 | 1.5–4.3 | mm |

The superior low-u pad's inner corner (u 3.0, s 19.8) is 3.64 mm from
CONTACT_1 (u 5.9, s 22.0) in (u, s). KEEPOUT_SIGNAL radius is 3.55 mm, so
the gap is 0.09 mm in (u, s). In the body frame, where s spacing grows
with u along the arc, WP2's script computes 0.152 mm at bow 3, 0.110 at
bow 1 and 0.263 at bow 8 (`keepout_clearance` in `manifest.json`), and
fails the build if any gap to a pad, the rib or a wall is not positive.
The 0.5 mm copper-free margin around the keep-out does overlap that pad
in plan view; the pad is nylon support, not copper. Y clearance from the
board underside to the keep-out top is 0.17 mm everywhere (§5.1). The
sagitta does not reduce that Y gap.

### 6.2 Heights by zone

| Zone | Allowed height | y span (full, board at 4.3–5.3) | Unit | From |
|---|---|---|---|---|
| Over KEEPOUT_SIGNAL | Air only to y 4.13; board underside at 4.3 (gap 0.17) | 1.5–4.13 keep-out, 4.3 board | mm | plan §3.3, §5 |
| Medial components | ≤ 1.2, not over keep-outs or the RF zone | 3.1–4.3 | mm | plan §5 |
| Board core | 1.0 | 4.3–5.3 | mm | plan §5 |
| Lateral, module | 2.3 max | 5.3–7.6 | mm | plan §5; 4.3 + 1.0 + 2.3 = 7.6 |
| Under the lid | Lid underside at 8.0; 0.4 remains above the module | 7.6–8.0 | mm | plan §5 |
| Thin body | Same stack does not fit under LID_Y = 6.0 | – | plan §5. Full 9.0 mm stays a design value; packing is not confirmed (§8.2); thin remains a gauge only |

### 6.3 RF zone

Module: Raytac MDBT50Q-1MV2, chip antenna.

| Feature | Value | Unit | From |
|---|---|---|---|
| Nominal module | 15.5 × 10.5 × 2.05 | mm | Raytac Spec K, issued 2022-07-01, page 7, https://cdn.sparkfun.com/assets/4/7/4/3/8/_nRF52840__MDBT50Q-1MV2___MDBT50Q-P1MV2_Ver.K_spec.pdf, read 2026-09-17; plan §8 row 10 |
| Width max | 10.5 + 0.2 = 10.7; length 15.5 + 0.2 = 15.7 | mm | Spec K page 7 table (Min −0.15, MAX +0.2 on L and W) |
| Reserved max (this interface) | 15.8 × 10.8 × 2.3 | mm | plan §5 (tolerance, solder, shield). Unchanged |
| Placement | Lateral side of the board; antenna end at the inferior board edge (high-s). Nominal footprint s 22.1–37.6, u centred on the board | – | plan §5; module 15.5 from s 37.6 |
| No-copper polygon | 12.4 wide × 3.8 along s, on every layer, at the inferior board edge; make it as wide as the PCB (here 12.5, clipped to 12.4). Extra top-layer notch at the feed as in Spec K page 9 | mm | Spec K §2.3 pages 9 and 13, issued 2022-07-01, read 2026-09-17 |
| Antenna on the board | s 33.8–37.6, u 2.30–14.70 | mm | 3.8 mm in from s 37.6; 12.4 centred on BOARD_U |
| Plan rule | "Raytac MDBT50Q-1MV2 15.8 × 10.8 × 2.3 max, antenna end at the inferior board edge, ≥ 5 mm from the battery" | – | plan §5. Spec K states no distance to a battery or metal |
| Module body to cell, reserved 15.8, cell packed to the hook | 4.70 (s 21.8 − 17.1) | mm | fails 5 if the rule means the module body |
| Module body to cell, reserved 15.8, cell against the rib | 4.30 (s 21.8 − 17.5) | mm | fails 5 |
| Module body to cell, nominal 15.5, packed to the hook | 5.00 (s 22.1 − 17.1) | mm | round 1's figure; nominal, not the reserved maximum |
| Antenna no-copper zone to cell, packed to the hook | 16.70 (s 33.8 − 17.1) | mm | passes 5 if the rule means the antenna. Which reading holds is open for Rolf (review r2 question 14). A DNK in-line pack (BL max 18) ends 2.4 further toward the module |
| Overlap | Antenna s 33.8–37.6 overlaps KEEPOUT_SIGNAL of CONTACT_2 (s 29.55–36.65) | – | plan §5; `placement.py` `rf_keepout2_overlap` |
| Lead pads vs RF | All three candidate pads have s ≤ 30.5, outside s 33.8 | – | §4 |

### 6.4 Where the ADS1292 and the charger may sit

| Part | Package | Body / courtyard | Height | Side | Rule | From |
|---|---|---|---|---|---|---|
| ADS1292 packing candidate | VQFN-32 (RSM), orderable ADS1292IRSMT / IRSMR | Body 4.00 × 4.00 nominal, 4.10 × 4.10 max; courtyard 4.60 × 4.60 | 1.0 max | Medial | Entire courtyard outside keep-outs + 0.5, lug tabs + 0.5 and the RF zone. Candidate site u 9.90–14.50, s 22.55–27.15 | TI ADS1292 datasheet SBAS502C (April 2020), RSM drawing 4219108/B 08/2019, https://www.ti.com/lit/ds/symlink/ads1292.pdf, read 2026-09-17; IPC-7351B Nominal excess 0.25 mm/side, https://www.pcbsync.com/ipc-7351-land-pattern/, read 2026-09-17 |
| ADS1292 TQFP-32 (PBS) | Not used on this board | Body 4.95–5.05 SQ; lead span 6.90–7.10 SQ; height 1.20 max; courtyard 7.60 × 7.60 | 1.2 max | Medial | Does not fit: largest empty rectangle on the free mask is 4.55 × 10.20 | TI PBS drawing 4087735/B 07/05, https://www.ti.com/lit/ml/mpqf027a/mpqf027a.pdf, read 2026-09-17 |
| Charger | TI BQ25100 YFP DSBGA-6 | Body 1.60 × 0.90; courtyard 2.10 × 1.40 | 0.5 max | Either; candidate u 10.25, s 21.15, toward the rib | Not in the RF zone; not over keep-outs | TI BQ25100 YFP0006 4223410/A 11/2016, https://www.ti.com/lit/ds/symlink/bq25100.pdf, read 2026-09-17 |
| LDO | TI TLV713 3.3 V, X2SON-4 (DQN) | Body 1.00 × 1.00; courtyard 1.50 × 1.50 | ≤ 1.2 | Medial, next to the charger; candidate u 12.35, s 21.05 | Not in the RF zone | TI TLV713 SBVS195F, revised August 2019, page 1, https://www.ti.com/lit/ds/symlink/tlv713.pdf, read 2026-09-17 |
| Charge pads | On the board, inside the cavity | – | – | Reached with the lid off | No skin-side port | plan §2 item 16, §5, §6 |
| Clamps | Two BAV199S-Q TSSOP6 (SOT363-3). One package is two independent series pairs (pins 1 A1, 6 K1;A2, 2 K2 and 4 A3, 3 K3;A4, 5 K4): array 1 clamps SIG1 and SIG2, array 2 clamps REF, one pair spare | Occupied area 2.65 × 2.35 each | ≤ 1.2 | Medial, within 10 mm of each pad | No legal site with the tabs counted (§8.2). Round 1's single array at u 4.20, s 27.10 clamped two lines, not three, and sat under the REF pad | Nexperia BAV199S-Q, 20 July 2026, pinning and Fig. 8, https://assets.nexperia.com/documents/data-sheet/BAV199S-Q.pdf, read 2026-09-17 |
| Clamps, SOT-23 option | Three BAV199 SOT-23, one pair each | Occupied area 3.3 × 2.9 each | ≤ 1.2 | Medial | 28.71 mm² for three | Nexperia BAV199, 1 April 2023, Fig. 9, https://assets.nexperia.com/documents/data-sheet/BAV199.pdf, read 2026-09-17 |

The module takes most of the lateral face (15.8 × 10.8 on a 19.0 × 12.5
board). The ADS1292 VQFN and the charger share the medial face with the
keep-outs, the lug tabs, and the three pads. TQFP-32 does not fit that
face at Nominal courtyards.

## 7. Insulation and safety (mechanical)

These are shell and stack rules. The schematic (three series resistors
and clamps) is not this package.

| Rule | Mechanical reservation | From |
|---|---|---|
| Kapton on each stack | 0.13 disc on top of nut and tip; signal tabs on the floor under Kapton; reference tab upright in the pocket | plan §4, §5, §6 |
| Three separately protected paths | Each contact reaches the board only through its own lug, insulated lead, pad, resistor, and clamp. No pre-resistor conductor may touch the battery, the charge pads, or other copper | plan §6; design record requirement 4 |
| Only insulated wire leaves the reference pocket | Bare tab stays in KEEPOUT_REF | plan §3.3, §5 |
| Board medial copper | Solder-mask except the three lead pads | plan §5 |
| Board underside vs keep-out top | 0.17 mm in Y everywhere on a chord-mounted board (§5.1). Do not stagger pad heights | plan §5; PATH_RADIUS |
| Lid underside over the module | Emboss ≤ 0.4 mm over BOARD_ZONE, or move the string over the battery zone (§5.2) | Q11 |
| No charging port | No skin-side connector. Charge pads inside the closed cavity, lid off | plan §5, §6 |
| Never charge while worn | Procedural, on the assembly sheet | plan §6; design record requirement 3 |
| CABLE_EXIT | Ø2.0 for tethered bring-up only; plugged before wear in Stage B | plan §5, §6 |
| Tethered bring-up | Laptop on battery, not mains | plan §6; design record requirement 3 |
| Skin materials | PA12 (natural grey) and titanium only | plan §4, §6 |
| Metal inside the cavity | Nut and lug: plated steel or tinned copper (plan §4). Stainless is not in that allowance and plan §1 item 4 says "no stainless"; a stainless nut needs Rolf's decision. Full list: contacts.md §6 | plan §1, §4; contacts.md §1.2, §6 |
| Cleaning | 70 % isopropanol wipe; nothing on the skin side but titanium and nylon | plan §4, §6 |

## 8. Packing budget

Board area 19.0 × 12.5 = 237.5 mm², quoted 237 in plan §5. Heights
are in §6.2. 9.0 mm body thickness stays a design value; in height, a
VQFN-32 and a 2.3 max module fit the 8.0 mm lid with 0.4 mm headroom,
subject to §5.2. In area the medial face does not close (§8.2).

Raster: 0.025 mm pitch on the board rectangle in `scripts/cad/placement.py`.
Unions, not a sum of overlapping boxes.

### 8.1 Area at maximum datasheet courtyards

| Item | mm² | From |
|---|---|---|
| Board | 237.50 | 19.0 × 12.5; plan §5 |
| Keep-out 1 on the board (Ø7.1, no margin) | 39.38 | circle ∩ board |
| Keep-out 1 + 0.5 copper-free | 48.65 | plan §5 margin 0.5 |
| Keep-out 2 on the board | 39.59 | circle ∩ board |
| Keep-out 2 + 0.5 | 51.53 | same margin |
| Antenna no-copper 12.4 × 3.8 | 47.12 | Spec K pages 9 and 13 |
| Keep-out 2 ∪ antenna (with margin) | 78.53 | union; plan estimated ≈ 68 |
| Signal lug tabs + 0.5 (3 × 7 from the Ø7.1 edge) | 40.91 | interface §3.1; union with the rest counted once |
| Rim 0.25 mm | 15.50 | plan §5 ≈ 15 |
| Available (free mask) | 69.36 | board minus keep-outs + 0.5, lug tabs + 0.5, antenna, rim; unions |
| Available if the tabs end under their pads | 86.97 | same mask, tab length to the pad centre |
| Available with no tabs (round 1's mask) | 101.53 | does not meet plan §5 "keep-outs Ø7.1 plus lug tabs plus 0.5 copper-free margin" |
| Largest empty rectangle | 4.55 × 10.20 = 46.41 | `placement.py` `_largest_rect` |
| ADS1292 TQFP-32 courtyard | 57.76 (7.60 × 7.60) | PBS lead span max 7.10 + 2 × 0.25 IPC-7351B Nominal |
| ADS1292 VQFN-32 courtyard | 21.16 (4.60 × 4.60) | RSM body max 4.10 + 2 × 0.25 |
| Three BAV199 SOT-23 | 28.71 (3 × 3.3 × 2.9) | Nexperia Fig. 9 occupied area, 1 April 2023 |
| Two BAV199S-Q | 12.46 (2 × 2.65 × 2.35) | Nexperia Fig. 8 occupied area, 20 July 2026 |
| BQ25100 courtyard | 2.94 (2.10 × 1.40) | 1.60 × 0.90 + 2 × 0.25 |
| TLV713 courtyard | 2.25 (1.50 × 1.50) | 1.00 × 1.00 + 2 × 0.25 |
| 25 × 0402 | 40.50 (25 × 1.80 × 0.90) | IPC-7351B small-chip Nominal; pcbsync courtyard excess 0.15 mm on chips smaller than 1608, read 2026-09-17 |
| Required, as-drawn TQFP + 3 SOT-23 | 132.16 | 57.76 + 28.71 + 2.94 + 2.25 + 40.50 |
| Required, named (VQFN + two BAV199S-Q) | 79.30 | 21.16 + 12.46 + 2.94 + 2.25 + 40.50 |
| Spare, named | −9.94 | 69.36 − 79.30 |
| TQFP 7.60² on the free mask | Does not fit | largest empty 4.55 wide |
| VQFN 4.60² on the free mask | Fits alone | candidate u 9.90, s 22.55 |
| 0402 courtyards placed after the ICs | 10 of 25 | greedy, medial only (`place_0402s`) |

Plan 105 vs 111 used body-sized boxes (7 × 7, 1 mm² per 0402) and no lug
tabs. Real Nominal courtyards are larger, the keep-out ∪ antenna union is
78.53 not 68, and the tabs take 40.91 with their margin. Round 1's
two-sided 0402 placements over the VQFN were not checked against
anything and are removed.

### 8.2 Escalation options (plan §10 interface item 1)

Packing is **not confirmed**. Round 1 confirmed it with one BAV199S-Q,
a 4.50 VQFN courtyard and no lug tabs in the mask; review r2 found those
three wrong (§4, §6.4, §8.1). `placement.py` `layout_conflicts()` now
lists, and `docs/fab/cad/v1/placement.svg` prints, what the candidate
layout breaks:

1. BAV199S_1: no legal site
2. BAV199S_2: no legal site
3. named pack 79.30 mm² > free 69.36 mm²
4. pad SIG2 within 0.5 of the SIG1 lug tab
5. pad REF within 0.5 of the SIG1 lug tab
6. pad REF within 0.5 of the SIG2 lug tab
7. SIG2 lug tab reaches a side wall (u 0.68–8.20)
8. reference wire crosses the SIG1 lug tab
9. reference wire crosses the SIG2 lug tab
10. cell to reserved module 4.70 < 5 mm

Items 1–9 depend on the tab reading (review r2 question 13); item 10 on
the RF reading (question 14). At the short tab reading the free area is
86.97 against 79.30 required, but the greedy layout still finds no array
site within 10 mm of the pads, so pads and tab directions need a WP6
round 3 either way. Rolf picks the escalation (plan §10 Open for Rolf
item 6; review r2 question 15).

| Option | What changes | Area it buys | Height / fit | From |
|---|---|---|---|---|
| A. Diode arrays only | Two BAV199S-Q in place of three SOT-23 | Saves 16.25 mm² (28.71 − 12.46) | TQFP still does not fit (7.60 > 4.55 empty width) | Nexperia occupied areas |
| B. Longer | Board length +3.5 mm → 22.5 × 12.5 = 281.25 | +43.75 board; empty width stays ~4.55; TQFP still no | Cavity length 36.7 → 40.2; BODY_ARC grows about 3.5; M1 gate moves. WP2 re-runs | plan §10 item 1 |
| C. Wider | Board width +3.0 mm → 19.0 × 15.5 = 294.5 | +57.0 board; empty width ~7.55; TQFP 7.60 still 0.05 short at Nominal; Least courtyard 7.30 would fit | BODY_WIDTH 17 → 20; cavity 14 → 17. Covertness. WP2 re-runs | plan §10 item 1 |
| D. Smaller front end | ADS1292 VQFN-32 4.60 × 4.60 (21.16 mm²) instead of TQFP 7.60 × 7.60 (57.76); plus two BAV199S-Q | Required 79.30 against 69.36 available; short by 9.94 | Medial height still ≤ 1.2; no shell change; does not close alone | TI RSM; this file §8.1 |
| E. Two-sided (not in the plan) | Passives on the lateral face outside the reserved module (s 18.6–21.8, about 3.2 × 12.5) | Up to about 40 mm² before rim and pads | Height there under the lid 8.0 − 5.3 = 2.7; plan §5 lists only the module on the lateral side | review r2; plan §5 |

Options B and C change the shell and need a second gauge (plan §7 order
1 rework). Option E changes no shell number but departs from plan §5.

## 9. Version notes (plan vs brief vs design record)

The plan wins. These are not silent CAD changes.

1. The WP1 brief names ISO 4032. The plan names a DIN 439 / ISO 4035
   thin nut, m = 1.6 mm. ISO 4032 M2.5 is m = 2.0 mm: level with the
   screw tip at nominal and into the board at a wall printed 0.3 thick
   (§2.3). This file follows the plan.
2. The design record allows stainless or carbon-TPU on skin. The plan
   allows titanium only. This file follows the plan.
3. L3 recommended 7–9 mm floating domes. The plan uses rigid ISO 7380
   M2.5, 4.7 mm. This file follows the plan. A different contact size
   is interface v2 (plan §10 item 5).
4. L4 placed charging pads on the skin-side face. The plan puts pads
   inside the cavity, lid off. This file follows the plan.
5. L4's module number is 15.5 × 10.5 × 2.05. This file reserves the
   plan's 15.8 × 10.8 × 2.3 maximum.
6. Plan packing used TQFP-32 and three SOT-23. Those courtyards do not
   fit. VQFN-32 and two BAV199S-Q (options D plus A) do not fit either
   once the lug tabs are counted (§8.2).

## 10. UNVERIFIED list

| # | Claim in this file | What would verify it | Owner |
|---|---|---|---|
| 1 | Dome Ø4.7, crown 1.35 | WP5 SKU drawing. ISO 7380-1:2022 has no M2.5 row; catalog M2.5 is 4.5 / 1.5 | WP5 |
| 2 | Lug tab ≤ 3 wide × 7 long | Thickness closed by WP5 (TE 31428, 0.46); barrel width still needs the drawing | WP5 |
| 3 | Assembled lug + nut + Kapton inside Ø7.1 | Height closed by WP5 (2.63 on the SKU set); plan-view fit of the ring (5.16 wide) and nut (5.77 across corners) inside Ø7.1 is by arithmetic, not a drawing | WP5 |
| 4 | Cell body ≤ 5.2 × 10.4 × 15.6 with PCM folded | Closed as a negative: no published SKU. DNK 501015 in-line BL 17 ± 1. WP8 pocket +2.4 mm along s if that pack is kept (§5) | WP6 / WP8 |
| 5 | RF no-copper polygon in millimetres | Closed: 12.4 × 3.8 at the inferior board edge, Spec K pages 9 and 13, issued 2022-07-01 (§6.3) | WP6 |
| 6 | Lead pad (u, s) values | Reopened by review r2: (5.9, 26.6), (5.5, 30.0), (4.0, 29.0) conflict with the lug tabs (§8.2) | WP6 round 3 |
| 7 | Channel opening 0.94 mm at bow 3 | Closed by WP2: 0.938 at bow 3, 1.089 at bow 1, 0.537 at bow 8 (`wire_channel` in manifest.json). Stage B containment still WP8 | WP2 / WP8 |
| 8 | 0.09 mm pad-to-keep-out gap at CONTACT_1 | Closed by WP2's check: body-frame gap 0.110–0.263 over bows 1–8 (§6.1) | WP2 |
| 9 | Plated-steel DIN 439 M2.5 nut SKU | A product page, date and price (contacts.md §1.2) | WP5 |

## 11. Sources read (web, 2026-09-16 and 2026-09-17)

| Source | URL | Used for |
|---|---|---|
| Plan | `docs/fab/plan.md` at `0c5d0eb` | Contract numbers |
| L3 | `docs/fab/L3-contacts.md` | Pitch band, three contacts |
| L4 | `docs/fab/L4-pod.md` | Module, ADS1292, 501015, charger, clamps |
| ISO 7380-1 manufacturer table | https://www.westfieldfasteners.co.uk/Standards/ScrewBolt-SHBtn-M.html | M2.5 dk 4.5, k 1.5, s 1.5; standard itself starts at M3 |
| ISO 7380-1:2022 scope | https://www.iso.org/standard/78699.html | M3–M16 only |
| ISO 4035 / DIN 439 | https://www.fasteners.eu/standards/iso/4035/ | Thin nut m 1.6, s 5 |
| ISO 4032 | https://www.fasteners.eu/standards/ISO/4032/ | Style-1 nut m 2.0; not used |
| ISO 273 medium M2.5 | https://fastenerchart.com/clearance-hole-chart/ | Hole Ø2.9 |
| Raytac Spec L | https://www.raytac.com/download/index.php?index_id=43 | Module size (v1). Spec K used for the keep-out millimetres in v2 |
| Raytac Spec K | https://cdn.sparkfun.com/assets/4/7/4/3/8/_nRF52840__MDBT50Q-1MV2___MDBT50Q-P1MV2_Ver.K_spec.pdf | Issued 2022-07-01. Module size page 7; no-ground 12.4 × 3.8 pages 9 and 13 |
| TI ADS1292 | https://www.ti.com/lit/ds/symlink/ads1292.pdf | VQFN 4 × 4, TQFP 7 × 7 class, 1.2 max (PBS) |
| TI PBS (S-PQFP-G32) | https://www.ti.com/lit/ml/mpqf027a/mpqf027a.pdf | 4087735/B 07/05; body 5.05 SQ max, lead span 7.10 SQ max |
| TI BQ25100 | https://www.ti.com/lit/ds/symlink/bq25100.pdf | YFP 1.60 × 0.90, 0.5 max, drawing 4223410/A 11/2016 |
| TI TLV713 | https://www.ti.com/lit/ds/symlink/tlv713.pdf | SBVS195F Aug 2019; X2SON 1.00 × 1.00 |
| Nexperia BAV199 | https://assets.nexperia.com/documents/data-sheet/BAV199.pdf | 1 April 2023; one series pair; SOT23 occupied 3.3 × 2.9 Fig. 9 |
| Nexperia BAV199S-Q | https://assets.nexperia.com/documents/data-sheet/BAV199S-Q.pdf | 20 July 2026; two independent series pairs; occupied 2.65 × 2.35 Fig. 8 |
| IPC-7351B courtyard excess | https://www.pcbsync.com/ipc-7351-land-pattern/ | Nominal 0.25 mm/side; Least 0.10; small-chip Nominal 0.15; read 2026-09-17 |
| Kapton 500HN | https://www.qnityelectronics.com/content/dam/electronics/amer/us/en/electronics/public/documents/en/QE-10167-Kapton-General-Specifications.pdf | 0.127 mm, tol. 0.122–0.130 |
| DNK 501015 | https://www.fpbattery.com/wp-content/uploads/2024/06/fpbattery-501015-3.7V-50mAh-Lithium-Polymer-Battery-Specification.pdf | Page 2: L 15, W 10, T 5, BL 17 ± 1; cell art 2022-12-10 |
| JP501015 | https://www.jx-battery.com/consumer-electronic-battery/li-polymer-battery/headset-battery-li-polymer-battery-jp501015.html | Cell 5.0 × 10 × 15 Max; PCM customized, no folded envelope |
| VCELL 501015 | https://www.vcellpower-battery.com/3.7v/501015-3-7v-50mah-lithium-polymer-battery-.html | 5.2 × 10.5 × 17.5 max example |
| 28 AWG silicone | https://bntechgo.com/28-awg-silicone-wire-stranded-tinned-copper-wire-1-feet-11-colors-optional/ | OD 1.2 ± 0.1 |

## 12. Pending interface notes

V2 items closed by this version are marked closed. Open items stay until
their owner closes them. None of the closed rows changes a number that
v1 froze except the RF polygon and the cell identity; review r2 reopened
the lead pads and the packing choice.

| # | Item | Now | What would change | Owner |
|---|---|---|---|---|
| V2-1 | Contact dome | CAD prints Ø4.7 × 1.35 (plan §3.3). No SKU drawing on file: WP5's listings give dk 4.40–4.70 and k 1.20–1.36; a manufacturer ISO 7380 M2.5 row gives dk max 4.5, k max 1.5 (note D1) | A drawing for the bought screw sets CONTACT_DOME; area 17.3 mm² at 4.7, 15.9 at 4.5, 15.2 at 4.4 (plan §4 pressure estimate moves with it) | WP5, then WP8 |
| V2-2 | Coupon-to-parameter mapping (plan §10 open item 2) | Mapping in this file, in `scripts/cad/bte_fit_shell.py` docstring, in `scripts/cad/placement.py` docstring, and in `scripts/cad/README.md` | Measured coupon sizes feed the parameters in the table | WP2 (mapping), WP8 (update) |
| V2-3 | Nut metal (Q6; Rolf's) | Plan §4 allows plated steel or tinned copper. No plated-steel DIN 439 M2.5 SKU is on file. Candidates, none chosen: (1) plated carbon-steel DIN 439 thin nut, zinc not nickel, SKU UNVERIFIED; (2) McMaster 18-8 `90710A025`, outside plan text, nickel-bearing; (3) Accu A2 `HNU-M2-5-A2`, same; (4) titanium DIN 934, m = 2.0, zero stack margin at wall +0.3. Status: open. WP6 does not decide it | A plated-steel SKU, or Rolf accepting stainless inside the cavity, or titanium DIN 934 with its zero margin (§2.3) | **Rolf**, WP5 |
| V2-4 | Packing shortfall | Reopened by review r2: VQFN-32 + two BAV199S-Q need 79.30 mm² against 69.36 free with lug tabs; ten layout conflicts (§8.2) | Tab reading (r2 Q13), RF reading (Q14), escalation B, C or E (Q15), then new pads | **Rolf**, WP6 round 3 |
| V2-5 | Lid emboss vs module (Q11) | Constraint written in §5.2. Gauge keeps 0.8 mm | Order 2: emboss 0.4 mm or move over the battery zone | WP8 |

V2-2, coupon features and what each one measures. Coupon axes as in
`scripts/cad/bte_fit_shell.py` `build_coupon`: x and y across the top
face from its centre, the rib on the top face.

| Coupon feature | Position (x, y) | Designed | Feeds |
|---|---|---|---|
| Hole | (−3, −3) | Ø1.7 through | Smallest round hole the process opens; lower bracket for CONTACT_HOLE |
| Hole | (0, −3) | Ø2.9 through | CONTACT_HOLE directly: an M2.5 shank (2.5) must pass |
| Hole | (3, −3) | Ø3.4 through | Upper bracket: CONTACT_HOLE moves toward it if Ø2.9 prints under 2.5 |
| Slot | (0, 2), 6 long | 0.9 wide through | TONGUE_SLOT height (0.9) and the 0.4 tongue clearance |
| Slot | (0, 4), 6 long | 0.4 wide through | Whether a 0.4 gap prints open: CLEAR_FIT and the 0.4 rigid-pair nominals (plan §3.6) |
| Rib | along x at y −0.5 | 0.4 thick × 3 tall × 12 long | E4; the thin-feature floor under E1 (tongue 0.5) and E3 (nubs 0.8) |
