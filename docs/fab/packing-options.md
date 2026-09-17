# Packing options (WP6b)

Rolf: pick one row. Reply with the one line at the bottom.

Lug: TE 31428 (C-31428 rev D4, contacts.md §8.1, 2026-09-17). Barrel end **8.85 mm** from the contact centre (0.348 in = ring radius 2.58 + 6.27 from the outer ring edge). The Ø7.1 keep-out already covers the ring (3.55 > 2.58), so the tab beyond the keep-out is **5.30 mm** (a0 3.55, a1 8.85), width 1.96 mm, plus 0.5 mm in the mask. Direction is a free angle. The wire, not the tab, reaches the pad. All signal tabs are **flat**. Upright does not fit (need 6.73 mm, have 2.63 mm). Reference stays upright in the tail pocket (contacts.md §5.3). Interface v2. Pads in §4 stay until you pick.

Q13 short tab (3 mm, SIG1 1.55 mm, SIG2 2.75 mm, end under the pad) is **not buildable with a crimp lug (WP5b)**. TE 31428 is the shortest. Panduit P22-4R is 10.61 mm from centre. Nichifu R0.3-3 is 9.40 mm. That row is not a pick.

| | Q13 short | A. As is | B. Longer | C. Wider | E. Two-sided |
|---|---|---|---|---|---|
| Buildable with a crimp lug? | **No (WP5b)** | **Yes**, TE 31428, **flat** | **Yes**, flat | **Yes**, flat | **Yes**, flat |
| Closes? | **No** | **Yes** | **Yes** | **Yes** | **Yes** |
| Free vs required 79.30 mm² | 82.97; sites fail | 83.23 (+3.93) | 106.93 (+27.62) | 130.18 (+50.87) | medial 83.23; lateral 19.50 |
| Conflicts | two arrays: no site | none | none | none | none |
| VQFN-32 4.60² | (9.90, 22.55) | (9.90, 23.15) | (9.90, 23.15) | (10.00, 23.50) | (9.90, 23.15) |
| Arrays (SIG1+SIG2, REF+spare) | none | (4.50, 27.10) and (7.15, 26.75); clamp 1.68 / 1.76 / 4.60 mm | (4.50, 27.10) and (2.65, 30.50); clamp 1.68 / 1.76 / 2.68 mm | same as A | same as A, medial. Height would allow arrays on the lateral face (1.2 < 2.2) |
| 0402s with a site | 16 of 25 (Q13 mask) | **10 of 25** medial. The other 15 have no 1.80×0.90 courtyard on this board. They sit on C (27 sites) | **15 of 25** medial. The other 10 have no site on the longer board. They sit on C | **25 of 25** medial (2 spare sites) | **12 of 25** (10 medial, 2 lateral). The other 13 have no site. Lateral takes only 2 of A's leftover 15 |
| Pads (u, s) | SIG1 (5.9, 26.6); SIG2 (5.5, 30.0); REF (4.0, 29.0) | same | same | same | same |
| Tab | 3 mm; Ø7.1 edge to far pad edge; toward the pad | a0 3.55 a1 8.85; SIG1 355°; SIG2 170°; **flat** | a0 3.55 a1 8.85; SIG1 355°; SIG2 120°; **flat** | a0 3.55 a1 8.85; SIG1 0°; SIG2 180°; **flat** | same as A |
| Shell | none | none | BODY_ARC 48.4 → 51.9; board 19×12.5 → 22.5×12.5 | BODY_WIDTH 17 → 20; board 19×12.5 → 19×15.5 | none |
| TOTAL_CHORD | 47.90 | 47.90 | **51.43** | 47.90 | 47.90 |
| M1 gate | 50.90 | 50.90 | **54.43** | 50.90 | 50.90 |
| You give up | not a part you can buy | 15 of 25 of the 0402 courtyards | 3.5 mm behind the ear; 10 of 25 of the 0402s | 3 mm of width in the crease | a two-sided assembly; 13 of 25 of the 0402s |

Drawings: `docs/fab/cad/v1/placement_A.svg` (also `placement.svg`), `placement_B.svg`, `placement_C.svg`, `placement_E.svg`.

## Recommendation

Pick **A**.

With a1 8.85 (C-31428 D4), the plan shell closes. `layout_conflicts("A")` is empty. Named parts sit. Tabs are flat: SIG1 at 355°, SIG2 at 170°. You do not give up length, width, or a second face.

Upright on SIG1 and SIG2 is not used. Keep-out air is 2.63 mm. The lug needs 6.73 mm. Reference stays upright in the tail pocket (contacts.md §5.3).

10 of 25 of the 0402 courtyards sit on A. The other 15 have no site on the 19×12.5 board (fragmentation, not area: spare 3.93 mm²). Pick **C** only if you need those 15 courtyards. C places 25 of 25. B places 15 of 25 and moves TOTAL_CHORD 47.90 → 51.43. E places 12 of 25 (two of them on the lateral face) and adds a two-sided process you do not need for the ICs.

Q14: cell to antenna zone is 16.70 mm on A/C/E and 20.20 mm on B. That passes ≥ 5 mm. Cell to reserved module body is 4.70 mm on A/C/E and 8.20 mm on B. That is not a packing fail.

## From

| Number | From |
|---|---|
| TE 31428 ring OD 5.16, radius 2.58, barrel end 8.85 from centre (0.348 in), 6.27 from outer ring edge, width 1.96, stock 0.46 | C-31428 rev D4; contacts.md §8.1.1; date read 2026-09-17 |
| Packing tab a0 3.55, a1 8.85; beyond keep-out 5.30 | 8.85 = 2.58 + 6.27; 5.30 = 8.85 − 3.55. `tab_span` mode `real` |
| Panduit P22-4R 10.61; Nichifu R0.3-3 9.40 from centre | contacts.md §8.1.2 |
| Overshoot SIG1 4.25, SIG2 3.05 if aimed at the pad | contacts.md §8.1.3 |
| Q13 SIG1 1.55, SIG2 2.75, width 3; **not buildable with a crimp lug (WP5b)** | Ø7.1 edge to far pad edge; Q13 |
| Angles A/E 355°/170°; B 355°/120°; C 0°/180°; all **flat** | `search_tab_degrees` / `TAB_DEG_BY_OPTION` |
| Upright SIG air 2.63; need 6.73 | Keep-out top 4.13; skin 1.5; stock 0.46 + barrel 6.27. REF: contacts.md §5.3 |
| Required named 79.30 mm² | VQFN 21.16; two BAV199S-Q 12.46; BQ 2.94; LDO 2.25; 25×0402 40.50. RSM 4.10 max (TI 4219108/B). BAV199S-Q Fig. 8, 20 July 2026. IPC-7351B |
| Free A 83.23; Q13 mask 82.97; B 106.93; C 130.18; E lateral 19.50 | `budget(option)` |
| 0402 sites A 10/10 max; B 15/15; C 25/27; E 12 (10+2) | `place_0402s`; leftover have no courtyard on that shell and sit on C |
| Conflicts | `layout_conflicts`; empty on A, B, C and E |
| Pads | interface v2 §4; SIG1 s 26.6 (Q16) |
| Sites / clamp ≤ 10 | `placed_parts`; L4 §5.1 / plan §4 |
| BODY_ARC 48.4, BODY_WIDTH 17; B +3.5; C +3 | plan §3.2, §5; interface §8.2 |
| TOTAL_CHORD 47.90 / 51.43; M1 +3 | `chord_from_arc_bow`; plan §3.2 |
| Lateral 2.7; under foam 2.2; array ≤ 1.2 | plan §5; interface §6.4 |
| Antenna 12.4×3.8; module 15.8 | Raytac Spec K p.9, p.13, p.7, 2022-07-01 |
| Cell→antenna 16.70; cell→module 4.70 | Q14; B: 20.20 and 8.20 |

WP8 changes CAD solids only after you pick.

## What you answer

Reply with one line: `I pick C` or `I pick B` or `I pick E` or `I pick A`.
