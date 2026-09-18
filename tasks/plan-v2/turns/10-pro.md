# Turn 10 — pro (plan v2)

Reviewed **2026-09-17**: `docs/fab/plan-v2.md` at **`c08b71f71c2beb4bafe035661297611087a3a990`**, retrieved as the committed blob, together with `tasks/plan-v2/turns/09-fable.md` and the complete preceding `08-pro.md`. This review assesses the incorporation of finding 26, finding 27 A–E, C14, the preceding review's §4 corrections, and the surviving release conditions. It does not substitute the author's response for the specification.

**Verdict: SIGNED OFF WITH EDITS.** Finding 26 is closed. The planning remedy for 27 A–E is accepted with the implementation conditions described below. C14 is partly sourced and remains a mandatory selected-part qualification, not a reason to keep rewriting this architecture. No blocker or major remains in the planning contract. One consolidated minor entry, **28**, lists the exact remaining editorial and handoff corrections. Apply them in the final pass; another adversarial specification round is not needed for those edits alone.

This is sign-off to proceed into the defined design/implementation work, not approval to order, a successful G7 result, or permission for untested skin-connected use. No CAD or board-load model was run and no hardware was tested. All external sources below were accessed **2026-09-17**. The Harwin drawing was inspected as a PDF page image. No supplier was contacted, quotation requested, design uploaded, purchase made, or project file other than this review written.

## 1. Provenance: the rewrite is now real

The read-only Git connector's `show` result includes the requested commit-stat information:

| Commit | Verified change |
|---|---|
| `2fbad3476df0ed5696bce3817e64d22ae880eee1` | `docs/fab/plan-v2.md` changed: **208 insertions, 133 deletions**, one file. This is the turn-07 rewrite missing from `dba5552`. |
| `c08b71f71c2beb4bafe035661297611087a3a990` | The plan changed by **123 insertions, 58 deletions**; `09-fable.md` adds 75 lines. Commit total: **2 files, 198 insertions, 58 deletions**. |

The committed plan is headed turn 09 and contains the direct-pad mechanism, narrowed R7, complete-circuit inhibit requirement, corrected voltage/transport/programming conditions and revised ledger. Thus **26 is closed**, not merely conditionally acknowledged. The earlier finding about `dba5552` remains historically correct; `2fbad34` remedied it. Do not alter earlier turn files to erase that history.

## 2. Dispositions: finding 27, C14 and the surviving conditions

“Closed with a condition” below means that the specification now assigns an acceptable implementation obligation. It does not assert that its calculation, drawing, sourcing or physical test has already passed.

### 27 A–E

| Item | Disposition | Remedy checked against `c08b71f` |
|---|---|---|
| **27A — offset, datum chain and all-three-site preload** | **Closed with a condition** | G7 now requires a common datum, supported relative tolerances, screw positions and tightening sequence. Its analysis must allow a contact to open, not provide fictitious tensile support. Section 5.3 calls 0.5 mm a starting value, not a proven offset. WP12/WP14 must produce minimum and maximum reactions for every permitted site/tolerance case. No new nominal offset is demanded in this review. |
| **27B — populated-board strain and retained preload** | **Closed with a condition** | G7 explicitly covers the populated board and components, fastener/boss loads, pull-out margin and retained preload after mechanical checks. Section 5.3 preserves off-body contact-stability testing and says static calculations do not replace it. The phrase that the whole qualification can be done on paper is absent from the operative plan. The released test plan must define load state, conditioning/duration, acceptance limits and post-test inspection; the results remain required before validation wear. |
| **27C — pad-containment region and landing states** | **Closed with a condition** | The conservative geometric expression is now `a ≤ 4 − 5/√3 − e = 1.113… − e` per axis, followed by intersection with mechanical and clearance limits. No ±1 mm workspace is granted. Worst-case screw-tip clearance is explicit. Clarify the landing-state sentence as a classification of permitted and rejected states, not a demand to accept an out-of-region contact; exact edit below. |
| **27D — cell clearance and total height** | **Closed with a condition** | The controlling requirement is now positive clearance to the deformed board with no battery support load; WP11 uses the maximum deformed envelope. The zero-clearance 3.5 mm case is acknowledged. The shorthand “4.0 standoff or a 0.5 recess” needs its height/recess combinations stated explicitly, but cannot override the positive-clearance gate. The correction is arithmetic annotation, not permission for any branch to pass. See the table and exact edit below. |
| **27E — pressure-contact materials and electrical stability** | **Closed with a condition** | Section 5.7 names nickel-plated brass against the gold pad. Section 5.3 requires a declared microvolt-scale acceptance and repeated checks after mechanical events. This is no longer asserted to be bare brass or qualified by pad area alone. Change “qualified as that pair” to “to be qualified as that pair”; exact finish, handling, contact stability and retained force remain G7 work. |

**Overall finding 27: closed with a condition.** The condition is the coupled G5/G7 implementation and validation contract now actually present. A calculation showing that interface I fails is a legitimate outcome: the plan must then reject it and qualify interface II separately, not quietly reduce force, clearance or signal requirements. Keeping I as the first candidate to evaluate is not the same as declaring it a passing or purchase-ready architecture.

### C14

**Planning requirement: accepted. Procurement evidence: partly closed, still open for the selected height and complete landing qualification.** The new evidence in §4 below establishes catalog geometry and material for 3.0 mm and 4.0 mm, plus a displayed small-quantity stock/price record for the exact 4.0 mm Harwin part. It does not establish controlled contact-face flatness, the assembled joint's performance or a complete Massachusetts delivered order. A 3.5 mm match remains unverified in this review.

A sourcing-open 3.5 mm case may be explored, but it is not an eligible architecture until the existing G3d/G7 requirement is met. No shortening, machining or substitution by Rolf is authorized. The 100-piece purchase quantity applies to the cited 3.0 mm route, not automatically to a different selected standoff.

### Surviving conditions and findings 23–25

| Item | Disposition now | Incorporation result / remaining implementation obligation |
|---|---|---|
| **23 / earlier 1,16 — R7 and hardware inhibit** | **Closed with a condition** | The universal claim about all battery wearables is gone. R7 scopes the 23 µA figure to one intact path at the stated voltage, distinguishes other return/fault paths and prohibits external connections during all skin-connected use. G2 lists switched rails, body diode, default state, digital I/O and back-power, reset and an uncooperative MCU. The proof-or-withdraw rule is present. Owner acceptance must be of this accurately limited proposal; it is not a circuit-safety certificate. |
| **24 / earlier 3,12,17 — contact workspace** | **Superseded and closed with a condition under 27** | The pin-array mechanism is gone. G5/G7 now govern the direct-pad region, force, deformation and clearance. The residual reference to underside pins in §4 is stale prose, not a second permissible architecture; delete it below. |
| **25 / earlier 15,22 — import reserve and ledger** | **Closed with a condition** | The max-of-two-percentages formula and $350–560 all-in assertion are gone. Section 9 requires complete import collection or a documented reserve, line status, no double counting, the conditional kit and meter, and the shell's delivered maximum before the first spend. G8 can still fail. Refresh route-specific allowances from actual purchased quantities; the current table is not a quote. |
| **2/18 — charger and termination** | **Closed with a condition** | G1 specifies the exact 4.20 V variant and networks, accepted termination profile, unknown capacity/runtime effect and procedural—not automatic—temperature limitation. Section 5.5 retains the system-load and off-body termination checks. Those obligations are incorporated; no charger redesign is demanded by this review. |
| **9/19 — undervoltage** | **Closed with a condition** | Section 5.5 now uses downward crossing of V_STOP, higher V_START, sensing/latency/load margins, settling and invalid-sample reasons, separate from 10-second telemetry and PCM protection. Actual thresholds and response evidence remain WP12/WP13 outputs. |
| **8/20 — acquisition, frame and protocol** | **Closed with a condition** | Section 6 includes session/epoch, frame sequence, conversion-tied acquisition index, payload count/length, metadata, status, fragmentation, wrap/reconnect and receiver fixtures. It uses more than 200 sample intervals for the physical >100 ms rule and preserves the DC path. The byte schema, filters/windows and per-criterion decisions must be released before S0; none is assumed implemented. |
| **11/21 — first load and recovery** | **Closed with a condition** | G4 now requires both-direction voltage checks rather than nominal-voltage inference. Section 8 contains the proposed numbered IDC map, with no power feed on pin 1, and requires agreement with the schematic. Board-specific provisioning/layout and update/recovery checks remain gates. Factory acceptance and price remain quote-only. A paper rehearsal cannot produce a measured physical completion time; correct that small wording below. |
| **10 — harness and polarity** | **Closed with a condition** | G1b still blocks the unresolved SH/PH footprint choice. Assembly step 6 now requires electrical polarity evidence, not wire colour or keying, and includes the meter. The exact purchased harness and safe no-solder measurement access must be established before release. |
| **4 / R3 — materials** | **Closed with a condition** | The limited-evidence acceptance language is retained; internal nickel is identified, not called nickel-free. The actual standoff/pad and skin-facing plug/finish evidence remain mandatory. No owner waiver establishes an unperformed test. |
| **6 — manufacturing tier** | **Closed with a condition** | Sides follow placement and actual acceptance under G3. Remove the obsolete pin-based explanation and keep any two-sided cost only as an allowance until the population is fixed. |
| **14 — closure and mechanical acceptance** | **Closed with a condition** | New closure/hook work remains required, without inheriting a gauge pass. Post-closure/drop contact checks are now called out. Correct their section reference, and make the pre-S0 design evidence versus post-assembly test-result timing explicit as below. |

Findings 5, 7 and 13 remain closed. No renewed objection is made to the bounded thin search, the gates-before-objectives rule or fail-closed release checks.

## 3. Literal incorporation check and arithmetic

### The §5.3 paragraph is substantively complete, but not literally verbatim

Against `08-pro.md` line 129, after joining line wraps, the paragraph in the pinned plan changes the initial **“Interface I”** to **“interface I”** following its introductory colon, and writes **“± 1 mm”** rather than **“±1 mm”**. The obligations are otherwise carried. These are editorial differences, not missing engineering requirements. The author's claim of literal verbatim incorporation is therefore too strong until the final pass restores the original text.

For exact incorporation, use a standalone paragraph after the §5.3 heading:

> Interface I is an unqualified direct-contact candidate. The released drawing names the standoff and actual top-face finish, exposed PCB pad geometry, separate board-fastener positions, nominal boss offset and its full tolerance chain. G7 demonstrates acceptable retained contact at all three sites across the permitted site region, assembly sequence and tolerance cases, with bounded PCB/component strain, board-fastener and boss loads, and positive clearance from the cell and unrelated conductors. G5 computes the permitted region from both geometric containment and those mechanical limits; no ±1 mm workspace is promised beforehand. WP11 uses the deformed maximum board envelope and a positively cleared, unloaded battery envelope. Off-body contact-stability and post-assembly mechanical checks remain release requirements; static calculations do not replace them. If these conditions fail, interface I is not eligible and interface II requires its own complete qualification and budget.

### The C14 wording is substantively carried, but also not literally verbatim

The original text in `08-pro.md` line 148 has a full stop after “delivered cost” and starts a new sentence “A near-match…”. G7 joins those sentences with a semicolon, lowercases “a”, and appends the useful no-machining restriction. No sourcing obligation was lost. Restore the original two sentences, retaining the addition as a separate third sentence:

> Before G3d/G7 passes, each standoff length actually used has an exact supplier SKU, current availability and purchase quantity, a dimensional/landing drawing, thread-depth and tolerance information, actual base material and finish, and a supported delivered cost. A near-match or generic brass family is not accepted as the selected part.

Then add: “No part is machined or shortened in Rolf's steps.” These textual changes do not justify another review round.

### The corrected geometry is a bounded calculation, not a fit promise

For the ideal 5 mm-across-flats hexagon, the circumradius is 5/√3 = 2.886751 mm. An 8 mm exposed square pad therefore gives the conservative orientation-independent per-axis bound **1.113249 − e mm**, as the plan now states. A nominal 0.5 mm boss offset is a trial input; it is not evidence of positive force at three sites. The released model must solve the unilateral contacts and include the local deformed board, not force all contacts closed in the analysis. These are now requirements of G7 rather than omitted assumptions.

The following arithmetic uses the plan's cell and foam inputs, before deformation, insulation or tolerances:

| Standoff height h | Cell-floor recess r | Nominal clearance h + r − (3.2 + 0.3) |
|---|---:|---:|
| 3.0 mm | 0 | −0.5 mm |
| 3.0 mm | 0.5 mm | 0.0 mm |
| 3.5 mm | 0 | 0.0 mm |
| 3.5 mm | 0.5 mm | +0.5 mm |
| 4.0 mm | 0 | +0.5 mm |

Thus the recess is not a general cure for the 3.0 mm case. The existing positive-clearance rule already excludes its zero result. The final edit must make that explicit rather than leave “4.0 or a 0.5 recess” as an apparent sufficient condition. Neither +0.5 mm case is a demonstrated pass once the board bends; the battery cannot become its support.

The no-clearance local module sums also reproduce the plan's range:

| Standoff | E73 reservation 2.0 mm | Raytac reservation 2.3 mm |
|---|---:|---:|
| 3.0 mm | 8.5 mm outer | 8.8 mm outer |
| 3.5 mm | 9.0 mm outer | 9.3 mm outer |
| 4.0 mm | 9.5 mm outer | 9.8 mm outer |

Each sum includes the stated 1.5 mm floor, 1.0 mm PCB and 1.0 mm lid. These are not maximum assembled envelopes or conclusions that a chosen shell closes. The plan now makes the appropriate distinction and allows a failed layout to stop.

## 4. Live-source verification: C14, C15 and the conditions

All URLs in this section were accessed **2026-09-17**. Quotes are short excerpts; displayed inventory is not a reservation and a catalog price is not a delivered quotation.

### C14: source evidence improves for the 4.0 mm branch

| Source | Verified observation and short quotation | What it does not establish |
|---|---|---|
| [Spacer Express LAI-FF-M2.5-SW5-L3-100](https://spacer-express.com/female-female/875-hexagonal-female-female-threaded-spacer-nickel-plated-brass-m2-5-5-mm-across-flats.html) | Exact 3.0 mm, female/female M2.5 through-thread, 5 mm across flats. Quotes: “Material: leaded nickel-plated brass.” and “Delivery within 5 to 10 working days”. The selected pack is 100 at **€91.08 excluding VAT**. | No on-hand stock count or qualified Massachusetts delivered total was established. This is a nickel landing, not bare brass. A simple dimensional sketch is not a controlled contact-face flatness/chamfer specification. |
| [Harwin R25-1000402 product page](https://www.harwin.com/products/R25-1000402) | Manufacturer identifies female/female M2.5, 4.0 mm body and 5 mm A/F. Quotes: “4mm body length.” and “Nickel plating for corrosion resistance.” | A product-page description alone does not qualify the pressure joint. |
| [Harwin R25-100XX02 customer drawing](https://content.harwin.com/asset/6e059b82-0a88-4a5e-8a59-36c0928fbfd1/DRG-01991-Technical-Drawing-Datasheet-R25-100-pdf.pdf) | Retrieved one-page PDF marked sheet 2 of 2, issue 4, date marked 10.09.08; inspected as an image. It shows **4.00 mm L1**, **±0.10 mm** length tolerance for lengths up to 12 mm, **“5.00 A/F MAX”**, M2.5×0.45-6H thread, brass CW614N/CuZn39Pb3 and nickel finish. The section depicts through-threading for this short part. | This advances dimensional evidence beyond the earlier page-only check. I did not authenticate dedicated top-face flatness, chamfer or plating-thickness limits adequate to qualify the electrical landing. Those remain selected-part/G7 conditions. |
| [DigiKey exact R25-1000402 listing, 952-2175-ND](https://www.digikey.com/en/products/detail/harwin-inc/R25-1000402/3728140) | The retrieved page displays **“In-Stock: 3,847”**, **$0.57 at quantity 1**, and **$2.36 for 5**. It identifies female/female, brass and nickel. | This is a stock/price observation for the exact 4.0 mm SKU, not a reserved order or final delivered price. Its generic outside-diameter field says 5.50 mm hex, conflicting with Harwin's 5.00 A/F maximum; use the controlled manufacturer drawing for geometry and reconcile the purchase documentation, not the conflicting catalog field. |

The exact 4.0 mm part is now supported by a displayed small-quantity stocking route and a manufacturer dimensional drawing. Update C14's historical “no stock count or landing drawing” summary to distinguish that progress from the still-missing contact-face qualification. Do not retroactively label the previous unsuccessful stock lookup wrong: it reported what that lookup established.

The cited 3.0 mm supplier's selectable lengths do not include 3.5 mm, and the Harwin drawing does not supply a 3.5 mm ordering row. No matching 3.5 mm part was authenticated by this review. That is a bounded retrieval result, not a nonexistence claim. The plan can keep that case sourcing-open; it need not procure every exploratory height.

### C15: the general wall datum is verified, the local recess is not automatically qualified

[JLC's PA12-HP page](https://jlc3dp.com/help/article/pa12-hp-nylon), updated 2026-07-30, states **“Wall thickness: 1mm”** and **“Tolerance: ±0.3mm (Within 100mm)”**. Its [design guideline](https://jlc3dp.com/help/article/3d-printing-design-guideline), updated 2026-08-24, gives size-dependent MJF wall recommendations: 1.0 mm at its 5×5 example, 1.2 mm at 10×10 and 1.5 mm at 50×50. It does not approve this particular cell recess.

Consequently C15 is **partly closed as a source check**. A 1.5 mm floor minus a 0.5 mm recess leaves 1.0 mm nominally. It still needs the existing local-wall/strength and manufacturing checks; the generic minimum is not proof of an adequate residual web after dimensional variation, finishing and load. No automatic instruction to thicken every wall or another prototype order follows from this observation.

### Populated-board qualification remains necessary

[Murata's mounting FAQ](https://www.murata.com/en-us/support/faqs/capacitor/ceramiccapacitor/mnt/0016) warns that PCB flex can be **“resulting in cracked chips or open solder joints.”** It establishes a relevant mechanism, not a failure threshold for this board. The revised G7 addresses that issue by requiring component-level as well as board-level limits. Actual layup, support positions, component placement, allowable strain and retained contact are implementation evidence; a generic FR4 modulus alone is not their substitute.

### The ledger correction is incorporated; the trade notice is still only a component

[CBP CSMS 69326983](https://content.govdelivery.com/accounts/USDHSCBP/bulletins/421d887), sent 2026-07-23 for entry guidance effective 2026-07-24, lists 9903.05.31 with **“an additional ad valorem rate of duty of 12.5%”** for China-origin articles subject to its exceptions. [JLC's tariff FAQ](https://jlcpcb.com/help/article/us-tariff-policy-faq), updated 2026-09-09, separately lists **“Section 301 Tariffs: 25%”** and product/material-based advance collection. Neither observation classifies this board or shell or establishes its final combined duty.

The plan now correctly requires a complete configured collection figure or supported reserve rather than selecting one of those percentages. That closes the specification objection. This turn did not obtain a configured PCBA/print quotation, a classification-specific September total, a factory SWD price or a complete-project delivered price. Actual procurement still has to pass G3/G8. For the 3.0 mm route, buy-pack quantity and international delivery must be included; for the 4.0 mm route, use that route's actual quantity and delivery instead.

## 5. Minor entry 28 — final editorial and handoff synchronization

**Severity: minor. Scope:** exact incorporation, stale cross-references and explicit application of the already-adopted gates. **Disposition:** apply in the author's final pass and proceed to implementation. These edits do not reopen the engineering choices resolved above.

The evidence is the pinned plan text, the literal comparison in §3, the arithmetic table and the live sources in §4. The following are the exact sentence actions; no old review needs overwriting.

| Location / current wording | Exact replacement or addition |
|---|---|
| §5.3 opening and G7 C14 sentence, both claimed verbatim | Use the two original passages reproduced in this review's §3 exactly, then keep the no-machining addition as its own sentence. Line wrapping is immaterial; do not claim literal identity while changing case, symbols or punctuation. |
| §4: “Assembly sides follow the released placement and are priced accordingly (interface I's pins are on the underside, so two-sided is the working assumption).” | “Assembly sides follow the released component placement and are priced accordingly; interface I has no discrete spring pins, and any two-sided allowance is provisional until placement is fixed.” |
| §12: “C11 closed by turn 06 (no stocked spring-loaded SMD pin at a 2.0–2.5 working height; the pins are gone)” | “C11 is retired from this candidate because pins are not used; turn 06 did not authenticate a pin meeting the complete low-height specification and did not prove that none exists.” This is the remaining unapplied item from the preceding review's §4; §3 already has the appropriately limited statement. |
| §1 item 3 fixes the standoff as “3.0 mm long” while §5.3/D-3 allow another selected height | Replace that parenthesis with “(female M2.5, 5 mm across flats, at the C14-qualified height selected by WP11 and G7)”. |
| §3: “the cell-under-board arrangement needs the 4.0 standoff or a 0.5 recess in the floor under the cell” | “At the planning dimensions, a 4.0 mm standoff without a recess or a 3.5 mm standoff with a 0.5 mm recess leaves 0.5 mm nominal clearance; a 3.0 mm standoff with that recess still leaves zero. These are only candidate layouts: G5/G7 must demonstrate positive worst-case clearance to the deformed board with an unloaded cell, and any recessed floor must separately pass C15.” |
| §5.3: “the pressure pair is nickel on gold, qualified as that pair” | “the pressure pair is nickel on gold, to be qualified as that pair under G7”. |
| §5.3 sentence beginning “Landing states G7 must show acceptable” | “G7 classifies full annular contact, pad-edge/hole and boundary cases, tilted-face contact and screw-tip clearance; only states inside the released G5 region with acceptable G7 contact and clearances are permitted, and out-of-region, tip-contact or inadequate-preload states are rejected.” This does not enlarge the released region or waive a failed state. |
| §5.3: “repeated after the closure and drop checks of §5.4 and WP14” | “repeated after the closure and drop checks of §7 and WP14”. Section 5.4 is the port, not the closure. |
| G7/S0 “evidenced” versus later physical checks | Add: “For S0, G7 evidence comprises the released parts/drawings, analysis, acceptance limits and off-body test procedures; results that require the assembled shell are recorded at S4 and must pass before S5. A pre-order design pass is not recorded as a passed physical test.” This makes the already-staged design/assembly distinction explicit and prevents an impossible pre-purchase test interpretation. |
| §5.6 offers either a later printed stand or folded card | Replace the stand parenthesis with “the folded-card stand serves S2; a printed stand is optional only after it is available”. R7 already establishes this order. |
| §5.4 fallback refers to obsolete “R7 (ii)” | “The end-face fallback changes only the ergonomic deterrent; R7's disconnection procedure and G2's electrical conditions are unchanged, and the selected position is recorded in the residual-risk list.” |
| §6: “VBUS present → front end off (hardware) and streaming refused (firmware)” | “VBUS present → streaming refused; hardware power-removal credit applies only if proved under R7/G2.” This aligns the shorthand with the existing proof-or-withdraw rule, not a new permission for plugged skin use. |
| §8 promises “completion time measured at WP15's rehearsal” while WP15's acceptance is a paper rehearsal | “A paper rehearsal checks completeness; physical completion time is recorded at the first off-body execution, not inferred or promised from the paper rehearsal.” |
| §9 small-parts route still says “US sellers, several parcels” while listing Spacer Express | “Selected suppliers, potentially domestic and international, with each purchased pack and parcel costed separately.” Keep the route-specific quantity and delivered-cost condition; do not treat the $80–130 allowance as a verified total for the 100-pack route. |
| §12 C14 repeats the previous no-stock/no-drawing result and says “nothing at 3.5” | “C14 remains open for the height actually selected and the complete landing qualification. Turn 10 verified the 3.0 mm Spacer Express catalog pack and the 4.0 mm Harwin manufacturer drawing plus a displayed DigiKey stock/price record; the exact 3.5 mm match, controlled contact-face details and delivered purchase remain unverified as applicable.” Add the dated links in this review's §4 to the source record. |

The four preceding §4 corrections are therefore disposed as follows: the heading/status is corrected; the unqualified ±1 mm promise is removed; the no-discrete-springs/PCB-compliance description is corrected; the low-height-pin nonexistence overstatement is corrected in §3 but survives in C11 and must receive the exact edit above. These are no longer grounds for retaining finding 26 as open.

## 6. What stays not settled — implementation and procurement gates

| Item | Required evidence, not presumed by this sign-off |
|---|---|
| Direct-contact interface I | Released screw/support locations, actual offset/tolerance chain, allowed region, all-three-site compressive reaction, populated-board strain and fastener margins; retained low-level contact through the specified checks. Failure rejects I, not the acceptance criteria. |
| C14 and C15 | The selected standoff's complete dimensional/contact/material/procurement evidence; qualified local web/recess if used. The 4.0 mm stocking observation is not the whole qualification. |
| Packing and fit | Deformed local board envelope, unloaded cell and harness, connector orientation, floor and wall clearances, final site positions, actual owner measurements and render approval. No thickness has been demonstrated by this review. |
| Electrical and firmware | G1 charger/harness and polarity; G2 complete-circuit states/off-body tests; undervoltage response; G4 image/map/I/O/recovery; G6 byte schema, receiver fixtures and dated criterion mapping. R7 still needs the owner's informed acceptance as a proposal. |
| Production and budget | Accepted assembler/BOM/side count, any programming/fixtures, selected finish and silicone evidence, each actual shipment, supported complete import/tax collection and the reserved delivered shell maximum under Rolf's ceiling. |
| Physical release | Off-body assembled-joint, post-mechanical and electrical checks before S5; the frozen controlled-validation criteria before S6. A paper template or calculation cannot substitute for these results. |
| Rolf's inputs | Measurements, ceiling, appearance/colour, destination/origin preference, objective order and informed residual-risk decision. No new demand for him to resolve the engineers' datum chain is introduced. |

C16 remains a research-only alternative, outside this selected mechanism. This sign-off does not start a research lane, select a grounding spring or authorize its substitution without the required qualification.

## 7. Stop-rule assessment

**The remaining specification disagreements are cosmetic/editorial and bounded handoff clarifications, not substantive grounds for another planning round.** The missing rewrite has landed; the coupled contact contract is now normative; the electrical and ledger replacements are incorporated. The remaining stock, force/strain, layout, circuit and test results are substantive engineering work, but the specification explicitly assigns them to gates and does not assert that they have passed. Requiring their completion during this dialogue would collapse implementation into planning and continue the loop Rolf asked to stop.

Apply entry 28's exact edits in the final pass and take the specification into implementation. Keep G3/G5/G7/G8 and the physical-release checks intact. An actual gate failure, an unorderable selected part or a proposed weakening of a requirement is a real escalation; typography, the retired pin wording and the identified cross-references are not.

## For Rolf

This revision is ready to leave the specification loop after the listed edits. The plan file now contains the rewrite, and it no longer pretends that a height offset proves all three contacts, that 23 µA is a complete USB/body-current safety bound, or that one tariff percentage is the whole delivered cost.

The board-as-spring joint is still a candidate that implementation must prove or reject. The real 4.0 mm Harwin stocking route is useful sourcing progress, not proof that the device fits or the contact works. No purchase or skin-connected use is approved by this review. Your existing spend and validation gates remain in force.

Only this review file was written. No plan, code, prior turn or design record was changed, and no vendor contact, quote request, purchase or design upload was made.

SIGNED OFF WITH EDITS
