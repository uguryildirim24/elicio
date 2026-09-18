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
                self.assertLess(a1, P.KEEPOUT_R + P.TAB_LEN)
        a0, a1 = P.tab_span("SIG1", mode="literal")
        self.assertAlmostEqual(a1 - a0, P.LITERAL_TAB_LEN)

    def test_real_lug_is_te_31428_to_barrel_end(self) -> None:
        self.assertAlmostEqual(P.TAB_W, 1.96, places=2)
        self.assertAlmostEqual(P.TAB_LEN, 6.27, places=2)
        self.assertAlmostEqual(P.LUG_A1, 8.85, places=2)
        self.assertAlmostEqual(P.TAB_PAST_KEEPOUT, 5.30, places=2)
        a0, a1 = P.tab_span("SIG1")
        self.assertAlmostEqual(a0, P.KEEPOUT_R, places=2)
        self.assertAlmostEqual(a1, P.LUG_A1, places=2)
        self.assertAlmostEqual(P.LEAD_BEND_R, 3.0)
        self.assertAlmostEqual(P.LEAD_EXIT, 3.65)

    def test_tab_direction_search_finds_committed_layouts(self) -> None:
        # WP6b's angles aimed each barrel end at a side wall: no lead exit.
        sig1 = P.legal_tab_degrees("SIG1", movable_pads=True)
        sig2 = P.legal_tab_degrees("SIG2", movable_pads=True)
        self.assertNotIn(355.0, sig1)
        self.assertNotIn(0.0, sig1)
        self.assertNotIn(170.0, sig2)
        self.assertNotIn(180.0, sig2)
        self.assertTrue(any("lead-exit" in r for r in P.tab_reasons("SIG1", 355.0, movable_pads=True)))
        for option in ("A", "C"):
            with self.subTest(option=option):
                self.assertEqual(P.search_tab_degrees(option), P.TAB_DEG_BY_OPTION[option])
                self.assertEqual(P.SEARCH_PADS[option], P.PADS_BY_OPTION[option])
                self.assertEqual(P.SEARCH_WIRE[option], P.REF_ROUTE_BY_OPTION[option])
        self.assertLess(P.upright_signal_clear_mm(), 0.0)

    def test_checker_catches_wp6b_wall_aimed_barrels(self) -> None:
        lay = P.get_layout("A")
        saved = (dict(lay.tab_deg), lay.ref_wire, dict(lay.lead_pads))
        try:
            P.bind_layout(
                "A",
                tab_deg={"SIG1": 355.0, "SIG2": 170.0},
                ref_wire=P.REF_WIRE_HIGH_U,
                lead_pads=dict(P.LEAD_PADS),
            )
            text = " ".join(P.layout_conflicts("A"))
            self.assertIn("SIG1 lead cannot leave the barrel", text)
            self.assertIn("SIG2 lead cannot leave the barrel", text)
            self.assertIn("corner pad", text)
            self.assertIn("0402 courtyards have no site", text)
        finally:
            P.bind_layout("A", tab_deg=saved[0], ref_wire=saved[1], lead_pads=saved[2])

    def test_leads_exit_and_turn_within_the_bend_radius(self) -> None:
        for option in P.OPTION_NAMES:
            for pad in ("SIG1", "SIG2"):
                with self.subTest(option=option, pad=pad):
                    self.assertGreaterEqual(P.lead_exit_gap(pad, option)[0], 0.0)
                    self.assertGreaterEqual(P.lead_path_gap(pad, option), 0.0)
                    pads = P.get_layout(option).lead_pads
                    self.assertTrue(P.lead_run_turn_ok(pad, pads[pad], option))
            with self.subTest(option=option, wire="ref"):
                self.assertGreaterEqual(P.wire_floor_gap(option), 0.0)
                self.assertEqual(P.crossings_under_parts(option), [])

    def test_0402_sites_stay_on_the_board_in_both_orientations(self) -> None:
        for option in P.OPTION_NAMES:
            lay = P.get_layout(option)
            for x, y, w, h, _face in P.place_0402s(option=option):
                with self.subTest(option=option, site=(x, y)):
                    self.assertIn((w, h), (P.R0402_CY, P.R0402_CY[::-1]))
                    self.assertLessEqual(x + w, lay.board_u[1] - P.RIM + 1e-9)
                    self.assertLessEqual(y + h, lay.board_s[1] - P.RIM + 1e-9)

    def test_option_b_moves_the_tail_and_channel(self) -> None:
        self.assertEqual(P.channel_s("A"), P.CHANNEL_S)
        self.assertAlmostEqual(P.channel_s("B")[0], P.CHANNEL_S[0] + P.OPTION_B_DS)
        self.assertAlmostEqual(P.wrap_s("B"), P.WRAP_S + P.OPTION_B_DS)
        self.assertAlmostEqual(P.get_layout("B").ref_wire[0][1], 40.5 + P.OPTION_B_DS)

    def test_lateral_face_ignores_medial_keepouts(self) -> None:
        u, s, _uu, lateral = P.board_free_mask(option="E", punch_module=True)
        i = int((P.CONTACT_1[0] - u[0]) / P.RASTER_PITCH)
        j = int((P.CONTACT_1[1] - 1.0 - s[0]) / P.RASTER_PITCH)
        self.assertTrue(lateral[j, i])
        _u, _s, _uu, medial = P.board_free_mask(option="E")
        self.assertFalse(medial[j, i])

    def test_upright_signal_tab_does_not_fit(self) -> None:
        self.assertLess(P.upright_signal_clear_mm(), 0.0)
        self.assertAlmostEqual(P.KEEPOUT_TOP_Y - P.SKIN_Y, 2.63, places=2)
        self.assertAlmostEqual(P.LUG_THICK + P.TAB_LEN, 6.73, places=2)

    def test_lug_tabs_are_in_the_free_mask(self) -> None:
        b = P.budget()
        self.assertAlmostEqual(b.board_mm2, 237.5, places=1)
        self.assertAlmostEqual(b.free_literal_mm2, 69.36, places=1)
        self.assertAlmostEqual(b.free_tabs_to_pad_mm2, 82.97, places=1)
        self.assertAlmostEqual(b.free_mm2, 72.18, places=1)
        self.assertGreater(b.free_without_tabs_mm2, b.free_mm2)
        self.assertNotAlmostEqual(b.free_mm2, b.free_tabs_to_pad_mm2, places=1)
        self.assertFalse(b.tqfp_fits)

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
        self.assertEqual(seen["C"], [])
        for option in ("A", "B", "E"):
            with self.subTest(option=option):
                self.assertIn("ADS1292_RSM: no legal site", seen[option])

    def test_option_a_does_not_close_on_real_lug(self) -> None:
        parts = P.placed_parts("A")
        self.assertNotIn("ADS1292_RSM", parts)
        self.assertEqual(len(P.place_0402s(option="A")), 10)
        self.assertLess(P.budget("A").spare_named_mm2, 0.0)

    def test_option_c_places_named_pack_and_all_0402s(self) -> None:
        parts = P.placed_parts("C")
        self.assertEqual(sorted(parts), sorted(P.PART_TARGETS))
        for pad in P.LEAD_PADS:
            self.assertLessEqual(P.clamp_distance(pad, "C"), P.CLAMP_MAX_MM)
        self.assertEqual(len(P.place_0402s(option="C")), P.N_0402)
        self.assertEqual(P.layout_conflicts("C"), [])

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
        self.assertIn("I pick C", sheet)
        self.assertIn("**Only C closes.**", sheet)
        self.assertIn("not buildable with a crimp lug (WP5b)", sheet)
        self.assertNotIn("wait for the lug drawing", sheet)
        self.assertIn("Packing is **not confirmed**", text)


NEEDS_MATPLOTLIB = unittest.skipUnless(
    P.HAS_MATPLOTLIB, "needs the sheets or cad extra: matplotlib is not installed"
)


@NEEDS_MATPLOTLIB
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


class PlacementV2Tests(unittest.TestCase):
    """WP11 packing v2: A/B, interfaces I/II, cell, series/stacked, width and lid."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.v2 = P._v2()
        cls.rows = cls.v2.run_matrix(include_arc=False)  # ~10 s; shared by the matrix tests

    def spec(self, **kwargs):
        v2 = self.v2
        base = dict(
            arch="A",
            cell="501015",
            layout="series",
            width=20.0,
            lid_y=8.0,
            arc_plus=0.0,
            iface="II",
            standoff=3.0,
            recess=0.0,
        )
        base.update(kwargs)
        return v2.V2Spec(
            base["arch"],
            base["cell"],
            base["layout"],
            base["width"],
            base["lid_y"],
            base["arc_plus"],
            base["iface"],
            base["standoff"],
            base["recess"],
        )

    def test_cli_requires_the_v2_flags_together(self) -> None:
        with self.assertRaises(SystemExit):
            P.main(["--arch", "A"])

    def test_architecture_c_is_out(self) -> None:
        result = self.v2.run_spec(self.spec(arch="C"))
        self.assertFalse(result.closes)
        self.assertIn("architecture C is out", result.first_conflict)
        self.assertTrue(
            any("architecture C is out" in c for c in P.layout_conflicts("C", spec=self.spec(arch="C")))
        )

    def test_stacked_501015_does_not_close(self) -> None:
        result = self.v2.run_spec(self.spec(layout="stacked", lid_y=8.0))
        self.assertFalse(result.closes)
        self.assertIn("cell top 13.32 > LID_Y 8", result.first_conflict)  # on the module: 7.62 + 5.2 + 0.5

    def test_interface_i_clearances_turn09(self) -> None:
        v2 = self.v2
        # Turn 09's numbers with foam 0.3, less 0.2: review r5 packs foam 0.5
        # (the order-1 CELL_envelope's number, decision 57).
        self.assertEqual(v2.FOAM, 0.5)
        cases = (
            ("dtp", 3.0, 0.0, -0.7, -1.2),
            ("dtp", 3.5, 0.0, -0.2, -0.7),
            ("dtp", 4.0, 0.0, 0.3, -0.2),
            ("dtp", 3.5, 0.5, 0.3, -0.2),
            ("dtp", 4.0, 0.5, 0.8, 0.3),
            ("501015", 3.5, 0.0, -2.2, -2.7),
            ("501015", 4.0, 0.5, -1.2, -1.7),
        )
        for cell, st, rec, nom, defm in cases:
            with self.subTest(cell=cell, standoff=st, recess=rec):
                spec = self.spec(iface="I", cell=cell, standoff=st, recess=rec, lid_y=8.0)
                clr = v2.cell_clearance(spec)
                self.assertAlmostEqual(clr["nominal"], nom)
                self.assertAlmostEqual(clr["deformed"], defm)
                result = v2.run_spec(spec)
                self.assertFalse(result.closes)
                self.assertAlmostEqual(result.nominal_clearance, nom)
                self.assertAlmostEqual(result.deformed_clearance, defm)

    def test_module_stack_outer_heights(self) -> None:
        v2 = self.v2
        a4 = v2.module_stack(self.spec(iface="I", standoff=4.0, lid_y=8.0))
        self.assertAlmostEqual(a4["stack"], 4.0 + 1.0 + 2.3)
        self.assertAlmostEqual(a4["outer_zero"], 1.5 + 7.3 + 1.0)
        b3 = v2.module_stack(self.spec(arch="B", iface="I", standoff=3.0, lid_y=8.0))
        self.assertAlmostEqual(b3["stack"], 3.0 + 1.0 + 2.0)
        self.assertAlmostEqual(b3["outer_zero"], 8.5)
        # Interface II: ring 0.31 + standoff 3.0 + flex 0.51 + module 2.3.
        a2 = v2.module_stack(self.spec())
        self.assertAlmostEqual(a2["stack"], 0.31 + 3.0 + 0.51 + 2.3)
        self.assertAlmostEqual(a2["outer_zero"], 8.62)

    def test_interface_ii_board_rests_on_the_standoff_tops(self) -> None:
        v2 = self.v2
        r = v2.run_spec(self.spec())
        self.assertAlmostEqual(r.board_underside, 1.5 + 0.31 + 3.0)
        self.assertAlmostEqual(r.board_top, r.board_underside + 0.51)
        for name in ("standoff_SIG1", "standoff_SIG2", "standoff_REF"):
            self.assertAlmostEqual(r.parts[name].y0, 1.81)
            self.assertAlmostEqual(r.parts[name].y1, r.board_underside)
        self.assertAlmostEqual(v2.tip_below_standoff_top(self.spec()), 0.81)
        # A standoff taller than the board underside is a conflict.
        import dataclasses

        low = dataclasses.replace(r, board_underside=4.5, board_top=5.01)
        self.assertTrue(any("board underside" in c for c in v2.list_conflicts(low)))

    def test_antenna_keepout_follows_the_module_pose(self) -> None:
        r = self.v2.run_spec(self.spec())
        m = r.parts["module"]
        self.assertGreater(m.wu, m.ws)  # length along u
        au0, as0, au1, as1 = r.antenna
        self.assertAlmostEqual(au0, m.u0)
        self.assertAlmostEqual(au1 - au0, 3.8)
        self.assertAlmostEqual(as1 - as0, 12.4)
        self.assertAlmostEqual((as0 + as1) / 2.0, m.s)
        for name, box in r.parts.items():
            if box.face == "top" and name not in {"module", "usb"}:
                self.assertFalse(
                    box.u1 > au0 and box.u0 < au1 and box.s1 > as0 and box.s0 < as1, name
                )

    def test_board_parts_are_the_board_bom_packages(self) -> None:
        r = self.v2.run_spec(self.spec())
        self.assertNotIn("BAV199S_1", r.parts)
        self.assertEqual(sorted((r.parts["TLV713"].wu, r.parts["TLV713"].ws)), [2.9, 3.3])
        self.assertIn("USBLC6", r.parts)
        self.assertIn("PESD_VBUS", r.parts)

    def test_interface_i_does_not_close(self) -> None:
        thick = self.v2.run_spec(self.spec(iface="I", standoff=3.5, lid_y=8.0))
        self.assertFalse(thick.closes)
        self.assertIn("nominal cell clearance", thick.first_conflict)
        dtp = self.v2.run_spec(self.spec(iface="I", standoff=3.5, cell="dtp", lid_y=8.0))
        self.assertFalse(dtp.closes)
        self.assertIn("nominal cell clearance", dtp.first_conflict)
        self.assertAlmostEqual(dtp.adjustment_mm, 0.8)
        loaded = self.v2.run_spec(self.spec(iface="I", standoff=4.0, cell="dtp", recess=0.0, lid_y=9.0))
        self.assertFalse(loaded.closes)
        self.assertTrue(any("carry board load" in c for c in loaded.conflicts))
        recessed = self.v2.run_spec(self.spec(iface="I", standoff=4.0, cell="dtp", recess=0.5, lid_y=9.0))
        self.assertFalse(recessed.closes)
        self.assertGreater(recessed.deformed_clearance, 0.0)
        self.assertTrue(any("SIG1" in c for c in recessed.conflicts))
        # Review r5: the REF site (s 43) is past the rigid board's end, and the
        # 8 x 8 SIG1 pad at u 5.9 overhangs the board edge at u 2.25.
        for name in ("pad_SIG1", "pad_REF"):
            self.assertTrue(any(c.startswith(name + " ") and "off the rigid board" in c for c in recessed.conflicts))
        self.assertTrue(all(
            any(c.startswith("pad_REF ") for c in r.conflicts) for r in self.rows if r.spec.iface == "I"
        ))

    def test_a_501015_series_w20_y7_interface_ii_no_longer_closes(self) -> None:
        # Module top 1.5 + 0.31 + 3.0 + 0.51 + 2.3 = 7.62 > 7.0; cell 5.2 + 0.5 foam = 7.2.
        result = self.v2.run_spec(self.spec(lid_y=7.0))
        self.assertFalse(result.closes)
        self.assertTrue(any(c.startswith("module top 7.62 > LID_Y 7") for c in result.conflicts))
        self.assertTrue(any(c.startswith("cell top 7.20 > LID_Y 7") for c in result.conflicts))

    def test_a_501015_series_w20_y8_interface_ii_closes(self) -> None:
        result = self.v2.run_spec(self.spec())
        self.assertEqual(result.spec, self.v2.stage_b_winner_spec())
        self.assertEqual(result.conflicts, [])
        self.assertTrue(result.closes)
        self.assertEqual(result.n_0402, 25)
        self.assertEqual(result.usb_wall, "hook-end end face (fallback)")
        self.assertAlmostEqual(result.total_chord, 47.9005, places=3)
        self.assertLessEqual(result.total_chord, 52.0 - 3.0)
        self.assertAlmostEqual(result.parts["switch"].y0, result.board_top)
        self.assertAlmostEqual(result.parts["header"].y0, result.board_top)
        self.assertEqual(result.parts["switch"].wu, 4.5)
        self.assertEqual(result.parts["header"].ws, 7.6)

    def test_matrix_closes_only_a_interface_ii_501015_series_w20(self) -> None:
        rows = self.rows
        self.assertEqual(len(rows), 864)
        self.assertEqual(sum(1 for r in rows if r.spec.iface == "I"), 720)
        closed = [r for r in rows if r.closes]
        self.assertEqual(
            [r.spec.tag for r in closed],
            [
                "A_501015_series_w20_y8_iII_s3",
                "A_501015_series_w20_y8.5_iII_s3",
                "A_501015_series_w20_y9_iII_s3",
            ],
        )
        self.assertTrue(all(r.spec.arch == "A" and r.spec.iface == "II" for r in closed))
        self.assertFalse(any(r.spec.arch == "B" and r.closes for r in rows))
        self.assertFalse(any(r.spec.iface == "I" and r.closes for r in rows))

    def test_arc_plus_fails_the_m1_gate(self) -> None:
        result = self.v2.run_spec(self.spec(arc_plus=1.5))
        self.assertFalse(result.closes)
        self.assertTrue(any("TOTAL_CHORD" in c and "M1" in c for c in result.conflicts))

    @NEEDS_MATPLOTLIB
    def test_v2_svg_regenerates_byte_identical(self) -> None:
        spec = self.spec()
        first = self.v2.render_svg(spec)
        second = self.v2.render_svg(spec)
        self.assertEqual(first, second)
        named = self.v2.drawing_path(spec)
        self.assertTrue(named.is_file(), named)
        self.assertEqual(named.read_bytes(), first)

    @NEEDS_MATPLOTLIB
    def test_failing_svg_lists_the_conflict(self) -> None:
        spec = self.spec(arch="C")
        data = self.v2.render_svg(spec).decode("utf-8")
        self.assertIn('id="packing-v2"', data)
        self.assertIn("closes=0", data)
        self.assertIn("architecture C is out", data)

    @NEEDS_MATPLOTLIB
    def test_every_committed_v2_svg_matches_a_fresh_render(self) -> None:
        rows = self.rows
        self.assertEqual(len(rows), 864)
        by_spec = {r.spec: r for r in rows}
        kept = self.v2.kept_drawing_specs(rows)
        self.assertLessEqual(len(kept), 40)
        committed = {p.name for p in self.v2.V2_DRAW_DIR.glob("placement_v2_*.svg")}
        self.assertEqual(committed, {spec.filename for spec in kept})
        for spec in kept:
            with self.subTest(tag=spec.tag):
                path = self.v2.drawing_path(spec)
                self.assertEqual(path.read_bytes(), self.v2.render_svg(spec, by_spec[spec]))

    def test_kept_drawings_are_closers_winner_and_one_per_family(self) -> None:
        rows = self.rows
        kept = self.v2.kept_drawing_specs(rows)
        closers = [r.spec for r in rows if r.closes]
        self.assertTrue(set(closers) <= set(kept))
        self.assertIn(self.v2.stage_b_winner_spec(), kept)
        families = {self.v2.conflict_family(r.first_conflict) for r in rows if not r.closes}
        reps = self.v2.family_representatives(rows)
        self.assertEqual(set(reps), families)
        self.assertTrue({r.spec for r in reps.values()} <= set(kept))
        self.assertEqual(
            self.v2.conflict_family("module top 6.70 > LID_Y 6"), "module top # > LID_Y #"
        )

    @NEEDS_MATPLOTLIB
    def test_all_writes_closers_only_unless_all_drawings(self) -> None:
        rows = self.rows
        closers = {r.spec.filename for r in rows if r.closes}
        with tempfile.TemporaryDirectory() as temp_dir:
            out = Path(temp_dir)
            self.assertEqual(P.main(["--all", "--out-dir", str(out)]), 0)
            self.assertEqual({p.name for p in out.glob("*.svg")}, closers)
        with tempfile.TemporaryDirectory() as temp_dir:
            out = Path(temp_dir)
            self.assertEqual(P.main(["--kept-drawings", "--out-dir", str(out)]), 0)
            kept = {s.filename for s in self.v2.kept_drawing_specs(rows)}
            self.assertEqual({p.name for p in out.glob("*.svg")}, kept)
            for name in kept:
                self.assertEqual(
                    (out / name).read_bytes(), (self.v2.V2_DRAW_DIR / name).read_bytes(), name
                )

    def test_packing_doc_regenerates_byte_identical(self) -> None:
        doc = Path(__file__).resolve().parents[1] / "docs" / "fab" / "packing-v2.md"
        rows = self.rows
        self.assertEqual(doc.read_text(encoding="utf-8"), self.v2.packing_markdown(rows))

    @NEEDS_MATPLOTLIB
    def test_cli_writes_the_named_v2_drawing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            out = Path(temp_dir) / "one.svg"
            code = P.main(
                [
                    "--arch",
                    "A",
                    "--cell",
                    "501015",
                    "--layout",
                    "series",
                    "--width",
                    "20",
                    "--lid-y",
                    "7",
                    "--iface",
                    "II",
                    "--standoff",
                    "3",
                    "--out",
                    str(out),
                ]
            )
            self.assertEqual(code, 0)
            self.assertTrue(out.is_file())
            self.assertIn("elicio packing v2 A_501015_series_w20_y7_iII_s3", out.read_text(encoding="utf-8"))


class PlacementWP11bTests(unittest.TestCase):
    """WP11b: DTP arc-plus under interface II, and the REF tab route (Q55, Q59)."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.v2 = P._v2()
        cls.dtp = cls.v2.run_dtp_arc_plus()
        cls.jauch = cls.v2.run_jauch_series()

    def spec(self, **kwargs):
        base = dict(
            arch="A",
            cell="dtp",
            layout="series",
            width=20.0,
            lid_y=8.0,
            arc_plus=1.5,
            iface="II",
            standoff=3.0,
            recess=0.0,
        )
        base.update(kwargs)
        return self.v2.V2Spec(
            base["arch"],
            base["cell"],
            base["layout"],
            base["width"],
            base["lid_y"],
            base["arc_plus"],
            base["iface"],
            base["standoff"],
            base["recess"],
        )

    def test_dtp_arc_plus_matrix_is_48_runs_and_none_close(self) -> None:
        rows = self.dtp
        self.assertEqual(len(rows), 48)
        self.assertEqual(len(self.v2.dtp_arc_plus_specs()), 48)
        self.assertTrue(all(r.spec.cell == "dtp" and r.spec.iface == "II" for r in rows))
        self.assertTrue(all(r.spec.layout == "series" for r in rows))
        self.assertEqual(sorted({r.spec.arc_plus for r in rows}), [1.5, 3.0])
        self.assertEqual(sorted({r.spec.standoff for r in rows}), [3.0, 4.0])
        self.assertFalse(any(r.closes for r in rows))

    def test_dtp_w20_y8_s3_a1_5_antenna_gap_is_4_15(self) -> None:
        result = self.v2.run_spec(self.spec(arc_plus=1.5, lid_y=8.0, standoff=3.0, width=20.0))
        self.assertFalse(result.closes)
        self.assertEqual(result.first_conflict, "cell to antenna zone 4.15 < 5 mm")
        self.assertAlmostEqual(result.total_chord, 49.4157, places=3)
        self.assertGreater(result.total_chord, self.v2.M1_DEFAULT - 3.0)

    def test_dtp_arc_plus_3_0_chord_exceeds_m1_by_1_93(self) -> None:
        result = self.v2.run_spec(self.spec(arc_plus=3.0, lid_y=8.0, standoff=3.0, width=20.0))
        self.assertFalse(result.closes)
        self.assertAlmostEqual(result.total_chord, 50.9301, places=3)
        self.assertAlmostEqual(result.total_chord - (self.v2.M1_DEFAULT - 3.0), 1.9301, places=3)
        winner = self.v2.run_spec(self.v2.stage_b_winner_spec())
        self.assertAlmostEqual(result.total_chord - winner.total_chord, 3.0295, places=3)

    def test_round5_ref_tab_is_still_the_straight_floor_path(self) -> None:
        result = self.v2.run_spec(self.v2.stage_b_winner_spec())
        ref = result.tabs["REF"].points
        self.assertEqual(len(ref), 2)
        self.assertAlmostEqual(ref[0][0], 8.5)
        self.assertAlmostEqual(ref[0][1], 43.0)
        self.assertAlmostEqual(ref[1][0], 8.5)
        self.assertAlmostEqual(ref[1][1], 36.8)
        self.assertAlmostEqual(self.v2.TAB_T, 0.31)
        self.assertAlmostEqual(self.v2.FOAM, 0.5)
        self.assertAlmostEqual(self.v2.BEND_R, 1.0)
        self.assertAlmostEqual(self.v2.BOARD_BEND_R, 1.5)

    def test_ref_tab_along_floor_crosses_end_wall_at_38_2(self) -> None:
        routes = {r.name: r for r in self.v2.ref_tab_routes()}
        floor = routes["along_floor"]
        self.assertFalse(floor.in_cavity)
        self.assertTrue(floor.end_wall_crosses)
        self.assertEqual(floor.end_wall_where, "s 38.20–39.25 at u 8.50")
        self.assertAlmostEqual(floor.min_wall_distance_mm, 0.0)
        self.assertAlmostEqual(floor.min_side_wall_mm, 5.75)
        self.assertAlmostEqual(floor.length_added_mm, 0.0)
        self.assertAlmostEqual(floor.length_mm, 6.2)
        self.assertAlmostEqual(floor.y0, 1.5)
        self.assertAlmostEqual(floor.y1, 1.81)

    def test_ref_tab_lateral_and_over_pocket_also_leave_the_cavity(self) -> None:
        routes = {r.name: r for r in self.v2.ref_tab_routes()}
        lat = routes["along_lateral_wall"]
        air = routes["over_pocket_air"]
        self.assertFalse(lat.in_cavity)
        self.assertTrue(lat.end_wall_crosses)
        self.assertAlmostEqual(lat.min_side_wall_mm, 0.0)
        self.assertAlmostEqual(lat.length_added_mm, 11.5)
        self.assertTrue(lat.bend_ok)
        self.assertFalse(air.in_cavity)
        self.assertTrue(air.end_wall_crosses)
        self.assertAlmostEqual(air.y0, 7.3)
        self.assertAlmostEqual(air.y1, 7.61)
        self.assertIsNone(self.v2.best_ref_tab_route())

    def test_ref_end_wall_slot_is_2_5_by_1_05_by_0_31(self) -> None:
        slot = self.v2.ref_end_wall_slot()
        self.assertAlmostEqual(slot["u0"], 7.25)
        self.assertAlmostEqual(slot["u1"], 9.75)
        self.assertAlmostEqual(slot["s0"], 38.2)
        self.assertAlmostEqual(slot["s1"], 39.25)
        self.assertAlmostEqual(slot["y0"], 1.5)
        self.assertAlmostEqual(slot["y1"], 1.81)
        self.assertAlmostEqual(slot["width"], 2.5)
        self.assertAlmostEqual(slot["through"], 1.05)
        self.assertAlmostEqual(slot["height"], 0.31)

    def test_packing_doc_has_dtp_and_ref_tables(self) -> None:
        doc = Path(__file__).resolve().parents[1] / "docs" / "fab" / "packing-v2.md"
        text = doc.read_text(encoding="utf-8")
        self.assertIn("## 1b. DTP301120 arc-plus under interface II (WP11b)", text)
        self.assertIn("## 1c. Jauch LP501218JH under interface II (WP11b, L7 §2)", text)
        self.assertIn("### Smallest body per buyable cell (WP11b, L7 §2)", text)
        self.assertIn("### REF tab route (WP11b, Q59)", text)
        self.assertIn("`REF_end_wall_slot`", text)
        self.assertIn("cell to antenna zone 4.15 < 5 mm", text)
        self.assertIn("cell to antenna zone 4.65 < 5 mm", text)
        self.assertIn("L7-research-v4.md", text)
        self.assertIn("Rolf solders nothing", text)
        rows = getattr(PlacementV2Tests, "rows", None)
        generated = self.v2.packing_markdown(
            rows if rows is not None else self.v2.run_matrix(include_arc=False)
        )
        self.assertEqual(text, generated)

    def test_jauch_series_is_72_runs_and_none_close(self) -> None:
        rows = self.jauch
        self.assertEqual(len(rows), 72)
        self.assertEqual(len(self.v2.jauch_specs()), 72)
        self.assertTrue(all(r.spec.cell == "jauch" and r.spec.iface == "II" for r in rows))
        self.assertTrue(all(r.spec.layout == "series" for r in rows))
        self.assertEqual(sorted({r.spec.arc_plus for r in rows}), [0.0, 1.5, 3.0])
        self.assertEqual(sorted({r.spec.standoff for r in rows}), [3.0, 4.0])
        self.assertAlmostEqual(self.v2.CELL["jauch"]["t"] + self.v2.FOAM, 5.9)
        self.assertFalse(any(r.closes for r in rows))

    def test_jauch_w20_y8_5_s3_antenna_gap_is_4_65(self) -> None:
        result = self.v2.run_spec(self.spec(cell="jauch", arc_plus=0.0, lid_y=8.5, standoff=3.0, width=20.0))
        self.assertFalse(result.closes)
        self.assertEqual(result.first_conflict, "cell to antenna zone 4.65 < 5 mm")
        self.assertAlmostEqual(result.total_chord, 47.9005, places=3)
        self.assertAlmostEqual(result.parts["cell"].y1, 7.4, places=2)

    def test_jauch_cell_top_7_40_exceeds_lid_y_7(self) -> None:
        result = self.v2.run_spec(self.spec(cell="jauch", arc_plus=0.0, lid_y=7.0, standoff=3.0, width=20.0))
        self.assertFalse(result.closes)
        self.assertTrue(any(c.startswith("cell top 7.40 > LID_Y 7") for c in result.conflicts))
        self.assertAlmostEqual(result.parts["cell"].wu, 12.5)
        self.assertAlmostEqual(result.parts["cell"].ws, 20.0)

    def test_buyable_ext_108_runs_dtp_antenna_gap_is_2_65(self) -> None:
        rows = self.v2.run_buyable_ext()
        self.assertEqual(len(rows), 108)
        self.assertEqual(len(self.v2.buyable_ext_specs()), 108)
        self.assertFalse(any(r.closes for r in rows))
        self.assertFalse(any(self.v2.packs_outside_brief_box(r) for r in rows))
        result = self.v2.run_spec(
            self.spec(cell="dtp", width=20.0, lid_y=9.5, arc_plus=0.0, standoff=3.0)
        )
        self.assertEqual(result.first_conflict, "cell to antenna zone 2.65 < 5 mm")
        self.assertAlmostEqual(result.outer_at_lid, 10.5)
        dtp = [r for r in rows if r.spec.cell == "dtp"]
        self.assertTrue(
            all(any(c.startswith("cell overlaps standoff_SIG") for c in r.conflicts) for r in dtp)
        )
        doc = Path(__file__).resolve().parents[1] / "docs" / "fab" / "packing-v2.md"
        self.assertIn("## 1d. Bigger body for the two buyable cells (WP11b note 2)", doc.read_text(encoding="utf-8"))

    def test_l7_packs_winner_17mm_fails_and_501012_closes_at_w19(self) -> None:
        rows = self.v2.run_pack_cells()
        self.assertEqual(len(rows), 144)
        self.assertEqual(len(self.v2.pack_cell_specs()), 144)
        self.assertAlmostEqual(self.v2.CELL["pack501015"]["l"], 17.0)
        self.assertAlmostEqual(self.v2.CELL["pack501012"]["l"], 13.0)
        p15 = [r for r in rows if r.spec.cell == "pack501015"]
        p12 = [r for r in rows if r.spec.cell == "pack501012"]
        self.assertEqual(len(p15), 72)
        self.assertFalse(any(r.closes for r in p15))
        overlay = self.v2.winner_with_pack501015()
        self.assertFalse(overlay.closes)
        self.assertEqual(overlay.first_conflict, "BQ25100 overlaps header")
        self.assertAlmostEqual(overlay.total_chord, 47.9005, places=3)
        closed = [r for r in p12 if r.closes]
        self.assertEqual(len(closed), 8)
        best = min(
            closed,
            key=lambda r: (r.spec.width, r.spec.lid_y, r.spec.arc_plus, r.spec.standoff, r.total_chord),
        )
        self.assertEqual(best.spec.tag, "A_pack501012_series_w19_y8_iII_s3")
        self.assertAlmostEqual(best.spec.width, 19.0)
        self.assertAlmostEqual(best.total_chord, 47.9005, places=3)
        self.assertAlmostEqual(best.outer_at_lid, 9.0)
        doc = Path(__file__).resolve().parents[1] / "docs" / "fab" / "packing-v2.md"
        self.assertIn("## 1e. 501015 pack and 501012 pack under interface II (WP11b note 3, L7 §7)", doc.read_text(encoding="utf-8"))


class PlacementWP11cTests(unittest.TestCase):
    """WP11c: real F.CrtYd from 845bac7 and a courtyard-true layout search."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.v2 = P._v2()
        cls.fps = cls.v2.parse_kicad_pcb(cls.v2.load_wp12b_pcb())
        cls.lay12 = cls.v2.layout_v2_501012()
        cls.lay15 = cls.v2.layout_v2_501015_arc()

    def test_kicad_courtyards_match_wp12b_file(self) -> None:
        self.assertEqual(len(self.fps), 66)
        table = self.v2.kicad_part_table(self.fps)
        for fp in self.fps:
            with self.subTest(ref=fp.ref):
                want = self.v2.KICAD_COURTYARD[fp.footprint]
                self.assertLessEqual(abs(fp.cr_w - want[0]), 0.05)
                self.assertLessEqual(abs(fp.cr_h - want[1]), 0.05)
                row = table[fp.ref]
                self.assertLessEqual(abs(row["cr_w"] - fp.cr_w), 0.05)
                self.assertLessEqual(abs(row["cr_h"] - fp.cr_h), 0.05)
                self.assertLessEqual(abs(row["pad_w"] - fp.pad_w), 0.05)
                self.assertLessEqual(abs(row["pad_h"] - fp.pad_h), 0.05)

    def test_contact_netclass_is_1_0_mm(self) -> None:
        self.assertAlmostEqual(self.v2.contact_netclass_clearance(), 1.0)
        self.assertAlmostEqual(self.v2.CONTACT_NETCLASS_CLEARANCE, 1.0)
        zones = self.v2.parse_kicad_keepouts(self.v2.load_wp12b_pcb())
        self.assertIn("RF_NO_COPPER", zones)
        self.assertIn("RF_FEED_NOTCH", zones)
        self.assertIn("J4_USB_C_keepout", zones)

    def test_layout_v2_501012_blocks_on_jlc_assembly_edge(self) -> None:
        lay = self.lay12
        self.assertTrue(lay.first_blocking.startswith("JLC FPC assembly edge 2.5 mm"))
        self.assertEqual(lay.contacts_moved_mm, {"SIG1": 0.0, "SIG2": 0.0, "REF": 0.0})
        self.assertTrue(any(p.ref == "U1" for p in lay.parts))
        # Decision 73 hole at (14.85, 21.50) occupies the leftover SW1 site.
        self.assertFalse(any(p.ref == "SW1" for p in lay.parts))
        by_ref = {p.ref: p for p in lay.parts}
        self.assertAlmostEqual(by_ref["P1"].u, 5.9)
        self.assertAlmostEqual(by_ref["P1"].s, 22.0)
        self.assertAlmostEqual(by_ref["P2"].u, 10.4)
        self.assertAlmostEqual(by_ref["P2"].s, 33.1)
        self.assertAlmostEqual(by_ref["P3"].u, 8.5)
        self.assertAlmostEqual(by_ref["P3"].s, 43.0)

    def test_layout_v2_501015_arc_blocks_on_m1(self) -> None:
        lay = self.lay15
        self.assertTrue(lay.first_blocking.startswith("M1 ≥ TOTAL_CHORD + 3"))
        self.assertAlmostEqual(self.v2.body_geom(lay.spec)["total_chord"], 49.4157, places=3)

    def test_packing_doc_has_section_5b(self) -> None:
        doc = Path(__file__).resolve().parents[1] / "docs" / "fab" / "packing-v2.md"
        text = doc.read_text(encoding="utf-8")
        self.assertIn("## 5b. Layout for the board lane, v2 (WP11c)", text)
        self.assertIn("Variant A:", text)
        self.assertIn("Variant B:", text)
        self.assertIn("845bac7", text)
        rows = getattr(PlacementV2Tests, "rows", None)
        generated = self.v2.packing_markdown(
            rows if rows is not None else self.v2.run_matrix(include_arc=False)
        )
        self.assertEqual(text, generated)
        committed = {p.name for p in self.v2.V2_DRAW_DIR.glob("placement_v2_*.svg")}
        kept = {s.filename for s in self.v2.kept_drawing_specs(
            rows if rows is not None else self.v2.run_matrix(include_arc=False)
        )}
        self.assertEqual(committed, kept)

    def test_r6_decision_70_usb_body_nothing_closes(self) -> None:
        o = self.v2.usb_c_close_options(self.lay12.spec)
        self.assertAlmostEqual(o["wu"], 10.64, places=2)
        self.assertAlmostEqual(o["ws"], 9.42, places=2)
        self.assertAlmostEqual(o["h"], 3.2, places=1)
        self.assertAlmostEqual(o["packing_hang_mm"], 4.80, places=2)
        self.assertGreater(o["hang_mm"], 4.80)
        self.assertAlmostEqual(o["opening_u0"], 5.50, places=2)
        self.assertAlmostEqual(o["hook_u_max"], 6.39, places=2)
        self.assertAlmostEqual(o["hook_shift_mm"], 2.40, places=2)
        self.assertFalse(o["longer_closes"])
        self.assertFalse(o["hook_only_closes"])
        self.assertEqual(o["what_closes"], "nothing")
        names = [n for n, _ok, _why in self.lay12.rules]
        self.assertTrue(any("code-r6.md decision 70" in n for n in names))
        usb_rule = next(r for r in self.lay12.rules if "decision 70" in r[0])
        self.assertFalse(usb_rule[1])
        self.assertIn("What closes it: nothing", usb_rule[2])

    def test_r6_decision_72_three_ring_stiffeners(self) -> None:
        self.assertEqual(self.v2.RING_FR4_PIECES, 3)
        self.assertAlmostEqual(self.v2.TAB_T, 0.31, places=2)
        self.assertAlmostEqual(self.v2.STIFFENER_TAB, 0.2, places=2)
        rule = next(r for r in self.lay12.rules if "decision 72" in r[0])
        self.assertTrue(rule[1])
        self.assertIn("3 pieces", rule[2])
        self.assertIn("0.31", rule[2])

    def test_r6_decision_73_boss_holes(self) -> None:
        self.assertEqual(self.v2.BOSS_HOLE_SITES, ((14.85, 21.50), (14.85, 28.10)))
        self.assertAlmostEqual(self.v2.BOSS_HOLE_DIA, 2.7)
        hits = self.v2.boss_hole_hits(self.lay12.parts)
        self.assertTrue(any("28.10" in h for h in hits))
        rule = next(r for r in self.lay12.rules if "decision 73" in r[0])
        self.assertFalse(rule[1])
        names = {k[0] for k in self.lay12.keepouts}
        self.assertIn("HOLE_M1", names)
        self.assertIn("HOLE_M2", names)

    def test_r6_decision_74_fold_variants_shared_numbers(self) -> None:
        f = self.v2.tab_fold_variants(self.lay12.spec)
        self.assertAlmostEqual(f["R"], 1.5, places=1)
        self.assertAlmostEqual(f["neck"]["SIG1_strip"], 10.71, places=2)
        self.assertAlmostEqual(f["neck"]["SIG2_strip"], 21.81, places=2)
        self.assertAlmostEqual(f["side"]["SIG1_strip"], 8.36, places=2)
        self.assertAlmostEqual(f["side"]["SIG2_strip"], 12.06, places=2)
        self.assertAlmostEqual(f["side"]["pocket"][0], 0.85, places=2)
        rule = next(r for r in self.lay12.rules if "decision 74" in r[0])
        self.assertTrue(rule[1])
        self.assertIn("10.71", rule[2])
        self.assertIn("8.36", rule[2])
        self.assertIn("Same numbers for PCB, packing table and shell", rule[2])
        doc = Path(__file__).resolve().parents[1] / "docs" / "fab" / "packing-v2.md"
        text = doc.read_text(encoding="utf-8")
        self.assertIn("tasks/reviews/code-r6.md decision 70", text)
        self.assertIn("tasks/reviews/code-r6.md decision 72", text)
        self.assertIn("tasks/reviews/code-r6.md decision 73", text)
        self.assertIn("tasks/reviews/code-r6.md decision 74", text)
        self.assertIn("What closes it: nothing", text)
        self.assertIn("| 501012 BODY_ARC | neck-end | 10.71 | 21.81 |", text)
        self.assertIn("| 501012 BODY_ARC | side-wall pockets | 8.36 | 12.06 |", text)


class PlacementWP11dTests(unittest.TestCase):
    """WP11d: 32-cell layout grid, both edge readings, two sides, Q81–Q83."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.v2 = P._v2()
        cls.mod = cls.v2._layout_v2c_mod()
        cls.rows = cls.mod.run_v2c_grid(cls.v2)

    def test_grid_has_sixteen_cells(self) -> None:
        self.assertEqual(len(self.rows), 32)
        keys = {
            (r.edge, r.width, round(r.chord, 2), r.sides, r.receptacle) for r in self.rows
        }
        self.assertEqual(len(keys), 32)

    def test_process_w20_chord_4790_two_sides_does_not_place_all_66(self) -> None:
        lay = self.mod.v2c_cell(self.v2, "process", 20.0, 47.90, True, True)
        self.assertLess(lay.placed, 66)
        self.assertAlmostEqual(lay.extra_u, 0.0, places=2)
        self.assertAlmostEqual(lay.extra_s, 0.0, places=2)
        self.assertAlmostEqual(lay.under_clear_mm, 3.31, places=2)

    def test_q81_no_receptacle_cells(self) -> None:
        norec = [r for r in self.rows if not r.receptacle]
        self.assertEqual(len(norec), 16)
        for lay in norec:
            refs = {p.ref for p in lay.parts}
            self.assertNotIn("J1", refs)
            self.assertNotIn("U5", refs)
            self.assertIn("P4", refs)
            self.assertIn("P5", refs)
            self.assertEqual(lay.bom_n, 64)

    def test_q83_neck_end_is_the_default_fold(self) -> None:
        for lay in self.rows:
            self.assertEqual(lay.fold, "neck")
            self.assertLess(lay.wall_left, 1.0)

    def test_winning_layout_if_any(self) -> None:
        win = self.mod.smallest_full(self.rows, "process", receptacle=True)
        wp12 = self.mod.wp12d_layout(self.v2)
        w20 = self.mod.v2c_cell(self.v2, "process", 20.0, 47.90, True, True)
        if w20.placed < 66 or w20.first_blocking:
            self.assertIsNotNone(wp12)
            self.assertGreater(wp12.width, 20.0)
        else:
            self.assertIs(wp12, win)
        if win is None:
            return
        self.assertGreaterEqual(win.placed, win.bom_n)
        self.assertEqual(win.missing, [])
        self.assertEqual(win.first_blocking, "")
        for name, ok, why in win.rules:
            self.assertTrue(ok, f"{name}: {why}")
        by = {p.ref: p for p in win.parts}
        for ref in ("R1", "R2", "R3"):
            self.assertIn(ref, by)
            self.assertIn(by[ref].face, {"top", "bottom"})
        overlaps = []
        for face in ("top", "bottom"):
            group = [p for p in win.parts if p.face == face]
            boxes = [self.v2._part_box(p, 0.0, 1.0) for p in group]
            for i, a in enumerate(boxes):
                for b in boxes[i + 1 :]:
                    if self.v2._overlap(a, b, 0.0):
                        overlaps.append(f"{a.name}/{b.name}")
        self.assertEqual(overlaps, [])
        bu0, bu1, bs0, bs1 = win.island
        self.assertEqual(len(win.hole_sites), 2)
        if "SW1" in by:
            sw1 = by["SW1"]
            for hu, hs in win.hole_sites:
                hole = self.v2.Box(
                    "hole", hu, hs, self.v2.BOSS_HOLE_KEEP, self.v2.BOSS_HOLE_KEEP, -1.0, 20.0, "floor"
                )
                self.assertFalse(
                    self.v2._overlap(self.v2._part_box(sw1, 0.0, 1.0), hole, 0.0),
                    "SW1 overlaps a Q82 hole",
                )
        for ref in ("R1", "R2", "R3"):
            p = by[ref]
            self.assertTrue(
                self.mod._inside(p.u, p.s, p.wu, p.ws, win.island)
                or self.mod._inside(p.u, p.s, p.wu, p.ws, win.leftover),
                f"{ref} not on the island (Q79)",
            )
        for p in win.parts:
            if p.face == "hook":
                self.assertEqual(p.ref, "J1")
                continue
            if p.face == "floor":
                self.assertIn(p.ref, {"P1", "P2", "P3", "P4", "P5"})
                continue
            if p.ref in {"J2", "J3"}:
                continue
            in_island = self.mod._inside(p.u, p.s, p.wu, p.ws, win.island)
            in_left = self.mod._inside(p.u, p.s, p.wu, p.ws, win.leftover)
            in_pocket = p.s + p.ws / 2.0 <= bs0 + 0.3
            self.assertTrue(
                in_island or in_left or in_pocket,
                f"{p.ref} not inside island, leftover, or pocket",
            )
        for p in win.parts:
            if p.face != "bottom":
                continue
            for site in (self.v2.CONTACT_1, self.v2.CONTACT_2):
                ring = self.v2.Box("ring", site[0], site[1], 7.0, 7.0, -1.0, 20.0, "floor")
                self.assertFalse(
                    self.v2._overlap(self.v2._part_box(p, 0.0, 1.0), ring, 0.0),
                    f"{p.ref} over ring {site}",
                )
            for hu, hs in win.hole_sites:
                hole = self.v2.Box(
                    "hole", hu, hs, self.v2.BOSS_HOLE_KEEP, self.v2.BOSS_HOLE_KEEP, -1.0, 20.0, "floor"
                )
                self.assertFalse(
                    self.v2._overlap(self.v2._part_box(p, 0.0, 1.0), hole, 0.0),
                    f"{p.ref} over Q82 hole ({hu}, {hs})",
                )
            for name, u, s, wu, ws in (
                ("TABROOT_SIG1", self.v2.CONTACT_1[0], bs0 + 1.0, self.v2.TAB_W, 2.0),
                ("TABROOT_SIG2", self.v2.CONTACT_2[0], bs0 + 1.0, self.v2.TAB_W, 2.0),
                ("TABROOT_REF", self.v2.CONTACT_REF[0], bs1 - 2.0, self.v2.TAB_W, 4.0),
            ):
                root = self.v2.Box(name, u, s, wu, ws, -1.0, 20.0, "floor")
                self.assertFalse(
                    self.v2._overlap(self.v2._part_box(p, 0.0, 1.0), root, 0.0),
                    f"{p.ref} over {name}",
                )
        u1 = by["U1"]
        sw1 = by.get("SW1")
        for hu, hs in win.hole_sites:
            hole = self.v2.Box(
                "hole", hu, hs, self.v2.BOSS_HOLE_KEEP, self.v2.BOSS_HOLE_KEEP, -1.0, 20.0, "floor"
            )
            self.assertFalse(
                self.v2._overlap(self.v2._part_box(u1, 0.0, 1.0), hole, 0.0),
                f"Q82 hole ({hu}, {hs}) under U1",
            )
            if sw1 is not None:
                self.assertFalse(
                    self.v2._overlap(self.v2._part_box(sw1, 0.0, 1.0), hole, 0.0),
                    "SW1 overlaps a Q82 hole",
                )
        pocket = None
        for p in win.parts:
            if p.face not in {"top", "bottom"} or p.ref in self.mod.COPPER_SKIP_REFS:
                continue
            outline = self.mod._copper_outline_for(p.u, p.s, p.wu, p.ws, win.island, pocket)
            if outline is None:
                continue
            edge_mm = self.mod._pad_edge(
                self.v2, p.u, p.s, p.pad_w, p.pad_h, p.rot, outline
            )
            self.assertGreaterEqual(edge_mm, 0.30 - 1e-9, f"{p.ref} copper-to-edge {edge_mm:.3f}")
        for ref in ("D1", "C3", "C10", "C11", "C12"):
            self.assertIn(ref, by)

    def test_packing_doc_has_section_5c(self) -> None:
        doc = Path(__file__).resolve().parents[1] / "docs" / "fab" / "packing-v2.md"
        text = doc.read_text(encoding="utf-8")
        self.assertIn("## 5c. Layout grid v2c", text)
        self.assertIn("Q78", text)
        self.assertIn("Q79", text)
        self.assertIn("Q80", text)
        self.assertIn("Q81", text)
        self.assertIn("Q82", text)
        self.assertIn("Q83", text)
        self.assertIn("| process | 20 | 47.90 | two |", text)
        self.assertIn("The 16 cells with no receptacle", text)
        self.assertIn("WP12d pin table", text)
        self.assertIn("not under U1", text)
        self.assertIn("D1, C3, C10, C11 and C12", text)
        self.assertIn("| ref | side | u | s | rot |", text)
        self.assertIn("docs/fab/cad/v2c/", text)
        v1_v2 = {p.name for p in self.v2.V2_DRAW_DIR.glob("placement_v2_*.svg")}
        self.assertEqual(len(v1_v2), 14)
        v1_v2c = {p.name for p in self.v2.V2_DRAW_DIR.glob("placement_v2c_*.svg")}
        self.assertEqual(v1_v2c, set())
        v2c_dir = Path(__file__).resolve().parents[1] / "docs" / "fab" / "cad" / "v2c"
        v2c = {p.name for p in v2c_dir.glob("placement_v2c_*.svg")}
        self.assertLessEqual(len(v2c), 4)
        self.assertGreaterEqual(len(v2c), 1)


if __name__ == "__main__":
    unittest.main()
