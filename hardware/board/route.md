# How this board was routed (WP12c)

The copper on `elicio-v2.kicad_pcb` has seven locked tab stubs and no SES import. DRC 0 with 0 unconnected was not reached. This file is the redo recipe and the hang log.

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

## 10. WP12f route (Q87, DSN classes, locked stubs)

Repeat: `.venv/bin/python scripts/board/route_v2.py --dsn-check` then `--route`.
Jar: `~/.local/opt/freerouting/freerouting-2.4.1.jar`. OpenJDK 25.0.4.1.
KiCad python for DSN/SES. Copy import copies `elicio-v2.kicad_pro` and `.kicad_dru` beside the copy PCB so Default stays 0.10/0.10.

### Q87 deviations from pin table v2 (packing folds these back)

| Ref | From table (u, s) | To (u, s) | Why |
|---|---|---|---|
| R23 | (18.28, 21.17) | (18.37, 21.17) | J4 NPTH hole clearance 0.20 |
| R26 | (14.22, 21.63) | (14.17, 21.63) | J4 NPTH hole clearance 0.20 |
| R24 | (18.28, 22.37) | (18.75, 22.37) | J4 NPTH (17.266, 22.06); +0.47 mm u, past the 0.1 mm pin |

Zero-track DRC after R24: **0 errors**, 146 unconnected, 0 shorts.

### DSN class blocks (unit um)

```text
(via "Via[0-1]_700:300_um")
(rule (width 100) (clearance 100))
(class kicad_default … (width 100) (clearance 100))
(class Contact REF SIG1 SIG2 (width 150) (clearance 200))
```

WP12e 199 `track_width` (min 0.2000, actual 0.1000): SES import leaked Contact onto Default / board min width. The DSN already had 100 um. `sanitize_dsn` drops `(clearance 25 (type smd_smd))`. `import_ses` restores §12 and floors track width at 0.10 mm. `--router.automatic_neckdown=false --router.neck_width_um=100 --router.strict_drc=true`.

Locked wires in the DSN (`type fix`): SIG1/SIG2/REF 150 um along strip centres to s=15.50 / 37.95; VBUS/GND 100 um along the CHARGE tab to u=26.27. Island manhattan to R1–R3 was not locked: it shorts J2, crosses SIG2/REF, and still intersects `tabs`.

### Freerouting 2.4.1 run (OpenJDK 25)

```text
/opt/homebrew/opt/openjdk@25/bin/java -Djava.awt.headless=true \
  -jar ~/.local/opt/freerouting/freerouting-2.4.1.jar \
  --gui.enabled=false \
  --user_data_path=/tmp/wp12f/fr-home \
  -de /tmp/wp12f/elicio-v2.dsn \
  -do /tmp/wp12f/elicio-v2.ses \
  -mp 12 -mt 4 \
  --router.job_timeout=00:10:00 \
  --router.automatic_neckdown=false \
  --router.strict_drc=true \
  --router.neck_width_um=100 \
  --router.copper_to_edge_clearance_um=300 \
  --router.hole_clearance_um=200 \
  --router.fanout.enabled=true \
  --router.fanout.max_passes=40 \
  --router.fanout.ripup_allowed=true
```

| Item | Result |
|---|---|
| Version | Freerouting v2.4.1 (build-date: 2026-09-03) |
| Wall time | 1 m 48.19 s |
| Fanout | 126/230 SMD pins escaped (**54.8 %**), 40 passes |
| Auto-route | 12 passes; final 60 unrouted, 25 violations |
| SES | **yes** `/tmp/wp12f/elicio-v2.ses` 33305 bytes |
| Copy import (with `.kicad_pro`) | 444 tracks, 37 vias, clamped 17 necks to 0.10 mm |
| Copy DRC | **12** errors, 60 unconnected (was 0 / 146 zero-track) |
| Copy DRC without `.kicad_pro` | 204 errors (192 clearance at 0.20) |
| Foreign nets in strips | 0 |
| Owned PCB | SES **not** written back |

Copy DRC types (with project file): 6 via_dangling, 5 track_dangling (the locked stubs), 1 clearance (GND vs U1 pad 12, 0.0916 mm). Shorts 0.

### First structural reason

Q84 1.0 mm on `tabs` versus parts at the attach line: L1 pad 1 is 0.70 mm from SIG1 attach, D2 pad 2 is 0.60 mm from SIG2 attach, U1 pad 26 is 0.90 mm from REF attach. No copper can leave a strip onto the island without Contact-to-part clearance under 1.0 mm. Freerouting joined R1–R3 to J3 on the island and left the ring stubs dangling. Step 5: stop **un-shorted**, `routed: false`.

## 11. WP12g route (Q88, pin table v2.1, locked Contact)

Repeat: `.venv/bin/python scripts/board/route_v2.py --dsn-check` then `--route`.
Jar: `~/.local/opt/freerouting/freerouting-2.4.1.jar`. OpenJDK 25.0.4.1.
KiCad python for DSN/SES. Copy import copies `elicio-v2.kicad_pro` and `.kicad_dru` beside the copy PCB.

### Q88 rule areas

`tabs` is three 7 × 7 boxes around P1–P3. `tail_pads` is two 7 × 7 boxes around P4–P5. Strips carry one Contact 0.15/0.20 trace and a foreign-net keep-out. Island Contact stays 0.20.

### Q87 / pin table v2.1 (`e4b857c`)

| Ref | Table v2 (u, s, rot) | v2.1 (u, s, rot) | On copper |
|---|---|---|---|
| R23 | (18.28, 21.17, 0) | (18.32, 21.10, 0) | yes, DRC 0 |
| R24 | (18.28, 22.37, 0) | (18.49, 22.57, 90) | yes; 0.29 mm from v2; Q87 deviation closes |
| R26 | (14.22, 21.63, 90) | (14.21, 21.63, 90) | yes, DRC 0 |

Zero-track DRC with v2.1 poses: **0 errors**. R24 rot 90 clears J4 NPTH.

### Locked Contact (before router)

Ring → strip centre → island → R1–R3. VBUS stub on the CHARGE south edge to (26.27, 1.20). GND to J2 pad 2, split at the P5 7 × 7. Locked-only DRC: **0 errors**, 1 VBUS `track_dangling` warning, 142 unconnected, 30 tracks. Paste:

```text
Found 1 violations
Found 142 unconnected items
locked DRC errors 0 warnings 1 unconnected 142
types Counter({('track_dangling', 'warning'): 1})
```

### Freerouting 2.4.1 runs (OpenJDK 25)

Via first 0.70/0.30, then §12 JLC 0.55/0.30 because 0.70 blocked F.Cu↔B.Cu. Flags: `-mp 20 -mt 4 --router.job_timeout=00:20:00 --router.fanout.max_passes=80 --router.fanout.ripup_allowed=true --router.automatic_neckdown=false --router.strict_drc=true --router.neck_width_um=100 --router.copper_to_edge_clearance_um=300 --router.hole_clearance_um=200`.

| Item | 0.70 via (first SES) | 0.55 via (imported) |
|---|---|---|
| Wall time | 2 m 40.80 s | 1 m 37.38 s |
| Fanout | 47 already connected from locks; 80 passes | 123/230 (53.5 %), 9 passes |
| Auto-route | 20 passes; 70 unrouted, 28 violations | 20 passes; 67 unrouted, 30 violations |
| SES | `/tmp/wp12g/elicio-v2.ses` 25768 bytes | `/tmp/wp12g-via55/elicio-v2.ses` 53381 bytes |
| Copy DRC | 0 errors, 70 unconnected | 0 errors, 63 unconnected |
| Copy tracks / vias | 353 / 23 | 421 / 33 |
| Foreign nets in strips | 0 | 0 |
| Owned PCB | first SES imported, then replaced by 0.55 SES | **yes** 0.55 SES |

DSN class check OK: Default 100/100 um, Contact 150/200 um, via 550:300 um (700:300 vias from the first pass remain).

A later GND pour plus J3 Contact manhattan produced 15 DRC errors including SIG1/SIG2 shorts. That copper was discarded.

### First structural reason

63 unconnected after Q88, locked R1–R3 Contact, and Freerouting with via 0.55/0.30. Remaining rats are U2 QFN escapes, J4 SWD, VBUS P4→island, J3 Contact, and layer stitches. Step 5: stop **un-shorted**, `routed: false`.

## 12. WP12h hand-route (63 rats on the WP12g copper)

Script: `hardware/board/hand_route.py` (KiCad python). Does not wipe tracks. Groups: `vbus`, `j4`, `j3`, `u2`, `stitch`. Default via 0.55/0.30. `--via-extreme` is 0.30/0.10 (JLC 2-layer extreme, extra cost; page line “②Extreme for 2-layer: 0.10mm/0.3mm (extra cost required)”, read 2026-09-18 https://jlcpcb.com/capabilities/flex-pcb-capabilities).

WP12g copper stayed: 421 tracks, 33 vias, DRC 0 errors, 0 shorts, 63 unconnected. Every explicit channel that joined a named pad produced DRC errors. Those traces were not kept. A* on the remaining rats did not close a pair without a DRC rise.

Freerouting 2.4.1 OpenJDK 25, `scripts/board/route_v2.py --work /tmp/wp12h-ext --route --via-extreme`. Fanout 137/230 (59.6 %) in 25.67 s. Auto-route 20 passes, 59 unrouted, 29 violations, 100.66 s. Copy after SES: 504 tracks, 54 vias, DRC **63 errors** (21 `annular_width` + 21 `drill_out_of_range` + 21 `via_diameter`: 0.30/0.10 vias vs board min 0.55/0.30), 56 unconnected, 0 shorts, 0 foreign nets in strips. **Not imported.** Extreme vias need a board-min change; they do not close the named pads.

Default need: track 0.10 + 2 × 0.10 clearance = **0.30 mm**. Contact need: 0.15 + 2 × 0.20 = **0.55 mm**.

### Named pads that cannot close (geometry)

| Pad | Net | Size / layer | Other copper | Remaining gap | Need |
|---|---|---|---|---|---|
| P4.1 | VBUS | Ø5.0 RING, F.Cu+B.Cu (37.470, 2.800). Stub ends (26.270, 1.200) | H1 keep east 15.10 and H2 keep west 16.30 (gap 1.20). RLD_FB B.Cu 0.10 at x=15.263. AFE_DRDY_AFE B.Cu 0.10 at x=15.742 | 0.179 mm in the hole gap | 0.30 |
| P4.1 (east neck) | VBUS | same | H2 keep east 19.60. Edge.Cuts 19.75. Copper-edge 0.30 → track centre ≤ 19.40 | 19.40 is 0.20 mm inside H2 keep | 0.35 to edge |
| P4.1 (F.Cu hang) | VBUS | same | GND F.Cu 0.10 at y=7.80 (J2). Hang south Edge.Cuts y=7.40. Track centre min 7.75 | 0.05 mm to GND | 0.20 |
| R16.1 | VBUS | 0402 0.54×0.64 B.Cu (17.590, 23.570) | AFE_DRDY_AFE B.Cu 0.10 at x=17.152 y=23.426–23.863 | 0.118 mm (pad half 0.27 + track half 0.05) | 0.30 |
| R16.1 | VBUS | same | GND B.Cu 0.10 at x=18.972 y=22.542–26.368 | east approach at y=23.57 crosses that vertical | 0.30 |
| R16.1 | VBUS | same | Q2_G B.Cu 0.10 at x=17.658 y=24.658–29.902. J4-NPTH3 (16.57–17.96, 21.36–22.75) | 0.068 mm to Q2_G | 0.30 |
| J4.2 | SWDIO | 0.787×0.787 F.Cu (15.615, 25.870) → U1.51 0.60×0.40 (12.650, 27.500) | SIG2 Contact 0.15 at x=13.500 y=19.50–28.20. AFE_IN1P 0.10 at x=13.173 y=22.08–29.01. J4 keep vias=False x=14.25–18.25 y=21.10–28.10 | via centre needs ≥14.050 and ≤13.975 | empty |
| J4.4 | SWDCLK | 0.787×0.787 F.Cu (15.615, 24.600) → U1.53 (12.650, 26.700) | same SIG2 / AFE_IN1P / J4 keep | same empty via slot | empty |
| J3.1 | SIG1 | PTH Ø1.5 (26.110, 20.310) from locked SIG1 (10.190, 19.500) | R4.1 RLD_FB 0.54×0.64 B.Cu (15.190, 19.970). GND B.Cu y=20.578 x=16.78–18.31 | 0.228 mm window | 0.55 Contact |
| J3.2 | SIG2 | PTH Ø1.5 (26.110, 22.850) from locked SIG2 (16.400, 28.200) | LED_EN B.Cu 0.10 at x=19.327 y=28.447–35.002. GND B.Cu 0.10 at x=18.972 y=22.542–26.368 | 0.355 mm | 0.40 (two Default tracks) |
| U2.3 | AFE_IN1N | QFN 0.775×0.200 F.Cu (13.143, 9.680), 0.40 mm pitch | neighbour pads 0.20 mm wide leave 0.20 mm between pads | 0.20 mm | via 0.55 or 0.30 does not fit between pads |
| U2.4 | AFE_IN1P | (13.143, 10.080) | same QFN pitch | 0.20 mm | same |
| U3.A2 | VBUS | DSBGA 0.25×0.25 F.Cu (15.880, 30.450), 0.40 mm pitch | 0.55 via; extreme 0.30 vs pad 0.25 + 2×0.10 | 0.40 mm pitch | 0.45 |

Unused ADS1292R pads (no net to route; named, left open): U2.1 PGA1N, U2.2 PGA1P, U2.7 PGA2N, U2.8 PGA2P, U2.17 CLK, U2.25 GPIO2, U2.26 GPIO1.

The other rats in the 63 are F.Cu↔B.Cu stitches of the same nets (GND, +3V0, +VDD, VBAT, nRESET, SPI, U3 TS/ISET/PRETERM). They need a via slot that the named geometry above already fills.

### First structural reason

63 unconnected after scripted hand-route attempts on the WP12g copper. Packing must move H1/H2 (hole gap), J4 (via slot vs SIG2), or the east 0402 row (R16 vs AFE_DRDY and GND). This lane does not move packing. Step 5: stop **un-shorted**, `routed: false`.

## 13. WP12i v3 routing attempt (2026-09-23)

Merged `origin/lane/w2` 3a27ffd then `origin/lane/w3` ab9ce95; no conflicts. Initial committed board DRC 0 errors, 140 unconnected, 2 Contact dangling ends and 1 U2 library mismatch warning. Interrupted VBUS/nRESET tracks passed the DRC, so they stayed. No WP12g copper was transplanted from the old v2 pin positions. Pin table v3's Q98 channels and locked Contact paths stayed at their flat sites.

`uv venv --python 3.13 .venv && uv pip install --python .venv/bin/python -e .`. `scripts/board/route_v2.py --work /tmp/t0002-route1 --route` exported a checked DSN (Default 100/100 µm, Contact 150/200 µm, via 550:300 µm). Freerouting 2.4.1 with OpenJDK 25, `-Xmx4g`, `-mp 20`, `-mt 4`: 3m33s, 715.5 MB peak heap, 96 unrouted / 32 router violations. The router's '2223 GB allocated' counter is cumulative allocation, **not** peak RAM. KiCad import on the copy: 0 DRC errors, 96 airwires, 0 foreign-net tracks in strips (223 tracks / 25 vias). No router violations were accepted into the PCB; KiCad DRC is the gate.

Then KiCad-Python `hand_route.py --pcb /tmp/t0002-route1/elicio-v2-copy.kicad_pcb --group GROUP` (0.55/0.30 vias) tried in order; each candidate was rolled back if the DRC error count rose:

| Group | Clean new links | Rejected attempts | Airwires after |
|---|---:|---:|---:|
| j3 | 0 | 5 | 96 |
| vbus | 1 | 5 | 95 |
| j4 | 1 | 9 | 94 |
| u2 | 3 | 23 | 91 |
| stitch | 7 | 73 | 84 |

The named Contact failures remain: the SIG2 strip copper end (11.270, 16.500) → R2.1 (19.070, 33.340), 18.559 mm straight; R2.1 → J3.2 (28.410, 29.340), 10.160 mm. REF R3.1 (19.070, 31.340) → strip end (8.500, 39.350), 13.262 mm; R3.1 → J3.3 (28.410, 31.880), 9.356 mm. SIG1 R1.1 island anchor (10.190, 20.120) → J3.1 (28.410, 26.800), DRC endpoint gap 19.628 mm. A* tried each and added 2–29 DRC errors, then reverted the copper; the J3 PTH pad layout and narrow cut-neck still constrain Contact. Q98's slot is insufficient on this copper: U1.51 → J4.2 SWDIO 3.622 mm and U1.53 → J4.4 SWDCLK 3.857 mm both failed A* DRC. U2.21 → R8.1 AFE_MISO_AFE 19.397 mm failed A* search (no path at 0.10 track/0.10 clearance). Relocating packing sites is a decision for packing, not a board-side silent fix. These are not assertions that no alternative route can ever exist.

Owned board DRC paste:

```text
Found 11 violations
Found 84 unconnected items
0 errors, 0 shorts; 8 via_dangling + 2 track_dangling + 1 lib_footprint_mismatch warnings
```

`hardware/board/unrouted-v3.md` is the **complete** 84-airwire list from that exact board and DRC, with both endpoints, pad anchors when connected, and straight-line millimetre gaps. Generate it with KiCad Python `scripts/board/unrouted.py PCB DRC.json OUT.md`; do not mistake the endpoint gap for channel width. `release.py --routed` exited 1, `routed: false`, refused only on 84 unconnected. ERC 0, BOM/CPL 55 each, Gerber/drill and STEP generated but **not orderable**. STEP misses the SW1, U2 and U3 models listed in board-v2 §15. No purchases or uploads.
