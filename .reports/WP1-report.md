# WP1 report — Interface v1

Lane `w1`, branch `lane/w1`, worktree
`/home/user/projects/elicio/.worktrees/w1`. Package `WP1`.
Plan commit `0c5d0eb`. Interpreter: Python 3.13.15 (`.venv`).

## What was built

`docs/fab/interface.md` version 1. It is the mechanical contract
between the shell (WP2/WP8), the contact hardware (WP5), and the
Stage B board (WP6). Tables with units and a "From" column cover:

1. Contact coordinates in the body frame, hole, dome, and the stack
   above the floor (lug, nut, tip, Kapton) totalling 2.63 mm.
2. Keep-outs: KEEPOUT_SIGNAL, KEEPOUT_REF, RIB, walls, lid recess.
3. Lead route: WIRE_CHANNEL, lug tabs, LEAD_PADS candidates,
   CABLE_EXIT, and the rule that only insulated wire leaves the
   reference pocket.
4. 501015-class cell envelope, PCM fold, pocket, identity left to WP6.
5. Board outline, heights by zone, RF rules from the module datasheet,
   ADS1292 and charger placement rules.
6. Mechanical insulation and safety: Kapton, three separate paths, no
   charging port, cable exit plugged in Stage B.
7. Packing budget 105 mm² available vs 111 mm² required, and the four
   WP6 escalations with the area each one buys.
8. Version header and the change-log rule (bump, re-run WP2, repeat
   affected §3.7 items).

No product code was changed. No CAD was added. Optional extra
dependencies were not needed.

A `post-commit` hook pushed `lane/w1` to `origin`. This lane did not
run `git push`. The common file forbids a push; the hook did it.

## Plan §9 acceptance (WP1)

Acceptance: every dimension traced to a standard, a datasheet, or the
plan; versioned.

| Item | How verified | Command / result |
|---|---|---|
| Versioned | File header is version 1 with a change-log rule matching plan §9 | Read `docs/fab/interface.md`. Not a command. |
| Traced | Every numeric row has a From cell. Eight claims that cannot be closed from a public table are listed UNVERIFIED with an owner | Read the same file, sections 2–8 and 10. Not a command. |

Web pages used for standards and datasheets are listed in section 11
of the interface file, with URL and date 2026-09-16.

## Gates

### Unit tests

```
.venv/bin/python -m unittest discover -s tests -v
```

Result: 42 tests, OK, 0.010 s. Python 3.13.15. This lane touched no
code.

### Package acceptance

See the table above. Both items pass as a document check. There is no
second executable gate for WP1.

## What was not done

- WP2 CAD and §3.3 geometry checks (channel opening, pad-to-keep-out).
- WP5 SKU drawings (dome 4.7/1.35, lug 0.5 mm, stack inside Ø7.1).
- WP6 named cell, RF polygon from Spec L §2.3, final lead pads.
- No purchase, upload, or vendor contact.

## Needs a decision

None that block version 1. The plan already decides these; later
packages close them:

1. Brief named ISO 4032. Plan names DIN 439 / ISO 4035 (m = 1.6 mm).
   This file follows the plan. ISO 4032 M2.5 (m = 2.0 mm) does not
   fit the y 4.13 keep-out.
2. Dome Ø4.7 / crown 1.35 is the CAD contract. ISO 7380-1:2022 has no
   M2.5 row. Catalog M2.5 is 4.5 / 1.5. WP5 names the SKU; mismatch
   is interface v2.
3. Lug 0.5 mm is UNVERIFIED. Catalog #4/M2.5 lugs read 0.71–0.79 mm.
   WP5 must find a drawing ≤ 0.5 mm or bump the stack.
4. Packing shortfall ≈ 6 mm². Rolf chooses longer, wider, or a
   smaller front end after WP6 (plan Open for Rolf item 6).
5. Superior low-u board pad is 0.09 mm from KEEPOUT_SIGNAL 1. WP2
   checks it.

Design-record stainless contacts and L4 skin-side charge pads lose to
the plan. Recorded in interface section 9. Not silent CAD changes.

## Final commit sha

`a9be8874ce689aa0f380930ff82a51192a00fc2b`
(`docs(fab): add Stage B mechanical interface v1`)
