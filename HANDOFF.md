# Elicio handoff — 2026-09-17 05:10 local

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
(Q1–Q23).

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
  2. Q20 packing: only option C closes on the real lug (body 3 mm wider,
     pads moved, one wire crossing on the floor). My reading: C. He answers
     with the one line in `docs/fab/packing-options.md`; WP8 starts on it.
  3. Q6 nut metal (WP5b's table in `docs/fab/contacts.md` §8.2 has a
     plan-conforming zinc-plated steel row, brass, titanium), Q7 screw SKU,
     Q21 reference lug in the tail pocket, Q23 fold-and-solder for the 28 AWG
     lead: all before order 2, none before order 1.
  4. Q17 reference site: answered by wearing the gauge. Q18 cell: buy one
     501015 cell with the Stage A parts. Q19: accept the frozen protocol
     numbers or edit before Stage A data.
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
| r3 | WP5b lug, nut and dome drawings in `docs/fab/contacts.md` §8 | MERGE-AFTER-DECISION (9 fixes) | `1170b2a` | `tasks/reviews/code-r3.md` |
| r3 | WP6b packing options; only C closes; sheet `docs/fab/packing-options.md` | MERGE-AFTER-DECISION (9 fixes) | `1170b2a` | `tasks/reviews/code-r3.md` |
| r3 | decisions Q20–Q23 | coordinator | `7caff1c` | `docs/fab/open-questions.md` |

Round 3 gates at merge: 98 tests OK none skipped; option drawings,
solids and renders byte-identical. Round 2 gates at merge: 83 tests OK none skipped; fifteen solids
byte-identical twice and equal to the committed files; renders, drawing
and placement drawing byte-identical; manifest validator passes and fails
on a removed key.

## In flight

No lane is working. All five lanes are idle at `main`, fast-forwarded,
their reports read and merged:

- **w1** (cursor `cursor-grok-4.6-xhigh`, `lane/w1`): last package WP6b
  (four passes; the coordinator's own wording error on the lug datum cost
  one). Next candidate: interface v3 after Rolf picks Q20.
- **w2** (cursor, `lane/w2`): last package WP3. Holds the CAD context; next
  candidate WP8 (Stage B shell, order 2 files) once Q20 is answered.
- **w4** (cursor, `lane/w4`): last package WP4. Next candidate: sheet
  updates when interface v3 changes the order 2 numbers.
- **w5** (agy `gemini-3.8-flash-high`, `lane/w5`): last package WP5b. Next
  candidate: WP7a part 2 when the Stage A parts exist; WP5 purchase-time
  checks before S1.
- **w9** (cursor, `lane/w9`): last package WP9. Next candidate: design
  record update bundled with WP8.

The build now waits on Rolf more than on lanes. What each of his answers
starts: "I pick C" (or an alternative) → `tasks/WP8-shell-v2.md` (expected) on w2 from
plan §9 row WP8, §3.3, Q18, Q20, Q21, Q22, plus interface v3 on w1, one
round, one fresh reviewer. Renders approved and M1 measured → order 1 is
his under `docs/fab/order1.md`; nothing for a lane. Stage A parts bought →
WP7a part 2 on w5 from `docs/fab/montage.md` §2.

## Open

Plan open items live in `plan.md` §10 and `docs/fab/open-questions.md`
Q1–Q23 (Rolf's: Q6, Q7, Q12, Q17, Q18, Q19, Q20, Q21, Q23). Outside those:

1. WP7a part 2 (bench montage, three coordinates) — open because Stage A
   parts are unbought; Rolf's purchase.
2. WP8 Stage B shell (order 2 files) — open because it takes Rolf's
   packing pick (Q20), the cell answer (Q18) and WP7a's coordinates.
3. Order 1 itself — open because it needs Rolf's render approval and his M1.
   The vault (`~/Documents/obsidian/rolfiersbox`, page
   `Wiki/projects/Elicio.md`) has rounds 1 to 3 and his questions in its
   Open questions form as of 2026-09-17.
4. `docs/fab/L2-vendors.md` says no bureau prints conductive TPU, later
   found wrong — open because nobody has corrected the lane report; low
   priority, the plan does not use conductive TPU.
5. Design record open questions 3 and 4 still say "until WP6" — open
   because the update belongs with WP8's record change; bundle it there.

## Next

- Idle until Rolf's first answer arrives; the In flight table says which
  package each answer starts (Q20 → WP8 and interface v3, one round).

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
- A coordinator note sent to a Cursor lane mid-package lands in its
  follow-up queue and runs as a new turn after the lane's DONE → expect a
  second DONE; do not open the review on the first one.
- Quote drawing numbers with their datum. "6.27 from the ring edge" became
  "6.27 from the Ø7.1 edge" in a coordinator prompt and cost WP6b a pass;
  the drawing's number is 8.85 from the contact centre (8.788 max).
- A lane's "every number has a source" can be false (WP7a citations, WP5b
  dead URLs and page claims) → the reviewer checks quotes verbatim, with a
  read-only agy lane for live pages if needed.
- `sed -i ''` fails on non-ASCII patterns → edit with python.
- A relative screenshot path lands in the repo root → absolute scratchpad paths.
- Do not `cd` into worktrees from the coordinator shell → `git -C` with the
  worktree path.
- `herdr agent read` output is plain text, not JSON → do not pipe it to a
  JSON parser.

<!-- Everything below this line is generated. Regenerate it at every
checkpoint with:  python3 ~/.claude/skills/save-state/state.py snapshot
Do not hand-edit ids into it. -->

## Herdr (generated 2026-09-17T03:33:49-04:00 by state.py, herdr 0.9.0, session `default`)
Workspace `w1B` (elicio), 6 tabs. Coordinator: pane `w1B:p1` in tab `w1B:t1`, agent name `elicio`, kind claude, status working, cwd `/Users/rolfie/projects/elicio`.
Coordinator session id `61ba63c7-8fd8-497e-b665-c65cc34e72f6`; transcript `/Users/rolfie/.claude/projects/-Users-rolfie-projects-elicio/61ba63c7-8fd8-497e-b665-c65cc34e72f6.jsonl`.

### Workers nested under the coordinator
| name | kind | status | pane | tab (label) | cwd | tokens | last title |
|---|---|---|---|---|---|---|---|
| w1 | cursor | done | `w1B:pA` | `w1B:tA` (w1) | `/Users/rolfie/projects/elicio/.worktrees/w1` | done=1 lane=WP6b | Lane W1 Instructions |
| w2 | cursor | done | `w1B:pB` | `w1B:tB` (w2) | `/Users/rolfie/projects/elicio/.worktrees/w2` | done=1 lane=WP3 | Lane W2 Instructions |
| w4 | cursor | done | `w1B:pC` | `w1B:tC` (w4) | `/Users/rolfie/projects/elicio/.worktrees/w4` | done=1 lane=WP4 | Lane W4 Instructions |
| w5 | agy | done | `w1B:pD` | `w1B:tD` (w5) | `/Users/rolfie/projects/elicio/.worktrees/w5` | done=1 lane=WP5b |  |
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
| `/Users/rolfie/projects/elicio` | `main` | 7caff1c | 0 | Round 3: record the reviewer's decisions 20 to 23 as open questions Q20 to Q23 |
| `/Users/rolfie/projects/elicio/.worktrees/w1` | `lane/w1` | 7caff1c | 0 | Round 3: record the reviewer's decisions 20 to 23 as open questions Q20 to Q23 |
| `/Users/rolfie/projects/elicio/.worktrees/w2` | `lane/w2` | 7caff1c | 0 | Round 3: record the reviewer's decisions 20 to 23 as open questions Q20 to Q23 |
| `/Users/rolfie/projects/elicio/.worktrees/w4` | `lane/w4` | 7caff1c | 0 | Round 3: record the reviewer's decisions 20 to 23 as open questions Q20 to Q23 |
| `/Users/rolfie/projects/elicio/.worktrees/w5` | `lane/w5` | 7caff1c | 0 | Round 3: record the reviewer's decisions 20 to 23 as open questions Q20 to Q23 |
| `/Users/rolfie/projects/elicio/.worktrees/w9` | `lane/w9` | 7caff1c | 0 | Round 3: record the reviewer's decisions 20 to 23 as open questions Q20 to Q23 |

Last commits on the integration branch:

```
7caff1c Round 3: record the reviewer's decisions 20 to 23 as open questions Q20 to Q23
1170b2a review(r3): verdict MERGE-AFTER-DECISION, gates, defects 1–18, decisions 20–23
8392a20 review(WP6b): cite C-31428 D4 as 8.788 max; 8.85 stays as the conservative barrel end
e87ca6d review(WP5b): working URLs for TME, Titanium Webshop, Fastenright, Westfield, Nichifu; 31428 is 8.788 max; mark unsourced passivation, certificate, RJX dk/k and Panduit numbers
635535a review(WP5b): plain-text math; stack at wall +0.3 and DIN 934 Kapton top; budget against plan §7 lines; six Ti nuts; drop unsourced claims; reference tab vs TE 31428
7c973fe review(WP6b): say which 0402 counts are placed; give E's lateral height and its source
```

### Record files (newest first)
- handoff: `HANDOFF.md`
- briefs: `tasks/L-r3-sources.md`, `tasks/review-r3.md`, `tasks/WP5b-drawings.md`, `tasks/WP6b-packing-options.md`, `tasks/L-r2-datasheets.md`, `tasks/review-r2.md`, `tasks/WP7a-protocol.md`, `tasks/WP6-packing.md`, `tasks/WP3-renders.md`, `tasks/phase1-common.md`, `tasks/review-r1.md`, `tasks/review-code-template.md`
- verdicts: `tasks/reviews/code-r3.md`, `tasks/reviews/code-r2.md`, `tasks/reviews/code-r1.md`

### Restore
Run from the coordinator pane after a server restart, or from the fresh coordinator pane that takes over:

```bash
python3 ~/.claude/skills/save-state/state.py restore --from /Users/rolfie/projects/elicio/HANDOFF.json
# the old coordinator conversation, if herdr did not resume it in the pane:
# cd /Users/rolfie/projects/elicio && claude --resume 61ba63c7-8fd8-497e-b665-c65cc34e72f6
```
