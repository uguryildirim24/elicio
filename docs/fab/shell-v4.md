# Shell v4 — W18 × T8.1, same 48.4 mm arc (snap print trial only)

The unmodified `cad/v4` shell has only a hinge; it is **not closed**. The
separate `cad/v4-snap` shell has a ramped two-arm latch and a full-width key
corridor, but printed fit, retention and repeatability remain unverified.
Do not wear or order it as a finished product.

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
cross). It removes **1.4008 mm³** of the pre-slot rib. The folded flap continues to s19.30,
and the original bay shoulder *also* overlapped its lower plate volume by
**1.1845 mm³** beyond that slot (missed by the initial 97 checks). An
additional recess u16.00–16.50 × s15.70–19.30 × y1.50–4.50 removes
**2.5755 mm³** before the joint relief; the full folded flap now has zero
solid overlap. The v2 island corner pad otherwise collides with the v4
P4/P5 joint root by **0.8433 mm³** before either recess; its obsolete top
corner is relieved at u15.09–16.30 × s16.30–19.30 × y3.80–5.12, leaving
**0 mm³** overlap with the joint. Floor-to-outer-side wall at the recess is
**18.00−16.50 = 1.50 mm**. The standoff's open −u end
is at 13.19: gap to the cell's 11.90 edge is **1.29 mm**. The P5 key near
the rib and bay shoulder are locally interrupted by the flap recess;
retention force is UNVERIFIED. Posts Ø2.0 extend **1.98 mm** from (5.90, 23.00) to board top
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
| C1 | 2.0900 | C2 | 1.6096 | C3 | 0.8319 |
| C4 | 1.1938 | C5 | 1.1600 | C6 | 0.3900 |
| C7 | 1.5300 | C8 | 0.9109 | C9 | 1.3800 |
| C10 | 1.6200 | C11 | 1.0500 | C12 | 0.5850 |
| C13 | 1.0755 | C14 | 1.4400 | C15 | 1.6300 |
| C16 | 0.8237 | C17 | 1.6300 | C18 | 0.9700 |
| C19 | 1.3800 | D1 | 1.1989 | | |
| D2 | 0.9200 | J2 | 0.4320 | J3 | cut off |
| J4 | 0.8535 | Q1 | 1.1100 | Q2 | 2.0900 |
| Q3 | 1.1240 | Q4 | 1.2000 | R1 | 1.0600 |
| R2 | 1.1526 | R3 | 1.0200 | R4 | 2.0900 |
| R5 | 0.9398 | R6 | 1.6200 | R7 | 1.6300 |
| R8 | 0.9192 | R11 | 0.8037 | R12 | 1.6300 |
| R13 | 1.6300 | R14 | 1.1600 | R15 | 1.6687 |
| R16 | 1.9785 | R17 | 2.0900 | R18 | 1.3014 |
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
| P4/P5 folded flap, s14.85–19.30 × y1.695–3.905 | 0.0000, zero overlap |
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
fixture is not included. The P4/P5 plate and flap checks probe bounding
prisms, not a 3D model of its bends or actual hardware.

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

Two **separate** body/lid builds, not edits to `cad/v4`: `cad/v4-m16` and
`cad/v4-snap`. Rebuild one at a time with `build_shell_v4.py --closure
m16|snap --out docs/fab/cad/v4-<name>`; `render_v4.py --single --out` on
each directory makes the closure view. On the routed board's current §10.2
courtyards, the base has **101/101 checks passed** (100 base, seated overlap),
including C3 on top, C18, C19, the moved R17 and the full P4/P5 folded flap.
M1.6 was rebuilt too: **105/105 checks passed**, but its 0.13 mm wall
rejects it. The snap has **106/106 checks passed** (100 base, seated overlap,
three swept-key checks, two tolerance builds); zero seated overlap, zero flap
overlap, both STLs watertight. The exterior render cannot expose the concealed hook: inspect
STEP for that geometry. These are CAD solids, not validated print fits.

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

### Ramped twin-arm PA12 snap with existing hinge — trial candidate

![snap shell](cad/v4-snap/render_closure.png)

**Close:** align the hinge, then lower the lid. The foot slides down the two
sloping ledges; the two arms bend toward the hinge and spring back when the
foot passes underneath. Do not force a jammed print. **Open:** find the
rectangular opening in the lid beside the tail at s39.80–44.60; insert the
existing 1.5 mm hex key vertically in the *middle* (u≈12, s≈43.38), down
to the foot (tip y≈3.35). Push the key **toward the hinge** (decreasing s)
to move the foot clear of both side ledges; hold it there and lift the lid.
Do not pry against the floor or either ledge. No second tool, glue or crimp.

The body pocket is u9.50–14.50, s38.05–44.60, y2.50–7.10, retaining a
1.00 mm floor. Its paired ramped ledges lie on u9.50–10.90 and
13.10–14.50; the left rail joins the tail at s47.50, the right at s45.00.
Their undersides start at s41.30, y4.85. Two 1.00 mm-thick, 1.10 mm-wide
lid arms (s39.70–40.70) extend to y3.15; a 1.00-mm-high foot spans
u9.80–14.20, s40.60–42.00. Horizontal engagement is **0.70 mm** nominal;
with *opposing* ±0.30 mm errors on ledge and foot it is **0.10–1.30 mm**.
Each wing overlaps its side ledge 1.10 mm across u, at least 0.50 mm
after opposing ±0.30 mm errors. The foot-to-ledge vertical air is 0.70 mm
nominal, at least 0.10 mm for opposing errors; floor-to-foot air is 0.65 mm
nominal, at least 0.05 mm.
The full 1.5 mm across-flats hex prism plus 0.20 mm per flat was swept
through the opening and down the approach, then along the initial release
stroke: zero body/lid collision except the deliberately contacted foot.
The two extreme ledge/foot solids were rebuilt with opposing ±0.30 mm
s offsets: each retained positive engagement and a zero-volume collision
when the entire foot was posed behind the ledge at closing (0.12 and
1.32 mm travel, respectively). These are rigid clearance checks, not a
nonlinear simulation of bending or a physical release test.

For a straight rectangular beam, worst-case ε≈3tδ/(2L²) with t=1.00,
δ=1.32 and L≈3.95 mm gives **12.69%** surface strain, below published
**20% elongation at break** by a factor **1.58**. This is a simplified
beam model, not a fatigue guarantee: the joining bridge and root may
concentrate stress. Source: [JLC3DP PA12-HP MJF material datasheet](https://jlc3dp.com/help/article/pa12-hp-nylon),
20% ASTM D638 elongation, 1800 MPa tensile modulus and 48 MPa tensile
strength; accessed 2026-09-25. Approximate two-arm lateral force at 1.32 mm:
Ebt³δ/(4L³) with total arm width 2.20 mm = **21.2 N** (model only).
Actual axial retention, wear, fatigue, closure force and key leverage remain
**UNVERIFIED**. Minimum pocket floor, arm thickness, ledge height and foot
height are 1.00 mm; each arm is 1.10 mm wide. The right outer wall near
s44.60 is approximately 0.99 mm by the taper formula and requires print
review. The central corridor
is 2.20 mm between ledges; the 1.9 mm AF inflated key leaves 0.15 mm
on each side. Parts: printed PA12 body/lid, price **UNVERIFIED** (JLC page
advertises from $1.00, not a quote for this shell). No added closure hardware.
The former 1.15 mm firm arm was **dropped**: it had an impassable key slot,
a blocked ledge path and sub-tolerance 0.22 mm engagement. Thickening it
cannot fix those defects.

| Variant | Minimum closure wall | Retention evidence | Solid checks | Parts / price | Status |
|---|---:|---|---:|---|---|
| M1.6 × 4 cap | **0.13 mm** head wall | 122 N conditional thread model; actual unknown | 105/105 | screw price UNVERIFIED; shell price UNVERIFIED | Unsuitable: below 1 mm |
| Twin-arm snap | **≈0.99 mm right tail wall** (1.00 mm arm thickness) | 0.10–1.30 mm tolerance engagement; axial pull-off UNVERIFIED | 106/106 | PA12 body/lid only, price UNVERIFIED | Trial candidate, tail wall needs print review |

**Recommendation:** assess the new snap geometry on a first test print and
cycle it before use. The 0.0894 mm U3 nominal clearance is still below
print tolerance. The original M2.5×8 needs screw centre s≥50.25 and tip
at least **s53.75** (centre + 2.50 head radius + 1.00 end wall): **5.35 mm
extra arc**; at bow 3.0 the M1 chord gate rises from **50.901** to
**56.301 mm**. The longer body is reference only, not built, and changes fit.

## UNVERIFIED / do not order

Physical PA12 print tolerance, snap/retention and S4 pull/drop, contact
installation, actual folded-board bend radii and P5 interrupted-key strength,
post load on U1, flap recess strength, package maxima marked UNVERIFIED
in §10.2, cell lead
routing, RF/antenna range, skin fit, seam and visual approval are not proven.
Even though all nominal box checks pass, a nominal U3 gap of 0.0894 does
not absorb a ±0.3 mm print tolerance. The two exterior renders show the
shell; the folded-board view contains **schematic envelopes**, not an actual
PCB assembly. All three PNGs and STEP/STL/3MF file hashes are in the v4
manifest. The CAD is a **test-print candidate, not a wearable release**; the first
print must prove that the key actually reaches and releases the foot, that
both hooks engage and close without fracture across repeated cycles, and
that the seam and U3 clearance remain usable. Do not order or wear as a
finished product before that evidence.
