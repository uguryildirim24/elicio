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

    def test_v2_svg_regenerates_byte_identical(self) -> None:
        spec = self.spec()
        first = self.v2.render_svg(spec)
        second = self.v2.render_svg(spec)
        self.assertEqual(first, second)
        named = self.v2.drawing_path(spec)
        self.assertTrue(named.is_file(), named)
        self.assertEqual(named.read_bytes(), first)

    def test_failing_svg_lists_the_conflict(self) -> None:
        spec = self.spec(arch="C")
        data = self.v2.render_svg(spec).decode("utf-8")
        self.assertIn('id="packing-v2"', data)
        self.assertIn("closes=0", data)
        self.assertIn("architecture C is out", data)

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


if __name__ == "__main__":
    unittest.main()
