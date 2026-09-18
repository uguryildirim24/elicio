# Shell v2 — the wearable body on the round 5 winner

WP14 then WP14b. The plan is not changed. Nothing is ordered. The body is
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
hook fills the opening's anterior 0.89 mm. WP14b leaves the hook-end
wall solid. `V2_USB_end` is NOT_MEASURED until packing §5b (Q70).
The recovery switch is under a blind 0.5 recess in the lid, no hole.
There is no text on the outside. The three contact heads are on the
medial face; the lid screw sits in a well at the tail, not as a
lateral screw.

The hook starts as a circular root (r 1.75), then lofts to 4.4 × 3.0
and to a 3.0 × 2.2 tip (Q76). Radius from M8 (HOOK_RADIUS on the
default set). The tube-to-body joint fillet 1.5 builds. The tail is
the order-1 loft plus the REF dome (Q17, provisional).

## 2. Closure (measured, Q71)

No snaps. A hinge lip in the hook-end wall plus one concealed ISO 7380
M2.5×4 titanium screw at the tail (u 14.50, s 41.00). E1 tongue/web is
omitted (Q28). `V2_CLOSURE` measures the built lid and body:

| Number | Measured |
|---|---:|
| Body nylon over the lip (undercut) | yes (1) |
| Lid lip in the groove | yes (1) |
| Screw engagement in the tail bulk | 4.00 mm |
| Boss wall beside the Ø2.0 pilot | 3.13 mm |
| Screw well air (head under the boss top) | yes (1) |
| Head below the boss top | 1.75 mm |
| Screw hole through the lid | yes (1) |

The hinge groove is s 1.00–1.48, y 7.25–7.70. That leaves 1.00 mm of
outer end wall and 0.30 mm of body nylon over the lip, so the lid
cannot lift straight off. The screw head sits in a Ø5.0 well in a
local lid boss; it is not a screw on the lateral face. S4 two-finger
pull and 0.5 m drop stay **qualitative** (plan v2 §7). Insertion and
retention forces stay **NOT_MEASURED** until a printed PA12 part is
in the hand.

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

Build exit 0. `stage_b_failing` is empty. `V2_USB_end` is NOT_MEASURED
by name (packing §5b, Q70) and does not fail the build.

| Item | Answer | Check / number |
|---|---|---|
| Stranger's glance: no lateral screws | Pass on the drawing. Three contact heads on the medial face are the skin seats. The lid screw is in a tail well | renders |
| No text outside | Pass. Stage B emboss is skipped when `STAGE=shell` | notes.emboss |
| Nothing else through the skin | Pass. The v1 bench-cable exit and REF wire channel are not cut on the shell | `CABLE_EXIT_cavity` NOT_MEASURED, wall_closed 1 |
| Seam ≤ 0.3 | NOT_MEASURED. Lid inset 0.15 laps the wall tops; print and close at S4 | — |
| No planar facet over 3 mm | Pass. Lofted lid, 0 of 6 stations flat; min rise over 3 mm 0.030 | `V2_EDGE_radii` flat_stations 0 |
| Outside edges R ≥ 1.0 | Pass. Rim R 1.08 measured on the solid (3-point fit on the outer profile) | `V2_EDGE_radii` lid_rim_R 1.08 |
| Medial face flat, R0.5 | Pass. FILLET_MEDIAL 1.5 applied on the outline; the face is the floor | FILLET_MEDIAL |
| Closure | Pass. Hinge undercut 1; screw engagement 4.00; boss wall 3.13 | `V2_CLOSURE` |
| Hook circular root, ellipse, fillet, M8 radius | Circular root r 1.75, then 4.4 × 3.0 / 3.0 × 2.2. Joint fillet 1.5 applied. Radius from default HOOK_RADIUS | assemble_shell, Q76 |
| Tail blended, REF dome | Order-1 tail loft; REF dome on the tail (Q17 provisional) | Q17 |
| Colour | NOT_MEASURED. Grey or dyed black is Q30 | Q30 |
| USB ligament ≥ 1.5 to the hook | NOT_MEASURED. Wall left solid until packing §5b | `V2_USB_end` |
| USB receptacle recessed ≥ 1.0 | NOT_MEASURED. Same row | `V2_USB_end` |
| Wall ≥ 1.0 at slot and ligaments, ≥ 1.5 elsewhere | Pass. Hinge outer wall 1.00; side walls 1.50; floor under the slot 1.50; flex clearance 0.20 per side in u (slot width 2.90) | `V2_WALL_minima` |
| Captive standoff | Pass. 5 AF prism holds no nylon; wells AF 5.30 | `V2_STANDOFF` |
| `V2_TAB_envelope` | Pass. REF_body_mm3 0, SIG1 0, SIG2 0 | `V2_TAB_envelope` |
| `REF_WIRE_envelope` | Pass. body_mm3 0, lid_mm3 0 | `REF_WIRE_envelope` |

Matte / vapour smoothing is a finish on the order, not this solid.

## 5. What Rolf must approve

The two renders in `docs/fab/cad/v2/`:

- `render_medial.png` — skin face, three domes, tail, hook.
- `render_lateral.png` — lofted lid, circular-root hook, hinge at the
  hook-end wall, tail screw well. No USB opening.

One drawing page `drawing.pdf` in the v1 sheet style. His yes is the
gate before any shell order (plan v2 §7). Nothing is uploaded.

## 6. Checks named NOT_MEASURED

| Check | Reason |
|---|---|
| `TAB_envelope_air` | v1 TE 31428 envelope; see `V2_TAB_envelope` |
| `V2_USB_end` | waits for packing §5b, Q70; hook-end wall left solid |
| `V2_USB_medial` | Medial USB is not cut; hook-end opening waits for packing §5b |
| `V2_ADJUSTMENT` | Region ±0.80 from pad vs hex vs JLC ±0.3; G5/G7 |
| `V2_HARNESS` | 100 ± 3 mm cell leads, not a solid |
| `V2_RECESS` | 0.5 floor recess is not on this solid (winner recess 0) |
| S4 pull and drop | Qualitative (plan v2 §7); needs a printed PA12 part in the hand |
| `CLOSURE_PASSED` | v1 E1 flag; the shell's closure row is `V2_CLOSURE` |
| `KEEPOUT_SIGNAL_air`, `KEEPOUT_REF_air` | v1 TE and lug keep-outs; interface II puts the hex collars there (`V2_STANDOFF`, `V2_RING_seat`) |
| `CABLE_EXIT_cavity` | No bench cable on the shell |

`antenna_body_mm3` 3.72 is nylon in the RF no-copper prism. That keep-out
is no copper, not air; the check reports it and does not fail.

## 7. Needs a decision

Review r6 moved these to `tasks/reviews/code-r6.md` (decisions 69 on).
Still open from the lane: M1 (Q34), colour (Q30), Q17 REF dome, the S4
pull and drop, standoff 3.0 vs Harwin 4.0 (a parameter change, not a
fork). Q59 is closed as the slot. Q70 waits for WP11c packing §5b.
Q71 and Q76 are built on this solid.
