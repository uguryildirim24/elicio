# Code review, round 1 (rev1)

**Verdict: MERGE-AFTER-DECISION.**
All gates pass on `review/r1` after the review fixes; the order-1 solids regenerate byte-identical and every plan-named check passes.
Twelve items below change or bend plan text and need Rolf's call before order 1 goes out.

Branch `review/r1`. Merged in order: `lane/w9` (f172c8f), `lane/w1` (e98bfe6),
`lane/w4` (963bfa5), `lane/w5` (ac7502e), `lane/w2` (1fd8463). Every merge
was clean. Line numbers in the defects table point at the merge tip
`1fd8463`, before the review commits.

## Gates

Interpreter: private `.venv`, Python 3.13.15, `pip install -e '.[cad]'`
(build123d 0.11.1, trimesh 5.1.0).

| Gate | Command | Result |
|---|---|---|
| Full test suite | `.venv/bin/python -m unittest discover -s tests -v` | 67 tests OK. The 25 CAD tests run; none skipped. |
| Reference build, twice | `.venv/bin/python scripts/cad/bte_fit_shell.py --out <tmpA>` then `--out <tmpB>` | Exit 0. All 15 files identical between A and B and to `docs/fab/cad/v1/` (SHA-256). |
| Manifest checks | read `checks` in `docs/fab/cad/v1/manifest.json` | 184 checks, 184 passed. |
| Pre-CAD checks | `.venv/bin/python scripts/cad/bte_fit_shell.py --checks-only` | Exit 0. |
| Measurement overlay checks | `.venv/bin/python scripts/cad/bte_fit_shell.py --params scripts/cad/params/rolf.toml --checks-only` | Exit 0 (rolf.toml has no measurements yet, so REF). |
| Robustness builds | same script with an overlay of `CREASE_BOW = 1`, `CREASE_BOW = 8`, `SIDE = "left"`, and `--variant thin --preload 2.5` | All exit 0; one solid per part; all checks pass. At merge tip, bow 8 failed with `hook: expected one solid, got 2`. |
| Stage A untouched | `git diff main -- src/` | 0 lines. |
| plan.md untouched | `git diff main -- docs/fab/plan.md` | 0 lines. |

## Defects

Severity: **High** = wrong part, wrong order, or a check that passes when it
should fail. **Medium** = wrong number or instruction a person would act on.
**Low** = wording, traceability.

| # | Sev | File:line (at 1fd8463) | What was wrong | What I changed | Commit |
|---|---|---|---|---|---|
| 1 | High | scripts/cad/bte_fit_shell.py:833 | `_try_fillet` asked `max_fillet`, which returns 0 on these solids, so every §3.5 fillet was silently skipped: no tip round 4.0, no medial 1.5, no lid edge 0.8, no lip root, no hook joint. The manifest said nothing. | Fillet with `Solid.fillet`, requested radius first, stepping down 0.25; build body and tail sharp, fuse, then fillet (the fused-after-fillet order left an untriangulated sliver that broke the 3MF). Each fillet's applied radius goes in manifest `notes`. | 051a186 |
| 2 | High | scripts/cad/bte_fit_shell.py:1240 | Hook fused straight onto the body: its −5° embedded start sits in the battery cavity (4.58 mm³ at bow 3, about 20 mm³ at bow 8). | Cut the hook with the rotated cavity before fusing; record `hook_stub_in_cavity_removed_mm3`. | 051a186 |
| 3 | High | scripts/cad/bte_fit_shell.py:1240 | At CREASE_BOW 8 the hook cut left a floor sliver: build failed with 2 solids, so a measured ear near the clamp could not build. | Fuse the whole cut result, then take the one solid; clamp-limit builds added to the tests. | 4054e39 |
| 4 | High | scripts/cad/bte_fit_shell.py:599–679 | Pre-CAD checks were constants (`record("E5_lip", 1.0 >= 1.0)`, E1–E4 fixed sizes, walls read from params). The §3.6 fit table, CONTACT_STACK and keep-out checks the plan names were missing. | Measure walls, E1–E5 sizes, fit nominals and adverse ±0.6 from the built geometry; add `contact_stack` (with wall +0.3), `keepout_clearances` (pads, rib, walls, cavity end), `contact_caps`. A drifted fit now fails (test added). | 4beaaa3 |
| 5 | High | scripts/cad/bte_fit_shell.py:372–436, 1607–1657 | Overlay rules: `--params default.toml` was treated as an overlay (every key "measured", REF lost); CREASE_BOW computed from M1 alone or from defaults; unknown and locked keys accepted; `MOCK_CONTACTS = false` accepted with no Stage B checks behind it. | `validate_overrides` + `resolve_overrides`: default.toml is never an overlay; bow computed only when the overlay sets M1 and M2 and not CREASE_BOW; `--from-measurements` needs M1 and M2; unknown or locked keys and MOCK_CONTACTS=false fail before export. Nine overlay tests. | 09c0fbb |
| 6 | High | scripts/cad/bte_fit_shell.py:428–435, params/default.toml:15 | HOOK_RADIUS pinned at 13.5 in default.toml, so M8 never drove it; the fallback formula `+ 1.0` gives 13.75 at M8 = 11 and fails the plan's own `< M8 + 1` bound. | Removed HOOK_RADIUS from default.toml; HOOK_RADIUS = M8 + HOOK_DIA/2 + 0.75 (13.5 at the default) unless set; the check is strict `<`. See decision 2. | 09c0fbb |
| 7 | High | scripts/cad/bte_fit_shell.py:1525 | Lid overlap checked only against the body of the current loop, in the body frame, with the lid built per body; the hook was never checked; no test that one lid closes all three bodies. | Check the exported lid seated on every body at that body's LID_Y, and against the hook in the shell frame. Thin body: 0 mm³. | 051a186 |
| 8 | High | tests/test_cad.py:96 | Regen test compared a subset of hashes and did not check the temp dir's contents; stale files from another parameter set would pass. | Hash all 15 files, compare file lists and both manifests, require every check passed. Build refuses an `--out` whose manifest lists other parts (test added). | c58cffb |
| 9 | Medium | scripts/cad/bte_fit_shell.py:1360 | `stl_watertight` returned True when trimesh was missing. | Raise instead. Lid and coupon also get recorded watertight checks. | 4beaaa3 |
| 10 | Medium | scripts/cad/bte_fit_shell.py:1158–1171 | A failed lid emboss was recorded as a note and the lid still exported. | Raise CheckFail. | 051a186 |
| 11 | Medium | scripts/cad/bte_fit_shell.py:903 | Coupon rib extruded flat (0.4 high), not the standing 0.4 wall E4 describes. | Standing box 12 × 0.4 × 3.2. | 051a186 |
| 12 | Medium | scripts/cad/bte_fit_shell.py:1459 | Manifest listed the full part matrix and plan quantities whatever was built. | Parts and quantities from what was built; add walls, contact_stack, keepout_clearance, span per body, `crease_bow.source`. | 4beaaa3, 6caa0ed |
| 13 | Medium | scripts/cad/README.md:19–35 | Reference command used `--params default.toml` (overlay bug) and did not reproduce the committed lid; single-variant command wrote into `v1/` and would mix sets. | Rewritten: reference command, overlay rules, full and single-variant builds, §3.5 deviations, font caveat, check commands. | c58cffb |
| 14 | High | docs/fab/measure.md:22 | Stop rule quoted one gate (50.9 at bow 3) though the script's gate moves with the bow from M1 and M2; an ear between 47.68 and 51.35 got the wrong answer. | Gate table at bows 1/3/8, stop rule in three bands, M2 − M1 table computed at M1 = 47.7 so it never passes an ear the script rejects. | c1ea238 |
| 15 | Medium | docs/fab/measure.md:94, 114 | M3 described jaws, not the depth rod; M4 said front to back; M8 did not say what it feeds. | Depth rod for M3; jaws sideways for M4; M8 feeds HOOK_RADIUS = M8 + 2.5. | c1ea238 |
| 16 | High | docs/fab/order1.md:26–27 | Do-not-order used a fixed 50.9 gate and made a DFM wall warning a stop, though E1–E5 are the plan's accepted thin features. | Read `chord_gate.gate` and `checks` from the manifest; DFM warnings on E1–E5 are recorded, not stops. | 42d33a0 |
| 17 | Medium | docs/fab/order1.md:86 | Price stop did not match plan §9 (line over $200, total over $55 Standard / $75 DHL). | Stops are exactly those. | 42d33a0 |
| 18 | Medium | docs/fab/order1.md:141, 166 | Hook test taped the hook down (measures nothing); tape fallback at s 10 and s 40, not the plan's 10 mm and 40 mm from the hook end. | Hook arc taped over a box edge, domes up, Before − After drop; fallback positions from the hook end. Order no. and Total charged added to `orders.md`. | 42d33a0 |
| 19 | High | docs/fab/contacts.md:51 | Recommended 18-8 stainless nut as "plan §4 conforming"; §4 allows plated steel or tinned copper only. Titanium DIN 934 shown with margin; it has zero (Kapton top 4.39 at wall +0.3). | Nut row cites §4 as written; 18-8 marked outside the text; titanium zero margin stated. See decision 6. | 0f0f06e |
| 20 | Medium | docs/fab/contacts.md:30, 38 | Prices, URLs (home pages) and head dimensions presented as verified. | Marked UNVERIFIED; RJX pack flagged over the $20 line. | 0f0f06e |
| 21 | Medium | docs/fab/contacts.md:96 | TE 31428 barrel is 22–26 AWG; sheet said suitable for 28 AWG as-is. | Fold the wire and solder. | 0f0f06e |
| 22 | Medium | docs/fab/contacts.md:381 | Torque 0.20–0.25 N·m with no source, for an M2.5 in a 1.0 mm printed wall. | Removed; tighten by feel, with the caution. Wrench 5.0 mm. | 0f0f06e |
| 23 | Medium | docs/fab/contacts.md:234, 318 | DMG negative presented as proving Ni ≤ 0.01% / below 10 ppm. | Screen pass only; the claim removed. New §5.4 "Before any wear". | 0f0f06e |
| 24 | Medium | docs/fab/contacts.md:423 | Kapton disc on the nut bottom; the stack puts it on top. | Kapton on the nut top. | 0f0f06e |
| 25 | Low | docs/fab/contacts.md:446, 454 | Internal-metal list incomplete; S1 checklist ticked with nothing bought. | Items 10–15 added; checklist unticked with a status per line. | 0f0f06e |
| 26 | Medium | docs/fab/interface.md:115, 125 | Stack derivation: D2/D3 wrong, ISO 4032 arithmetic wrong, no reservation vs SKU split. | §2.3 reservation and SKU columns plus the tip rule; D2, D3 and ISO 4032 note corrected. | cca14d1, 6e92eee |
| 27 | Medium | docs/fab/interface.md:248 | §6.1 pad gap quoted in the shell frame and only at bow 3. | Body-frame gaps 0.152 (bow 3), 0.110 (bow 1), 0.263 (bow 8); the test checks > 0.09 at all three. | cca14d1 |
| 28 | Low | docs/fab/interface.md:345 | §8.2 option A area stated as fact. | Marked UNVERIFIED; §7 nut metal row, §9 item 1, §10; new §12 pending v2 notes (V2-1 dome, V2-2 coupon map, V2-3 nut, V2-4 packing); errata change-log row, version stays 1. | cca14d1, 6e92eee |
| 29 | Low | docs/EARPIECE_DESIGN.md:303 | Row 9 added a reason not in the plan ("so five contacts are not required"). | Row 9 now reads as the plan: three, not five; clench is 3–5× a flex. | 42e51d5 |
| 30 | Low | docs/EARPIECE_DESIGN.md:350 | Open question 3 struck through though WP6 has not confirmed the board. | Strikethrough removed; still open until WP6. | 42e51d5 |

## Needs a decision

1. **Chord gate `>` vs `≥`.** Plan §3.3 writes M1 > TOTAL_CHORD + 3. The
   script and measure.md use ≥. The difference is one 0.01 mm reading.
2. **HOOK_RADIUS formula.** Plan §3.3 writes M8 + HOOK_DIA/2 + 1.0 and
   quotes 13.5 at M8 = 11, which needs + 0.75. The plan's form gives 13.75
   and fails its own `< M8 + 1`. Implemented + 0.75, strict `<`. Pick one
   and fix plan text.
3. **Hook joint fillet 2.0 (§3.5 step 9) does not build.** The tube edge is
   1.25 mm from the medial face at M4 = 6. Built: 1.5 (full p15), 1.75
   (thin p15, full p25), about 1.25 at bow 5.5, 0.75 at bow 8. Accept the
   largest-that-builds rule, or change the hook root.
4. **Lip root fillet 0.5 (§3.5 step 7).** 0.5 overlaps the body top edge by
   0.045 mm³ when seated; 0.2 is used.
5. **Hook stub in the cavity.** The −5° embedded start is cut back (4.58 mm³
   at bow 3, about 20 mm³ at bow 8). Confirm that is the intent, or move the
   hook start.
6. **Nut metal.** Plan §4 allows plated steel or tinned copper. No
   plated-steel DIN 439 M2.5 SKU was found; 18-8 is outside the text;
   titanium DIN 934 has zero stack margin at wall +0.3. Choose the metal
   (interface §12 V2-3).
7. **Dome dimensions** have no drawing (interface §12 V2-1). Stack numbers
   hold only for the assumed dome.
8. **LID_EDGE 0.8 at the lip end.** Not applied on the top edge at the lip
   so the lip keeps its full joint. Accept, or give the lip a different
   root.
9. **Plan §3.1 single-variant command into `v1/`** is refused by the stale
   guard, because it would mix a one-variant manifest with the other parts.
   Change the plan command to a separate `--out`, or drop the guard.
10. **Emboss font.** The lid's bytes depend on the Arial OCCT finds; another
    machine can change hashes. Accept per-machine regen, or ship a font
    file in the repo.
11. **Emboss depth.** The 0.8 emboss reaches below the lid underside into the
    0.4 module headroom (plan §5) in Stage B. Fine for the Stage A gauge;
    decide before Stage B.
12. **Carried as-is.** Packing shortfall (interface §12 V2-4) and the
    requirement-5 vs titanium question stay open.
