# WP8-prep report (lane w2)

Stage B path in the gauge script, with provisional inputs. No files under
`docs/fab/cad/v1/` or `docs/fab/cad/v2/`.

## What was built

- `scripts/cad/bte_fit_shell.py`: `MOCK_CONTACTS = false` now builds. It
  cuts CONTACT_HOLE Ø2.9 through the 1.5 mm wall, KEEPOUT_REF Ø7.5, WIRE_CHANNEL,
  CABLE_EXIT Ø2.0, and reserved-air TE 31428 tab envelopes (1.96 × 2.0, Ø7.1
  to 8.85). Order 1 (`MOCK_CONTACTS = true`) still uses the previous gauge
  builder, so the fifteen solids stay byte-identical.
- `PACKING = A | B | C` (default C). Pad coordinates and tab angles come from
  `placement.py` (`PADS_BY_OPTION` / `get_layout`). `placement.py` was not
  edited.
- Named Stage B checks: `CONTACT_HOLE_wall`, `KEEPOUT_SIGNAL_air`,
  `KEEPOUT_REF_air`, `TAB_envelope_air`, `BOARD_underside_clear`,
  `REF_WIRE_envelope`, `CABLE_EXIT_cavity`, `CELL_envelope`, `Q21_REF_lug`,
  `CLOSURE_PASSED`. Q21 records a fail with numbers and does not stop the
  write. The other named checks fail loudly with the number.
- `scripts/cad/params/stageb_provisional.toml`: PACKING C, MOCK_CONTACTS
  false, CLOSURE_PASSED false, plan §3.3 contact sites, TAB_HEIGHT 2.0. Header
  lists the open question for each value. `--out` of `v1/` or `v2/` is refused.
- Stage B manifest stays schema 1 and adds `stage`, `provisional`, `packing`,
  `closure_passed`, `contact_source`, `stage_b`. `scripts/cad/manifest.py`
  validates those keys when `stage` is `B`.
- README section "Stage B (provisional)" with the build command.
- Tests for the lifted guard, packing A/B/C, each named failing case, Q21
  numbers, CLOSURE_PASSED, v1/v2 refuse, and a two-process regen of the
  provisional build.

## Plan §9 / brief acceptance

| Item | Command | Result |
|---|---|---|
| Full suite | `.venv/bin/python -m unittest discover -s tests -v` | 111 tests, OK, 39.6 s |
| Order 1 solids and views vs main | compare `docs/fab/cad/v1/manifest.json` `files` and `views` to `main` | equal; `commit` `66b5564…` |
| Order 1 regen | `tests.test_cad.CadRegenTests` | OK |
| Provisional Stage B build | `.venv/bin/python scripts/cad/bte_fit_shell.py --params scripts/cad/params/stageb_provisional.toml --out <tmp> --parts body_full_p15,lid,coupon` | exit 0; Q21 fail `lug_top_y=8.23` vs `lid_y=8.0`, `barrel_outer=4.54` vs `pocket_r=3.75`; other named Stage B checks pass |
| Stage B regen | two fresh processes, same command | `files` maps equal |
| Manifest schema | validator on the Stage B temp manifest and on committed v1 | both OK |

## What was not done

- No order 2 solids under `docs/fab/cad/v2/`.
- Contact sites are still plan §3.3 defaults (WP7a).
- E1/E3/E5 stay off (`CLOSURE_PASSED = false`).
- No purchase, no upload.

## Needs a decision

- Q20 packing: this path defaults to C. A and B are switches. Rolf has not
  picked.
- Q21 reference lug: TE 31428 upright collides with the lid (8.23 vs 8.0)
  and the pocket wall (4.54 vs 3.75). The check reports it. It does not hide
  the lug.
- Q18 cell pack: the pocket check uses 5.2 × 10.4 × 15.6 with 0.5 mm foam on
  the lid face (clearances 0.3 / 0.4 / 0.4 mm). A real folded pack may not
  match.
- Closure test: `CLOSURE_PASSED` is a flag. This package does not decide it.
- Foam on all cell faces would not fit the 10.8 mm pocket in u (10.4 + 2×0.5).
  The check treats foam as the superior lid-face strip in plan §5.

## Final commit

`39a62d9f6f7aaa1c8e32902e5a55e3e8cdf17b6b`
