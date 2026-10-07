# WP14c report — shell v2c: concealed screw, boss pilots, render stamp

Lane `w1`, branch `lane/w1-r6`, package WP14c. Merged `origin/main`
(`7b23eb5`, Round 7 briefs) first. `plan-v2.md` and `open-questions.md`
were not edited. Order 1 files under `docs/fab/cad/v1/` were not written.

## What was built

Same construction path as Stage B v2. `STAGE=shell` now puts the Q71
head well on the medial tail (skin hides it). The lateral lid is not
cut. CAD pilots are Ø2.10 with boss OD ≥ 5.0 at the tail and the two
island bosses (L8 §4). `render.py` stamps the manifest commit that
built the solids, or the tree hash plus `dirty` when STEP/STL/3MF
differ from HEAD. Overlay `scripts/cad/params/shell_v2.toml`. Outputs
`docs/fab/cad/v2/`. Record `docs/fab/shell-v2.md` §2, §4, §5. Manifest
`provisional: true`.

USB opening and tab-fold pockets wait for packing §5c (WP11d, Q70).

## Before / after (measured on the built solid)

| Check | WP14b (`bb0c788`) | WP14c |
|---|---|---|
| `V2_CLOSURE` | pass. Hinge undercut 1, engagement 4.00, boss wall 3.13, well on the lid | pass. Hinge undercut 1, lip in 1, engagement 4.30, boss wall 3.08, well air 1, well on the medial tail |
| `V2_LATERAL_unbroken` | (absent; lid well visible) | pass. 18 samples, 0 pits, old lid-well site nylon |
| `V2_BOSS_pilot` | (absent; CAD pilot Ø2.0) | pass. Tail Ø2.10 / wall 1.92 / OD 5.94; both islands Ø2.10 / 1.45 / 5.00 |
| `V2_BOSS` | pass. drop 0.50 | pass. drop 0.50, island tops 0.5 below standoff |
| `V2_EDGE_radii` | pass. flat_stations 0, lid_rim_R 1.08 | pass. stations 6, flat_stations 0, min rise 0.030, lid_rim_R 1.08 |
| `V2_USB_end` | NOT_MEASURED packing §5b, Q70 | NOT_MEASURED packing §5c, Q70; hook-end wall left solid |
| Build exit | 0 | 0. USB row is NOT_MEASURED by name and does not fail the build |
| Render stamp | `c68d4b2839c9` (reviewer solids) | `solids commit ccb66085ad6d` = `manifest.commit` |

Renders (committed):

- `docs/fab/cad/v2/render_medial.png`
- `docs/fab/cad/v2/render_lateral.png`

Solids commit stamped on both views:
`ccb66085ad6dcd82ff379c60afd1d86d10ad294b`.

## Gates

| Gate | Command | Result |
|---|---|---|
| Full suite | `.venv/bin/python -m unittest discover -s tests -v` | OK, 207 tests, 283.181 s, CAD tests ran |
| Order 1 byte-identical | `CadRegenTests.test_reference_regen_matches_committed_hashes` and `CadRenderTests.test_renders_and_drawing_regen_byte_identical` | both ok |
| Stage B v2 | `CadStageBV2BuildTests` vs `STAGE_B_V2_MEASURED`; two consecutive runs | ok. Q59 still fail on the unslotted Stage B path. File hashes identical run to run |
| Shell twice identical | `CadShellV2BuildTests.test_two_consecutive_shell_runs_are_identical` | ok, exit 0, `stage_b_failing: []`, solids equal to `docs/fab/cad/v2/` |
| Stamp equals manifest | `CadShellV2StampTests.test_stamp_text_equals_manifest_commit` | ok |
| Manifest bytes | `.venv/bin/python scripts/cad/manifest.py --check-bytes docs/fab/cad/v2/manifest.json` | schema 1 ok |
| git status | `git status --short` | empty at DONE (this report untracked) |

Plan §9 row 14 (shell v2 body, lid, closure and hook, §7 checks, Stage B
checks on the built solid, identical regeneration): the listed files
exist; §7 and Stage B rows are in the manifest and in `shell-v2.md`;
regeneration tested as above.

## What was not done

No order, quote, or upload. USB opening waits for WP11d packing §5c
(Q70). S4 two-finger pull and 0.5 m drop stay qualitative. Insertion
and retention forces stay NOT_MEASURED (need printed PA12). The Ø2.7
holes in the board island stay the board lane's.

## Needs a decision

1. M1 (Q34). Default 52. Manifest `provisional: true`.
2. Colour, grey or dyed black (Q30).
3. Q17 REF dome on the tail.
4. S4 pull and drop (qualitative, plan v2 §7).
5. Standoff 3.0 vs Harwin 4.0. This file keeps 3.0.
6. Q70 USB: packing §5c (WP11d). This shell does not cut the opening.

Q59 stays the slot. Q71 is built on this solid: medial-tail well, lateral
lid unbroken.

## Final commit sha

`7d111c6ab40925dcf2345ce1ada4e07afe9df617`
(`shell(v2c): concealed screw, boss pilots, render stamp`).
