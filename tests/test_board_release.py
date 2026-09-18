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
    """Named SMT centres from the vendored pin table v2 (flat coordinates)."""
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
            self.assertFalse({"Q5", "R29", "R30"} & cpl)
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
        self.assertAlmostEqual(packing["P4"][0], 37.47, places=2)
        self.assertAlmostEqual(packing["P4"][1], 2.80, places=2)
        self.assertAlmostEqual(packing["P5"][0], 30.05, places=2)
        self.assertAlmostEqual(packing["P5"][1], 5.80, places=2)
        for ref, (px, py) in packing.items():
            if ref.startswith("H"):
                continue
            self.assertIn(ref, found, ref)
            x, y = found[ref]
            dist = ((x - px) ** 2 + (y - py) ** 2) ** 0.5
            limit = 0.50 if ref == "R24" else 0.1
            self.assertLessEqual(
                dist, limit, f"{ref} pcb=({x},{y}) packing=({px},{py}) d={dist}"
            )
        self.assertIn("H1", found)
        self.assertIn("H2", found)
        self.assertLessEqual(
            ((found["H1"][0] - 13.45) ** 2 + (found["H1"][1] - 17.70) ** 2) ** 0.5, 0.1
        )
        self.assertLessEqual(
            ((found["H2"][0] - 17.95) ** 2 + (found["H2"][1] - 17.70) ** 2) ** 0.5, 0.1
        )


class Wp12cRoutedAssertionTests(unittest.TestCase):
    def test_order_release_stays_unrouted(self) -> None:
        """WP12g: Contact and SES copper exist; DRC 0 with 0 unconnected was not reached."""
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

    def test_vendored_v2_table_p4_p5_and_j4_keep_diameter(self) -> None:
        import sys

        sys.path.insert(0, str(ROOT / "hardware" / "board"))
        from placement_table import forbids_back_copper, parse_j4_keepouts, parse_pin_table_v2

        text = PACKING.read_text(encoding="utf-8")
        rows = {r.ref: r for r in parse_pin_table_v2(text)}
        self.assertAlmostEqual(rows["P4"].u, 37.47)
        self.assertAlmostEqual(rows["P4"].s, 2.80)
        self.assertAlmostEqual(rows["P5"].u, 30.05)
        self.assertAlmostEqual(rows["P5"].s, 5.80)
        self.assertAlmostEqual(rows["P1"].s, 5.29)
        self.assertAlmostEqual(rows["P2"].s, -5.81)
        zones = parse_j4_keepouts(text)
        self.assertEqual(len(zones), 3)
        self.assertTrue(all(forbids_back_copper(z) for z in zones))
        self.assertTrue(all(abs(2 * z.radius - 1.39) < 1e-6 for z in zones))


if __name__ == "__main__":
    unittest.main()
