# WP12i — board v3: footprints checked, stiffeners (Q94), R9/R10 DNP (Q95), the envelope (Q97), then re-pin on pin table v3 and route (lane w2)

Read `tasks/phase1-common.md`, your `.reports/WP12h-report.md` and
`hardware/board/route.md` §12, the verdict `tasks/reviews/code-r7.md`
(board attack points; decisions 94, 95, 97; the "Routing is not yours"
seam no longer applies, the review is merged), `docs/fab/open-questions.md`
Q89 to Q98 with the Round 8 notes, `docs/fab/board-v2.md` §12 and §13,
and `tasks/WP11g-flat-pattern-v3.md` plus the Q98 channels (what lane w3
is producing for you). Lane `w2`, worktree
`/Users/rolfie/projects/elicio/.worktrees/w2`, branch `lane/w2` on top of
`c9c750d`; `git merge main` first, never rebase. Start line (coordinator
restarts you by copy-paste):

    herdr agent start w2 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Why: WP12h showed the island cannot be closed at JLC's flex rules until
the packing opens channels (Q98), and the review left the board three
items of its own. The packing's pin table v3 (J2 inside, the charging
pads in the far side wall, R9/R10 out, the break-off tab, the channels)
is coming; the board does its own part first. Nothing is ordered.

Owns: `hardware/board/*`, `scripts/board/*`, `tests/test_board_release.py`,
`docs/fab/board-v2.md`. Not the packing, not the shell, not plan v2, not
open-questions, not the firmware.

Deliver:

1. **Now, before v3 lands.**
   (a) Footprints against datasheets: U2 against the ADS1292R RSM
   (VQFN-32: pitch, pad, thermal pad, the datasheet's land pattern) and
   U3 against its own; fix a wrong footprint and say what changed. If
   U3's inner ball cannot be escaped under 0.10/0.10 with 0.55/0.30 vias
   even with a free channel, name the same-family regulator in a larger
   package (SOT-23-5 or similar, LCSC number, price UNVERIFIED) and make
   the swap in schematic, BOM and footprint, stating it as a BOM change.
   (b) Q95: R9/R10 DNP (schematic marked, out of the BOM, the CPL and
   the PCB).
   (c) Q94: stiffener zones redrawn so no piece covers lands on its own
   side, PI 0.1 where FR4 cannot sit, the ring pieces drawn, the count
   and JLC's fee stated in §12.
   (d) Q97 as tests: one Contact net per strip on one layer with a
   through-thickness foreign-net keep-out; no other net's via or pour
   inside a land's 7 × 7 zone on either layer; on the island R1–R3's
   pads are the only exposed Contact copper.
   (e) Vendoring: the parser reads §5e (pin table v3, 66 rows, the
   channel rows or keep-out list) and replaces `packing_v2_flat.md` with
   the v3 table when it lands.
   Commit these.
2. **WAITING.** Unless the coordinator has sent the line "pin table v3"
   plus a sha, push `herdr agent prompt coordinator "WAITING WP12i pin
   table v3"` with the pane token per the common file and stop.
3. **On the prompt:** re-pin on v3 (J2 inside the cavity; P4/P5's wall
   sites are the shell's, the board pins the flat charge tab and its
   pads), rebuild the flat outline (the v3 charge tab, the J3 break-off
   tab with its cut line on a fabrication layer), the Q98 channels as
   keep-outs the tests check, zero-track DRC 0; lock the Contact routes
   (ring → strip → R1–R3, shortest, one layer, GND under them where Q97
   allows); `hand_route.py`, then Freerouting on OpenJDK 25 for the
   remainder with the hand routes locked, hand-fix residue; DRC 0
   errors and 0 unconnected, 0 shorts; `release.py --routed` exit 0
   with `routed: true`; Gerbers, BOM, CPL; board-v2 §15 and `route.md`
   §13 the run. If rats remain: name each pad with its geometry as
   WP12h did, stop un-shorted, `routed: false`, a truthful last commit
   message.

Gates: board tests green, ERC 0, the DRC pasted, `release.py` as above,
`git status --short` empty; the CAD tests skip by name on your venv
since the review (install `.[cad]` if you want them to run). Commit in
steps; every commit message describes the state reached. Report
`.reports/WP12i-report.md` (untracked). Closing steps per the common
file with `<PKG>` = `WP12i`, `<lane>` = `w2`, also when you fail.
