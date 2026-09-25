"""Guard the frozen ISP1807 pin assignments against committed KiCad changes."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PCB = ROOT / "hardware/board/elicio-v4.kicad_pcb"
SCH = ROOT / "hardware/board/elicio-v4.kicad_sch"
HEADER = ROOT / "firmware/src/board_pins.h"
SKETCH = ROOT / "firmware/elicio_stream/elicio_stream.ino"

# ISP1807 datasheet R19 §3 pin table, pp. 10-11, read 2026-09-25:
# https://www.insightsip.com/fichiers_insightsip/pdf/ble/ISP1807/isp_ble_DS1807.pdf
# Quoted table cells (Pin Name): "4 P0_10 NFC2", "6 P0_26",
# "13 P0_18 RESET", "32 P0_08", "34 P0_06", "36 P0_05 AIN3",
# "38 P0_03 AIN1", "40 P0_02 AIN0", "42 P0_31 AIN7",
# "44 P0_30 AIN6", "46 P0_29 AIN5", "48 P0_28 AIN4".
# SWDIO=28, SWDCLK=30, VCC_nRF=26.
GPIO_PADS = {
    4: 10, 6: 26, 13: 18, 32: 8, 34: 6, 36: 5,
    38: 3, 40: 2, 42: 31, 44: 30, 46: 29, 48: 28,
}
NET_MACROS = {
    "AFE_SCLK": "ADS_SCLK", "AFE_MOSI": "ADS_MOSI",
    "AFE_MISO": "ADS_MISO", "AFE_CS": "ADS_CS",
    "AFE_DRDY": "ADS_DRDY", "AFE_START": "ADS_START",
    "AFE_RESET": "ADS_PWDN", "VBUS_DET": "VBUS_DET",
    "CHG_MON": "CHG_MON", "VBAT_SENSE": "VBAT_SENSE",
    "LED_EN": "LED_EN", "nRESET": "NRESET",
}
FIXED_NETS = {
    1: "GND", 7: "GND", 14: "GND", 16: "GND", 18: "GND",
    21: "GND", 23: "GND", 24: "GND", 25: "GND", 31: "GND",
    20: "RF_ANT", 22: "RF_ANT", 26: "+VDD",
    28: "SWDIO", 30: "SWDCLK",
}


def group(text: str, start: int) -> str:
    """Extract a balanced KiCad S-expression (ignoring parentheses in strings)."""
    depth = 0
    quoted = escaped = False
    for i in range(start, len(text)):
        c = text[i]
        if quoted:
            if escaped:
                escaped = False
            elif c == "\\":
                escaped = True
            elif c == '"':
                quoted = False
        elif c == '"':
            quoted = True
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    raise ValueError("unterminated KiCad group")


def pcb_pads(text: str) -> dict[int, str]:
    footprint = group(text, text.index('(footprint "elicio:InsightSiP_ISP1807"'))
    assert '(property "Reference" "U1"' in footprint
    pads = {}
    for match in re.finditer(r'\(pad "(\d+)"', footprint):
        pad = group(footprint, match.start())
        net = re.search(r'\(net "([^"]+)"\)', pad)
        if net and not net[1].startswith("unconnected-"):
            pads[int(match[1])] = net[1]
    return pads


def schematic_pins(text: str) -> dict[int, str]:
    symbol = group(text, text.index('(symbol "elicio:ISP1807"'))
    assert '(symbol "ISP1807_1_1"' in symbol
    pins = {}
    for match in re.finditer(r'\(pin (?:power_in|passive|bidirectional) line', symbol):
        pin = group(symbol, match.start())
        name = re.search(r'\(name "([^"]+)"', pin)
        number = re.search(r'\(number "(\d+)"', pin)
        if name and number:
            pins[int(number[1])] = name[1]
    return pins


class FirmwarePinsV4(unittest.TestCase):
    def test_v4_kicad_and_firmware_agree(self) -> None:
        pcb = pcb_pads(PCB.read_text(encoding="utf-8"))
        schematic = SCH.read_text(encoding="utf-8")
        sch = schematic_pins(schematic)
        header = HEADER.read_text(encoding="utf-8")
        macros = dict(re.findall(r'^#define ELICIO_PIN_(\w+) (\d+)\b', header, re.M))
        expected_pads = FIXED_NETS | {
            pad: net for pad, net in (
                (4, "AFE_START"), (6, "AFE_RESET"), (13, "nRESET"),
                (32, "AFE_MISO"), (34, "AFE_SCLK"), (36, "AFE_MOSI"),
                (38, "LED_EN"), (40, "VBUS_DET"), (42, "VBAT_SENSE"),
                (44, "CHG_MON"), (46, "AFE_DRDY"), (48, "AFE_CS"),
            )
        }
        self.assertEqual(pcb, expected_pads)  # Includes power, debug, antenna and VSS.
        self.assertEqual(set(sch), set(range(1, 65)))
        for pad in (1, 7, 14, 16, 18, 21, 23, 24, 25, 31):
            self.assertEqual(sch[pad], "VSS")
        self.assertEqual(sch[26], "VCC_nRF")
        self.assertEqual(sch[28], "SWDIO")
        self.assertEqual(sch[30], "SWDCLK")
        self.assertEqual(sch[20], "OUT_ANT")
        self.assertEqual(sch[22], "OUT_MOD")
        self.assertIn("AIN0", sch[40])  # VBUS_DET cannot use digitalRead at 3 V VDD.
        self.assertIn("AIN7", sch[42])
        self.assertIn("AIN6", sch[44])
        self.assertIn('(reference "U1")', schematic)
        # The VBUS ADC threshold assumes this divider, not just the correct U1 pad.
        resistors = {}
        for match in re.finditer(r'\(symbol\s+\(lib_id "Device:R"\)', schematic):
            symbol = group(schematic, match.start())
            reference = re.search(r'\(property "Reference" "(R18|R19)"', symbol)
            if reference:
                value = re.search(r'\(property "Value" "([^"]+)"', symbol)
                self.assertIsNotNone(value)
                resistors[reference[1]] = value[1]
        self.assertEqual(resistors, {"R18": "47k", "R19": "27k"})
        for pad, pin in GPIO_PADS.items():
            with self.subTest(pad=pad):
                self.assertTrue(sch[pad].startswith(f"P0.{pin:02d}"), sch[pad])
                macro = NET_MACROS[pcb[pad]]
                self.assertEqual(int(macros[macro]), pin)
        self.assertEqual(set(macros), set(NET_MACROS.values()))
        self.assertNotIn("BAT_MEAS_EN", macros)
        self.assertNotIn("ELICIO_PIN_LED_STREAM", header)
        self.assertNotIn("ELICIO_PIN_RECOVERY", header)
        sketch = SKETCH.read_text(encoding="utf-8")
        self.assertIn("analogRead(ELICIO_PIN_VBUS_DET) >= 1138", sketch)
        self.assertNotIn("digitalRead(ELICIO_PIN_VBUS_DET)", sketch)


if __name__ == "__main__":
    unittest.main()
