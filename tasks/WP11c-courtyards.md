# WP11c — Pack with the real footprints (lane w3, runs alongside the round 6 review)

Read `tasks/phase1-common.md`, plan v2 §4 and §5, your own
`tasks/WP11b-packing-followups.md` and `.reports/WP11b-report.md`,
`docs/fab/packing-v2.md` §1e and §5, `docs/fab/board-v2.md` §11, §12 and
§15, and the board file as lane w2 left it after dropping the shorting
copper: `git show 845bac7:hardware/board/elicio-v2.kicad_pcb` (the object
is in the shared repo; the branch `lane/w2` is not yours to check out).
Lane `w3`, worktree `/home/user/projects/elicio/.worktrees/w3`, branch
`lane/w3`, on top of `bcecc83`. The round 6 reviewer merges `lane/w3` **at
`bcecc83` only**; everything after it lands in round 7. Start line
(coordinator restarts you by copy-paste):

    herdr agent start w3 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Why: WP12b placed the board from `packing-v2.md` §5 within 0.1 mm and it
cannot be routed: with zero tracks `kicad-cli pcb drc` reports 128 errors
because footprints collide. The packing table's part envelopes are
smaller than the real courtyards. WP12c's list (all at zero copper):
solder-mask bridges J3 vs SW1, J2 vs J4, U5 vs J4; shorting items J2 MP
GND vs J4 +VDD, C15 GND vs C8 +3V0, J3 SIG1 vs SW1 nRESET; Contact
netclass 1.0 mm violated by the 0402 pad gap 0.48 on R1, R2, R3 and by
J3's 2.54 mm pitch; copper-to-edge U2 pads 0.275 against 0.300 and J2 at
the outline; hole clearance J4 NPTH vs U5; J2 and U5 inside J4's
keep-out, U3 inside U1's courtyard, R25 and C10 in RF_FEED_NOTCH. The
next board turn (WP12d) needs a layout that has none of these. Analysis
and a generated table only; no plan edit, no order.

Owns: `scripts/cad/placement_v2.py`, `scripts/cad/placement.py`,
`tests/test_placement.py`, `docs/fab/packing-v2.md` (generated, extend
the generator), drawings under `docs/fab/cad/v1/` within the Q56 cap
(closers only, at most 20 files in total). Not the board files, not the
shell.

Deliver:

1. **A real part table.** For every footprint on the board, read from the
   KiCad file: reference, footprint name, courtyard rectangle (F.CrtYd),
   pad extent, any keep-out the footprint or a zone carries (U1 module
   keep-out and RF_FEED_NOTCH, J4 USB-C keep-out), and put those sizes
   into `placement_v2.py`'s part table with a test that reads the KiCad
   file and fails when the table and the file disagree by more than
   0.05 mm. Keep the round 5 sizes as a second column so the difference
   is visible in `packing-v2.md`.
2. **Rules the search must meet**, each cited: JLC FPC assembly edge
   2.5 mm (board-v2 §12 / L6), copper-to-edge 0.30, courtyard-to-courtyard
   ≥ 0 with the DRC's solder-mask bridge margin, the Contact netclass
   clearance as WP12b set it in `elicio-v2.kicad_pro` (report what it is;
   if 1.0 mm cannot hold on a 2.5 mm tab with an 0402 across it, the
   table gives two variants: the 220 kΩ moved onto the island at the tab
   root with the tab carrying one trace, or a wider tab; the reviewer and
   the board lane pick), the module keep-out empty of everything, J4 on
   the hook-end end face with its plug volume, SW1 under the lid recess,
   J3 and TC2030 reachable.
3. **The search** on the w20 × y8 body (the shell as built) for the
   501012 pack case (13.0 × 10.1 × 5.1 with PCM, foam 0.5) and, as a
   second table, the 17.0 × 10.0 × 5.0 501015 pack at +1.5 mm of arc
   (valid only if M1 ≥ 52.5): a layout with zero courtyard overlaps and
   every rule above met, or the first rule that cannot be met with the
   reason. Keep the winner's contact sites and the REF tab path
   (`REF_end_wall_slot` is cut in the shell); if the sites must move, say
   by how much and why.
4. **Publish** as `packing-v2.md` §5b "Layout for the board lane, v2":
   every part's (u, s, rotation) and the courtyards, the tab exits, the
   outline, the keep-outs, in the form WP12d can place from and test
   against within 0.1 mm. Drawings of the closers only.

Gates: `.venv/bin/python -m unittest discover -s tests -v` green (your
venv has `.[cad]`); `packing-v2.md` regenerated, not edited; order 1
untouched; the round 5 tables unchanged; `git status --short` empty.
Commit in steps; the last commit is `packing(v2c): real courtyards, layout
v2 for the board`. Report `.reports/WP11c-report.md` (untracked): the
size differences, the rule set, the two layouts or the blocking rule,
"Needs a decision", the final sha. Closing steps per the common file with
`<PKG>` = `WP11c`, `<lane>` = `w3`.
