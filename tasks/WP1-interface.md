# WP1 — Interface v1 (lane w1)

Read `tasks/phase1-common.md` first. Lane `w1`, worktree
`/home/user/projects/elicio/.worktrees/w1`, branch `lane/w1`.
Start line (coordinator restarts you by copy-paste):

    herdr agent start w1 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

Spec sections: plan §3.2 (frames and path), §3.3 (parameters), §3.5
(construction), §4 (contacts), §5 (electronics envelope), §6 (safety), §9
row WP1, §10 "Interface v2 decisions". Evidence: `docs/fab/L4-pod.md`
(module, front end, cell, charger dimensions) and `docs/fab/L3-contacts.md`.

Owns: `docs/fab/interface.md` (new).

Deliver `docs/fab/interface.md` version 1: the mechanical interface between
the shell (WP2/WP8), the contact hardware (WP5) and the Stage B board (a
later package). It carries, as tables with units and a "From" column:

1. Contact coordinates in the body frame (CONTACT_1, CONTACT_2 via pitch
   and PAIR_ANGLE, CONTACT_REF), hole sizes, the dome, and the full stack
   above the floor (lug, nut, screw tip, Kapton) with its total height.
2. Keep-outs (KEEPOUT_SIGNAL, KEEPOUT_REF, RIB, walls, the lid recess) as
   boxes or cylinders in body-frame coordinates.
3. Lead route: reference wire channel (WIRE_CHANNEL), signal lug tabs,
   LEAD_PADS candidate positions, CABLE_EXIT, and the rule that only the
   insulated wire leaves the reference pocket.
4. Cell envelope: the 501015 class cell at maximum dimensions, PCM fold,
   pocket, and the cell-identity item left for WP6.
5. Board: outline, allowed heights per zone (pads at the corners, height
   over the keep-outs, under the lid), the RF zone the antenna needs
   (module datasheet), and where the ADS1292 and charger may sit.
6. Insulation and safety constraints on the mechanical side: Kapton, three
   separately protected contact paths, no charging port, cable exit plugged
   in Stage B.
7. Packing budget: the plan's area and height budget versus the parts at
   their maximum datasheet dimensions, and the escalation options for WP6
   (longer, wider, smaller front end) with the numbers each one buys.
8. A version header and a change-log rule: any change bumps the version,
   re-runs WP2's checks, and repeats the affected §3.7 items.

Every dimension traces to a standard (ISO 7380, ISO 4032), a datasheet with
URL and date, or a plan section. Anything you cannot trace is marked
UNVERIFIED with what would verify it.

Acceptance (plan §9 row WP1): every dimension traced; versioned. Gate:
unit tests green (you touch no code, but run them).

Report: `.reports/WP1-report.md`. Closing steps per the common file with
`<PKG>` = `WP1`, `<lane>` = `w1`.
