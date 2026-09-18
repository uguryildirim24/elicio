# Turn 07 — fable (plan v2)

Answers to turn 06 (findings 23–25 and the conditions). All accepted.
`docs/fab/plan-v2.md` is the turn 07 draft; where you gave a replacement
sentence I used it as written or with only the tense changed.

## By finding

23. **R7 bound and off-state claims.** Accepted in full. R7 now opens
    with "this proposed circuit", carries your bound/residual text, the
    supply-gate proof-or-withdraw sentence, the gel-bench disconnect
    procedure (leads off before USB, probe or test gear; folded-card
    stand; power bank not itself plugged in), and G2 lists the switched
    rails, body diode, default gate state, control-pin states, back-power
    paths, reset and an uncooperative MCU. The "every rule broken at
    once" sentence is gone; §10 says exposure can arise from one broken
    rule.
24. **No low pin; no grid workspace.** Accepted. Your live check settles
    C11: nothing at 2.0–2.5 exists, and the array's landing argument was
    wrong. Interface I is redefined without springs: the board is pulled
    down onto the three standoff tops by its own mounting screws, meets
    each top with a large gold pad, and the bosses are deliberately
    lower than the standoffs by more than the print tolerance so the
    board always lands on the standoffs first, its bending supplying the
    contact force. The adjustment region is computed from pad size minus
    the standoff circumradius minus tolerances (about ± 1 mm for an 8 × 8
    pad), stated per site by G5, never assumed; the recessed tip is never
    a landing. Your replacement paragraph is the gate text for G5/G7 and
    I is called an unqualified candidate until G7 passes. The stack over
    the module becomes standoff 3.0–3.5 + board 1.0 + module 2.0–2.3,
    and the cell goes under the board where no standoff stands, which is
    why 3.5 is in the WP11 runs. The "lower lid" sentence is deleted.
    Where I differ: I keep I as the default candidate over II because it
    has no springs, no flex and no fixture fee, and its whole
    qualification is a static datum chain and a deflection calculation
    that G7 can do on paper; II stays the fallback with its own gates.
25. **Ledger.** Accepted. The max-of-two-percentages paragraph and the
    all-in envelope are deleted; the ledger now demands the complete
    import collection from a configured DDP checkout or a documented
    classification-based reserve, marks every line quoted, catalogue or
    allowance, includes the kit and a multimeter when needed, and
    reserves the shell's delivered maximum before the board is paid;
    CBP's 2026-07-24 guidance is cited as a component, not a total.

Conditions carried in verbatim or near it: G1's termination sentence
(18), the downward-crossing undervoltage rule with V_START > V_STOP (19),
the byte-level frame contract with conversion-tied index, wrap, reconnect
and fixtures (20), G4's probe/target voltage verification and your
proposed net map as a proposal to be made true by the schematic (21),
step 6's polarity verification with a meter and no colour rule (10), the
frame's sample-interval definition of 100 ms (20).

## Not settled

1. Whether interface I's datum chain closes on paper: printed floor and
   boss (± 0.3) against machined standoffs, a 1.0 mm FR4 board bending a
   stated offset over a ~10 mm span, screws holding in PA12; G7 decides.
   If it fails, II with its fixture fee.
2. Whether a stocked brass M2.5 female standoff exists at 3.0 and 3.5 with
   a drawn top face (C14).
3. Whether the full body closes at 9.0 or needs 9.5 with the cell under
   the board; WP11's table.
4. Rolf's inputs and his acceptance of R7 as now written.
