plain: Finish the earpiece shell v2f (WP14f) from the paused wip 938984e: wall-mounted charging pads, lid boss, measured checks passing, solids and renders committed

# Task

## Lead brief

# Finish the earpiece shell v2f (WP14f) from the paused wip

Elicio is Rolf's custom EEG earpiece (right ear, behind the ear, printed nylon shell, custom flex board). The design repo is this one. Rolf paused this package on 2026-09-18 because his Mac ran out of memory during CAD builds. You run on the Oracle box (Linux aarch64, 16 cores, 94 GB) so CAD has room. Rolf, today: "Go ahead. Do everything. Push and turn and get me the 3D design and photos of it." Your shell solids feed the 3D model and photo job that runs beside you.

## Start

1. `git fetch origin`. Merge, never rebase, in this order: `origin/lane/w1-r6` (938984e, the paused WIP of this package), `origin/lane/w3` (ab9ce95, WP11g packing pin table v3 with the Q98 channels; never merged to main), `origin/lane/w4` (dbeeafa, WP13d, one sentence each in receiver-v2.md and montage.md §8). Resolve conflicts yourself and list each one in your report.
2. Environment: create your own venv in your worktree with uv (`uv venv --python 3.13`, then `uv pip install -e '.[cad]'`; fall back to Python 3.12 if a CAD wheel is missing for aarch64). Missing system libraries (for example libgl1, libxrender1) may be installed with apt. If the CAD stack cannot run on this box at all, stop and report that with the exact error; do not work around it with another CAD library.
3. Read: `tasks/WP14f-shell-v2f.md` (the original brief; items 1 and 2 are done, item 3 is yours), `tasks/phase1-common.md` (rules only), `tasks/reviews/code-r7.md` (defects 1 to 3 and 10, Seams "Shell sections" and "Stamp vs HEAD"), `docs/fab/open-questions.md` Q89 to Q98, `tasks/WP11g-flat-pattern-v3.md`, `docs/fab/packing-v2.md` §5e after the merge, and HANDOFF.md "Traps" (the CAD items).

Ignore in those older files: lane names, worktree paths, `herdr agent start` lines, the `herdr agent prompt elicio` DONE/WAITING pushes and the closing steps of `tasks/phase1-common.md`. This brief's finish path replaces them. The rest of phase1-common's rules apply: stdlib unittest, no purchases or vendor contact, never edit `docs/fab/plan-v2.md`, `docs/fab/plan.md` or `docs/fab/open-questions.md`, no packing or board files.

## Where the paused WIP stopped (its report, summarised)

Done at 938984e: §5e reader (`S5eShell`) at ab9ce95; island bosses at H1 (13.23, 17.70) / H2 (17.95, 17.70), keep gap 1.42; P4/P5 as Ø2.7 holes through the posterior wall with the ring pad inside and a hex collar/well 3.0 into the bay, rotation 30°, clipped at floor and lid; skin-face Ø5 floor holes, rib slot and drop channel no longer cut; medial well (16.50, 41.00), M2.5×8; checks rewritten (`V2_CHARGE_pads` for the wall, `V2_TAB_envelope`, `V2_WALL_minima` seat probes, `V2_CAVITY_v3` added to `SHELL_CHECKS`, `V2_BOSS_sites` on §5e); tests, `shell_v2.toml` (Q98 token added, parser class not re-run after that), `render.py` posterior labels. Q89 lid boss and `V2_CLOSURE` pass were already on the branch (solids 825793e, views 89279c2).

One temp build then exited 3:
- `V2_CHARGE_pads` and `V2_WALL_minima`: `P4_wall_around` / `P5_wall_around` = -1.0 (the u-thickness probe found no boundary at the offset samples). Decide whether the probe or the geometry is wrong, by sectioning the built solid, and fix the one that is wrong.
- `V2_BOARD_envelope`: 0.0467 mm³ of nylon in the board zone from the wall standoffs.
- `V2_CAVITY_v3` passed but recorded `j2_p5_standoff_gap` -4.93 (the P5 well overlaps J2's courtyard). If the shell alone cannot clear it, name the clash with numbers under "Needs a decision"; do not edit the packing.

Not done: those fixes, `docs/fab/shell-v2.md` §2, §4, §5 and the before/after table, solids in `docs/fab/cad/v2/` (still the Q89 set), renders with the stamp equal to the solids commit and a view that shows the side-wall charging pads, all gates.

## Rules that bit earlier rounds

- Every check measures the built solid through one construction path. No constants, no cut-then-probe tautologies, no forked construction to keep hashes stable. Every wall or skin-face feature gets a face probe (air at the face). A joint is measured on both parts.
- Commit only the closing outputs. No per-run drawings or search dumps in git.
- Never `git stash` (the stash is shared across worktrees).
- Every commit message states the true state reached, including failure.
- Run one CAD build at a time.
- Throwaway helper panes, if you start any, run Claude Haiku: `--model claude-haiku-4-5-20251001`.

## Done means

The task's acceptance conditions, plus: the report lists the exact paths of the final shell solids (STEP and STL for body and lid) and the render files, and the commit they come from, because the photo job builds the assembled model from them.

## job-0001 — Finish the earpiece shell v2f (WP14f) from the paused wip 938984e: wall-mounted charging pads, lid boss, measured checks passing, solids and renders committed

Requests: request:q-1790170873805-83781

Acceptance conditions:
1. Branch contains lane/w1-r6 at 938984e, lane/w3 at ab9ce95 (WP11g) and lane/w4 at dbeeafa (WP13d), merged, never rebased
2. Shell build exits 0 with every check measured on the built solid, or exits 3 with each failing check named with its measured number and the geometry that causes it
3. docs/fab/cad/v2/ solids and renders regenerated from the final commit, manifest stamp equals the solids commit, two consecutive shell runs byte-identical, manifest.py --check-bytes passes
4. Full unittest suite green, order 1 files under docs/fab/cad/v1/ byte-identical, docs/fab/shell-v2.md sections 2, 4, 5 and the before/after table updated, git status clean

# Instructions in force

None.

# Facts in force

None.

# Repository, machine and pinned gates

- Repository: `/home/user/projects/elicio`.
- Machine: local.
- Gates: not configured for this repository.

# Finish

Commit the finished work, then run `hp done --report /home/user/projects/elicio/.worktrees/t-0001/.herdr-project/elicio-t-0001/report.md --sha <commit-sha>`.

# Paths

- Report: `/home/user/projects/elicio/.worktrees/t-0001/.herdr-project/elicio-t-0001/report.md`
- Library folder for files meant for Rolf: `/home/user/projects/elicio/.worktrees/t-0001/.herdr-project/elicio-t-0001/library`
