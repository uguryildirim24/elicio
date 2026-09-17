from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "cad" / "bte_fit_shell.py"
MANIFEST_SCRIPT = ROOT / "scripts" / "cad" / "manifest.py"
RENDER_SCRIPT = ROOT / "scripts" / "cad" / "render.py"
MANIFEST = ROOT / "docs" / "fab" / "cad" / "v1" / "manifest.json"
ARTWORK = ("render_medial.png", "render_lateral.png", "drawing.pdf")


def load_cad():
    spec = importlib.util.spec_from_file_location("bte_fit_shell", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules["bte_fit_shell"] = module
    spec.loader.exec_module(module)
    return module


CAD = load_cad()

try:
    import matplotlib  # noqa: F401
    import trimesh  # noqa: F401

    HAS_RENDER = True
except ImportError:
    HAS_RENDER = False


def load_manifest_mod():
    spec = importlib.util.spec_from_file_location("cad_manifest", MANIFEST_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_render_mod():
    spec = importlib.util.spec_from_file_location("cad_render", RENDER_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


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

    def test_stage_b_mock_false_checks_run(self) -> None:
        self.assertEqual(CAD.cli(["--set", "MOCK_CONTACTS=false", "--checks-only"]), 0)
        params, _used = CAD.build_reference_params(
            variant="full", preload=1.5, overrides={"MOCK_CONTACTS": False}
        )
        names = {check.name: check for check in CAD.run_pre_cad_checks(params)}
        self.assertIn("Q21_REF_lug", names)
        self.assertFalse(names["Q21_REF_lug"].passed)
        self.assertGreater(names["Q21_REF_lug"].numbers["lug_top_y"], names["Q21_REF_lug"].numbers["lid_y"])
        self.assertNotIn("E1", names)
        self.assertNotIn("E5_bump", names)
        self.assertIn("BOARD_underside_clear", names)
        self.assertIn("CELL_envelope", names)
        self.assertIn("REF_WIRE_envelope", names)
        self.assertIn("CABLE_EXIT_cavity", names)
        self.assertIn("TAB_envelope_air", names)
        self.assertIn("M1_gate", names)


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
        # placement*.svg are WP6 drawings, regenerated by tests/test_placement.py.
        placement = {
            "placement.svg",
            "placement_A.svg",
            "placement_B.svg",
            "placement_C.svg",
            "placement_E.svg",
        }
        self.assertEqual(committed, expected | {"manifest.json"} | placement | set(ARTWORK))
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
            self.assertEqual(regenerated["commit"], manifest["commit"])
            self.assertNotIn("views", regenerated)
            # Everything else the writer records must match the committed file,
            # so a generator change (a new note, a changed check) cannot leave
            # a stale manifest behind.
            committed_rest = {
                k: v for k, v in manifest.items() if not k.startswith("views")
            }
            self.assertEqual(regenerated, committed_rest)


class ManifestSchemaTests(unittest.TestCase):
    def test_committed_manifest_validates(self) -> None:
        mod = load_manifest_mod()
        payload = mod.load_manifest(MANIFEST)
        mod.validate(payload)
        mod.validate_bytes(payload, MANIFEST.parent)

    def test_validator_rejects_missing_key(self) -> None:
        mod = load_manifest_mod()
        payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
        del payload["files"]
        with self.assertRaises(mod.ManifestError) as ctx:
            mod.validate(payload)
        self.assertIn("files", str(ctx.exception))
        self.assertIn("missing key", str(ctx.exception))


@unittest.skipUnless(HAS_RENDER, "matplotlib/trimesh is not installed")
class CadRenderTests(unittest.TestCase):
    def test_renders_and_drawing_regen_byte_identical(self) -> None:
        render = load_render_mod()
        v1 = MANIFEST.parent
        with tempfile.TemporaryDirectory() as temp_dir:
            dest = Path(temp_dir)
            for name in ("body_full_p15.stl", "body_thin_p15.stl", "lid.stl", "manifest.json"):
                shutil.copy2(v1 / name, dest / name)
            self.assertEqual(render.main(["--out", str(dest)]), 0)
            for name in ARTWORK:
                with self.subTest(name=name):
                    self.assertEqual(
                        CAD.sha256_file(dest / name),
                        CAD.sha256_file(v1 / name),
                        name,
                    )
            again = Path(tempfile.mkdtemp())
            self.addCleanup(shutil.rmtree, again, True)
            for name in ("body_full_p15.stl", "body_thin_p15.stl", "lid.stl", "manifest.json"):
                shutil.copy2(v1 / name, again / name)
            self.assertEqual(render.main(["--out", str(again)]), 0)
            committed_views = json.loads(MANIFEST.read_text(encoding="utf-8"))["views"]
            rendered_views = json.loads((again / "manifest.json").read_text("utf-8"))["views"]
            self.assertEqual(rendered_views, committed_views)
            for name in ARTWORK:
                with self.subTest(second=name):
                    self.assertEqual(
                        CAD.sha256_file(dest / name),
                        CAD.sha256_file(again / name),
                        name,
                    )


@unittest.skipUnless(CAD.HAS_BUILD123D, "build123d is not installed")
class CadBuildGuardTests(unittest.TestCase):
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


class CadStageBTests(unittest.TestCase):
    STAGE_B = ROOT / "scripts" / "cad" / "params" / "stageb_provisional.toml"

    def _stage_b(self, overrides: dict | None = None) -> dict:
        merged = {"MOCK_CONTACTS": False}
        if overrides:
            merged.update(overrides)
        params, _used = CAD.build_reference_params(
            variant="full", preload=1.5, overrides=merged
        )
        return params

    def test_packing_a_is_plan_shell(self) -> None:
        params = self._stage_b({"PACKING": "A"})
        self.assertEqual(params["PACKING"], "A")
        self.assertAlmostEqual(params["BODY_WIDTH"], 17.0)
        self.assertAlmostEqual(params["BODY_ARC"], 48.4)

    def test_packing_c_widens_body_and_uses_placement_pads(self) -> None:
        params = self._stage_b({"PACKING": "C"})
        self.assertEqual(params["PACKING"], "C")
        self.assertAlmostEqual(params["BODY_WIDTH"], 20.0)
        self.assertEqual(params["LEAD_PADS"]["SIG1"], [7.5, 29.35])
        self.assertEqual(params["LEAD_PADS"]["SIG2"], [13.5, 21.35])
        self.assertEqual(params["LEAD_PADS"]["REF"], [5.5, 29.35])
        placement = CAD.load_placement()
        self.assertEqual(
            params["LEAD_PADS"]["SIG1"],
            list(placement.PADS_BY_OPTION["C"]["SIG1"]),
        )

    def test_packing_b_lengthens_arc_and_moves_tail(self) -> None:
        params = self._stage_b({"PACKING": "B"})
        self.assertAlmostEqual(params["BODY_ARC"], 51.9)
        self.assertAlmostEqual(params["TAIL_DS"], 3.5)
        self.assertAlmostEqual(params["TAIL_S0"], 41.7)

    def test_q21_records_failure_with_numbers(self) -> None:
        params = self._stage_b()
        q21 = {c.name: c for c in CAD.run_pre_cad_checks(params)}["Q21_REF_lug"]
        self.assertFalse(q21.passed)
        self.assertIn("Q21", q21.detail)
        self.assertGreater(q21.numbers["lug_top_y"], q21.numbers["lid_y"])
        self.assertGreater(q21.numbers["barrel_outer"], q21.numbers["pocket_r"])

    def test_keepout_on_rib_fails_with_gap(self) -> None:
        with self.assertRaises(CAD.CheckFail) as ctx:
            CAD.cli(
                [
                    "--set",
                    "MOCK_CONTACTS=false",
                    "--set",
                    "CONTACT_1_S=17.9",
                    "--checks-only",
                ]
            )
        message = str(ctx.exception)
        self.assertIn("keep-out", message)
        self.assertIn("gap", message)

    def test_tab_height_3_fails_board_clearance(self) -> None:
        with self.assertRaises(CAD.CheckFail) as ctx:
            CAD.cli(
                [
                    "--set",
                    "MOCK_CONTACTS=false",
                    "--set",
                    "TAB_HEIGHT=3",
                    "--checks-only",
                ]
            )
        message = str(ctx.exception)
        self.assertIn("BOARD_underside_clear", message)
        self.assertIn("4.5", message)

    def test_cable_exit_in_battery_fails(self) -> None:
        with self.assertRaises(CAD.CheckFail) as ctx:
            CAD.cli(
                [
                    "--set",
                    "MOCK_CONTACTS=false",
                    "--set",
                    "CABLE_EXIT_S=10",
                    "--checks-only",
                ]
            )
        message = str(ctx.exception)
        self.assertIn("CABLE_EXIT_cavity", message)
        self.assertIn("10", message)

    def test_cell_too_wide_fails(self) -> None:
        params = self._stage_b()
        original = CAD.BATTERY_U
        CAD.BATTERY_U = (3.1, 8.0)
        try:
            with self.assertRaises(CAD.CheckFail) as ctx:
                CAD.run_pre_cad_checks(params)
        finally:
            CAD.BATTERY_U = original
        self.assertIn("CELL_envelope", str(ctx.exception))

    def test_closure_passed_restores_e1_e3_e5(self) -> None:
        params = self._stage_b({"CLOSURE_PASSED": True})
        names = {c.name for c in CAD.run_pre_cad_checks(params)}
        self.assertIn("E1", names)
        self.assertIn("E3", names)
        self.assertIn("E5_bump", names)

    def test_provisional_file_defaults(self) -> None:
        args = CAD.parse_args(["--params", str(self.STAGE_B)])
        overrides, _from_m = CAD.resolve_overrides(args)
        self.assertFalse(overrides["MOCK_CONTACTS"])
        self.assertEqual(overrides["PACKING"], "C")
        self.assertFalse(overrides["CLOSURE_PASSED"])
        self.assertEqual(overrides["TAB_HEIGHT"], 2.0)

    def test_stage_b_refuses_v1_out(self) -> None:
        params = self._stage_b()
        with self.assertRaises(CAD.CheckFail) as ctx:
            CAD.assert_stage_b_out_dir(CAD.V1_DIR, params)
        self.assertIn("v1", str(ctx.exception).lower())
        with self.assertRaises(CAD.CheckFail):
            CAD.assert_stage_b_out_dir(CAD.V2_DIR, params)


@unittest.skipUnless(CAD.HAS_BUILD123D, "build123d is not installed")
class CadStageBBuildTests(unittest.TestCase):
    STAGE_B = ROOT / "scripts" / "cad" / "params" / "stageb_provisional.toml"

    def test_hole_in_side_wall_fails_wall_only_check(self) -> None:
        params, _used = CAD.build_reference_params(
            variant="full",
            preload=1.5,
            overrides={"MOCK_CONTACTS": False, "CONTACT_1_U": 0.5},
        )
        body, lid, path, _notes = CAD.build_body_and_lid(params)
        with self.assertRaises(CAD.CheckFail) as ctx:
            CAD.run_stage_b_solid_checks(body, lid, path, params)
        self.assertIn("CONTACT_HOLE_wall", str(ctx.exception))
        self.assertIn("0.5", str(ctx.exception))

    def test_provisional_build_into_temp_records_q21(self) -> None:
        cmd = [
            sys.executable,
            str(SCRIPT),
            "--params",
            str(self.STAGE_B),
            "--parts",
            "body_full_p15,lid,coupon",
        ]
        with tempfile.TemporaryDirectory() as temp_dir:
            dest = Path(temp_dir)
            self.assertEqual(subprocess.check_call(cmd + ["--out", str(dest)]), 0)
            payload = json.loads((dest / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(payload["stage"], "B")
            self.assertTrue(payload["provisional"])
            self.assertEqual(payload["packing"], "C")
            self.assertFalse(payload["closure_passed"])
            self.assertIn("plan §3.3", payload["contact_source"])
            q21 = payload["stage_b"]["Q21_REF_lug"]
            self.assertFalse(q21["passed"])
            self.assertGreater(q21["numbers"]["lug_top_y"], q21["numbers"]["lid_y"])
            for name in (
                "BOARD_underside_clear",
                "CELL_envelope",
                "REF_WIRE_envelope",
                "CABLE_EXIT_cavity",
                "TAB_envelope_air",
                "CONTACT_HOLE_wall",
                "KEEPOUT_SIGNAL_air",
                "KEEPOUT_REF_air",
            ):
                with self.subTest(name=name):
                    self.assertIn(name, payload["stage_b"])
                    if name != "Q21_REF_lug":
                        self.assertTrue(payload["stage_b"][name]["passed"], name)
            mod = load_manifest_mod()
            mod.validate(payload)
        with tempfile.TemporaryDirectory() as temp_dir2:
            dest2 = Path(temp_dir2)
            self.assertEqual(subprocess.check_call(cmd + ["--out", str(dest2)]), 0)
            again = json.loads((dest2 / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(again["files"], payload["files"])


if __name__ == "__main__":
    unittest.main()
