# Gauge CAD

This folder builds the Stage B fit-gauge solids from plan §3.

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
- Only SIDE, VARIANT, HOOK_PRELOAD, CREASE_BOW, HOOK_RADIUS and M1–M8 may be set. Any other key, an unknown key, or `MOCK_CONTACTS = false` fails before export.
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

## Run the checks

```bash
.venv/bin/python scripts/cad/bte_fit_shell.py --checks-only
.venv/bin/python scripts/cad/bte_fit_shell.py --params scripts/cad/params/rolf.toml --checks-only
.venv/bin/python -m unittest tests.test_cad -v
```

Do not upload files to a vendor. WP3 draws from the STEP files. Purchases need Rolf's approval.
