# WP6b report — third pass (TE 31428 a1 8.85 from centre)

Lane `w1`, branch `lane/w1`, package WP6b. Third pass: coordinator wording “6.27 from the Ø7.1 edge” was wrong. C-31428 rev D4 (contacts.md §8.1) puts 6.27 mm from the ring outer edge. Ring radius 2.58 mm. Barrel end **8.85 mm** from the contact centre (0.348 in). Ø7.1 already covers the ring (3.55 > 2.58). Tab beyond the keep-out is 8.85 − 3.55 = **5.30 mm**. Working span: a0 3.55, a1 8.85. Direction search, Q13 “not buildable” row, answer line, and untracked report stay from the second pass.

## What was built

- `tab_span` mode `real` returns `(KEEPOUT_R, LUG_A1)` = (3.55, 8.85). First relayout `2531ff0` had a1 8.85; this pass keeps that a1 and keeps a0 at the keep-out edge (3.55), not at RING_R.
- Direction search stays: `legal_tab_degrees` / `search_tab_degrees`. Tests assert 355°/170° and 0°/180° are legal, and search matches `TAB_DEG_BY_OPTION` for A and C.
- Signal tabs are **flat**. Upright does not fit (need 6.73 mm, have 2.63 mm). Reference stays upright in the tail pocket (contacts.md §5.3).
- Q13 short tab stays one sheet row, marked **not buildable with a crimp lug (WP5b)**. The answer line does not offer “wait for the lug drawing”.
- Option A: closes. Empty `layout_conflicts`. SIG1 355°, SIG2 170°, HIGH_U wire. VQFN (9.90, 23.15). Arrays (4.50, 27.10) and (7.15, 26.75). Clamp 1.68 / 1.76 / 4.60 mm. Free 83.23, spare 3.93. **10 of 25** 0402s have a medial site. The other 15 have no 1.80×0.90 courtyard on this board; they sit on C (27 sites).
- Option B: closes. SIG1 355°, SIG2 120°, INFERIOR wire. Arrays (4.50, 27.10) and (2.65, 30.50). TOTAL_CHORD 47.90 → 51.43. M1 50.90 → 54.43. **15 of 25** 0402s. The other 10 sit on C.
- Option C: closes. SIG1 0°, SIG2 180°, HIGH_U wire. **25 of 25** 0402s (max 27, 2 spare). TOTAL_CHORD unchanged. You give up 3 mm of width.
- Option E: closes. Same tabs/wire as A. ICs medial. **12 of 25** 0402s (10 medial + 2 lateral). The other 13 have no site. Lateral takes only 2 of A’s leftover 15.
- Drawings regenerated. `placement.svg` equals `placement_A.svg` (sha256 `044db94711e3fb3b32b5aa73c066ae98935ef7e3a04a72f40f6bd8167f7f7ca3`).
- Sheet recommends **A**. Pick C only if you need all 25 of the 0402 courtyards.
- `.reports/WP6b-report.md` is untracked (`.reports/` is gitignored).

CAD solids, `manifest.json`, `plan.md`, `open-questions.md`, `contacts.md`, and `montage.md` were not edited. Interface version stays 2. Pads in §4 stay.

## Plan §9 acceptance

WP6: "confirmed, or v2 with the escalation for Rolf".

| Item | Command | Result |
|---|---|---|
| Full suite | `.venv/bin/python -m unittest discover -s tests -v` | 93 tests OK |
| Drawings twice | `placement.py --option A\|B\|C\|E` then regen tests | A/B/C/E regenerate byte-identical |
| Escalation sheet | `docs/fab/packing-options.md` | Q13 not buildable (WP5b). A, B, C and E close. Recommend A. |

Packing is not confirmed until Rolf picks.

## What was not done

- No CAD solid change (WP8 after Rolf picks).
- Pads in interface §4 were not moved.
- Signal tabs were not bent upright.

## Needs a decision

Rolf picks from `docs/fab/packing-options.md`: `I pick C` or `I pick B` or `I pick E` or `I pick A`. Recommendation: **A**. Pick C only if you need all 25 of the 0402 courtyards.

## Final commit sha

`c6cbd45`
