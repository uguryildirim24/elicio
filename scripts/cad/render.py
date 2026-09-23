#!/usr/bin/env python3.13
"""Headless renders and one-page drawing for the order-1 gauge (WP3).

Reads committed STL files and ``manifest.json``. Does not rebuild solids.
Does not open a GUI. PNG and PDF metadata dates are pinned so a second
run is byte-identical.

    .venv/bin/python scripts/cad/render.py --out docs/fab/cad/v1/

Writes ``render_medial.png``, ``render_lateral.png``, ``drawing.pdf`` and
updates the ``views`` map in the manifest. Solid hashes in ``files`` are
not rewritten. ``--debug-png DIR`` also writes the drawing page as a PNG
(not hashed, not committed) so it can be looked at without a PDF viewer.

Shading is a z-buffer rasteriser in numpy over the STL triangles, one
flat shade per triangle, with outline and crease lines found in the depth
and normal buffers. Every view is orthographic and head-on or edge-on, so
the 10 mm scale bar is true in the plane of the view. Large flat faces
shade as one tone whatever their triangulation, so tessellation seams do
not show. Images are embedded in the PDF as rasters; the section views,
tables and text stay vector.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import struct
import subprocess
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
# Versions the committed hashes were produced with; another matplotlib or
# numpy build can move PNG/PDF bytes (README, "Renders and drawing").
TESTED_WITH = "numpy 2.5.3, matplotlib 3.11.2, pypdf 6.19.0, trimesh 5.1.0"

# Nylon grey, thin body slightly cooler, lid warm so the seam reads.
COLOR_FULL = np.array([0.78, 0.79, 0.80])
COLOR_THIN = np.array([0.66, 0.74, 0.84])
COLOR_LID = np.array([0.88, 0.80, 0.62])
COLOR_TITANIUM = np.array([0.55, 0.56, 0.60])
COLOR_ENIG = np.array([0.82, 0.68, 0.34])
EDGE_SHADE = 0.18
CREASE_COS = math.cos(math.radians(28.0))
DEPTH_JUMP_MM = 0.6
RASTER_CHUNK = 3_000_000

# Body-frame view directions (toward the camera) and screen up.
MEDIAL = (np.array([0.0, -1.0, 0.0]), np.array([0.0, 0.0, 1.0]))
LATERAL = (np.array([0.0, 1.0, 0.0]), np.array([0.0, 0.0, 1.0]))
POSTERIOR = (np.array([1.0, 0.0, 0.0]), np.array([0.0, 0.0, 1.0]))


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
        out.extend(_png_chunk(tag, chunk))
        if tag == b"IHDR":
            for etag, edata in extra:
                out.extend(_png_chunk(etag, edata))
    return bytes(out)


def pin_pdf(data: bytes, title: str = "Elicio BTE fit gauge v1 drawing") -> bytes:
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import ArrayObject, ByteStringObject

    reader = PdfReader(io.BytesIO(data))
    writer = PdfWriter()
    writer.append(reader)
    writer.add_metadata(
        {
            "/Title": title,
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

    if not FONT_PATH.is_file():
        raise RenderError(f"font missing: {FONT_PATH}")
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
            "image.interpolation": "antialiased",
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


def titanium_heads(manifest: dict[str, Any]) -> list[tuple[np.ndarray, np.ndarray, np.ndarray]]:
    """Bought ISO 7380 heads at the three EMG sites and the two wall pads.

    Review r7: the shell STL carries holes, not printed domes (plan §4:
    only the gauge prints domes). The views draw the titanium heads as
    hardware so the medial face and the posterior wall read as worn.
    """
    cad = load_cad()
    params = manifest["parameters"]
    path = cad.make_path(float(params["BODY_ARC"]), float(params["CREASE_BOW"]))
    s5e = cad.load_s5e_shell()
    meshes = []
    for u, s in (s5e.p1, s5e.p2, s5e.p3):
        cap = cad._cap_solid(path, float(u), float(s))
        pts, tris = cap.tessellate(0.02, 0.2)
        verts = np.array([[p.X, p.Y, p.Z] for p in pts], dtype=np.float64)
        faces = np.array(tris, dtype=np.int64)
        meshes.append((verts, faces, COLOR_TITANIUM))
    width = float(params["BODY_WIDTH"])
    charge = next(c for c in manifest["checks"] if c["name"] == "V2_CHARGE_pads")["numbers"]
    for name, site in (("P4", s5e.p4), ("P5", s5e.p5)):
        u, s = site
        pad_y = float(charge[f"{name}_y"])
        head = cad._u_button_head(path, width, float(s), pad_y)
        ring = cad._u_cylinder(
            path, float(u), float(s), pad_y, cad.CHARGE_PAD_D / 2.0, 0.08, into_bay=True
        )
        for solid, color in ((head, COLOR_TITANIUM), (ring, COLOR_ENIG)):
            pts, tris = solid.tessellate(0.02, 0.2)
            verts = np.array([[p.X, p.Y, p.Z] for p in pts], dtype=np.float64)
            faces = np.array(tris, dtype=np.int64)
            meshes.append((verts, faces, color))
    return meshes


def rotate_x(vertices: np.ndarray, deg: float) -> np.ndarray:
    rad = np.radians(deg)
    cos_a, sin_a = np.cos(rad), np.sin(rad)
    out = np.array(vertices, copy=True, dtype=np.float64)
    y, z = out[..., 1].copy(), out[..., 2].copy()
    out[..., 1] = y * cos_a - z * sin_a
    out[..., 2] = y * sin_a + z * cos_a
    return out


def to_body_frame(vertices: np.ndarray, theta_deg: float) -> np.ndarray:
    """Undo assemble_shell's rotate(Axis.X, -THETA_DEG)."""
    return rotate_x(vertices, float(theta_deg))


def basis(view_forward: np.ndarray, up_hint: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    vf = np.asarray(view_forward, dtype=np.float64)
    vf = vf / np.linalg.norm(vf)
    up = np.asarray(up_hint, dtype=np.float64)
    right = np.cross(up, vf)
    right = right / np.linalg.norm(right)
    up = np.cross(vf, right)
    up = up / np.linalg.norm(up)
    return right, up, vf


class View:
    """Orthographic view: screen x along ``right``, screen y along ``up``, mm."""

    def __init__(self, direction: tuple[np.ndarray, np.ndarray]) -> None:
        self.right, self.up, self.vf = basis(*direction)
        light = 0.75 * self.vf + 0.45 * self.up - 0.35 * self.right
        self.light = light / np.linalg.norm(light)

    def project(self, points: np.ndarray) -> np.ndarray:
        pts = np.asarray(points, dtype=np.float64)
        return np.stack((pts @ self.right, pts @ self.up), axis=-1)

    def bounds(self, meshes: list[tuple[np.ndarray, np.ndarray, np.ndarray]]) -> tuple[float, float, float, float]:
        pts = np.concatenate([self.project(v) for v, _f, _c in meshes])
        return (
            float(pts[:, 0].min()),
            float(pts[:, 0].max()),
            float(pts[:, 1].min()),
            float(pts[:, 1].max()),
        )


def rasterize(
    view: View,
    meshes: list[tuple[np.ndarray, np.ndarray, np.ndarray]],
    *,
    extent: tuple[float, float, float, float],
    px_per_mm: float,
    supersample: int = 2,
) -> np.ndarray:
    """Return an RGB float image of ``meshes`` seen through ``view``.

    ``extent`` is (x0, x1, y0, y1) in view millimetres. One z-buffer for
    all meshes, so occlusion between parts is correct.
    """
    x0, x1, y0, y1 = extent
    scale = px_per_mm * supersample
    width = int(math.ceil((x1 - x0) * scale))
    height = int(math.ceil((y1 - y0) * scale))
    zbuf = np.full(width * height, -np.inf)
    tbuf = np.full(width * height, -1, dtype=np.int64)
    tri_normal: list[np.ndarray] = []
    tri_color: list[np.ndarray] = []
    tri_mesh: list[np.ndarray] = []
    offset = 0
    for mesh_id, (vertices, faces, color) in enumerate(meshes):
        tri = vertices[faces]
        normal = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
        length = np.linalg.norm(normal, axis=1)
        keep = length > 1e-12
        tri, normal, length = tri[keep], normal[keep], length[keep]
        normal = normal / length[:, None]
        keep = normal @ view.vf > 1e-9
        tri, normal = tri[keep], normal[keep]
        sx = (tri @ view.right - x0) * scale
        sy = (y1 - tri @ view.up) * scale
        depth = tri @ view.vf
        _raster_triangles(sx, sy, depth, offset, width, height, zbuf, tbuf)
        tri_normal.append(normal)
        tri_color.append(np.broadcast_to(color, normal.shape))
        tri_mesh.append(np.full(len(normal), mesh_id, dtype=np.int64))
        offset += len(normal)
    normals = np.concatenate(tri_normal)
    colors = np.concatenate(tri_color)
    mesh_of = np.concatenate(tri_mesh)
    hit = tbuf >= 0
    idx = np.where(hit, tbuf, 0)
    shade = 0.36 + 0.64 * np.clip(normals[idx] @ view.light, 0.0, 1.0)
    rgb = np.where(hit[:, None], colors[idx] * shade[:, None], 1.0)
    # Outline and crease lines from neighbouring pixels.
    tb = tbuf.reshape(height, width)
    zb = np.where(hit, zbuf, 0.0).reshape(height, width)
    nb = np.where(hit[:, None], normals[idx], 0.0).reshape(height, width, 3)
    mb = np.where(hit, mesh_of[idx], -1).reshape(height, width)
    edge = np.zeros((height, width), dtype=bool)
    for axis in (0, 1):
        a = (slice(None, -1), slice(None)) if axis == 0 else (slice(None), slice(None, -1))
        b = (slice(1, None), slice(None)) if axis == 0 else (slice(None), slice(1, None))
        ha, hb = tb[a] >= 0, tb[b] >= 0
        both = ha & hb
        crease = both & ((nb[a] * nb[b]).sum(axis=-1) < CREASE_COS)
        jump = both & (np.abs(zb[a] - zb[b]) > DEPTH_JUMP_MM)
        part = both & (mb[a] != mb[b])
        line = crease | jump | part | (ha != hb)
        edge[a] |= line
        edge[b] |= line & (ha != hb)
    img = rgb.reshape(height, width, 3)
    img[edge] = EDGE_SHADE
    if supersample > 1:
        h2, w2 = height // supersample, width // supersample
        img = img[: h2 * supersample, : w2 * supersample]
        img = img.reshape(h2, supersample, w2, supersample, 3).mean(axis=(1, 3))
    return np.clip(img, 0.0, 1.0)


def _raster_triangles(
    sx: np.ndarray,
    sy: np.ndarray,
    depth: np.ndarray,
    offset: int,
    width: int,
    height: int,
    zbuf: np.ndarray,
    tbuf: np.ndarray,
) -> None:
    area = (sx[:, 1] - sx[:, 0]) * (sy[:, 2] - sy[:, 0]) - (sx[:, 2] - sx[:, 0]) * (sy[:, 1] - sy[:, 0])
    ix0 = np.clip(np.ceil(sx.min(axis=1) - 0.5), 0, width).astype(np.int64)
    ix1 = np.clip(np.floor(sx.max(axis=1) - 0.5), -1, width - 1).astype(np.int64)
    iy0 = np.clip(np.ceil(sy.min(axis=1) - 0.5), 0, height).astype(np.int64)
    iy1 = np.clip(np.floor(sy.max(axis=1) - 0.5), -1, height - 1).astype(np.int64)
    bw = np.maximum(ix1 - ix0 + 1, 0)
    bh = np.maximum(iy1 - iy0 + 1, 0)
    counts = np.where(np.abs(area) > 1e-12, bw * bh, 0)
    ends = np.cumsum(counts)
    start = 0
    n = len(counts)
    while start < n:
        base = ends[start - 1] if start else 0
        stop = int(np.searchsorted(ends, base + RASTER_CHUNK, side="right"))
        stop = max(stop, start + 1)
        sel = np.arange(start, stop)
        cnt = counts[sel]
        total = int(cnt.sum())
        start = stop
        if total == 0:
            continue
        rep = np.repeat(sel, cnt)
        first = np.cumsum(cnt) - cnt
        k = np.arange(total, dtype=np.int64) - np.repeat(first, cnt)
        w = bw[rep]
        px = ix0[rep] + k % w
        py = iy0[rep] + k // w
        cx = px + 0.5
        cy = py + 0.5
        X, Y, A = sx[rep], sy[rep], area[rep]
        w0 = ((X[:, 1] - cx) * (Y[:, 2] - cy) - (X[:, 2] - cx) * (Y[:, 1] - cy)) / A
        w1 = ((X[:, 2] - cx) * (Y[:, 0] - cy) - (X[:, 0] - cx) * (Y[:, 2] - cy)) / A
        w2 = 1.0 - w0 - w1
        inside = (w0 >= -1e-9) & (w1 >= -1e-9) & (w2 >= -1e-9)
        if not inside.any():
            continue
        D = depth[rep]
        d = (w0 * D[:, 0] + w1 * D[:, 1] + w2 * D[:, 2])[inside]
        pid = (py * width + px)[inside]
        tid = rep[inside] + offset
        order = np.lexsort((-d, pid))
        pid, d, tid = pid[order], d[order], tid[order]
        head = np.ones(len(pid), dtype=bool)
        head[1:] = pid[1:] != pid[:-1]
        pid, d, tid = pid[head], d[head], tid[head]
        better = d > zbuf[pid]
        zbuf[pid[better]] = d[better]
        tbuf[pid[better]] = tid[better]


def place_image(ax, img: np.ndarray, extent: tuple[float, float, float, float], ppm: float, dx: float = 0.0) -> None:
    """Draw ``img`` with its top-left corner at (x0 + dx, y1), one pixel = 1/ppm mm."""
    x0, _x1, _y0, y1 = extent
    h, w = img.shape[:2]
    ax.imshow(
        img,
        extent=(x0 + dx, x0 + dx + w / ppm, y1 - h / ppm, y1),
        origin="upper",
        interpolation="antialiased",
        zorder=1,
    )


def scale_bar(ax, x: float, y: float, length: float = 10.0, size: float = 8.0) -> None:
    ax.plot([x, x + length], [y, y], color="black", lw=1.4, solid_capstyle="butt", zorder=5)
    for xx in (x, x + length):
        ax.plot([xx, xx], [y - 0.6, y + 0.6], color="black", lw=1.1, zorder=5)
    ax.text(x + length / 2.0, y - 1.0, f"{length:.0f} mm", ha="center", va="top", fontsize=size, zorder=5)


def git_commit_date(commit: str) -> str:
    """Committer date (YYYY-MM-DD) of the solids commit; fixed for a given commit."""
    try:
        return subprocess.check_output(
            ["git", "show", "-s", "--format=%cs", commit],
            cwd=REPO_ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip() or "unknown"
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def stamp_label(commit: str, date: str) -> str:
    """Corner stamp. A dirty tree hash keeps the word 'dirty' after the short id."""
    if commit.endswith(" dirty"):
        raw = commit[: -len(" dirty")]
        short = raw[:12] if len(raw) >= 12 else raw
        return f"solids commit {short} dirty  {date}"
    short = commit[:12] if commit not in ("", "unknown") else commit or "unknown"
    return f"solids commit {short}  {date}"


def stamp(ax, commit: str, date: str) -> None:
    ax.text(
        0.995,
        0.005,
        stamp_label(commit, date),
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=7,
        family="monospace",
    )


def _out_dir_dirty(out_dir: Path) -> bool:
    """True when hashed solids (STEP/STL/3MF) under out_dir differ from HEAD."""
    try:
        rel = out_dir.resolve().relative_to(REPO_ROOT.resolve())
    except ValueError:
        return True
    try:
        text = subprocess.check_output(
            ["git", "status", "--porcelain", "--", str(rel)],
            cwd=REPO_ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return True
    for line in text.splitlines():
        name = line[3:].strip().rsplit(" -> ", 1)[-1]
        if name.lower().endswith((".step", ".stl", ".3mf")):
            return True
    return False


def _git_head_tree() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD^{tree}"],
            cwd=REPO_ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def solids_stamp_commit(manifest: dict[str, Any], out_dir: Path) -> str:
    """Commit id drawn on the views: the manifest commit, or tree hash + ' dirty'."""
    if _out_dir_dirty(out_dir):
        tree = _git_head_tree()
        return f"{tree} dirty"
    return str(manifest.get("commit") or "unknown")


def save_png(fig) -> bytes:
    import matplotlib.pyplot as plt

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=DPI, facecolor="white", edgecolor="none")
    plt.close(fig)
    return pin_png(buf.getvalue())


def save_pdf(fig, title: str = "Elicio BTE fit gauge v1 drawing") -> bytes:
    import matplotlib.pyplot as plt

    buf = io.BytesIO()
    fig.savefig(buf, format="pdf", facecolor="white", edgecolor="none")
    plt.close(fig)
    return pin_pdf(buf.getvalue(), title=title)


def write_bytes(path: Path, data: bytes) -> dict[str, Any]:
    path.write_bytes(data)
    return {"sha256": sha256_bytes(data), "bytes": len(data)}


def _view_block(view: View, meshes, pad: float = 1.0) -> tuple[float, float, float, float]:
    xa, xb, ya, yb = view.bounds(meshes)
    return (xa - pad, xb + pad, ya - pad, yb + pad)


def render_medial(out_dir: Path, *, manifest: dict[str, Any], commit: str, date: str) -> dict[str, Any]:
    """Medial faces of full p15 and thin p15, each with an edge-on posterior view."""
    import matplotlib.pyplot as plt

    theta = float(manifest["parameters"]["THETA_DEG"])
    span = manifest["span"]
    if manifest.get("stage") == "shell":
        bodies = (("body_full_p15", COLOR_FULL, "shell body"),)
    else:
        bodies = (
            ("body_full_p15", COLOR_FULL, "full p15"),
            ("body_thin_p15", COLOR_THIN, "thin p15"),
        )
    medial, posterior = View(MEDIAL), View(POSTERIOR)
    ppm = 13.0
    fig, ax = plt.subplots(figsize=(11.0, 6.6), dpi=DPI, facecolor="white")
    cursor = 0.0
    top = bottom = 0.0
    labels: list[tuple[float, str]] = []
    medial_place: tuple[View, float] | None = None
    posterior_place: tuple[View, float] | None = None
    for name, color, label in bodies:
        verts, faces = load_stl(out_dir / f"{name}.stl")
        verts = to_body_frame(verts, theta)
        meshes = [(verts, faces, color)]
        if manifest.get("stage") == "shell":
            meshes += titanium_heads(manifest)
        thick = float(span[name]["BODY_THICK"])
        labels.append(
            (cursor, f"{label}:  BODY_THICK {thick:.1f} mm,  SPAN {float(span[name]['span']):.2f} (thickness + crown 1.35)")
        )
        for view, caption in ((medial, "medial face"), (posterior, "edge-on, from posterior")):
            ext = _view_block(view, meshes)
            img = rasterize(view, meshes, extent=ext, px_per_mm=ppm)
            dx = cursor - ext[0]
            if view is medial and medial_place is None:
                medial_place = (view, dx)
            if view is posterior:
                posterior_place = (view, dx)
            place_image(ax, img, ext, ppm, dx)
            top = max(top, ext[3])
            bottom = min(bottom, ext[2])
            if view is posterior:
                # BODY_THICK dimension across the body at mid-length (y 0 → thick).
                ymid = 0.5 * (ext[2] + ext[3]) - 8.0
                ax.annotate(
                    "",
                    xy=(dx + 0.0, ymid),
                    xytext=(dx + thick, ymid),
                    arrowprops={"arrowstyle": "<->", "lw": 0.9, "color": "#b00000", "shrinkA": 0, "shrinkB": 0},
                    zorder=6,
                )
                ax.text(dx + thick / 2.0, ymid - 1.2, f"{thick:.1f}", ha="center", va="top", fontsize=9, color="#b00000", zorder=6)
                ax.text(dx + ext[0], ext[2] - 1.0, "medial ← → lateral", fontsize=6.5, va="top", zorder=6)
            ax.text(cursor, ext[3] + 1.2, caption, fontsize=7.5, va="bottom", zorder=6)
            cursor += (ext[1] - ext[0]) + (4.0 if view is medial else 14.0)
    for x, text in labels:
        ax.text(x, top + 6.0, text, fontsize=9.5, va="bottom", zorder=6)
    if manifest.get("stage") == "shell" and medial_place is not None:
        cad = load_cad()
        path = cad.make_path(
            float(manifest["parameters"]["BODY_ARC"]),
            float(manifest["parameters"]["CREASE_BOW"]),
        )
        view, dx = medial_place
        well_xyz = np.array(
            cad.p_xyz(path, cad.SHELL_SCREW_U, cad.SHELL_SCREW_S, -0.2)
        )
        well_xyz = to_body_frame(well_xyz.reshape(1, 3), theta)[0]
        p = view.project(well_xyz)
        ax.annotate(
            "concealed M2.5 well on the medial tail (Q71).\n"
            "Skin hides the head. Lateral lid is unbroken.\n"
            "M2.5×8 into a lid boss in the tail pocket (Q89).",
            xy=(p[0] + dx, p[1]),
            xytext=(p[0] + dx + 18.0, p[1] + 10.0),
            fontsize=8,
            arrowprops={"arrowstyle": "->", "lw": 0.7},
            zorder=8,
        )
        if posterior_place is not None:
            view_p, dx_p = posterior_place
            s5e = cad.load_s5e_shell()
            width = float(manifest["parameters"]["BODY_WIDTH"])
            for label, site, pad_y, dxy in (
                ("P4 CHARGE_VBUS, posterior wall (Q90)", s5e.p4, s5e.p4_y, (8.0, 10.0)),
                ("P5 CHARGE_GND, posterior wall (Q90)", s5e.p5, s5e.p5_y, (8.0, -8.0)),
            ):
                xyz = np.array(cad.p_xyz(path, width + 0.4, site[1], pad_y))
                xyz = to_body_frame(xyz.reshape(1, 3), theta)[0]
                q = view_p.project(xyz)
                ax.annotate(
                    label,
                    xy=(q[0] + dx_p, q[1]),
                    xytext=(q[0] + dx_p + dxy[0], q[1] + dxy[1]),
                    fontsize=8,
                    arrowprops={"arrowstyle": "->", "lw": 0.7},
                    zorder=8,
                )
    ax.set_xlim(-2.0, cursor - 8.0)
    ax.set_ylim(bottom - 9.0, top + (16.0 if manifest.get("stage") == "shell" else 13.0))
    ax.set_aspect("equal")
    ax.set_axis_off()
    scale_bar(ax, 0.0, bottom - 3.5)
    caption = (
        "Medial (skin side): three titanium ISO 7380 EMG heads (bought, drawn dark; the print has Ø2.7 holes),\n"
        "concealed M2.5 well on the tail. No charging pads on the skin (Q90). Posterior edge-on: P4/P5 clamped\n"
        "button-heads through the far side wall. Same scale throughout. "
        "Faint facet shading on curved edges is the STL mesh (0.02 mm chord), not geometry."
        if manifest.get("stage") == "shell"
        else
        "Medial (skin side): three mock contact caps, tail, hook. Same scale throughout; "
        "edge-on views show the 9.0 vs 7.0 thickness.\nFaint facet shading on curved edges is the STL mesh "
        "(0.02 mm chord), not geometry."
    )
    ax.text(
        0.0,
        1.0,
        caption,
        transform=ax.transAxes,
        fontsize=8.5,
        va="top",
    )
    stamp(ax, commit, date)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.97, bottom=0.03)
    return write_bytes(out_dir / "render_medial.png", save_png(fig))


def lid_outside_body(view: View, body: tuple, lid: tuple, extent, ppm: float) -> np.ndarray:
    """Mask of pixels where the lid shows outside the body's silhouette."""
    body_img = rasterize(view, [(body[0], body[1], np.ones(3))], extent=extent, px_per_mm=ppm, supersample=1)
    lid_img = rasterize(view, [(lid[0], lid[1], np.ones(3))], extent=extent, px_per_mm=ppm, supersample=1)
    return (lid_img.min(axis=2) < 0.999) & ~(body_img.min(axis=2) < 0.999)


def render_lateral(out_dir: Path, *, manifest: dict[str, Any], commit: str, date: str) -> dict[str, Any]:
    import matplotlib.pyplot as plt

    params = manifest["parameters"]
    theta = float(params["THETA_DEG"])
    body_v, body_f = load_stl(out_dir / "body_full_p15.stl")
    lid_v, lid_f = load_stl(out_dir / "lid.stl")
    body_v = to_body_frame(body_v, theta)
    lid_v = to_body_frame(lid_v, theta)
    lateral = View(LATERAL)
    meshes = [(body_v, body_f, COLOR_FULL), (lid_v, lid_f, COLOR_LID)]
    ext = _view_block(lateral, meshes)
    ppm = 13.0
    img = rasterize(lateral, meshes, extent=ext, px_per_mm=ppm)
    fig, ax = plt.subplots(figsize=(11.0, 6.6), dpi=DPI, facecolor="white")
    place_image(ax, img, ext, ppm)
    cad = load_cad()
    path = cad.make_path(float(params["BODY_ARC"]), float(params["CREASE_BOW"]))
    lid_y = float(params["LID_Y"])

    def at(u: float, s: float, y: float) -> np.ndarray:
        return lateral.project(np.array(cad.p_xyz(path, u, s, y)))

    if manifest.get("stage") == "shell":
        usb = at(10.0, 0.2, 2.8)
        ax.annotate(
            "No USB opening (Q81: no receptacle at M1 52).\n"
            "V2_USB_end is NOT_APPLICABLE.",
            xy=usb,
            xytext=(usb[0] + 28.0, usb[1] - 14.0),
            fontsize=8,
            arrowprops={"arrowstyle": "->", "lw": 0.7},
            zorder=6,
        )
        hinge = at(10.0, 3.5, 8.4)
        ax.annotate(
            "hinge lip in the hook-end wall (Q71).\n"
            "0.30 mm of body nylon over the lip.",
            xy=hinge,
            xytext=(hinge[0] + 28.0, hinge[1] + 12.0),
            fontsize=8,
            arrowprops={"arrowstyle": "->", "lw": 0.7},
            zorder=6,
        )
        tail = at(14.5, 41.0, lid_y + 1.2)
        ax.annotate(
            "lid screw well is on the medial tail (Q71),\n"
            "not on this lateral face.",
            xy=tail,
            xytext=(tail[0] + 16.0, tail[1] - 4.0),
            fontsize=8,
            arrowprops={"arrowstyle": "->", "lw": 0.7},
            zorder=6,
        )
    else:
        lip = at(sum(cad.LIP_U) / 2.0, sum(cad.LIP_S) / 2.0, lid_y + 1.0)
        ax.annotate(
            "lid lip (E5) and plate edge stand past the body's top end by\n"
            "design: the lip hooks over the top face and its bump snaps\n"
            "into the groove (plan §3.3 LID_LIP, §3.5 step 7). The only lid\n"
            "area outside the body outline in this view: about 9 mm²",
            xy=lip,
            xytext=(lip[0] + 30.0, lip[1] - 12.0),
            fontsize=8,
            arrowprops={"arrowstyle": "->", "lw": 0.7},
            zorder=6,
        )
        tail = at(8.5, cad.TONGUE_SLOT_S[1] - 0.8, lid_y + 1.0)
        ax.annotate(
            "tail lip, full thickness; the lid tongue (E1)\nis hidden in the slot under it",
            xy=tail,
            xytext=(tail[0] + 14.0, tail[1] - 2.0),
            fontsize=8,
            arrowprops={"arrowstyle": "->", "lw": 0.7},
            zorder=6,
        )
    hook_c = rotate_x(
        np.array([float(params["HOOK_ROOT_X"]) - float(params["HOOK_RADIUS"]), float(params["HOOK_ROOT_Y"]), 0.0]),
        theta,
    )
    hc = lateral.project(hook_c)
    hook_mid = lateral.project(rotate_x(np.array([float(params["HOOK_ROOT_X"]) - float(params["HOOK_RADIUS"]), float(params["HOOK_ROOT_Y"]), float(params["HOOK_RADIUS"])]), theta))
    ax.annotate(
        "hook, circular root then elliptical section, glasses flat on its lateral-superior side"
        if manifest.get("stage") == "shell"
        else "hook, glasses flat on its lateral-superior side",
        xy=hook_mid,
        xytext=(hook_mid[0] + 8.0, hook_mid[1] + 3.0),
        fontsize=8,
        arrowprops={"arrowstyle": "->", "lw": 0.7},
        zorder=6,
    )
    del hc
    ax.set_xlim(ext[0] - 2.0, ext[1] + 62.0)
    ax.set_ylim(ext[2] - 8.0, ext[3] + 4.0)
    ax.set_aspect("equal")
    ax.set_axis_off()
    scale_bar(ax, ext[0], ext[2] - 3.0)
    ax.text(
        0.0,
        1.0,
        "Lateral (outer side): shell v2, lid seated, circular-root hook"
        if manifest.get("stage") == "shell"
        else "Lateral (outer side): full p15, lid seated, hook",
        transform=ax.transAxes,
        fontsize=9.5,
        va="top",
    )
    stamp(ax, commit, date)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.97, bottom=0.03)
    return write_bytes(out_dir / "render_lateral.png", save_png(fig))


def _rect(ax, s0, s1, y0, y1, *, fc, ec="black", lw=0.5, hatch=None, z=2):
    from matplotlib.patches import Rectangle

    ax.add_patch(Rectangle((s0, y0), s1 - s0, y1 - y0, facecolor=fc, edgecolor=ec, linewidth=lw, hatch=hatch, zorder=z))


BODY_FC, BODY_EC = "#d4d4d4", "#555555"
LID_FC, LID_EC = "#ead9ad", "#6a5520"
AIR_FC = "#ffffff"


def _section_axes(ax, xlim, ylim, title: str, xlabel: str) -> None:
    ax.set_aspect("equal")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xlabel(xlabel, fontsize=6.5, labelpad=1)
    ax.set_ylabel("y (mm)", fontsize=6.5, labelpad=1)
    ax.set_title(title, fontsize=7.5, pad=3)
    ax.tick_params(labelsize=5.5, length=2, pad=1)


def _callout(ax, xy, xytext, text) -> None:
    ax.annotate(
        text,
        xy=xy,
        xytext=xytext,
        fontsize=5.8,
        arrowprops={"arrowstyle": "-", "lw": 0.4, "color": "#222222"},
        zorder=8,
    )


def section_lip(ax, cad, lid_y: float) -> None:
    """(s, y) at u 11 (inside LIP_U and GROOVE_U): lip, bump, groove, E5."""
    lip_y0 = lid_y + 1.0 - cad.LIP_LENGTH
    _rect(ax, 0.0, 3.2, 0.0, lid_y, fc=BODY_FC, ec=BODY_EC, z=1)
    _rect(ax, cad.CAVITY_S[0], 3.2, 1.5, lid_y, fc=AIR_FC, ec=BODY_EC, z=2)
    _rect(ax, cad.GROOVE_S[0], cad.GROOVE_S[1], lid_y + cad.GROOVE_Y_OFF[0], lid_y + cad.GROOVE_Y_OFF[1], fc=AIR_FC, ec=BODY_EC, z=2)
    _rect(ax, cad.LID_PLATE_S[0], 3.2, lid_y, lid_y + 1.0, fc=LID_FC, ec=LID_EC, z=3)
    _rect(ax, cad.LIP_S[0], cad.LIP_S[1], lip_y0, lid_y + 1.0, fc=LID_FC, ec=LID_EC, z=3)
    _rect(ax, cad.LIP_S[1], cad.LIP_S[1] + cad.BUMP_OUT, lip_y0, lip_y0 + cad.BUMP_TALL, fc="#c9a24a", ec=LID_EC, z=4)
    _section_axes(ax, (-4.2, 3.2), (2.4, 10.0), "lip, bump, groove (E5)  at u 11", "s (mm)")
    _callout(ax, (-0.7, 6.0), (-4.0, 7.2), "lip 1.0\nE5 min 1.0")
    _callout(ax, (0.05, lip_y0 + 0.3), (-4.0, 3.0), "bump 0.5 × 0.6\nE5 min 0.2")
    _callout(ax, (0.4, lid_y + cad.GROOVE_Y_OFF[1] - 0.1), (1.0, 5.2), "groove\n0.5 × 1.0")
    _callout(ax, (1.0, lid_y + 0.5), (0.4, 9.3), "plate, lid top y 9.0")


def section_nubs(ax, cad, lid_y: float, clear_fit: float) -> None:
    """(u, y) at s 17.9 (through the nubs and the rib): nub to side wall, E3."""
    _rect(ax, 0.0, 4.2, 0.0, 1.5, fc=BODY_FC, ec=BODY_EC, z=1)
    _rect(ax, 0.0, cad.CAVITY_U[0], 0.0, lid_y, fc=BODY_FC, ec=BODY_EC, z=1)
    _rect(ax, cad.CAVITY_U[0], 4.2, cad.RIB_Y[0], cad.RIB_Y[1], fc=BODY_FC, ec=BODY_EC, hatch="////", z=1)
    _rect(ax, clear_fit, 4.2, lid_y, lid_y + 1.0, fc=LID_FC, ec=LID_EC, z=3)
    nub_u = cad.NUB_U[0]
    _rect(ax, nub_u[0], nub_u[1], lid_y - cad.NUB, lid_y, fc=LID_FC, ec=LID_EC, z=3)
    _section_axes(ax, (-0.6, 4.2), (3.2, 9.6), "nub (E3)  at s 17.9", "u (mm)")
    ax.annotate(
        "",
        xy=(cad.CAVITY_U[0], lid_y - 0.4),
        xytext=(nub_u[0], lid_y - 0.4),
        arrowprops={"arrowstyle": "<->", "lw": 0.5, "shrinkA": 0, "shrinkB": 0},
        zorder=8,
    )
    _callout(ax, (1.7, lid_y - 0.4), (0.2, 5.6), f"nub : side wall\n{nub_u[0] - cad.CAVITY_U[0]:.1f}")
    _callout(ax, (2.3, lid_y - 0.6), (2.6, 5.9), "nub 0.8\nE3 min 0.6")
    _callout(ax, (3.5, 4.2), (2.6, 5.0), "rib (E2),\n0.8 in s")


def section_tail(ax, cad, lid_y: float, thick: float) -> None:
    """(s, y) at u 8.5 (tail centre): web, pocket, tongue, slot, E1."""
    s0 = 44.2
    _rect(ax, s0, cad.LID_RECESS_S1, 0.0, lid_y, fc=BODY_FC, ec=BODY_EC, z=1)
    _rect(ax, cad.LID_RECESS_S1, cad.TONGUE_SLOT_S[1], 0.0, thick, fc=BODY_FC, ec=BODY_EC, z=1)
    _rect(ax, cad.WEB_POCKET_S[0], cad.WEB_POCKET_S[1], lid_y + cad.WEB_POCKET_Y_OFF[0], lid_y, fc=AIR_FC, ec=BODY_EC, z=2)
    _rect(ax, cad.TONGUE_SLOT_S[0], cad.TONGUE_SLOT_S[1] + 0.05, lid_y + cad.TONGUE_SLOT_Y_OFF[0], lid_y + cad.TONGUE_SLOT_Y_OFF[1], fc=AIR_FC, ec=BODY_EC, z=2)
    _rect(ax, s0, cad.LID_PLATE_S[1], lid_y, lid_y + 1.0, fc=LID_FC, ec=LID_EC, z=3)
    _rect(ax, cad.LID_WEB_S[0], cad.LID_WEB_S[1], lid_y - 0.8, lid_y, fc=LID_FC, ec=LID_EC, z=3)
    _rect(ax, cad.LID_TONGUE_S[0], cad.LID_TONGUE_S[1], lid_y - 0.8, lid_y - 0.3, fc=LID_FC, ec=LID_EC, z=3)
    _section_axes(ax, (s0, 49.4), (5.0, 10.2), "web, tongue, slot (E1)  at u 8.5", "s (mm)")
    _callout(ax, (46.0, lid_y - 0.6), (44.4, 5.4), "web 0.8 in pocket 1.4")
    _callout(ax, (47.6, lid_y - 0.55), (47.2, 5.9), "tongue 0.5\nE1 min 0.4")
    _callout(ax, (48.2, lid_y - 0.15), (48.0, 9.6), "slot 0.9,\nlip 1.1 above")


def load_cad():
    import importlib.util

    script = SCRIPT_DIR / "bte_fit_shell.py"
    if "bte_fit_shell" in sys.modules:
        return sys.modules["bte_fit_shell"]
    spec = importlib.util.spec_from_file_location("bte_fit_shell", script)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules["bte_fit_shell"] = module
    spec.loader.exec_module(module)
    return module


def parameter_set_name(manifest: dict[str, Any]) -> str:
    used = set(manifest["defaults_used"])
    measured = [f"M{i}" for i in range(1, 9) if f"M{i}" not in used]
    if not measured:
        return "default.toml (REF: M1–M8 all defaults)"
    return "overlay, measured " + ", ".join(measured)


def fillet_summary(manifest: dict[str, Any]) -> list[str]:
    rows = []
    names = ("body_full_p15",) if manifest.get("stage") == "shell" else ("body_full_p15", "body_thin_p15", "body_full_p25")
    for name in names:
        notes = manifest["notes"].get(name, {})
        hook = next((f for f in notes.get("fillets", []) if "hook joint" in f), "hook joint: not recorded")
        lip = next((f for f in notes.get("fillets", []) if "lip root" in f), "lip root: not recorded")
        rows.append(f"{name}: {hook.replace('§3.5 step 9 ', '')}; {lip}")
    return rows


def draw_page(out_dir: Path, *, cad, manifest: dict[str, Any], commit: str, date: str, debug_png: Path | None = None) -> dict[str, Any]:
    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec

    params = manifest["parameters"]
    theta = float(params["THETA_DEG"])
    lid_y = float(params["LID_Y"])
    thick = float(params["BODY_THICK"])
    body_v, body_f = load_stl(out_dir / "body_full_p15.stl")
    lid_v, lid_f = load_stl(out_dir / "lid.stl")
    body_v = to_body_frame(body_v, theta)
    lid_v = to_body_frame(lid_v, theta)
    path = cad.make_path(float(params["BODY_ARC"]), float(params["CREASE_BOW"]))

    fig = plt.figure(figsize=(8.27, 11.69), dpi=100, facecolor="white")
    fig.suptitle(
        "Elicio shell v2 — wearable body (round 5 winner) and lid"
        if manifest.get("stage") == "shell"
        else "Elicio BTE fit gauge v1 — reference body (full p15) and lid",
        fontsize=12,
        y=0.985,
    )
    gs = GridSpec(
        4, 6, figure=fig, height_ratios=[1.85, 0.95, 1.05, 0.95],
        hspace=0.28, wspace=0.45, left=0.05, right=0.98, top=0.955, bottom=0.02,
    )
    ax_views = fig.add_subplot(gs[0, :])
    ax_lip = fig.add_subplot(gs[1, 0:2])
    ax_nub = fig.add_subplot(gs[1, 2:4])
    ax_tail = fig.add_subplot(gs[1, 4:6])
    ax_m = fig.add_subplot(gs[2, 0:3])
    ax_e = fig.add_subplot(gs[2, 3:6])
    ax_block = fig.add_subplot(gs[3, :])

    ppm = 11.0
    body_mesh = (body_v, body_f, COLOR_FULL)
    lid_mesh = (lid_v, lid_f, COLOR_LID)
    lateral, medial, posterior = View(LATERAL), View(MEDIAL), View(POSTERIOR)
    cursor = 0.0
    placed: dict[str, tuple[View, float]] = {}
    top = bottom = 0.0
    hardware = titanium_heads(manifest) if manifest.get("stage") == "shell" else []
    for key, view, meshes, caption in (
        ("lateral", lateral, [body_mesh, lid_mesh], "lateral (lid side)"),
        ("medial", medial, [body_mesh, lid_mesh, *hardware], "medial (skin side)"),
        ("posterior", posterior, [body_mesh, lid_mesh, *hardware], "edge-on from posterior"),
    ):
        ext = _view_block(view, meshes)
        img = rasterize(view, meshes, extent=ext, px_per_mm=ppm)
        dx = cursor - ext[0]
        place_image(ax_views, img, ext, ppm, dx)
        placed[key] = (view, dx)
        ax_views.text(cursor, ext[3] + 1.5, caption, fontsize=8, va="bottom")
        top, bottom = max(top, ext[3]), min(bottom, ext[2])
        cursor += (ext[1] - ext[0]) + (30.0 if key != "posterior" else 0.0)

    def pt(key: str, xyz) -> np.ndarray:
        view, dx = placed[key]
        p = view.project(np.asarray(xyz, dtype=np.float64))
        return np.array([p[0] + dx, p[1]])

    def note(key, xyz, dxy, text, color="black"):
        p = pt(key, xyz)
        ax_views.annotate(
            text, xy=p, xytext=(p[0] + dxy[0], p[1] + dxy[1]), fontsize=6.2, color=color,
            arrowprops={"arrowstyle": "->", "lw": 0.5, "color": color}, zorder=8,
        )

    red = "#a00000"
    # M1 / TOTAL_CHORD: the chord from O to the path end, lateral view.
    o = pt("lateral", (0.0, lid_y + 1.0, 0.0))
    end = pt("lateral", cad.p_xyz(path, 0.0, float(params["BODY_ARC"]), lid_y + 1.0))
    ax_views.plot([o[0], end[0]], [o[1], end[1]], color=red, lw=0.8, ls="--", zorder=7)
    gate = manifest["chord_gate"]
    ax_views.text(
        max(o[0], end[0]) + 1.5, 0.5 * (o[1] + end[1]) + 6.0,
        f"M1 {params['M1']:.1f} vs chord O→tail\nTOTAL_CHORD {gate['total_chord']:.2f}\ngate M1 ≥ {gate['gate']:.2f}",
        fontsize=6.2, color=red, ha="left", va="center", zorder=8,
    )
    # M2: path arc, CREASE_BOW.
    arc_mid = cad.p_xyz(path, 0.0, float(params["BODY_ARC"]) / 2.0, lid_y + 1.0)
    note("lateral", arc_mid, (5.0, -14.0), f"M2 {params['M2']:.1f} → CREASE_BOW {params['CREASE_BOW']:.2f}\nBODY_ARC {params['BODY_ARC']:.1f}\nalong the path", red)
    # M8 and M5 on the hook, lateral view.
    hr = float(params["HOOK_RADIUS"])
    hcx = float(params["HOOK_ROOT_X"]) - hr
    hook_c = rotate_x(np.array([hcx, float(params["HOOK_ROOT_Y"]), 0.0]), theta)
    hook_top = rotate_x(np.array([hcx, float(params["HOOK_ROOT_Y"]), hr]), theta)
    pc, ptop = pt("lateral", hook_c), pt("lateral", hook_top)
    ax_views.annotate("", xy=ptop, xytext=pc, arrowprops={"arrowstyle": "->", "lw": 0.7, "color": red}, zorder=8)
    ax_views.text(pc[0] + 0.8, pc[1] + 1.0, f"M8 {params['M8']:.1f} → HOOK_RADIUS {hr:.2f}\n(= M8 + HOOK_DIA/2 + 0.75)", fontsize=6.2, color=red, zorder=8)
    a75 = math.radians(75.0)
    hook_75 = rotate_x(np.array([hcx + hr * math.cos(a75), float(params["HOOK_ROOT_Y"]), hr * math.sin(a75)]), theta)
    flat = "GLASSES_FLAT 0.8 over 30°–120°" if float(params["M5"]) > 0 else "no glasses flat (M5 = 0)"
    note("lateral", hook_75, (-14.0, 9.0), f"M5 {params['M5']:.1f} → {flat}", red)
    # M6, M7 at the contacts, medial view.
    c1 = cad.p_xyz(path, cad.CONTACT_1[0], cad.CONTACT_1[1], -cad.CONTACT_DOME_CROWN)
    c2 = cad.p_xyz(path, float(params["CONTACT_2_U"]), float(params["CONTACT_2_S"]), -cad.CONTACT_DOME_CROWN)
    cr = cad.p_xyz(path, cad.CONTACT_REF[0], cad.CONTACT_REF[1], -cad.CONTACT_DOME_CROWN)
    note("medial", c1, (12.0, 4.0), f"C1 (u {cad.CONTACT_1[0]}, s {cad.CONTACT_1[1]})\nM7 {params['M7']:.1f} recorded, not a driver", red)
    note("medial", c2, (12.0, 0.0), "C2 = C1 + 12.0 at 22°", red)
    note("medial", cr, (12.0, -3.0), f"REF (u {cad.CONTACT_REF[0]}, s {cad.CONTACT_REF[1]})\nM6 {params['M6']:.1f} recorded, not a driver", red)
    # M4 and M3 on the edge-on view.
    hook_root = rotate_x(np.array([float(params["HOOK_ROOT_X"]), float(params["HOOK_ROOT_Y"]), 0.0]), theta)
    y0 = pt("posterior", (0.0, 0.0, 2.0))
    yh = pt("posterior", hook_root + np.array([0.0, 0.0, 2.0]))
    ax_views.annotate("", xy=(y0[0], y0[1] + 3.0), xytext=(yh[0], y0[1] + 3.0), arrowprops={"arrowstyle": "<->", "lw": 0.6, "color": red, "shrinkA": 0, "shrinkB": 0}, zorder=8)
    ax_views.text(y0[0] - 1.0, y0[1] + 4.2, f"M4 {params['M4']:.1f} → hook plane\ny = M4/2 = {params['HOOK_ROOT_Y']:.1f}", fontsize=6.2, color=red, zorder=8, ha="right")
    span_row = manifest["span"]["body_full_p15"]
    crown = pt("posterior", c2)
    lid_top = pt("posterior", cad.p_xyz(path, float(params["CONTACT_2_U"]), float(params["CONTACT_2_S"]), thick))
    ax_views.annotate("", xy=(crown[0], crown[1]), xytext=(lid_top[0], crown[1]), arrowprops={"arrowstyle": "<->", "lw": 0.6, "color": red, "shrinkA": 0, "shrinkB": 0}, zorder=8)
    ax_views.text(lid_top[0] + 1.5, crown[1], f"M3 {span_row['M3']:.1f}\nvs SPAN {span_row['span']:.2f}\n= BODY_THICK\n{thick:.1f} + crown\n1.35", fontsize=6.2, color=red, va="center", ha="left", zorder=8)
    if manifest.get("stage") == "shell":
        s5e = cad.load_s5e_shell()
        width = float(params["BODY_WIDTH"])
        note(
            "posterior",
            cad.p_xyz(path, width + 0.2, s5e.p4[1], s5e.p4_y),
            (6.0, 8.0),
            f"P4 wall ({s5e.p4[0]:.2f}, {s5e.p4[1]:.2f}, y {s5e.p4_y:.2f})\nclamped +u, Ø2.7 (Q90)",
            red,
        )
        note(
            "posterior",
            cad.p_xyz(path, width + 0.2, s5e.p5[1], s5e.p5_y),
            (6.0, -10.0),
            f"P5 wall ({s5e.p5[0]:.2f}, {s5e.p5[1]:.2f}, y {s5e.p5_y:.2f})\nclamped +u, Ø2.7 (Q90)",
            red,
        )

    ax_views.set_xlim(-6.0, cursor + 22.0)
    ax_views.set_ylim(bottom - 7.0, top + 5.0)
    ax_views.set_aspect("equal")
    ax_views.set_axis_off()
    scale_bar(ax_views, 0.0, bottom - 3.0, size=7)

    section_lip(ax_lip, cad, lid_y)
    section_nubs(ax_nub, cad, lid_y, float(params.get("CLEAR_FIT", 0.4)))
    section_tail(ax_tail, cad, lid_y, thick)

    ax_m.axis("off")
    ax_e.axis("off")
    m_rows = [
        ["M", "value", "where it lands on the part"],
        ["M1", f"{params['M1']:.2f}", f"gate M1 ≥ TOTAL_CHORD + 3 = {gate['gate']:.2f}"],
        ["M2", f"{params['M2']:.2f}", f"CREASE_BOW {params['CREASE_BOW']:.2f}, " + ("computed from M1 and M2" if manifest["crease_bow"]["source"].startswith("computed") else "default (M1 and M2 not both measured)")],
        ["M3", f"{params['M3']:.2f}", f"span report: SPAN {span_row['span']:.2f}"],
        ["M4", f"{params['M4']:.2f}", f"HOOK_ROOT Y = M4/2 = {params['HOOK_ROOT_Y']:.2f}"],
        ["M5", f"{params['M5']:.2f}", flat],
        ["M6", f"{params['M6']:.2f}", "recorded for WP7a; not a CAD driver"],
        ["M7", f"{params['M7']:.2f}", "recorded for WP7a; not a CAD driver"],
        ["M8", f"{params['M8']:.2f}", f"HOOK_RADIUS {hr:.2f}"],
    ]
    table_m = ax_m.table(cellText=m_rows, loc="center", cellLoc="left", colWidths=[0.09, 0.13, 0.78])
    table_m.auto_set_font_size(False)
    table_m.set_fontsize(6.2)
    table_m.scale(1.0, 1.25)
    ax_m.set_title("M1–M8 (defaults unless measured)", fontsize=8.5, pad=10)

    ex = manifest["exceptions"]
    e_rows = [["id", "feature", "nominal", "fitted min", "note"]]
    for eid in ("E1", "E2", "E3", "E4"):
        e_rows.append([eid, ex[eid]["feature"], f"{ex[eid]['plan_size']}", f"{ex[eid]['minimum']}", ex[eid].get("note", "")])
    e_rows.append(["E5", "lip cantilever", f"{ex['E5']['plan_size']['lip']}", f"{ex['E5']['minimum']['lip']}", "below JLC 1.5"])
    e_rows.append(["E5", "snap bump", f"{ex['E5']['plan_size']['bump']}", f"{ex['E5']['minimum']['bump']}", "below JLC 1.5"])
    table_e = ax_e.table(cellText=e_rows, loc="center", cellLoc="left", colWidths=[0.08, 0.30, 0.14, 0.16, 0.32])
    table_e.auto_set_font_size(False)
    table_e.set_fontsize(6.2)
    table_e.scale(1.0, 1.25)
    ax_e.set_title("E1–E5 exceptions (plan §3.6), from manifest.json", fontsize=8.5, pad=10)

    ax_block.axis("off")
    lines = [
        f"parameter set: {parameter_set_name(manifest)}   SIDE={params.get('SIDE', 'right')}   "
        f"VARIANT={params['VARIANT']}   HOOK_PRELOAD={params['HOOK_PRELOAD']}",
        f"CREASE_BOW={params['CREASE_BOW']:.2f}   TOTAL_CHORD={gate['total_chord']:.3f}   "
        f"chord gate: M1 ≥ {gate['gate']:.3f}",
        f"solids commit {commit}   date {date}",
        "General tolerance: ±0.3 mm under 100 mm, JLC MJF PA12",
        "Built fillets (plan §3.5 asks hook joint 2.0, lip root 0.5; open questions Q3, Q4):",
        *("  " + row for row in fillet_summary(manifest)),
        "Numbers are plan §3.3/§3.5 constants and manifest values, not pixel measurements. Views are",
        "orthographic STL shading at one scale; sections are drawn from the constants. Thin p15 and",
        "full p25 differ only in BODY_THICK 7.0 and HOOK_PRELOAD 2.5 (see render_medial.png).",
    ]
    if manifest.get("stage") == "shell":
        lines = [
            f"Winner {manifest.get('winner', '')}   STAGE=shell   provisional: true",
            f"params {manifest.get('params_file', '')}   sha256 {str(manifest.get('params_sha256', ''))[:12]}…",
            f"Q34 M1={params['M1']:.1f} default.toml (blank). Interface II, standoff {params.get('V2_STANDOFF', 3.0)} mm.",
            f"VARIANT={params['VARIANT']}   HOOK_PRELOAD={params['HOOK_PRELOAD']}",
            f"CREASE_BOW={params['CREASE_BOW']:.2f}   TOTAL_CHORD={gate['total_chord']:.3f}   "
            f"chord gate: M1 ≥ {gate['gate']:.3f}",
            f"solids commit {commit}   date {date}",
            "General tolerance: ±0.3 mm under 100 mm, JLC MJF PA12",
            "Closure: Q89 hinge lip plus concealed medial-tail M2.5×8 into a lid boss. S4 pull/drop qualitative.",
            "Head in the well at y 1.55; lid boss drops 3.2 mm; ≥ 3 mm of thread in the lid (V2_CLOSURE).",
            "Contacts: titanium ISO 7380 heads through Ø2.7 holes (bought, not printed).",
            "Q90: P4/P5 clamped button-heads in the posterior wall (third view). Skin face: P1–P3 and the well only.",
            "Q81: no USB receptacle at M1 52. Q89 lid boss / M2.5×8. No text on the outside. Q59 slot stays.",
            *("  " + row for row in fillet_summary(manifest)),
            "Rolf approves the two renders before any shell order. Nothing is ordered here.",
        ]
    ax_block.text(0.0, 1.0, "\n".join(lines), ha="left", va="top", fontsize=6.6, family="monospace", linespacing=1.35)

    data = save_pdf_and_debug(
        fig,
        debug_png,
        title=(
            "Elicio shell v2 drawing"
            if manifest.get("stage") == "shell"
            else "Elicio BTE fit gauge v1 drawing"
        ),
    )
    return write_bytes(out_dir / "drawing.pdf", data)


def save_pdf_and_debug(fig, debug_png: Path | None, title: str = "Elicio BTE fit gauge v1 drawing") -> bytes:
    if debug_png is not None:
        debug_png.mkdir(parents=True, exist_ok=True)
        fig.savefig(debug_png / "drawing_page.png", format="png", dpi=160, facecolor="white")
    return save_pdf(fig, title=title)


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
    parser.add_argument("--debug-png", type=Path, default=None, help="also write drawing_page.png here (not hashed)")
    args = parser.parse_args(argv)
    out_dir = args.out
    manifest_path = out_dir / "manifest.json"
    if not manifest_path.is_file():
        raise RenderError(f"missing {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    needed = (
        ("body_full_p15.stl", "lid.stl")
        if manifest.get("stage") == "shell"
        else ("body_full_p15.stl", "body_thin_p15.stl", "lid.stl")
    )
    for name in needed:
        if not (out_dir / name).is_file():
            raise RenderError(f"missing {out_dir / name}")
    configure_matplotlib()
    cad = load_cad()
    manifest_commit = str(manifest.get("commit") or "unknown")
    if manifest.get("stage") == "shell":
        stamp_commit = solids_stamp_commit(manifest, out_dir)
        recorded_commit = manifest_commit
    else:
        stamp_commit = cad.git_commit_solids(REPO_ROOT, None)
        recorded_commit = stamp_commit
    date_id = (
        stamp_commit[: -len(" dirty")]
        if stamp_commit.endswith(" dirty")
        else stamp_commit
    )
    date = git_commit_date("HEAD" if stamp_commit.endswith(" dirty") else date_id)
    views = {
        "render_medial.png": render_medial(out_dir, manifest=manifest, commit=stamp_commit, date=date),
        "render_lateral.png": render_lateral(out_dir, manifest=manifest, commit=stamp_commit, date=date),
        "drawing.pdf": draw_page(
            out_dir, cad=cad, manifest=manifest, commit=stamp_commit, date=date, debug_png=args.debug_png
        ),
    }
    update_manifest(out_dir, views, recorded_commit, recorded_commit)
    print(json.dumps({"out": str(out_dir), "views": views}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RenderError as exc:
        print(f"RENDER FAIL: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
