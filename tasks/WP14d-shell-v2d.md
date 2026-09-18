# WP14d — shell v2d on packing §5c: width 22, bosses at the hole sites, neck-end strips, two tail charging contacts (lane w1)

Read `tasks/phase1-common.md`, your `.reports/WP14c-report.md`,
`docs/fab/open-questions.md` Q78 to Q83 and the Round 7 notes (main),
packing §5c on `lane/w3` at `e1f1d6f` or later
(`/Users/rolfie/projects/elicio/.worktrees/w3/docs/fab/packing-v2.md`,
drawings under `docs/fab/cad/v2c/` there; write the sha you used in the
report), and L8 §4 on `lane/w5`
(`/Users/rolfie/projects/elicio/.worktrees/w5/docs/fab/L8-research-v5.md`).
Lane `w1`, worktree `/Users/rolfie/projects/elicio/.worktrees/w1`, branch
`lane/w1-r6` on top of `7d111c6`; `git merge main` first. Start line
(coordinator restarts you by copy-paste):

    herdr agent start w1 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Why: the layout grid closes only at width 22 on two sides (66 of 66 with
the USB-C receptacle hanging outside the face, 64 of 64 without it). The
receptacle needs M1 ≥ 58.3, which Rolf has not measured, so the shell the
build carries is 22 wide, 9.0 outer (Q38 unchanged), no USB opening, two
charging contacts on the tail (Q81), bosses at §5c's hole sites (Q82),
neck-end tab strips with no side pockets (Q83). Nothing is ordered.

Owns: the WP14 files (`scripts/cad/bte_fit_shell.py` shell path,
`scripts/cad/render.py`, `scripts/cad/manifest.py`,
`scripts/cad/params/shell_v2.toml`, `tests/test_cad.py`,
`docs/fab/cad/v2/`, `docs/fab/shell-v2.md`). Not the packing, not the
board, not order 1, not Stage B v2's results, not plan v2, not
open-questions.

Deliver, every number measured on the built solid:

1. **Width 22.** The width parameter in `shell_v2.toml` becomes 22; the
   cavity, island and leftover follow §5c's width-22 chord-47.90 geometry
   (island u 2.25–19.75, s 16.00–37.60; leftover per §5c); outer height
   9.0 and TOTAL_CHORD 47.90 unchanged; every V2 check re-measured at the
   new width (walls, slot, ring seats, standoff, tab envelopes, edge
   radii, lateral unbroken).
2. **Bosses (Q82).** The two island bosses at §5c's hole sites (13.45,
   17.70) and (17.95, 17.70), Ø2.10 pilots, OD ≥ 5.0, tops 0.5 below the
   standoff tops; a new `V2_BOSS_sites` check reads the §5c table (no
   hard-coded sites) and measures centre error ≤ 0.05 and ≥ 3.30 clear of
   every §5c courtyard; `V2_BOSS_pilot` kept.
3. **Tabs (Q83).** Neck-end strips with the SIG1 and SIG2 lengths §5c
   gives at width 22, channels for them in the neck measured, no side-wall
   pockets; the REF end-wall slot stays; `V2_TAB_envelope` on the new
   geometry.
4. **Two charging contacts on the tail (Q81).** At §5c's P4 and P5 sites
   (0.75, 44.0) and (21.25, 44.0) in board u/s: the same ring-pad-under-
   standoff construction as the EMG domes (titanium dome, brass standoff,
   captive hex well), or, if the tail cannot take two more standoffs,
   flush pads through the tail end wall with the same clamp; say which
   and measure: pad exposure, nylon around each pad, ≥ 3.0 of nylon
   between the two, ≥ 2.0 from the REF dome and from the medial screw
   well. The hook-end wall stays solid: `V2_USB_end` becomes
   NOT_APPLICABLE by name with "Q81: no receptacle at M1 52", and a new
   `V2_CHARGE_pads` measures the above. Do not cut a USB opening; WP14e
   does if M1 says so.
5. §7 look re-measured at width 22, Q76 hook root kept, renders
   regenerated with honest stamps (the medial view shows the two tail
   contacts), `shell-v2.md` §2, §4, §5 rewritten, manifest
   `provisional: true`.

Gates: `.venv/bin/python -m unittest discover -s tests -v` green with the
CAD tests running; order 1 byte-identical; Stage B v2 manifest unchanged
except the stamp; shell identical twice; exit 0 with every measured check
passing (NOT_APPLICABLE rows do not fail the build); `git status --short`
empty. Commit in steps; last commit `shell(v2d): width 22 on §5c, bosses
at the hole sites, neck-end strips, tail charging contacts`. Report
`.reports/WP14d-report.md` (untracked) with before/after per check, the
§5c sha used and the two renders' paths. Closing steps per the common file
with `<PKG>` = `WP14d`, `<lane>` = `w1`, also when you fail.
