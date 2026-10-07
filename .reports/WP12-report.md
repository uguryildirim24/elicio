# WP12 report — Board v2 (lane w2)

Worktree: `/home/user/projects/elicio/.worktrees/w2`
Branch: `lane/w2`
Package: WP12 (coordinator follow-up: interface II)
Date: 2026-09-17

## What was built

First pass (HEAD was `9fa31d2`): schematic, 4-layer 17 × 33 mm interface I, release job, G2/G4.

This follow-up, after WP11 `lane/w1` `43a982a` `docs/fab/packing-v2.md`:

- PCB is now a **2-layer FPC**, PI 0.11 mm, FR4 stiffener 0.3 mm under parts (Eco1.User) and 0.2 mm at the three tabs (Eco2.User).
- Outline and part centres from winner **`A_501015_series_w20`** (`packing-v2.md` §4–§5). USB-C on the hook-end end face.
- Three flex tabs, ring pad Ø5.0 / hole Ø2.7, ENIG, clamped under the brass standoff. Footprint `elicio:RING_PAD_D5_H2.7`.
- Interface I 8 × 8 B.Cu pads recorded as the rejected candidate in `docs/fab/board-v2.md` §11a. Reason: I closes 0 runs at the anatomical sites (coordinator 0/288; packing §2: 720 I runs, none close). Cell under the board hits SIG1; neither cell fits under 3.0 or 3.5 mm with the load rule.
- Schematic contract unchanged (nets, values, G2/G4). P1–P3 still `elicio:PAD_8x8` symbols; footprint is the ring.
- JLC FPC capabilities, coverlay, stiffener list, flex fixture fee, and FPC assembly acceptance quoted in `board-v2.md`. No request, no upload, no quote.
- `scripts/board/release.py` gerbers are F.Cu/B.Cu plus Eco/Dwgs/Cmts (stiffener and bend notes). No inner layers.

Nothing ordered, quoted or uploaded. No vendor contact.

## WP11 numbers used

From `git show lane/w1:docs/fab/packing-v2.md` (report file is untracked).

- Closer: Raytac MDBT50Q-1MV2, 501015 series, width 20, standoff 3.0, LID_Y 7.0–9.0 (8.0 with order-1 foam).
- Hand-off layout: `A_501015_series_w20_y7_iII_s3` with Stage B using y8 for foam 0.5.
- USB-C hook-end end face (plan v2 §5.4 fallback).

## Install

Unchanged from the first pass: KiCad 10.0.6, `kicad-cli`, cask about 5.5 GB, 57 s.

## Gates

### 1. Unittest

```text
.venv/bin/python -m unittest tests.test_board_release -v
```

Result: **OK** (2 tests). ERC 0. BOM rows = placed parts = 59.

```text
.venv/bin/python -m unittest discover -s tests -v
```

Result: 131 tests, **13 FAIL**, all `test_cad.CadRegenTests` v1 solid hashes (`body_full_p15`, `body_full_p25`, `body_thin_p15`, `lid`). This lane did not edit CAD. Same 13 as the first WP12 close-out.

### 2. Release job

```text
.venv/bin/python scripts/board/release.py
```

| Field | Value |
|---|---|
| erc_errors | 0 |
| erc_warnings | 13 (same extends/lib warnings as before) |
| drc_errors | 893 |
| drc_warnings | 33 |
| unconnected_items | 0 |
| bom_rows | 59 |
| placed_parts | 59 |
| exit | 0 |

Gerbers include User_Eco1, User_Eco2, User_Drawings, User_Comments. No In1/In2.

### 3. git status at DONE

Must be empty of owned files after the commit. `.reports/WP12-report.md` is gitignored.

## What was not done

- Layout routing.
- Folded-tab solid (SIG1/SIG2 Gerber rings are unfolded; packing XY is the folded site).
- Factory programming quote (G4 quote-only, Rolf).
- Live re-open of every 0402 LCSC stock page at close-out.
- Confirmation of E73-2G4M08S1C and YFP0006 lands against the drawings.
- Physical G2 leakage measurement.
- Any JLC order, cart, quote, or upload.

## Needs a decision

See `docs/fab/board-v2.md` §19. Short list: G1b JST-SH vs PH plus 501015 harness 100 ± 3 mm; JLC FR4 has no 0.3 mm (WP11 assumed 0.3); six stiffener pieces vs extra-fee at ≥4; SW1 vs 2.5 mm assembly edge; SIG1/SIG2 unfold vs packing XY; ISET LED; system load vs 2 mA termination; Debug Probe at 3.0 V; E73/YFP lands; no BAV199; BQ25100 stock; protective ADC cadence.

## Final commit sha

`a4080c23e738237d6234e1736e2f0e43d22c1f43` (`board(v2): flex layout for interface II from WP11 winner`)

A repository post-commit hook pushed `lane/w2` to origin after the commit. This lane did not run `git push`. The package brief said never push.
