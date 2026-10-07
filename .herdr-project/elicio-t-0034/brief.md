plain: Remake the photo-style pictures and the 3D model for the new 18 millimetre earpiece.

# Task

## Lead brief

# Photo-style pictures and a 3D model of the 18 mm Elicio earpiece

Elicio is Rolf's custom behind-the-ear EEG earpiece. What Rolf gets from this project is "a picture": photo-style pictures and a 3D model he can turn on his phone. The first set (lane t-0003, branch `origin/hp/elicio/t-0003-give-rolf-the-earpiece-in-3d-and-as-phot`) showed the old 22 mm design. The body is now 18 × 8.1 mm on a new routed board. Make the pictures and the model again for the new design.

## Inputs

Merge these into your branch with `--no-edit`, and don't rebase:
- `origin/hp/elicio/t-0003-give-rolf-the-earpiece-in-3d-and-as-phot`: the renderer `scripts/cad/assemble_photo.py`, `scripts/cad/render.py` and `docs/fab/assemble.md`;
- `origin/hp/elicio/t-0032-design-and-measure-lid-closure-options-f`: the v4 shell and its closure variants. Use **`docs/fab/cad/v4-snap/`**, the soft snap latch. It's the likely pick, and its latch is hidden, so the outside looks the same whichever closure Rolf chooses;
- `origin/hp/elicio/t-0019-close-the-last-open-connections-on-the-v`: the routed v4 board. Run `scripts/board/release.py --board elicio-v4 --routed` to regenerate `hardware/board/release/elicio-v4/elicio-v4.step`, and use `docs/fab/board-v4-design.md` §10.2 for the folded sites.

## The work

1. **Extend the assembly script** for v4 so it builds the assembled earpiece from committed outputs only, with no hand-placed geometry:
   - v4-snap body and lid;
   - the folded v4 board placed by the §10.2 folded sites (flat board STEP plus fold transforms, or clean boxes at the courtyards if a true fold isn't practical; say which);
   - the 501012 cell;
   - three titanium M2.5 button heads at P1–P3;
   - the P4/P5 charging heads in the posterior wall.

   There's no lid screw on v4.
2. **The model.** Export a GLB under 15 MB that opens in a web viewer.
3. **The renders.** At least seven photo-style PNG renders, each under 2 MB: on-ear side, skin side, top, three-quarter, exploded, inside with the lid off, and one beside a US-quarter disc for scale. Use the same finish as before: natural grey PA12 with titanium heads. Also add one side-by-side of the old 22 mm and new 18 mm bodies at the same scale, if the old solids are in the repo.
4. **Captions.** Every picture states the commits it shows. Write a `captions.json` like t-0003's.
5. **Hand over.** Put the GLB, the PNGs and `captions.json` in your lane's library folder, so the coordinator can publish them to Rolf's page.

## Rules

- **Memory.** This Mac ran out of memory once on this project. Run one Blender or CAD job at a time, and close what you start.
- **Files you may edit:** the render and assembly scripts and docs only. Don't change shell CAD, board files or the plan.
- **No spending or uploads.** No purchase, upload or vendor contact.
- **Git.**
  - Never `git stash`.
  - Pass `--no-edit` to merges and `-m` to commits.
  - Commit in steps with true messages.

## Done means

The task's acceptance conditions. The report opens with one short paragraph Rolf can read on his phone: what the pictures show and what's still only approximate, for example board parts drawn as blocks.

## job-0003 — Give Rolf the earpiece in 3D and as photo-style pictures: an assembled 3D model he can turn on his phone and realistic renders from several angles

Requests: request:q-1790170873805-83781

Acceptance conditions:
1. One committed script builds the assembled earpiece (body, lid, board, cell, electrode heads, charging pads, screw) from the committed CAD and board outputs, with no hand-placed geometry
2. A GLB file of the assembled earpiece under 15 MB that opens in a web 3D viewer
3. At least six photo-style renders (on-ear side, skin side, top, three-quarter, exploded, inside with the lid off) as PNG, each under 2 MB, in the chosen titanium-look or finish colour with the colour stated
4. Renders and the GLB are regenerated from the final shell and board commits once those land, and each picture says which commit it shows

# Instructions in force

<!-- n-0003 · 2026-09-25 · request:adeherdr/q-1790295901101-67630 -->
Rolf, 2026-09-24: keep working until this project's goal is reached. When a lane or task is blocked, or nothing is running, pick the next useful step toward the goal and start it; ask Rolf only what truly needs him, without stopping other work. Implementation lanes run on gpt-6-sol high and reviewer lanes on gpt-6-sol xhigh; routing picks this, so start lanes without a recipe override.

# Facts in force

## n-0004

<!-- n-0004 · 2026-09-25 · request:adeherdr/q-1790295901101-67630 -->
The adeherdr coordinator turned nudge on in PROJECT.md (2026-09-25 ~08:20Z) for Rolf's request that every coordinator churn: when this coordinator is idle with no lane working, the ticker asks it for the next step about every 20 minutes. Automated prompts will wait while Rolf has text typed in this pane once adeherdr W117 lands.

## n-0002

<!-- n-0002 · 2026-09-23 · request:q-1790177634256-92066 -->
Rolf, 2026-09-23: he likes the design but the body is too big horizontally (22 mm wide, 9.0 thick), and part changes are the way he expects to make it smaller; a smaller body is the main goal of the board redesign.

# Repository, machine and pinned gates

- Repository: `/home/user/projects/elicio`.
- Machine: local.
- Gates: not configured for this repository.

# Finish

Commit the finished work, then run `ha done --report /home/user/projects/elicio/.worktrees/t-0034/.herdr-project/elicio-t-0034/report.md --sha <commit-sha>`.

# Paths

- Report: `/home/user/projects/elicio/.worktrees/t-0034/.herdr-project/elicio-t-0034/report.md`
- Library folder for files meant for Rolf: `/home/user/projects/elicio/.worktrees/t-0034/.herdr-project/elicio-t-0034/library`
