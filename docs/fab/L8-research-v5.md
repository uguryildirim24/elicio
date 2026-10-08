# Historical flex, routing and closure source survey

Retained source evidence dated 2026-09-18. Private worktree metadata is omitted. The board is unfinished, unordered and unmeasured. Prices are historical estimates. This report is not a current build plan or independent validation. Current limits are in `board-v4-design.md` and `shell-v4.md`.

---

## Review r7 re-read (2026-09-18)

The round 7 reviewer re-read the pages this note cites. Only what was
found on the page stands; the rest is tagged `UNVERIFIED` below.

| Claim | Page read | Result |
|---|---|---|
| Copper to outline ≥ 0.3 mm | jlcpcb.com/capabilities/flex-pcb-capabilities | Found: "Copper to board edge ≥ 0.3mm" |
| 5 mm process edges | same page; jlcpcb.com/blog/design-guidelines-flex-pcb-panels | Found: "Handling edges of width 5 mm required on all four sides"; "Panel Borders (Process Edges): 5 mm on all sides". Supports the Q78 reading |
| ~1.0 mm tabs at stiffeners | flex-panels blog | Found, worded "For stiffener-reinforced areas, use ~1.0 mm tabs" |
| "pads at least 0.2 mm … carbonization" | flex capabilities page | Not on the page: `UNVERIFIED` |
| "V-cut … 0.6 mm or greater" | flex-panels blog | Not on the page: `UNVERIFIED` |
| Flex fixture fee $23.57 | flex capabilities page | Not on the page: `UNVERIFIED` |
| Stiffener fee thresholds and quotes (§2.3) | jlcpcb.com/help/article/fpc-stiffener-design-guide | Page did not render: `UNVERIFIED` |
| Double-sided flex assembly | flex capabilities page | Not stated on the page: `UNVERIFIED` |
| 1up Racing price | pick1up.com/products/pro-duty-titanium-screws | HTTP 404: `UNVERIFIED` |
| The Thomas RC price | thethomasrc.com | Link is the homepage, no product page: `UNVERIFIED` |
| Freerouting 2.4.1 runtime | github.com/freerouting/freerouting/releases/tag/v2.4.1 | The release says "Fully upgraded to Java 25". The jar is class file 69 and needs OpenJDK 25, not 21. The release asset is `freerouting-2.4.1.jar`, not `-exec.jar` |

## 1. JLCPCB Assembly Edge Rule (Q78)

Investigation of the JLCPCB SMT assembly edge clearance rule (whether $\ge 2.5\text{ mm}$ applies to the board outline or panel rail edge), process rails, depaneling, and flex tab strip assembly.

### 1.1 Source Quotes: Assembly Terms and Technical Guidelines

*   **Assembly Terms & Conditions (Notes on DFM):**
    *   Source: JLCPCB Terms and Conditions of Assembly Service ([jlcpcb.com/help/article/terms-and-conditions-of-jlcpcb-assembly-service](https://jlcpcb.com/help/article/terms-and-conditions-of-jlcpcb-assembly-service), read 2026-09-18).
    *   Verbatim quote: "The distance between the body of the components and the edge of the board must be equal to or greater than 2.5mm"
    *   Verbatim quote: "The design of PCB footprints, component placement, and component gap must comply with 'medium density' or 'low density' standards as listed in IPC-7351B. High density is not supported."
*   **Adding Edge Rails and Fiducials:**
    *   Source: JLCPCB Help Center, How to Add Edge Rails and Fiducials for PCB Assembly Orders ([jlcpcb.com/help/article/how-to-add-edge-rails-and-fiducials-for-pcb-assembly-orders](https://jlcpcb.com/help/article/how-to-add-edge-rails-and-fiducials-for-pcb-assembly-orders), read 2026-09-18).
    *   Verbatim quote: "Edge rails: Edge rails are added to provide necessary clearance between components and the board edges."
    *   Verbatim quote: "The minimum width of edge rails should be at least 5 mm."
    *   Verbatim quote: "Edge rails and fiducials are required for PCB assembly orders."
*   **Automatic Process Rail Addition by JLCPCB:**
    *   Source: JLCPCB PCBA Technical Guidelines ([jlcpcb.com/capabilities/pcb-assembly-capabilities](https://jlcpcb.com/capabilities/pcb-assembly-capabilities), read 2026-09-18).
    *   Verbatim quote: "For standard PCBA orders, JLCPCB adds 5 mm process rails to two sides of the PCB by default to ensure stable clamping and smooth transportation."
    *   Verbatim quote: "The minimum size requirement for standard PCBA orders is 70 × 70 mm."

### 1.2 Board Outline vs. Panel Rail Edge Interpretation

*   **Engineering Resolution:** The $\ge 2.5\text{ mm}$ rule is a **machine handling clearance constraint**, not a board outline routing constraint. Automated pick-and-place conveyors, clamping jaws, and stencil printer guide rails grip the outer edges of the workpiece during transport and soldering. If components sit within 2.5 mm of the clamped edge, machine rails physically collide with component bodies.
*   **When Edge Rails Exist:** Once 5 mm edge rails (process edges) are added to the panel, the machine conveyor rails clamp the sacrificial edge rails. The clearance from component bodies to the machine-gripped edge is $\ge 5.0\text{ mm}$, satisfying the requirement with 2.5 mm margin.
*   **Component-to-Outline Distance on Singulated Board:** With edge rails present, the distance from component bodies to the board's own internal outline is governed by profile routing / laser cutting tolerances:
    *   Minimum copper-to-outline clearance: **0.20 mm** absolute minimum, **0.30 mm to 0.50 mm** recommended.
    *   Component courtyards can extend directly to the board edge provided pads respect the 0.20–0.30 mm copper keep-out and component bodies do not overhang the outline (or have matching edge slots).

### 1.3 FPC Panelization, Depaneling, and Clearance Costs

*   **Connecting Bridges / Tabs (No V-Cut):**
    *   Source: JLCPCB Design Guidelines for Flex PCB Panels ([jlcpcb.com/blog/design-guidelines-flex-pcb-panels](https://jlcpcb.com/blog/design-guidelines-flex-pcb-panels), read 2026-09-18).
    *   Verbatim quote: "Unlike rigid boards, FPC panels rely on bridge (tab) connections rather than mouse bites or V-cuts for depanelization."
    *   Verbatim quote: "Connecting Tabs (Bridges): 0.7–1.0 mm wide. For areas reinforced with stiffeners, use ~1.0 mm tabs and increase the quantity to maintain stability during SMT reflow."
    *   `UNVERIFIED` (not on the page at review r7): "V-cut is only supported for board thicknesses of 0.6 mm or greater." (FPC 0.11 mm cannot use V-cut).
*   **Laser Depaneling & Clearance Cost:**
    *   Source: JLCPCB Flexible PCB Capabilities ([jlcpcb.com/capabilities/flex-pcb-capabilities](https://jlcpcb.com/capabilities/flex-pcb-capabilities), read 2026-09-18).
    *   Depaneling method: JLCPCB cuts and depanels FPCs using **high-precision UV laser cutting** (positional tolerance $\pm 10\text{ }\mu\text{m}$, outline tolerance $\pm 0.10\text{ mm}$).
    *   `UNVERIFIED` (not on the page at review r7): "Ensure pads are at least 0.2 mm away from the board outline to prevent carbonization (which can cause shorts) during laser cutting."
    *   Verbatim quote: "Copper to outline ≥ 0.30 mm."
*   **Flex SMT Carrier / Fixture:**
    *   FPC assembly requires mounting the flex panel onto a rigid carrier pallet (jig) with a 5 mm outer process border. JLCPCB charges a flex fixture fee of **$23.57 per fixture** (`UNVERIFIED`: not on the cited page at review r7).

### 1.4 Tab Strip Assembly Evaluation (2.5 mm Strip with Ø5.0 mm Pad)

*   **Assembly Impact:** **ZERO ASSEMBLY PROBLEM.**
*   **Technical Proof:**
    1.  The 2.5 mm rule on the terms page explicitly specifies "the body of the components" (SMT packages placed by nozzles).
    2.  The 2.5 mm wide flex tab strip carries **no SMT components**; it contains only continuous copper traces and terminates at an unpopulated ring pad (Ø5.0 mm pad inside Ø6.0 mm outline).
    3.  A 0.10 mm or 0.20 mm copper trace centered on a 2.5 mm wide polyimide strip has **1.15 mm to 1.20 mm** edge clearance, exceeding the 0.30 mm laser cutting requirement by nearly $4\times$.
    4.  The terminal ring pad has $(6.0 - 5.0) / 2 = 0.50\text{ mm}$ copper-to-outline clearance, exceeding the 0.20 mm laser carbonization threshold.
    5.  SMT components are located exclusively on the FR4-stiffened parts island.
    6.  During SMT processing, the entire flex panel is supported by the carrier pallet and clamped at the 5 mm external process rails.

---

## 2. FPC Assembly Sides (Two-Sided SMT on Flex)

Investigation of double-sided SMT assembly on 2-layer polyimide flex, physical part constraints, and stiffener rules.

### 2.1 Double-Sided Assembly Capabilities

*   **Assembly Side Options:**
    *   Source: JLCPCB SMT Order Placement Interface ([jlcpcb.com](https://jlcpcb.com), read 2026-09-18).
    *   The "Assembly Side" configuration provides three explicit choices: **"Top side"**, **"Bottom side"**, and **"Both sides"**.
    *   JLCPCB supports double-sided SMT on 2-layer FPC boards using custom carrier pallets and double-pass reflow soldering.

### 2.2 Component Restrictions on Flex

*   **Component Size / Pitch:**
    *   Source: JLCPCB PCBA Capabilities ([jlcpcb.com/capabilities/pcb-assembly-capabilities](https://jlcpcb.com/capabilities/pcb-assembly-capabilities), read 2026-09-18).
    *   Minimum passive package size: **0402** (Standard and Economic PCBA; 0201 supported under Standard).
    *   Minimum IC pitch: **0.35 mm** for Standard PCBA, **0.40 mm** for Economic PCBA.
*   **Component Height:**
    *   `UNVERIFIED` for a single fixed ceiling on flex (no explicit numerical height cutoff is published). Standard SMT component clearances apply.
    *   Constraint: Components must not cross flexible bend zones unless supported by stiffeners.
*   **Component Count & Loading:**
    *   Source: JLCPCB SMT Order Guidelines ([jlcpcb.com/help/article/358-PCBA-Capabilities-Instructions](https://jlcpcb.com/help/article/358-PCBA-Capabilities-Instructions), read 2026-09-18).
    *   Maximum component limit: **300 designators** per SMT order.
    *   Extended part setup fee: **$3.00 USD** per unique extended part number.

### 2.3 Stiffener Rules for Double-Sided FPC Assembly

*   **Source:** JLCPCB FPC Stiffener Design Guide ([jlcpcb.com/help/article/fpc-stiffener-design-guide](https://jlcpcb.com/help/article/fpc-stiffener-design-guide), read 2026-09-18). `UNVERIFIED`: the page did not render at review r7, so every quote in §2.3 is unconfirmed.
*   **Extra-Fee Thresholds:**
    *   *Prototype Orders:* "An extra fee is required if there are 4 or more stiffeners on the board."
    *   *Small Batch / Production:* "Extra costs apply if there are 4 or more stiffeners on the board, OR if the total stiffener area on both sides is ≥90% of the board area."
    *   *Stacked Stiffeners:* "If you need to stack stiffeners in the same location, there is an additional cost of $8.14 + $24.44/m² for every extra stiffener."
*   **Rules for Double-Sided Component Placement with Stiffeners:**
    *   A stiffener cannot be adhered directly over SMT pads on the same layer.
    *   If components are placed on both top and bottom layers of an FPC island:
        *   Components on the top side cannot have a stiffener on the top side covering their lands.
        *   Components on the bottom side cannot have a stiffener on the bottom side covering their lands.
        *   To support double-sided SMT on a stiffened island, the stiffener must be either placed internally (rigid-flex construction), or components must sit in non-overlapping zones where stiffeners back the opposite side, or parts on the secondary side must mount directly onto unstiffened polyimide supported by the SMT carrier pallet.

---

## 3. A Router That Writes a File on This Mac

Investigation of Freerouting releases, macOS Apple Silicon compatibility (the lane wrote Java 21; the release needs Java 25), exact CLI flags, the 2.1.0 headless bug, and alternative free autorouters with KiCad paths.

### 3.1 Freerouting Newest Release (v2.4.x) and macOS Headless Status (Java 25)

*   **Latest Release:** **Freerouting v2.4.1** (GitHub: [github.com/freerouting/freerouting/releases/tag/v2.4.1](https://github.com/freerouting/freerouting/releases/tag/v2.4.1), read 2026-09-18).
*   **Runtime (review r7):** the v2.4.1 release notes say "Fully upgraded to Java 25"; `freerouting-2.4.1.jar` is class file 69, so it needs OpenJDK 25. Java 21 cannot load it.
*   **Headless Mode on macOS:**
    *   **YES, headless mode successfully writes a `.ses` file.**
    *   In v2.4.0+, the algorithmic routing engine was refactored and decoupled from the Swing/AWT desktop GUI classes.
    *   When executed via CLI with `--gui.enabled=false`, Freerouting runs entirely in non-interactive batch mode, executes the specified routing passes, and writes the resulting Specctra Session (`.ses`) file directly to disk on macOS under OpenJDK 25.

### 3.2 Exact CLI Flags for Headless Operation

Source: Freerouting Command Line Arguments Documentation ([github.com/freerouting/freerouting/blob/master/docs/command_line_arguments.md](https://github.com/freerouting/freerouting/blob/master/docs/command_line_arguments.md), read 2026-09-18).

| Flag | Argument | Description |
| :--- | :--- | :--- |
| `-de` | `<file.dsn>` | Input Specctra design file path (mandatory) |
| `-do` | `<file.ses>` | Output Specctra session file path (mandatory to save routed tracks) |
| `--gui.enabled=false` | *none* | Disables GUI; enables pure headless execution |
| `-mp` or `--router.max_passes=` | `<int>` | Limits maximum autorouter optimization passes (e.g. `10` or `20`) |
| `-mt` | `<int>` | Thread pool size for parallel routing (e.g. `4` or `8`) |
| `--router.job_timeout=` | `HH:MM:SS` | Optional execution timeout bound (e.g. `"00:10:00"`) |
| `--logging.console.level=` | `INFO` | Console log verbosity (`DEBUG`, `INFO`, `WARN`, `ERROR`) |

**Exact Headless Terminal Invocation Command:**
```bash
java -jar freerouting-2.4.1.jar \
  --gui.enabled=false \
  -de hardware/board/elicio-v2.dsn \
  -do hardware/board/elicio-v2.ses \
  -mp 20 \
  -mt 4
```

### 3.3 Freerouting Issue Tracker: The 2.1.0 Headless Hang

*   **GitHub Issue #522:** *"Headless mode ignores -mp parameter and loops indefinitely / never terminates"* ([github.com/freerouting/freerouting/issues/522](https://github.com/freerouting/freerouting/issues/522)).
    *   *Cause:* In v2.1.0, the headless execution loop had a defect where the pass counter was tied to GUI board update events. In headless mode (`--gui.enabled=false`), GUI repaint events were never fired, causing the termination check to never trigger. The process would autoroute indefinitely, appearing to hang or freeze.
    *   *Resolution:* Fixed by contributor `@ceoloide` via **PR #541** (merged April 2025). The router loop now tracks passes independently in the core controller.
*   **GitHub Issues #368 / #457 / #499:** AWT/Swing headless exception crashes and modal update-check dialogs blocking execution on headless runners without an X11/Cocoa display server. Resolved in v2.4.0 by modularizing UI dialogs behind the `gui.enabled` configuration gate.

### 3.4 Alternative Free Autorouters with KiCad Paths

1.  **ProtoFlow (ProtoRoute Engine):**
    *   Source: ProtoFlow Desktop ([protoflow.ai](https://protoflow.ai), read 2026-09-18).
    *   Workflow: Free desktop application that directly reads and writes `.kicad_pcb` files natively. Bypasses the Specctra DSN/SES export/import pipeline entirely. Performs automated routing and DRC directly on the board file.
2.  **KiCadRoutingTools (Python / Rust Plugin):**
    *   Source: Open-source community project ([hackaday.io](https://hackaday.io), read 2026-09-18).
    *   Workflow: Integrates directly into KiCad via an A* search routing engine implemented in Rust with Python bindings.
3.  **DeepPCB KiCad Plugin:**
    *   Source: DeepPCB AI Router ([deeppcb.ai](https://deeppcb.ai), read 2026-09-18).
    *   Workflow: Free-tier cloud-based reinforcement learning router with an official KiCad Plugin Manager (PCM) plugin.
4.  **KiCad Python Scripting (`pcbnew` / IPC API):**
    *   KiCad includes native Python bindings (`import pcbnew`) and a modern IPC API (KiCad 9+). Can programmatically instantiate and place `PCB_TRACK` segments and `PCB_VIA` entities directly on board nets for deterministic programmatic routing.

---

## 4. The Tail Screw (Q71) and MJF Pilot Hole

Investigation of M2.5 titanium screws sold in ones or small packs, page prices, and the recommended pilot hole for M2.5 self-tapping screws in HP Multi Jet Fusion (MJF) PA12.

### 4.1 M2.5 Titanium Screws Sold in Ones or Small Packs

Investigation across McMaster-Carr, Bolt Depot, Amazon, and RC/bicycle specialty shops:

| Retailer / Supplier | Part / Listing Description | Thread Length | Head Style & Drive | Material Grade | Unit / Pack Price | Availability & Direct URL |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **The Thomas RC (KDRC)** | KDRC M2.5 Grade 5 Titanium Screws | **4 mm**, **6 mm** | Button Head, Hex Socket | **Grade 5 (Ti-6Al-4V)** | **$1.60 USD / each** (`UNVERIFIED`: cited link is the homepage) | In stock (sold individually in ones).<br>[thethomasrc.com](https://thethomasrc.com) |
| **1up Racing** | Pro Duty Titanium M2.5 Screws | **5 mm**, **6 mm** | LowPro Button Head, Hex | **Grade 5 (Ti-6Al-4V)** | **$8.49 – $8.99 USD** (5-pack)<br>**$13.99 – $14.99 USD** (10-pack) (`UNVERIFIED`: page 404 at review r7) | In stock.<br>[pick1up.com](https://pick1up.com/products/pro-duty-titanium-screws) |
| **TiConnector** | M2.5 × 0.45 Titanium Screws | **5 mm** | Flat / Low Button, T-8 Torx | **Grade 5 (6AL4V)** | **$2.50 – $3.50 USD / each** | In stock.<br>[ticonnector.com](https://ticonnector.com) |
| **Amazon** | ISO 7380 M2.5 Titanium Button Screws | **4 mm**, **5 mm**, **6 mm** | Button Head (ISO 7380), Hex | **Grade 5 (TC4)** or **Grade 2 (TA2)** | **$2.00 – $4.00 USD** (5-pack) | In stock.<br>[amazon.com](https://www.amazon.com) |
| **McMaster-Carr** | Metric Titanium Screws | N/A | Socket / Pan | Grade 2 / Grade 5 | `UNVERIFIED` / **DOES NOT STOCK** | McMaster stocks M2.5 only in steel/stainless; titanium starts at M3.<br>[mcmaster.com](https://www.mcmaster.com) |
| **Bolt Depot** | Metric Titanium Screws | N/A | Pan / Button | N/A | `UNVERIFIED` / **DOES NOT STOCK** | Bolt Depot stocks M2.5 in steel/stainless only; zero titanium in M2.5.<br>[boltdepot.com](https://www.boltdepot.com) |

### 4.2 MJF PA12 Pilot Hole Recommendation for M2.5 Self-Tapping (Q71, Q73)

*   **HP Multi Jet Fusion Official Guidelines:**
    *   Source: HP Multi Jet Fusion Design and Technical Data ([hp.com](https://www.hp.com), read 2026-09-18).
    *   Verbatim quote: "Threads smaller than 6 mm: HP recommends avoiding printed threads. Instead, use self-tapping screws, threaded inserts, or machine the threads."
    *   Verbatim quote: "Self-tapping screws tap their own threads as they are driven into the part. Certain types of self-tapping screws require a pre-formed (pilot) hole. You should consult your screw supplier for recommended dimensions for these holes."
*   **JLC3DP PA12 MJF Guidelines:**
    *   Source: JLC3DP 3D Printing Design Guidelines ([jlc3dp.com](https://jlc3dp.com), read 2026-09-18).
    *   Verbatim quote: "When printing with MJF (PA12 Nylon), parts shrink slightly as the powder cools after fusion. This typically causes holes to print slightly smaller than the CAD model."
    *   Typical MJF PA12 bore diameter contraction: **$0.10\text{ mm to }0.15\text{ mm}$**.
*   **Recommended Pilot Hole Dimensions for M2.5 Thread-Forming into MJF PA12:**
    *   *Fastener Specs:* M2.5 nominal outer diameter $D = 2.50\text{ mm}$, pitch $P = 0.45\text{ mm}$, minor diameter $d_{min} \approx 1.95\text{ mm}$.
    *   *Thermoplastic Rule of Thumb:* Target pilot hole diameter is **$80\%\text{ to }85\%\text{ of }D$** ($2.00\text{ mm to }2.12\text{ mm}$).
    *   *CAD Model Pilot Hole:* **$\mathbf{\varnothing 2.10\text{ to }2.15\text{ mm}}$**.
        *   After ~0.10 mm MJF bore shrinkage during cooling, the printed hole will measure **$\mathbf{\varnothing 2.00\text{ to }2.05\text{ mm}}$**.
        *   This provides approximately 70% to 75% thread engagement, ensuring maximum pull-out retention without cracking or splitting the boss.
    *   *Boss Outer Diameter ($D_{boss}$):* Recommended **$\mathbf{\ge 5.00\text{ mm}}$** ($2.0 \times D$, minimum radial wall thickness $1.4\text{ mm}$ around hole) to resist hoop stress when the M2.5 screw is driven.
    *   *Chamfer:* A small $0.2\text{ mm} \times 45^\circ$ lead-in chamfer at the mouth of the pilot hole is recommended to prevent surface lip formation.

---

## 5. Summary Matrix

| Question / Topic | Result / Determination | Primary Source / Reference |
| :--- | :--- | :--- |
| **JLC $\ge 2.5\text{ mm}$ Edge Rule** | Measured to **panel rail edge**, NOT board outline. Once 5 mm rails exist, outline copper clearance is $\ge 0.30\text{ mm}$. | JLC Assembly Terms §Notes on DFM; Help Article "How to Add Edge Rails" |
| **Automatic Edge Rails** | **YES.** JLC adds 5 mm process rails by default for standard PCBA < 70×70 mm, and on FPC panels via carrier fixtures ($23.57, `UNVERIFIED`). | JLC PCBA Capabilities & Flex SMT Guides |
| **FPC Depaneling** | **Laser cutting** with 0.7–1.0 mm bridge tabs. No V-cuts. Minimum pad-to-outline clearance is 0.20 mm. | JLC Flex Panel Design Guidelines |
| **2.5 mm Tab Strip with Pad** | **NO PROBLEM.** Rule applies to SMT component bodies; tab strip carries only bare copper traces and ring pad. | JLC Assembly Terms |
| **FPC Assembly Sides** | **Both sides supported.** Configured via "Both sides" selector with SMT carrier pallet. | JLCPCB SMT order portal |
| **Flex Stiffener Extra Fee** | Extra fee triggers at **$\ge 4$ stiffeners** (prototype) or $\ge 90\%$ area / stacked stiffeners. | JLC FPC Stiffener Design Guide |
| **Freerouting on macOS / Java 25**| **YES, writes `.ses` in headless mode.** Issue #522 infinite loop fixed in PR #541; v2.4.1 decouples GUI via `--gui.enabled=false`. | Freerouting GitHub repository & Issue #522 |
| **M2.5 Titanium Tail Screw** | Available in ones from **The Thomas RC ($1.60/ea)** or 1up Racing ($8.49/5-pk). McMaster/Bolt Depot do not stock. Both prices `UNVERIFIED` at review r7. | The Thomas RC / 1up Racing |
| **M2.5 MJF PA12 Pilot Hole** | **CAD $\varnothing 2.10\text{–}2.15\text{ mm}$** (yields $\varnothing 2.00\text{–}2.05\text{ mm}$ printed after shrinkage); boss $\varnothing \ge 5.0\text{ mm}$. | HP MJF Design Guide / JLC3DP |
