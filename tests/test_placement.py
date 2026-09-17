from __future__ import annotations

import hashlib
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "cad" / "placement.py"
DRAWING = ROOT / "docs" / "fab" / "cad" / "v1" / "placement.svg"
INTERFACE = ROOT / "docs" / "fab" / "interface.md"


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

    def test_lug_tabs_are_in_the_free_mask(self) -> None:
        b = P.budget()
        self.assertAlmostEqual(b.board_mm2, 237.5, places=1)
        self.assertLess(b.free_mm2, b.free_tabs_to_pad_mm2)
        self.assertLess(b.free_tabs_to_pad_mm2, b.free_without_tabs_mm2)
        self.assertFalse(b.tqfp_fits)
        self.assertTrue(b.vqfn_fits)

    def test_rf_distance_uses_reserved_module(self) -> None:
        b = P.budget()
        self.assertTrue(b.rf_keepout2_overlap)
        self.assertAlmostEqual(b.battery_to_module_hook_nominal_mm, 5.0, places=2)
        self.assertAlmostEqual(b.battery_to_module_hook_mm, 4.70, places=2)
        self.assertAlmostEqual(b.battery_to_module_rib_mm, 4.30, places=2)
        self.assertGreater(b.battery_to_antenna_hook_mm, P.BATTERY_RF_MIN)

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

    def test_conflicts_make_packing_not_confirmed_in_interface(self) -> None:
        conflicts = P.layout_conflicts()
        text = INTERFACE.read_text(encoding="utf-8")
        if conflicts:
            self.assertIn("Packing is **not confirmed**", text)
            for c in conflicts:
                self.assertIn(c, text)
        else:
            self.assertNotIn("Packing is **not confirmed**", text)


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


if __name__ == "__main__":
    unittest.main()
