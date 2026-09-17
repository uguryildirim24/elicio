# Earpiece hardware design record

This is the design record for Elicio's first self-built hardware direction.
It records the decisions made on 2026-08-13, the evidence behind them, the
staged build plan, and the circuit design for the first bench stage. Nothing
in this document authorizes a purchase; per the handoff rules, every purchase
requires the owner's explicit approval.

## Decision record, 2026-08-13

**Subtlety is the binding requirement.** The owner rejected the forearm
gesture vocabulary not on accuracy but because visible gestures fail the real
goal: input that an observer cannot see. Both the act and the worn hardware
must be unremarkable. This supersedes peak-accuracy comparisons between
devices.

**The hardware will be self-built.** 3D printing for the wearable and the
electrodes, outsourced PCB fabrication and assembly for boards, purchased ICs
for the parts nobody fabricates at home. The owner explicitly prefers a
longer self-built path over buying sensor modules.

**The ear is the convergence point.** Every covert channel that survived
review co-locates at one ear, so one printed earpiece replaces the
four-devices-in-four-places stack:

| Channel | Role | Sensor | Where |
| --- | --- | --- | --- |
| Auricular muscle flex | Primary command | Dry electrodes over posterior/superior auricular muscles | Behind ear |
| Jaw clench (masseter/temporalis) | Confirmation, per the existing policy design | Same electrode region | Behind ear |
| Tensor tympani rumble | Command, if the owner has or trains it | Pressure sensor in a sealed canal tip | In canal |
| Tongue/teeth clicks | Extra discrete symbols | Piezo contact mic | Behind ear |
| Ear-EEG | Slow state channel, much later | Electrode ring in canal/concha | In canal |

**Primary channel: auricular EMG.** On 2026-08-13 the owner verified
voluntary control of the auricular muscles, and on the same day confirmed
independent left-ear and right-ear control plus graded control (twitch,
sustained hold, and levels between). That is at least six covert symbols
(left, right, both, each as twitch or hold) before any pattern coding —
the size of the current harness alphabet. Voluntary tensor tympani control
is unverified for the owner; the sealed-tip pressure sensor will answer it
objectively later, so it is a candidate, not a dependency. The auricular
muscles are functionally near-silent in daily life, which gives the primary
command channel a low background false-positive rate; known cross-talk
sources (yawning, wide smiles) must appear in the false-positive test plan.

Stage A remains single-channel on purpose. Left-versus-right needs a second
channel and makes a bilateral Stage B (a pod per ear) the likely follow-on;
one channel already distinguishes twitch, hold, and double-twitch by
duration and pattern.

Command and confirmation remain different muscle groups (auricular versus
masseter), satisfying the harness's independence rule inside one device.

## Evidence

- EarRumble, CHI 2021: discreet input from voluntary tensor tympani
  contraction; patterned gestures (double, long) used against natural
  activations during chewing and vocalization.
- EarSwitch concept study, J NeuroEng Rehabil 2024: 43.2% of surveyed people
  report voluntary ear rumbling; in-ear barometry in a sealed canal detected
  voluntary contraction with a 95%-accuracy classifier. Developed as
  assistive technology for motor neurone disease.
- NextSense Smartbuds, commercial launch February 2026: six dry EEG sensors
  in earbud tips, validated against intracranial EEG. Proof that ear-canal
  biopotential sensing works in a consumer form factor.
- Wolterink et al., Sensors 2020, and Alokaily et al., Micromachines 2026
  (already recorded in `VISION.md`): 3D-printed carbon-black TPU dry
  electrodes classify at 83-87% with SNR comparable to gelled Ag/AgCl;
  contacts of roughly 16 mm diameter work where 5 mm fail.
- Owner self-test, 2026-08-13: voluntary auricular movement confirmed;
  tensor tympani rumble uncertain.

## Requirements

1. The act of issuing a command must produce no externally visible movement.
2. The worn hardware must be one device at one site, plausible as a normal
   earpiece.
3. Everything that touches skin runs on battery. Never charge while worn.
   During tethered debugging the laptop runs on battery, not mains.
4. Every electrode lead carries a series current-limiting resistor and
   protection clamps. Measurement only; nothing on this path stimulates.
5. Skin contacts are nickel-free: printed carbon-TPU or stainless steel.
6. The decoder output remains `(symbol, confidence, timestamp)`. The harness
   does not change for hardware reasons.
7. Raw samples and timestamps are saved for every session as the permanent
   source record (`elicio capture` does this).

## Staged build plan

Debug loud, operate quiet: each stage brings up hardware on large, easy
signals before moving to the small covert ones.

**Stage A - bench amplifier, one channel.** A protoboard biopotential
amplifier proven on a large forearm contraction, then pointed at the
auricular site. Exit criteria: a live envelope visibly tracking deliberate
contraction in `elicio scope`; a captured auricular session replayed through
`elicio replay-recording` completing one verified harness action. That
replay is the project's first real biological signal completing a real
action.

**Stage B - behind-ear pod.** The same circuit miniaturized onto an
outsourced PCB in a shaped behind-ear shell with dry electrode contacts
and a small battery plus BLE microcontroller. See "Fabrication without a
3D printer" below for how the shell and contacts get made. Exit
criteria: re-donned on three separate days with the detector threshold
unchanged, false-positive rate measured during eating, talking, and walking.

**Stage C - sealed canal tip.** A moulded or printed canal tip sealing a
MEMS pressure sensor (barometry, per the EarSwitch method) plus a piezo contact mic.
Answers the owner's tensor-tympani question objectively and adds click
symbols. This stage is a pressure measurement, not a biopotential one, and
may prove easier than Stage A.

**Stage D - integration.** Pod plus tip as one device feeding the harness
with a small patterned alphabet (short flex, long flex, double flex; rumble
if available; clench confirmation). Only after Stage D does multi-channel
ADS1299-class acquisition or ear-EEG deserve discussion.

## Stage A circuit design

Signal chain, one channel, three skin contacts (two signal over the muscle,
one reference on the mastoid or another bony site):

```text
electrodes -> series R + clamps -> instrumentation amp (G~10)
  -> high-pass ~20 Hz -> gain stage (G 10..100, trimmable)
  -> low-pass ~500 Hz -> level shift to ADC mid-rail
  -> ADC -> microcontroller -> one ASCII sample per line -> elicio scope
```

Starting values, to be verified on the bench rather than trusted:

| Block | Part | Values and rationale |
| --- | --- | --- |
| Protection | 220 kOhm series per lead + diode clamps to rails | Limits any single-fault current to tens of microamps; bias current through 220 k adds negligible offset |
| First gain | INA128 (or AD8226) | Gain 10 (Rg = 5.6 kOhm). Low first-stage gain so electrode DC offset does not saturate the amp |
| High-pass | Passive RC, 100 nF + 82 kOhm | ~19 Hz corner; blocks offset and most motion artifact before further gain |
| Second gain | Non-inverting op-amp (half a TL072) | Gain 11 to 101 via trimmer; total system gain roughly 100 to 1000, tuned live against `elicio scope` |
| Low-pass | Sallen-Key, 22 kOhm with 22 nF / 10 nF | ~490 Hz corner for anti-aliasing |
| Supply | Two 9 V batteries for a +/-9 V bench rail | Simplest correct analog supply; single-supply conversion happens in Stage B |
| Level shift | Divider to ADC mid-rail through a coupling cap | ADC sees 0 to 3.3 V centered at half rail |
| ADC | ADS1115 breakout at 860 SPS | Sufficient for envelope-based contraction detection; the microcontroller's internal ADC is a fallback with known linearity caveats. Full-rate EMG fidelity is a later-stage concern |

The auricular muscles are small, so usable total gain may need to reach a
few thousand; the trimmer plus the live meter make that an empirical
adjustment, not a redesign.

Known limitation, recorded rather than hidden: this stage has no driven
bias (right-leg-drive) electrode. Mains hum rejection relies on battery
power, short twisted leads, and the reference electrode. If hum dominates
on the bench, adding a driven bias amp is the designed next step, not a
failure.

## Stream protocol and software bridge

The firmware prints one ASCII sample value per line at a fixed declared
rate. Blank lines and `#`-prefixed lines are annotations. That is the whole
protocol; it keeps the signal package standard-library-only and makes every
capture human-readable.

For a serial device on Linux, configure the port once and pass it as the
input:

```bash
stty -F /dev/ttyUSB0 raw -echo 115200
.venv/bin/elicio scope --input /dev/ttyUSB0 --sample-rate 860 \
    --offset 2048 --gain 0.001
```

`--offset` recenters the ADC counts and `--gain` scales them so a firm
contraction lands near 1.0 on the meter, matching the detector's working
range and the synthetic fixtures.

The three commands added for this stage:

- `elicio scope` - live envelope meter with the onset threshold marked, and
  event lines when the detector fires. This is also the biofeedback trainer
  for the auricular channel: the meter is the feedback.
- `elicio capture` - saves a session as a recording JSON file with
  provenance metadata. The raw samples in that file are the permanent
  source record for the session.
- `elicio replay-recording` - replays a captured file through detection,
  policy, audit, and the real local marker action, with the same verified
  exit discipline as the demos.

A captured file is deterministic: replaying it always produces the same
events, so real sessions become fixtures exactly like the synthetic ones.

## Harness mapping and false-positive budget

The first real capture deliberately reuses the existing `wrist_down ->
local_marker` command mapping; the detector's default symbol is unchanged.
Renaming the alphabet (for example `auricular_flex`) is a policy-table
decision to make explicitly once the channel is real, not a side effect of
hardware work. The detector accepts a `symbol` argument so capture sessions
can label their site without touching policy.

Budget discipline for the covert channels, using the existing floors:

- A single auricular flex maps only to `RiskLevel.NONE` actions (floor
  0.60).
- Patterned gestures (double flex, long flex) are required before any
  `REVERSIBLE` mapping is proposed, because single covert twitches sit
  closer to background noise than overt gestures.
- `DANGEROUS` keeps its two-event, two-muscle-group rule: auricular command
  plus masseter clench confirmation at 0.85 within the existing window.
- Measured false-positive rates during eating, talking, walking, and
  yawning are recorded per stage before any mapping is promoted.

## Fabrication without a 3D printer

Superseded in part on 2026-09-16 by "Fabrication plan, 2026-09-16"
below. Of the three routes recorded here, outsourced printing survived
and is now JLCPCB (HP MJF PA12-HP), not a conductive-TPU bureau.
Stainless contacts became titanium; conductive TPU remains available
from Palmiga and is not chosen for Stage B. Hand-shaped PCL is dropped.
The rest of this section is the 2026-08-13 record.

Recorded 2026-08-13: the owner does not own a 3D printer. This changes
nothing before Stage B, and Stage A is entirely unaffected because it is
breadboard, modules, and gelled electrodes with no fabricated part in it.

Stage B needs two things made: a shell that holds the pod behind the ear,
and skin contacts. Three routes, none of which require owning a printer:

1. **Outsource the printing.** Palmiga Innovation manufactures the
   PI-ETPU 95-250 carbon-black filament this design cites and offers
   custom printing in its own materials
   (<https://rubber3dprinting.com/>, <https://palmiga.com/3d-printing/>).
   This is consistent with the plan already outsourcing the PCB. General
   print bureaus and library makerspaces are not a substitute here: they
   run rigid PLA and resin, not conductive flexible TPU.
2. **Skip the printed electrode entirely.** Requirement 5 already permits
   stainless steel contacts. Off-the-shelf stainless or gold-plated dry
   electrode discs remove the conductive-filament problem, at the cost of
   giving up the conformal fit that carbon-TPU buys on curved skin.
3. **Shape the shell by hand.** Moldable polycaprolactone thermoplastic
   softens in hot water, is shaped by hand, sets rigid, and remelts if the
   fit is wrong. For a one-off prototype whose geometry is unknown until
   it is worn, hand-shaping iterates faster than printing does.

Stage C is the case where not printing is an advantage. Custom canal tips
are conventionally made from silicone ear impressions, not printed, and
DIY impression kits are sold for exactly this. A moulded tip seals the
canal better than a printed one, and the seal is the whole measurement in
a barometric channel.

No printer purchase is warranted yet. Revisit only if Stage B proves the
channel and contact geometry turns into a real iteration bottleneck.

## Fabrication plan, 2026-09-16

**The Stage B shell is a scripted nylon part, printed by JLCPCB.** CAD
lives in build123d, headless, exporting native STEP from
`scripts/cad/bte_fit_shell.py`. The print is JLC3DP HP MJF PA12-HP,
natural grey, duties prepaid. Skin contacts are three titanium ISO 7380
M2.5 button heads (4.7 mm domes), rigid through a 1.5 mm wall. The first
order is a provisional passive fit gauge for Rolf's ear, not the
electronics. Wear and purchase sit on release states S0 to S4. Nothing
here buys anything: agents do not purchase, upload, quote, or contact a
vendor. Purchases stay Rolf's explicit approval.

`docs/fab/plan.md` is the Phase 1 contract (revision 5, signed off by
GPT-6 Pro at commit `0c5d0eb`). The review record is `tasks/plan/turns/`.

Skin side is PA12 and titanium. Cleaning is a 70 % isopropanol wipe
after each wear. The pod runs on battery only: no connector, no port;
charging is off the ear with the lid removed. Each contact reaches the
board only through its own lead, series resistor, and clamp.

### Conflicts resolved

Each item below is one decision from the plan's §2, with the reason.

1. **Battery.** The cell is a 501015, 50 mAh. Seven hours of streaming
   covers a session. A 30 mm 100 mAh cell forces stacking past 10 mm,
   and 110 mAh was a pricing box, not a fit.
2. **Envelope.** The body is 48.4 × 17.0 × 9.0 mm plus hook, derived in
   the plan's §5. L4's 16 × 9.5 mm islands cannot carry the 15.5 × 10.5
   mm module; L2's box was for quoting; L1 assumed no contact hardware.
   Thickness 9.0 mm is a design value until WP6 confirms packing.
3. **Contact metal.** Titanium only. The brief and this record require
   nickel-free skin contacts; 316L is 10–14 % nickel, and gold flash over
   nickel wears through. Changing requirement 5 is Rolf's, outside the
   plan.
4. **Contact size.** ISO 7380 M2.5, 4.7 mm dome. Other sizes are an
   interface v2 change. Over 4.7 mm the exploratory pressure is 17–23
   kPa; every millimetre of nut keep-out costs body length.
5. **Conductive TPU.** Titanium is primary. Palmiga still prints
   conductive TPU on request; it is a conditional alternative, not the
   Stage B contact. Titanium wins on assembly, small area, and no third
   supplier.
6. **Lid closure.** An external snap lip at the top, a tongue with web
   at the tail tip, and two nubs. Nothing sits inside the cavity. Tape
   is the passive fallback. The first lid is the snap test article.
7. **Gauge material.** MJF PA12, same as order 2. The gauge spends hours
   on skin, so resin is out.
8. **Montage.** Signal pair at 22° off the body axis, 12 mm pitch;
   reference on the tail over the mastoid surface. WP7a fixes positions.
   A 17 mm face cannot hold a horizontal pair, and the mastoid tip sits
   beyond any behind-the-ear body.
9. **Contact count.** Three, not the five L4 asked for. Clench is three
   to five times a flex on the same pair.
10. **Suspension.** Rigid mount, hook preload 1.5 mm. A floating stud
    plus foam does not fit under the board. Force is measured at the
    active gate.
11. **Ear capture.** A generic shell from caliper numbers M1–M8, each
    with a default; defaults only give a provisional gauge. An impression
    waits for Stage C. The gauge costs about $40 and tests the real ear.
12. **Shipping.** Standard DDP for order 1, DHL for order 2. Order 1 is
    not on the critical path.
13. **Shells and PCB.** Separate parcels. They are different tariff
    lines.
14. **Hook.** PA12, one piece with the body. One material; preload is
    measured in WP4.
15. **Gasket.** None. This is a prototype.
16. **Charging.** No port. Pads sit inside the closed cavity; the lid
    comes off to charge. Pad placement is not a mechanical interlock.
17. **Short ears.** This release rejects M1 below the chord gate (about
    51 mm). A second hook-tip branch needs its own schedule and closure;
    it is an interface v2 item, not a silent shrink.

Order 1 is the provisional gauge set, allowance $30–44 with standard
shipping. Order 2 is two Stage B bodies, verified titanium hardware, and
a nickel test kit, allowance about $130, after the §9 gates.

### Release states

| State | Allowed | Entry requires |
| --- | --- | --- |
| S0 gauge | Passive wear per the plan's §3.7 | Rolf's approval of the renders; order 1 checkout gate |
| S1 order 2 | Purchase of shells and hardware | WP5 verified spec; interface v2 accepted; WP7a coordinates and frozen protocol; §3.7 re-run for any changed input; closure test result |
| S2 assembled | Bench only | Reviewed schematic with three separately protected paths; assembled inspection; battery-powered leakage and continuity check; DMG screen |
| S3 validation wear | Only the sessions WP7a prescribes, at most 4 h per day | S2 pass; protocol unchanged since S1 |
| S4 routine use | Daily wear; decoder mapping promotion per this record | All WP7a criteria pass, including three days and background activities |

Fail at S3 returns to S2. Changed contacts, coordinates, or shell void
the affected S0 and S3 observations.

### Phase 1, rounds 1 to 3 (2026-09-17)

**Order 1 files exist; packing and a real cell still wait on Rolf.**
Rounds 1 to 3 left the order 1 solids, renders and drawing in
`docs/fab/cad/v1/`, interface version 2 in `docs/fab/interface.md`,
measurement and order sheets in `docs/fab/measure.md`,
`docs/fab/order1.md` and `docs/fab/orders.md`, the contacts kit with
drawings in `docs/fab/contacts.md`, the frozen dry-test protocol in
`docs/fab/montage.md`, and the packing sheet in
`docs/fab/packing-options.md`.

Decisions after the plan live in one place:
`docs/fab/open-questions.md`. The plan stays the spec. Where a review
disagrees on a number, that file records the reading the build follows
until Rolf rules.

Three facts changed the design's shape.

A crimp ring lug does not end under its pad. The drawings are in
`docs/fab/contacts.md` §8.

Only the 3 mm wider body closes the packing on that lug, pending Rolf.
The layouts are in `docs/fab/packing-options.md`.

No published cell pack fits folded, so the plan's hand fold stands until
a cell is measured. The SKUs that were read are in
`docs/fab/interface.md` §5.

## Open questions

1. ~~Does the owner's voluntary auricular control include each ear
   independently, or sustained holds versus twitches?~~ Answered
   2026-08-13: both ears independently and together, twitch through
   sustained hold with graded levels between. The symbol space is rich;
   what remains is measuring how reliably the decoder separates the
   distinctions the owner can produce.
2. Can the owner produce a tensor tympani rumble at all? Stage C answers
   this with the pressure sensor if self-testing stays inconclusive.
3. Exact microcontroller and ADC for Stage B (the bench stage is
   deliberately module-based and forgiving). Pointed 2026-09-16: L4
   (`docs/fab/L4-pod.md`) picks the Raytac MDBT50Q-1MV2 (nRF52840) for
   the custom board and the TI ADS1292 as the front-end ADC. Status
   2026-09-17, electronics fit: WP6 ran the packing options against the
   real lug; the result is in `docs/fab/packing-options.md`. The pick is
   Rolf's (Q20).
4. Dry-electrode contact geometry behind the ear, where skin curvature
   is tighter than the forearm geometries in the cited papers. Constrained
   by the fabrication route chosen below. Status 2026-09-17: the plan
   §3.3 defaults stand until WP7a part 2, which waits on the Stage A
   parts (`docs/fab/montage.md` §1). The reference site is checked when
   the gauge is worn (Q17).
