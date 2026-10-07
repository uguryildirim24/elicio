# WP9 report — Design record update

Lane `w9`, branch `lane/w9`, worktree
`/home/user/projects/elicio/.worktrees/w9`. Interpreter: Python 3.13.15
in a worktree-local `.venv`. No optional-dependency group was added;
this package touched no code.

## What was built

`docs/EARPIECE_DESIGN.md` now carries a dated section, "Fabrication plan,
2026-09-16", in the record's voice. It records the decision (CAD in
build123d, JLCPCB MJF PA12-HP, three titanium M2.5 dome contacts, the
provisional gauge first, release states S0 to S4), each plan §2 decision
once with its reason, and pointers to `docs/fab/plan.md` as the Phase 1
contract and `tasks/plan/turns/` as the review record.

The "Fabrication without a 3D printer" section is kept. A superseded note
at its top says: outsourced printing survived (now JLCPCB); stainless
contacts became titanium, and Palmiga conductive TPU remains available
but is not chosen for Stage B; hand-shaped PCL was dropped.

Open question 3 now points at `docs/fab/L4-pod.md` (Raytac MDBT50Q-1MV2 /
nRF52840 and TI ADS1292) and `docs/fab/interface.md` (WP1 then WP6).
Open question 4 is answered by the plan's §3.3 and §4, with the WP7a
montage test still ahead.

`AGENTS.md` Key Directories gained `docs/fab/`. Important Files gained
`docs/fab/plan.md`. Nothing else in that file changed.

Requirements 1 to 7 and the Stage A circuit material were not edited.
The 2026-08-13 history was not removed. New prose uses "Rolf"; older
prose still uses "the owner".

`README.md` status table was left alone. "Sensor hardware | Not
purchased" and "Personal recording | Does not exist" remain true.

## Plan §9 acceptance

Row WP9: "record updated; each §2 decision appears once."

The plan's §2 table has **seventeen** rows, not sixteen as the WP9 brief
said. The plan wins. All seventeen appear once in "Conflicts resolved"
in `docs/EARPIECE_DESIGN.md` (battery, envelope, contact metal, contact
size, conductive TPU, lid closure, gauge material, montage, contact
count, suspension, ear capture, shipping, shells and PCB, hook, gasket,
charging, short ears).

Verified by reading that section after the edit. No command prints a
count; the rows are the check.

## Gates

### Unit tests

Command:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

Result: Ran 42 tests in 0.010s. OK. (Python 3.13.15, worktree `.venv`.)
No code was changed.

### WP9 acceptance row

See above. Each §2 decision appears once. The README status table was
not run as a gate; no row was wrong.

## What was not done

- `docs/fab/interface.md` is not on this branch. Open question 3 points
  at the path WP1 owns; it was not created here.
- Requirement 5 still names carbon-TPU or stainless steel. The
  fabrication section records titanium as the Stage B pick and does not
  rewrite the requirement.
- README was not edited.
- This lane did not run `git push`. A post-commit hook on this
  worktree pushed `lane/w9` to origin after each commit. The common
  file says never push. The hook, not this lane, contacted origin.

## Needs a decision

- Requirement 5 versus titanium. The plan's §2 row 3 and §10 item 9
  already say changing the nickel-free wording is Rolf's, outside the
  plan. The record now states both the old requirement and the new
  pick. Leave them until Rolf edits the requirement.
- The WP9 brief said "sixteen" §2 rows. The signed-off plan has
  seventeen (row 17, short ears). This lane recorded all seventeen.
  No further pick is needed unless a later brief wants row 17 omitted.

## Final commit sha

`fce354ecda32424e3562402393e98ff20f2743f8`

That commit is `docs(agents): index the fabrication plan in the agent
maps` on `lane/w9`. The design-record commit immediately under it is
`ddd7cd8`.
