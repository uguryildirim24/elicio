# WP12b — Board v2, turn 3: place from the packing, sync, route, release (lane w2)

Read `tasks/phase1-common.md` first (for this package "the plan" is
`docs/fab/plan-v2.md`, signed off at `ef369bd`), then plan v2 §4 G1 to
G7, §5 all, §8, §11 row 12; `docs/fab/open-questions.md` Q50 to Q68 (Q58,
Q60, Q62, Q63, Q64, Q65, Q67, Q68 govern you); `docs/fab/board-v2.md` as
the reviewer left it (§15, §18, §19 first); `docs/fab/packing-v2.md` §5
and §6; `tasks/reviews/code-r5.md` defects 15 to 25 and 3, 4; your own
`.reports/WP12-report.md`. Lane `w2`, worktree
`/home/user/projects/elicio/.worktrees/w2`, branch `lane/w2`
(fast-forwarded to `main` at the round 5 merge). Start line (coordinator
restarts you by copy-paste):

    herdr agent start w2 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Why: the round 5 reviewer fixed the schematic (charger ISET, LED gate,
VBAT divider, ERC 0/0) but the PCB is not a placement: it follows your
own packing run instead of `packing-v2.md` §5, has 3 nets and 877 DRC
errors, and `release.py --routed` fails closed on it by design (Q62). S0
needs a routed, released flex board that matches the shell's numbers.
Nothing is ordered, quoted or uploaded.

Owns: `hardware/board/` (all), `scripts/board/release.py`,
`tests/test_board_release.py`, `docs/fab/board-v2.md`. Nothing else;
`firmware/src/board_pins.h` is WP13b's (lane w4) and takes your §9 map
as its input, so publish the final GPIO map in `board-v2.md` §9 first
and commit it early.

Deliver:

1. **Placement from the packing** (Q62): outline, module pose and its
   keep-out (review r5 defect 4), cell connector edge, USB-C on the
   end-face edge, the three tab exits and ring pads, the switch under the
   lid's recess, the bench header, TC2030, all from `packing-v2.md` §5 for
   `A_501015_series_w20_y8_iII_s3`; if WP11b (`lane/w3`) publishes a REF
   tab route before you place, use it (`git show lane/w3:docs/fab/packing-v2.md`)
   and say so. Board-to-packing agreement checked by a test that reads
   both (positions within 0.1 mm).
2. **Sync and route**: every schematic net on the PCB, 2-layer flex rules
   from JLC's FPC page (quoted, dated, encoded as DRC rules), the contact
   nets isolated (1.0 mm clear of other copper, no copper of theirs under
   the module keep-out), the ADS1292 analog front end with the 220 kΩ at
   the tab entries, star ground where the sheet asks, USB pairs short,
   antenna keep-out empty. `release.py --routed` exits 0 with DRC 0
   errors, 0 unconnected, `routed: true`; the tests assert it.
3. **Stiffeners** (Q60): merge pieces to three or fewer if the geometry
   allows (one island under the parts, one per tab only where the ring
   needs it); the pieces as separate mechanical layers with a legend the
   assembler reads; the count and JLC's fee text in `board-v2.md` §18.
4. **Circuit closures**: decoupling per the ADS1292 sheet (10 µF + 0.1 µF
   per supply at the pins, Q68); the standby load during charge computed
   from the sheets (nRF idle and system-off, LDO quiescent, ADS powered
   down, dividers, gate leakage) against the BQ25100 termination floor
   with the margin stated (Q65); the LED and ISET as the reviewer left
   them (defects 15, 16) re-checked; REGOUT0 and the first-load voltage
   in §4 with the G4 consequence (Q64: the kit question is WP17b's, you
   state what the board offers: VTref on TC2030 pin 1 from the actual
   rail, and whether a 1.8 V first session can set REGOUT0 through a
   3.3 V probe without exceeding the pin limits, from the nRF52840 sheet's
   absolute maximum).
5. **BOM** (Q63): every line with an LCSC number re-read on its page
   today (URL, date, displayed stock, tier, price) or UNVERIFIED; the 18
   blanked lines filled or left UNVERIFIED with the search tried; U1's
   two candidate numbers resolved from the pages or both left with
   their evidence; the Raytac routes (Q67) both in §18 with JLC's global
   sourcing and consignment page text.
6. **Joint inputs for G7** in `board-v2.md` §11: ring pad copper and
   coverlay opening, ENIG thickness from JLC's page, the tab's bend
   radius and strain relief, the datum from the ring's hole to the
   board's outline, how the ring is captured under the standoff (Q58), and
   the STEP of the board with the tabs modelled flat plus a note on the
   fold.
7. `board-v2.md` updated throughout; §19 "Needs a decision" renumbered
   from what remains; the rejected interface I stays in §11a.

Gates: `.venv/bin/python -m unittest discover -s tests -v` green;
`release.py --routed` exit 0 with the numbers in the report; `git diff
main -- docs/fab/plan-v2.md docs/fab/open-questions.md firmware/` empty;
`git status --short` empty. Commit in steps; the last commit is
`board(v2b): placed from the packing, routed, released`. Report
`.reports/WP12b-report.md` (untracked): what changed, each gate with
command and result, the release summary, what stayed UNVERIFIED, "Needs
a decision", the final sha. Closing steps per the common file with
`<PKG>` = `WP12b`, `<lane>` = `w2`. A mid-package prompt from the
coordinator runs after your DONE as a new turn; push another DONE for it.
