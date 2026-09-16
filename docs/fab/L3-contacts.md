# L3 — Auricular Anatomy and Skin Contacts for a Manufactured Shell

- **Report path:** `docs/fab/L3-contacts.md`
- **Lane:** L3 (Auricular Anatomy and Skin Contacts)
- **Target:** Elicio Stage B Behind-The-Ear (BTE) Pod (`docs/EARPIECE_DESIGN.md`)
- **Date:** 2026-09-16

---

## 1. Executive Summary

This study establishes the electrophysiological, anatomical, and material engineering foundations for the contact interface of the Elicio Stage B behind-the-ear (BTE) pod.

1. **Target Musculature & Electrode Montage:**
   - The primary command channel targets the **posterior auricular muscle (PAM)**, a thin horizontal fan (~15–25 mm length, ~10–15 mm width) originating on the mastoid process and inserting into the ponticulus of the cranial concha.
   - A secondary/alternative site is the **superior auricular muscle (SAM)**, a fan-shaped muscle (~25–35 mm height) originating on the galea aponeurotica and inserting into the upper cranial auricle.
   - The optimal montage uses a **bipolar pair aligned along the muscle-fiber direction** (horizontal/oblique anterior-posterior for PAM; vertical cranial-caudal for SAM) with an **inter-electrode distance (IED) of 12–15 mm**.
   - The reference electrode sits over the **inferior mastoid tip** or the **cranial lobule attachment**, providing a local, electrically neutral bony/cartilaginous site that maximizes common-mode rejection of far-field cranial and neck EMG.
   - **Cross-talk Mitigation:** Jaw clenches (masseter/temporalis) generate large 200–800 µV signals across the retroauricular crease. This cross-talk is deliberately utilized as the safety harness confirmation channel. Facial expressions (smile/blink) and neck rotation (sternocleidomastoid) must be isolated via differential spacing and high-pass filtering (corner at 20–30 Hz).

2. **Electrophysiological Signal Regimes:**
   - Voluntary auricular muscle contractions generate surface EMG amplitudes of **50–350 µV peak-to-peak**, with spectral energy concentrated between **25 Hz and 400 Hz** (peak power at 70–160 Hz).
   - Involuntary vestigial auriculomotor orienting twitches (studied in auditory attention literature) are far subtler: **2–15 µV**.
   - The Stage A bench amplifier gain (100–1000×) and Stage B sampling rate (800–1000 SPS) are well matched to capture voluntary PAM/SAM activation without aliasing.

3. **Skin Contact Architecture:**
   - **Contact Material Recommendation:** **Grade 2 or Grade 5 Titanium** (or surgical **316L Stainless Steel**) configured as **convex dome studs** with a diameter of **7.0–9.0 mm** and a spherical dome radius of **5.0–7.0 mm**.
   - **Contact Physics (TPU vs. Metal):** The design record note that "16 mm contacts work where 5 mm fail" applies specifically to conductive TPU due to its high bulk volume resistivity (~100–250 Ω·cm). For metals, bulk resistance is negligible ($10^{-7}\text{ }\Omega\cdot\text{m}$). Rigid 16 mm metal plates fail behind the ear because they cannot conform to the concave retroauricular crease, causing edge lift and air gaps. Conversely, 7–9 mm convex metal domes concentrate contact pressure (target: **10–25 kPa**) to breach stratum corneum air gaps and displace fine vellus hair while maintaining long-term wearer comfort.
   - **Mechanical Suspension:** Contacts must not be rigidly bonded to an inflexible shell. Each contact should be sprung using miniature internal coil springs, conductive silicone elastomeric pads, or low-profile pogo suspension (0.5–1.0 N normal force per contact) to maintain continuous contact under jaw and pinna movements.
   - **Nickel Safety:** All metallic contacts must be verified 100% nickel-free via Mill Test Certificates (ASTM F136 / ASTM F67 for titanium) or proven compliant with **EN 1811** (<0.05 µg/cm²/week nickel release). Standard off-the-shelf gold-plated medical snaps and catalog pogo pins are disqualified because they rely on an underlying 2.5–5.0 µm nickel barrier layer that exposes bare nickel when the flash gold plating wears through.

---

## 2. Auricular Anatomy and Surface EMG Electrode Placement

The extrinsic auricular muscles are vestigial motor structures in humans that retain somatic motor innervation via the facial nerve (Cranial Nerve VII). Voluntary control is present in 15–20% of the adult population and is readily trainable via biofeedback.

```
       [ Galea Aponeurotica / Temporalis Fascia ]
                         |
                       (SAM)  <-- Superior Auricular Muscle (Fibers run vertical)
                         |
           +-------------+-------------+
           |       ROOT OF HELIX       |
           |                           |
[ Anterior |         PINNA             | [ RETROAURICULAR SULCUS ]
  Auricular|                           |
  Muscle ] |                           | (PAM) <-- Posterior Auricular Muscle
  (AAM)    |       CONCHA / CRANIAL    |           (Fibers run horizontal)
           |       SURFACE             |           Origin: Mastoid Bone
           |                           |           Insertion: Conchal Ponticulus
           +-------------+-------------+
                         |
                     [ LOBULE ]  <-- Alternative Reference Site
                         |
                 [ MASTOID PROCESS ] <-- Primary Reference Site (Inferior Bony Tip)
```

### 2.1 Musculature Dimensions, Innervation, and Landmarks

| Muscle | Origin | Insertion | Dimensions (Length × Width × Thickness) | Fiber Orientation | Innervation | Anatomical Skin Landmark |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Posterior Auricular (PAM)** | Mastoid portion of temporal bone, lateral to mastoid crest | Ponticulus on cranial surface of concha of pinna | 15–25 mm × 10–15 mm × 1.0–2.0 mm | **Horizontal / slightly oblique** (posterior-inferior to anterior-superior) | Posterior auricular branch of facial nerve (CN VII) | Mid-posterior retroauricular sulcus, 10–15 mm behind the pinna attachment fold, halfway up the conchal bowl. |
| **Superior Auricular (SAM)** | Galea aponeurotica and temporal fascia above helix | Thin tendon into upper cranial surface of auricle / antihelix | 25–35 mm × 15–25 mm × 0.8–1.5 mm | **Vertical** (cranial to caudal / superior to inferior) | Temporal branches of facial nerve (CN VII) | Superior to pinna root, 10–20 mm above upper helix crest, inferior to scalp hairline. |
| **Anterior Auricular (AAM)** | Lateral edge of galea aponeurotica | Spine of helix on anterior auricle | 10–15 mm × 8–12 mm × 0.5–1.0 mm | **Oblique** (anterior-superior to posterior-inferior) | Temporal branches of facial nerve (CN VII) | Preauricular region immediately in front of tragus and crus of helix. |

*Sources:* Rüschenschmidt et al., *Diagnostics* 2022 ([10.3390/diagnostics12010121](https://doi.org/10.3390/diagnostics12010121)); Gray's Anatomy (42nd Ed., 2020); Standring et al.

### 2.2 Surface EMG Contact Placement & Inter-Electrode Distance

1. **Posterior Auricular Muscle (PAM) Montage (Primary Channel):**
   - **Signal Contact 1 (Active/Positive):** Sits over the muscle belly, roughly 8–10 mm posterior to the retroauricular crease at the vertical midpoint of the ear (level with the external auditory canal aperture).
   - **Signal Contact 2 (Active/Negative):** Placed 12–15 mm posterior to Contact 1 along the horizontal axis toward the mastoid portion of the temporal bone.
   - **Inter-Electrode Distance (IED):** **12–15 mm center-to-center**. Because the muscle belly length is 15–25 mm, an IED exceeding 18 mm spans off the muscle belly onto the occipitalis or neck fascia, causing differential cancellation and loss of spatial selectivity.
   - **Orientation:** Horizontal (running along the line connecting the conchal ponticulus to the mastoid crest).

2. **Superior Auricular Muscle (SAM) Montage (Alternative/Secondary Channel):**
   - **Signal Contacts:** Placed vertically above the helix root. Signal Contact 1 sits 5 mm above the helix attachment; Signal Contact 2 sits 12–15 mm superior to Contact 1.
   - **Orientation:** Strictly vertical (cranial-caudal).
   - **Constraint:** In many individuals, the scalp hairline extends down to or near the upper helix, requiring contacts to penetrate or navigate hair. PAM has much less hair occlusion in the retroauricular groove.

3. **Reference Electrode Placement:**
   - **Primary Site:** The **inferior tip of the mastoid process**. This is a prominent bony projection devoid of muscular bellies, situated 15–20 mm inferior to the PAM belly. It provides high common-mode rejection of cranial electrical activity without picking up local contraction.
   - **Secondary Site:** The **cranial attachment of the earlobe (lobule)**. The lobule consists of cutaneous and adipose tissue with zero underlying skeletal muscle, making it an ideal biopotential reference.

### 2.3 Cross-Talk Analysis & Mitigation

Because the retroauricular space is bounded by powerful cranial and cervical muscles, biopotential isolation requires deliberate mechanical and electrical separation:

| Muscle Group | Action | Typical Amplitude at Retroauricular Site | Spectral Profile | Impact on Auricular Channel | Mitigation / Engineering Role |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Temporalis** | Clenching teeth, chewing, jaw clench | 200–800 µV | 30–350 Hz (high energy at 80–150 Hz) | Dominates superior retroauricular space; radiates into SAM and upper PAM. | **Intentional Confirmation Channel.** Harness policy leverages this large burst for secondary confirmation (`jaw_clench` at floor 0.85). |
| **Masseter** | Clenching teeth, biting | 150–600 µV | 20–300 Hz | Far-field volume conduction to lower mastoid. | Forms confirmation signature; distinct temporal envelope from fast auricular twitches. |
| **Occipitalis** | Scalp retraction, eyebrow raising | 100–300 µV | 40–250 Hz | Sits directly posterior to PAM; fibers run horizontally. | Kept outside detection field by maintaining tight contact spacing (IED $\le 15\text{ mm}$) close to the conchal fold. |
| **Sternocleidomastoid (SCM)** | Head rotation, neck flexion | 100–500 µV | 20–250 Hz | Inserts into the mastoid process tip; strong signal during neck turning. | Reference electrode must sit on the lateral bony mastoid surface rather than the posterior/inferior muscular insertion. High-pass filter at 25 Hz blocks low-frequency neck sway. |
| **Splenius Capitis** | Head extension, lateral flexion | 80–250 µV | 20–200 Hz | Deep posterior neck activity. | Far-field; rejected by high CMRR (>90 dB) differential amplifier. |
| **Facial Mimicry (Orbicularis Oculi/Zygomaticus)** | Hard blinks, smiling, squinting | 50–150 µV | 20–150 Hz | Involuntary synkinesis in some subjects. | Fast rise time (<20 ms) distinguishes intentional voluntary holds from blinks. |

---

## 3. Prior Recordings of Auricular EMG: Literature and Benchmarks

Auricular electrophysiology divides historically into three domains:
1. **The Postauricular Muscle Response (PAMR):** An acoustic reflex (sonomotor response) evoked by loud transient sounds, mediated by the brainstem.
2. **Vestigial Auditory Attention Research (Saarland Group):** Involuntary, covert orienting twitches of the PAM and SAM when attending to lateralized auditory stimuli.
3. **Earable Gesture Systems & In-Ear Biopotentials:** Active voluntary microgestures (wiggling, ear clicks, canal deformations) for human-computer interaction.

### 3.1 Comparison of Key Historical and Recent Studies

| Study / Product | Modality / Target | Electrode Type & Size | Electrode Positions & IED | Signal Amplitude Range ($\mu\text{V}$) | Sample Rate | Bandpass Filters | Classification / Findings | Source Citation / DOI |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Patuzzi & O'Beirne (1999)** | PAMR (Acoustic sonomotor reflex) | Wet Ag/AgCl discs (8 mm dia) | Active on PAM belly, ref on pinna dorsal surface; IED ~20 mm | **10–50 $\mu\text{V}$** (involuntary reflex); **up to 250 $\mu\text{V}$** with facilitation | 5–10 kHz | 20 Hz – 2 kHz | Reflex latency ~12–15 ms; amplitude scales with voluntary muscle tone. | *Hearing Research* 136(1-2): 101–110. [10.1016/S0378-5955(99)00115-5](https://doi.org/10.1016/S0378-5955(99)00115-5) |
| **Strauss et al. (2020)** | Vestigial auditory attention (Saarland) | Passive Ag/AgCl wet discs (g.LADYbird) | Bipolar pairs over PAM and SAM; IED = **10 mm**; ground on forehead | **2–15 $\mu\text{V}$** (covert involuntary attention shifts) | 4.8 kHz or 9.6 kHz (g.USBamp / g.HIamp) | 10 Hz – 500 Hz | Significant tonic ipsilateral PAM/SAM increase when attending lateral sound source. | *eLife* 9: e54536. [10.7554/eLife.54536](https://doi.org/10.7554/eLife.54536) |
| **Rüschenschmidt et al. (2022)** | Extrinsic ear muscle EMG in healthy & synkinesis | Concentric needle & wet Ag/AgCl surface | Defined hot spots: PAM behind ear, SAM above helix, AAM in front; ref on mastoid | **50–400 $\mu\text{V}$** (voluntary contractions); synkinesis ~100 $\mu\text{V}$ | 4 kHz | 20 Hz – 1 kHz | Established needle and surface hot spots; validated voluntary ear-wiggling surface detection. | *Diagnostics* 12(1): 121. [10.3390/diagnostics12010121](https://doi.org/10.3390/diagnostics12010121) |
| **Schroeer et al. (2023)** | In-ear and around-ear vestigial auriculomotor | Custom dry-contact earpiece vs. around-ear wet Ag/AgCl | In-concha dry pins + retroauricular surface electrodes | **5–25 $\mu\text{V}$** (transient acoustic evoked, ~70 ms latency) | 4.8 kHz | 15 Hz – 450 Hz | Dry in-ear contacts successfully recorded directional auriculomotor activation without skin prep. | *Trends in Hearing* 27: 1–14. [10.1177/23312165231212873](https://doi.org/10.1177/23312165231212873) |
| **Schmalfuß et al. (2025)** | Auriculomotor listening effort in hearing aid users | Gelled Ag/AgCl bipolar pairs | Bilateral PAM and SAM pairs, IED = 10 mm | **10–80 $\mu\text{V}$** (tonic listening effort in noise) | 4.8 kHz | 20 Hz – 400 Hz | SAM/PAM EMG correlates directly with perceived listening effort in complex audio scenes. | *Frontiers in Neuroscience* 19: 1489012. [10.3389/fnins.2025.1489012](https://doi.org/10.3389/fnins.2025.1489012) |
| **EarFieldSensing (Matthies et al., 2017)** | In-ear electric field sensing (EFS) | 4 copper strip electrodes on earbud surface | In-ear canal perimeter (differential capacitive sensing) | Relative voltage shift ($\Delta V \approx 5–50\text{ mV}$) | 1 kHz | Low-pass filtered (DC–100 Hz) | **90.2% accuracy** across 5 facial gestures (smile, wink, open mouth, clench, neutral). | *CHI 2017*: 2610–2620. [10.1145/3025453.3025692](https://doi.org/10.1145/3025453.3025692) |
| **EarBuddy (Xu et al., 2020)** | On-face touch & tap sensing | Commercial ANC feedforward microphones | External earphone mic orifices | Acoustic transmission ($0.1–10\text{ Pa}$) | 44.1 kHz | Acoustic bandpass (100 Hz – 16 kHz) | **95.3% accuracy** on 8 tapping gestures across face/ears. *(Note: Acoustic, not EMG).* | *CHI 2020*: 1–13. [10.1145/3313831.3376246](https://doi.org/10.1145/3313831.3376246) |
| **Open-cEEGrid (Knierim et al., 2022)** | Around-ear flex-PCB EEG/EMG | Gold-plated flex PCB pads (10 ch) | C-shaped grid around ear; IED = 12–18 mm | **30–500 $\mu\text{V}$** (jaw clench/bruxism); **5–40 $\mu\text{V}$** (EEG) | 250 Hz (OpenBCI Cyton) | 1 Hz – 50 Hz (EEG) / 10–100 Hz (EMG) | Real-time teeth grinding (bruxism) and facial action detection with low false positives. | *HardwareX* 12: e00300. [10.1016/j.hardwarex.2022.e00300](https://doi.org/10.1016/j.hardwarex.2022.e00300) |

---

## 4. cEEGrid and Flex-Print Around-the-Ear Arrays

The **cEEGrid** represents the benchmark for conformal retroauricular biopotential recording. Conceived by Stefan Debener and Martin Bleichner at the University of Oldenburg (2015), it wraps an array of sensors around the pinna.

```
                  .-''''-.  <-- Upper C-arm (SAM region)
                .'   C1   '.
               /   C2   C3  \
              |   [ EAR ]    |
              |   CANAL     C4 |
               \            C5/ <-- Retroauricular crease (PAM region)
                '.  C8    C6.'
                  '-. C7 .-'   <-- Lower C-arm (Mastoid tip / ref)
```

### 4.1 Commercial Status of cEEGrid (2026)

- **Original Developer:** University of Oldenburg (Debener et al., 2015; Bleichner & Debener, 2017, *Brain Topography*).
- **Commercial Manufacturer / Distributor:** [TMSi](https://www.tmsi.com/) (Twente Medical Systems International B.V., Oldenzaal, Netherlands) and [Easycap GmbH](https://www.easycap.de/) (Woerthsee, Germany).
- **Product Details:** Currently sold as the **cEEGrid V4** (10-channel Ag/AgCl printed array). It features screen-printed Ag/AgCl circular electrodes (approx. 4.0 mm diameter) embedded on a flexible, transparent polyester (PET) substrate with a thickness of ~0.12 mm.
- **Adhesive Interface:** Requires custom die-cut C-shaped double-sided medical adhesive stickers ([3M 1522](https://www.3m.com/) or similar biocompatible acrylic tape). Each electrode well is filled with a drop of electrolyte gel (Abralyt HiCl or Signa Gel).
- **2026 Availability & Pricing:**
  - TMSi and Easycap continue to manufacture and sell cEEGrids in 2026. They operate primarily on a research/clinical quote-based model.
  - Easycap list pricing (educational/research): Packs of 10 pairs are priced around **€280–€350** (~$300–$380 USD), making individual grids ~$15–$19 each as semi-reusable items.
  - [OpenBCI](https://shop.openbci.com/products/around-the-ear-eeg-bundle) previously marketed an "Open-cEEGrid Kit" ($799.99 including Cyton adapters, replacement stickers, and gold-plated arrays).

### 4.2 Reproduction via Custom Flex PCB (JLCPCB / PCBWay)

A custom Flexible Printed Circuit (FPC) ordered through commercial rapid PCB fabricators can replicate the cEEGrid geometry for minimal cost.

#### Fabrication Specifications:
- **Substrate:** 1-layer or 2-layer Polyimide (PI), base thickness 0.05–0.10 mm (total thickness with coverlay: ~0.11 mm).
- **Trace Metallurgy:** $0.5\text{ oz}$ ($18\text{ }\mu\text{m}$) rolled annealed copper.
- **Surface Finish:** **ENIG** (Electroless Nickel Immersion Gold) or **Hard Gold**.
- **Unit Cost:** JLCPCB fabricates a minimum batch of 5 custom FPCs (dimensions $80 \times 60\text{ mm}$) for **$16.00–$25.00 total** ($3.20–$5.00 per grid), with 3–5 day turnaround to Massachusetts.

#### Trade-Offs: Custom Flex PCB vs. Rigid Manufactured Shell

| Parameter | Custom Flex PCB (cEEGrid Clone) | Rigid Shell with Discrete Metal Contacts |
| :--- | :--- | :--- |
| **Initial Fabrication Cost** | **$16–$25** for 5 units (JLCPCB). | **$5–$15** (3D printed shell + $3–$8 hardware). |
| **Consumables per Session** | **Required:** Fresh double-sided adhesive tape ($0.50/use) and electrolyte gel. | **Zero consumables.** Dry mechanical interface. |
| **Donning & Doffing Speed** | **Slow (3–5 minutes):** Skin degreasing, tape peeling, precision alignment, gel injection. | **Instant (2–5 seconds):** Slips over pinna like a standard hearing aid. |
| **Reusability & Durability** | **Poor to Moderate:** Thin polyimide tears easily; trace fatigue breaks after 10–20 tape removals. | **High:** Rugged monolithic shell; withstands years of insertion/removal. |
| **Contact Impedance** | **Low (5–20 k$\Omega$):** Maintained by electrolyte gel bridge. | **Moderate (30–100 k$\Omega$):** Dry skin contact; requires high-Z input buffer ($>1\text{ G}\Omega$). |
| **Sweat & Hair Vulnerability** | **Severe:** Sweat dissolves tape adhesion; hair strands trapped under tape cause complete contact lift-off. | **Low:** Concentrated spring pressure penetrates past hair strands; sweat reduces dry impedance. |
| **Subtlety & Form Factor** | Visible shiny flex tail descending behind ear; looks clinical/experimental. | **Completely covert:** Concealed entirely inside a standard BTE pod geometry. |

**Synthesis Assessment:** While a custom FPC is an outstanding, inexpensive bench tool for 16-channel spatial mapping, it is disqualified for daily covert wearable use due to the mandatory consumable tape, preparation friction, and mechanical fragility. The rigid BTE shell is mandatory for the product slice.

---

## 5. Dry-Contact Options for a Manufactured Shell

The design specification mandates **nickel-free** dry skin contacts that mechanically anchor into a manufactured shell.

```
       [ MANUFACTURED BTE SHELL WALL ]
            |                      |
            |   +--------------+   |
            |   | RETAINING NUT|   |  <-- Internal termination
            |   +-------+------+   |
            |           | (Thread) |
            |   +-------+------+   |
============+===+==============+===+============ [ Skin Boundary ]
                |  CONVEX DOME |
                |  STUD (7 mm) |      <-- Smooth, nickel-free metal
                +--------------+          presses against retroauricular skin
```

### 5.1 Deep Evaluation of Candidate Contact Technologies

#### 1. 316L Stainless Steel Discs, Domes, and Studs
- **Skin Safety & The Nickel Question:** 316L contains 10.0–14.0% nickel by weight. However, the addition of 2.0–3.0% molybdenum and 16.0–18.0% chromium forms a highly stable, self-healing passive chromium-molybdenum oxide film. Under the European standard **EN 1811:2011+A1:2015**, 316L consistently demonstrates a nickel release rate below $0.03\text{ }\mu\text{g/cm}^2/\text{week}$, far below the legal threshold of $0.5\text{ }\mu\text{g/cm}^2/\text{week}$ for prolonged skin contact articles. It is classified as hypoallergenic for medical tools, but individuals with extreme, pre-sensitized Type IV contact allergies may occasionally react if the surface is scratched.
- **Contact Impedance (Dry):** $30–100\text{ k}\Omega$ at 100 Hz on unprepared skin (dropping to $15–40\text{ k}\Omega$ after 10 minutes of natural perspiration accumulation).
- **Comfort:** Excellent when machined with a convex spherical dome (radius 5.0–7.0 mm); poor if flat-edged.
- **Attachment Method:** Threaded M2 or M2.5 stud through shell wall secured with an internal locknut or heat-set insert; press-fit into reamed boss.
- **Wire Termination:** Crimp ring terminal clamped beneath internal retaining nut, or soft soldering using aggressive stainless-steel flux (phosphoric acid base, thoroughly cleaned post-solder).
- **Concrete Source & Part:** [McMaster-Carr](https://www.mcmaster.com/) 92095A178 (M3 × 6 mm 316 Stainless Steel Button Head Hex Drive Screw), pack of 50 for **$11.20** ($0.22/ea) as of 2026. Smooth domed head diameter = 5.7 mm, head height = 1.65 mm.

#### 2. Gold-Plated Snap Studs
- **Skin Safety & The Nickel Question:** **Severe hazard.** The vast majority of commercial medical and garment snap studs (e.g., standard 4.0 mm ECG snaps) are stamped from brass, plated with a **2.5–5.0 $\mu\text{m}$ electrolytic nickel barrier**, and finished with a micro-thin (0.025–0.05 µm) gold flash. Under frictional skin contact and acidic sweat (pH 4.5–6.0), the gold flash wears off within days, directly exposing the nickel underlayer and causing rapid sensitization. True nickel-free gold snaps require a pure silver, bronze, or palladium barrier layer, which is rarely certified on generic parts.
- **Contact Impedance (Dry):** $15–50\text{ k}\Omega$.
- **Comfort:** High (standard 4 mm smooth rounded stud).
- **Attachment Method:** Rivet staked through shell wall.
- **Wire Termination:** Snaps directly into standard 4 mm medical lead socket, or soldered rear rivet.
- **Concrete Source & Part:** [Bio-Medical Instruments](https://bio-medical.com/) Gold Snap Electrodes / Leads; or [Prym Fashion](https://www.prym.com/) certified nickel-free brass snaps ($5.50/pack of 10). *Status: Must be verified by supplier certification.*

#### 3. Titanium (Grade 2 CP or Grade 5 Ti-6Al-4V)
- **Skin Safety & The Nickel Question:** **100% Nickel-Free.** Commercially Pure (CP) Grade 2 Titanium (ASTM F67) and Grade 5 / Grade 23 Ti-6Al-4V ELI (ASTM F136) contain 0.00% nickel. Titanium spontaneously forms an inert, biologically non-reactive titanium dioxide ($\text{TiO}_2$) ceramic passivation layer that prevents all metal ion leaching. It is the gold standard for permanent human medical implants.
- **Contact Impedance (Dry):** $40–120\text{ k}\Omega$ at 100 Hz. The $\text{TiO}_2$ layer adds a slight capacitive barrier, easily handled by an instrumentation amplifier with input impedance $\ge 1\text{ G}\Omega$.
- **Comfort:** Superb. Extremely lightweight (density $4.5\text{ g/cm}^3$, half that of steel) and low thermal conductivity (does not feel cold against the skin).
- **Attachment Method:** M2/M2.5/M3 threaded button-head screw driven into an internal brass/copper heat-set insert; or internally threaded flat-back labret body jewelry studs.
- **Wire Termination:** Mechanical ring-lug terminal clamped under internal locknut. (Titanium cannot be soft-soldered with rosin flux; mechanical crimp/clamp is mandatory).
- **Concrete Source & Part:** [McMaster-Carr](https://www.mcmaster.com/) 93625A110 (Grade 2 Titanium Button Head Hex Drive Screw, M3 × 6 mm), pack of 10 for **$18.65** ($1.87/ea). Alternatively: [BodyArtForms](https://bodyartforms.com/) ASTM F136 Implant Grade Titanium Flat-Back Labret Studs ($4.50–$7.00/ea).

#### 4. Sintered Ag/AgCl Pellets
- **Skin Safety & The Nickel Question:** **100% Nickel-Free.** Consists of compressed, sintered silver and silver chloride powder. Non-toxic, but prolonged exposure to sweat can cause localized dark silver oxide skin staining (argyria-like spot, harmless but cosmetically undesirable).
- **Contact Impedance (Dry/Semi-Dry):** **Lowest of all biopotential contacts**: $5–20\text{ k}\Omega$ dry; non-polarizable interface with minimal half-cell offset voltage drift ($<100\text{ }\mu\text{V}$).
- **Comfort:** Moderate. Brittle ceramic-like texture; must be cast into a smooth bezel.
- **Attachment Method:** Potted into recessed shell pockets using medical-grade epoxy or RTV silicone.
- **Wire Termination:** Supplied with an embedded pure silver lead wire welded directly into the sintered matrix.
- **Concrete Source & Part:** [BioMed Electrodes](https://www.biomedelectrodes.com/) (part #EP-02, 2.0 mm dia × 4.0 mm sintered Ag/AgCl pellet with silver wire), priced at **$15.00 each** (2026 catalog); or [Bio-Medical Instruments](https://bio-medical.com/) 12 mm Sintered Ag/AgCl Disc Electrode with lead ($40.32/ea).

#### 5. Conductive Silicone (Carbon-Loaded Elastomer)
- **Skin Safety & The Nickel Question:** **100% Nickel-Free.** Pure medical silicone matrix compounded with high-purity conductive carbon black. Completely hypoallergenic, inert, and non-cytotoxic.
- **Contact Impedance (Dry):** $50–180\text{ k}\Omega$ on dry skin. Lower bulk resistivity than TPU, and provides conformal microscopic contact.
- **Comfort:** Exceptional. Soft elastomeric compliance (Shore 40A–60A); flexes smoothly with ear and jaw motion without pressure hotspots.
- **Attachment Method:** Molded pills press-fit into undercut retention bezels, or bonded with specialized silicone transfer adhesive ([Sil-Poxy](https://www.smooth-on.com/products/sil-poxy/) by Smooth-On).
- **Wire Termination:** Mechanical compression against an internal gold PCB pad, conductive silver-filled epoxy ([MG Chemicals 8331](https://mgchemicals.com/)), or an embedded fine platinum/silver wire.
- **Concrete Source & Part:** [Parker Chomerics](https://www.parker.com/chomerics) CHO-SEAL 1285 carbon-filled silicone sheet / molded contacts (available via [DigiKey](https://www.digikey.com/)); or [Specialty Silicone Products (SSP)](https://www.sspinc.com/) SSP-2529 conductive silicone elastomer ($25–$50 sample sheet).

#### 6. Conductive TPU (Palmiga PI-ETPU 95-250)
- **Skin Safety & The Nickel Question:** **100% Nickel-Free.** Thermoplastic polyurethane filled with conductive carbon black. Safe for prolonged skin contact.
- **Contact Impedance (Dry):** **High**: $80–300\text{ k}\Omega$ on dry skin. Volume resistivity is relatively high (~$150–250\text{ }\Omega\cdot\text{cm}$), necessitating a large contact area ($\ge 12–16\text{ mm}$ diameter) to keep impedance under $200\text{ k}\Omega$.
- **Comfort:** Moderate. Shore 95A is relatively hard (comparable to a shopping cart wheel or hard boot heel), offering minimal elastomeric cushion.
- **Attachment Method:** Co-printed in a multi-material FDM printer directly into a rigid TPU/PLA hull, or printed as a separate press-fit plug.
- **Wire Termination:** Mechanical compression against stripped copper wire, or conductive copper foil tape with conductive adhesive.
- **Sourcing & Print Bureaus:** Developed by Thomas Palm of Palmiga Innovation (Sweden). Sold as 250 g spools on [Rubber3DPrinting.com](https://rubber3dprinting.com/) and [Creative Tools](https://www.creativetools.se/) for **€47.80 (~$52 USD)**. Palmiga provides custom printing on request. **Critical Bureau Reality:** Commercial rapid print bureaus (JLCPCB, PCBWay, Xometry, Shapeways, Protolabs) **do not stock or print conductive TPU**. They reject customer-supplied filaments due to cross-contamination and extruder jamming risks. Outsourced manufacturing cannot rely on conductive TPU.

#### 7. Conductive Fabric (Silver-Plated Textile)
- **Skin Safety & The Nickel Question:** Pure silver-plated nylon (e.g., Statex Shieldex) is **100% Nickel-Free** and antibacterial. *Caution:* Cheap generic RF shielding fabrics from Amazon/AliExpress are plated with copper and nickel (~20% nickel by weight) and will trigger severe contact dermatitis. Only certified pure silver textiles can be used.
- **Contact Impedance (Dry):** $20–80\text{ k}\Omega$. Sweat rapidly lowers impedance.
- **Comfort:** Highest possible comfort. Zero pressure points; breathes naturally.
- **Attachment Method:** Fabric wrapped around a soft silicone or polyurethane foam core, adhesively bonded to the shell rim using [3M 9474LE](https://www.3m.com/) 300LSE high-tack transfer tape.
- **Wire Termination:** Machine-sewn or hand-stitched with stainless conductive thread ([Adafruit 1167](https://www.adafruit.com/product/1167)), clamped under a terminal screw, or bonded with conductive epoxy.
- **Concrete Source & Part:** [Adafruit](https://www.adafruit.com/product/1070) Silver Conductive Fabric (Product ID 1070, 20 cm × 20 cm sheet), **$11.95** as of 2026. Surface resistivity $<0.5\text{ }\Omega/\text{sq}$.

#### 8. PCB ENIG / ENEPIG Pads
- **Skin Safety & The Nickel Question:** **Severe Nickel Hazard with standard ENIG.** ENIG consists of $3.0–5.0\text{ }\mu\text{m}$ of electroless nickel covered by $0.025–0.05\text{ }\mu\text{m}$ (1–2 micro-inches) of immersion gold. The gold flash is porous and wears off under skin abrasion in days, exposing raw nickel. **Alternative:** Specify **ENEPIG** (Electroless Nickel Electroless Palladium Immersion Gold), which adds a 0.1–0.2 µm pure palladium barrier that blocks nickel diffusion, or specify **Hard Gold** ($>0.75\text{ }\mu\text{m}$ pure electroplated gold).
- **Contact Impedance (Dry):** $30–100\text{ k}\Omega$.
- **Comfort:** Poor if flat rigid PCB; acceptable if mounted on flexible polyimide conforming to the crease.
- **Attachment Method:** The PCB itself forms the inner wall of the shell; zero assembly required.
- **Wire Termination:** Internal copper traces route directly to amplifier inputs with zero wiring.
- **Concrete Source & Part:** JLCPCB or PCBWay custom 2-layer FPC with ENEPIG or Hard Gold surface finish (**$35.00–$50.00** for 5 boards).

#### 9. Spring-Loaded Pogo Pins
- **Skin Safety & The Nickel Question:** Standard catalog pogo pins (Mill-Max, Harwin, C.C.P.) are brass with a $2.54\text{ }\mu\text{m}$ ($100\text{ }\mu\text{''}$) nickel barrier beneath a $0.5\text{ }\mu\text{m}$ gold plating. Plunger sliding motion rapidly strips gold, releasing nickel. Custom nickel-free pogo pins require high MOQs (>1,000 pcs).
- **Contact Impedance (Dry):** $15–40\text{ k}\Omega$.
- **Comfort:** Very poor if pointed or serrated; acceptable only if equipped with a large spherical or concave radiused head ($R \ge 2.0\text{ mm}$).
- **Attachment Method:** Press-fit into calibrated shell bores; tails soldered directly to the main PCB.
- **Wire Termination:** Direct PCB surface-mount or through-hole solder joint.
- **Concrete Source & Part:** [Mill-Max](https://www.mill-max.com/) 0906-0-15-20-76-14-11-0 Spring-Loaded Contact (available via [DigiKey](https://www.digikey.com/en/products/detail/mill-max-manufacturing-corp/0906-0-15-20-76-14-11-0/1147048)), priced at **$0.81 each** (2026). Stroke = 1.4 mm, spring force ~60 g. *Note: Nickel-plated underlayer requires clear user advisory.*

---

## 6. Commercial Ear-Worn Biopotential Benchmarks

Commercial earable and consumer BCI systems have transitioned from wet lab electrodes to conformal dry contacts over the 2024–2026 product cycles.

```
                    [ COMMERCIAL CONTACT MODALITIES ]
                                   |
         +-------------------------+-------------------------+
         |                                                   |
   [ IN-CANAL / CONCHA ]                           [ CIRCUMAURAL / BTE ]
   - NextSense: Coated Silicone                    - Neurable: Conductive Fabric
   - IDUN Guardian: Dryode Polymer                 - Cognionics: Spring Polymer Legs
   - Naox: Silver-Inked Silicone                   - Emotiv: Hydrophilic Polymer Arms
   - OpenEarable: Dätwyler SoftPulse
```

### 6.1 Systematic Benchmark Matrix

| Product / Company | Form Factor | Electrode Material & Construction | Contact Geometry & Dimensions | Pressure Mechanism | Published Impedance & Stability | Re-Donning Repeatability | Source Reference |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **NextSense Smartbuds** (Commercial Launch Feb 2026) | True Wireless In-Ear Earbuds | Conductive silicone elastomer with proprietary **Tecticoat®** coating | 6 integrated dry sensors on ear-tip barrel and concha wing | In-canal radial silicone expansion + concha lock wing | **$<100\text{ k}\Omega$**; clinical-grade sleep EEG validated vs. intracranial EEG | High; silicone self-seats into canal bore; robust to minor head turns | [NextSense.io](https://nextsense.io/); Twice (Feb 2026) |
| **IDUN Guardian 4** (IDUN Technologies, Zurich) | In-Ear Canal Earbud | Proprietary **Dryode™** conductive polymer (carbon-filled polyurethane matrix) | 2–3 in-canal sensor rings (each ~3 mm wide) | Custom-molded or multi-size elastomeric canal tip compression | **$<200\text{ k}\Omega$** (stabilizes $<100\text{ k}\Omega$ after 10 min); dry contact | High; re-donning delta $<15\%$ impedance variation across multi-day trials | [IDUN Technologies](https://iduntechnologies.com/); *Front. Neurosci.* 2023 |
| **Naox Link / Wave** (Naox Technologies) | Wired Clinical / True Wireless (FDA 510(k) Cleared) | Medical-grade silicone substrate coated with **conductive silver ink** | Cylindrical canal rings (dia 6–9 mm, length 2.5 mm) | Radial elastic pressure against ear canal walls | **$<50\text{ k}\Omega$**; clinical EEG monitoring for epilepsy and sleep | High; FDA 510(k) validation demonstrated multi-hour recording stability | [Naox.tech](https://naox.tech/); *Bio-Protocol* 2024 |
| **Neurable MW75 Neuro** (Neurable / Master & Dynamic) | Over-Ear ANC Headphones | Soft **conductive textile (silver-plated fabric)** | 12 wide-area fabric pads embedded in ear cushions | Headband clamping force (~4.5 N total distributed around ear) | **$100–300\text{ k}\Omega$**; trades low impedance for comfort; active preamplifiers | High; headband geometry guarantees repeatable clamp pressure on every wear | [Neurable.com](https://neurable.com/); *IEEE TBME* 2024 |
| **OpenEarable ExG** (TECO / KIT Open Source) | In-Ear 3D Printed Earpiece | **Dätwyler SoftPulse®** conductive silicone dry electrodes | Hemispherical conductive silicone studs (dia 4 mm) | 3D-printed plug tailored to ear canal with interference fit | **$<150\text{ k}\Omega$**; AD7124-4 24-bit ADC with driven-right-leg (DRL) circuit | Moderate; dependent on user alignment during insertion | [OpenEarable GitHub](https://github.com/OpenEarable/open-earable); Röddiger et al. |
| **CGX / Cognionics DryPad / Flex** | Scalp / Mastoid Headset | 3D-printed flexible **nylon multi-leg spider** with conductive Ag/AgCl coating | 5–8 flexible legs per sensor (span ~15 mm) | Cantilever spring arm pressing legs through hair to skin | **$<50\text{ k}\Omega$**; active shielding and onboard buffer amplifier | High; flexible legs conform across hair and irregular skull contours | [CGX Systems](https://www.cgxsystems.com/); Chi et al. (IEEE TBME) |
| **Zeto z2EEG** | Clinical Dry Headset | Soft-tip disposable conductive polymer prongs | Multi-pronged array (dia 12 mm) | Mechanical spring-loaded pods in adjustable helmet frame | **Tolerates up to $1,000\text{ k}\Omega$** via ultra-high-Z active buffers | High; rapid donning (<5 min) without skin abrasion or gel | [Zeto-inc.com](https://zeto-inc.com/); FDA 510(k) K182852 |
| **Emotiv Insight** | Semi-Dry Headset | Hydrophilic conductive polymer composite | Flat rectangular pads ($8 \times 10\text{ mm}$) | Flexible polymer cantilever arms clamping against mastoid/forehead | **$50–200\text{ k}\Omega$** when primed with saline; dry $>500\text{ k}\Omega$ | Moderate; plastic cantilever arms lose tension over prolonged use | [Emotiv.com](https://www.emotiv.com/); Insight Specs |

---

## 7. Recommendations for the Elicio Stage B Shell

### 7.1 Contact Count, Geometry, and Spatial Arrangement

1. **Number of Contacts:** Exactly **3 contacts per earpiece**:
   - Contact 1: **Active Channel (+)** over anterior PAM belly.
   - Contact 2: **Active Channel (-)** over posterior PAM belly.
   - Contact 3: **Reference / Ground** over the inferior mastoid bone tip.
2. **Contact Dimensions:**
   - **Form:** **Convex spherical dome studs**.
   - **Diameter:** **7.0–9.0 mm**.
   - **Dome Crown Height:** **1.5–2.5 mm** (spherical radius $R = 5.0–7.0\text{ mm}$).
3. **Contact Spacing (IED):**
   - **12.0–15.0 mm center-to-center** between Contacts 1 and 2.
   - **20.0–25.0 mm distance** from the active pair to Contact 3 (Reference), oriented inferiorly.
4. **Resolution of the Contact Area Paradox (16 mm vs. 5 mm):**
   - *The Evidence:* The design record notes that Wolterink et al. (2020) and Alokaily et al. (2026) found that ~16 mm diameter contacts succeeded where 5 mm contacts failed for 3D-printed conductive TPU.
   - *The Physics:* Conductive carbon-TPU (such as Palmiga PI-ETPU 95-250) has a high volume resistivity of $\rho \approx 150–250\text{ }\Omega\cdot\text{cm}$. A 5 mm disc has a cross-sectional area of only $0.196\text{ cm}^2$. Its bulk resistance plus micro-contact interfacial impedance creates a source impedance of several mega-ohms, severely degrading signal-to-noise ratio. A 16 mm disc increases the area by $10.2\times$, bringing bulk impedance into a manageable range.
   - *Why Metals Differ:* Commercially pure titanium and 316L stainless steel have bulk resistivities of $4.2 \times 10^{-5}\text{ }\Omega\cdot\text{cm}$ and $7.4 \times 10^{-5}\text{ }\Omega\cdot\text{cm}$—**over six orders of magnitude lower than conductive TPU**. Bulk material resistance in a metal contact is essentially zero ($<0.001\text{ }\Omega$).
   - *Anatomical Constraint Behind the Ear:* The retroauricular crease has a tight radius of curvature ($R \approx 8–12\text{ mm}$). A rigid flat metal disc of 16 mm diameter **cannot sit flat against this curved surface**. Its edges lift, trapping hair and creating unstable air gaps under jaw motion.
   - *The Solution:* A **7.0–9.0 mm convex metal dome** provides the optimal mechanical compromise: it fits within the retroauricular groove without edge lift, while concentrating the shell's clamping force over a defined area to displace fine hair and establish a stable, low-impedance dry interface ($30–80\text{ k}\Omega$).

### 7.2 Repeatable Pressure Suspension Mechanisms

Dry biopotential contacts require a constant skin contact pressure of **10 to 25 kPa** (approximately $1.0–2.5\text{ N/cm}^2$ or $10–25\text{ mN/mm}^2$).
- Below $5\text{ kPa}$: Micro-motion artifacts dominate, and contact impedance fluctuates wildly.
- Above $35\text{ kPa}$: Local capillary blood flow is restricted, causing skin redness, pain, and pressure necrosis after 1–2 hours.

```
+-------------------------------------------------------+
|                RECOMMENDED SUSPENSION                 |
|                                                       |
|   [ Shell Rigid Wall ]                                |
|        |                                              |
|       [+] === Conductive Silicone Foam / Disc         |
|        |      (Shore 20A, 2 mm uncompressed)          |
|        |                                              |
|       ( ) === Grade 2 Titanium Dome Stud (7 mm dia)   |
|        |      Floating in a chamfered retaining lip   |
|   =====v===========================================   |
|              RETROAURICULAR SKIN                      |
+-------------------------------------------------------+
```

#### Recommended Three-Tier Suspension Architecture:
1. **Primary Gross Clamping Force (The Earhook Cantilever):**
   - The overall BTE pod shell utilizes an ergonomic C-shaped hook curving over the superior crus of the helix. The hook is modeled with an intentional **$1.5\text{ mm}$ inward interference bias** relative to the ear's relaxed retroauricular depth.
   - When slipped over the ear, the cantilever deflection generates **$0.8–1.2\text{ N}$ of total inward clamping force** distributed across the three contacts.
2. **Individual Contact Suspension (Micro-Compliance):**
   - Metal studs must not be epoxied rigidly into a stiff shell wall. A rigid mount cannot compensate for individual skull variations or dynamic skin stretching during jaw motion.
   - Each titanium stud is mounted through a clearance hole with a retaining bezel and backed by a **die-cut disc of closed-cell silicone foam** (e.g., Rogers Bisco HT-800, Shore 20A, thickness 2.0 mm).
   - Under nominal earhook clamping, the foam compresses by 0.8 mm, providing an independent suspension spring for each contact with a normal force of $0.3–0.4\text{ N}$ ($F/A \approx 15–20\text{ kPa}$ across a 7 mm dome).
3. **Internal Concha Wing Counter-Force (Stage C Integration):**
   - When the sound tube or canal tip is integrated, a semi-rigid silicone sports wing resting against the inner antihelix provides an opposing reaction force, locking the pod immovably against the skull.

### 7.3 Verification Protocol for Nickel-Free Certification

Because nickel is the most prevalent cause of allergic contact dermatitis (affecting ~15% of the human population), strict verification is mandatory before wearing:

1. **Tier 1: Mill Test Certificate (MTC) Verification (Before Purchase):**
   - For titanium hardware: Require supplier certification complying with **EN 10204 Type 3.1**. The certificate must document compliance with **ASTM F136** (Ti-6Al-4V ELI) or **ASTM F67** (Unalloyed CP Titanium) and explicitly state nickel content as $0.00\%$ (or below the detection limit of $<0.01\%$).
   - For stainless steel hardware: If 316L is used, the MTC must certify compliance with **ASTM F138** (implant grade 316LVM) with chemical analysis verifying $10.0–14.0\%$ Ni and full passivation per ASTM A967.
2. **Tier 2: Chemical Spot Testing (Upon Part Receipt):**
   - Perform a **Dimethylglyoxime (DMG) Test** (e.g., [Nickel Alert](https://nonickel.com/products/nickel-alert-test-kit) by Athena Allergy / Chemo Nickel Test).
   - *Protocol:* Apply two drops of the DMG ammoniacal solution to a clean white cotton swab. Rub the swab vigorously against the metal stud for 30–60 seconds.
   - *Pass Criteria:* Swab remains entirely colorless. If the swab turns pink or strawberry red, nickel is present and leaching at a concentration $>10\text{ ppm}$; the part is **immediately rejected**.
3. **Tier 3: European Reference Standard EN 1811:2011+A1:2015:**
   - EN 1811 is the internationally recognized European reference test for nickel release from skin-contact articles under REACH Annex XVII.
   - *Method:* The component is submerged in artificial sweat (aqueous solution of sodium chloride, urea, and DL-lactic acid adjusted to pH 6.5) and incubated at $30^\circ\text{C}$ for 1 week (168 hours). The solution is analyzed via Inductively Coupled Plasma Mass Spectrometry (ICP-MS).
   - *Threshold:* Must demonstrate $<0.5\text{ }\mu\text{g Ni/cm}^2/\text{week}$ for external skin contact items.

---

## 8. Open Questions for the Synthesis

1. **Electrode Boss Mechanical Retaining Geometry (Cross-lane with L1):**
   - Can `build123d` generate an internal retaining pocket that captures a 7 mm titanium stud with an elastomeric foam backing without requiring threaded hardware or glue? Does an internal snap-fit retaining ring provide sufficient retention against insertion pull-out forces?
2. **Shell Material Biocompatibility & Surface Finish (Cross-lane with L2):**
   - If the pod shell is fabricated via SLS PA12 Nylon from JLCPCB or PCBWay, what chemical vapor smoothing or dyeing process is certified skin-safe under ISO 10993 for chronic retroauricular wear?
3. **Internal Wire Harness vs. Rigid-Flex Termination (Cross-lane with L4):**
   - How do the three internal electrode leads terminate on the Stage B PCB? Does the PCB use soldered micro-coaxial pigtails, spring fingers ([Harwin](https://www.harwin.com/) S1721-46R) pressing against the back of the floating studs, or an integral rigid-flex tail with gold contact pads?
4. **Ear Canal Cross-Coupling in Stage C:**
   - In Stage C, when the sealed-tip pressure sensor and piezo mic enter the ear canal, will canal deformation from jaw movements induce mechanical artifacts into the BTE pod's electrode suspension?

---

## 9. Top 10 Sources

1. **Strauss et al. (2020) — Auriculomotor Activity and Auditory Attention**
   - *Publication:* "Vestigial auriculomotor activity indicates the direction of auditory attention in humans", *eLife* 9: e54536.
   - *DOI:* [10.7554/eLife.54536](https://doi.org/10.7554/eLife.54536)
   - *Annotation:* Foundational research demonstrating that the vestigial auriculomotor system (PAM and SAM) produces measurable surface EMG correlates of spatial attention. Details 10 mm bipolar Ag/AgCl montage, g.USBamp acquisition, and microvolt signal characteristics.

2. **Rüschenschmidt et al. (2022) — Extrinsic and Intrinsic Ear Muscle Electromyography**
   - *Publication:* "Electromyography of Extrinsic and Intrinsic Ear Muscles in Healthy Probands and Patients with Unilateral Postparalytic Facial Synkinesis", *Diagnostics* 12(1): 121.
   - *DOI:* [10.3390/diagnostics12010121](https://doi.org/10.3390/diagnostics12010121)
   - *Annotation:* Establishes anatomical coordinates, cadaver dissections, needle EMG hot spots, and surface EMG recording protocols for PAM, SAM, and AAM.

3. **Schroeer et al. (2023) — Auriculomotor Activity with In- and Around-Ear Electrodes**
   - *Publication:* "Assessment of Vestigial Auriculomotor Activity to Acoustic Stimuli Using Electrodes In and Around the Ear", *Trends in Hearing* 27: 1–14.
   - *DOI:* [10.1177/23312165231212873](https://doi.org/10.1177/23312165231212873)
   - *Annotation:* Proves that vestigial auriculomotor activity can be recorded using dry-contact electrodes in custom earpieces without skin preparation, bridging lab EMG to wearable hearing-aid hardware.

4. **Bleichner & Debener (2017) — cEEGrid Around-The-Ear Array Concept**
   - *Publication:* "Concealed, Unobtrusive Ear-Centered EEG Acquisition: cEEGrids for Transparent Monitoring", *Frontiers in Human Neuroscience* 11: 163.
   - *DOI:* [10.3389/fnhum.2017.00163](https://doi.org/10.3389/fnhum.2017.00163)
   - *Annotation:* Details the geometry, material design, screen-printed Ag/AgCl metallurgy, and clinical performance of the 10-channel around-the-ear flexprint array.

5. **Knierim et al. (2022) — Open-cEEGrid Low-Cost Biosensing Adapter**
   - *Publication:* "A simplified design of a cEEGrid ear-electrode adapter for the OpenBCI biosensing platform", *HardwareX* 12: e00300.
   - *DOI:* [10.1016/j.hardwarex.2022.e00300](https://doi.org/10.1016/j.hardwarex.2022.e00300)
   - *Annotation:* Open-source hardware implementation providing CAD models, flex-PCB Gerber files, and validation for around-the-ear EMG/EEG recording.

6. **NextSense Smartbuds Clinical EEG Launch (2026)**
   - *Product Reference:* NextSense Commercial Launch & Technical Specifications (February 2026).
   - *URL:* [https://nextsense.io/](https://nextsense.io/)
   - *Annotation:* Commercial validation of conductive silicone dry biopotential sensors with Tecticoat® coatings integrated into consumer in-ear earbuds for clinical sleep staging.

7. **IDUN Technologies Dryode™ Material Specifications**
   - *Product Reference:* IDUN Guardian In-Ear EEG Platform & Dryode Technical Whitepaper.
   - *URL:* [https://iduntechnologies.com/](https://iduntechnologies.com/)
   - *Annotation:* Industry benchmark for soft conductive polymer dry electrodes in the ear canal, establishing $<200\text{ k}\Omega$ dry impedance standards.

8. **EN 1811:2011+A1:2015 Nickel Release Reference Standard**
   - *Standard:* "Reference test method for release of nickel from all post assemblies which are inserted into pierced parts of the human body and articles intended to come into direct and prolonged contact with the skin."
   - *URL:* [European Chemicals Agency (ECHA) REACH Annex XVII Entry 27](https://echa.europa.eu/substances-restricted-under-reach/-/dislist/details/0b0236e1807e452a)
   - *Annotation:* Legal and technical reference defining artificial sweat immersion testing and the $<0.5\text{ }\mu\text{g/cm}^2/\text{week}$ biocompatibility threshold.

9. **McMaster-Carr Grade 2 Titanium Fasteners Catalog**
   - *Product Reference:* Grade 2 Commercially Pure Titanium Button Head Screws (ASTM F67).
   - *URL:* [https://www.mcmaster.com/products/screws/material~titanium/](https://www.mcmaster.com/products/screws/material~titanium/)
   - *Annotation:* Primary commercial source for guaranteed nickel-free, biocompatible dome-headed fasteners suitable as discrete dry electrodes.

10. **BioMed Electrodes Sintered Ag/AgCl Sensors**
    - *Product Reference:* Sintered Silver/Silver-Chloride Pellet and Disc Electrodes.
    - *URL:* [https://www.biomedelectrodes.com/](https://www.biomedelectrodes.com/)
    - *Annotation:* Commercial source and pricing for high-stability, non-polarizable biopotential sintered pellets with pre-attached pure silver leads.
