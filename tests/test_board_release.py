from __future__ import annotations

import csv
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "scripts" / "board" / "release.py"
SCH = ROOT / "hardware" / "board" / "elicio-v2.kicad_sch"
PCB = ROOT / "hardware" / "board" / "elicio-v2.kicad_pcb"

PACKING = ROOT / "hardware" / "board" / "packing_v2_flat.md"


def packing_section5_centres() -> dict[str, tuple[float, float]]:
    """Named SMT centres from the vendored pin table v3 (flat coordinates)."""
    sys.path.insert(0, str(ROOT / "hardware" / "board"))
    from placement_table import parse_pin_table_v2

    rows = parse_pin_table_v2(PACKING.read_text(encoding="utf-8"))
    return {row.ref: (row.u, row.s) for row in rows}


def kicad_missing_message() -> str:
    return "kicad-cli is absent; install with: brew install --cask kicad"


class BoardReleaseTests(unittest.TestCase):
    def test_kicad_cli_is_installed(self) -> None:
        if shutil.which("kicad-cli") is None:
            self.fail(kicad_missing_message())

    def test_release_job_erc_zero_and_outputs(self) -> None:
        if shutil.which("kicad-cli") is None:
            self.fail(kicad_missing_message())
        self.assertTrue(RELEASE.is_file())
        self.assertTrue(SCH.is_file())
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "release"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(RELEASE),
                    "--board-dir",
                    str(SCH.parent),
                    "--out",
                    str(out),
                ],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
            )
            self.assertEqual(
                proc.returncode,
                0,
                msg=proc.stderr + "\n" + proc.stdout[-4000:],
            )
            summary_path = out / "summary.json"
            self.assertTrue(summary_path.is_file())
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            self.assertEqual(summary["erc_errors"], 0)
            self.assertTrue((out / "bom.csv").is_file())
            self.assertTrue((out / "cpl.csv").is_file())
            self.assertTrue((out / "elicio-v2.step").is_file())
            self.assertTrue(any((out / "gerbers").iterdir()))
            # Q94 PI 0.1 piece lives on User.1; a missing layer loses the drawing at order.
            self.assertTrue((out / "gerbers" / "elicio-v2-User_1.gbr").is_file())
            with (out / "bom.csv").open(newline="") as fh:
                rows = [r for r in csv.DictReader(fh) if any(r.values())]
            self.assertEqual(len(rows), summary["bom_rows"])
            self.assertEqual(summary["bom_rows"], summary["placed_parts"])
            self.assertGreater(len(rows), 0)
            designators = [r.get("Designator") or r.get("Reference") for r in rows]
            self.assertEqual(len(set(designators)), len(designators))
            # Review r6: the CPL places exactly the BOM's parts (J3 is THT;
            # Q5, R29, R30 are DNP on the schematic).
            with (out / "cpl.csv").open(newline="") as fh:
                cpl = {r["Designator"] for r in csv.DictReader(fh)}
            self.assertEqual(cpl, set(designators))
            self.assertIn("J3", cpl)
            self.assertFalse({"Q5", "R29", "R30", "R9", "R10"} & cpl)
            self.assertEqual(summary["bom_refs_without_cpl"], [])
            # Review r5: ERC is clean (no lib_symbol_mismatch), DRC is counted
            # and the summary says the board is not routed.
            self.assertEqual(summary["erc_warnings"], 0)
            self.assertIs(summary["routed"], False)
            self.assertIs(summary["routed_requested"], False)
            self.assertEqual(summary["refused"], {})
            for key in ("drc_errors", "drc_warnings", "unconnected_items", "pcb_tracks", "pcb_pads_without_net"):
                self.assertIsInstance(summary[key], int, key)
            self.assertGreater((out / "elicio-v2.step").stat().st_size, 0)

    def test_routed_release_fails_closed_on_this_board(self) -> None:
        if shutil.which("kicad-cli") is None:
            self.fail(kicad_missing_message())
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "release"
            proc = subprocess.run(
                [sys.executable, str(RELEASE), "--board-dir", str(SCH.parent), "--out", str(out), "--routed"],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 1, proc.stdout[-2000:])
            self.assertIn("routed release refused", proc.stderr)
            summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
            # Review r6: a refused release never reports routed: true.
            self.assertIs(summary["routed"], False)
            self.assertIs(summary["routed_requested"], True)
            self.assertTrue(summary["refused"])
            self.assertGreater(summary["refused"].get("unconnected_items", 0), 0)
            # WP12g: Contact and SES copper are present; 63 nets are not finished.
            self.assertGreater(summary["pcb_tracks"], 0)


class PackingAgreementTests(unittest.TestCase):
    def test_named_smt_centres_match_packing_v2_within_0_1_mm(self) -> None:
        text = PCB.read_text(encoding="utf-8")
        found: dict[str, tuple[float, float]] = {}
        for chunk in text.split("(footprint ")[1:]:
            at = re.search(r"\(at ([+-]?\d+(?:\.\d+)?) ([+-]?\d+(?:\.\d+)?)", chunk)
            ref = re.search(r'\(property "Reference" "([^"]+)"', chunk)
            if at and ref:
                found[ref.group(1)] = (float(at.group(1)), float(at.group(2)))
        packing = packing_section5_centres()
        self.assertIn("U1", packing)
        self.assertNotIn("J1", packing)
        self.assertNotIn("U5", packing)
        self.assertIn("P4", packing)
        self.assertIn("P5", packing)
        self.assertAlmostEqual(packing["P4"][0], 23.32, places=2)
        self.assertAlmostEqual(packing["P4"][1], 4.35, places=2)
        self.assertAlmostEqual(packing["P5"][0], 23.32, places=2)
        self.assertAlmostEqual(packing["P5"][1], 12.35, places=2)
        for ref, (px, py) in packing.items():
            if ref.startswith("H") or ref in {"R9", "R10"}:
                continue
            self.assertIn(ref, found, ref)
            x, y = found[ref]
            dist = ((x - px) ** 2 + (y - py) ** 2) ** 0.5
            self.assertLessEqual(
                dist, 0.1, f"{ref} pcb=({x},{y}) packing=({px},{py}) d={dist}"
            )
        self.assertIn("H1", found)
        self.assertIn("H2", found)
        self.assertLessEqual(
            ((found["H1"][0] - 13.23) ** 2 + (found["H1"][1] - 17.70) ** 2) ** 0.5, 0.1
        )
        self.assertLessEqual(
            ((found["H2"][0] - 17.95) ** 2 + (found["H2"][1] - 17.70) ** 2) ** 0.5, 0.1
        )


    def test_pcb_matches_packing_5e_pin_table_v3(self) -> None:
        """Board and vendored pin table v3 carry one set of numbers, side and rotation."""
        text = PCB.read_text(encoding="utf-8")
        found: dict[str, tuple[float, float, float, str]] = {}
        for chunk in text.split("\n\t(footprint ")[1:]:
            at = re.search(r"\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)", chunk)
            ref = re.search(r'\(property "Reference" "([^"]+)"', chunk)
            layer = re.search(r'\(layer "([^"]+)"\)', chunk)
            if at and ref and layer:
                found[ref.group(1)] = (
                    float(at.group(1)), float(at.group(2)), float(at.group(3) or 0.0), layer.group(1)
                )
        packing = PACKING.read_text(encoding="utf-8")
        section = packing[packing.index("### Pin table v3"):]
        section = section[: section.index("\n### ", 5)]
        rows = 0
        for line in section.splitlines():
            m = re.match(
                r"^\|\s*([A-Z][A-Z0-9]*)\s*\|\s*(\w+)\s*\|\s*([-0-9.]+)\s*\|\s*([-0-9.]+)\s*\|\s*([-0-9.]+)\s*\|",
                line,
            )
            if m is None:
                continue
            rows += 1
            ref, side = m.group(1), m.group(2)
            u, s, rot = float(m.group(3)), float(m.group(4)), float(m.group(5))
            with self.subTest(ref=ref):
                self.assertNotIn(ref, {"R9", "R10"})
                self.assertIn(ref, found)
                x, y, prot, layer = found[ref]
                self.assertLessEqual(((x - u) ** 2 + (y - s) ** 2) ** 0.5, 0.1, (ref, x, y, u, s))
                if side == "bottom":
                    self.assertEqual(layer, "B.Cu", ref)
                else:
                    self.assertEqual(layer, "F.Cu", ref)
                want = (180.0 - rot) % 360.0 if side == "bottom" else rot % 360.0
                self.assertAlmostEqual(prot % 360.0, want, places=1, msg=ref)
        self.assertEqual(rows, 66)


class Wp12cRoutedAssertionTests(unittest.TestCase):
    def test_order_release_stays_unrouted(self) -> None:
        """WP12h: Contact and SES copper exist; DRC 0 with 0 unconnected was not reached."""
        if shutil.which("kicad-cli") is None:
            self.fail(kicad_missing_message())
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "release"
            proc = subprocess.run(
                [sys.executable, str(RELEASE), "--board-dir", str(SCH.parent), "--out", str(out), "--routed"],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 1, proc.stdout[-2000:])
            self.assertIn("routed release refused", proc.stderr)
            summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
            self.assertGreater(summary["pcb_tracks"], 0)
            self.assertGreater(summary["unconnected_items"], 0)
            self.assertEqual(summary["pcb_pads_without_net"], 0)


class FlexDsnClassTests(unittest.TestCase):
    def test_check_dsn_classes_accepts_section_12_blocks(self) -> None:
        sys.path.insert(0, str(ROOT / "scripts" / "board"))
        import route_v2

        text = """
    (class kicad_default GND
      (rule
        (width 100)
        (clearance 100)
      )
    )
    (class Contact REF SIG1 SIG2
      (rule
        (width 150)
        (clearance 200)
      )
    )
    (via "Via[0-1]_550:300_um")
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "elicio-v2.dsn"
            path.write_text(text, encoding="utf-8")
            self.assertEqual(route_v2.check_dsn_classes(path), [])


class SideColumnTests(unittest.TestCase):
    def test_synthetic_two_row_table_marks_bottom_for_flip(self) -> None:
        # Two-row packing table: one top, one bottom. Does not load the PCB.
        import sys

        sys.path.insert(0, str(ROOT / "hardware" / "board"))
        from placement_table import parse_placement_markdown, wants_back_copper

        table = """
| ref | u | s | rot | side |
|---|---:|---:|---:|---|
| U1 | 10.00 | 32.35 | 90 | top |
| C6 | 3.70 | 20.20 | 0 | bottom |
"""
        rows = parse_placement_markdown(table)
        self.assertEqual([r.ref for r in rows], ["U1", "C6"])
        self.assertEqual(rows[0].side, "top")
        self.assertEqual(rows[1].side, "bottom")
        self.assertAlmostEqual(rows[0].u, 10.00)
        self.assertAlmostEqual(rows[0].s, 32.35)
        self.assertAlmostEqual(rows[0].rot, 90)
        self.assertFalse(wants_back_copper(rows[0]))
        self.assertTrue(wants_back_copper(rows[1]))

    def test_section5b_face_column_maps_top_and_bottom_only(self) -> None:
        import sys

        sys.path.insert(0, str(ROOT / "hardware" / "board"))
        from placement_table import parse_placement_markdown, wants_back_copper

        table = """
| ref | u | s | rot | courtyard wu × ws | face | notes |
|---|---:|---:|---:|---|---|---|
| U1 | 10.00 | 32.35 | 90 | 16.50 × 11.50 | top | packing centre |
| C6 | 3.70 | 20.20 | 0 | 2.96 × 1.46 | bottom | B.Cu under ADS |
| C7 | 13.58 | 3.88 | 0 | 2.96 × 1.46 | pocket | region, not a copper side |
"""
        rows = parse_placement_markdown(table)
        self.assertEqual([r.side for r in rows], ["top", "bottom", "top"])
        self.assertEqual([wants_back_copper(r) for r in rows], [False, True, False])


class Q84ContactAreaTests(unittest.TestCase):
    def test_dru_file_names_tabs_and_tail_pads(self) -> None:
        dru = (ROOT / "hardware" / "board" / "elicio-v2.kicad_dru").read_text(encoding="utf-8")
        self.assertIn("(version 1)", dru)
        self.assertIn("intersectsArea('tabs')", dru)
        self.assertIn("intersectsArea('tail_pads')", dru)
        self.assertIn("1.0mm", dru)
        self.assertIn("Q88", dru)

    def test_contact_netclass_is_island_default_0_20(self) -> None:
        pro = json.loads((ROOT / "hardware" / "board" / "elicio-v2.kicad_pro").read_text(encoding="utf-8"))
        contact = next(c for c in pro["net_settings"]["classes"] if c["name"] == "Contact")
        self.assertAlmostEqual(contact["clearance"], 0.2)

    def test_drc_has_no_contact_clearance_on_island_0402(self) -> None:
        """Q84/Q88: R1–R3 on the island use 0.20 mm, not tab creepage 1.0 mm."""
        if shutil.which("kicad-cli") is None:
            self.fail(kicad_missing_message())
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "drc.json"
            proc = subprocess.run(
                ["kicad-cli", "pcb", "drc", "--format", "json", "-o", str(report), str(PCB)],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            data = json.loads(report.read_text(encoding="utf-8"))
            island_refs = (" of R1 ", " of R2 ", " of R3 ")
            hits = []
            for viol in data.get("violations") or []:
                if viol.get("type") != "clearance":
                    continue
                desc = viol.get("description") or ""
                if "Contact" not in desc:
                    continue
                blob = " " + " ".join(item.get("description") or "" for item in viol.get("items") or []) + " "
                if any(ref in blob for ref in island_refs):
                    hits.append((desc, blob.strip()))
            self.assertEqual(hits, [], msg=hits)

    def test_drc_has_no_one_mm_creepage_at_strip_roots(self) -> None:
        """Q88: L1, D2, U1 at the attach line are not under 1.0 mm tab creepage."""
        if shutil.which("kicad-cli") is None:
            self.fail(kicad_missing_message())
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "drc.json"
            proc = subprocess.run(
                ["kicad-cli", "pcb", "drc", "--format", "json", "-o", str(report), str(PCB)],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            data = json.loads(report.read_text(encoding="utf-8"))
            roots = (" of L1 ", " of D2 ", " of U1 ")
            hits = []
            for viol in data.get("violations") or []:
                if viol.get("type") != "clearance":
                    continue
                desc = viol.get("description") or ""
                if "1.0000 mm" not in desc and "1.0 mm" not in desc:
                    continue
                blob = " " + " ".join(item.get("description") or "" for item in viol.get("items") or []) + " "
                if any(ref in blob for ref in roots):
                    hits.append((desc, blob.strip()))
            self.assertEqual(hits, [], msg=hits)

    def test_strip_keepout_names_are_on_the_board(self) -> None:
        text = PCB.read_text(encoding="utf-8")
        for name in ("strip_sig1", "strip_sig2", "strip_ref"):
            self.assertIn(name, text)

    def test_foreign_copper_in_a_strip_fails_drc(self) -> None:
        """A GND track beside the SIG1 strip centre must fail Contact clearance."""
        if shutil.which("kicad-cli") is None:
            self.fail(kicad_missing_message())
        kicad_py = Path(
            "/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3"
        )
        if not kicad_py.is_file():
            self.fail("KiCad python3 is absent")
        with tempfile.TemporaryDirectory() as tmp:
            dirty = Path(tmp) / "dirty.kicad_pcb"
            shutil.copy2(PCB, dirty)
            pro = PCB.with_suffix(".kicad_pro")
            dru = PCB.with_suffix(".kicad_dru")
            if pro.is_file():
                shutil.copy2(pro, dirty.with_suffix(".kicad_pro"))
            if dru.is_file():
                shutil.copy2(dru, dirty.with_suffix(".kicad_dru"))
            add_py = Path(tmp) / "add_gnd.py"
            add_py.write_text(
                "\n".join(
                    [
                        "import wx",
                        "_APP = wx.App(False)",
                        "import pcbnew",
                        f"b = pcbnew.LoadBoard({str(dirty)!r})",
                        "net = b.FindNet('GND')",
                        "t = pcbnew.PCB_TRACK(b)",
                        "t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(6.05), pcbnew.FromMM(10.00)))",
                        "t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(6.05), pcbnew.FromMM(12.00)))",
                        "t.SetWidth(pcbnew.FromMM(0.10))",
                        "t.SetLayer(pcbnew.F_Cu)",
                        "t.SetNet(net)",
                        "b.Add(t)",
                        "b.Save(str(b.GetFileName()))",
                    ]
                ),
                encoding="utf-8",
            )
            proc = subprocess.run(
                [str(kicad_py), str(add_py)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            report = Path(tmp) / "drc.json"
            proc = subprocess.run(
                ["kicad-cli", "pcb", "drc", "--format", "json", "-o", str(report), str(dirty)],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            data = json.loads(report.read_text(encoding="utf-8"))
            hits = [
                v
                for v in (data.get("violations") or [])
                if v.get("severity") == "error"
                and v.get("type") in {"clearance", "shorting_items", "tracks_crossing"}
            ]
            self.assertGreater(len(hits), 0, "foreign strip copper produced no DRC error")


class PinTableV2ParserTests(unittest.TestCase):
    SAMPLE = """
# Pin table v2 (flat coordinates)

| ref | side | u | s | rot | notes |
|---|---|---:|---:|---:|---|
| U1 | top | 8.00 | 29.35 | 0 | island |
| R6 | bottom | 14.68 | 22.37 | 0 | second side |
| P1 | top | 5.90 | 12.00 | 0 | flat strip end |

## Folded shell sites (u, s, y) — shell lane only

| ref | u | s | y |
|---|---:|---:|---:|
| P1 | 5.90 | 22.00 | 4.81 |
| P2 | 10.40 | 33.10 | 4.81 |

## J4 both-side keep-out (hole diameter plus hole clearance)

| name | u | s | diameter | clearance | layers |
|---|---:|---:|---:|---:|---|
| j4_h1 | 16.25 | 22.06 | 0.9906 | 0.20 | both |
| j4_h2 | 17.27 | 27.14 | 0.9906 | 0.20 | both |
"""

    XY_SAMPLE = """
Pin table v2 flat

| ref | side | x | y | rot |
|---|---|---:|---:|---:|
| J4 | top | 16.25 | 24.60 | 90 |
"""

    def test_flat_rows_ignore_folded_shell_sites(self) -> None:
        import sys

        sys.path.insert(0, str(ROOT / "hardware" / "board"))
        from placement_table import parse_pin_table_v2

        rows = parse_pin_table_v2(self.SAMPLE)
        refs = [r.ref for r in rows]
        self.assertEqual(refs, ["U1", "R6", "P1"])
        p1 = next(r for r in rows if r.ref == "P1")
        self.assertAlmostEqual(p1.s, 12.00)
        self.assertEqual(p1.side, "top")
        r6 = next(r for r in rows if r.ref == "R6")
        self.assertEqual(r6.side, "bottom")

    def test_flat_x_y_columns(self) -> None:
        import sys

        sys.path.insert(0, str(ROOT / "hardware" / "board"))
        from placement_table import parse_pin_table_v2

        rows = parse_pin_table_v2(self.XY_SAMPLE)
        self.assertEqual(len(rows), 1)
        self.assertAlmostEqual(rows[0].u, 16.25)
        self.assertAlmostEqual(rows[0].s, 24.60)
        self.assertAlmostEqual(rows[0].rot, 90)

    def test_j4_keepout_is_both_side_and_forbids_back_copper(self) -> None:
        import sys

        sys.path.insert(0, str(ROOT / "hardware" / "board"))
        from placement_table import forbids_back_copper, parse_j4_keepouts

        zones = parse_j4_keepouts(self.SAMPLE)
        self.assertEqual(len(zones), 2)
        self.assertTrue(all(forbids_back_copper(z) for z in zones))
        self.assertAlmostEqual(zones[0].radius, 0.9906 / 2 + 0.20)
        self.assertAlmostEqual(zones[0].u, 16.25)
        self.assertAlmostEqual(zones[0].s, 22.06)

    def test_vendored_v3_table_p4_p5_and_j4_keep_diameter(self) -> None:
        import sys

        sys.path.insert(0, str(ROOT / "hardware" / "board"))
        from placement_table import forbids_back_copper, parse_j4_keepouts, parse_pin_table_v3

        text = PACKING.read_text(encoding="utf-8")
        rows = {r.ref: r for r in parse_pin_table_v3(text)}
        self.assertEqual(len(rows), 66)
        self.assertNotIn("R9", rows)
        self.assertNotIn("R10", rows)
        self.assertAlmostEqual(rows["P4"].u, 23.32)
        self.assertAlmostEqual(rows["P4"].s, 4.35)
        self.assertAlmostEqual(rows["P5"].u, 23.32)
        self.assertAlmostEqual(rows["P5"].s, 12.35)
        self.assertAlmostEqual(rows["P1"].s, 5.29)
        self.assertAlmostEqual(rows["P2"].s, -5.81)
        self.assertAlmostEqual(rows["J2"].u, 15.15)
        self.assertAlmostEqual(rows["J2"].s, 11.35)
        self.assertAlmostEqual(rows["J3"].u, 28.41)
        self.assertAlmostEqual(rows["J4"].u, 16.52)
        self.assertAlmostEqual(rows["H1"].u, 13.23)
        zones = parse_j4_keepouts(text)
        self.assertEqual(len(zones), 3)
        self.assertTrue(all(forbids_back_copper(z) for z in zones))
        self.assertTrue(all(abs(2 * z.radius - 1.39) < 1e-6 for z in zones))


class Wp12iFootprintAndDnpTests(unittest.TestCase):
    """U2/U3 against the datasheets; Q95 R9/R10 off the PCB."""

    def _u2_block(self) -> str:
        text = PCB.read_text(encoding="utf-8")
        parts = text.split("\n\t(footprint ")
        for chunk in parts[1:]:
            if '(property "Reference" "U2"' in chunk:
                return chunk
        self.fail("U2 footprint missing")

    def test_u2_rsm_land_matches_ads1292_4219108b(self) -> None:
        # SBAS502C mechanical / 4219108/B: 4 x 4, 0.40 mm pitch, pads 0.55 x 0.20,
        # C 3.85, EP 2.8. Q98's "0.50 mm pitch" does not match that drawing.
        chunk = self._u2_block()
        self.assertIn("elicio:Texas_RSM0032", "\t(footprint " + chunk)
        pads = re.findall(
            r'\(pad "(\d+)" smd roundrect\s+\(at ([-\d.]+) ([-\d.]+)(?: [-\d.]+)?\)\s+\(size ([-\d.]+) ([-\d.]+)\)',
            chunk,
        )
        numbered = [(int(n), float(x), float(y), float(sx), float(sy)) for n, x, y, sx, sy in pads]
        self.assertEqual(len(numbered), 32)
        west = [p for p in numbered if p[0] <= 8]
        east = [p for p in numbered if 17 <= p[0] <= 24]
        south = [p for p in numbered if 9 <= p[0] <= 16]
        north = [p for p in numbered if p[0] >= 25]
        self.assertEqual(len(west), 8)
        for _n, x, _y, sx, sy in west:
            self.assertAlmostEqual(x, -1.925, places=3)
            self.assertAlmostEqual(sx, 0.55, places=3)
            self.assertAlmostEqual(sy, 0.20, places=3)
        ys = sorted(p[2] for p in west)
        for a, b in zip(ys, ys[1:]):
            self.assertAlmostEqual(b - a, 0.40, places=3)
        for _n, x, _y, sx, sy in east:
            self.assertAlmostEqual(x, 1.925, places=3)
            self.assertAlmostEqual(sx, 0.55, places=3)
        for _n, _x, y, sx, sy in south:
            self.assertAlmostEqual(y, 1.925, places=3)
            self.assertAlmostEqual(sx, 0.20, places=3)
            self.assertAlmostEqual(sy, 0.55, places=3)
        for _n, _x, y, sx, sy in north:
            self.assertAlmostEqual(y, -1.925, places=3)
        ep = re.search(r'\(pad "33" smd rect\s+\(at 0 0(?: [-\d.]+)?\)\s+\(size ([-\d.]+) ([-\d.]+)\)', chunk)
        self.assertIsNotNone(ep)
        self.assertAlmostEqual(float(ep.group(1)), 2.8, places=2)
        self.assertAlmostEqual(float(ep.group(2)), 2.8, places=2)

    def test_u3_yfp_kept_and_inner_balls_escape(self) -> None:
        # BQ25100 is DSBGA-6 only (SLUSBV8C). Pad 0.25, pitch 0.40. Gap 0.15
        # cannot take a 0.10 track at 0.10 clearance. Each ball has an exterior
        # side, so a 0.10 radial escape plus a 0.55 via 0.50 from the pad
        # centre fits inside the 1.48 courtyard. No BOM swap.
        text = PCB.read_text(encoding="utf-8")
        self.assertIn("Texas_YFP0006", text)
        self.assertIn("BQ25100YFPR", SCH.read_text(encoding="utf-8"))
        pads = {}
        for chunk in text.split("\n\t(footprint ")[1:]:
            if '(property "Reference" "U3"' not in chunk:
                continue
            for n, x, y, s in re.findall(
                r'\(pad "([A-C][12])" smd circle\s+\(at ([-\d.]+) ([-\d.]+)\)\s+\(size ([-\d.]+)',
                chunk,
            ):
                pads[n] = (float(x), float(y), float(s))
        self.assertEqual(set(pads), {"A1", "A2", "B1", "B2", "C1", "C2"})
        self.assertAlmostEqual(pads["A2"][0] - pads["A1"][0], 0.40, places=3)
        self.assertAlmostEqual(pads["C1"][1] - pads["A1"][1], 0.80, places=3)
        self.assertAlmostEqual(pads["B1"][2], 0.25, places=3)
        gap = 0.40 - 0.25
        self.assertLess(gap, 0.10 + 2 * 0.10)
        via_centre = 0.25 / 2 + 0.10 + 0.55 / 2
        self.assertAlmostEqual(via_centre, 0.50, places=2)
        self.assertLess(0.20 + via_centre, 1.48)

    def test_r9_r10_dnp_and_absent_from_pcb(self) -> None:
        sch = SCH.read_text(encoding="utf-8")
        pcb = PCB.read_text(encoding="utf-8")
        self.assertNotIn('(property "Reference" "R9"', pcb)
        self.assertNotIn('(property "Reference" "R10"', pcb)
        for ref, uuid in (
            ("R9", "b750ffb9-5366-4799-8df3-e23280612ba6"),
            ("R10", "98f44132-45fe-4b00-baab-23f5dde96cd7"),
        ):
            block = sch.split(uuid, 1)[0][-400:] + sch.split(uuid, 1)[1][:200]
            self.assertIn("(dnp yes)", block, ref)
            self.assertIn("(in_bom no)", block, ref)
            self.assertIn("(on_board no)", block, ref)


class Wp12iStiffenerAndEnvelopeTests(unittest.TestCase):
    def test_q94_stiffener_drawings_and_count(self) -> None:
        text = PCB.read_text(encoding="utf-8")
        self.assertIn("Q94 stiffeners 9 pcs", text)
        self.assertIn("Eco1 FR4 0.4 leftover B.Cu face", text)
        self.assertIn("Eco1 FR4 0.4 U1 west B.Cu", text)
        self.assertIn("Eco1 FR4 0.4 U1 RF B.Cu", text)
        self.assertIn("User.1 PI 0.1 F.Cu", text)
        for ref in ("P1", "P2", "P3", "P4", "P5"):
            self.assertIn(f"Eco2 FR4 0.2 {ref}", text)
        self.assertIn("(start 2.55 20.2)", text)
        self.assertIn("(end 8 25.7)", text)
        self.assertIn("(start 8 29.5)", text)
        self.assertIn("(end 13.9 37.3)", text)
        self.assertIn("(start 18.55 21.2)", text)
        self.assertNotIn("Eco1 FR4 0.4 #1 parts island", text)

    def test_q97_strip_has_only_its_contact_net(self) -> None:
        text = PCB.read_text(encoding="utf-8")
        regions = {
            "SIG1": (5.90 - 1.25, min(5.29, 16.00) - 3.2, 5.90 + 1.25, 16.00),
            "SIG2": (10.40 - 1.25, min(-5.81, 16.00) - 3.2, 10.40 + 1.25, 16.00),
            "REF": (8.50 - 1.25, 37.60, 8.50 + 1.25, 43.00 + 3.2),
        }
        found = {name: set() for name in regions}
        for sx, sy, ex, ey, layer, net_name in re.findall(
            r"\(segment\s+\(start ([-\d.]+) ([-\d.]+)\)\s+\(end ([-\d.]+) ([-\d.]+)\)"
            r'\s+\(width [-\d.]+\)(?:\s+\(locked yes\))?\s+\(layer "([^"]+)"\)\s+\(net "([^"]*)"',
            text,
        ):
            x0, y0, x1, y1 = float(sx), float(sy), float(ex), float(ey)
            for name, (u0, s0, u1, s1) in regions.items():
                if (u0 <= x0 <= u1 and s0 <= y0 <= s1) or (u0 <= x1 <= u1 and s0 <= y1 <= s1):
                    found[name].add((net_name, layer))
        self.assertEqual(found["SIG1"], {("SIG1", "F.Cu")})
        self.assertEqual(found["SIG2"], {("SIG2", "F.Cu")})
        self.assertEqual(found["REF"], {("REF", "F.Cu")})

    def test_q97_no_foreign_via_in_land_7x7(self) -> None:
        text = PCB.read_text(encoding="utf-8")
        land_net = {"P1": "SIG1", "P2": "SIG2", "P3": "REF", "P4": "VBUS", "P5": "GND"}
        sites = {
            "P1": (5.90, 5.29),
            "P2": (10.40, -5.81),
            "P3": (8.50, 43.00),
            "P4": (23.32, 4.35),
            "P5": (23.32, 12.35),
        }
        half = 3.50
        hits = []
        for ax, ay, net_name in re.findall(
            r'\(via\s+\(at ([-\d.]+) ([-\d.]+)\)\s+\(size [-\d.]+\)\s+\(drill [-\d.]+\)'
            r'\s+\(layers "[^"]+" "[^"]+"\)\s+\(net "([^"]*)"',
            text,
        ):
            x, y = float(ax), float(ay)
            for pad, (cx, cy) in sites.items():
                if abs(x - cx) <= half and abs(y - cy) <= half and net_name != land_net[pad]:
                    hits.append((pad, net_name, x, y))
        self.assertEqual(hits, [])

    def test_q97_island_exposed_contact_is_only_r1_r2_r3(self) -> None:
        text = PCB.read_text(encoding="utf-8")
        refs = []
        for chunk in text.split("\n\t(footprint ")[1:]:
            ref_m = re.search(r'\(property "Reference" "([^"]+)"', chunk)
            if not ref_m:
                continue
            ref = ref_m.group(1)
            at = re.search(r"\(at ([-\d.]+) ([-\d.]+)", chunk)
            if not at:
                continue
            x, y = float(at.group(1)), float(at.group(2))
            if not (2.25 <= x <= 19.75 and 16.00 <= y <= 37.60):
                continue
            body = re.split(r"\n\t\((?:gr_|segment|via|zone)", chunk, maxsplit=1)[0]
            pad_nets = []
            for pad in re.finditer(r'\(pad "[^"]+" smd[\s\S]*?\n\t\t\)', body):
                net_m = re.search(r'\(net "([^"]*)"', pad.group(0))
                if net_m:
                    pad_nets.append(net_m.group(1))
            if any(net in {"SIG1", "SIG2", "REF"} for net in pad_nets):
                refs.append(ref)
        self.assertEqual(sorted(set(refs)), ["R1", "R2", "R3"])


    def test_q98_named_channel_boxes(self) -> None:
        sys.path.insert(0, str(ROOT / "hardware" / "board"))
        from placement_table import parse_channel_keepouts

        want = {
            "HOLE_CH": (14.880, 16.050, 16.300, 19.350),
            "U2_CH": (11.620, 1.220, 18.080, 7.680),
            "U3_CH": (14.000, 28.900, 18.160, 33.600),
            "J4_CH": (13.925, 20.500, 19.125, 28.700),
            "J4_VIA_SLOT": (13.775, 21.100, 14.525, 28.100),
            "J4_APPROACH_EAST": (18.525, 20.500, 21.025, 28.700),
        }
        boxes = {z.name: z for z in parse_channel_keepouts(PACKING.read_text(encoding="utf-8"))}
        self.assertEqual(set(boxes), set(want))
        text = PCB.read_text(encoding="utf-8")
        for name, (u0, s0, u1, s1) in want.items():
            z = boxes[name]
            self.assertAlmostEqual(z.u0, u0, places=3, msg=name)
            self.assertAlmostEqual(z.s0, s0, places=3, msg=name)
            self.assertAlmostEqual(z.u1, u1, places=3, msg=name)
            self.assertAlmostEqual(z.s1, s1, places=3, msg=name)
            self.assertIn(f'(name "{name}")', text, name)

    def test_j3_breakoff_cut_on_fab_layer(self) -> None:
        text = PCB.read_text(encoding="utf-8")
        self.assertIn("J3 CUT u=22.25", text)
        self.assertIn("(layer \"F.Fab\")", text)
        self.assertIn("(start 22.25 ", text)


class PinTableV3ParserTests(unittest.TestCase):
    SAMPLE = """
# packing

## 5d. stale

| ref | side | u | s | rot |
|---|---|---:|---:|---:|
| U1 | top | 1 | 1 | 0 |

## 5e. Pin table v3 (flat coordinates)

| ref | side | u | s | rot | notes |
|---|---|---:|---:|---:|---|
""" + "\n".join(
        f"| R{i:02d} | top | {i}.00 | 10.00 | 0 | row |" for i in range(1, 65)
    ) + """
| H1 | top | 13.45 | 17.70 | 0 | hole |
| H2 | top | 17.95 | 17.70 | 0 | hole |

### Q98 channels

| name | u0 | s0 | u1 | s1 | layers |
|---|---:|---:|---:|---:|---|
| hole_gap | 15.10 | 16.05 | 16.30 | 19.35 | both |
| j4_via_slot | 13.40 | 21.10 | 14.25 | 28.10 | both |

## 6. other
"""

    def test_v3_reads_66_rows_and_skips_folded(self) -> None:
        sys.path.insert(0, str(ROOT / "hardware" / "board"))
        from placement_table import parse_channel_keepouts, parse_pin_table_v3

        rows = parse_pin_table_v3(self.SAMPLE)
        self.assertEqual(len(rows), 66)
        self.assertNotIn("U1", [r.ref for r in rows])
        self.assertEqual({r.ref for r in rows if r.ref.startswith("H")}, {"H1", "H2"})
        zones = parse_channel_keepouts(self.SAMPLE)
        self.assertEqual({z.name for z in zones}, {"hole_gap", "j4_via_slot"})

    def test_vendor_writes_only_when_5e_has_66_rows(self) -> None:
        sys.path.insert(0, str(ROOT / "hardware" / "board"))
        from placement_table import extract_section5e, parse_pin_table_v3, vendor_pin_table

        packing_doc = ROOT / "docs" / "fab" / "packing-v2.md"
        source = packing_doc.read_text(encoding="utf-8")
        self.assertIsNotNone(extract_section5e(source))
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "packing_v2_flat.md"
            dest.write_text("keep\n", encoding="utf-8")
            self.assertFalse(vendor_pin_table("no section 5e\n", dest))
            self.assertEqual(dest.read_text(encoding="utf-8"), "keep\n")
            self.assertTrue(vendor_pin_table(source, dest))
            self.assertEqual(len(parse_pin_table_v3(dest.read_text(encoding="utf-8"))), 66)
            dest2 = Path(tmp) / "v3.md"
            self.assertTrue(vendor_pin_table(self.SAMPLE, dest2))
            self.assertIn("Pin table v3", dest2.read_text(encoding="utf-8"))
            self.assertIn("hole_gap", dest2.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
