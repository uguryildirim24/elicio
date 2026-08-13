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
outsourced PCB in a printed behind-ear shell with printed carbon-TPU
electrode contacts and a small battery plus BLE microcontroller. Exit
criteria: re-donned on three separate days with the detector threshold
unchanged, false-positive rate measured during eating, talking, and walking.

**Stage C - sealed canal tip.** A printed canal tip sealing a MEMS pressure
sensor (barometry, per the EarSwitch method) plus a piezo contact mic.
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
   deliberately module-based and forgiving).
4. Printed-electrode contact geometry behind the ear, where skin curvature
   is tighter than the forearm geometries in the cited papers.
