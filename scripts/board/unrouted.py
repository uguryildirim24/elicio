#!/usr/bin/env python3
"""Inventory every KiCad DRC airwire on a PCB, including copper-island pad anchors.

Run with KiCad's bundled Python: python3 scripts/board/unrouted.py PCB DRC.json OUT.md
The positions/distance are the DRC airwire endpoints, NOT claimed available
routing channels; a track/via's nearest electrically connected pad is named
only as an island anchor. Never substitute the nearest unconnected pad.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import wx

_APP = wx.App(False)
import pcbnew


def mm(x: int) -> float:
    return pcbnew.ToMM(x)


def main(pcb: Path, drc: Path, output: Path) -> None:
    board = pcbnew.LoadBoard(str(pcb))
    connectivity = board.GetConnectivity()
    items = {item.m_Uuid.AsString(): item for item in [*board.GetTracks(), *board.GetPads()]}
    rats = json.loads(drc.read_text(encoding="utf-8"))["unconnected_items"]

    def endpoint(info: dict) -> str:
        item = items.get(info["uuid"])
        if item is None:
            raise ValueError(f"DRC item {info['uuid']} not on {pcb}")
        pos = info["pos"]
        desc = info["description"]
        site = f"({pos['x']:.3f}, {pos['y']:.3f})"
        if item.GetClass() == "PAD":
            pad = item
            label = f"{pad.GetParentFootprint().GetReference()}.{pad.GetNumber()}"
            layer = "F.Cu/B.Cu" if desc.startswith("PTH pad") else desc.split(" on ")[-1].split(" (")[0]
            return f"{label} {site} ({layer})"
        layer = desc.split(" on ")[-1].split(",")[0]
        pads = list(connectivity.GetConnectedPads(item))
        if pads:
            pad = min(pads, key=lambda p: math.dist(
                (mm(p.GetPosition().x), mm(p.GetPosition().y)),
                (pos["x"], pos["y"]),
            ))
            label = f"{pad.GetParentFootprint().GetReference()}.{pad.GetNumber()}"
            xy = pad.GetPosition()
            anchor = f"({mm(xy.x):.3f}, {mm(xy.y):.3f})"
            return f"{desc.split(' [')[0]} {site} ({layer}) → island anchored at {label} {anchor}"
        return f"{desc.split(' [')[0]} {site} ({layer}) → no pad on this copper island"

    rows = []
    for index, rat in enumerate(rats, 1):
        a, b = rat["items"][:2]
        net = a["description"].split("[")[1].split("]")[0]
        distance = math.dist((a["pos"]["x"], a["pos"]["y"]),
                             (b["pos"]["x"], b["pos"]["y"]))
        rows.append(f"| {index} | {net} | {endpoint(a)} | {endpoint(b)} | {distance:.3f} |")
    output.write_text(
        "# WP12i unresolved board connections (flat PCB, millimetres)\n\n"
        f"Source: `{pcb.name}` and KiCad DRC JSON, {len(rats)} unconnected items. "
        "Each row is a distinct KiCad airwire. Pad labels are physical pads; "
        "when the DRC endpoint is a track or via, its named pad is only a "
        "connected island anchor, not necessarily the trace end. 'No pad' "
        "means an isolated copper stub. Endpoint distance is straight-line, "
        "not available channel width or routed length. KiCad may choose different "
        "endpoints for an equivalent airwire on a repeat DRC; the rows are a "
        "snapshot, not stable identifiers. F/B sides and actual copper obstructions "
        "must be checked before routing. Do not order.\n\n"
        "| # | Net | Endpoint A / pad anchor | Endpoint B / pad anchor | Endpoint gap (mm) |\n"
        "|---:|---|---|---|---:|\n" + "\n".join(rows) + "\n",
        encoding="utf-8",
    )
    print(f"{output}: {len(rows)} airwires")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit("usage: unrouted.py PCB DRC.json OUT.md")
    main(*(Path(arg) for arg in sys.argv[1:]))
