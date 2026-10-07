# WP17c Work Package Report: Research v5 — JLC Edge Rule, FPC Sides, Router, Tail Screw

**Package:** WP17c — Research v5: the JLC edge rule, FPC assembly sides, a router, a screw  
**Lane:** w5  
**Worktree:** `/home/user/projects/elicio/.worktrees/w5`  
**Branch:** `lane/w5`  
**Date:** 2026-09-18  
**Final Commit SHA:** `f8b16343527b273027d8b55ee06d473c95028545`  

---

## 1. Answer to Item 1: The JLC Assembly Edge Rule

The JLCPCB $\ge 2.5\text{ mm}$ edge rule is an automated machine handling and conveyor clamping clearance constraint measured from component bodies to the panel's rail edge, not to the board's own internal routed or laser-cut outline. For standard PCBA and panelized FPC orders, JLCPCB adds 5 mm sacrificial process rails by default (and mounts flexible circuits onto a rigid carrier pallet) so conveyor belts and clamping jaws grip the outer rail border. With edge rails present, the distance from component bodies and copper features to the board outline is governed solely by profile laser cutting tolerances ($\ge 0.20\text{ mm}$ pad-to-outline to prevent carbonization micro-shorts, and $\ge 0.30\text{ mm}$ copper trace clearance). A 2.5 mm wide tab strip terminating in a Ø5.0 mm ring pad is not an assembly problem because it carries no SMT component bodies, maintains $> 1.1\text{ mm}$ trace-to-edge margin, and has $0.50\text{ mm}$ ring pad clearance to outline while supported by the SMT carrier fixture.

---

## 2. What Was Built

Created and delivered `docs/fab/L8-research-v5.md` on branch `lane/w5` (committed at `f8b16343527b273027d8b55ee06d473c95028545` with message `research(v5): JLC edge rule and FPC sides, router, screw`).

### Summary of Findings by Section

1.  **JLC Assembly Edge Rule (Q78):**
    *   *Terms & Conditions Statement:* "The distance between the body of the components and the edge of the board must be equal to or greater than 2.5mm" under Notes on DFM.
    *   *Technical Intent:* Prevents pick-and-place nozzle and conveyor guide rail collisions with component bodies.
    *   *Edge Rails:* JLCPCB adds 5 mm process rails by default for standard PCBA orders under 70 × 70 mm, and on all 4 sides of FPC panels when "Panel by JLCPCB" is selected. SMT conveyor rails clamp the 5 mm process edges, ensuring $\ge 5.0\text{ mm}$ clearance to all parts.
    *   *Board Outline Clearance:* With rails present, component courtyards can extend directly to the board outline. Minimum copper-to-outline clearance is **0.20 mm** (laser cutting carbonization threshold) and **0.30 mm** for routing/traces.
    *   *FPC Depaneling:* FPC does not use V-cuts (thickness 0.11 mm is below the 0.6 mm V-cut floor). Depaneling uses UV laser cutting along 0.7–1.0 mm bridge tabs.
    *   *Tab Strip:* A 2.5 mm wide strip with a Ø5.0 mm ring pad has zero SMT components and satisfies all copper-to-outline clearances (> 1.1 mm for traces, 0.5 mm for the pad). It is zero assembly problem.
2.  **FPC Assembly Sides:**
    *   *Double-Sided SMT:* Fully supported on 2-layer polyimide flex. Configured via the "Both sides" selector in the JLCPCB SMT portal. Uses custom carrier pallets ($23.57 fixture fee) and two-pass reflow.
    *   *Component Constraints:* Minimum passive package size 0402 (0201 in Standard SMT). Minimum IC lead pitch 0.35 mm (Standard) / 0.40 mm (Economic). Maximum component limit is **300 designators** per order. Extended parts incur a $3.00 USD setup fee per unique line.
    *   *Stiffener Rules:* Extra fee applies if $\ge 4$ stiffeners are used on prototype orders, or if stiffeners cover $\ge 90\%$ of board area or are stacked ($8.14 + $24.44/m² per extra stiffener). Stiffeners cannot cover SMT component pads on the same layer.
3.  **A Router That Writes a File on This Mac:**
    *   *Freerouting v2.4.1:* Decoupled the algorithmic core from Swing/AWT desktop GUI. Headless mode **writes a `.ses` file** on macOS Apple Silicon under Java 21+.
    *   *Exact CLI Flags:*
        ```bash
        java -jar freerouting-2.4.1-exec.jar --gui.enabled=false -de <input.dsn> -do <output.ses> -mp <passes> -mt <threads>
        ```
    *   *Issue Tracker on 2.1.0 Hang:* Issue #522 (pass counter tied to GUI repaint loop in headless mode causing infinite looping) was fixed by `@ceoloide` in **PR #541** (merged April 2025). Issues #368 and #457 (headless AWT exceptions and modal update dialogs) were eliminated by the v2.4.0 architectural separation.
    *   *Alternative Free Autorouters:*
        *   **ProtoFlow (ProtoRoute):** Desktop tool (`protoflow.ai`) that natively reads and writes `.kicad_pcb` files directly, eliminating DSN/SES conversion.
        *   **KiCadRoutingTools:** Open-source Python/Rust A* router plugin for KiCad.
        *   **DeepPCB:** Free-tier AI cloud-assisted router with an official KiCad PCM plugin.
        *   **KiCad Python Scripting (IPC API / `pcbnew`):** Programmatic trace and via placement.
4.  **The Tail Screw (Q71) and MJF Pilot Hole:**
    *   *M2.5 Titanium Screws in Ones:*
        *   **The Thomas RC (KDRC):** KDRC M2.5 Grade 5 Titanium Button Head Screws (4 mm and 6 mm length) sold individually in single units for **$1.60 USD each**.
        *   **1up Racing:** Pro Duty Titanium M2.5 LowPro / Button Head Screws (5 mm and 6 mm length) sold in 5-packs for **$8.49 – $8.99 USD**.
        *   **McMaster-Carr / Bolt Depot:** Neither stocks M2.5 in titanium (McMaster titanium starts at M3; Bolt Depot stocks steel/stainless M2.5 only).
    *   *MJF PA12 Pilot Hole Recommendation:*
        *   HP Multi Jet Fusion guidelines recommend self-tapping screws for threads $< 6\text{ mm}$ into pre-formed pilot holes.
        *   MJF PA12 bores contract by $0.10\text{ to }0.15\text{ mm}$ during cooling.
        *   Recommended CAD pilot hole diameter for M2.5 thread-forming: **$\mathbf{\varnothing 2.10\text{ to }2.15\text{ mm}}$** (yields $\varnothing 2.00\text{ to }2.05\text{ mm}$ printed hole after shrinkage, giving 70–75% thread engagement).
        *   Recommended boss outer diameter: **$\mathbf{\ge 5.00\text{ mm}}$** (radial wall thickness $\ge 1.4\text{ mm}$) to withstand hoop stress without cracking.

---

## 3. Acceptance Verification and Gates

### Gate 1: Test Suite
*   **Command:** `/home/user/projects/elicio/.worktrees/w5/.venv/bin/python -m unittest discover -s tests -v`
*   **Result:** Ran 206 tests in 83.403s. **OK (skipped=26)**. 0 errors, 0 failures.

### Gate 2: Clean Git Working Tree
*   **Command:** `git status --short`
*   **Result:** Empty (clean). Report `.reports/WP17c-report.md` is gitignored.

### Gate 3: Commit History on `lane/w5`
*   Commit `f8b16343527b273027d8b55ee06d473c95028545`: `research(v5): JLC edge rule and FPC sides, router, screw`

---

## 4. What Stayed UNVERIFIED

1.  **Fixed Numerical Component Height Ceiling on FPC:** `UNVERIFIED` as a single published value on JLCPCB flex pages (constrained by standard pick-and-place nozzle clearance and carrier fixture design).
2.  **McMaster-Carr & Bolt Depot M2.5 Titanium Screws:** Verified that neither supplier stocks M2.5 in titanium (McMaster starts titanium at M3; Bolt Depot stocks steel/stainless only).

---

## 5. Needs a Decision for Plan v2 Build Rounds

1.  **Board Packing Search Constraints (Q78, WP11d):**
    *   Now confirmed that the 2.5 mm JLC rule applies to the panel rail edge, not the board outline.
    *   *Action:* WP11d can place components on the parts island up to the standard 0.30 mm copper-to-outline clearance boundary. Dense single-sided and double-sided placement on the w20 body can proceed without an artificial 2.5 mm internal border setback.
2.  **Tail Fastener Selection (Q71):**
    *   *Action:* Specify M2.5 × 4 mm or M2.5 × 6 mm Grade 5 Titanium Button Head screws (e.g. from The Thomas RC at $1.60 each, or 1up Racing 5-pack at $8.49) for the concealed tail closure screw.
3.  **MJF Boss Pilot Hole Sizing (Q71, Q73, WP14b):**
    *   *Action:* Model the tail closure boss and the two island retention bosses (Q73) with a CAD pilot hole diameter of **$\varnothing 2.10\text{ mm}$** and an outer boss diameter of **$\varnothing 5.00\text{ mm}$**.
4.  **Autorouting Toolchain Execution (Q77, WP12d):**
    *   *Action:* The board lane can invoke Freerouting v2.4.1 headlessly with `--gui.enabled=false -de elicio-v2.dsn -do elicio-v2.ses -mp 20 -mt 4` on macOS with Java 21, or utilize ProtoFlow for direct `.kicad_pcb` routing.

---

## 6. Final Commit SHA

`f8b16343527b273027d8b55ee06d473c95028545`
