# WP12h — finish the 63 rats by hand on the WP12g copper, or name each one with its geometry (lane w2)

Read `tasks/phase1-common.md`, your `.reports/WP12g-report.md` and
`hardware/board/route.md` §11, `docs/fab/board-v2.md` §12 (JLC 2-layer
flex minima: trace, space, via drill and annulus; quote the page line
for the smallest via the process allows) and §15, and
`docs/fab/open-questions.md` Q84, Q87, Q88 and the Round 8 notes (main).
Lane `w2`, worktree `/home/user/projects/elicio/.worktrees/w2`, branch
`lane/w2` on top of `8348e62`; `git merge main` first, never rebase
(review r7 is merging `lane/w2` at `fbd56e6`; your later commits go to
round 8's review). Start line (coordinator restarts you by copy-paste):

    herdr agent start w2 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Why: WP12g left the owned PCB at 421 tracks, 33 vias, DRC 0 errors, 0
shorts and 63 unconnected with Q88 in force and Q87 closed. Nothing
structural stops the rest: they are U2's QFN escapes, J4's SWD lines,
VBUS from P4 onto the island, J3's Contact pads and layer stitches. An
autorouter that gives up at 20 passes is not a reason to move parts; a
routed pad, or a pad whose geometry cannot be routed, is. Nothing is
ordered.

Owns: as WP12g. Not the packing, not the shell, not plan v2, not
open-questions, not the firmware.

Deliver:

1. **Keep the copper you have.** Start from `8348e62`'s PCB: the locked
   Contact routes, the 421 tracks and 33 vias stay unless a specific
   trace must move to make room; say which and why.
2. **Hand-route by script, rat by rat**, in this order, each step a
   commit with the DRC and the unconnected count in its message: VBUS
   P4 → island (one trace along the charge tab and the leftover, width
   per §12 for the charge current); J4 SWD (SWDIO, SWCLK, RESET, VTref,
   GND to U1's pins); J3's Contact pads (Contact class 0.20 on the
   island, locked when done; no other net inside the Q88 lands); U2's
   QFN escapes (radial on F.Cu, vias at the smallest §12 via if
   0.55/0.30 does not fit, never a via in a pad or a bend window; the
   pads the ADS1292R leaves unused are not routed and are named); the
   remaining stitches. Your maze or manhattan router from the earlier
   rounds may do the legwork; the DRC is the judge.
3. **Then Freerouting** (OpenJDK 25, `route_v2.py`) only if rats remain,
   with the hand routes locked; import when it improves; hand-fix
   residue.
4. **Finish**: DRC 0 errors and 0 unconnected, 0 shorts, no foreign net
   in a strip or a Q88 land, `release.py --routed` exit 0 with
   `routed: true`, Gerbers, BOM, CPL, board-v2 §15 and `route.md` §12
   the run.
5. If a rat cannot be closed: name the pad, the net and the geometric
   reason (which two coppers leave less than trace + 2 × clearance,
   with the numbers), so the packing can move a part on facts; stop
   un-shorted, `routed: false`, the count and the list, and a last
   commit message that says what is true.

Gates: as WP12g (board tests green, ERC 0, the DRC pasted, `release.py`
as above, `git status --short` empty). Commit in steps; the last commit
describes the state reached. Report `.reports/WP12h-report.md`
(untracked). Closing steps per the common file with `<PKG>` = `WP12h`,
`<lane>` = `w2`, also when you fail.
