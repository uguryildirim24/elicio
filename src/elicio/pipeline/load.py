"""Data-loading module for the muscle-signal (sEMG) gesture pipeline.

sEMG means surface electromyography. It is a muscle signal picked up by
electrodes placed on the skin, not inside the body.

STANDARD FORM
-------------
Every loader in this package, and every loader added later for the
user's own hardware, must produce a list of ``Recording`` objects. A
Recording holds:

  signal        : float32 array, shape [n_samples, n_channels].
                  One row per time sample, one column per channel.
  labels        : int32 array, shape [n_samples].
                  The gesture id active at each time sample. Rest is a
                  normal gesture id, not a missing value.
  sample_rate   : float. Samples per second (Hz).
  channel_names : list of str, length n_channels. Names travel with
                  the signal so a later step can pick a subset of
                  channels (for example, to compare an 8-channel
                  device against a 3-channel device).
  subject       : str. Which person the recording came from.
  session       : str. Which recording session or arm placement the
                  recording came from. Two recordings from the same
                  subject but a different session must use different
                  session values, so a cross-session split (see
                  ``splits.py``) can tell them apart.
  gesture_name  : str. Human-readable gesture name, for reports only.
  trial         : int. Trial number within the subject/session/gesture
                  (kept for traceability, not used by later steps).

This form is the only door into the rest of the pipeline. A future
loader for the user's own armband must return the same
``Recording`` objects; the windowing, feature, and split modules do
not know or care which sensor or dataset produced them.

DATASET USED HERE: GRABMyo
---------------------------
GRABMyo (Gesture Recognition and Biometrics ElectroMyogram) is a
public sEMG dataset hosted on PhysioNet, a free repository for
physiological signal data. It records 43 people performing 17 hand
and wrist gestures, repeated on three different days (three
"sessions"). Each recording already holds exactly one gesture held
for its full length, so within a GRABMyo recording the label does
not change over time.

GRABMyo records 32 raw electrode channels per recording:
  - F1-F16: 16 channels around the forearm (the main gesture signal).
  - W1-W12: 12 channels around the wrist.
  - U1-U4:  4 reference/unused channels (not gesture signal; dropped
            by default).

Each recording is stored as a pair of PhysioNet WFDB files (Waveform
Database format): a ``.dat`` file (the raw samples) and a ``.hea``
file (a text header with channel names, sample rate, and units). This
module reads that pair with the ``wfdb`` package.

License and access: GRABMyo is distributed under the Creative Commons
Attribution 4.0 International license (CC-BY 4.0) on PhysioNet. No
login or registration was needed to download the files used here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional

import numpy as np

try:
    import wfdb
except ModuleNotFoundError:
    wfdb = None

# The 17 GRABMyo gestures, in dataset order (gesture id 1 to 17).
# Gesture id 17, "Rest", is the explicit rest class.
GRABMYO_GESTURE_NAMES = [
    "Lateral Prehension",
    "Thumb Adduction",
    "Thumb and Little Finger Opposition",
    "Thumb and Index Finger Opposition",
    "Thumb and Index Finger Extension",
    "Thumb and Little Finger Extension",
    "Index and Middle Finger Extension",
    "Little Finger Extension",
    "Index Finger Extension",
    "Thumb Finger Extension",
    "Wrist Extension",
    "Wrist Flexion",
    "Forearm Supination",
    "Forearm Pronation",
    "Hand Open",
    "Hand Close",
    "Rest",
]
GRABMYO_REST_GESTURE_ID = 17
GRABMYO_N_GESTURES = 17
GRABMYO_N_TRIALS = 7  # trials per subject/session/gesture in the full dataset
GRABMYO_SAMPLE_RATE_HZ = 2048.0

# Channels that carry the forearm and wrist gesture signal. The "U"
# channels are reference/unused channels, not gesture signal, and are
# dropped by default.
GRABMYO_FOREARM_CHANNELS = [f"F{i}" for i in range(1, 17)]
GRABMYO_WRIST_CHANNELS = [f"W{i}" for i in range(1, 13)]
GRABMYO_KEEP_CHANNELS = GRABMYO_FOREARM_CHANNELS + GRABMYO_WRIST_CHANNELS


@dataclass
class Recording:
    """One sEMG recording in the standard form. See module docstring."""

    signal: np.ndarray  # float32 [n_samples, n_channels]
    labels: np.ndarray  # int32 [n_samples]
    sample_rate: float
    channel_names: list
    subject: str
    session: str
    gesture_name: str = ""
    trial: int = 0
    extra: dict = field(default_factory=dict)

    def __post_init__(self):
        assert self.signal.ndim == 2, "signal must be [n_samples, n_channels]"
        assert self.labels.ndim == 1, "labels must be 1-D, aligned to samples"
        assert self.signal.shape[0] == self.labels.shape[0], (
            f"signal has {self.signal.shape[0]} samples but labels has "
            f"{self.labels.shape[0]}"
        )
        assert self.signal.shape[1] == len(self.channel_names), (
            "channel_names length must match number of signal columns"
        )
        self.signal = self.signal.astype(np.float32, copy=False)
        self.labels = self.labels.astype(np.int32, copy=False)


def _read_wfdb_record(record_path: str) -> tuple:
    """Read one WFDB (.dat + .hea) pair. Returns (signal, channel_names, fs).

    ``record_path`` has no file extension; wfdb finds the .dat and .hea
    files itself.
    """
    if wfdb is None:
        raise RuntimeError(
            "loading GRABMyo recordings requires the research dependency: "
            "pip install 'elicio[research]'"
        )
    rec = wfdb.rdrecord(record_path)
    signal = np.asarray(rec.p_signal, dtype=np.float32)  # [n_samples, n_channels]
    return signal, list(rec.sig_name), float(rec.fs)


def load_grabmyo_recording(
    root_dir: str,
    session: int,
    subject: int,
    gesture_id: int,
    trial: int,
    keep_channels: Optional[Iterable[str]] = GRABMYO_KEEP_CHANNELS,
) -> Recording:
    """Load one GRABMyo recording (one subject, session, gesture, trial).

    ``root_dir`` is the folder that directly contains ``Session1``,
    ``Session2``, ``Session3``. ``keep_channels`` selects which
    electrode channels to keep, by name; pass ``None`` to keep all 32
    raw channels, including the reference channels.
    """
    stem = f"session{session}_participant{subject}_gesture{gesture_id}_trial{trial}"
    record_path = str(
        Path(root_dir) / f"Session{session}" / f"session{session}_participant{subject}" / stem
    )
    signal, channel_names, fs = _read_wfdb_record(record_path)

    if keep_channels is not None:
        keep_set = list(keep_channels)
        idx = [channel_names.index(c) for c in keep_set]
        signal = signal[:, idx]
        channel_names = keep_set

    gesture_name = GRABMYO_GESTURE_NAMES[gesture_id - 1]
    labels = np.full(signal.shape[0], gesture_id, dtype=np.int32)

    return Recording(
        signal=signal,
        labels=labels,
        sample_rate=fs,
        channel_names=channel_names,
        subject=f"participant{subject}",
        session=f"session{session}",
        gesture_name=gesture_name,
        trial=trial,
    )


def load_grabmyo_slice(
    root_dir: str,
    subjects: Iterable[int],
    sessions: Iterable[int],
    gestures: Optional[Iterable[int]] = None,
    trials: Optional[Iterable[int]] = None,
    keep_channels: Optional[Iterable[str]] = GRABMYO_KEEP_CHANNELS,
) -> list:
    """Load many GRABMyo recordings into a list of ``Recording`` objects.

    ``root_dir`` is the folder that directly contains ``Session1``,
    ``Session2``, ``Session3`` (as downloaded from PhysioNet). Missing
    files are skipped with a printed warning, so a partial local slice
    does not crash the whole load.
    """
    gestures = list(gestures) if gestures is not None else list(range(1, GRABMYO_N_GESTURES + 1))
    trials = list(trials) if trials is not None else list(range(1, GRABMYO_N_TRIALS + 1))

    recordings = []
    for session in sessions:
        for subject in subjects:
            for gesture_id in gestures:
                for trial in trials:
                    try:
                        rec = load_grabmyo_recording(
                            root_dir, session, subject, gesture_id, trial, keep_channels
                        )
                        recordings.append(rec)
                    except FileNotFoundError:
                        print(
                            f"[load] skip missing file: session{session} "
                            f"participant{subject} gesture{gesture_id} trial{trial}"
                        )
    return recordings
