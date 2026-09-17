# Elicio handoff — 2026-09-17 02:20 local

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
`0c5d0eb`. Readings after each review: `docs/fab/open-questions.md`
(Q1–Q19).

## Authority

- Delegated by Rolf, 2026-09-16 night: "i sleep autonomous. i trust your
  decisions and agency don't wait for my input". So: finish rounds, merge,
  open the next round, record his decisions as open questions and keep
  building around them. Never: purchase, sign-up, quote request, upload,
  vendor contact, destructive git.
- Waiting on Rolf, with my reading so he can just say yes
  (all in `docs/fab/open-questions.md`):
  1. Q6 nut metal inside the cavity. My reading: a nickel-free non-ferrous
     DIN 439 M2.5 thin nut if WP5b finds one with a drawing; otherwise
     titanium DIN 934 with the wall measured on the printed part. Not
     needed before order 1.
  2. Q13 lug tab: my reading, the tab ends under its own pad; WP5b's lug
     drawing gives the length. He confirms, or keeps 7 mm and the pads move.
  3. Q15 packing escalation: his by the plan; WP6b is building the sheet
     with options B, C, E and a recommendation. He picks from the sheet.
  4. Q17 reference site: answered by wearing the gauge (is the mark on
     bone). Q18 cell: buy one 501015 cell with the Stage A parts; the
     plan's hand fold stands until measured. Q19: accept the frozen
     protocol numbers or edit before Stage A data.
  5. Requirement 5 in `docs/EARPIECE_DESIGN.md` still says stainless. My
     reading: titanium Grade 2 or 5; his edit.
  6. Plan §10 "Open for Rolf" 1–10: measure M1 first (gate about 51 mm,
     `docs/fab/measure.md`), which ear (default right), approve the renders
     (`docs/fab/cad/v1/render_medial.png`, `render_lateral.png`,
     `drawing.pdf`), then order 1 under `docs/fab/order1.md`, buy the
     Stage A parts (`docs/STAGE_A_PARTS.md`).

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

Round 2 gates at merge: 83 tests OK none skipped; fifteen solids
byte-identical twice and equal to the committed files; renders, drawing
and placement drawing byte-identical; manifest validator passes and fails
on a removed key.

## In flight

- **w1** (cursor `cursor-grok-4.6-xhigh`, `lane/w1`, `.worktrees/w1`):
  brief `tasks/WP6b-packing-options.md` (option A under Q13, options B, C,
  E with drawings, `docs/fab/packing-options.md` (expected) decision sheet for Rolf,
  `placement.py --option`). Last told: "Round 3, package WP6b ... do
  everything in it start to finish; end with the DONE or WAITING push".
  Waiting for from the coordinator: nothing. Report expected at
  `.reports/WP6b-report.md` (absent). When it lands: check the worktree is
  clean, read the report, hold for w5.
- **w5** (agy `gemini-3.8-flash-high`, `lane/w5`, `.worktrees/w5`): brief
  `tasks/WP5b-drawings.md` (lug drawing for Q13, nut candidates for Q6,
  dome drawings for Q7, in `docs/fab/contacts.md`). Last told: the pointer
  line to that brief. Waiting for from the coordinator: nothing. Report
  expected at `.reports/WP5b-report.md` (absent). Status unreliable; the
  DONE push is the only signal.
- **w2**, **w4**, **w9** (cursor): idle, no package this round,
  fast-forwarded to main. w2 holds the CAD context for WP8 later.

When both land: `git worktree add .worktrees/review -b review/r3 main`, a
review tab, `tasks/review-r3.md` (expected) from `tasks/review-code-template.md` with
both reports and the seams (WP6b's tab geometry against WP5b's lug
drawing; the option drawings against the conflict checker; every price
and drawing number with URL and date), one fresh reviewer `rev3` on
`claude --model claude-opus-5 --effort high --dangerously-skip-permissions`,
then merge, open questions from 20, checkpoint. Also check
`herdr tab list --workspace w1B` after the verdict: the round 2 reviewer
spawned a helper agy lane whose tab outlived it.

## Open

Plan open items live in `plan.md` §10 and `docs/fab/open-questions.md`
Q1–Q19 (Rolf's: Q6, Q12, Q13 confirm, Q15, Q17, Q18, Q19). Outside those:

1. WP7a part 2 (bench montage, three coordinates) — open because Stage A
   parts are unbought; Rolf's purchase.
2. WP8 Stage B shell (order 2 files) — open because it takes Rolf's
   packing pick (Q15), the cell answer (Q18) and WP7a's coordinates.
3. Order 1 itself — open because it needs Rolf's render approval and his M1.
   The vault (`~/Documents/obsidian/rolfiersbox`, page
   `Wiki/projects/Elicio.md`) has rounds 1 and 2 and seven questions for
   Rolf in its Open questions form as of 2026-09-17; round 3 is not filed
   back yet.
4. `docs/fab/L2-vendors.md` says no bureau prints conductive TPU, later
   found wrong — open because nobody has corrected the lane report; low
   priority, the plan does not use conductive TPU.

## Next

- Idle for the two DONE pushes (WP6b, WP5b); on the second, open review
  round 3 as written under In flight.

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
- `sed -i ''` fails on non-ASCII patterns → edit with python.
- A relative screenshot path lands in the repo root → absolute scratchpad paths.
- Do not `cd` into worktrees from the coordinator shell → `git -C` with the
  worktree path.
- `herdr agent read` output is plain text, not JSON → do not pipe it to a
  JSON parser.

<!-- Everything below this line is generated. Regenerate it at every
checkpoint with:  python3 ~/.claude/skills/save-state/state.py snapshot
Do not hand-edit ids into it. -->

## Herdr (generated 2026-09-17T01:37:57-04:00 by state.py, herdr 0.9.0, session `default`)
Workspace `w1B` (elicio), 6 tabs. Coordinator: pane `w1B:p1` in tab `w1B:t1`, agent name `elicio`, kind claude, status working, cwd `/Users/rolfie/projects/elicio`.
Coordinator session id `61ba63c7-8fd8-497e-b665-c65cc34e72f6`; transcript `/Users/rolfie/.claude/projects/-Users-rolfie-projects-elicio/61ba63c7-8fd8-497e-b665-c65cc34e72f6.jsonl`.

### Workers nested under the coordinator
| name | kind | status | pane | tab (label) | cwd | tokens | last title |
|---|---|---|---|---|---|---|---|
| w1 | cursor | working | `w1B:pA` | `w1B:tA` (w1) | `/Users/rolfie/projects/elicio/.worktrees/w1` | done=1 lane=WP6 | Lane W1 Instructions |
| w2 | cursor | done | `w1B:pB` | `w1B:tB` (w2) | `/Users/rolfie/projects/elicio/.worktrees/w2` | done=1 lane=WP3 | Lane W2 Instructions |
| w4 | cursor | done | `w1B:pC` | `w1B:tC` (w4) | `/Users/rolfie/projects/elicio/.worktrees/w4` | done=1 lane=WP4 | Lane W4 Instructions |
| w5 | agy | working | `w1B:pD` | `w1B:tD` (w5) | `/Users/rolfie/projects/elicio/.worktrees/w5` | done=1 lane=WP7a |  |
| w9 | cursor | done | `w1B:pE` | `w1B:tE` (w9) | `/Users/rolfie/projects/elicio/.worktrees/w9` | done=1 lane=WP9 | Lane W9 Instructions |

Start lines as they run now (from `pane process-info`), for restarting a worker that is gone:

```bash
herdr agent start w1 --kind cursor --pane <new pane> --parent "$HERDR_PANE_ID" -- --model cursor-grok-4.6-xhigh --force
herdr agent start w2 --kind cursor --pane <new pane> --parent "$HERDR_PANE_ID" -- --model cursor-grok-4.6-xhigh --force
herdr agent start w4 --kind cursor --pane <new pane> --parent "$HERDR_PANE_ID" -- --model cursor-grok-4.6-xhigh --force
herdr agent start w5 --kind agy --pane <new pane> --parent "$HERDR_PANE_ID" -- --dangerously-skip-permissions --add-dir /Users/rolfie/projects/elicio --effort high --model gemini-3.8-flash-high
herdr agent start w9 --kind cursor --pane <new pane> --parent "$HERDR_PANE_ID" -- --model cursor-grok-4.6-xhigh --force
```

Other workspaces on this server (not yours to touch): `w16` flyonenomics (done), `w1D` ablirated (done)

### Git
Repo `/Users/rolfie/projects/elicio`, integration branch `main` (0 ahead, 0 behind origin/main).

| worktree | branch | head | dirty files | last commit |
|---|---|---|---|---|
| `/Users/rolfie/projects/elicio` | `main` | 9b264a5 | 0 | Phase 1 round 3: briefs for WP6 round 3 (packing decision sheet) and WP5 part 2 (lug, nut, dome drawings) |
| `/Users/rolfie/projects/elicio/.worktrees/w1` | `lane/w1` | 9b264a5 | 0 | Phase 1 round 3: briefs for WP6 round 3 (packing decision sheet) and WP5 part 2 (lug, nut, dome drawings) |
| `/Users/rolfie/projects/elicio/.worktrees/w2` | `lane/w2` | c704145 | 0 | Round 2: record the reviewer's decisions 13 to 19 as open questions Q13 to Q19 |
| `/Users/rolfie/projects/elicio/.worktrees/w4` | `lane/w4` | c704145 | 0 | Round 2: record the reviewer's decisions 13 to 19 as open questions Q13 to Q19 |
| `/Users/rolfie/projects/elicio/.worktrees/w5` | `lane/w5` | 9b264a5 | 0 | Phase 1 round 3: briefs for WP6 round 3 (packing decision sheet) and WP5 part 2 (lug, nut, dome drawings) |
| `/Users/rolfie/projects/elicio/.worktrees/w9` | `lane/w9` | c704145 | 0 | Round 2: record the reviewer's decisions 13 to 19 as open questions Q13 to Q19 |

Last commits on the integration branch:

```
9b264a5 Phase 1 round 3: briefs for WP6 round 3 (packing decision sheet) and WP5 part 2 (lug, nut, dome drawings)
c704145 Round 2: record the reviewer's decisions 13 to 19 as open questions Q13 to Q19
443a178 review: round 2 verdict, MERGE-AFTER-DECISION
7bc9f24 review(WP6): note the DNK 501015 drawing is marked PRELIMINARY
0bad5af review(WP6): cell fold thickness against the pocket, and what a longer pocket moves
93ab908 review(WP6): lug tabs in the free mask, two clamp arrays, packing not confirmed
```

### Record files (newest first)
- handoff: `HANDOFF.md`
- briefs: `tasks/WP5b-drawings.md`, `tasks/WP6b-packing-options.md`, `tasks/L-r2-datasheets.md`, `tasks/review-r2.md`, `tasks/WP7a-protocol.md`, `tasks/WP6-packing.md`, `tasks/WP3-renders.md`, `tasks/phase1-common.md`, `tasks/review-r1.md`, `tasks/review-code-template.md`, `tasks/WP9-record.md`, `tasks/WP5-contacts.md`
- verdicts: `tasks/reviews/code-r2.md`, `tasks/reviews/code-r1.md`

### Restore
Run from the coordinator pane after a server restart, or from the fresh coordinator pane that takes over:

```bash
python3 ~/.claude/skills/save-state/state.py restore --from /Users/rolfie/projects/elicio/HANDOFF.json
# the old coordinator conversation, if herdr did not resume it in the pane:
# cd /Users/rolfie/projects/elicio && claude --resume 61ba63c7-8fd8-497e-b665-c65cc34e72f6
```
