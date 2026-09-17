# Turn 02 — pro

Reviewed: `docs/fab/plan.md` **as committed at `d887ac1`**, retrieved with `git show d887ac1:docs/fab/plan.md`, not substituted with the working-tree plan. Review and public-source verification date: 2026-09-16.

Read first: `tasks/plan/pro.md`. Then, in its required order: `tasks/plan/protocol.md`, `docs/fab/brief.md`, `docs/EARPIECE_DESIGN.md`, `docs/fab/L1-cad.md`, `docs/fab/L2-vendors.md`, `docs/fab/L3-contacts.md`, `docs/fab/L4-pod.md`, the pinned plan, and `tasks/plan/turns/01-fable.md`. The supporting documents were read through Local files in this session; only the plan was explicitly pinned to the requested commit.

This is a specification and source review, not a CAD build, electrical safety certification, or wear-test result. Public manufacturer/catalog pages were checked without requesting quotes, uploading designs, contacting vendors, or purchasing anything. Only this review file is being written.

The direction is workable: parametric CAD, a passive first fit gauge, three contacts, and a separate biological montage gate. The rejection of L4's undersized module islands is justified. The simple straight-cantilever estimate also reproduces approximately 0.88 N for the stated inputs; that arithmetic is not itself a defect. The problem is that the replacement plan still contains incompatible assembly dimensions, a wrong procurement identity, and requirements that its acceptance gates do not establish.

There are **15 findings: 8 blockers, 6 majors, and 1 minor**. Numbering starts at 1 for this first review. Findings 1–6 address mechanical construction, 7–10 electrodes and safety, 11–13 purchasing and sourcing, and 14–15 delivery contracts.

## Findings

### 1. The construction does not define one consistent assembly frame

**Severity:** blocker. **Plan:** §§3.1–3.3 and 3.5, especially steps 1, 2, 6–8.

**What is wrong.** A CAD worker cannot follow these instructions literally without making design decisions. `s` is distance along the centre path, but `BODY_LENGTH` is used as the endpoint separation of a bowed arc. Those are different lengths. The path is called a centre path while its swept section spans X = 0 to BODY_WIDTH, without stating whether contact X values are global coordinates or offsets in a moving section. The cavity is described as a rectangular cut without specifying how it follows that curved shell and preserves wall thickness.

The hook is in Y = HOOK_Y = 3, yet starts at the stated origin, whose Y is zero. Step 6 blends it into the body; step 7 then rotates the body and tail, but not the hook. Neither the lid's matching transform nor the new joint construction is defined. Step 8 subsequently places contacts on world Y = 0, although the medial face has been rotated away from that plane. This changes contact protrusion and alignment. Mirroring across YZ also reverses the declared posterior X direction; the anatomical frame for the left-ear output needs an explicit definition.

**Evidence.** The coordinate and operation definitions in the pinned §§3.2 and 3.5 are mutually inconsistent. These are deductions from the specified geometry, not claims that an existing CAD model has failed.

**Concrete fix.** Define the unpreloaded shell in a single local assembly frame, distinguish chord length from arc length, and define the section origin and transport along the path. Give the hook's actual root coordinate and transition. Apply the preload construction consistently to the body, mating lid, pockets, pads, and contacts, then define the hook-body join. Supply a transformation rule for each side. Add checks for connected solids, preserved minimum walls, lid registration, and contact axes normal to the actual medial surface. Do not leave these choices to WP1 as undocumented interpretations.

### 2. Optional measurements do not currently produce the promised valid default order

**Severity:** major. **Plan:** §§3.3–3.4, 3.7, and 10, open item 8.

**What is wrong.** M1–M8 have typical ranges, not a complete set of numerical defaults or missing-value semantics. Nevertheless, derived parameters and mandatory checks reference them. “Skip any and the default stands” does not specify whether to calculate, substitute a reference-ear measurement, or skip a fit check.

The default 48 mm body-plus-tail requires M1 ≥ 51 mm. The proposed shorter-ear fallback is 38 + 8 = 46 mm and still requires M1 ≥ 49 mm; it does not cover the plan's stated 45–48 mm examples. Reducing a battery pocket from 16.8 to 16 mm is not an established solution to either the anatomical length problem or the cell-fit problem.

The sulcus comparison uses body thickness alone. The nominal skin-to-lateral span including the stated contact protrusion is 9.2 + 0.6 + 1.65 = **11.45 mm before deformation**, not 9.2 mm. A fit check must use the assembled, loaded geometry rather than silently omit the electrodes. Testing one user's ear also cannot substantiate “generic shells fit most adults.”

**Evidence.** Direct arithmetic from §§3.3, 3.4, 4 and 10. L1's measurement ranges are not individual measurements or population validation.

**Concrete fix.** Publish a complete default parameter set, explicit precedence and null handling, and which checks are design checks versus measured-ear checks. A no-measurement build may remain available as a provisional gauge, but must not be described as a verified personalized fit. Define the supported measurement domain and reject unsupported combinations rather than shrink a battery pocket by assumption. Check the complete contact/shell envelope, including glasses and preload, against the measurements.

### 3. The signal-contact formula puts a contact under the battery

**Severity:** blocker. **Plan:** §§3.3, 3.5 and 5; §2, row 8.

**What is wrong.** With `s` increasing downward, the written formula gives:

| Quantity | Derived value |
|---|---:|
| Contact 1 | X = 4.5, s = 22.5 mm |
| Contact 2 X | 4.5 + 12 sin(30°) = 10.5 mm |
| Contact 2 s, as written | 22.5 − 12 cos(30°) = 12.108 mm |
| Contact 2 s, opposite sign | 22.5 + 12 cos(30°) = 32.892 mm |

The written second contact lies in the superior battery region, not the inferior board region. It contradicts the packaging justification that the two signal contacts sit below the board and cannot share the battery pocket.

Changing the sign alone is insufficient. The allowed first-contact clamp extends down to s = 19.5. A 3.75 mm-radius hardware keep-out there reaches s = 15.75, across the battery/rib boundary. The required checks only constrain dome crowns to the face; they do not constrain the complete moving hardware against the battery, rib, sidewalls or board supports.

**Evidence.** Literal evaluation of the formula in §3.3 against the pocket/rib placement in §3.5. No biological assumption is needed to establish the collision.

**Concrete fix.** Correct the intended direction and resolve global versus section-local X under finding 1. Derive the allowable contact-position range from full hardware swept volumes and manufacturing clearances, not just dome diameter. Reject conflicting measurement/montage overrides. Test both signal contacts and the reference against the battery, rib, pads, wall margins, tail, wire routes and lid at every permitted travel position. If the biologically useful montage is outside that feasible domain, revise the shell instead of clamping the coordinates into it.

### 4. The floating contact assembly exceeds its depth reservation and lacks a secure moving electrical joint

**Severity:** blocker. **Plan:** §§3.3, 3.5 step 8, 4, 5 and 10, open item 1.

**What is wrong.** Using the conventional under-head length of the specified M3 × 6 button-head screw, the tip projects **6 − 0.6 − 1.2 = 4.2 mm** beyond the inner wall at the stated compressed washer thickness. The board underside is only 3.6 mm above that wall. The nominal screw already crosses the board plane by 0.6 mm, before adding tolerances or further inward travel. This is not merely an unknown nut thickness that can be discovered later.

There is also a solid-versus-clearance contradiction: step 8 cuts a 3.6 mm-deep pocket into a 1.2 mm body floor; §5 instead describes a 3.6 mm-high free volume above that floor. Literal cutting would breach the wall. The tail pocket and body hardware reservation require different constructions.

Finally, the one-nut stack clamps the ring lug against the shell only at its outward stop. When the stud moves inward and the nut lifts, no described feature positively locks the lug to the moving stud. Electrical continuity under motion is therefore unestablished. The specified 22–26 AWG crimp terminals also do not match the specified 28 AWG wire.

**Evidence.** Dimensions and assembly order in §§3–5. The screw-length calculation assumes the intended M3 button-head convention; finding 11 separately establishes that the named catalog part is not that screw at all.

**Concrete fix.** Select the actual contact hardware and draw an assembled axial section through both travel limits, including screw tip, lug barrel, wire bend, retention and insulation. Define a mechanically secure conductive joint that does not depend on the lug being pressed against the stationary shell. Match terminal and wire specifications. Preserve the medial wall and distinguish cut pockets from reserved free space. Resolve the full travel envelope with WP5 before freezing shell thickness; a shorter post or another joint may be preferable to automatically making the body thicker. Require a bench continuity-under-motion test and assembly-tool access check.

### 5. The lid geometry and print rules do not support the promised closure

**Severity:** blocker. **Plan:** §§3.3, 3.5 steps 4–5, 3.6, and WP1–WP2.

**What is wrong.** The 14 mm-wide rebate in a 15 mm body leaves a **0.5 mm outer rim**; the corresponding end rim is also 0.5 mm. The tongue slot further reduces an end-wall section. These local features are not captured by listing the main walls as 1–1.25 mm.

If “starting 6.0 below the ledge” means inward depth, the 2 mm-tall snap recess reaches 8 mm below it: beyond either cavity. No alternate datum is supplied. The thin cavity depth is also inconsistent: its formula yields 7.6 − 1.2 − 1.0 − 0.1 = **5.3 mm**, not the stated 5.4. The common lid's tab insertion geometry, tongue's third dimension and mating clearances are not fully fixed. A worker must invent a closure that fits both variants.

**Evidence.** Derived rim/depth dimensions above. Independently checked JLC sources contradict the adopted DFM assumptions:

- [JLC PA12-HP specification](https://jlc3dp.com/help/article/pa12-hp-nylon), updated July 30, 2026: ±0.3 mm within 100 mm and a listed 1 mm wall thickness, not the plan's ±0.15 mm and 0.8 mm minimum.
- [JLC design guideline](https://jlc3dp.com/help/article/3d-printing-design-guideline), §§2–5: size-dependent nylon wall recommendations, more than 1.5 mm recommended for snaps/fasteners, 0.8 mm embossed depth/width, and 0.2–0.4 mm assembly clearance. Its separate 0.6 mm moving-part guidance is qualified by geometry.

The drawing's cavity +0.2/−0.0 and contact ±0.2 callouts are not demonstrated capabilities of the selected standard service. Nominal clearance and guaranteed worst-case fit are different.

**Concrete fix.** Provide a fully dimensioned closure section for each thickness and recalculate every remaining wall after rebates, slots and reliefs. Resolve the supplier recommendations rather than copying L1's numbers. Use a tolerance stack for lid/rebate engagement, tabs, contact holes and board insertion; specify any permitted post-finishing or fit coupon. Either demonstrate one common lid works for all three bodies or name separate lids and update the order. Watertight STL checks must be supplemented by minimum-wall, engagement and interference checks.

### 6. The revised electronics envelope still has no feasible demonstrated packing arrangement

**Severity:** blocker. **Plan:** §§1, 3.3, 3.5, 5, WP5 and §10, open item 2.

**What is wrong.** Correcting L4's island width does not establish that all selected electronics fit in the new box. Section 5 describes one 18 × 12.5 mm board with a component-free medial side. The named module occupies 15.5 × 10.5 mm. An axis-aligned placement leaves only 2.5 mm of total longitudinal separation or 2 mm transversely: neither accommodates the selected ADS1292 TQFP's 5 × 5 mm body beside it. This excludes leads, passives and protection parts. No second board or alternate arrangement is reserved in the 3.3 mm usable height.

The board zone also has exactly the same nominal width as the cavity, despite wires supposedly rising beside the board. FR4 1.0 plus 2.1 mm components leaves just 0.2 mm beneath the lid, while retention adds a 1 mm foam pad without specifying its compressed thickness, load or bearing locations. The battery pocket has no linked maximum-dimension drawing for a particular protected cell, tabs, folded PCM or wire exit.

**Evidence.** [Raytac specification, Version L](https://www.raytac.com/download/index.php?index_id=43), printed pp. 7 and 11, inspected as page images: the module is nominally 15.5 × 10.5 × 2.05 mm; its dimensions have tolerances, and antenna layout requires an all-layer no-ground region and edge-oriented placement. A generic “5 mm from battery” sentence is not that keep-out drawing. [TI ADS129x datasheet, Rev. C](https://www.ti.com/lit/ds/symlink/ads1292.pdf), p. 1, confirms the 5 × 5 mm TQFP body used by L4. The packing and stack-height conflicts are deductions from these dimensions and §5.

**Concrete fix.** Produce a bounded packaging layout using maximum part dimensions: module, AFE, representative required passives/protection, board thickness, battery/PCM, leads, insulation, contact swept volumes, foam and RF exclusions. Define nonzero board insertion/wire clearances and the battery's actual retention geometry. This is an envelope proof, not a request to finish the PCB. If the current component choice cannot fit, change the component arrangement or shell envelope explicitly before WP1's production-intent geometry is frozen. Do not describe 9.2 mm as guaranteed while WP5 may invalidate it.

### 7. Nominal dome pressure and a rigid fit gauge are being asked to validate the dry-electrode design

**Severity:** major. **Plan:** §2 rows 4 and 10; §§3.7 and 4; WP3, WP6 and WP7.

**What is wrong.** The correction of L3's disk-area arithmetic is useful, but 0.3–0.4 N divided by a 5.7 mm projected disk is not a measurement of local skin pressure under a curved, socketed screw head. The cited 10–25 kPa window has no identified experimental source applicable to this site and geometry. Nor does a total hook reaction establish equal force at three contacts.

The 100 g tail test measures a particular stiffness/load case, not the distribution of contact forces on an ear. Rigid printed caps do not reproduce the floating metal assembly, socket edges, foam compression or electrical interface. Gel-electrode montage results can establish useful locations but do not establish that these dry contacts retain adequate signal during jaw motion and repeated donning.

**Evidence.** L3 §7.2 supplies the pressure assertion without a source page. The limitations follow from the different geometries and test objectives in §§3.7, 4 and WP6. `docs/EARPIECE_DESIGN.md`, Stage B exit, requires three separate days with the same threshold and false-positive testing while eating, talking and walking; the plan's WP7 acceptance lists geometric checks instead.

**Concrete fix.** Label force and nominal pressure as exploratory engineering targets, not established comfort or electrode-performance bounds. Specify a bench force/travel/continuity characterization for the actual assembly and distinguish passive fit acceptance from active dry-signal acceptance. Add an actual-contact validation gate covering baseline stability, signal/noise, saturation/dropout, movement and three-day re-donning at a fixed threshold. Establish an impedance/noise budget tied to the AFE; any on-body impedance test needs its own reviewed safe method, not an ordinary mains-connected meter. The test protocol and acceptance criteria are needed now; the experiments themselves remain later work.

### 8. The stainless fallback breaks the binding nickel-free requirement, and DMG is not a composition certificate

**Severity:** blocker. **Plan:** §2 row 3; §4; §6; §10, Open for Rolf item 5.

**What is wrong.** The plan acknowledges nickel in 316/316L, then offers it as a purchasable skin-contact fallback and asks Rolf to choose it as the cheaper option. Elsewhere it says skin-facing metal is titanium only. A release threshold and a nickel-free composition requirement are not interchangeable. An option that changes the binding brief cannot be treated as an ordinary materials preference within this plan.

Buying on a grade label and accepting a negative DMG swab also does not establish the stated “0% nickel.” Absolute zero, nominal alloy composition, surface contamination, and nickel release are different claims. Hidden hardware may use different materials, but its isolation from skin must be real, including at the open reference pocket and any charging interface.

**Evidence.** The fabrication brief and `docs/EARPIECE_DESIGN.md` require nickel-free contacts. L3 itself distinguishes 316L composition from release. [Thyssen et al., 2010](https://pubmed.ncbi.nlm.nih.gov/20536475/) tested 96 metallic earring components and reported 59.3% DMG sensitivity against EN 1811 release results. That study establishes a limitation of negative screening; it is not a measured false-negative rate for this proposed titanium device.

**Concrete fix.** Remove the 316 skin-contact fallback from the compliant order path unless the owner separately changes the requirement. State one supported titanium material/finish specification and its documentary acceptance evidence, with no nickel-bearing underplate. Replace the absolute-zero claim with the actual supplier/lot specification. Retain DMG as a supplemental reject screen, not proof that a part is nickel-free or a substitute for material traceability. Enumerate and protect every other potentially exposed metal surface.

### 9. The HP material claim is partly verifiable; the finished dyed shell and four-hour wear claim are not

**Severity:** major. **Plan:** §2 row 7; §§3.7 and 6; claims 6–7; §10, open item 3.

**What is wrong.** “Safest uncertified polymer,” “no residual monomer,” and accepting an unverified dye by wearing it for four hours are unsupported conclusions. A lack of an immediate visible reaction does not certify a finished part for repeated skin contact. Changing to natural grey removes one added variable; it does not prove the remainder of the manufacturing and cleaning process.

**Evidence.** [HP's current materials portfolio](https://www.hp.com/us-en/printers/3d-printers/materials.html), PA12 enabled by Evonik section, does state USP Class I–VI and intact-skin guidance claims. Its PA12 disclaimer describes preliminary testing of representative printed parts. Thus the manufacturer's broad statement is verified, rather than merely the author's recollection. I found no evidence in that page qualifying JLC's particular black dye, its finishing/cleaning process, or this assembled shell. Claim 7 remains unverified.

**Concrete fix.** Cite the HP statement with its limited scope and remove the unsupported superlatives/absolutes. Make the first wearable finish an explicit decision supported by process information; use natural grey as the default while black-dye evidence is absent, without calling grey certified. Identify the foam and cleaning compatibility separately. Replace “try four hours and reorder if red” with short initial fit inspections, immediate removal on pain, numbness or skin reaction, and conditional progression to longer wear. Comfort observations must be recorded as observations, not biocompatibility proof. Black versus grey is not solely an aesthetic choice while the material gate is open.

### 10. The shell does not enforce the electrical-safety statements it makes

**Severity:** blocker. **Plan:** §2 rows 15–16; §§4–6; WP5 and WP7.

**What is wrong.** A medial charging window does not by itself make charging while worn physically impossible. The proposed pads introduce conductors other than the three protected electrode leads; their covering, material, isolation and disconnected state during wear are unspecified. “No mains-capable opening” also cannot be inferred from a 2 mm cable hole or absence of a conventional power socket.

The 220 kΩ resistors near the board protect paths through those resistors, not an accidental connection from an upstream electrode lug/lead to the cell or charging conductors. The plan has not reserved insulation or strain-relief features that keep the moving bare hardware and pre-resistor leads isolated from those sources. Conformal coating is not a complete definition of that boundary, particularly around moving contacts and an unsealed reference pocket.

**Evidence.** The direct skin-to-board and optional charge/debug paths in §§4–6, compared with the design record's battery-only, never-charge-worn and protection-on-every-lead requirements. This is a circuit-path and mechanical-isolation review; no leakage-current safety test has been performed.

**Concrete fix.** Keep charging/debug interfaces inaccessible during wear by a defined cover, removal/disconnection mechanism or hardware interlock; do not rely on pad placement alone. Explicitly require the charger and externally powered connections to be disconnected for worn use. Reserve insulation, strain relief and mechanical exclusion volumes for every pre-resistor conductor, including the reference. Have the board handoff show a separately current-limited and protected path for each of the three skin contacts and no bypass to battery/charger conductors. Gate active wear on a reviewed schematic and assembled inspection/bench checks. Leave the charge window absent until that integrated interface is specified.

### 11. The named titanium contact SKU is a stainless-steel M8 locknut

**Severity:** blocker. **Plan:** §§1, 2 row 3, 4, 7.2 and claim 8; author turn 01, contact choice.

**What is wrong.** `McMaster-Carr 93625A110` is not a Grade 2 titanium M3 × 6 button-head screw. This is a verified wrong identity, not a price that merely needs refreshing. It invalidates the asserted source for the selected contact's material, geometry, pack quantity and cost.

**Evidence.** [McMaster's M8 locknut catalog](https://www.mcmaster.com/products/nuts/nut-type~locknut/thread-size~m8-2/), “Nylon-Insert Locknuts / Corrosion-Resistant Stainless Steel / 18-8 Stainless Steel” row, explicitly lists **93625A110, M8 × 1 mm, 13 mm width, 8 mm height, pack of 5**. The public catalog also lists a material-certificate type for that item; it does not make it a titanium screw. The direct SKU page did not load, but the manufacturer's category table supplies the exact identity.

**Concrete fix.** Replace the candidate with an actually verified supplier part and linked dimensional/material drawing. Reconcile it with finding 4 before retaining any pocket depth or electrode dimensions. Recheck the other hardware rather than treating their L3 numbers as authenticated by association. Provide exact nut, terminal and foam identifiers, compatible wire range, required quantities, purchasable pack sizes, and the material-evidence route. This review does not nominate an unverified replacement or authorize a purchase.

### 12. Conductive TPU was rejected on a false availability premise

**Severity:** major. **Plan:** §2 row 5 and the associated Stage B contact decision.

**What is wrong.** “No print service will make it” and “revisit only if Rolf owns an FDM printer” are false as categorical statements. They also contradict the custom-printing route already present in the design record and acknowledged in the lanes. Major automated bureaus not stocking a material is a narrower finding than no service offering it.

**Evidence.** [Palmiga's own 3D-printing service page](https://palmiga.com/3d-printing/) explicitly offers FDM printing in black electrically conductive TPU at Shore 85 A and 95 A. This agrees with `docs/EARPIECE_DESIGN.md`'s Palmiga route and L3's custom-printing discussion. The page does not establish that Palmiga will accept this particular job, its price, delivery date or skin-contact performance; no inquiry was made.

**Concrete fix.** Correct the conflict table. Titanium may remain the primary route for assembly, sourcing or electrical-performance reasons, but explain those reasons without claiming the alternative is unavailable. Keep outsourced conductive TPU as a conditional alternative with quote, material and performance gates, all requiring owner authorization for any supplier contact. Do not make ownership of a printer a prerequisite that the actual supplier page does not impose.

### 13. The orders are planning allowances, not verified all-in purchase instructions

**Severity:** major. **Plan:** §§1 and 7–8; WP3–WP4; §10, open item 5.

**What is wrong.** The estimates still use an invalid contact SKU, unspecified hardware, and unverified destination shipping. Order 2 adds about $42 of shell costs to $62.65 of assumed hardware, but omits the two hardware suppliers' shipping and any applicable tax. “About $105 all-in” is therefore unsupported even before replacing the wrong part. The verification kit is also not at the stated price on the currently readable supplier page.

**Evidence checked today.**

| Item | Verification result and source |
|---|---|
| PA12-HP service | [JLC material page](https://jlc3dp.com/help/article/pa12-hp-nylon) lists MJF, natural grey, 72-hour build time and a generic price from $1.00. This is not a quote for these bodies/lids, their finish or quantities. |
| US shipping terms | [JLC's actual tariff-policy FAQ](https://jlcpcb.com/help/article/us-tariff-policy-faq), updated September 9, 2026, says US individual-customer orders use DDP. This verifies the supplier's DDP policy, not every legal assertion in L2. |
| Plastic advance-collection rate | The FAQ's rate table was an image that failed to load. The specific 40% rate remains UNVERIFIED in this review. Do not silently convert it into a verified current rate. |
| Destination shipping prices/transit | I did not verify the $6–10/10–14-day standard option or $22–28/3–5-day DHL option for this order to Massachusetts. The public [shipping page](https://jlc3dp.com/shipping) did not establish those ranges. |
| Nickel Alert | [Supplier product page](https://nonickel.com/products/nickel-alert-nickel-test-kit), SKU 1012-A, displays $24.99, an “Unavailable” notice, and shipping calculated at checkout. It also warns of surface-mail delivery. Stock and delivery were not verified. |
| Other contact hardware | Titanium candidate contradicted by finding 11; remaining exact hardware prices, availability and the claimed McMaster transit remain unverified. |

**Concrete fix.** Replace “all-in” with clearly labelled, dated planning allowances until each cost is supported. Separate printed parts, finishing, import collection, destination shipping, each hardware shipment and tax; show quantities and contingencies. Use the correct FAQ URL and distinguish merchant policy from independently verified law. Add a written checkout acceptance gate for Rolf: compatible parts/finish, current DDP line, complete delivered total and expected delivery; stop and return for revision on a material deviation. No agent should request a quote or enter checkout to fill these gaps without authorization. The $200 flag remains a purchasing check, not a guarantee based on the current table.

### 14. Cross-package changes are being carried as if they were local implementation details

**Severity:** major. **Plan:** §§7, 9 and 10; WP1, WP4–WP7.

**What is wrong.** The protocol permits carrying an issue only when its fix stays wholly within one work package and changes no other package contract. Here WP4 may change contact depth, which changes WP1's thickness and WP5's board space. WP5 may change the envelope after the first shell files are produced. WP6 may move contacts after fit approval, but the order-2 gate does not require rechecking the changed contact/body geometry. WP7's listed dependencies omit a completed contact-kit contract and its acceptance does not explicitly include actual-contact performance.

A “listed change to §5” is not an accepted envelope. A signed-off planning document cannot simultaneously treat these interfaces as fixed and authorize downstream workers to redefine them independently.

**Evidence.** `tasks/plan/protocol.md`, sign-off/carry rule; §9 acceptance for WP5; §10 open items 1–2; and order 2's stated gates. Findings 3–6 establish that the cross-package risks are concrete, not hypothetical scope expansion.

**Concrete fix.** Reorder the dependencies so hardware/packaging specifications are reconciled before a production-intent fit geometry is frozen. Alternatively, explicitly authorize order 1 only as a provisional fit experiment with no guaranteed electronics fit, and identify the expected rework and budget consequences. Define one versioned mechanical interface containing contact coordinates/travel, cell envelope, board outline/heights, RF and insulation keep-outs. Changes require coordinated review and rerunning the affected CAD/fit checks; changed contact positions do not inherit a previous fit pass automatically. Preserve the design record's three-day dry-use gate in Stage B acceptance. Experiments may remain future work; unresolved interface definitions cannot be marked carried under the present protocol.

### 15. The order confuses unique files with manufactured quantities

**Severity:** minor. **Plan:** §§3.6, 7.1 and WP1.

**What is wrong.** The output list contains three unique body models plus one lid model, while the order says to download/upload five STL files and also set lid quantity to two. There are five physical parts, not five unique models under the stated common-lid design. The instructions can cause a duplicate lid upload or an unnecessary missing-file search.

**Evidence.** Comparison of the filenames in §3.6 with the quantities and upload steps in §7.1.

**Concrete fix.** Publish an explicit file-to-quantity order manifest: each of the three body files ×1, common lid file ×2, subject to finding 5's final lid decision. Use that same manifest for export checks and Rolf's checklist. This is minor housekeeping and would not independently require another review round.

## For Rolf

Do not place either order from this revision. The problem is not whether the concept is worth trying; it is that these instructions can produce parts that do not assemble. One signal contact is mathematically located under the battery, the intended screw projects into the board space, the closure is not resolved for the thin body, and the named titanium part is actually a large stainless locknut.

Keep the parametric-shell and passive-fit-first approach. Fable should first reconcile the geometry, actual contact hardware and electronics envelope, then return one corrected plan with explicit safety and purchase gates. You do not need to resolve those engineering contradictions by choosing a colour or accepting a thicker shell now. A generic gauge can still be an option, provided it is honestly labelled as provisional rather than guaranteed to house the electronics.

No purchase, supplier contact or design upload was made during this review. Nothing here changes your nickel-free, battery-only or no-charge-while-worn requirements. The blocking findings concern the written contract; actual fabrication and wear experiments remain later work.

NOT SIGNED OFF
