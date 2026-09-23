#!/usr/bin/env python3
"""Write the v4 library parts: ISP1807 footprint and the new symbols.

Footprint: ``lib/elicio.pretty/InsightSiP_ISP1807.kicad_mod`` from the pad
table in ``isp1807.py`` (datasheet R19 §4.1). Symbols go into
``lib/elicio.kicad_sym``; ``lib_blocks()`` returns the same text keyed
``elicio:NAME`` for embedding in the schematic (no lib_symbol_mismatch).

Run: python3 hardware/board/make_v4_lib.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from isp1807 import PIN_NAMES, pads  # noqa: E402
from sch_gen import box_symbol  # noqa: E402
from sexpr_util import lib_symbol_blocks  # noqa: E402

LIB_SYM = HERE / "lib" / "elicio.kicad_sym"
LIB_FP = HERE / "lib" / "elicio.pretty"
ISP_FP = "InsightSiP_ISP1807"

# Row 6 VSS pads between VBUS and OUT_ANT. Reaching them needs via-in-pad or
# copper in the antenna keep-out, so they carry no application net (the
# module ties every VSS inside). board-v4-design.md §3.1.
ISP_ISOLATED_VSS = ("14", "16", "18")


def _fp_line(x0, y0, x1, y1, layer, width):
    return (
        f'\t(fp_line\n\t\t(start {x0:.4f} {y0:.4f})\n\t\t(end {x1:.4f} {y1:.4f})\n'
        f'\t\t(stroke\n\t\t\t(width {width})\n\t\t\t(type solid)\n\t\t)\n\t\t(layer "{layer}")\n\t)\n'
    )


def _rect(x0, y0, x1, y1, layer, width):
    return (
        _fp_line(x0, y0, x1, y0, layer, width)
        + _fp_line(x1, y0, x1, y1, layer, width)
        + _fp_line(x1, y1, x0, y1, layer, width)
        + _fp_line(x0, y1, x0, y0, layer, width)
    )


def _text_prop(name, value, y, layer, hide=False):
    hide_s = "\n\t\t(hide yes)" if hide else ""
    return (
        f'\t(property "{name}" "{value}"\n\t\t(at 0 {y} 0)\n\t\t(layer "{layer}"){hide_s}\n'
        "\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 0.8 0.8)\n\t\t\t\t(thickness 0.12)\n\t\t\t)\n\t\t)\n\t)\n"
    )


def isp1807_footprint() -> str:
    """Module centre at the origin; KiCad view = datasheet top view (antenna half +y)."""
    out = [
        f'(footprint "{ISP_FP}"\n',
        "\t(version 20260206)\n",
        '\t(generator "elicio")\n',
        '\t(layer "F.Cu")\n',
        '\t(descr "Insight SiP ISP1807-LR nRF52840 SiP 8x8x1.0 LGA-78 (62 functional). Land = module pads, '
        'isp_ble_DS1807_R19 s4.1 p13; antenna half is +y; keep-out s4.3 p14 is drawn by the board builder")\n',
        '\t(tags "ISP1807 nRF52840 LGA")\n',
        _text_prop("Reference", "REF**", -5.0, "F.SilkS"),
        _text_prop("Value", "ISP1807-LR", 5.0, "F.Fab"),
        "\t(attr smd)\n",
        "\t(duplicate_pad_numbers_are_jumpers no)\n",
        _rect(-4.0, -4.0, 4.0, 4.0, "F.Fab", 0.1),
        _rect(-4.25, -4.25, 4.25, 4.25, "F.CrtYd", 0.05),
        _fp_line(-4.0, 0.0, 4.0, 0.0, "F.Fab", 0.1),
        _fp_line(-4.12, -4.12, -3.2, -4.12, "F.SilkS", 0.12),
        _fp_line(-4.12, -4.12, -4.12, -3.2, "F.SilkS", 0.12),
    ]
    for num, (x, y, w, h) in sorted(pads().items(), key=lambda kv: int(kv[0])):
        out.append(
            f'\t(pad "{num}" smd rect\n\t\t(at {x - 4.0:.4f} {y - 4.0:.4f})\n\t\t(size {w} {h})\n'
            '\t\t(layers "F.Cu" "F.Mask" "F.Paste")\n\t)\n'
        )
    out.append("\t(embedded_fonts no)\n)\n")
    return "".join(out)


def isp1807_symbol(lib: str) -> str:
    etype = {}
    for n, name in PIN_NAMES.items():
        if name == "VSS":
            etype[n] = "power_in"
        elif name == "VCC_nRF":
            etype[n] = "power_in"
        elif name == "VBUS":
            etype[n] = "power_in"
        elif name in ("OUT_ANT", "OUT_MOD"):
            etype[n] = "passive"
        elif name == "NC":
            etype[n] = "no_connect"
        else:
            etype[n] = "bidirectional"
    for n in ISP_ISOLATED_VSS:
        etype[int(n)] = "passive"
    left_order = [26, 12, 28, 30, 13, 20, 22, 8, 10, 1, 7, 21, 23, 24, 25, 31, 14, 16, 18]
    left = [(str(n), PIN_NAMES[n], etype[n]) for n in left_order]
    rest = [n for n in range(1, 65) if n not in left_order]

    def gpio_key(n):
        m = re.match(r"P(\d)\.(\d+)", PIN_NAMES[n])
        return (int(m.group(1)), int(m.group(2))) if m else (9, n)

    right = [(str(n), PIN_NAMES[n], etype[n]) for n in sorted(rest, key=gpio_key)]
    bottom = [(str(n), "NC", "no_connect") for n in range(65, 79)]
    return box_symbol(
        lib,
        "ISP1807",
        "U",
        "Insight SiP ISP1807-LR nRF52840 SiP, 8x8x1.0 LGA, integrated antenna",
        left,
        right,
        footprint=f"elicio:{ISP_FP}",
        bottom=bottom,
    )


def ldo_dqn_symbol(lib: str, name: str, description: str) -> str:
    # TI X2SON-4 DQN: 1 OUT, 2 GND, 3 EN, 4 IN, 5 thermal pad (GND).
    return box_symbol(
        lib,
        name,
        "U",
        description,
        [("4", "IN", "power_in"), ("3", "EN", "input")],
        [("1", "OUT", "power_out"), ("2", "GND", "power_in"), ("5", "EP", "passive")],
        footprint="Package_SON:Texas_X2SON-4_1x1mm_P0.65mm",
    )


NEW_SYMBOLS = {
    "ISP1807": lambda lib: isp1807_symbol(lib),
    "TLV71330PDQN": lambda lib: ldo_dqn_symbol(
        lib, "TLV71330PDQN", "TI TLV713 3.0 V 150 mA LDO, X2SON-4 DQN 1x1"
    ),
    "TPS7A0230PDQN": lambda lib: ldo_dqn_symbol(
        lib, "TPS7A0230PDQN", "TI TPS7A02 3.0 V 200 mA 25 nA-Iq LDO, X2SON-4 DQN 1x1"
    ),
}


def write_symbols() -> None:
    text = LIB_SYM.read_text(encoding="utf-8")
    have = lib_symbol_blocks(text, "kicad_symbol_lib")
    for name, make in NEW_SYMBOLS.items():
        block = make("")
        if name in have:
            text = text.replace(have[name], block.strip())
        else:
            end = text.rstrip().rfind(")")
            text = text[:end].rstrip() + "\n\t" + block.strip() + "\n)\n"
    LIB_SYM.write_text(text, encoding="utf-8")


def lib_blocks() -> dict[str, str]:
    """Embedded form of every elicio symbol, keyed elicio:NAME."""
    text = LIB_SYM.read_text(encoding="utf-8")
    out = {}
    for name, block in lib_symbol_blocks(text, "kicad_symbol_lib").items():
        emb = block.replace(f'(symbol "{name}"', f'(symbol "elicio:{name}"', 1)
        out[f"elicio:{name}"] = emb
    return out


def wall_ring_footprint() -> str:
    """P4/P5 wall ring: copper Ø4.6 so the Ø5.2 outline stays inside y 1.7-6.9 (§4.4)."""
    text = (LIB_FP / "RING_PAD_D5_H2.7.kicad_mod").read_text(encoding="utf-8")
    swaps = [
        ('"RING_PAD_D5_H2.7"', '"RING_PAD_D4.6_H2.7"'),
        (
            "Interface II ring pad: ENIG ring Ø5.0 mm",
            "Wall charge ring (P4/P5, board v4): ENIG ring Ø4.6 mm, outline Ø5.2 between floor and lid",
        ),
        ("(end 3.2 0)", "(end 2.9 0)"),
        ("(end 2.5 0)", "(end 2.3 0)"),
        ("(size 5 5)", "(size 4.6 4.6)"),
    ]
    for old, new in swaps:
        if old not in text:
            raise ValueError(f"ring template changed: {old!r} missing")
        text = text.replace(old, new)
    return text


def main() -> None:
    (LIB_FP / f"{ISP_FP}.kicad_mod").write_text(isp1807_footprint(), encoding="utf-8")
    (LIB_FP / "RING_PAD_D4.6_H2.7.kicad_mod").write_text(wall_ring_footprint(), encoding="utf-8")
    write_symbols()
    print("wrote", LIB_FP / f"{ISP_FP}.kicad_mod", "and", ", ".join(NEW_SYMBOLS))


if __name__ == "__main__":
    main()
