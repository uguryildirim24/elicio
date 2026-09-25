# Shell v2f — the wearable body on packing §5e (width 22)

This is a measured **v2 reference solid**, not a shell for the newer 18 mm v4
board (`board-v4-design.md`). Its J2/P5 hardware collision remains open; the
v4 board changes the cell connector and charging geometry and needs its own
built shell. Do not upload these v2 solids for a v4 build.

WP14 then WP14b then WP14c then WP14d then WP14e then WP14f. The plan is not
changed. Nothing is ordered. The body is provisional until Rolf
measures M1 (Q34) and approves the two renders.

Winner: `A_pack501012_series_w22_y8_iII_s3` (`packing-v2.md` §5e pin table v3
at `ab9ce95`; §5d is frozen history). Same order-1 construction path as
Stage B v2 (`STAGE = "shell"` adds wearable cuts; it is not a fork).
Overlay: `scripts/cad/params/shell_v2.toml`.
Solids and views: `docs/fab/cad/v2/`. Stage B v2 still uses packing C
at width 20 (`stageb_v2.toml`, no `STAGE=shell`).

WP11b on `lane/w3` at `284ec05` (`packing-v2.md` §5, table REF tab
route): no REF tab route stays inside the cavity. Q59 is the slot
`REF_end_wall_slot`: u 7.25–9.75 (centre 8.50), s 38.20–39.25,
y 1.50–1.81, width 2.50, through 1.05, height 0.31, rectangular volume
0.814 mm³. This shell cuts that box plus 0.20 mm flex clearance per side
in u, 0.20 mm in s, and 0.15 mm in y. The live `V2_BOSS_sites` and `V2_CHARGE_pads` read §5e at `ab9ce95`
from this repository; §5d at `e4b857c` is retained only for older
placement readers. No other worktree is consulted.

Rebuild:

```bash
.venv/bin/python scripts/cad/bte_fit_shell.py --params scripts/cad/params/shell_v2.toml --stage shell --out docs/fab/cad/v2/
.venv/bin/python scripts/cad/render.py --out docs/fab/cad/v2/
.venv/bin/python scripts/cad/manifest.py --check-bytes docs/fab/cad/v2/manifest.json
```

## 1. What the body is

A behind-the-ear PA12 shell, **22 mm wide**, LID_Y 8.0, BODY_THICK 9.0,
BODY_ARC 48.4, TOTAL_CHORD 47.90. Cavity u 1.50–20.50, island (board
zone) u 2.25–19.75 × s 16.00–37.60, 501012 pack in the pocket, rib s
14.90–15.70. The tail loft starts at s 45.5. P4/P5 are not on the tail.

The medial face is the skin face: three ISO 7380 M2.5×4 titanium EMG
heads (SIG1, SIG2, REF) and the concealed closure well only. Charging
heads P4/P5 face +u on the posterior wall, away from skin. The
titanium head is the dome; the print has only the Ø2.7 hole (plan v1 §4:
only the gauge prints domes; review r7 removed the nylon domes the lane
fused over the holes). Each EMG
screw goes through the 1.5 floor and a Ø2.7 hole, through a Ø5 ring-pad
on a flex tab, into a brass female hex standoff 5 AF and 3.0 mm tall.
The standoff sits in a printed hex collar on the floor. The flex board
rests on the standoff tops (underside y 4.81, top y 5.32). Two printed
bosses at §5e H1 (13.23, 17.70) and H2 (17.95, 17.70) stop 0.5
below those tops so the board lands on the standoffs first.
`V2_BOSS_sites` reads those sites from the packing table (no hard-coded
coordinates). Each island boss and the tail closure boss carries a CAD
pilot Ø2.10 and OD ≥ 5.0 (L8 §4). The lid closure boss is the same
rule. The 3.30 keep box around each hole is
clear of every courtyard; the H1/H2 keep-out gap is 1.42.

SIG1 and SIG2 are neck-end strips (Q83): floor channels from the rings
to island s 16.00, lengths 10.71 mm and 21.81 mm as packing states.
Side walls at those s stations stay 1.50 (no side-wall pockets). REF
still uses `REF_end_wall_slot`. The old rib slot and drop channel are
not cut: the charge tab now folds 90° onto the posterior wall from the
pocket island's high-u edge (§5e).

P4 (20.50, 4.35, y 4.35) and P5 (20.50, 12.35, y 4.35) use open Ø2.7
holes through the posterior wall u 20.50–22.00. Titanium heads face +u;
Ø5 ring pads sit on the inner face and are clamped in 5.30 AF hex wells
with printed collars 3.0 mm into the bay. The P5 collar is trimmed only
where it would intersect the island board thickness, y 4.81–5.32.
Built-solid checks measure 3.4448 mm of remaining u-direction nylon
at the eligible seat offset samples (excluding sections through the
solid end wall or rib), 3.00 mm between head edges, 3.10 mm to the
cell pocket, and zero board-zone nylon. The end wall and the skin face
have no charging holes. There is no USB opening.
`V2_USB_end` is NOT_APPLICABLE by name: "Q81: no receptacle at M1 52".

The 501012 pack sits in the pocket in series with the board, foam 0.5
on the lid face. The recovery switch is under a blind 0.5 recess in
the lid, no hole. There is no text on the outside. The lid-screw head
well is on the medial tail (skin hides it). The lateral lid and body
have no well.

The hook starts as a circular root (r 1.75), then lofts to 4.4 × 3.0
and to a 3.0 × 2.2 tip (Q76). Radius from M8 (HOOK_RADIUS on the
default set). The tube-to-body joint fillet 1.5 builds. The tail is
the delayed loft plus the REF dome (Q17, provisional).

## 2. Closure (measured, Q89): lid boss and M2.5×8

No snaps. The v2f build remeasured the Q89 joint on the current §5e
body and lid; moving P4/P5 to the posterior wall did not change this
closure. A hinge lip in the hook-end wall plus one concealed ISO 7380
M2.5×8 titanium button-head screw on the medial tail (u 16.50, s 41.00).
The head sits in the Ø5.0 well at y 1.55. A lid boss drops 3.2 mm from
the lid underside (y 8.00) into a tail pocket. The screw passes the
body's tail boss and threads into the lid boss. The lateral lid is not
cut; a closed outer pad keeps the tip inside nylon. E1 tongue/web is
omitted (Q28). `V2_CLOSURE` and `V2_LATERAL_unbroken` measure the built
lid and body. `V2_BOSS_pilot` measures the tail boss, the lid boss, and
the two island bosses (L8 §4: CAD pilot Ø2.10, boss OD ≥ 5.0, radial
wall ≥ 1.4).

| Number | Measured |
|---|---:|
| Body nylon over the lip (undercut) | yes (1) |
| Lid lip in the groove | yes (1) |
| Screw engagement in the tail boss (off-axis, to the pocket) | 3.15 mm |
| Screw tip (head at the well bottom y 1.55, M2.5×8) | y 9.55 |
| Lid-boss underside (`lid_underside_y`) | y 4.80 |
| Screw thread in the lid (`lid_engagement`) | 4.75 mm |
| Boss wall beside the Ø2.10 pilot (`V2_CLOSURE`, +u) | 4.45 mm |
| Screw well air on the medial face | yes (1) |
| Lateral lid pits | 0 (`V2_LATERAL_unbroken`, 19 samples) |
| Lid-boss wall nylon / closed outer pad | yes (1) / yes (1) |
| Tail CAD pilot / wall / OD (`V2_BOSS_pilot`) | Ø2.10 / 3.92 / 9.94 |
| Lid CAD pilot / wall / OD | Ø2.10 / 1.45 / 5.00 |
| Island boss 1 CAD pilot / wall / OD | Ø2.10 / 1.45 / 5.00 |
| Island boss 2 CAD pilot / wall / OD | Ø2.10 / 2.40 / 6.90 |

The hinge groove is s 1.00–1.48, y 7.25–7.70, u 7.5–14.5 (centred on
width 22). That leaves 1.00 mm of outer end wall and 0.30 mm of body
nylon over the lip, so the lid cannot lift straight off. The screw
head sits in a Ø5.0 well through the medial floor at u 16.50, s 41.00
(clear of the Ø7.5 REF pocket at 8.50, 43.00). A Ø2.10 pilot in a Ø5.0
boss on the floor meets a tail pocket; the lid boss drops 3.2 mm into
that pocket. The M2.5×8 is the standard length that puts 4.75 mm of
thread in the lid (3.2 mm of hanging boss plus the plate and a closed
outer pad so the tip at y 9.55 stays in nylon). The ×8 length needs
sourcing and Rolf's explicit approval; none has been ordered. S4 two-finger
pull and 0.5 m drop stay
**qualitative** (plan v2 §7). Insertion and retention forces stay
**NOT_MEASURED** until a printed PA12 part is in the hand.

## 3. Contact joint — what G7 needs from the shell

Interface II (`board-v2.md` §11). Datum chain, medial face y = 0 up:

| Datum | y | Source |
|---|---:|---|
| Medial outer face | 0.00 | body frame |
| Floor inner face (WALL_MEDIAL) | 1.50 | plan v2 §3 |
| Ring pad top (PI 0.11 + FR4 0.2) | 1.81 | `packing-v2.md` §5, review r5. The board Gerber draws no ring FR4 (decision 72) |
| Standoff top / board underside | 4.81 | standoff 3.0 (Q43, Q58) |
| Board top | 5.32 | flex 0.51 at parts |
| Boss top | 4.31 | 0.5 below the standoff tops |
| Lid underside | 8.00 | LID_Y, lofted plate |
| Lid rim | 9.25 | SHELL_LID_RIM_T 1.25 |
| Lid crown | +0.90 at mid-s, 0 at the rim | fades in u and s (plan v2 §7) |

Pocket, seat, hole:

| Feature | Number | Notes |
|---|---|---|
| Brass standoff | 5 AF, female M2.5, h 3.0 | Spacer Express 3.0; Harwin R25-1000402 4.0 is listed, not fitted |
| Printed hex collar | AF 8.4 outside, 2.0 from the floor | 1.0 wall around the Ø6.4 ring seat at its base, 1.55 at the flats above it |
| Printed well | AF 5.30, measured 5.30, corners r 3.06 | Fit: 5.30 − 0.3 ≥ 5.00. Lock: 5.30 + 0.3 = 5.60 < 5.77 across corners |
| Ring seat | Ø6.4, measured 6.4 | Flex ring outline Ø6.0 + 0.10 FPC outline + 0.3 print |
| Ring pad | Ø5.0, hole Ø2.7 | ENIG, both copper layers |
| Screw | ISO 7380 M2.5 × 4, Grade 5 titanium | Head Ø4.7, h 1.35 (bought; the only dome) |
| Through-hole in the 1.5 wall | Ø2.7 | Open at the skin face; `V2_RING_seat` face_open |
| Tab strip | 2.5 × 0.31, neck-end | SIG1 10.71 mm, SIG2 21.81 mm to island s 16.00; REF uses `REF_end_wall_slot` |
| Charging pads (Q90/Q93) | P4 (20.50, 4.35, y 4.35), P5 (20.50, 12.35, y 4.35) | Ø2.7 open through posterior wall, +u titanium heads, RING_PAD Ø5 on inner face in a clamped 3.0 standoff; `V2_CHARGE_pads` |
| Print tolerance | ±0.3 mm under 100 mm | JLC PA12-HP page, plan v2 §12 (2026-07-30) |
| Placement on the printed floor | ±0.3 | `packing-v2.md` |

Path: skin → titanium head → screw → standoff (clamping the ring) →
board island on the standoff tops.

Bend on the tabs: packing R ≥ 1.0; this board states R = 1.5
(`board-v2.md` §11). Strain relief and assembler flex rules stay on the
board package.

## 4. §7 checklist (measured on this solid)

Build exit 0. `stage_b_failing` is empty. This only clears shell checks:
`V2_CAVITY_v3` checks pin centres, not assembled hardware clearance; its
J2/P5 overlap is still open. `V2_USB_end` is NOT_APPLICABLE by name
(Q81: no receptacle at M1 52) and does not fail the build.

| Item | Answer | Check / number |
|---|---|---|
| Stranger's glance: no lateral screws | Pass on the drawing. Three EMG heads and the tail well on the medial face; P4/P5 only on the posterior side wall. `V2_LATERAL_unbroken` reports no lid pit | renders, `V2_LATERAL_unbroken` |
| No text outside | Pass. Stage B emboss is skipped when `STAGE=shell` | notes.emboss |
| Nothing else through the skin | Pass. The v1 bench-cable exit and REF wire channel are not cut on the shell | `CABLE_EXIT_cavity` NOT_MEASURED, wall_closed 1 |
| Seam ≤ 0.3 | NOT_MEASURED. Lid inset 0.15 laps the wall tops; print and close at S4 | — |
| No planar facet over 3 mm | Pass. Lofted lid, 0 of 7 stations flat; min rise over 3 mm 0.025 | `V2_EDGE_radii` flat_stations 0 |
| Outside edges R ≥ 1.0 | Pass. Rim R 1.05 measured on the solid (3-point fit on the outer profile) | `V2_EDGE_radii` lid_rim_R 1.05 |
| Medial face flat, R0.5 | Pass. FILLET_MEDIAL 1.5 applied on the outline; the face is the floor | FILLET_MEDIAL |
| Closure | **Pass.** Hinge undercut 1; M2.5×8 from the well (tip y 9.55) into a lid boss (underside y 4.80); `lid_engagement` 4.75; boss wall 4.45; well on the medial tail | `V2_CLOSURE` |
| Lateral lid unbroken | Pass. 0 pits in 19 samples; lid-boss wall nylon; outer pad closed | `V2_LATERAL_unbroken` |
| Boss pilots Ø2.10, OD ≥ 5.0, wall ≥ 1.4 | Pass. Tail Ø2.10 / 3.92 / 9.94; lid Ø2.10 / 1.45 / 5.00; island 1 Ø2.10 / 1.45 / 5.00; island 2 Ø2.10 / 2.40 / 6.90 | `V2_BOSS_pilot` |
| Bosses at §5e hole sites | Pass. H1 (13.23, 17.70), H2 (17.95, 17.70); keep-out gap 1.42; checked against §5e courtyards | `V2_BOSS_sites` |
| Neck-end tabs, no side pockets | Pass. SIG1 10.71, SIG2 21.81; side walls 1.50; channels air; old rib slot and drop channel no longer cut | `V2_TAB_envelope` |
| Posterior-wall charging contacts | Pass. P4/P5 Ø2.7 through holes, outer faces open, no caps; u-wall around each 3.4448, nylon between heads 3.00, cell gap 3.10, hinge gaps 3.5422 / 9.0811 | `V2_CHARGE_pads`, `V2_WALL_minima` |
| Hook circular root, ellipse, fillet, M8 radius | Circular root r 1.75, then 4.4 × 3.0 / 3.0 × 2.2. Joint fillet 1.5 applied. Radius from default HOOK_RADIUS | assemble_shell, Q76 |
| Tail blended, REF dome | Delayed tail loft from s 45.5; REF dome on the tail (Q17 provisional) | Q17 |
| Colour | NOT_MEASURED. Grey or dyed black is Q30 | Q30 |
| USB ligament ≥ 1.5 to the hook | NOT_APPLICABLE. No receptacle at M1 52 | `V2_USB_end` |
| USB receptacle recessed ≥ 1.0 | NOT_APPLICABLE. Same row | `V2_USB_end` |
| Wall ≥ 1.0 at slot and ligaments, ≥ 1.5 elsewhere | Pass. Hinge outer wall 1.00; side walls 1.50; floor under REF slot 1.50; posterior seat offset samples 3.4448; flex clearance 0.20 per side in u (slot width 2.90) | `V2_WALL_minima` |
| Captive standoff | Pass. 5 AF prism holds no nylon; wells AF 5.30 | `V2_STANDOFF` |
| `V2_TAB_envelope` | Pass. REF_body_mm3 0, SIG1 0, SIG2 0 | `V2_TAB_envelope` |
| `REF_WIRE_envelope` | Pass. body_mm3 0, lid_mm3 0 | `REF_WIRE_envelope` |
| Island board envelope | Pass. P5 collar trimmed at board zone; body_mm3 0, lid_mm3 0 (was 0.0467) | `V2_BOARD_envelope` |
| §5e cavity | Pin centres declared inside or exterior; J2 inside at (15.15, 11.35), but its courtyard overlaps the P5 well by 4.93 mm. Not an assembly fit claim | `V2_CAVITY_v3` |

Matte / vapour smoothing is a finish on the order, not this solid.

| Before (paused WP14f trial) | After (v2f built solid) |
|---|---|
| `V2_CHARGE_pads` and `V2_WALL_minima`: P4/P5 `wall_around` −1.0 (probe had no boundary) | Both pass: 3.4448 mm at each seat; inner probe now starts in the cavity beyond the hex collar; sections through the solid end wall and rib are excluded |
| `V2_BOARD_envelope`: 0.0467 mm³ nylon at P5 collar | Pass: 0.0000 mm³ after trimming the collar at the board zone |
| `V2_CAVITY_v3`: J2/P5 well gap −4.93 mm | Still −4.93 mm; a packing decision is needed before assembly |
| Q89-era committed solids showed medial floor P4/P5 | New solids cut wall P4/P5; skin-face pads, rib slot and drop channel absent |

## 5. What Rolf must approve

The two renders in `docs/fab/cad/v2/`:

- `render_medial.png` — skin face with three titanium EMG heads and the
  medial-tail screw well; an edge-on posterior view shows the side-wall
  P4 VBUS and P5 GND heads (drawn hardware, not nylon).
- `render_lateral.png` — lofted lid, circular-root hook, hinge at the
  hook-end wall, closed pad over the lid boss, unbroken lateral face.
  No USB opening.

One drawing page `drawing.pdf` in the v1 sheet style. His yes is the
gate before any shell order (plan v2 §7). Nothing is uploaded.

## 6. Checks named NOT_MEASURED or NOT_APPLICABLE

| Check | Reason |
|---|---|
| `TAB_envelope_air` | v1 TE 31428 envelope; see `V2_TAB_envelope` |
| `V2_USB_end` | NOT_APPLICABLE: Q81: no receptacle at M1 52; hook-end wall left solid |
| `V2_USB_medial` | NOT_APPLICABLE: same Q81 reading |
| `V2_ADJUSTMENT` | Region ±0.80 from pad vs hex vs JLC ±0.3; G5/G7 |
| `V2_HARNESS` | 100 ± 3 mm cell leads, not a solid |
| `V2_RECESS` | 0.5 floor recess is not on this solid (winner recess 0) |
| S4 pull and drop | Qualitative (plan v2 §7); needs a printed PA12 part in the hand |
| `CLOSURE_PASSED` | v1 E1 flag; the shell's closure row is `V2_CLOSURE` |
| `KEEPOUT_SIGNAL_air`, `KEEPOUT_REF_air` | v1 TE and lug keep-outs; interface II puts the hex collars there (`V2_STANDOFF`, `V2_RING_seat`) |
| `CABLE_EXIT_cavity` | No bench cable on the shell |

`antenna_body_mm3` 3.75 is nylon in the RF no-copper prism. That keep-out
is no copper, not air; the check reports it and does not fail.

## 7. Needs a decision

Review r6 moved these to `tasks/reviews/code-r6.md` (decisions 69 on).
Still open from the lane: M1 (Q34), colour (Q30), Q17 REF dome, the S4
pull and drop, standoff 3.0 vs Harwin 4.0 (a parameter change, not a
fork). Q59 is closed as the slot. Q81 is built: no USB opening. The Q86
floor pads, rib slot and drop channel were superseded by the Q90 posterior
wall pads; none is cut on this solid. Q89 is built: lid boss into a tail
pocket, M2.5×8, `V2_CLOSURE` passes.
Q82, Q83, Q90 and Q93 are built on this solid. The posterior pad heads
are not bare on the skin face. L8 lists titanium button lengths 4 mm and
6 mm; the closure geometry uses ×8, which has not been sourced or approved.
**Packing decision:**
§5e J2's 5.80 × 6.56 courtyard at (15.15, 11.35) overlaps the P5
standoff's 3.0 × 5.30 hex-well box by 4.93 mm (`V2_CAVITY_v3`). Moving
or reorienting J2/its tab is a packing/board change; the shell alone
cannot make the connector clear while keeping the pinned wall seat.
Do not order or claim assembly fit until that collision is resolved.
The render stamp is the manifest commit that built the solids.
