from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from elicio.harness.adapters import AdapterRouter, LocalMarkerAdapter
from elicio.harness.audit import MemoryAuditLog
from elicio.harness.events import GestureEvent
from elicio.harness.harness import Harness
from elicio.harness.policy import DecisionStatus
from elicio.signal.detector import ContractionDetector
from elicio.signal.replay import (
    Recording,
    ReplaySource,
    build_noise_only_recording,
    build_synthetic_recording,
)


class SignalReplayAndDetectorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.recording = build_synthetic_recording()
        self.detector = ContractionDetector()

    def test_fixture_has_exactly_one_bounded_gesture_event(self) -> None:
        events = self.detector.detect(ReplaySource(self.recording))

        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertIsInstance(event, GestureEvent)
        self.assertEqual(event.symbol, "wrist_down")
        self.assertGreaterEqual(event.confidence, 0.0)
        self.assertLessEqual(event.confidence, 1.0)
        self.assertGreaterEqual(event.timestamp, 1.0)
        self.assertLess(event.timestamp, 1.7)

    def test_noise_only_recording_has_no_events(self) -> None:
        recording = build_noise_only_recording()
        events = self.detector.detect(ReplaySource(recording))

        self.assertEqual(events, [])

    def test_rest_gaps_do_not_create_extra_events(self) -> None:
        first = self.detector.detect(ReplaySource(self.recording))
        second = self.detector.detect(ReplaySource(self.recording))

        self.assertEqual(len(first), 1)
        self.assertEqual(first, second)

    def test_replay_and_detection_are_deterministic(self) -> None:
        replay_a = list(ReplaySource(self.recording))
        replay_b = list(ReplaySource(build_synthetic_recording()))
        self.assertEqual(replay_a, replay_b)

        events_a = ContractionDetector().detect(replay_a)
        events_b = ContractionDetector().detect(replay_b)
        self.assertEqual(events_a, events_b)

    def test_refractory_suppresses_a_second_close_burst(self) -> None:
        samples = (0.0,) * 30 + (0.8,) * 20 + (0.0,) * 10 + (0.8,) * 20
        recording = Recording(samples + (0.0,) * 100, sample_rate_hz=100.0)

        events = ContractionDetector().detect(ReplaySource(recording))

        self.assertEqual(len(events), 1)

    def test_replay_detector_harness_writes_one_linked_action(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            marker_path = Path(temporary_dir) / "actions" / "replay-marker.json"
            audit = MemoryAuditLog()
            harness = Harness(
                AdapterRouter({"local_marker": LocalMarkerAdapter(marker_path)}),
                audit,
            )
            recording = build_synthetic_recording()
            events = ContractionDetector(
                sample_rate_hz=recording.sample_rate_hz
            ).detect(ReplaySource(recording))
            outcomes = [harness.feed(event) for event in events]

            self.assertEqual(len(events), 1)
            self.assertEqual(len(outcomes), 1)
            self.assertEqual(outcomes[0].decision.status, DecisionStatus.APPROVED)
            self.assertIsNotNone(outcomes[0].result)
            self.assertTrue(outcomes[0].result.success)
            self.assertTrue(marker_path.is_file())
            marker = json.loads(marker_path.read_text(encoding="utf-8"))
            self.assertEqual(marker["event"], events[0].to_dict())

            self.assertEqual(
                [entry["record_type"] for entry in audit.entries],
                ["intent", "result"],
            )
            self.assertEqual(
                {entry["audit_id"] for entry in audit.entries},
                {outcomes[0].audit_id},
            )
            self.assertEqual(audit.entries[0]["result"], {"status": "pending"})
            self.assertTrue(audit.entries[1]["result"]["success"])


if __name__ == "__main__":
    unittest.main()
