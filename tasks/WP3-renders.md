# WP3 — Renders and drawing (lane w2)

Read `tasks/phase1-common.md` first. Lane `w2`, worktree
`/Users/rolfie/projects/elicio/.worktrees/w2`, branch `lane/w2`, now
fast-forwarded to `main` (round 1 merged at `121ccb3`, open questions at `9838573`; read `docs/fab/open-questions.md` after the plan) (round 1 merged, including your WP2
after review; read `tasks/reviews/code-r1.md` for what the reviewer changed
in `scripts/cad/` and why). Start line (coordinator restarts you by
copy-paste):

    herdr agent start w2 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Spec sections: plan §3.6 (outputs: `render_medial.png`, `render_lateral.png`,
`drawing.pdf` with side, medial, closure section, M1–M8, exceptions, ±0.3
general), §3.3 (the parameters the drawing dimensions), §3.5 (closure
geometry for the section), §9 row WP3, §10 open item 3 (manifest schema and
hash rule; closing check: `manifest.json` validates). `docs/fab/measure.md`
and `docs/fab/order1.md` name your files; match them.

Owns: `docs/fab/cad/v1/render_medial.png`, `render_lateral.png`,
`drawing.pdf`; a new `scripts/cad/render.py` (or a `--render` stage of
`bte_fit_shell.py`, your call, documented in the README); the manifest
schema (a documented validator, `scripts/cad/manifest.py` or similar, and
the `schema` field); additions to `tests/test_cad.py`; new entries in the
`cad` optional-dependency group. You do not change the solids except the lid emboss font (item 5): the
other fourteen STEP/STL/3MF hashes in the committed manifest stay identical. If a render
or drawing exposes a geometry defect, report it under "Needs a decision"
and do not fix the solid.

Deliver:

1. Two renders, headless and deterministic from the command line, no GUI,
   no vendor tool. `render_medial.png`: the medial face of the reference
   body (full, preload 1.5) with the three mock contact caps, the tail and
   the hook, the thin body beside it at the same scale so Rolf sees the
   thickness difference. `render_lateral.png`: the lateral face with the
   lid seated and the hook. Scale bar in mm, variant labels, commit hash
   in a corner. Shaded, not wireframe. A matplotlib triangulation of the
   STL is acceptable if it reads clearly; a GPU renderer is not required
   and must not be assumed (this is a headless lane).
2. One page `drawing.pdf` for the reference body plus lid: side view,
   medial view, and the closure section through the lip, bump, tongue,
   web and nubs; M1–M8 called out where each one lands on the part;
   exceptions E1–E5 each labelled with its nominal and its fitted minimum
   from §3.6; general tolerance note "±0.3 mm under 100 mm, JLC MJF PA12";
   a title block with the parameter set name, VARIANT, HOOK_PRELOAD,
   CREASE_BOW, TOTAL_CHORD, the chord gate, commit and date. Views may come
   from build123d's SVG exporter on the STEP (hidden lines removed) or
   from sections you compute; dimensions are the §3.3 values, not measured
   from pixels. Pin every PDF and PNG metadata field that carries a date so
   the file is byte-identical on regeneration.
3. Open item 3. Write the manifest schema down (required keys and types
   for `schema: 1`, what `files` hashes, what the `hash_rule` string
   promises) and a validator that fails loudly. Add the renders and the
   drawing to the manifest under their own map with SHA-256 and the same
   pinning rule; the fifteen solid hashes stay where they are. The
   `commit` field: define whether it is the build commit or the solids'
   last-change commit, and make the regen test consistent with that
   definition (it must not fail every time an unrelated file commits).
4. Tests: manifest validates; renders and drawing regenerate
   byte-identical; the validator rejects a manifest with a missing key.
   Skip cleanly without build123d, as `test_cad.py` already does.
5. Open question Q10: the lid emboss depends on whichever Arial OCCT finds,
   so hashes change between machines. Vendor an open-licence font (OFL or
   Apache, licence file beside it) under `scripts/cad/fonts/`, point the
   emboss at that file, regenerate the lid, and update the manifest. The
   fourteen other solid hashes stay identical; the lid's changes once, in
   its own commit that says so.
6. README: the exact render and drawing commands, the validator command,
   and the font note.

Do not order, upload, or contact anyone. Do not edit `docs/fab/plan.md`,
`measure.md`, `order1.md` or `interface.md`; if your file names must
differ from theirs, keep theirs.

Acceptance (plan §9 row WP3): two renders, one page; medial and lateral
faces, closure section, M1–M8, E1–E5, ±0.3 general; open item 3 closes
with `manifest.json` validating. Gates: unit tests green; render and
drawing commands run twice yield identical hashes; fourteen solid hashes
unchanged and the lid's changed only by the font commit.

Report: `.reports/WP3-report.md` (say which renderer and PDF library, why,
and what Rolf will and will not be able to judge from the images). Closing
steps per the common file with `<PKG>` = `WP3`, `<lane>` = `w2`.
