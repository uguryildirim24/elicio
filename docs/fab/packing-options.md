# Historical v1 packing options

These nominal calculations explain the retained v1 drawings and existing placement checks. They are not the current v4 flex-board design or purchasing advice. The current board is unfinished and unordered. No physical assembly was checked.

**Only C closes.** This is the historical reference search, not the v4 board. A, B and E leave the ADS1292 with no site once both signal lugs lie flat and their leads can leave the barrels.

| Option | Closes? | Shell change | You give up |
|---|---|---|---|
| A. As is | **No**: no VQFN site; 10 of 25 0402s placed | none | nothing, but it does not fit |
| B. Longer | **No**: no VQFN site; 14 of 25 0402s placed | BODY_ARC 48.4 → 51.9; M1 gate 50.90 → 54.43 | 3.5 mm behind the ear, and it still does not fit |
| C. Wider | **Yes**: all named parts, 25 of 25 0402s, no conflicts | BODY_WIDTH 17 → 20; board 19 × 12.5 → 19 × 15.5 | 3 mm of width in the crease |
| E. Two-sided | **No**: no VQFN site (arrays and 8 0402s go lateral) | none | a two-sided build, and it still does not fit |

The short Q13 tab (ends under its pad) is **not a row**: it is not buildable with a crimp lug (WP5b). The shortest lug read, TE 31428 (historical C-31428 drawing, source pointer in references.md), reaches 8.85 mm from the contact centre.

## Reference search result

**C** is the only option where this calculation finds a site for every part with the retained lug envelope.

- The lug is TE 31428, flat, barrel end 8.85 mm from the contact centre, 1.96 wide, plus 0.5 in the copper mask.
- Each lead leaves its barrel straight and bends at 3 mm (plan §3.3). That rules out any barrel aimed at a wall. WP6b's first sheet had them aimed at walls (SIG2 ended 0.13 mm from the side wall), which is why it said A closes.
- On the plan's 17 mm body, both barrels must point into the middle of the board. They cut two 3 mm strips through it, and the 4.6 mm VQFN courtyard no longer fits anywhere (A free 72.18 mm² against 79.30 needed). B's extra length adds area at the wrong end (free 93.72, still no 4.6 × 4.6 hole). E moves the arrays and passives to the lateral face but the VQFN stays medial.
- C's extra 3 mm of width gives the VQFN a site beside the SIG2 barrel.

What C needs from you besides the width:

1. **The lead pads move** from interface v2 §4 (Q13 said the pads move if the tab is long). New pads: SIG1 (7.5, 29.35), SIG2 (13.5, 21.35), REF (5.5, 29.35).
2. **The reference wire crosses the SIG1 lead once**, on the floor near (3.9, 33.7), where no part or pad sits above. Two Ø1.3 wires stack to 2.6 mm under a board 2.8 mm above the floor. The plan does not forbid a crossing; this is the reading. Without it, C needs a 2 mm lead bend instead of 3.

## C in numbers

| Item | Value | From |
|---|---|---|
| Free medial area vs required | 126.26 vs 79.30 mm² | `budget("C")` |
| Tabs | SIG1 110°, SIG2 270° (0° = +u, 90° = +s), flat | `search_tab_degrees("C")` |
| Lead exit clearance | SIG1 0.54, SIG2 0.63 mm | `lead_exit_gap` |
| VQFN-32 (4.60²) | (11.90, 21.85) | `placed_parts("C")` |
| Arrays | SIG1+SIG2 at (5.85, 26.50); REF+spare at (11.90, 27.00) | `placed_parts("C")`, `ARRAY_LINES` |
| Clamp distances (≤ 10) | SIG1 1.71, SIG2 8.94, REF 7.81 mm | `clamp_distance`; plan §4 |
| Charger, LDO | BQ25100 (10.25, 20.45); TLV713 (10.40, 22.25) | `placed_parts("C")` |
| Reference route | channel → wrap s 37 → (5.0, 34.6) → REF pad; clears keep-out 2 by 0.09 | `wire_keepout_gap`, `wire_floor_gap` |
| TOTAL_CHORD, M1 gate | 47.90, 50.90 (unchanged) | `chord_from_arc_bow`; plan §3.2 |
| Cell to antenna zone, to module body | 16.70, 4.70 mm (Q14: passes) | `budget`; interface §6.3 |
| Conflicts | none | `layout_conflicts("C")` |

## Why the others fail

| Option | Tabs | Free vs 79.30 | What is missing |
|---|---|---|---|
| A | SIG1 110°, SIG2 270° | 72.18 | VQFN; 15 of 25 0402s have no site |
| B | SIG1 90°, SIG2 295° | 93.72 | VQFN (no 4.6 × 4.6 hole); 11 of 25 0402s have no site |
| E | SIG1 110°, SIG2 270° | medial 72.18, lateral 53.40 | VQFN |

The search also tried A, B and E with a 2 mm lead bend. None placed the VQFN. The search steps tab angles by 5°, puts each pad nearest its lead's bend and tries four reference routes, so "no site" means the search found none, not a proof.

Drawings: `docs/fab/cad/v1/placement_C.svg`, `placement_A.svg` (also `placement.svg`), `placement_B.svg`, `placement_E.svg`. Each lists its conflicts.

## From

| Number | From |
|---|---|
| TE 31428 barrel end 8.85 from centre (drawing 8.788 max, so 0.06 conservative), 6.27 past the ring edge, width 1.96 max | C-31428 rev D4; references.md |
| Lead Ø1.3, bend radius 3 | plan §3.3 script checks and WIRE_CHANNEL route; `LEAD_BEND_R` |
| Required 79.30 mm² | VQFN 21.16 (RSM 4.10 max, TI 4219108/B); two BAV199S-Q 12.46 (Fig. 8); BQ 2.94; LDO 2.25; 25 × 0402 40.50 (IPC-7351B) |
| Board 19 × 12.5 at y 4.3, parts ≤ 1.2 tall | plan §5 |
| B +3.5 length, C +3 width | plan §10 interface decision 1; interface §8.2 |
| Lateral face (E): module 15.8 × 10.8, RF zone, rim; height lid 8.0 − board top 5.3 = 2.7, 2.2 under the 0.5 foam strip | plan §5 lateral row and battery-pocket row; Raytac Spec K p.7, p.9, p.13; `LATERAL_H`, `LATERAL_H_FOAM` |

The historical selection reply was `I pick C`. That reply is not approval to fabricate the current board. The original selection dialogue is retired. The current candidate and its limits are in `board-v4-design.md` and `shell-v4.md`.
