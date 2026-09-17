from __future__ import annotations

import hashlib
import importlib.util
import math
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "cad" / "placement.py"
DRAWING = ROOT / "docs" / "fab" / "cad" / "v1" / "placement.svg"
INTERFACE = ROOT / "docs" / "fab" / "interface.md"
SHEET = ROOT / "docs" / "fab" / "packing-options.md"


def load_placement():
    spec = importlib.util.spec_from_file_location("elicio_placement", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules["elicio_placement"] = module
    spec.loader.exec_module(module)
    return module


P = load_placement()


class PlacementMathTests(unittest.TestCase):
    def test_sagitta_of_19_mm_board_on_path_radius(self) -> None:
        h = P.sagitta_mm()
        self.assertAlmostEqual(h, 0.4658, places=3)
        self.assertAlmostEqual(P.chord_gap_at(0.0), h, places=6)
        self.assertAlmostEqual(P.chord_gap_at(P.BOARD_LEN / 2.0), 0.0, places=6)

    def test_y_clearance_is_unchanged_by_sagitta(self) -> None:
        b = P.budget()
        self.assertAlmostEqual(b.y_clear_mm, 0.17, places=2)
        self.assertGreater(b.y_clear_mm, 0.0)

    def test_courtyards_use_maximum_bodies(self) -> None:
        # RSM 4.1 max, BAV199 Fig. 9 3.3 x 2.9
        self.assertEqual(P.VQFN_CY, (4.60, 4.60))
        self.assertEqual(P.SOT23_CY, (3.30, 2.90))

    def test_three_lines_need_two_arrays(self) -> None:
        b = P.budget()
        self.assertGreaterEqual(b.clamp_pairs, P.N_LINES)
        served = sorted(p for pads in P.ARRAY_LINES.values() for p in pads)
        self.assertEqual(served, sorted(P.LEAD_PADS))
        for pads in P.ARRAY_LINES.values():
            self.assertLessEqual(len(pads), P.PAIRS_PER_ARRAY)

    def test_q13_tab_ends_at_far_pad_edge(self) -> None:
        for pad in ("SIG1", "SIG2"):
            with self.subTest(pad=pad):
                a0, a1 = P.tab_span(pad, mode="q13")
                c = P.PAD_CONTACT[pad]
                assert c is not None
                pu, ps = P.LEAD_PADS[pad]
                d = math.hypot(pu - c[0], ps - c[1])
                self.assertAlmostEqual(a0, P.KEEPOUT_R)
                self.assertAlmostEqual(a1, d + P.PAD_SIZE / 2.0)
                self.assertLess(a1, P.LUG_A1)
        a0, a1 = P.tab_span("SIG1", mode="literal")
        self.assertAlmostEqual(a1 - a0, P.LITERAL_TAB_LEN)

    def test_real_lug_is_te_31428(self) -> None:
        self.assertAlmostEqual(P.TAB_W, 1.96, places=2)
        self.assertAlmostEqual(P.TAB_LEN, 6.27, places=2)
        self.assertAlmostEqual(P.RING_R, 2.58, places=2)
        a0, a1 = P.tab_span("SIG1")
        self.assertAlmostEqual(a0, P.RING_R, places=2)
        self.assertAlmostEqual(a1, P.LUG_A1, places=2)
        self.assertEqual(P.TAB_DEG["SIG1"], 0.0)
        self.assertEqual(P.TAB_DEG["SIG2"], 180.0)
        _c, eu, es = P._tab_axes("SIG1")
        self.assertAlmostEqual(eu, 1.0, places=6)
        self.assertAlmostEqual(es, 0.0, places=6)

    def test_upright_signal_tab_does_not_fit(self) -> None:
        self.assertLess(P.upright_signal_clear_mm(), 0.0)
        self.assertAlmostEqual(P.KEEPOUT_TOP_Y - P.SKIN_Y, 2.63, places=2)
        self.assertAlmostEqual(P.LUG_THICK + P.TAB_LEN, 6.73, places=2)

    def test_lug_tabs_are_in_the_free_mask(self) -> None:
        b = P.budget()
        self.assertAlmostEqual(b.board_mm2, 237.5, places=1)
        self.assertAlmostEqual(b.free_literal_mm2, 69.36, places=1)
        self.assertAlmostEqual(b.free_tabs_to_pad_mm2, 82.97, places=1)
        self.assertAlmostEqual(b.free_mm2, 79.32, places=1)
        self.assertGreater(b.free_without_tabs_mm2, b.free_mm2)
        self.assertNotAlmostEqual(b.free_mm2, b.free_tabs_to_pad_mm2, places=1)
        self.assertFalse(b.tqfp_fits)
        self.assertTrue(b.vqfn_fits)

    def test_rf_distance_uses_reserved_module(self) -> None:
        b = P.budget()
        self.assertTrue(b.rf_keepout2_overlap)
        self.assertAlmostEqual(b.battery_to_module_hook_nominal_mm, 5.0, places=2)
        self.assertAlmostEqual(b.battery_to_module_hook_mm, 4.70, places=2)
        self.assertAlmostEqual(b.battery_to_module_rib_mm, 4.30, places=2)
        self.assertGreater(b.battery_to_antenna_hook_mm, P.BATTERY_RF_MIN)

    def test_q14_module_body_gap_is_not_a_packing_fail(self) -> None:
        for option in P.OPTION_NAMES:
            with self.subTest(option=option):
                text = " ".join(P.layout_conflicts(option))
                self.assertNotIn("cell to reserved module", text)

    def test_placed_parts_sit_in_free_mask_clear_of_pads_and_each_other(self) -> None:
        u, s, _uu, free = P.board_free_mask()
        parts = P.placed_parts()
        names = list(parts)
        for i, name in enumerate(names):
            with self.subTest(part=name):
                self.assertTrue(P._courtyard_in_free(free, u, s, *parts[name]))
                for pad in P.LEAD_PADS:
                    self.assertFalse(P._boxes_overlap(parts[name], P.pad_box(pad)))
                for other in names[i + 1 :]:
                    self.assertFalse(P._boxes_overlap(parts[name], parts[other]))

    def test_checker_catches_round_1_array_on_ref_pad(self) -> None:
        # WP6 round 1 put one BAV199S at (4.20, 27.10); the REF pad sits on it.
        self.assertTrue(P._boxes_overlap((4.20, 27.10, *P.ARRAY_CY), P.pad_box("REF")))

    def test_reference_wire_clears_signal_keepouts(self) -> None:
        self.assertGreaterEqual(P.wire_keepout_gap(), 0.0)

    def test_pads_outside_keepouts_margin_and_antenna(self) -> None:
        for name in P.LEAD_PADS:
            with self.subTest(pad=name):
                self.assertGreaterEqual(P.pad_keepout_gap(name), 0.0)
                self.assertFalse(P.pad_in_antenna(name))

    def test_conflict_checker_runs_for_every_option(self) -> None:
        seen = {option: P.layout_conflicts(option) for option in P.OPTION_NAMES}
        self.assertEqual(list(seen), list(P.OPTION_NAMES))
        for option, conflicts in seen.items():
            with self.subTest(option=option):
                self.assertEqual(conflicts, [])

    def test_option_a_places_named_pack_on_real_lug(self) -> None:
        parts = P.placed_parts("A")
        self.assertEqual(sorted(parts), sorted(P.PART_TARGETS))
        for pad in P.LEAD_PADS:
            self.assertLessEqual(P.clamp_distance(pad, "A"), P.CLAMP_MAX_MM)
        self.assertEqual(P.layout_conflicts("A"), [])

    def test_option_c_places_named_pack_and_all_0402s(self) -> None:
        parts = P.placed_parts("C")
        self.assertEqual(sorted(parts), sorted(P.PART_TARGETS))
        for pad in P.LEAD_PADS:
            self.assertLessEqual(P.clamp_distance(pad, "C"), P.CLAMP_MAX_MM)
        self.assertEqual(len(P.place_0402s(option="C")), P.N_0402)

    def test_option_b_lengthens_arc_and_moves_m1_gate(self) -> None:
        a = P.budget("A")
        b = P.budget("B")
        self.assertAlmostEqual(b.body_arc_mm - a.body_arc_mm, P.OPTION_B_DS, places=6)
        self.assertGreater(b.total_chord_mm, a.total_chord_mm)
        self.assertGreater(b.m1_gate_mm, a.m1_gate_mm)
        c = P.budget("C")
        self.assertAlmostEqual(c.total_chord_mm, a.total_chord_mm, places=4)
        self.assertAlmostEqual(c.m1_gate_mm, a.m1_gate_mm, places=4)
        e = P.budget("E")
        self.assertAlmostEqual(e.total_chord_mm, a.total_chord_mm, places=4)

    def test_packing_decision_waits_on_the_sheet(self) -> None:
        text = INTERFACE.read_text(encoding="utf-8")
        self.assertIn("packing-options.md", text)
        self.assertTrue(SHEET.is_file())
        sheet = SHEET.read_text(encoding="utf-8")
        self.assertIn("I pick A", sheet)
        self.assertIn("not a SKU", sheet)
        self.assertIn("Packing is **not confirmed**", text)


@unittest.skipUnless(P.HAS_MATPLOTLIB, "matplotlib is not installed")
class PlacementRegenTests(unittest.TestCase):
    def test_drawing_regenerates_byte_identical(self) -> None:
        first = P.render_svg()
        second = P.render_svg()
        self.assertEqual(hashlib.sha256(first).hexdigest(), hashlib.sha256(second).hexdigest())
        self.assertEqual(first, second)
        self.assertTrue(DRAWING.is_file())
        self.assertEqual(P.sha256_file(DRAWING), P.sha256_bytes(first))

    def test_write_to_temp_matches_committed(self) -> None:
        committed = P.sha256_file(DRAWING)
        with tempfile.TemporaryDirectory() as temp_dir:
            out = Path(temp_dir) / "placement.svg"
            digest = P.write_drawing(out)
            self.assertEqual(digest, committed)
            self.assertEqual(out.read_bytes(), DRAWING.read_bytes())

    def test_four_option_drawings_regenerate_identical(self) -> None:
        for option in P.OPTION_NAMES:
            with self.subTest(option=option):
                named = P.named_drawing_path(option)
                self.assertTrue(named.is_file(), named)
                first = P.render_svg(option)
                second = P.render_svg(option)
                self.assertEqual(first, second)
                self.assertEqual(P.sha256_file(named), P.sha256_bytes(first))
        self.assertEqual(DRAWING.read_bytes(), P.named_drawing_path("A").read_bytes())
        self.assertEqual(P.render_svg("A"), DRAWING.read_bytes())


if __name__ == "__main__":
    unittest.main()
