+++
verdict = "MERGE"
round = "r8"
candidate = "f5a8c4e1cc8d884a467d957e7bdb2bccec86ee28"
manifest_hash = "459a4cf5b1099d06b3e733aadf34c86eca1c246b560e90beaeb9058fb4bd82cd"
policy_hash = "1c3cad69dbe16364808c60426f45c7a1ad7d4c3554b1b85fc37bdc8bc580e3f2"
gates = []
+++

## t-0002

Merged pinned `1721eca72836076df558431b796034481451203f` into review base `15a3d7436f95ff45333287312addeb75c8fab6ab`, then committed small fixes as `review(board):`. The round manifest remained revision 1 with the pinned hash. The measured board has **84 unconnected items, zero DRC errors and zero shorts**. This meets the round's stated partial-wiring outcome, **not** an order-ready board. The 84-row inventory is in `hardware/board/unrouted-v3.md`. It lists actual endpoints, islands and straight-line gaps, not routable channels. Repeating KiCad's DRC chose equivalent different endpoints for rows 7 (GND) and 43 (SIG1) while preserving the 84 count. I clarified in the inventory and generator that rows are a snapshot rather than stable airwire IDs. Also removed a duplicated diagnostic in `apply_wp12i.py`, preserved its saved-track count check including arcs, and corrected the stale v2.1 test claim in `docs/fab/board-v2.md`.

Rolf must **not order** this board. A future packing decision must make space for the remaining Contact connections, J3 break-off neck and U2/SWD routes, followed by DRC and a successful routed release. That decision is not needed to merge this explicitly partial milestone. The STEP is incomplete (missing SW1/U2/U3 models); the stiffener fee remains unverified.

## Gates

None configured. `gates = []`; no pinned gate commands to run.

## Independent verification (not gates)

- `kicad-cli pcb drc --format json -o /tmp/t0005-r8-drc.json hardware/board/elicio-v2.kicad_pcb` — exit 0:
  ```text
  Found 11 violations
  Found 84 unconnected items
  Saved DRC Report to /tmp/t0005-r8-drc.json
  unconnected 84
  violations Counter({('warning', 'via_dangling'): 8, ('warning', 'track_dangling'): 2, ('warning', 'lib_footprint_mismatch'): 1})
  errors 0
  ```
- `uv venv --python 3.13 .venv && uv pip install --python .venv/bin/python -e . && .venv/bin/python -m unittest discover -s tests -q` — exit 0:
  ```text
  Ran 271 tests in 122.813s
  OK (skipped=60)
  ```
  An argparse usage message from an existing test's expected failure appeared before the result; it did not fail the suite. CAD optional dependencies were not installed, hence 60 skips.
- `/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 scripts/board/unrouted.py hardware/board/elicio-v2.kicad_pcb /tmp/t0005-r8-drc.json /tmp/t0005-r8-unrouted.md` — exit 0:
  ```text
  /tmp/t0005-r8-unrouted.md: 84 airwires
  ```
  The generated file differs from the committed snapshot only at rows 7 and 43 (equivalent DRC airwire endpoints); duplicate wx image-handler debug messages also appeared.
- `.venv/bin/python scripts/board/release.py --routed --out /tmp/t0005-r8-release` — exit 1 (expected refusal):
  ```text
  routed release refused: {"unconnected_items": 84}
  release_exit=1
  routed False
  routed_requested True
  refused {'unconnected_items': 84}
  drc_errors 0
  drc_warnings 11
  unconnected_items 84
  pcb_tracks 278
  bom_rows 55
  cpl_rows 55
  ```
- `git diff --check main...HEAD` — exit 0, no output. Worktree clean after commit; post-commit hook published only this review lane branch.
