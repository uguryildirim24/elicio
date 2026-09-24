"""Board v4 Contact-safety and fold checks on elicio-v4.kicad_pcb.

Plain text parse, no KiCad. Geometry is the design note's (docs/fab/board-v4-design.md
§4-§5); the numbers match hardware/board/build_v4.py.
"""
from __future__ import annotations

import json
import math
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOARD = ROOT / "hardware" / "board"
PCB = BOARD / "elicio-v4.kicad_pcb"
SUMMARY = BOARD / "release" / "elicio-v4" / "summary.json"

sys.path.insert(0, str(BOARD))
from v4_tables import footprints  # noqa: E402

CONTACT = {"SIG1", "SIG2", "REF"}
# Bench header nets: J3's pins, each behind its own 220 kOhm (R31-R33) on the break-off tab (§5.4).
BENCH = {"BENCH_SIG1": ("R31", "AFE_IN1P"), "BENCH_SIG2": ("R32", "AFE_IN1N"), "BENCH_REF": ("R33", "RLD_FB")}
ELECTRODE = {"R1": ("SIG1", "AFE_IN1P"), "R2": ("SIG2", "AFE_IN1N"), "R3": ("REF", "RLD_FB")}
ISLAND = (2.25, 16.0, 15.75, 37.6)
J3_CUT_U = 16.20
ZONE_HALF = 3.5  # Q84/Q88 7 x 7 zone around each flat land
LANDS = {
    "P1": ("SIG1", (5.90, 5.29)),
    "P2": ("SIG2", (10.40, -5.81)),
    "P3": ("REF", (8.50, 43.00)),
    "P4": ("VBUS", (16.514, 4.35)),
    "P5": ("GND", (16.514, 12.10)),
}
# Strip bodies off the island (u0, s0, u1, s1), their net and copper layer (§4.5).
STRIPS = {
    "SIG1": ((4.65, 2.09, 7.15, 16.0), "B.Cu"),
    "SIG2": ((9.15, -9.01, 11.65, 16.0), "F.Cu"),
    "REF": ((7.25, 37.6, 9.75, 46.2), "B.Cu"),
}
# Folded P5 standoff: PI face at u 16.19 (fold at u 15.09, inner R 1.1), 3.0 long (§4.9).
P5_STANDOFF_END_U = 15.09 + 1.1 - 3.0
J2_WELL_GAP = 0.3


def items(text: str, kind: str) -> list[str]:
    return text.split(f"\n\t({kind}\n")[1:]


def num(block: str, key: str) -> list[float]:
    m = re.search(r"\(" + key + r" ([-\d.]+) ([-\d.]+)\)", block)
    return [float(m.group(1)), float(m.group(2))]


def field(block: str, key: str) -> str:
    m = re.search(r"\(" + key + r' "([^"]*)"\)', block)
    return m.group(1) if m else ""


def inside(p: tuple[float, float], box: tuple[float, float, float, float]) -> bool:
    return box[0] <= p[0] <= box[2] and box[1] <= p[1] <= box[3]


def zone_box(site: tuple[float, float]) -> tuple[float, float, float, float]:
    return (site[0] - ZONE_HALF, site[1] - ZONE_HALF, site[0] + ZONE_HALF, site[1] + ZONE_HALF)


class BoardV4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = PCB.read_text(encoding="utf-8")
        cls.fps = {f["ref"]: f for f in footprints(cls.text)}
        cls.segments = [
            (num(b, "start"), num(b, "end"), field(b, "layer"), field(b, "net")) for b in items(cls.text, "segment")
        ]
        cls.vias = [(tuple(num(b, "at")), field(b, "net")) for b in items(cls.text, "via")]

    def contact_pads(self) -> list[tuple[str, str, float, float, str]]:
        return [
            (ref, pnum, ax, ay, net)
            for ref, fp in self.fps.items()
            for pnum, _kind, ax, ay, net in fp["pads"]
            if net in CONTACT
        ]

    def value(self, ref: str) -> str:
        chunk = self.text.split(f'(property "Reference" "{ref}"', 1)[1].split("\n\t(footprint ", 1)[0]
        return field(chunk, "property \"Value\"")

    def test_contact_nets_only_on_rings_and_resistors(self) -> None:
        refs = {ref for ref, *_ in self.contact_pads()}
        self.assertEqual(refs, {"P1", "P2", "P3", "R1", "R2", "R3"})

    def test_island_exposed_contact_copper_is_r1_r3_pads_only(self) -> None:
        # Q97(d): vias are tented; pads are the exposed copper. Nothing Contact leaves the island
        # toward the J3 tab, so the cut edge carries no Contact copper.
        on_island = {ref for ref, _p, ax, ay, _n in self.contact_pads() if inside((ax, ay), ISLAND)}
        self.assertEqual(on_island, {"R1", "R2", "R3"})
        east = [s for s in self.segments if s[3] in CONTACT and max(s[0][0], s[1][0]) > ISLAND[2]]
        self.assertEqual(east, [])
        self.assertEqual([v for v in self.vias if v[1] in CONTACT and v[0][0] > ISLAND[2]], [])

    def test_each_electrode_path_has_220k(self) -> None:
        for ref, (net, afe) in ELECTRODE.items():
            self.assertEqual(self.value(ref), "220k", ref)
            self.assertEqual({n for *_x, n in self.fps[ref]["pads"]}, {net, afe}, ref)

    def test_bench_header_sits_behind_its_own_220k(self) -> None:
        # R7: every gel-header path has its own 220 kOhm. J3's pins carry bench nets, each bridged
        # to the electrode's AFE node by R31-R33 on the tab side of the cut, never by R1-R3.
        self.assertEqual({n for *_x, n in self.fps["J3"]["pads"]}, set(BENCH))
        for net, (ref, afe) in BENCH.items():
            self.assertEqual(self.value(ref), "220k", ref)
            self.assertEqual({n for *_x, n in self.fps[ref]["pads"]}, {net, afe}, ref)
            self.assertGreaterEqual(self.fps[ref]["x"], J3_CUT_U, f"{ref} must leave with the tab")
            on_island = [s for s in self.segments if s[3] == net and min(s[0][0], s[1][0]) < J3_CUT_U]
            self.assertEqual(on_island, [], f"{net} copper west of the cut")
        afe_nets = {afe for _r, afe in BENCH.values()}
        self.assertEqual(afe_nets, {afe for _n, afe in ELECTRODE.values()})

    def test_u1_vss_pads_are_ground(self) -> None:
        nets = {num: net for num, _k, _x, _y, net in self.fps["U1"]["pads"]}
        for pad in ("14", "16", "18"):
            self.assertEqual(nets[pad], "GND", pad)

    def test_each_strip_carries_one_contact_net_on_one_layer(self) -> None:
        # Q97(a): anything with an end on a strip body is that strip's net, on that strip's layer.
        for net, (box, layer) in STRIPS.items():
            with self.subTest(strip=net):
                on_strip = [s for s in self.segments if inside(tuple(s[0]), box) or inside(tuple(s[1]), box)]
                self.assertTrue(on_strip, "strip has no copper")
                self.assertEqual({s[3] for s in on_strip}, {net})
                self.assertEqual({s[2] for s in on_strip}, {layer})
                self.assertEqual([v for v in self.vias if inside(v[0], box)], [])

    def test_no_foreign_via_or_pour_in_a_land_zone(self) -> None:
        # Q97(c).
        for ref, (net, site) in LANDS.items():
            box = zone_box(site)
            with self.subTest(land=ref):
                self.assertEqual([v for v in self.vias if inside(v[0], box) and v[1] != net], [])
                for zone in items(self.text, "zone"):
                    if "(filled_polygon" not in zone or field(zone, "net") in ("", net):
                        continue
                    pts = re.findall(r"\(xy ([-\d.]+) ([-\d.]+)\)", zone.split("(filled_polygon", 1)[1])
                    hits = [p for p in pts if inside((float(p[0]), float(p[1])), box)]
                    self.assertEqual(hits, [], f"{field(zone, 'net')} pour in {ref}'s zone")

    def test_lands_sit_at_the_documented_sites(self) -> None:
        for ref, (_net, site) in LANDS.items():
            fp = self.fps[ref]
            self.assertAlmostEqual(fp["x"], site[0], places=2, msg=ref)
            self.assertAlmostEqual(fp["y"], site[1], places=2, msg=ref)

    def test_j2_clears_the_p5_hex_well(self) -> None:
        chunk = self.text.split('(property "Reference" "J2"', 1)[1].split("\n\t(footprint ", 1)[0]
        fp = self.fps["J2"]
        th = math.radians(fp["rot"])
        us = []
        for block in re.findall(r'\(fp_(?:rect|line|poly)\s([\s\S]*?)\(layer "F\.CrtYd"\)', chunk):
            for px, py in re.findall(r"\((?:start|end|xy) ([-\d.]+) ([-\d.]+)\)", block):
                px, py = float(px), float(py)
                us.append(fp["x"] + px * math.cos(th) + py * math.sin(th))
        self.assertTrue(us, "J2 has no F courtyard")
        self.assertGreaterEqual(P5_STANDOFF_END_U - max(us), J2_WELL_GAP)

    def test_routed_claim_needs_a_passing_routed_release(self) -> None:
        if not SUMMARY.is_file():
            self.skipTest("no v4 release summary")
        summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
        if summary.get("routed"):
            self.assertTrue(summary.get("routed_requested"))
            self.assertEqual(summary.get("refused"), {})
            self.assertEqual(summary["drc_errors"], 0)
            self.assertEqual(summary["unconnected_items"], 0)
            self.assertEqual(summary["pcb_pads_without_net"], 0)
            self.assertGreater(summary["pcb_tracks"], 0)


if __name__ == "__main__":
    unittest.main()
