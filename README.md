# Elicio

Elicio is a personal biological-input layer for an AI work environment.

The intended flow is:

```text
body sensor -> personal decoder -> gesture event -> safety harness -> AI tools
```

The stable decoder event is:

```text
(symbol, confidence, timestamp)
```

## Current status

Claude Science completed the first research phase. It established the initial
surface-EMG direction, built a reusable training pipeline, compared model
families and channel counts, and produced a simulated safety harness.

Elicio is not yet an end-to-end product. No hardware has been purchased. The
current harness prints simulated actions, and no personal sensor recordings
exist yet.

The engineering phase starts in this repository. Read
`docs/CLAUDE_SCIENCE_HANDOFF.md` before importing or changing the research
artifacts.

