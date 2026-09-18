# WP12d — board v2d: no-receptacle BOM, width 22 outline, placed on two sides from §5c, routed to DRC 0 (lane w2)

Read `tasks/phase1-common.md`, your `.reports/WP12d-prep-report.md` and
`hardware/board/route.md` §6–§7, `docs/fab/board-v2.md`,
`docs/fab/open-questions.md` Q77 to Q83 and the Round 7 notes (main), the
round 6 verdict's "To WP12c" note in `tasks/reviews/code-r6.md`, packing
§5c on `lane/w3`
(`/home/user/projects/elicio/.worktrees/w3/docs/fab/packing-v2.md`,
at `e1f1d6f` now; a final sha follows, see step 3), and L8 §1–§3 on
`lane/w5` (`/home/user/projects/elicio/.worktrees/w5/docs/fab/L8-research-v5.md`).
Lane `w2`, worktree `/home/user/projects/elicio/.worktrees/w2`, branch
`lane/w2` on top of `edf612f`; `git merge main` first. Start line
(coordinator restarts you by copy-paste):

    herdr agent start w2 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Why: the layout grid closes only at width 22 on two sides; the USB-C
receptacle needs M1 ≥ 58.3 that Rolf has not measured, so the board the
build carries has no receptacle (Q81): 64 footprints plus two tail
charging pads, R1–R3 on the island (Q79), J4 TC2030 on the leftover
(Q80), the island holes at §5c's sites (Q82), neck-end tab strips (Q83).
The router is proven on OpenJDK 25. Nothing is ordered.

Owns: `hardware/board/*` (schematic, PCB, build and route scripts,
`route.md`, generated BOM/CPL/Gerbers), `tests/test_board_release.py`,
`docs/fab/board-v2.md`; `scripts/board/release.py` only if a test needs
it (say so in the report). Not the packing, not the shell, not plan v2,
not open-questions, not the firmware (`firmware/src/board_pins.h`: if a
GPIO changes, say so; lane w4 aligns it).

Deliver:

1. **Schematic.** J1 (USB-C) and U5 (USBLC6, D+/D−) out; two pads P4
   (VBUS_IN) and P5 (GND) on the tail as the RING_PAD footprint §5c uses;
   VBUS from P4 through the existing P-FET inhibit and charger path,
   unchanged otherwise; a TVS on the pad-fed VBUS (one Basic part if one
   exists, LCSC code tagged UNVERIFIED) unless the schematic already
   protects VBUS, say which; the nRF USB pins left as the datasheet says
   for unused USB; ERC 0; BOM regenerated with the count stated;
   `board-v2.md` §3, §4, §12 updated (two-sided assembly, the pads, the
   charging rule unchanged).
2. **Outline and regions from §5c width 22, chord 47.90.** Island u
   2.25–19.75, s 16.00–37.60; leftover per §5c; the three tabs as neck-end
   strips with §5c's lengths; the two Ø2.7 island holes at (13.45, 17.70)
   and (17.95, 17.70); J4's keep-out on the leftover; RF notch and module
   keep-out; copper-to-edge 0.30 everywhere.
3. **Place** from §5c's no-receptacle, width-22, two-sided pin table with
   the side column (your WP12d-prep parser), bottom parts flipped; R1–R3
   at the tab roots on the island; the zero-track DRC must show 0 errors
   apart from unconnected (paste it). The coordinator sends
   `§5c final <sha>` when w3's last nudge turn lands; if it has not
   arrived when you reach this step, push
   `herdr agent prompt coordinator "WAITING WP12d §5c final sha"` (with
   the pane token per the common file) and stop; on the prompt, re-pin
   from the final table (a script run) and continue. If the final table
   still has a part under 0.30 to the edge, nudge it inward by the
   smallest step and record each nudge in `route.md`.
4. **Route.** pcbnew DSN export; Freerouting 2.4.1 on
   `/opt/homebrew/opt/openjdk@25/bin/java` with the jar kept somewhere
   durable (`~/.local/opt/freerouting/` or a gitignored
   `hardware/board/tools/`; say where); passes bounded; import the SES;
   DRC; hand-fix the residue. Contact class 1.0 mm kept, one Contact trace
   per tab and nothing else on a tab, J3 pads Ø1.5. DRC 0 errors and 0
   unconnected; `release.py --routed` exit 0 with `routed: true`;
   Gerbers, BOM and CPL (= BOM) regenerated; `board-v2.md` §15 the route
   record; `route.md` §8 the run.
5. If DRC 0 cannot be reached, stop un-shorted with `routed: false`, the
   DRC list in `route.md` and the first structural reason, and say so in
   the report.

Gates: `.venv/bin/python -m unittest discover -s tests -v` green (the 14
CAD failures in your venv are your pins from rounds 5 and 6: fix the venv
with `pip install -e '.[cad]'` if you can, otherwise name them and show
the board tests green); ERC 0; the DRC pasted; `release.py` as above;
`git status --short` empty. Commit in steps; the last commit
`board(v2d): no-receptacle BOM, width 22, placed on two sides from §5c,
routed`. Report `.reports/WP12d-report.md` (untracked). Closing steps per
the common file with `<PKG>` = `WP12d`, `<lane>` = `w2`, also when you
fail.
