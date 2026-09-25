# Montage procedure and frozen dry-test protocol (WP7a part 1)

For the Stage B behind-the-ear pod. Plan `docs/fab/plan.md` §3.3, §3.4,
§3.7 item 9, §4, §6, §9 rows 7a and 7b, §10. Requirements from
`docs/EARPIECE_DESIGN.md`; bands from `docs/fab/L3-contacts.md`; the bench
is `docs/STAGE_A_PARTS.md`.

How to read the criteria. A number marked **Quoted** appears verbatim in
the named file, and the quote is given. A number marked **PROPOSED** has no
source; the line gives the rationale and what would settle it. Nothing
here is measured.

## 1. Status

- No data exists. No bench, gel or dry-contact recording is in the
  repository.
- Criteria frozen on 2026-09-17, before any dry-contact data (plan §9 row
  7a: "criteria frozen before any dry data"). Review r2 corrected the
  sources and PROPOSED tags on the same day, before any data.
- A PROPOSED number may be changed once, from Stage A gel recordings, before
  the first dry-contact recording, with a dated row in §7. After the first
  dry-contact recording, any change to §3 voids the S1 entry.
- Part 2, the bench measurement, runs when the Stage A parts
  (`docs/STAGE_A_PARTS.md`) exist. Buying them is Rolf's call (plan §10
  Open for Rolf item 8).

## 2. Montage bench procedure

### 2.1 Coordinates and landmarks

Positions are body-frame path coordinates (plan §3.2): `s` is arc length
from the hook root O along the body, `u` is the posterior offset from the
body's anterior edge (u = 0), both in millimetres.

| Point | u | s | Source |
|---|---|---|---|
| CONTACT_1 | 5.9 | 22.0 | plan §3.3 |
| CONTACT_2 | 10.4 | 33.1 | plan §3.3: contact 1 + 12.0 at 22° |
| CONTACT_REF | 8.5 | 43.0 | plan §3.3 |

Landmarks Rolf measures (plan §3.4):

| No. | What | Plan §3.4 "How" | Used here for |
|---|---|---|---|
| M6 | Mastoid offset | "Crease to the bony bump behind the lower ear" | whether CONTACT_REF sits on bone |
| M7 | Crease top to mid-concha | "Along the crease to the canal-opening level" | whether CONTACT_1 sits at the PAM level |

M6 and M7 are recorded, not CAD drivers (plan §3.3). At the default M6 of
15, a reference 8.5 mm behind the body's front edge lands about 6.5 mm in
front of the bony bump if the front edge lies in the crease. Part 2 checks
this by touch (§2.2 step 6) and records the offset; see §6.

### 2.2 Marking the positions on the skin

The plan's method is plan §3.7 item 9: "Mark dome positions on the skin,
photograph; input to WP7a." The gauge sets where the domes actually sit, so
its marks win over any caliper reading.

1. Clean the skin behind the ear with 70 % isopropanol and let it dry (plan
   §6).
2. Put on the full p15 gauge from order 1 as in plan §3.7. With it seated,
   press a washable skin marker to each of the three domes through the gap
   under the body, or dab marker ink on each dome and seat the gauge once
   so the domes print on the skin.
3. Remove the gauge. Photograph the marks from the side and from behind,
   with a millimetre ruler laid along the crease in the frame.
4. Cross-check with a caliper. Measure along the crease from the top
   attachment to the level of mark 1 (compare with CONTACT_1 s 22.0 and
   with M7), then straight back from the crease to each mark (compare with
   u, remembering u starts at the body's front edge, not at the crease).
   Record both numbers per mark; do not move the marks.
5. Check the pair: the distance between marks 1 and 2 should be about 12
   mm (plan §3.3 CONTACT_PITCH) and the line between them about 22° off the
   crease (PAIR_ANGLE). Record the measured values.
6. Press on mark 3 (reference). Record whether it lies on bone or on soft
   tissue, and the distance from it to the bony bump M6 names.

If there is no gauge yet, mark from the caliper numbers in step 4 and say
so in the record; those marks are provisional until the gauge marks exist.

### 2.3 Gel-electrode montage: the plan's pair versus L3's pair

Two configurations on the Stage A bench, same reference, same session:

| | A: plan pair | B: L3 horizontal pair |
|---|---|---|
| Signal 1 | mark 1 (u 5.9, s 22.0) | 8.0 mm straight back from the crease, level with the ear canal opening |
| Signal 2 | mark 2 (u 10.4, s 33.1) | 12.0 mm straight back from B signal 1 |
| Pitch | 12.0 | 12.0 |
| Orientation | 22° off the body axis | across the crease |
| Reference | mark 3 | mark 3 |
| Fits the shell | yes, plan §3.3 | no: plan §2 row 8, "A 17 mm face cannot hold a horizontal pair" |

Configuration B follows L3 §2.2: signal contact 1 "Sits over the muscle
belly, roughly 8–10 mm posterior to the retroauricular crease at the
vertical midpoint of the ear (level with the external auditory canal
aperture)"; contact 2 "Placed 12–15 mm posterior to Contact 1 along the
horizontal axis". B takes the low ends, 8.0 and 12.0, so its pitch equals
the plan's and the two configurations differ only in site and angle. L3 puts the reference on
"The **inferior tip of the mastoid process**"; both configurations use
mark 3 instead, because the plan's reference is on the tail (plan §2 row
8), so only the signal pair changes.

Electrodes are the Dealmed pre-gelled Ag/AgCl pads in
`docs/STAGE_A_PARTS.md`. Two 35 mm pads overlap at a 12 mm pitch. Cut the
foam so the pads do not overlap, keeping each gel disc whole, and check
that the two signal gels do not touch on the skin; touching gels short the
pair. If the gel discs cannot sit 12 mm apart without touching, record the
smallest pitch at which they do not and run both configurations at that
pitch. (PROPOSED procedure: the parts list gives "35 mm" but not the gel
disc size.)

Order: five deliberate contractions on B, then five on A, then five on B
again, so fatigue shows as a B-to-B drop. Acceptance of A for Stage B:
A's median flex amplitude is at least 70 % of B's, and A passes §3.2 and
§3.3. **PROPOSED:** 70 %. Rationale: the shell cannot hold B, so A only has
to keep enough of the signal to pass §3 on its own; a loss above 30 % would
eat most of the margin between L3's 50 µV lower bound and the 45 µV
criterion. Settles it: the A-versus-B ratio from Stage A gel recordings.

### 2.4 Stage A bench settings

From `docs/EARPIECE_DESIGN.md` "Stage A circuit design", which gives the
chain as:

```text
electrodes -> series R + clamps -> instrumentation amp (G~10)
  -> high-pass ~20 Hz -> gain stage (G 10..100, trimmable)
  -> low-pass ~500 Hz -> level shift to ADC mid-rail
  -> ADC -> microcontroller -> one ASCII sample per line -> elicio scope
```

The record's chain has "three skin contacts (two signal over the muscle,
one reference on the mastoid or another bony site)". The two signal leads
go to the amplifier's two inputs. The record does not say where the
reference lead lands; wire it as the Stage A schematic does and record it.

| Block | Design record says | Parts list |
|---|---|---|
| Protection | "220 kOhm series per lead + diode clamps to rails" | 220k resistors; onsemi 1N4148 |
| First gain | "INA128 (or AD8226)", "Gain 10 (Rg = 5.6 kOhm)" | TI INA128P; 5.6k |
| High-pass | "Passive RC, 100 nF + 82 kOhm", "~19 Hz corner" | 1/(2π · 82 kΩ · 100 nF) = 19.4 Hz |
| Second gain | "Non-inverting op-amp (half a TL072)", "Gain 11 to 101 via trimmer" | TI TL072CP; Bourns 3296W 100 kΩ |
| Low-pass | "Sallen-Key, 22 kOhm with 22 nF / 10 nF", "~490 Hz corner" | 22k; 22 nF, 10 nF |
| Supply | "Two 9 V batteries for a +/-9 V bench rail" | 9 V alkaline, snap clips |
| Level shift | "Divider to ADC mid-rail through a coupling cap", "ADC sees 0 to 3.3 V centered at half rail" | – |
| ADC | "ADS1115 breakout at 860 SPS" | Adafruit 1085 |
| Microcontroller | one ASCII sample per line | Espressif ESP32-DEVKITC-32E |

Serial and software, from the design record "Stream protocol and software
bridge" (Linux form; on macOS the port is `/dev/cu.usbserial-*` and `stty`
takes `-f` instead of `-F`):

```bash
stty -F /dev/ttyUSB0 raw -echo 115200
.venv/bin/elicio scope --input /dev/ttyUSB0 --sample-rate 860 --offset 2048 --gain 0.001
```

The design record's `--offset 2048 --gain 0.001` are its starting values;
record the ones used.

### 2.5 What is recorded per trial

1. Date, time, configuration (A or B), which marks, pitch used, trimmer
   setting (total gain), and the `elicio scope` threshold.
2. The raw stream, kept as the permanent record ("Keep raw sensor data and
   timestamps as the permanent source record", `docs/CLAUDE_SCIENCE_HANDOFF.md`
   "Safety and authority"):

   ```bash
   .venv/bin/elicio capture --input /dev/ttyUSB0 --sample-rate 860 --offset 2048 --gain 0.001 \
       --seconds 60 --site "A mark1-mark2 ref mark3" --note "trial 01, rest then 5 flexes" \
       --out recordings/montage/2026-MM-DD-A-trial01.json
   ```

   Files are never edited or deleted.
3. Per block: rest (face relaxed, 60 s), deliberate auricular twitch,
   deliberate hold of at least 1 s, firm teeth clench, and the §3.4 and
   §3.6–§3.10 activities. For each, peak-to-peak amplitude referred to the
   input (µV) and the envelope mean.
4. No on-body impedance or resistance measurement. Plan review turn 02
   finding 7: "any on-body impedance test needs its own reviewed safe
   method, not an ordinary mains-connected meter". None is reviewed yet.

### 2.6 The coordinates S1 needs

Plan §9 S1 entry requires "7a coordinates and frozen protocol". Part 2
outputs exactly three body-frame points, to 0.1 mm, with the photo file
names they came from:

| Output | Default | Comes from |
|---|---|---|
| CONTACT_1 (u, s) | (5.9, 22.0) | gauge mark 1, confirmed by configuration A passing §2.3 |
| CONTACT_2 (u, s) | (10.4, 33.1) | gauge mark 2 |
| CONTACT_REF (u, s) | (8.5, 43.0) | gauge mark 3 and the step 6 bone check |

If configuration A passes and the marks agree with the defaults, the
defaults are the output. Any other value is an interface change: it bumps
`docs/fab/interface.md`, re-runs WP2's checks (including
`keepout_clearances`, which fails a keep-out that reaches the rib or a
wall), and repeats the affected plan §3.7 items (plan §9). There is no
pre-approved window.

## 3. Frozen dry-test protocol

Run at S3 on the assembled Stage B pod with dry titanium contacts, same
bench chain as §2.4 unless the Stage B board replaces it. Amplitudes are
referred to the input. "Rest" is §3.1's recording.

| # | Test | Pass | Status |
|---|---|---|---|
| 3.1 | Resting noise, 20–490 Hz | ≤ 5 µV RMS | PROPOSED |
| 3.2 | Deliberate auricular flex | ≥ 45 µV pk-pk and ≥ 3:1 over rest pk-pk | PROPOSED |
| 3.3 | Firm teeth clench | ≥ 150 µV pk-pk; ≥ 10:1 over rest; ≥ 3:1 over the §3.2 flex | 150 from L3 range, 10:1 PROPOSED, 3:1 quoted |
| 3.4 | Jaw motion, 10 open-close-side cycles | 0 dropouts; INA128 output shift ≤ ±0.5 V | PROPOSED |
| 3.5 | Re-donning on 3 separate days, threshold unchanged | ≥ 9 of 10 flexes detected each day | 3 days quoted, 9/10 PROPOSED |
| 3.6 | Eating, 5 min | ≤ 0.20 false flex events/min | PROPOSED |
| 3.7 | Talking, 5 min reading aloud | 0 false flex events | PROPOSED |
| 3.8 | Walking, 5 min | 0 false flex events | PROPOSED |
| 3.9 | Three yawns | 0 confirmation pairs; 0 actions above NONE | yawns quoted, counts PROPOSED |
| 3.10 | Five wide smiles, five hard blinks | ≤ 1 of 5 NONE triggers per set; 0 above NONE | smiles quoted, counts PROPOSED |

### 3.1 Resting noise

Pass: ≤ 5 µV RMS in 20–490 Hz over 60 s at rest.

- **PROPOSED:** 5 µV RMS. Rationale: L3 §1 puts voluntary contraction at
  "**50–350 µV peak-to-peak**" and involuntary twitches at "**2–15 µV**";
  5 µV RMS (about 30 µV pk-pk for Gaussian noise) leaves the flex criterion
  visible above rest. Settles it: Stage A gel rest recordings at the plan
  positions.
- Band: the chain's corners, "~19 Hz" and "~490 Hz" (design record, Stage A
  circuit design).

### 3.2 Deliberate auricular flex

Pass: median of 10 flexes ≥ 45 µV pk-pk, and ≥ 3 times the rest pk-pk.

- **PROPOSED:** 45 µV. Rationale: 10 % under the lower end of L3 §1,
  "Voluntary auricular muscle contractions generate surface EMG amplitudes
  of **50–350 µV peak-to-peak**", which is for wet electrodes; dry contacts
  are not expected to do better. Settles it: configuration A gel
  amplitudes (§2.3).
- **PROPOSED:** 3:1. Rationale: the single flex maps only to `RiskLevel.NONE`
  (design record, "A single auricular flex maps only to `RiskLevel.NONE`
  actions (floor 0.60)"), so a modest margin is enough. Settles it: the
  detector's hit rate at that ratio in Stage A replays.

### 3.3 Firm teeth clench

Pass: median of 10 clenches ≥ 150 µV pk-pk, ≥ 10 times rest pk-pk, and ≥ 3
times the §3.2 flex median.

- 150 µV: the lower end of the masseter row in L3 §2.3, "| **Masseter** |
  Clenching teeth, biting | 150–600 µV |" (temporalis: "200–800 µV"). Using
  the range's lower end as a pass bound is this protocol's choice.
- **PROPOSED:** 10:1. Rationale: clench confirms `DANGEROUS` actions at
  0.85 (below), so it needs a wider margin than the flex. Settles it: Stage
  A gel clench recordings.
- 3:1, quoted: plan §2 row 9, "Clench is 3–5× a flex on the same pair".

### 3.4 Jaw motion

Pass, over 10 cycles of open, close and side-to-side chewing motion with an
empty mouth: no dropout, and the INA128 output (gain 10) moves by no more
than ±0.5 V from its rest level.

- The requirement is quoted: plan §9 row 7a, "dropout under jaw motion";
  plan review turn 02 finding 7, "saturation/dropout".
- **PROPOSED:** dropout means the ADC reading at either end of its range,
  or a flat trace, for more than 100 ms. Rationale: longer than one flex
  onset, so a dropout can hide a command. Settles it: the detector's
  onset window in `elicio scope`.
- **PROPOSED:** ±0.5 V at the INA128 output (±50 mV at its input).
  Rationale: the high-pass blocks a slow shift from later stages, but a
  step that large drives the second stage (gain up to 101) to its rails
  during the transient. Settles it: shifts seen on the gel bench during the
  same motion.

### 3.5 Re-donning on three days

Pass: on each of 3 separate days, take the pod off and put it back on, and
at least 9 of 10 deliberate flexes are detected, with no change to the
threshold or the trimmer between days.

- Quoted: design record, Stage B exit criteria, "re-donned on three
  separate days with the detector threshold unchanged".
- **PROPOSED:** 9 of 10. Rationale: matches the 90 % bar the project uses
  for its gesture milestone, "Milestone 1 is 5 to 8 gestures at 90 percent
  or better cross-session accuracy" (`docs/CLAUDE_SCIENCE_HANDOFF.md`,
  "Established research results"); that milestone is for classification,
  not this detector. Settles it: Stage A replays of repeated sessions.

### 3.6 Eating

Pass: over 5 minutes of chewing solid food, ≤ 0.20 false flex events per
minute (at most 1 in 5 minutes).

- The test is quoted: design record, Stage B exit criteria,
  "false-positive rate measured during eating, talking, and walking".
- **PROPOSED:** 0.20/min. Rationale: chewing drives the masseter and
  temporalis next to the pair, and a false single flex can only reach
  `RiskLevel.NONE`. Settles it: eating recordings at S3.

### 3.7 Talking

Pass: 5 minutes reading aloud at normal volume, 0 false flex events.

- The test is quoted (§3.6).
- **PROPOSED:** 0 in 5 minutes. Rationale: the design record says "The
  auricular muscles are functionally near-silent in daily life, which
  gives the primary command channel a low background false-positive
  rate". Settles it: talking recordings at S3.

### 3.8 Walking

Pass: 5 minutes of brisk walking, 0 false flex events.

- The test is quoted (§3.6).
- **PROPOSED:** 0 in 5 minutes, same rationale as §3.7. Settles it: walking
  recordings at S3.

### 3.9 Yawning

Pass: over three full yawns, no flex-plus-clench pair inside the
confirmation window, and no action above `RiskLevel.NONE` executed.

- Quoted: design record, "known cross-talk sources (yawning, wide smiles)
  must appear in the false-positive test plan"; "three yawns" is the count
  in plan §3.7 item 2.
- Quoted: design record, "`DANGEROUS` keeps its two-event, two-muscle-group
  rule: auricular command plus masseter clench confirmation at 0.85 within
  the existing window"; `src/elicio/harness/policy.py`
  `CONFIRM_CONFIDENCE_FLOOR = 0.85` and `CONFIRM_WINDOW_S = 3.0`.
- **PROPOSED:** 0 pairs and 0 actions above NONE. Rationale: a yawn opens
  the jaw and can look like flex then clench, which is exactly the
  `DANGEROUS` pattern. Settles it: yawn recordings at S3.

### 3.10 Wide smiles and hard blinks

Pass: in five wide smiles and in five hard blinks, at most 1 of 5 triggers
a `RiskLevel.NONE` flex event per set, and none triggers anything above
NONE.

- Quoted: "wide smiles" (design record, §3.9 quote). L3 §2.3, facial
  mimicry: "| **Facial Mimicry (Orbicularis Oculi/Zygomaticus)** | Hard
  blinks, smiling, squinting | 50–150 µV |".
- Quoted: floors in `src/elicio/harness/policy.py`, `RiskLevel.NONE: 0.60`,
  `RiskLevel.REVERSIBLE: 0.75`, `RiskLevel.DANGEROUS: 0.85`.
- **PROPOSED:** ≤ 1 of 5 and 0 above NONE. Rationale: L3's mimicry band
  overlaps the flex band, so some NONE triggers are expected; anything
  above NONE needs a patterned gesture or a confirmation. Settles it: smile
  and blink recordings at S3.

## 4. Session rules

### 4.1 What each release state allows

From plan §9 "Release states":

| State | Plan "Allowed" | For this protocol |
|---|---|---|
| S0 gauge | "passive wear per 3.7" | passive gauge wear only; the gel bench of §2 is Stage A, not a Stage B state |
| S1 order 2 | "purchase of shells and hardware" | passive gauge wear continues; no wear of Stage B contacts |
| S2 assembled | "bench only" | no wear |
| S3 validation wear | "only the sessions 7a prescribes, ≤ 4 h/day" | only the §3 sessions, at most 4 hours of wear per day |
| S4 routine use | "daily wear; decoder mapping promotion per the design record" | entry needs every §3 criterion passed |

### 4.2 Skin checks and stop rules

1. Look at the skin behind the ear before every session. Do not wear on
   broken or irritated skin.
2. Plan §3.7 item 3: "remove at once on pain, numbness, or skin reaction
   and record it; a red mark over 15 minutes after removal fails that
   variant."
3. Look again after removal and at 15 minutes; photograph any mark.

### 4.3 Cleaning

Plan §6: "Cleaning: 70 % isopropanol, air dry; no acetone." Plan §4:
"70 % isopropanol wipe after each wear".

### 4.4 Electrical safety

1. Stage A: `docs/STAGE_A_PARTS.md`, "Everything touching skin runs from
   the 9 V batteries only. Never connect mains-powered equipment to the
   electrode side; during tethered debugging the laptop runs on battery.
   The 220 kOhm series resistors and clamp diodes go in before the first
   electrode is ever worn."
2. Stage B: plan §6, "Battery-only: no connector, no port; charging off the
   ear, lid removed. "Never charge while worn" is procedural, on the
   assembly sheet. Tethered bring-up: side exit, laptop on battery, plug
   back before wear."
3. Stage B protection: plan §4, "each pad feeds its own 220 kΩ resistor
   and clamp within 10 mm".

## 5. Results

Headings only. Nothing is written here before part 2. After the first
dry-contact recording, any change to §3 voids the S1 entry (§1).

### 5.1 Resting noise

### 5.2 Deliberate auricular flex

### 5.3 Firm teeth clench

### 5.4 Jaw motion

### 5.5 Re-donning on three days

### 5.6 Eating

### 5.7 Talking

### 5.8 Walking

### 5.9 Yawning

### 5.10 Wide smiles and hard blinks

### 5.11 Montage A versus B and the three coordinates

## 6. Inputs to other packages

- **WP7b** measures the real stack on the bench (force, travel,
  continuity) and runs §3 at S3 under §4. It passes or fails against §3
  only (plan §9 row 7b).
- **WP8** takes the three coordinates of §2.6. If CONTACT_REF is not on
  bone at Rolf's M6 (§2.2 step 6), WP8 gets that offset as an open
  question, not a silent move.
- **WP6** takes nothing unless §2.6 moves a contact; then the keep-outs,
  lug tabs and lead pads in `docs/fab/interface.md` move with it.

## 7. Change log

| Date | Change |
|---|---|
| 2026-09-17 | First issue (WP7a part 1). |
| 2026-09-17 | Review r2, before any data: quotes checked against their files; numbers without a verbatim source tagged PROPOSED; configuration B and the reference choice sourced; gel-pad overlap and the on-body meter step removed; `elicio` commands corrected; coordinate window struck. |

## 8. Protocol v2 mapping (WP13)

Measurement path on the ADS1292 worn chain (plan v2 §6). Amplitudes are
input-referred µV using the nominal scale in `docs/fab/frame-v2.md`
(metadata only). That is an explicit decision to apply the v1 numbers to
this transfer function. It is not a claim that the INA128 bench and this
chain are the same.

Digital band-pass for noise and pk-pk lines: Butterworth order 4, band
20 Hz to 490 Hz, zero-phase `sosfiltfilt`, fs = 2000 Hz. Rest RMS window:
the full 60 s record after start-up exclusions. Flex and clench pk-pk
window: 2.0 s starting at the cue.

Dropout on this chain: rail or a flat trace for more than 200 sample
intervals at 2000 SPS (100 ms). Counted on the acquisition stream
(`acq_index` and the sample bytes). A gap in `frame_seq` is transport
loss. Report it beside dropout. Do not substitute it for dropout.

Start-up exclusions (not scored): HELLO; STREAM with N = 0; any sample
with INVALID; any interval with VBUS streaming refused; the first 200
conversions after a RESTART flag (rail and reference settle); OVERRUN
gaps (those conversions were not stored).

Input headroom and common-mode headroom are separate from the shift
line. Both are **open: needs S2 data**.

| # | v1 pass | Mapping |
|---|---|---|
| 3.1 | Resting noise, 20–490 Hz, ≤ 5 µV RMS | revised: same number, on the digital band-pass above, input-referred from ADS1292 codes. Not a claim the analog noise matches the INA128 bench. |
| 3.2 | Deliberate auricular flex ≥ 45 µV pk-pk and ≥ 3:1 over rest pk-pk | revised: same numbers, same filter and 2.0 s window, input-referred. |
| 3.3 | Firm teeth clench ≥ 150 µV pk-pk; ≥ 10:1 over rest; ≥ 3:1 over the §3.2 flex | revised: same numbers, same filter and 2.0 s window, input-referred. |
| 3.4 | 0 dropouts; INA128 output shift ≤ ±0.5 V | revised: dropout is the original rule, 200 sample intervals, on the acquisition stream, with transport loss reported beside it. Shift restated as ± 50 mV input-referred (± 0.5 V at gain 10) on the DC-preserving path (raw codes, no high-pass) relative to rest. Input headroom and common-mode headroom separately: open: needs S2 data. |
| 3.5 | Re-donning on 3 days, threshold unchanged, ≥ 9 of 10 flexes detected each day | same criterion (detector hits, not ADC scale). |
| 3.6 | Eating, 5 min, ≤ 0.20 false flex events/min | same criterion. |
| 3.7 | Talking, 5 min, 0 false flex events | same criterion. |
| 3.8 | Walking, 5 min, 0 false flex events | same criterion. |
| 3.9 | Three yawns: 0 confirmation pairs; 0 actions above NONE | same criterion (harness). |
| 3.10 | Five wide smiles, five hard blinks: ≤ 1 of 5 NONE triggers per set; 0 above NONE | same criterion (harness). |

Lines 3.1 to 3.3 (noise, flex and clench numbers) are scored by the
analysis pipeline after the session; `receive-check` stops only on the
same-criterion lines 3.5 to 3.10 (Q96).

The bench montage procedure in §2 is re-targeted to the board on its
stand with the plan v2 §5.6 leads when that board exists. No dry data
was judged against this table.
