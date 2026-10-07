# WP2 report — gauge script and order 1 files

Lane `w2`. Branch `lane/w2`. Final commit `47749e19619a9063a5a226b4b4edf6415e64f26b`.
Python 3.13.15 with build123d 0.11.1. No 3.12 fallback was needed.

## What was built

- `scripts/cad/bte_fit_shell.py` — build123d generator for the §3 fit gauge.
- `scripts/cad/params/default.toml` — reference-ear defaults.
- `scripts/cad/params/rolf.toml` — measurement overlay (empty keys take defaults and mark REF).
- `scripts/cad/README.md` — install, reference build, measurement build, checks.
- `cad` optional-dependency group in `pyproject.toml` (`build123d>=0.7`, `trimesh>=4`).
- `docs/fab/cad/v1/` — five files, each STEP + STL + 3MF: `body_full_p15`, `body_thin_p15`, `body_full_p25`, `lid`, `coupon`.
- `docs/fab/cad/v1/manifest.json` — parameters, clamped CREASE_BOW, chord gate, WIRE_CHANNEL openings, E1–E5, §3.6 fits, interference, SHA-256, quantities.
- `tests/test_cad.py` — math, matrix/M1 failures, identical regeneration.

The path `P(u,s,y)` uses the signed-off formula from turn 06. CREASE_BOW from M1/M2 is clamped 1–8 (open item 1). The chord gate is M1 ≥ TOTAL_CHORD + 3. MOCK_CONTACTS is true: gauge bodies carry Ø4.7 × 1.35 caps on −Y and do not cut holes, pocket, or channel.

A post-commit hook pushed `lane/w2` to origin. The lane brief said never push. The hook did it. This lane did not run `git push`.

## Plan §9 acceptance (WP2)

| Item | How | Result |
|---|---|---|
| All §3.3 checks | `.venv/bin/python scripts/cad/bte_fit_shell.py --checks-only` and the `checks` array in `manifest.json` (60 entries) | All passed. Matrix, walls, E1–E5 minima, M1 gate 50.9005 mm, hook inner radius, WIRE_CHANNEL openings at bows 1/3/8, one solid per part, seated lid/body overlap 0 mm³, STL watertight after vertex merge, contact caps on −Y. |
| Exceptions and interference in the manifest | Read `docs/fab/cad/v1/manifest.json` | E1–E5 present. `lid_body_overlap_mm3` = 0.0. Fit table from §3.6 present. SPAN = 10.35 vs M3 = 11. Pinna displacement = 0. |
| Identical regeneration | Export to `docs/fab/cad/v1` then to a temp dir; `tests.test_cad.CadRegenTests.test_reference_regen_matches_committed_hashes` | All 15 CAD files matched SHA-256. STEP timestamp pinned. 3MF UUIDs rewritten after Lib3MF write. |

## Gates

| Gate | Command | Result |
|---|---|---|
| Unit tests | `.venv/bin/python -m unittest discover -s tests -v` | 53 tests OK, including 11 CAD tests. |
| Script twice | `.venv/bin/python scripts/cad/bte_fit_shell.py --out docs/fab/cad/v1/` then `--out /tmp/elicio-cad-regen3` | 15/15 hashes identical. |

Failing cases (parameter and number in the message):

- `VARIANT=medium` → `CHECK FAIL: VARIANT=medium: must be full or thin`
- `HOOK_PRELOAD=3` → `CHECK FAIL: matrix: ... HOOK_PRELOAD=3.0`
- `M1=40` → `CHECK FAIL: M1_gate: ... (M1=40.0, TOTAL_CHORD=47.9005, gate=50.9005)`

## What was not done

- Renders and `drawing.pdf` — WP3 owns those.
- No order, upload, quote, or vendor contact.
- Stage B holes, reference pocket, WIRE_CHANNEL cut, and CABLE_EXIT — MOCK_CONTACTS is true for order 1. The script can cut them when MOCK_CONTACTS is false. Stage B keep-out and Ø1.3 wire-envelope containment were not run on solids.
- `body_thin_p25` — allowed by the matrix, not in the §3.6 order-1 file list.
- Coupon-to-parameter mapping was not written into `docs/fab/interface.md` (WP1 owns that file). The mapping is in the script docstring and README.

## Needs a decision

1. **Tip round 4.0 (§3.5 step 2).** The two vertical tip edges take at most 1.60 mm on the full bodies (medial fillet 1.5 already occupies the same corner). Thin: no valid tip fillet. Closest geometry: lofted tail to width 10, fillet 1.60 where it holds. Reading: 4.0 mm needs a tail section without the medial fillet, or a plan-view cap built as its own solid.

2. **Hook joint fillet 2.0 (§3.5 step 9).** HOOK_DIA/2 is 1.75 mm, so a 2.0 mm fillet cannot sit on the tube. No stable intersection-loop edges were found. Closest geometry: hook union with the rotated body, no joint fillet. Reading: drop the radius below 1.75 mm, or fillet in the body frame before rotate.

3. **§3.3 gate wording.** The table says `TOTAL_CHORD > M1 − 3`. The signed-off rule is M1 ≥ TOTAL_CHORD + 3 (50.9 at bow 3, 51.3 at bow 1). This lane implemented the latter. Confirm that reading.

4. **Default CREASE_BOW vs M1/M2.** Default M1=52 and M2=58 give a computed bow of 11.00, clamped to 8. The reference build keeps CREASE_BOW=3.0 from `default.toml`. Rolf's file computes bow only when CREASE_BOW is omitted. Confirm that split.

5. **One lid file.** Exported lid is VARIANT=full, HOOK_PRELOAD=1.5. Thin has LID_Y=6.0. Order 1 quantities are lid ×2 for the full-body closure test. Confirm thin does not need its own lid file.

6. **Open item 2 (coupon mapping).** Holes Ø1.7 / 2.9 / 3.4; slots 0.9 and 0.4; rib 0.4. CONTACT_HOLE is 2.9. Slot 0.9 is TONGUE_SLOT height. E4 is the 0.4 rib. WP1/WP6 should copy this into the interface v2 note.

7. **Open item 4.** Physical opening at u=9.3 is 0.938 mm at bow 3, 1.089 at bow 1, 0.537 at bow 8. All positive. End section at s=40.5 is inside the pocket (distance 2.84 mm < 3.75). Stage B containment of the Ø1.3 wire envelope is still due when MOCK_CONTACTS is false.

## Final commit

`47749e19619a9063a5a226b4b4edf6415e64f26b`
