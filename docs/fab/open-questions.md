# Hardware decisions and open gates

The current candidate is the v4 flex board and v4-snap shell. The board is unfinished and unordered. No physical fit, electrical safety, live acquisition or RF result exists.

## Retained engineering decisions

These decisions replace private workflow records. IDs remain so reference tables can identify their constraints.

| ID | Decision |
| --- | --- |
| Q57 | Keep 0.5 mm foam under the reference cell envelope. |
| Q58 | The reference interface-II clamp uses ring pad, standoff and board without an intermediate nut. |
| Q59 | The REF flex root needs an end-wall slot. A nominal box check is not proof of bend or print fit. |
| Q69 | Require a fitted protected pack and verified polarity. A bare cell or a listing alone is not a qualified pack. |
| Q70 | USB-C was removed from the product direction because its full body did not fit the reference envelope. Historical packing studies still record the rejected geometry. |
| Q71 | Charging is off-ear only. The current fixed TS resistor is not a temperature sensor. |
| Q72 | Reference ring tabs include FR4 stiffeners. The actual stiffener drawing, count and assembly process must be reviewed. |
| Q73 | Historical v2 mounting holes must clear component courtyards and probe geometry. Current v4 uses lid posts instead of those board screws. |
| Q74 | Historical SIG1/SIG2 flex folds use the specified bend envelope rather than zero-radius folding. Actual folds remain untested. |
| Q78/Q84 | Distinguish panel process rails from the finished board edge. Fabricator acceptance is still required. |
| Q89 | A hinge alone is not a closed shell. The selected snap needs repeated physical closure and release checks. |
| Q90 | Do not expose charging pads on the skin face. The current proposal moves them to the posterior wall. |
| Q97/Q98 | Keep electrode branches separated from foreign copper and preserve dedicated contact routes. Check the actual fabricated boundary, not only schematic continuity. |

## Open gates for v4

1. **Electrical protection:** review charger IN/OUT transient protection, effective decoupling and layout. Component ratings do not certify the assembled contacts. Review the fixed-TS, off-ear-only arrangement and cell charge limits.
2. **RF:** the radio keep-out differs from the module recommendation. No range test exists.
3. **Fabrication and supply:** obtain assembly acceptance for two-sided flex, 0201 parts, stiffeners and consigned parts. Recheck all part codes and package identity. No manufacturer order is placed.
4. **First load:** implement the ISP1807 product Arduino variant and verify bootloader, reset configuration, debug voltage levels and GPIO mapping. Do not build the product with a Feather pinout.
5. **Mechanical:** validate snap release, repeated retention, folded flex, lid-post loads, cell lead routing, contact installation and fit. The CAD manifest does not model a person's anatomy.
6. **Evidence:** record raw signal and provenance locally, then show one real contraction completing one harmless audited action. The present demos are synthetic.
7. **Purchase readiness:** replace historical estimates with supported route-specific totals after the design gates pass. Keep any checkout, delivery address and payment records outside the public tree.

Rolf's physical design choices include the earpiece form, titanium contact hardware, limited final assembly and off-ear-only charging. Personal anatomy and physiology are not public design evidence. Any measurements belong in ignored `measurements/`.
