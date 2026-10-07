# WP12h report

Lane `w2`. Branch `lane/w2`. Final commit `c9c750d0ea62c72c9dd89cdd7c8d7629f4c1c62c`.
Main was merged first (`795d154`). No rebase.

## What was built

- Script `hardware/board/hand_route.py` tries VBUS, J4, J3, U2, then A* stitches on the WP12g copper. It does not wipe tracks. New copper that raises DRC is not kept.
- `scripts/board/route_v2.py --via-extreme` injects JLC 2-layer extreme via 0.10/0.30 mm (um padstack `Via[0-1]_300:100_um`).
- `docs/fab/board-v2.md` §12 records the extreme via line from the JLC FPC page (read 2026-09-18). §15 records the WP12h stop.
- `hardware/board/route.md` §12 names each pad that cannot close, with the two coppers and the millimetre numbers.

Owned PCB is still the WP12g SES copper (`8348e62`): 421 tracks, 33 vias. No WP12g trace was moved.

## Plan §9 / package gates

| Item | Command | Result |
|---|---|---|
| Merge main, never rebase | `git merge origin/main` (already at `795d154`) | done |
| Keep WP12g copper | `cmp` start PCB vs owned | identical |
| DRC | `kicad-cli pcb drc --format json` | **0 errors**, 3 warnings (`via_dangling` ×2, `track_dangling` ×1), **63 unconnected**, 0 shorts |
| ERC | `kicad-cli sch erc --format json` | **0 errors, 0 warnings** |
| Board tests | `.venv/bin/python -m unittest tests.test_board_release -v` | 18 tests, OK, 14.002 s |
| `--routed` | `release.py --routed` via the unittest | refused; `routed: false`; unconnected > 0 |
| Non-`--routed` release | same module | exit 0, ERC 0 |
| DSN classes | `scripts/board/route_v2.py --dsn-check` | OK: Default 100/100, Contact 150/200, via 550:300 |
| Foreign nets in strips | import check / Q84 tests | 0 |

CAD regen (not this package): `test_cad.CadRegenTests.test_reference_regen_matches_committed_hashes` × 13 and `test_cad.CadShellV2BuildTests.test_two_consecutive_shell_runs_are_identical` (14 FAIL, same as WP12g).

## Freerouting (copy only, not imported)

`.venv/bin/python scripts/board/route_v2.py --work /tmp/wp12h-ext --route --via-extreme`

- OpenJDK 25, Freerouting 2.4.1, `-mp 20`, fanout 80, timeout 20 min.
- Fanout: 137/230 (59.6 %), 25.67 s.
- Auto-route: 20 passes, 59 unrouted, 29 violations, 100.66 s.
- Copy after SES: 504 tracks, 54 vias, DRC **63 errors** (21 annular + 21 drill + 21 via_diameter: 0.30/0.10 vs board min 0.55/0.30), **56 unconnected**, 0 shorts.
- Not imported.

## What was not done

- DRC 0 with 0 unconnected.
- `release.py --routed` exit 0.
- Gerbers/BOM/CPL as an order set (`routed: true`).
- Packing move of H1/H2, J4, or the east 0402 row.

## Named pads (geometry)

Need Default: 0.10 + 2 × 0.10 = 0.30 mm. Need Contact: 0.15 + 2 × 0.20 = 0.55 mm. Full table: `hardware/board/route.md` §12.

| Pad | Net | Why it cannot close |
|---|---|---|
| P4.1 | VBUS | Hole gap 1.20 mm: RLD_FB at x=15.263 and AFE_DRDY_AFE at x=15.742 leave 0.179 mm (need 0.30). East neck 19.60 keep to 19.75 edge is 0.15 mm (need 0.35 to edge). F.Cu hang GND at y=7.80 vs hang south 7.40 (track centre min 7.75). |
| R16.1 | VBUS | 0402 B.Cu (17.590, 23.570). AFE_DRDY_AFE at x=17.152 leaves 0.118 mm. GND at x=18.972 crosses the east approach. Q2_G at x=17.658 leaves 0.068 mm. J4-NPTH3 is south. |
| J4.2 / J4.4 | SWDIO / SWDCLK | SIG2 0.15 at x=13.500 y=19.50–28.20. AFE_IN1P at x=13.173. J4 keep vias=False to x=14.25. Via centre needs ≥14.050 and ≤13.975 (empty). |
| J3.1 | SIG1 | Contact 0.55 vs R4.1 (15.190, 19.970) and GND B.Cu at y=20.578 (0.228 mm window). |
| J3.2 | SIG2 | LED_EN at x=19.327 and GND at x=18.972 leave 0.355 mm (two Default tracks need 0.40). |
| U2.3 / U2.4 | AFE_IN1N / AFE_IN1P | QFN 0.40 mm pitch. Pad 0.20 mm leaves 0.20 mm between pads. Via 0.55 and extreme 0.30 do not fit. |
| U3.A2 | VBUS | DSBGA 0.25 mm pad, 0.40 mm pitch. Extreme via 0.30 vs pad + 2 × 0.10 = 0.45. |

Unused ADS1292R pads (named, not routed): U2.1 PGA1N, U2.2 PGA1P, U2.7 PGA2N, U2.8 PGA2P, U2.17 CLK, U2.25 GPIO2, U2.26 GPIO1.

Last copper commit message: `board(v2h): 63 rats remain, not routed` (`4f9f7f3`). Follow-up `c9c750d` only drops an unused helper.

## Needs a decision

Packing must move one of: H1/H2 (widen the 1.20 mm gap by at least 0.12 mm plus margin), J4 (open a via slot west of SIG2), or the east 0402 row (R16 vs AFE_DRDY and GND). This lane does not move packing (Q87 is already closed on R24). Extreme 0.10/0.30 vias need a board-min change before they can sit on this land; they still do not open the named channels.

## Final commit sha

`c9c750d0ea62c72c9dd89cdd7c8d7629f4c1c62c`
