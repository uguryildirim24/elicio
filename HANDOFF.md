# Elicio handoff — 2026-09-17 00:35 local

Written by the coordinator in herdr pane `w1B:p1` for whoever coordinates
next: a fresh pane, this pane after a compaction or a server restart, or
Rolf. Read this, then the files it names. Chat history is not a record.
This file supersedes every earlier handoff in the repo.

## Goal

Rolf, 2026-09-16: "we design the airpiece in blender or something and i
get it custom made in china or something", then "for coding after spec is
clean use grok xhigh for the code on as many as lanes as possible, the
usual flow as you know then one opus high to review and commot" (Grok
through Cursor, not the Grok CLI). Done looks like: the order 1 fit-gauge
files approved by Rolf and ordered under the checkout gate (release state
S0 in `docs/fab/plan.md` §9), then S1 once WP5, WP6 and WP7a close. Brief:
`docs/fab/brief.md`. Spec: `docs/fab/plan.md`, signed off by GPT-6 Pro at
`0c5d0eb`. Readings after each review: `docs/fab/open-questions.md`.

## Authority

- Delegated by Rolf, 2026-09-16 night: "i sleep autonomous. i trust your
  decisions and agency don't wait for my input". So: finish rounds, merge,
  open the next round, record his decisions as open questions and keep
  building around them. Never: purchase, sign-up, quote request, upload,
  vendor contact, destructive git.
- Waiting on Rolf, with my reading so he can just say yes:
  1. `open-questions.md` Q6, nut metal inside the cavity. My reading: a
     nickel-free non-ferrous DIN 439 M2.5 thin nut (brass or tinned brass) if
     WP5 part 2 finds one with a drawing; otherwise titanium DIN 934 with the
     wall measured on the printed part before order 2. Not needed before
     order 1.
  2. Requirement 5 in `docs/EARPIECE_DESIGN.md` still says stainless. My
     reading: replace with titanium Grade 2 or 5; his edit, outside the plan.
  3. Plan §10 "Open for Rolf" 1–10: measure M1 first (gate about 51 mm, see
     `docs/fab/measure.md`), which ear (default right), approve the renders
     when WP3 lands, then order 1 under `docs/fab/order1.md`, buy the Stage A
     parts (`docs/STAGE_A_PARTS.md`) to unblock WP7a part 2 and order 2.

## Settled

| round | package | verdict | on the integration branch at | verdict file |
|---|---|---|---|---|
| spec | `docs/fab/plan.md` (9 turns, fable vs GPT-6 Pro) | SIGNED OFF (turn 08) | `0c5d0eb` | `tasks/plan/turns/08-pro.md` |
| r1 | WP9 design record | MERGE-AFTER-DECISION (2 fixes) | `121ccb3` | `tasks/reviews/code-r1.md` |
| r1 | WP1 interface v1 | MERGE-AFTER-DECISION (3 fixes) | `121ccb3` | `tasks/reviews/code-r1.md` |
| r1 | WP4 measure, order1, orders sheets | MERGE-AFTER-DECISION (5 fixes) | `121ccb3` | `tasks/reviews/code-r1.md` |
| r1 | WP5 contacts kit | MERGE-AFTER-DECISION (7 fixes) | `121ccb3` | `tasks/reviews/code-r1.md` |
| r1 | WP2 gauge script and order 1 solids | MERGE-AFTER-DECISION (13 fixes) | `121ccb3` | `tasks/reviews/code-r1.md` |
| r1 | decisions Q1–Q12 recorded | coordinator | `9838573` | `docs/fab/open-questions.md` |

Round 1 gates at merge: 67 tests OK with the 25 CAD tests running, two
reference builds byte-identical to the committed fifteen solids, 184 of 184
manifest checks passed.

## In flight

- **w2** (cursor `cursor-grok-4.6-xhigh`, `lane/w2`, `.worktrees/w2`):
  brief `tasks/WP3-renders.md` (renders, one-page drawing, manifest schema,
  vendored emboss font for Q10). Last told: "Round 2, package WP3 ... do
  everything in it start to finish; end with the DONE or WAITING push".
  Waiting for from the coordinator: nothing. Report expected at
  `.reports/WP3-report.md` (absent). When it lands: check the worktree is
  clean, read the report, hold for the other two.
- **w1** (cursor `cursor-grok-4.6-xhigh`, `lane/w1`, `.worktrees/w1`):
  brief `tasks/WP6-packing.md` (cell SKU, RF zone, packing at max
  dimensions, flat board on the curved floor, lead pads, interface v2, Q6
  status, Q11). Last told: "Round 2, package WP6 ... do everything in it".
  Waiting for from the coordinator: nothing. Report expected at
  `.reports/WP6-report.md` (absent). When it lands: same as w2.
- **w5** (agy `gemini-3.8-flash-high`, `lane/w5`, `.worktrees/w5`): brief
  `tasks/WP7a-protocol.md` (montage procedure and frozen dry-test protocol,
  `docs/fab/montage.md` (expected); part 2, the bench measurement, waits on Stage A
  parts). Last told: the pointer line to that brief. Waiting for from the
  coordinator: nothing. Report expected at `.reports/WP7a-report.md`
  (absent). When it lands: same as w2. Its status is unreliable; the DONE
  push is the only signal.
- **w4** and **w9** (cursor, `lane/w4`, `lane/w9`): idle, no package this
  round, fast-forwarded to main. Candidates for a later package: w4 updates
  the sheets when interface v2 changes them; WP8 (Stage B shell) after WP7a
  part 2.

When all three land: `git worktree add .worktrees/review -b review/r2 main`,
a review tab, `tasks/review-r2.md` (expected) from `tasks/review-code-template.md` with
the three reports pasted in and the seams (renders versus the sheets' file
names, interface v2 versus the manifest's coordinates, Q10 lid hash change,
protocol numbers versus the design record), one fresh reviewer `rev2` on
`claude --model claude-opus-5 --effort high --dangerously-skip-permissions`,
then merge, open questions, checkpoint.

## Open

Plan open items live in `plan.md` §10 (open items 1–4, interface v2
decisions 1–7, Open for Rolf 1–10) and `docs/fab/open-questions.md` Q1–Q12
(Q6 and Q12 are Rolf's). Outside those:

1. WP7a part 2 (bench montage, three coordinates) — open because Stage A
   parts are unbought; Rolf's purchase.
2. WP8 Stage B shell (order 2 files) — open because it takes WP7a's
   coordinates and WP6's interface v2.
3. WP5 part 2 (SKU drawings, nut candidate per Q6, live prices) — open
   because it belongs at purchase time, before S1.
4. Wiki file-back of round results — open because the vault
  (`~/Documents/obsidian/rolfiersbox`, page `Wiki/projects/Elicio.md`) holds
  the plan as of 2026-09-16 and not Q1–Q12 or the order 1 status; do it
  after round 2 merges, in one `vault run`.
5. Order 1 itself — open because it needs Rolf's render approval and his M1.

## Next

- Idle for the three DONE pushes (WP3, WP6, WP7a); on the third, open review
  round 2 as written under In flight.

## Traps

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
- `sed -i ''` fails on non-ASCII patterns → edit with python.
- A relative screenshot path lands in the repo root → absolute scratchpad paths.
- Do not `cd` into worktrees from the coordinator shell → `git -C` with the worktree path.
- `herdr agent read` output is plain text, not JSON → do not pipe it to a
  JSON parser.

<!-- Everything below this line is generated. Regenerate it at every
checkpoint with:  python3 ~/.claude/skills/save-state/state.py snapshot
Do not hand-edit ids into it. -->

## Herdr (generated 2026-09-17T00:31:17-04:00 by state.py, herdr 0.9.0, session `default`)
Workspace `w1B` (elicio), 6 tabs. Coordinator: pane `w1B:p1` in tab `w1B:t1`, agent name `elicio`, kind claude, status working, cwd `/Users/rolfie/projects/elicio`.
Coordinator session id `61ba63c7-8fd8-497e-b665-c65cc34e72f6`; transcript `/Users/rolfie/.claude/projects/-Users-rolfie-projects-elicio/61ba63c7-8fd8-497e-b665-c65cc34e72f6.jsonl`.

### Workers nested under the coordinator
| name | kind | status | pane | tab (label) | cwd | tokens | last title |
|---|---|---|---|---|---|---|---|
| w1 | cursor | working | `w1B:pA` | `w1B:tA` (w1) | `/Users/rolfie/projects/elicio/.worktrees/w1` | done=1 lane=WP1 | Lane W1 Instructions |
| w2 | cursor | working | `w1B:pB` | `w1B:tB` (w2) | `/Users/rolfie/projects/elicio/.worktrees/w2` | done=1 lane=WP2 | Lane W2 Instructions |
| w4 | cursor | done | `w1B:pC` | `w1B:tC` (w4) | `/Users/rolfie/projects/elicio/.worktrees/w4` | done=1 lane=WP4 | Lane W4 Instructions |
| w5 | agy | working | `w1B:pD` | `w1B:tD` (w5) | `/Users/rolfie/projects/elicio/.worktrees/w5` | done=1 lane=WP5 |  |
| w9 | cursor | done | `w1B:pE` | `w1B:tE` (w9) | `/Users/rolfie/projects/elicio/.worktrees/w9` | done=1 lane=WP9 | Lane W9 Instructions |

Start lines as they run now (from `pane process-info`), for restarting a worker that is gone:

```bash
herdr agent start w1 --kind cursor --pane <new pane> --parent "$HERDR_PANE_ID" -- --model cursor-grok-4.6-xhigh --force
herdr agent start w2 --kind cursor --pane <new pane> --parent "$HERDR_PANE_ID" -- --model cursor-grok-4.6-xhigh --force
herdr agent start w4 --kind cursor --pane <new pane> --parent "$HERDR_PANE_ID" -- --model cursor-grok-4.6-xhigh --force
herdr agent start w5 --kind agy --pane <new pane> --parent "$HERDR_PANE_ID" -- --dangerously-skip-permissions --add-dir /Users/rolfie/projects/elicio --effort high --model gemini-3.8-flash-high
herdr agent start w9 --kind cursor --pane <new pane> --parent "$HERDR_PANE_ID" -- --model cursor-grok-4.6-xhigh --force
```

Other workspaces on this server (not yours to touch): `w16` flyonenomics (working), `w1D` ablirated (done)

### Git
Repo `/Users/rolfie/projects/elicio`, integration branch `main` (0 ahead, 0 behind origin/main).

| worktree | branch | head | dirty files | last commit |
|---|---|---|---|---|
| `/Users/rolfie/projects/elicio` | `main` | 1450581 | 0 | Phase 1 round 2: briefs for WP3 (renders, drawing), WP6 (packing, interface v2), WP7a part 1 (frozen protocol) |
| `/Users/rolfie/projects/elicio/.worktrees/w1` | `lane/w1` | 1450581 | 0 | Phase 1 round 2: briefs for WP3 (renders, drawing), WP6 (packing, interface v2), WP7a part 1 (frozen protocol) |
| `/Users/rolfie/projects/elicio/.worktrees/w2` | `lane/w2` | 1450581 | 0 | Phase 1 round 2: briefs for WP3 (renders, drawing), WP6 (packing, interface v2), WP7a part 1 (frozen protocol) |
| `/Users/rolfie/projects/elicio/.worktrees/w4` | `lane/w4` | 1450581 | 0 | Phase 1 round 2: briefs for WP3 (renders, drawing), WP6 (packing, interface v2), WP7a part 1 (frozen protocol) |
| `/Users/rolfie/projects/elicio/.worktrees/w5` | `lane/w5` | 1450581 | 0 | Phase 1 round 2: briefs for WP3 (renders, drawing), WP6 (packing, interface v2), WP7a part 1 (frozen protocol) |
| `/Users/rolfie/projects/elicio/.worktrees/w9` | `lane/w9` | 1450581 | 0 | Phase 1 round 2: briefs for WP3 (renders, drawing), WP6 (packing, interface v2), WP7a part 1 (frozen protocol) |

Last commits on the integration branch:

```
1450581 Phase 1 round 2: briefs for WP3 (renders, drawing), WP6 (packing, interface v2), WP7a part 1 (frozen protocol)
9838573 Round 1: record the reviewer's twelve decisions as open questions
121ccb3 review(r1): verdict MERGE-AFTER-DECISION, gates, defects and decisions
6caa0ed review(WP2): say in the manifest where the bow came from
42e51d5 review(WP9): drop an added reason from row 9 and reopen question 3
6e92eee review(WP1): align the ISO 4032 note and dome note with §2.3 and §12
```

### Record files (newest first)
- briefs: `tasks/WP7a-protocol.md`, `tasks/WP6-packing.md`, `tasks/WP3-renders.md`, `tasks/phase1-common.md`, `tasks/review-r1.md`, `tasks/review-code-template.md`, `tasks/WP9-record.md`, `tasks/WP5-contacts.md`, `tasks/WP4-sheets.md`, `tasks/WP2-gauge.md`, `tasks/WP1-interface.md`, `tasks/L4-pod.md`
- verdicts: `tasks/reviews/code-r1.md`

### Restore
Run from the coordinator pane after a server restart, or from the fresh coordinator pane that takes over:

```bash
python3 ~/.claude/skills/save-state/state.py restore --from /Users/rolfie/projects/elicio/HANDOFF.json
# the old coordinator conversation, if herdr did not resume it in the pane:
# cd /Users/rolfie/projects/elicio && claude --resume 61ba63c7-8fd8-497e-b665-c65cc34e72f6
```
