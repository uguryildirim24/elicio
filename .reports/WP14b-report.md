# WP14b report — shell v2b: screw closure, lofted lid, hook root

Lane `w1`, branch `lane/w1-r6`, package WP14b. Base `110a79b` (round 6
merge). `plan-v2.md` and `open-questions.md` were not edited. Order 1
files under `docs/fab/cad/v1/` were not written.

## What was built

Same construction path as Stage B v2. `STAGE=shell` now adds Q71, the
§7 lofted lid, and Q76. Overlay `scripts/cad/params/shell_v2.toml`.
Outputs `docs/fab/cad/v2/`. Record `docs/fab/shell-v2.md` §2, §4, §5.
Manifest `provisional: true`.

Captive hex wells, ring seats, Q59 slot, and the reviewer's measured
checks stay.

## Before / after (measured on the built solid)

| Check | Review r6 (main `110a79b`) | WP14b |
|---|---|---|
| `V2_CLOSURE` | fail. Snap undercut 0 / 0 / 0, beam 0.50, ε 0.135 | pass. Hinge undercut 1, lip in 1, engagement 4.00, boss wall 3.13, well air 1, head below boss top 1.75 |
| `V2_EDGE_radii` | fail. flat_stations 4, lid_rim_R 0.8 (constant) | pass. stations 6, flat_stations 0, min rise over 3 mm 0.030, lid_rim_R 1.08 (3-point fit) |
| `V2_USB_end` | fail. ligament_hook −0.89, mouth_recess −4.80 | NOT_MEASURED: waits for packing §5b, Q70; hook-end wall left solid |
| `V2_WALL_minima` | fail on the USB ligament | pass. hinge outer wall 1.00, side walls 1.50, slot floor 1.50, slot clear u 0.20 |
| Build exit | 3 (`V2_CLOSURE`, `V2_EDGE_radii`, `V2_USB_end`, `V2_WALL_minima`) | 0. USB row is NOT_MEASURED by name and does not fail the build |
| Q76 hook root | elliptical 4.4 × 3.0 from t=0; joint fillet left sharp | circular root r 1.75, then 4.4 × 3.0 / 3.0 × 2.2; joint fillet 1.5 applied (`notes.q76`) |

Renders (committed):

- `docs/fab/cad/v2/render_medial.png`
- `docs/fab/cad/v2/render_lateral.png`

## Gates

| Gate | Command | Result |
|---|---|---|
| Full suite | `.venv/bin/python -m unittest discover -s tests -v` | OK, 206 tests, 221.543 s, CAD tests ran |
| Order 1 byte-identical | `CadRegenTests.test_reference_regen_matches_committed_hashes` and `CadRenderTests.test_renders_and_drawing_regen_byte_identical` | both ok |
| Stage B v2 | `CadStageBV2BuildTests` vs `STAGE_B_V2_MEASURED`; two consecutive runs | ok. Q59 still fail on the unslotted Stage B path. File hashes identical run to run. Manifest not rewritten in `docs/fab/cad/v2/` (that folder is the shell) |
| Shell twice identical | `CadShellV2BuildTests.test_two_consecutive_shell_runs_are_identical` | ok, exit 0, `stage_b_failing: []`, solids equal to `docs/fab/cad/v2/` |
| Manifest bytes | `.venv/bin/python scripts/cad/manifest.py --check-bytes docs/fab/cad/v2/manifest.json` | schema 1 ok |
| git status | `git status --short` | empty at DONE (this report untracked) |

Plan §9 row 14 (shell v2 body, lid, closure and hook, §7 checks, Stage B
checks on the built solid, identical regeneration): the listed files
exist; §7 and Stage B rows are in the manifest and in `shell-v2.md`;
regeneration tested as above.

## What was not done

No order, quote, or upload. USB opening waits for WP11c packing §5b
(Q70). S4 two-finger pull and 0.5 m drop stay qualitative. Insertion
and retention forces stay NOT_MEASURED (need printed PA12). The hinge
callout on `render_lateral.png` sits near the hook tube; the lip itself
is in the hook-end wall under the lid.

## Needs a decision

1. M1 (Q34). Default 52. Manifest `provisional: true`.
2. Colour, grey or dyed black (Q30).
3. Q17 REF dome on the tail.
4. S4 pull and drop (qualitative, plan v2 §7).
5. Standoff 3.0 vs Harwin 4.0. This file keeps 3.0.
6. Q70 USB: packing §5b (WP11c). This shell does not cut the opening.
7. Q76 built: circular root r 1.75, fillet 1.5 applied. No coordinator
   fallback.

Q59 stays the slot. Q71 is built on this solid.

## Final commit sha

`bb0c788b8d34b1d098feab73a60fa1a2f7be8c3d`
(`shell(v2b): screw closure, lofted lid, hook root`).
