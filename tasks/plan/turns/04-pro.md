# Turn 04 — pro

Reviewed: `docs/fab/plan.md` **as committed at `b948e38`**, retrieved with `git show b948e38:docs/fab/plan.md`. Review date: 2026-09-16. The working-tree plan was not substituted for that blob.

Read for this turn: the pinned plan, `tasks/plan/turns/03-fable.md`, `tasks/plan/protocol.md`, and the complete `tasks/plan/turns/02-pro.md`. The fabrication brief, design record, and L1–L4 remain the supporting context read in turn 02. I reopened JLC's material and design-guideline pages for the manufacturing checks below. This is a specification review with arithmetic, not a CAD build, a fabricated-part inspection, or an electrical/wear-test result.

Fable accepted all fifteen previous findings; none was rejected. No rejected finding is being re-argued. Only remaining defects and new counterexamples in this revision are numbered below. The explicitly provisional first gauge and later packing proof are acceptable scope choices: this review does not require completing the PCB or proving the acknowledged 105-versus-111 mm² packing budget before a passive experiment. It does require a gauge specification that can be built and pass its own stated checks.

There are **five findings, numbered 16–20: three blockers and two majors**. Previously corrected sourcing and material claims are not reopened. No replacement titanium SKU was authenticated in this turn; specification-based sourcing remains subject to WP5's documentary gate, not an asserted purchase-ready part.

## Findings

### 16. The shorter-ear branch and parameter-to-construction contract are still incomplete

**Severity:** blocker. **Plan:** §§3.2–3.5, §4 hook-tip variant, and §10. **Relationship:** unresolved construction/domain portions of findings 1–2; new evidence from the replacement geometry.

**What is wrong.** `REF_SITE=hook_tip` changes the tabulated `BODY_CHORD` to 38.2 mm, but the construction still sweeps the tail to s = 48.4, places the reference at s = 42.5, and puts the lid tongue/slot at s = 46.8–48.4. There is no corresponding branch in those operations. The short path cannot support those placements.

For the specified circular arc, radius is `C²/(8b) + b/2` and arc length is `4R atan(2b/C)`, where C is chord and b is bow. At the default 3 mm bow:

| Path choice | Chord | Available arc length | Conflict |
|---|---:|---:|---|
| Tail reference | 48.4 mm | 48.8944 mm | Construction ends at s = 48.4, not at the chord endpoint; the length used for fit/preload must be defined explicitly |
| Hook-tip reference | 38.2 mm | 38.8252 mm | Reference at s = 42.5 and tail/lid features near s = 48.4 lie beyond the defined path |

Simply deleting the tail is insufficient: the cavity cut still runs to s = 38.2, exactly where the shortened body sweep ends, leaving no specified inferior end wall. Section 4 gives a hook-tip foot and groove, but §3 never constructs them or defines their full orientation, pocket/lead connection, and replacement closure.

`TOTAL_LENGTH`, used in the preload and mandatory ear check, has no derivation. Even treating the short length as 38.2 mm, the advertised M1 = 41 mm boundary fails `TOTAL_LENGTH ≤ M1 − 3`, because 38.2 exceeds 38.0. Separately, §3.5 hard-codes the hook centre, Y plane, radius and glasses cut while the parameter table says M4, M8 and M5 change them. The procedure must distinguish reference-example numbers from governing formulas. The announced M3 switch similarly has no complete derived coordinate/closure schedule.

**Evidence.** Direct comparison of the pinned parameter table and construction, with the arc arithmetic above. `03-fable.md`, lines 19–24, says the shortened domain is resolved; lines 91–94 identify the new hook-tip variant. These are specification counterexamples, not observations from running a CAD script.

**Concrete fix.** Choose one of two bounded contracts: fully specify each supported branch, or restrict this release to the tail-reference gauge and reject shorter ears/other contact sizes until a later reviewed interface. For every supported branch publish one derived schedule for path domain, body/cavity end and end wall, reference site, lid, hook foot and wire route. Define `TOTAL_LENGTH` and its anatomical measurement meaning. Replace competing hard-coded construction values with parameter references, including the zero-glasses case; define path extension for features at negative s. Check the actual accepted M1 boundary rather than rounding it down. A short-ear option may not silently shrink the reserved contents or omit an end wall. Add generation checks for every advertised reference-site/thickness/preload combination; unsupported combinations must fail before export.

### 17. The lid still overlaps the solid tail, and its tongue is a separate unconnected feature

**Severity:** blocker. **Plan:** §3.5 steps 2–6 and §3.3 assembly checks. **Relationship:** finding 5 remains unresolved, with different concrete geometry from turn 02.

**What is wrong.** The tail is swept with the body's full thickness. Step 5 expressly leaves its lateral face outside the reference pocket and tongue slot solid. The lid plate then occupies the upper 1 mm of that same tail over a substantial length. No tail-wide lid recess or lowering operation removes this overlap.

A literal nominal counterexample for the full body is `P(3, 40, 8.5)`. It is inside the tail, away from the reference pocket and tongue slot, and also inside the specified lid plate. The small outline clearance and edge fillet do not remove an interior overlap. The thin version repeats the same problem at its translated lid height. If the intended operation is to lower the entire covered tail surface to the lid underside, that must be an explicit cut, not an interpretation of “wall tops.”

There is an independent connected-solid failure in the tongue:

| Full-body feature | Specified Y interval |
|---|---|
| Lid plate | 8.0–9.0 mm |
| Tongue, 0.5 thick with its top 0.3 below the underside | 7.2–7.7 mm |

The tongue starts where the plate ends longitudinally, but a 0.3 mm vertical gap separates their solids. No connecting neck or web is specified. Consequently the written lid does not satisfy the one-connected-solid check even after the tail overlap is removed.

**Evidence.** The exact solids and intervals in the pinned §3.5; `03-fable.md`, lines 37–44, claims the replacement closure is resolved and common to the three bodies. These failures occur at nominal geometry, before any print-tolerance discussion.

**Concrete fix.** Give a complete closure section and Boolean sequence: the tail's remaining solid/recess under the lid, ledges and remaining walls, an attached tongue with a dimensioned connecting web, the slot, and the lip engagement. Prove disjoint body/lid interiors in the seated state and one connected solid per printed part for full and thin bodies. Then show the insertion/removal motion and confirm that the same lid geometry works for the two thicknesses. Do not delegate the missing recess or tongue connection to an undocumented CAD-worker choice. This does not require changing closure type if the present one can be made consistent.

### 18. Manufacturing exceptions and unconditional acceptance checks contradict each other

**Severity:** major. **Plan:** §§3.3, 3.5–3.6, §2 row 6, and WP2–WP3. **Relationship:** remaining manufacturing/acceptance portion of finding 5.

**What is wrong.** Section 3.3 requires every wall in the analytic table to be at least 1.0 mm and thickness sampling over the lip/tail to pass that floor. The supplied construction includes a 0.5 mm tongue, 0.8 mm rib and positioning nubs, and a 0.4 mm coupon rib. It does not state which are experimental exceptions or how the checks treat them. Repeating a 1.5 mm main-wall dimension does not reconcile those local features.

The tolerance gate is also contradictory. Section 3.3 requires no lid/body intersection at nominal and at the stated adverse mating tolerances. Section 3.6 explicitly permits 0.2 mm worst-case interference for hand fitting. The arithmetic `0.4 − 0.3 − 0.3 = −0.2 mm` explains the risk, but an allowed interference condition cannot simultaneously pass an unconditional non-interference requirement.

Finally, the claimed lip-test coupon is only specified as a block with holes, slots and a rib. It has no mating cantilever/bump/root geometry reproducing the closure. Such features can measure print dimensions; they do not establish retention or ten-cycle survival of the actual snap. “Nylon screw as fallback” is not a usable fallback without its attachment geometry and parts.

**Evidence.** I reopened [JLC's PA12-HP page](https://jlc3dp.com/help/article/pa12-hp-nylon), dated July 30, 2026: it lists ±0.3 mm below 100 mm and a 1 mm wall. The [JLC design guideline](https://jlc3dp.com/help/article/3d-printing-design-guideline), dated August 24, 2026, §2 recommends more than 1.5 mm for protrusions, locating features, snaps and fasteners; §5 gives 0.2–0.4 mm assembly clearance. These are supplier guidelines, not evidence that a particular thin snap must fail or that JLC has rejected this design. The 1 mm snap and 0.5 mm tongue remain departures needing an explicit experimental disposition. The conflicting acceptance rules are in the pinned plan itself.

**Concrete fix.** State one consistent acceptance policy. Either redesign the necessary features to the chosen rules, or explicitly enumerate experimental exceptions and restrict their release accordingly. Separate nominal CAD clearance, predicted as-printed interference, permitted material removal, minimum remaining thickness, and final assembled acceptance. Retain a fail on unintended nominal overlaps such as finding 17. Specify a representative closure test or use the actual first lid as that test; do not claim a plain slot proves a cantilever. Before weighted wear, require a retained, inspected closure or a fully specified passive fallback. Put the exceptions, measurements and results in the manifest/drawing/checklist so WP2 and Rolf are not asked to enforce incompatible instructions.

### 19. The reference keep-out cannot pass, and its protected lead has no defined route into the main cavity

**Severity:** blocker. **Plan:** §3.3 `KEEPOUT`, §3.5 steps 3–4, §§4–6. **Relationship:** remaining full-stack/lead-path portions of findings 3 and 10, with a new regression in the tail construction. The previous signal-pair sign error is not being reopened.

**What is wrong.** The plan requires all three contact keep-outs to contain only air and applies that design check always. In the passive `MOCK_CONTACTS=true` branch, step 4 only adds domes; it does not cut the tail pocket. The reference keep-out therefore lies in the solid tail of the very gauge being ordered.

The active branch still cannot satisfy the same check: its reference pocket is Ø6.5 mm while the specified keep-out is Ø7.1 mm over y = 1.5–4.0. That leaves 0.3 mm radially of required clearance occupied by nylon. A smaller real nut fitting inside Ø6.5 is not a pass of the separately declared Ø7.1 reservation.

The reference well is also isolated from the main cavity by solid tail material. The cavity ends at s = 38.2; the well is centred at s = 42.5 and no joining channel is constructed. The former reference lead channel is absent. An external Ø2 cable-exit hole at the inferior wall is not a defined well-to-board route. Running a wire across an unspecified lid gap would change both the closure and the isolation/strain-relief contract. Section 6 says the lead route is reserved in §5, but that section contains no dimensioned route connecting this well to the board.

**Evidence.** The gauge/active Boolean branches and pocket/keep-out dimensions in the pinned §§3.3 and 3.5. `03-fable.md`, lines 25–35, says all three full-stack checks are covered and distinguishes the tail pocket; lines 64–68 describe the intended safety reservation. The needed cavity connectivity is still missing from the construction. This is not an allegation that a built device has an electrical fault.

**Concrete fix.** Make keep-out applicability explicit for a purely passive gauge, or cut its dummy clearance features too; either choice must permit the declared default to pass. Reconcile the actual reference pocket with its full hardware, assembly-tool and insulation envelope. Add a dimensioned channel from that pocket to the board, with lead retention/strain relief and clearance from the lid, cell and charging conductors. Include the Kapton thickness and installed lead/terminal envelopes rather than a top-cover disc alone. Check floor preservation, all relevant clearance solids and an uninterrupted insulated route. Changes needed for the hook-tip route belong to finding 16's complete branch, including a check of the 40 mm lead limit. The three separately protected contact paths must exist mechanically as well as in the schematic requirement.

### 20. The active-contact release sequence is circular and does not distinguish validation wear from accepted use

**Severity:** major. **Plan:** §3.7, §§6–7, and WP5–WP8. **Relationship:** remaining gate/dependency portions of findings 7 and 14; the pressure-target relabelling itself is not reopened.

**What is wrong.** WP7 includes actual-contact performance and three-day re-donning, while WP8 permits Stage B wear only after that WP7 gate has passed. The metal contacts are procured with order 2, and the first ordered gauge has printed mock domes, not the specified assembled contact interface. No separate dry-contact fixture or explicit permission for controlled validation wear is specified. Read literally, the data required to authorize wear cannot be collected without first doing the wear that is prohibited.

WP7 also mixes a pre-order output (gel-derived coordinates and written pass criteria) with post-assembly observations (the real stack's dry signal and repeated donning). Its deliverables list baseline, SNR and jaw-motion dropout, but the release logic does not explicitly preserve the design record's false-positive measurements during eating, talking and walking. Recording intended tests is not yet an unambiguous pass/fail or release contract.

**Evidence.** WP7 and WP8's own acceptance sentences, order 2's placement after coordinates/packing, and §6's separate schematic/inspection/leakage prerequisites. `docs/EARPIECE_DESIGN.md`, “Stage B” exit criteria and “Harness mapping and false-positive budget,” requires fixed-threshold re-donning and background-activity measurements. `03-fable.md`, lines 51–56, expressly says the active gate precedes Stage B wear. No physical test result is being demanded during this planning turn.

**Concrete fix.** Split the sequence explicitly. Before ordering production-intent parts, require the verified contact specification from WP5, accepted packing/interface, gel-montage coordinates, affected passive-fit checks, and a frozen dry-test protocol. After parts arrive and assembly/bench safety checks pass, allow only the controlled validation wear needed to execute that protocol. Release routine use and any promotion of decoder/action mappings only after the dry-contact criteria pass, including three-day fixed-threshold re-donning and specified background activities. Define failure/rework and revalidation transitions, with changed contacts/coordinates invalidating the appropriate previous observations. Exact numerical signal thresholds can be a named WP7 deliverable, frozen before validation data are collected; they must not be an undefined permission for use or be chosen after seeing the result. Repairing this dependency graph is required now; executing the experiments remains later work.

## For Rolf

Do not order from this revision yet. The remaining blockers are in the instructions themselves: the shorter-ear option is not fully constructed, the lid occupies solid tail material and has an unattached tongue, and the reference contact's clearance and wire route are inconsistent. The manufacturing checks and active-wear release sequence also need one clear, executable interpretation.

The next revision does not need a finished PCB, a supplier inquiry, or three days of test data. It needs a consistent gauge and staged release rules. Keeping the first order explicitly provisional is reasonable; completing the shorter-ear option is optional if unsupported measurements are rejected honestly. The replacement titanium hardware must still pass WP5 before any active-contact order.

Only this review file was written. No design file, brief, lane report or prior turn was changed; no purchase, vendor contact, quote request or design upload was made. These five findings are substantive, not a request for another cosmetic pass.

NOT SIGNED OFF
