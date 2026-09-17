# Open questions after each round

Numbered items raised by round reviews of the fabrication plan
(`plan.md`, signed off at `0c5d0eb`). The plan stays the spec. Each item
records the reading the build follows until Rolf rules otherwise, who
closes it, and its status. New items append; numbers never change.

## Round 1 (review `tasks/reviews/code-r1.md`, merged 2026-09-17)

| # | Question | Reading the build follows | Closes it | Status |
|---|---|---|---|---|
| Q1 | Chord gate `>` (plan §3.3 table) or `≥` (plan §1, §2 row 17, §10) | `M1 ≥ TOTAL_CHORD + 3`; a 0.01 mm difference is below caliper resolution; the script and `measure.md` use ≥ | plan erratum, coordinator | decided |
| Q2 | HOOK_RADIUS: plan writes `M8 + HOOK_DIA/2 + 1.0` but quotes 13.5 at M8 = 11, which needs `+ 0.75`; the plan's form fails its own `< M8 + 1` bound | `M8 + HOOK_DIA/2 + 0.75`, strict `<`; 13.5 is the number every other document was built on | plan erratum, coordinator | decided |
| Q3 | Hook joint fillet 2.0 (§3.5 step 9) does not build: 1.5 on full p15, 1.75 on thin p15 and full p25, less at high bow | Largest radius that builds, recorded per body in `manifest.json` notes and on the WP3 drawing; it is strain relief, not a fit feature | Rolf may override at render approval | decided, provisional |
| Q4 | Lip root fillet 0.5 (§3.5 step 7) overlaps the seated body by 0.045 mm³ | 0.2 mm; E5 is an experiment the closure test decides | closure test (3.7 item 7) | decided |
| Q5 | Hook start at −5° sat inside the battery cavity; the reviewer cuts it back (4.6 mm³ at bow 3, about 20 at bow 8) | Cut it: the cavity is air by definition; the hook root outside is unchanged | none | decided |
| Q6 | Nut metal inside the cavity. Plan §4 allows plated steel or tinned copper; no plated-steel DIN 439 M2.5 found; 18-8 stainless is nickel-bearing and outside the text; titanium DIN 934 has zero stack margin at wall +0.3 | No purchase happens before S1, so nothing is blocked. Before S1, WP5 part 2 looks for a brass or tinned-brass DIN 439 M2.5 thin nut (nickel-free, stocked) as a candidate inside the plan's spirit, and shows its drawing. Rolf picks the metal | **Rolf** (interface §12 V2-3) | open |
| Q7 | Dome dimensions have no SKU drawing (interface §12 V2-1) | CAD keeps 4.7 × 1.35; the internal stack does not depend on the dome; a purchased SKU's drawing becomes interface v2 or v3 | WP5 part 2, before S1 | open |
| Q8 | LID_EDGE 0.8 not applied on the top edge at the lip so the lip keeps its full joint | Accept | none | decided |
| Q9 | Plan §3.1's single-variant command writing into `v1/` is refused by the stale-part guard | Keep the guard; single-variant builds go to a separate `--out` as the README says | plan erratum, coordinator | decided |
| Q10 | Lid emboss bytes depend on the Arial that OCCT finds on the machine | Vendor an open-licence font in the repo and point the emboss at it, so regeneration is machine-independent; WP3 (lane w2, round 2) does it | WP3 | assigned |
| Q11 | Emboss 0.8 reaches below the lid underside into the 0.4 mm module headroom (plan §5) | Fine for the gauge. WP6 records the lid-underside constraint in interface v2; WP8 makes the order 2 emboss 0.4 or moves it over the battery zone | WP6 records, WP8 builds | assigned |
| Q12 | Carried: packing shortfall (interface §12 V2-4) and requirement 5 wording (stainless versus titanium) | Packing is WP6's round 2 package; requirement 5 is Rolf's, outside the plan | WP6; **Rolf** | open |

## Round 2 (review `tasks/reviews/code-r2.md`, merged 2026-09-17)

The reviewer numbered its decisions 13 to 19; these are Q13 to Q19.

| # | Question | Reading the build follows | Closes it | Status |
|---|---|---|---|---|
| Q13 | Signal lug tab "3 × 7 × 1.5 from the cylinder toward the pad" (interface §3.1): read literally the tab runs past its own pad, through the side wall for CONTACT_2, and into other nets' margins; free area 69.4 mm² literal versus 87.0 if the tab ends under its pad | The tab ends under its own pad; its real length and direction come from the lug drawing (TE 31428 or the SKU WP5 picks), which WP5 part 2 supplies. WP6 round 3 lays out on that reading | WP5 part 2 drawing; **Rolf** confirms or keeps 7 mm | decided, provisional |
| Q14 | What plan §5's "≥ 5 mm from the battery" measures: module body 4.70 (cell packed to the hook) or 4.30 (on the rib); antenna no-copper zone 16.70 | The rule protects the antenna, so it passes; "cell packed to the hook end, foam toward the rib" becomes an interface rule | none | decided |
| Q15 | Packing escalation (plan §10 Open for Rolf item 6, reopened): VQFN-32 plus two diode arrays need 79.3 mm² against 69.4 free; no array site within 10 mm of its pads | Rolf's choice by the plan. Under Q13's reading, WP6 round 3 lays out options B (+3.5 mm length), C (+3 mm width) and E (passives on the lateral face outside the module, not in plan §5) with areas, pad and tab positions, and a recommendation; no shell change until Rolf sees that sheet | **Rolf**, after WP6 round 3 | open |
| Q16 | Plan §3.3 LEAD_PADS SIG1 s 26.5 breaks its own 0.5 mm margin (pad edge 4.00 against 4.05 required) | 26.6 per interface v2 (plan §10 gives WP6 the final pads); plan erratum; likely moot after round 3 | plan erratum, coordinator | decided |
| Q17 | Reference site against M6: at the default M6 = 15, CONTACT_REF lands about 6.5 mm in front of the mastoid bump if the body's front edge sits in the crease | Rolf's gauge wear answers it: montage §2.2 step 6 records whether the mark is on bone and the M6 offset. If not on bone, CONTACT_REF moves by the measured offset as an interface change before order 2 | gauge wear (plan §3.7 item 9), then interface v3 | open, waits on order 1 |
| Q18 | Cell pack: no published 501015 pack fits folded; the DNK in-line pack is 17 ± 1 long and its drawing is preliminary; the plan's hand fold has 0.3 to 0.5 mm for PCM and Kapton | The plan's fold on the lateral face stands as the design. One cell is bought with the Stage A parts and its folded thickness measured; the +2.4 mm pocket is WP8's fallback and moves the M1 gate, which the interface states. No cell purchase on a preliminary drawing | measurement on a real cell; **Rolf** buys it | open |
| Q19 | The PROPOSED numbers in `montage.md` §3 (5 µV RMS, 45 µV, 3:1 flex, 10:1 clench, 70 % ratio, 100 ms dropout, ±0.5 V at the INA128 output, 9 of 10, 0.20 per minute eating, 0 talking and walking, the yawn and smile counts) | Frozen as proposed. The file's own rule allows one revision from Stage A gel data before the first dry recording, with a dated row. Rolf may edit them earlier | **Rolf**, before S1 | open |

## Round 3 (review `tasks/reviews/code-r3.md`, merged 2026-09-17)

The reviewer numbered its decisions 20 to 23; these are Q20 to Q23.

| # | Question | Reading the build follows | Closes it | Status |
|---|---|---|---|---|
| Q20 | Packing: on the real TE 31428 lug with leads that can leave their barrels, only option C closes (BODY_WIDTH 17 → 20, board 19 × 15.5), with the lead pads moved to SIG1 (7.5, 29.35), SIG2 (13.5, 21.35), REF (5.5, 29.35) and one reference-over-SIG1 wire crossing on the floor where nothing sits above it | Rolf's pick from `docs/fab/packing-options.md`. Coordinator's reading: C, with the crossing (the plan does not forbid one; the alternative is a 2 mm lead bend against the plan's 3). WP8 starts on the line "I pick C". Closes Q15 | **Rolf** | open |
| Q21 | Reference lug in the tail pocket: TE 31428 upright is 1.96 thick against the plan's 1.5 envelope, reaches about y 8.2 against the lid at 8.0 when bent at the ring edge, and its wire would leave pointing at the lid | Before order 2, bend the tab toward the axis over the Kapton at a smaller radius and check it as installed geometry (plan §10 already requires that check); WP8 sizes the pocket to the real lug. Changing KEEPOUT_REF in plan §3.3 is Rolf's | **Rolf** (plan §3.3), before order 2 | open |
| Q22 | Signal lug barrel height: 1.96 mm across against the plan's 1.5 mm tab envelope; the barrel tops at y 3.46 under the board at 4.3 | Plan erratum: the flat-tab envelope height becomes 2.0 for WP8's keep-out solids; the placement already keeps parts and copper off the barrel strip, so option C does not change. Rolf may instead ask WP5 for a flatter barrel | plan erratum, coordinator; Rolf may override | decided |
| Q23 | 28 AWG wire in TE 31428's 26 to 22 AWG barrel (carried from round 1) | Fold the strip and solder the crimp, as the assembly sheet says; acceptable for a bench prototype. WP5 keeps looking for a 28 AWG barrel of similar length at purchase time | Rolf accepts, or WP5 at purchase time | open, low |

## For Rolf

Plan §10 "Open for Rolf" items 1 to 10 stand. From round 1, in addition:

- Q6 nut metal (before S1, not before order 1).
- Q3 accept the built hook fillets when approving the renders.
- Requirement 5 wording (Q12).
- Buying the Stage A parts (`docs/STAGE_A_PARTS.md`) gates WP7a part 2 and
  order 2; add one 501015 cell to that order for Q18.
- Q13 confirm the short lug tab, or keep 7 mm and the pads move.
- Q20 pick the packing option from `docs/fab/packing-options.md` (only C closes); this closes Q15.
- Q21 the reference lug in the tail pocket, before order 2.
- Q23 accept fold-and-solder for the 28 AWG lead in the 26 to 22 AWG barrel.
- Q17 after wearing the gauge: is the reference mark on bone.
- Q19 accept the frozen protocol numbers, or edit them before Stage A data.
