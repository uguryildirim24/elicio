# Gauge CAD

This folder builds the Stage B fit-gauge solids from plan §3.

## V4-snap preview from committed solids

`assemble_native.py` exports an assembled GLB and eight studio-style PNGs with
commit captions. It uses the committed v4-snap STL pair, routed v4 board
footprints, v4 shell manifest, and `board-v4-design.md` §10.2 folded sites
and courtyard heights. A flat routed STEP cannot depict the board after its
folds: the board and populated packages are curved envelope geometry rather
than copper or exact package CAD. The cell is its 501012 envelope; the three
M2.5 titanium heads, P4/P5 titanium wall heads and US quarter are simplified
visuals. The old/new image loads the committed v2 body STL. No lid screw is
present on v4-snap. These are assembly visualizations, **not** a clearance or
buildability check; the committed v4-snap interior predates the later base-v4
interior correction.

With Python 3.11+, NumPy and Pillow, render with SceneKit and Swift on macOS,
or with Blender (including 4.0) on Linux:

```bash
python scripts/cad/assemble_native.py --out /path/to/output
```

The Linux Blender build used here has no OpenImageDenoiser, so it renders
32 CPU samples without denoising. The camera keeps the hook and separated lid
inside the picture in each view.

`earpiece.glb` is glTF 2.0 in metres, with PA12 and metal materials;
`captions.json` records full shell and board commits and the approximations.
The renderer makes one offline job for all eight views and cleans its
temporary geometry on exit. No model is downloaded.
The Blender/Cycles alternative is `assemble_photo.py` if Blender starts.

## Install

Python 3.13 is enough. build123d has a 3.13 wheel.

```bash
python3.13 -m venv .venv
.venv/bin/python -m pip install -e '.[cad]'
```

## Build the reference set

Writes the five order-1 files (STEP, STL, 3MF) and `manifest.json` under `docs/fab/cad/v1/`. Every M1–M8 is a default, so the build and the lid emboss are marked REF.

```bash
.venv/bin/python scripts/cad/bte_fit_shell.py --out docs/fab/cad/v1/
```

Passing `--params scripts/cad/params/default.toml` gives the same build: `default.toml` is the reference, never an overlay.

## Build from Rolf's measurements

Put M1–M8 (and `SIDE`) in `scripts/cad/params/rolf.toml`. The overlay rules:

- A key left out keeps its reference-ear default, and the build is marked REF.
- CREASE_BOW is computed from M1 and M2 (arc–chord, clamped to 1–8) only when the file sets **both** M1 and M2 and does not set CREASE_BOW. Otherwise it stays 3.0.
- HOOK_RADIUS follows M8: M8 + HOOK_DIA/2 + 0.75, which is the 13.5 plan §3.3 quotes at M8 = 11 (the plan's written "+ 1.0" gives 13.75 and fails its own `< M8 + 1` check).
- Order 1: only SIDE, VARIANT, HOOK_PRELOAD, CREASE_BOW, HOOK_RADIUS and M1–M8 may be set. Any other key or an unknown key fails before export. `MOCK_CONTACTS = false` is Stage B (see below), not an order-1 overlay.
- The script rejects M1 below TOTAL_CHORD + 3 for the bow it uses.

Full order-1 set from the measurements:

```bash
.venv/bin/python scripts/cad/bte_fit_shell.py --params scripts/cad/params/rolf.toml --out docs/fab/cad/v1/
```

One variant only (plan §3.1 form) writes that body, the lid and the coupon, with a manifest listing just those. Give it an empty `--out`; the script refuses a folder whose manifest lists other parts, so `docs/fab/cad/v1/` never mixes two parameter sets:

```bash
.venv/bin/python scripts/cad/bte_fit_shell.py --params scripts/cad/params/rolf.toml --variant thin --preload 1.5 --out /tmp/elicio-thin/
```

`--variant` takes full or thin, `--preload` 1.5 or 2.5. Anything else fails before export.

## What the build does not do as plan §3.5 writes it

The manifest `notes` record each of these per body:

- Hook joint fillet (§3.5 step 9): 2.0 does not build. The tube edge sits 1.25 mm from the medial face at M4 = 6.0; the script applies the largest step that builds (1.5 on full p15, 1.75 on thin p15 and full p25).
- Hook stub: the −5° embedded start is cut back to the cavity wall (about 4.6 mm³ removed), so the cavity and battery pocket stay clear.
- Lip root fillet (§3.5 step 7): 0.2, not 0.5. Above the 0.2 lip-to-top-face gap the fillet overlaps the body's top edge when seated.
- LID_EDGE 0.8 runs round the plate rim except the top edge at the lip end, which stays sharp so the lip keeps its full joint.

The lid emboss uses `fonts/LiberationSans-Regular.ttf` (SIL Open Font Licence 1.1, `fonts/OFL.txt`). It does not use Arial or any system font.

## Renders and drawing

Headless. No GUI, no GPU. `render.py` rasterises the STL triangles with a z-buffer in numpy (one flat shade per triangle, outlines and creases from the depth and normal buffers) and lays the images out with matplotlib Agg. Every view is orthographic, head-on or edge-on, so the 10 mm bar is true in the plane of the view. The PDF embeds the shaded views as images; sections, tables and text are vector. pypdf pins PDF dates; PNG `tIME`/`tEXt` dates are rewritten. The corner stamp is the solids commit and its commit date. Run twice; the hashes must match.

```bash
.venv/bin/python scripts/cad/render.py --out docs/fab/cad/v1/
.venv/bin/python scripts/cad/render.py --out docs/fab/cad/v1/ --debug-png /tmp/elicio-draw   # also drawing_page.png, not hashed
```

Writes `render_medial.png`, `render_lateral.png`, `drawing.pdf` and the `views` map in `manifest.json`. It does not rebuild solids and does not change hashes in `files`.

The committed PNG and PDF hashes were produced with numpy 2.5.3, matplotlib 3.11.2, pypdf 6.19.0 and trimesh 5.1.0 on Python 3.13. Another build of those libraries can move the image bytes without any geometry change; regenerate and compare the pictures, not only the hashes, before committing new ones. `placement.svg` (WP6) is not in `views`; `tests/test_placement.py` checks it.

After a commit that changes a solid, `commit` in the manifest still names the previous solids commit until you rebuild and commit the manifest (and renders) once more; the regen test fails in between on purpose.

## Validate the manifest

```bash
.venv/bin/python scripts/cad/manifest.py docs/fab/cad/v1/manifest.json
.venv/bin/python scripts/cad/manifest.py --check-bytes docs/fab/cad/v1/manifest.json
```

`schema` must be 1. `hash_rule` is SHA-256 of raw file bytes with the STEP/STL/3MF pins. `commit` is the last git commit that changed a hashed solid (`*.step`, `*.stl`, `*.3mf` under `docs/fab/cad/v1`), not HEAD. Artwork under `views` uses the same SHA-256 rule; PNG and PDF dates are pinned to 2026-09-16T00:00:00Z. `views_commit` is that same solids commit; adding or regenerating artwork does not move `commit`.

## Coupon-to-parameter mapping (plan §10 open item 2)

Coupon file: `docs/fab/cad/v1/coupon.*`. Built by `build_coupon` in `bte_fit_shell.py`. Axes: x and y across the top face from its centre; the rib stands on the top face. Measured sizes feed these parameters (interface §12 V2-2):

| Coupon feature | Position (x, y) | Designed | Feeds |
|---|---|---|---|
| Hole | (−3, −3) | Ø1.7 through | Smallest round hole the process opens; lower bracket for CONTACT_HOLE |
| Hole | (0, −3) | Ø2.9 through | CONTACT_HOLE directly: an M2.5 shank (2.5) must pass |
| Hole | (3, −3) | Ø3.4 through | Upper bracket: CONTACT_HOLE moves toward it if Ø2.9 prints under 2.5 |
| Slot | (0, 2), 6 long | 0.9 wide through | TONGUE_SLOT height (0.9) and the 0.4 tongue clearance |
| Slot | (0, 4), 6 long | 0.4 wide through | Whether a 0.4 gap prints open: CLEAR_FIT and the 0.4 rigid-pair nominals (plan §3.6) |
| Rib | along x at y −0.5 | 0.4 thick × 3 tall × 12 long | E4; the thin-feature floor under E1 (tongue 0.5) and E3 (nubs 0.8) |

WP8 updates the parameters when the coupon is measured. Do not edit `manifest.json` by hand.

## Placement drawing (WP6)

```bash
.venv/bin/python -m pip install -e '.[cad]'
.venv/bin/python scripts/cad/placement.py --out docs/fab/cad/v1/placement.svg
.venv/bin/python -m unittest tests.test_placement -v
```

The drawing is 2D in the body-frame `(u, s)` plane. It does not change the gauge solids. matplotlib must be in the `cad` extra. Regeneration is byte-identical on one machine; hashes can move with the matplotlib build, as with the CAD lid font.

## Run the checks

```bash
.venv/bin/python scripts/cad/bte_fit_shell.py --checks-only
.venv/bin/python scripts/cad/bte_fit_shell.py --params scripts/cad/params/rolf.toml --checks-only
.venv/bin/python -m unittest tests.test_cad -v
```

Do not upload files to a vendor. WP3 draws from the STEP files. Purchases need Rolf's approval.

## Stage B (provisional)

WP8-prep. Nothing here is decided or ordered: the build is a parameter run for WP8, and its files go to a temp folder. No order 2 files exist.

The Stage B path uses the same construction as the gauge (one `build_body_and_lid`: path, body, tail, fillets, recess, cavity, rib, pads, lid, hook, hook-in-cavity cut). Only the inputs and plan §3.5 step 5 change. Packing moves the width, arc, cavity, tail and board zone. Step 5 cuts the pocket, the three holes, WIRE_CHANNEL and CABLE_EXIT instead of fusing mock domes. E1/E3/E5 are built only with `CLOSURE_PASSED = true`. The keep-out cylinders and the TE 31428 tab envelopes are reserved air. They are never cut, so any nylon inside them shows up in a check.

Write to a folder you name. The script refuses `docs/fab/cad/v1/` and `docs/fab/cad/v2/`.

```bash
.venv/bin/python scripts/cad/bte_fit_shell.py --params scripts/cad/params/stageb_provisional.toml --out /tmp/elicio-stageb/
```

Without `--parts` a Stage B build writes `body_full_p15`, `body_full_p25` and `lid`. Plan §7 order 2 is two bodies and two lids. The preload is Rolf's pick after 3.7, and a thin body cannot hold the cell, so `CELL_envelope` fails on it. `--parts` takes any comma list with at least one body, because the checks run on bodies. The stale-part guard works as for order 1.

Exit codes: 0 when every Stage B check passes. 2 when a check fails, and nothing is written for that body. 3 when the files and manifest are written but the manifest says `stage_b_passed: false`. Today that is 3, because of Q21.

Named checks, measured on each built body and its seated lid (manifest `stage_b`, each with numbers per body):

| Check | Measured |
|---|---|
| `CONTACT_HOLE_wall` | each Ø2.9 hole removed exactly the 1.5 wall disc (9.91 mm³) and is open |
| `KEEPOUT_SIGNAL_air` | nylon volume inside each Ø7.1 keep-out, floor to 4.13 |
| `TAB_envelope_air` | nylon volume inside each tab envelope, 1.96 wide × `TAB_HEIGHT`, Ø7.1 edge to 8.85, at the placement angle |
| `KEEPOUT_REF_air` | pocket air, lid volume inside the pocket, and a full 1.0 wall band around it |
| `BOARD_underside_clear` | probed pad tops against the stack top, barrel tops and envelope tops above the probed floor |
| `REF_WIRE_envelope` | a Ø1.3 wire along the placement route at y 3.3: overlap with body, lid, cell, keep-outs and tabs; lid gap; each turn at bend radius 3 |
| `CABLE_EXIT_cavity` | nylon the exit removed inside the cavity (a pad or the rib), pierced wall, opening into the cavity, board side of the rib |
| `CELL_envelope` | the 5.2 × 10.4 × 15.6 cell plus 0.5 foam on the probed floor against body and lid (with the emboss), and probed wall and rib clearances |
| `Q21_REF_lug` | lug top 8.23 against the lid underside probed over the pocket, and barrel 4.54 against the probed pocket radius. Recorded; it does not stop the write |
| `CLOSURE_PASSED` | tongue, slot, nubs and lip present on the solids exactly when the flag is set |

`--checks-only` runs the plan-number versions of these ("... pre-CAD") and `PLACEMENT_contacts`. The measured versions need the build.

Decided in the provisional file (each still provisional; the header says what each waits on):

- `PACKING = C` (Q20 reading: BODY_WIDTH 20, board 19 × 15.5, pads and tab angles from `placement.py`)
- `MOCK_CONTACTS = false`
- `TAB_HEIGHT = 2.0` (Q22)
- `CABLE_EXIT_S = 35.0`: plan §3.3's s 36 cuts a corner pad (review r4 decision 24)
- contact positions = plan §3.3 defaults until WP7a. Any other site fails `PLACEMENT_contacts` until `placement.py` is re-run for it.

Not decided:

- Rolf's packing pick (Q20). A and B are switches: `--set PACKING=A` or `--set PACKING=B`.
- The reference lug against the lid and the pocket wall (Q21). `Q21_REF_lug` fails and records the numbers.
- Contact coordinates (WP7a) and the reference site (Q17).
- `CLOSURE_PASSED` (default false). Set true today, it fails `KEEPOUT_REF_air`: the E1 web and tongue sit inside the reference pocket (review r4 decision 25).
- The cell pack (Q18). The check uses the plan envelope with 0.5 foam on the lid face.
- Stage B keys (`PACKING`, `CONTACT_*`, `CABLE_EXIT_S`, `TAB_HEIGHT`, `CLOSURE_PASSED`) fail on an order 1 overlay.

The Stage B manifest keeps schema 1 and adds `stage`, `provisional`, `packing`, `closure_passed`, `contact_source`, `stage_b`, `stage_b_failing` and `stage_b_passed`. `manifest.py` validates them when `stage` is `B`. Order 1 manifests omit those keys, and a Stage B manifest never carries order 1 `views`. The Stage B lid is embossed `ELICIO V2 …`, 0.4 deep over the battery zone (Q11), so it cannot be mistaken for an order 1 lid.

### Stage B v2 (packing v2, WP11)

```bash
.venv/bin/python scripts/cad/bte_fit_shell.py --params scripts/cad/params/stageb_v2.toml --out /tmp/elicio-stageb-v2/
```

Same construction and exit codes as above; `PACKING = "v2"` adds the `V2_*` checks for the packing-v2 layout named in the file. Each check reports a number or `NOT_MEASURED` by name, and the manifest lists the unmeasured ones under `stage_b_not_measured`. Today it exits 3: the floor-level REF tab crosses the cavity end wall (`V2_TAB_envelope`, `REF_WIRE_envelope`). `docs/fab/packing-v2.md` §6 has the numbers, and `tests/test_cad.py` checks them against a fresh build. The packing matrix and its drawings: `placement.py --all` (closers), `--kept-drawings` (the committed set) and `--all-drawings --out-dir <tmp>` (every run, never committed).

## Assembled v4-snap earpiece (visualisation, not fabrication CAD)

With Blender 5.2+ on `PATH`, regenerate the flat board export, then render:

```bash
python3 scripts/board/release.py --board elicio-v4 --routed
python3 scripts/cad/assemble_photo.py --out .herdr-project/elicio-t-0034/library --samples 12
```

The script uses the committed v4-snap body/lid STL (the STEP exports' tessellation), shell manifest frame, routed v4 PCB footprints and `board-v4-design.md` §10.2 folded sites, courtyards and height intervals. The released KiCad STEP is **flat**, not a folded assembly; the model instead sweeps simplified flex/island envelopes and draws electronic parts as §10.2 courtyard blocks. The 501012 cell occupies the §1.4 pocket. Contact and charging hardware are visual titanium proxies without threads or complete electrical detail. The latch is hidden; **there is no lid screw**. The renders show natural grey PA12 and titanium. `earpiece.glb`, eight PNGs (including the previous 22 mm body at the same scale) and `captions.json` are written to the specified output folder. `--only lateral` renders one view; a complete rerun replaces all output from current commits. The v4 base-shell interior correction in t-0031 was not regenerated in the v4-snap variant: the outside is the chosen snap variant, while its lid-off interior remains the older revision. Do not use this assembly as fit or production proof.
