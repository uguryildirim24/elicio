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
board edge.

The cell 501015 sits in the pocket in series with the board, foam 0.5 on
the lid face. USB-C opens on the hook-end end face (plan v2 §5.4
fallback; the medial face cannot hold the receptacle next to the cell).
The recovery switch is under a blind 0.5 recess in the lid, no hole.
There is no text on the outside. The three contact heads are on the
medial face; no screw is visible from the lateral side.

The hook is an elliptical loft, 4.4 × 3.0 at the root and 3.0 × 2.2 at
the tip. Radius from M8 (HOOK_RADIUS on the default set). A 1.5 fillet
at the tube-to-body joint was requested; OCCT left that edge sharp on
this solid. The tail is the order-1 loft plus the REF dome (Q17,
provisional).

## 2. Closure calculation

Choice: hinge lip in the tail (past the board, because USB occupies the
hook-end wall) plus two cantilever snaps on the inner side walls over
the board. E1 tongue/web is omitted (Q28). No concealed tail M2.5.

Each snap: beam L = 8.0 mm, thickness t = 1.0 mm, width w = 4.0 mm,
catch y = 0.5 mm, groove 0.4 into the 1.5 side wall (residual 1.1).

Cantilever end-load strain, Roark: ε ≈ 1.5 t y / L²

ε = 1.5 × 1.0 × 0.5 / 8.0² = 0.0117 (1.17 %).

Limit used here: 0.04 for a repeated PA12 snap. Measured check
`V2_CLOSURE` records 0.01172 and the groove air.

Insertion force and retention force are **NOT_MEASURED**. They need the
printed PA12 modulus E and a part in the hand (plan v2 §7: drawing and
calculation at S0; qualitative pull and 0.5 m drop at S4).

## 3. Contact joint — what G7 needs from the shell

Interface II (`board-v2.md` §11). Datum chain, medial face y = 0 up:

| Datum | y | Source |
|---|---:|---|
| Medial outer face | 0.00 | body frame |
| Floor inner face (WALL_MEDIAL) | 1.50 | plan v2 §3 |
| Ring pad top (PI 0.11 + FR4 0.2) | 1.81 | `packing-v2.md` §5, review r5 |
| Standoff top / board underside | 4.81 | standoff 3.0 (Q43, Q58) |
| Board top | 5.32 | flex 0.51 at parts |
| Boss top | 4.31 | 0.5 below the standoff tops |
| Lid underside | 8.00 | LID_Y |
| Lid outer | 9.00 | LID_THICK 1.0, plus crown ~0.3 |

Pocket, seat, hole:

| Feature | Number | Notes |
|---|---|---|
| Brass standoff | 5 AF, female M2.5, h 3.0 | Spacer Express 3.0; Harwin R25-1000402 4.0 is listed, not fitted |
| Printed hex collar height | 2.0 from the floor | Captive well on the floor, not a 3.31-deep cut in a 1.5 wall |
| Printed well | AF 6.3 plus Ø7.4 | Oversized so the packing 5 × 5 standoff envelope is air. G7 sets the captive clearance |
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

| Item | Answer | Check / number |
|---|---|---|
| Stranger's glance: no lateral screws | Pass on the drawing. Three contact heads on the medial face are the skin seats, not lid screws | renders |
| No text outside | Pass. Stage B emboss is skipped when `STAGE=shell` | notes.emboss |
| Seam ≤ 0.3 | NOT_MEASURED. Lid CLEAR_FIT is the order-1 plate inset; print and close at S4 | — |
| No planar facet over 3 mm | Pass. Lid crown sagitta 0.31 at the probe | `V2_EDGE_radii` lid_crown_mm 0.3059 |
| Outside edges R ≥ 1.0 | Partial. Medial outline R0.5 (plan). Tip round 4.0. Hook joint 1.5 requested, left sharp | fillets in the manifest |
| Medial face flat, R0.5 | Pass. FILLET_MEDIAL 1.5 applied on the outline; the face is the floor | FILLET_MEDIAL |
| Closure: snap strain or screw | Snap ε = 0.0117 plus tail hinge lip | `V2_CLOSURE` |
| Hook elliptical, fillet, M8 radius | Axes 4.4 × 3.0 / 3.0 × 2.2. Joint fillet left sharp. Radius from default HOOK_RADIUS | assemble_shell |
| Tail blended, REF dome | Order-1 tail loft; REF dome on the tail (Q17 provisional) | Q17 |
| Colour | NOT_MEASURED. Grey or dyed black is Q30 | Q30 |
| USB ligaments ≥ 1.5 | 1.5 to the hook root | `V2_USB_end` ligament_hook 1.5 |
| Wall ≥ 1.0 at slot and ligaments, ≥ 1.5 elsewhere | Snap residual 1.1; USB ligament 1.5; side walls 1.5; remaining end wall beside the slot 1.827 / 1.879; floor under the slot 1.50; measured flex clearance 0.20 mm per side in u (slot width 2.90) | `V2_WALL_minima` |
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
| Hook joint R ≥ 1.0 | 1.5 fillet requested; OCCT left the ellipse-to-body edge sharp |
| Captive hex fit | Printed well AF 6.3 + Ø7.4 vs brass 5 AF; G7 |

`antenna_body_mm3` 3.72 is nylon in the RF no-copper prism. That keep-out
is no copper, not air; the check reports it and does not fail.

## 7. Needs a decision

1. M1 (Q34). Default 52. Manifest `provisional: true`.
2. Printed hex clearance vs captive 5 AF (G7). This well is oversized so
   the packing envelope is air.
3. Hook joint fillet: leave sharp, or a different blend (different
   section count, or a circular root then ellipse).
4. Snap insertion and retention forces, and the S4 pull and drop, once
   a PA12 coupon exists.
5. Colour, grey or dyed black (Q30).
6. Q17 REF dome on the tail, still provisional.
7. Q59 is closed as the slot: `packing-v2.md` §5 on lane/w3 at `284ec05`
   found no in-cavity REF route. This shell cuts `REF_end_wall_slot`
   plus the stated flex clearance. No further packing search.
8. Standoff 3.0 vs Harwin 4.0. This file keeps 3.0. A 4.0 swap is a
   parameter change, not a construction fork.
