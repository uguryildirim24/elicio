#!/usr/bin/env python3
"""Place elicio-v2 from packing §5c (no receptacle), sync nets, save.

WP12d. Packing (u, s) = PCB (x, y). Width 22 island. No maze unless --route-only.
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
    parse_placement_markdown,
    wants_back_copper,
)

ROOT = Path(__file__).resolve().parents[2]
BOARD_DIR = ROOT / "hardware" / "board"
KICAD_FP = Path("/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints")
LOCAL_FP = BOARD_DIR / "lib" / "elicio.pretty"
TABLE = BOARD_DIR / "packing_5c_norec.md"
V2_TABLE = BOARD_DIR / "packing_v2_flat.md"
CONTACT_ISLAND_CLEARANCE = 0.20
TAB_RULE_HALF = 3.20
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
NECK_FOLD_S0 = 14.40
TAB_STRIP = 2.5
TAB_CAP_R = 3.2
HOLES = ((13.45, 17.70), (17.95, 17.70))
SIG1_SITE = (5.90, 22.00)
SIG2_SITE = (10.40, 33.10)
REF_SITE = (8.50, 43.00)
P4_SITE = (0.75, 44.00)
P5_SITE = (21.25, 44.00)
# Neck-end fold strips (Q83): 2.5 mm at the island low-s edge.
SIG1_FOLD_U = SIG1_SITE[0]
SIG2_FOLD_U = SIG2_SITE[0]
# U1 process pose keep-out 12.4 × 3.8 at the high-s antenna end.
RF_BOX = (2.25, 33.80, 14.20, 37.60)
J4_KEEP = (14.25, 21.10, 18.25, 28.10)
SKIP_REFS = {"J1", "U5"}
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
    """tabs = three strips plus P1–P3 rings; tail_pads = P4 and P5."""
    hw = TAB_STRIP / 2
    strips = (
        (SIG1_FOLD_U - hw, NECK_FOLD_S0, SIG1_FOLD_U + hw, BOARD_S0),
        (SIG2_FOLD_U - hw, NECK_FOLD_S0, SIG2_FOLD_U + hw, BOARD_S0),
        (REF_SITE[0] - hw, BOARD_S1, REF_SITE[0] + hw, REF_SITE[1] + TAB_RULE_HALF),
    )
    for x0, y0, x1, y1 in strips:
        add_drc_rule_area(board, x0, y0, x1, y1, "tabs")
    for cx, cy in (SIG1_SITE, SIG2_SITE, REF_SITE):
        add_drc_rule_area(
            board, cx - TAB_RULE_HALF, cy - TAB_RULE_HALF, cx + TAB_RULE_HALF, cy + TAB_RULE_HALF, "tabs"
        )
    for cx, cy in (P4_SITE, P5_SITE):
        add_drc_rule_area(
            board,
            cx - TAB_RULE_HALF,
            cy - TAB_RULE_HALF,
            cx + TAB_RULE_HALF,
            cy + TAB_RULE_HALF,
            "tail_pads",
        )


def add_j4_both_side_keepout(board) -> None:
    """NPTH diameter plus board hole clearance; no B.Cu footprint or pad."""
    j4 = next((fp for fp in board.GetFootprints() if fp.GetReference() == "J4"), None)
    if j4 is None:
        return
    clearance = pcbnew.ToMM(board.GetDesignSettings().m_HoleClearance)
    bcu = pcbnew.LSET()
    bcu.AddLayer(pcbnew.B_Cu)
    for pad in j4.Pads():
        try:
            attr = pad.GetAttribute()
        except Exception:
            continue
        if attr != pcbnew.PAD_ATTRIB_NPTH:
            continue
        pos = pad.GetPosition()
        drill = pcbnew.ToMM(pad.GetDrillSize().x)
        radius = drill / 2.0 + clearance
        x = pcbnew.ToMM(pos.x)
        y = pcbnew.ToMM(pos.y)
        add_named_area(
            board,
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            "j4_holes",
            layers=bcu,
            allow_tracks=False,
            allow_vias=False,
            allow_fills=False,
            allow_pads=False,
            allow_footprints=False,
        )


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
    """Width-22 island, leftover/pocket, J3 hang, neck-end folds, three tail tabs."""
    hw = TAB_STRIP / 2
    pts = [
        (BOARD_U0, BOARD_S0),
        (SIG1_FOLD_U - hw, BOARD_S0),
        (SIG1_FOLD_U - hw, NECK_FOLD_S0),
        (SIG1_FOLD_U + hw, NECK_FOLD_S0),
        (SIG1_FOLD_U + hw, BOARD_S0),
        (SIG2_FOLD_U - hw, BOARD_S0),
        (SIG2_FOLD_U - hw, NECK_FOLD_S0),
        (SIG2_FOLD_U + hw, NECK_FOLD_S0),
        (SIG2_FOLD_U + hw, BOARD_S0),
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
    ]
    pts += tab_detour((BOARD_U1, BOARD_S1), P5_SITE)
    pts += [(REF_SITE[0], BOARD_S1)]
    pts += tab_detour((REF_SITE[0], BOARD_S1), REF_SITE)
    pts += [(BOARD_U0, BOARD_S1)]
    pts += tab_detour((BOARD_U0, BOARD_S1), P4_SITE)
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


def load_table() -> dict[str, PlacementRow]:
    path = V2_TABLE if V2_TABLE.exists() else TABLE
    text = path.read_text()
    if path == V2_TABLE or "pin table v2" in text.lower() or "folded" in text.lower():
        rows = parse_pin_table_v2(text)
    else:
        rows = parse_placement_markdown(text)
    print("placement table", path.name, "rows", len(rows))
    return {row.ref: row for row in rows}


def build() -> None:
    sch = BOARD_DIR / "elicio-v2.kicad_sch"
    net_path = Path("/tmp/wp12d/elicio-v2.net")
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
    skip |= SKIP_REFS

    out = BOARD_DIR / "elicio-v2.kicad_pcb"
    if out.exists():
        out.unlink()
    board = pcbnew.NewBoard(str(out))
    board.SetCopperLayerCount(2)
    configure_rules(board)
    add_segments(board, outline_points(), pcbnew.Edge_Cuts, close=True)

    add_keepout(board, RF_BOX[0], RF_BOX[1], RF_BOX[2], RF_BOX[3], "RF_NO_COPPER", allow_pads=True)
    add_keepout(board, J4_KEEP[0], J4_KEEP[1], J4_KEEP[2], J4_KEEP[3], "J4_KEEP", allow_pads=True, allow_tracks=True)
    add_q84_contact_areas(board)
    for (cx, cy), name in (
        (SIG1_SITE, "RING_SIG1_CLEAR"),
        (SIG2_SITE, "RING_SIG2_CLEAR"),
        (REF_SITE, "RING_REF_CLEAR"),
        (P4_SITE, "RING_P4_CLEAR"),
        (P5_SITE, "RING_P5_CLEAR"),
    ):
        add_keepout(board, cx - 3.2, cy - 3.2, cx + 3.2, cy + 3.2, name, allow_pads=True, allow_tracks=True)
    for i, (hx, hy) in enumerate(HOLES, 1):
        add_keepout(board, hx - 1.65, hy - 1.65, hx + 1.65, hy + 1.65, f"HOLE{i}_KEEP", allow_pads=True)

    add_filled_rect(board, BOARD_U0 + 0.30, BOARD_S0 + 0.30, BOARD_U1 - 0.30, BOARD_S1 - 0.30, pcbnew.Eco1_User)
    add_filled_rect(board, POCKET_U0 + 0.20, POCKET_S0 + 0.20, BOARD_U1 - 0.20, BOARD_S0 - 0.20, pcbnew.Eco1_User)
    add_text(board, 11.0, 36.9, "Eco1 FR4 0.4 #1 parts island", pcbnew.Eco1_User, 0.5)
    add_text(board, 16.0, 8.0, "Eco1 FR4 0.4 #2 leftover/pocket", pcbnew.Eco1_User, 0.5)
    add_text(board, 11.0, 15.2, "BEND R>=1.5 NO VIA/PART/STIFFENER", pcbnew.Dwgs_User, 0.6)
    add_text(board, 11.0, 15.9, "NECK-END FOLD Q83 SIG1 10.71 SIG2 21.81", pcbnew.Dwgs_User, 0.5)
    add_filled_rect(board, 4.65, NECK_FOLD_S0, 11.65, BOARD_S0, pcbnew.Cmts_User)
    add_text(board, 8.2, 15.2, "NECK BEND", pcbnew.Cmts_User, 0.5)

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

    u1 = next(fp for fp in board.GetFootprints() if fp.GetReference() == "U1")
    # Packing: module keep-out empty. The Raytac library zone blocks B.Cu parts.
    for zone in list(u1.Zones()):
        u1.Remove(zone)

    for i, (hx, hy) in enumerate(HOLES, 1):
        fp = load_fp("elicio:MountingHole_M2.5")
        fp.SetReference(f"H{i}")
        fp.SetValue("HOLE_D2.7")
        fp.SetPosition(v2(hx, hy))
        fp.SetExcludedFromBOM(True)
        fp.SetExcludedFromPosFiles(True)
        board.Add(fp)
        print("hole", f"H{i}", hx, hy)

    assign_nets(board, nets)
    shrink_j3_pads(board)
    configure_rules(board)
    add_j4_both_side_keepout(board)
    if V2_TABLE.exists():
        for zone in parse_j4_keepouts(V2_TABLE.read_text()):
            print("v2 keepout", zone.name, zone.u, zone.s, zone.radius, zone.layers)
    # No copper zones on the un-routed land: a GND pour on the island shorts
    # Contact rings (class 1.0 mm on the tabs). Zones return after a DRC-0 route.

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
    board.SetFileName(str(pcb_path))
    board.Save(str(pcb_path))
    ntracks = len([t for t in board.GetTracks() if t.GetClass() in {"PCB_TRACK", "PCB_ARC"}])
    nvias = len([t for t in board.GetTracks() if t.GetClass() == "PCB_VIA"])
    print("imported ses", ses_path, "ok", ok, "tracks", ntracks, "vias", nvias)


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--route-only" in args:
        rest = [a for a in args if a != "--route-only"]
        route_only(Path(rest[0]) if rest else None)
    elif "--export-dsn" in args:
        rest = [a for a in args if a != "--export-dsn"]
        dsn = Path(rest[0]) if rest else Path("/tmp/wp12d/elicio-v2.dsn")
        export_dsn(BOARD_DIR / "elicio-v2.kicad_pcb", dsn)
    elif "--import-ses" in args:
        rest = [a for a in args if a != "--import-ses"]
        ses = Path(rest[0]) if rest else Path("/tmp/wp12d/elicio-v2.ses")
        import_ses(BOARD_DIR / "elicio-v2.kicad_pcb", ses)
    else:
        build()
