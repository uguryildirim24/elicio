# Assembly readiness

The v4 board is unfinished and unordered. No assembled device exists. The former v2 step-by-step assembly and Feather flash instructions are superseded and have been removed.

The current candidate combines the v4 flex board, a fitted protected cell, titanium contact hardware and the v4-snap shell. It is not a qualified kit. Do not substitute parts or assume final assembly needs only the modeled steps.

## Before a real assembly

- Resolve the electrical, fabrication and supply gates in [open questions](open-questions.md).
- Implement and verify the ISP1807 product Arduino variant and first-load voltage levels. The Feather variant is not the product pinout.
- Inspect a passive shell print. Verify repeated closure, key access, contact installation and lid-post loads.
- Review the actual cell pack, polarity, connector, insulation, charging limits and off-ear-only arrangement.
- Re-run the board release checks after any design change. A historical DRC count is not safety approval.

No on-body assembly, charge procedure or wear result is validated here. Rolf's requirement for limited final assembly remains a design constraint, not a measured completion-time claim.

Use [board v4](board-v4-design.md), [shell v4](shell-v4.md) and [firmware status](firmware-v2.md) as the current references. Keep future purchase and assembly records in ignored local directories. Do not publish payment or delivery information.
