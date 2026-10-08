# Historical fit-shell reference

This is a reference for the original parametric fit shell, not a current fabrication or ordering plan. The v4 board is unfinished and unordered. The selected candidate is the [v4-snap shell](shell-v4.md).

## Geometry contract

The generator uses a body frame with `u` across the width, `s` along the curved path from the hook end and `y` through the thickness. Flat PCB coordinates use `(u, s)`. Reference anatomy values are examples, not Rolf's measurements.

`bte_fit_shell.py` contains the construction, parameter validation and geometry checks. `params/default.toml` defines the original reference. `params/shell_v4.toml` overlays the current nominal body. The construction includes the curved floor, walls, tail, hook, contact pockets, cell cavity and lid. Current folded board courtyards come from `board-v4-design.md` section 10.2.

The original fit studies considered full/thin bodies and two hook preloads. Their v1/v2 exports remain because the current generator and existing checks depend on those references. They are not alternate production candidates.

## Measurement and fit limits

M1 is the straight upper-to-lower ear-attachment distance. M2 is the crease arc. The remaining M parameters describe sulcus clearance, helix root, glasses, mastoid offset, concha position and helix rise. See the blank [measurement guide](measure.md). Store any completed guide or parameter overlay under ignored `measurements/`.

The `M1_gate` compares reference chord length with M1 plus a placement allowance. It does not model a person's skull or prove pressure, comfort, skin compatibility or electrical contact. A rendered shell is not a worn device.

The snap candidate needs a passive print, repeated latch checks, contact-position review and tolerance assessment. Powered wear must wait for qualified electrical review and bench validation. No fit, force, drop, fatigue or on-body recording result is available.

## Retired ordering path

The gauge-first order sequence, shopping sheets and empty public order ledger have been removed. Minimize order count and resolve the complete board, shell and parts design before payment. Historical planning prices are not current quotes.

Current constraints and blockers are in [plan-v2.md](plan-v2.md) and [open-questions.md](open-questions.md). Historical interface and packing tables remain in `interface.md`, `packing-v2.md` and `board-v2.md` to explain reference generator inputs.

## Regeneration

Follow [scripts/cad/README.md](../../scripts/cad/README.md). Use ignored `.reports/cad/` output rather than overwriting tracked exports. Reference checks do not certify manufacture or wear.
