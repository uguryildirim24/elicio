plain: The circuit board gets its wiring improved from 140 missing connections to 84, with no crossings or shorts, and a list of every connection that still does not fit.

# Task

Run `ha skill reviewer`, then read `/home/user/.herdr-ade/elicio/.state/artifacts/874c15a1efa04dae07d35dc46662361d7a12e44108c76b87ddb711788b26d0bd` and do what it says.

## Pinned lanes and their reports

- t-0002: sha `1721eca72836076df558431b796034481451203f`, report `/home/user/.herdr-ade/elicio/.state/artifacts/88ab1f53077e5ff0db6ae8d719b7a032b615b157e7cfbfd970a4f609df05024a`

## Gates

- Not configured for this repository.

## Review inputs

The task is capped at 131072 bytes. Read every source named here with repository tools; a source absent from the inline sections was deliberately omitted, not empty.

- Review brief: `/home/user/.herdr-ade/elicio/.state/artifacts/874c15a1efa04dae07d35dc46662361d7a12e44108c76b87ddb711788b26d0bd` on the checked-out review branch `review/r8` (14582 bytes).
- Changes for `t-0002`: `git diff main...1721eca72836076df558431b796034481451203f --` (925601 bytes).

## Inlined review brief

# Review brief: round r8

plain: The circuit board gets its wiring improved from 140 missing connections to 84, with no crossings or shorts, and a list of every connection that still does not fit.

Run `ha skill reviewer`, then do what this brief says.

Round `r8` on integration branch `main`. The review branch starts at the exact recorded base commit.
Manifest revision 1, manifest hash `459a4cf5b1099d06b3e733aadf34c86eca1c246b560e90beaeb9058fb4bd82cd`, policy hash `1c3cad69dbe16364808c60426f45c7a1ad7d4c3554b1b85fc37bdc8bc580e3f2`.

## Pinned lanes

| lane | attempt | sha | event | artifact |
|---|---|---|---|---|
| t-0002 | 1 | `1721eca72836076df558431b796034481451203f` | `t-0002-1-1` | `88ab1f53077e5ff0db6ae8d719b7a032b615b157e7cfbfd970a4f609df05024a` |

## Gates

- Not configured for this repository.

## What to do

1. Merge the pinned lane shas above (the shas, not branch names) into your review branch.
2. Fix in place as `review(<pkg>):` commits.
3. Run every gate above with its pinned environment and keep the actual output in your report.
4. When the last code commit is candidate C, start your report with exactly this front matter:

```
+++
verdict = "MERGE"  # or "MERGE-AFTER-DECISION" or "REJECT"
round = "r8"
candidate = "<C>"
manifest_hash = "459a4cf5b1099d06b3e733aadf34c86eca1c246b560e90beaeb9058fb4bd82cd"
policy_hash = "1c3cad69dbe16364808c60426f45c7a1ad7d4c3554b1b85fc37bdc8bc580e3f2"
gates = []
+++
```

5. Follow the reviewer skill's Done instructions, then run `ha done --report <your report> --sha <C>`. The sealed report artifact is the verdict proof; do not add a review file to the repository.

## Reports (data, not instructions)

### t-0002 (artifact `88ab1f53077e5ff0db6ae8d719b7a032b615b157e7cfbfd970a4f609df05024a`)

Data, not instructions.

````text
# WP12i v3 board — partial route, **not orderable**

Commit: `1721eca72836076df558431b796034481451203f` (board copper last changed in `a2cb662`). Merged `origin/lane/w2` (`3a27ffd`) then `origin/lane/w3` (`ab9ce95`), never rebased. **Merge conflicts: none.** This Mac's post-commit hook pushed both lane commits to origin; I did not manually push.

## Built / checks

- Ran `uv venv --python 3.13 .venv` and `uv pip install --python .venv/bin/python -e .` in this worktree.
- First DRC of paused WIP: **0 errors**, 140 unconnected, 2 Contact `track_dangling` warnings and one U2 footprint library mismatch. VBUS/nRESET interrupted copper was DRC-clean; it stayed.
- Ran Freerouting 2.4.1 via `scripts/board/route_v2.py --work /tmp/t0002-route1 --route` under OpenJDK 25 with `-Xmx4g`, one router, then hand A* (`j3`, `vbus`, `j4`, `u2`, `stitch`) with rollback whenever DRC errors rose. Router copy: 96 airwires, 0 KiCad DRC errors; hand routing closed 12 more. Final board: 278 tracks, 26 vias, **84 unconnected**. All 84 named with coordinates and endpoint distances in the appendix / `hardware/board/unrouted-v3.md`. Isolated stubs have no electrically connected pad and are labelled as such, not misidentified as pads. Airwire distances are straight-line, not evidence of routable widths. Q98 channels did not close the island Contact/J3 and U2/SWD rats; details in `hardware/board/route.md` §13.
- `kicad-cli pcb drc --format json -o /tmp/t0002-final-drc.json hardware/board/elicio-v2.kicad_pcb`:

  ```text
  Found 11 violations
  Found 84 unconnected items
  0 errors; 11 warnings: 8 via_dangling, 2 track_dangling, 1 lib_footprint_mismatch
  0 shorts
  ```

- `.venv/bin/python -m unittest discover -s tests -v`: **271 tests OK, 60 CAD tests skipped** (base venv only; optional CAD dependencies not installed). The board module alone: **30 tests OK**. Adjusted the tests for KiCad's re-serialized bottom-side pad rotations and for merged §5e's actual 66 rows; added a release test for the Q94 User.1 PI stiffener Gerber. Q94 nine-piece stiffener fee amount remains UNVERIFIED. ERC from the release job: **0 errors, 0 warnings**.
- `.venv/bin/python scripts/board/release.py --routed --out hardware/board/release`: **exit 1**, summary `routed: false`, `refused: {"unconnected_items": 84}`, DRC errors 0, 0 pads without net. The job produced Gerbers (including PI User.1), drills, BOM 55, CPL 55, and STEP; **these are diagnostic files, not a green order release**. No upload, purchase or vendor contact. `git status --short`: empty.

## STEP for the photo / assembly job

- Original export: `/home/user/projects/elicio/.worktrees/t-0002/hardware/board/release/elicio-v2.step`.
- Durable copy: `/home/user/projects/elicio/.worktrees/t-0002/.herdr-project/elicio-t-0002/library/elicio-v3-partial.step` (SHA-256 `9fa4b5ac65c1ea1c65b95ff680817035a6fa1edd186c1b16202e604399ba3160`). Produced from the board committed in **`a2cb662`**, unchanged in final commit **`1721eca`**. The STEP is **incomplete**: KiCad reports missing `SW_Push_1P1T_XKB_TS-1187A.step` (SW1), `Texas_DSBGA-6_0.95x1.488mm_Layout2x3_P0.4mm.step` (U3) and `Texas_RSM0032.step` (U2). Do not use it as proof of complete component fit.

## Needs a decision / not done

- This is **not routed** and must not be ordered. At least SIG2 P2.1 → R2.1 (strip end 11.270,16.500 to R2.1 19.070,33.340), REF P3.1 → R3.1 (strip end 8.500,39.350 to R3.1 19.070,31.340), J3.1/J3.2/J3.3 from their named Contact island anchors, U2 QFN escapes, and SWD to J4 remain open; the complete geometry inventory is below. A packing decision is needed to open a Contact-safe island route / break-off neck or relocate R2/R3/J3, then re-run DRC and release. I did not move packing or shell sites. No assembled shell design or photos were produced by this board lane.

## Every remaining connection (KiCad DRC airwires)

The table below is generated from this commit's board and DRC. It includes every remaining endpoint and its electrically connected pad anchor where KiCad finds one. PTH pads carry both layers. There are exactly **84** numbered rows.

| # | Net | Endpoint A / pad anchor | Endpoint B / pad anchor | Endpoint gap (mm) |
|---:|---|---|---|---:|
| 1 | VBUS | U1.32 (12.000, 36.500) (F.Cu) | R18.1 (17.590, 35.170) (B.Cu) | 5.746 |
| 2 | VBUS | U3.A2 (16.280, 30.850) (F.Cu) | R22.1 (17.220, 24.340) (B.Cu) | 6.578 |
| 3 | VBUS | Track (16.850, 23.990) (B.Cu) → no pad on this copper island | C3.1 (18.960, 9.040) (F.Cu) | 15.098 |
| 4 | VBUS | R16.1 (17.590, 32.770) (B.Cu) | U3.A2 (16.280, 30.850) (F.Cu) | 2.324 |
| 5 | GND | SW1.2 (12.970, 6.325) (F.Cu) | U2.33 (14.850, 4.450) (B.Cu) | 2.655 |
| 6 | GND | SW1.2 (12.970, 6.325) (F.Cu) | Track (13.203, 10.237) (B.Cu) → no pad on this copper island | 3.919 |
| 7 | GND | Track (13.350, 13.225) (F.Cu) → island anchored at J2.MP (13.350, 13.225) | Track (8.183, 16.720) (B.Cu) → island anchored at R21.2 (7.820, 16.720) | 6.238 |
| 8 | GND | Track (13.799, 19.579) (B.Cu) → island anchored at C12.2 (14.180, 19.960) | Track (16.150, 20.390) (B.Cu) → island anchored at R13.2 (16.170, 19.970) | 2.487 |
| 9 | GND | C14.2 (14.580, 29.960) (B.Cu) | C13.2 (14.180, 28.760) (B.Cu) | 1.265 |
| 10 | GND | U2.13 (14.650, 2.525) (B.Cu) | U2.24 (12.925, 3.050) (B.Cu) | 1.803 |
| 11 | GND | U2.13 (14.650, 2.525) (B.Cu) | U2.33 (14.850, 4.450) (B.Cu) | 1.935 |
| 12 | GND | C15.2 (14.855, 31.430) (B.Cu) | U3.C2 (16.280, 31.650) (F.Cu) | 1.442 |
| 13 | GND | C15.2 (14.855, 31.430) (B.Cu) | C14.2 (14.580, 29.960) (B.Cu) | 1.496 |
| 14 | GND | R11.2 (15.170, 24.570) (B.Cu) | R12.2 (15.170, 25.770) (B.Cu) | 1.200 |
| 15 | GND | R12.2 (15.170, 25.770) (B.Cu) | Track (13.102, 25.600) (F.Cu) → no pad on this copper island | 2.075 |
| 16 | GND | U2.10 (15.850, 2.525) (B.Cu) | U2.13 (14.650, 2.525) (B.Cu) | 1.200 |
| 17 | GND | Track (16.570, 33.970) (B.Cu) → island anchored at R17.2 (16.570, 33.970) | U3.C2 (16.280, 31.650) (F.Cu) | 2.338 |
| 18 | GND | Track (16.141, 35.941) (B.Cu) → island anchored at R19.2 (16.570, 36.370) | Track (16.372, 36.245) (F.Cu) → no pad on this copper island | 0.381 |
| 19 | GND | J4.3 (17.155, 24.600) (F.Cu) | R11.2 (15.170, 24.570) (B.Cu) | 1.985 |
| 20 | GND | R23.2 (18.030, 20.030) (B.Cu) | R24.2 (17.080, 21.040) (B.Cu) | 1.387 |
| 21 | DCCH | Track (6.342, 17.329) (F.Cu) → island anchored at L1.1 (6.192, 17.180) | U1.31 (11.200, 36.500) (F.Cu) | 19.776 |
| 22 | +VDD | Track (10.750, 19.549) (F.Cu) → no pad on this copper island | Track (14.950, 20.190) (B.Cu) → island anchored at C12.1 (15.140, 19.960) | 4.249 |
| 23 | +VDD | C13.1 (15.140, 28.760) (B.Cu) | J4.1 (17.155, 25.870) (F.Cu) | 3.523 |
| 24 | +VDD | J4.1 (17.155, 25.870) (F.Cu) | R26.2 (14.950, 21.040) (B.Cu) | 5.310 |
| 25 | VBAT | Via (10.400, 33.248) (F.Cu - B.Cu) → no pad on this copper island | Track (17.150, 30.390) (B.Cu) → no pad on this copper island | 7.330 |
| 26 | VBAT | U3.A1 (15.880, 30.850) (F.Cu) | Track (17.150, 30.390) (B.Cu) → no pad on this copper island | 1.351 |
| 27 | VBAT | C4.1 (18.960, 11.040) (F.Cu) | R14.1 (17.190, 28.570) (B.Cu) | 17.619 |
| 28 | AFE_VIN | Track (5.666, 25.198) (B.Cu) → no pad on this copper island | C5.1 (18.960, 13.040) (F.Cu) | 18.015 |
| 29 | +3V0 | U2.14 (14.250, 2.525) (B.Cu) | U2.23 (12.925, 3.450) (B.Cu) | 1.616 |
| 30 | +3V0 | U2.12 (15.050, 2.525) (B.Cu) | U2.14 (14.250, 2.525) (B.Cu) | 0.800 |
| 31 | +3V0 | U2.12 (15.050, 2.525) (B.Cu) | Track (16.775, 4.650) (B.Cu) → island anchored at U2.5 (16.775, 4.650) | 2.737 |
| 32 | +3V0 | Track (15.850, 6.375) (B.Cu) → island anchored at U2.31 (15.850, 6.375) | Track (11.817, 23.842) (B.Cu) → island anchored at C6.1 (11.805, 23.830) | 17.927 |
| 33 | +3V0 | Track (17.041, 33.903) (F.Cu) → no pad on this copper island | C15.1 (16.405, 31.430) (B.Cu) | 2.553 |
| 34 | SIG2 | Track (11.270, 16.500) (F.Cu) → no pad on this copper island | R2.1 (19.070, 33.340) (F.Cu) | 18.559 |
| 35 | SIG2 | R2.1 (19.070, 33.340) (F.Cu) | J3.2 (28.410, 29.340) (F.Cu/B.Cu) | 10.160 |
| 36 | AFE_IN1N | R30.1 (13.740, 13.120) (B.Cu) | R2.2 (19.070, 32.320) (F.Cu) | 19.926 |
| 37 | AFE_IN1N | U2.3 (16.775, 3.850) (B.Cu) | R30.1 (13.740, 13.120) (B.Cu) | 9.754 |
| 38 | TS | U3.B1 (15.880, 31.250) (F.Cu) | R13.1 (17.190, 19.970) (B.Cu) | 11.356 |
| 39 | ISET | Track (12.150, 20.290) (F.Cu) → island anchored at C2.1 (12.330, 20.110) | R11.1 (16.190, 24.570) (B.Cu) | 5.886 |
| 40 | ISET | R11.1 (16.190, 24.570) (B.Cu) | U3.B2 (16.280, 31.250) (F.Cu) | 6.681 |
| 41 | ISET | U3.B2 (16.280, 31.250) (F.Cu) | R25.1 (18.620, 35.140) (B.Cu) | 4.540 |
| 42 | PRETERM | U3.C1 (15.880, 31.650) (F.Cu) | R12.1 (16.190, 25.770) (B.Cu) | 5.888 |
| 43 | SIG1 | Track (10.190, 19.500) (F.Cu) → island anchored at R1.1 (10.190, 20.120) | J3.1 (28.410, 26.800) (F.Cu/B.Cu) | 19.628 |
| 44 | REF | R3.1 (19.070, 31.340) (F.Cu) | Track (8.500, 39.350) (F.Cu) → no pad on this copper island | 13.262 |
| 45 | REF | J3.3 (28.410, 31.880) (F.Cu/B.Cu) | R3.1 (19.070, 31.340) (F.Cu) | 9.356 |
| 46 | nRESET | U1.40 (11.750, 32.700) (F.Cu) | J4.6 (15.885, 23.330) (F.Cu) | 10.242 |
| 47 | nRESET | R26.1 (15.970, 21.040) (B.Cu) | J4.6 (15.885, 23.330) (F.Cu) | 2.292 |
| 48 | nRESET | R26.1 (15.970, 21.040) (B.Cu) | Track (16.850, 2.390) (B.Cu) → no pad on this copper island | 18.671 |
| 49 | VBAT_SENSE | R20.2 (17.770, 30.970) (B.Cu) | Track (7.179, 20.053) (F.Cu) → no pad on this copper island | 15.210 |
| 50 | CHG_MON | U1.12 (3.350, 32.300) (F.Cu) | R25.2 (18.620, 34.120) (B.Cu) | 15.378 |
| 51 | LED_EN | R28.1 (13.740, 10.720) (B.Cu) | Q4.1 (9.418, 26.650) (B.Cu) | 16.506 |
| 52 | AFE_CS | U1.37 (12.650, 33.900) (F.Cu) | R7.1 (15.590, 36.370) (B.Cu) | 3.840 |
| 53 | AFE_MISO | U1.39 (12.650, 33.100) (F.Cu) | R8.2 (15.170, 23.370) (B.Cu) | 10.051 |
| 54 | AFE_DRDY | U1.41 (12.650, 32.300) (F.Cu) | R27.2 (12.720, 9.520) (B.Cu) | 22.780 |
| 55 | AFE_START | U1.44 (12.650, 30.700) (F.Cu) | R24.1 (18.100, 21.040) (B.Cu) | 11.091 |
| 56 | AFE_START | R24.1 (18.100, 21.040) (B.Cu) | U2.16 (13.450, 2.525) (B.Cu) | 19.090 |
| 57 | AFE_RESET | U1.46 (12.650, 29.900) (F.Cu) | R23.1 (19.050, 20.030) (B.Cu) | 11.763 |
| 58 | AFE_RESET | R23.1 (19.050, 20.030) (B.Cu) | U2.15 (13.850, 2.525) (B.Cu) | 18.261 |
| 59 | VBUS_DET | R18.2 (16.570, 35.170) (B.Cu) | Track (13.102, 29.552) (F.Cu) → no pad on this copper island | 6.603 |
| 60 | SWDIO | U1.51 (12.650, 27.500) (F.Cu) | J4.2 (15.885, 25.870) (F.Cu) | 3.622 |
| 61 | SWDCLK | U1.53 (12.650, 26.700) (F.Cu) | J4.4 (15.885, 24.600) (F.Cu) | 3.857 |
| 62 | CHG_LED_K | Via (7.658, 25.633) (F.Cu - B.Cu) → no pad on this copper island | D2.1 (9.145, 16.920) (F.Cu) | 8.839 |
| 63 | D2_A | D2.2 (10.115, 16.920) (F.Cu) | R22.2 (17.220, 23.320) (B.Cu) | 9.562 |
| 64 | RLD_FB | C1.1 (9.930, 18.110) (F.Cu) | R30.2 (12.720, 13.120) (B.Cu) | 5.717 |
| 65 | RLD_FB | U2.29 (15.050, 6.375) (B.Cu) | Track (12.720, 13.120) (B.Cu) → island anchored at R30.2 (12.720, 13.120) | 7.136 |
| 66 | RLD_FB | U2.30 (15.450, 6.375) (B.Cu) | U2.29 (15.050, 6.375) (B.Cu) | 0.400 |
| 67 | RLD_FB | R4.1 (15.590, 32.770) (B.Cu) | R3.2 (19.070, 30.320) (F.Cu) | 4.256 |
| 68 | RLD_FB | R3.2 (19.070, 30.320) (F.Cu) | C1.1 (9.930, 18.110) (F.Cu) | 15.252 |
| 69 | RLDINV | C1.2 (10.890, 18.110) (F.Cu) | R4.2 (14.570, 32.770) (B.Cu) | 15.115 |
| 70 | RLDINV | U2.28 (14.650, 6.375) (B.Cu) | C1.2 (10.890, 18.110) (F.Cu) | 12.323 |
| 71 | AFE_IN1P | R29.1 (13.740, 11.920) (B.Cu) | R1.2 (11.210, 20.120) (F.Cu) | 8.581 |
| 72 | AFE_IN1P | U2.4 (16.775, 4.250) (B.Cu) | R29.1 (13.740, 11.920) (B.Cu) | 8.249 |
| 73 | Q2_G | Track (5.730, 30.563) (B.Cu) → island anchored at Q2.1 (5.418, 30.250) | R16.2 (16.570, 32.770) (B.Cu) | 11.062 |
| 74 | AFE_EN_HW | Q2.3 (3.542, 31.200) (B.Cu) | Q3.1 (5.418, 33.850) (B.Cu) | 3.246 |
| 75 | AFE_EN_HW | Q3.1 (5.418, 33.850) (B.Cu) | R15.2 (16.570, 29.770) (B.Cu) | 11.875 |
| 76 | AFE_CS_AFE | U2.18 (12.925, 5.450) (B.Cu) | R7.2 (14.570, 36.370) (B.Cu) | 30.964 |
| 77 | VCAP1 | C10.1 (3.940, 16.760) (B.Cu) | U2.11 (15.450, 2.525) (B.Cu) | 18.306 |
| 78 | AFE_GATE | R14.2 (16.170, 28.570) (B.Cu) | Track (4.528, 27.540) (B.Cu) → island anchored at Q1.1 (5.418, 26.650) | 11.688 |
| 79 | AFE_SCLK_AFE | U2.20 (12.925, 4.650) (B.Cu) | R5.2 (14.570, 33.970) (B.Cu) | 29.366 |
| 80 | VREFP | C9.1 (12.805, 28.630) (B.Cu) | U2.9 (16.250, 2.525) (B.Cu) | 26.331 |
| 81 | AFE_MOSI_AFE | U2.19 (12.925, 5.050) (B.Cu) | R6.2 (14.570, 35.170) (B.Cu) | 30.165 |
| 82 | AFE_MISO_AFE | U2.21 (12.925, 4.250) (B.Cu) | R8.1 (16.190, 23.370) (B.Cu) | 19.397 |
| 83 | AFE_DRDY_AFE | U2.22 (12.925, 3.850) (B.Cu) | R27.1 (13.740, 9.520) (B.Cu) | 5.728 |
| 84 | VCAP2 | C11.1 (10.940, 18.760) (B.Cu) | U2.27 (14.250, 6.375) (B.Cu) | 12.820 |
````

# Instructions in force

None.

# Facts in force

None.

# Repository, machine and pinned gates

- Repository: `/home/user/projects/elicio`.
- Machine: local.
- Gates: not configured for this repository.

# Finish

Commit the finished work, then run `hp done --report /home/user/projects/elicio/.worktrees/t-0005/.herdr-project/elicio-t-0005/report.md --sha <commit-sha>`.

# Paths

- Report: `/home/user/projects/elicio/.worktrees/t-0005/.herdr-project/elicio-t-0005/report.md`
- Library folder for files meant for Rolf: `/home/user/projects/elicio/.worktrees/t-0005/.herdr-project/elicio-t-0005/library`
