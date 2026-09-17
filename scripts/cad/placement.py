#!/usr/bin/env python3.13
"""Stage B board packing drawing (plan §5, interface v2).

2D drawing in the body-frame (u, s) plane. Headless matplotlib, Agg,
deterministic SVG. Does not edit CAD solids or ``manifest.json``.

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
    .venv/bin/python scripts/cad/placement.py --out docs/fab/cad/v1/placement.svg
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import io
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

HAS_MATPLOTLIB = importlib.util.find_spec("matplotlib") is not None

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "docs" / "fab" / "cad" / "v1" / "placement.svg"

# ---------------------------------------------------------------------------
# Geometry (millimetres). Every number used in the drawing has a From in
# interface.md §5–§8. Raster pitch is 0.025 mm.
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
KEEPOUT_TOP_Y = 4.13
BOARD_UNDERSIDE_Y = 4.3
PAD_Y = (1.5, 4.3)

# Courtyards at maximum dimensions (IPC-7351B Nominal unless named).
# SOT-23 / SOT-363 use the vendor reflow "occupied area".
VQFN_CY = (4.50, 4.50)  # 4.00 body + 2 × 0.25
TQFP_CY = (7.60, 7.60)  # 7.10 lead span max + 2 × 0.25
SOT23_CY = (3.30, 3.00)  # Nexperia BAV199 Fig. 9 occupied
ARRAY_CY = (2.65, 2.35)  # Nexperia BAV199S-Q Fig. 8 occupied
BQ_CY = (2.10, 1.40)  # 1.60 × 0.90 + 2 × 0.25
LDO_CY = (1.50, 1.50)  # TLV713 X2SON 1.00 × 1.00 + 2 × 0.25
R0402_CY = (1.80, 0.90)  # IPC-7351B small-chip Nominal
N_0402 = 25

# Frozen lead pads (interface v2). SIG1 moved +0.1 mm in s so a 1.0 × 1.0
# pad stays outside keep-out 1 plus 0.5 mm.
LEAD_PADS: dict[str, tuple[float, float]] = {
    "SIG1": (5.9, 26.6),
    "SIG2": (5.5, 30.0),
    "REF": (4.0, 29.0),
}

# Confirmed packing (named non-shell change: VQFN-32 and one BAV199S array).
# Lower-left corners in (u, s).
PLACED: dict[str, tuple[float, float, float, float]] = {
    "ADS1292_RSM": (10.00, 18.90, *VQFN_CY),
    "BAV199S": (4.20, 27.10, *ARRAY_CY),
    "BQ25100": (10.10, 23.50, *BQ_CY),
    "TLV713": (12.40, 23.50, *LDO_CY),
}


@dataclass(frozen=True, slots=True)
class Budget:
    board_mm2: float
    keepout1_mm2: float
    keepout1_margin_mm2: float
    keepout2_mm2: float
    keepout2_margin_mm2: float
    antenna_mm2: float
    keepout2_union_antenna_mm2: float
    rim_mm2: float
    blocked_mm2: float
    free_mm2: float
    largest_u: float
    largest_s: float
    largest_mm2: float
    tqfp_fits: bool
    vqfn_fits: bool
    required_as_drawn_mm2: float
    required_named_mm2: float
    spare_named_mm2: float
    sagitta_mm: float
    y_clear_mm: float
    battery_to_module_hook_mm: float
    battery_to_module_rib_mm: float
    rf_keepout2_overlap: bool


def _mesh() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    u0, u1 = BOARD_U
    s0, s1 = BOARD_S
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


def antenna_rect() -> tuple[float, float, float, float]:
    """Return (u0, u1, s0, s1) of the no-copper zone on the board."""
    u0, u1 = BOARD_U
    s1 = BOARD_S[1]
    s0 = s1 - ANTENNA_ALONG_S
    mid = 0.5 * (u0 + u1)
    half = ANTENNA_WID / 2.0
    return (max(u0, mid - half), min(u1, mid + half), s0, s1)


def module_rect() -> tuple[float, float, float, float]:
    """Nominal module on the board, antenna at the inferior edge."""
    u0, u1 = BOARD_U
    s1 = BOARD_S[1]
    s0 = s1 - MODULE_L
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


def board_free_mask() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    u, s, uu, ss = _mesh()
    free = np.ones(uu.shape, dtype=bool)
    free = _punch_circle(free, uu, ss, CONTACT_1[0], CONTACT_1[1], KEEPOUT_R + COPPER_FREE)
    free = _punch_circle(free, uu, ss, CONTACT_2[0], CONTACT_2[1], KEEPOUT_R + COPPER_FREE)
    au0, au1, as0, as1 = antenna_rect()
    free = _punch_rect(free, uu, ss, au0, au1, as0, as1)
    u0, u1 = BOARD_U
    s0, s1 = BOARD_S
    free = _punch_rect(free, uu, ss, u0, u0 + RIM, s0, s1)
    free = _punch_rect(free, uu, ss, u1 - RIM, u1, s0, s1)
    free = _punch_rect(free, uu, ss, u0, u1, s0, s0 + RIM)
    free = _punch_rect(free, uu, ss, u0, u1, s1 - RIM, s1)
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


def _fits_rect(free: np.ndarray, wu: float, ws: float) -> bool:
    du = RASTER_PITCH
    ku = int(round(wu / du))
    ks = int(round(ws / du))
    ns, nu = free.shape
    if ku < 1 or ks < 1 or ku > nu or ks > ns:
        return False
    img = free.astype(np.int32)
    cs = img.cumsum(0).cumsum(1)
    z = np.zeros((ns + 1, nu + 1), dtype=np.int32)
    z[1:, 1:] = cs
    need = ks * ku
    for r in range(ks, ns + 1):
        row = z[r]
        prev = z[r - ks]
        for c in range(ku, nu + 1):
            tot = row[c] - prev[c] - row[c - ku] + prev[c - ku]
            if tot == need:
                return True
    return False


def _courtyard_in_free(free: np.ndarray, u: np.ndarray, s: np.ndarray, x: float, y: float, wu: float, ws: float) -> bool:
    du = RASTER_PITCH
    i0 = int(round((x - BOARD_U[0]) / du))
    j0 = int(round((y - BOARD_S[0]) / du))
    i1 = int(round((x + wu - BOARD_U[0]) / du))
    j1 = int(round((y + ws - BOARD_S[0]) / du))
    i0 = max(0, i0)
    j0 = max(0, j0)
    i1 = min(free.shape[1], i1)
    j1 = min(free.shape[0], j1)
    if i1 <= i0 or j1 <= j0:
        return False
    return bool(free[j0:j1, i0:i1].all())


def budget() -> Budget:
    u, s, uu, free = board_free_mask()
    board = np.ones(free.shape, dtype=bool)
    _, _, uu, ss = _mesh()
    board = np.ones(uu.shape, dtype=bool)
    k1 = _punch_circle(board, uu, ss, CONTACT_1[0], CONTACT_1[1], KEEPOUT_R)
    k1m = _punch_circle(board, uu, ss, CONTACT_1[0], CONTACT_1[1], KEEPOUT_R + COPPER_FREE)
    k2 = _punch_circle(board, uu, ss, CONTACT_2[0], CONTACT_2[1], KEEPOUT_R)
    k2m = _punch_circle(board, uu, ss, CONTACT_2[0], CONTACT_2[1], KEEPOUT_R + COPPER_FREE)
    au0, au1, as0, as1 = antenna_rect()
    ant = _punch_rect(board, uu, ss, au0, au1, as0, as1)
    u0, u1 = BOARD_U
    s0, s1 = BOARD_S
    rim = _punch_rect(board, uu, ss, u0, u0 + RIM, s0, s1)
    rim = _punch_rect(rim, uu, ss, u1 - RIM, u1, s0, s1)
    rim = _punch_rect(rim, uu, ss, u0, u1, s0, s0 + RIM)
    rim = _punch_rect(rim, uu, ss, u0, u1, s1 - RIM, s1)
    board_mm2 = BOARD_LEN * BOARD_WID
    lu, ls, la = _largest_rect(free)
    vqfn = _fits_rect(free, VQFN_CY[0], VQFN_CY[1])
    tqfp = _fits_rect(free, TQFP_CY[0], TQFP_CY[1])
    as_drawn = TQFP_CY[0] * TQFP_CY[1] + 3 * SOT23_CY[0] * SOT23_CY[1] + BQ_CY[0] * BQ_CY[1] + LDO_CY[0] * LDO_CY[1] + N_0402 * R0402_CY[0] * R0402_CY[1]
    named = (
        VQFN_CY[0] * VQFN_CY[1]
        + ARRAY_CY[0] * ARRAY_CY[1]
        + BQ_CY[0] * BQ_CY[1]
        + LDO_CY[0] * LDO_CY[1]
        + N_0402 * R0402_CY[0] * R0402_CY[1]
    )
    free_mm2 = _area(free)
    mu0, mu1, ms0, ms1 = module_rect()
    cell_hook_end = BATTERY_S[0] + CELL_BODY_MAX[2]
    cell_rib_end = BATTERY_S[1]
    return Budget(
        board_mm2=board_mm2,
        keepout1_mm2=board_mm2 - _area(k1),
        keepout1_margin_mm2=board_mm2 - _area(k1m),
        keepout2_mm2=board_mm2 - _area(k2),
        keepout2_margin_mm2=board_mm2 - _area(k2m),
        antenna_mm2=board_mm2 - _area(ant),
        keepout2_union_antenna_mm2=board_mm2 - _area(k2m & ant),
        rim_mm2=board_mm2 - _area(rim),
        blocked_mm2=board_mm2 - free_mm2,
        free_mm2=free_mm2,
        largest_u=lu,
        largest_s=ls,
        largest_mm2=la,
        tqfp_fits=tqfp,
        vqfn_fits=vqfn,
        required_as_drawn_mm2=as_drawn,
        required_named_mm2=named,
        spare_named_mm2=free_mm2 - named,
        sagitta_mm=sagitta_mm(),
        y_clear_mm=BOARD_UNDERSIDE_Y - KEEPOUT_TOP_Y,
        battery_to_module_hook_mm=ms0 - cell_hook_end,
        battery_to_module_rib_mm=ms0 - cell_rib_end,
        rf_keepout2_overlap=as0 < CONTACT_2[1] + KEEPOUT_R,
    )


def pad_keepout_gap(name: str) -> float:
    u, s = LEAD_PADS[name]
    c = CONTACT_1 if name == "SIG1" else CONTACT_2 if name == "SIG2" else None
    if c is None:
        d1 = math.hypot(u - CONTACT_1[0], s - CONTACT_1[1]) - KEEPOUT_R - COPPER_FREE - PAD_SIZE / 2.0
        d2 = math.hypot(u - CONTACT_2[0], s - CONTACT_2[1]) - KEEPOUT_R - COPPER_FREE - PAD_SIZE / 2.0
        return min(d1, d2)
    return math.hypot(u - c[0], s - c[1]) - KEEPOUT_R - COPPER_FREE - PAD_SIZE / 2.0


def pad_in_antenna(name: str) -> bool:
    u, s = LEAD_PADS[name]
    au0, au1, as0, as1 = antenna_rect()
    half = PAD_SIZE / 2.0
    return not (u + half < au0 or u - half > au1 or s + half < as0 or s - half > as1)


def clamp_distance(pad: str, part: str = "BAV199S") -> float:
    pu, ps = LEAD_PADS[pad]
    x, y, wu, ws = PLACED[part]
    cu, cs = x + wu / 2.0, y + ws / 2.0
    return math.hypot(pu - cu, ps - cs)


def _boxes_overlap(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> bool:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return not (ax + aw <= bx or bx + bw <= ax or ay + ah <= by or by + bh <= ay)


def occupied_boxes() -> list[tuple[float, float, float, float]]:
    boxes = list(PLACED.values())
    for pu, ps in LEAD_PADS.values():
        boxes.append((pu - PAD_SIZE / 2.0, ps - PAD_SIZE / 2.0, PAD_SIZE, PAD_SIZE))
    return boxes


def place_0402s(n: int = N_0402) -> list[tuple[float, float]]:
    """Greedy 0402 courtyards in the free mask, away from ICs and pads."""
    u, s, _uu, free = board_free_mask()
    taken = occupied_boxes()
    sites: list[tuple[float, float]] = []
    r_w, r_h = R0402_CY
    y = BOARD_S[0] + RIM
    y_end = BOARD_S[1] - RIM - r_h
    x_end = BOARD_U[1] - RIM - r_w
    while y <= y_end + 1e-9 and len(sites) < n:
        x = BOARD_U[0] + RIM
        while x <= x_end + 1e-9 and len(sites) < n:
            box = (x, y, r_w, r_h)
            if not any(_boxes_overlap(box, t) for t in taken) and _courtyard_in_free(
                free, u, s, x, y, r_w, r_h
            ):
                sites.append((x, y))
                taken.append(box)
                x += r_w
            else:
                x += 0.10
        y += r_h
    if len(sites) < n:
        # One or two 0402 on the lateral face over the VQFN courtyard
        # (two-sided; VQFN is medial ≤ 1.2 mm; 0402 body ~0.50 mm; the
        # module starts at s 22.1 so the superior end of that courtyard
        # is free of the module).
        x0, y0, wu, ws = PLACED["ADS1292_RSM"]
        for xx, yy in ((x0 + 0.10, y0 + 0.10), (x0 + 0.10 + r_w, y0 + 0.10)):
            if len(sites) >= n:
                break
            sites.append((xx, yy))
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


def render_svg() -> bytes:
    plt, Circle, Rectangle = _require_mpl()
    b = budget()
    fig, ax = plt.subplots(figsize=(8.5, 11.0), facecolor="white")
    ax.set_aspect("equal")
    ax.set_xlim(-1.5, 28.0)
    ax.set_ylim(-1.0, 50.0)
    ax.set_xlabel("u (mm), posterior")
    ax.set_ylabel("s (mm), inferior up")
    ax.set_title("Elicio Stage B placement at maximum courtyards  (u, s) body frame")

    def add_rect(u0, s0, du, ds, **kw):
        ax.add_patch(Rectangle((u0, s0), du, ds, **kw))

    # cavity walls / body
    add_rect(BODY_U[0], 0.0, BODY_U[1] - BODY_U[0], 48.4, fill=False, edgecolor="0.3", linewidth=1.2, label="body")
    add_rect(
        CAVITY_U[0],
        CAVITY_S[0],
        CAVITY_U[1] - CAVITY_U[0],
        CAVITY_S[1] - CAVITY_S[0],
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
        BOARD_ZONE_U[0],
        BOARD_ZONE_S[0],
        BOARD_ZONE_U[1] - BOARD_ZONE_U[0],
        BOARD_ZONE_S[1] - BOARD_ZONE_S[0],
        fill=False,
        edgecolor="#1d4f91",
        linestyle=":",
        linewidth=0.7,
        label="BOARD_ZONE",
    )
    add_rect(
        BOARD_U[0],
        BOARD_S[0],
        BOARD_WID,
        BOARD_LEN,
        facecolor="#d9e8f6",
        edgecolor="#1d4f91",
        linewidth=1.0,
        alpha=0.9,
        label="board 19×12.5",
    )

    au0, au1, as0, as1 = antenna_rect()
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
    mu0, mu1, ms0, ms1 = module_rect()
    add_rect(
        mu0,
        ms0,
        mu1 - mu0,
        ms1 - ms0,
        fill=False,
        edgecolor="#0b3d0b",
        linewidth=0.9,
        linestyle="-.",
        label="module 15.5×10.5",
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

    # corner nylon pads at BOARD_ZONE corners (interface v1, unchanged)
    corners = [
        (1.5, 18.3),
        (14.0, 18.3),
        (1.5, 36.4),
        (14.0, 36.4),
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

    colors = {
        "ADS1292_RSM": "#6b4c9a",
        "BAV199S": "#c45c26",
        "BQ25100": "#2a6f97",
        "TLV713": "#2a6f97",
    }
    labels_done: set[str] = set()
    for name, (x, y, wu, ws) in PLACED.items():
        key = name.split("_")[0]
        lab = {
            "ADS1292": "ADS1292 VQFN-32 4.50²",
            "BAV199S": "BAV199S SOT-363 2.65×2.35",
            "BQ25100": "BQ25100 2.10×1.40",
            "TLV713": "TLV713 1.50²",
        }[key]
        add_rect(
            x,
            y,
            wu,
            ws,
            facecolor=colors[name],
            edgecolor="black",
            alpha=0.55,
            linewidth=0.6,
            label=lab if lab not in labels_done else None,
        )
        labels_done.add(lab)
        ax.text(x + 0.08, y + 0.12, name.replace("_", "\n"), fontsize=5, color="white")

    # 25 × 0402 at IPC-7351 small-chip Nominal courtyards.
    # Sites on the VQFN courtyard are two-sided (lateral, over the AFE).
    r_w, r_h = R0402_CY
    vqfn = PLACED["ADS1292_RSM"]
    for i, (x, y) in enumerate(place_0402s()):
        two_sided = _boxes_overlap((x, y, r_w, r_h), vqfn)
        add_rect(
            x,
            y,
            r_w,
            r_h,
            facecolor="#8a6d9a" if two_sided else "#888",
            edgecolor="#222",
            linewidth=0.3,
            alpha=0.7,
            hatch=".." if two_sided else None,
            label="0402 courtyard 1.80×0.90" if i == 0 else ("0402 two-sided" if two_sided and i == 24 else None),
        )

    for name, (pu, ps) in LEAD_PADS.items():
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
        ax.text(pu + 0.55, ps - 0.15, name, fontsize=6, color="#111")

    x, y, wu, ws = PLACED["BAV199S"]
    cu, cs = x + wu / 2.0, y + ws / 2.0
    for pad in LEAD_PADS:
        pu, ps = LEAD_PADS[pad]
        ax.plot([pu, cu], [ps, cs], color="#c45c26", linewidth=0.6, linestyle=":")
        d = math.hypot(pu - cu, ps - cs)
        ax.text((pu + cu) / 2.0, (ps + cs) / 2.0, f"{d:.1f}", fontsize=5, color="#8a3b10")

    # reference wire: pocket → channel → wrap at s 37 → pad, Ø1.3, bend 3 mm
    ch_u = 0.5 * (CHANNEL_U[0] + CHANNEL_U[1])
    path_u = [ch_u, ch_u, ch_u, 4.0]
    path_s = [CHANNEL_S[1], CHANNEL_S[0], WRAP_S, LEAD_PADS["REF"][1]]
    ax.plot(path_u, path_s, color="#d4a017", linewidth=WIRE_OD * 2.2, solid_capstyle="round", label="ref wire Ø1.3")
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
    bend = Circle((ch_u, WRAP_S), BEND_R, fill=False, edgecolor="#d4a017", linestyle=":", linewidth=0.5)
    ax.add_patch(bend)

    # 5 mm battery–module marker
    ax.annotate(
        "",
        xy=(8.5, ms0),
        xytext=(8.5, cell_hook := BATTERY_S[0] + CELL_BODY_MAX[2]),
        arrowprops=dict(arrowstyle="<->", color="#8a6d00", lw=0.7),
    )
    ax.text(8.7, 0.5 * (ms0 + cell_hook), f"{b.battery_to_module_hook_mm:.1f} mm", fontsize=6, color="#8a6d00")

    # numbers box
    lines = [
        f"board {b.board_mm2:.1f} mm²",
        f"keep-out 1 + 0.5   {b.keepout1_margin_mm2:.2f}",
        f"keep-out 2 ∪ RF    {b.keepout2_union_antenna_mm2:.2f}",
        f"rim 0.25           {b.rim_mm2:.2f}",
        f"free               {b.free_mm2:.2f}",
        f"largest empty rect {b.largest_u:.2f} × {b.largest_s:.2f}",
        f"TQFP-32 7.60² fit? {b.tqfp_fits}",
        f"VQFN-32 4.50² fit? {b.vqfn_fits}",
        f"required named     {b.required_named_mm2:.2f}",
        f"spare named        {b.spare_named_mm2:.2f}",
        f"sagitta 19 mm chord {b.sagitta_mm:.3f}",
        f"Y clear 4.3−4.13   {b.y_clear_mm:.2f}",
        f"cell→module (hook) {b.battery_to_module_hook_mm:.2f}",
        f"cell→module (rib)  {b.battery_to_module_rib_mm:.2f}",
        f"RF overlaps K2     {b.rf_keepout2_overlap}",
        "result: VQFN-32 + BAV199S; no shell change",
    ]
    ax.text(
        17.6,
        47.5,
        "Packing at max courtyards\n" + "\n".join(lines),
        fontsize=6.5,
        family="DejaVu Sans",
        va="top",
        ha="left",
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
        metadata={"Creator": "elicio-wp6", "Title": "elicio placement v1"},
    )
    plt.close(fig)
    text = buf.getvalue().decode("utf-8")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"<metadata>.*?</metadata>", "", text, flags=re.S)
    text = re.sub(r"\s+$", "\n", text)
    return text.encode("utf-8")


def write_drawing(path: Path = DEFAULT_OUT) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = render_svg()
    path.write_bytes(data)
    return sha256_bytes(data)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Draw the Stage B packing figure.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args(argv)
    digest = write_drawing(args.out)
    print(f"wrote {args.out} sha256={digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
