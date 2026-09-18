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
