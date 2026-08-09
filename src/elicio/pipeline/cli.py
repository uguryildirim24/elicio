"""Single command-line entry point for the muscle-signal (sEMG) pipeline.

This file gives THREE commands. Each command wraps one existing
script in this package; nothing about the underlying logic changes.

  prepare   Download and window one or more subjects' raw signal,
            compute the standard features, and save one file per
            subject. Wraps ``prepare_subjects.py``.
  train     Train and score the baseline classifiers and neural
            networks for one or more subjects, at three channel
            counts. Wraps ``train_and_eval.py``.
  evaluate  Score the "six best gestures plus rest" reduced gesture
            set for one or more subjects. Wraps ``six_best_rest.py``.

WORD LIST
---------
subject   One person in the dataset. Given as a number, for example
          ``--subjects 1 2 3``.
channel   One electrode. A channel count is how many electrodes a
          device or a comparison run uses.
CLI       Command-Line Interface. A program you run by typing a
          command, instead of clicking buttons.

USAGE
-----
  python -m elicio.pipeline.cli prepare  --subjects 1 2 3 --out-dir results
  python -m elicio.pipeline.cli train    --data-dir results --subjects 1 2 3 \\
                                       --epochs 20 --out results/train_results.csv
  python -m elicio.pipeline.cli evaluate --data-dir results --subjects 1 2 3 \\
                                       --epochs 20 --out results/six_best_rest.csv

Run ``python -m elicio.pipeline.cli <command> --help`` for a command's
own option list.

PLUGGING IN YOUR OWN RECORDINGS
--------------------------------
The ``prepare`` command above is built for the public GRABMyo
dataset only. To run this pipeline on your OWN sensor recordings
instead, you do not edit ``train`` or ``evaluate`` at all -- you write
one new loader function that produces the same ``Recording`` objects
that ``load.py`` defines (see the "STANDARD FORM" section at the top
of ``load.py``), save its output the same way ``prepare_subjects.py``
does (one ``.npz`` file per subject, with the same field names), and
then point ``train``/``evaluate`` at that folder with ``--data-dir``.
See the "Adding your own recordings" section of ``README.md`` for the
exact steps.
"""
from __future__ import annotations

import sys


def _run_prepare(argv):
    from . import prepare_subjects

    return prepare_subjects.main(argv)


def _run_train(argv):
    from . import train_and_eval

    return train_and_eval.main(argv)


def _run_evaluate(argv):
    from . import six_best_rest

    return six_best_rest.main(argv)


COMMANDS = {
    "prepare": _run_prepare,
    "train": _run_train,
    "evaluate": _run_evaluate,
}


def main(argv=None):
    argv = sys.argv[1:] if argv is None else list(argv)

    if not argv or argv[0] in ("-h", "--help"):
        print(
            "usage: elicio-emg <command> [options]\n\n"
            "Muscle-signal (sEMG) gesture pipeline: prepare, train, evaluate.\n\n"
            "commands:\n"
            "  prepare   download raw signal, window it, compute features\n"
            "  train     train and score baseline models and networks\n"
            "  evaluate  score the six-best-gestures-plus-rest subset\n\n"
            "Run 'elicio-emg <command> --help' for a command's own options."
        )
        return

    command, rest = argv[0], argv[1:]
    if command not in COMMANDS:
        print(f"unknown command: {command!r}. Choose one of: {list(COMMANDS.keys())}")
        raise SystemExit(2)

    # ``rest`` (including any --help in it) is handed to the wrapped
    # script's OWN argparse parser untouched, so ``elicio-emg prepare
    # --help`` shows that command's real options, not this wrapper's.
    COMMANDS[command](rest)


if __name__ == "__main__":
    main()
