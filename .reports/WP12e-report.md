# WP12e report — Contact by area, pin table v2 flat pattern, route to DRC 0 (lane w2)

Worktree: `/home/user/projects/elicio/.worktrees/w2`
Branch: `lane/w2`
Package: WP12e
Pane: `w1B:pB`
Date: 2026-09-18
KiCad: 10.0.6 (`kicad-cli`)
Java: Homebrew OpenJDK 25 (`/opt/homebrew/opt/openjdk@25/bin/java`)
Jar: `~/.local/opt/freerouting/freerouting-2.4.1.jar`
Pin table v2: `408a476` (`git show 408a476:docs/fab/packing-v2.md` §5d)
Final commit: `30ca79d7b31b834c7096a88c8f31f83b125f40f3`

## What was built

`git merge origin/main` first (Q86 on main). Pin table v2 copied to `hardware/board/packing_v2_flat.md`. Folded-site table omitted. `packing_5c_norec.md` deleted.

Parser: flat `u,s` (or `x,y`) plus side; skip folded (`pad`/`y` without `rot`); J4 keep-out `keep` column is diameter Ø1.39; `F.Cu and B.Cu` forbids B.Cu.

Place: 66 table parts + H1/H2 = 68 footprints. 38 flipped to B.Cu. Flat rings P1 (5.90, 5.29), P2 (10.40, −5.81), P3 (8.50, 43.00), P4 (37.47, 2.80), P5 (30.05, 5.80). CHARGE rectangle centre (33.02, 4.30) 14.50 × 8.60 is Edge.Cuts. SIG1/SIG2 `tab_detour` from s=16.00 toward −s. REF tab from s=37.60. J4 NPTH keep-out Ø1.39 on B.Cu at the KiCad hole centres. Q84 `tabs` / `tail_pads` (CHARGE in `tail_pads`). Tracks 0.

Hole nudges inside 0.1 mm: R23 +0.09 u, R26 −0.05 u. R24 not moved (needs 0.46 mm).

Freerouting 2.4.1 on OpenJDK 25 (`--gui.enabled=false -mp 8 -mt 4`, 75.47 s) wrote `/tmp/wp12e/elicio-v2.ses` (22585 bytes). Import on a copy: 268 tracks, 12 vias, **317** DRC errors (was 2). Shorts 0. SES **not** written to the owned PCB.

Step 5: stop **un-shorted**, `routed: false`. Last commit: `board(v2e): placed on the flat pattern, not routed`.

`scripts/board/release.py` was not edited. `firmware/src/board_pins.h` was not edited.

Nothing ordered, quoted or uploaded. No vendor contact.

## Gates

### 1. Unittest (this package)

```text
.venv/bin/python -m unittest tests.test_board_release -v
```

Result: **OK** (14 tests). ERC 0. BOM rows = placed parts. `"routed": false` without `--routed`. `--routed` refused (`drc_errors` 2, `unconnected_items` 146, `no_tracks` 1). `pcb_tracks` = 0. Named SMT centres within 0.1 mm of `packing_v2_flat.md`. P4/P5 at (37.47, 2.80) and (30.05, 5.80). J1/U5 absent. H1/H2 at the Q82 sites. Q84: no Contact-clearance on R1–R3.

```text
.venv/bin/python -m unittest discover -s tests -v
```

Result: **14 FAIL**, all CAD, this package does not own:

- `test_cad.CadRegenTests.test_reference_regen_matches_committed_hashes` × 13 (`body_full_p15` 3mf/step/stl, `body_full_p25` 3mf/step/stl, `body_thin_p15` 3mf/step/stl, `lid` 3mf/step/stl, plus one more hash row)
- `test_cad.CadShellV2BuildTests.test_two_consecutive_shell_runs_are_identical`

Same 14 as WP12d. `[cad]` extras were not installed.

### 2. ERC

```text
kicad-cli sch erc --format json
```

**0 errors, 0 warnings.**

### 3. DRC (owned PCB, 0 tracks)

```text
kicad-cli pcb drc --format json
Found 2 violations
Found 146 unconnected items
   1 hole_clearance
   1 solder_mask_bridge
```

Both: Pad 2 [GND] of R24 on B.Cu vs J4 NPTH. Copper-edge 0. Shorts 0.

Paste and first structural reason: `hardware/board/route.md` §9 and `docs/fab/board-v2.md` §15.

### 4. `release.py`

Without `--routed`: exit **0**. `routed: false`. Gerbers, BOM, CPL, STEP written.

With `--routed`: exit **1**. `routed release refused` on DRC errors, unconnected items, and no tracks.

## What was not done

DRC 0 and 0 unconnected were not reached. `--routed` with `routed: true` was not released. Gerbers/BOM/CPL exist from the non-`--routed` job only. One Contact trace per tab was not routed (no tracks).

## Needs a decision

Pin table v2 J4 keep-out XY (pair at s=27.14) does not match KiCad Tag-Connect TC2030 at (16.25, 24.60) rot 90 (pair at s=22.06). R24 on B.Cu sits on the real hole at (17.266, 22.06). Clearing it needs 0.46 mm, past the 0.1 mm pin. Packing (or a J4 rotation that matches the table) must keep B.Cu pads out of the KiCad hole sites before a router can reach DRC 0.

## First structural reason

R24 pad 2 [GND] on B.Cu occupies J4 NPTH. Stop un-shorted. `routed: false`.
