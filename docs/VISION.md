# Elicio: vision and design reference

This is the design-level reference for Elicio. It describes what the project is,
why it exists, what has actually been established, and what is still open. It
contains no code. Read `AGENTS.md` for the engineering conventions and `README.md`
for the current runnable state.

## What Elicio is

Elicio is a meeting point between a person and a language model in the physical
world.

A person produces a small, deliberate physical signal. A personal model trained
on that person's own body converts the signal into an explicit event. A harness
decides what that event is allowed to do, and only then does a language model act.

The canonical project statement puts it this way:

> This project will create a personal neural-input system that translates a
> user's biological signals into instructions for an AI-powered work environment.

The important structural claim is that the harness is the product. Models are
interchangeable parts inside it:

> The custom harness will manage context, model selection, tool access,
> permissions, confirmations, and work execution. Codex, Claude, and other models
> will function as replaceable reasoning and execution engines rather than
> defining the product itself.

That is the whole design thesis. The body is the input. The harness is the
contract. The model is a component that can be swapped without changing what
Elicio is.

## The flow

```text
sensor
  -> personal model trained on the user's own signals
    -> decoded event  (symbol, confidence, timestamp)
      -> harness  (permissions, confidence floors, confirmation)
        -> Codex, Claude, or another compatible model
          -> files, terminal, browser, tests, connected tools
```

Every arrow is a real boundary. The one that matters most is the third.

## The event is the stable interface

Everything upstream of the harness collapses into three values:

```text
(symbol, confidence, timestamp)
```

A keyboard can produce this. A replay fixture can produce this. Eventually a real
electrode can produce this. The harness cannot tell the difference, and that is
deliberate. It means the sensor, the decoder, and the model can each be replaced
independently without renegotiating the interface.

An event names a gesture. It never names a file path, a shell command, or a
target. The action's parameters are fixed when the harness is built, not chosen by
the signal. A misfiring muscle cannot invent a destructive argument.

## Safety is structural, not advisory

Three rules are built into the boundary rather than documented as good practice.

**Confidence rises with consequence.** Harmless actions require 0.60 confidence,
reversible edits 0.75, dangerous actions 0.85.

**Dangerous actions never run from one event.** A second, independent confirmation
gesture must arrive within three seconds. The confirmation is deliberately sourced
from a different muscle group than the command, so one twitch cannot produce both.

**The audit is written before the action, not after.** If the intent record cannot
be written, the action does not run. If the result record fails after the action
ran, the system reports the completed action and the audit failure rather than
hiding either. An action that was not recorded is treated as an action that must
not happen.

## What is deliberately out of scope

The project statement is explicit:

> The project is not initially intended to decode unrestricted thoughts or
> reproduce a person's internal speech.

This is not a brain reading project. It is a small, learnable vocabulary of
deliberate physical gestures. The sensor documentation states the constraint
directly: the personal model sends only the name of the gesture, how sure it is,
and the time. Do not try to decode complete sentences or free thoughts. Meaning
comes from combining that small alphabet with the harness's context, not from
extracting richer signal from the body.

## What the research established

All numbers below are cross-session: train on one recording day, test on a
different day. This is the only measurement the project accepts.

Within-session accuracy on this kind of data reads 98 to 99 percent and is
meaningless, because electrode position and skin state leak between train and
test. That figure appears in the record only as a warning.

Public GRABMyo dataset, 43 subjects, 3 sessions, 16 forearm channels. 23 subjects
had usable data across all three sessions.

| Test | Result |
| --- | --- |
| 17 gestures, classic models | 55 to 57 percent |
| 17 gestures, temporal CNN | 64.9 percent |
| 6 best gestures + rest, gradient-boosted trees | 76.0 percent mean |
| 6 best gestures + rest, temporal CNN | 82.7 percent mean, 8 of 23 subjects at or above 90 percent |
| Later 8-channel run | 79.3 percent mean, 84.3 percent median, 7 of 23 at or above 90 percent |

Channel count matters and the loss accelerates: 64.9 percent at 16 channels, 56.8
at the best 8, 42.3 at the best 3.

A temporal CNN was the best model family tested, beating classic features by 8 to
10 points. GRU and small Transformer variants did worse than classic baselines at
this data scale. CPU inference was 0.24 ms per window, so latency is not the
bottleneck.

Large, mechanically distinct movements separated best: wrist flexion, wrist
extension, forearm rotation. A full fist separated poorly. The best six gestures
were personal rather than universal, though wrist extension and flexion won for 20
of 23 subjects.

### What these numbers do not show

Milestone 1 is 5 to 8 gestures at 90 percent or better cross-session, under 300 ms.
The recorded verdict is that milestone 1 is within reach but not yet met for a
typical person.

None of this was measured on the owner's own arm. There was no person-specific
calibration beyond a normal training session, and no systematic hyperparameter
search. These are public-dataset results, not a working system.

The training code is also not seeded. Torch batch shuffling and model
initialisation are drawn from unseeded global state, so rerunning `train` or
`evaluate` will not reproduce these exact figures. The migrated research
implementation is deliberately preserved as-is, so this is recorded as a known
limitation rather than quietly patched. Making runs reproducible is a real
decision with a real cost: it changes the numbers, which means the evidence trail
above has to be regenerated. That is worth doing before the pipeline is ever run
against a personal recording, and it needs an explicit call first.

## Hardware: decided and open

Nothing has been purchased.

sEMG was chosen over EEG for the first usable layer, because EEG's 2 to 4 classes
and multi-second decisions cannot carry an input alphabet. EEG is deferred, not
rejected, and may later serve as a slow auxiliary state channel.

Research favored an 8-channel dry-sEMG armband. The owner pushed back on cost
directly:

> claude I'm pressing this because 800 dollar band from across the world for a
> project I'm passionate about seems a lil crazy

The response to that was not to argue for the purchase. It was to find a path that
proves the idea for less: a single-channel sensor making one deliberate muscle
contraction complete one real, safe action. Establish the boundary first, buy
resolution later.

The binding hardware constraint is reliable mapping across days, not peak accuracy
within one session. Raw signal access and re-donning repeatability decide whether a
device is usable. A device without documented raw access is rejected regardless of
its marketing.

Still unresolved: optimal channel count, wrist versus proximal forearm placement,
recalibration versus retraining, and facial versus forearm comfort for the
confirmation gesture.

## Where the project actually stands

The software boundary is real and runs today. One simulated gesture event passes
validation and a confidence policy, and an explicit adapter atomically writes a
harmless local file, with a linked intent and result audit pair. A deterministic
one-channel signal fixture runs the full replay, detection, policy, and action
path.

Everything upstream of the event is still synthetic. No hardware exists, no
personal recording exists, and no real sensor signal has completed a harness
action.

The project must not be described as end-to-end until a real signal from a real
body has been recorded, decoded, and used to complete a real action.

## Open design questions

These are the decisions worth a conversation, as opposed to implementation work:

1. **Gesture vocabulary.** Which 5 to 8 gestures earn a slot? The research says
   pick mechanically distinct ones and that the best set is personal.
2. **Confirmation channel.** A jaw or facial gesture is independent from the
   forearm, which is what makes it safe. Is that acceptable to perform in public?
3. **What deserves the dangerous tier.** Currently sending a message and running
   tests. Where is the real line?
4. **Failure feel.** What should a rejected or low-confidence gesture do so the
   person learns the boundary without frustration?
5. **First real action.** One harmless local action is proven. What is the first
   action worth risking on a single muscle contraction?
6. **The cheap proof.** Does one channel and one action justify the 8-channel
   purchase, and what result would settle it?
