# WP6 round 3 — packing decision sheet under the short-tab reading (lane w1)

Read `tasks/phase1-common.md` first, then `docs/fab/open-questions.md`
(Q13 to Q16 are yours to build on). Lane `w1`, worktree
`/Users/rolfie/projects/elicio/.worktrees/w1`, branch `lane/w1`,
fast-forwarded to `main` (round 2 merged at `443a178`; read
`tasks/reviews/code-r2.md` defects 21 to 31 and decisions 13 to 15 for
what the reviewer changed in your `interface.md` and `placement.py`, and
why packing is now "not confirmed"). Start line (coordinator restarts you
by copy-paste):

    herdr agent start w1 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Spec sections: plan §5, §6 (three separately protected paths), §3.3
(BOARD_ZONE, LEAD_PADS, keep-outs, WIRE_CHANNEL), §10 interface decision 1
and Open for Rolf item 6. Interface v2 §3.1 (tabs), §4 (pads, route), §6
(board on the curved floor), §8.2 (options), §12. `scripts/cad/placement.py`
with its `layout_conflicts()` and budget readings (literal tab, short tab,
no tabs).

Owns: `docs/fab/packing-options.md` (new: the decision sheet for Rolf),
`scripts/cad/placement.py` (an `--option` switch), new drawings
`docs/fab/cad/v1/placement_A.svg`, `placement_B.svg`, `placement_C.svg`,
`placement_E.svg`, `tests/test_placement.py`, and one errata row plus a §12
pointer in `docs/fab/interface.md` (version stays 2; the version bumps
after Rolf picks).

Deliver:

1. **Option A, as is, under Q13.** The signal lug tab ends under its own
   pad: width 3, length from the Ø7.1 edge to the far edge of its pad,
   plus the 0.5 margin. Recompute the free mask, place VQFN-32 (4.60
   courtyard), two BAV199S-Q (line map SIG1+SIG2, REF+spare), charger,
   LDO and the 0402s, each array within 10 mm of its pads, with
   `layout_conflicts()` empty. If it closes, say so, with the numbers. If
   not, say what is short by how much.
2. **Options B, C, E.** B: BODY_ARC +3.5 mm. C: BODY_WIDTH +3 mm. E:
   passives and, if the height allows, the arrays on the lateral face
   beside the module (board top to lid underside, minus the foam strip
   over the superior 3 mm, minus the module's own footprint; plan §5's
   lateral row gives the heights). For each option: the drawing, free
   against required area, new pad positions and tab directions, conflicts
   list (must be empty or explained), what shell parameters change and by
   how much, the effect on TOTAL_CHORD and the M1 gate (B moves them, C
   does not, E does not), what Rolf gives up (length behind the ear, width
   in the crease, a two-sided assembly). Every number has a From cell.
3. **The sheet** `docs/fab/packing-options.md`: one table, one row per
   option, then one recommendation with reasons, then exactly what Rolf
   answers (one line). Write it so he can pick from his phone.
4. `placement.py --option A|B|C|E --out <file>`; A is the default and
   regenerates the committed `placement.svg` byte-identical. Tests: the
   four drawings regenerate identical; the conflict checker is run for
   every option in the tests; the Q13 tab geometry has its own test.
5. The interface: an errata row in the change log (version stays 2) and a
   §12 line saying the packing decision waits on `packing-options.md`;
   nothing else in it changes. The pads in §4 stay as frozen until Rolf
   picks; the sheet carries the candidate pads per option.

Do not change CAD solids or `manifest.json` (a shell change is WP8's, after
Rolf picks). Do not edit `plan.md`, `open-questions.md`, `contacts.md`,
`montage.md`. Web only for package drawings and datasheets, page and date
per number; the round 2 datasheet facts in `code-r2.md` (RSM 4.10 max,
BAV199S-Q two pairs, Spec K) may be reused with their citations.

Acceptance: option A closes under Q13, or the sheet gives Rolf B, C and E
with complete numbers and a recommendation. Gates: unit tests green; all
drawings regenerate byte-identical; every new number has a From cell.

Report: `.reports/WP6b-report.md`. Closing steps per the common file with
`<PKG>` = `WP6b`, `<lane>` = `w1`.
