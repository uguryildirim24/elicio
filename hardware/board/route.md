# How this board was routed (WP12c)

The copper on `elicio-v2.kicad_pcb` is still empty of tracks. DRC 0 was not
reached. This file is the redo recipe and the hang log.

## 1. Specctra DSN (KiCad 10.0.6)

`kicad-cli pcb export` has **no `specctra` subcommand** on this install
(subcommands are 3dpdf, gerbers, step, pos, …). DSN is written with pcbnew:

```text
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3
wx.App(False)
board = pcbnew.LoadBoard("hardware/board/elicio-v2.kicad_pcb")
pcbnew.ExportSpecctraDSN(board, "elicio-v2.dsn")
```

Export on 2026-09-17: 58492 bytes, 94 nets. Host CAD string in the file is
`KiCad's Pcbnew` / `10.0.6`.

## 2. Freerouting CLI

Jar: `/tmp/wp12b/freerouting.jar` — Freerouting v2.1.0, build-date 2025-04-12.
Java (Homebrew):

```text
openjdk version "21.0.12.1" 2026-08-18
OpenJDK Runtime Environment Homebrew (build 21.0.12.1)
OpenJDK 64-Bit Server VM Homebrew (build 21.0.12.1, mixed mode, sharing)
```

Binary: `/opt/homebrew/opt/openjdk@21/bin/java`.

Headless flags that actually parse (`--help` / `-h` open the GUI and hang):

```text
FREEROUTING__GUI__ENABLED=false
java -Djava.awt.headless=true -jar /tmp/wp12b/freerouting.jar \
  --user_data_path=/tmp/wp12c/fr-home \
  -de elicio-v2.dsn \
  -do elicio-v2.ses \
  -mp 10 \
  -dct 2
```

`freerouting.json` used: `gui.enabled=false`, `gui.exitWhenFinished=true`,
`router.max_passes=20`, `router.job_timeout=00:10:00`, `router.vias_allowed=true`.

## 3. Hang log (verbatim, every run)

```text
INFO   Freerouting v2.1.0 (build-date: 2025-04-12)
WARN   No default constructor found for field: currentLocale
INFO   Settings were loaded from freerouting.json
WARN   GUI is disabled and you don't have a console available, so the only feedback from Freerouting is in the log.
INFO   New version available: v2.4.1
INFO   [……] Job '……' started at 2026-09-18T……Z
```

No further line. No `.ses`. No `hs_err_pid` dump.

| Run | Wall clock | What happened |
|---|---|---|
| Diagnose | 180 s | CPU live; log frozen at 541 bytes; killed |
| `script` TTY | ~8 s | `script` sent EOF (`^D`); process died |
| nohup | ~2 min | Died; log still frozen; no SES |
| subprocess | 90 s | Still running; log frozen; killed for the maze trial |
| nohup 20 min slot | dead before 12 min | Same freeze; no SES |

The job never prints a pass. It never writes the output file. WP12b already
saw a 240 s hang on the same jar.

## 4. Maze fallback (copy only)

```text
KiCad python3 hardware/board/build_v2b.py --route-only /tmp/wp12c/maze-try.kicad_pcb
```

`maze_route.py` is now a real A* (0.20 mm grid, Default 0.10 mm clearance,
4-neighbour, ring 7×7 keep-outs, one net per tab, RF keep-out empty, no
shorting B.Cu bus). Contact 1.0 mm is **not** inflated on the grid: that
value cannot sit on a 2.5 mm tab next to the 0402 (pad gap 0.48 mm). Isolation
stays the ring keep-out, as WP12b.

Trial on a **copy**, 2026-09-18:

| Item | Result |
|---|---|
| Nets routed | 23 |
| Nets failed | 25 (USB_DP failed in 13 expansions — U5/J4 pads overlap) |
| Tracks written | 420 |
| DRC errors | 770 |
| Unconnected | 97 |

That is worse than the un-routed board (128 errors, 132 unconnected). The
copy was **not** written back. `build_v2b.py` without `--route-only` still
rebuilds the whole land; do not run it on this placement.

## 5. Why DRC 0 cannot land here

`kicad-cli pcb drc` on the committed un-routed file (0 tracks, 0 vias):

| Type | Errors (un-routed) |
|---|---|
| solder_mask_bridge | 38 |
| shorting_items | 32 (pad-to-pad: J2/J4, C15/C8, J3/SW1, leftover B.Cu) |
| clearance | 26, all netclass `Contact` 1.000 mm (R1/R2/R3 0402 gap 0.48 mm; J3 2.54 mm pitch) |
| copper_edge_clearance | 18 (U2 pads 0.275 mm vs 0.300 mm; J2 at the outline) |
| hole_clearance | 9 (J4 NPTH vs U5; J1 NPTH vs leftover B.Cu) |
| items_not_allowed | 5 (J2 and U5 in J4 keep-out; U3 in U1 keep-out; R25/C10 in RF_FEED_NOTCH) |

These are footprints and the Contact netclass in `elicio-v2.kicad_pro`.
WP12c must not move footprints and must not edit that project file. Hand
segments cannot separate overlapping pads. A router cannot either.

USB_DP / USB_DN were not routed. The rule that would apply on a clean land:
nRF52840 USB is Full Speed; keep the pair on the tongue, same layer, length
delta ≤ 1.0 mm (USB 2.0 FS intra-pair skew is tens of ns; 1 mm is the
layout budget this flex can hold).

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

1. Place from packing §5c no-receptacle table (`hardware/board/packing_5c_norec.md`).
2. R1, R2, R3 sit on the island at the tab roots (Q79 variant A).
3. Each 2.5 mm tab carries one Contact trace and nothing else.
4. Keep netclass Contact 1.0 mm; no DRC exception.
5. J1 and U5 are out (Q81). P4/P5 are RING_PAD charge pads. D1 stays on VBUS.
6. J4 TC2030 sits on the leftover; its keep-out is a board no-part zone (Q80).
7. J3 pads are Ø1.5 mm. Island holes at (13.45, 17.70) and (17.95, 17.70).
8. Export DSN with pcbnew (`kicad-cli` has no specctra).
9. Run Freerouting 2.4.1 on OpenJDK 25 with `--gui.enabled=false -de -do -mp -mt`.
10. Import the SES only after `§5c final <sha>`; then DRC and hand-fix residue.

## 8. WP12d place and route (`c6bd2fe`)

Pinned from `hardware/board/packing_5c_norec.md` (`c6bd2fe` on lane/w3, second §5c table: smallest all-64, no receptacle, width 22, chord 47.90, two sides, fold neck). Width 22 island u 2.25–19.75, s 16.00–37.60. 66 table parts plus H1/H2. 38 footprints flipped to B.Cu. R1–R3 on the island. P4/P5 RING_PAD at (0.75, 44.00) and (21.25, 44.00). J1/U5 absent. Holes (13.45, 17.70) and (17.95, 17.70). Neck-end strips SIG1 10.71 mm, SIG2 21.81 mm. Tracks 0.

Jar: `~/.local/opt/freerouting/freerouting-2.4.1.jar`. OpenJDK 25.0.4.1.

### Outline nudges (copper-to-edge)

Packing claims copper-to-edge ≥ 0.30 on courtyards. KiCad DRC uses pad copper. Two hang-outline steps, no part moved:

| Change | From | To | Why |
|---|---|---|---|
| `HANG_U1` | 32.50 | 33.20 | J3 hang length |
| Pocket SW1 u | 19.75 | 20.40 | SW1 courtyard at (16.25, 4.45) |
| `HANG_S1` | 24.80 | 26.70 | J3 pad 3 at (26.11, 25.39), Ø1.5, plus 0.30 |

After those, copper-edge errors are 0.

### Zero-track DRC (owned PCB)

```text
kicad-cli pcb drc --format json -o /tmp/wp12d/drc-pin3.json hardware/board/elicio-v2.kicad_pcb
Found 56 violations
Found 146 unconnected items
errors 56 warnings 0 unconnected 146
  23 clearance
  15 solder_mask_bridge
  11 shorting_items
   7 hole_clearance
```

Shorts (all pad-to-pad, unique pairs):

```text
PTH pad 1 [SIG2] of P2 | Pad 27 [unconnected-(U1-P0.11-Pad27)] of U1 on F.Cu
PTH pad 1 [SIG2] of P2 | Pad 29 [unconnected-(U1-P0.12-Pad29)] of U1 on F.Cu
PTH pad 1 [SIG2] of P2 | Pad 35 [unconnected-(U1-D+-Pad35)] of U1 on F.Cu
PTH pad 1 [SIG2] of P2 | Pad 36 [unconnected-(U1-P0.14-Pad36)] of U1 on F.Cu
PTH pad 1 [SIG2] of P2 | Pad 37 [AFE_CS] of U1 on F.Cu
PTH pad 1 [SIG2] of P2 | Pad 38 [unconnected-(U1-P0.16-Pad38)] of U1 on F.Cu
PTH pad 1 [SIG2] of P2 | Pad 39 [AFE_MISO] of U1 on F.Cu
PTH pad 1 [SIG2] of P2 | Pad 40 [nRESET] of U1 on F.Cu
PTH pad 1 [SIG2] of P2 | Pad 41 [AFE_DRDY] of U1 on F.Cu
PTH pad 1 [SIG2] of P2 | Pad 42 [unconnected-(U1-P0.19-Pad42)] of U1 on F.Cu
PTH pad 1 [SIG2] of P2 | Pad 43 [unconnected-(U1-P0.21-Pad43)] of U1 on F.Cu
```

Hole clearance: J4 NPTH vs R5, R6, R18, R19, R21, R22 on B.Cu.

Contact 1.0 mm vs R1/R2/R3 0402 pad gap 0.48 mm (kept; no DRC exception).

### Freerouting 2.4.1 run (OpenJDK 25)

DSN: pcbnew `ExportSpecctraDSN` → `/tmp/wp12d/elicio-v2.dsn` (56640 bytes).

```text
/opt/homebrew/opt/openjdk@25/bin/java -Djava.awt.headless=true \
  -jar ~/.local/opt/freerouting/freerouting-2.4.1.jar \
  --gui.enabled=false \
  --user_data_path=/tmp/wp12d/fr-home \
  -de /tmp/wp12d/elicio-v2.dsn \
  -do /tmp/wp12d/elicio-v2.ses \
  -mp 8 \
  -mt 4 \
  --router.job_timeout=00:08:00
```

| Item | Result |
|---|---|
| Version | Freerouting v2.4.1 (build-date: 2026-09-03) |
| Wall time | 75.86 s (`time` real; job elapsed 1 m 13.58 s) |
| Fanout | 95/230 SMD pins escaped (41.3%) |
| Auto-route | 8 passes; final 79 unrouted, 50 violations (optimizer: 81 unrouted, 50 violations) |
| SES | **yes** `/tmp/wp12d/elicio-v2.ses` 22813 bytes |
| Copy import | 275 tracks, 17 vias |
| Copy DRC | **374** errors, 79 unconnected (was 56 / 146 un-routed) |
| Owned PCB | SES **not** written back |

Copy DRC types: 199 track_width, 122 clearance, 15 solder_mask_bridge, 11 shorting_items (same P2 vs U1 pairs), 9 copper_edge, 8 hole_clearance.

### First structural reason

P2 RING_PAD at (10.40, 33.10) is inside U1's courtyard (U1 at (8.00, 29.35), 11.50 × 16.50). The PTH copper shorts U1 F.Cu pads. Routing cannot clear pad-to-pad shorts. Step 5: stop **un-shorted**, `routed: false`.

Contact class 1.0 mm and J4 NPTH vs B.Cu remain after any route of this land.

## 9. WP12e place and route (`408a476`)

Pinned from `hardware/board/packing_v2_flat.md` (`408a476` packing-v2.md §5d). Folded-site table ignored. Width 22 island u 2.25–19.75, s 16.00–37.60. 66 table parts plus H1/H2. 38 footprints flipped to B.Cu. R1–R3 on the island. Flat rings: P1 (5.90, 5.29), P2 (10.40, −5.81), P3 (8.50, 43.00), P4 (37.47, 2.80), P5 (30.05, 5.80). CHARGE rectangle centre (33.02, 4.30) 14.50 × 8.60 is in Edge.Cuts. J1/U5 absent. Holes (13.45, 17.70) and (17.95, 17.70). Tracks 0.

Jar: `~/.local/opt/freerouting/freerouting-2.4.1.jar`. OpenJDK 25.0.4.1.

### Outline

SIG1/SIG2 `tab_detour` from attach (5.90, 16.00) and (10.40, 16.00) to the flat rings. REF tab from (8.50, 37.60) to (8.50, 43.00). CHARGE tab: after pocket (20.40, 7.40) enter u=25.77, then the 14.50 × 8.60 rectangle, then J2 hang to s=14.40. No copper-to-edge nudge.

### Hole nudges (inside 0.1 mm pin)

| Ref | From table (u, s) | To (u, s) | Why |
|---|---|---|---|
| R23 | (18.28, 21.17) | (18.37, 21.17) | J4 NPTH hole clearance 0.20 |
| R26 | (14.22, 21.63) | (14.17, 21.63) | J4 NPTH hole clearance 0.20 |
| R24 | (18.28, 22.37) | unchanged | needs +0.46 mm u; past the pin |

### Zero-track DRC (owned PCB)

```text
kicad-cli pcb drc --format json -o /tmp/wp12e/drc-zero5.json hardware/board/elicio-v2.kicad_pcb
Found 2 violations
Found 146 unconnected items
errors 2 warnings 0 unconnected 146
   1 hole_clearance
   1 solder_mask_bridge
```

Both hits: Pad 2 [GND] of R24 on B.Cu | NPTH pad of J4. Copper-edge 0. Shorts 0. Q84 island Contact-clearance 0.

KiCad J4 NPTH centres at rot 90: (16.25, 27.14), (15.234, 22.06), (17.266, 22.06). Keep-out Ø1.39 on B.Cu at those centres. Pin table v2 listed (16.25, 22.06), (17.27, 27.14), (15.23, 27.14).

### Freerouting 2.4.1 run (OpenJDK 25)

DSN: pcbnew `ExportSpecctraDSN` → `/tmp/wp12e/elicio-v2.dsn` (59013 bytes).

```text
/opt/homebrew/opt/openjdk@25/bin/java -Djava.awt.headless=true \
  -jar ~/.local/opt/freerouting/freerouting-2.4.1.jar \
  --gui.enabled=false \
  --user_data_path=/tmp/wp12e/fr-home \
  -de /tmp/wp12e/elicio-v2.dsn \
  -do /tmp/wp12e/elicio-v2.ses \
  -mp 8 \
  -mt 4 \
  --router.job_timeout=00:08:00
```

| Item | Result |
|---|---|
| Version | Freerouting v2.4.1 (build-date: 2026-09-03) |
| Wall time | 75.47 s (`time` real; job elapsed 1 m 12.94 s) |
| Fanout | 113/230 SMD pins escaped (49.1%) |
| Auto-route | 8 passes; final 75 unrouted, 17 violations |
| SES | **yes** `/tmp/wp12e/elicio-v2.ses` 22585 bytes |
| Copy import | 268 tracks, 12 vias |
| Copy DRC | **317** errors, 75 unconnected (was 2 / 146 un-routed) |
| Owned PCB | SES **not** written back |

Copy DRC types: 199 track_width, 103 clearance, 9 copper_edge_clearance, 3 hole_clearance, 2 npth_inside_courtyard, 1 solder_mask_bridge. Shorts 0.

### First structural reason

R24 pad 2 [GND] on B.Cu occupies J4 NPTH at (17.266, 22.06). The 0.1 mm pin cannot separate them (0.46 mm required). Step 5: stop **un-shorted**, `routed: false`.


