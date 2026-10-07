# WP12g report — Contact creepage at the exposed lands only (Q88), route to DRC 0 (lane w2)

Worktree: `/home/user/projects/elicio/.worktrees/w2`
Branch: `lane/w2`
Package: WP12g
Pane: `w1B:pB`
Date: 2026-09-18
KiCad: 10.0.6 (`kicad-cli`)
Java: Homebrew OpenJDK 25.0.4.1 (`/opt/homebrew/opt/openjdk@25/bin/java`)
Jar: `~/.local/opt/freerouting/freerouting-2.4.1.jar`
Pin table v2.1: `e4b857c` on `lane/w3`
Final commit: `8348e62526bda3874338e4a9c5a82f67cdd2a4dc`

## What was built

`git merge origin/main` first (`c59e9db`, merge of `e06262f`: Q88, WP12g brief). Work stayed on top of `fbd56e6`. No rebase.

Q88: `tabs` is three 7 × 7 boxes around P1–P3. `tail_pads` is two 7 × 7 boxes around P4–P5. Coverlaid strips carry one Contact 0.15/0.20 trace and a foreign-net keep-out. Island Contact stays 0.20.

R24 from pin table v2.1 (18.49, 22.57) rot 90 is copper-clean (zero-track DRC 0). Distance to vendored v2 (18.28, 22.37) is 0.29 mm. Q87 deviation closes. R23 and R26 match v2.1 within 0.1 mm.

Locked Contact: ring → strip centre → island → R1–R3. VBUS stub on the CHARGE south edge. GND to J2 pad 2, split at the P5 7 × 7. Locked-only DRC:

```text
kicad-cli pcb drc --format json
Found 1 violations
Found 142 unconnected items
locked DRC errors 0 warnings 1 unconnected 142
types Counter({('track_dangling', 'warning'): 1})
```

DSN (`scripts/board/route_v2.py --dsn-check`): Default 100/100 um, Contact 150/200 um. Via first 700:300, then JLC 550:300 because 0.70 blocked F.Cu↔B.Cu.

Freerouting 2.4.1 on OpenJDK 25, `-mp 20`, fanout `max_passes=80`, job timeout 20 min, `strict_drc`, neck 100 um, copper-to-edge 300 um, hole 200 um.

| Run | Wall | Fanout | Auto-route | Copy DRC | Tracks / vias |
|---|---|---|---|---|---|
| 0.70 via | 2 m 40.80 s | locks already on; 80 passes | 20 passes, 70 unrouted, 28 violations | 0 errors, 70 unconnected | 353 / 23 |
| 0.55 via (imported) | 1 m 37.38 s | 123/230 (53.5 %) | 20 passes, 67 unrouted, 30 violations | 0 errors, 63 unconnected | 421 / 33 |

Foreign nets in strips: 0. SES imported into the owned PCB (0.55 run). A later GND pour plus J3 manhattan produced 15 DRC errors including SIG1/SIG2 shorts and was discarded.

Owned PCB: 421 tracks, 33 vias, DRC **0 errors**, 3 warnings (2 `via_dangling`, 1 `track_dangling`), **63 unconnected**, 0 shorts. `routed: false`.

Last commit: `board(v2g): Q88 lands, not routed`.

`docs/fab/plan-v2.md` and `docs/fab/open-questions.md` were not edited. Firmware was not edited. Packing and the shell were not edited.

Nothing ordered, quoted or uploaded. No vendor contact.

## Gates

### 1. Unittest (this package)

```text
.venv/bin/python -m unittest tests.test_board_release -v
```

Result: **OK** (18 tests). ERC 0. BOM rows = placed parts. `"routed": false` without `--routed`. `--routed` refused on `unconnected_items` 63. `pcb_tracks` > 0. R24 within 0.50 mm of the v2 table. Q88: no 1.0 mm creepage at L1/D2/U1 strip roots; foreign GND in a strip fails DRC; strip keep-out names present.

```text
.venv/bin/python -m unittest discover -s tests -v
```

CAD-related modules: **14 FAIL**, this package does not own:

- `test_cad.CadRegenTests.test_reference_regen_matches_committed_hashes` × 13 (`body_full_p15` 3mf/step/stl, `body_full_p25` 3mf/step/stl, `body_thin_p15` 3mf/step/stl, `lid` 3mf/step/stl, plus one more hash row)
- `test_cad.CadShellV2BuildTests.test_two_consecutive_shell_runs_are_identical`

Same 14 as WP12f. `[cad]` extras were not installed.

### 2. ERC

```text
kicad-cli sch erc --format json
```

**0 errors, 0 warnings** (from the release job in the board tests).

### 3. DRC

Locked-only (paste above): 0 errors, 1 warning, 142 unconnected.

Owned PCB after SES:

```text
kicad-cli pcb drc --format json
Found 3 violations
Found 63 unconnected items
types: via_dangling × 2 (warning), track_dangling × 1 (warning)
shorts 0
```

Paste and first structural reason: `hardware/board/route.md` §11 and `docs/fab/board-v2.md` §15.

### 4. `release.py`

Without `--routed`: exit **0**. `routed: false`. Gerbers, BOM, CPL, STEP written.

With `--routed`: exit **1**. `routed release refused` on unconnected items (63). DRC errors 0 (dangling is a warning).

## What was not done

DRC 0 errors and 0 unconnected were not reached together. `--routed` with `routed: true` was not released. J3 Contact, U2 QFN escapes, J4 SWD, and VBUS from P4 onto the island stay open.

## Needs a decision

The island still has 63 rats after Q88. Packing or a later board pass must open channels for U2, J4, J3, and CHARGE VBUS, or accept that Stage B stays un-routed. R24 v2.1 rot 90 is the copper truth (Q87 closed on this land).

## First structural reason

63 unconnected after Q88, locked Contact to R1–R3, and Freerouting with via 0.55/0.30. Remaining rats are U2 QFN escapes, J4 SWD, VBUS P4→island, J3 Contact, and layer stitches. A GND pour plus J3 manhattan shorted SIG1/SIG2 and was discarded. Stop un-shorted. `routed: false`.
