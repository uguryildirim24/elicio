# HANDOFF — Elicio coordinator

Written 2026-09-18 00:50 (America/New_York) by the coordinator (`elicio`,
pane `w1B:p1`) right after merging round 6 (`110a79b`) and opening round
7. Rolf is asleep; the delegation below is in force.

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
     The first shell pictures are on the sheet (version 6) with the
     reviewer's findings: the size is right, the closure and the USB end
     fail as drawn and are being redone (WP14b).
  1b. Q69 the battery route (sheet question 2b): the marketplace 501012
     pack (13.0 × 10.1 × 5.1 with PCM, 40 mAh, no drawing) or a factory
     sample of the real 17.0 mm 501015 pack with M1 ≥ 52.5 and a body 1.5
     longer. Reading: the record carries the 501012 pack in the w20 × y8
     pocket; nothing is bought.
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
| r7 | briefs WP11c, WP14b | coordinator | `e2c7f09`, `58ae5b8` | `tasks/WP11c-courtyards.md`, `tasks/WP14b-shell-v2b.md` |

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

Round 7 opened 2026-09-18 00:45 on the merged main `110a79b`: two lanes
working, four idle, no reviewer yet. Every lane sits on its own branch in
its own worktree; `lane/w1-r6`, `lane/w4`, `lane/w5`, `lane/w9` are
fast-forwarded to `110a79b`.

- **w1 → WP14b shell v2, second pass** (`tasks/WP14b-shell-v2b.md`, main
  `58ae5b8`): RUNNING since 00:45 on `lane/w1-r6` at `110a79b`; prompt:
  read the brief in full and do it. Closure per Q71 (concealed tail M2.5
  titanium screw into a boss plus the hinge lip, no snaps), a lofted lid
  lapping the wall tops with R ≥ 1.0 all round and no flat station over
  3 mm, hook root blend per Q76, every check measured on the built solid,
  the USB row NOT_MEASURED until packing §5b (Q70). Waits for nothing
  from me. Report (expected) `.worktrees/w1/.reports/WP14b-report.md` →
  `DONE WP14b`; then a second turn once WP11c publishes §5b (USB wall,
  tab fold pockets, island bosses); merges in round 7's review.
- **w3 → WP11c courtyards** (`tasks/WP11c-courtyards.md`, main
  `e2c7f09`): RUNNING on `lane/w3` on top of `bcecc83` (not
  fast-forwarded; it merges main itself if it needs the reviewer's §5
  cell record), prompted after the verdict with the decisions 70–74
  amendment: re-pack with the real KiCad courtyards, the JLC assembly
  edge and copper-to-edge 0.30, the USB receptacle body and hook root as
  occupants (Q70), three FR4 ring pieces (Q72), two Ø2.7 island holes at
  the boss sites (Q73), the tab fold at R 1.5 with both variants (Q74),
  the Contact rule per the verdict's "To WP12c" note; publishes
  `docs/fab/packing-v2.md` §5b. Waits for nothing from me. Report
  (expected) `.worktrees/w3/.reports/WP11c-report.md` → `DONE WP11c`;
  then WP12d (w2) and WP14b's second turn (w1) run on §5b.
- **w2**: idle on `lane/w2` at `f4376ca`, which holds WP12c (bus dropped,
  `routed: false`, `hardware/board/route.md` (absent on main) with the
  zero-track DRC diagnosis; recorded as Q77) on top of the merged
  `e3e085b`. NOT merged and not fast-forwarded (not an ancestor). Next:
  WP12d after `DONE WP11c`: merge main, place from §5b, route with
  Freerouting 2.4.1 or its own router to DRC 0, R1–R3 on the island, J3
  pads Ø1.5, one net per tab.
- **w4**: idle on `lane/w4` at `110a79b`. Next: WP13c (Q75, small): a 3.4
  dropout reports and does not stop S2; `docs/fab/receiver-v2.md` and the
  montage sheet wording; brief not yet written.
- **w5** (agy): idle on `lane/w5` at `110a79b`. Next: WP17c only if a lane
  needs a page read (Freerouting 2.4.1 headless on macOS, the M2.5
  titanium screw source for Q71); nothing queued.
- **w9**: idle on `lane/w9` at `110a79b`. Next: WP15b, the sheets refilled
  after WP14b and WP12d settle the shell and board numbers; nothing
  queued.
- **Reviewer r6**: CLOSED. Verdict MERGE-AFTER-DECISION at `c7c4e5a`,
  second turn `f9e4144` (zero-track DRC confirmed, UTF-8 in
  `scripts/board/release.py`), third turn `f407b12` (decision numbers
  follow open-questions Q69–Q77); merged into main at `110a79b` with
  `--no-ff`, HANDOFF kept from main. Tab `w1B:tS` closed (herdr pushed
  `GONE rev6`, expected), worktree removed, branch `review/r6` kept.
  Round 7's reviewer is a fresh Opus 5 high pane after WP11c, WP14b,
  WP12d and WP13c land.
- No lane is WAITING or BLOCKED as of writing (00:50).

## Open

Plan v2 carries claims C1–C16 and gates G1–G8; Q1–Q68 hold the readings.
Outside those:

1. `lane/w1` diverged from `main` at `7df78b5` with 864 SVGs (109 MB,
   pushed). Q56: nobody deletes it but Rolf; round 6 work is on `lane/w1-r6`.
2. The answer sheet (artifact `https://claude.ai/artifact/5e9H1dC5CFHggtiaYtDDeA`)
   is at version 6 (00:45: the reviewed renders with the review's labels
   in question 2, the paragraph says the latch and the port end fail as
   drawn and are being redone, the banner counts the second review, a
   note under question 4 that "printed block" is the finding, not the
   target); version 5 (00:05) added question 2b the battery route;
   version 4 (23:35) the first WP14 renders; version 3 (22:40) brought: M1, body 9.0, ceiling, look and colour,
   China or not and ship-to, the charging rule, priorities, module route,
   probes owned, tools on the Mac, anything else. Answers land in db doc
   `answers/rolf` (ArtifactData `get`), merged with his earlier fields;
   `sheet: 3` marks a v3 save.
3. The vault holds rounds 1 to 5 (page `Wiki/projects/Elicio.md`, stub
   `raw/research/2026-09-17-elicio-round-5-board-packing-firmware.md`,
   vault main `e67a685`); round 6 is being filed now (a `vault run start
   edit --by claude` run; if it is still open at resume, finish or abort
   it before anything else in the vault).
4. The HANDOFF checker treats any backticked path as a claim; nonexistent
   ones need "(expected)" or "(absent on main)" on the same line.
5. Order 1 (the fit gauge) is not ordered and will not be: plan v2 is one
   order per thing; `docs/fab/cad/v1/` stays byte-identical as the
   regression anchor only.

## Next

- Idle until `DONE WP11c` (w3) or `DONE WP14b` (w1), or BLOCKED/GONE for
  either (a DONE is checked: report present, tree clean; then read);
  after `DONE WP11c` brief WP12d for w2 and WP14b's second turn for w1;
  in the gap write and send WP13c (Q75) to w4; when WP11c, WP14b, WP12d
  and WP13c have landed, open review r7 (fresh Opus 5 high pane,
  `tasks/review-r7.md` (expected) from `tasks/review-code-template.md`).

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

## Herdr (generated 2026-09-18T00:39:14-04:00 by state.py, herdr 0.9.0, session `default`)
Workspace `w1B` (elicio), 8 tabs. Coordinator: pane `w1B:p1` in tab `w1B:t1`, agent name `elicio`, kind claude, status working, cwd `/Users/rolfie/projects/elicio`.
Coordinator session id `61ba63c7-8fd8-497e-b665-c65cc34e72f6`; transcript `/Users/rolfie/.claude/projects/-Users-rolfie-projects-elicio/61ba63c7-8fd8-497e-b665-c65cc34e72f6.jsonl`.

### Workers nested under the coordinator
| name | kind | status | pane | tab (label) | cwd | tokens | last title |
|---|---|---|---|---|---|---|---|
| w1 | cursor | working | `w1B:pA` | `w1B:tA` (w1) | `/Users/rolfie/projects/elicio/.worktrees/w1` | done=1 lane=WP14 | Lane W1 Instructions |
| w2 | cursor | done | `w1B:pB` | `w1B:tB` (w2) | `/Users/rolfie/projects/elicio/.worktrees/w2` | done=1 lane=WP12c | Lane W2 Instructions |
| w4 | cursor | done | `w1B:pC` | `w1B:tC` (w4) | `/Users/rolfie/projects/elicio/.worktrees/w4` | done=1 lane=WP13b | Lane W4 Instructions |
| w5 | agy | done | `w1B:pD` | `w1B:tD` (w5) | `/Users/rolfie/projects/elicio/.worktrees/w5` | done=1 lane=WP17b |  |
| w9 | cursor | done | `w1B:pE` | `w1B:tE` (w9) | `/Users/rolfie/projects/elicio/.worktrees/w9` | done=1 lane=WP15 | Lane W9 Instructions |
| w3 | cursor | working | `w1B:pR` | `w1B:tR` (w3) | `/Users/rolfie/projects/elicio/.worktrees/w3` | done=1 lane=WP11b | New Package Brief |

Start lines as they run now (from `pane process-info`), for restarting a worker that is gone:

```bash
herdr agent start w1 --kind cursor --pane <new pane> --parent "$HERDR_PANE_ID" -- --resume 791832d5-f944-40f4-80ec-82deb5c4efca
herdr agent start w2 --kind cursor --pane <new pane> --parent "$HERDR_PANE_ID" -- --resume 137b6bf4-e654-4a43-bc69-e0421552a50c
herdr agent start w4 --kind cursor --pane <new pane> --parent "$HERDR_PANE_ID" -- --resume 3f977624-113c-48fa-b55e-666aa970b9a3
herdr agent start w5 --kind agy --pane <new pane> --parent "$HERDR_PANE_ID" -- --conversation 18235bfb-f5b8-4365-9383-d66c69251f4b --dangerously-skip-permissions --add-dir /Users/rolfie/projects/elicio --effort high --model gemini-3.8-flash-high
herdr agent start w9 --kind cursor --pane <new pane> --parent "$HERDR_PANE_ID" -- --resume ea20ccc0-04da-408f-a016-57766846ee99
herdr agent start w3 --kind cursor --pane <new pane> --parent "$HERDR_PANE_ID" -- --model cursor-grok-4.6-xhigh --force
```

Other workspaces on this server (not yours to touch): `w16` flyonenomics (done), `w1D` ablirated (done), `w1E` jevtest (idle)

### Git
Repo `/Users/rolfie/projects/elicio`, integration branch `main` (0 ahead, 0 behind origin/main).

| worktree | branch | head | dirty files | last commit |
|---|---|---|---|---|
| `/Users/rolfie/projects/elicio` | `main` | 110a79b | 1 | Merge review/r6 at f407b12: round 6 (WP11b packing follow-ups, WP14 shell v2, WP17b research v4, WP13b receiver v2, WP15 Rolf's sheets v2, WP12b board place) after the reviewer's fixes; verdict MERGE-AFTER-DECISION, decisions Q69 to Q77 |
| `/Users/rolfie/projects/elicio/.worktrees/w1` | `lane/w1-r6` | 110a79b | 0 | Merge review/r6 at f407b12: round 6 (WP11b packing follow-ups, WP14 shell v2, WP17b research v4, WP13b receiver v2, WP15 Rolf's sheets v2, WP12b board place) after the reviewer's fixes; verdict MERGE-AFTER-DECISION, decisions Q69 to Q77 |
| `/Users/rolfie/projects/elicio/.worktrees/w2` | `lane/w2` | f4376ca | 0 | merge origin/lane/w2: restore e3e085b after the WP12c reset |
| `/Users/rolfie/projects/elicio/.worktrees/w3` | `lane/w3` | bcecc83 | 2 | packing(v2b): L7 pack tables in packing-v2 |
| `/Users/rolfie/projects/elicio/.worktrees/w4` | `lane/w4` | 110a79b | 0 | Merge review/r6 at f407b12: round 6 (WP11b packing follow-ups, WP14 shell v2, WP17b research v4, WP13b receiver v2, WP15 Rolf's sheets v2, WP12b board place) after the reviewer's fixes; verdict MERGE-AFTER-DECISION, decisions Q69 to Q77 |
| `/Users/rolfie/projects/elicio/.worktrees/w5` | `lane/w5` | 110a79b | 0 | Merge review/r6 at f407b12: round 6 (WP11b packing follow-ups, WP14 shell v2, WP17b research v4, WP13b receiver v2, WP15 Rolf's sheets v2, WP12b board place) after the reviewer's fixes; verdict MERGE-AFTER-DECISION, decisions Q69 to Q77 |
| `/Users/rolfie/projects/elicio/.worktrees/w9` | `lane/w9` | 110a79b | 0 | Merge review/r6 at f407b12: round 6 (WP11b packing follow-ups, WP14 shell v2, WP17b research v4, WP13b receiver v2, WP15 Rolf's sheets v2, WP12b board place) after the reviewer's fixes; verdict MERGE-AFTER-DECISION, decisions Q69 to Q77 |

Last commits on the integration branch:

```
110a79b Merge review/r6 at f407b12: round 6 (WP11b packing follow-ups, WP14 shell v2, WP17b research v4, WP13b receiver v2, WP15 Rolf's sheets v2, WP12b board place) after the reviewer's fixes; verdict MERGE-AFTER-DECISION, decisions Q69 to Q77
f407b12 review(r6): decision numbers follow open-questions Q69 to Q77
231e2d1 handoff: In flight and Next after the round 6 verdict (rev6 second turn, WP12c landed un-routed, WP11c running, WP14b brief waits for the merge)
f9e4144 review(r6): coordinator note 2: re-pack with real courtyards is decision 70; zero-track DRC confirmed
59c7945 review(WP12b): release job and its test read and write UTF-8 explicitly
fdac6b2 handoff: round 6 verdict in (c7c4e5a), rev6 on a second turn for the footprint collisions; WP12c landed un-routed (Q77), WP11c running on w3, WP14b brief waits for the merge
```

### Record files (newest first)
- handoff: `HANDOFF.md`
- briefs: `tasks/WP14b-shell-v2b.md`, `tasks/WP11c-courtyards.md`, `tasks/review-r6.md`, `tasks/WP12c-route.md`, `tasks/WP17b-research-v4.md`, `tasks/WP15-sheets-v2.md`, `tasks/WP13b-receiver.md`, `tasks/WP12b-board-route.md`, `tasks/WP11b-packing-followups.md`, `tasks/WP14-shell-v2.md`, `tasks/review-r5.md`, `tasks/WP17-research-v3.md`
- verdicts: `tasks/reviews/code-r6.md`, `tasks/reviews/code-r5.md`, `tasks/reviews/code-r4.md`, `tasks/reviews/code-r3.md`, `tasks/reviews/code-r2.md`, `tasks/reviews/code-r1.md`

### Restore
Run from the coordinator pane after a server restart, or from the fresh coordinator pane that takes over:

```bash
python3 ~/.claude/skills/save-state/state.py restore --from /Users/rolfie/projects/elicio/HANDOFF.json
# the old coordinator conversation, if herdr did not resume it in the pane:
# cd /Users/rolfie/projects/elicio && claude --resume 61ba63c7-8fd8-497e-b665-c65cc34e72f6
```
