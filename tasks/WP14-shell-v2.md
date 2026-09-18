# WP14 — Shell v2: the body Rolf wears, on the round 5 winner (lane w1)

Read `tasks/phase1-common.md` first (for this package "the plan" is
`docs/fab/plan-v2.md`, signed off at `ef369bd`), then plan v2 §3, §4 G5
and G7, §5.3 (interface II), §5.4, §7, §8, §11 row 14; `docs/fab/open-questions.md`
Q28 to Q68 (Q38, Q50, Q51, Q57, Q58, Q59 govern you); `docs/fab/packing-v2.md`
§2, §5, §6 (the winner `A_501015_series_w20_y8_iII_s3` and its measured
Stage B numbers); `docs/fab/board-v2.md` §8, §11, §12 (the flex tabs,
ring pads, stiffeners, USB position); `tasks/reviews/code-r5.md` (defects
1 to 9 and decisions 57 to 62 on the CAD); `scripts/cad/README.md` (the
Stage B v2 section). Lane `w1`, worktree
`/Users/rolfie/projects/elicio/.worktrees/w1`, **new branch `lane/w1-r6`**
from `main` (the coordinator created it; `lane/w1` keeps the round 5
history and is not yours any more). Start line (coordinator restarts you
by copy-paste):

    herdr agent start w1 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Why: round 5 settled the architecture (Q50, Q51, Q57, Q58): Raytac
module, 501015 cell in series, width 20, LID_Y 8.0, interface II with the
board resting on three brass standoff tops over ring-pad flex tabs, USB-C
on the hook-end end face. Stage B v2 still exits 3 because the REF tab
crosses the cavity end wall (Q59). This package turns the winner into the
shell Rolf will order once he has measured M1: the real body and lid, the
closure, the port wall, the bosses and pockets, the renders he approves,
and the manifest. Nothing is ordered, quoted or uploaded.

Owns: `scripts/cad/bte_fit_shell.py` (the Stage B v2 path and a new
`--stage shell` output set), `scripts/cad/render.py`, `scripts/cad/manifest.py`,
`scripts/cad/params/shell_v2.toml` (new, an overlay on `stageb_v2.toml`),
`tests/test_cad.py`, `docs/fab/cad/v2/` (new: STEP, STL, 3MF, two renders,
one drawing page, `manifest.json`), `docs/fab/shell-v2.md` (new).
Not yours: `placement*.py`, `packing-v2.md`, `tests/test_placement.py`
(WP11b on lane w3 owns them this round; read them, do not edit), order 1
files under `docs/fab/cad/v1/` (byte-identical, as always).

Inputs you take as given (source in the report): the winner's numbers
from `packing-v2.md` §5 and §6 and the Stage B v2 manifest; the standoff
Harwin R25-1000402 (4.0 mm, 5 mm across flats, Ø2.7 through) or the
Spacer Express 3.0 mm part, both in the parameter file with 3.0 as the
current value (Q43, Q58: WP11's winner used 3.0); ISO 7380 M2.5 × 4
titanium dome (v1 numbers); ring pad Ø5.0, hole Ø2.7, flex 0.11 + 0.2
stiffener at the tab, 0.11 + 0.4 elsewhere (review r5 defect 3); the
USB-C plug volume 12 × 6.5 × 15 in front of the end-face opening 9.0 × 3.5
recessed 1.0 with 1.5 ligaments (coordinator note 1 to WP11; plan v2 §5.4);
the silicone plug; the tactile switch 4.5 × 4.5 × 1.6 on the board top
under the lid; M1 = 52 as the default with `provisional: true` and the
Q34 pointer in the manifest.

Deliver:

1. **The shell path.** From the Stage B v2 construction (one path, no
   fork; round 4 decision and review r5 defect 7 apply): the body with
   the three standoff hex pockets on the medial wall (5 mm across flats,
   captive, pocket depth for the standoff plus the 0.31 ring; the screw's
   Ø2.7 through-hole in the 1.5 wall; the dome outside), the ring-pad
   seat and the tab channel from each pocket to the board edge, the REF
   tab's path to the tail site with the end-wall slot (Q59) or a route
   that stays in the cavity if WP11b publishes one on `lane/w3` before
   you cut (`git show lane/w3:docs/fab/packing-v2.md`; if absent, slot
   and say so), the two or more board bosses (M2.5 self-tapping pilot
   holes in PA12, boss height so the board rests on the standoff tops
   first: 0.5 below the tops, review r5 defect 2), the cell pocket with
   the 0.5 foam (Q57), the USB-C end-face opening with the recess,
   ligaments and plug seat, the switch reach under the lid (a blind
   recess in the lid over the switch, no hole), the closure of §7 (a
   cantilever snap with beam dimensions and a strain number in
   `shell-v2.md`, or one concealed M2.5 at the tail plus a hinge lip;
   state the choice and the calculation), the hook with an elliptical
   section (axes at root and tip, blend fillet, radius from M8), the tail
   blended with the reference dome on it (Q17 provisional), outside edges
   R ≥ 1.0, the medial face flat with R0.5, no text, no visible screws
   from the lateral side.
2. **Checks on the built solid, measured never constants**: every Stage
   B v2 check passes (exit 0) including V2_TAB_envelope and
   REF_WIRE_envelope; new checks V2_BOSS (board underside on the standoff
   tops, bosses 0.5 lower), V2_RING_seat, V2_USB_end (opening, recess,
   ligaments, plug volume clear of the cavity parts), V2_SWITCH_reach,
   V2_CLOSURE (the snap's beam or the screw's engagement), V2_WALL_minima
   at the slot and the ligaments (≥ 1.0 anywhere, ≥ 1.5 elsewhere), §7's
   edge radii and facet rule as a probe, V2_TOTAL_CHORD and the M1 gate.
   NOT_MEASURED stays allowed, named, with the reason.
3. **Outputs** under `docs/fab/cad/v2/`: body and lid STEP, STL, 3MF; two
   renders (medial, lateral) and one drawing page in the v1 style; the
   manifest with `stage: shell`, `provisional: true`, every check with its
   number, the winner id, the parameter file's hash; two consecutive
   builds byte-identical (test).
4. `docs/fab/shell-v2.md`: what the body is (in plain prose), the closure
   calculation, the contact joint drawing content G7 needs from the shell
   side (pocket, seat, datum chain from the medial face through the
   standoff to the board, tolerances from JLC's page), the §7 checklist
   with each item's measured answer, what Rolf must approve (the two
   renders), and "Needs a decision".

Gates: `.venv/bin/python -m unittest discover -s tests -v` green with the
CAD tests running (`.[cad]` in your venv); order 1 byte-identical to
`main`; Stage B v2 (`stageb_v2.toml`) still builds and its manifest is
byte-identical to the round 5 one except where Q59's fix changes a check
from fail to pass (say which numbers moved); the shell build twice
identical; `git status --short` empty. Commit in steps; the last commit
is `shell(v2): the wearable body on the round 5 winner`. Report
`.reports/WP14-report.md` (untracked): what was built, each gate with
command and result, the §7 checklist, numbers taken as given with
sources, "Needs a decision", the final sha. Closing steps per the common
file with `<PKG>` = `WP14`, `<lane>` = `w1`. A mid-package prompt from the
coordinator runs after your DONE as a new turn; push another DONE for it.
Cap on generated files in the repo: nothing beyond the listed outputs;
no per-run drawings (Q56).
