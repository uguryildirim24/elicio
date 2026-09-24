#!/usr/bin/env python3
"""Finish elicio-v4's routing after Freerouting: grid A* on the board text.

No pcbnew: reads the .kicad_pcb as text, finds each net's unjoined copper,
routes a 0.10 track between the pieces (vias 0.40/0.15) and appends plain
segment/via blocks. Optionally drops unlocked segments first (by uuid, e.g.
the items of DRC clearance errors). Locked copper is never touched.

Rules held on the grid (design note §3.2, §5): clearance 0.10 (0.20 to
Contact copper), copper to edge 0.30, no track in the RF band, no via in a
via keep-out (landings, strips, bend, J3 neck), nothing in the Q84/Q88
land zones, routing only on the island.

Run with the repo venv (numpy):
  .venv/bin/python hardware/board/v4_route_fix.py --pcb PCB [--drop-drc DRC.json] [--out PCB2]
"""
from __future__ import annotations

import argparse
import heapq
import json
import math
import re
import uuid
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
STEP = 0.025
DOMAIN = (2.25, 16.0, 15.75, 37.6)  # the island (design note §4.1)
TRACK_W = 0.10
VIA_D, VIA_DRILL = 0.40, 0.15
CLEAR = 0.10
CONTACT_CLEAR = 0.20
EDGE_CLEAR = 0.30
# Grid discretisation allowance. Every clearance region is convex (inflated
# pad, track or via), so a step between two free cell centres dips into one
# by far less than this; two staircase tracks can sit 0.3 cell (0.007) closer
# than their cell centres.
MARGIN = 0.008
VIA_IN_OWN_PAD: set[str] = set()  # nets whose own pads may carry a stitching via (v4_stitch.py)
VIA_COST = 1.2  # mm of track a via is worth
CONTACT = {"SIG1", "SIG2", "REF"}
NO_ROUTE_AREAS = {"tabs", "tail_pads"}
LAYERS = ("F.Cu", "B.Cu")


# ---------------------------------------------------------------- parsing


def blocks(text: str, kind: str, indent: str = "\n\t") -> list[str]:
    parts = text.split(f"{indent}({kind}")
    out = []
    for p in parts[1:]:
        if p[:1] not in ("\n", " "):
            continue
        depth, i = 1, 0
        while depth and i < len(p):
            depth += {"(": 1, ")": -1}.get(p[i], 0)
            i += 1
        out.append(p[:i])
    return out


def xy(block: str, key: str) -> tuple[float, float]:
    m = re.search(r"\(" + key + r" ([-\d.e]+) ([-\d.e]+)", block)
    return float(m.group(1)), float(m.group(2))


def sval(block: str, key: str) -> str:
    m = re.search(r"\(" + key + r' "([^"]*)"\)', block)
    return m.group(1) if m else ""


def cu_layers(block: str) -> set[str]:
    m = re.search(r"\(layers ([^)]*)\)", block)
    names = set(re.findall(r'"([^"]+)"', m.group(1))) if m else set()
    if "*.Cu" in names:
        return set(LAYERS)
    return names & set(LAYERS)


def poly_dist(px, py, edges: np.ndarray):
    """Distance from points to a filled polygon (0 inside, even-odd). edges: (n, 4) x0 y0 x1 y1."""
    px, py = np.asarray(px, float), np.asarray(py, float)
    shape = np.broadcast(px, py).shape
    xs, ys = np.broadcast_to(px, shape).reshape(-1), np.broadcast_to(py, shape).reshape(-1)
    x0, y0, x1, y1 = (edges[:, i] for i in range(4))
    vx, vy = x1 - x0, y1 - y0
    ll = np.where(vx * vx + vy * vy > 0, vx * vx + vy * vy, 1e-12)
    out = np.empty(xs.size)
    chunk = max(1, 1_000_000 // len(edges))
    for a in range(0, xs.size, chunk):
        x, y = xs[a:a + chunk, None], ys[a:a + chunk, None]
        cond = (y0 > y) != (y1 > y)
        with np.errstate(divide="ignore", invalid="ignore"):
            xi = x0 + (y - y0) * vx / (y1 - y0)
        inside = (cond & (x < xi)).sum(axis=1) % 2 == 1
        tt = np.clip(((x - x0) * vx + (y - y0) * vy) / ll, 0, 1)
        d = np.hypot(x - x0 - tt * vx, y - y0 - tt * vy).min(axis=1)
        out[a:a + chunk] = np.where(inside, 0.0, d)
    return out.reshape(shape)


class Shape:
    """Pad, track or via copper: a capsule (segment with radius), a rotated box,
    or a filled zone polygon."""

    def __init__(self, net: str, layers: set[str], *, seg=None, r=0.0, box=None, poly=None, locked=False, uid="",
                 kind=""):
        self.net, self.layers, self.seg, self.r, self.box = net, layers, seg, r, box
        self.locked, self.uid, self.kind = locked, uid, kind
        self.rc = 0.0  # roundrect corner radius
        self.poly = poly
        if poly is not None:
            pts = np.asarray(poly, float)
            self.edges = np.hstack([pts, np.roll(pts, -1, axis=0)])

    def dist(self, px, py):
        """Distance from points to the copper (0 inside). Works on numpy arrays."""
        if self.poly is not None:
            return poly_dist(px, py, self.edges)
        if self.box is not None:
            cx, cy, hw, hh, ang = self.box
            c, s = math.cos(ang), math.sin(ang)
            dx, dy = px - cx, py - cy
            # Board = pos + [[c, s], [-s, c]] local (KiCad angles, y down); invert.
            lx = np.abs(dx * c - dy * s) - hw + self.rc
            ly = np.abs(dx * s + dy * c) - hh + self.rc
            return np.maximum(np.hypot(np.maximum(lx, 0), np.maximum(ly, 0)) - self.rc, 0)
        (x0, y0), (x1, y1) = self.seg
        vx, vy = x1 - x0, y1 - y0
        ll = vx * vx + vy * vy
        t = np.clip(((px - x0) * vx + (py - y0) * vy) / ll, 0, 1) if ll > 0 else 0
        return np.maximum(np.hypot(px - (x0 + t * vx), py - (y0 + t * vy)) - self.r, 0)

    def center(self) -> tuple[float, float]:
        if self.poly is not None:
            return float(np.mean(self.edges[:, 0])), float(np.mean(self.edges[:, 1]))
        if self.box is not None:
            return self.box[0], self.box[1]
        (x0, y0), (x1, y1) = self.seg
        return (x0 + x1) / 2, (y0 + y1) / 2

    def bbox(self, grow: float) -> tuple[float, float, float, float]:
        if self.poly is not None:
            xs, ys = [p[0] for p in self.poly], [p[1] for p in self.poly]
            return min(xs) - grow, min(ys) - grow, max(xs) + grow, max(ys) + grow
        if self.box is not None:
            cx, cy, hw, hh, _ = self.box
            e = math.hypot(hw, hh) + grow
            return cx - e, cy - e, cx + e, cy + e
        (x0, y0), (x1, y1) = self.seg
        e = self.r + grow
        return min(x0, x1) - e, min(y0, y1) - e, max(x0, x1) + e, max(y0, y1) + e


def parse_board(text: str):
    shapes: list[Shape] = []
    holes: list[tuple[float, float, float]] = []  # NPTH only; via holes are handled in Grid.stamp
    for fp in blocks(text, "footprint"):
        fx, fy = xy(fp, "at")
        m = re.search(r"\n\t\t\(at [-\d.]+ [-\d.]+ ([-\d.]+)\)", fp)
        frot = math.radians(float(m.group(1))) if m else 0.0
        name = fp.split("\n", 1)[0].strip().strip('"')
        for pad in blocks(fp, "pad", "\n\t\t"):
            head = pad.split("\n", 1)[0]
            pm = re.match(r' "([^"]*)" (\w+) (\w+)', head)
            kind, shape = pm.group(2), pm.group(3)
            am = re.search(r"\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)", pad)
            px, py = float(am.group(1)), float(am.group(2))
            prot = math.radians(float(am.group(3) or 0))
            ax = fx + px * math.cos(frot) + py * math.sin(frot)
            ay = fy - px * math.sin(frot) + py * math.cos(frot)
            w, h = xy(pad, "size")
            if kind == "np_thru_hole":
                holes.append((ax, ay, w / 2))
                continue
            layers = cu_layers(pad)
            if not layers:
                continue  # mask or paste aperture only
            net = sval(pad, "net")
            if shape == "custom" and "RING" in name:
                outer = 2.5 if "D5" in name else 2.3
                shapes.append(Shape(net, layers, seg=((fx, fy), (fx, fy)), r=outer, kind="pad"))
                continue
            if shape == "custom":
                # Copper is the primitives (pad-local, turned by the pad angle) plus the anchor.
                c, s = math.cos(prot), math.sin(prot)
                for prim in re.findall(r"\(gr_poly\s*\(pts([\s\S]*?)\)\s*\(width", pad):
                    loc = [(float(a), float(b)) for a, b in re.findall(r"\(xy ([-\d.]+) ([-\d.]+)\)", prim)]
                    pts = [(ax + lx * c + ly * s, ay - lx * s + ly * c) for lx, ly in loc]
                    if len(pts) >= 3:
                        shapes.append(Shape(net, layers, poly=pts, kind="pad"))
            if shape == "circle" or (shape == "custom" and "(anchor circle)" in pad):
                shapes.append(Shape(net, layers, seg=((ax, ay), (ax, ay)), r=w / 2, kind="pad"))
            elif shape == "oval":
                a = w / 2 - h / 2 if w > h else 0
                b = h / 2 - w / 2 if h > w else 0
                c, s = math.cos(prot), math.sin(prot)
                dx, dy = a * c + b * s, -a * s + b * c
                shapes.append(Shape(net, layers, seg=((ax - dx, ay - dy), (ax + dx, ay + dy)), r=min(w, h) / 2, kind="pad"))
            else:
                box = Shape(net, layers, box=(ax, ay, w / 2, h / 2, prot), kind="pad")
                rr = re.search(r"\(roundrect_rratio ([-\d.]+)\)", pad)
                if shape == "roundrect" and rr:
                    box.rc = float(rr.group(1)) * min(w, h)
                shapes.append(box)
    for seg in blocks(text, "segment"):
        shapes.append(Shape(sval(seg, "net"), {sval(seg, "layer")}, seg=(xy(seg, "start"), xy(seg, "end")),
                            r=float(re.search(r"\(width ([-\d.]+)\)", seg).group(1)) / 2,
                            locked="(locked yes)" in seg, uid=sval(seg, "uuid"), kind="track"))
    for via in blocks(text, "via"):
        at = xy(via, "at")
        d = float(re.search(r"\(size ([-\d.]+)\)", via).group(1))
        shapes.append(Shape(sval(via, "net"), set(LAYERS), seg=(at, at), r=d / 2,
                            locked="(locked yes)" in via, uid=sval(via, "uuid"), kind="via"))
    edges = []
    for kind in ("gr_line", "gr_arc"):
        for g in blocks(text, kind):
            if '"Edge.Cuts"' in g:
                edges.append((xy(g, "start"), xy(g, "end")))
    zones = []
    for z in blocks(text, "zone"):
        if "(keepout" not in z:
            # Copper pour: each filled_polygon is one island of the fill.
            for fp in blocks(z, "filled_polygon", "\n\t\t"):
                pts = [(float(a), float(b)) for a, b in re.findall(r"\(xy ([-\d.]+) ([-\d.]+)\)", fp)]
                if len(pts) >= 3:
                    shapes.append(Shape(sval(z, "net"), {sval(fp, "layer")}, poly=pts, kind="fill"))
        pts = [(float(a), float(b)) for a, b in re.findall(r"\(xy ([-\d.]+) ([-\d.]+)\)", z.split("(polygon", 1)[1])]
        flags = z.split("(keepout", 1)[1].split("(placement", 1)[0] if "(keepout" in z else ""
        zones.append({
            "name": sval(z, "name"),
            "layers": cu_layers(z) or set(LAYERS),
            "pts": pts,
            "no_tracks": "(tracks not_allowed)" in flags,
            "no_vias": "(vias not_allowed)" in flags,
            "rule_area": "(keepout" in z,
        })
    return shapes, holes, edges, zones


# ---------------------------------------------------------------- connectivity


def touches(a: Shape, b: Shape) -> bool:
    if not (a.layers & b.layers):
        return False
    ab, bb = a.bbox(0.0), b.bbox(0.0)
    if ab[0] > bb[2] + 1e-3 or bb[0] > ab[2] + 1e-3 or ab[1] > bb[3] + 1e-3 or bb[1] > ab[3] + 1e-3:
        return False
    pts = []
    for s in (a, b):
        if s.poly is not None:
            pts.append((s.edges[:, 0], s.edges[:, 1], 0.0))
        elif s.seg is not None:
            (x0, y0), (x1, y1) = s.seg
            n = max(2, int(math.hypot(x1 - x0, y1 - y0) / 0.02) + 1)
            pts.append((np.linspace(x0, x1, n), np.linspace(y0, y1, n), s.r))
        else:
            # A box: its inscribed circle plus its corners and edge midpoints, so a fill
            # that meets one edge of a rectangular pad counts as touching it.
            cx, cy, hw, hh, ang = s.box
            c, sn = math.cos(ang), math.sin(ang)
            px, py = [cx], [cy]
            for u, v in ((hw, hh), (hw, -hh), (-hw, hh), (-hw, -hh), (hw, 0), (-hw, 0), (0, hh), (0, -hh)):
                px.append(cx + u * c - v * sn)
                py.append(cy + u * sn + v * c)
            pts.append((np.array(px), np.array(py), np.array([min(hw, hh)] + [0.0] * 8)))
    ax, ay, ar = pts[0]
    bx, by, br = pts[1]
    return bool((b.dist(ax, ay) <= ar + 1e-3).any() or (a.dist(bx, by) <= br + 1e-3).any())


def components(shapes: list[Shape], net: str) -> list[list[Shape]]:
    items = [s for s in shapes if s.net == net]
    parent = list(range(len(items)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if find(i) != find(j) and touches(items[i], items[j]):
                parent[find(i)] = find(j)
    groups: dict[int, list[Shape]] = {}
    for i, s in enumerate(items):
        groups.setdefault(find(i), []).append(s)
    return list(groups.values())


# ---------------------------------------------------------------- grid


class Grid:
    def __init__(self, shapes, holes, edges, zones):
        u0, s0, u1, s1 = DOMAIN
        self.nx = int(round((u1 - u0) / STEP)) + 1
        self.ny = int(round((s1 - s0) / STEP)) + 1
        self.xs = u0 + np.arange(self.nx) * STEP
        self.ys = s0 + np.arange(self.ny) * STEP
        self.nets: dict[str, int] = {}
        # owner: -1 free, -2 blocked for all, k >= 0 blocked for every net but k.
        self.track = {l: np.full((self.ny, self.nx), -1, np.int32) for l in LAYERS}
        self.via = {l: np.full((self.ny, self.nx), -1, np.int32) for l in LAYERS}
        gx, gy = np.meshgrid(self.xs, self.ys)
        inside = np.zeros(gx.shape, bool)
        dedge = np.full(gx.shape, 1e9)
        for (x0, y0), (x1, y1) in edges:
            cond = (y0 > gy) != (y1 > gy)
            with np.errstate(divide="ignore", invalid="ignore"):
                xi = x0 + (gy - y0) * (x1 - x0) / (y1 - y0)
            inside ^= cond & (gx < xi)
            vx, vy = x1 - x0, y1 - y0
            ll = vx * vx + vy * vy or 1e-12
            t = np.clip(((gx - x0) * vx + (gy - y0) * vy) / ll, 0, 1)
            dedge = np.minimum(dedge, np.hypot(gx - x0 - t * vx, gy - y0 - t * vy))
        for l in LAYERS:
            self.track[l][~inside | (dedge < EDGE_CLEAR + TRACK_W / 2 + MARGIN)] = -2
            self.via[l][~inside | (dedge < EDGE_CLEAR + VIA_D / 2)] = -2
        for z in zones:
            if not z["rule_area"]:
                continue
            poly = z["pts"]
            din = self._poly_dist(gx, gy, poly)
            for l in z["layers"]:
                if z["name"] in NO_ROUTE_AREAS:
                    self.track[l][din < 1.0 + TRACK_W / 2] = -2
                    self.via[l][din < 1.0 + VIA_D / 2] = -2
                if z["no_tracks"]:
                    self.track[l][din < TRACK_W / 2 + MARGIN] = -2
                    self.via[l][din < VIA_D / 2] = -2
                if z["no_vias"]:
                    self.via[l][din < VIA_D / 2] = -2
        for hx, hy, hr in holes:
            # Hole clearance 0.20 to copper; hole to hole 0.25.
            for l in LAYERS:
                self._stamp_circle(self.track[l], hx, hy, hr + 0.20 + TRACK_W / 2 + MARGIN, -2)
                self._stamp_circle(self.via[l], hx, hy, max(hr + 0.20 + VIA_D / 2, hr + 0.25 + VIA_DRILL / 2), -2)
        for s in shapes:
            self.stamp(s)

    def nid(self, net: str) -> int:
        return self.nets.setdefault(net, len(self.nets))

    @staticmethod
    def _poly_dist(gx, gy, poly):
        """0 inside the polygon, else the distance to it."""
        inside = np.zeros(gx.shape, bool)
        d = np.full(gx.shape, 1e9)
        for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
            cond = (y0 > gy) != (y1 > gy)
            with np.errstate(divide="ignore", invalid="ignore"):
                xi = x0 + (gy - y0) * (x1 - x0) / (y1 - y0)
            inside ^= cond & (gx < xi)
            vx, vy = x1 - x0, y1 - y0
            ll = vx * vx + vy * vy or 1e-12
            t = np.clip(((gx - x0) * vx + (gy - y0) * vy) / ll, 0, 1)
            d = np.minimum(d, np.hypot(gx - x0 - t * vx, gy - y0 - t * vy))
        return np.where(inside, 0.0, d)

    def _window(self, bb):
        u0, s0 = DOMAIN[0], DOMAIN[1]
        i0 = max(0, int(math.floor((bb[0] - u0) / STEP)))
        i1 = min(self.nx, int(math.ceil((bb[2] - u0) / STEP)) + 1)
        j0 = max(0, int(math.floor((bb[1] - s0) / STEP)))
        j1 = min(self.ny, int(math.ceil((bb[3] - s0) / STEP)) + 1)
        return i0, i1, j0, j1

    def _stamp_circle(self, arr, x, y, r, val):
        i0, i1, j0, j1 = self._window((x - r, y - r, x + r, y + r))
        if i0 >= i1 or j0 >= j1:
            return
        gx, gy = np.meshgrid(self.xs[i0:i1], self.ys[j0:j1])
        arr[j0:j1, i0:i1][np.hypot(gx - x, gy - y) < r] = val

    def _claim(self, arr, win, mask, k):
        i0, i1, j0, j1 = win
        sub = arr[j0:j1, i0:i1]
        free = mask & (sub == -1)
        clash = mask & (sub >= 0) & (sub != k)
        sub[free] = k
        sub[clash] = -2

    def stamp(self, s: Shape) -> None:
        k = self.nid(s.net)
        clr = CONTACT_CLEAR if s.net in CONTACT else CLEAR
        grow_t = clr + TRACK_W / 2 + MARGIN
        grow_v = clr + VIA_D / 2
        win = self._window(s.bbox(grow_v))
        i0, i1, j0, j1 = win
        if i0 >= i1 or j0 >= j1:
            return
        gx, gy = np.meshgrid(self.xs[i0:i1], self.ys[j0:j1])
        d = s.dist(gx, gy)
        for l in s.layers:
            self._claim(self.track[l], win, d < grow_t, k)
            self._claim(self.via[l], win, d < grow_v, k)
            if s.kind == "pad":
                if s.net in VIA_IN_OWN_PAD:
                    # Stitching (v4_stitch.py): a via may sit fully inside a big own-net pad
                    # (an exposed or mounting pad, 0.20 in from its edge) or touch a small
                    # own-net pad's edge with its hole 0.05 outside the copper. It still
                    # stays out of every other pad.
                    sub = self.via[l][j0:j1, i0:i1]
                    sub[(d > -(VIA_D / 2 + 0.20)) & (d < VIA_DRILL / 2 + 0.05)] = -2
                else:
                    # No via in any pad, own net included.
                    self.via[l][j0:j1, i0:i1][d < VIA_D / 2 + 0.02] = -2
        if s.kind == "via":
            # Hole to hole 0.25 for any net's via.
            (x, y), _ = s.seg
            for l in LAYERS:
                self._stamp_circle(self.via[l], x, y, 0.25 + VIA_DRILL, -2)

    def cell(self, x: float, y: float) -> tuple[int, int]:
        return int(round((x - DOMAIN[0]) / STEP)), int(round((y - DOMAIN[1]) / STEP))

    def pos(self, i: int, j: int) -> tuple[float, float]:
        return round(DOMAIN[0] + i * STEP, 4), round(DOMAIN[1] + j * STEP, 4)


# ---------------------------------------------------------------- search

MOVES = [(1, 0, 1.0), (-1, 0, 1.0), (0, 1, 1.0), (0, -1, 1.0),
         (1, 1, math.sqrt(2)), (1, -1, math.sqrt(2)), (-1, 1, math.sqrt(2)), (-1, -1, math.sqrt(2))]


def seed_cells(grid: Grid, comp: list[Shape], k: int) -> set[tuple[int, int, int]]:
    """Grid cells inside a component's copper that this net may stand on."""
    out = set()
    for s in comp:
        win = grid._window(s.bbox(0.0))
        i0, i1, j0, j1 = win
        if i0 >= i1 or j0 >= j1:
            continue
        gx, gy = np.meshgrid(grid.xs[i0:i1], grid.ys[j0:j1])
        inside = s.dist(gx, gy) <= 1e-9
        for li, l in enumerate(LAYERS):
            if l not in s.layers:
                continue
            ok = inside & np.isin(grid.track[l][j0:j1, i0:i1], (-1, k))
            for jj, ii in zip(*np.nonzero(ok)):
                out.add((li, i0 + ii, j0 + jj))
    return out


def astar(grid: Grid, k: int, starts, goals, cap: int = 3_000_000, soft: Grid | None = None, pen: float = 0.0):
    """Multi-source A*. With soft, cells free on grid but taken on soft (other
    nets' unlocked copper) are allowed at pen extra cells each (rip-up search)."""
    if not starts or not goals:
        return None
    gl = np.array([(i, j) for _, i, j in goals], float)
    gb = (gl[:, 0].min(), gl[:, 1].min(), gl[:, 0].max(), gl[:, 1].max())

    def h(i, j):
        dx = max(gb[0] - i, 0, i - gb[2])
        dy = max(gb[1] - j, 0, j - gb[3])
        return math.hypot(dx, dy)

    ok_t = [np.isin(grid.track[l], (-1, k)) for l in LAYERS]
    ok_v = np.isin(grid.via[LAYERS[0]], (-1, k)) & np.isin(grid.via[LAYERS[1]], (-1, k))
    via_cost = VIA_COST / STEP
    if soft is not None:
        kk = soft.nets.get(grid_net_name(grid, k), -99)
        hit_t = [ok_t[li] & ~np.isin(soft.track[l], (-1, kk)) for li, l in enumerate(LAYERS)]
        hit_v = ok_v & ~(np.isin(soft.via[LAYERS[0]], (-1, kk)) & np.isin(soft.via[LAYERS[1]], (-1, kk)))
    else:
        hit_t, hit_v = None, None
    best = {}
    prev = {}
    heap = []
    for c in starts:
        best[c] = 0.0
        heapq.heappush(heap, (h(c[1], c[2]), 0.0, c))
    goalset = set(goals)
    pops = 0
    while heap:
        f, g, c = heapq.heappop(heap)
        if g > best.get(c, 1e18):
            continue
        if c in goalset:
            path = [c]
            while path[-1] in prev:
                path.append(prev[path[-1]])
            return path[::-1]
        pops += 1
        if pops > cap:
            return None
        li, i, j = c
        okl = ok_t[li]
        for di, dj, w in MOVES:
            ni, nj = i + di, j + dj
            if not (0 <= ni < grid.nx and 0 <= nj < grid.ny) or not okl[nj, ni]:
                continue
            if di and dj and not (okl[j, ni] or okl[nj, i]):
                continue
            n = (li, ni, nj)
            ng = g + w + (pen if hit_t is not None and hit_t[li][nj, ni] else 0.0)
            if ng < best.get(n, 1e18):
                best[n] = ng
                prev[n] = c
                heapq.heappush(heap, (ng + h(ni, nj), ng, n))
        if ok_v[j, i]:
            n = (1 - li, i, j)
            ng = g + via_cost + (pen * 8 if hit_v is not None and hit_v[j, i] else 0.0)
            if ok_t[1 - li][j, i] and ng < best.get(n, 1e18):
                best[n] = ng
                prev[n] = c
                heapq.heappush(heap, (ng + h(i, j), ng, n))
    return None


def grid_net_name(grid: Grid, k: int) -> str:
    for name, idx in grid.nets.items():
        if idx == k:
            return name
    return ""


def clear_line(ok, a, b) -> bool:
    """Every grid cell the straight a -> b line passes near is free."""
    (i0, j0), (i1, j1) = a, b
    n = int(max(abs(i1 - i0), abs(j1 - j0)) * 2) + 1
    for t in np.linspace(0, 1, n + 1):
        i, j = i0 + (i1 - i0) * t, j0 + (j1 - j0) * t
        for ii in {math.floor(i), math.ceil(i)}:
            for jj in {math.floor(j), math.ceil(j)}:
                if not ok[jj, ii]:
                    return False
    return True


def path_items(grid: Grid, path, net: str, k: int) -> list[Shape]:
    out: list[Shape] = []
    run = [path[0]]

    def flush(run):
        if len(run) < 2:
            return
        ok = np.isin(grid.track[LAYERS[run[0][0]]], (-1, k))
        cells = [(c[1], c[2]) for c in run]
        pts = [run[0]]
        i = 0
        while i < len(cells) - 1:
            j = len(cells) - 1
            while j > i + 1 and not clear_line(ok, cells[i], cells[j]):
                j -= 1
            pts.append(run[j])
            i = j
        layer = LAYERS[run[0][0]]
        for a, b in zip(pts, pts[1:]):
            out.append(Shape(net, {layer}, seg=(grid.pos(a[1], a[2]), grid.pos(b[1], b[2])), r=TRACK_W / 2,
                             uid=str(uuid.uuid4()), kind="track"))

    for c in path[1:]:
        if c[0] != run[-1][0]:
            flush(run)
            at = grid.pos(c[1], c[2])
            out.append(Shape(net, set(LAYERS), seg=(at, at), r=VIA_D / 2, uid=str(uuid.uuid4()), kind="via"))
            run = [c]
        else:
            run.append(c)
    flush(run)
    return out


# ---------------------------------------------------------------- text out


def seg_text(s: Shape) -> str:
    (x0, y0), (x1, y1) = s.seg
    if s.kind == "via":
        return (f'\t(via\n\t\t(at {x0:g} {y0:g})\n\t\t(size {VIA_D:g})\n\t\t(drill {VIA_DRILL:g})\n'
                f'\t\t(layers "F.Cu" "B.Cu")\n\t\t(net "{s.net}")\n\t\t(uuid "{s.uid}")\n\t)\n')
    return (f"\t(segment\n\t\t(start {x0:g} {y0:g})\n\t\t(end {x1:g} {y1:g})\n\t\t(width {TRACK_W:g})\n"
            f'\t\t(layer "{next(iter(s.layers))}")\n\t\t(net "{s.net}")\n\t\t(uuid "{s.uid}")\n\t)\n')


def drop_blocks(text: str, uids: set[str]) -> tuple[str, int]:
    n = 0
    for kind in ("segment", "via"):
        for b in blocks(text, kind):
            if sval(b, "uuid") in uids and "(locked yes)" not in b:
                text = text.replace(f"\n\t({kind}{b}", "", 1)
                n += 1
    return text, n


def route_open(grid: Grid, cur: list[Shape], net: str, log: bool = True) -> tuple[list[Shape], int]:
    """Join a net's pieces on grid (stamping as it goes). Returns (items, pieces left unjoined)."""
    k = grid.nid(net)
    comps = components(cur, net)
    items_all: list[Shape] = []
    while len(comps) > 1:
        comps.sort(key=lambda cp: -len(cp))
        main_c, rest = comps[0], comps[1:]
        starts = seed_cells(grid, main_c, k)
        goals, owner = set(), {}
        for idx, cp in enumerate(rest):
            for c in seed_cells(grid, cp, k):
                goals.add(c)
                owner[c] = idx
        path = astar(grid, k, starts, goals)
        if path is None:
            if log:
                print(f"FAIL {net}: {len(rest)} piece(s) unreachable")
            return items_all, len(rest)
        items = path_items(grid, path, net, k)
        for s in items:
            grid.stamp(s)
        items_all += items
        joined = rest.pop(owner[path[-1]])
        comps = [main_c + joined + items] + rest
        if log:
            length = sum(math.dist(*s.seg) for s in items if s.kind == "track")
            print(f"routed {net}: {length:.2f} mm, {sum(s.kind == 'via' for s in items)} via(s)")
    return items_all, 0


def victims_of(path, grid: Grid, cur: list[Shape], net: str, keep: set[str]) -> list[Shape]:
    """Unlocked copper of other nets (not in keep) that the path's track or via cells hit."""
    pts = {l: [] for l in LAYERS}
    vias = []
    for a, b in zip(path, path[1:]):
        if a[0] != b[0]:
            vias.append(grid.pos(a[1], a[2]))
    for li, i, j in path:
        pts[LAYERS[li]].append(grid.pos(i, j))
    out = []
    for s in cur:
        if s.locked or s.kind in ("pad", "fill") or s.net == net or s.net in keep:
            continue
        clr = max(CONTACT_CLEAR if s.net in CONTACT else CLEAR, CLEAR)
        hit = False
        for l in s.layers:
            if pts[l]:
                a = np.array(pts[l])
                if (s.dist(a[:, 0], a[:, 1]) < clr + TRACK_W / 2).any():
                    hit = True
        if vias and not hit:
            a = np.array(vias)
            hit = bool((s.dist(a[:, 0], a[:, 1]) < clr + VIA_D / 2).any())
        if hit:
            out.append(s)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pcb", type=Path, required=True)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--drop-drc", type=Path, help="DRC json: drop unlocked tracks named in clearance errors")
    ap.add_argument("--drop", nargs="*", default=[], help="uuids of unlocked tracks/vias to drop")
    ap.add_argument("--nets", nargs="*", help="only these nets")
    ap.add_argument("--skip", nargs="*", default=[], help="nets left alone (e.g. GND, left to pours)")
    ap.add_argument("--ripup", type=int, default=0, help="rounds of local rip-up and reroute for what stays open")
    ap.add_argument("--pen", type=float, default=12.0, help="rip-up: extra cells per cell of other copper crossed")
    ap.add_argument("--soft-fills", action="store_true",
                    help="a filled pour blocks only its own net's routing (it is copper for GND, a source and a "
                         "target); every other net routes through it as if the board were unfilled, since the "
                         "pour yields on the next refill. Use on a filled board; refill and re-join GND after.")
    args = ap.parse_args()
    text = args.pcb.read_text(encoding="utf-8")
    drop = set(args.drop)
    if args.drop_drc:
        rep = json.loads(args.drop_drc.read_text())
        for v in rep.get("violations", []):
            if v["severity"] == "error" and v["type"] in ("clearance", "shorting_items", "tracks_crossing"):
                drop |= {i["uuid"] for i in v["items"] if i["description"].startswith(("Track", "Via"))}
    if drop:
        text, n = drop_blocks(text, drop)
        print("dropped", n, "unlocked items")
    shapes, holes, edges, zones = parse_board(text)
    nets = sorted({s.net for s in shapes if s.net and not s.net.startswith("unconnected")})
    if args.nets:
        nets = [n for n in nets if n in args.nets]
    nets = [n for n in nets if n not in args.skip]
    cur = list(shapes)
    removed: set[str] = set()  # uids of routed copper taken out again

    def gap(net):
        comps = components(cur, net)
        if len(comps) < 2:
            return 0.0
        c = [np.mean([s.center() for s in cp], axis=0) for cp in comps]
        return min(math.dist(a, b) for a in c for b in c if a is not b)

    def mkgrid(net, items=None):
        """The routing grid for net: with --soft-fills, other nets' pours are left out."""
        src = cur if items is None else items
        if args.soft_fills:
            src = [s for s in src if not (s.kind == "fill" and s.net != net)]
        return Grid(src, holes, edges, zones)

    todo = [n for n in nets if len(components(cur, n)) > 1]
    todo.sort(key=gap)
    grid = Grid(cur, holes, edges, zones)
    for net in todo:
        items, _ = route_open(mkgrid(net) if args.soft_fills else grid, cur, net)
        cur += items

    def open_nets():
        return [n for n in nets if len(components(cur, n)) > 1]

    for rnd in range(args.ripup):
        still = open_nets()
        print(f"rip-up round {rnd}: open {still}")
        if not still:
            break
        for net in still:
            if len(components(cur, net)) < 2:
                continue
            before = len(open_nets())
            snap_cur, snap_removed = list(cur), set(removed)
            keep = {net}
            hard = mkgrid(net, [s for s in cur if s.locked or s.kind in ("pad", "fill") or s.net == net])
            full = mkgrid(net)
            k = hard.nid(net)
            comps = components(cur, net)
            comps.sort(key=lambda cp: -len(cp))
            starts = seed_cells(hard, comps[0], k)
            goals = set().union(*(seed_cells(hard, cp, k) for cp in comps[1:]))
            path = astar(hard, k, starts, goals, soft=full, pen=args.pen)
            if path is None:
                print(f"  {net}: no path even through other copper")
                continue
            vic = victims_of(path, hard, cur, net, keep)
            vnets = sorted({s.net for s in vic})
            print(f"  {net}: rips {len(vic)} item(s) of {vnets}")
            vids = {s.uid for s in vic}
            removed |= vids
            cur = [s for s in cur if s.uid not in vids or not s.uid]
            grid = mkgrid(net)
            items, left = route_open(grid, cur, net, log=False)
            cur += items
            for vn in vnets:
                if args.soft_fills:
                    grid = mkgrid(vn)
                items, _ = route_open(grid, cur, vn, log=False)
                cur += items
            after = len(open_nets())
            if after > before or left:
                print(f"  {net}: no gain ({before} -> {after} open nets), reverted")
                cur, removed = snap_cur, snap_removed
            else:
                print(f"  {net}: open nets {before} -> {after}")
    failed = open_nets()
    for n in failed:
        print("OPEN", n, len(components(cur, n)) - 1, "piece(s)")
    added = [s for s in cur if s.kind in ("track", "via") and s.uid and s not in shapes]
    out = args.out or args.pcb
    text, _ = drop_blocks(text, removed)
    body = text.rstrip()
    assert body.endswith(")")
    text = body[:-1] + "".join(seg_text(s) for s in added) + ")\n"
    out.write_text(text, encoding="utf-8")
    print("wrote", out, "added", len(added), "removed", len(removed), "open", len(failed))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
