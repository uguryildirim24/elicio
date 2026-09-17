# WP6b report — packing options under Q13

Lane `w1`, branch `lane/w1`, package WP6b.

## What was built

- `scripts/cad/placement.py --option A|B|C|E`. A is the default. It writes `docs/fab/cad/v1/placement.svg`. A also writes `placement_A.svg` (byte-identical). B, C and E write `placement_B.svg`, `placement_C.svg`, `placement_E.svg`.
- Q13 tab: width 3 mm, length from the Ø7.1 edge to the far edge of its own pad. The mask adds 0.5 mm. SIG1 length 1.55 mm. SIG2 length 2.75 mm.
- Q14: cell-to-module 4.70 mm is not a packing fail. The antenna-to-cell distance is 16.70 mm on A/C/E.
- Option A (plan shell): free 82.97 mm² vs required 79.30. Area closes. Sites do not. VQFN-32 and the two arrays share one 4.55 mm corridor. `layout_conflicts("A")` is `BAV199S_1: no legal site` and `BAV199S_2: no legal site`.
- Option B (BODY_ARC +3.5 mm): all named parts sit. Conflicts empty. TOTAL_CHORD 47.90 → 51.43. M1 gate 50.90 → 54.43. 0402s 17 of 25.
- Option C (BODY_WIDTH +3 mm): all named parts sit. All 25 of the 0402s sit. Conflicts empty. TOTAL_CHORD and M1 gate do not move.
- Option E (two-sided): array height 1.2 mm would fit (lid gap 2.7 mm; 2.2 mm under the foam strip). The only lateral hole outside the module is 11.48 mm from SIG2. Conflicts same as A.
- `docs/fab/packing-options.md`: one table, one recommendation (C), one answer line.
- `docs/fab/interface.md`: version stays 2. One errata row. §12 V2-4 points at the sheet. Pads in §4 stay.

CAD solids and `manifest.json` were not edited.

## Plan §9 acceptance

WP6: "confirmed, or v2 with the escalation for Rolf".

| Item | Command | Result |
|---|---|---|
| Full suite | `.venv/bin/python -m unittest discover -s tests -v` | 89 tests OK |
| Drawings twice | `placement.py --option A\|B\|C\|E --out …` then regen tests | A/B/C/E regenerate byte-identical. `placement.svg` equals `placement_A.svg` |
| Escalation sheet | `docs/fab/packing-options.md` | A does not close. B and C close. Recommend C. |

Packing is not confirmed. Interface v2 waits on Rolf.

## What was not done

- No CAD solid change (WP8 after Rolf picks).
- Pads in interface §4 were not moved.
- Option E was not closed by moving pads: a SIG2 move that reaches the lateral hole cuts the VQFN corridor with its tab.

## Needs a decision

Rolf picks from `docs/fab/packing-options.md`: `I pick C` or `I pick B` or `I pick E` or `keep A; wait for the lug drawing`. Recommendation: C.

## Final commit sha

`45d0016` (packing options). This report commit follows it.
