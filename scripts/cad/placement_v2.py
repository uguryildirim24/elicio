"""WP11 packing v2: arch A/B, interfaces I and II, cell, series/stacked.

Interface I: no springs, no pins. Board underside on brass standoff tops.
Interface II: flex tabs under the standoffs (fallback). Analysis only.
"""
from __future__ import annotations

import hashlib
import html
import importlib.util
import io
import math
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

# ---------------------------------------------------------------------------
# Numbers taken as given (sources in packing-v2.md and the WP11 report).
# ---------------------------------------------------------------------------

ARCHES = ("A", "B", "C")  # C is out (turn 02); kept so an explicit spec can fail
ARCHES_RUN = ("A", "B")
CELLS = ("dtp", "501015")
LAYOUTS = ("series", "stacked")
WIDTHS = (18.0, 19.0, 20.0)
LID_YS = (6.0, 6.5, 7.0, 8.0, 8.5, 9.0)
ARC_STEPS = (0.0, 1.5, 3.0)
IFACES = ("I", "II")
STANDOFFS = (3.0, 3.5)

WALL = 1.5
SIDE_CLEAR = 0.75
END_CLEAR = 0.3
FLOOR_Y = 1.5
PATH_BODY_ARC = 48.4
CREASE_BOW = 3.0
M1_DEFAULT = 52.0  # default.toml; Q34 is blank
RIB_S0 = 17.5
RIB_THICK = 0.8
CAVITY_S0 = 1.5
CAVITY_S1_V1 = 38.2
BOARD_S0_V1 = 18.6
BOARD_S1_V1 = 37.6
CONTACT_1 = (5.9, 22.0)
CONTACT_2 = (10.4, 33.1)
CONTACT_REF = (8.5, 43.0)
KEEPOUT_R = 3.55
COPPER_FREE = 0.5
KEEPOUT_MARGIN_R = KEEPOUT_R + COPPER_FREE
POCKET_DIA = 7.5
ANTENNA_CELL_MIN = 5.0
CLAMP_MAX = 10.0
RASTER = 0.25  # mm; packing mask, not v1's 0.025 (108 runs)

# Flex tab + nut + screw (plan v2 §3, brief).
TAB_T = 0.2
TAB_W = 2.5
RING_D = 5.0
RING_R = RING_D / 2.0
RING_HOLE = 2.7
BEND_R = 1.0
NUT_M = 1.6  # DIN 439 / ISO 4035 M2.5
NUT_S = 5.0
SCREW_L = 4.0  # ISO 7380 M2.5×4, tip at y=SCREW_L from the medial face
TIP_PAST_NUT = SCREW_L - WALL - TAB_T - NUT_M  # 0.70
STACK_INSIDE = TAB_T + NUT_M + TIP_PAST_NUT  # 2.50
STACK_TOP_Y = FLOOR_Y + STACK_INSIDE  # 4.00
KEEPOUT_TOP_Y = 4.13  # v1 keep-out air; parts above this may overlap in plan

FLEX = 0.11
STIFFENER = 0.3
BOARD_AT_PARTS = 0.4  # Interface II: 0.11 + 0.3
BOARD_AT_TABS = 0.2
BOARD_RIGID = 1.0  # Interface I: FR4 4-layer, plan v2 §5.2
FOAM = 0.3

# Interface I landing (turn 07; coordinator note 3). Heights are above the
# inner floor. Board underside = FLOOR_Y + standoff. Bosses 0.5 lower.
STANDOFF_AF = 5.0  # across flats, M2.5 hex
STANDOFF_CIRCUMR = 2.9  # coordinator: 5/√3 ≈ 2.887, stated 2.9
PAD_XY = 8.0
PAD_HALF = PAD_XY / 2.0
PLACEMENT_TOL = 0.3  # JLC printed floor ±0.3, turn 07 G7
BOSS_DROP = 0.5
BOSS_DIA = 5.0
HARNESS_RESERVE = (8.0, 6.0, 2.0)  # coil/service loop; 100 mm length is NOT_MEASURED
SWITCH = (4.5, 4.5, 1.6)  # recovery, board top (coordinator note 3)
HEADER = (7.6, 2.5, 2.5)  # 3-pin 2.54 mm right-angle, plan v2 §5.6
USB_OPENING = (9.0, 3.5)
USB_RECESS = 1.0
USB_LIGAMENT = 1.5
PLUG_VOLUME = (12.0, 6.5, 15.0)  # in front of the opening, plan v2 §5.4
HOOK_ROOT_S = 0.0

# Modules. A: Raytac Spec K / plan v2 §3 reserve 2.3. B: Ebyte 13×18×2.0.
# C: out (turn 02). Antenna for B: sheet unreachable, v1 12.4 × 3.8.
MODULE = {
    "A": {"name": "Raytac MDBT50Q-1MV2", "w": 10.5, "l": 15.5, "h": 2.3,
          "ant": (12.4, 3.8), "ant_from": "Raytac Spec K p.9/p.13, interface §6.3; height 2.3 plan v2 §3"},
    "B": {"name": "Ebyte E73-2G4M08S1C", "w": 13.0, "l": 18.0, "h": 2.0,
          "ant": (12.4, 3.8), "ant_from": "sheet unreachable; v1 rule interface §6.3"},
    "C": {"name": "Seeed XIAO nRF52840", "w": 17.5, "l": 21.0, "h": 4.5,
          "pcb": 1.2, "usb_overhang": 1.48, "ant": (12.4, 3.8),
          "ant_from": "sheet unreachable; v1 rule interface §6.3; C is out"},
}
CELL = {
    "dtp": {"name": "DTP301120", "t": 3.2, "w": 11.5, "l": 22.0,
            "from": "SparkFun PRT-25270 drawing p.9, L5-research-v2.md §1"},
    "501015": {"name": "501015", "t": 5.2, "w": 10.4, "l": 15.6,
               "from": "v1 CELL_BODY_MAX; plan v2 §3 quotes 5.4 thick"},
}

VQFN = (5.0, 5.0, 1.0)  # brief; v1 packing courtyard was 4.60
ARRAY = (2.65, 2.35, 1.2)
BQ = (2.10, 1.40, 0.5)
LDO = (1.50, 1.50, 1.2)
JST = (4.0, 6.0, 2.9)
USB = (8.9, 7.3, 3.2)
R0402 = (1.80, 0.90)
N_0402 = 25
N_SWD = 5
SWD = (1.0, 1.0)
N_ARRAYS = 2

ROOT = Path(__file__).resolve().parents[2]
V2_DRAW_DIR = ROOT / "docs" / "fab" / "cad" / "v1"


def _placement():
    for name in ("elicio_cad_placement", "elicio_placement"):
        mod = sys.modules.get(name)
        if mod is not None and hasattr(mod, "chord_from_arc_bow"):
            return mod
    main = sys.modules.get("__main__")
    if main is not None and hasattr(main, "chord_from_arc_bow"):
        return main
    path = Path(__file__).with_name("placement.py")
    spec = importlib.util.spec_from_file_location("elicio_cad_placement", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules["elicio_cad_placement"] = mod
    spec.loader.exec_module(mod)
    return mod


@dataclass(frozen=True, slots=True)
class V2Spec:
    arch: str
    cell: str
    layout: str
    width: float
    lid_y: float
    arc_plus: float = 0.0
    iface: str = "I"
    standoff: float = 3.5

    def __post_init__(self) -> None:
        if self.arch not in ARCHES:
            raise ValueError(f"arch must be A|B|C, got {self.arch!r}")
        if self.cell not in CELLS:
            raise ValueError(f"cell must be dtp|501015, got {self.cell!r}")
        if self.layout not in LAYOUTS:
            raise ValueError(f"layout must be series|stacked, got {self.layout!r}")
        if self.width not in WIDTHS:
            raise ValueError(f"width must be 18|19|20, got {self.width!r}")
        if self.lid_y not in LID_YS:
            raise ValueError(f"lid-y must be 6.0–9.0 in 0.5 steps, got {self.lid_y!r}")
        if self.arc_plus not in ARC_STEPS:
            raise ValueError(f"arc-plus must be 0|1.5|3.0, got {self.arc_plus!r}")
        if self.iface not in IFACES:
            raise ValueError(f"iface must be I|II, got {self.iface!r}")
        if self.standoff not in STANDOFFS:
            raise ValueError(f"standoff must be 3.0|3.5, got {self.standoff!r}")

    @property
    def tag(self) -> str:
        w = f"{self.width:.0f}"
        y = f"{self.lid_y:g}"
        s = f"{self.standoff:g}"
        base = f"{self.arch}_{self.cell}_{self.layout}_w{w}_y{y}_i{self.iface}_s{s}"
        if self.arc_plus:
            return f"{base}_a{self.arc_plus:g}"
        return base

    @property
    def filename(self) -> str:
        return f"placement_v2_{self.tag}.svg"

    @property
    def adjustment_region(self) -> float:
        """Pad half-size − standoff circumradius − placement tolerance."""
        return PAD_HALF - STANDOFF_CIRCUMR - PLACEMENT_TOL


@dataclass(frozen=True, slots=True)
class Box:
    name: str
    u: float
    s: float
    wu: float
    ws: float
    y0: float
    y1: float
    face: str  # "top" | "bottom" | "floor"

    @property
    def u0(self) -> float:
        return self.u - self.wu / 2.0

    @property
    def u1(self) -> float:
        return self.u + self.wu / 2.0

    @property
    def s0(self) -> float:
        return self.s - self.ws / 2.0

    @property
    def s1(self) -> float:
        return self.s + self.ws / 2.0

    def as_tuple(self) -> tuple[float, float, float, float]:
        return (self.u, self.s, self.wu, self.ws)


@dataclass(frozen=True, slots=True)
class TabPath:
    name: str
    points: tuple[tuple[float, float], ...]
    width: float = TAB_W
    thick: float = TAB_T


@dataclass
class V2Result:
    spec: V2Spec
    body_arc: float
    cavity_u: tuple[float, float]
    cavity_s: tuple[float, float]
    board_u: tuple[float, float]
    board_s: tuple[float, float]
    rib_s: tuple[float, float]
    board_underside: float
    board_top: float
    total_chord: float
    m1_gate: float
    free_mm2: float
    parts: dict[str, Box] = field(default_factory=dict)
    tabs: dict[str, TabPath] = field(default_factory=dict)
    antenna: tuple[float, float, float, float] | None = None  # u0,s0,u1,s1
    usb_wall: str | None = None
    pocket_ref_dia: float = POCKET_DIA
    n_0402: int = 0
    adjustment_mm: float = 0.0
    board_thick: float = BOARD_RIGID
    standoff_top_y: float = 5.0
    boss_top_y: float = 4.5
    conflicts: list[str] = field(default_factory=list)

    @property
    def closes(self) -> bool:
        return not self.conflicts

    @property
    def first_conflict(self) -> str:
        return self.conflicts[0] if self.conflicts else ""


def drawing_path(spec: V2Spec) -> Path:
    return V2_DRAW_DIR / spec.filename


def body_geom(spec: V2Spec) -> dict[str, Any]:
    w = spec.width
    ds = spec.arc_plus
    cavity_u = (WALL, w - WALL)
    cavity_s = (CAVITY_S0, CAVITY_S1_V1 + ds)
    board_u = (WALL + SIDE_CLEAR, w - WALL - SIDE_CLEAR)
    cell = CELL[spec.cell]
    if spec.layout == "series":
        pocket_len = cell["l"] + 0.4
        pocket_s1 = CAVITY_S0 + pocket_len
        rib_s = (pocket_s1, pocket_s1 + RIB_THICK)
        board_s = (rib_s[1] + 0.3, BOARD_S1_V1 + ds)
        if spec.cell == "501015" and ds == 0.0:
            # v1 pocket and rib when the cell fits it.
            rib_s = (RIB_S0, RIB_S0 + RIB_THICK)
            board_s = (BOARD_S0_V1, BOARD_S1_V1 + ds)
    else:
        rib_s = (RIB_S0, RIB_S0)  # no rib; one cavity
        board_s = (CAVITY_S0 + END_CLEAR, CAVITY_S1_V1 + ds - END_CLEAR)
    if spec.iface == "I":
        # One board plane over the cavity. The cell lies under it on the floor.
        board_s = (CAVITY_S0 + END_CLEAR, CAVITY_S1_V1 + ds - END_CLEAR)
        board_underside = FLOOR_Y + spec.standoff
        board_top = board_underside + BOARD_RIGID
    elif spec.layout == "series":
        board_underside = STACK_TOP_Y
        board_top = board_underside + BOARD_AT_PARTS
    else:
        board_underside = FLOOR_Y
        board_top = board_underside + BOARD_AT_PARTS
    P = _placement()
    chord, _r = P.chord_from_arc_bow(PATH_BODY_ARC + ds, CREASE_BOW)
    return {
        "body_u": (0.0, w),
        "body_arc": PATH_BODY_ARC + ds,
        "cavity_u": cavity_u,
        "cavity_s": cavity_s,
        "board_u": board_u,
        "board_s": board_s,
        "rib_s": rib_s,
        "board_underside": board_underside,
        "board_top": board_top,
        "board_thick": board_top - board_underside,
        "standoff_top_y": FLOOR_Y + spec.standoff,
        "boss_top_y": FLOOR_Y + spec.standoff - BOSS_DROP,
        "total_chord": float(chord),
        "m1_gate": float(chord) + 3.0,
    }


def _overlap(a: Box, b: Box, margin: float = 0.0) -> bool:
    """True when two courtyards share volume (u, s and y)."""
    if a.u1 + margin <= b.u0 or b.u1 + margin <= a.u0:
        return False
    if a.s1 + margin <= b.s0 or b.s1 + margin <= a.s0:
        return False
    if a.y1 <= b.y0 + 1e-9 or b.y1 <= a.y0 + 1e-9:
        return False
    return True


def _same_level_overlap(cand: Box, other: Box, margin: float = 0.05) -> bool:
    """True when courtyards share (u,s,y) and the other is a real SMT neighbour."""
    if other.name.startswith(("standoff", "pad_", "boss")):
        return False
    if other.name.endswith("_ring") or "_seg" in other.name:
        return False
    return _overlap(cand, other, margin)


def _in_rect(
    u: float, s: float, wu: float, ws: float, u_span: tuple[float, float], s_span: tuple[float, float]
) -> bool:
    return (
        u - wu / 2.0 >= u_span[0] - 1e-9
        and u + wu / 2.0 <= u_span[1] + 1e-9
        and s - ws / 2.0 >= s_span[0] - 1e-9
        and s + ws / 2.0 <= s_span[1] + 1e-9
    )


def _circle_hits_box(cu: float, cs: float, r: float, box: Box) -> bool:
    nearest_u = min(max(cu, box.u0), box.u1)
    nearest_s = min(max(cs, box.s0), box.s1)
    return math.hypot(cu - nearest_u, cs - nearest_s) < r - 1e-9


def _tab_boxes(tab: TabPath, y0: float, y1: float) -> list[Box]:
    out: list[Box] = []
    pts = tab.points
    out.append(
        Box(f"{tab.name}_ring", pts[0][0], pts[0][1], RING_D, RING_D, y0, y1, "floor")
    )
    for i in range(len(pts) - 1):
        u0, s0 = pts[i]
        u1, s1 = pts[i + 1]
        du, ds = u1 - u0, s1 - s0
        length = math.hypot(du, ds)
        if length < 1e-9:
            continue
        mid_u, mid_s = (u0 + u1) / 2.0, (s0 + s1) / 2.0
        if abs(du) >= abs(ds):
            wu, ws = length, tab.width
        else:
            wu, ws = tab.width, length
        out.append(Box(f"{tab.name}_seg{i}", mid_u, mid_s, wu, ws, y0, y1, "floor"))
    return out


def _bend_ok(points: tuple[tuple[float, float], ...]) -> bool:
    if len(points) < 3:
        return True
    for i in range(1, len(points) - 1):
        a, b, c = points[i - 1], points[i], points[i + 1]
        v1 = (b[0] - a[0], b[1] - a[1])
        v2 = (c[0] - b[0], c[1] - b[1])
        n1 = math.hypot(*v1)
        n2 = math.hypot(*v2)
        if n1 < 1e-9 or n2 < 1e-9:
            return False
        cos_t = max(-1.0, min(1.0, (v1[0] * v2[0] + v1[1] * v2[1]) / (n1 * n2)))
        theta = math.acos(cos_t)
        need = BEND_R * math.tan(theta / 2.0) if theta < math.pi - 1e-9 else math.inf
        if n1 < need or n2 < need:
            return False
    return True


def _make_tabs(spec: V2Spec, geom: dict[str, Any]) -> dict[str, TabPath]:
    if spec.iface == "I":
        return {}
    bs0, bs1 = geom["board_s"]
    # Straight runs, no 90° jog. Bend radius is free on a straight tab.
    sig1_end_s = min(CONTACT_1[1] + 7.0, bs1 - 0.8)
    sig2_end_s = max(CONTACT_2[1] - 7.0, bs0 + 0.8)
    ref_end_s = bs1 - 0.8
    return {
        "SIG1": TabPath("SIG1", (CONTACT_1, (CONTACT_1[0], sig1_end_s))),
        "SIG2": TabPath("SIG2", (CONTACT_2, (CONTACT_2[0], sig2_end_s))),
        "REF": TabPath("REF", (CONTACT_REF, (CONTACT_REF[0], ref_end_s))),
    }


def _place_cell(spec: V2Spec, geom: dict[str, Any], module: Box | None) -> Box:
    cell = CELL[spec.cell]
    cu = geom["cavity_u"]
    mid_u = (cu[0] + cu[1]) / 2.0
    y0, y1 = FLOOR_Y, FLOOR_Y + cell["t"] + FOAM
    if spec.iface == "I" or spec.layout == "series":
        s0 = geom["cavity_s"][0]
        u = geom["cavity_u"][0] + cell["w"] / 2.0 + 0.3
        if u + cell["w"] / 2.0 > cu[1]:
            u = mid_u
        return Box(
            "cell",
            u,
            s0 + cell["l"] / 2.0,
            cell["w"],
            cell["l"],
            y0,
            y1,
            "floor",
        )
    y0m = module.y1 if module is not None else geom["board_top"]
    s = (module.s0 + cell["l"] / 2.0) if module is not None else (geom["board_s"][0] + cell["l"] / 2.0)
    u = module.u if module is not None else mid_u
    probe = Box("cell", u, s, cell["w"], cell["l"], y0m, y0m + cell["t"] + FOAM, "top")
    hits = _circle_hits_box(CONTACT_1[0], CONTACT_1[1], KEEPOUT_MARGIN_R, probe) or _circle_hits_box(
        CONTACT_2[0], CONTACT_2[1], KEEPOUT_MARGIN_R, probe
    )
    if hits:
        y0m = max(y0m, STACK_TOP_Y + 0.13)
    return Box("cell", u, s, cell["w"], cell["l"], y0m, y0m + cell["t"] + FOAM, "top")


def _orient_module(spec: V2Spec, geom: dict[str, Any]) -> tuple[float, float]:
    """Return (wu, ws). Prefer length along s; rotate if that is the only fit."""
    m = MODULE[spec.arch]
    bu = geom["board_u"][1] - geom["board_u"][0]
    bs = geom["board_s"][1] - geom["board_s"][0]
    # Prefer the pose that leaves a ≥ 5.2 mm strip along s for the VQFN.
    poses = []
    if m["l"] <= bs + 1e-6 and m["w"] <= bu + 1e-6:
        poses.append((m["w"], m["l"]))
    if m["w"] <= bs + 1e-6 and m["l"] <= bu + 1e-6:
        poses.append((m["l"], m["w"]))
    if not poses:
        return m["w"], m["l"]
    poses.sort(key=lambda p: -(bs - p[1]))
    return poses[0]


def _place_module(spec: V2Spec, geom: dict[str, Any]) -> tuple[Box, tuple[float, float, float, float]]:
    m = MODULE[spec.arch]
    wu, ws = _orient_module(spec, geom)
    bu0, bu1 = geom["board_u"]
    bs0, bs1 = geom["board_s"]
    # Pack to low-u when a ≥ 2.4 mm side strip remains (arrays, B).
    if (bu1 - bu0) - wu >= ARRAY[1] + 0.15:
        u = bu0 + wu / 2.0
    else:
        u = (bu0 + bu1) / 2.0
    if spec.layout == "stacked":
        s = bs0 + ws / 2.0 + 0.4
    else:
        s = bs1 - ws / 2.0
    y0 = geom["board_top"]
    box = Box("module", u, s, wu, ws, y0, y0 + m["h"], "top")
    aw, al = m["ant"]
    a_s1 = box.s1
    a_s0 = a_s1 - al
    a_u0 = u - aw / 2.0
    a_u1 = u + aw / 2.0
    return box, (a_u0, a_s0, a_u1, a_s1)


def _place_usb(spec: V2Spec, geom: dict[str, Any], module: Box) -> tuple[Box | None, str | None]:
    cu, cs = geom["cavity_u"], geom["cavity_s"]
    bu0, bu1 = geom["board_u"]
    bs0, bs1 = geom["board_s"]
    if spec.arch == "C":
        overhang = MODULE["C"]["usb_overhang"]
        usb_s = module.s0 - overhang / 2.0
        box = Box(
            "usb_xiao",
            module.u,
            usb_s,
            9.0,
            overhang + 0.2,
            module.y0,
            module.y1,
            "top",
        )
        wall = "hook-end wall (low-s)" if box.s0 < cs[0] + WALL else None
        if box.s1 > cs[1] - WALL:
            wall = "tail-end wall (high-s)"
        return box, wall
    # Prefer the medial face near the hook. The battery pocket sits there, so
    # the packing hangs the receptacle off the hook-end wall (fallback) when
    # the medial leftover cannot hold 8.9 × 7.3 without the cell or the module.
    wu, ws = USB[0], USB[1]
    u = (bu0 + bu1) / 2.0
    y0, y1 = USB_RECESS, USB_RECESS + USB[2]
    on_board = Box("usb_c", u, bs0 + ws / 2.0 + 0.2, wu, ws, geom["board_top"], geom["board_top"] + USB[2], "top")
    if _overlap(on_board, module):
        box = Box("usb_c", u, cs[0] - ws / 2.0, wu, ws, y0, y1, "top")
        return box, "hook-end end face (fallback)"
    box = on_board
    lig_hook = box.s0 - HOOK_ROOT_S
    nearest = min(
        math.hypot(box.u - CONTACT_1[0], box.s - CONTACT_1[1]) - KEEPOUT_R,
        math.hypot(box.u - CONTACT_2[0], box.s - CONTACT_2[1]) - KEEPOUT_R,
        math.hypot(box.u - CONTACT_REF[0], box.s - CONTACT_REF[1]) - POCKET_DIA / 2.0,
    )
    if lig_hook + 1e-9 >= USB_LIGAMENT and nearest + 1e-9 >= USB_LIGAMENT:
        wall = "medial face near hook end"
        return box, wall
    box = Box("usb_c", u, cs[0] - ws / 2.0, wu, ws, y0, y1, "top")
    return box, "hook-end end face (fallback)"


def _place_standoffs(spec: V2Spec, geom: dict[str, Any]) -> list[Box]:
    y0 = FLOOR_Y
    y1 = geom["standoff_top_y"]
    out = []
    for name, site in (("standoff_SIG1", CONTACT_1), ("standoff_SIG2", CONTACT_2), ("standoff_REF", CONTACT_REF)):
        out.append(Box(name, site[0], site[1], STANDOFF_AF, STANDOFF_AF, y0, y1, "floor"))
    return out


def _place_pads(spec: V2Spec, geom: dict[str, Any]) -> list[Box]:
    if spec.iface != "I":
        return []
    y0 = geom["board_underside"]
    y1 = geom["board_underside"]
    out = []
    for name, site in (("pad_SIG1", CONTACT_1), ("pad_SIG2", CONTACT_2), ("pad_REF", CONTACT_REF)):
        out.append(Box(name, site[0], site[1], PAD_XY, PAD_XY, y0, y1, "bottom"))
    return out


def _place_bosses(spec: V2Spec, geom: dict[str, Any], occupied: list[Box]) -> list[Box]:
    bu0, bu1 = geom["board_u"]
    bs0, bs1 = geom["board_s"]
    y0, y1 = FLOOR_Y, geom["boss_top_y"]
    candidates = [
        ("boss_1", bu0 + BOSS_DIA / 2.0 + 0.4, bs0 + BOSS_DIA / 2.0 + 0.4),
        ("boss_2", bu1 - BOSS_DIA / 2.0 - 0.4, bs1 - BOSS_DIA / 2.0 - 0.4),
    ]
    out = []
    for name, u, s in candidates:
        cand = Box(name, u, s, BOSS_DIA, BOSS_DIA, y0, y1, "floor")
        if any(_circle_hits_box(cu, cs, STANDOFF_CIRCUMR + 0.4, cand) for cu, cs in (CONTACT_1, CONTACT_2, CONTACT_REF)):
            continue
        if any(_overlap(cand, other, 0.2) for other in occupied if other.name == "cell"):
            continue
        out.append(cand)
    return out


def _place_switch_and_header(spec: V2Spec, geom: dict[str, Any], occupied: list[Box]) -> dict[str, Box]:
    y0 = geom["board_top"]
    regions = [
        (
            (geom["board_u"][0] + 0.2, geom["board_u"][1] - 0.2, geom["board_s"][0] + 0.2, geom["board_s"][1] - 0.2),
            y0,
            "top",
        )
    ]
    parts: dict[str, Box] = {}
    sw = _find_site("switch", [(SWITCH[0], SWITCH[1])], SWITCH[2], regions, occupied)
    if sw is None:
        sw = _smt_box(
            "switch",
            geom["board_u"][0] + SWITCH[0] / 2.0 + 0.3,
            geom["board_s"][0] + SWITCH[1] / 2.0 + 0.3,
            SWITCH[0],
            SWITCH[1],
            SWITCH[2],
            y0,
            "top",
        )
    parts["switch"] = sw
    occupied = occupied + [sw]
    hd = _find_site("header", [(HEADER[0], HEADER[1]), (HEADER[1], HEADER[0])], HEADER[2], regions, occupied)
    if hd is None:
        hd = _smt_box(
            "header",
            geom["board_u"][1] - HEADER[0] / 2.0 - 0.3,
            geom["board_s"][0] + HEADER[1] / 2.0 + 0.3,
            HEADER[0],
            HEADER[1],
            HEADER[2],
            y0,
            "top",
        )
    parts["header"] = hd
    return parts


def _smt_box(
    name: str, u: float, s: float, wu: float, ws: float, h: float, y0: float, face: str
) -> Box:
    return Box(name, u, s, wu, ws, y0, y0 + h, face)


def _fe_regions(
    spec: V2Spec, geom: dict[str, Any], module: Box, cell: Box
) -> list[tuple[tuple[float, float, float, float], float, str]]:
    """Return (u0,u1,s0,s1), y0, face for leftover, side strip, and pocket."""
    bu0, bu1 = geom["board_u"]
    bs0, bs1 = geom["board_s"]
    regions: list[tuple[tuple[float, float, float, float], float, str]] = []
    if spec.layout == "stacked":
        leftover = (bu0 + 0.15, bu1 - 0.15, module.s1 + 0.25, bs1 - 0.15)
    else:
        leftover = (bu0 + 0.15, bu1 - 0.15, bs0 + 0.15, min(module.s0 - 0.25, bs1) - 0.05)
    regions.append((leftover, geom["board_top"], "top"))
    # Side strip on the radio board, high-u of a low-u module.
    side = (module.u1 + 0.05, bu1, max(bs0, module.s0), min(bs1, module.s1))
    regions.append((side, geom["board_top"], "top"))
    if spec.layout == "series":
        pu0 = cell.u1 + 0.2
        pu1 = geom["cavity_u"][1] - 0.15
        ps0 = geom["cavity_s"][0] + 0.15
        ps1 = (geom["rib_s"][0] if geom["rib_s"][1] > geom["rib_s"][0] else cell.s1) - 0.15
        regions.append(((pu0, pu1, ps0, ps1), FLOOR_Y + BOARD_AT_PARTS, "pocket"))
    return regions


def _find_site(
    name: str,
    sizes: list[tuple[float, float]],
    h: float,
    regions: list[tuple[tuple[float, float, float, float], float, str]],
    occupied: list[Box],
    *,
    near: tuple[float, float] | None = None,
    step: float = 0.45,
    margin: float = 0.05,
) -> Box | None:
    def ok(cand: Box) -> bool:
        if cand.y0 < KEEPOUT_TOP_Y - 1e-9:
            if _circle_hits_box(CONTACT_1[0], CONTACT_1[1], KEEPOUT_MARGIN_R, cand):
                return False
            if _circle_hits_box(CONTACT_2[0], CONTACT_2[1], KEEPOUT_MARGIN_R, cand):
                return False
        return not any(_overlap(cand, other, margin) for other in occupied)

    ranked = list(regions)
    if near is not None:
        ranked = sorted(
            ranked,
            key=lambda r: math.hypot(
                near[0] - min(max(near[0], r[0][0]), r[0][1]),
                near[1] - min(max(near[1], r[0][2]), r[0][3]),
            ),
        )
    best: Box | None = None
    best_d = math.inf
    for (u0, u1, s0, s1), y0, face in ranked:
        if u1 - u0 < 0.5 or s1 - s0 < 0.5:
            continue
        for wu, ws in sizes:
            if wu > (u1 - u0) + 1e-9 or ws > (s1 - s0) + 1e-9:
                continue
            u_lo, u_hi = u0 + wu / 2.0, u1 - wu / 2.0
            s_lo, s_hi = s0 + ws / 2.0, s1 - ws / 2.0
            if near is not None:
                u_start = min(max(near[0], u_lo), u_hi)
                s_start = min(max(near[1], s_lo), s_hi)
            else:
                u_start, s_start = u_lo, s_lo
            u = u_start
            n_u = 0
            while u <= u_hi + 1e-9 and n_u < 50:
                s = s_start if n_u == 0 else s_lo
                n_s = 0
                while s <= s_hi + 1e-9 and n_s < 50:
                    cand = _smt_box(name, u, s, wu, ws, h, y0, face)
                    if ok(cand):
                        if near is None:
                            return cand
                        d = math.hypot(cand.u - near[0], cand.s - near[1])
                        if d < best_d:
                            best_d = d
                            best = cand
                        if d <= CLAMP_MAX:
                            return cand
                    s += step
                    n_s += 1
                u += step
                n_u += 1
            # Also sweep from the low corner if the near-start missed.
            if near is not None and best is None:
                u = u_lo
                n_u = 0
                while u <= u_hi + 1e-9 and n_u < 50:
                    s = s_lo
                    n_s = 0
                    while s <= s_hi + 1e-9 and n_s < 50:
                        cand = _smt_box(name, u, s, wu, ws, h, y0, face)
                        if ok(cand):
                            d = math.hypot(cand.u - near[0], cand.s - near[1])
                            if d < best_d:
                                best_d = d
                                best = cand
                            if d <= CLAMP_MAX:
                                return cand
                        s += step
                        n_s += 1
                    u += step
                    n_u += 1
    return best


def _place_fe(
    spec: V2Spec,
    geom: dict[str, Any],
    module: Box,
    cell: Box,
    extra: list[Box] | None = None,
) -> dict[str, Box]:
    """Front end on leftover, side strip, or the battery-pocket island."""
    regions = _fe_regions(spec, geom, module, cell)
    occupied: list[Box] = [module, cell, *(extra or [])]
    parts: dict[str, Box] = {}
    items: list[tuple[str, list[tuple[float, float]], float, tuple[float, float] | None]] = [
        ("ADS1292_RSM", [(VQFN[0], VQFN[1])], VQFN[2], None),
    ]
    if spec.arch != "C":
        items += [
            ("BQ25100", [(BQ[0], BQ[1]), (BQ[1], BQ[0])], BQ[2], None),
            ("TLV713", [(LDO[0], LDO[1])], LDO[2], None),
        ]
    items += [
        ("BAV199S_1", [(ARRAY[0], ARRAY[1]), (ARRAY[1], ARRAY[0])], ARRAY[2], CONTACT_1),
        ("BAV199S_2", [(ARRAY[0], ARRAY[1]), (ARRAY[1], ARRAY[0])], ARRAY[2], CONTACT_2),
        ("JST_SH", [(JST[0], JST[1]), (JST[1], JST[0])], JST[2], None),
    ]
    leftover_first = list(regions)
    pocket_first = list(reversed(regions)) if spec.layout == "series" else leftover_first
    for name, sizes, h, near in items:
        ranked = pocket_first if name == "JST_SH" else leftover_first
        placed = _find_site(name, sizes, h, ranked, occupied, near=near)
        if placed is None:
            (u0, u1, s0, s1), y0, face = regions[0]
            wu, ws = sizes[0]
            placed = _smt_box(name, u0 + wu / 2.0, s0 + ws / 2.0, wu, ws, h, y0, face)
        parts[name] = placed
        occupied.append(placed)
    return parts


def _place_swds(
    spec: V2Spec,
    geom: dict[str, Any],
    module: Box,
    cell: Box,
    occupied: list[Box],
) -> dict[str, Box]:
    regions = _fe_regions(spec, geom, module, cell)
    parts: dict[str, Box] = {}
    extra = list(occupied)
    for i in range(N_SWD):
        name = f"SWD_{i + 1}"
        placed = _find_site(name, [(SWD[0], SWD[1])], 0.05, regions, extra)
        if placed is None:
            (u0, u1, s0, s1), y0, face = regions[0]
            placed = _smt_box(
                name, u0 + SWD[0] / 2.0, s0 + SWD[1] / 2.0, SWD[0], SWD[1], 0.05, y0, face
            )
        parts[name] = placed
        extra.append(placed)
    return parts


def _place_0402s(
    spec: V2Spec,
    geom: dict[str, Any],
    occupied: list[Box],
    antenna: tuple[float, float, float, float] | None,
) -> list[Box]:
    bu0, bu1 = geom["board_u"]
    bs0, bs1 = geom["board_s"]
    face = "top"
    y0, y1 = geom["board_top"], geom["board_top"] + 0.5
    found: list[Box] = []
    step_u, step_s = 0.30, 0.30
    u = bu0 + R0402[0] / 2.0 + 0.1
    while u + R0402[0] / 2.0 <= bu1 + 1e-9 and len(found) < N_0402:
        s = bs0 + R0402[1] / 2.0 + 0.1
        while s + R0402[1] / 2.0 <= bs1 + 1e-9 and len(found) < N_0402:
            for wu, ws in (R0402, (R0402[1], R0402[0])):
                cand = Box(f"R0402_{len(found)+1}", u, s, wu, ws, y0, y1, face)
                if y0 < KEEPOUT_TOP_Y - 1e-9:
                    if _circle_hits_box(CONTACT_1[0], CONTACT_1[1], KEEPOUT_MARGIN_R, cand):
                        continue
                    if _circle_hits_box(CONTACT_2[0], CONTACT_2[1], KEEPOUT_MARGIN_R, cand):
                        continue
                if any(_same_level_overlap(cand, other, 0.05) for other in occupied + found):
                    continue
                if not _in_rect(u, s, wu, ws, geom["board_u"], geom["board_s"]):
                    continue
                if antenna is not None:
                    au0, as0, au1, as1 = antenna
                    if cand.u1 >= au0 and cand.u0 <= au1 and cand.s1 >= as0 and cand.s0 <= as1:
                        continue
                found.append(cand)
                break
            s += step_s
        u += step_u
    # Series: leftover of the battery pocket beside the cell, on the floor.
    cell_box = next((b for b in occupied if b.name == "cell"), None)
    if spec.layout == "series" and cell_box is not None:
        pu0 = cell_box.u1 + 0.15
        pu1 = geom["cavity_u"][1] - 0.15
        ps0 = geom["cavity_s"][0] + 0.15
        ps1 = (geom["rib_s"][0] if geom["rib_s"][1] > geom["rib_s"][0] else cell_box.s1) - 0.15
        u = pu0 + R0402[0] / 2.0
        while u + R0402[0] / 2.0 <= pu1 + 1e-9 and len(found) < N_0402:
            s = ps0 + R0402[1] / 2.0
            while s + R0402[1] / 2.0 <= ps1 + 1e-9 and len(found) < N_0402:
                for wu, ws in (R0402, (R0402[1], R0402[0])):
                    cand = Box(
                        f"R0402_{len(found)+1}",
                        u,
                        s,
                        wu,
                        ws,
                        FLOOR_Y,
                        FLOOR_Y + 0.5,
                        "floor",
                    )
                    if any(_overlap(cand, other, 0.05) for other in occupied + found):
                        continue
                    if cand.u0 < pu0 - 1e-9 or cand.u1 > pu1 + 1e-9:
                        continue
                    if cand.s0 < ps0 - 1e-9 or cand.s1 > ps1 + 1e-9:
                        continue
                    found.append(cand)
                    break
                s += 0.30
            u += 0.30
    return found


def _free_area(spec: V2Spec, geom: dict[str, Any], parts: dict[str, Box], antenna: tuple[float, float, float, float] | None) -> float:
    bu0, bu1 = geom["board_u"]
    bs0, bs1 = geom["board_s"]
    if bu1 <= bu0 or bs1 <= bs0:
        return 0.0
    us = np.arange(bu0 + RASTER / 2.0, bu1, RASTER)
    ss = np.arange(bs0 + RASTER / 2.0, bs1, RASTER)
    if us.size == 0 or ss.size == 0:
        return 0.0
    uu, sss = np.meshgrid(us, ss, indexing="xy")
    free = np.ones(uu.shape, dtype=bool)
    for cu, cs in (CONTACT_1, CONTACT_2):
        free &= (uu - cu) ** 2 + (sss - cs) ** 2 >= KEEPOUT_MARGIN_R ** 2
    if antenna is not None:
        au0, as0, au1, as1 = antenna
        free &= ~((uu >= au0) & (uu <= au1) & (sss >= as0) & (sss <= as1))
    return float(free.sum()) * RASTER * RASTER


def run_spec(spec: V2Spec) -> V2Result:
    geom = body_geom(spec)
    tabs = _make_tabs(spec, geom)
    module, antenna = _place_module(spec, geom)
    cell = _place_cell(spec, geom, module)
    usb, usb_wall = _place_usb(spec, geom, module)
    stand_boxes = _place_standoffs(spec, geom)
    pad_boxes = _place_pads(spec, geom)
    seed = [module, cell, *stand_boxes, *pad_boxes]
    if usb is not None:
        seed.append(usb)
    fe = _place_fe(spec, geom, module, cell, extra=seed[2:])
    switch_parts = _place_switch_and_header(spec, geom, seed + list(fe.values()))
    swds = _place_swds(spec, geom, module, cell, seed + list(fe.values()) + list(switch_parts.values()))
    parts: dict[str, Box] = {"module": module, "cell": cell, **fe, **switch_parts, **swds}
    if usb is not None:
        parts["usb"] = usb
    for box in stand_boxes:
        parts[box.name] = box
    for box in pad_boxes:
        parts[box.name] = box
    occupied = list(parts.values())
    for box in _place_bosses(spec, geom, occupied):
        parts[box.name] = box
        occupied.append(box)
    occupied = list(parts.values())
    for tab in tabs.values():
        occupied.extend(_tab_boxes(tab, FLOOR_Y, FLOOR_Y + TAB_T))
    passives = _place_0402s(spec, geom, occupied, antenna)
    for p in passives:
        parts[p.name] = p
    result = V2Result(
        spec=spec,
        body_arc=geom["body_arc"],
        cavity_u=geom["cavity_u"],
        cavity_s=geom["cavity_s"],
        board_u=geom["board_u"],
        board_s=geom["board_s"],
        rib_s=geom["rib_s"],
        board_underside=geom["board_underside"],
        board_top=geom["board_top"],
        total_chord=geom["total_chord"],
        m1_gate=geom["m1_gate"],
        free_mm2=_free_area(spec, geom, parts, antenna),
        parts=parts,
        tabs=tabs,
        antenna=antenna,
        usb_wall=usb_wall,
        n_0402=len(passives),
        adjustment_mm=spec.adjustment_region,
        board_thick=geom["board_thick"],
        standoff_top_y=geom["standoff_top_y"],
        boss_top_y=geom["boss_top_y"],
    )
    result.conflicts = list_conflicts(result)
    return result


def list_conflicts(r: V2Result) -> list[str]:
    spec = r.spec
    out: list[str] = []
    m = MODULE[spec.arch]
    cell = CELL[spec.cell]
    cu, cs = r.cavity_u, r.cavity_s
    bu, bs = r.board_u, r.board_s

    if bu[1] <= bu[0] or bs[1] <= bs[0]:
        out.append(f"board span empty u {bu} s {bs}")
        return out

    if spec.arch == "C":
        out.append("architecture C is out (plan v2 turn 02 findings 1 and 2)")

    for name in ("switch", "header"):
        box = r.parts.get(name)
        if box is None:
            out.append(f"{name} is missing")
        elif abs(box.y0 - r.board_top) > 1e-6:
            out.append(f"{name} is not on the board top (y0 {box.y0:.2f} vs board {r.board_top:.2f})")

    # Architecture C: XIAO 17.5 vs cavity width-3.
    cav_w = cu[1] - cu[0]
    if spec.arch == "C" and m["w"] > cav_w + 1e-9:
        out.append(
            f"XIAO width {m['w']:.2f} > cavity u {cav_w:.2f} at BODY_WIDTH {spec.width:g}"
        )

    if spec.iface == "I":
        need = cell["t"] + FOAM
        if spec.standoff + 1e-9 < need:
            out.append(
                f"cell {cell['t']:.1f}+{FOAM:g}={need:.1f} does not fit under standoff {spec.standoff:g} "
                f"(board underside y {r.board_underside:.2f})"
            )
        cellb = r.parts.get("cell")
        if cellb is not None:
            for site_name, site in (("SIG1", CONTACT_1), ("SIG2", CONTACT_2), ("REF", CONTACT_REF)):
                if _circle_hits_box(site[0], site[1], STANDOFF_CIRCUMR, cellb):
                    out.append(f"cell hits {site_name} standoff (circumradius {STANDOFF_CIRCUMR:g})")
                pocket = POCKET_DIA / 2.0 if site_name == "REF" else 0.0
                if pocket and _circle_hits_box(site[0], site[1], pocket, cellb):
                    out.append("cell hits the REF pocket")
            for name, box in r.parts.items():
                if name.startswith("boss") and _overlap(cellb, box):
                    out.append(f"cell hits {name}")

    # Height vs lid.
    for name, box in r.parts.items():
        if name.startswith("usb"):
            continue
        if box.y1 > spec.lid_y + 1e-9:
            out.append(f"{name} top {box.y1:.2f} > LID_Y {spec.lid_y:g}")
        if box.y0 < FLOOR_Y - 1e-9:
            out.append(f"{name} below the floor ({box.y0:.2f})")

    stacked_need = BOARD_AT_PARTS + m["h"] + cell["t"] + FOAM
    cav_h = spec.lid_y - FLOOR_Y
    if spec.iface == "II" and spec.layout == "stacked" and stacked_need > cav_h + 1e-9:
        out.append(
            f"stacked height {stacked_need:.2f} (0.4+{m['h']}+{cell['t']}+0.3) > cavity {cav_h:.2f}"
        )

    # Footprints in cavity / board.
    for name, box in r.parts.items():
        if name == "cell" and spec.layout == "series":
            if not _in_rect(box.u, box.s, box.wu, box.ws, cu, (cs[0], r.rib_s[0] or cs[1])):
                out.append(f"cell {box.wu:.2f}×{box.ws:.2f} does not sit in the pocket")
            continue
        if name.startswith("usb") or name.startswith("standoff") or name.startswith("pad_") or name.startswith("boss"):
            continue
        if name.startswith("R0402") and box.face in {"floor", "pocket"}:
            pocket_s = (cs[0], r.rib_s[0] if r.rib_s[1] > r.rib_s[0] else cs[1])
            if not _in_rect(box.u, box.s, box.wu, box.ws, cu, pocket_s):
                out.append(
                    f"{name} {box.wu:.2f}×{box.ws:.2f} at ({box.u:.2f},{box.s:.2f}) outside the pocket"
                )
            continue
        if box.face == "pocket":
            pocket_s = (cs[0], r.rib_s[0] if r.rib_s[1] > r.rib_s[0] else cs[1])
            if not _in_rect(box.u, box.s, box.wu, box.ws, cu, pocket_s):
                out.append(
                    f"{name} {box.wu:.2f}×{box.ws:.2f} at ({box.u:.2f},{box.s:.2f}) outside the pocket"
                )
            continue
        if name == "module" or name.startswith("BAV") or name.startswith("ADS") or name in {
            "BQ25100", "TLV713", "JST_SH", "switch", "header"
        } or name.startswith("R0402") or name.startswith("SWD"):
            if not _in_rect(box.u, box.s, box.wu, box.ws, bu, bs) and name != "cell":
                out.append(
                    f"{name} {box.wu:.2f}×{box.ws:.2f} at ({box.u:.2f},{box.s:.2f}) outside the board"
                )

    # Keep-outs vs parts that sit in the keep-out height band (floor to 4.13).
    for name, box in r.parts.items():
        if name == "cell" and spec.layout == "series":
            continue
        if name.startswith("usb") or name.startswith("standoff") or name.startswith("pad_") or name.startswith("boss"):
            continue
        if box.y0 >= KEEPOUT_TOP_Y - 1e-9:
            continue
        if _circle_hits_box(CONTACT_1[0], CONTACT_1[1], KEEPOUT_MARGIN_R, box):
            out.append(f"{name} enters SIG1 keep-out + 0.5")
        if _circle_hits_box(CONTACT_2[0], CONTACT_2[1], KEEPOUT_MARGIN_R, box):
            out.append(f"{name} enters SIG2 keep-out + 0.5")

    # Antenna vs cell.
    if r.antenna is not None:
        au0, as0, au1, as1 = r.antenna
        cellb = r.parts["cell"]
        gap_s = min(abs(as0 - cellb.s1), abs(cellb.s0 - as1), abs((as0 + as1) / 2.0 - cellb.s))
        # Separation along s between rectangles.
        if cellb.s1 < as0:
            gap = as0 - cellb.s1
        elif as1 < cellb.s0:
            gap = cellb.s0 - as1
        else:
            gap = 0.0
        if gap + 1e-9 < ANTENNA_CELL_MIN:
            out.append(f"cell to antenna zone {gap:.2f} < 5 mm")
        # Parts in the antenna rectangle on copper faces.
        ant_box = Box("antenna", (au0 + au1) / 2.0, (as0 + as1) / 2.0, au1 - au0, as1 - as0, 0, 10, "top")
        for name, box in r.parts.items():
            if name in {"module", "cell", "usb"} or name.startswith("usb"):
                continue
            if box.face == "top" and _overlap(box, ant_box):
                out.append(f"{name} in the antenna keep-out")

    # Overlaps same face / y.
    names = list(r.parts)
    for i, a in enumerate(names):
        for b in names[i + 1 :]:
            if _overlap(r.parts[a], r.parts[b]):
                if a.startswith("pad_") and b.startswith("standoff"):
                    continue
                if b.startswith("pad_") and a.startswith("standoff"):
                    continue
                # Standoff tops meet the board underside; lid-facing parts sit above the board.
                if a.startswith("standoff") and r.parts[b].y0 + 1e-9 >= r.board_underside:
                    continue
                if b.startswith("standoff") and r.parts[a].y0 + 1e-9 >= r.board_underside:
                    continue
                out.append(f"{a} overlaps {b}")

    # Tabs: bend, no cross, no courtyard. Interface I has no tabs.
    for name, tab in r.tabs.items():
        if not _bend_ok(tab.points):
            out.append(f"{name} flex tab bend radius < {BEND_R:g} mm")
        tboxes = _tab_boxes(tab, FLOOR_Y, FLOOR_Y + TAB_T)
        for other_name, other in r.tabs.items():
            if other_name <= name:
                continue
            for tb in tboxes:
                for ob in _tab_boxes(other, FLOOR_Y, FLOOR_Y + TAB_T):
                    if tb.name.endswith("_ring") and ob.name.endswith("_ring"):
                        continue
                    if _overlap(tb, ob, 0.0):
                        out.append(f"{name} tab crosses {other_name} tab")
                        break
        for pname, pbox in r.parts.items():
            if pname == "cell" and spec.layout == "series":
                continue
            for tb in tboxes:
                if tb.name.endswith("_ring"):
                    continue
                if pbox.name.startswith("standoff"):
                    continue
                if _overlap(tb, pbox, 0.0) and pbox.face in {"bottom", "floor", "top"}:
                    if pbox.y0 < tb.y1 - 1e-9 and pbox.y1 > tb.y0 + 1e-9:
                        out.append(f"{name} tab crosses {pname} courtyard")
                        break

    if r.n_0402 < N_0402:
        out.append(f"{N_0402 - r.n_0402} of {N_0402} 0402 courtyards have no site")

    # Arrays within 10 mm of their contacts.
    for aname, site in (("BAV199S_1", CONTACT_1), ("BAV199S_2", CONTACT_2)):
        if aname in r.parts:
            box = r.parts[aname]
            d = math.hypot(box.u - site[0], box.s - site[1])
            if d > CLAMP_MAX:
                out.append(f"{aname} {d:.2f} mm from its contact (> {CLAMP_MAX:g})")

    if r.total_chord - 1e-9 > M1_DEFAULT - 3.0:
        out.append(
            f"TOTAL_CHORD {r.total_chord:.2f} > M1−3 ({M1_DEFAULT - 3.0:.2f}); M1={M1_DEFAULT:g} (Q34 blank, default.toml)"
        )

    if spec.width - 1e-9 > 20.0 or spec.lid_y - 1e-9 > 9.0:
        out.append("body outside the ≤ 9.0 high and 20 wide cap")

    # USB opening is reported, not a packing fail by itself (brief: decide nothing).
    return out


def layout_conflicts(spec: V2Spec) -> list[str]:
    return run_spec(spec).conflicts


def all_specs(*, include_arc: bool = False) -> list[V2Spec]:
    specs: list[V2Spec] = []
    for a in ARCHES_RUN:
        for c in CELLS:
            for lay in LAYOUTS:
                for w in WIDTHS:
                    for y in LID_YS:
                        for iface in IFACES:
                            stands = STANDOFFS if iface == "I" else (3.0,)
                            for st in stands:
                                specs.append(V2Spec(a, c, lay, w, y, 0.0, iface, st))
    if include_arc:
        extra = []
        for spec in list(specs):
            for ds in (1.5, 3.0):
                extra.append(
                    V2Spec(
                        spec.arch,
                        spec.cell,
                        spec.layout,
                        spec.width,
                        spec.lid_y,
                        ds,
                        spec.iface,
                        spec.standoff,
                    )
                )
        specs.extend(extra)
    return specs


def run_matrix(*, include_arc: bool = False) -> list[V2Result]:
    return [run_spec(s) for s in all_specs(include_arc=include_arc)]


def winners(rows: list[V2Result], limit: int = 6) -> list[V2Result]:
    closed = [r for r in rows if r.closes]
    closed.sort(key=lambda r: (r.spec.arch, r.spec.width, r.spec.lid_y, r.spec.arc_plus, r.spec.cell, r.spec.layout))
    # Smallest body per architecture first, then fill.
    picked: list[V2Result] = []
    seen_arch: set[str] = set()
    for r in closed:
        if r.spec.arch not in seen_arch:
            picked.append(r)
            seen_arch.add(r.spec.arch)
    for r in closed:
        if r in picked:
            continue
        picked.append(r)
        if len(picked) >= limit:
            break
    return picked[:limit]


def smallest_per_arch(rows: list[V2Result]) -> dict[str, V2Result | None]:
    out: dict[str, V2Result | None] = {a: None for a in ARCHES}
    closed = [r for r in rows if r.closes]
    for a in ARCHES:
        cand = [r for r in closed if r.spec.arch == a]
        if not cand:
            continue
        cand.sort(key=lambda r: (r.spec.width, r.spec.lid_y, r.spec.arc_plus, r.spec.layout, r.spec.cell))
        out[a] = cand[0]
    return out


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def render_svg(spec: V2Spec, result: V2Result | None = None) -> bytes:
    if not _placement().HAS_MATPLOTLIB:
        raise RuntimeError("matplotlib is not installed")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

    matplotlib.rcParams.update(
        {
            "svg.hashsalt": "elicio-wp11-placement-v2",
            "figure.dpi": 120,
            "savefig.dpi": 120,
            "font.family": "DejaVu Sans",
            "font.size": 7.0,
            "axes.linewidth": 0.5,
            "path.simplify": False,
            "svg.fonttype": "path",
            "text.hinting": "none",
        }
    )

    r = result or run_spec(spec)
    w = spec.width
    fig, ax = plt.subplots(figsize=(11.0, 8.5), dpi=120)
    ax.set_aspect("equal")
    ax.set_xlim(-1.5, w + 16)
    ax.set_ylim(-1.5, r.body_arc + 4)
    ax.set_xlabel("u (mm)")
    ax.set_ylabel("s (mm)")
    ax.set_title(f"Elicio packing v2  {spec.tag}  (u, s) body frame")

    ax.add_patch(Rectangle((0, 0), w, r.body_arc, fill=False, lw=1.2, edgecolor="0.2"))
    ax.add_patch(
        Rectangle(
            (r.cavity_u[0], r.cavity_s[0]),
            r.cavity_u[1] - r.cavity_u[0],
            r.cavity_s[1] - r.cavity_s[0],
            fill=False,
            lw=0.8,
            edgecolor="0.5",
            linestyle="--",
        )
    )
    ax.add_patch(
        Rectangle(
            (r.board_u[0], r.board_s[0]),
            r.board_u[1] - r.board_u[0],
            r.board_s[1] - r.board_s[0],
            fill=True,
            facecolor="#f4f1ea",
            edgecolor="#8a7a55",
            lw=0.6,
            label="board",
        )
    )
    if r.rib_s[1] > r.rib_s[0]:
        ax.add_patch(
            Rectangle(
                (r.cavity_u[0], r.rib_s[0]),
                r.cavity_u[1] - r.cavity_u[0],
                r.rib_s[1] - r.rib_s[0],
                facecolor="#cfcfcf",
                edgecolor="0.4",
                lw=0.4,
                label="rib",
            )
        )
    for site, label in ((CONTACT_1, "SIG1"), (CONTACT_2, "SIG2"), (CONTACT_REF, "REF")):
        ax.add_patch(Circle(site, KEEPOUT_R, fill=False, edgecolor="#b33", lw=0.7, linestyle=":"))
        ax.add_patch(Circle(site, RING_R, fill=False, edgecolor="#333", lw=0.8))
        ax.plot(*site, "k.", ms=3)
        ax.text(site[0] + 0.3, site[1] + 0.3, label, fontsize=6)
    colors = {
        "module": "#4c78a8",
        "cell": "#f58518",
        "ADS1292_RSM": "#54a24b",
        "usb": "#e45756",
        "usb_c": "#e45756",
        "usb_xiao": "#e45756",
        "JST_SH": "#b279a2",
    }
    for name, box in r.parts.items():
        col = colors.get(name, "#9d9d9d")
        if name.startswith("R0402"):
            col = "#d4a574"
        if name.startswith("SWD"):
            col = "#333"
        if name.startswith("BAV"):
            col = "#72b7b2"
        ax.add_patch(
            FancyBboxPatch(
                (box.u0, box.s0),
                box.wu,
                box.ws,
                boxstyle="square,pad=0",
                facecolor=col,
                edgecolor="0.2",
                alpha=0.55,
                lw=0.4,
            )
        )
    if r.antenna:
        au0, as0, au1, as1 = r.antenna
        ax.add_patch(
            Rectangle(
                (au0, as0),
                au1 - au0,
                as1 - as0,
                fill=False,
                edgecolor="#e45756",
                lw=0.8,
                linestyle="--",
                label="antenna keep-out",
            )
        )
    for tab in r.tabs.values():
        xs = [p[0] for p in tab.points]
        ys = [p[1] for p in tab.points]
        ax.plot(xs, ys, color="#5c3a1e", lw=1.6, solid_capstyle="round", label=f"{tab.name} tab" if tab.name == "SIG1" else None)
    lines = [
        f"arch {spec.arch}  cell {spec.cell}  {spec.layout}  iface {spec.iface}",
        f"W {spec.width:g}  LID_Y {spec.lid_y:g}  standoff {spec.standoff:g}  arc+ {spec.arc_plus:g}",
        f"chord {r.total_chord:.2f}  M1 gate {r.m1_gate:.2f}",
        f"free {r.free_mm2:.1f} mm²  0402 {r.n_0402}/{N_0402}",
        f"board y {r.board_underside:.2f}–{r.board_top:.2f}  thick {r.board_thick:.2f}",
        f"standoff top y {r.standoff_top_y:.2f}  boss top y {r.boss_top_y:.2f}",
        f"adjust ±{r.adjustment_mm:.2f} (4.0−2.9−{PLACEMENT_TOL:g})",
        f"USB wall: {r.usb_wall or 'none'}  recess {USB_RECESS:g}  lig {USB_LIGAMENT:g}",
        "result: closes" if r.closes else "result: DOES NOT CLOSE",
    ]
    lines += [f"✗ {c}" for c in r.conflicts[:18]]
    if len(r.conflicts) > 18:
        lines.append(f"… {len(r.conflicts) - 18} more")
    ax.text(
        w + 0.6,
        r.body_arc - 0.4,
        "\n".join(lines),
        fontsize=6.0,
        family="DejaVu Sans",
        va="top",
        ha="left",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor="0.4"),
    )
    ax.legend(loc="lower right", fontsize=6, framealpha=0.9)
    ax.grid(True, linestyle=":", lw=0.3, color="0.75")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(
        buf,
        format="svg",
        facecolor="white",
        metadata={"Creator": "elicio-wp11", "Title": f"elicio packing v2 {spec.tag}"},
    )
    plt.close(fig)
    text = buf.getvalue().decode("utf-8")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"<metadata>.*?</metadata>", "", text, flags=re.S)
    text = text.rstrip()
    first = html.escape(r.first_conflict, quote=True)
    usb = html.escape(r.usb_wall or "none", quote=True)
    desc = (
        f'<desc id="packing-v2">closes={int(r.closes)} first={first} usb_wall={usb}</desc>\n'
    )
    if not text.endswith("</svg>"):
        raise RuntimeError("matplotlib svg has no closing tag")
    text = text[: -len("</svg>")] + desc + "</svg>\n"
    return text.encode("utf-8")


def write_drawing(spec: V2Spec, path: Path | None = None, result: V2Result | None = None) -> str:
    dest = path or drawing_path(spec)
    dest.parent.mkdir(parents=True, exist_ok=True)
    data = render_svg(spec, result)
    dest.write_bytes(data)
    return sha256_bytes(data)


def write_all_drawings(*, include_arc: bool = False, dest_dir: Path | None = None) -> list[tuple[V2Spec, str]]:
    """Write one SVG per spec. Returns (spec, sha256) rows."""
    out: list[tuple[V2Spec, str]] = []
    for spec in all_specs(include_arc=include_arc):
        path = (dest_dir / spec.filename) if dest_dir is not None else drawing_path(spec)
        digest = write_drawing(spec, path)
        out.append((spec, digest))
    return out


def cad_overrides(result: V2Result) -> dict[str, Any]:
    """Stage B overlay keys. Packing v2 then moves width, arc and lid."""
    spec = result.spec
    return {
        "PACKING": "v2",
        "V2_ARCH": spec.arch,
        "V2_CELL": spec.cell,
        "V2_LAYOUT": spec.layout,
        "V2_WIDTH": spec.width,
        "V2_LID_Y": spec.lid_y,
        "V2_ARC_PLUS": spec.arc_plus,
        "V2_IFACE": spec.iface,
        "V2_STANDOFF": spec.standoff,
        "MOCK_CONTACTS": False,
        "CONTACT_SOURCE": (
            "interface I gold pads on standoff tops (WP11 turn 07)"
            if spec.iface == "I"
            else "interface II flex tabs under standoffs (WP11)"
        ),
    }


def _md_cell(text: str) -> str:
    return text.replace("|", "/").replace("\n", " ")


def packing_markdown(rows: list[V2Result]) -> str:
    """WP11 packing-v2.md body. Plan is not changed."""
    closed = [r for r in rows if r.closes]
    per = smallest_per_arch(rows)
    lines: list[str] = []
    lines.append("# Packing v2 — which architectures close")
    lines.append("")
    lines.append("WP11 analysis. The plan is not changed. Nothing is ordered.")
    lines.append("Architecture C is out (plan v2 turn 02). Interface I is turn 07:")
    lines.append("no springs, no pins; board underside on three brass standoff tops;")
    lines.append("8 × 8 gold pad per site; bosses 0.5 lower than the standoff tops;")
    lines.append("cell under the board on the floor. Interface II is the flex-tab fallback.")
    lines.append("Arc-plus was not run: layouts already close at BODY_ARC 48.4.")
    lines.append("")
    lines.append("## 1. Every run at BODY_ARC 48.4")
    lines.append("")
    lines.append(
        "| arch | iface | standoff | cell | layout | width | lid | closes | first conflict | free mm² | TOTAL_CHORD | M1 gate |"
    )
    lines.append("|---|---|---:|---|---|---:|---:|---|---|---:|---:|---:|")
    for r in rows:
        spec = r.spec
        first = "—" if r.closes else _md_cell(r.first_conflict)
        lines.append(
            f"| {spec.arch} | {spec.iface} | {spec.standoff:g} | {spec.cell} | {spec.layout} | "
            f"{spec.width:g} | {spec.lid_y:g} | {'yes' if r.closes else 'no'} | {first} | "
            f"{r.free_mm2:.1f} | {r.total_chord:.2f} | {r.m1_gate:.2f} |"
        )
    lines.append("")
    lines.append("## 2. First-conflict families")
    lines.append("")
    lines.append("Interface I (288 runs): none close.")
    lines.append("")
    lines.append("- DTP301120 + standoff 3.0 (72): cell 3.2+0.3=3.5 does not fit under standoff 3.0 (board underside y 4.50).")
    lines.append("- DTP301120 + standoff 3.5 (72): cell hits SIG1 standoff (circumradius 2.9). The 22.0 mm cell on the floor reaches s of SIG1 at 22.0.")
    lines.append("- 501015 + standoff 3.0 (72): cell 5.2+0.3=5.5 does not fit under standoff 3.0.")
    lines.append("- 501015 + standoff 3.5 (72): cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00). The cell fits a 3.5 standoff only when its packed height is ≤ 3.5; 501015 is 5.5.")
    lines.append("")
    lines.append("Adjustment region per site (Interface I, formula only): 4.0 − 2.9 − 0.3 = ±0.8 mm. NOT_MEASURED on the solid.")
    lines.append("")
    lines.append("Interface II (144 runs): four close, all A 501015 series width 20.")
    lines.append("")
    lines.append("## 3. Plan v2 §4 rule, line by line")
    lines.append("")
    lines.append("Rule (1) closes ≤ 9.0 high and 20 wide, checks on the built solid, TOTAL_CHORD ≤ M1−3.")
    lines.append("")
    if closed:
        lines.append(
            "Four layouts close in packing: "
            + ", ".join(r.spec.tag for r in closed)
            + ". TOTAL_CHORD 47.90 ≤ 49.00 (M1=52 from default.toml; Q34 blank). USB-C hangs off the hook-end end face (fallback); the medial opening is not cut on the order-1 solid."
        )
    else:
        lines.append("No layout closes.")
    lines.append("Architecture B does not close. Architecture C is out.")
    lines.append("Interface I does not close.")
    lines.append("")
    lines.append("Rule (2) parts orderable. The closer uses Raytac MDBT50Q-1MV2, cell 501015, ADS1292, BQ25100, TLV713, JST-SH, USB-C 16-pin, BAV199S arrays, a 4.5 × 4.5 × 1.6 recovery switch, a 7.6 × 2.5 × 2.5 bench header, DIN 439 M2.5 nuts and ISO 7380 M2.5×4 screws, flex tabs. Page prices are NOT_MEASURED (no vendor contact).")
    lines.append("")
    lines.append("Rule (3) fewest Rolf steps. Interface I would skip tabs (board on standoff tops). It does not close, so the only closer is Interface II (tabs under standoffs). No decision.")
    lines.append("")
    lines.append("Rule (4) lowest page price. NOT_MEASURED.")
    lines.append("")
    lines.append("Ties go to A. The only architecture that closes is A.")
    lines.append("")
    lines.append("## 4. Smallest body per architecture")
    lines.append("")
    for arch in ("A", "B", "C"):
        hit = per.get(arch)
        if hit is None:
            lines.append(f"- **{arch}**: does not close.")
        else:
            spec = hit.spec
            lines.append(
                f"- **{arch}**: packing-smallest `{spec.tag}`. BODY_WIDTH {spec.width:g}, LID_Y {spec.lid_y:g}, "
                f"BODY_THICK {spec.lid_y + 1.0:g}, TOTAL_CHORD {hit.total_chord:.2f}, "
                f"USB wall: {hit.usb_wall}."
            )
            if spec.lid_y == 7.0:
                lines.append(
                    "  Stage B of the order-1 path uses LID_Y 8.0: CELL_envelope is the v1 5.2+0.5 foam box, "
                    "and LID_Y 7.0 fails that check by 0.2 mm before the solid is written."
                )
    lines.append("")
    lines.append("## 5. Layout for the board lane (architectures that close)")
    lines.append("")
    a = per.get("A")
    if a is None:
        lines.append("No architecture closes. There is no board-lane layout.")
    else:
        spec = a.spec
        p = a.parts
        lines.append(f"Hand `{spec.tag}` to the board lane. Interface II. Flex 0.4 at parts, 0.2 at tabs.")
        lines.append("Board zone u 2.25–17.75, s 18.60–37.60. Underside y 4.00, top y 4.40.")
        lines.append("Cell 501015 10.4 × 15.6 × 5.2 plus foam 0.3 in the pocket, centre (7.00, 9.30), y 1.50–7.00.")
        lines.append("Module Raytac 15.50 × 10.50 × 2.3, centre (10.00, 32.35), y 4.40–6.70 (length along u). Antenna keep-out 12.4 × 3.8 at s 33.80–37.60, u 3.80–16.20 (Raytac Spec K / interface §6.3).")
        lines.append("Recovery switch 4.5 × 4.5 × 1.6 on the board top, centre (4.80, 21.15), y 4.40–6.00.")
        lines.append("Bench header 2.5 × 7.6 × 2.5 on the board top, centre (15.40, 22.60), y 4.40–6.90.")
        lines.append("ADS1292 5.0 × 5.0 × 1.0 at (11.20, 21.25). BAV199S_1 (9.95, 25.32), BAV199S_2 (12.65, 25.32). BQ25100 (3.45, 25.30). TLV713 (5.40, 25.35). JST-SH 4.0 × 6.0 × 2.9 in the pocket at (14.40, 4.65), y 1.90–4.80.")
        lines.append("USB-C 8.9 × 7.3 × 3.2 at (10.00, −2.15), y 1.00–4.20. It would cut the **hook-end end face (fallback)**. Recess 1.0, ligaments 1.5, plug volume 12 × 6.5 × 15. No decision.")
        lines.append("Flex tabs (ring Ø5.0, hole Ø2.7, strip 2.5, bend R ≥ 1.0):")
        lines.append("- SIG1: (5.90, 22.00) → (5.90, 29.00).")
        lines.append("- SIG2: (10.40, 33.10) → (10.40, 26.10).")
        lines.append("- REF: (8.50, 43.00) → (8.50, 36.80). REF runs to the tail pocket. Q28 allows the pocket to grow.")
        lines.append("Stack inside the wall: tab 0.2 + nut 1.6 + screw tip past the nut 0.70 = 2.50. Screw ISO 7380 M2.5×4. Nut DIN 439 M2.5, m 1.6, s 5.0.")
        lines.append("Standoffs 5 AF from the floor to y 4.50 (height 3.0 above the inner floor). Bosses 0.5 lower are NOT_MEASURED on the order-1 solid.")
        lines.append("Harness 100 ± 3 mm: NOT_MEASURED (routed length, not a solid).")
        lines.append("25 of 25 0402 courtyards placed (6 on the board, 19 in the pocket).")
        lines.append("")
        lines.append("B and C do not close. There is no board-lane layout for them.")
    lines.append("")
    lines.append("## 6. Winners sent to Stage B (at most six)")
    lines.append("")
    if closed:
        for r in closed:
            mark = (
                " (`scripts/cad/params/stageb_v2.toml`; smallest LID_Y the order-1 CELL_envelope accepts)"
                if r.spec.lid_y == 8.0
                else ""
            )
            note = (
                " — packing-closes; Stage B CELL_envelope uses foam 0.5 and fails at LID_Y 7.0 (clear_y −0.2)"
                if r.spec.lid_y == 7.0
                else mark
            )
            lines.append(f"- `{r.spec.tag}`{note}")
        lines.append("Construction is the order-1 path with packing C (width 20, arc 48.4). No fork.")
    else:
        lines.append("None close. Stage B still measures a representative Interface I and Interface II overlay on the order-1 solid.")
    lines.append("")
    lines.append("## 7. Numbers taken as given")
    lines.append("")
    lines.append("| Item | Number | Source |")
    lines.append("|---|---|---|")
    lines.append("| Raytac MDBT50Q-1MV2 | 10.5 × 15.5 × 2.3 | coordinator note 3 / plan v2 §3 reserve; Spec K footprint 10.5 × 15.5 × 2.0 |")
    lines.append("| Raytac antenna keep-out | 12.4 × 3.8 | Raytac Spec K p.9/p.13, interface.md §6.3 |")
    lines.append("| Ebyte E73-2G4M08S1C | 13 × 18 × 2.0 | brief; plan v2 §3 |")
    lines.append("| E73 antenna keep-out | 12.4 × 3.8 | sheet unreachable; v1 rule interface §6.3 |")
    lines.append("| Seeed XIAO nRF52840 | out | plan v2 turn 02 findings 1 and 2 |")
    lines.append("| DTP301120 with protection | 22.0 × 11.5 × 3.2 | SparkFun PRT-25270 drawing, L5-research-v2.md §1 |")
    lines.append("| 501015 | 5.2 × 10.4 × 15.6 | v1 CELL_BODY_MAX; plan v2 §3 quotes 5.4 thick |")
    lines.append("| Foam under a cell | 0.3 | brief; plan v2 §3 |")
    lines.append("| Interface I board | FR4 1.0, 4-layer | plan v2 turn 07 |")
    lines.append("| Interface I pad | 8 × 8 ENIG, half-size 4.0 | turn 07 |")
    lines.append("| Standoff | M2.5 hex 5 AF, circumradius 2.9, heights 3.0 and 3.5 | turn 07; coordinator note 3 |")
    lines.append("| Boss drop | 0.5 | turn 07 |")
    lines.append("| Placement tolerance | 0.3 | JLC floor ±0.3, turn 07 G7 |")
    lines.append("| Adjustment region | ±0.8 | 4.0 − 2.9 − 0.3 |")
    lines.append("| Flex + stiffener | 0.11 + 0.3 = 0.4 at parts, 0.2 at tabs | brief |")
    lines.append("| ADS1292 VQFN-32 courtyard | 5.0 × 5.0 × 1.0 | brief |")
    lines.append("| Recovery switch | 4.5 × 4.5 × 1.6 | coordinator note 3 |")
    lines.append("| Bench header | 7.6 × 2.5 × 2.5 | plan v2 §5.6 |")
    lines.append("| USB-C 16-pin | 8.9 × 7.3 × 3.2 | brief |")
    lines.append("| USB opening / recess / ligament | 9.0 × 3.5 / 1.0 / 1.5 | coordinator note 1 |")
    lines.append("| Plug volume | 12 × 6.5 × 15 | plan v2 §5.4 |")
    lines.append("| JST-SH | 4.0 × 6.0 × 2.9 side entry | brief |")
    lines.append("| Ring pad | Ø5.0, hole Ø2.7, strip 2.5 | brief; Interface II |")
    lines.append("| Nut DIN 439 M2.5 | m 1.6, s 5.0 | brief |")
    lines.append("| Screw ISO 7380 M2.5×4 | length 4.0 | v1; brief |")
    lines.append("| Stack inside the wall | 2.50 | 0.2 + 1.6 + 0.70 |")
    lines.append("| Harness | 100 ± 3 mm | plan v2; NOT_MEASURED as a solid |")
    lines.append("| BODY_WIDTH / LID_Y / BODY_ARC | 18–20 / 6.0–9.0 / 48.4 | coordinator note 1; other params stageb_provisional.toml |")
    lines.append("| M1 | 52 | default.toml; Q34 blank |")
    lines.append("| PATH_RADIUS | 97.1025 | v1 |")
    lines.append("| Floor | 1.5 | v1 |")
    lines.append("")
    lines.append("## 8. What could not be measured")
    lines.append("")
    lines.append("- TAB_envelope_air pre-CAD for PACKING=v2: the TE 31428 pad-gap search is not the flex tab.")
    lines.append("- V2_WALL_minima inner face at y 0.75: the probe returned the outer skin (~0.20), not 1.5.")
    lines.append("- V2_ADJUSTMENT: ±0.8 is a pad/standoff formula, not a solid probe.")
    lines.append("- V2_USB_medial: the order-1 solid has no medial USB cut.")
    lines.append("- V2_HARNESS: 100 ± 3 mm is a routed length.")
    lines.append("- V2_BOSS: printed bosses 0.5 below the standoff top are not on the order-1 solid.")
    lines.append("- E73 antenna sheet: unreachable; v1 12.4 × 3.8 used.")
    lines.append("- M1 on Rolf (Q34): default 52 used for the gate.")
    lines.append("")
    return "\n".join(lines) + "\n"


def write_packing_doc(path: Path | None = None, *, include_arc: bool = False) -> Path:
    dest = path or (ROOT / "docs" / "fab" / "packing-v2.md")
    dest.write_text(packing_markdown(run_matrix(include_arc=include_arc)), encoding="utf-8")
    return dest
