# Code review, round 2 (rev2)

**Verdict: MERGE-AFTER-DECISION.**
All gates pass on `review/r2` after the review fixes. The renders and drawing now show the real geometry, and the montage protocol's sources are checked.
WP6 packing is **not confirmed**: once the lug tabs, the RSM maximum body and a second diode array are counted, the medial face does not close. Items 13–15 need Rolf before WP6 round 3; 16–19 before S1.

Branch `review/r2` from `main` e3c3a2f. Merged in order: `lane/w5` (e0ea395)
as d1ab41f, `lane/w2` (a325a63) as bd5b5ae, `lane/w1` (3579223) as
dbacc00. Line numbers in the defects table point at the merge tip
`dbacc00`, before the review commits.

Datasheet facts come from a read-only agy lane (`r2ds`, brief
`tasks/L-r2-datasheets.md`, a2ba08c). It read TI ADS1292 SBAS502C, Nexperia
BAV199S-Q (20 July 2026) and BAV199 (1 April 2023), the DNK 501015 drawing,
and Raytac Spec K on 2026-09-17. It confirmed that ADS1292IRSMT/IRSMR
exist, with an RSM body of 4.00 nominal and 4.10 max. It also confirmed
that one BAV199S-Q has two independent series pairs.

## Gates

Interpreter: private `.venv`, Python 3.13, `pip install -e '.[cad]'`
(build123d 0.11.1, numpy 2.5.3, matplotlib 3.11.2, pypdf 6.19.0, trimesh
5.1.0). Run on the final tree.

| Gate | Command | Result |
|---|---|---|
| Full test suite | `.venv/bin/python -m unittest discover -s tests -v` | 83 tests OK, none skipped (CAD, render and placement tests run). |
| Reference build, twice | `.venv/bin/python scripts/cad/bte_fit_shell.py --out <tmpA>` then `--out <tmpB>` | All 15 solids identical between A, B, `docs/fab/cad/v1/` and the manifest `files` hashes. |
| Solids vs `main` | compare `files` with `git show main:docs/fab/cad/v1/manifest.json` | 12 non-lid hashes equal. `lid.step`, `lid.stl`, `lid.3mf` differ; the only commit on the branch that touches a solid is `66b5564` (font). |
| Renders, twice | `.venv/bin/python scripts/cad/render.py --out <tmpA>` then `--out <tmpB>` (each over its build) | `render_medial.png`, `render_lateral.png`, `drawing.pdf` and `manifest.json` identical in A, B and `docs/fab/cad/v1/`. |
| Manifest schema | `.venv/bin/python scripts/cad/manifest.py --check-bytes docs/fab/cad/v1/manifest.json` | `schema 1 ok`, exit 0. |
| Manifest missing key | same validator on a copy with `commit` removed | `MANIFEST FAIL: … missing key 'commit'`, exit 2. |
| Placement drawing, twice | `.venv/bin/python scripts/cad/placement.py --out <tmp1>` then `<tmp2>` | Both `9465bfde…c52c9d`, equal to the committed `placement.svg`. |
| Untouched files | `git diff main -- src/ docs/fab/plan.md docs/fab/open-questions.md` | 0 lines. |
| Pictures | Read `render_medial.png`, `render_lateral.png`, the drawing page via `render.py --debug-png`, and `placement.svg` rendered to PNG | Looked at each after the fixes; notes in the defects below. |

`placement.svg` stays out of the manifest `views` map. The map is limited
to pictures of the solids that `render.py` regenerates from the build;
`tests/test_placement.py` checks the SVG. This is written in
`scripts/cad/README.md` and in `manifest.py`.

## Defects

Severity: **High** = wrong part, wrong order, a check that passes when it
should fail, or a picture that misleads Rolf. **Medium** = wrong number or
instruction a person would act on. **Low** = wording, traceability.

| # | Sev | File:line (at dbacc00) | What was wrong | What I changed | Commit |
|---|---|---|---|---|---|
| 1 | Low | pyproject.toml, tests/test_cad.py, scripts/cad/README.md, scripts/cad/bte_fit_shell.py | Merge conflicts between WP3 and WP6. `.reports/WP6-report.md` was tracked on `lane/w1`. | Kept both lanes' additions. `cad` extra is `build123d>=0.7`, `trimesh>=4`, `matplotlib>=3.9`, `pypdf>=5`. The committed-file test allows the gauge files, `manifest.json`, `placement.svg` and the artwork. `git rm --cached` on the report; the file stays on disk. | dbacc00 |
| 2 | High | scripts/cad/render.py:203–226 | Each part was a separate depth-sorted `PolyCollection`, so the lid painted over the body. The drawing's medial and side views showed the lid underside through the body with no caps. The lateral render showed the hidden tongue as a tab past the tail (the coordinator's seam c). | All parts rasterised into one numpy z-buffer with 2× supersampling. Edges come from depth jumps, normal creases, part boundaries and silhouettes. A silhouette check found one lid area outside the body: about 9 mm² of lip and plate edge at the top end, which the plan puts there (§3.3 LID_LIP, §3.5 step 7). The render labels it. | b4733bd |
| 3 | High | scripts/cad/render.py (medial figure) | The medial views were near head-on, so the 9.0 and 7.0 bodies looked identical (seam a). | Each body is shown twice: a medial view and an edge-on posterior view with a `BODY_THICK` dimension. Same scale, true orthographic scale bar. | b4733bd |
| 4 | High | scripts/cad/render.py (shading) | Long boolean triangles around the mock caps shaded as a starburst that dominated the medial face (seam b). | One flat shade per triangle, with outlines and creases drawn from the buffers. The starburst is gone. The faint facet banding left on the posterior fillet is noted in the caption as STL mesh. | b4733bd |
| 5 | High | scripts/cad/render.py (drawing sections) | The closure sections were wrong: the body ran under the lip, the recess above LID_Y was drawn solid, and the nub fit was drawn in the wrong plane. | Sections rebuilt from the §3.3 constants: lip (s, y) at u 11, nubs (u, y) at s 17.9 with the 0.4 gap, tail (s, y) at u 8.5. | b4733bd |
| 6 | Medium | scripts/cad/render.py (drawing text) | M1–M8, E-table and title block values were typed-in strings, not taken from the manifest. | Every value and callout comes from the manifest or params: chord and gate, bow, hook radius, glasses flat, contacts with M6/M7 marked recorded, SPAN vs M3, E2/E4 notes, and the built hook-joint and lip-root fillets per body (Q3, Q4). The date is the solids commit date. | b4733bd |
| 7 | Medium | docs/fab/cad/v1/drawing.pdf | 3.7 MB for one page (vector STL triangles). | Shaded views are embedded as images; tables and sections stay vector. Now 72,810 bytes, byte-identical on regeneration. | b4733bd |
| 8 | Medium | scripts/cad/render.py (font setup) | A missing vendored font fell back to a system font silently. | `configure_matplotlib` raises `RenderError`. | b4733bd |
| 9 | High | tests/test_cad.py:223 | The regen test compared hashes, checks and `commit` only, so a committed manifest missing the `emboss_font` notes the writer now records still passed. | The test compares every key except `views`. The render test compares the `views` map with the committed one. Manifest regenerated (solid hashes unchanged). | 684c11d, b4733bd |
| 10 | Low | scripts/cad/README.md | Hash drift across library versions was not stated (seam). | README gives the renderer, the `--debug-png` command, tested versions, the two-step commit a solids change needs, and the `views` decision. | 684c11d |
| 11 | High | docs/fab/montage.md:169–181 | The frozen criteria cited sources that do not say that. "L3 §3.1" (5 µV RMS) has no such text. "L3 §1 r2" gives 50–350 µV, not 45. "DESIGN r60" (3:1) and 10:1 appear nowhere. "HANDOFF M1" is the gesture-classification milestone. "DESIGN FP" gives no talking or walking rate. The yawn and smile counts were also marked quoted. The WP7a gate ("no number without a source or PROPOSED") passed on false citations. | Every quote is checked verbatim against L3, the design record, the handoff, `policy.py` or the plan, with section. Every other number is tagged **PROPOSED** with a rationale and what settles it. PROPOSED numbers may change once, from Stage A gel data, before the first dry recording, with a dated row (§1, §7). | ab41681 |
| 12 | High | docs/fab/montage.md:133 | Per-trial DMM resistance measurement on the worn electrodes. Plan review turn 02 finding 7: "any on-body impedance test needs its own reviewed safe method, not an ordinary mains-connected meter". | Removed. §2.5 item 4 forbids it until a method is reviewed. | ab41681 |
| 13 | Medium | docs/fab/montage.md:252 | `policy.py` names were wrong (`CONFIRMATION_TIMEOUT_SECONDS`, `CONFIRMATION_CONFIDENCE_FLOOR`). | `CONFIRM_WINDOW_S = 3.0`, `CONFIRM_CONFIDENCE_FLOOR = 0.85`, the floors quoted from the file. | ab41681 |
| 14 | Medium | docs/fab/montage.md:125, 136 | `elicio scope` had no `--input`; `elicio capture --output --duration` flags do not exist. | The design record's `stty` and `scope` lines, the macOS `stty -f` form, and `capture` with the real flags (`--input --sample-rate --offset --gain --seconds --site --note --out`). | ab41681 |
| 15 | Medium | docs/fab/montage.md:64 | 35 mm pads "trimmed to 15 mm" at a 12 mm pitch overlap and bridge the gel. | Cut the foam only, keep the gel discs apart, and record the smallest non-touching pitch if 12 cannot be met (PROPOSED procedure). | ab41681 |
| 16 | Medium | docs/fab/montage.md:86–90 | The chain diagram joined all three leads at one node. | Replaced by the design record's chain block; the reference wiring follows the Stage A schematic and is recorded. | ab41681 |
| 17 | Medium | docs/fab/montage.md:155 | Unsourced window s1 ∈ [20, 24]; at s1 below about 21.85 keep-out 1 reaches the rib. | No window. Any coordinate other than the defaults is an interface change that re-runs WP2's `keepout_clearances`. | ab41681 |
| 18 | Medium | docs/fab/montage.md:24–60 | The caliper from the hook root was the primary marking method. Plan §3.7 item 9 marks dome positions from the worn gauge. The M6 relation to the reference was not checked. | The gauge marks are primary, with the caliper as a cross-check. Added a press test for bone under the reference mark and the M6 offset. Configuration B uses the L3 §2.2 quotes; the plan-§2-row-8 quote says why the shell cannot hold it. | ab41681 |
| 19 | Medium | docs/fab/montage.md:243 | "L3 §7.2 heel strike" and the hook-preload claim are not in L3. | Removed; walking rests on the design record quote plus PROPOSED. | ab41681 |
| 20 | Low | docs/fab/montage.md:272, 290, 348, passim | S1 said "zero wear" while S0 passive wear continues. "Chlorinated solvents, abrasive pads" was presented as a plan §6 quote. Pads at 26.5 were stale. LaTeX units throughout. | Release-state table quotes plan §9. Cleaning quotes plan §6 and §4. Pads removed from §6. Units in plain text. | ab41681 |
| 21 | High | scripts/cad/placement.py:213 | The free mask left out the signal lug tabs and their 0.5 margin, which plan §5 and interface §3.1 require. Free area 101.53 mm² should be 69.36. The "confirmed" packing (interface.md:430) rested on it. | Tabs 3 × 7 from the Ø7.1 edge toward the pad, plus 0.5, are in the mask and on the drawing. The budget also reports the short reading (86.97) and no tabs (101.53). Packing withdrawn to **not confirmed**. | 93ab908 |
| 22 | High | scripts/cad/placement.py:119; docs/fab/interface.md:354 | One BAV199S-Q is two independent series pairs, so it clamps two lines, not three. Plan §6 and S2 need "three separately protected paths". | Two arrays (SIG1+SIG2, REF plus a spare pair) with a line-to-array map and a test. With the tabs counted, neither has a legal site within 10 mm of its pads; this is reported, not hidden. | 93ab908 |
| 23 | High | scripts/cad/placement.py:119 | The array courtyard (u 4.20–6.85, s 27.10–29.45) sat under the REF pad. No test checked courtyards against pads, so the "within 10 mm" rule passed on an illegal site. | Parts are placed only at legal sites. `layout_conflicts()` checks courtyards against the mask, pads and each other; pads against other nets' tabs; the wire against keep-outs and tabs; tabs against walls. A regression test covers the round-1 site. | 93ab908 |
| 24 | High | scripts/cad/placement.py:667 | The reference wire ran straight from the s 37 wrap to (4.0, 29.0). Its Ø1.3 surface entered keep-out 2 by 0.63. | Rerouted via (5.0, 34.6), clearing keep-out 2 by 0.09. The test asserts ≥ 0. At the 7 mm tab reading it still crosses both tabs (conflict list). | 93ab908 |
| 25 | Medium | scripts/cad/placement.py:98 | VQFN courtyard came from the 4.00 nominal body; the RSM drawing maximum is 4.10. | `VQFN_CY = (4.60, 4.60)`; interface cites SBAS502C and drawing 4219108/B. | 93ab908 |
| 26 | Medium | scripts/cad/placement.py:344; docs/fab/interface.md:340; tests/test_placement.py:52 | Battery separation used the 15.5 nominal module, but plan §5 reserves 15.8; the test pinned 5.00. | Module body at the reserved 15.8 gives 4.70 (hook) and 4.30 (rib), both under 5. The antenna zone is 16.70 from the cell. Both readings are in interface §6.3 (question 14). | 93ab908 |
| 27 | Medium | scripts/cad/placement.py (`place_0402s` fallback) | Two 0402s were put "two-sided" over the VQFN with no check at all, to reach 25. | Fallback removed. 10 of 25 fit medially after the ICs, which is reported. | 93ab908 |
| 28 | Low | scripts/cad/placement.py:100; docs/fab/interface.md:355, 408 | SOT-23 occupied area 3.3 × 3.0; Fig. 9 gives 3.3 × 2.9. | 3.3 × 2.9, three = 28.71. | 93ab908 |
| 29 | Low | docs/fab/interface.md:24–25, 161 | Duplicated rule line. Tab row pointed at pad (5.9, 26.5) while §4 froze 26.6. | Duplicate removed; 26.6. | 93ab908 |
| 30 | Medium | docs/fab/interface.md:219–242 | §5 discussed a PCM fold onto the 10 mm face. Plan §5 folds it "on the lateral face under Kapton", and the depth budget was missing. It also did not say a +2.4 mm pocket moves the M1 gate. | Depth budget: 6.0 − 0.5 foam = 5.5, leaving 0.5 at T 5 and 0.3 at T 5.2 for PCM and Kapton (PCM thickness UNVERIFIED). Growing BODY_ARC 2.4 raises TOTAL_CHORD and the gate and is a shell change. | 0bad5af |
| 31 | Low | docs/fab/interface.md:226 | The DNK drawing's "PRELIMINARY DATASHEET. SPECS SUBJECT TO CHANGE." header was not mentioned. | Noted; a released drawing is needed before buying a cell. | 7bc9f24 |

Not defects, checked: SIG1's move from 26.5 to 26.6 is needed. At 26.5 the
1.0 mm pad edge is 4.00 from CONTACT_1, under the 4.05 that the keep-out
plus 0.5 requires. `keepout_clearances` in `bte_fit_shell.py` checks the
nylon corner pads, not the lead pads, so the script and interface do not
disagree. `order1.md` names the committed PNG files correctly. Lid solids
changed only in `66b5564`, and `bte_fit_shell.py` fails when the vendored
font is missing.

## Needs a decision

13. **Signal lug tab length and direction.** Interface §3.1 says "3 × 7 ×
    1.5; from the cylinder toward pad". Read literally (7 mm past the Ø7.1
    edge), each tab runs past its own pad, which sits 4.6 and 5.8 from the
    contact centres. The CONTACT_2 tab would also reach u 0.68, through the
    side wall at u 1.5, and the SIG2 and REF pads land inside other nets'
    tab margins. If the tab ends under its pad, free area is 86.97 mm², not
    69.36. My reading: the tab should end under its own pad, and its
    direction and length go on WP5's lug drawing (UNVERIFIED #2). Rolf
    confirms that reading, or keeps 7 mm and the pads move.
14. **What "≥ 5 mm from the battery" measures** (plan §5 module row). At the
    reserved 15.8 module, the module body sits 4.70 from a cell packed to
    the hook and 4.30 from one on the rib. The antenna no-copper zone sits
    16.70 away. Spec K gives no battery distance. My reading: the rule is
    for the antenna, so it passes; keep "cell packed to the hook" as a
    rule anyway. If it means the module body, the board or the cell has to
    move.
15. **Packing escalation** (plan §10 Open for Rolf item 6, reopened). VQFN-32
    plus two BAV199S-Q need 79.30 mm² against 69.36 free, and even at the
    short tab reading the greedy layout finds no array site within 10 mm
    of the pads. Options, with areas in interface §8.2: B longer (+3.5
    mm), C wider (+3 mm), or E, passives on the lateral face outside the
    module (not in plan §5). A WP6 round 3 then sets new pads and tab
    directions. My reading: settle 13 first. If the short tab holds, try E
    before a shell change.
16. **Plan §3.3 LEAD_PADS SIG1 s 26.5 → 26.6.** This is a plan erratum (the
    pad breaks the 0.5 margin at 26.5). It is likely moot once round 3
    moves the pads, but plan text should not keep a pad that fails its own
    rule.
17. **Reference site against M6.** At M6's default of 15, CONTACT_REF at u
    8.5 lands about 6.5 mm in front of the bony bump if the body's front
    edge sits in the crease. Plan §2 row 8 wants the reference "over the
    mastoid surface". Montage §2.2 step 6 records whether it is on bone.
    Rolf decides whether a measured offset moves CONTACT_REF (an interface
    change) or is accepted.
18. **Cell pack** (carried from WP6, interface §5). Either keep the DNK
    in-line pack and grow the pocket 2.4 mm (a shell change that moves the
    M1 gate), or do the plan's hand fold on the lateral face. That fold has
    0.3–0.5 mm for PCM and Kapton, and the PCM thickness is unverified.
    The DNK drawing is preliminary either way.
19. **The PROPOSED numbers in montage §3**: 5 µV RMS, 45 µV, 3:1 flex, 10:1
    clench, 70 % A/B ratio, 100 ms dropout, ±0.5 V at the INA128 output, 9
    of 10, 0.20 per minute eating, 0 talking and walking, the yawn and
    smile counts. Rolf accepts them as the frozen set, or they are revised
    once from Stage A gel data before the first dry recording (montage §1).
    S1 needs this settled.
