# HANDOFF — Elicio coordinator

Written 2026-09-18 09:20 (America/New_York) by the coordinator (`elicio`,
pane `w1B:p1`) right after merging round 7 (`facb0c1`, verdict
`tasks/reviews/code-r7.md`, decisions Q89–Q97) and opening round 8. Rolf
is asleep; the delegation below is in force.

## Goal

Rolf, 2026-09-16: "we design the airpiece in blender or something and i
get it custom made in china or something", then "for coding after spec is
clean use grok xhigh for the code on as many as lanes as possible, the
usual flow as you know then one opus high to review and commot" (Grok
through Cursor, not the Grok CLI). Done looks like: release state S0 of
`docs/fab/plan-v2.md` §10 (the shell files, the routed board release and
Rolf's sheets approved and ordered by Rolf under the three checkout gates
of §8), then S1 and S2 as the parts arrive. Spec: `docs/fab/plan-v2.md`,
signed off by GPT-6 Pro at `ef369bd` (plan v1 `docs/fab/plan.md`,
`0c5d0eb`, is superseded where v2 speaks). Readings after each review:
`docs/fab/open-questions.md` (Q1–Q97).

Rolf's answer sheet, 2026-09-17 (Q28–Q36): one order per thing ("I
literally don't have the financial means to order several versions"),
"look prettier", "we design it properly custom order it" (no breadboard),
thin, right ear, requirement 5 to titanium, tail pocket may grow, lid rib
out; "this will come put together right?" (Q35: yes, JLC assembles the
board; the shell and the eight steps are his) and "do we actually have to
get it from china?" (Q36: no, a US route exists at a price; his call).

## Authority

- Delegated by Rolf, 2026-09-16 night: "i sleep autonomous. i trust your
  decisions and agency don't wait for my input". So: finish rounds, merge,
  open the next round, record his decisions as open questions and keep
  building around them. Never: purchase, sign-up, quote request, upload,
  vendor contact, destructive git (Q56: the 109 MB of SVGs on `lane/w1`
  stay until Rolf deletes the branch himself).
- Waiting on Rolf, with my reading so he can just say yes (all in
  `docs/fab/open-questions.md`, "For Rolf"):
  1. Q38 body height: the arithmetic refuses "thin"; the smallest body
     that closes at width 20 is 9.0 outer (Q57 foam 0.5). Reading: 9.0.
     The first shell pictures are on the sheet (version 6) with the
     reviewer's findings: the size is right, the closure and the USB end
     fail as drawn and are being redone (WP14b).
  1a. Q81 with Q34: the USB-C receptacle needs M1 ≥ 58.3 (a body 7.3
     longer); until he measures, the build carries two charging contacts
     on the tail and a magnetic cable, and USB-C returns if M1 allows.
     Reading: contacts; his M1 decides. A plan v2 §5.4 amendment turn
     with Pro if he confirms. With Q78 the body is now 22 wide (the parts
     fit nowhere at 20, receptacle or not); Q38's approval covers it.
  1b. Q69 the battery route (sheet question 2b): the marketplace 501012
     pack (13.0 × 10.1 × 5.1 with PCM, 40 mAh, no drawing) or a factory
     sample of the real 17.0 mm 501015 pack with M1 ≥ 52.5 and a body 1.5
     longer. Reading: the record carries the 501012 pack in the w20 × y8
     pocket; nothing is bought.
  1c. Q89 the tail screw: the M2.5×4 never reaches the lid (the reviewer
     measured it); the lid gets a boss and the screw grows to M2.5×8 or
     ×10 as WP14f states. Reading: build it; he buys that length.
  1d. Q90 the charging pads: bare VBUS and GND on the skin face break
     the 220 kΩ per-path rule, so they move to the back edge of the body
     at the hook end as clamped button heads (WP11g decides which wall
     is the hidden one). His alternative: a cover plus a GND switch.
     Sheet question 6c is being rewritten (version 12).
  2. Q34 M1: measure it once (`docs/fab/measure.md`, v2 lands with WP15);
     52 is the default the CAD carries as provisional until then.
  3. Q30 colour and finish, Q33 the money ceiling, Q36 country (China DDP
     or a US shop): blank until he writes them; WP17b reads the colour
     pages, WP15 leaves his rows blank with his name on them.
  4. Q41 R7 acceptance (the ADS1292 noise test as the criterion of use),
     Q46/Q53 the tools lanes installed (KiCad, arduino-cli, Arm GNU, Rosetta
     2; he may veto any), Q47 objectives and residual risks as written in
     `docs/EARPIECE_DESIGN.md`, Q67 Raytac route (JLC global sourcing vs
     consignment) at G3, Q64 buys no probe until G4 names the kit.
  5. Requirement 5 in `docs/EARPIECE_DESIGN.md` says titanium since WP16;
     his edit if he wants otherwise.

## Settled

| round | package | verdict | on the integration branch at | verdict file |
|---|---|---|---|---|
| spec | `docs/fab/plan.md` (9 turns, fable vs GPT-6 Pro) | SIGNED OFF (turn 08) | `0c5d0eb` | `tasks/plan/turns/08-pro.md` |
| r1 | WP9, WP1, WP4, WP5, WP2 | MERGE-AFTER-DECISION (30 fixes) | `121ccb3` | `tasks/reviews/code-r1.md` |
| r1 | decisions Q1–Q12 | coordinator | `9838573` | `docs/fab/open-questions.md` |
| r2 | WP7a part 1 `docs/fab/montage.md` | MERGE-AFTER-DECISION (10 fixes) | `443a178` | `tasks/reviews/code-r2.md` |
| r2 | WP3 renders, drawing, manifest schema, vendored font | MERGE-AFTER-DECISION (9 fixes) | `443a178` | `tasks/reviews/code-r2.md` |
| r2 | WP6 interface v2, placement drawing; packing NOT confirmed | MERGE-AFTER-DECISION (12 fixes) | `443a178` | `tasks/reviews/code-r2.md` |
| r2 | decisions Q13–Q19 | coordinator | `c704145` | `docs/fab/open-questions.md` |
| r3 | WP5b lug, nut and dome drawings in `docs/fab/contacts.md` §8 | MERGE-AFTER-DECISION (9 fixes) | `1170b2a` | `tasks/reviews/code-r3.md` |
| r3 | WP6b packing options; only C closes; sheet `docs/fab/packing-options.md` | MERGE-AFTER-DECISION (9 fixes) | `1170b2a` | `tasks/reviews/code-r3.md` |
| r3 | decisions Q20–Q23 | coordinator | `7caff1c` | `docs/fab/open-questions.md` |
| r4 | WP9b design record after rounds 1 to 3, L2 erratum | MERGE (2 fixes) | `7dec1b6` | `tasks/reviews/code-r4.md` |
| r4 | WP8-prep Stage B path in `bte_fit_shell.py`, provisional inputs, ten measured checks, no order 2 files | MERGE (17 fixes) | `7dec1b6` | `tasks/reviews/code-r4.md` |
| r4 | decisions Q24–Q27 | coordinator | `3122d44` | `docs/fab/open-questions.md` |
| r5 | Rolf's answers as Q28–Q36 | coordinator | `4dd5b46`, `cd7aea7` | `docs/fab/open-questions.md` |
| v2 | plan v2 (`docs/fab/plan-v2.md`, 11 turns, fable vs GPT-6 Pro) | SIGNED OFF WITH EDITS (turn 10), edits applied turn 11 | `ef369bd` | `tasks/plan-v2/turns/10-pro.md` |
| r5 | decisions Q37–Q56 (plan v2 and the round 5 prompts) | coordinator | `401f92d`, `5d23c54` | `docs/fab/open-questions.md` |
| r5 | WP10 + WP17 research (`docs/fab/L5-research-v2.md`, `docs/fab/L6-research-v3.md`), eight spot-checks, six retags UNVERIFIED | MERGE-AFTER-DECISION | `0195b66` | `tasks/reviews/code-r5.md` |
| r5 | WP11 packing v2 (`scripts/cad/placement_v2.py`, `docs/fab/packing-v2.md`): interface I dead 0/720, winner `A_501015_series_w20_y8_iII_s3`, REF tab crosses the end wall (exit 3, Q59) | MERGE-AFTER-DECISION (9 fixes, 864 SVGs squashed to 14) | `0195b66` | `tasks/reviews/code-r5.md` |
| r5 | WP12 board v2 (`hardware/board/`, `scripts/board/release.py`, `docs/fab/board-v2.md`): schematic ERC 0/0, PCB not placed from the packing, `--routed` fails closed | MERGE-AFTER-DECISION (11 fixes) | `0195b66` | `tasks/reviews/code-r5.md` |
| r5 | WP13 firmware v2 (`firmware/`, `src/elicio/frame_v2.py`, `docs/fab/frame-v2.md`, `docs/fab/firmware-v2.md`): frame v2 little-endian, CRC-32, compiles on the Adafruit core | MERGE-AFTER-DECISION (5 fixes) | `0195b66` | `tasks/reviews/code-r5.md` |
| r5 | WP16 design record (`docs/EARPIECE_DESIGN.md` requirement 5 titanium, plan v2 decisions, `docs/fab/orders-v2.md` ledger) | MERGE-AFTER-DECISION (2 fixes) | `0195b66` | `tasks/reviews/code-r5.md` |
| r5 | decisions Q57–Q68 | coordinator | `f306532` | `docs/fab/open-questions.md` |
| r6 | briefs WP14, WP11b, WP12b, WP13b, WP15, WP17b | coordinator | `dbe39ff` | `tasks/WP14-shell-v2.md` and siblings |
| r6 | WP11b packing follow-ups (`scripts/cad/placement_v2.py` arc-plus, DTP arc, Jauch and pack-cell runs; `docs/fab/packing-v2.md` §1b–§1e, §5 REF end-wall slot, the 501012 pack as the record cell): no buyable cell closes but the marketplace pack | MERGE-AFTER-DECISION | `110a79b` | `tasks/reviews/code-r6.md` |
| r6 | WP14 shell v2 (`docs/fab/cad/v2/`, `docs/fab/shell-v2.md`, `scripts/cad/params/shell_v2.toml`): the reviewer made every check measure the solid; four fail (closure, USB end, edge radii, wall minima), exit 3, provisional | MERGE-AFTER-DECISION | `110a79b` | `tasks/reviews/code-r6.md` |
| r6 | WP17b research v4 (`docs/fab/L7-research-v4.md` §1–§7): probe VDD + 0.3 V limit, no 501015 in ones, the 17.0 mm pack, LCSC code fixes, JLC fees and colours | MERGE-AFTER-DECISION | `110a79b` | `tasks/reviews/code-r6.md` |
| r6 | WP13b receiver v2 (`src/elicio/receiver_v2.py`, receive and receive-check commands, `firmware/src/board_pins.h`, `docs/fab/receiver-v2.md`, the ble extra) | MERGE-AFTER-DECISION | `110a79b` | `tasks/reviews/code-r6.md` |
| r6 | WP15 Rolf's sheets v2 (`docs/fab/measure.md`, `docs/fab/template.pdf`, `docs/fab/sheets/`, `docs/fab/order-board.md`, `docs/fab/order-shell.md`, `docs/fab/order-parts.md`, `docs/fab/assemble.md`) | MERGE-AFTER-DECISION | `110a79b` | `tasks/reviews/code-r6.md` |
| r6 | WP12b board placed from packing §5 (`hardware/board/build_v2b.py`, `docs/fab/board-v2.md` §9 GPIO map, BOM from L7): not routed, release refused with `--routed`, footprint collisions (Q77) | MERGE-AFTER-DECISION | `110a79b` | `tasks/reviews/code-r6.md` |
| r6 | decisions Q69–Q77 | coordinator | `58ae5b8` | `docs/fab/open-questions.md` |
| r7 | briefs WP11c, WP14b, WP13c, WP11d, WP17c, WP14c, WP12d-prep | coordinator | `e2c7f09`, `58ae5b8`, `0293d48`, `7983847`, `7b23eb5` | `tasks/WP11c-courtyards.md` and siblings |
| r7 | decisions Q78–Q80 (edge rule and board area, Contact variant A, USB-C vs TC2030) | coordinator | `7983847` | `docs/fab/open-questions.md` |
| r7 | decisions Q81–Q83 (no receptacle until M1 is measured, bosses follow the island holes, neck-end strips) | coordinator, Q81 Rolf's | `a3960d6` | `docs/fab/open-questions.md` |
| r7 | Q78 settled at width 22, Q81–Q83 with §5c's numbers; briefs WP14d, WP12d | coordinator | `d67e534` | `docs/fab/open-questions.md`, `tasks/WP14d-shell-v2d.md`, `tasks/WP12d-board-v2d.md` |
| r7 | decisions Q84 (Contact rule by area), Q85 (flat pattern); briefs WP11e, WP12e | coordinator | `aea2345` | `docs/fab/open-questions.md`, `tasks/WP11e-flat-pattern.md`, `tasks/WP12e-route-v2.md` |
| r7 | Q86 charging pad site (hook-end medial floor); WP14e brief | coordinator | `690c88e`, `77d310d` | `docs/fab/open-questions.md`, `tasks/WP14e-shell-v2e.md` |
| r7 | Q87 board deviation where the table's hole is wrong; briefs WP12f, WP11f | coordinator | `5b836a2` | `docs/fab/open-questions.md`, `tasks/WP12f-route-v2.md`, `tasks/WP11f-j4-holes.md` |
| r7 | Q88 Contact creepage at the exposed lands only; WP12g brief; round 7 closed for review | coordinator | `e06262f` | `docs/fab/open-questions.md`, `tasks/WP12g-route-v2-q88.md` |
| r7 | review r7 brief | coordinator | `d915ee3` | `tasks/review-r7.md` |
| r8 | WP12g recorded; WP12h brief | coordinator | `fea34f8` | `docs/fab/open-questions.md`, `tasks/WP12h-route-by-hand.md` |
| r7 | WP11c–WP11f packing (real courtyards, §5c grid, §5d flat pattern and pin table v2/v2.1, J4 holes from KiCad) | MERGE-AFTER-DECISION | `facb0c1` | `tasks/reviews/code-r7.md` |
| r7 | WP14b–WP14e shell (concealed medial screw, lofted lid, hook blend, width 22, hook-end pads; the reviewer opened the contact holes and measured the closure: exit 3 on `V2_CLOSURE`) | MERGE-AFTER-DECISION | `facb0c1` | `tasks/reviews/code-r7.md` |
| r7 | WP17c research v5 (`docs/fab/L8-research-v5.md`: JLC process edge, two-sided FPC assembly, Freerouting on Java 25, titanium screws) | MERGE-AFTER-DECISION | `facb0c1` | `tasks/reviews/code-r7.md` |
| r7 | WP13c dropout rule (`receive-check` exits per montage §8) | MERGE-AFTER-DECISION | `facb0c1` | `tasks/reviews/code-r7.md` |
| r7 | WP12c–WP12f board (no receptacle, two sides, flat pattern, Q84 rule areas, zero-track DRC 0, DSN classes, `routed: false`) at `fbd56e6` | MERGE-AFTER-DECISION | `facb0c1` | `tasks/reviews/code-r7.md` |
| r7 | decisions Q89–Q97 | coordinator | `5cef436` | `docs/fab/open-questions.md` |
| r8 | briefs WP11g, WP14f, WP13d | coordinator | `9354834` | `tasks/WP11g-flat-pattern-v3.md`, `tasks/WP14f-shell-v2f.md`, `tasks/WP13d-montage-scoring.md` |
| r8 | Q98 routing channels as packing constraints; WP12i brief | coordinator | `27b7991` | `docs/fab/open-questions.md`, `tasks/WP12i-board-v3.md` |

Round 7 gates at merge (`tasks/reviews/code-r7.md`, final `1be01ff`): 251
tests OK none skipped with the cad and ble extras, order 1 byte-identical,
Stage B v2 identical twice (exit 3 on the round 6 names), shell v2
identical twice and exit 3 on `V2_CLOSURE` only (measured, Q89), packing
doc byte-identical with 68 rows, `release.py` exit 0 unrouted and refused
with `--routed` (146 unconnected), DSN classes at the §12 limits, firmware
134 012 B, sheets and receiver identical, repo growth 11.43 MiB. Twelve
review fixes; the verdict's Q88 ruling adopted as Q97.
Round 6 gates at merge (`tasks/reviews/code-r6.md`, final `f407b12`): 206
tests OK none skipped with the cad and ble extras (34 named skips on the
base venv), order 1 byte-identical, Stage B v2 identical twice and exit 3
on Q59 only, shell v2 identical twice and exit 3 on four measured
failures, `scripts/board/release.py` exit 0 unrouted and refused with
`--routed` (1293 DRC errors), firmware 134012 B flash, receiver simulate
and check exit 0, repo growth 6.70 MB. Sixteen review fixes; the
reviewer's second and third turns confirmed the zero-track DRC (128
errors) and kept the decision numbers as open-questions has them.
Round 5 gates at merge (`tasks/reviews/code-r5.md`): 191 tests OK none
skipped, order 1 byte-identical, Stage B v2 identical twice and exit 3 on
Q59 only, `release.py` exit 0 (unrouted) and exit 1 with `--routed`,
`arduino-cli compile` exit 0, repo growth 0.63 MB. Round 4 gates: 129
tests OK; order 1 byte-identical; provisional Stage B identical twice,
exit 3 on Q21 only.

## In flight

Round 7 is merged (`facb0c1`); its packages are in Settled. Round 8
opened 09:05 on four lanes; every brief on main carries its start line.

- **w3 → WP11g flat pattern v3** (`tasks/WP11g-flat-pattern-v3.md`, main
  `9354834`): RUNNING since 09:05 on `lane/w3` at `facb0c1` (told to
  `git merge main` first): which side wall is the posterior edge; P4/P5
  as clamped button heads in that wall beside the cell (Q90, Q93); J2
  inside the cavity and J3 on a break-off tab (Q91, Q92); R9/R10 out
  (Q95); a cavity test for every courtyard and hang; flat pattern v3 and
  pin table v3 in §5e with the shell's wall-site table. Addendum sent
  10:05 (queues as its next turn, so expect a second DONE): the Q98
  routing channels (H1/H2 apart, a via slot beside J4, the east 0402
  row clear, 0.6 mm around U2, U3, J4) as §5e rows with a test. Waits
  for nothing from me. Report (expected)
  `.worktrees/w3/.reports/WP11g-report.md` (expected) → `DONE WP11g`
  (the second one carries the channels); then I send w1 the line "flat
  pattern v3" plus the sha and w2 the line "pin table v3" plus the sha.
- **w1 → WP14f shell v2f** (`tasks/WP14f-shell-v2f.md`, main `9354834`): WAITING since 10:20, `WAITING WP14f flat pattern v3`
  received, lane at `89279c2` on `lane/w1-r6` (tree clean, no report
  yet, expected). First half done: Q89 built, lid boss 3.2 mm into a
  tail pocket, M2.5×8, `lid_engagement` 4.75, `V2_CLOSURE` passes,
  build exit 0; the medial well moved to (16.50, 41.00) to clear the
  REF pocket, tail boss OD 9.94 measured; renders viewed (medial still
  shows the Q86 skin pads until the wall pads are cut). Waits for my
  line "flat pattern v3" plus w3's sha, then cuts the Q90 wall pads at
  the v3 sites, third view with the wall, closure text. Report
  (expected) `.worktrees/w1/.reports/WP14f-report.md` (expected) →
  `DONE WP14f`; then sheet v13 with the new renders.
- **w4 → WP13d montage scoring** (`tasks/WP13d-montage-scoring.md`, main
  `9354834`): LANDED, `DONE WP13d` at `dbeeafa` on `lane/w4` (tree
  clean, report `.worktrees/w4/.reports/WP13d-report.md` present, 251
  tests OK with 28 named CAD skips): one sentence each in
  `docs/fab/receiver-v2.md` and `docs/fab/montage.md` §8 (Q96). w4 idle.
- **w2 → WP12h hand-route** (`tasks/WP12h-route-by-hand.md`, main
  `fea34f8`): LANDED UN-ROUTED, `DONE WP12h` at `c9c750d` on `lane/w2`
  (tree clean, report `.worktrees/w2/.reports/WP12h-report.md` present,
  board tests 18 OK, ERC 0, DRC 0 errors / 63 unconnected / 0 shorts,
  WP12g copper untouched). `hardware/board/hand_route.py` closed
  nothing; `route.md` §12 names every rat with its two coppers and
  millimetres (H1/H2 gap 1.20 with two traces in it, J4 walled by the
  SIG2 run, R16 on B.Cu by a J4 hole, J3 vs Contact clearance, U2 pads
  at 0.20 gap, U3 DSBGA 0.40 pitch); JLC's extreme via 0.10/0.30 tried
  on a copy (56 unconnected, 63 via-rule errors, not imported). → Q98.
- **w2 → WP12i board v3** (`tasks/WP12i-board-v3.md`, main `27b7991`):
  RUNNING since 10:05 on `lane/w2` on top of `c9c750d` (told to `git
  merge main` first): U2/U3 footprints against datasheets (U3 swap to a
  larger package if its ball cannot escape, a stated BOM change), R9/R10
  DNP (Q95), stiffener zones (Q94), Q97 envelope tests, the §5e parser;
  then it STOPS with `WAITING WP12i pin table v3` unless I have sent
  that line plus w3's sha; then re-pin on v3 with the Q98 channels,
  lock Contact routes, hand-route then Freerouting, DRC 0 and 0
  unconnected, `release.py --routed`; or name the pads and stop.
  Report (expected) `.worktrees/w2/.reports/WP12i-report.md` (expected)
  → `DONE WP12i`.
- **w5** (agy, `lane/w5` at `facb0c1`): idle since WP17c landed; no
  research package open. **w9** (cursor, `lane/w9` at `facb0c1`): idle
  since WP15 (round 6); a WP15b sheets refill waits until the pads, the
  screw and the board settle.
- **rev7** (review r7): closed at 09:00 after `DONE review-r7` at
  `1be01ff`; tab `w1B:tT` closed (its GONE received), the worktree
  removed, branch `review/r7` kept.

## Open

Plan v2 carries claims C1–C16 and gates G1–G8; Q1–Q68 hold the readings.
Outside those:

1. `lane/w1` diverged from `main` at `7df78b5` with 864 SVGs (109 MB,
   pushed). Q56: nobody deletes it but Rolf; round 6 work is on `lane/w1-r6`.
2. The answer sheet (artifact `https://claude.ai/artifact/5e9H1dC5CFHggtiaYtDDeA`)
   is at version 12 (09:30: question 6c rewritten for the back-edge
   pads with the cover-plus-switch and small-tail alternatives, the Q89
   screw-length note; the renders are still WP14e's and say so);
   version 11 (07:00) the WP14e renders; version 10 said the body
   is 22 wide; version 8 added question 6b the charging port; version 6
   (00:45) the reviewed renders; version 5 (00:05) question 2b the
   battery route;
   version 4 (23:35) the first WP14 renders; version 3 (22:40) brought: M1, body 9.0, ceiling, look and colour,
   China or not and ship-to, the charging rule, priorities, module route,
   probes owned, tools on the Mac, anything else. Answers land in db doc
   `answers/rolf` (ArtifactData `get`), merged with his earlier fields;
   `sheet: 3` marks a v3 save.
3. The vault holds rounds 1 to 7 (page `Wiki/projects/Elicio.md`, stub
   `raw/research/2026-09-18-elicio-round-7-flat-pattern-review.md`, vault
   main `a3826dd`, filed 09:35; no run is open).
4. The HANDOFF checker treats any backticked path as a claim; nonexistent
   ones need "(expected)" or "(absent on main)" on the same line.
5. Order 1 (the fit gauge) is not ordered and will not be: plan v2 is one
   order per thing; `docs/fab/cad/v1/` stays byte-identical as the
   regression anchor only.
6. Seams for review r8, collected as lanes land (they go into the
   review brief, expected at `tasks/review-r8.md` (expected)): pin table
   v3 against the board and the shell (P4/P5 wall sites, J2 inside, the
   break-off tab, R9/R10 gone); WP12h routes on the v2.1 flat pattern
   before v3 exists (WP12i re-pins; check what survived); the shell's
   drop channel was described as 0.31 high while the cut is 3.0 tall
   (moot once removed); `hardware/board/packing_v2_flat.md` is still pin
   table v2 (re-vendor v3); three STEP models missing in the release;
   `V2_CLOSURE` measured in the lid (Q89); L8's UNVERIFIED prices; the
   Q84/Q88 rows still attribute 1.0 mm to plan v2 §5.3 (Q97 corrects it
   in its own row; the rows are not edited); Rolf's Q90 alternative (a
   cover plus a switch) untouched unless he picks it.

## Next

- Idle until `DONE WP11g` (w3; the second DONE carries the Q98
  channels), `DONE WP14f` or `WAITING WP14f flat pattern v3` (w1),
  `DONE WP12i` or `WAITING WP12i pin table v3` (w2), or BLOCKED/GONE for
  any (a DONE is checked: report present, tree clean; then read); on
  w3's final DONE send w1 "flat pattern v3" plus the sha and w2 "pin
  table v3" plus the sha; when WP11g, WP14f and WP12i have landed
  (WP13d has), open review r8 the way r7 was opened (merge order w3,
  w1-r6, w4, w2).

## Traps

- After a herdr restart, a non-Claude lane comes back as its bare resume
  line (`agy --conversation <id>`) without the flags it was started
  with; agy then asks for every URL, edit and command and no BLOCKED
  push arrives for it. Check `herdr pane process-info --pane <id>` after
  a restart and restart such an agent with its recorded start line plus
  `--conversation <id>` (the conversation survives).

- zsh does not word-split an unquoted variable: `set -- $pkg` with
  `pkg="w2 WP12-board"` gives `$1` = the whole string, and
  `herdr agent prompt $1` fails with "agent ... not found". Three lane
  prompts were lost that way on 2026-09-17; write each prompt out.
- A python rewrite script that asserts on anchors before `write_text`
  leaves the file untouched when one anchor misses, and a following
  `git commit` in the same command still commits the other files. Turn 07
  went to Pro with the plan unchanged. Run `git show --stat HEAD` and
  read it before prompting anyone with a sha.

- `pro-mcp start --help` and `pro-mcp status` run a real serve: the first
  opens a Pro tab, the second fails to bind 8765 and turns the shared
  Tailscale funnel off → only `pro-mcp --help` and `pro-mcp url` are safe
  reads; recover with `launchctl kickstart -k gui/$(id -u)/com.rolfiersbox.pro-mcp`
  and check `tailscale funnel status` shows `/` → 8765 and `/wiki` → 8766.
- The name `coordinator` is taken by the flyonenomics coordinator in `w16`
  → this project's coordinator is `elicio`; every brief's closing steps push
  to `elicio`.
- agy lanes drop a prompt sent before their TUI is ready and `agent prompt`
  stalls on them → `herdr pane run PANE-ID "the prompt text"` then
  `herdr pane send-keys PANE-ID enter`; read the pane once to confirm; trust
  only the DONE push, never the status.
- `grok` is not a CLI here → Grok runs as `--kind cursor -- --model cursor-grok-4.6-xhigh --force`.
- Cursor lanes take the whole brief in one `herdr agent prompt`; they fetch
  datasheet pages themselves (allowed by `tasks/phase1-common.md`).
- The post-commit hook pushes every branch to origin, lanes and `review/*`
  included → lanes report "the hook pushed"; not a defect.
- Plan §3.3's table writes the chord gate backwards → the build follows Q1
  (`M1 ≥ TOTAL_CHORD + 3`); do not "fix" the script to match the table.
- The review worktree path is reused each round → `git worktree remove
  .worktrees/review` after the merge or the next `worktree add` fails.
- A reviewer may spawn its own helper lane under its pane (round 2: agy
  `r2ds`) → after closing the review tab, list the workspace tabs and close
  the orphan.
- Claude Code's bypass mode still blocks `rm -rf $VAR/$x` with "Dangerous rm
  operation on possibly-empty variable path" → the server pushes `BLOCKED`;
  read the pane once, then `herdr agent send-keys` with `enter` on that
  agent if the path is the lane's own scratchpad.
- The coordinator's Read tool cannot rasterize a PDF (no poppler) →
  `scripts/cad/render.py --debug-png` writes the drawing page as PNG.
- Two lanes editing `pyproject.toml`, `tests/test_cad.py`,
  `scripts/cad/README.md`, `scripts/cad/bte_fit_shell.py` in one round →
  the reviewer resolves; name the shared files in its brief.
- A lane can force-add its report file under `.reports/` despite
  `.gitignore` → the reviewer `git rm --cached` it.
- A coordinator note sent to a Cursor lane mid-package lands in its
  follow-up queue and runs as a new turn after the lane's DONE → expect a
  second DONE; do not open the review on the first one.
- Quote drawing numbers with their datum. "6.27 from the ring edge" became
  "6.27 from the Ø7.1 edge" in a coordinator prompt and cost WP6b a pass;
  the drawing's number is 8.85 from the contact centre (8.788 max).
- A lane's "every number has a source" can be false (WP7a citations, WP5b
  dead URLs and page claims) → the reviewer checks quotes verbatim, with a
  read-only agy lane for live pages if needed.
- CAD lanes write checks as constants or cut-then-probe tautologies
  (rounds 1, 2 and 4) and fork the construction to keep hashes stable
  (round 4) → every CAD brief says "measured on the built solid, one
  construction path", and the reviewer builds and sections a part itself.
- The XIAO nRF52840 charges at a fixed 50 mA; a 40 mAh cell may not
  allow it (plan v2 claim C3). Do not pick architecture C before C3 and
  WP11 are in.
- Rolf answers in plain-English radio buttons; "thin" and "on bone" were
  given before any fit check. Treat them as preferences, and say so when
  the arithmetic refuses one (plan v2 §3, D-1).
- `sed -i ''` fails on non-ASCII patterns → edit with python.
- A relative screenshot path lands in the repo root → absolute scratchpad paths.
- Do not `cd` into worktrees from the coordinator shell → `git -C` with the
  worktree path.
- `herdr agent read` output is plain text, not JSON → do not pipe it to a
  JSON parser.

- A review branch that was cut from `main` before the coordinator
  committed on `main` again is no fast-forward: `merge-base --is-ancestor`
  says no → `git merge --no-ff review/r5` (the round's branch) from the clean root
  checkout; keep the round's decisions commit before the merge.
- A failed `state.py check` followed by another command in the same shell
  line still lets `git commit` run (`c057aba` on 2026-09-17) → `check &&
  git add && git commit`, never `check; ...`.
- A CAD lane's placement search can write thousands of per-run drawings
  into the repo (`lane/w1`, 864 SVGs, 109 MB pushed by the hook) → every
  brief caps generated files and says "closers only"; the reviewer squashes.

- A brief that prescribes the last commit message as a fact ("…,
  routed") gets that message verbatim even when the gate failed (WP12d,
  `1e055de`). Prescribe messages that describe the state, or "if the
  gate passes"; tell lanes the message says what is true.
- A pin table that mixes folded (shell) and flat (PCB) coordinates gets
  pinned literally (WP12d: the SIG2 ring pad inside U1). Flex boards are
  drawn flat: the packing publishes flat coordinates for the PCB and
  folded sites for the shell, in two tables (Q85).
- A packing table without a cavity test put J2, J3 and the charge tab's
  root outside the body for a whole round (r7, Q91, Q92). Every packing
  brief names the cavity test for every courtyard, hang and tab root.
- The gauge's mock contact domes stayed fused over the contact holes
  into the shell for a round because the checks probed mid-wall. Every
  skin-face or wall feature gets a face probe (air at the face).
- A check that reads a joint's number from one part ("screw engagement
  4.30 in the tail boss") is not a measurement of the joint; measure
  both parts (the screw tip against the lid boss, Q89).
- Charging pads on the skin face are a safety rule violation (220 kΩ
  per path, R7/G2) however they are recessed; the packing puts bare
  charge copper only where skin cannot reach.

<!-- Everything below this line is generated. Regenerate it at every
checkpoint with:  python3 ~/.claude/skills/save-state/state.py snapshot
Do not hand-edit ids into it. -->

## Herdr (generated 2026-09-18T07:19:18-04:00 by state.py, herdr 0.9.0, session `default`)
Workspace `w1B` (elicio), 8 tabs. Coordinator: pane `w1B:p1` in tab `w1B:t1`, agent name `elicio`, kind claude, status working, cwd `/Users/rolfie/projects/elicio`.
Coordinator session id `61ba63c7-8fd8-497e-b665-c65cc34e72f6`; transcript `/Users/rolfie/.claude/projects/-Users-rolfie-projects-elicio/61ba63c7-8fd8-497e-b665-c65cc34e72f6.jsonl`.

### Workers nested under the coordinator
| name | kind | status | pane | tab (label) | cwd | tokens | last title |
|---|---|---|---|---|---|---|---|
| w1 | cursor | working | `w1B:pA` | `w1B:tA` (w1) | `/Users/rolfie/projects/elicio/.worktrees/w1` | done=1 lane=WP14e | Lane W1 Instructions |
| w2 | cursor | working | `w1B:pB` | `w1B:tB` (w2) | `/Users/rolfie/projects/elicio/.worktrees/w2` | done=1 lane=WP12g waiting=pin table v2 | Lane W2 Instructions |
| w4 | cursor | working | `w1B:pC` | `w1B:tC` (w4) | `/Users/rolfie/projects/elicio/.worktrees/w4` | done=1 lane=WP13c | Lane W4 Instructions |
| w5 | agy | done | `w1B:pD` | `w1B:tD` (w5) | `/Users/rolfie/projects/elicio/.worktrees/w5` | done=1 lane=WP17c |  |
| w9 | cursor | done | `w1B:pE` | `w1B:tE` (w9) | `/Users/rolfie/projects/elicio/.worktrees/w9` | done=1 lane=WP15 | Lane W9 Instructions |
| w3 | cursor | working | `w1B:pR` | `w1B:tR` (w3) | `/Users/rolfie/projects/elicio/.worktrees/w3` | done=1 lane=WP11e | New Package Brief |

Start lines as they run now (from `pane process-info`), for restarting a worker that is gone:

```bash
herdr agent start w1 --kind cursor --pane <new pane> --parent "$HERDR_PANE_ID" -- --resume 791832d5-f944-40f4-80ec-82deb5c4efca
herdr agent start w2 --kind cursor --pane <new pane> --parent "$HERDR_PANE_ID" -- --resume 137b6bf4-e654-4a43-bc69-e0421552a50c
herdr agent start w4 --kind cursor --pane <new pane> --parent "$HERDR_PANE_ID" -- --resume 3f977624-113c-48fa-b55e-666aa970b9a3
herdr agent start w5 --kind agy --pane <new pane> --parent "$HERDR_PANE_ID" -- --conversation 18235bfb-f5b8-4365-9383-d66c69251f4b --dangerously-skip-permissions --add-dir /Users/rolfie/projects/elicio --effort high --model gemini-3.8-flash-high
herdr agent start w9 --kind cursor --pane <new pane> --parent "$HERDR_PANE_ID" -- --resume ea20ccc0-04da-408f-a016-57766846ee99
herdr agent start w3 --kind cursor --pane <new pane> --parent "$HERDR_PANE_ID" -- --model cursor-grok-4.6-xhigh --force
```

Other workspaces on this server (not yours to touch): `w16` flyonenomics (done), `w1D` ablirated (idle), `w1E` jevtest (idle)

### Git
Repo `/Users/rolfie/projects/elicio`, integration branch `main` (0 ahead, 0 behind origin/main).

| worktree | branch | head | dirty files | last commit |
|---|---|---|---|---|
| `/Users/rolfie/projects/elicio` | `main` | 9354834 | 0 | Round 8: briefs WP11g (flat pattern v3, pads in the far side wall, J2 inside, J3 break-off, R9/R10 out), WP14f (lid boss and long screw, then wall pads), WP13d (Q96 sentences) |
| `/Users/rolfie/projects/elicio/.worktrees/w1` | `lane/w1-r6` | facb0c1 | 0 | Merge review/r7: round 7 (packing v2.1 and the flat pattern, shell v2e, L8 v5, dropout rule, board placed on the flat pattern) with the reviewer's fixes; verdict MERGE-AFTER-DECISION, Q89–Q97 recorded |
| `/Users/rolfie/projects/elicio/.worktrees/w2` | `lane/w2` | 795d154 | 1 | Merge remote-tracking branch 'origin/main' into lane/w2 |
| `/Users/rolfie/projects/elicio/.worktrees/w3` | `lane/w3` | facb0c1 | 0 | Merge review/r7: round 7 (packing v2.1 and the flat pattern, shell v2e, L8 v5, dropout rule, board placed on the flat pattern) with the reviewer's fixes; verdict MERGE-AFTER-DECISION, Q89–Q97 recorded |
| `/Users/rolfie/projects/elicio/.worktrees/w4` | `lane/w4` | 9354834 | 0 | Round 8: briefs WP11g (flat pattern v3, pads in the far side wall, J2 inside, J3 break-off, R9/R10 out), WP14f (lid boss and long screw, then wall pads), WP13d (Q96 sentences) |
| `/Users/rolfie/projects/elicio/.worktrees/w5` | `lane/w5` | facb0c1 | 0 | Merge review/r7: round 7 (packing v2.1 and the flat pattern, shell v2e, L8 v5, dropout rule, board placed on the flat pattern) with the reviewer's fixes; verdict MERGE-AFTER-DECISION, Q89–Q97 recorded |
| `/Users/rolfie/projects/elicio/.worktrees/w9` | `lane/w9` | facb0c1 | 0 | Merge review/r7: round 7 (packing v2.1 and the flat pattern, shell v2e, L8 v5, dropout rule, board placed on the flat pattern) with the reviewer's fixes; verdict MERGE-AFTER-DECISION, Q89–Q97 recorded |

Last commits on the integration branch:

```
9354834 Round 8: briefs WP11g (flat pattern v3, pads in the far side wall, J2 inside, J3 break-off, R9/R10 out), WP14f (lid boss and long screw, then wall pads), WP13d (Q96 sentences)
facb0c1 Merge review/r7: round 7 (packing v2.1 and the flat pattern, shell v2e, L8 v5, dropout rule, board placed on the flat pattern) with the reviewer's fixes; verdict MERGE-AFTER-DECISION, Q89–Q97 recorded
5cef436 Round 7 verdict: Q89–Q97 recorded with readings (lid boss and longer screw, charging pads off the skin face, J2 inside, break-off J3, flat pattern v3, stiffeners, R9/R10 DNP, montage scoring, contact envelope)
1be01ff review: code-r7 verdict MERGE-AFTER-DECISION; gates, defects, §7 look, Q88 ruling, decisions 89–97
3696f5c review(WP11): undo the R24 packing move; the board moves to v2.1 in WP12g (Q87 closed)
210804d review(WP12): board-v2 §11–§13 describe the Gerber this round carries
```

### Record files (newest first)
- handoff: `HANDOFF.md`
- briefs: `tasks/WP13d-montage-scoring.md`, `tasks/WP14f-shell-v2f.md`, `tasks/WP11g-flat-pattern-v3.md`, `tasks/WP12h-route-by-hand.md`, `tasks/review-r7.md`, `tasks/WP12g-route-v2-q88.md`, `tasks/WP11f-j4-holes.md`, `tasks/WP12f-route-v2.md`, `tasks/WP14e-shell-v2e.md`, `tasks/WP12e-route-v2.md`, `tasks/WP11e-flat-pattern.md`, `tasks/WP12d-board-v2d.md`
- verdicts: `tasks/reviews/code-r7.md`, `tasks/reviews/code-r6.md`, `tasks/reviews/code-r5.md`, `tasks/reviews/code-r4.md`, `tasks/reviews/code-r3.md`, `tasks/reviews/code-r2.md`, `tasks/reviews/code-r1.md`

### Restore
Run from the coordinator pane after a server restart, or from the fresh coordinator pane that takes over:

```bash
python3 ~/.claude/skills/save-state/state.py restore --from /Users/rolfie/projects/elicio/HANDOFF.json
# the old coordinator conversation, if herdr did not resume it in the pane:
# cd /Users/rolfie/projects/elicio && claude --resume 61ba63c7-8fd8-497e-b665-c65cc34e72f6
```
