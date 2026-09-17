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
    the first failure, so a written manifest lists passes only.
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
        Face,
        GeomType,
        Location,
        Mesher,
        Plane,
        Pos,
        PrecisionMode,
        Rectangle,
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
PACKING_OPTIONS = frozenset({"A", "B", "C"})
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
STAGE_B_EMBOSS = 0.4  # Q11; gauge keeps 0.8
STAGE_B_EMBOSS_S = 10.0  # battery zone, not over the module


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


def apply_stage_b_packing(p: dict[str, Any]) -> None:
    """Packing A/B/C from placement.Layout. Default C (Q20, provisional)."""
    packing = str(p.get("PACKING", "C")).upper()
    if packing not in PACKING_OPTIONS:
        raise CheckFail(f"PACKING={p.get('PACKING')}: must be A, B or C")
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


def validate_overrides(base: Mapping[str, Any], override: Mapping[str, Any]) -> None:
    """Unknown keys and keys fixed for this release fail before export."""
    known = {canonical_key(k) for k in base} | OVERRIDABLE_KEYS
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
    return f"ELICIO V1 {side} {variant} {tag}{ref}".strip()


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


def git_commit_solids(repo: Path) -> str:
    """Last commit that changed a hashed solid, not HEAD of the repository.

    Paths are the committed STEP/STL/3MF files under docs/fab/cad/v1. A
    later commit that only adds renders, docs, or tests does not move this
    field, so a solids regen test stays stable.
    """
    v1 = repo / "docs" / "fab" / "cad" / "v1"
    paths = sorted(
        str(path)
        for path in v1.iterdir()
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


def git_commit(repo: Path) -> str:
    """Manifest ``commit``: solids last-change, not the current HEAD."""
    return git_commit_solids(repo)


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
    if not params.get("MOCK_CONTACTS", True):
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
    """TE 31428 upright in the Ø7.5 pocket (contacts.md §5.3, Q21)."""
    wall = float(params["WALL_MEDIAL"])
    lid_y = float(params["LID_Y"])
    pl = load_placement()
    tab_len = float(pl.TAB_LEN)
    lug_thick = float(pl.LUG_THICK)
    ring_r = float(pl.RING_R)
    barrel = float(pl.TAB_W)
    lug_top_y = wall + tab_len + lug_thick
    barrel_outer = ring_r + barrel
    pocket_r = POCKET_DIA / 2.0
    return {
        "lug_top_y": round(lug_top_y, 4),
        "lid_y": lid_y,
        "barrel_outer": round(barrel_outer, 4),
        "pocket_r": pocket_r,
        "lug_thick": lug_thick,
        "envelope_y": 1.5,
    }


def cell_pocket_clearances(params: Mapping[str, Any]) -> dict[str, float]:
    """Cell 5.2 × 10.4 × 15.6 in the battery pocket; foam 0.5 on the lid face."""
    pocket_y = BATTERY_Y[1] - BATTERY_Y[0]
    pocket_u = BATTERY_U[1] - BATTERY_U[0]
    pocket_s = BATTERY_S[1] - BATTERY_S[0]
    need_y = CELL_MAX[0] + FOAM_THICK
    need_u = CELL_MAX[1]
    need_s = CELL_MAX[2]
    return {
        "pocket_y": round(pocket_y, 4),
        "pocket_u": round(pocket_u, 4),
        "pocket_s": round(pocket_s, 4),
        "need_y": round(need_y, 4),
        "need_u": round(need_u, 4),
        "need_s": round(need_s, 4),
        "clear_y": round(pocket_y - need_y, 4),
        "clear_u": round(pocket_u - need_u, 4),
        "clear_s": round(pocket_s - need_s, 4),
    }


def ref_wire_containment(params: Mapping[str, Any]) -> dict[str, float]:
    """Ø1.3 envelope at bend radius 3: pocket → channel → pad (open item 4)."""
    pl = load_placement()
    packing = str(params["PACKING"])
    layout = pl.get_layout(packing)
    route = layout.ref_wire
    cu0, cu1 = cavity_u(params)
    cs0, cs1 = cavity_s(params)
    ws0, ws1 = wire_s_pair(params)
    wire_r = float(pl.WIRE_OD) / 2.0
    pad_u, pad_s = layout.lead_pads["REF"]
    worst_cavity = math.inf
    worst_battery = math.inf
    worst_pad = math.inf
    n = 24
    for i in range(len(route) - 1):
        (u0, s0), (u1, s1) = route[i], route[i + 1]
        for k in range(n + 1):
            t = k / n
            u = u0 + (u1 - u0) * t
            s = s0 + (s1 - s0) * t
            in_channel = ws0 - wire_r <= s <= ws1 + wire_r and WIRE_U[0] - wire_r <= u <= WIRE_U[1] + wire_r
            in_pocket = math.hypot(u - contact_ref_us(params)[0], s - contact_ref_us(params)[1]) <= POCKET_DIA / 2.0 + wire_r
            in_cavity = (cu0 + wire_r <= u <= cu1 - wire_r and cs0 + wire_r <= s <= cs1 + wire_r)
            if in_channel or in_pocket or in_cavity:
                cavity_margin = 1.0
            else:
                cavity_margin = min(
                    u - cu0, cu1 - u, s - cs0, cs1 - s, 0.0
                ) - wire_r
            worst_cavity = min(worst_cavity, cavity_margin)
            bu0, bu1 = BATTERY_U
            bs0, bs1 = BATTERY_S
            du = 0.0 if bu0 <= u <= bu1 else min(abs(u - bu0), abs(u - bu1))
            ds = 0.0 if bs0 <= s <= bs1 else min(abs(s - bs0), abs(s - bs1))
            if bu0 <= u <= bu1 and bs0 <= s <= bs1:
                batt_gap = -wire_r
            else:
                batt_gap = math.hypot(du, ds) - wire_r
            worst_battery = min(worst_battery, batt_gap)
            for (pu0, pu1, ps0, ps1) in (
                (cu0, cu0 + PAD_SIZE, board_zone_s(params)[0], board_zone_s(params)[0] + PAD_SIZE),
                (cu1 - PAD_SIZE, cu1, board_zone_s(params)[0], board_zone_s(params)[0] + PAD_SIZE),
                (cu0, cu0 + PAD_SIZE, board_zone_s(params)[1] - PAD_SIZE, board_zone_s(params)[1]),
                (cu1 - PAD_SIZE, cu1, board_zone_s(params)[1] - PAD_SIZE, board_zone_s(params)[1]),
            ):
                if pu0 <= u <= pu1 and ps0 <= s <= ps1:
                    worst_pad = min(worst_pad, -wire_r)
                else:
                    dpu = 0.0 if pu0 <= u <= pu1 else min(abs(u - pu0), abs(u - pu1))
                    dps = 0.0 if ps0 <= s <= ps1 else min(abs(s - ps0), abs(s - ps1))
                    worst_pad = min(worst_pad, math.hypot(dpu, dps) - wire_r)
    end = route[-1]
    end_gap = math.hypot(end[0] - pad_u, end[1] - pad_s)
    lid_y = float(params["LID_Y"])
    wire_top = WIRE_Y[1]
    return {
        "cavity_margin": round(worst_cavity, 4),
        "battery_gap": round(worst_battery, 4),
        "charge_pad_gap": round(worst_pad, 4),
        "lid_gap": round(lid_y - wire_top, 4),
        "end_to_pad": round(end_gap, 4),
        "wire_od": float(pl.WIRE_OD),
        "bend_r": float(pl.BEND_R),
    }


def cable_exit_pre_cad(params: Mapping[str, Any]) -> dict[str, float]:
    s_exit = cable_exit_s(params)
    cs0, cs1 = cavity_s(params)
    in_cavity_s = 1.0 if cs0 < s_exit < cs1 else 0.0
    hits_battery = 1.0 if BATTERY_S[0] < s_exit < BATTERY_S[1] else 0.0
    hits_rib = 1.0 if RIB_S[0] < s_exit < RIB_S[1] else 0.0
    y_ok = 1.0 if float(params["WALL_MEDIAL"]) < CABLE_EXIT_Y < float(params["LID_Y"]) else 0.0
    return {
        "CABLE_EXIT_S": s_exit,
        "in_cavity_s": in_cavity_s,
        "hits_battery": hits_battery,
        "hits_rib": hits_rib,
        "y_ok": y_ok,
        "CABLE_EXIT_Y": CABLE_EXIT_Y,
    }


def run_stage_b_pre_cad_checks(params: Mapping[str, Any], record: Callable[..., None]) -> None:
    """Named Stage B checks that do not need a solid (plan §3.3, §5, Q21, Q22)."""
    wall = float(params["WALL_MEDIAL"])
    tab_h = tab_height(params)
    barrel_top = wall + BARREL_HEIGHT
    envelope_top = wall + tab_h
    stack_top = KEEPOUT_TOP_Y
    board_y = BOARD_UNDERSIDE_Y
    record(
        "BOARD_underside_clear",
        board_y > stack_top + 1e-9
        and board_y > barrel_top + 1e-9
        and board_y > envelope_top + 1e-9,
        "board underside at y 4.3 clears stack top 4.13 and both barrels 3.46",
        stack_top=stack_top,
        barrel_top=round(barrel_top, 4),
        envelope_top=round(envelope_top, 4),
        board_underside=board_y,
        TAB_HEIGHT=tab_h,
    )
    cell = cell_pocket_clearances(params)
    record(
        "CELL_envelope",
        cell["clear_y"] >= -1e-9 and cell["clear_u"] >= -1e-9 and cell["clear_s"] >= -1e-9,
        "cell 5.2 × 10.4 × 15.6 fits the pocket with 0.5 foam on the lid face",
        **cell,
    )
    wire = ref_wire_containment(params)
    record(
        "REF_WIRE_envelope",
        wire["cavity_margin"] > 0.0
        and wire["battery_gap"] > 0.0
        and wire["charge_pad_gap"] > 0.0
        and wire["lid_gap"] > 0.0,
        "Ø1.3 envelope at bend radius 3 is in cavity air and clears battery, charge pads, lid",
        **wire,
    )
    cable = cable_exit_pre_cad(params)
    record(
        "CABLE_EXIT_cavity",
        cable["in_cavity_s"] == 1.0
        and cable["hits_battery"] == 0.0
        and cable["hits_rib"] == 0.0
        and cable["y_ok"] == 1.0,
        "CABLE_EXIT meets the cavity and nothing else",
        **cable,
    )
    q21 = q21_ref_lug_numbers(params)
    record(
        "Q21_REF_lug",
        q21["lug_top_y"] < q21["lid_y"] - 1e-9 and q21["barrel_outer"] <= q21["pocket_r"] + 1e-9,
        "reference lug collides with the lid or the pocket wall (Q21); not hidden",
        fatal=False,
        **q21,
    )
    record(
        "CLOSURE_PASSED",
        True,
        "E1/E3/E5 omitted until the closure test passes"
        if not lid_experiments(params)
        else "E1/E3/E5 present (closure test passed)",
        flag=1.0 if params.get("CLOSURE_PASSED") else 0.0,
    )
    gaps = keepout_clearances(params, make_path(float(params["BODY_ARC"]), float(params["CREASE_BOW"])))
    tab_min = min(gaps.get("TAB SIG1 min pad/rib gap", 1.0), gaps.get("TAB SIG2 min pad/rib gap", 1.0))
    record(
        "TAB_envelope_air",
        tab_min > 0.0,
        "tab envelopes 1.96 × 2.0 from Ø7.1 to 8.85: corner pads and rib outside",
        min_gap=round(tab_min, 4),
        TAB_HEIGHT=tab_h,
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
    record(
        "BODY_THICK",
        abs(float(params["BODY_THICK"]) - thick_expected) < 1e-9,
        "thickness follows VARIANT",
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


def _cut_stage_b_contacts(
    body: Shape,
    path: PathGeom,
    params: Mapping[str, Any],
    path_solid: Callable[..., Shape],
) -> Shape:
    """Holes through the 1.5 wall, pocket, channel, cable exit, reserved-air stacks."""
    wall = float(params["WALL_MEDIAL"])
    lid_y = float(params["LID_Y"])
    width = float(params["BODY_WIDTH"])
    hole_r = CONTACT_HOLE / 2.0
    hole_h = wall + 1.0
    c1 = contact_1_us(params)
    c2 = (float(params["CONTACT_2_U"]), float(params["CONTACT_2_S"]))
    cref = contact_ref_us(params)

    def cylinder_y(x: float, y0: float, z: float, radius: float, height: float) -> Shape:
        plane = Plane(origin=Vector(x, y0, z), z_dir=Vector(0.0, 1.0, 0.0))
        return Solid.make_cylinder(radius, height, plane)

    for u, s in (c1, c2, cref):
        origin = _vec(path, float(u), float(s), 0.0)
        body = body.cut(cylinder_y(origin.X, -0.5, origin.Z, hole_r, hole_h))
    pocket_c = _vec(path, cref[0], cref[1], 0.0)
    body = body.cut(
        cylinder_y(pocket_c.X, wall, pocket_c.Z, POCKET_DIA / 2.0, lid_y - wall + 0.2)
    )
    ws0, ws1 = wire_s_pair(params)
    channel = path_solid(WIRE_U[0], WIRE_U[1], ws0, ws1, WIRE_Y[0], WIRE_Y[1])
    body = body.cut(channel)
    s_exit = cable_exit_s(params)
    exit_pt = _vec(path, width, s_exit, CABLE_EXIT_Y)
    a = angle_at(path, s_exit)
    normal = Vector(math.cos(a), 0.0, math.sin(a))
    exit_plane = Plane(
        origin=Vector(exit_pt.X - 3.0 * normal.X, exit_pt.Y, exit_pt.Z - 3.0 * normal.Z),
        z_dir=normal,
    )
    cable = Solid.make_cylinder(CABLE_EXIT_DIA / 2.0, 6.0, exit_plane)
    body = body.cut(cable)

    pl = load_placement()
    packing = str(params["PACKING"])
    tab_h = tab_height(params)
    keep_r = float(pl.KEEPOUT_R)
    a0, a1 = float(pl.KEEPOUT_R), float(pl.LUG_A1)
    tab_w = float(pl.TAB_W)
    for name, (cu, cs) in (("SIG1", c1), ("SIG2", c2)):
        origin = _vec(path, float(cu), float(cs), 0.0)
        keep = cylinder_y(origin.X, wall - 0.02, origin.Z, keep_r, KEEPOUT_TOP_Y - wall + 0.05)
        body = body.cut(keep)
        deg = float(params["TAB_DEG"][name])
        tab = _tab_envelope_solid(
            path, float(cu), float(cs), deg, a0, a1, tab_w, wall, wall + tab_h
        )
        body = body.cut(tab)
    return body


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
        body = _cut_stage_b_contacts(body, path, params, path_solid)
        notes["q21_ref_lug"] = q21_ref_lug_numbers(params)

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
    pos = Vector(
        center.X + hook_radius * math.cos(start),
        center.Y,
        center.Z + hook_radius * math.sin(start),
    )
    tangent = Vector(-math.sin(start), 0.0, math.cos(start))
    sec = Plane(origin=pos, z_dir=tangent)
    circle = sec * Circle(hook_dia / 2.0)
    axis = Axis(center, Vector(0.0, -1.0, 0.0))
    arc = float(params["HOOK_ANGLE"]) - HOOK_EMBED_DEG
    hook = revolve(circle.faces()[0], axis=axis, revolution_arc=arc)
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
        return abs(dist - hook_dia / 2.0) < 0.02

    # The joint is the loop where the tube leaves the top face: every point
    # on the tube surface, within a tube diameter of O, and not a circle
    # (circles are the tube's own section edges).
    joint = [
        e
        for e in fused.edges()
        if e.geom_type != GeomType.CIRCLE
        and all(on_hook_tube(Vector(e @ t)) for t in (0.0, 0.25, 0.5, 0.75, 1.0))
        and (e.center() - root).length < hook_dia
    ]
    if not joint:
        raise CheckFail("hook joint: no tube-to-top-face edge found")
    fused, applied = _try_fillet(fused, joint, JOINT_FILLET)
    notes["fillets"].append(_fillet_note("§3.5 step 9 hook joint fillet", JOINT_FILLET, applied))
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


def _normalize_3mf(path: Path, part: str) -> None:
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
            seen[original] = str(uuid.uuid5(UUID_NAMESPACE, f"elicio:cad:v1:{part}:{counter}"))
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


def export_part(shape: Shape, dest: Path, part: str) -> dict[str, Any]:
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
        uuid_value=uuid.uuid5(UUID_NAMESPACE, f"elicio:cad:v1:{part}"),
    )
    mesher.write(mf_path)
    _normalize_3mf(mf_path, part)
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
        "commit": git_commit(REPO_ROOT),
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
        payload["stage"] = "B"
        payload["provisional"] = True
        payload["packing"] = params["PACKING"]
        payload["closure_passed"] = bool(params.get("CLOSURE_PASSED", False))
        payload["contact_source"] = str(params.get("CONTACT_SOURCE", "plan §3.3 defaults"))
        payload["stage_b"] = {
            c.name: {"passed": c.passed, "detail": c.detail, "numbers": c.numbers}
            for c in checks
            if c.name in STAGE_B_CHECK_NAMES
        }
    dest = out_dir / "manifest.json"
    if dest.is_file():
        previous = json.loads(dest.read_text(encoding="utf-8"))
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


def _point_inside(body: Solid, path: PathGeom, u: float, s: float, y: float) -> bool:
    x, yy, z = p_xyz(path, u, s, y)
    return bool(body.is_inside(Vector(x, yy, z)))


def run_stage_b_solid_checks(
    body: Solid,
    lid: Solid,
    path: PathGeom,
    params: Mapping[str, Any],
) -> list[Check]:
    """Solid Stage B checks. Fail loudly except Q21 (already recorded)."""
    checks: list[Check] = []

    def record(name: str, passed: bool, detail: str, **numbers: float) -> None:
        checks.append(Check(name, passed, detail, numbers))
        if not passed:
            num = ", ".join(f"{k}={v}" for k, v in numbers.items())
            raise CheckFail(f"{name}: {detail} ({num})" if num else f"{name}: {detail}")

    wall = float(params["WALL_MEDIAL"])
    width = float(params["BODY_WIDTH"])
    hole_r = CONTACT_HOLE / 2.0
    c1 = contact_1_us(params)
    c2 = (float(params["CONTACT_2_U"]), float(params["CONTACT_2_S"]))
    cref = contact_ref_us(params)
    pierced = True
    ring = True
    side_ant = True
    side_post = True
    for u, s in (c1, c2):
        pierced = pierced and not _point_inside(body, path, u, s, wall / 2.0)
        ring = ring and _point_inside(body, path, u, s + hole_r + 0.5, wall / 2.0)
        side_ant = side_ant and _point_inside(body, path, 0.35, s, wall / 2.0)
        side_post = side_post and _point_inside(body, path, width - 0.35, s, wall / 2.0)
    record(
        "CONTACT_HOLE_wall",
        pierced and ring and side_ant and side_post,
        "CONTACT_HOLE Ø2.9 through the 1.5 medial wall only",
        u=c1[0],
        s=c1[1],
        pierced=1.0 if pierced else 0.0,
        ring=1.0 if ring else 0.0,
        side_ant=1.0 if side_ant else 0.0,
        side_post=1.0 if side_post else 0.0,
    )
    keep_r = KEEPOUT_SIGNAL_DIA / 2.0
    air_ok = True
    sample_y = (wall + KEEPOUT_TOP_Y) / 2.0
    for u, s in (c1, c2):
        for du, ds in ((0.0, 0.0), (keep_r * 0.4, 0.0), (0.0, keep_r * 0.4)):
            if _point_inside(body, path, u + du, s + ds, sample_y):
                air_ok = False
    record(
        "KEEPOUT_SIGNAL_air",
        air_ok,
        "keep-out cylinders Ø7.1 are air; no nylon inside",
        y=sample_y,
    )
    pocket_air = not _point_inside(body, path, cref[0], cref[1], wall + 1.0)
    record(
        "KEEPOUT_REF_air",
        pocket_air,
        "KEEPOUT_REF Ø7.5 pocket is air",
        u=cref[0],
        s=cref[1],
    )
    return checks


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
    wanted = parts or ORDER_PARTS
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
        elif name == "body_full_p15":
            all_checks.extend(run_stage_b_solid_checks(body_bf, lid_bf, path, params))
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
        exported = export_part(assembled, out_dir / name, name)
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
        exported = export_part(lid_shape, out_dir / "lid", "lid")
        files.update(exported)
        if not stl_watertight(out_dir / "lid.stl"):
            raise CheckFail("lid: STL is not watertight")
        all_checks.append(Check("watertight", True, "lid", {}))

    if "coupon" in wanted:
        coupon = build_coupon()
        all_checks.append(Check("one connected solid", True, "coupon", {}))
        exported = export_part(coupon, out_dir / "coupon", "coupon")
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
        )
    return {"files": files, "overlap": overlap, "checks": all_checks}


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
        help="Comma list of parts (default: the five order-1 names)",
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
        parts = (name, "lid", "coupon")
        # Single-variant export still writes lid+coupon beside the body.
        result = build_and_export(
            args.out,
            overrides=overrides,
            crease_bow_from_m=crease_from_m,
            parts=parts if name in ORDER_PARTS else (name,),
        )
        print(json.dumps({"out": str(args.out), "files": list(result["files"])}, indent=2))
        return 0

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
    return 0


def main() -> None:
    try:
        raise SystemExit(cli())
    except CheckFail as exc:
        print(f"CHECK FAIL: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()
