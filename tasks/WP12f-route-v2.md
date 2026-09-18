# WP12f — route pin table v2 to DRC 0: R24 off the real J4 hole, rules in the DSN, Contact nets pre-routed (lane w2)

Read `tasks/phase1-common.md`, your `.reports/WP12e-report.md` and
`hardware/board/route.md` §9, `docs/fab/board-v2.md` §12 (the JLC flex
limits) and §15, `docs/fab/open-questions.md` Q84 to Q87 and the Round 7
notes (main). Lane `w2`, worktree `/home/user/projects/elicio/.worktrees/w2`,
branch `lane/w2` on top of `30ca79d`; `git merge main` first. Start line
(coordinator restarts you by copy-paste):

    herdr agent start w2 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Why: WP12e placed the flat pattern with 2 zero-track DRC errors (R24 on
the real J4 hole: the pin table's J4 hole sites are mirrored against the
KiCad footprint at rot 90; w3 fixes the table in WP11f) and the router
run produced 317 errors of its own (199 track_width, 103 clearance, 9
copper_edge, 3 hole, 2 npth_inside_courtyard) with 49 % fanout and 75
unrouted, which says the router did not get the board's rules, not that
the board cannot be routed. Nothing is ordered.

Owns: as WP12e. Not the packing, not the shell, not plan v2, not
open-questions, not the firmware.

Deliver:

1. **R24 (Q87).** Move R24 off J4's real NPTH by the minimum that
   clears hole clearance 0.20 and keeps the 0402 rules (courtyards, pad
   to outline ≥ 0.30, second-side rules); the 0.1 mm pin does not bind
   here. Any other B.Cu part the real hole centres (16.25, 27.14),
   (15.234, 22.06), (17.266, 22.06) touch: same. Record every move in
   `route.md` §10 as a deviation from v2 for the packing to fold back.
   Zero-track DRC 0 errors (paste it).
2. **Rules the router can see.** Set the board's netclasses explicitly
   to the JLC 2-layer flex limits in board-v2 §12 (track, clearance, via
   drill and annulus; state the numbers) so the DRC minima and the
   class values agree; export the DSN and show that its `class` blocks
   carry those widths and clearances (grep the DSN, paste the lines).
   The 199 track_width errors came from a width below the DRC minimum;
   find which value the router used and close the gap.
3. **Contact and charge nets by hand.** Script in pcbnew: one trace per
   strip for SIG1, SIG2, REF from the ring pad along the strip's centre
   to R1–R3's pad on the island, and CHARGE_VBUS / CHARGE_GND from
   P4/P5 along the charge tab to their first part; widths per §12;
   locked, so the DSN carries them as fixed and Freerouting leaves them
   alone. The Q84 rule areas hold for them; nothing else may enter the
   strips (a track-and-via keep-out over each strip for every other net,
   or a check after routing that no other net's copper is inside a
   strip).
4. **Route.** Freerouting 2.4.1 on OpenJDK 25 with the jar you have;
   fanout must climb well past 49 % before autorouting is worth reading
   (if it does not, say which pins cannot escape and why: via size,
   pad pitch, clearance). Import the SES into a copy, DRC, then into the
   owned PCB only when it improves on the zero-track state; hand-fix
   residue by script; DRC 0 errors and 0 unconnected; `release.py
   --routed` exit 0 with `routed: true`; Gerbers, BOM, CPL; board-v2 §15
   and route.md §10 the run, with the exact Freerouting flags and the
   DSN check in a script under `scripts/board/` so the run repeats.
5. If DRC 0 is not reached: stop un-shorted, `routed: false`, the DRC
   list by type and the first structural reason, and a last commit
   message that says what is true.

Gates: as WP12e (board tests green, ERC 0, the DRC pasted, `release.py`
as above, `git status --short` empty). Commit in steps; the last commit
describes the state reached. Report `.reports/WP12f-report.md`
(untracked). Closing steps per the common file with `<PKG>` = `WP12f`,
`<lane>` = `w2`, also when you fail.
