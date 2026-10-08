# Earpiece board route study — measured copies, **none orderable** (2026-09-23)

**Rolf: none of the three changes routes the board.** The best remaining connection count is 63 on four layers, but it still has a Contact-clearance error and the battery plug collides with the shell's charging-post well. Replacing parts on two layers leaves 84 connections open and a board-edge error even after moving that plug to clear the shell. Four layers are thicker flex, not a demonstrated thinner earpiece, and their price difference was not published on the public pricing page. Please do not order any of these copies.

| Option, actual copy | Width tried | Body thickness | Length change | KiCad DRC errors / unconnected / shorts after routing + hand fixes | Routes? | JLC fabrication price difference vs current 2-layer |
|---|---:|---:|---:|---|---|---|
| A: SPI re-placement, 2 copper layers | 22 mm | 9.0 mm retained | 0 | **1 / 84 / 0** | **No** | Same 2-layer process; actual bill **UNVERIFIED** |
| B: current placement, 4 copper layers, inner GND/+3V0 | 22 mm | 9.0 mm retained | 0 | **1 / 63 / 0** | **No** | **UNVERIFIED** (public page gives no layer-specific price) |
| C: A + 4 layers, inner GND/+3V0 | 22 mm | 9.0 mm retained | 0 | **1 / 70 / 0** | **No** | **UNVERIFIED** |
| 20 and 18 mm outline/courtyard screens for A/B/C | 20, 18 mm | 9.0 mm retained | 0 in screens; see area trade below | Fail with 37–136 errors and 5–24 pad shorts *before routing* | **Not routed**: placement invalid | **UNVERIFIED** |

**Recommendation:** Choose **B as the next routing research starting point only** (measured **1 DRC error / 63 unconnected / 0 shorts**), not as an order candidate: it retains shell sites on the PCB but the *existing* J2 site collides with P5's shell well. Before manufacture a new complete packing pass must move J2 **and** keep its pads clear of the SIG2 strip, place the Contact resistors by accessible strip roots, and give J3 and U2/charger escapes their own channels; then route and recheck the real shell. B's lower airwire count is **not** a working board and its additional layer price is unknown. No width or thickness has been demonstrated with all parts placed *and* all connections routed; the narrowest successful width is **unknown**, not 22 mm. The current 22 × 9 mm envelope is only a packaging reference.

## Trial contract and measurements

Base: `hardware/board/elicio-v2.kicad_pcb` from `1721eca` (identical board copper after merging `origin/main` at `f5a8c4e`), 2-layer/0.11 mm FPC, 22 mm body width, 9.0 mm shell, chord 47.90 mm, 0 DRC errors, 84 unconnected, 0 shorts. **No committed board, packing, shell, plan-v2 or open-questions file was changed.** Repro script `scripts/board/route_study.py` saves all PCBs/DSNs/SES/DRC JSON and router/hand logs under the specified outside-repo `--work` folder. Actual work folders: `/tmp/t0004-A`, `/tmp/t0004-B`, `/tmp/t0004-C` (each under 8 MB). These are ephemeral measurements, not release artifacts. Script retains locked Contact strips, removes stale copper for moved footprints in A/C, and retains existing DRC-clean copper for B. That difference means raw A-vs-B airwire counts are **not** an apples-to-apples layer-only experiment; compare success or failure, not relative route percentages.

A and C swap the *sites* of R5↔R27, R6↔R28, R7↔R29, R8↔R30 on B.Cu. The SPI series resistors formerly at (15.08,33.97), (15.08,35.17), (15.08,36.37), (15.68,23.37) move to (13.23,9.52), (13.23,10.72), (13.23,11.92), (13.23,13.12); the other four take the vacated sites. U2 stays at (14.85,4.45), as do its decouplers, under SW1 on the opposite face. R1–R3 retain their **220 kΩ** and original island sites: the strip approaches R2/R3 were *not* solved by this partial swap. H1/H2, five ring sites, J3 break-off neck, SIG/REF folds, and P4/P5 wall seats are unchanged. The *one* shell-related moved part is J2: (15.15,11.35) → **(14.30,11.35)**, 0.85 mm inward, same rotation. The shell's exact `V2_CAVITY_v3` axis-aligned courtyard-vs-P5-standoff-well calculation changes from **−4.93 mm** to **+0.30 mm** (P5 well centre (19.00,12.35), 3.00 × 5.30; J2 courtyard 5.80 × 6.56). This meets the new *shell AABB* threshold on the copy, **but not board DRC**: J2's west mounting pad reaches 0.25 mm from the SIG2 strip's Edge.Cuts, versus 0.30 required. Moving J2 0.05 mm back to the east closes that electrical gap but drops the shell AABB gap to 0.25 mm. The battery connector's access in the physical shell at this new pose has not been checked. Neither A nor C can be called valid. The swapped B.Cu resistors also overlap the pocket's nominal B.Cu-face FR4 stiffener rectangle (12.20–19.55 × 1.55–15.80); even the **original** B.Cu U2 is in that rectangle. Reconciling the **actual** stiffener face with lands and the folded shell needs a separate physical layout check in all three options. No safety net class, 7 × 7 mm exposed-land zone, strip other-net keep-out, or series resistor value was relaxed.

B uses *every original footprint and hole site* and all original two-layer tracks as a starting copy. Four copper layers were added at **0.20 mm minimum JLC listed finished FPC thickness**, retaining the source's regular 0.55/0.30 mm through-via, 0.10/0.10 mm Default trace/space and 0.15/0.20 mm Contact class. After routing/hand work, GND rectangles on In1.Cu and +3V0 rectangles on In2.Cu were filled on the pocket and island only: no foreign net plane enters the Contact strips, ring sites, folds, RF antenna no-copper zone or break-off tab. Plane filling did **not** reduce the 63 rats and produced two isolated-copper warnings (27 in C); the remaining error is a 0.9107 mm VBAT-via-to-GND-track clearance in the P4/P5 exposed zone (requires 1.0000). B also retains J2's **−4.93 mm shell collision**, so a lower rats count does not make it an order candidate. C receives the same filled inner layers; its 70 rats do not improve after fills. Plane areas were added **after** Freerouting plus hand fixes, not treated as constraints by Freerouting: this is an exploratory inner-plane check, *not* proof that the full power-distribution layout routes. GND and power connectivity, isolated islands, antenna no-copper region, coverlay, pad escapes and fabrication remain to be signed off.

All three copied boards used one Freerouting 2.4.1 process at a time on OpenJDK 25 (`-Xmx4g`, `-mp 20`, `-mt 4`, `--router.strict_drc=true`, automatic neckdown off, same `route_v2.py` flags), Specctra DSN export and SES import, then the existing `hand_route.py` groups `j3`, `vbus`, `j4`, `u2`, `stitch`, one at a time, each rejected candidate rolled back when its DRC error count rose. Hand A* works on the two *outer* layers even in B/C; it does not search inner-layer paths. The four-layer trials therefore do **not** exhaust the possible hand-routing options. All imported tracks <0.10 mm were raised to the 1 oz board minimum. Freerouting's cumulative allocation statistic is not resident memory (C's logged peak heap was 892 MB). No extreme vias were used.

| Copy | DRC before router (errors / unconnected / shorts) | After Freerouting import | After same five hand groups; after planes where relevant |
|---|---|---|---|
| A | 1 / 143 / 0 | 1 / 99 / 0 | **1 / 84 / 0** |
| B | 0 / 84 / 0 | 1 / 67 / 0 | **1 / 63 / 0**; planes 1 / 63 / 0 |
| C | 1 / 143 / 0 | 1 / 78 / 0 | **1 / 70 / 0**; planes 1 / 70 / 0 |

Final **KiCad CLI** output (the JSON is also in `/tmp/t0004-{A,B,C}/final-verify.json`):

```text
A  kicad-cli pcb drc --format json -o /tmp/t0004-A/final-verify.json /tmp/t0004-A/trial.kicad_pcb
   Found 15 violations
   Found 84 unconnected items
   1 error (copper_edge_clearance 0.25 < 0.30), 14 warnings, 0 shorts
B  kicad-cli pcb drc --format json -o /tmp/t0004-B/final-verify.json /tmp/t0004-B/with-planes.kicad_pcb
   Found 13 violations
   Found 63 unconnected items
   1 error (tail_pads clearance 0.9107 < 1.0), 12 warnings, 0 shorts
C  kicad-cli pcb drc --format json -o /tmp/t0004-C/final-verify.json /tmp/t0004-C/with-planes.kicad_pcb
   Found 34 violations
   Found 70 unconnected items
   1 error (copper_edge_clearance 0.25 < 0.30), 33 warnings, 0 shorts
```

These copies fail the release gate; **do not export/order production Gerbers**. Baseline 0 / 84 / 0 from t-0002 is also unrouted. A and C's extra 1 is the necessary connector move at the *old strip outline*, not a router-created short. B's 1 is a router copper error violating Contact zone creepage; no attempt was made to waive it.

## Narrow-body screens; thickness and length

The reproducible `--width-screen 20|18` takes *copies* for **each** option, slides the posterior island/pocket/charge outline inward 2 or 4 mm and moves J2, H1/H2 and the two charge rings with the wall. The SIG/REF ring and fold sites stay; J2 also moves left with P5 to keep its shell AABB gap at 0.30 mm. These are **necessary-condition geometry screens**, not optimized placement solutions, not shell CAD, and **not routing runs**: pad-to-pad shorts and holes/copper beyond Edge.Cuts cannot be fixed by an autorouter. B also retains its old copper; its screen scores include stale copper. On A/C only the locked Contact traces remain. All pads remain on the same electrical nets; there is no smaller-package substitution hidden in the results.

| Screen | 20 mm: errors / unconnected / shorts | 18 mm: errors / unconnected / shorts | First missing work |
|---|---|---|---|
| A, B.Cu SPI swap + J2 moved | **37 / 142 / 5** | **67 / 141 / 10** | Repack colliding pads/holes and restore clearance to moved edge |
| B, original placement + 4 layers | **61 / 87 / 5** | **136 / 88 / 24** | Repack before rerouting; inherited copper is stale |
| C, SPI swap + J2 moved + 4 layers | **37 / 142 / 5** | **67 / 141 / 10** | Same as A; more layers do not move copper pads |

This does not prove that a 20 or 18 mm design cannot exist. The older independent packing-grid search remains a reference tool. It is not evidence for the current board. No 18 mm complete placement has been established. Do not call any width routed on the basis of these screens.

**Area trade only, not a new body claim:** the present island is 17.50 × 21.60 mm; reducing width by 2 mm removes 43.2 mm², which needs **at least** 43.2/15.50 = 2.79 mm more island length to restore bare area. Reducing by 4 mm needs at least 86.4/13.50 = 6.40 mm. If all else were movable, the chord would become at least 50.69 or 54.30 mm; the `M1 ≥ chord + 3 mm` gate would require M1 ≥ 53.69 or 57.30 mm (default M1=52, existing 47.90 mm chord leaves only 1.10 mm length budget). These are area lower bounds, **not packing/routing results**: moving the cell, U1 antenna, tail well, tabs, standoffs and connector could cost more length. Each removed mm of width near 22 mm costs at least 21.60/17.50 ≈ **1.23 mm** island length (rises as the island gets narrower). Rolf must measure M1 before promising a longer part.

No body-thickness reduction is demonstrated. Four-layer flex changes un-stiffened board thickness **0.11 → ≥0.20 mm**, and JLC says four-layer flex is less bendable; if every other vertical clearance were fixed, second-side air falls from 3.31 to roughly 3.22 mm, not up. The 9.0 mm body, 3.0 mm contact standoffs, 5.6 mm cell/foam stack, lid, ribs, pocket and real printed solid must be recomputed together before changing the shell height. Swapping 0402s for JLC-assembled 0201s (Standard PCBA lists 0201; Economic 0402 minimum) or removing components could save area but this trial did neither. R1–R3's three 220 kΩ paths and Contact R7/G2 envelope cannot be traded away. R9/R10 and Q5 were already DNP. Removing J3 before programming or changing its electrical connection would require a new debug plan; no BOM or schematic reduction was tested.

## JLC evidence / cost to Rolf

Pages accessed **2026-09-23**, without a quote, upload, account, order or vendor contact:

- [JLC flex capabilities](https://jlcpcb.com/capabilities/flex-pcb-capabilities) lists 1/2/4 layers, finished 2-layer 25 µm dielectric at 0.11/0.12/0.2 mm, 4-layer FPC at 0.20/0.25/0.30/0.35/0.40/0.45 mm, regular vias 0.30/0.55 mm and extreme 4-layer 0.15/0.35 mm at **extra cost**; 1 oz 4/4 mil trace/spacing. Four-layer flexibility is substantially lower; static bends need verifying against the actual folded stack/stiffener positions. This page **does not give an assembly+fabrication quote or 2→4 layer dollar delta**.
- [JLC flexible PCB fabrication](https://jlcpcb.com/pcb-fabrication/flexible-pcb) advertises 1–4 layers but no readable price comparison for this specific outline/stackup. [JLC flex pricing](https://jlcpcb.com/pcb-fabrication/flexible-pcb-pricing) returned a shell requiring a live calculator; **2-vs-4 delta UNVERIFIED**. It would be dishonest to call 4 layers a known-price fix.
- [JLC FPC extra charges](https://jlcpcb.com/help/article/fpc-extra-charges) states a prototype fee for ≥4 stiffeners (the current nine-piece scheme remains nominally nine in all options); the amount for **these** nine pieces was not readable, **UNVERIFIED**. It states extreme small vias cost **$16.29 per prototype order**; these trials used regular 0.30/0.55 mm vias, not the extreme process. It separately lists **$8.14 per prototype order** if SMT parts require stiffeners applied after assembly; whether that applies here is **UNVERIFIED**. No vendor-approved stiffener layout, flex assembly fixture charge or price difference was obtained. A/C's resistor move changes stiffener conflicts, so do not assume identical assembly cost.

The `CONTACT` isolation and 220 kΩ inputs remain mandatory irrespective of price. A cheaper board with even one Contact violation is not an alternative. Current trials are *evidence of remaining engineering work*, not a promise that any option can be ordered once its one DRC error is fixed.

## Reproduce

```bash
uv venv --python 3.13 .venv
uv pip install --python .venv/bin/python -e .
KPY=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3
# Sequential: one router/KiCad batch at a time, Java -Xmx4g. Keep work OUTSIDE the repo.
"$KPY" scripts/board/route_study.py A --work /tmp/t0004-A
"$KPY" scripts/board/route_study.py B --work /tmp/t0004-B
"$KPY" scripts/board/route_study.py C --work /tmp/t0004-C
for opt in A B C; do
  for width in 20 18; do
    "$KPY" scripts/board/route_study.py "$opt" --width-screen "$width" --work "/tmp/t0004-$opt-w$width"
  done
done
.venv/bin/python -m unittest discover -s tests -q
```

DRC JSON: `before.json`, `router.json`, `after-{j3,vbus,j4,u2,stitch}.json`, and `planes.json` for B/C. The script saves a machine-readable `measure.json`, full Freerouting/hand logs and a separate `with-planes.kicad_pcb`; it never imports a SES into the tracked board. Measured base tests: **271 run, OK, 60 CAD tests skipped** in the base venv. `--resume-hand` / `--planes-only` can finish a stopped copy without rerunning Freerouting. This is a finite routing experiment, **not** a claimed impossibility proof or complete order-release check.
