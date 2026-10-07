plain: Close the last open connections on the new board, starting from the Fable session's second placement.

# Task

## Lead brief

# Close the last open connections on the Elicio v4 board (Opus 5.5 max)

Elicio is Rolf's custom EEG earpiece. The v4 flex board makes the body 18 × 8.1 mm. Two sessions got it this far:
- Opus 5.5 (t-0012) designed it.
- Fable 5.1 max (t-0014) finished all but the last step.

The board has no shorts, 0 DRC errors under the project rules, 0 starved thermals, the J3 cut-edge fix and the ISP1807 VSS vias. **Ten connections are still open**: 5 GND and 5 signal. Your job is to close them without changing the body, the layer count or the 0.10/0.10 rules.

Rolf asked for this model by name: "give it to opus 5.5 max let it rip again". You are the third session on this board. The Fable session before you (t-0016) stopped twice on the 64000-token reply limit and lost hours. Your limit is raised to 128000, but keep replies to one finding or one action anyway, and commit WIP after every placement pass.

## Where t-0016 left off

- Its branch is `hp/elicio/t-0016-finish-the-v4-earpiece-board-from-the-op`, tip `209564f`, pushed. Merge it into your branch. It holds t-0014, and its WIP commit changes only the pass-2 placement in `hardware/board/build_v4.py`. The PCB has not been rebuilt from that placement.
- Router run 2 on the pass-2 placement left **7 conflict knots, all north of s 25**. Earlier knots in the west stack cleared.
- What it found: AFE_EN_HW runs R15.2/Q3.1 → Q2.3, not to U1. CHG_MON runs U1.44 → R25.2. The two cross on B west of the stack. That is a real topological crossing, so a placement move fixes it and more routing won't. The B corridor between the west stack and U2's parts is 0.49 mm pad-to-pad.
- Its scratch tools and renders are in `/private/tmp/claude-501/-Users-rolfie-projects-elicio--worktrees-t-0016/4fcf54ea-16ef-42a4-8951-c3df26c1bae6/scratchpad`: `plot_board.py` (knot renders of F and B), `dump_geom.py`, `geom.txt`, `rects.py`, `nets.py` and `conf_sum.py` (conflict summary). Copy what helps into your own scratch or the repo. Don't rely on that folder staying.

## Start here

1. Your branch starts from main, which already has t-0014's draft and the r13 reviewer's tool fixes. Merge `hp/elicio/t-0016-finish-the-v4-earpiece-board-from-the-op` (209564f) into it. Do not rebase.
2. Read t-0014's report. The sealed copy is at `/home/user/.herdr-ade/elicio/.state/artifacts/b7164a883b5780f3708101668b1395de05febc3c6811ced8d062b1338ca48fc4`.
3. Then read these parts of `docs/fab/board-v4-design.md`:
   - §9, above all §9.4: every open connection with its pads, the copper in the way and the gap;
   - §9.2: the placement reliefs so far and why relief 4 was reversed;
   - §9.3: the thermal stubs.
4. Read HANDOFF.md "Traps".

## The work

Do t-0014's recommended steps 1 and 2 together, before any rule or layer change:

1. **Placement at the knots.** The six spots every router variant ended on are structural (t-0014's "Lessons"):
   - SOT-883 crossings in the west stack;
   - U1's east pads sharing one via column;
   - the four SPI lines on F walling off U1's south-east.

   Moves t-0014 proposed:
   - R18, R20, R21 and R19 one row further east, so U1's east pads get a second via column;
   - Q1 turned so AFE_VIN's pin faces U4;
   - C11 out from under U2.

   You may choose other moves inside the island if the numbers say so. Keep every part on the island. Keep the contact rings, the strip and tab roots, and the P4/P5 sites where they are.
2. **Locked pre-routes** for the two common blockers:
   - +3V0 from U4.1 over C8.1 to U2's supply pads on B, east of the corridor;
   - AFE_EN_HW from Q3.1 to a via just outside LAND_P1, then on F across the P1 landing to U1.

   Check the second one against Q97: no foreign via or copper inside a land's 7 × 7 zone.
3. **Fresh route with GND live.** Route GND together with the signals, as t-0014's regional split did. Don't pour after. Use `v4_route_pf.py`, `hardware/board/v4_finish.sh` and the stitch and thermal-stub tools.
4. **Release.** Aim for DRC 0 errors, 0 unconnected, 0 shorts after a refill, then `scripts/board/release.py --board elicio-v4 --routed` exit 0 with `routed: true`. The outputs are Gerbers, drill, BOM, CPL and STEP. Then:
   - Regenerate the §10.1 and §10.2 tables for the final placement, with a cavity margin for every courtyard, hang and tab root.
   - Confirm that J2 still clears the P5 standoff well by ≥ 0.3 mm.
   - Confirm that the folded body is still 18 × 8.1 mm.

## Limits

- **Stop points.** The body stays 18 × 8.1 at the same length. Two copper layers. The 0.10/0.10 track and clearance floor everywhere. If closing needs a narrower rule or a third layer, stop and report. That choice goes to Rolf.
- **Budget.** At most six full route-and-finish runs; one is about 40 minutes. If the count of open connections stops falling across two runs, stop. Report the best state, with every open connection named with its two pads and the gap in millimetres.
- **Parts.** Don't change parts, values or the J3 and VSS fixes.
- **Shell.** No shell CAD edits.

## Rules

- **Contact safety is not negotiable:**
  - 220 kΩ per electrode path (R1–R3; R31–R33 on the J3 tab);
  - R7/G2;
  - the Q84 rule areas;
  - Q88 creepage;
  - Q97: one Contact net per strip, no foreign via or pour inside a land's 7 × 7 zone, and R1–R3's pads are the only exposed Contact copper;
  - charge copper only where skin cannot reach.
- **pcbnew crash rules.** Crashes put dialogs on Rolf's screen.
  - `board.Add` every new item before `Flip`.
  - Never let Python free board-held items.
  - Revert by reloading the file.
  - End pcbnew scripts with `os._exit(0)`.
  - Run a script once cleanly before looping it.
  - Never retry a crashing call in a loop.
- **Scratch copies.** `build_v4.py` overwrites the PCB, so route in scratch copies. A DRC on a copy needs `<stem>.kicad_pro` and `<stem>.kicad_dru` beside it. `release.py` doesn't refill zones.
- **Memory.** Run one router or KiCad batch at a time. Cap Freerouting at `-Xmx4g` if you use it. Close what you start.
- **No spending or vendor contact.** No purchase, quote request, upload, account or vendor contact.
- **Git.**
  - Never `git stash`.
  - Commit in steps; every commit message states the true state.
  - Never write "routed" unless the routed release passed.
- **Protected files.** Don't edit `docs/fab/plan-v2.md` or `docs/fab/open-questions.md`.
- **Helper panes.** Throwaway helper panes, if you start any, run Claude Haiku: `--model claude-haiku-4-5-20251001`.

## Done means

The task's acceptance conditions. The report opens with one short paragraph Rolf can read on his phone:
- whether the board is ready to order;
- the body size;
- what, if anything, he still has to decide.

List the release outputs with their paths, and the final DRC lines verbatim.

## job-0008 — Close the last open connections on the v4 earpiece board on Opus 5.5 max, from the Fable session's second placement, and pass the routed release

Requests: request:q-1790287727542-37692, request:q-1790202028699-83571, request:q-1790177529449-90206

Acceptance conditions:
1. hardware/board/elicio-v4.kicad_pcb has KiCad DRC 0 errors, 0 unconnected and 0 shorts after a zone refill, with the body still 18 by 8.1 mm on two copper layers at the 0.10/0.10 floor
2. scripts/board/release.py --board elicio-v4 --routed exits 0 with routed: true and writes Gerbers, BOM, CPL and a STEP export
3. docs/fab/board-v4-design.md §9 and §10 match the final board, including the folded shell table with a cavity test for every courtyard, hang and tab root, and the board tests pass

# Instructions in force

None.

# Facts in force

## n-0002

<!-- n-0002 · 2026-09-23 · request:q-1790177634256-92066 -->
Rolf, 2026-09-23: he likes the design but the body is too big horizontally (22 mm wide, 9.0 thick), and part changes are the way he expects to make it smaller; a smaller body is the main goal of the board redesign.

# Repository, machine and pinned gates

- Repository: `/home/user/projects/elicio`.
- Machine: local.
- Gates: not configured for this repository.

# Finish

Commit the finished work, then run `hp done --report /home/user/projects/elicio/.worktrees/t-0019/.herdr-project/elicio-t-0019/report.md --sha <commit-sha>`.

# Paths

- Report: `/home/user/projects/elicio/.worktrees/t-0019/.herdr-project/elicio-t-0019/report.md`
- Library folder for files meant for Rolf: `/home/user/projects/elicio/.worktrees/t-0019/.herdr-project/elicio-t-0019/library`
