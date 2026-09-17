# Elicio Stage B Earpiece — Montage Procedure and Frozen Dry-Test Protocol (WP7a Part 1)

This document establishes the anatomical electrode montage procedure and freezes the quantitative electrophysiological acceptance criteria for the Elicio Stage B behind-the-ear (BTE) pod.

This specification serves the requirements in `docs/EARPIECE_DESIGN.md` ("Staged build plan", "Harness mapping and false-positive budget", "Requirements"), `docs/CLAUDE_SCIENCE_HANDOFF.md` ("Established research results", "Safety and authority"), `docs/fab/L3-contacts.md` (montage, PAM pair, SNR band, mastoid reference), `docs/STAGE_A_PARTS.md`, and `docs/fab/plan.md` (§3.3, §3.4, §3.7 item 9, §4, §6, §9 rows 7a and 7b, §10).

---

## 1. Status Line

*   **Protocol Status:** FROZEN on 2026-09-17 before the acquisition of any dry-electrode data.
*   **Data State:** Zero empirical bench or dry-contact experimental data exists in this repository.
*   **Execution Gate:** Stage A parts (`docs/STAGE_A_PARTS.md`) have not been purchased. This package (Part 1) writes the frozen protocol and montage procedure. Part 2 (bench acquisition and quantitative execution) runs when Stage A parts exist.

---

## 2. Montage Bench Procedure

### 2.1 Anatomical Landmarks and Marking on Skin

The retroauricular target is the posterior auricular muscle (PAM), which originates from the mastoid portion of the temporal bone and inserts into the ponticulus of the cranial conchal surface.

Anatomical reference coordinates use the caliper parameters defined in plan §3.3, §3.4, and `docs/fab/measure.md`:
*   **Retroauricular Crease:** The natural groove between the pinna cartilage and the temporal cranium. Defines arc path parameter $s$, with $s = 0.0\text{ mm}$ at the superior helix attachment root (hook root level).
*   **Crease Arc Length ($M_2$):** String distance along the crease from superior attachment to the inferior lobule attachment fold (typical 50–65 mm; default 58.0 mm).
*   **Ear Root Length ($M_1$):** Straight-line attachment chord (typical 45–58 mm; default 52.0 mm).
*   **Mid-Concha Level ($M_7$):** Distance along the crease from $s = 0.0\text{ mm}$ to the vertical midpoint of the conchal bowl, level with the external auditory canal aperture (typical 18–26 mm; default 22.0 mm).
*   **Mastoid Offset ($M_6$):** Distance from the retroauricular crease to the lateral bony surface of the mastoid process behind the lower ear (typical 12–18 mm; default 15.0 mm).

```
                      [ RETROAURICULAR SKIN LANDMARKS ]

   s = 0.0 mm ---------------------------------------- [ Superior Attachment / Hook Root ]
                          \
                           \  Retroauricular Crease (s axis)
                            \
   s = 22.0 mm (M7 level) ---+--- u = 5.9 mm -------- ( CONTACT_1: Anterior PAM belly )
                              \            \
                               \            \ 12.0 mm pitch at 22° pair angle
                                \            \
   s = 33.1 mm ------------------+--- u = 10.4 mm ---- ( CONTACT_2: Posterior PAM belly )
                                  \
                                   \
   s = 43.0 mm ---------------------+--- u = 8.5 mm -- ( CONTACT_REF: Mastoid Bony Surface )
                                    |
                           [ Inferior Mastoid Tip / SCM insertion ] (Avoid muscular tendon)
```

#### Skin Marking Step-by-Step Procedure

1.  **Skin Preparation:** Degrease the retroauricular groove, helix root, and mastoid skin with a 70% isopropanol wipe for 15 seconds. Allow the skin to air dry for 1 minute.
2.  **Crease Arc Tracing:** Using a sterile gentian violet surgical marker or fine-point dermographic pencil, trace the retroauricular crease from $s = 0.0\text{ mm}$ (superior attachment) downward.
3.  **Landmark $M_7$ Identification:** Locate the horizontal plane passing through the center of the external auditory canal aperture. Measure along the crease to locate $s = 22.0\text{ mm}$.
4.  **Contact 1 Marking:** At $s = 22.0\text{ mm}$, measure perpendicular (normal) to the crease posteriorly by $u = 5.9\text{ mm}$. Mark the skin coordinate **CONTACT_1** $(u=5.9,\, s=22.0)$.
5.  **Contact 2 Marking:** Measure along the crease to $s = 33.1\text{ mm}$. Measure perpendicular to the crease posteriorly by $u = 10.4\text{ mm}$. Mark the skin coordinate **CONTACT_2** $(u=10.4,\, s=33.1)$.
    *   *Verification:* Center-to-center Euclidean distance between Contact 1 and Contact 2 must equal $\sqrt{(10.4 - 5.9)^2 + (33.1 - 22.0)^2} = \sqrt{4.5^2 + 11.1^2} = 11.98 \approx 12.0\text{ mm}$, inclined at an angle of $\arctan(4.5 / 11.1) = 22.07^\circ \approx 22^\circ$ relative to the crease tangent.
6.  **Contact Reference Marking:** Locate the flat lateral bony surface of the mastoid process ($M_6 \approx 15\text{ mm}$ posterior to the lower crease fold, superior to the sternocleidomastoid tendon insertion). Mark the skin coordinate **CONTACT_REF** at $u = 8.5\text{ mm}$, $s = 43.0\text{ mm}$.
7.  **Photographic Record:** Photograph the marked skin from side and posterior views with a millimeter scale aligned along the crease (fulfilling plan §3.7 item 9).

---

### 2.2 Gel-Electrode Montage: Plan's Pair vs. L3's Pair

During Stage A bench bring-up, two electrode configurations are compared using clinical disposable Ag/AgCl snap electrodes (Dealmed 35 mm, trimmed to 15 mm circular footprints to fit the retroauricular groove without edge overlap):

| Parameter | Configuration A: The Plan's 22° Angled Pair | Configuration B: L3's Strictly Horizontal PAM Pair |
| :--- | :--- | :--- |
| **Contact 1 Position** | $u = 5.9\text{ mm}$, $s = 22.0\text{ mm}$ (Anterior PAM belly) | $u = 8.0\text{ mm}$, $s = 22.0\text{ mm}$ (Anterior PAM belly) |
| **Contact 2 Position** | $u = 10.4\text{ mm}$, $s = 33.1\text{ mm}$ (Posterior PAM / mastoid transition) | $u = 21.0\text{ mm}$, $s = 22.0\text{ mm}$ (Posterior mastoid crest insertion) |
| **Inter-Electrode Distance**| **12.0 mm** center-to-center | **13.0 mm** center-to-center |
| **Montage Orientation** | **22° inclined** relative to body path | **0° (strictly horizontal)** perpendicular to crease |
| **Reference Position** | $u = 8.5\text{ mm}$, $s = 43.0\text{ mm}$ (Mastoid bone) | $u = 8.5\text{ mm}$, $s = 43.0\text{ mm}$ (Mastoid bone) |
| **Mechanical Feasibility** | **Fits in 17 mm BTE shell:** Maximum cavity span $u = 1.5\text{ to } 15.5\text{ mm}$. | **Cannot fit in BTE shell:** Requires $u \ge 21.0\text{ mm}$ ($> 17\text{ mm}$ total body width). |
| **Bench Role** | Target production geometry for Stage B. | Physiological ceiling benchmark for horizontal PAM fiber orientation. |

*Protocol Comparison:* The bench test records 5 trials of deliberate contraction on Configuration B, then 5 trials on Configuration A. Configuration A is accepted for Stage B if its contraction amplitude reaches $\ge 70\%$ of Configuration B while maintaining the required clench separation.

---

### 2.3 Stage A Bench Settings

All bench tests use the single-channel hardware chain specified in `docs/EARPIECE_DESIGN.md` ("Stage A circuit design") and `docs/STAGE_A_PARTS.md`:

```
   [ Electrodes ]
   Active 1 (+) ---[ 220k ]---+---( INA128P )
                              |    Gain = 10
   Active 2 (-) ---[ 220k ]---+   (Rg = 5.6k)
                              |        |
   Ref (Mastoid) --[ 220k ]---+        v
                              |    [ Passive High-Pass ]
                            Diodes (100nF + 82k, fc = 19.4 Hz)
                           to rails    |
                                       v
                                   [ Second Gain Stage ]
                                   (TL072CP, G = 11 to 101)
                                       |
                                       v
                                   [ Sallen-Key Low-Pass ]
                                   (22k, 22nF/10nF, fc = 490 Hz)
                                       |
                                       v
                                   [ Level Shift to 1.65 V ]
                                       |
                                       v
                                   [ Adafruit 1085 ADS1115 ] (860 SPS)
                                       |
                                       v  (I2C)
                                   [ ESP32 Microcontroller ]
                                       |
                                       v  (USB UART, 115200 baud)
                                  .venv/bin/elicio scope
```

*   **Lead Protection:** Each electrode lead contains a $220\text{ k}\Omega$ 1% metal film series resistor and 1N4148 diode clamps to the $\pm 9\text{ V}$ rails.
*   **Instrumentation Amplifier:** Texas Instruments INA128P (8-DIP) with gain resistor $R_g = 5.6\text{ k}\Omega \pm 1\%$, setting first-stage gain $G_1 = 1 + (50\text{ k}\Omega / 5.6\text{ k}\Omega) = 9.93 \approx 10$.
*   **High-Pass Filter:** Passive RC stage with $C = 100\text{ nF}$ film capacitor and $R = 82\text{ k}\Omega$ metal film resistor, setting corner frequency $f_c = 1 / (2\pi \times 82000 \times 100 \times 10^{-9}) = 19.4\text{ Hz}$.
*   **Second Gain Stage:** Texas Instruments TL072CP non-inverting amplifier with Bourns 3296W $100\text{ k}\Omega$ multi-turn trimmer and $1\text{ k}\Omega$ fixed resistor ($G_2 = 11\text{ to } 101$). Total analog gain range $G_{\text{total}} = 110\text{ to } 1010$.
*   **Low-Pass Anti-Aliasing Filter:** 2nd-order Sallen-Key active low-pass with $R_1 = R_2 = 22\text{ k}\Omega$, $C_1 = 22\text{ nF}$, $C_2 = 10\text{ nF}$, setting Butterworth corner frequency $f_c = 490\text{ Hz}$.
*   **Power Supply:** Two 9 V alkaline batteries providing isolated $\pm 9.0\text{ V}$ analog rails. Zero connection to mains earth.
*   **ADC Interface:** AC-coupled voltage divider centering signal at $+1.65\text{ V}$. Adafruit 1085 (TI ADS1115 16-bit ADC) operating at 860 SPS.
*   **Microcontroller & Protocol:** ESP32 streaming ASCII integer counts over USB UART at 115200 baud, 1 sample per line.
*   **Software Execution:** Run from `.venv` in repository root:
    ```bash
    .venv/bin/elicio scope --sample-rate 860 --offset 2048 --gain 0.001
    ```

---

### 2.4 Per-Trial Recording Protocol

For each test block, the operator records:
1.  **Electrode Impedance:** Battery-powered digital multimeter measurement of inter-electrode resistance ($R_{1-2}$, $R_{1-\text{ref}}$, $R_{2-\text{ref}}$) before and after testing.
2.  **Permanent Session Capture:** Captured using standard CLI:
    ```bash
    .venv/bin/elicio capture --output results/montage_trial_NN.json --duration 60 --sample-rate 860
    ```
    Raw samples and timestamps are preserved as the unedited source record (`docs/CLAUDE_SCIENCE_HANDOFF.md` §Safety).
3.  **Signal Amplitudes:** Peak-to-peak amplitude ($\mu\text{V}$ referred-to-input) and envelope mean across:
    *   Resting baseline (motionless, relaxed face).
    *   Voluntary deliberate PAM twitch (short pulse).
    *   Voluntary deliberate PAM hold (sustained contraction $\ge 1.0\text{ s}$).
    *   Voluntary maximal teeth clench (`jaw_clench`, masseter/temporalis).
    *   Dynamic disturbance motions (chewing, continuous talking, brisk walking, yawning, maximal smile).

---

### 2.5 Coordinate Derivation for S1 Entry Gate

The S1 entry gate (plan §9) requires frozen physical coordinates $(u_1, s_1)$, $(u_2, s_2)$, and $(u_{\text{ref}}, s_{\text{ref}})$ before purchasing Stage B shells:
1.  If bench recordings confirm that Configuration A achieves $\ge 70\%$ of Configuration B amplitude and passes all Section 3 criteria, the nominal coordinates are frozen:
    $$\text{CONTACT\_1} = (5.9\text{ mm},\, 22.0\text{ mm})$$
    $$\text{CONTACT\_2} = (10.4\text{ mm},\, 33.1\text{ mm})$$
    $$\text{CONTACT\_REF} = (8.5\text{ mm},\, 43.0\text{ mm})$$
2.  If the optimal PAM hot spot on the user's ear deviates longitudinally along the crease, $s$ may shift within the window $s_1 \in [20.0,\, 24.0\text{ mm}]$ and $s_2 = s_1 + 11.1\text{ mm}$. Any shift updates `docs/fab/interface.md` to version 2 before CAD release.

---

## 3. Frozen Dry-Test Protocol and Acceptance Criteria

Every criterion below is quantitative and numeric. Each number is traced to a quoted section in the project specifications or tagged `PROPOSED` with a rationale.

```
       [ QUANTITATIVE PASS CRITERIA BOUNDS SUMMARY ]

   +---------------------------------------+---------------------+-------------------+
   | Test Parameter                        | Numeric Threshold   | Status / Source   |
   +---------------------------------------+---------------------+-------------------+
   | 1. Baseline Noise Floor (20–490 Hz)   | <= 5.0 uV RMS       | Quoted L3 §3.1    |
   | 2. Voluntary Auricular Flex Amplitude | >= 45.0 uV pk-pk    | Quoted L3 §1 r2   |
   | 3. SNR: Auricular Flex vs. Rest       | >= 3.0 : 1 (9.5 dB) | Quoted DESIGN r60 |
   | 4. Voluntary Teeth Clench Amplitude   | >= 150.0 uV pk-pk   | Quoted L3 §2.3    |
   | 5. SNR: Clench vs. Rest               | >= 10.0 : 1 (20 dB) | Quoted L3 §2.3    |
   | 6. Clench-to-Flex Amplitude Ratio     | >= 3.0 : 1          | Quoted DESIGN §2  |
   | 7. Dropout Under Jaw Motion           | 0 dropouts (>100ms) | Quoted DESIGN StB |
   | 8. Three-Day Re-Donning Stability     | >= 9/10 (90.0%)     | Quoted HANDOFF M1 |
   | 9. False Positives: Eating (Chewing)  | <= 0.20 / min       | PROPOSED          |
   | 10. False Positives: Talking (Speech) | 0.0 / min (0 in 5m) | Quoted DESIGN FP  |
   | 11. False Positives: Walking (Gait)   | 0.0 / min (0 in 5m) | Quoted DESIGN FP  |
   | 12. Cross-Talk: Yawning Confirmation  | 0 unconfirmed runs  | Quoted DESIGN FP  |
   | 13. Cross-Talk: Smiles / Blinks       | <= 1 / 5 reps (NONE)| Quoted L3 §2.3    |
   +---------------------------------------+---------------------+-------------------+
```

---

### 3.1 Baseline Resting Noise Floor

*   **Criterion:** In the band 20 Hz to 490 Hz during motionless sitting with relaxed facial musculature, the referred-to-input (RTI) noise floor must be $\le 5.0\text{ }\mu\text{V RMS}$ (equivalent to $\le 15.0\text{ }\mu\text{V peak-to-peak}$).
*   **Source:** Quoted from `docs/fab/L3-contacts.md` §3.1 (citing Strauss et al., 2020: vestigial auriculomotor involuntary activity is 2–15 µV; resting baseline must remain $\le 5.0\text{ }\mu\text{V RMS}$ to prevent spurious threshold crossing); corroborated by `docs/EARPIECE_DESIGN.md` "Stage A circuit design" (INA128 input noise $8\text{ nV}/\sqrt{\text{Hz}}$ + $220\text{ k}\Omega$ thermal noise yields theoretical floor $< 3.0\text{ }\mu\text{V RMS}$).

---

### 3.2 Signal-to-Noise Ratio: Voluntary Auricular Flex

*   **Criterion:** Deliberate voluntary contraction of the auricular channel (`auricular_flex` / `wrist_down`) must produce a peak-to-peak amplitude $\ge 45.0\text{ }\mu\text{V}$ referred-to-input, achieving an amplitude SNR $\ge 3.0:1$ ($9.54\text{ dB}$) relative to the $\le 15.0\text{ }\mu\text{V}$ peak-to-peak baseline noise.
*   **Source:** Quoted from `docs/fab/L3-contacts.md` §1 row 2 and §3.1 (citing Rüschenschmidt et al., 2022: voluntary auricular contractions generate 50–400 µV; 45 µV represents the 90% lower bound for detection); and `docs/EARPIECE_DESIGN.md` "Harness mapping and false-positive budget" (detector confidence floor 0.60 requires contraction envelope distinctly above resting noise).

---

### 3.3 Signal-to-Noise Ratio: Jaw Clench Confirmation Channel

*   **Criterion:** Deliberate firm teeth clenching (`jaw_clench`, temporalis/masseter activation) must produce a peak-to-peak amplitude $\ge 150.0\text{ }\mu\text{V}$ referred-to-input, achieving an amplitude SNR $\ge 10.0:1$ ($20.0\text{ dB}$) relative to the $\le 15.0\text{ }\mu\text{V}$ baseline noise, and an amplitude ratio $\ge 3.0:1$ relative to the voluntary auricular flex.
*   **Source:** Quoted from `docs/fab/L3-contacts.md` §2.3 table (temporalis and masseter clench generates 150–800 µV in the retroauricular crease); and `docs/EARPIECE_DESIGN.md` "Fabrication plan §2 row 9" ("Clench is 3–5× a flex on the same pair").

---

### 3.4 Contact Continuity and Dropout Under Jaw Motion

*   **Criterion:** During 10 continuous cycles of active mastication movement (jaw lateralization, opening 15–20 mm, and closing):
    1.  Zero signal dropouts (defined as ADC clipping/saturation to rail $0\text{ V}$ or $3.3\text{ V}$, or flatline loss of signal $> 100.0\text{ ms}$).
    2.  Transient baseline DC shift at the amplifier input must not exceed $\le \pm 50.0\text{ mV}$.
*   **Source:** Quoted from `docs/EARPIECE_DESIGN.md` "Staged build plan" Stage B exit criteria ("signal continuity under jaw motion"); and `tasks/plan/turns/02-pro.md` finding 7 ("saturation/dropout under jaw motion"). PROPOSED: $\le \pm 50.0\text{ mV}$ maximum input DC shift [Rationale: Keeps differential input within linear common-mode range of INA128 at $G=10$ on $\pm 9\text{ V}$ rails; source that would settle it: bench oscilloscope measurement of half-cell potential drift during jaw motion].

---

### 3.5 Three-Day Re-Donning Stability

*   **Criterion:** The earpiece is removed and re-donned on 3 separate calendar days without adjusting the hardware gain trimmer or modifying the software detection threshold in `elicio scope`:
    *   On each day, at least 9 out of 10 ($90.0\%$) deliberate voluntary auricular flexes must trigger the detector above confidence floor $0.60$.
    *   Zero manual threshold or hardware gain recalibrations permitted across the 3 days.
*   **Source:** Quoted from `docs/EARPIECE_DESIGN.md` "Staged build plan" Stage B exit criteria ("re-donned on three separate days with the detector threshold unchanged"); and `docs/CLAUDE_SCIENCE_HANDOFF.md` "Established research results" ("Milestone 1 is 5 to 8 gestures at 90 percent or better cross-session accuracy").

---

### 3.6 False-Positive Rate: Eating (Chewing)

*   **Criterion:** During 5 minutes of continuous mastication of solid food (e.g., chewing bread or nuts), false triggers of the auricular flex detector must be $\le 0.20\text{ events per minute}$ (at most 1 false trigger across the 5-minute test).
*   **Source:** PROPOSED: $\le 0.20\text{ false triggers per minute}$ [Rationale: Allows at most 3 benign `RiskLevel.NONE` triggers during a typical 15-minute meal; source that would settle it: 3-day continuous eating wear log on the user's ear]; policy context quoted from `docs/EARPIECE_DESIGN.md` "Harness mapping and false-positive budget" ("Measured false-positive rates during eating, talking, walking, and yawning are recorded per stage before any mapping is promoted").

---

### 3.7 False-Positive Rate: Talking (Continuous Speech)

*   **Criterion:** During 5 minutes of continuous verbal reading of text aloud at normal conversational volume (60–70 dB SPL), false triggers of the auricular flex detector must be exactly $0.0\text{ events}$ ($0.0\text{ events per minute}$).
*   **Source:** Quoted from `docs/EARPIECE_DESIGN.md` "Harness mapping and false-positive budget" (covert channels must remain fully silent during conversational speech); and `docs/fab/L3-contacts.md` §2.3 (speech acoustic and mandibular vibrations produce sub-threshold far-field potentials rejected by the 19.4 Hz high-pass filter).

---

### 3.8 False-Positive Rate: Walking (Locomotion)

*   **Criterion:** During 5 minutes of continuous brisk walking on a hard surface (gait cadence 100–120 steps/minute), false triggers of the auricular flex detector must be exactly $0.0\text{ events}$ ($0.0\text{ events per minute}$).
*   **Source:** Quoted from `docs/EARPIECE_DESIGN.md` "Harness mapping and false-positive budget"; and `docs/fab/L3-contacts.md` §7.2 (heel-strike kinetic shock is absorbed by the 1.5 mm hook interference preload and filtered by the 19.4 Hz high-pass stage).

---

### 3.9 Cross-Talk Rejection: Yawning

*   **Criterion:** During 3 maximal-aperture yawning gestures:
    1.  Zero unintended actions executed.
    2.  If large facial deformation triggers the primary flex detector, it must NOT produce a secondary confirmation `jaw_clench` event at confidence $\ge 0.85$ within the $3.0\text{ s}$ confirmation window.
*   **Source:** Quoted from `docs/EARPIECE_DESIGN.md` "Harness mapping and false-positive budget" ("DANGEROUS keeps its two-event, two-muscle-group rule: auricular command plus masseter clench confirmation at 0.85 within the existing window"); and `src/elicio/harness/policy.py` (`CONFIRMATION_TIMEOUT_SECONDS = 3.0`, `CONFIRMATION_CONFIDENCE_FLOOR = 0.85`).

---

### 3.10 Cross-Talk Rejection: Facial Mimicry (Smiling and Blinking)

*   **Criterion:** During 5 maximal voluntary smiles and 5 forced hard blinks:
    *   $\le 1\text{ false trigger}$ per 5 repetitions for `RiskLevel.NONE` actions (confidence floor 0.60).
    *   Zero false triggers ($0.0\%$) for `RiskLevel.REVERSIBLE` (floor 0.75) or `RiskLevel.DANGEROUS` (floor 0.85).
*   **Source:** Quoted from `docs/fab/L3-contacts.md` §2.3 table (facial mimicry generates 50–150 µV transient spikes with fast rise time <20 ms, distinguished from deliberate sustained flexes); and `docs/EARPIECE_DESIGN.md` "Harness mapping and false-positive budget".

---

## 4. Operational Safety and Session Rules

Per plan §6, plan §9 (Release States S0–S4), and `docs/EARPIECE_DESIGN.md`:

### 4.1 Wear Limits per Release State

*   **State S0 (Fit Gauge):** Passive wear only per plan §3.7 (progression: 15 minutes, 1 hour, 4 hours). Zero electronic hardware.
*   **State S1 (Order 2):** Hardware procurement gate. Zero wear.
*   **State S2 (Assembled Pod):** Benchtop testing only. Battery-powered continuity check, leakage check, and DMG chemical spot screen. Zero human skin wear.
*   **State S3 (Validation Wear):** Human on-body wear permitted **strictly for the specific test sessions prescribed by this protocol**. Maximum wear duration must not exceed **$\le 4.0\text{ hours per calendar day}$**.
*   **State S4 (Routine Use):** Daily wear and harness mapping promotion permitted only after all Section 3 criteria pass across 3 separate days.

---

### 4.2 Skin Inspection and Immediate Stop Rules

1.  **Pre-Wear Inspection:** Examine retroauricular skin and mastoid process under direct light before donning. Do not don if abrasion, erythema, dermatitis, or skin breakdown is present.
2.  **Immediate Removal Rule:** Remove the earpiece immediately upon any sensation of sharp localized pain, pressure pinching, numbness, burning, or skin irritation.
3.  **Objective Erythema Stop Rule:** Inspect the skin immediately upon removal. Any erythema (red mark) persisting $> 15.0\text{ minutes}$ after removal fails that variant and halts further sessions until complete recovery (quoted from plan §3.7 item 3).

---

### 4.3 Hygiene and Cleaning

*   **Disinfection Cadence:** Thoroughly wipe titanium contact domes and nylon shell surfaces with a 70% isopropanol wipe immediately after each wear session. Allow to air dry completely.
*   **Solvent Prohibition:** Do not use acetone, chlorinated solvents, or abrasive pads (quoted from plan §6).

---

### 4.4 Electrical Safety Interlocks

1.  **Battery-Only Operation:** Power must originate solely from isolated DC batteries (two 9 V batteries for Stage A; single 501015 Li-ion cell for Stage B). Connection to mains-powered supplies is strictly prohibited.
2.  **Never Charge While Worn:** The earpiece contains no external charging port. Charging occurs strictly off the ear with the lid removed (quoted from plan §6).
3.  **Tethered Debugging Isolation:** During serial monitoring via USB, the host computer must run on internal battery power with its AC wall charger unplugged. The debug cable must be disconnected and the Ø2.0 mm exit port sealed before active wear.
4.  **Hardware Series Protection:** Every electrode lead incorporates an in-line $220\text{ k}\Omega$ resistor and clamping diodes located within 10 mm of the board pads before reaching any active silicon.

---

## 5. Quantitative Results (Stage A Part 2 Bench Execution)

> [!IMPORTANT]
> **Binding Rule:** Headings only. No empirical data is recorded in this section during Part 1. Data may be entered only during Part 2 after Stage A hardware has been acquired and tested. Any retrospective alteration or relaxation of any frozen criterion in Section 3 after experimental data exists immediately voids S1 gate entry and invalidates the release state.

### 5.1 Baseline Resting Noise Floor (20–490 Hz)
*(Awaiting Stage A hardware acquisition)*

### 5.2 Signal-to-Noise Ratio: Voluntary Auricular Flex
*(Awaiting Stage A hardware acquisition)*

### 5.3 Signal-to-Noise Ratio: Jaw Clench Confirmation Channel
*(Awaiting Stage A hardware acquisition)*

### 5.4 Contact Continuity and Dropout Under Jaw Motion
*(Awaiting Stage A hardware acquisition)*

### 5.5 Three-Day Re-Donning Stability (Fixed Threshold)
*(Awaiting Stage A hardware acquisition)*

### 5.6 False-Positive Rate: Eating (Chewing)
*(Awaiting Stage A hardware acquisition)*

### 5.7 False-Positive Rate: Talking (Continuous Speech)
*(Awaiting Stage A hardware acquisition)*

### 5.8 False-Positive Rate: Walking (Locomotion)
*(Awaiting Stage A hardware acquisition)*

### 5.9 Cross-Talk Rejection: Yawning
*(Awaiting Stage A hardware acquisition)*

### 5.10 Cross-Talk Rejection: Facial Mimicry (Smiling, Blinking)
*(Awaiting Stage A hardware acquisition)*

---

## 6. Interface Inputs and Handoffs to Other Packages

*   **Handoff to WP7b (Validation Wear):**
    *   WP7b measures bench clamping force, travel, and electrical continuity of the physical Stage B hardware stack against the criteria frozen in Section 3.
    *   WP7b conducts the S3 validation wear trials adhering strictly to the session rules and stop criteria in Section 4.
*   **Handoff to WP8 (Stage B Shell CAD):**
    *   WP8 takes the confirmed body-frame coordinates $(u_1, s_1)$, $(u_2, s_2)$, and $(u_{\text{ref}}, s_{\text{ref}})$ derived from Section 2.5 to position the contact clearance holes, reference pocket, and wire channel in `docs/fab/cad/v2/`.
*   **Handoff to WP6 (Board Packing & Interface v2):**
    *   WP6 confirms that medial PCB lead pads $(5.9, 26.5)$, $(5.5, 30.0)$, and $(4.0, 29.0)$ match the internal lead wire routing corridors.
    *   WP6 takes nothing from WP7a unless the bench montage requires moving the contact center-lines beyond the keep-out envelopes defined in `docs/fab/interface.md`.
