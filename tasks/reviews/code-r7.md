# Code review r7: WP11c–WP11f, WP14b–WP14e, WP17c, WP13c, WP12c–WP12f

Reviewer: rev7 (Claude Opus 5), branch `review/r7`, 2026-09-18.

## Verdict

**MERGE-AFTER-DECISION.**
The five lanes merge clean and every gate passes except one: shell v2 now exits 3 on `V2_CLOSURE`, because the concealed tail M2.5×4 never reaches the lid (decision 89). Before this review the check passed without measuring that.
The review removed the nylon domes the shell printed over all five contact holes, and fixed the §5d read from another worktree, L8's Java claim, three test gaps and the stale board-v2 text. Decisions 89–97 are Rolf's.

## Merged

| Order | Lane | Sha | Packages | Merge commit |
|---|---|---|---|---|
| 1 | `lane/w3` | `e4b857c` | WP11c–WP11f | `0a671aa` |
| 2 | `lane/w1-r6` | `bdfc429` | WP14b–WP14e | `18beacb` |
| 3 | `lane/w5` | `f8b1634` | WP17c | `2bf3b10` |
| 4 | `lane/w4` | `21dde8a` | WP13c | `0d8bcbc` |
| 5 | `lane/w2` | `fbd56e6` (exactly) | WP12c–WP12f | `c76a5d6` |

Base `d915ee3`. The `HANDOFF.md`/`HANDOFF.json` conflicts were resolved to main's version. `main` has moved since then (`0eef1c2`, `fea34f8`, `667b1e4`: round 8 notes, WP12g recorded, WP12h brief). This branch does not carry those commits. Round 8 merges them.

## Gates (final tree)

All gates were run at `3696f5c` with `LC_ALL=C` (except firmware, see its row). The last commit adds only this file.

| Gate | Command | Result |
|---|---|---|
| Unit tests | `LC_ALL=C .venv/bin/python -m unittest discover -s tests -v` | **251 run, 251 ok, 0 skipped**, 305 s. Per module: test_cad 72 (CAD build, render, shell v2, stamp, packing source), test_placement 88 (including `PlacementWP11eTests`, `PlacementWP11fTests`), test_board_release 16, test_receiver_v2 16, test_capture 16, test_frame_v2 13, test_harness 11, test_signal 6, test_sheets 4, test_events 4, test_splits 4, test_pipeline_features 1. With part of the extra blocked (defect 5): no trimesh/matplotlib → test_cad 72 run, 49 skipped; no build123d → 72 run, 22 skipped; 0 errors in both |
| Order 1 | `bte_fit_shell.py --out <tmp>` ×2, `render.py --out <tmp>` ×2 | Exit 0 both. All 15 STEP/STL/3MF are byte-identical to each other and to `docs/fab/cad/v1/`. Both renders and `drawing.pdf` are identical across the two runs. `git diff main -- docs/fab/cad/v1/manifest.json` is empty |
| Stage B v2 | `bte_fit_shell.py --params scripts/cad/params/stageb_v2.toml --out <tmp>` ×2 | Exit 3 both, all 10 files byte-identical to each other and to my build of the merged tree before any review commit. It fails the same eight names as round 6 (`REF_WIRE_envelope`, `V2_TAB_envelope` measured; six NOT_MEASURED) |
| Shell v2 | `bte_fit_shell.py --params scripts/cad/params/shell_v2.toml --stage shell --out <tmp>` ×2, then in place | **Exit 3** (was 0): `stage_b_failing ["V2_CLOSURE"]`, a measured failure (defect 3, decision 89). Every other check is a number, NOT_MEASURED or NOT_APPLICABLE by name (`V2_USB_end` NOT_APPLICABLE, Q81). The six solids are byte-identical across the two runs and to `docs/fab/cad/v2/`, and `files` hashes are equal. An in-place rebuild plus `render.py` leaves the tree clean. Stamp = `manifest.commit` = solids commit = `a83e13b`. `manifest.py --check-bytes` ok |
| Packing doc | `placement.py --packing-doc` | Exit 0, `docs/fab/packing-v2.md` byte-identical. Pin table v2.1 has 68 rows. The folded-site table = §5 contact sites P1–P3 plus Q86 P4 (14.70, 4.30), P5 (17.70, 11.72). `docs/fab/cad/v2c/` holds 4 drawings |
| Release | `scripts/board/release.py --board-dir hardware/board --out <tmp>` | Exit 0. `routed false`, ERC 0 errors / 0 warnings, DRC 0 errors / 5 warnings, 146 unconnected, BOM 57 = placed 57 = CPL 57, Gerbers, drills and STEP present (3 STEP models missing, as recorded) |
| Release `--routed` | same with `--routed` | Exit 1, "routed release refused", `summary.json` `routed: false`, `refused {unconnected_items: 146}`. The test asserts the refusal |
| Placement agreement | `PackingAgreementTests` (2 tests) | PCB vs vendored pin table v2 (R24 0.50) and PCB vs §5d v2.1 (67 rows ≤ 0.1, worst 0.086; R24 0.328 under Q87; side and rotation) |
| DSN classes | `scripts/board/route_v2.py --dsn-check --work <tmp>` | Exit 0, "DSN class check OK: Default 100/100 um, Contact 150/200 um, via 700:300 um" (60 096 bytes) |
| Firmware | `arduino-cli compile --fqbn adafruit:nrf52:feather52840 --library firmware --output-dir <tmp> firmware/elicio_stream` | Exit 0 **with the shell's UTF-8 locale**. Flash 134 012 B (16 %), RAM 18 472 B (7 %). Under `LC_ALL=C` the Adafruit `adafruit-nrfutil` step (Click) aborts on an ASCII locale, so do not force `LC_ALL=C` on this gate. `board_pins.h` equals board-v2 §9 (`assert_pin_map_matches`), and it claims no USB/J1/U5 pins |
| Sheets | `scripts/sheets/template.py --out <tmp>` ×2 | Exit 0 both. `template.pdf` and `sheets/m1–m8.svg` are byte-identical to each other and to the committed files |
| Receiver | `elicio receive --simulate-live --out <tmp> --seconds 2`, `elicio receive-check <session>` | Exit 0 / exit 0 (8 samples, `same_criterion_failed []`). The dropout rule's exits 1/2/3 are covered by the tests |
| Frozen files | `git diff d915ee3 HEAD -- docs/fab/plan.md docs/fab/plan-v2.md docs/fab/open-questions.md docs/fab/interface.md docs/fab/contacts.md docs/fab/cad/v1/` | Empty. Against today's `main` it shows 4 lines, which are main's own round 8 note (`fea34f8`) added after the base; this branch never edits the file |
| Repo growth | `git rev-list --objects main..HEAD \| git cat-file --batch-check='%(objectsize:disk)'` | 636 objects, **11.43 MiB** on disk (38.31 MiB raw), under 12 MB. The largest are the shell STLs (three versions of about 2.2–2.9 MB raw). `git count-objects -vH`: size-pack 34.51 MiB unchanged, 194 loose objects (3.58 MiB) |
| Wording | `grep -rn "owner\|the user" docs/ tasks/WP1[1-7]*.md` | 23 hits, identical to main's; nothing new |

## Defects

| # | Sev | File:line (at `c76a5d6`) | What was wrong | What changed | Commit |
|---|---|---|---|---|---|
| 1 | High | `scripts/cad/bte_fit_shell.py:4187`, `:4254` | The shell STL fused Ø4.7 × 1.35 nylon ISO 7380 domes over the three contact holes and the two charging-pad holes (added in round 6, `6546771`). Sections show nylon on the hole axis from y −1.34 to −0.59 at P1–P3, so the holes are blind from the skin and the titanium screws cannot go in (plan v2 §8 step 2). P4/P5 had a 0.3 web plus a dome, so the charger could not reach copper. Plan v1 §4: "MOCK_CONTACTS true – gauge prints domes; Stage B cuts holes". | The body cuts only the Ø2.7 holes (P1–P3) and open Ø5 holes (P4/P5). Sections at all five sites show air from y −1.5 to the cavity; the hole is Ø2.5–2.7 at P1–P3 and Ø5 at P4/P5. | `a83e13b` |
| 2 | High | `bte_fit_shell.py:3536`, `:3589` (`V2_CHARGE_pads`), `V2_RING_seat` | The checks probed only at mid-wall (y = wall/2), so they passed with the domes on. `V2_CHARGE_pads` *required* the dome (`flush_pads`, `{name}_dome`). | `V2_RING_seat` adds `{site}_face_open` (air at y −0.68, −0.05, 0.05). `V2_CHARGE_pads` fails on a cap (`{name}_cap`) and records `pad_recess` 1.50. Tests assert all of these. | `a83e13b` |
| 3 | High | `bte_fit_shell.py:3286` (`V2_CLOSURE`) | The check passed on "screw engagement 4.30 in the tail boss". The M2.5×4 head sits at the well bottom (y 1.55), so the tip reaches y 5.55 in the body's own solid tail. The lid underside is 8.00 and the lid has no boss. The screw holds nothing; only the hinge lip retains the lid. | Measures `screw_tip_y` 5.55, `lid_underside_y` 8.00 and `lid_engagement` 0.00. The check fails, the shell exits 3 with `stage_b_failing ["V2_CLOSURE"]`, and `shell-v2.md` §2/§4 and the drawing say so. The design question is decision 89. | `a83e13b`, `9679d8d` |
| 4 | Med | `bte_fit_shell.py:347` | The shell read packing §5c/§5d from `/Users/rolfie/projects/elicio/.worktrees/w3` and wrote that absolute path into the manifest. The build depended on another worktree's state. | Reads `git show e4b857c:docs/fab/packing-v2.md` from this repo, falling back to the working-tree file. A new test pins the folded rows and shell extras to the working tree, and the manifest carries no `.worktrees` path. | `a83e13b` |
| 5 | Med | `tests/test_cad.py:239` and five more classes | The CAD build tests were guarded on build123d only. With build123d present but trimesh or matplotlib missing, 24 tests errored (STL checks import trimesh; the packing overlays import `placement.py`, which imports matplotlib). This is the w2-venv failure class. | Build classes need build123d, trimesh and matplotlib; the pre-CAD classes need matplotlib. Measured with import blockers: no trimesh/matplotlib → 72 run, 49 skipped, 0 errors; no build123d → 72 run, 22 skipped, 0 errors. | `e1a6d2d` |
| 6 | Med | `tests/test_board_release.py:145` | The placement-agreement test read only the vendored `hardware/board/packing_v2_flat.md` (pin table v2), not §5d's pin table v2.1. It checked neither side nor rotation. | New test on §5d v2.1's 68 rows: 0.1 mm, side (bottom = B.Cu) and rotation (pcb = 180 − rot on bottom). R24 keeps the Q87 allowance 0.50 on this tree (d 0.328). The worst other row is R23 at 0.086. | `1203bf0`, `3696f5c` |
| 7 | Med | `docs/fab/L8-research-v5.md:110–136`, `:215` | §3 said Freerouting 2.4.1 runs on Java 21 and named `freerouting-2.4.1-exec.jar`. The release says "Fully upgraded to Java 25", the jar is class file 69, and the asset is `freerouting-2.4.1.jar`. Several quotes were not on the cited pages when re-read. | Java 25 and the jar name fixed in §3 and §5. A re-read table was added. The 0.2 mm carbonization quote, the V-cut quote, the $23.57 fixture fee, the stiffener-guide quotes (the page did not render), the 1up price (404) and the Thomas RC price (homepage only) are tagged `UNVERIFIED`. | `ce72578` |
| 8 | Low | `tests/test_receiver_v2.py:195` | Only line 3.7 went through `receive-check`. | New test that parses montage §8. It asserts that `SAME_CRITERION` equals the rows marked "same criterion" (3.5–3.10) and that each gives exit 1 on fail and 0 on pass or not_scored. The revised lines 3.1–3.4 are not scored by the tool (decision 96). | `e2242c8` |
| 9 | Low | `docs/fab/board-v2.md:278–294`, `:337`, `:416`, `:423` | §11 still had the WP12b table (7.0 edge strips, unfolded rings at (−4.75, 22.00) and (24.75, 33.10)) and the round 6 boss and fold notes. §13 called P4/P5 "tail charge pads". §12 did not say the stiffeners cover two-sided parts. | §11 now lists the §5d flat ring centres, folded seats and routes, plus H1/H2. §12 and §13 state the stiffener conflict, P4 VBUS / P5 GND, and R9/R10's unconnected pad 1. §15 was not touched. | `210804d` |
| 10 | Low | `scripts/cad/render.py` (shell captions) | The medial render's caption ran off the page. Both charging pads carried the same label, and one sat over the edge-on view. With no heads drawn, the holes showed white or the lid colour through them. | The titanium heads and the P4/P5 ring copper (gold, 1.50 down) are drawn in `render_medial.png` and on the drawing page. P4 is labelled VBUS and P5 GND. The caption wraps. The closure lines state the failed check. | `9679d8d` |
| 11 | Low | commit `1e055de` (WP12d) | The message says "routed" on an un-routed tree (the brief prescribed the line). | Recorded only. The tree's docs and `summary.json` say `routed: false`, and WP12e/WP12f corrected the habit. | — |
| 12 | Low (mine) | `scripts/cad/layout_v2c.py` | I first moved §5d's R24 to the fbd56e6 board site (18.75, 22.37) rot 0, following "the board is copper truth". Main meanwhile recorded WP12g (`8348e62`): the board moves to v2.1's (18.49, 22.57) rot 90, and Q87 is closed. | Reverted. Packing is back to `e4b857c`'s bytes and `--packing-doc` regenerates it identically. | `3f3f960` → `3696f5c` |

## Seams

**One packing truth.**
- The shell's pad and boss sites equal §5d's folded-site table: P1 (5.90, 22.00), P2 (10.40, 33.10), P3 (8.50, 43.00), P4 (14.70, 4.30), P5 (17.70, 11.72) at y 1.50; bosses (13.45, 17.70) and (17.95, 17.70). The rows at `408a476` and `e4b857c` are identical; only "pin table v2" became "v2.1" in one sentence.
- The PCB matches §5d v2.1 within 0.1 mm on 67 of 68 rows, with side and rotation matching. R24 is 0.328 off: the board has (18.75, 22.37) rot 0, v2.1 has (18.49, 22.57) rot 90. WP12g moves the board onto v2.1, so the packing row stays.
- J4's three NPTH match KiCad's own drill export exactly: (15.234, 22.06), (16.25, 27.14), (17.266, 22.06). The rotated 0402s R26 and R27 (rot 90, pads split along s) and R24 (rot 0, split along u) match the Gerber flashes. The "Y-down, CCW" mapping is right, and the pad model is symmetric, so it cannot mirror an 0402.
- J4's keep radius 0.6953 = 0.9906/2 + 0.20, which equals `min_hole_clearance` 0.2 in `elicio-v2.kicad_pro`.
- `hardware/board/packing_v2_flat.md` is still pin table v2 (R24 at 18.28). The board lane can re-vendor v2.1 in round 8.
- The CHARGE rectangle does not match §5d's prose. See decision 92.

**Charging pads, third pass (Q86).**
- I reproduced the tail arithmetic with the lane's rules. The window is s 39.25 + r to 45.5 − r and u 1.8 + r to 20.2 − r. Clearances: REF dome ≥ 5.2 + r, screw well ≥ 4.5 + r, pair spacing ≥ d + 3.
- The largest pair is exactly Ø2.10, e.g. (2.85, 40.30) and (18.85, 44.45). Ø2.12 fails.
- No Ø3 or Ø4 pad has even a single site, so no Ø3 or Ø4 pair fits the tail at chord 47.90.
- Without the screw well, the Ø3 region is about 4.8 across against 6.0 needed, and the largest Ø4 gap is 3.51 against 7.0. With the gaps halved to 1.0 there is still no Ø3 pair.
- At the hook end, P4's Ø5 copper edge is u 12.20, 0.30 from the cell pocket (u 11.90). P5's edge is u 20.20, 0.30 from the wall (u 20.50). The pads are 8.00 apart centre to centre and 3.00 edge to edge, so the lane's 0.30 claims hold for the copper.
- The ring outlines do not clear: P4's Ø6 outline reaches u 11.70, 0.2 under the cell. P5's Ø6.4 seat notches the side wall to u 20.90, which leaves 1.10 of wall. See decision 93.

**Stamp vs HEAD.** The test asserts the render stamp equals `manifest.commit`, and (new) that `manifest.commit` equals `git log -1 -- <solids>` (`git_commit_solids`). The rule survives merges: history simplification skips TREESAME merge commits, so a merge that does not change the solids never becomes the stamp. After this review the solids commit is `a83e13b`. The renders (`9679d8d`) are stamped `a83e13b`, and an in-place rebuild plus render leaves the tree clean.

**w2's 14 failing CAD tests.** Their venv now has the same build123d 0.11.1 and OCP 7.9.3.1.1 as mine. The failure class that remains is a partial `cad` extra, fixed in defect 5.

**WP13c.** The tool matches montage §8's "same criterion" column exactly: 3.5–3.10 stop with exit 1, and a 3.4 dropout gives exit 3 and a report (Q75). `receiver-v2.md` has the exit-code table. Lines 3.1–3.3 are revised numeric lines that the tool neither scores nor stops on (decision 96).

**Wording.** `grep -rn "owner\|the user" docs/ tasks/WP1[1-7]*.md` gives the same 23 hits as `main` (VISION, STAGE_A_PARTS, EARPIECE_DESIGN). Nothing is new.

## Attack points (numbers from my own cuts and runs)

- **Shell sections.** mesh_plane sections at s 15.3, s 16, P1–P5 and the tail well show:
  - rib slot and drop channel are air. At s 15.3 the rib (to y 4.5) is removed down to the floor (y 1.5) over u 11.9–20.5. That is the drop channel's vertical leg crossing the rib, so the opening is 3.0 tall, not the "height 0.31" slot `shell-v2.md` §1 and §5d describe. It is consistent with the fold, and the text should say so in round 8;
  - holes open (after defect 1);
  - the medial well is air, and the tail boss has a Ø2.10 pilot with a 6.45 wall.

  The lateral face is unbroken.
- **Width-20 cells.** All 16 fail on J4 ("TC2030 on the leftover (Q80)"); the best is 61/64 (process, no receptacle, chord 49.00, two sides). The failures are real.
- **B.Cu heights.** B.Cu parts are only SOT-23 (Q1–Q5), 0603 (C6–C9, C15) and 0402. All are ≤ 1.2 mm, under the 3.31 limit.
- **BOM.** 57 rows = 57 placed = 57 CPL rows, and every row has an LCSC number. Stock and price stay UNVERIFIED as §13 says.
- **Schematic nets.**
  - P4 → VBUS (D1 cathode, U3 IN, U1 VBUS pin 32, R16, R18, R22, C3). P5 → GND.
  - The inhibit chain VBUS → R16/R17 → Q2 → AFE_EN_HW → Q3 → AFE_GATE → Q1 is driven.
  - U1 D+/D− are unconnected. R9/R10 have pad 1 unconnected (decision 95).
  - ERC 0 matches what the nets show.
- **J2 and J3 are outside the body.** J2 (battery JST-SH) sits at u 22.40, with its courtyard at u 19.5–25.3, past the cavity wall (20.50) and the outer wall (22.0). J3 (bench header) spans u 19.95–32.3. Their board hangs (J2: u 20.4–25.8, s 7.4–14.4; J3: to u 33.2, s 16–26.7) are outside the shell. The shell's courtyard list comes from §5c and includes these rows, and no check tests them against the cavity. See decision 91.

## §7 look of the WP14e renders (after the fixes)

**Lateral view.** It passes the stranger's glance: one lofted, unbroken lid with no screw, no text and no seam other than the lid rim. The hook reads as a normal BTE hook with a circular root, and the lip is invisible from outside. Two faults:
- The tail's grey body shows as a band below the lid at the bottom, which makes the part read as a cap on a block rather than one shell.
- At 22 × 47.9 × 9 mm the body is broad for a behind-the-ear piece. It looks like a hearing aid a size up.

The annotation arrows for "hinge lip" and "No USB opening" cross (cosmetic).

**Medial view.** This is the view Rolf will judge. It now shows what will touch the skin: three titanium button heads in a line down the body, two gold charging pads near the hook, and the concealed screw well at the tail.
- The skin face carries five metal features, which is more than the plan pictures.
- The two pads sit 1.5 mm down in their holes, so they collect sweat.

As drawn before this review (nylon domes, blind holes) the renders showed a part that could not be assembled. **Rolf should not approve them until decisions 89 and 90 are taken.**

## Q88 ruling

**What plan v2 §5.3 says.** It does not say 1.0 mm. It asks that the exposed pad have "its net kept clear of all other copper". G7 asks for "positive clearance from the cell and unrelated conductors" and an "insulation envelope around each contact net". The 1.0 mm is board-v2's own number (§11's 7 × 7 other-net keep-out, 1.0 beyond the Ø5 land). Q84 and Q88 cite it as §5.3's creepage, and that attribution is wrong.

**Q88 is faithful to those words.** Exposed contact copper, meaning the Ø5 lands and their annular mask openings, keeps 1.0 from every other net. That is the conservative reading of "kept clear of all other copper" where copper is bare and meets sweat.

**What the envelope must mean.** Where the contact net runs under coverlay, "insulation envelope" is met by insulation on both faces plus a clearance to foreign copper, not by 1.0 mm of air. For this board, the rule must be:
- (a) each strip carries only its own Contact net, on one layer, with no other-net copper on either layer of that strip (foreign-net keep-out through the thickness, not just beside the trace);
- (b) the trace is at the Contact class clearance 0.20 to anything, and coverlay covers it on both faces up to the land's mask opening;
- (c) no via and no pour of another net inside the land's 7 × 7 zone, on either layer;
- (d) inside the sealed cavity on the island, the class clearance 0.20 applies (Q84), with R1–R3's pads the only exposed Contact copper there.

WP12g's GND pour that shorted SIG1/SIG2 breaks (a) and (c), and was rightly discarded.

**R1–R3 are not at the tab roots.**
- R1 (10.70, 20.12) is about 4.1 mm from SIG2's root (10.40, 16.00) and 6.3 mm from SIG1's (5.90, 16.00).
- R2 (17.87, 32.03) and R3 (17.87, 30.03) are about 10.9 and 12.1 mm from REF's root (8.50, 37.60).

The Contact runs across the island are therefore 4–12 mm. §5.3 sets no length. The runs stay inside the envelope under the rule above, so they are not a §5.3 violation. They matter for pickup: µV EMG on 4–12 mm of unshielded trace on a two-sided island beside a BLE module and a charger. WP12h should route them shortest, on one layer, with GND on the other layer under them where the envelope allows, and away from U1's antenna edge and the charger's switching nodes. Moving R1–R3 to the roots is a round 8 packing option if the routes cannot be kept short.

## Needs a decision

89. **The tail screw closes nothing.**
    - The M2.5×4 from the medial well ends at y 5.55 inside the body's own tail. The lid underside is at 8.00 and the lid has no boss.
    - Only the hinge lip retains the lid, and `V2_CLOSURE` fails.
    - Options:
      - (a) a lid boss dropping into a tail pocket, with a screw long enough for about 3 mm of thread in it (M2.5×8 or ×10: Rolf buys it; Q71 named ×4);
      - (b) a second lip or latch at the tail (Q71 said no snaps);
      - (c) accept hinge-plus-friction, which S4's pull test would have to prove.
    - The shell stays exit 3 until one is chosen.
90. **P4 = VBUS and P5 = GND sit bare on the skin face.**
    - This is a 0 Ω path from skin to circuit ground outside the 220 kΩ per-path bound (R7 / G2).
    - It is a fourth electrode in parallel with REF/RLD, and sweat bridges the 3.0 mm gap to VBUS.
    - Options: pads behind a removable cover, a series element on the GND pad, or move the pads off the skin face (the tail cannot hold Ø3 or Ø4, see Seams).
91. **J2 and J3 and their hangs are outside the body.**
    - J2 (battery connector) must be inside. J3 (bench header) could be a snap-off tab removed before closing, but the flat pattern and the shell do not say so.
    - Packing round 8: move J2 into the cavity, and either define J3's hang as a break-off tab or drop it. Add a cavity test for every courtyard.
92. **The CHARGE tab root does not match §5d.**
    - The flat rectangle (33.02, 4.30) 14.50 × 8.60 spans u 25.77–40.27, s 0–8.6. It joins the board only through J2's hang (u 25.8, s 7.4–8.6, a 1.2 mm joint) outside the body.
    - §5d's prose puts the root at the leftover s 16.00 through the rib slot.
    - Packing round 8, together with 91.
93. **P4/P5 retention, recess and fit.**
    - Nothing clamps the P4/P5 rings, so the charger's pogo force lifts them off the floor.
    - The copper sits 1.50 below the skin face.
    - P4's ring outline reaches 0.2 under the cell. P5's Ø6.4 seat leaves 1.10 of side wall over the seat's 0.36 height, below the 1.5 rule; `V2_WALL_minima` does not probe there.
    - Options: heat-stake or adhesive the rings, printed bosses that bring the copper flush, move P5 in by ≥ 0.4.
94. **Stiffeners against two-sided assembly.**
    - Both FR4 0.4 pieces cover lands on both faces, and a stiffener cannot sit over lands on its own side.
    - The ring FR4 0.2 of decision 72 is still undrawn, and drawing it makes the count 5 (fee).
    - Choose: stiffener on the side without parts in zones, stiffen only one face, or PI stiffeners.
95. **R9/R10 (5.1 kΩ CC) do nothing.** With no receptacle, pad 1 is unconnected, yet they are placed, bought and packed. Mark them DNP or delete them (BOM 57 → 55, and packing and the PCB lose two 0402s).
96. **Montage lines 3.1–3.3** (noise, flex and clench numbers, revised) are not scored or stopped by `receive-check`. Say whether the analysis pipeline scores them, or `receive-check` should.
97. **Contact envelope.** Adopt the envelope rule in the Q88 ruling (a)–(d) as the reading WP12h routes under, and correct Q84/Q88's attribution of 1.0 mm to plan v2 §5.3.
