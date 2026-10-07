# WP14e report — shell v2e: hook-end charging pads per §5d

Lane `w1`, branch `lane/w1-r6`, package WP14e. Merged `origin/main`
first (`bd24e26`). `plan-v2.md` and `open-questions.md` were not edited.
Order 1 files under `docs/fab/cad/v1/` were not written. Packing and
board files were not edited.

## What was built

Same construction path as Stage B v2. `STAGE=shell` keeps the width-22
§5d geometry. P4 and P5 left the tail corners. They sit on the hook-end
medial floor at the §5d folded sites, y 1.50, with flush RING_PAD Ø5
holes through the floor. A rib slot and a drop channel carry the flex
tab from leftover s 16.00. `V2_USB_end` stays NOT_APPLICABLE. Overlay
`scripts/cad/params/shell_v2.toml`. Outputs `docs/fab/cad/v2/`. Record
`docs/fab/shell-v2.md` §2, §4, §5. Manifest `provisional: true`.

§5d was read from `lane/w3` at sha
`408a4765ec953d6cc84210fd3e5632185ff95cbb`
(`packing(v2e): give P4/P5 Q85 flat centres through the rib-slot fold`).
`V2_BOSS_sites` / `V2_CHARGE_pads` parse the folded-site table for
P1–P5. Sites are not hard-coded in the check. P1–P3 are unchanged.

Construction is flush RING_PAD Ø5 through the floor (the tail cannot
take two Ø5 pads). Hex standoffs stay on SIG1/SIG2/REF only.

## Before / after (measured on the built solid)

| Check | WP14d (`ecfff54`) | WP14e |
|---|---|---|
| Width / cell | 22 / pack501012 | 22 / pack501012 |
| `V2_BOSS` | pass. drop 0.50 at (13.45, 17.70) and (17.95, 17.70) | pass. same sites, drop 0.50 |
| `V2_BOSS_sites` | pass. centre error 0; keep gap 0.15; packed from §5c | pass. centre error 0; keep gap 0.15; P1–P5 from §5d folded table sha `408a476` |
| `V2_BOSS_pilot` | Tail Ø2.10 / 1.92 / 5.94; boss 1 Ø2.10 / 1.45 / 5.00; boss 2 Ø2.10 / 2.40 / 6.90 | Tail Ø2.10 / 1.92 / 5.94; boss 1 Ø2.10 / 1.45 / 5.00; boss 2 Ø2.10 / 2.40 / 6.90 |
| `V2_TAB_envelope` | pass. neck-end SIG1 10.71, SIG2 21.81; side pockets 0 | pass. same strips; rib slot air 1; drop channel air 1; side pockets 0 |
| `V2_CHARGE_pads` | pass. flush pads at tail (0.75, 44.0) and (21.25, 44.0); nylon between 17.8 | pass. flush Ø5 floor pads at (14.70, 4.30) and (17.70, 11.72); nylon between 3.00; floor 1.50; cell gap 0.30 / 3.30; creepage nylon 1.0 |
| `V2_USB_end` | NOT_APPLICABLE: Q81: no receptacle at M1 52 | NOT_APPLICABLE: Q81: no receptacle at M1 52 |
| `V2_CLOSURE` | engagement 4.30, boss wall 6.45 | engagement 4.30, boss wall 6.45 |
| `V2_LATERAL_unbroken` | 20 samples, 0 pits | 20 samples, 0 pits |
| `V2_EDGE_radii` | 7 stations, min rise 0.025, rim R 1.08 | 7 stations, min rise 0.025, rim R 1.08 |
| `V2_WALL_minima` | sides 1.50, hinge 1.00 | sides 1.50, hinge 1.00 |
| Build exit | 0 | 0. NOT_APPLICABLE does not fail the build |
| Render stamp | solids `f52afc5` | solids `9734c3418445` = `manifest.commit` |

Renders (committed):

- `docs/fab/cad/v2/render_medial.png`
- `docs/fab/cad/v2/render_lateral.png`

Both views stamp solids commit
`9734c34184451cbac9a76a7d0a5caa45fdfb3ed0`.
Pads are labelled `P4/P5 charging pads, hook end (Q86)`.

## Gates

| Gate | Command | Result |
|---|---|---|
| Full suite | `LC_ALL=C LANG=C .venv/bin/python -m unittest discover -s tests -v` | exit 0 |
| Shell CAD class | `LC_ALL=C .venv/bin/python -m unittest tests.test_cad.CadShellV2Tests tests.test_cad.CadShellV2BuildTests tests.test_cad.CadShellV2StampTests -v` | OK, 7 tests, 142.133 s |
| Order 1 byte-identical | `CadRegenTests.test_reference_regen_matches_committed_hashes` and `CadRenderTests.test_renders_and_drawing_regen_byte_identical` | both ok on the full suite |
| Stage B v2 | `CadStageBV2BuildTests.test_two_consecutive_v2_stage_b_runs_are_identical` | ok |
| Shell twice identical | `CadShellV2BuildTests.test_two_consecutive_shell_runs_are_identical` | ok, `stage_b_failing: []`, solids equal to `docs/fab/cad/v2/` |
| Stamp equals manifest | `CadShellV2StampTests.test_stamp_text_equals_manifest_commit` | ok |
| Manifest bytes | `.venv/bin/python scripts/cad/manifest.py --check-bytes docs/fab/cad/v2/manifest.json` | schema 1 ok |
| git status | `git status --short` | empty at DONE (this report untracked) |

Plan §9 row 14 (shell v2 body, lid, closure and hook, §7 checks, Stage B
checks on the built solid, identical regeneration): the listed files
exist; §7 and Stage B rows are in the manifest and in `shell-v2.md`;
regeneration tested as above.

Last commit message is
`shell(v2e): charging pads on the hook-end floor per §5d, rib slot and drop channel`.

## What was not done

No order, quote, or upload. USB opening waits if M1 ≥ 58.3. S4
two-finger pull and 0.5 m drop stay qualitative. Insertion and
retention forces stay NOT_MEASURED (need printed PA12). Board holes and
the Q84 DRC rule stay the board lane's. The cell-side drop at u 11.90
is not used (packing extras).

## Needs a decision

1. M1 (Q34). Default 52. Manifest `provisional: true`.
2. Colour, grey or dyed black (Q30).
3. Q17 REF dome on the tail.
4. S4 pull and drop (qualitative, plan v2 §7).
5. Standoff 3.0 vs Harwin 4.0. This file keeps 3.0.
6. Q86: Rolf can overrule the hook-end pads with Ø2.1 pads on the tail.

Q81/Q82/Q83/Q86 are built on this solid.

## Final commit sha

`bdfc429481f1bd0589b2c157dcf7c42e6c75f726`
(`shell(v2e): charging pads on the hook-end floor per §5d, rib slot and drop channel`).

Solids sha stamped on the renders:
`9734c34184451cbac9a76a7d0a5caa45fdfb3ed0`.
§5d sha:
`408a4765ec953d6cc84210fd3e5632185ff95cbb`.
