# WP17b — Research v4: the probe, the cell in ones, the assembler's fees (lane w5, web only)

Read `tasks/phase1-common.md` first. Lane `w5`, worktree
`/home/user/projects/elicio/.worktrees/w5`, branch `lane/w5`
(fast-forwarded to `main` at the round 5 merge). Start line (coordinator
restarts you by copy-paste; the `--conversation` id is optional and only
keeps your context):

    herdr agent start w5 --kind agy --pane <pane> --parent w1B:p1 -- --dangerously-skip-permissions --add-dir /home/user/projects/elicio --effort high --model gemini-3.8-flash-high

Why: round 5's decisions left facts to find (`docs/fab/open-questions.md`
Q55, Q60, Q63, Q64, Q65, Q67, Q68; `tasks/reviews/code-r5.md` decisions
57 to 68 and defects 28 to 35, which retagged several of your round 5
numbers UNVERIFIED because the quote was not on the page). You search the
web and report. You design nothing, contact nobody, buy nothing, request
no quote, sign up nowhere, upload nothing, and never put anything in a
cart. A number without its sentence on the page is UNVERIFIED, not
paraphrased; that rule cost you six retags in round 5.

Owns: `docs/fab/L7-research-v4.md` (new). Nothing else.

Deliver `docs/fab/L7-research-v4.md` with these sections, every number
with URL, date read, and a verbatim quote, or UNVERIFIED with the search
tried:

1. **First-load probe (Q64).** The nRF52840 runs its GPIO at 1.8 V until
   REGOUT0 is set. For each of: SEGGER J-Link EDU Mini, Black Magic Probe
   (native or a stocked clone), Raspberry Pi Debug Probe, an ST-LINK V3
   MINIE: the target-voltage range or VTref sensing statement, the
   licence terms that matter for a private prototype (J-Link EDU), price
   and stock at one US seller, and whether the vendor's software runs on
   macOS (Apple silicon). Also: does the Adafruit bootloader or pyOCD set
   REGOUT0 on first flash (the source or docs sentence), and the nRF52840
   product specification's absolute maximum on a GPIO relative to VDD.
2. **A cell in ones (Q55).** A 501015-class LiPo pack (about 5.0 × 10 × 15
   mm, 40 to 60 mAh, with protection and a 2-pin lead) sold in single
   units by a seller with a page price, displayed stock and a drawing or
   dimensioned photo: Adafruit, SparkFun, DigiKey, Mouser, PowerStream,
   Tinycircuits, Pimoroni, Seeed. Report each candidate's dimensions with
   protection, capacity, max charge rate, connector and wire gauge as the
   page states them.
3. **JLC fees you can read** (Q60, Q67, Q65): the FPC assembly page's
   stiffener wording (count-based fee, thicknesses offered), the flex
   fixture fee, the consignment (customer-supplied parts) page and its
   fees, the global sourcing page's statement about quoting, the parts
   library's tier fee sentences; only what the pages say without a login.
4. **Component facts** (Q63, Q68, Q65): the LCSC pages for the board's
   BOM lines that `board-v2.md` §13 marks UNVERIFIED (read the list from
   `git show main:docs/fab/board-v2.md`), each with number, displayed
   stock, tier and price; the ADS1292 datasheet's decoupling sentence;
   the BQ25100's termination-current and pre-charge sentences and the
   sentence on system load during charge; the TLV71330's quiescent and
   dropout lines.
5. **Shell colour and finish (Q30).** JLC3DP's MJF PA12 colour options and
   the finish names as the configurator page lists them, plus any price
   difference the page states; the same for Xometry.
6. **E73 drawing, one more try.** The Ebyte E73-2G4M08S1C mechanical
   drawing (antenna keep-out) from Ebyte's own site or a distributor's
   PDF; if unreachable again, say where you looked.

Report `.reports/WP17b-report.md` (untracked): what each section found,
what stayed UNVERIFIED, "Needs a decision", the final commit sha. Commit
in steps; the last commit is `research(v4): probe, cell in ones, fees`.
Gates: `git status --short` empty; every number in the file has a quote
or UNVERIFIED (grep your own file). Closing steps per the common file with
`<PKG>` = `WP17b`, `<lane>` = `w5`.
