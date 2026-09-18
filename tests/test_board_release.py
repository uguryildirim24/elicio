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

PACKING = ROOT / "docs" / "fab" / "packing-v2.md"

# Reference designator per packing-v2.md §5 bullet (the name the bullet
# starts with). Review r6: the test reads the centres from §5 itself.
PACKING_REFS = {
    "Module Raytac": "U1",
    "ADS1292": "U2",
    "BQ25100": "U3",
    "TLV71330": "U4",
    "USBLC6-2SC6": "U5",
    "PESD5V0L1UL": "D1",
    "USB-C": "J1",
    "JST-SH": "J2",
    "Bench header": "J3",
    "Recovery switch": "SW1",
}


def packing_section5_centres() -> dict[str, tuple[float, float]]:
    """Named SMT centres from packing-v2.md §5 bullets, keyed by reference."""
    text = PACKING.read_text(encoding="utf-8")
    start = text.index("## 5. Layout for the board lane")
    end = text.index("\n## 6.", start)
    section = text[start:end]
    out: dict[str, tuple[float, float]] = {}
    for line in section.splitlines():
        if not line.startswith("- "):
            continue
        for name, ref in PACKING_REFS.items():
            if line[2:].startswith(name):
                m = re.search(r"centre \(([-\d.]+), ([-\d.]+)\)", line)
                if m:
                    out[ref] = (float(m.group(1)), float(m.group(2)))
    return out


def packing_ref_ring() -> tuple[float, float]:
    text = PACKING.read_text(encoding="utf-8")
    m = re.search(r"^- REF: \(([-\d.]+), ([-\d.]+)\)", text, re.M)
    assert m, "packing-v2.md §5 has no REF tab line"
    return float(m.group(1)), float(m.group(2))


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
        self.assertEqual(sorted(packing), sorted(PACKING_REFS.values()))
        # The REF ring is drawn at its folded site (along_floor); SIG1/SIG2
        # rings are unfolded off the island and are not compared here.
        packing["P3"] = packing_ref_ring()
        for ref, (px, py) in packing.items():
            self.assertIn(ref, found, ref)
            x, y = found[ref]
            dist = ((x - px) ** 2 + (y - py) ** 2) ** 0.5
            self.assertLessEqual(
                dist, 0.1, f"{ref} pcb=({x},{y}) packing=({px},{py}) d={dist}"
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


if __name__ == "__main__":
    unittest.main()
