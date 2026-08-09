# emg_pipeline

A reusable pipeline for the muscle-signal (sEMG) gesture-decoding
project. This package prepares public training data, trains gesture
decoders, and scores them the same honest way every time: train on
one recording session, test on a later, different session.

## Word list

Read this list first. Every word below is used later in this file.

| Word | Meaning |
|---|---|
| sEMG | Surface electromyography. A muscle signal picked up by electrodes placed on the skin, not inside the body. |
| gesture | One hand or wrist movement the pipeline learns to recognize, for example "fist" or "rest" (arm relaxed). |
| channel | One electrode. A device with 8 channels has 8 electrodes. |
| window | A short, fixed-length slice of signal that one gesture decision is made from (200 ms in this pipeline). |
| session | One recording sitting: one day, one time the sensor band was put on. |
| cross-session accuracy | How well a decoder trained on one session performs on a LATER, different session. The only honest accuracy number for a wearable, because sensor placement shifts a little every time the band goes back on. |
| subject | One person in the training dataset. |
| CLI | Command-Line Interface. A program you run by typing a command, instead of clicking buttons. |
| epoch | One full pass of a neural network over its training data during training. |

## What this package contains

```
elicio/pipeline/
  config.py          one file with every shared setting (window length, epoch count, file paths)
  cli.py             the three commands: prepare, train, evaluate
  load.py            Recording standard form + the GRABMyo public-dataset loader
  features.py        windowing (200 ms / 50 ms step) + 5 standard sEMG features
  splits.py          the ONLY split function; blocks any accidental same-session leakage
  models.py           LDA, linear SVM, Gradient-Boosted-Trees baseline classifiers
  net_models.py       Temporal_CNN, GRU, Transformer neural networks
  prepare_subjects.py the "prepare" script (streams GRABMyo, windows, saves .npz per subject)
  train_and_eval.py   the "train" script (16 vs 8 vs 3 channels, all six models)
  six_best_rest.py    the "evaluate" script (six best gestures + rest, milestone check)
  README.md           this file
```

## The three commands

Run every command from the folder that CONTAINS `elicio/pipeline/` (one
level above this file), with that folder on `PYTHONPATH`:

```bash
export PYTHONPATH=.

# 1. prepare: download raw signal for chosen subjects, window it,
#    compute features, save one file per subject to results/
python -m elicio.pipeline.cli prepare --subjects 1 2 3 --out-dir results

# 2. train: train and score the baseline models AND the neural
#    networks, at 16, 8, and 3 channels, for chosen subjects
python -m elicio.pipeline.cli train --data-dir results --subjects 1 2 3 \
    --epochs 20 --out results/train_results.csv

# 3. evaluate: score the reduced "six best gestures + rest" set,
#    the milestone-1 target set
python -m elicio.pipeline.cli evaluate --data-dir results --subjects 1 2 3 \
    --epochs 20 --out results/six_best_rest.csv
```

Each command has its own `--help`, for example
`python -m elicio.pipeline.cli prepare --help`.

The `train` and `evaluate` commands need the `torch` neural-network
library. Install it before running them:
`pip install torch` (or the matching `manage_packages` install on a
Claude Science host). The `prepare` command does not need `torch`.

Per project rule, do not run `train` or `evaluate` on this laptop —
both loop neural-network training over many subjects and belong on
remote compute (see the project's compute setup). `prepare` for a
small number of subjects is light enough to run locally if needed.

## One configuration file

`config.py` holds every setting the three commands share: window
length, step length, epoch count, default file paths, and the
channel counts compared in `train`. Change a value there once; every
command picks it up. Do not hard-code these numbers again in a new
script.

## Adding your own recordings

The `prepare` command above is wired to the public GRABMyo dataset
only. To run this SAME pipeline on your own sensor recordings later,
follow these steps. You will not touch `train.py`, `six_best_rest.py`,
`features.py`, or `splits.py` at all.

1. Read the "STANDARD FORM" section at the top of `load.py`. It
   defines the `Recording` object: a signal array, a label array, a
   sample rate, channel names, a subject name, and a session name.
2. Write one new loader function, in a new file (for example
   `load_my_device.py`), that reads your device's raw recording
   files and returns a list of `Recording` objects in that same
   standard form. Give each recording session a DIFFERENT `session`
   value (for example `"day1"`, `"day2"`) so the cross-session split
   can tell them apart.
3. Copy the structure of `prepare_subjects.py`, but call your new
   loader instead of the GRABMyo loader. Keep the rest unchanged:
   window with `features.window_recordings`, compute features with
   `features.compute_features`, and save one `.npz` file per subject
   with the exact same field names (`windows`, `features`,
   `feature_names`, `labels`, `subjects`, `sessions`,
   `channel_names`, `sample_rate`).
4. Point `train` and `evaluate` at your new output folder with
   `--data-dir`. No other change is needed; both commands read the
   `.npz` files by field name, not by dataset.

This is the "documented path for the user's own future recordings"
promised in the project plan: one small loader file, everything
else stays the same.

## Honest testing, always

`splits.py` is the only place this pipeline builds a train/test
split. Every split it returns is checked for "session leakage" —
the same session appearing on both the training side and the testing
side. If your own loader reuses a session name by mistake, this
check stops the run with an error instead of silently producing an
inflated accuracy number.
