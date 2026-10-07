# WP14f report — WIP, stopped (out of memory)

Lane `w1`, branch `lane/w1-r6`, package WP14f. Rolf stopped the lane:
the machine is out of memory and CAD is failing. No further tests,
builds, renders, or router work after that stop.

`plan-v2.md` and `open-questions.md` were not edited. Order 1 files
under `docs/fab/cad/v1/` were not written. Packing and board files were
not edited.

Q89 (lid boss, M2.5×8, `V2_CLOSURE` pass) is already on this branch:
solids `825793e`, views `89279c2`.

## What is done (in this WIP commit)

Live shell sites read §5e from this repository at
`ab9ce9588d55aff5143828f6dd88f5d22ed8223c` (`git show`, not another
worktree). §5d at `e4b857c` stays the frozen v2.1 reader.

Code in the tree:

- `S5eShell` parser: wall table P4 (20.50, 4.35, y 4.35) / P5
  (20.50, 12.35, y 4.35), head +u, H1 (13.23, 17.70), H2 (17.95, 17.70),
  J2 (15.15, 11.35), pin table v3.
- Island bosses follow §5e H1/H2 (`h1_h2_keep_gap` 1.42).
- P4/P5 construction: Ø2.7 through the posterior wall, RING_PAD on the
  inner face, hex collar/well 3.0 into the bay, rotation 30°, clipped at
  the floor and lid. Skin-face Ø5 floor holes, rib slot and drop channel
  are not cut. Medial well stays (16.50, 41.00), M2.5×8.
- Checks rewritten: `V2_CHARGE_pads` (wall), `V2_TAB_envelope` (rib/drop
  left solid), `V2_WALL_minima` (seat probes), `V2_CAVITY_v3` (added to
  `SHELL_CHECKS`), `V2_BOSS_sites` on §5e.
- Tests, `shell_v2.toml`, and `render.py` (posterior labels, wall heads)
  updated. `VIEW_FILES` still three names.

Parser-only unittest (`CadShellV2Tests`, `CadShellV2PackingSourceTests`)
ran before the stop: 5 ok, 1 fail (`Q98` missing from the toml header).
That token was then added. The class was not re-run after the toml fix.

## What is not done / failed

A one-shot shell build to `/tmp/elicio-wp14f` **failed**. Exit 3.
`stage_b_failing`: `V2_BOARD_envelope`, `V2_CHARGE_pads`,
`V2_WALL_minima`.

| Check | Result on that temp solid |
|---|---|
| `V2_CHARGE_pads` | **Failed.** Outer open and through-hole air 1 at both seats; `nylon_between` 3.00; cell gap 3.10; `P4_wall_around` / `P5_wall_around` **-1.0** (u-thickness probe found no boundary at the offset samples) |
| `V2_WALL_minima` | **Failed.** Seat/outer open 1; sides 1.50; hinge 1.00; slot ok; same `*_wall_around` **-1.0** |
| `V2_BOARD_envelope` | **Failed.** `body_mm3` 0.0467 (nylon in the board zone from the wall standoffs) |
| `V2_CAVITY_v3` | Passed on that solid. J2 inside; `n_illegal` 0; `j2_p5_standoff_gap` -4.93 (overlap recorded, not a fail) |
| `V2_BOSS_sites` | Passed. H1/H2 (13.23, 17.70) / (17.95, 17.70); keep gap 1.42; courtyard hits 0 |
| `V2_TAB_envelope` | Passed. SIG1 10.71, SIG2 21.81; `rib_slot_air` 0; `drop_channel_air` 0 |
| `V2_CLOSURE` | Passed. `lid_engagement` 4.75; well (16.50, 41.00) |

Not done after the stop:

- Fix of `wall_around` / board-envelope overlap
- `docs/fab/shell-v2.md` §2, §4, §5 and the before/after table
- Solids written to `docs/fab/cad/v2/` (still the Q89 stamp)
- Honest-stamp renders
- Full `unittest discover`, two consecutive identical shell runs,
  `manifest.py --check-bytes`, empty `git status`
- Shell exit 0
- `DONE WP14f`

## Gates

| Gate | Command | Result |
|---|---|---|
| Full suite | `LC_ALL=C LANG=C .venv/bin/python -m unittest discover -s tests -v` | **Not run** (stop) |
| Shell CAD class | `CadShellV2BuildTests` | **Not run** after the wall CAD (stop). Parser classes: partial, see above |
| Order 1 byte-identical | — | **Not run** (stop) |
| Shell twice identical | — | **Not run** (stop) |
| Manifest bytes | `manifest.py --check-bytes docs/fab/cad/v2/manifest.json` | **Not run** (stop) |
| git status | `git status --short` | WIP commit plus this untracked report |

Plan §9 row 14 is **not** closed. The committed `docs/fab/cad/v2/` solids
are still the Q89 lid-boss set.

## Needs a decision

None new from this WIP. The temp solid already shows the P5 well
overlapping the J2 courtyard (`j2_p5_standoff_gap` -4.93) and a trace of
nylon in the board zone. That is a packing/shell clash to resolve when
CAD can run again. Rolf stopped the lane for memory, not for that clash.

## Final commit sha

`938984e24550bc61754f63b8e8260581329e0816`
(`wip(WP14f): wall P4/P5 CAD and §5e checks against pin table v3 ab9ce95`).
The report file itself is gitignored.
