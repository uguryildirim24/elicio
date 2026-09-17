# WP8 prep — Stage B geometry path in the gauge script, provisional inputs (lane w2)

Read `tasks/phase1-common.md` first, then `docs/fab/open-questions.md`
(Q5, Q11, Q18, Q20, Q21, Q22 govern this package). Lane `w2`, worktree
`/home/user/projects/elicio/.worktrees/w2`, branch `lane/w2`,
fast-forwarded to `main` (round 3 merged at `1170b2a`). Start line
(coordinator restarts you by copy-paste):

    herdr agent start w2 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Why now: plan §9 row WP8 (order 2 files) waits on Rolf's packing pick
(Q20), WP7a's contact coordinates and the order 1 closure test. None of
those exist yet. What can be built now is the script's Stage B path with
every check the plan names, driven by parameters, so that WP8 proper is a
parameter set and a run, not a build. This package commits **no files under
`docs/fab/cad/v2/`** and changes **nothing under `docs/fab/cad/v1/`** (the
fifteen order 1 solids, the three views and `manifest.json` stay
byte-identical; the regen tests prove it).

Spec sections: plan §3.3 (all Stage B rows: CONTACT_HOLE, KEEPOUT_SIGNAL,
KEEPOUT_REF, WIRE_CHANNEL, CABLE_EXIT, RIB, BOARD_ZONE, LEAD envelopes,
MOCK_CONTACTS false), §3.5 (construction order), §3.6 (E1/E3/E5 carry into
order 2 only if the closure test passes; parametrize, do not decide), §5,
§6, §9 row WP8, §10 open item 4 (Stage B containment). `docs/fab/interface.md`
v2 §2 to §6 and §12. `docs/fab/packing-options.md` (option C geometry:
BODY_WIDTH 17 → 20, board 19 × 15.5, moved pads, wire crossing; A and B as
alternatives). `docs/fab/contacts.md` §5.3 and §8.1 (TE 31428 envelope:
0.46 stock, ring OD 5.16, barrel 1.96 wide, barrel end 8.85 from the contact
centre). `tasks/reviews/code-r1.md` defect 5 (why `MOCK_CONTACTS=false`
currently fails before export) and `code-r3.md` decisions 20 to 23.

Owns: `scripts/cad/bte_fit_shell.py` (Stage B path), a new
`scripts/cad/params/stageb_provisional.toml`, `tests/test_cad.py`
additions, `scripts/cad/README.md` section "Stage B (provisional)". Nothing
else.

Deliver:

1. **`MOCK_CONTACTS = false` builds.** Lift the round 1 guard only when the
   Stage B checks below exist and run. The body then cuts CONTACT_HOLE Ø2.9
   at CONTACT_1 and CONTACT_2, the reference pocket KEEPOUT_REF Ø7.5 in the
   tail, WIRE_CHANNEL through the end wall, CABLE_EXIT Ø2.0 in the posterior
   wall at s 36, y 3, and models (as reserved air, not printed) the signal
   stacks with the real lug: flat tab 1.96 wide, height 2.0 (Q22), from the
   Ø7.1 edge to 8.85 from the contact centre, at a per-contact angle
   parameter; the reference lug upright in the pocket per contacts.md §5.3
   with its real thickness, and report where it collides with the lid or
   pocket wall (Q21) instead of hiding it.
2. **Packing option as a parameter.** `PACKING = A | B | C` (default C per
   Q20's reading, marked provisional in the manifest): C sets BODY_WIDTH 20
   and the board zone 19 × 15.5 with the pads `packing-options.md` gives for
   C; B sets BODY_ARC +3.5 and moves the tail, channel and wrap; A is the
   plan shell. Read the pad coordinates from one place shared with
   `placement.py` (import or a small shared module), not a second copy.
3. **Stage B checks, each by name, failing loudly with the number**: hole
   through the 1.5 wall only; keep-out cylinders and tab envelopes are air
   (no nylon inside them; corner pads and rib outside them); the board
   underside at y 4.3 clears every stack top (4.13) and both barrels (3.46);
   the reference wire envelope Ø1.3 at bend radius 3 from the pocket through
   the channel to its pad is contained in the cavity air and clears the
   battery pocket, charge pads and lid (open item 4); CABLE_EXIT meets the
   cavity and nothing else; the cell envelope 5.2 × 10.4 × 15.6 fits the
   pocket with 0.5 foam; E1/E3/E5 present or absent by a `CLOSURE_PASSED`
   flag (default false: order 2 without the experiments until the test
   says otherwise); everything §3.3 already checks for the gauge still
   runs.
4. **Provisional parameter file** `stageb_provisional.toml`: PACKING C,
   MOCK_CONTACTS false, CLOSURE_PASSED false, contact positions = plan §3.3
   defaults (WP7a will replace them), Q22 tab height 2.0, with a header
   comment listing which open question each provisional value waits on.
   Building with it writes to a `--out` the user names, never to `v1/` or
   `v2/`; the tests build it into a temp dir and assert the checks pass or
   name the check that cannot pass yet (Q21 is expected to fail; the test
   asserts that specific failure with its number, so the day it passes we
   notice).
5. Manifest for a Stage B build carries `stage: B`, `provisional: true`,
   the packing option, the closure flag, the contact positions' source, and
   the Stage B check results, under the same schema (bump the schema
   version and the validator if a new key needs it; WP3's `manifest.py` is
   the place).
6. README section with the exact provisional build command and what is and
   is not decided.

Do not order or upload. Do not edit `plan.md`, `open-questions.md`,
`interface.md`, `packing-options.md`, `contacts.md`, `placement.py`
(import from it; if it needs a small refactor to share the pads, do the
smallest one and say so). If a §3.3 Stage B rule cannot be built as
written, build the closest geometry, keep the check honest, and put the
sentence under "Needs a decision".

Acceptance: the order 1 outputs unchanged byte for byte; the provisional
Stage B build runs from the README command into a temp dir with every
named check reporting; regeneration byte-identical; tests cover the
guard, each Stage B check's failing case, and the packing switch. Gates:
full suite green; the fifteen order 1 hashes and three views equal
`main`'s manifest.

Report: `.reports/WP8-prep-report.md` (keep it untracked). Closing steps
per the common file with `<PKG>` = `WP8-prep`, `<lane>` = `w2`.
