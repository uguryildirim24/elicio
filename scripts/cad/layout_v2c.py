"""WP11d layout v2c: edge rule both ways, two widths, two chords, two sides.

Loaded by placement_v2 at publish time. The 864-run table and §5b stay.
"""
from __future__ import annotations

import math
import re
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
# Q81: two charging pads on the tail (same RING_PAD construction as the EMG domes).
CHARGE_PAD_S = 44.00
# WP12d pin table: these five sit inward so copper-to-edge is ≥ 0.30.
NUDGE_COPPER_REFS = ("D1", "C3", "C10", "C11", "C12")
COPPER_SKIP_REFS = {"J1", "J2", "J3", "P1", "P2", "P3", "P4", "P5"}

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
            while uu <= u_hi + 1e-9 and n_u < 60:
                ss = s_lo
                if near is not None and n_u == 0:
                    ss = min(max(near[1], s_lo), s_hi)
                n_s = 0
                while ss <= s_hi + 1e-9 and n_s < 60:
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


def charge_pad_sites(width: float) -> tuple[tuple[float, float], tuple[float, float]]:
    """Q81: two tail-end charging pads, in the side walls, clear of REF at (8.5, 43)."""
    return ((0.75, CHARGE_PAD_S), (width - 0.75, CHARGE_PAD_S))


def find_hole_sites(
    v2: Any,
    island: tuple[float, float, float, float],
    occupied: list[Any],
    *,
    y0: float,
    y1: float,
    prefer: tuple[float, float, float, float] | None = None,
    step: float = 0.5,
) -> list[tuple[float, float]]:
    """Q82: two Ø2.7 holes (keep 3.30) where courtyards allow. Prefer not leftover."""
    bu0, bu1, bs0, bs1 = island
    ku = v2.BOSS_HOLE_KEEP
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
                if all(math.hypot(uu - hu, ss - hs) >= ku + 1.0 for hu, hs in found):
                    found.append((uu, ss))
                ss += step
            uu += step

    if prefer is not None and prefer[1] - prefer[0] > ku and prefer[3] - prefer[2] > ku:
        try_region(prefer)
    try_region(island)
    return found


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
    skip_refs = set() if receptacle else {"J1", "U5"}
    bom_n = len(table) - len(skip_refs)
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
        for i, site in enumerate(charge_pad_sites(width), 1):
            occupied.append(v2.Box(f"RING_CHG{i}", site[0], site[1], 7.0, 7.0, y_air0, y_top + 8.0, "floor"))

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
        for ref, site, note in (
            ("P4", charge_pad_sites(width)[0], "CHARGE_VBUS tail pad (Q81)"),
            ("P5", charge_pad_sites(width)[1], "CHARGE_GND tail pad (Q81)"),
        ):
            add(
                v2.LayoutPart(
                    ref, "RING_PAD_D5_H2.7", site[0], site[1], 0.0,
                    cr[0], cr[1], pad[0], pad[1], cr[0], cr[1], "floor", note,
                ),
                v2.FLOOR_Y,
                v2.TAB_T,
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

    def try_top(ref: str, regions: list, near=None, notes="") -> bool:
        row = table[ref]
        h = _height(row)
        found = _v2c_find(
            v2, ref, sizes_for(ref), h, y_top, "top", regions, occupied, near=near,
            pad=(row["pad_w"], row["pad_h"]), island=copper_island, pocket=copper_pocket,
        )
        if found is None:
            return False
        placed, rot = found
        add(v2._make_part(ref, table, placed.u, placed.s, rot, "top", notes), y_top, h)
        return True

    def try_bottom(ref: str, notes="") -> bool:
        if not two_sides:
            return False
        row = table[ref]
        h = _height(row)
        if h > clr["air_mm"] + 1e-9:
            return False
        y0 = y_und - h
        found = _v2c_find(
            v2, ref, sizes_for(ref), h, y0, "bottom", [bot_region], occupied, step=0.4,
            pad=(row["pad_w"], row["pad_h"]), island=copper_island, pocket=copper_pocket,
        )
        if found is None:
            return False
        placed, rot = found
        add(v2._make_part(ref, table, placed.u, placed.s, rot, "bottom", notes or "second side"), y0, h)
        second_side.append(ref)
        return True

    # Q82: SW1 keeps the lid-recess leftover. Then holes, then J4.
    if not try_top("SW1", [leftover_i, side_i], near=((leftover[0] + leftover[1]) / 2.0, (leftover[2] + leftover[3]) / 2.0), notes="lid recess"):
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
    hole_sites = find_hole_sites(
        v2, island, hole_blockers, y0=y_air0, y1=y_top + 8.0, prefer=prefer
    )
    for i, (hu, hs) in enumerate(hole_sites, 1):
        occupied.append(
            v2.Box(f"HOLE_M{i}", hu, hs, v2.BOSS_HOLE_KEEP, v2.BOSS_HOLE_KEEP, y_air0, y_top + 8.0, "floor")
        )

    if try_top("J4", [leftover_i, side_i], near=(bu1 - 3.5, (leftover[2] + leftover[3]) / 2.0), notes="TC2030 leftover; keep-out is a board no-part zone"):
        j4p = next(p for p in parts if p.ref == "J4")
        occupied.append(v2.Box("J4_keepout", j4p.u, j4p.s, j4p.wu + 1.0, j4p.ws + 1.0, y_top, y_top + 8.0, "top"))
    else:
        missing.append("J4")

    if "U2" not in {p.ref for p in parts}:
        if not try_top("U2", [pocket_i, leftover_i, side_i], notes="ADS1292"):
            if not try_bottom("U2", "ADS1292"):
                missing.append("U2")

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
        if ref == "J3":
            if try_top("J3", [hang], notes="bench header; pins hang off the high-u outline"):
                continue
        if ref == "J2":
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
    for ref in rest:
        if not try_top(ref, top_regions, notes="passive"):
            if not try_bottom(ref, "passive, second side"):
                missing.append(ref)

    still = list(missing)
    for ref in still:
        if ref in {"U1", "J1", "P1", "P2", "P3"} or ref in skip_refs:
            continue
        if try_top(ref, top_regions, notes="last-chance top"):
            missing.remove(ref)
        elif try_bottom(ref, "last-chance second side"):
            missing.remove(ref)

    if edge == "process":
        _nudge_copper_parts(v2, parts, occupied, island, pocket)

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
            if p.ref in {"J1", "J2", "J3", "P1", "P2", "P3", "P4", "P5"} or p.face in {"hook", "floor"}:
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
        rules.append(
            (
                "no receptacle: J1 and U5 absent, two tail charging pads (Q81)",
                j1 is None and "U5" not in by_ref and p4 is not None and p5 is not None,
                (
                    f"P4 CHARGE_VBUS ({p4.u:.2f}, {p4.s:.2f}); P5 CHARGE_GND ({p5.u:.2f}, {p5.s:.2f})"
                    if p4 and p5
                    else "P4/P5 missing"
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
            if p.ref in {"P1", "P2", "P3", "P4", "P5"} or p.face == "floor":
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
            "two Ø2.7 island holes where courtyards allow, keep 3.30 (Q82)",
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
    placed_bom = sum(1 for p in parts if p.ref in table and p.ref not in skip_refs)
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
        "on the hook-end face (Q80) and U5 stays. With no receptacle, J1 and U5 leave the BOM "
        "(64 footprints) and two charging pads sit on the tail end (same RING_PAD Ø5 as the EMG "
        "domes, VBUS and GND). Growing the body to M1 ≥ 58.3 seats USB-C inside; dropping the "
        "receptacle is the other reading until Rolf measures M1."
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
        (False, "with no receptacle (J1 and U5 off the BOM, 64 footprints, two tail pads)", norec_rows),
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

    w20_norec_ok = [
        r
        for r in rows
        if (not r.receptacle)
        and r.edge == "process"
        and abs(r.width - 20.0) < 1e-9
        and r.placed >= r.bom_n
        and not r.missing
        and not r.first_blocking
    ]
    if w20_norec_ok:
        norec20 = min(w20_norec_ok, key=lambda r: (0 if r.sides == "top" else 1, r.chord))
        holes = "; ".join(f"({hu:.2f}, {hs:.2f})" for hu, hs in norec20.hole_sites) or "—"
        lines.append(
            f"### WP12d pin table — no-receptacle cell at width 20 that places the full BOM "
            f"(chord {norec20.chord:.2f}, {norec20.sides} sides, fold {norec20.fold})"
        )
        lines.append("")
        lines.append(
            "J1 and U5 are absent. P4 and P5 are the tail charging pads (Q81). "
            "Every rule this table is checked against is met, including copper-to-edge ≥ 0.30. "
            f"Hole sites (Q82, not under U1): {holes}."
        )
        lines.append("")
        lines.extend(_placement_table(norec20))
    else:
        lines.append(
            "No no-receptacle cell at width 20 places the full BOM under every rule, "
            "so there is no second WP12d pin table from width 20."
        )
        lines.append("")

    lines.append(
        "Drawings (at most four, Q56) live under `docs/fab/cad/v2c/` so the round-5 14-file "
        "`placement_v2_*.svg` set in `docs/fab/cad/v1/` stays pinned."
    )
    names = [f"`{_drawing_name(lay)}`" for lay in pick_v2c_drawings(v2)]
    if names:
        lines.append("This package keeps " + ", ".join(names) + ".")
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
    min_u, max_u = min(u0, -6.0) - pad, max(u1, 22.0) + pad
    min_s, max_s = min(s0, -8.0) - pad, max(s1, 50.0) + pad
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
    colors = {"top": "#6b4c9a", "bottom": "#2a6f97", "hook": "#c45c26", "floor": "#888"}
    for p in lay.parts:
        parts.append(rect(p.u, p.s, p.wu, p.ws, colors.get(p.face, "#999"), "#111"))
        tx, ty = xy(p.u, p.s)
        parts.append(
            f'<text x="{tx:.1f}" y="{ty:.1f}" font-size="7" text-anchor="middle" fill="#fff">{p.ref}</text>'
        )
    for hu, hs in lay.hole_sites:
        parts.append(rect(hu, hs, 3.30, 3.30, "#f7f4ef", "#b33"))
    parts.append(
        f'<text x="12" y="16" font-size="11" fill="#111">{lay.edge} {"usb" if lay.receptacle else "norec"} '
        f"w{lay.width:g} chord {lay.chord:.2f} {lay.sides} {lay.placed}/{lay.bom_n} fold {lay.fold}</text>"
    )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"
