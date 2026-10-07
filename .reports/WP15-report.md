# WP15 report — Rolf's sheets v2

Lane `w9`, branch `lane/w9`, worktree
`/home/user/projects/elicio/.worktrees/w9`. Interpreter: Python
3.13 in a worktree-local `.venv`. HEAD at start `dbe39ff` (same as
`main`). Docs plus `scripts/sheets/template.py` and
`tests/test_sheets.py`. `pyproject.toml` was not edited. matplotlib
3.11.2 and pypdf 6.19.0 were installed into `.venv` from the existing
`cad` extra pins.

## What was written

- `scripts/sheets/template.py`: 1:1 US-letter PDF of winner
  `A_501015_series_w20_y8_iII_s3` (packing-v2.md §5) with contacts
  (5.9, 22.0), (10.4, 33.1), (8.5, 43.0), a 50 mm bar, and the check
  "Measure the 50 mm bar before you trust this template." Also eight
  SVGs in `docs/fab/sheets/` (m1–m8). PDF dates pinned via pypdf.
- `docs/fab/template.pdf` and `docs/fab/sheets/m1.svg` … `m8.svg`.
- `docs/fab/measure.md`: v2 rewrite. M1–M8 keep the v1 definitions.
  Right ear (Q28). On-bone check at REF with the paper template (Q17).
  M1 gates everything once (50.90 mm, packing-v2.md §6).
- `docs/fab/order-board.md`, `order-shell.md`, `order-parts.md`: G8
  first, then the order. Unknown vendor fields say "the agent fills
  this after WP12b/WP14". Uploads from `docs/fab/cad/v2/` and
  `hardware/board/release/` marked expected. Massachusetts. Duties as
  DDP shows them. Raytac Q67 on the board sheet. One ledger line per
  small-parts parcel. Q64 names two probe options and does not pick.
- `docs/fab/assemble.md`: plan v2 §8 eight steps, each with tool,
  part, check, and a WP14 picture placeholder; step 6 polarity in the
  plan's words; first-load net map from board-v2.md §4, REGOUT0 note,
  firmware-v2.md commands, time "measured, not promised"; §7 pull and
  drop as qualitative steps; fail = stop and write one line.
- `docs/fab/orders-v2.md`: Q33 ceiling row still blank, with Rolf's
  name on it. Shell reserved-maximum row unchanged. No total.

`plan-v2.md` and `open-questions.md` were not edited.

## Plan v2 §11 row 15

Acceptance: no step needs a question; the first-load procedure
rehearsed on paper.

`grep '?' docs/fab/measure.md docs/fab/order-board.md
docs/fab/order-shell.md docs/fab/order-parts.md docs/fab/assemble.md`
finds nothing. First load is a paper section in `assemble.md` (net
map, REGOUT0, commands, write-back for measured time and VTref). It
was not run on hardware.

## Gates

### Unit tests

Command:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

Result: Ran 173 tests in 83.641s. OK (skipped=21). Skips need
build123d / trimesh. New `tests/test_sheets.py` ran four tests,
including two-run byte identity and match to the committed PDF/SVGs.

### Template twice identical

Command: `tests.test_sheets.TemplateRegenTests.test_script_run_twice_is_byte_identical`

Result: ok.

### owner / the user

Command:

```bash
grep -n "owner\|the user" docs/fab/*.md
```

Result: one hit, pre-existing, `docs/fab/interface.md:554`. Nothing
new in the WP15 sheets.

### git status

`git status --short` empty after the four commits (this report
untracked under `.reports/`, gitignored).

## Numbers that wait on WP12b and WP14

WP12b: gerber names; flex ENIG/coverlay checkout fields; extra-stiffener
fee amount; stiffener count after merge; BOM/CPL/STEP in
`hardware/board/release/`; `summary.json` with `routed: true`; Raytac
global-sourcing vs consignment prices on the day; factory programming
catalogue line; product first-load hex (with WP13b).

WP14: `docs/fab/cad/v2/` body and lid STL/STEP/3MF names; two renders;
drawing page; manifest checks; stand-if-printed; colour process;
closure geometry for step 7; board-screw SKU for step 5; connector
picture for step 6; tab-wall slot (Q59).

## What was not done

- No purchase, quote, upload, or vendor contact.
- First load was not run. Time is blank for Rolf to measure.
- Exact JLC flex and JLC3DP checkout fields that are not already on
  `main` were left as "the agent fills this after WP12b/WP14".
- matplotlib was not added to `pyproject.toml` (not in Owns).
- This lane did not run `git push`. A post-commit hook pushed
  `lane/w9` to origin after each commit.

## Needs a decision

- Q33 ceiling (Rolf; ledger row blank).
- Q64 probe: Raspberry Pi Debug Probe vs J-Link EDU Mini class / level
  shifter. The sheet names both. G4 names one before a buy.
- Q67 Raytac route at G3 with both prices in front of him.
- Q55 cell SKU with a page price, or WP11b length trade.
- Q36 China vs not, for the default JLC carts.
- Q59 REF tab vs cavity end wall: nothing orders until it passes.
- G1b pack/connector freeze before assemble step 6.
- Step 5 board screws: plan v2 §8 names them; Interface II retention
  is WP14's (`V2_BOSS` NOT_MEASURED).

## Final commit sha

`018ac588a1f54b5e2fec1bde510ee930a154aabf`

Message: `sheets(v2): measure, three checkouts, assemble, first load`.

Under it: `c1afb71` checkouts, `52f5cb5` measure.md, `958d448`
template script and drawings.
