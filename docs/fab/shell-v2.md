# Shell v2 — the wearable body on the round 5 winner

WP14. The plan is not changed. Nothing is ordered. The body is
provisional until Rolf measures M1 (Q34) and approves the two renders.

Winner: `A_501015_series_w20_y8_iII_s3` (`packing-v2.md` §5–§6). Same
order-1 construction path as Stage B v2 (`STAGE = "shell"` adds the
wearable cuts; it is not a fork). Overlay:
`scripts/cad/params/shell_v2.toml`. Solids and views:
`docs/fab/cad/v2/`.

WP11b on `lane/w3` at `284ec05` (`packing-v2.md` §5, table REF tab
route): no REF tab route stays inside the cavity. The cavity ends at
s 38.20, the Ø7.5 tail pocket starts at s 39.25, and 1.05 mm of nylon
sits between them. Every searched path crosses that wall. Q59 is the
slot `REF_end_wall_slot`: u 7.25–9.75 (centre 8.50), s 38.20–39.25,
y 1.50–1.81, width 2.50, through 1.05, height 0.31, rectangular volume
0.814 mm³, containing the straight floor tab (8.50, 43.00) → (8.50,
36.80). This shell cuts that box plus 0.20 mm flex clearance per side
in u, 0.20 mm in s, and 0.15 mm in y (JLC PA12 ±0.3; FPC outline ±0.10
in `board-v2.md` §12). Stage B v2 (`stageb_v2.toml`, no `STAGE=shell`)
still builds without that slot. This branch does not merge `lane/w3`.

Rebuild:

```bash
.venv/bin/python scripts/cad/bte_fit_shell.py --params scripts/cad/params/shell_v2.toml --stage shell --out docs/fab/cad/v2/
.venv/bin/python scripts/cad/render.py --out docs/fab/cad/v2/
.venv/bin/python scripts/cad/manifest.py --check-bytes docs/fab/cad/v2/manifest.json
```

## 1. What the body is

A behind-the-ear PA12 shell, 20 mm wide, LID_Y 8.0, BODY_THICK 9.0,
BODY_ARC 48.4, TOTAL_CHORD 47.90. The medial face is the skin face: three
ISO 7380 M2.5×4 titanium domes stand on it (SIG1, SIG2, REF). Each screw
goes through the 1.5 floor and a Ø2.7 hole, through a Ø5 ring-pad on a
flex tab, into a brass female hex standoff 5 AF and 3.0 mm tall. The
standoff sits in a printed hex collar on the floor. The flex board rests
on the three standoff tops (underside y 4.81, top y 5.32). Two printed
bosses at (14.85, 21.50) and (14.85, 28.10) stop 0.5 below those tops so
the board lands on the standoffs first. Packing skipped both board-corner
bosses (they sat on SIG1 or the antenna); these two sit on the high-u
board edge. Review r6: the board (`board-v2.md` §11) has no
mounting holes, and the bosses sit under J3 and under the module, so no
board screw can go into them. The REF standoff (s 43.0) is past the
board's end (s 37.6); the board rests on two standoffs only. Retention
is decision 73 in `tasks/reviews/code-r6.md`.

The cell 501015 sits in the pocket in series with the board, foam 0.5 on
the lid face. USB-C opens on the hook-end end face (plan v2 §5.4
fallback; the medial face cannot hold the receptacle next to the cell).
Review r6: the packing places the receptacle at s −5.80 to 1.50, so its
mouth stands 4.8 mm outside the end face (outer face s −1.00), and the
hook fills the opening's anterior 0.89 mm. Neither closes on this body
(`V2_USB_end`, decision 70).
The recovery switch is under a blind 0.5 recess in the lid, no hole.
There is no text on the outside. The three contact heads are on the
medial face; no screw is visible from the lateral side.

The hook is an elliptical loft, 4.4 × 3.0 at the root and 3.0 × 2.2 at
the tip. Radius from M8 (HOOK_RADIUS on the default set). A 1.5 fillet
at the tube-to-body joint was requested; the script finds no
tube-to-top-face edge on this solid and leaves the joint sharp. The tail is the order-1 loft plus the REF dome (Q17,
provisional).

## 2. Closure (measured, review r6)

Choice by the lane: hinge lip in the tail plus two cantilever snaps on
the inner side walls over the board. E1 tongue/web is omitted (Q28).
No concealed tail M2.5.

The lane's calculation used L 8.0, t 1.0, y 0.5 (ε 0.0117). That beam is
not the one built. `V2_CLOSURE` now measures the built lid and body:

| Number | Anterior | Posterior |
|---|---:|---|
| Beam thickness (u) | 0.50 | 0.50 |
| Beam hang (y, free length) | 1.00 | 1.00 |
| Hook stand-out past the wall face | 0.18 | 0.18 |
| Strain 1.5·t·y/L² | 0.135 | 0.135 |
| Body nylon over the hook (undercut) | none | none |

The snap grooves run to lid_y + 0.15 and the lip groove to lid_y + 0.12,
so nothing of the body sits over any lid feature: the lid lifts straight
off. The beam is also under JLC's 1 mm wall (plan v2 §12), and the
0.75 mm between the module and the side wall has no room for a 1 mm
beam. A working closure is decision 71 (concealed tail screw per plan
v2 §7, or a different snap site).

Insertion and retention forces stay **NOT_MEASURED** (printed PA12 E and
a part in the hand, S4).

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
| Lid underside | 8.00 | LID_Y |
| Lid outer | 9.00 | LID_THICK 1.0, plus a Ø19 crown of 0.5 at s 22 |

Pocket, seat, hole:

| Feature | Number | Notes |
|---|---|---|
| Brass standoff | 5 AF, female M2.5, h 3.0 | Spacer Express 3.0; Harwin R25-1000402 4.0 is listed, not fitted |
| Printed hex collar | AF 8.4 outside, 2.0 from the floor | 1.0 wall around the Ø6.4 ring seat at its base, 1.55 at the flats above it |
| Printed well | AF 5.30, measured 5.30, corners r 3.06 | Fit: 5.30 − 0.3 ≥ 5.00 (Harwin "5.00 A/F MAX"). Lock: 5.30 + 0.3 = 5.60 < 5.77 across the standoff's corners. Review r6; the lane's AF 6.3 plus Ø7.4 was round and let the standoff turn |
| Ring seat | Ø6.4, measured 6.4 | Flex ring outline Ø6.0 (`board-v2.md` §11) + 0.10 FPC outline + 0.3 print |
| Ring pad | Ø5.0, hole Ø2.7 | ENIG, both copper layers |
| Screw | ISO 7380 M2.5 × 4, Grade 5 titanium | Head Ø4.6, h 1.5 (v1 dome) |
| Through-hole in the 1.5 wall | Ø2.7 | Dome on the outside |
| Tab strip | 2.5 × 0.31 | Channel in the floor from each ring to the board; REF uses `REF_end_wall_slot` (`packing-v2.md` §5 on lane/w3) plus 0.20 mm clearance per side in u |
| Print tolerance | ±0.3 mm under 100 mm | JLC PA12-HP page, plan v2 §12 (2026-07-30) |
| Placement on the printed floor | ±0.3 | `packing-v2.md` |

Path: skin → titanium dome → screw → standoff (clamping the ring) →
board island on the standoff tops.

Bend on the tabs: packing R ≥ 1.0; this board states R = 1.5
(`board-v2.md` §11). Strain relief and assembler flex rules stay on the
board package.

## 4. §7 checklist (measured on this solid)

Build exit 3. `stage_b_failing`: `V2_CLOSURE`, `V2_EDGE_radii`,
`V2_USB_end`, `V2_WALL_minima`. Each is a measured number, not a
constant (review r6).

| Item | Answer | Check / number |
|---|---|---|
| Stranger's glance: no lateral screws | Pass on the drawing. Three contact heads on the medial face are the skin seats, not lid screws | renders |
| No text outside | Pass. Stage B emboss is skipped when `STAGE=shell` | notes.emboss |
| Nothing else through the skin | Pass. The v1 bench-cable exit and REF wire channel are not cut on the shell | `CABLE_EXIT_cavity` NOT_MEASURED, wall_closed 1 |
| Seam ≤ 0.3 | NOT_MEASURED. Lid CLEAR_FIT is the order-1 plate inset; print and close at S4 | — |
| No planar facet over 3 mm | Fail. The crown is a Ø19 blister at s 22; 4 of 6 stations along the lid are flat over 3 mm | `V2_EDGE_radii` flat_stations 4 |
| Outside edges R ≥ 1.0 | Fail. Lid rim LID_EDGE 0.8. Hook joint left sharp | `V2_EDGE_radii` lid_rim_R 0.8 |
| Medial face flat, R0.5 | Pass. FILLET_MEDIAL 1.5 applied on the outline; the face is the floor | FILLET_MEDIAL |
| Closure | Fail. No undercut; beam 0.5 × 1.0, strain 0.135 | `V2_CLOSURE` |
| Hook elliptical, fillet, M8 radius | Axes 4.4 × 3.0 / 3.0 × 2.2. Joint fillet left sharp. Radius from default HOOK_RADIUS | assemble_shell |
| Tail blended, REF dome | Order-1 tail loft; REF dome on the tail (Q17 provisional) | Q17 |
| Colour | NOT_MEASURED. Grey or dyed black is Q30 | Q30 |
| USB ligament ≥ 1.5 to the hook | Fail. The hook reaches u 6.39 on the face; the opening starts at u 5.50 | `V2_USB_end` ligament_hook −0.89 |
| USB receptacle recessed ≥ 1.0 | Fail. Packing box s −5.80 to 1.50 against an outer face at s −1.00 | `V2_USB_end` mouth_recess −4.80 |
| Wall ≥ 1.0 at slot and ligaments, ≥ 1.5 elsewhere | Fail on the USB ligament only. Snap residual 1.10; side walls 1.5; floor under the slot 1.50; flex clearance 0.20 per side in u (slot width 2.90) | `V2_WALL_minima` |
| Captive standoff | Pass. 5 AF prism holds no nylon; wells AF 5.30 | `V2_STANDOFF` |
| `V2_TAB_envelope` | Pass. REF_body_mm3 0, SIG1 0, SIG2 0 | `V2_TAB_envelope` |
| `REF_WIRE_envelope` | Pass. body_mm3 0, lid_mm3 0 | `REF_WIRE_envelope` |

Matte / vapour smoothing is a finish on the order, not this solid.

## 5. What Rolf must approve

The two renders in `docs/fab/cad/v2/`:

- `render_medial.png` — skin face, three domes, tail, hook.
- `render_lateral.png` — lid, elliptical hook, USB on the hook-end face.

One drawing page `drawing.pdf` in the v1 sheet style. His yes is the
gate before any shell order (plan v2 §7). Nothing is uploaded.

## 6. Checks named NOT_MEASURED

| Check | Reason |
|---|---|
| `TAB_envelope_air` | v1 TE 31428 envelope; see `V2_TAB_envelope` |
| `V2_USB_medial` | Medial USB is not cut; hook-end fallback, see `V2_USB_end` |
| `V2_ADJUSTMENT` | Region ±0.80 from pad vs hex vs JLC ±0.3; G5/G7 |
| `V2_HARNESS` | 100 ± 3 mm cell leads, not a solid |
| `V2_RECESS` | 0.5 floor recess is not on this solid (winner recess 0) |
| Snap insertion / retention force | Needs printed PA12 E and a hand sample (S4) |
| Hook joint R ≥ 1.0 | 1.5 fillet requested; no tube-to-top-face edge found, left sharp |
| `CLOSURE_PASSED` | v1 E1 flag; the shell's closure row is `V2_CLOSURE` |
| `KEEPOUT_SIGNAL_air`, `KEEPOUT_REF_air` | v1 TE and lug keep-outs; interface II puts the hex collars there (`V2_STANDOFF`, `V2_RING_seat`) |
| `CABLE_EXIT_cavity` | No bench cable on the shell |

`antenna_body_mm3` 3.72 is nylon in the RF no-copper prism. That keep-out
is no copper, not air; the check reports it and does not fail.

## 7. Needs a decision

Review r6 moved these to `tasks/reviews/code-r6.md` (decisions 69 on).
Still open from the lane: M1 (Q34), colour (Q30), Q17 REF dome, snap
forces and the S4 pull and drop, standoff 3.0 vs Harwin 4.0 (a
parameter change, not a fork). Q59 is closed as the slot.
