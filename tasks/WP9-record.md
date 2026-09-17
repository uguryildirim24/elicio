# WP9 — Design record update (lane w9)

Read `tasks/phase1-common.md` first. Lane `w9`, worktree
`/Users/rolfie/projects/elicio/.worktrees/w9`, branch `lane/w9`.
Start line (coordinator restarts you by copy-paste):

    herdr agent start w9 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Spec sections: plan §1 (decision summary), §2 (conflicts resolved, all
sixteen rows), §6 (skin, safety, hygiene), §9 (release states), §10; the
whole of `docs/EARPIECE_DESIGN.md`; `docs/fab/brief.md`; `AGENTS.md`
"Important Files" and "Key Directories".

Owns: `docs/EARPIECE_DESIGN.md`, `AGENTS.md` (the two lists named above
only), `README.md` status table only if a row is now wrong.

Deliver:

1. A new section in `docs/EARPIECE_DESIGN.md`, "Fabrication plan,
   2026-09-16", in the record's own voice and format: the decision (CAD in
   build123d, JLCPCB MJF PA12, three titanium M2.5 dome contacts, the
   provisional gauge first, the release states S0 to S4), each §2 decision
   of the plan stated once with its reason in one or two sentences, and a
   pointer to `docs/fab/plan.md` as the Phase 1 contract and to
   `tasks/plan/turns/` as the review record.
2. The "Fabrication without a 3D printer" section kept, with a short
   superseded note at its top saying which of its three routes survived
   (outsourced printing, now JLCPCB), which changed (stainless contacts
   became titanium; conductive TPU is available from Palmiga but not
   chosen for Stage B), and which was dropped (hand-shaped PCL).
3. "Open questions" 3 and 4 updated: 3 (Stage B microcontroller and ADC)
   now points at the L4 report and the interface; 4 (contact geometry) is
   answered by the plan's §3.3 and §4 with the montage test still ahead.
4. `AGENTS.md`: add `docs/fab/` and `docs/fab/plan.md` to the directory and
   important-files lists in the existing style; nothing else changes.
5. Requirements 1 to 7 and the Stage A material stay untouched. Do not
   remove history. The record uses "the owner" for Rolf in older text;
   in the new section write "Rolf".

Acceptance (plan §9 row WP9): each §2 decision appears once. Gate: unit
tests green (you touch no code, but run them).

Report: `.reports/WP9-report.md`. Closing steps per the common file with
`<PKG>` = `WP9`, `<lane>` = `w9`.
