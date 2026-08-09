from __future__ import annotations

from types import SimpleNamespace
import unittest

import numpy as np

from elicio.pipeline.splits import (
    assert_no_session_leakage,
    cross_session_split,
)


class SessionLeakageGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.window_set = SimpleNamespace(
            sessions=["session1", "session1", "session2", "session3"],
            subjects=["participant1"] * 4,
        )

    def test_cross_session_split_returns_only_disjoint_sessions(self) -> None:
        train_idx, test_idx = cross_session_split(
            self.window_set,
            train_sessions=["session1"],
            test_sessions=["session2"],
        )

        self.assertEqual(train_idx.tolist(), [0, 1])
        self.assertEqual(test_idx.tolist(), [2])

    def test_requested_session_overlap_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "overlap"):
            cross_session_split(
                self.window_set,
                train_sessions=["session1"],
                test_sessions=["session1"],
            )

    def test_manual_row_split_with_session_leakage_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "session leakage detected"):
            assert_no_session_leakage(
                self.window_set,
                np.array([0]),
                np.array([1]),
            )

    def test_manual_disjoint_row_split_passes(self) -> None:
        assert_no_session_leakage(
            self.window_set,
            np.array([0, 1]),
            np.array([2, 3]),
        )


if __name__ == "__main__":
    unittest.main()
