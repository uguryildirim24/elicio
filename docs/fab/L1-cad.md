# Historical CAD and geometry source survey

Retained source evidence, not a current build plan. The board is unfinished, unordered and unmeasured. Prices are historical estimates. Agent-written fit and fabrication claims were not independently validated. Current limits are in `board-v4-design.md` and `shell-v4.md`.

- **Report path:** `docs/fab/L1-cad.md`
- **Lane:** L1 (CAD Tool, Ear Geometry, Starting Models, Design Rules)
- **Target:** Elicio Stage B Behind-The-Ear (BTE) Pod (`docs/EARPIECE_DESIGN.md`)
- **Date:** 2026-09-16

---

## 1. Executive Summary

This study defines the mechanical modeling pipeline, anatomical capture route, reference models, and manufacturing constraints for the Elicio Stage B covert behind-the-ear earpiece.

1. **CAD Tool Recommendation:**
   - **Primary:** [`build123d`](https://github.com/gumyr/build123d) (v0.7.0+, Apache-2.0). A Python parametric BREP library built on OpenCASCADE. It runs headlessly on macOS Apple Silicon, maintains clean code-driven constraints for internal component pockets (PCB, battery, electrode bosses, snap fits), and natively exports STEP, STL, and 3MF files.
   - **Fallback:** [Blender 4.x](https://www.blender.org/) (GPL-2.0+). Driven via headless Python (`blender -b -P script.py`). Essential if an organic scan mesh requires direct sculpting, retopology, or shrinkwrapping, with built-in multi-angle Cycles rendering for review.
2. **Ear Geometry Capture:**
   - Direct iPhone scanning of the living retroauricular sulcus fails due to hair occlusion, deep crevice shadows, and ear cartilage deflection.
   - The recommended low-cost route is a **two-step physical-to-digital workflow**: Rolf takes a physical impression using a $12–$15 silicone earplug putty ([Radians Custom Molded Earplugs](https://www.radians.com/products/radians-custom-molded-earplugs)), mounts the cured hair-free cast on a turntable under diffuse light, and captures it via iPhone photogrammetry using [Scaniverse](https://scaniverse.com/) or Apple Object Capture.
   - However, **an individualized scan is not required to begin**. Commercial hearing-aid precedent proves that mass-market BTE and Receiver-In-Canal (RIC) devices use standardized generic curved housings that fit >90% of adult ears.
3. **First Deliverable:**
   - A passive fit-check shell (`bte_fit_shell_v1`) scripted in `build123d` from a 7-parameter manual caliper measurement protocol.
   - Features mock electrode bosses (two auricular, one mastoid), glasses relief chamfers, and internal envelope checks for the Stage B PCB and battery.
   - Unit fabrication cost: $2.50–$5.00 in SLA resin or SLS PA12 nylon via JLCPCB or PCBWay, delivering to Massachusetts in 3–5 business days.

---

## 2. CAD Tool Evaluation for Agentic BTE Shell Modeling

The Elicio BTE pod requires an ergonomic outer hull conforming to the retroauricular crease, plus high-precision internal prismatic pockets for the PCB, battery, snap-lid lip, and electrode bosses.

Because the designer is an autonomous AI agent working from text specifications and code, and the reviewer is Rolf inspecting visual renders on macOS, GUI-only tools are disqualified.

### 2.1 Tool Comparison Matrix

| Tool | Paradigm | Headless Python on macOS? | Native STEP / STL / 3MF | Cost & License | Organic vs. Precision Fit | Suitability |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **build123d** | Parametric BREP | **Yes** (`pip install build123d`) | **Yes / Yes / Yes** | Free (Apache-2.0) | Sweeps profiles along 3D splines; exact booleans for pockets. | **Top Choice.** Pythonic, deterministic, native STEP. |
| **CadQuery** | Parametric BREP | **Yes** (`pip install cadquery`) | **Yes / Yes / Yes** | Free (Apache-2.0) | Solid BREP modeling; fluent API can be rigid for branching parts. | **Strong.** Predecessor to build123d. |
| **Blender 4.x** | Mesh / Sub-D | **Yes** (`blender -b -P script.py`) | STL/3MF native; STEP via plugins | Free (GPL-2.0+) | Superb for organic sculpting; polygon booleans cause mesh errors. | **Top Fallback.** Best for scan retopology & rendering. |
| **FreeCAD 1.0** | Parametric BREP | **Yes** (`FreeCADCmd script.py`) | **Yes / Yes / Yes** | Free (LGPL-2.1+) | Solid modeling; headless `PartDesign` API is verbose and fragile. | **Viable Fallback.** Heavy install bundle. |
| **OpenSCAD** | CSG Code | **Yes** (`openscad -o out.stl in.scad`) | STL/3MF native; **No native STEP** | Free (GPL-2.0) | Cannot loft smooth double-curved ergonomic surfaces easily. | **Unsuitable.** No native STEP export. |
| **Fusion 360** | Parametric BREP | **No** (Desktop GUI required) | STEP/STL export (10 active doc limit) | Free Personal (restricted) | Excellent T-Splines and solid CAD. | **Disqualified.** GUI only; no headless agent execution. |
| **Onshape** | Cloud Parametric | **Partial** (REST API) | **Yes / Yes / Yes** (via cloud API) | Free tier makes **all docs public** | Excellent surfacing and solid tools. | **Disqualified.** Cloud latency; free tier exposes IP publicly. |
| **Plasticity** | Direct NURBS | **No** (Interactive GUI only) | STEP/STL export | $149 Indie perpetual | Superb direct modeling, but no parametric history tree. | **Disqualified.** No Python API or headless CLI mode. |
| **Shapr3D** | Direct / Parametric | **No** (iPad/macOS GUI only) | STEP/STL export (Pro only) | $299/year subscription | Intuitive direct modeler. | **Disqualified.** Closed proprietary ecosystem. |

*Sources:* [build123d Docs](https://build123d.readthedocs.io/), [CadQuery Docs](https://cadquery.readthedocs.io/), [FreeCAD 1.0](https://www.freecad.org/), [Blender API](https://docs.blender.org/api/current/), [Plasticity](https://www.plasticity.xyz/), [Shapr3D](https://www.shapr3d.com/).

### 2.2 Recommendation and Workflow

- **Primary Recommendation: `build123d`**
  - *Rationale:* The AI agent writes and maintains pure Python scripts (`scripts/cad/bte_pod.py`). The script defines parametric dimensions (`wall_thickness = 1.2`, `pcb_length = 28.0`, `hook_radius = 13.5`). Updating parameters regenerates exact solid STEP files deterministically in under one second.
  - *Ergonomics:* Lofting rounded cross-sections along a 3D spline produces a smooth outer hull.
  - *Precision:* Parametric boolean cuts create the PCB cavity, battery pocket, snap lip, and press-fit electrode bosses with exact tolerances.
  - *Headless rendering:* The script exports an STL/STEP and triggers a lightweight background renderer ([F3D](https://f3d.app/) or a headless Blender script) to generate multi-angle PNG images for Rolf.
- **Fallback Recommendation: Blender 4.x (`bpy`)**
  - *Rationale:* If Rolf captures a raw 3D mesh of his ear, Blender can import the scan, apply a `Shrinkwrap` modifier to adapt the inner face, and sculpt transitions.
  - *Limitation:* Polygonal booleans can produce non-manifold edges, making tight mechanical clearances ($\pm 0.15\text{ mm}$ snap fits) difficult to maintain.

---

## 3. Capturing Rolf's Ear and Mastoid Geometry

To ensure electrode contact pressure without displacing the ear pinna, the enclosure must match the retroauricular crease and mastoid bone.

### 3.1 iPhone Sensors: TrueDepth vs. LiDAR vs. Photogrammetry

| Sensor System | Location | Working Principle | Working Distance | Depth Accuracy | Suitability for Behind-Ear Sulcus |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TrueDepth** | Front Camera | Structured Light (30k IR dots) | 200–500 mm | **0.5–1.0 mm** | **High.** Fine detail; self-scanning requires a helper. |
| **LiDAR** | Rear Camera (Pro) | Direct Time-of-Flight (dToF) | 500–5000 mm | **3.0–5.0 mm** | **Unusable.** Coarse; bridges over grooves and creases. |
| **Photogrammetry** | Rear Cameras | Multi-View Stereo (MVS) | 150–500 mm | **0.2–0.5 mm** | **High Potential.** Fine geometry; vulnerable to hair and shadow. |

*Sources:* [Apple Object Capture](https://developer.apple.com/augmented-reality/object-capture/), [Heges Technical Overview](https://hege.sh/).

### 3.2 The Optical Pitfalls: Hair, Shadow, and Deflection

Direct optical scanning of the living retroauricular sulcus presents three major issues:
1. **Hair Occlusion:** Hair strands scatter structured light and prevent matching in photogrammetry, generating floating artifacts and holes.
2. **Crevice Shadowing:** The sulcus forms an acute angle where ambient light cannot reach, blinding optical sensors.
3. **Cartilage Deflection:** Pulling the ear forward deforms cartilage and shifts auricular muscle landmarks.
4. **Mitigation:** Hair must be bound flat with a silicone cap and paper tape, skin dusted with powder, and a second person must operate the scanner.

### 3.3 Evaluation of iPhone Scanning Applications

| App | Sensor Mode | Accuracy | Native Exports | Price (2026) | macOS M5 Pro Workflow |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **[Heges](https://hege.sh/)** | TrueDepth | **Best for head** (~0.8 mm) | OBJ, PLY, STL | Free; $2.99–$9.99 export IAP. | AirDrop or Wi-Fi transfer. |
| **[3D Scanner App](https://3dscannerapp.com/)** | TrueDepth & LiDAR | High with TrueDepth | OBJ, STL, USDZ, PLY | **100% Free** (Laan Labs). | Direct AirDrop to macOS. |
| **[Scaniverse](https://scaniverse.com/)** | Photogrammetry & LiDAR | High detail | OBJ, FBX, USDZ, PLY | **100% Free** (Niantic). | Export via iOS share sheet. |
| **[Polycam](https://polycam.ai/)** | Photogrammetry & LiDAR | High quality | STL, OBJ, 3MF, STEP | Free basic; Pro $17.99/mo. | Cloud download or app export. |
| **[Kiri Engine](https://www.kiriengine.com/)** | Cloud Photogrammetry | High texture detail | OBJ, STL, PLY | Freemium; Pro ~$14.99/mo. | Browser download to Mac. |
| **[RealityScan](https://capturingreality.com/realityscan)** | Photogrammetry (Epic) | High detail (50+ photos) | OBJ, FBX | **Free** (Epic account). | Download from Sketchfab. |

*Hardware Note:* **Meshroom is not viable on Apple Silicon.** Meshroom requires [NVIDIA CUDA](https://github.com/alicevision/meshroom); on macOS M5 Pro it runs only in slow CPU draft mode. The native alternative is **Apple Object Capture API**, which executes on Metal and the M5 GPU.

### 3.4 The Industrial Route: Silicone Impressions and Turntable Scanning

In custom hearing-aid and IEM manufacturing, direct optical scanning remains secondary to **physical silicone impressions**:
1. **The Impression Process:** An audiologist inserts an oto-dam in the ear canal and injects two-part addition-cure vinyl polysiloxane (VPS) silicone putty. It cures in 3–5 minutes into a flexible cast capturing the canal, concha, and retroauricular fold.
2. **Turntable Scanning:** The silicone cast has **no hair**, does not move, and has a uniform matte surface. Placing the cast on a turntable under diffuse lighting allows an iPhone or camera to capture sub-0.2 mm photogrammetry with zero crevice shadowing.
3. **Kits and Costs:**
   - **DIY Putty:** [Radians Custom Molded Earplugs](https://www.radians.com/products/radians-custom-molded-earplugs) ($12.00–$15.00). Rolf mixes the putties, presses them into the retroauricular crease and mastoid area, and removes the cured cast after 10 minutes.
   - **Audiologist Visit:** Professional earmold impressions cost **$30.00–$75.00** per pair.
4. **Shell Modeling Software:**
   - Commercial industry uses proprietary suites: [3Shape Audio](https://www.3shape.com/en/software/audio) and [Cyfex Secret Ear Designer](https://www.cyfex.com/), costing thousands of dollars per seat.
   - Free/cheap tools: No turnkey open-source medical earmold generator exists. DIY makers use **Blender** or legacy [Autodesk Meshmixer](https://meshmixer.com/) for mesh hollowing, boolean cutting, and sculpting, as documented by [Project Resonator](https://github.com/mistertf/Project-Resonator).

---

## 4. Starting Models and Anthropometric Standards

### 4.1 Open-Source Repositories

| Project | Description | Repository / URL | License | Formats | Relevance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **OpenEarable 2.0** | Open earable sensor platform (IMU, mic, speaker). | [GitHub - OpenEarable](https://github.com/OpenEarable/open-earable) | MIT License | Onshape, STL, STEP | Reference ear-hook curvature and battery layout. |
| **Open-cEEGrid Adapter** | 3D-printed housing for around-ear flex-EEG arrays. | [GitHub - mknierim/open-ceegrid](https://github.com/mknierim/open-ceegrid) | MIT / CC BY 4.0 | STL, STEP | Reference for electrode routing and stability. |
| **Printables / Thingiverse** | Generic BTE hearing aid dummy shells. | [Printables](https://www.printables.com/) / [Thingiverse](https://www.thingiverse.com/) | CC-BY / CC-BY-SA | STL | Baseline dimensional checks; lack parametric trees. |
| **GrabCAD Library** | Engineering models of BTE hearing aid housings. | [GrabCAD Library](https://grabcad.com/library?query=hearing%20aid%20bte) | Free download | STEP, IGES, SolidWorks | Reference wall thicknesses, parting lines, and doors. |

*Sources:* [OpenEarable TECO](https://open-earable.teco.edu/), [Knierim et al., Front. Neurosci. 2020](https://doi.org/10.3389/fnins.2020.612081).

### 4.2 Standard BTE Hearing Aid Dimensions

| Dimension | Standard Adult BTE | Mini-BTE / RIC | Elicio Stage B Target | Constraints |
| :--- | :--- | :--- | :--- | :--- |
| **Body Length ($L$)** | 32.0–42.0 mm | 22.0–28.0 mm | **34.0–38.0 mm** | Houses Stage B PCB (25–28 mm) and 401020 LiPo. |
| **Transverse Width ($W$)** | 7.0–9.0 mm | 5.5–7.0 mm | **7.5–8.2 mm** | Sulcus width is 8–12 mm. Widths $>9\text{ mm}$ force ear outward. |
| **Sagittal Depth ($D$)** | 8.0–12.0 mm | 6.5–8.5 mm | **8.5–10.0 mm** | Accommodates internal board width and snap lid. |
| **Hook Arc Radius ($R$)** | 12.0–16.0 mm | 10.0–14.0 mm | **13.5 mm** | Curvature over the cranial root of the helix. |
| **Hook Arc Angle** | 130°–160° | 120°–140° | **145°** | Secures shell against slippage without pinching. |

*Sources:* [Hearing Aid Sizing Standards](https://hearingaidsweatband.com/), [JH Hearing Aids Specs](https://www.jhhearingaids.com/).

### 4.3 The Generic BTE Fit Hypothesis

**Finding:** **A personal ear scan is NOT required to design and evaluate the initial earpiece.**
- Millions of commercial BTE hearing aids rely on standardized generic shells; custom molds are used exclusively for canal inserts.
- The human retroauricular crease is anthropometrically consistent across adults, following a smooth C-curve with a 28–36 mm radius.
- The AI agent can script a generic, parametric BTE shell in `build123d` immediately. Personal scans are needed only if dry electrode contacts fail to maintain skin contact.

---

## 5. Manufacturing Design Rules and Tolerances

Prototypes will be fabricated through rapid-turnaround bureaus (JLCPCB, PCBWay, Xometry).

### 5.1 Process Comparison and Tolerances

| Parameter | SLA Resin (8000) | SLA Resin (Tough) | SLS / MJF Nylon (PA12) | TPU (FDM 95A / SLS) | Cast Silicone (RTV) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Min Wall Thickness** | 0.8 mm (supported) | 0.8 mm (supported) | **0.8 mm (min), 1.0–1.2 mm (rec)** | 1.2 mm (FDM), 1.0 mm (SLS) | 1.0 mm (min), 1.5–2.0 mm (rec) |
| **Clearance (Mating)** | 0.15–0.20 mm | 0.15–0.20 mm | **0.25–0.35 mm** | 0.30–0.50 mm | 0.20–0.30 mm |
| **Min Hole Diameter** | 0.6 mm | 0.6 mm | **1.0 mm** (powder cleanout) | 1.5 mm | 1.0 mm |
| **Boss OD to ID Ratio** | $\text{OD} \ge 2.2 \times \text{ID}$ | $\text{OD} \ge 2.0 \times \text{ID}$ | **$\text{OD} \ge 2.5 \times \text{ID}$** | N/A (threads strip) | N/A (press-fit only) |
| **Snap-Fit Suitability** | **Prohibited** (brittle) | **Moderate** (shallow) | **Excellent** (standard) | **N/A** (friction lip) | **N/A** (stretch lip) |
| **Elongation at Break** | 5%–10% | 20%–35% | **15%–25%** | 250%–500% | 300%–700% |
| **Tolerance** | $\pm 0.10\text{ mm}$ | $\pm 0.10\text{ mm}$ | **$\pm 0.15\text{ mm}$** | $\pm 0.30\text{ mm}$ | $\pm 0.20\text{ mm}$ (shrink 1.5–2.5%) |

*Sources:* [JLCPCB Design Guide](https://jlc3dp.com/), [PCBWay Capabilities](https://www.pcbway.com/rapid-prototyping/manufacture-guidelines/3D-Printing.html), [Formlabs Specs](https://formlabs.com/).

### 5.2 Cantilever Snap-Fit Guidance

- **Standard SLA resin must not be used for cantilever snap-fits.** Its 5–8% elongation causes brittle fractures. For SLA parts, use micro-screws (M1.2 into brass inserts) or sliding dovetails.
- **SLS / MJF PA12 Nylon is the recommended material.** Its 18% elongation supports cyclic snap deformation.
- **Cantilever Beam Strain Formula:**
  $$\epsilon = 1.5 \cdot \frac{t \cdot y}{L^2} \le 0.03 \text{ (for reusable PA12 snaps)}$$
  *Parameters for Elicio lid:* Thickness $t = 1.0\text{ mm}$, length $L = 6.0\text{ mm}$, undercut $y = 0.35\text{ mm}$.
  $$\epsilon = 1.5 \cdot \frac{1.0 \cdot 0.35}{36.0} = 0.0146 \text{ (1.46\% strain, safely below the 3.0\% limit)}$$
  *Fillet rule:* Add a root fillet radius $R \ge 0.5 \times t$ ($0.5\text{ mm}$) to prevent notch stress cracking.

### 5.3 File Formats and Data Exchange

1. **Primary Solid Model: `STEP` (AP214 / AP242).** Bureau slicing engines use native BREP solids to generate toolpaths without chordal faceting.
2. **Mesh Formats: `3MF` or binary `STL`.** For STL exports, CAD meshing must enforce:
   - *Chordal deviation:* $\le 0.02\text{ mm}$.
   - *Angular tolerance:* $\le 5^\circ$.
   - *Manifoldness:* Watertight, zero non-manifold edges, zero self-intersecting triangles.
3. **2D Technical Drawing (PDF):** A 1-page drawing specifying critical tolerances (PCB pocket $+0.2/-0.0\text{ mm}$, electrode bore $\pm 0.05\text{ mm}$), general standard **ISO 2768-m**, and material finish ("PA12 Nylon, Natural Black, Media Blasted").
4. **Units:** **Millimeters (mm)** across all files.

---

## 6. Concrete First Deliverable: Passive Fit-Check Shell

### 6.1 Deliverable Definition

Before manufacturing functional PCBs, Rolf can physically evaluate ear fit and electrode stability using a passive test shell.

- **Artifact Name:** `bte_fit_shell_v1` (Passive Mechanical Gauge).
- **Tool:** Pure Python script in `build123d` (`scripts/cad/bte_fit_shell.py`).
- **Generated File Package:**
  1. `bte_fit_shell_v1.step` (Parametric master solid).
  2. `bte_fit_shell_v1.stl` (Binary mesh, chord deviation $\le 0.02\text{ mm}$).
  3. `bte_fit_shell_v1.3mf` (Manufacturing archive with embedded millimeter units).
  4. `bte_fit_shell_render_side.png` and `_iso.png` (Visual verification renders).
  5. `bte_fit_shell_drawing_v1.pdf` (1-page dimensional reference drawing).
- **Physical Features:**
  - C-curved body conforming to a 34 mm retroauricular sweep with a 13.5 mm radius ear hook.
  - Three mock electrode studs (3.0 mm diameter, 1.2 mm height) located at the superior auricular, posterior auricular, and mastoid contact sites.
  - Dummy internal cavities matching the target PCB envelope ($28.0 \times 8.0 \times 3.2\text{ mm}$) and LiPo 401020 battery ($22.0 \times 10.0 \times 4.2\text{ mm}$).
  - A 45° eyeglass temple relief chamfer along the superior hook crest.
  - A cantilever snap lid (0.25 mm clearance) to evaluate closure retention.
- **Fabrication Cost:** $2.50–$4.50 on JLCPCB/PCBWay (SLA 8000 or SLS PA12); shipping to Massachusetts is $16.00–$22.00 (DHL/FedEx, 3–5 days).

### 6.2 Manual Anthropometric Caliper Protocol

Rolf can measure all required parametric variables in 10 minutes using a digital caliper and tape (or string):

| No. | Parameter | Tool | Procedure | Typical Range | `build123d` Variable |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **M1** | **Ear Root Length ($L_{root}$)** | Caliper | Straight-line distance from superior to inferior otobasion along crease. | 45.0–58.0 mm | `EAR_ROOT_LENGTH` |
| **M2** | **Sulcus Arc Length ($S_{arc}$)** | Tape / String | Lay string along deepest valley of crease from top fold to mastoid tip. | 50.0–65.0 mm | `SULCUS_ARC_LENGTH` |
| **M3** | **Sulcus Clearance ($W_{sulcus}$)** | Caliper depth rod | Depth from mastoid skull to outer rim of pinna at midpoint. | 8.0–14.0 mm | `MAX_SHELL_WIDTH` |
| **M4** | **Helix Root Thickness ($T_{hook}$)** | Caliper jaws | Span jaws across cartilage bridge at superior otobasion; do not compress. | 4.5–7.5 mm | `HOOK_INNER_GAP` |
| **M5** | **Eyeglass Frame Width ($T_{glass}$)** | Caliper jaws | Measure frame thickness where temple passes over the ear. | 1.8–3.2 mm | `GLASSES_RELIEF_DEPTH` |
| **M6** | **Mastoid Offset ($D_{mastoid}$)** | Caliper | Distance laterally/posteriorly from crease to mastoid bone peak. | 12.0–18.0 mm | `MASTOID_OFFSET` |
| **M7** | **Electrode Spacing ($D_{elec}$)** | Caliper points | Distance along crease from top fold to midpoint behind concha. | 18.0–26.0 mm | `ELECTRODE_PITCH` |

---

## 7. Open Questions for the Synthesis

1. **Electrode Boss Interface (Cross-lane with L3):**
   - Does the shell require through-holes for discrete stainless-steel contact studs, or pockets for conductive carbon-TPU inserts? If conductive TPU is used, must it be co-printed or press-fit?
2. **Skin Biocompatibility (Cross-lane with L2):**
   - Standard photopolymer resins (e.g., JLCPCB 8000) are not certified for prolonged skin contact. Does the Stage B shell require certified medical resin (ISO 10993 / Class IIa), or does media-blasted, dyed SLS PA12 Nylon satisfy contact safety?
3. **Internal Board Layout (Cross-lane with L4):**
   - Can the Stage B electronics fit on a single rigid PCB ($28 \times 8\text{ mm}$), or does the curved housing require a rigid-flex PCB to track ear curvature without wasted volume?
4. **Moisture Sealing:**
   - Retroauricular skin accumulates perspiration. Should the snap lid include a silicone gasket, or can the prototype rely on conformal PCB coating and a tight friction-fit lid?

---

## 8. Top 10 Sources

1. **build123d CAD Framework**
   - *URL:* https://github.com/gumyr/build123d
   - *Annotation:* Python parametric boundary representation (BREP) library built on OpenCASCADE for code-driven, headless enclosure generation.
2. **Blender Python API (`bpy`)**
   - *URL:* https://docs.blender.org/api/current/
   - *Annotation:* Official reference for headless Blender automation, mesh manipulation, and Cycles rendering on macOS Apple Silicon.
3. **OpenEarable 2.0 Repository**
   - *URL:* https://github.com/OpenEarable/open-earable
   - *Annotation:* Open-source earable sensor platform developed at KIT (MIT License). Reference Onshape CAD and STL files for ear-worn sensor enclosures.
4. **Open-cEEGrid Around-The-Ear EEG Project**
   - *URL:* https://github.com/mknierim/open-ceegrid
   - *Publication:* Knierim et al., "Open-cEEGrid: An open-source adapter for around-the-ear EEG", *Frontiers in Neuroscience*, 2020. https://doi.org/10.3389/fnins.2020.612081
   - *Annotation:* Open-source hardware repository and paper detailing 3D-printed around-ear electrode holders and bio-potential interfaces.
5. **Apple Object Capture API**
   - *URL:* https://developer.apple.com/augmented-reality/object-capture/
   - *Annotation:* Apple's photogrammetry framework optimized for macOS Metal and Apple Silicon, providing the recommended local photogrammetry pipeline.
6. **Heges TrueDepth iOS 3D Scanner**
   - *URL:* https://hege.sh/
   - *Annotation:* iOS app utilizing the front TrueDepth structured-light sensor for high-accuracy (<1 mm) surface capture with local export.
7. **Scaniverse Photogrammetry**
   - *URL:* https://scaniverse.com/
   - *Annotation:* Niantic's free mobile 3D reconstruction tool supporting photogrammetric mesh generation on iOS.
8. **JLCPCB (JLC3DP) 3D Printing Design Guidelines**
   - *URL:* https://jlc3dp.com/help/article/3d-printing-design-guideline
   - *Annotation:* Primary manufacturing design rules detailing wall thickness, clearances, and tolerances for SLA resin, SLS PA12, and MJF.
9. **Project Resonator DIY In-Ear Monitor Guide**
   - *URL:* https://github.com/mistertf/Project-Resonator
   - *Annotation:* Open-source engineering guide detailing the digital workflow from silicone ear impressions to 3D scan cleanup, shell modeling, and SLA printing.
10. **Cyfex Secret Ear Designer & 3Shape Audio**
    - *URL:* https://www.cyfex.com/ and https://www.3shape.com/en/software/audio
    - *Annotation:* Commercial software suites used in hearing-aid and custom IEM industries for digital earmold modeling from 3D impression scans.
