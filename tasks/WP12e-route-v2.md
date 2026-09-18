# WP12e — Contact rule by area, flat-pattern re-pin, route to DRC 0 (lane w2)

Read `tasks/phase1-common.md`, your `.reports/WP12d-report.md` and
`hardware/board/route.md` §8, `docs/fab/open-questions.md` Q79, Q84, Q85
and the Round 7 notes (main), and `tasks/WP11e-flat-pattern.md` (what
lane w3 is producing for you). Lane `w2`, worktree
`/home/user/projects/elicio/.worktrees/w2`, branch `lane/w2` on top of
`1e055de`; `git merge main` first. Start line (coordinator restarts you
by copy-paste):

    herdr agent start w2 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Why: three structural reasons stopped WP12d. Two are the packing's and
come back as pin table v2 in flat coordinates with J4's holes kept clear
on both sides (WP11e). The third is the board's: the Contact netclass
1.0 mm was meant for the exposed tab and ring copper (creepage on the
skin side), not for the 0402 that joins SIG2 to the front end on the
island; Q84 reads it as a rule area. Nothing is ordered.

Owns: as WP12d (`hardware/board/*`, `tests/test_board_release.py`,
`docs/fab/board-v2.md`; `scripts/board/release.py` only if a test needs
it, say so). Not the packing, not the shell, not plan v2, not
open-questions, not the firmware.

Deliver:

1. **Q84 now, before WP11e lands.** A custom DRC rules file for the board
   with rule areas `tabs` (the three strips and their ring pads) and
   `tail_pads` (P4, P5) where Contact-to-anything clearance is 1.0 mm; on
   the island the Contact nets take the board default clearance (state
   it; ≥ 0.20 for JLC flex). R1–R3's pads then pass. A test runs DRC on
   the zero-track board and asserts no Contact-clearance violation on the
   island. `board-v2.md` §12 states the rule and why.
2. **Parser for v2.** Read pin table v2 (flat coordinates plus side; the
   folded-site table is the shell's, ignore it) and J4's both-side
   keep-out as a rule area with no B.Cu footprint allowed.
3. **WAITING.** When 1 and 2 are committed and the coordinator has not
   sent the line "pin table v2" plus a sha, push
   `herdr agent prompt coordinator "WAITING WP12e pin table v2"` (with the
   pane token per the common file) and stop.
4. **On the prompt:** re-pin from v2 (flat coordinates), rebuild the
   outline as the flat pattern (strips and ring pads part of the
   outline), zero-track DRC 0 apart from unconnected (paste it); then
   route: pcbnew DSN, Freerouting 2.4.1 on
   `/opt/homebrew/opt/openjdk@25/bin/java` with the jar at
   `~/.local/opt/freerouting/`, import the SES, DRC, hand-fix residue;
   Contact rule areas respected, one Contact trace per tab, J3 pads Ø1.5;
   DRC 0 errors and 0 unconnected; `release.py --routed` exit 0 with
   `routed: true`; Gerbers, BOM, CPL regenerated; `board-v2.md` §15 and
   `route.md` §9 the run.
5. If DRC 0 is not reached: stop un-shorted with `routed: false`, the DRC
   list and the first structural reason in `route.md`, and a last commit
   message that says what is true (for example `board(v2e): placed on the
   flat pattern, not routed`). Never a message that claims a state the
   tree does not have.

Gates: as WP12d (`.venv/bin/python -m unittest discover -s tests -v`
green, or the 14 CAD pins named and the board tests green; ERC 0; the DRC
pasted; `release.py` as above; `git status --short` empty). Commit in
steps; the last commit describes the state reached. Report
`.reports/WP12e-report.md` (untracked). Closing steps per the common file
with `<PKG>` = `WP12e`, `<lane>` = `w2`, also when you fail.
