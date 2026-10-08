# Elicio: purpose and boundaries

Rolf chose a behind-the-ear device for deliberate, discreet input to an AI work environment. The intended input is auricular muscle EMG. A contraction should become an explicit event before any action is allowed.

```text
ear-muscle signal -> decoder -> (symbol, confidence, timestamp) -> policy -> action
```

This is a design goal, not a demonstrated biological interface. The board is unfinished and has not been ordered. No physical earpiece or real EMG recording has been validated.

## Why an explicit gate

The event boundary keeps sensing separate from execution. A decoder supplies a gesture name, confidence and time. It cannot supply a file path or shell command. The adapter fixes its target in advance.

The implemented policy applies confidence floors and a timed confirmation rule. Intent auditing happens before execution. Failure to write that intent blocks the action. Failure to write a result after execution is reported without pretending the action did not occur.

The confirmation symbol is `jaw_clench`. Distinct symbols do not prove distinct muscle sources. The current event contract has no channel identity or physiological independence check. A real device must establish that property upstream before connecting consequential actions.

## Present evidence

The synthetic demos exercise policy, audit records and an atomic local marker write. The binary receiver also accepts committed synthetic transport fixtures. No model execution adapter is implemented.

The research package prepares public forearm sEMG data and compares decoders across recording sessions. Forearm classification is not evidence of ear-muscle decoding. Earlier research summaries were imported from private workspaces. Their result CSVs, checkpoints and timing reports are not included here, so this repository makes no measured accuracy or inference-latency claim. See [research provenance](RESEARCH_PROVENANCE.md).

## Decisions and open work

Rolf selected the earpiece form, deliberate physical gating, titanium contact hardware, limited final assembly and off-ear-only charging. AI coding agents translated those constraints into software and design files. Software checks and CAD geometry checks are not physical safety or fit tests.

The next proof should remain small: resolve fabrication and electrical blockers, finish the product firmware variant, check physical fit and retention, then record a real signal and use it for one harmless local action. A model adapter and a reliable independent confirmation channel are later work.

The project does not attempt thought decoding or unrestricted internal speech. It is not a medical device or a finished wearable.
