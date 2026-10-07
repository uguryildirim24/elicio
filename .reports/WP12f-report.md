# WP12f report — route pin table v2 to DRC 0 (lane w2)

Worktree: `/home/user/projects/elicio/.worktrees/w2`
Branch: `lane/w2`
Package: WP12f
Pane: `w1B:pB`
Date: 2026-09-18
KiCad: 10.0.6 (`kicad-cli`)
Java: Homebrew OpenJDK 25.0.4.1 (`/opt/homebrew/opt/openjdk@25/bin/java`)
Jar: `~/.local/opt/freerouting/freerouting-2.4.1.jar`
Pin table v2: `408a476`
Final commit: `fbd56e648bc0aa704615a6cd8420e1b431b69769`

## What was built

`git merge origin/main` first (`8d3a2ac`, briefs WP12f/WP11f and Q87).

R24 moved +0.47 mm u (Q87). R23 +0.09 mm u and R26 −0.05 mm u stay inside 0.1 mm. Zero-track DRC **0 errors**, 146 unconnected, 0 shorts.

Netclasses set to JLC 1 oz flex §12: Default track/clearance 0.10/0.10 mm, Contact 0.15/0.20 mm, via 0.70/0.30 mm. DSN (`scripts/board/route_v2.py --dsn-check`):

```text
(via "Via[0-1]_700:300_um")
(width 100)
(clearance 100)
(class kicad_default … (width 100) (clearance 100))
(class Contact REF SIG1 SIG2 (width 150) (clearance 200))
```

WP12e 199 `track_width` (min 0.2000 mm, actual 0.1000 mm): the DSN already had 100 µm. SES import leaked Contact onto Default unless `elicio-v2.kicad_pro` sits next to the copy. `import_ses` restores §12 and clamps necks below 0.10 mm. `sanitize_dsn` drops `(clearance 25 (type smd_smd))`.

Locked stubs (7 tracks, Specctra `type fix`): SIG1/SIG2/REF along strip centres to s=15.50 / 37.95 (1.0 mm before L1/D2); VBUS/GND along the CHARGE tab to u=26.27. Island manhattan to R1–R3 was not locked (Q84, shorts, crossings). Foreign-net keep-outs on the strips (`allow_tracks` so the locked nets stay).

Freerouting 2.4.1 on OpenJDK 25, fanout 40 passes, 126/230 SMD pins escaped (**54.8 %**, above 49 %), 12 auto-route passes, 1 m 48 s, SES 33305 bytes, 60 unrouted / 25 router violations. Copy import with project file: 444 tracks, 37 vias, 12 DRC, 60 unconnected, 0 shorts, 0 foreign nets in the strips. Copy without `.kicad_pro`: 204 errors. SES **not** written to the owned PCB.

Owned PCB: 7 locked stubs, 5 `track_dangling` warnings, 0 DRC errors, 146 unconnected, 0 shorts. `routed: false`.

Last commit: `board(v2f): R24 off the hole, not routed`.

`scripts/board/release.py` was not edited. Firmware was not edited. `docs/fab/plan-v2.md` and `docs/fab/open-questions.md` were not edited.

Nothing ordered, quoted or uploaded. No vendor contact.

## Gates

### 1. Unittest (this package)

```text
.venv/bin/python -m unittest tests.test_board_release -v
```

Result: **OK** (15 tests). ERC 0. BOM rows = placed parts. `"routed": false` without `--routed`. `--routed` refused on `unconnected_items` 146. `pcb_tracks` > 0. R24 within 0.50 mm of the table (Q87). Other named SMT centres within 0.1 mm of `packing_v2_flat.md`. DSN class-check unit test green.

```text
.venv/bin/python -m unittest discover -s tests -v
```

CAD-related modules: **14 FAIL**, this package does not own:

- `test_cad.CadRegenTests.test_reference_regen_matches_committed_hashes` × 13 (`body_full_p15` 3mf/step/stl, `body_full_p25` 3mf/step/stl, `body_thin_p15` 3mf/step/stl, `lid` 3mf/step/stl, plus one more hash row)
- `test_cad.CadShellV2BuildTests.test_two_consecutive_shell_runs_are_identical`

Same 14 as WP12e. `[cad]` extras were not installed.

### 2. ERC

```text
kicad-cli sch erc --format json
```

**0 errors, 0 warnings** (from the release job in the board tests).

### 3. DRC

Zero-track (R24 moved, `--no-pre-route`):

```text
kicad-cli pcb drc --format json
Found 0 violations
Found 146 unconnected items
```

Owned PCB (locked stubs, SES discarded):

```text
kicad-cli pcb drc --format json
Found 5 violations
Found 146 unconnected items
types: track_dangling × 5 (severity warning)
shorts 0
```

Paste and first structural reason: `hardware/board/route.md` §10 and `docs/fab/board-v2.md` §15.

### 4. `release.py`

Without `--routed`: exit **0**. `routed: false`. Gerbers, BOM, CPL, STEP written.

With `--routed`: exit **1**. `routed release refused` on unconnected items (146). DRC errors 0 (dangling is a warning).

## What was not done

DRC 0 errors and 0 unconnected were not reached together. `--routed` with `routed: true` was not released. Island legs from the rings to R1–R3 were not locked (Q84). SES copper was not imported into the owned PCB.

## Needs a decision

Q84 1.0 mm on `tabs` versus L1 (0.70 mm from SIG1 attach), D2 (0.60 mm from SIG2 attach), and U1 pad 26 (0.90 mm from REF attach). Packing must keep those parts off the 1.0 mm tab creepage, or Q84 must stop at the ring copper only. R24 +0.47 mm u is a Q87 deviation for packing to fold back (WP11f).

## First structural reason

Q84 1.0 mm on the tab roots leaves no legal path from the locked ring stubs onto the island. Stop un-shorted. `routed: false`.
