# Turn 04 — pro (plan v2)

Reviewed: `docs/fab/plan-v2.md` **at commit `6552942`**, retrieved with `git show 6552942:docs/fab/plan-v2.md`, not replaced by the working-tree draft. Read `tasks/plan-v2/turns/03-fable.md`, the complete previous `02-pro.md`, and the review protocol. The standing v1 specification, open questions, packing report and `montage.md` remain supporting documents from the preceding turn.

Review and live-source access date: **2026-09-17**. Publication and drawing revision dates are separately identified below. Relevant PDF tables and drawings were inspected as page images. This is a specification/source review with arithmetic, not a CAD execution, assembled-device test, safety certification or supplier quotation. No purchase, supplier contact, quotation request or design upload was made.

Fable accepted all fifteen findings, some with a different remedy; none was rejected. Changing a remedy is acceptable. The tests below concern whether the replacement actually meets its stated contract, not whether it preserves my earlier preferred implementation.

**Verdict: NOT SIGNED OFF. Seven substantive findings, numbered 16–22: two blockers and five majors.** Several important previous issues are closed. In particular, dropping the incompatible XIAO pairing, restoring thin to the search, separating the factory bootloader from the application, and making release checks non-skippable are real improvements. The new spring part exists. Its existence does not establish the proposed nut workspace or tolerance stack.

## Disposition of all fifteen previous findings

“Closed with a condition” means the planning remedy is acceptable provided the named, mandatory pre-release evidence is obtained; it does not mean that evidence already exists. A condition does not require buying parts or running physical experiments during this dialogue. “Still open” identifies a contradiction or omission in the present written contract.

| Previous finding | Disposition | Remedy assessment and sentence action |
|---|---|---|
| 1. USB/electrode boundary | **Still open** | Battery-only acquisition and off-body checks are now explicit. Replace “A plugged device cannot be worn; that is the physical interlock.” The medial opening has not established that claim and does not interlock the external gel leads. Replacement in finding 16. |
| 2. DTP301120 versus XIAO charge current | **Closed with a condition** | The stock-XIAO incompatibility is removed. Retain the BQ25100 nominal 20 mA choice only subject to G1's complete charge profile. The new sentence “TS disabled or a fixed resistor per its datasheet” needs replacement under finding 18; that is not a recurrence of the old 50 mA arithmetic error. |
| 3. Screwdriver-only contact assembly | **Still open** | Captive nuts and a named hex key address anti-rotation and tool ambiguity. The replacement spring joint still lacks a valid landing/height contract. Change the sentence granting ±2 mm from the nut's across-flats dimension; see finding 17. |
| 4. Finish/material chain | **Closed with a condition** | OSP as a pressure-contact substitute and the claim of a sealed cavity are removed. R3 now explicitly presents a weaker-evidence choice to Rolf rather than silently certifying it. Add to R3: “A written acceptance records the limits of the evidence; it is not a test certificate, does not establish nickel-free plating, and does not waive the electrical boundary.” The new port plug and internal spring containment remain part of findings 16–17. |
| 5. Thin impossibility claim | **Closed** | The revised §3 distinguishes failed stacks from an impossibility proof and tests the thin case. No replacement is required. Keep the complete-envelope search and report actual passing dimensions, not an expectation as a result. |
| 6. Wrong assembly tier | **Closed with a condition** | Standard rigid-board assembly is an appropriate candidate rather than the previous Economic-flex assumption. Replace the unconditional “One-sided assembly” with “Assembly sides are taken from the released placement drawing and priced accordingly.” The underside springs make the actual face allocation consequential; finding 22. |
| 7. Architecture rule | **Closed** | Gates, owner-approved objective order and the no-eligible-candidate outcome resolve the earlier rule defect. No replacement is required. Individual gates still need the corrections below; an objective order is not itself a gate failure. |
| 8. 500 SPS and unchanged protocol | **Still open** | 2000 SPS removes the original Nyquist contradiction. The mapping still changes dropout semantics and needs separate DC and filtered measurement paths. Replace “dropout as frames lost or samples at rail” and qualify “Its numbers stay as accepted”; finding 20. |
| 9. Power and return paths | **Still open** | The supply assignment and separately protected RLD path are now explicit. The battery protection threshold is not an AFE undervoltage cutoff. Replace the parenthetical relying on the pack cutting off below the AFE minimum; finding 19. |
| 10. Battery harness | **Closed with a condition** | G1b/C12 now stop release without an exact harness, polarity and routed envelope. The source discrepancy remains real. Add to step 6: “Keying is not polarity verification; mate only the G1b-qualified harness after the specified off-body polarity check.” Live evidence is recorded below. No assumed SH or PH footprint may pass G1b. |
| 11. Factory image versus later firmware | **Still open** | A factory bootloader followed by a later application resolves the chronology. The fallback still is not a complete specified programming connection, and recovery is not defined by a reset pad alone. Replace the two-tool/one-command sentence as in finding 21. Factory acceptance and its price remain quote-only, not a verified service for this board. |
| 12. Board ordered before sites | **Still open** | Waiting for the bench before ordering the shell is retained and the out-of-workspace stop is correct. The claimed ±2 mm workspace is not demonstrated and cannot be derived from a 5 mm nut. Replace it under finding 17 before purchasing a site-specific board. |
| 13. Skipped checks and first-try promise | **Closed** | R1/R6 and the pinned, fail-closed release job resolve the original defect. No replacement is required. Physical uncertainty is now expressly retained rather than concealed by an ERC/DRC pass. |
| 14. New closure inheriting gauge approval | **Closed with a condition** | A new closure/hook drawing and first-assembly check are valid remedies; a concealed screw is not inherently objectionable. Change “20 N pull by hand” to a defined load application and measurement method, or label it a qualitative hand-retention check. Include any required measuring tool in R2b. This clarification can be carried into WP14/WP15 and is not an independent reason for another round. |
| 15. Delivered budget and turnkey claim | **Still open** | Explicit allowances and a Massachusetts assumption are improvements. Standard/Economic fees are still mixed, the programming kit is incomplete, and the later shell commitment needs a reserved delivered budget before the first spend. Finding 22 supplies the correction. Also replace “No vendor delivers that” with “No accepted, priced turnkey delivery route has been established for this build.” |

### C12 live recheck: the harness condition is necessary

The [SparkFun PRT-25270 page](https://www.sparkfun.com/polymer-lithium-ion-battery-40mah-jst-sh.html), accessed 2026-09-17, displays **$7.39** and describes a “JST-SH connector - 2mm spacing between pins”. Its linked [Data Power drawing](https://cdn.sparkfun.com/datasheets/Prototyping/SPE-00-301120-40mah-en-1.0ver.pdf), version 1.0 dated 2015-11-06, page 9, labels the connector **“JST-PHR-2PIN”** and specifies 100 ±3 mm leads. This is not a reconciled current pack/harness drawing.

JST's own [SH sheet](https://www.jst-mfg.com/product/pdf/eng/eSH.pdf) identifies **“1.0 mm pitch”**; its [PH sheet](https://www.jst-mfg.com/product/pdf/eng/ePH.pdf) identifies **“2.0 mm pitch”**. Both were accessed 2026-09-17. The discrepancy is documentary evidence, not proof of what connector or polarity a delivered pack will have. Keep G1b closed to release until the exact mating part, pin numbering, polarity, maximum harness geometry and permitted shipping service agree. The vendor's US shipping restrictions also need to be applied to the Massachusetts checkout; no international/express route is assumed.

## New and still-unresolved findings

### 16. Moving USB onto the medial face does not establish the claimed physical interlock

**Severity: blocker. Sections:** §1 item 6, R7, G2, §§3, 5.4, 5.6 and 10. **Related previous finding:** 1.

**Sentence to change:** “With the device on the ear the medial face lies against the head; a plug cannot be inserted or remain inserted.”

**What remains wrong.** This is still a conclusion without a defined exclusion mechanism. The electrodes protrude from the face; the local face-to-skin gap is therefore not established by declaring the whole face coincident with a skull plane. The head is not an undeformable CAD plane, the hook can move, and USB plugs have different overmoulds and cable exit directions. Interference with a nominal head model could make the intended fit awkward without proving that no electrode can remain against skin in a plugged configuration.

There is a decisive second configuration that does not depend on ear geometry: at S2 the board is on a desk stand and its three gel leads reach Rolf. Moving the port onto the future shell's medial face does not prevent USB connection to that board while the gel leads remain attached. The battery-only procedural rule correctly forbids this, but the stand and port placement do not physically enforce it. G2 must distinguish that procedural restriction from a demonstrated disconnect/interlock. Firmware power-down still does not remove copper paths.

**Effect of the opening on the contact face.** An approximately 9 × 3.5 mm opening removes roughly 31.5 mm² from the medial face before corner radii, retention details and wall margins. That area estimate alone does not prove structural failure. It does mean WP11/WP14 must evaluate a different skin-facing structure, not merely fit a connector box inside the old cavity. Specify the connector's actual mating axis and mounting orientation, local wall ligaments to the hook, nearby contact bosses, plug support, retention, skin-side protrusion/recess and the face's deformation under load. A generic 8.9 × 7.3 × 3.2 mm receptacle box supplies none of those interfaces.

The silicone plug becomes a skin-contact component and potentially a fourth pressure point. Its material, installed height, retention and failure state are not covered by PA12 evidence. If it is absent or displaced, the assertion that the receptacle shell never touches skin is no longer guaranteed. A closed lid is not a seal against perspiration entering this opening.

**Evidence.** The conflict follows directly from the pinned port geometry, protruding contacts and external gel-header configuration. The [TI BQ25100 reference circuit](https://www.ti.com/lit/ds/symlink/bq25100.pdf), Rev. C, page 1, accessed 2026-09-17, is a charger circuit, not an isolated patient interface; it provides no basis for treating acquisition shutdown as disconnection. No measured leakage or fitted-head test is claimed here.

**Required replacement:** “The medial port is a candidate ergonomic exclusion feature, not an established physical interlock. G2 must define and verify the permissible charging/acquisition assemblies, including the external gel harness, and prevent a powered USB connection to any skin-connected electrode path by the accepted physical arrangement or separately reviewed isolation. Firmware inhibit is secondary. All on-body acquisition remains battery-only with external power/data cables disconnected.”

Define one actual mechanism and its off-body checks before G2 passes. A charging configuration that requires removal of the electrode-bearing assembly is one possible approach, not a demand for a particular redesign. A claim limited to procedural off-body charging must instead be stated as a proposed change to R7, not passed off as geometric impossibility. Include the port plug, opening and lost/removed-plug state in the material and mechanical gates.

### 17. A suitable spring exists, but the 5 mm nut cannot grant the claimed ±2 mm workspace

**Severity: blocker. Sections:** §3, G5/G7, §§5.2–5.3, 8 and 10. **Related previous findings:** 3 and 12.

**Sentence to change:** “The nut face is Ø5.0 across flats; a site may move ± 2.0 mm from nominal before the contact leaves the nut, so the bench (S2) may choose sites inside that workspace without a new board.”

**C11 verified candidate.** [Harwin S7121-42R](https://www.harwin.com/products/S7121-42R), accessed 2026-09-17, states: **“Free height = 1.7mm, working height = 1.5mm, minimum height = 1.2mm.”** It also states **“Gold finish on contact area and termination.”** This directly answers the requested existence question.

The linked [Harwin S7121-42R customer drawing](https://content.harwin.com/asset/b2065811-22ac-4b29-8497-b8b2be4014ae/DRG-02326-Technical-Drawing-Datasheet-S7121R-pdf.pdf), issue 8 dated 2022-01-11, inspected as a page image on 2026-09-17, specifies a **1.2 N minimum force at 1.50 mm working height**, a 1.20 mm minimum working height, and **0.7–1.3 µm nickel with gold flash on the contact areas**. It is an internal, nickel-bearing contact candidate, not a nickel-free electrode. Its actual assembler stock, cut quantity, price and qualification against an unplated brass nut remain unverified.

**Why the workspace fails.** Across flats is not the diameter of a solid landing disc. The nut has a threaded central opening occupied by the screw; §3 places the screw tip 0.9 mm above the nut. There is only a narrow brass land between the central thread/chamfer and the hex perimeter. Even using the generous idealization of a 5 mm-wide face and only a 2.5 mm central excluded diameter, the radial land toward a flat is `(5 − 2.5)/2 = 1.25 mm`, before allowing the spring's finite footprint, nut chamfers, placement error or wear.

A spring placed over the centre meets the screw tip, not the brass top face. Moving the nut relative to the board can move the tip under a spring that initially touched brass. A 1.5 mm working gap referenced to the nut becomes approximately **0.6 mm** over a tip 0.9 mm higher. That is below this candidate's 1.2 mm minimum height. Conversely, avoiding the tip constrains the useful landing region; it does not provide an unrestricted ±2 mm disk or square around the nominal site. The workspace shape and directions must be specified and computed from the actual contact surface, not inferred from across-flats width.

**The height margin is also real.** The candidate has only 0.2 mm nominal compression from 1.7 to 1.5. JLC's [PA12-HP page](https://jlc3dp.com/help/article/pa12-hp-nylon), accessed 2026-09-17, lists ±0.3 mm below 100 mm. A single ±0.3 mm contribution to the nominal gap already spans 1.2–1.8 mm: the high end can lose preload and the low end consumes the whole compression limit before the other tolerances. This is an illustrative tolerance counterexample, not an assertion that every part dimension has an independent ±0.3 error. G7 needs the actual datum chain, PCB deflection and mechanical stops.

Three such contacts at their stated working force impose at least about **3.6 N** of reaction on the board/support assembly. That is not automatically 3.6 N of skin force; the board fasteners and nut pockets carry the internal load. Their deflection, pull-out and creep nonetheless affect contact compression. Self-forming ISO 7380 screws in unqualified PA12 pilot holes do not establish that support by designation alone.

**Corrected example height budget, not an impossibility proof:** if the module is on the opposite PCB face directly above this joint, nut 1.6 + spring gap 1.5 + PCB 1.0 + Raytac reservation 2.3 = **6.4 mm above the inner floor**. With the stated floor and lid that is **8.9 mm outer height before additional allowances**. A different lateral arrangement can differ. WP11 must not substitute the spring's 1.5 mm height for the entire joint stack.

**Required replacement:** “Each contact site has a bounded adjustment region computed from the actual nut or separate landing feature, excluding the screw tip, thread opening, chamfers and edges, and reduced by the spring footprint and tolerances. No ±2 mm workspace is promised. G7 specifies a stocked candidate, controlled working-height range, positive overtravel protection, stable low-level contact, structural support and the installed clearance/insulation envelope; G5 proves that region before the board is ordered.”

Use the Harwin part as a candidate, not an automatic selection. A larger supported landing feature, a different contact or a different electrode carrier may be needed. Gold on one side of a brass pressure joint is not by itself a microvolt-signal stability test. Define off-body continuity and motion/noise acceptance with appropriate test access; an unspecified LED self-test or a 1 kΩ-scale check is not a complete proof of every joint. Internal nickel remains permissible only under the documented containment rule; electrical continuity to a titanium screw does not itself prove nickel exposure.

### 18. Twenty milliamps is feasible, but the TS and termination choices do not yet meet G1

**Severity: major. Sections:** G1, §5.5 and §8 charging indication. **Related previous finding:** 2, with new charger-configuration evidence.

**Sentence to change:** “BQ25100 charger with ISET for 20 mA, TS disabled or a fixed resistor per its datasheet, VBUS only from the receptacle.”

**Live evidence.** The [TI BQ25100 datasheet](https://www.ti.com/lit/ds/symlink/bq25100.pdf), Rev. C, pages 3 and 6, accessed 2026-09-17, says: **“Floating TS pin or pulling high puts part in TTDM ‘Charger’ mode and disables TS monitoring, Timers and Termination.”** The alternative fixed 10 kΩ connection is a different defined configuration, not interchangeable with floating TS. The part's minimum absolute termination current is 1 mA.

The [Data Power sheet](https://cdn.sparkfun.com/datasheets/Prototyping/SPE-00-301120-40mah-en-1.0ver.pdf), version 1.0, page 4, accessed 2026-09-17, gives maximum continuous charge **40 mA**, end-of-charge **0.01C**, and charging temperature **0–45°C**. For 40 mAh, 0.01C is **0.4 mA**. Both tables were inspected as images.

The nominal-current choice is not the problem: using TI's typical ISET factor 135 AΩ gives `135/0.020 = 6750 Ω`. An illustrative 6.81 kΩ, 1% resistor and the listed maximum factor 145 AΩ give `145/(6810 × 0.99) ≈ 21.5 mA`, below 40 mA. WP12 still owns the actual component and full worst-case operating calculation.

The remaining contract problem is that “TS disabled” can select behavior that disables termination/timers, while a fixed resistor removes actual pack-temperature sensing. The charging window must be enforced or explicitly bounded by a reviewed operating procedure; IC die thermal regulation is not pack-temperature measurement. The 1 mA termination floor also differs from the cell sheet's 0.4 mA endpoint. Earlier termination is not automatically unsafe, but it is not an identical qualified charge/capacity profile and must not be described as one.

**Required replacement:** “WP12 fixes the BQ25100 ordering code, ISET and PRETERM networks, TS connection, maximum charge voltage/current, timer behavior, parallel system load and permitted pack-temperature conditions. Floating/high TS is not an allowed shorthand for normal terminated charging. G1 records whether the selected termination profile is accepted for the exact pack and what capacity/runtime assumption follows.”

Retain 20 mA as the candidate setpoint. Either qualify the termination/temperature arrangement or change the charger; do not bypass the discrepancy because the current is small. Also define what the LED actually indicates. The BQ25100 has a PRETERM pin where the BQ25101 variant has CHG; a VBUS indication must not be labelled verified charging/completion without the corresponding measurement or circuit. This can be resolved in the design gate without requesting a battery test from Rolf now.

### 19. Pack protection below 2.7 V does not keep a 3 V AFE supply valid

**Severity: major. Sections:** §5.5, G1/G2/G6 and protocol validity. **Related previous finding:** 9.

**Sentence to change:** “ADS1292 (non-R) with AVDD = DVDD = 3.0 V from a TLV713 3.0 V LDO on the battery (AVDD minimum 2.7 V per the datasheet; the pack's protection cuts off below that)”.

**Evidence.** [TI ADS1292 Rev. C](https://www.ti.com/lit/ds/symlink/ads1292.pdf), page 9, accessed 2026-09-17, lists **2.7 V minimum AVDD–AVSS**. The [Data Power pack specification](https://cdn.sparkfun.com/datasheets/Prototyping/SPE-00-301120-40mah-en-1.0ver.pdf), page 7, accessed the same day, gives **“Over discharge detection voltage”** as **2.4 V ±0.100 V**. That is a protection threshold, distinct from page 4's 2.80 V discharge endpoint.

A linear regulator cannot maintain a 3.0 V output when its input is below the necessary output-plus-dropout headroom. Relying on a pack cutoff below the AFE minimum leaves a region where the pack still powers the board but the declared acquisition operating conditions are no longer met. Reset/restart or radio-current transients make an undefined boundary worse; the 10-second battery report is not an undervoltage design by itself.

**Required replacement:** “The system inhibits acquisition and marks samples invalid before the worst-case AFE supply leaves its specified range. WP12 defines the battery/rail threshold, regulator-dropout and load margins, hysteresis, shutdown/restart behavior and digital-pin states. The pack PCM is a last-resort cell-protection device, not the measurement-validity cutoff.”

The exact threshold belongs to WP12's named LDO and current budget. State that requirement now rather than relying on the favorable-looking 3.0 V nominal label. No different regulator is mandated if the chosen one and a proper undervoltage boundary meet the contract.

### 20. The new sample rate is valid, but protocol v2 must preserve measurement meaning and dropout semantics

**Severity: major. Sections:** G6, §6, S0/S2/S5. **Related previous finding:** 8.

**Sentences to change:** “Its numbers stay as accepted (Q28)” and “dropout as frames lost or samples at rail.”

**What is resolved.** [TI ADS1292 Rev. C](https://www.ti.com/lit/ds/symlink/ads1292.pdf), Table 4 on page 16, accessed 2026-09-17, explicitly pairs **2000 SPS** with **524 Hz −3 dB bandwidth** at the relevant setting. The cited 524 is correct. A 2000 SPS stream can support the requested 20–490 Hz analysis band; the earlier 500 SPS contradiction is gone.

**What still matters.** A −3 dB corner just above 490 Hz is not a flat response or proof that old peak-to-peak and noise measurements are numerically interchangeable. Input-referred scaling removes the gain factor, not the acquisition/filter transfer function. The release table must specify the digital filter, measurement windows, treatment of startup/transients, and whether each threshold is intentionally applied to the newly filtered signal or to a calibrated equivalent. That is a controlled protocol revision, not silently weakening a frozen threshold.

The old `montage.md` §3.4 defines dropout using rail saturation **or a flat trace lasting more than 100 ms**. The rewritten phrase omits the flat-trace condition and its duration, while adding transport loss. These are different failures. At 2000 SPS, 100 ms is 200 samples; at 20 samples/frame it is ten frame durations. A transport sequence number does not reveal an ADC sample that was never captured before framing unless the acquisition counter/status also records that loss.

The old INA128 output-shift criterion is ±0.5 V at gain 10, hence **±50 mV input-referred**, using the stated old gain. Evaluate that offset on the raw/DC-preserving path, not after the 20 Hz high-pass that removes it. Keep common-mode and input headroom checks separate from that differential threshold.

For an implementation check, the nominal signed-code scale is approximately `2.42 / (12 × (2^23 − 1)) = 24.04 nV/code`, with approximately ±201.7 mV differential full scale. These are nominal conversion arithmetic, not proof of achievable resolution or tolerated common-mode voltage. The code format, reference/gain metadata and actual clock/rate must accompany the data.

**Required replacement:** “Before S0, WP13 releases the ADS1292-specific measurement and transport contract and a criterion-by-criterion protocol-v2 table. It preserves or explicitly records each approved change, including the original flat-trace/rail duration criterion, separate acquisition and transport losses, DC offset before high-pass filtering, calibrated units, filter/window definitions and input headroom. No dry result is accepted against an unspecified mapping.”

Define byte order, frame/version fields, sample counter/timing, incomplete-frame handling and BLE fragmentation for the negotiated payload. Twenty samples alone occupy 60 bytes before metadata; the receiver cannot assume a single notification always holds a frame. This is an implementation contract for the existing streaming boundary, not a request to move decoding onto the wearable or develop a new classifier.

### 21. Factory UF2 is a coherent route; the stated fallback and recovery are still incomplete

**Severity: major. Sections:** G4, §6, R2b, §8 and §9. **Related previous finding:** 11.

**Sentence to change:** “press the Tag-Connect TC2030-NL pogo cable onto the board's footprint with a Raspberry Pi Debug Probe attached and run one command from `docs/fab/assemble.md` (about 30 s); both tools are in order 3 under that condition.”

**Factory service: what the pages actually establish.** [JLC's assembly-capabilities page](https://jlcpcb.com/capabilities/pcb-assembly-capabilities), accessed 2026-09-17, states: **“For standard assembly orders, we partially support this programming service.”** It asks for target/programming information for assessment. I did **not** authenticate an explicit acceptance and published price for programming two nRF52840 modules over SWD, including fixture and verification. The [JLC fee schedule](https://jlcpcb.com/help/article/pcb-assembly-price) does not supply a target-specific SWD fee.

The public [Screaming Circuits assembly page](https://www.screamingcircuits.com/capabilities/pcb-assembly), [MacroFab capabilities](https://www.macrofab.com/capabilities/) and the accessible [CircuitHub documentation](https://docs.circuithub.com/getting-started/welcome) did not yield a verified target-specific SWD service/price in this check. This is a limited retrieval result, not a claim that those companies cannot do the work. **C6 remains quote-only and requires later owner-authorized acceptance.** No quotation was requested.

**The fallback needs more than two family names.** [Tag-Connect TC2030-IDC-NL](https://www.tag-connect.com/product/tc2030-idc-nl), accessed 2026-09-17, is listed at **$33.95**, with a **“6-pin 0.1″ pitch ribbon connector.”** The separately listed [TC2030-MCP-NL](https://www.tag-connect.com/product/tc2030-mcp-nl-6-pin-no-legs-cable-with-rj12-modular-plug-for-microchip-icd) is **$35.95** and has RJ12. “TC2030-NL” does not specify which host-end connection has been qualified.

The [Raspberry Pi Debug Probe documentation](https://www.raspberrypi.com/documentation/microcontrollers/debug-probe.html), accessed 2026-09-17, states: **“The probe operates at 3.3V nominal I/O voltage.”** Its SWD port is a three-pin connection; the supplied harnesses do not establish a direct six-pin Tag-Connect mating assembly. Target power and common ground, an exact no-solder adapter/pin map, target-voltage compatibility and physical contact retention must be specified. A [US retail page](https://www.adafruit.com/product/5699), accessed the same day, lists the probe at **$12.00**. Thus $33.95 + $12.00 = **$45.95 for these two listed items**, before any adapter, target-power arrangement, shipping or tax. This is not a complete verified programming kit, and the draft's $60 remains an allowance rather than a measured task cost.

**Bootloader/app/recovery.** The [Adafruit nRF52 bootloader repository](https://github.com/adafruit/Adafruit_nRF52_Bootloader), accessed 2026-09-17, documents board-specific bootloader builds and distinguishes bootloader flashing from SoftDevice/MBR provisioning. It supports the general concept, not a ready-made image qualified for this custom board and its nRF Connect SDK application. Freeze the exact target build, factory HEX/BIN contents, flash layout, required provisioning, application start address, USB identity and update/recovery procedure. Do not assume a UF2 file format determines these choices.

A reset pad beneath the lid is not yet a one-tool recovery interaction: specify how Rolf enters and confirms bootloader mode without shorting arbitrary copper, what happens after a bad application image, and whether the recovery tool is in R2b. A pre-release factory test should record programming verification, USB enumeration and a representative update/recovery check; it need not pretend the final analog performance has already been tested.

**Required replacement:** “Before S1, G4 selects either an accepted factory SWD programming-and-verification job at a stated price or an exact, fully connected no-solder fallback kit with power, pin mapping and target-voltage compatibility. WP13 supplies the board-specific bootloader/provisioning image and compatible application layout, and WP15 supplies a tested programming and recovery procedure. Completion time is measured, not promised as 30 seconds.”

The bootloader-first strategy is accepted. The unresolved issue is treating an unqualified connection and pad as a complete owner workflow.

### 22. The revised allowances still need a coherent manufacturing basis and a whole-project delivered-spend gate

**Severity: major. Sections:** G3/G8, §5.2, §9 and S1/S3. **Related previous findings:** 6 and 15.

**Sentences to change:** “One-sided assembly.” Also the price entry “feeder $1.53 each, extended parts $3.07 each (JLC schedule)” and the claim that R8 is closed solely by three separate checkout gates.

**Manufacturing and fee correction.** The board has underside SMD spring contacts. A one-sided build remains possible only if the released placement puts all assembled parts on that same face; a module/front end on the other face makes it a two-sided job. The plan currently fixes the price before this is resolved. The port orientation and edge header also need the actual accepted placement/assembly process.

[JLC's price schedule](https://jlcpcb.com/help/article/pcb-assembly-price), updated 2026-09-09 and accessed 2026-09-17, separates **“$3.07 Extend”** for Economic from **“$1.53 Basic/Extend”** for Standard. Do not add both to every Standard extended item. Its relevant published components are:

| Component, not a configured quote | Standard one side | Standard two sides |
|---|---:|---:|
| Setup | $25.56 | $51.12 |
| Stencil | $8.21 | $16.42 |
| Arithmetic subtotal of those two items | **$33.77** | **$67.54** |

The same schedule lists a rigid-PCB two-fixture amount of $16.42 for 1–29 pieces where applicable, and $1.64 per inspected component in the 1–10 X-ray bracket. Its handling fee explanation is conditional, not an instruction to add every listed fee. All remaining actual manufacturing, component, inspection, programming and delivery lines still need the selected order. These numbers do not constitute a minimum or final quote for Elicio.

**Orders at the present evidence level.**

| Order | What is substantiated or corrected | What remains unpriced |
|---|---|---|
| Board, allowance $150–220 | Correct Standard service components above; assembly sides must follow placement | Complete accepted BOM/quantity, required panel or handling arrangement, factory depaneling, any fixtures, programming and functional test, freight, import collection and tax |
| Shell, allowance $50–90 | [JLC PA12-HP](https://jlc3dp.com/help/article/pa12-hp-nylon), accessed 2026-09-17: “Price: From $1.00”; “Build time: 72 hours” | This body/lid/spare, the R3-qualified finish, shipping, duties and tax; no configured price was obtained |
| Small parts, allowance $80–130 | [Sortafast](https://sortafast.com/products/sortafast-titanium-screws-button-head-10pk-m2-5) displays $17.50/10; [SparkFun](https://www.sparkfun.com/polymer-lithium-ion-battery-40mah-jst-sh.html) displays $7.39; accessed 2026-09-17 | Verified nut price; qualified plugs/foam; complete gel leads, stand and electrodes; inspection tools; all shipments and tax. Screw geometry/lot evidence and pack harness still gate purchase |
| Conditional owner-programming kit | Named IDC cable and probe above total $45.95 at displayed prices | Adapter/harness, target power, any retention fixture and delivery; neither a complete $45.95 kit nor a confirmed $60 total |

The allowances sum correctly: **$150–220 + $50–90 + $80–130 = $280–440**. The issue is scope, not that addition. Small parts are a procurement category spanning multiple sellers, not necessarily one parcel or one delivery charge.

**C13: duties and Massachusetts tax, with dates and limits.**

[JLC's tariff FAQ](https://jlcpcb.com/help/article/us-tariff-policy-faq), updated 2026-09-09, accessed 2026-09-17, states **“122 Tariff: 12.5% (New，effective July 24, 2026)”** and separately says it uses 10% for that element in its own collection calculation. It also distinguishes individual-customer DDP from company shipping options. Those are merchant statements, not independently verified September statutory classifications/rates for this board and shell. Its detailed product-rate image could not be retrieved; I did not verify the exact current PCBA or plastic-print collection percentage from that image.

The [February 20, 2026 federal surcharge proclamation](https://www.whitehouse.gov/presidential-actions/2026/02/imposing-a-temporary-import-surcharge-to-address-fundamental-international-payments-problems/), accessed 2026-09-17, prescribed a 10% surcharge for a period ending July 24 unless changed or extended as provided there. It therefore does **not** independently verify JLC's asserted post-July rate for September 17. I did not authenticate a later primary instrument establishing that exact 12.5% claim. Do not reuse an expired period as current evidence.

The [February 20 de-minimis order](https://www.whitehouse.gov/presidential-actions/2026/02/continuing-the-suspension-of-duty-free-de-minimis-treatment-for-all-countries/), accessed 2026-09-17, continues suspension for the covered shipments **“regardless of value, country of origin, mode of transportation, or method of entry.”** It supplies no basis to assume these ordinary commercial orders are duty-free merely because each is below $800. Exact September duties still require the current applicable classification, origin, customs value, exclusions and import/merchant terms. An assembled acquisition board must not silently be priced as a bare IC or assumed to inherit a bare-PCB classification.

Massachusetts separately imposes **6.25%** sales/use tax, subject to the applicable rules and exemptions. The current primary texts [Chapter 64H §2](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleIX/Chapter64H/Section2) and [Chapter 64I §2](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleIX/Chapter64I/Section2), accessed 2026-09-17, state **“at the rate of 6.25 per cent”**. Lack of seller collection does not itself prove the purchase is exempt. As arithmetic only, a taxable base of $280–440 would yield $17.50–27.50; the actual base and collection treatment must come from the order/tax record, not this illustrative calculation.

**Current exact delivered total: UNVERIFIED.** No current exact PCBA/print statutory rate, configured DDP charge or US-assembler price is invented here. The unresolved rate does not justify leaving an unbounded import bill outside R8.

**Required replacement:** “Before the first payment, Rolf receives the selected assembly-side/service calculation and a cumulative delivered budget covering all orders, programming, every shipment, import collection and applicable Massachusetts sales/use tax. Where the shell cannot yet be finally quoted, reserve a stated maximum for it and a stop condition; later checkout gates update the same remaining balance. No initial order is represented as within the complete-project ceiling while necessary later costs are unbounded.”

Use DDP totals without adding already-collected duties twice. Keep statutory duty, merchant advance collection, shipping and sales/use tax as different ledger entries. A US sales office is not proof of US manufacturing origin. US assembly/print alternatives remain quote-only until their actual origin and like-for-like services are accepted. Requests for those quotes still require the authorization the plan specifies.

## What stays not settled

These are closing tasks for the appropriate work packages, not a list of engineering decisions to push onto Rolf.

| Unsettled item | Closing evidence / owner |
|---|---|
| USB/electrode boundary, including the gel bench | Corrected R7/G2 mechanism and state diagram, all three paths, charging and disconnected configurations, off-body checks; WP12 with WP11/WP14 |
| Medial opening and plug | Exact connector/plug parts, orientation, local wall/support geometry, retention, skin-contact evidence and lost-plug disposition; WP11/WP14 |
| Spring interface and site workspace | Actual usable landing region, screw-tip exclusion, tolerance-controlled compression, support load, finish/continuity qualification and orderable spring; WP12/G7 and WP11/G5. S7121-42R establishes existence, not suitability |
| Battery charge and low-voltage behavior | Exact charger configuration and pack revision; termination/temperature acceptance; independent acquisition-validity shutdown and recovery; WP12/G1/G2 |
| C12 harness | One reconciled current drawing, mating connector and pin polarity, complete routed leads, qualified delivery route; G1b before PCB footprint freeze |
| Acquisition/protocol v2 | Filtered and DC paths, units, amplitude transfer, original or explicitly revised dropout semantics, sample timing/loss reporting, test-table version before release/data; WP13/G6 |
| First-load and recovery | Accepted factory SWD job and price, or complete matched owner kit; exact bootstrap/application layout, provisioning and accessible recovery; WP13/WP15/G4 |
| Manufacturing and budget | One- or two-sided accepted layout, full BOM and required services, real import collection and applicable tax, complete-project reserve before first payment; G3/G8 |
| Finished materials, nut/screw evidence and closure | R3 process evidence or explicit limited-evidence owner choice; G3/G7 part documents; new WP14 closure/hook and measurable acceptance. No old gauge approval is inherited |
| Owner inputs | Actual M1–M8, overall ceiling, appearance/colour, confirmed Massachusetts delivery and origin preference, objective order and residual-risk acceptance |

## Stop-rule assessment: substantive, not cosmetic

The remaining disagreements change which electrical configurations can contact the body, whether the preordered board can reach the chosen sites, whether springs remain engaged without overtravel, whether charging and low-battery operation stay within their contracts, and whether the required programming/manufacturing route fits the complete budget. Those are substantive. They are not requests to reword an accepted decision or repeat a completed source lookup.

The closure's “20 N by hand” measurement wording, the unsupported universal turnkey sentence and similar housekeeping can be corrected in the relevant sheets without buying another review round on their own. I do not require completed hardware, factory quotations obtained without authorization, or wear data to finish this planning dialogue. I require a coherent, bounded contract whose later gates can actually be passed.

## For Rolf

Do not order from this revision yet. The BQ25100 at 20 mA is a credible replacement for the incompatible XIAO charger, and there is a real gold-plated spring at the requested working height. The unresolved part is how those components are integrated: moving USB onto the contact face does not by itself create the claimed interlock, and a nut with a screw through its centre does not provide the promised ±2 mm landing workspace.

The next revision should resolve those mechanisms, the charging/undervoltage states, the acquisition mapping and the complete first-load route without restarting the whole project. Keep thin in the measured search, keep the single-order/no-hidden-spend rule, and keep the distinction between a design gate and evidence from an actual built device. The unknown supplier SWD price and September classification-specific duties remain explicit procurement conditions, not numbers the reviewer has verified.

Only this review file was written. No plan, code, prior turn or design record was changed, and no supplier was contacted.

NOT SIGNED OFF
