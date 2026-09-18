# WP11 — Packing v2: which architecture closes (lane w1)

Read `tasks/phase1-common.md` first, then `docs/fab/plan-v2.md` (draft,
turn 01) §3, §4, §5, §8 and §11 row 11, and `docs/fab/open-questions.md`
Q28 to Q36. Lane `w1`, worktree `/home/user/projects/elicio/.worktrees/w1`,
branch `lane/w1`. Start line (coordinator restarts you by copy-paste):

    herdr agent start w1 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Why: Rolf's answers changed the plan (one order per thing, a custom board
assembled by the vendor, no wires or lugs, the smallest body that closes).
Plan v2 §4 names three radio candidates and a rule; §3 does the height
arithmetic by hand. Your package turns that into measured layouts so the
spec dialogue and Rolf decide on numbers, not prose. Analysis package:
you change no plan, order nothing, contact nobody.

Owns: `scripts/cad/placement.py`, the Stage B path of
`scripts/cad/bte_fit_shell.py` and its parameter files under
`scripts/cad/params/`, `tests/test_placement.py`, `tests/test_cad.py`,
`docs/fab/packing-v2.md` (new), `docs/fab/cad/v1/placement_v2_*.svg` (new).
Order 1 outputs (`docs/fab/cad/v1/*.step|stl|3mf`, `manifest.json`,
`render_*.png`, `drawing.pdf`) stay byte-identical; nothing under
`docs/fab/cad/v2/`.

Inputs you take as given (each with its source in the report):

- Modules: A Raytac MDBT50Q-1MV2 10.5 × 15.5 × 2.0; B Ebyte E73-2G4M08S1C
  13 × 18 × 2.0; C Seeed XIAO nRF52840 21.0 × 17.5, PCB 1.2, 4.5 tall
  over the USB-C, the connector at one short end and protruding ~1.0
  beyond the board edge (state the number you use and where from; the
  Seeed wiki has the STEP). Antenna keep-outs from each module's sheet;
  where the sheet is unreachable, the v1 rule from `docs/fab/interface.md`
  §6.3 and say so.
- Cells: DTP301120 with protection 22.0 × 11.5 × 3.2 (SparkFun PRT-25270,
  drawing in `.worktrees/w5/docs/fab/L5-research-v2.md` §1, or
  `git show lane/w5:docs/fab/L5-research-v2.md`); 501015 as v1. Foam 0.3
  under a cell.
- Board: flex 0.11 plus a 0.3 stiffener under parts (0.4 where parts sit,
  0.2 at the tabs). Front end: ADS1292 VQFN-32 5.0 × 5.0 × 1.0 courtyard
  as `placement.py` has it, its passives as before, no charger and no LDO
  for C (the XIAO has them), BQ25100 + TLV713 for A and B, a JST-SH
  receptacle 4.0 × 6.0 × 2.9 (side entry) for the cell, a USB-C 16-pin
  receptacle 8.9 × 7.3 × 3.2 for A and B, SWD/UART pads 1.0 × 1.0 × 5.
- Contacts: as interface v2 and contacts.md §8, but no lug and no wire.
  Each contact gets a flex tab: a ring pad Ø5.0 with a Ø2.7 hole clamped
  under the brass nut (DIN 439 M2.5, m 1.6, s 5.0), on a 2.5-wide strip
  that leaves the ring toward the board along a path you choose and
  report. Stack inside the wall = tab 0.2 + nut 1.6 + screw tip beyond
  the nut per the screw length; state it. The reference tab runs to the
  tail pocket; the pocket may grow (Q28).
- Body: BODY_WIDTH 18, 19, 20; LID_Y 8.0, 8.5, 9.0 (floor 1.5 as v1);
  BODY_ARC as v1 plus 0, +1.5, +3.0 only if nothing closes at v1 length.
  Every other parameter as `stageb_provisional.toml`.

Deliver:

1. `placement.py --arch A|B|C --cell dtp|501015 --layout series|stacked
   --width W --lid-y Y [--arc-plus X]` laying out the parts above with
   `layout_conflicts()` extended to heights (a part's top against the lid
   band and against anything above it), to the flex tabs (they are parts:
   width, thickness, bend radius ≥ 1.0, no crossing of another tab or a
   courtyard), to the antenna zone, and to the USB receptacle's opening if
   the layout puts it at the end wall (report the wall it would cut,
   decide nothing). One SVG per run under
   `docs/fab/cad/v1/placement_v2_<arch>_<cell>_<layout>_w<W>_y<Y>.svg`
   with the conflicts listed on the drawing.
2. Stage B of `bte_fit_shell.py` takes the winner layouts (every one that
   closes in step 1, at most six) and measures on the built solid: the
   cell envelope, the module envelope with its keep-out, the board and tab
   envelopes, the contact stacks, the lid band, wall minima, TOTAL_CHORD
   and the M1 gate. One construction path with order 1 (the reviewer of
   round 4 folded a fork back; do not fork again). Checks are measured,
   never constants; a check that cannot be measured is reported as
   NOT_MEASURED with why, not as passed.
3. `docs/fab/packing-v2.md`: one table of every run (arch, cell, layout,
   width, lid, closes yes/no, first conflict, free area, TOTAL_CHORD, M1
   gate), then the §4 rule of plan v2 applied line by line with the
   measured numbers, then the smallest body per architecture, then the
   layout you would hand to the board lane for each architecture that
   closes (part positions, tab paths, receptacle position). No
   recommendation beyond the rule; the dialogue decides.
4. Tests: every new path exercised; a failing layout fails; identical
   regeneration of every SVG and of the provisional Stage B build.

Gates: `.venv/bin/python -m unittest discover -s tests -v` green, none
skipped (build123d installed in your private `.venv`); order 1 files
byte-identical to `main`; two consecutive Stage B runs identical. Commit
in steps; the last commit is `packing(v2): which architectures close`.
Report `.reports/WP11-report.md` (keep it untracked): the table, what
could not be measured, every number you took as given with its source,
"Needs a decision". Closing steps per the common file with `<PKG>` =
`WP11`, `<lane>` = `w1`. If a mid-package prompt from the coordinator
arrives, it runs after your DONE as a new turn; expect that and push a
second DONE for it.
