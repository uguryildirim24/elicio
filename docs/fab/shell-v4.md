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

## Closure variants on the unchanged 48.40 mm arc (2026-09-25)

Three **separate** body/lid builds, not edits to `cad/v4`: `cad/v4-m16`,
`cad/v4-snap`, `cad/v4-snap-firm`. Rebuild one at a time with
`build_shell_v4.py --closure m16|snap|snap-firm --out docs/fab/cad/v4-<name>`;
`render_v4.py --single --out` on each directory generates the closure view.
Each manifest contains the complete rerun of **all 97 base §10.2 solid
checks** (courtyards, folded plate, cell, roots, posts, axes, keys), plus
seated body/lid nonintersection and four closure occupancy probes:
**102/102 passing, zero seated overlap, both STL meshes watertight for each**.
The exterior renders cannot show the concealed catch or screw pilot; inspect
STEP for that geometry. These are *nominal solids*, not validated print fits.

### M1.6 cap screw — built, but **reject** for printing

![M1.6 closure shell](cad/v4-m16/render_closure.png)

The screw has moved from the blocked REF tail to **u14.10, s11.80** beside
(but not through) the cell and folded charging plate. Medial entry in the
floor: Ø3.34 head well (Ø3.14 maximum head + 0.20 clearance), seat y1.76,
Ø1.80 clearance shank into a hanging lid boss Ø3.60; Ø1.40 pilot in PA12.
A 4 mm shank ends at y5.76; the lid boss begins at y4.05 and has **1.71 mm
nominal engagement**, only **1.01 mm after allowing two incomplete 0.35 mm
threads** (Westfield's 4–6 mm shank-length tolerance is ±0.24 mm, so a
short screw could leave only 0.77 mm of that effective engagement).
Body boss Ø3.60 connects to the floor, with 0.10 mm separation
from the lid boss. Neither changes the board, contact holes or hinge.
The **minimum wall is just 0.13 mm radially at the head well**, though the
lid pilot's radial wall is 1.10 mm (1.00 mm around a nominal Ø1.60 shank).
JLC3DP's published PA12-HP MJF wall is **1 mm**, tolerance **±0.3 mm**
([material page](https://jlc3dp.com/help/article/pa12-hp-nylon), accessed
2026-09-25): this head pocket does not meet it. Do not order this shell.

**Pull-out calculation, not a test:** an assumed printed-PA12 thread shear
allowable of *half* the datasheet tensile strength (48/2 = 24 MPa) times
π × nominal M1.6 diameter × 1.01 effective engagement gives **122 N ideal
thread stripping force**. The factor of 1/2, stripped-thread geometry and
print direction are unverified, so actual pull-out margin is **UNVERIFIED**;
this is not a rated 122 N fastener. A failed 0.13 mm wall supersedes the
thread estimate. The screw is a separate purchase: ISO 4762/DIN 912
M1.6×4, hex 1.5 mm; **price and stocked SKU UNVERIFIED**
([Westfield DIN 912 table](https://www.westfieldfasteners.co.uk/Standards/ScrewBolt-SHCap-M.html),
accessed 2026-09-25). Printed body/lid price **UNVERIFIED** (JLC3DP
[PA12-HP](https://jlc3dp.com/help/article/pa12-hp-nylon) advertises *from*
$1.00, not this shell's quote; accessed 2026-09-25). One existing 1.5 mm
hex key only, no insert, glue, solder or crimp.

The same [Westfield table](https://www.westfieldfasteners.co.uk/Standards/ScrewBolt-SHCap-M.html)
(accessed 2026-09-25) gives ISO 4762 M2 Ø3.98 max × 2.00 high,
1.5 mm hex; M1.6 Ø3.14 max × 1.64 high, 1.5 mm hex. A trial of M2
at the cell-side station left a disconnected boss because the Ø4.18 well
exceeded a Ø4.00 pillar. A pillar with ≥1 mm wall there intersects the
fixed folded charging plate/cell; it was **not exported as a valid variant**.
The Westfield [ISO 7380-1 table](https://www.westfieldfasteners.co.uk/Standards/ScrewBolt-SHBtn-M.html)
does not even specify M2 (starts at M3; M2.5 is a vendor extension). An M2
button-head with a documented 1.5 mm hex, diameter, height and SKU is
**UNVERIFIED**, not assumed R2-compatible.

### PA12 snap with existing hinge — two release-feel candidates

**Softer beam:** ![snap shell](cad/v4-snap/render_closure.png)

**Firmer beam:** ![firm snap shell](cad/v4-snap-firm/render_closure.png)

Both cut an end-wall recess u13.30–15.50, s38.05–40.05, y4.05–7.10 and
replace the catch ledge at u13.40–15.50 × s39.80–40.80 × y5.35–6.35.
The lid has a u13.65–15.35 beam from y7.18 down to y4.15, a 1.00-mm-high
foot protruding to s40.02 under the ledge (0.22 mm nominal horizontal
engagement; **0.20 mm** vertical clearance), and a 2.00 × 1.20 mm opening
in its top to press the foot toward −s with the *existing* hex key before
lifting. The **minimum new free wall is 1.00 mm** (beam thickness along s
for the soft option; side wall u15.50–16.50; foot, ledge and remaining lid
plate each 1.00 mm). The firm option thickens just the beam along s from
1.00 to **1.15 mm**. Beam width 1.70 mm, effective cantilever length
**2.95 mm** from lid underside y7.10 to foot y4.15; estimated release
travel **0.25 mm**, more than the 0.22 mm engagement. Body and lid retain
unchanged contact geometries and hinge. Neither adds purchased closure
hardware. Parts: the v4 PA12 MJF body and lid only, **price UNVERIFIED**;
[JLC3DP PA12-HP page](https://jlc3dp.com/help/article/pa12-hp-nylon)
(accessed 2026-09-25) advertises from $1.00, not an approved quote.

For a straight rectangular cantilever, ε≈3tδ/(2L²) gives **4.31%** soft
and **4.96%** firm; below JLC3DP's published **20% elongation at break**
(ASTM D638; same [PA12-HP datasheet](https://jlc3dp.com/help/article/pa12-hp-nylon),
accessed 2026-09-25). With its published tensile modulus **1800 MPa**, the
ideal lateral release force Ebt³δ/(4L³) is **7.45 N** soft or **11.33 N**
firm. These are beam-model numbers, *not measured latch retention*.
A crude upper bound on vertical force before an ideal unnotched beam
cross-section reaches the published 48 MPa tensile strength is
48 × 1.70 × t = **81.6 N / 93.8 N**, respectively; the real axial pull-off
load and cycle life are **UNVERIFIED** (stress at the root/foot and key slot,
no dynamic snap or physical coupon test). The 0.20–0.25 mm catch/clearance
features are **smaller than ±0.3 mm print tolerance**, so a print can jam,
fail to engage or open too easily. R2 is preserved: no solder, glue, crimp
or wire stripping, and at most the one existing key to open.

| Variant | Body / lid change | Minimum new wall | Nominal release or pull-out | §10.2 + seam + four closure probes | Parts / price | Status |
|---|---|---:|---|---|---|---|
| M1.6 × 4 cap | Floor pillar + medial well / lid pilot boss at s11.80 | **0.13 mm** head wall | 122 N *conditional* thread model; actual unknown | 102/102 | M1.6 screw price UNVERIFIED; shell price UNVERIFIED | Reject: below 1 mm print wall |
| Soft snap | Tail notch and 1 mm ledge / 1 mm beam + key opening | **1.00 mm** | 7.45 N lateral model; axial unknown | 102/102 | PA12 body/lid only, price UNVERIFIED | Trial candidate |
| Firm snap | Same / 1.15 mm beam | **1.00 mm** at body sidewall | 11.33 N lateral model; axial unknown | 102/102 | PA12 body/lid only, price UNVERIFIED | Trial candidate |

**Recommendation:** choose the **soft snap for a print/coupon and cycle-fit
experiment**, *not for wear or an order today*: it has no sub-1 mm new wall
and the gentler release model. If repeated closures show insufficient
engagement, try the firm beam. The 0.0894 mm U3 nominal clearance remains
below print tolerance in *all* variants. The original M2.5×8 would require
screw centre s≥50.25 and tip at least **s53.75** (centre + 2.50 head radius
+ 1.00 end wall), i.e. **5.35 mm extra arc**; at bow 3.0 the M1 chord gate
would rise from **50.901** to **56.301 mm**. Lengthening is reference only,
not built here, and would change the behind-ear fit.

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
