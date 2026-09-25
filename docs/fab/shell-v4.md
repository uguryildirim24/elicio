# Shell v4 — W18 × T8.1, same 48.4 mm arc (prototype, NOT CLOSED)

The v4 board's folded **courtyard boxes**, not only pin centres, clear the built
shell nominally. **This is not a wearable/print release**: the screw cannot fit
at the unchanged length and the lid has only its hinge. Rolf must choose
whether to change the length or the closure concept. No latch was substituted.

## Build / difference from v2f

```sh
.venv/bin/python scripts/cad/build_shell_v4.py --out docs/fab/cad/v4
.venv/bin/python scripts/cad/render_v4.py --out docs/fab/cad/v4
```

`params/shell_v4.toml` overlays the same construction path as v2f; it does not
replace v2f solids. Body width **18.00**, floor **1.50**, cavity
**u 1.50–16.50**, LID_Y **7.10**, body-frame highest lid **8.10**, arc
**48.40** (length unchanged). On the built solid, body-frame bounding box
maximum y = **8.1000001** and lid maximum y = **8.1000001**. The r9 lid's
extra 1.25 rim + 0.90 crown would have reached y **9.25** here, so the v4
loft follows the same ear-fit outline and curved body path but uses a 1.0 mm
lid with no raised crown; its rim rounding is 0.8 instead of 1.0. This
trade-off needs visual/physical approval before printing. Hook root, elliptical
hook loft, REF end-wall slot, SIG channels, hinge undercut and P1–P3
contacts remain from the r9 shell. No USB or skin-face charging contacts.

The folded charging plate uses holes Ø2.7 through the posterior wall at
s **4.35** and **12.10**, y **4.295**, without proud hex sockets. Each
standoff is keyed by two floor-standing walls u **13.19–16.19**, s
**site−3.80 to site−2.80** and **site+2.80 to site+3.80**, y
**1.50–4.30**. The rib slot is u **16.00–16.50** × s **14.90–15.70** ×
y **1.50–4.50** (last cut, so it also trims the P5 upper key where they
cross). It removes **1.4008 mm³** of the pre-slot rib. The v2 island corner pad
otherwise collides with the v4 P4/P5 joint root by **0.8433 mm³**; its
obsolete top corner is relieved at u15.09–16.30 × s16.30–19.30 ×
y3.80–5.12, leaving **0 mm³** overlap with the joint. Floor-to-outer-side
wall at the slot is **18.00−16.50 = 1.50 mm**. The standoff's open −u end
is at 13.19: gap to the cell's 11.90 edge is **1.29 mm**. The P5 key near
the rib is locally interrupted by the flap slot; retention force is
UNVERIFIED. Posts Ø2.0 extend **1.98 mm** from (5.90, 23.00) to board top
y5.12 and **0.98 mm** from (9.40, 32.10) to U1 top y6.12; both were
probed in the lid solid.

## Measured nominal folded fit

`cad/v4/manifest.json` stores one check per §10.2 courtyard (the actual
line-centre u/s bounds and y extents), including the four exterior tab
components, plus envelopes and hardware. For each component the margin below
is the **minimum OCCT distance from its entire courtyard prism to the body or
lid solid**, in mm, provided both intersections have zero volume; it is *not*
a placement coordinate or a print-tolerance guarantee. U1 touching the
second post by design has zero margin. Exterior tab rows are absent from the
closed shell after cutting and have no distance. Post rows report occupied
volume (mm³), not free distance. All measured interior intersections are
**0 mm³**. Table source: `board-v4-design.md` §10.2, not §10.1 pin centres.

| Row | margin | Row | margin | Row | margin |
|---|---:|---|---:|---|---:|
| C1 | 2.0900 | C2 | 1.6096 | C3 | 1.6000 |
| C4 | 1.1938 | C5 | 1.1600 | C6 | 0.3900 |
| C7 | 1.5300 | C8 | 0.9109 | C9 | 1.3800 |
| C10 | 1.6200 | C11 | 1.0500 | C12 | 0.5850 |
| C13 | 1.0755 | C14 | 1.4400 | C15 | 1.6300 |
| C16 | 0.8237 | C17 | 1.6300 | D1 | 1.1989 |
| D2 | 0.9200 | J2 | 0.4320 | J3 | cut off |
| J4 | 0.8535 | Q1 | 1.1100 | Q2 | 2.0900 |
| Q3 | 1.1240 | Q4 | 1.2000 | R1 | 1.0600 |
| R2 | 1.1526 | R3 | 1.0200 | R4 | 2.0900 |
| R5 | 0.9398 | R6 | 1.6200 | R7 | 1.6300 |
| R8 | 0.9192 | R11 | 0.8037 | R12 | 1.6300 |
| R13 | 1.6300 | R14 | 1.1600 | R15 | 1.6687 |
| R16 | 1.9785 | R17 | 1.3500 | R18 | 1.3014 |
| R19 | 1.1600 | R20 | 2.0900 | R21 | 1.8846 |
| R22 | 1.2000 | R23 | 0.5696 | R24 | 1.7258 |
| R25 | 2.0900 | R27 | 1.6300 | R28 | 1.6300 |
| R31 | cut off | R32 | cut off | R33 | cut off |
| R34 | 1.2000 | R35 | 1.4000 | SW1 | 0.8000 |
| U1 | 0.0000 | U2 | 0.9800 | U3 | 0.0894 |
| U4 | 1.1100 | U5 | 0.3100 | | |

| Additional §10.2 row / test | measured margin, mm (or occupied volume) |
|---|---:|
| Cell + foam envelope u1.8–11.9 × s1.5–14.5 × y1.501–7.099 | 0.0000, zero overlap |
| SIG1 folded root | 0.0100 |
| SIG2 folded root | 0.0100 |
| REF root through end-wall slot | 0.0000 |
| P4/P5 flap slot | 0.0100 |
| Folded P4/P5 plate | 0.0000 |
| P4/P5 joint root (v4 notch relief) | 0.0000 |
| P1/P2/P3 ring axes at y0.05, 0.75, 1.65 | 9/9 open, 0.0000 each |
| J3 stub after tab cut | 0.3000 |
| Island board plane | 0.5952 |
| P1 post in specified landing region | 6.1375 mm³ nylon |
| P2 post in specified landing region | 3.0378 mm³ nylon |
| P1, P2 post bottom y datum | 5.12, 6.12 (each occupied +0.05; air −0.05) |
| P4/P5 four key walls at mid-wall probe | 4/4 solid, 0.50 inside the 1.0-wide key |
| P4/P5 axis at u13.10, 16.55, 17.95, 18.05 | 8/8 air (outer face open) |
| J2 courtyard edge to P5 standoff's open end (8.38 → 13.19) | **4.81**, against ≥0.30 needed |
| Body vs seated lid interiors | 0 mm³ overlap |
| STL body / lid | both watertight |

The earliest side clearance to a component is U5 0.31 mm; U3 is only
**0.0894 mm** from the nearest shell surface. These are nominal CAD
numbers, not tolerance-stack release. J4 height is pads-only; a mating
fixture is not included. The P4/P5 plate check probes the plate volume,
not a 3D model of its bends or actual hardware.

## Closure blocked by the unchanged length

The r9 medial-tail M2.5×8 head well Ø5.0 beside REF Ø7.5 cannot keep
1.0 mm nylon each side at W18: REF pocket's +u edge = **12.25**;
12.25 + 1.00 + 5.00 + 1.00 = **19.25**, **1.25 mm beyond** the 18.00
body (the −u option ends at 4.75−7.00 = **−2.25**). Clearing the REF
pocket in s needs screw centre ≥ **43.00+3.75+1.00+2.50 = 50.25**;
this is **1.85 mm beyond the 48.40 arc/tip** and **4.75 mm past the
45.50 tail-loft start**. No pilot, well, boss or tongue can be placed
there with a ≥1.0 wall; at this location available body nylon is **0**,
so achievable thread engagement is **0 mm**, below the required 3.0.
The previous screw geometry was omitted, rather than claiming a working
closure or adding an unapproved latch. The retained hinge alone does **not**
retain the lid. A longer tail would violate the same-length requirement;
a different fastener/closure needs Rolf's decision. No hardware board
changes are requested.

## UNVERIFIED / do not order

Physical PA12 print tolerance, snap/retention and S4 pull/drop, contact
installation, actual folded-board bend radii and P5 interrupted-key strength,
post load on U1, package maxima marked UNVERIFIED in §10.2, cell lead
routing, RF/antenna range, skin fit, seam and visual approval are not proven.
Even though all nominal box checks pass, a nominal U3 gap of 0.0894 does
not absorb a ±0.3 mm print tolerance. The two exterior renders show the
shell; the folded-board view contains **schematic envelopes**, not an actual
PCB assembly. All three PNGs and STEP/STL/3MF file hashes are in the v4
manifest. The body is **not ready to print or wear** without a working
closure and physical verification.
