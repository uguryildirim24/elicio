# WP4 report

Lane `w4`, worktree `/home/user/projects/elicio/.worktrees/w4`, branch
`lane/w4`. Package WP4. Python 3.13.15 in `.venv`. No extra optional
dependency group. No code change.

Final commit: `fcd2b2a7fed769a29f57c9cd43bf29b833458f0a`

## What was built

Three phone sheets, all new:

- `docs/fab/measure.md` — M1 first, chord-gate formula and a two-line table
  for bow 1, 3 and 8, stop rule, then M2–M8 in plan §3.4 order (tool,
  landmark, picture in words, typical range, write-in box). Defaults line
  if only M1 is measured. Ear default right.
- `docs/fab/order1.md` — do-not-order list, five §3.6 STL names and
  quantities, JLC MJF / PA12-HP / natural grey / DDP, checkout gate with
  §7 allowances and the stop rule if a live price is outside them,
  UNVERIFIED lines to copy at checkout, 100 g hook test, then §3.7 wear
  and the thickness / preload / back-view boxes.
- `docs/fab/orders.md` — empty log template. No row filled.

Commits: `b808992`, `d5d8518`, `fcd2b2a`.

JLC pages read 2026-09-16 (no quote, no upload, no account):

- https://jlcpcb.com/3d-printing — process label MJF(Nylon)
- https://jlc3dp.com/help/article/pa12-hp-nylon — updated 2026-07-30;
  colour label Natural gray; price “from $1.00”
- https://jlcpcb.com/help/article/us-tariff-policy-faq — updated 2026-09-09;
  US individuals ship DDP. The extracted page did not show a 40 % plastics
  line.

## Plan §9 row WP4

Acceptance: no step needs a question. Gate: unit tests green.

| Item | Command | Result |
|---|---|---|
| Unit tests | `.venv/bin/python -m unittest discover -s tests -v` | `Ran 42 tests in 0.010s` / `OK` |
| M1-first sheet, checkout gate, empty order log, 100 g hook test | files exist on `lane/w4` | written; not a human trial |
| No step needs a question | review of the three sheets | each step is an instruction with one write-in; not run with Rolf |

Nothing in this package was claimed verified that was not run. The sheets
were not walked with a caliper or a JLC cart.

## What was not done

- No purchase, no JLC account, no upload, no quote request.
- CAD files under `docs/fab/cad/v1/` were not created (WP2 / WP3).
- M1–M8 were not measured. The hook test was not run (no printed part).
- `docs/fab/plan.md` was not edited.
- I did not run `git push`. A post-commit hook pushed `lane/w4` to origin
  after each commit.

## Needs a decision

1. Plan §3.3 writes the script check as `TOTAL_CHORD > M1 − 3`. That fails
   the default ear (47.9 > 49 is false). Plan §1, §2 row 17, §10 item 1,
   and turn 07 state the gate as M1 at least TOTAL_CHORD + 3 (50.9 mm at
   bow 3, 51.3 mm at bow 1). The sheets implement that §10 reading. WP2
   should not code the `>` as written.
2. Brief WP4 says the 100 g hook test sits in §3.7. Plan §3.7 does not
   list it. Plan §9 row WP4 and §10 interface item 3 do. Plan wins. The
   test is in `order1.md` after receipt, on `body_full_p15`. Force at
   1.5 mm preload is `0.98 N × 1.5 mm / drop`. 100 g = 0.98 N is standard
   gravity, not a plan number. Pass 0.5 N to 1.5 N. Outside that band, WP6
   decides HOOK_DIA.
3. The 40 % import collection stays UNVERIFIED. The tariff FAQ read
   2026-09-16 still does not give that plastics rate as a usable line.
   Rolf copies the live tariff line at checkout.
