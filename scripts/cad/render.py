#!/usr/bin/env python3.13
"""Headless renders and one-page drawing for the order-1 gauge (WP3).

Reads committed STL files and ``manifest.json``. Does not rebuild solids.
Does not open a GUI. PNG and PDF metadata dates are pinned so a second
run is byte-identical.

    .venv/bin/python scripts/cad/render.py --out docs/fab/cad/v1/

Writes ``render_medial.png``, ``render_lateral.png``, ``drawing.pdf`` and
updates the ``views`` map in the manifest. Solid hashes in ``files`` are
not rewritten.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import struct
import sys
import zlib
from pathlib import Path
from typing import Any

import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
DEFAULT_OUT = REPO_ROOT / "docs" / "fab" / "cad" / "v1"
FONT_PATH = SCRIPT_DIR / "fonts" / "LiberationSans-Regular.ttf"
PIN_DATE = "2026-09-16T00:00:00Z"
PDF_DATE = "D:20260916000000Z"
PNG_SIG = b"\x89PNG\r\n\x1a\n"
DPI = 150
VIEW_FILES = ("render_medial.png", "render_lateral.png", "drawing.pdf")
VIEWS_HASH_RULE = (
    "SHA-256 of raw file bytes. PNG tIME/tEXt/zTXt/iTXt/eXIf rewritten; "
    "Creation Time text and PDF CreationDate/ModDate/ID pinned to "
    "2026-09-16T00:00:00Z. Same pin as the solids hash_rule timestamp."
)

# Nylon-grey, lid slightly warmer, thin slightly cooler.
COLOR_FULL = np.array([0.74, 0.76, 0.78])
COLOR_THIN = np.array([0.60, 0.70, 0.80])
COLOR_LID = np.array([0.86, 0.82, 0.72])


def view_light(right: np.ndarray, up: np.ndarray, vf: np.ndarray) -> np.ndarray:
    vec = 0.70 * vf + 0.40 * up + 0.25 * right
    return vec / np.linalg.norm(vec)


class RenderError(RuntimeError):
    """Render or drawing failed."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _png_chunk(tag: bytes, data: bytes) -> bytes:
    crc = zlib.crc32(tag + data) & 0xFFFFFFFF
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)


def pin_png(data: bytes) -> bytes:
    if not data.startswith(PNG_SIG):
        raise RenderError("not a PNG")
    pos = 8
    kept: list[tuple[bytes, bytes]] = []
    while pos < len(data):
        length = int.from_bytes(data[pos : pos + 4], "big")
        tag = data[pos + 4 : pos + 8]
        chunk = data[pos + 8 : pos + 8 + length]
        pos += 12 + length
        if tag in {b"tIME", b"tEXt", b"zTXt", b"iTXt", b"eXIf"}:
            continue
        kept.append((tag, chunk))
    extra = [
        (b"tEXt", b"Software\x00elicio-cad"),
        (b"tEXt", b"Creation Time\x00" + PIN_DATE.encode("ascii")),
    ]
    out = bytearray(PNG_SIG)
    for tag, chunk in kept:
        if tag == b"IHDR":
            out.extend(_png_chunk(tag, chunk))
            for etag, edata in extra:
                out.extend(_png_chunk(etag, edata))
        else:
            out.extend(_png_chunk(tag, chunk))
    return bytes(out)


def pin_pdf(data: bytes) -> bytes:
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import ArrayObject, ByteStringObject

    reader = PdfReader(io.BytesIO(data))
    writer = PdfWriter()
    writer.append(reader)
    writer.add_metadata(
        {
            "/Title": "Elicio BTE fit gauge v1 drawing",
            "/Creator": "elicio-cad",
            "/Producer": "elicio-cad",
            "/CreationDate": PDF_DATE,
            "/ModDate": PDF_DATE,
        }
    )
    ident = b"elicio-cad-v1draw"
    writer._ID = ArrayObject([ByteStringObject(ident), ByteStringObject(ident)])
    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()


def configure_matplotlib() -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager

    if FONT_PATH.is_file():
        font_manager.fontManager.addfont(str(FONT_PATH))
        name = font_manager.FontProperties(fname=str(FONT_PATH)).get_name()
        plt.rcParams["font.family"] = name
    plt.rcParams.update(
        {
            "figure.autolayout": False,
            "path.simplify": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.hashsalt": "elicio-cad-v1",
            "axes.unicode_minus": False,
        }
    )


def load_stl(path: Path) -> tuple[np.ndarray, np.ndarray]:
    import trimesh

    mesh = trimesh.load(str(path), process=False, force="mesh")
    vertices = np.asarray(mesh.vertices, dtype=np.float64)
    faces = np.asarray(mesh.faces, dtype=np.int64)
    if vertices.size == 0 or faces.size == 0:
        raise RenderError(f"{path.name}: empty mesh")
    return vertices, faces


def rotate_x(vertices: np.ndarray, deg: float) -> np.ndarray:
    rad = np.radians(deg)
    cos_a, sin_a = np.cos(rad), np.sin(rad)
    out = np.array(vertices, copy=True)
    y, z = out[:, 1], out[:, 2]
    out[:, 1] = y * cos_a - z * sin_a
    out[:, 2] = y * sin_a + z * cos_a
    return out


def to_body_frame(vertices: np.ndarray, theta_deg: float) -> np.ndarray:
    """Undo assemble_shell's rotate(Axis.X, -THETA_DEG)."""
    return rotate_x(vertices, float(theta_deg))


def basis(view_forward: np.ndarray, up_hint: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    vf = np.asarray(view_forward, dtype=np.float64)
    vf = vf / np.linalg.norm(vf)
    up = np.asarray(up_hint, dtype=np.float64)
    right = np.cross(up, vf)
    norm = np.linalg.norm(right)
    if norm < 1e-9:
        up = np.array([1.0, 0.0, 0.0])
        right = np.cross(up, vf)
        norm = np.linalg.norm(right)
    right = right / norm
    up = np.cross(vf, right)
    up = up / np.linalg.norm(up)
    return right, up, vf


def add_mesh(
    ax,
    vertices: np.ndarray,
    faces: np.ndarray,
    *,
    origin: np.ndarray,
    right: np.ndarray,
    up: np.ndarray,
    vf: np.ndarray,
    color: np.ndarray,
    light: np.ndarray,
) -> np.ndarray:
    from matplotlib.collections import PolyCollection

    tri = vertices[faces]
    normals = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    lengths = np.linalg.norm(normals, axis=1)
    good = lengths > 1e-12
    tri, normals, lengths = tri[good], normals[good], lengths[good]
    normals = normals / lengths[:, None]
    visible = normals @ vf > 0.02
    tri, normals, lengths = tri[visible], normals[visible], lengths[visible]
    if len(tri) == 0:
        return np.zeros((0, 2))
    # Offset along the normal so coplanar boolean leftovers (contact caps)
    # do not sparkle. This is a draw offset; the STL is unchanged.
    tri = tri + 0.03 * normals[:, None, :]
    centroids = tri.mean(axis=1)
    order = np.argsort(centroids @ vf + 1e-5 * lengths)
    tri, normals = tri[order], normals[order]
    uv = np.stack(((tri - origin) @ right, (tri - origin) @ up), axis=-1)
    intensity = 0.38 + 0.62 * np.clip(normals @ light, 0.0, 1.0)
    rgba = np.zeros((len(tri), 4))
    rgba[:, :3] = np.outer(intensity, color)
    rgba[:, 3] = 1.0
    coll = PolyCollection(
        uv,
        facecolors=rgba,
        edgecolors="none",
        linewidths=0.0,
        antialiaseds=True,
    )
    ax.add_collection(coll)
    return uv.reshape(-1, 2)


def finish_view(
    ax,
    points: np.ndarray,
    *,
    title: str,
    labels: list[tuple[float, float, str]],
    commit: str,
    scale_mm: float = 10.0,
) -> None:
    ax.set_aspect("equal")
    ax.set_axis_off()
    ax.set_facecolor("white")
    if points.size == 0:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        return
    xmin, ymin = points.min(axis=0)
    xmax, ymax = points.max(axis=0)
    span = max(xmax - xmin, ymax - ymin, 1.0)
    pad = 0.08 * span
    ax.set_xlim(xmin - pad, xmax + pad)
    ax.set_ylim(ymin - pad, ymax + pad)
    bar_x = xmin
    bar_y = ymin - 0.04 * span
    ax.plot([bar_x, bar_x + scale_mm], [bar_y, bar_y], color="black", lw=1.4, solid_capstyle="butt")
    ax.plot([bar_x, bar_x], [bar_y - 0.6, bar_y + 0.6], color="black", lw=1.2)
    ax.plot(
        [bar_x + scale_mm, bar_x + scale_mm],
        [bar_y - 0.6, bar_y + 0.6],
        color="black",
        lw=1.2,
    )
    ax.text(
        bar_x + scale_mm / 2.0,
        bar_y - 1.4,
        f"{scale_mm:.0f} mm",
        ha="center",
        va="top",
        fontsize=8,
        color="black",
    )
    ax.text(
        0.01,
        0.99,
        title,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9,
        color="black",
    )
    ax.text(
        0.99,
        0.01,
        commit[:12],
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=7,
        family="monospace",
        color="black",
    )
    for x, y, text in labels:
        ax.text(x, y, text, fontsize=8, color="black", ha="left", va="bottom")


def save_png(fig, path: Path) -> bytes:
    import matplotlib.pyplot as plt

    buf = io.BytesIO()
    fig.savefig(
        buf,
        format="png",
        dpi=DPI,
        facecolor="white",
        edgecolor="none",
        bbox_inches=None,
        pad_inches=0.15,
    )
    plt.close(fig)
    return pin_png(buf.getvalue())


def save_pdf(fig, path: Path) -> bytes:
    import matplotlib.pyplot as plt

    buf = io.BytesIO()
    fig.savefig(
        buf,
        format="pdf",
        facecolor="white",
        edgecolor="none",
        bbox_inches=None,
    )
    plt.close(fig)
    return pin_pdf(buf.getvalue())


def write_bytes(path: Path, data: bytes) -> dict[str, Any]:
    path.write_bytes(data)
    return {"sha256": sha256_bytes(data), "bytes": len(data)}


def render_medial(
    out_dir: Path,
    *,
    theta_deg: float,
    commit: str,
) -> dict[str, Any]:
    import matplotlib.pyplot as plt

    full_v, full_f = load_stl(out_dir / "body_full_p15.stl")
    thin_v, thin_f = load_stl(out_dir / "body_thin_p15.stl")
    full_v = to_body_frame(full_v, theta_deg)
    thin_v = to_body_frame(thin_v, theta_deg)
    gap = 8.0
    offset = float(full_v[:, 0].max() - thin_v[:, 0].min() + gap)
    thin_v = np.array(thin_v, copy=True)
    thin_v[:, 0] += offset
    # Medial 3/4: mostly −Y so caps face the camera; a little +X/+Z shows thickness.
    right, up, vf = basis(np.array([0.28, -1.0, 0.18]), np.array([0.0, 0.0, 1.0]))
    light = view_light(right, up, vf)
    origin = np.array(
        [
            0.5 * (full_v[:, 0].mean() + thin_v[:, 0].mean()),
            0.5 * (full_v[:, 1].mean() + thin_v[:, 1].mean()),
            0.5 * (full_v[:, 2].mean() + thin_v[:, 2].mean()),
        ]
    )
    fig, ax = plt.subplots(figsize=(11.0, 6.2), dpi=DPI, facecolor="white")
    pts = []
    pts.append(add_mesh(ax, full_v, full_f, origin=origin, right=right, up=up, vf=vf, color=COLOR_FULL, light=light))
    pts.append(add_mesh(ax, thin_v, thin_f, origin=origin, right=right, up=up, vf=vf, color=COLOR_THIN, light=light))
    points = np.vstack([p for p in pts if p.size])
    full_c = (full_v - origin) @ np.stack((right, up), axis=1)
    thin_c = (thin_v - origin) @ np.stack((right, up), axis=1)
    labels = [
        (float(full_c[:, 0].mean()), float(full_c[:, 1].max()) + 2.0, "full p15  BODY_THICK 9.0"),
        (float(thin_c[:, 0].mean()), float(thin_c[:, 1].max()) + 2.0, "thin p15  BODY_THICK 7.0"),
    ]
    finish_view(
        ax,
        points,
        title="medial  full p15 + thin p15  caps, tail, hook",
        labels=labels,
        commit=commit,
        scale_mm=10.0,
    )
    fig.subplots_adjust(left=0.04, right=0.98, top=0.96, bottom=0.08)
    dest = out_dir / "render_medial.png"
    return write_bytes(dest, save_png(fig, dest))


def render_lateral(
    out_dir: Path,
    *,
    theta_deg: float,
    commit: str,
) -> dict[str, Any]:
    import matplotlib.pyplot as plt

    body_v, body_f = load_stl(out_dir / "body_full_p15.stl")
    lid_v, lid_f = load_stl(out_dir / "lid.stl")
    body_v = to_body_frame(body_v, theta_deg)
    lid_v = to_body_frame(lid_v, theta_deg)
    right, up, vf = basis(np.array([-0.22, 1.0, 0.16]), np.array([0.0, 0.0, 1.0]))
    light = view_light(right, up, vf)
    origin = np.concatenate((body_v, lid_v)).mean(axis=0)
    fig, ax = plt.subplots(figsize=(11.0, 6.2), dpi=DPI, facecolor="white")
    pts = []
    pts.append(add_mesh(ax, body_v, body_f, origin=origin, right=right, up=up, vf=vf, color=COLOR_FULL, light=light))
    pts.append(add_mesh(ax, lid_v, lid_f, origin=origin, right=right, up=up, vf=vf, color=COLOR_LID, light=light))
    points = np.vstack([p for p in pts if p.size])
    finish_view(
        ax,
        points,
        title="lateral  full p15  lid seated, hook",
        labels=[],
        commit=commit,
        scale_mm=10.0,
    )
    fig.subplots_adjust(left=0.04, right=0.98, top=0.96, bottom=0.08)
    dest = out_dir / "render_lateral.png"
    return write_bytes(dest, save_png(fig, dest))


def _rect(ax, s0, s1, y0, y1, *, fc, ec="black", lw=0.4, hatch=None, z=2):
    from matplotlib.patches import Rectangle

    ax.add_patch(
        Rectangle(
            (s0, y0),
            s1 - s0,
            y1 - y0,
            facecolor=fc,
            edgecolor=ec,
            linewidth=lw,
            hatch=hatch,
            zorder=z,
        )
    )


def draw_closure_geometry(ax, cad, params: dict[str, Any]) -> dict[str, Any]:
    """(s, y) from plan §3.3 / §3.5 constants, not pixels."""
    lid_y = float(params["LID_Y"])
    thick = float(params["BODY_THICK"])
    lid_t = float(params["LID_THICK"])
    lip_y0 = lid_y + lid_t - cad.LIP_LENGTH
    _rect(ax, cad.LIP_S[0], 48.4, 0.0, thick, fc="#d9d9d9", ec="#444444", lw=0.5, z=1)
    _rect(ax, cad.LID_PLATE_S[0], cad.LID_PLATE_S[1], lid_y, lid_y + lid_t, fc="#e6d9b8", ec="#5a4a20", lw=0.5, z=3)
    _rect(ax, cad.LIP_S[0], cad.LIP_S[1], lip_y0, lid_y + lid_t, fc="#e6d9b8", ec="#5a4a20", lw=0.6, z=4)
    _rect(ax, cad.LIP_S[1], cad.LIP_S[1] + cad.BUMP_OUT, lip_y0, lip_y0 + cad.BUMP_TALL, fc="#c9a24a", ec="#5a4a20", lw=0.6, z=5)
    _rect(ax, cad.GROOVE_S[0], cad.GROOVE_S[1], lid_y + cad.GROOVE_Y_OFF[0], lid_y + cad.GROOVE_Y_OFF[1], fc="#ffffff", ec="#222222", lw=0.7, z=2)
    _rect(ax, cad.NUB_S[0], cad.NUB_S[1], lid_y - cad.NUB, lid_y, fc="#e6d9b8", ec="#5a4a20", lw=0.6, hatch="///", z=4)
    _rect(ax, cad.LID_WEB_S[0], cad.LID_WEB_S[1], lid_y + cad.LID_WEB_Y_OFF[0], lid_y + cad.LID_WEB_Y_OFF[1], fc="#e6d9b8", ec="#5a4a20", lw=0.6, z=4)
    _rect(ax, cad.LID_TONGUE_S[0], cad.LID_TONGUE_S[1], lid_y + cad.LID_TONGUE_Y_OFF[0], lid_y + cad.LID_TONGUE_Y_OFF[1], fc="#e6d9b8", ec="#5a4a20", lw=0.6, z=4)
    _rect(ax, cad.WEB_POCKET_S[0], cad.WEB_POCKET_S[1], lid_y + cad.WEB_POCKET_Y_OFF[0], lid_y + cad.WEB_POCKET_Y_OFF[1], fc="#ffffff", ec="#222222", lw=0.6, z=2)
    _rect(ax, cad.TONGUE_SLOT_S[0], cad.TONGUE_SLOT_S[1], lid_y + cad.TONGUE_SLOT_Y_OFF[0], lid_y + cad.TONGUE_SLOT_Y_OFF[1], fc="#ffffff", ec="#222222", lw=0.6, z=2)
    return {"lid_y": lid_y, "lid_t": lid_t, "lip_y0": lip_y0, "thick": thick}


def _section_axes(ax, xlim, ylim, title: str) -> None:
    ax.set_aspect("equal")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xlabel("s (mm)", fontsize=7)
    ax.set_ylabel("y (mm)", fontsize=7)
    ax.set_title(title, fontsize=8)
    ax.tick_params(labelsize=6)


def shaded_pair(ax, body_v, body_f, lid_v, lid_f, view_forward, title: str):
    right, up, vf = basis(np.asarray(view_forward, dtype=np.float64), np.array([0.0, 0.0, 1.0]))
    light = view_light(right, up, vf)
    origin = np.concatenate((body_v, lid_v)).mean(axis=0)
    add_mesh(ax, body_v, body_f, origin=origin, right=right, up=up, vf=vf, color=COLOR_FULL, light=light)
    add_mesh(ax, lid_v, lid_f, origin=origin, right=right, up=up, vf=vf, color=COLOR_LID, light=light)
    pts = np.concatenate(
        (
            (body_v - origin) @ np.stack((right, up), axis=1),
            (lid_v - origin) @ np.stack((right, up), axis=1),
        )
    )
    ax.set_aspect("equal")
    ax.set_axis_off()
    lo, hi = pts.min(axis=0), pts.max(axis=0)
    span = max(*(hi - lo), 1.0)
    pad = 0.10 * span
    ax.set_xlim(lo[0] - pad, hi[0] + pad)
    ax.set_ylim(lo[1] - pad, hi[1] + pad)
    ax.set_title(title, fontsize=9)
    bar_x, bar_y = lo[0], lo[1] - 0.04 * span
    ax.plot([bar_x, bar_x + 10.0], [bar_y, bar_y], color="black", lw=1.1)
    ax.text(bar_x + 5.0, bar_y - 0.8, "10 mm", ha="center", va="top", fontsize=7)
    return origin, right, up


def _annotate(ax, origin, right, up, xyz, text, dy=0.0, dx=4.0):
    uv = (np.asarray(xyz) - origin) @ np.stack((right, up), axis=1)
    ax.annotate(
        text,
        xy=(uv[0], uv[1]),
        xytext=(uv[0] + dx, uv[1] + 3.0 + dy),
        fontsize=6.5,
        arrowprops={"arrowstyle": "->", "lw": 0.5, "color": "black"},
        color="black",
    )


def draw_page(
    out_dir: Path,
    *,
    cad,
    manifest: dict[str, Any],
    commit: str,
) -> dict[str, Any]:
    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec

    params = manifest["parameters"]
    theta = float(params["THETA_DEG"])
    body_v, body_f = load_stl(out_dir / "body_full_p15.stl")
    lid_v, lid_f = load_stl(out_dir / "lid.stl")
    body_v = to_body_frame(body_v, theta)
    lid_v = to_body_frame(lid_v, theta)
    fig = plt.figure(figsize=(8.27, 11.69), dpi=100, facecolor="white")
    gs = GridSpec(
        4,
        6,
        figure=fig,
        height_ratios=[1.20, 1.05, 1.20, 0.80],
        hspace=0.42,
        wspace=0.55,
        left=0.07,
        right=0.97,
        top=0.93,
        bottom=0.06,
    )
    ax_side = fig.add_subplot(gs[0, 0:3])
    ax_med = fig.add_subplot(gs[0, 3:6])
    ax_lip = fig.add_subplot(gs[1, 0:2])
    ax_nub = fig.add_subplot(gs[1, 2:4])
    ax_tail = fig.add_subplot(gs[1, 4:6])
    ax_m = fig.add_subplot(gs[2, 0:3])
    ax_e = fig.add_subplot(gs[2, 3:6])
    ax_block = fig.add_subplot(gs[3, :])

    origin, right, up = shaded_pair(
        ax_side, body_v, body_f, lid_v, lid_f, (-1.0, 0.35, 0.08), "side  (thickness × length)"
    )
    hook_root = np.array([float(params["HOOK_ROOT_X"]), float(params["HOOK_ROOT_Y"]), 0.0])
    _annotate(ax_side, origin, right, up, hook_root, "M4 root Y = M4/2", dy=2.0)
    _annotate(
        ax_side,
        origin,
        right,
        up,
        np.array([float(params["BODY_WIDTH"]) / 2.0, float(params["BODY_THICK"]), -float(params["TOTAL_CHORD"]) / 2.0]),
        "M3 SPAN 10.35 vs 11",
        dy=8.0,
        dx=2.0,
    )

    origin, right, up = shaded_pair(
        ax_med, body_v, body_f, lid_v, lid_f, (0.08, -1.0, 0.05), "medial  (caps toward viewer)"
    )
    path = cad.make_path(float(params["BODY_ARC"]), float(params["CREASE_BOW"]))
    x1, _y1, z1 = cad.p_xyz(path, cad.CONTACT_1[0], cad.CONTACT_1[1], 0.0)
    xr, _yr, zr = cad.p_xyz(path, cad.CONTACT_REF[0], cad.CONTACT_REF[1], 0.0)
    _annotate(ax_med, origin, right, up, np.array([x1, 0.0, z1]), "C1  M1 chord along Z", dy=4.0)
    _annotate(ax_med, origin, right, up, np.array([xr, 0.0, zr]), "REF  M6 recorded", dy=-4.0)
    hook_inner = np.array(
        [
            float(params.get("HOOK_ROOT_X", 4.0)) - float(params["HOOK_RADIUS"]),
            float(params["HOOK_ROOT_Y"]),
            0.0,
        ]
    )
    _annotate(ax_med, origin, right, up, hook_inner, "M8 HOOK_RADIUS 13.5", dy=-2.0, dx=-12.0)

    for ax in (ax_lip, ax_nub, ax_tail):
        info = draw_closure_geometry(ax, cad, params)
    _section_axes(ax_lip, (-2.4, 2.8), (2.8, 10.2), "lip, bump, groove  E5")
    ax_lip.text(cad.LIP_S[0] + 0.05, info["lip_y0"] + 2.4, "lip 1.0", fontsize=6.5)
    ax_lip.text(cad.LIP_S[1] + 0.05, info["lip_y0"] + 0.15, "bump 0.5", fontsize=6.5)
    ax_lip.text(cad.GROOVE_S[1] + 0.08, info["lid_y"] + cad.GROOVE_Y_OFF[0] + 0.15, "groove", fontsize=6.5)
    _section_axes(ax_nub, (16.6, 19.4), (6.6, 9.4), "nubs  E3  (u 1.9–2.7, 14.3–15.1)")
    ax_nub.text(cad.NUB_S[0] + 0.05, info["lid_y"] - cad.NUB - 0.35, "nub 0.8", fontsize=6.5)
    _section_axes(ax_tail, (44.6, 49.4), (6.4, 9.6), "web, tongue, slot  E1")
    ax_tail.text(cad.LID_WEB_S[0], info["lid_y"] + cad.LID_WEB_Y_OFF[0] - 0.35, "web 0.8", fontsize=6.5)
    ax_tail.text(cad.LID_TONGUE_S[0], info["lid_y"] + cad.LID_TONGUE_Y_OFF[0] - 0.35, "tongue 0.5", fontsize=6.5)

    ax_m.axis("off")
    ax_e.axis("off")
    m_rows = [
        ["M", "lands on the part", "mm"],
        ["M1", "ear-root chord; gate vs TOTAL_CHORD", f"{params['M1']:.2f}"],
        ["M2", "crease arc (BODY_ARC 48.4); bow source", f"{params['M2']:.2f}"],
        ["M3", "sulcus; SPAN = 9.0 + 1.35 crown = 10.35", f"{params['M3']:.2f}"],
        ["M4", "HOOK_ROOT.Y = M4/2 = 3.0", f"{params['M4']:.2f}"],
        ["M5", "GLASSES_FLAT 0.8 on hook (M5 > 0)", f"{params['M5']:.2f}"],
        ["M6", "recorded for WP7a; not a CAD driver", f"{params['M6']:.2f}"],
        ["M7", "recorded for WP7a; not a CAD driver", f"{params['M7']:.2f}"],
        ["M8", "HOOK_RADIUS = M8 + 1.75 + 0.75 = 13.5", f"{params['M8']:.2f}"],
    ]
    table_m = ax_m.table(
        cellText=m_rows, loc="center", cellLoc="left", colWidths=[0.10, 0.72, 0.18]
    )
    table_m.auto_set_font_size(False)
    table_m.set_fontsize(6.2)
    table_m.scale(1.05, 1.38)
    ax_m.set_title("M1–M8  (plan §3.3 values)", fontsize=9)

    ex = manifest["exceptions"]
    e_rows = [["id", "feature", "nominal", "fitted min"]]
    e_rows.append(["E1", "tongue", "0.5", "0.4"])
    e_rows.append(["E2", "rib (locating only)", "0.8", "0.8"])
    e_rows.append(["E3", "nubs", "0.8", "0.6"])
    e_rows.append(["E4", "coupon rib", "0.4", "0.4"])
    e_rows.append(["E5 lip", "lip cantilever", f"{ex['E5']['plan_size']['lip']}", f"{ex['E5']['minimum']['lip']}"])
    e_rows.append(["E5 bump", "snap bump", f"{ex['E5']['plan_size']['bump']}", f"{ex['E5']['minimum']['bump']}"])
    table_e = ax_e.table(
        cellText=e_rows, loc="center", cellLoc="left", colWidths=[0.16, 0.40, 0.22, 0.22]
    )
    table_e.auto_set_font_size(False)
    table_e.set_fontsize(6.2)
    table_e.scale(1.05, 1.38)
    ax_e.set_title("E1–E5  nominal and fitted minimum (§3.6)", fontsize=9)

    ax_block.axis("off")
    gate = manifest["chord_gate"]
    title = (
        "Elicio BTE fit gauge  v1  drawing.pdf\n"
        f"parameter set: default.toml  REF={'yes' if manifest['ref_build'] else 'no'}  "
        f"VARIANT={params['VARIANT']}  HOOK_PRELOAD={params['HOOK_PRELOAD']}\n"
        f"CREASE_BOW={params['CREASE_BOW']}  TOTAL_CHORD={params['TOTAL_CHORD']:.3f}  "
        f"chord gate={gate['gate']:.3f}  (M1 ≥ TOTAL_CHORD + 3)\n"
        f"commit (solids last-change) {commit}   date {PIN_DATE}\n"
        "General tolerance: ±0.3 mm under 100 mm, JLC MJF PA12\n"
        "Dimensions are plan §3.3 / §3.5 values, not measured from pixels."
    )
    ax_block.text(0.0, 1.0, title, ha="left", va="top", fontsize=8, family="monospace")
    fig.suptitle("Elicio BTE fit gauge v1 — reference body + lid", fontsize=12, y=0.98)
    dest = out_dir / "drawing.pdf"
    return write_bytes(dest, save_pdf(fig, dest))


def load_cad():
    import importlib.util

    script = SCRIPT_DIR / "bte_fit_shell.py"
    spec = importlib.util.spec_from_file_location("bte_fit_shell", script)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules["bte_fit_shell"] = module
    spec.loader.exec_module(module)
    return module


def update_manifest(out_dir: Path, views: dict[str, Any], views_commit: str, solids_commit: str) -> None:
    path = out_dir / "manifest.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["views"] = views
    payload["views_hash_rule"] = VIEWS_HASH_RULE
    payload["views_commit"] = views_commit
    payload["commit"] = solids_commit
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render order-1 PNGs and drawing.pdf.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args(argv)
    out_dir = args.out
    manifest_path = out_dir / "manifest.json"
    if not manifest_path.is_file():
        raise RenderError(f"missing {manifest_path}")
    for name in ("body_full_p15.stl", "body_thin_p15.stl", "lid.stl"):
        if not (out_dir / name).is_file():
            raise RenderError(f"missing {out_dir / name}")
    configure_matplotlib()
    cad = load_cad()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    theta = float(manifest["parameters"]["THETA_DEG"])
    solids_commit = cad.git_commit_solids(REPO_ROOT)
    views = {
        "render_medial.png": render_medial(out_dir, theta_deg=theta, commit=solids_commit),
        "render_lateral.png": render_lateral(out_dir, theta_deg=theta, commit=solids_commit),
        "drawing.pdf": draw_page(out_dir, cad=cad, manifest=manifest, commit=solids_commit),
    }
    update_manifest(out_dir, views, solids_commit, solids_commit)
    print(json.dumps({"out": str(out_dir), "views": views}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RenderError as exc:
        print(f"RENDER FAIL: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
