"""Cross-session splitter for the muscle-signal (sEMG) pipeline.

This module is the ONLY way this pipeline splits data into a training
set and a test set. It exists to make one mistake impossible: putting
windows from the same recording session into both the training set
and the test set at once (called "session leakage" or "leakage" for
short).

WHY CROSS-SESSION SPLITS
--------------------------
An sEMG sensor moves slightly every time a person puts it back on.
Skin condition, sweat, and electrode contact also change from day to
day. A gesture decoder that is trained and tested on windows from the
SAME session will look much more accurate than it really is, because
it is partly memorising that one placement, not the gesture itself.
The only honest test is: train on one session (one day, one arm
placement), test on a DIFFERENT, LATER session from the same person or
a held-out person. This module enforces that.

WHAT COUNTS AS A SESSION
--------------------------
Each ``Recording`` (see ``load.py``) carries a ``session`` field, for
example ``"session1"``. Every window inherits its source recording's
session (see ``features.py``). A split is valid only if no session
value appears on both sides of the split.
"""

from __future__ import annotations

from typing import Iterable, Optional, Tuple

import numpy as np


def cross_session_split(
    window_set,
    train_sessions: Iterable[str],
    test_sessions: Iterable[str],
    train_subjects: Optional[Iterable[str]] = None,
    test_subjects: Optional[Iterable[str]] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """Split a ``WindowSet`` into train/test row indices, by session.

    ``train_sessions`` and ``test_sessions`` are the session values to
    put on each side, for example ``train_sessions=["session1"]``,
    ``test_sessions=["session2"]``. The two session lists must not
    share any value; this is checked and raises an error if broken.

    ``train_subjects`` / ``test_subjects`` optionally also restrict by
    subject (for example, to test cross-session accuracy on the SAME
    people only). Leave as ``None`` to keep all subjects.

    Returns ``(train_idx, test_idx)``, two integer arrays of row
    indices into ``window_set.features`` / ``window_set.windows`` /
    ``window_set.labels``.
    """
    train_sessions = set(train_sessions)
    test_sessions = set(test_sessions)
    overlap = train_sessions & test_sessions
    if overlap:
        raise ValueError(
            f"train_sessions and test_sessions overlap: {sorted(overlap)}. "
            "A cross-session split must not share a session between train "
            "and test."
        )

    sessions = np.array(window_set.sessions)
    subjects = np.array(window_set.subjects)

    train_mask = np.isin(sessions, list(train_sessions))
    test_mask = np.isin(sessions, list(test_sessions))

    if train_subjects is not None:
        train_mask &= np.isin(subjects, list(train_subjects))
    if test_subjects is not None:
        test_mask &= np.isin(subjects, list(test_subjects))

    train_idx = np.nonzero(train_mask)[0]
    test_idx = np.nonzero(test_mask)[0]

    assert_no_session_leakage(window_set, train_idx, test_idx)
    return train_idx, test_idx


def assert_no_session_leakage(window_set, train_idx: np.ndarray, test_idx: np.ndarray) -> None:
    """Raise an error if any session appears in both train and test rows.

    Any code path that builds a train/test split, not only
    ``cross_session_split`` above, can call this as a final safety
    check before training a model.
    """
    sessions = np.array(window_set.sessions)
    train_sessions = set(sessions[train_idx].tolist())
    test_sessions = set(sessions[test_idx].tolist())
    leaked = train_sessions & test_sessions
    if leaked:
        raise ValueError(
            f"session leakage detected: session(s) {sorted(leaked)} appear "
            "in both the train split and the test split."
        )
