# WP6 report — Packing proof and interface v2

Lane `w1`, branch `lane/w1`, worktree
`/home/user/projects/elicio/.worktrees/w1`. Package `WP6`.
Plan commit `0c5d0eb`. Interpreter: Python 3.13.15 (`.venv`).
`cad` extra now includes matplotlib (3.10.8 in this venv).

## What was built

1. `docs/fab/interface.md` version 2, with a change-log row. v1 numbers
   that did not change are kept. New numbers have a From cell.
2. `scripts/cad/placement.py`: headless matplotlib, Agg, deterministic
   SVG in the body-frame `(u, s)` plane. Coupon-to-parameter mapping is
   in this docstring, in `bte_fit_shell.py`, and in `scripts/cad/README.md`.
3. `docs/fab/cad/v1/placement.svg`, courtyards at maximum dimensions.
4. `tests/test_placement.py`: packing maths plus byte-identical regen.
5. `pyproject.toml` `cad` extra: `matplotlib>=3.9`.
6. `tests/test_cad.py` allows `placement.svg` next to the gauge files.

No CAD solid and no `manifest.json` was edited. No purchase, quote, or
vendor contact.

## Plan §9 acceptance (WP6)

Acceptance: confirmed, or v2 with the escalation for Rolf; placement at
max dims; cell named; RF zone; lead pads.

| Item | Result | How verified |
|---|---|---|
| Confirmed or escalation | **Confirmed with a named non-shell change.** ADS1292 VQFN-32 (RSM) and one BAV199S-Q array. Free 101.53 mm², required 72.17, spare 29.36. TQFP-32 does not fit (largest empty rectangle 4.55 × 10.20). Options B (+3.5 mm length) and C (+3 mm width) are not needed for packing; the numbers each buys are in interface §8.2 | `placement.py` raster and `tests.test_placement.PlacementMathTests` |
| Placement at max dims | `docs/fab/cad/v1/placement.svg` | Regen test, hash below |
| Cell named | DNK 501015 from the fpbattery drawing (page 2, cell art 2022-12-10). **No published folded pack fits 5.2 × 10.4 × 15.6.** In-line BL 17 ± 1. WP8 pocket length 16.0 → 18.4 along s if that pack is kept | Datasheet URL and date in interface §5 and §11 |
| RF zone | 12.4 × 3.8 mm no-copper at the inferior board edge, Spec K pages 9 and 13, issued 2022-07-01. Overlaps keep-out 2. Battery gap 5.00 mm with the cell packed to the hook; 4.60 mm if the cell sits on the rib | Spec K; `budget().rf_keepout2_overlap` True |
| Lead pads | Frozen (5.9, 26.6), (5.5, 30.0), (4.0, 29.0). SIG1 moved +0.1 mm in s. All outside keep-outs + 0.5 and outside the antenna. Clamp distances 1.69–1.73 mm. Reference route drawn Ø1.3, 3 mm bend, Kapton wrap at s 37 | `pad_keepout_gap`, `clamp_distance`, drawing |

## Gates

### Unit tests

```
.venv/bin/python -m unittest discover -s tests -v
```

Result: 76 tests, OK, 10.407 s. Python 3.13.15. Includes 9 placement
tests. CAD regen still matches committed gauge hashes.

### Drawing regen

```
.venv/bin/python scripts/cad/placement.py --out docs/fab/cad/v1/placement.svg
```

SHA-256 `3ca2268c0d0696b000045b8d9b05e04504ba06e3a8c6f74c8fe1643ad8f73aa9`.
Two writes in one process and a write to a temp dir match this hash
(`PlacementRegenTests`).

## What was not done

- No gauge CAD change (forbidden). The +2.4 mm pocket, if chosen, is WP8.
- Q6 nut metal: recorded in interface §12 V2-3, not decided.
- Q11: lid-underside constraint written; WP8 builds 0.4 mm or moves the
  emboss over the battery zone.
- No layout (traces, planes). This is courtyards only.
- Spec L PDF from raytac.com returned HTTP 403; Spec K (same keep-out
  drawing, issued 2022-07-01) was used.

## Needs a decision

1. **Cell pack (interface decision 2).** No SKU on a dated page shows a
   folded pack ≤ 5.2 × 10.4 × 15.6. Pick: (a) WP8 lengthens the pocket
   to 18.4 mm along s for the published DNK in-line pack, or (b) wait
   for a drawing that shows a fold inside the present envelope. Do not
   buy on a custom fold with no drawing.
2. **Packing (plan §10 Open for Rolf item 6).** Closed as option D plus
   the array. Rolf does not need to pick +3.5 mm length or +3 mm width
   for area. Those options still do not fit TQFP-32 at Nominal
   courtyards (empty width 4.55 mm; +3 mm width gives ~7.55 vs 7.60).
3. **Q6 nut metal.** Still Rolf's. Candidates in §12 V2-3. Not a WP6
   decision.
4. **Q11 emboss.** WP8: 0.4 mm over the board, or move the string over
   the battery zone.

## Plan vs brief

The plan wins. The brief asked for a 501015 SKU whose folded pack fits
the envelope. The plan's envelope is unchanged. No such published SKU
was found; that is written in interface v2 rather than silent CAD.

## Final commit

Recorded after the last commit on `lane/w1`.
