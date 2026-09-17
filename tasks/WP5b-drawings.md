# WP5 part 2 — lug, nut and dome drawings for Q13, Q6 and Q7 (lane w5)

Read `tasks/phase1-common.md` first, then `docs/fab/open-questions.md`
(Q6, Q7, Q13). Lane `w5`, worktree
`/home/user/projects/elicio/.worktrees/w5`, branch `lane/w5`,
fast-forwarded to `main` (round 2 merged at `443a178`). Start line
(coordinator restarts you by copy-paste):

    herdr agent start w5 --kind agy --pane <pane> --parent w1B:p1 -- --dangerously-skip-permissions --add-dir /home/user/projects/elicio --effort high --model gemini-3.8-flash-high

Spec sections: plan §4 (contacts, inside stack, nut and lug materials),
§6, §9 row WP5 and state S1. `docs/fab/contacts.md` as merged (the round 1
reviewer's changes are in `tasks/reviews/code-r1.md` defects 19 to 25).
`docs/fab/interface.md` §2.2, §2.3, §3.1 (tab envelope, pad distances:
SIG1 pad about 4.6 mm and SIG2 about 5.8 mm from their contact centres).

Owns: `docs/fab/contacts.md` (a new dated section "Drawings for the open
questions, 2026-09-17", and updates to the SKU tables it supersedes).

This is a research package: read live pages, quote drawings, cite URL and
date per number. No purchase, cart, quote, sign-up, upload or vendor
contact. If a page needs a login, write UNVERIFIED and what page it was.

Deliver:

1. **Ring lug drawing (Q13).** For TE 31428: thickness, ring outer
   diameter, hole, overall length from the ring centre to the barrel end,
   barrel width, wire range, from the TE drawing, with URL and date. Then
   two alternatives (#4 or M2.5 ring, 22 to 28 AWG barrel, thickness
   ≤ 0.5 mm) whose length from the ring edge to the barrel end is at most
   the pad distance (4.6 mm SIG1, 5.8 mm SIG2), or the shortest available
   if none is. State plainly which lug lets the tab end under its own pad
   and which does not. If none does, say so; WP6 needs the number, not a
   hope.
2. **Nut candidates (Q6), no decision.** For DIN 439 / ISO 4035 M2.5 thin
   nuts in brass, tinned brass, titanium and plated steel, and for DIN 934
   titanium as the zero-margin fallback: SKU, vendor page, date, price,
   material statement or certificate availability, height m, across flats
   s, across corners e, from a drawing. Each row says whether it is inside
   plan §4's text ("plated steel or tinned copper") and whether it is
   nickel-free. Do not recommend; Rolf picks.
3. **Dome drawing (Q7).** Titanium ISO 7380 M2.5 × 4 button-head SKUs
   (Grade 2 or 5) with a drawing showing dk (head diameter) and k (head
   height), the hex socket size, the material statement. Say for each
   whether dk and k equal the plan's 4.7 and 1.35 and, if not, by how
   much; interface §2.2 note D1 says what a difference does.
4. **Prices**: every price has URL and date or is UNVERIFIED; any line
   over $20 flagged per plan §9; total for the kit as it would be bought
   at the cheapest nickel-free row, marked estimate.

Do not edit `plan.md`, `open-questions.md`, `interface.md`, `montage.md`,
`packing-options.md`. Do not change the stack numbers in `contacts.md`
§2; if a drawing contradicts them, write it under "Needs a decision" with
the arithmetic.

Acceptance: Q13 gets a lug length from a drawing; Q6 gets a candidate
table with drawings; Q7 gets dome drawings. Gates: unit tests unchanged
and green; every number has URL and date or UNVERIFIED (grep your own
section).

Report: `.reports/WP5b-report.md`. Closing steps per the common file with
`<PKG>` = `WP5b`, `<lane>` = `w5`.
