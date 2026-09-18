#!/usr/bin/env python3.13
"""BTE fit-gauge generator (plan §3).

Build a nylon Stage-B shell from caliper numbers. Defaults are the
reference-ear build. Override any parameter from a TOML or JSON file,
from ``--set KEY=VALUE``, or from ``--variant`` / ``--preload`` /
``--side``.

Manifest schema (WP3 may extend this file; keep these keys):

``schema`` (int)
    This writer uses 1.
``commit`` (str)
    Last git commit that changed a hashed solid under ``docs/fab/cad/v1``
    (``*.step``, ``*.stl``, ``*.3mf``). It is not ``HEAD``. Artwork under
    ``views`` does not move this field. ``unknown`` if git is missing.
``parameters`` (object)
    The full parameter set after derivation and clamp.
``defaults_used`` (list of str)
    Keys that still hold the reference-ear default.
``ref_build`` (bool)
    True when any of M1–M8 used a default.
``crease_bow`` (object)
    ``source``, ``requested``, ``computed_from_m1_m2`` (always reported),
    ``clamped`` (always 1–8; the value the build used).
``chord_gate`` (object)
    ``total_chord``, ``gate`` (TOTAL_CHORD + 3), ``m1``.
``wire_channel`` (object)
    Body-frame opening at u=9.3 for the clamped bow, plus the table at
    bows 1, 3 and 8. Distances are millimetres along the offset path.
``exceptions`` (object)
    E1–E5 names, sizes, minima.
``fits`` (list)
    The §3.6 lid:body pairs with nominal and adverse values.
``interference`` (object)
    CAD overlap volume of the seated lid and body, mm^3.
``span`` (object)
    Per body: BODY_THICK + dome crown versus M3.
``walls`` (object)
    Each enclosing wall from the geometry; all ≥ 1.0.
``contact_stack`` (object)
    Reserved stack at nominal wall and at wall +0.3 (MJF tolerance).
``keepout_clearance`` (object)
    Body-frame gap from each KEEPOUT_SIGNAL Ø7.1 to the pads, rib, walls.
``checks`` (list)
    Each check name, pass/fail, and the numbers used. The export stops on
    the first failure, so an order 1 manifest lists passes only. A Stage B
    manifest can list Q21_REF_lug failing; ``stage_b_passed`` says so.
``files`` (object)
    Relative file name → ``{sha256, bytes}`` for the fifteen solids.
``views`` (object, optional)
    ``render_medial.png``, ``render_lateral.png``, ``drawing.pdf`` each
    ``{sha256, bytes}``. Written by ``render.py``. Solids export keeps
    this map if it is already present.
``quantities`` (object)
    Order-1 counts: three bodies ×1, lid ×2, coupon ×1.
``hash_rule``
    SHA-256 of raw file bytes. STEP timestamp is pinned to
    ``2026-09-16T00:00:00Z``. STL/3MF mesh: chord 0.02 mm, angle 5°.
    3MF UUIDs are UUID5 in the URL namespace with name
    ``elicio:cad:v1:<part>``.

Coupon-to-parameter mapping (plan §10 open item 2; interface §12 V2-2).
Coupon axes as in ``build_coupon``: x and y across the top face from its
centre; the rib stands on the top face.

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
"""
from __future__ import annotations

import argparse
import functools
import hashlib
import importlib.util
import json
import math
import subprocess
import sys
import tomllib
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Mapping

try:
    from build123d import (
        Axis,
        Box,
        Circle,
        Compound,
        Ellipse,
        Face,
        GeomType,
        Location,
        Mesher,
        Plane,
        Pos,
        PrecisionMode,
        Rectangle,
        RegularPolygon,
        Shape,
        Solid,
        Sphere,
        Text,
        Vector,
        export_step,
        export_stl,
        extrude,
        fillet,
        loft,
        revolve,
    )

    HAS_BUILD123D = True
except ImportError:  # pragma: no cover - exercised by skip in tests
    HAS_BUILD123D = False

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
DEFAULT_PARAMS_PATH = SCRIPT_DIR / "params" / "default.toml"
FONT_PATH = SCRIPT_DIR / "fonts" / "LiberationSans-Regular.ttf"
STEP_TIMESTAMP = "2026-09-16T00:00:00Z"
MESH_CHORD = 0.02
MESH_ANGLE_RAD = math.radians(5.0)
UUID_NAMESPACE = uuid.NAMESPACE_URL
MATRIX_VARIANTS = frozenset({"full", "thin"})
MATRIX_PRELOADS = frozenset({1.5, 2.5})
VARIANT_THICK = {"full": 9.0, "thin": 7.0}
CREASE_BOW_MIN = 1.0
CREASE_BOW_MAX = 8.0
CONTACT_DOME_DIA = 4.7
CONTACT_DOME_CROWN = 1.35
CONTACT_HOLE = 2.9
CONTACT_1 = (5.9, 22.0)
CONTACT_PITCH = 12.0
PAIR_ANGLE_DEG = 22.0
CONTACT_REF = (8.5, 43.0)
POCKET_DIA = 7.5
WIRE_U = (7.7, 9.3)
WIRE_Y = (2.5, 4.1)
WIRE_S = (38.2, 40.5)
CAVITY_S = (1.5, 38.2)
CAVITY_U = (1.5, 15.5)
BATTERY_U = (3.1, 13.9)
BATTERY_S = (1.5, 17.5)
BATTERY_Y = (1.5, 7.5)
RIB_S = (17.5, 18.3)
RIB_Y = (1.5, 4.5)
BOARD_S = (18.3, 37.9)
PAD_SIZE = 1.5
PAD_Y = (1.5, 4.3)
TAIL_S0 = 38.2
LID_RECESS_S1 = 46.8
TAIL_TIP_WIDTH = 10.0
TIP_ROUND = 4.0
LIP_U = (8.0, 14.0)
LIP_S = (-1.2, -0.2)
LIP_LENGTH = 5.5
BUMP_OUT = 0.5
BUMP_TALL = 0.6
GROOVE_S = (0.0, 0.5)
GROOVE_U = (7.5, 14.5)
GROOVE_Y_OFF = (-4.7, -3.7)
TONGUE_SLOT_S = (46.8, 48.4)
TONGUE_SLOT_U = (5.0, 12.0)
TONGUE_SLOT_Y_OFF = (-1.0, -0.1)
WEB_POCKET_S = (45.4, 46.8)
WEB_POCKET_Y_OFF = (-1.2, 0.0)
LID_PLATE_S = (-0.2, 46.4)
LID_TONGUE_S = (46.4, 48.0)
LID_WEB_S = (45.6, 46.4)
LID_TONGUE_WIDTH = 6.0
NUB = 0.8
NUB_S = (17.5, 18.3)
NUB_U = ((1.9, 2.7), (14.3, 15.1))
CABLE_EXIT_S = 36.0
CABLE_EXIT_Y = 3.0
CABLE_EXIT_DIA = 2.0
HOOK_EMBED_DEG = -5.0
GLASSES_FLAT_DEPTH = 0.8
GLASSES_FLAT_ANGLES = (30.0, 120.0)
JOINT_FILLET = 2.0
HOOK_CLEARANCE = 0.75
LIP_ROOT_FILLET = 0.2  # plan §3.5 step 7 says 0.5; see the lip root note
EMBOSS = 0.8
COUPON_XY = 12.0
COUPON_Z = 3.0
ORDER_PARTS = (
    "body_full_p15",
    "body_thin_p15",
    "body_full_p25",
    "lid",
    "coupon",
)
QUANTITIES = {
    "body_full_p15": 1,
    "body_thin_p15": 1,
    "body_full_p25": 1,
    "lid": 2,
    "coupon": 1,
}

REFERENCE_M_KEYS = ("M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8")
# Keys an overlay may change. Everything else in default.toml is fixed for
# this release: the feature constants above assume those values, and plan
# §3.3 says anything outside the matrix fails before export.
OVERRIDABLE_KEYS = frozenset(
    {
        "SIDE",
        "VARIANT",
        "HOOK_PRELOAD",
        "CREASE_BOW",
        "HOOK_RADIUS",
        "PACKING",
        "MOCK_CONTACTS",
        "CLOSURE_PASSED",
        "TAB_HEIGHT",
        "CONTACT_1_U",
        "CONTACT_1_S",
        "CONTACT_REF_U",
        "CONTACT_REF_S",
        "CABLE_EXIT_S",
        "CONTACT_SOURCE",
        "V2_ARCH",
        "V2_CELL",
        "V2_LAYOUT",
        "V2_WIDTH",
        "V2_LID_Y",
        "V2_ARC_PLUS",
        "V2_IFACE",
        "V2_STANDOFF",
        "V2_RECESS",
        "STAGE",
        *REFERENCE_M_KEYS,
    }
)
STAGE_B_ONLY_KEYS = frozenset(
    {
        "PACKING",
        "CLOSURE_PASSED",
        "TAB_HEIGHT",
        "CONTACT_1_U",
        "CONTACT_1_S",
        "CONTACT_REF_U",
        "CONTACT_REF_S",
        "CABLE_EXIT_S",
        "CONTACT_SOURCE",
        "V2_ARCH",
        "V2_CELL",
        "V2_LAYOUT",
        "V2_WIDTH",
        "V2_LID_Y",
        "V2_ARC_PLUS",
        "V2_IFACE",
        "V2_STANDOFF",
        "V2_RECESS",
        "STAGE",
        "TAIL_DS",
        "TAIL_S0",
        "CAVITY_U",
        "CAVITY_S",
        "BOARD_ZONE_U",
        "BOARD_ZONE_S",
        "LEAD_PADS",
        "TAB_DEG",
        "WIRE_S",
        "NUB_U",
    }
)
# Keys an overlay may set only with MOCK_CONTACTS = false. On order 1 they
# fail: derived_params drops them, so the gauge would build the plan value.
STAGE_B_OVERLAY_KEYS = frozenset(
    {
        "PACKING",
        "CLOSURE_PASSED",
        "TAB_HEIGHT",
        "CONTACT_1_U",
        "CONTACT_1_S",
        "CONTACT_REF_U",
        "CONTACT_REF_S",
        "CABLE_EXIT_S",
        "CONTACT_SOURCE",
        "V2_ARCH",
        "V2_CELL",
        "V2_LAYOUT",
        "V2_WIDTH",
        "V2_LID_Y",
        "V2_ARC_PLUS",
        "V2_IFACE",
        "V2_STANDOFF",
        "V2_RECESS",
        "STAGE",
    }
)
PLACEMENT_CONTACT_TOL = 0.05  # placement.py rounds CONTACT_2 to (10.4, 33.1)
PACKING_OPTIONS = frozenset({"A", "B", "C", "v2", "V2"})
STAGE_B_CHECK_NAMES = frozenset(
    {
        "CONTACT_HOLE_wall",
        "KEEPOUT_SIGNAL_air",
        "KEEPOUT_REF_air",
        "TAB_envelope_air",
        "BOARD_underside_clear",
        "REF_WIRE_envelope",
        "CABLE_EXIT_cavity",
        "CELL_envelope",
        "Q21_REF_lug",
        "CLOSURE_PASSED",
    }
)
V1_DIR = REPO_ROOT / "docs" / "fab" / "cad" / "v1"
V2_DIR = REPO_ROOT / "docs" / "fab" / "cad" / "v2"
TAB_HEIGHT_DEFAULT = 2.0  # Q22; plan §3.3 wrote 1.5
BARREL_HEIGHT = 1.96  # TE 31428; board check quotes 3.46 = 1.5 + 1.96
CELL_MAX = (5.2, 10.4, 15.6)  # y, u, s; plan §5
FOAM_THICK = 0.5
STAGE_B_NONFATAL = frozenset({"Q21_REF_lug"})  # recorded, build still writes (Q21)
# Order 2 is two bodies and two lids (plan §7); preload is Rolf's after 3.7,
# thin cannot hold the cell (LID_Y 6.0), the coupon is order 1's.
STAGE_B_PARTS = ("body_full_p15", "body_full_p25", "lid")
ENVELOPE_LIFT = 1e-3  # reserved-air solids start this far above the floor face
HOLE_VOLUME_TOL = 0.02  # removed hole volume within 2 % of the wall disc
BAND_NOISE_MM3 = 0.01
ROUTE_STRAIGHT_DEG = 3.0
STAGE_B_EMBOSS = 0.4  # Q11; gauge keeps 0.8
STAGE_B_EMBOSS_S = 10.0  # battery zone, not over the module
SHELL_PARTS = ("body_full_p15", "lid")
SHELL_WINNER = "A_501015_series_w20_y8_iII_s3"
SHELL_PARAMS_FILE = SCRIPT_DIR / "params" / "shell_v2.toml"
# ISO 7380 M2.5×4 head (v1 contact dome stays the skin seat).
ISO_7380_HEAD_D = 4.6
ISO_7380_HEAD_H = 1.5
# Captive hex well for the 5 AF brass standoff (review r6). Inputs: the
# standoff is 5.00 A/F max (Harwin DRG-01991; the Spacer Express 3.0 part
# is sold as "5 mm across flats"); JLC PA12-HP "Tolerance: ±0.3mm (Within
# 100mm)" (jlc3dp.com/help/article/pa12-hp-nylon, plan v2 §12 C15).
# Fit: the smallest printed well (AF − 0.3) must take the largest standoff,
# AF − 0.3 ≥ 5.00, so AF ≥ 5.30. Lock: the largest printed well (AF + 0.3)
# must stay under the standoff's across-corners, 5.60 < 1.1547 × AF_standoff,
# which holds for any standoff at or above 4.85 AF. 5.30 is the one value
# that satisfies both at every print tolerance.
STANDOFF_AF = 5.00
PRINT_TOL = 0.30
SHELL_HEX_AF = STANDOFF_AF + PRINT_TOL  # 5.30
# Collar: JLC's 1.0 minimum wall around the Ø6.4 ring seat at its base.
SHELL_HEX_OUTER_AF = 8.4
SHELL_COLLAR_H = 2.0
# Ring seat at the collar base: the flex ring outline is Ø6.0 (cap radius
# 3.0 around the Ø5.0 pad, board-v2.md §11), FPC outline ±0.10
# (board-v2.md §12) plus the print ±0.3: Ø6.4.
SHELL_RING_SEAT_D = 6.0 + 0.10 + PRINT_TOL
SHELL_SCREW_HOLE = 2.7  # brief; Stage B already opens CONTACT_HOLE 2.9
JLC_MIN_WALL = 1.0  # JLC PA12-HP "Wall thickness: 1mm" (plan v2 §12)
SHELL_PILOT = 2.0  # M2.5 self-tap in PA12 (~80 % of 2.5)
# Cantilever snap (PA12). Strain ε ≈ 1.5 t y / L².
SHELL_SNAP_L = 8.0
SHELL_SNAP_T = 1.0
SHELL_SNAP_W = 4.0
SHELL_SNAP_Y = 0.5  # deflection / catch
SHELL_SNAP_CATCH = 0.4  # into the 1.5 side wall; residual 1.1
SHELL_SNAP_S0 = 28.0
# Elliptical hook half-axes (root then tip), millimetres.
SHELL_HOOK_ROOT = (2.20, 1.50)  # 4.4 × 3.0
SHELL_HOOK_TIP = (1.50, 1.10)  # 3.0 × 2.2
SHELL_HOOK_BLEND = 1.5
SHELL_LID_CROWN = 0.5
SHELL_SWITCH_RECESS = 0.5
SHELL_USB_CORNER_R = 0.6
# packing-v2.md §5 on lane/w3 at 284ec05, table REF_end_wall_slot.
# Cavity ends at s 38.20; Ø7.5 tail pocket starts at s 39.25; 1.05 mm of
# nylon between them. Every REF route crosses that wall (Q59).
REF_SLOT_U = (7.25, 9.75)
REF_SLOT_S = (38.20, 39.25)
REF_SLOT_Y = (1.50, 1.81)
REF_SLOT_PACK_VOL = 0.814
# Flex 2.50 × 0.31 in that box. JLC PA12 ±0.3 under 100 mm; FPC outline
# ±0.10 (board-v2.md §12). Clearance is extra on the packing box, not a
# substitute for it. Floor y=1.50 is not cut.
REF_SLOT_CLEAR_U = 0.20  # per side
REF_SLOT_CLEAR_S = 0.20  # into the cavity and the pocket
REF_SLOT_CLEAR_Y = 0.15  # above the 0.31 tab


class CheckFail(Exception):
    """A named check failed. The message includes the parameter and number."""


@dataclass(frozen=True, slots=True)
class PathGeom:
    body_arc: float
    crease_bow: float
    chord: float
    radius: float
    a0: float
    cx: float
    cz: float

    @property
    def center_xz(self) -> tuple[float, float]:
        return self.cx, self.cz


@dataclass
class Check:
    name: str
    passed: bool
    detail: str
    numbers: dict[str, float] = field(default_factory=dict)


def chord_from_arc_bow(arc: float, bow: float) -> tuple[float, float]:
    """Return (chord, radius) for arc length and sagitta, millimetres."""
    if bow <= 0.0:
        raise CheckFail(f"CREASE_BOW={bow}: bow must be positive")
    if arc <= 0.0:
        raise CheckFail(f"BODY_ARC={arc}: arc must be positive")
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


def bow_from_arc_chord(arc: float, chord: float) -> float:
    """Return sagitta for a circular arc given arc length and chord."""
    if arc <= chord:
        return 0.0
    lo, hi = 1e-9, max(chord, arc - chord)
    for _ in range(80):
        bow = (lo + hi) / 2.0
        radius = chord * chord / (8.0 * bow) + bow / 2.0
        length = 4.0 * radius * math.atan(2.0 * bow / chord)
        if length < arc:
            lo = bow
        else:
            hi = bow
    return (lo + hi) / 2.0


def clamp_crease_bow(value: float) -> float:
    return min(CREASE_BOW_MAX, max(CREASE_BOW_MIN, value))


def make_path(body_arc: float, crease_bow: float) -> PathGeom:
    chord, radius = chord_from_arc_bow(body_arc, crease_bow)
    a0 = math.asin(min(1.0, chord / (2.0 * radius)))
    return PathGeom(
        body_arc=body_arc,
        crease_bow=crease_bow,
        chord=chord,
        radius=radius,
        a0=a0,
        cx=crease_bow - radius,
        cz=-chord / 2.0,
    )


def angle_at(path: PathGeom, s: float) -> float:
    return path.a0 - s / path.radius


def p_xyz(path: PathGeom, u: float, s: float, y: float) -> tuple[float, float, float]:
    a = angle_at(path, s)
    return (
        path.cx + (path.radius + u) * math.cos(a),
        y,
        path.cz + (path.radius + u) * math.sin(a),
    )


def contact_2_us(origin: tuple[float, float] | None = None) -> tuple[float, float]:
    """CONTACT_2 = CONTACT_1 + pitch × (sin, +cos) of PAIR_ANGLE."""
    u0, s0 = origin if origin is not None else CONTACT_1
    rad = math.radians(PAIR_ANGLE_DEG)
    u = u0 + CONTACT_PITCH * math.sin(rad)
    s = s0 + CONTACT_PITCH * math.cos(rad)
    return u, s


def wire_channel_opening(
    radius: float,
    u: float = WIRE_U[1],
    s_end: float = WIRE_S[1],
    u_center: float = CONTACT_REF[0],
    s_center: float = CONTACT_REF[1],
    pocket_radius: float = POCKET_DIA / 2.0,
) -> dict[str, float]:
    """Body-frame circle entry and physical opening along the offset path.

    Finding 23 / open item 4. ``d² = (R+u)²+(R+u_c)² − 2(R+u)(R+u_c)
    cos((s_c−s)/R)``. Physical distance is ``(1 + u/R) × (s_end − s_entry)``.
    """

    def dist(s: float) -> float:
        da = (s_center - s) / radius
        return math.sqrt(
            (radius + u) ** 2
            + (radius + u_center) ** 2
            - 2.0 * (radius + u) * (radius + u_center) * math.cos(da)
        )

    lo, hi = WIRE_S[0], s_end
    if dist(s_end) >= pocket_radius:
        return {
            "u": u,
            "s_entry": s_end,
            "s_opening": 0.0,
            "physical_opening": 0.0,
            "end_inside": 0.0,
        }
    for _ in range(80):
        mid = (lo + hi) / 2.0
        if dist(mid) > pocket_radius:
            lo = mid
        else:
            hi = mid
    s_entry = (lo + hi) / 2.0
    physical = (1.0 + u / radius) * (s_end - s_entry)
    return {
        "u": u,
        "s_entry": s_entry,
        "s_opening": s_end - s_entry,
        "physical_opening": physical,
        "end_inside": 1.0 if dist(s_end) < pocket_radius else 0.0,
        "end_distance": dist(s_end),
    }


def sphere_cap_radius(diameter: float, crown: float) -> float:
    base = diameter / 2.0
    return (base * base + crown * crown) / (2.0 * crown)


def default_params() -> dict[str, Any]:
    with DEFAULT_PARAMS_PATH.open("rb") as handle:
        return dict(tomllib.load(handle))


def _parse_value(raw: str) -> Any:
    lowered = raw.strip().lower()
    if lowered in {"true", "yes"}:
        return True
    if lowered in {"false", "no"}:
        return False
    try:
        if any(ch in raw for ch in ".eE"):
            return float(raw)
        return int(raw)
    except ValueError:
        return raw


def load_params_file(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    if path.suffix.lower() == ".json":
        parsed = json.loads(data.decode("utf-8"))
    else:
        parsed = tomllib.loads(data.decode("utf-8"))
    if parsed is None:
        return {}
    if not isinstance(parsed, dict):
        raise CheckFail(f"params file={path}: must be a table/object")
    return parsed


def canonical_key(key: Any) -> str:
    return str(key).strip().upper()


@functools.lru_cache(maxsize=1)
def load_placement() -> Any:
    """Load placement.py from this folder. Pad coordinates live there only."""
    name = "elicio_cad_placement"
    if name in sys.modules:
        return sys.modules[name]
    path = SCRIPT_DIR / "placement.py"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise CheckFail(f"placement.py: cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    module.__dict__["__name__"] = name
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _pair(params: Mapping[str, Any], key: str, default: tuple[float, float]) -> tuple[float, float]:
    if key not in params:
        return default
    value = params[key]
    return (float(value[0]), float(value[1]))


def cavity_u(params: Mapping[str, Any]) -> tuple[float, float]:
    return _pair(params, "CAVITY_U", CAVITY_U)


def cavity_s(params: Mapping[str, Any]) -> tuple[float, float]:
    return _pair(params, "CAVITY_S", CAVITY_S)


def board_zone_s(params: Mapping[str, Any]) -> tuple[float, float]:
    return _pair(params, "BOARD_ZONE_S", BOARD_S)


def board_zone_u(params: Mapping[str, Any]) -> tuple[float, float]:
    return _pair(params, "BOARD_ZONE_U", CAVITY_U)


def tail_ds(params: Mapping[str, Any]) -> float:
    return float(params.get("TAIL_DS", 0.0))


def tail_s0(params: Mapping[str, Any]) -> float:
    return float(params.get("TAIL_S0", TAIL_S0))


def shift_tail_s(params: Mapping[str, Any], s: float) -> float:
    if s >= TAIL_S0 - 1e-9:
        return s + tail_ds(params)
    return s


def shift_tail_pair(params: Mapping[str, Any], pair: tuple[float, float]) -> tuple[float, float]:
    return shift_tail_s(params, pair[0]), shift_tail_s(params, pair[1])


def contact_1_us(params: Mapping[str, Any]) -> tuple[float, float]:
    return (
        float(params.get("CONTACT_1_U", CONTACT_1[0])),
        float(params.get("CONTACT_1_S", CONTACT_1[1])),
    )


def contact_ref_us(params: Mapping[str, Any]) -> tuple[float, float]:
    return (
        float(params.get("CONTACT_REF_U", CONTACT_REF[0])),
        float(params.get("CONTACT_REF_S", shift_tail_s(params, CONTACT_REF[1]))),
    )


def wire_s_pair(params: Mapping[str, Any]) -> tuple[float, float]:
    return _pair(params, "WIRE_S", shift_tail_pair(params, WIRE_S))


def cable_exit_s(params: Mapping[str, Any]) -> float:
    return float(params.get("CABLE_EXIT_S", CABLE_EXIT_S))


def tab_height(params: Mapping[str, Any]) -> float:
    return float(params.get("TAB_HEIGHT", TAB_HEIGHT_DEFAULT))


def lid_experiments(params: Mapping[str, Any]) -> bool:
    """E1/E3/E5 geometry: order 1 always; order 2 only if CLOSURE_PASSED."""
    return bool(params.get("MOCK_CONTACTS", True)) or bool(params.get("CLOSURE_PASSED", False))


def nub_u_pair(params: Mapping[str, Any]) -> tuple[tuple[float, float], tuple[float, float]]:
    if "NUB_U" in params:
        raw = params["NUB_U"]
        return (float(raw[0][0]), float(raw[0][1])), (float(raw[1][0]), float(raw[1][1]))
    cu = cavity_u(params)
    return (cu[0] + 0.4, cu[0] + 1.2), (cu[1] - 1.2, cu[1] - 0.4)


def packing_is_v2(params: Mapping[str, Any]) -> bool:
    return str(params.get("PACKING", "")).upper() == "V2"


def stage_is_shell(params: Mapping[str, Any]) -> bool:
    return str(params.get("STAGE", "")).lower() == "shell"


def snap_strain(length: float, thick: float, deflection: float) -> float:
    """Cantilever snap strain, ε ≈ 1.5 t y / L² (Roark beam, end load)."""
    if length <= 0.0:
        return math.inf
    return 1.5 * thick * deflection / (length * length)


def _shell_boss_sites(layout: Any, v2: Any) -> list[tuple[str, float, float]]:
    """Board-boss (u, s). Packing skips both corners on this II winner."""
    placed = [
        (n, layout.parts[n].u, layout.parts[n].s)
        for n in layout.parts
        if str(n).startswith("boss")
    ]
    if placed:
        return placed
    _bu0, bu1 = layout.board_u
    bs0, bs1 = layout.board_s
    r = v2.BOSS_DIA / 2.0
    return [
        ("boss_1", bu1 - r - 0.4, bs0 + r + 0.4),
        ("boss_2", bu1 - r - 0.4, (bs0 + bs1) / 2.0),
    ]


def v2_spec(params: Mapping[str, Any]) -> Any:
    """The WP11 V2Spec a PACKING=v2 parameter set names."""
    v2 = load_placement()._v2()
    return v2.V2Spec(
        str(params.get("V2_ARCH", "A")),
        str(params.get("V2_CELL", "501015")),
        str(params.get("V2_LAYOUT", "series")),
        float(params.get("V2_WIDTH", 20.0)),
        float(params.get("V2_LID_Y", 8.0)),
        float(params.get("V2_ARC_PLUS", 0.0)),
        str(params.get("V2_IFACE", "I")),
        float(params.get("V2_STANDOFF", 3.5)),
        float(params.get("V2_RECESS", 0.0)),
    )


def apply_stage_b_packing(p: dict[str, Any]) -> None:
    """Packing A/B/C from placement.Layout, or v2 from placement_v2.V2Spec."""
    packing = str(p.get("PACKING", "C"))
    if packing.upper() == "V2":
        _apply_v2_packing(p)
        return
    packing = packing.upper()
    if packing not in {"A", "B", "C"}:
        raise CheckFail(f"PACKING={p.get('PACKING')}: must be A, B, C or v2")
    p["PACKING"] = packing
    layout = load_placement().get_layout(packing)
    p["BODY_WIDTH"] = float(layout.body_u[1] - layout.body_u[0])
    p["BODY_ARC"] = float(layout.body_arc)
    p["CAVITY_U"] = [float(layout.cavity_u[0]), float(layout.cavity_u[1])]
    p["CAVITY_S"] = [float(layout.cavity_s[0]), float(layout.cavity_s[1])]
    p["BOARD_ZONE_U"] = [float(layout.board_zone_u[0]), float(layout.board_zone_u[1])]
    p["BOARD_ZONE_S"] = [float(layout.board_zone_s[0]), float(layout.board_zone_s[1])]
    p["TAIL_DS"] = float(layout.tail_ds)
    p["TAIL_S0"] = float(layout.cavity_s[1])
    p["LEAD_PADS"] = {
        name: [float(coord[0]), float(coord[1])] for name, coord in layout.lead_pads.items()
    }
    p["TAB_DEG"] = {name: float(deg) for name, deg in layout.tab_deg.items()}
    p["WIRE_S"] = [WIRE_S[0] + p["TAIL_DS"], WIRE_S[1] + p["TAIL_DS"]]
    if "CONTACT_REF_S" not in p:
        p["CONTACT_REF_S"] = CONTACT_REF[1] + p["TAIL_DS"]
    if "CONTACT_REF_U" not in p:
        p["CONTACT_REF_U"] = CONTACT_REF[0]
    nu = nub_u_pair(p)
    p["NUB_U"] = [[nu[0][0], nu[0][1]], [nu[1][0], nu[1][1]]]


def _apply_v2_packing(p: dict[str, Any]) -> None:
    """Move width, arc and lid from a WP11 V2Spec. Construction stays packing C/A."""
    v2 = load_placement()._v2()
    spec = v2.V2Spec(
        str(p.get("V2_ARCH", "A")),
        str(p.get("V2_CELL", "501015")),
        str(p.get("V2_LAYOUT", "series")),
        float(p.get("V2_WIDTH", 20.0)),
        float(p.get("V2_LID_Y", 8.0)),
        float(p.get("V2_ARC_PLUS", 0.0)),
        str(p.get("V2_IFACE", "I")),
        float(p.get("V2_STANDOFF", 3.5)),
        float(p.get("V2_RECESS", 0.0)),
    )
    result = v2.run_spec(spec)
    # Order-1 construction path: packing C at 20 mm, packing A at 17 mm.
    # WP11 does not fork the solid; it overlays the numbers and measures.
    host = "C" if spec.width >= 20.0 - 1e-9 else "A"
    layout = load_placement().get_layout(host)
    p["PACKING"] = "v2"
    p["V2_ARCH"] = spec.arch
    p["V2_CELL"] = spec.cell
    p["V2_LAYOUT"] = spec.layout
    p["V2_WIDTH"] = spec.width
    p["V2_LID_Y"] = spec.lid_y
    p["V2_ARC_PLUS"] = spec.arc_plus
    p["V2_IFACE"] = spec.iface
    p["V2_STANDOFF"] = spec.standoff
    p["V2_RECESS"] = spec.recess
    p["V2_TAG"] = spec.tag
    p["BODY_WIDTH"] = spec.width
    p["BODY_ARC"] = float(result.body_arc)
    p["BODY_THICK"] = spec.lid_y + float(p["LID_THICK"])
    p["LID_Y"] = spec.lid_y
    p["CAVITY_U"] = [float(layout.cavity_u[0]), float(layout.cavity_u[1])]
    p["CAVITY_S"] = [float(layout.cavity_s[0]), float(layout.cavity_s[1])]
    p["BOARD_ZONE_U"] = [float(layout.board_zone_u[0]), float(layout.board_zone_u[1])]
    p["BOARD_ZONE_S"] = [float(layout.board_zone_s[0]), float(layout.board_zone_s[1])]
    p["TAIL_DS"] = float(layout.tail_ds) + spec.arc_plus
    p["TAIL_S0"] = float(layout.cavity_s[1]) + spec.arc_plus
    p["LEAD_PADS"] = {
        name: [float(coord[0]), float(coord[1])] for name, coord in layout.lead_pads.items()
    }
    p["TAB_DEG"] = {name: float(deg) for name, deg in layout.tab_deg.items()}
    p["WIRE_S"] = [WIRE_S[0] + p["TAIL_DS"], WIRE_S[1] + p["TAIL_DS"]]
    if "CONTACT_REF_S" not in p:
        p["CONTACT_REF_S"] = CONTACT_REF[1] + spec.arc_plus
    if "CONTACT_REF_U" not in p:
        p["CONTACT_REF_U"] = CONTACT_REF[0]
    nu = nub_u_pair(p)
    p["NUB_U"] = [[nu[0][0], nu[0][1]], [nu[1][0], nu[1][1]]]
    path = make_path(p["BODY_ARC"], p["CREASE_BOW"])
    p["TOTAL_CHORD"] = path.chord
    p["PATH_RADIUS"] = path.radius
    if "STAGE" in p:
        p["STAGE"] = str(p.get("STAGE", "")).lower()


def validate_overrides(base: Mapping[str, Any], override: Mapping[str, Any]) -> None:
    """Unknown keys and keys fixed for this release fail before export."""
    known = {canonical_key(k) for k in base} | OVERRIDABLE_KEYS
    canon_over = {canonical_key(k): v for k, v in override.items()}
    if bool(canon_over.get("MOCK_CONTACTS", True)):
        stage_b = sorted(STAGE_B_OVERLAY_KEYS & set(canon_over))
        if stage_b:
            raise CheckFail(
                f"{', '.join(stage_b)}: Stage B keys need MOCK_CONTACTS = false; "
                "order 1 would ignore them and build the plan value"
            )
    for key, value in override.items():
        canon = canonical_key(key)
        if canon not in known:
            raise CheckFail(f"{key}={value}: unknown parameter")
        if canon in OVERRIDABLE_KEYS:
            continue
        default = base[canon]
        same = (
            abs(float(value) - float(default)) < 1e-9
            if isinstance(default, (int, float)) and not isinstance(default, bool)
            else value == default
        )
        if not same:
            raise CheckFail(
                f"{canon}={value}: fixed at {default} in this release "
                "(plan §3.3 matrix; feature constants assume it)"
            )


def merge_params(
    base: dict[str, Any],
    override: Mapping[str, Any],
    used_defaults: list[str],
) -> dict[str, Any]:
    validate_overrides(base, override)
    merged = dict(base)
    for key, value in override.items():
        canon = canonical_key(key)
        merged[canon] = value
        if canon in used_defaults:
            used_defaults.remove(canon)
    return merged


def derived_params(raw: dict[str, Any], *, crease_bow_from_m: bool) -> dict[str, Any]:
    p = dict(raw)
    variant = str(p.get("VARIANT", "full")).lower()
    p["VARIANT"] = variant
    p["SIDE"] = str(p.get("SIDE", "right")).lower()
    p["HOOK_PRELOAD"] = float(p["HOOK_PRELOAD"])
    p["BODY_ARC"] = float(p["BODY_ARC"])
    p["BODY_WIDTH"] = float(p["BODY_WIDTH"])
    p["BODY_THICK"] = float(VARIANT_THICK[variant]) if variant in VARIANT_THICK else float(
        p.get("BODY_THICK", 9.0)
    )
    p["LID_THICK"] = float(p["LID_THICK"])
    p["LID_Y"] = p["BODY_THICK"] - p["LID_THICK"]
    p["M1"] = float(p["M1"])
    p["M2"] = float(p["M2"])
    p["M3"] = float(p["M3"])
    p["M4"] = float(p["M4"])
    p["M5"] = float(p["M5"])
    p["M8"] = float(p["M8"])
    p["HOOK_DIA"] = float(p["HOOK_DIA"])
    p["HOOK_ROOT_Y"] = float(p["M4"]) / 2.0
    p["GLASSES_FLAT"] = GLASSES_FLAT_DEPTH if p["M5"] > 0.0 else 0.0
    computed_bow = bow_from_arc_chord(p["M2"], p["M1"])
    if crease_bow_from_m:
        bow = computed_bow
    else:
        bow = float(p.get("CREASE_BOW", 3.0))
    p["CREASE_BOW_COMPUTED"] = computed_bow
    p["CREASE_BOW_REQUESTED"] = bow
    p["CREASE_BOW"] = clamp_crease_bow(bow)
    path = make_path(p["BODY_ARC"], p["CREASE_BOW"])
    p["TOTAL_CHORD"] = path.chord
    p["PATH_RADIUS"] = path.radius
    p["THETA_DEG"] = math.degrees(math.atan(p["HOOK_PRELOAD"] / path.chord))
    if "HOOK_RADIUS" in p:
        p["HOOK_RADIUS"] = float(p["HOOK_RADIUS"])
    else:
        # Plan §3.3 writes M8 + HOOK_DIA/2 + 1.0 but quotes 13.5 at M8 = 11,
        # centres the arc at (−9.5, 3, 0) and checks inner < M8 + 1. Only
        # a 0.75 clearance satisfies all three; the review logs it for Rolf.
        p["HOOK_RADIUS"] = p["M8"] + p["HOOK_DIA"] / 2.0 + HOOK_CLEARANCE
    p["MOCK_CONTACTS"] = bool(p.get("MOCK_CONTACTS", True))
    if p["MOCK_CONTACTS"]:
        for key in STAGE_B_ONLY_KEYS:
            p.pop(key, None)
        u2, s2 = contact_2_us()
        p["CONTACT_2_U"] = u2
        p["CONTACT_2_S"] = s2
        return p
    apply_stage_b_packing(p)
    c1 = contact_1_us(p)
    p["CONTACT_1_U"], p["CONTACT_1_S"] = c1
    u2, s2 = contact_2_us(c1)
    p["CONTACT_2_U"] = u2
    p["CONTACT_2_S"] = s2
    p["TAB_HEIGHT"] = tab_height(p)
    p["CLOSURE_PASSED"] = bool(p.get("CLOSURE_PASSED", False))
    p["CONTACT_SOURCE"] = str(p.get("CONTACT_SOURCE", "plan §3.3 defaults"))
    stage = str(p.get("STAGE", "")).lower()
    p["STAGE"] = stage
    if stage and stage not in {"b", "shell"}:
        raise CheckFail(f"STAGE={p.get('STAGE')}: must be B or shell")
    if stage_is_shell(p) and not packing_is_v2(p):
        raise CheckFail("STAGE=shell needs PACKING=v2")
    return p


def preload_tag(preload: float) -> str:
    return f"p{int(round(preload * 10)):02d}"


def part_name(kind: str, params: Mapping[str, Any]) -> str:
    if kind == "body":
        return f"body_{params['VARIANT']}_{preload_tag(params['HOOK_PRELOAD'])}"
    return kind


def emboss_label(params: Mapping[str, Any], defaults_used: list[str]) -> str:
    side = "R" if params["SIDE"] == "right" else "L"
    variant = str(params["VARIANT"]).upper()
    tag = preload_tag(params["HOOK_PRELOAD"]).upper()
    ref = " REF" if any(key in defaults_used for key in REFERENCE_M_KEYS) else ""
    # V1 is the order 1 gauge; a Stage B lid must not read as one.
    version = "V1" if params.get("MOCK_CONTACTS", True) else "V2"
    return f"ELICIO {version} {side} {variant} {tag}{ref}".strip()


def git_rev_parse(repo: Path) -> str:
    try:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                cwd=repo,
                stderr=subprocess.DEVNULL,
                text=True,
            ).strip()
        )
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def git_commit_solids(repo: Path, cad_dir: Path | None = None) -> str:
    """Last commit that changed a hashed solid, not HEAD of the repository.

    Paths are the committed STEP/STL/3MF files under docs/fab/cad/v1 (order 1)
    or the given cad_dir (shell v2). A later commit that only adds renders,
    docs, or tests does not move this field.
    """
    folder = cad_dir if cad_dir is not None else (repo / "docs" / "fab" / "cad" / "v1")
    if not folder.is_dir():
        return git_rev_parse(repo)
    paths = sorted(
        str(path)
        for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() in {".step", ".stl", ".3mf"}
    )
    if not paths:
        return git_rev_parse(repo)
    try:
        return (
            subprocess.check_output(
                ["git", "log", "-1", "--format=%H", "--", *paths],
                cwd=repo,
                stderr=subprocess.DEVNULL,
                text=True,
            ).strip()
            or git_rev_parse(repo)
        )
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def git_commit(repo: Path, cad_dir: Path | None = None) -> str:
    """Manifest ``commit``: solids last-change, not the current HEAD."""
    return git_commit_solids(repo, cad_dir)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


# Plan §3.6 fit table: (pair, type, nominal, adverse). The script derives
# each nominal from the feature constants and fails if it drifts.
PLAN_FITS = (
    ("plate underside : recess floor", "seating", 0.0, None),
    ("lip inner face : top face, s", "compliant, one-sided", 0.2, (-0.4, 0.8)),
    ("bump tip : groove bottom, s", "compliant, one-sided", 0.2, (-0.4, 0.8)),
    ("bump engagement into groove, s", "retention", 0.3, (-0.3, 0.9)),
    ("bump 0.6 : groove 1.0, y", "rigid, total", 0.4, (-0.2, 1.0)),
    ("tongue 0.5 : slot 0.9, y", "rigid, total", 0.4, (-0.2, 1.0)),
    ("tongue tip : slot end, s", "rigid, one-sided", 0.4, (-0.2, 1.0)),
    ("web 0.8 : pocket 1.4, s", "rigid, total", 0.6, (0.0, 1.2)),
    ("web bottom : pocket floor, y", "rigid, one-sided", 0.4, (-0.2, 1.0)),
    ("nub : side wall, u", "rigid, one-sided", 0.4, (-0.2, 1.0)),
)
PART_TOLERANCE = 0.3  # ±0.3 per part, plan §3.6; a pair moves by 2 × 0.3
LID_TONGUE_Y_OFF = (-0.8, -0.3)
LID_WEB_Y_OFF = (-0.8, 0.0)
# Contact stack reservation, plan §3.3 CONTACT_STACK and §4.
SCREW_LENGTH = 4.0
STACK_LUG = 0.5
STACK_NUT = 1.6
STACK_KAPTON = 0.13
KEEPOUT_SIGNAL_DIA = 7.1
KEEPOUT_TOP_Y = 4.13
BOARD_UNDERSIDE_Y = 4.3
COUPON_RIB = (0.4, 3.0, 12.0)  # thickness, height above the plate, length


def fit_nominals(params: Mapping[str, Any]) -> dict[str, float]:
    """Nominal clearance of each §3.6 pair, from the feature constants."""
    lip_y0_off = float(params["LID_THICK"]) - LIP_LENGTH  # lip bottom − LID_Y
    bump_y = (lip_y0_off, lip_y0_off + BUMP_TALL)
    tongue_u0 = (TONGUE_SLOT_U[0] + TONGUE_SLOT_U[1] - LID_TONGUE_WIDTH) / 2.0
    return {
        "plate underside : recess floor": 0.0,
        "lip inner face : top face, s": 0.0 - LIP_S[1],
        "bump tip : groove bottom, s": GROOVE_S[1] - (LIP_S[1] + BUMP_OUT),
        "bump engagement into groove, s": (LIP_S[1] + BUMP_OUT) - GROOVE_S[0],
        "bump 0.6 : groove 1.0, y": (GROOVE_Y_OFF[1] - GROOVE_Y_OFF[0]) - (bump_y[1] - bump_y[0]),
        "tongue 0.5 : slot 0.9, y": (TONGUE_SLOT_Y_OFF[1] - TONGUE_SLOT_Y_OFF[0])
        - (LID_TONGUE_Y_OFF[1] - LID_TONGUE_Y_OFF[0]),
        "tongue tip : slot end, s": TONGUE_SLOT_S[1] - LID_TONGUE_S[1],
        "web 0.8 : pocket 1.4, s": (WEB_POCKET_S[1] - WEB_POCKET_S[0]) - (LID_WEB_S[1] - LID_WEB_S[0]),
        "web bottom : pocket floor, y": LID_WEB_Y_OFF[0] - WEB_POCKET_Y_OFF[0],
        "nub : side wall, u": min(
            nub_u_pair(params)[0][0] - cavity_u(params)[0],
            cavity_u(params)[1] - nub_u_pair(params)[1][1],
        ),
        "_bump_inside_groove_y": min(bump_y[0] - GROOVE_Y_OFF[0], GROOVE_Y_OFF[1] - bump_y[1]),
        "_tongue_inside_slot_u": min(tongue_u0 - TONGUE_SLOT_U[0], TONGUE_SLOT_U[1] - tongue_u0 - LID_TONGUE_WIDTH),
    }


def fit_table(params: Mapping[str, Any]) -> list[dict[str, Any]]:
    """§3.6 pairs with the nominal derived from geometry, adverse at ±0.3 per part."""
    derived = fit_nominals(params)
    rows = []
    for pair, kind, _plan_nominal, plan_adverse in PLAN_FITS:
        nominal = round(derived[pair], 6)
        adverse = (
            None
            if plan_adverse is None
            else [round(nominal - 2 * PART_TOLERANCE, 6), round(nominal + 2 * PART_TOLERANCE, 6)]
        )
        rows.append({"pair": pair, "type": kind, "nominal": nominal, "adverse": adverse})
    return rows


def wall_sizes(params: Mapping[str, Any]) -> dict[str, float]:
    """Enclosing walls from the geometry, each held to ≥ 1.0 (plan §3.6)."""
    lid_y = float(params["BODY_THICK"]) - float(params["LID_THICK"])
    cu = cavity_u(params)
    cs = cavity_s(params)
    return {
        "floor (WALL_MEDIAL)": float(params["WALL_MEDIAL"]),
        "anterior side wall": cu[0],
        "posterior side wall": float(params["BODY_WIDTH"]) - cu[1],
        "top end wall": cs[0],
        "top end wall at LIP_GROOVE": cs[0] - GROOVE_S[1],
        "lip above TONGUE_SLOT": float(params["BODY_THICK"]) - (lid_y + TONGUE_SLOT_Y_OFF[1]),
        "tail below TONGUE_SLOT": lid_y + TONGUE_SLOT_Y_OFF[0],
        "tail below web pocket": lid_y + WEB_POCKET_Y_OFF[0],
        "lid plate": float(params["LID_THICK"]),
        "hook": float(params["HOOK_DIA"]),
    }


def exceptions_block(params: Mapping[str, Any]) -> dict[str, Any]:
    """E1–E5 sizes from the feature constants; minima from plan §3.6."""
    return {
        "E1": {
            "feature": "tongue",
            "size": round(LID_TONGUE_Y_OFF[1] - LID_TONGUE_Y_OFF[0], 6),
            "plan_size": 0.5,
            "minimum": 0.4,
            "note": "minimum fitted",
        },
        "E2": {
            "feature": "rib",
            "size": round(RIB_S[1] - RIB_S[0], 6),
            "plan_size": 0.8,
            "minimum": 0.8,
            "note": "locating only",
        },
        "E3": {
            "feature": "nubs",
            "size": NUB,
            "plan_size": 0.8,
            "minimum": 0.6,
        },
        "E4": {
            "feature": "coupon rib",
            "size": COUPON_RIB[0],
            "plan_size": 0.4,
            "minimum": 0.4,
            "note": "measurement",
        },
        "E5": {
            "feature": "lip cantilever / bump",
            "size": {"lip": round(LIP_S[1] - LIP_S[0], 6), "bump": BUMP_OUT},
            "plan_size": {"lip": 1.0, "bump": 0.5},
            "minimum": {"lip": 1.0, "bump": 0.2},
            "note": "below JLC 1.5; fitted bump ≥ 0.2",
        },
    }


def contact_stack(params: Mapping[str, Any], wall_extra: float = 0.0) -> dict[str, float]:
    """Stack above the floor. The screw tip sits at y = SCREW_LENGTH whatever
    the wall; the nut top sits at wall + lug + nut. The higher one, plus
    Kapton, is the stack top (plan §3.3 CONTACT_STACK, §4)."""
    wall = float(params["WALL_MEDIAL"]) + wall_extra
    nut_top = wall + STACK_LUG + STACK_NUT
    metal_top = max(SCREW_LENGTH, nut_top)
    return {
        "wall": wall,
        "lug": STACK_LUG,
        "nut": STACK_NUT,
        "tip_past_nut": SCREW_LENGTH - nut_top,
        "kapton": STACK_KAPTON,
        "height_above_floor": metal_top + STACK_KAPTON - wall,
        "top_y": metal_top + STACK_KAPTON,
    }


def keepout_clearances(params: Mapping[str, Any], path: PathGeom) -> dict[str, float]:
    """Body-frame gap from each KEEPOUT_SIGNAL cylinder to the pads, rib and
    cavity walls (plan §3.3 CONTACT_1 note; interface v1 §6.1: 0.09 mm in
    (u, s) at the superior low-u pad)."""
    radius = KEEPOUT_SIGNAL_DIA / 2.0
    cu0, cu1 = cavity_u(params)
    cs0, cs1 = cavity_s(params)
    bs0, bs1 = board_zone_s(params)
    c1 = contact_1_us(params)

    def xz(u: float, s: float) -> tuple[float, float]:
        x, _y, z = p_xyz(path, u, s, 0.0)
        return x, z

    def gap_to_patch(cu: float, cs: float, u0: float, u1: float, s0: float, s1: float) -> float:
        cx, cz = xz(cu, cs)
        best = math.inf
        n = 60
        for i in range(n + 1):
            for u, s in (
                (u0 + (u1 - u0) * i / n, s0),
                (u0 + (u1 - u0) * i / n, s1),
                (u0, s0 + (s1 - s0) * i / n),
                (u1, s0 + (s1 - s0) * i / n),
            ):
                px, pz = xz(u, s)
                best = min(best, math.hypot(px - cx, pz - cz))
        return best - radius

    contacts = {
        "CONTACT_1": c1,
        "CONTACT_2": (float(params["CONTACT_2_U"]), float(params["CONTACT_2_S"])),
    }
    pads = {
        "superior low-u pad": (cu0, cu0 + PAD_SIZE, bs0, bs0 + PAD_SIZE),
        "superior high-u pad": (cu1 - PAD_SIZE, cu1, bs0, bs0 + PAD_SIZE),
        "inferior low-u pad": (cu0, cu0 + PAD_SIZE, bs1 - PAD_SIZE, bs1),
        "inferior high-u pad": (cu1 - PAD_SIZE, cu1, bs1 - PAD_SIZE, bs1),
        "rib": (cu0, cu1, RIB_S[0], RIB_S[1]),
    }
    out: dict[str, float] = {}
    for cname, (cu, cs) in contacts.items():
        for pname, (u0, u1, s0, s1) in pads.items():
            out[f"{cname} to {pname}"] = gap_to_patch(cu, cs, u0, u1, s0, s1)
        # Walls: offset-path distance is exact in u; the end wall is a radial line.
        out[f"{cname} to anterior wall"] = (cu - radius) - cu0
        out[f"{cname} to posterior wall"] = cu1 - (cu + radius)
        out[f"{cname} to cavity end"] = gap_to_patch(cu, cs, cu0, cu1, cs1, cs1)
    if not params.get("MOCK_CONTACTS", True) and not packing_is_v2(params):
        pl = load_placement()
        packing = str(params["PACKING"])
        for pad_name in ("SIG1", "SIG2"):
            best = math.inf
            n = 40
            for pname, (u0, u1, s0, s1) in pads.items():
                local = math.inf
                for i in range(n + 1):
                    for uu, ss in (
                        (u0 + (u1 - u0) * i / n, s0),
                        (u0 + (u1 - u0) * i / n, s1),
                        (u0, s0 + (s1 - s0) * i / n),
                        (u1, s0 + (s1 - s0) * i / n),
                    ):
                        local = min(
                            local,
                            pl.point_tab_gap(pad_name, uu, ss, packing, mode="real"),
                        )
                out[f"TAB {pad_name} to {pname}"] = local
                best = min(best, local)
            out[f"TAB {pad_name} min pad/rib gap"] = best
    return out


def assert_override_matrix(overrides: Mapping[str, Any]) -> None:
    """Anything outside VARIANT × HOOK_PRELOAD fails before export."""
    if "VARIANT" in overrides:
        variant = str(overrides["VARIANT"]).lower()
        if variant not in MATRIX_VARIANTS:
            raise CheckFail(
                f"VARIANT={overrides['VARIANT']}: must be full or thin"
            )
    if "HOOK_PRELOAD" in overrides:
        preload = float(overrides["HOOK_PRELOAD"])
        if preload not in MATRIX_PRELOADS:
            raise CheckFail(
                f"HOOK_PRELOAD={overrides['HOOK_PRELOAD']}: must be 1.5 or 2.5"
            )


def q21_ref_lug_numbers(params: Mapping[str, Any]) -> dict[str, float]:
    """TE 31428 upright in the Ø7.5 pocket (contacts.md §5.3, Q21), plan numbers.

    PACKING=v2 replaces the lug with the brass standoff: in interface II the
    flex ring lies under it (plan v2 §5.3); review r5 replaced the lane's
    DIN 439 nut stack, which plan v2 no longer uses.
    """
    wall = float(params["WALL_MEDIAL"])
    lid_y = float(params["LID_Y"])
    pl = load_placement()
    if packing_is_v2(params):
        v2 = pl._v2()
        spec = v2_spec(params)
        st_y0, st_y1 = v2.standoff_y(spec)
        return {
            "stack_top_y": round(st_y1, 4),
            "lid_y": lid_y,
            "ring_d": v2.RING_D,
            "ring_t": round(v2.ring_under(spec), 4),
            "standoff_h": spec.standoff,
            "standoff_circumr": v2.STANDOFF_CIRCUMR,
            "tip_below_top": round(v2.tip_below_standoff_top(spec), 4),
            "pocket_dia": POCKET_DIA,
            "pocket_r": POCKET_DIA / 2.0,
        }
    lug_top_y = wall + float(pl.TAB_LEN) + float(pl.LUG_THICK)
    barrel_outer = float(pl.RING_R) + float(pl.TAB_W)
    return {
        "lug_top_y": round(lug_top_y, 4),
        "lid_y": lid_y,
        "barrel_outer": round(barrel_outer, 4),
        "pocket_r": POCKET_DIA / 2.0,
        "lug_thick": float(pl.LUG_THICK),
    }


def cell_pocket_clearances(params: Mapping[str, Any]) -> dict[str, float]:
    """Cell 5.2 × 10.4 × 15.6 plus 0.5 foam against the plan pocket and LID_Y."""
    wall = float(params["WALL_MEDIAL"])
    top = min(BATTERY_Y[1], float(params["LID_Y"]))
    need_y = CELL_MAX[0] + FOAM_THICK
    return {
        "pocket_top_y": top,
        "need_y": round(need_y, 4),
        "clear_y": round(top - wall - need_y, 4),
        "clear_u": round(BATTERY_U[1] - BATTERY_U[0] - CELL_MAX[1], 4),
        "clear_s": round(BATTERY_S[1] - BATTERY_S[0] - CELL_MAX[2], 4),
    }


def cable_exit_pre_cad(params: Mapping[str, Any]) -> dict[str, float]:
    """Ø2.0 exit s and y ranges against the cavity, rib, battery and corner pads."""
    s_exit = cable_exit_s(params)
    r = CABLE_EXIT_DIA / 2.0
    cs0, cs1 = cavity_s(params)
    bs0, bs1 = board_zone_s(params)
    ey0, ey1 = CABLE_EXIT_Y - r, CABLE_EXIT_Y + r
    pad_s_gap = min(
        s_exit - r - (bs0 + PAD_SIZE) if s_exit > bs0 else bs0 - (s_exit + r),
        (bs1 - PAD_SIZE) - (s_exit + r) if s_exit < bs1 else s_exit - r - bs1,
    )
    pads_in_y = ey0 < PAD_Y[1] and ey1 > PAD_Y[0]
    return {
        "CABLE_EXIT_S": s_exit,
        "CABLE_EXIT_Y": CABLE_EXIT_Y,
        "in_cavity_s": 1.0 if cs0 < s_exit - r and s_exit + r < cs1 else 0.0,
        "board_side_of_rib": 1.0 if s_exit - r > RIB_S[1] else 0.0,
        "y_ok": 1.0 if float(params["WALL_MEDIAL"]) < ey0 and ey1 < float(params["LID_Y"]) else 0.0,
        "corner_pad_s_gap": round(pad_s_gap if pads_in_y else math.inf, 4),
    }


def run_stage_b_pre_cad_checks(params: Mapping[str, Any], record: Callable[..., None]) -> None:
    """Stage B fail-fast checks from the plan numbers, before any solid exists.

    Names end in " pre-CAD". The named Stage B checks in the manifest are
    measured on the built solids (``run_stage_b_solid_checks``).
    """
    pl = load_placement()
    c1 = contact_1_us(params)
    c2 = (float(params["CONTACT_2_U"]), float(params["CONTACT_2_S"]))
    drift = max(
        math.hypot(c1[0] - pl.CONTACT_1[0], c1[1] - pl.CONTACT_1[1]),
        math.hypot(c2[0] - pl.CONTACT_2[0], c2[1] - pl.CONTACT_2[1]),
    )
    # Pads, tab angles and the reference route come from placement.py, which
    # searched them for its own contact sites. Other sites need a new search.
    record(
        "PLACEMENT_contacts",
        drift <= PLACEMENT_CONTACT_TOL,
        "signal contacts at the sites placement.py searched pads, tab angles and "
        "the reference route for; new sites (WP7a) need a placement re-run first",
        CONTACT_1_U=c1[0],
        CONTACT_1_S=c1[1],
        placement_CONTACT_1_U=float(pl.CONTACT_1[0]),
        placement_CONTACT_1_S=float(pl.CONTACT_1[1]),
        drift=round(drift, 4),
    )
    wall = float(params["WALL_MEDIAL"])
    tab_h = tab_height(params)
    barrel_top = wall + BARREL_HEIGHT
    envelope_top = wall + tab_h
    record(
        "BOARD_underside_clear pre-CAD",
        BOARD_UNDERSIDE_Y > KEEPOUT_TOP_Y
        and BOARD_UNDERSIDE_Y > barrel_top
        and BOARD_UNDERSIDE_Y > envelope_top,
        "board underside at y 4.3 clears stack top 4.13, barrels and tab envelopes",
        stack_top=KEEPOUT_TOP_Y,
        barrel_top=round(barrel_top, 4),
        envelope_top=round(envelope_top, 4),
        board_underside=BOARD_UNDERSIDE_Y,
        TAB_HEIGHT=tab_h,
    )
    cell = cell_pocket_clearances(params)
    record(
        "CELL_envelope pre-CAD",
        cell["clear_y"] >= -1e-9 and cell["clear_u"] >= -1e-9 and cell["clear_s"] >= -1e-9,
        "cell 5.2 × 10.4 × 15.6 plus 0.5 foam fits the plan pocket under LID_Y",
        **cell,
    )
    cable = cable_exit_pre_cad(params)
    record(
        "CABLE_EXIT_cavity pre-CAD",
        cable["in_cavity_s"] == 1.0
        and cable["board_side_of_rib"] == 1.0
        and cable["y_ok"] == 1.0
        and cable["corner_pad_s_gap"] > 0.0,
        "Ø2.0 exit lies in the board zone between the corner pads, above the floor, below LID_Y",
        **cable,
    )
    gaps = keepout_clearances(params, make_path(float(params["BODY_ARC"]), float(params["CREASE_BOW"])))
    if packing_is_v2(params):
        record(
            "TAB_envelope_air pre-CAD",
            False,
            "NOT_MEASURED: v2 flex tabs are not the TE 31428 pad-gap search; solids measure them",
            fatal=False,
            TAB_HEIGHT=tab_h,
        )
    else:
        tab_min = min(gaps.get("TAB SIG1 min pad/rib gap", 1.0), gaps.get("TAB SIG2 min pad/rib gap", 1.0))
        record(
            "TAB_envelope_air pre-CAD",
            tab_min > 0.0,
            "tab envelopes 1.96 wide from Ø7.1 to 8.85 miss the corner pads and rib (u, s)",
            min_gap=round(tab_min, 4),
            TAB_HEIGHT=tab_h,
        )
    q21 = q21_ref_lug_numbers(params)
    if packing_is_v2(params):
        record(
            "Q21_REF_lug pre-CAD",
            q21["stack_top_y"] < q21["lid_y"]
            and max(q21["ring_d"] / 2.0, q21["standoff_circumr"]) <= q21["pocket_r"],
            "v2: ring and brass standoff (hex corners) against LID_Y and the Ø7.5 pocket; no TE 31428 lug",
            fatal=False,
            **q21,
        )
    else:
        record(
            "Q21_REF_lug pre-CAD",
            q21["lug_top_y"] < q21["lid_y"] and q21["barrel_outer"] <= q21["pocket_r"],
            "reference lug upright against LID_Y and the Ø7.5 pocket (Q21); recorded, not fatal",
            fatal=False,
            **q21,
        )


def run_pre_cad_checks(params: Mapping[str, Any]) -> list[Check]:
    checks: list[Check] = []

    def record(name: str, passed: bool, detail: str, fatal: bool = True, **numbers: float) -> None:
        checks.append(Check(name, passed, detail, numbers))
        if not passed and fatal:
            num = ", ".join(f"{k}={v}" for k, v in numbers.items())
            raise CheckFail(f"{name}: {detail} ({num})" if num else f"{name}: {detail}")

    variant = params["VARIANT"]
    preload = float(params["HOOK_PRELOAD"])
    record(
        "matrix",
        variant in MATRIX_VARIANTS and preload in MATRIX_PRELOADS,
        "VARIANT × HOOK_PRELOAD must be {full,thin} × {1.5,2.5}",
        VARIANT=0.0 if variant not in MATRIX_VARIANTS else 1.0,
        HOOK_PRELOAD=preload,
    )
    thick_expected = VARIANT_THICK[variant]
    thick_detail = "thickness follows VARIANT"
    if packing_is_v2(params):
        thick_expected = float(params["LID_Y"]) + float(params["LID_THICK"])
        thick_detail = "thickness follows LID_Y + LID_THICK when PACKING=v2"
    record(
        "BODY_THICK",
        abs(float(params["BODY_THICK"]) - thick_expected) < 1e-9,
        thick_detail,
        BODY_THICK=float(params["BODY_THICK"]),
        expected=thick_expected,
    )
    bow = float(params["CREASE_BOW"])
    record(
        "CREASE_BOW_clamp",
        CREASE_BOW_MIN - 1e-9 <= bow <= CREASE_BOW_MAX + 1e-9,
        "clamped bow is 1–8",
        CREASE_BOW=bow,
    )
    gate = float(params["TOTAL_CHORD"]) + 3.0
    record(
        "M1_gate",
        float(params["M1"]) + 1e-9 >= gate,
        "M1 must be at least TOTAL_CHORD + 3",
        M1=float(params["M1"]),
        TOTAL_CHORD=float(params["TOTAL_CHORD"]),
        gate=gate,
    )
    inner = float(params["HOOK_RADIUS"]) - float(params["HOOK_DIA"]) / 2.0
    limit = float(params["M8"]) + 1.0
    record(
        "HOOK_RADIUS",
        inner < limit - 1e-9,
        "hook inner radius HOOK_RADIUS − HOOK_DIA/2 must be < M8 + 1",
        HOOK_RADIUS=float(params["HOOK_RADIUS"]),
        inner=inner,
        M8=float(params["M8"]),
        limit=limit,
    )
    for wall_name, value in wall_sizes(params).items():
        record(
            f"wall: {wall_name}",
            value + 1e-9 >= 1.0,
            "walls ≥ 1.0 (plan §3.6)",
            size=round(value, 6),
        )
    for key, block in exceptions_block(params).items():
        if not lid_experiments(params) and key in {"E1", "E3", "E5"}:
            continue
        sizes = block["size"] if isinstance(block["size"], dict) else {"": block["size"]}
        plans = block["plan_size"] if isinstance(block["plan_size"], dict) else {"": block["plan_size"]}
        minima = block["minimum"] if isinstance(block["minimum"], dict) else {"": block["minimum"]}
        for part, size in sizes.items():
            name = f"{key}_{part}" if part else key
            record(
                name,
                abs(size - plans[part]) < 1e-6 and size + 1e-9 >= minima[part],
                f"{block['feature']} at its plan size and ≥ its minimum (plan §3.6)",
                size=size,
                plan_size=plans[part],
                minimum=minima[part],
            )
    skip_fits: set[str] = set()
    if not lid_experiments(params):
        skip_fits = {
            "lip inner face : top face, s",
            "bump tip : groove bottom, s",
            "bump engagement into groove, s",
            "bump 0.6 : groove 1.0, y",
            "tongue 0.5 : slot 0.9, y",
            "tongue tip : slot end, s",
            "web 0.8 : pocket 1.4, s",
            "web bottom : pocket floor, y",
            "nub : side wall, u",
        }
    nominals = fit_nominals(params)
    for pair, _kind, plan_nominal, _adverse in PLAN_FITS:
        if pair in skip_fits:
            continue
        record(
            f"fit: {pair}",
            abs(nominals[pair] - plan_nominal) < 1e-6,
            "nominal from geometry matches plan §3.6",
            nominal=round(nominals[pair], 6),
            plan=plan_nominal,
        )
    if lid_experiments(params):
        for inner in ("_bump_inside_groove_y", "_tongue_inside_slot_u"):
            record(
                f"fit: {inner.strip('_')}",
                nominals[inner] > 0.0,
                "mating feature sits inside its slot",
                margin=round(nominals[inner], 6),
            )
    stack = contact_stack(params)
    adverse = contact_stack(params, wall_extra=PART_TOLERANCE)
    record(
        "CONTACT_STACK",
        abs(stack["top_y"] - KEEPOUT_TOP_Y) < 1e-6
        and stack["tip_past_nut"] >= 0.0
        and adverse["top_y"] < BOARD_UNDERSIDE_Y,
        "stack top at KEEPOUT_SIGNAL top 4.13, tip past the nut, below the board at wall +0.3",
        top_y=round(stack["top_y"], 6),
        tip_past_nut=round(stack["tip_past_nut"], 6),
        top_y_wall_plus_0_3=round(adverse["top_y"], 6),
        board_underside=BOARD_UNDERSIDE_Y,
    )
    path_now = make_path(float(params["BODY_ARC"]), float(params["CREASE_BOW"]))
    ws = wire_s_pair(params)
    ref_u, ref_s = contact_ref_us(params)
    for name, gap in keepout_clearances(params, path_now).items():
        record(
            f"keep-out: {name}",
            gap > 0.0,
            "KEEPOUT_SIGNAL Ø7.1 clear of solid (body frame)",
            gap=round(gap, 4),
        )
    opening = wire_channel_opening(
        float(params["PATH_RADIUS"]),
        s_end=ws[1],
        u_center=ref_u,
        s_center=ref_s,
    )
    record(
        "WIRE_CHANNEL_opening",
        opening["physical_opening"] > 0.0,
        "physical opening at u=9.3 must be positive",
        physical_opening=opening["physical_opening"],
        s_entry=opening["s_entry"],
    )
    for bow in (1.0, 3.0, 8.0):
        path = make_path(float(params["BODY_ARC"]), bow)
        report = wire_channel_opening(
            path.radius,
            s_end=ws[1],
            u_center=ref_u,
            s_center=ref_s,
        )
        record(
            f"WIRE_CHANNEL_bow_{bow:g}",
            report["physical_opening"] > 0.0,
            "opening at supported bow",
            CREASE_BOW=bow,
            physical_opening=report["physical_opening"],
        )
    if not params.get("MOCK_CONTACTS", True):
        run_stage_b_pre_cad_checks(params, record)
    return checks


# --- CAD (lazy: only called when build123d is installed) ---


def _require_cad() -> None:
    if not HAS_BUILD123D:
        raise CheckFail("build123d: not installed (pip install -e '.[cad]')")


def _vec(path: PathGeom, u: float, s: float, y: float) -> Vector:
    x, yv, z = p_xyz(path, u, s, y)
    return Vector(x, yv, z)


def _station_plane(path: PathGeom, s: float) -> Plane:
    a = angle_at(path, s)
    radial = Vector(math.cos(a), 0.0, math.sin(a))
    return Plane(
        origin=Vector(path.cx, 0.0, path.cz),
        x_dir=radial,
        y_dir=Vector(0.0, 1.0, 0.0),
    )


def _y_axis(path: PathGeom) -> Axis:
    return Axis(Vector(path.cx, 0.0, path.cz), Vector(0.0, 1.0, 0.0))


def _section(
    path: PathGeom,
    s: float,
    u0: float,
    u1: float,
    y0: float,
    y1: float,
    *,
    round_medial: bool = False,
    fillet_r: float = 1.5,
) -> Shape:
    width = u1 - u0
    height = y1 - y0
    plane = _station_plane(path, s)
    sketch = plane * Pos(path.radius + (u0 + u1) / 2.0, (y0 + y1) / 2.0, 0.0) * Rectangle(
        width, height
    )
    if round_medial and y0 <= 1e-9:
        radius = min(fillet_r, width / 2.0 - 0.05, height - 0.05)
        if radius > 0.05:
            medial = [v for v in sketch.vertices() if abs(v.Y - y0) < 1e-5]
            if len(medial) == 2:
                sketch = fillet(medial, radius)
    return sketch


def _revolve_s(path: PathGeom, sketch: Shape, s0: float, s1: float) -> Shape:
    angle = math.degrees((s1 - s0) / path.radius)
    if abs(angle) < 1e-9:
        return Solid.make_box(0.01, 0.01, 0.01)
    return revolve(sketch.faces()[0], axis=_y_axis(path), revolution_arc=angle)


def _loft_s(
    path: PathGeom,
    s0: float,
    s1: float,
    u_at: Callable[[float], tuple[float, float]],
    y0: float,
    y1: float,
    *,
    round_medial: bool = False,
    fillet_r: float = 1.5,
    step: float = 2.0,
) -> Shape:
    count = max(2, int(math.ceil(abs(s1 - s0) / step)) + 1)
    faces: list[Face] = []
    for i in range(count):
        s = s0 + (s1 - s0) * i / (count - 1)
        u0, u1 = u_at(s)
        sk = _section(path, s, u0, u1, y0, y1, round_medial=round_medial, fillet_r=fillet_r)
        faces.append(sk.faces()[0])
    return loft(faces)


def _path_solid(
    path: PathGeom,
    u0: float,
    u1: float,
    s0: float,
    s1: float,
    y0: float,
    y1: float,
    *,
    round_medial: bool = False,
    fillet_r: float = 1.5,
    split_s: float = TAIL_S0,
) -> Shape:
    """Revolved along the body arc up to ``split_s`` (the tail start: 38.2,
    or 41.7 for packing B), lofted past it."""
    def const_u(_s: float) -> tuple[float, float]:
        return u0, u1

    if s1 <= split_s + 1e-9:
        sketch = _section(
            path, s0, u0, u1, y0, y1, round_medial=round_medial, fillet_r=fillet_r
        )
        return _revolve_s(path, sketch, s0, s1)
    if s0 >= split_s - 1e-9:
        return _loft_s(
            path,
            s0,
            s1,
            const_u,
            y0,
            y1,
            round_medial=round_medial,
            fillet_r=fillet_r,
        )
    return _path_solid(
        path, u0, u1, s0, split_s, y0, y1, round_medial=round_medial, fillet_r=fillet_r, split_s=split_s
    ).fuse(
        _path_solid(
            path, u0, u1, split_s, s1, y0, y1, round_medial=round_medial, fillet_r=fillet_r, split_s=split_s
        )
    )


def _tail_width(
    s: float, body_width: float, split_s: float = TAIL_S0, tail_end: float = 48.4
) -> float:
    span = tail_end - split_s
    t = (s - split_s) / span if abs(span) > 1e-9 else 1.0
    t = min(1.0, max(0.0, t))
    return body_width + (TAIL_TIP_WIDTH - body_width) * t


def _tail_u(
    s: float, body_width: float, split_s: float = TAIL_S0, tail_end: float = 48.4
) -> tuple[float, float]:
    width = _tail_width(s, body_width, split_s, tail_end)
    center = body_width / 2.0
    return center - width / 2.0, center + width / 2.0


def _one_solid(shape: Shape, name: str) -> Solid:
    solids = list(shape.solids())
    if len(solids) != 1:
        raise CheckFail(f"{name}: expected one solid, got {len(solids)}")
    solid = solids[0]
    if not solid.is_valid:
        raise CheckFail(f"{name}: solid is not valid")
    return solid


FILLET_STEP = 0.25
OVERLAP_NOISE_MM3 = 0.005


def _try_fillet(shape: Shape, edges: list, radius: float) -> tuple[Shape, float | None]:
    """Return (shape, applied_radius); None when no radius builds.

    Tries the requested radius first, then steps down by 0.25 mm. OCCT's
    max_fillet search throws on these shapes, so it is not used: it made the
    original script skip fillets that build at full size (LID_EDGE 0.8).
    """
    if not edges:
        return shape, None
    steps = [radius]
    step = radius - FILLET_STEP
    while step >= FILLET_STEP - 1e-9:
        steps.append(round(step, 6))
        step -= FILLET_STEP
    solids = list(shape.solids())
    if len(solids) != 1:
        return shape, None
    for use in steps:
        try:
            result = solids[0].fillet(use, edges)
        except Exception:
            continue
        if result.is_valid and len(result.solids()) == 1:
            return result, use
    return shape, None


def _fillet_note(label: str, wanted: float, applied: float | None) -> str:
    if applied is None:
        return f"{label} {wanted}: no radius builds; left sharp"
    if applied + 1e-6 < wanted:
        return f"{label} {wanted}: largest that builds is {applied:.2f}"
    return f"{label} {wanted} applied"


def _overlap_volume(a: Shape, b: Shape) -> float:
    common = a.intersect(b)
    if common is None:
        return 0.0
    total = 0.0
    try:
        for solid in common.solids():
            total += float(solid.volume)
    except Exception:
        volume = getattr(common, "volume", None)
        if volume:
            total += float(volume)
    return total


def _first_solid(shape: Any, name: str) -> Solid:
    if shape is None:
        raise CheckFail(f"{name}: empty boolean")
    if isinstance(shape, Solid) and shape._wrapped is not None:
        return shape
    solids = list(shape.solids())
    if len(solids) != 1:
        raise CheckFail(f"{name}: expected one solid, got {len(solids)}")
    if not solids[0].is_valid:
        raise CheckFail(f"{name}: solid is not valid")
    return solids[0]


def _cap_solid(path: PathGeom, u: float, s: float) -> Shape:
    """Spherical cap Ø4.7 × 1.35 standing to −Y from the medial face."""
    radius = sphere_cap_radius(CONTACT_DOME_DIA, CONTACT_DOME_CROWN)
    origin = _vec(path, u, s, 0.0)
    # Centre sits inside the wall so the crown points to −Y.
    center_y = radius - CONTACT_DOME_CROWN
    sphere = Sphere(radius).locate(Location((origin.X, center_y, origin.Z)))
    # Keep the cap plus 0.3 mm of root so the fuse has overlap.
    keep_h = CONTACT_DOME_CROWN + 0.3
    slab = Box(CONTACT_DOME_DIA + 1.0, keep_h, CONTACT_DOME_DIA + 1.0)
    slab = slab.locate(Location((origin.X, 0.3 - keep_h / 2.0, origin.Z)))
    return _first_solid(sphere.intersect(slab), "mock_contact")


def build_coupon() -> Shape:
    _require_cad()
    sketch = (
        Rectangle(COUPON_XY, COUPON_XY)
        - Pos(-3.0, -3.0) * Circle(1.7 / 2.0)
        - Pos(0.0, -3.0) * Circle(CONTACT_HOLE / 2.0)
        - Pos(3.0, -3.0) * Circle(3.4 / 2.0)
        - Pos(0.0, 2.0) * Rectangle(6.0, 0.9)
        - Pos(0.0, 4.0) * Rectangle(6.0, 0.4)
    )
    plate = extrude(sketch.faces()[0], amount=COUPON_Z)
    # E4 rib: a standing fin 0.4 thick × 3 tall × 12 long on the top face,
    # between the hole row and the slots. It was a 12 × 3 plate 0.4 thick
    # lying flat, 0.2 proud of the top, which measures no thin feature.
    thick, tall, length = COUPON_RIB
    rib = Box(length, thick, tall + 0.2).locate(
        Location((0.0, -0.5, COUPON_Z + tall / 2.0 - 0.1))
    )
    return _one_solid(plate.fuse(rib), "coupon")


def _tab_envelope_solid(
    path: PathGeom,
    cu: float,
    cs: float,
    angle_deg: float,
    a0: float,
    a1: float,
    tab_w: float,
    y0: float,
    y1: float,
) -> Shape:
    """Reserved-air tab from keep-out radius a0 to barrel end a1, in XYZ."""
    rad = math.radians(angle_deg)
    length = max(a1 - a0, 0.05)
    height = max(y1 - y0, 0.05)
    a = angle_at(path, cs)
    radial = Vector(math.cos(a), 0.0, math.sin(a))
    tangent = Vector(math.sin(a), 0.0, -math.cos(a))
    tab_dir = (radial * math.cos(rad) + tangent * math.sin(rad)).normalized()
    mid_u = cu + ((a0 + a1) / 2.0) * math.cos(rad)
    mid_s = cs + ((a0 + a1) / 2.0) * math.sin(rad)
    mid = _vec(path, mid_u, mid_s, (y0 + y1) / 2.0)
    across = tab_dir.cross(Vector(0.0, 1.0, 0.0))
    if across.length < 1e-9:
        across = Vector(0.0, 0.0, 1.0)
    plane = Plane(origin=mid, x_dir=tab_dir, z_dir=across.normalized())
    return plane * Box(length, height, tab_w)


def _as_compound(shape: Any) -> Shape:
    """intersect() can return a ShapeList; boolean ops need one Shape."""
    if isinstance(shape, Shape):
        return shape
    return Compound(list(shape.solids()) if hasattr(shape, "solids") else list(shape))


def _y_cylinder(x: float, y0: float, z: float, radius: float, height: float) -> Shape:
    plane = Plane(origin=Vector(x, y0, z), z_dir=Vector(0.0, 1.0, 0.0))
    return Solid.make_cylinder(radius, height, plane)


def _cable_exit_solid(path: PathGeom, params: Mapping[str, Any]) -> Shape:
    """Ø2.0 along the in-plane normal through P(BODY_WIDTH, CABLE_EXIT_S, 3), ±3 mm."""
    s_exit = cable_exit_s(params)
    exit_pt = _vec(path, float(params["BODY_WIDTH"]), s_exit, CABLE_EXIT_Y)
    a = angle_at(path, s_exit)
    normal = Vector(math.cos(a), 0.0, math.sin(a))
    exit_plane = Plane(
        origin=Vector(exit_pt.X - 3.0 * normal.X, exit_pt.Y, exit_pt.Z - 3.0 * normal.Z),
        z_dir=normal,
    )
    return Solid.make_cylinder(CABLE_EXIT_DIA / 2.0, 6.0, exit_plane)


def _signal_sites(params: Mapping[str, Any]) -> tuple[tuple[str, tuple[float, float]], ...]:
    return (
        ("SIG1", contact_1_us(params)),
        ("SIG2", (float(params["CONTACT_2_U"]), float(params["CONTACT_2_S"]))),
    )


def _keepout_signal_solid(path: PathGeom, params: Mapping[str, Any], site: tuple[float, float]) -> Shape:
    """Reserved air: Ø7.1 from the floor top to the stack top 4.13 (not cut)."""
    wall = float(params["WALL_MEDIAL"])
    origin = _vec(path, float(site[0]), float(site[1]), 0.0)
    y0 = wall + ENVELOPE_LIFT
    return _y_cylinder(origin.X, y0, origin.Z, KEEPOUT_SIGNAL_DIA / 2.0, KEEPOUT_TOP_Y - y0)


def _tab_solid(path: PathGeom, params: Mapping[str, Any], name: str, site: tuple[float, float]) -> Shape:
    """Reserved air: TE 31428 flat tab, Ø7.1 edge to 8.85, TAB_HEIGHT tall (not cut)."""
    pl = load_placement()
    wall = float(params["WALL_MEDIAL"])
    return _tab_envelope_solid(
        path,
        float(site[0]),
        float(site[1]),
        float(params["TAB_DEG"][name]),
        float(pl.KEEPOUT_R),
        float(pl.LUG_A1),
        float(pl.TAB_W),
        wall + ENVELOPE_LIFT,
        wall + tab_height(params),
    )


def _cut_stage_b_contacts(
    body: Shape,
    path: PathGeom,
    params: Mapping[str, Any],
    path_solid: Callable[..., Shape],
) -> tuple[Shape, dict[str, Any]]:
    """Plan §3.5 step 5 Stage B: pocket, holes, channel, cable exit.

    Returns the cut body and what each cut removed, measured on the body
    before that cut (the Stage B checks read it). Keep-out cylinders and tab
    envelopes are reserved air: they are not cut, so nylon inside them shows
    up as overlap instead of being carved away silently.
    """
    wall = float(params["WALL_MEDIAL"])
    lid_y = float(params["LID_Y"])
    thick = float(params["BODY_THICK"])
    hole_r = CONTACT_HOLE / 2.0
    cu0, cu1 = cavity_u(params)
    cs0, cs1 = cavity_s(params)
    cref = contact_ref_us(params)
    measure: dict[str, Any] = {"hole_removed_mm3": {}}

    pocket_c = _vec(path, cref[0], cref[1], 0.0)
    pocket = _y_cylinder(pocket_c.X, wall, pocket_c.Z, POCKET_DIA / 2.0, lid_y - wall + 0.2)
    measure["pocket_removed_mm3"] = round(_overlap_volume(body, pocket), 4)
    body = body.cut(pocket)
    # Hole tool: below the medial face to just above the floor top, so the
    # removed volume is the wall disc and nothing else.
    for name, (u, s) in (*_signal_sites(params), ("REF", cref)):
        origin = _vec(path, float(u), float(s), 0.0)
        hole = _y_cylinder(origin.X, -0.5, origin.Z, hole_r, wall + 0.5 + ENVELOPE_LIFT * 10.0)
        measure["hole_removed_mm3"][name] = round(_overlap_volume(body, hole), 4)
        body = body.cut(hole)
    if stage_is_shell(params):
        # Review r6: the v1 REF wire channel (1.6 × 1.6 through the end wall
        # above the Q59 slot) and the Ø2.0 bench-cable exit through the
        # posterior wall serve v1's wired contacts. The shell carries the
        # REF flex tab in REF_end_wall_slot and has no external cable, so
        # neither is cut (plan v2 §7: nothing outside but the domes and the
        # port). Stage B (no STAGE=shell) is unchanged.
        measure["exit_removed_mm3"] = 0.0
        measure["exit_nylon_in_cavity_mm3"] = 0.0
        measure["shell_skipped"] = "v1 REF wire channel and bench-cable exit"
        return body, measure
    ws0, ws1 = wire_s_pair(params)
    channel = path_solid(WIRE_U[0], WIRE_U[1], ws0, ws1, WIRE_Y[0], WIRE_Y[1])
    body = body.cut(channel)
    cable = _cable_exit_solid(path, params)
    inside = path_solid(-1.0, cu1 - ENVELOPE_LIFT, cs0, cs1, 0.0, thick + 1.0)
    measure["exit_removed_mm3"] = round(_overlap_volume(body, cable), 4)
    measure["exit_nylon_in_cavity_mm3"] = round(_overlap_volume(cable, _as_compound(body.intersect(inside))), 4)
    body = body.cut(cable)
    return body, measure


def _bisect(inside: Callable[[float], bool], lo: float, hi: float, tol: float = 1e-4) -> float:
    """Boundary between lo and hi, where inside(lo) != inside(hi)."""
    at_lo = inside(lo)
    if inside(hi) == at_lo:
        raise CheckFail(f"probe: no boundary between {lo} and {hi}")
    while abs(hi - lo) > tol:  # review r6: descending ranges bisect too
        mid = (lo + hi) / 2.0
        if inside(mid) == at_lo:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def _inside_uys(solid: Solid, path: PathGeom, u: float, s: float, y: float) -> bool:
    x, yy, z = p_xyz(path, u, s, y)
    return bool(solid.is_inside(Vector(x, yy, z)))


def _min_y_in(shape: Shape, tool: Shape) -> float | None:
    common = shape.intersect(tool)
    if common is None:
        return None
    solids = list(common.solids()) if hasattr(common, "solids") else []
    if not solids or sum(float(s.volume) for s in solids) <= OVERLAP_NOISE_MM3:
        return None
    return min(float(s.bounding_box().min.Y) for s in solids)


def _route_turn_slack(points: list[tuple[float, float]], bend_r: float) -> float:
    """Smallest (segment length − the two tangent lengths a bend of radius
    bend_r needs at its ends), in the body-frame XZ plane. A vertex that
    turns less than ROUTE_STRAIGHT_DEG is not a bend: a constant-u run such
    as the channel to s 37 is a radius-105 arc in XZ, about 1° per vertex."""
    merged = [points[0]]
    for i in range(1, len(points) - 1):
        a = (points[i][0] - merged[-1][0], points[i][1] - merged[-1][1])
        b = (points[i + 1][0] - points[i][0], points[i + 1][1] - points[i][1])
        cos_t = (a[0] * b[0] + a[1] * b[1]) / (math.hypot(*a) * math.hypot(*b))
        if math.degrees(math.acos(max(-1.0, min(1.0, cos_t)))) >= ROUTE_STRAIGHT_DEG:
            merged.append(points[i])
    points = merged + [points[-1]]
    if len(points) < 2:
        return math.inf
    lengths = [math.dist(points[i], points[i + 1]) for i in range(len(points) - 1)]
    tangents = [0.0] * len(points)
    for i in range(1, len(points) - 1):
        a = (points[i][0] - points[i - 1][0], points[i][1] - points[i - 1][1])
        b = (points[i + 1][0] - points[i][0], points[i + 1][1] - points[i][1])
        cos_t = (a[0] * b[0] + a[1] * b[1]) / (math.hypot(*a) * math.hypot(*b))
        theta = math.acos(max(-1.0, min(1.0, cos_t)))
        tangents[i] = bend_r * math.tan(theta / 2.0) if theta < math.pi - 1e-9 else math.inf
    return min(lengths[i] - tangents[i] - tangents[i + 1] for i in range(len(lengths)))


def run_stage_b_solid_checks(
    body: Solid,
    lid: Solid,
    path: PathGeom,
    params: Mapping[str, Any],
    cuts: Mapping[str, Any],
    *,
    raise_on_fail: bool = True,
) -> list[Check]:
    """Stage B checks measured on the built body and seated lid (body frame).

    Every named check is recorded. Afterwards every failing check except
    Q21_REF_lug raises one CheckFail that lists each failure and its numbers.
    ``cuts`` is what ``_cut_stage_b_contacts`` measured before each cut.
    """
    checks: list[Check] = []

    def record(name: str, passed: bool, detail: str, **numbers: float) -> None:
        row = Check(name, bool(passed), detail, numbers)
        # A shell row supersedes the Stage B row of the same name in place,
        # so the manifest lists each check once (review r6).
        for i, old in enumerate(checks):
            if old.name == name:
                checks[i] = row
                return
        checks.append(row)

    noise = OVERLAP_NOISE_MM3
    wall = float(params["WALL_MEDIAL"])
    width = float(params["BODY_WIDTH"])
    lid_y = float(params["LID_Y"])
    cu0, cu1 = cavity_u(params)
    cs0, _cs1 = cavity_s(params)
    bs0, bs1 = board_zone_s(params)
    cref = contact_ref_us(params)
    pl = load_placement()

    # Floor and wall faces, probed on the solid.
    u_mid = (cu0 + cu1) / 2.0
    s_batt = (cs0 + RIB_S[0]) / 2.0
    floor_y = _bisect(lambda y: _inside_uys(body, path, u_mid, s_batt, y), 0.5, 2.5)

    # CONTACT_HOLE_wall: each hole removed the floor disc and nothing else.
    disc = math.pi * (CONTACT_HOLE / 2.0) ** 2 * wall
    removed = dict(cuts["hole_removed_mm3"])
    open_at = {
        name: not _inside_uys(body, path, float(u), float(s), wall / 2.0)
        for name, (u, s) in (*_signal_sites(params), ("REF", cref))
    }
    record(
        "CONTACT_HOLE_wall",
        all(abs(v - disc) <= HOLE_VOLUME_TOL * disc for v in removed.values())
        and all(open_at.values()),
        "each Ø2.9 hole removed the 1.5 medial wall disc only (removed volume = disc) and is open",
        wall_disc_mm3=round(disc, 4),
        **{f"removed_{k}_mm3": v for k, v in removed.items()},
        **{f"open_{k}": 1.0 if v else 0.0 for k, v in open_at.items()},
    )

    # KEEPOUT_SIGNAL_air and TAB_envelope_air: reserved air, never cut.
    keep = {}
    tabs = {}
    for name, site in _signal_sites(params):
        k = _keepout_signal_solid(path, params, site)
        keep[f"{name}_body_mm3"] = round(_overlap_volume(body, k), 4)
        keep[f"{name}_lid_mm3"] = round(_overlap_volume(lid, k), 4)
        tab = _tab_solid(path, params, name, site)
        tabs[f"{name}_body_mm3"] = round(_overlap_volume(body, tab), 4)
        tabs[f"{name}_lid_mm3"] = round(_overlap_volume(lid, tab), 4)
    record(
        "KEEPOUT_SIGNAL_air",
        all(v <= noise for v in keep.values()),
        "Ø7.1 keep-outs from the floor to 4.13 hold no nylon (body or lid)",
        **keep,
    )
    if packing_is_v2(params):
        record(
            "TAB_envelope_air",
            False,
            "NOT_MEASURED: v2 flex tabs are not the TE 31428 envelope; see V2_TAB_envelope",
            TAB_HEIGHT=tab_height(params),
        )
    else:
        record(
            "TAB_envelope_air",
            all(v <= noise for v in tabs.values()),
            "TE 31428 tab envelopes 1.96 wide × TAB_HEIGHT, Ø7.1 edge to 8.85, hold no nylon",
            TAB_HEIGHT=tab_height(params),
            **tabs,
        )

    # KEEPOUT_REF_air: pocket air, lid out of it, a ≥ 1.0 wall band around it.
    pocket_c = _vec(path, cref[0], cref[1], 0.0)
    r_pocket = POCKET_DIA / 2.0
    pocket = _y_cylinder(pocket_c.X, wall + ENVELOPE_LIFT, pocket_c.Z, r_pocket, lid_y - wall - 2 * ENVELOPE_LIFT)
    band_missing = 0.0
    for y0, y1 in ((wall, WIRE_Y[0]), (WIRE_Y[1], lid_y)):
        y0, y1 = y0 + ENVELOPE_LIFT, y1 - ENVELOPE_LIFT
        if y1 <= y0:
            continue
        ring = _y_cylinder(pocket_c.X, y0, pocket_c.Z, r_pocket + 1.0, y1 - y0).cut(
            _y_cylinder(pocket_c.X, y0 - 0.1, pocket_c.Z, r_pocket, y1 - y0 + 0.2)
        )
        band_missing += float(ring.volume) - _overlap_volume(body, ring)
    ref = {
        "pocket_body_mm3": round(_overlap_volume(body, pocket), 4),
        "pocket_lid_mm3": round(_overlap_volume(lid, pocket), 4),
        "wall_band_1mm_missing_mm3": round(band_missing, 4),
        "pocket_removed_mm3": float(cuts["pocket_removed_mm3"]),
    }
    record(
        "KEEPOUT_REF_air",
        ref["pocket_body_mm3"] <= noise
        and ref["pocket_lid_mm3"] <= noise
        and ref["wall_band_1mm_missing_mm3"] <= BAND_NOISE_MM3,
        "Ø7.5 pocket from the floor to LID_Y is air, the lid stays out, and nylon at least "
        "1.0 thick surrounds it above and below the channel",
        **ref,
    )

    # BOARD_underside_clear: pad tops against stack, barrels and envelopes.
    pad_tops = []
    for pu in (cu0 + PAD_SIZE / 2.0, cu1 - PAD_SIZE / 2.0):
        for ps in (bs0 + PAD_SIZE / 2.0, bs1 - PAD_SIZE / 2.0):
            pad_tops.append(_bisect(lambda y, pu=pu, ps=ps: _inside_uys(body, path, pu, ps, y), 2.5, 6.0))
    board_y = min(pad_tops)
    stack_top = max(SCREW_LENGTH, floor_y + STACK_LUG + STACK_NUT) + STACK_KAPTON
    barrel_top = floor_y + BARREL_HEIGHT
    envelope_top = floor_y + tab_height(params)
    record(
        "BOARD_underside_clear",
        board_y > stack_top and board_y > barrel_top and board_y > envelope_top,
        "board underside (lowest pad top) above the stack top, both barrels and the tab envelopes",
        board_underside=round(board_y, 4),
        floor_y=round(floor_y, 4),
        stack_top=round(stack_top, 4),
        barrel_top=round(barrel_top, 4),
        envelope_top=round(envelope_top, 4),
        TAB_HEIGHT=tab_height(params),
    )

    # REF_WIRE_envelope: Ø1.3 along the placement route, or the v2 REF flex tab.
    if packing_is_v2(params):
        v2 = pl._v2()
        spec = v2_spec(params)
        layout_v2 = v2.run_spec(spec)
        if spec.iface == "I" or "REF" not in layout_v2.tabs:
            record(
                "REF_WIRE_envelope",
                False,
                "NOT_MEASURED: interface I has no flex REF tab (gold pad on the standoff top)",
                iface=0.0 if spec.iface == "I" else 1.0,
            )
        else:
            tab = layout_v2.tabs["REF"]
            y0, y1 = v2.FLOOR_Y + ENVELOPE_LIFT, v2.FLOOR_Y + v2.TAB_T
            tab_shape = None
            for box in v2._tab_boxes(tab, y0, y1):
                piece = path_solid_for(path, params)(box.u0, box.u1, box.s0, box.s1, y0, y1)
                tab_shape = piece if tab_shape is None else tab_shape.fuse(piece)
            ref_tab = {
                "body_mm3": round(_overlap_volume(body, tab_shape), 4) if tab_shape is not None else -1.0,
                "lid_mm3": round(_overlap_volume(lid, tab_shape), 4) if tab_shape is not None else -1.0,
                "tab_t": v2.TAB_T,
                "tab_w": v2.TAB_W,
            }
            record(
                "REF_WIRE_envelope",
                tab_shape is not None
                and ref_tab["body_mm3"] <= noise
                and ref_tab["lid_mm3"] <= noise,
                f"v2 REF flex tab {v2.TAB_W:g} wide × {v2.TAB_T:g} thick along the ring-to-board path holds no nylon",
                **ref_tab,
            )
    else:
        layout = pl.get_layout(str(params["PACKING"]))
        route = [(float(u), float(s)) for u, s in layout.ref_wire]
        wire_r = float(pl.WIRE_OD) / 2.0
        wire_y = (WIRE_Y[0] + WIRE_Y[1]) / 2.0
        pts = [_vec(path, u, s, wire_y) for u, s in route]
        wire: Shape | None = None
        for i in range(len(pts) - 1):
            seg = pts[i + 1] - pts[i]
            piece = Solid.make_cylinder(wire_r, seg.length, Plane(origin=pts[i], z_dir=seg.normalized()))
            wire = piece if wire is None else wire.fuse(piece)
        for p in pts[1:-1]:
            wire = wire.fuse(Solid.make_sphere(wire_r, Plane(origin=p)))
        cell_box = _cell_box(path, params, floor_y)
        others = {
            "body_mm3": _overlap_volume(body, wire),
            "lid_mm3": _overlap_volume(lid, wire),
            "cell_envelope_mm3": _overlap_volume(cell_box, wire),
        }
        for name, site in _signal_sites(params):
            others[f"keepout_{name}_mm3"] = _overlap_volume(_keepout_signal_solid(path, params, site), wire)
            others[f"tab_{name}_mm3"] = _overlap_volume(_tab_solid(path, params, name, site), wire)
        lid_under = min(
            _bisect(lambda y, u=u, s=s: _inside_uys(lid, path, u, s, y), wire_y, lid_y + 0.5)
            for u, s in route
        )
        slack = _route_turn_slack([(p.X, p.Z) for p in pts], float(pl.BEND_R))
        wire_numbers = {k: round(v, 4) for k, v in others.items()}
        record(
            "REF_WIRE_envelope",
            all(v <= noise for v in others.values())
            and lid_under - (wire_y + wire_r) > 0.0
            and slack >= 0.0,
            "Ø1.3 wire at y 3.3 from the channel to the REF pad holds no nylon, misses the lid, "
            "cell envelope, keep-outs and tabs, and each turn fits bend radius 3; charge pads "
            "are not placed yet (board out of scope) and the pocket-to-channel turn is Q21",
            wire_od=float(pl.WIRE_OD),
            bend_r=float(pl.BEND_R),
            bend_slack=round(slack, 4),
            lid_gap=round(lid_under - (wire_y + wire_r), 4),
            **wire_numbers,
        )

    # CABLE_EXIT_cavity: pierces the posterior wall into cavity air only.
    s_exit = cable_exit_s(params)
    pierced = not _inside_uys(body, path, (cu1 + width) / 2.0, s_exit, CABLE_EXIT_Y)
    opens = not _inside_uys(body, path, cu1 - 0.3, s_exit, CABLE_EXIT_Y)
    in_cavity_s = cs0 < s_exit - CABLE_EXIT_DIA / 2.0 and s_exit + CABLE_EXIT_DIA / 2.0 < cavity_s(params)[1]
    off_battery = s_exit - CABLE_EXIT_DIA / 2.0 > RIB_S[1]
    if stage_is_shell(params):
        # Review r6: the shell has no bench cable, so no exit is cut; the
        # posterior wall at CABLE_EXIT_S is measured closed instead.
        record(
            "CABLE_EXIT_cavity",
            False,
            "NOT_MEASURED: no bench-cable exit on the shell (plan v2 §7); posterior wall closed at CABLE_EXIT_S",
            CABLE_EXIT_S=s_exit,
            wall_closed=0.0 if pierced else 1.0,
        )
    else:
        record(
            "CABLE_EXIT_cavity",
            pierced and opens and in_cavity_s and off_battery
            and float(cuts["exit_nylon_in_cavity_mm3"]) <= noise,
            "Ø2.0 exit pierces the posterior wall and meets cavity air only "
            "(no pad, rib or battery pocket)",
            CABLE_EXIT_S=s_exit,
            nylon_in_cavity_mm3=float(cuts["exit_nylon_in_cavity_mm3"]),
            removed_mm3=float(cuts["exit_removed_mm3"]),
            pierced=1.0 if pierced else 0.0,
            opens_into_cavity=1.0 if opens else 0.0,
            board_side_of_rib=1.0 if off_battery else 0.0,
        )

    # CELL_envelope: 5.2 × 10.4 × 15.6 plus 0.5 foam, on the floor, centred
    # in the plan pocket reservation, against body and seated lid.
    cell_box = _cell_box(path, params, floor_y)
    s_mid, u_mid_b = (BATTERY_S[0] + BATTERY_S[1]) / 2.0, (BATTERY_U[0] + BATTERY_U[1]) / 2.0
    need_y = CELL_MAX[0] + FOAM_THICK
    cell_u = (u_mid_b - CELL_MAX[1] / 2.0, u_mid_b + CELL_MAX[1] / 2.0)
    cell_s = (s_mid - CELL_MAX[2] / 2.0, s_mid + CELL_MAX[2] / 2.0)
    # Shell USB 9 × 3.5 opens the hook-end wall at u=10, y 1–4.5. Probe the
    # anterior ligament so the end-wall inner face still has a boundary.
    end_probe_u = 4.2 if stage_is_shell(params) else u_mid_b
    end_wall_s = _bisect(lambda s: _inside_uys(body, path, end_probe_u, s, 3.0), 0.2, cell_s[0])
    rib_s = _bisect(lambda s: _inside_uys(body, path, u_mid_b, s, 3.0), cell_s[1], RIB_S[1] - 0.1)
    wall_u0 = _bisect(lambda u: _inside_uys(body, path, u, s_mid, 3.0), 0.2, cell_u[0])
    wall_u1 = _bisect(lambda u: _inside_uys(body, path, u, s_mid, 3.0), cell_u[1], width - 0.2)
    over_cell = path_solid_for(path, params)(cell_u[0], cell_u[1], cell_s[0], cell_s[1], floor_y + need_y, lid_y + 3.0)
    lid_over_cell = _min_y_in(lid, over_cell)
    cell = {
        "body_mm3": round(_overlap_volume(body, cell_box), 4),
        "lid_mm3": round(_overlap_volume(lid, cell_box), 4),
        "floor_y": round(floor_y, 4),
        "need_y": round(need_y, 4),
        "clear_y_lid": round((lid_over_cell if lid_over_cell is not None else lid_y) - (floor_y + need_y), 4),
        "clear_s_end_wall": round(cell_s[0] - end_wall_s, 4),
        "clear_s_rib": round(rib_s - cell_s[1], 4),
        "clear_u_anterior": round(cell_u[0] - wall_u0, 4),
        "clear_u_posterior": round(wall_u1 - cell_u[1], 4),
        "plan_pocket_clear_y": round(BATTERY_Y[1] - BATTERY_Y[0] - need_y, 4),
        "plan_pocket_clear_u": round(BATTERY_U[1] - BATTERY_U[0] - CELL_MAX[1], 4),
        "plan_pocket_clear_s": round(BATTERY_S[1] - BATTERY_S[0] - CELL_MAX[2], 4),
    }
    record(
        "CELL_envelope",
        cell["body_mm3"] <= noise
        and cell["lid_mm3"] <= noise
        and min(cell["clear_y_lid"], cell["clear_s_end_wall"], cell["clear_s_rib"],
                cell["clear_u_anterior"], cell["clear_u_posterior"]) >= 0.0
        and floor_y + need_y <= BATTERY_Y[1] + 1e-9,
        "cell 5.2 × 10.4 × 15.6 plus 0.5 foam on the lid face (plan §5, Q18) sits in the pocket "
        "clear of body, rib, walls and the seated lid with its emboss",
        **cell,
    )

    # Q21_REF_lug: TE 31428 upright (contacts.md §5.3) against the measured
    # lid underside over the pocket and the measured pocket radius.
    lug_top_y = wall + float(pl.TAB_LEN) + float(pl.LUG_THICK)
    barrel_outer = float(pl.RING_R) + float(pl.TAB_W)
    lid_col = _y_cylinder(pocket_c.X, wall, pocket_c.Z, r_pocket, lid_y + 3.0 - wall)
    lid_over_pocket = _min_y_in(lid, lid_col)
    probe_y = (WIRE_Y[1] + lid_y) / 2.0
    radii = []
    for du, ds in ((1.0, 0.0), (-1.0, 0.0), (0.0, 1.0)):
        radii.append(
            _bisect(
                lambda r, du=du, ds=ds: bool(
                    body.is_inside(Vector(pocket_c.X, probe_y, pocket_c.Z) + _dir_us(path, cref, du, ds) * r)
                ),
                0.5,
                r_pocket + 0.9,
            )
        )
    pocket_r = min(radii)
    lid_under_pocket = lid_over_pocket if lid_over_pocket is not None else math.inf
    if packing_is_v2(params):
        v2 = pl._v2()
        spec = v2_spec(params)
        ring_r = v2.RING_D / 2.0
        hex_r = v2.STANDOFF_CIRCUMR
        stack_top = floor_y + v2.ring_under(spec) + spec.standoff
        record(
            "Q21_REF_lug",
            stack_top < lid_under_pocket and max(ring_r, hex_r) <= pocket_r,
            "v2: ring and brass standoff (hex corners, circumradius 2.9) on the probed floor against "
            "the measured lid over the pocket and the measured pocket radius; no TE 31428 lug (Q21, Q28)",
            stack_top_y=round(stack_top, 4),
            lid_y=round(lid_under_pocket, 3),
            ring_r=round(ring_r, 4),
            standoff_circumr=round(hex_r, 4),
            pocket_r=round(pocket_r, 3),
            floor_y=round(floor_y, 4),
            ring_t=round(v2.ring_under(spec), 4),
            standoff_h=round(spec.standoff, 4),
        )
    else:
        record(
            "Q21_REF_lug",
            lug_top_y < lid_under_pocket and barrel_outer <= pocket_r,
            "reference lug upright (TE 31428) against the lid and the pocket wall (Q21); "
            "recorded, not hidden, and does not stop the write",
            lug_top_y=round(lug_top_y, 4),
            lid_y=round(lid_under_pocket, 3),
            lug_into_lid=round(lug_top_y - lid_under_pocket, 3),
            barrel_outer=round(barrel_outer, 4),
            pocket_r=round(pocket_r, 3),
            barrel_into_wall=round(barrel_outer - pocket_r, 3),
            lug_thick=float(pl.LUG_THICK),
        )

    # CLOSURE_PASSED: E1/E3/E5 present on the solids exactly when the flag is set.
    flag = bool(params.get("CLOSURE_PASSED", False))
    tongue_s = shift_tail_s(params, (LID_TONGUE_S[0] + LID_TONGUE_S[1]) / 2.0)
    tongue_y = lid_y + (LID_TONGUE_Y_OFF[0] + LID_TONGUE_Y_OFF[1]) / 2.0
    tongue_u = (TONGUE_SLOT_U[0] + TONGUE_SLOT_U[1]) / 2.0
    nub_u = nub_u_pair(params)[0]
    present = {
        "tongue": _inside_uys(lid, path, tongue_u, tongue_s, tongue_y),
        "slot": not _inside_uys(body, path, tongue_u, tongue_s, tongue_y),
        "nub": _inside_uys(lid, path, (nub_u[0] + nub_u[1]) / 2.0, (NUB_S[0] + NUB_S[1]) / 2.0, lid_y - NUB / 2.0),
        "lip": _inside_uys(lid, path, (LIP_U[0] + LIP_U[1]) / 2.0, (LIP_S[0] + LIP_S[1]) / 2.0, lid_y - 2.0),
    }
    record(
        "CLOSURE_PASSED",
        all(v == flag for v in present.values()),
        "E1 tongue and slot, E3 nubs and E5 lip on the solids exactly when CLOSURE_PASSED "
        "(plan §3.6: order 2 keeps them only if the order 1 closure test passed)",
        flag=1.0 if flag else 0.0,
        **{k: 1.0 if v else 0.0 for k, v in present.items()},
    )

    if packing_is_v2(params):
        _record_v2_packing_checks(
            record, body, lid, path, params, floor_y, lid_y, width, noise
        )

    nonfatal = set(STAGE_B_NONFATAL)
    if packing_is_v2(params) and not stage_is_shell(params):
        nonfatal.add("REF_WIRE_envelope")
    latest = {c.name: c for c in checks}
    failing = [
        c
        for c in latest.values()
        if not c.passed
        and c.name in STAGE_B_CHECK_NAMES
        and c.name not in nonfatal
        and not str(c.detail).startswith("NOT_MEASURED")
    ]
    if failing and raise_on_fail:
        raise CheckFail(
            "; ".join(
                f"{c.name}: {c.detail} ("
                + ", ".join(f"{k}={v}" for k, v in c.numbers.items())
                + ")"
                for c in failing
            )
        )
    return checks


def _dir_us(path: PathGeom, site: tuple[float, float], du: float, ds: float) -> Vector:
    """Unit body-frame XZ vector along +u (du) or +s (ds) at a site."""
    a = angle_at(path, float(site[1]))
    radial = Vector(math.cos(a), 0.0, math.sin(a))
    tangent = Vector(math.sin(a), 0.0, -math.cos(a))
    return (radial * du + tangent * ds).normalized()


def _record_v2_packing_checks(
    record: Callable[..., None],
    body: Solid,
    lid: Solid,
    path: PathGeom,
    params: Mapping[str, Any],
    floor_y: float,
    lid_y: float,
    width: float,
    noise: float,
) -> None:
    """WP11 envelopes measured on the order-1 construction path (no fork)."""
    v2 = load_placement()._v2()
    spec = v2_spec(params)
    layout = v2.run_spec(spec)
    maker = path_solid_for(path, params)

    def box_solid(box: Any, y0: float | None = None, y1: float | None = None) -> Shape:
        return maker(box.u0, box.u1, box.s0, box.s1, y0 if y0 is not None else box.y0, y1 if y1 is not None else box.y1)

    cell_box = layout.parts["cell"]
    cell_shape = box_solid(cell_box)
    record(
        "V2_CELL_envelope",
        _overlap_volume(body, cell_shape) <= noise and _overlap_volume(lid, cell_shape) <= noise,
        "v2 cell box from the packing layout holds no nylon on the built body or seated lid",
        body_mm3=round(_overlap_volume(body, cell_shape), 4),
        lid_mm3=round(_overlap_volume(lid, cell_shape), 4),
        y0=round(cell_box.y0, 4),
        y1=round(cell_box.y1, 4),
        wu=round(cell_box.wu, 4),
        ws=round(cell_box.ws, 4),
    )
    module = layout.parts["module"]
    mod_shape = box_solid(module)
    ant = layout.antenna
    ant_shape = maker(ant[0], ant[2], ant[1], ant[3], module.y0, lid_y) if ant else None
    record(
        "V2_MODULE_envelope",
        _overlap_volume(body, mod_shape) <= noise and _overlap_volume(lid, mod_shape) <= noise,
        "v2 module box holds no nylon; antenna_body_mm3 is nylon inside the keep-out prism over the board (reported, not gated: the keep-out is no copper, not air)",
        body_mm3=round(_overlap_volume(body, mod_shape), 4),
        lid_mm3=round(_overlap_volume(lid, mod_shape), 4),
        y0=round(module.y0, 4),
        y1=round(module.y1, 4),
        antenna_body_mm3=(
            round(_overlap_volume(body, ant_shape), 4) if ant_shape is not None else -1.0
        ),
    )
    bu, bs = layout.board_u, layout.board_s
    board_shape = maker(bu[0], bu[1], bs[0], bs[1], layout.board_underside, layout.board_top)
    board_body = _overlap_volume(body, board_shape)
    board_lid = _overlap_volume(lid, board_shape)
    record(
        "V2_BOARD_envelope",
        board_body <= noise and board_lid <= noise,
        "v2 board zone from its underside (the standoff tops) to its top holds no nylon, body or lid",
        body_mm3=round(board_body, 4),
        lid_mm3=round(board_lid, 4),
        underside=round(layout.board_underside, 4),
        top=round(layout.board_top, 4),
    )
    if spec.iface == "I" or not layout.tabs:
        record(
            "V2_TAB_envelope",
            False,
            "NOT_MEASURED: interface I has no flex tabs (gold pad on each standoff top)",
            iface=0.0,
        )
    else:
        tab_hits = {}
        for name, tab in layout.tabs.items():
            shape = None
            for box in v2._tab_boxes(tab, v2.FLOOR_Y, v2.FLOOR_Y + v2.TAB_T):
                piece = maker(box.u0, box.u1, box.s0, box.s1, v2.FLOOR_Y, v2.FLOOR_Y + v2.TAB_T)
                shape = piece if shape is None else shape.fuse(piece)
            tab_hits[f"{name}_body_mm3"] = round(_overlap_volume(body, shape), 4) if shape is not None else -1.0
        record(
            "V2_TAB_envelope",
            all(v <= noise for v in tab_hits.values()),
            f"v2 flex tabs {v2.TAB_W:g} × {v2.TAB_T:g} with Ø{v2.RING_D:g} rings, on the floor, hold no nylon",
            **tab_hits,
        )
    if spec.iface == "I":
        stack_top = layout.standoff_top_y
        try:
            lid_at_c1 = _bisect(
                lambda y: _inside_uys(lid, path, v2.CONTACT_1[0], v2.CONTACT_1[1], y),
                stack_top,
                lid_y + 0.8,
            )
            record(
                "V2_CONTACT_STACK",
                stack_top < lid_at_c1,
                "standoff top (board underside) stays under the lid over SIG1",
                floor_y=round(floor_y, 4),
                standoff_h=round(spec.standoff, 4),
                stack_top_y=round(stack_top, 4),
                lid_over_SIG1=round(lid_at_c1, 4),
                boss_top_y=round(layout.boss_top_y, 4),
            )
        except CheckFail as exc:
            record(
                "V2_CONTACT_STACK",
                False,
                f"NOT_MEASURED: lid over SIG1 has no y-boundary ({exc})",
                floor_y=round(floor_y, 4),
                standoff_h=round(spec.standoff, 4),
            )
    else:
        ring_t = v2.ring_under(spec)
        stack_top = floor_y + ring_t + spec.standoff
        tip_depth = v2.tip_below_standoff_top(spec)
        try:
            lid_at_c1 = _bisect(
                lambda y: _inside_uys(lid, path, v2.CONTACT_1[0], v2.CONTACT_1[1], y),
                stack_top,
                lid_y + 0.8,
            )
            record(
                "V2_CONTACT_STACK",
                stack_top < lid_at_c1
                and stack_top <= layout.board_underside + 1e-3
                and tip_depth > 0.0,
                "measured floor + flex ring + brass standoff: top at or under the board underside "
                "and under the lid over SIG1; the screw tip ends inside the standoff",
                floor_y=round(floor_y, 4),
                ring_t=round(ring_t, 4),
                standoff_h=round(spec.standoff, 4),
                stack_top_y=round(stack_top, 4),
                board_underside=round(layout.board_underside, 4),
                lid_over_SIG1=round(lid_at_c1, 4),
                tip_below_top=round(tip_depth, 4),
            )
        except CheckFail as exc:
            record(
                "V2_CONTACT_STACK",
                False,
                f"NOT_MEASURED: lid over SIG1 has no y-boundary ({exc})",
                floor_y=round(floor_y, 4),
                standoff_h=round(spec.standoff, 4),
            )
    mid_u = (layout.cavity_u[0] + layout.cavity_u[1]) / 2.0
    mid_s = (layout.board_s[0] + layout.board_s[1]) / 2.0
    try:
        lid_band = _bisect(lambda y: _inside_uys(lid, path, mid_u, mid_s, y), floor_y + 2.0, lid_y + 1.0)
        record(
            "V2_LID_band",
            abs(lid_band - lid_y) < 0.6,
            "lid underside over the board mid-point, measured on the seated lid",
            lid_underside_y=round(lid_band, 4),
            LID_Y=round(lid_y, 4),
        )
    except CheckFail as exc:
        record(
            "V2_LID_band",
            False,
            f"NOT_MEASURED: lid underside has no y-boundary at board mid ({exc})",
            LID_Y=round(lid_y, 4),
        )
    try:
        # Review r5: the lane probed at y 0.75, inside the 1.5 floor, and
        # read the outer fillet. The side walls are measured at mid cavity.
        probe_y = (floor_y + lid_y) / 2.0
        def in_body(u: float) -> bool:
            return _inside_uys(body, path, u, mid_s, probe_y)

        outer_u0 = _bisect(in_body, -0.5, 0.75)
        inner_u0 = _bisect(in_body, 0.75, 3.0)
        inner_u1 = _bisect(in_body, width - 3.0, width - 0.75)
        outer_u1 = _bisect(in_body, width - 0.75, width + 0.5)
        ant, post = inner_u0 - outer_u0, outer_u1 - inner_u1
        record(
            "V2_WALL_minima",
            min(ant, post) >= float(params["WALL_MEDIAL"]) - 0.05,
            "side walls probed on the body at board mid-s, mid cavity height: each at least the 1.5 wall",
            anterior_wall=round(ant, 4),
            posterior_wall=round(post, 4),
            probe_y=round(probe_y, 4),
            BODY_WIDTH=round(width, 4),
        )
    except CheckFail as exc:
        record(
            "V2_WALL_minima",
            False,
            f"NOT_MEASURED: wall inner face has no u-boundary ({exc})",
            BODY_WIDTH=round(width, 4),
        )
    chord = float(path.chord)
    m1 = float(params["M1"])
    gate = chord + 3.0
    record(
        "V2_TOTAL_CHORD",
        abs(chord - layout.total_chord) < 1e-3,
        "TOTAL_CHORD of the path that built this solid equals the packing layout's",
        packing_TOTAL_CHORD=round(layout.total_chord, 4),
        TOTAL_CHORD=round(chord, 4),
        BODY_ARC=round(float(params["BODY_ARC"]), 4),
        CREASE_BOW=round(float(params["CREASE_BOW"]), 4),
    )
    record(
        "V2_M1_gate",
        m1 + 1e-9 >= gate and chord <= (m1 - 3.0) + 1e-9,
        "M1 versus TOTAL_CHORD + 3 on the built path (Q34 blank, default.toml M1)",
        M1=m1,
        TOTAL_CHORD=round(chord, 4),
        gate=round(gate, 4),
        m1_minus_3=round(m1 - 3.0, 4),
    )
    stand_hits = {}
    for name in ("standoff_SIG1", "standoff_SIG2", "standoff_REF"):
        if name not in layout.parts:
            continue
        shape = box_solid(layout.parts[name])
        stand_hits[f"{name}_body_mm3"] = round(_overlap_volume(body, shape), 4)
    record(
        "V2_STANDOFF",
        bool(stand_hits) and all(v <= noise for v in stand_hits.values()),
        "brass hex standoffs 5 AF from the floor to the standoff top hold no nylon",
        standoff_h=round(spec.standoff, 4),
        top_y=round(layout.standoff_top_y, 4),
        **stand_hits,
    )
    record(
        "V2_ADJUSTMENT",
        False,
        (
            f"NOT_MEASURED on the solid: region ±{layout.adjustment_mm:.2f} = "
            f"4.0 − 2.9 − {v2.PLACEMENT_TOL:g} (JLC floor ±0.3)"
        ),
        region_mm=round(layout.adjustment_mm, 4),
        pad_half=4.0,
        circumradius=2.9,
        placement_tol=v2.PLACEMENT_TOL,
    )
    record(
        "V2_USB_medial",
        False,
        f"NOT_MEASURED: order-1 solid has no medial USB cut; packing reports {layout.usb_wall}",
        recess=v2.USB_RECESS,
        ligament=v2.USB_LIGAMENT,
        plug_x=v2.PLUG_VOLUME[0],
        plug_y=v2.PLUG_VOLUME[1],
        plug_z=v2.PLUG_VOLUME[2],
    )
    record(
        "V2_HARNESS",
        False,
        "NOT_MEASURED: 100 ± 3 mm cell leads are a routed length, not a solid envelope",
        reserve_mm=100.0,
    )
    record(
        "V2_BOSS",
        False,
        (
            "NOT_MEASURED: printed bosses 0.5 below the standoff top are not on the order-1 solid"
            if spec.iface == "I"
            else "NOT_MEASURED: interface II has no board bosses (WP12: the flex rests on the standoff "
            "tops); its retention is WP14's and G7's"
        ),
        boss_top_y=round(layout.boss_top_y, 4),
        drop=v2.BOSS_DROP,
    )
    cellb = layout.parts["cell"]
    bu, bs = layout.board_u, layout.board_s
    under_board = cellb.u1 > bu[0] and cellb.u0 < bu[1] and cellb.s1 > bs[0] and cellb.s0 < bs[1]
    if under_board:
        record(
            "V2_CELL_CLEARANCE",
            False,
            (
                f"NOT_MEASURED on the solid: nominal {layout.nominal_clearance:+.2f} "
                f"deformed {layout.deformed_clearance:+.2f} "
                f"(standoff {spec.standoff:g}, recess {spec.recess:g}, boss drop {v2.BOSS_DROP:g})"
            ),
            nominal=round(layout.nominal_clearance, 4),
            deformed=round(layout.deformed_clearance, 4),
            recess=round(spec.recess, 4),
            floor_web=round(layout.floor_web, 4),
        )
    else:
        record(
            "V2_CELL_CLEARANCE",
            True,
            "the cell sits beside the board (no u-s overlap with the board zone); the under-board "
            "clearance rule does not apply, V2_CELL_envelope measures the cell",
            cell_s1=round(cellb.s1, 4),
            board_s0=round(bs[0], 4),
        )
    try:
        lid_over_module = _bisect(
            lambda y: _inside_uys(lid, path, layout.parts["module"].u, layout.parts["module"].s, y),
            layout.parts["module"].y1 - 1.0,
            lid_y + 1.0,
        )
        module_gap = lid_over_module - layout.parts["module"].y1
        record(
            "V2_STACK",
            module_gap > 0.0,
            "module top (ring + standoff + board + module above the floor) under the lid underside "
            "probed over the module centre",
            stack=round(layout.stack_over_module, 4),
            module_top_y=round(layout.parts["module"].y1, 4),
            lid_over_module=round(lid_over_module, 4),
            module_lid_gap=round(module_gap, 4),
            outer_zero=round(layout.outer_zero, 4),
            outer_lid=round(layout.outer_at_lid, 4),
        )
    except CheckFail as exc:
        record(
            "V2_STACK",
            False,
            f"NOT_MEASURED: lid over the module has no y-boundary ({exc})",
            stack=round(layout.stack_over_module, 4),
        )
    record(
        "V2_RECESS",
        False,
        "NOT_MEASURED: 0.5 floor recess and 1.0 residual web (C15) are not on the order-1 solid",
        recess=round(spec.recess, 4),
        floor_web=round(layout.floor_web, 4),
    )
    if stage_is_shell(params):
        _record_shell_checks(
            record, body, lid, path, params, floor_y, lid_y, width, noise, layout, spec, v2
        )


def _record_shell_checks(
    record: Callable[..., None],
    body: Solid,
    lid: Solid,
    path: PathGeom,
    params: Mapping[str, Any],
    floor_y: float,
    lid_y: float,
    width: float,
    noise: float,
    layout: Any,
    spec: Any,
    v2: Any,
) -> None:
    """Measured shell-v2 rows. Overwrite the Stage B NOT_MEASURED placeholders."""
    maker = path_solid_for(path, params)
    wall = float(params["WALL_MEDIAL"])

    boss_hits: dict[str, float] = {}
    boss_ok = True
    placed = _shell_boss_sites(layout, v2)
    for name, u, s in placed:
        top_inside = _inside_uys(body, path, u + 1.6, s, layout.boss_top_y - 0.15)
        above = _inside_uys(body, path, u + 1.6, s, layout.standoff_top_y - 0.05)
        boss_hits[f"{name}_top_solid"] = 1.0 if top_inside else 0.0
        boss_hits[f"{name}_at_standoff_top"] = 1.0 if above else 0.0
        if not top_inside or above:
            boss_ok = False
    drop = layout.standoff_top_y - layout.boss_top_y
    record(
        "V2_BOSS",
        boss_ok and abs(drop - v2.BOSS_DROP) < 0.05 and bool(boss_hits),
        "board rests on the standoff tops first: printed bosses 0.5 lower, nylon at the boss top, air at the standoff top",
        boss_top_y=round(layout.boss_top_y, 4),
        standoff_top_y=round(layout.standoff_top_y, 4),
        drop=round(drop, 4),
        **boss_hits,
    )

    ring_ok = True
    ring_nums: dict[str, float] = {}
    for label, (u, s) in (
        ("SIG1", contact_1_us(params)),
        ("SIG2", (float(params["CONTACT_2_U"]), float(params["CONTACT_2_S"]))),
        ("REF", contact_ref_us(params)),
    ):
        in_well = not _inside_uys(body, path, u, s, floor_y + v2.ring_under(spec) / 2.0)
        hole_open = not _inside_uys(body, path, u, s, wall / 2.0)
        ring_nums[f"{label}_well_air"] = 1.0 if in_well else 0.0
        ring_nums[f"{label}_hole_open"] = 1.0 if hole_open else 0.0
        if not in_well or not hole_open:
            ring_ok = False
    ring_t = v2.ring_under(spec)
    sites = (
        ("SIG1", contact_1_us(params)),
        ("SIG2", (float(params["CONTACT_2_U"]), float(params["CONTACT_2_S"]))),
        ("REF", contact_ref_us(params)),
    )
    seat_need = 6.0 + 0.10  # flex ring outline Ø6.0, FPC outline ±0.10
    for label, (u, s) in sites:
        seat_r = _radial_air(body, path, u, s, floor_y + ring_t / 2.0, "u", 4.5)
        ring_nums[f"{label}_seat_d"] = round(2.0 * seat_r, 4) if seat_r > 0 else -1.0
        if seat_r <= 0 or 2.0 * seat_r - PRINT_TOL < seat_need - 0.01:
            ring_ok = False
    record(
        "V2_RING_seat",
        ring_ok,
        (
            f"ring-pad seat: air over the floor at each site, Ø2.7 hole through the 1.5 wall, "
            f"seat Ø measured on the solid ≥ Ø{seat_need:g} ring outline + {PRINT_TOL:g} print"
        ),
        ring_t=round(ring_t, 4),
        hole=SHELL_SCREW_HOLE,
        **ring_nums,
    )

    # Captive hex (review r6): a 5 AF prism from the ring to the standoff top
    # holds no nylon, and the well's measured flats and corners give fit at
    # −0.3 and lock at +0.3 print tolerance.
    stand_ok = True
    stand_nums: dict[str, float] = {}
    so_r = _af_circumr(STANDOFF_AF)
    probe_y = floor_y + ring_t + 1.0
    corner_to_corner = 2.0 * so_r
    for label, (u, s) in sites:
        prism = _hex_prism(
            path,
            u,
            s,
            floor_y + ring_t + ENVELOPE_LIFT,
            layout.standoff_top_y - floor_y - ring_t - 2.0 * ENVELOPE_LIFT,
            so_r,
        )
        over = _overlap_volume(body, prism)
        flat = _radial_air(body, path, u, s, probe_y, "s", SHELL_HEX_OUTER_AF / 2.0 - 0.2)
        corner = _radial_air(body, path, u, s, probe_y, "u", _af_circumr(SHELL_HEX_OUTER_AF) - 0.2)
        af = 2.0 * flat
        stand_nums[f"{label}_body_mm3"] = round(over, 4)
        stand_nums[f"{label}_well_af"] = round(af, 4) if flat > 0 else -1.0
        stand_nums[f"{label}_well_corner_r"] = round(corner, 4) if corner > 0 else -1.0
        fit = flat > 0 and af - PRINT_TOL >= STANDOFF_AF - 0.01
        lock = flat > 0 and af + PRINT_TOL < corner_to_corner
        if over > noise or not fit or not lock:
            stand_ok = False
    record(
        "V2_STANDOFF",
        stand_ok,
        (
            f"5 AF brass standoff: prism from the ring to the standoff top holds no nylon; "
            f"well AF − {PRINT_TOL:g} ≥ {STANDOFF_AF:g} (fit) and well AF + {PRINT_TOL:g} < "
            f"{corner_to_corner:.3f} across corners (no turn)"
        ),
        standoff_h=round(spec.standoff, 4),
        top_y=round(layout.standoff_top_y, 4),
        probe_y=round(probe_y, 4),
        **stand_nums,
    )

    usb_u = 10.0
    opening_air = not _inside_uys(
        body, path, usb_u, wall / 2.0, 1.00 + v2.USB_OPENING[1] / 2.0
    )
    plug = maker(
        usb_u - v2.PLUG_VOLUME[0] / 2.0,
        usb_u + v2.PLUG_VOLUME[0] / 2.0,
        -v2.PLUG_VOLUME[2],
        0.0,
        1.00 + v2.USB_OPENING[1] / 2.0 - v2.PLUG_VOLUME[1] / 2.0,
        1.00 + v2.USB_OPENING[1] / 2.0 + v2.PLUG_VOLUME[1] / 2.0,
    )
    plug_cell = 0.0
    if "cell" in layout.parts:
        plug_cell = _overlap_volume(plug, maker(
            layout.parts["cell"].u0, layout.parts["cell"].u1,
            layout.parts["cell"].s0, layout.parts["cell"].s1,
            layout.parts["cell"].y0, layout.parts["cell"].y1,
        ))
    # Review r6: measured, not u_edge − HOOK_ROOT_X. The hook is fused in
    # assemble_shell, so it is built here in the body frame (the export
    # rotates body and hook together by −THETA_DEG) and probed on the face.
    open_u0 = usb_u - v2.USB_OPENING[0] / 2.0
    usb_y0 = 1.00
    usb_y1 = usb_y0 + v2.USB_OPENING[1]
    hook_b = build_hook(params).rotate(Axis.X, float(params["THETA_DEG"]))
    hook_u_max = -1.0e9
    for s_face in (-v2.USB_RECESS, 0.0, wall / 2.0, wall):
        for k in range(15):
            y = usb_y0 + (usb_y1 - usb_y0) * k / 14.0
            if not _inside_uys(hook_b, path, 0.0, s_face, y) and not _inside_uys(
                hook_b, path, float(params.get("HOOK_ROOT_X", 4.0)), s_face, y
            ):
                continue
            lo = 0.0 if _inside_uys(hook_b, path, 0.0, s_face, y) else float(params.get("HOOK_ROOT_X", 4.0))
            try:
                edge = _bisect(lambda uu: _inside_uys(hook_b, path, uu, s_face, y), lo, usb_u)
            except CheckFail:
                continue
            hook_u_max = max(hook_u_max, edge)
    lig_hook = open_u0 - hook_u_max if hook_u_max > -1.0e8 else 99.0
    usb = layout.parts.get("usb")
    face_s = _bisect(
        lambda ss: _inside_uys(body, path, open_u0 + v2.USB_OPENING[0] + v2.USB_LIGAMENT / 2.0, ss, usb_y0 + 1.0),
        -4.0,
        wall / 2.0,
    )
    mouth_recess = (usb.s0 - face_s) if usb is not None else -99.0
    lig_sig1 = contact_1_us(params)[1] - (usb.s1 if usb is not None else 0.0) - _af_circumr(SHELL_HEX_OUTER_AF)
    record(
        "V2_USB_end",
        opening_air
        and plug_cell <= noise
        and lig_hook >= v2.USB_LIGAMENT - 0.05
        and mouth_recess >= v2.USB_RECESS - 0.05,
        (
            "USB-C hook-end end face: opening 9.0 × 3.5 open, receptacle mouth ≥ 1.0 behind the "
            "outer face (measured face vs packing usb box), ligament ≥ 1.5 from the opening to the "
            "hook measured on the face with the hook in the body frame, plug volume clear of the cell"
        ),
        opening_air=1.0 if opening_air else 0.0,
        recess=v2.USB_RECESS,
        outer_face_s=round(face_s, 4),
        receptacle_s0=round(usb.s0, 4) if usb is not None else -99.0,
        receptacle_s1=round(usb.s1, 4) if usb is not None else -99.0,
        mouth_recess=round(mouth_recess, 4),
        hook_u_max_on_face=round(hook_u_max, 4),
        opening_u0=round(open_u0, 4),
        ligament_hook=round(lig_hook, 4),
        ligament_SIG1_collar_s=round(lig_sig1, 4),
        plug_cell_mm3=round(plug_cell, 4),
        plug_x=v2.PLUG_VOLUME[0],
        plug_y=v2.PLUG_VOLUME[1],
        plug_z=v2.PLUG_VOLUME[2],
    )
    record(
        "V2_USB_medial",
        False,
        "NOT_MEASURED: the closer uses the hook-end end face (plan v2 §5.4 fallback); see V2_USB_end",
        recess=v2.USB_RECESS,
    )

    switch_ok = False
    switch_nums: dict[str, float] = {}
    if "switch" in layout.parts:
        sw = layout.parts["switch"]
        try:
            lid_over = _bisect(
                lambda y: _inside_uys(lid, path, sw.u, sw.s, y),
                lid_y - 0.2,
                lid_y + SHELL_SWITCH_RECESS + 0.3,
            )
            membrane = (lid_y + float(params["LID_THICK"])) - lid_over
            # Recess from the underside: lid material starts above lid_y + SHELL_SWITCH_RECESS.
            switch_ok = lid_over >= lid_y + SHELL_SWITCH_RECESS - 0.15 and membrane >= 0.3
            switch_nums = {
                "lid_over_switch": round(lid_over, 4),
                "membrane": round(membrane, 4),
                "recess": SHELL_SWITCH_RECESS,
            }
        except CheckFail:
            switch_nums = {"lid_over_switch": -1.0}
    record(
        "V2_SWITCH_reach",
        switch_ok,
        "blind recess in the lid over the recovery switch, no through-hole",
        **switch_nums,
    )

    # Review r6: measured on the built lid and body. A snap retains only if
    # body nylon sits over its hook (an undercut); the lane's grooves run to
    # lid_y + 0.15, so the lid lifts straight off. The beam is the one built
    # (hangs in y, bends in u), not the SHELL_SNAP_* constants.
    cu0, cu1 = cavity_u(params)
    s_hook = SHELL_SNAP_S0 + 2.5
    snap_nums: dict[str, float] = {}
    undercuts: list[bool] = []
    strains: list[float] = []
    beam_ts: list[float] = []
    for label, u_wall, sign in (("ant", cu0, 1.0), ("post", cu1, -1.0)):
        u_beam = u_wall + 0.43 * sign
        u_hook = u_wall - 0.10 * sign
        try:
            t_lo = _bisect(lambda uu: _inside_uys(lid, path, uu, s_hook - 1.5, lid_y - 0.5), u_beam - 0.6 * sign, u_beam)
            t_hi = _bisect(lambda uu: _inside_uys(lid, path, uu, s_hook - 1.5, lid_y - 0.5), u_beam, u_beam + 0.6 * sign)
            beam_t = abs(t_hi - t_lo)
            beam_bottom = _bisect(lambda yy: _inside_uys(lid, path, u_beam, s_hook - 1.5, yy), lid_y - 2.0, lid_y - 0.2)
            beam_L = lid_y - beam_bottom
            # Deflection to insert: how far the hook stands past the wall face.
            hook_outer = _bisect(lambda uu: _inside_uys(lid, path, uu, s_hook, lid_y - 0.5), u_hook, u_wall - 0.5 * sign)
            deflect = abs(hook_outer - u_wall)
        except CheckFail:
            beam_t = beam_L = deflect = -1.0
        # Undercut: body nylon above the hook, below or at the lid seat.
        over = any(
            _inside_uys(body, path, u_hook, ss, y)
            for ss in (s_hook - 0.6, s_hook, s_hook + 0.6)
            for y in (lid_y - 0.12, lid_y - 0.05, lid_y + 0.05, lid_y + 0.3)
        )
        undercuts.append(over)
        eps = snap_strain(beam_L, beam_t, deflect) if beam_L > 0 else 1.0
        strains.append(eps)
        beam_ts.append(beam_t)
        snap_nums[f"{label}_beam_t"] = round(beam_t, 4)
        snap_nums[f"{label}_beam_L"] = round(beam_L, 4)
        snap_nums[f"{label}_deflection"] = round(deflect, 4)
        snap_nums[f"{label}_strain"] = round(eps, 5)
        snap_nums[f"{label}_undercut"] = 1.0 if over else 0.0
    ts_ = tail_s0(params)
    lip_over = any(
        _inside_uys(body, path, 11.0, ts_ + 1.0, y) for y in (lid_y - 0.05, lid_y + 0.05, lid_y + 0.3)
    )
    snap_nums["hinge_lip_undercut"] = 1.0 if lip_over else 0.0
    closure_ok = (
        all(undercuts)
        and lip_over
        and max(strains) <= 0.04
        and min(beam_ts) >= JLC_MIN_WALL - 0.05
    )
    record(
        "V2_CLOSURE",
        closure_ok,
        (
            "built lid: body nylon over each snap hook and over the hinge lip (undercut), "
            f"beam ≥ JLC {JLC_MIN_WALL:g} wall, strain 1.5·t·y/L² of the built beam ≤ 0.04 (PA12 repeated snap)"
        ),
        jlc_min_wall=JLC_MIN_WALL,
        **snap_nums,
    )

    # Review r6: plan v2 §7 "no planar facet over 3 mm" is probed along the
    # whole lid, not at one station inside the Ø19 crown. At each station
    # the top is sampled 3 mm apart across u; a rise under 0.02 over 3 mm in
    # both directions is a facet. Lid rim R is the built LID_EDGE fillet.
    top_hi = lid_y + float(params["LID_THICK"]) + SHELL_LID_CROWN + 0.8

    def lid_top(uu: float, ss: float) -> float:
        return _bisect(lambda y: _inside_uys(lid, path, uu, ss, y), lid_y + 0.4, top_hi)

    facets = 0
    stations = 0
    crown_min = 1.0e9
    for ss in (4.0, 10.0, 16.0, 22.0, 28.0, 34.0, 40.0):
        try:
            mid_top = lid_top(width / 2.0, ss)
            side_top = lid_top(width / 2.0 - 3.0, ss)
            s_top = lid_top(width / 2.0, ss + 3.0)
        except CheckFail:
            continue
        stations += 1
        rise_u = mid_top - side_top
        rise_s = abs(mid_top - s_top)
        crown_min = min(crown_min, rise_u)
        if rise_u < 0.02 and rise_s < 0.02:
            facets += 1
    rim_r = float(params["LID_EDGE"])
    record(
        "V2_EDGE_radii",
        stations > 0 and facets == 0 and rim_r >= 1.0 - 1e-9,
        (
            "plan v2 §7: no planar facet over 3 mm on the lid (top sampled 3 mm apart at 7 stations), "
            "outside edges R ≥ 1.0 (lid rim is the built LID_EDGE fillet)"
        ),
        stations=float(stations),
        flat_stations=float(facets),
        min_rise_over_3mm=round(crown_min, 4) if stations else -1.0,
        lid_rim_R=rim_r,
        medial_fillet=float(params["FILLET_MEDIAL"]),
    )

    # Snap catch is 0.4 into the 1.5 side wall (residual 1.1). USB ligaments
    # 1.5. Q59 REF_end_wall_slot (packing-v2.md §5 on lane/w3): remaining
    # nylon beside the slot is the 1.05 mm end wall, still ≥ 1.0.
    slot_u = (REF_SLOT_U[0] + REF_SLOT_U[1]) / 2.0
    slot_s = (REF_SLOT_S[0] + REF_SLOT_S[1]) / 2.0
    slot_y = (REF_SLOT_Y[0] + REF_SLOT_Y[1]) / 2.0
    cut_u0 = REF_SLOT_U[0] - REF_SLOT_CLEAR_U
    cut_u1 = REF_SLOT_U[1] + REF_SLOT_CLEAR_U
    slot_open = not _inside_uys(body, path, slot_u, slot_s, slot_y)
    lig_ant = lig_hook
    # Residual side wall behind the snap groove, measured.
    try:
        g_in = _bisect(lambda uu: _inside_uys(body, path, uu, s_hook, lid_y - 0.6), cu0 + 0.05, cu0 - 1.0)
        g_out = _bisect(lambda uu: _inside_uys(body, path, uu, s_hook, lid_y - 0.6), cu0 - 1.0, -0.5)
        snap_residual = abs(g_in - g_out)
    except CheckFail:
        snap_residual = -1.0
    wall_nums: dict[str, float] = {
        "usb_ligament_hook": round(lig_ant, 4),
        "snap_residual": round(snap_residual, 4),
        "WALL_MEDIAL": wall,
        "slot_open": 1.0 if slot_open else 0.0,
        "slot_clear_u_cad": REF_SLOT_CLEAR_U,
        "slot_clear_s_cad": REF_SLOT_CLEAR_S,
        "slot_clear_y_cad": REF_SLOT_CLEAR_Y,
        "slot_pack_vol_mm3": REF_SLOT_PACK_VOL,
    }
    minima_ok = (
        slot_open
        and lig_ant >= v2.USB_LIGAMENT - 0.05
        and snap_residual >= 1.0 - 0.05
    )
    try:
        mid_s = (layout.board_s[0] + layout.board_s[1]) / 2.0
        probe_y = (floor_y + lid_y) / 2.0

        def in_side(u: float) -> bool:
            return _inside_uys(body, path, u, mid_s, probe_y)

        outer_u0 = _bisect(in_side, -0.5, 0.75)
        inner_u0 = _bisect(in_side, 0.75, 3.0)
        inner_u1 = _bisect(in_side, width - 3.0, width - 0.75)
        outer_u1 = _bisect(in_side, width - 0.75, width + 0.5)
        ant, post = inner_u0 - outer_u0, outer_u1 - inner_u1
        wall_nums["anterior_wall"] = round(ant, 4)
        wall_nums["posterior_wall"] = round(post, 4)
        minima_ok = minima_ok and min(ant, post) >= wall - 0.05
    except CheckFail:
        minima_ok = False
        wall_nums["anterior_wall"] = -1.0
        wall_nums["posterior_wall"] = -1.0
    try:
        wall_left = _end_wall_s_thick(body, path, cut_u0 - 0.40, slot_y)
        wall_right = _end_wall_s_thick(body, path, cut_u1 + 0.40, slot_y)
        wall_nums["slot_wall_s_left"] = round(wall_left, 4)
        wall_nums["slot_wall_s_right"] = round(wall_right, 4)
        minima_ok = minima_ok and min(wall_left, wall_right) >= 1.0 - 0.05
    except CheckFail:
        minima_ok = False
        wall_nums["slot_wall_s_left"] = -1.0
        wall_nums["slot_wall_s_right"] = -1.0
    try:
        floor_outer = _bisect(
            lambda y: _inside_uys(body, path, slot_u, slot_s, y), -0.4, 0.7
        )
        floor_inner = _bisect(
            lambda y: _inside_uys(body, path, slot_u, slot_s, y), 0.7, slot_y
        )
        floor_t = floor_inner - floor_outer
        wall_nums["slot_floor_y"] = round(floor_t, 4)
        minima_ok = minima_ok and floor_t >= 1.0 - 0.05
    except CheckFail:
        minima_ok = False
        wall_nums["slot_floor_y"] = -1.0
    try:
        u_left = _bisect(
            lambda u: _inside_uys(body, path, u, slot_s, slot_y), 5.0, slot_u
        )
        u_right = _bisect(
            lambda u: _inside_uys(body, path, u, slot_s, slot_y), slot_u, 12.0
        )
        slot_width = u_right - u_left
        clear_u = (slot_width - (REF_SLOT_U[1] - REF_SLOT_U[0])) / 2.0
        wall_nums["slot_width"] = round(slot_width, 4)
        wall_nums["slot_clear_u"] = round(clear_u, 4)
        minima_ok = minima_ok and clear_u >= REF_SLOT_CLEAR_U - 0.05
    except CheckFail:
        minima_ok = False
        wall_nums["slot_width"] = -1.0
        wall_nums["slot_clear_u"] = -1.0
    record(
        "V2_WALL_minima",
        minima_ok,
        "side walls 1.5; Q59 slot open with remaining end wall and floor ≥ 1.0 beside it; "
        f"flex clearance {REF_SLOT_CLEAR_U:g} mm per side in u on REF_end_wall_slot",
        **wall_nums,
    )

    # Review r6: these were recorded True as constants. They are v1 rows:
    # the E1 flag and the TE 31428 / lug keep-outs, which interface II fills
    # with hex collars by design. The shell's rows are V2_CLOSURE,
    # V2_STANDOFF and V2_RING_seat.
    record(
        "CLOSURE_PASSED",
        False,
        "NOT_MEASURED: v1 E1 flag (Q28, E1 dropped); the shell closure is V2_CLOSURE",
        flag=0.0,
    )
    record(
        "KEEPOUT_SIGNAL_air",
        False,
        "NOT_MEASURED: v1 Ø7.1 TE keep-out; interface II puts the hex collar there (V2_STANDOFF, V2_RING_seat)",
    )
    record(
        "KEEPOUT_REF_air",
        False,
        "NOT_MEASURED: v1 Ø7.5 lug pocket; interface II puts the REF hex collar and the Q59 slot there",
    )


def path_solid_for(path: PathGeom, params: Mapping[str, Any]) -> Callable[..., Shape]:
    split = tail_s0(params)

    def path_solid(u0, u1, s0, s1, y0, y1, **kwargs):
        return _path_solid(path, u0, u1, s0, s1, y0, y1, split_s=split, **kwargs)

    return path_solid


def _cell_box(path: PathGeom, params: Mapping[str, Any], floor_y: float) -> Shape:
    """Cell envelope plus 0.5 foam, centred in the plan pocket reservation."""
    s_mid = (BATTERY_S[0] + BATTERY_S[1]) / 2.0
    u_mid = (BATTERY_U[0] + BATTERY_U[1]) / 2.0
    return path_solid_for(path, params)(
        u_mid - CELL_MAX[1] / 2.0,
        u_mid + CELL_MAX[1] / 2.0,
        s_mid - CELL_MAX[2] / 2.0,
        s_mid + CELL_MAX[2] / 2.0,
        floor_y + ENVELOPE_LIFT,
        floor_y + CELL_MAX[0] + FOAM_THICK,
    )


def _af_circumr(across_flats: float) -> float:
    return across_flats / math.sqrt(3.0)


def _radial_air(
    body: Shape, path: PathGeom, u: float, s: float, y: float, axis: str, reach: float
) -> float:
    """Smallest distance in mm from (u, s) to nylon along ±u or ±s at height y.

    Air at the centre is required. Along s the probe is scaled to arc length
    at radius R + u. Directions with no boundary inside reach are skipped
    (a tab channel); −1.0 when no direction finds one.
    """
    if _inside_uys(body, path, u, s, y):
        return -1.0
    scale = (path.radius + u) / path.radius if axis == "s" else 1.0
    found: list[float] = []
    for sign in (1.0, -1.0):
        if axis == "u":
            fn = lambda d: _inside_uys(body, path, u + sign * d, s, y)  # noqa: E731
        else:
            fn = lambda d: _inside_uys(body, path, u, s + sign * d / scale, y)  # noqa: E731
        try:
            found.append(_bisect(fn, 0.0, reach))
        except CheckFail:
            continue
    return min(found) if found else -1.0


def _hex_prism(
    path: PathGeom,
    u: float,
    s: float,
    y0: float,
    height: float,
    circumr: float,
    *,
    rotation: float = 0.0,
) -> Shape:
    origin = _vec(path, u, s, y0)
    a = angle_at(path, s)
    radial = Vector(math.cos(a), 0.0, math.sin(a))
    plane = Plane(origin=origin, z_dir=Vector(0.0, 1.0, 0.0), x_dir=radial)
    poly = plane * RegularPolygon(circumr, 6, rotation=rotation)
    return extrude(poly.faces()[0], amount=height)


def _tab_channel(path: PathGeom, params: Mapping[str, Any], tab: Any, y0: float, y1: float) -> Shape | None:
    v2 = load_placement()._v2()
    maker = path_solid_for(path, params)
    shape = None
    for box in v2._tab_boxes(tab, y0, y1):
        piece = maker(
            box.u0 - 0.4,
            box.u1 + 0.4,
            box.s0 - 0.4,
            box.s1 + 0.4,
            y0,
            y1,
        )
        shape = piece if shape is None else shape.fuse(piece)
    return shape


def _ref_end_wall_slot(path: PathGeom, params: Mapping[str, Any]) -> Shape:
    """packing-v2.md §5 REF_end_wall_slot plus the stated flex clearance."""
    maker = path_solid_for(path, params)
    return maker(
        REF_SLOT_U[0] - REF_SLOT_CLEAR_U,
        REF_SLOT_U[1] + REF_SLOT_CLEAR_U,
        REF_SLOT_S[0] - REF_SLOT_CLEAR_S,
        REF_SLOT_S[1] + REF_SLOT_CLEAR_S,
        REF_SLOT_Y[0],
        REF_SLOT_Y[1] + REF_SLOT_CLEAR_Y,
    )


def _end_wall_s_thick(body: Solid, path: PathGeom, u: float, y: float) -> float:
    """Remaining nylon in s at (u, y) between the cavity and the tail pocket."""

    def in_body(s: float) -> bool:
        return _inside_uys(body, path, u, s, y)

    inner = _bisect(in_body, 37.4, 38.7)
    outer = _bisect(in_body, 38.7, 40.6)
    return outer - inner


def _apply_shell_features(
    body: Shape,
    lid: Shape,
    path: PathGeom,
    params: Mapping[str, Any],
    notes: dict[str, Any],
) -> tuple[Shape, Shape]:
    """Wearable cuts and bosses on the Stage B v2 solid. Same construction path."""
    v2 = load_placement()._v2()
    spec = v2_spec(params)
    layout = v2.run_spec(spec)
    maker = path_solid_for(path, params)
    wall = float(params["WALL_MEDIAL"])
    lid_y = float(params["LID_Y"])
    lid_thick = float(params["LID_THICK"])
    width = float(params["BODY_WIDTH"])
    floor_y = wall
    cu0, cu1 = cavity_u(params)
    ring_t = v2.ring_under(spec)
    inner_r = _af_circumr(SHELL_HEX_AF)
    outer_r = _af_circumr(SHELL_HEX_OUTER_AF)
    sites = (
        ("SIG1", contact_1_us(params)),
        ("SIG2", (float(params["CONTACT_2_U"]), float(params["CONTACT_2_S"]))),
        ("REF", contact_ref_us(params)),
    )
    measure: dict[str, Any] = {
        "q59_slot": "REF_end_wall_slot",
        "wp11b_route": "none in cavity",
        "q59_clear_u": REF_SLOT_CLEAR_U,
        "q59_clear_s": REF_SLOT_CLEAR_S,
        "q59_clear_y": REF_SLOT_CLEAR_Y,
        "q59_pack_vol_mm3": REF_SLOT_PACK_VOL,
    }

    # Q59: packing-v2.md §5 on lane/w3 at 284ec05. No in-cavity REF route.
    # Cut REF_end_wall_slot (u 7.25–9.75, s 38.20–39.25, y 1.50–1.81) plus
    # the stated flex clearance. Stage B without STAGE=shell is not slotted.
    if spec.iface == "II" and "REF" in layout.tabs:
        pack = maker(
            REF_SLOT_U[0],
            REF_SLOT_U[1],
            REF_SLOT_S[0],
            REF_SLOT_S[1],
            REF_SLOT_Y[0],
            REF_SLOT_Y[1],
        )
        slot = _ref_end_wall_slot(path, params)
        measure["q59_pack_overlap_mm3"] = round(_overlap_volume(body, pack), 4)
        measure["q59_removed_mm3"] = round(_overlap_volume(body, slot), 4)
        body = body.cut(slot)
        notes["q59"] = (
            "packing-v2.md §5 on lane/w3 at 284ec05 (git show 284ec05): "
            "no in-cavity REF tab route; REF_end_wall_slot u 7.25–9.75, "
            "s 38.20–39.25, y 1.50–1.81, width 2.50, through 1.05, height "
            f"0.31, 0.814 mm³, plus flex clearance {REF_SLOT_CLEAR_U:g} mm "
            f"per side in u, {REF_SLOT_CLEAR_S:g} mm in s, {REF_SLOT_CLEAR_Y:g} mm in y"
        )

    for name, (u, s) in sites:
        collar = _hex_prism(path, u, s, floor_y, SHELL_COLLAR_H, outer_r)
        origin = _vec(path, u, s, 0.0)
        well_h = layout.standoff_top_y - floor_y + 0.2
        # Review r6: the well is the 5.30 AF hex alone. The Ø7.4 cylinder the
        # lane cut with it swallowed the hex (circumradius 3.06 < 3.70), so
        # the standoff could turn and the collar flats were 0.2 thick.
        well = _hex_prism(path, u, s, floor_y - 0.05, well_h, inner_r)
        try:
            body = body.fuse(collar).cut(well)
        except Exception as exc:
            raise CheckFail(f"hex pocket {name}: {exc}") from exc
        ring_seat = _y_cylinder(
            origin.X,
            floor_y - 0.02,
            origin.Z,
            SHELL_RING_SEAT_D / 2.0,
            ring_t + 0.05,
        )
        body = body.cut(ring_seat)
        hole = _y_cylinder(
            origin.X,
            -0.6,
            origin.Z,
            SHELL_SCREW_HOLE / 2.0,
            wall + SHELL_COLLAR_H + 1.0,
        )
        body = body.cut(hole)
        cap = _cap_solid(path, u, s)
        body = body.fuse(cap)
        body = body.cut(hole)

    if spec.iface == "II":
        for name, tab in layout.tabs.items():
            # REF uses REF_end_wall_slot plus the exact packing boxes, not
            # the 0.4 floor-channel pad (that pad would widen the slot past
            # the stated clearance).
            if name != "REF":
                channel = _tab_channel(
                    path, params, tab, floor_y + ENVELOPE_LIFT, floor_y + v2.TAB_T + 0.25
                )
                if channel is not None:
                    body = body.cut(channel)
            else:
                # REF: the slot's own clearance from the slot to the ring
                # seat, through the REF collar (review r6: the exact tab box
                # left zero clearance in the collar).
                body = body.cut(
                    maker(
                        REF_SLOT_U[0] - REF_SLOT_CLEAR_U,
                        REF_SLOT_U[1] + REF_SLOT_CLEAR_U,
                        REF_SLOT_S[1],
                        contact_ref_us(params)[1],
                        REF_SLOT_Y[0] - 0.02,
                        REF_SLOT_Y[1] + REF_SLOT_CLEAR_Y,
                    )
                )
            for box in v2._tab_boxes(tab, v2.FLOOR_Y, v2.FLOOR_Y + v2.TAB_T):
                body = body.cut(
                    maker(box.u0, box.u1, box.s0, box.s1, box.y0, box.y1)
                )
    # Review r6: the packing's 5 × 5 standoff boxes are not cut any more;
    # their corners (radius 3.54) opened the hex well past the standoff's
    # corners (2.89) and undid the lock. V2_STANDOFF measures the hex.

    bosses = _shell_boss_sites(layout, v2)
    for name, u, s in bosses:
        boss_h = layout.boss_top_y - floor_y
        origin = _vec(path, u, s, floor_y)
        boss = _y_cylinder(origin.X, floor_y, origin.Z, v2.BOSS_DIA / 2.0, boss_h)
        pilot = _y_cylinder(
            origin.X, floor_y + 0.3, origin.Z, SHELL_PILOT / 2.0, boss_h + 0.2
        )
        body = body.fuse(boss).cut(pilot)
        measure[f"{name}_u"] = round(u, 4)
        measure[f"{name}_s"] = round(s, 4)
    measure["bosses"] = len(bosses)
    measure["boss_top_y"] = round(layout.boss_top_y, 4)
    measure["standoff_top_y"] = round(layout.standoff_top_y, 4)

    # USB-C on the hook-end end face (plan v2 §5.4 fallback). Opening
    # 9.0 × 3.5 through the 1.5 wall; 1.0 recess lives in a 1.0 outer pad
    # so residual wall stays 1.5. Plug volume stays outside (keep-out).
    usb_u = 10.0
    usb_half_u = v2.USB_OPENING[0] / 2.0
    usb_y0 = 1.00
    usb_y1 = usb_y0 + v2.USB_OPENING[1]
    pad_u0 = usb_u - usb_half_u - v2.USB_LIGAMENT
    pad_u1 = usb_u + usb_half_u + v2.USB_LIGAMENT
    pad = maker(pad_u0, pad_u1, -v2.USB_RECESS, 0.05, usb_y0 - 0.4, usb_y1 + 0.4)
    try:
        body = body.fuse(pad)
    except Exception as exc:
        raise CheckFail(f"USB outer pad: {exc}") from exc
    opening = maker(
        usb_u - usb_half_u,
        usb_u + usb_half_u,
        -v2.USB_RECESS - 0.2,
        wall + 0.08,
        usb_y0,
        usb_y1,
    )
    measure["usb_opening_removed_mm3"] = round(_overlap_volume(body, opening), 4)
    body = body.cut(opening)
    recess = maker(
        usb_u - usb_half_u - 0.2,
        usb_u + usb_half_u + 0.2,
        -v2.USB_RECESS - 0.05,
        0.02,
        usb_y0 - 0.2,
        usb_y1 + 0.2,
    )
    body = body.cut(recess)

    # Hinge lip in the tail, past the board. USB occupies the hook-end face.
    # Short in y so it stays above the module (top 7.62) and off the board zone.
    ts = tail_s0(params)
    groove = maker(
        8.0,
        14.0,
        ts + 0.6,
        ts + 1.25,
        lid_y - 0.85,
        lid_y + 0.12,
    )
    body = body.cut(groove)
    # Lip and bump stay in the groove so body and lid interiors stay disjoint.
    lip = maker(8.2, 13.8, ts + 0.65, ts + 1.20, lid_y - 0.50, lid_y + lid_thick)
    lid = lid.fuse(lip)
    bump = maker(8.2, 13.8, ts + 0.85, ts + 1.15, lid_y - 0.50, lid_y - 0.10)
    lid = lid.fuse(bump)

    # Two cantilever snaps on the inner side walls, over the board.
    # Hook sits in the cut groove (air) so body and lid interiors stay disjoint.
    snap_s1 = SHELL_SNAP_S0 + SHELL_SNAP_L
    for u_wall, sign in ((cu0, 1.0), (cu1, -1.0)):
        groove_u0 = u_wall - SHELL_SNAP_CATCH if sign > 0 else u_wall
        groove_u1 = u_wall if sign > 0 else u_wall + SHELL_SNAP_CATCH
        catch = maker(
            groove_u0,
            groove_u1,
            SHELL_SNAP_S0,
            snap_s1,
            lid_y - 1.2,
            lid_y + 0.15,
        )
        body = body.cut(catch)
        beam_u0 = u_wall + 0.18 if sign > 0 else u_wall - 0.68
        beam_u1 = beam_u0 + 0.5
        beam = maker(
            beam_u0,
            beam_u1,
            SHELL_SNAP_S0 + 0.4,
            snap_s1 - 0.4,
            lid_y - SHELL_SNAP_T,
            lid_y + lid_thick,
        )
        hook_u0 = u_wall - 0.18 if sign > 0 else u_wall + 0.02
        hook_u1 = u_wall - 0.02 if sign > 0 else u_wall + 0.18
        hook = maker(
            hook_u0,
            hook_u1,
            SHELL_SNAP_S0 + 1.8,
            SHELL_SNAP_S0 + 3.2,
            lid_y - 0.85,
            lid_y - 0.15,
        )
        # A thin rib keeps the hook on the beam (hook sits in the groove air).
        rib = maker(
            min(hook_u0, beam_u0),
            max(hook_u1, beam_u1),
            SHELL_SNAP_S0 + 1.9,
            SHELL_SNAP_S0 + 3.1,
            lid_y - 0.25,
            lid_y + 0.05,
        )
        lid = lid.fuse(beam).fuse(rib).fuse(hook)

    if "switch" in layout.parts:
        sw = layout.parts["switch"]
        recess = maker(
            sw.u0 - 0.4,
            sw.u1 + 0.4,
            sw.s0 - 0.4,
            sw.s1 + 0.4,
            lid_y,
            lid_y + SHELL_SWITCH_RECESS,
        )
        lid = lid.cut(recess)
        measure["switch_u"] = round(sw.u, 4)
        measure["switch_s"] = round(sw.s, 4)

    # Shallow crown so the lateral lid is not a 3 mm plane (plan v2 §7).
    mid = _vec(path, width / 2.0, 22.0, lid_y + lid_thick)
    crown_r = 90.0
    sphere = Sphere(crown_r).locate(
        Location((mid.X, lid_y + lid_thick - crown_r + SHELL_LID_CROWN, mid.Z))
    )
    slab = maker(-1.0, width + 1.0, -1.0, float(params["BODY_ARC"]) + 1.0, lid_y + lid_thick - 0.05, lid_y + lid_thick + 3.0)
    try:
        bump_lid = sphere.intersect(slab)
        if bump_lid is not None:
            lid = lid.fuse(_as_compound(bump_lid))
            measure["lid_crown"] = SHELL_LID_CROWN
    except Exception:
        measure["lid_crown"] = 0.0

    strain = snap_strain(SHELL_SNAP_L, SHELL_SNAP_T, SHELL_SNAP_Y)
    notes["closure"] = (
        f"hinge lip at the cavity-tail wall plus two cantilever snaps "
        f"L={SHELL_SNAP_L:g} t={SHELL_SNAP_T:g} y={SHELL_SNAP_Y:g} "
        f"strain={strain:.4f} (PA12)"
    )
    notes["shell_measure"] = measure
    notes["winner"] = SHELL_WINNER
    return body, lid


def build_body_and_lid(
    params: Mapping[str, Any],
) -> tuple[Solid, Solid, PathGeom, dict[str, Any]]:
    """Return (body in body frame, lid in body frame, path, notes).

    One construction path (plan §3.5) for the order 1 gauge and Stage B.
    Stage B changes only inputs (packing moves the width, arc, cavity, tail
    and board zone) and step 5 (holes, pocket, channel, cable exit instead
    of mock domes); E1/E3/E5 follow ``lid_experiments``. With the order 1
    parameters every input equals the plan constant, so the order 1 solids
    are the same operations on the same numbers.
    """
    _require_cad()
    notes: dict[str, Any] = {"fillets": []}
    path = make_path(float(params["BODY_ARC"]), float(params["CREASE_BOW"]))
    width = float(params["BODY_WIDTH"])
    thick = float(params["BODY_THICK"])
    lid_y = float(params["LID_Y"])
    wall = float(params["WALL_MEDIAL"])
    fillet_r = float(params["FILLET_MEDIAL"])
    tail_end = float(params["BODY_ARC"])
    split = tail_s0(params)
    cu0, cu1 = cavity_u(params)
    cs0, cs1 = cavity_s(params)
    bs0, bs1 = board_zone_s(params)
    recess_s1 = shift_tail_s(params, LID_RECESS_S1)
    plate_s = shift_tail_pair(params, LID_PLATE_S)
    tongue_slot_s = shift_tail_pair(params, TONGUE_SLOT_S)
    web_pocket_s = shift_tail_pair(params, WEB_POCKET_S)
    lid_tongue_s = shift_tail_pair(params, LID_TONGUE_S)
    lid_web_s = shift_tail_pair(params, LID_WEB_S)
    experiments = lid_experiments(params)

    def path_solid(u0, u1, s0, s1, y0, y1, **kwargs):
        return _path_solid(path, u0, u1, s0, s1, y0, y1, split_s=split, **kwargs)

    def tail_u(s: float) -> tuple[float, float]:
        return _tail_u(s, width, split, tail_end)

    main = path_solid(0.0, width, 0.0, split, 0.0, thick)

    # Body and tail are built sharp and fused. The two plan-view tip corners
    # take TIP_ROUND first, then FILLET_MEDIAL runs along the whole medial
    # outline except the top end. Filleting the tip after the medial fillet
    # capped it at 1.6 (full) and failed on thin; fusing two separately
    # filleted pieces left a 0.03 mm² sliver face the 3MF mesher rejects.
    tail: Shape = _loft_s(path, split, tail_end, tail_u, 0.0, thick, step=1.5)
    body: Shape = main.fuse(tail)
    tip = _vec(path, width / 2.0, tail_end, thick / 2.0)
    vertical = []
    for edge in body.edges():
        delta = Vector(edge @ 1) - Vector(edge @ 0)
        if delta.length < 0.5 * thick or abs(delta.Y) < 0.7 * delta.length:
            continue
        center = edge.center()
        if abs(center.Z - tip.Z) < 4.0 and abs(center.X - tip.X) < 8.0:
            vertical.append(edge)
    if len(vertical) != 2:
        raise CheckFail(f"TIP_ROUND: expected 2 tip corner edges, found {len(vertical)}")
    body, applied = _try_fillet(body, vertical, TIP_ROUND)
    notes["fillets"].append(_fillet_note("§3.5 step 2 tip round", TIP_ROUND, applied))
    medial = [
        e
        for e in body.edges()
        if abs(e.center().Y) < 1e-6 and _approx_s(path, e.center()) > 0.2
    ]
    body, applied = _try_fillet(body, medial, fillet_r)
    notes["fillets"].append(_fillet_note("FILLET_MEDIAL", fillet_r, applied))
    if applied is None or applied + 1e-6 < fillet_r:
        raise CheckFail(f"FILLET_MEDIAL={fillet_r}: medial outline fillet did not build")

    # Lid recess: remove y > LID_Y over s 0–46.8, keep lip zone full thickness.
    recess = path_solid(
        -1.0,
        width + 1.0,
        0.0,
        recess_s1,
        lid_y,
        thick + 4.0,
    )
    body = body.cut(recess)

    cavity = path_solid(
        cu0,
        cu1,
        cs0,
        cs1,
        wall,
        thick + 1.0,
    )
    body = body.cut(cavity)

    rib = path_solid(cu0, cu1, RIB_S[0], RIB_S[1], RIB_Y[0], RIB_Y[1])
    body = body.fuse(rib)
    pad_u = (
        (cu0, cu0 + PAD_SIZE),
        (cu1 - PAD_SIZE, cu1),
    )
    pad_s = (
        (bs0, bs0 + PAD_SIZE),
        (bs1 - PAD_SIZE, bs1),
    )
    for u0, u1 in pad_u:
        for s0, s1 in pad_s:
            pad = path_solid(u0, u1, s0, s1, PAD_Y[0], PAD_Y[1])
            body = body.fuse(pad)

    c1 = contact_1_us(params)
    c2 = (float(params["CONTACT_2_U"]), float(params["CONTACT_2_S"]))
    cref = contact_ref_us(params)
    if params["MOCK_CONTACTS"]:
        for u, s in (c1, c2, cref):
            cap = _cap_solid(path, float(u), float(s))
            body = body.fuse(cap)
    else:
        body, notes["stage_b_cuts"] = _cut_stage_b_contacts(body, path, params, path_solid)

    if experiments:
        groove = path_solid(
            GROOVE_U[0],
            GROOVE_U[1],
            GROOVE_S[0],
            GROOVE_S[1],
            lid_y + GROOVE_Y_OFF[0],
            lid_y + GROOVE_Y_OFF[1],
        )
        body = body.cut(groove)
        slot = path_solid(
            TONGUE_SLOT_U[0],
            TONGUE_SLOT_U[1],
            tongue_slot_s[0],
            tongue_slot_s[1],
            lid_y + TONGUE_SLOT_Y_OFF[0],
            lid_y + TONGUE_SLOT_Y_OFF[1],
        )
        body = body.cut(slot)
        web_pocket = path_solid(
            TONGUE_SLOT_U[0],
            TONGUE_SLOT_U[1],
            web_pocket_s[0],
            web_pocket_s[1],
            lid_y + WEB_POCKET_Y_OFF[0],
            lid_y + WEB_POCKET_Y_OFF[1],
        )
        body = body.cut(web_pocket)

    # Lid plate: plan outline inset CLEAR_FIT, s -0.2 to 46.4 (tail shift on B).
    clear = float(params["CLEAR_FIT"])
    lid_thick = float(params["LID_THICK"])
    plate_main = path_solid(
        clear,
        width - clear,
        plate_s[0],
        split,
        lid_y,
        lid_y + lid_thick,
    )

    def lid_u(s: float) -> tuple[float, float]:
        u0, u1 = tail_u(s)
        return u0 + clear, u1 - clear

    plate_tail = _loft_s(
        path,
        split,
        plate_s[1],
        lid_u,
        lid_y,
        lid_y + lid_thick,
        step=1.5,
    )
    lid: Shape = plate_main.fuse(plate_tail)
    try:
        # The top edge at the lip end (s = −0.2) stays sharp: rounded, it
        # would leave the lip joined to the plate by 0.2 mm of end face.
        rim = [
            e
            for e in lid.edges()
            if abs(e.center().Y - (lid_y + lid_thick)) < 0.15
            and e.length > 2.0
            and abs(_approx_s(path, e.center()) - plate_s[0]) > 0.05
        ]
        lid, applied = _try_fillet(lid, rim, float(params["LID_EDGE"]))
        notes["fillets"].append(
            _fillet_note("LID_EDGE (plate rim except the lip end)", float(params["LID_EDGE"]), applied)
        )
    except Exception as exc:
        raise CheckFail(f"LID_EDGE: rim fillet failed ({exc})") from exc

    if experiments:
        lip_y0 = lid_y + lid_thick - LIP_LENGTH
        lip = path_solid(LIP_U[0], LIP_U[1], LIP_S[0], LIP_S[1], lip_y0, lid_y + lid_thick)
        lid = lid.fuse(lip)
        bump = path_solid(
            LIP_U[0],
            LIP_U[1],
            LIP_S[1],
            LIP_S[1] + BUMP_OUT,
            lip_y0,
            lip_y0 + BUMP_TALL,
        )
        lid = lid.fuse(bump)
        try:
            # The root is the concave edge where the lip's inner face meets the
            # plate underside (s = −0.2, y = LID_Y). Plan §3.5 step 7 asks 0.5;
            # a radius above the 0.2 lip-to-top-face gap overlaps the body's
            # top edge when seated (0.045 mm³ at 0.5), so LIP_ROOT_FILLET is 0.2.
            root_edges = [
                e
                for e in lid.edges()
                if abs(e.center().Y - lid_y) < 0.05
                and abs(_approx_s(path, e.center()) - LIP_S[1]) < 0.05
                and LIP_U[0] - 0.1 < _approx_u(path, e.center()) < LIP_U[1] + 0.1
            ]
            if len(root_edges) != 1:
                raise CheckFail(f"lip root: expected 1 root edge, found {len(root_edges)}")
            lid, applied = _try_fillet(lid, root_edges, LIP_ROOT_FILLET)
            notes["fillets"].append(_fillet_note("lip root fillet", LIP_ROOT_FILLET, applied))
        except CheckFail:
            raise
        except Exception as exc:
            raise CheckFail(f"lip root fillet failed ({exc})") from exc

        tongue_u0 = (TONGUE_SLOT_U[0] + TONGUE_SLOT_U[1] - LID_TONGUE_WIDTH) / 2.0
        tongue_u1 = tongue_u0 + LID_TONGUE_WIDTH
        web = path_solid(
            tongue_u0,
            tongue_u1,
            lid_web_s[0],
            lid_web_s[1],
            lid_y + LID_WEB_Y_OFF[0],
            lid_y + LID_WEB_Y_OFF[1],
        )
        tongue = path_solid(
            tongue_u0,
            tongue_u1,
            lid_tongue_s[0],
            lid_tongue_s[1],
            lid_y + LID_TONGUE_Y_OFF[0],
            lid_y + LID_TONGUE_Y_OFF[1],
        )
        lid = lid.fuse(web).fuse(tongue)
        for u0, u1 in nub_u_pair(params):
            nub = path_solid(u0, u1, NUB_S[0], NUB_S[1], lid_y - NUB, lid_y)
            lid = lid.fuse(nub)
    else:
        notes["closure"] = "E1/E3/E5 omitted; CLOSURE_PASSED is false"

    if stage_is_shell(params):
        body, lid = _apply_shell_features(body, lid, path, params, notes)

    if stage_is_shell(params):
        notes["emboss"] = "none (plan v2 §7: no text outside)"
    else:
        label = emboss_label(params, list(params.get("_defaults_used", [])))
        # Order 1 embosses 0.8 at s 28. Stage B (Q11): 0.4 over the battery zone.
        emboss_s = 28.0 if params["MOCK_CONTACTS"] else STAGE_B_EMBOSS_S
        emboss_h = EMBOSS if params["MOCK_CONTACTS"] else STAGE_B_EMBOSS
        try:
            if not FONT_PATH.is_file():
                raise CheckFail(f"emboss font missing: {FONT_PATH}")
            mid = _vec(path, width / 2.0, emboss_s, lid_y)
            plane = Plane(
                origin=Vector(mid.X, lid_y, mid.Z),
                x_dir=Vector(0, 0, -1),
                y_dir=Vector(1, 0, 0),
            )
            text = plane * Text(label, font_size=1.4, font_path=str(FONT_PATH))
            letters = extrude(text, amount=emboss_h)
            lid = lid.fuse(letters)
            notes["emboss"] = label
            notes["emboss_font"] = FONT_PATH.name
            if not params["MOCK_CONTACTS"]:
                notes["emboss_s"] = emboss_s
                notes["emboss_h"] = emboss_h
        except CheckFail:
            raise
        except Exception as exc:
            raise CheckFail(f"EMBOSS={label!r}: text did not build ({exc})") from exc

    body_solid = _one_solid(body, "body")
    lid_solid = _one_solid(lid, "lid")
    return body_solid, lid_solid, path, notes


def _approx_s(path: PathGeom, point: Vector) -> float:
    """Invert P for s at y-ignored; nearest station by angle."""
    dx = point.X - path.cx
    dz = point.Z - path.cz
    a = math.atan2(dz, dx)
    return (path.a0 - a) * path.radius


def _approx_u(path: PathGeom, point: Vector) -> float:
    dx = point.X - path.cx
    dz = point.Z - path.cz
    return math.hypot(dx, dz) - path.radius


def build_hook(params: Mapping[str, Any]) -> Shape:
    _require_cad()
    hook_radius = float(params["HOOK_RADIUS"])
    hook_dia = float(params["HOOK_DIA"])
    root = Vector(float(params.get("HOOK_ROOT_X", 4.0)), float(params["HOOK_ROOT_Y"]), 0.0)
    center = Vector(root.X - hook_radius, root.Y, 0.0)
    start = math.radians(HOOK_EMBED_DEG)
    arc = float(params["HOOK_ANGLE"]) - HOOK_EMBED_DEG
    if stage_is_shell(params):
        faces: list[Face] = []
        count = 7
        for i in range(count):
            t = i / (count - 1)
            a = start + math.radians(arc) * t
            pos = Vector(
                center.X + hook_radius * math.cos(a),
                center.Y,
                center.Z + hook_radius * math.sin(a),
            )
            tangent = Vector(-math.sin(a), 0.0, math.cos(a))
            xr = SHELL_HOOK_ROOT[0] + (SHELL_HOOK_TIP[0] - SHELL_HOOK_ROOT[0]) * t
            yr = SHELL_HOOK_ROOT[1] + (SHELL_HOOK_TIP[1] - SHELL_HOOK_ROOT[1]) * t
            plane = Plane(origin=pos, z_dir=tangent)
            faces.append((plane * Ellipse(xr, yr)).faces()[0])
        hook = loft(faces)
    else:
        pos = Vector(
            center.X + hook_radius * math.cos(start),
            center.Y,
            center.Z + hook_radius * math.sin(start),
        )
        tangent = Vector(-math.sin(start), 0.0, math.cos(start))
        sec = Plane(origin=pos, z_dir=tangent)
        circle = sec * Circle(hook_dia / 2.0)
        axis = Axis(center, Vector(0.0, -1.0, 0.0))
        hook = revolve(circle.faces()[0], axis=axis, revolution_arc=arc)
    axis = Axis(center, Vector(0.0, -1.0, 0.0))
    if float(params["GLASSES_FLAT"]) > 0.0:
        y_cut = root.Y + hook_dia / 2.0 - float(params["GLASSES_FLAT"])
        a0 = math.radians(GLASSES_FLAT_ANGLES[0])
        pos0 = Vector(
            center.X + hook_radius * math.cos(a0),
            center.Y,
            center.Z + hook_radius * math.sin(a0),
        )
        tan0 = Vector(-math.sin(a0), 0.0, math.cos(a0))
        cut_plane = Plane(origin=Vector(pos0.X, y_cut + 4.0, pos0.Z), z_dir=tan0)
        cutter_face = cut_plane * Rectangle(hook_dia + 4.0, 8.0)
        cutter = revolve(
            cutter_face.faces()[0],
            axis=axis,
            revolution_arc=GLASSES_FLAT_ANGLES[1] - GLASSES_FLAT_ANGLES[0],
        )
        hook = hook.cut(cutter)
    return _one_solid(hook, "hook")


def assemble_shell(
    body: Solid,
    lid: Solid,
    params: Mapping[str, Any],
    notes: dict[str, Any],
) -> tuple[Solid, Solid]:
    theta = -float(params["THETA_DEG"])
    body_r = body.rotate(Axis.X, theta)
    lid_r = lid.rotate(Axis.X, theta)
    hook = build_hook(params)
    # The −5° embedded start reaches past the 1.5 mm end wall into the
    # cavity and the battery pocket (4.6 mm³ at the defaults). Plan §2 row 6
    # keeps the cavity clear, so the stub is cut back to the cavity wall.
    path = make_path(float(params["BODY_ARC"]), float(params["CREASE_BOW"]))
    cu0, cu1 = cavity_u(params)
    cavity = _path_solid(
        path,
        cu0,
        cu1,
        cavity_s(params)[0],
        RIB_S[0],
        float(params["WALL_MEDIAL"]),
        float(params["BODY_THICK"]) + 1.0,
    ).rotate(Axis.X, theta)
    stub = _overlap_volume(hook, cavity)
    notes["hook_stub_in_cavity_removed_mm3"] = round(stub, 4)
    if stub > 0.0:
        # The cut can leave a sliver of tube inside the floor (y < WALL_MEDIAL,
        # at large bows); it lies in body material, so the whole cut result is
        # fused and the one-solid check runs on the assembly.
        hook = hook.cut(cavity)
    fused = _first_solid(body_r.fuse(hook), "body+hook")
    hook_r = float(params["HOOK_RADIUS"])
    hook_dia = float(params["HOOK_DIA"])
    root = Vector(float(params.get("HOOK_ROOT_X", 4.0)), float(params["HOOK_ROOT_Y"]), 0.0)
    center = Vector(root.X - hook_r, root.Y, 0.0)

    def on_hook_tube(point: Vector) -> bool:
        radial = math.hypot(point.X - center.X, point.Z - center.Z)
        dist = math.hypot(radial - hook_r, point.Y - root.Y)
        if stage_is_shell(params):
            lo, hi = min(SHELL_HOOK_TIP), max(SHELL_HOOK_ROOT)
            return lo - 0.4 <= dist <= hi + 0.4
        return abs(dist - hook_dia / 2.0) < 0.02

    # The joint is the loop where the tube leaves the top face: every point
    # on the tube surface, within a tube diameter of O, and not a circle
    # (circles are the tube's own section edges).
    joint = [
        e
        for e in fused.edges()
        if e.geom_type != GeomType.CIRCLE
        and all(on_hook_tube(Vector(e @ t)) for t in (0.0, 0.25, 0.5, 0.75, 1.0))
        and (e.center() - root).length < (
            max(SHELL_HOOK_ROOT) * 2.5 if stage_is_shell(params) else hook_dia
        )
    ]
    if not joint:
        if stage_is_shell(params):
            notes["fillets"].append("§3.5 step 9 hook joint fillet: no tube-to-top-face edge; blend skipped")
        else:
            raise CheckFail("hook joint: no tube-to-top-face edge found")
    else:
        fused, applied = _try_fillet(
            fused, joint, SHELL_HOOK_BLEND if stage_is_shell(params) else JOINT_FILLET
        )
        notes["fillets"].append(
            _fillet_note(
                "§3.5 step 9 hook joint fillet",
                SHELL_HOOK_BLEND if stage_is_shell(params) else JOINT_FILLET,
                applied,
            )
        )
    if params["SIDE"] == "left":
        fused = fused.mirror(Plane.YZ)
        lid_r = lid_r.mirror(Plane.YZ)
    return _one_solid(fused, "assembled_body"), _one_solid(lid_r, "assembled_lid")


def contact_caps(body: Solid, path: PathGeom, params: Mapping[str, Any]) -> dict[str, bool]:
    """Each mock dome stands along −y at its own P(u, s, 0): the point half a
    crown below the face is solid, and a point just past the crown is air."""
    out: dict[str, bool] = {}
    for name, (u, s) in (
        ("CONTACT_1", contact_1_us(params)),
        ("CONTACT_2", (float(params["CONTACT_2_U"]), float(params["CONTACT_2_S"]))),
        ("CONTACT_REF", contact_ref_us(params)),
    ):
        x, _y, z = p_xyz(path, float(u), float(s), 0.0)
        inside = body.is_inside(Vector(x, -CONTACT_DOME_CROWN / 2.0, z))
        beyond = body.is_inside(Vector(x, -CONTACT_DOME_CROWN - 0.1, z))
        out[name] = bool(inside and not beyond)
    return out


def _normalize_3mf(path: Path, part: str, uuid_ns: str = "elicio:cad:v1") -> None:
    """Rewrite 3MF UUIDs and zip metadata so SHA-256 is stable."""
    import io
    import re
    import zipfile

    uuid_re = re.compile(
        r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
    )
    with zipfile.ZipFile(path, "r") as src:
        names = sorted(src.namelist())
        contents = {name: src.read(name) for name in names}
    seen: dict[str, str] = {}
    counter = 0

    def replace_uuid(match: re.Match[str]) -> str:
        nonlocal counter
        original = match.group(0)
        if original not in seen:
            seen[original] = str(uuid.uuid5(UUID_NAMESPACE, f"{uuid_ns}:{part}:{counter}"))
            counter += 1
        return seen[original]

    for name, data in list(contents.items()):
        if name.endswith(".model") or name.endswith(".xml") or name.endswith(".rels"):
            text = data.decode("utf-8")
            text = uuid_re.sub(replace_uuid, text)
            contents[name] = text.encode("utf-8")
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as dest:
        for name in names:
            info = zipfile.ZipInfo(name, date_time=(2026, 9, 16, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            dest.writestr(info, contents[name])
    path.write_bytes(buffer.getvalue())


def export_part(shape: Shape, dest: Path, part: str, *, uuid_ns: str = "elicio:cad:v1") -> dict[str, Any]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    step_path = dest.with_suffix(".step")
    stl_path = dest.with_suffix(".stl")
    mf_path = dest.with_suffix(".3mf")
    labeled = shape
    try:
        labeled.label = part
    except Exception:
        pass
    ok = export_step(
        labeled,
        step_path,
        write_pcurves=True,
        precision_mode=PrecisionMode.AVERAGE,
        timestamp=STEP_TIMESTAMP,
    )
    if not ok:
        raise CheckFail(f"{part}: STEP export failed")
    ok = export_stl(
        labeled,
        stl_path,
        tolerance=MESH_CHORD,
        angular_tolerance=MESH_ANGLE_RAD,
        ascii_format=False,
    )
    if not ok:
        raise CheckFail(f"{part}: STL export failed")
    mesher = Mesher()
    mesher.add_shape(
        labeled,
        linear_deflection=MESH_CHORD,
        angular_deflection=MESH_ANGLE_RAD,
        part_number=part,
        uuid_value=uuid.uuid5(UUID_NAMESPACE, f"{uuid_ns}:{part}"),
    )
    mesher.write(mf_path)
    _normalize_3mf(mf_path, part, uuid_ns)
    files = {}
    for path in (step_path, stl_path, mf_path):
        files[path.name] = {"sha256": sha256_file(path), "bytes": path.stat().st_size}
    return files


def stl_watertight(path: Path) -> bool:
    try:
        import trimesh
    except ImportError as exc:
        raise CheckFail("trimesh: not installed; STL watertight check cannot run") from exc
    # OCCT STL writers emit unwelded vertices. Merge them before the check.
    mesh = trimesh.load(path, force="mesh", process=True)
    return bool(getattr(mesh, "is_watertight", False))


def build_reference_params(
    *,
    variant: str,
    preload: float,
    overrides: Mapping[str, Any] | None = None,
    crease_bow_from_m: bool = False,
) -> tuple[dict[str, Any], list[str]]:
    base = default_params()
    used = list(base.keys())
    merged = merge_params(base, overrides or {}, used)
    merged["VARIANT"] = variant
    merged["HOOK_PRELOAD"] = preload
    if "VARIANT" in used:
        used.remove("VARIANT")
    if "HOOK_PRELOAD" in used:
        used.remove("HOOK_PRELOAD")
    derived = derived_params(merged, crease_bow_from_m=crease_bow_from_m)
    derived["_defaults_used"] = used
    derived["_crease_bow_from_m"] = crease_bow_from_m
    return derived, used


def write_manifest(
    out_dir: Path,
    *,
    params_by_part: dict[str, dict[str, Any]],
    checks: list[Check],
    files: dict[str, dict[str, Any]],
    notes: dict[str, Any],
    overlap: float,
    defaults_used: list[str],
    params: Mapping[str, Any],
    stage_b_rows: Mapping[str, Mapping[str, Check]] | None = None,
) -> Path:
    path = make_path(float(params["BODY_ARC"]), float(params["CREASE_BOW"]))
    ws = wire_s_pair(params)
    ref_u, ref_s = contact_ref_us(params)
    openings = {
        str(bow): wire_channel_opening(
            make_path(float(params["BODY_ARC"]), bow).radius,
            s_end=ws[1],
            u_center=ref_u,
            s_center=ref_s,
        )
        for bow in (1.0, 3.0, 8.0)
    }
    openings["clamped"] = wire_channel_opening(
        path.radius, s_end=ws[1], u_center=ref_u, s_center=ref_s
    )
    payload = {
        "schema": 1,
        "hash_rule": (
            "SHA-256 of raw file bytes. STEP timestamp "
            f"{STEP_TIMESTAMP}. STL/3MF linear deflection {MESH_CHORD} mm, "
            "angular deflection 5 deg. 3MF object UUID5 is "
            "elicio:cad:v1:<part>; remaining UUIDs are rewritten in "
            "appearance order and the zip date is pinned to 2026-09-16."
        ),
        "commit": git_commit(REPO_ROOT, out_dir if stage_is_shell(params) else None),
        "parameters": {
            k: v
            for k, v in params.items()
            if not str(k).startswith("_") and _jsonable(v)
        },
        "defaults_used": sorted(defaults_used),
        "ref_build": any(k in defaults_used for k in REFERENCE_M_KEYS),
        "crease_bow": {
            "source": (
                "computed from M1 and M2"
                if params.get("_crease_bow_from_m")
                else "CREASE_BOW parameter (M1 and M2 not both measured)"
            ),
            "requested": params["CREASE_BOW_REQUESTED"],
            "computed_from_m1_m2": params["CREASE_BOW_COMPUTED"],
            "clamped": params["CREASE_BOW"],
        },
        "chord_gate": {
            "total_chord": params["TOTAL_CHORD"],
            "gate": float(params["TOTAL_CHORD"]) + 3.0,
            "m1": params["M1"],
        },
        "wire_channel": openings,
        "exceptions": exceptions_block(params),
        "fits": fit_table(params),
        "interference": {
            "lid_body_overlap_mm3": overlap,
            "unintended_nominal_overlap_fail": overlap > OVERLAP_NOISE_MM3,
        },
        "span": {
            name: {
                "BODY_THICK": float(p["BODY_THICK"]),
                "span": float(p["BODY_THICK"]) + CONTACT_DOME_CROWN,
                "M3": float(p["M3"]),
                "pinna_displacement": max(
                    0.0, float(p["BODY_THICK"]) + CONTACT_DOME_CROWN - float(p["M3"])
                ),
            }
            for name, p in params_by_part.items()
            if name.startswith("body_")
        },
        "walls": {k: round(v, 6) for k, v in wall_sizes(params).items()},
        "contact_stack": {
            "nominal": {k: round(v, 6) for k, v in contact_stack(params).items()},
            "wall_plus_0_3": {
                k: round(v, 6)
                for k, v in contact_stack(params, wall_extra=PART_TOLERANCE).items()
            },
            "keepout_top_y": KEEPOUT_TOP_Y,
            "board_underside_y": BOARD_UNDERSIDE_Y,
        },
        "keepout_clearance": {
            k: round(v, 4) for k, v in keepout_clearances(params, path).items()
        },
        "checks": [
            {
                "name": c.name,
                "passed": c.passed,
                "detail": c.detail,
                "numbers": c.numbers,
            }
            for c in checks
        ],
        "notes": notes,
        "files": files,
        "quantities": {part: QUANTITIES.get(part, 1) for part in built_parts(files)},
        "parts": built_parts(files),
        "variant_preload_built": {
            name: {
                "VARIANT": params_by_part[name]["VARIANT"],
                "HOOK_PRELOAD": params_by_part[name]["HOOK_PRELOAD"],
            }
            for name in params_by_part
            if name.startswith("body_")
        },
    }
    if not params.get("MOCK_CONTACTS", True):
        payload["stage"] = "shell" if stage_is_shell(params) else "B"
        payload["provisional"] = True
        payload["packing"] = params["PACKING"]
        payload["closure_passed"] = bool(params.get("CLOSURE_PASSED", False))
        payload["contact_source"] = str(params.get("CONTACT_SOURCE", "plan §3.3 defaults"))
        rows_by_body = stage_b_rows or {}
        bodies = sorted(rows_by_body)
        lead = "body_full_p15" if "body_full_p15" in rows_by_body else (bodies[0] if bodies else None)
        check_names = set(STAGE_B_CHECK_NAMES)
        if lead:
            check_names |= set(rows_by_body[lead])
        payload["stage_b"] = {
            name: {
                "passed": all(rows_by_body[b][name].passed for b in bodies if name in rows_by_body[b]),
                "detail": rows_by_body[lead][name].detail,
                "numbers": rows_by_body[lead][name].numbers,
                "numbers_from": lead,
                "bodies": {
                    b: {
                        "passed": rows_by_body[b][name].passed,
                        "numbers": rows_by_body[b][name].numbers,
                    }
                    for b in bodies
                    if name in rows_by_body[b]
                },
            }
            for name in sorted(check_names)
            if lead and name in rows_by_body[lead]
        } if lead else {}
        not_measured = sorted(
            name
            for name, row in payload["stage_b"].items()
            if str(row["detail"]).startswith("NOT_MEASURED")
        )
        payload["stage_b_not_measured"] = not_measured
        failing = stage_b_failing(rows_by_body, skip_not_measured=stage_is_shell(params))
        payload["stage_b_failing"] = failing
        payload["stage_b_passed"] = not failing
        if stage_is_shell(params):
            payload["winner"] = SHELL_WINNER
            payload["params_file"] = "scripts/cad/params/shell_v2.toml"
            if SHELL_PARAMS_FILE.is_file():
                payload["params_sha256"] = sha256_file(SHELL_PARAMS_FILE)
            payload["q34"] = "M1=52 default.toml; Q34 blank"
            payload["hash_rule"] = (
                "SHA-256 of raw file bytes. STEP timestamp "
                f"{STEP_TIMESTAMP}. STL/3MF linear deflection {MESH_CHORD} mm, "
                "angular deflection 5 deg. 3MF object UUID5 is "
                "elicio:cad:v2:<part>; remaining UUIDs are rewritten in "
                "appearance order and the zip date is pinned to 2026-09-16."
            )
    dest = out_dir / "manifest.json"
    if dest.is_file():
        previous = json.loads(dest.read_text(encoding="utf-8"))
        # Views are pictures of the order 1 solids; a Stage B build never
        # inherits them, and order 1 never inherits a Stage B folder's.
        if previous.get("stage") == payload.get("stage"):
            for key in ("views", "views_hash_rule", "views_commit"):
                if key in previous:
                    payload[key] = previous[key]
    dest.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return dest


def built_parts(files: Mapping[str, Any]) -> list[str]:
    names = sorted({name.rsplit(".", 1)[0] for name in files})
    order = [part for part in ORDER_PARTS if part in names]
    return order + [part for part in names if part not in ORDER_PARTS]


def _jsonable(value: Any) -> bool:
    return isinstance(value, (str, int, float, bool, list, dict, type(None)))


def assert_stage_b_out_dir(out_dir: Path, params: Mapping[str, Any]) -> None:
    if params.get("MOCK_CONTACTS", True):
        return
    resolved = out_dir.resolve()
    if stage_is_shell(params):
        try:
            resolved.relative_to(V1_DIR.resolve())
        except ValueError:
            return
        raise CheckFail(
            f"--out {out_dir}: shell must not write under {V1_DIR} "
            "(order 1 stays byte-identical)"
        )
    for forbidden in (V1_DIR, V2_DIR):
        forb = forbidden.resolve()
        try:
            resolved.relative_to(forb)
        except ValueError:
            continue
        raise CheckFail(
            f"--out {out_dir}: Stage B must not write under {forb} "
            "(name a temp directory)"
        )


def build_and_export(
    out_dir: Path,
    *,
    overrides: Mapping[str, Any] | None = None,
    crease_bow_from_m: bool = False,
    parts: tuple[str, ...] | None = None,
) -> dict[str, Any]:
    _require_cad()
    probe, _ = build_reference_params(
        variant="full",
        preload=1.5,
        overrides=overrides,
        crease_bow_from_m=crease_bow_from_m,
    )
    assert_stage_b_out_dir(out_dir, probe)
    stage_b = not probe["MOCK_CONTACTS"]
    wanted = parts or (
        SHELL_PARTS if stage_is_shell(probe) else STAGE_B_PARTS if stage_b else ORDER_PARTS
    )
    uuid_ns = "elicio:cad:v2" if stage_is_shell(probe) else "elicio:cad:v1"
    if stage_b and not any(name.startswith("body_") for name in wanted):
        raise CheckFail(
            f"--parts {','.join(wanted)}: a Stage B build needs a body; the Stage B checks run on bodies"
        )
    existing = out_dir / "manifest.json"
    if existing.is_file():
        # A subset build would rewrite the manifest and leave the other
        # parts' files from an older parameter set beside it.
        listed = json.loads(existing.read_text(encoding="utf-8")).get("files", {})
        stale = sorted({n.rsplit(".", 1)[0] for n in listed} - set(wanted))
        if stale:
            raise CheckFail(
                f"--out {out_dir}: would leave stale parts {', '.join(stale)}; "
                "build the full set or use an empty --out"
            )
    out_dir.mkdir(parents=True, exist_ok=True)
    files: dict[str, dict[str, Any]] = {}
    params_by_part: dict[str, dict[str, Any]] = {}
    all_checks: list[Check] = []
    notes_acc: dict[str, Any] = {}
    overlap = 0.0
    defaults_used: list[str] = []
    report_params: dict[str, Any] = {}
    stage_b_rows: dict[str, dict[str, Check]] = {}

    jobs: list[tuple[str, str, float]] = []
    tag_to_preload = {"p15": 1.5, "p25": 2.5}
    for name in wanted:
        if not name.startswith("body_"):
            continue
        rest = name[len("body_") :]
        if "_" not in rest:
            raise CheckFail(f"{name}: not a body_<variant>_<preload> name")
        variant, tag = rest.split("_", 1)
        if variant not in MATRIX_VARIANTS or tag not in tag_to_preload:
            raise CheckFail(f"{name}: outside the VARIANT × HOOK_PRELOAD matrix")
        jobs.append((name, variant, tag_to_preload[tag]))

    lid_shape: Shape | None = None
    reference_lid: tuple[Solid, float] | None = None

    def exported_lid_in_body_frame() -> tuple[Solid, float]:
        """The one lid file is the full-body p15 lid (plan §3.6 lists one)."""
        nonlocal reference_lid
        if reference_lid is None:
            ref_params, _ = build_reference_params(
                variant="full",
                preload=1.5,
                overrides=overrides,
                crease_bow_from_m=crease_bow_from_m,
            )
            _b, ref_lid, _p, _n = build_body_and_lid(ref_params)
            reference_lid = (ref_lid, float(ref_params["LID_Y"]))
        return reference_lid

    for name, variant, preload in jobs:
        params, used = build_reference_params(
            variant=variant,
            preload=preload,
            overrides=overrides,
            crease_bow_from_m=crease_bow_from_m,
        )
        if name == "body_full_p15" or not report_params:
            defaults_used = used
            report_params = params
        checks = run_pre_cad_checks(params)
        all_checks.extend(checks)
        body_bf, lid_bf, path, notes = build_body_and_lid(params)
        notes_acc[name] = notes
        if name == "body_full_p15" and reference_lid is None:
            reference_lid = (lid_bf, float(params["LID_Y"]))
        ref_lid, ref_lid_y = exported_lid_in_body_frame()
        # Lid features are placed relative to LID_Y, so the one exported lid
        # seats on every body at that body's LID_Y. Check it there.
        seated = ref_lid.moved(Location((0.0, float(params["LID_Y"]) - ref_lid_y, 0.0)))
        part_overlap = _overlap_volume(body_bf, seated)
        overlap = max(overlap, part_overlap)
        if part_overlap > OVERLAP_NOISE_MM3:
            raise CheckFail(
                f"lid_body_overlap={part_overlap:.4f} mm³ on {name}: unintended nominal overlap"
            )
        if params["MOCK_CONTACTS"]:
            for contact, ok in contact_caps(body_bf, path, params).items():
                if not ok:
                    raise CheckFail(f"contact axes: {name} {contact} dome does not stand to −y")
                all_checks.append(Check(f"contact axis −y: {contact}", True, name, {}))
        else:
            rows = run_stage_b_solid_checks(body_bf, lid_bf, path, params, notes["stage_b_cuts"])
            missing = sorted(STAGE_B_CHECK_NAMES - {row.name for row in rows})
            if missing:
                # Round 1 decision 5: MOCK_CONTACTS = false builds only behind
                # the Stage B checks. Nothing is exported without all of them.
                raise CheckFail(
                    f"MOCK_CONTACTS=false: Stage B checks missing on {name}: {', '.join(missing)}"
                )
            all_checks.extend(rows)
            stage_b_rows[name] = {row.name: row for row in rows}
        all_checks.append(
            Check(
                "exported lid seated on this body: interiors disjoint",
                True,
                name,
                {"overlap_mm3": part_overlap, "LID_Y": float(params["LID_Y"])},
            )
        )
        assembled, lid_s = assemble_shell(body_bf, lid_bf, params, notes)
        all_checks.append(Check("one connected solid", True, name, {}))
        with_hook = _overlap_volume(assembled, lid_s)
        if with_hook > OVERLAP_NOISE_MM3:
            raise CheckFail(
                f"lid_body_overlap={with_hook:.4f} mm³ on {name} with the hook: unintended overlap"
            )
        overlap = max(overlap, with_hook)
        exported = export_part(assembled, out_dir / name, name, uuid_ns=uuid_ns)
        files.update(exported)
        stl = out_dir / f"{name}.stl"
        if not stl_watertight(stl):
            raise CheckFail(f"{name}: STL is not watertight")
        all_checks.append(
            Check("watertight", True, name, {"bytes": float(stl.stat().st_size)})
        )
        params_by_part[name] = params
        if name == "body_full_p15":
            lid_shape = lid_s

    if "lid" in wanted:
        if lid_shape is None:
            params, used = build_reference_params(
                variant="full",
                preload=1.5,
                overrides=overrides,
                crease_bow_from_m=crease_bow_from_m,
            )
            defaults_used = used
            report_params = params
            all_checks.extend(run_pre_cad_checks(params))
            _body, lid_bf, _path, notes = build_body_and_lid(params)
            _assembled, lid_shape = assemble_shell(_body, lid_bf, params, notes)
            notes_acc["lid"] = notes
        all_checks.append(Check("one connected solid", True, "lid", {}))
        exported = export_part(lid_shape, out_dir / "lid", "lid", uuid_ns=uuid_ns)
        files.update(exported)
        if not stl_watertight(out_dir / "lid.stl"):
            raise CheckFail("lid: STL is not watertight")
        all_checks.append(Check("watertight", True, "lid", {}))

    if "coupon" in wanted:
        coupon = build_coupon()
        all_checks.append(Check("one connected solid", True, "coupon", {}))
        exported = export_part(coupon, out_dir / "coupon", "coupon", uuid_ns=uuid_ns)
        files.update(exported)
        if not stl_watertight(out_dir / "coupon.stl"):
            raise CheckFail("coupon: STL is not watertight")
        all_checks.append(Check("watertight", True, "coupon", {}))

    if report_params:
        write_manifest(
            out_dir,
            params_by_part=params_by_part,
            checks=all_checks,
            files=files,
            notes=notes_acc,
            overlap=overlap,
            defaults_used=defaults_used,
            params=report_params,
            stage_b_rows=stage_b_rows if stage_b else None,
        )
    failing = (
        stage_b_failing(
            stage_b_rows,
            skip_not_measured=stage_is_shell(report_params or probe),
        )
        if stage_b
        else None
    )
    return {
        "files": files,
        "overlap": overlap,
        "checks": all_checks,
        "stage_b_passed": None if failing is None else not failing,
        "stage_b_failing": failing,
    }


def stage_b_failing(
    stage_b_rows: Mapping[str, Mapping[str, Check]],
    *,
    skip_not_measured: bool = False,
) -> list[str]:
    names = {
        name
        for rows in stage_b_rows.values()
        for name, row in rows.items()
        if not row.passed
        and not (skip_not_measured and str(row.detail).startswith("NOT_MEASURED"))
    }
    return sorted(names)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the Elicio BTE fit gauge.")
    parser.add_argument(
        "--params",
        type=Path,
        default=None,
        help="TOML or JSON overrides (default.toml keys). Relative paths also try params/",
    )
    parser.add_argument("--variant", choices=sorted(MATRIX_VARIANTS), default=None)
    parser.add_argument("--preload", type=float, default=None)
    parser.add_argument("--side", choices=("right", "left"), default=None)
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "docs" / "fab" / "cad" / "v1")
    parser.add_argument(
        "--stage",
        choices=("gauge", "B", "shell"),
        default=None,
        help="gauge = order 1; B = Stage B temp; shell = wearable body into docs/fab/cad/v2/",
    )
    parser.add_argument(
        "--set",
        dest="sets",
        action="append",
        default=[],
        help="KEY=VALUE override, repeatable",
    )
    parser.add_argument(
        "--from-measurements",
        action="store_true",
        help="Compute CREASE_BOW from M1/M2 (both must be set; automatic for an overlay file)",
    )
    parser.add_argument(
        "--checks-only",
        action="store_true",
        help="Run §3.3 pre-export checks and stop",
    )
    parser.add_argument(
        "--parts",
        default=None,
        help=(
            "Comma list of parts. Default: the five order-1 names; with "
            "MOCK_CONTACTS=false, body_full_p15,body_full_p25,lid"
        ),
    )
    return parser.parse_args(argv)


def resolve_params_path(path: Path | None) -> Path | None:
    if path is None:
        return None
    if path.exists():
        return path
    alt = SCRIPT_DIR / "params" / path.name
    if alt.exists():
        return alt
    raise CheckFail(f"params={path}: file not found")


def resolve_overrides(args: argparse.Namespace) -> tuple[dict[str, Any], bool]:
    """Collect the overlay and decide whether CREASE_BOW comes from M1/M2.

    ``default.toml`` passed with ``--params`` is the reference build, not an
    overlay: its keys stay defaults and the build stays REF. A measurement
    overlay computes CREASE_BOW only when it sets both M1 and M2 and does not
    set CREASE_BOW (plan §3.3: "from arc–chord when both measured").
    """
    overrides: dict[str, Any] = {}
    params_path = resolve_params_path(args.params)
    is_overlay_file = (
        params_path is not None and params_path.resolve() != DEFAULT_PARAMS_PATH.resolve()
    )
    if is_overlay_file:
        overrides.update(
            {canonical_key(k): v for k, v in load_params_file(params_path).items()}
        )
    for item in args.sets:
        if "=" not in item:
            raise CheckFail(f"--set {item}: expected KEY=VALUE")
        key, value = item.split("=", 1)
        overrides[canonical_key(key)] = _parse_value(value)
    if args.side:
        overrides["SIDE"] = args.side
    if args.variant:
        overrides["VARIANT"] = args.variant
    if args.preload is not None:
        overrides["HOOK_PRELOAD"] = args.preload
    assert_override_matrix(overrides)
    validate_overrides(default_params(), overrides)

    both_measured = "M1" in overrides and "M2" in overrides
    if args.from_measurements:
        if not both_measured:
            raise CheckFail("--from-measurements: M1 and M2 must both be set")
        if "CREASE_BOW" in overrides:
            raise CheckFail("--from-measurements: remove CREASE_BOW from the overlay")
        return overrides, True
    return overrides, is_overlay_file and both_measured and "CREASE_BOW" not in overrides


def cli(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    overrides, crease_from_m = resolve_overrides(args)
    if args.stage == "shell":
        overrides["STAGE"] = "shell"
        overrides.setdefault("MOCK_CONTACTS", False)
    elif args.stage == "B":
        overrides["STAGE"] = "b"
        overrides.setdefault("MOCK_CONTACTS", False)
    probe, _used = build_reference_params(
        variant=str(overrides.get("VARIANT", "full")).lower(),
        preload=float(overrides.get("HOOK_PRELOAD", 1.5)),
        overrides=overrides,
        crease_bow_from_m=crease_from_m,
    )
    if stage_is_shell(probe) and args.out.resolve() == V1_DIR.resolve():
        args.out = V2_DIR

    if args.variant is not None or args.preload is not None:
        variant = str(overrides.get("VARIANT", "full")).lower()
        preload = float(overrides.get("HOOK_PRELOAD", 1.5))
        params, _used = build_reference_params(
            variant=variant,
            preload=preload,
            overrides=overrides,
            crease_bow_from_m=crease_from_m,
        )
        run_pre_cad_checks(params)
        if args.checks_only:
            print(f"checks passed VARIANT={variant} HOOK_PRELOAD={preload}")
            return 0
        name = part_name("body", params)
        parts = (name, "lid", "coupon") if params["MOCK_CONTACTS"] else (name, "lid")
        # Single-variant export still writes lid+coupon beside the body.
        result = build_and_export(
            args.out,
            overrides=overrides,
            crease_bow_from_m=crease_from_m,
            parts=parts if name in ORDER_PARTS else (name,),
        )
        print(json.dumps({"out": str(args.out), "files": list(result["files"])}, indent=2))
        return _stage_b_exit(result)

    params, _used = build_reference_params(
        variant="full",
        preload=1.5,
        overrides=overrides,
        crease_bow_from_m=crease_from_m,
    )
    run_pre_cad_checks(params)
    if args.checks_only:
        print("checks passed for reference set")
        return 0
    wanted = tuple(p.strip() for p in args.parts.split(",")) if args.parts else None
    result = build_and_export(
        args.out,
        overrides=overrides,
        crease_bow_from_m=crease_from_m,
        parts=wanted,
    )
    print(json.dumps({"out": str(args.out), "files": list(result["files"])}, indent=2))
    return _stage_b_exit(result)


STAGE_B_NOT_PASSED_EXIT = 3


def _stage_b_exit(result: Mapping[str, Any]) -> int:
    """0 for order 1 and for a Stage B build whose checks all pass. A Stage B
    build with a recorded non-fatal failure (Q21) wrote its files and exits 3."""
    if result.get("stage_b_passed") is False:
        print(
            "STAGE B NOT PASSED (files and manifest written, provisional): "
            + ", ".join(result["stage_b_failing"]),
            file=sys.stderr,
        )
        return STAGE_B_NOT_PASSED_EXIT
    return 0


def main() -> None:
    try:
        raise SystemExit(cli())
    except CheckFail as exc:
        print(f"CHECK FAIL: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()
