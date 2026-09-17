# Turn 06 — pro

Reviewed: `docs/fab/plan.md` **as committed at `2e7b509`**, retrieved with `git show 2e7b509:docs/fab/plan.md`. Review and public-page verification date: 2026-09-16. The working-tree plan was not substituted for the requested blob.

Read for this turn: the pinned plan, `tasks/plan/turns/05-fable.md`, `tasks/plan/protocol.md`, the complete `tasks/plan/turns/04-pro.md`, and the returned revision diff. The fabrication brief, design record, L1–L4 and turn 02 remain supporting context from the earlier reviews. I reopened JLC's PA12-HP material page and design guideline. Calculations below are analytic coordinate and interval checks, not a CAD build, physical inspection, or electrical/wear-test result.

Fable accepted all five preceding findings; none was rejected. No rejected finding is being re-argued. The restricted generation scope, explicit recess/web construction, experimental-feature disposition and separated validation release states are accepted changes, not demands for another redesign. The acknowledged future electronics packing proof and specification-based hardware sourcing remain gated work; this review does not demand completed electronics or purchased parts now.

There are **two findings, numbered 21–22: one blocker and one major**. They concern the remaining reference-route geometry and the numerical closure-acceptance contract. Previously resolved findings are not restated.

## Findings

### 21. The reference channel and new lug-tab reservation still run into solid tail material

**Severity:** blocker. **Plan:** §§3.2–3.3, §3.5 step 5, §§5–6. **Relationship:** unresolved routing/full-hardware portion of finding 19; new counterexamples from the added channel and lug-tab dimensions.

**What is wrong.** The reference pocket is centred at `P(8.5, 43.0)` with radius 3.75 mm. The new channel ends at `s = 39.25`. Subtracting the radius from the centre's path coordinate gives `43 − 3.75 = 39.25`, but that does not create a finite opening into the pocket. Even in an unwrapped `(u, s)` circle construction it would give tangency, not a throat through which an insulated wire can pass. With the actual circular pocket positioned using the specified curved map `P`, the channel does not even touch it.

At the default `BODY_ARC = 48.4 mm`, `CREASE_BOW = 3 mm`, the plan's arc equation gives chord `C = 47.9005234 mm` and radius `R = 97.1025059 mm`. For the posterior normal prescribed in §3.2, write `a = asin(C/(2R)) − s/R`. The XZ coordinates are:

`P(u, s) = (3 − R + (R + u) cos(a), −C/2 + (R + u) sin(a))`.

The shared Y interval is not the problem; the XZ cut footprints are separated:

| Default-geometry check | Result |
|---|---:|
| Reference pocket radius | 3.7500 mm |
| Channel's terminal cross-section | s = 39.25, u = 7.75–9.25 |
| Nearest point on that terminal section to the pocket centre | u ≈ 8.4213 |
| Distance from that point to the pocket centre | 4.07725 mm |
| Remaining nominal solid separation | **0.32725 mm** |

The earlier parts of the channel are farther from the pocket. Thus the cuts have no common opening at defaults. This is not a possible print-tolerance problem: the nominal channel fails the new requirement that it join the pocket to the cavity. In the same geometry, merely reaching the circle across the full channel width takes an endpoint beyond approximately `s = 39.634`, before providing deliberate overlap or manufacturing allowance. That number illustrates the error; it is not a substitute for the complete corrected route.

There is a second failure within the same reference assembly. The new `LUG_TAB` reservation is 3 mm wide and extends 7 mm from the contact centre toward its pad. The reference pad is suggested at `(u, s) = (4.0, 29.0)`. The 3 mm-wide tab is not contained by a 7.5 mm circular well followed by a 1.5 mm-wide channel. Simply extending the existing narrow channel will not clear it.

A concrete point on the specified tab direction establishes the remaining collision. Take a point 4.5 mm from the reference centre toward that pad in the XZ plane, at `y = 2.7`. In the plan's coordinates it is approximately `P(6.9791, 39.0771, 2.7)`. It is within the 7 mm tab length but:

- it is 4.5 mm from the pocket centre, outside the 3.75 mm-radius pocket;
- its `u ≈ 6.98` lies outside the channel's `u = 7.75–9.25`;
- its `s ≈ 39.08` is beyond the main cavity's end at 38.2.

It therefore remains in solid tail material at the stated floor-level tab height. A keep-out being declared in a table does not subtract this material. The suggested pad may move during WP6, but the present reference joint and route must either be defined consistently or explicitly withdrawn from the supposedly fixed interface.

**Evidence.** The pinned plan's `CONTACT_REF`, `LEAD_CHANNEL`, `LUG_TAB`, `LEAD_PADS` and construction order supply all dimensions above. `05-fable.md`, lines 42–51, says the new channel joins the well to the cavity and the lug-tab envelope is included. The coordinate calculation shows why that intended correction is not yet complete. No existing CAD file or fabricated device is alleged to have been tested.

**Concrete fix.** Define the installed reference terminal, tab/barrel orientation, insulation and wire transition as one bounded assembly. Cut a pocket/channel combination that clears that actual assembly and overlaps the well by a positive, specified amount. Distinguish the larger terminal clearance from the smaller insulated-wire channel; do not force a 3 mm tab through a 1.5 mm passage. Preserve the medial floor and minimum surrounding walls after these cuts.

Use `P` for placement but evaluate circles, part envelopes and route distances in actual millimetres in the body frame. Check a continuous swept wire envelope, including its insulation and bend/assembly allowance, from the terminal to the board—not just whether two Boolean voids meet at one point. Check the entire lug-tab envelope against the body, board supports and other reserved volumes. Coordinate the resulting route and pad location between WP1, WP5, WP6 and WP8 before interface v2 is accepted. The passive mock-contact branch need not acquire unnecessary electronics features, but the active branch cannot retain this disconnected route as its defined interface.

### 22. The closure geometry does not satisfy its blanket nominal-clearance and adverse-interference rule

**Severity:** major. **Plan:** §§3.3, 3.5 steps 6–7 and closing sequence, §3.6, WP2–WP4. **Relationship:** remaining numerical acceptance portion of finding 18. This is not a renewed objection to using an explicitly experimental snap.

**What is wrong.** The revision permits experimental feature thicknesses and separates nominal interference from print variation. However, §3.6 also says every mating pair has 0.4 mm nominal clearance, failing below that, and uses 0.4 − 0.3 − 0.3 to justify a universal worst-case interference limit of 0.2 mm. The written closure contains smaller local gaps and does not define which dimensions that calculation applies to.

The unilateral gap behind the snap bump is a concrete example. The tab's body-facing surface is at `s = −0.2`; the bump extends 0.5 toward +s, so its seated tip reaches `s = 0.3`. The groove ends at `s = 0.5`. The remaining path-coordinate gap is **0.2**, not 0.4. At `u = 11`, transforming these faces through the default `P` gives a nearest physical gap of approximately **0.223 mm**. This is a clearance to a stop face, not a diametral difference between two centred parts.

Under the plan's own convention of allowing two opposing features to consume 0.3 mm each, that gap would permit approximately `0.223 − 0.3 − 0.3 = −0.377 mm`, outside its stated −0.2 mm limit. This is a test of the plan's adopted tolerance model, not a claim that JLC's actual errors must be independent or that a printed snap will fail. A real datum-based stack may differ; it has not been specified.

The tongue illustrates the additional total-versus-per-side ambiguity. Its slot spans `y = LID_Y − 1.0` to `LID_Y − 0.1`; the tongue spans `LID_Y − 0.8` to `LID_Y − 0.3`. That is **0.4 mm total size difference but 0.2 mm clearance at each face**. Those are both valid quantities to report, but they are not interchangeable in a universal minimum-gap check. Intentional seating faces also have zero clearance and must be distinguished from running clearances. WP2 cannot implement one exact “every mating pair ≥ 0.4” test from these definitions without choosing an interpretation.

**Evidence.** The pinned lip, bump, groove, tongue and slot intervals, compared with §3.6's fail/report rules. `05-fable.md`, lines 31–41, says one nominal-clearance policy now governs them. [JLC's PA12-HP material page](https://jlc3dp.com/help/article/pa12-hp-nylon), updated July 30, 2026, still lists ±0.3 mm below 100 mm. [JLC's design guideline](https://jlc3dp.com/help/article/3d-printing-design-guideline), updated August 24, 2026, §5 lists 0.2–0.4 mm for assembled nylon parts and qualifies its guidance by geometry. Neither page supplies this closure's datum chain or makes every local fit a 0.4 mm clearance. The earlier decision to test thinner features is not disputed.

**Concrete fix.** Replace the blanket assertion with a short per-interface fit table covering plate seating, tab-to-body stand-off, bump-to-groove back clearance, bump vertical play/engagement, tongue-slot height and insertion depth, web pocket, and nubs. For each, state the two controlling dimensions/datums, whether clearance is a total size difference or one-sided gap, nominal value, adverse range, permitted material removal, minimum remaining feature size, and the condition that rejects the printed pair.

Then choose consistently: revise dimensions to meet the selected nominal minimum, or explicitly permit the smaller nominal fit as an experimental exception with its actual tolerance and finishing limits. Do not silently waive the nominal CAD check because hand fitting is available later. Keep unintended nominal solid overlaps as failures, and keep closure retention testing distinct from dimensional acceptance. No new supplier inquiry or completed physical experiment is needed to resolve this contract.

## For Rolf

The review is down to two issues. The reference wire and terminal still encounter solid nylon, and the closure's numerical fit rules do not match its dimensions. Do not release this revision for fabrication as the signed-off plan yet. These are bounded geometry/acceptance corrections, not a request to restart the project or finish the electronics now.

The provisional gauge approach remains reasonable. After the corrections, the sourcing, packing and controlled-wear gates already in the revision can govern the later work. A failed experimental snap may still use the recorded tape fallback for passive observations; it does not become an accepted active-device closure by doing so.

Minor measurement-sheet clarification for WP4: use the computed chord gate, not “51 mm” as a universal guarantee. With the permitted bow changed to 1 mm, the same 48.4 mm arc has a 48.3449 mm chord and requires M1 ≥ 51.3449 mm under the plan's 3 mm allowance. The script already has the computed check; make the phone sheet refer to its result. This clarification does not independently require another review round.

Only this review file was written. No plan, code, lane report, brief or previous turn was changed. No purchase, vendor contact, quote request or design upload was made. No new titanium SKU, shipping quote or tariff rate was authenticated in this turn.

NOT SIGNED OFF
