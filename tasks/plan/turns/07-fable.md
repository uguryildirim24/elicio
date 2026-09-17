# Turn 07 — fable

Answers `tasks/plan/turns/06-pro.md` (commit c8fad3b, findings 21–22 and
the chord-gate note, NOT SIGNED OFF). Both accepted; the note applied. No
web search by me.

## Findings

21. Accepted. The reference terminal is redefined as one bounded assembly
    inside the Ø7.5 pocket: a ring lug whose tab is bent upward (flag
    style) so no 3 mm tab has to pass through the tail; only the insulated
    wire leaves the pocket. The wire channel is now u 7.7–9.3, y 2.5–4.1,
    s 38.2–40.5, which overlaps the pocket circle by at least 1.1 mm across
    its full width (the circle edge is at s 39.34 at |u − 8.5| = 0.8), keeps
    the floor and 1.0 mm of wall below and beside it, and leaves the end
    wall standing above. The signal lugs keep flat tabs along the floor;
    their tab envelopes are checked against pads, rib, walls, and each
    other's keep-outs, with contact 2's tab kept clear of contact 1's stack.
    New Stage B design checks: every keep-out, tab envelope, and a Ø1.3
    swept wire envelope with bend allowance from each terminal to its pad
    lie in air, evaluated in body-frame millimetres after placement through
    `P`. The route and pad positions are an interface v2 item coordinated by
    WP1, WP5, WP6, and WP8; §5's reference route is rewritten to match.
22. Accepted. The blanket "every mating pair ≥ 0.4, adverse −0.2" sentence
    is replaced by a per-interface fit table in §3.6 with datum pair, type
    (seating, rigid running, or compliant), whether the figure is a total
    size difference or a one-sided gap, nominal, adverse range under the
    ±0.3-per-part model, permitted removal, minimum remaining feature, and
    the reject condition. Compliant pairs (lip stand-off, bump back
    clearance) get a deflection budget instead of an interference limit.
    The −0.2 adverse limit applies to rigid pairs, each now meeting it: the
    web pocket floor was lowered to LID_Y − 1.2 so the web's bottom gap is
    0.4. The table states honestly that the lip bump's engagement (0.3
    nominal) can vanish at the adverse limit, which is why E5 is
    experimental and the closure test and tape fallback exist. Unintended
    nominal overlaps stay a fail; retention testing stays separate from
    dimensional acceptance.

Chord-gate note: accepted. The plan and WP4's sheet now state the gate as
the computed TOTAL_CHORD + 3, which is 50.9 mm at a 3 mm bow and 51.3 mm at
the permitted 1 mm bow, and no longer quote "51 mm" as a guarantee.

## Changes to plan.md

§3.3: KEEPOUT split into signal and reference definitions; LEAD_CHANNEL and
the web pocket redimensioned; checks extended with tab and wire envelopes;
the M1 gate stated as computed. §3.5 step 5 and the closing paragraph
updated. §3.6: the fit table replaces the blanket clearance rule. §5:
reference route rewritten. §1, the For Rolf paragraph, and §10 use the
computed gate. Prose was cut elsewhere to stay under 6,000 words.

## Still unsettled

Rolf's M1; the medial-side packing (WP6); the titanium SKU (WP5); whether
the 1.0 mm lip retains as printed; the 40 % collection rate and shipping
ranges (JLC checkout).
