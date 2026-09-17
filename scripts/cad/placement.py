#!/usr/bin/env python3.13
"""Stage B board packing drawing (plan §5, interface v2; WP6b options).

2D drawing in the body-frame (u, s) plane. Headless matplotlib, Agg,
deterministic SVG. Does not edit CAD solids or ``manifest.json``.

``--option A`` (default) is the plan shell with the TE 31428 lug
(contacts.md §8.1, C-31428 rev D4). B lengthens BODY_ARC 3.5 mm.
C widens BODY_WIDTH 3 mm. E keeps the shell and uses the lateral face.

Q13 short tabs (end under the pad, 3 mm wide) stay as a budget mask
only. No crimp ring lug ends under its pad. See packing-options.md.

``layout_conflicts(option)`` lists every rule that option breaks. An
empty list is the only state that confirms that option. Packing of the
product waits on ``docs/fab/packing-options.md`` until Rolf picks.

Coupon-to-parameter mapping (plan §10 open item 2; interface §12 V2-2).
The coupon itself is built in ``bte_fit_shell.py`` ``build_coupon``. Axes
are x and y across the top face from its centre; the rib stands on the
top face.

* hole (−3, −3) Ø1.7 through → smallest round hole the process opens;
  lower bracket for CONTACT_HOLE
* hole (0, −3) Ø2.9 through → CONTACT_HOLE directly: an M2.5 shank
  (2.5) must pass
* hole (3, −3) Ø3.4 through → upper bracket: CONTACT_HOLE moves toward
  it if Ø2.9 prints under 2.5
* slot (0, 2), 6 long, 0.9 wide through → TONGUE_SLOT height (0.9) and
  the 0.4 tongue clearance
* slot (0, 4), 6 long, 0.4 wide through → whether a 0.4 gap prints open:
  CLEAR_FIT and the 0.4 rigid-pair nominals (plan §3.6)
* rib along x at y −0.5, 0.4 thick × 3 tall × 12 long → E4; the
  thin-feature floor under E1 (tongue 0.5) and E3 (nubs 0.8)

Run::

    .venv/bin/python scripts/cad/placement.py
    .venv/bin/python scripts/cad/placement.py --option A --out docs/fab/cad/v1/placement.svg
    .venv/bin/python scripts/cad/placement.py --option B --out docs/fab/cad/v1/placement_B.svg
"""
from __future__ import annotations

import argparse
import functools
import hashlib
import importlib.util
import io
import math
import re
import sys
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Mapping

import numpy as np

HAS_MATPLOTLIB = importlib.util.find_spec("matplotlib") is not None

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "docs" / "fab" / "cad" / "v1" / "placement.svg"
OPTION_NAMES = ("A", "B", "C", "E")

# ---------------------------------------------------------------------------
# Geometry (millimetres). Raster pitch is 0.025 mm.
# ---------------------------------------------------------------------------

RASTER_PITCH = 0.025
PATH_RADIUS = 97.10250594613626  # manifest PATH_RADIUS; plan §3.2 via WP2
BOARD_LEN = 19.0
BOARD_WID = 12.5
BOARD_U = (2.25, 14.75)  # BOARD_ZONE u 1.5–15.5 minus side clearance 0.75
BOARD_S = (18.6, 37.6)  # BOARD_ZONE s 18.3–37.9 minus end clearance 0.3
BOARD_ZONE_U = (1.5, 15.5)
BOARD_ZONE_S = (18.3, 37.9)
CAVITY_U = (1.5, 15.5)
CAVITY_S = (1.5, 38.2)
BODY_U = (0.0, 17.0)
BODY_ARC = 48.4  # plan §3.2
BODY_WIDTH = 17.0
CREASE_BOW = 3.0
OPTION_B_DS = 3.5  # BODY_ARC +3.5; interface §8.2 B
OPTION_C_DU = 3.0  # BODY_WIDTH +3; interface §8.2 C
BATTERY_U = (3.1, 13.9)
BATTERY_S = (1.5, 17.5)
RIB_U = (1.5, 15.5)
RIB_S = (17.5, 18.3)
CONTACT_1 = (5.9, 22.0)
CONTACT_2 = (10.4, 33.1)
KEEPOUT_R = 3.55  # Ø7.1 / 2
COPPER_FREE = 0.5
RIM = 0.25  # plan §5 rim ≈ 15 mm² on a 19 × 12.5 board
ANTENNA_ALONG_S = 3.8  # Raytac Spec K p.9 and p.13, issued 2022-07-01
ANTENNA_WID = 12.4  # Spec K p.9 "No ground pad" width
MODULE_L = 15.5
MODULE_W = 10.5
MODULE_L_MAX = 15.7  # 15.5 + 0.2 Spec K p.7
MODULE_L_RESERVED = 15.8  # plan §5 reserved maximum
CELL_BODY_MAX = (5.2, 10.4, 15.6)  # thick, wide, long; plan §5
DNK_CELL = (5.0, 10.0, 15.0)
DNK_BL_MAX = 18.0  # 17 ± 1 in-line PCM
PAD_SIZE = 1.0  # lead-pad copper, millimetres
CORNER_PAD = 1.5
WIRE_OD = 1.3
BEND_R = 3.0
WRAP_S = 37.0
CHANNEL_U = (7.7, 9.3)
CHANNEL_S = (38.2, 40.5)
CLAMP_MAX_MM = 10.0
BATTERY_RF_MIN = 5.0
# TE Connectivity 31428, Customer Drawing C-31428 rev D4, date read
# 2026-09-17 (contacts.md §8.1). Ring OD 5.16 → radius 2.58. Barrel end
# 8.85 from the ring centre. Packing envelope: 1.96 wide, 6.27 long from
# the Ø7.1 edge (WP6b second pass). The tab need not point at its pad;
# the wire does that. Q13 short tabs are not buildable with a crimp lug.
RING_OD = 5.16
RING_R = RING_OD / 2.0
LUG_A1 = 8.85  # physical barrel end from the ring centre
TAB_W = 1.96
TAB_LEN = 6.27  # from the Ø7.1 keep-out edge
LUG_THICK = 0.46
TAB_W_Q13 = 3.0
LITERAL_TAB_LEN = 7.0
TAB_SEARCH_STEP = 5.0
SKIN_Y = 1.5
TAB_MODES = ("real", "q13", "literal")
KEEPOUT_TOP_Y = 4.13
BOARD_UNDERSIDE_Y = 4.3
BOARD_TOP_Y = 5.3  # underside 4.3 + core 1.0; plan §5
LID_Y = 8.0
FOAM_THICK = 0.5  # plan §5 foam strip over the superior 3 mm
FOAM_SUPERIOR_MM = 3.0
LATERAL_H = LID_Y - BOARD_TOP_Y  # 2.7
LATERAL_H_FOAM = LATERAL_H - FOAM_THICK  # 2.2 under the foam strip
ARRAY_H_MAX = 1.2  # interface §6.4 BAV199S-Q
PAD_Y = (1.5, 4.3)
SIDE_CLEAR = 0.75
END_CLEAR = 0.3
WALL = 1.5

# Courtyards at maximum dimensions (IPC-7351B Nominal unless named).
# SOT-23 / SOT-363 use the vendor reflow "occupied area".
VQFN_CY = (4.60, 4.60)  # RSM 4.10 body max + 2 × 0.25
TQFP_CY = (7.60, 7.60)  # 7.10 lead span max + 2 × 0.25
SOT23_CY = (3.30, 2.90)  # Nexperia BAV199 Fig. 9 occupied
ARRAY_CY = (2.65, 2.35)  # Nexperia BAV199S-Q Fig. 8 occupied
BQ_CY = (2.10, 1.40)  # 1.60 × 0.90 + 2 × 0.25
LDO_CY = (1.50, 1.50)  # TLV713 X2SON 1.00 × 1.00 + 2 × 0.25
R0402_CY = (1.80, 0.90)  # IPC-7351B small-chip Nominal
N_0402 = 25
# BAV199S-Q is two independent series pairs (pins 1-6-2 and 4-3-5); each
# protected line needs its own pair, so three lines need two arrays.
PAIRS_PER_ARRAY = 2
N_ARRAYS = 2
N_LINES = 3

# Lead pads (interface v2 §4). Frozen in the interface until Rolf picks.
# Option sheets may carry the same numbers as candidates.
LEAD_PADS: dict[str, tuple[float, float]] = {
    "SIG1": (5.9, 26.6),
    "SIG2": (5.5, 30.0),
    "REF": (4.0, 29.0),
}
PAD_CONTACT: dict[str, tuple[float, float] | None] = {
    "SIG1": CONTACT_1,
    "SIG2": CONTACT_2,
    "REF": None,
}

# Candidate layout. placed_parts() puts each part, in this order, at the
# legal site whose centre is nearest the target (u, s).
PART_TARGETS: dict[str, tuple[tuple[float, float], tuple[float, float]]] = {
    "ADS1292_RSM": (VQFN_CY, (12.3, 21.2)),
    "BAV199S_1": (ARRAY_CY, (5.7, 28.3)),
    "BAV199S_2": (ARRAY_CY, (4.0, 29.0)),
    "BQ25100": (BQ_CY, (11.3, 24.2)),
    "TLV713": (LDO_CY, (13.1, 24.2)),
}
ARRAY_LINES: dict[str, tuple[str, ...]] = {
    "BAV199S_1": ("SIG1", "SIG2"),
    "BAV199S_2": ("REF",),
}
LINE_ARRAY = {pad: name for name, pads in ARRAY_LINES.items() for pad in pads}

# Reference wire: pocket → channel → wrap at s 37 → REF pad. The path
# is chosen with the tab angles so the Ø1.3 jacket misses both barrels.
# Low-u hugs keep-out 2 on the posterior side. High-u goes round K2 on
# the inferior / high-u side when SIG2's barrel occupies low-u.
REF_WIRE_LOW_U: tuple[tuple[float, float], ...] = (
    (8.5, 40.5),
    (8.5, 38.2),
    (8.5, 37.0),
    (2.8, 36.5),
    (2.8, 29.0),
    (4.0, 29.0),
)
REF_WIRE_HIGH_U: tuple[tuple[float, float], ...] = (
    (8.5, 40.5),
    (8.5, 38.2),
    (8.5, 37.0),
    (10.4, 37.50),
    (14.80, 37.50),
    (14.80, 26.4),
    (4.0, 26.4),
    (4.0, 29.0),
)
REF_WIRE_INFERIOR: tuple[tuple[float, float], ...] = (
    (8.5, 40.5),
    (8.5, 41.0),
    (14.80, 41.0),
    (14.80, 26.4),
    (4.0, 26.4),
    (4.0, 29.0),
)
# Search result (search_tab_degrees). Flat. 0° = +u, 90° = +s.
TAB_DEG_BY_OPTION: dict[str, dict[str, float]] = {
    "A": {"SIG1": 25.0, "SIG2": 290.0},
    "B": {"SIG1": 25.0, "SIG2": 290.0},
    "C": {"SIG1": 5.0, "SIG2": 255.0},
    "E": {"SIG1": 25.0, "SIG2": 290.0},
}
TAB_DEG: dict[str, float] = dict(TAB_DEG_BY_OPTION["A"])
REF_WIRE_BY_OPTION: dict[str, tuple[tuple[float, float], ...]] = {
    "A": REF_WIRE_LOW_U,
    "B": REF_WIRE_LOW_U,
    "C": REF_WIRE_LOW_U,
    "E": REF_WIRE_LOW_U,
}
REF_WIRE = REF_WIRE_LOW_U


@dataclass(frozen=True, slots=True)
class Layout:
    option: str
    board_len: float
    board_wid: float
    board_u: tuple[float, float]
    board_s: tuple[float, float]
    board_zone_u: tuple[float, float]
    board_zone_s: tuple[float, float]
    cavity_u: tuple[float, float]
    cavity_s: tuple[float, float]
    body_u: tuple[float, float]
    body_arc: float
    two_sided: bool
    lead_pads: Mapping[str, tuple[float, float]]
    ref_wire: tuple[tuple[float, float], ...]
    tab_deg: Mapping[str, float]
    give_up: str


@dataclass(frozen=True, slots=True)
class Budget:
    board_mm2: float
    keepout1_mm2: float
    keepout1_margin_mm2: float
    keepout2_mm2: float
    keepout2_union_antenna_mm2: float
    tabs_margin_mm2: float
    rim_mm2: float
    blocked_mm2: float
    free_mm2: float
    free_without_tabs_mm2: float
    free_tabs_to_pad_mm2: float
    free_literal_mm2: float
    lateral_free_mm2: float
    largest_u: float
    largest_s: float
    largest_mm2: float
    tqfp_fits: bool
    vqfn_fits: bool
    required_as_drawn_mm2: float
    required_named_mm2: float
    spare_named_mm2: float
    clamp_pairs: int
    sagitta_mm: float
    y_clear_mm: float
    battery_to_module_hook_mm: float
    battery_to_module_rib_mm: float
    battery_to_module_hook_nominal_mm: float
    battery_to_antenna_hook_mm: float
    rf_keepout2_overlap: bool
    n_0402: int
    body_arc_mm: float
    total_chord_mm: float
    m1_gate_mm: float
    option: str


def chord_from_arc_bow(arc: float, bow: float = CREASE_BOW) -> tuple[float, float]:
    """Return (chord, radius) for arc length and sagitta, millimetres.

    Same iteration as ``bte_fit_shell.chord_from_arc_bow`` (plan §3.2).
    """
    lo, hi = 1e-9, arc
    for _ in range(80):
        chord = (lo + hi) / 2.0
        radius = chord * chord / (8.0 * bow) + bow / 2.0
        length = 4.0 * radius * math.atan(2.0 * bow / chord)
        if length > arc:
            hi = chord
        else:
            lo = chord
    chord = (lo + hi) / 2.0
    radius = chord * chord / (8.0 * bow) + bow / 2.0
    return chord, radius


def _build_options() -> dict[str, Layout]:
    pads = dict(LEAD_PADS)
    a = Layout(
        option="A",
        board_len=BOARD_LEN,
        board_wid=BOARD_WID,
        board_u=BOARD_U,
        board_s=BOARD_S,
        board_zone_u=BOARD_ZONE_U,
        board_zone_s=BOARD_ZONE_S,
        cavity_u=CAVITY_U,
        cavity_s=CAVITY_S,
        body_u=BODY_U,
        body_arc=BODY_ARC,
        two_sided=False,
        lead_pads=pads,
        ref_wire=REF_WIRE_BY_OPTION["A"],
        tab_deg=dict(TAB_DEG_BY_OPTION["A"]),
        give_up="packing does not close on the plan shell",
    )
    b_s1 = BOARD_S[1] + OPTION_B_DS
    b = Layout(
        option="B",
        board_len=BOARD_LEN + OPTION_B_DS,
        board_wid=BOARD_WID,
        board_u=BOARD_U,
        board_s=(BOARD_S[0], b_s1),
        board_zone_u=BOARD_ZONE_U,
        board_zone_s=(BOARD_ZONE_S[0], BOARD_ZONE_S[1] + OPTION_B_DS),
        cavity_u=CAVITY_U,
        cavity_s=(CAVITY_S[0], CAVITY_S[1] + OPTION_B_DS),
        body_u=BODY_U,
        body_arc=BODY_ARC + OPTION_B_DS,
        two_sided=False,
        lead_pads=pads,
        ref_wire=REF_WIRE_BY_OPTION["B"],
        tab_deg=dict(TAB_DEG_BY_OPTION["B"]),
        give_up="3.5 mm of length behind the ear; M1 gate moves; VQFN still has no site",
    )
    c_u1 = BOARD_U[1] + OPTION_C_DU
    c = Layout(
        option="C",
        board_len=BOARD_LEN,
        board_wid=BOARD_WID + OPTION_C_DU,
        board_u=(BOARD_U[0], c_u1),
        board_s=BOARD_S,
        board_zone_u=(BOARD_ZONE_U[0], BOARD_ZONE_U[1] + OPTION_C_DU),
        board_zone_s=BOARD_ZONE_S,
        cavity_u=(CAVITY_U[0], CAVITY_U[1] + OPTION_C_DU),
        cavity_s=CAVITY_S,
        body_u=(BODY_U[0], BODY_U[1] + OPTION_C_DU),
        body_arc=BODY_ARC,
        two_sided=False,
        lead_pads=pads,
        ref_wire=REF_WIRE_BY_OPTION["C"],
        tab_deg=dict(TAB_DEG_BY_OPTION["C"]),
        give_up="3 mm of width in the crease",
    )
    e = Layout(
        option="E",
        board_len=BOARD_LEN,
        board_wid=BOARD_WID,
        board_u=BOARD_U,
        board_s=BOARD_S,
        board_zone_u=BOARD_ZONE_U,
        board_zone_s=BOARD_ZONE_S,
        cavity_u=CAVITY_U,
        cavity_s=CAVITY_S,
        body_u=BODY_U,
        body_arc=BODY_ARC,
        two_sided=True,
        lead_pads=pads,
        ref_wire=REF_WIRE_BY_OPTION["E"],
        tab_deg=dict(TAB_DEG_BY_OPTION["E"]),
        give_up="a two-sided assembly; the VQFN still has no site on the medial face",
    )
    return {"A": a, "B": b, "C": c, "E": e}


OPTIONS = _build_options()


def get_layout(option: str = "A") -> Layout:
    key = option.upper()
    if key not in OPTIONS:
        raise ValueError(f"option must be one of {OPTION_NAMES}, got {option!r}")
    return OPTIONS[key]


def drawing_path(option: str = "A") -> Path:
    lay = get_layout(option)
    if lay.option == "A":
        return DEFAULT_OUT
    return DEFAULT_OUT.with_name(f"placement_{lay.option}.svg")


def named_drawing_path(option: str) -> Path:
    return DEFAULT_OUT.with_name(f"placement_{get_layout(option).option}.svg")


def _mesh(option: str = "A") -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    lay = get_layout(option)
    u0, u1 = lay.board_u
    s0, s1 = lay.board_s
    du = RASTER_PITCH
    nu = int(round((u1 - u0) / du))
    ns = int(round((s1 - s0) / du))
    u = u0 + (np.arange(nu) + 0.5) * du
    s = s0 + (np.arange(ns) + 0.5) * du
    uu, ss = np.meshgrid(u, s, indexing="xy")
    return u, s, uu, ss


def _area(mask: np.ndarray) -> float:
    return float(mask.sum()) * RASTER_PITCH * RASTER_PITCH


def _punch_circle(mask: np.ndarray, uu: np.ndarray, ss: np.ndarray, uc: float, sc: float, r: float) -> np.ndarray:
    return mask & (((uu - uc) ** 2 + (ss - sc) ** 2) >= r * r)


def _punch_rect(
    mask: np.ndarray, uu: np.ndarray, ss: np.ndarray, ua: float, ub: float, sa: float, sb: float
) -> np.ndarray:
    return mask & ~((uu >= ua) & (uu <= ub) & (ss >= sa) & (ss <= sb))


def tab_width(mode: str = "real") -> float:
    if mode not in TAB_MODES:
        raise ValueError(f"mode must be one of {TAB_MODES}, got {mode!r}")
    return TAB_W if mode == "real" else TAB_W_Q13


def tab_span(pad: str, option: str = "A", *, mode: str = "real") -> tuple[float, float]:
    """Start and end of a signal lug tab along its axis, from the contact centre.

    ``mode="real"`` is TE 31428 on the board: Ø7.1 edge to Ø7.1 + 6.27.
    ``mode="q13"`` is the short-tab reading: Ø7.1 edge to the far pad edge.
    ``mode="literal"`` is the r2 7 mm envelope from the Ø7.1 edge.
    """
    if mode not in TAB_MODES:
        raise ValueError(f"mode must be one of {TAB_MODES}, got {mode!r}")
    if mode == "real":
        return KEEPOUT_R, KEEPOUT_R + TAB_LEN
    if mode == "literal":
        return KEEPOUT_R, KEEPOUT_R + LITERAL_TAB_LEN
    lay = get_layout(option)
    c = PAD_CONTACT[pad]
    assert c is not None
    pu, ps = lay.lead_pads[pad]
    d = math.hypot(pu - c[0], ps - c[1])
    return KEEPOUT_R, d + PAD_SIZE / 2.0


def _tab_axes(
    pad: str, option: str = "A", *, mode: str = "real", deg: float | None = None
) -> tuple[tuple[float, float], float, float]:
    c = PAD_CONTACT[pad]
    assert c is not None
    if mode == "real":
        angle = get_layout(option).tab_deg[pad] if deg is None else deg
        rad = math.radians(angle)
        return c, math.cos(rad), math.sin(rad)
    lay = get_layout(option)
    pu, ps = lay.lead_pads[pad]
    d = math.hypot(pu - c[0], ps - c[1])
    return c, (pu - c[0]) / d, (ps - c[1]) / d


def point_tab_gap(
    pad: str,
    u: float,
    s: float,
    option: str = "A",
    *,
    mode: str = "real",
    deg: float | None = None,
) -> float:
    """Distance from (u, s) to the tab rectangle of ``pad``'s contact; 0 inside."""
    (cu, cs), eu, es = _tab_axes(pad, option, mode=mode, deg=deg)
    a0, a1 = tab_span(pad, option, mode=mode)
    along = (u - cu) * eu + (s - cs) * es
    across = -(u - cu) * es + (s - cs) * eu
    da = max(a0 - along, 0.0, along - a1)
    dc = max(abs(across) - tab_width(mode) / 2.0, 0.0)
    return math.hypot(da, dc)


def tab_corners(
    pad: str, option: str = "A", *, mode: str = "real", deg: float | None = None
) -> list[tuple[float, float]]:
    (cu, cs), eu, es = _tab_axes(pad, option, mode=mode, deg=deg)
    a0, a1 = tab_span(pad, option, mode=mode)
    h = tab_width(mode) / 2.0
    return [
        (cu + a * eu - c * es, cs + a * es + c * eu)
        for a, c in ((a0, -h), (a1, -h), (a1, h), (a0, h))
    ]


def _tab_mask(
    uu: np.ndarray,
    ss: np.ndarray,
    pad: str,
    margin: float,
    option: str = "A",
    *,
    mode: str = "real",
) -> np.ndarray:
    (cu, cs), eu, es = _tab_axes(pad, option, mode=mode)
    a0, a1 = tab_span(pad, option, mode=mode)
    along = (uu - cu) * eu + (ss - cs) * es
    across = -(uu - cu) * es + (ss - cs) * eu
    half = tab_width(mode) / 2.0 + margin
    return (along >= a0 - margin) & (along <= a1 + margin) & (np.abs(across) <= half)


def upright_signal_clear_mm() -> float:
    """Air above the skin in the signal keep-out, minus the upright lug.

    Ring stock 0.46 plus barrel 6.27. Keep-out top is 4.13. The board
    underside is 4.3. Both are short of 6.73, so SIG1 and SIG2 stay flat.
    Reference uses the tail pocket (contacts.md §5.3), not this cylinder.
    """
    have = KEEPOUT_TOP_Y - SKIN_Y
    need = LUG_THICK + TAB_LEN
    return have - need


def bind_layout(
    option: str,
    *,
    tab_deg: Mapping[str, float] | None = None,
    ref_wire: tuple[tuple[float, float], ...] | None = None,
) -> Layout:
    """Swap tab angles or the reference wire on a live option (search / tests)."""
    key = option.upper()
    current = OPTIONS[key]
    OPTIONS[key] = replace(
        current,
        tab_deg=dict(tab_deg) if tab_deg is not None else current.tab_deg,
        ref_wire=ref_wire if ref_wire is not None else current.ref_wire,
    )
    placed_layout.cache_clear()
    return OPTIONS[key]


def antenna_rect(option: str = "A") -> tuple[float, float, float, float]:
    """Return (u0, u1, s0, s1) of the no-copper zone on the board."""
    lay = get_layout(option)
    u0, u1 = lay.board_u
    s1 = lay.board_s[1]
    s0 = s1 - ANTENNA_ALONG_S
    mid = 0.5 * (u0 + u1)
    half = ANTENNA_WID / 2.0
    return (max(u0, mid - half), min(u1, mid + half), s0, s1)


def module_rect(length: float = MODULE_L, option: str = "A") -> tuple[float, float, float, float]:
    """Module on the board, antenna at the inferior edge (nominal by default)."""
    lay = get_layout(option)
    u0, u1 = lay.board_u
    s1 = lay.board_s[1]
    s0 = s1 - length
    mid = 0.5 * (u0 + u1)
    half = MODULE_W / 2.0
    return (mid - half, mid + half, s0, s1)


def sagitta_mm(chord: float = BOARD_LEN, radius: float = PATH_RADIUS) -> float:
    half = chord / 2.0
    return radius - math.sqrt(radius * radius - half * half)


def chord_gap_at(distance_from_mid: float, chord: float = BOARD_LEN, radius: float = PATH_RADIUS) -> float:
    """Arc-to-chord gap in the path plane, millimetres, at |x| from mid-s."""
    h = sagitta_mm(chord, radius)
    x = abs(distance_from_mid)
    half = chord / 2.0
    if x >= half:
        return 0.0
    return math.sqrt(radius * radius - x * x) - (radius - h)


def board_free_mask(
    tabs: bool = True,
    option: str = "A",
    punch_module: bool = False,
    *,
    mode: str = "real",
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Copper-free mask on one face. Default tabs are TE 31428 (real)."""
    lay = get_layout(option)
    u, s, uu, ss = _mesh(option)
    free = np.ones(uu.shape, dtype=bool)
    free = _punch_circle(free, uu, ss, CONTACT_1[0], CONTACT_1[1], KEEPOUT_R + COPPER_FREE)
    free = _punch_circle(free, uu, ss, CONTACT_2[0], CONTACT_2[1], KEEPOUT_R + COPPER_FREE)
    if tabs:
        for pad in ("SIG1", "SIG2"):
            free &= ~_tab_mask(uu, ss, pad, COPPER_FREE, option, mode=mode)
    au0, au1, as0, as1 = antenna_rect(option)
    free = _punch_rect(free, uu, ss, au0, au1, as0, as1)
    u0, u1 = lay.board_u
    s0, s1 = lay.board_s
    free = _punch_rect(free, uu, ss, u0, u0 + RIM, s0, s1)
    free = _punch_rect(free, uu, ss, u1 - RIM, u1, s0, s1)
    free = _punch_rect(free, uu, ss, u0, u1, s0, s0 + RIM)
    free = _punch_rect(free, uu, ss, u0, u1, s1 - RIM, s1)
    if punch_module:
        mu0, mu1, ms0, ms1 = module_rect(MODULE_L_RESERVED, option)
        free = _punch_rect(free, uu, ss, mu0, mu1, ms0, ms1)
    return u, s, uu, free


def _largest_rect(free: np.ndarray) -> tuple[float, float, float]:
    ns, nu = free.shape
    height = np.zeros(nu, dtype=int)
    best = 0
    best_wh = (0, 0)
    for r in range(ns):
        height = np.where(free[r], height + 1, 0)
        stack: list[tuple[int, int]] = []
        hist = np.append(height, 0)
        for i, hi in enumerate(hist):
            last = i
            while stack and stack[-1][0] > hi:
                hj, j = stack.pop()
                area = hj * (i - j)
                if area > best:
                    best = area
                    best_wh = (i - j, hj)
                last = j
            stack.append((hi, last))
    wu = best_wh[0] * RASTER_PITCH
    hs = best_wh[1] * RASTER_PITCH
    return wu, hs, wu * hs


def _integral(free: np.ndarray) -> np.ndarray:
    ns, nu = free.shape
    z = np.zeros((ns + 1, nu + 1), dtype=np.int32)
    z[1:, 1:] = free.astype(np.int32).cumsum(0).cumsum(1)
    return z


def _fits_rect(free: np.ndarray, wu: float, ws: float) -> bool:
    du = RASTER_PITCH
    ku = int(round(wu / du))
    ks = int(round(ws / du))
    ns, nu = free.shape
    if ku < 1 or ks < 1 or ku > nu or ks > ns:
        return False
    z = _integral(free)
    tot = z[ks:, ku:] - z[:-ks, ku:] - z[ks:, :-ku] + z[:-ks, :-ku]
    return bool((tot == ks * ku).any())


def _courtyard_in_free(
    free: np.ndarray, u: np.ndarray, s: np.ndarray, x: float, y: float, wu: float, ws: float, option: str = "A"
) -> bool:
    lay = get_layout(option)
    du = RASTER_PITCH
    i0 = int(round((x - lay.board_u[0]) / du))
    j0 = int(round((y - lay.board_s[0]) / du))
    i1 = int(round((x + wu - lay.board_u[0]) / du))
    j1 = int(round((y + ws - lay.board_s[0]) / du))
    if i0 < 0 or j0 < 0 or i1 > free.shape[1] or j1 > free.shape[0] or i1 <= i0 or j1 <= j0:
        return False
    return bool(free[j0:j1, i0:i1].all())


def _boxes_overlap(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> bool:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return not (ax + aw <= bx or bx + bw <= ax or ay + ah <= by or by + bh <= ay)


def pad_box(name: str, option: str = "A") -> tuple[float, float, float, float]:
    pu, ps = get_layout(option).lead_pads[name]
    return (pu - PAD_SIZE / 2.0, ps - PAD_SIZE / 2.0, PAD_SIZE, PAD_SIZE)


def _orientations(name: str, size: tuple[float, float]) -> tuple[tuple[float, float], ...]:
    if name.startswith("BAV") and size[0] != size[1]:
        return (size, (size[1], size[0]))
    return (size,)


def _find_site(
    free: np.ndarray,
    wu: float,
    ws: float,
    target: tuple[float, float],
    taken: list[tuple[float, float, float, float]],
    pads: Mapping[str, tuple[float, float]],
    lines: tuple[str, ...],
    option: str,
    step: float = 0.05,
) -> tuple[float, float, float, float] | None:
    lay = get_layout(option)
    z = _integral(free)
    ku = int(round(wu / RASTER_PITCH))
    ks = int(round(ws / RASTER_PITCH))
    nu = int((lay.board_u[1] - lay.board_u[0] - wu) / step) + 1
    ns = int((lay.board_s[1] - lay.board_s[0] - ws) / step) + 1
    best: tuple[float, float, float] | None = None
    for j in range(ns):
        y = round(lay.board_s[0] + j * step, 4)
        for i in range(nu):
            x = round(lay.board_u[0] + i * step, 4)
            cu, cs = x + wu / 2.0, y + ws / 2.0
            cost = math.hypot(cu - target[0], cs - target[1])
            if best is not None and cost >= best[0]:
                continue
            if any(math.hypot(pads[p][0] - cu, pads[p][1] - cs) > CLAMP_MAX_MM for p in lines):
                continue
            i0 = int(round((x - lay.board_u[0]) / RASTER_PITCH))
            j0 = int(round((y - lay.board_s[0]) / RASTER_PITCH))
            if i0 + ku > free.shape[1] or j0 + ks > free.shape[0]:
                continue
            if z[j0 + ks, i0 + ku] - z[j0, i0 + ku] - z[j0 + ks, i0] + z[j0, i0] != ks * ku:
                continue
            if any(_boxes_overlap((x, y, wu, ws), t) for t in taken):
                continue
            best = (cost, x, y)
    if best is None:
        return None
    return (best[1], best[2], wu, ws)


@functools.cache
def placed_layout(option: str = "A") -> tuple[dict[str, tuple[float, float, float, float]], dict[str, str]]:
    """Greedy candidate layout; a part with no legal site is left out.

    An array must sit within CLAMP_MAX_MM of every pad it clamps.
    Option E searches the lateral face for arrays after the medial face.
    """
    lay = get_layout(option)
    _u, _s, _uu, medial = board_free_mask(option=option)
    lateral = board_free_mask(option=option, punch_module=True)[3] if lay.two_sided else medial
    pads = lay.lead_pads
    taken_m = [pad_box(p, option) for p in pads]
    taken_l = list(taken_m)
    out: dict[str, tuple[float, float, float, float]] = {}
    faces: dict[str, str] = {}
    for name, (size, target) in PART_TARGETS.items():
        lines = ARRAY_LINES.get(name, ())
        prefer_lat = lay.two_sided and name.startswith("BAV")
        face_order = ("lateral", "medial") if prefer_lat else (("medial", "lateral") if lay.two_sided else ("medial",))
        site = None
        face = "medial"
        for face in face_order:
            free = lateral if face == "lateral" else medial
            taken = taken_l if face == "lateral" else taken_m
            for wu, ws in _orientations(name, size):
                site = _find_site(free, wu, ws, target, taken, pads, lines, option)
                if site is not None:
                    break
            if site is not None:
                break
        if site is not None:
            out[name] = site
            faces[name] = face
            if face == "lateral":
                taken_l.append(site)
            else:
                taken_m.append(site)
    return out, faces


def placed_parts(option: str = "A") -> dict[str, tuple[float, float, float, float]]:
    return placed_layout(option)[0]


def placed_faces(option: str = "A") -> dict[str, str]:
    return placed_layout(option)[1]


def budget(option: str = "A") -> Budget:
    lay = get_layout(option)
    u, s, uu, free = board_free_mask(option=option)
    _, _, _, free_no_tabs = board_free_mask(tabs=False, option=option)
    _, _, _, free_q13 = board_free_mask(mode="q13", option=option)
    _, _, _, free_lit = board_free_mask(mode="literal", option=option)
    _, _, _, free_lat = board_free_mask(option=option, punch_module=True)
    _, _, _, ss = _mesh(option)
    board = np.ones(uu.shape, dtype=bool)
    k1 = _punch_circle(board, uu, ss, CONTACT_1[0], CONTACT_1[1], KEEPOUT_R)
    k1m = _punch_circle(board, uu, ss, CONTACT_1[0], CONTACT_1[1], KEEPOUT_R + COPPER_FREE)
    k2 = _punch_circle(board, uu, ss, CONTACT_2[0], CONTACT_2[1], KEEPOUT_R)
    k2m = _punch_circle(board, uu, ss, CONTACT_2[0], CONTACT_2[1], KEEPOUT_R + COPPER_FREE)
    tabs = np.zeros(uu.shape, dtype=bool)
    for pad in ("SIG1", "SIG2"):
        tabs |= _tab_mask(uu, ss, pad, COPPER_FREE, option, mode="real")
    au0, au1, as0, as1 = antenna_rect(option)
    ant = _punch_rect(board, uu, ss, au0, au1, as0, as1)
    u0, u1 = lay.board_u
    s0, s1 = lay.board_s
    rim = _punch_rect(board, uu, ss, u0, u0 + RIM, s0, s1)
    rim = _punch_rect(rim, uu, ss, u1 - RIM, u1, s0, s1)
    rim = _punch_rect(rim, uu, ss, u0, u1, s0, s0 + RIM)
    rim = _punch_rect(rim, uu, ss, u0, u1, s1 - RIM, s1)
    board_mm2 = lay.board_len * lay.board_wid
    lu, ls, la = _largest_rect(free)
    vqfn = _fits_rect(free, VQFN_CY[0], VQFN_CY[1])
    tqfp = _fits_rect(free, TQFP_CY[0], TQFP_CY[1])
    as_drawn = (
        TQFP_CY[0] * TQFP_CY[1]
        + 3 * SOT23_CY[0] * SOT23_CY[1]
        + BQ_CY[0] * BQ_CY[1]
        + LDO_CY[0] * LDO_CY[1]
        + N_0402 * R0402_CY[0] * R0402_CY[1]
    )
    named = (
        VQFN_CY[0] * VQFN_CY[1]
        + N_ARRAYS * ARRAY_CY[0] * ARRAY_CY[1]
        + BQ_CY[0] * BQ_CY[1]
        + LDO_CY[0] * LDO_CY[1]
        + N_0402 * R0402_CY[0] * R0402_CY[1]
    )
    free_mm2 = _area(free)
    cell_hook_end = BATTERY_S[0] + CELL_BODY_MAX[2]
    cell_rib_end = BATTERY_S[1]
    mr = module_rect(MODULE_L_RESERVED, option)[2]
    chord, _radius = chord_from_arc_bow(lay.body_arc, CREASE_BOW)
    return Budget(
        board_mm2=board_mm2,
        keepout1_mm2=board_mm2 - _area(k1),
        keepout1_margin_mm2=board_mm2 - _area(k1m),
        keepout2_mm2=board_mm2 - _area(k2),
        keepout2_union_antenna_mm2=board_mm2 - _area(k2m & ant),
        tabs_margin_mm2=_area(tabs),
        rim_mm2=board_mm2 - _area(rim),
        blocked_mm2=board_mm2 - free_mm2,
        free_mm2=free_mm2,
        free_without_tabs_mm2=_area(free_no_tabs),
        free_tabs_to_pad_mm2=_area(free_q13),
        free_literal_mm2=_area(free_lit),
        lateral_free_mm2=_area(free_lat),
        largest_u=lu,
        largest_s=ls,
        largest_mm2=la,
        tqfp_fits=tqfp,
        vqfn_fits=vqfn,
        required_as_drawn_mm2=as_drawn,
        required_named_mm2=named,
        spare_named_mm2=free_mm2 - named,
        clamp_pairs=N_ARRAYS * PAIRS_PER_ARRAY,
        sagitta_mm=sagitta_mm(lay.board_len),
        y_clear_mm=BOARD_UNDERSIDE_Y - KEEPOUT_TOP_Y,
        battery_to_module_hook_mm=mr - cell_hook_end,
        battery_to_module_rib_mm=mr - cell_rib_end,
        battery_to_module_hook_nominal_mm=module_rect(MODULE_L, option)[2] - cell_hook_end,
        battery_to_antenna_hook_mm=as0 - cell_hook_end,
        rf_keepout2_overlap=as0 < CONTACT_2[1] + KEEPOUT_R,
        n_0402=len(place_0402s(option=option)),
        body_arc_mm=lay.body_arc,
        total_chord_mm=chord,
        m1_gate_mm=chord + 3.0,
        option=lay.option,
    )


def pad_keepout_gap(name: str, option: str = "A") -> float:
    """Gap from the pad square to each keep-out circle plus 0.5, minimum."""
    u, s = get_layout(option).lead_pads[name]
    gaps = [
        math.hypot(u - c[0], s - c[1]) - KEEPOUT_R - COPPER_FREE - PAD_SIZE / 2.0
        for c in (CONTACT_1, CONTACT_2)
    ]
    return min(gaps)


def pad_in_antenna(name: str, option: str = "A") -> bool:
    u, s = get_layout(option).lead_pads[name]
    au0, au1, as0, as1 = antenna_rect(option)
    half = PAD_SIZE / 2.0
    return not (u + half < au0 or u - half > au1 or s + half < as0 or s - half > as1)


def clamp_distance(pad: str, option: str = "A") -> float:
    """Pad centre to the centre of the array that clamps it; inf if unplaced."""
    sites = placed_parts(option)
    name = LINE_ARRAY[pad]
    if name not in sites:
        return math.inf
    x, y, wu, ws = sites[name]
    pu, ps = get_layout(option).lead_pads[pad]
    return math.hypot(pu - (x + wu / 2.0), ps - (y + ws / 2.0))


def _segment_point_gap(a: tuple[float, float], b: tuple[float, float], p: tuple[float, float]) -> float:
    ax, ay = a
    bx, by = b
    px, py = p
    dx, dy = bx - ax, by - ay
    t = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
    t = min(1.0, max(0.0, t))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def wire_keepout_gap(option: str = "A") -> float:
    """Wire surface to the nearest signal keep-out circle, in (u, s)."""
    wire = get_layout(option).ref_wire
    return min(
        _segment_point_gap(a, b, c) - WIRE_OD / 2.0 - KEEPOUT_R
        for a, b in zip(wire, wire[1:])
        for c in (CONTACT_1, CONTACT_2)
    )


def wire_tab_gap(pad: str, samples: int = 400, option: str = "A") -> float:
    """Wire surface to a signal lug tab rectangle, sampled along the wire."""
    wire = get_layout(option).ref_wire
    best = math.inf
    for a, b in zip(wire, wire[1:]):
        for k in range(samples + 1):
            t = k / samples
            u = a[0] + t * (b[0] - a[0])
            s = a[1] + t * (b[1] - a[1])
            best = min(best, point_tab_gap(pad, u, s, option) - WIRE_OD / 2.0)
    return best


def _box_tab_gap(
    pad: str,
    box: tuple[float, float, float, float],
    option: str = "A",
    *,
    deg: float | None = None,
) -> float:
    """Smallest gap from a box to a tab rectangle; ≤ 0 when they touch."""
    x, y, wu, ws = box
    corners_box = [(x, y), (x + wu, y), (x + wu, y + ws), (x, y + ws)]
    if any(point_tab_gap(pad, cu, cs, option, deg=deg) == 0.0 for cu, cs in corners_box):
        return 0.0
    tab = tab_corners(pad, option, deg=deg)
    if any(x <= tu <= x + wu and y <= ts <= y + ws for tu, ts in tab):
        return 0.0
    gaps = []
    for i in range(4):
        a, b = tab[i], tab[(i + 1) % 4]
        for p in corners_box:
            gaps.append(_segment_point_gap(a, b, p))
        for j in range(4):
            gaps.append(_segment_point_gap(corners_box[j], corners_box[(j + 1) % 4], a))
    return min(gaps)


def tab_tab_gap(option: str = "A") -> float:
    """Smallest gap between the two signal barrels; 0 if they overlap."""
    a = tab_corners("SIG1", option)
    b = tab_corners("SIG2", option)
    if any(point_tab_gap("SIG2", u, s, option) == 0.0 for u, s in a):
        return 0.0
    if any(point_tab_gap("SIG1", u, s, option) == 0.0 for u, s in b):
        return 0.0
    gaps = []
    for i in range(4):
        p, q = a[i], a[(i + 1) % 4]
        for r in b:
            gaps.append(_segment_point_gap(p, q, r))
        p, q = b[i], b[(i + 1) % 4]
        for r in a:
            gaps.append(_segment_point_gap(p, q, r))
    return min(gaps)


def corner_pad_boxes(option: str = "A") -> list[tuple[float, float, float, float]]:
    lay = get_layout(option)
    zu0, zu1 = lay.board_zone_u
    zs0, zs1 = lay.board_zone_s
    return [
        (zu0, zs0, CORNER_PAD, CORNER_PAD),
        (zu1 - CORNER_PAD, zs0, CORNER_PAD, CORNER_PAD),
        (zu0, zs1 - CORNER_PAD, CORNER_PAD, CORNER_PAD),
        (zu1 - CORNER_PAD, zs1 - CORNER_PAD, CORNER_PAD, CORNER_PAD),
    ]


def tab_reasons(pad: str, deg: float, option: str = "A") -> list[str]:
    """Why a flat TE 31428 tab at ``deg`` fails (empty means the metal is legal)."""
    lay = get_layout(option)
    us = [c[0] for c in tab_corners(pad, option, deg=deg)]
    ss = [c[1] for c in tab_corners(pad, option, deg=deg)]
    out: list[str] = []
    if min(us) < lay.cavity_u[0] or max(us) > lay.cavity_u[1]:
        out.append(f"wall-u {min(us):.2f}–{max(us):.2f}")
    if min(ss) < lay.cavity_s[0] or max(ss) > lay.cavity_s[1]:
        out.append(f"wall-s {min(ss):.2f}–{max(ss):.2f}")
    if min(ss) < BATTERY_S[1]:
        out.append("battery")
    for name, _pad in lay.lead_pads.items():
        if name == pad:
            continue
        if _box_tab_gap(pad, pad_box(name, option), option, deg=deg) < COPPER_FREE:
            out.append(f"pad-{name}")
    for i, box in enumerate(corner_pad_boxes(option)):
        if _box_tab_gap(pad, box, option, deg=deg) <= 0.0:
            out.append(f"corner-{i}")
    return out


def legal_tab_degrees(
    pad: str, option: str = "A", step: float = TAB_SEARCH_STEP
) -> list[float]:
    """Angles (deg, 0 = +u, 90 = +s) where the flat barrel clears walls and pads."""
    out: list[float] = []
    deg = 0.0
    while deg < 360.0 - 1e-9:
        if not tab_reasons(pad, deg, option):
            out.append(deg)
        deg += step
    return out


def tab_tab_gap_at(d1: float, d2: float, option: str = "A") -> float:
    a = tab_corners("SIG1", option, deg=d1)
    b = tab_corners("SIG2", option, deg=d2)
    if any(point_tab_gap("SIG2", u, s, option, deg=d2) == 0.0 for u, s in a):
        return 0.0
    if any(point_tab_gap("SIG1", u, s, option, deg=d1) == 0.0 for u, s in b):
        return 0.0
    gaps = []
    for i in range(4):
        p, q = a[i], a[(i + 1) % 4]
        for r in b:
            gaps.append(_segment_point_gap(p, q, r))
        p, q = b[i], b[(i + 1) % 4]
        for r in a:
            gaps.append(_segment_point_gap(p, q, r))
    return min(gaps)


SEARCH_WIRE: dict[str, tuple[tuple[float, float], ...]] = {}


@functools.cache
def search_tab_degrees(
    option: str = "A", step: float = TAB_SEARCH_STEP
) -> dict[str, float]:
    """Pick a SIG1/SIG2 pair. Prefers all named parts placed, then more 0402s.

    Tries the low-u and high-u reference wires. Signal tabs stay flat:
    ``upright_signal_clear_mm`` is negative. Restores the layout on the way out.
    """
    lay = get_layout(option)
    saved_deg = dict(lay.tab_deg)
    saved_wire = lay.ref_wire
    sig1 = legal_tab_degrees("SIG1", option, step)
    sig2 = legal_tab_degrees("SIG2", option, step)
    wires = [("low", REF_WIRE_LOW_U), ("high", REF_WIRE_HIGH_U)]
    if get_layout(option).cavity_s[1] > CAVITY_S[1] + 1e-9:
        wires.append(("inferior", REF_WIRE_INFERIOR))
    best: tuple[tuple[int, int, int, float, float], float, float, str] | None = None
    try:
        for d1 in sig1:
            for d2 in sig2:
                if tab_tab_gap_at(d1, d2, option) < COPPER_FREE:
                    continue
                deg = {"SIG1": float(d1), "SIG2": float(d2)}
                for wname, wire in wires:
                    bind_layout(option, tab_deg=deg, ref_wire=wire)
                    if wire_keepout_gap(option) < 0:
                        continue
                    if wire_tab_gap("SIG1", option=option) < 0 or wire_tab_gap("SIG2", option=option) < 0:
                        continue
                    parts = placed_parts(option)
                    missing = sum(1 for name in PART_TARGETS if name not in parts)
                    n_ok = 1 if missing == 0 else 0
                    n_parts = len(parts)
                    n_0402 = len(place_0402s(option=option)) if n_ok else 0
                    score = (n_ok, n_parts, n_0402, -abs(d1), -abs(d2 - 180.0))
                    if best is None or score > best[0]:
                        best = (score, float(d1), float(d2), wname)
        if best is None:
            raise ValueError(f"no legal TE 31428 tab pair for option {option}")
        _score, d1, d2, wname = best
        SEARCH_WIRE[option.upper()] = {"low": REF_WIRE_LOW_U, "high": REF_WIRE_HIGH_U, "inferior": REF_WIRE_INFERIOR}[wname]
        return {"SIG1": d1, "SIG2": d2}
    finally:
        bind_layout(option, tab_deg=saved_deg, ref_wire=saved_wire)


def layout_conflicts(option: str = "A") -> list[str]:
    """Every rule the candidate layout breaks, as short sentences.

    Q14: plan §5's ≥ 5 mm is antenna-to-cell, not module body. The 4.70 mm
    module-body figure is reported in the budget, not as a packing fail.
    """
    out: list[str] = []
    lay = get_layout(option)
    b = budget(option)
    u, s, _uu, medial = board_free_mask(option=option)
    lateral = board_free_mask(option=option, punch_module=True)[3] if lay.two_sided else medial
    parts = placed_parts(option)
    faces = placed_faces(option)
    if b.clamp_pairs < N_LINES:
        out.append(f"{b.clamp_pairs} clamp pairs for {N_LINES} lines")
    for name in PART_TARGETS:
        if name not in parts:
            out.append(f"{name}: no legal site")
    if b.spare_named_mm2 < 0:
        out.append(f"named pack {b.required_named_mm2:.2f} mm² > free {b.free_mm2:.2f} mm²")
    for name, box in parts.items():
        free = lateral if faces.get(name) == "lateral" else medial
        if not _courtyard_in_free(free, u, s, *box, option):
            out.append(f"{name} courtyard outside the free mask")
    names = list(parts)
    for i, a in enumerate(names):
        for c in names[i + 1 :]:
            if faces.get(a) == faces.get(c) and _boxes_overlap(parts[a], parts[c]):
                out.append(f"{a} overlaps {c}")
        for pad in lay.lead_pads:
            if _boxes_overlap(parts[a], pad_box(pad, option)):
                out.append(f"{a} overlaps pad {pad}")
    for pad in lay.lead_pads:
        if pad_keepout_gap(pad, option) < 0:
            out.append(f"pad {pad} inside a keep-out + 0.5")
        if pad_in_antenna(pad, option):
            out.append(f"pad {pad} in the RF zone")
        for other in ("SIG1", "SIG2"):
            if other == pad:
                continue
            if _box_tab_gap(other, pad_box(pad, option), option) < COPPER_FREE:
                out.append(f"pad {pad} within 0.5 of the {other} lug tab")
        if LINE_ARRAY[pad] in parts and clamp_distance(pad, option) > CLAMP_MAX_MM:
            out.append(f"pad {pad} more than {CLAMP_MAX_MM:.0f} mm from its clamp")
    for pad in ("SIG1", "SIG2"):
        us = [c[0] for c in tab_corners(pad, option)]
        ss = [c[1] for c in tab_corners(pad, option)]
        if min(us) < lay.cavity_u[0] or max(us) > lay.cavity_u[1]:
            out.append(f"{pad} lug tab reaches a side wall (u {min(us):.2f}–{max(us):.2f})")
        if min(ss) < lay.cavity_s[0] or max(ss) > lay.cavity_s[1]:
            out.append(f"{pad} lug tab reaches an end wall (s {min(ss):.2f}–{max(ss):.2f})")
        if min(ss) < BATTERY_S[1]:
            out.append(f"{pad} lug tab enters the battery pocket")
        for i, box in enumerate(corner_pad_boxes(option)):
            if _box_tab_gap(pad, box, option) <= 0.0:
                out.append(f"{pad} lug tab hits corner pad {i}")
    if tab_tab_gap(option) < COPPER_FREE:
        out.append(f"signal lug tabs within 0.5 of each other ({tab_tab_gap(option):.2f})")
    if wire_keepout_gap(option) < 0:
        out.append(f"reference wire enters a keep-out ({wire_keepout_gap(option):.2f})")
    for pad in ("SIG1", "SIG2"):
        if wire_tab_gap(pad, option=option) < 0:
            out.append(f"reference wire crosses the {pad} lug tab")
    return out


def place_0402s(n: int = N_0402, option: str = "A") -> list[tuple[float, float, str]]:
    """Greedy 0402 courtyards. Option E fills medial then lateral."""
    lay = get_layout(option)
    u, s, _uu, medial = board_free_mask(option=option)
    faces_masks: list[tuple[str, np.ndarray, list[tuple[float, float, float, float]]]] = [
        ("medial", medial, list(placed_parts(option).values()) + [pad_box(p, option) for p in lay.lead_pads])
    ]
    if lay.two_sided:
        lat_taken = [pad_box(p, option) for p in lay.lead_pads]
        for name, box in placed_parts(option).items():
            if placed_faces(option).get(name) == "lateral":
                lat_taken.append(box)
        faces_masks.append(("lateral", board_free_mask(option=option, punch_module=True)[3], lat_taken))
    sites: list[tuple[float, float, str]] = []
    orients = (R0402_CY, (R0402_CY[1], R0402_CY[0]))
    for face, free, taken in faces_masks:
        if len(sites) >= n:
            break
        for r_w, r_h in orients:
            y = lay.board_s[0] + RIM
            y_end = lay.board_s[1] - RIM - r_h
            x_end = lay.board_u[1] - RIM - r_w
            while y <= y_end + 1e-9 and len(sites) < n:
                x = lay.board_u[0] + RIM
                while x <= x_end + 1e-9 and len(sites) < n:
                    box = (x, y, r_w, r_h)
                    if not any(_boxes_overlap(box, t) for t in taken) and _courtyard_in_free(
                        free, u, s, x, y, r_w, r_h, option
                    ):
                        sites.append((x, y, face))
                        taken.append(box)
                        x += r_w
                    else:
                        x += 0.10
                y += r_h
    return sites


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def _require_mpl() -> Any:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.patches import Circle, Rectangle

    except ImportError as exc:
        raise RuntimeError("matplotlib is not installed; pip install -e '.[cad]'") from exc
    matplotlib.rcParams.update(
        {
            "svg.hashsalt": "elicio-wp6-placement",
            "figure.dpi": 100,
            "savefig.dpi": 100,
            "font.family": "DejaVu Sans",
            "font.size": 7.0,
            "axes.linewidth": 0.5,
            "path.simplify": False,
            "svg.fonttype": "path",
            "text.hinting": "none",
        }
    )
    return plt, Circle, Rectangle


def render_svg(option: str = "A") -> bytes:
    plt, Circle, Rectangle = _require_mpl()
    lay = get_layout(option)
    b = budget(option)
    fig, ax = plt.subplots(figsize=(8.5, 11.0), facecolor="white")
    ax.set_aspect("equal")
    ax.set_xlim(-1.5, 32.0)
    ax.set_ylim(-1.0, max(50.0, lay.body_arc + 3.0))
    ax.set_xlabel("u (mm), posterior")
    ax.set_ylabel("s (mm), inferior up")
    ax.set_title(f"Elicio Stage B packing option {lay.option}  (u, s) body frame")

    def add_rect(u0, s0, du, ds, **kw):
        ax.add_patch(Rectangle((u0, s0), du, ds, **kw))

    add_rect(
        lay.body_u[0],
        0.0,
        lay.body_u[1] - lay.body_u[0],
        lay.body_arc,
        fill=False,
        edgecolor="0.3",
        linewidth=1.2,
        label="body",
    )
    add_rect(
        lay.cavity_u[0],
        lay.cavity_s[0],
        lay.cavity_u[1] - lay.cavity_u[0],
        lay.cavity_s[1] - lay.cavity_s[0],
        fill=False,
        edgecolor="0.15",
        linewidth=0.8,
        linestyle="--",
        label="cavity",
    )
    add_rect(
        BATTERY_U[0],
        BATTERY_S[0],
        BATTERY_U[1] - BATTERY_U[0],
        BATTERY_S[1] - BATTERY_S[0],
        facecolor="#f6e27f",
        edgecolor="#8a6d00",
        alpha=0.55,
        label="battery pocket",
    )
    add_rect(
        RIB_U[0],
        RIB_S[0],
        RIB_U[1] - RIB_U[0],
        RIB_S[1] - RIB_S[0],
        facecolor="#b07a4a",
        edgecolor="#5c3a1e",
        alpha=0.8,
        label="rib",
    )
    add_rect(
        lay.board_zone_u[0],
        lay.board_zone_s[0],
        lay.board_zone_u[1] - lay.board_zone_u[0],
        lay.board_zone_s[1] - lay.board_zone_s[0],
        fill=False,
        edgecolor="#1d4f91",
        linestyle=":",
        linewidth=0.7,
        label="BOARD_ZONE",
    )
    add_rect(
        lay.board_u[0],
        lay.board_s[0],
        lay.board_wid,
        lay.board_len,
        facecolor="#d9e8f6",
        edgecolor="#1d4f91",
        linewidth=1.0,
        alpha=0.9,
        label=f"board {lay.board_len:g}×{lay.board_wid:g}",
    )

    au0, au1, as0, as1 = antenna_rect(option)
    add_rect(
        au0,
        as0,
        au1 - au0,
        as1 - as0,
        facecolor="#7dce7d",
        edgecolor="#1a6b1a",
        alpha=0.45,
        hatch="///",
        label="RF no-copper 12.4×3.8",
    )
    mu0, mu1, ms0, ms1 = module_rect(MODULE_L_RESERVED, option)
    add_rect(
        mu0,
        ms0,
        mu1 - mu0,
        ms1 - ms0,
        fill=False,
        edgecolor="#0b3d0b",
        linewidth=0.9,
        linestyle="-.",
        label="module reserved 15.8 long",
    )

    for (uc, sc), name in ((CONTACT_1, "K1"), (CONTACT_2, "K2")):
        ax.add_patch(
            Circle(
                (uc, sc),
                KEEPOUT_R + COPPER_FREE,
                facecolor="#f4c1c1",
                edgecolor="#a33",
                alpha=0.45,
                linewidth=0.6,
                label="keep-out + 0.5" if name == "K1" else None,
            )
        )
        ax.add_patch(
            Circle(
                (uc, sc),
                KEEPOUT_R,
                facecolor="#e07070",
                edgecolor="#7a1010",
                alpha=0.4,
                hatch="xxx",
                label="KEEPOUT_SIGNAL Ø7.1" if name == "K1" else None,
            )
        )
        ax.plot(uc, sc, "k.", markersize=3)
        ax.text(uc + 0.2, sc + 0.2, name, fontsize=6, color="#5a0000")

    zu0, zu1 = lay.board_zone_u
    zs0, zs1 = lay.board_zone_s
    corners = [
        (zu0, zs0),
        (zu1 - CORNER_PAD, zs0),
        (zu0, zs1 - CORNER_PAD),
        (zu1 - CORNER_PAD, zs1 - CORNER_PAD),
    ]
    for i, (cu, cs) in enumerate(corners):
        add_rect(
            cu,
            cs,
            CORNER_PAD,
            CORNER_PAD,
            facecolor="#cfcfcf",
            edgecolor="#333",
            linewidth=0.5,
            label="corner pad 1.5×1.5" if i == 0 else None,
        )

    from matplotlib.patches import Polygon

    for i, pad in enumerate(("SIG1", "SIG2")):
        ax.add_patch(
            Polygon(
                tab_corners(pad, option),
                closed=True,
                facecolor="#e07070",
                edgecolor="#7a1010",
                alpha=0.35,
                hatch="\\\\",
                linewidth=0.5,
                label="TE 31428 barrel 1.96×6.27" if i == 0 else None,
            )
        )

    parts = placed_parts(option)
    faces = placed_faces(option)
    colors = {
        "ADS1292_RSM": "#6b4c9a",
        "BAV199S_1": "#c45c26",
        "BAV199S_2": "#c45c26",
        "BQ25100": "#2a6f97",
        "TLV713": "#2a6f97",
    }
    labels = {
        "ADS1292_RSM": "ADS1292 VQFN-32 4.60²",
        "BAV199S_1": "BAV199S-Q 2.65×2.35",
        "BAV199S_2": "BAV199S-Q 2.65×2.35",
        "BQ25100": "BQ25100 2.10×1.40",
        "TLV713": "TLV713 1.50²",
    }
    labels_done: set[str] = set()
    for name, (x, y, wu, ws) in parts.items():
        lab = labels[name]
        if faces.get(name) == "lateral":
            lab = lab + " lat"
        add_rect(
            x,
            y,
            wu,
            ws,
            facecolor=colors[name],
            edgecolor="black",
            alpha=0.55,
            linewidth=0.6,
            hatch=".." if faces.get(name) == "lateral" else None,
            label=lab if lab not in labels_done else None,
        )
        labels_done.add(lab)
        ax.text(x + 0.08, y + 0.12, name.replace("_", "\n"), fontsize=5, color="white")

    r_w, r_h = R0402_CY
    sites_0402 = place_0402s(option=option)
    for i, (x, y, face) in enumerate(sites_0402):
        add_rect(
            x,
            y,
            r_w,
            r_h,
            facecolor="#888",
            edgecolor="#222",
            linewidth=0.3,
            alpha=0.7,
            hatch="xx" if face == "lateral" else None,
            label="0402 courtyard 1.80×0.90" if i == 0 else None,
        )

    for name, (pu, ps) in lay.lead_pads.items():
        add_rect(
            pu - PAD_SIZE / 2.0,
            ps - PAD_SIZE / 2.0,
            PAD_SIZE,
            PAD_SIZE,
            facecolor="#111",
            edgecolor="#ffd24a",
            linewidth=0.7,
            label="lead pad 1.0×1.0" if name == "SIG1" else None,
        )
        ax.text(pu - 1.9, ps - 0.15, name, fontsize=6, color="#111")

    for pad in lay.lead_pads:
        arr = LINE_ARRAY[pad]
        if arr not in parts:
            continue
        x, y, wu, ws = parts[arr]
        cu, cs = x + wu / 2.0, y + ws / 2.0
        pu, ps = lay.lead_pads[pad]
        ax.plot([pu, cu], [ps, cs], color="#c45c26", linewidth=0.6, linestyle=":")
        ax.text(
            (pu + cu) / 2.0,
            (ps + cs) / 2.0,
            f"{clamp_distance(pad, option):.1f}",
            fontsize=5,
            color="#8a3b10",
        )

    ax.plot(
        [p[0] for p in lay.ref_wire],
        [p[1] for p in lay.ref_wire],
        color="#d4a017",
        linewidth=WIRE_OD * 2.2,
        solid_capstyle="round",
        label="ref wire Ø1.3",
    )
    ch_u = 0.5 * (CHANNEL_U[0] + CHANNEL_U[1])
    ax.plot(ch_u, WRAP_S, "s", color="#c9a227", markersize=6, label="Kapton wrap s 37")
    add_rect(
        CHANNEL_U[0],
        CHANNEL_S[0],
        CHANNEL_U[1] - CHANNEL_U[0],
        CHANNEL_S[1] - CHANNEL_S[0],
        fill=False,
        edgecolor="#d4a017",
        linewidth=0.8,
        label="WIRE_CHANNEL",
    )

    cell_hook = BATTERY_S[0] + CELL_BODY_MAX[2]
    ax.annotate(
        "",
        xy=(8.5, ms0),
        xytext=(8.5, cell_hook),
        arrowprops=dict(arrowstyle="<->", color="#8a6d00", lw=0.7),
    )
    ax.text(8.7, 0.5 * (ms0 + cell_hook), f"{b.battery_to_module_hook_mm:.1f} mm", fontsize=6, color="#8a6d00")

    conflicts = layout_conflicts(option)
    lines = [
        f"option {lay.option}  two-sided={lay.two_sided}",
        f"board {b.board_mm2:.1f} mm²  {lay.board_len:g}×{lay.board_wid:g}",
        f"keep-out 1 + 0.5   {b.keepout1_margin_mm2:.2f}",
        f"keep-out 2 ∪ RF    {b.keepout2_union_antenna_mm2:.2f}",
        f"TE 31428 tabs+0.5  {b.tabs_margin_mm2:.2f}",
        f"rim 0.25           {b.rim_mm2:.2f}",
        f"free (real lug)    {b.free_mm2:.2f}",
        f"  Q13 short        {b.free_tabs_to_pad_mm2:.2f}",
        f"  7 mm tabs        {b.free_literal_mm2:.2f}",
        f"  without tabs     {b.free_without_tabs_mm2:.2f}",
        f"  lateral (E)      {b.lateral_free_mm2:.2f}",
        f"SIG1 tab           {lay.tab_deg['SIG1']:.0f} deg (0=+u)",
        f"SIG2 tab           {lay.tab_deg['SIG2']:.0f} deg",
        f"upright SIG air    {upright_signal_clear_mm():.2f} (flat)",
        f"largest empty rect {b.largest_u:.2f} × {b.largest_s:.2f}",
        f"TQFP-32 7.60² fit? {b.tqfp_fits}",
        f"VQFN-32 4.60² fit? {b.vqfn_fits}",
        f"required named     {b.required_named_mm2:.2f}",
        f"spare named        {b.spare_named_mm2:.2f}",
        f"0402 placed        {b.n_0402} of {N_0402}",
        f"clamp pairs        {b.clamp_pairs} for {N_LINES} lines",
        f"BODY_ARC           {b.body_arc_mm:.1f}",
        f"TOTAL_CHORD        {b.total_chord_mm:.2f}",
        f"M1 gate (chord+3)  {b.m1_gate_mm:.2f}",
        f"sagitta            {b.sagitta_mm:.3f}",
        f"Y clear 4.3−4.13   {b.y_clear_mm:.2f}",
        f"cell→module 15.8 (hook) {b.battery_to_module_hook_mm:.2f}",
        f"cell→antenna zone (hook) {b.battery_to_antenna_hook_mm:.2f}",
        f"RF overlaps K2     {b.rf_keepout2_overlap}",
        "result: NOT confirmed" if conflicts else "result: no conflicts",
    ]
    lines += [f"✗ {c}" for c in conflicts]
    ax.text(
        lay.body_u[1] + 0.6,
        lay.body_arc - 0.9,
        "Packing at max courtyards\n" + "\n".join(lines),
        fontsize=5.6,
        family="DejaVu Sans",
        va="top",
        ha="left",
        wrap=False,
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor="0.4"),
    )
    ax.legend(loc="lower right", fontsize=5.5, framealpha=0.92)
    ax.grid(True, which="both", linestyle=":", linewidth=0.3, color="0.75")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(
        buf,
        format="svg",
        facecolor="white",
        metadata={"Creator": "elicio-wp6", "Title": f"elicio placement option {lay.option}"},
    )
    plt.close(fig)
    text = buf.getvalue().decode("utf-8")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"<metadata>.*?</metadata>", "", text, flags=re.S)
    text = re.sub(r"\s+$", "\n", text)
    return text.encode("utf-8")


def write_drawing(path: Path | None = None, option: str = "A") -> str:
    if path is None:
        path = drawing_path(option)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = render_svg(option)
    path.write_bytes(data)
    return sha256_bytes(data)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Draw a Stage B packing option.")
    parser.add_argument("--option", choices=OPTION_NAMES, default="A")
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args(argv)
    out = args.out if args.out is not None else drawing_path(args.option)
    digest = write_drawing(out, args.option)
    print(f"wrote {out} option={args.option} sha256={digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
