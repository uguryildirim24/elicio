# WP12g — Contact creepage at the exposed lands only (Q88), full Contact routes locked, route to DRC 0 (lane w2)

Read `tasks/phase1-common.md`, your `.reports/WP12f-report.md` and
`hardware/board/route.md` §10, `docs/fab/board-v2.md` §12 (the 7 × 7
other-net keep-out around each ring land) and §15,
`docs/fab/open-questions.md` Q84, Q87, Q88 and the Round 7 notes
(main), and pin table v2.1 on `lane/w3` at `e4b857c`
(`git show e4b857c:docs/fab/packing-v2.md` §5d) for R23, R24, R26. Lane
`w2`, worktree `/home/user/projects/elicio/.worktrees/w2`, branch
`lane/w2` on top of `fbd56e6`; `git merge main` first. Start line
(coordinator restarts you by copy-paste):

    herdr agent start w2 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Why: WP12f proved the router path (DSN classes verified, fanout 54.8 %,
444 tracks on the copy) and stopped only on Q84's `tabs` area at the
strip roots. Q88 reads plan v2 §5.3's 1.0 mm as creepage for EXPOSED
copper: the ring lands and the charging lands plus 1.0 mm (board-v2
§12's 7 × 7 keep-out), not the coverlaid strip trace. The strips carry
one Contact trace at the Contact class clearance and nothing else.
Review r7 runs in parallel and merges `lane/w2` at `fbd56e6`; you work
on top of it, never rebase, and take main's merge later. Nothing is
ordered.

Owns: as WP12f (`hardware/board/*`, `scripts/board/route_v2.py`,
`tests/test_board_release.py`, `docs/fab/board-v2.md`). Not the packing,
not the shell, not plan v2, not open-questions, not the firmware.

Deliver:

1. **Rule areas per Q88.** `tabs` becomes three areas, one per ring land,
   each the Ø5 land plus 1.0 mm (the 7 × 7 of §12) with 1.0 mm clearance
   to any other net; `tail_pads` becomes the two charging lands plus
   1.0 mm; the strips keep the Contact class (0.15/0.20) and the
   foreign-net keep-outs; the island as Q84. Board-v2 §12's table says
   so; the test asserts no Contact-clearance violation at the roots and
   that foreign copper inside a strip fails.
2. **R24 (Q87).** Take pin table v2.1's (18.49, 22.57) rot 90 if it meets
   every board rule on copper (the deviation then closes); otherwise
   keep +0.47 u and say why in `route.md` §11. R23 and R26 per v2.1
   within 0.1 mm.
3. **Contact routes locked.** By script: ring land → strip centre →
   island → R1–R3's Contact pad, one trace each, no via on a strip or
   in a bend window; VBUS and GND from P4/P5 along the charge tab to
   their first parts; DRC 0 with only the locked copper before the
   router runs (paste it).
4. **Route.** Freerouting 2.4.1 on OpenJDK 25 through `route_v2.py`;
   raise fanout and autoroute passes and the job timeout as needed
   (state them); the via at §12's flex minimum if 0.70/0.30 blocks
   escapes; import the SES into the owned PCB once it improves on the
   locked-only state; hand-fix residue by script until DRC 0 errors and
   0 unconnected; `release.py --routed` exit 0 with `routed: true`;
   Gerbers, BOM, CPL; board-v2 §15 and `route.md` §11 the run.
5. If DRC 0 with 0 unconnected is not reached: stop un-shorted,
   `routed: false`, the DRC list by type, the unconnected count and the
   first structural reason, and a last commit message that says what
   is true.

Gates: as WP12f (board tests green, ERC 0, the DRC pasted, `release.py`
as above, `git status --short` empty). Commit in steps; the last commit
describes the state reached. Report `.reports/WP12g-report.md`
(untracked). Closing steps per the common file with `<PKG>` = `WP12g`,
`<lane>` = `w2`, also when you fail.
