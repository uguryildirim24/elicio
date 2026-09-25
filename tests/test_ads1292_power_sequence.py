"""ADS1292 POR/reset ordering and unused GPIO contract."""
from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Ads1292PowerSequence(unittest.TestCase):
    def test_reset_after_por_and_gpio_stays_input(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            exe = Path(tmp) / "power_sequence"
            subprocess.run([
                "gcc", "-std=c11", "-Wall", "-Wextra", "-Werror",
                "-I", str(ROOT / "firmware/src"),
                str(ROOT / "firmware/src/ads1292.c"),
                str(ROOT / "tests/native/ads1292_power_sequence.c"),
                "-o", str(exe),
            ], check=True)
            subprocess.run([str(exe)], check=True)
