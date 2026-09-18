# HANDOFF — Elicio coordinator

Written 2026-09-18 00:25 (America/New_York) by the coordinator (`elicio`,
pane `w1B:p1`) right after opening the round 6 review. Rolf is asleep; the
delegation below is in force.

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
`docs/fab/open-questions.md` (Q1–Q68).

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

Round 5 gates at merge (`tasks/reviews/code-r5.md`): 191 tests OK none
skipped, order 1 byte-identical, Stage B v2 identical twice and exit 3 on
Q59 only, `release.py` exit 0 (unrouted) and exit 1 with `--routed`,
`arduino-cli compile` exit 0, repo growth 0.63 MB. Round 4 gates: 129
tests OK; order 1 byte-identical; provisional Stage B identical twice,
exit 3 on Q21 only.

## In flight

Round 6, opened 2026-09-17 22:15. Six lanes, all prompted with "read your
brief in full and do it", nothing owed from me until their pushes.

- **w1 → WP14 shell v2**: LANDED, `DONE WP14` at `553b302` on
  `lane/w1-r6` (three commits, tree clean, report
  `.worktrees/w1/.reports/WP14-report.md` present, 174 tests OK with the
  CAD tests running, order 1 byte-identical, Stage B v2 unchanged and
  still exit 3 on Q59 by design, the shell build identical twice).
  Delivered `docs/fab/cad/v2/` (absent on main) with body and lid STEP,
  STL, 3MF, two renders, a drawing page and a manifest marked
  provisional at M1 52; `docs/fab/shell-v2.md` (absent on main);
  `scripts/cad/params/shell_v2.toml` (absent on main). The shell slots
  the cavity end wall for the REF tab (Q59); closure is a tail hinge lip
  plus two cantilever snaps with a strain number; USB-C on the hook-end
  end face; standoff 3.0. Open from its report: printed hex well
  oversized against the brass 5 mm across flats (G7), the hook joint
  fillet left sharp by the kernel, snap forces not computed, Q17 REF
  dome. Second `DONE WP14` at `c3c11d8`: the slot cut from
  `packing-v2.md` §5 on `lane/w3` with 0.20 mm flex clearance;
  `V2_TAB_envelope` and `REF_WIRE_envelope` pass on the shell solid (0.0
  mm³), walls beside the slot 1.83 and 1.88, floor under it 1.50; Stage B
  v2 stays unslotted and exit 3 by design. w1 idles. The reviewer measured the shell and four checks fail
  (closure, USB end, edge radii, wall minima; see Reviewer r6). WP14b
  brief `tasks/WP14b-shell-v2b.md` (main, `58ae5b8`): concealed tail
  screw plus hinge lip (Q71), lofted lid lapping the wall tops, hook root
  blend (Q76), USB row NOT_MEASURED until packing §5b. Prompt it AFTER
  the r6 merge, once `lane/w1-r6` is fast-forwarded to main. The answer
  sheet's Q2 renders (version 4) are pre-review and will be replaced.
- **w3 → WP11b packing follow-ups**: LANDED, `DONE WP11b` at `284ec05`
  on `lane/w3` (two commits, tree clean, report
  `.worktrees/w3/.reports/WP11b-report.md` present, 177 tests OK, doc
  regenerated not edited). Results: the DTP301120 closes in 0 of 48
  arc-plus runs (+1.5 already fails the M1 gate, 49.42 > 49.00); no REF
  tab route stays inside the cavity, so `REF_end_wall_slot` (2.50 wide,
  1.05 through, 0.31 high at u 7.25–9.75, s 38.20–39.25) is published in
  `docs/fab/packing-v2.md` §5 on `lane/w3` for WP14 to cut; the winner
  is unchanged. Note sent 23:05 to w1 to cut that slot. Second `DONE
  WP11b` at `90d6d0a` (Jauch LP501218JH as a third cell: 0 of 72 runs
  close, packed height 5.9, so no buyable cell closes inside the brief's
  box). Third `DONE WP11b` at `9f8136f`: LID_Y 9.5–10.5 and widths
  20–22 do not help either (0 of 108), because the buyable cells fail on
  length along the body (antenna zone, SIG1 standoff), not on height.
  Only a cell inside the 15.6 × 10.4 × 5.2 envelope packs. Fourth
  `DONE WP11b` at `bcecc83` (§1e): the winner body does NOT close with
  the real 17.0 mm 501015 pack (`BQ25100 overlaps header`; at +1.5 arc
  only the M1 gate fails, 49.42 > 49.00 at M1 52); the marketplace 501012
  pack closes on 8 bodies, smallest w19 × y8, outer 9.0, chord 47.90.
  Reading (Q69): shell and board stay on w20 × y8, the carried cell is
  the 501012 pack, the purchase route is Rolf's.
- **w3 → WP11c courtyards** (`tasks/WP11c-courtyards.md`, main
  `e2c7f09`): RUNNING on `lane/w3` on top of `bcecc83`, prompted after
  the verdict with the decisions 70–74 amendment: re-pack with the real
  KiCad courtyards, the JLC assembly edge and copper-to-edge 0.30, the
  USB receptacle body and hook root as occupants (Q70), three FR4 ring
  pieces (Q72), two Ø2.7 island holes at the boss sites (Q73), the tab
  fold at R 1.5 with both variants (Q74), Contact rule per the verdict's
  "To WP12c" note; publishes `docs/fab/packing-v2.md` §5b. Waits for
  nothing from me. Report (expected) `.worktrees/w3/.reports/WP11c-report.md`
  → `DONE WP11c`; checked and recorded, merges in round 7;
  then WP12d (w2) and WP14b's second turn (w1) run on §5b.
- **w2 → WP12b board route**: LANDED, `DONE WP12b` at `480e355` on
  `lane/w2` (three commits, tree clean, report
  `.worktrees/w2/.reports/WP12b-report.md` present). Placement from
  packing §5 within 0.1 mm (test), every net synced, GPIO map in
  board-v2 §9, Q68 decoupling, BOM codes from L7 (stock and price
  UNVERIFIED), two stiffeners, Q64 and Q65 stated. Routing FAILED:
  Freerouting hung, a bus fallback wrote shorting copper (DRC 1290, 31
  unconnected), `release.py --routed` refused; its last commit message
  says "routed, released" and it is not. 13 CadRegen failures in its
  venv again (round 5: the lane's pins). The queued 22:58 BOM note then
  ran as a turn: second `DONE WP12b` at `e3e085b` (L7 quotes taken after
  a page re-check; board-v2.md, schematic, patch script, no copper). The
  reviewer was told at 00:32 to merge `lane/w2` at `e3e085b`, not
  `480e355`; the brief file carries the amendment.
- **w2 → WP12c route** (`tasks/WP12c-route.md`): LANDED, `DONE WP12c`
  at `845bac7`, then `f4376ca` on `lane/w2` (tree clean, report
  `.worktrees/w2/.reports/WP12c-report.md` present). Result: the
  shorting bus is dropped (0 tracks, `routed: false`); Freerouting 2.1.0
  headless never writes a SES on Java 21 on this Mac; the lane's own A*
  trial (770 DRC errors) was discarded; with ZERO tracks the board has
  128 DRC errors and 132 unconnected because the packing table's part
  envelopes are smaller than the real courtyards (J3 vs SW1, J2 vs J4,
  U5 vs J4, U3 in U1's courtyard, U2 at the edge, R25/C10 in the RF
  notch, Contact 1.0 mm vs 0402 gaps and J3's pitch), recorded as Q77
  and handed to WP11c. `hardware/board/route.md` (absent on main) holds
  the diagnosis. The lane read "continuing from 480e355" literally and
  reset its branch, dropping `e3e085b`; on my note it merged
  `origin/lane/w2` back (`f4376ca`), so `e3e085b` is an ancestor again.
  NOT merged (round 7). w2 idles until WP12d (place and route on §5b),
  after `DONE WP11c`.
- **w4 → WP13b receiver**: LANDED, `DONE WP13b` at `e7c366a` on
  `lane/w4` (five commits, tree clean, report
  `.worktrees/w4/.reports/WP13b-report.md` present, 179 tests OK with 21
  skips, `arduino-cli compile` exit 0). Delivered
  `src/elicio/receiver_v2.py` (absent on main), `elicio receive` and
  `receive-check` in the CLI, `tests/test_receiver_v2.py` (absent on
  main) with fixtures, `firmware/src/board_pins.h` aligned to board-v2 §9
  (w2's table matches), `docs/fab/receiver-v2.md` (absent on main), the
  `ble` extra in `pyproject.toml` (a seam with w9, which installed
  matplotlib without editing it). Two decisions for the reviewer: the
  dropout rule in `receive-check` against montage §8 line 3.4, and a
  Feather stand-in pin variant. w4 idles; nothing queued.
- **w9 → WP15 Rolf's sheets v2**: LANDED, `DONE WP15` at `018ac58` on
  `lane/w9` (four commits, tree clean, report
  `.worktrees/w9/.reports/WP15-report.md` present, 173 tests OK with 21
  skips for missing CAD extras). Delivered, all absent on main until the
  r6 merge: `docs/fab/measure.md` v2 (exists on main in v1),
  `docs/fab/template.pdf` (absent on main),
  `docs/fab/sheets/m1.svg` to m8 (absent on main),
  `scripts/sheets/template.py` (absent on main),
  `docs/fab/order-board.md` (absent on main),
  `docs/fab/order-shell.md` (absent on main),
  `docs/fab/order-parts.md` (absent on main),
  `docs/fab/assemble.md` (absent on main). Vendor fields wait on WP12b
  and WP14 and say so. w9 idles; nothing queued.
- **w5 → WP17b research v4**: LANDED, `DONE WP17b` at `ea3b9bd` on
  `lane/w5` (one commit, tree clean, report
  `.worktrees/w5/.reports/WP17b-report.md` present). Delivered
  `docs/fab/L7-research-v4.md` (absent on main) with 13 UNVERIFIED tags.
  Findings that moved other lanes: the nRF52840 GPIO absolute maximum is
  VDD + 0.3 V, so the Raspberry Pi Debug Probe (fixed 3.3 V) cannot touch
  an erased 1.8 V part; VTref-sensing probes with page prices are the
  ST-LINK V3 MINIE, Black Magic Probe V2.3 and J-Link EDU Mini (Q64, the
  reviewer verifies the quotes, Rolf still buys nothing until G4). No
  501015 cell in ones anywhere (Q55); buyable with drawings: SparkFun
  DTP301120 and Jauch LP501218JH (bare leads). LCSC resolutions for the
  UNVERIFIED BOM lines (two codes were invalid, one was a 4-pin part).
  JLC3DP colours: natural grey or dyed black (Q30). Notes sent 22:58 to
  w2 (take the BOM codes, fee and datasheet sentences from L7 §3 and §4,
  state the probe limit in board-v2 §4) and to w3 (add the Jauch cell as
  a third case). Second `DONE WP17b` at `ba45071` (L7 §7, cells under
  16 mm): no distributor cell under 16 mm at 30 mAh or more; a 501015
  pack WITH its protection board is 17.0 mm long on the DNK and Benzo
  sheets, so the plan's 15.6 envelope is a bare cell; only marketplace
  501012 packs (13.0 × 10.1 × 5.1 with PCM, 40 mAh, eBay/AliExpress) fit.
  w5 idles; nothing queued.
- **Reviewer r6**: VERDICT IN, `DONE review-r6` at `c7c4e5a` (00:25) on
  `review/r6` (agent `rev6`, Claude Opus 5 high, skip-permissions,
  worktree `.worktrees/review`, brief `tasks/review-r6.md`). Merged all
  six lanes (`lane/w2` at `e3e085b`), fixed 16 defects in per-package review
  commits, verdict MERGE-AFTER-DECISION in
  `.worktrees/review/tasks/reviews/code-r6.md` (absent on main until the
  merge): 206 tests OK on `.[cad]`+`.[ble]`, order 1 identical, Stage B
  v2 exit 3 on Q59 only, the shell's checks were constants and measured
  four fail (V2_CLOSURE no undercut, V2_USB_end ligament −0.89 and the
  receptacle 4.8 outside the face, V2_EDGE_radii R 0.8, V2_WALL_minima),
  captive hex wells fixed, `routed` false, CPL = BOM, §7 look "a printed
  block with a hook". Decisions 69–76 plus my Q77 recorded with readings
  on main at `58ae5b8`. SECOND TURN RUNNING: my footprint-collision note
  reached it after the verdict and it is editing (worktree dirty at
  00:32: assemble, board-v2, shell-v2, receiver-v2, order-board,
  order-shell, cad/v2 drawing, manifest and lateral render,
  `scripts/cad/render.py`). Waits for nothing from me; expect a second
  `DONE review-r6` with a new sha, or `GONE rev6` if it exits. Then: read
  its second report, `git merge --no-ff review/r6` from the clean root
  checkout on main (main moved to `58ae5b8`, so no fast-forward), verify
  order 1 and the tests once on main, fast-forward `lane/w1-r6`,
  `lane/w4`, `lane/w5`, `lane/w9` (ancestors; not `lane/w2`, not
  `lane/w3`), close the review tab (pane `w1B:pS`; `GONE rev6` is then
  expected) and `git worktree remove .worktrees/review`, prompt w1 with
  WP14b, checkpoint, file round 6 into the vault, refresh the answer
  sheet (version 6: the reviewed renders and the note that the drawn
  closure and port fail as drawn).
- No lane is WAITING or BLOCKED as of writing (00:35). `rev5` pushed `GONE` after
  I closed its tab (expected). The `pro` tab is closed; `pro-mcp start
  --name pro` reopens it if another spec dialogue is needed.

## Open

Plan v2 carries claims C1–C16 and gates G1–G8; Q1–Q68 hold the readings.
Outside those:

1. `lane/w1` diverged from `main` at `7df78b5` with 864 SVGs (109 MB,
   pushed). Q56: nobody deletes it but Rolf; round 6 work is on `lane/w1-r6`.
2. The answer sheet (artifact `https://claude.ai/artifact/5e9H1dC5CFHggtiaYtDDeA`)
   is at version 5 (00:05, question 2b the battery route: marketplace
   501012 or a factory sample of the 17 mm pack with M1 ≥ 52.5); version
   4 (23:35) added the two WP14 renders to question 2, marked "before
   review"; version 3 (22:40) brought: M1, body 9.0, ceiling, look and colour,
   China or not and ship-to, the charging rule, priorities, module route,
   probes owned, tools on the Mac, anything else. Answers land in db doc
   `answers/rolf` (ArtifactData `get`), merged with his earlier fields;
   `sheet: 3` marks a v3 save.
3. The vault holds rounds 1 to 5 (page `Wiki/projects/Elicio.md`, stub
   `raw/research/2026-09-17-elicio-round-5-board-packing-firmware.md`,
   vault main `e67a685`); round 6 is filed after its merge.
4. The HANDOFF checker treats any backticked path as a claim; nonexistent
   ones need "(expected)" or "(absent on main)" on the same line.
5. Order 1 (the fit gauge) is not ordered and will not be: plan v2 is one
   order per thing; `docs/fab/cad/v1/` stays byte-identical as the
   regression anchor only.

## Next

- Idle until the second `DONE review-r6` from rev6 (or BLOCKED/GONE for
  it, or `DONE WP11c` from w3, which is checked and recorded but merges
  in round 7); then do the post-verdict steps listed under Reviewer r6
  (merge `review/r6` with `--no-ff`, fast-forward the idle lanes, close
  the review tab, prompt w1 with WP14b, checkpoint, vault, sheet).

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

<!-- Everything below this line is generated. Regenerate it at every
checkpoint with:  python3 ~/.claude/skills/save-state/state.py snapshot
Do not hand-edit ids into it. -->

## Herdr (generated 2026-09-18T00:32:37-04:00 by state.py, herdr 0.9.0, session `default`)
Workspace `w1B` (elicio), 9 tabs. Coordinator: pane `w1B:p1` in tab `w1B:t1`, agent name `elicio`, kind claude, status working, cwd `/Users/rolfie/projects/elicio`.
Coordinator session id `61ba63c7-8fd8-497e-b665-c65cc34e72f6`; transcript `/Users/rolfie/.claude/projects/-Users-rolfie-projects-elicio/61ba63c7-8fd8-497e-b665-c65cc34e72f6.jsonl`.

### Workers nested under the coordinator
| name | kind | status | pane | tab (label) | cwd | tokens | last title |
|---|---|---|---|---|---|---|---|
| w1 | cursor | done | `w1B:pA` | `w1B:tA` (w1) | `/Users/rolfie/projects/elicio/.worktrees/w1` | done=1 lane=WP14 | Lane W1 Instructions |
| w2 | cursor | done | `w1B:pB` | `w1B:tB` (w2) | `/Users/rolfie/projects/elicio/.worktrees/w2` | done=1 lane=WP12c | Lane W2 Instructions |
| w4 | cursor | done | `w1B:pC` | `w1B:tC` (w4) | `/Users/rolfie/projects/elicio/.worktrees/w4` | done=1 lane=WP13b | Lane W4 Instructions |
| w5 | agy | done | `w1B:pD` | `w1B:tD` (w5) | `/Users/rolfie/projects/elicio/.worktrees/w5` | done=1 lane=WP17b |  |
| w9 | cursor | done | `w1B:pE` | `w1B:tE` (w9) | `/Users/rolfie/projects/elicio/.worktrees/w9` | done=1 lane=WP15 | Lane W9 Instructions |
| w3 | cursor | working | `w1B:pR` | `w1B:tR` (w3) | `/Users/rolfie/projects/elicio/.worktrees/w3` | done=1 lane=WP11b | New Package Brief |
| rev6 | claude | working | `w1B:pS` | `w1B:tS` (review) | `/Users/rolfie/projects/elicio/.worktrees/review` | done=1 lane=review-r6 | Review round 6 |

Start lines as they run now (from `pane process-info`), for restarting a worker that is gone:

```bash
herdr agent start w1 --kind cursor --pane <new pane> --parent "$HERDR_PANE_ID" -- --resume 791832d5-f944-40f4-80ec-82deb5c4efca
herdr agent start w2 --kind cursor --pane <new pane> --parent "$HERDR_PANE_ID" -- --resume 137b6bf4-e654-4a43-bc69-e0421552a50c
herdr agent start w4 --kind cursor --pane <new pane> --parent "$HERDR_PANE_ID" -- --resume 3f977624-113c-48fa-b55e-666aa970b9a3
herdr agent start w5 --kind agy --pane <new pane> --parent "$HERDR_PANE_ID" -- --conversation 18235bfb-f5b8-4365-9383-d66c69251f4b --dangerously-skip-permissions --add-dir /Users/rolfie/projects/elicio --effort high --model gemini-3.8-flash-high
herdr agent start w9 --kind cursor --pane <new pane> --parent "$HERDR_PANE_ID" -- --resume ea20ccc0-04da-408f-a016-57766846ee99
herdr agent start w3 --kind cursor --pane <new pane> --parent "$HERDR_PANE_ID" -- --model cursor-grok-4.6-xhigh --force
herdr agent start rev6 --kind claude --pane <new pane> --parent "$HERDR_PANE_ID" -- --model claude-opus-5 --effort high --dangerously-skip-permissions
```

Other workspaces on this server (not yours to touch): `w16` flyonenomics (done), `w1D` ablirated (done), `w1E` jevtest (idle)

### Git
Repo `/Users/rolfie/projects/elicio`, integration branch `main` (0 ahead, 0 behind origin/main).

| worktree | branch | head | dirty files | last commit |
|---|---|---|---|---|
| `/Users/rolfie/projects/elicio` | `main` | 58ae5b8 | 0 | Round 6: record the reviewer's decisions 69 to 76 and the coordinator's Q77 (footprint collisions) with the readings the build follows; WP14b brief |
| `/Users/rolfie/projects/elicio/.worktrees/review` | `review/r6` | c7c4e5a | 14 | review(r6): verdict MERGE-AFTER-DECISION, gates, defects, §7 look, decisions 69–76 |
| `/Users/rolfie/projects/elicio/.worktrees/w1` | `lane/w1-r6` | c3c11d8 | 0 | shell(v2): cut REF_end_wall_slot from packing-v2 §5 |
| `/Users/rolfie/projects/elicio/.worktrees/w2` | `lane/w2` | f4376ca | 0 | merge origin/lane/w2: restore e3e085b after the WP12c reset |
| `/Users/rolfie/projects/elicio/.worktrees/w3` | `lane/w3` | bcecc83 | 0 | packing(v2b): L7 pack tables in packing-v2 |
| `/Users/rolfie/projects/elicio/.worktrees/w4` | `lane/w4` | e7c366a | 0 | receiver(v2): record and check a stream on the Mac |
| `/Users/rolfie/projects/elicio/.worktrees/w5` | `lane/w5` | ba45071 | 0 | research(v4b): cells under 16 mm |
| `/Users/rolfie/projects/elicio/.worktrees/w9` | `lane/w9` | 018ac58 | 0 | sheets(v2): measure, three checkouts, assemble, first load |

Last commits on the integration branch:

```
58ae5b8 Round 6: record the reviewer's decisions 69 to 76 and the coordinator's Q77 (footprint collisions) with the readings the build follows; WP14b brief
e2c7f09 docs(tasks): WP11c brief, pack with the real footprint courtyards
7d5443c review-r6: merge lane/w2 at e3e085b (queued BOM note landed after the pin); handoff notes it
d4b5a93 handoff: round 6 review running (rev6 on review/r6), WP12c routing in parallel on lane/w2
b710ed1 docs(tasks): round 6 review brief (review-r6) and WP12c routing brief
9aa2934 handoff: answer sheet v5 asks the battery route
```

### Record files (newest first)
- handoff: `HANDOFF.md`
- briefs: `tasks/WP14b-shell-v2b.md`, `tasks/WP11c-courtyards.md`, `tasks/review-r6.md`, `tasks/WP12c-route.md`, `tasks/WP17b-research-v4.md`, `tasks/WP15-sheets-v2.md`, `tasks/WP13b-receiver.md`, `tasks/WP12b-board-route.md`, `tasks/WP11b-packing-followups.md`, `tasks/WP14-shell-v2.md`, `tasks/review-r5.md`, `tasks/WP17-research-v3.md`
- verdicts: `tasks/reviews/code-r5.md`, `tasks/reviews/code-r4.md`, `tasks/reviews/code-r3.md`, `tasks/reviews/code-r2.md`, `tasks/reviews/code-r1.md`

### Restore
Run from the coordinator pane after a server restart, or from the fresh coordinator pane that takes over:

```bash
python3 ~/.claude/skills/save-state/state.py restore --from /Users/rolfie/projects/elicio/HANDOFF.json
# the old coordinator conversation, if herdr did not resume it in the pane:
# cd /Users/rolfie/projects/elicio && claude --resume 61ba63c7-8fd8-497e-b665-c65cc34e72f6
```
