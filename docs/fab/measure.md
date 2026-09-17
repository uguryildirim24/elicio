# Measure the ear (order 1)

Phone sheet. Digital caliper and a non-stretch string. About ten minutes.
One step, one number. Write millimetres. Do not order anything from this
sheet.

Defaults are the reference-ear build in `docs/fab/plan.md` §3.3. A key you
leave blank takes that default and the build is marked REF. Measure M1
first. If you measure nothing else, that is the REF gauge.

Ear (write `right` or `left`): ________
If this line is blank, the build is the right ear.

**Defaults, if you measure M1 only.** M2 = 58, M3 = 11, M4 = 6.0, M5 = 2.5,
M6 = 15, M7 = 22, M8 = 11. CREASE_BOW stays 3.0 mm, so the gate is 50.91 mm.
SIDE stays right unless you wrote `left`. The CAD run is marked REF.

**How the bow is set.** The script computes CREASE_BOW from M1 and M2 only
when you give it both. If M2 is blank, the bow stays 3.0 mm.

---

## M1 — ear root length (do this first)

**Gate.** The shell chord is TOTAL_CHORD. The CAD script rejects the build
if M1 is below TOTAL_CHORD + 3 mm. TOTAL_CHORD depends on the bow, and the
bow comes from M1 and M2, so the gate is read after M2.

**Formula** (plan §3.2–§3.3). BODY_ARC is 48.4 mm. CREASE_BOW is `b` mm.
TOTAL_CHORD is the chord `C` of that arc:

- `R = C² / (8b) + b / 2`
- `BODY_ARC = 4R · atan(2b / C) = 48.4`
- gate = TOTAL_CHORD + 3

The script's gate at the three reference bows, and the smallest caliper
reading (0.01 mm) that passes:

| CREASE_BOW (mm) | 1 | 3 | 8 |
|---|---:|---:|---:|
| TOTAL_CHORD (mm) | 48.34 | 47.90 | 44.67 |
| Script gate (mm) | 51.345 | 50.901 | 47.673 |
| M1 must be at least (mm) | 51.35 | 50.91 | 47.68 |

**Stop rule, after M1.**

- M1 is 51.35 or more: you pass at every bow. Go on to M2.
- M1 is below 47.68: stop. Do not measure M2–M8. This release does not
  build a shorter shell (plan §10, Open for Rolf item 1, and interface
  item 4).
- M1 is between: measure M2 next, then read the gate in the M2 step.

**Tool.** Digital caliper, outside jaws. No string.

**Landmark.** The two points where the ear joins the skull: the top of the
crease (helix root) and the bottom of the crease.

**Picture.** Stand side-on to a mirror, or take a side photo. Behind the
ear is a groove (the crease) from the top attachment down to the bottom
attachment. Open the caliper. Put one jaw on the top attachment. Put the
other jaw on the bottom attachment. The line is straight, through the air,
not along the groove.

**Typical range.** 45–58 mm.

**Write M1.** ________ mm

If M1 is below 47.68 mm, stop here.

---

## M2 — crease arc

**Tool.** Non-stretch string, then the caliper.

**Landmark.** The same two attachment points as M1, along the crease.

**Picture.** The crease is the groove where the back of the ear meets the
skull. Lay the string in that groove from the top attachment to the bottom
attachment. Mark the two points on the string. Straighten the string.
Measure the marked length with the caliper.

**Typical range.** 50–65 mm.

**Feeds.** CREASE_BOW (with M1), clamped 1–8 mm.

**Write M2.** ________ mm

**Gate, if M1 was below 51.35.** Subtract: M2 − M1 = ________ mm. Find the
largest row not above your difference. If M1 is below that row's number,
stop: this release does not build for your ear.

| M2 − M1 (mm) | Bow the script uses (mm) | M1 must be at least (mm) |
|---:|---:|---:|
| M2 not measured | 3.0 | 50.91 |
| 0 or less | 1.0 | 51.35 |
| 0.25 | 2.1 | 51.16 |
| 0.5 | 3.0 | 50.91 |
| 1.0 | 4.2 | 50.40 |
| 1.5 | 5.2 | 49.88 |
| 2.0 | 6.0 | 49.35 |
| 2.5 | 6.7 | 48.80 |
| 3.0 | 7.4 | 48.25 |
| 3.5 or more | 8.0 | 47.68 |

The rows are computed at M1 = 47.7, which gives the highest gate for each
difference, so the table never passes an ear the script rejects. The
script's own check decides.

---

## M3 — sulcus clearance

**Tool.** Digital caliper, depth rod.

**Landmark.** Mid-height of the ear. Skull in the crease, out to the helix
rim.

**Picture.** At mid-height of the ear, the rim of the ear stands off the
head. Hold the caliper behind the ear, pointing at the head. Rest the end
of the beam on the edge of the rim. Open the caliper so the depth rod slides
past the rim into the groove until it touches the head. Read the caliper.
Do not press the ear flat.

**Typical range.** 8–14 mm.

**Feeds.** Span report only (BODY_THICK + 1.35 mm crown versus M3).

**Write M3.** ________ mm

---

## M4 — helix root thickness

**Tool.** Digital caliper, outside jaws.

**Landmark.** The cartilage bridge at the top attachment, where the hook
will sit.

**Picture.** At the top of the ear, a thin cartilage ridge joins the ear
to the head; the hook sits over it. Put one jaw in the top of the groove
behind the ear, against the head. Put the other jaw on the outer face of
the ear at the same point. The jaws close sideways, head to outside, not
front to back. Close until the jaws touch. Do not squeeze.

**Typical range.** 4.5–7.5 mm.

**Feeds.** HOOK_ROOT Y (half of M4).

**Write M4.** ________ mm

---

## M5 — glasses temple thickness

**Tool.** Digital caliper, outside jaws.

**Landmark.** The glasses temple where it passes the ear. If you do not
wear glasses, write 0.

**Picture.** Put the glasses on. At the ear, the temple is the arm that
runs back above the crease. Put the jaws on the temple there, top to
bottom. If there are no glasses, write 0. The hook then has no glasses
flat.

**Typical range.** 1.8–3.2 mm, or 0.

**Feeds.** GLASSES_FLAT (0.8 mm cut if M5 > 0).

**Write M5.** ________ mm

---

## M6 — mastoid offset

**Tool.** Digital caliper, outside jaws.

**Landmark.** Crease to the bony bump behind the lower ear.

**Picture.** Feel behind the lower ear for the mastoid, a hard bump of
bone. One jaw in the crease at that height. The other jaw on the peak of
the bump. The line is straight, roughly backward.

**Typical range.** 12–18 mm.

**Feeds.** Recorded for WP7a. Not a CAD driver in this release.

**Write M6.** ________ mm

---

## M7 — crease top to mid-concha

**Tool.** Non-stretch string, then the caliper.

**Landmark.** Top attachment, along the crease, down to the height of the
ear-canal opening.

**Picture.** Look in the ear. The canal opening is the hole. Follow the
crease down from the top attachment until you are at that same height.
Mark that point. String along the crease between the top attachment and
that point. Measure the string.

**Typical range.** 18–26 mm.

**Feeds.** Recorded for WP7a. Not a CAD driver in this release.

**Write M7.** ________ mm

---

## M8 — helix rise

**Tool.** Digital caliper, outside jaws, vertical.

**Landmark.** Top attachment, up to the highest point of the ear rim.

**Picture.** The highest point of the ear rim is the top of the helix,
above the attachment. One jaw on the top attachment. The other jaw on that
highest rim point. The line is straight up.

**Typical range.** 8–14 mm.

**Feeds.** HOOK_RADIUS = M8 + 2.5 mm (13.5 at the default 11).

**Write M8.** ________ mm

---

## Copy line

Give this block to the CAD run (`scripts/cad/params/rolf.toml`). Blank
keys take the reference values above and mark REF. The bow is computed only
if both M1 and M2 are filled in.

```
SIDE    ________     (right or left; blank = right)
M1      ________ mm
M2      ________ mm
M3      ________ mm
M4      ________ mm
M5      ________ mm
M6      ________ mm
M7      ________ mm
M8      ________ mm
```

The 100 g hook test is not an ear measurement. Do it on the printed
`body_full_p15` after the parcel arrives. Steps are in `order1.md`.
