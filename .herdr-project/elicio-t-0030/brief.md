plain: Build the shell for the v4 board: an 18 by 8.1 millimetre body with the board's shell changes and measured fit checks

# Task

## Lead brief

# Build the Elicio shell for the v4 board (18 × 8.1 mm body)

Elicio is Rolf's custom behind-the-ear EEG earpiece, printed in PA12 MJF. He liked the design but said the body was "too thick ... horizontally" (22 × 9.0 mm). The v4 flex board is now routed and passes its release (branch `origin/hp/elicio/t-0019-close-the-last-open-connections-on-the-v`, 6f653a1, in review as round r18). It makes an **18 × 8.1 mm** body possible at the same length. The shell hasn't been rebuilt for it yet. That is your job.

## Start here

1. Merge these into your branch with `--no-edit`, and don't rebase:
   - `origin/hp/elicio/t-0021-review-r9-the-shell-shape-gets-its-charg`: the reviewed r9 shell v2f, the base shell;
   - `origin/hp/elicio/t-0019-close-the-last-open-connections-on-the-v`: the routed v4 board and design note.
2. Read:
   - `docs/fab/board-v4-design.md` §4 (floor plan, cavity tests), §7 (the shell changes, with numbers), §10.1/§10.2 (flat and folded tables: every courtyard, ring, strip root and tab root in the shell frame);
   - `docs/fab/shell-v2.md`;
   - `scripts/cad/params/shell_v2.toml` and the CAD scripts in `scripts/cad/`;
   - HANDOFF.md "Traps".

## The work

Make a v4 shell as a new parameter set and solids beside v2f, for example `shell_v4.toml` and `docs/fab/cad/v4/`. Keep everything of r9 that §7 says to keep: the SIG fold pockets, REF slot, hinge, hook and outer ear-fit loft.
1. **Width and height.** Cavity u 1.5–16.5 (W18). LID_Y 7.1, T 8.1. Same length.
2. **Rib slot for the P4/P5 flap.** Remove u 16.00–16.50 × s 14.90–15.70 × y 1.50–4.50.
3. **P4/P5 keying walls.** Remove r9's wall sockets. Key each standoff with two floor-standing walls: u 13.19–16.19, s = site ± 2.80 outward, 1.0 thick, y 1.50–4.30. Use the P5 site at s 12.10.
4. **Lid posts.**
   - Ø2.0 at (5.90, 23.00), 1.98 long;
   - Ø2.0 at (9.40, 32.10), 0.98 long, onto U1.
5. **Closure.** At W18 the M2.5×8 head well no longer fits beside the REF pocket (§7). Keep the screw closure if you can: move the well past the pocket into the tail loft (centre s ≥ 50.25), move the tongue slot as needed, and prove wall thickness ≥ 1.0 and thread engagement with numbers.
   - Plan-v2 R2 allows one 1.5 mm hex key, no glue.
   - If the screw truly cannot fit, don't build a latch. Stop that item and report the numbers, and the coordinator will ask Rolf.
6. **Measured checks on the built solid.** Rerun the WP14 checks, with the cavity test against every row of the v4 §10.2 table: courtyards, hangs, tab roots, the cell, J2 against the P5 well (≥ 0.3), and the lid posts landing on their pads. Report the minimum margin per row. Fix `V2_CAVITY_v3`'s weakness: it checks pin centres, not courtyards. The v4 check must use courtyard boxes.
7. **Solids, manifest and renders.** Export STEP/STL/3MF with a manifest of hashes, like v2, plus two PNG views of the shell and one of the folded board inside it if the tools allow.
8. **Docs.** Write `docs/fab/shell-v4.md`: what changed from v2f, every check with its number, and what's UNVERIFIED.

## Rules

- **Files you may edit:** shell CAD, shell params, shell docs and tests only. Don't change `hardware/board/*`, the board design note, `docs/fab/plan-v2.md` or `docs/fab/open-questions.md`. If the board must change for the shell, list it in the report.
- **Contact geometry is fixed.** Keep the contact sites P1–P3, the ring and landing geometry, and the Q84/Q88/Q97 clearances exactly as the board design note states.
- **Memory.** This Mac ran out of memory once on this project. Run one CAD build at a time, and close what you start.
- **No spending or vendor contact.** No purchase, upload, quote, account or vendor contact.
- **Git.**
  - Never `git stash`.
  - Pass `--no-edit` to merges and `-m` to commits.
  - Commit in steps with true messages.

## Done means

The task's acceptance conditions. The report opens with one short paragraph Rolf can read on his phone:
- the body size;
- whether the board fits with every check passing;
- how the lid closes;
- anything he has to decide.

## job-0011 — Build the shell for the v4 board: an 18 by 8.1 millimetre body with the board's shell changes and measured fit checks

Requests: request:q-1790177634256-92066, request:q-1790170873805-83781

Acceptance conditions:
1. A v4 shell parameter set and solids exist beside v2f, with the cavity at u 1.5 to 16.5, LID_Y 7.1, the rib slot, the P4 and P5 keying walls and both lid posts from board-v4-design section 7
2. Measured checks on the built solid pass for every row of the v4 folded table using courtyard boxes, with each margin reported and J2 at least 0.3 mm clear of the P5 well
3. The closure is a working screw with wall and thread numbers, or the report states with numbers why it cannot fit, and docs/fab/shell-v4.md, the manifest and renders are committed

# Instructions in force

<!-- n-0003 · 2026-09-25 · request:adeherdr/q-1790295901101-67630 -->
Rolf, 2026-09-24: keep working until this project's goal is reached. When a lane or task is blocked, or nothing is running, pick the next useful step toward the goal and start it; ask Rolf only what truly needs him, without stopping other work. Implementation lanes run on gpt-6-sol high and reviewer lanes on gpt-6-sol xhigh; routing picks this, so start lanes without a recipe override.

# Facts in force

## n-0002

<!-- n-0002 · 2026-09-23 · request:q-1790177634256-92066 -->
Rolf, 2026-09-23: he likes the design but the body is too big horizontally (22 mm wide, 9.0 thick), and part changes are the way he expects to make it smaller; a smaller body is the main goal of the board redesign.

# Repository, machine and pinned gates

- Repository: `/home/user/projects/elicio`.
- Machine: local.
- Gates: not configured for this repository.

# Finish

Commit the finished work, then run `ha done --report /home/user/projects/elicio/.worktrees/t-0030/.herdr-project/elicio-t-0030/report.md --sha <commit-sha>`.

# Paths

- Report: `/home/user/projects/elicio/.worktrees/t-0030/.herdr-project/elicio-t-0030/report.md`
- Library folder for files meant for Rolf: `/home/user/projects/elicio/.worktrees/t-0030/.herdr-project/elicio-t-0030/library`
