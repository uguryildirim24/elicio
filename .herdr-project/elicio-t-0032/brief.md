plain: Design and measure lid closure options for the 18 millimetre v4 shell so Rolf can choose one

# Task

## Lead brief

# Find a lid closure for the 18 mm Elicio shell

Elicio is Rolf's custom behind-the-ear EEG earpiece, printed in PA12 MJF. The v4 shell (branch `origin/hp/elicio/t-0030-build-the-shell-for-the-v4-board-an-18-b`, c3b7fd3) makes the body 18 × 8.1 mm at the same 48.4 mm arc, and all 97 fit checks pass. The lid has only a hinge and nothing holding it shut:
- The M2.5×8 screw head well needs u 19.25 beside the REF pocket (u 4.75–12.25), and the body is 18 wide.
- Past the pocket it would need s ≥ 50.25, and the body ends at s 48.40.

Rolf chooses the closure. Your job is to give him two to four real options, each built and measured, so he can pick with numbers.

## Start here

1. Merge `origin/hp/elicio/t-0030-build-the-shell-for-the-v4-board-an-18-b` into your branch with `--no-edit`.
2. Read:
   - `docs/fab/shell-v4.md` (the closure arithmetic);
   - `docs/fab/board-v4-design.md` §7 and §10.2;
   - `scripts/cad/build_shell_v4.py` and `scripts/cad/params/shell_v4.toml`;
   - plan-v2 R2: "one 1.5 mm hex key, no soldering, glue, crimping or wire stripping".

## Options to build and measure (each as a variant; don't overwrite the base v4 shell)

1. **A smaller screw that still uses the 1.5 mm hex key.** ISO 4762 / DIN 912 M1.6 and M2 socket heads, or ISO 7380 M2: give each one's head diameter, head height and key size from a standards or vendor page with URL and date. Place the well beside the REF pocket or elsewhere on the lid, and give its walls, the thread engagement into printed PA12 (or into a titanium or brass insert only if R2 allows fitting it), and the pull-out margin with the source of the numbers.
2. **The screw somewhere else**, for example near the hook or front end, or through the lid into a boss clear of the board. The §10.2 courtyards and the Contact geometry are fixed.
3. **A PA12 snap latch with the existing hinge.** It needs no tool, so it's within R2. Give the cantilever length, deflection and strain against PA12 MJF's elongation from a public datasheet (HP or JLC3DP), the retention force, and how Rolf opens it without a tool (a slot for the hex key used as a pry is fine).
4. **For reference only:** the length the body would need to keep the M2.5 screw (s end and M1 needed). Don't build it.

For each option, give:
- what changes on the body and lid;
- the minimum wall;
- every §10.2 check still passing on the solid, rerun;
- the retention number and its source;
- the parts to buy, with price, URL and date, or UNVERIFIED;
- one render.

Close with a comparison table and your recommendation.

## Rules

- **Files you may edit:** shell CAD, params, docs and tests only. No board changes.
- **Memory.** One CAD build at a time.
- **No spending or vendor contact.** No purchase, upload, quote, account or vendor contact.
- **Git.**
  - Never `git stash`.
  - Pass `--no-edit` to merges and `-m` to commits.
  - Commit in steps with true messages.

## Done means

The task's acceptance conditions. The report opens with one short paragraph Rolf can read on his phone: the options, in one line each, and which you'd pick.

## job-0012 — Design and measure lid closure options for the 18 millimetre v4 shell so Rolf can choose one

Requests: request:q-1790177634256-92066, request:q-1790170873805-83781

Acceptance conditions:
1. Two to four closure variants are built as shell variants, each with its changes, minimum wall, retention number with source, and every v4 folded-table check rerun on the solid
2. Each variant lists the parts to buy with price, URL and date or UNVERIFIED, and keeps plan rule R2 (one 1.5 mm hex key, no glue or crimping)
3. docs/fab/shell-v4.md has a comparison table, one render per variant, and a recommendation

# Instructions in force

<!-- n-0003 · 2026-09-25 · request:adeherdr/q-1790295901101-67630 -->
Rolf, 2026-09-24: keep working until this project's goal is reached. When a lane or task is blocked, or nothing is running, pick the next useful step toward the goal and start it; ask Rolf only what truly needs him, without stopping other work. Implementation lanes run on gpt-6-sol high and reviewer lanes on gpt-6-sol xhigh; routing picks this, so start lanes without a recipe override.

# Facts in force

## n-0004

<!-- n-0004 · 2026-09-25 · request:adeherdr/q-1790295901101-67630 -->
The adeherdr coordinator turned nudge on in PROJECT.md (2026-09-25 ~08:20Z) for Rolf's request that every coordinator churn: when this coordinator is idle with no lane working, the ticker asks it for the next step about every 20 minutes. Automated prompts will wait while Rolf has text typed in this pane once adeherdr W117 lands.

## n-0002

<!-- n-0002 · 2026-09-23 · request:q-1790177634256-92066 -->
Rolf, 2026-09-23: he likes the design but the body is too big horizontally (22 mm wide, 9.0 thick), and part changes are the way he expects to make it smaller; a smaller body is the main goal of the board redesign.

# Repository, machine and pinned gates

- Repository: `/home/user/projects/elicio`.
- Machine: local.
- Gates: not configured for this repository.

# Finish

Commit the finished work, then run `ha done --report /home/user/projects/elicio/.worktrees/t-0032/.herdr-project/elicio-t-0032/report.md --sha <commit-sha>`.

# Paths

- Report: `/home/user/projects/elicio/.worktrees/t-0032/.herdr-project/elicio-t-0032/report.md`
- Library folder for files meant for Rolf: `/home/user/projects/elicio/.worktrees/t-0032/.herdr-project/elicio-t-0032/library`
