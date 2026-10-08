# Engineering scope

The research pipeline was migrated from a Claude Science development project. Private project IDs, workspace paths and conversation records are intentionally excluded. Public data preparation and migration scope are described in [RESEARCH_PROVENANCE.md](RESEARCH_PROVENANCE.md).

## Boundaries

- The intended device is an ear-muscle EMG earpiece. Hardware is unfinished and unordered.
- The implemented proof uses synthetic input and a fixed-path local marker adapter.
- Other action names are console simulations. No AI execution adapter exists.
- The event is `(symbol, confidence, timestamp)`. It carries neither a path nor a shell command.
- Consequential actions require confirmation. The tuple cannot establish independent muscle sources.
- Intent auditing must succeed before execution. Post-action audit failures remain visible.
- Research evaluation must use separate recording sessions through `cross_session_split` and `assert_no_session_leakage`.
- Preserve raw acquisition records. Recordings and anatomy measurements belong in ignored local directories, not in public examples.

Rolf directs design choices. Purchases, vendor contact, publication and real consequential actions require Rolf's explicit approval. Coding agents do not commit or push.

See the root README for runnable commands and [EARPIECE_DESIGN.md](EARPIECE_DESIGN.md) for the current hardware inventory and next steps.
