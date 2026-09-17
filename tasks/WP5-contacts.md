# WP5 — Contacts kit: verified sourcing and assembly (lane w5)

Read `tasks/phase1-common.md` first. Lane `w5`, worktree
`/Users/rolfie/projects/elicio/.worktrees/w5`, branch `lane/w5`.
Start line (coordinator restarts you by copy-paste):

    herdr agent start w5 --kind agy --pane <pane> --parent w1B:p1 -- --dangerously-skip-permissions --add-dir /Users/rolfie/projects/elicio --effort high --model gemini-3.8-flash-high

You are an Antigravity lane because this package is web verification.
Read public product pages only. Do not sign up, request a quote, add to a
cart, or contact anyone.

Spec sections: plan §2 rows 3 and 4 (titanium, M2.5 ISO 7380), §3.3
CONTACT_* and KEEPOUT_* rows, §4 (contacts specification), §6 (safety),
§7 order 2 hardware lines, §8 claims, §9 row WP5, §10 "Open for Rolf" item
9. Evidence: `docs/fab/L3-contacts.md` §5 and §7.3; `tasks/plan/turns/02-pro.md`
finding 11 (the wrong SKU) and finding 8 (the nickel argument).

Owns: `docs/fab/contacts.md` (new).

Deliver `docs/fab/contacts.md`:

1. Verified SKUs, each with the product page URL, the date read, the price
   and pack size, and the catalog drawing's dimensions: ISO 7380 M2.5
   button-head screws in Grade 2 or Grade 5 titanium (McMaster-Carr, Bolt
   Depot, Titanium fasteners specialists, Amazon only if nothing else),
   thin nuts (ISO 4035 or DIN 439) in titanium, ring lugs sized for M2.5 in
   a nickel-free finish or bare copper, Kapton tape, and the nickel spot
   test kit. Where titanium M2.5 hardware is not stocked, say so and give
   the nearest real option with what it changes.
2. The stack arithmetic on catalog drawings: lug, nut, screw tip above the
   nut, Kapton; must total at most 2.63 mm above the floor (plan §3.3
   CONTACT_STACK; §9 row WP5). Show the numbers per SKU set.
3. The material-evidence route: what document proves the alloy (mill test
   certificate to EN 10204 3.1, ASTM F67 or F136 statement, supplier
   material declaration), which of the listed suppliers provide it, and
   the fallback if none does. State plainly that 316 stainless is not
   nickel-free and is not a fallback.
4. The DMG spot-test protocol for received parts, with a named kit and its
   page, and what a positive result means (reject the lot).
5. The assembly sheet: order of assembly for one contact (screw through the
   medial wall from outside, Kapton, lug, nut, torque by feel or a number
   with its source), the reference contact in its pocket with the upright
   lug tab, and the insulated wire route into the cavity.
6. The internal-metal list: every metal part inside the shell, its alloy or
   plating, and whether it can touch skin in any failure.

Mark anything you could not verify UNVERIFIED with what would verify it.
Every price has a page and a date, or is not written.

Acceptance (plan §9 row WP5): every price has a page and date; the stack is
at most 2.63 mm on catalog drawings. Gate: unit tests green (you touch no
code, but run them once: `python3.13 -m venv .venv && .venv/bin/python -m pip install -e . && .venv/bin/python -m unittest discover -s tests`).

Report: `.reports/WP5-report.md`. Closing steps per the common file with
`<PKG>` = `WP5`, `<lane>` = `w5`. Commit `docs/fab/contacts.md` on
`lane/w5` before the DONE line and put the commit sha in it.
