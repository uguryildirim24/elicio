#!/usr/bin/env python3
"""Place elicio-v2 from pin table v2 (flat coordinates), sync nets, save.

WP12e. Packing (u, s) = PCB (x, y). Flat pattern with SIG/REF/CHARGE tabs.
"""
from __future__ import annotations

import math
import re
import subprocess
import sys
from pathlib import Path

import wx

_APP = wx.App(False)

import pcbnew  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from maze_route import maze_route  # noqa: E402
from placement_table import (  # noqa: E402
    PlacementRow,
    parse_j4_keepouts,
    parse_pin_table_v2,
    wants_back_copper,
)

ROOT = Path(__file__).resolve().parents[2]
BOARD_DIR = ROOT / "hardware" / "board"
KICAD_FP = Path("/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints")
LOCAL_FP = BOARD_DIR / "lib" / "elicio.pretty"
TABLE = BOARD_DIR / "packing_v2_flat.md"
V2_TABLE = TABLE
FLEX_TRACK = 0.10
FLEX_CLEAR = 0.10
FLEX_VIA_D = 0.55
FLEX_VIA_DRILL = 0.30
CONTACT_TRACK = 0.15
CONTACT_CLEAR = 0.20
CONTACT_NETS = ("SIG1", "SIG2", "REF")
TAB_RULE_HALF = 3.50
JAVA = Path("/opt/homebrew/opt/openjdk@25/bin/java")
FREEROUTE_JAR = Path.home() / ".local" / "opt" / "freerouting" / "freerouting-2.4.1.jar"

BOARD_U0, BOARD_U1 = 2.25, 19.75
BOARD_S0, BOARD_S1 = 16.00, 37.60
# Leftover / pocket island (SW1, U2, J2) and J3 hang, copper-to-edge 0.30.
POCKET_U0, POCKET_U1 = 12.00, 25.50
POCKET_S0, POCKET_S1 = 1.35, 16.00
J2_HANG_S0, J2_HANG_S1 = 7.40, 14.40
HANG_U1 = 33.20
HANG_S0, HANG_S1 = 16.00, 26.70
TAB_STRIP = 2.5
TAB_CAP_R = 3.2
HOLES = ((13.45, 17.70), (17.95, 17.70))
SIG1_ATTACH = (5.90, 16.00)
SIG2_ATTACH = (10.40, 16.00)
REF_ATTACH = (8.50, 37.60)
SIG1_SITE = (5.90, 5.29)
SIG2_SITE = (10.40, -5.81)
REF_SITE = (8.50, 43.00)
P4_SITE = (37.47, 2.80)
P5_SITE = (30.05, 5.80)
CHARGE_CX, CHARGE_CY = 33.02, 4.30
CHARGE_WU, CHARGE_WS = 14.50, 8.60
CHARGE_U0, CHARGE_U1 = CHARGE_CX - CHARGE_WU / 2, CHARGE_CX + CHARGE_WU / 2
CHARGE_S0, CHARGE_S1 = CHARGE_CY - CHARGE_WS / 2, CHARGE_CY + CHARGE_WS / 2
# U1 process pose keep-out 12.4 × 3.8 at the high-s antenna end.
RF_BOX = (2.25, 33.80, 14.20, 37.60)
J4_KEEP = (14.25, 21.10, 18.25, 28.10)
SKIP_REFS = {"J1", "U5", "R9", "R10"}  # Q81 no USB-C; Q95 DNP, not on the PCB.
# Pin table v2.1 (e4b857c): J4 holes from the KiCad footprint. R24 rot 90.
V21_POSE = {
    "R23": (18.32, 21.10, 0.0),
    "R24": (18.49, 22.57, 90.0),
    "R26": (14.21, 21.63, 90.0),
}
HOLE_REFS = {"H1", "H2"}
RING_REFS = {"P1", "P2", "P3", "P4", "P5"}

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


def add_filled_circle(board, cx: float, cy: float, radius: float, layer) -> None:
    s = pcbnew.PCB_SHAPE(board)
    s.SetShape(pcbnew.SHAPE_T_CIRCLE)
    s.SetFilled(True)
    s.SetLayer(layer)
    s.SetStart(v2(cx, cy))
    s.SetEnd(v2(cx + radius, cy))
    s.SetWidth(pcbnew.FromMM(0.05))
    board.Add(s)


# Q94. FR4 0.4 only where that face has no SMT lands. PI 0.1 on the thin
# B.Cu-only sliver east of J4 (FR4 0.4 cannot sit in 1.1 mm). Eco2 = FR4 0.2
# ring pieces (decision 72 / Q72). User.1 = PI 0.1.
STIFF_FR4_04 = (
    ("leftover_B", 12.20, 1.55, 19.55, 15.80),
    ("u1_west_B", 2.55, 20.20, 8.00, 25.70),
    ("u1_rf_B", 8.00, 29.50, 13.90, 37.30),
)
STIFF_PI_01 = (("east_j4_F", 18.35, 21.20, 19.45, 26.10),)
RING_FR4_02_R = TAB_CAP_R
STIFF_COUNT = len(STIFF_FR4_04) + len(STIFF_PI_01) + len(RING_REFS)


def clear_stiffener_drawings(board) -> int:
    n = 0
    for drawing in list(board.GetDrawings()):
        layer = drawing.GetLayer()
        if layer not in {pcbnew.Eco1_User, pcbnew.Eco2_User, pcbnew.User_1}:
            continue
        if drawing.GetClass() == "PCB_TEXT":
            blob = drawing.GetText().upper()
            if not any(k in blob for k in ("FR4", "PI 0.1", "STIFF", "RING")):
                continue
        board.Remove(drawing)
        n += 1
    return n


def draw_q94_stiffeners(board) -> int:
    """Redraw Q94 zones on the owned board. Does not touch copper."""
    clear_stiffener_drawings(board)
    for _name, x0, y0, x1, y1 in STIFF_FR4_04:
        add_filled_rect(board, x0, y0, x1, y1, pcbnew.Eco1_User)
    add_text(board, 16.0, 8.0, "Eco1 FR4 0.4 leftover B.Cu face", pcbnew.Eco1_User, 0.5)
    add_text(board, 5.2, 22.8, "Eco1 FR4 0.4 U1 west B.Cu", pcbnew.Eco1_User, 0.4)
    add_text(board, 10.8, 33.4, "Eco1 FR4 0.4 U1 RF B.Cu", pcbnew.Eco1_User, 0.4)
    for _name, x0, y0, x1, y1 in STIFF_PI_01:
        add_filled_rect(board, x0, y0, x1, y1, pcbnew.User_1)
    add_text(board, 18.9, 23.5, "User.1 PI 0.1 F.Cu", pcbnew.User_1, 0.35)
    for ref, (cx, cy) in (
        ("P1", SIG1_SITE),
        ("P2", SIG2_SITE),
        ("P3", REF_SITE),
        ("P4", P4_SITE),
        ("P5", P5_SITE),
    ):
        add_filled_circle(board, cx, cy, RING_FR4_02_R, pcbnew.Eco2_User)
        add_text(board, cx, cy, f"Eco2 FR4 0.2 {ref}", pcbnew.Eco2_User, 0.4)
    add_text(
        board,
        11.0,
        36.9,
        f"Q94 stiffeners {STIFF_COUNT} pcs (3xFR4 0.4 + 1xPI 0.1 + 5xFR4 0.2)",
        pcbnew.Eco1_User,
        0.4,
    )
    return STIFF_COUNT


def apply_u2_rsm_land(board) -> None:
    """ADS1292 RSM land 4219108/B: 0.40 pitch, 0.55 x 0.20 pads, C=3.85, EP 2.8."""
    u2 = next(fp for fp in board.GetFootprints() if fp.GetReference() == "U2")
    radial = 3.85 / 2.0
    pad_len, pad_w = 0.55, 0.20
    for pad in u2.Pads():
        num = pad.GetNumber()
        if not num or not num.isdigit() or num == "33":
            continue
        n = int(num)
        pos0 = pad.GetFPRelativePosition()
        x = pcbnew.ToMM(pos0.x)
        y = pcbnew.ToMM(pos0.y)
        if n <= 8:
            pad.SetFPRelativePosition(v2(-radial, y))
            pad.SetSize(pcbnew.VECTOR2I(pcbnew.FromMM(pad_len), pcbnew.FromMM(pad_w)))
        elif n <= 16:
            pad.SetFPRelativePosition(v2(x, radial))
            pad.SetSize(pcbnew.VECTOR2I(pcbnew.FromMM(pad_w), pcbnew.FromMM(pad_len)))
        elif n <= 24:
            pad.SetFPRelativePosition(v2(radial, y))
            pad.SetSize(pcbnew.VECTOR2I(pcbnew.FromMM(pad_len), pcbnew.FromMM(pad_w)))
        else:
            pad.SetFPRelativePosition(v2(x, -radial))
            pad.SetSize(pcbnew.VECTOR2I(pcbnew.FromMM(pad_w), pcbnew.FromMM(pad_len)))
    ep = next(p for p in u2.Pads() if p.GetNumber() == "33")
    ep.SetSize(pcbnew.VECTOR2I(pcbnew.FromMM(2.8), pcbnew.FromMM(2.8)))
    u2.SetFPID(pcbnew.LIB_ID("elicio", "Texas_RSM0032"))
    u2.SetValue("ADS1292IRSMT")


def remove_dnp_footprints(board, refs: set[str]) -> list[str]:
    gone: list[str] = []
    for fp in list(board.GetFootprints()):
        if fp.GetReference() in refs:
            board.Remove(fp)
            gone.append(fp.GetReference())
    return gone


def add_keepout(board, x0, y0, x1, y1, name, allow_pads: bool, allow_tracks: bool = False) -> None:
    add_named_area(
        board,
        x0,
        y0,
        x1,
        y1,
        name,
        layers=pcbnew.LSET.AllCuMask(),
        allow_tracks=allow_tracks,
        allow_vias=False,
        allow_fills=False,
        allow_pads=allow_pads,
        allow_footprints=True,
    )


def add_named_area(
    board,
    x0,
    y0,
    x1,
    y1,
    name,
    layers,
    allow_tracks: bool,
    allow_vias: bool,
    allow_fills: bool,
    allow_pads: bool,
    allow_footprints: bool,
) -> None:
    zone = pcbnew.ZONE(board)
    zone.SetIsRuleArea(True)
    zone.SetDoNotAllowTracks(not allow_tracks)
    zone.SetDoNotAllowVias(not allow_vias)
    zone.SetDoNotAllowZoneFills(not allow_fills)
    zone.SetDoNotAllowPads(not allow_pads)
    zone.SetDoNotAllowFootprints(not allow_footprints)
    zone.SetLayerSet(layers)
    zone.SetZoneName(name)
    poly = zone.Outline()
    poly.NewOutline()
    for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)):
        poly.Append(pcbnew.FromMM(x), pcbnew.FromMM(y))
    board.Add(zone)


def add_drc_rule_area(board, x0, y0, x1, y1, name) -> None:
    """Named area for custom DRC only. Does not keep copper out."""
    add_named_area(
        board,
        x0,
        y0,
        x1,
        y1,
        name,
        layers=pcbnew.LSET.AllCuMask(),
        allow_tracks=True,
        allow_vias=True,
        allow_fills=True,
        allow_pads=True,
        allow_footprints=True,
    )


def add_q84_contact_areas(board) -> None:
    """Q88: 1.0 mm creepage on each Ø5 land plus 1.0 mm (7 × 7 of §12)."""
    half = TAB_RULE_HALF
    for cx, cy in (SIG1_SITE, SIG2_SITE, REF_SITE):
        add_drc_rule_area(board, cx - half, cy - half, cx + half, cy + half, "tabs")
    for cx, cy in (P4_SITE, P5_SITE):
        add_drc_rule_area(board, cx - half, cy - half, cx + half, cy + half, "tail_pads")


def add_j4_both_side_keepout(board) -> None:
    """NPTH keep-out Ø1.39 on B.Cu at the real hole centres; J4 pads allowed."""
    keep_r = 1.39 / 2.0
    if TABLE.exists():
        parsed = parse_j4_keepouts(TABLE.read_text())
        if parsed:
            keep_r = parsed[0].radius
    j4 = next((fp for fp in board.GetFootprints() if fp.GetReference() == "J4"), None)
    if j4 is None:
        return
    bcu = pcbnew.LSET()
    bcu.AddLayer(pcbnew.B_Cu)
    n = 0
    for pad in j4.Pads():
        try:
            attr = pad.GetAttribute()
        except Exception:
            continue
        if attr != pcbnew.PAD_ATTRIB_NPTH:
            continue
        pos = pad.GetPosition()
        x = pcbnew.ToMM(pos.x)
        y = pcbnew.ToMM(pos.y)
        n += 1
        add_named_area(
            board,
            x - keep_r,
            y - keep_r,
            x + keep_r,
            y + keep_r,
            f"J4-NPTH{n}",
            layers=bcu,
            allow_tracks=False,
            allow_vias=False,
            allow_fills=False,
            allow_pads=True,
            allow_footprints=True,
        )
        print("j4 keepout", f"J4-NPTH{n}", round(x, 3), round(y, 3), "dia", round(2 * keep_r, 3))


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
    """Flat pattern: island, leftover/pocket, J3 hang, SIG strips, REF tab, CHARGE tab."""
    pts = [(BOARD_U0, BOARD_S0)]
    pts += tab_detour(SIG1_ATTACH, SIG1_SITE)
    pts += tab_detour(SIG2_ATTACH, SIG2_SITE)
    pts += [
        (POCKET_U0, BOARD_S0),
        (POCKET_U0, POCKET_S0),
        (20.40, POCKET_S0),
        (20.40, J2_HANG_S0),
        (CHARGE_U0, J2_HANG_S0),
        (CHARGE_U0, CHARGE_S0),
        (CHARGE_U1, CHARGE_S0),
        (CHARGE_U1, CHARGE_S1),
        (CHARGE_U0, CHARGE_S1),
        (CHARGE_U0, J2_HANG_S1),
        (BOARD_U1, J2_HANG_S1),
        (BOARD_U1, HANG_S0),
        (HANG_U1, HANG_S0),
        (HANG_U1, HANG_S1),
        (BOARD_U1, HANG_S1),
        (BOARD_U1, BOARD_S1),
    ]
    pts += tab_detour(REF_ATTACH, REF_SITE)
    pts += [(BOARD_U0, BOARD_S1)]
    return pts


def island_outline():
    """GND fill: island + leftover/pocket + J3 hang. Tabs stay contact-only."""
    return [
        (BOARD_U0, BOARD_S0),
        (POCKET_U0, BOARD_S0),
        (POCKET_U0, POCKET_S0),
        (20.40, POCKET_S0),
        (20.40, J2_HANG_S0),
        (POCKET_U1, J2_HANG_S0),
        (POCKET_U1, J2_HANG_S1),
        (BOARD_U1, J2_HANG_S1),
        (BOARD_U1, HANG_S0),
        (HANG_U1, HANG_S0),
        (HANG_U1, HANG_S1),
        (BOARD_U1, HANG_S1),
        (BOARD_U1, BOARD_S1),
        (BOARD_U0, BOARD_S1),
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
        comps[m.group(1)] = {"value": m.group(2), "footprint": m.group(3)}
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
    try:
        ref = fp.Reference()
        val = fp.Value()
        if hasattr(ref, "SetVisible"):
            ref.SetVisible(False)
            ref.SetLayer(pcbnew.F_Fab)
        if hasattr(val, "SetVisible"):
            val.SetVisible(False)
            val.SetLayer(pcbnew.B_Fab if fp.IsFlipped() else pcbnew.F_Fab)
    except Exception:
        pass
    doomed = []
    for gi in list(fp.GraphicalItems()):
        try:
            ly = gi.GetLayer()
        except Exception:
            continue
        if ly in (pcbnew.F_SilkS, pcbnew.B_SilkS):
            doomed.append(gi)
    for gi in doomed:
        try:
            fp.Remove(gi)
        except Exception:
            pass


def place_fp(board, ref: str, lib_id: str, x: float, y: float, rot: float, value: str, dnp: bool):
    if ref in RING_REFS:
        lib_id = "elicio:RING_PAD_D5_H2.7"
    fp = load_fp(lib_id)
    fp.SetReference(ref)
    fp.SetValue(value)
    fp.SetPosition(v2(x, y))
    fp.SetOrientationDegrees(rot)
    if dnp:
        fp.SetDNP(True)
    if ref in {"J4"} | RING_REFS or dnp:
        fp.SetExcludedFromBOM(True)
        if ref in RING_REFS | {"J4"}:
            fp.SetExcludedFromPosFiles(True)
    board.Add(fp)
    return fp


def apply_placement_row(fp, row: PlacementRow) -> None:
    """Pin a footprint from a packing row. Bottom-side uses KiCad Flip.

    Set (u, s) and rotation first. Then Flip about that point with
    ``aFlipLeftRight=False`` so a ``side=bottom`` row lands on B.Cu without a
    left-right courtyard mirror.
    """
    fp.SetPosition(v2(row.u, row.s))
    fp.SetOrientationDegrees(row.rot)
    if wants_back_copper(row) != bool(fp.IsFlipped()):
        fp.Flip(fp.GetPosition(), False)


def assign_nets(board, nets: dict[tuple[str, str], str]) -> None:
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        for pad in fp.Pads():
            num = pad.GetNumber()
            if num == "":
                try:
                    attr = pad.GetAttribute()
                except Exception:
                    attr = None
                if attr == pcbnew.PAD_ATTRIB_NPTH:
                    continue
                pad.SetNet(ensure_net(board, "GND"))
                continue
            name = nets.get((ref, num)) or nets.get((ref, num.upper())) or nets.get((ref, num.lower()))
            if name is None:
                if num.upper() in {"SH", "S1", "S2", "MP", "MOUNT", "A1", "B1", "A12", "B12"}:
                    name = "GND"
            if name is None:
                name = f"NC-{ref}-{num}"
            pad.SetNet(ensure_net(board, name))


def configure_rules(board) -> None:
    ds = board.GetDesignSettings()
    ds.SetBoardThickness(pcbnew.FromMM(0.11))
    ds.m_TrackMinWidth = pcbnew.FromMM(FLEX_TRACK)
    ds.m_MinClearance = pcbnew.FromMM(FLEX_CLEAR)
    ds.m_ViasMinSize = pcbnew.FromMM(FLEX_VIA_D)
    ds.m_ViasMinDrill = pcbnew.FromMM(FLEX_VIA_DRILL)
    ds.m_ViasMinAnnularWidth = pcbnew.FromMM(0.12)
    ds.m_CopperEdgeClearance = pcbnew.FromMM(0.30)
    ds.m_HoleToHoleMin = pcbnew.FromMM(0.25)
    ds.m_MinThroughDrill = pcbnew.FromMM(FLEX_VIA_DRILL)
    ds.m_HoleClearance = pcbnew.FromMM(0.20)
    if hasattr(ds, "m_SolderMaskMargin"):
        ds.m_SolderMaskMargin = pcbnew.FromMM(0.10)
    apply_flex_netclasses(board)


def apply_flex_netclasses(board) -> None:
    """JLC 2-layer flex 1 oz: track/space 0.10, via 0.55/0.30. Contact 0.15/0.20."""
    ns = board.GetDesignSettings().m_NetSettings
    default = ns.GetDefaultNetclass()
    default.SetTrackWidth(pcbnew.FromMM(FLEX_TRACK))
    default.SetClearance(pcbnew.FromMM(FLEX_CLEAR))
    default.SetViaDiameter(pcbnew.FromMM(FLEX_VIA_D))
    default.SetViaDrill(pcbnew.FromMM(FLEX_VIA_DRILL))
    contact = ns.GetNetClassByName("Contact")
    if contact is None:
        contact = default
    else:
        contact.SetTrackWidth(pcbnew.FromMM(CONTACT_TRACK))
        contact.SetClearance(pcbnew.FromMM(CONTACT_CLEAR))
        contact.SetViaDiameter(pcbnew.FromMM(FLEX_VIA_D))
        contact.SetViaDrill(pcbnew.FromMM(FLEX_VIA_DRILL))
    for name in CONTACT_NETS:
        net = board.FindNet(name)
        if net is not None and contact is not default:
            net.SetNetClass(contact)


def pad_center(board, ref: str, num: str) -> tuple[float, float]:
    fp = next(f for f in board.GetFootprints() if f.GetReference() == ref)
    for pad in fp.Pads():
        if pad.GetNumber() == num:
            p = pad.GetPosition()
            return pcbnew.ToMM(p.x), pcbnew.ToMM(p.y)
    raise KeyError(f"{ref}.{num}")


def add_locked_track(board, x0: float, y0: float, x1: float, y1: float, net, layer, width: float) -> None:
    if math.hypot(x1 - x0, y1 - y0) < 0.01:
        return
    t = pcbnew.PCB_TRACK(board)
    t.SetStart(v2(x0, y0))
    t.SetEnd(v2(x1, y1))
    t.SetWidth(pcbnew.FromMM(width))
    t.SetLayer(layer)
    t.SetNet(net)
    t.SetLocked(True)
    board.Add(t)


def add_locked_path(board, pts: list[tuple[float, float]], net, layer, width: float) -> None:
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        add_locked_track(board, x0, y0, x1, y1, net, layer, width)


def pre_route_tabs(board) -> None:
    """Locked Contact: ring → strip centre → island → R1–R3. Charge tab to first parts.

    Q88 7×7 ends at the land. A segment that only clips that box still carries
    1.0 mm for its whole length, so REF and GND split at the box edge. SIG2
    cannot enter at u=10.40 (D2 pad 2 sits on that centre line); it jogs on
    the coverlaid strip to u=11.27, then to 11.50 to pass C1 west of H1.
    VBUS stays on the CHARGE south edge: island VBUS to D1 crosses SIG1.
    """
    sig1 = ensure_net(board, "SIG1")
    sig2 = ensure_net(board, "SIG2")
    ref = ensure_net(board, "REF")
    vbus = ensure_net(board, "VBUS")
    gnd = ensure_net(board, "GND")
    fcu = pcbnew.F_Cu
    p1 = pad_center(board, "P1", "1")
    r1 = pad_center(board, "R1", "1")
    add_locked_path(
        board,
        [
            p1,
            (SIG1_ATTACH[0], 15.50),
            (5.38, 15.50),
            (5.38, 19.50),
            (r1[0], 19.50),
            r1,
        ],
        sig1,
        fcu,
        CONTACT_TRACK,
    )
    p2 = pad_center(board, "P2", "1")
    r2 = pad_center(board, "R2", "1")
    add_locked_path(
        board,
        [
            p2,
            (SIG2_ATTACH[0], 15.50),
            (11.27, 15.50),
            (11.27, 16.50),
            (11.50, 16.50),
            (11.50, 19.50),
            (13.50, 19.50),
            (13.50, 28.20),
            (16.40, 28.20),
            (16.40, r2[1]),
            r2,
        ],
        sig2,
        fcu,
        CONTACT_TRACK,
    )
    p3 = pad_center(board, "P3", "1")
    r3 = pad_center(board, "R3", "1")
    # 7×7 south edge is s=39.50. Leave it on a short stub so the island
    # run does not inherit 1.0 mm versus U1 pad 26.
    add_locked_path(board, [p3, (REF_ATTACH[0], 39.35)], ref, fcu, CONTACT_TRACK)
    add_locked_path(
        board,
        [
            (REF_ATTACH[0], 39.35),
            (REF_ATTACH[0], 37.20),
            (14.40, 37.20),
            (14.40, 33.20),
            (18.47, 33.20),
            (18.47, r3[1]),
            r3,
        ],
        ref,
        fcu,
        CONTACT_TRACK,
    )
    p4 = pad_center(board, "P4", "1")
    add_locked_path(
        board,
        [p4, (p4[0], 1.20), (CHARGE_U0 + 0.5, 1.20)],
        vbus,
        fcu,
        FLEX_TRACK,
    )
    p5 = pad_center(board, "P5", "1")
    j2g = pad_center(board, "J2", "2")
    p5_west = P5_SITE[0] - TAB_RULE_HALF
    add_locked_path(
        board,
        [p5, (p5[0], 8.20), (p5_west, 8.20), (p5_west, 7.80), (p5_west - 0.15, 7.80)],
        gnd,
        fcu,
        FLEX_TRACK,
    )
    add_locked_path(
        board,
        [(p5_west - 0.15, 7.80), (j2g[0], 7.80), j2g],
        gnd,
        fcu,
        FLEX_TRACK,
    )
    print("pre-route locked Contact ring-to-R and charge-tab traces")


def add_strip_other_net_keepouts(board) -> None:
    """Vias and fills stay off the strips. Locked Contact traces already sit there."""
    hw = TAB_STRIP / 2
    boxes = (
        (SIG1_SITE[0] - hw, min(SIG1_SITE[1], SIG1_ATTACH[1]) - TAB_CAP_R, SIG1_SITE[0] + hw, SIG1_ATTACH[1], "strip_sig1"),
        (SIG2_SITE[0] - hw, min(SIG2_SITE[1], SIG2_ATTACH[1]) - TAB_CAP_R, SIG2_SITE[0] + hw, SIG2_ATTACH[1], "strip_sig2"),
        (REF_SITE[0] - hw, REF_ATTACH[1], REF_SITE[0] + hw, REF_SITE[1] + TAB_CAP_R, "strip_ref"),
    )
    for x0, y0, x1, y1, name in boxes:
        add_named_area(
            board,
            x0,
            y0,
            x1,
            y1,
            name,
            layers=pcbnew.LSET.AllCuMask(),
            allow_tracks=True,
            allow_vias=False,
            allow_fills=False,
            allow_pads=True,
            allow_footprints=True,
        )


def clamp_track_widths(board) -> int:
    """SES import can write 0.075 mm necks. Floor is JLC 1 oz 0.10 mm."""
    n = 0
    floor = pcbnew.FromMM(FLEX_TRACK)
    for t in board.GetTracks():
        if t.GetClass() not in {"PCB_TRACK", "PCB_ARC"}:
            continue
        if t.GetWidth() < floor:
            t.SetWidth(floor)
            n += 1
    print("clamped tracks to", FLEX_TRACK, "mm:", n)
    return n


def foreign_tracks_in_strips(board) -> list[str]:
    """Other nets must not enter the SIG/REF strips or the CHARGE rectangle."""
    hits: list[str] = []
    regions = (
        ("SIG1", SIG1_SITE[0] - 1.25, min(SIG1_SITE[1], SIG1_ATTACH[1]) - 3.2, SIG1_SITE[0] + 1.25, SIG1_ATTACH[1], {"SIG1"}),
        ("SIG2", SIG2_SITE[0] - 1.25, min(SIG2_SITE[1], SIG2_ATTACH[1]) - 3.2, SIG2_SITE[0] + 1.25, SIG2_ATTACH[1], {"SIG2"}),
        ("REF", REF_SITE[0] - 1.25, REF_ATTACH[1], REF_SITE[0] + 1.25, REF_SITE[1] + 3.2, {"REF"}),
        ("CHARGE", CHARGE_U0, CHARGE_S0, CHARGE_U1, CHARGE_S1, {"VBUS", "GND"}),
    )
    for t in board.GetTracks():
        if t.GetClass() not in {"PCB_TRACK", "PCB_ARC"}:
            continue
        net = t.GetNetname()
        x = pcbnew.ToMM(t.GetX())
        y = pcbnew.ToMM(t.GetY())
        for name, x0, y0, x1, y1, allowed in regions:
            if x0 <= x <= x1 and y0 <= y <= y1 and net not in allowed:
                hits.append(f"{net} in {name} at ({x:.2f},{y:.2f})")
    return hits


def shrink_j3_pads(board) -> None:
    """Contact class 1.0 mm vs 2.54 mm pitch needs Ø1.5 pads (WP12d)."""
    for fp in board.GetFootprints():
        if fp.GetReference() != "J3":
            continue
        for pad in fp.Pads():
            pad.SetSize(pcbnew.VECTOR2I(pcbnew.FromMM(1.5), pcbnew.FromMM(1.5)))


def hide_silk_in_file(path: Path) -> None:
    text = path.read_text()
    text = text.replace('(layer "F.SilkS")', '(layer "F.Fab")')
    text = text.replace('(layer "B.SilkS")', '(layer "B.Fab")')
    path.write_text(text)


def stamp_paste_pad_nets(path: Path) -> None:
    """VQFN paste-only pads have no copper net; release.py counts missing (net )."""
    text = path.read_text()
    pattern = re.compile(r'(\(pad "[^"]*" (?:smd|thru_hole|connect)\b)(.*?)(\n\t\t\))', re.S)

    def repl(m: re.Match) -> str:
        head, body, tail = m.group(1), m.group(2), m.group(3)
        if "(net " in body:
            return m.group(0)
        return head + body + '\n\t\t\t(net 0 "")' + tail

    path.write_text(pattern.sub(repl, text))


def hole_xy(table: dict[str, PlacementRow], href: str, index: int) -> tuple[float, float]:
    if href in table:
        return table[href].u, table[href].s
    return HOLES[index]


def load_table() -> dict[str, PlacementRow]:
    text = TABLE.read_text()
    rows = parse_pin_table_v2(text)
    print("placement table", TABLE.name, "rows", len(rows))
    return {row.ref: row for row in rows}


def build() -> None:
    sch = BOARD_DIR / "elicio-v2.kicad_sch"
    net_path = Path("/tmp/wp12f/elicio-v2.net")
    net_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["kicad-cli", "sch", "export", "netlist", "--format", "kicadsexpr", "-o", str(net_path), str(sch)],
        check=True,
    )
    comps, nets = parse_netlist(net_path)
    table = load_table()
    print("comps", len(comps), "table", len(table))
    if "U1" not in comps:
        raise SystemExit(f"U1 missing from netlist parse, have {sorted(comps)[:20]}")
    if "J1" in comps or "U5" in comps:
        raise SystemExit("J1/U5 still in netlist; schematic Q81 is not applied")
    if "P4" not in comps or "P5" not in comps:
        raise SystemExit("P4/P5 missing from netlist")
    skip = {r for r, c in comps.items() if not c["footprint"] or ":" not in c["footprint"]}
    skip |= {r for r, c in comps.items() if c["footprint"].startswith("power:")}
    skip |= SKIP_REFS | HOLE_REFS

    out = BOARD_DIR / "elicio-v2.kicad_pcb"
    if out.exists():
        out.unlink()
    board = pcbnew.NewBoard(str(out))
    board.SetCopperLayerCount(2)
    configure_rules(board)
    add_segments(board, outline_points(), pcbnew.Edge_Cuts, close=True)

    add_keepout(board, RF_BOX[0], RF_BOX[1], RF_BOX[2], RF_BOX[3], "RF_NO_COPPER", allow_pads=True, allow_tracks=True)
    add_keepout(board, J4_KEEP[0], J4_KEEP[1], J4_KEEP[2], J4_KEEP[3], "J4_KEEP", allow_pads=True, allow_tracks=True)
    add_q84_contact_areas(board)
    for (cx, cy), name in (
        (SIG1_SITE, "RING_SIG1_CLEAR"),
        (SIG2_SITE, "RING_SIG2_CLEAR"),
        (REF_SITE, "RING_REF_CLEAR"),
        (P4_SITE, "RING_P4_CLEAR"),
        (P5_SITE, "RING_P5_CLEAR"),
    ):
        add_keepout(board, cx - TAB_RULE_HALF, cy - TAB_RULE_HALF, cx + TAB_RULE_HALF, cy + TAB_RULE_HALF, name, allow_pads=True, allow_tracks=True)
    for i, href in enumerate(("H1", "H2"), 1):
        hx, hy = hole_xy(table, href, i - 1)
        add_keepout(board, hx - 1.65, hy - 1.65, hx + 1.65, hy + 1.65, f"HOLE{i}_KEEP", allow_pads=True)

    draw_q94_stiffeners(board)
    add_text(board, 11.0, 15.2, "BEND R>=1.5 NO VIA/PART/STIFFENER", pcbnew.Dwgs_User, 0.6)
    add_text(board, 8.2, 10.6, "SIG1 STRIP FLAT 10.71", pcbnew.Cmts_User, 0.5)
    add_text(board, 13.5, 5.1, "SIG2 STRIP FLAT 21.81", pcbnew.Cmts_User, 0.5)
    add_text(board, 33.0, 4.3, "CHARGE TAB Q86", pcbnew.Cmts_User, 0.5)
    add_filled_rect(board, 4.65, 14.40, 11.65, BOARD_S0, pcbnew.Cmts_User)

    missing_table = sorted(ref for ref in table if ref not in comps and ref not in skip)
    if missing_table:
        raise SystemExit(f"table refs missing from netlist: {missing_table}")
    extra = sorted(ref for ref in comps if ref not in skip and ref not in table)
    if extra:
        print("netlist refs not in table (skipped):", extra)

    for ref, row in sorted(table.items()):
        if ref in skip:
            continue
        meta = comps[ref]
        fp_id = meta["footprint"]
        print("place", ref, fp_id, row.u, row.s, row.rot, row.side)
        fp = place_fp(board, ref, fp_id, row.u, row.s, row.rot, meta["value"], bool(meta.get("dnp")))
        apply_placement_row(fp, row)
        pose = V21_POSE.get(ref)
        if pose:
            u, s, rot = pose
            fp.SetPosition(v2(u, s))
            fp.SetOrientationDegrees(rot)
            print("v2.1 pose", ref, u, s, rot)

    u1 = next(fp for fp in board.GetFootprints() if fp.GetReference() == "U1")
    # Packing: module keep-out empty. The Raytac library zone blocks B.Cu parts.
    for zone in list(u1.Zones()):
        u1.Remove(zone)

    for i, href in enumerate(("H1", "H2"), 1):
        hx, hy = hole_xy(table, href, i - 1)
        fp = load_fp("elicio:MountingHole_M2.5")
        fp.SetReference(href)
        fp.SetValue("HOLE_D2.7")
        fp.SetPosition(v2(hx, hy))
        fp.SetExcludedFromBOM(True)
        fp.SetExcludedFromPosFiles(True)
        board.Add(fp)
        print("hole", href, hx, hy)

    assign_nets(board, nets)
    shrink_j3_pads(board)
    configure_rules(board)
    add_j4_both_side_keepout(board)
    add_strip_other_net_keepouts(board)
    if "--no-pre-route" not in sys.argv:
        pre_route_tabs(board)
    apply_flex_netclasses(board)
    # No copper zones on the un-routed land: a GND pour on the island shorts
    # Contact rings on the tabs. Zones return after a DRC-0 route.

    board.SetFileName(str(out))
    board.Save(str(out))
    hide_silk_in_file(out)
    stamp_paste_pad_nets(out)
    board = pcbnew.LoadBoard(str(out))
    ntracks = len([t for t in board.GetTracks() if t.GetClass() in {"PCB_TRACK", "PCB_ARC"}])
    print("saved", out, "footprints", len(list(board.GetFootprints())), "tracks", ntracks)
    missing = []
    for fp in board.GetFootprints():
        for pad in fp.Pads():
            if pad.GetNumber() != "" and pad.GetNetCode() == 0:
                missing.append(f"{fp.GetReference()}.{pad.GetNumber()}")
    print("pads without net", len(missing), missing[:20])
    flipped = [fp.GetReference() for fp in board.GetFootprints() if fp.IsFlipped()]
    print("flipped", sorted(flipped))


def route_only(pcb_path: Path | None = None) -> None:
    """Load an existing placement and add maze copper. Do not move footprints."""
    out = pcb_path or (BOARD_DIR / "elicio-v2.kicad_pcb")
    board = pcbnew.LoadBoard(str(out))
    n = 0
    for item in list(board.GetTracks()):
        board.Remove(item)
        n += 1
    print("stripped tracks", n, "file", out)
    failed = maze_route(board, outline_points())
    print("route failed nets", failed)
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())
    board.SetFileName(str(out))
    board.Save(str(out))
    ntracks = len([t for t in board.GetTracks() if t.GetClass() in {"PCB_TRACK", "PCB_ARC"}])
    print("saved", out, "tracks", ntracks, "failed", len(failed))


def export_dsn(pcb_path: Path, dsn_path: Path) -> None:
    board = pcbnew.LoadBoard(str(pcb_path))
    dsn_path.parent.mkdir(parents=True, exist_ok=True)
    ok = pcbnew.ExportSpecctraDSN(board, str(dsn_path))
    print("dsn", dsn_path, "ok", ok, "bytes", dsn_path.stat().st_size if dsn_path.exists() else 0)


def import_ses(pcb_path: Path, ses_path: Path) -> None:
    board = pcbnew.LoadBoard(str(pcb_path))
    ok = pcbnew.ImportSpecctraSES(board, str(ses_path))
    configure_rules(board)
    clamp_track_widths(board)
    apply_flex_netclasses(board)
    board.SetFileName(str(pcb_path))
    board.Save(str(pcb_path))
    ntracks = len([t for t in board.GetTracks() if t.GetClass() in {"PCB_TRACK", "PCB_ARC"}])
    nvias = len([t for t in board.GetTracks() if t.GetClass() == "PCB_VIA"])
    print("imported ses", ses_path, "ok", ok, "tracks", ntracks, "vias", nvias)
    foreign = foreign_tracks_in_strips(board)
    print("foreign tracks in strips", len(foreign), foreign[:8])


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--route-only" in args:
        rest = [a for a in args if a != "--route-only"]
        route_only(Path(rest[0]) if rest else None)
    elif "--export-dsn" in args:
        rest = [a for a in args if a not in {"--export-dsn", "--no-pre-route"}]
        dsn = Path(rest[0]) if rest else Path("/tmp/wp12f/elicio-v2.dsn")
        export_dsn(BOARD_DIR / "elicio-v2.kicad_pcb", dsn)
    elif "--import-ses" in args:
        rest = [a for a in args if a not in {"--import-ses", "--no-pre-route"}]
        ses = Path(rest[0]) if rest else Path("/tmp/wp12f/elicio-v2.ses")
        pcb = Path(rest[1]) if len(rest) > 1 else BOARD_DIR / "elicio-v2.kicad_pcb"
        import_ses(pcb, ses)
    elif "--apply-rules" in args:
        out = BOARD_DIR / "elicio-v2.kicad_pcb"
        board = pcbnew.LoadBoard(str(out))
        configure_rules(board)
        board.SetFileName(str(out))
        board.Save(str(out))
        print("applied rules", out, "via", FLEX_VIA_D, FLEX_VIA_DRILL)
    elif "--pre-route" in args:
        out = BOARD_DIR / "elicio-v2.kicad_pcb"
        board = pcbnew.LoadBoard(str(out))
        pre_route_tabs(board)
        apply_flex_netclasses(board)
        board.SetFileName(str(out))
        board.Save(str(out))
    else:
        build()
