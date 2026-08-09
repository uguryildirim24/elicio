from __future__ import annotations

from types import SimpleNamespace
import unittest

import numpy as np

from elicio.pipeline.features import window_recording


class PipelineRestTests(unittest.TestCase):
    def test_rest_is_kept_as_a_real_window_label(self) -> None:
        recording = SimpleNamespace(
            signal=np.zeros((10, 2), dtype=np.float32),
            labels=np.full(10, 17, dtype=np.int32),
            sample_rate=10.0,
            channel_names=["F1", "F2"],
            subject="participant1",
            session="session1",
        )

        windows = window_recording(recording, window_ms=200.0, step_ms=100.0)

        self.assertGreater(windows.windows.shape[0], 0)
        self.assertEqual(set(windows.labels.tolist()), {17})
        self.assertEqual(set(windows.sessions), {"session1"})


if __name__ == "__main__":
    unittest.main()
