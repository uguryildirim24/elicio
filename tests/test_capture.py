from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from elicio.cli import main
from elicio.signal.capture import (
    TrailingEnvelope,
    collect_samples,
    load_recording,
    load_recording_meta,
    parse_sample_line,
    render_meter,
    save_recording,
    stream_samples,
)
from elicio.signal.detector import ContractionDetector
from elicio.signal.replay import (
    Recording,
    ReplaySource,
    build_synthetic_recording,
)


class ParseAndCollectTests(unittest.TestCase):
    def test_parses_numbers_and_skips_annotations(self) -> None:
        self.assertEqual(parse_sample_line("0.5\n"), 0.5)
        self.assertEqual(parse_sample_line("  -2 "), -2.0)
        self.assertIsNone(parse_sample_line("\n"))
        self.assertIsNone(parse_sample_line("# electrode adjusted"))

    def test_rejects_garbage_and_non_finite_values(self) -> None:
        for line in ("volts", "1,2", "nan", "inf"):
            with self.subTest(line=line):
                with self.assertRaises(ValueError):
                    parse_sample_line(line)

    def test_collect_applies_offset_and_gain(self) -> None:
        lines = ["2048", "# note", "2148", "", "1948"]
        samples = collect_samples(lines, offset=2048.0, gain=0.01)
        self.assertEqual(samples, [0.0, 1.0, -1.0])

    def test_collect_stops_at_max_samples(self) -> None:
        lines = [str(value) for value in range(10)]
        self.assertEqual(collect_samples(lines, max_samples=3), [0.0, 1.0, 2.0])

    def test_collect_rejects_invalid_transform(self) -> None:
        with self.assertRaises(ValueError):
            collect_samples(["1"], gain=0.0)
        with self.assertRaises(ValueError):
            collect_samples(["1"], offset=float("inf"))

    def test_stream_synthesizes_timestamps_from_rate(self) -> None:
        pairs = list(stream_samples(["1", "2", "3"], sample_rate_hz=10.0))
        self.assertEqual(pairs, [(0.0, 1.0), (0.1, 2.0), (0.2, 3.0)])


class RecordingFileTests(unittest.TestCase):
    def test_save_and_load_round_trip(self) -> None:
        recording = build_synthetic_recording()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "capture.json"
            save_recording(recording, path, meta={"site": "auricular_posterior"})
            loaded = load_recording(path)
            self.assertEqual(loaded, recording)
            self.assertEqual(
                load_recording_meta(path)["site"], "auricular_posterior"
            )

    def test_load_rejects_other_json_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "other.json"
            path.write_text(json.dumps({"samples": [1, 2]}), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_recording(path)

    def test_loaded_capture_detects_like_the_source_fixture(self) -> None:
        recording = build_synthetic_recording()
        direct = ContractionDetector(
            sample_rate_hz=recording.sample_rate_hz
        ).detect(ReplaySource(recording))
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "capture.json"
            save_recording(recording, path)
            loaded = load_recording(path)
        replayed = ContractionDetector(
            sample_rate_hz=loaded.sample_rate_hz
        ).detect(ReplaySource(loaded))
        self.assertEqual(replayed, direct)
        self.assertEqual(len(replayed), 1)


class MeterTests(unittest.TestCase):
    def test_trailing_envelope_matches_manual_mean(self) -> None:
        envelope = TrailingEnvelope(window=2)
        self.assertEqual(envelope.update(1.0), 1.0)
        self.assertEqual(envelope.update(-3.0), 2.0)
        self.assertEqual(envelope.update(5.0), 4.0)

    def test_render_meter_marks_threshold_and_clamps(self) -> None:
        line = render_meter(0.5, 0.25, width=8, peak=1.0)
        self.assertIn("[##|#----]", line)
        full = render_meter(9.0, 0.25, width=8, peak=1.0)
        self.assertTrue(full.startswith("[##|#####]"))

    def test_render_meter_rejects_invalid_arguments(self) -> None:
        with self.assertRaises(ValueError):
            render_meter(-0.1, 0.2)
        with self.assertRaises(ValueError):
            render_meter(0.1, 0.2, peak=0.0)


class DetectorSymbolTests(unittest.TestCase):
    def test_custom_symbol_is_emitted(self) -> None:
        recording = build_synthetic_recording()
        events = ContractionDetector(
            symbol="auricular_flex", sample_rate_hz=recording.sample_rate_hz
        ).detect(ReplaySource(recording))
        self.assertEqual([event.symbol for event in events], ["auricular_flex"])

    def test_invalid_symbol_is_rejected(self) -> None:
        for symbol in ("", "  ", " padded "):
            with self.subTest(symbol=symbol):
                with self.assertRaises(ValueError):
                    ContractionDetector(symbol=symbol)


class CliCaptureTests(unittest.TestCase):
    def test_capture_then_replay_recording_completes_one_action(self) -> None:
        recording = build_synthetic_recording()
        with tempfile.TemporaryDirectory() as tmp:
            stream_path = Path(tmp) / "stream.txt"
            stream_path.write_text(
                "".join(f"{sample}\n" for sample in recording.samples),
                encoding="utf-8",
            )
            capture_path = Path(tmp) / "capture.json"
            capture_code = main(
                [
                    "capture",
                    "--input",
                    str(stream_path),
                    "--sample-rate",
                    str(recording.sample_rate_hz),
                    "--out",
                    str(capture_path),
                ]
            )
            self.assertEqual(capture_code, 0)
            self.assertEqual(load_recording(capture_path), recording)

            state_dir = Path(tmp) / "state"
            replay_code = main(
                [
                    "replay-recording",
                    "--recording",
                    str(capture_path),
                    "--state-dir",
                    str(state_dir),
                ]
            )
            self.assertEqual(replay_code, 0)
            self.assertTrue(
                (state_dir / "actions" / "recording-marker.json").is_file()
            )

    def test_replay_recording_fails_closed_on_silent_capture(self) -> None:
        silent = Recording((0.0, 0.001, -0.001, 0.0), sample_rate_hz=100.0)
        with tempfile.TemporaryDirectory() as tmp:
            capture_path = Path(tmp) / "silent.json"
            save_recording(silent, capture_path)
            state_dir = Path(tmp) / "state"
            code = main(
                [
                    "replay-recording",
                    "--recording",
                    str(capture_path),
                    "--state-dir",
                    str(state_dir),
                ]
            )
            self.assertEqual(code, 1)
            self.assertFalse(
                (state_dir / "actions" / "recording-marker.json").exists()
            )


if __name__ == "__main__":
    unittest.main()
