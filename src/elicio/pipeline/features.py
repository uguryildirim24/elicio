"""Windowing and feature module for the muscle-signal (sEMG) pipeline.

This module takes ``Recording`` objects from ``load.py`` (see that
module for the standard data form) and produces short, overlapping
time windows, plus a standard set of time-domain features per window
and per channel.

WHY WINDOWS
-----------
A gesture decoder does not look at one signal sample at a time. It
looks at a short slice of time (a "window") and decides which gesture
was most likely happening during that slice. A 200 ms window with a
50 ms step means: look at a 200-millisecond slice of signal, decide,
then move forward 50 milliseconds and repeat. The windows overlap
(150 ms of each window repeats in the next one), so the decoder gets a
new answer every 50 ms instead of every 200 ms.

WINDOWS NEVER CROSS A GESTURE CHANGE
-------------------------------------
Windows are cut "aligned to gesture onsets". This means: whenever the
label changes (one gesture ends and the next, including rest, begins)
the windowing process starts a fresh window at that point. No window
is allowed to span two different labels. This keeps every window's
label unambiguous.

REST IS A REAL CLASS
---------------------
Rest (the arm relaxed, no gesture) is an explicit label like any
other gesture, not a gap or a missing value. A window entirely inside
a rest segment is labelled "rest" and is used for training and
testing exactly like any other gesture window.

STANDARD TIME-DOMAIN FEATURES
------------------------------
For each window and each channel, five standard sEMG features are
computed. All five are well established in the muscle-signal
literature for gesture decoding:

  MAV  Mean Absolute Value. The average size of the signal, ignoring
       sign. Rises when the muscle contracts harder.
  WL   Waveform Length. The total up-and-down distance the signal
       traces during the window. Higher for busier, noisier signal.
  ZC   Zero Crossings. How many times the signal crosses zero during
       the window. Higher for higher-frequency signal.
  SSC  Slope Sign Changes. How many times the signal's slope changes
       direction (from rising to falling or back). A measure of how
       often the signal changes direction.
  RMS  Root Mean Square. The square root of the average squared
       signal value. Another standard measure of signal size.

A small dead-zone threshold is used for ZC and SSC so that flat, quiet
signal (during rest) does not produce spurious crossings from
measurement noise alone.

RAW-WINDOW EXPORT
------------------
Besides the five features above, this module can also return the raw
window arrays unchanged (samples x channels, per window). A future
neural-network model can train directly on the raw windows instead of
the five hand-built features.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional

import numpy as np

from .config import STEP_MS, WINDOW_MS

# Zero-amplitude threshold used for the zero-crossing and slope-sign-change
# features, in the same signal units as the loaded recordings (millivolts
# for GRABMyo). Differences smaller than this threshold are treated as
# noise, not as a real crossing or slope change.
ZC_SSC_THRESHOLD = 1e-3


@dataclass
class WindowSet:
    """A batch of windows cut from one or more recordings.

    windows        : float32 array [n_windows, window_samples, n_channels].
                     Raw signal per window; use for a neural-network path.
    features       : float32 array [n_windows, n_channels * n_features] or
                     None if features were not requested.
    feature_names  : list of str, length n_channels * n_features, matching
                     the columns of ``features``. None if features were
                     not requested.
    labels         : int32 array [n_windows]. Gesture id per window.
    subjects       : list of str, length n_windows.
    sessions       : list of str, length n_windows.
    channel_names  : list of str, length n_channels.
    sample_rate    : float, samples per second.
    """

    windows: np.ndarray
    features: Optional[np.ndarray]
    feature_names: Optional[list]
    labels: np.ndarray
    subjects: list
    sessions: list
    channel_names: list
    sample_rate: float

    def __post_init__(self):
        n = self.windows.shape[0]
        assert self.labels.shape[0] == n
        assert len(self.subjects) == n
        assert len(self.sessions) == n
        if self.features is not None:
            assert self.features.shape[0] == n


def _contiguous_label_segments(labels: np.ndarray):
    """Yield (start, end) sample-index pairs, end exclusive, for each
    run of samples that share one label. This is how a window is kept
    from spanning a gesture onset: each segment is windowed on its own.
    """
    n = len(labels)
    if n == 0:
        return
    start = 0
    for i in range(1, n):
        if labels[i] != labels[start]:
            yield start, i
            start = i
    yield start, n


def window_recording(
    recording,
    window_ms: float = WINDOW_MS,
    step_ms: float = STEP_MS,
) -> WindowSet:
    """Cut one ``Recording`` into overlapping windows, aligned to onsets.

    Returns a ``WindowSet`` with ``features=None`` (call
    ``compute_features`` to add features). Segments shorter than one
    window are dropped, since a partial window at the sample rate given
    could not carry the full feature-window length.
    """
    fs = recording.sample_rate
    window_samples = int(round(window_ms / 1000.0 * fs))
    step_samples = int(round(step_ms / 1000.0 * fs))
    assert window_samples > 0 and step_samples > 0

    windows = []
    labels = []
    for seg_start, seg_end in _contiguous_label_segments(recording.labels):
        seg_len = seg_end - seg_start
        if seg_len < window_samples:
            continue
        label = recording.labels[seg_start]
        last_start = seg_len - window_samples
        for w_start in range(0, last_start + 1, step_samples):
            a = seg_start + w_start
            b = a + window_samples
            windows.append(recording.signal[a:b, :])
            labels.append(label)

    if len(windows) == 0:
        n_channels = recording.signal.shape[1]
        windows_arr = np.zeros((0, window_samples, n_channels), dtype=np.float32)
        labels_arr = np.zeros((0,), dtype=np.int32)
    else:
        windows_arr = np.stack(windows).astype(np.float32)
        labels_arr = np.array(labels, dtype=np.int32)

    n = windows_arr.shape[0]
    return WindowSet(
        windows=windows_arr,
        features=None,
        feature_names=None,
        labels=labels_arr,
        subjects=[recording.subject] * n,
        sessions=[recording.session] * n,
        channel_names=list(recording.channel_names),
        sample_rate=fs,
    )


def window_recordings(
    recordings: Iterable,
    window_ms: float = WINDOW_MS,
    step_ms: float = STEP_MS,
) -> WindowSet:
    """Cut many ``Recording`` objects and concatenate the resulting windows.

    All recordings must share the same channel names and sample rate;
    this is asserted so a mismatched recording fails loudly instead of
    silently mixing incompatible channels.
    """
    parts = [window_recording(r, window_ms, step_ms) for r in recordings]
    parts = [p for p in parts if p.windows.shape[0] > 0]
    if not parts:
        raise ValueError("no windows produced from the given recordings")

    channel_names = parts[0].channel_names
    sample_rate = parts[0].sample_rate
    for p in parts:
        assert p.channel_names == channel_names, "channel name mismatch across recordings"
        assert p.sample_rate == sample_rate, "sample rate mismatch across recordings"

    windows = np.concatenate([p.windows for p in parts], axis=0)
    labels = np.concatenate([p.labels for p in parts], axis=0)
    subjects = sum((p.subjects for p in parts), [])
    sessions = sum((p.sessions for p in parts), [])

    return WindowSet(
        windows=windows,
        features=None,
        feature_names=None,
        labels=labels,
        subjects=subjects,
        sessions=sessions,
        channel_names=channel_names,
        sample_rate=sample_rate,
    )


def _mean_absolute_value(x: np.ndarray) -> np.ndarray:
    # x: [n_windows, window_samples, n_channels] -> [n_windows, n_channels]
    return np.mean(np.abs(x), axis=1)


def _waveform_length(x: np.ndarray) -> np.ndarray:
    return np.sum(np.abs(np.diff(x, axis=1)), axis=1)


def _root_mean_square(x: np.ndarray) -> np.ndarray:
    return np.sqrt(np.mean(x ** 2, axis=1))


def _zero_crossings(x: np.ndarray, threshold: float = ZC_SSC_THRESHOLD) -> np.ndarray:
    a = x[:, :-1, :]
    b = x[:, 1:, :]
    sign_change = (a * b) < 0
    big_enough = (np.abs(a) > threshold) | (np.abs(b) > threshold)
    return np.sum(sign_change & big_enough, axis=1)


def _slope_sign_changes(x: np.ndarray, threshold: float = ZC_SSC_THRESHOLD) -> np.ndarray:
    d = np.diff(x, axis=1)  # [n_windows, window_samples-1, n_channels]
    d1 = d[:, :-1, :]
    d2 = d[:, 1:, :]
    sign_change = (d1 * d2) < 0
    big_enough = (np.abs(d1) > threshold) | (np.abs(d2) > threshold)
    return np.sum(sign_change & big_enough, axis=1)


# Name -> function, in the fixed column order used by compute_features.
TIME_DOMAIN_FEATURES = {
    "MAV": _mean_absolute_value,
    "WL": _waveform_length,
    "ZC": _zero_crossings,
    "SSC": _slope_sign_changes,
    "RMS": _root_mean_square,
}


def compute_features(window_set: WindowSet) -> WindowSet:
    """Add the five standard time-domain features to a ``WindowSet``.

    Returns a new ``WindowSet`` with ``features`` filled in, shape
    [n_windows, n_channels * 5], and ``feature_names`` listing each
    column as ``"<channel>_<feature>"``, e.g. ``"F1_MAV"``. The
    ``windows`` array (raw signal) is kept unchanged, so a later step
    can still use raw windows for a neural-network path.
    """
    x = window_set.windows  # [n_windows, window_samples, n_channels]
    per_feature = []
    names = []
    for feat_name, fn in TIME_DOMAIN_FEATURES.items():
        values = fn(x)  # [n_windows, n_channels]
        per_feature.append(values)
        names.extend(f"{ch}_{feat_name}" for ch in window_set.channel_names)

    # Stack as [n_windows, n_features, n_channels] then flatten to
    # [n_windows, n_features * n_channels] in (feature, channel) order,
    # matching the order `names` was built in above.
    stacked = np.stack(per_feature, axis=1)  # [n_windows, n_features, n_channels]
    n_windows = stacked.shape[0]
    features = stacked.reshape(n_windows, -1).astype(np.float32)

    return WindowSet(
        windows=window_set.windows,
        features=features,
        feature_names=names,
        labels=window_set.labels,
        subjects=window_set.subjects,
        sessions=window_set.sessions,
        channel_names=window_set.channel_names,
        sample_rate=window_set.sample_rate,
    )
