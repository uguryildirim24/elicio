from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "cad" / "bte_fit_shell.py"
MANIFEST = ROOT / "docs" / "fab" / "cad" / "v1" / "manifest.json"


def load_cad():
    spec = importlib.util.spec_from_file_location("bte_fit_shell", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules["bte_fit_shell"] = module
    spec.loader.exec_module(module)
    return module


CAD = load_cad()


class CadMathTests(unittest.TestCase):
    def test_default_chord_and_radius_match_plan(self) -> None:
        path = CAD.make_path(48.4, 3.0)
        self.assertAlmostEqual(path.chord, 47.9005234, places=6)
        self.assertAlmostEqual(path.radius, 97.1025059, places=6)

    def test_origin_and_mid_arc_and_tail(self) -> None:
        path = CAD.make_path(48.4, 3.0)
        self.assertEqual(CAD.p_xyz(path, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
        mid = CAD.p_xyz(path, 0.0, 24.2, 0.0)
        self.assertAlmostEqual(mid[0], 3.0, places=6)
        tail = CAD.p_xyz(path, 0.0, 48.4, 0.0)
        self.assertAlmostEqual(tail[0], 0.0, places=6)
        self.assertAlmostEqual(tail[2], -path.chord, places=6)

    def test_chord_gate_at_bow_1_and_3(self) -> None:
        gate3 = CAD.make_path(48.4, 3.0).chord + 3.0
        gate1 = CAD.make_path(48.4, 1.0).chord + 3.0
        self.assertAlmostEqual(gate3, 50.9005234, places=6)
        self.assertAlmostEqual(gate1, 51.3448596, places=6)

    def test_wire_channel_openings_match_finding_23(self) -> None:
        expected = {
            1.0: (39.4444, 1.0891),
            3.0: (39.6437, 0.9383),
            8.0: (40.0750, 0.5373),
        }
        for bow, (s_entry, physical) in expected.items():
            with self.subTest(bow=bow):
                report = CAD.wire_channel_opening(CAD.make_path(48.4, bow).radius)
                self.assertAlmostEqual(report["s_entry"], s_entry, places=3)
                self.assertAlmostEqual(report["physical_opening"], physical, places=3)
                self.assertGreater(report["physical_opening"], 0.0)

    def test_crease_bow_clamp(self) -> None:
        self.assertEqual(CAD.clamp_crease_bow(0.2), 1.0)
        self.assertEqual(CAD.clamp_crease_bow(11.0), 8.0)
        self.assertEqual(CAD.clamp_crease_bow(3.0), 3.0)


class CadCheckTests(unittest.TestCase):
    def test_m1_below_gate_fails_with_parameter_and_number(self) -> None:
        with self.assertRaises(CAD.CheckFail) as ctx:
            CAD.cli(["--set", "M1=40", "--checks-only"])
        message = str(ctx.exception)
        self.assertIn("M1", message)
        self.assertIn("40", message)
        self.assertIn("gate", message)

    def test_variant_outside_matrix_fails_before_export(self) -> None:
        with self.assertRaises(CAD.CheckFail) as ctx:
            CAD.cli(["--set", "VARIANT=medium", "--checks-only"])
        message = str(ctx.exception)
        self.assertIn("VARIANT", message)
        self.assertIn("medium", message)

    def test_preload_outside_matrix_fails_before_export(self) -> None:
        with self.assertRaises(CAD.CheckFail) as ctx:
            CAD.cli(["--set", "HOOK_PRELOAD=3", "--checks-only"])
        message = str(ctx.exception)
        self.assertIn("HOOK_PRELOAD", message)
        self.assertIn("3", message)

    def test_reference_checks_pass(self) -> None:
        self.assertEqual(CAD.cli(["--checks-only"]), 0)


@unittest.skipUnless(CAD.HAS_BUILD123D, "build123d is not installed")
class CadRegenTests(unittest.TestCase):
    def test_reference_regen_matches_committed_hashes(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as temp_dir:
            CAD.build_and_export(Path(temp_dir))
            for name, meta in manifest["files"].items():
                with self.subTest(name=name):
                    path = Path(temp_dir) / name
                    self.assertTrue(path.is_file(), name)
                    self.assertEqual(CAD.sha256_file(path), meta["sha256"], name)

    def test_m1_below_gate_does_not_write_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(CAD.CheckFail):
                CAD.cli(
                    [
                        "--set",
                        "M1=40",
                        "--out",
                        temp_dir,
                    ]
                )
            self.assertEqual(list(Path(temp_dir).iterdir()), [])


if __name__ == "__main__":
    unittest.main()
