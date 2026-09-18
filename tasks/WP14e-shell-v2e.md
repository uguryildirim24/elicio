# WP14e — shell v2e: charging pads on the hook-end floor per §5d, rib slot and drop channel (lane w1)

Read `tasks/phase1-common.md`, your `.reports/WP14d-report.md`,
`docs/fab/open-questions.md` Q84 to Q86 and the Round 7 notes (main),
packing §5d on `lane/w3` at `408a476`
(`git show 408a476:docs/fab/packing-v2.md`, the §5d folded-site table
and its "shell extras"), and w3's report
`/Users/rolfie/projects/elicio/.worktrees/w3/.reports/WP11e-report.md`
(Addendum 2 and 3). Lane `w1`, worktree
`/Users/rolfie/projects/elicio/.worktrees/w1`, branch `lane/w1-r6` on top
of `ecfff54`; `git merge main` first. Start line (coordinator restarts
you by copy-paste):

    herdr agent start w1 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Why: §5c's charging pads were inside the 1.5 mm side walls (your WP14d
built them there and the domes protrude past the silhouette). The tail
cannot take two Ø5 pads once the end-wall slot, the REF dome, the
screw well and the tail loft are respected, so §5d puts P4/P5 on the
hook-end medial floor beside the cell (Q86), reached by a floor tab
from the leftover through a rib slot with a drop channel (Q85 flat
pattern). The shell follows the folded-site table and adds the channel.
Nothing is ordered.

Owns: as WP14d (`scripts/cad/` shell modules, `scripts/cad/params/shell_v2.toml`,
`tests/test_cad.py` shell classes, `docs/fab/shell-v2.md`,
`docs/fab/cad/v2/` outputs and renders). Not the packing, not the
board, not plan v2, not open-questions, not order 1.

Deliver:

1. **Pads.** P4 (14.70, 4.30) and P5 (17.70, 11.72), y 1.50 ring seat,
   the same flush RING_PAD construction as WP14d, Ø5 holes through the
   medial floor; the tail-corner pads removed. `V2_BOSS_sites` (or a
   sibling) parses §5d's folded-site table for P1–P5 at `408a476`, so
   no site is hard-coded; P1–P3 unchanged.
2. **Channel.** Rib slot s 14.90–15.70, u 11.90–20.50, height 0.31
   through the rib; the drop channel at the leftover's s 16.00 edge,
   u 11.90–20.50, for two 90° bends at R 1.5 dropping 3.31 (board
   underside 4.81 to the floor 1.50), a clearance the 0.31 flex passes
   through; wall minima kept and stated.
3. **Checks.** `V2_CHARGE_pads` re-measured at the new sites: flush pads;
   nylon between pads ≥ 3.0 edge-to-edge; clearance to the cell pocket
   (cell u 1.80–11.90, s 1.50–14.50) stated; floor thickness around
   the Ø5 holes ≥ the wall minimum; nylon under the 1.0 mm creepage zone
   (Q84). Every existing check re-run on the built solid (`V2_BOSS`,
   `V2_BOSS_sites`, `V2_BOSS_pilot`, `V2_TAB_envelope` including the new
   slot, `V2_CLOSURE`, `V2_LATERAL_unbroken`, `V2_EDGE_radii`,
   `V2_WALL_minima`); render stamp = manifest.commit = solids commit;
   both renders regenerated with the pads labelled "P4/P5 charging pads,
   hook end (Q86)"; `shell-v2.md` §2, §4, §5 updated; the report carries
   the before/after table as WP14d's did.

Gates: as WP14d (`LC_ALL=C LANG=C .venv/bin/python -m unittest discover
-s tests -v` exit 0, the shell class, order 1 byte-identical, two
consecutive shell runs identical, `manifest.py --check-bytes`,
`git status --short` empty). Commit in steps; the last commit message
describes the state reached (`shell(v2e): charging pads on the hook-end
floor per §5d, rib slot and drop channel` only if every gate passed).
Report `.reports/WP14e-report.md` (untracked). Closing steps per the
common file with `<PKG>` = `WP14e`, `<lane>` = `w1`, also when you fail.
