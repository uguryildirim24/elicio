# Packing options (WP6b)

Rolf: pick one row. Reply with the one line at the bottom.

The lug is TE 31428 (Customer Drawing C-31428 rev D4, contacts.md §8.1, date 2026-09-17). Barrel 1.96 mm wide, 6.27 mm from the ring edge (8.85 mm from the ring centre). The mask adds 0.5 mm. Direction is free: SIG1 at 0° (+u), SIG2 at 180° (−u). Both are **flat**. Upright does not fit in the signal keep-out (need 6.73 mm, have 2.63 mm). Reference stays upright in the tail pocket (contacts.md §5.3). Version of `docs/fab/interface.md` stays 2. Pads in interface §4 stay until you pick.

Q13 short tab (3 mm, end under its own pad) is **not a SKU**. No crimp ring lug ends under its pad. TE 31428 overshoots SIG1 by 4.25 mm and SIG2 by 3.05 mm if the barrel points at the pad. That row is the reading Q13 asked about. It is not a pick.

| | Q13 short (not a SKU) | A. As is | B. Longer | C. Wider | E. Two-sided |
|---|---|---|---|---|---|
| Buildable with a crimp lug? | **No** | **Yes** (TE 31428, flat) | **Yes** | **Yes** | **Yes** |
| Closes? | **No** | **Yes** | **Yes** | **Yes** | **Yes** |
| Free vs required 79.30 mm² | 82.97 (+3.66); sites do not fit | 79.32 (+0.01) | 98.09 (+18.78) | 130.18 (+50.87) | medial 79.32; lateral 20.69 |
| Conflicts (`layout_conflicts`) | BAV199S_1 no site; BAV199S_2 no site | none | none | none | none |
| VQFN-32 4.60² | (9.90, 22.55) | (9.90, 23.50) | (9.90, 23.50) | (10.00, 23.50) | (9.90, 23.50) |
| Arrays (SIG1+SIG2, REF+spare) | none | (4.50, 27.10) and (7.15, 26.75); clamp 1.68 / 1.76 / 4.60 mm | same as A | same as A | same as A, all medial. Height would allow arrays on the lateral face (1.2 < 2.2). They are not needed |
| 0402s placed | 16 of 25 (on the Q13 mask) | 7 of 25 | 11 of 25 | 25 of 25 | 9 of 25 (7 medial, 2 lateral) |
| Pads (u, s), candidate | SIG1 (5.9, 26.6); SIG2 (5.5, 30.0); REF (4.0, 29.0) | same | same | same | same |
| Tab | 3 mm wide; Ø7.1 edge to far pad edge; toward the pad | 1.96 mm wide; 6.27 mm from the ring edge; SIG1 0° (+u); SIG2 180° (−u); **flat** | same as A | same as A | same as A |
| Shell change | none | none | BODY_ARC 48.4 → 51.9; cavity 36.7 → 40.2; board 19×12.5 → 22.5×12.5 | BODY_WIDTH 17 → 20; cavity width 14 → 17; board 19×12.5 → 19×15.5 | none |
| TOTAL_CHORD | 47.90 | 47.90 | **51.43** | 47.90 | 47.90 |
| M1 gate (chord+3) | 50.90 | 50.90 | **54.43** | 50.90 | 50.90 |
| You give up | not a part you can buy | packing closes on the plan shell; only 7 of 25 of the 0402 courtyards sit | 3.5 mm of length behind the ear | 3 mm of width in the crease; all 25 of the 0402s sit | a two-sided assembly; the ICs already sit on the medial face |

Drawings: `docs/fab/cad/v1/placement_A.svg` (also `placement.svg`), `placement_B.svg`, `placement_C.svg`, `placement_E.svg`.

## Recommendation

Pick **A**.

The real lug is narrower than the Q13 3 mm strip (1.96 mm) and it does not have to point at its pad. SIG1 points +u. SIG2 points −u. The VQFN-32 and both arrays sit. `layout_conflicts("A")` is empty. You do not give up length, width, or a second face.

Upright on SIG1 and SIG2 is not used. Keep-out air is 4.13 − 1.5 = 2.63 mm. The lug needs 0.46 + 6.27 = 6.73 mm. The board underside at 4.3 mm is still short. Reference stays upright in the tail pocket (contacts.md §5.3).

Only 7 of 25 of the 0402 courtyards sit on A (fragmentation, not area: spare 0.01 mm²). C places all 25. Pick C only if you need those courtyards. B moves TOTAL_CHORD 47.90 → 51.43 and the M1 gate 50.90 → 54.43. E adds two 0402s on the lateral face and a two-sided process you do not need.

Q14: cell to antenna zone is 16.70 mm on A/C/E and 20.20 mm on B. That passes ≥ 5 mm. Cell to reserved module body is 4.70 mm on A/C/E and 8.20 mm on B. That is not a packing fail.

## From

| Number | From |
|---|---|
| TE 31428 ring OD 5.16, radius 2.58, barrel end 8.85, edge-to-end 6.27, width 1.96, stock 0.46 | TE Customer Drawing C-31428 rev D4; contacts.md §8.1.1; URL on that page; date read 2026-09-17 |
| Panduit P22-4R 10.61 from centre; Nichifu R0.3-3 9.40 from centre | contacts.md §8.1.2, same date |
| Overshoot SIG1 4.25, SIG2 3.05; no SKU ends under its pad | contacts.md §8.1.3 (pad centres 4.60 and 5.80) |
| Q13 length SIG1 1.55, SIG2 2.75; width 3 | Ø7.1 edge to far pad edge: `hypot(pad, contact) + 0.5 − 3.55`. Interface §3.1; Q13. **Not a SKU** |
| Tab angles SIG1 0° (+u), SIG2 180° (−u), flat | `placement.py` `TAB_DEG`; metal in the cavity; 0.5 mm from other pads and the other barrel |
| Upright SIG air 2.63; need 6.73; short 4.10 | Keep-out top 4.13 (plan §3.3); skin 1.5; stock 0.46 + barrel 6.27. REF upright: contacts.md §5.3, Ø7.5 × 6.5 pocket, 6.0 mm tall envelope |
| Required named 79.30 mm² | VQFN 4.60×4.60 = 21.16; two BAV199S-Q 2×2.65×2.35 = 12.46; BQ 2.10×1.40 = 2.94; LDO 1.50×1.50 = 2.25; 25×0402 25×1.80×0.90 = 40.50. RSM body max 4.10 (TI 4219108/B, code-r2.md). BAV199S-Q Fig. 8 occupied 2.65×2.35, two pairs, 20 July 2026. IPC-7351B Nominal 0.25 / small-chip 0.15 |
| Free A 79.32; Q13 mask 82.97; 7 mm tabs 69.36; no tabs 101.53 | `placement.py` `budget("A")`. Working mask is TE 31428 |
| Free B 98.09; C 130.18; E lateral 20.69 | `budget("B"|"C"|"E")`; E punches the reserved module 15.8×10.5 off the lateral face |
| Conflicts | `layout_conflicts(option)`; empty on A, B, C and E with the real lug |
| Pads | interface v2 §4; plan §3.3 with SIG1 s 26.6 (Q16) |
| VQFN / array / 0402 sites | `placed_parts` / `place_0402s`; clamp ≤ 10 mm from L4 §5.1 / plan §4 |
| BODY_ARC 48.4, BODY_WIDTH 17.0, cavity 36.7×14.0 | plan §3.2, §5 |
| B: BODY_ARC 51.9, cavity 40.2, board 22.5×12.5 | interface §8.2 B; +3.5 on the inferior edge |
| C: BODY_WIDTH 20, cavity width 17, board 19×15.5 | interface §8.2 C; extra 3 mm on high-u |
| TOTAL_CHORD 47.90 / 51.43; M1 gate +3 | `chord_from_arc_bow(arc, bow=3.0)`, same as `bte_fit_shell.py`; plan §3.2 M1 ≥ chord+3 |
| Lateral height 2.7; under foam 2.2; array ≤ 1.2 | plan §5: lid 8.0 − board top 5.3; foam 0.5 over superior 3 mm; interface §6.4 |
| Antenna 12.4×3.8; module reserved 15.8 | Raytac Spec K p.9 and p.13 / p.7, issued 2022-07-01; plan §5 |
| Cell→antenna 16.70; cell→module 4.70 | Q14; `budget` hook packing. B moves the antenna with the board: 20.20 and 8.20 |
| Reference wire | pocket → channel → wrap at s 37 → inferior of K2 → high-u → s 26.4 → REF. Candidate in `placement.py`; interface §4 is not edited |

WP8 changes CAD solids and `manifest.json` only after you pick. This package does not.

## What you answer

Reply with one line: `I pick A` or `I pick C` or `I pick B` or `I pick E`.
