# Code review r5: WP10, WP11, WP12, WP13, WP16, WP17

**Verdict: MERGE-AFTER-DECISION.**
Every gate passes on `review/r5` after the fixes. Order 1 solids, renders and the v1 manifest are unchanged, Stage B v2 is byte-identical twice, ERC is 0/0 and the sketch compiles.
The merge itself is safe. Decisions 57 to 68 come before order 2 and the board order: Stage B v2 still fails the REF tab (59), the PCB is not a valid placement (62), and two plan numbers are wrong (57, 58). Nothing was ordered, uploaded or requested.

Branch `review/r5` from `main` 5d23c54. `main` has since moved to 83e8def, a HANDOFF-only commit. Merges, in this order:

| Lane | Tip | Into review/r5 | How |
|---|---|---|---|
| `lane/w1` (WP11) | 7df78b5 | 46bf7bf | squash, with the drawing prune (Q56: 864 SVGs, about 109 MB, on the lane; 14 kept after the fixes) |
| `lane/w5` (WP10, WP17) | f395e70 | bb1ca27 | merge |
| `lane/w4` (WP13) | 28b284c | 68e1cc7 | merge |
| `lane/w9` (WP16) | cc22134 | 4ee3856 | merge |
| `lane/w2` (WP12) | a4080c2 | 5a43967 | merge |

No merge touched `HANDOFF.*`. fcd755c copies `main`'s current HANDOFF (83e8def) onto the branch so the two agree. Its message blames `lane/w5` for bringing in an older copy. That is wrong: the older copy is this branch's own base, 5d23c54.

Line numbers in the defects table point at the final tree.

## Gates

Interpreter: the worktree's `.venv`, Python 3.13, build123d 0.11.1, OCP 7.9.3.1.1, numpy 2.5.3. KiCad 10.0.6 `kicad-cli`. Everything ran on the final tree c5f87cb.

| Gate | Command | Result |
|---|---|---|
| Tests | `.venv/bin/python -m unittest discover -s tests -v` | **169 tests OK, 150.9 s, 0 skipped.** CAD, render, placement, frame_v2 native (clang harness) and board-release tests all run |
| Order 1, twice | `.venv/bin/python scripts/cad/bte_fit_shell.py --out <tmp>/A`, then `<tmp>/B` | Exit 0. All 15 solids are SHA-256 identical across A, B and `docs/fab/cad/v1/`: body_full_p15.step e4c90892…, body_full_p25.step 9083eb2d…, body_thin_p15.step d4aac001…, coupon.step 82689ab8…, lid.step bce82f1d…, plus the matching STL and 3MF |
| Renders, twice | `.venv/bin/python scripts/cad/render.py --out <tmp>/A`, then B | Exit 0. render_lateral.png f291b51b…, render_medial.png 18f88d46…, drawing.pdf aac59658… and manifest.json 5cc57920… are identical across A, B and `v1/` |
| v1 manifest vs main | `git diff main --quiet -- docs/fab/cad/v1/manifest.json` | identical |
| Stage B v2, twice (README command) | `.venv/bin/python scripts/cad/bte_fit_shell.py --params scripts/cad/params/stageb_v2.toml --out <tmp>/SA`, then SB | **Exit 3 both times** (files written, checks not all passed). The 9 solids and the manifest are byte-identical (manifest 724fd999…). Every named check carries numbers. `stage_b_not_measured`: TAB_envelope_air, V2_ADJUSTMENT, V2_BOSS, V2_HARNESS, V2_RECESS, V2_USB_medial. Two fail, both on the REF tab where it crosses the cavity end wall (s 38.2–39.25): V2_TAB_envelope (REF_body_mm3 1.194) and REF_WIRE_envelope (body_mm3 1.1902). Passing numbers: V2_BOARD_envelope 0/0 mm³ (underside 4.81, top 5.32), V2_STACK module–lid gap 0.38, V2_WALL_minima 1.5/1.5, V2_TOTAL_CHORD 47.9005, V2_M1_gate 50.9005 against M1 52, V2_CONTACT_STACK tip below the standoff top 0.81. V2_MODULE_envelope antenna_body_mm3 3.7167 is reported, not gated |
| Nothing written to cad/ | `git status --short docs/fab/cad` after all builds | empty. `docs/fab/cad/v2/` does not exist |
| Placement `--all` | `.venv/bin/python scripts/cad/placement.py --all --out-dir <tmp>` | 17.1 s, 3 SVGs (the closers). `--kept-drawings` writes 14, each byte-identical to the committed file |
| Board release | `.venv/bin/python scripts/board/release.py --out <tmp>` | Exit 0, `routed: false`. **ERC 0 errors / 0 warnings.** DRC 877 errors, 34 warnings, 0 unconnected (meaningless: 251 of 254 pads have no net, 0 tracks, 3 nets). BOM 58 rows = 58 placed parts. CPL 54. Gerbers 16 files incl. Eco1/Eco2 stiffener layers. STEP written; 4 models missing (listed in `step_missing_models`). `test_kicad_cli_is_installed` calls `self.fail`, not skip |
| Firmware | `arduino-cli compile --fqbn adafruit:nrf52:feather52840 --library firmware --output-dir <tmp> firmware/elicio_stream` | Exit 0. Flash 134,012 B (16 %), RAM 18,472 B (7 %) |
| Frozen files | `git diff main -- docs/fab/plan.md docs/fab/plan-v2.md docs/fab/open-questions.md docs/fab/interface.md docs/fab/contacts.md` | empty |
| Object growth | `git rev-list --objects main..review/r5 \| cut -d' ' -f1 \| git cat-file --batch-check='%(objectsize:disk)'` | **0.63 MB** on disk (274 objects; 7.09 MB uncompressed). Limit 10 MB |
| Wording | added lines vs main, grep `owner`, `user` | only the KiCad layer names `Eco1.User`, `Eco2.User`, `Cmts.User` |

## Defects

Severity: **H** breaks a gate, the solid, the board or the stream; **M** wrong number or claim in the record; **L** wording or missing citation.

| # | Sev | File:line | What was wrong | What changed | Commit |
|---|---|---|---|---|---|
| 1 | H | `scripts/cad/placement_v2.py:74` | Foam 0.3 in the packing, 0.5 in the solid and in `stageb_v2.toml`. The "closers" did not match the body they build | One `FOAM = 0.5`, used by the packing, the CAD and the doc. y7 no longer closes (module top 7.62 > LID_Y 7); the closers are y8, y8.5, y9 | fd4ad1a |
| 2 | H | `scripts/cad/placement_v2.py:103` | Interface II stack kept a DIN 439 nut under a standoff the board had already been put on top of; the board sat below the standoff tops | `standoff_y` / `ring_under`: ring 0.31 + standoff 3.0, so the board underside is 4.81 and the top 5.32; no nut. Q21 checks in `bte_fit_shell.py` follow | fd4ad1a |
| 3 | H | `scripts/cad/placement_v2.py:66` | The stiffener was FR4 0.3, which JLC does not make (0.1 / 0.2 / 0.4) | `STIFFENER = 0.4`; board 0.11 + 0.4 = 0.51. The KiCad project, Eco1 text and `board-v2.md` §18 changed to match | fd4ad1a, 6cc30d0 |
| 4 | H | `scripts/cad/placement_v2.py:288` | The antenna keep-out was laid along s while the module lies along u. On the PCB that rectangle covered 15 module pads | `_place_module` returns the keep-out at the low-u end when the length runs on u; it is seeded into the placers; the cell–antenna gap is a rectangle distance | fd4ad1a |
| 5 | H | `scripts/cad/placement_v2.py:143` | Placed two BAV199S clamps the board does not have and a wrong LDO package; the free area ignored the real parts | Real BOM packages: SOT23-6 USBLC6, SOD523 PESD, SOT23-5 LDO, placed pocket-first. `ARRAY`/`N_ARRAYS` and the clamp-distance rule removed. Test `test_board_parts_are_the_board_bom_packages` | fd4ad1a |
| 6 | H | `scripts/cad/placement_v2.py:1116` | Interface I never checked that the pads were on the rigid board. It looked closeable | Pad-on-board check placed after the outer-height check. Interface I closes 0 of 720; in every run pad_SIG1 and pad_REF are off the board | fd4ad1a |
| 7 | M | `scripts/cad/placement_v2.py:1652` | `packing-v2.md` §2–§8 carried hand-typed numbers and a Stage B table no build had produced | `STAGE_B_V2_MEASURED` holds the build's numbers; the doc is generated (`placement.py --packing-doc`); `test_cad` rebuilds and compares | fd4ad1a |
| 8 | M | `scripts/cad/bte_fit_shell.py:2469` | V2_WALL_minima probed at y 0.75, inside the 1.5 floor, and read the outer fillet | Side walls probed at mid-cavity height (y 4.75); 1.5/1.5 | fd4ad1a |
| 9 | L | `scripts/cad/params/stageb_v2.toml:1` | Header did not say what each provisional value waits on | Header lists V2_* (Rolf's pick), TAB_HEIGHT (Q22), CABLE_EXIT_S (decision 24), CLOSURE_PASSED, M1 52 default (Q34), CONTACT_* | fd4ad1a |
| 10 | H | `firmware/src/ads1292.h:44` | RESP2 written 0x02; SBAS502C requires bits 2 and 0 set | `ADS1292_RESP2_RLDREF_INT 0x07u` | 3b854da |
| 11 | H | `firmware/src/ads1292.h:36` | The unused CH2 ran at gain 12 on open inputs. SBAS502C: power it down with MUX 0001 (shorted) | `ADS1292_CH2SET_OFF 0x81u` used for CH2; test asserts reg 0x05 == 0x81, 0x0A == 0x07 | 3b854da |
| 12 | M | `firmware/src/undervoltage.h:17` | V_STOP 2700 / V_START 2800 placeholders | 3000 / 3200 from `board-v2.md` §6; tests at 3000/3001/3199/3200 | 3b854da |
| 13 | H | `firmware/elicio_stream/elicio_stream.ino:316` | A frame could span a gap in acquisition indices and still claim contiguity | Frames copy only consecutive indices; OVERRUN set when `first != next_acq` | 3b854da |
| 14 | H | `firmware/elicio_stream/elicio_stream.ino:163` | With VBUS present the AFE is unpowered but SPI and PWDN/START stayed driven, back-powering it through the pins | `afe_pins_safe()`: SPI.end, the five lines to INPUT; `afe_pins_active()` on restart. `firmware-v2.md` documents it with REGOUT0 | 3b854da |
| 15 | H | `docs/fab/board-v2.md:131` | R25 + R28 hung on ISET: RISET 6.8 k ∥ 20 k = 5.07 kΩ, charge current about 26.6 mA instead of 20 mA | R28 moved to LED_EN; ISET sees R25 into a high-Z ADC only | 6cc30d0 |
| 16 | H | `docs/fab/board-v2.md:145` | LED gate on ISET (about 1 V, below the 2N7002's worst-case threshold) and LED current from VBAT, about ITERM | LED from VBUS through R22, Q4 gate on LED_EN (P0.04, was NC) with R28 pull-down. Schematic relabelled | 6cc30d0 |
| 17 | H | `docs/fab/board-v2.md:167` | With Q5 off, P0.02 sat at VBAT through 1 MΩ, above the pin limit | Divider always connected to GND (R21.2 and Q5.3 to GND), Q5 DNP | 6cc30d0 |
| 18 | M | `hardware/board/elicio-v2.kicad_sch` | ERC 13 warnings: 12 symbol mismatches plus one footprint-link issue | Embedded symbol copies moved into `lib/elicio.kicad_sym`; J3 library name fixed. ERC 0/0, netlist unchanged | 6cc30d0 |
| 19 | M | `docs/fab/board-v2.md:296` | C25803, C25765 and C1525 were each on two different values, including R1–R3 on the G2 path | LCSC blank on 18 lines, UNVERIFIED, to be read at G3 | 6cc30d0 |
| 20 | H | `hardware/board/elicio-v2.kicad_pcb` | PCB not synced with the schematic (3 nets, 251 netless pads), not placeable (877 DRC), RF rule area in the wrong pose | Wrong RF zone removed, Q5 DNP, stiffener text fixed. Placement and sync are **not** fixed: decision 62. `board-v2.md` §15 now says so | 6cc30d0 |
| 21 | H | `scripts/board/release.py:118` | Release could report "unconnected 0" on a board with no nets and pass | `pcb_stats()`; `--routed` fails closed on DRC errors, unconnected items, netless pads or no tracks; summary carries `routed` and the stats; STEP without `--board-only`. Test `test_routed_release_fails_closed_on_this_board` | 6cc30d0 |
| 22 | M | `docs/fab/board-v2.md:81` | The G2 default-state sentence had the P-FET off with no MCU; it is on without VBUS | Sentence and table rewritten from the netlist | 6cc30d0 |
| 23 | M | `docs/fab/board-v2.md:109` | REGOUT0 not documented: an erased nRF52840 runs at 1.8 V in HV mode, below the ADS VIH | G4 text: first load at 1.8 V, 3.0 V after UICR REGOUT0; probe limits from the page (3.3 V nominal only; WP17's 3.63 V UNVERIFIED) | 6cc30d0, c5f87cb |
| 24 | M | `docs/fab/board-v2.md:328` | Decoupling "per typical"; SBAS502C asks for 10 µF + 0.1 µF per supply | Marked as a deviation; decision 68 | 6cc30d0 |
| 25 | M | `docs/fab/board-v2.md:181` | Q54: only one Raytac route, LCSC numbers disagree between lanes | Both routes (JLC global sourcing, consignment from DigiKey/Mouser); C5118826 vs C5142646 UNVERIFIED | c5f87cb |
| 26 | M | `docs/EARPIECE_DESIGN.md:541` | Q50–Q55 missing from the record; Q48 price summed wrong | Each recorded once with pointers from D-1, D-3, D-4, Q45; header Q37–Q55; Q48 "$33.95 and $12.00 listed, $45.95 together" | 310f87e |
| 27 | M | `docs/fab/orders-v2.md:71` | Ledger numbers without URLs, per-order rows read as totals, no flex lines, the cell priced | URLs filled, rows renamed "allowance (not a delivered total)", flex fixture and stiffener lines, Raytac line, cell an open line | 310f87e |
| 28 | M | `docs/fab/L6-research-v3.md:175` | Debug Probe "0–3.63 V" is not on the cited page; two quotes reworded | Retagged UNVERIFIED (2026-09-17); page quotes put in | e1a8639 |
| 29 | M | `docs/fab/L6-research-v3.md:98` | "Standard PCBA minimum 70 × 70 mm" not on the cited page; JLC's FPC page states it for FPC+SMT only | Retagged UNVERIFIED with the FPC quote | e1a8639 |
| 30 | M | `docs/fab/L6-research-v3.md:132` | Programming fee "$7.86 + $7.86/h" not on the cited page | Retagged UNVERIFIED | e1a8639 |
| 31 | M | `docs/fab/L6-research-v3.md:47` | DigiKey price at 10 is $0.438, not $0.478; the page says 5.50 mm hex, the lane wrote 5.00 | Page values put in; the Harwin drawing's "5.00 A/F MAX" wins | e1a8639 |
| 32 | L | `docs/fab/L6-research-v3.md:17` | SparkFun quote reworded; the page's own text says "JST-SH connector - 2mm spacing" | Page quote put in | e1a8639 |
| 33 | L | `docs/fab/L6-research-v3.md:194` | Bootloader quote was a paraphrase; `0x20007F7C` not in the cited README | README quote ("within 500 ms") put in; address UNVERIFIED | e1a8639 |
| 34 | M | `docs/fab/L6-research-v3.md:117`, `docs/fab/L5-research-v2.md:89` | TLV713 rows are the 3.3 V TLV71333 (C90840, basic); the board uses the 3.0 V TLV71330 (C2863702, extended) | Note on both; the row's figures UNVERIFIED | 94cb374, e1a8639 |
| 35 | L | `docs/fab/L5-research-v2.md:103`, L6 §4.2 | E73 LCSC page (identifier fix) returned 404 on re-read; the E73 drawing was never reached | Said so; C356849 UNVERIFIED; XIAO P0.13 fix confirmed with the wiki quote | 94cb374, e1a8639 |
| 36 | L | `docs/fab/L5-research-v2.md:122` | §4.2 trade-off list could read as a recommendation | Marked as the lane's list; plan v2 §1 item 5 is what the plan chose | 94cb374 |

Spot checks (live pages, 2026-09-17):

| Number | Page | Result |
|---|---|---|
| Harwin R25-100XX02 geometry | content.harwin.com DRG-01991 PDF | confirmed: "5.00 A/F MAX", L1 4.00, ±0.10, CW614N, nickel |
| DigiKey stock | digikey.com 952-2175-ND | "In-Stock: 3,847" confirmed; 10-off price and A/F wrong (#31) |
| JLC 70 × 70 | jlcpcb.com | not on page, UNVERIFIED (#29) |
| JLC programming fee | jlcpcb.com | not on page, UNVERIFIED (#30) |
| TLV713 3.3 V vs 3.0 V | lcsc.com (root) | wrong variant for the board (#34) |
| Debug Probe 3.63 V | raspberrypi.com debug-probe docs | absent; only "3.3V nominal I/O" (#28) |
| Bootloader 500 ms | github.com/adafruit/Adafruit_nRF52_Bootloader | confirmed, reworded quote fixed (#33) |
| SparkFun connector | sparkfun.com/products/25270 | "JST-SH connector - 2mm spacing" confirmed; contradicts itself (#32) |

Checked and found correct: the TC2030 map equals plan v2 §8 (1 VTref, 2 SWDIO, 3 GND, 4 SWCLK, 5 GND, 6 nRESET; netlist J4 pins 3 and 5 on GND). `montage.md` above §8 is byte-identical to `main`. `placement.py`'s older tests pass unchanged.

## Needs a decision

57. **Foam 0.3 vs 0.5.** Plan v2 §3 says 0.3. The solid and the review use 0.5, the value the lane's own Stage B file used. The plan text needs an erratum, or everything goes back to 0.3 and y7 might close again. Rolf.
58. **Interface II stack.** Plan text and WP11 had a DIN 439 nut under the standoff. With the board on the standoff tops, the clamp is ring + standoff + board, with no nut (4.81 underside). Accept the no-nut clamp or re-specify the stack. Rolf.
59. **REF tab through the end wall.** Stage B v2 fails V2_TAB_envelope and REF_WIRE_envelope (1.19 mm³) where the REF tab crosses the cavity end wall at s 38.2–39.25. Needs a slot in the wall (WP14) or a tab route that stays in the cavity. Nothing orders until this passes.
60. **Six stiffener pieces** (one FR4 0.4 island plus Ø6 rings and tab pieces) vs JLC's extra-stiffener fee at four or more pieces. Merge pieces or accept the fee.
61. **Flex allowance** in `orders-v2.md` was not re-derived for the 0.4 stiffener and the fixture line. It stays an allowance until a configured checkout exists.
62. **PCB placement and sync.** The PCB follows the lane's packing run, not `packing-v2.md` §5 (review r5). It has 3 nets and 877 DRC errors. It must be re-placed from §5, synced from the schematic, then routed and released with `--routed`. WP12 turn 3.
63. **LCSC codes at G3.** 18 lines were blanked, and U1's number is disputed (C5118826 vs C5142646). They get read from the assembler's library at G3.
64. **Debug Probe target voltage.** On first load the target is at 1.8 V (REGOUT0 erased), 3.0 V after. The probe page only says 3.3 V nominal I/O. Options: level shifter, a probe with VTref sensing, or setting REGOUT0 some other way before the probe connects. G4.
65. **System load vs ITERM.** The board's standby load during charge against the BQ25100 termination floor. WP12's "2 mA" item needs a number from the sheet and a measured board.
66. **Interface I REF site** (s 43) is past every rigid board in the 720 runs. Interface I stays out unless the REF site moves or a flex tail carries it.
67. **Raytac route.** JLC global sourcing or consignment (Q54 records both). Rolf picks at G3.
68. **ADS1292 decoupling.** Board has 1 µF + 2 × 100 nF on a shared +3V0; SBAS502C wants 10 µF + 0.1 µF per supply. Change the BOM, or accept the deviation with a measured noise floor.
