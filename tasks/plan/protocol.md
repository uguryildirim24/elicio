# plan — spec round for the earpiece fabrication plan (shared protocol)

Goal: `docs/fab/plan.md`, the Phase 0 synthesis and Phase 1 specification for
the Elicio earpiece shell. Written from `docs/fab/brief.md`,
`docs/EARPIECE_DESIGN.md`, and the four lane reports `docs/fab/L1-cad.md`,
`docs/fab/L2-vendors.md`, `docs/fab/L3-contacts.md`, `docs/fab/L4-pod.md`. It
must resolve every cross-lane conflict explicitly and be precise enough that a
CAD worker can script the fit-check shell and Rolf can place the first order
without asking questions.

Participants:

- `fable`: author. A Claude lane in the elicio herdr workspace, working in the
  main checkout at `/home/user/projects/elicio`. Owns `docs/fab/plan.md`
  and its turn files `tasks/plan/turns/NN-fable.md`.
- `pro`: adversarial reviewer. GPT-6 Pro in a ChatGPT chat with Rolf's local
  files (pro-mcp). Owns `tasks/plan/turns/NN-pro.md`. Cannot run commands or
  commit.
- `elicio`: coordinator, herdr pane `w1B:p1`. Relays turns, commits every
  file, ends the round.

## Turn mechanics

- Turns are numbered 01, 02, 03 and alternate: odd turns are `fable`, even
  turns are `pro`. Each turn is one new file under `tasks/plan/turns/`. Never
  overwrite a previous turn file.
- `fable`, when a turn is done: make sure `docs/fab/plan.md` and
  `tasks/plan/turns/NN-fable.md` are written, then run, in order:

      herdr pane report-metadata "$HERDR_PANE_ID" --source lane --token lane=plan --token turn=NN
      herdr agent prompt elicio "DONE plan-NN tasks/plan/turns/NN-fable.md -"

  and end the turn. The next turn arrives later as a prompt from `elicio`.
  Do not message `pro`, do not poll, do not read other panes. If the prompt
  command fails, run it once more; a turn that ends silently is the one
  failure nothing catches.
- `pro`, when a turn is done: write `tasks/plan/turns/NN-pro.md` with
  `write_doc`, then `herdr_prompt elicio: "DONE plan-NN tasks/plan/turns/NN-pro.md -"`.
- `elicio` commits each turn file (and `plan.md`) on `main`, then prompts the
  other participant with the next turn number, the commit it should read, and
  the path of the file to answer.

## Review format (`pro`)

Header: the `plan.md` commit reviewed (the TURN line names it) and what was
read. Then numbered findings. Numbering continues across turns: turn 02 starts
at 1, turn 04 continues where 02 stopped. Each finding carries a severity
(blocker, major, minor), the `plan.md` section, what is wrong, the evidence (a
URL, a lane-report line, a datasheet), and a concrete fix. Only new findings
or findings still unresolved from the previous round; never restate a resolved
one. Verify prices and claims on the web where the lanes did not: the lane
reports marked almost nothing UNVERIFIED. End with a section `## For Rolf`,
then the last line exactly `SIGNED OFF` or `NOT SIGNED OFF`.

## Revision format (`fable`)

`tasks/plan/turns/NN-fable.md`: every finding from the previous `pro` turn,
by number, marked accepted (what changed, which section), rejected (why, with
evidence), or carried (see below). Then one paragraph summarising the
`plan.md` changes. Turn 01 instead records every decision made, every
conflict and its pick, and what could not be settled.

## Rounds: until they settle

Open-ended. Rolf, 2026-09-16: "not once or twice but till they settle; only if
it gets nitpicky you intervene."

- `pro` signs off when no blockers or majors remain. Remaining minors go to
  `## For Rolf` or become carried items; they do not cause another round.
- A finding `fable` rejected may be re-argued once by `pro`, with new
  evidence. If rejected again it goes to `## For Rolf` and is closed.
- Carried items: a finding whose fix lives inside one Phase 1 work package
  and changes no other package's contract may be carried as a numbered item
  in the plan's "Open items" section, naming the work package and the check
  that closes it. `SIGNED OFF` with carried items is a valid verdict.
- Nitpicky rule: when `elicio` judges the remaining findings cosmetic
  (wording, ordering, formatting, restating a logged decision), it ends the
  round and takes `plan.md` as it stands. Findings still open at that point
  go to "Open items".
- On `SIGNED OFF`, `fable` does one final pass: applies newly accepted items,
  completes "Open items" and "Open for Rolf", writes the final turn file, and
  pushes DONE. No further turns.

## Rules

- No git commits by `fable` or `pro`. `fable` edits only `docs/fab/plan.md`
  and its own turn files. Nobody edits `docs/EARPIECE_DESIGN.md`, the lane
  reports, the briefs, or code. Folding the plan into the design record is a
  later work package.
- Nobody purchases, signs up, requests a quote, uploads a file to a vendor,
  or contacts anyone. Purchases need Rolf's explicit approval
  (`docs/CLAUDE_SCIENCE_HANDOFF.md`).
- Web search: `fable` only to verify a citation or a price; `pro` as much as
  it needs for verification. No new research lanes.
- Plain prose. Tables for numbers, parts, dimensions, costs, and work
  packages. Types and rules, not essays.
- Size: `plan.md` stays under 6,000 words. If it grows past that, cut prose,
  not tables.
- Lane reports are evidence, not law. When lanes conflict, `plan.md` picks one
  and says why. When a lane number looks wrong, say so and mark it.

## What `plan.md` must contain

1. Decision summary: the route in ten sentences or fewer (tool, geometry
   capture, vendor and material, contacts, electronics envelope, first order).
2. Conflicts resolved: a table of every cross-lane disagreement, with the pick
   and the reason. At least: battery 50 versus 110 mAh; envelope 33 x 10.5 x
   6.8 mm versus 35 x 20 x 12 mm; titanium versus 316L versus gold-plated
   studs; conductive TPU; screws versus snap lid; resin versus nylon for the
   fit-check shell.
3. Fit-check shell specification: tool (build123d unless the author argues
   otherwise), script path, every parameter with default, unit, and the
   caliper measurement it maps to; features (three electrode bosses sized for
   the chosen contact, the board and battery envelope from L4, lid, glasses
   relief, ear hook); design rules for the chosen JLCPCB process (wall
   thickness, clearances, tolerances); outputs (STEP, STL, 3MF, two renders,
   one drawing); and acceptance: what Rolf checks when he wears it.
4. Contacts specification: count, material, geometry, suspension, sourcing
   candidates with prices, nickel verification steps, how they mount and how
   the leads terminate.
5. Electronics envelope handoff: the dimensions and mounting features the
   shell reserves for the Stage B board and battery, per L4. The board itself
   is out of scope.
6. Skin, safety, hygiene: material rationale, cleaning, and the battery-only
   and series-protection rules restated as constraints on the shell.
7. Orders: order 1 (fit-check) and order 2 (Stage B shell) with vendor,
   process, material, files, all-in cost, lead time, and exactly what Rolf
   does. Every price with its source page and date, and an UNVERIFIED mark
   where it came from a lane without a page.
8. Claims to verify before ordering: a table of the numbers the plan depends
   on, each with its source and who verified it.
9. Phase 1 work packages, one worker each, one to three days: owned files,
   inputs, outputs, acceptance. Ordered so the fit-check shell files arrive
   first.
10. Open items (carried findings, numbered) and Open for Rolf (decisions only
    he can make: measurements, material choice, purchases, whether to take an
    impression).
