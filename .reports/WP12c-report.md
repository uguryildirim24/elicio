# WP12c report — Route the flex board to DRC 0 (lane w2)

Worktree: `/home/user/projects/elicio/.worktrees/w2`
Branch: `lane/w2`
Package: WP12c
Date: 2026-09-18
KiCad: 10.0.6 (`kicad-cli`)
Java: Homebrew OpenJDK 21.0.12.1 (`/opt/homebrew/opt/openjdk@21/bin/java`)
Continuing from: `480e355`
Final commit: `f4376ca9eac250ea38eba2690eed312f34012943`

## What was built

First commit `ca484d5` dropped the WP12b shorting B.Cu bus (465 segments, 134 vias). Footprints were not moved. Named SMT centres still match packing-v2.md §5.

Freerouting v2.1.0 was run headless (`gui.enabled=false`, `-mp`, `-dct`, wall-clock timeout). `kicad-cli pcb export` has no `specctra` subcommand; DSN came from `pcbnew.ExportSpecctraDSN` (58492 bytes). Every run froze after `Job started`. No SES. No hs_err dump. Redo log: `hardware/board/route.md`.

Own router: `maze_route.py` is now a clearance-aware A* (Default 0.10 mm, ring 7×7 keep-outs, one net per tab, no shorting bus). Trial on a copy: 23 nets routed, 25 failed, 420 tracks, DRC 770 errors. That copper was **not** written back.

The committed board stays un-shorted and un-routed: 0 tracks, 0 vias. `routed: false`. Last commit is not `board(v2c): routed to DRC 0`.

`docs/fab/board-v2.md` §15 only. Schematic, project rules, `scripts/` untouched vs `480e355`.

Nothing ordered, quoted or uploaded. No vendor contact.

## Gates

### 1. Unittest (this package)

```text
.venv/bin/python -m unittest tests.test_board_release -v
```

Result: **OK** (5 tests). ERC 0. BOM rows = placed parts = 59. `"routed": false` without `--routed`. `--routed` refused (`drc_errors` 128, `unconnected_items` 132, `no_tracks` 1). `pcb_tracks` = 0. Named SMT centres within 0.1 mm of packing §5. WP12c assertion: order release stays un-routed.

```text
.venv/bin/python -m unittest discover -s tests -v
```

Result: 171 tests, **13 FAIL**, all `test_cad.CadRegenTests` v1 solid hashes (`body_full_p15`, `body_full_p25`, `body_thin_p15`, `lid`). This package does not own CAD. Same 13 as WP12b.

### 2. `release.py --routed`

```text
.venv/bin/python scripts/board/release.py --board-dir hardware/board --out /tmp/wp12c-release --routed
```

| Field | Value |
|---|---|
| exit | 1 (`routed release refused`) |
| erc_errors | 0 |
| erc_warnings | 0 |
| drc_errors | 128 |
| drc_warnings | 21 |
| unconnected_items | 132 |
| pcb_tracks | 0 |
| pcb_pads_without_net | 0 |
| routed | true (flag only; order release is not green) |
| bom_rows | 59 |
| placed_parts | 59 |

Non-`--routed` job still exits 0 (ERC 0, outputs present).

**This gate is not met.** DRC 0 is not reachable on this placement with frozen footprints and frozen `elicio-v2.kicad_pro`.

### 3. Forbidden paths vs `480e355`

```text
git diff 480e355 -- hardware/board/elicio-v2.kicad_sch hardware/board/elicio-v2.kicad_pro scripts/ docs/fab/board-v2.md
```

Result: schematic, project file, and `scripts/` empty. `docs/fab/board-v2.md` is §15 only (`@@ -397,22 +397,27 @@`).

### 4. `git status --short`

Empty.

## Plan §9 / brief deliverables

| Item | Result |
|---|---|
| Drop shorting bus first | `ca484d5`. 0 tracks, 0 vias. |
| Diagnose Freerouting hang | Done. Java 21.0.12.1. Log in `route.md`. No SES. |
| Own router if hang | A* with netclass Default 0.10 mm and ring keep-outs. Trial on a copy only. |
| `release.py --routed` exit 0 | **Fail.** 128 DRC, 132 unconnected, 0 tracks. |
| Contact isolation as WP12b | Unchanged: 7×7 ring keep-outs. Contact 1.0 mm vs 0402 still DRC-fails on pads. |
| Nothing new under RF keep-out | No new copper. |
| USB pairs short and matched | Not routed. Rule that would apply: nRF52840 USB is FS; ≤ 1.0 mm length delta on the tongue. |
| `board-v2.md` §15 | Rewritten. Via count 0. No analog trace. No hand-fix. |
| Routed assertion | `test_order_release_stays_unrouted`: tracks 0, DRC > 0, `--routed` refused. |

## What blocks DRC 0 (un-routed board, `kicad-cli pcb drc`)

These errors exist with **zero tracks**. A router cannot clear them without moving footprints or editing `elicio-v2.kicad_pro` (both frozen for WP12c):

| Type | Count | Examples |
|---|---|---|
| solder_mask_bridge | 38 | J3 vs SW1, J2 vs J4, U5 vs J4 |
| shorting_items | 32 | J2 MP GND vs J4 +VDD; C15 GND vs C8 +3V0; J3 SIG1 vs SW1 nRESET |
| Contact clearance 1.0 mm | 26 | R1/R2/R3 0402 pad gap 0.48 mm; J3 2.54 mm pitch |
| copper_edge_clearance | 18 | U2 pads 0.275 mm vs 0.300 mm; J2 at the outline |
| hole_clearance | 9 | J4 NPTH vs U5; J1 NPTH vs leftover B.Cu |
| items_not_allowed | 5 | J2 and U5 in J4 keep-out; U3 in U1 keep-out; R25/C10 in RF_FEED_NOTCH |

Maze copper on a copy made this worse (770 errors). It was discarded.

## What was not done

- DRC 0 / 0 unconnected / `release.py --routed` exit 0.
- Import of a Freerouting SES (none written).
- USB pair length match (no USB tracks).
- Hand-placed residue on the committed file (no route to fix).
- Full one-hour Freerouting wall clock on a single process: the job dies or freezes after `Job started` with no further log (180 s, 90 s, ~2 min, dead before 12 min). Same hang as WP12b (240 s). Extra time does not change the placement DRC.

## Needs a decision

1. Contact netclass 1.0 mm vs 0402 220 kΩ on a 2.5 mm tab (pad gap 0.48 mm) and vs J3 2.54 mm pitch. Isolation today is the 7×7 ring keep-out. DRC 0 needs a different Contact clearance or a different tab/header land.
2. Packing leftovers collide: J4 vs J2/U5, U3 vs U1 courtyard, U2 0.025 mm inside copper-to-edge, C15 vs C8, J3 vs SW1. WP12c must not move those footprints.
3. Freerouting v2.1.0 headless on this Mac never writes SES. A later lane can try v2.4.1 (the jar prints that version as available) or a different DSN path. That still does not clear (1) or (2).

## Commits

| SHA | Message |
|---|---|
| `ca484d5` | `board(v2c): drop the shorting bus fallback` |
| `d0a081b` | `board(v2c): clearance-aware maze after Freerouting hang` |
| `184c43a` | `docs(board-v2): record un-routed DRC after dropping the bus` |
| `845bac7` | `test(board-v2): assert WP12c stays un-routed` |
| `f4376ca` | `merge origin/lane/w2: restore e3e085b after the WP12c reset` |

Merge restored `e3e085b` (L7 quotes, schematic, `patch_sch_v2b.py`) on top of WP12c. `docs/fab/board-v2.md` auto-merged: L7 quotes and §15 both kept. `git push` fast-forwarded `origin/lane/w2` `e3e085b..f4376ca`. Working tree empty. Do not reset this lane below its pushed tip again.
