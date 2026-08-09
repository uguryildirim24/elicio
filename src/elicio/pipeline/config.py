"""Single configuration file for the muscle-signal (sEMG) gesture pipeline.

This file holds every setting that the ``prepare``, ``train``, and
``evaluate`` commands share. Change a value here once; every command
picks it up. Do not hard-code these numbers again in a new script --
import them from this file instead.

WORD LIST
---------
sEMG           Surface electromyography. A muscle signal picked up by
               electrodes placed on the skin.
window         A short, fixed-length slice of signal (see WINDOW_MS
               below) that one gesture decision is made from.
step           How far forward in time the next window starts,
               relative to the current window (see STEP_MS below).
epoch          One full pass of a neural network over its training
               data during training.
session        One recording sitting (one day, one arm placement).
               See ``splits.py`` for why sessions must not mix
               between training and testing.
"""
from __future__ import annotations

# --- Windowing (used by prepare_subjects.py -> features.window_recordings) ---
# WINDOW_MS is the length of each window, in milliseconds. STEP_MS is
# how far forward each next window starts. A 200 ms window with a
# 50 ms step gives a new gesture decision every 50 ms, with 150 ms of
# overlap between neighbouring windows.
WINDOW_MS = 200.0
STEP_MS = 50.0

# --- GRABMyo public dataset settings (used by prepare_subjects.py) ---
# GRABMyo has 3 recording sessions per subject and stores its forearm
# electrode data on PhysioNet's public server, streamed record by
# record (no bulk download needed).
GRABMYO_SESSIONS = (1, 2, 3)
GRABMYO_PN_DIR_ROOT = "grabmyo/1.1.0"

# --- Training (used by train_and_eval.py and six_best_rest.py) ---
DEFAULT_EPOCHS = 20
DEFAULT_DATA_DIR = "results"
DEFAULT_TRAIN_RESULTS_CSV = "results/train_results.csv"
DEFAULT_EVALUATE_RESULTS_CSV = "results/six_best_rest.csv"

# --- Channel-count comparison (used by train_and_eval.py) ---
# For each subject, the pipeline always compares the full forearm
# channel set against a reduced 8-channel and 3-channel set, chosen
# by training-data-only ranking (see models.select_channels_by_fscore).
CHANNEL_SET_SIZES = (8, 3)
