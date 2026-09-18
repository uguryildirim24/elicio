from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from elicio.cli import main
from elicio.pipeline.load import Recording
from elicio.receiver_v2 import (
    FRAME_CASES,
    LOADER_NAME,
    assert_pin_map_matches,
    case_packets,
    check_session,
    dump_fixture_packets,
    live_fake_packets,
    load_fixture_packets,
    load_receiver_session,
    receive_packets,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "receiver_v2"
BOARD_MD = ROOT / "docs" / "fab" / "board-v2.md"
PINS_H = ROOT / "firmware" / "src" / "board_pins.h"


def _run(argv: list[str]) -> tuple[int, str]:
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = main(argv)
    return code, buf.getvalue()


class ReceiverV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        FIXTURES.mkdir(parents=True, exist_ok=True)
        for name in FRAME_CASES + ("dropout", "undervoltage", "vbus"):
            dump_fixture_packets(FIXTURES / f"{name}.json", case_packets(name))
        dump_fixture_packets(FIXTURES / "simulate_live.json", live_fake_packets())

    def test_pin_header_matches_board_v2_section_9(self) -> None:
        assert_pin_map_matches(BOARD_MD.read_text(encoding="utf-8"), PINS_H.read_text(encoding="utf-8"))

    def test_pipeline_loader_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "sess"
            receive_packets(case_packets("normal"), out, "bench", "s2")
            recording = load_receiver_session(out)
            self.assertIsInstance(recording, Recording)
            self.assertEqual(recording.signal.dtype, "float32")
            self.assertEqual(recording.labels.dtype, "int32")
            self.assertEqual(recording.signal.shape, (4, 2))
            self.assertEqual(recording.channel_names, ["ADS_CH1", "ADS_CH2"])
            self.assertEqual(recording.sample_rate, 2000.0)
            codes = recording.extra["codes_int32"]
            self.assertEqual(codes.dtype, "int32")
            self.assertTrue((recording.signal == codes.astype("float32")).all())
            meta = json.loads((out / "meta.json").read_text(encoding="utf-8"))
            self.assertEqual(meta["loader"], LOADER_NAME)

    def test_every_frame_v2_case_through_the_receiver(self) -> None:
        expected = {
            "normal": {"samples": 4},
            "wrap": {"samples": 4, "wraps": 1},
            "fragment": {"samples": 3},
            "reorder": {"samples": 3},
            "loss": {"samples": 2, "losses": 1},
            "overrun": {"samples": 1, "overruns": 1},
            "partial": {"samples": 0},
            "reconnect": {"samples": 0, "reconnects": 1},
            "bad_crc": {"errors": "bad_crc"},
            "version_mismatch": {"errors": "version_mismatch"},
        }
        for name, want in expected.items():
            with self.subTest(name=name):
                packets = load_fixture_packets(FIXTURES / f"{name}.json")
                with tempfile.TemporaryDirectory() as tmp:
                    out = Path(tmp) / name
                    receive_packets(packets, out, "bench", name)
                    sidecar = json.loads((out / "sidecar.json").read_text(encoding="utf-8"))
                    recording = load_receiver_session(out)
                    if "samples" in want:
                        self.assertEqual(recording.signal.shape[0], want["samples"])
                    if "wraps" in want:
                        self.assertGreaterEqual(sidecar["wrap_count"], want["wraps"])
                    if "losses" in want:
                        self.assertGreaterEqual(sidecar["transport_loss_count"], want["losses"])
                    if "overruns" in want:
                        self.assertGreaterEqual(sidecar["overrun_count"], want["overruns"])
                    if "reconnects" in want:
                        self.assertGreaterEqual(sidecar["reconnect_count"], want["reconnects"])
                    if "errors" in want:
                        self.assertIn(want["errors"], sidecar["decode_errors"])

    def test_undervoltage_and_vbus_are_events(self) -> None:
        for name, kind in (("undervoltage", "undervoltage"), ("vbus", "vbus")):
            with self.subTest(name=name):
                with tempfile.TemporaryDirectory() as tmp:
                    out = Path(tmp) / name
                    receive_packets(case_packets(name), out, "bench", name)
                    sidecar = json.loads((out / "sidecar.json").read_text(encoding="utf-8"))
                    kinds = [event["kind"] for event in sidecar["events"]]
                    self.assertIn(kind, kinds)

    def test_simulate_live_injects_faults(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "live"
            receive_packets(live_fake_packets(), out, "bench", "live")
            sidecar = json.loads((out / "sidecar.json").read_text(encoding="utf-8"))
            self.assertGreaterEqual(sidecar["transport_loss_count"], 1)
            self.assertGreaterEqual(sidecar["reconnect_count"], 1)
            self.assertGreaterEqual(sidecar["overrun_count"], 1)
            self.assertGreater(load_receiver_session(out).signal.shape[0], 0)
            self.assertTrue(sidecar["batteries"])

    def test_cli_simulate_and_check_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "cli"
            code, text = _run(
                ["receive", "--simulate", str(FIXTURES / "normal.json"), "--out", str(out)]
            )
            self.assertEqual(code, 0)
            self.assertIn("simulate", text)
            code, text = _run(["receive-check", str(out)])
            self.assertEqual(code, 0)
            summary = json.loads(text)
            self.assertEqual(summary["sample_count"], 4)
            self.assertTrue(summary["ok"])

    def test_cli_simulate_live(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "live"
            code, _text = _run(["receive", "--simulate-live", "--out", str(out)])
            self.assertEqual(code, 0)
            code, text = _run(["receive-check", str(out)])
            self.assertEqual(code, 0)
            summary = json.loads(text)
            self.assertGreater(summary["sample_count"], 0)
            self.assertGreaterEqual(summary["losses"], 1)

    def test_receive_check_fails_on_dropout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "drop"
            receive_packets(case_packets("dropout"), out, "bench", "drop")
            summary = check_session(out)
            self.assertGreater(summary["dropout_stretches"], 0)
            self.assertFalse(summary["ok"])
            code, _text = _run(["receive-check", str(out)])
            self.assertEqual(code, 1)

    def test_receive_check_fails_scored_same_criterion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "same"
            receive_packets(case_packets("normal"), out, "bench", "same")
            sidecar_path = out / "sidecar.json"
            sidecar = json.loads(sidecar_path.read_text(encoding="utf-8"))
            sidecar["same_criterion"]["3.7"] = "fail"
            sidecar_path.write_text(json.dumps(sidecar) + "\n", encoding="utf-8")
            self.assertEqual(_run(["receive-check", str(out)])[0], 1)

    def test_bleak_is_optional_for_the_fake_path(self) -> None:
        import elicio.receiver_v2 as mod

        self.assertTrue(hasattr(mod, "PacketSource"))
        self.assertNotIn("bleak", dir(mod))


if __name__ == "__main__":
    unittest.main()
