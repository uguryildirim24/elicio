# WP11e — the flat pattern: tab pads in PCB coordinates, J4 keep-out on both sides, pin table v2 (lane w3)

Read `tasks/phase1-common.md`, your `.reports/WP11d-report.md`,
`docs/fab/open-questions.md` Q83 to Q85 and the Round 7 notes (main),
WP12d's report and its route log on `lane/w2`
(`/Users/rolfie/projects/elicio/.worktrees/w2/.reports/WP12d-report.md`,
`/Users/rolfie/projects/elicio/.worktrees/w2/hardware/board/route.md` §8:
the three structural reasons), and `docs/fab/board-v2.md` §11–§12. Lane
`w3`, worktree `/Users/rolfie/projects/elicio/.worktrees/w3`, branch
`lane/w3` on top of `c6bd2fe`; `git merge main` first. Start line
(coordinator restarts you by copy-paste):

    herdr agent start w3 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Why: WP12d pinned the §5c table literally and the SIG2 ring pad P2 at
(10.40, 33.10) sits inside U1's courtyard. The table gives the tabs'
FOLDED (shell) sites, but a flex board is drawn flat: the strips and
their ring pads need flat coordinates that leave the island's neck end
and reach nothing else in the flat pattern. And J4's NPTH holes go
through both sides, so its footprint is a keep-out on B.Cu too. Two of
the three structural reasons are the table's; the third (Contact class
against 0402 pads) is the board lane's (Q84). Nothing is ordered.

Owns: `scripts/cad/layout_v2c.py`, `scripts/cad/placement_v2.py`,
`scripts/cad/placement.py` flags, `tests/test_placement.py`,
`docs/fab/packing-v2.md` (regenerated, never hand-edited; §5c gains the
v2 tables or a §5d), drawings under `docs/fab/cad/v2c/` (replace, four at
most in total, Q56). Not the board, not the shell, not plan v2, not
open-questions.

Deliver:

1. **Flat pattern** for the build's cell (no receptacle, width 22, chord
   47.90, two sides): the board outline unfolded: island, neck, leftover,
   and the three strips as they leave the board (SIG1 and SIG2 from the
   island's neck end per Q83, REF per §5 through the end-wall slot), each
   strip's flat rectangle (flat length = folded run plus the fold
   allowance: state the arc at R 1.5 for the 0.31 stack and the
   flat-to-folded mapping), the ring pads P1–P3 at the strip ends in flat
   coordinates, P4/P5 in their flat positions on the tail. Prove the flat
   pattern does not self-overlap and no strip crosses a part on either
   side of the leftover or the pocket region (a 2D check). If the neck end
   cannot host both strips beside J4, SW1 and the leftover parts, say so
   with numbers and give the next exit (strips leaving the island's high-s
   end and folding under the tail; the side-edge pockets of Q74 were
   refused by the 0.65 wall).
2. **Pin table v2**: every PCB footprint in FLAT coordinates with its
   side; the folded shell sites for P1–P5 in a separate small table (u, s,
   y) for the shell lane; H1/H2; J4's two NPTH holes as a both-side
   keep-out (hole diameter plus the board's hole clearance, read from the
   KiCad file) with no B.Cu part inside; every rule re-checked: courtyards
   on both sides, pad-to-outline ≥ 0.30, Contact variant A, hole keep
   3.30, second-side height ≤ 3.31, no second-side part over a standoff,
   ring seat, boss, tab root or J4 hole.
3. **Tests**: flat pattern non-overlap; P1–P3 flat centres outside every
   courtyard; the J4 hole zone empty on B.Cu; the folded-site table equal
   to §5's contact sites and the P4/P5 sites.

Gates: `.venv/bin/python -m unittest discover -s tests -v` green;
`packing-v2.md` byte-identical on a second run; drawings ≤ 4; order 1
untouched; `git status --short` empty. Commit in steps; the last is
`packing(v2e): flat pattern, tab pads in PCB coordinates, J4 keep-out
both sides, pin table v2`. Report `.reports/WP11e-report.md` (untracked)
with the flat-pattern drawing path and the v2 table's row count. Closing
steps per the common file with `<PKG>` = `WP11e`, `<lane>` = `w3`, also
when you fail.
