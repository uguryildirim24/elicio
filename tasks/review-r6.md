# Code review + fix — Phase 1 round 6 (WP14, WP11b, WP12b, WP13b, WP15, WP17b) on branch review/r6 (Claude Opus 5, high)

You are the reviewer for this round, herdr agent `rev6`. Six lanes
finished six packages under plan v2 (signed off at `ef369bd`). You merge
them into one candidate, inspect it, **fix what is wrong yourself**, run
every gate, and write one verdict. You never push by hand (the repo's
post-commit hook pushes every commit), never merge into `main`, never
touch another worktree, never edit `docs/fab/plan.md`, `docs/fab/plan-v2.md`
or `docs/fab/open-questions.md`. No purchase, sign-up, quote request,
upload or vendor contact; web only to re-read a page a lane cites. No
Agent-tool subagents. Rolf is asleep; nothing waits on him.

Worktree `/home/user/projects/elicio/.worktrees/review`, branch
`review/r6` from `main`. Private environment inside this worktree:
`python3.13 -m venv .venv && .venv/bin/python -m pip install -e '.[cad]'`
plus `-e '.[ble]'` once lane w4's extra is merged. KiCad 10 (`kicad-cli`),
`arduino-cli` with the Adafruit nRF52 core, and matplotlib are on this
Mac; install nothing else.

Start line (the coordinator restarts you by copy-paste):

    herdr agent start rev6 --kind claude --pane <pane> --parent w1B:p1 -- --model claude-opus-5 --effort high --dangerously-skip-permissions

## Steps

1. Read `tasks/phase1-common.md`, `docs/fab/plan-v2.md` (§3, §4, §5, §6,
   §7, §8, §9, §11), `docs/fab/open-questions.md` Q50 to Q68, the round 5
   verdict `tasks/reviews/code-r5.md` (its decisions 57 to 68 bind this
   round), the briefs `tasks/WP14-shell-v2.md`, `tasks/WP11b-packing-followups.md`,
   `tasks/WP12b-board-route.md`, `tasks/WP13b-receiver.md`,
   `tasks/WP15-sheets-v2.md`, `tasks/WP17b-research-v4.md`, and the
   coordinator notes quoted under each report below.
2. Merge, in this order, resolving conflicts yourself: `lane/w3`
   (WP11b), `lane/w1-r6` (WP14; NOT `lane/w1`, which is round 5's branch
   with 109 MB of drawings and stays out of history, Q56), `lane/w5`
   (WP17b), `lane/w4` (WP13b), `lane/w9` (WP15), and `lane/w2` **at
   commit `480e355` exactly** (`git merge 480e355`), because lane w2
   keeps working on `lane/w2` after that commit (WP12c, routing the
   copper) while you review. Each lane's diff against `main` shows
   `HANDOFF.md` and `HANDOFF.json` as changed only because `main` moved
   after the lanes branched; keep `main`'s.
3. Gates, all on the merged tree:
   - `.venv/bin/python -m unittest discover -s tests -v` passes with the
     CAD, render, placement, shell v2, sheets, receiver, frame_v2 native
     harness and board-release tests running, not skipped; report count
     and skips.
   - Order 1 untouched: reference build twice, solids identical to each
     other and to `docs/fab/cad/v1/`; `render.py` twice identical; the v1
     `manifest.json` byte-identical to `main`'s.
   - Stage B v2 (`stageb_v2.toml`) built twice by the README command into
     a temp dir: byte-identical; still exit 3 on Q59 only (the shell path
     carries the slot, the Stage B path does not; say so in the verdict).
   - Shell v2 (`shell_v2.toml`, `STAGE=shell`) built twice: byte-identical
     to each other and to `docs/fab/cad/v2/`; exit 0; every check a number
     or NOT_MEASURED by name; `manifest.py --check-bytes` ok.
   - `scripts/board/release.py` (without `--routed`) exits 0: ERC 0,
     BOM rows = placed parts, outputs present; with `--routed` it is
     REFUSED on this candidate and the test asserts that refusal (WP12b
     did not reach DRC 0: 1290 errors, 31 unconnected, a shorting bus
     fallback; routing is WP12c on lane w2, in parallel). The
     placement-agreement test reads both the PCB and `packing-v2.md` §5.
   - `arduino-cli compile --fqbn adafruit:nrf52:feather52840 --library
     firmware --output-dir <tmp> firmware/elicio_stream` exits 0; the
     `board_pins.h` map equals `board-v2.md` §9 after the merge.
   - `scripts/sheets/template.py` twice byte-identical and equal to the
     committed PDF and SVGs.
   - `elicio receive --simulate-live` runs without a radio and
     `receive-check` on its output exits as the test expects.
   - `git diff main -- docs/fab/plan.md docs/fab/plan-v2.md
     docs/fab/open-questions.md docs/fab/interface.md docs/fab/contacts.md
     docs/fab/cad/v1/` is empty.
   - `git count-objects -vH` growth over `main` under 12 MB (the shell
     outputs are about 5.5 MB); report the number.
4. Adversarial review: the seams below first, then the attack points.
   Build the shell and cut sections through the standoff pockets, the
   REF slot, the USB wall and a snap before trusting any check; open the
   routed board in `kicad-cli` exports (or `pcbnew` if you must) and look
   at the ring pads, the tabs and the antenna keep-out.
5. Fix every defect yourself, in separate commits on `review/r6` with
   messages starting `review(WPn):`. Do not run `git push`.
6. What cannot be fixed without changing plan v2 goes under "Needs a
   decision", numbered from 69.

## Seams

- **One packing truth, again.** WP11b regenerated `packing-v2.md` on
  `lane/w3` (§1b DTP arc-plus, §1c Jauch, §1d bigger box, §5 the REF tab
  route table with `REF_end_wall_slot`). WP14 read the slot numbers from
  `lane/w3` and cut them; WP12b placed from §5. After the merge all three
  must agree on the same numbers: the slot (u 7.25–9.75, s 38.20–39.25,
  y 1.50–1.81), the winner's contact sites, the board outline, the tab
  exits. Where they differ the solid wins and the others move, or it is
  a decision.
- **The cell.** WP17b §2 found no 501015-class cell in ones at any
  distributor; WP11b §1b–§1d showed the two distributor cells (DTP301120
  22 mm, Jauch LP501218JH 20 mm) fail on length in every body up to 22
  wide and 11.5 outer. WP17b §7 then found that a 501015 pack WITH its
  protection board is 17.0 mm long on the manufacturers' sheets (DNK,
  Benzo), so the plan's 15.6 × 10.4 × 5.2 envelope is a bare cell, and
  the only packs under 16 mm are marketplace listings (501012 at
  13.0 × 10.1 × 5.1 with PCM, 40 mAh, eBay and AliExpress; the "includes
  PCM" statements there are partly the lane's inference, check which are
  quotes). WP11b §1e then ran the real packs: the winner body with the
  17.0 mm 501015 pack does NOT close (`BQ25100 overlaps header`; at
  +1.5 mm of arc the overlap clears and only the M1 gate fails, 49.42
  against 49.00 at the default M1 52, so a measured M1 of 52.5 or more
  would open that route); the 501012 pack closes on 8 bodies, smallest
  `A_pack501012_series_w19_y8_iII_s3`, TOTAL_CHORD 47.90, outer 9.0.
  Coordinator reading for this round, which you check rather than
  re-decide: the shell and board stay on the w20 × y8 body as built;
  the cell envelope the record carries becomes the 501012 pack
  (13.0 × 10.1 × 5.1 with PCM) in the w20 × y8 pocket, which is longer
  than needed (confirm from §1e that w20 y8 s3 is among the eight
  closers, and that the shell's pocket, the foam rule Q57 and the board's
  cell connector position accept a 13.0 mm pack without a change; if
  they do not, that is a defect to fix in the packing table and the
  shell, not a decision). State as decision 69: the cell purchase route
  is Rolf's (a marketplace pack without a drawing, plan v2 R2 and §9 say
  page price, stock and drawing; or a manufacturer sample of the 17 mm
  501015 pack with M1 ≥ 52.5 and a body 1.5 mm longer, which re-opens the
  shell and the board). Do not pick a cell yourself and do not order one.
- **Shell §7 look.** Plan v2 §7 is Rolf's "would not look out of whack if
  I wore it outside". Judge the two renders against it: outside edges
  R ≥ 1.0 (the lane says the hook joint fillet failed in OCCT), the tail's
  corners, the lid crown 0.305 against "continuous curvature", the
  medial face flat. Fix what the kernel allows in the construction path
  (one path, no fork; round 4 rule), regenerate the outputs, and say in
  the verdict what still reads as a printed block.
- **Standoff pocket versus the brass part.** WP14 prints the hex well at
  6.3 across flats plus Ø7.4 against the standoff's 5.0 across flats
  (Harwin DRG-01991 5.00 max; DigiKey lists 5.50). A captive hex needs a
  clearance the printer can hold (JLC3DP MJF tolerance page, quoted in
  L6/L7), not a guess; compute it, apply it, and put the datum chain in
  `shell-v2.md` §3 and `board-v2.md` §11 with the same numbers (G7 joint
  drawing inputs).
- **Routing is not yours.** Do not edit copper, vias or zones in
  `hardware/board/elicio-v2.kicad_pcb`, nor `hardware/board/maze_route.py`,
  `hardware/board/build_v2b.py`, nor `board-v2.md` §15: lane w2 is
  rewriting exactly those on `lane/w2` after `480e355` (WP12c) and a
  conflict costs a round. Record the state in the verdict: WP12b's last
  commit message says "routed, released" and the branch is neither; the
  `summary.json` field `routed: true` on a refused release is a defect in
  `release.py`'s reporting (fix the script and its test so the flag is
  false whenever the release is refused). Footprints, pads, keep-outs,
  rules in the `.kicad_pro`, the schematic, the BOM and the docs outside
  §15 are yours to fix.
- **Board placement from the packing.** WP12b's PCB must match §5 within
  0.1 mm by a test that reads both. The tabs are drawn flat and fold at
  the site; the fold geometry (tab length from board edge to ring centre,
  bend radius R 1.5 from `board-v2.md` §11) must be the same number in
  the PCB, the packing table and the shell's channel.
- **BOM from L7.** WP17b §4 resolved codes the coordinator passed to
  WP12b (U2 `C134015`/`C2841443`, U4 `C132291`, J2 `C160402`, 0402
  passives). Verify on the pages what you can today, keep UNVERIFIED
  where the quote is not on the page, and check that `board-v2.md` §13
  cites L7 by section rather than restating.
- **Probe and REGOUT0.** L7 §1 says the nRF52840 GPIO absolute maximum is
  VDD + 0.3 V and lists three VTref-sensing probes with prices. Verify the
  product specification sentence and one probe page. `board-v2.md` §4,
  `assemble.md`'s first-load section and `order-parts.md`'s conditional
  kit must say the same thing: no purchase until G4 names the kit (Q64),
  the Raspberry Pi Debug Probe is not it for an erased part.
- **Receiver and montage.** WP13b's `receive-check` fails on the montage
  §8 dropout rule but not on lines 3.5–3.10 unless scored; read montage
  §8's table and make the tool match the table's "same criterion"
  column; if the table is ambiguous, that is a decision, not a guess.
  `board_pins.h` follows `board-v2.md` §9 after WP12b's merge (w4 checked
  w2's branch mid-round; check again).
- **Rolf's sheets against the round.** WP15 wrote "the agent fills this
  after WP12b/WP14" where numbers were missing. After the merge, fill
  every field the merged tree now settles (file names under
  `docs/fab/cad/v2/`, release folder contents, stiffener count, slot,
  closure step, colour options from L7 §5) and leave the rest marked.
  The sheets must still contain no question and no number without a
  source; `grep -n "owner\|the user"` finds nothing new.
- **pyproject.toml.** w4 added the `ble` extra; w9 installed matplotlib
  without editing it although `template.py` imports it; w3's and w1's
  tests need `.[cad]`. Make the extras honest (a `sheets` extra or fold
  matplotlib into `cad`) and make the tests consistent: a test that
  needs an extra skips by name with the extra named, and the verdict
  lists the skip count per extra; on your full `.[cad]` + `.[ble]` venv
  nothing skips.
- **Record once.** Decisions 57 to 68 are in `open-questions.md` (not
  yours); `docs/EARPIECE_DESIGN.md` should point at them once. Anything
  WP14, WP12b or WP15 restates is trimmed to a pointer.
- **Rolf, never "owner" or "user"**, in every new prose file.

## Attack points per package

- **WP14**: every V2_* check re-derived from your own section cuts
  (pocket depth = standoff + ring 0.31, boss tops 0.5 below standoff tops,
  slot wall ≥ 1.0 beside the slot, USB ligaments 1.5, switch membrane
  0.5); the snap strain 0.0117 recomputed from the beam numbers and the
  PA12 modulus the lane cites (or NOT_MEASURED if no modulus source);
  the hook ellipse axes from M8's default; `render.py` labels match the
  solid; the manifest's `provisional: true` and Q34 pointer; two
  consecutive builds identical; no per-run files; Stage B v2 untouched.
- **WP11b**: the arc-plus and bigger-box runs use the round 5 conflict
  logic unchanged (diff `layout_conflicts`); the REF route search's wall
  model (cavity end at s 38.20, pocket at 39.25) equals the solid's; the
  Jauch dims include the PCM (L7 §2's quote); `packing-v2.md` regenerated
  not edited (the test); `--all` still writes closers only.
- **WP12b**: the 13 `CadRegenTests` failures the lane reports in its
  venv, again (round 5 traced them to the lane's build123d pins; confirm
  on your `.[cad]` venv that order 1 matches on the merged tree and say
  which pins); DRC rules encode JLC's FPC page numbers (quoted, dated);
  contact nets clear of other copper by the rule the lane could actually
  meet (it says 1.0 mm is not possible on a 2.5 mm tab with the 220 kΩ
  on it; check the number and the reasoning, decide the rule in the
  `.kicad_pro`, tell WP12c through the verdict); nothing under the module
  keep-out; ADS
  decoupling 10 µF + 0.1 µF per supply at the pins; the standby-load sum
  against the BQ25100 termination floor with the sheet's sentences (L7
  §4); stiffener count ≤ 3 and legend; release outputs match JLC's FPC
  upload list; every BOM line LCSC-numbered with date and stock or
  UNVERIFIED; G7 inputs in §11 with the ring capture under the standoff.
- **WP13b**: every `frame-v2.md` case through the receiver with an
  asserted outcome; the session file loads through the named pipeline
  loader; reconnect and reorder paths exercised by the fake transport;
  `bleak` imported lazily so the tests need no radio; `receive-check`'s
  exit code table documented in `receiver-v2.md`.
- **WP15**: each step of `assemble.md` has tool, part, check; step 6
  polarity in the plan's words; the first-load section's net map equals
  `board-v2.md` §4; the template's outline equals the winner's (compare
  the numbers in `template.py` with `packing-v2.md` §5); the ledger has
  no total and Rolf's ceiling row blank; every sheet ends with write-back
  lines.
- **WP17b**: six spot-checks on live pages (the nRF52840 absolute
  maximum, the ST-LINK V3 MINIE voltage range and DigiKey price, the
  Black Magic Probe range, JLC's stiffener fee sentence, the ADS1292
  decoupling sentence, the Jauch DigiKey line); UNVERIFIED tags kept; no
  recommendation beyond the facts.

## Output

1. `tasks/reviews/code-r6.md`: a three-line verdict (MERGE /
   MERGE-AFTER-DECISION / REJECT), the gate results with commands and
   numbers (test count and skips per extra, hash identity, Stage B v2 and
   shell identity, release summary, firmware build size, repo growth), a
   table of defects (severity, file:line, what was wrong, what you
   changed, commit hash), the §7 look judgement in prose, and "Needs a
   decision" numbered from 69. Commit it on `review/r6`.
2. `.reports/review-r6-report.md` in this worktree: what you merged, what
   you changed, the final commit sha.
3. Then, in order:

       herdr pane report-metadata "$HERDR_PANE_ID" --source lane --token lane=review-r6 --token done=1
       herdr notification show "review r6 done" --body "reviewer rev6" --sound done
       herdr agent prompt elicio "DONE review-r6 .reports/review-r6-report.md <final commit sha>" || herdr agent prompt elicio "DONE review-r6 .reports/review-r6-report.md <final commit sha>"

Your turn must end with that push, including if the verdict is REJECT. If
you must stop for something outside yourself, push
`WAITING review-r6 <what>` instead. If you start a helper lane, close its
tab before you push.

## The worker reports, verbatim

Coordinator notes sent mid-round, in order: to w2 (22:58) take the BOM
codes, fee and datasheet sentences from L7 §3 and §4 and state the probe
limit in board-v2 §4; to w3 (22:58) add the Jauch cell; to w1 (23:05) cut
`REF_end_wall_slot` from `lane/w3`'s §5; to w3 (23:12) bigger box; to w5
(23:20) any cell under 16 mm; to w3 (23:48) the 17.0 mm 501015 pack and
the 501012 pack. Each ran as a new turn and its DONE is in the reports.

### WP14 (lane w1, both turns)

```markdown
# WP14 report — shell v2 on the round 5 winner

Lane `w1`, branch `lane/w1-r6`, package WP14. Plan v2 at `ef369bd`
(`docs/fab/plan-v2.md`). `plan-v2.md` and `open-questions.md` were not
edited. Order 1 files under `docs/fab/cad/v1/` were not written.
`lane/w3` was not merged.

## What was built

Wearable body and lid on winner `A_501015_series_w20_y8_iII_s3`. Same
Stage B v2 construction path; `STAGE=shell` adds hex collars, ring seats,
Q59 `REF_end_wall_slot`, bosses, USB end-face opening, switch recess, tail
hinge lip, two cantilever snaps, elliptical hook, lid crown. Overlay
`scripts/cad/params/shell_v2.toml`. Outputs `docs/fab/cad/v2/`. Record
`docs/fab/shell-v2.md`.

Closure: hinge lip in the tail plus two snaps L=8 t=1 y=0.5, strain
0.0117. USB on the hook-end end face. Standoff 3.0 mm. M1=52,
`provisional: true`.

## Coordinator note (second DONE)

WP11b on `lane/w3` at `284ec05`, `packing-v2.md` §5, table REF tab route:
no in-cavity REF route. Cavity ends at s 38.20, tail pocket starts at
s 39.25, 1.05 mm of nylon between them. Q59 is `REF_end_wall_slot`
(u 7.25–9.75, s 38.20–39.25, y 1.50–1.81, 2.50 × 1.05 × 0.31,
0.814 mm³). The shell cuts that box plus 0.20 mm flex clearance per side
in u, 0.20 mm in s, 0.15 mm in y. Measured on the built solid: slot width
2.90, clearance 0.20 mm per side in u.

`V2_TAB_envelope` pass: REF_body_mm3 0.0, SIG1 0.0, SIG2 0.0.
`REF_WIRE_envelope` pass: body_mm3 0.0, lid_mm3 0.0.

`V2_WALL_minima` pass: anterior 1.5, posterior 1.5, remaining end wall
beside the slot 1.827 / 1.879, floor under the slot 1.50, snap residual
1.1, USB ligament 1.5. All ≥ 1.0 beside the slot, ≥ 1.5 on the side
walls.

Stage B v2 without `STAGE=shell` is not slotted. Q59 still fails there
(REF 1.194 mm³ / 1.1902 mm³). Cited `packing-v2.md` §5 on lane/w3 in
`shell-v2.md`. Did not merge `lane/w3`.

## Gates

| Gate | Command | Result |
|---|---|---|
| Full suite | `.venv/bin/python -m unittest discover -s tests -v` | OK, 174 tests, 167.029 s, CAD tests ran |
| Order 1 byte-identical | `CadRegenTests.test_reference_regen_matches_committed_hashes` and `CadRenderTests.test_renders_and_drawing_regen_byte_identical` in that run | both ok |
| Stage B v2 still the round 5 solid | `CadStageBV2BuildTests` vs `STAGE_B_V2_MEASURED` | ok. Q59 still fail (`V2_TAB_envelope` REF 1.194 mm³, `REF_WIRE_envelope` 1.1902). No numbers moved. Exit 3 on a Stage B write. Two consecutive file hashes identical |
| Shell twice identical | `CadShellV2BuildTests.test_two_consecutive_shell_runs_are_identical` | ok, exit 0, `stage: shell` |
| Manifest bytes | `.venv/bin/python scripts/cad/manifest.py --check-bytes docs/fab/cad/v2/manifest.json` | schema 1 ok |
| git status | `git status --short` | empty at DONE (report untracked) |

Plan §9 row 14 (shell v2: body, lid, closure and hook, port wall, bosses,
pockets, renders, manifest; §7 checks; Stage B checks on the built solid;
identical regeneration): the listed files exist; §7 and Stage B rows are
in the manifest and in `shell-v2.md`; regeneration tested as above.

## What was not done

No order, quote, or upload. Insertion and retention forces not computed
(no printed PA12 E). Hook joint 1.5 fillet requested; OCCT left it sharp.
Printed hex well is AF 6.3 plus Ø7.4 (oversized vs brass 5 AF).

## Needs a decision

1. M1 (Q34). Default 52. Manifest `provisional: true`.
2. Printed hex clearance vs captive 5 AF (G7).
3. Hook joint fillet: leave sharp, or a different blend.
4. Snap insertion and retention, and the S4 pull and drop.
5. Colour, grey or dyed black (Q30).
6. Q17 REF dome on the tail.
7. Q59 is the slot (`packing-v2.md` §5 on lane/w3 at `284ec05`). No
   further packing search.
8. Standoff 3.0 vs Harwin 4.0. This file keeps 3.0.

## Final commit sha

First DONE: `553b3026d7324bf9115ec38658e341098394f3f8`
(`shell(v2): the wearable body on the round 5 winner`).

Second DONE: `c3c11d8d500f60ee93a0102a75fbdcf29ff91ff6`
(`shell(v2): cut REF_end_wall_slot from packing-v2 §5`).

A post-commit hook on this repo pushed `lane/w1-r6` to origin after each
commit. This lane did not run `git push`.
```

### WP11b (lane w3, four turns)

```markdown
# WP11b report — DTP arc-plus and the REF tab route

Lane `w3`, branch `lane/w3`, package WP11b.
Plan for this package: `docs/fab/plan-v2.md` at `ef369bd`.
Analysis only. The plan was not edited. Order 1 was not touched.
No order. No vendor contact.

## What was built

`scripts/cad/placement_v2.py` now runs the DTP301120 series under interface II
at `--arc-plus 1.5` and `3.0`, the Jauch LP501218JH series at BODY_ARC and
arc-plus, and three REF tab routes on the 501015 winner board.
`scripts/cad/placement.py` accepts `--dtp-arc`, `--jauch`, `--buyable-ext`,
`--pack-cells`, and `--cell` `jauch|pack501015|pack501012`.
`docs/fab/packing-v2.md` was regenerated, not hand-edited. Round-5 packing tabs
are unchanged, so Stage B still measures the straight floor REF path.
Jauch and the L7 packs are not in the 864-run matrix. Round 5 tests stay as they were.
The 864-run table and the Stage B winner row were not rewritten.

The 501012 pack closes on 8 bodies. Those drawings were not added under
`docs/fab/cad/v1/`: 14 + 8 would exceed the WP11b Q56 cap of 20, and the
round-5 kept-set test pins `placement_v2_*.svg` to the 864-run 14-file set.

Python 3.13 venv in this worktree. Install: `.venv/bin/python -m pip install -e '.[cad]'`.

## L7 packs (note 3, L7 §7 and §7.8)

144 runs (2 cells × 3 widths × 4 lids × 2 standoffs × 3 arcs). Round-5 checker.
Foam 0.5. Series. Interface II. BODY_ARC and arc-plus 1.5 and 3.0.

The winner body with the real 17.0 mm pack does not close.
First conflict: `BQ25100 overlaps header`. Board s 20.0–37.6 (bare cell was 18.6–37.6).
0 of 72 501015-pack runs close. No first-conflict family is on every run.
On the winner body, +1.5 mm of arc clears the overlap and then fails M1 (49.42 > 49.00).

8 of 72 501012-pack runs close. Smallest closer: `A_pack501012_series_w19_y8_iII_s3`.
TOTAL_CHORD 47.90. Outer 9.0. Width 19 (−1 mm vs the 501015 winner). Same chord. Same outer.

| cell | size (L × W × T) | packed | smallest closer | width | lid | outer | TOTAL_CHORD |
|---|---|---:|---|---:|---:|---:|---:|
| 501015 (bare, 864-run winner) | 15.6 × 10.4 × 5.2 | 5.7 | `A_501015_series_w20_y8_iII_s3` | 20 | 8 | 9.0 | 47.90 |
| 501015 pack | 17.0 × 10.0 × 5.0 | 5.5 | none | — | — | 9.0 | 47.90 |
| 501012 pack | 13.0 × 10.1 × 5.1 | 5.6 | `A_pack501012_series_w19_y8_iII_s3` | 19 | 8 | 9.0 | 47.90 |

Sources: L7-research-v4.md §7 and §7.8. Full table: `docs/fab/packing-v2.md` §1e.

## DTP301120 arc-plus (Q55)

DTP301120 22.0 × 11.5 × 3.2, foam 0.5 (Q57), series, interface II, architecture A.
Widths 18 to 20, LID_Y 7 to 9, standoffs 3.0 and 4.0. Same round-5 conflict logic.
48 runs. 0 close at +1.5. 0 close at +3.0. There is no DTP body that closes.

Winner stays `A_501015_series_w20_y8_iII_s3`. TOTAL_CHORD 47.9005.

| arch | standoff | width | lid | arc+ | closes | first conflict | TOTAL_CHORD | M1 gate |
|---|---:|---:|---:|---:|---|---|---:|---:|
| A | 3 | 18 | 7 | 1.5 | no | module top 7.62 > LID_Y 7 | 49.42 | 52.42 |
| A | 3 | 18 | 7 | 3 | no | module top 7.62 > LID_Y 7 | 50.93 | 53.93 |
| A | 4 | 18 | 7 | 1.5 | no | module top 8.62 > LID_Y 7 | 49.42 | 52.42 |
| A | 4 | 18 | 7 | 3 | no | module top 8.62 > LID_Y 7 | 50.93 | 53.93 |
| A | 3 | 18 | 8 | 1.5 | no | JST_SH top 8.22 > LID_Y 8 | 49.42 | 52.42 |
| A | 3 | 18 | 8 | 3 | no | JST_SH top 8.22 > LID_Y 8 | 50.93 | 53.93 |
| A | 4 | 18 | 8 | 1.5 | no | module top 8.62 > LID_Y 8 | 49.42 | 52.42 |
| A | 4 | 18 | 8 | 3 | no | module top 8.62 > LID_Y 8 | 50.93 | 53.93 |
| A | 3 | 18 | 8.5 | 1.5 | no | module 10.50×15.50 at (7.50,31.35) outside the board | 49.42 | 52.42 |
| A | 3 | 18 | 8.5 | 3 | no | module overlaps ADS1292_RSM | 50.93 | 53.93 |
| A | 4 | 18 | 8.5 | 1.5 | no | module top 8.62 > LID_Y 8.5 | 49.42 | 52.42 |
| A | 4 | 18 | 8.5 | 3 | no | module top 8.62 > LID_Y 8.5 | 50.93 | 53.93 |
| A | 3 | 18 | 9 | 1.5 | no | module 10.50×15.50 at (7.50,31.35) outside the board | 49.42 | 52.42 |
| A | 3 | 18 | 9 | 3 | no | module overlaps ADS1292_RSM | 50.93 | 53.93 |
| A | 4 | 18 | 9 | 1.5 | no | JST_SH top 9.22 > LID_Y 9 | 49.42 | 52.42 |
| A | 4 | 18 | 9 | 3 | no | JST_SH top 9.22 > LID_Y 9 | 50.93 | 53.93 |
| A | 3 | 19 | 7 | 1.5 | no | module top 7.62 > LID_Y 7 | 49.42 | 52.42 |
| A | 3 | 19 | 7 | 3 | no | module top 7.62 > LID_Y 7 | 50.93 | 53.93 |
| A | 4 | 19 | 7 | 1.5 | no | module top 8.62 > LID_Y 7 | 49.42 | 52.42 |
| A | 4 | 19 | 7 | 3 | no | module top 8.62 > LID_Y 7 | 50.93 | 53.93 |
| A | 3 | 19 | 8 | 1.5 | no | JST_SH top 8.22 > LID_Y 8 | 49.42 | 52.42 |
| A | 3 | 19 | 8 | 3 | no | JST_SH top 8.22 > LID_Y 8 | 50.93 | 53.93 |
| A | 4 | 19 | 8 | 1.5 | no | module top 8.62 > LID_Y 8 | 49.42 | 52.42 |
| A | 4 | 19 | 8 | 3 | no | module top 8.62 > LID_Y 8 | 50.93 | 53.93 |
| A | 3 | 19 | 8.5 | 1.5 | no | module 10.50×15.50 at (7.50,31.35) outside the board | 49.42 | 52.42 |
| A | 3 | 19 | 8.5 | 3 | no | module overlaps ADS1292_RSM | 50.93 | 53.93 |
| A | 4 | 19 | 8.5 | 1.5 | no | module top 8.62 > LID_Y 8.5 | 49.42 | 52.42 |
| A | 4 | 19 | 8.5 | 3 | no | module top 8.62 > LID_Y 8.5 | 50.93 | 53.93 |
| A | 3 | 19 | 9 | 1.5 | no | module 10.50×15.50 at (7.50,31.35) outside the board | 49.42 | 52.42 |
| A | 3 | 19 | 9 | 3 | no | module overlaps ADS1292_RSM | 50.93 | 53.93 |
| A | 4 | 19 | 9 | 1.5 | no | JST_SH top 9.22 > LID_Y 9 | 49.42 | 52.42 |
| A | 4 | 19 | 9 | 3 | no | JST_SH top 9.22 > LID_Y 9 | 50.93 | 53.93 |
| A | 3 | 20 | 7 | 1.5 | no | module top 7.62 > LID_Y 7 | 49.42 | 52.42 |
| A | 3 | 20 | 7 | 3 | no | module top 7.62 > LID_Y 7 | 50.93 | 53.93 |
| A | 4 | 20 | 7 | 1.5 | no | module top 8.62 > LID_Y 7 | 49.42 | 52.42 |
| A | 4 | 20 | 7 | 3 | no | module top 8.62 > LID_Y 7 | 50.93 | 53.93 |
| A | 3 | 20 | 8 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| A | 3 | 20 | 8 | 3 | no | ADS1292_RSM in the antenna keep-out | 50.93 | 53.93 |
| A | 4 | 20 | 8 | 1.5 | no | module top 8.62 > LID_Y 8 | 49.42 | 52.42 |
| A | 4 | 20 | 8 | 3 | no | module top 8.62 > LID_Y 8 | 50.93 | 53.93 |
| A | 3 | 20 | 8.5 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| A | 3 | 20 | 8.5 | 3 | no | ADS1292_RSM in the antenna keep-out | 50.93 | 53.93 |
| A | 4 | 20 | 8.5 | 1.5 | no | module top 8.62 > LID_Y 8.5 | 49.42 | 52.42 |
| A | 4 | 20 | 8.5 | 3 | no | module top 8.62 > LID_Y 8.5 | 50.93 | 53.93 |
| A | 3 | 20 | 9 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| A | 3 | 20 | 9 | 3 | no | ADS1292_RSM in the antenna keep-out | 50.93 | 53.93 |
| A | 4 | 20 | 9 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| A | 4 | 20 | 9 | 3 | no | ADS1292_RSM in the antenna keep-out | 50.93 | 53.93 |

At +1.5 mm of arc, TOTAL_CHORD 49.4157 against M1−3 = 49.00 (M1 = 52, Q34 blank, `default.toml`).
That chord already fails the M1 gate.
At +3.0 mm of arc, TOTAL_CHORD 50.9301. Excess versus M1−3 is 1.9301 mm.
Length cost versus the 501015 winner chord 47.9005 is +3.0295 mm of chord.
That is not a closer.

Nearest packing layout to the winner (width 20, LID_Y 8, standoff 3.0):
- +1.5 first conflict: `cell to antenna zone 4.15 < 5 mm`
- +3.0 first conflict: `ADS1292_RSM in the antenna keep-out`

Standoff 4.0 under interface II puts the module top at 8.62, so LID_Y 7 to 9 never closes.

## Coordinator note — Jauch LP501218JH (L7 §2)

L7-research-v4.md §2 (lane/w5) found no 501015-class cell sold in ones.
Buyable packs with page price, stock and a drawing: SparkFun DTP301120 and
Jauch LP501218JH+PCM (5.4 × 12.5 × 20.0 mm, 60 mAh, DigiKey
`1908-LP501218JH+PCM+2WIRE50MM-ND`, bare 2-wire leads).

72 interface-II series runs. Widths 18 to 20, LID_Y 7 to 9, standoffs 3.0 and 4.0,
BODY_ARC and +1.5 and +3.0. Foam 0.5. Packed height 5.9. Cell top 7.40.
**0 close.** There is no smallest Jauch body.

Bare 2-wire leads (28 AWG, 50 ± 3 mm, no connector) per L7 §2. Plan v2 R2:
Rolf solders nothing. This cell is a packing candidate only if the assembler
or the seller terminates the leads.

Nearest winner-like runs (width 20, standoff 3.0):
- LID_Y 8, BODY_ARC: first conflict `JST_SH top 8.22 > LID_Y 8`; also `cell to antenna zone 4.65 < 5 mm`
- LID_Y 8.5, BODY_ARC: first conflict `cell to antenna zone 4.65 < 5 mm`; TOTAL_CHORD 47.90
- LID_Y 7: `cell top 7.40 > LID_Y 7`

At +3.0 mm of arc, TOTAL_CHORD 50.93 (+3.03 mm versus the 501015 winner). That is not a closer.

### Smallest body per cell

| cell | sold in ones | smallest closer | width | lid | standoff | arc+ | TOTAL_CHORD | vs 501015 winner |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 501015 | no (L7 §2) | `A_501015_series_w20_y8_iII_s3` | 20 | 8 | 3 | 0 | 47.90 | — |
| DTP301120 | yes, SparkFun PRT-25270 | none | — | — | — | — | — | no closer |
| LP501218JH | yes, DigiKey (bare leads; needs a terminator) | none | — | — | — | — | — | no closer |

Full Jauch first-conflict table: `docs/fab/packing-v2.md` §1c.

## Coordinator note 2 — bigger lid and width

108 runs. DTP301120 and LP501218JH only. Series, interface II, standoffs 3.0 and 4.0, foam 0.5, BODY_ARC and +1.5 and +3.0. LID_Y 9.5, 10.0 and 10.5. Widths 20, 21 and 22. Same round-5 checker. 0 close. 0 pack if the ≤9×20 cap is set aside. No new drawing (Q56, closers only).

| cell | box | smallest closer | width | lid | outer | TOTAL_CHORD | height vs winner | chord vs winner | never-clears family |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 501015 | ≤9×20 | `A_501015_series_w20_y8_iII_s3` | 20 | 8 | 9.0 | 47.90 | — | — | — |
| DTP301120 | lid 9.5–10.5, w 20–22 | none | — | — | 11.5 | — | +2.5 mm still open | +0 / +3.03 mm, no closer | `SIG# tab crosses boss_# courtyard`, `cell overlaps standoff_SIG#` |
| LP501218JH | lid 9.5–10.5, w 20–22 | none | — | — | 11.5 | — | +2.5 mm still open | +0 / +3.03 mm, no closer | `cell overlaps standoff_SIG#` |

DTP at width 20, LID_Y 9.5, standoff 3, BODY_ARC: first conflict `cell to antenna zone 2.65 < 5 mm`. Outer 10.5. The 22 mm cell still hits SIG1 on every bigger-box run. Arc-plus +3.0 is TOTAL_CHORD 50.93 vs M1−3 = 49.00.

A buyable cell does not pack at +2.5 mm outer height or +3.03 mm chord. The 501015 winner stays the only closer.

Full table: `docs/fab/packing-v2.md` §1d.

## REF tab route (Q59)

Winner board `A_501015_series_w20_y8_iII_s3`. Tail site CONTACT_REF (8.50, 43.00).
Flex at the tab 0.31 (PI 0.11 + FR4 0.2). Bend R 1.5 (`board-v2.md` §11).

| name | y | points | length | added | min wall | side wall | end wall | in cavity | bend R 1.5 |
|---|---|---|---:|---:|---:|---:|---|---|---|
| `along_floor` | 1.50–1.81 | (8.50, 43.00) → (8.50, 36.80) | 6.20 | +0.00 | 0.00 | 5.75 | s 38.20–39.25 at u 8.50 | no | yes |
| `along_lateral_wall` | 1.50–1.81 | (8.50, 43.00) → (2.75, 43.00) → (2.75, 36.80) → (8.50, 36.80) | 17.70 | +11.50 | 0.00 | 0.00 | s 38.20–39.25 at u 2.75 | no | yes |
| `over_pocket_air` | 7.30–7.61 | (8.50, 43.00) → (8.50, 36.80) | 6.20 | +0.00 | 0.00 | 5.75 | s 38.20–39.25 at u 8.50 | no | yes |

No in-cavity route exists. The cavity ends at s 38.20. The Ø7.5 tail pocket starts at s 39.25.
1.05 mm of nylon sits between them. Every searched path crosses that wall.
`best_ref_tab_route()` is none.

WP14 cuts a slot that contains the straight floor tab:

| item | number |
|---|---|
| name | `REF_end_wall_slot` |
| u | 7.25–9.75 (centre 8.50) |
| s | 38.20–39.25 (centre 38.73) |
| y | 1.50–1.81 |
| width | 2.50 |
| through (s) | 1.05 |
| height (y) | 0.31 |
| volume (rect) | 0.814 mm³ |

Default packing REF tab is still (8.50, 43.00) → (8.50, 36.80).

## Plan §9 acceptance (WP11 row)

Plan v2 §11 row 11: packing table on the built solid; which close and why the rest fail.

| item | command | result |
|---|---|---|
| Round 5 864-run table still present | regenerated `docs/fab/packing-v2.md` §1 | 3 closers, all 501015 series w20 iII s3. Winner unchanged. |
| DTP arc-plus table | `.venv/bin/python scripts/cad/placement.py --dtp-arc` (and `--arc-plus 1.5\|3.0`) | 48 runs, 0 close. First conflict per run in §1b. |
| Jauch series table | `.venv/bin/python scripts/cad/placement.py --jauch` | 72 runs, 0 close. First conflict per run in §1c. Compare table next to DTP and 501015. |
| Bigger-box table (note 2) | `.venv/bin/python scripts/cad/placement.py --buyable-ext` | 108 runs, 0 close, 0 pack. §1d. |
| L7 pack cells (note 3) | `.venv/bin/python scripts/cad/placement.py --pack-cells` | 144 runs, 8 close (all 501012 pack). Winner body + 17.0 mm pack does not close (`BQ25100 overlaps header`). Smallest 501012 closer `A_pack501012_series_w19_y8_iII_s3`, TOTAL_CHORD 47.90, outer 9.0. §1e. |
| REF tab route table | packing generator §5 | no in-cavity route; slot numbers for WP14. |
| DTP / REF measured on a new solid | not run | WP11b is packing analysis. Stage B solids stay with WP14. Round 5 already measured `V2_TAB_envelope` fail (REF_body_mm3 1.194) on the winner solid. |
| Order 1 identity | `CadRegenTests` / `CadStageBV2BuildTests` in the full suite | pass. Order 1 files not edited. |

## Gates

Command: `.venv/bin/python -m unittest discover -s tests -v`

Result: Ran 182 tests in 166.175s. OK. 0 failures. 0 errors.

Round 5 placement tests were not rewritten. They passed in that run.
`packing-v2.md` matches a fresh generator write (`test_packing_doc_regenerates_byte_identical` and `test_packing_doc_has_dtp_and_ref_tables`).

`git status --short` is empty. `.reports/WP11b-report.md` is gitignored.

A post-commit hook on this worktree pushed `lane/w3` to origin. This lane did not run `git push`.

## What was not done

- No purchase, quote, or vendor contact (Q55 stays a research question).
- No edit of `plan-v2.md` or `open-questions.md`.
- No file under `docs/fab/cad/v2/`.
- No change to `bte_fit_shell.py`, `render.py`, `manifest.py`, or `tests/test_cad.py`.
- No new committed SVG (8 of 72 501012-pack runs close; 14 + 8 exceeds Q56's 20-file cap, and round-5 tests pin the v1 glob).
- No solid probe of a lid-to-wall gap for the REF tab.

## What could not be measured

- DTP arc-plus on a built solid. Packing arithmetic only.
- REF tab lid-to-wall gap. Packing treats the cavity end wall as solid from floor 1.5 to LID_Y 8.0.
- A 501015 pack in ones: none found (L7-research-v4.md §2). DNK/Benzo sheets give 17 × 10 × 5.0 with PCM (L7 §7 and §7.8). The 17.0 mm pack was packing arithmetic only. The 501012 13.0 × 10.1 × 5.1 figure is an eBay marketplace quote (L7 §7), not a manufacturer sheet. This package does not order. Jauch leads were not terminated.
- M1 on Rolf. Q34 blank. Default 52 used for the gate.
- Harness 100 ± 3 mm. Routed length, not a solid.
- Same Stage B NOT_MEASURED rows as round 5 (`V2_ADJUSTMENT`, `V2_BOSS`, `V2_RECESS`, `V2_USB_medial`, `TAB_envelope_air`).

## Numbers taken as given

| Item | Number | Source |
|---|---|---|
| DTP301120 | 22 × 11.5 × 3.2 | SparkFun PRT-25270 drawing p.9, L5-research-v2.md §1 |
| 501015 | 15.6 × 10.4 × 5.2 | v1 CELL_BODY_MAX (plan v1 §3.3); this is a bare cell (L7 §7) |
| 501015 pack (with PCM) | 17.0 × 10.0 × 5.0 | DNK Power DNK501015; Benzo; L7-research-v4.md §7 and §7.8 |
| 501012 pack (with PCM) | 13.0 × 10.1 × 5.1 | eBay quote 'approx 13.0mm x 10.1mm x 5.1mm', 40 mAh; L7-research-v4.md §7 |
| LP501218JH | 20.0 × 12.5 × 5.4 | L7-research-v4.md §2; DigiKey 1908-LP501218JH+PCM+2WIRE50MM-ND |
| Foam on the cell | 0.5 | plan v1 §5 and order-1 CELL_envelope; plan v2 §3 says 0.3 (decision 57 / Q57) |
| Flex at rings | 0.31 (PI 0.11 + FR4 0.2) | JLC FPC stiffener list, WP12 2026-09-17 |
| Flex tab bend for this search | R 1.5 | board-v2.md §11 |
| Round-5 packing bend floor | R 1.0 | existing `BEND_R` (unchanged) |
| CONTACT_REF | (8.5, 43.0) | packing-v2.md §5 |
| Cavity end / pocket start | s 38.2 / 39.25 | packing-v2.md §5 / Q59 |
| M1 | 52 | default.toml; Q34 blank |
| BODY_ARC | 48.4 | coordinator note 1 |
| Antenna keep-out | 12.4 × 3.8 | Raytac Spec K p.9/p.13, interface §6.3 |
| Floor | 1.5 | v1 |

Full source table: `docs/fab/packing-v2.md` §7.

## Needs a decision

1. The buyable DTP301120 does not close at +1.5 or +3.0 mm of arc. Keep the 501015 winner, or change M1 / body length / cell. +1.5 already fails M1 ≥ TOTAL_CHORD + 3 (49.42 > 49.00).
2. The buyable Jauch LP501218JH does not close at BODY_ARC, +1.5 or +3.0. Packed height 5.9. Antenna gap 4.65 mm at the winner width. Bare leads need a terminator (plan v2 R2).
3. No REF tab route stays inside the cavity. WP14 cuts `REF_end_wall_slot` (2.50 × 1.05 × 0.31 at u 7.25–9.75, s 38.20–39.25, y 1.50–1.81), or another path is chosen.
4. A bigger lid (9.5–10.5, outer 10.5–11.5) and width (20–22) still does not pack DTP or Jauch. The family that never clears is `cell overlaps standoff_SIG#` (DTP also keeps `SIG# tab crosses boss_# courtyard`). Keep the 501015 winner, or change the cell / antenna / standoff layout.
5. Q55: a 501015 pack in ones is not sold (L7 §2). This package did not order.
6. The real 17.0 mm 501015 pack does not close on the winner body or on any body in this grid. First conflict on the winner body: `BQ25100 overlaps header` (the pocket is longer, the board starts at s 20.0 instead of 18.6). Arc-plus +1.5 on that body clears the overlap and then fails M1 (49.42 > 49.00). The 501012 pack (marketplace listing) closes at width 19, LID_Y 8, standoff 3, BODY_ARC, TOTAL_CHORD 47.90, outer 9.0. Keep the bare-501015 Stage B winner, switch the candidate to the 501012 listing, or change the board/pocket for a 17 mm pack.

## Final commit sha

`bcecc831ac9ff3ab0a5ba5af4e1eccb8f30485b3`
```

### WP12b (lane w2)

```markdown
# WP12b report — Board v2, place, route, release (lane w2)

Worktree: `/home/user/projects/elicio/.worktrees/w2`
Branch: `lane/w2`
Package: WP12b
Date: 2026-09-17
KiCad: 10.0.6 (`kicad-cli`)

## What changed

GPIO map for WP13b went in first (`85b074f`, `docs/fab/board-v2.md` §9).

Schematic (`01f90b1`):

- Q68: C6 and C8 are 10 µF 0603 (`C19702`). C7 and C15 are 100 nF 0603 (`C14663`). C15 is new on `+3V0` / `GND`.
- C9 footprint is 0603 with `C19702` (old `C15850` is 0805).
- Blanked LCSC lines filled from pages on 2026-09-17: C2 `C91601`; C11/C12 `C1525`; R1–R3 `C881401`; R4/R17/R20/R21 `C2782127`; R14–R16/R23/R24 `C25741`; R22 `C11702`.
- U1 is `C5118826` (MDBT50Q-1MV2). `C5142646` is a GOOSVN screw terminal, not a Raytac module.
- Displayed stock and unit price: **UNVERIFIED** (pages did not show them).

PCB from `packing-v2.md` §5 winner `A_501015_series_w20_y8_iII_s3`:

- Packing (u, s) = PCB (x, y). Named SMT centres match within 0.1 mm (`tests/test_board_release.py`).
- WP11b `lane/w3` §5 REF tab search (Q59) left `along_floor` (8.50, 43.00) → (8.50, 36.80). This board uses that path. SIG1/SIG2 rings unfold off the island so the Gerber is flat.
- U1 at (10.00, 32.35) rot 90°. Zero module pads in the RF keep-out.
- Two FR4 0.4 stiffener pieces on Eco1.User (island + USB/pocket). No tab FR4 (Q58 clamp, Q60 merge). Count = 2, under JLC extra-stiffener fee at ≥4.
- Every schematic net is on the PCB. Pads without a net: 0. Tracks: 465.
- Freerouting v2.1.0 hung. A B.Cu bus fallback wrote copper so nets are not empty. That copper still shorts and violates clearance.

Q64: first-load REGOUT0 is 1.8 V. A 3.3 V probe high exceeds VDD + 0.3 V. The board offers VTref on TC2030 pin 1 from `+VDD`. It cannot set REGOUT0 through that probe.

Q65: System OFF + divider ≈ 3 µA vs ITERM 2.0 mA (floor 1 mA). Firmware must hold System OFF while charging.

LED and ISET stay as review r5 left them.

`scripts/board/release.py` is unchanged (Q62 fail-closed).

Nothing ordered, quoted or uploaded. No vendor contact.

## Gates

### 1. Unittest

```text
.venv/bin/python -m unittest tests.test_board_release -v
```

Result: **OK** (4 tests). ERC 0. BOM rows = placed parts = 59. `"routed": false` without `--routed`. `--routed` still refused. `pcb_tracks` > 0. Named SMT centres within 0.1 mm of packing §5.

```text
.venv/bin/python -m unittest discover -s tests -v
```

Result: 170 tests, **13 FAIL**, all `test_cad.CadRegenTests` v1 solid hashes (`body_full_p15`, `body_full_p25`, `body_thin_p15`, `lid`). This package does not own CAD. Same 13 as WP12.

### 2. `release.py --routed`

```text
.venv/bin/python scripts/board/release.py --board-dir hardware/board --out /tmp/wp12b-release --routed
```

| Field | Value |
|---|---|
| exit | 1 (`routed release refused`) |
| erc_errors | 0 |
| erc_warnings | 0 |
| drc_errors | 1290 |
| drc_warnings | 25 |
| unconnected_items | 31 |
| pcb_tracks | 465 |
| pcb_pads_without_net | 0 |
| routed | true (flag only; order release is not green) |
| bom_rows | 59 |
| placed_parts | 59 |

Non-`--routed` job still exits 0 (ERC 0, outputs present).

**This gate is not met.** Order release needs DRC 0 and 0 unconnected.

### 3. Forbidden paths vs `main`

```text
git diff main -- docs/fab/plan-v2.md docs/fab/open-questions.md firmware/
```

Result: empty.

### 4. `git status --short`

Empty of owned files. `.reports/WP12b-report.md` is gitignored.

## Plan §9 / brief deliverables

| Item | Result |
|---|---|
| Placement from packing §5 | Done. Test within 0.1 mm. |
| WP11b REF tab | Packing tab unchanged; used `along_floor`. Slot is WP14. |
| Sync every net | Done. Pads without a net = 0. |
| JLC 2-layer FPC DRC rules | Encoded in `elicio-v2.kicad_pro`. Copper does not pass them. |
| Contact 1.0 mm isolation | Ring keep-outs 7×7 mm. 1.0 mm netclass vs 220 kΩ on a 2.5 mm tab is not geometrically possible. |
| No contact copper under module keep-out | RF box empty of extra copper; module pads allowed. |
| 220 kΩ at tab entries | R1/R2/R3 at tab midpoints, past the 4 mm strain-relief window. |
| Star ground / USB pairs / antenna empty | GND zones on the island. USB pairs exist as tracks but DRC fails. Antenna keep-out has no extra copper. |
| `--routed` exit 0 | **Fail.** 1290 DRC errors, 31 unconnected. |
| Stiffeners ≤ 3 | 2 pieces. Fee text in `board-v2.md` §18. |
| Q68 decoupling | Schematic and land. Caps on B.Cu under the ADS. |
| Q64 / Q65 | In `board-v2.md` §4 and §5. |
| BOM Q63 / U1 / Q67 | Pages 2026-09-17. Stock/price UNVERIFIED. U1 = C5118826. Raytac routes in §18. |
| G7 joint inputs | `board-v2.md` §11. STEP tabs modelled flat. |
| §11a rejected I | Kept. |
| §19 | Renumbered. |

## What stayed UNVERIFIED

- LCSC displayed stock and unit price (pages 2026-09-17).
- JLC global sourcing and consignment as a live Raytac buy (Q67 pages are thin).
- E73-2G4M08S1C land vs M08S1C drawing.
- YFP0006 land vs TI 4223410/A.
- 501015 harness 100 ± 3 mm (`NOT_MEASURED`).
- LDO dropout at 1–2 mA (interpolation in §6).
- Physical G2 leakage.

## Needs a decision

See `docs/fab/board-v2.md` §19.

1. G1b — JST-SH vs PH; 501015 harness 100 ± 3 mm.
2. SIG1/SIG2 unfold — Gerber rings are off the island; WP14 folds them.
3. Order route — `--routed` is fail-closed. A human or a working autorouter must finish the 2-layer flex before G3.
4. 3.3 V probe vs 1.8 V first-load — Q64; kit is WP17b.
5. E73 land vs M08S1C drawing.
6. YFP0006 land vs TI drawing.
7. BQ25100YFPR stock (extended).
8. Protective monitor cadence (firmware).
9. Displayed LCSC stock/price at G3.
10. JLC assembly edge 2.5 mm vs packing centres.

## Final commit sha

`480e35533030ddc02f5bf434f57dde1f242016b7` (`board(v2b): placed from the packing, routed, released`)

A repository post-commit hook pushed `lane/w2` to origin after the commits. This lane did not run `git push`. The package brief said never push.
```

### WP13b (lane w4)

```markdown
# WP13b report — Receiver v2

Lane `w4`. Branch `lane/w4`. Final commit `e7c366a8191bf6abb26ab20045fabb5e70e23452`.
Worktree `/home/user/projects/elicio/.worktrees/w4`.

Host-only. No radio and no board were used.

## What was built

- `src/elicio/receiver_v2.py`: NUS packet ingest through `frame_v2.Reassembler`, session writer, `load_receiver_session` (returns `elicio.pipeline.load.Recording`), `receive-check`, fake transports. Loader name: `elicio.receiver_v2.load_receiver_session`.
- `elicio receive --device|--simulate|--simulate-live --out DIR` and `elicio receive-check DIR` in `src/elicio/cli.py`.
- `tests/test_receiver_v2.py` and `tests/fixtures/receiver_v2/`: every `frame-v2.md` case plus dropout, undervoltage, VBUS, and simulate-live. No BLE adapter.
- `firmware/src/board_pins.h` aligned to `docs/fab/board-v2.md` §9. The same table on `lane/w2` matches (w2 added a sentence above the table; pin numbers did not move).
- `docs/fab/receiver-v2.md`. One dated heading in `docs/fab/firmware-v2.md`.
- `pyproject.toml` optional extra `ble` (`bleak>=0.22`). Required by the brief; not on the Owns list otherwise.

Session files: `samples.npz` (int32 codes `[n,2]` plus metadata), `sidecar.json` (overrun, transport loss, wrap, reconnect, VBUS and undervoltage events), `meta.json`.

## Gates

1. `.venv/bin/python -m unittest discover -s tests -v`

   Result: exit 0. `Ran 179 tests in 84.407s` `OK (skipped=21)`. On a clean tree without matplotlib, 18 existing `PlacementV2Tests` SVG cases error (`matplotlib is not installed`). matplotlib 3.x was installed in this venv so those inherited tests run. They are not WP13b files.

2. `arduino-cli compile --fqbn adafruit:nrf52:feather52840 --library firmware --output-dir /tmp/elicio-firmware-build firmware/elicio_stream`

   Result: exit 0. Sketch uses 134012 bytes (16 %) of 815104. Global variables 18472 bytes (7 %) of 237568.

3. `git status --short` empty after the last commit.

Plan v2 §11 row 13 "builds in CI; bench-tested at S2": no CI in the repo. Host unittest and the compile above ran. S2 bench was not run (no board).

## What was installed

| Item | How | Size / version |
|---|---|---|
| bleak 3.0.2 | `.venv/bin/python -m pip install -e '.[ble]'` | 1.3 MB in site-packages |
| matplotlib | pip, so inherited placement SVG tests do not error | needed by `tests/test_placement.py` on this main, not by the receiver |

## What was not exercised

`receive --device` was not run on air. No Feather, no product board, no ADS1292, no gel montage. Same-criterion lines 3.5–3.10 stay `not_scored` without a detector log. The Feather FQBN compile treats nRF P0.n values as Arduino digital numbers; that is not a product wiring run.

A local unversioned `post-commit` hook ran `git push` after each commit on `lane/w4`. This lane did not invoke `git push`.

## Needs a decision

1. `receive-check` fails on montage §8 dropout (rail or flat > 200 sample intervals) even though table line 3.4 is marked "revised". 3.5–3.10 only fail when scored in the sidecar. Confirm that split for S2.
2. Product pin numbers in `board_pins.h` are not a Feather silkscreen map. A product variant or a `#ifdef` is still needed before a Feather is used as a wired stand-in.

## Final sha

`e7c366a8191bf6abb26ab20045fabb5e70e23452`
```

### WP15 (lane w9)

```markdown
# WP15 report — Rolf's sheets v2

Lane `w9`, branch `lane/w9`, worktree
`/home/user/projects/elicio/.worktrees/w9`. Interpreter: Python
3.13 in a worktree-local `.venv`. HEAD at start `dbe39ff` (same as
`main`). Docs plus `scripts/sheets/template.py` and
`tests/test_sheets.py`. `pyproject.toml` was not edited. matplotlib
3.11.2 and pypdf 6.19.0 were installed into `.venv` from the existing
`cad` extra pins.

## What was written

- `scripts/sheets/template.py`: 1:1 US-letter PDF of winner
  `A_501015_series_w20_y8_iII_s3` (packing-v2.md §5) with contacts
  (5.9, 22.0), (10.4, 33.1), (8.5, 43.0), a 50 mm bar, and the check
  "Measure the 50 mm bar before you trust this template." Also eight
  SVGs in `docs/fab/sheets/` (m1–m8). PDF dates pinned via pypdf.
- `docs/fab/template.pdf` and `docs/fab/sheets/m1.svg` … `m8.svg`.
- `docs/fab/measure.md`: v2 rewrite. M1–M8 keep the v1 definitions.
  Right ear (Q28). On-bone check at REF with the paper template (Q17).
  M1 gates everything once (50.90 mm, packing-v2.md §6).
- `docs/fab/order-board.md`, `order-shell.md`, `order-parts.md`: G8
  first, then the order. Unknown vendor fields say "the agent fills
  this after WP12b/WP14". Uploads from `docs/fab/cad/v2/` and
  `hardware/board/release/` marked expected. Massachusetts. Duties as
  DDP shows them. Raytac Q67 on the board sheet. One ledger line per
  small-parts parcel. Q64 names two probe options and does not pick.
- `docs/fab/assemble.md`: plan v2 §8 eight steps, each with tool,
  part, check, and a WP14 picture placeholder; step 6 polarity in the
  plan's words; first-load net map from board-v2.md §4, REGOUT0 note,
  firmware-v2.md commands, time "measured, not promised"; §7 pull and
  drop as qualitative steps; fail = stop and write one line.
- `docs/fab/orders-v2.md`: Q33 ceiling row still blank, with Rolf's
  name on it. Shell reserved-maximum row unchanged. No total.

`plan-v2.md` and `open-questions.md` were not edited.

## Plan v2 §11 row 15

Acceptance: no step needs a question; the first-load procedure
rehearsed on paper.

`grep '?' docs/fab/measure.md docs/fab/order-board.md
docs/fab/order-shell.md docs/fab/order-parts.md docs/fab/assemble.md`
finds nothing. First load is a paper section in `assemble.md` (net
map, REGOUT0, commands, write-back for measured time and VTref). It
was not run on hardware.

## Gates

### Unit tests

Command:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

Result: Ran 173 tests in 83.641s. OK (skipped=21). Skips need
build123d / trimesh. New `tests/test_sheets.py` ran four tests,
including two-run byte identity and match to the committed PDF/SVGs.

### Template twice identical

Command: `tests.test_sheets.TemplateRegenTests.test_script_run_twice_is_byte_identical`

Result: ok.

### owner / the user

Command:

```bash
grep -n "owner\|the user" docs/fab/*.md
```

Result: one hit, pre-existing, `docs/fab/interface.md:554`. Nothing
new in the WP15 sheets.

### git status

`git status --short` empty after the four commits (this report
untracked under `.reports/`, gitignored).

## Numbers that wait on WP12b and WP14

WP12b: gerber names; flex ENIG/coverlay checkout fields; extra-stiffener
fee amount; stiffener count after merge; BOM/CPL/STEP in
`hardware/board/release/`; `summary.json` with `routed: true`; Raytac
global-sourcing vs consignment prices on the day; factory programming
catalogue line; product first-load hex (with WP13b).

WP14: `docs/fab/cad/v2/` body and lid STL/STEP/3MF names; two renders;
drawing page; manifest checks; stand-if-printed; colour process;
closure geometry for step 7; board-screw SKU for step 5; connector
picture for step 6; tab-wall slot (Q59).

## What was not done

- No purchase, quote, upload, or vendor contact.
- First load was not run. Time is blank for Rolf to measure.
- Exact JLC flex and JLC3DP checkout fields that are not already on
  `main` were left as "the agent fills this after WP12b/WP14".
- matplotlib was not added to `pyproject.toml` (not in Owns).
- This lane did not run `git push`. A post-commit hook pushed
  `lane/w9` to origin after each commit.

## Needs a decision

- Q33 ceiling (Rolf; ledger row blank).
- Q64 probe: Raspberry Pi Debug Probe vs J-Link EDU Mini class / level
  shifter. The sheet names both. G4 names one before a buy.
- Q67 Raytac route at G3 with both prices in front of him.
- Q55 cell SKU with a page price, or WP11b length trade.
- Q36 China vs not, for the default JLC carts.
- Q59 REF tab vs cavity end wall: nothing orders until it passes.
- G1b pack/connector freeze before assemble step 6.
- Step 5 board screws: plan v2 §8 names them; Interface II retention
  is WP14's (`V2_BOSS` NOT_MEASURED).

## Final commit sha

`018ac588a1f54b5e2fec1bde510ee930a154aabf`

Message: `sheets(v2): measure, three checkouts, assemble, first load`.

Under it: `c1afb71` checkouts, `52f5cb5` measure.md, `958d448`
template script and drawings.
```

### WP17b (lane w5, both turns)

```markdown
# WP17b Work Package Report: Research v4 — Probe, Cell in Ones, Fees

**Package:** WP17b — Research v4: the probe, the cell in ones, the assembler's fees  
**Lane:** w5  
**Worktree:** `/home/user/projects/elicio/.worktrees/w5`  
**Branch:** `lane/w5`  
**Date:** 2026-09-17  
**Final Commit SHA:** `ba45071bc81810fc9290e0e4db4aa3a11a0395e3`  

---

## 1. What Was Built

Updated `docs/fab/L7-research-v4.md` across two turns:
- **Turn 1 (commit `ea3b9bd`):** Initial Research v4 covering first-load probe (Q64), cell in ones (Q55), JLCPCB fees (Q60/Q67/Q65), component facts (Q63/Q68/Q65), shell colour/finish (Q30), and Ebyte E73 drawing.
- **Turn 2 (commit `ba45071`):** Appended Section 7 covering exhaustive research into secondary lithium pouch cells fitting within the maximum envelope of $16.0\text{ mm (L)} \times 10.5\text{ mm (W)} \times 5.2\text{ mm (T)}$ with Protection Circuit Module (PCM), capacity $\ge 30\text{ mAh}$, with leads/connector, available in single units with displayed price and stock.

---

## 2. Turn 2 Dedicated Findings: Pouch Cells Under 16 mm (Q55 Follow-Up)

### 2.1 The 16 mm Envelope Problem and Distributor Reality
- **Authorized Component Distributors (DigiKey, Mouser):** Parametric filtering for secondary Li-ion/LiPo cells $\le 16.0\text{ mm}$ length with $\ge 30\text{ mAh}$ yields **0 results**. Shortest Jauch cell is `LP501218JH` ($20.0\text{ mm}$ long); shortest Renata cell is `ICP641620PA` ($21.5\text{ mm}$ long).
- **Hobbyist / Maker Distributors (Adafruit, SparkFun, TinyCircuits, Pimoroni, The Pi Hut, Seeed Studio, Kitronik):** Zero secondary pouch cells $\le 16.0\text{ mm}$ length exist.
  - TinyCircuits `ASR00035` is 500 mAh ($30.0 \times 20.0 \times 9.5\text{ mm}$); smallest cell `ASR00007` is 150 mAh ($19.5 \times 25.5 \times 4.5\text{ mm}$).
  - PowerStream PGEB series has only one micro-cell under 16 mm (`GM-NM300910`, $3.0 \times 9.0 \times 10.0\text{ mm}$), but its capacity is only 12 mAh (fails $\ge 30\text{ mAh}$). All other PGEB models are $\ge 25.0\text{ mm}$ long.
  - Adafruit smallest cell is Product 1570 (100 mAh, $12 \times 28 \times 5.5\text{ mm}$).
  - SparkFun smallest cell is `PRT-25270` / `DTP301120` (40 mAh, $3.2 \times 11.5 \times 22.0\text{ mm}$).
  - Pimoroni, The Pi Hut, Seeed Studio, and Kitronik stock only cells $\ge 25.0\text{ mm}$ long.

### 2.2 The 501015 Dimension and PCM Trap
- A generic **501015** pouch cell ($5.0 \times 10.0 \times 15.0\text{ mm}$) specifies only the **bare pouch** dimensions.
- Technical datasheets from manufacturers (DNK Power `DNK501015`, Benzo Energy `BZ 501015`) show that adding the end-mounted Protection Circuit Module (PCM) and tape increases the finished pack length to **17.0 mm** (DNK Power verbatim: "Dimensions: 17 × 10 × 5.0 mm").
- Therefore, any 501015 pack with PCM **exceeds the 16.0 mm length limit by 1.0 to 1.5 mm** and will collide with the antenna keep-out or SIG1 standoff in the packing layout.

### 2.3 The Identified Solution: Model 501012 (or 401012)
- **Model 501012 (Earphone / TWS Pouch Cell):**
  - **Dimensions with PCM:** **$5.1\text{ mm (T)} \times 10.1\text{ mm (W)} \times 13.0\text{ to }14.5\text{ mm (L)}$** (bare pouch is $5.0 \times 10.0 \times 12.0\text{ mm}$).
  - **Envelope fit:** Length $13.0\text{–}14.5\text{ mm} \le 16.0\text{ mm}$ (clears length constraint with 1.5–3.0 mm margin!); Width $10.1\text{ mm} \le 10.5\text{ mm}$; Thickness $5.1\text{ mm} \le 5.2\text{ mm}$.
  - **Capacity:** **40 mAh** (35–45 mAh), satisfying the $\ge 30\text{ mAh}$ floor.
  - **Leads:** Red/Black flying wire leads (typically 28–30 AWG, 30–50 mm length) attached to top PCM.
  - **Availability in Ones:** Readily available in stock on eBay (e.g. item `183480766633`) and AliExpress (e.g. item `1005006093774888`) for **$4.00 to $8.00 USD** with published prices and stock counts.
- **Model 401012:**
  - Bare dimensions $4.0 \times 10.0 \times 12.0\text{ mm}$; pack length with PCM is ~14.0 mm; capacity 30–35 mAh; passes all axes.

---

## 3. Acceptance Verification and Gates

### Gate 1: Test Suite
*   **Command:** `/home/user/projects/elicio/.worktrees/w5/.venv/bin/python -m unittest discover -s tests -v`
*   **Result:** Ran 169 tests in 79.260s. **OK (skipped=21)**. 0 errors, 0 failures.

### Gate 2: Clean Git Working Tree
*   **Command:** `git status --short`
*   **Result:** Empty (clean). Untracked report `.reports/WP17b-report.md` is gitignored.

### Gate 3: Commit History on `lane/w5`
*   Commit `ea3b9bd3d22ea879c86e026b6e2bb07cbe6943ea`: `research(v4): probe, cell in ones, fees`
*   Commit `ba45071bc81810fc9290e0e4db4aa3a11a0395e3`: `research(v4b): cells under 16 mm`

---

## 4. What Stayed UNVERIFIED

1.  **Distributor-Stocked LiPo Cells $\le 16.0\text{ mm}$ Length with $\ge 30\text{ mAh}$:** `UNVERIFIED` / None exist across DigiKey, Mouser, Adafruit, SparkFun, TinyCircuits, Pimoroni, The Pi Hut, Seeed Studio, or Kitronik.
2.  **JLC3DP / Xometry Static Price Deltas for Finish Options:** `UNVERIFIED` as static published catalog figures (both vendors utilize dynamic 3D model geometry quotation).
3.  **Ebyte E73 Direct DXF/CAD File:** `UNVERIFIED` on public direct links without vendor account portal access.

---

## 5. Needs a Decision for Plan v2 Build Rounds

1.  **Cell Selection for S0 Prototype and Packing (Gate G4):**
    *   The packing lane determined that 20 mm and 22 mm cells collide with the antenna zone or SIG1 standoff.
    *   Nominal 501015 cells with PCM are **17.0 mm long** and also fail the 16.0 mm body limit.
    *   *Decision:* Adopt **Model 501012** (40 mAh, $5.1 \times 10.1 \times 13.0\text{–}14.5\text{ mm}$ with PCM) for the mechanical packaging model and prototype procurement. Procure 2–5 units via eBay / AliExpress or request manufacturer engineering samples from DNK Power / Benzo Energy.
2.  **First-Load Programming Probe Selection:**
    *   Adopt a level-shifting probe with $V_{TRef}$ sensing for first load: ST-LINK V3 MINIE ($25.51 USD, DigiKey), Black Magic Probe V2.3 ($74.95 USD, 1BitSquared), or SEGGER J-Link EDU Mini ($75.95 USD, Adafruit).
3.  **Charger System Load Management (BQ25100):**
    *   Firmware must enter low-power sleep on the radio and MCU during USB attachment to prevent system load from exceeding $I_{TERM}$ and triggering the 10-hour safety timer fault.

---

## 6. Final Commit SHA

`ba45071bc81810fc9290e0e4db4aa3a11a0395e3`
```

