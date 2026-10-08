# Shell v2: retained geometry reference

The 22 mm v2 body is not the selected product candidate. The current candidate is the [18 mm v4 snap shell](shell-v4.md). No shell has been ordered, printed, assembled or fit-validated.

The v2 exports remain in `cad/v2/` because the current generator and existing checks retain this geometry reference. They are not manufacturing instructions or evidence of powered wear. The old lid-screw arrangement and its shopping route are not active product plans.

## Reference inputs

- Overlay: `scripts/cad/params/shell_v2.toml`.
- Reference packing ID: `A_pack501012_series_w22_y8_iII_s3`.
- Nominal width: 22 mm. Body thickness: 9 mm. Lid underside: y = 8 mm.
- Body arc: 48.4 mm. Reference chord: approximately 47.90 mm.
- Folded sites: tracked `packing-v2.md` section 5e. Section 5d remains a reference for earlier placement readers.

The generator first reads pinned revisions of `packing-v2.md` through read-only Git commands. Its existing alternate path reads the working-tree table when those revisions are absent. Section 5c supplies the earlier courtyard and hole table; section 5d supplies its folded pads and extras. Section 5e supplies the later live shell table. History changes can affect provenance and geometry comparisons. Anatomy defaults are examples, not Rolf's measurements.

## What the retained manifest shows

`cad/v2/manifest.json` records nominal solid checks, not physical measurements. Its checks cover ring seats, standoffs, board envelopes, posterior-wall charging holes, the hook, a hinge and an M2.5 tail-screw closure.

The documented J2 courtyard overlaps the P5 standoff well by 4.93 mm in this reference. `V2_CAVITY_v3` checks pin centres and does not establish assembled component clearance. The later v4 board changes the connector, posts and charging geometry, so passing v2 checks cannot establish v4 fit.

Print tolerance, seam fit, thread retention, flex routing, RF behavior, forces, drops and repeated closure remain unverified. The old screw arrangement is retained for geometry checks only. It is not an alternative to validating the selected snap.

## Regenerate a reference locally

From the repository root with the CAD extra installed:

```bash
.venv/bin/python scripts/cad/bte_fit_shell.py \
    --params scripts/cad/params/shell_v2.toml --stage shell --out .reports/cad/v2
.venv/bin/python scripts/cad/render.py --out .reports/cad/v2
.venv/bin/python scripts/cad/manifest.py --check-bytes .reports/cad/v2/manifest.json
```

Use ignored output rather than overwriting tracked reference files. Regeneration was not performed during publication cleanup. See [CAD instructions](../../scripts/cad/README.md) for dependencies and [open gates](open-questions.md) for current engineering work.
