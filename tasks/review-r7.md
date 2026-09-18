# Code review + fix — Phase 1 round 7 (WP11c–WP11f, WP14b–WP14e, WP17c, WP13c, WP12c–WP12f) on branch review/r7 (Claude Opus 5, high)

You are the reviewer for this round, herdr agent `rev7`. Five lanes
finished fourteen packages under plan v2 (signed off at `ef369bd`). You
merge them into one candidate, inspect it, **fix what is wrong
yourself**, run every gate, and write one verdict. You never push by hand
(the repo's post-commit hook pushes every commit), never merge into
`main`, never touch another worktree, never edit `docs/fab/plan.md`,
`docs/fab/plan-v2.md` or `docs/fab/open-questions.md`. No purchase,
sign-up, quote request, upload or vendor contact; web only to re-read a
page a lane cites. No Agent-tool subagents. Rolf is asleep; nothing
waits on him. Rolf is "Rolf", never "owner" or "user".

Worktree `/home/user/projects/elicio/.worktrees/review`, branch
`review/r7` from `main`. Private environment inside this worktree:
`python3.13 -m venv .venv && .venv/bin/python -m pip install -e '.[cad]'`
plus `-e '.[ble]'` (and the sheets extra if `pyproject.toml` has one).
KiCad 10 (`kicad-cli`), `arduino-cli` with the Adafruit nRF52 core,
matplotlib, Homebrew OpenJDK 25 (`/opt/homebrew/opt/openjdk@25/bin/java`)
and Freerouting 2.4.1 at `~/.local/opt/freerouting/` are on this Mac;
install nothing else.

Start line (the coordinator restarts you by copy-paste):

    herdr agent start rev7 --kind claude --pane <pane> --parent w1B:p1 -- --model claude-opus-5 --effort high --dangerously-skip-permissions

## Steps

1. Read `tasks/phase1-common.md`, `docs/fab/plan-v2.md` (§3 to §9, §11),
   `docs/fab/open-questions.md` Q69 to Q88 with the Round 7 notes (the
   coordinator's readings for this round; you check them, you do not
   re-decide them unless a fact contradicts them), the round 6 verdict
   `tasks/reviews/code-r6.md` (decisions 69 to 77 bind this round), and
   the briefs `tasks/WP13c-dropout.md`, `tasks/WP11c-layout-v2.md` (or
   the WP11c brief under `tasks/`), `tasks/WP11d-layout-v2c.md`,
   `tasks/WP11e-flat-pattern.md`, `tasks/WP11f-j4-holes.md`,
   `tasks/WP14b-shell-v2b.md`, `tasks/WP14c-shell-v2c.md`,
   `tasks/WP14d-shell-v2d.md`, `tasks/WP14e-shell-v2e.md`,
   `tasks/WP17c-research-v5.md`, `tasks/WP12d-prep-router.md`,
   `tasks/WP12d-board-v2d.md`, `tasks/WP12e-route-v2.md`,
   `tasks/WP12f-route-v2.md`, and the reports pasted below.
2. Merge, in this order, resolving conflicts yourself: `lane/w3` at
   `e4b857c` (WP11c to WP11f), `lane/w1-r6` at `bdfc429` (WP14b to
   WP14e; NOT `lane/w1`, round 5's branch with 109 MB of drawings, Q56),
   `lane/w5` at `f8b1634` (WP17c), `lane/w4` at `21dde8a` (WP13c), and
   `lane/w2` **at commit `fbd56e6` exactly** (`git merge fbd56e6`),
   because lane w2 keeps working on `lane/w2` after that commit (WP12g,
   routing under Q88) while you review. Each lane's diff against `main`
   shows `HANDOFF.md` and `HANDOFF.json` as changed only because `main`
   moved after the lanes branched; keep `main`'s.
3. Gates, all on the merged tree:
   - `LC_ALL=C .venv/bin/python -m unittest discover -s tests -v` passes
     with the CAD, render, placement (including `PlacementWP11eTests`
     and `PlacementWP11fTests`), shell v2, board-release, receiver and
     sheets tests running, not skipped; report count and skips per
     extra.
   - Order 1 untouched: reference build twice, solids identical to each
     other and to `docs/fab/cad/v1/`; `render.py` twice identical; the v1
     `manifest.json` byte-identical to `main`'s.
   - Stage B v2 built twice into a temp dir: byte-identical.
   - Shell v2 (`shell_v2.toml`, `STAGE=shell`) built twice: byte-identical
     to each other and to `docs/fab/cad/v2/`; exit 0; every check a
     number, NOT_MEASURED or NOT_APPLICABLE by name (V2_USB_end is
     NOT_APPLICABLE under Q81); render stamp equals `manifest.commit`
     equals the solids commit; `manifest.py --check-bytes` ok.
   - `scripts/cad/placement.py --packing-doc` regenerates
     `docs/fab/packing-v2.md` byte-identical; §5d's pin table v2.1 has 68
     rows; the folded-site table equals §5's contact sites plus the Q86
     P4/P5 sites; drawings under `docs/fab/cad/v2c/` ≤ 4.
   - `scripts/board/release.py` (without `--routed`) exits 0: ERC 0, BOM
     rows = placed parts, outputs present; with `--routed` it is REFUSED
     on this candidate (146 unconnected) and the test asserts the
     refusal; `summary.json` says `routed: false`. The
     placement-agreement test reads both the PCB and §5d (R24 within the
     Q87 allowance, everything else within 0.1 mm).
   - `scripts/board/route_v2.py --dsn-check` (or the lane's equivalent)
     shows the DSN classes at the §12 flex limits.
   - `arduino-cli compile --fqbn adafruit:nrf52:feather52840 --library
     firmware --output-dir <tmp> firmware/elicio_stream` exits 0; the
     `board_pins.h` map equals `board-v2.md` §9 after the merge (J1 and
     U5 are out: no USB pins claimed).
   - `scripts/sheets/template.py` twice byte-identical and equal to the
     committed PDF and SVGs; `elicio receive --simulate-live` and
     `receive-check` as their tests expect (WP13c's dropout rule).
   - `git diff main -- docs/fab/plan.md docs/fab/plan-v2.md
     docs/fab/open-questions.md docs/fab/interface.md docs/fab/contacts.md
     docs/fab/cad/v1/` is empty.
   - `git count-objects -vH` growth over `main` under 12 MB; report it.
4. Adversarial review: the seams below first, then the attack points.
   Build the shell and cut sections through the standoff pockets, the
   REF slot, the rib slot, the drop channel, the hook-end Ø5 floor holes
   and the medial-tail screw well before trusting any check; export the
   board from `kicad-cli` (SVG or Gerbers) and look at the flat outline,
   the strips, the ring lands, the charge tab and the J4 holes.
5. Fix every defect yourself, in separate commits on `review/r7` with
   messages starting `review(WPn):`. Do not run `git push`.
6. What cannot be fixed without changing plan v2 or a coordinator reading
   goes under "Needs a decision", numbered from 89.

## Seams

- **One packing truth, third time.** Three artefacts must carry the same
  numbers after the merge: packing §5d at `e4b857c` (pin table v2.1 in
  FLAT PCB coordinates, the folded-site table for the shell, the flat
  pattern: neck-end strips SIG1 10.71 / SIG2 21.81 at R 1.5 with arc
  4.71, REF straight through the end-wall slot, the charge tab through
  the rib slot s 14.90–15.70, u 11.90–20.50, h 0.31, two 90° bends at
  R 1.5 dropping 3.31, CHARGE rectangle centre (33.02, 4.30) 14.50 ×
  8.60, J4's three NPTH at (16.25, 27.14), (15.234, 22.06), (17.266,
  22.06)); the board at `fbd56e6` (`hardware/board/packing_v2_flat.md`,
  the Edge.Cuts flat outline, the footprints, R24 at +0.47 u rot 0 under
  Q87 while v2.1 says (18.49, 22.57) rot 90: reconcile within 0.1 mm,
  the board's copper being the truth, and note which one moves); the
  shell at `bdfc429` (`V2_BOSS_sites` / `V2_CHARGE_pads` parse the
  folded-site table at `408a476`, P4/P5 floor holes at (14.70, 4.30) and
  (17.70, 11.72), rib slot and drop channel). Where they differ the solid
  wins for the shell's sites and the copper for the board, or it is a
  decision.
- **The charging pads moved three times in WP11e** (side walls → off
  the body at s 49.50 → hook-end medial floor, Q86). Check the third
  pass's argument against the shell's real geometry (tail loft from
  s 45.5, REF dome Ø6.4 at (8.50, 43.00), concealed M2.5 well at (14.50,
  41.00), end-wall slot s 38.20–39.25): is "largest tail pair Ø2.1" right,
  and are the hook-end sites clear of the 501012 pocket (u 1.80–11.90,
  s 1.50–14.50) with the 0.30 the lane claims? Q86 offers Rolf Ø2.1 tail
  pads as the alternative; do not re-decide it, but say in the verdict
  whether a Ø3 or Ø4 pair would fit the tail, with numbers, so Rolf's
  choice is informed.
- **Q84 and Q88, the Contact rule.** Plan v2 §5.3 says 1.0 mm creepage
  for exposed copper and an insulation envelope around each contact
  net; board-v2 §12 draws a 7 × 7 other-net keep-out around each Ø5 land.
  Q84 moved the 1.0 mm off the island 0402s; WP12f showed the `tabs`
  area at 1.0 mm blocks every path from a strip onto the island; Q88
  shrinks the areas to the exposed lands plus 1.0 mm and lets the
  coverlaid strips carry one Contact trace at the class clearance 0.20.
  Read §5.3's words and rule in the verdict whether Q88 is faithful to
  them; if not, say what the rule must be (WP12g on lane w2 is routing
  under Q88 right now and will take your ruling in round 8). Also check
  variant A's claim "R1–R3 on the island at the tab root" against the
  actual sites (R1 (10.70, 20.12), R2 (17.87, 32.03), R3 (17.87, 30.03)):
  if they are not at the roots, the Contact runs across the island are
  long; say whether that matters under §5.3.
- **Routing is not yours.** Do not edit copper, vias, zones or rule
  areas in `hardware/board/elicio-v2.kicad_pcb`, nor
  `scripts/board/route_v2.py`, `hardware/board/route.md`, nor
  `board-v2.md` §15: lane w2 rewrites exactly those after `fbd56e6`
  (WP12g). Footprints' correctness, the schematic, the `.kicad_pro`
  netclasses, the `.kicad_dru` rules' logic (as a review finding, fixed
  in round 8 if it touches the copper), the BOM, `release.py` and its
  tests, and the docs outside §15 are yours to fix.
- **A brief's prescribed commit message became a false claim.** WP12d's
  last commit `1e055de` says "routed" on an un-routed tree (the brief
  prescribed the line); WP12e and WP12f corrected the habit. Record it;
  nothing to fix in the tree beyond the docs saying the true state.
- **Stamp versus HEAD.** WP14d's renders stamp the solids commit
  `f52afc5` while its HEAD `ecfff54` was a one-line read fix; WP14e
  rebuilt (`9734c34` stamped, HEAD `bdfc429`). Confirm the rule "stamp =
  manifest.commit = the commit whose tree built the solids" is what the
  test asserts and that it holds after your merge (a merge commit does
  not rebuild; say how the rule survives merges).
- **L8 §3 says Freerouting 2.4.1 runs on Java 21**; the jar is class
  file 69 and needs OpenJDK 25 (WP12d-prep measured it, WP12f ran it).
  Fix L8 §3 (docs, `lane/w5`'s file) and keep L8 §4's screw prices and
  the fixture fee as the lane tagged them (verify one page each if you
  can, else keep UNVERIFIED).
- **w2's venv fails 14 CAD tests** (`CadRegenTests` × 13,
  `CadShellV2BuildTests` × 1) that pass in w1's and (round 6) the
  reviewer's; the lane never installed `.[cad]`. Confirm on your venv
  that order 1 matches on the merged tree, and make the CAD tests skip
  by name when the extra is absent instead of failing (or document why
  they must fail).
- **J4's hole model.** WP11f parses the KiCad footprint with "canvas
  Y-down, positive rot CCW"; check that mapping against the PCB's actual
  hole coordinates for J4 at rot 90 and for one rotated 0402, so the
  packing cannot mirror another footprint later.
- **WP13c's dropout rule** against montage §8's table: the tool must
  match the table's "same criterion" column; ambiguity is a decision.
- **The vault and the sheets are not in this round**; `grep -rn
  "owner\|the user" docs/ tasks/WP1[1-7]*.md` must find nothing new.

## Attack points per package

- **WP14b–WP14e (shell)**: every V2_* check re-derived from your own
  cuts (standoff pockets = 3.0 + ring 0.31, boss drops 0.50 at the Q82
  sites, hinge lip undercut 1.0 with 0.30 nylon over it, screw
  engagement 4.30 in the tail boss, well concealed on the medial tail,
  lateral face with 0 pits, rim R 1.08, edge rise ≥ 0.025 at 7
  stations, walls 1.50 sides / 1.00 hinge, floor 1.50 around the Ø5
  holes, rib slot and drop channel air); the width-22 cavity 1.50–20.50
  against the island 2.25–19.75 and the process-edge rule; the tab
  channel lengths equal the flat pattern's folded runs (SIG1 6.00, SIG2
  17.10 after the 4.71 arc); `render.py` labels match the solid; no
  per-run files; Stage B v2 untouched; the medial well against the REF
  dome and skin (Q17, Q71) stated.
- **WP11c–WP11f (packing)**: the courtyard table equals the PCB's
  courtyards within 0.05 (the test); the process-edge reading (Q78) and
  its JLC source (WP17c §1) quoted; the width-20 failures are real
  (re-run one cell); `layout_conflicts` unchanged from round 5; the flat
  pattern's self-overlap check covers both sides and the CHARGE
  rectangle; `packing-v2.md` regenerated not edited; the J4 keep-out
  radius (drill/2 + 0.20 = 0.6953) equals KiCad's hole_clearance rule;
  the Q86 tail arithmetic.
- **WP12c–WP12f (board)**: schematic changes for the no-receptacle
  variant (J1, U5 out; D1 as VBUS TVS on the charge pads; nRF USB pins
  no-connect; the P-FET inhibit still driven; BQ25100 input from the
  pads; ERC 0 is not proof, read the nets); BOM 57 lines each
  LCSC-numbered with date and stock or UNVERIFIED; the flat outline's
  copper-to-edge 0.30 everywhere including the strips and the CHARGE
  rectangle; RING_PAD_D5_H2.7 footprint (pad, hole, mask, the 7 × 7
  keep-out) on P1–P5; nothing under the module keep-out; both-side
  height ≤ 3.31 for B.Cu parts; `.kicad_dru` rule-area logic; the DSN
  class check; `release.py`'s `routed` flag false on refusal; the
  Freerouting invocation reproducible (flags, jar, Java) and OpenJDK 25
  stated everywhere Java is named.
- **WP13c**: every montage §8 case through `receive-check` with an
  asserted outcome; exit code table in `receiver-v2.md`; no radio needed
  by the tests.
- **WP17c**: spot-check JLC's FPC panelisation page (process edge, 2.5
  mm to the rail), the double-sided FPC assembly statement and fixture
  fee, one titanium M2.5 screw page, the Freerouting release page (Java
  requirement); UNVERIFIED tags kept; no recommendation beyond the facts.

## Output

1. `tasks/reviews/code-r7.md`: a three-line verdict (MERGE /
   MERGE-AFTER-DECISION / REJECT), the gate results with commands and
   numbers (test count and skips per extra, hash identity, Stage B v2 and
   shell identity, packing doc identity, release summary, DSN classes,
   firmware build size, repo growth), a table of defects (severity,
   file:line, what was wrong, what you changed, commit hash), the §7 look
   judgement of the WP14e renders in prose, the Q88 ruling, and "Needs a
   decision" numbered from 89. Commit it on `review/r7`.
2. `.reports/review-r7-report.md` in this worktree: what you merged, what
   you changed, the final commit sha.
3. Then, in order:

       herdr pane report-metadata "$HERDR_PANE_ID" --source lane --token lane=review-r7 --token done=1
       herdr notification show "review r7 done" --body "reviewer rev7" --sound done
       herdr agent prompt elicio "DONE review-r7 .reports/review-r7-report.md <final commit sha>" || herdr agent prompt elicio "DONE review-r7 .reports/review-r7-report.md <final commit sha>"

Your turn must end with that push, including if the verdict is REJECT. If
you must stop for something outside yourself, push
`WAITING review-r7 <what>` instead. If you start a helper lane, close its
tab before you push.

## The worker reports, verbatim

### WP11c (lane w3)

````markdown
# WP11c report — real courtyards and layout v2 (round-6 rules 70–74)

Lane `w3`, branch `lane/w3`, package WP11c.
On top of `bcecc83`. Round 6 merges that commit only. These commits are round 7.
Plan for this package: `docs/fab/plan-v2.md`. Analysis only.
The plan was not edited. Order 1 was not touched. No order. No vendor contact.
Board files and the shell were not edited.

Python 3.13 venv in this worktree. Install: `.venv/bin/python -m pip install -e '.[cad]'`.

This report covers the first WP11c close and the coordinator amendment
(round 6 verdict `tasks/reviews/code-r6.md` decisions 70–74).

## What was built

`scripts/cad/placement_v2.py` reads every footprint from
`git show 845bac7:hardware/board/elicio-v2.kicad_pcb` (WP12b after the shorting
copper was dropped). The part table holds F.CrtYd, pad extent, and the round-5
packing size as a second column. Keep-out zones from that file are listed
(RF_NO_COPPER, RF_FEED_NOTCH, ring clears, J4 USB-C keep-out).
Contact netclass clearance is 1.0 mm (WP12b `elicio-v2.kicad_pro`, nets
SIG1/SIG2/REF).

`scripts/cad/placement.py --layout-v2` runs the search on the 501012 w20 × y8
body and on the 17.0 mm 501015 pack at +1.5 mm of arc.
`docs/fab/packing-v2.md` §5b was regenerated, not hand-edited.
The 864-run table, the Stage B winner row, and the round-5 tests were not
rewritten. No extra `placement_v2_*.svg` was added (Q56; 14 files remain).

The amendment adds layout rules 70, 72, 73 and 74 from `code-r6.md`.
Each rule is cited by decision number in §5b.

## Size differences (KiCad courtyard vs round 5)

| ref | courtyard | round-5 packing | Δw | Δh |
|---|---|---|---:|---:|
| U1 | 11.50 × 16.50 | 10.50 × 15.50 | +1.00 | +1.00 |
| U2 | 5.26 × 5.26 | 5.00 × 5.00 | +0.26 | +0.26 |
| U3 | 2.96 × 3.50 | 2.10 × 1.40 | +0.86 | +2.10 |
| U4 | 4.10 × 3.40 | 3.30 × 2.90 | +0.80 | +0.50 |
| U5 | 4.10 × 3.40 | 3.30 × 2.90 | +0.80 | +0.50 |
| SW1 | 7.50 × 5.60 | 4.50 × 4.50 | +3.00 | +1.10 |
| J1 | 10.64 × 9.42 | 8.90 × 7.30 | +1.74 | +2.12 |
| J2 | 5.80 × 6.56 | 4.00 × 6.00 | +1.80 | +0.56 |
| J3 | 12.31 × 8.62 | 7.60 × 2.50 | +4.71 | +6.12 |
| D1 | 2.50 × 1.40 | 2.20 × 1.00 | +0.30 | +0.40 |
| R1–R3 | 1.86 × 0.94 | 1.80 × 0.90 | +0.06 | +0.04 |
| J4 | 7.00 × 4.00 | (not packed) | — | — |

66 footprints. The test re-reads the KiCad file and fails if a courtyard disagrees by more than 0.05 mm.

## Rules the search must meet

| rule | source | 501012 w20 y8 | 17 mm pack +1.5 |
|---|---|---|---|
| JLC FPC assembly edge 2.5 mm | board-v2.md §12 / L6 | **no** (first) | no |
| copper-to-edge 0.30 | board-v2.md §12 | no (U1 pad 0.15) | no |
| courtyard-to-courtyard ≥ 0, mask margin 0.10 | DRC 0.05 × 2 | yes (placed parts) | yes (placed parts) |
| Contact netclass 1.0 mm | WP12b kicad_pro | no (0402 pad gap 0.48) | no |
| module keep-out empty | Raytac Spec K | yes | yes |
| J4 on hook-end with plug volume | plan v2 §5.4 | no (USB courtyard fills that face) | no |
| SW1 under lid recess | packing-v2.md §5 | no (HOLE_M1 takes that leftover site) | no |
| J3 and TC2030 reachable | WP11c brief | yes | no (J3 unplaced) |
| every WP12b footprint placed | WP11c brief | no | no |
| USB-C body inside outline | code-r6.md decision 70 | no | no |
| three FR4 0.2 ring pieces; ring 0.31 stays | code-r6.md decision 72 | yes | yes |
| two Ø2.7 boss-site holes, courtyard-clear | code-r6.md decision 73 | no (U1 covers 14.85, 28.10) | no |
| SIG1/SIG2 180° fold at R 1.5, shared numbers | code-r6.md decision 74 | yes (both variants numbered) | yes |
| M1 ≥ TOTAL_CHORD + 3 | Q34; 17 mm only if M1 ≥ 52.5 | (BODY_ARC, not applied) | **no** (first) |

Contact sites were not moved: SIG1 (5.90, 22.00), SIG2 (10.40, 33.10), REF (8.50, 43.00).
REF tab (8.50, 43.00) → (8.50, 36.80). `REF_end_wall_slot` stays cut.

## Round 6 decision 70 — USB-C body

The USB-C land on 845bac7 is J1 (`USB_C_Receptacle_HRO_TYPE-C-31-M-12`).
J4 is TC2030. The real body is the J1 courtyard 10.64 × 9.42 × 3.2
(height from packing `USB` / plan v2 §5.4; board-v2.md §12 is the stackup).

Packing hangs the receptacle 4.80 mm past the outer face s=−1.00.
The courtyard hangs 5.86 mm (J1 s0=−6.86).
The hook root occupies u up to 6.39 on that face.
The opening starts at u=5.50 (overlap 0.89 mm).
A 2.4 mm posterior hook-root move clears the opening and the 1.5 mm ligament.
It does not pull the body inside the outline.

A longer body that seats the body behind the face needs +7.32 mm of arc
with the cell moved back. Chord 55.29. M1 ≥ 58.29 against default.toml M1=52.

**What closes it: nothing.**

## Round 6 decision 72 — ring stiffeners

Three FR4 0.2 ring stiffener pieces exist on the tabs (SIG1, SIG2, REF).
Ring stack 0.31 stays (PI 0.11 + FR4 0.2).
Island Eco1 still has 2 pieces of FR4 0.4.
FR4 piece count 5 (JLC extra-fee threshold 4).

## Round 6 decision 73 — island mounting holes

Two holes in the island at the shell boss sites:
(14.85, 21.50) and (14.85, 28.10), Ø2.7, courtyard keep 3.30 mm.
HOLE_M1 and HOLE_M2 are reserved on leftover.
U1's courtyard covers (14.85, 28.10).
HOLE_M1 takes the leftover SW1 site, so SW1 is not placed.

## Round 6 decision 74 — SIG1/SIG2 fold

180° fold at R 1.5 (arc 4.71 mm, stand-out 1.6 mm).
The same number is used for the PCB, the packing table and the shell.

| pack | variant | SIG1 strip | SIG2 strip | pocket |
|---|---|---:|---:|---|
| 501012 BODY_ARC | neck-end | 10.71 | 21.81 | s 14.40–16.00, 3.50 × 3.00 (neck drop; no side-wall cut) |
| 501012 BODY_ARC | side-wall pockets | 8.36 | 12.06 | 0.85 deep × 3.50 along s × 3.00 along y; wall left 0.65 |
| 501015 +1.5 mm arc | neck-end | 6.71 | 17.81 | s 18.40–20.00, 3.50 × 3.00 (neck drop; no side-wall cut) |
| 501015 +1.5 mm arc | side-wall pockets | 8.36 | 12.06 | 0.85 deep × 3.50 along s × 3.00 along y; wall left 0.65 |

## The two layouts

**501012 pack, w20 × y8, interface II, standoff 3 (the shell as built).**
TOTAL_CHORD 47.90. Island u 2.25–17.75, s 16.00–37.60.
**First rule that cannot be met:** JLC FPC assembly edge 2.5 mm.
U1 at the packing pose (long along u) sits 0.00 mm from the island edge.
Turning U1 long-along-s needs a 15.5 × 20.5 island; this island is 15.50 × 21.60,
so U1 can meet 2.5 mm on the short sides only if nothing else shares that 10.5 mm
strip. U2 courtyard 5.26 cannot sit beside U1 under that rule.

U2 sits on the pocket island. J1 hangs on the hook-end. J2 hangs off the
pocket high-u wall. J3 hangs off the high-u outline. SW1 is not placed
(decision 73 HOLE_M1).

**501015 pack 17.0 × 10.0 × 5.0 at +1.5 mm of arc.**
TOTAL_CHORD 49.42. Need M1 ≥ 52.42. default.toml M1 = 52.
**First rule that cannot be met:** M1 ≥ TOTAL_CHORD + 3 (valid only if M1 ≥ 52.5).

## Contact 1.0 mm on a 2.5 mm tab

An 0402 across a Contact net has pad gap 0.48 mm. That cannot hold 1.0 mm
(SIG1–AFE_IN1P, SIG2–AFE_IN1N, REF–RLD_FB).

- Variant A: R1/R2/R3 on the island at the tab root; each tab carries one Contact trace.
- Variant B: widen each tab to 4.0 mm. The 0402 pad gap 0.48 mm still violates
  Contact-to-Default 1.0 mm; that needs a larger package or a DRC exception.

The reviewer and the board lane pick.

## Plan §9 acceptance

This package has no row of its own in plan §9. The software gate was run:

```text
.venv/bin/python -m unittest discover -s tests -v
```

191 tests. Result: OK.

`packing-v2.md` regenerated with `scripts/cad/placement.py --packing-doc`.
Byte-identical to a fresh `packing_markdown` of the 864-run matrix.
14 `placement_v2_*.svg` files (the round-5 kept set). Order 1 untouched.

## What was not done

No plan edit. No order. No board edit. No shell edit. No new v1 drawings.
No layout that meets every rule on this shell: JLC 2.5 mm cannot hold U1 and U2
on the 15.5 mm island. Decision 70 does not close the USB-C body inside the
outline. Decision 73 does not clear U1 from the high-s boss hole.

## Needs a decision

1. JLC FPC assembly edge 2.5 mm vs a 15.5 mm island that already holds U1 at
   15.5 mm along u. A waiver, a wider island, or U1 off the leftover (module
   only) is required before WP12d can meet that rule.
2. Contact netclass 1.0 mm: variant A (0402 on the island, one trace on the
   2.5 mm tab) or variant B (4.0 mm tab) plus a larger package or a DRC
   exception for the 0.48 mm pad gap.
3. 17 mm 501015 pack at +1.5 mm: raise M1 to ≥ 52.5 or drop that pack.
4. J4 cannot share the hook-end with USB-C (courtyard 10.64 × 9.42). Place J4
   on leftover (as in this table) or move USB.
5. Decision 70: USB-C inside the outline does not close on this M1=52 shell
   (`code-r6.md` decision 70). Longer body needs M1 ≥ 58.29. Hook-root shift
   2.4 mm clears the opening only.
6. Decision 73: U1 covers (14.85, 28.10). Move U1, move the boss, or drop
   that hole. HOLE_M1 also removes the leftover SW1 site.
7. Decision 74: neck-end vs side-wall pockets. Side-wall remaining wall is
   0.65 mm (under 1.0 mm). The reviewer, the board lane and the shell pick
   one pair of strip lengths from the table.

## Final commit

`5f864bf` `packing(v2c): apply round-6 layout rules 70-74`
Parent: `1897df0` `packing(v2c): real courtyards, layout v2 for the board`.
Round 6 reviewer merges `bcecc83` only.
````

### WP11d (lane w3)

````markdown
# WP11d report — layout grid v2c (Q78–Q83)

Lane `w3`, branch `lane/w3`, package WP11d.
First merge of `main`: `57c03ad` (Q78–Q80).
Addendum merge of `main`: `037c4c4` `merge main: Q81-Q83 onto lane/w3 for WP11d addendum`.
Third addendum merge: `0b5c838` `merge main: Q81 settled no-receptacle onto lane/w3 for WP11d addendum`.
Plan for this package: `docs/fab/plan-v2.md`. Analysis only.
The plan was not edited. Order 1 was not touched. No order. No vendor contact.
Board files, the shell, and `docs/fab/open-questions.md` were not edited.

Python 3.13 venv in this worktree. Install: `.venv/bin/python -m pip install -e '.[cad]'`.

## What was built

`scripts/cad/layout_v2c.py` searches a 32-cell grid on the 501012 pack only (Q69).
16 cells keep J1 and U5 (BOM 66). 16 cells drop them (Q81, BOM 64) and put two
charging contact pads on the tail end. Fixed: Contact variant A (Q79), J4
TC2030 on the leftover (Q80), three FR4 0.2 ring pieces (Q72), two Ø2.7
island holes where courtyards allow with keep 3.30 (Q82), neck-end fold
unless remaining wall ≥ 1.0 (Q83), SW1 under the lid, module keep-out empty,
copper-to-edge 0.30, courtyard-to-courtyard ≥ 0 with 0.10 mask.

Vary: process-edge vs body-to-outline 2.5 mm; width 20 and 22; TOTAL_CHORD
47.90 vs 49.00; one-sided vs two-sided; receptacle present vs absent.

`--layout-v2c` on `scripts/cad/placement.py` writes `docs/fab/packing-v2.md`
§5c and at most four drawings in `docs/fab/cad/v2c/`.

## Second addendum — WP12d pin table that meets every rule

The pin table WP12d takes must pass every rule it is checked against.
The placer now keeps pad-to-outline ≥ 0.30 on the island and on the
pocket. D1, C3, C10, C11 and C12 sit inward. The two Ø2.7 holes stay at
the Q82 sites (13.45, 17.70) and (17.95, 17.70), keep 3.30, not under U1.
SW1 stays in the lid recess.

Smallest all-66 with receptacle: process-edge, width 22, chord 47.90,
two sides, fold neck, 66/66, first rule "—". That is the WP12d pin table
in §5c, with the side column.

No no-receptacle cell at width 20 places the full BOM under every rule
(process 20, 47.90, two: 52/64; J4 does not place).

## Third addendum — no-receptacle pin table the build carries (Q81)

Q81 is settled: the build carries no receptacle. §5c now has a second pin
table, same format and rules as the USB table (side column, pad-to-outline
≥ 0.30, Q82 holes, SW1 in the lid recess, Contact A).

Smallest all-64 with no receptacle: process-edge, width 22, chord 47.90,
two sides, fold neck, 64/64, first rule "—". J1 and U5 are absent.

| item | value |
|---|---|
| holes (Q82) | (13.45, 17.70); (17.95, 17.70) |
| SIG1 strip (Q83) | 10.71 mm |
| SIG2 strip (Q83) | 21.81 mm |
| P4 CHARGE_VBUS | floor, (0.75, 44.00), RING_PAD_D5_H2.7 courtyard 6.40 × 6.40 |
| P5 CHARGE_GND | floor, (21.25, 44.00), RING_PAD_D5_H2.7 courtyard 6.40 × 6.40 |

Drawing `docs/fab/cad/v2c/placement_v2c_process_norec_w22_c47.90_two.svg`
was regenerated. Geometry matches the committed file.

Named centres on the USB width-22 table:

| ref | side | u | s | rot |
|---|---|---:|---:|---:|
| D1 | top | 3.95 | 16.75 | 0 |
| C3 | top | 19.06 | 32.01 | 90 |
| C10 | top | 17.41 | 13.71 | 0 |
| C11 | top | 18.56 | 8.56 | 90 |
| C12 | top | 18.56 | 10.56 | 90 |

## Q81 — grow the body to M1 58.3, or drop the receptacle

M1 58.3 is the USB-inside length (Q70). It is not a closer for 66 footprints
on width 20. Dropping J1 and U5 also does not close width 20 two-sided.

| cell | USB (66) | no receptacle (64) |
|---|---|---|
| process, 20, 47.90, two | 53/66 | 52/64 |
| process, 22, 47.90, two | 66/66 | 64/64 |
| body 2.5 mm, 22, 47.90, two | 32/66 | 31/64 |

Width 20 two-sided with no receptacle still has J4 unplaced.
The first rule that cannot be met is copper-to-edge 0.30 (board-v2.md §12).
The USB-C receptacle is not that first fail. Growing the body to M1 58.3
does not change width 20 island area. Closing 66 or 64 under every rule
needs width 22.

No-receptacle cells have no J1 and no U5. Two `RING_PAD` parts P4 and P5
sit on the tail at (0.75, 44.0) and (width−0.75, 44.0).

## Q82 — hole sites the shell can follow

Holes are reserved after SW1, before J4 and the passives. RING_* boxes are
not hole blockers. SW1 keeps the lid-recess leftover site. If SW1 sits on
the leftover, the two Ø2.7 holes prefer the island.

Process-edge width 22, chord 47.90, two sides (the closer, USB or no USB):

- (13.45, 17.70)
- (17.95, 17.70)

WP14d can move the bosses to those sites. Keep from courtyard is 3.30.

## Q83 — neck-end fold is the default

`wall_left = WALL(1.5) − (FOLD_STAND_OUT 1.6 − SIDE_CLEAR 0.75) = 0.65` mm
at width 20 and at width 22. The extra 2 mm at width 22 is island, not wall.
Every cell in this grid uses neck-end strips. No cell uses side-wall pockets.

## 16 cells with USB-C receptacle (BOM 66)

| edge | width | chord | sides | fold | placed / N | first rule that cannot be met | island mm² | leftover mm² | holes | extra u | extra s | second side |
|---|---:|---:|---|---|---:|---|---:|---:|---|---:|---:|---|
| process | 20 | 47.90 | top | neck | 28/66 | J4 TC2030 on the leftover (Q80) | 334.8 | 74.7 | (13.45, 17.70); (15.40, 21.65) | +0.00 | +0.00 | — |
| process | 20 | 47.90 | two | neck | 53/66 | J4 TC2030 on the leftover (Q80) | 334.8 | 74.7 | (13.45, 17.70); (15.40, 21.65) | +0.00 | +0.00 | U2, Q1, Q2, Q3, Q4, C7, C8, C9, C15, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19 |
| process | 20 | 49.00 | top | neck | 19/66 | J4 TC2030 on the leftover (Q80) | 351.7 | 91.5 | (15.45, 23.84); (15.45, 28.34) | +0.00 | +1.09 | — |
| process | 20 | 49.00 | two | neck | 52/66 | J4 TC2030 on the leftover (Q80) | 351.7 | 91.5 | (15.45, 23.84); (15.45, 28.34) | +0.00 | +1.09 | Q1, Q2, Q3, Q4, Q5, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13, C14, C15, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17 |
| process | 22 | 47.90 | top | neck | 26/66 | every required footprint placed | 378.0 | 84.4 | (13.45, 17.70); (17.95, 17.70) | +2.00 | +0.00 | — |
| process | 22 | 47.90 | two | neck | 66/66 | — | 378.0 | 84.4 | (13.45, 17.70); (17.95, 17.70) | +2.00 | +0.00 | U5, Q1, Q2, Q3, Q4, Q5, C6, C7, C8, C9, C13, C14, C15, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30 |
| process | 22 | 49.00 | top | neck | 29/66 | every required footprint placed | 397.0 | 103.3 | (15.45, 23.84); (15.45, 28.34) | +2.00 | +1.09 | — |
| process | 22 | 49.00 | two | neck | 66/66 | — | 397.0 | 103.3 | (15.45, 23.84); (15.45, 28.34) | +2.00 | +1.09 | Q1, Q2, Q3, Q4, Q5, C8, C9, C13, C14, C15, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30 |
| body | 20 | 47.90 | top | neck | 14/66 | J4 TC2030 on the leftover (Q80) | 334.8 | 43.9 | — | +0.00 | +0.00 | — |
| body | 20 | 47.90 | two | neck | 25/66 | J4 TC2030 on the leftover (Q80) | 334.8 | 43.9 | — | +0.00 | +0.00 | U2, U3, U4, D1, L1, C4, C5, C6, C10, C11, C12 |
| body | 20 | 49.00 | top | neck | 14/66 | J4 TC2030 on the leftover (Q80) | 351.7 | 60.7 | (13.40, 17.65) | +0.00 | +1.09 | — |
| body | 20 | 49.00 | two | neck | 24/66 | J4 TC2030 on the leftover (Q80) | 351.7 | 60.7 | (13.40, 17.65) | +0.00 | +1.09 | U2, U3, U4, D1, L1, C4, C5, C10, C11, C12 |
| body | 22 | 47.90 | top | neck | 14/66 | J4 TC2030 on the leftover (Q80) | 378.0 | 49.6 | — | +2.00 | +0.00 | — |
| body | 22 | 47.90 | two | neck | 32/66 | J4 TC2030 on the leftover (Q80) | 378.0 | 49.6 | — | +2.00 | +0.00 | U2, U4, U5, Q1, C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13, C14 |
| body | 22 | 49.00 | top | neck | 14/66 | J4 TC2030 on the leftover (Q80) | 397.0 | 68.5 | (13.40, 17.65); (17.90, 17.65) | +2.00 | +1.09 | — |
| body | 22 | 49.00 | two | neck | 32/66 | J4 TC2030 on the leftover (Q80) | 397.0 | 68.5 | (13.40, 17.65); (17.90, 17.65) | +2.00 | +1.09 | U2, U4, U5, Q1, C1, C2, C3, C4, C5, C6, C7, C8, C10, C11, C12, C13, C14, R4 |

## 16 cells with no receptacle (BOM 64)

| edge | width | chord | sides | fold | placed / N | first rule that cannot be met | island mm² | leftover mm² | holes | extra u | extra s | second side |
|---|---:|---:|---|---|---:|---|---:|---:|---|---:|---:|---|
| process | 20 | 47.90 | top | neck | 26/64 | J4 TC2030 on the leftover (Q80) | 334.8 | 74.7 | (13.45, 17.70); (15.40, 21.65) | +0.00 | +0.00 | — |
| process | 20 | 47.90 | two | neck | 52/64 | J4 TC2030 on the leftover (Q80) | 334.8 | 74.7 | (13.45, 17.70); (15.40, 21.65) | +0.00 | +0.00 | U2, Q2, Q3, Q4, Q5, C8, C9, C13, C14, C15, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19 |
| process | 20 | 49.00 | top | neck | 23/64 | J4 TC2030 on the leftover (Q80) | 351.7 | 91.5 | (15.45, 23.84); (15.45, 28.34) | +0.00 | +1.09 | — |
| process | 20 | 49.00 | two | neck | 56/64 | J4 TC2030 on the leftover (Q80) | 351.7 | 91.5 | (15.45, 23.84); (15.45, 28.34) | +0.00 | +1.09 | Q1, Q2, Q3, Q4, Q5, C6, C7, C8, C9, C12, C13, C14, C15, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23 |
| process | 22 | 47.90 | top | neck | 25/64 | every required footprint placed | 378.0 | 84.4 | (13.45, 17.70); (17.95, 17.70) | +2.00 | +0.00 | — |
| process | 22 | 47.90 | two | neck | 64/64 | — | 378.0 | 84.4 | (13.45, 17.70); (17.95, 17.70) | +2.00 | +0.00 | Q1, Q2, Q3, Q4, Q5, C6, C7, C8, C9, C13, C14, C15, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30 |
| process | 22 | 49.00 | top | neck | 29/64 | every required footprint placed | 397.0 | 103.3 | (15.45, 23.84); (15.45, 28.34) | +2.00 | +1.09 | — |
| process | 22 | 49.00 | two | neck | 64/64 | — | 397.0 | 103.3 | (15.45, 23.84); (15.45, 28.34) | +2.00 | +1.09 | Q2, Q3, Q4, Q5, C8, C9, C13, C14, C15, R4, R5, R6, R7, R8, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30 |
| body | 20 | 47.90 | top | neck | 13/64 | J4 TC2030 on the leftover (Q80) | 334.8 | 43.9 | — | +0.00 | +0.00 | — |
| body | 20 | 47.90 | two | neck | 24/64 | J4 TC2030 on the leftover (Q80) | 334.8 | 43.9 | — | +0.00 | +0.00 | U2, U3, U4, D1, L1, C4, C5, C6, C10, C11, C12 |
| body | 20 | 49.00 | top | neck | 13/64 | J4 TC2030 on the leftover (Q80) | 351.7 | 60.7 | (13.40, 17.65) | +0.00 | +1.09 | — |
| body | 20 | 49.00 | two | neck | 23/64 | J4 TC2030 on the leftover (Q80) | 351.7 | 60.7 | (13.40, 17.65) | +0.00 | +1.09 | U2, U3, U4, D1, L1, C4, C5, C10, C11, C12 |
| body | 22 | 47.90 | top | neck | 13/64 | J4 TC2030 on the leftover (Q80) | 378.0 | 49.6 | — | +2.00 | +0.00 | — |
| body | 22 | 47.90 | two | neck | 31/64 | J4 TC2030 on the leftover (Q80) | 378.0 | 49.6 | — | +2.00 | +0.00 | U2, U4, Q1, Q2, C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13, C14 |
| body | 22 | 49.00 | top | neck | 13/64 | J4 TC2030 on the leftover (Q80) | 397.0 | 68.5 | (13.40, 17.65); (17.90, 17.65) | +2.00 | +1.09 | — |
| body | 22 | 49.00 | two | neck | 31/64 | J4 TC2030 on the leftover (Q80) | 397.0 | 68.5 | (13.40, 17.65); (17.90, 17.65) | +2.00 | +1.09 | U2, U4, Q1, Q2, C1, C2, C3, C4, C5, C6, C7, C8, C10, C11, C12, C13, C14, R4 |

## Geometry that does not vary with the receptacle

Island (process-edge, leftover 3.9 mm, Q80):

| width | chord | island u×s | leftover mm² | extra u | extra s |
|---|---|---|---|---|---|
| 20 | 47.90 | 17.50 × 21.60 = 334.8 | 74.7 | +0.00 | +0.00 |
| 20 | 49.00 | 17.50 × 22.69 = 351.7 | 91.5 | +0.00 | +1.09 |
| 22 | 47.90 | 19.50 × 21.60 = 378.0 | 84.4 | +2.00 | +0.00 |
| 22 | 49.00 | 19.50 × 22.69 = 397.0 | 103.3 | +2.00 | +1.09 |

Body-to-outline 2.5 mm shrinks leftover to 43.9 / 60.7 / 49.6 / 68.5 mm².
J4 6.0×16.0 does not fit that leftover. First fail on every body-edge cell
is `J4 TC2030 on the leftover (Q80)`.

Under-board air on 501012: 3.31 mm. Second-side parts need body height ≤ 3.31 mm.
V2C_ARC_PLUS_M1 at chord 49.00 is 1.0883 mm. Box is frozen with slots.

## Drawings (four, `docs/fab/cad/v2c/`)

- `placement_v2c_process_usb_w22_c47.90_two.svg` — 66/66
- `placement_v2c_process_norec_w22_c47.90_two.svg` — 64/64
- `placement_v2c_body_usb_w22_c47.90_two.svg` — 32/66
- `placement_v2c_body_norec_w22_c47.90_two.svg` — 31/64

`docs/fab/cad/v1/` still has the 14 `placement_v2_*.svg` files from WP11c.

## Tests

`.venv/bin/python -m unittest discover -s tests -v`

`Ran 222 tests in 200.223s OK`

`PlacementWP11dTests` covers 32 cells, Q81 skip of J1/U5 plus P4/P5,
Q83 neck-end on every cell, winning process-edge USB overlaps, regions,
Contact A, copper-to-edge ≥ 0.30 on both pin tables, hole keep versus
U1, SW1 and the bottom edge, and the no-receptacle cell (P4/P5 RING_PAD
courtyards, Q82 sites, SIG1/SIG2 strip lengths).

## Commits (do not push; the hook still pushes)

- `57c03ad` merge main: round 7 onto lane/w3 for WP11d
- `d4d2e6f` packing(v2c): search the 16-cell layout grid under both edge readings
- `e2a0e01` packing(v2c): layout grid, edge rule both ways, two sides
- `037c4c4` merge main: Q81-Q83 onto lane/w3 for WP11d addendum
- `6c945e1` packing(v2c): Q81 no-receptacle cells, Q82 courtyard holes, Q83 neck-end fold
- `e1f1d6f` packing(v2c): publish §5c for Q81-Q83
- `eebe871` packing(v2c): pin table meets copper-to-edge; holes not under U1
- `ae19850` packing(v2c): publish the WP12d pin table that meets every rule
- `0b5c838` merge main: Q81 settled no-receptacle onto lane/w3 for WP11d addendum
- `e1ebea7` packing(v2c): publish the Q81 no-receptacle pin table WP12d takes
- `c6bd2fe` packing(v2c): §5c second pin table for the no-receptacle cell

Tip: `c6bd2fe`. `git status --short` is empty.

## What this does not decide

WP12d does not get a pin table from width 20. Body-to-outline 2.5 mm
does not place J4. Width 20 no-receptacle does not place J4 either.
The board lane pins both width-22 tables. The build carries the
no-receptacle table (Q81). The shell lane moves bosses to the Q82 sites.
````

### WP11e (lane w3)

````markdown
# WP11e report — flat pattern, pin table v2, J4 NPTH keep-out (lane w3)

Lane `w3`, branch `lane/w3`, package WP11e.
Merge of `main`: `c88eaf9` (HANDOFF only). Earlier merge `a1fe352` brought
the WP11e brief and Q84/Q85.
Plan for this package: `docs/fab/plan-v2.md`. Analysis only.
The plan was not edited. Order 1 was not touched. No order. No vendor contact.
Board files, the shell, and `docs/fab/open-questions.md` were not edited.

Python 3.13 venv in this worktree.

## What was built

`docs/fab/packing-v2.md` §5d publishes the flat pattern for the build cell
(process-edge, width 22, chord 47.90, two sides, fold neck, no receptacle).

WP12d pinned §5c literally. P2 at the folded site (10.40, 33.10) sits inside
U1's courtyard. A flex board is drawn flat. Pin table v2 gives PCB coordinates.
The shell keeps a separate folded-site table.

### Flat pattern

| item | value |
|---|---|
| exit | neck-end (Q83). Side-wall pockets stay refused (wall 0.65 mm). |
| fold | 180° at inner R 1.5 mm, stack 0.31 mm (PI 0.11 + FR4 0.2) |
| arc | πR = 4.71 mm (Q83). Midplane π(R + t/2) = 5.20 mm is not used for L_flat. |
| SIG1 | attach (5.90, 16.00); flat ring (5.90, 5.29); L_flat 10.71 mm; folded run 6.00 mm |
| SIG2 | attach (10.40, 16.00); flat ring (10.40, −5.81); L_flat 21.81 mm; folded run 17.10 mm |
| REF | attach (8.50, 37.60); flat ring (8.50, 43.00); along the floor through the end-wall slot; no 180° fold |
| P4 / P5 | (14.70, 4.30) and (17.70, 11.72); hook-end medial floor; flat = folded |
| 2D check | no self-overlap; no strip crosses a leftover or pocket part; P1–P3 flat centres outside every other courtyard |

Mapping: each SIG strip leaves the island neck toward −s. After the 180° fold
the ring sits on the floor at the contact site.

Drawing: `docs/fab/cad/v2c/placement_v2c_process_norec_w22_c47.90_two.svg`
(four drawings in `docs/fab/cad/v2c/`, Q56).

### Pin table v2

68 rows (66 footprints including P4/P5, plus H1 and H2). Side column. Pad-to-outline
≥ 0.30. Q82 holes (13.45, 17.70) and (17.95, 17.70). SW1 in the lid recess.
Contact variant A. P1 and P2 are flat centres, not the folded sites.

### Folded sites for the shell (u, s, y)

| pad | net | u | s | y |
|---|---|---:|---:|---:|
| P1 | SIG1 | 5.90 | 22.00 | 1.50 |
| P2 | SIG2 | 10.40 | 33.10 | 1.50 |
| P3 | REF | 8.50 | 43.00 | 1.50 |
| P4 | CHARGE_VBUS | 14.70 | 4.30 | 1.50 |
| P5 | CHARGE_GND | 17.70 | 11.72 | 1.50 |

y is the ring seat on the inner floor.

### J4 NPTH keep-out (Q85)

KiCad footprint `Tag-Connect_TC2030-IDC-NL` has three NPTH, drill 0.9906 mm.
`elicio-v2.kicad_pro` min_hole_clearance 0.20 mm. Keep diameter 1.39 mm.
No B.Cu part in that zone on the no-receptacle cell. Same-face courtyard
keep-out on F.Cu stands.

| hole | u | s |
|---|---:|---:|
| J4-NPTH1 | 16.25 | 22.06 |
| J4-NPTH2 | 17.27 | 27.14 |
| J4-NPTH3 | 15.23 | 27.14 |

## Addendum 1 — P4/P5 off the side walls (superseded)

§5c had P4 at (0.75, 44.00) and P5 at (21.25, 44.00) in the 1.5 mm walls.
Addendum 1 moved them to (5.05, 49.50) and (16.95, 49.50). Those sites are
off the body (TOTAL_CHORD 47.90, loft s 45.5, Ø5 copper to s 52.0). Do not
use them.

## Addendum 2 — hook-end medial floor

Two Ø5 pads cannot sit on the tail with the rules in this pass.

Tail window: copper after `REF_end_wall_slot` (s ≥ 39.25 + r) and ahead of
the loft (s + r ≤ 45.5). For Ø5, s ∈ [41.75, 43.00]. Edge-to-edge ≥ 2.0 to
the REF Ø6.4 dome (8.50, 43.00) needs centre distance ≥ 7.7 mm. Edge-to-edge
≥ 2.0 to the Ø5 screw head (14.50, 41.00) needs centre distance ≥ 7.0 mm.
Cavity u with pad-to-outline 0.30 is u ∈ [4.30, 17.70]. That set is empty
for one Ø5 pad, so it is empty for a pair. Largest pair that fits on that
tail is Ø2.1.

Hook-end sites (width 22), beside the 501012 cell (u 1.80–11.90, s 1.50–14.50):

| pad | net | folded (u, s, y) |
|---|---|---|
| P4 | CHARGE_VBUS | (14.70, 4.30, 1.50) |
| P5 | CHARGE_GND | (17.70, 11.72, 1.50) |

Checks that pass:

- cavity u 1.50–20.50; Ø5 copper inside the cavity
- pad-to-outline ≥ 0.30 vs the hook-end lobe and vs the cavity
- whole Ø5 copper ahead of loft 45.5 (P4 copper to s 6.80; P5 copper to s 14.22)
- copper not in `REF_end_wall_slot` s 38.20–39.25
- nylon between pads ≥ 3.0 mm (copper edge-to-edge)
- REF dome edge-to-edge ≥ 2.0 mm
- screw head edge-to-edge ≥ 2.0 mm
- no courtyard overlap with P3
- cell still 64/64, every rule met

Extra channel for the shell: Ø5 holes through the medial floor at these
sites. `REF_end_wall_slot` is unchanged. The pocket island already sits
there (SW1, U2). If that island cannot carry the rings, the shell also
needs a rib slot at s 14.90–15.70, u 11.90–20.50, height 0.31, for a
floor tab from leftover s 16.

Shell lane: stop using (0.75, 44.00), (21.25, 44.00), (5.05, 49.50), and
(16.95, 49.50). Follow the §5d folded table. P1–P3 are unchanged.

The cell is marked in §5d and in the rule
`P4/P5 on the hook-end medial floor (Q81)`: tail Ø5 impossible, max tail
pair Ø2.1.

## Addendum 3 — P4/P5 flat path (Q85 on the Q86 sites)

The hook-end folded sites stand: P4 (14.70, 4.30), P5 (17.70, 11.72),
y 1.50. They share XY with SW1 (16.25, 4.45) and U2 (15.13, 10.28) on the
pocket island. Those parts sit at board height. The pads sit on the floor.
A flex board is drawn flat, so flat = folded is refused.

Fold picked: leftover s=16.00 through the rib slot (s 14.90–15.70,
u 11.90–20.50, height 0.31). The cell-side drop at u 11.90 is refused
because SIG2's flat strip occupies u 9.15–11.65 through that s.

| item | value |
|---|---|
| drop height | 3.31 mm (underside 4.81 to floor 1.50) |
| bend | two 90° at inner R 1.5 mm |
| allowance | πR + 0.31 vertical = 5.02 mm, plus 1.00 mm past J2 |
| flat map | 90° at leftover corner: 3D −s → +u |
| P4 flat | (37.47, 2.80) |
| P5 flat | (30.05, 5.80) |
| CHARGE rectangle | centre (33.02, 4.30), 14.50 × 8.60 |

2D check: no self-overlap. No pad or strip over a courtyard on either
side. Cell still 64/64.

Shell extras (folded sites stay in the shell table):

- Ø5 floor holes at (14.70, 4.30) and (17.70, 11.72)
- rib slot s 14.90–15.70, u 11.90–20.50, height 0.31
- drop channel at leftover s=16.00, u 11.90–20.50, two 90° at R 1.5,
  drop 3.31 mm, vertical 0.31 mm

Pin table v2 P4/P5 rows are the flat centres with `FLAT PCB (Q85)`.

## Gates

`.venv/bin/python -m unittest discover -s tests -v`

`Ran 231 tests in 193.250s OK`

`scripts/cad/placement.py --packing-doc` twice: `docs/fab/packing-v2.md` is
byte-identical. Drawings = 4. Order 1 not touched. `git status --short` empty
after the last commit (the report file is untracked).

Plan §9 acceptance for this packing slice: the pin table the board pins is
flat; the shell table equals §5 contact sites for P1–P3 and the hook-end
P4/P5 sites; P4/P5 flat centres are distinct from those folded sites; J4
holes are a both-side keep-out. Verified by `PlacementWP11eTests`
(including `test_floor_pad_sharing_xy_with_top_has_distinct_flat_centre`)
and the regenerated §5d.

## What was not done

USB-C cells do not get the both-side J4 NPTH keep-out in the search. That
variant is not the build (Q81). Applying it there left R28–R30 unplaced.
The no-receptacle cell is the one WP12e pins.

Q84 (Contact rule by area) is the board lane.

The shell solids were not edited. WP14 must keep the hook-end Ø5 holes,
add the rib slot, and add the drop channel named above.

Nothing was ordered.

## Needs a decision

None that blocks WP12e. The KiCad TC2030 footprint has three NPTH, not two.
The keep-out uses all three from the file.

## Commits (do not push; the hook still pushes)

- `c88eaf9` Merge remote-tracking branch `origin/main` into `lane/w3`
- `5dc642c` packing(v2e): flat pattern in PCB coordinates and J4 NPTH keep-out
- `723e74c` packing(v2e): flat pattern, tab pads in PCB coordinates, J4 keep-out both sides, pin table v2
- `bf9f3f6` packing(v2e): move P4/P5 onto the flex tail inside the cavity
- `303be75` packing(v2e): move P4/P5 to the hook-end medial floor
- `c53ddd6` Merge remote-tracking branch `origin/main` into `lane/w3` (Q86)
- `408a476` packing(v2e): give P4/P5 Q85 flat centres through the rib-slot fold

Tip: `408a476`. `git status --short` is empty except this report.
````

### WP11f (lane w3)

````markdown
# WP11f report — J4 hole sites from KiCad, pin table v2.1 (lane w3)

Lane `w3`, branch `lane/w3`, package WP11f.
Merge of `main`: `f514b14` (HANDOFF, Q87, WP11f brief).
Plan for this package: `docs/fab/plan-v2.md`. Analysis only.
The plan was not edited. Order 1 was not touched. No order. No vendor contact.
Board files, the shell, and `docs/fab/open-questions.md` were not edited.

Python 3.13 venv in this worktree.

## What was built

§5d J4 NPTH centres now come from the KiCad footprint
`Tag-Connect_TC2030-IDC-NL` in `git show 30ca79d:hardware/board/elicio-v2.kicad_pcb`.
Pad locals are parsed from that file. The world map uses KiCad canvas Y-down
(positive rot CCW on that canvas). At the pinned J4 (16.25, 24.60) rot 90
the three centres equal KiCad within 0.01:

| hole | u | s |
|---|---:|---:|
| J4-NPTH1 | 16.250 | 27.140 |
| J4-NPTH2 | 15.234 | 22.060 |
| J4-NPTH3 | 17.266 | 22.060 |

Pin table v2 had the pair and the single swapped along s
((16.25, 22.06), (17.27, 27.14), (15.23, 27.14)). That put R24 on a real hole.

Q85 keep-out on B.Cu is pad vs the circle of radius drill/2 + min_hole_clearance
(0.6953 mm). That matches KiCad hole_clearance. Courtyard vs a square keep
could not clear R24 and R26 without a large move or a copper-edge fail.

The no-receptacle build cell was re-run. The J4-side cluster was folded back
to pin table v2, then nudged by the smallest 0.01 mm step (both 0402 rotations)
that keeps pads out of the three holes and keeps copper-to-edge 0.30.

### Pin table v2.1

68 rows. Folded-site table unchanged. Flat P4/P5 unchanged.

| ref | pin table v2 | pin table v2.1 | delta |
|---|---|---|---|
| R23 | (18.28, 21.17) rot 0 | (18.32, 21.10) rot 0 | +0.04 u, −0.07 s |
| R24 | (18.28, 22.37) rot 0 | (18.49, 22.57) rot 90 | +0.21 u, +0.20 s |
| R26 | (14.22, 21.63) rot 90 | (14.21, 21.63) rot 90 | −0.01 u |

WP12e zero-track DRC (`route.md` §9 on `lane/w2`) asked R24 +0.46 u at rot 0.
`route.md` §10 was not on `lane/w2` at this pass. Packing cannot take +0.46 u
at rot 0: pad-to-outline falls below 0.30. Rot 90 plus a 0.29 mm step clears
the hole and the copper rule. Distance from the WP12e +0.46 site (18.74, 22.37)
to (18.49, 22.57) is 0.32 mm, past the 0.1 mm pin. Q87: the reviewer
reconciles within 0.1 mm; the board is copper truth.

WP12e also nudged R23 +0.09 u and R26 −0.05 u for the *wrong* hole pair.
Those nudges are not used. The real-hole moves are the rows above.

Drawing: `docs/fab/cad/v2c/placement_v2c_process_norec_w22_c47.90_two.svg`
(four drawings in `docs/fab/cad/v2c/`, Q56).

## Gates

`.venv/bin/python -m unittest discover -s tests -v`

`Ran 233 tests in 203.484s OK` (LC_ALL=C).

`scripts/cad/placement.py --packing-doc` twice: `docs/fab/packing-v2.md` is
byte-identical (`cksum 2573139946 281403`). Drawings = 4. Order 1 not touched.
`git status --short` empty after the last commit (the report file is untracked
and gitignored).

Plan §9 acceptance for this packing slice: J4 hole sites equal the KiCad
footprint at the pinned pose; pin table v2.1 has 68 rows; B.Cu pads stay out
of the three holes. Verified by `PlacementWP11fTests` and the regenerated §5d.

## What was not done

USB-C cells do not get the both-side J4 NPTH fold. That variant is not the
build (Q81). Applying the restore there broke courtyard rules on the USB cell.

The board was not edited. WP12f still owns R24 on copper and `route.md` §10.

The shell was not edited. Folded sites are unchanged.

Nothing was ordered.

## Needs a decision

R24: packing v2.1 is (18.49, 22.57) rot 90. WP12e's named copper move was
+0.46 u at rot 0. They differ by 0.32 mm and by rotation. Q87 says the board
is copper truth; the reviewer reconciles within 0.1 mm. No stop for this lane.

## Commits (do not push; the hook still pushes)

- `f514b14` Merge remote-tracking branch `origin/main` into `lane/w3` (Q87, WP11f)
- `e4b857c` packing(v2f): J4 hole sites from the KiCad footprint, pin table v2.1

Tip: `e4b857c`. `git status --short` is empty except this report.
````

### WP14b (lane w1)

````markdown
# WP14b report — shell v2b: screw closure, lofted lid, hook root

Lane `w1`, branch `lane/w1-r6`, package WP14b. Base `110a79b` (round 6
merge). `plan-v2.md` and `open-questions.md` were not edited. Order 1
files under `docs/fab/cad/v1/` were not written.

## What was built

Same construction path as Stage B v2. `STAGE=shell` now adds Q71, the
§7 lofted lid, and Q76. Overlay `scripts/cad/params/shell_v2.toml`.
Outputs `docs/fab/cad/v2/`. Record `docs/fab/shell-v2.md` §2, §4, §5.
Manifest `provisional: true`.

Captive hex wells, ring seats, Q59 slot, and the reviewer's measured
checks stay.

## Before / after (measured on the built solid)

| Check | Review r6 (main `110a79b`) | WP14b |
|---|---|---|
| `V2_CLOSURE` | fail. Snap undercut 0 / 0 / 0, beam 0.50, ε 0.135 | pass. Hinge undercut 1, lip in 1, engagement 4.00, boss wall 3.13, well air 1, head below boss top 1.75 |
| `V2_EDGE_radii` | fail. flat_stations 4, lid_rim_R 0.8 (constant) | pass. stations 6, flat_stations 0, min rise over 3 mm 0.030, lid_rim_R 1.08 (3-point fit) |
| `V2_USB_end` | fail. ligament_hook −0.89, mouth_recess −4.80 | NOT_MEASURED: waits for packing §5b, Q70; hook-end wall left solid |
| `V2_WALL_minima` | fail on the USB ligament | pass. hinge outer wall 1.00, side walls 1.50, slot floor 1.50, slot clear u 0.20 |
| Build exit | 3 (`V2_CLOSURE`, `V2_EDGE_radii`, `V2_USB_end`, `V2_WALL_minima`) | 0. USB row is NOT_MEASURED by name and does not fail the build |
| Q76 hook root | elliptical 4.4 × 3.0 from t=0; joint fillet left sharp | circular root r 1.75, then 4.4 × 3.0 / 3.0 × 2.2; joint fillet 1.5 applied (`notes.q76`) |

Renders (committed):

- `docs/fab/cad/v2/render_medial.png`
- `docs/fab/cad/v2/render_lateral.png`

## Gates

| Gate | Command | Result |
|---|---|---|
| Full suite | `.venv/bin/python -m unittest discover -s tests -v` | OK, 206 tests, 221.543 s, CAD tests ran |
| Order 1 byte-identical | `CadRegenTests.test_reference_regen_matches_committed_hashes` and `CadRenderTests.test_renders_and_drawing_regen_byte_identical` | both ok |
| Stage B v2 | `CadStageBV2BuildTests` vs `STAGE_B_V2_MEASURED`; two consecutive runs | ok. Q59 still fail on the unslotted Stage B path. File hashes identical run to run. Manifest not rewritten in `docs/fab/cad/v2/` (that folder is the shell) |
| Shell twice identical | `CadShellV2BuildTests.test_two_consecutive_shell_runs_are_identical` | ok, exit 0, `stage_b_failing: []`, solids equal to `docs/fab/cad/v2/` |
| Manifest bytes | `.venv/bin/python scripts/cad/manifest.py --check-bytes docs/fab/cad/v2/manifest.json` | schema 1 ok |
| git status | `git status --short` | empty at DONE (this report untracked) |

Plan §9 row 14 (shell v2 body, lid, closure and hook, §7 checks, Stage B
checks on the built solid, identical regeneration): the listed files
exist; §7 and Stage B rows are in the manifest and in `shell-v2.md`;
regeneration tested as above.

## What was not done

No order, quote, or upload. USB opening waits for WP11c packing §5b
(Q70). S4 two-finger pull and 0.5 m drop stay qualitative. Insertion
and retention forces stay NOT_MEASURED (need printed PA12). The hinge
callout on `render_lateral.png` sits near the hook tube; the lip itself
is in the hook-end wall under the lid.

## Needs a decision

1. M1 (Q34). Default 52. Manifest `provisional: true`.
2. Colour, grey or dyed black (Q30).
3. Q17 REF dome on the tail.
4. S4 pull and drop (qualitative, plan v2 §7).
5. Standoff 3.0 vs Harwin 4.0. This file keeps 3.0.
6. Q70 USB: packing §5b (WP11c). This shell does not cut the opening.
7. Q76 built: circular root r 1.75, fillet 1.5 applied. No coordinator
   fallback.

Q59 stays the slot. Q71 is built on this solid.

## Final commit sha

`bb0c788b8d34b1d098feab73a60fa1a2f7be8c3d`
(`shell(v2b): screw closure, lofted lid, hook root`).
````

### WP14c (lane w1)

````markdown
# WP14c report — shell v2c: concealed screw, boss pilots, render stamp

Lane `w1`, branch `lane/w1-r6`, package WP14c. Merged `origin/main`
(`7b23eb5`, Round 7 briefs) first. `plan-v2.md` and `open-questions.md`
were not edited. Order 1 files under `docs/fab/cad/v1/` were not written.

## What was built

Same construction path as Stage B v2. `STAGE=shell` now puts the Q71
head well on the medial tail (skin hides it). The lateral lid is not
cut. CAD pilots are Ø2.10 with boss OD ≥ 5.0 at the tail and the two
island bosses (L8 §4). `render.py` stamps the manifest commit that
built the solids, or the tree hash plus `dirty` when STEP/STL/3MF
differ from HEAD. Overlay `scripts/cad/params/shell_v2.toml`. Outputs
`docs/fab/cad/v2/`. Record `docs/fab/shell-v2.md` §2, §4, §5. Manifest
`provisional: true`.

USB opening and tab-fold pockets wait for packing §5c (WP11d, Q70).

## Before / after (measured on the built solid)

| Check | WP14b (`bb0c788`) | WP14c |
|---|---|---|
| `V2_CLOSURE` | pass. Hinge undercut 1, engagement 4.00, boss wall 3.13, well on the lid | pass. Hinge undercut 1, lip in 1, engagement 4.30, boss wall 3.08, well air 1, well on the medial tail |
| `V2_LATERAL_unbroken` | (absent; lid well visible) | pass. 18 samples, 0 pits, old lid-well site nylon |
| `V2_BOSS_pilot` | (absent; CAD pilot Ø2.0) | pass. Tail Ø2.10 / wall 1.92 / OD 5.94; both islands Ø2.10 / 1.45 / 5.00 |
| `V2_BOSS` | pass. drop 0.50 | pass. drop 0.50, island tops 0.5 below standoff |
| `V2_EDGE_radii` | pass. flat_stations 0, lid_rim_R 1.08 | pass. stations 6, flat_stations 0, min rise 0.030, lid_rim_R 1.08 |
| `V2_USB_end` | NOT_MEASURED packing §5b, Q70 | NOT_MEASURED packing §5c, Q70; hook-end wall left solid |
| Build exit | 0 | 0. USB row is NOT_MEASURED by name and does not fail the build |
| Render stamp | `c68d4b2839c9` (reviewer solids) | `solids commit ccb66085ad6d` = `manifest.commit` |

Renders (committed):

- `docs/fab/cad/v2/render_medial.png`
- `docs/fab/cad/v2/render_lateral.png`

Solids commit stamped on both views:
`ccb66085ad6dcd82ff379c60afd1d86d10ad294b`.

## Gates

| Gate | Command | Result |
|---|---|---|
| Full suite | `.venv/bin/python -m unittest discover -s tests -v` | OK, 207 tests, 283.181 s, CAD tests ran |
| Order 1 byte-identical | `CadRegenTests.test_reference_regen_matches_committed_hashes` and `CadRenderTests.test_renders_and_drawing_regen_byte_identical` | both ok |
| Stage B v2 | `CadStageBV2BuildTests` vs `STAGE_B_V2_MEASURED`; two consecutive runs | ok. Q59 still fail on the unslotted Stage B path. File hashes identical run to run |
| Shell twice identical | `CadShellV2BuildTests.test_two_consecutive_shell_runs_are_identical` | ok, exit 0, `stage_b_failing: []`, solids equal to `docs/fab/cad/v2/` |
| Stamp equals manifest | `CadShellV2StampTests.test_stamp_text_equals_manifest_commit` | ok |
| Manifest bytes | `.venv/bin/python scripts/cad/manifest.py --check-bytes docs/fab/cad/v2/manifest.json` | schema 1 ok |
| git status | `git status --short` | empty at DONE (this report untracked) |

Plan §9 row 14 (shell v2 body, lid, closure and hook, §7 checks, Stage B
checks on the built solid, identical regeneration): the listed files
exist; §7 and Stage B rows are in the manifest and in `shell-v2.md`;
regeneration tested as above.

## What was not done

No order, quote, or upload. USB opening waits for WP11d packing §5c
(Q70). S4 two-finger pull and 0.5 m drop stay qualitative. Insertion
and retention forces stay NOT_MEASURED (need printed PA12). The Ø2.7
holes in the board island stay the board lane's.

## Needs a decision

1. M1 (Q34). Default 52. Manifest `provisional: true`.
2. Colour, grey or dyed black (Q30).
3. Q17 REF dome on the tail.
4. S4 pull and drop (qualitative, plan v2 §7).
5. Standoff 3.0 vs Harwin 4.0. This file keeps 3.0.
6. Q70 USB: packing §5c (WP11d). This shell does not cut the opening.

Q59 stays the slot. Q71 is built on this solid: medial-tail well, lateral
lid unbroken.

## Final commit sha

`7d111c6ab40925dcf2345ce1ada4e07afe9df617`
(`shell(v2c): concealed screw, boss pilots, render stamp`).
````

### WP14d (lane w1)

````markdown
# WP14d report — shell v2d: width 22 on packing §5c

Lane `w1`, branch `lane/w1-r6`, package WP14d. Merged `origin/main`
first. `plan-v2.md` and `open-questions.md` were not edited. Order 1
files under `docs/fab/cad/v1/` were not written. Packing and board
files were not edited.

## What was built

Same construction path as Stage B v2. `STAGE=shell` now overlays the
§5c width-22 geometry: cavity u 1.50–20.50, island u 2.25–19.75 × s
16.00–37.60, 501012 pack, rib s 14.90–15.70. Outer height 9.0 and
TOTAL_CHORD 47.90 stay. Island bosses sit at the §5c hole sites.
SIG1/SIG2 are neck-end strips. Two flush charging pads sit at P4/P5.
`V2_USB_end` is NOT_APPLICABLE. Overlay
`scripts/cad/params/shell_v2.toml`. Outputs `docs/fab/cad/v2/`. Record
`docs/fab/shell-v2.md` §2, §4, §5. Manifest `provisional: true`.

§5c was read from `/home/user/projects/elicio/.worktrees/w3/docs/fab/packing-v2.md`
at sha `e1f1d6facf37526d358569dace7ebf75ee4e160f`
(`packing(v2c): publish §5c for Q81-Q83`). `V2_BOSS_sites` parses that
table. Sites are not hard-coded in the check.

The tail cannot take two more 5 AF standoffs at u 0.75 and 21.25 (those
points sit in the 1.5 side walls on the medial fillet). Construction is
flush RING_PAD Ø5 stems and domes, Ø2.7 holes, Ø2.10 self-tap pilots.

## Before / after (measured on the built solid)

| Check | WP14c (`7d111c6`) | WP14d |
|---|---|---|
| Width / cell | 20 / 501015 | 22 / pack501012 |
| Cavity u | packing C 1.5–18.5 | 1.50–20.50 |
| Island | u 2.25–17.75 × s 18.6–37.6 | u 2.25–19.75 × s 16.00–37.60 |
| `V2_BOSS` | pass. drop 0.50 at layout fallback sites | pass. drop 0.50 at (13.45, 17.70) and (17.95, 17.70) |
| `V2_BOSS_sites` | (absent) | pass. centre error 0; 3.30 keep gap 0.15 vs every courtyard |
| `V2_BOSS_pilot` | Tail Ø2.10 / 1.92 / 5.94; islands Ø2.10 / 1.45 / 5.00 | Tail Ø2.10 / 1.92 / 5.94; boss 1 Ø2.10 / 1.45 / 5.00; boss 2 Ø2.10 / 2.40 / 6.90 |
| `V2_TAB_envelope` | board-ward tabs | pass. neck-end SIG1 10.71, SIG2 21.81; side walls 1.50; no side pockets |
| `V2_CHARGE_pads` | (absent) | pass. flush pads; nylon between 17.8; P4/P5 clear of REF ≥ 7.81 and screw ≥ 7.39 |
| `V2_USB_end` | NOT_MEASURED packing §5c, Q70 | NOT_APPLICABLE: Q81: no receptacle at M1 52 |
| `V2_CLOSURE` | engagement 4.30, boss wall 3.08 | engagement 4.30, boss wall 6.45 (width 22) |
| `V2_LATERAL_unbroken` | 18 samples, 0 pits | 20 samples, 0 pits |
| `V2_EDGE_radii` | 6 stations, min rise 0.030, rim R 1.08 | 7 stations, min rise 0.025, rim R 1.08 |
| `V2_WALL_minima` | sides 1.50, hinge 1.00 | sides 1.50, hinge 1.00 |
| Build exit | 0 | 0. NOT_APPLICABLE does not fail the build |
| Render stamp | `solids commit ccb66085ad6d` | `solids commit f52afc5b7b25` = solids commit, not HEAD |

Renders (committed):

- `docs/fab/cad/v2/render_medial.png`
- `docs/fab/cad/v2/render_lateral.png`

Solids stamp on both views:
`f52afc5b7b25eb1562aaf916858b9def935d0179`.

## Gates

| Gate | Command | Result |
|---|---|---|
| Full suite | `LC_ALL=C LANG=C .venv/bin/python -m unittest discover -s tests -v` | exit 0. CAD tests ran. First run failed two shell tests: `git show` of §5c decoded as ASCII. Fixed (`encoding="utf-8"`). Second run exit 0 |
| Shell CAD class | `LC_ALL=C .venv/bin/python -m unittest tests.test_cad.CadShellV2Tests tests.test_cad.CadShellV2BuildTests tests.test_cad.CadShellV2StampTests -v` | OK, 7 tests, 146.751 s |
| Order 1 byte-identical | `CadRegenTests.test_reference_regen_matches_committed_hashes` and `CadRenderTests.test_renders_and_drawing_regen_byte_identical` | both ok on the full suite |
| Stage B v2 | `CadStageBV2BuildTests` two consecutive runs | ok. File hashes identical run to run. Width 20 packing C overlay unchanged |
| Shell twice identical | `CadShellV2BuildTests.test_two_consecutive_shell_runs_are_identical` | ok, exit 0, `stage_b_failing: []`, solids equal to `docs/fab/cad/v2/` |
| Stamp equals manifest | `CadShellV2StampTests.test_stamp_text_equals_manifest_commit` | ok |
| Manifest bytes | `.venv/bin/python scripts/cad/manifest.py --check-bytes docs/fab/cad/v2/manifest.json` | schema 1 ok |
| git status | `git status --short` | empty at DONE (this report untracked) |

Plan §9 row 14 (shell v2 body, lid, closure and hook, §7 checks, Stage B
checks on the built solid, identical regeneration): the listed files
exist; §7 and Stage B rows are in the manifest and in `shell-v2.md`;
regeneration tested as above.

The brief asked for last commit message
`shell(v2d): width 22 on §5c, bosses at the hole sites, neck-end strips, tail charging contacts`.
That is `829aeba`. HEAD is `ecfff54` (UTF-8 decode so unittest under
`LC_ALL=C` can read the §5c en-dashes). Solids were not rebuilt after
that one-line change.

## What was not done

No order, quote, or upload. USB opening waits for WP14e if M1 ≥ 58.3.
S4 two-finger pull and 0.5 m drop stay qualitative. Insertion and
retention forces stay NOT_MEASURED (need printed PA12). Board holes at
the boss sites stay the board lane's.

## Needs a decision

1. M1 (Q34). Default 52. Manifest `provisional: true`.
2. Colour, grey or dyed black (Q30).
3. Q17 REF dome on the tail.
4. S4 pull and drop (qualitative, plan v2 §7).
5. Standoff 3.0 vs Harwin 4.0. This file keeps 3.0.
6. WP14e USB if Rolf measures M1 ≥ 58.3.

Q81/Q82/Q83 are built on this solid.

## Final commit sha

`ecfff5486bbbb84b87a550954ecf6febd3acf478`
(`shell(v2d): read packing §5c as UTF-8 under LC_ALL=C`).

Named last-commit message is
`829aeba74e9231c0cc7a9c16b6dd796ef8e3a26d`
(`shell(v2d): width 22 on §5c, bosses at the hole sites, neck-end strips, tail charging contacts`).
Solids sha stamped on the renders:
`f52afc5b7b25eb1562aaf916858b9def935d0179`.
````

### WP14e (lane w1)

````markdown
# WP14e report — shell v2e: hook-end charging pads per §5d

Lane `w1`, branch `lane/w1-r6`, package WP14e. Merged `origin/main`
first (`bd24e26`). `plan-v2.md` and `open-questions.md` were not edited.
Order 1 files under `docs/fab/cad/v1/` were not written. Packing and
board files were not edited.

## What was built

Same construction path as Stage B v2. `STAGE=shell` keeps the width-22
§5d geometry. P4 and P5 left the tail corners. They sit on the hook-end
medial floor at the §5d folded sites, y 1.50, with flush RING_PAD Ø5
holes through the floor. A rib slot and a drop channel carry the flex
tab from leftover s 16.00. `V2_USB_end` stays NOT_APPLICABLE. Overlay
`scripts/cad/params/shell_v2.toml`. Outputs `docs/fab/cad/v2/`. Record
`docs/fab/shell-v2.md` §2, §4, §5. Manifest `provisional: true`.

§5d was read from `lane/w3` at sha
`408a4765ec953d6cc84210fd3e5632185ff95cbb`
(`packing(v2e): give P4/P5 Q85 flat centres through the rib-slot fold`).
`V2_BOSS_sites` / `V2_CHARGE_pads` parse the folded-site table for
P1–P5. Sites are not hard-coded in the check. P1–P3 are unchanged.

Construction is flush RING_PAD Ø5 through the floor (the tail cannot
take two Ø5 pads). Hex standoffs stay on SIG1/SIG2/REF only.

## Before / after (measured on the built solid)

| Check | WP14d (`ecfff54`) | WP14e |
|---|---|---|
| Width / cell | 22 / pack501012 | 22 / pack501012 |
| `V2_BOSS` | pass. drop 0.50 at (13.45, 17.70) and (17.95, 17.70) | pass. same sites, drop 0.50 |
| `V2_BOSS_sites` | pass. centre error 0; keep gap 0.15; packed from §5c | pass. centre error 0; keep gap 0.15; P1–P5 from §5d folded table sha `408a476` |
| `V2_BOSS_pilot` | Tail Ø2.10 / 1.92 / 5.94; boss 1 Ø2.10 / 1.45 / 5.00; boss 2 Ø2.10 / 2.40 / 6.90 | Tail Ø2.10 / 1.92 / 5.94; boss 1 Ø2.10 / 1.45 / 5.00; boss 2 Ø2.10 / 2.40 / 6.90 |
| `V2_TAB_envelope` | pass. neck-end SIG1 10.71, SIG2 21.81; side pockets 0 | pass. same strips; rib slot air 1; drop channel air 1; side pockets 0 |
| `V2_CHARGE_pads` | pass. flush pads at tail (0.75, 44.0) and (21.25, 44.0); nylon between 17.8 | pass. flush Ø5 floor pads at (14.70, 4.30) and (17.70, 11.72); nylon between 3.00; floor 1.50; cell gap 0.30 / 3.30; creepage nylon 1.0 |
| `V2_USB_end` | NOT_APPLICABLE: Q81: no receptacle at M1 52 | NOT_APPLICABLE: Q81: no receptacle at M1 52 |
| `V2_CLOSURE` | engagement 4.30, boss wall 6.45 | engagement 4.30, boss wall 6.45 |
| `V2_LATERAL_unbroken` | 20 samples, 0 pits | 20 samples, 0 pits |
| `V2_EDGE_radii` | 7 stations, min rise 0.025, rim R 1.08 | 7 stations, min rise 0.025, rim R 1.08 |
| `V2_WALL_minima` | sides 1.50, hinge 1.00 | sides 1.50, hinge 1.00 |
| Build exit | 0 | 0. NOT_APPLICABLE does not fail the build |
| Render stamp | solids `f52afc5` | solids `9734c3418445` = `manifest.commit` |

Renders (committed):

- `docs/fab/cad/v2/render_medial.png`
- `docs/fab/cad/v2/render_lateral.png`

Both views stamp solids commit
`9734c34184451cbac9a76a7d0a5caa45fdfb3ed0`.
Pads are labelled `P4/P5 charging pads, hook end (Q86)`.

## Gates

| Gate | Command | Result |
|---|---|---|
| Full suite | `LC_ALL=C LANG=C .venv/bin/python -m unittest discover -s tests -v` | exit 0 |
| Shell CAD class | `LC_ALL=C .venv/bin/python -m unittest tests.test_cad.CadShellV2Tests tests.test_cad.CadShellV2BuildTests tests.test_cad.CadShellV2StampTests -v` | OK, 7 tests, 142.133 s |
| Order 1 byte-identical | `CadRegenTests.test_reference_regen_matches_committed_hashes` and `CadRenderTests.test_renders_and_drawing_regen_byte_identical` | both ok on the full suite |
| Stage B v2 | `CadStageBV2BuildTests.test_two_consecutive_v2_stage_b_runs_are_identical` | ok |
| Shell twice identical | `CadShellV2BuildTests.test_two_consecutive_shell_runs_are_identical` | ok, `stage_b_failing: []`, solids equal to `docs/fab/cad/v2/` |
| Stamp equals manifest | `CadShellV2StampTests.test_stamp_text_equals_manifest_commit` | ok |
| Manifest bytes | `.venv/bin/python scripts/cad/manifest.py --check-bytes docs/fab/cad/v2/manifest.json` | schema 1 ok |
| git status | `git status --short` | empty at DONE (this report untracked) |

Plan §9 row 14 (shell v2 body, lid, closure and hook, §7 checks, Stage B
checks on the built solid, identical regeneration): the listed files
exist; §7 and Stage B rows are in the manifest and in `shell-v2.md`;
regeneration tested as above.

Last commit message is
`shell(v2e): charging pads on the hook-end floor per §5d, rib slot and drop channel`.

## What was not done

No order, quote, or upload. USB opening waits if M1 ≥ 58.3. S4
two-finger pull and 0.5 m drop stay qualitative. Insertion and
retention forces stay NOT_MEASURED (need printed PA12). Board holes and
the Q84 DRC rule stay the board lane's. The cell-side drop at u 11.90
is not used (packing extras).

## Needs a decision

1. M1 (Q34). Default 52. Manifest `provisional: true`.
2. Colour, grey or dyed black (Q30).
3. Q17 REF dome on the tail.
4. S4 pull and drop (qualitative, plan v2 §7).
5. Standoff 3.0 vs Harwin 4.0. This file keeps 3.0.
6. Q86: Rolf can overrule the hook-end pads with Ø2.1 pads on the tail.

Q81/Q82/Q83/Q86 are built on this solid.

## Final commit sha

`bdfc429481f1bd0589b2c157dcf7c42e6c75f726`
(`shell(v2e): charging pads on the hook-end floor per §5d, rib slot and drop channel`).

Solids sha stamped on the renders:
`9734c34184451cbac9a76a7d0a5caa45fdfb3ed0`.
§5d sha:
`408a4765ec953d6cc84210fd3e5632185ff95cbb`.
````

### WP17c (lane w5)

````markdown
# WP17c Work Package Report: Research v5 — JLC Edge Rule, FPC Sides, Router, Tail Screw

**Package:** WP17c — Research v5: the JLC edge rule, FPC assembly sides, a router, a screw  
**Lane:** w5  
**Worktree:** `/home/user/projects/elicio/.worktrees/w5`  
**Branch:** `lane/w5`  
**Date:** 2026-09-18  
**Final Commit SHA:** `f8b16343527b273027d8b55ee06d473c95028545`  

---

## 1. Answer to Item 1: The JLC Assembly Edge Rule

The JLCPCB $\ge 2.5\text{ mm}$ edge rule is an automated machine handling and conveyor clamping clearance constraint measured from component bodies to the panel's rail edge, not to the board's own internal routed or laser-cut outline. For standard PCBA and panelized FPC orders, JLCPCB adds 5 mm sacrificial process rails by default (and mounts flexible circuits onto a rigid carrier pallet) so conveyor belts and clamping jaws grip the outer rail border. With edge rails present, the distance from component bodies and copper features to the board outline is governed solely by profile laser cutting tolerances ($\ge 0.20\text{ mm}$ pad-to-outline to prevent carbonization micro-shorts, and $\ge 0.30\text{ mm}$ copper trace clearance). A 2.5 mm wide tab strip terminating in a Ø5.0 mm ring pad is not an assembly problem because it carries no SMT component bodies, maintains $> 1.1\text{ mm}$ trace-to-edge margin, and has $0.50\text{ mm}$ ring pad clearance to outline while supported by the SMT carrier fixture.

---

## 2. What Was Built

Created and delivered `docs/fab/L8-research-v5.md` on branch `lane/w5` (committed at `f8b16343527b273027d8b55ee06d473c95028545` with message `research(v5): JLC edge rule and FPC sides, router, screw`).

### Summary of Findings by Section

1.  **JLC Assembly Edge Rule (Q78):**
    *   *Terms & Conditions Statement:* "The distance between the body of the components and the edge of the board must be equal to or greater than 2.5mm" under Notes on DFM.
    *   *Technical Intent:* Prevents pick-and-place nozzle and conveyor guide rail collisions with component bodies.
    *   *Edge Rails:* JLCPCB adds 5 mm process rails by default for standard PCBA orders under 70 × 70 mm, and on all 4 sides of FPC panels when "Panel by JLCPCB" is selected. SMT conveyor rails clamp the 5 mm process edges, ensuring $\ge 5.0\text{ mm}$ clearance to all parts.
    *   *Board Outline Clearance:* With rails present, component courtyards can extend directly to the board outline. Minimum copper-to-outline clearance is **0.20 mm** (laser cutting carbonization threshold) and **0.30 mm** for routing/traces.
    *   *FPC Depaneling:* FPC does not use V-cuts (thickness 0.11 mm is below the 0.6 mm V-cut floor). Depaneling uses UV laser cutting along 0.7–1.0 mm bridge tabs.
    *   *Tab Strip:* A 2.5 mm wide strip with a Ø5.0 mm ring pad has zero SMT components and satisfies all copper-to-outline clearances (> 1.1 mm for traces, 0.5 mm for the pad). It is zero assembly problem.
2.  **FPC Assembly Sides:**
    *   *Double-Sided SMT:* Fully supported on 2-layer polyimide flex. Configured via the "Both sides" selector in the JLCPCB SMT portal. Uses custom carrier pallets ($23.57 fixture fee) and two-pass reflow.
    *   *Component Constraints:* Minimum passive package size 0402 (0201 in Standard SMT). Minimum IC lead pitch 0.35 mm (Standard) / 0.40 mm (Economic). Maximum component limit is **300 designators** per order. Extended parts incur a $3.00 USD setup fee per unique line.
    *   *Stiffener Rules:* Extra fee applies if $\ge 4$ stiffeners are used on prototype orders, or if stiffeners cover $\ge 90\%$ of board area or are stacked ($8.14 + $24.44/m² per extra stiffener). Stiffeners cannot cover SMT component pads on the same layer.
3.  **A Router That Writes a File on This Mac:**
    *   *Freerouting v2.4.1:* Decoupled the algorithmic core from Swing/AWT desktop GUI. Headless mode **writes a `.ses` file** on macOS Apple Silicon under Java 21+.
    *   *Exact CLI Flags:*
        ```bash
        java -jar freerouting-2.4.1-exec.jar --gui.enabled=false -de <input.dsn> -do <output.ses> -mp <passes> -mt <threads>
        ```
    *   *Issue Tracker on 2.1.0 Hang:* Issue #522 (pass counter tied to GUI repaint loop in headless mode causing infinite looping) was fixed by `@ceoloide` in **PR #541** (merged April 2025). Issues #368 and #457 (headless AWT exceptions and modal update dialogs) were eliminated by the v2.4.0 architectural separation.
    *   *Alternative Free Autorouters:*
        *   **ProtoFlow (ProtoRoute):** Desktop tool (`protoflow.ai`) that natively reads and writes `.kicad_pcb` files directly, eliminating DSN/SES conversion.
        *   **KiCadRoutingTools:** Open-source Python/Rust A* router plugin for KiCad.
        *   **DeepPCB:** Free-tier AI cloud-assisted router with an official KiCad PCM plugin.
        *   **KiCad Python Scripting (IPC API / `pcbnew`):** Programmatic trace and via placement.
4.  **The Tail Screw (Q71) and MJF Pilot Hole:**
    *   *M2.5 Titanium Screws in Ones:*
        *   **The Thomas RC (KDRC):** KDRC M2.5 Grade 5 Titanium Button Head Screws (4 mm and 6 mm length) sold individually in single units for **$1.60 USD each**.
        *   **1up Racing:** Pro Duty Titanium M2.5 LowPro / Button Head Screws (5 mm and 6 mm length) sold in 5-packs for **$8.49 – $8.99 USD**.
        *   **McMaster-Carr / Bolt Depot:** Neither stocks M2.5 in titanium (McMaster titanium starts at M3; Bolt Depot stocks steel/stainless M2.5 only).
    *   *MJF PA12 Pilot Hole Recommendation:*
        *   HP Multi Jet Fusion guidelines recommend self-tapping screws for threads $< 6\text{ mm}$ into pre-formed pilot holes.
        *   MJF PA12 bores contract by $0.10\text{ to }0.15\text{ mm}$ during cooling.
        *   Recommended CAD pilot hole diameter for M2.5 thread-forming: **$\mathbf{\varnothing 2.10\text{ to }2.15\text{ mm}}$** (yields $\varnothing 2.00\text{ to }2.05\text{ mm}$ printed hole after shrinkage, giving 70–75% thread engagement).
        *   Recommended boss outer diameter: **$\mathbf{\ge 5.00\text{ mm}}$** (radial wall thickness $\ge 1.4\text{ mm}$) to withstand hoop stress without cracking.

---

## 3. Acceptance Verification and Gates

### Gate 1: Test Suite
*   **Command:** `/home/user/projects/elicio/.worktrees/w5/.venv/bin/python -m unittest discover -s tests -v`
*   **Result:** Ran 206 tests in 83.403s. **OK (skipped=26)**. 0 errors, 0 failures.

### Gate 2: Clean Git Working Tree
*   **Command:** `git status --short`
*   **Result:** Empty (clean). Report `.reports/WP17c-report.md` is gitignored.

### Gate 3: Commit History on `lane/w5`
*   Commit `f8b16343527b273027d8b55ee06d473c95028545`: `research(v5): JLC edge rule and FPC sides, router, screw`

---

## 4. What Stayed UNVERIFIED

1.  **Fixed Numerical Component Height Ceiling on FPC:** `UNVERIFIED` as a single published value on JLCPCB flex pages (constrained by standard pick-and-place nozzle clearance and carrier fixture design).
2.  **McMaster-Carr & Bolt Depot M2.5 Titanium Screws:** Verified that neither supplier stocks M2.5 in titanium (McMaster starts titanium at M3; Bolt Depot stocks steel/stainless only).

---

## 5. Needs a Decision for Plan v2 Build Rounds

1.  **Board Packing Search Constraints (Q78, WP11d):**
    *   Now confirmed that the 2.5 mm JLC rule applies to the panel rail edge, not the board outline.
    *   *Action:* WP11d can place components on the parts island up to the standard 0.30 mm copper-to-outline clearance boundary. Dense single-sided and double-sided placement on the w20 body can proceed without an artificial 2.5 mm internal border setback.
2.  **Tail Fastener Selection (Q71):**
    *   *Action:* Specify M2.5 × 4 mm or M2.5 × 6 mm Grade 5 Titanium Button Head screws (e.g. from The Thomas RC at $1.60 each, or 1up Racing 5-pack at $8.49) for the concealed tail closure screw.
3.  **MJF Boss Pilot Hole Sizing (Q71, Q73, WP14b):**
    *   *Action:* Model the tail closure boss and the two island retention bosses (Q73) with a CAD pilot hole diameter of **$\varnothing 2.10\text{ mm}$** and an outer boss diameter of **$\varnothing 5.00\text{ mm}$**.
4.  **Autorouting Toolchain Execution (Q77, WP12d):**
    *   *Action:* The board lane can invoke Freerouting v2.4.1 headlessly with `--gui.enabled=false -de elicio-v2.dsn -do elicio-v2.ses -mp 20 -mt 4` on macOS with Java 21, or utilize ProtoFlow for direct `.kicad_pcb` routing.

---

## 6. Final Commit SHA

`f8b16343527b273027d8b55ee06d473c95028545`
````

### WP13c (lane w4)

````markdown
# WP13c report — Q75 dropout is a report, S2 continues

Lane `w4`. Branch `lane/w4`. Final commit `21dde8a76a609ea6454773cac8cc093048197504`.
Worktree `/home/user/projects/elicio/.worktrees/w4`.
Python 3.13.15. Extra `ble` installed (bleak 3.0.2).

Host-only. No radio and no board were used.

## What was built

`elicio receive-check` still uses exit 3 when no scored line failed and a montage §8 line 3.4 dropout is present. Exit 3 is a report, not a stop (Q75). The printed output names the dropout count, the longest run in sample intervals (`length − 1`), and the acquisition index where that run began. The last line of an exit-3 run is exactly `S2 continues (Q75); dropout count goes in the session note`. A same-criterion failure still wins: exit 1, with the dropout count printed, and without that continues line. Exit 0 and 2 keep their meaning.

The session record is `sidecar.json`. After a check, it carries `dropout_count`, `longest_run_intervals`, and `longest_run_start_acq`.

`docs/fab/receiver-v2.md`: the open-decision-75 sentence is gone. The exit-code table marks 1 and 2 as stops and 3 as a report (Q75).

`docs/fab/assemble.md`: one sentence after the firmware copy step. At exit 3, write the count in the session note and continue. Stop only on exit 1 or 2.

Tests: dropout only (exit 3 plus the continues line); failure plus dropout (exit 1 plus the count); clean (exit 0). Existing fixture `tests/fixtures/receiver_v2/dropout.json` was enough. `elicio receive --simulate-live` still exits 0.

Files: `src/elicio/receiver_v2.py`, `tests/test_receiver_v2.py`, `docs/fab/receiver-v2.md`, `docs/fab/assemble.md`. One commit. No firmware, board, montage, plan-v2, or open-questions edits.

## Gates

1. `.venv/bin/python -m unittest discover -s tests -v`

   Result: exit 0. `Ran 207 tests in 83.970s` `OK (skipped=26)`. Receiver module: 15 tests, OK.

2. `elicio receive-check` on the three cases (paste below).

3. `git status --short` empty after the commit.

Plan v2 §11 row 13 "builds in CI; bench-tested at S2": no CI in the repo. Host unittest ran. S2 bench was not run (no board). Plan v2 §9 S2 row was not run.

### Clean fixture — exit 0

```
.venv/bin/python -m elicio.cli receive --simulate tests/fixtures/receiver_v2/normal.json --out <tmp>/clean
.venv/bin/python -m elicio.cli receive-check <tmp>/clean
```

```
{
  "dropout_count": 0,
  "dropout_stretches": 0,
  "dropouts": [],
  "duration_s": 0.002,
  "exit_code": 0,
  "loader": "elicio.receiver_v2.load_receiver_session",
  "longest_run_intervals": 0,
  "longest_run_start_acq": null,
  "losses": 0,
  "ok": true,
  "overruns": 0,
  "same_criterion": {
    "3.10": "not_scored",
    "3.5": "not_scored",
    "3.6": "not_scored",
    "3.7": "not_scored",
    "3.8": "not_scored",
    "3.9": "not_scored"
  },
  "same_criterion_failed": [],
  "sample_count": 4,
  "wraps": 0
}
```

Process exit: 0. No continues line.

### Dropout only — exit 3

```
.venv/bin/python -m elicio.cli receive --simulate tests/fixtures/receiver_v2/dropout.json --out <tmp>/drop
.venv/bin/python -m elicio.cli receive-check <tmp>/drop
```

```
{
  "dropout_count": 2,
  "dropout_stretches": 2,
  "dropouts": [
    {
      "channel": 0,
      "kind": 1,
      "length": 205,
      "start_acq": 0
    },
    {
      "channel": 1,
      "kind": 1,
      "length": 205,
      "start_acq": 0
    }
  ],
  "duration_s": 0.1025,
  "exit_code": 3,
  "loader": "elicio.receiver_v2.load_receiver_session",
  "longest_run_intervals": 204,
  "longest_run_start_acq": 0,
  "losses": 0,
  "ok": false,
  "overruns": 0,
  "same_criterion": {
    "3.10": "not_scored",
    "3.5": "not_scored",
    "3.6": "not_scored",
    "3.7": "not_scored",
    "3.8": "not_scored",
    "3.9": "not_scored"
  },
  "same_criterion_failed": [],
  "sample_count": 205,
  "wraps": 0
}
dropout count: 2
longest run: 204 sample intervals beginning at acq_index 0
S2 continues (Q75); dropout count goes in the session note
```

Process exit: 3.

### Same-criterion failure plus dropout — exit 1

The dropout session above, with `sidecar.json` `same_criterion["3.7"] = "fail"`.

```
{
  "dropout_count": 2,
  "dropout_stretches": 2,
  "dropouts": [
    {
      "channel": 0,
      "kind": 1,
      "length": 205,
      "start_acq": 0
    },
    {
      "channel": 1,
      "kind": 1,
      "length": 205,
      "start_acq": 0
    }
  ],
  "duration_s": 0.1025,
  "exit_code": 1,
  "loader": "elicio.receiver_v2.load_receiver_session",
  "longest_run_intervals": 204,
  "longest_run_start_acq": 0,
  "losses": 0,
  "ok": false,
  "overruns": 0,
  "same_criterion": {
    "3.10": "not_scored",
    "3.5": "not_scored",
    "3.6": "not_scored",
    "3.7": "fail",
    "3.8": "not_scored",
    "3.9": "not_scored"
  },
  "same_criterion_failed": [
    "3.7"
  ],
  "sample_count": 205,
  "wraps": 0
}
dropout count: 2
longest run: 204 sample intervals beginning at acq_index 0
```

Process exit: 1. No continues line.

`elicio receive --simulate-live` still exits 0 (unittest `test_cli_simulate_live`).

## What was not done

No radio. No board. No gel montage. `docs/fab/montage.md` was not edited. `docs/fab/plan-v2.md` and `docs/fab/open-questions.md` were not edited. Firmware and board files were not edited.

A local unversioned `post-commit` hook ran `git push` after the commit on `lane/w4`. This lane did not invoke `git push`.

## Needs a decision

None. Q75 is the reading this package follows.

## Final sha

`21dde8a76a609ea6454773cac8cc093048197504`
````

### WP12c (lane w2)

````markdown
# WP12c report — Route the flex board to DRC 0 (lane w2)

Worktree: `/home/user/projects/elicio/.worktrees/w2`
Branch: `lane/w2`
Package: WP12c
Date: 2026-09-18
KiCad: 10.0.6 (`kicad-cli`)
Java: Homebrew OpenJDK 21.0.12.1 (`/opt/homebrew/opt/openjdk@21/bin/java`)
Continuing from: `480e355`
Final commit: `f4376ca9eac250ea38eba2690eed312f34012943`

## What was built

First commit `ca484d5` dropped the WP12b shorting B.Cu bus (465 segments, 134 vias). Footprints were not moved. Named SMT centres still match packing-v2.md §5.

Freerouting v2.1.0 was run headless (`gui.enabled=false`, `-mp`, `-dct`, wall-clock timeout). `kicad-cli pcb export` has no `specctra` subcommand; DSN came from `pcbnew.ExportSpecctraDSN` (58492 bytes). Every run froze after `Job started`. No SES. No hs_err dump. Redo log: `hardware/board/route.md`.

Own router: `maze_route.py` is now a clearance-aware A* (Default 0.10 mm, ring 7×7 keep-outs, one net per tab, no shorting bus). Trial on a copy: 23 nets routed, 25 failed, 420 tracks, DRC 770 errors. That copper was **not** written back.

The committed board stays un-shorted and un-routed: 0 tracks, 0 vias. `routed: false`. Last commit is not `board(v2c): routed to DRC 0`.

`docs/fab/board-v2.md` §15 only. Schematic, project rules, `scripts/` untouched vs `480e355`.

Nothing ordered, quoted or uploaded. No vendor contact.

## Gates

### 1. Unittest (this package)

```text
.venv/bin/python -m unittest tests.test_board_release -v
```

Result: **OK** (5 tests). ERC 0. BOM rows = placed parts = 59. `"routed": false` without `--routed`. `--routed` refused (`drc_errors` 128, `unconnected_items` 132, `no_tracks` 1). `pcb_tracks` = 0. Named SMT centres within 0.1 mm of packing §5. WP12c assertion: order release stays un-routed.

```text
.venv/bin/python -m unittest discover -s tests -v
```

Result: 171 tests, **13 FAIL**, all `test_cad.CadRegenTests` v1 solid hashes (`body_full_p15`, `body_full_p25`, `body_thin_p15`, `lid`). This package does not own CAD. Same 13 as WP12b.

### 2. `release.py --routed`

```text
.venv/bin/python scripts/board/release.py --board-dir hardware/board --out /tmp/wp12c-release --routed
```

| Field | Value |
|---|---|
| exit | 1 (`routed release refused`) |
| erc_errors | 0 |
| erc_warnings | 0 |
| drc_errors | 128 |
| drc_warnings | 21 |
| unconnected_items | 132 |
| pcb_tracks | 0 |
| pcb_pads_without_net | 0 |
| routed | true (flag only; order release is not green) |
| bom_rows | 59 |
| placed_parts | 59 |

Non-`--routed` job still exits 0 (ERC 0, outputs present).

**This gate is not met.** DRC 0 is not reachable on this placement with frozen footprints and frozen `elicio-v2.kicad_pro`.

### 3. Forbidden paths vs `480e355`

```text
git diff 480e355 -- hardware/board/elicio-v2.kicad_sch hardware/board/elicio-v2.kicad_pro scripts/ docs/fab/board-v2.md
```

Result: schematic, project file, and `scripts/` empty. `docs/fab/board-v2.md` is §15 only (`@@ -397,22 +397,27 @@`).

### 4. `git status --short`

Empty.

## Plan §9 / brief deliverables

| Item | Result |
|---|---|
| Drop shorting bus first | `ca484d5`. 0 tracks, 0 vias. |
| Diagnose Freerouting hang | Done. Java 21.0.12.1. Log in `route.md`. No SES. |
| Own router if hang | A* with netclass Default 0.10 mm and ring keep-outs. Trial on a copy only. |
| `release.py --routed` exit 0 | **Fail.** 128 DRC, 132 unconnected, 0 tracks. |
| Contact isolation as WP12b | Unchanged: 7×7 ring keep-outs. Contact 1.0 mm vs 0402 still DRC-fails on pads. |
| Nothing new under RF keep-out | No new copper. |
| USB pairs short and matched | Not routed. Rule that would apply: nRF52840 USB is FS; ≤ 1.0 mm length delta on the tongue. |
| `board-v2.md` §15 | Rewritten. Via count 0. No analog trace. No hand-fix. |
| Routed assertion | `test_order_release_stays_unrouted`: tracks 0, DRC > 0, `--routed` refused. |

## What blocks DRC 0 (un-routed board, `kicad-cli pcb drc`)

These errors exist with **zero tracks**. A router cannot clear them without moving footprints or editing `elicio-v2.kicad_pro` (both frozen for WP12c):

| Type | Count | Examples |
|---|---|---|
| solder_mask_bridge | 38 | J3 vs SW1, J2 vs J4, U5 vs J4 |
| shorting_items | 32 | J2 MP GND vs J4 +VDD; C15 GND vs C8 +3V0; J3 SIG1 vs SW1 nRESET |
| Contact clearance 1.0 mm | 26 | R1/R2/R3 0402 pad gap 0.48 mm; J3 2.54 mm pitch |
| copper_edge_clearance | 18 | U2 pads 0.275 mm vs 0.300 mm; J2 at the outline |
| hole_clearance | 9 | J4 NPTH vs U5; J1 NPTH vs leftover B.Cu |
| items_not_allowed | 5 | J2 and U5 in J4 keep-out; U3 in U1 keep-out; R25/C10 in RF_FEED_NOTCH |

Maze copper on a copy made this worse (770 errors). It was discarded.

## What was not done

- DRC 0 / 0 unconnected / `release.py --routed` exit 0.
- Import of a Freerouting SES (none written).
- USB pair length match (no USB tracks).
- Hand-placed residue on the committed file (no route to fix).
- Full one-hour Freerouting wall clock on a single process: the job dies or freezes after `Job started` with no further log (180 s, 90 s, ~2 min, dead before 12 min). Same hang as WP12b (240 s). Extra time does not change the placement DRC.

## Needs a decision

1. Contact netclass 1.0 mm vs 0402 220 kΩ on a 2.5 mm tab (pad gap 0.48 mm) and vs J3 2.54 mm pitch. Isolation today is the 7×7 ring keep-out. DRC 0 needs a different Contact clearance or a different tab/header land.
2. Packing leftovers collide: J4 vs J2/U5, U3 vs U1 courtyard, U2 0.025 mm inside copper-to-edge, C15 vs C8, J3 vs SW1. WP12c must not move those footprints.
3. Freerouting v2.1.0 headless on this Mac never writes SES. A later lane can try v2.4.1 (the jar prints that version as available) or a different DSN path. That still does not clear (1) or (2).

## Commits

| SHA | Message |
|---|---|
| `ca484d5` | `board(v2c): drop the shorting bus fallback` |
| `d0a081b` | `board(v2c): clearance-aware maze after Freerouting hang` |
| `184c43a` | `docs(board-v2): record un-routed DRC after dropping the bus` |
| `845bac7` | `test(board-v2): assert WP12c stays un-routed` |
| `f4376ca` | `merge origin/lane/w2: restore e3e085b after the WP12c reset` |

Merge restored `e3e085b` (L7 quotes, schematic, `patch_sch_v2b.py`) on top of WP12c. `docs/fab/board-v2.md` auto-merged: L7 quotes and §15 both kept. `git push` fast-forwarded `origin/lane/w2` `e3e085b..f4376ca`. Working tree empty. Do not reset this lane below its pushed tip again.
````

### WP12d-prep (lane w2)

````markdown
# WP12d-prep report — router proof and side column (lane w2)

Worktree: `/home/user/projects/elicio/.worktrees/w2`
Branch: `lane/w2`
Package: WP12d-prep
Date: 2026-09-18
KiCad: 10.0.6 (`kicad-cli`)
Java 21: Homebrew OpenJDK 21.0.12.1 (cannot load the 2.4.1 jar)
Java 25: Homebrew OpenJDK 25.0.4.1 `/opt/homebrew/opt/openjdk@25/bin/java`
Final commit: `edf612faa1019002471188a6b01b6598676d72a9`

## What was built

`git merge main` first (`68f38ba`). Conflict in `tests/test_board_release.py` kept both sides: review r6 `routed: false` / `refused` and WP12c `pcb_tracks == 0`.

Freerouting 2.4.1 jar at `/tmp/wp12d/freerouting-2.4.1.jar` (GitHub release v2.4.1, Q46 free). Class file version 69. Java 21 fails to load it. Java 25 runs L8 §3 flags (`--gui.enabled=false -de -do -mp 5 -mt 4`). SES written. Not imported. Board file byte-for-byte unchanged (`494283e3…`).

`hardware/board/placement_table.py` parses a packing markdown table with `side` `top`/`bottom`. `build_v2b.py` `apply_placement_row` Flips bottom rows with KiCad `Flip(pos, False)`. Synthetic two-row test does not load the PCB.

`route.md` §6–§7: proof table and the ten-line WP12d plan (Q79, Q80). `board-v2.md` §15 only.

Nothing ordered, quoted or uploaded. No vendor contact. SES stays under `/tmp/wp12d/`.

## Gates

### 1. Unittest (this package)

```text
.venv/bin/python -m unittest tests.test_board_release -v
```

Result: **OK** (7 tests), including the two-row side-column test.

```text
.venv/bin/python -m unittest discover -s tests -v
```

Result: 209 tests, **14 FAIL**, all `test_cad` (v1 regen hashes and `test_two_consecutive_shell_runs_are_identical`). This package does not own CAD.

### 2. Board file unchanged

```text
git diff --stat -- hardware/board/*.kicad_pcb
```

Empty. SHA-256 `494283e31725e58eea29325d8fb9fd20cb98c3f58973b27d46b904fbd69e2f34`.

### 3. `release.py` without `--routed`

```text
.venv/bin/python scripts/board/release.py --board-dir hardware/board --out /tmp/wp12d-release
```

Exit **0**. `routed: false`. `pcb_tracks: 0`. ERC 0. BOM 59 = placed 59. CPL 59.

### 4. `git status --short`

Empty after the commit.

## Plan §9 / brief deliverables

| Item | Result |
|---|---|
| Merge main, keep both sides | `68f38ba` |
| Freerouting 2.4.1 writes SES | Yes, on OpenJDK 25. Java 21 cannot load the jar. |
| SES imported | **No** (evidence only) |
| Two-sided `side` column | Parser + `apply_placement_row`; synthetic test green |
| §5b column match | `face` `top`/`bottom` aliases `side`; `pocket`/`floor` stay top |
| Q79 / Q80 ten-line plan | `route.md` §7 |
| Copper committed | None |

## What was not done

- Place or route on packing §5c (WP11d has not published it).
- Import the SES.
- DRC 0.

## Needs a decision

1. L8 §3 says 2.4.1 runs on Java 21. The GitHub `freerouting-2.4.1.jar` is class 69 and needs OpenJDK 25. WP12d should use `/opt/homebrew/opt/openjdk@25/bin/java`.
2. `kicad-cli pcb export` still has no `specctra`; DSN stays pcbnew.

## route.md §6–§7 (paste)

## 6. Freerouting 2.4.1 headless proof (WP12d-prep)

Jar: `/tmp/wp12d/freerouting-2.4.1.jar` from
https://github.com/freerouting/freerouting/releases/tag/v2.4.1 (Q46: free;
Rolf may veto). Manifest Build-Date 2026-09-03, Main-Class
`app.freerouting.Freerouting`, class file version 69 (Java 25).

`kicad-cli pcb export` still has no `specctra` subcommand. DSN for this run
is pcbnew `ExportSpecctraDSN` → `/tmp/wp12d/elicio-v2.dsn` (58492 bytes).

Java 21.0.12.1 (`/opt/homebrew/opt/openjdk@21/bin/java`) **does not load**
the 2.4.1 jar:

```text
Error: LinkageError occurred while loading main class app.freerouting.Freerouting
	java.lang.UnsupportedClassVersionError: app/freerouting/Freerouting has been compiled by a more recent version of the Java Runtime (class file version 69.0), this version of the Java Runtime only recognizes class file versions up to 65.0
```

Java 25.0.4.1 (Homebrew `openjdk@25`, keg-only,
`/opt/homebrew/opt/openjdk@25/bin/java`) does. L8 §3 flags, pass count
bounded to 5:

```text
/opt/homebrew/opt/openjdk@25/bin/java -jar /tmp/wp12d/freerouting-2.4.1.jar \
  --gui.enabled=false \
  -de /tmp/wp12d/elicio-v2.dsn \
  -do /tmp/wp12d/elicio-v2.ses \
  -mp 5 \
  -mt 4 \
  --router.job_timeout=00:08:00
```

| Item | Result |
|---|---|
| Version | Freerouting v2.4.1 (build-date: 2026-09-03) |
| Wall time | 39.52 s (`time` real; job elapsed 37.21 s) |
| SES | **yes** `/tmp/wp12d/elicio-v2.ses` |
| SES size | 14531 bytes |
| Track count | 60 `(wire` / 60 `(path`; 19 `(via` |
| Unrouted after 5 passes | 80 nets, 148 violations (placement still collides) |
| stderr / log | Polyline warnings; then `Successfully saved output file` |
| Import | **not done** (evidence only) |

The committed `elicio-v2.kicad_pcb` is unchanged.

## 7. WP12d plan (Q79, Q80)

1. Place from packing §5c; parser already reads `ref u s rot side` (`top`/`bottom`).
2. R1, R2, R3 sit on the island at the tab roots (Q79 variant A).
3. Each 2.5 mm tab carries one Contact trace and nothing else.
4. Keep netclass Contact 1.0 mm; no DRC exception.
5. J1 USB-C stays on the hook-end face (Q80, plan v2 §5.4).
6. J4 TC2030 sits on the leftover; its keep-out is a board no-part zone.
7. J3 pads are Ø1.5 mm.
8. Export DSN with pcbnew (`kicad-cli` has no specctra).
9. Run Freerouting 2.4.1 on OpenJDK 25 with `--gui.enabled=false -de -do -mp -mt`.
10. Import the SES only after §5c is pinned; then DRC and hand-fix residue.
````

### WP12d (lane w2)

````markdown
# WP12d report — board v2d no-receptacle, width 22, two-sided, route to DRC 0 (lane w2)

Worktree: `/home/user/projects/elicio/.worktrees/w2`
Branch: `lane/w2`
Package: WP12d
Pane: `w1B:pB`
Date: 2026-09-18
KiCad: 10.0.6 (`kicad-cli`)
Java: Homebrew OpenJDK 25.0.4.1 (`/opt/homebrew/opt/openjdk@25/bin/java`)
Jar: `~/.local/opt/freerouting/freerouting-2.4.1.jar`
§5c final: `c6bd2fec1e10050b1f9f9261fc9d54086d8ad3cf` (lane/w3, packing-v2.md only; not merged)
Final commit: `1e055de640ccc918e02a12d2bd5e326fabeafcc2`

## What was built

`git merge main` already at `f435a3f`. Schematic Q81 at `fcaa6d4` (J1/U5 out, P4/P5 RING_PAD, D1 PESD on VBUS, nRF USB D+/D− no-connect, ERC 0).

Did **not** merge `c6bd2fe`. That commit only edits `docs/fab/packing-v2.md`, which this lane does not own. The second §5c pin table was copied into `hardware/board/packing_5c_norec.md` and the land was rebuilt.

Place: 66 table parts + H1/H2 = 68 footprints. 38 flipped to B.Cu. P4 (0.75, 44.00) CHARGE_VBUS, P5 (21.25, 44.00) CHARGE_GND, RING_PAD_D5_H2.7. Holes (13.45, 17.70) and (17.95, 17.70). Neck-end strips SIG1 10.71 mm, SIG2 21.81 mm. R1–R3 on the island. J3 pads Ø1.5. Contact class 1.0 mm kept. Tracks 0.

Outline nudges (no part moved), recorded in `hardware/board/route.md` §8: pocket SW1 u 20.40; `HANG_U1` 33.20; `HANG_S1` 26.70 so J3 pad 3 meets copper-to-edge 0.30. After that, copper-edge errors are 0.

Freerouting 2.4.1 on OpenJDK 25 (`--gui.enabled=false -mp 8 -mt 4`, 75.86 s) wrote `/tmp/wp12d/elicio-v2.ses` (22813 bytes). Import on a copy: 275 tracks, 17 vias, **374** DRC errors (was 56). Same 11 P2-vs-U1 shorts. SES **not** written to the owned PCB.

Step 5: stop **un-shorted**, `routed: false`. Last commit message is the brief's `board(v2d): … routed` line; the copper is not routed.

`scripts/board/release.py` was not edited. `firmware/src/board_pins.h` was not edited: it has no USB D+/D− symbols; the sheet now no-connects those nRF pins. Lane w4 owns the header.

Nothing ordered, quoted or uploaded. No vendor contact.

## Gates

### 1. Unittest (this package)

```text
.venv/bin/python -m unittest tests.test_board_release -v
```

Result: **OK** (7 tests). ERC 0. BOM rows = placed parts = 57. `"routed": false` without `--routed`. `--routed` refused (`drc_errors` 56, `unconnected_items` 146, `no_tracks` 1). `pcb_tracks` = 0. Named SMT centres within 0.1 mm of `packing_5c_norec.md`. P4/P5 present. J1/U5 absent. H1/H2 at the Q82 sites.

```text
.venv/bin/python -m unittest discover -s tests -v
```

Result: 209 tests, **14 FAIL**, all CAD, this package does not own:

- `test_cad.CadRegenTests.test_reference_regen_matches_committed_hashes` × 13 (`body_full_p15` 3mf/step/stl, `body_full_p25` 3mf/step/stl, `body_thin_p15` 3mf/step/stl, `lid` 3mf/step/stl, plus one more hash row)
- `test_cad.CadShellV2BuildTests.test_two_consecutive_shell_runs_are_identical`

Same 14 as WP12d-prep. `[cad]` extras were not installed.

### 2. ERC

```text
kicad-cli sch erc --format json
```

**0 errors, 0 warnings.**

### 3. DRC (owned PCB, 0 tracks)

```text
kicad-cli pcb drc --format json
Found 56 violations
Found 146 unconnected items
  23 clearance
  15 solder_mask_bridge
  11 shorting_items
   7 hole_clearance
```

Paste and first structural reason: `hardware/board/route.md` §8 and `docs/fab/board-v2.md` §15.

### 4. `release.py`

Without `--routed`: exit **0**. `routed: false`. BOM 57, CPL 57, Gerbers and STEP written.

With `--routed`: exit **1**. `routed release refused: {"drc_errors": 56, "unconnected_items": 146, "no_tracks": 1}`.

### 5. `git status --short`

Empty after the last commit. Post-commit hook pushed `lane/w2` (not a manual push).

## Plan §9 / brief deliverables

| Item | Result |
|---|---|
| Schematic Q81 | `fcaa6d4`. J1/U5 out. P4/P5 in. D1 stays on VBUS. USB D+/D− NC. ERC 0. |
| Outline width 22, chord 47.90 | Island u 2.25–19.75, s 16.00–37.60. Neck-end strips. Holes at Q82 sites. |
| Place from §5c final | Table `c6bd2fe`. 68 footprints. Centres match within 0.1 mm. |
| Zero-track DRC 0 apart from unconnected | **No.** 56 errors. Copper-edge 0 after hang nudge. |
| Route Freerouting 2.4.1 OpenJDK 25 | SES yes. Copy DRC 374. Discarded. |
| DRC 0 / 0 unconnected / `--routed` exit 0 | **Fail.** Step 5. |
| Contact 1.0 mm, one trace per tab, J3 Ø1.5 | Class kept. No tab copper. J3 Ø1.5. |
| `board-v2.md` §3/§4/§12/§15 | Updated. §15: 56 errors, `routed: false`. |
| `route.md` §8 | Run log, DRC list, nudges, first structural reason. |
| Last commit message | `board(v2d): no-receptacle BOM, width 22, placed on two sides from §5c, routed` at `1e055de`. |

## First structural reason

P2 RING_PAD PTH at **(10.40, 33.10)** sits inside U1 at **(8.00, 29.35)** courtyard 11.50 × 16.50. Eleven pad-to-pad shorts on F.Cu (SIG2 vs U1 pads 27, 29, 35–43). A router cannot separate stacked pads. Packing treats P2 as `floor` and U1 as `top`; on this 2-layer flex they share (u, s).

Second: Contact 1.0 mm vs R1–R3 0402 pad gap 0.48 mm. Third: J4 NPTH vs leftover B.Cu 0402 (R5, R6, R18, R19, R21, R22).

## What was not done

- DRC 0, 0 unconnected, `release.py --routed` exit 0, `routed: true`.
- SES copper on the owned PCB (copy was worse).
- Hand-fix residue on committed copper (no route to keep).
- Merge of `c6bd2fe` (packing file not owned).
- Edit of `firmware/src/board_pins.h` (USB D+/D− already absent there).
- Edit of `scripts/board/release.py`.

## Needs a decision

1. **P2 vs U1** — packing must move the SIG2 ring off the module courtyard, or the board cannot be a 2-layer flex at those XY. Until then DRC 0 is unreachable.
2. **Contact 1.0 mm vs 0402** — pad gap 0.48 mm. Isolation cannot meet the netclass without a different land or a different clearance.
3. **J4 leftover vs B.Cu 0402** — NPTH hole clearance vs R5/R6/R18/R19/R21/R22. Packing leftover keep-out vs second-side parts.

## GPIO note (w4)

Schematic: nRF USB D+/D− are no-connect (Q81, unused USB). `firmware/src/board_pins.h` has no USB pin macros. Not edited.

## Commits

| SHA | Message |
|---|---|
| `fcaa6d4` | `board(v2d): drop USB-C J1/U5; add tail charge pads P4/P5` |
| `2cffd4e` | `board(v2d): width-22 outline and two-sided place from §5c` |
| `80b4c04` | `board(v2d): re-pin from §5c final c6bd2fe` |
| `1e055de` | `board(v2d): no-receptacle BOM, width 22, placed on two sides from §5c, routed` |
````

### WP12e (lane w2)

````markdown
# WP12e report — Contact by area, pin table v2 flat pattern, route to DRC 0 (lane w2)

Worktree: `/home/user/projects/elicio/.worktrees/w2`
Branch: `lane/w2`
Package: WP12e
Pane: `w1B:pB`
Date: 2026-09-18
KiCad: 10.0.6 (`kicad-cli`)
Java: Homebrew OpenJDK 25 (`/opt/homebrew/opt/openjdk@25/bin/java`)
Jar: `~/.local/opt/freerouting/freerouting-2.4.1.jar`
Pin table v2: `408a476` (`git show 408a476:docs/fab/packing-v2.md` §5d)
Final commit: `30ca79d7b31b834c7096a88c8f31f83b125f40f3`

## What was built

`git merge origin/main` first (Q86 on main). Pin table v2 copied to `hardware/board/packing_v2_flat.md`. Folded-site table omitted. `packing_5c_norec.md` deleted.

Parser: flat `u,s` (or `x,y`) plus side; skip folded (`pad`/`y` without `rot`); J4 keep-out `keep` column is diameter Ø1.39; `F.Cu and B.Cu` forbids B.Cu.

Place: 66 table parts + H1/H2 = 68 footprints. 38 flipped to B.Cu. Flat rings P1 (5.90, 5.29), P2 (10.40, −5.81), P3 (8.50, 43.00), P4 (37.47, 2.80), P5 (30.05, 5.80). CHARGE rectangle centre (33.02, 4.30) 14.50 × 8.60 is Edge.Cuts. SIG1/SIG2 `tab_detour` from s=16.00 toward −s. REF tab from s=37.60. J4 NPTH keep-out Ø1.39 on B.Cu at the KiCad hole centres. Q84 `tabs` / `tail_pads` (CHARGE in `tail_pads`). Tracks 0.

Hole nudges inside 0.1 mm: R23 +0.09 u, R26 −0.05 u. R24 not moved (needs 0.46 mm).

Freerouting 2.4.1 on OpenJDK 25 (`--gui.enabled=false -mp 8 -mt 4`, 75.47 s) wrote `/tmp/wp12e/elicio-v2.ses` (22585 bytes). Import on a copy: 268 tracks, 12 vias, **317** DRC errors (was 2). Shorts 0. SES **not** written to the owned PCB.

Step 5: stop **un-shorted**, `routed: false`. Last commit: `board(v2e): placed on the flat pattern, not routed`.

`scripts/board/release.py` was not edited. `firmware/src/board_pins.h` was not edited.

Nothing ordered, quoted or uploaded. No vendor contact.

## Gates

### 1. Unittest (this package)

```text
.venv/bin/python -m unittest tests.test_board_release -v
```

Result: **OK** (14 tests). ERC 0. BOM rows = placed parts. `"routed": false` without `--routed`. `--routed` refused (`drc_errors` 2, `unconnected_items` 146, `no_tracks` 1). `pcb_tracks` = 0. Named SMT centres within 0.1 mm of `packing_v2_flat.md`. P4/P5 at (37.47, 2.80) and (30.05, 5.80). J1/U5 absent. H1/H2 at the Q82 sites. Q84: no Contact-clearance on R1–R3.

```text
.venv/bin/python -m unittest discover -s tests -v
```

Result: **14 FAIL**, all CAD, this package does not own:

- `test_cad.CadRegenTests.test_reference_regen_matches_committed_hashes` × 13 (`body_full_p15` 3mf/step/stl, `body_full_p25` 3mf/step/stl, `body_thin_p15` 3mf/step/stl, `lid` 3mf/step/stl, plus one more hash row)
- `test_cad.CadShellV2BuildTests.test_two_consecutive_shell_runs_are_identical`

Same 14 as WP12d. `[cad]` extras were not installed.

### 2. ERC

```text
kicad-cli sch erc --format json
```

**0 errors, 0 warnings.**

### 3. DRC (owned PCB, 0 tracks)

```text
kicad-cli pcb drc --format json
Found 2 violations
Found 146 unconnected items
   1 hole_clearance
   1 solder_mask_bridge
```

Both: Pad 2 [GND] of R24 on B.Cu vs J4 NPTH. Copper-edge 0. Shorts 0.

Paste and first structural reason: `hardware/board/route.md` §9 and `docs/fab/board-v2.md` §15.

### 4. `release.py`

Without `--routed`: exit **0**. `routed: false`. Gerbers, BOM, CPL, STEP written.

With `--routed`: exit **1**. `routed release refused` on DRC errors, unconnected items, and no tracks.

## What was not done

DRC 0 and 0 unconnected were not reached. `--routed` with `routed: true` was not released. Gerbers/BOM/CPL exist from the non-`--routed` job only. One Contact trace per tab was not routed (no tracks).

## Needs a decision

Pin table v2 J4 keep-out XY (pair at s=27.14) does not match KiCad Tag-Connect TC2030 at (16.25, 24.60) rot 90 (pair at s=22.06). R24 on B.Cu sits on the real hole at (17.266, 22.06). Clearing it needs 0.46 mm, past the 0.1 mm pin. Packing (or a J4 rotation that matches the table) must keep B.Cu pads out of the KiCad hole sites before a router can reach DRC 0.

## First structural reason

R24 pad 2 [GND] on B.Cu occupies J4 NPTH. Stop un-shorted. `routed: false`.
````

### WP12f (lane w2)

````markdown
# WP12f report — route pin table v2 to DRC 0 (lane w2)

Worktree: `/home/user/projects/elicio/.worktrees/w2`
Branch: `lane/w2`
Package: WP12f
Pane: `w1B:pB`
Date: 2026-09-18
KiCad: 10.0.6 (`kicad-cli`)
Java: Homebrew OpenJDK 25.0.4.1 (`/opt/homebrew/opt/openjdk@25/bin/java`)
Jar: `~/.local/opt/freerouting/freerouting-2.4.1.jar`
Pin table v2: `408a476`
Final commit: `fbd56e648bc0aa704615a6cd8420e1b431b69769`

## What was built

`git merge origin/main` first (`8d3a2ac`, briefs WP12f/WP11f and Q87).

R24 moved +0.47 mm u (Q87). R23 +0.09 mm u and R26 −0.05 mm u stay inside 0.1 mm. Zero-track DRC **0 errors**, 146 unconnected, 0 shorts.

Netclasses set to JLC 1 oz flex §12: Default track/clearance 0.10/0.10 mm, Contact 0.15/0.20 mm, via 0.70/0.30 mm. DSN (`scripts/board/route_v2.py --dsn-check`):

```text
(via "Via[0-1]_700:300_um")
(width 100)
(clearance 100)
(class kicad_default … (width 100) (clearance 100))
(class Contact REF SIG1 SIG2 (width 150) (clearance 200))
```

WP12e 199 `track_width` (min 0.2000 mm, actual 0.1000 mm): the DSN already had 100 µm. SES import leaked Contact onto Default unless `elicio-v2.kicad_pro` sits next to the copy. `import_ses` restores §12 and clamps necks below 0.10 mm. `sanitize_dsn` drops `(clearance 25 (type smd_smd))`.

Locked stubs (7 tracks, Specctra `type fix`): SIG1/SIG2/REF along strip centres to s=15.50 / 37.95 (1.0 mm before L1/D2); VBUS/GND along the CHARGE tab to u=26.27. Island manhattan to R1–R3 was not locked (Q84, shorts, crossings). Foreign-net keep-outs on the strips (`allow_tracks` so the locked nets stay).

Freerouting 2.4.1 on OpenJDK 25, fanout 40 passes, 126/230 SMD pins escaped (**54.8 %**, above 49 %), 12 auto-route passes, 1 m 48 s, SES 33305 bytes, 60 unrouted / 25 router violations. Copy import with project file: 444 tracks, 37 vias, 12 DRC, 60 unconnected, 0 shorts, 0 foreign nets in the strips. Copy without `.kicad_pro`: 204 errors. SES **not** written to the owned PCB.

Owned PCB: 7 locked stubs, 5 `track_dangling` warnings, 0 DRC errors, 146 unconnected, 0 shorts. `routed: false`.

Last commit: `board(v2f): R24 off the hole, not routed`.

`scripts/board/release.py` was not edited. Firmware was not edited. `docs/fab/plan-v2.md` and `docs/fab/open-questions.md` were not edited.

Nothing ordered, quoted or uploaded. No vendor contact.

## Gates

### 1. Unittest (this package)

```text
.venv/bin/python -m unittest tests.test_board_release -v
```

Result: **OK** (15 tests). ERC 0. BOM rows = placed parts. `"routed": false` without `--routed`. `--routed` refused on `unconnected_items` 146. `pcb_tracks` > 0. R24 within 0.50 mm of the table (Q87). Other named SMT centres within 0.1 mm of `packing_v2_flat.md`. DSN class-check unit test green.

```text
.venv/bin/python -m unittest discover -s tests -v
```

CAD-related modules: **14 FAIL**, this package does not own:

- `test_cad.CadRegenTests.test_reference_regen_matches_committed_hashes` × 13 (`body_full_p15` 3mf/step/stl, `body_full_p25` 3mf/step/stl, `body_thin_p15` 3mf/step/stl, `lid` 3mf/step/stl, plus one more hash row)
- `test_cad.CadShellV2BuildTests.test_two_consecutive_shell_runs_are_identical`

Same 14 as WP12e. `[cad]` extras were not installed.

### 2. ERC

```text
kicad-cli sch erc --format json
```

**0 errors, 0 warnings** (from the release job in the board tests).

### 3. DRC

Zero-track (R24 moved, `--no-pre-route`):

```text
kicad-cli pcb drc --format json
Found 0 violations
Found 146 unconnected items
```

Owned PCB (locked stubs, SES discarded):

```text
kicad-cli pcb drc --format json
Found 5 violations
Found 146 unconnected items
types: track_dangling × 5 (severity warning)
shorts 0
```

Paste and first structural reason: `hardware/board/route.md` §10 and `docs/fab/board-v2.md` §15.

### 4. `release.py`

Without `--routed`: exit **0**. `routed: false`. Gerbers, BOM, CPL, STEP written.

With `--routed`: exit **1**. `routed release refused` on unconnected items (146). DRC errors 0 (dangling is a warning).

## What was not done

DRC 0 errors and 0 unconnected were not reached together. `--routed` with `routed: true` was not released. Island legs from the rings to R1–R3 were not locked (Q84). SES copper was not imported into the owned PCB.

## Needs a decision

Q84 1.0 mm on `tabs` versus L1 (0.70 mm from SIG1 attach), D2 (0.60 mm from SIG2 attach), and U1 pad 26 (0.90 mm from REF attach). Packing must keep those parts off the 1.0 mm tab creepage, or Q84 must stop at the ring copper only. R24 +0.47 mm u is a Q87 deviation for packing to fold back (WP11f).

## First structural reason

Q84 1.0 mm on the tab roots leaves no legal path from the locked ring stubs onto the island. Stop un-shorted. `routed: false`.
````

