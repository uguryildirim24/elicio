# WP12d-prep report — router proof and side column (lane w2)

Worktree: `/home/user/projects/elicio/.worktrees/w2`
Branch: `lane/w2`
Package: WP12d-prep
Date: 2026-09-18
KiCad: 10.0.6 (`kicad-cli`)
Java 21: Homebrew OpenJDK 21.0.12.1 (cannot load the 2.4.1 jar)
Java 25: Homebrew OpenJDK 25.0.4.1 `/opt/homebrew/opt/openjdk@25/bin/java`
Final commit: `edf612faa1019002471188a6b01b6598676d72a9`

## What was built

`git merge main` first (`68f38ba`). Conflict in `tests/test_board_release.py` kept both sides: review r6 `routed: false` / `refused` and WP12c `pcb_tracks == 0`.

Freerouting 2.4.1 jar at `/tmp/wp12d/freerouting-2.4.1.jar` (GitHub release v2.4.1, Q46 free). Class file version 69. Java 21 fails to load it. Java 25 runs L8 §3 flags (`--gui.enabled=false -de -do -mp 5 -mt 4`). SES written. Not imported. Board file byte-for-byte unchanged (`494283e3…`).

`hardware/board/placement_table.py` parses a packing markdown table with `side` `top`/`bottom`. `build_v2b.py` `apply_placement_row` Flips bottom rows with KiCad `Flip(pos, False)`. Synthetic two-row test does not load the PCB.

`route.md` §6–§7: proof table and the ten-line WP12d plan (Q79, Q80). `board-v2.md` §15 only.

Nothing ordered, quoted or uploaded. No vendor contact. SES stays under `/tmp/wp12d/`.

## Gates

### 1. Unittest (this package)

```text
.venv/bin/python -m unittest tests.test_board_release -v
```

Result: **OK** (7 tests), including the two-row side-column test.

```text
.venv/bin/python -m unittest discover -s tests -v
```

Result: 209 tests, **14 FAIL**, all `test_cad` (v1 regen hashes and `test_two_consecutive_shell_runs_are_identical`). This package does not own CAD.

### 2. Board file unchanged

```text
git diff --stat -- hardware/board/*.kicad_pcb
```

Empty. SHA-256 `494283e31725e58eea29325d8fb9fd20cb98c3f58973b27d46b904fbd69e2f34`.

### 3. `release.py` without `--routed`

```text
.venv/bin/python scripts/board/release.py --board-dir hardware/board --out /tmp/wp12d-release
```

Exit **0**. `routed: false`. `pcb_tracks: 0`. ERC 0. BOM 59 = placed 59. CPL 59.

### 4. `git status --short`

Empty after the commit.

## Plan §9 / brief deliverables

| Item | Result |
|---|---|
| Merge main, keep both sides | `68f38ba` |
| Freerouting 2.4.1 writes SES | Yes, on OpenJDK 25. Java 21 cannot load the jar. |
| SES imported | **No** (evidence only) |
| Two-sided `side` column | Parser + `apply_placement_row`; synthetic test green |
| §5b column match | `face` `top`/`bottom` aliases `side`; `pocket`/`floor` stay top |
| Q79 / Q80 ten-line plan | `route.md` §7 |
| Copper committed | None |

## What was not done

- Place or route on packing §5c (WP11d has not published it).
- Import the SES.
- DRC 0.

## Needs a decision

1. L8 §3 says 2.4.1 runs on Java 21. The GitHub `freerouting-2.4.1.jar` is class 69 and needs OpenJDK 25. WP12d should use `/opt/homebrew/opt/openjdk@25/bin/java`.
2. `kicad-cli pcb export` still has no `specctra`; DSN stays pcbnew.

## route.md §6–§7 (paste)

## 6. Freerouting 2.4.1 headless proof (WP12d-prep)

Jar: `/tmp/wp12d/freerouting-2.4.1.jar` from
https://github.com/freerouting/freerouting/releases/tag/v2.4.1 (Q46: free;
Rolf may veto). Manifest Build-Date 2026-09-03, Main-Class
`app.freerouting.Freerouting`, class file version 69 (Java 25).

`kicad-cli pcb export` still has no `specctra` subcommand. DSN for this run
is pcbnew `ExportSpecctraDSN` → `/tmp/wp12d/elicio-v2.dsn` (58492 bytes).

Java 21.0.12.1 (`/opt/homebrew/opt/openjdk@21/bin/java`) **does not load**
the 2.4.1 jar:

```text
Error: LinkageError occurred while loading main class app.freerouting.Freerouting
	java.lang.UnsupportedClassVersionError: app/freerouting/Freerouting has been compiled by a more recent version of the Java Runtime (class file version 69.0), this version of the Java Runtime only recognizes class file versions up to 65.0
```

Java 25.0.4.1 (Homebrew `openjdk@25`, keg-only,
`/opt/homebrew/opt/openjdk@25/bin/java`) does. L8 §3 flags, pass count
bounded to 5:

```text
/opt/homebrew/opt/openjdk@25/bin/java -jar /tmp/wp12d/freerouting-2.4.1.jar \
  --gui.enabled=false \
  -de /tmp/wp12d/elicio-v2.dsn \
  -do /tmp/wp12d/elicio-v2.ses \
  -mp 5 \
  -mt 4 \
  --router.job_timeout=00:08:00
```

| Item | Result |
|---|---|
| Version | Freerouting v2.4.1 (build-date: 2026-09-03) |
| Wall time | 39.52 s (`time` real; job elapsed 37.21 s) |
| SES | **yes** `/tmp/wp12d/elicio-v2.ses` |
| SES size | 14531 bytes |
| Track count | 60 `(wire` / 60 `(path`; 19 `(via` |
| Unrouted after 5 passes | 80 nets, 148 violations (placement still collides) |
| stderr / log | Polyline warnings; then `Successfully saved output file` |
| Import | **not done** (evidence only) |

The committed `elicio-v2.kicad_pcb` is unchanged.

## 7. WP12d plan (Q79, Q80)

1. Place from packing §5c; parser already reads `ref u s rot side` (`top`/`bottom`).
2. R1, R2, R3 sit on the island at the tab roots (Q79 variant A).
3. Each 2.5 mm tab carries one Contact trace and nothing else.
4. Keep netclass Contact 1.0 mm; no DRC exception.
5. J1 USB-C stays on the hook-end face (Q80, plan v2 §5.4).
6. J4 TC2030 sits on the leftover; its keep-out is a board no-part zone.
7. J3 pads are Ø1.5 mm.
8. Export DSN with pcbnew (`kicad-cli` has no specctra).
9. Run Freerouting 2.4.1 on OpenJDK 25 with `--gui.enabled=false -de -do -mp -mt`.
10. Import the SES only after §5c is pinned; then DRC and hand-fix residue.
