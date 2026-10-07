# Lane t-0014 — finish the v4 earpiece board

Body stays 18 × 8.1 mm: nothing moved off the island. **Not ready to order.** The board has no shorts, no clearance errors and no starved thermals under the project rules, but 10 connections are still open (5 GND, 5 signal) after six router runs and every finishing trick I had. Each open sits behind one foreign track in a 0.4–0.6 mm gap in the two B corridors of the island; the design note names the copper in the way of each. The release files exist for review only (`routed: false`). You still have to decide: the five shell changes, the cell (501012 kept), the parts without a JLC code and the consigned U1/U5/J2, and how the next round closes the routing: a placement round first (my recommendation), a JLC confirmation for 0.075 rules in the corridors, or a third copper layer.

## Release outputs

All under `hardware/board/release/elicio-v4/` in the worktree (the folder is gitignored; `release.py --board elicio-v4` regenerates it in two minutes):

- `gerbers/`: 17 files (F/B copper, mask, paste, silkscreen, Edge_Cuts, the User layers, `elicio-v4-job.gbrjob`, `elicio-v4-PTH.drl`, `elicio-v4-NPTH.drl`).
- `bom.csv`: 58 rows. U1 ISP1807-LR-RS, U5 TPS7A0230PDQNR and J2 Molex 202656-0021 say `CONSIGNED` in the LCSC column. R31–R33 are C881401. Q2–Q4, R18, R19 and C14 have no code.
- `cpl.csv`: 58 rows (and `pos.csv`, KiCad's raw placement).
- `elicio-v4.step`: written; five footprints have no 3D model (Molex 202656, TI DSBGA-6, TI RSM0032, TI X2SON-4, SOT-883).
- `erc.json` (0 errors), `drc.json` (0 errors, 10 unconnected), `summary.json` (`routed: false`).

`release.py --board elicio-v4 --routed`: exit 1, `routed release refused: {"unconnected_items": 10}`. Without `--routed`: exit 0.

Final DRC (kicad-cli 10.0.6, project rules `elicio-v4.kicad_dru`, `--refill-zones --save-board --schematic-parity`), verbatim:

```
Found 75 violations
Found 10 unconnected items
Found 2 schematic parity issues
```

The 75 are warnings: 64 `lib_footprint_issues` (embedded footprints), 10 `track_dangling` (the free ends of the open connections), 1 `via_dangling` (the +VDD pre-route via, used on F only). Errors: 0. The parity issues are J2's two MP pads, which have no schematic pin. Tests: `.venv/bin/python -m unittest discover -s tests -q` ran 281, OK (60 skipped).

## What I did

1. **Merged** t-0012 (815ca29, Opus's board) and t-0013 (058b08e, the r12 reviewer's fix). No rebase.
2. **J3 cut edge (Q97(d)).** J3 is a skin-connected gel-lead bench header, so it cannot tap the AFE side of R1–R3 directly (plan-v2 R7: every gel-header path gets its own 220 kΩ). Each J3 pin has its own 220 kΩ (R31–R33, 0402, C881401) on the break-off tab, and only AFE-side copper (AFE_IN1P, AFE_IN1N, RLD_FB, F 0.10) crosses the neck and the cut. Contact nets end at R1–R3 on the island. The tab grew (u 20.10–33.40 × s 16.0–28.0); R32 sits on the neck. Design note §2, §4.6, §5.4, §5.5; `tests/test_board_v4.py` checks it and passes on the committed board.
3. **ISP1807 VSS pads 14/16/18.** Tied to the B pour by two locked GND vias between the pads at (6.70, 28.725) and (6.70, 29.375): drills in the 0.25 gaps, ring edge 0.05 outside the RF band, no copper in the band. Not via-in-pad. The coverlay window over the land and wicking into the 0.15 holes are UNVERIFIED with JLC (§3.1, §11.1). I could not quote Insight SiP on internal ties (no web lane in this session); with the vias it is no longer needed.
4. **GND.** GND cannot be added after the signals at this density: on Opus's routing the pours plus the finisher reach 15 of 37 pieces and the rest are boxed in on both layers. As one live net it never converges. What worked best: the GND pads the pours cannot reach split into three regional nets (west stack, power corner, R19/R21/R28/C15; `v4_gnd_split.py`), routed with everything else for 80 rounds, merged back, filled, then the finisher and a new stitching tool (`v4_stitch.py`: vias where F and B GND overlap, own-pad vias allowed inside U2's exposed pad) joined the pours. Five GND pieces stay open: the pour inside U2's pad ring, three small B islands under U2, and the P5 charge run's island in the north-east corner. §9.4 has each with the copper in the way (+3V0 for three of them, ISET, VBUS).
5. **Starved thermals.** No relaxation of the DRC check. Exposed pads (U2.33, U4.5, U5.5) and J2's mounting pads connect solid by a rule in `hardware/board/elicio-v4.kicad_dru`; every 0201/0402 pad keeps its relief; where the pour reaches a pad from one side only, a 0.10 GND track from the pad into the pour is the second connection (`v4_thermal_stubs.py`, nine of them, listed in §9.3). Result: 0 starved-thermal errors. No Contact, creepage or clearance rule changed.
6. **Release.** `--routed` refused, as it must. It also refused on 72 "pads without net": KiCad's footprints carry paste-only pads with blank numbers, which cannot have a net; `scripts/board/release.py` now counts copper pads only. That would have blocked a fully routed board too. The plain release ran clean (ERC 0, DRC 0 errors).
7. **Placement relief 5 and a pre-route** (§9.2): the west stack 0.10 west, C8/C14/C11 turned so their GND pads face east under U2's exposed pad, Q3 and R15 turned, VCAP1 locked on F west of U2. Opus's relief 4 (C14's VBAT pad east) is reversed and the note says why.
8. **Folded table (§10.2)** regenerated for the final placement: every courtyard, ring, strip root and tab root in the shell frame with its margins against the v4 target body. Smallest courtyard margin 0.45 mm (J2 to the rib face). J2 clears the P5 standoff well by 4.81 mm in u (need 0.3). The P2 lid post lands on U1 by design.
9. **Design note** §2, §3.1, §4.6, §4.9, §5.4, §5.5, §7, §9, §10.1, §10.2, §11.1 updated to the true final state. §9.4 is the honest list: each open connection with its pads, the nearest copper of its net, the layer and the gap.

## What the next round should do (§9.4, cheapest first; none tried)

1. Locked pre-routes for the two common blockers, +3V0 (U4.1 over C8.1 to U2's supply pads on B, east of the corridor) and AFE_EN_HW (Q3.1 to a via just outside LAND_P1, then on F across the P1 landing to U1), then a fresh route through `v4_route_pf.py` and `hardware/board/v4_finish.sh`. About two hours of lane time; no guarantee.
2. Placement: R18/R20/R21 and R19 one row further east so U1's east pads get a second via column; Q1 turned so AFE_VIN's pin faces U4; C11 out from under U2. Then a fresh route.
3. 0.075 track/clearance in the two corridors only: needs JLC's confirmation first (their two-layer flex floor is 0.10/0.10, §3.2); no vendor contact was allowed here.
4. A third copper layer: certain, and it changes the stack-up and the thickness chain.

## Shell changes the board needs (no shell CAD edited; §7 has the numbers)

- **Rib slot for the P4/P5 flap:** cut the rib back 0.50 from the posterior wall over its full height: remove u 16.00–16.50 × s 14.90–15.70 × y 1.50–4.50.
- **P4/P5 wall sockets must go:** r9's hex sockets stand 2.08 proud of the wall face, where the v4 plate lies (u 16.19–16.50 × s 1.75–14.85 × y 1.695–6.895). Proposal: two floor-standing keying walls per standoff, u 13.19–16.19, s = site ± 2.80, 1.0 thick, y 1.50–4.30.
- **Closure at W18 is a redesign, not a move:** beside the Ø7.5 REF pocket (u 4.75–12.25) a Ø5.0 head well with 1.0 walls needs 7.0 of u and the tail is 18 wide (19.25 needed on the +u side). Either the well goes past the pocket into the tail loft or the closure becomes a latch.
- **Two lid posts** Ø2.0 at (5.90, 23.00), 1.98 long, and at (9.40, 32.10), 0.98 long onto U1.
- **LID_Y 7.1, cavity u 1.5–16.5.** r9's SIG fold pockets, REF slot, hinge and hook are used unchanged.

## For Rolf to decide

1. **Shell:** the five changes above. Nothing in the shell CAD was touched (ask a-3).
2. **Cell:** 501012 kept, T 8.1 (ask a-5).
3. **Parts without a JLC code:** Q2–Q4 (N-FET DFN1006-3, no part chosen), R18 47 kΩ and R19 27 kΩ 0201, C14 4.7 µF 0402 (codes UNVERIFIED). U1 ISP1807, U5 TPS7A0230 and J2 Molex 202656 say CONSIGNED in the BOM. Opus's part choices stand.
4. **RF:** about 13 mm of metal-free edge against the 18 the ISP1807 datasheet asks for; a range test is still owed.
5. **How to close the routing:** one of the four above. My pick is 1 then 2 in one round, same tools, before any rule or layer change.

## UNVERIFIED (also in §11.1)

- Part heights beyond U1, J2, SW1 and the TI outlines: package maxima.
- The coverlay window over U1's land and the two VSS vias.
- The REF strip's drop into the end-wall slot (v2 geometry).
- The P4/P5 keying walls and the closure: proposals by numbers, not built.
- The five footprints without a STEP model are placeholders in the STEP file.

## Lessons for the coordinator

- **GND has to be routed live.** Skipping it and pouring afterwards leaves 30-odd pieces the finisher cannot join at 0.10/0.10 on two layers. As one net it never converges; three regional nets was the best compromise, and it still leaves the pour under U2 and in the north-east corner cut off. Budget a placement round for GND, not a stitching pass.
- **The knots are structural, not router luck:** SOT-883 pinouts (pins 1 and 2 one side, 3 the other) force local crossings in the west stack; U1's east pads share one via column; the four SPI lines on F wall off U1's south-east. Six router variants (regional GND, all-after, rip-near, deep rip-up, soft fills) all end on the same six spots. A next lane should change the placement at those spots before running any router.
- **Costs:** one 80-round router run is about 25 minutes, the finishing sequence about 15; a lane can afford four or five full iterations. The first stitcher version ran over 10 minutes per call until it was vectorized.
- **Two latent blockers fixed on the way:** `release.py` counted paste-only pads as "pads without net" (it would have refused a routed board), and the board tests parsed the property format KiCad writes at `--save-board` wrongly. Both would have surfaced only on a routed board.
- **No web lane** was available this session; the Insight SiP question about internal VSS ties is answered by the two vias instead.
- Memory stayed fine with one router at a time and no Freerouting.

## Commits

- 5d1f881 board(v4): GND split, stitching, thermal-stub, pieces and finishing tools; NOT routed
- 234a681 board(v4): relief 5, VCAP1 pre-route, solid-pad rule; PCB at 0 DRC errors, 10 open; NOT routed
- 24e61f8 docs(board v4): §9 true state (0 DRC errors, 10 open, not routed), §10 tables

The branch is pushed (post-commit hook). Acceptance: (1) DRC 0 errors and 0 shorts after a refill, the starved-thermal rule decided and stated: met; 0 unconnected: not met (10). (2) `release.py --routed` exit 0: not met; the plain release wrote Gerbers, drill, BOM, CPL and STEP. (3) Design note §9 and §10 complete with the folded table, board tests pass: met.
