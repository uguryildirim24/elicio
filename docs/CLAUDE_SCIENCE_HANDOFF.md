# Claude Science handoff

Read this file before beginning Elicio engineering work.

## Project purpose

Elicio translates the user's biological signals into small, explicit gesture
events. A separate harness maps those events to AI-assisted work while applying
confidence thresholds, permission rules, and independent confirmation for
dangerous actions.

It is not intended to decode unrestricted thoughts or internal speech.

## Source project

- Claude Science project name: `Elicio`
- Claude Science project id: `proj_329a0b4f3b3a`
- Organization root:
  `/Users/uguryildirim/.claude-science/orgs/2755aa35-59e8-4420-aafc-8f2176cb6050`
- Main research workspace:
  `workspaces/db1c321f-2691-4450-99b3-f03c4cbe2ef0`
- Hardware and latest eight-channel workspace:
  `workspaces/97322daa-0e54-4e21-9ef3-6d37f68ed1d6`
- Artifact storage:
  `artifacts/proj_329a0b4f3b3a`

Treat the Claude Science project as read-only evidence. Do not reorganize,
delete, or edit it during migration.

## Established research results

- The first modality is surface electromyography (sEMG), not EEG.
- Honest evaluation means training on one recording session and testing on a
  different later session. Same-session splits are not accepted as proof.
- Milestone 1 is 5 to 8 gestures at 90 percent or better cross-session
  accuracy, with no more than 300 milliseconds decision latency.
- A Temporal CNN was the best tested model family.
- On 23 GRABMyo subjects, personalized six-gesture-plus-rest recognition
  reached 82.7 percent mean accuracy with 16 channels.
- The latest eight-channel run reached 79.3 percent mean accuracy, 84.3 percent
  median accuracy, and 7 of 23 subjects at or above 90 percent.
- Large, mechanically distinct movements such as wrist flexion, wrist
  extension, and forearm rotation separated best. A full fist separated poorly.
- The milestone is promising but has not been met for a typical person, and it
  has not been tested on the user's own body.

Latest eight-channel result:

`workspaces/97322daa-0e54-4e21-9ef3-6d37f68ed1d6/six_best_rest_8ch_summary.csv`

## Existing software to inspect and migrate

- Simulated harness:
  `workspaces/db1c321f-2691-4450-99b3-f03c4cbe2ef0/milestone0.py`
- Final pipeline README artifact:
  `artifacts/proj_329a0b4f3b3a/d83ec363-744e-410d-b5cc-9b854a45bd51/v784d1137_README.md`
- Final result report artifact:
  `artifacts/proj_329a0b4f3b3a/6e3c5863-4a57-4f25-9a16-e0f2de629497/v5dc65755_results_final.md`

The pipeline package was stored as separate artifacts with repeated filenames.
Resolve the latest final package versions carefully. Do not copy an earlier
`load.py`, `features.py`, or similarly named intermediate artifact by mistake.

## Current hardware decision

No purchase has been made.

Research favored an eight-channel MindRove Armband 2 over three-channel Mudra
and two-channel Elemyo for the full milestone. The user considers the roughly
$799 price too large for an unproven passion project. The latest proposed path
is therefore a low-cost, one-channel proof first: use a MyoWare-class sensor to
make one deliberate muscle contraction confirm one real, safe action. Exact
parts, current prices, seller terms, and any purchase still require the user's
explicit approval.

## First engineering slice

Build the smallest real vertical slice before adding hardware:

1. Import the final research pipeline and simulated harness into coherent
   packages in this repository.
2. Add tests for the event contract, confidence thresholds, confirmation
   timeout, rest handling, and session-leakage guard.
3. Replace one printed simulated action with one real but harmless local action
   behind an explicit adapter.
4. Keep a complete audit log showing the event, policy decision, and result.
5. Document one command that runs the verified demonstration.

Do not describe the project as end-to-end until a real sensor signal has been
recorded, decoded, and used to complete a real harness action.

## Safety and authority

- Do not purchase hardware, contact vendors, send messages, publish anything,
  or perform final submissions without explicit user approval.
- Dangerous actions must never run from a single biological event.
- Keep raw sensor data and timestamps as the permanent source record.
- Preserve provider independence. Codex, Claude, and other models are
  replaceable reasoning engines behind the harness.
