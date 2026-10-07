# WP3 report — renders, drawing, manifest schema

Lane `w2`. Branch `lane/w2`. Font commit `66b5564151991f4fd5f6a6457f798839d349b1d9`. Final commit `a325a635f790d73875d2045ae475189f2708cfd4`.
Python 3.13.15, build123d 0.11.1, matplotlib 3.11.2, pypdf 6.19.0, trimesh 5.x.

## What was built

- `scripts/cad/fonts/LiberationSans-Regular.ttf` and `OFL.txt` (SIL OFL 1.1, Liberation Fonts 2.1.5). Lid emboss uses that file, not Arial. Own commit `66b5564`.
- `scripts/cad/render.py` — headless medial and lateral PNG, one-page `drawing.pdf`.
- `scripts/cad/manifest.py` — schema 1 validator. Fails on a missing key.
- `docs/fab/cad/v1/render_medial.png`, `render_lateral.png`, `drawing.pdf`.
- `views` map on `manifest.json` with SHA-256. The fifteen solid hashes in `files` are unchanged since the font commit (twelve body/coupon files unchanged since main; three lid files changed only in `66b5564`).
- `commit` is the last git commit that changed a hashed solid under `docs/fab/cad/v1` (`*.step`, `*.stl`, `*.3mf`). It is not HEAD. Artwork does not move it. `views_commit` copies that same value.
- Tests and README commands. `cad` extra now also has `matplotlib>=3.8` and `pypdf>=5`.

Renderer: matplotlib Agg, orthographic shaded STL triangulation (no GUI, no GPU). PDF: matplotlib figure, then pypdf to pin CreationDate, ModDate, Producer, and `/ID` to 2026-09-16. PNG `tIME`/`tEXt` dates are rewritten the same way. Chosen because this lane is headless and the hashes must match on a second run.

## Plan §9 acceptance (WP3)

| Item | How | Result |
|---|---|---|
| Two renders, one page | files in `docs/fab/cad/v1/` | `render_medial.png`, `render_lateral.png`, `drawing.pdf` |
| Medial and lateral faces | PNGs | Medial: full p15 with caps, tail, hook, thin p15 beside it. Lateral: lid seated, hook. Scale bar 10 mm, labels, commit `66b5564`. |
| Closure section | drawing.pdf three zooms | lip/bump/groove (E5), nubs (E3), web/tongue/slot (E1). Sizes from §3.3 constants, not pixels. |
| M1–M8 | drawing table and leaders | All eight named with §3.3 values. M6 and M7 marked recorded, not CAD drivers. |
| E1–E5 | drawing table | Nominal and fitted minimum from §3.6. |
| ±0.3 general | title block | "±0.3 mm under 100 mm, JLC MJF PA12" |
| Open item 3 | validator | `.venv/bin/python scripts/cad/manifest.py --check-bytes docs/fab/cad/v1/manifest.json` → `schema 1 ok` |

## Gates

| Gate | Command | Result |
|---|---|---|
| Unit tests | `.venv/bin/python -m unittest discover -s tests -v` | 70 tests OK |
| Render twice | `scripts/cad/render.py --out` two temp dirs | PNG and PDF SHA-256 identical, and identical to `docs/fab/cad/v1/` |
| Fourteen / solid hashes | compare `files` to commit `66b5564` | No solid hash changed after the font commit. Lid STEP/STL/3MF changed only in `66b5564`. The other twelve solid files match main. The brief said fourteen; lid is three files, so twelve others stay put. |

## What Rolf can judge from the images

- Overall shape of the hook and body, tail, three mock caps, and that the lid sits on the lateral face.
- Thickness difference full 9.0 mm vs thin 7.0 mm (medial PNG, same scale).
- Glasses flat on the hook (lateral PNG).
- Closure layout: lip, bump, groove, nubs, web, tongue, slot, with the plan sizes.
- M1–M8 values and E1–E5 minima as tables.

## What he cannot judge from the images

- Print quality, surface finish, or true hidden-line edges. This is a shaded STL, not a vendor drawing.
- Fillet radii and the inside emboss. The emboss is on the lid underside.
- Exact millimetre distances by counting pixels. Use the tables and the (s, y) section.
- Whether the starburst on the medial face around each cap is a print defect. That pattern is the STL tessellation of the sphere-cap boolean. The solid was not changed.

## What was not done

- No order, upload, quote, or vendor contact.
- Solids other than the lid font were not edited.
- `docs/fab/plan.md`, `measure.md`, `order1.md`, `interface.md` were not edited.
- Open questions file was not edited. Q10 is done in this package.

## Needs a decision

1. **Medial-face starburst at the mock caps.** The STL of the body shows long triangles around each Ø4.7 cap where the sphere meets the medial face. The renderer offsets faces 0.03 mm along the normal; the stars remain. Reading: leave the solid. A later tessellation or a cap cut that does not boolean against the face would clean the picture. Not a wall or fit fail.

2. **Brief said fourteen solid hashes.** Order-1 is five parts × three formats = fifteen hashes. Lid is three of those. Twelve non-lid hashes were unchanged. Confirm that reading.

## Final commit

`a325a635f790d73875d2045ae475189f2708cfd4`
