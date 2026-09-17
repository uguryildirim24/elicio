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

    def test_free_area_and_named_pack_fit(self) -> None:
        b = P.budget()
        self.assertAlmostEqual(b.board_mm2, 237.5, places=1)
        self.assertGreater(b.free_mm2, 100.0)
        self.assertLess(b.free_mm2, 110.0)
        self.assertFalse(b.tqfp_fits)
        self.assertTrue(b.vqfn_fits)
        self.assertLess(b.required_named_mm2, b.free_mm2)
        self.assertGreater(b.required_as_drawn_mm2, b.free_mm2)

    def test_rf_zone_overlaps_keepout_2_and_meets_5_mm_with_cell_at_hook(self) -> None:
        b = P.budget()
        self.assertTrue(b.rf_keepout2_overlap)
        self.assertAlmostEqual(b.battery_to_module_hook_mm, 5.0, places=2)
        self.assertLess(b.battery_to_module_rib_mm, 5.0)

    def test_lead_pads_outside_keepouts_margin_and_antenna(self) -> None:
        for name in P.LEAD_PADS:
            with self.subTest(pad=name):
                self.assertGreaterEqual(P.pad_keepout_gap(name), 0.0)
                self.assertFalse(P.pad_in_antenna(name))
                self.assertLessEqual(P.clamp_distance(name), P.CLAMP_MAX_MM)

    def test_placed_ics_sit_in_free_mask(self) -> None:
        u, s, _uu, free = P.board_free_mask()
        for name, box in P.PLACED.items():
            with self.subTest(part=name):
                self.assertTrue(P._courtyard_in_free(free, u, s, *box), name)

    def test_twenty_five_0402_courtyards(self) -> None:
        sites = P.place_0402s()
        self.assertEqual(len(sites), 25)


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
