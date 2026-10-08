# Shell v4: snap print-trial candidate

The selected design is `cad/v4-snap/`. It has a ramped twin-arm latch and a key corridor. It has not been printed or tested. Fit, release, retention, fatigue and contact stability are unverified. Do not treat it as a finished wearable.

![Snap-shell CAD preview](cad/v4-snap/render_closure.png)

## What exists

The folder contains body/lid STEP, STL and 3MF exports, a closure preview and `manifest.json`. The nominal body width is 18 mm, thickness is 8.1 mm and curved arc is 48.4 mm. These are reference geometry values, not personal measurements.

The committed snap manifest records 106 passing nominal checks. They include board courtyard prisms, the folded charging flap, seated body/lid overlap, swept key clearance and opposing tolerance offsets. Both committed STL meshes are reported watertight. Courtyard prisms are simplified envelopes, not a folded physical PCB assembly.

The component clearance rule is 0.40 mm, except the documented U1 lid-post seat. CAD passing status is not a tolerance-stack release or an electrical safety result. Snap force and deformation values in the manifest are simplified models, not measured material performance.

## Open mechanical limits

- The right tail wall is approximately 0.99 mm in the design record and needs print-process review.
- The P1 lid post has local relief. Its load capacity is untested.
- The P2 post seats on U1. Actual package loading is untested.
- The folded flap, interrupted key walls, cell lead routing and contact installation remain untested.
- Key access, repeated hook engagement, seam clearance and retention need a physical print.
- Reference geometry has not been checked against a person's anatomy.

## Retained and rejected references

`cad/v4/` is a hinge-only base shell. The hinge does not retain the lid. It remains as a geometry reference and test input, not a second product candidate.

The rejected M1.6 screw closure left only 0.13 mm of radial wall around its head well. It was unsuitable for the intended print process. Its `--closure m16` diagnostic branch and exports in `cad/v4-m16/` remain as rejected-design evidence. The old M2.5 tail closure also does not fit within the unchanged body length. Rejection does not establish that the snap works physically.

## Regenerate without overwriting references

From the repository root, after the base install:

```bash
.venv/bin/python -m pip install -e '.[cad]'
.venv/bin/python scripts/cad/build_shell_v4.py --closure snap --out .reports/cad/v4-snap
.venv/bin/python scripts/cad/render_v4.py --single --out .reports/cad/v4-snap
```

Output is ignored. Regeneration was not performed during publication cleanup. The current v4 board courtyard table is read from `board-v4-design.md` section 10.2. Physical board folds and the print process must be reviewed separately.
