# WP4 — Rolf's sheets: measure, order 1, order log, hook test (lane w4)

Read `tasks/phase1-common.md` first. Lane `w4`, worktree
`/home/user/projects/elicio/.worktrees/w4`, branch `lane/w4`.
Start line (coordinator restarts you by copy-paste):

    herdr agent start w4 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Spec sections: plan §3.3 (the M1 chord gate and which parameters map to
measurements), §3.4 (caliper protocol), §3.6 (print rules, files), §3.7
(passive fit acceptance, including the hook test), §7 (orders, the
checkout gate), §8 (claims to verify before ordering), §9 row WP4, §10
"Open for Rolf" items 1 to 5 and 7. `docs/fab/L2-vendors.md` for the JLC
pages.

Owns: `docs/fab/measure.md`, `docs/fab/order1.md`, `docs/fab/orders.md`
(all new).

Rolf reads these on his phone, alone, with a caliper and a tape. Every step
is one instruction with one number to write down. No step needs a
question.

1. `measure.md`: M1 first, with the computed chord gate stated as the
   plan states it (the script's check, about 51 mm at the default bow; give
   the formula and a two-line table for bow 1, 3 and 8 so he can read the
   gate without the script), and the stop rule if M1 is below it. Then M2
   to M8 in the §3.4 order, each with the tool, the landmark, a picture
   description in words, the typical range, and the box to write in. A
   "defaults" line: if he measures nothing but M1, what gets built. Which
   ear (default right).
2. `order1.md`: the checkout gate as a checklist. Which files from
   `docs/fab/cad/v1/` (name them as §3.6 does), which JLC service and
   options (process, material, colour, finish, DDP shipping), what the
   quote page must show before he pays (the plan's allowances per line
   from §7, and the rule for a price outside them), what to record, and
   the "do not order if" list (renders not approved, a §3.3 check failed,
   M1 below the gate). No purchase is made by any agent.
3. `orders.md`: the order log template. One row per order: date, vendor,
   files and hashes from the manifest, quantities, quoted and charged
   price by line, duty and shipping actually paid, lead time, tracking,
   receipt inspection results. Fill nothing in.
4. The hook test, in `measure.md` or `order1.md` as §3.7 places it: 100 g
   at the tail tip, what to measure, the pass band (0.5 to 1.5 N), and
   what to do outside it.

Every number you write comes from the plan or from a page you cite with
its date. Where the plan marks a number UNVERIFIED, the sheet says so and
tells Rolf to read the live value at checkout.

Acceptance (plan §9 row WP4): no step needs a question. Gate: unit tests
green (you touch no code, but run them).

Report: `.reports/WP4-report.md`. Closing steps per the common file with
`<PKG>` = `WP4`, `<lane>` = `w4`.
