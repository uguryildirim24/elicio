Rolf, **none of the three board changes is ready to order**. Four layers with the current part sites got closest (63 open connections, one clearance error, no shorts), but the battery plug still hits the charging-post well in the shell. The two-layer re-placement and the combined trial also failed. I recommend **four layers only as the next research starting point**, not as a purchase: its dollar premium was not available on JLC's public pricing page, it makes the flex thicker (0.11 → at least 0.20 mm), and no trial proves a narrower or thinner earpiece.

| Trial | Width | Body thickness | Added length | Routes? KiCad errors / unconnected / shorts | JLC price difference |
|---|---:|---:|---:|---|---|
| A: re-place SPI resistors; two layers | 22 mm | 9 mm retained | 0 | **No: 1 / 84 / 0** | Same layer process; actual bill UNVERIFIED |
| B: current sites; four layers + inner GND/power | 22 mm | 9 mm retained | 0 | **No: 1 / 63 / 0** | **UNVERIFIED** |
| C: A + four layers + inner GND/power | 22 mm | 9 mm retained | 0 | **No: 1 / 70 / 0** | **UNVERIFIED** |
| 20/18 mm outline screens for each option | 20 / 18 mm | 9 mm retained | 0 in screens | **Not routed:** placement shorts before routing | **UNVERIFIED** |

Commit **`ec7a09e455293f0378bf98cc7925e87fcff9e064`** adds `scripts/board/route_study.py` (reproducible, serial -Xmx4g Freerouting 2.4.1 / OpenJDK 25, KiCad DRC, five hand-fix groups, saved JSON/logs under `/tmp/t0004-*`) and `docs/fab/board-route-study.md` (full study, sources, all sites, warnings and limitations). Merged t-0002 (`1721eca`) and then main (`f5a8c4e`) without rebasing. No tracked board/packing/shell/safety rule changed. All trial boards are separate copies under `/tmp`, below 8 MB per folder. No upload, quote, vendor contact or purchase.

A/C swapped R5–R8 with R27–R30 (four SPI series parts moved to s=9.52–13.12 next to U2; shell contact/ring/hole/fold sites unchanged). The additional shell constraint forced J2 from (15.15,11.35) to (14.30,11.35): its AABB gap from P5's hex well went from **−4.93 mm to +0.30 mm**, but its mounting pad is **0.25 mm** from SIG2's Edge.Cuts, below the required **0.30 mm**. Moving it east 0.05 mm would again fail the shell gap. A/C's 1 error is that board-edge conflict. B retains original J2 and the **−4.93 mm shell clash**; its 1 error is a VBAT-via-to-GND-track distance of **0.9107 mm** inside an exposed Contact zone requiring 1.0000 mm. No shorts in the final 22-mm copies. A/C do not re-place R2/R3, which remain unreachable; this experiment does not prove that no alternative packing could route. The nominal B.Cu-face pocket stiffener also overlaps U2 even on the original board; the new resistors in A/C add overlaps. Physical stiffener approval is outstanding.

Final KiCad CLI output on routed/final-with-planes copies:

```text
A: Found 15 violations; Found 84 unconnected items. 1 error, 14 warnings, 0 shorts.
B: Found 13 violations; Found 63 unconnected items. 1 error, 12 warnings, 0 shorts.
C: Found 34 violations; Found 70 unconnected items. 1 error, 33 warnings, 0 shorts.
```

Four-layer boards use regular 0.55/0.30 mm through-vias. Filled inner GND/+3V0 island/pocket planes are kept out of the antenna, Contact strips, rings, folds and break-off tab. Planes were added after autorouting/hand repair and left isolated-copper warnings; hand A* searches only outer layers. This is a **bounded trial**, not a claim that four-layer hand routing cannot succeed. DRC input/output and failed hand candidates are recorded in the work folders and the study doc. Contact 220 kΩ paths, R7/G2, Q84/Q88/Q97 and JLC's copper-edge constraint stayed intact; none of the errors was waived.

Narrow-width necessary-condition screens on copies, **not claimed routed designs**: 20-mm A/C **37 errors / 142 unconnected / 5 shorts**, B **61 / 87 / 5**; 18-mm A/C **67 / 141 / 10**, B **136 / 88 / 24**. The 20/18 attempts slide the island/pocket edge and move charge rings, J2 and both holes with the wall but do **not** fully repack. They cannot be routed until their pad collisions are fixed. Minimum successful width is **unknown**. Area-only lower bounds: width 20 needs ≥2.79 mm extra island length (M1 ≥53.69 vs default 52); width 18 needs ≥6.40 mm (M1 ≥57.30). No smaller packages, removed parts or reduced shell height were tested. Four layers decrease second-side vertical air from about 3.31 to 3.22 mm and are less flexible, so there is no measured height saving.

JLC public pages read **2026-09-23**: https://jlcpcb.com/capabilities/flex-pcb-capabilities (2/4 layers, 0.11 mm two-layer vs ≥0.20 mm four-layer, regular vias); https://jlcpcb.com/pcb-fabrication/flexible-pcb (capabilities); https://jlcpcb.com/pcb-fabrication/flexible-pcb-pricing (live calculator did not return a public layer-specific amount), hence **2→4 price difference UNVERIFIED**. https://jlcpcb.com/help/article/fpc-extra-charges states extra fee for ≥4 stiffeners, but nine-piece fee **UNVERIFIED**; extreme small via prototype fee $16.29 does not apply to the regular vias tried. No quote or ordering action.

`.venv/bin/python -m unittest discover -s tests -q`: **271 OK, 60 CAD skips**; source PCB unchanged and worktree clean. Local post-commit hook attempted to push the lane branch to SSH origin and failed (`Permission denied (publickey)`); the commit is safe locally. No integration branch was pushed.
