#!/usr/bin/env python3
"""Place elicio-v2 from packing-v2.md §5, sync nets, route, save.

WP12b. Packing (u, s) = PCB (x, y). SIG1/SIG2 rings unfold off the island.
"""
from __future__ import annotations

import math
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import wx

_APP = wx.App(False)

import pcbnew  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from maze_route import maze_route, add_via  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
BOARD_DIR = ROOT / "hardware" / "board"
KICAD_FP = Path("/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints")
LOCAL_FP = BOARD_DIR / "lib" / "elicio.pretty"
JAVA = Path("/opt/homebrew/opt/openjdk@21/bin/java")
FREEROUTE_JAR = Path("/tmp/wp12b/freerouting.jar")

BOARD_U0, BOARD_U1 = 2.25, 17.75
BOARD_S0, BOARD_S1 = 18.60, 37.60
NECK_U0 = 12.50
USB_U0, USB_U1 = 4.50, 15.50
USB_S0, USB_S1 = -7.70, 1.50

SIG1_SITE = (5.90, 22.00)
SIG1_ATTACH_PACK = (5.90, 29.00)
SIG2_SITE = (10.40, 33.10)
SIG2_ATTACH_PACK = (10.40, 26.10)
REF_SITE = (8.50, 43.00)
REF_ATTACH_PACK = (8.50, 36.80)

TAB_LEN_SIG1 = math.hypot(SIG1_SITE[0] - SIG1_ATTACH_PACK[0], SIG1_SITE[1] - SIG1_ATTACH_PACK[1])
TAB_LEN_SIG2 = math.hypot(SIG2_SITE[0] - SIG2_ATTACH_PACK[0], SIG2_SITE[1] - SIG2_ATTACH_PACK[1])
TAB_STRIP = 2.5
TAB_CAP_R = 3.0

SIG1_ATTACH = (BOARD_U0, SIG1_SITE[1])
SIG1_RING = (BOARD_U0 - TAB_LEN_SIG1, SIG1_SITE[1])
SIG2_ATTACH = (BOARD_U1, SIG2_SITE[1])
SIG2_RING = (BOARD_U1 + TAB_LEN_SIG2, SIG2_SITE[1])
REF_ATTACH = (REF_SITE[0], BOARD_S1)
REF_RING = REF_SITE

LIBS = {
    "elicio": LOCAL_FP,
    "RF_Module": KICAD_FP / "RF_Module.pretty",
    "Package_DFN_QFN": KICAD_FP / "Package_DFN_QFN.pretty",
    "Package_TO_SOT_SMD": KICAD_FP / "Package_TO_SOT_SMD.pretty",
    "Package_BGA": KICAD_FP / "Package_BGA.pretty",
    "Connector_USB": KICAD_FP / "Connector_USB.pretty",
    "Connector_JST": KICAD_FP / "Connector_JST.pretty",
    "Connector": KICAD_FP / "Connector.pretty",
    "Connector_PinHeader_2.54mm": KICAD_FP / "Connector_PinHeader_2.54mm.pretty",
    "Button_Switch_SMD": KICAD_FP / "Button_Switch_SMD.pretty",
    "Resistor_SMD": KICAD_FP / "Resistor_SMD.pretty",
    "Capacitor_SMD": KICAD_FP / "Capacitor_SMD.pretty",
    "Inductor_SMD": KICAD_FP / "Inductor_SMD.pretty",
    "LED_SMD": KICAD_FP / "LED_SMD.pretty",
    "Diode_SMD": KICAD_FP / "Diode_SMD.pretty",
}

# packing-v2.md §5 named centres. Rotation chosen so courtyards match the packing box.
NAMED = {
    "U1": (10.00, 32.35, 90),
    "U2": (4.90, 21.25, 0),
    "U3": (3.45, 24.85, 0),
    "U4": (9.45, 20.20, 0),
    "U5": (14.05, 3.10, 0),
    "D1": (13.50, 5.30, 90),
    "J1": (10.00, -2.15, 0),
    "J2": (14.40, 9.15, 90),
    "J3": (14.05, 22.60, 0),
    "J4": (15.10, 5.40, 90),
    "SW1": (10.10, 24.20, 0),
    "P1": (SIG1_RING[0], SIG1_RING[1], 0),
    "P2": (SIG2_RING[0], SIG2_RING[1], 0),
    "P3": (REF_RING[0], REF_RING[1], 0),
}

# 220 kΩ at the tab entries, past the 4 mm strain-relief window.
TAB_PARTS = {
    "R1": ((SIG1_ATTACH[0] + SIG1_RING[0]) / 2.0, SIG1_RING[1], 90),
    "R2": ((SIG2_ATTACH[0] + SIG2_RING[0]) / 2.0, SIG2_RING[1], 90),
    "R3": (REF_RING[0], (REF_ATTACH[1] + REF_RING[1]) / 2.0, 0),
}

FRONT_PASSIVES = {
    "R9": (5.30, -5.40, 90),
    "R10": (14.70, -5.40, 90),
    "R18": (5.30, -3.60, 90),
    "R19": (14.70, -3.60, 90),
}
FRONT_KEEP = set(NAMED) | set(TAB_PARTS) | set(FRONT_PASSIVES)

# Q68 caps sit on the back under the ADS (courtyards are per-layer).
DECOUPLE_BACK = {
    "C6": (3.70, 20.20, 0),
    "C7": (6.10, 20.20, 0),
    "C8": (3.70, 22.30, 0),
    "C15": (6.10, 22.30, 0),
}

PACK_0402 = [
    (13.25, 2.10, 0),
    (13.25, 3.30, 0),
    (13.25, 4.50, 0),
    (13.25, 5.70, 0),
    (13.25, 6.90, 0),
    (13.25, 8.10, 0),
    (13.25, 10.50, 0),
    (13.25, 11.70, 0),
    (13.25, 12.90, 0),
    (13.25, 14.10, 0),
    (13.25, 15.30, 0),
    (13.25, 16.50, 0),
    (14.75, 2.70, 90),
    (14.75, 4.80, 90),
    (14.75, 6.90, 90),
    (14.75, 11.10, 90),
    (14.75, 13.20, 90),
    (14.75, 15.30, 90),
    (15.35, 16.80, 0),
    (16.55, 11.00, 0),
    (16.55, 13.20, 0),
    (16.55, 15.40, 0),
    (6.20, -6.40, 0),
    (7.40, -6.40, 0),
    (8.60, -6.40, 0),
    (11.40, -6.40, 0),
    (12.60, -6.40, 0),
    (13.80, -6.40, 0),
    (5.40, -0.20, 0),
    (6.60, -0.20, 0),
    (13.40, -0.20, 0),
    (16.20, 3.40, 90),
    (16.20, 5.60, 90),
    (16.20, 7.80, 90),
    (11.90, 19.25, 0),
    (11.90, 20.60, 0),
    (5.15, 24.65, 0),
    (6.50, 24.65, 0),
    (6.95, 26.00, 0),
    (16.40, 19.80, 90),
    (16.40, 21.90, 90),
    (16.40, 25.80, 90),
]


def v2(x: float, y: float):
    return pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y))


def tab_detour(attach, ring, half_w: float = TAB_STRIP / 2, cap_r: float = TAB_CAP_R, n: int = 18):
    ax, ay = attach
    rx, ry = ring
    dx, dy = rx - ax, ry - ay
    length = math.hypot(dx, dy)
    ux, uy = dx / length, dy / length
    wx, wy = -uy, ux
    lx, ly = -wx * half_w, -wy * half_w
    tx, ty = wx * half_w, wy * half_w
    chord = math.sqrt(max(cap_r * cap_r - half_w * half_w, 0.0))
    along = length - chord

    def pt(dist, ox, oy):
        return (ax + ux * dist + ox, ay + uy * dist + oy)

    lead_root = pt(0.0, lx, ly)
    lead_chord = pt(along, lx, ly)
    trail_chord = pt(along, tx, ty)
    trail_root = pt(0.0, tx, ty)
    a0 = math.atan2(lead_chord[1] - ry, lead_chord[0] - rx)
    a1 = math.atan2(trail_chord[1] - ry, trail_chord[0] - rx)
    afar = math.atan2(uy, ux)
    ccw_span = (a1 - a0) % (2 * math.pi)
    afar_from_a0 = (afar - a0) % (2 * math.pi)
    if 0.0 < afar_from_a0 < ccw_span:
        span, sign = ccw_span, 1.0
    else:
        span, sign = (a0 - a1) % (2 * math.pi), -1.0
    pts = [lead_root, lead_chord]
    for i in range(1, n):
        ang = a0 + sign * span * i / n
        pts.append((rx + cap_r * math.cos(ang), ry + cap_r * math.sin(ang)))
    pts.extend([trail_chord, trail_root])
    return pts


def add_segments(board, pts, layer, width=0.05, close=False) -> None:
    seq = list(pts)
    if close:
        seq = seq + [seq[0]]
    for (x0, y0), (x1, y1) in zip(seq, seq[1:]):
        s = pcbnew.PCB_SHAPE(board)
        s.SetShape(pcbnew.SHAPE_T_SEGMENT)
        s.SetLayer(layer)
        s.SetStart(v2(x0, y0))
        s.SetEnd(v2(x1, y1))
        s.SetWidth(pcbnew.FromMM(width))
        board.Add(s)


def add_filled_rect(board, x0, y0, x1, y1, layer) -> None:
    s = pcbnew.PCB_SHAPE(board)
    s.SetShape(pcbnew.SHAPE_T_RECT)
    s.SetFilled(True)
    s.SetLayer(layer)
    s.SetStart(v2(x0, y0))
    s.SetEnd(v2(x1, y1))
    s.SetWidth(pcbnew.FromMM(0.05))
    board.Add(s)


def add_keepout(board, x0, y0, x1, y1, name, allow_pads: bool, allow_tracks: bool = False) -> None:
    zone = pcbnew.ZONE(board)
    zone.SetIsRuleArea(True)
    zone.SetDoNotAllowTracks(not allow_tracks)
    zone.SetDoNotAllowVias(True)
    zone.SetDoNotAllowZoneFills(True)
    zone.SetDoNotAllowPads(not allow_pads)
    zone.SetDoNotAllowFootprints(False)
    zone.SetLayerSet(pcbnew.LSET.AllCuMask())
    zone.SetZoneName(name)
    poly = zone.Outline()
    poly.NewOutline()
    for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)):
        poly.Append(pcbnew.FromMM(x), pcbnew.FromMM(y))
    board.Add(zone)


def add_text(board, x, y, text, layer, size=0.7) -> None:
    t = pcbnew.PCB_TEXT(board)
    t.SetText(text)
    t.SetPosition(v2(x, y))
    t.SetLayer(layer)
    t.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(size), pcbnew.FromMM(size)))
    t.SetTextThickness(pcbnew.FromMM(max(0.10, size * 0.15)))
    board.Add(t)


def add_copper_zone(board, name: str, net, pts, layer) -> None:
    zone = pcbnew.ZONE(board)
    zone.SetIsRuleArea(False)
    zone.SetNet(net)
    zone.SetLayer(layer)
    zone.SetLocalClearance(pcbnew.FromMM(0.15))
    zone.SetMinThickness(pcbnew.FromMM(0.15))
    zone.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL)
    zone.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_NEVER)
    zone.SetAssignedPriority(0)
    zone.SetZoneName(name)
    poly = zone.Outline()
    poly.NewOutline()
    for x, y in pts:
        poly.Append(pcbnew.FromMM(x), pcbnew.FromMM(y))
    board.Add(zone)


def outline_points():
    pts = [
        (USB_U0, USB_S0),
        (USB_U1, USB_S0),
        (USB_U1, USB_S1),
        (BOARD_U1, USB_S1),
    ]
    pts += tab_detour(SIG2_ATTACH, SIG2_RING)
    pts += [(BOARD_U1, BOARD_S1)]
    pts += tab_detour(REF_ATTACH, REF_RING)
    pts += [(BOARD_U0, BOARD_S1)]
    pts += tab_detour(SIG1_ATTACH, SIG1_RING)
    pts += [
        (BOARD_U0, BOARD_S0),
        (NECK_U0, BOARD_S0),
        (NECK_U0, USB_S1),
        (USB_U0, USB_S1),
    ]
    return pts


def island_outline():
    return [
        (USB_U0, USB_S0),
        (USB_U1, USB_S0),
        (USB_U1, USB_S1),
        (BOARD_U1, USB_S1),
        (BOARD_U1, BOARD_S1),
        (BOARD_U0, BOARD_S1),
        (BOARD_U0, BOARD_S0),
        (NECK_U0, BOARD_S0),
        (NECK_U0, USB_S1),
        (USB_U0, USB_S1),
    ]


def load_fp(lib_id: str):
    lib, name = lib_id.split(":", 1)
    pretty = LIBS.get(lib)
    if pretty is None:
        raise KeyError(lib_id)
    io = pcbnew.PCB_IO_KICAD_SEXPR()
    loaded = io.FootprintLoad(str(pretty), name)
    if loaded is None:
        raise FileNotFoundError(lib_id)
    fp = pcbnew.FOOTPRINT(loaded)
    return fp


def parse_netlist(path: Path) -> tuple[dict[str, dict], dict[tuple[str, str], str]]:
    text = path.read_text()
    comps: dict[str, dict] = {}
    comp_sec = text[text.find("(components") : text.find("(libparts")]
    for m in re.finditer(
        r'\(ref "([^"]+)"\)\s*\(value "([^"]*)"\)\s*\(footprint "([^"]*)"\)',
        comp_sec,
    ):
        ref, value, fp = m.group(1), m.group(2), m.group(3)
        comps[ref] = {"value": value, "footprint": fp}
    # dnp / extra fields
    for block in text.split("(comp\n")[1:]:
        rm = re.search(r'\(ref "([^"]+)"\)', block)
        if not rm:
            continue
        ref = rm.group(1)
        if ref in comps:
            comps[ref]["dnp"] = "(fields" in block and "DNP" in block[:800]
    nets: dict[tuple[str, str], str] = {}
    nets_section = text[text.find("(nets") :]
    for block in re.split(r"\n\t\t\(net\n", nets_section)[1:]:
        nm = re.search(r'\(name "([^"]+)"\)', block)
        if not nm:
            continue
        name = nm.group(1)
        for ref, pin in re.findall(r'\(ref "([^"]+)"\)\s*\(pin "([^"]+)"\)', block):
            nets[(ref, pin)] = name
    return comps, nets


def ensure_net(board, name: str):
    net = board.FindNet(name)
    if net is None or net.GetNetCode() == 0:
        item = pcbnew.NETINFO_ITEM(board, name)
        board.Add(item)
        net = item
    return net


def strip_silk(fp) -> None:
    fp.Reference().SetVisible(False)
    fp.Value().SetVisible(False)
    fp.Reference().SetLayer(pcbnew.F_Fab)
    fp.Value().SetLayer(pcbnew.F_Fab)
    doomed = []
    for gi in list(fp.GraphicalItems()):
        try:
            ly = gi.GetLayer()
        except Exception:
            continue
        if ly in (pcbnew.F_SilkS, pcbnew.B_SilkS):
            doomed.append(gi)
    for gi in doomed:
        fp.Remove(gi)


def pad_in_rect(pad, x0, y0, x1, y1) -> bool:
    p = pad.GetPosition()
    x, y = pcbnew.ToMM(p.x), pcbnew.ToMM(p.y)
    return x0 - 0.05 <= x <= x1 + 0.05 and y0 - 0.05 <= y <= y1 + 0.05


def place_fp(board, ref: str, lib_id: str, x: float, y: float, rot: float, value: str, dnp: bool):
    if ref in {"P1", "P2", "P3"}:
        lib_id = "elicio:RING_PAD_D5_H2.7"
    fp = load_fp(lib_id)
    fp.SetReference(ref)
    fp.SetValue(value)
    fp.SetPosition(v2(x, y))
    fp.SetOrientationDegrees(rot)
    if dnp:
        fp.SetDNP(True)
    if ref in {"J4", "P1", "P2", "P3"} or dnp:
        fp.SetExcludedFromBOM(True)
        if ref in {"P1", "P2", "P3", "J4"}:
            fp.SetExcludedFromPosFiles(True)
    board.Add(fp)
    return fp


def back_sites_by_kind() -> dict[str, list[tuple[float, float, float]]]:
    sot = [
        (16.05, 20.40, 90),
        (16.05, 24.00, 90),
        (16.05, 27.60, 90),
        (16.05, 31.20, 90),
        (16.05, 34.80, 90),
    ]
    big = [
        (15.20, 26.20, 0),
        (13.20, 26.20, 0),
        (11.20, 26.20, 0),
    ]
    small = []
    # Under the module, east of the RF box. Leave the ADS island back empty for vias.
    for u in (7.80, 9.80, 11.80, 13.80, 15.80):
        for s in (28.90, 30.90, 32.90, 34.90, 36.80):
            small.append((u, s, 0))
    # Under the USB tongue (front is the receptacle).
    for u in (6.20, 8.20, 11.80, 13.80):
        for s in (-6.20, -4.40, -2.60):
            small.append((u, s, 0))
    return {"sot": sot, "0603": big, "0402": small}


def fp_kind(fp) -> str:
    name = str(fp.GetFPIDAsString())
    if "SOT-23" in name:
        return "sot"
    if "0603" in name or "1608" in name:
        return "0603"
    return "0402"


def assign_nets(board, nets: dict[tuple[str, str], str]) -> None:
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        for pad in fp.Pads():
            num = pad.GetNumber()
            name = nets.get((ref, num)) or nets.get((ref, num.upper())) or nets.get((ref, num.lower()))
            if name is None:
                # USB shell / mechanical / unmatched
                if num.upper() in {"SH", "S1", "S2", "MP", "MOUNT", "A1", "B1", "A12", "B12"}:
                    name = "GND"
            if name is None:
                name = f"NC-{ref}-{num}"
            pad.SetNet(ensure_net(board, name))


def configure_rules(board) -> None:
    ds = board.GetDesignSettings()
    ds.SetBoardThickness(pcbnew.FromMM(0.11))
    ds.m_TrackMinWidth = pcbnew.FromMM(0.10)
    ds.m_MinClearance = pcbnew.FromMM(0.10)
    ds.m_ViasMinSize = pcbnew.FromMM(0.70)
    ds.m_ViasMinDrill = pcbnew.FromMM(0.30)
    ds.m_ViasMinAnnularWidth = pcbnew.FromMM(0.18)
    ds.m_CopperEdgeClearance = pcbnew.FromMM(0.30)
    ds.m_HoleToHoleMin = pcbnew.FromMM(0.25)
    ds.m_MinThroughDrill = pcbnew.FromMM(0.30)
    ds.m_HoleClearance = pcbnew.FromMM(0.20)
    if hasattr(ds, "m_SolderMaskMargin"):
        ds.m_SolderMaskMargin = pcbnew.FromMM(0.10)


def add_via(board, net, x: float, y: float) -> None:
    via = pcbnew.PCB_VIA(board)
    via.SetPosition(v2(x, y))
    via.SetWidth(pcbnew.FromMM(0.55))
    via.SetDrill(pcbnew.FromMM(0.30))
    via.SetNet(net)
    board.Add(via)


def manhattan_track(board, net, x0, y0, x1, y1, layer) -> None:
    w = pcbnew.FromMM(0.10)
    def seg(a, b, c, d):
        if abs(a - c) < 0.01 and abs(b - d) < 0.01:
            return
        t = pcbnew.PCB_TRACK(board)
        t.SetStart(v2(a, b))
        t.SetEnd(v2(c, d))
        t.SetWidth(w)
        t.SetLayer(layer)
        t.SetNet(net)
        board.Add(t)

    if abs(x0 - x1) < 0.05:
        seg(x0, y0, x1, y1)
        return
    if abs(y0 - y1) < 0.05:
        seg(x0, y0, x1, y1)
        return
    mid_x, mid_y = x1, y0
    if 2.25 <= min(x0, mid_x) <= 6.05 and 26.15 <= y0 <= 38.55:
        mid_x, mid_y = x0, y1
    seg(x0, y0, mid_x, mid_y)
    seg(mid_x, mid_y, x1, y1)


def simple_route(board) -> None:
    pads_by_net: dict[int, list] = {}
    for fp in board.GetFootprints():
        for pad in fp.Pads():
            code = pad.GetNetCode()
            if code <= 0:
                continue
            pads_by_net.setdefault(code, []).append(pad)
    for code, pads in pads_by_net.items():
        net = pads[0].GetNet()
        name = net.GetNetname()
        if name == "GND" or name.startswith("unconnected") or name.startswith("NC-"):
            continue
        if len(pads) < 2:
            continue
        pts = []
        for pad in pads:
            p = pad.GetPosition()
            pts.append((pcbnew.ToMM(p.x), pcbnew.ToMM(p.y), pad))
        unused = set(range(1, len(pts)))
        cur = 0
        while unused:
            cx, cy, _ = pts[cur]
            nxt = min(unused, key=lambda i: (pts[i][0] - cx) ** 2 + (pts[i][1] - cy) ** 2)
            unused.remove(nxt)
            x0, y0, p0 = pts[cur]
            x1, y1, p1 = pts[nxt]
            ly0 = p0.GetLayer()
            ly1 = p1.GetLayer()
            if ly0 not in (pcbnew.F_Cu, pcbnew.B_Cu):
                ly0 = pcbnew.F_Cu
            if ly1 not in (pcbnew.F_Cu, pcbnew.B_Cu):
                ly1 = pcbnew.F_Cu
            if ly0 != ly1:
                mx, my = (x0 + x1) / 2.0, (y0 + y1) / 2.0
                manhattan_track(board, net, x0, y0, mx, my, ly0)
                add_via(board, net, mx, my)
                manhattan_track(board, net, mx, my, x1, y1, ly1)
            else:
                manhattan_track(board, net, x0, y0, x1, y1, ly0)
            cur = nxt


def hide_silk_in_file(path: Path) -> None:
    text = path.read_text()
    text = text.replace('(layer "F.SilkS")', '(layer "F.Fab")')
    text = text.replace('(layer "B.SilkS")', '(layer "B.Fab")')
    path.write_text(text)


def build() -> None:
    sch = BOARD_DIR / "elicio-v2.kicad_sch"
    net_path = Path("/tmp/wp12b/elicio-v2.net")
    net_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["kicad-cli", "sch", "export", "netlist", "--format", "kicadsexpr", "-o", str(net_path), str(sch)],
        check=True,
    )
    comps, nets = parse_netlist(net_path)
    print("comps", len(comps), "placed named", list(NAMED))
    if "U1" not in comps:
        raise SystemExit(f"U1 missing from netlist parse, have {sorted(comps)[:20]}")
    skip = {r for r, c in comps.items() if not c["footprint"] or ":" not in c["footprint"]}
    skip |= {r for r, c in comps.items() if c["footprint"].startswith("power:")}
    skip |= {r for r, c in comps.items() if "PAD_8x8" in c["footprint"]}

    out = BOARD_DIR / "elicio-v2.kicad_pcb"
    board = pcbnew.NewBoard(str(out))
    board.SetCopperLayerCount(2)
    configure_rules(board)
    add_segments(board, outline_points(), pcbnew.Edge_Cuts, close=True)

    # Antenna keep-out packing §5 / r5 defect 4. Pads allowed so the module land can sit.
    add_keepout(board, 2.25, 26.15, 6.05, 38.55, "RF_NO_COPPER", allow_pads=True)
    add_keepout(board, 6.05, 33.05, 7.25, 34.65, "RF_FEED_NOTCH", allow_pads=False)
    for (cx, cy), name in (
        (SIG1_RING, "RING_SIG1_CLEAR"),
        (SIG2_RING, "RING_SIG2_CLEAR"),
        (REF_RING, "RING_REF_CLEAR"),
    ):
        add_keepout(board, cx - 3.5, cy - 3.5, cx + 3.5, cy + 3.5, name, allow_pads=True, allow_tracks=True)

    # Q60: two FR4 0.4 pieces (parts island + USB/pocket). No tab stiffener: Q58 clamp.
    add_filled_rect(board, 2.55, 18.90, 17.45, 37.30, pcbnew.Eco1_User)
    add_filled_rect(board, 4.70, -7.40, 15.30, 12.20, pcbnew.Eco1_User)
    add_text(board, 10.0, 36.9, "Eco1 FR4 0.4 #1 parts island", pcbnew.Eco1_User, 0.5)
    add_text(board, 10.0, -7.0, "Eco1 FR4 0.4 #2 USB+pocket", pcbnew.Eco1_User, 0.5)
    add_text(board, 10.0, 15.4, "BEND R>=1.5 NO VIA/PART/STIFFENER", pcbnew.Dwgs_User, 0.6)
    add_text(board, 10.0, 16.4, "NO TAB FR4; STANDOFF CLAMP Q58", pcbnew.Dwgs_User, 0.6)
    add_filled_rect(board, 12.50, 12.00, 17.75, 18.60, pcbnew.Cmts_User)
    add_text(board, 15.1, 15.3, "NECK BEND", pcbnew.Cmts_User, 0.5)

    placed: dict[str, tuple[float, float, float]] = {}
    placed.update(NAMED)
    placed.update(TAB_PARTS)
    placed.update(FRONT_PASSIVES)

    park = back_sites_by_kind()["0402"] + back_sites_by_kind()["0603"] + back_sites_by_kind()["sot"]
    ei = 0
    for ref, meta in sorted(comps.items()):
        if ref in skip or ref in placed:
            continue
        if ei >= len(park):
            raise SystemExit(f"no site for {ref}")
        placed[ref] = park[ei]
        ei += 1

    for ref, (x, y, rot) in sorted(placed.items()):
        if ref in skip:
            continue
        meta = comps.get(ref)
        if meta is None:
            continue
        fp_id = meta["footprint"]
        print("place", ref, fp_id, x, y, rot)
        place_fp(board, ref, fp_id, x, y, rot, meta["value"], bool(meta.get("dnp")))

    assign_nets(board, nets)

    out = BOARD_DIR / "elicio-v2.kicad_pcb"
    board.SetFileName(str(out))
    board.Save(str(out))
    board = pcbnew.LoadBoard(str(out))

    kinds = back_sites_by_kind()
    cursors = {k: 0 for k in kinds}
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        if ref in DECOUPLE_BACK:
            x, y, rot = DECOUPLE_BACK[ref]
            fp.SetPosition(v2(x, y))
            fp.SetOrientationDegrees(rot)
            if not fp.IsFlipped():
                fp.Flip(fp.GetPosition(), False)
            continue
        if ref in FRONT_KEEP:
            continue
        kind = fp_kind(fp)
        i = cursors[kind]
        if i >= len(kinds[kind]):
            kind = "0402"
            i = cursors[kind]
        x, y, rot = kinds[kind][i]
        cursors[kind] = i + 1
        fp.SetPosition(v2(x, y))
        fp.SetOrientationDegrees(rot)
        if not fp.IsFlipped():
            fp.Flip(fp.GetPosition(), False)

    u1 = next(fp for fp in board.GetFootprints() if fp.GetReference() == "U1")
    hits = sum(1 for p in u1.Pads() if pad_in_rect(p, 2.25, 26.15, 6.05, 38.55))
    if hits > 8:
        u1.SetOrientationDegrees(270)
        print("U1 rotation 270, pads in RF box", hits, "->", sum(1 for p in u1.Pads() if pad_in_rect(p, 2.25, 26.15, 6.05, 38.55)))
    else:
        print("U1 rotation 90, pads in RF box", hits)

    assign_nets(board, nets)
    configure_rules(board)

    # GND planes on the island/pocket/USB only. Tabs stay contact-only (1.0 mm isolation).
    gnd = ensure_net(board, "GND")
    add_copper_zone(board, "GND_F", gnd, island_outline(), pcbnew.F_Cu)
    add_copper_zone(board, "GND_B", gnd, island_outline(), pcbnew.B_Cu)

    print("maze route...")
    failed = maze_route(board, outline_points())
    print("route failed nets", failed)

    gnd = ensure_net(board, "GND")
    for u in (3.20, 7.60, 9.60, 11.60, 13.60, 16.20):
        for s in (19.20, 21.40, 23.60, 25.50, 27.20, 29.40, 31.60, 34.00, 36.20):
            if 2.25 <= u <= 6.05 and 26.15 <= s <= 38.55:
                continue
            if 12.50 <= u <= 17.75 and 12.00 <= s <= 18.60:
                continue
            add_via(board, gnd, u, s)

    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())

    board.SetFileName(str(out))
    board.Save(str(out))
    hide_silk_in_file(out)
    board = pcbnew.LoadBoard(str(out))
    ntracks = len([t for t in board.GetTracks() if t.GetClass() in {"PCB_TRACK", "PCB_ARC"}])
    print("saved", out, "footprints", len(list(board.GetFootprints())), "tracks", ntracks)
    missing = []
    for fp in board.GetFootprints():
        for pad in fp.Pads():
            if pad.GetNetCode() == 0:
                missing.append(f"{fp.GetReference()}.{pad.GetNumber()}")
    print("pads without net", len(missing), missing[:20])


if __name__ == "__main__":
    build()
