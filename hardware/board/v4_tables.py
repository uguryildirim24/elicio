#!/usr/bin/env python3
"""Print the v4 flat PCB table (markdown).

Plain python: reads elicio-v4.kicad_pcb as text, no pcbnew. The flat table
is what the Gerber carries (PCB x, y = packing u, s). The folded shell-site
table (docs/fab/board-v4-design.md §10.2) is not generated yet.

Run: python3 hardware/board/v4_tables.py [--pads]
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PCB = HERE / "elicio-v4.kicad_pcb"

# Pads listed pad by pad (connectors, rings, test header).
PAD_REFS = ("P1", "P2", "P3", "P4", "P5", "J2", "J3", "J4", "SW1")


def footprints(text: str) -> list[dict]:
    out = []
    for chunk in text.split("\n\t(footprint ")[1:]:
        name = chunk.split("\n", 1)[0].strip().strip('"')
        ref = re.search(r'\(property "Reference" "([^"]+)"', chunk).group(1)
        layer = re.search(r'\n\t\t\(layer "([^"]+)"\)', chunk).group(1)
        at = re.search(r"\n\t\t\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)", chunk)
        x, y, rot = float(at.group(1)), float(at.group(2)), float(at.group(3) or 0)
        pads = []
        for pad in re.finditer(r'\n\t\t\(pad "([^"]*)" (\w+) (\w+)\s+\(at ([-\d.]+) ([-\d.]+)', chunk):
            num, kind = pad.group(1), pad.group(2)
            px, py = float(pad.group(4)), float(pad.group(5))
            th = math.radians(rot)
            ax = x + px * math.cos(th) + py * math.sin(th)
            ay = y - px * math.sin(th) + py * math.cos(th)
            tail = chunk[pad.end(): pad.end() + 1500]
            net = re.search(r'\(net "([^"]*)"\)', tail.split("\n\t\t(pad ", 1)[0])
            pads.append((num, kind, round(ax, 3), round(ay, 3), net.group(1) if net else ""))
        out.append({"ref": ref, "fp": name, "side": "bottom" if layer == "B.Cu" else "top",
                    "x": x, "y": y, "rot": rot, "pads": pads})
    return sorted(out, key=lambda f: (re.sub(r"\d", "", f["ref"]), int(re.sub(r"\D", "", f["ref"]) or 0)))


def main() -> int:
    fps = footprints(PCB.read_text(encoding="utf-8"))
    print("| ref | side | x (u) | y (s) | rot | footprint |")
    print("|---|---|---:|---:|---:|---|")
    for f in fps:
        print(f"| {f['ref']} | {f['side']} | {f['x']:.2f} | {f['y']:.2f} | {f['rot']:.0f} | `{f['fp']}` |")
    if "--pads" in sys.argv:
        print()
        print("| pad | kind | net | x (u) | y (s) |")
        print("|---|---|---|---:|---:|")
        for f in fps:
            if f["ref"] not in PAD_REFS:
                continue
            for num, kind, ax, ay, net in f["pads"]:
                if not num:
                    continue
                print(f"| {f['ref']}.{num} | {kind} | {net} | {ax:.2f} | {ay:.2f} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
