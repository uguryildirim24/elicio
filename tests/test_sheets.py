from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "sheets" / "template.py"
COMMITTED_DIR = ROOT / "docs" / "fab"
SHEET_NAMES = ("m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8")

try:
    import matplotlib  # noqa: F401
    import pypdf  # noqa: F401

    HAS_SHEETS = True
except ImportError:
    HAS_SHEETS = False


def load_sheets():
    spec = importlib.util.spec_from_file_location("elicio_sheets_template", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def artefact_map(out_dir: Path) -> dict[str, Path]:
    files = {"template.pdf": out_dir / "template.pdf"}
    for name in SHEET_NAMES:
        files[f"{name}.svg"] = out_dir / "sheets" / f"{name}.svg"
    return files


class TemplateConstantTests(unittest.TestCase):
    def test_winner_numbers_match_packing_v2(self) -> None:
        sheets = load_sheets()
        self.assertEqual(sheets.BODY_WIDTH, 20.0)
        self.assertEqual(sheets.BODY_ARC, 48.4)
        self.assertEqual(sheets.TOTAL_CHORD, 47.90)
        self.assertEqual(sheets.M1_GATE, 50.90)
        self.assertEqual(sheets.CONTACT_1, (5.9, 22.0))
        self.assertEqual(sheets.CONTACT_2, (10.4, 33.1))
        self.assertEqual(sheets.CONTACT_REF, (8.5, 43.0))
        self.assertEqual(sheets.SHEET_NAMES, SHEET_NAMES)


@unittest.skipUnless(HAS_SHEETS, "matplotlib/pypdf is not installed")
class TemplateRegenTests(unittest.TestCase):
    def test_script_run_twice_is_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            for dest in (first, second):
                proc = subprocess.run(
                    [sys.executable, str(SCRIPT), "--out", dest],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(proc.returncode, 0)
            left = artefact_map(Path(first))
            right = artefact_map(Path(second))
            self.assertEqual(set(left), set(right))
            for name, path in left.items():
                self.assertTrue(path.is_file(), name)
                self.assertGreater(path.stat().st_size, 0, name)
                self.assertEqual(
                    path.read_bytes(),
                    right[name].read_bytes(),
                    f"{name} differed between two runs",
                )

    def test_regen_matches_committed_files(self) -> None:
        committed = artefact_map(COMMITTED_DIR)
        missing = [name for name, path in committed.items() if not path.is_file()]
        if missing:
            self.skipTest("committed template artefacts not on the tree yet: " + ", ".join(missing))
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                [sys.executable, str(SCRIPT), "--out", tmp],
                check=True,
                capture_output=True,
                text=True,
            )
            generated = artefact_map(Path(tmp))
            for name, path in committed.items():
                self.assertEqual(
                    path.read_bytes(),
                    generated[name].read_bytes(),
                    f"committed {name} does not match a fresh run",
                )

    def test_pdf_page_is_us_letter_and_names_the_bar_check(self) -> None:
        from pypdf import PdfReader

        with tempfile.TemporaryDirectory() as tmp:
            sheets = load_sheets()
            sheets.write_all(Path(tmp))
            pdf_path = Path(tmp) / "template.pdf"
            reader = PdfReader(str(pdf_path))
            self.assertEqual(len(reader.pages), 1)
            box = reader.pages[0].mediabox
            self.assertAlmostEqual(float(box.width), 8.5 * 72, places=1)
            self.assertAlmostEqual(float(box.height), 11 * 72, places=1)
            text = reader.pages[0].extract_text() or ""
            self.assertIn("Measure the 50 mm bar before you trust this template.", text)
            self.assertIn("A_501015_series_w20_y8_iII_s3", text)


if __name__ == "__main__":
    unittest.main()
