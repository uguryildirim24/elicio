# WP14c — shell v2c: conceal the screw, boss pilots, honest render stamp (lane w1)

Read `tasks/phase1-common.md`, your `.reports/WP14b-report.md`,
`docs/fab/open-questions.md` Q71, Q73, Q76 and the Round 7 section
(main), `HANDOFF.md` Open item 6, and L8 §4 at
`/Users/rolfie/projects/elicio/.worktrees/w5/docs/fab/L8-research-v5.md`
(on `lane/w5`, not yet on main; read it there). Lane `w1`, worktree
`/Users/rolfie/projects/elicio/.worktrees/w1`, branch `lane/w1-r6` on top
of `bb0c788`; `git merge main` first (main has the briefs and the
readings, no CAD changes). Start line (coordinator restarts you by
copy-paste):

    herdr agent start w1 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Why: WP14b's closure passes, but its screw well is a visible round recess
on the lateral face near the tail, and Q71 reads "invisible from the
lateral side"; the renders stamp "solids commit c68d4b2839c9", the
reviewer's build, on new solids; and the research lane found the pilot
hole MJF nylon wants for an M2.5 self-tapper. The USB opening and the tab
fold pockets still wait for packing §5c (WP11d on w3); this package is
what does not.

Owns: the WP14 files (`scripts/cad/bte_fit_shell.py` shell path,
`scripts/cad/render.py`, `scripts/cad/manifest.py`,
`scripts/cad/params/shell_v2.toml`, `tests/test_cad.py`,
`docs/fab/cad/v2/`, `docs/fab/shell-v2.md`). Not the packing, not the
board, not order 1, not Stage B v2's results, not plan v2, not
open-questions.

Deliver, every number measured on the built solid:

1. **Concealed screw (Q71).** Move the head well off the lateral surface:
   into the tail's end face (screw along s into a boss under the lid's
   tail lip) or into the medial tail where the skin hides it, whichever
   the one construction path builds with engagement ≥ 4.0 and a radial
   boss wall ≥ 1.4. The lateral lid and body surface become unbroken. Add
   `V2_LATERAL_unbroken`: no hole, well, slot or cut opens on the lateral
   surface (sample it; a constant is a defect). `V2_CLOSURE` re-measured.
2. **Boss pilots (Q71, Q73; L8 §4).** The tail boss and the two island
   bosses at the packing §5 boss sites carry a CAD pilot of Ø2.10 and a
   boss OD ≥ 5.00 (radial wall ≥ 1.4), and stay 0.5 below the standoff
   tops (Q73). Add `V2_BOSS_pilot` measuring each pilot Ø and radial wall.
   The Ø2.7 holes in the board island are the board lane's, not yours.
3. **Render stamp.** `render.py` stamps the commit that built the solids
   (the manifest's commit field, or the tree hash when the tree is
   dirty, marked "dirty"), never a stale constant; both renders
   regenerated; a test that the stamp text equals the manifest's value.
4. Keep the WP14b measured checks passing, the USB row NOT_MEASURED by
   name, two consecutive builds byte-identical, `shell-v2.md` §2, §4, §5
   updated, the manifest `provisional: true`.

Gates: `.venv/bin/python -m unittest discover -s tests -v` green with the
CAD tests running; order 1 byte-identical; Stage B v2 manifest unchanged
except the stamp; shell identical twice; exit 0 with every measured check
passing (the USB row does not fail the build); `git status --short`
empty. Commit in steps; last commit `shell(v2c): concealed screw, boss
pilots, render stamp`. Report `.reports/WP14c-report.md` (untracked) with
before/after per check and the two renders' paths. Closing steps per the
common file with `<PKG>` = `WP14c`, `<lane>` = `w1`, also when you fail.
