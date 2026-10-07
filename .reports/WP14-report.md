# WP14 report — shell v2 on the round 5 winner

Lane `w1`, branch `lane/w1-r6`, package WP14. Plan v2 at `ef369bd`
(`docs/fab/plan-v2.md`). `plan-v2.md` and `open-questions.md` were not
edited. Order 1 files under `docs/fab/cad/v1/` were not written.
`lane/w3` was not merged.

## What was built

Wearable body and lid on winner `A_501015_series_w20_y8_iII_s3`. Same
Stage B v2 construction path; `STAGE=shell` adds hex collars, ring seats,
Q59 `REF_end_wall_slot`, bosses, USB end-face opening, switch recess, tail
hinge lip, two cantilever snaps, elliptical hook, lid crown. Overlay
`scripts/cad/params/shell_v2.toml`. Outputs `docs/fab/cad/v2/`. Record
`docs/fab/shell-v2.md`.

Closure: hinge lip in the tail plus two snaps L=8 t=1 y=0.5, strain
0.0117. USB on the hook-end end face. Standoff 3.0 mm. M1=52,
`provisional: true`.

## Coordinator note (second DONE)

WP11b on `lane/w3` at `284ec05`, `packing-v2.md` §5, table REF tab route:
no in-cavity REF route. Cavity ends at s 38.20, tail pocket starts at
s 39.25, 1.05 mm of nylon between them. Q59 is `REF_end_wall_slot`
(u 7.25–9.75, s 38.20–39.25, y 1.50–1.81, 2.50 × 1.05 × 0.31,
0.814 mm³). The shell cuts that box plus 0.20 mm flex clearance per side
in u, 0.20 mm in s, 0.15 mm in y. Measured on the built solid: slot width
2.90, clearance 0.20 mm per side in u.

`V2_TAB_envelope` pass: REF_body_mm3 0.0, SIG1 0.0, SIG2 0.0.
`REF_WIRE_envelope` pass: body_mm3 0.0, lid_mm3 0.0.

`V2_WALL_minima` pass: anterior 1.5, posterior 1.5, remaining end wall
beside the slot 1.827 / 1.879, floor under the slot 1.50, snap residual
1.1, USB ligament 1.5. All ≥ 1.0 beside the slot, ≥ 1.5 on the side
walls.

Stage B v2 without `STAGE=shell` is not slotted. Q59 still fails there
(REF 1.194 mm³ / 1.1902 mm³). Cited `packing-v2.md` §5 on lane/w3 in
`shell-v2.md`. Did not merge `lane/w3`.

## Gates

| Gate | Command | Result |
|---|---|---|
| Full suite | `.venv/bin/python -m unittest discover -s tests -v` | OK, 174 tests, 167.029 s, CAD tests ran |
| Order 1 byte-identical | `CadRegenTests.test_reference_regen_matches_committed_hashes` and `CadRenderTests.test_renders_and_drawing_regen_byte_identical` in that run | both ok |
| Stage B v2 still the round 5 solid | `CadStageBV2BuildTests` vs `STAGE_B_V2_MEASURED` | ok. Q59 still fail (`V2_TAB_envelope` REF 1.194 mm³, `REF_WIRE_envelope` 1.1902). No numbers moved. Exit 3 on a Stage B write. Two consecutive file hashes identical |
| Shell twice identical | `CadShellV2BuildTests.test_two_consecutive_shell_runs_are_identical` | ok, exit 0, `stage: shell` |
| Manifest bytes | `.venv/bin/python scripts/cad/manifest.py --check-bytes docs/fab/cad/v2/manifest.json` | schema 1 ok |
| git status | `git status --short` | empty at DONE (report untracked) |

Plan §9 row 14 (shell v2: body, lid, closure and hook, port wall, bosses,
pockets, renders, manifest; §7 checks; Stage B checks on the built solid;
identical regeneration): the listed files exist; §7 and Stage B rows are
in the manifest and in `shell-v2.md`; regeneration tested as above.

## What was not done

No order, quote, or upload. Insertion and retention forces not computed
(no printed PA12 E). Hook joint 1.5 fillet requested; OCCT left it sharp.
Printed hex well is AF 6.3 plus Ø7.4 (oversized vs brass 5 AF).

## Needs a decision

1. M1 (Q34). Default 52. Manifest `provisional: true`.
2. Printed hex clearance vs captive 5 AF (G7).
3. Hook joint fillet: leave sharp, or a different blend.
4. Snap insertion and retention, and the S4 pull and drop.
5. Colour, grey or dyed black (Q30).
6. Q17 REF dome on the tail.
7. Q59 is the slot (`packing-v2.md` §5 on lane/w3 at `284ec05`). No
   further packing search.
8. Standoff 3.0 vs Harwin 4.0. This file keeps 3.0.

## Final commit sha

First DONE: `553b3026d7324bf9115ec38658e341098394f3f8`
(`shell(v2): the wearable body on the round 5 winner`).

Second DONE: `c3c11d8d500f60ee93a0102a75fbdcf29ff91ff6`
(`shell(v2): cut REF_end_wall_slot from packing-v2 §5`).

A post-commit hook on this repo pushed `lane/w1-r6` to origin after each
commit. This lane did not run `git push`.
