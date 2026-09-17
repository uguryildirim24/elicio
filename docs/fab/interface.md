# Elicio earpiece — mechanical interface

Version **1**. Date 2026-09-16. Plan revision 5, commit `0c5d0eb`.

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
SKU is 4.5 / 1.5, this file becomes v2.

### 2.3 Stack above the floor

Floor of the cavity is y = 1.5. The stack sits on that floor. Order
from the floor: lug, nut, screw tip, Kapton disc.

| Layer | Height | y span (full body) | Unit | From |
|---|---|---|---|---|
| Cavity floor | – | 1.50 | mm | plan §3.3 CAVITY |
| Ring lug | 0.50 | 1.50–2.00 | mm | plan §3.3, §4. See note D2 |
| Thin nut | 1.60 | 2.00–3.60 | mm | plan §4 DIN 439; ISO 4035 M2.5 m max 1.6, s max 5, e min 5.45, read 2026-09-16 at https://www.fasteners.eu/standards/iso/4035/ |
| Screw tip past nut | 0.40 | 3.60–4.00 | mm | plan §3.3, §4; 4.0 − 1.5 − 0.5 − 1.6 = 0.4 |
| Kapton disc | 0.13 | 4.00–4.13 | mm | plan §3.3, §4. See note D3 |
| Metal stack (lug+nut+tip) | 2.50 | 1.50–4.00 | mm | plan §3.3 CONTACT_STACK |
| Total above floor | 2.63 | 1.50–4.13 | mm | plan §4; 2.50 + 0.13 |
| Keep-out top | – | 4.13 | mm | plan §3.3 KEEPOUT_SIGNAL |

Note D2. Plan §8 row 9 assigns the 0.5 mm lug thickness and tab ≤ 7 mm
to WP5. Catalog #4 / M2.5 ring lugs read on 2026-09-16 are thicker:
Molex 0193230001 0.71 mm, TE 34157 0.79 mm. **UNVERIFIED** until WP5
shows a catalog drawing with thickness ≤ 0.5 mm and tab ≤ 7 mm. A
thicker lug raises the stack and this file becomes v2.

Note D3. DuPont Kapton 500HN is 5.00 mil, 127 µm nominal, tolerance
122–130 µm (QE-10167, https://www.qnityelectronics.com/content/dam/electronics/amer/us/en/electronics/public/documents/en/QE-10167-Kapton-General-Specifications.pdf,
read 2026-09-16). Plan 0.13 mm is the rounded top of that band.

Do not use ISO 4032 for this nut. ISO 4032 M2.5 is a style-1 nut,
m max 2.00 mm (https://www.fasteners.eu/standards/ISO/4032/, read
2026-09-16). That nut adds 0.40 mm and the stack top would sit at
y 4.53, into the board. The brief named ISO 4032; the plan names
DIN 439 / ISO 4035. The plan wins.

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
| Signal lug tab, CONTACT_1 | Box on the floor, toward its pad | 3 × 7 × 1.5; from the cylinder toward pad (5.9, 26.5) | mm | plan §3.3 |
| Signal lug tab, CONTACT_2 | Box on the floor, toward its pad | 3 × 7 × 1.5; from the cylinder toward pad (5.5, 30.0) | mm | plan §3.3 |
| Copper-free margin | Extra 0.5 around each signal keep-out and tab, on the board | 0.5 | mm | plan §5 |
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
| LEAD_PADS (candidates) | Three pads, medial board copper | (u, s) = (5.9, 26.5), (5.5, 30.0), (4.0, 29.0) | mm | plan §3.3; final positions interface v2 (plan §10 item 7) |
| Reference pad | The (4.0, 29.0) candidate | Route: pocket → channel → under the board at y 2.5–4.1 → pad | mm | plan §5 |
| Strain wrap | One Kapton wrap to the floor | at s 37 | mm | plan §5 |
| CABLE_EXIT | Cylinder through the posterior side wall (high-u wall) | Ø2.0 at s 36, y 3; plugged in Stage B | mm | plan §3.3, §5, §6 |

Pad rule: each pad sits on the medial side of the board, outside
keep-outs plus 0.5 mm and outside the antenna no-copper zone. Each
pad feeds its own 220 kΩ resistor and clamp within 10 mm (L4 §5.1,
plan §4). Those resistors are schematic, not this file.

## 5. Cell envelope

The cell is a 501015-class pouch. WP6 names the SKU and freezes
maximum dimensions (plan §8 row 12, §10 item 2). Until then the
pocket is sized for the plan's maximum body.

| Feature | Value | Unit | From |
|---|---|---|---|
| Class | 501015, 50 mAh, 3.7 V | – | plan §1, §5; L4 §1.4 |
| Cell body maximum | 5.2 thick × 10.4 wide × 15.6 long | mm | plan §3.3, §5 |
| Nominal class size | 5.0 × 10.0 × 15.0 | mm | 501015 name; DNK 501015 drawing L = 15, W = 10, T = 5, https://www.fpbattery.com/wp-content/uploads/2024/06/fpbattery-501015-3.7V-50mAh-Lithium-Polymer-Battery-Specification.pdf, read 2026-09-16 |
| Pack with PCM in-line | 17 ± 1 long in that DNK drawing (BL) | mm | same datasheet. Does not fit the pocket unless the PCM is folded |
| PCM | Folded on the lateral face of the cell, under Kapton; tabs toward the rib | – | plan §5 |
| BATTERY_POCKET | s 1.5–17.5, u 3.1–13.9, y 1.5–7.5 | mm | plan §3.3 |
| Pocket size | 16.0 × 10.8 × 6.0 | mm | plan §5 |
| Foam under the lid | 0.5 | mm | plan §5 |
| Cell identity | Left for WP6 | – | plan §8 row 12, §10 item 2 |

A vendor max of 5.2 × 10.5 × 17.5 (VCELL VP501015, read 2026-09-16 at
https://www.vcellpower-battery.com/3.7v/501015-3-7v-50mah-lithium-polymer-battery-.html)
does not fit this pocket if the PCM stays in line. WP6 must pick a
cell whose folded pack is ≤ 5.2 × 10.4 × 15.6 in the pocket axes, or
this file becomes v2.

## 6. Board

The board is out of scope for layout. This section is the envelope
WP6 must meet or raise as interface v2.

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
CONTACT_1 (u 5.9, s 22.0). KEEPOUT_SIGNAL radius is 3.55 mm, so the
nominal gap is 0.09 mm. WP2 must check this pair. The 0.5 mm
copper-free margin around the keep-out does overlap that pad in plan
view; the pad is nylon support, not copper.

### 6.2 Heights by zone

| Zone | Allowed height | y span (full, board at 4.3–5.3) | Unit | From |
|---|---|---|---|---|
| Over KEEPOUT_SIGNAL | Air only to y 4.13; board underside at 4.3 (gap 0.17) | 1.5–4.13 keep-out, 4.3 board | mm | plan §3.3, §5 |
| Medial components | ≤ 1.2, not over keep-outs or the RF zone | 3.1–4.3 | mm | plan §5 |
| Board core | 1.0 | 4.3–5.3 | mm | plan §5 |
| Lateral, module | 2.3 max | 5.3–7.6 | mm | plan §5; 4.3 + 1.0 + 2.3 = 7.6 |
| Under the lid | Lid underside at 8.0; 0.4 remains above the module | 7.6–8.0 | mm | plan §5 |
| Thin body | Same stack does not fit under LID_Y = 6.0 | – | plan §5: 9.0 mm is a design value until WP6 |

### 6.3 RF zone

Module: Raytac MDBT50Q-1MV2, chip antenna.

| Feature | Value | Unit | From |
|---|---|---|---|
| Nominal module | 15.5 × 10.5 × 2.05 | mm | Raytac Spec L, https://www.raytac.com/download/index.php?index_id=43, and product page https://www.raytac.com/product/ins.php?index_id=24, read 2026-09-16; plan §8 row 10 verified by `pro` |
| Width max on Spec K/L table | 10.5 + 0.2 = 10.7 | mm | SparkFun Spec K table, https://cdn.sparkfun.com/assets/4/7/4/3/8/_nRF52840__MDBT50Q-1MV2___MDBT50Q-P1MV2_Ver.K_spec.pdf, read 2026-09-16 |
| Reserved max (this interface) | 15.8 × 10.8 × 2.3 | mm | plan §5 (tolerance, solder, shield) |
| Placement | Lateral side of the board; antenna end at the inferior board edge (high-s) | – | plan §5 |
| Battery separation | ≥ 5 from the battery | mm | plan §5 |
| No-copper rule | No ground or copper on any layer in the antenna's corresponding area; make that area as wide as the PCB allows; put the module on the PCB edge | – | Raytac Spec L §2.3, read 2026-09-16 |
| Overlap | The antenna no-copper zone overlaps KEEPOUT_SIGNAL of CONTACT_2 | – | plan §5 |
| Exact polygon | **UNVERIFIED** | mm | Spec L §2.3 is a drawing. WP6 traces that drawing into copper. Do not invent millimetres |

Until WP6 traces the drawing, treat the inferior end of the module
footprint, full module width, on every layer, as no-copper, and keep
that zone off the three lead pads.

### 6.4 Where the ADS1292 and the charger may sit

| Part | Package | Body / courtyard | Height | Side | Rule | From |
|---|---|---|---|---|---|---|
| ADS1292 | TQFP-32 (PBS) | Body 5.00 × 5.00; TI package size 7 × 7 | 1.0 typ, 1.2 max | Medial (height = the 1.2 cap) | Entire 7 × 7 courtyard outside keep-outs + 0.5 and outside the RF zone | TI ADS1292 datasheet rev C, https://www.ti.com/lit/ds/symlink/ads1292.pdf, read 2026-09-16; plan §5, §8 row 11 |
| ADS1292 VQFN option | VQFN-32 (RSM) | Body 4.00 × 4.00; TI package size 4 × 4 | 1.0 max | Medial | Same keep-out rule; this is the "smaller front end" escalation | same datasheet |
| Charger | TI BQ25100 YFP DSBGA-6 | 1.60 × 0.90 | 0.5 class | Either; prefer superior, toward the rib, for short battery leads | Not in the RF zone; not over keep-outs | TI BQ25100, https://www.ti.com/lit/gpn/BQ25100A, read 2026-09-16; L4 §1.4; plan packing 7 mm² for charger + LDO |
| Charge pads | On the board, inside the cavity | – | – | Reached with the lid off | No skin-side port | plan §2 item 16, §5, §6 |
| Clamps | Three SOT-23 (BAV199 class) | Body max 3.0 × 1.4 × 1.1; packing uses 10 mm² each | ≤ 1.2 | Medial, within 10 mm of each pad | Each contact's own clamp | Nexperia BAV199, https://assets.nexperia.com/documents/data-sheet/BAV199.pdf, read 2026-09-16; L4 §5.1; plan §5 |

The module takes most of the lateral face (15.8 × 10.8 on a 19.0 × 12.5
board). The ADS1292 and the charger therefore share the medial face
with the keep-outs, the lug tabs, and the three pads.

## 7. Insulation and safety (mechanical)

These are shell and stack rules. The schematic (three series resistors
and clamps) is not this package.

| Rule | Mechanical reservation | From |
|---|---|---|
| Kapton on each stack | 0.13 disc on top of nut and tip; signal tabs on the floor under Kapton; reference tab upright in the pocket | plan §4, §5, §6 |
| Three separately protected paths | Each contact reaches the board only through its own lug, insulated lead, pad, resistor, and clamp. No pre-resistor conductor may touch the battery, the charge pads, or other copper | plan §6; design record requirement 4 |
| Only insulated wire leaves the reference pocket | Bare tab stays in KEEPOUT_REF | plan §3.3, §5 |
| Board medial copper | Solder-mask except the three lead pads | plan §5 |
| No charging port | No skin-side connector. Charge pads inside the closed cavity, lid off | plan §5, §6 |
| Never charge while worn | Procedural, on the assembly sheet | plan §6; design record requirement 3 |
| CABLE_EXIT | Ø2.0 for tethered bring-up only; plugged before wear in Stage B | plan §5, §6 |
| Tethered bring-up | Laptop on battery, not mains | plan §6; design record requirement 3 |
| Skin materials | PA12 (natural grey) and titanium only | plan §4, §6 |
| Cleaning | 70 % isopropanol wipe; nothing on the skin side but titanium and nylon | plan §4, §6 |

## 8. Packing budget

Board area 19.0 × 12.5 = 237.5 mm², quoted 237 in plan §5. Heights
are in §6.2. 9.0 mm body thickness is a design value until WP6
confirms it (plan §5).

### 8.1 Area at maximum datasheet dimensions

| Item | mm² | From |
|---|---|---|
| Board | 237 | plan §5 |
| Minus keep-out 1 on the board | 49 | plan §5 (Ø7.1 reserved as ≈ 7 × 7) |
| Minus keep-out 2 ∪ antenna zone | ≈ 68 | plan §5 |
| Minus rim | ≈ 15 | plan §5 |
| Available | ≈ 105 | plan §5 |
| ADS1292 TQFP-32 courtyard | 49 (7 × 7) | plan §5; TI package size 7 × 7, read 2026-09-16 |
| Three SOT-23 clamps | 30 | plan §5 |
| Charger and LDO | 7 | plan §5 |
| About 25 passives 0402 | 25 | plan §5 |
| Required | ≈ 111 | plan §5 |
| Shortfall | ≈ 6 | 111 − 105 |

Feasible only with tighter courtyards or a diode array. WP6 decides
(plan §5). Rolf chooses the escalation (plan §10 Open for Rolf item 6).

### 8.2 Escalation options (plan §10 interface item 1)

| Option | What changes | Area it buys | Height / fit | From |
|---|---|---|---|---|
| A. Fits as drawn | Tighter courtyards, or one diode array in place of three SOT-23 (30 mm² → about 8 mm², about +22 mm² effective) | About +22 mm² if the array is used; enough to cover the 6 mm² shortfall | No shell change | plan §5 |
| B. Longer | Board length +3.5 mm → 22.5 × 12.5 = 281 mm² | +44 mm² board; available about 149 against 111 required | Cavity length 36.7 → 40.2; BODY_ARC grows about 3.5; M1 gate moves. WP2 re-runs | plan §10 item 1 |
| C. Wider | Board width +3.0 mm → 19.0 × 15.5 = 295 mm² | +57 mm² board; available about 162 against 111 required | BODY_WIDTH 17 → 20; cavity 14 → 17. Covertness. WP2 re-runs | plan §10 item 1 |
| D. Smaller front end | ADS1292 VQFN-32 4 × 4 (16 mm²) instead of TQFP 7 × 7 (49 mm²) | +33 mm²; required drops to about 78 against 105 available | Medial height still ≤ 1.2 | TI datasheet RSM package; plan §10 item 1 |

Options B and C are interface v2 and a second gauge if thickness or
width changes (plan §7 order 1 rework). Option D is a WP6 parts
choice and stays on this shell if the courtyards fit.

## 9. Version notes (plan vs brief vs design record)

The plan wins. These are not silent CAD changes.

1. The WP1 brief names ISO 4032. The plan names a DIN 439 / ISO 4035
   thin nut, m = 1.6 mm. ISO 4032 M2.5 is m = 2.0 mm and does not fit
   the y 4.13 keep-out. This file follows the plan.
2. The design record allows stainless or carbon-TPU on skin. The plan
   allows titanium only. This file follows the plan.
3. L3 recommended 7–9 mm floating domes. The plan uses rigid ISO 7380
   M2.5, 4.7 mm. This file follows the plan. A different contact size
   is interface v2 (plan §10 item 5).
4. L4 placed charging pads on the skin-side face. The plan puts pads
   inside the cavity, lid off. This file follows the plan.
5. L4's module number is 15.5 × 10.5 × 2.05. This file reserves the
   plan's 15.8 × 10.8 × 2.3 maximum.

## 10. UNVERIFIED list

| # | Claim in this file | What would verify it | Owner |
|---|---|---|---|
| 1 | Dome Ø4.7, crown 1.35 | WP5 SKU drawing. ISO 7380-1:2022 has no M2.5 row; catalog M2.5 is 4.5 / 1.5 | WP5 |
| 2 | Lug thickness 0.5, tab ≤ 7 | WP5 catalog drawing | WP5 |
| 3 | Assembled lug + nut + Kapton inside Ø7.1 | WP5 stack on catalog drawings; plan §9 WP5 acceptance ≤ 2.63 | WP5 |
| 4 | Cell body ≤ 5.2 × 10.4 × 15.6 with PCM folded | WP6 named cell drawing | WP6 |
| 5 | RF no-copper polygon in millimetres | WP6 trace of Raytac Spec L §2.3 | WP6 |
| 6 | Lead pad (u, s) values | Interface v2 after WP6 placement | WP6 |
| 7 | Channel opening 0.94 mm at bow 3 | WP2 geometry report (plan §10 open item 4) | WP2 |
| 8 | 0.09 mm pad-to-keep-out gap at CONTACT_1 | WP2 keep-out check | WP2 |

## 11. Sources read (web, 2026-09-16)

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
| Raytac Spec L | https://www.raytac.com/download/index.php?index_id=43 | Module size, RF rules |
| Raytac Spec K | https://cdn.sparkfun.com/assets/4/7/4/3/8/_nRF52840__MDBT50Q-1MV2___MDBT50Q-P1MV2_Ver.K_spec.pdf | W max +0.2 |
| TI ADS1292 | https://www.ti.com/lit/ds/symlink/ads1292.pdf | 5 × 5 body, 7 × 7 package, 1.2 max height |
| TI BQ25100 | https://www.ti.com/lit/gpn/BQ25100A | 1.60 × 0.90 |
| Nexperia BAV199 | https://assets.nexperia.com/documents/data-sheet/BAV199.pdf | SOT-23 3.0 × 1.4 × 1.1 max |
| Kapton 500HN | https://www.qnityelectronics.com/content/dam/electronics/amer/us/en/electronics/public/documents/en/QE-10167-Kapton-General-Specifications.pdf | 0.127 mm, tol. 0.122–0.130 |
| DNK 501015 | https://www.fpbattery.com/wp-content/uploads/2024/06/fpbattery-501015-3.7V-50mAh-Lithium-Polymer-Battery-Specification.pdf | 15 × 10 × 5 cell, 17 ± 1 with PCM |
| VCELL 501015 | https://www.vcellpower-battery.com/3.7v/501015-3-7v-50mah-lithium-polymer-battery-.html | 5.2 × 10.5 × 17.5 max example |
| 28 AWG silicone | https://bntechgo.com/28-awg-silicone-wire-stranded-tinned-copper-wire-1-feet-11-colors-optional/ | OD 1.2 ± 0.1 |
