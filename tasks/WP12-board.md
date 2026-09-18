# WP12 — Board v2: KiCad project, release job, G2/G4 records (lane w2)

Read `tasks/phase1-common.md` first (for this package "the plan" is
`docs/fab/plan-v2.md`, signed off at `ef369bd`), then plan v2 §1, §2 R7,
§4 G1 to G7, §5 all, §6 (frame and pins only), §8 (first-load map), §11
row 12, §12 claims; `docs/fab/open-questions.md` Q37 to Q49;
`docs/fab/interface.md` §6 (module keep-out, site coordinates);
`docs/fab/contacts.md` §8 (the 220 kΩ paths); the research file
`git show lane/w5:docs/fab/L5-research-v2.md` (unreviewed; two identifiers
were corrected in plan v2's header). Lane `w2`, worktree
`/Users/rolfie/projects/elicio/.worktrees/w2`, branch `lane/w2`. Start
line (coordinator restarts you by copy-paste):

    herdr agent start w2 --kind cursor --pane <pane> --parent w1B:p1 -- --model cursor-grok-4.6-xhigh --force

First: `git merge --ff-only main` in your worktree (your branch is behind).

Why: plan v2 replaces the breadboard bench with one custom board assembled
by the vendor. This package builds the board's design record and its
release job so that the schematic is complete and checked before WP11's
outline and G7's joint analysis decide the layout. Nothing is ordered,
quoted or uploaded. You contact nobody.

Tooling: KiCad is not installed. Install it with `brew install --cask
kicad` (10.0.6, free, no account; record download size and time in your
report). Everything the release job needs runs through `kicad-cli`. If the
install fails, push WAITING with the error.

Owns: `hardware/board/` (new: `elicio-v2.kicad_pro`, `.kicad_sch`,
`.kicad_pcb`, `lib/` symbols and footprints, `release/.gitignore` for
generated files), `scripts/board/release.py` (new), `docs/fab/board-v2.md`
(new), `tests/test_board_release.py` (new). Nothing else.

Circuit contract (from plan v2; each value traced to its sheet in
`board-v2.md`, page and date, or marked UNVERIFIED):

- Module: Raytac MDBT50Q-1MV2 footprint placed, per Raytac's spec (Q42);
  the E73-2G4M08S1C footprint in `lib/`, unplaced, with a pin-mapping table.
  RF no-copper polygon per `interface.md` §6.3 and the module sheet.
- Front end: ADS1292 (non-R) VQFN-32, AVDD = DVDD from a 3.0 V LDO on the
  battery (name the LDO, dropout and quiescent traced); internal 2.42 V
  reference; SIG1 and SIG2 to one channel through 220 kΩ each; the REF
  contact to the RLD output through its own 220 kΩ; lead-off components
  present but off by default; decoupling per the datasheet's typical
  circuit; SPI plus DRDY, START, RESET, PWDN to the module.
- Supply gate: a P-channel high-side switch on the front end's supply,
  off when VBUS is present, gate driven so the default state with an
  uncooperative MCU is "front end off while VBUS present"; body diode
  orientation and every path that could back-power the front end (SPI
  lines, pull-ups, RLD, the gel header) listed in the G2 table.
- Charger: BQ25100-family 4.20 V variant, exact ordering code; ISET for
  about 20 mA (about 6.8 kΩ, computed from the sheet's equation); PRETERM;
  TS 10 kΩ to VSS; timers on; the parallel system load during charge
  computed; VBUS detection to an nRF pin through a divider; charge status
  to an LED and an nRF pin from the actual pins.
- Battery: a divider with an enable for the 10 s telemetry and the
  protective monitor; the undervoltage numbers V_STOP and V_START computed
  per §5.5 (sensing error, latency, LDO dropout, transients, the pack's
  discharge endpoint) and written as named constants for WP13.
- Cell connector: JST-SH 2-pin placed (SparkFun's page), JST-PH 2-pin in
  `lib/` as the G1b alternate; polarity marked in silkscreen against the
  connector's contacts, not a wire colour.
- USB-C: 16-pin receptacle, USB 2.0 only, 5.1 kΩ on CC1 and CC2, ESD on
  D+/D− and VBUS; recessed medial placement is WP14's, you place it at the
  board edge WP11 names or, if `git show lane/w1:docs/fab/packing-v2.md`
  does not exist yet, at the provisional edge and say so.
- Debug: Tag-Connect TC2030 footprint (NL, no legs) with the §8 net map
  (1 VTref sense with no power feed, 2 SWDIO, 3 GND, 4 SWCLK, 5 GND,
  6 nRESET); tactile switch 4.5 × 4.5 × 1.6 on nRESET; the 3-pin 2.54 mm
  right-angle bench header (SIG1, SIG2, REF) behind the 220 kΩ.
- Contacts: three 8 × 8 exposed ENIG pads on the bottom copper, nets
  SIG1, SIG2, REF, each net clear of all other copper within 1.0 mm, at
  the interface v2 site coordinates as provisional positions; two or more
  M2.5 mounting holes for the bosses, clear of the pads; a note that the
  pads' final positions come from WP11/G5.
- Stackup and rules: JLCPCB 4-layer 1.0 mm ENIG, their published stackup
  and capability limits quoted with URL and date, encoded as the DRC
  rules; 0402 minimum passives; standard-tier parts preferred; every part
  a catalogue line with the LCSC number read on its page (URL, date,
  price, stock as displayed, "basic/extended") or UNVERIFIED. No cart.

Deliver:

1. The KiCad 10 project with the schematic complete, ERC at 0 errors and
   every warning explained in `board-v2.md`, footprints assigned, parts
   placed on a provisional outline (WP11's if it exists, else 17 × 33 mm
   stated as provisional). Routing is not required this round; DRC runs
   and its unrouted count and errors are reported honestly.
2. `scripts/board/release.py`: runs `kicad-cli` ERC and DRC (JSON), BOM
   and CPL in JLC's column format, gerbers, a STEP export, and a
   `release/summary.json` with counts; exits non-zero on any ERC error or
   any missing output (fails closed, plan §5.1). `tests/test_board_release.py`
   runs it and asserts ERC 0, summary present, BOM rows equal placed parts;
   if `kicad-cli` is absent the test fails with the install line, it does
   not skip.
3. `docs/fab/board-v2.md`: block diagram (text or generated SVG), net
   summary, the G2 state table (powered, off, reset, uncooperative MCU,
   fault, VBUS present, bench: rails, gate state, SPI and control pins,
   pull-ups, protection paths, back-power paths, rail discharge and
   start-up), the G4 net map, the charger calculations (ISET, PRETERM,
   termination, timers, system load), the undervoltage derivation with
   V_STOP and V_START, the LDO threshold at which AVDD leaves 2.7 V, the
   BOM table with tier and source status per line, the E73 alternate
   mapping, what DRC says, and "Needs a decision" (G1b, WP11 outline,
   anything the reference designs contradict).
4. Every design choice checked against the ADS1292, BQ25100 and module
   reference circuits, named per line as "per reference" or "deviates:
   why".

Gates: `.venv/bin/python -m unittest discover -s tests -v` green including
the new test; `release.py` runs end to end; `git status --short` empty.
Commit in steps; the last commit is `board(v2): schematic, release job,
G2/G4 records`. Report `.reports/WP12-report.md` (untracked): what was
built, each gate with command and result, what was installed, what was not
done, "Needs a decision", the final sha. Closing steps per the common file
with `<PKG>` = `WP12`, `<lane>` = `w2`. A mid-package prompt from the
coordinator runs after your DONE as a new turn; push another DONE for it.
