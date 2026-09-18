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
import subprocess
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
# WP11b note 2: bigger box for buyable cells only. Not in the 864-run matrix.
BUYABLE_EXT_WIDTHS = (20.0, 21.0, 22.0)
BUYABLE_EXT_LID_YS = (9.5, 10.0, 10.5)
BUYABLE_EXT_CELLS = ("dtp", "jauch")
ALLOWED_WIDTHS = tuple(dict.fromkeys((*WIDTHS, *BUYABLE_EXT_WIDTHS)))
ALLOWED_LID_YS = tuple(dict.fromkeys((*LID_YS, *BUYABLE_EXT_LID_YS)))
ARC_STEPS = (0.0, 1.5, 3.0)
IFACES = ("I", "II")
STANDOFFS = (3.0, 3.5, 4.0)
RECESSES = (0.0, 0.5)
LID_THICK = 1.0  # default.toml; outer = LID_Y + 1.0
CELL_RECESS = 0.5  # floor pocket under the cell; remaining web 1.0 (C15)

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

# Flex (interface II). JLC's FPC page (read by WP12, 2026-09-17) lists FR4
# stiffeners 0.1 / 0.2 / 0.4 / 0.6 ... mm, no 0.3 (review r5): parts sit on
# 0.11 PI + 0.4 FR4 and each ring on 0.11 PI + the 0.2 FR4 disc WP12 draws.
FLEX = 0.11
STIFFENER = 0.4
STIFFENER_TAB = 0.2
BOARD_AT_PARTS = FLEX + STIFFENER  # 0.51
BOARD_AT_TABS = FLEX + STIFFENER_TAB  # 0.31
BOARD_RIGID = 1.0  # Interface I: FR4 4-layer, plan v2 §5.2
# One packing truth (review r5): plan v1 §5's 0.5 foam, the number the
# order-1 Stage B CELL_envelope measures on the solid. Plan v2 §3 and the
# WP11 brief say 0.3; 0.5 is the conservative reading (decision 57).
FOAM = 0.5

# Flex tab ring clamped under the brass standoff (plan v2 §5.3 interface II).
TAB_T = BOARD_AT_TABS
TAB_W = 2.5
RING_D = 5.0
RING_R = RING_D / 2.0
RING_HOLE = 2.7
BEND_R = 1.0
# board-v2.md §11: packing R ≥ 1.0; JLC 10×PI → 1.1; that file states R = 1.5.
# WP11b uses 1.5 for the REF tab search. Conflict checks keep BEND_R (review r5).
BOARD_BEND_R = 1.5
TAB_ATTACH_INSET = 0.8  # _make_tabs: board-side end of a straight tab
SCREW_L = 4.0  # ISO 7380 M2.5×4: projects SCREW_L - WALL = 2.5 past the inner floor
SCREW_PROJ = SCREW_L - WALL  # 2.50
KEEPOUT_TOP_Y = 4.13  # v1 keep-out air (nut stack); v2 uses the standoff top too

# Interface I landing (turn 07/09). Heights are above the inner floor.
# Board underside (rigid) = FLOOR_Y + standoff. Bosses 0.5 lower; the board
# bends down over them. Cell under the board needs positive nominal
# clearance and must carry no load after that bend.
STANDOFF_AF = 5.0  # across flats, M2.5 hex
STANDOFF_CIRCUMR = 2.9  # coordinator: 5/√3 ≈ 2.887, stated 2.9
PAD_XY = 8.0
PAD_HALF = PAD_XY / 2.0
PLACEMENT_TOL = 0.3  # JLC printed floor ±0.3, turn 07 G7


def ring_under(spec: "V2Spec") -> float:
    """Ring thickness under each standoff: the flex tab in II, nothing in I."""
    return TAB_T if spec.iface == "II" else 0.0


def standoff_y(spec: "V2Spec") -> tuple[float, float]:
    """Bottom and top of each brass standoff above the part frame (floor at 1.5)."""
    y0 = FLOOR_Y + ring_under(spec)
    return y0, y0 + spec.standoff


def tip_below_standoff_top(spec: "V2Spec") -> float:
    """Screw tip depth under the standoff's top face (plan v2 §5.3)."""
    return spec.standoff - (SCREW_PROJ - ring_under(spec))
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
               "from": "v1 CELL_BODY_MAX (plan v1 §3.3)"},
    # WP11b coordinator note: L7-research-v4.md §2. Not in CELLS, so the
    # round-5 864-run matrix is unchanged.
    "jauch": {"name": "LP501218JH", "t": 5.4, "w": 12.5, "l": 20.0,
              "from": "Jauch LP501218JH+PCM+2 WIRE 50MM; DigiKey 1908-LP501218JH+PCM+2WIRE50MM-ND; L7-research-v4.md §2"},
    # WP11b note 3: L7-research-v4.md §7 and §7.8. Not in CELLS.
    "pack501015": {"name": "501015 pack", "t": 5.0, "w": 10.0, "l": 17.0,
                   "from": "DNK Power DNK501015 'Dimensions: 17 × 10 × 5.0 mm'; Benzo '5mm x 10mm x 17mm'; L7-research-v4.md §7 and §7.8"},
    "pack501012": {"name": "501012 pack", "t": 5.1, "w": 10.1, "l": 13.0,
                   "from": "eBay quote 'approx 13.0mm x 10.1mm x 5.1mm' with PCM, 40 mAh; L7-research-v4.md §7"},
}

VQFN = (5.0, 5.0, 1.0)  # brief; v1 packing courtyard was 4.60
# Review r5: the board (board-v2.md §8, BOM) has no BAV199 arrays; its ESD
# parts are USBLC6-2SC6 (SOT-23-6) on D+/D- and PESD5V0L1UL (the board's
# D_SOD-523 land) on VBUS, and the LDO is TLV71330PDBVR (SOT-23-5, not the
# 1.5 x 1.5 X2SON the lane packed). SOT-23 occupied area as placement.py
# (Nexperia Fig. 9, 3.30 x 2.90); height 1.45 = TI DBV maximum.
SOT23_6 = (3.30, 2.90, 1.45)
SOD523 = (2.20, 1.00, 0.70)
BQ = (2.10, 1.40, 0.5)
LDO = (3.30, 2.90, 1.45)  # TLV71330PDBVR, SOT-23-5
JST = (4.0, 6.0, 2.9)
USB = (8.9, 7.3, 3.2)
R0402 = (1.80, 0.90)
N_0402 = 25
N_SWD = 5
SWD = (1.0, 1.0)

# WP11c: real F.CrtYd / pad extent from the WP12b board (commit 845bac7).
# Round-5 packing sizes stay in VQFN/BQ/LDO/... and still drive the 864-run matrix.
WP12B_REV = "845bac7"
WP12B_PCB = "hardware/board/elicio-v2.kicad_pcb"
WP12B_PRO = "hardware/board/elicio-v2.kicad_pro"
JLC_ASSEMBLY_EDGE = 2.5  # board-v2.md §12 / L6; JLC FPC assembly, body to edge
COPPER_TO_EDGE = 0.30  # board-v2.md §12; DRC min_copper_edge_clearance
CONTACT_NETCLASS_CLEARANCE = 1.0  # WP12b elicio-v2.kicad_pro netclass Contact
SOLDER_MASK_TO_COPPER = 0.05  # WP12b DRC solder_mask_to_copper_clearance
SOLDER_MASK_BRIDGE_MARGIN = 0.10  # two mask expansions
COURTYARD_GAP = 0.0
TAB_WIDTH_II = 2.5
# 0402 pad centres ±0.51, size 0.54 → inner gap 0.48 (WP12c Contact violation).
R0402_PAD_GAP = 0.48
WIDER_TAB_MM = 4.0  # variant B: tab wide enough for one 0402 plus 1.0 mm Contact

# Local F.CrtYd width × height (mm) per footprint name. Source: 845bac7 PCB.
KICAD_COURTYARD = {
    "C_0402_1005Metric": (1.820, 0.920),
    "C_0603_1608Metric": (2.960, 1.460),
    "D_SOD-523": (2.500, 1.400),
    "LED_0402_1005Metric": (1.860, 0.940),
    "USB_C_Receptacle_HRO_TYPE-C-31-M-12": (10.640, 9.420),
    "JST_SH_SM02B-SRSS-TB_1x02-1MP_P1.00mm_Horizontal": (5.800, 6.560),
    "PinHeader_1x03_P2.54mm_Horizontal": (12.310, 8.620),
    "Tag-Connect_TC2030-IDC-NL_2x03_P1.27mm_Vertical": (7.000, 4.000),
    "L_0603_1608Metric": (2.960, 1.460),
    "RING_PAD_D5_H2.7": (6.400, 6.400),
    "SOT-23": (3.860, 3.400),
    "R_0402_1005Metric": (1.860, 0.940),
    "SW_Push_1P1T_XKB_TS-1187A": (7.500, 5.600),
    "Raytac_MDBT50Q": (11.500, 16.500),
    "VQFN-32-1EP_4x4mm_P0.4mm_EP2.8x2.8mm": (5.260, 5.260),
    "Texas_YFP0006": (2.960, 3.500),
    "SOT-23-5": (4.100, 3.400),
    "SOT-23-6": (4.100, 3.400),
}
KICAD_PAD_EXTENT = {
    "C_0402_1005Metric": (1.520, 0.620),
    "C_0603_1608Metric": (2.450, 0.950),
    "D_SOD-523": (2.100, 0.600),
    "LED_0402_1005Metric": (1.560, 0.640),
    "USB_C_Receptacle_HRO_TYPE-C-31-M-12": (9.640, 6.620),
    "JST_SH_SM02B-SRSS-TB_1x02-1MP_P1.00mm_Horizontal": (5.400, 4.775),
    "PinHeader_1x03_P2.54mm_Horizontal": (1.700, 6.780),
    "Tag-Connect_TC2030-IDC-NL_2x03_P1.27mm_Vertical": (6.071, 3.023),
    "L_0603_1608Metric": (2.450, 0.950),
    "RING_PAD_D5_H2.7": (5.000, 5.000),
    "SOT-23": (2.475, 3.375),
    "R_0402_1005Metric": (1.560, 0.640),
    "SW_Push_1P1T_XKB_TS-1187A": (7.000, 4.500),
    "Raytac_MDBT50Q": (10.200, 11.400),
    "VQFN-32-1EP_4x4mm_P0.4mm_EP2.8x2.8mm": (4.750, 4.750),
    "Texas_YFP0006": (0.650, 1.050),
    "SOT-23-5": (3.600, 2.500),
    "SOT-23-6": (3.600, 2.500),
}
# Round-5 packing envelopes used by run_spec (not courtyards). None = not a named packing box.
ROUND5_XY = {
    "U1": (10.5, 15.5),
    "U2": (5.0, 5.0),
    "U3": (2.10, 1.40),
    "U4": (3.30, 2.90),
    "U5": (3.30, 2.90),
    "D1": (2.20, 1.00),
    "J1": (8.9, 7.3),
    "J2": (4.0, 6.0),
    "J3": (7.6, 2.5),
    "SW1": (4.5, 4.5),
    "R1": (1.80, 0.90),
    "R2": (1.80, 0.90),
    "R3": (1.80, 0.90),
}

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
    recess: float = 0.0

    def __post_init__(self) -> None:
        if self.arch not in ARCHES:
            raise ValueError(f"arch must be A|B|C, got {self.arch!r}")
        if self.cell not in CELL:
            raise ValueError(f"cell must be {'|'.join(CELL)}, got {self.cell!r}")
        if self.layout not in LAYOUTS:
            raise ValueError(f"layout must be series|stacked, got {self.layout!r}")
        if self.width not in ALLOWED_WIDTHS:
            raise ValueError(f"width must be 18–22, got {self.width!r}")
        if self.lid_y not in ALLOWED_LID_YS:
            raise ValueError(f"lid-y must be 6.0–10.5 in 0.5 steps, got {self.lid_y!r}")
        if self.arc_plus not in ARC_STEPS:
            raise ValueError(f"arc-plus must be 0|1.5|3.0, got {self.arc_plus!r}")
        if self.iface not in IFACES:
            raise ValueError(f"iface must be I|II, got {self.iface!r}")
        if self.standoff not in STANDOFFS:
            raise ValueError(f"standoff must be 3.0|3.5|4.0, got {self.standoff!r}")
        if self.recess not in RECESSES:
            raise ValueError(f"recess must be 0|0.5, got {self.recess!r}")

    @property
    def tag(self) -> str:
        w = f"{self.width:.0f}"
        y = f"{self.lid_y:g}"
        s = f"{self.standoff:g}"
        base = f"{self.arch}_{self.cell}_{self.layout}_w{w}_y{y}_i{self.iface}_s{s}"
        if self.recess:
            base = f"{base}_r{self.recess:g}"
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


@dataclass(frozen=True, slots=True)
class RefTabRoute:
    """One WP11b candidate for the REF flex tab on the 501015 winner board."""

    name: str
    points: tuple[tuple[float, float], ...]
    y0: float
    y1: float
    length_mm: float
    length_added_mm: float
    min_wall_distance_mm: float
    min_side_wall_mm: float
    end_wall_crosses: bool
    end_wall_where: str
    in_cavity: bool
    bend_ok: bool
    notes: str


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
    cell_y0: float = FLOOR_Y
    nominal_clearance: float = 0.0
    deformed_clearance: float = 0.0
    floor_web: float = FLOOR_Y
    stack_over_module: float = 0.0
    outer_zero: float = 0.0
    outer_at_lid: float = 0.0
    module_lid_clearance: float = 0.0
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
    st_y0, st_y1 = standoff_y(spec)
    if spec.iface == "I":
        # One board plane over the cavity. The cell lies under it on the floor.
        board_s = (CAVITY_S0 + END_CLEAR, CAVITY_S1_V1 + ds - END_CLEAR)
        board_underside = st_y1
        board_top = board_underside + BOARD_RIGID
    else:
        # Interface II: the rings are clamped under the standoffs, so each
        # standoff stands ring + standoff above the floor. The flex island
        # covers the SIG1 and SIG2 sites in every layout, so its underside
        # rests on the standoff tops (review r5; WP11 had the nut stack 4.0,
        # 0.5 below the 3.0 standoff's top).
        board_underside = st_y1
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
        "standoff_top_y": st_y1,
        "boss_top_y": st_y1 - BOSS_DROP,
        "cell_y0": FLOOR_Y - spec.recess,
        "total_chord": float(chord),
        "m1_gate": float(chord) + 3.0,
    }


def cell_clearance(spec: V2Spec) -> dict[str, float]:
    """Nominal and deformed under-board cell clearance (turn 09).

    Nominal: rigid board underside at the standoff top, cell top = packed
    height above the cell floor (inner floor minus recess).
    Deformed: board underside at the boss tops (0.5 below the standoff).
    """
    pack = CELL[spec.cell]["t"] + FOAM
    cell_above_inner = pack - spec.recess
    nominal = spec.standoff - cell_above_inner
    deformed = spec.standoff - BOSS_DROP - cell_above_inner
    cell_y0 = FLOOR_Y - spec.recess
    return {
        "pack": pack,
        "cell_y0": cell_y0,
        "cell_y1": cell_y0 + pack,
        "floor_web": cell_y0,
        "cell_above_inner": cell_above_inner,
        "nominal": nominal,
        "deformed": deformed,
    }


def module_stack(spec: V2Spec) -> dict[str, float]:
    """Module stack above the inner floor, then outer height at zero added clearance.

    Interface I: standoff + rigid board 1.0 + module. Interface II (review r5):
    ring + standoff + flex at parts (0.11 + 0.4 FR4) + module.
    """
    h = MODULE[spec.arch]["h"]
    board = BOARD_RIGID if spec.iface == "I" else BOARD_AT_PARTS
    stack = ring_under(spec) + spec.standoff + board + h
    outer_zero = FLOOR_Y + stack + LID_THICK
    outer_lid = spec.lid_y + LID_THICK
    module_top = FLOOR_Y + stack
    return {
        "module_h": h,
        "stack": stack,
        "outer_zero": outer_zero,
        "outer_lid": outer_lid,
        "module_top": module_top,
        "module_lid_clearance": spec.lid_y - module_top,
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


def _bend_ok(points: tuple[tuple[float, float], ...], radius: float | None = None) -> bool:
    r = BEND_R if radius is None else radius
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
        need = r * math.tan(theta / 2.0) if theta < math.pi - 1e-9 else math.inf
        if n1 < need or n2 < need:
            return False
    return True


def _make_tabs(spec: V2Spec, geom: dict[str, Any]) -> dict[str, TabPath]:
    if spec.iface == "I":
        return {}
    bs0, bs1 = geom["board_s"]
    # Straight runs, no 90° jog. Bend radius is free on a straight tab.
    sig1_end_s = min(CONTACT_1[1] + 7.0, bs1 - TAB_ATTACH_INSET)
    sig2_end_s = max(CONTACT_2[1] - 7.0, bs0 + TAB_ATTACH_INSET)
    ref_end_s = bs1 - TAB_ATTACH_INSET
    return {
        "SIG1": TabPath("SIG1", (CONTACT_1, (CONTACT_1[0], sig1_end_s))),
        "SIG2": TabPath("SIG2", (CONTACT_2, (CONTACT_2[0], sig2_end_s))),
        "REF": TabPath("REF", (CONTACT_REF, (CONTACT_REF[0], ref_end_s))),
    }


def _ref_attach(geom: dict[str, Any]) -> tuple[float, float]:
    """Board-side end of the straight REF tab (same inset as ``_make_tabs``)."""
    return (CONTACT_REF[0], geom["board_s"][1] - TAB_ATTACH_INSET)


def _polyline_length(points: tuple[tuple[float, float], ...]) -> float:
    return float(sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(points, points[1:])))


def _sample_polyline(points: tuple[tuple[float, float], ...], step: float = 0.05) -> list[tuple[float, float]]:
    out: list[tuple[float, float]] = []
    for a, b in zip(points, points[1:]):
        dist = math.hypot(b[0] - a[0], b[1] - a[1])
        n = max(1, int(math.ceil(dist / step)))
        for k in range(n):
            t = k / n
            out.append((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
    out.append(points[-1])
    return out


def _in_ref_pocket(u: float, s: float) -> bool:
    return math.hypot(u - CONTACT_REF[0], s - CONTACT_REF[1]) <= POCKET_DIA / 2.0 + 1e-9


def _end_wall_span(geom: dict[str, Any]) -> tuple[float, float]:
    """s-range of nylon between the cavity end and the Ø7.5 REF pocket."""
    return (geom["cavity_s"][1], CONTACT_REF[1] - POCKET_DIA / 2.0)


def _crosses_end_wall(
    points: tuple[tuple[float, float], ...], geom: dict[str, Any]
) -> tuple[bool, str]:
    s0, s1 = _end_wall_span(geom)
    if s1 <= s0 + 1e-9:
        return False, "no"
    for u, s in _sample_polyline(points):
        if s0 < s < s1 and not _in_ref_pocket(u, s):
            return True, f"s {s0:.2f}–{s1:.2f} at u {u:.2f}"
    return False, "no"


def _min_side_wall_mm(points: tuple[tuple[float, float], ...], geom: dict[str, Any]) -> float:
    """Smallest tab-edge gap to a cavity side wall (u), on samples inside the cavity."""
    cu = geom["cavity_u"]
    cs = geom["cavity_s"]
    best = math.inf
    for u, s in _sample_polyline(points):
        if not (cs[0] - 1e-9 <= s <= cs[1] + 1e-9):
            continue
        gap = min(u - cu[0], cu[1] - u) - TAB_W / 2.0
        best = min(best, gap)
    return 0.0 if best is math.inf else float(best)


def _route_in_cavity(points: tuple[tuple[float, float], ...], geom: dict[str, Any]) -> bool:
    """True when every sample is in the cavity or in the REF pocket, never in the end wall."""
    if _crosses_end_wall(points, geom)[0]:
        return False
    cu, cs = geom["cavity_u"], geom["cavity_s"]
    for u, s in _sample_polyline(points):
        in_cavity = cu[0] - 1e-9 <= u <= cu[1] + 1e-9 and cs[0] - 1e-9 <= s <= cs[1] + 1e-9
        if not in_cavity and not _in_ref_pocket(u, s):
            return False
    return True


def _measure_ref_route(
    name: str,
    points: tuple[tuple[float, float], ...],
    y0: float,
    y1: float,
    geom: dict[str, Any],
    straight_len: float,
    notes: str,
) -> RefTabRoute:
    length = _polyline_length(points)
    crosses, where = _crosses_end_wall(points, geom)
    side = _min_side_wall_mm(points, geom)
    return RefTabRoute(
        name=name,
        points=points,
        y0=y0,
        y1=y1,
        length_mm=length,
        length_added_mm=length - straight_len,
        min_wall_distance_mm=0.0 if crosses else side,
        min_side_wall_mm=side,
        end_wall_crosses=crosses,
        end_wall_where=where,
        in_cavity=_route_in_cavity(points, geom),
        bend_ok=_bend_ok(points, BOARD_BEND_R),
        notes=notes,
    )


def ref_tab_routes(spec: V2Spec | None = None) -> list[RefTabRoute]:
    """Three in-cavity searches for the REF tab on the 501015 winner board (Q59).

    The ring stays at ``CONTACT_REF``. Flex at the tab is ``TAB_T`` (0.31). Bend
    radius is ``BOARD_BEND_R`` (board-v2.md §11). The default packing tab is
    unchanged: Stage B still measures the straight floor path.
    """
    spec = spec or stage_b_winner_spec()
    geom = body_geom(spec)
    attach = _ref_attach(geom)
    straight = (CONTACT_REF, attach)
    straight_len = _polyline_length(straight)
    y_floor0, y_floor1 = FLOOR_Y, FLOOR_Y + TAB_T
    cell = CELL[spec.cell]
    y_air0 = FLOOR_Y + cell["t"] + FOAM + 0.1
    y_air1 = y_air0 + TAB_T
    lat_u = geom["cavity_u"][0] + TAB_W / 2.0
    lateral = (CONTACT_REF, (lat_u, CONTACT_REF[1]), (lat_u, attach[1]), attach)
    s0, s1 = _end_wall_span(geom)
    wall_note = (
        f"cavity ends at s {s0:.2f}; Ø{POCKET_DIA:g} pocket starts at s {s1:.2f}; "
        f"{s1 - s0:.2f} mm of nylon between them"
    )
    return [
        _measure_ref_route(
            "along_floor",
            straight,
            y_floor0,
            y_floor1,
            geom,
            straight_len,
            "current packing tab, ring to board along s at u 8.50; " + wall_note,
        ),
        _measure_ref_route(
            "along_lateral_wall",
            lateral,
            y_floor0,
            y_floor1,
            geom,
            straight_len,
            f"hug posterior inner wall at u {lat_u:.2f}, then to the ring; "
            "the ring is past the cavity, so the high-s leg leaves cavity air; " + wall_note,
        ),
        _measure_ref_route(
            "over_pocket_air",
            straight,
            y_air0,
            y_air1,
            geom,
            straight_len,
            f"same (u, s) as along_floor at y {y_air0:.2f}–{y_air1:.2f} "
            f"(cell top {FLOOR_Y + cell['t'] + FOAM:.2f} + 0.10, lid {spec.lid_y:g}); "
            "cell-pocket free air at low s does not reach the tail site without the end wall; "
            + wall_note,
        ),
    ]


def best_ref_tab_route(spec: V2Spec | None = None) -> RefTabRoute | None:
    """The in-cavity route with least added length, or None if none stays in the cavity."""
    inside = [r for r in ref_tab_routes(spec) if r.in_cavity]
    if not inside:
        return None
    inside.sort(key=lambda r: (r.length_added_mm, r.length_mm, r.name))
    return inside[0]


def ref_end_wall_slot(spec: V2Spec | None = None) -> dict[str, float]:
    """Slot through the cavity end wall that contains the straight REF tab (WP14)."""
    spec = spec or stage_b_winner_spec()
    geom = body_geom(spec)
    s0, s1 = _end_wall_span(geom)
    u = CONTACT_REF[0]
    return {
        "u0": u - TAB_W / 2.0,
        "u1": u + TAB_W / 2.0,
        "s0": s0,
        "s1": s1,
        "y0": FLOOR_Y,
        "y1": FLOOR_Y + TAB_T,
        "u": u,
        "s": (s0 + s1) / 2.0,
        "width": TAB_W,
        "through": s1 - s0,
        "height": TAB_T,
    }


DTP_ARC_LID_YS = (7.0, 8.0, 8.5, 9.0)
DTP_ARC_STANDOFFS = (3.0, 4.0)
DTP_ARC_STEPS = (1.5, 3.0)


def dtp_arc_plus_specs() -> list[V2Spec]:
    """WP11b: DTP301120 series, interface II, arc +1.5 and +3.0 (Q55, Q57)."""
    specs: list[V2Spec] = []
    for width in WIDTHS:
        for lid_y in DTP_ARC_LID_YS:
            for standoff in DTP_ARC_STANDOFFS:
                for arc_plus in DTP_ARC_STEPS:
                    specs.append(
                        V2Spec("A", "dtp", "series", width, lid_y, arc_plus, "II", standoff, 0.0)
                    )
    return specs


_DTP_ARC_PLUS_ROWS: list[V2Result] | None = None


def run_dtp_arc_plus() -> list[V2Result]:
    global _DTP_ARC_PLUS_ROWS
    if _DTP_ARC_PLUS_ROWS is None:
        _DTP_ARC_PLUS_ROWS = [run_spec(s) for s in dtp_arc_plus_specs()]
    return _DTP_ARC_PLUS_ROWS


JAUCH_LID_YS = (7.0, 8.0, 8.5, 9.0)
JAUCH_STANDOFFS = (3.0, 4.0)
JAUCH_ARC_STEPS = (0.0, 1.5, 3.0)


def jauch_specs() -> list[V2Spec]:
    """WP11b: Jauch LP501218JH series, interface II, BODY_ARC and arc-plus (L7 §2)."""
    specs: list[V2Spec] = []
    for width in WIDTHS:
        for lid_y in JAUCH_LID_YS:
            for standoff in JAUCH_STANDOFFS:
                for arc_plus in JAUCH_ARC_STEPS:
                    specs.append(
                        V2Spec("A", "jauch", "series", width, lid_y, arc_plus, "II", standoff, 0.0)
                    )
    return specs


_JAUCH_ROWS: list[V2Result] | None = None


def run_jauch_series() -> list[V2Result]:
    global _JAUCH_ROWS
    if _JAUCH_ROWS is None:
        _JAUCH_ROWS = [run_spec(s) for s in jauch_specs()]
    return _JAUCH_ROWS


def buyable_ext_specs() -> list[V2Spec]:
    """WP11b note 2: DTP and Jauch, bigger lid and width, same round-5 checker."""
    specs: list[V2Spec] = []
    for cell in BUYABLE_EXT_CELLS:
        for width in BUYABLE_EXT_WIDTHS:
            for lid_y in BUYABLE_EXT_LID_YS:
                for standoff in DTP_ARC_STANDOFFS:
                    for arc_plus in ARC_STEPS:
                        specs.append(
                            V2Spec("A", cell, "series", width, lid_y, arc_plus, "II", standoff, 0.0)
                        )
    return specs


_BUYABLE_EXT_ROWS: list[V2Result] | None = None


def run_buyable_ext() -> list[V2Result]:
    global _BUYABLE_EXT_ROWS
    if _BUYABLE_EXT_ROWS is None:
        _BUYABLE_EXT_ROWS = [run_spec(s) for s in buyable_ext_specs()]
    return _BUYABLE_EXT_ROWS


def _brief_box_conflict(text: str) -> bool:
    return text == "body outside the ≤ 9.0 high and 20 wide cap"


def packing_conflicts(r: V2Result) -> list[str]:
    """Round-5 conflicts except the plan's ≤9×20 box, which this search leaves."""
    return [c for c in r.conflicts if not _brief_box_conflict(c)]


def packs_outside_brief_box(r: V2Result) -> bool:
    return not packing_conflicts(r)


PACK_LID_YS = (7.0, 8.0, 8.5, 9.0)
PACK_STANDOFFS = (3.0, 4.0)
PACK_CELLS = ("pack501015", "pack501012")


def pack_cell_specs() -> list[V2Spec]:
    """WP11b note 3: 501015 pack 17×10×5 and 501012 pack 13×10.1×5.1 (L7 §7)."""
    specs: list[V2Spec] = []
    for cell in PACK_CELLS:
        for width in WIDTHS:
            for lid_y in PACK_LID_YS:
                for standoff in PACK_STANDOFFS:
                    for arc_plus in ARC_STEPS:
                        specs.append(
                            V2Spec("A", cell, "series", width, lid_y, arc_plus, "II", standoff, 0.0)
                        )
    return specs


_PACK_CELL_ROWS: list[V2Result] | None = None


def run_pack_cells() -> list[V2Result]:
    global _PACK_CELL_ROWS
    if _PACK_CELL_ROWS is None:
        _PACK_CELL_ROWS = [run_spec(s) for s in pack_cell_specs()]
    return _PACK_CELL_ROWS


def winner_with_pack501015() -> V2Result:
    """The Stage B winner body, with the 17.0 mm 501015 pack in place of the bare cell."""
    w = stage_b_winner_spec()
    return run_spec(
        V2Spec(w.arch, "pack501015", w.layout, w.width, w.lid_y, w.arc_plus, w.iface, w.standoff, w.recess)
    )


def _place_cell(spec: V2Spec, geom: dict[str, Any], module: Box | None) -> Box:
    cell = CELL[spec.cell]
    cu = geom["cavity_u"]
    mid_u = (cu[0] + cu[1]) / 2.0
    y0 = geom.get("cell_y0", FLOOR_Y - spec.recess)
    y1 = y0 + cell["t"] + FOAM
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
        y0m = max(y0m, standoff_y(spec)[1] + 0.13)
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
    # Pack to low-u when a ≥ 2.4 mm side strip remains (B).
    if (bu1 - bu0) - wu >= 2.5:
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
    if ws >= wu:
        # Length along s: antenna end at the high-s board edge (interface §6.3).
        return box, (u - aw / 2.0, box.s1 - al, u + aw / 2.0, box.s1)
    # Length along u (review r5): the antenna is a short end of the module, so
    # the keep-out is `al` along u at the low-u end and `aw` along s, centred
    # on the module. WP11 kept the length-along-s rectangle for this pose,
    # which put 15 module pads inside it on the board (WP12 drew both zones).
    return box, (box.u0, s - aw / 2.0, box.u0 + al, s + aw / 2.0)


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
    y0, y1 = standoff_y(spec)
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
            ("TLV713", [(LDO[0], LDO[1]), (LDO[1], LDO[0])], LDO[2], None),
        ]
    items += [
        ("USBLC6", [(SOT23_6[0], SOT23_6[1]), (SOT23_6[1], SOT23_6[0])], SOT23_6[2], None),
        ("PESD_VBUS", [(SOD523[0], SOD523[1]), (SOD523[1], SOD523[0])], SOD523[2], None),
        ("JST_SH", [(JST[0], JST[1]), (JST[1], JST[0])], JST[2], None),
    ]
    leftover_first = list(regions)
    pocket_first = list(reversed(regions)) if spec.layout == "series" else leftover_first
    for name, sizes, h, near in items:
        # USB ESD sits by the hook-end USB, which is next to the pocket island.
        ranked = pocket_first if name in {"JST_SH", "USBLC6", "PESD_VBUS"} else leftover_first
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
    """Board-top area left after the antenna keep-out and every placed top-face courtyard.

    Rastered at RASTER on the board zone. Review r5: the lane's version never
    used ``parts`` (it subtracted the under-board keep-out circles only), so
    the column was the same for every layout of a width.
    """
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
    if antenna is not None:
        au0, as0, au1, as1 = antenna
        free &= ~((uu >= au0) & (uu <= au1) & (sss >= as0) & (sss <= as1))
    for box in parts.values():
        if box.face != "top" or box.y0 + 1e-9 < geom["board_top"]:
            continue
        free &= ~((uu >= box.u0) & (uu <= box.u1) & (sss >= box.s0) & (sss <= box.s1))
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
    if antenna is not None:
        au0, as0, au1, as1 = antenna
        seed.append(Box("antenna_keepout", (au0 + au1) / 2.0, (as0 + as1) / 2.0, au1 - au0, as1 - as0,
                        geom["board_top"], geom["board_top"] + 10.0, "top"))
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
    clr = cell_clearance(spec)
    stk = module_stack(spec)
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
        cell_y0=geom["cell_y0"],
        nominal_clearance=clr["nominal"],
        deformed_clearance=clr["deformed"],
        floor_web=clr["floor_web"],
        stack_over_module=stk["stack"],
        outer_zero=stk["outer_zero"],
        outer_at_lid=stk["outer_lid"],
        module_lid_clearance=spec.lid_y - parts["module"].y1,
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
        clr = cell_clearance(spec)
        cellb = r.parts.get("cell")
        under = cellb is not None and cellb.u0 < bu[1] and cellb.u1 > bu[0] and cellb.s0 < bs[1] and cellb.s1 > bs[0]
        if under and clr["nominal"] <= 1e-9:
            out.append(
                f"nominal cell clearance {clr['nominal']:+.1f} is not positive "
                f"(cell {clr['pack']:.1f} under standoff {spec.standoff:g}"
                f"{f' recess {spec.recess:g}' if spec.recess else ''})"
            )
        if under and clr["deformed"] <= 1e-9:
            out.append(
                f"cell would carry board load (deformed clearance {clr['deformed']:+.1f}; "
                f"bosses {BOSS_DROP:g} below standoff tops)"
            )
        stk = module_stack(spec)
        if stk["outer_zero"] > 9.0 + 1e-9:
            out.append(
                f"outer height {stk['outer_zero']:.1f} > 9.0 at zero added clearance "
                f"(standoff {spec.standoff:g}+board {BOARD_RIGID:g}+module {stk['module_h']:g}"
                f"+floor {FLOOR_Y:g}+lid {LID_THICK:g})"
            )
        # Review r5: every Interface I pad must be on the rigid board. The REF
        # site (s 43.0, tail pocket) is past the cavity end wall, so no rigid
        # board in this matrix reaches it; WP11 never checked.
        for pname in ("pad_SIG1", "pad_SIG2", "pad_REF"):
            pad = r.parts.get(pname)
            if pad is not None and not _in_rect(pad.u, pad.s, pad.wu, pad.ws, bu, bs):
                out.append(
                    f"{pname} {pad.wu:g}×{pad.ws:g} at ({pad.u:.2f},{pad.s:.2f}) is off the rigid board "
                    f"(u {bu[0]:.2f}–{bu[1]:.2f}, s {bs[0]:.2f}–{bs[1]:.2f})"
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
        floor_min = (FLOOR_Y - spec.recess) if name == "cell" else FLOOR_Y
        if box.y0 < floor_min - 1e-9:
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
        if name == "module" or name.startswith("ADS") or name in {
            "BQ25100", "TLV713", "USBLC6", "PESD_VBUS", "JST_SH", "switch", "header"
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
        # Rectangle-to-rectangle distance in (u, s).
        du = max(0.0, au0 - cellb.u1, cellb.u0 - au1)
        ds = max(0.0, as0 - cellb.s1, cellb.s0 - as1)
        gap = math.hypot(du, ds)
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
                # Parts on or above the standoff top clear it (review r5: the
                # test was against the board underside, which let a 3.0
                # standoff stand through a board at 4.0 in interface II).
                if a.startswith("standoff") and r.parts[b].y0 + 1e-9 >= r.parts[a].y1:
                    continue
                if b.startswith("standoff") and r.parts[a].y0 + 1e-9 >= r.parts[b].y1:
                    continue
                out.append(f"{a} overlaps {b}")

    # The board slab against every standoff it covers (review r5).
    board_box = Box("board", (bu[0] + bu[1]) / 2.0, (bs[0] + bs[1]) / 2.0, bu[1] - bu[0], bs[1] - bs[0],
                    r.board_underside, r.board_top, "top")
    for name, box in r.parts.items():
        if name.startswith("standoff") and _overlap(board_box, box):
            out.append(f"{name} top {box.y1:.2f} stands through the board underside {r.board_underside:.2f}")

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
                            if iface == "I":
                                combos = [(st, 0.0) for st in STANDOFFS]
                                combos += [(st, CELL_RECESS) for st in (3.5, 4.0)]
                            else:
                                combos = [(3.0, 0.0)]
                            for st, rec in combos:
                                specs.append(
                                    V2Spec(a, c, lay, w, y, 0.0, iface, st, rec)
                                )
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
                        spec.recess,
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
        if name in {"USBLC6", "PESD_VBUS"}:
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
        f"standoff top y {r.standoff_top_y:.2f}  boss top y {r.boss_top_y:.2f}  recess {spec.recess:g}",
        f"cell clr nom {r.nominal_clearance:+.1f}  def {r.deformed_clearance:+.1f}  web {r.floor_web:.1f}",
        f"stack {r.stack_over_module:.1f} (standoff+1.0+mod)  outer0 {r.outer_zero:.1f}  outer@lid {r.outer_at_lid:.1f}",
        f"module-to-lid {r.module_lid_clearance:+.2f}",
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


STAGE_B_V2_TOML = ROOT / "scripts" / "cad" / "params" / "stageb_v2.toml"
MAX_KEPT_DRAWINGS = 40  # Q56: the repo keeps closers, the Stage B winner, one per family


def conflict_family(text: str) -> str:
    """A first conflict with its numbers replaced by '#', so runs group by rule."""
    return re.sub(r"[-+]?\d+(?:\.\d+)?", "#", text)


def stage_b_winner_spec(path: Path | None = None) -> V2Spec:
    """The V2Spec the Stage B v2 parameter file builds."""
    import tomllib

    data = tomllib.loads((path or STAGE_B_V2_TOML).read_text(encoding="utf-8"))
    return V2Spec(
        str(data.get("V2_ARCH", "A")),
        str(data.get("V2_CELL", "501015")),
        str(data.get("V2_LAYOUT", "series")),
        float(data.get("V2_WIDTH", 20.0)),
        float(data.get("V2_LID_Y", 8.0)),
        float(data.get("V2_ARC_PLUS", 0.0)),
        str(data.get("V2_IFACE", "I")),
        float(data.get("V2_STANDOFF", 3.5)),
        float(data.get("V2_RECESS", 0.0)),
    )


def family_representatives(rows: list[V2Result]) -> dict[str, V2Result]:
    """First failing run, in matrix order, of each first-conflict family."""
    out: dict[str, V2Result] = {}
    for r in rows:
        if r.closes:
            continue
        out.setdefault(conflict_family(r.first_conflict), r)
    return out


def kept_drawing_specs(rows: list[V2Result]) -> list[V2Spec]:
    """Drawings committed to the repo: closers, the Stage B winner, one per family."""
    specs: list[V2Spec] = [r.spec for r in rows if r.closes]
    winner = stage_b_winner_spec()
    if winner not in specs:
        specs.append(winner)
    for r in family_representatives(rows).values():
        if r.spec not in specs:
            specs.append(r.spec)
    if len(specs) > MAX_KEPT_DRAWINGS:
        raise RuntimeError(f"{len(specs)} kept drawings > {MAX_KEPT_DRAWINGS} (Q56)")
    return specs


def write_all_drawings(
    *,
    include_arc: bool = False,
    dest_dir: Path | None = None,
    which: str = "closers",
) -> list[tuple[V2Spec, str]]:
    """Write one SVG per selected run. Returns (spec, sha256) rows.

    ``which``: "closers" (default, placement.py --all), "kept" (closers, the
    Stage B winner and one per first-conflict family: the committed set,
    placement.py --kept-drawings) or "all" (every run, placement.py
    --all-drawings; 864 files, about 109 MB, never committed, Q56).
    """
    rows = run_matrix(include_arc=include_arc)
    by_spec = {r.spec: r for r in rows}
    if which == "all":
        specs = [r.spec for r in rows]
    elif which == "kept":
        specs = kept_drawing_specs(rows)
    elif which == "closers":
        specs = [r.spec for r in rows if r.closes]
    else:
        raise ValueError(f"which must be closers|kept|all, got {which!r}")
    out: list[tuple[V2Spec, str]] = []
    for spec in specs:
        path = (dest_dir / spec.filename) if dest_dir is not None else drawing_path(spec)
        digest = write_drawing(spec, path, by_spec.get(spec))
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
        "V2_RECESS": spec.recess,
        "MOCK_CONTACTS": False,
        "CONTACT_SOURCE": (
            "interface I gold pads on standoff tops (WP11 turn 07)"
            if spec.iface == "I"
            else "interface II flex tabs under standoffs (WP11)"
        ),
    }


# Stage B v2 on the built solid (stageb_v2.toml), review r5. status is
# "pass", "fail" or "NOT_MEASURED"; numbers are the manifest's. The CAD test
# CadStageBV2BuildTests checks every row against a fresh build.
STAGE_B_V2_MEASURED: dict[str, tuple[str, dict[str, float], str]] = {
    "V2_CELL_envelope": ("pass", {"body_mm3": 0.0, "lid_mm3": 0.0, "y1": 7.2}, ""),
    "V2_MODULE_envelope": ("pass", {"body_mm3": 0.0, "lid_mm3": 0.0, "y1": 7.62}, ""),
    "V2_BOARD_envelope": ("pass", {"body_mm3": 0.0, "lid_mm3": 0.0, "underside": 4.81, "top": 5.32}, ""),
    "V2_TAB_envelope": (
        "fail",
        {"REF_body_mm3": 1.194, "SIG1_body_mm3": 0.0, "SIG2_body_mm3": 0.0},
        "the floor-level REF tab crosses the cavity end wall (s 38.2 to the Ø7.5 pocket at 39.25); "
        "needs a slot in that wall (WP14, decision 59)",
    ),
    "REF_WIRE_envelope": ("fail", {"body_mm3": 1.1902, "lid_mm3": 0.0}, "same end-wall crossing"),
    "V2_CONTACT_STACK": ("pass", {"stack_top_y": 4.81, "board_underside": 4.81, "tip_below_top": 0.81}, ""),
    "V2_STANDOFF": ("pass", {"standoff_SIG1_body_mm3": 0.0, "standoff_SIG2_body_mm3": 0.0, "standoff_REF_body_mm3": 0.0}, ""),
    "Q21_REF_lug": ("pass", {"stack_top_y": 4.81, "pocket_r": 3.75, "standoff_circumr": 2.9}, ""),
    "V2_LID_band": ("pass", {"lid_underside_y": 8.0}, ""),
    "V2_STACK": ("pass", {"module_top_y": 7.62, "lid_over_module": 8.0, "module_lid_gap": 0.38}, ""),
    "V2_WALL_minima": ("pass", {"anterior_wall": 1.5, "posterior_wall": 1.5}, ""),
    "V2_TOTAL_CHORD": ("pass", {"TOTAL_CHORD": 47.9005, "packing_TOTAL_CHORD": 47.9005}, ""),
    "V2_M1_gate": ("pass", {"gate": 50.9005, "M1": 52.0}, ""),
    "V2_CELL_CLEARANCE": ("pass", {"cell_s1": 17.1, "board_s0": 18.6}, "cell beside the board"),
    "TAB_envelope_air": ("NOT_MEASURED", {}, "the TE 31428 tab envelope is not the v2 flex tab; V2_TAB_envelope measures the tabs"),
    "V2_ADJUSTMENT": ("NOT_MEASURED", {"region_mm": 0.8}, "±0.8 is the Interface I pad/standoff formula, not a solid probe"),
    "V2_BOSS": ("NOT_MEASURED", {}, "Interface II has no board bosses; flex retention is WP14's and G7's"),
    "V2_RECESS": ("NOT_MEASURED", {}, "the 0.5 floor recess and 1.0 web (C15) are not on the order-1 solid"),
    "V2_USB_medial": ("NOT_MEASURED", {}, "the order-1 solid has no USB cut; packing reports the hook-end end face"),
    "V2_HARNESS": ("NOT_MEASURED", {}, "100 ± 3 mm is a routed length"),
}


def _md_cell(text: str) -> str:
    return text.replace("|", "/").replace("\n", " ")


def _dtp_arc_plus_section(winner_chord: float) -> list[str]:
    """WP11b table: DTP series, interface II, arc +1.5 and +3.0."""
    rows = run_dtp_arc_plus()
    closed = [r for r in rows if r.closes]
    lines: list[str] = []
    lines.append("## 1b. DTP301120 arc-plus under interface II (WP11b)")
    lines.append("")
    lines.append(
        "DTP301120 22.0 × 11.5 × 3.2, foam 0.5 (Q57), series, interface II, architecture A. "
        f"Widths {WIDTHS[0]:g} to {WIDTHS[-1]:g}, LID_Y {DTP_ARC_LID_YS[0]:g} to {DTP_ARC_LID_YS[-1]:g} "
        f"(the v2 lid steps in that range), standoffs {DTP_ARC_STANDOFFS[0]:g} and {DTP_ARC_STANDOFFS[1]:g}. "
        "Conflict logic is the round 5 checker (no new constants). "
        f"{len(rows)} runs."
    )
    lines.append("")
    lines.append(
        "| arch | standoff | width | lid | arc+ | closes | first conflict | TOTAL_CHORD | M1 gate |"
    )
    lines.append("|---|---:|---:|---:|---:|---|---|---:|---:|")
    for r in rows:
        spec = r.spec
        first = "—" if r.closes else _md_cell(r.first_conflict)
        lines.append(
            f"| {spec.arch} | {spec.standoff:g} | {spec.width:g} | {spec.lid_y:g} | {spec.arc_plus:g} | "
            f"{'yes' if r.closes else 'no'} | {first} | {r.total_chord:.2f} | {r.m1_gate:.2f} |"
        )
    lines.append("")
    if closed:
        closed.sort(key=lambda r: (r.spec.width, r.spec.lid_y, r.spec.arc_plus, r.spec.standoff))
        best = closed[0]
        cost = best.total_chord - winner_chord
        lines.append(
            f"{len(closed)} of {len(rows)} close. Smallest body: `{best.spec.tag}`. "
            f"TOTAL_CHORD {best.total_chord:.2f} against M1−3 = {M1_DEFAULT - 3.0:.2f} "
            f"(M1 = {M1_DEFAULT:g}, Q34). Length cost versus the 501015 winner chord {winner_chord:.2f}: "
            f"{cost:+.2f} mm."
        )
    else:
        plus3 = next(r for r in rows if r.spec.arc_plus == 3.0)
        plus15 = next(r for r in rows if r.spec.arc_plus == 1.5)
        cost3 = plus3.total_chord - winner_chord
        lines.append(
            f"0 of {len(rows)} close at +1.5 or +3.0. There is no DTP body that closes. "
            f"At +1.5 mm of arc, TOTAL_CHORD {plus15.total_chord:.2f} against M1−3 = {M1_DEFAULT - 3.0:.2f} "
            f"(M1 = {M1_DEFAULT:g}, Q34 blank, default.toml). "
            f"At +3.0 mm of arc, TOTAL_CHORD {plus3.total_chord:.2f} (M1 gate {plus3.m1_gate:.2f}). "
            f"Length cost versus the 501015 winner chord {winner_chord:.2f} is not a closer: "
            f"+3.0 mm of arc is {cost3:+.2f} mm of chord. First conflict of each run is in the table."
        )
    fam_counts: dict[str, int] = {}
    for r in rows:
        if not r.closes:
            key = conflict_family(r.first_conflict)
            fam_counts[key] = fam_counts.get(key, 0) + 1
    if fam_counts:
        lines.append("")
        lines.append("First-conflict families (numbers masked), failing DTP arc-plus runs:")
        lines.append("")
        lines.append("| family | runs |")
        lines.append("|---|---:|")
        for fam, n in sorted(fam_counts.items(), key=lambda kv: (-kv[1], kv[0])):
            lines.append(f"| {_md_cell(fam)} | {n} |")
    lines.append("")
    return lines


def _smallest_closed(rows: list[V2Result]) -> V2Result | None:
    closed = [r for r in rows if r.closes]
    if not closed:
        return None
    closed.sort(key=lambda r: (r.spec.width, r.spec.lid_y, r.spec.arc_plus, r.spec.standoff, r.total_chord))
    return closed[0]


def _jauch_section(winner_chord: float) -> list[str]:
    """WP11b table: Jauch LP501218JH, interface II, BODY_ARC and arc-plus (L7 §2)."""
    rows = run_jauch_series()
    closed = [r for r in rows if r.closes]
    cell = CELL["jauch"]
    lines: list[str] = []
    lines.append("## 1c. Jauch LP501218JH under interface II (WP11b, L7 §2)")
    lines.append("")
    lines.append(
        f"Jauch Quartz {cell['name']}+PCM {cell['t']:g} × {cell['w']:g} × {cell['l']:g}, foam {FOAM:g} (Q57), "
        "series, interface II, architecture A. Widths 18 to 20, LID_Y 7 to 9, standoffs 3 and 4, "
        "BODY_ARC 48.4 and arc-plus +1.5 and +3.0. Conflict logic is the round 5 checker "
        f"(no new constants). {len(rows)} runs. Source: `docs/fab/L7-research-v4.md` §2 "
        "(DigiKey `1908-LP501218JH+PCM+2WIRE50MM-ND`, 60 mAh, page price and stock on 2026-09-17)."
    )
    lines.append("")
    lines.append(
        "Bare 2-wire leads (28 AWG, 50 ± 3 mm, no connector) per L7 §2. Plan v2 R2: "
        "Rolf solders nothing (no soldering, glue, crimping or wire stripping). "
        "This cell is a packing candidate only if the assembler or the seller terminates the leads."
    )
    lines.append("")
    lines.append(
        "| arch | standoff | width | lid | arc+ | closes | first conflict | TOTAL_CHORD | M1 gate |"
    )
    lines.append("|---|---:|---:|---:|---:|---|---|---:|---:|")
    for r in rows:
        spec = r.spec
        first = "—" if r.closes else _md_cell(r.first_conflict)
        lines.append(
            f"| {spec.arch} | {spec.standoff:g} | {spec.width:g} | {spec.lid_y:g} | {spec.arc_plus:g} | "
            f"{'yes' if r.closes else 'no'} | {first} | {r.total_chord:.2f} | {r.m1_gate:.2f} |"
        )
    lines.append("")
    best = _smallest_closed(rows)
    if best is not None:
        cost = best.total_chord - winner_chord
        lines.append(
            f"{len(closed)} of {len(rows)} close. Smallest body: `{best.spec.tag}`. "
            f"TOTAL_CHORD {best.total_chord:.2f} against M1−3 = {M1_DEFAULT - 3.0:.2f} "
            f"(M1 = {M1_DEFAULT:g}, Q34). Length cost versus the 501015 winner chord {winner_chord:.2f}: "
            f"{cost:+.2f} mm."
        )
    else:
        plus0 = next(r for r in rows if r.spec.arc_plus == 0.0)
        plus3 = next(r for r in rows if r.spec.arc_plus == 3.0)
        cost3 = plus3.total_chord - winner_chord
        lines.append(
            f"0 of {len(rows)} close at BODY_ARC or +1.5 or +3.0. There is no Jauch body that closes. "
            f"At BODY_ARC, TOTAL_CHORD {plus0.total_chord:.2f} against M1−3 = {M1_DEFAULT - 3.0:.2f}. "
            f"At +3.0 mm of arc, TOTAL_CHORD {plus3.total_chord:.2f} "
            f"({cost3:+.2f} mm of chord versus the 501015 winner). "
            "First conflict of each run is in the table."
        )
    fam_counts: dict[str, int] = {}
    for r in rows:
        if not r.closes:
            key = conflict_family(r.first_conflict)
            fam_counts[key] = fam_counts.get(key, 0) + 1
    if fam_counts:
        lines.append("")
        lines.append("First-conflict families (numbers masked), failing Jauch runs:")
        lines.append("")
        lines.append("| family | runs |")
        lines.append("|---|---:|")
        for fam, n in sorted(fam_counts.items(), key=lambda kv: (-kv[1], kv[0])):
            lines.append(f"| {_md_cell(fam)} | {n} |")
    lines.append("")
    return lines


def _never_clears_families(rows: list[V2Result]) -> list[str]:
    keys: list[set[str]] = []
    for r in rows:
        pc = packing_conflicts(r)
        keys.append({conflict_family(c) for c in pc})
    if not keys:
        return []
    common = set.intersection(*keys)
    return sorted(common)


def _buyable_ext_section(winner_chord: float, winner_row: V2Result | None) -> list[str]:
    """WP11b note 2: DTP and Jauch at LID_Y 9.5–10.5 and width 20–22."""
    rows = run_buyable_ext()
    winner_outer = winner_row.outer_at_lid if winner_row is not None else 9.0
    winner_lid = winner_row.spec.lid_y if winner_row is not None else 8.0
    winner_width = winner_row.spec.width if winner_row is not None else 20.0
    lines: list[str] = []
    lines.append("## 1d. Bigger body for the two buyable cells (WP11b note 2)")
    lines.append("")
    lines.append(
        "DTP301120 and LP501218JH only. Series, interface II, architecture A, foam 0.5, "
        "standoffs 3 and 4, BODY_ARC and arc-plus +1.5 and +3.0. LID_Y 9.5, 10.0 and 10.5; "
        "widths 20, 21 and 22. Conflict logic is the round 5 checker (no new constants). "
        f"{len(rows)} runs. The plan's ≤ 9.0 high and 20 wide cap still records a conflict; "
        "a run packs here if that cap is the only remaining conflict, so the table can "
        "answer how much bigger a buyable cell needs."
    )
    lines.append("")
    lines.append(
        "| cell | standoff | width | lid | outer | arc+ | packs | first packing conflict | TOTAL_CHORD | M1 gate |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|---|---|---:|---:|")
    for r in rows:
        spec = r.spec
        pc = packing_conflicts(r)
        packs = not pc
        first = "—" if packs else _md_cell(pc[0])
        lines.append(
            f"| {CELL[spec.cell]['name']} | {spec.standoff:g} | {spec.width:g} | {spec.lid_y:g} | "
            f"{r.outer_at_lid:.1f} | {spec.arc_plus:g} | {'yes' if packs else 'no'} | {first} | "
            f"{r.total_chord:.2f} | {r.m1_gate:.2f} |"
        )
    lines.append("")
    n_full = sum(1 for r in rows if r.closes)
    n_pack = sum(1 for r in rows if packs_outside_brief_box(r))
    lines.append(
        f"{n_full} of {len(rows)} close under every round-5 check (including the ≤9×20 cap). "
        f"{n_pack} of {len(rows)} pack if that cap is set aside. No new drawing: Q56 keeps closers only."
    )
    for cell_key, label in (("dtp", "DTP301120"), ("jauch", "LP501218JH")):
        cr = [r for r in rows if r.spec.cell == cell_key]
        packed = [r for r in cr if packs_outside_brief_box(r)]
        never = _never_clears_families(cr)
        lines.append("")
        if packed:
            packed.sort(
                key=lambda r: (r.spec.width, r.spec.lid_y, r.spec.arc_plus, r.spec.standoff, r.total_chord)
            )
            best = packed[0]
            hcost = best.outer_at_lid - winner_outer
            ccost = best.total_chord - winner_chord
            wcost = best.spec.width - winner_width
            lines.append(
                f"- **{label}**: smallest packing body `{best.spec.tag}`. "
                f"Width {best.spec.width:g} ({wcost:+.0f} mm vs winner {winner_width:g}), "
                f"LID_Y {best.spec.lid_y:g} (winner {winner_lid:g}), "
                f"outer thickness {best.outer_at_lid:.1f} ({hcost:+.1f} mm vs winner {winner_outer:.1f}), "
                f"TOTAL_CHORD {best.total_chord:.2f} against M1−3 = {M1_DEFAULT - 3.0:.2f} "
                f"({ccost:+.2f} mm vs winner {winner_chord:.2f})."
            )
        else:
            plus0 = next(r for r in cr if r.spec.arc_plus == 0.0)
            plus3 = next(r for r in cr if r.spec.arc_plus == 3.0)
            fams = ", ".join(f"`{f}`" for f in never) if never else "none"
            hmax = max(r.outer_at_lid for r in cr)
            lines.append(
                f"- **{label}**: no body packs. Family that never clears: {fams}. "
                f"Height cost: no closer; the search reaches LID_Y 10.5, outer {hmax:.1f} "
                f"({hmax - winner_outer:+.1f} mm vs winner outer {winner_outer:.1f}). "
                f"Chord cost: no closer; BODY_ARC TOTAL_CHORD {plus0.total_chord:.2f} "
                f"(same as the 501015 winner {winner_chord:.2f}); +3.0 mm of arc is "
                f"{plus3.total_chord:.2f} ({plus3.total_chord - winner_chord:+.2f} mm) and fails "
                f"M1−3 = {M1_DEFAULT - 3.0:.2f}."
            )
    fam_counts: dict[str, int] = {}
    for r in rows:
        pc = packing_conflicts(r)
        if pc:
            key = conflict_family(pc[0])
            fam_counts[key] = fam_counts.get(key, 0) + 1
    if fam_counts:
        lines.append("")
        lines.append("First packing-conflict families (numbers masked), failing bigger-box runs:")
        lines.append("")
        lines.append("| family | runs |")
        lines.append("|---|---:|")
        for fam, n in sorted(fam_counts.items(), key=lambda kv: (-kv[1], kv[0])):
            lines.append(f"| {_md_cell(fam)} | {n} |")
    lines.append("")
    return lines


def _pack_cells_section(winner_chord: float, winner_row: V2Result | None) -> list[str]:
    """WP11b note 3: 501015 pack 17×10×5 and 501012 pack 13×10.1×5.1 (L7 §7)."""
    rows = run_pack_cells()
    winner_outer = winner_row.outer_at_lid if winner_row is not None else 9.0
    winner_width = winner_row.spec.width if winner_row is not None else 20.0
    overlay = winner_with_pack501015()
    overlay_geom = body_geom(overlay.spec)
    winner_geom = body_geom(winner_row.spec) if winner_row is not None else None
    p15 = CELL["pack501015"]
    p12 = CELL["pack501012"]
    lines: list[str] = []
    lines.append("## 1e. 501015 pack and 501012 pack under interface II (WP11b note 3, L7 §7)")
    lines.append("")
    lines.append(
        f"L7-research-v4.md §7 and §7.8: a 501015 pack **with** its protection board is "
        f"{p15['l']:.1f} × {p15['w']:.1f} × {p15['t']:.1f} mm on the manufacturers' sheets "
        "(DNK Power DNK501015 'Dimensions: 17 × 10 × 5.0 mm', Benzo '5mm x 10mm x 17mm'). "
        "The plan's envelope 15.6 × 10.4 × 5.2 is a bare cell, not a pack. Packs that fit "
        f"under 16 mm exist only as marketplace listings. This search uses the 501012 pack "
        f"{p12['l']:.1f} × {p12['w']:.1f} × {p12['t']:.1f} with PCM, 40 mAh (eBay quote "
        "'approx 13.0mm x 10.1mm x 5.1mm'). The 401012 listing is not run here."
    )
    lines.append("")
    lines.append(
        "Series, interface II, architecture A, foam 0.5, standoffs 3.0 and 4.0, widths 18 to 20, "
        "LID_Y 7 to 9, BODY_ARC and arc-plus +1.5 and +3.0. Conflict logic is the round 5 checker "
        f"(no new constants). {len(rows)} runs. Neither cell is in the 864-run matrix."
    )
    lines.append("")
    if winner_geom is not None:
        wb, ob = winner_geom["board_s"], overlay_geom["board_s"]
        lines.append(
            f"The current winner `{stage_b_winner_spec().tag}` with the real 17.0 mm pack "
            f"(`{overlay.spec.tag}`) does **not** close. First conflict: "
            f"`{overlay.first_conflict}`. The 17.0 mm body length moves the pocket and shortens "
            f"the board from s {wb[0]:.1f}–{wb[1]:.1f} (bare 15.6 mm cell) to "
            f"{ob[0]:.1f}–{ob[1]:.1f}. Packed height {p15['t']:.1f} + {FOAM:.1f} = "
            f"{p15['t'] + FOAM:.1f} (cell top {FLOOR_Y + p15['t'] + FOAM:.1f}). "
            "No body in this grid closes for the 17.0 mm pack. No first-conflict family is "
            "present on every run. On the winner body, BODY_ARC fails first as "
            "`BQ25100 overlaps header` (also TLV713 and switch overlap the header). "
            "Arc-plus +1.5 on that body leaves only "
            f"`TOTAL_CHORD {next(r for r in rows if r.spec.cell == 'pack501015' and r.spec.width == 20.0 and r.spec.lid_y == 8.0 and r.spec.standoff == 3.0 and r.spec.arc_plus == 1.5).total_chord:.2f} > M1−3 "
            f"({M1_DEFAULT - 3.0:.2f})`; the overlap clears, the M1 gate does not."
        )
    lines.append("")
    lines.append(
        "| arch | cell | standoff | width | lid | arc+ | closes | first conflict | TOTAL_CHORD | M1 gate | outer |"
    )
    lines.append("|---|---|---:|---:|---:|---:|---|---|---:|---:|---:|")
    for r in rows:
        spec = r.spec
        first = "—" if r.closes else _md_cell(r.first_conflict)
        lines.append(
            f"| {spec.arch} | {CELL[spec.cell]['name']} | {spec.standoff:g} | {spec.width:g} | "
            f"{spec.lid_y:g} | {spec.arc_plus:g} | {'yes' if r.closes else 'no'} | {first} | "
            f"{r.total_chord:.2f} | {r.m1_gate:.2f} | {r.outer_at_lid:.1f} |"
        )
    lines.append("")
    n_full = sum(1 for r in rows if r.closes)
    lines.append(
        f"{n_full} of {len(rows)} close under every round-5 check. "
        "Drawings of those closers are not added under `docs/fab/cad/v1/`: the round-5 "
        "14-file kept set is pinned (`placement_v2_*.svg` = `kept_drawing_specs` of the 864-run "
        f"matrix), and 14 + {n_full} would exceed the WP11b Q56 cap of 20."
    )
    for cell_key, label in (("pack501015", "501015 pack"), ("pack501012", "501012 pack")):
        cr = [r for r in rows if r.spec.cell == cell_key]
        closed = [r for r in cr if r.closes]
        never = _never_clears_families(cr)
        lines.append("")
        if closed:
            closed.sort(
                key=lambda r: (r.spec.width, r.spec.lid_y, r.spec.arc_plus, r.spec.standoff, r.total_chord)
            )
            best = closed[0]
            hcost = best.outer_at_lid - winner_outer
            ccost = best.total_chord - winner_chord
            wcost = best.spec.width - winner_width
            lines.append(
                f"- **{label}**: smallest closer `{best.spec.tag}`. "
                f"Width {best.spec.width:g} ({wcost:+.0f} mm vs winner {winner_width:g}), "
                f"LID_Y {best.spec.lid_y:g}, standoff {best.spec.standoff:g}, arc+ {best.spec.arc_plus:g}. "
                f"TOTAL_CHORD {best.total_chord:.2f} against M1−3 = {M1_DEFAULT - 3.0:.2f} "
                f"({ccost:+.2f} mm vs winner {winner_chord:.2f}). "
                f"Outer thickness {best.outer_at_lid:.1f} ({hcost:+.1f} mm vs winner {winner_outer:.1f})."
            )
        else:
            fams = ", ".join(f"`{f}`" for f in never) if never else "none (first conflict rotates)"
            plus0 = next(r for r in cr if r.spec.arc_plus == 0.0)
            plus15 = next(
                r for r in cr
                if r.spec.width == 20.0 and r.spec.lid_y == 8.0 and r.spec.standoff == 3.0 and r.spec.arc_plus == 1.5
            )
            plus3 = next(r for r in cr if r.spec.arc_plus == 3.0)
            lines.append(
                f"- **{label}**: no body closes. Family that never clears: {fams}. "
                f"Winner-body first conflict: `{overlay.first_conflict}`. "
                f"BODY_ARC TOTAL_CHORD {plus0.total_chord:.2f} (same as the 501015 winner "
                f"{winner_chord:.2f}). +1.5 mm of arc on the winner body is "
                f"{plus15.total_chord:.2f} and fails M1−3 = {M1_DEFAULT - 3.0:.2f}. "
                f"+3.0 mm of arc is {plus3.total_chord:.2f} "
                f"({plus3.total_chord - winner_chord:+.2f} mm)."
            )
    fam_counts: dict[str, int] = {}
    for r in rows:
        if not r.closes:
            key = conflict_family(r.first_conflict)
            fam_counts[key] = fam_counts.get(key, 0) + 1
    if fam_counts:
        lines.append("")
        lines.append("First-conflict families (numbers masked), failing pack-cell runs:")
        lines.append("")
        lines.append("| family | runs |")
        lines.append("|---|---:|")
        for fam, n in sorted(fam_counts.items(), key=lambda kv: (-kv[1], kv[0])):
            lines.append(f"| {_md_cell(fam)} | {n} |")
    lines.append("")
    return lines


def _buyable_cell_compare_section(matrix_rows: list[V2Result], winner_chord: float) -> list[str]:
    """Smallest closer per cell: 501015, DTP301120, Jauch LP501218JH."""
    dtp_rows = [r for r in matrix_rows if r.spec.cell == "dtp" and r.spec.iface == "II" and r.spec.layout == "series"]
    dtp_rows = dtp_rows + run_dtp_arc_plus()
    rows_501015 = [
        r for r in matrix_rows
        if r.spec.cell == "501015" and r.spec.iface == "II" and r.spec.layout == "series" and r.spec.arch == "A"
    ]
    jauch_rows = run_jauch_series()
    lines: list[str] = []
    lines.append("### Smallest body per buyable cell (WP11b, L7 §2)")
    lines.append("")
    lines.append(
        "L7-research-v4.md §2 found no 501015-class cell sold in ones. "
        "The two buyable packs with page price, stock and a drawing are DTP301120 and LP501218JH."
    )
    lines.append("")
    lines.append(
        "| cell | sold in ones | smallest closer | width | lid | standoff | arc+ | TOTAL_CHORD | vs 501015 winner |"
    )
    lines.append("|---|---|---|---:|---:|---:|---:|---:|---:|")

    def row_for(label: str, sold: str, rows: list[V2Result]) -> str:
        best = _smallest_closed(rows)
        if best is None:
            return (
                f"| {label} | {sold} | none | — | — | — | — | — | no closer |"
            )
        cost = best.total_chord - winner_chord
        vs = "—" if abs(cost) < 1e-9 else f"{cost:+.2f} mm chord"
        return (
            f"| {label} | {sold} | `{best.spec.tag}` | {best.spec.width:g} | {best.spec.lid_y:g} | "
            f"{best.spec.standoff:g} | {best.spec.arc_plus:g} | {best.total_chord:.2f} | {vs} |"
        )

    pack_rows = run_pack_cells()
    lines.append(row_for("501015", "no (L7 §2)", rows_501015))
    lines.append(row_for("DTP301120", "yes, SparkFun PRT-25270", dtp_rows))
    lines.append(
        row_for(
            "LP501218JH",
            "yes, DigiKey (bare leads; needs a terminator)",
            jauch_rows,
        )
    )
    lines.append(
        row_for(
            "501015 pack",
            "sheets (DNK/Benzo with PCM; L7 §7.8); not sold as a verified one-off here",
            [r for r in pack_rows if r.spec.cell == "pack501015"],
        )
    )
    lines.append(
        row_for(
            "501012 pack",
            "marketplace listing (eBay quote with PCM; L7 §7)",
            [r for r in pack_rows if r.spec.cell == "pack501012"],
        )
    )
    lines.append("")
    ext = run_buyable_ext()
    winner_hit = _smallest_closed(rows_501015)
    winner_outer = winner_hit.outer_at_lid if winner_hit is not None else 9.0
    lines.append(
        "Extended (WP11b note 2): LID_Y 9.5, 10.0 and 10.5; widths 20, 21 and 22. "
        "A run packs if the only extra conflict is the plan's ≤ 9.0 high and 20 wide cap."
    )
    lines.append("")
    lines.append(
        "| cell | box | smallest closer | width | lid | outer | TOTAL_CHORD | height vs winner | chord vs winner | never-clears family |"
    )
    lines.append("|---|---|---|---:|---:|---:|---:|---:|---:|---|")
    if winner_hit is not None:
        lines.append(
            f"| 501015 | ≤9×20 | `{winner_hit.spec.tag}` | {winner_hit.spec.width:g} | "
            f"{winner_hit.spec.lid_y:g} | {winner_hit.outer_at_lid:.1f} | {winner_hit.total_chord:.2f} | "
            f"— | — | — |"
        )
    else:
        lines.append("| 501015 | ≤9×20 | none | — | — | — | — | — | — | — |")
    for cell_key, label in (("dtp", "DTP301120"), ("jauch", "LP501218JH")):
        cr = [r for r in ext if r.spec.cell == cell_key]
        packed = [r for r in cr if packs_outside_brief_box(r)]
        never = ", ".join(f"`{f}`" for f in _never_clears_families(cr)) if cr else "—"
        if packed:
            packed.sort(
                key=lambda r: (r.spec.width, r.spec.lid_y, r.spec.arc_plus, r.spec.standoff, r.total_chord)
            )
            best = packed[0]
            lines.append(
                f"| {label} | lid 9.5–10.5, w 20–22 | `{best.spec.tag}` | {best.spec.width:g} | "
                f"{best.spec.lid_y:g} | {best.outer_at_lid:.1f} | {best.total_chord:.2f} | "
                f"{best.outer_at_lid - winner_outer:+.1f} mm | "
                f"{best.total_chord - winner_chord:+.2f} mm | — |"
            )
        else:
            hmax = max(r.outer_at_lid for r in cr)
            plus3 = next(r for r in cr if r.spec.arc_plus == 3.0)
            ccost = plus3.total_chord - winner_chord
            lines.append(
                f"| {label} | lid 9.5–10.5, w 20–22 | none | — | — | {hmax:.1f} | — | "
                f"{hmax - winner_outer:+.1f} mm still open | +0 / {ccost:+.2f} mm, no closer | {never} |"
            )
    overlay = winner_with_pack501015()
    p15_rows = [r for r in pack_rows if r.spec.cell == "pack501015"]
    p12_rows = [r for r in pack_rows if r.spec.cell == "pack501012"]
    p12_closed = [r for r in p12_rows if r.closes]
    p15_never = ", ".join(f"`{f}`" for f in _never_clears_families(p15_rows)) or "none (first conflict rotates)"
    lines.append(
        f"| 501015 pack | ≤9×20 II series (L7 §7) | none | — | — | {overlay.outer_at_lid:.1f} | "
        f"{overlay.total_chord:.2f} | — | — | `{overlay.first_conflict}` on winner body; {p15_never} |"
    )
    if p12_closed:
        p12_closed.sort(
            key=lambda r: (r.spec.width, r.spec.lid_y, r.spec.arc_plus, r.spec.standoff, r.total_chord)
        )
        best12 = p12_closed[0]
        lines.append(
            f"| 501012 pack | ≤9×20 II series (L7 §7) | `{best12.spec.tag}` | {best12.spec.width:g} | "
            f"{best12.spec.lid_y:g} | {best12.outer_at_lid:.1f} | {best12.total_chord:.2f} | "
            f"{best12.outer_at_lid - winner_outer:+.1f} mm | "
            f"{best12.total_chord - winner_chord:+.2f} mm | — |"
        )
    else:
        lines.append(
            "| 501012 pack | ≤9×20 II series (L7 §7) | none | — | — | — | — | — | — | no closer |"
        )
    lines.append("")
    return lines


def _ref_tab_route_section() -> list[str]:
    """WP11b REF tab search on the 501015 winner board (Q59)."""
    routes = ref_tab_routes()
    slot = ref_end_wall_slot()
    best = best_ref_tab_route()
    lines: list[str] = []
    lines.append("### REF tab route (WP11b, Q59)")
    lines.append("")
    lines.append(
        f"Winner board `{stage_b_winner_spec().tag}`, tail site CONTACT_REF "
        f"({CONTACT_REF[0]:.2f}, {CONTACT_REF[1]:.2f}). Flex at the tab {TAB_T:g} "
        f"(PI {FLEX:g} + FR4 {STIFFENER_TAB:g}). Bend R {BOARD_BEND_R:g} (board-v2.md §11). "
        f"The packing tab itself is unchanged (Stage B still measures the straight floor path)."
    )
    lines.append("")
    lines.append(
        "| name | y | points | length | added | min wall | side wall | end wall | in cavity | bend R 1.5 |"
    )
    lines.append("|---|---|---|---:|---:|---:|---:|---|---|---|")
    for route in routes:
        pts = " → ".join(f"({u:.2f}, {s:.2f})" for u, s in route.points)
        wall = "no" if not route.end_wall_crosses else route.end_wall_where
        lines.append(
            f"| `{route.name}` | {route.y0:.2f}–{route.y1:.2f} | {pts} | {route.length_mm:.2f} | "
            f"{route.length_added_mm:+.2f} | {route.min_wall_distance_mm:.2f} | "
            f"{route.min_side_wall_mm:.2f} | {wall} | "
            f"{'yes' if route.in_cavity else 'no'} | {'yes' if route.bend_ok else 'no'} |"
        )
    lines.append("")
    for route in routes:
        lines.append(f"- `{route.name}`: {route.notes}")
    lines.append("")
    if best is not None:
        lines.append(
            f"Named layout: `{best.name}`. WP14 can cut that path; points and y are in the table."
        )
    else:
        lines.append(
            "No in-cavity route exists. The Ø7.5 tail pocket starts at s 39.25 and the cavity ends "
            "at s 38.20, so 1.05 mm of nylon sits between them. Every searched path crosses that wall. "
            "WP14 cuts a slot that contains the straight floor tab:"
        )
        lines.append("")
        lines.append("| item | number |")
        lines.append("|---|---|")
        lines.append(f"| name | `REF_end_wall_slot` |")
        lines.append(f"| u | {slot['u0']:.2f}–{slot['u1']:.2f} (centre {slot['u']:.2f}) |")
        lines.append(f"| s | {slot['s0']:.2f}–{slot['s1']:.2f} (centre {slot['s']:.2f}) |")
        lines.append(f"| y | {slot['y0']:.2f}–{slot['y1']:.2f} |")
        lines.append(f"| width | {slot['width']:.2f} |")
        lines.append(f"| through (s) | {slot['through']:.2f} |")
        lines.append(f"| height (y) | {slot['height']:.2f} |")
        lines.append(
            f"| volume (rect) | {slot['width'] * slot['through'] * slot['height']:.3f} mm³ |"
        )
    lines.append("")
    return lines


# ---------------------------------------------------------------------------
# WP11c — real courtyards and a board-lane layout (round 7).
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class KicadFootprint:
    ref: str
    footprint: str
    value: str
    at: tuple[float, float, float]
    cr_w: float
    cr_h: float
    pad_w: float
    pad_h: float


@dataclass(frozen=True, slots=True)
class LayoutPart:
    ref: str
    footprint: str
    u: float
    s: float
    rot: float
    cr_w: float
    cr_h: float
    pad_w: float
    pad_h: float
    wu: float
    ws: float
    face: str
    notes: str = ""


@dataclass
class LayoutV2:
    name: str
    spec: V2Spec
    parts: list[LayoutPart]
    keepouts: list[tuple[str, float, float, float, float]]
    rules: list[tuple[str, bool, str]]
    variants: list[str]
    first_blocking: str
    contacts_moved_mm: dict[str, float]


def _sexp_extract(text: str, start: int) -> tuple[str, int]:
    depth = 0
    i = start
    in_str = False
    while i < len(text):
        c = text[i]
        if in_str:
            if c == "\\":
                i += 2
                continue
            if c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
                if depth == 0:
                    return text[start : i + 1], i + 1
        i += 1
    raise ValueError("unbalanced s-expression")


_WP12B_PCB_TEXT: str | None = None
_WP12B_PRO_TEXT: str | None = None


def git_show(rev_path: str) -> str:
    return subprocess.check_output(["git", "show", rev_path], cwd=ROOT, encoding="utf-8")


def load_wp12b_pcb() -> str:
    global _WP12B_PCB_TEXT
    if _WP12B_PCB_TEXT is None:
        _WP12B_PCB_TEXT = git_show(f"{WP12B_REV}:{WP12B_PCB}")
    return _WP12B_PCB_TEXT


def load_wp12b_pro() -> str:
    global _WP12B_PRO_TEXT
    if _WP12B_PRO_TEXT is None:
        _WP12B_PRO_TEXT = git_show(f"{WP12B_REV}:{WP12B_PRO}")
    return _WP12B_PRO_TEXT


def contact_netclass_clearance(pro_text: str | None = None) -> float:
    text = pro_text if pro_text is not None else load_wp12b_pro()
    for block in re.finditer(r"\{[^{}]+\}", text):
        chunk = block.group(0)
        if '"name": "Contact"' not in chunk and '"name":"Contact"' not in chunk:
            continue
        match = re.search(r'"clearance":\s*([0-9.]+)', chunk)
        if match is None:
            raise ValueError("Contact netclass has no clearance")
        return float(match.group(1))
    raise ValueError("Contact netclass missing from WP12b elicio-v2.kicad_pro")


def _fp_bbox(pts: list[tuple[float, float]]) -> tuple[float, float]:
    if not pts:
        return (0.0, 0.0)
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return (max(xs) - min(xs), max(ys) - min(ys))


def parse_kicad_pcb(text: str) -> list[KicadFootprint]:
    """Courtyard rectangle and pad extent for every footprint on a KiCad PCB."""
    out: list[KicadFootprint] = []
    idx = 0
    while True:
        i = text.find("(footprint ", idx)
        if i < 0:
            break
        blob, idx = _sexp_extract(text, i)
        name_m = re.match(r'\(footprint "([^"]+)"', blob)
        if name_m is None:
            continue
        fpname = name_m.group(1).split(":")[-1]
        at_m = re.search(r"\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)", blob)
        ax = float(at_m.group(1)) if at_m else 0.0
        ay = float(at_m.group(2)) if at_m else 0.0
        arot = float(at_m.group(3) or 0.0) if at_m else 0.0
        ref_m = re.search(r'\(property "Reference" "([^"]+)"', blob)
        val_m = re.search(r'\(property "Value" "([^"]+)"', blob)
        crd: list[tuple[float, float]] = []
        gidx = 0
        while True:
            j = blob.find("(fp_", gidx)
            if j < 0:
                break
            kind_m = re.match(r"\(fp_(line|rect|circle|poly|arc)\b", blob[j:])
            if kind_m is None:
                gidx = j + 4
                continue
            g, gidx = _sexp_extract(blob, j)
            if "F.CrtYd" not in g and "B.CrtYd" not in g:
                continue
            kind = kind_m.group(1)
            if kind in ("line", "rect"):
                st = re.search(r"\(start ([-\d.]+) ([-\d.]+)\)", g)
                en = re.search(r"\(end ([-\d.]+) ([-\d.]+)\)", g)
                if st and en:
                    crd += [
                        (float(st.group(1)), float(st.group(2))),
                        (float(en.group(1)), float(en.group(2))),
                    ]
            elif kind == "circle":
                c = re.search(r"\(center ([-\d.]+) ([-\d.]+)\)", g)
                e = re.search(r"\(end ([-\d.]+) ([-\d.]+)\)", g)
                if c and e:
                    cx, cy = float(c.group(1)), float(c.group(2))
                    rad = math.hypot(float(e.group(1)) - cx, float(e.group(2)) - cy)
                    crd += [(cx - rad, cy - rad), (cx + rad, cy + rad)]
            elif kind == "poly":
                crd += [(float(a), float(b)) for a, b in re.findall(r"\(xy ([-\d.]+) ([-\d.]+)\)", g)]
        pad_pts: list[tuple[float, float]] = []
        pidx = 0
        while True:
            j = blob.find("(pad ", pidx)
            if j < 0:
                break
            pblob, pidx = _sexp_extract(blob, j)
            pat = re.search(r"\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)", pblob)
            psz = re.search(r"\(size ([-\d.]+) ([-\d.]+)\)", pblob)
            if pat is None or psz is None:
                continue
            px, py = float(pat.group(1)), float(pat.group(2))
            prot = math.radians(float(pat.group(3) or 0.0))
            hw, hh = float(psz.group(1)) / 2.0, float(psz.group(2)) / 2.0
            for cx, cy in ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)):
                rx = cx * math.cos(prot) - cy * math.sin(prot)
                ry = cx * math.sin(prot) + cy * math.cos(prot)
                pad_pts.append((px + rx, py + ry))
        cr_w, cr_h = _fp_bbox(crd)
        pad_w, pad_h = _fp_bbox(pad_pts)
        out.append(
            KicadFootprint(
                ref_m.group(1) if ref_m else "?",
                fpname,
                val_m.group(1) if val_m else "",
                (ax, ay, arot),
                cr_w,
                cr_h,
                pad_w,
                pad_h,
            )
        )
    return out


def parse_kicad_keepouts(text: str) -> dict[str, tuple[float, float, float, float]]:
    """Named zone / keep-out bboxes from the WP12b PCB (board XY = packing u,s)."""
    out: dict[str, tuple[float, float, float, float]] = {}
    idx = 0
    while True:
        i = text.find("(zone", idx)
        if i < 0:
            break
        if text[i : i + 5] != "(zone" or (len(text) > i + 5 and text[i + 5] not in " \n\t"):
            idx = i + 5
            continue
        blob, idx = _sexp_extract(text, i)
        if "(keepout" not in blob:
            continue
        name_m = re.search(r'\(name "([^"]+)"\)', blob)
        pts = [(float(a), float(b)) for a, b in re.findall(r"\(xy ([-\d.]+) ([-\d.]+)\)", blob)]
        if not pts:
            continue
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        name = name_m.group(1) if name_m else f"unnamed_keepout_{len(out) + 1}"
        if name.startswith("unnamed_keepout_") and min(xs) > 14.0 and max(xs) < 16.0 and min(ys) > 4.0 and max(ys) < 7.0:
            name = "J4_USB_C_keepout"
        out[name] = (min(xs), min(ys), max(xs), max(ys))
    return out


_KICAD_TABLE: dict[str, dict[str, Any]] | None = None
_LAYOUT_501012: LayoutV2 | None = None
_LAYOUT_501015: LayoutV2 | None = None


def kicad_part_table(fps: list[KicadFootprint] | None = None) -> dict[str, dict[str, Any]]:
    """Per-reference courtyard / pad sizes plus the round-5 packing column."""
    global _KICAD_TABLE
    if fps is None and _KICAD_TABLE is not None:
        return _KICAD_TABLE
    rows = fps if fps is not None else parse_kicad_pcb(load_wp12b_pcb())
    table: dict[str, dict[str, Any]] = {}
    for fp in rows:
        cr = KICAD_COURTYARD.get(fp.footprint, (fp.cr_w, fp.cr_h))
        table[fp.ref] = {
            "ref": fp.ref,
            "footprint": fp.footprint,
            "value": fp.value,
            "cr_w": cr[0],
            "cr_h": cr[1],
            "pad_w": fp.pad_w,
            "pad_h": fp.pad_h,
            "round5": ROUND5_XY.get(fp.ref),
            "wp12b_at": fp.at,
        }
    if fps is None:
        _KICAD_TABLE = table
    return table


def _rot_size(w: float, h: float, rot: float) -> tuple[float, float]:
    quarter = abs(rot) % 180.0
    if abs(quarter - 90.0) < 1.0:
        return (h, w)
    return (w, h)


def _part_box(part: LayoutPart, y0: float, y1: float) -> Box:
    return Box(part.ref, part.u, part.s, part.wu, part.ws, y0, y1, part.face)


def _gap(a: Box, b: Box) -> float:
    du = max(0.0, max(a.u0 - b.u1, b.u0 - a.u1))
    ds = max(0.0, max(a.s0 - b.s1, b.s0 - a.s1))
    if du == 0.0 and ds == 0.0:
        # overlap: negative inset
        return -min(a.u1 - b.u0, b.u1 - a.u0, a.s1 - b.s0, b.s1 - a.s0)
    if du == 0.0:
        return ds
    if ds == 0.0:
        return du
    return math.hypot(du, ds)


def _make_part(ref: str, table: dict[str, dict[str, Any]], u: float, s: float, rot: float, face: str, notes: str = "") -> LayoutPart:
    row = table[ref]
    wu, ws = _rot_size(row["cr_w"], row["cr_h"], rot)
    return LayoutPart(
        ref,
        row["footprint"],
        u,
        s,
        rot,
        row["cr_w"],
        row["cr_h"],
        row["pad_w"],
        row["pad_h"],
        wu,
        ws,
        face,
        notes,
    )


def _regions_from_geom(geom: dict[str, Any], module: Box, cell: Box) -> dict[str, tuple[float, float, float, float]]:
    bu0, bu1 = geom["board_u"]
    bs0, bs1 = geom["board_s"]
    leftover = (bu0 + 0.15, bu1 - 0.15, bs0 + 0.15, min(module.s0 - 0.55, bs1) - 0.05)
    side = (module.u1 + 0.05, bu1, max(bs0, module.s0), min(bs1, module.s1))
    pu0 = cell.u1 + 0.2
    pu1 = geom["cavity_u"][1] - 0.15
    ps0 = geom["cavity_s"][0] + 0.15
    ps1 = geom["rib_s"][0] - 0.15
    pocket = (pu0, pu1, ps0, ps1)
    hook = (4.5, 15.5, -7.7, 1.5)
    hang = (bu1 + 0.2, bu1 + 14.0, leftover[2], leftover[3])
    sidehang = (geom["cavity_u"][1] - 1.0, geom["cavity_u"][1] + 8.0, pocket[2], pocket[3])
    return {"leftover": leftover, "side": side, "pocket": pocket, "hook": hook, "hang": hang, "sidehang": sidehang}


def search_layout_v2(spec: V2Spec, *, table: dict[str, dict[str, Any]] | None = None) -> LayoutV2:
    """Place every WP12b footprint on the w20 × y8 shell using real courtyards."""
    table = table if table is not None else kicad_part_table()
    geom = body_geom(spec)
    bu0, bu1 = geom["board_u"]
    bs0, bs1 = geom["board_s"]
    module, antenna = _place_module(spec, geom)
    cell = _place_cell(spec, geom, module)
    usb, usb_wall = _place_usb(spec, geom, module)
    y_top = geom["board_top"]
    y_pocket = FLOOR_Y + BOARD_AT_PARTS
    regs = _regions_from_geom(geom, module, cell)
    occupied: list[Box] = [module, cell]
    if antenna is not None:
        au0, as0, au1, as1 = antenna
        occupied.append(
            Box("RF_NO_COPPER", (au0 + au1) / 2.0, (as0 + as1) / 2.0, au1 - au0, as1 - as0, y_top, y_top + 10.0, "top")
        )
    # SIG1 ring keep-out is on the island leftover. SIG2 sits under U1; REF is on the tab.
    occupied.append(Box("RING_SIG1_CLEAR", CONTACT_1[0], CONTACT_1[1], 7.0, 7.0, y_top, y_top + 8.0, "top"))
    parts: list[LayoutPart] = []

    def add(part: LayoutPart, y0: float, h: float) -> None:
        parts.append(part)
        occupied.append(_part_box(part, y0, y0 + h))

    # U1 keeps the packing centre so SIG2 and the antenna keep-out stay.
    u1 = _make_part("U1", table, module.u, module.s, 90.0, "top", "packing centre; courtyard 11.5×16.5 at rot 90")
    add(u1, y_top, MODULE["A"]["h"])
    # J1 USB on the hook-end end face (plan fallback).
    if usb is not None:
        j1 = _make_part("J1", table, usb.u, usb.s, 0.0, "top", f"USB {usb_wall}")
        add(j1, usb.y0, USB[2])
    # P1–P3 stay on the winner contact sites (folded packing XY).
    for ref, site, note in (
        ("P1", CONTACT_1, "SIG1 folded site"),
        ("P2", CONTACT_2, "SIG2 folded site"),
        ("P3", CONTACT_REF, "REF site; REF_end_wall_slot"),
    ):
        add(_make_part(ref, table, site[0], site[1], 0.0, "floor", note), FLOOR_Y, TAB_T)

    def try_place(ref: str, rots: tuple[float, ...], region_names: tuple[str, ...], y0: float, h: float, near=None, notes="") -> bool:
        row = table[ref]
        ranked = []
        for rn in region_names:
            u0, u1, s0, s1 = regs[rn]
            face = {"pocket": "pocket", "hook": "hook", "hang": "top", "sidehang": "pocket"}.get(rn, "top")
            ranked.append(((u0, u1, s0, s1), y0, face))
        sizes = []
        for rot in rots:
            wu, ws = _rot_size(row["cr_w"], row["cr_h"], rot)
            sizes.append((wu, ws, rot))
        for wu, ws, rot in sizes:
            placed = _find_site(ref, [(wu, ws)], h, ranked, occupied, near=near, step=0.5, margin=SOLDER_MASK_TO_COPPER)
            if placed is not None:
                add(
                    LayoutPart(ref, row["footprint"], placed.u, placed.s, rot, row["cr_w"], row["cr_h"], row["pad_w"], row["pad_h"], wu, ws, placed.face, notes),
                    placed.y0,
                    h,
                )
                return True
        return False

    named = [
        ("U2", (0.0, 90.0), ("pocket", "leftover"), y_top, VQFN[2], (14.0, 8.0), "ADS1292"),
        ("SW1", (0.0, 90.0), ("leftover",), y_top, SWITCH[2], (13.5, 24.2), "lid recess"),
        ("J4", (0.0, 90.0), ("leftover", "pocket"), y_top, 2.0, (15.1, 16.8), "TC2030; reachable from the leftover high-u edge"),
        ("J2", (0.0, 90.0), ("sidehang", "pocket", "leftover"), y_top, JST[2], (20.0, 8.0), "JST-SH; hangs off the pocket high-u wall"),
        ("U4", (0.0, 90.0), ("leftover", "pocket"), y_top, LDO[2], (9.45, 20.2), "TLV71330"),
        ("U3", (0.0, 90.0), ("leftover", "pocket"), y_top, BQ[2], (3.45, 16.8), "BQ25100"),
        ("U5", (0.0, 90.0), ("pocket", "leftover"), y_top, SOT23_6[2], (15.0, 4.0), "USBLC6"),
        ("D1", (0.0, 90.0), ("pocket", "leftover"), y_top, SOD523[2], (15.0, 5.5), "PESD VBUS"),
        ("L1", (0.0, 90.0), ("leftover", "pocket"), y_top, 1.0, None, "10 µH"),
        ("D2", (0.0, 90.0), ("leftover", "pocket"), y_top, 0.5, None, "LED"),
        ("J3", (0.0, 90.0), ("hang",), y_top, HEADER[2], (bu1 + 7.0, (regs["leftover"][2] + regs["leftover"][3]) / 2.0), "bench header; pins hang off the high-u outline"),
    ]
    for q in ("Q1", "Q2", "Q3", "Q4", "Q5"):
        named.append((q, (0.0, 90.0), ("leftover", "pocket"), y_top, 1.15, None, "SOT-23"))
    missing: list[str] = []
    for ref, rots, rns, y0, h, near, notes in named:
        if not try_place(ref, rots, rns, y0, h, near, notes):
            missing.append(ref)

    # R1–R3 variant A: island at each tab root, not on the 2.5 mm strip.
    leftover_reg = regs["leftover"]
    tab_roots = {
        "R1": (leftover_reg[0] + 2.0, leftover_reg[2] + 1.5),
        "R2": (leftover_reg[1] - 2.0, leftover_reg[2] + 1.5),
        "R3": (CONTACT_REF[0], leftover_reg[3] - 1.0),
    }
    for ref, near in tab_roots.items():
        if not try_place(ref, (0.0, 90.0), ("leftover", "pocket"), y_top, 0.5, near, "220 kΩ variant A: island at tab root"):
            missing.append(ref)

    # Remaining C/R on leftover then pocket.
    rest = [r for r in table if r not in {p.ref for p in parts} and r[0] in "CR"]
    rest.sort(key=lambda r: (r[0], int(re.sub(r"\D", "", r) or "0")))
    for ref in rest:
        y0 = y_top
        regions = ("leftover", "pocket")
        if ref.startswith("C") and table[ref]["footprint"].startswith("C_0603"):
            h = 1.0
        else:
            h = 0.5
        if not try_place(ref, (0.0, 90.0), regions, y0, h, None, "passive grid"):
            if not try_place(ref, (0.0, 90.0), ("pocket", "hook"), y_pocket, h, None, "passive grid, pocket"):
                missing.append(ref)

    still = list(missing)
    for ref in still:
        if try_place(ref, (0.0, 90.0), ("leftover", "pocket"), y_top, 0.5, None, "last-chance"):
            missing.remove(ref)

    keepouts = [
        ("RF_NO_COPPER", *antenna) if antenna is not None else ("RF_NO_COPPER", 0, 0, 0, 0),
        ("RF_FEED_NOTCH", 6.05, 33.05, 7.25, 34.65),
        ("RING_SIG1_CLEAR", CONTACT_1[0] - 3.5, CONTACT_1[1] - 3.5, CONTACT_1[0] + 3.5, CONTACT_1[1] + 3.5),
        ("RING_SIG2_CLEAR", CONTACT_2[0] - 3.5, CONTACT_2[1] - 3.5, CONTACT_2[0] + 3.5, CONTACT_2[1] + 3.5),
        ("RING_REF_CLEAR", CONTACT_REF[0] - 3.5, CONTACT_REF[1] - 3.5, CONTACT_REF[0] + 3.5, CONTACT_REF[1] + 3.5),
        ("J4_keepout", 14.46, 4.13, 15.73, 6.67),
    ]
    if antenna is None:
        keepouts[0] = ("RF_NO_COPPER", 0.0, 0.0, 0.0, 0.0)
    else:
        keepouts[0] = ("RF_NO_COPPER", antenna[0], antenna[1], antenna[2], antenna[3])

    rules = _layout_rules(spec, geom, parts, module, cell, usb_wall, missing, occupied, antenna)
    blocking = next((f"{n}: {why}" for n, ok, why in rules if not ok), "")
    variants = [
        (
            f"Contact 1.0 mm (WP12b netclass Contact) cannot hold on a {TAB_WIDTH_II:g} mm tab "
            f"with an 0402 across it (pad gap {R0402_PAD_GAP:.2f} mm). "
            "Variant A: R1/R2/R3 on the island at the tab root; each tab carries one Contact trace."
        ),
        (
            f"Variant B: widen each tab to {WIDER_TAB_MM:.1f} mm so an 0402 can sit on the tab "
            f"with {CONTACT_NETCLASS_CLEARANCE:.1f} mm to other copper. The 0402 pad gap "
            f"{R0402_PAD_GAP:.2f} mm still violates Contact-to-Default {CONTACT_NETCLASS_CLEARANCE:.1f} mm; "
            "that needs a larger package or a DRC exception."
        ),
    ]
    return LayoutV2(
        name=f"layout_v2_{spec.tag}",
        spec=spec,
        parts=parts,
        keepouts=keepouts,
        rules=rules,
        variants=variants,
        first_blocking=blocking,
        contacts_moved_mm={"SIG1": 0.0, "SIG2": 0.0, "REF": 0.0},
    )


def _layout_rules(
    spec: V2Spec,
    geom: dict[str, Any],
    parts: list[LayoutPart],
    module: Box,
    cell: Box,
    usb_wall: str | None,
    missing: list[str],
    occupied: list[Box],
    antenna: tuple[float, float, float, float] | None,
) -> list[tuple[str, bool, str]]:
    bu0, bu1 = geom["board_u"]
    bs0, bs1 = geom["board_s"]
    by_ref = {p.ref: p for p in parts}
    rules: list[tuple[str, bool, str]] = []

    # JLC 2.5 mm body-to-edge for U1 on this island.
    u1_body_w, u1_body_l = 10.5, 15.5
    island_w = bu1 - bu0
    island_l = bs1 - bs0
    need_w = u1_body_w + 2 * JLC_ASSEMBLY_EDGE
    need_l = u1_body_l + 2 * JLC_ASSEMBLY_EDGE
    jlc_u1 = island_w + 1e-9 >= need_w and island_l + 1e-9 >= need_l
    # Packing pose is long-along-u (15.5 in 15.5): body-to-edge 0.
    packing_edge = (island_w - 15.5) / 2.0
    rules.append(
        (
            "JLC FPC assembly edge 2.5 mm (board-v2.md §12 / L6)",
            False,
            (
                f"U1 body 10.5×15.5 at the packing pose (long along u) sits {packing_edge:.2f} mm "
                f"from the island edge u {bu0:.2f}–{bu1:.2f} (width {island_w:.2f}). "
                f"JLC wants {JLC_ASSEMBLY_EDGE:.1f} mm. Turning U1 long-along-s needs island "
                f"{need_w:.1f}×{need_l:.1f}; this island is {island_w:.2f}×{island_l:.2f}, so U1 "
                "can meet 2.5 mm on the short sides only if nothing else shares that 10.5 mm strip. "
                "U2 courtyard 5.26 cannot sit beside U1 under that rule. First rule that cannot be met."
            ),
        )
    )
    # copper-to-edge 0.30 using pad extent
    copper_fail = []
    for p in parts:
        if p.face not in {"top", "pocket"}:
            continue
        if p.ref in {"J1", "J2", "J3", "P1", "P2", "P3"} or p.face == "hook":
            continue  # connector / ring may hang off or sit on a tab
        if p.u - p.wu / 2.0 > bu1 - 0.05:
            continue  # hanging off the high-u outline
        pw, ph = _rot_size(p.pad_w, p.pad_h, p.rot)
        u0, u1 = p.u - pw / 2.0, p.u + pw / 2.0
        s0, s1 = p.s - ph / 2.0, p.s + ph / 2.0
        if p.face == "top":
            edge = min(u0 - bu0, bu1 - u1, s0 - bs0, bs1 - s1)
            if edge < COPPER_TO_EDGE - 1e-9:
                copper_fail.append(f"{p.ref} pad-edge {edge:.3f} < {COPPER_TO_EDGE:.2f}")
    rules.append(
        (
            "copper-to-edge 0.30 (board-v2.md §12)",
            not copper_fail,
            "; ".join(copper_fail) if copper_fail else f"on-island pads ≥ {COPPER_TO_EDGE:.2f} mm from the island outline",
        )
    )
    # courtyard overlaps
    boxes = [b for b in occupied if b.name in by_ref]
    overlaps = []
    for i, a in enumerate(boxes):
        for b in boxes[i + 1 :]:
            if _overlap(a, b, 0.0):
                overlaps.append(f"{a.name}/{b.name}")
    rules.append(
        (
            "courtyard-to-courtyard ≥ 0 with solder-mask bridge margin 0.10",
            not overlaps,
            "; ".join(overlaps[:12]) if overlaps else "no courtyard overlap among placed parts",
        )
    )
    rules.append(
        (
            f"Contact netclass {CONTACT_NETCLASS_CLEARANCE:.1f} mm (WP12b elicio-v2.kicad_pro)",
            False,
            (
                f"R1/R2/R3 0402 pad gap {R0402_PAD_GAP:.2f} mm < {CONTACT_NETCLASS_CLEARANCE:.1f} mm "
                f"(SIG1–AFE_IN1P, SIG2–AFE_IN1N, REF–RLD_FB). A 2.5 mm tab cannot hold the 0402 "
                "and that clearance. See variants A and B."
            ),
        )
    )
    ko_hits = []
    if antenna is not None:
        ko = Box("RF_NO_COPPER", (antenna[0] + antenna[2]) / 2.0, (antenna[1] + antenna[3]) / 2.0,
                 antenna[2] - antenna[0], antenna[3] - antenna[1], -1.0, 20.0, "top")
        for p in parts:
            if p.ref == "U1":
                continue
            if _overlap(_part_box(p, 0.0, 1.0), ko, 0.0):
                ko_hits.append(p.ref)
    rules.append(
        (
            "module keep-out empty (RF_NO_COPPER / U1 antenna)",
            not ko_hits,
            f"inside RF_NO_COPPER: {', '.join(ko_hits)}" if ko_hits else "no non-U1 footprint in RF_NO_COPPER",
        )
    )
    j4 = by_ref.get("J4")
    rules.append(
        (
            "J4 on the hook-end end face with its plug volume",
            bool(j4 is not None and j4.face == "hook"),
            (
                f"J1 USB wall {usb_wall} (USB courtyard 10.64×9.42 fills that face). "
                f"J4 at ({j4.u:.2f}, {j4.s:.2f}) rot {j4.rot:g} face {j4.face}"
                if j4
                else "J4 not placed"
            ),
        )
    )
    sw1 = by_ref.get("SW1")
    sw1_ok = sw1 is not None and sw1.face == "top" and sw1.s >= bs0
    rules.append(
        (
            "SW1 under the lid recess",
            bool(sw1_ok),
            f"SW1 at ({sw1.u:.2f}, {sw1.s:.2f}) on the board top" if sw1 else "SW1 not placed",
        )
    )
    j3 = by_ref.get("J3")
    rules.append(
        (
            "J3 and TC2030 reachable",
            j3 is not None and j4 is not None,
            (
                f"J3 ({j3.u:.2f}, {j3.s:.2f}) rot {j3.rot:g}; "
                f"J4 ({j4.u:.2f}, {j4.s:.2f}) rot {j4.rot:g}"
                if j3 and j4
                else f"missing {', '.join(r for r in ('J3', 'J4') if r not in by_ref)}"
            ),
        )
    )
    rules.append(
        (
            "every WP12b footprint placed",
            not missing,
            f"unplaced: {', '.join(missing)}" if missing else f"{len(parts)} footprints placed",
        )
    )
    if spec.arc_plus >= 1.5:
        need_m1 = geom["total_chord"] + 3.0
        rules.insert(
            0,
            (
                "M1 ≥ TOTAL_CHORD + 3 (Q34); 17 mm pack at +1.5 only if M1 ≥ 52.5",
                M1_DEFAULT + 1e-9 >= 52.5 and M1_DEFAULT + 1e-9 >= need_m1,
                f"TOTAL_CHORD {geom['total_chord']:.2f}, need M1 ≥ {need_m1:.2f}; default.toml M1={M1_DEFAULT:g}",
            ),
        )
    return rules


def layout_v2_501012() -> LayoutV2:
    global _LAYOUT_501012
    if _LAYOUT_501012 is None:
        spec = V2Spec("A", "pack501012", "series", 20.0, 8.0, 0.0, "II", 3.0, 0.0)
        _LAYOUT_501012 = search_layout_v2(spec)
    return _LAYOUT_501012


def layout_v2_501015_arc() -> LayoutV2:
    global _LAYOUT_501015
    if _LAYOUT_501015 is None:
        spec = V2Spec("A", "pack501015", "series", 20.0, 8.0, 1.5, "II", 3.0, 0.0)
        _LAYOUT_501015 = search_layout_v2(spec)
    return _LAYOUT_501015


def _layout_v2_section() -> list[str]:
    table = kicad_part_table()
    lay12 = layout_v2_501012()
    lay15 = layout_v2_501015_arc()
    lines: list[str] = []
    lines.append("## 5b. Layout for the board lane, v2 (WP11c)")
    lines.append("")
    lines.append(
        "Real F.CrtYd and pad extents from `git show 845bac7:hardware/board/elicio-v2.kicad_pcb` "
        "(WP12b after dropping the shorting copper). Round-5 packing envelopes stay in the 864-run "
        "table. Courtyard-to-courtyard uses a 0.05 mm solder-mask-to-copper margin "
        f"(DRC; two expansions = {SOLDER_MASK_BRIDGE_MARGIN:.2f} mm pad-to-pad). "
        f"Contact netclass clearance is {CONTACT_NETCLASS_CLEARANCE:.1f} mm "
        "(WP12b `elicio-v2.kicad_pro`, nets SIG1/SIG2/REF)."
    )
    lines.append("")
    lines.append("### Part table — KiCad courtyard vs round 5")
    lines.append("")
    lines.append(
        "| ref | footprint | courtyard w × h | pad extent w × h | round-5 packing | Δw | Δh |"
    )
    lines.append("|---|---|---:|---:|---:|---:|---:|")
    def refkey(r: str) -> tuple:
        m = re.match(r"([A-Za-z]+)(\d+)", r)
        return (m.group(1), int(m.group(2))) if m else (r, 0)
    for ref in sorted(table, key=refkey):
        row = table[ref]
        r5 = row["round5"]
        if r5 is None:
            r5s, dw, dh = "—", "—", "—"
        else:
            r5s = f"{r5[0]:.2f} × {r5[1]:.2f}"
            dw = f"{row['cr_w'] - r5[0]:+.2f}"
            dh = f"{row['cr_h'] - r5[1]:+.2f}"
        lines.append(
            f"| {ref} | {row['footprint']} | {row['cr_w']:.3f} × {row['cr_h']:.3f} | "
            f"{row['pad_w']:.3f} × {row['pad_h']:.3f} | {r5s} | {dw} | {dh} |"
        )
    lines.append("")
    lines.append("Keep-outs on that board (zone bbox from the same KiCad file):")
    lines.append("")
    lines.append("| name | x0 | y0 | x1 | y1 |")
    lines.append("|---|---:|---:|---:|---:|")
    for name, (x0, y0, x1, y1) in sorted(parse_kicad_keepouts(load_wp12b_pcb()).items()):
        lines.append(f"| {name} | {x0:.2f} | {y0:.2f} | {x1:.2f} | {y1:.2f} |")
    lines.append("")
    lines.append("### Rules the search must meet")
    lines.append("")
    lines.append("| rule | source |")
    lines.append("|---|---|")
    lines.append(f"| JLC FPC assembly, body to board edge ≥ {JLC_ASSEMBLY_EDGE:.1f} mm | board-v2.md §12 / L6 |")
    lines.append(f"| copper to outline ≥ {COPPER_TO_EDGE:.2f} mm | board-v2.md §12; DRC min_copper_edge_clearance |")
    lines.append(
        f"| courtyard-to-courtyard ≥ 0, with solder-mask bridge margin "
        f"{SOLDER_MASK_BRIDGE_MARGIN:.2f} mm | WP11c brief; DRC solder_mask_to_copper_clearance "
        f"{SOLDER_MASK_TO_COPPER:.2f} mm |"
    )
    lines.append(
        f"| Contact netclass clearance {CONTACT_NETCLASS_CLEARANCE:.1f} mm | WP12b elicio-v2.kicad_pro |"
    )
    lines.append("| module keep-out empty of everything | Raytac Spec K; RF_NO_COPPER |")
    lines.append("| J4 on the hook-end end face with its plug volume | packing-v2.md §5; plan v2 §5.4 |")
    lines.append("| SW1 under the lid recess | packing-v2.md §5 |")
    lines.append("| J3 and TC2030 reachable | WP11c brief |")
    lines.append("")
    for label, lay in (
        ("501012 pack, w20 × y8, BODY_ARC, interface II, standoff 3 (the shell as built)", lay12),
        ("501015 pack 17.0×10.0×5.0 at +1.5 mm of arc (valid only if M1 ≥ 52.5)", lay15),
    ):
        lines.append(f"### {label}")
        lines.append("")
        lines.append(
            f"Spec `{lay.spec.tag}`. TOTAL_CHORD {body_geom(lay.spec)['total_chord']:.2f}. "
            f"Board u {body_geom(lay.spec)['board_u'][0]:.2f}–{body_geom(lay.spec)['board_u'][1]:.2f}, "
            f"s {body_geom(lay.spec)['board_s'][0]:.2f}–{body_geom(lay.spec)['board_s'][1]:.2f}."
        )
        lines.append("")
        if lay.first_blocking:
            lines.append(f"**First rule that cannot be met:** {lay.first_blocking}")
        else:
            lines.append("Every listed rule is met.")
        lines.append("")
        lines.append("| rule | met | detail |")
        lines.append("|---|---|---|")
        for name, ok, why in lay.rules:
            lines.append(f"| {name} | {'yes' if ok else 'no'} | {why} |")
        lines.append("")
        for v in lay.variants:
            lines.append(f"- {v}")
        lines.append("")
        lines.append(
            "Contact sites are unchanged: SIG1 (5.90, 22.00), SIG2 (10.40, 33.10), "
            "REF (8.50, 43.00). REF tab (8.50, 43.00) → (8.50, 36.80); `REF_end_wall_slot` is cut."
        )
        lines.append("")
        lines.append(
            "| ref | u | s | rot | courtyard wu × ws | face | notes |"
        )
        lines.append("|---|---:|---:|---:|---:|---|---|")
        for p in sorted(lay.parts, key=lambda x: refkey(x.ref)):
            lines.append(
                f"| {p.ref} | {p.u:.2f} | {p.s:.2f} | {p.rot:g} | "
                f"{p.wu:.2f} × {p.ws:.2f} | {p.face} | {p.notes} |"
            )
        lines.append("")
        lines.append(
            "Tab exits (unchanged): SIG1 (5.90, 22.00) → (5.90, 29.00); "
            "SIG2 (10.40, 33.10) → (10.40, 26.10); REF (8.50, 43.00) → (8.50, 36.80). "
            "Island outline u 2.25–17.75, s as in the spec row. "
            "WP12d places from this table and tests within 0.1 mm."
        )
        lines.append("")
    lines.append(
        "Drawings: this layout does not add `placement_v2_*.svg` under `docs/fab/cad/v1/`. "
        "The round-5 14-file kept set is pinned, and the layout does not fully close every rule (Q56)."
    )
    lines.append("")
    return lines


def packing_markdown(rows: list[V2Result]) -> str:
    """WP11 packing-v2.md body. Plan is not changed."""
    closed = [r for r in rows if r.closes]
    per = smallest_per_arch(rows)
    lines: list[str] = []
    lines.append("# Packing v2 — which architectures close")
    lines.append("")
    lines.append("WP11 analysis. The plan is not changed. Nothing is ordered.")
    lines.append("Architecture C is out (plan v2 turn 02). Interface I is turn 07/09:")
    lines.append("no springs, no pins; board underside on three brass standoff tops;")
    lines.append("8 × 8 gold pad per site; bosses 0.5 lower than the standoff tops;")
    lines.append("cell under the board only with positive nominal clearance and no load")
    lines.append("after the board bends onto the bosses. Standoffs 3.0, 3.5 and 4.0.")
    lines.append("A 0.5-deep floor recess (web 1.0 remaining) is run at 3.5 and 4.0.")
    lines.append("Interface II is the flex-tab fallback.")
    lines.append("Arc-plus for the DTP301120 under interface II is §1b (WP11b, Q55).")
    lines.append("The Jauch LP501218JH under interface II is §1c (WP11b, L7-research-v4.md §2).")
    lines.append("A bigger lid and width for the two buyable cells is §1d (WP11b note 2).")
    lines.append("The 501015 pack (17.0 mm with PCM) and 501012 pack are §1e (WP11b note 3, L7 §7).")
    lines.append("The REF tab route search is in §5 (WP11b, Q59).")
    lines.append("The board-lane layout with real courtyards is §5b (WP11c).")
    lines.append("")
    lines.append("## 1. Every run at BODY_ARC 48.4")
    lines.append("")
    lines.append(
        "| arch | iface | standoff | recess | cell | layout | width | lid | closes | first conflict | "
        "nom clr | def clr | stack | outer0 | outer@lid | free mm² | TOTAL_CHORD | M1 gate |"
    )
    lines.append(
        "|---|---|---:|---:|---|---|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|"
    )
    for r in rows:
        spec = r.spec
        first = "—" if r.closes else _md_cell(r.first_conflict)
        lines.append(
            f"| {spec.arch} | {spec.iface} | {spec.standoff:g} | {spec.recess:g} | {spec.cell} | "
            f"{spec.layout} | {spec.width:g} | {spec.lid_y:g} | {'yes' if r.closes else 'no'} | {first} | "
            f"{r.nominal_clearance:+.1f} | {r.deformed_clearance:+.1f} | {r.stack_over_module:.1f} | "
            f"{r.outer_zero:.1f} | {r.outer_at_lid:.1f} | {r.free_mm2:.1f} | {r.total_chord:.2f} | {r.m1_gate:.2f} |"
        )
    lines.append("")
    n_i = sum(1 for r in rows if r.spec.iface == "I")
    n_ii = sum(1 for r in rows if r.spec.iface == "II")
    closed_i = [r for r in closed if r.spec.iface == "I"]
    closed_ii = [r for r in closed if r.spec.iface == "II"]
    winner = stage_b_winner_spec()
    winner_row = next((r for r in rows if r.spec == winner), None)
    winner_chord = winner_row.total_chord if winner_row is not None else 47.9005
    lines.extend(_dtp_arc_plus_section(winner_chord))
    lines.extend(_jauch_section(winner_chord))
    lines.extend(_buyable_ext_section(winner_chord, winner_row))
    lines.extend(_pack_cells_section(winner_chord, winner_row))
    lines.extend(_buyable_cell_compare_section(rows, winner_chord))
    lines.append("## 2. Clearance, stack, and first-conflict families")
    lines.append("")
    packs = "; ".join(
        f"{CELL[c]['name']} {CELL[c]['t']:g} + {FOAM:g} = {CELL[c]['t'] + FOAM:g}" for c in CELLS
    )
    j = CELL["jauch"]
    p15 = CELL["pack501015"]
    p12 = CELL["pack501012"]
    packs = (
        f"{packs}; {j['name']} {j['t']:g} + {FOAM:g} = {j['t'] + FOAM:g} "
        "(WP11b Jauch series, not in the 864-run matrix); "
        f"{p15['name']} {p15['t']:g} + {FOAM:g} = {p15['t'] + FOAM:g}; "
        f"{p12['name']} {p12['t']:g} + {FOAM:g} = {p12['t'] + FOAM:g} "
        "(WP11b note 3, L7 §7, not in the 864-run matrix)"
    )
    lines.append(f"Cell packed height = body + foam {FOAM:g}: {packs}.")
    lines.append(
        f"Foam {FOAM:g} is plan v1 §5's number and the one the order-1 Stage B `CELL_envelope` "
        "measures on the solid. Plan v2 §3 says 0.3; this file and Stage B use one number "
        "(review r5, decision 57)."
    )
    lines.append("Nominal clearance = standoff − (packed − recess). The board underside is at the standoff top (rigid).")
    lines.append(
        f"Deformed clearance = (standoff − {BOSS_DROP:g}) − (packed − recess). The board bends down onto the bosses."
    )
    lines.append(
        "The cell may lie under the board only with positive nominal clearance and must carry no load "
        "(positive deformed clearance). C15 for a 0.5 recess (web 1.0) is NOT_MEASURED."
    )
    lines.append("")
    lines.append("| cell | standoff | recess | nom | def | under-board? | load? |")
    lines.append("|---|---:|---:|---:|---:|---|---|")
    unloaded: list[str] = []
    for cell_name in CELLS:
        for st in STANDOFFS:
            for rec in RECESSES:
                dummy = V2Spec("A", cell_name, "series", 20.0, 8.0, 0.0, "I", st, rec)
                clr = cell_clearance(dummy)
                under = "yes" if clr["nominal"] > 1e-9 else "no"
                load = "no load" if clr["deformed"] > 1e-9 else "carries load"
                if clr["deformed"] > 1e-9:
                    unloaded.append(f"{CELL[cell_name]['name']} standoff {st:g} recess {rec:g}")
                lines.append(
                    f"| {cell_name} | {st:g} | {rec:g} | {clr['nominal']:+.1f} | {clr['deformed']:+.1f} | {under} | {load} |"
                )
    lines.append("")
    lines.append(
        "Positive deformed clearance: " + ("; ".join(unloaded) if unloaded else "none") + "."
    )
    lines.append("")
    lines.append(
        f"Module stack above the inner floor. Interface I: standoff + rigid board {BOARD_RIGID:g} + module. "
        f"Interface II: ring {TAB_T:g} (PI {FLEX:g} + FR4 {STIFFENER_TAB:g}) + standoff + board "
        f"{BOARD_AT_PARTS:g} (PI {FLEX:g} + FR4 {STIFFENER:g}) + module. "
        f"Outer at zero added clearance = {FLOOR_Y:g} floor + stack + {LID_THICK:g} lid."
    )
    lines.append("")
    lines.append("| arch | iface | standoff | stack | outer0 | ≤ 9.0? |")
    lines.append("|---|---|---:|---:|---:|---|")
    for arch in ARCHES_RUN:
        for iface in IFACES:
            for st in STANDOFFS:
                dummy = V2Spec(arch, "501015", "series", 20.0, 8.0, 0.0, iface, st, 0.0)
                stk = module_stack(dummy)
                ok = "yes" if stk["outer_zero"] <= 9.0 + 1e-9 else "no"
                lines.append(
                    f"| {arch} | {iface} | {st:g} | {stk['stack']:.2f} | {stk['outer_zero']:.2f} | {ok} |"
                )
    lines.append("")
    lines.append(
        "outer@lid in the run table is LID_Y + 1.0 (the candidate body at that lid). For the Stage B "
        "winner the module-to-lid gap is also probed on the solid (`V2_STACK`, §6)."
    )
    lines.append("")
    lines.append(f"Interface I ({n_i} runs): {len(closed_i)} close.")
    for pname in ("pad_SIG1", "pad_SIG2", "pad_REF"):
        hits = [c for r in rows if r.spec.iface == "I" for c in r.conflicts if c.startswith(pname + " ")]
        if hits:
            lines.append(f"Also in {len(hits)} of {n_i}: {_md_cell(hits[0])} (review r5 check).")
    lines.append(
        f"Interface II ({n_ii} runs): {len(closed_ii)} close"
        + (": " + ", ".join(f"`{r.spec.tag}`" for r in closed_ii) if closed_ii else "")
        + "."
    )
    lines.append("")
    lines.append("First-conflict families (numbers masked), failing runs:")
    lines.append("")
    lines.append("| family | runs |")
    lines.append("|---|---:|")
    fam_counts: dict[str, int] = {}
    for r in rows:
        if not r.closes:
            key = conflict_family(r.first_conflict)
            fam_counts[key] = fam_counts.get(key, 0) + 1
    for fam, n in sorted(fam_counts.items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"| {_md_cell(fam)} | {n} |")
    lines.append("")
    adj = V2Spec("A", "501015", "series", 20.0, 8.0).adjustment_region
    lines.append(
        f"Adjustment region per site (Interface I, formula only): {PAD_HALF:g} − {STANDOFF_CIRCUMR:g} − "
        f"{PLACEMENT_TOL:g} = ±{adj:.1f} mm. NOT_MEASURED on the solid."
    )
    lines.append("")
    lines.append("## 3. Plan v2 §4 rule, line by line")
    lines.append("")
    lines.append("Rule (1) closes ≤ 9.0 high and 20 wide, checks on the built solid, TOTAL_CHORD ≤ M1−3.")
    lines.append("")
    if closed:
        first = closed[0]
        lines.append(
            f"{len(closed)} layouts close in packing: "
            + ", ".join(f"`{r.spec.tag}`" for r in closed)
            + f". TOTAL_CHORD {first.total_chord:.2f} ≤ {M1_DEFAULT - 3.0:.2f} "
            f"(M1 = {M1_DEFAULT:g} from default.toml; Q34 blank). USB-C: {first.usb_wall}; "
            "the medial opening is not cut on the order-1 solid."
        )
        failing = [n for n, (status, _nums, _text) in STAGE_B_V2_MEASURED.items() if status == "fail"]
        if failing:
            lines.append(
                f"On the built solid (§6) `{winner.tag}` still fails {', '.join(f'`{n}`' for n in failing)}, "
                "so rule (1) is not met on the solid yet."
            )
    else:
        lines.append("No layout closes.")
    for arch in ARCHES:
        if not any(r.spec.arch == arch for r in closed):
            lines.append(f"Architecture {arch} does not close" + (" (out, plan v2 turn 02)." if arch == "C" else "."))
    if not closed_i:
        lines.append("Interface I does not close.")
    lines.append("")
    if per.get("A") is not None:
        mod = MODULE[per["A"].spec.arch]["name"]
        cell = CELL[per["A"].spec.cell]["name"]
        lines.append(
            f"Rule (2) parts orderable. The closer uses {mod}, cell {cell}, ADS1292, BQ25100, TLV71330 "
            "(SOT-23-5), USBLC6-2SC6 and PESD5V0L1UL at the USB, JST-SH, USB-C 16-pin, a "
            f"{SWITCH[0]:g} × {SWITCH[1]:g} × {SWITCH[2]:g} recovery switch, a {HEADER[0]:g} × {HEADER[1]:g} × "
            f"{HEADER[2]:g} bench header, brass M2.5 hex standoffs {STANDOFF_AF:g} AF, ISO 7380 M2.5×4 screws "
            "and a flex board with FR4 stiffeners. No BAV199 (board-v2.md: 220 kΩ series and the ADS1292's "
            "own input diodes). Page prices are NOT_MEASURED (no vendor contact)."
        )
    lines.append("")
    lines.append(
        "Rule (3) fewest Rolf steps. Interface I would skip tabs (board on standoff tops). "
        + ("It does not close, so the only closers are Interface II (rings under the standoffs)."
           if not closed_i else "It closes.")
        + " No decision."
    )
    lines.append("")
    lines.append("Rule (4) lowest page price. NOT_MEASURED.")
    lines.append("")
    lines.append("Ties go to A." + (" The only architecture that closes is A." if closed and all(r.spec.arch == "A" for r in closed) else ""))
    lines.append("")
    lines.append("## 4. Smallest body per architecture")
    lines.append("")
    for arch in ARCHES:
        hit = per.get(arch)
        if hit is None:
            lines.append(f"- **{arch}**: does not close.")
        else:
            spec = hit.spec
            lines.append(
                f"- **{arch}**: packing-smallest `{spec.tag}`. BODY_WIDTH {spec.width:g}, LID_Y {spec.lid_y:g}, "
                f"BODY_THICK {spec.lid_y + LID_THICK:g}, TOTAL_CHORD {hit.total_chord:.2f}, "
                f"USB wall: {hit.usb_wall}."
            )
            if spec == winner:
                lines.append("  It is the Stage B winner (`scripts/cad/params/stageb_v2.toml`).")
            else:
                lines.append(f"  The Stage B winner is `{winner.tag}`.")
    lines.append("")
    lines.append("## 5. Layout for the board lane (architectures that close)")
    lines.append("")
    a = per.get("A")
    if a is None:
        lines.append("No architecture closes. There is no board-lane layout.")
    else:
        spec = a.spec
        p = a.parts

        def box_line(label: str, key: str) -> str:
            b = p[key]
            return (
                f"{label} {b.wu:g} × {b.ws:g} × {b.y1 - b.y0:.2f}, centre ({b.u:.2f}, {b.s:.2f}), "
                f"y {b.y0:.2f}–{b.y1:.2f} ({b.face})"
            )

        lines.append(
            f"Hand `{spec.tag}` to the board lane. Interface {spec.iface}. Board {a.board_thick:.2f} at parts "
            f"(PI {FLEX:g} + FR4 {STIFFENER:g}), {TAB_T:g} at the rings (PI {FLEX:g} + FR4 {STIFFENER_TAB:g})."
        )
        lines.append(
            f"Board zone u {a.board_u[0]:.2f}–{a.board_u[1]:.2f}, s {a.board_s[0]:.2f}–{a.board_s[1]:.2f}. "
            f"Underside y {a.board_underside:.2f} (the standoff tops), top y {a.board_top:.2f}."
        )
        lines.append("")
        lines.append("- " + box_line(f"Cell {CELL[spec.cell]['name']} + foam {FOAM:g}", "cell") + ".")
        mod = MODULE[spec.arch]
        m = p["module"]
        axis = "u" if m.wu >= m.ws else "s"
        lines.append("- " + box_line(f"Module {mod['name']}", "module") + f", length along {axis}.")
        if a.antenna is not None:
            au0, as0, au1, as1 = a.antenna
            lines.append(
                f"- Antenna keep-out (no copper, every layer) u {au0:.2f}–{au1:.2f}, s {as0:.2f}–{as1:.2f} "
                f"({au1 - au0:.1f} × {as1 - as0:.1f}; {mod['ant_from']})."
            )
        for label, key in (
            ("ADS1292 VQFN-32", "ADS1292_RSM"),
            ("BQ25100", "BQ25100"),
            ("TLV71330 SOT-23-5", "TLV713"),
            ("USBLC6-2SC6 SOT-23-6", "USBLC6"),
            ("PESD5V0L1UL", "PESD_VBUS"),
            ("JST-SH", "JST_SH"),
            ("Recovery switch", "switch"),
            ("Bench header", "header"),
        ):
            if key in p:
                lines.append("- " + box_line(label, key) + ".")
        swd = [p[k] for k in sorted(p) if k.startswith("SWD")]
        if swd:
            lines.append(
                "- SWD test pads 1.0 × 1.0: " + ", ".join(f"({b.u:.2f}, {b.s:.2f})" for b in swd) + "."
            )
        if "usb" in p:
            lines.append(
                "- " + box_line("USB-C", "usb") + f". It would cut the **{a.usb_wall}**. Recess "
                f"{USB_RECESS:g}, ligaments {USB_LIGAMENT:g}, plug volume "
                f"{PLUG_VOLUME[0]:g} × {PLUG_VOLUME[1]:g} × {PLUG_VOLUME[2]:g}. No decision."
            )
        n_top = sum(1 for k, b in p.items() if k.startswith("R0402") and b.face == "top")
        n_floor = sum(1 for k, b in p.items() if k.startswith("R0402") and b.face != "top")
        lines.append(f"- {a.n_0402} of {N_0402} 0402 courtyards placed ({n_top} on the board, {n_floor} in the pocket).")
        lines.append("")
        lines.append(f"Flex tabs (ring Ø{RING_D:g}, hole Ø{RING_HOLE:g}, strip {TAB_W:g}, bend R ≥ {BEND_R:g}):")
        for name, tab in a.tabs.items():
            pts = " → ".join(f"({u:.2f}, {s:.2f})" for u, s in tab.points)
            lines.append(f"- {name}: {pts}.")
        lines.append("")
        lines.extend(_ref_tab_route_section())
        st0, st1 = standoff_y(spec)
        lines.append("")
        lines.append(
            f"Stack at each site: floor {FLOOR_Y:g}, ring {ring_under(spec):g}, brass standoff "
            f"{spec.standoff:g} ({STANDOFF_AF:g} AF, circumradius {STANDOFF_CIRCUMR:g}) from y {st0:.2f} to "
            f"{st1:.2f} = board underside. ISO 7380 M2.5×{SCREW_L:g} from outside projects {SCREW_PROJ:g} "
            f"past the floor and ends {tip_below_standoff_top(spec):.2f} below the standoff top. "
            "No nut: the standoff's female thread takes the screw (plan v2 §5.3). The flex over the "
            "standoffs is not fastened to them; its retention is WP14's."
        )
        lines.append("Harness 100 ± 3 mm: NOT_MEASURED (routed length, not a solid).")
        others = [x for x in ("B", "C") if per.get(x) is None]
        if others:
            lines.append("")
            lines.append(f"{' and '.join(others)} do not close. There is no board-lane layout for them.")
    lines.append("")
    lines.extend(_layout_v2_section())
    lines.append("## 6. Winners sent to Stage B (at most six)")
    lines.append("")
    if closed:
        for r in closed[:6]:
            mark = " — Stage B winner (`scripts/cad/params/stageb_v2.toml`)" if r.spec == winner else ""
            lines.append(f"- `{r.spec.tag}`{mark}")
        lines.append("")
        lines.append(
            "Construction is the order-1 path with packing C (width 20, arc 48.4). No fork. "
            "Build (writes only into the temp dir; exit 3 = files written, not every check passed):"
        )
        lines.append("")
        lines.append("```bash")
        lines.append(
            ".venv/bin/python scripts/cad/bte_fit_shell.py --params scripts/cad/params/stageb_v2.toml "
            "--out /tmp/elicio-stageb-v2/"
        )
        lines.append("```")
        lines.append("")
        lines.append(f"Measured on the built `{winner.tag}` solid (review r5; `tests/test_cad.py` checks these rows against a fresh build):")
        lines.append("")
        lines.append("| check | result | numbers |")
        lines.append("|---|---|---|")
        for name, (status, nums, text) in STAGE_B_V2_MEASURED.items():
            shown = "; ".join(x for x in (", ".join(f"{k} {v:g}" for k, v in nums.items()), text) if x)
            lines.append(f"| `{name}` | {status} | {_md_cell(shown)} |")
    else:
        lines.append("None close. Stage B still measures a representative overlay on the order-1 solid.")
    lines.append("")
    lines.append("## 7. Numbers taken as given")
    lines.append("")
    lines.append("| Item | Number | Source |")
    lines.append("|---|---|---|")
    for key in ARCHES:
        m = MODULE[key]
        lines.append(f"| {m['name']} | {m['w']:g} × {m['l']:g} × {m['h']:g} | {'out, plan v2 turn 02' if key == 'C' else 'plan v2 §3'} |")
        lines.append(f"| {m['name']} antenna keep-out | {m['ant'][0]:g} × {m['ant'][1]:g} | {m['ant_from']} |")
    for key in CELL:
        c = CELL[key]
        lines.append(f"| {c['name']} | {c['l']:g} × {c['w']:g} × {c['t']:g} | {c['from']} |")
    lines.append(f"| Foam on the cell | {FOAM:g} | plan v1 §5 and order-1 CELL_envelope; plan v2 §3 says 0.3 (decision 57) |")
    lines.append(f"| Interface I board | FR4 {BOARD_RIGID:g}, 4-layer | plan v2 §5.2 |")
    lines.append(f"| Interface I pad | {PAD_XY:g} × {PAD_XY:g} ENIG | turn 07 |")
    lines.append(
        f"| Standoff | M2.5 hex {STANDOFF_AF:g} AF, circumradius {STANDOFF_CIRCUMR:g}, heights "
        + ", ".join(f"{x:g}" for x in STANDOFFS)
        + " | plan v2 §3; C14 |"
    )
    lines.append(f"| Boss drop | {BOSS_DROP:g} | turn 07/09 |")
    lines.append(f"| Cell floor recess | {CELL_RECESS:g}, web 1.0 | turn 09; C15 NOT_MEASURED |")
    lines.append(f"| Placement tolerance | {PLACEMENT_TOL:g} | JLC printed floor ±0.3 |")
    lines.append(
        f"| Flex board | PI {FLEX:g} + FR4 {STIFFENER:g} = {BOARD_AT_PARTS:g} at parts, "
        f"PI {FLEX:g} + FR4 {STIFFENER_TAB:g} = {BOARD_AT_TABS:g} at rings | JLC FPC stiffener list "
        "(0.1/0.2/0.4 …, no 0.3), read by WP12 2026-09-17 |"
    )
    lines.append(f"| ADS1292 VQFN-32 courtyard | {VQFN[0]:g} × {VQFN[1]:g} × {VQFN[2]:g} | WP11 brief |")
    lines.append(f"| BQ25100 | {BQ[0]:g} × {BQ[1]:g} × {BQ[2]:g} | WP11 brief |")
    lines.append(f"| TLV71330 SOT-23-5 / USBLC6-2SC6 SOT-23-6 | {LDO[0]:g} × {LDO[1]:g} × {LDO[2]:g} | board BOM; placement.py SOT-23 occupied area; TI DBV max height |")
    lines.append(f"| PESD5V0L1UL | {SOD523[0]:g} × {SOD523[1]:g} × {SOD523[2]:g} | board land D_SOD-523 |")
    lines.append(f"| Recovery switch | {SWITCH[0]:g} × {SWITCH[1]:g} × {SWITCH[2]:g} | coordinator note 3 |")
    lines.append(f"| Bench header | {HEADER[0]:g} × {HEADER[1]:g} × {HEADER[2]:g} | plan v2 §5.6 |")
    lines.append(f"| USB-C 16-pin | {USB[0]:g} × {USB[1]:g} × {USB[2]:g} | WP11 brief |")
    lines.append(
        f"| USB opening / recess / ligament | {USB_OPENING[0]:g} × {USB_OPENING[1]:g} / {USB_RECESS:g} / {USB_LIGAMENT:g} | coordinator note 1 |"
    )
    lines.append(f"| Plug volume | {PLUG_VOLUME[0]:g} × {PLUG_VOLUME[1]:g} × {PLUG_VOLUME[2]:g} | plan v2 §5.4 |")
    lines.append(f"| JST-SH | {JST[0]:g} × {JST[1]:g} × {JST[2]:g} side entry | WP11 brief |")
    lines.append(f"| Ring pad | Ø{RING_D:g}, hole Ø{RING_HOLE:g}, strip {TAB_W:g} | plan v2 §5.3 interface II |")
    lines.append(f"| Flex tab bend (WP11b REF search) | R {BOARD_BEND_R:g} | board-v2.md §11 |")
    lines.append(f"| Screw ISO 7380 M2.5×{SCREW_L:g} | projects {SCREW_PROJ:g} past the floor | v1 |")
    lines.append("| Harness | 100 ± 3 mm | plan v2; NOT_MEASURED as a solid |")
    lines.append(
        f"| BODY_WIDTH / LID_Y / BODY_ARC | {WIDTHS[0]:g}–{WIDTHS[-1]:g} / {LID_YS[0]:g}–{LID_YS[-1]:g} / "
        f"{PATH_BODY_ARC:g} | coordinator note 1; other params stageb_provisional.toml |"
    )
    lines.append(f"| M1 | {M1_DEFAULT:g} | default.toml; Q34 blank |")
    lines.append(f"| Floor | {FLOOR_Y:g} | v1 |")
    lines.append("")
    lines.append("## 8. What could not be measured")
    lines.append("")
    for name, (status, _nums, text) in STAGE_B_V2_MEASURED.items():
        if status == "NOT_MEASURED":
            lines.append(f"- `{name}`: {text}")
    lines.append(
        "- Nominal and deformed cell clearance for Interface I: packing arithmetic, not a solid probe. G5/G7 remain open."
    )
    lines.append("- E73 antenna sheet: unreachable; v1 12.4 × 3.8 used.")
    lines.append("- M1 on Rolf (Q34): default 52 used for the gate.")
    lines.append(
        "- REF tab lid-to-wall gap: packing treats the cavity end wall as solid from floor "
        f"{FLOOR_Y:g} to LID_Y 8.0; a gap under the lid was not probed on the solid."
    )
    lines.append(
        "- 501015 pack in ones: none found (`docs/fab/L7-research-v4.md` §2). "
        "DTP301120 is sold in ones (SparkFun PRT-25270). "
        "LP501218JH is sold in ones (DigiKey 1908-LP501218JH+PCM+2WIRE50MM-ND) with bare 2-wire leads; "
        "plan v2 R2, Rolf solders nothing, so it is a candidate only if the assembler or the seller "
        "terminates the leads. This package does not order."
    )
    lines.append(
        "- 501015 pack with PCM: DNK/Benzo sheets give 17 × 10 × 5.0 (L7-research-v4.md §7 and §7.8). "
        "The 17.0 mm pack was not probed on a solid; packing arithmetic only. "
        "The 501012 13.0 × 10.1 × 5.1 figure is an eBay marketplace quote (L7 §7), not a manufacturer sheet."
    )
    lines.append("")
    lines.append("## 9. Drawings in the repo")
    lines.append("")
    lines.append(
        "Q56: the repo keeps only the drawings of the runs that close, the Stage B winner "
        "(`scripts/cad/params/stageb_v2.toml`) and the first run, in table order, of each "
        "first-conflict family (the first conflict with its numbers masked). "
        "`placement.py --all` writes the closers, `--kept-drawings` this set, and "
        "`--all-drawings --out-dir <tmp>` every run (never committed). All under `docs/fab/cad/v1/`."
    )
    lines.append("")
    lines.append("| drawing | why kept |")
    lines.append("|---|---|")
    reps = {r.spec: fam for fam, r in family_representatives(rows).items()}
    for spec in kept_drawing_specs(rows):
        why = []
        if any(r.spec == spec and r.closes for r in rows):
            why.append("closes")
        if spec == winner:
            why.append("Stage B winner")
        if spec in reps:
            why.append(f"family: {_md_cell(reps[spec])}")
        lines.append(f"| `{spec.filename}` | {'; '.join(why)} |")
    lines.append("")
    return "\n".join(lines) + "\n"


def write_packing_doc(path: Path | None = None, *, include_arc: bool = False) -> Path:
    dest = path or (ROOT / "docs" / "fab" / "packing-v2.md")
    dest.write_text(packing_markdown(run_matrix(include_arc=include_arc)), encoding="utf-8")
    return dest
