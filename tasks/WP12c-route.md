# WP12c — Route the flex board to DRC 0 (lane w2, runs alongside the round 6 review)

Read `tasks/phase1-common.md`, then your own `tasks/WP12b-board-route.md`
and `.reports/WP12b-report.md`, `docs/fab/board-v2.md` §15 and §19,
`docs/fab/packing-v2.md` §5. Lane `w2`, worktree
`/Users/rolfie/projects/elicio/.worktrees/w2`, branch `lane/w2`,
continuing from `480e355`. The round 6 reviewer merges `lane/w2` **at
`480e355` only**; everything you commit after it lands in round 7. Start
line (coordinator restarts you by copy-paste):

    herdr agent start w2 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Why: WP12b placed the board from the packing and synced every net, but
routing did not converge: Freerouting hung, and the bus fallback wrote
copper that shorts nets (1290 DRC errors, 31 unconnected). Order release
is fail-closed on that (Q62) and S0 cannot start without a routed board.
Nothing is ordered, quoted or uploaded.

Owns, and nothing else (the reviewer is editing the rest of the board
package at the same time; touching these files elsewhere costs a round
of conflicts): `hardware/board/elicio-v2.kicad_pcb` (copper, vias, zones
only; do not move footprints, the placement test pins them),
`hardware/board/maze_route.py`, `hardware/board/build_v2b.py`, a new
`hardware/board/route.md` (how the route was made, so it can be redone),
and `docs/fab/board-v2.md` **§15 only**. Not the schematic, not the
project file's rules, not `release.py`, not the tests except a routed
assertion added to `tests/test_board_release.py` at the very end.

Deliver:

1. Remove the shorting fallback copper first; commit that alone
   (`board(v2c): drop the shorting bus fallback`), so the branch never
   again carries copper that fails on purpose.
2. Diagnose the Freerouting hang before writing another router: run the
   Freerouting CLI headless with an explicit Java (`java -version` in the
   report), `--max_passes`, a wall-clock timeout, and the DSN exported by
   `kicad-cli pcb export specctra` (KiCad 10); log its output to
   `route.md`. If it routes, import the SES, run DRC, fix the residue by
   hand-placed segments in the file. If it does not route in an hour of
   wall clock, say so with the log and fall back to your own router,
   improved to respect the netclass clearances and the ring keep-outs,
   then hand-fix the residue the same way.
3. Reach `release.py --routed` exit 0: DRC 0 errors, 0 unconnected,
   `routed: true`, 2-layer flex rules of `elicio-v2.kicad_pro` unchanged.
   Contact nets isolated as WP12b defined; nothing new under the RF
   keep-out; USB pairs short and matched within the rule you cite.
4. `board-v2.md` §15 rewritten for the routed state: layer use, via
   count, the longest analog trace, what was hand-fixed, and the DRC
   report summary.

Gates: `.venv/bin/python -m unittest tests.test_board_release -v` green
including the routed assertion; `release.py --routed` exit 0 with the
numbers in the report; `git diff 480e355 -- hardware/board/elicio-v2.kicad_sch
hardware/board/elicio-v2.kicad_pro scripts/ docs/fab/board-v2.md` shows
only §15 in the doc and nothing in the others; `git status --short`
empty. Commit in steps; the last commit is `board(v2c): routed to DRC 0`.
If DRC 0 is not reached after your fallback, stop with the board
un-shorted and un-routed, `routed: false`, and say exactly what blocks in
the report. Report `.reports/WP12c-report.md` (untracked). Closing steps
per the common file with `<PKG>` = `WP12c`, `<lane>` = `w2`.
