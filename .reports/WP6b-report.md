# WP6b report — packing options on the TE 31428 lug

Lane `w1`, branch `lane/w1`, package WP6b. Mid-package update after WP5b `f5ae1e4` on `lane/w5`.

## What was built

- `scripts/cad/placement.py --option A|B|C|E`. Working tabs are TE 31428 (C-31428 rev D4): width 1.96 mm, 6.27 mm from the ring edge (8.85 mm from the centre). SIG1 at 0° (+u). SIG2 at 180° (−u). Both **flat**. The Q13 short-tab mask stays as `mode="q13"` for budget and tests only.
- Upright on SIG1 and SIG2 does not fit: keep-out air 2.63 mm, lug 6.73 mm. Reference stays upright in the tail pocket (contacts.md §5.3).
- Option A (plan shell): `layout_conflicts("A")` is empty. VQFN-32 at (9.90, 23.50). Arrays at (4.50, 27.10) and (7.15, 26.75). Clamp 1.68 / 1.76 / 4.60 mm. Free 79.32 mm² vs required 79.30. 0402s 7 of 25.
- Option B: empty conflicts. TOTAL_CHORD 47.90 → 51.43. M1 gate 50.90 → 54.43. 0402s 11 of 25.
- Option C: empty conflicts. All 25 of the 0402s sit. TOTAL_CHORD and M1 gate do not move.
- Option E: empty conflicts. ICs sit on the medial face. Two extra 0402s on the lateral face. Two-sided assembly is not required for the named pack.
- Q13 short tab (3 mm, far pad edge) is kept as one sheet row, marked **not a SKU**. No crimp lug ends under its pad (overshoot SIG1 4.25 mm, SIG2 3.05 mm).
- `docs/fab/packing-options.md`: Q13 row plus A/B/C/E on the real lug. Recommendation **A**.
- `docs/fab/interface.md`: version stays 2. Second WP6b errata row. §12 V2-4 points at the sheet. Pads in §4 stay.
- Drawings: `placement.svg` = `placement_A.svg`, plus B, C, E.

CAD solids and `manifest.json` were not edited. `plan.md`, `open-questions.md`, `contacts.md`, and `montage.md` were not edited.

## Plan §9 acceptance

WP6: "confirmed, or v2 with the escalation for Rolf".

| Item | Command | Result |
|---|---|---|
| Full suite | `.venv/bin/python -m unittest discover -s tests -v` | 92 tests OK |
| Drawings twice | `placement.py --option A\|B\|C\|E --out …` then regen tests | A/B/C/E regenerate byte-identical. `placement.svg` equals `placement_A.svg` |
| Escalation sheet | `docs/fab/packing-options.md` | Q13 is not a SKU. A, B, C and E close on TE 31428. Recommend A. |

Packing is not confirmed until Rolf picks. Interface v2 waits on Rolf.

## What was not done

- No CAD solid change (WP8 after Rolf picks).
- Pads in interface §4 were not moved.
- Signal tabs were not bent upright (height does not allow it).

## Needs a decision

Rolf picks from `docs/fab/packing-options.md`: `I pick A` or `I pick C` or `I pick B` or `I pick E`. Recommendation: **A**. Pick C only if you need all 25 of the 0402 courtyards.

## Final commit sha

Packing work on `lane/w1` HEAD after this file is committed.
