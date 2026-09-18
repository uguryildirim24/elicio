# Code review, round 6

Reviewer rev6 on `review/r6`. Date 2026-09-18.

**Verdict: MERGE-AFTER-DECISION.**
The merged tree tests clean. Order 1 and Stage B v2 regenerate unchanged. Stage B v2 still exits 3 on Q59 only, because the shell path carries `REF_end_wall_slot` and the Stage B path does not.
The shell now measures itself instead of recording constants, and four checks fail (closure, USB end, edges, wall minima). Decisions 69–77 come before any order. The board is not routed, and it cannot be routed on the WP12b placement (decision 70); WP12c owns the copper.

## Merged

In brief order, with no conflicts: `lane/w3` (WP11b) 3036226, `lane/w1-r6` (WP14) a01eb53, `lane/w5` (WP17b) ee389b3, `lane/w4` (WP13b) 5a0275c, `lane/w9` (WP15) 82f2367, and `lane/w2` at `480e355` (29a6d72). Then, per the coordinator's amendment, `lane/w2` at `e3e085b` (1e290de). Main's HANDOFF (`d4b5a93`) was kept (17abc60). `lane/w1` (round 5, 109 MB) stays out of history.

Coordinator note 2 asked to merge `lane/w3` at `bcecc83` exactly. That commit is already an ancestor of this branch (via the `lane/w3` merge), so there is nothing to merge. Its other ask, that `summary.json` never says `routed: true` on a refused release, is 0c95ff4: `routed` is `bool(args.routed) and not refused` (`scripts/board/release.py:348`), and `test_routed_release_fails_closed_on_this_board` asserts `routed: false` with `routed_requested: true`.

WP12b's last commit says "routed, released". The branch is neither: `release.py --routed` is refused with 1293 DRC errors and 31 unconnected items. Before 0c95ff4, `summary.json` said `"routed": true` on that refused release.

## Gates

Venv `.venv`, Python 3.13, `-e '.[cad]' -e '.[ble]'`: build123d 0.11.1, OCP 7.9.3.1.1, numpy 2.5.3, trimesh 5.1.0, matplotlib 3.11.2, pypdf 6.19.0, bleak 3.0.2. kicad-cli 10.0.6. arduino-cli with adafruit:nrf52 1.7.0.

| Gate | Command | Result |
|---|---|---|
| Tests, full venv | `.venv/bin/python -m unittest discover -s tests -v` | 206 tests, OK, **0 skipped**, 193 s (CAD, render, placement, shell v2, sheets, receiver, frame_v2 native harness and board-release all ran) |
| Tests, base venv (numpy only) | same, in a venv with the base install only (no extras) | 206 tests, OK, 34 skipped, each naming its extra: `cad` 22 (build123d) + 1 (matplotlib/trimesh), `sheets` 3 (matplotlib/pypdf), `sheets` or `cad` 8 (matplotlib). `ble`: 0; bleak is imported lazily and no test needs a radio. Before 0f1159b this venv had 18 errors |
| Order 1 twice | `bte_fit_shell.py --out <tmp>` ×2, then `render.py --out <tmp>` | Solids, views and manifest identical run to run and byte-identical to `docs/fab/cad/v1/` |
| v1 manifest vs main | `cmp <(git show main:docs/fab/cad/v1/manifest.json) docs/fab/cad/v1/manifest.json` | identical |
| Stage B v2 twice | `bte_fit_shell.py --params scripts/cad/params/stageb_v2.toml --out <tmp>` ×2 | exit 3 both times, byte-identical to each other. They are also identical to a build of the pre-review tree (`git archive HEAD` before my CAD commits), except the `commit` stamp. The measured failures are `REF_WIRE_envelope` and `V2_TAB_envelope`, both the REF tab crossing the end wall (Q59). The other six `stage_b_failing` names are NOT_MEASURED rows. The Stage B path has no slot; the shell path carries it |
| Shell v2 twice | `bte_fit_shell.py --params scripts/cad/params/shell_v2.toml --stage shell --out <tmp>` ×2, `render.py`, `manifest.py --check-bytes` | Solids, views and manifest are byte-identical run to run. Solids are byte-identical to `docs/fab/cad/v2/`. Views differ in a temp dir only by the `commit` stamp ("unknown" outside the repo); an in-place rebuild of `docs/fab/cad/v2/` leaves `git status` clean. `--check-bytes` ok. **Exit 3, not 0**: `stage_b_failing` = `V2_CLOSURE`, `V2_EDGE_radii`, `V2_USB_end`, `V2_WALL_minima`, each a measured number. The lane's exit 0 came from constants (defects 2–5) |
| Board release | `scripts/board/release.py --out <tmp>` | exit 0; ERC 0 errors, 0 warnings; BOM 59 rows = 59 placed parts = 59 CPL rows; every BOM line has an LCSC code; outputs present; `routed: false`, `refused: {}` |
| Board release routed | `release.py --routed --out <tmp>` | exit 1, `routed release refused: {"drc_errors": 1293, "unconnected_items": 31}`; the summary says `routed: false`, `routed_requested: true`; `test_routed_release_fails_closed_on_this_board` asserts it |
| Firmware | `arduino-cli compile --fqbn adafruit:nrf52:feather52840 --library firmware --output-dir <tmp> firmware/elicio_stream` | exit 0. 134012 bytes (16 %) of 815104 flash; 18472 bytes (7 %) of 237568 RAM |
| Pin map | `firmware/src/board_pins.h` vs `board-v2.md` §9 | all 13 GPIO equal (P0.08, 06, 15, 13, 17, 20, 22, 24, 31, 02, 03, 04, 18) |
| Template | `scripts/sheets/template.py --out <tmp>` ×2 | identical run to run and to committed `docs/fab/template.pdf` and `docs/fab/sheets/m1–m8.svg` |
| Receiver | `elicio receive --simulate-live --out <tmp>`, then `elicio receive-check <tmp>` | exit 0 and exit 0 (`exit_code` 0, 0 dropouts, losses ≥ 1 as the test expects) |
| Frozen files | `git diff main -- docs/fab/plan.md docs/fab/plan-v2.md docs/fab/open-questions.md docs/fab/interface.md docs/fab/contacts.md docs/fab/cad/v1/` | empty |
| Repo growth | `git rev-list --objects main..HEAD` sized with `cat-file --batch-check='%(objectsize:disk)'` | 6.70 MB on disk (19.36 MB raw), under 12 MB. `count-objects -vH`: size-pack 24.29 MiB + 3.51 MiB loose, against 20.58 MiB before the merges; the object store is shared with the other lanes |
| Zero-track DRC (coordinator note 2) | `git show 845bac7:hardware/board/elicio-v2.kicad_pcb` (with its `.kicad_pro`), 0 segments/arcs, `kicad-cli pcb drc --format json` | 128 errors, 132 unconnected. By type: 38 solder_mask_bridge, 32 shorting_items, 26 clearance, 18 copper_edge_clearance, 9 hole_clearance, 5 items_not_allowed. Top pairs: U2 copper-to-edge (11), J4/U5 hole clearance and mask bridge (5 + 5), J3/U1 (4 clearance, 4 shorting, 4 mask bridge), J3/L1, SW1/U2 shorting, J3/SW1 shorting and mask bridge, J2/J4 mask bridge, Q5/R26 shorting, J1 hole clearance to C5/R16/R29, R25 and C10 in a no-parts area. It confirms WP12c's finding: the footprints collide before any copper is laid |

The lane's 13 `CadRegenTests` failures do not reproduce here. Order 1 matches on build123d 0.11.1 / OCP 7.9.3.1.1, the pins round 5 traced them to.

Section cuts through the three standoff pockets, the REF slot, the USB wall and a snap were made in the body frame from the exported STEP (rotated back by THETA_DEG) before any check was trusted. They found defects 1, 2, 3 and 6.

## Defects

Line numbers are at the final commit.

| Sev | File:line | What was wrong | What changed | Commit |
|---|---|---|---|---|
| H | `scripts/cad/bte_fit_shell.py:355`, `:3388` | The hex well was AF 6.3 plus a Ø7.4 cylinder. That is round: the cylinder (r 3.70) swallows the hex (circumradius 3.64), so the brass standoff could turn and the collar flats were 0.2 thick. The REF well was round too. The packing's 5 × 5 boxes were cut on top | Captive well AF 5.30 = 5.00 A/F max (Harwin) + 0.3 (JLC PA12 ±0.3). It locks: 5.30 + 0.3 = 5.60 < 5.77 across the standoff's corners. Collar AF 8.4, ring seat Ø6.4 (Ø6.0 ring outline + 0.10 FPC + 0.3). Box cuts removed. REF gets the slot clearance through its collar. `V2_STANDOFF` measures a 5 AF prism (0 mm³ nylon) and the well flats (5.30) and corners (r 3.06); `V2_RING_seat` measures Ø6.40 | c68d4b2 |
| H | `bte_fit_shell.py:2903` | `V2_USB_end` ligament was arithmetic (u 5.5 − HOOK_ROOT_X 4.0 = 1.5). The hook's elliptical root reaches u 6.39 on the end face and fills the opening's anterior 0.89. The packing puts the receptacle at s −5.80…1.50, standing 4.8 outside the outer face (s −1.00). Neither was measured | The hook is built in the body frame and probed on the face; the packing's `usb` box is measured against the face. Now fails: ligament −0.89, mouth −4.80. Decision 71 | c68d4b2 |
| H | `bte_fit_shell.py:2993` | `V2_CLOSURE` computed ε 0.0117 from constants (L 8, t 1, y 0.5). The built beam is 0.5 thick, hangs 1.0 and stands 0.18 past the wall (ε 0.135). The snap grooves run to lid_y + 0.15 and the lip groove to lid_y + 0.12, so nothing holds the lid: it lifts straight off. 0.5 is also under JLC's 1 mm wall | Measures the built beam and the undercut over each hook and the lip. Now fails: undercut 0/0/0, ε 0.135. `shell-v2.md` §2 rewritten. Decision 72 | c68d4b2 |
| M | `bte_fit_shell.py:3054` | `V2_EDGE_radii` probed one station inside the Ø19 crown blister and recorded `outside_min_R=1.0` as a constant. The lid rim is 0.8 | Samples the lid top 3 mm apart at 7 stations (4 flat) and reads the built rim R 0.8. Now fails | c68d4b2 |
| M | `bte_fit_shell.py:3192` | `CLOSURE_PASSED`, `KEEPOUT_SIGNAL_air`, `KEEPOUT_REF_air` were recorded `True` as constants on the shell, next to the Stage B rows of the same name (duplicates in the manifest) | NOT_MEASURED by name. A shell row replaces the Stage B row in place (`:2054`), so each check is listed once | c68d4b2 |
| M | `bte_fit_shell.py:1959`, `:2259` | The shell kept v1's REF wire channel (1.6 × 1.6 through the end wall above the Q59 slot, leaving a 0.54 bridge) and the Ø2.0 bench-cable exit through the posterior wall at s 35 | Not cut when `STAGE=shell`; `CABLE_EXIT_cavity` NOT_MEASURED with `wall_closed` 1. Stage B unchanged | c68d4b2 |
| M | `bte_fit_shell.py:1985` | `_bisect` ran zero iterations when lo > hi and returned the midpoint | Bisects either way. Order 1 and Stage B v2 are unchanged, so no existing caller used a descending range | c68d4b2 |
| M | `bte_fit_shell.py` `V2_WALL_minima` | `usb_ligament_hook` and `snap_residual` were arithmetic | Measured (−0.89; 1.10). Fails on the USB ligament only | c68d4b2 |
| M | `tests/test_cad.py` `CadShellV2BuildTests` | Asserted that the constant checks passed and that the shell exits 0. It never compared with the committed v2 files | Asserts the measured failures and numbers, the NOT_MEASURED rows, exit 3 with the four names, and solids and `files` equal to `docs/fab/cad/v2/` | c68d4b2 |
| M | `scripts/cad/render.py:545`, `:554`, `:915` | The shell render and drawing said "Two cantilever snaps close the lid" and "Recess 1.0 in an outer pad" | Labels state the measured failures and the decision numbers; v1 views unchanged | 9210599 |
| H | `scripts/board/release.py:345` | `"routed": true` on a refused `--routed` release | `routed` is true only when a `--routed` release passes; `routed_requested` and `refused` are added; the test asserts the refusal | 0c95ff4 |
| M | `tests/test_board_release.py` | The placement-agreement test compared the PCB with a hand copy of §5 | It parses the `packing-v2.md` §5 bullets and the REF tab line | 0c95ff4 |
| M | `scripts/board/release.py:301` | The CPL had 61 rows for a 59-row BOM. `--smd-only` dropped the THT bench header J3, and the PCB does not carry the schematic's DNP on Q5, R29, R30 | The pos export keeps THT; the CPL is filtered to the BOM's designators; a BOM part without a CPL row is a blocker and exit 1; test and §17 follow | 0d75fcd |
| M | `scripts/board/release.py`, `tests/test_board_release.py` | Bare `read_text()`. Run after `test_cad` in one process (OCCT sets the C locale), the placement test decoded the PCB as ASCII and errored | Every read and write names utf-8 | 59c7945 |
| H | `src/elicio/receiver_v2.py:354` | The dropout scan let a later RESTART's settling window hide an earlier dropout (0 stretches on that case). `receive-check` had no exit-code table | One settling window per RESTART; threshold tested at 201/202 samples. Exit codes 0 ok, 1 same-criterion failure (lines 3.5–3.10), 2 not a session, 3 dropout on line 3.4; documented in `receiver-v2.md` | 6bf201f |
| L | `tests/test_receiver_v2.py` | `setUpClass` rewrote the committed fixtures | A test compares the committed fixtures with the generators | 6bf201f |
| M | `tests/test_placement.py:250`, `pyproject.toml` | In a venv without matplotlib, 18 `PlacementV2Tests` errored instead of skipping. No extra carried the sheets' matplotlib/pypdf | `NEEDS_MATPLOTLIB` skip naming the extra. New `sheets` extra. Every skip message names its extra | 0f1159b |
| H | `docs/fab/board-v2.md:15`, `:269`, `:330`, `:476` | §11, the zone row and packing say the ring is 0.31 (FR4 0.2). §12 and the Gerber draw no ring FR4, so as drawn the standoff clamps 0.11 and lands 0.2 low | Stated in each place with the numbers. Decision 73 | d50ddb3 |
| H | `board-v2.md:285`, `shell-v2.md:44` | The shell has two bosses with pilots at (14.85, 21.50) under J3 and (14.85, 28.10) under U1. The board has no holes, so plan v2 §8 step 5 cannot be done. P3 (s 43.0) is past the island (s 37.6), so the island rests on two standoffs | Stated in both docs and in `assemble.md` steps 4–5. Decision 74 | d50ddb3 |
| H | `board-v2.md` §11 | SIG tabs are 7.0 mm strips off the island edges. A 180° fold at R 1.5 stands about 1.6 outside the edge, and there is 0.75 to the wall. Edge to ring centre folded is about 8.5, not 7.0. P1's packing attach (5.90, 29.00) is in the antenna keep-out | Stated. Decision 75 | d50ddb3 |
| H | `hardware/board/elicio-v2.kicad_pcb` R1 (−1.25, 22.0), R2 (21.25, 33.1), R3 (8.5, 40.3) | The 220 kΩ series resistors sit on the tabs, 3.5 / 3.5 / 2.7 mm from the roots. That is inside §11's 4 mm no-part strain-relief window and on the fold. Each tab then carries two nets (SIG1 and AFE_IN1P, …), which is why the lane found the 1.0 mm contact rule impossible | Not fixed: placement plus routing is WP12c's (brief). See "To WP12c" | — |
| H | `tests/test_board_release.py` `test_named_smt_centres_match_packing_v2_within_0_1_mm`, `packing-v2.md` §5 | The test pins the PCB to the packing placement within 0.1 mm. But the packing's part envelopes are smaller than the real KiCad courtyards, so the pinned placement cannot be built (zero-track DRC above) | Not fixed: moving footprints is out of this round (coordinator note 2). The test stays and asserts agreement with a table that WP11c re-packs. Decision 70 | — |
| M | `elicio-v2.kicad_pcb` J3 | Bench header pads Ø1.7 at 2.54 pitch, all three on contact nets: 0.84 between SIG1/SIG2/REF, under the Contact class 1.0 | Not fixed (WP12c regenerates the PCB). See "To WP12c" | — |
| M | `docs/fab/L7-research-v4.md` | Paraphrases shown as verbatim quotes (stiffener fee, ADS1292). BMP price stale. The Jauch DigiKey link is a Siemens part. FR4 0.3 is not on the page. The fixture fee conflicts with §18. §4.1 codes are refuted by §13. "Includes PCM" is inference | Re-check block at the top plus inline notes | 9720d2a |
| M | `docs/fab/packing-v2.md:1472` via `scripts/cad/placement_v2.py` | The record still carried the bare 501015 cell | Cell record: the 501012 pack in the w20 y8 pocket. §1e lists `A_pack501012_series_w20_y8_iII_s3` as a closer; packed 5.6 ≤ 5.7; 2.6 along s for foam; J2 unchanged. Regenerated, not edited | a20c1d2 |
| M | `docs/fab/order-parts.md`, `assemble.md`, `order-shell.md`, `order-board.md` | They proposed the RPi Debug Probe as the kit. The cell line was 501015-class. Fields the tree now settles were "the agent fills this". The shell's do-not-order line read `checks` (which includes NOT_MEASURED rows) | Probe: not for an erased part; L7 §1.3's three VTref probes listed, none picked; no purchase until G4. Cell line and decision 69. v2 file names, gerber names, coverlay, stiffener count and fee rule, colour and finish option names. Steps 4, 5 and 7 stop on decisions 74 and 72 | 3d700cf |
| L | `docs/EARPIECE_DESIGN.md` | No pointer to decisions 57–68 | One pointer to Q57–Q68 and to 69 on | ea9e62a |
| L | `docs/fab/shell-v2.md`, `receiver-v2.md` | Restated the closure calculation and the checklist with the constant numbers | Rewritten to the measured numbers; decisions moved here | c68d4b2, final |
| M | Shell look, `bte_fit_shell.py` lid crown and rim | See §7 below | Not fixed in this round; next WP14 turn | — |

## §7 look

On the renders, the shell reads as a printed block with a hook, not an earbud. The lateral view is a flat 20 × 48 plate with a Ø19 spherical blister at s 22. Four of six stations along the lid are flat over 3 mm, so "one continuously curved lateral shell" fails. The lid rim is R 0.8 against R ≥ 1.0. The lid is a 1.0 mm plate, so R 1.0 on its own edge is at the limit; the outside edge needs the lid to overlap the wall tops. The hook's joint to the body is sharp. The script finds no tube-to-top-face edge to blend, so the stated 1.5 blend never ran. A rectangular USB pad stands out of the end face, and the hook end face is planar. In the edge-on view the tail's hinge lip steps out. The medial face is right: flat, the three domes the only things on it, the outline filleted. The tail loft and REF dome read well.

What the kernel allows inside the one construction path: a lofted lid top across u and s with the crown fading to zero at the rim (the hook already uses a loft), the lid lapping the wall tops so the outside edge can take R 1.0, and a circular hook root blending into the ellipse. I did not do these this round. They are construction work for the next WP14 turn, not plan changes. The hook blend is decision 77 only if that turn cannot build it.

## Needs a decision

69. **Cell purchase route — Rolf's.** The record cell is the 501012 pack in the w20 × y8 pocket (`packing-v2.md` §5). Two routes:
    - a marketplace 501012 pack. It has no drawing and no named listing (L7 §7.7; plan v2 R2 and §9 ask for page price, stock and drawing).
    - a manufacturer sample of the 17.0 mm 501015 pack. That needs M1 ≥ 52.5 and a body 1.5 mm longer, which re-opens the shell and the board.

    I did not pick or order a cell.
70. **Re-pack with the real courtyards.** The board cannot be routed on the WP12b placement. With zero tracks, DRC reports 128 errors and 132 unconnected (845bac7):
    - footprints overlap: J3/SW1, J3/U1, J2/J4, U5/J4, SW1/U2, Q5/R26;
    - U2 and J2 break copper-to-edge;
    - J4's NPTH is too close to U5;
    - R25 and C10 sit in the RF feed notch (items_not_allowed). WP12c also reports U3 inside U1's courtyard; kicad-cli did not flag courtyards on this file (the check is off), so I have not confirmed that one;
    - the Contact class 1.0 cannot hold across R1–R3's 0402 pad gap (0.48) or J3's 2.54 pitch.

    The packing table's part envelopes are smaller than the footprint courtyards, and the placement test pins that table. Re-pack from the courtyards in `elicio-v2.kicad_pcb`: WP11c on `lane/w3` after `bcecc83`. Then re-place and route (WP12c). A re-pack may move the body's closers, which feeds decisions 71–75. No routing or footprint moves in this round.
71. **USB-C on the round 5 winner.** With a real receptacle, the winner does not close. The packing hangs it 4.8 mm outside the end face, and the space inside is the cell's. The hook root fills 0.89 of the opening. Options:
    - a longer body with the cell moved back;
    - moving the hook root posteriorly by ≥ 2.4 mm, plus room for the receptacle;
    - the medial port of plan v2 §5.4, which the packing found blocked by the cell.
72. **Closure.** The drawn snaps cannot work: there is no undercut, and no ≥ 1 mm beam fits the 0.75 mm beside the module. Options: plan v2 §7's concealed tail screw plus the hinge lip, or a snap site that needs a wider body.
73. **Ring stack.** Packing, the shell and Q58 assume a 0.31 ring (PI 0.11 + FR4 0.2). The board draws none. Options:
    - three FR4 0.2 ring pieces. The count becomes 5, over JLC's extra-fee threshold of 4; the amount is known only at checkout;
    - a shell with the seats 0.2 higher, clamping 0.11 of flex.
74. **Island retention.** The board has no mounting holes; the bosses sit under J3 and U1; the island rests on two standoffs. Options:
    - two holes in the island at the boss sites (WP12c placement);
    - no bosses, and a lid rib pressing the island onto the standoffs;
    - a third standoff under the island.
75. **Tab fold.** A 7.0 mm strip off the island's side edge cannot fold 180° at R 1.5 within 0.75 of the wall, and it is about 1.5 mm short. P1's attach is in the antenna keep-out. Options: route SIG1/SIG2 out of the island's neck end, or give the side walls fold pockets and lengthen the strips. This decision sets the same number in the PCB, the packing table and the shell's channels.
76. **Montage §8 line 3.4.** `receive-check` exits 3 on a dropout, which is line 3.4 ("revised" in the table, not "same criterion"). Does a 3.4 dropout stop S2? Until decided, code 3 is treated as a stop (`receiver-v2.md`).
77. **Hook joint blend.** Plan v2 §7 asks for a stated fillet. If the next WP14 turn cannot build it with a circular root, either accept a stated unblended joint or change the hook section.

## To WP12c

The contact-net rule stays in `elicio-v2.kicad_pro`: net class `Contact` (SIG1, SIG2, REF), clearance 1.0 mm to every other net.

It holds on the tabs when each tab carries one net. A 0.15 track on a 2.5 strip with 0.3 copper-to-edge fits. So:

- Move R1–R3 onto the island at the tab roots, clear of §11's 4 mm window and the fold.
- Where the island has no room (R3: the module fills the island's end), put the resistor on the tab's flat run past the fold. Scope a custom rule to that resistor's own pad pair only.
- J3's pads: Ø1.5 (1.04 between contact nets, annular 0.25), or a rule scoped to J3.
- Route only after decision 70's re-pack. Decisions 73–75 change the tab length, the ring stiffeners and possibly island holes, so take them with that re-pack.
