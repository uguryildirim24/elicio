# t-0012 report: board v4 (handover)

**For Rolf.** The new board makes the body **18 mm wide and 8.1 mm thick**, down from 22 × 9.0. The length is the same, so your ear still needs M1 ≥ 50.9 (default 52). Electrically the earpiece loses nothing:

- The radio module is smaller, with about 13 mm of antenna clearance against the 18 mm its maker recommends. Range needs a test.
- The cell must come with a small Molex plug already fitted.
- The shell's closure screw moves.

It's **not ready to order.** Every wire except ground is routed with no rule errors. Ground is still in 37 separate pieces that need joining, and a fresh session is taking that over.

## Board order cost (board only, qty 5)

No quote was requested; nothing was uploaded; no account was used.

| Line | Qty / board | Price | Source, read date |
|---|---:|---|---|
| JLC 2-layer flex, island + strips + tab, qty 5 | — | UNVERIFIED | — |
| Assembly setup fee | — | UNVERIFIED | — |
| Stencil | — | UNVERIFIED | — |
| Flex assembly fixture | — | $24.63 per fixture; 1–29 pcs → 2 fixtures, $49.25. Whether both sides need their own fixtures: UNVERIFIED | https://jlcpcb.com/help/article/pcb-assembly-price, 2026-09-17 (board-v2 §18) |
| Extended part fee | per extended type | $3.00 each. The number of extended lines is UNVERIFIED (estimate 6–12, $18–36) | https://jlcpcb.com/help/article/358-PCBA-Capabilities-Instructions, 2026-09-18 (L8 §2.2) |
| Stiffener extra fee (6 pieces, ≥ 4 triggers it) | — | Amount UNVERIFIED | https://jlcpcb.com/help/article/fpc-extra-charges, 2026-09-18 |
| Consignment handling (ISP1807) | per shipment | "2% of declared value, minimum USD 10" is L7's quote; the live page is UNVERIFIED | L7 §3.3 |
| U1 ISP1807-LR-RS (consigned, not LCSC) | 1 | $13.65 (−RS) / $14.01 (−ST), qty 1 | https://www.mouser.com/ProductDetail/Insight-SiP/ISP1807-LR-ST, 2026-09-23 |
| U2 ADS1292IRSMT C89288 | 1 | $6.50 qty 1 was seen on LCSC 2026-09-17, but no URL was recorded, so UNVERIFIED | board-v2 G3 |
| U3 BQ25100YFPR C527572 | 1 | UNVERIFIED | — |
| U4 TLV71330PDQNT C3071062 (0 stock at JLC) | 1 | UNVERIFIED | — |
| U5 TPS7A0230PDQNR (no LCSC code) | 1 | UNVERIFIED | — |
| Q1 WPM3027-3 C240195 | 1 | UNVERIFIED | — |
| Q2–Q4 N-FET SOT-883 (not chosen) | 3 | UNVERIFIED | — |
| D1 PESD5V0L1UL C24109 | 1 | UNVERIFIED | — |
| D2 19-217/GHC C72043 | 1 | UNVERIFIED | — |
| J2 Molex 202656-0021 (not in JLC library) | 1 | UNVERIFIED | — |
| J3 3-pin RA header C49257 | 1 | UNVERIFIED | — |
| SW1 HRO 1TS015A C398746 | 1 | UNVERIFIED | — |
| R1–R3 220k 0402 C881401 | 3 | UNVERIFIED | — |
| 1M 0201 C473482 | 4 | UNVERIFIED | — |
| 10k 0201 C473048 | 8 | UNVERIFIED | — |
| 100k 0201 C270364 | 5 | UNVERIFIED | — |
| 6.8k 0201 C4104700 | 1 | UNVERIFIED | — |
| 6.04k 0201 C270341 | 1 | UNVERIFIED | — |
| 1k 0201 C270365 | 1 | UNVERIFIED | — |
| 47k 0201, 27k 0201 (no code) | 1 + 1 | UNVERIFIED | — |
| 1.5nF 0201 C285104 | 1 | UNVERIFIED | — |
| 10nF 0201 C43380 | 1 | UNVERIFIED | — |
| 1uF 0201 C5142566 | 6 | UNVERIFIED | — |
| 10uF 0402 C15525 | 3 | UNVERIFIED | — |
| 100nF 0201 C307380 | 4 | UNVERIFIED | — |
| 4.7uF 0402 (no code) | 1 | UNVERIFIED | — |
| **Board order total** | | **UNVERIFIED** | |

The prices come from the repo's research files only. I started no web lanes for this table.

## State at handover

- **Commits:** `815ca29` (board and note) on top of the WIP `9ddf1bd`. Both are pushed on `hp/elicio/t-0012-design-the-earpiece-board-from-scratch-f`. `uv.lock` is left untracked; it isn't mine.
- **Board:** `hardware/board/elicio-v4.kicad_pcb`.
  - Every net except GND is routed: 961 segments and 45 vias, locked pre-routes included.
  - Both GND pours are filled and saved.
- **DRC:**
  - 0 shorts, 0 clearance errors.
  - 13 `starved_thermal` errors, all GND pads.
  - 36 unconnected items, all GND.
  - Warnings: 21 lib mismatch, 1 dangling +VDD pre-route via, 2 J2-MP parity.
- **Tests:** full suite 279 run, OK, 61 skipped. `test_board_v4`: 7 OK, 1 skipped (no release summary).
- **Crash count:** `ls ~/Library/Logs/DiagnosticReports/ | grep -c Python-2026-09-23` = 5. It hasn't changed since the crash rule.
- **Design note:** `docs/fab/board-v4-design.md` §9 has:
  - what Freerouting and my router each achieved;
  - the four placement reliefs;
  - the 37 GND pieces, each with its pads;
  - all 36 KiCad joins with pads and mm;
  - the next steps and the exact rebuild and re-route commands (§9.5).
- **Not done:**
  - GND stitching;
  - the starved-thermal decision;
  - `release.py --board elicio-v4 --routed`, and so no Gerbers, BOM, CPL or STEP;
  - the §10.2 folded table with a cavity test per courtyard, hang and tab root. §10.1 flat table is in.

## Routing record

| Router | Result |
|---|---|
| Freerouting 2.4.1 (OpenJDK 25, `-Xmx4g`, Contact copper locked as fixed wires) on the 9fc962b W18 placement | 18 connections open; it never closed them |
| `hardware/board/v4_route_pf.py` negotiated congestion, reliefs 1–3 | Nets in conflict at the last round: 13 → 9 → 5 → 2 |
| Same, after C14 turned (relief 4) | 0 conflicts at round 30 (about 6 min) |
| `hardware/board/v4_route_fix.py` finisher | Nothing left to do on that output |

The last trap was topological. VBAT ran R14 → Q1 → C14 → R20 on B, which walled off AFE_VIN's path from U4 to C5 and Q1.3. Turning C14 so its VBAT pad faces east fixed it.

## Next session: do this

```bash
cd hardware/board
S=<scratch>; for s in d e; do cp elicio-v4.kicad_pro $S/$s.kicad_pro; cp elicio-v4.kicad_dru $S/$s.kicad_dru; done
../../.venv/bin/python -u v4_route_fix.py --pcb elicio-v4.kicad_pcb --nets GND --ripup 4 --out $S/d.kicad_pcb   # untried on GND; reads fills as copper
cp $S/d.kicad_pcb $S/e.kicad_pcb
kicad-cli pcb drc --refill-zones --save-board --format json --schematic-parity -o $S/drc_e.json $S/e.kicad_pcb
```

1. If the finisher can't join the islands, place vias by hand where F and B islands overlap. Vias stay out of LAND_P1/LAND_P2 (R 3.2) and the RF band.
2. For the starved thermals, I'd allow 1 spoke on GND pads (custom rule `min_resolved_spokes`), give U2's and U4's exposed pads a solid connection, and keep reliefs on the 0201s so they don't tombstone.
3. Then copy the board back, run `.venv/bin/python -m unittest tests.test_board_v4`, and run `scripts/board/release.py --board elicio-v4 --routed`.

The full rebuild from scratch is in §9.5:

```bash
$KP build_v4.py
v4_route_pf.py --fresh --skip GND --rounds 45
kicad-cli drc
v4_route_fix.py --drop-drc … --skip GND --ripup 4
kicad-cli drc --refill-zones --save-board
```

## Traps I hit

- **pcbnew crashes.**
  - `board.Add` every item you create, then `Flip`.
  - Never let Python free board-held items.
  - To revert, reload the board file instead of calling `Remove()`.
  - `build_v4.py` ends with `os._exit(0)` to skip SWIG teardown, which segfaults and pops a macOS dialog.
  - Run a script once cleanly before any loop, and never retry a crashing call in a loop.
- **Memory.** One router or KiCad batch at a time; Freerouting at `-Xmx4g`.
- **`build_v4.py` overwrites `hardware/board/elicio-v4.kicad_pcb`,** routing included. Route in a scratch copy and copy the result back.
- **A DRC on a copy needs `<stem>.kicad_pro` and `<stem>.kicad_dru` beside it.** Without them it silently runs default rules.
- **`release.py` runs DRC without a refill,** so the board must be saved with filled zones.
- **Numberless mask/paste aperture pads (U4/U5 X2SON) carry no net.** They gave `solder_mask_bridge` errors; the build now stamps their nets, and the finisher skips copper-less pads.
- **Finisher geometry.**
  - Model roundrect corners, or KiCad reads a track end on a corner as unconnected.
  - Route to a custom pad's primitives, not its anchor.
  - Skip GND until the pours exist, or it eats room.
- **Transplanting tracks onto a moved placement doesn't work.** It gave dozens of clearance errors and a new open net. Re-run `v4_route_pf.py` after any placement move.
- **Small tooling notes.**
  - `sed -i ''` fails in this shell (GNU sed comes first); edit with Python.
  - qlmanage thumbnails crop to a square.
  - `hp` isn't on PATH in this pane; `ha done` / `ha waiting` are the same commands.

## Open decisions for Rolf

1. **Which "too thick horizontally" he meant.** I designed the narrowest width first: W 18. T 8.1 is set by the cell stack, not the board.
2. **Cell.**
   - 501012: T 8.1, the pick.
   - 401012: T ≈ 7.6, needs a plate re-cut and a shell check.
   - 401010: T ≈ 7.6 and 1.5 shorter, 30 mAh; only if M1 < 50.9.
   - M1 (Q34) is still unmeasured.
3. **ISP1807 module.** About 13 mm of antenna clearance against 18 until a range test, and the module has to be consigned (it isn't in the JLC library).
4. **Cell plug.** The cell must arrive with a Molex Pico-EZmate Slim plug fitted (R2: no crimping). Supply is UNVERIFIED.
5. **Shell changes.** The closure screw moves off u 16.5, and the rib needs a slot for the P4/P5 flap (design note §7).
