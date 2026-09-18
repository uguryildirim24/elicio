# WP12d-prep — prove the router writes a file; placement reads a side column (lane w2)

Read `tasks/phase1-common.md`, your `.reports/WP12c-report.md` and
`hardware/board/route.md`, `docs/fab/open-questions.md` Q77, Q79, Q80 and
the Round 7 section (main), and L8 §3 at
`/Users/rolfie/projects/elicio/.worktrees/w5/docs/fab/L8-research-v5.md`
(on `lane/w5`, not yet on main; read it there). Lane `w2`, worktree
`/Users/rolfie/projects/elicio/.worktrees/w2`, branch `lane/w2` on top of
`f4376ca`; `git merge main` first (main has the round 6 merge with the
reviewer's board fixes; keep both sides, regenerate nothing by hand).
Start line (coordinator restarts you by copy-paste):

    herdr agent start w2 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Why: WP12c stopped because Freerouting 2.1.0 headless never wrote a SES
on this Mac. The research lane reports that 2.4.1 does, with
`--gui.enabled=false -de <dsn> -do <ses> -mp <passes> -mt <threads>`, and
that JLC assembles both sides of the flex. The real placement waits for
packing §5c (WP11d on w3); before it lands, prove the toolchain and make
the placement script ready for a two-sided table. No copper is committed.

Owns: `hardware/board/build_v2b.py` (or its successor), the routing
scripts, `hardware/board/route.md`, `tests/test_board_release.py`,
`docs/fab/board-v2.md` §15 only. Not the schematic, not the placement
(the board stays at the WP12c state), not `scripts/board/release.py`'s
refusal, not plan v2, not open-questions.

Deliver:

1. **Freerouting 2.4.1 headless on this Mac.** Install the release jar
   (free; Java 21 is present; say where it lives; Q46 lets Rolf veto).
   Export a DSN of the current `elicio-v2.kicad_pcb` with `kicad-cli`, run
   the headless command from L8 §3 with a bounded pass count, and record
   in `route.md`: version, exact command, wall time, whether a SES
   appeared, its size and track count, stderr. The SES is evidence only:
   do not import it (the placement is being redone). If 2.4.1 also writes
   nothing, say so with the log and try the next free option from L8 §3
   that runs offline; ProtoFlow and DeepPCB (cloud, account) are out.
2. **Two-sided placement input.** `build_v2b.py` accepts a `side` column
   (`top`/`bottom`) in the placement table it pins from packing §5 and
   places bottom-side footprints flipped to B.Cu with the rotation
   convention KiCad uses; a unit test with a synthetic two-row table
   proves it without touching the committed board. Read the §5b table
   format on `lane/w3` (`/Users/rolfie/projects/elicio/.worktrees/w3/docs/fab/packing-v2.md`)
   so §5c's columns match; do not depend on §5c existing yet.
3. **Q79 and Q80 ready.** In `route.md`, the plan for WP12d in ten lines:
   R1–R3 on the island at the tab roots, one Contact trace per tab, J1
   USB-C on the hook-end face, J4 TC2030 on the leftover with its keep-out
   as a board no-part zone, the Contact class 1.0 mm kept, J3 pads Ø1.5.

Gates: `.venv/bin/python -m unittest discover -s tests -v` green; the
committed board unchanged byte-for-byte except nothing (verify with `git
diff --stat` on `hardware/board/*.kicad_pcb` = empty); `release.py`
without `--routed` still exit 0; `git status --short` empty. Commit
`board(v2d-prep): Freerouting 2.4.1 headless proof; placement reads a side
column`. Report `.reports/WP12d-prep-report.md` (untracked) with the
route.md block pasted. Closing steps per the common file with `<PKG>` =
`WP12d-prep`, `<lane>` = `w2`, also when you fail.
