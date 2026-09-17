# Packing options (WP6b)

Rolf: pick one row. Reply with the one line at the bottom.

Lug: TE 31428 (C-31428 rev D4, contacts.md §8.1, 2026-09-17). Tab 1.96 mm wide, **6.27 mm from the Ø7.1 edge**, plus 0.5 mm in the mask. Direction is a free angle. The wire, not the tab, reaches the pad. All signal tabs are **flat**. Upright does not fit (need 6.73 mm, have 2.63 mm). Reference stays upright in the tail pocket (contacts.md §5.3). Interface v2. Pads in §4 stay until you pick.

Q13 short tab (3 mm, SIG1 1.55 mm, SIG2 2.75 mm, end under the pad) is **not buildable with a crimp lug (WP5b)**. TE 31428 is the shortest (8.85 mm from centre). Panduit P22-4R is 10.61 mm. Nichifu R0.3-3 is 9.40 mm. That row is not a pick.

| | Q13 short | A. As is | B. Longer | C. Wider | E. Two-sided |
|---|---|---|---|---|---|
| Buildable with a crimp lug? | **No (WP5b)** | **Yes**, TE 31428, **flat** | **Yes**, flat | **Yes**, flat | **Yes**, flat |
| Closes? | **No** | **No** | **No** | **Yes** | **No** |
| Free vs required 79.30 mm² | 82.97; sites fail | 75.67 (−3.64) | 97.55 (+18.24); VQFN has no site | 124.13 (+44.83) | medial 75.67; lateral 26.38 |
| Conflicts | two arrays: no site | ADS1292_RSM: no site | ADS1292_RSM: no site | none | ADS1292_RSM: no site |
| VQFN-32 4.60² | (9.90, 22.55) | none | none | (10.85, 24.35) | none |
| Arrays (SIG1+SIG2, REF+spare) | none | (4.50, 27.10) and (2.65, 30.50); clamp 1.68 / 1.76 / 2.68 mm | same as A | same as A | same as A, medial. Height would allow arrays on the lateral face (1.2 < 2.2) |
| 0402s placed | 16 of 25 (Q13 mask) | 12 of 25 | 19 of 25 | 25 of 25 | 18 of 25 |
| Pads (u, s) | SIG1 (5.9, 26.6); SIG2 (5.5, 30.0); REF (4.0, 29.0) | same | same | same | same |
| Tab | 3 mm; Ø7.1 edge to far pad edge; toward the pad | 1.96 × 6.27 from Ø7.1; SIG1 25°; SIG2 290°; **flat** | same as A | 1.96 × 6.27 from Ø7.1; SIG1 5°; SIG2 255°; **flat** | same as A |
| Shell | none | none | BODY_ARC 48.4 → 51.9; board 19×12.5 → 22.5×12.5 | BODY_WIDTH 17 → 20; board 19×12.5 → 19×15.5 | none |
| TOTAL_CHORD | 47.90 | 47.90 | **51.43** | 47.90 | 47.90 |
| M1 gate | 50.90 | 50.90 | **54.43** | 50.90 | 50.90 |
| You give up | not a part you can buy | packing does not close | 3.5 mm behind the ear; still no VQFN site | 3 mm of width in the crease | a two-sided assembly; still no VQFN site |

Drawings: `docs/fab/cad/v1/placement_A.svg` (also `placement.svg`), `placement_B.svg`, `placement_C.svg`, `placement_E.svg`.

## Recommendation

Pick **C**.

A does not close. The 6.27 mm tab from the Ø7.1 edge is longer than the Q13 stub. On the plan shell, every legal angle pair leaves no VQFN-32 site. Free area is 75.67 mm², 3.64 mm² short of 79.30.

B does not close. The extra 3.5 mm is in the RF zone. TOTAL_CHORD moves 47.90 → 51.43. The VQFN still has no site.

E does not close. Array height 1.2 mm would fit under the lid (2.2 mm under the foam). The VQFN still has no medial site.

C closes. `layout_conflicts("C")` is empty. All named parts sit. All 25 of the 0402s sit. Tabs are flat: SIG1 at 5° (+u), SIG2 at 255°. TOTAL_CHORD does not move. You give up 3 mm of width in the crease.

Q14: cell to antenna zone is 16.70 mm on A/C/E and 20.20 mm on B. That passes ≥ 5 mm. Cell to reserved module body is 4.70 mm on A/C/E and 8.20 mm on B. That is not a packing fail.

## From

| Number | From |
|---|---|
| TE 31428 ring OD 5.16, barrel end 8.85 from centre, 6.27 from ring edge, width 1.96, stock 0.46 | C-31428 rev D4; contacts.md §8.1.1; date read 2026-09-17 |
| Packing tab 6.27 from the Ø7.1 edge (a0 3.55, a1 9.82) | WP6b second pass; `tab_span` mode `real` |
| Panduit P22-4R 10.61; Nichifu R0.3-3 9.40 from centre | contacts.md §8.1.2 |
| Overshoot SIG1 4.25, SIG2 3.05 if aimed at the pad | contacts.md §8.1.3 |
| Q13 SIG1 1.55, SIG2 2.75, width 3; **not buildable with a crimp lug (WP5b)** | Ø7.1 edge to far pad edge; Q13 |
| Angles A/B/E SIG1 25° SIG2 290°; C SIG1 5° SIG2 255°; all **flat** | `search_tab_degrees` / `TAB_DEG_BY_OPTION`; `legal_tab_degrees` |
| Upright SIG air 2.63; need 6.73 | Keep-out top 4.13; skin 1.5; stock 0.46 + barrel 6.27. REF: contacts.md §5.3 |
| Required named 79.30 mm² | VQFN 21.16; two BAV199S-Q 12.46; BQ 2.94; LDO 2.25; 25×0402 40.50. RSM 4.10 max (TI 4219108/B). BAV199S-Q Fig. 8, 20 July 2026. IPC-7351B |
| Free A 75.67; Q13 mask 82.97; C 124.13; B 97.55; E lateral 26.38 | `budget(option)` |
| Conflicts | `layout_conflicts`; empty only on C |
| Pads | interface v2 §4; SIG1 s 26.6 (Q16) |
| Sites / clamp ≤ 10 | `placed_parts` / `place_0402s`; L4 §5.1 / plan §4 |
| BODY_ARC 48.4, BODY_WIDTH 17; B +3.5; C +3 | plan §3.2, §5; interface §8.2 |
| TOTAL_CHORD 47.90 / 51.43; M1 +3 | `chord_from_arc_bow`; plan §3.2 |
| Lateral 2.7; under foam 2.2; array ≤ 1.2 | plan §5; interface §6.4 |
| Antenna 12.4×3.8; module 15.8 | Raytac Spec K p.9, p.13, p.7, 2022-07-01 |
| Cell→antenna 16.70; cell→module 4.70 | Q14; B: 20.20 and 8.20 |

WP8 changes CAD solids only after you pick.

## What you answer

Reply with one line: `I pick C` or `I pick B` or `I pick E` or `I pick A`.
