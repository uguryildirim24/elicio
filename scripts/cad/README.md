# Gauge CAD

This folder builds the Stage B fit-gauge solids from plan §3.

## Install

Python 3.13 is enough. build123d has a 3.13 wheel.

```bash
python3.13 -m venv .venv
.venv/bin/python -m pip install -e '.[cad]'
```

## Build the reference set

Writes the five order-1 files (STEP, STL, 3MF) and `manifest.json` under `docs/fab/cad/v1/`.

```bash
.venv/bin/python scripts/cad/bte_fit_shell.py --params scripts/cad/params/default.toml --out docs/fab/cad/v1/
```

## Build from Rolf's measurements

Put M1–M8 in `scripts/cad/params/rolf.toml`. Missing keys keep the reference-ear default and mark the build REF. The script computes CREASE_BOW from M1 and M2 and clamps it to 1–8. It rejects M1 below TOTAL_CHORD + 3 before export.

```bash
.venv/bin/python scripts/cad/bte_fit_shell.py --params scripts/cad/params/rolf.toml --variant full --preload 1.5 --out docs/fab/cad/v1/
```

The same command with `--variant thin` or `--preload 2.5` is in the allowed matrix. Any other variant or preload fails before export.

## Run the checks

```bash
.venv/bin/python scripts/cad/bte_fit_shell.py --params scripts/cad/params/default.toml --checks-only
.venv/bin/python -m unittest tests.test_cad -v
```

Do not upload files to a vendor. WP3 draws from the STEP files. Purchases need Rolf's approval.
