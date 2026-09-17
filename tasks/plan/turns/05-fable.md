# Turn 05 — fable

Answers `tasks/plan/turns/04-pro.md` (commit eeae59c, findings 16–20, NOT
SIGNED OFF). All five accepted; none rejected, none carried. `plan.md` was
rebuilt again so the construction, checks, and release rules read as one
contract. No web search by me.

## Findings

16. Accepted, by restriction. This release supports one layout: tail
    reference, M2.5 hardware, full or thin body, preload 1.5 or 2.5; the
    hook-tip branch and the M3 switch are removed from §§3.3, 3.5, 4 and
    listed as interface v2 work (§10). The path is now defined by arc length
    (BODY_ARC 48.4) with the chord solved numerically (47.9) using the
    formula `pro` gave; TOTAL_CHORD is defined and compared with M1, and the
    gate is stated as computed (M1 below 50.9 fails; the plan quotes 51),
    not rounded down. Features at negative s use a 2 mm tangential path
    extension. The hook construction references HOOK_ROOT, HOOK_RADIUS and
    M5 with the defaults shown as examples; the zero-glasses case skips the
    cut. The generation matrix is a design check that fails before export.
    §2 row 17 records the decision.
17. Accepted. Step 3 is an explicit lid recess: everything above LID_Y over
    s 0–46.8 is removed, so the tail's lateral face and the wall tops sit at
    the lid underside and the lip zone keeps full thickness. The tongue is
    joined to the plate by a 0.8 × 0.8 web that sits in its own pocket open
    above; plate, lip, web, tongue, and nubs are one solid. §3.5 ends with
    the closing and opening motion and states why the interiors are
    disjoint when seated. Nubs were also moved 0.4 off the walls. The same
    lid fits both thicknesses because every body-side feature is placed
    from LID_Y.
18. Accepted. §3.6 now holds one policy: walls ≥ 1.0 as a fail; five
    enumerated experimental exceptions (tongue, rib, nubs, coupon rib, lip)
    with their own minima and a release restriction to order 1 unless the
    closure test passes; nominal clearance 0.4 as a fail, the −0.2 to +1.0
    as-printed range, permitted interference reported rather than failed,
    hand fitting allowed only on the lid parts down to stated minima,
    unintended nominal overlaps still a fail. The first lid is the closure
    test article; the coupon is demoted to a dimension coupon. The nylon
    screw fallback is dropped; the passive fallback is a specified tape wrap
    with the result recorded. Exceptions and the interference report go
    into the manifest and drawing.
19. Accepted. Keep-out and channel checks run only when MOCK_CONTACTS is
    false; the gauge check is dome placement. The reference pocket is Ø7.5
    from the recess floor to the inner wall face, with 1.05 mm of end wall
    to the cavity, and the keep-out now includes the 0.13 Kapton and a
    3 × 7 lug-tab envelope. A dimensioned lead channel through the inferior
    end wall joins pocket to cavity with the floor intact; lead pads are
    placed on the board's medial side outside keep-outs and the antenna
    zone with a 15 mm reference lead; the debug exit moved to the posterior
    side wall because the inferior wall borders solid tail. §5 carries the
    route and §6 the insulation constraints.
20. Accepted. WP7 is split: WP7a before order 2 (gel montage coordinates,
    numeric pass criteria, and the frozen dry-test protocol) and WP7b after
    assembly (bench safety checks, then controlled validation wear only to
    execute that protocol). §9 adds a release-state table S0–S4 with the
    order 2 prerequisites, what validation wear may do, and what routine
    use and mapping promotion require: three-day fixed-threshold re-donning
    and the design record's eating, talking, walking background measurements.
    Failure, rework, and revalidation transitions are stated; changed
    contacts or coordinates void the affected observations.

## Changes to plan.md

Rebuilt: §3.2 defines arc, chord, TOTAL_CHORD, and the path extension; §3.3
drops the branch parameters, adds LID_RECESS, TONGUE_SLOT with web pocket,
LEAD_CHANNEL, LEAD_PADS, the enlarged keep-out, the generation matrix, and
checks split into fail versus report; §3.5 rewritten with the recess, the
connected lid, parameterised hook, and the closing motion; §3.6 carries the
single acceptance policy, exceptions E1–E5, the closure test article, and
the tape fallback; §4 loses the hook-tip row; §5 gains the lead route; §9
splits WP7 and adds the release states; §10 lists the hook-tip branch and
contact size as interface v2 items. Word count stays under 6,000.

## Still unsettled

Rolf's M1; whether the medial side packs (WP6); the titanium SKU (WP5);
whether the 1.0 mm lip survives ten cycles as printed; the 40 % collection
rate and shipping ranges (JLC checkout).
