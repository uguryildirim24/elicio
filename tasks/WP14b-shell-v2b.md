# WP14b — Shell v2, second pass: closure, look, hook root, on the reviewed tree (lane w1)

Read `tasks/phase1-common.md`, plan v2 §7 and §8, `docs/fab/open-questions.md`
Q69 to Q77, the round 6 verdict `tasks/reviews/code-r6.md` (defects 1 to
10 on the shell, the "§7 look" section, decisions 70, 71, 74, 76),
`docs/fab/shell-v2.md` as the reviewer left it, and your own
`.reports/WP14-report.md`. Lane `w1`, worktree
`/Users/rolfie/projects/elicio/.worktrees/w1`, branch `lane/w1-r6`
fast-forwarded to `main` after the round 6 merge (check `git log -1`
shows the merge). Start line (coordinator restarts you by copy-paste):

    herdr agent start w1 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Why: the reviewer measured your shell and four checks fail: the snaps
hold nothing (no undercut, beam 0.5 thick), the USB receptacle stands
outside the end face and the hook root fills the opening, the lid rim is
R 0.8 and four of six stations along the lid are flat, the USB ligament
is negative. It also judged the look: a printed block with a hook, not
an earbud. The USB and tab-fold geometry wait for the re-pack (WP11c,
lane w3); everything else is yours now, on the w20 × y8 body as it
stands. Nothing is ordered.

Owns: the same files as WP14 (`scripts/cad/bte_fit_shell.py` shell path,
`render.py`, `manifest.py`, `params/shell_v2.toml`, `tests/test_cad.py`,
`docs/fab/cad/v2/`, `docs/fab/shell-v2.md`). Not the packing, not the
board, not order 1 (byte-identical, always), not the Stage B v2 path's
results (its manifest stays as the reviewer measured it).

Deliver, one construction path, every number measured on the built solid
(the reviewer's rule: a check that records a constant is a defect):

1. **Closure per Q71**: no snaps. A hinge lip at the hook end and one
   concealed M2.5 titanium screw at the tail into a boss (screw head under
   the lid surface or in the tail's end, invisible from the lateral
   side), engagement length and boss wall measured; `V2_CLOSURE` measures
   the lip's undercut and the screw's engagement; the S4 pull and drop of
   plan v2 §7 stated as the qualitative checks they are.
2. **Look per §7 and the verdict**: a lofted lid top across u and s with
   the crown fading to zero at the rim, the lid lapping the wall tops so
   the outside edge takes R ≥ 1.0 all round, no flat station over 3 mm on
   the lateral face (`V2_EDGE_radii` samples the whole lid, not one
   station), the tail hinge lip not stepping out in the edge-on view, the
   USB pad no longer standing proud of the end face (the opening itself
   waits for WP11c; leave the wall solid there with a NOT_MEASURED row
   named `V2_USB_end (waits for packing §5b, Q70)`).
3. **Hook root per Q76**: a circular root section blending into the
   elliptical hook with a stated fillet (measured); if OCCT cannot build
   it in the one path, say so with the error and leave Q76's fallback to
   the coordinator.
4. Keep the reviewer's captive hex wells, ring seats, slot and measured
   checks; regenerate `docs/fab/cad/v2/` (renders with honest labels),
   two consecutive builds byte-identical; `shell-v2.md` §2, §4, §5 rewritten
   for the new closure and look; the manifest still `provisional: true`.

Gates: `.venv/bin/python -m unittest discover -s tests -v` green with the
CAD tests running; order 1 byte-identical; Stage B v2 manifest unchanged
except the commit stamp; the shell build identical twice; the exit code
honest (0 only if every measured check passes; the USB row is
NOT_MEASURED by name and does not fail the build); `git status --short`
empty. Commit in steps; the last commit is `shell(v2b): screw closure,
lofted lid, hook root`. Report `.reports/WP14b-report.md` (untracked)
with the before/after numbers per check and two renders' paths. Closing
steps per the common file with `<PKG>` = `WP14b`, `<lane>` = `w1`.
