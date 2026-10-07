# WP7a Work Package Report: Montage Bench Procedure & Frozen Test Protocol (Part 1)

**Package:** WP7a — Montage bench procedure and frozen dry-test protocol (Part 1)  
**Lane:** w5  
**Worktree:** `/home/user/projects/elicio/.worktrees/w5`  
**Branch:** `lane/w5`  
**Date:** 2026-09-17  
**Final Commit SHA:** `e0ea395c50756d5300dce85e38470f875622f4d6`

---

## 1. What Was Built

Created `docs/fab/montage.md` satisfying all requirements of `tasks/WP7a-protocol.md` and `tasks/phase1-common.md`:

1.  **Status Line:**
    *   Formally declared protocol frozen on 2026-09-17 before the acquisition of any dry-electrode data.
    *   Confirmed zero empirical bench or dry-contact experimental data exists in the repository.
    *   Gated Part 2 execution on Stage A hardware acquisition.
2.  **Montage Bench Procedure:**
    *   **Landmarks & Skin Marking:** Defined retroauricular crease arc $s$ from hook root ($s = 0$), ear root length $M_1$, crease arc length $M_2$, mid-concha level $M_7$ ($s = 22.0\text{ mm}$), and mastoid offset $M_6$ ($s = 43.0\text{ mm}$).
    *   **Contact Skin Coordinates:** Derived Contact 1 $(u=5.9,\, s=22.0)$, Contact 2 $(u=10.4,\, s=33.1)$, and Reference $(u=8.5,\, s=43.0)$ with verified center-to-center pitch of 12.0 mm at 22° inclination.
    *   **Montage Comparison:** Compared the Plan's 22° angled pair (fits within 17 mm BTE shell cavity span) against L3's strictly horizontal PAM pair (requires $u \ge 21\text{ mm}$, exceeding shell width). Prescribed bench acceptance rule ($\ge 70\%$ amplitude of horizontal ceiling).
    *   **Stage A Bench Hardware Settings:** Specified analog front-end chain (INA128 $G=10$, passive RC HPF $f_c = 19.4\text{ Hz}$, TL072 non-inverting gain $G = 11\text{ to } 101$, Sallen-Key LPF $f_c = 490\text{ Hz}$, ADS1115 16-bit ADC at 860 SPS, ESP32 streaming ASCII integer counts over USB UART at 115200 baud).
    *   **Per-Trial Recording:** Mandated pre/post impedance check, permanent JSON session capture via `.venv/bin/elicio capture`, and amplitude logging across rest, deliberate flexes, clenches, and dynamic disturbances.
    *   **Coordinate Derivation for S1 Entry:** Documented nominal coordinate freeze for CAD release and tolerance window ($s_1 \in [20.0,\, 24.0\text{ mm}]$).
3.  **Frozen Dry-Test Protocol and Criteria (All Quantitative & Numeric):**
    *   Baseline resting noise floor $\le 5.0\text{ }\mu\text{V RMS}$ (Quoted: L3 §3.1).
    *   Voluntary auricular flex amplitude $\ge 45.0\text{ }\mu\text{V pk-pk}$ (Quoted: L3 §1 r2).
    *   Voluntary auricular flex SNR $\ge 3.0:1$ (9.54 dB) (Quoted: DESIGN r60).
    *   Voluntary teeth clench amplitude $\ge 150.0\text{ }\mu\text{V pk-pk}$ (Quoted: L3 §2.3).
    *   Voluntary teeth clench SNR $\ge 10.0:1$ (20.0 dB) (Quoted: L3 §2.3).
    *   Clench-to-flex amplitude ratio $\ge 3.0:1$ (Quoted: DESIGN §2 r9).
    *   Zero dropouts under jaw motion across 10 cycles (Quoted: DESIGN Stage B exit criteria); maximum input DC shift $\le \pm 50.0\text{ mV}$ (`PROPOSED`).
    *   Three-day re-donning stability: $\ge 9/10$ deliberate contractions detected on each of 3 separate days at fixed threshold (Quoted: DESIGN Stage B exit criteria, HANDOFF M1).
    *   False-positive rate for eating: $\le 0.20\text{ events/min}$ (`PROPOSED`).
    *   False-positive rate for talking: $0.0\text{ events/min}$ (Quoted: DESIGN FP budget).
    *   False-positive rate for walking: $0.0\text{ events/min}$ (Quoted: DESIGN FP budget).
    *   Cross-talk rejection for yawning: 0 unconfirmed actions executed (Quoted: DESIGN FP budget, `policy.py`).
    *   Cross-talk rejection for facial mimicry: $\le 1/5$ reps for NONE, 0 for REVERSIBLE/DANGEROUS (Quoted: L3 §2.3, DESIGN FP budget).
4.  **Operational Safety and Session Rules:**
    *   Wear duration limits per release state: S0 passive progression, S1 order gate (zero wear), S2 bench electrical/chemical screen (zero skin wear), S3 validation wear $\le 4.0\text{ h/day}$, S4 routine use.
    *   Skin inspection pre/post wear and stop rule: halt immediately on pain, numbness, or erythema persisting $> 15.0\text{ min}$ (Quoted: plan §3.7 item 3).
    *   Hygiene: 70% isopropanol wipe after every wear session; solvent prohibition (Quoted: plan §6).
    *   Electrical safety interlocks: isolated DC battery power only, never charge while worn, host laptop on battery during serial debug, lead series protection $220\text{ k}\Omega$ (Quoted: plan §6).
5.  **Results Section:**
    *   Headings only (5.1 to 5.10); binding rule stating empirical data waits for Part 2 and criterion relaxation voids S1 gate.
6.  **Inputs to Other Packages:**
    *   To WP7b: test protocol for validation wear.
    *   To WP8: confirmed contact body-frame coordinates.
    *   To WP6: board packing and lead pad alignment confirmation.

---

## 2. Acceptance Verification (Plan §9 Row WP7a and Common Gates)

### Gate 1: Test Suite
*   **Command:** `.venv/bin/python -m unittest discover -s tests -v`
*   **Result:** Ran 67 tests in 0.027s. Result: **OK (skipped=4)**. 0 failures.

### Gate 2: Clean Git Working Tree
*   **Command:** `git status --short`
*   **Result:** Clean. Untracked file `.reports/WP7a-report.md` is gitignored.

### Gate 3: Protocol Frozen Before Dry Data
*   **Verification:** Section 1 explicitly declares criteria frozen on 2026-09-17 before dry data. Zero empirical data exists in the repository. Section 5 contains headings only and mandates that changing criteria after seeing data voids S1 entry.
*   **Result:** **PASS**.

### Gate 4: Numeric Criteria Completeness & Traceability
*   **Verification:** Every single test parameter in Section 3 has an explicit numeric threshold. Every threshold cites a quoted passage from existing documentation (`docs/fab/L3-contacts.md`, `docs/EARPIECE_DESIGN.md`, `docs/CLAUDE_SCIENCE_HANDOFF.md`, or `src/elicio/harness/policy.py`) or is tagged `PROPOSED:` with engineering rationale and what source would settle it.
*   **Result:** **PASS**.

---

## 3. What Was Not Done

1.  **Stage A Hardware Acquisition & Bench Measurement:** Per the WP7a brief, bench measurements constitute Part 2 and are blocked on hardware procurement by Rolf (`docs/STAGE_A_PARTS.md`). Part 1 delivers the frozen protocol and procedure.
2.  **No Hardware Purchasing or Quotes:** Per `tasks/phase1-common.md`, no purchase orders were placed, carts filled, or vendors contacted.
3.  **No Modification of Baseline Specifications:** `docs/fab/plan.md` and `docs/EARPIECE_DESIGN.md` remain untouched per task instructions.

---

## 4. Needs a Decision

1.  **Confirmation of Proposed Bounds:**
    *   `PROPOSED:` Maximum input DC shift during jaw motion bounded at $\le \pm 50.0\text{ mV}$. (Keeps INA128 input within linear common-mode operating range at $G=10$ on $\pm 9\text{ V}$ rails).
    *   `PROPOSED:` Eating false-positive rate bounded at $\le 0.20\text{ events/min}$ (allows at most 3 benign `RiskLevel.NONE` marker triggers during a 15-minute meal).
2.  **Part 2 Trigger:**
    *   Part 2 bench testing will run when Rolf acquires the Stage A parts cataloged in `docs/STAGE_A_PARTS.md`.

---

## 5. Final Commit SHA

*   `e0ea395c50756d5300dce85e38470f875622f4d6`
