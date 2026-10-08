# Scripted shell CAD

The selected candidate is the committed `docs/fab/cad/v4-snap/` body and lid. The board is unfinished and unordered. No shell has been printed or fit-validated.

## Install and generate

From the repository root with Python >=3.11:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[cad]'
.venv/bin/python scripts/cad/build_shell_v4.py --closure snap --out .reports/cad/v4-snap
.venv/bin/python scripts/cad/render_v4.py --single --out .reports/cad/v4-snap
```

All generated output belongs under ignored `.reports/cad/`. Do not overwrite tracked reference exports during routine checks. The CAD extra pins the kernel used for geometry exports. Library versions can still change render bytes. Regeneration is not physical validation.

`build_shell_v4.py` reads board courtyard envelopes from `docs/fab/board-v4-design.md` section 10.2. Its manifest records nominal geometry and key-clearance checks. The base `--closure hinge` is a reference without lid retention. `--closure m16` remains a diagnostic prototype. Its 0.13 mm head-well wall rejects it for printing. Committed M1.6 exports remain as evidence, not a print candidate.

See [shell limits](../../docs/fab/shell-v4.md) for print and load questions.

## Reference fixtures

`bte_fit_shell.py`, `placement.py`, `placement_v2.py` and `layout_v2c.py` retain the original construction, packing searches and document generator. The older PCB reader uses revision `845bac7` for board dimensions and project rules. J4 geometry prefers revision `30ca79d`. Shell readers prefer pinned packing revisions. These are read-only Git operations, but the inputs depend on history. A history rewrite can invalidate them. They must not be replaced by a later PCB without checking the changed geometry and rules.

The v1/v2 solids, matrix drawings, v2c grid drawings and packing tables remain reference inputs. The earlier shell reader combines section 5c courtyards and holes with section 5d folded pads and extras. Section 5e supplies the later wall-site geometry. The v4 generator reads `board-v4-design.md`, not either older placement table. Superseded fit-gauge ordering instructions do not define the current build. Historical technical source surveys L1 to L8 remain. `docs/fab/references.md` indexes key sources. Private task and review dialogue is not included.

`placement.py` retains `--packing-doc`, `--layout-v2` and `--layout-v2c`. The first regenerates tracked `docs/fab/packing-v2.md`; the grid option writes its reference drawings. Run these only when deliberately regenerating the references. Matrix drawing options are `--all`, `--kept-drawings` and `--all-drawings`, with `--out-dir` for a separate output directory. The full grid and document searches can be lengthy.

Existing tests still compare regenerated CAD and render bytes with committed hashes. Kernel versions, Git provenance and rendering dependencies can affect those comparisons. The scope review did not weaken those checks or claim a complete suite pass.

A reference-only check without the CAD kernel:

```bash
.venv/bin/python scripts/cad/bte_fit_shell.py --checks-only
```

A new reference export, with the CAD extra installed:

```bash
.venv/bin/python scripts/cad/bte_fit_shell.py --out .reports/cad/reference
```

The default M1 to M8 dimensions are examples. They are not Rolf's measurements. Put any later anatomy overlay under ignored `measurements/`, then pass its path through `--params`. Do not fill a tracked parameter file with personal measurements. Check supported parameters with `--help`. The full v4 folded fit must be re-evaluated after parameter changes.

## Optional assembly visualizations

`assemble_native.py` uses SceneKit/Swift on macOS or Blender on Linux. It also needs Pillow. It reads the committed shell STL and board data and generates simplified curved board and package envelopes, not a folded physical assembly.

```bash
.venv/bin/python -m pip install Pillow
.venv/bin/python scripts/cad/assemble_native.py --out .reports/cad/assembly
```

`assemble_photo.py` provides a Blender render path. Rendering also uses read-only git provenance. These pictures do not prove clearances, package tolerances, RF performance or manufacturability. Preview generation was not rerun during publication cleanup.

## Font

`fonts/LiberationSans-Regular.ttf` is bundled for CAD embossing. Its separate SIL Open Font License 1.1 and attribution are in `fonts/OFL.txt`. The project MIT license does not replace that notice.
