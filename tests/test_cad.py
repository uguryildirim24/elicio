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

    def test_plan_named_checks_are_present(self) -> None:
        params, _used = CAD.build_reference_params(variant="full", preload=1.5)
        names = {check.name for check in CAD.run_pre_cad_checks(params)}
        for expected in (
            "matrix",
            "M1_gate",
            "HOOK_RADIUS",
            "CONTACT_STACK",
            "keep-out: CONTACT_1 to superior low-u pad",
            "fit: tongue 0.5 : slot 0.9, y",
            "wall: top end wall at LIP_GROOVE",
            "E1",
            "E5_bump",
            "WIRE_CHANNEL_opening",
        ):
            self.assertIn(expected, names)

    def test_pad_keepout_gap_is_positive_at_supported_bows(self) -> None:
        for bow in (1.0, 3.0, 8.0):
            with self.subTest(bow=bow):
                params, _used = CAD.build_reference_params(
                    variant="full", preload=1.5, overrides={"CREASE_BOW": bow}
                )
                path = CAD.make_path(48.4, bow)
                gaps = CAD.keepout_clearances(params, path)
                self.assertGreater(gaps["CONTACT_1 to superior low-u pad"], 0.09)

    def test_fit_drift_fails(self) -> None:
        params, _used = CAD.build_reference_params(variant="full", preload=1.5)
        original = CAD.LIP_S
        CAD.LIP_S = (-1.2, -0.1)
        try:
            with self.assertRaises(CAD.CheckFail) as ctx:
                CAD.run_pre_cad_checks(params)
        finally:
            CAD.LIP_S = original
        self.assertIn("E5_lip", str(ctx.exception))


class CadOverlayTests(unittest.TestCase):
    def _params(self, argv: list[str]) -> dict:
        args = CAD.parse_args(argv)
        overrides, from_m = CAD.resolve_overrides(args)
        params, _used = CAD.build_reference_params(
            variant="full", preload=1.5, overrides=overrides, crease_bow_from_m=from_m
        )
        return params

    def _overlay(self, text: str) -> Path:
        handle = tempfile.NamedTemporaryFile("w", suffix=".toml", delete=False)
        handle.write(text)
        handle.close()
        self.addCleanup(Path(handle.name).unlink)
        return Path(handle.name)

    def test_default_toml_as_params_is_not_an_overlay(self) -> None:
        args = CAD.parse_args(["--params", str(CAD.DEFAULT_PARAMS_PATH)])
        overrides, from_m = CAD.resolve_overrides(args)
        self.assertEqual(overrides, {})
        self.assertFalse(from_m)

    def test_empty_overlay_keeps_default_bow(self) -> None:
        params = self._params(["--params", str(self._overlay("# nothing measured\n"))])
        self.assertEqual(params["CREASE_BOW"], 3.0)

    def test_overlay_with_m1_only_keeps_default_bow(self) -> None:
        params = self._params(["--params", str(self._overlay("M1 = 53.0\n"))])
        self.assertEqual(params["CREASE_BOW"], 3.0)

    def test_overlay_with_m1_and_m2_computes_and_clamps_bow(self) -> None:
        params = self._params(["--params", str(self._overlay("M1 = 52.0\nM2 = 58.0\n"))])
        self.assertAlmostEqual(params["CREASE_BOW_COMPUTED"], 11.0014, places=3)
        self.assertEqual(params["CREASE_BOW"], 8.0)

    def test_overlay_crease_bow_wins_over_m1_m2(self) -> None:
        text = "M1 = 52.0\nM2 = 58.0\nCREASE_BOW = 2.0\n"
        params = self._params(["--params", str(self._overlay(text))])
        self.assertEqual(params["CREASE_BOW"], 2.0)

    def test_m8_drives_hook_radius(self) -> None:
        params = self._params(["--set", "M8=13"])
        self.assertAlmostEqual(params["HOOK_RADIUS"], 13.0 + 1.75 + 0.75)
        self.assertEqual(CAD.cli(["--set", "M8=13", "--checks-only"]), 0)

    def test_unknown_key_fails(self) -> None:
        with self.assertRaises(CAD.CheckFail) as ctx:
            CAD.cli(["--set", "M9=12", "--checks-only"])
        self.assertIn("M9", str(ctx.exception))

    def test_fixed_geometry_key_fails(self) -> None:
        with self.assertRaises(CAD.CheckFail) as ctx:
            CAD.cli(["--set", "BODY_WIDTH=15", "--checks-only"])
        self.assertIn("BODY_WIDTH=15", str(ctx.exception))

    def test_stage_b_contacts_fail_before_export(self) -> None:
        with self.assertRaises(CAD.CheckFail) as ctx:
            CAD.cli(["--set", "MOCK_CONTACTS=false", "--checks-only"])
        self.assertIn("MOCK_CONTACTS", str(ctx.exception))


@unittest.skipUnless(CAD.HAS_BUILD123D, "build123d is not installed")
class CadRegenTests(unittest.TestCase):
    def test_reference_regen_matches_committed_hashes(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        expected = {
            f"{part}.{ext}" for part in CAD.ORDER_PARTS for ext in ("step", "stl", "3mf")
        }
        self.assertEqual(set(manifest["files"]), expected)
        self.assertEqual(manifest["parts"], list(CAD.ORDER_PARTS))
        self.assertEqual(sum(manifest["quantities"].values()), 6)
        committed = {p.name for p in MANIFEST.parent.iterdir()}
        extra = {"placement.svg", "placement.png"}
        self.assertEqual(committed - extra, expected | {"manifest.json"})
        for name, meta in manifest["files"].items():
            with self.subTest(committed=name):
                self.assertEqual(
                    CAD.sha256_file(MANIFEST.parent / name), meta["sha256"], name
                )
        with tempfile.TemporaryDirectory() as temp_dir:
            CAD.build_and_export(Path(temp_dir))
            written = {p.name for p in Path(temp_dir).iterdir()}
            self.assertEqual(written, expected | {"manifest.json"})
            regenerated = json.loads((Path(temp_dir) / "manifest.json").read_text("utf-8"))
            for name in sorted(expected):
                with self.subTest(regenerated=name):
                    path = Path(temp_dir) / name
                    self.assertEqual(CAD.sha256_file(path), manifest["files"][name]["sha256"])
                    self.assertEqual(
                        regenerated["files"][name]["sha256"], manifest["files"][name]["sha256"]
                    )
            self.assertTrue(all(check["passed"] for check in regenerated["checks"]))

    def test_clamp_limits_build_one_solid(self) -> None:
        for bow in (1.0, 8.0):
            with self.subTest(bow=bow), tempfile.TemporaryDirectory() as temp_dir:
                result = CAD.build_and_export(
                    Path(temp_dir), overrides={"CREASE_BOW": bow}, parts=("body_full_p15",)
                )
                self.assertEqual(len(result["files"]), 3)

    def test_subset_build_refuses_to_leave_stale_parts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            (Path(temp_dir) / "manifest.json").write_text(
                json.dumps({"files": {"body_thin_p15.stl": {}}}), encoding="utf-8"
            )
            with self.assertRaises(CAD.CheckFail) as ctx:
                CAD.build_and_export(Path(temp_dir), parts=("coupon",))
            self.assertIn("body_thin_p15", str(ctx.exception))

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
