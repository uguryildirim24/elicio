#!/usr/bin/env python3
"""Place elicio-v4 (W18 body, ISP1807) from the table below, sync nets, save.

docs/fab/board-v4-design.md §4-§6. The flex is drawn flat: PCB (x, y) =
packing (u, s) in mm. Folded shell sites are in the note's §10 tables.

Run with KiCad's python:
  build_v4.py                     build elicio-v4.kicad_pcb (unrouted, pre-routes locked)
  build_v4.py --export-dsn OUT    Specctra DSN for Freerouting
  build_v4.py --import-ses SES    import a Freerouting session, clamp widths
"""
from __future__ import annotations

import math
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import build_v2b as b2  # noqa: E402  (starts wx.App, imports pcbnew)
from build_v2b import (  # noqa: E402
    add_filled_circle,
    add_locked_path,
    add_named_area,
    add_segments,
    add_text,
    clamp_track_widths,
    ensure_net,
    hide_silk_in_file,
    load_fp,
    pad_center,
    parse_netlist,
    stamp_paste_pad_nets,
    strip_silk,
    tab_detour,
    v2,
)

import pcbnew  # noqa: E402

KICAD_FP = b2.KICAD_FP
b2.LIBS["Connector_Molex"] = KICAD_FP / "Connector_Molex.pretty"
b2.LIBS["Package_SON"] = KICAD_FP / "Package_SON.pretty"

BOARD = HERE / "elicio-v4"
NET_PATH = Path("/tmp/elicio-v4/elicio-v4.net")

# JLC 2-layer flex (design note §3): track/space 0.10, standard via 0.40/0.15
# (JLC flex page: hole >= 0.15, pad >= 0.35, 0.40 recommended). Contact class
# keeps v2's 0.15 track / 0.20 clearance.
FLEX_TRACK = 0.10
FLEX_CLEAR = 0.10
VIA_D = 0.40
VIA_DRILL = 0.15
CONTACT_TRACK = 0.15
CONTACT_CLEAR = 0.20
CONTACT_NETS = ("SIG1", "SIG2", "REF")
CHARGE_TRACK = 0.20
TAB_RULE_HALF = 3.50  # Q84/Q88 7 x 7 zones

# Island (design note §5.1). Cavity u 1.50-16.50 at W 18: everything east of
# U1 sits 1.0 further out than the W17 draft (§1.4 says why W17 was dropped).
BODY_W = 18.0
DW = BODY_W - 17.0
U0, U1_EDGE = 2.25, 14.75 + DW
S0, S1 = 16.00, 37.60
# P4/P5 joint: 90° fold at R 1.1 from u 15.09; relief notch s 16.0-19.6.
BEND_U0, BEND_U1 = 14.090 + DW, 15.904 + DW
JOINT_S0, JOINT_S1 = 16.30, 19.30
NOTCH_S1 = 19.60
PLATE_U0, PLATE_U1 = 12.914 + DW, 18.114 + DW
PLATE_S0, PLATE_S1 = 1.75, 14.85
P4_FLAT = (15.514 + DW, 4.35)
P5_FLAT = (15.514 + DW, 12.10)
# SIG/REF strips: v2's Q83 fold (180° at R 1.5 at the neck), same flat rings.
STRIP_W = 2.50
CAP_R = 3.20
SIG1_ATTACH, SIG1_SITE = (5.90, S0), (5.90, 5.29)
SIG2_ATTACH, SIG2_SITE = (10.40, S0), (10.40, -5.81)
REF_ATTACH, REF_SITE = (8.50, S1), (8.50, 43.00)
# J3 break-off tab (bench header, Contact nets). Cut before closing.
J3_NECK_S0, J3_NECK_S1 = 19.90, 22.40
J3_CUT_U = 15.20 + DW
J3_TAB_U0, J3_TAB_U1 = 18.60 + DW, 31.40 + DW
J3_TAB_S0, J3_TAB_S1 = 16.55, 25.75
J3_PIN1 = (20.35 + DW, 18.61)
# Contact corridor (design note §5.4), Contact class 0.15 / 0.20. The J3
# branches of SIG1/SIG2 run on F along the -s and +u edges, so the charge
# nets can cross the joint on B and the charger sits on B (no net boxed in).
SIG1_CORR_S = 16.40
SIG1_VIA = (6.75, 16.60)
SIG1_F_S = 17.05
SIG2_VIA = (10.40, 16.50)
SIG1_CORR_U = 13.35 + DW
SIG2_CORR_U = 13.70 + DW
REF_CORR_U = 14.35 + DW
# J3 is a symmetric 1 x 3 header: pin 1 (-s end) is REF, pin 3 is SIG1, so the
# three branches reach it without crossing on one layer (REF on B).
J3_S2_S, J3_S1_S, J3_REF_S = 20.30, 20.65, 21.20
J3_SIG1_U = 19.00 + DW
J3_SIG2_U = 19.60 + DW
J3_REF_U = 19.05 + DW
# Charge nets cross the joint on B: GND north, VBUS south (VBUS goes F -> B
# on the flap, clear of the bend and 1.0 mm clear of GND inside P5's zone).
VBUS_FLAP_VIA = (17.40 + DW, 17.00)
P5_ZONE_EXIT_S = P5_FLAT[1] + TAB_RULE_HALF + 0.15
CHG_GND_S, CHG_VBUS_S = 16.90, 18.40
# Test header J4 and the reset line (design note §4.3).
VDD_VIA = (7.60, 36.70)
J4_GND_VIA = (10.63, 36.70)
NRST_S = 37.25
NRST_E_U = 14.95
# ISP1807 (design note §4.2): u = 10.45 - Y, s = MOD_S0 + X; KiCad rot 270.
MOD_S0 = 25.05
U1_CENTRE = (6.45, MOD_S0 + 4.0)
RF_BAND = (U0, 21.80, 6.45, S1)
# Landings (standoff tops) and lid posts (design note §5.3).
P1_LAND = (5.90, 22.00)
P2_LAND = (10.40, 33.10)
LAND_R = 3.20
POST_P1 = (5.90, 23.00)
POST_P2 = (9.40, 32.10)
POST_KEEP_R = 1.30
# B-side FR4 0.2 under U1, the P2 landing and J4 (one stiffener).
STIFF_U1_B = [
    (2.45, MOD_S0), (10.70, MOD_S0), (10.70, 29.90), (13.80 + DW, 29.90),
    (13.80 + DW, 37.30), (6.45, 37.30), (6.45, MOD_S0 + 8.0), (2.45, MOD_S0 + 8.0),
]

# ref -> (side, u, s, rot). Top rot is KiCad's; bottom parts are set to rot
# then flipped top-bottom about their centre (build_v2b.apply_placement_row).
PLACE: dict[str, tuple[str, float, float, float]] = {
    # Fixed: module, battery header, test header, bench header, rings.
    "U1": ("top", *U1_CENTRE, 270),
    "J2": ("top", 5.45, 18.90, 270),
    "J4": ("top", 10.00, 35.40, 0),
    "J3": ("top", *J3_PIN1, 0),
    "P1": ("top", *SIG1_SITE, 0),
    "P2": ("top", *SIG2_SITE, 0),
    "P3": ("top", *REF_SITE, 0),
    "P4": ("bottom", *P4_FLAT, 0),
    "P5": ("bottom", *P5_FLAT, 0),
    # F: AFE, reset switch, the AFE's west-side decoupling and RESET pull-down.
    "U2": ("top", 11.85, 22.08, 270),
    "SW1": ("top", 14.45, 31.10, 180),
    "C6": ("top", 7.75, 22.66, 90),
    "C7": ("top", 8.78, 22.66, 90),
    "R23": ("top", 7.95, 24.10, 180),
    # F above U2 (south of the SIG corridors): AFE references, TS/PRETERM pulls.
    "C9": ("top", 9.10, 18.45, 90),
    "C10": ("top", 10.20, 18.60, 90),
    "R12": ("top", 12.60, 18.15, 0),
    "R13": ("top", 12.60, 18.95, 0),
    # F corner above SW1: CS/DRDY series, pad-23 decoupling, charge LED.
    "R7": ("top", 11.14, 25.50, 90),
    "R27": ("top", 12.45, 25.50, 90),
    "C15": ("top", 13.60, 25.15, 0),
    "D2": ("top", 14.65, 26.10, 0),
    "R22": ("top", 14.60, 27.02, 180),
    "Q4": ("top", 14.60, 28.00, 0),
    "R28": ("top", 13.35, 27.70, 90),
    # F between U1 and SW1: SPI series resistors in U2's pad order.
    "R6": ("top", 11.40, 29.63, 90),
    "R5": ("top", 11.40, 31.12, 90),
    "R8": ("top", 11.40, 32.61, 90),
    # B, -s edge: +VDD LDO, Contact resistors at the strip roots, VBAT bulk.
    "U5": ("bottom", 3.30, 17.10, 0),
    "C16": ("bottom", 4.70, 17.15, 90),
    "C12": ("bottom", 3.10, 18.30, 0),
    "C13": ("bottom", 4.60, 18.30, 0),
    "R1": ("bottom", 5.90, 17.30, 270),
    "R2": ("bottom", 9.39, 17.25, 0),
    "C4": ("bottom", 7.25, 17.45, 0),
    # B, joint corner: charger (both charge nets arrive on B), ISET parts, TVS.
    "U3": ("bottom", 13.90, 17.75, 90),
    "R11": ("bottom", 12.00, 16.75, 0),
    "C2": ("bottom", 11.95, 17.55, 0),
    "R25": ("bottom", 11.95, 18.35, 0),
    "C3": ("bottom", 14.40, 19.95, 90),
    "D1": ("bottom", 12.60, 19.70, 0),
    # B under U2: AFE supply switch, LDO, bulk, RLD network.
    "R15": ("bottom", 9.95, 19.95, 0),
    "Q3": ("bottom", 9.95, 20.90, 0),
    "R14": ("bottom", 9.95, 21.85, 0),
    "Q1": ("bottom", 9.95, 22.80, 0),
    "C5": ("bottom", 9.95, 23.75, 0),
    "R24": ("bottom", 9.40, 24.65, 0),
    "U4": ("bottom", 11.65, 21.25, 0),
    "C8": ("bottom", 11.65, 22.55, 0),
    "C14": ("bottom", 11.65, 23.60, 0),
    "C11": ("bottom", 11.65, 24.60, 0),
    "R4": ("bottom", 13.30, 22.15, 90),
    "C1": ("bottom", 13.30, 23.65, 90),
    # B pocket right of the stiffener: REF resistor, dividers, charge interlock.
    "R3": ("bottom", 14.55, 25.60, 0),
    "R18": ("bottom", 11.45, 25.60, 0),
    "R19": ("bottom", 12.95, 26.52, 0),
    "R20": ("bottom", 11.45, 26.40, 0),
    "R21": ("bottom", 11.45, 27.20, 0),
    "Q2": ("bottom", 13.00, 27.60, 0),
    "R16": ("bottom", 14.40, 27.10, 90),
    "R17": ("bottom", 11.45, 28.00, 0),
}

RING_REFS = {"P1", "P2", "P3", "P4", "P5"}
NO_BOM = {"J4"} | RING_REFS


def outline_points() -> list[tuple[float, float]]:
    pts = [(U0, S0)]
    pts += tab_detour(SIG1_ATTACH, SIG1_SITE, STRIP_W / 2, CAP_R)
    pts += tab_detour(SIG2_ATTACH, SIG2_SITE, STRIP_W / 2, CAP_R)
    pts += [
        (BEND_U0, S0),
        (BEND_U0, JOINT_S0),
        (BEND_U1, JOINT_S0),
        (BEND_U1, PLATE_S1),
        (PLATE_U0, PLATE_S1),
        (PLATE_U0, PLATE_S0),
        (PLATE_U1, PLATE_S0),
        (PLATE_U1, JOINT_S1),
        (BEND_U0, JOINT_S1),
        (BEND_U0, NOTCH_S1),
        (U1_EDGE, NOTCH_S1),
        (U1_EDGE, J3_NECK_S0),
        (J3_TAB_U0, J3_NECK_S0),
        (J3_TAB_U0, J3_TAB_S0),
        (J3_TAB_U1, J3_TAB_S0),
        (J3_TAB_U1, J3_TAB_S1),
        (J3_TAB_U0, J3_TAB_S1),
        (J3_TAB_U0, J3_NECK_S1),
        (U1_EDGE, J3_NECK_S1),
        (U1_EDGE, S1),
    ]
    pts += tab_detour(REF_ATTACH, REF_SITE, STRIP_W / 2, CAP_R)
    pts += [(U0, S1)]
    return pts


def circle_pts(cx: float, cy: float, r: float, n: int = 24) -> list[tuple[float, float]]:
    return [(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n)) for k in range(n)]


def lset(*layers):
    s = pcbnew.LSET()
    for layer in layers:
        s.AddLayer(layer)
    return s


def add_poly_area(board, pts, name, layers, *, tracks, vias, fills, pads, footprints) -> None:
    zone = pcbnew.ZONE(board)
    zone.SetIsRuleArea(True)
    zone.SetDoNotAllowTracks(not tracks)
    zone.SetDoNotAllowVias(not vias)
    zone.SetDoNotAllowZoneFills(not fills)
    zone.SetDoNotAllowPads(not pads)
    zone.SetDoNotAllowFootprints(not footprints)
    zone.SetLayerSet(layers)
    zone.SetZoneName(name)
    poly = zone.Outline()
    poly.NewOutline()
    for x, y in pts:
        poly.Append(pcbnew.FromMM(x), pcbnew.FromMM(y))
    board.Add(zone)


def add_filled_poly(board, pts, layer) -> None:
    s = pcbnew.PCB_SHAPE(board)
    s.SetShape(pcbnew.SHAPE_T_POLY)
    s.SetFilled(True)
    s.SetLayer(layer)
    s.SetPolyPoints([v2(x, y) for x, y in pts])
    s.SetWidth(pcbnew.FromMM(0.05))
    board.Add(s)


def add_rule_areas(board) -> None:
    all_cu = pcbnew.LSET.AllCuMask()
    # ISP1807 §4.3 keep-out: no copper on any layer except the module's own
    # mechanical pads. Footprints allowed so U1's courtyard may overlap;
    # check_keepouts() refuses any other courtyard in it.
    x0, y0, x1, y1 = RF_BAND
    add_poly_area(board, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], "RF_BAND", all_cu,
                  tracks=False, vias=False, fills=False, pads=True, footprints=True)
    # Standoff landings: no vias (Q97 spirit), no B parts; B tracks allowed.
    for name, (cx, cy) in (("LAND_P1", P1_LAND), ("LAND_P2", P2_LAND)):
        add_poly_area(board, circle_pts(cx, cy, LAND_R), name, all_cu,
                      tracks=True, vias=False, fills=False, pads=True, footprints=True)
    # Q84/Q88 creepage areas at the flat lands (7 x 7).
    for cx, cy in (SIG1_SITE, SIG2_SITE, REF_SITE):
        b2.add_drc_rule_area(board, cx - TAB_RULE_HALF, cy - TAB_RULE_HALF, cx + TAB_RULE_HALF, cy + TAB_RULE_HALF, "tabs")
    for cx, cy in (P4_FLAT, P5_FLAT):
        b2.add_drc_rule_area(board, cx - TAB_RULE_HALF, cy - TAB_RULE_HALF, cx + TAB_RULE_HALF, cy + TAB_RULE_HALF, "tail_pads")
    # Strips carry one Contact net each: no vias, no fills (Q97).
    hw = STRIP_W / 2
    for name, (ax, ay), (rx, ry) in (
        ("strip_sig1", SIG1_ATTACH, SIG1_SITE),
        ("strip_sig2", SIG2_ATTACH, SIG2_SITE),
        ("strip_ref", REF_ATTACH, REF_SITE),
    ):
        lo, hi = min(ay, ry - CAP_R), max(ay, ry + CAP_R)
        if ry < ay:
            hi = ay
        else:
            lo = ay
        add_poly_area(board, [(ax - hw - 2.0, lo), (ax + hw + 2.0, lo), (ax + hw + 2.0, hi), (ax - hw - 2.0, hi)],
                      name, all_cu, tracks=True, vias=False, fills=False, pads=True, footprints=True)
    # Joint bend and the plate: no vias in the bend, no parts anywhere on it.
    add_poly_area(board, [(BEND_U0, JOINT_S0), (BEND_U1, JOINT_S0), (BEND_U1, JOINT_S1), (BEND_U0, JOINT_S1)],
                  "BEND_P45", all_cu, tracks=True, vias=False, fills=False, pads=False, footprints=False)
    # J3 neck: cut line crosses it; no vias.
    add_poly_area(board, [(U1_EDGE, J3_NECK_S0), (J3_TAB_U0, J3_NECK_S0), (J3_TAB_U0, J3_NECK_S1), (U1_EDGE, J3_NECK_S1)],
                  "J3_NECK", all_cu, tracks=True, vias=False, fills=False, pads=False, footprints=True)


def draw_stiffeners(board) -> None:
    """Eco2.User = FR4 0.2 on the B side; Eco1.User = FR4 0.2 on the F side."""
    add_filled_poly(board, STIFF_U1_B, pcbnew.Eco2_User)
    add_filled_circle(board, *P1_LAND, LAND_R, pcbnew.Eco2_User)
    # Rings P1-P3: FR4 0.2 on the side away from the contact face (v2 Q72).
    for cx, cy in (SIG1_SITE, SIG2_SITE, REF_SITE):
        add_filled_circle(board, cx, cy, CAP_R - 0.3, pcbnew.Eco1_User)
    # Wall plate: FR4 0.2 on F (the wall side after the fold), holes at P4/P5.
    add_filled_poly(board, [(PLATE_U0 + 0.3, PLATE_S0 + 0.3), (PLATE_U1 - 0.3, PLATE_S0 + 0.3),
                            (PLATE_U1 - 0.3, PLATE_S1 - 0.3), (PLATE_U0 + 0.3, PLATE_S1 - 0.3)], pcbnew.Eco1_User)
    add_text(board, 7.0, 36.8, "ECO2 = FR4 0.2 B SIDE", pcbnew.Eco2_User, 0.5)
    add_text(board, 15.5 + DW, 1.0, "ECO1 = FR4 0.2 F SIDE", pcbnew.Eco1_User, 0.5)


def add_fab_notes(board) -> None:
    for layer in (pcbnew.Dwgs_User, pcbnew.F_Fab):
        s = pcbnew.PCB_SHAPE(board)
        s.SetShape(pcbnew.SHAPE_T_SEGMENT)
        s.SetLayer(layer)
        s.SetStart(v2(J3_CUT_U, J3_NECK_S0 - 0.4))
        s.SetEnd(v2(J3_CUT_U, J3_NECK_S1 + 0.4))
        s.SetWidth(pcbnew.FromMM(0.12))
        board.Add(s)
    add_text(board, 24.0 + DW, 27.0, f"J3 BREAK-OFF: CUT u={J3_CUT_U:.2f}", pcbnew.Dwgs_User, 0.5)
    add_text(board, 15.0 + DW, 17.8, f"90 DEG FOLD R1.1 u {BEND_U0:.2f}-{BEND_U1:.2f}", pcbnew.Dwgs_User, 0.4)
    add_text(board, 8.2, 12.0, "SIG FOLDS 180 DEG R1.5 AT s=16", pcbnew.Dwgs_User, 0.4)
    add_text(board, 3.2, 30.0, "RF KEEP-OUT", pcbnew.Dwgs_User, 0.5)
    for (cx, cy), label in ((POST_P1, "LID POST P1"), (POST_P2, "LID POST P2")):
        add_segments(board, circle_pts(cx, cy, 1.0), pcbnew.Dwgs_User, 0.05, close=True)
        add_text(board, cx, cy - 1.6, label, pcbnew.Dwgs_User, 0.35)


def netlist_fields(path: Path) -> dict[str, dict[str, str]]:
    """LCSC and MPN per ref, so the board matches the schematic (DRC parity)."""
    text = path.read_text()
    out: dict[str, dict[str, str]] = {}
    for block in text[text.find("(components"): text.find("(libparts")].split("(comp\n")[1:]:
        rm = re.search(r'\(ref "([^"]+)"\)', block)
        if rm:
            found = re.findall(r'\(field\s+\(name "(LCSC|MPN|Datasheet)"\)(?: "([^"]*)")?\s*\)', block)
            out[rm.group(1)] = {k: v for k, v in found}
    return out


def place(board, comps: dict[str, dict], fields: dict[str, dict[str, str]]) -> None:
    for ref, (side, u, s, rot) in PLACE.items():
        if ref not in comps:
            raise SystemExit(f"{ref} in PLACE but not in the netlist")
        meta = comps[ref]
        fp = load_fp(meta["footprint"])
        lib, name = meta["footprint"].split(":", 1)
        fp.SetFPID(pcbnew.LIB_ID(lib, name))
        fp.SetReference(ref)
        fp.SetValue(meta["value"])
        for key, val in sorted(fields.get(ref, {}).items()):
            fp.SetField(key, val)
            fp.GetField(key).SetVisible(False)
        fp.SetPosition(v2(u, s))
        fp.SetOrientationDegrees(rot)
        if ref in NO_BOM:
            fp.SetExcludedFromBOM(True)
            fp.SetExcludedFromPosFiles(True)
        strip_silk(fp)
        for zone in list(fp.Zones()):
            fp.Remove(zone)
        board.Add(fp)
        if side == "bottom":
            fp.Flip(fp.GetPosition(), False)
    missing = sorted(r for r, c in comps.items() if r not in PLACE and ":" in c["footprint"] and not c["footprint"].startswith("power:"))
    if missing:
        raise SystemExit(f"netlist parts without a placement: {missing}")


def assign_nets(board, nets: dict[tuple[str, str], str]) -> None:
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        for pad in fp.Pads():
            num = pad.GetNumber()
            if pad.GetAttribute() == pcbnew.PAD_ATTRIB_NPTH:
                continue
            if num == "" or num == "MP":
                name = "GND" if ref == "J2" else None
                if name is None:
                    continue
            else:
                name = nets.get((ref, num))
            if name is None:
                continue
            pad.SetNet(ensure_net(board, name))


def configure_rules(board) -> None:
    ds = board.GetDesignSettings()
    ds.SetBoardThickness(pcbnew.FromMM(0.11))
    ds.m_TrackMinWidth = pcbnew.FromMM(FLEX_TRACK)
    ds.m_MinClearance = pcbnew.FromMM(FLEX_CLEAR)
    ds.m_ViasMinSize = pcbnew.FromMM(VIA_D)
    ds.m_ViasMinDrill = pcbnew.FromMM(VIA_DRILL)
    ds.m_ViasMinAnnularWidth = pcbnew.FromMM(0.12)
    ds.m_CopperEdgeClearance = pcbnew.FromMM(0.30)
    ds.m_HoleToHoleMin = pcbnew.FromMM(0.25)
    ds.m_MinThroughDrill = pcbnew.FromMM(VIA_DRILL)
    ds.m_HoleClearance = pcbnew.FromMM(0.20)
    ns = ds.m_NetSettings
    default = ns.GetDefaultNetclass()
    default.SetTrackWidth(pcbnew.FromMM(FLEX_TRACK))
    default.SetClearance(pcbnew.FromMM(FLEX_CLEAR))
    default.SetViaDiameter(pcbnew.FromMM(VIA_D))
    default.SetViaDrill(pcbnew.FromMM(VIA_DRILL))
    contact = ns.GetNetClassByName("Contact")
    if contact is not None and contact.GetName() == "Contact":
        contact.SetTrackWidth(pcbnew.FromMM(CONTACT_TRACK))
        contact.SetClearance(pcbnew.FromMM(CONTACT_CLEAR))
        contact.SetViaDiameter(pcbnew.FromMM(VIA_D))
        contact.SetViaDrill(pcbnew.FromMM(VIA_DRILL))
        for name in CONTACT_NETS:
            net = board.FindNet(name)
            if net is not None:
                net.SetNetClass(contact)


def zone_exit(site: tuple[float, float], direction: int) -> tuple[float, float]:
    """Point on the strip axis just outside a land's 7 x 7 zone, toward the island."""
    return (site[0], site[1] + direction * (TAB_RULE_HALF + 0.10))


def add_locked_via(board, pos: tuple[float, float], net) -> None:
    via = pcbnew.PCB_VIA(board)
    via.SetPosition(v2(*pos))
    via.SetWidth(pcbnew.FromMM(VIA_D))
    via.SetDrill(pcbnew.FromMM(VIA_DRILL))
    via.SetNet(net)
    via.SetLocked(True)
    board.Add(via)


def pre_routes(board) -> None:
    """Locked: rings along the strips to R1-R3, the J3 branches (§5.4), the
    P4/P5 charge runs, U1 pad 13 (nRESET) out of the pad field and round J4
    to J4.6 and SW1, +VDD into U1.26 and J4.1, and J4's GND via (§4.3)."""
    bcu, fcu = pcbnew.B_Cu, pcbnew.F_Cu
    sig1, sig2, ref = (ensure_net(board, n) for n in CONTACT_NETS)
    # Every strip run breaks where it leaves its land's 7 x 7 zone, so the Q84
    # 1.0 mm rule covers the land segment only (Q88: strips use Contact 0.20).
    # SIG1: strip on B to R1; its J3 branch goes to F by the strip root and
    # runs east inside SIG2's branch, then down the +u edge.
    r1 = pad_center(board, "R1", "1")
    add_locked_path(board, [pad_center(board, "P1", "1"), zone_exit(SIG1_SITE, +1), (SIG1_SITE[0], SIG1_CORR_S), r1],
                    sig1, bcu, CONTACT_TRACK)
    add_locked_path(board, [(SIG1_SITE[0], SIG1_CORR_S), SIG1_VIA], sig1, bcu, CONTACT_TRACK)
    add_locked_via(board, SIG1_VIA, sig1)
    j3 = {net: pad_center(board, "J3", n) for n, net in (("1", "REF"), ("2", "SIG2"), ("3", "SIG1"))}
    add_locked_path(board, [SIG1_VIA, (SIG1_VIA[0] + 0.45, SIG1_F_S), (SIG1_CORR_U, SIG1_F_S), (SIG1_CORR_U, J3_S1_S),
                            (J3_SIG1_U, J3_S1_S), (J3_SIG1_U, j3["SIG1"][1]), j3["SIG1"]], sig1, fcu, CONTACT_TRACK)
    # SIG2: strip on F (P2 is plated) to its via; R2 on B, J3 branch on F.
    add_locked_path(board, [pad_center(board, "P2", "1"), zone_exit(SIG2_SITE, +1), SIG2_VIA], sig2, fcu, CONTACT_TRACK)
    add_locked_via(board, SIG2_VIA, sig2)
    add_locked_path(board, [SIG2_VIA, pad_center(board, "R2", "1")], sig2, bcu, CONTACT_TRACK)
    add_locked_path(board, [SIG2_VIA, (SIG2_CORR_U, SIG2_VIA[1]), (SIG2_CORR_U, J3_S2_S), (J3_SIG2_U, J3_S2_S),
                            (J3_SIG2_U, j3["SIG2"][1]), j3["SIG2"]], sig2, fcu, CONTACT_TRACK)
    # REF: strip on B, along the +s edge and up the +u edge on B.
    r3 = pad_center(board, "R3", "1")
    add_locked_path(board, [pad_center(board, "P3", "1"), zone_exit(REF_SITE, -1), (REF_ATTACH[0], 37.20), (REF_CORR_U, 37.20),
                            (REF_CORR_U, J3_REF_S), (J3_REF_U, J3_REF_S), (J3_REF_U, j3["REF"][1]), j3["REF"]],
                    ref, bcu, CONTACT_TRACK)
    add_locked_path(board, [(REF_CORR_U, r3[1]), r3], ref, bcu, CONTACT_TRACK)

    # Charge: both nets cross the joint on B. P4 (VBUS) goes to F in its own
    # 7 x 7 zone, passes P5 on F (P5 has no F copper), and returns to B on the
    # flap; P5 (GND) stays on B. The rest of GND is the B pour (§9).
    gnd, vbus = ensure_net(board, "GND"), ensure_net(board, "VBUS")
    p4, p5 = fp_pos(board, "P4"), fp_pos(board, "P5")
    ring_edge = 2.3
    gnd_u = 16.95 + DW
    # Split where GND leaves P5's zone so the 1.0 mm rule covers the zone segment only.
    add_locked_path(board, [(p5[0] + ring_edge - 0.4, p5[1]), (gnd_u, p5[1] + 1.2), (gnd_u, P5_ZONE_EXIT_S)],
                    gnd, bcu, CHARGE_TRACK)
    add_locked_path(board, [(gnd_u, P5_ZONE_EXIT_S), (gnd_u, CHG_GND_S), (BEND_U0 - 0.25, CHG_GND_S)],
                    gnd, bcu, CHARGE_TRACK)
    via_s = p4[1] + ring_edge + 0.9
    add_locked_path(board, [(p4[0], p4[1] + ring_edge - 0.4), (p4[0], via_s)], vbus, bcu, CHARGE_TRACK)
    add_locked_via(board, (p4[0], via_s), vbus)
    vbus_u = VBUS_FLAP_VIA[0]
    # Split where VBUS leaves P5's zone so only the zone segment carries the 1.0 mm rule.
    add_locked_path(board, [(p4[0], via_s), (vbus_u, via_s + 1.0), (vbus_u, P5_ZONE_EXIT_S)], vbus, fcu, CHARGE_TRACK)
    add_locked_path(board, [(vbus_u, P5_ZONE_EXIT_S), VBUS_FLAP_VIA], vbus, fcu, CHARGE_TRACK)
    add_locked_via(board, VBUS_FLAP_VIA, vbus)
    a2 = pad_center(board, "U3", "A2")
    add_locked_path(board, [VBUS_FLAP_VIA, (vbus_u, CHG_VBUS_S), (a2[0] + 0.35, CHG_VBUS_S), (a2[0] + 0.35, a2[1]), a2],
                    vbus, bcu, CHARGE_TRACK)

    # nRESET: pad 13 out of the module's +s edge between pads 25 and 26, then
    # west of J4 and along the +s edge (J4's +VDD/SWD fan-out sits between),
    # up the +u side to J4.6 (between J4's two +u holes) and SW1.1.
    nrst = ensure_net(board, "nRESET")
    p13 = pad_center(board, "U1", "13")
    s0 = MOD_S0

    def mod(x, y):
        return (10.45 - y, s0 + x)

    nr_out = mod(8.35, 3.05)
    add_locked_path(board, [p13, mod(3.025, 2.7625), mod(6.80, 2.7625), mod(6.80, 3.05), nr_out,
                            (6.70, nr_out[1] + 0.70), (6.70, NRST_S - 0.35), (7.05, NRST_S), (NRST_E_U - 0.35, NRST_S),
                            (NRST_E_U, NRST_S - 0.35), (NRST_E_U, 35.40), (12.00, 35.40), pad_center(board, "J4", "6")],
                    nrst, fcu, FLEX_TRACK)
    sw1 = pad_center(board, "SW1", "1")
    add_locked_path(board, [(NRST_E_U, 35.40), (NRST_E_U, sw1[1] + 0.10)], nrst, fcu, FLEX_TRACK)
    # +VDD: U1.26 to J4.1 between J4's -u hole and J4.2, then to the via that
    # brings +VDD from U5 on B (outside the P2 landing's no-via circle).
    vdd = ensure_net(board, "+VDD")
    add_locked_path(board, [pad_center(board, "U1", "26"), (7.75, 33.55), (8.10, 35.00), pad_center(board, "J4", "1"), VDD_VIA],
                    vdd, fcu, FLEX_TRACK)
    add_locked_via(board, VDD_VIA, vdd)
    # J4 GND pads 3 and 5 to one via south of the landing circle.
    add_locked_path(board, [pad_center(board, "J4", "5"), pad_center(board, "J4", "3"), J4_GND_VIA], gnd, fcu, FLEX_TRACK)
    add_locked_via(board, J4_GND_VIA, gnd)
    # RF bridge OUT_ANT (20) - OUT_MOD (22), datasheet §4.
    rf = ensure_net(board, "RF_ANT")
    add_locked_path(board, [pad_center(board, "U1", "20"), pad_center(board, "U1", "22")], rf, fcu, 0.25)
    # Inner VSS 21/23/24 reach the edge pad 25 inside the module field.
    gnd_u1 = [pad_center(board, "U1", n) for n in ("21", "23", "25")]
    add_locked_path(board, gnd_u1, gnd, fcu, 0.12)
    add_locked_path(board, [pad_center(board, "U1", "24"), gnd_u1[-1]], gnd, fcu, 0.12)


def fp_pos(board, ref: str) -> tuple[float, float]:
    fp = next(f for f in board.GetFootprints() if f.GetReference() == ref)
    pos = fp.GetPosition()
    return pcbnew.ToMM(pos.x), pcbnew.ToMM(pos.y)


def check_keepouts(board) -> list[str]:
    """Courtyards that enter a no-part region, by side (DRC has no area test for these)."""
    probs: list[str] = []
    rf = pcbnew.BOX2I(v2(RF_BAND[0], RF_BAND[1]), pcbnew.VECTOR2I(pcbnew.FromMM(RF_BAND[2] - RF_BAND[0]), pcbnew.FromMM(RF_BAND[3] - RF_BAND[1])))
    stiff = pcbnew.SHAPE_LINE_CHAIN()
    for x, y in STIFF_U1_B:
        stiff.Append(pcbnew.FromMM(x), pcbnew.FromMM(y))
    stiff.SetClosed(True)
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        if ref in RING_REFS or ref == "J3":
            continue
        back = fp.IsFlipped()
        cy = fp.GetCourtyard(pcbnew.B_CrtYd if back else pcbnew.F_CrtYd)
        if cy.OutlineCount() == 0:
            probs.append(f"{ref}: no courtyard")
            continue
        bb = cy.BBox()
        x0, y0 = pcbnew.ToMM(bb.GetLeft()), pcbnew.ToMM(bb.GetTop())
        x1, y1 = pcbnew.ToMM(bb.GetRight()), pcbnew.ToMM(bb.GetBottom())
        if ref != "U1" and bb.Intersects(rf):
            probs.append(f"{ref}: courtyard in RF_BAND")
        # U1's body sits 0.20 inside the anterior edge; its 0.295 courtyard margin may overhang.
        m = 0.295 if ref == "U1" else 0.0
        if x0 + m < U0 - 0.01 or x1 - m > U1_EDGE + 0.01 or y0 + m < S0 - 0.01 or y1 - m > S1 + 0.01:
            probs.append(f"{ref}: courtyard off the island ({x0:.2f},{y0:.2f})-({x1:.2f},{y1:.2f})")
        if x1 > BEND_U0 and y0 < NOTCH_S1:
            probs.append(f"{ref}: courtyard in the joint notch")
        if back:
            for (cx, cy_), r in ((P1_LAND, LAND_R), (P2_LAND, LAND_R)):
                nx, ny = min(max(cx, x0), x1), min(max(cy_, y0), y1)
                if math.hypot(nx - cx, ny - cy_) < r:
                    probs.append(f"{ref}: B courtyard on landing at ({cx},{cy_})")
            box = pcbnew.SHAPE_LINE_CHAIN()
            for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)):
                box.Append(pcbnew.FromMM(x), pcbnew.FromMM(y))
            box.SetClosed(True)
            if stiff.Intersects(box) or stiff.PointInside(box.CPoint(0)) or box.PointInside(stiff.CPoint(0)):
                probs.append(f"{ref}: B courtyard on the U1/P2/J4 stiffener")
        else:
            for (cx, cy_) in (POST_P1,):
                nx, ny = min(max(cx, x0), x1), min(max(cy_, y0), y1)
                if math.hypot(nx - cx, ny - cy_) < POST_KEEP_R:
                    probs.append(f"{ref}: F courtyard under lid post P1")
    return probs


def build() -> None:
    sch = BOARD.with_suffix(".kicad_sch")
    NET_PATH.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["kicad-cli", "sch", "export", "netlist", "--format", "kicadsexpr", "-o", str(NET_PATH), str(sch)],
                   check=True, capture_output=True)
    comps, nets = parse_netlist(NET_PATH)
    comps = {r: c for r, c in comps.items() if c["footprint"] and not c["footprint"].startswith("power:")}
    out = BOARD.with_suffix(".kicad_pcb")
    if out.exists():
        out.unlink()
    board = pcbnew.NewBoard(str(out))
    board.SetCopperLayerCount(2)
    add_segments(board, outline_points(), pcbnew.Edge_Cuts, close=True)
    add_rule_areas(board)
    draw_stiffeners(board)
    add_fab_notes(board)
    place(board, comps, netlist_fields(NET_PATH))
    assign_nets(board, nets)
    configure_rules(board)
    pre_routes(board)
    configure_rules(board)
    board.SetFileName(str(out))
    board.Save(str(out))
    hide_silk_in_file(out)
    stamp_paste_pad_nets(out)
    board = pcbnew.LoadBoard(str(out))
    probs = check_keepouts(board)
    print("saved", out, "footprints", len(list(board.GetFootprints())))
    print("keep-out problems", len(probs))
    for p in probs:
        print("  ", p)
    nonet = [f"{fp.GetReference()}.{p.GetNumber()}" for fp in board.GetFootprints() for p in fp.Pads()
             if p.GetNumber() not in ("",) and p.GetAttribute() != pcbnew.PAD_ATTRIB_NPTH and p.GetNetCode() == 0]
    print("pads without net", len(nonet), nonet[:40])


def export_dsn(dsn: Path) -> None:
    board = pcbnew.LoadBoard(str(BOARD.with_suffix(".kicad_pcb")))
    dsn.parent.mkdir(parents=True, exist_ok=True)
    ok = pcbnew.ExportSpecctraDSN(board, str(dsn))
    print("dsn", dsn, "ok", ok)


def import_ses(ses: Path) -> None:
    pcb = BOARD.with_suffix(".kicad_pcb")
    board = pcbnew.LoadBoard(str(pcb))
    ok = pcbnew.ImportSpecctraSES(board, str(ses))
    configure_rules(board)
    clamp_track_widths(board)
    board.SetFileName(str(pcb))
    board.Save(str(pcb))
    tracks = [t for t in board.GetTracks() if t.GetClass() in {"PCB_TRACK", "PCB_ARC"}]
    vias = [t for t in board.GetTracks() if t.GetClass() == "PCB_VIA"]
    print("imported", ses, "ok", ok, "tracks", len(tracks), "vias", len(vias))


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--export-dsn":
        export_dsn(Path(args[1]))
    elif args and args[0] == "--import-ses":
        import_ses(Path(args[1]))
    else:
        build()
    # Leave without interpreter teardown: SWIG frees of board-held items at
    # exit can segfault KiCad's python, which pops a crash dialog on macOS.
    sys.stdout.flush()
    os._exit(0)
