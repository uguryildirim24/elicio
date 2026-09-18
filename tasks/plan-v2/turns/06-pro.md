# Turn 06 — pro (plan v2)

Reviewed **2026-09-17**. `git log main` resolved the requested main HEAD after `32cebc6` to **`11c4dcc`**, “plan-v2 turn 05: R7 rewritten without an isolation claim; standoff landing and pin arrays; charger, undervoltage, protocol v2, first-load kit, ledger.” I reviewed `git show 11c4dcc:docs/fab/plan-v2.md`, not a subsequently changing working-tree plan. Also read `tasks/plan-v2/turns/05-fable.md`, the complete previous `04-pro.md`, and `tasks/plan/protocol.md`. Earlier supplied design, montage and review documents remain supporting context; no new code execution or physical validation is claimed.

All external-source access dates below are **2026-09-17**. Relevant PDF drawings and tables were inspected as page images. Manufacturer statements, distributor inventory and engineering deductions are distinguished. No supplier was contacted, quotation requested, design uploaded or purchase made.

**Verdict: NOT SIGNED OFF. Three substantive findings, 23–25: two blockers and one major.** Fable accepted findings 16–22; none is being re-argued after rejection. A procedural off-body charging rule can be a coherent proposal without pretending it provides isolation. The remaining objection is its asserted hazard bound and implementation, not a demand to reinstate a particular interlock. A stocked gold-plated SMT pin with substantial travel and a documented hard stop exists, but its height does not fit the draft's placeholder. The shorter candidate does not establish all the requested properties.

## Dispositions

“Closed with a condition” accepts the planning remedy with the specified evidence required before its release gate. It does not certify hardware that has not been built. Conditions below need to be incorporated into the named work-package acceptance, not silently treated as already satisfied.

### Findings 16–22

| Finding | Disposition | Remedy and sentence action |
|---|---|---|
| 16 — medial port/interlock | **Still open** | Withdrawal of the isolation/interlock claim is accepted. R7's per-path 5 V arithmetic is correct within its assumptions, but is not an overall body-current bound; “if every rule above is broken at once” is false. The hardware supply gate also needs an off-state/back-power contract. Replace the R7 bound/residual-hazard sentences and the supply-gate sentence as specified in finding 23. |
| 17 — landing/workspace and spring stack | **Still open** | A recessed screw and captive standoff improve the joint, but a perforated hexagonal landing is still not a solid disc. A point-grid theorem does not prove full pin landing. The compression direction is reversed in the text, and the assumed 2.0–2.5 mm working-height pin is unverified. Replace the grid guarantee and height paragraph under finding 24. |
| 18 — charger TS/termination | **Closed with a condition** | The fixed TS network, active timers/termination and explicit procedural temperature limit are an acceptable planning remedy. G1 must select the actual voltage variant and networks, document termination with system load, and leave unmeasured capacity loss unknown. Replace “recorded with the capacity it forgoes” with the conditional sentence in the charger check below. No return to the rejected XIAO pairing is needed. |
| 19 — undervoltage | **Closed with a condition** | Separating PCM protection from acquisition validity resolves the architectural error. Replace “inhibits acquisition and marks samples invalid above that threshold” with a downward-crossing shutdown rule and explicit higher restart threshold, given below. Monitoring latency, radio transients and settling must be in WP12/WP13's gate, independent of the 10-second telemetry interval. |
| 20 — acquisition/protocol mapping | **Closed with a condition** | The DC path, original rail-or-flat duration, named filters/windows and per-criterion revision table resolve the earlier mapping objection. The release format still needs the fields its prose refers to: frame sequence, sample count/length, gain/reference and fragmentation metadata. Replace the abbreviated frame sentence with the release-contract sentence below. This is a bounded WP13 deliverable before S0, not a demand to implement it in this review. |
| 21 — first load/recovery | **Closed with a condition** | The exact IDC cable, supplied male jumpers, own target power and accessible reset switch make a coherent candidate route. The voltage and target pin assignment are still checks, not established facts. Replace the asserted 3.0/3.3 V compatibility with the G4 condition below. Factory SWD acceptance/price remains quote-only. A board-specific bootloader and compatible application map must exist before ordering. |
| 22 — manufacturing/budget | **Still open** | Assembly sides, Standard fees and the cumulative reserve are corrected. Taking the larger of two figures for one import component is not a complete duty allowance. The stated all-in envelope also omits the conditional kit at its upper bound. Replace that ledger paragraph under finding 25. |

### Earlier items and conditions from findings 1–15

| Earlier finding | Current disposition | Sentence action / surviving condition |
|---|---|---|
| 1 — USB/electrode boundary | **Still open** | Same unresolved matter as 16/23, not a separate new finding. Change R7 and the residual-risk description under 23. |
| 2 — XIAO/cell current | **Closed with a condition** | The incompatible XIAO route is removed. Keep the nominal 20 mA candidate subject to the completed G1 profile; see the charger check. |
| 3 — one-tool contact joint | **Still open** | Captive anti-rotation and the named hex key are accepted. The new landing, pin state and support-load contract must satisfy 17/24. |
| 4 — finish/material chain | **Closed with a condition** | The new R3 limitation wording is appropriate. Preserve the exact process/finish evidence or explicit limited-evidence owner decision; it is not a certificate or an electrical-safety waiver. No additional wording change is required to R3 itself. The standoff, pin finish and port plug still require their own G3d/G7 evidence. |
| 6 — assembly tier | **Closed with a condition** | “Sides follow the released placement” and a two-sided Standard baseline resolve the old pricing basis. Retain actual assembler acceptance, population quantities and conditional fixtures in G3; no additional change to that sentence is required. |
| 8 — sample rate/protocol | **Closed with a condition** | Same condition as 20: release the explicit ADS1292 protocol and wire format before S0. The 500 SPS contradiction is not reopened. |
| 9 — power/return paths | **Closed with a condition** | Same condition as 19, plus the separately protected RLD path and G2 off-state checks. No assumption that PCM cut-off protects acquisition validity remains acceptable. |
| 10 — harness | **Closed with a condition** | G1b correctly blocks footprint release on the SH/PH discrepancy. Change step 6's red-wire comparison: colour is not electrical polarity verification. The legacy drawing supplies a concrete reason, recorded below. |
| 11 — programming chronology | **Closed with a condition** | Bootstrap before shipment, application later and switch-based recovery are coherent; complete G4's map, voltage and image/recovery checks. See the first-load section. |
| 12 — buying before sites are known | **Still open** | The out-of-workspace stop and board-before-shell order are accepted, but the workspace cannot be granted by the array assertion. Same fix as 17/24. |
| 14 — new closure | **Closed with a condition** | No old gauge pass is inherited, and the unmeasured “20 N by hand” has gone. WP14 must specify the actual first-assembly test, load state and post-drop inspection before powered wear. No further architectural change is demanded here. |
| 15 — delivered budget | **Still open** | Same ledger correction as 22/25. The universal turnkey assertion has been replaced appropriately and is closed. |

Findings 5, 7 and 13 remain closed. Thin stays in the bounded layout comparison; eligibility precedes objectives; release checks fail closed. They are not new findings.

## New and still-unresolved findings

### 23. R7 is a coherent procedural proposal only after its current bound and off-state claims are narrowed

**Severity: blocker. Sections:** summary 6; R7; G2; §§5.4–5.6 and 10. **Continues:** 1/16.

**Sentences to change:** “There is no galvanic isolation between the electrodes and the USB port in any single-battery wearable”; “which bounds device-sourced current to ≤ 23 µA at 5 V”; “The residual hazard is a certified adapter's touch current through a small skin area if every rule above is broken at once”; and “a P-channel switch removes the front end's supply when VBUS is present.”

The first statement should describe this design, not all single-battery wearables. A battery does not logically preclude an isolated interface. Accepting a procedural proposal does not require making that universal claim.

**The 23 µA calculation.** For one intact resistance of at least 220 kΩ with no more than 5.000 V across it, Ohm's law gives 22.73 µA. Even a nominal 220 kΩ, 1% resistor at its low limit gives 22.96 µA at exactly 5 V. Thus the rounded number is not the arithmetic defect. The missing scope is consequential:

| Explicit circuit assumption | Calculated current |
|---|---:|
| One intact 220 kΩ path, 5.000 V across it | 22.73 µA |
| One nominal 220 kΩ path at −1%, 5.000 V | 22.96 µA |
| Illustrative 5.25 V across that −1% path | 24.10 µA |
| Two intact 220 kΩ paths in series, 5 V across the pair | 11.36 µA |
| Three intact 220 kΩ paths in parallel to an external return, 5 V | 68.18 µA total |

These are different hypothetical networks, not measured currents in this device. The 5.25 V row illustrates why a nominal supply label cannot establish a worst-case bound; it is not an asserted specification for a selected adapter. The parallel example is not a claim that normal acquisition sends that current through Rolf. It shows why a per-lead bound is not automatically a total body-current bound.

The 5 V differential calculation does not bound adapter-to-earth common-mode current, a bypass of the resistor, a resistor failure, or contact with an unprotected receptacle/other conductor. Those require their own paths and source assumptions. Testing each electrode only against the port shell also does not establish every electrode-to-electrode or externally referenced return path.

“Every rule broken at once” is particularly misleading. At the gel bench, a person can remain attached while a USB cable is connected, even with the approved adapter used, the supply gate functioning and firmware refusing to stream. The no-cable rule has been violated; the other controls need not all fail. The cap and stand are useful reminders, not disconnection. Do not present an ordinary adapter designation as qualification of this assembled electrode interface.

**Is the hardware gate meaningful?** Yes, as a functional inhibit that can remove AFE operation independently of application software, provided the actual circuit does that. It is not galvanic isolation. A high-side switch alone does not establish absence of power through the digital interface or other rails. [TI's ADS1292 datasheet, Rev. C, printed p.6](https://www.ti.com/lit/ds/symlink/ads1292.pdf), accessed 2026-09-17, limits a digital input to **“DVDD + 0.3”** under absolute maximum ratings. Driving an input high while DVDD is disconnected cannot be assumed permissible. [TI SCDA015C](https://www.ti.com/lit/SCDA015), accessed 2026-09-17, describes how an I/O path can back-power a switched supply. That note establishes the general failure mechanism, not the behavior of an unreviewed Elicio schematic.

G2 must show the switched rails, switch orientation/body diode and VBUS detection, default gate state, SPI/control-pin states, pull-ups and protection paths, rail discharge and startup. Include reset and an uncooperative MCU in the state checks. The result must either support the claimed hardware inhibit or withdraw that credit. Removing AFE power leaves shared returns and electrode connections unless a separate mechanism removes them.

**Required replacement for R7's bound and residual-risk text:**

> This proposed circuit has no galvanic isolation between USB-connected circuitry and its electrode paths. All skin-connected use, including the gel bench, is battery-only with external power, data and debug connections disconnected. The 220 kΩ protection provides a per-path bound only for the specified intact circuit and maximum applied voltage; 23 µA is the 5 V calculation, not a total patient-current, adapter-leakage or single-fault safety claim. G2 records the other return paths and foreseeable connection errors. The VBUS hardware gate is a separately verified functional inhibit, not isolation. Residual USB/earth-referenced exposure can arise without simultaneous failure of every rule and remains a reason to prohibit skin connection while charging or debugging.

**Required replacement for the supply-gate sentence:**

> WP12 proves the VBUS inhibit in the complete circuit, including digital I/O, all AFE supplies and possible back-power paths, or removes the claimed power-removal credit; no powered-off pin may be driven outside its allowed conditions.

**Gel-bench closing procedure:** remove/disconnect all three skin leads before attaching USB, the debug probe or test equipment; unplug those external connections before attaching electrodes. Check each gel-header path is actually protected, not merely on the side of a drawing described as “behind 220 kΩ.” Use the folded-card stand before the later shell order; a printed stand not yet ordered cannot be the sole S2 provision. A power bank used for off-body charging must have its own charging/input connection disconnected rather than silently operating in mains-connected pass-through. All leakage/fault checks in this review are off-body tests; none is an instruction to connect test equipment to Rolf.

The medial opening, recessed shell and no-wear-without-plug rule may remain engineering choices. They do not close the electrical argument. Its current dimensions, silicone evidence and ligaments remain WP11/WP14 gates. Rolf can accept a clearly described procedural proposal, but his acceptance cannot make an unsupported bound true.

### 24. A qualifying pogo pin exists, but neither the claimed low stack nor the array workspace follows

**Severity: blocker. Sections:** §3; G3d/G5/G7; §5.3; §8. **Continues:** 3/12/17.

**Sentences to change:** “working height about 2.0–2.5”; “a pin landing on brass compresses less”; the sentence beginning “Because a Ø4 disc always contains a point of a 2.0 mm grid”; and “thin will need the contact zone under a lower lid region or will fail.”

**C11 live answer.** There is a stocked gold-contact SMT pin with more than 1 mm travel and an expressly documented stop. It is not a part that fits the assumed low height.

| Candidate | Maximum / recommended / minimum height | Stroke from listed limits | Stop and packaging evidence | Public inventory and price |
|---|---|---|---|---|
| Mill-Max **0919-0-15-20-89-14-11-0** | 9.63 / 8.13 / 6.63 mm | 3.00 mm | Manufacturer explicitly documents a hard stop, SMT termination and minimum 2.54 mm spacing. Gold-plated contact. | [DigiKey exact part](https://www.digikey.com/en/products/detail/mill-max-manufacturing-corp/0919-0-15-20-89-14-11-0/6193088): 12,533 shown in stock; $1.52 at one. |
| Mill-Max **0900-1-15-20-75-14-11-0** | 4.50 / 3.80 / 3.10 mm | 1.40 mm | SMT, gold, Ø1.07 mm plunger, Ø1.83 mm pad layout. A positive internal stop was not authenticated in the pages inspected. | [DigiKey exact part](https://www.digikey.com/en/products/detail/mill-max-manufacturing-corp/0900-1-15-20-75-14-11-0/663499): 29,485 shown in stock; $0.82 at one. |

All table observations accessed 2026-09-17; stock is a displayed observation, not a reservation or JLC assembly-library acceptance. The 0900 family page is [Mill-Max's surface-mount 0900 page](https://www.mill-max.com/products/discrete-spring-loaded-pins/surface-mount-spring-loaded-pin/0900). Do not convert a minimum-height specification alone into evidence of an internal hard stop.

[Mill-Max's 0919 announcement](https://www.mill-max.com/products/new/3-mm-maximum-stroke-spring-loaded-pin), published 2019-09-06 and accessed 2026-09-17, says: **“There is a hard stop incorporated to prevent over compression and minimize the risk of damage to the spring.”** The same manufacturer identifies gold-plated pads/target pins as intended mating surfaces. This is not qualification of bare brass or an oxidized titanium screw tip for this low-level joint. An internal spring stop also does not establish that the PCB, solder joint or printed bosses can withstand the installation load.

The listed 0919 maximum, recommended and minimum heights are **“9.63mm”, “8.13mm”, “6.63mm”** on the linked distributor page. The 0900 counterpart lists **“4.50mm”, “3.80mm”, “3.10mm”**. Neither is the draft's 2.0–2.5 mm working-height example. The 0919 also cannot simply populate the illustrated 2.0 mm pitch: its manufacturer specifies at least 2.54 mm spacing. This review does not claim no shorter qualifying product exists; I did not authenticate one meeting the complete low-height specification.

**Actual height chain.** For the described unrecessed standoff on the inner floor and a parallel rigid PCB:

`outer height = 1.5 floor + 3.0 standoff + Hpin + 1.0 PCB + Htop + 1.0 lid + clearance`.

| Case, zero added clearance | No component over the contact | With an allowed 1.0 mm top component |
|---|---:|---:|
| Draft's hypothetical Hpin = 2.0–2.5 | 8.5–9.0 mm | 9.5–10.0 mm |
| 0900 at recommended 3.80 | 10.30 mm | 11.30 mm |
| 0900 at minimum 3.10, with no compression margin | 9.60 mm | 10.60 mm |
| 0919 at recommended 8.13 | 14.63 mm | 15.63 mm |

These are local stack deductions, not an impossibility proof for all architectures. A component elsewhere still needs the height of the actual common PCB plane; “elsewhere” does not itself lower one portion of a rigid board. Recesses, a changed support, other contact parts or interface II require their own measured arrangement. A lower lid decreases, not increases, the available clearance. The search must use verified part envelopes rather than acquire a pass with placeholder dimensions.

**Compression direction.** With the board fixed and the brass surface 0.5 mm above the screw tip, `Htip = Hbrass + 0.5`. A pin on brass is compressed **more** than one on the recessed tip. A nominal 0.5 mm level difference plus an illustrative ±0.3 mm gap uncertainty already spans 1.1 mm before adding preload and end-stop margins. That example does not assume all print errors are independent; it demonstrates why “at least 1 mm travel” alone cannot prove the combined datum chain. Avoid both loss of contact at the low target and over-compression at the high target.

**The grid proof is insufficient.** The landing is an annulus within a hexagon, not the solid Ø4 disc used in the argument. For a concrete clearance-envelope counterexample, use the published Ø1.07 mm plunger and the plan's idealized Ø2.5 opening. Let the 3 × 3 array centres be `(−2, 0, 2)` in each axis and translate the standoff centre to `(1, 1)`, inside the claimed workspace. The nearest four pin centres are √2 = 1.414 mm from the standoff centre. A whole plunger footprint on brass outside that opening would need at least `1.25 + 0.535 = 1.785 mm`. Those four footprints straddle the opening. The other pin centres are at least √10 = 3.162 mm away, outside even the 2.887 mm circumradius of an ideal 5 mm-across-flats hexagon.

This uses the full plunger footprint as a conservative clearance envelope. It does not prove that all electrical contact disappears: a rounded tip might touch a rim, a thread or the screw. It does prove that the point-grid argument is not a full-footprint brass-landing guarantee. If rim or recessed-tip contact is intended, its contact geometry, force, motion and finish must be qualified as such. Finite array edges, chamfers, actual thread opening, screw-tip form and assembly tolerances are additional exclusions, not free area.

**Required replacement:**

> Interface I is an unqualified candidate until G7 names the standoff and pin, their actual contact surfaces, free/working/minimum heights, travel, stop and force. G5 computes the permitted site region from the finite array and actual landing geometry, with pin footprint and tolerances; no ±1.5 mm region is granted by a point-grid argument. Every possible landed pin, including edge, hole and screw-tip states, must remain mechanically and electrically acceptable. WP11 uses the resulting maximum stack and the complete board support plane. No low working height or workspace is assumed to make the candidate pass.

Add to the joint drawing: count the maximum simultaneously compressed pins, use their force curves rather than “about 1 N” for all products, include PCB/boss deflection and installation travel, and keep all contact-connected metal clear of unrelated copper and the battery. The supplier's current rating or a trace that merely does not go open is not a microvolt motion-noise qualification. Exact standoff availability, thread depth, finish and landing drawing remain G3d evidence; no new standoff SKU was authenticated here.

This is not a requirement to buy or test a pin now. It is a requirement not to freeze the first board against an unsupported workspace and height. Interface II remains possible under its own manufacturing, material, reach and cost gates.

### 25. The ledger takes a component of import duty as if it were the complete reserve

**Severity: major. Sections:** R8/G8; §9; S0/S1. **Continues:** 15/22.

**Sentences to change:** the paragraph taking the higher of JLC's 12.5% and 10% figures for import collection, and “Planning envelope, all in: about $350–560.”

**What is now correct.** The architecture is no longer priced as Economic assembly. The [JLC fee schedule](https://jlcpcb.com/help/article/pcb-assembly-price), updated 2026-09-09 and accessed 2026-09-17, confirms Standard setup $25.56/$51.12 and stencil $8.21/$16.42 for one/two sides. Two-sided setup plus stencil is $67.54. Standard feeder loading is $1.53 per line, not an additional Economic $3.07. The $16.42 rigid-fixture and $1.64 low-quantity X-ray entries are conditional service components, not universally additive or a configured board quote. Keep this corrected basis.

**C13 update: new primary evidence, not just the previous unresolved FAQ.** [CBP CSMS 69326983](https://content.govdelivery.com/accounts/USDHSCBP/bulletins/421d887), sent **2026-07-23**, gives entry guidance effective **2026-07-24**. Under 9903.05.31 it says **“articles the product of China will be assessed an additional ad valorem rate of duty of 12.5%”**, subject to the listed exemptions. Accessed 2026-09-17. The notice identifies this action as Section 301, not the “122” label used by JLC. This supplies post-July primary evidence absent from my preceding review; it does not classify this PCBA or print or establish its final combined September duty.

[JLC's tariff FAQ](https://jlcpcb.com/help/article/us-tariff-policy-faq), updated 2026-09-09 and accessed 2026-09-17, separately lists **“Section 301 Tariffs: 25%”**, regular tariff components and product/material-dependent advance collection. Its 10% merchant figure versus a 12.5% element is not a statement that the complete order has only one of those rates. Nor should every rate mentioned on the page simply be added: classification, exclusions and entry terms must determine applicability.

Therefore `max(10%, 12.5%)` is not a demonstrated conservative total. A complete collection figure from a configured DDP order, or a documented classification-based reserve, is required. The current exact product-level statutory and merchant collection rates remain unsettled. Do not classify the assembled acquisition board as a bare PCB or an IC merely to obtain a convenient rate. Do not add statutory duty again after paying a DDP total that already includes it.

**Budget arithmetic.** The base allowance sum is correct: `160–240 + 50–90 + 80–130 = 290–460`. The conditional kit adds `50–70`, giving `340–530` before any unincluded import collection, freight and tax. [Massachusetts Chapter 64I §2](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleIX/Chapter64I/Section2), accessed 2026-09-17, specifies **“at the rate of 6.25 per cent”**, subject to its rules/exemptions. As arithmetic only, if the high-end $530 were all taxable, tax would be $33.125: **$563.13 before import collection and any additional freight**, already beyond the advertised all-in upper end. The actual taxable base must be determined from the actual purchases; this is not a tax assessment.

Pin-array quantities also belong in the populated-board BOM. Three 3 × 3 arrays mean 27 pins per populated board, 54 for two or 135 for five. For illustration only, the linked 0900 distributor price breaks are $0.6248 at 50 and $0.5949 at 100: those quantities would cost about $33.74 or $80.31 before fees/shipping. That is not a selected Elicio part or an addition to an already itemized quote; it illustrates why “parts” must reflect the actual array rather than three contacts. A single feeder line does not mean three physical pins.

**Required replacement:**

> Before S1, the ledger uses the selected population and assembly services, every shipment, applicable sales/use tax and complete import collection for each China-origin order. A percentage for one trade-remedy component is not the total import reserve. Mark each line as quoted, catalog-priced or allowance, with included freight/duty/tax identified to prevent double counting. Include the full conditional programming kit when needed. Reserve the shell's complete delivered maximum before paying for the board; if an adequate supported reserve cannot be established, G8 is not passed. Delete the $350–560 all-in claim until the same ledger reproduces it.

The whole-project reserve mechanism itself is accepted. A $90 shell cap is a spend limit with a stop consequence, not evidence that the selected finished shell can be obtained for $90. US alternative assembly and printing routes remain quote-only. No configured quotation or exact delivered total was obtained in this review.

## Conditional closures: live checks and exact sentence corrections

### Charger, TS, termination and harness — findings 2/10/18

[TI BQ25100 Rev. C](https://www.ti.com/lit/ds/symlink/bq25100.pdf), printed p.3, accessed 2026-09-17: **“If NTC sensing is not needed, connect this pin to VSS through an external 10-kΩ resistor.”** This supports the fixed-TS configuration; it is different from floating TS. Pages 3/6 distinguish the 4.20 V BQ25100 from other family regulation voltages and list the 1 mA minimum absolute termination current. The exact ordering code remains essential.

Using the page-6 maximum ISET factor 145 AΩ and an illustrative 6.8 kΩ, 1% resistor gives `145/(6800 × 0.99) = 21.54 mA`, below 40 mA. The typical-factor result is about 19.85 mA. These are setpoint calculations, not a complete charge-profile test. G1 still includes voltage accuracy, PRETERM, timers, startup behavior, the actual parallel system load and the datasheet's low-current application provisions.

The [Data Power specification](https://cdn.sparkfun.com/datasheets/Prototyping/SPE-00-301120-40mah-en-1.0ver.pdf), version 1.0, 2015-11-06, printed p.4, accessed 2026-09-17, lists **“1C (40mA)”** as maximum continuous charge and 0.01C as the endpoint. For 40 mAh that endpoint is 0.4 mA. Earlier termination at a higher current does not by itself establish an unsafe charge; it does mean capacity under the new profile is unmeasured. A fixed TS resistor does not sense cell temperature, and a procedure must not claim that it does.

Replace **“recorded with the capacity it forgoes”** with:

> G1 records the selected termination profile and its acceptance for the exact pack. Any change in delivered capacity/runtime is unknown until characterized; no numerical capacity-loss claim is inferred from termination current alone. The temperature limit is an operating restriction, not automatic cell-temperature protection.

The harness gate is justified more strongly than the red-wire step suggests. [SparkFun's current product page](https://www.sparkfun.com/polymer-lithium-ion-battery-40mah-jst-sh.html), accessed 2026-09-17, still says **“JST-SH connector - 2mm spacing between pins”**. The linked legacy drawing, printed p.9, labels **“JST-PHR-2PIN”** and visibly labels **“(+)Black”** and **“Red (−)”**. This is inconsistent documentation, not proof of the connector or polarity on a delivered pack. It specifically prevents using a red-wire convention as verification.

Replace assembly step 6 with:

> Mate only the G1b-qualified pack and connector revision. Before plugging it into the board, verify electrical polarity at the identified connector contacts using the specified off-body method or documented supplier test; neither keying nor insulation colour proves polarity. Include any meter or no-solder test adapter in R2b and the ledger.

No cutting, stripping or retermination by Rolf is introduced. The current pack drawing, maximum harness envelope and permitted Massachusetts delivery route remain conditions before PCB release.

### Undervoltage — findings 9/19

The minimum AFE supply and PCM cutoff are no longer being conflated. Keep the separately calculated supply/load margin. Correct the ambiguous shutdown direction rather than reopening the whole power architecture.

Replace the undervoltage sentence with:

> Inhibit acquisition when the monitored voltage falls to V_STOP, chosen with sensing error, response latency, regulator/load transients and the pack's normal discharge endpoint so the AFE remains valid until shutdown. Resume only above V_START > V_STOP after the specified rail/reference settling checks. Report invalid samples and the stop/restart reason. The 10-second battery telemetry cadence is not the protective monitoring cadence.

G2's off-state I/O/back-power treatment under finding 23 also applies here. WP12 may implement a conservative firmware threshold if its response is demonstrated to meet the stated bound; this review does not mandate a new supervisor solely because the threshold value is still a work-package output. A completed threshold and restart contract is required before S0.

### Acquisition and frame contract — findings 8/20

[TI ADS1292 Rev. C](https://www.ti.com/lit/ds/symlink/ads1292.pdf), Table 4, printed p.16, accessed 2026-09-17, lists 2000 SPS with 524 Hz −3 dB bandwidth at gain 12. The rate supports the requested analysis band. The draft's nominal 24.04 nV/code and ±201.7 mV full-scale arithmetic is correct; it is not a claim of effective resolution or flat frequency response. The DC-preserving ±50 mV criterion and separate transport loss are appropriate remedies.

The frame prose refers to a frame sequence, gain and reference although its initial field list omits them. A sample counter incremented only for successful reads would also hide missed conversions. Sixteen bits at 2000 SPS wrap every **32.768 s**. These are implementation definitions that G6 must freeze, not reasons to increase the sample rate again.

Replace the abbreviated frame sentence with:

> Before S0, WP13 freezes a byte-level versioned format containing session/epoch identification, frame sequence, acquisition index tied to conversions rather than only successful reads, sample count and payload length, gain/reference/rate metadata, defined ADS status handling, and fragment identification/reassembly rules. It specifies counter wrap, reconnect/reset, partial-frame rejection and separate acquisition-overrun versus transport-loss reporting. Receiver fixtures cover all of those cases.

N may adapt to negotiated payload size, but its meaning must be transmitted or fixed by the version. Preserve the named analysis filters/windows, startup exclusions and the original rail-or-flat duration definition in protocol v2. Decide explicitly whether run duration counts sample intervals or samples; do not change a physical 100 ms threshold accidentally. Applying old amplitude criteria to a different transfer function must be an explicit per-line protocol decision, not an assertion that unit scaling alone makes chains identical.

### First-load kit, pin map and recovery — findings 11/21

The fallback is now a plausible no-solder kit. [Tag-Connect TC2030-IDC-NL](https://www.tag-connect.com/product/tc2030-idc-nl), accessed 2026-09-17, lists $33.95. Its [Rev. B cable drawing, sheet 2](https://www.tag-connect.com/wp-content/uploads/bsk-pdf-manager/2019/12/TC2030-IDC-NL-Datasheet-Rev-B.pdf) maps TAG contacts 1–6 one-for-one to IDC contacts 1–6. It does not assign Elicio's target signals. The connector/footprint views and key orientation must be followed, not guessed from wire order.

[Raspberry Pi's Debug Probe documentation](https://www.raspberrypi.com/documentation/microcontrollers/debug-probe.html), accessed 2026-09-17, says **“The probe operates at 3.3V nominal I/O voltage.”** It includes a male 0.1-inch breakout cable suitable for a female IDC endpoint. On the D port, orange SC is SWCLK, yellow SD is SWDIO, and black is GND; establish common ground before signal connections. This supports a candidate connection, not the draft's unverified target-voltage compatibility assertion.

One explicit **proposed project assignment**, not an observed Elicio PCB pinout or a universal Tag-Connect signal convention, is:

| TC2030/IDC contact | Target assignment to put in the released schematic | Debug Probe connection |
|---|---|---|
| 1 | Target-voltage sense/test point | No probe connection; do not use it as a power feed |
| 2 | SWDIO | D-port yellow SD |
| 3 | GND | D-port black, connected first |
| 4 | SWCLK | D-port orange SC |
| 5 | GND | No additional probe lead required |
| 6 | nRESET, also connected to the recovery switch as designed | No probe lead in the three-wire kit |

WP12/WP15 may choose another assignment, but the target footprint, IDC view, sheet and netlist must agree. The target is independently powered off-body, with electrodes disconnected. A 3.0 V label is not evidence that every 3.3 V probe output and target input is compatible at worst case. Replace that assertion with:

> G4 verifies both directions of the probe/target I/O limits at the actual powered target voltage, the exact numbered net map and ground-first connection. If the selected rails do not meet the limits, change the programming voltage arrangement or include a qualified interface; do not infer compatibility from nominal voltages.

[Adafruit's bootloader repository](https://github.com/adafruit/Adafruit_nRF52_Bootloader), accessed 2026-09-17, documents **“Reset twice within 500 ms will enter DFU with UF2 and CDC support”** for nRF52840. It distinguishes merged bootloader/SoftDevice provisioning from flashing the bootloader alone; application addresses depend on the selected SoftDevice version. Thus the tactile-switch remedy is coherent. The release must still pin the board build, merged image, application/linker layout and update/recovery tests. Naming nRF Connect SDK does not itself demonstrate compatibility with that reserved map, but it is not proof of incompatibility either.

The [JLC capability page](https://jlcpcb.com/capabilities/pcb-assembly-capabilities), accessed 2026-09-17, still states **“we partially support this programming service”** for Standard assembly. A target-specific two-board SWD job, fixture, verification scope and price were not authenticated. That route remains quote-only, with owner authorization required; no new quotation is demanded during this turn. [Adafruit's probe page](https://www.adafruit.com/product/5699), accessed 2026-09-17, lists $12, so the named cable and probe alone total $45.95 before delivery and other necessities. A paper rehearsal establishes completeness, not measured physical completion time.

## What stays not settled

| Item | Required closing evidence |
|---|---|
| R7 proposal and electrical states | Correct per-path versus system/fault claims, complete off-state/back-power diagram, gel-bench disconnect procedure, off-body tests; then the owner's informed decision on the accurately described proposal |
| Contact architecture I or II | Orderable standoff/pin or flex specification, actual landing region, contact-height/force/tolerance stack and support proof, surface/continuity/motion qualification; no unsupported workspace before the board purchase |
| Actual packaging and port | Measured populated-board/support planes, routed harness, connector orientation, medial opening/ligaments/plug and end-face fallback, owner measurements; G5 must not pass with provisional pin boxes |
| Charger and harness | Exact BQ variant/networks and pack revision; charge profile, procedural temperature limits, system-load/termination behavior; reconciled connector and electrical polarity evidence |
| Acquisition validity and transport | Shutdown/restart thresholds and latency; complete byte schema, counters/reassembly fixtures and protocol-v2 mapping before S0 |
| Factory or owner programming | Accepted factory service/price or released kit map, voltage proof, board-specific image/linker arrangement and accessible recovery |
| Delivered budget | Actual quantities and services, full import collection or supported reserve, each shipment and applicable tax, conditional kit and shell delivered cap; no invented product-specific duty or configured quote |
| Materials and final mechanical acceptance | R3's process/finish evidence or limited-evidence owner decision, skin-facing silicone evidence, actual standoff/screw finish, new closure/hook and first-assembly inspection; no inheritance of a gauge pass |
| Owner inputs | M1–M8, complete-project ceiling, colour/appearance, confirmed delivery address/origin preference, objective order and the revised residual-risk proposal |

## Stop-rule assessment: substantive, not cosmetic

The remaining disagreements are substantive. Finding 23 changes the electrical claim presented for owner acceptance and the conditions under which the supply gate works. Finding 24 changes the board's required height, purchased contact components and guaranteed site adjustment. Finding 25 changes whether the first spend actually fits the complete-project ceiling. None is a request for another round over typography, an accepted design preference or an already-closed source lookup.

The other corrections are bounded conditions within existing work packages: precise undervoltage wording, explicit frame fields, measured rather than asserted programming time, and the completed numbered cable map. They need to appear in the final release contracts, but do not independently justify demanding another planning round or physical experiments now. The false “lower lid” wording must be fixed along with the substantive stack correction. No new research lane, unauthorized vendor inquiry or hardware purchase is necessary to revise these contracts.

## For Rolf

Do not order this revision yet. The procedural charging approach can be stated honestly, and a real gold-plated spring-loaded pin with a hard stop exists. The remaining problem is integration: 23 µA is not an overall USB/body-current safety bound, the example array has not proved its landing workspace, and the real pin heights materially change the enclosure budget. The import reserve also needs the complete applicable charge, not one percentage selected from a list.

Keep the thin comparison, the single-order/no-hidden-spend rule, the custom assembled-board route and the corrected separation of development from release checks. The next revision should resolve those three bounded issues and carry the already-defined charger, harness, firmware and programming conditions into their release gates. It does not need to restart the project or collect wear data to answer this review.

Only this review file was written. No prior turn, plan, code or design record was modified. No supplier was contacted and no order or design upload was made.

NOT SIGNED OFF
