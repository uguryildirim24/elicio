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

PACKING = ROOT / "hardware" / "board" / "packing_5c_norec.md"

def packing_section5_centres() -> dict[str, tuple[float, float]]:
    """Named SMT centres from the vendored §5c no-receptacle pin table."""
    text = PACKING.read_text(encoding="utf-8")
    out: dict[str, tuple[float, float]] = {}
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5 or cells[0] in {"ref", "---"} or cells[0].startswith("---"):
            continue
        ref = cells[0]
        try:
            out[ref] = (float(cells[2]), float(cells[3]))
        except ValueError:
            continue
    return out


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
            self.assertGreater(summary["refused"].get("drc_errors", 0), 0)
            # WP12c: the shorting bus is gone; copper stays dropped.
            self.assertEqual(summary["pcb_tracks"], 0)


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
        for ref, (px, py) in packing.items():
            if ref.startswith("H"):
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
            ((found["H1"][0] - 13.45) ** 2 + (found["H1"][1] - 17.70) ** 2) ** 0.5, 0.1
        )
        self.assertLessEqual(
            ((found["H2"][0] - 17.95) ** 2 + (found["H2"][1] - 17.70) ** 2) ** 0.5, 0.1
        )


class Wp12cRoutedAssertionTests(unittest.TestCase):
    def test_order_release_stays_unrouted(self) -> None:
        """WP12c: DRC 0 was not reached. Copper stays dropped."""
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
            self.assertEqual(summary["pcb_tracks"], 0)
            self.assertGreater(summary["drc_errors"], 0)
            self.assertGreater(summary["unconnected_items"], 0)
            self.assertEqual(summary["pcb_pads_without_net"], 0)


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


if __name__ == "__main__":
    unittest.main()
