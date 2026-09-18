# WP17 — Research v3 for the build rounds (lane w5, web only)

Read `tasks/phase1-common.md` first. Lane `w5`, worktree
`/Users/rolfie/projects/elicio/.worktrees/w5`, branch `lane/w5`. Start
line (coordinator restarts you by copy-paste):

    herdr agent start w5 --kind agy --pane <pane> --parent w1B:p1 -- --dangerously-skip-permissions --add-dir /Users/rolfie/projects/elicio --effort high --model gemini-3.8-flash-high

First: `git merge --no-edit main` in your worktree (your branch carries
WP10's commit `832ef28`, which main does not have yet; the merge adds
plan v2 and the new briefs).

Why: plan v2 (`docs/fab/plan-v2.md`, signed off at `ef369bd`) leaves claims
C1 to C16 and gates G1b, G3, G4 and G8 waiting on facts from live pages.
You search the web and report. You design nothing, contact nobody, buy
nothing, request no quote, sign up nowhere, upload nothing, and never put
anything in a cart. Configured-price pages that need a login or an upload
are named as such and left.

Owns: `docs/fab/L6-research-v3.md` (new). Also fix two identifiers in your
own `docs/fab/L5-research-v2.md`: the E73-2G4M08S1C LCSC number is
C356849 (not C474779) and the Seeed XIAO nRF52840 charge-current pin is
P0.13 (not P0.17); cite the pages you re-read. Nothing else.

Deliver `docs/fab/L6-research-v3.md` with the sections below. Every number
carries the page URL, the date you read it, and a verbatim quote of the
sentence it came from, or the tag UNVERIFIED with the search you tried.
Never paraphrase a number into a quote.

1. **Cell harness (G1b).** SparkFun PRT-25270: what connector the current
   page says, what the current drawing says, pin pitch, wire gauge, lead
   length; the Data Power DTP301120 sheet's connector, if any; JST SH and
   PH 2-pin receptacle part numbers stocked at LCSC with numbers and
   displayed stock.
2. **Standoffs (C14).** Harwin R25-1000402 at DigiKey and Mouser (stock,
   price at 1 and 10, hex across flats as each page and the drawing
   state); Spacer Express LAI-FF-M2.5-SW5-L3-100 shipping to the USA if the
   page states it; any stocked 3.5 mm M2.5 female brass hex standoff, 5 mm
   across flats; nickel plating thickness and any top-face tolerance on
   those drawings.
3. **Contact alternatives (C16, research only).** SMD grounding spring
   contacts (Harwin S17xx and S7121 families, Würth WE-GSC): working
   height, travel, force, contact tip size, plating, LCSC or DigiKey
   stock. Report, do not recommend.
4. **Assembler facts (G3, G8).** JLCPCB standard PCBA: minimum assembled
   quantity, 4-layer 1.0 mm ENIG stackup page, which of ADS1292IRSMR,
   BQ25100 variants, TLV713-class LDOs, the Raytac MDBT50Q-1MV2 and the
   E73-2G4M08S1C are in the JLC parts library (number, basic or extended,
   displayed stock, price); the programming service page (price per board
   if published); the DDP tariff FAQ as it reads today. US alternatives
   (MacroFab, Screaming Circuits, OSH Park + hand assembly) with only what
   their public pages state.
5. **Shell finish (C1).** JLC3DP MJF PA12 finishes (grey, dyed black,
   vapour smoothing if offered) with prices as displayed; the skin-contact
   or biocompatibility statements those pages make, quoted; Xometry's
   equivalents.
6. **First load (G4).** Raspberry Pi Debug Probe: I/O voltage statement
   and target-voltage limits from its documentation; Tag-Connect
   TC2030-IDC-NL page and drawing; Adafruit nRF52840 bootloader latest
   release page, the double-reset statement, and any statement about
   custom-board variants.
7. **Materials (R3).** Grade 5 titanium ISO 7380 M2.5 button heads: the
   Sortafast page as it reads today plus one alternative seller; a
   skin-contact statement for PA12 MJF from HP's own material page.

Report `.reports/WP17-report.md` (untracked): what each section found,
what stayed UNVERIFIED, "Needs a decision", the final commit sha. Commit
in steps; the last commit is `research(v3): facts for the build rounds`.
Gates: `git status --short` empty; every number in the file has a quote
or UNVERIFIED (grep your own file). Closing steps per the common file with
`<PKG>` = `WP17`, `<lane>` = `w5`.
