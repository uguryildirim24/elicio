# Phase 1 — rules every lane brief includes by reference

Spec: `docs/fab/plan.md`, signed off by GPT-6 Pro at commit `0c5d0eb`
(turns in `tasks/plan/turns/`). `docs/EARPIECE_DESIGN.md` holds the
requirements the plan serves. Where your brief, the plan and the design
record disagree, the plan wins and you say so in your report.

Coordinator: herdr agent `elicio`, pane `w1B:p1`. Integration branch: `main`.

## Environment

Your worktree is `/Users/rolfie/projects/elicio/.worktrees/<lane>` on branch
`lane/<lane>` from `main`. Work only there. Create your own environment
inside it, never in another worktree or the main checkout:

    python3.13 -m venv .venv && .venv/bin/python -m pip install -e .

Add optional dependencies your package needs to `pyproject.toml` under a new
optional-dependencies group (for example `cad`) and install with
`.venv/bin/python -m pip install -e '.[cad]'`. Python 3.13 is the only
interpreter on this Mac; if a dependency has no 3.13 wheel, `uv python
install 3.12` and use that for your `.venv`, and record it in your report.

## Gates (every lane, before DONE)

    .venv/bin/python -m unittest discover -s tests -v

stays green (stdlib `unittest`, no pytest, see `AGENTS.md`). Your package's
own acceptance row in plan §9 is the second gate; your report shows the
command and the result for each item, or says it was not run and why.

## Rules

- Commit on your lane branch only, small commits, conventional messages.
  Never push. Never merge. Never touch `main`, another worktree, or another
  package's owned files. `git status --short` is empty at DONE.
- No purchase, sign-up, quote request, upload to a vendor, or vendor
  contact. Purchases need Rolf's explicit approval
  (`docs/CLAUDE_SCIENCE_HANDOFF.md`).
- Web only to read a datasheet, a standard, or a product page for a
  dimension, price or material fact your package needs. Cite the URL and the
  date you read it. No new research.
- Do not edit `docs/fab/plan.md`. If the plan is wrong or ambiguous for
  your package, implement the reading plan §10 supports, and record the
  problem under "Needs a decision" in your report. Interface-level changes
  go into `docs/fab/interface.md` version notes (WP1/WP6), never silently
  into code.
- Plain prose in docs; tables for numbers, parts, dimensions, costs.
- Nothing is claimed verified that was not run.

## Report and closing steps (verbatim, from inside your worktree)

Report: `.reports/<PKG>-report.md` in your worktree, with: what was built,
each plan §9 acceptance item and how it was verified (command, result), what
was not done, "Needs a decision", the final commit sha.

Then run, in order:

    herdr pane report-metadata "$HERDR_PANE_ID" --source lane --token lane=<PKG> --token done=1
    herdr notification show "<PKG> done" --body "lane <lane>" --sound done
    herdr agent prompt elicio "DONE <PKG> .reports/<PKG>-report.md <final commit sha>" || herdr agent prompt elicio "DONE <PKG> .reports/<PKG>-report.md <final commit sha>"

If you must stop and wait on something outside yourself (Rolf, a part, a
service), before you stop:

    herdr pane report-metadata "$HERDR_PANE_ID" --source lane --token lane=<PKG> --token waiting="<what>"
    herdr agent prompt elicio "WAITING <PKG> <what>"

Your turn must end with one of those pushes, including when the package
fails. A lane that stops silently is the one failure nothing catches.
