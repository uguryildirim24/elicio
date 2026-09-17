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

Coupon-to-parameter mapping (open item 2; interface v2 note):

* holes Ø1.7, Ø2.9, Ø3.4 → CONTACT_HOLE is 2.9; 1.7 and 3.4 bound it
* slot 0.9 → TONGUE_SLOT height
* slot 0.4 → E4 / JLC thin-feature floor
* rib 0.4 × 3 × 12 → E4 coupon rib
"""
from __future__ import annotations

import argparse
import hashlib
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
    {"SIDE", "VARIANT", "HOOK_PRELOAD", "CREASE_BOW", "HOOK_RADIUS", *REFERENCE_M_KEYS}
)


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


def contact_2_us() -> tuple[float, float]:
    """CONTACT_2 = CONTACT_1 + pitch × (sin, +cos) of PAIR_ANGLE."""
    rad = math.radians(PAIR_ANGLE_DEG)
    u = CONTACT_1[0] + CONTACT_PITCH * math.sin(rad)
    s = CONTACT_1[1] + CONTACT_PITCH * math.cos(rad)
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


def validate_overrides(base: Mapping[str, Any], override: Mapping[str, Any]) -> None:
    """Unknown keys and keys fixed for this release fail before export."""
    known = {canonical_key(k) for k in base} | OVERRIDABLE_KEYS
    for key, value in override.items():
        canon = canonical_key(key)
        if canon not in known:
            raise CheckFail(f"{key}={value}: unknown parameter")
        if canon in OVERRIDABLE_KEYS:
            continue
        if canon == "MOCK_CONTACTS":
            if bool(value) is not True:
                raise CheckFail(
                    f"MOCK_CONTACTS={value}: Stage B keep-out and wire-envelope "
                    "containment checks (plan §3.3) are not implemented; WP8"
                )
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
    u2, s2 = contact_2_us()
    p["CONTACT_2_U"] = u2
    p["CONTACT_2_S"] = s2
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
        "nub : side wall, u": min(NUB_U[0][0] - CAVITY_U[0], CAVITY_U[1] - NUB_U[1][1]),
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
    return {
        "floor (WALL_MEDIAL)": float(params["WALL_MEDIAL"]),
        "anterior side wall": CAVITY_U[0],
        "posterior side wall": float(params["BODY_WIDTH"]) - CAVITY_U[1],
        "top end wall": CAVITY_S[0],
        "top end wall at LIP_GROOVE": CAVITY_S[0] - GROOVE_S[1],
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
        "CONTACT_1": CONTACT_1,
        "CONTACT_2": (float(params["CONTACT_2_U"]), float(params["CONTACT_2_S"])),
    }
    pads = {
        "superior low-u pad": (CAVITY_U[0], CAVITY_U[0] + PAD_SIZE, BOARD_S[0], BOARD_S[0] + PAD_SIZE),
        "superior high-u pad": (CAVITY_U[1] - PAD_SIZE, CAVITY_U[1], BOARD_S[0], BOARD_S[0] + PAD_SIZE),
        "inferior low-u pad": (CAVITY_U[0], CAVITY_U[0] + PAD_SIZE, BOARD_S[1] - PAD_SIZE, BOARD_S[1]),
        "inferior high-u pad": (CAVITY_U[1] - PAD_SIZE, CAVITY_U[1], BOARD_S[1] - PAD_SIZE, BOARD_S[1]),
        "rib": (CAVITY_U[0], CAVITY_U[1], RIB_S[0], RIB_S[1]),
    }
    out: dict[str, float] = {}
    for cname, (cu, cs) in contacts.items():
        for pname, (u0, u1, s0, s1) in pads.items():
            out[f"{cname} to {pname}"] = gap_to_patch(cu, cs, u0, u1, s0, s1)
        # Walls: offset-path distance is exact in u; the end wall is a radial line.
        out[f"{cname} to anterior wall"] = (cu - radius) - CAVITY_U[0]
        out[f"{cname} to posterior wall"] = CAVITY_U[1] - (cu + radius)
        out[f"{cname} to cavity end"] = gap_to_patch(cu, cs, CAVITY_U[0], CAVITY_U[1], CAVITY_S[1], CAVITY_S[1])
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


def run_pre_cad_checks(params: Mapping[str, Any]) -> list[Check]:
    checks: list[Check] = []

    def record(name: str, passed: bool, detail: str, **numbers: float) -> None:
        checks.append(Check(name, passed, detail, numbers))
        if not passed:
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
    nominals = fit_nominals(params)
    for pair, _kind, plan_nominal, _adverse in PLAN_FITS:
        record(
            f"fit: {pair}",
            abs(nominals[pair] - plan_nominal) < 1e-6,
            "nominal from geometry matches plan §3.6",
            nominal=round(nominals[pair], 6),
            plan=plan_nominal,
        )
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
    for name, gap in keepout_clearances(params, path_now).items():
        record(
            f"keep-out: {name}",
            gap > 0.0,
            "KEEPOUT_SIGNAL Ø7.1 clear of solid (body frame)",
            gap=round(gap, 4),
        )
    opening = wire_channel_opening(float(params["PATH_RADIUS"]))
    record(
        "WIRE_CHANNEL_opening",
        opening["physical_opening"] > 0.0,
        "physical opening at u=9.3 must be positive",
        physical_opening=opening["physical_opening"],
        s_entry=opening["s_entry"],
    )
    for bow in (1.0, 3.0, 8.0):
        path = make_path(float(params["BODY_ARC"]), bow)
        report = wire_channel_opening(path.radius)
        record(
            f"WIRE_CHANNEL_bow_{bow:g}",
            report["physical_opening"] > 0.0,
            "opening at supported bow",
            CREASE_BOW=bow,
            physical_opening=report["physical_opening"],
        )
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
) -> Shape:
    def const_u(_s: float) -> tuple[float, float]:
        return u0, u1

    if s1 <= TAIL_S0 + 1e-9:
        sketch = _section(
            path, s0, u0, u1, y0, y1, round_medial=round_medial, fillet_r=fillet_r
        )
        return _revolve_s(path, sketch, s0, s1)
    if s0 >= TAIL_S0 - 1e-9:
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
        path, u0, u1, s0, TAIL_S0, y0, y1, round_medial=round_medial, fillet_r=fillet_r
    ).fuse(
        _path_solid(
            path, u0, u1, TAIL_S0, s1, y0, y1, round_medial=round_medial, fillet_r=fillet_r
        )
    )


def _tail_width(s: float, body_width: float) -> float:
    t = (s - TAIL_S0) / (48.4 - TAIL_S0)
    t = min(1.0, max(0.0, t))
    return body_width + (TAIL_TIP_WIDTH - body_width) * t


def _tail_u(s: float, body_width: float) -> tuple[float, float]:
    width = _tail_width(s, body_width)
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


def build_body_and_lid(
    params: Mapping[str, Any],
) -> tuple[Solid, Solid, PathGeom, dict[str, Any]]:
    """Return (body in body frame, lid in body frame, path, notes)."""
    _require_cad()
    notes: dict[str, Any] = {"fillets": []}
    path = make_path(float(params["BODY_ARC"]), float(params["CREASE_BOW"]))
    width = float(params["BODY_WIDTH"])
    thick = float(params["BODY_THICK"])
    lid_y = float(params["LID_Y"])
    wall = float(params["WALL_MEDIAL"])
    fillet_r = float(params["FILLET_MEDIAL"])
    tail_end = float(params["BODY_ARC"])

    main = _path_solid(path, 0.0, width, 0.0, TAIL_S0, 0.0, thick)

    def tail_u(s: float) -> tuple[float, float]:
        return _tail_u(s, width)

    # Body and tail are built sharp and fused. The two plan-view tip corners
    # take TIP_ROUND first, then FILLET_MEDIAL runs along the whole medial
    # outline except the top end. Filleting the tip after the medial fillet
    # capped it at 1.6 (full) and failed on thin; fusing two separately
    # filleted pieces left a 0.03 mm² sliver face the 3MF mesher rejects.
    tail: Shape = _loft_s(path, TAIL_S0, tail_end, tail_u, 0.0, thick, step=1.5)
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
    recess = _path_solid(
        path,
        -1.0,
        width + 1.0,
        0.0,
        LID_RECESS_S1,
        lid_y,
        thick + 4.0,
    )
    body = body.cut(recess)

    cavity = _path_solid(
        path,
        CAVITY_U[0],
        CAVITY_U[1],
        CAVITY_S[0],
        CAVITY_S[1],
        wall,
        thick + 1.0,
    )
    body = body.cut(cavity)

    rib = _path_solid(path, CAVITY_U[0], CAVITY_U[1], RIB_S[0], RIB_S[1], RIB_Y[0], RIB_Y[1])
    body = body.fuse(rib)
    pad_u = (
        (CAVITY_U[0], CAVITY_U[0] + PAD_SIZE),
        (CAVITY_U[1] - PAD_SIZE, CAVITY_U[1]),
    )
    pad_s = (
        (BOARD_S[0], BOARD_S[0] + PAD_SIZE),
        (BOARD_S[1] - PAD_SIZE, BOARD_S[1]),
    )
    for u0, u1 in pad_u:
        for s0, s1 in pad_s:
            pad = _path_solid(path, u0, u1, s0, s1, PAD_Y[0], PAD_Y[1])
            body = body.fuse(pad)

    if params["MOCK_CONTACTS"]:
        for u, s in (CONTACT_1, (params["CONTACT_2_U"], params["CONTACT_2_S"]), CONTACT_REF):
            cap = _cap_solid(path, float(u), float(s))
            body = body.fuse(cap)
    else:
        hole_r = CONTACT_HOLE / 2.0
        for u, s in (CONTACT_1, (params["CONTACT_2_U"], params["CONTACT_2_S"]), CONTACT_REF):
            origin = _vec(path, float(u), float(s), 0.0)
            hole = Solid.make_cylinder(hole_r, thick + 4.0).locate(
                Location((origin.X, -1.0, origin.Z))
            )
            body = body.cut(hole)
        pocket_c = _vec(path, CONTACT_REF[0], CONTACT_REF[1], 0.0)
        pocket = Solid.make_cylinder(POCKET_DIA / 2.0, lid_y - wall + 0.2).locate(
            Location((pocket_c.X, wall, pocket_c.Z))
        )
        body = body.cut(pocket)
        channel = _path_solid(
            path, WIRE_U[0], WIRE_U[1], WIRE_S[0], WIRE_S[1], WIRE_Y[0], WIRE_Y[1]
        )
        body = body.cut(channel)
        # CABLE_EXIT through the posterior side wall at s 36, y 3.
        exit_pt = _vec(path, width, CABLE_EXIT_S, CABLE_EXIT_Y)
        a = angle_at(path, CABLE_EXIT_S)
        normal = Vector(math.cos(a), 0.0, math.sin(a))
        exit_axis = Axis(exit_pt, normal)
        cable = Solid.make_cylinder(CABLE_EXIT_DIA / 2.0, 6.0, exit_axis)
        body = body.cut(cable.move(Location((-3.0 * normal.X, 0.0, -3.0 * normal.Z))))

    groove = _path_solid(
        path,
        GROOVE_U[0],
        GROOVE_U[1],
        GROOVE_S[0],
        GROOVE_S[1],
        lid_y + GROOVE_Y_OFF[0],
        lid_y + GROOVE_Y_OFF[1],
    )
    body = body.cut(groove)
    slot = _path_solid(
        path,
        TONGUE_SLOT_U[0],
        TONGUE_SLOT_U[1],
        TONGUE_SLOT_S[0],
        TONGUE_SLOT_S[1],
        lid_y + TONGUE_SLOT_Y_OFF[0],
        lid_y + TONGUE_SLOT_Y_OFF[1],
    )
    body = body.cut(slot)
    web_pocket = _path_solid(
        path,
        TONGUE_SLOT_U[0],
        TONGUE_SLOT_U[1],
        WEB_POCKET_S[0],
        WEB_POCKET_S[1],
        lid_y + WEB_POCKET_Y_OFF[0],
        lid_y + WEB_POCKET_Y_OFF[1],
    )
    body = body.cut(web_pocket)

    # Lid plate: plan outline inset CLEAR_FIT, s -0.2 to 46.4.
    clear = float(params["CLEAR_FIT"])
    lid_thick = float(params["LID_THICK"])
    plate_main = _path_solid(
        path,
        clear,
        width - clear,
        LID_PLATE_S[0],
        TAIL_S0,
        lid_y,
        lid_y + lid_thick,
    )

    def lid_u(s: float) -> tuple[float, float]:
        u0, u1 = _tail_u(s, width)
        return u0 + clear, u1 - clear

    plate_tail = _loft_s(
        path,
        TAIL_S0,
        LID_PLATE_S[1],
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
            and abs(_approx_s(path, e.center()) - LID_PLATE_S[0]) > 0.05
        ]
        lid, applied = _try_fillet(lid, rim, float(params["LID_EDGE"]))
        notes["fillets"].append(
            _fillet_note("LID_EDGE (plate rim except the lip end)", float(params["LID_EDGE"]), applied)
        )
    except Exception as exc:
        raise CheckFail(f"LID_EDGE: rim fillet failed ({exc})") from exc

    lip_y0 = lid_y + lid_thick - LIP_LENGTH
    lip = _path_solid(path, LIP_U[0], LIP_U[1], LIP_S[0], LIP_S[1], lip_y0, lid_y + lid_thick)
    lid = lid.fuse(lip)
    bump = _path_solid(
        path,
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
    web = _path_solid(
        path,
        tongue_u0,
        tongue_u1,
        LID_WEB_S[0],
        LID_WEB_S[1],
        lid_y + LID_WEB_Y_OFF[0],
        lid_y + LID_WEB_Y_OFF[1],
    )
    tongue = _path_solid(
        path,
        tongue_u0,
        tongue_u1,
        LID_TONGUE_S[0],
        LID_TONGUE_S[1],
        lid_y + LID_TONGUE_Y_OFF[0],
        lid_y + LID_TONGUE_Y_OFF[1],
    )
    lid = lid.fuse(web).fuse(tongue)
    for u0, u1 in NUB_U:
        nub = _path_solid(path, u0, u1, NUB_S[0], NUB_S[1], lid_y - NUB, lid_y)
        lid = lid.fuse(nub)

    label = emboss_label(params, list(params.get("_defaults_used", [])))
    try:
        if not FONT_PATH.is_file():
            raise CheckFail(f"emboss font missing: {FONT_PATH}")
        mid = _vec(path, width / 2.0, 28.0, lid_y)
        plane = Plane(
            origin=Vector(mid.X, lid_y, mid.Z),
            x_dir=Vector(0, 0, -1),
            y_dir=Vector(1, 0, 0),
        )
        text = plane * Text(label, font_size=1.4, font_path=str(FONT_PATH))
        letters = extrude(text, amount=EMBOSS)
        lid = lid.fuse(letters)
        notes["emboss"] = label
        notes["emboss_font"] = FONT_PATH.name
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
    cavity = _path_solid(
        path,
        CAVITY_U[0],
        CAVITY_U[1],
        CAVITY_S[0],
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
        ("CONTACT_1", CONTACT_1),
        ("CONTACT_2", (float(params["CONTACT_2_U"]), float(params["CONTACT_2_S"]))),
        ("CONTACT_REF", CONTACT_REF),
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
    openings = {
        str(bow): wire_channel_opening(make_path(float(params["BODY_ARC"]), bow).radius)
        for bow in (1.0, 3.0, 8.0)
    }
    openings["clamped"] = wire_channel_opening(path.radius)
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


def build_and_export(
    out_dir: Path,
    *,
    overrides: Mapping[str, Any] | None = None,
    crease_bow_from_m: bool = False,
    parts: tuple[str, ...] | None = None,
) -> dict[str, Any]:
    _require_cad()
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
        for contact, ok in contact_caps(body_bf, path, params).items():
            if not ok:
                raise CheckFail(f"contact axes: {name} {contact} dome does not stand to −y")
            all_checks.append(Check(f"contact axis −y: {contact}", True, name, {}))
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
