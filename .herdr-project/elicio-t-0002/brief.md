plain: Finish the earpiece circuit board v3 (WP12i) from the paused wip 3a27ffd: route every connection and produce the order files, or name each pad that cannot be routed

# Task

## Lead brief

# Finish the earpiece circuit board v3 (WP12i) from the paused wip

Elicio is Rolf's custom EEG earpiece (right ear, behind the ear, printed nylon shell, custom flex board that JLC will assemble). Rolf paused this package on 2026-09-18 because his Mac ran out of memory. It resumes on the Mac because KiCad is installed here; the heavy shell CAD now runs on the Oracle box instead. Rolf, today: "Go ahead. Do everything. Push and turn and get me the 3D design and photos of it."

## Start

1. `git fetch origin`. Merge, never rebase: `origin/lane/w2` (3a27ffd, the paused WIP of this package), then `origin/lane/w3` (ab9ce95, WP11g packing pin table v3 with the Q98 channels; the WIP vendored its §5e but never merged it). Resolve conflicts yourself and list each one in your report.
2. Environment: your own venv in your worktree (`uv venv --python 3.13`, `uv pip install -e .`; add `.[cad]` only if you need the CAD tests to run). KiCad's Python and `kicad-cli` are on this Mac.
3. Read: `tasks/WP12i-board-v3.md` (the original brief; item 1 and most of item 3 are done), `tasks/phase1-common.md` (rules only), `tasks/reviews/code-r7.md` (board attack points; decisions 94, 95, 97), `docs/fab/open-questions.md` Q89 to Q98, `docs/fab/board-v2.md` §12 and §13, `hardware/board/route.md` §12, `docs/fab/L8-research-v5.md` (JLC flex rules, Freerouting on Java 25), and HANDOFF.md "Traps".

Ignore in those older files: lane names, worktree paths, `herdr agent start` lines, the `herdr agent prompt elicio` DONE/WAITING pushes and the closing steps of `tasks/phase1-common.md`. This brief's finish path replaces them. The rest of phase1-common's rules apply: stdlib unittest, no purchases, uploads or vendor contact, never edit `docs/fab/plan-v2.md`, `docs/fab/plan.md` or `docs/fab/open-questions.md`, no packing or shell files. You own `hardware/board/*`, `scripts/board/*`, `tests/test_board_release.py`, `docs/fab/board-v2.md`.

## Where the paused WIP stopped (its report, summarised)

Done: U2 land checked at 0.40 mm pitch (`elicio:Texas_RSM0032`), U3 stays DSBGA-6, R9/R10 DNP, nine Q94 stiffener drawings (fee UNVERIFIED), Q97 tests, §5e vendored into `hardware/board/packing_v2_flat.md` (66 rows), re-pin on v3 (H1 13.23/17.70, H2 17.95/17.70, J4 16.52/24.60 rot 90, J2 15.15/11.35, J3 28.41/26.80, P4 23.32/4.35, P5 23.32/12.35, U2 on B.Cu under SW1), flat outline with the charge tab and the J3 break-off neck (cut u=22.25 on Dwgs.User and F.Fab), Q98 rule areas, zero-track DRC 0 / 144 unconnected; Contact strips locked at DRC 0 / 143 unconnected in commit 0da86a0.

Failed or not done: island SIG2 → R2 and REF → R3 by hand A* (R2.1 at (19.070, 33.340) and R3.1 at (19.070, 31.340) on one u beside U4 pad 5 at u 17.13–18.45, s 34.65; island east edge 19.75, Contact centre ≤ 19.375 for 0.30 copper-to-edge); the J3 PTH pads (28.41, 26.80 / 29.34 / 31.88); the `hand_route.py` vbus/j4/u2 loop was interrupted and left extra VBUS and nRESET segments in the committed PCB with no DRC run after; Freerouting not run; nothing released.

First step: DRC the committed PCB. If the interrupted copper is not clean, go back to the 0da86a0 board (`git show 0da86a0:<path>`) rather than repairing it. The old worktree `/home/user/projects/elicio/.worktrees/w2` also holds an untracked `hardware/board/elicio-v2.good.kicad_pcb`; read it only if git's copy is missing something, do not edit that worktree. Then Freerouting (OpenJDK 25) for the remainder with the locked routes locked, hand-fix residue, and release.

## Memory on this Mac

Rolf's Mac ran out of memory the last time this ran. Cap Freerouting's Java heap (for example `-Xmx4g`), run one router or KiCad batch at a time, and close anything you started when it finishes.

## Rules that bit earlier rounds

- Never `git stash`.
- Every commit message states the true state reached; never write "routed" unless `release.py --routed` passed.
- Flex boards are drawn flat: pin flat coordinates, never folded shell sites.
- A pin or channel that cannot be routed is named with its two pads and millimetres; do not move packing sites yourself. Propose a packing change under "Needs a decision" if one would close it.
- Throwaway helper panes, if you start any, run Claude Haiku: `--model claude-haiku-4-5-20251001`.

## Done means

The task's acceptance conditions, plus: the report lists the path of the board STEP export (with which component models are missing from it) and the commit it comes from, because the photo job puts the board inside the assembled model.

## job-0002 — Finish the earpiece circuit board v3 (WP12i) from the paused wip 3a27ffd: route every connection and produce the order files, or name each pad that cannot be routed

Requests: request:q-1790170873805-83781

Acceptance conditions:
1. Branch contains lane/w2 at 3a27ffd and lane/w3 at ab9ce95, merged, never rebased
2. The interrupted VBUS and nRESET copper is either DRC-clean or removed before any new routing
3. Either DRC 0 errors, 0 unconnected, 0 shorts and release.py --routed exit 0 with routed: true plus Gerbers, BOM and CPL; or routed: false with every remaining connection named with its two pads and millimetre geometry
4. Board tests green, ERC 0, DRC output pasted in the report, board-v2.md section 15 and route.md section 13 describe the run, git status clean

# Instructions in force

None.

# Facts in force

None.

# Repository, machine and pinned gates

- Repository: `/home/user/projects/elicio`.
- Machine: local.
- Gates: not configured for this repository.

# Finish

Commit the finished work, then run `hp done --report /home/user/projects/elicio/.worktrees/t-0002/.herdr-project/elicio-t-0002/report.md --sha <commit-sha>`.

# Paths

- Report: `/home/user/projects/elicio/.worktrees/t-0002/.herdr-project/elicio-t-0002/report.md`
- Library folder for files meant for Rolf: `/home/user/projects/elicio/.worktrees/t-0002/.herdr-project/elicio-t-0002/library`
