# WP7a (part 1) — Montage procedure and frozen dry-test protocol (lane w5)

Read `tasks/phase1-common.md` first. Lane `w5`, worktree
`/Users/rolfie/projects/elicio/.worktrees/w5`, branch `lane/w5`, now
fast-forwarded to `main` (round 1 merged at `121ccb3`, open questions at `9838573`; read `docs/fab/open-questions.md` after the plan). Start line (coordinator restarts
you by copy-paste):

    herdr agent start w5 --kind agy --pane <pane> --parent w1B:p1 -- --dangerously-skip-permissions --add-dir /Users/rolfie/projects/elicio --effort high --model gemini-3.8-flash-high

Stage A parts are not bought, so WP7a's bench measurement cannot run.
Plan §9 row 7a also requires "criteria frozen before any dry data". This
package writes the frozen protocol and the montage procedure now; the
measurement itself is part 2, blocked on Rolf's purchase.

Spec sections: plan §4 (positions, leads, cleaning), §3.3 (CONTACT_1,
CONTACT_2, CONTACT_PITCH, PAIR_ANGLE, CONTACT_REF, M6), §3.7 item 9 (dome
positions marked on skin, photographed), §6, §9 rows 7a and 7b and release
states S1–S4, §10 interface decision 4. `docs/EARPIECE_DESIGN.md`
("Staged build plan", "Harness mapping and false-positive budget",
"Requirements"), `docs/CLAUDE_SCIENCE_HANDOFF.md` ("Established research
results", "Safety and authority"), `docs/RESEARCH_PROVENANCE.md`,
`docs/fab/L3-contacts.md` (montage, PAM pair, SNR band, mastoid
reference), `docs/STAGE_A_PARTS.md` (what the bench is).

Owns: `docs/fab/montage.md` (new).

Deliver, in this order inside the file:

1. **Status line**: no data exists; criteria frozen on the date of your
   commit before any dry data; part 2 runs when Stage A parts exist.
2. **Montage bench procedure**: how to mark the plan's positions on the
   skin from the landmarks §3.3 and §3.4 define (M6 and the crease), the
   gel-electrode montage at those positions versus L3's pair, the
   reference on the mastoid at CONTACT_REF, the Stage A bench settings
   from the design record, what is recorded per trial, and how the three
   coordinates come out (the `(u, s)` pair for CONTACT_1 and CONTACT_2
   and the reference site), which is what S1 needs.
3. **Frozen dry-test protocol** with a numeric pass criterion per item:
   baseline (resting noise in the band the design record names), SNR of a
   clench against rest, dropout under jaw motion, three-day re-donning
   with the detector threshold unchanged, and false-positive rates during
   eating, talking and walking, plus the cross-talk cases the design
   record lists (yawning, wide smiles). Each number comes from a named
   source (the design record's criteria and false-positive budget, the
   research results in the handoff, L3's bands) with the section quoted.
   Where no source gives a number, write PROPOSED with a one-line
   rationale and the source that would settle it; do not invent
   physiology.
4. **Session rules** from plan §6 and §9: wear limits per state (S3 ≤ 4
   h/day, only the sessions this protocol prescribes), skin inspection,
   stop rules, cleaning, battery-only, never charged while worn.
5. **Results section**: headings only, one per criterion, with the rule
   that nothing is written there before part 2 and that a change to any
   criterion after data exists voids the S1 entry.
6. **Inputs to other packages**: what WP7b measures, what WP8 takes
   (coordinates), what WP6 takes (nothing unless the pads move).

Do not buy anything, do not contact anyone, do not write results, do not
edit `plan.md` or the design record. Web only for a standard or paper
you cite, with URL and date.

Acceptance (plan §9 row 7a, the part that can be met now): criteria
frozen before any dry data, every criterion numeric with a source or
marked PROPOSED. Gates: unit tests unchanged and green; no number without
a source or PROPOSED tag (grep your own file).

Report: `.reports/WP7a-report.md`. Closing steps per the common file with
`<PKG>` = `WP7a`, `<lane>` = `w5`.
