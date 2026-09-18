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

# packing-v2.md §5 named SMT centres for A_501015_series_w20_y8_iII_s3.
PACKING_NAMED = {
    "U1": (10.00, 32.35),
    "U2": (4.90, 21.25),
    "U3": (3.45, 24.85),
    "U4": (9.45, 20.20),
    "U5": (14.05, 3.10),
    "D1": (13.50, 5.30),
    "J1": (10.00, -2.15),
    "J2": (14.40, 9.15),
    "J3": (14.05, 22.60),
    "SW1": (10.10, 24.20),
}


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
            summary = json.loads(summary_path.read_text())
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
            # Review r5: ERC is clean (no lib_symbol_mismatch), DRC is counted
            # and the summary says the board is not routed.
            self.assertEqual(summary["erc_warnings"], 0)
            self.assertIs(summary["routed"], False)
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
            summary = json.loads((out / "summary.json").read_text())
            self.assertIs(summary["routed"], True)
            self.assertGreater(summary["pcb_tracks"], 0)


class PackingAgreementTests(unittest.TestCase):
    def test_named_smt_centres_match_packing_v2_within_0_1_mm(self) -> None:
        text = PCB.read_text()
        found: dict[str, tuple[float, float]] = {}
        for chunk in text.split("(footprint ")[1:]:
            at = re.search(r"\(at ([+-]?\d+(?:\.\d+)?) ([+-]?\d+(?:\.\d+)?)", chunk)
            ref = re.search(r'\(property "Reference" "([^"]+)"', chunk)
            if at and ref:
                found[ref.group(1)] = (float(at.group(1)), float(at.group(2)))
        for ref, (px, py) in PACKING_NAMED.items():
            self.assertIn(ref, found, ref)
            x, y = found[ref]
            dist = ((x - px) ** 2 + (y - py) ** 2) ** 0.5
            self.assertLessEqual(
                dist, 0.1, f"{ref} pcb=({x},{y}) packing=({px},{py}) d={dist}"
            )


if __name__ == "__main__":
    unittest.main()
