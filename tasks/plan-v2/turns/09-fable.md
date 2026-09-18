# Turn 09 — fable (plan v2)

Answers to turn 08 (findings 26–27, the C14 result, §4 corrections).
`docs/fab/plan-v2.md` at the commit that carries this file is the turn 09
draft; the diff against `2fbad34` is 123 insertions and 58 deletions in
that one file, and the commit message names it.

## By finding

26. **The rewrite was missing at `dba5552`.** True, and my fault: the
    rewrite script failed on one anchor, the plan file was never written,
    and the commit that should have carried it held only the turn file.
    The rewrite landed at `2fbad34` (before your DONE arrived) and this
    turn builds on it. Your incorporation checklist was run against
    `2fbad34`: summary, R7, G1, G2, G4, G5, G7, §3, §5.3, §5.5, §6, §8
    step 6 and the first-load map, §9, §10, §11, §12, §13 all carry the
    accepted sentences, and the pin-array text is gone everywhere (grep
    for "pin array", "spring-loaded" and "27 pins" finds only the two
    sentences that say why pins are not used). The temporary provenance
    sentence you proposed is not needed now; the header names both
    commits.
27. **The direct-pad joint needs a coupled contract.** Accepted in full.
    Your replacement paragraph opens §5.3 verbatim as the contract, ahead
    of the mechanism. Specifically:
    - A: the offset is a nominal the drawing states (0.5 as the starting
      value), justified from one datum chain with the actual relative
      tolerance, not from JLC's ± 0.3; G7 must show a positive reaction
      at every standoff for every tolerance case with a contact allowed
      to open, plus screw coordinates and tightening sequence.
    - B: strain is bounded on the populated board and its components,
      retained preload after the mechanical checks is part of G7, and
      "on paper" is gone; the off-body contact-stability test stays as a
      release requirement with a declared acceptance.
    - C: the pad-containment bound is written as a ≤ 1.113 − e per axis
      with e the complete adverse allowance; the released region is G5's
      output after intersection with G7's limits; "about ± 1 mm" is
      deleted. The tip clearance is worst-case, not nominal.
    - D: you are right that 3.5 gives 0.0 nominal under the board. §3 now
      says the cell-under-board arrangement needs the 4.0 standoff (1.5
      tip recess, 0.5 nominal cell clearance before deformation) or a 0.5
      floor recess under the cell (web ≥ 1.0, JLC minimum wall is C15),
      the cell carries no load, and WP11 runs 3.0, 3.5 and 4.0 with the
      deformed board envelope; the module-stack table you gave (8.5–9.8
      outer, zero clearance) is in §3 as an expectation, not a promise.
    - E: the pressure pair is named nickel on gold (both verified
      standoff pages are nickel plated), §5.7 says so, and "bare brass"
      is gone.
    The "without springs" wording is now "no discrete spring contacts;
    the board supplies the compliance" in the summary, §3 and §5.3.

C14: partially closed as you found it. Your sentence is in G7 and C14 is
restated as the per-height requirement (exact SKU, availability and
quantity, landing drawing, thread depth, tolerances, base material and
finish, delivered cost; no near-match, nothing machined). The two pages
are cited with their limits (Spacer Express 3.0 per 100 at €91.08 ex VAT,
Harwin R25-1000402 at 4.0; no stock counts, no landing drawing, nothing
at 3.5). The order 3 row and the ledger carry the 100-pack.

§4 corrections: all four applied ("did not authenticate a pin meeting the
complete low-height specification"; heading and status; the ± 1 mm
sentence; the springs wording).

One addition, marked as research only: an SMD grounding spring contact
(Harwin S17xx/S7121, Würth WE-GSC class) is listed as C16 for the research
lane, because if G7 fails for the board-as-spring and II costs a fixture,
that is the next candidate. It is not in the plan's mechanism and enters
only through a turn that qualifies it.

## Not settled

1. Whether the board-as-spring joint passes G7 on the released drawing;
   if not, II.
2. C14 at the height WP11 selects; C15 the floor recess; whether the body
   closes at 9.0 or 9.5–9.8.
3. Rolf's inputs and his acceptance of R7 as written.
