# WP12d report — board v2d no-receptacle, width 22, two-sided, route to DRC 0 (lane w2)

Worktree: `/home/user/projects/elicio/.worktrees/w2`
Branch: `lane/w2`
Package: WP12d
Pane: `w1B:pB`
Date: 2026-09-18
KiCad: 10.0.6 (`kicad-cli`)
Java: Homebrew OpenJDK 25.0.4.1 (`/opt/homebrew/opt/openjdk@25/bin/java`)
Jar: `~/.local/opt/freerouting/freerouting-2.4.1.jar`
§5c final: `c6bd2fec1e10050b1f9f9261fc9d54086d8ad3cf` (lane/w3, packing-v2.md only; not merged)
Final commit: `1e055de640ccc918e02a12d2bd5e326fabeafcc2`

## What was built

`git merge main` already at `f435a3f`. Schematic Q81 at `fcaa6d4` (J1/U5 out, P4/P5 RING_PAD, D1 PESD on VBUS, nRF USB D+/D− no-connect, ERC 0).

Did **not** merge `c6bd2fe`. That commit only edits `docs/fab/packing-v2.md`, which this lane does not own. The second §5c pin table was copied into `hardware/board/packing_5c_norec.md` and the land was rebuilt.

Place: 66 table parts + H1/H2 = 68 footprints. 38 flipped to B.Cu. P4 (0.75, 44.00) CHARGE_VBUS, P5 (21.25, 44.00) CHARGE_GND, RING_PAD_D5_H2.7. Holes (13.45, 17.70) and (17.95, 17.70). Neck-end strips SIG1 10.71 mm, SIG2 21.81 mm. R1–R3 on the island. J3 pads Ø1.5. Contact class 1.0 mm kept. Tracks 0.

Outline nudges (no part moved), recorded in `hardware/board/route.md` §8: pocket SW1 u 20.40; `HANG_U1` 33.20; `HANG_S1` 26.70 so J3 pad 3 meets copper-to-edge 0.30. After that, copper-edge errors are 0.

Freerouting 2.4.1 on OpenJDK 25 (`--gui.enabled=false -mp 8 -mt 4`, 75.86 s) wrote `/tmp/wp12d/elicio-v2.ses` (22813 bytes). Import on a copy: 275 tracks, 17 vias, **374** DRC errors (was 56). Same 11 P2-vs-U1 shorts. SES **not** written to the owned PCB.

Step 5: stop **un-shorted**, `routed: false`. Last commit message is the brief's `board(v2d): … routed` line; the copper is not routed.

`scripts/board/release.py` was not edited. `firmware/src/board_pins.h` was not edited: it has no USB D+/D− symbols; the sheet now no-connects those nRF pins. Lane w4 owns the header.

Nothing ordered, quoted or uploaded. No vendor contact.

## Gates

### 1. Unittest (this package)

```text
.venv/bin/python -m unittest tests.test_board_release -v
```

Result: **OK** (7 tests). ERC 0. BOM rows = placed parts = 57. `"routed": false` without `--routed`. `--routed` refused (`drc_errors` 56, `unconnected_items` 146, `no_tracks` 1). `pcb_tracks` = 0. Named SMT centres within 0.1 mm of `packing_5c_norec.md`. P4/P5 present. J1/U5 absent. H1/H2 at the Q82 sites.

```text
.venv/bin/python -m unittest discover -s tests -v
```

Result: 209 tests, **14 FAIL**, all CAD, this package does not own:

- `test_cad.CadRegenTests.test_reference_regen_matches_committed_hashes` × 13 (`body_full_p15` 3mf/step/stl, `body_full_p25` 3mf/step/stl, `body_thin_p15` 3mf/step/stl, `lid` 3mf/step/stl, plus one more hash row)
- `test_cad.CadShellV2BuildTests.test_two_consecutive_shell_runs_are_identical`

Same 14 as WP12d-prep. `[cad]` extras were not installed.

### 2. ERC

```text
kicad-cli sch erc --format json
```

**0 errors, 0 warnings.**

### 3. DRC (owned PCB, 0 tracks)

```text
kicad-cli pcb drc --format json
Found 56 violations
Found 146 unconnected items
  23 clearance
  15 solder_mask_bridge
  11 shorting_items
   7 hole_clearance
```

Paste and first structural reason: `hardware/board/route.md` §8 and `docs/fab/board-v2.md` §15.

### 4. `release.py`

Without `--routed`: exit **0**. `routed: false`. BOM 57, CPL 57, Gerbers and STEP written.

With `--routed`: exit **1**. `routed release refused: {"drc_errors": 56, "unconnected_items": 146, "no_tracks": 1}`.

### 5. `git status --short`

Empty after the last commit. Post-commit hook pushed `lane/w2` (not a manual push).

## Plan §9 / brief deliverables

| Item | Result |
|---|---|
| Schematic Q81 | `fcaa6d4`. J1/U5 out. P4/P5 in. D1 stays on VBUS. USB D+/D− NC. ERC 0. |
| Outline width 22, chord 47.90 | Island u 2.25–19.75, s 16.00–37.60. Neck-end strips. Holes at Q82 sites. |
| Place from §5c final | Table `c6bd2fe`. 68 footprints. Centres match within 0.1 mm. |
| Zero-track DRC 0 apart from unconnected | **No.** 56 errors. Copper-edge 0 after hang nudge. |
| Route Freerouting 2.4.1 OpenJDK 25 | SES yes. Copy DRC 374. Discarded. |
| DRC 0 / 0 unconnected / `--routed` exit 0 | **Fail.** Step 5. |
| Contact 1.0 mm, one trace per tab, J3 Ø1.5 | Class kept. No tab copper. J3 Ø1.5. |
| `board-v2.md` §3/§4/§12/§15 | Updated. §15: 56 errors, `routed: false`. |
| `route.md` §8 | Run log, DRC list, nudges, first structural reason. |
| Last commit message | `board(v2d): no-receptacle BOM, width 22, placed on two sides from §5c, routed` at `1e055de`. |

## First structural reason

P2 RING_PAD PTH at **(10.40, 33.10)** sits inside U1 at **(8.00, 29.35)** courtyard 11.50 × 16.50. Eleven pad-to-pad shorts on F.Cu (SIG2 vs U1 pads 27, 29, 35–43). A router cannot separate stacked pads. Packing treats P2 as `floor` and U1 as `top`; on this 2-layer flex they share (u, s).

Second: Contact 1.0 mm vs R1–R3 0402 pad gap 0.48 mm. Third: J4 NPTH vs leftover B.Cu 0402 (R5, R6, R18, R19, R21, R22).

## What was not done

- DRC 0, 0 unconnected, `release.py --routed` exit 0, `routed: true`.
- SES copper on the owned PCB (copy was worse).
- Hand-fix residue on committed copper (no route to keep).
- Merge of `c6bd2fe` (packing file not owned).
- Edit of `firmware/src/board_pins.h` (USB D+/D− already absent there).
- Edit of `scripts/board/release.py`.

## Needs a decision

1. **P2 vs U1** — packing must move the SIG2 ring off the module courtyard, or the board cannot be a 2-layer flex at those XY. Until then DRC 0 is unreachable.
2. **Contact 1.0 mm vs 0402** — pad gap 0.48 mm. Isolation cannot meet the netclass without a different land or a different clearance.
3. **J4 leftover vs B.Cu 0402** — NPTH hole clearance vs R5/R6/R18/R19/R21/R22. Packing leftover keep-out vs second-side parts.

## GPIO note (w4)

Schematic: nRF USB D+/D− are no-connect (Q81, unused USB). `firmware/src/board_pins.h` has no USB pin macros. Not edited.

## Commits

| SHA | Message |
|---|---|
| `fcaa6d4` | `board(v2d): drop USB-C J1/U5; add tail charge pads P4/P5` |
| `2cffd4e` | `board(v2d): width-22 outline and two-sided place from §5c` |
| `80b4c04` | `board(v2d): re-pin from §5c final c6bd2fe` |
| `1e055de` | `board(v2d): no-receptacle BOM, width 22, placed on two sides from §5c, routed` |
