# WP17b Work Package Report: Research v4 — Probe, Cell in Ones, Fees

**Package:** WP17b — Research v4: the probe, the cell in ones, the assembler's fees  
**Lane:** w5  
**Worktree:** `/home/user/projects/elicio/.worktrees/w5`  
**Branch:** `lane/w5`  
**Date:** 2026-09-17  
**Final Commit SHA:** `ba45071bc81810fc9290e0e4db4aa3a11a0395e3`  

---

## 1. What Was Built

Updated `docs/fab/L7-research-v4.md` across two turns:
- **Turn 1 (commit `ea3b9bd`):** Initial Research v4 covering first-load probe (Q64), cell in ones (Q55), JLCPCB fees (Q60/Q67/Q65), component facts (Q63/Q68/Q65), shell colour/finish (Q30), and Ebyte E73 drawing.
- **Turn 2 (commit `ba45071`):** Appended Section 7 covering exhaustive research into secondary lithium pouch cells fitting within the maximum envelope of $16.0\text{ mm (L)} \times 10.5\text{ mm (W)} \times 5.2\text{ mm (T)}$ with Protection Circuit Module (PCM), capacity $\ge 30\text{ mAh}$, with leads/connector, available in single units with displayed price and stock.

---

## 2. Turn 2 Dedicated Findings: Pouch Cells Under 16 mm (Q55 Follow-Up)

### 2.1 The 16 mm Envelope Problem and Distributor Reality
- **Authorized Component Distributors (DigiKey, Mouser):** Parametric filtering for secondary Li-ion/LiPo cells $\le 16.0\text{ mm}$ length with $\ge 30\text{ mAh}$ yields **0 results**. Shortest Jauch cell is `LP501218JH` ($20.0\text{ mm}$ long); shortest Renata cell is `ICP641620PA` ($21.5\text{ mm}$ long).
- **Hobbyist / Maker Distributors (Adafruit, SparkFun, TinyCircuits, Pimoroni, The Pi Hut, Seeed Studio, Kitronik):** Zero secondary pouch cells $\le 16.0\text{ mm}$ length exist.
  - TinyCircuits `ASR00035` is 500 mAh ($30.0 \times 20.0 \times 9.5\text{ mm}$); smallest cell `ASR00007` is 150 mAh ($19.5 \times 25.5 \times 4.5\text{ mm}$).
  - PowerStream PGEB series has only one micro-cell under 16 mm (`GM-NM300910`, $3.0 \times 9.0 \times 10.0\text{ mm}$), but its capacity is only 12 mAh (fails $\ge 30\text{ mAh}$). All other PGEB models are $\ge 25.0\text{ mm}$ long.
  - Adafruit smallest cell is Product 1570 (100 mAh, $12 \times 28 \times 5.5\text{ mm}$).
  - SparkFun smallest cell is `PRT-25270` / `DTP301120` (40 mAh, $3.2 \times 11.5 \times 22.0\text{ mm}$).
  - Pimoroni, The Pi Hut, Seeed Studio, and Kitronik stock only cells $\ge 25.0\text{ mm}$ long.

### 2.2 The 501015 Dimension and PCM Trap
- A generic **501015** pouch cell ($5.0 \times 10.0 \times 15.0\text{ mm}$) specifies only the **bare pouch** dimensions.
- Technical datasheets from manufacturers (DNK Power `DNK501015`, Benzo Energy `BZ 501015`) show that adding the end-mounted Protection Circuit Module (PCM) and tape increases the finished pack length to **17.0 mm** (DNK Power verbatim: "Dimensions: 17 × 10 × 5.0 mm").
- Therefore, any 501015 pack with PCM **exceeds the 16.0 mm length limit by 1.0 to 1.5 mm** and will collide with the antenna keep-out or SIG1 standoff in the packing layout.

### 2.3 The Identified Solution: Model 501012 (or 401012)
- **Model 501012 (Earphone / TWS Pouch Cell):**
  - **Dimensions with PCM:** **$5.1\text{ mm (T)} \times 10.1\text{ mm (W)} \times 13.0\text{ to }14.5\text{ mm (L)}$** (bare pouch is $5.0 \times 10.0 \times 12.0\text{ mm}$).
  - **Envelope fit:** Length $13.0\text{–}14.5\text{ mm} \le 16.0\text{ mm}$ (clears length constraint with 1.5–3.0 mm margin!); Width $10.1\text{ mm} \le 10.5\text{ mm}$; Thickness $5.1\text{ mm} \le 5.2\text{ mm}$.
  - **Capacity:** **40 mAh** (35–45 mAh), satisfying the $\ge 30\text{ mAh}$ floor.
  - **Leads:** Red/Black flying wire leads (typically 28–30 AWG, 30–50 mm length) attached to top PCM.
  - **Availability in Ones:** Readily available in stock on eBay (e.g. item `183480766633`) and AliExpress (e.g. item `1005006093774888`) for **$4.00 to $8.00 USD** with published prices and stock counts.
- **Model 401012:**
  - Bare dimensions $4.0 \times 10.0 \times 12.0\text{ mm}$; pack length with PCM is ~14.0 mm; capacity 30–35 mAh; passes all axes.

---

## 3. Acceptance Verification and Gates

### Gate 1: Test Suite
*   **Command:** `/home/user/projects/elicio/.worktrees/w5/.venv/bin/python -m unittest discover -s tests -v`
*   **Result:** Ran 169 tests in 79.260s. **OK (skipped=21)**. 0 errors, 0 failures.

### Gate 2: Clean Git Working Tree
*   **Command:** `git status --short`
*   **Result:** Empty (clean). Untracked report `.reports/WP17b-report.md` is gitignored.

### Gate 3: Commit History on `lane/w5`
*   Commit `ea3b9bd3d22ea879c86e026b6e2bb07cbe6943ea`: `research(v4): probe, cell in ones, fees`
*   Commit `ba45071bc81810fc9290e0e4db4aa3a11a0395e3`: `research(v4b): cells under 16 mm`

---

## 4. What Stayed UNVERIFIED

1.  **Distributor-Stocked LiPo Cells $\le 16.0\text{ mm}$ Length with $\ge 30\text{ mAh}$:** `UNVERIFIED` / None exist across DigiKey, Mouser, Adafruit, SparkFun, TinyCircuits, Pimoroni, The Pi Hut, Seeed Studio, or Kitronik.
2.  **JLC3DP / Xometry Static Price Deltas for Finish Options:** `UNVERIFIED` as static published catalog figures (both vendors utilize dynamic 3D model geometry quotation).
3.  **Ebyte E73 Direct DXF/CAD File:** `UNVERIFIED` on public direct links without vendor account portal access.

---

## 5. Needs a Decision for Plan v2 Build Rounds

1.  **Cell Selection for S0 Prototype and Packing (Gate G4):**
    *   The packing lane determined that 20 mm and 22 mm cells collide with the antenna zone or SIG1 standoff.
    *   Nominal 501015 cells with PCM are **17.0 mm long** and also fail the 16.0 mm body limit.
    *   *Decision:* Adopt **Model 501012** (40 mAh, $5.1 \times 10.1 \times 13.0\text{–}14.5\text{ mm}$ with PCM) for the mechanical packaging model and prototype procurement. Procure 2–5 units via eBay / AliExpress or request manufacturer engineering samples from DNK Power / Benzo Energy.
2.  **First-Load Programming Probe Selection:**
    *   Adopt a level-shifting probe with $V_{TRef}$ sensing for first load: ST-LINK V3 MINIE ($25.51 USD, DigiKey), Black Magic Probe V2.3 ($74.95 USD, 1BitSquared), or SEGGER J-Link EDU Mini ($75.95 USD, Adafruit).
3.  **Charger System Load Management (BQ25100):**
    *   Firmware must enter low-power sleep on the radio and MCU during USB attachment to prevent system load from exceeding $I_{TERM}$ and triggering the 10-hour safety timer fault.

---

## 6. Final Commit SHA

`ba45071bc81810fc9290e0e4db4aa3a11a0395e3`
