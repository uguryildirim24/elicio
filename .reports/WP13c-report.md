# WP13c report — Q75 dropout is a report, S2 continues

Lane `w4`. Branch `lane/w4`. Final commit `21dde8a76a609ea6454773cac8cc093048197504`.
Worktree `/home/user/projects/elicio/.worktrees/w4`.
Python 3.13.15. Extra `ble` installed (bleak 3.0.2).

Host-only. No radio and no board were used.

## What was built

`elicio receive-check` still uses exit 3 when no scored line failed and a montage §8 line 3.4 dropout is present. Exit 3 is a report, not a stop (Q75). The printed output names the dropout count, the longest run in sample intervals (`length − 1`), and the acquisition index where that run began. The last line of an exit-3 run is exactly `S2 continues (Q75); dropout count goes in the session note`. A same-criterion failure still wins: exit 1, with the dropout count printed, and without that continues line. Exit 0 and 2 keep their meaning.

The session record is `sidecar.json`. After a check, it carries `dropout_count`, `longest_run_intervals`, and `longest_run_start_acq`.

`docs/fab/receiver-v2.md`: the open-decision-75 sentence is gone. The exit-code table marks 1 and 2 as stops and 3 as a report (Q75).

`docs/fab/assemble.md`: one sentence after the firmware copy step. At exit 3, write the count in the session note and continue. Stop only on exit 1 or 2.

Tests: dropout only (exit 3 plus the continues line); failure plus dropout (exit 1 plus the count); clean (exit 0). Existing fixture `tests/fixtures/receiver_v2/dropout.json` was enough. `elicio receive --simulate-live` still exits 0.

Files: `src/elicio/receiver_v2.py`, `tests/test_receiver_v2.py`, `docs/fab/receiver-v2.md`, `docs/fab/assemble.md`. One commit. No firmware, board, montage, plan-v2, or open-questions edits.

## Gates

1. `.venv/bin/python -m unittest discover -s tests -v`

   Result: exit 0. `Ran 207 tests in 83.970s` `OK (skipped=26)`. Receiver module: 15 tests, OK.

2. `elicio receive-check` on the three cases (paste below).

3. `git status --short` empty after the commit.

Plan v2 §11 row 13 "builds in CI; bench-tested at S2": no CI in the repo. Host unittest ran. S2 bench was not run (no board). Plan v2 §9 S2 row was not run.

### Clean fixture — exit 0

```
.venv/bin/python -m elicio.cli receive --simulate tests/fixtures/receiver_v2/normal.json --out <tmp>/clean
.venv/bin/python -m elicio.cli receive-check <tmp>/clean
```

```
{
  "dropout_count": 0,
  "dropout_stretches": 0,
  "dropouts": [],
  "duration_s": 0.002,
  "exit_code": 0,
  "loader": "elicio.receiver_v2.load_receiver_session",
  "longest_run_intervals": 0,
  "longest_run_start_acq": null,
  "losses": 0,
  "ok": true,
  "overruns": 0,
  "same_criterion": {
    "3.10": "not_scored",
    "3.5": "not_scored",
    "3.6": "not_scored",
    "3.7": "not_scored",
    "3.8": "not_scored",
    "3.9": "not_scored"
  },
  "same_criterion_failed": [],
  "sample_count": 4,
  "wraps": 0
}
```

Process exit: 0. No continues line.

### Dropout only — exit 3

```
.venv/bin/python -m elicio.cli receive --simulate tests/fixtures/receiver_v2/dropout.json --out <tmp>/drop
.venv/bin/python -m elicio.cli receive-check <tmp>/drop
```

```
{
  "dropout_count": 2,
  "dropout_stretches": 2,
  "dropouts": [
    {
      "channel": 0,
      "kind": 1,
      "length": 205,
      "start_acq": 0
    },
    {
      "channel": 1,
      "kind": 1,
      "length": 205,
      "start_acq": 0
    }
  ],
  "duration_s": 0.1025,
  "exit_code": 3,
  "loader": "elicio.receiver_v2.load_receiver_session",
  "longest_run_intervals": 204,
  "longest_run_start_acq": 0,
  "losses": 0,
  "ok": false,
  "overruns": 0,
  "same_criterion": {
    "3.10": "not_scored",
    "3.5": "not_scored",
    "3.6": "not_scored",
    "3.7": "not_scored",
    "3.8": "not_scored",
    "3.9": "not_scored"
  },
  "same_criterion_failed": [],
  "sample_count": 205,
  "wraps": 0
}
dropout count: 2
longest run: 204 sample intervals beginning at acq_index 0
S2 continues (Q75); dropout count goes in the session note
```

Process exit: 3.

### Same-criterion failure plus dropout — exit 1

The dropout session above, with `sidecar.json` `same_criterion["3.7"] = "fail"`.

```
{
  "dropout_count": 2,
  "dropout_stretches": 2,
  "dropouts": [
    {
      "channel": 0,
      "kind": 1,
      "length": 205,
      "start_acq": 0
    },
    {
      "channel": 1,
      "kind": 1,
      "length": 205,
      "start_acq": 0
    }
  ],
  "duration_s": 0.1025,
  "exit_code": 1,
  "loader": "elicio.receiver_v2.load_receiver_session",
  "longest_run_intervals": 204,
  "longest_run_start_acq": 0,
  "losses": 0,
  "ok": false,
  "overruns": 0,
  "same_criterion": {
    "3.10": "not_scored",
    "3.5": "not_scored",
    "3.6": "not_scored",
    "3.7": "fail",
    "3.8": "not_scored",
    "3.9": "not_scored"
  },
  "same_criterion_failed": [
    "3.7"
  ],
  "sample_count": 205,
  "wraps": 0
}
dropout count: 2
longest run: 204 sample intervals beginning at acq_index 0
```

Process exit: 1. No continues line.

`elicio receive --simulate-live` still exits 0 (unittest `test_cli_simulate_live`).

## What was not done

No radio. No board. No gel montage. `docs/fab/montage.md` was not edited. `docs/fab/plan-v2.md` and `docs/fab/open-questions.md` were not edited. Firmware and board files were not edited.

A local unversioned `post-commit` hook ran `git push` after the commit on `lane/w4`. This lane did not invoke `git push`.

## Needs a decision

None. Q75 is the reading this package follows.

## Final sha

`21dde8a76a609ea6454773cac8cc093048197504`
