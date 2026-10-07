# WP14d report — shell v2d: width 22 on packing §5c

Lane `w1`, branch `lane/w1-r6`, package WP14d. Merged `origin/main`
first. `plan-v2.md` and `open-questions.md` were not edited. Order 1
files under `docs/fab/cad/v1/` were not written. Packing and board
files were not edited.

## What was built

Same construction path as Stage B v2. `STAGE=shell` now overlays the
§5c width-22 geometry: cavity u 1.50–20.50, island u 2.25–19.75 × s
16.00–37.60, 501012 pack, rib s 14.90–15.70. Outer height 9.0 and
TOTAL_CHORD 47.90 stay. Island bosses sit at the §5c hole sites.
SIG1/SIG2 are neck-end strips. Two flush charging pads sit at P4/P5.
`V2_USB_end` is NOT_APPLICABLE. Overlay
`scripts/cad/params/shell_v2.toml`. Outputs `docs/fab/cad/v2/`. Record
`docs/fab/shell-v2.md` §2, §4, §5. Manifest `provisional: true`.

§5c was read from `/home/user/projects/elicio/.worktrees/w3/docs/fab/packing-v2.md`
at sha `e1f1d6facf37526d358569dace7ebf75ee4e160f`
(`packing(v2c): publish §5c for Q81-Q83`). `V2_BOSS_sites` parses that
table. Sites are not hard-coded in the check.

The tail cannot take two more 5 AF standoffs at u 0.75 and 21.25 (those
points sit in the 1.5 side walls on the medial fillet). Construction is
flush RING_PAD Ø5 stems and domes, Ø2.7 holes, Ø2.10 self-tap pilots.

## Before / after (measured on the built solid)

| Check | WP14c (`7d111c6`) | WP14d |
|---|---|---|
| Width / cell | 20 / 501015 | 22 / pack501012 |
| Cavity u | packing C 1.5–18.5 | 1.50–20.50 |
| Island | u 2.25–17.75 × s 18.6–37.6 | u 2.25–19.75 × s 16.00–37.60 |
| `V2_BOSS` | pass. drop 0.50 at layout fallback sites | pass. drop 0.50 at (13.45, 17.70) and (17.95, 17.70) |
| `V2_BOSS_sites` | (absent) | pass. centre error 0; 3.30 keep gap 0.15 vs every courtyard |
| `V2_BOSS_pilot` | Tail Ø2.10 / 1.92 / 5.94; islands Ø2.10 / 1.45 / 5.00 | Tail Ø2.10 / 1.92 / 5.94; boss 1 Ø2.10 / 1.45 / 5.00; boss 2 Ø2.10 / 2.40 / 6.90 |
| `V2_TAB_envelope` | board-ward tabs | pass. neck-end SIG1 10.71, SIG2 21.81; side walls 1.50; no side pockets |
| `V2_CHARGE_pads` | (absent) | pass. flush pads; nylon between 17.8; P4/P5 clear of REF ≥ 7.81 and screw ≥ 7.39 |
| `V2_USB_end` | NOT_MEASURED packing §5c, Q70 | NOT_APPLICABLE: Q81: no receptacle at M1 52 |
| `V2_CLOSURE` | engagement 4.30, boss wall 3.08 | engagement 4.30, boss wall 6.45 (width 22) |
| `V2_LATERAL_unbroken` | 18 samples, 0 pits | 20 samples, 0 pits |
| `V2_EDGE_radii` | 6 stations, min rise 0.030, rim R 1.08 | 7 stations, min rise 0.025, rim R 1.08 |
| `V2_WALL_minima` | sides 1.50, hinge 1.00 | sides 1.50, hinge 1.00 |
| Build exit | 0 | 0. NOT_APPLICABLE does not fail the build |
| Render stamp | `solids commit ccb66085ad6d` | `solids commit f52afc5b7b25` = solids commit, not HEAD |

Renders (committed):

- `docs/fab/cad/v2/render_medial.png`
- `docs/fab/cad/v2/render_lateral.png`

Solids stamp on both views:
`f52afc5b7b25eb1562aaf916858b9def935d0179`.

## Gates

| Gate | Command | Result |
|---|---|---|
| Full suite | `LC_ALL=C LANG=C .venv/bin/python -m unittest discover -s tests -v` | exit 0. CAD tests ran. First run failed two shell tests: `git show` of §5c decoded as ASCII. Fixed (`encoding="utf-8"`). Second run exit 0 |
| Shell CAD class | `LC_ALL=C .venv/bin/python -m unittest tests.test_cad.CadShellV2Tests tests.test_cad.CadShellV2BuildTests tests.test_cad.CadShellV2StampTests -v` | OK, 7 tests, 146.751 s |
| Order 1 byte-identical | `CadRegenTests.test_reference_regen_matches_committed_hashes` and `CadRenderTests.test_renders_and_drawing_regen_byte_identical` | both ok on the full suite |
| Stage B v2 | `CadStageBV2BuildTests` two consecutive runs | ok. File hashes identical run to run. Width 20 packing C overlay unchanged |
| Shell twice identical | `CadShellV2BuildTests.test_two_consecutive_shell_runs_are_identical` | ok, exit 0, `stage_b_failing: []`, solids equal to `docs/fab/cad/v2/` |
| Stamp equals manifest | `CadShellV2StampTests.test_stamp_text_equals_manifest_commit` | ok |
| Manifest bytes | `.venv/bin/python scripts/cad/manifest.py --check-bytes docs/fab/cad/v2/manifest.json` | schema 1 ok |
| git status | `git status --short` | empty at DONE (this report untracked) |

Plan §9 row 14 (shell v2 body, lid, closure and hook, §7 checks, Stage B
checks on the built solid, identical regeneration): the listed files
exist; §7 and Stage B rows are in the manifest and in `shell-v2.md`;
regeneration tested as above.

The brief asked for last commit message
`shell(v2d): width 22 on §5c, bosses at the hole sites, neck-end strips, tail charging contacts`.
That is `829aeba`. HEAD is `ecfff54` (UTF-8 decode so unittest under
`LC_ALL=C` can read the §5c en-dashes). Solids were not rebuilt after
that one-line change.

## What was not done

No order, quote, or upload. USB opening waits for WP14e if M1 ≥ 58.3.
S4 two-finger pull and 0.5 m drop stay qualitative. Insertion and
retention forces stay NOT_MEASURED (need printed PA12). Board holes at
the boss sites stay the board lane's.

## Needs a decision

1. M1 (Q34). Default 52. Manifest `provisional: true`.
2. Colour, grey or dyed black (Q30).
3. Q17 REF dome on the tail.
4. S4 pull and drop (qualitative, plan v2 §7).
5. Standoff 3.0 vs Harwin 4.0. This file keeps 3.0.
6. WP14e USB if Rolf measures M1 ≥ 58.3.

Q81/Q82/Q83 are built on this solid.

## Final commit sha

`ecfff5486bbbb84b87a550954ecf6febd3acf478`
(`shell(v2d): read packing §5c as UTF-8 under LC_ALL=C`).

Named last-commit message is
`829aeba74e9231c0cc7a9c16b6dd796ef8e3a26d`
(`shell(v2d): width 22 on §5c, bosses at the hole sites, neck-end strips, tail charging contacts`).
Solids sha stamped on the renders:
`f52afc5b7b25eb1562aaf916858b9def935d0179`.
