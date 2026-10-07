# WP14f — shell v2f finish

Final commit: `252afbb5c6c377c8e670b164169b016f8c1a9c49` on `hp/elicio/t-0001-finish-the-earpiece-shell-v2f-wp14f-from` (post-commit hook pushed the lane branch). Solids commit and render/manifest stamp: `f7675ec099ffa9e1b5bab14fad3920c5d666262e`.

## Built

Merged `origin/lane/w1-r6` (`938984e`), `origin/lane/w3` (`ab9ce95`), `origin/lane/w4` (`dbeeafa`) in that order, without rebasing. **Conflicts: none.** Resolved the wall probe's false no-boundary readings by probing from cavity air beyond the collar and excluding the solid end-wall/rib sections; clipped the P5 collar only in the actual board envelope. No forked construction or check constants. Q89's lid boss and M2.5×8 were already present and remain measured. Updated `docs/fab/shell-v2.md` §§2, 4, 5, and the before/after table. Rendered the posterior side-wall view and moved its overlapping tail callout. Pinned the CAD extra to build123d 0.11.1 and OCP 7.9.3.1.1 so order-1 reference bytes regenerate unchanged.

**Committed files for the assembled model** (all from solids commit `f7675ec099ffa9e1b5bab14fad3920c5d666262e`):

- Body: `docs/fab/cad/v2/body_full_p15.step`, `docs/fab/cad/v2/body_full_p15.stl` (also `body_full_p15.3mf`).
- Lid: `docs/fab/cad/v2/lid.step`, `docs/fab/cad/v2/lid.stl` (also `lid.3mf`).
- Views from those solids, committed at `11c74615a49653544d4c8b8d28b0076f3090b803`: `docs/fab/cad/v2/render_medial.png` (posterior side-wall inset), `docs/fab/cad/v2/render_lateral.png`, `docs/fab/cad/v2/drawing.pdf`.
- `docs/fab/cad/v2/manifest.json` stamps `f7675ec099ffa9e1b5bab14fad3920c5d666262e`.

## Acceptance / gates

| Gate | Command / result |
|---|---|
| Shell checks on built solid | `OPENBLAS_NUM_THREADS=1 .venv/bin/python scripts/cad/bte_fit_shell.py --params scripts/cad/params/shell_v2.toml --stage shell --out docs/fab/cad/v2/`: **exit 0**, `stage_b_failing []`. `V2_CHARGE_pads` and `V2_WALL_minima` each measure P4/P5 `wall_around` 3.4448 mm, open outer faces and through holes. `V2_BOARD_envelope` body/lid 0 mm³ (previous body 0.0467 mm³). `V2_CLOSURE` lid engagement ≥3 mm and `V2_BOSS_sites`, `V2_TAB_envelope` pass. `V2_CAVITY_v3` records J2/P5 gap −4.93 mm; see below. Inapplicable/unmeasured legacy names remain named in the manifest. |
| Determinism | Two successive runs to `/tmp/elicio-t0001-runA` and `/tmp/elicio-t0001-runB`: all six STEP/STL/3MF and generated manifests byte-identical; six solids also byte-identical to committed `docs/fab/cad/v2/`. The temp manifests use `commit: unknown` because their paths are outside git; the committed manifest matches the solids sha. |
| Manifest/render | `scripts/cad/render.py --out docs/fab/cad/v2/` exit 0; manually inspected medial/posterior and lateral PNGs. `.venv/bin/python scripts/cad/manifest.py --check-bytes docs/fab/cad/v2/manifest.json`: schema 1 ok. Stamp = solids commit. |
| Unit tests | `OPENBLAS_NUM_THREADS=1 LC_ALL=C LANG=C .venv/bin/python -m unittest discover -s tests -v`: **258 tests, OK**, 392.581 s. An initial run with the unpinned new CAD kernel failed 16 order-1 hash comparisons; pinning and rerunning made all 258 green. |
| Order 1 | `PYTHONPATH=tests OPENBLAS_NUM_THREADS=1 .venv/bin/python -m unittest test_cad.CadRegenTests.test_reference_regen_matches_committed_hashes -v`: OK; all 38 files under `docs/fab/cad/v1/` unchanged against HEAD. |
| Tree | `git status --short` empty after output commit. No plan, open-questions, board or packing files edited. No purchases, vendor contact, hardware tests or shell order. |

## Needs a decision / not done

J2's 5.80 × 6.56 mm courtyard at (u 15.15, s 11.35) overlaps the P5 hex standoff well by **4.93 mm** (`V2_CAVITY_v3: j2_p5_standoff_gap = -4.93`). Although the §5e pin-centre cavity test passes, this is **not an assembled fit**. Moving J2 or its tab requires a packing/board decision; the shell alone cannot clear the overlap while respecting the pinned wall sites. Do not order before that is resolved. M1 and fit on a person, physical S4 retention/drop tests, material/colour and Rolf's render approval remain open; CAD views are not photos of a printed part.

This run used the **local Darwin arm64 Mac**, not the Oracle Linux box described in the paused brief; its Python 3.13 CAD wheels installed and ran successfully, so no platform fallback was needed.
