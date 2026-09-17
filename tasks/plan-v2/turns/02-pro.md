# Turn 02 — pro (plan v2)

Reviewed on **2026-09-17**: the working-tree draft `docs/fab/plan-v2.md`, turn 01, 271 lines. No commit was specified for this review; I did not substitute a claim of commit-pinned provenance. Read `tasks/plan-v2/turns/01-fable.md`; `docs/fab/open-questions.md`, particularly Round 5 Q28–Q36; `.worktrees/w5/docs/fab/L5-research-v2.md`; and the standing v1 specification, including §§3.3, 4, 5 and 6. Also read `docs/fab/montage.md` and `docs/fab/packing-options.md` because the draft relies on their unchanged protocol and packing result.

This is a new v2 dialogue, so findings start at 1. The earlier sign-off covered a provisional-gauge-first workflow, not this replacement architecture. Removing that experiment, changing the electrical interface, and introducing USB charging require reviewing the new contracts. This review does not withdraw resolved v1 findings merely because the project changed.

**Verdict: NOT SIGNED OFF. Fifteen findings: five blockers and ten majors.** The strongest direct contradictions are the proposed charger/cell pairing, the acquisition protocol, the assembler tier used for costing, and the claimed charging interlock. Several other claims are only partly verified, not established facts. The C1–C10 ledger and order-price audit below distinguish those cases.

Public pages and relevant PDF page images were inspected. No CAD build, schematic simulation, physical fit test, electrical safety test, supplier inquiry, quote request, purchase or design upload was performed. All external-source access dates below are **2026-09-17**; a publication/revision date is separately stated where available.

## Findings

### 1. Disabling acquisition does not disconnect the worn electrodes from USB

**Severity: blocker. Sections:** §2 R7, §6, §10 S2/S4, D-5.

**Sentence to change:** “No charging while worn, by a physical interlock or by a firmware interlock plus a covered port, decided in D-5.”

**Failure and evidence.** A cap can be opened while the device is worn. Refusing to stream or powering down the front end does not establish electrical isolation of SIG1, SIG2 and the driven reference from USB-connected circuitry. Seeed's [XIAO schematic, revision dated 2026-08-28, PDF page 3](https://files.seeedstudio.com/wiki/XIAO-BLE/Res/260828_XIAO_nRF52840.pdf) shows USB, charger and board ground in the same circuit; it does not provide an isolated patient interface. Firmware cannot remove those copper connections. The exact body-current paths still depend on the custom schematic, including protection and RLD in powered, unpowered, reset and fault states.

D-5(b), opening the lid, is not inherently an interlock either: it becomes one only if the mechanical arrangement actually prevents the worn configuration or disconnects the electrode assembly. V1 described off-ear charging as procedural rather than claiming isolation. The new gel-electrode bench is also an on-body connection; its safety prerequisites must precede the first montage recording, not appear in the same unordered S2 list after it.

**Required replacement:** “Worn acquisition and gel-montage acquisition are battery-powered with external power/data cables disconnected. VBUS detection is a secondary inhibit, not isolation. Before architecture selection, specify either a physical removal/disconnection arrangement that prevents a USB-connected worn configuration, or a separately reviewed isolation design; a cap and firmware shutdown alone do not satisfy R7.”

Define the mechanism, all three contact paths, assembly states and failure checks. Put inspection, current-limiting/protection verification and off-body electrical checks before any skin connection. This is not a request to certify a medical device; it is a request not to substitute a software condition for an electrical boundary.

### 2. The documented DTP301120 limit excludes the stock XIAO charging settings

**Severity: blocker. Sections:** §1 item 4, §4 charger row, D-2/D-4.

**Sentence to change:** “Reading before WP11 runs: C if it closes and the cell's sheet allows 50 mA; else B with the programming service; else A.”

**Failure and evidence.** C3 is no longer an unanswered 50 mA question. The [DTP301120 specification cited by the draft, version 1.0, PDF page 4](https://cdn.sparkfun.com/datasheets/Prototyping/SPE-00-301120-40mah-en-1.0ver.pdf) gives a maximum continuous charge current of **40 mA**. The [Seeed wiki](https://wiki.seeedstudio.com/XIAO_BLE/) documents approximately 50 or 100 mA, controlled by **P0.13**, not L5's P0.17. Those settings are respectively **1.25 and 2.5 times** the documented maximum. The connector-revision uncertainty in finding 10 does not authorize assuming a higher current.

**Required replacement:** “DTP301120 is not paired with the stock XIAO charging circuit on the available evidence. A candidate passes only with a named protected pack and a charger whose worst-case current, voltage, temperature conditions and reset behavior meet that pack's specification.”

A different qualified cell or a factory-implemented charging redesign may reopen C. Neither can be treated as a software setting below 50 mA that the published XIAO design does not provide. The 501015 fallback also needs an exact pack specification; its nominal capacity is not a charge-current qualification.

### 3. The nut-clamped flex interface is not yet a screwdriver-only assembly

**Severity: blocker. Sections:** §5 construction, §8 steps 2–4, D-3.

**Sentence to change:** “Inside, drop a brass nut over each screw tip through the ring pad; tighten with the small screwdriver from outside until snug.”

**Failure and evidence.** No feature captures the nut against rotation, holds the ring pad in alignment, or prevents the flex from turning with the nut. The standing circular reference pocket is not a hexagonal nut trap. A nut that needs an internal wrench violates R2. “Snug” also leaves the clamp load on the thin flex undefined. A successful metal-to-metal lug joint from v1 does not validate loading copper, coverlay and a stiffener in its place.

The necessary dimensions are missing: contact-pad annulus and exposed face, hole tolerance, stiffener extent, reaction surface, anti-rotation feature, trace exit, minimum bend radius, strain relief, installed and insertion envelopes, and allowable tightening method. These are omissions in `plan-v2.md` lines 128–133 and 180–184, not observed failures of a manufactured flex.

**Required replacement:** “Each contact joint uses a dimensioned captive anti-rotation nut and supported contact pad, assembled with the specified 1.5 mm hex driver without another tool. The joint drawing defines the tightening limit, support and insulation stack, trace strain relief and inspection criteria; the completed joint must retain electrical continuity under the prescribed mechanical checks.”

Show how all three joints are reached and assembled without twisting the board or loading the battery. Recalculate screw-tip intrusion: a 4 mm under-head screw through a 1.5 mm wall still projects **2.5 mm** inside. Deleting a lug does not shorten that screw. Flex tabs remain a candidate, not the only possible no-solder-by-Rolf architecture and not an already-qualified joint.

### 4. The finish and material acceptance chain is incomplete

**Severity: major. Sections:** R3, §5 finish, §7 finish, D-3/D-8.

**Sentences to change:** “Finish: immersion tin or OSP if the flex process offers it, ENIG otherwise; nickel inside the sealed cavity is on v1 §4's internal-metal list, never skin-side.” Also: “Skin-side materials as v1 §6: titanium domes, PA12 with a skin-contact certificate for the finish actually ordered, no resin.”

**Failure and evidence.** OSP is not a tinned metallic contact finish. The original technical disclosure [US8961678B2, description](https://patents.google.com/patent/US8961678B2/en) describes a non-metallic solderability-preserving treatment of copper. That does not establish a durable screw-clamped contact through the coating. Tin and ENIG likewise require a defined joint qualification; naming an available board finish is not the same as qualifying that electrical interface.

Internal nickel is not automatically prohibited by the titanium-skin-contact requirement. However, the draft has not defined a sealed cavity: it retains a seam, electrode penetrations and potentially an external port. It needs an actual containment/insulation design, not the adjective “sealed.” Do not equate electrical connection through a titanium screw with proof of nickel exposure, either; the relevant exposure path must be evaluated rather than assumed.

C1 verifies generic JLC biocompatibility marketing, not a certificate for this finish. C8 distinguishes SLS skin-irritation evidence from MJF cytotoxicity evidence. C9 verifies a titanium grade claim, not ISO 7380 conformity or the assumed head drawing. R3 is stronger than v1's explicitly unverified finished-part status.

**Required replacement:** “Select one qualified terminal finish and document its pressure-contact acceptance. Identify every potentially exposed material and its containment. The exact printed material/finish and titanium SKU must satisfy the stated documentary requirements before release; generic material claims and a negative nickel screen do not replace them.”

Either obtain the finished-process evidence R3 requires through an owner-authorized route, or explicitly return a proposed requirement change to Rolf. Do not silently treat the current JLC default as satisfying the certificate requirement.

### 5. Section 3 does not prove that thin is impossible, or that full fits

**Severity: major. Sections:** §0, §3, WP11, D-1.

**Sentence to change:** “So a thin body cannot hold a radio and a battery. The full body can, and may come down to about 8.5 if WP11 finds the stack has slack.”

**Failure and evidence.** The four scalar calculations exclude selected stacking and width arrangements, not every arrangement. They do not eliminate a tandem arrangement or a revised length/contact layout. WP11 only searches heights **8.0–9.0**, so its result cannot establish that 7.0 is impossible. Conversely, summing heights below 6.5 does not establish a three-dimensional fit with the antenna exclusion, front end, receptacle, tabs, supports and actual harness.

The addition itself is mostly correct; the conclusions and inputs are not:

| Check | Result and consequence |
|---|---|
| Module/cell expression as written | 0.4 + 2.0 + 3.2 + 0.3 = 5.9 mm, correctly added, but not a complete maximum stack |
| Standing Raytac reservation | V1 §5 reserves 2.3 mm maximum module height, not the 2.0 used here; substituting it gives 6.2 mm before other omitted allowances |
| Cell/contact expression | 2.63 + 0.2 + 3.2 + 0.3 = 6.33 mm, rounded to 6.3; reconcile whether the new tab is already inside the old stack before using it |
| An 8.5 mm shell retaining the stated floor/lid | 8.5 − 1.5 − 1.0 = 6.0 mm cavity: neither 6.2 nor 6.33 fits that particular stack |
| Width 20 with standing 1.5 mm sidewalls | 20 − 2 × 1.5 = 17.0 mm, not the stated 17.6 |

**Required replacement:** “The listed overlapping layouts exceed the thin cavity using these provisional inputs. Thin feasibility remains unproved; WP11 compares supported tandem and stacked layouts using complete maximum assembly envelopes, including the requested thin case or a documented reason it cannot be tested. Only a passing layout supports a proposed thickness.”

Keep Rolf's thin request active until that comparison. A result may justify asking him to accept thicker, longer or wider; it must not be described as a universal physical impossibility established by these four sums.

### 6. The selected manufacturing route cannot be budgeted as Economic rigid-board assembly

**Severity: blocker. Sections:** §4 stock/rule, §5 construction, §9 board order, C2/C5/C7.

**Sentence to change:** “JLCPCB economic PCBA: setup $8.18, stencil $1.53, extended feeders ~$3 each, parts ~$20–35 per board, boards ~$5, shipping ~$20–25.”

**Failure and evidence.** The design being priced is a thin flex assembly with stiffeners, not the rigid-board promotion used in that sentence. The verified E73 listing itself is **Standard Only**, independently invalidating the Economic assumption for B. JLC's published FPC assembly route has fixture costs; the public capability limits also require a handling panel/rails for a board this small. See C2, C5, C7 and the price audit for exact pages and amounts.

The rigid-plus-flex fallback is another manufacturing assembly, not evidence that the original low quote remains applicable. Its factory interconnect work and handling must be accepted and costed too.

**Required replacement:** “The architecture is costed only in a service tier that explicitly accepts its substrate, thickness, panel, component set, assembly sides and interconnect work. Standard/FPC costs are the baseline where required; the rigid-plus-flex fallback gets a separate acceptance and price calculation.”

Do not freeze the PCB or authorize a spend against R8 until that route is selected. A component appearing in a distributor catalog is not proof that Economic PCBA can place it.

### 7. The architecture rule omits hard gates and its preliminary winner is unsupported

**Severity: major. Sections:** §4, D-2.

**Sentence to change:** “Reading before WP11 runs: C if it closes and the cell's sheet allows 50 mA; else B with the programming service; else A.”

**Failure and evidence.** The necessary gating set is larger than geometry and parts availability. Charging compatibility, the electrode/USB boundary, actual assembler acceptance, factory programming, the electrical operating point, the terminal joint and the cost ceiling can each disqualify a candidate. C3 already defeats the proposed C/cell combination; C5 does not verify on-hand assembler stock; C6 does not verify an nRF52840 SWD programming job or its price; C7 does not quote this flex assembly. Falling through to A does not make its missing evidence pass.

The rule also does not implement “smallest”: after maximum bounds it minimizes Rolf's steps, then price. That can be a sensible objective, but it is not the same as minimizing thickness. The table's “RF risk: none” is not an integration result for an antenna next to a cell, skin and the new shell. `packing-options.md` proves only its enumerated old-component layout, not the new one.

**Required replacement:** “First reject any candidate failing a listed safety, cell, manufacturing, programming, functional, geometry or budget gate. Among the survivors apply an explicit owner-approved objective order, including thickness where intended. If none passes, report no eligible architecture; do not choose by fallback.”

Report measured geometry separately from sourced constraints and unresolved facts. Consignment, programming, panel removal, firmware recovery and all user tools count as real burdens, not just the eight final assembly lines.

### 8. The 500 SPS design cannot execute the unchanged frozen protocol

**Severity: blocker. Sections:** §5 front end, §6, S2/S4, D-6.

**Sentence to change:** “§3 of that file (frozen protocol, accepted Q28) is unchanged.”

**Failure and evidence.** `montage.md` lines 212/225 require noise in **20–490 Hz**; lines 215 and 264–278 require an **INA128 output** displacement measurement. V2 replaces that analog chain with ADS1292 at 500 SPS. Its Nyquist frequency is 250 Hz, and the INA128 node does not exist.

The [TI ADS129x datasheet, Rev. C, Table 4, printed page 16](https://www.ti.com/lit/ds/symlink/ads1292.pdf) also gives a 131 Hz −3 dB bandwidth for the relevant 500 SPS setting. Thus this is not merely a change in sample count while preserving the same measurement. Old amplitude/noise criteria cannot silently be declared equivalent across the new transfer function.

**Required replacement:** “Before release, publish a versioned ADS1292-specific acquisition and test contract: sample rate, analog/digital bandwidth, gain/reference, input-referred units, saturation/offset criterion and equivalent measurement nodes. Reconcile each frozen criterion explicitly before collecting dry data.”

Streaming-only firmware remains an appropriate boundary. Specify signed sample encoding, scale, actual rate, timing/sequence and loss reporting so the laptop receives interpretable raw data. Choose the required measurement band first; selecting a supported higher rate may be part of the solution, but is not by itself proof of an unchanged end-to-end response.

### 9. The power and electrode-return schematic contract remains ambiguous

**Severity: major. Sections:** §5 front end, standing v1 §6, WP12.

**Sentence to change:** “Front end: ADS1292 per L4 and v1 §5; SIG1, SIG2 to one differential channel at gain 12, 500 SPS; the reference contact to the bias (RLD) output; input protection per the ADS1292 datasheet's reference schematic; the 2.5 V/3.3 V rails from the module's regulator or a TLV713.”

**Failure and evidence.** A list of two voltages does not assign them to supplies or demonstrate operation over the battery range. TI's [electrical characteristics, Rev. C, printed page 9](https://www.ti.com/lit/ds/symlink/ads1292.pdf) require at least **2.7 V across AVDD–AVSS**. The sentence does not prove that AVDD is wrongly connected to 2.5 V, but it leaves that consequential choice unresolved.

The driven reference is an output path to the body, not an inert third input. The standing requirement for a separately current-limited/protected path on every lead must expressly include it. “Per a reference schematic” must not silently replace v1's 220 kΩ-per-contact requirement or omit pre-resistor insulation. Reset, power-off, lead-off/test modes, RLD stability, electrode offsets and rail headroom need a named review, not an assumption that use of the IC qualifies the assembled circuit.

**Required replacement:** “WP12 assigns every rail and electrode path, retains the three independently limited/protected contact paths, and documents operating and fault states, input/offset headroom, bias configuration and off-body acceptance tests before first skin use.”

Finishing that schematic is WP12's job. Defining the valid supply and safety contract is part of this plan.

### 10. The cell harness is not yet a verified plug-in part of the envelope

**Severity: major. Sections:** §1 cell, §3, §5 connectors, §8 steps 1/5, C3/C4.

**Sentence to change:** “Cell: Data Power DTP301120, 40 mAh, 3.2 × 11.5 × 22 mm with its protection circuit, JST-SH leads (SparkFun PRT-25270), if its drawing allows the charger's current (claim C3); else v1's 501015.”

**Failure and evidence.** The [SparkFun PRT-25270 page](https://www.sparkfun.com/polymer-lithium-ion-battery-40mah-jst-sh.html) calls the connector JST-SH, while the linked legacy pack drawing, PDF page 9, calls it **JST-PHR-2PIN** and specifies **100 ±3 mm leads**. The product text additionally describes 2 mm spacing under its SH description. That is not a reliable, reconciled mating-part specification for a one-spin PCB.

The packaging sums reserve the pouch, not its connector, stored lead length or routing. The XIAO route also needs a defined factory connection to its battery pads; a carrier's JST connector does not connect those pads by assertion. None of this authorizes Rolf to cut, strip, solder or reterminate anything.

**Required replacement:** “Use one exact protected-pack/harness revision with a mating connector part number, contact numbering, polarity, lead length, maximum assembly envelope and shipping eligibility verified before PCB release. All pad-to-carrier connections and harness customization are factory work.”

Treat the SH/PH discrepancy as unresolved documentation, not proof that a received battery is reverse-polarized. Require polarity verification before plugging in, and reserve the complete delivered harness in WP11.

### 11. Factory programming and post-arrival firmware development conflict

**Severity: major. Sections:** §4 first load, §6 title, §8 step 8, WP13 sequencing, C6.

**Sentences to change:** “Firmware (WP13, after the board arrives)” and “Copy the firmware file to the drive that appears (C), or nothing (A/B, already programmed).”

**Failure and evidence.** The manufacturer says the E73 is delivered unprogrammed; see C5. C6 establishes only a conditional programming service, not acceptance of this target, fixture, image, verification procedure or price. Firmware developed after arrival cannot be the image programmed before shipment. For C, a preinstalled bootloader is not Elicio firmware; recovery entry and the required reset access must remain available after assembly.

**Required replacement:** “Before the board order, freeze the programming/recovery route and provide the factory image or bootloader, programming contacts, verification procedure and acceptance record. Firmware development and hardware validation may continue after arrival, but no required first-load operation is omitted from Rolf's tool/step budget.”

A qualified factory bootstrap plus later USB update can satisfy the intent. An unspecified pogo clip and a nominal $6 probe cannot. The board test should include power-up, programming/readback as appropriate, sensor communication and a recorded functional result, with its actual cost identified.

### 12. Ordering a custom flex before finding contact sites can lock in the wrong geometry

**Severity: major. Sections:** §5 construction, §6 montage, S1–S3, D-7.

**Sentence to change:** “S3 shell ordered | S2 sites in interface v3; WP14 re-run on them; renders re-approved only if the shape changed; Rolf places order 2.”

**Failure and evidence.** S1 purchases the flex with three finished contact tabs. S2 then discovers where those contacts should be. Moving holes in the shell does not make already-fabricated tabs reach new sites with an acceptable bend, joint orientation and strain relief. Q26 previously required rerunning placement after site changes; removing wires has not removed that dependency.

No allowable tab-reach workspace, slack storage or accessible montage adapter is specified. Clipping gel electrodes to bare flex is also not a complete supplied bench harness. Buying board first is preferable to buying both blindly, but it does not by itself de-risk a site-specific flex.

**Required replacement:** “Before S1, prove the purchased board/tab assembly accommodates a defined contact-position workspace, or obtain the required site information before freezing it. S2 may select positions only within that demonstrated workspace; anything outside it is a failed interface requiring a stop, not a shell-only update.”

Include the preassembled gel-electrode adapters and clips in the first purchase and specify an off-body support for the board. Do not authorize the simultaneous-shell option in D-7 under a rule forbidding reprints unless Rolf explicitly accepts that additional risk.

### 13. The first-try release gate can currently pass without its required checks

**Severity: major. Sections:** R1/R6, §5 CI, S0.

**Sentences to change:** “Works first try: every electrical function follows a manufacturer reference design or lives inside a proven module…” and “tests/ gains a board test that skips when kicad-cli is absent and fails on any DRC error when present.”

**Failure and evidence.** A skipped release check is not a passing ERC/DRC result. Reference designs and geometric checks reduce certain risks; they do not establish solder quality, component correctness, analog noise, antenna performance against the head, clamp continuity, dry-electrode stability or three-dimensional comfort. L5 itself, lines 151–153, says the paper profile cannot check skull clearance, contact pressure or pinching.

The budget constraint is real. It calls for a no-hidden-iteration plan and an explicit stop on failure, not a guarantee that these tests cannot establish. A first custom biological-sensor assembly still needs controlled validation; removing a gauge does not remove that uncertainty.

**Required replacement:** “First-pass success is the objective, not an established result. Ordering requires non-skipped, versioned evidence for every mandatory check and documented acceptance of the remaining first-assembly risks. If validation fails, routine use is withheld and no further expenditure occurs without Rolf's approval.”

Keep local developer skips if useful, but the release job must install the pinned tools and fail closed. Add factory inspection/functional acceptance and post-arrival safe validation responsibilities, without quietly adding an unpriced second hardware round.

### 14. The new appearance and closure cannot inherit the gauge's experimental pass

**Severity: major. Sections:** §7, standing v1 §3.6, WP14/S0.

**Sentence to change:** “Parting: the lid becomes the whole lateral shell; the seam runs along the perimeter at mid-height as a 0.4 mm feature groove, tongue and lip inside it (v1 §3.6 closure without E1, Q25).”

**Failure and evidence.** E1 is the old tongue/web geometry, yet the new sentence drops E1 and still calls for a tongue without defining its replacement. Q25 records interference with the reference pocket; Q28 accepts dropping E1. Moving the seam and changing the hook section also change the joint, cavity and stiffness assumptions. The old snap was expressly experimental and depended on a printed closure test; that gauge no longer exists.

Aesthetic constraints are useful direction, but G2 “where possible,” a taper without dimensions and “largest fillet that builds” do not by themselves define a repeatable new shell. Nor does an externally measured 0.4 mm groove specify its fit stack or retention.

**Required replacement:** “WP14 produces a new dimensioned closure and hook contract, with the dropped E1 explicitly replaced or absent, full cavity/contact clearances, tolerance and assembly-motion checks, and a safe first-assembly retention test. No old gauge pass is inherited.”

Keep the single-order goal: do the new CAD and interface review before purchase, then test the actual delivered closure before powered wear. Any necessary final adjustment must fit R2; sanding or reworking parts cannot be concealed inside ‘snap the lid on.’

### 15. The three-order total is not a page-priced delivered budget

**Severity: major. Sections:** §0, §1 budget, §9, D-8.

**Sentences to change:** “Total $185–285 at page prices, before Rolf's country's duties.” Also: “No vendor does that.”

**Failure and evidence.** The order audit below can substantiate selected catalog prices and assembly fee components, not these complete configured orders. Board substrate/process, fixtures, programming, functional testing, panel removal and the complete BOM remain unsettled. Shell geometry/finish prices require a configured quote. The small-parts estimate spans several shops, omits the montage harness, and includes a kit whose page says unavailable. A supplier's home country does not establish the fabrication origin or its ability to ship the selected battery to Rolf.

The summary's $200–260 also disagrees with §9's $185–285. That numerical edit alone is minor; the uncosted qualifying manufacturing route is not. Economic assembly is already assumed in the estimate, so recommending it as a later saving is not a real contingency. The universal turnkey-assembly assertion is unverified; the correct statement is that no accepted and priced turnkey route has been established here.

**Required replacement:** “These are dated planning allowances, not a verified delivered total. Before release, calculate each eligible architecture from its actual manufacturing tier, quantities, BOM, required services, every shipment, taxes/duties and bench accessories. Give one like-for-like non-China route or label it quote-only; do not invent a multiplier.”

No agent is authorized to request those quotes in this turn. Quote-dependent costs remain explicit gates for a later owner-authorized step. Until Rolf's ceiling and delivery destination are fixed, R8 is unresolved rather than passed.

## C1–C10: independent live-source ledger

All quotations below are short excerpts from the linked sources, accessed **2026-09-17**. A source saying something is distinguished from evidence qualifying this particular assembled device. No live stock result is a reservation.

| Claim | Result, quotation, URL and scope |
|---|---|
| **C1 — JLC PA12/PA12S skin/ISO statement** | **Partly verified.** [JLC MJF article](https://jlc3dp.com/blog/mjf), updated 2026-02-24, contains “Certified for skin contact and medical device use” and “ISO 10993 Biocompatibility, sterilizable.” These are generic material statements. I did not obtain a certificate or test report tying the ordered JLC process, dye or smoothing finish to this shell. The lane's claimed material-page wording is not substituted for the actual page found. |
| **C2 — Economic fees and minimum two** | **Fees/minimum verified, applicability not.** [JLC price schedule](https://jlcpcb.com/help/article/pcb-assembly-price), updated 2026-09-08, lists Economic setup $8.18, stencil $1.53 and extended feeder $3.07. [Assembly capabilities](https://jlcpcb.com/capabilities/pcb-assembly-capabilities) lists a two-piece assembly minimum. Those facts do not qualify the proposed flex for Economic service. Applicable fee components are in the order audit. |
| **C3 — DTP301120 versus 50 mA** | **Contradicts the proposed pairing on the cited specification.** [Data Power PDF](https://cdn.sparkfun.com/datasheets/Prototyping/SPE-00-301120-40mah-en-1.0ver.pdf), version 1.0 dated 2015-11-06, page 4: “Maximum Continuous Charge Current” / “1C (40mA).” Page 9 gives the protected-pack maxima 3.2 × 11.5 × 22 mm. The linked drawing is legacy PH-harness evidence, not confirmation of the current SH harness revision. |
| **C4 — XIAO height and charging** | **Charging verified; quoted maximum assembled height unverified.** [Seeed wiki](https://wiki.seeedstudio.com/XIAO_BLE/): “The battery charging current can be set to approximately 50 mA or 100 mA using P0.13.” High-impedance/low states select those modes. L5's P0.17 is not the documented control. I did not authenticate a toleranced drawing establishing 4.3–4.5 mm as the installed maximum height. Use the selected revision's mechanical model/drawing, not that range as a proven envelope. |
| **C5 — E73 assembler stock and antenna** | **Identity/classification verified; quantitative stock, price and exact antenna exclusion not verified.** [JLC exact E73 listing](https://jlcpcb.com/partdetail/Chengdu_Ebyte_ElecTech-E732G4M08S1C/C356849) identifies **C356849**, “Extended,” “Standard Only,” and “X-ray Inspection Required.” That is not L5's C474779. The retrieved catalog did not supply a reliable current on-hand count or unit price. [Ebyte's product page](https://www.cdebyte.com/products/E73-2G4M08S1C) says “The module is not programmed.” The detailed manual/download attempts did not yield an inspectable antenna-clearance drawing; no keep-out approval is claimed. |
| **C6 — factory nRF52840 SWD programming** | **Generic possibility verified; this job and price remain unverified.** [JLC assembly capabilities](https://jlcpcb.com/capabilities/pcb-assembly-capabilities) says “we partially support this programming service.” It does not establish acceptance of this nRF52840, its SWD fixture, desired image, verification or fee. No substitute assembler's job-specific service/price was authenticated. |
| **C7 — small stiffened flex assembly** | **General service verified; exact job/minimum handling configuration and total unquoted.** [JLC capabilities](https://jlcpcb.com/capabilities/pcb-assembly-capabilities): “JLCPCB provides assembly services for FPCs.” Its published Standard handling minimum requires panel/rail treatment for the proposed small board. [Price schedule](https://jlcpcb.com/help/article/pcb-assembly-price) separately lists “Fixture (Flexible PCB).” The two-piece assembly minimum is not proof that two unpanelized 40 × 20 mm flexes with arbitrary stiffeners are accepted. |
| **C8 — vapour-smoothed PA12 evidence** | **Qualified evidence exists; L5 merges different tests.** [Xometry vapour-smoothing page](https://www.xometry.com/capabilities/vapor-smoothing/) lists “Skin Irritation Test” with “PASS” for SLS PA12, while its MJF PA12 entry is cytotoxicity. The linked [AMT health/safety report, July 2020, page 2](https://prismic-io.s3.amazonaws.com/xometry-marketing/b411cca2-b468-4f6b-887d-5303075647e4_AMT_Health_Safety_Certifications.pdf) was inspected as a page image. It does not justify saying the same MJF sample passed every SLS skin test. No equivalent JLC finished-process report was established. This is evidence for evaluating a route, not certification of the proposed purchased shell. |
| **C9 — titanium screw and brass nut** | **Screw price/material partly verified; exact conformity and nut price unresolved.** [Sortafast M2.5 page](https://sortafast.com/products/sortafast-titanium-screws-button-head-10pk-m2-5) lists the 4 mm variant and $17.50/10, “Machined from Grade 5 6Al-4V titanium,” “Natural titanium finish (uncoated),” and a “unique tapered button head.” I did not find an ISO 7380 conformity statement or the required head drawing/lot certificate there. The page exposes both sold-out wording and cart controls, so available quantity is not authenticated. The supplied [TME BN 147 / 1159550 URL](https://www.tme.eu/en/details/b2.5_bn147/hex-nuts/bossard/1159550/) could not be retrieved; its $1.60/10 and stock remain UNVERIFIED, not disproved. |
| **C10 — non-R ADS1292 at LCSC/DigiKey today** | **Not established.** The searches did not produce a reliably readable current LCSC or DigiKey stock/price record for the exact non-R ordering code. L5's overlapping R/non-R IDs must not be accepted as verification. [TI's exact ADS1292IRSMT page](https://www.ti.com/product/ADS1292/part-details/ADS1292IRSMT) confirms the non-R part, but displays “Out of stock” alongside “Log in to view inventory.” That is limited public TI information, not proof of stock at either requested distributor or a claim of worldwide unavailability. C10 remains a pre-release sourcing gate. |

## Pricing the three orders from the evidence available

**These are public fee/catalog observations, not quotes, purchases or a complete bill.** Amounts are USD unless marked otherwise. The draft's three orders are procurement categories: the small-parts category alone involves several potential shipments.

### Order 1 — assembled board

The [JLC schedule](https://jlcpcb.com/help/article/pcb-assembly-price), accessed 2026-09-17, supplies these relevant components:

| Published fee component | One-sided Standard | Two-sided Standard |
|---|---:|---:|
| Setup | $25.56 | $51.12 |
| Stencil | $8.21 | $16.42 |
| Flexible-PCB fixture, 1–29 pieces; listed two-fixture total | $49.25 | $49.25 |
| **Arithmetic subtotal of those components only** | **$83.02** | **$116.79** |

These are not delivered-order lower bounds for every possible contract or promotion; they are the applicable published components of the route being considered. Standard feeder loading is listed separately at $1.53 per feeder. The final calculation still needs substrate/stiffeners, exact population quantities, BOM, placement, required X-ray, any programming/testing, factory interconnect work, depaneling, packing, freight and import/tax amounts. Do not blanket-add conditional handling fees or price thin flex as the $5 rigid-board promotion. The **$90–140 total is not substantiated** for the proposed configured assembly.

**Non-China comparator:** [AISLER's assembly page](https://aisler.net/en-US/products/assembly) and [published pricing explanation](https://community.aisler.net/t/our-simple-pricing/102), accessed 2026-09-17, make assembly depend on the board, components and assembly tasks; exact configuration is quote-dependent. [MacroFab](https://www.macrofab.com/) also requires the actual design/BOM for pricing. Neither source supports a like-for-like **2–4×** multiplier for this board. Required flex/interconnect acceptance and actual manufacturing location remain to be confirmed. Keep one qualified alternative in the comparison, not a list of names presented as priced options.

### Order 2 — body, lid and spare lid

[JLC's PA12-HP page](https://jlc3dp.com/help/article/pa12-hp-nylon), accessed 2026-09-17, says “Price: From $1.00” and “Build time: 72 hours.” That is a generic starting price/build time, not a price for three finished parts or a delivered schedule. The actual geometry, finishing needed to satisfy R3, destination and shipping determine this order. **$40–70 remains an allowance.**

**Non-China comparator:** Xometry's vapour-smoothing page in C8 provides useful process evidence but no configured price for this shell. **Exact part price: quote-only/not verified.** Factory origin and the exact material/finish test scope must be part of that comparison. An aggregator or US office address alone is not a non-China manufacturing guarantee.

### Order 3 — small parts and bench accessories

| Item | Public evidence on 2026-09-17 | Cost treatment |
|---|---|---:|
| Sortafast M2.5 × 4 titanium screws, ten | C9; material/geometry and availability qualifications remain | $17.50 displayed |
| SparkFun PRT-25270 40 mAh pack | [Product page](https://www.sparkfun.com/polymer-lithium-ion-battery-40mah-jst-sh.html) shows in stock; harness qualification still open | $7.39 displayed |
| Nickel Alert, SKU 1012-A | [Supplier page](https://nonickel.com/products/nickel-alert-nickel-test-kit) displays “$24.99 USD” and “Unavailable”; shipping at checkout | $24.99 displayed, not an available purchase route |
| **Sum of the three displayed prices** | Not an orderable qualified cart | **$49.88** |
| Brass nuts | TME page not retrieved | $1.60 draft allowance, UNVERIFIED |
| Precut foam/adhesive support, insulation, any contact supports/captive hardware | No exact qualified BOM | Unpriced |
| Gel electrodes and factory-made montage adapters/clips | Required by S2, absent from the small-parts row | Unpriced |
| Required cable, specified driver, programming fixture/service if not factory supplied | Architecture-dependent; not assumed owned | Unpriced |
| Every shipment, applicable tax/import collection | Destination and supplier-dependent | Unpriced |

The [SparkFun page](https://www.sparkfun.com/polymer-lithium-ion-battery-40mah-jst-sh.html) restricts this battery's international/express and certain US shipping routes. The [Nickel Alert page](https://nonickel.com/products/nickel-alert-nickel-test-kit) requires surface-mail handling. Those restrictions affect the delivery plan as well as price. Adding the draft's unverified nut allowance to the displayed subtotal would be $51.48 before the remaining items, not proof that the whole order fits $55–75.

**Combined delivered total: NOT VERIFIED.** An honest review cannot turn absent geometry quotes, unresolved assembler services and unavailable items into a page-priced $185–285 total. Retain a clearly labelled planning range only after recalculating the eligible architecture, and use a complete delivered checkout/quote gate before spending.

## D-1 to D-8: disposition

| Decision | Review disposition |
|---|---|
| **D-1 thickness** | Return for the bounded layout comparison. “Thin is impossible” is not proved; 8.5–9.0 is not yet a demonstrated passing result. Rolf decides the thickness/length/width tradeoff after that evidence. |
| **D-2 architecture rule** | Revise to hard eligibility gates followed by an explicit objective order. No provisional C/B/A winner is justified yet. |
| **D-3 flex tabs** | Plausible research/design candidate, not accepted as the final joint. Needs supported captive mechanics, qualified contact finish, insulation, insertion/reach proof and assembler acceptance. |
| **D-4 cell** | DTP301120's cited 40 mA maximum rules out stock XIAO charging. A different charging circuit or fully qualified alternative pack is needed; do not default to an unnamed 501015 pack. |
| **D-5 charging** | Do not accept cap plus firmware shutdown as isolation or as a demonstrated no-charge-while-worn interlock. Resolve the physical/electrical boundary before choosing the radio/USB architecture. |
| **D-6 firmware** | Keep decoding on the laptop and firmware focused on acquisition/transport. Add the missing data contract, early bootstrap plan, and hardware-specific test protocol; the existing protocol cannot remain unchanged. |
| **D-7 order sequence** | Prefer board/bench before shell, but only after the preordered flex's site-adjustment contract is resolved. Simultaneous ordering is not the default under the one-order constraint. |
| **D-8 suppliers** | Keep JLC as a candidate, not an already-qualified price winner. Compare accepted manufacturing routes and delivered totals; separate distributor location, fabrication origin and battery shipping eligibility. |

## What stays not settled

These are not all tasks for Rolf. The engineers should close the engineering questions before presenting him with a spend decision.

| Unsettled item | Required closing evidence |
|---|---|
| USB/electrode boundary and gel-bench safety | A reviewed connection/state diagram and specified physical restriction or qualified isolation; off-body tests before skin connection |
| Exact battery/charger/harness | Current pack drawing, maximum ratings, connector/polarity and complete routed envelope; charger limits including reset/tolerances |
| Contact joint and nickel/material evidence | Exact screw and nut drawings/material records, captive supported flex-pad section, finish qualification, tightening/strain-relief and inspection criteria |
| Actual thin/full packing | Complete maximum-dimension layouts, including ports, battery harness, insulation, antenna exclusion and adjustable contact sites; no universal impossibility claim from a restricted search |
| Assembly and sourcing | Accepted service tier, panel/stiffeners/interconnect work, non-R AFE and module ordering codes with usable stock/lead time, programming/test/depaneling scope |
| Firmware and protocol | Bootstrap/update/recovery before procurement; calibrated acquisition contract and revised frozen criteria before dry data |
| Skin-contact finish and new closure | Evidence meeting R3 for the ordered process; dimensioned replacement closure/hook with a safe first-assembly acceptance procedure |
| One-order risk and complete price | Complete delivered budget, explicit stop/rework disposition and residual-risk statement; no unauthorized second purchase |
| Owner inputs | Actual measurements, budget ceiling, appearance/colour and manufacturing-origin preference; use the existing Massachusetts destination as a planning assumption only until Q36's current delivery destination is confirmed |

## For Rolf

Do not order this draft. The immediate issue is not whether to accept a slightly thicker shell: the proposed battery/charger pair exceeds the published cell charging limit, the charging “interlock” is only a software inhibit, and the board is being budgeted under the wrong manufacturing route. The screwdriver-only contact joint is also not yet specified as something you could actually assemble with one tool.

Keeping the decoder on your laptop and buying a custom assembled board before the shell are sensible directions. They do not require pretending a paper template proves pressure/contact reliability or that a first custom assembly is guaranteed to work. The next revision should narrow to a qualified, completely costed architecture, preserve your thin request until the packing comparison is real, and state what happens without further spending if first-assembly validation fails.

No supplier was contacted and no purchase or upload was made. Only this review file is being written. The unresolved live-source results are recorded above rather than supplied with invented quotes or prices.

NOT SIGNED OFF
