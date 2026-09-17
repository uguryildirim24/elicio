# Packing options (WP6b)

Rolf: pick one row. Reply with the one line at the bottom.

Q13 (open-questions.md): each signal lug tab is 3 mm wide. It runs from the Ø7.1 edge to the far edge of its own pad. The mask adds 0.5 mm around it. Version of `docs/fab/interface.md` stays 2. Pads in interface §4 stay until you pick.

| | A. As is | B. Longer | C. Wider | E. Two-sided |
|---|---|---|---|---|
| Closes? | **No** | **Yes** | **Yes** | **No** |
| Free vs required 79.30 mm² | 82.97 (+3.66); sites do not fit | 104.84 (+25.54) | 137.05 (+57.75) | medial 82.97; lateral 29.51; arrays still fail |
| Conflicts (`layout_conflicts`) | BAV199S_1 no site; BAV199S_2 no site | none | none | BAV199S_1 no site; BAV199S_2 no site |
| VQFN-32 4.60² | (9.90, 22.55) | (9.90, 22.55) | (10.00, 18.90) | (9.90, 22.55) |
| Arrays (SIG1+SIG2, REF+spare) | none | (2.50, 32.15) and (2.65, 34.50); clamp 7.04 / 3.72 / 6.68 mm | (7.90, 26.70) and (9.25, 24.30); clamp 3.56 / 4.29 / 7.46 mm | none. Height would allow them (1.2 < 2.2). The lateral hole is 11.48 mm from SIG2 (limit 10) |
| 0402s placed | 16 of 25 | 17 of 25 | 25 of 25 | 22 of 25 |
| Pads (u, s), candidate | SIG1 (5.9, 26.6); SIG2 (5.5, 30.0); REF (4.0, 29.0) | same | same | same |
| Tab direction | CONTACT_1 → SIG1; CONTACT_2 → SIG2 | same | same | same |
| Tab length, Q13 | SIG1 1.55 mm; SIG2 2.75 mm (not 7) | same | same | same |
| Shell change | none | BODY_ARC 48.4 → 51.9; cavity 36.7 → 40.2; board 19×12.5 → 22.5×12.5 | BODY_WIDTH 17 → 20; cavity width 14 → 17; board 19×12.5 → 19×15.5 | none |
| TOTAL_CHORD | 47.90 | **51.43** | 47.90 | 47.90 |
| M1 gate (chord+3) | 50.90 | **54.43** | 50.90 | 50.90 |
| You give up | packing does not close | 3.5 mm of length behind the ear | 3 mm of width in the crease | a two-sided assembly; it still does not close |

Drawings: `docs/fab/cad/v1/placement_A.svg` (also `placement.svg`), `placement_B.svg`, `placement_C.svg`, `placement_E.svg`.

## Recommendation

Pick **C**.

A does not close. Free area is enough (82.97 vs 79.30). The VQFN-32 and the two arrays need the same 4.55 mm corridor. After the VQFN sits, no array is within 10 mm of its pads.

E does not close on this shell. The only lateral hole outside the module is the superior high-u strip. SIG2 is 11.48 mm from that hole. The 10 mm clamp rule fails. Array height 1.2 mm would fit under the lid (2.7 mm, or 2.2 mm under the foam strip). Review r2 said try E before a shell change. E was tried. It fails.

B closes. It adds 3.5 mm of body length. TOTAL_CHORD moves 47.90 → 51.43. The M1 gate moves 50.90 → 54.43. You give up length behind the ear. Only 17 of 25 of the 0402 courtyards sit (fragmentation, not area).

C closes. All named parts sit. All 25 of the 0402 courtyards sit. TOTAL_CHORD and the M1 gate do not move. You give up 3 mm of width in the crease. WP8 changes the shell after you pick.

Q14: cell to antenna zone is 16.70 mm on A/C/E and 20.20 mm on B. That passes ≥ 5 mm. Cell to reserved module body is 4.70 mm on A/C/E and 8.20 mm on B. That is not a packing fail.

## From

| Number | From |
|---|---|
| Required named 79.30 mm² | VQFN 4.60×4.60 = 21.16; two BAV199S-Q 2×2.65×2.35 = 12.46; BQ 2.10×1.40 = 2.94; LDO 1.50×1.50 = 2.25; 25×0402 25×1.80×0.90 = 40.50. RSM body max 4.10 (TI 4219108/B, code-r2.md). BAV199S-Q Fig. 8 occupied 2.65×2.35, two pairs, 20 July 2026. IPC-7351B Nominal 0.25 / small-chip 0.15 |
| Free A 82.97; literal 7 mm tabs 69.36; no tabs 101.53 | `placement.py` `budget("A")`. Q13 far-edge (not the r2 centre-end 86.97) |
| Free B 104.84; C 137.05; E lateral 29.51 | `budget("B"|"C"|"E")`; E punches the reserved module 15.8×10.5 off the lateral face |
| Conflicts | `layout_conflicts(option)`; empty on B and C |
| Pads | interface v2 §4; plan §3.3 with SIG1 s 26.6 (Q16) |
| Tab length SIG1 1.55, SIG2 2.75 | Ø7.1 edge to far pad edge: `hypot(pad, contact) + 0.5 − 3.55`. Width 3. Interface §3.1; Q13 |
| VQFN / array / 0402 sites | `placed_parts` / `place_0402s`; clamp ≤ 10 mm from L4 §5.1 / plan §4 |
| BODY_ARC 48.4, BODY_WIDTH 17.0, cavity 36.7×14.0 | plan §3.2, §5 |
| B: BODY_ARC 51.9, cavity 40.2, board 22.5×12.5 | interface §8.2 B; +3.5 on the inferior edge |
| C: BODY_WIDTH 20, cavity width 17, board 19×15.5 | interface §8.2 C; extra 3 mm on high-u |
| TOTAL_CHORD 47.90 / 51.43; M1 gate +3 | `chord_from_arc_bow(arc, bow=3.0)`, same as `bte_fit_shell.py`; plan §3.2 M1 ≥ chord+3 |
| Lateral height 2.7; under foam 2.2; array ≤ 1.2 | plan §5: lid 8.0 − board top 5.3; foam 0.5 over superior 3 mm; interface §6.4 |
| Antenna 12.4×3.8; module reserved 15.8 | Raytac Spec K p.9 and p.13 / p.7, issued 2022-07-01; plan §5 |
| Cell→antenna 16.70; cell→module 4.70 | Q14; `budget` hook packing. B moves the antenna with the board: 20.20 and 8.20 |
| SIG2 to E lateral hole 11.48 mm | array centre (11.27, 20.08) vs pad (5.5, 30.0) |

WP8 changes CAD solids and `manifest.json` only after you pick. This package does not.

## What you answer

Reply with one line: `I pick C` or `I pick B` or `I pick E` or `keep A; wait for the lug drawing`.
