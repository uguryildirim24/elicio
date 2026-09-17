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

## For Rolf

Plan §10 "Open for Rolf" items 1 to 10 stand. From round 1, in addition:

- Q6 nut metal (before S1, not before order 1).
- Q3 accept the built hook fillets when approving the renders.
- Requirement 5 wording (Q12).
- Buying the Stage A parts (`docs/STAGE_A_PARTS.md`) gates WP7a part 2 and
  order 2.
