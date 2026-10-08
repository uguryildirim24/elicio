"""WP11d layout v2c: edge rule both ways, two widths, two chords, two sides.

Loaded by placement_v2 at publish time. The 864-run table and §5b stay.
"""
from __future__ import annotations

import math
import re
import subprocess
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any

V2C_CHORD_AS_BUILT = 47.90
V2C_CHORD_M1 = 49.00
V2C_DRAW_DIR = Path(__file__).resolve().parents[2] / "docs" / "fab" / "cad" / "v2c"
# PATH_BODY_ARC + this ds → TOTAL_CHORD 49.00 at CREASE_BOW 3.0.
V2C_ARC_PLUS_M1 = 1.0883365029235392
V2C_WIDTHS = (20.0, 22.0)
V2C_CHORDS = (V2C_CHORD_AS_BUILT, V2C_CHORD_M1)
V2C_EDGES = ("process", "body")
V2C_SIDES = ("top", "two")
V2C_RECEPTACLE = (True, False)
V2C_WALL_MIN = 1.0
# Q81 addendum 2 / Q86: Ø5 charging pads cannot sit on the tail (loft s 45.5,
# REF_end_wall_slot 38.20–39.25, REF dome, screw well). Q90 moves them off the
# skin face into the posterior side wall. Largest pair on the tail is Ø2.1.
CHARGE_LOFT_S = 45.5
CHARGE_SLOT_S = (38.20, 39.25)
CHARGE_CELL_U1 = 11.90  # pack501012 as placed: u0 1.80, u1 11.90, s 1.50–14.50
CHARGE_CELL_S = (1.50, 14.50)
CHARGE_BAY_S = (1.50, 14.90)  # free bay beside the cell, floor to board
CHARGE_TAIL_MAX_D = 2.1
CHARGE_REF_DOME_R = 3.20  # Ø6.4 ring seat
CHARGE_SCREW_HEAD_R = 2.50  # ISO 7380 head ~Ø5 well
# Shell V2_CHARGE_pads: nylon between pads ≥ 3.0, edge-to-edge to REF/screw ≥ 2.0.
CHARGE_NYLON = 3.0
CHARGE_CLEAR = 2.0
CHARGE_SCREW_U = 16.50  # WP14f: well moved from 14.50 to clear the REF pocket
CHARGE_SCREW_S = 41.00
CHARGE_SCREW_LEN = "M2.5×8"
CHARGE_TAIL_BOSS_OD = 9.94
CHARGE_STANDOFF = 3.0  # interface II winner; underside = FLOOR_Y + TAB_T + this
CHARGE_WALL_AROUND = 1.5  # remaining wall around each through-wall seat (Q93)
CHARGE_HOLE_D = 2.7
CHARGE_HEAD_AXIS = "+u"
CHARGE_WALL_NAME = "posterior side wall"
# Hook-end hinge lip (shell-v2.md §2): not the posterior wall.
HINGE_LIP_U = (7.5, 14.5)
HINGE_LIP_S = (1.00, 1.48)
HINGE_LIP_Y = (7.25, 7.70)
# Rib slot / drop channel: unused after Q90. Leave them in the shell extras list.
CHARGE_RIB_S = (14.90, 15.70)
CHARGE_RIB_U = (11.90, 20.50)
CHARGE_RIB_H = 0.31
CHARGE_FLAT_EXTRA = 0.0  # tab leaves the pocket edge; no J2 hang to clear
J3_BREAK_NECK = 2.5  # Q91: break-off tab neck, cut before closing
J3_ASSEMBLY_STEP = (
    "Remove the J3 break-off tab after programming and before closing the shell"
)
# Q98: routing channels as packing constraints (WP12h named the millimetres).
DEFAULT_TRACK_W = 0.10
DEFAULT_CLEAR = 0.10
CONTACT_TRACK_W = 0.15
CONTACT_CLEAR = 0.20
VIA_PAD_D = 0.55  # board Default via 0.55/0.30
Q98_TRACKS = 3
Q98_GAP_WAS = 1.20  # keep-to-keep on pin table v2.1 (H1 13.45, H2 17.95, keep 3.30)
Q98_GAP_EXTRA = 0.12  # three Default tracks need 0.12 more than that gap
Q98_GAP_MARGIN = 0.10
Q98_CHANNEL = 0.6  # free on both sides around U2, U3, J4
SIG2_RUN_U = 13.50  # locked SIG2 Contact run (route.md §12)
SIG2_RUN_S = (19.50, 28.20)
Q98_HOLE_S = 17.70
Q98_H2_U = 17.95  # do not move H2 east: east neck is already 0.15 to the outline
EAST_0402_ROW = frozenset(
    {"R13", "R14", "R15", "R16", "R22", "R23", "R24", "R25", "R26"}
)
Q98_STACK_SKIP = frozenset({("U2", "SW1"), ("SW1", "U2")})
NOREC_SKIP_REFS = frozenset({"J1", "U5", "R9", "R10"})
CAVITY_EXTERIOR_REFS = frozenset({"J3"})  # break-off tab of the flat pattern
# WP12d pin table: these five sit inward so copper-to-edge is ≥ 0.30.
NUDGE_COPPER_REFS = ("D1", "C3", "C10", "C11", "C12")
COPPER_SKIP_REFS = {"J1", "J3", "P1", "P2", "P3", "P4", "P5"}

FOOTPRINT_H = {
    "C_0402_1005Metric": 0.50,
    "C_0603_1608Metric": 1.00,
    "R_0402_1005Metric": 0.40,
    "LED_0402_1005Metric": 0.40,
    "D_SOD-523": 0.70,
    "L_0603_1608Metric": 1.00,
    "SOT-23": 1.15,
    "SOT-23-5": 1.45,
    "SOT-23-6": 1.45,
    "Texas_YFP0006": 0.50,
    "VQFN-32-1EP_4x4mm_P0.4mm_EP2.8x2.8mm": 1.00,
    "Raytac_MDBT50Q": 2.30,
    "SW_Push_1P1T_XKB_TS-1187A": 1.60,
    "USB_C_Receptacle_HRO_TYPE-C-31-M-12": 3.20,
    "JST_SH_SM02B-SRSS-TB_1x02-1MP_P1.00mm_Horizontal": 2.90,
    "PinHeader_1x03_P2.54mm_Horizontal": 2.50,
    "Tag-Connect_TC2030-IDC-NL_2x03_P1.27mm_Vertical": 1.50,
    "RING_PAD_D5_H2.7": 0.31,
}


@dataclass
class LayoutV2c:
    edge: str
    width: float
    chord: float
    sides: str
    island: tuple[float, float, float, float]
    leftover: tuple[float, float, float, float]
    island_mm2: float
    leftover_mm2: float
    island_fill: float
    leftover_fill: float
    extra_u: float
    extra_s: float
    under_clear_mm: float
    placed: int
    missing: list[str]
    second_side: list[str]
    first_blocking: str
    parts: list[Any] = field(default_factory=list)
    rules: list[tuple[str, bool, str]] = field(default_factory=list)
    keepouts: list[tuple[str, float, float, float, float]] = field(default_factory=list)
    contacts_moved_mm: dict[str, float] = field(
        default_factory=lambda: {"SIG1": 0.0, "SIG2": 0.0, "REF": 0.0}
    )
    receptacle: bool = True
    bom_n: int = 66
    fold: str = "neck"
    wall_left: float = 0.65
    hole_sites: tuple[tuple[float, float], ...] = ()
    sig1_strip: float = 10.71
    sig2_strip: float = 21.81
    j4_npth: tuple[tuple[float, float], ...] = ()
    j3_cut_u: float = 0.0
    j3_neck_s: float = 0.0


_CACHE: dict[tuple, LayoutV2c] | None = None


def arc_plus_for_chord(v2: Any, chord: float) -> float:
    if abs(chord - V2C_CHORD_AS_BUILT) < 0.02:
        return 0.0
    return V2C_ARC_PLUS_M1


def v2c_geom(v2: Any, width: float, chord: float) -> tuple[Any, dict[str, Any]]:
    spec = v2.V2Spec("A", "pack501012", "series", width, 8.0, 0.0, "II", 3.0, 0.0)
    geom = dict(v2.body_geom(spec))
    ds = arc_plus_for_chord(v2, chord)
    if ds > 1e-12:
        P = v2._placement()
        c, _r = P.chord_from_arc_bow(v2.PATH_BODY_ARC + ds, v2.CREASE_BOW)
        bs0, bs1 = geom["board_s"]
        cs0, cs1 = geom["cavity_s"]
        geom["board_s"] = (bs0, bs1 + ds)
        geom["cavity_s"] = (cs0, cs1 + ds)
        geom["body_arc"] = v2.PATH_BODY_ARC + ds
        geom["total_chord"] = float(c)
        geom["m1_gate"] = float(c) + 3.0
    geom["arc_plus"] = ds
    geom["width"] = width
    return spec, geom


def under_board_clearance(v2: Any, geom: dict[str, Any]) -> dict[str, Any]:
    """Air under the island. The 501012 pack sits in the pocket, not under the island."""
    underside = geom["board_underside"]
    air = underside - v2.FLOOR_Y
    cell = v2.CELL["pack501012"]
    packed = cell["t"] + v2.FOAM
    pocket_s1 = v2.CAVITY_S0 + cell["l"] + 0.4
    return {
        "air_mm": air,
        "underside": underside,
        "floor": v2.FLOOR_Y,
        "ring": v2.TAB_T,
        "standoff": 3.0,
        "board": v2.BOARD_AT_PARTS,
        "cell_packed": packed,
        "pocket_s1": pocket_s1,
        "island_s0": geom["board_s"][0],
        "source": (
            f"floor {v2.FLOOR_Y:g} (packing); ring {v2.TAB_T:g} (Q72 PI {v2.FLEX:g} + FR4 "
            f"{v2.STIFFENER_TAB:g}); standoff 3.0 → underside {underside:.2f} "
            f"(packing-v2.md §5 / board-v2.md §11); board at parts {v2.BOARD_AT_PARTS:g}. "
            f"501012 pack {cell['l']:g}×{cell['w']:g}×{cell['t']:g} + foam {v2.FOAM:g} = {packed:g} "
            f"in the pocket (s {v2.CAVITY_S0:g}–{pocket_s1:.1f}); island s0 {geom['board_s'][0]:.2f} "
            f"is past the rib, so the cell is not under the island (Q69). Air {air:.2f} mm."
        ),
    }


def _body_xy(row: dict[str, Any]) -> tuple[float, float]:
    r5 = row.get("round5")
    if r5 is not None:
        return (r5[0], r5[1])
    return (row["cr_w"], row["cr_h"])


def _height(row: dict[str, Any]) -> float:
    return FOOTPRINT_H.get(row["footprint"], 0.50)


def _region_inset(
    bu0: float, bu1: float, bs0: float, bs1: float, inset_u: float, inset_s: float
) -> tuple[float, float, float, float]:
    return (bu0 + inset_u, bu1 - inset_u, bs0 + inset_s, bs1 - inset_s)


def _area(r: tuple[float, float, float, float]) -> float:
    return max(0.0, r[1] - r[0]) * max(0.0, r[3] - r[2])


def _clip_area(u: float, s: float, wu: float, ws: float, r: tuple[float, float, float, float]) -> float:
    u0, u1 = max(u - wu / 2.0, r[0]), min(u + wu / 2.0, r[1])
    s0, s1 = max(s - ws / 2.0, r[2]), min(s + ws / 2.0, r[3])
    return max(0.0, u1 - u0) * max(0.0, s1 - s0)


def _inside(u: float, s: float, wu: float, ws: float, r: tuple[float, float, float, float], slack: float = 1e-6) -> bool:
    return (
        u - wu / 2.0 >= r[0] - slack
        and u + wu / 2.0 <= r[1] + slack
        and s - ws / 2.0 >= r[2] - slack
        and s + ws / 2.0 <= r[3] + slack
    )


def _pad_edge(
    v2: Any, u: float, s: float, pad_w: float, pad_h: float, rot: float,
    outline: tuple[float, float, float, float],
) -> float:
    pw, ph = v2._rot_size(pad_w, pad_h, rot)
    u0, u1, s0, s1 = outline
    return min(
        (u - pw / 2.0) - u0,
        u1 - (u + pw / 2.0),
        (s - ph / 2.0) - s0,
        s1 - (s + ph / 2.0),
    )


def _copper_outline_for(
    u: float, s: float, wu: float, ws: float,
    island: tuple[float, float, float, float] | None,
    pocket: tuple[float, float, float, float] | None,
) -> tuple[float, float, float, float] | None:
    if island is not None and _inside(u, s, wu, ws, island, slack=0.4):
        return island
    if pocket is not None and _inside(u, s, wu, ws, pocket, slack=0.4):
        return pocket
    return None


def _v2c_find(
    v2: Any,
    name: str,
    sizes: list[tuple[float, float, float]],
    h: float,
    y0: float,
    face: str,
    regions: list[tuple[float, float, float, float]],
    occupied: list[Any],
    near: tuple[float, float] | None = None,
    step: float = 0.4,
    margin: float = 0.10,
    pad: tuple[float, float] | None = None,
    island: tuple[float, float, float, float] | None = None,
    pocket: tuple[float, float, float, float] | None = None,
) -> tuple[Any, float] | None:
    best: tuple[Any, float] | None = None
    best_d = math.inf
    copper_min = v2.COPPER_TO_EDGE if (pad is not None and island is not None) else None
    for (u0, u1, s0, s1) in regions:
        for wu, ws, rot in sizes:
            if wu > (u1 - u0) + 1e-9 or ws > (s1 - s0) + 1e-9:
                continue
            u_lo, u_hi = u0 + wu / 2.0, u1 - wu / 2.0
            s_lo, s_hi = s0 + ws / 2.0, s1 - ws / 2.0
            if u_hi < u_lo - 1e-9 or s_hi < s_lo - 1e-9:
                continue
            n_u = 0
            uu = u_lo
            if near is not None:
                uu = min(max(near[0], u_lo), u_hi)
            while uu <= u_hi + 1e-9 and n_u < 120:
                ss = s_lo
                if near is not None and n_u == 0:
                    ss = min(max(near[1], s_lo), s_hi)
                n_s = 0
                while ss <= s_hi + 1e-9 and n_s < 120:
                    cand = v2.Box(name, uu, ss, wu, ws, y0, y0 + h, face)
                    if not any(v2._overlap(cand, other, margin) for other in occupied):
                        if copper_min is not None and name not in COPPER_SKIP_REFS:
                            outline = _copper_outline_for(uu, ss, wu, ws, island, pocket)
                            if outline is not None:
                                if _pad_edge(v2, uu, ss, pad[0], pad[1], rot, outline) < copper_min - 1e-9:
                                    ss += step
                                    n_s += 1
                                    continue
                        if near is None:
                            return (cand, rot)
                        d = math.hypot(uu - near[0], ss - near[1])
                        if d < best_d:
                            best_d = d
                            best = (cand, rot)
                    ss += step
                    n_s += 1
                uu += step
                n_u += 1
    return best


def _u1_poses(v2: Any, geom: dict[str, Any], edge: str) -> list[tuple[float, float, float, float, float]]:
    """(rot, u, s, wu, ws) courtyard poses that meet the edge reading."""
    bu0, bu1 = geom["board_u"]
    bs0, bs1 = geom["board_s"]
    cr_w, cr_h = v2.KICAD_COURTYARD["Raytac_MDBT50Q"]
    bw, bh = 10.5, 15.5
    out: list[tuple[float, float, float, float, float]] = []
    for rot, wu, ws, body_u, body_s in (
        (0.0, cr_w, cr_h, bw, bh),
        (90.0, cr_h, cr_w, bh, bw),
    ):
        if edge == "process":
            if wu > (bu1 - bu0) + 1e-9 or ws > (bs1 - bs0) + 1e-9:
                continue
            u = bu0 + wu / 2.0 if (bu1 - bu0) - wu >= 2.5 else (bu0 + bu1) / 2.0
            s = bs1 - ws / 2.0
        else:
            need_u = body_u + 2 * v2.JLC_ASSEMBLY_EDGE
            need_s = body_s + 2 * v2.JLC_ASSEMBLY_EDGE
            if need_u > (bu1 - bu0) + 1e-9 or need_s > (bs1 - bs0) + 1e-9:
                continue
            u_lo = bu0 + v2.JLC_ASSEMBLY_EDGE + body_u / 2.0
            u_hi = bu1 - v2.JLC_ASSEMBLY_EDGE - body_u / 2.0
            s_hi = bs1 - v2.JLC_ASSEMBLY_EDGE - body_s / 2.0
            u = (u_lo + u_hi) / 2.0
            s = s_hi
        out.append((rot, u, s, wu, ws))
    return out


def fold_choice(v2: Any, spec: Any) -> tuple[str, dict[str, Any], float]:
    """Q83: neck-end is the default. Side-wall pockets only if remaining wall ≥ 1.0."""
    f = v2.tab_fold_variants(spec)
    wall_left = float(f["side"]["wall_left"])
    if spec.width + 1e-9 >= 22.0 and wall_left + 1e-9 >= V2C_WALL_MIN:
        return "side", f["side"], wall_left
    return "neck", f["neck"], wall_left


def posterior_wall_u(width: float, v2: Any | None = None) -> tuple[float, float]:
    """Inner and outer u of the posterior side wall.

    montage.md §2.1: u is the posterior offset from the body's anterior edge
    (u = 0). shell-v2.md: the hook root sits at low u on the hook-end face.
    params/default.toml HOOK_ROOT_X = 4.0. packing-v2.md: the hook root occupies
    u up to 6.39. The far wall from that root is u (width−1.50)–width.
    """
    wall = v2.WALL if v2 is not None else 1.5
    return (round(width - wall, 2), round(width, 2))


def charge_pad_y(v2: Any | None = None) -> float:
    """Ring centre y on the wall inner face: 1.5 of wall around the Ø2.7 hole vs floor."""
    floor = v2.FLOOR_Y if v2 is not None else 1.5
    return round(floor + CHARGE_WALL_AROUND + CHARGE_HOLE_D / 2.0, 2)


def charge_underside(v2: Any | None = None) -> float:
    floor = v2.FLOOR_Y if v2 is not None else 1.5
    tab = v2.TAB_T if v2 is not None else 0.31
    return floor + tab + CHARGE_STANDOFF


def charge_pad_sites(width: float, v2: Any | None = None) -> tuple[tuple[float, float], tuple[float, float]]:
    """Q90: two Ø5 charging pads on the posterior wall inner face, beside the cell.

    Folded (shell) sites: u is the inner face, s along the wall in the free bay.
    y is charge_pad_y. Flat centres are charge_flat_pads.
    """
    ring_r = v2.RING_R if v2 is not None else 2.5
    u_inner, _u_outer = posterior_wall_u(width, v2)
    s4 = round(CHARGE_BAY_S[0] + CHARGE_WALL_AROUND + CHARGE_HOLE_D / 2.0, 2)
    s5 = round(s4 + 2.0 * ring_r + CHARGE_NYLON, 2)
    return ((u_inner, s4), (u_inner, s5))


def charge_wall_sites(
    width: float, v2: Any | None = None
) -> dict[str, tuple[float, float, float, str, str]]:
    """P4/P5 (u, s, y, wall name, head axis)."""
    p4, p5 = charge_pad_sites(width, v2)
    y = charge_pad_y(v2)
    u0, u1 = posterior_wall_u(width, v2)
    wall = f"{CHARGE_WALL_NAME} (u {u0:.2f}–{u1:.2f})"
    return {
        "P4": (p4[0], p4[1], y, wall, CHARGE_HEAD_AXIS),
        "P5": (p5[0], p5[1], y, wall, CHARGE_HEAD_AXIS),
    }


def charge_tail_outline(
    v2: Any | None, island: tuple[float, float, float, float], width: float
) -> tuple[float, float, float, float]:
    """CHARGE rectangle in wall (s, y) mapped as (s0, s1, y0, y1) then unused.

    Kept as the s-span of both lands plus copper-to-edge, at the inner face.
    """
    p4, p5 = charge_pad_sites(width, v2)
    ring_r = v2.RING_R if v2 is not None else 2.5
    copper = v2.COPPER_TO_EDGE if v2 is not None else 0.30
    inset = ring_r + copper
    u_inner = p4[0]
    s0 = min(p4[1], p5[1]) - inset
    s1 = max(p4[1], p5[1]) + inset
    return (u_inner, u_inner, s0, s1)


def charge_drop_mm(v2: Any | None = None) -> float:
    """Island underside to floor. Unused by the v3 wall fold; kept for §5d history."""
    tab = v2.TAB_T if v2 is not None else 0.31
    return tab + CHARGE_STANDOFF


def charge_fold_allowance(v2: Any | None = None) -> float:
    """One 90° at BOARD_BEND_R: πR/2. Q90 wall fold, not the old two-bend drop."""
    r = v2.BOARD_BEND_R if v2 is not None else 1.5
    return math.pi * r / 2.0


def charge_wall_run(v2: Any | None = None) -> float:
    """Along the wall from the pocket-island plane to the pad y."""
    return abs(charge_underside(v2) - charge_pad_y(v2))


def charge_floor_lobe(
    v2: Any | None, island: tuple[float, float, float, float], width: float
) -> tuple[float, float, float, float]:
    """Folded wall-face span covering P4/P5 copper + 0.30 (u inner, s0, s1 unused u1)."""
    return charge_tail_outline(v2, island, width)


def charge_flat_map(
    v2: Any | None,
    island: tuple[float, float, float, float],
    u: float,
    s: float,
) -> tuple[float, float]:
    """90° unfold at the pocket high-u edge: wall −y becomes +u."""
    allow = charge_fold_allowance(v2)
    run = charge_wall_run(v2)
    fu = u + allow + run + CHARGE_FLAT_EXTRA
    return (round(fu, 2), round(s, 2))


def charge_flat_pads(
    v2: Any | None, island: tuple[float, float, float, float], width: float
) -> dict[str, tuple[float, float]]:
    p4, p5 = charge_pad_sites(width, v2)
    return {
        "P4": charge_flat_map(v2, island, *p4),
        "P5": charge_flat_map(v2, island, *p5),
    }


def charge_flat_box(
    v2: Any | None, island: tuple[float, float, float, float], width: float
) -> tuple[str, float, float, float, float]:
    """Unfolded CHARGE rectangle from the pocket island's high-u edge (name, u, s, wu, ws)."""
    flats = charge_flat_pads(v2, island, width)
    p4, p5 = charge_pad_sites(width, v2)
    copper = v2.COPPER_TO_EDGE if v2 is not None else 0.30
    ring_r = v2.RING_R if v2 is not None else 2.5
    inset = ring_r + copper + 0.02
    u_inner = p4[0]
    fus = [flats["P4"][0], flats["P5"][0]]
    fss = [flats["P4"][1], flats["P5"][1]]
    ru0 = min(u_inner, min(fus) - inset)
    ru1 = max(fus) + inset
    rs0 = min(fss) - inset
    rs1 = max(fss) + inset
    return ("CHARGE", (ru0 + ru1) / 2.0, (rs0 + rs1) / 2.0, ru1 - ru0, rs1 - rs0)


def charge_path_boxes(
    v2: Any | None, island: tuple[float, float, float, float], width: float
) -> list[tuple[str, float, float, float, float]]:
    """Q92: no rib slot, no drop corridor. The CHARGE rectangle is the whole path."""
    return []


def _edge_gap(
    u: float, s: float, r: float, ou: float, os: float, or_: float
) -> float:
    """Edge-to-edge gap of two circles. Negative is overlap."""
    return math.hypot(u - ou, s - os) - r - or_


# Tag-Connect TC2030-IDC-NL NPTH pads. Locals come from the KiCad footprint
# (`git show 6860a54:hardware/board/elicio-v2.kicad_pcb` or the board file).
# Fallback matches that footprint: three NPTH, drill 0.9906. min_hole_clearance
# 0.20 in elicio-v2.kicad_pro.
J4_NPTH_LOCAL = ((-2.54, 0.0), (2.54, -1.016), (2.54, 1.016))
J4_NPTH_DRILL = 0.9906
J4_HOLE_CLEARANCE = 0.20
J4_KICAD_COMMIT = "6860a54"
# Pin table v2 B.Cu cluster around J4 (WP11e). Restore, then fold the smallest hole move.
J4_NPTH_FOLD_SEEDS = {
    "R23": (18.28, 21.17),
    "R24": (18.28, 22.37),
    "R26": (14.22, 21.63),
}
# (u, s, rot) as published in pin table v2. Greedy-with-real-holes otherwise
# packs R27–R30 into R24's +u lane.
PIN_TABLE_V2_J4_CLUSTER = {
    "R23": (18.28, 21.17, 0.0),
    "R24": (18.28, 22.37, 0.0),
    "R26": (14.22, 21.63, 90.0),
    "R27": (18.22, 25.23, 90.0),
    "R28": (18.62, 27.23, 90.0),
    "R29": (18.62, 29.23, 90.0),
    "R30": (18.62, 31.23, 90.0),
}
_J4_PCB_CACHE: str | None = None


def fold_arc_mm(v2: Any) -> float:
    """180° at R 1.5: πR. Q83 strip lengths use this, not the midplane of the 0.31 stack."""
    return math.pi * v2.BOARD_BEND_R


def _j4_pcb_text() -> str:
    """KiCad PCB that holds the TC2030 footprint. Prefer the board WP12e pinned."""
    global _J4_PCB_CACHE
    if _J4_PCB_CACHE is not None:
        return _J4_PCB_CACHE
    root = Path(__file__).resolve().parents[2]
    text = ""
    try:
        out = subprocess.run(
            ["git", "show", f"{J4_KICAD_COMMIT}:hardware/board/elicio-v2.kicad_pcb"],
            cwd=root,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if out.returncode == 0 and "Tag-Connect_TC2030" in out.stdout:
            text = out.stdout
    except OSError:
        pass
    if not text:
        pcb = root / "hardware" / "board" / "elicio-v2.kicad_pcb"
        if pcb.is_file():
            text = pcb.read_text(encoding="utf-8")
    _J4_PCB_CACHE = text
    return text


def _j4_npth_locals_from_pcb(text: str) -> tuple[list[tuple[float, float]], float | None]:
    found: list[tuple[float, float]] = []
    d_found: float | None = None
    if not text:
        return found, d_found
    for block in text.split("(footprint "):
        if '(property "Reference" "J4"' not in block:
            continue
        if "Tag-Connect_TC2030" not in block:
            continue
        for m in re.finditer(
            r'\(pad "" np_thru_hole circle\s+\(at ([-\d.]+) ([-\d.]+)',
            block,
        ):
            found.append((float(m.group(1)), float(m.group(2))))
        dm = re.search(r"np_thru_hole circle.*?\(drill ([-\d.]+)\)", block, re.S)
        if dm:
            d_found = float(dm.group(1))
        break
    return found, d_found


_J4_SPEC_CACHE: tuple[tuple[tuple[float, float], ...], float, float] | None = None


def j4_npth_spec() -> tuple[tuple[tuple[float, float], ...], float, float]:
    """NPTH locals, drill, and hole clearance, read from the KiCad files when present."""
    global _J4_SPEC_CACHE
    if _J4_SPEC_CACHE is not None:
        return _J4_SPEC_CACHE
    root = Path(__file__).resolve().parents[2]
    pads = list(J4_NPTH_LOCAL)
    drill = J4_NPTH_DRILL
    clr = J4_HOLE_CLEARANCE
    found, d_found = _j4_npth_locals_from_pcb(_j4_pcb_text())
    if found:
        pads = found
    if d_found is not None:
        drill = d_found
    pro = root / "hardware" / "board" / "elicio-v2.kicad_pro"
    if pro.is_file():
        pm = re.search(r'"min_hole_clearance"\s*:\s*([0-9.]+)', pro.read_text(encoding="utf-8"))
        if pm:
            clr = float(pm.group(1))
    _J4_SPEC_CACHE = (tuple(pads), drill, clr)
    return _J4_SPEC_CACHE


def j4_npth_world(u: float, s: float, rot: float) -> tuple[tuple[float, float], ...]:
    """World centres. KiCad Y increases down; positive rot is CCW on that canvas."""
    pads, _drill, _clr = j4_npth_spec()
    rad = math.radians(rot)
    c, si = math.cos(rad), math.sin(rad)
    out: list[tuple[float, float]] = []
    for px, py in pads:
        du = px * c + py * si
        ds = -px * si + py * c
        out.append((round(u + du, 3), round(s + ds, 3)))
    return tuple(out)


def j4_npth_keep() -> float:
    _pads, drill, clr = j4_npth_spec()
    return drill + 2.0 * clr


def j4_npth_keep_r() -> float:
    """Pad-to-hole keep radius: drill/2 + min_hole_clearance (KiCad)."""
    _pads, drill, clr = j4_npth_spec()
    return drill / 2.0 + clr


def _pad_hits_j4_npth(
    v2: Any,
    u: float,
    s: float,
    pad_w: float,
    pad_h: float,
    rot: float,
    holes: tuple[tuple[float, float], ...],
    keep_r: float,
) -> bool:
    pw, ph = v2._rot_size(pad_w, pad_h, rot)
    u0, u1 = u - pw / 2.0, u + pw / 2.0
    s0, s1 = s - ph / 2.0, s + ph / 2.0
    for hu, hs in holes:
        nu = min(max(hu, u0), u1)
        ns = min(max(hs, s0), s1)
        if math.hypot(hu - nu, hs - ns) < keep_r - 1e-9:
            return True
    return False


def neck_flat_pads(
    v2: Any, island: tuple[float, float, float, float], sig1_strip: float, sig2_strip: float
) -> dict[str, tuple[float, float]]:
    """Ring centres in PCB (flat) coordinates. SIG1/SIG2 leave the island neck toward −s."""
    _u0, _u1, bs0, _bs1 = island
    return {
        "P1": (v2.CONTACT_1[0], bs0 - sig1_strip),
        "P2": (v2.CONTACT_2[0], bs0 - sig2_strip),
        "P3": (v2.CONTACT_REF[0], v2.CONTACT_REF[1]),
    }


def all_flat_pads(v2: Any, lay: LayoutV2c) -> dict[str, tuple[float, float]]:
    """P1–P3 neck flats plus P4/P5 charge flats when the cell carries them."""
    pads = neck_flat_pads(v2, lay.island, lay.sig1_strip, lay.sig2_strip)
    if any(p.ref in {"P4", "P5"} for p in lay.parts):
        pads.update(charge_flat_pads(v2, lay.island, lay.width))
    return pads


def folded_pad_sites(v2: Any, width: float, receptacle: bool) -> dict[str, tuple[float, float, float]]:
    """Shell sites (u, s, y). P1–P3 on the inner floor; P4/P5 on the posterior wall."""
    y = v2.FLOOR_Y
    out: dict[str, tuple[float, float, float]] = {
        "P1": (v2.CONTACT_1[0], v2.CONTACT_1[1], y),
        "P2": (v2.CONTACT_2[0], v2.CONTACT_2[1], y),
        "P3": (v2.CONTACT_REF[0], v2.CONTACT_REF[1], y),
    }
    if not receptacle:
        walls = charge_wall_sites(width, v2)
        for ref, (u, s, yy, _wall, _axis) in walls.items():
            out[ref] = (u, s, yy)
    return out


def _wall_around_mm(centre: float, hole_r: float, edge: float) -> float:
    return abs(edge - centre) - hole_r


def cavity_hits(v2: Any, lay: LayoutV2c, geom: dict[str, Any] | None = None) -> list[str]:
    """Every courtyard, hang and folded-board region is in the cavity or declared exterior."""
    if geom is None:
        _spec, geom = v2c_geom(v2, lay.width, lay.chord)
    cu0, cu1 = geom["cavity_u"]
    cs0, cs1 = geom["cavity_s"]
    _bu0, bu1, _bs0, _bs1 = lay.island
    hits: list[str] = []
    by = {p.ref: p for p in lay.parts}
    for p in lay.parts:
        if p.ref in CAVITY_EXTERIOR_REFS:
            if p.u - p.wu / 2.0 < bu1 - 1e-9:
                hits.append(
                    f"{p.ref} courtyard u {p.u - p.wu / 2.0:.2f} not on the break-off tab "
                    f"(island u1 {bu1:.2f})"
                )
            continue
        if p.face == "wall":
            if abs(p.u - cu1) > 0.05:
                hits.append(f"{p.ref} wall u {p.u:.2f} not inner face {cu1:.2f}")
            if p.s - 2.50 < cs0 - 1e-9 or p.s + 2.50 > cs1 + 1e-9:
                hits.append(f"{p.ref} Ø5 s outside cavity {cs0:.2f}–{cs1:.2f}")
            continue
        if p.ref == "P3":
            continue
        u0, u1 = p.u - p.wu / 2.0, p.u + p.wu / 2.0
        s0p, s1p = p.s - p.ws / 2.0, p.s + p.ws / 2.0
        if u0 < cu0 - 1e-9 or u1 > cu1 + 1e-9:
            hits.append(
                f"{p.ref} courtyard u {u0:.2f}–{u1:.2f} outside cavity {cu0:.2f}–{cu1:.2f}"
            )
        if s0p < cs0 - 1e-9 or s1p > cs1 + 1e-9:
            hits.append(
                f"{p.ref} courtyard s {s0p:.2f}–{s1p:.2f} outside cavity {cs0:.2f}–{cs1:.2f}"
            )
    j3 = by.get("J3")
    if j3 is not None:
        neck = j3.u - j3.wu / 2.0 - bu1
        if neck > J3_BREAK_NECK + 0.05:
            hits.append(f"J3 neck {neck:.2f} > {J3_BREAK_NECK:g}")
        if lay.j3_cut_u <= bu1 + 1e-9:
            hits.append("J3 cut line missing")
    return hits


def q97_zone_hits(v2: Any, lay: LayoutV2c) -> list[str]:
    """No other courtyard inside a land's 7 × 7 zone in PCB coordinates (Q97)."""
    hits: list[str] = []
    skip = {"P1", "P2", "P3", "P4", "P5"}
    pads = all_flat_pads(v2, lay)
    for name, (u, s) in pads.items():
        zone = v2.Box(f"{name}_7x7", u, s, 7.0, 7.0, -1.0, 20.0, "floor")
        for p in lay.parts:
            if p.ref in skip or p.face in {"floor", "wall", "hook"}:
                continue
            if v2._overlap(v2._part_box(p, 0.0, 1.0), zone, 0.0):
                hits.append(f"{p.ref} courtyard inside {name} 7×7")
    return hits


def _xy_overlap(
    u: float, s: float, wu: float, ws: float,
    ou: float, os: float, owu: float, ows: float,
    margin: float = 0.0,
) -> bool:
    if (u + wu / 2.0 + margin) <= (ou - owu / 2.0) or (ou + owu / 2.0 + margin) <= (u - wu / 2.0):
        return False
    if (s + ws / 2.0 + margin) <= (os - ows / 2.0) or (os + ows / 2.0 + margin) <= (s - ws / 2.0):
        return False
    return True


def _centre_in_courtyard(u: float, s: float, p: Any) -> bool:
    return abs(p.u - u) <= p.wu / 2.0 + 1e-9 and abs(p.s - s) <= p.ws / 2.0 + 1e-9


def flat_strip_box(
    v2: Any, name: str, pad: tuple[float, float], s_attach: float
) -> tuple[str, float, float, float, float]:
    """Strip rectangle from the island edge to the flat ring centre (u, s, wu, ws)."""
    u, s_pad = pad
    return (name, u, (s_attach + s_pad) / 2.0, v2.TAB_W, abs(s_attach - s_pad))


def flat_pattern_hits(v2: Any, lay: LayoutV2c) -> list[str]:
    """2D: strips vs leftover/pocket parts, rings vs other courtyards, strips vs strips."""
    pads = all_flat_pads(v2, lay)
    _u0, _u1, bs0, bs1 = lay.island
    cr_u, cr_s = v2.KICAD_COURTYARD["RING_PAD_D5_H2.7"]
    hits: list[str] = []
    strips = [
        flat_strip_box(v2, "SIG1", pads["P1"], bs0),
        flat_strip_box(v2, "SIG2", pads["P2"], bs0),
        flat_strip_box(v2, "REF", pads["P3"], bs1),
    ]
    charge_strips: list[tuple[str, float, float, float, float]] = []
    if "P4" in pads:
        charge_strips.append(charge_flat_box(v2, lay.island, lay.width))
        charge_strips.extend(charge_path_boxes(v2, lay.island, lay.width))
        strips.extend(charge_strips)
    for i, a in enumerate(strips):
        for b in strips[i + 1 :]:
            if _xy_overlap(a[1], a[2], a[3], a[4], b[1], b[2], b[3], b[4]):
                hits.append(f"strip {a[0]} overlaps strip {b[0]}")
    ring_names = tuple(pads)
    for i, ra in enumerate(ring_names):
        for rb in ring_names[i + 1 :]:
            if _xy_overlap(pads[ra][0], pads[ra][1], cr_u, cr_s, pads[rb][0], pads[rb][1], cr_u, cr_s):
                hits.append(f"flat {ra} courtyard overlaps flat {rb}")
    skip = {"P1", "P2", "P3", "P4", "P5"}
    leftover_or_pocket = []
    others = []
    for p in lay.parts:
        if p.ref in skip:
            continue
        if p.face == "hook":
            continue
        others.append(p)
        in_left = _inside(p.u, p.s, p.wu, p.ws, lay.leftover, slack=0.4)
        in_pocket = p.s + p.ws / 2.0 <= bs0 + 0.3
        if in_left or in_pocket:
            leftover_or_pocket.append(p)
    for name, su, ss, wu, ws in strips:
        targets = others if name.startswith("CHARGE") else leftover_or_pocket
        for p in targets:
            if _xy_overlap(su, ss, wu, ws, p.u, p.s, p.wu, p.ws):
                hits.append(f"strip {name} crosses {p.ref} on {p.face}")
        if name in {"SIG1", "SIG2"}:
            ru, rs = pads["P1" if name == "SIG1" else "P2"]
            for p in leftover_or_pocket:
                if _xy_overlap(ru, rs, cr_u, cr_s, p.u, p.s, p.wu, p.ws):
                    hits.append(f"flat {name} ring crosses {p.ref} on {p.face}")
        if name == "CHARGE":
            for pref in ("P4", "P5"):
                if pref not in pads:
                    continue
                ru, rs = pads[pref]
                for p in others:
                    if _xy_overlap(ru, rs, cr_u, cr_s, p.u, p.s, p.wu, p.ws):
                        hits.append(f"flat {pref} courtyard crosses {p.ref} on {p.face}")
    for ref, (u, s) in pads.items():
        for p in lay.parts:
            if p.ref in skip or p.face == "hook":
                continue
            if _centre_in_courtyard(u, s, p):
                hits.append(f"{ref} flat centre inside {p.ref} courtyard")
    return hits


def find_hole_sites(
    v2: Any,
    island: tuple[float, float, float, float],
    occupied: list[Any],
    *,
    y0: float,
    y1: float,
    prefer: tuple[float, float, float, float] | None = None,
    step: float = 0.5,
    min_sep: float | None = None,
) -> list[tuple[float, float]]:
    """Q82: two Ø2.7 holes (keep 3.30) where courtyards allow. Prefer not leftover."""
    bu0, bu1, bs0, bs1 = island
    ku = v2.BOSS_HOLE_KEEP
    sep = ku + 1.0 if min_sep is None else min_sep
    found: list[tuple[float, float]] = []

    def try_region(r: tuple[float, float, float, float]) -> None:
        u0, u1, s0, s1 = r
        uu = u0 + ku / 2.0
        while uu <= u1 - ku / 2.0 + 1e-9 and len(found) < 2:
            ss = s0 + ku / 2.0
            while ss <= s1 - ku / 2.0 + 1e-9 and len(found) < 2:
                cand = v2.Box("HOLE", uu, ss, ku, ku, y0, y1, "floor")
                if any(v2._overlap(cand, other, 0.0) for other in occupied):
                    ss += step
                    continue
                if any(str(other.name) == "U1" and v2._overlap(cand, other, 0.0) for other in occupied):
                    ss += step
                    continue
                if all(math.hypot(uu - hu, ss - hs) >= sep for hu, hs in found):
                    found.append((uu, ss))
                ss += step
            uu += step

    if prefer is not None and prefer[1] - prefer[0] > ku and prefer[3] - prefer[2] > ku:
        try_region(prefer)
    try_region(island)
    return found


def q98_three_track_need() -> float:
    """n Default tracks between two keep-outs: n×width + (n+1)×clearance."""
    return Q98_TRACKS * DEFAULT_TRACK_W + (Q98_TRACKS + 1) * DEFAULT_CLEAR


def q98_hole_gap_need() -> float:
    """Keep-to-keep gap: 0.12 more than the 1.20 mm WP12h gap, plus margin."""
    return Q98_GAP_WAS + Q98_GAP_EXTRA + Q98_GAP_MARGIN


def q98_via_slot_need() -> float:
    """Via pad plus Default clearance on both sides."""
    return VIA_PAD_D + 2.0 * DEFAULT_CLEAR


def hole_keep_gap(sites: tuple[tuple[float, float], ...] | list[tuple[float, float]], keep: float) -> float:
    if len(sites) < 2:
        return 0.0
    (u0, s0), (u1, s1) = sites[0], sites[1]
    c2c = math.hypot(u1 - u0, s1 - s0)
    return c2c - keep


def pin_q98_hole_sites(
    v2: Any,
    leftover: tuple[float, float, float, float],
    occupied: list[Any],
    *,
    y0: float,
    y1: float,
) -> list[tuple[float, float]]:
    """H1 west of H2 so the keep-out gap takes three Default tracks (Q98). H2 stays put."""
    ku = v2.BOSS_HOLE_KEEP
    gap = q98_hole_gap_need()
    c2c = ku + gap
    s = Q98_HOLE_S
    skip = ("RING_", "FLAT", "Q97", "TABROOT")
    blockers = [b for b in occupied if not str(b.name).startswith(skip)]
    u2 = min(Q98_H2_U, leftover[1] - ku / 2.0)
    u1 = u2 - c2c
    if u1 - ku / 2.0 < leftover[0] - 1e-9:
        u1 = leftover[0] + ku / 2.0
        u2 = u1 + c2c

    def clear(uu: float) -> bool:
        if uu - ku / 2.0 < leftover[0] - 1e-9 or uu + ku / 2.0 > leftover[1] + 1e-9:
            return False
        cand = v2.Box("HOLE", uu, s, ku, ku, y0, y1, "floor")
        return not any(v2._overlap(cand, other, 0.0) for other in blockers)

    if not clear(u1) or not clear(u2):
        for du in (i * 0.05 for i in range(0, 40)):
            a = u1 - du
            b = a + c2c
            if clear(a) and clear(b):
                u1, u2 = a, b
                break
            a = u1 + du
            b = a + c2c
            if clear(a) and clear(b):
                u1, u2 = a, b
                break
        else:
            return []
    return [(u1, s), (u2, s)]


def hole_channel_box(
    v2: Any, sites: list[tuple[float, float]] | tuple[tuple[float, float], ...]
) -> tuple[float, float, float, float] | None:
    if len(sites) < 2:
        return None
    keep = v2.BOSS_HOLE_KEEP if v2 is not None else 3.30
    k = keep / 2.0
    (u0, s0), (u1, s1) = sites[0], sites[1]
    if u1 < u0:
        u0, s0, u1, s1 = u1, s1, u0, s0
    return (u0 + k, min(s0, s1) - k, u1 - k, max(s0, s1) + k)


def j4_via_slot(j4: Any) -> tuple[float, float, float, float]:
    """Empty via bay beside J4, east of the SIG2 run (the west face of J4)."""
    u0 = SIG2_RUN_U + CONTACT_TRACK_W / 2.0 + CONTACT_CLEAR
    u1 = j4.u - j4.wu / 2.0
    s0 = max(SIG2_RUN_S[0], j4.s - j4.ws / 2.0)
    s1 = min(SIG2_RUN_S[1], j4.s + j4.ws / 2.0)
    return (u0, s0, u1, s1)


def _aabb_channel_gap(
    au: float, as_: float, awu: float, aws: float,
    bu: float, bs: float, bwu: float, bws: float,
) -> float:
    du = abs(au - bu) - (awu + bwu) / 2.0
    ds = abs(as_ - bs) - (aws + bws) / 2.0
    if du < 0.0 and ds < 0.0:
        return min(du, ds)
    if du < 0.0:
        return ds
    if ds < 0.0:
        return du
    return math.hypot(du, ds)


def _xy_boxes_overlap(
    u0: float, s0: float, u1: float, s1: float,
    cu: float, cs: float, wu: float, ws: float,
) -> bool:
    a0, a1 = cu - wu / 2.0, cu + wu / 2.0
    b0, b1 = cs - ws / 2.0, cs + ws / 2.0
    return a0 < u1 - 1e-9 and a1 > u0 + 1e-9 and b0 < s1 - 1e-9 and b1 > s0 + 1e-9


def q98_channel_boxes(v2: Any, lay: LayoutV2c) -> list[tuple[str, float, float, float, float, str]]:
    """Keep-out list for the board: (name, u0, s0, u1, s1, note)."""
    out: list[tuple[str, float, float, float, float, str]] = []
    hole_box = hole_channel_box(v2, lay.hole_sites)
    if hole_box is not None:
        u0, s0, u1, s1 = hole_box
        out.append(
            (
                "HOLE_CH",
                u0, s0, u1, s1,
                f"three Default tracks between H1/H2 keep-outs; gap {u1 - u0:.2f} mm "
                f"(need {q98_hole_gap_need():.2f}; {Q98_TRACKS}×{DEFAULT_TRACK_W:.2f}+"
                f"{Q98_TRACKS + 1}×{DEFAULT_CLEAR:.2f}={q98_three_track_need():.2f})",
            )
        )
    by = {p.ref: p for p in lay.parts}
    extra = Q98_CHANNEL
    for ref, note in (
        ("U2", "0.6 mm around U2 (B.Cu escape)"),
        ("U3", "0.6 mm around U3 (F.Cu escape)"),
        ("J4", "0.6 mm around J4, both sides"),
    ):
        p = by.get(ref)
        if p is None:
            continue
        out.append(
            (
                f"{ref}_CH",
                p.u - p.wu / 2.0 - extra,
                p.s - p.ws / 2.0 - extra,
                p.u + p.wu / 2.0 + extra,
                p.s + p.ws / 2.0 + extra,
                note,
            )
        )
    j4 = by.get("J4")
    if j4 is not None:
        u0, s0, u1, s1 = j4_via_slot(j4)
        out.append(
            (
                "J4_VIA_SLOT",
                u0, s0, u1, s1,
                "via slot beside J4, east of the SIG2 run at u 13.50 (west face of J4); "
                f"width {u1 - u0:.2f} mm, need {q98_via_slot_need():.2f}",
            )
        )
        out.append(
            (
                "J4_APPROACH_EAST",
                j4.u + j4.wu / 2.0,
                j4.s - j4.ws / 2.0 - extra,
                j4.u + j4.wu / 2.0 + 2.50,
                j4.s + j4.ws / 2.0 + extra,
                "east 0402 row stays out of the J4 approach (R16 and neighbours)",
            )
        )
    return out


def q98_hits(v2: Any, lay: LayoutV2c) -> list[str]:
    """Courtyards inside a Q98 channel, a thin hole gap, or the J4 via slot."""
    hits: list[str] = []
    by = {p.ref: p for p in lay.parts}
    keep = v2.BOSS_HOLE_KEEP
    gap = hole_keep_gap(lay.hole_sites, keep)
    if len(lay.hole_sites) < 2:
        hits.append("H1/H2 missing")
    elif gap + 1e-9 < q98_hole_gap_need():
        hits.append(f"H1/H2 keep-out gap {gap:.3f} < {q98_hole_gap_need():.2f}")
    elif gap + 1e-9 < q98_three_track_need():
        hits.append(f"H1/H2 keep-out gap {gap:.3f} < three Default tracks {q98_three_track_need():.2f}")
    j4 = by.get("J4")
    if j4 is None:
        hits.append("J4 missing")
    else:
        u0, s0, u1, s1 = j4_via_slot(j4)
        width = u1 - u0
        if width + 1e-9 < q98_via_slot_need():
            hits.append(f"J4 via slot {width:.3f} < {q98_via_slot_need():.2f}")
        keep_r = j4_npth_keep_r()
        for p in lay.parts:
            if p.ref == "J4" or p.face in {"floor", "wall", "hook"}:
                continue
            small = p.wu <= 2.0 and p.ws <= 2.0
            if p.ref in EAST_0402_ROW or (small and p.face == "bottom"):
                if _xy_boxes_overlap(u0, s0, u1, s1, p.u, p.s, p.wu, p.ws):
                    hits.append(f"{p.ref} in J4_VIA_SLOT")
                east0 = j4.u + j4.wu / 2.0
                if _xy_boxes_overlap(
                    east0,
                    j4.s - j4.ws / 2.0 - Q98_CHANNEL,
                    east0 + 2.50,
                    j4.s + j4.ws / 2.0 + Q98_CHANNEL,
                    p.u, p.s, p.wu, p.ws,
                ):
                    hits.append(f"{p.ref} in J4_APPROACH_EAST")
            if p.face == "bottom" and _pad_hits_j4_npth(
                v2, p.u, p.s, p.pad_w, p.pad_h, p.rot, lay.j4_npth, keep_r
            ):
                hits.append(f"{p.ref} on a J4 hole")
        for p in lay.parts:
            if p.ref in {"J4", "U1"} or p.face != "top":
                continue
            g = _aabb_channel_gap(j4.u, j4.s, j4.wu, j4.ws, p.u, p.s, p.wu, p.ws)
            if g + 1e-9 < Q98_CHANNEL:
                hits.append(f"{p.ref} {g:.3f} mm from J4 (need {Q98_CHANNEL:.1f})")
    for ref in ("U2", "U3"):
        p = by.get(ref)
        if p is None:
            hits.append(f"{ref} missing")
            continue
        for other in lay.parts:
            if other.ref == ref or other.face in {"floor", "wall", "hook"}:
                continue
            if (ref, other.ref) in Q98_STACK_SKIP:
                continue
            if ref == "U2" and other.face != "bottom":
                continue
            if ref == "U3" and other.face != "top":
                continue
            g = _aabb_channel_gap(p.u, p.s, p.wu, p.ws, other.u, other.s, other.wu, other.ws)
            if g + 1e-9 < Q98_CHANNEL:
                hits.append(f"{other.ref} {g:.3f} mm from {ref} (need {Q98_CHANNEL:.1f})")
    hole_box = hole_channel_box(v2, lay.hole_sites)
    if hole_box is not None:
        u0, s0, u1, s1 = hole_box
        for p in lay.parts:
            if p.ref in {"P1", "P2", "P3", "P4", "P5"} or p.face in {"floor", "wall", "hook"}:
                continue
            if _xy_boxes_overlap(u0, s0, u1, s1, p.u, p.s, p.wu, p.ws):
                hits.append(f"{p.ref} in HOLE_CH")
    return hits


def _nudge_one(
    v2: Any,
    part: Any,
    occupied: list[Any],
    island: tuple[float, float, float, float],
    pocket: tuple[float, float, float, float],
    need: float,
) -> Any:
    """Move a part inward until pad-to-outline ≥ need, or leave it if the site is blocked."""
    if part.ref in COPPER_SKIP_REFS or part.face not in {"top", "bottom"}:
        return part
    outline = _copper_outline_for(part.u, part.s, part.wu, part.ws, island, pocket)
    if outline is None:
        return part
    edge = _pad_edge(v2, part.u, part.s, part.pad_w, part.pad_h, part.rot, outline)
    if edge + 1e-9 >= need:
        return part
    pw, ph = v2._rot_size(part.pad_w, part.pad_h, part.rot)
    u0, u1, s0, s1 = outline
    du = ds = 0.0
    left = (part.u - pw / 2.0) - u0
    right = u1 - (part.u + pw / 2.0)
    bot = (part.s - ph / 2.0) - s0
    top = s1 - (part.s + ph / 2.0)
    if left < need:
        du += need - left
    if right < need:
        du -= need - right
    if bot < need:
        ds += need - bot
    if top < need:
        ds -= need - top
    nu, ns = part.u + du, part.s + ds
    old = next((b for b in occupied if b.name == part.ref), None)
    if old is None:
        return replace(part, u=nu, s=ns)
    cand = v2.Box(part.ref, nu, ns, part.wu, part.ws, old.y0, old.y1, old.face)
    if any(v2._overlap(cand, other, 0.10) for other in occupied if other.name != part.ref):
        return part
    occupied[occupied.index(old)] = cand
    return replace(part, u=nu, s=ns)


def _nudge_copper_parts(
    v2: Any,
    parts: list[Any],
    occupied: list[Any],
    island: tuple[float, float, float, float],
    pocket: tuple[float, float, float, float],
    *,
    named: tuple[str, ...] = NUDGE_COPPER_REFS,
) -> None:
    """Named refs first (WP12d pin table), then any other pad that is still short of 0.30."""
    need = v2.COPPER_TO_EDGE
    seen: set[str] = set()
    order = list(named) + [p.ref for p in parts if p.ref not in named]
    by = {p.ref: i for i, p in enumerate(parts)}
    for ref in order:
        if ref in seen or ref not in by:
            continue
        seen.add(ref)
        parts[by[ref]] = _nudge_one(v2, parts[by[ref]], occupied, island, pocket, need)


def _part_hits_j4_npth(v2: Any, part: Any, holes: tuple[tuple[float, float], ...], keep_r: float) -> bool:
    return _pad_hits_j4_npth(v2, part.u, part.s, part.pad_w, part.pad_h, part.rot, holes, keep_r)


def _site_clears_j4_npth(
    v2: Any,
    part: Any,
    uu: float,
    ss: float,
    occupied: list[Any],
    island: tuple[float, float, float, float],
    pocket: tuple[float, float, float, float],
    holes: tuple[tuple[float, float], ...],
    keep_r: float,
    need: float,
    *,
    rot: float | None = None,
    wu: float | None = None,
    ws: float | None = None,
) -> bool:
    rot = part.rot if rot is None else rot
    wu = part.wu if wu is None else wu
    ws = part.ws if ws is None else ws
    old = next((b for b in occupied if b.name == part.ref), None)
    y0, y1 = (old.y0, old.y1) if old is not None else (0.0, 1.0)
    cand = v2.Box(part.ref, uu, ss, wu, ws, y0, y1, part.face)
    for other in occupied:
        if other.name == part.ref:
            continue
        if str(other.name).startswith("J4_NPTH"):
            continue
        if v2._overlap(cand, other, 0.0):
            return False
    outline = _copper_outline_for(uu, ss, wu, ws, island, pocket)
    if outline is not None:
        if _pad_edge(v2, uu, ss, part.pad_w, part.pad_h, rot, outline) < need - 1e-9:
            return False
    if _pad_hits_j4_npth(v2, uu, ss, part.pad_w, part.pad_h, rot, holes, keep_r):
        return False
    return True


def _min_site_off_j4_npth(
    v2: Any,
    part: Any,
    occupied: list[Any],
    island: tuple[float, float, float, float],
    pocket: tuple[float, float, float, float],
    holes: tuple[tuple[float, float], ...],
    keep_r: float,
    need: float,
    seed: tuple[float, float],
) -> tuple[float, float, float, float, float] | None:
    """Nearest 0.01 mm site to the pin-table-v2 seed. Tries both 0402 rotations."""
    su, ss0 = seed
    poses = (
        (part.rot, part.wu, part.ws),
        ((part.rot + 90.0) % 180.0, part.ws, part.wu),
    )
    for rot, wu, ws in poses:
        if _site_clears_j4_npth(
            v2, part, su, ss0, occupied, island, pocket, holes, keep_r, need, rot=rot, wu=wu, ws=ws
        ):
            return su, ss0, rot, wu, ws
    best: tuple[float, float, float, float, float] | None = None
    best_key: tuple[float, float, float, float] | None = None
    for n in range(1, 201):
        for du_i in range(-n, n + 1):
            for ds_i in range(-n, n + 1):
                if max(abs(du_i), abs(ds_i)) != n:
                    continue
                uu = round(su + du_i * 0.01, 2)
                ss = round(ss0 + ds_i * 0.01, 2)
                for rot, wu, ws in poses:
                    if not _site_clears_j4_npth(
                        v2, part, uu, ss, occupied, island, pocket, holes, keep_r, need,
                        rot=rot, wu=wu, ws=ws,
                    ):
                        continue
                    hyp = math.hypot(uu - su, ss - ss0)
                    rot_pen = 0.0 if abs(rot - part.rot) < 1e-9 else 0.01
                    key = (hyp + rot_pen, -(uu - su), abs(ss - ss0), rot_pen)
                    if best_key is None or key < best_key:
                        best_key = key
                        best = (uu, ss, rot, wu, ws)
        if best is not None:
            return best
    return None


def _clamp_courtyards_to_island(
    v2: Any,
    parts: list[Any],
    occupied: list[Any],
    island: tuple[float, float, float, float],
) -> None:
    """Pull on-island courtyards back to the outline (process-edge)."""
    bu0, bu1, bs0, bs1 = island
    by = {p.ref: i for i, p in enumerate(parts)}
    skip = {"J1", "J3", "P1", "P2", "P3", "P4", "P5"}
    for p in list(parts):
        if p.ref in skip or p.face not in {"top", "bottom"}:
            continue
        if p.s + p.ws / 2.0 < bs0 - 0.3:
            continue
        du = 0.0
        if p.u + p.wu / 2.0 > bu1 + 1e-9:
            du = bu1 - (p.u + p.wu / 2.0)
        elif p.u - p.wu / 2.0 < bu0 - 1e-9:
            du = bu0 - (p.u - p.wu / 2.0)
        if abs(du) < 1e-9:
            continue
        nu = p.u + du
        old = next((b for b in occupied if b.name == p.ref), None)
        y0, y1 = (old.y0, old.y1) if old is not None else (0.0, 1.0)
        cand = v2.Box(p.ref, nu, p.s, p.wu, p.ws, y0, y1, p.face)
        if any(o.name != p.ref and v2._overlap(cand, o, 0.10) for o in occupied):
            continue
        parts[by[p.ref]] = replace(p, u=nu)
        if old is not None:
            occupied[occupied.index(old)] = cand


def _restore_pin_table_v2_j4_cluster(
    v2: Any,
    parts: list[Any],
    occupied: list[Any],
) -> None:
    """Put the J4-side B.Cu cluster back on pin table v2 before the hole nudge (Q87)."""
    table = v2.kicad_part_table()
    by = {p.ref: i for i, p in enumerate(parts)}
    for ref, (u, s, rot) in PIN_TABLE_V2_J4_CLUSTER.items():
        if ref not in by:
            continue
        part = parts[by[ref]]
        row = table[ref]
        wu, ws = v2._rot_size(row["cr_w"], row["cr_h"], rot)
        old = next((b for b in occupied if b.name == ref), None)
        y0, y1, face = (old.y0, old.y1, old.face) if old is not None else (0.0, 1.0, part.face)
        cand = v2.Box(ref, u, s, wu, ws, y0, y1, face)
        if any(o.name != ref and v2._overlap(cand, o, 0.10) for o in occupied):
            continue
        parts[by[ref]] = replace(part, u=u, s=s, rot=rot, wu=wu, ws=ws)
        if old is not None:
            occupied[occupied.index(old)] = cand


def _nudge_off_j4_npth(
    v2: Any,
    parts: list[Any],
    occupied: list[Any],
    island: tuple[float, float, float, float],
    pocket: tuple[float, float, float, float],
    holes: tuple[tuple[float, float], ...],
) -> None:
    """Smallest move off the real J4 holes from pin table v2 (Q87)."""
    if not holes:
        return
    keep_r = j4_npth_keep_r()
    need = v2.COPPER_TO_EDGE
    by = {p.ref: i for i, p in enumerate(parts)}
    refs: list[str] = []
    for ref in ("R24", "R26", "R23"):
        if ref in by and parts[by[ref]].face == "bottom":
            refs.append(ref)
    for p in parts:
        if p.face == "bottom" and p.ref not in refs and _part_hits_j4_npth(v2, p, holes, keep_r):
            refs.append(p.ref)
    for ref in refs:
        part = parts[by[ref]]
        seed = J4_NPTH_FOLD_SEEDS.get(ref, (part.u, part.s))
        site = _min_site_off_j4_npth(v2, part, occupied, island, pocket, holes, keep_r, need, seed)
        if site is None:
            continue
        nu, ns, rot, wu, ws = site
        if abs(nu - part.u) < 1e-9 and abs(ns - part.s) < 1e-9 and abs(rot - part.rot) < 1e-9:
            continue
        old = next((b for b in occupied if b.name == ref), None)
        if old is not None:
            occupied[occupied.index(old)] = v2.Box(ref, nu, ns, wu, ws, old.y0, old.y1, old.face)
        parts[by[ref]] = replace(part, u=nu, s=ns, rot=rot, wu=wu, ws=ws)


def search_layout_v2c(
    v2: Any,
    edge: str,
    width: float,
    chord: float,
    two_sides: bool,
    *,
    receptacle: bool = True,
    table: dict[str, dict[str, Any]] | None = None,
) -> LayoutV2c:
    table = table if table is not None else v2.kicad_part_table()
    spec, geom = v2c_geom(v2, width, chord)
    bu0, bu1 = geom["board_u"]
    bs0, bs1 = geom["board_s"]
    island = (bu0, bu1, bs0, bs1)
    clr = under_board_clearance(v2, geom)
    y_top = geom["board_top"]
    y_und = geom["board_underside"]
    y_air0, y_air1 = v2.FLOOR_Y, y_und
    cell = v2._place_cell(spec, geom, None)
    fold_name, fold_nums, wall_left = fold_choice(v2, spec)
    skip_refs = set() if receptacle else set(NOREC_SKIP_REFS)
    required = {r for r in table if r not in skip_refs}
    if not receptacle:
        required.update({"P4", "P5"})
    bom_n = len(required)
    usb = None
    usb_wall = "none (Q81 no receptacle)"
    if receptacle:
        usb_u = (bu0 + bu1) / 2.0
        usb_s = v2.CAVITY_S0 - v2.USB[1] / 2.0
        usb = v2.Box("usb_c", usb_u, usb_s, v2.USB[0], v2.USB[1], v2.USB_RECESS, v2.USB_RECESS + v2.USB[2], "hook")
        usb_wall = "hook-end end face (occupant, Q80)"

    occupied: list[Any] = [cell]
    # Rings and tab roots occupy the under-board air. Holes wait until after SW1 (Q82).
    for name, site in (("RING_SIG1", v2.CONTACT_1), ("RING_SIG2", v2.CONTACT_2)):
        occupied.append(v2.Box(name, site[0], site[1], 7.0, 7.0, y_air0, y_top + 8.0, "floor"))
    occupied.append(
        v2.Box("RING_REF", v2.CONTACT_REF[0], v2.CONTACT_REF[1], 7.0, 7.0, y_air0, y_top + 8.0, "floor")
    )
    if fold_name == "neck":
        occupied.append(v2.Box("TABROOT_SIG1", v2.CONTACT_1[0], bs0 + 1.0, v2.TAB_W, 2.0, y_air0, y_air1, "floor"))
        occupied.append(v2.Box("TABROOT_SIG2", v2.CONTACT_2[0], bs0 + 1.0, v2.TAB_W, 2.0, y_air0, y_air1, "floor"))
    else:
        occupied.append(v2.Box("TABROOT_SIG1", bu0 + 2.0, v2.CONTACT_1[1], 4.0, v2.TAB_W, y_air0, y_air1, "floor"))
        occupied.append(v2.Box("TABROOT_SIG2", bu1 - 2.0, v2.CONTACT_2[1], 4.0, v2.TAB_W, y_air0, y_air1, "floor"))
    occupied.append(v2.Box("TABROOT_REF", v2.CONTACT_REF[0], bs1 - 2.0, v2.TAB_W, 4.0, y_air0, y_air1, "floor"))
    if not receptacle:
        for i, site in enumerate(charge_pad_sites(width, v2), 1):
            # Standoff lives in under-board air only. Top SMT may sit above it.
            occupied.append(
                v2.Box(
                    f"RING_CHG{i}",
                    site[0] - 1.2,
                    site[1],
                    2.4,
                    6.40,
                    y_air0,
                    y_und,
                    "wall",
                )
            )

    parts: list[Any] = []
    missing: list[str] = []
    second_side: list[str] = []

    def add(part: Any, y0: float, h: float) -> None:
        parts.append(part)
        occupied.append(v2._part_box(part, y0, y0 + h))

    poses = _u1_poses(v2, geom, edge)
    u1_row = table["U1"]
    if poses:
        rot, u, s, wu, ws = poses[0]
        u1 = v2.LayoutPart(
            "U1", u1_row["footprint"], u, s, rot, u1_row["cr_w"], u1_row["cr_h"],
            u1_row["pad_w"], u1_row["pad_h"], wu, ws, "top",
            f"{edge} pose; courtyard {wu:.2f}×{ws:.2f}",
        )
        add(u1, y_top, v2.MODULE["A"]["h"])
        if ws >= wu:
            ant = (u - 12.4 / 2.0, s + ws / 2.0 - 3.8, u + 12.4 / 2.0, s + ws / 2.0)
        else:
            ant = (u - wu / 2.0, s - 12.4 / 2.0, u - wu / 2.0 + 3.8, s + 12.4 / 2.0)
        occupied.append(
            v2.Box(
                "RF_NO_COPPER",
                (ant[0] + ant[2]) / 2.0,
                (ant[1] + ant[3]) / 2.0,
                ant[2] - ant[0],
                ant[3] - ant[1],
                y_top,
                y_top + 10.0,
                "top",
            )
        )
        leftover = (bu0 + 0.05, bu1 - 0.05, bs0 + 0.05, min(s - ws / 2.0 - 0.15, bs1) - 0.05)
        side = (u + wu / 2.0 + 0.05, bu1 - 0.05, max(bs0, s - ws / 2.0), min(bs1, s + ws / 2.0))
    else:
        missing.append("U1")
        leftover = (bu0 + 0.05, bu1 - 0.05, bs0 + 0.05, bs1 - 0.05)
        side = leftover
        ant = None

    pu0 = cell.u1 + 0.2
    pu1 = geom["cavity_u"][1] - 0.15
    ps0 = geom["cavity_s"][0] + 0.15
    ps1 = geom["rib_s"][0] - 0.15
    pocket = (pu0, pu1, ps0, ps1)
    inset = 0.0 if edge == "process" else v2.JLC_ASSEMBLY_EDGE
    def _in(r):
        return (r[0] + inset, r[1] - inset, r[2] + inset, r[3] - inset)
    leftover_i = _in(leftover)
    side_i = _in(side)
    pocket_i = (pocket[0] + inset, pocket[1] - inset, pocket[2] + inset, pocket[3] - inset)
    hang = (bu1 + 0.2, bu1 + 14.0, bs0, bs1)
    if not receptacle:
        hang = (bu1 + J3_BREAK_NECK, bu1 + J3_BREAK_NECK + 16.0, bs0, bs1)
    top_regions = [leftover_i, side_i, pocket_i]
    top_regions = [r for r in top_regions if r[1] - r[0] > 0.4 and r[3] - r[2] > 0.4]
    bot_inset = v2.COPPER_TO_EDGE if edge == "process" else v2.JLC_ASSEMBLY_EDGE
    bot_region = (bu0 + bot_inset, bu1 - bot_inset, bs0 + bot_inset, bs1 - bot_inset)

    if usb is not None:
        j1 = v2._make_part("J1", table, usb.u, usb.s, 0.0, "hook", f"USB hook-end occupant ({usb_wall})")
        add(j1, usb.y0, v2.USB[2])

    for ref, site, note in (
        ("P1", v2.CONTACT_1, "SIG1 ring; Q79 tab carries one Contact trace"),
        ("P2", v2.CONTACT_2, "SIG2 ring"),
        ("P3", v2.CONTACT_REF, "REF ring; REF_end_wall_slot"),
    ):
        add(v2._make_part(ref, table, site[0], site[1], 0.0, "floor", note), v2.FLOOR_Y, v2.TAB_T)

    if not receptacle:
        cr = v2.KICAD_COURTYARD["RING_PAD_D5_H2.7"]
        pad = v2.KICAD_PAD_EXTENT["RING_PAD_D5_H2.7"]
        u0, u1 = posterior_wall_u(width, v2)
        wall_note = f"{CHARGE_WALL_NAME} u {u0:.2f}–{u1:.2f}; head {CHARGE_HEAD_AXIS}; RING_PAD_D5_H2.7"
        for ref, site, note in (
            ("P4", charge_pad_sites(width, v2)[0], f"CHARGE_VBUS clamped button-head (Q90); {wall_note}"),
            ("P5", charge_pad_sites(width, v2)[1], f"CHARGE_GND clamped button-head (Q90); {wall_note}"),
        ):
            part = v2.LayoutPart(
                ref, "RING_PAD_D5_H2.7", site[0], site[1], 0.0,
                cr[0], cr[1], pad[0], pad[1], CHARGE_STANDOFF, cr[1], "wall", note,
            )
            parts.append(part)
            occupied.append(
                v2.Box(
                    ref,
                    site[0] - 1.2,
                    site[1],
                    2.4,
                    cr[1],
                    y_air0,
                    y_und,
                    "wall",
                )
            )

    def sizes_for(ref: str) -> list[tuple[float, float, float]]:
        row = table[ref]
        out = []
        for rot in (0.0, 90.0):
            wu, ws = v2._rot_size(row["cr_w"], row["cr_h"], rot)
            out.append((wu, ws, rot))
        return out

    copper_island = island if edge == "process" else None
    copper_pocket = pocket if edge == "process" else None

    def try_top(ref: str, regions: list, near=None, notes="", step: float = 0.4, margin: float = 0.10) -> bool:
        row = table[ref]
        h = _height(row)
        found = _v2c_find(
            v2, ref, sizes_for(ref), h, y_top, "top", regions, occupied, near=near,
            step=step, margin=margin,
            pad=(row["pad_w"], row["pad_h"]), island=copper_island, pocket=copper_pocket,
        )
        if found is None:
            return False
        placed, rot = found
        add(v2._make_part(ref, table, placed.u, placed.s, rot, "top", notes), y_top, h)
        return True

    def try_bottom(ref: str, notes="", step: float = 0.4, margin: float = 0.10, regions=None) -> bool:
        if not two_sides:
            return False
        row = table[ref]
        h = _height(row)
        if h > clr["air_mm"] + 1e-9:
            return False
        y0 = y_und - h
        found = _v2c_find(
            v2, ref, sizes_for(ref), h, y0, "bottom", regions or [bot_region], occupied, step=step,
            margin=margin,
            pad=(row["pad_w"], row["pad_h"]), island=copper_island, pocket=copper_pocket,
        )
        if found is None:
            return False
        placed, rot = found
        add(v2._make_part(ref, table, placed.u, placed.s, rot, "bottom", notes or "second side"), y0, h)
        second_side.append(ref)
        return True

    # Q85: neck-end strips occupy leftover/pocket XY on both sides so parts cannot sit on them.
    # Only the no-receptacle cell is the flat-pattern build (Q81). J1 on the hook sits in that XY.
    if not receptacle:
        flat_pads = neck_flat_pads(v2, island, float(fold_nums["SIG1_strip"]), float(fold_nums["SIG2_strip"]))
        cr_u, cr_s = v2.KICAD_COURTYARD["RING_PAD_D5_H2.7"]
        for name, s_attach, pref in (
            ("SIG1", bs0, "P1"),
            ("SIG2", bs0, "P2"),
            ("REF", bs1, "P3"),
        ):
            _n, su, ss, wu, ws = flat_strip_box(v2, name, flat_pads[pref], s_attach)
            occupied.append(v2.Box(f"FLATSTRIP_{name}", su, ss, wu, ws, -1.0, 20.0, "floor"))
            occupied.append(
                v2.Box(f"FLATRING_{name}", flat_pads[pref][0], flat_pads[pref][1], cr_u, cr_s, -1.0, 20.0, "floor")
            )
        _cn, cu, cs, cwu, cws = charge_flat_box(v2, island, width)
        occupied.append(v2.Box("FLATSTRIP_CHARGE", cu, cs, cwu, cws, -1.0, 20.0, "floor"))
        for pref, (pu, ps) in charge_flat_pads(v2, island, width).items():
            occupied.append(v2.Box(f"FLATRING_{pref}", pu, ps, cr_u, cr_s, -1.0, 20.0, "floor"))
            occupied.append(v2.Box(f"Q97_{pref}", pu, ps, 7.0, 7.0, -1.0, 20.0, "floor"))

    # Q82: SW1 keeps the lid-recess leftover. Then holes, then J4.
    # No-receptacle: pin SW1 rot 0 low-s in the pocket (u1 clear of P4's 7×7)
    # and J2 above it, toward the cell, inside the cavity (Q91).
    if not receptacle:
        sw1_wu, sw1_ws = table["SW1"]["cr_w"], table["SW1"]["cr_h"]
        q97_u0 = charge_flat_pads(v2, island, width)["P4"][0] - 3.5
        sw1_u = min(pocket[1] - sw1_wu / 2.0, q97_u0 - 0.10 - sw1_wu / 2.0)
        sw1_u = max(sw1_u, pocket[0] + sw1_wu / 2.0)
        sw1_s = pocket[2] + sw1_ws / 2.0
        sw1_row = table["SW1"]
        sw1_h = _height(sw1_row)
        sw1_box = v2.Box("SW1", sw1_u, sw1_s, sw1_wu, sw1_ws, y_top, y_top + sw1_h, "top")
        sw1_edge_ok = True
        sw1_outline = _copper_outline_for(sw1_u, sw1_s, sw1_wu, sw1_ws, copper_island, copper_pocket)
        if sw1_outline is not None:
            sw1_edge_ok = (
                _pad_edge(v2, sw1_u, sw1_s, sw1_row["pad_w"], sw1_row["pad_h"], 0.0, sw1_outline)
                >= v2.COPPER_TO_EDGE - 1e-9
            )
        if sw1_edge_ok and not any(v2._overlap(sw1_box, o, 0.10) for o in occupied):
            add(v2._make_part("SW1", table, sw1_u, sw1_s, 0.0, "top", "lid, pocket island"), y_top, sw1_h)
        elif not try_top("SW1", [pocket_i, leftover_i, side_i], notes="lid recess"):
            missing.append("SW1")
    elif not try_top("SW1", [leftover_i, side_i], near=((leftover[0] + leftover[1]) / 2.0, (leftover[2] + leftover[3]) / 2.0), notes="lid recess"):
        if not try_top("SW1", [pocket_i], notes="lid, pocket island"):
            missing.append("SW1")

    hole_blockers = [b for b in occupied if not str(b.name).startswith("RING_")]
    sw1p = next((p for p in parts if p.ref == "SW1"), None)
    sw1_on_left = (
        sw1p is not None and _inside(sw1p.u, sw1p.s, sw1p.wu, sw1p.ws, leftover)
    )
    prefer = leftover_i if not sw1_on_left else side_i
    if prefer[1] - prefer[0] <= v2.BOSS_HOLE_KEEP or prefer[3] - prefer[2] <= v2.BOSS_HOLE_KEEP:
        prefer = side_i if not sw1_on_left else leftover_i
    if not receptacle:
        hole_sites = pin_q98_hole_sites(
            v2, leftover, hole_blockers, y0=y_air0, y1=y_top + 8.0
        )
        if len(hole_sites) < 2:
            hole_sites = find_hole_sites(
                v2, island, hole_blockers, y0=y_air0, y1=y_top + 8.0, prefer=prefer,
                min_sep=v2.BOSS_HOLE_KEEP + q98_hole_gap_need(),
            )
    else:
        hole_sites = find_hole_sites(
            v2, island, hole_blockers, y0=y_air0, y1=y_top + 8.0, prefer=prefer
        )
    for i, (hu, hs) in enumerate(hole_sites, 1):
        occupied.append(
            v2.Box(f"HOLE_M{i}", hu, hs, v2.BOSS_HOLE_KEEP, v2.BOSS_HOLE_KEEP, y_air0, y_top + 8.0, "floor")
        )
    if not receptacle:
        hole_ch = hole_channel_box(v2, hole_sites)
        if hole_ch is not None:
            cu0, cs0, cu1, cs1 = hole_ch
            occupied.append(
                v2.Box(
                    "HOLE_CH",
                    (cu0 + cu1) / 2.0,
                    (cs0 + cs1) / 2.0,
                    max(0.2, cu1 - cu0),
                    max(0.2, cs1 - cs0),
                    -1.0,
                    20.0,
                    "floor",
                )
            )

    j4_npth: tuple[tuple[float, float], ...] = ()
    j4_note = (
        "TC2030 leftover; via slot west of J4; NPTH keep-out both sides (Q85, Q98)"
        if not receptacle
        else "TC2030 leftover; keep-out is a board no-part zone"
    )
    j4_near = (bu1 - 3.5, (leftover[2] + leftover[3]) / 2.0)
    j4_margin = 0.10
    if not receptacle:
        u1p = next((p for p in parts if p.ref == "U1"), None)
        j4_wu = table["J4"]["cr_h"]  # rot 90: 4.00 × 7.00
        u_lo = (u1p.u + u1p.wu / 2.0 + Q98_CHANNEL + j4_wu / 2.0) if u1p is not None else 16.80
        via_u0 = SIG2_RUN_U + CONTACT_TRACK_W / 2.0 + CONTACT_CLEAR
        u_lo = max(u_lo, via_u0 + q98_via_slot_need() + j4_wu / 2.0)
        j4_near = (u_lo, 24.60)
        j4_margin = Q98_CHANNEL
    if try_top(
        "J4",
        [side_i, leftover_i],
        near=j4_near,
        notes=j4_note,
        step=0.2 if not receptacle else 0.4,
        margin=j4_margin,
    ):
        j4p = next(p for p in parts if p.ref == "J4")
        ch = 2.0 * Q98_CHANNEL
        occupied.append(
            v2.Box("J4_CH", j4p.u, j4p.s, j4p.wu + ch, j4p.ws + ch, y_top, y_top + 8.0, "top")
        )
        j4_npth = j4_npth_world(j4p.u, j4p.s, j4p.rot)
        if not receptacle:
            su0, ss0, su1, ss1 = j4_via_slot(j4p)
            if su1 > su0 and ss1 > ss0:
                occupied.append(
                    v2.Box(
                        "J4_VIA_SLOT",
                        (su0 + su1) / 2.0,
                        (ss0 + ss1) / 2.0,
                        su1 - su0,
                        ss1 - ss0,
                        -1.0,
                        20.0,
                        "top",
                    )
                )
            east0 = j4p.u + j4p.wu / 2.0
            occupied.append(
                v2.Box(
                    "J4_APPROACH_EAST",
                    east0 + 1.25,
                    j4p.s,
                    2.50,
                    j4p.ws + 2.0 * Q98_CHANNEL,
                    -1.0,
                    20.0,
                    "top",
                )
            )
            keep = j4_npth_keep()
            for i, (hu, hs) in enumerate(j4_npth, 1):
                occupied.append(v2.Box(f"J4_NPTH{i}", hu, hs, keep, keep, -1.0, 20.0, "top"))
    else:
        missing.append("J4")

    if not receptacle:
        j2_wu, j2_ws = table["J2"]["cr_w"], table["J2"]["cr_h"]
        j2_u = pocket[0] + j2_wu / 2.0
        j2_s = pocket[3] - j2_ws / 2.0
        j2_row = table["J2"]
        j2_h = _height(j2_row)
        j2_box = v2.Box("J2", j2_u, j2_s, j2_wu, j2_ws, y_top, y_top + j2_h, "top")
        j2_edge_ok = True
        j2_outline = _copper_outline_for(j2_u, j2_s, j2_wu, j2_ws, copper_island, copper_pocket)
        if j2_outline is not None:
            j2_edge_ok = (
                _pad_edge(v2, j2_u, j2_s, j2_row["pad_w"], j2_row["pad_h"], 0.0, j2_outline)
                >= v2.COPPER_TO_EDGE - 1e-9
            )
        j2_ok = False
        if j2_edge_ok and not any(v2._overlap(j2_box, o, 0.10) for o in occupied):
            add(
                v2._make_part(
                    "J2", table, j2_u, j2_s, 0.0, "top",
                    "JST-SH; cell connector reachable; inside cavity (Q91)",
                ),
                y_top,
                j2_h,
            )
            j2_ok = True
        if not j2_ok:
            j2_near = (pocket[0] + 3.05, pocket[3] - 3.4)
            if not try_top(
                "J2",
                [pocket_i, leftover_i, side_i],
                near=j2_near,
                notes="JST-SH; cell connector reachable; inside cavity (Q91)",
                step=0.2,
            ):
                if not try_bottom("J2", "JST-SH; cell connector reachable; second side; inside cavity (Q91)"):
                    missing.append("J2")

    if "U2" not in {p.ref for p in parts}:
        u2_pinned = False
        sw1p = next((p for p in parts if p.ref == "SW1"), None)
        if not receptacle and sw1p is not None and two_sides:
            row = table["U2"]
            h = _height(row)
            if h <= clr["air_mm"] + 1e-9:
                wu, ws = v2._rot_size(row["cr_w"], row["cr_h"], 0.0)
                pad_half = row["pad_w"] / 2.0
                u_lo = pocket[0] + v2.COPPER_TO_EDGE + pad_half
                u_hi = geom["cavity_u"][1] - CHARGE_STANDOFF - wu / 2.0 - 0.02
                u = min(max(sw1p.u, u_lo), u_hi)
                s = sw1p.s
                y0 = y_und - h
                cand = v2.Box("U2", u, s, wu, ws, y0, y0 + h, "bottom")
                edge_ok = True
                outline = _copper_outline_for(u, s, wu, ws, copper_island, copper_pocket)
                if outline is not None:
                    edge_ok = (
                        _pad_edge(v2, u, s, row["pad_w"], row["pad_h"], 0.0, outline)
                        >= v2.COPPER_TO_EDGE - 1e-9
                    )
                if edge_ok and not any(v2._overlap(cand, o, 0.10) for o in occupied):
                    add(v2._make_part("U2", table, u, s, 0.0, "bottom", "ADS1292 under SW1, second side"), y0, h)
                    second_side.append("U2")
                    u2_pinned = True
                    occupied.append(
                        v2.Box(
                            "U2_CH",
                            u,
                            s,
                            wu + 2.0 * Q98_CHANNEL,
                            ws + 2.0 * Q98_CHANNEL,
                            y_air0,
                            y_und,
                            "bottom",
                        )
                    )
        if not u2_pinned:
            if not try_top("U2", [pocket_i, leftover_i, side_i], notes="ADS1292", margin=Q98_CHANNEL if not receptacle else 0.10):
                if not try_bottom("U2", "ADS1292", margin=Q98_CHANNEL if not receptacle else 0.10):
                    missing.append("U2")
            u2p = next((p for p in parts if p.ref == "U2"), None)
            if u2p is not None and not receptacle:
                y0 = y_und - _height(table["U2"]) if u2p.face == "bottom" else y_top
                y1 = y_und if u2p.face == "bottom" else y_top + _height(table["U2"])
                occupied.append(
                    v2.Box(
                        "U2_CH",
                        u2p.u,
                        u2p.s,
                        u2p.wu + 2.0 * Q98_CHANNEL,
                        u2p.ws + 2.0 * Q98_CHANNEL,
                        y0,
                        y1,
                        u2p.face,
                    )
                )

    named = [
        ("U3", "BQ25100"),
        ("U4", "TLV71330"),
        ("J2", "JST-SH"),
        ("J3", "bench header"),
        ("D1", "PESD VBUS"),
        ("L1", "10 µH"),
        ("D2", "LED"),
    ]
    if receptacle:
        named.insert(2, ("U5", "USBLC6"))
    for q in ("Q1", "Q2", "Q3", "Q4", "Q5"):
        named.append((q, "SOT-23"))
    for ref, note in named:
        if ref in {p.ref for p in parts}:
            continue
        if ref == "U3" and not receptacle:
            if try_top(ref, top_regions, notes=note, margin=Q98_CHANNEL, step=0.2):
                u3p = next(p for p in parts if p.ref == "U3")
                occupied.append(
                    v2.Box(
                        "U3_CH",
                        u3p.u,
                        u3p.s,
                        u3p.wu + 2.0 * Q98_CHANNEL,
                        u3p.ws + 2.0 * Q98_CHANNEL,
                        y_top,
                        y_top + _height(table["U3"]),
                        "top",
                    )
                )
                continue
            if try_bottom(ref, note, margin=Q98_CHANNEL, step=0.2):
                continue
            missing.append(ref)
            continue
        if ref == "J3":
            j3_note = (
                "bench header; break-off tab, cut before closing (Q91)"
                if not receptacle
                else "bench header; pins hang off the high-u outline"
            )
            j3_near = (hang[0] + table["J3"]["cr_w"] / 2.0, (bs0 + bs1) / 2.0)
            if try_top("J3", [hang], near=j3_near, notes=j3_note):
                continue
        if ref == "J2" and receptacle:
            sidehang = (geom["cavity_u"][1] - 1.0, geom["cavity_u"][1] + 8.0, pocket[2], pocket[3])
            if try_top("J2", [sidehang, leftover_i, side_i, pocket_i], notes="JST-SH"):
                continue
        if not try_top(ref, top_regions, notes=note):
            if not try_bottom(ref, note):
                missing.append(ref)

    # R1–R3 Contact variant A: island at tab roots, not on the tab (Q79).
    tab_roots = {
        "R1": (max(bu0 + 4.5, v2.CONTACT_1[0] + 4.0), v2.CONTACT_1[1]),
        "R2": (min(bu1 - 4.5, v2.CONTACT_2[0] - 4.0), v2.CONTACT_2[1]),
        "R3": (v2.CONTACT_REF[0], bs1 - 3.0),
    }
    for ref, near in tab_roots.items():
        if not try_top(ref, [leftover, side], near=near, notes="220 kΩ variant A: island at tab root"):
            if not try_top(ref, top_regions, near=near, notes="220 kΩ variant A"):
                if not try_bottom(ref, "220 kΩ variant A, second side"):
                    missing.append(ref)

    rest = [r for r in table if r not in {p.ref for p in parts} and r[0] in "CR" and r not in skip_refs]
    rest.sort(key=lambda r: (r[0], int("".join(ch for ch in r if ch.isdigit()) or "0")))
    bot_regions = [bot_region, pocket_i] if (not receptacle and two_sides) else [bot_region]
    for ref in rest:
        if not try_top(ref, top_regions, notes="passive"):
            if not try_bottom(ref, "passive, second side", step=0.2, regions=bot_regions):
                missing.append(ref)

    still = list(missing)
    for ref in still:
        if ref in {"U1", "J1", "P1", "P2", "P3"} or ref in skip_refs:
            continue
        if try_top(ref, top_regions, notes="last-chance top", step=0.1):
            missing.remove(ref)
        elif try_bottom(ref, "last-chance second side", step=0.1, regions=bot_regions):
            missing.remove(ref)

    if edge == "process":
        _nudge_copper_parts(v2, parts, occupied, island, pocket)
        if not receptacle:
            _nudge_off_j4_npth(v2, parts, occupied, island, pocket, j4_npth)
        _clamp_courtyards_to_island(v2, parts, occupied, island)

    extra_u = (bu1 - bu0) - 15.5
    extra_s = (bs1 - bs0) - 21.6
    island_mm2 = _area(island)
    leftover_mm2 = _area(leftover) if leftover[1] > leftover[0] and leftover[3] > leftover[2] else 0.0
    top_on_island = [p for p in parts if p.face == "top" and p.ref != "J1"]
    island_used = sum(_clip_area(p.u, p.s, p.wu, p.ws, island) for p in top_on_island)
    leftover_used = sum(_clip_area(p.u, p.s, p.wu, p.ws, leftover) for p in top_on_island)
    island_fill = island_used / island_mm2 if island_mm2 else 0.0
    leftover_fill = leftover_used / leftover_mm2 if leftover_mm2 else 0.0

    by_ref = {p.ref: p for p in parts}
    rules: list[tuple[str, bool, str]] = []
    if edge == "process":
        off = []
        for p in parts:
            if p.ref in {"J1", "J3", "P1", "P2", "P3", "P4", "P5"} or p.face in {"hook", "floor", "wall"}:
                continue
            rgn = island if p.face in {"top", "bottom"} else island
            if p.face == "top" and p.s < bs0 - 0.2:
                continue
            if not _inside(p.u, p.s, p.wu, p.ws, island) and p.face != "bottom":
                # pocket is off the island
                if not _inside(p.u, p.s, p.wu, p.ws, pocket):
                    off.append(p.ref)
        rules.append(
            (
                "process-edge: courtyard inside the outline, copper-to-edge 0.30 (Q78)",
                not off and "U1" in by_ref,
                "courtyard inside the board outline; JLC 2.5 mm is the panel rail, not this outline"
                if not off and "U1" in by_ref
                else f"U1 pose missing or courtyard off outline: {', '.join(off[:8])}",
            )
        )
    else:
        body_fail = "U1" not in by_ref
        rules.append(
            (
                "body-to-outline 2.5 mm (board-v2.md §12 / L6, Q78 body reading)",
                not body_fail,
                (
                    f"U1 body 10.5×15.5 with 2.5 mm to the island {bu1-bu0:.2f}×{bs1-bs0:.2f}"
                    if not body_fail
                    else f"island {bu1-bu0:.2f}×{bs1-bs0:.2f} cannot hold U1 body + 2×2.5 mm"
                ),
            )
        )
    copper_fail = []
    for p in parts:
        if p.face not in {"top", "bottom"}:
            continue
        if p.ref in COPPER_SKIP_REFS:
            continue
        outline = _copper_outline_for(p.u, p.s, p.wu, p.ws, island, pocket)
        if outline is None:
            continue
        edge_mm = _pad_edge(v2, p.u, p.s, p.pad_w, p.pad_h, p.rot, outline)
        if edge_mm < v2.COPPER_TO_EDGE - 1e-9:
            copper_fail.append(f"{p.ref} {edge_mm:.3f}")
    rules.append(
        (
            "copper-to-edge 0.30 (board-v2.md §12)",
            not copper_fail,
            "; ".join(copper_fail[:8]) if copper_fail else "on-island pads ≥ 0.30 mm from the outline",
        )
    )
    boxes = [b for b in occupied if b.name in by_ref]
    overlaps = []
    for i, a in enumerate(boxes):
        for b in boxes[i + 1 :]:
            if v2._overlap(a, b, 0.0):
                overlaps.append(f"{a.name}/{b.name}")
    rules.append(
        (
            "courtyard-to-courtyard ≥ 0 with mask margin 0.10",
            not overlaps,
            "; ".join(overlaps[:10]) if overlaps else "no courtyard overlap among placed parts",
        )
    )
    r_on_tab = [p.ref for p in parts if p.ref in {"R1", "R2", "R3"} and p.face not in {"top", "bottom"}]
    r_ok = all(r in by_ref for r in ("R1", "R2", "R3")) and not r_on_tab
    rules.append(
        (
            "Contact variant A (Q79): R1–R3 on the island, one trace per 2.5 mm tab",
            r_ok,
            "R1 R2 R3 on the island at the tab roots" if r_ok else "R1–R3 missing or on a tab",
        )
    )
    ko_hits = []
    if poses:
        ko = occupied[-1] if occupied and occupied[-1].name == "RF_NO_COPPER" else None
        # RF box was appended just after U1; find it
        rf = next((b for b in occupied if b.name == "RF_NO_COPPER"), None)
        if rf is not None:
            for p in parts:
                if p.ref == "U1":
                    continue
                if v2._overlap(v2._part_box(p, 0.0, 1.0), rf, 0.0):
                    ko_hits.append(p.ref)
    rules.append(
        (
            "module keep-out empty",
            not ko_hits,
            f"inside RF_NO_COPPER: {', '.join(ko_hits)}" if ko_hits else "no non-U1 footprint in RF_NO_COPPER",
        )
    )
    j1 = by_ref.get("J1")
    if receptacle:
        rules.append(
            (
                "J1 USB-C on the hook-end face (Q80 / Q70)",
                j1 is not None and j1.face in {"hook", "top"},
                f"J1 at ({j1.u:.2f}, {j1.s:.2f}) {j1.face}" if j1 else "J1 not placed",
            )
        )
    else:
        p4, p5 = by_ref.get("P4"), by_ref.get("P5")
        r9r10 = "R9" not in by_ref and "R10" not in by_ref
        rules.append(
            (
                "no receptacle: J1, U5, R9 and R10 absent; P4/P5 wall pads (Q81, Q90, Q95)",
                j1 is None and "U5" not in by_ref and r9r10 and p4 is not None and p5 is not None,
                (
                    f"P4 CHARGE_VBUS ({p4.u:.2f}, {p4.s:.2f}); P5 CHARGE_GND ({p5.u:.2f}, {p5.s:.2f})"
                    if p4 and p5 and r9r10
                    else "P4/P5 missing or R9/R10 still placed"
                ),
            )
        )
        charge_hits: list[str] = []
        if p4 is not None and p5 is not None:
            cu0, cu1 = geom["cavity_u"]
            y_pad = charge_pad_y(v2)
            y_lid = 8.0
            hole_r = CHARGE_HOLE_D / 2.0
            ring_r = v2.RING_R
            ch_box = charge_flat_box(v2, island, width)
            outline = (
                ch_box[1] - ch_box[3] / 2.0,
                ch_box[1] + ch_box[3] / 2.0,
                ch_box[2] - ch_box[4] / 2.0,
                ch_box[2] + ch_box[4] / 2.0,
            )
            flats = charge_flat_pads(v2, island, width)
            for p, pref in ((p4, "P4"), (p5, "P5")):
                if p.face != "wall":
                    charge_hits.append(f"{p.ref} face {p.face} not wall")
                if abs(p.u - cu1) > 0.05:
                    charge_hits.append(f"{p.ref} u {p.u:.2f} not inner face {cu1:.2f}")
                if p.s + ring_r > CHARGE_LOFT_S + 1e-9:
                    charge_hits.append(f"{p.ref} copper s past loft")
                if p.u - CHARGE_STANDOFF < CHARGE_CELL_U1 + 1e-9:
                    charge_hits.append(f"{p.ref} standoff into the cell pocket")
                wall_floor = _wall_around_mm(y_pad, hole_r, v2.FLOOR_Y)
                wall_lid = _wall_around_mm(y_pad, hole_r, y_lid)
                wall_hook = _wall_around_mm(p.s, hole_r, CHARGE_BAY_S[0])
                if min(wall_floor, wall_lid, wall_hook) < CHARGE_WALL_AROUND - 1e-9:
                    charge_hits.append(
                        f"{p.ref} wall around seat {min(wall_floor, wall_lid, wall_hook):.2f} < {CHARGE_WALL_AROUND:g}"
                    )
                fu, fs = flats[pref]
                edge_tab = _pad_edge(v2, fu, fs, p.pad_w, p.pad_h, p.rot, outline)
                if edge_tab < v2.COPPER_TO_EDGE - 1e-9:
                    charge_hits.append(f"{p.ref} pad-to-outline {edge_tab:.3f}")
                if (
                    p.s - ring_r < HINGE_LIP_S[1] + 1e-9
                    and p.s + ring_r > HINGE_LIP_S[0] - 1e-9
                    and y_pad - ring_r < HINGE_LIP_Y[1]
                    and y_pad + ring_r > HINGE_LIP_Y[0]
                    and HINGE_LIP_U[0] <= p.u <= HINGE_LIP_U[1]
                ):
                    charge_hits.append(f"{p.ref} hits the hinge lip")
            between = math.hypot(p4.u - p5.u, p4.s - p5.s) - 2.0 * v2.RING_R
            if between < CHARGE_NYLON - 1e-9:
                charge_hits.append(f"nylon between {between:.2f} < {CHARGE_NYLON:g}")
            ss_over = []
            for p in parts:
                if p.face != "bottom":
                    continue
                for ring in (p4, p5):
                    standoff = v2.Box(
                        "standoff",
                        ring.u - CHARGE_STANDOFF / 2.0,
                        ring.s,
                        CHARGE_STANDOFF,
                        7.0,
                        y_pad - 3.5,
                        y_pad + 3.5,
                        "wall",
                    )
                    if v2._overlap(v2._part_box(p, y_und - 3.31, y_und), standoff, 0.0):
                        ss_over.append(p.ref)
            if ss_over:
                charge_hits.append("second-side over standoff: " + ", ".join(ss_over[:6]))
        rules.append(
            (
                "P4/P5 clamped button-heads in the posterior side wall (Q90, Q93)",
                p4 is not None and p5 is not None and not charge_hits,
                (
                    "; ".join(charge_hits[:8])
                    if charge_hits
                    else (
                        f"{CHARGE_WALL_NAME}; inner face u {p4.u:.2f}; "
                        f"head {CHARGE_HEAD_AXIS}; nylon \u2265 {CHARGE_NYLON:g}; "
                        f"wall around seat \u2265 {CHARGE_WALL_AROUND:g}; "
                        f"pad-to-outline \u2265 {v2.COPPER_TO_EDGE:.2f}"
                        if p4 is not None and p5 is not None
                        else "P4/P5 missing"
                    )
                ),
            )
        )
    j4 = by_ref.get("J4")
    rules.append(
        (
            "J4 TC2030 on the leftover (Q80)",
            j4 is not None and j4.face == "top",
            f"J4 at ({j4.u:.2f}, {j4.s:.2f})" if j4 else "J4 not placed",
        )
    )
    sw1 = by_ref.get("SW1")
    rules.append(
        (
            "SW1 under the lid recess",
            sw1 is not None and sw1.face == "top",
            f"SW1 at ({sw1.u:.2f}, {sw1.s:.2f})" if sw1 else "SW1 not placed",
        )
    )
    hits = []
    keep_r = v2.BOSS_HOLE_DIA / 2.0 + v2.COPPER_TO_EDGE
    hole_ok = len(hole_sites) >= 2
    for hu, hs in hole_sites:
        hole = v2.Box("hole", hu, hs, 2 * keep_r, 2 * keep_r, -1.0, 20.0, "top")
        for p in parts:
            if p.ref in {"P1", "P2", "P3", "P4", "P5"} or p.face in {"floor", "wall"}:
                continue
            if v2._overlap(v2._part_box(p, 0.0, 1.0), hole, 0.0):
                hits.append(f"{p.ref}@({hu:.2f},{hs:.2f})")
                hole_ok = False
    sw1_on_hole = False
    if sw1 is not None:
        for hu, hs in hole_sites:
            hole = v2.Box("hole", hu, hs, v2.BOSS_HOLE_KEEP, v2.BOSS_HOLE_KEEP, -1.0, 20.0, "top")
            if v2._overlap(v2._part_box(sw1, 0.0, 1.0), hole, 0.0):
                sw1_on_hole = True
    rules.append(
        (
            "two Ø2.7 island holes where courtyards allow, keep 3.30 (Q82, Q98)",
            hole_ok and not sw1_on_hole,
            (
                "; ".join(f"({hu:.2f}, {hs:.2f})" for hu, hs in hole_sites)
                + ("; SW1 overlaps a hole" if sw1_on_hole else "")
                if hole_sites
                else "no courtyard-clear site for two holes"
            ),
        )
    )
    rules.append(
        (
            "three FR4 0.2 ring pieces; ring 0.31 stays (Q72)",
            True,
            "SIG1, SIG2, REF FR4 0.2; stack 0.31; island Eco1 still 2× FR4 0.4",
        )
    )
    rules.append(
        (
            "tab fold (Q83): neck-end default; side-wall pockets only if remaining wall ≥ 1.0",
            True,
            (
                f"{fold_name}; remaining wall {wall_left:.2f} mm; "
                f"SIG1 strip {fold_nums['SIG1_strip']:.2f} mm, SIG2 strip {fold_nums['SIG2_strip']:.2f} mm"
            ),
        )
    )
    j4_bot_hits = []
    keep_r_j4 = j4_npth_keep_r()
    if not receptacle:
        for p in parts:
            if p.face != "bottom":
                continue
            if _pad_hits_j4_npth(v2, p.u, p.s, p.pad_w, p.pad_h, p.rot, j4_npth, keep_r_j4):
                j4_bot_hits.append(p.ref)
        rules.append(
            (
                "J4 NPTH keep-out both sides (Q85)",
                j4 is not None and not j4_bot_hits,
                (
                    f"{len(j4_npth)} holes, keep Ø{j4_npth_keep():.2f} mm; B.Cu pads empty"
                    if j4 is not None and not j4_bot_hits
                    else (
                        f"B.Cu pads in J4 holes: {', '.join(j4_bot_hits[:8])}"
                        if j4_bot_hits
                        else "J4 not placed"
                    )
                ),
            )
        )
    scratch = LayoutV2c(
        edge=edge, width=width, chord=chord, sides="two" if two_sides else "top",
        island=island, leftover=leftover, island_mm2=0.0, leftover_mm2=0.0,
        island_fill=0.0, leftover_fill=0.0, extra_u=0.0, extra_s=0.0, under_clear_mm=0.0,
        placed=0, missing=[], second_side=[], first_blocking="", parts=parts,
        sig1_strip=float(fold_nums["SIG1_strip"]), sig2_strip=float(fold_nums["SIG2_strip"]),
        j4_npth=j4_npth, receptacle=receptacle,
        hole_sites=tuple(hole_sites),
        j3_cut_u=(bu1 + J3_BREAK_NECK) if by_ref.get("J3") is not None else 0.0,
        j3_neck_s=(by_ref["J3"].s if "J3" in by_ref else 0.0),
    )
    fp_hits = flat_pattern_hits(v2, scratch) if not receptacle else []
    if not receptacle:
        rules.append(
            (
                "flat pattern non-overlap (Q85)",
                not fp_hits,
                (
                    "strips and flat rings clear leftover/pocket parts and each other"
                    if not fp_hits
                    else "; ".join(fp_hits[:8])
                ),
            )
        )
        cav_hits = cavity_hits(v2, scratch, geom)
        rules.append(
            (
                "cavity test: courtyards and hangs inside or declared exterior (Q91)",
                not cav_hits,
                (
                    "J2 inside; J3 on the break-off tab; P4/P5 on the wall inner face; "
                    "strips declared exterior before folding"
                    if not cav_hits
                    else "; ".join(cav_hits[:8])
                ),
            )
        )
        z_hits = q97_zone_hits(v2, scratch)
        rules.append(
            (
                "Q97 7 × 7 zones empty of other courtyards",
                not z_hits,
                "no other courtyard in a land 7×7" if not z_hits else "; ".join(z_hits[:8]),
            )
        )
        q_hits = q98_hits(v2, scratch)
        rules.append(
            (
                "Q98 routing channels: H1/H2 gap, J4 via slot, 0.6 mm around U2/U3/J4",
                not q_hits,
                (
                    f"H1/H2 keep-out gap {hole_keep_gap(hole_sites, v2.BOSS_HOLE_KEEP):.2f} mm; "
                    "via slot west of J4; 0.6 mm around U2, U3 and J4; east 0402 row clear"
                    if not q_hits
                    else "; ".join(q_hits[:8])
                ),
            )
        )
    placed_bom = sum(1 for p in parts if p.ref in required)
    rules.append(
        (
            "every required footprint placed",
            not missing and placed_bom >= bom_n,
            f"{placed_bom}/{bom_n}" if not missing else f"unplaced: {', '.join(missing)}",
        )
    )
    blocking = next((f"{n}: {why}" for n, ok, why in rules if not ok), "")
    keepouts = [("RF_NO_COPPER", *ant) if ant is not None else ("RF_NO_COPPER", 0.0, 0.0, 0.0, 0.0)]
    for i, (hu, hs) in enumerate(hole_sites, 1):
        k = v2.BOSS_HOLE_KEEP / 2.0
        keepouts.append((f"HOLE_M{i}", hu - k, hs - k, hu + k, hs + k))
    return LayoutV2c(
        edge=edge,
        width=width,
        chord=chord,
        sides="two" if two_sides else "top",
        island=island,
        leftover=leftover,
        island_mm2=island_mm2,
        leftover_mm2=leftover_mm2,
        island_fill=island_fill,
        leftover_fill=leftover_fill,
        extra_u=extra_u,
        extra_s=extra_s,
        under_clear_mm=clr["air_mm"],
        placed=placed_bom,
        missing=missing,
        second_side=second_side,
        first_blocking=blocking,
        parts=parts,
        rules=rules,
        keepouts=keepouts,
        receptacle=receptacle,
        bom_n=bom_n,
        fold=fold_name,
        wall_left=wall_left,
        hole_sites=tuple(hole_sites),
        sig1_strip=float(fold_nums["SIG1_strip"]),
        sig2_strip=float(fold_nums["SIG2_strip"]),
        j4_npth=j4_npth,
        j3_cut_u=scratch.j3_cut_u,
        j3_neck_s=scratch.j3_neck_s,
    )


def run_v2c_grid(v2: Any) -> list[LayoutV2c]:
    global _CACHE
    if _CACHE is not None:
        return list(_CACHE.values())
    table = v2.kicad_part_table()
    cache: dict[tuple, LayoutV2c] = {}
    for rec in V2C_RECEPTACLE:
        for edge in V2C_EDGES:
            for width in V2C_WIDTHS:
                for chord in V2C_CHORDS:
                    for two in (False, True):
                        key = (edge, width, chord, two, rec)
                        cache[key] = search_layout_v2c(
                            v2, edge, width, chord, two, receptacle=rec, table=table
                        )
    _CACHE = cache
    return list(cache.values())


def v2c_cell(
    v2: Any, edge: str, width: float, chord: float, two_sides: bool, receptacle: bool = True
) -> LayoutV2c:
    run_v2c_grid(v2)
    assert _CACHE is not None
    return _CACHE[(edge, width, chord, two_sides, receptacle)]


def smallest_full(
    rows: list[LayoutV2c], edge: str, *, receptacle: bool | None = True
) -> LayoutV2c | None:
    cands = [r for r in rows if r.edge == edge]
    if receptacle is not None:
        cands = [r for r in cands if r.receptacle is receptacle]
    cands = [r for r in cands if r.placed >= r.bom_n and not r.missing and not r.first_blocking]
    if not cands:
        return None
    cands.sort(key=lambda r: (0 if r.sides == "top" else 1, r.width, r.chord))
    return cands[0]


def wp12d_layout(v2: Any) -> LayoutV2c | None:
    """Smallest process-edge all-66 with receptacle that meets every rule (width 22 today)."""
    return smallest_full(run_v2c_grid(v2), "process", receptacle=True)


def wp12d_norec_layout(v2: Any) -> LayoutV2c | None:
    """Smallest process-edge all-64 with no receptacle that meets every rule (Q81; width 22 today)."""
    return smallest_full(run_v2c_grid(v2), "process", receptacle=False)


def _shortfall(lay: LayoutV2c, table: dict[str, dict[str, Any]]) -> tuple[float, list[str]]:
    leftover_parts = lay.missing
    area = 0.0
    for ref in leftover_parts:
        row = table[ref]
        area += row["cr_w"] * row["cr_h"]
    free = max(0.0, lay.leftover_mm2 * (1.0 - lay.leftover_fill))
    if lay.sides == "two":
        free += max(0.0, lay.island_mm2 * 0.5)
    return (area - free, leftover_parts)


def section_5c(v2: Any) -> list[str]:
    rows = run_v2c_grid(v2)
    table = v2.kicad_part_table()
    spec20, geom20 = v2c_geom(v2, 20.0, V2C_CHORD_AS_BUILT)
    _spec22, geom22 = v2c_geom(v2, 22.0, V2C_CHORD_AS_BUILT)
    _spec49, geom49 = v2c_geom(v2, 20.0, V2C_CHORD_M1)
    clr = under_board_clearance(v2, geom20)
    fold20 = fold_choice(v2, spec20)
    lines: list[str] = []
    lines.append("## 5c. Layout grid v2c — edge rule both ways, two sides (WP11d)")
    lines.append("")
    lines.append(
        "501012 pack only (Q69). Contact sites as in §5. Contact variant A (Q79): R1–R3 on the "
        "island at the tab roots, one Contact trace per 2.5 mm tab, no other part on a tab. "
        "J4 (TC2030) is on the leftover; its keep-out is a board no-part zone (Q80). "
        "Three FR4 0.2 ring pieces (Q72). SW1 under the lid. Module keep-out empty. "
        "Copper-to-edge 0.30. Courtyard-to-courtyard ≥ 0 with the 0.10 mask margin. "
        "Q78–Q83 are on main."
    )
    lines.append("")
    lines.append(
        "Q81: each edge/width/chord/side cell is run twice. With a receptacle, J1 USB-C stays "
        "on the hook-end face (Q80) and U5 stays. With no receptacle, J1, U5, R9 and R10 leave "
        "the BOM (64 footprints including P4/P5) and two charging pads sit as clamped button-heads "
        "in the posterior side wall (Q90). Q81 is settled on main: the build carries the "
        "no-receptacle variant (width 22, chord 47.90, two sides). USB-C on the hook-end face "
        "returns if M1 measures ≥ 58.5."
    )
    lines.append("")
    lines.append(
        "Q82: the two Ø2.7 island holes (keep 3.30) sit where the courtyards allow. The bosses "
        "follow the holes. SW1 keeps the lid-recess leftover; a hole does not take that site."
    )
    lines.append("")
    lines.append(
        f"Q83: neck-end strips are the default fold. Side-wall pockets only in a cell whose "
        f"remaining wall is ≥ {V2C_WALL_MIN:.1f} mm. At width 20 the extra 2 mm of a width-22 "
        f"body is island, not wall: remaining wall after a 0.85 mm pocket is {fold20[2]:.2f} mm "
        f"(under 1.0), so every cell in this grid uses neck-end strips "
        f"(SIG1 {fold20[1]['SIG1_strip']:.2f} mm, SIG2 {fold20[1]['SIG2_strip']:.2f} mm)."
    )
    lines.append("")
    lines.append("### Island and leftover sizes")
    lines.append("")
    lines.append(
        f"Width 20 (the shell as built): island u {geom20['board_u'][0]:.2f}–{geom20['board_u'][1]:.2f} "
        f"({geom20['board_u'][1]-geom20['board_u'][0]:.2f} mm), "
        f"s {geom20['board_s'][0]:.2f}–{geom20['board_s'][1]:.2f} "
        f"({geom20['board_s'][1]-geom20['board_s'][0]:.2f} mm)."
    )
    lines.append(
        f"Width 22: island u {geom22['board_u'][0]:.2f}–{geom22['board_u'][1]:.2f} "
        f"({geom22['board_u'][1]-geom22['board_u'][0]:.2f} mm), same s as width 20. "
        f"Island +{geom22['board_u'][1]-geom20['board_u'][1]:.2f} mm along u; leftover beside U1 grows by that amount."
    )
    lines.append(
        f"TOTAL_CHORD 47.90 is BODY_ARC 48.4 as built. TOTAL_CHORD 49.00 is the M1 gate at M1 = 52 "
        f"(TOTAL_CHORD + 3). That needs +{V2C_ARC_PLUS_M1:.2f} mm of arc. Island s1 becomes "
        f"{geom49['board_s'][1]:.2f} (+{geom49['board_s'][1]-geom20['board_s'][1]:.2f} mm of leftover along s)."
    )
    lines.append("")
    lines.append("### Under-board clearance (second side)")
    lines.append("")
    lines.append(clr["source"])
    lines.append(
        f"Second-side parts need body height ≤ {clr['air_mm']:.2f} mm. They never sit over a ring seat, "
        "a boss, a standoff or a tab root."
    )
    lines.append("")

    def _table(subset: list[LayoutV2c], heading: str) -> None:
        lines.append(f"### {heading}")
        lines.append("")
        lines.append(
            "| edge | width | chord | sides | fold | placed / N | first rule that cannot be met | "
            "island mm² | leftover mm² | holes | extra u | extra s | second side |"
        )
        lines.append("|---|---:|---:|---|---|---:|---|---:|---:|---|---:|---:|---|")
        for lay in subset:
            first = lay.first_blocking.split(":")[0] if lay.first_blocking else "—"
            ss = ", ".join(lay.second_side) if lay.second_side else "—"
            holes = (
                "; ".join(f"({hu:.2f}, {hs:.2f})" for hu, hs in lay.hole_sites)
                if lay.hole_sites
                else "—"
            )
            lines.append(
                f"| {lay.edge} | {lay.width:g} | {lay.chord:.2f} | {lay.sides} | {lay.fold} | "
                f"{lay.placed}/{lay.bom_n} | {first} | {lay.island_mm2:.1f} | {lay.leftover_mm2:.1f} | "
                f"{holes} | {lay.extra_u:+.2f} | {lay.extra_s:+.2f} | {ss} |"
            )
        lines.append("")

    rec_rows = [r for r in rows if r.receptacle]
    norec_rows = [r for r in rows if not r.receptacle]
    _table(rec_rows, "The 16 cells with USB-C receptacle (Q80)")
    _table(norec_rows, "The 16 cells with no receptacle (Q81)")

    for rec, rec_title, subset in (
        (True, "with USB-C receptacle (J1 and U5 on the BOM, 66 footprints)", rec_rows),
        (False, "with no receptacle (J1, U5, R9 and R10 off the BOM, 64 footprints, wall pads)", norec_rows),
    ):
        for edge, title in (
            ("process", "Process-edge reading (Q78)"),
            ("body", "Body-to-outline 2.5 mm reading (board-v2.md §12 / L6)"),
        ):
            lines.append(f"### {title}, {rec_title}")
            lines.append("")
            full = smallest_full(subset, edge, receptacle=rec)
            n = 66 if rec else 64
            if full is not None:
                holes = "; ".join(f"({hu:.2f}, {hs:.2f})" for hu, hs in full.hole_sites) or "—"
                lines.append(
                    f"Smallest configuration that places all {n}: width {full.width:g}, chord {full.chord:.2f}, "
                    f"sides {full.sides}, fold {full.fold}. Island {full.island[0]:.2f}–{full.island[1]:.2f} × "
                    f"{full.island[2]:.2f}–{full.island[3]:.2f}. Hole sites (Q82, for the shell bosses): {holes}."
                )
            else:
                best = max(
                    (r for r in subset if r.edge == edge),
                    key=lambda r: (r.placed, -r.width, -r.chord),
                )
                short_mm2, _left = _shortfall(best, table)
                miss_area = sum(table[r]["cr_w"] * table[r]["cr_h"] for r in best.missing)
                lines.append(
                    f"None of the eight cells places all {n}. Best is width {best.width:g}, chord {best.chord:.2f}, "
                    f"sides {best.sides}: {best.placed}/{best.bom_n}. Unplaced: "
                    f"{', '.join(best.missing) if best.missing else '—'}. "
                    f"Courtyard area still to place {miss_area:.1f} mm²; "
                    f"shortfall versus free leftover (and half the island on two sides) is {short_mm2:.1f} mm²."
                )
            lines.append("")

    w20_usb = v2c_cell(v2, "process", 20.0, V2C_CHORD_AS_BUILT, True, True)
    if w20_usb.placed >= w20_usb.bom_n and not w20_usb.missing and not w20_usb.first_blocking:
        lines.append(
            "Process-edge at width 20, chord 47.90, two sides, with a receptacle, places all 66 "
            "and meets every rule, so that cell is the WP12d pin table below."
        )
        lines.append("")
    else:
        lines.append(
            "Process-edge at width 20, chord 47.90, two sides, with a receptacle, does not place all 66 "
            f"({w20_usb.placed}/{w20_usb.bom_n}"
            + (f"; {w20_usb.first_blocking.split(':')[0]}" if w20_usb.first_blocking else "")
            + "), so WP12d takes the smallest all-66 cell that meets every rule."
        )
        lines.append("")

    proc = smallest_full(rows, "process", receptacle=True)
    if proc is not None:
        holes = "; ".join(f"({hu:.2f}, {hs:.2f})" for hu, hs in proc.hole_sites) or "—"
        lines.append(
            f"### WP12d pin table — smallest all-66 with receptacle "
            f"(width {proc.width:g}, chord {proc.chord:.2f}, {proc.sides} sides, fold {proc.fold})"
        )
        lines.append("")
        lines.append(
            "Every rule this table is checked against is met, including copper-to-edge ≥ 0.30. "
            "D1, C3, C10, C11 and C12 sit inward of the outline. "
            f"Hole sites (Q82, keep 3.30, not under U1; SW1 stays in the lid recess): {holes}. "
            "Contact sites are unchanged. The board lane pins this table within 0.1 mm"
            + (
                f" if the body grows to width {proc.width:g}."
                if proc.width > 20.0 + 1e-9
                else "."
            )
        )
        lines.append("")
        lines.extend(_placement_table(proc))
    else:
        lines.append(
            "No process-edge cell with a receptacle places all 66 under every rule, "
            "so there is no WP12d pin table."
        )
        lines.append("")

    w20_norec = v2c_cell(v2, "process", 20.0, V2C_CHORD_AS_BUILT, True, False)
    if w20_norec.placed >= w20_norec.bom_n and not w20_norec.missing and not w20_norec.first_blocking:
        lines.append(
            "Process-edge at width 20, chord 47.90, two sides, with no receptacle, places all 64 "
            "and meets every rule."
        )
        lines.append("")
    else:
        lines.append(
            "No no-receptacle cell at width 20 places the full BOM under every rule "
            f"({w20_norec.placed}/{w20_norec.bom_n}"
            + (f"; {w20_norec.first_blocking.split(':')[0]}" if w20_norec.first_blocking else "")
            + ")."
        )
        lines.append("")

    norec = smallest_full(rows, "process", receptacle=False)
    if norec is not None:
        holes = "; ".join(f"({hu:.2f}, {hs:.2f})" for hu, hs in norec.hole_sites) or "—"
        lines.append(
            f"### WP12d pin table — smallest all-64 with no receptacle "
            f"(width {norec.width:g}, chord {norec.chord:.2f}, {norec.sides} sides, fold {norec.fold})"
        )
        lines.append("")
        lines.append(
            "Q81 is settled: the build carries this cell. J1 and U5 are absent. "
            "P4 and P5 are clamped button-heads in the posterior side wall with RING_PAD_D5_H2.7 courtyards. "
            "Every rule this table is checked against is met, including copper-to-edge ≥ 0.30. "
            f"Hole sites (Q82, Q98, keep 3.30, not under U1; SW1 stays in the lid recess): {holes}. "
            f"Neck-end strips (Q83): SIG1 {norec.sig1_strip:.2f} mm, SIG2 {norec.sig2_strip:.2f} mm. "
            "Contact variant A: R1–R3 on the island. Contact sites are unchanged. "
            "The board lane pins this table within 0.1 mm"
            + (
                f" if the body grows to width {norec.width:g}."
                if norec.width > 20.0 + 1e-9
                else "."
            )
        )
        lines.append("")
        lines.extend(_placement_table(norec))
    else:
        lines.append(
            "No process-edge cell with no receptacle places all 64 under every rule, "
            "so there is no second WP12d pin table."
        )
        lines.append("")

    lines.extend(section_5d(v2, rows))
    lines.extend(section_5e(v2, rows))

    lines.append(
        "Drawings (at most four, Q56) live under `docs/fab/cad/v2c/` so the round-5 14-file "
        "`placement_v2_*.svg` set in `docs/fab/cad/v1/` stays pinned."
    )
    names = [f"`{_drawing_name(lay)}`" for lay in pick_v2c_drawings(v2)]
    if names:
        lines.append("This package keeps " + ", ".join(names) + ".")
    lines.append("")
    return lines


def _refkey(r: str) -> tuple:
    m = re.match(r"([A-Za-z]+)(\d+)", r)
    return (m.group(1), int(m.group(2))) if m else (r, 0)


def section_5d(v2: Any, rows: list[LayoutV2c]) -> list[str]:
    """WP11e–WP11f pin table v2.1. Live numbers are in §5e.

    Frozen so the board's pin-table-v2.1 parser and the shell's §5d folded-site
    parser keep working until those lanes consume §5e.
    """
    del v2, rows
    raw = Path(__file__).with_name("section_5d_v21.md").read_text(encoding="utf-8")
    lines = raw.splitlines()
    note = (
        "Pin table v2.1 and the hook-end floor P4/P5 sites are superseded by §5e "
        "(flat pattern v3, Q90–Q95). The board lane still pins this 68-row table "
        "until it consumes pin table v3. J4 NPTH keep-out both sides stays; the live "
        "hole table is in §5e."
    )
    out: list[str] = [lines[0], "", note]
    # Skip the original heading; keep the rest of the frozen v2.1 section.
    rest = lines[1:]
    while rest and rest[0] == "":
        rest = rest[1:]
    out.append("")
    out.extend(rest)
    if out[-1] != "":
        out.append("")
    return out


def section_5e(v2: Any, rows: list[LayoutV2c]) -> list[str]:
    """WP11g: flat pattern v3, pin table v3, posterior-wall P4/P5, J2 inside, J3 break-off."""
    lines: list[str] = []
    lay = smallest_full(rows, "process", receptacle=False)
    lines.append("## 5e. Flat pattern v3 and pin table v3 (WP11g, Q90–Q95, Q97, Q98)")
    lines.append("")
    if lay is None:
        lines.append(
            "No all-64 process-edge cell exists, so there is no pin table v3."
        )
        lines.append("")
        return lines
    arc = fold_arc_mm(v2)
    midplane = math.pi * (v2.BOARD_BEND_R + v2.TAB_T / 2.0)
    _u0, _u1, bs0, bs1 = lay.island
    pads = all_flat_pads(v2, lay)
    folded = folded_pad_sites(v2, lay.width, False)
    walls = charge_wall_sites(lay.width, v2)
    cr_u, cr_s = v2.KICAD_COURTYARD["RING_PAD_D5_H2.7"]
    fp_hits = flat_pattern_hits(v2, lay)
    cav_hits = cavity_hits(v2, lay)
    z_hits = q97_zone_hits(v2, lay)
    drawing = _drawing_name(lay)
    ch_allow = charge_fold_allowance(v2)
    ch_run = charge_wall_run(v2)
    ch_box = charge_flat_box(v2, lay.island, lay.width)
    p4f, p5f = pads["P4"], pads["P5"]
    p4s, p5s = charge_pad_sites(lay.width, v2)
    y_pad = charge_pad_y(v2)
    u0w, u1w = posterior_wall_u(lay.width, v2)
    L_flat = ch_allow + ch_run + CHARGE_FLAT_EXTRA
    lines.append(
        f"Build cell: process-edge, width {lay.width:g}, chord {lay.chord:.2f}, {lay.sides} sides, "
        f"fold {lay.fold}, no receptacle (Q81). Island u {lay.island[0]:.2f}–{lay.island[1]:.2f}, "
        f"s {bs0:.2f}–{bs1:.2f}. Leftover s {lay.leftover[2]:.2f}–{lay.leftover[3]:.2f}. "
        "The flex board is drawn flat. Pin table v3 below is what the board lane pins."
    )
    lines.append("")
    lines.append(
        "Posterior wall: u "
        f"{u0w:.2f}–{u1w:.2f}. montage.md §2.1: u is the posterior offset from the body's "
        "anterior edge (u = 0). shell-v2.md: the hook root sits at low u on the hook-end face "
        "and the hook curves forward over the top of the ear. params/default.toml HOOK_ROOT_X = 4.0. "
        "packing-v2.md: the hook root occupies u up to 6.39. The far wall from that root is "
        "the posterior edge hidden behind the ear, so P4/P5 go there (Q90). The anterior wall "
        "u 0–1.50 is not used. The hook-end end-face fallback is not used."
    )
    lines.append("")
    lines.append(
        f"Fold allowance: inner R {v2.BOARD_BEND_R:.1f} mm, stack {v2.TAB_T:.2f} mm "
        f"(PI {v2.FLEX:g} + FR4 {v2.STIFFENER_TAB:g}). Arc at R for a 180° SIG fold is πR = {arc:.2f} mm. "
        f"Midplane arc π(R + t/2) = {midplane:.2f} mm. Q83 strip lengths use πR, so "
        f"SIG1 {lay.sig1_strip:.2f} mm and SIG2 {lay.sig2_strip:.2f} mm stay. "
        f"The CHARGE tab uses one 90° at R {v2.BOARD_BEND_R:.1f}: πR/2 = {ch_allow:.2f} mm "
        f"plus wall run {ch_run:.2f} mm (island underside {charge_underside(v2):.2f} to pad y {y_pad:.2f})."
    )
    lines.append("")
    lines.append(
        "Flat-to-folded mapping (neck-end, Q83): each SIG strip leaves the island at "
        f"(contact u, s={bs0:.2f}) toward −s. The ring centre in PCB coordinates is "
        f"(contact u, s0 − L_flat). A 180° fold at R 1.5 at the neck puts the ring on the "
        f"floor at the contact site. REF does not take that fold: it already leaves the "
        f"island high-s end (s={bs1:.2f}) through the end-wall slot, so P3 flat = P3 folded. "
        "P4 and P5 cannot sit on that tail "
        f"(largest tail pair Ø{CHARGE_TAIL_MAX_D:g}) and they cannot sit on the skin face (Q90). "
        "The CHARGE tab leaves the pocket island's high-u edge (the inner face of the posterior "
        "wall), folds 90° at R 1.5 onto that wall's inner face, and carries RING_PAD_D5_H2.7 "
        "clamped button-heads: head through the 1.50 wall, ring on the inner face, 3.0 standoff "
        "into the bay. It does not use J2's hang and it does not use the leftover rib slot (Q92). "
        f"P4 flat ({p4f[0]:.2f}, {p4f[1]:.2f}); P5 flat ({p5f[0]:.2f}, {p5f[1]:.2f})."
    )
    lines.append("")
    lines.append("| strip | attach (u, s) | flat ring (u, s) | flat rectangle centre wu × ws | folded run | L_flat |")
    lines.append("|---|---|---|---|---:|---:|")
    attach_u = {
        "SIG1": v2.CONTACT_1[0],
        "SIG2": v2.CONTACT_2[0],
        "REF": v2.CONTACT_REF[0],
    }
    for name, pref, s_att, run in (
        ("SIG1", "P1", bs0, v2.CONTACT_1[1] - bs0),
        ("SIG2", "P2", bs0, v2.CONTACT_2[1] - bs0),
        ("REF", "P3", bs1, v2.CONTACT_REF[1] - bs1),
    ):
        _n, su, ss, wu, ws = flat_strip_box(v2, name, pads[pref], s_att)
        pu, ps = pads[pref]
        L = abs(s_att - ps)
        lines.append(
            f"| {name} | ({attach_u[name]:.2f}, {s_att:.2f}) "
            f"| ({pu:.2f}, {ps:.2f}) | ({su:.2f}, {ss:.2f}) {wu:.2f} × {ws:.2f} | {run:.2f} | {L:.2f} |"
        )
    _cn, su, ss, wu, ws = ch_box
    lines.append(
        f"| CHARGE | pocket high-u edge ({p4s[0]:.2f}, s {min(p4s[1], p5s[1]):.2f}–{max(p4s[1], p5s[1]):.2f}) "
        f"| P4 ({p4f[0]:.2f}, {p4f[1]:.2f}); P5 ({p5f[0]:.2f}, {p5f[1]:.2f}) "
        f"| ({su:.2f}, {ss:.2f}) {wu:.2f} × {ws:.2f} "
        f"| wall run {ch_run:.2f} | {L_flat:.2f} |"
    )
    lines.append("")
    if not fp_hits:
        lines.append(
            "2D check: the flat pattern does not self-overlap. No SIG, REF or CHARGE strip "
            "crosses a part on either side of the leftover or the pocket. P1–P5 flat centres "
            "sit outside every other courtyard. Neck-end is the SIG exit. Side-wall pockets "
            f"stay refused (remaining wall {lay.wall_left:.2f} mm < 1.0)."
        )
    else:
        lines.append(
            "Flat pattern self-overlap: " + "; ".join(fp_hits[:12]) + "."
        )
    lines.append("")
    if not cav_hits:
        lines.append(
            "Cavity test: every courtyard, hang and folded-board region lies inside the cavity "
            f"(u {1.50:.2f}–{lay.width - 1.50:.2f}) or on a declared exterior. Declared exteriors: "
            "the SIG strips before folding, and the J3 break-off tab. "
            f"{J3_ASSEMBLY_STEP}."
        )
    else:
        lines.append("Cavity test fails: " + "; ".join(cav_hits[:12]) + ".")
    lines.append("")
    j3p = next((p for p in lay.parts if p.ref == "J3"), None)
    j2p = next((p for p in lay.parts if p.ref == "J2"), None)
    if j2p is not None:
        lines.append(
            f"J2 (JST-SH) is inside the cavity at ({j2p.u:.2f}, {j2p.s:.2f}) rot {j2p.rot:g}; "
            "the cell connector is reachable from that site."
        )
    if j3p is not None:
        lines.append(
            f"J3 sits on a break-off tab at ({j3p.u:.2f}, {j3p.s:.2f}) rot {j3p.rot:g}, "
            f"joined by a {J3_BREAK_NECK:.1f} mm neck. Cut line at u = {lay.j3_cut_u:.2f}, "
            f"s = {lay.j3_neck_s:.2f}. {J3_ASSEMBLY_STEP}."
        )
    lines.append("")
    lines.append(
        f"Flat-pattern drawing: `docs/fab/cad/v2c/{drawing}` "
        "(strips, CHARGE rectangle, J3 cut line; at most four drawings, Q56)."
    )
    lines.append("")
    n_rows = len(list(_pin_table_v2_parts(v2, lay)))
    lines.append(
        f"### Pin table v3 — flat PCB coordinates "
        f"(width {lay.width:g}, chord {lay.chord:.2f}, {lay.sides} sides, fold {lay.fold})"
    )
    lines.append("")
    lines.append(
        f"{n_rows} rows (64 parts including P4/P5, plus H1 and H2). R9 and R10 are DNP without "
        "the receptacle (Q95); they return with the USB-C variant (Q81). Side column as in §5c. "
        "Pad-to-outline ≥ 0.30. Holes at the Q82/Q98 sites, keep 3.30; the keep-out gap "
        "takes three Default tracks. SW1 in the lid recess. "
        "Contact variant A. P1, P2, P4 and P5 are the FLAT ring centres (not the folded sites). "
        "P4 and P5 keep RING_PAD_D5_H2.7 courtyards. Second-side height ≤ "
        f"{lay.under_clear_mm:.2f} mm. Q97: no other courtyard inside a land 7 × 7 zone"
        + ("." if not z_hits else "; hits: " + "; ".join(z_hits[:6]) + ".")
        + " The board lane pins this table within 0.1 mm. The shell lane takes the wall-site table."
    )
    lines.append("")
    lines.extend(_pin_table_v2(v2, lay))
    lines.append("### Shell table — floor sites and wall sites")
    lines.append("")
    lines.append(
        "P1–P3 floor sites are unchanged from §5. y is the ring seat on the inner floor "
        f"({v2.FLOOR_Y:.2f} mm); head axis +y through the 1.50 medial wall. "
        f"P4 and P5 are clamped button-heads in the {CHARGE_WALL_NAME} "
        f"(u {u0w:.2f}–{u1w:.2f}): ring on the inner face, head through the 1.50 wall "
        f"({CHARGE_HEAD_AXIS}), 3.0 standoff into the bay. Nylon between heads ≥ {CHARGE_NYLON:g} mm. "
        f"Wall around each seat ≥ {CHARGE_WALL_AROUND:g} mm. Clear of the hinge lip "
        f"(s {HINGE_LIP_S[0]:.2f}–{HINGE_LIP_S[1]:.2f}, y {HINGE_LIP_Y[0]:.2f}–{HINGE_LIP_Y[1]:.2f}, "
        f"u {HINGE_LIP_U[0]:g}–{HINGE_LIP_U[1]:g}) and of the cell pocket "
        f"(u 1.80–{CHARGE_CELL_U1:.2f}, s {CHARGE_CELL_S[0]:.2f}–{CHARGE_CELL_S[1]:.2f})."
    )
    lines.append("")
    lines.append("| pad | net | u | s | y | wall | head axis | courtyard | notes |")
    lines.append("|---|---|---:|---:|---:|---|---|---|---|")
    nets = {
        "P1": "SIG1",
        "P2": "SIG2",
        "P3": "REF",
        "P4": "CHARGE_VBUS",
        "P5": "CHARGE_GND",
    }
    for ref, (u, s, y) in folded.items():
        if ref in walls:
            _uu, _ss, _yy, wall, axis = walls[ref]
            note = "clamped button-head; RING_PAD_D5_H2.7; 3.0 standoff into the bay (Q90)"
            lines.append(
                f"| {ref} | {nets[ref]} | {u:.2f} | {s:.2f} | {y:.2f} | {wall} | {axis} | "
                f"{cr_u:.2f} × {cr_s:.2f} | {note} |"
            )
        else:
            lines.append(
                f"| {ref} | {nets[ref]} | {u:.2f} | {s:.2f} | {y:.2f} | medial floor | +y | "
                f"{cr_u:.2f} × {cr_s:.2f} | folded seat after the neck 180° fold |"
            )
    lines.append("")
    lines.append("### Shell extras")
    lines.append("")
    lines.append(
        f"Ø5 holes through the posterior wall at the wall sites "
        f"({p4s[0]:.2f}, {p4s[1]:.2f}, y {y_pad:.2f}) and ({p5s[0]:.2f}, {p5s[1]:.2f}, y {y_pad:.2f}), "
        "head axis +u. "
        f"Rib slot s {CHARGE_RIB_S[0]:.2f}–{CHARGE_RIB_S[1]:.2f}, u {CHARGE_RIB_U[0]:.2f}–{CHARGE_RIB_U[1]:.2f}, "
        f"height {CHARGE_RIB_H:.2f} mm: unused; leave it. "
        f"Drop channel at leftover s={bs0:.2f}: unused; leave it. "
        "REF_end_wall_slot is unchanged. "
        f"Medial M2.5 well (WP14f): head at ({CHARGE_SCREW_U:.2f}, {CHARGE_SCREW_S:.2f}), "
        f"screw {CHARGE_SCREW_LEN}, tail boss OD {CHARGE_TAIL_BOSS_OD:.2f} mm "
        "(moved from 14.50, 41.00 to clear the REF pocket). "
        f"J3 break-off cut at u = {lay.j3_cut_u:.2f}. {J3_ASSEMBLY_STEP}."
    )
    lines.append("")
    _pads, drill, clr = j4_npth_spec()
    keep = j4_npth_keep()
    lines.append("### J4 NPTH keep-out both sides (Q85)")
    lines.append("")
    j4p = next((p for p in lay.parts if p.ref == "J4"), None)
    lines.append(
        f"Tag-Connect TC2030-IDC-NL from `git show {J4_KICAD_COMMIT}:hardware/board/elicio-v2.kicad_pcb`: "
        f"{len(_pads)} NPTH, drill {drill:.4f} mm. "
        f"`elicio-v2.kicad_pro` min_hole_clearance {clr:.2f} mm. "
        f"Keep-out diameter = drill + 2 × clearance = {keep:.2f} mm. "
        "KiCad canvas Y increases down; at rot 90 the map is (u + py, s − px). "
        "No B.Cu pad may enter that zone. Same-face courtyard keep-out on F.Cu stands."
    )
    lines.append("")
    lines.append("| hole | u | s | drill | keep | sides |")
    lines.append("|---|---:|---:|---:|---:|---|")
    if j4p is not None:
        for i, (hu, hs) in enumerate(lay.j4_npth, 1):
            lines.append(
                f"| J4-NPTH{i} | {hu:.3f} | {hs:.3f} | {drill:.4f} | {keep:.2f} | F.Cu and B.Cu |"
            )
    lines.append("")
    lines.append("### Routing channels (Q98)")
    lines.append("")
    gap = hole_keep_gap(lay.hole_sites, v2.BOSS_HOLE_KEEP)
    lines.append(
        "WP12h could not close 63 rats on the island and named the millimetres in "
        "route.md §12. Those channels are packing constraints. Default track 0.10 + "
        f"2 × 0.10 clearance = 0.30 mm per track; three tracks between keep-outs need "
        f"{q98_three_track_need():.2f} mm. The H1/H2 keep-out gap was 1.20 mm; it is now "
        f"{gap:.2f} mm (0.12 more plus {Q98_GAP_MARGIN:.2f} mm margin). The shell's bosses "
        "follow H1/H2. The J4 via slot sits beside J4 on the west face, east of the locked "
        "SIG2 run at u 13.50 (west of that run is U1 copper). The east 0402 row (R16 and "
        "neighbours) stays out of that approach and out of the J4 holes. A 0.6 mm channel "
        "stays free on both sides around U2, U3 and J4 (U2/SW1 may share XY on opposite "
        "faces). The board tests this table."
    )
    lines.append("")
    lines.append("| name | u_min | s_min | u_max | s_max | note |")
    lines.append("|---|---:|---:|---:|---:|---|")
    for name, u0, s0, u1, s1, note in q98_channel_boxes(v2, lay):
        lines.append(
            f"| {name} | {u0:.3f} | {s0:.3f} | {u1:.3f} | {s1:.3f} | {note} |"
        )
    lines.append("")
    lines.append("")
    return lines


def _pin_table_v2_parts(v2: Any, lay: LayoutV2c):
    pads = all_flat_pads(v2, lay)
    remap = {"P1", "P2", "P4", "P5"}
    for p in sorted(lay.parts, key=lambda x: _refkey(x.ref)):
        if p.ref in pads and p.ref in remap:
            u, s = pads[p.ref]
            note = p.notes + "; FLAT PCB (Q85); folded site in the shell table"
            wu = v2.KICAD_COURTYARD["RING_PAD_D5_H2.7"][0]
            ws = v2.KICAD_COURTYARD["RING_PAD_D5_H2.7"][1]
            yield (p.ref, p.face, u, s, p.rot, wu, ws, note)
        else:
            yield (p.ref, p.face, p.u, p.s, p.rot, p.wu, p.ws, p.notes)
    for i, (hu, hs) in enumerate(lay.hole_sites, 1):
        yield (
            f"H{i}",
            "both",
            hu,
            hs,
            0.0,
            v2.BOSS_HOLE_KEEP,
            v2.BOSS_HOLE_KEEP,
            "Ø2.7 island hole (Q82, Q98); keep 3.30; both sides; shell bosses follow",
        )


def _pin_table_v2(v2: Any, lay: LayoutV2c) -> list[str]:
    lines = [
        "| ref | side | u | s | rot | courtyard wu × ws | notes |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for ref, face, u, s, rot, wu, ws, notes in _pin_table_v2_parts(v2, lay):
        lines.append(
            f"| {ref} | {face} | {u:.2f} | {s:.2f} | {rot:g} | {wu:.2f} × {ws:.2f} | {notes} |"
        )
    lines.append("")
    return lines


def _placement_table(lay: LayoutV2c) -> list[str]:
    lines = [
        "| ref | side | u | s | rot | courtyard wu × ws | notes |",
        "|---|---|---:|---:|---:|---:|---|",
    ]

    def refkey(r: str) -> tuple:
        m = re.match(r"([A-Za-z]+)(\d+)", r)
        return (m.group(1), int(m.group(2))) if m else (r, 0)

    for p in sorted(lay.parts, key=lambda x: refkey(x.ref)):
        lines.append(
            f"| {p.ref} | {p.face} | {p.u:.2f} | {p.s:.2f} | {p.rot:g} | "
            f"{p.wu:.2f} × {p.ws:.2f} | {p.notes} |"
        )
    lines.append("")
    return lines


def _drawing_name(lay: LayoutV2c) -> str:
    rec = "usb" if lay.receptacle else "norec"
    return f"placement_v2c_{lay.edge}_{rec}_w{lay.width:g}_c{lay.chord:.2f}_{lay.sides}.svg"


def pick_v2c_drawings(v2: Any) -> list[LayoutV2c]:
    """At most four new drawings (Q56): best/full cell per (edge × receptacle)."""
    rows = run_v2c_grid(v2)
    picked: list[LayoutV2c] = []
    for rec in (True, False):
        for edge in V2C_EDGES:
            full = smallest_full(rows, edge, receptacle=rec)
            if full is not None:
                picked.append(full)
            else:
                group = [r for r in rows if r.edge == edge and r.receptacle is rec]
                picked.append(max(group, key=lambda r: (r.placed, -r.width, -r.chord)))
    return picked[:4]


def write_v2c_drawings(v2: Any, dest_dir: Path | None = None) -> list[Path]:
    dest = dest_dir or V2C_DRAW_DIR
    dest.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for lay in pick_v2c_drawings(v2):
        path = dest / _drawing_name(lay)
        path.write_text(_svg_for(lay), encoding="utf-8")
        written.append(path)
    return written


def _svg_for(lay: LayoutV2c) -> str:
    u0, u1, s0, s1 = lay.island
    pad = 8.0
    by = {p.ref: p for p in lay.parts}
    extra_s = []
    extra_hi = [s1]
    extra_u = [u1, 22.0]
    extra_u_lo = [u0, -6.0]
    if "J3" in by:
        j3 = by["J3"]
        extra_u.append(j3.u + j3.wu / 2.0)
        extra_s.append(j3.s - j3.ws / 2.0)
        extra_hi.append(j3.s + j3.ws / 2.0)
    if "P1" in by:
        extra_s.append(s0 - lay.sig1_strip)
    if "P2" in by:
        extra_s.append(s0 - lay.sig2_strip)
    ch_pads = {}
    ch_box = None
    if "P4" in by and "P5" in by:
        ch_pads = charge_flat_pads(None, lay.island, lay.width)
        ch_box = charge_flat_box(None, lay.island, lay.width)
        _n, cu, cs, cwu, cws = ch_box
        extra_s.append(cs - cws / 2.0)
        extra_hi.append(cs + cws / 2.0)
        extra_u.append(cu + cwu / 2.0)
        extra_u_lo.append(cu - cwu / 2.0)
        for fu, fs in ch_pads.values():
            extra_s.append(fs - 3.20)
            extra_hi.append(fs + 3.20)
            extra_u.append(fu + 3.20)
            extra_u_lo.append(fu - 3.20)
    min_u, max_u = min(extra_u_lo) - pad, max(extra_u) + pad
    min_s, max_s = min(s0, -8.0, *extra_s) - pad, max(extra_hi) + pad
    w, h = max_u - min_u, max_s - min_s
    scale = 12.0
    sw, sh = w * scale, h * scale

    def xy(u: float, s: float) -> tuple[float, float]:
        return ((u - min_u) * scale, (max_s - s) * scale)

    def rect(u: float, s: float, wu: float, ws: float, fill: str, stroke: str = "#222") -> str:
        x, y = xy(u - wu / 2.0, s + ws / 2.0)
        return (
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{wu*scale:.1f}" height="{ws*scale:.1f}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="0.7"/>'
        )

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{sw:.0f}" height="{sh:.0f}" '
        f'viewBox="0 0 {sw:.1f} {sh:.1f}">',
        f"<title>v2c {lay.edge} {'usb' if lay.receptacle else 'norec'} w{lay.width:g} c{lay.chord:.2f} {lay.sides} {lay.placed}/{lay.bom_n}</title>",
        '<rect width="100%" height="100%" fill="#f7f4ef"/>',
    ]
    x0, y0 = xy(u0, s1)
    parts.append(
        f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{(u1-u0)*scale:.1f}" height="{(s1-s0)*scale:.1f}" '
        f'fill="#fff" stroke="#111" stroke-width="1.2"/>'
    )
    if ch_box is not None:
        _n, cu, cs, cwu, cws = ch_box
        parts.append(rect(cu, cs, cwu, cws, "#fff7e8", "#a67c00"))
        for name, pu, ps, pwu, pws in charge_path_boxes(None, lay.island, lay.width):
            parts.append(rect(pu, ps, pwu, pws, "#f3d27a", "#a67c00"))
        for ref, (fu, fs) in ch_pads.items():
            parts.append(rect(fu, fs, 6.40, 6.40, "#c45c26", "#7a2e0b"))
            tx, ty = xy(fu, fs)
            parts.append(
                f'<text x="{tx:.1f}" y="{ty:.1f}" font-size="7" text-anchor="middle" fill="#fff">{ref}flat</text>'
            )
    if lay.fold == "neck" and "P1" in by and "P2" in by:
        for ref, length in (("P1", lay.sig1_strip), ("P2", lay.sig2_strip)):
            p = by[ref]
            fu, fs = p.u, s0 - length
            parts.append(rect(fu, (s0 + fs) / 2.0, 2.5, abs(s0 - fs), "#f3d27a", "#a67c00"))
            parts.append(rect(fu, fs, 6.40, 6.40, "#c45c26", "#7a2e0b"))
            tx, ty = xy(fu, fs)
            parts.append(
                f'<text x="{tx:.1f}" y="{ty:.1f}" font-size="7" text-anchor="middle" fill="#fff">{ref}flat</text>'
            )
        if "P3" in by:
            p3 = by["P3"]
            parts.append(rect(p3.u, (s1 + p3.s) / 2.0, 2.5, abs(s1 - p3.s), "#f3d27a", "#a67c00"))
    colors = {"top": "#6b4c9a", "bottom": "#2a6f97", "hook": "#c45c26", "floor": "#888", "wall": "#c45c26"}
    for p in lay.parts:
        parts.append(rect(p.u, p.s, p.wu, p.ws, colors.get(p.face, "#999"), "#111"))
        tx, ty = xy(p.u, p.s)
        parts.append(
            f'<text x="{tx:.1f}" y="{ty:.1f}" font-size="7" text-anchor="middle" fill="#fff">{p.ref}</text>'
        )
    for hu, hs in lay.hole_sites:
        parts.append(rect(hu, hs, 3.30, 3.30, "#f7f4ef", "#b33"))
    if not lay.receptacle:
        for name, u0, s0, u1, s1, _note in q98_channel_boxes(None, lay):
            cu, cs = (u0 + u1) / 2.0, (s0 + s1) / 2.0
            parts.append(rect(cu, cs, max(0.2, u1 - u0), max(0.2, s1 - s0), "none", "#2a6f97"))
    for i, (hu, hs) in enumerate(lay.j4_npth, 1):
        parts.append(rect(hu, hs, j4_npth_keep(), j4_npth_keep(), "none", "#b33"))
    if lay.j3_cut_u > 0.0 and "J3" in by:
        j3 = by["J3"]
        x1, y1 = xy(lay.j3_cut_u, j3.s + max(j3.ws, J3_BREAK_NECK) / 2.0 + 1.0)
        x2, y2 = xy(lay.j3_cut_u, j3.s - max(j3.ws, J3_BREAK_NECK) / 2.0 - 1.0)
        parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="#b33" stroke-width="1.4" stroke-dasharray="4 3"/>'
        )
        tx, ty = xy(lay.j3_cut_u, j3.s)
        parts.append(
            f'<text x="{tx + 4:.1f}" y="{ty:.1f}" font-size="8" fill="#b33">CUT</text>'
        )
    parts.append(
        f'<text x="12" y="16" font-size="11" fill="#111">{lay.edge} {"usb" if lay.receptacle else "norec"} '
        f"w{lay.width:g} chord {lay.chord:.2f} {lay.sides} {lay.placed}/{lay.bom_n} fold {lay.fold}</text>"
    )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"
