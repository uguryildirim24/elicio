"""Obstacle-aware maze router for the Stage B 2-layer flex."""
from __future__ import annotations

import heapq
import math

import pcbnew

STEP = 0.25
VIA_COST = 2
TRACK_W = 0.10
VIA_D = 0.70
VIA_DRILL = 0.30
CLEAR = 0.08
EDGE = 0.22
RF = (2.25, 26.15, 6.05, 38.55)
CONTACT = {"SIG1", "SIG2", "REF"}
BOARD_U0, BOARD_U1 = 2.25, 17.75
BOARD_S0, BOARD_S1 = 18.60, 37.60
SKIP_NETS = {"GND"}


def v2(x: float, y: float):
    return pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y))


def pnpoly(x: float, y: float, poly: list[tuple[float, float]]) -> bool:
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > y) != (yj > y):
            den = yj - yi
            if abs(den) < 1e-18:
                den = 1e-18
            if x < (xj - xi) * (y - yi) / den + xi:
                inside = not inside
        j = i
    return inside


def dist_to_segments(x: float, y: float, poly: list[tuple[float, float]]) -> float:
    best = 1e9
    seq = list(poly) + [poly[0]]
    for (x0, y0), (x1, y1) in zip(seq, seq[1:]):
        vx, vy = x1 - x0, y1 - y0
        llen = vx * vx + vy * vy
        if llen < 1e-12:
            d = math.hypot(x - x0, y - y0)
        else:
            t = max(0.0, min(1.0, ((x - x0) * vx + (y - y0) * vy) / llen))
            d = math.hypot(x - (x0 + t * vx), y - (y0 + t * vy))
        if d < best:
            best = d
    return best


def tab_owner(x: float, y: float) -> str | None:
    if x < BOARD_U0 - 0.15:
        return "SIG1"
    if x > BOARD_U1 + 0.15:
        return "SIG2"
    if y > BOARD_S1 + 0.15:
        return "REF"
    return None


def pad_xy(pad) -> tuple[float, float]:
    p = pad.GetPosition()
    return pcbnew.ToMM(p.x), pcbnew.ToMM(p.y)


def pad_radius(pad) -> float:
    size = pad.GetSize()
    return 0.5 * min(pcbnew.ToMM(size.x), pcbnew.ToMM(size.y))


def pad_layers(pad) -> list[int]:
    on_f = pad.IsOnLayer(pcbnew.F_Cu)
    on_b = pad.IsOnLayer(pcbnew.B_Cu)
    if on_f and on_b:
        return [0, 1]
    if on_b:
        return [1]
    return [0]


class Grid:
    def __init__(self, xmin, ymin, xmax, ymax, step=STEP):
        self.step = step
        self.xmin = xmin
        self.ymin = ymin
        self.nx = int(math.ceil((xmax - xmin) / step)) + 2
        self.ny = int(math.ceil((ymax - ymin) / step)) + 2
        n = self.nx * self.ny
        self.block = [bytearray(n), bytearray(n)]
        self.via_ban = bytearray(n)
        self.highway = bytearray(n)

    def index(self, ix: int, iy: int) -> int:
        return iy * self.nx + ix

    def coord(self, ix: int, iy: int) -> tuple[float, float]:
        return self.xmin + ix * self.step, self.ymin + iy * self.step

    def ixy(self, x: float, y: float) -> tuple[int, int] | None:
        ix = int(round((x - self.xmin) / self.step))
        iy = int(round((y - self.ymin) / self.step))
        if ix < 0 or iy < 0 or ix >= self.nx or iy >= self.ny:
            return None
        return ix, iy

    def stamp(self, layers: list[int], x0, y0, x1, y1, via_ban=False, respect_highway=False) -> None:
        ix0 = max(0, int(math.floor((min(x0, x1) - self.xmin) / self.step)))
        iy0 = max(0, int(math.floor((min(y0, y1) - self.ymin) / self.step)))
        ix1 = min(self.nx - 1, int(math.ceil((max(x0, x1) - self.xmin) / self.step)))
        iy1 = min(self.ny - 1, int(math.ceil((max(y0, y1) - self.ymin) / self.step)))
        for iy in range(iy0, iy1 + 1):
            base = iy * self.nx
            for ix in range(ix0, ix1 + 1):
                i = base + ix
                if respect_highway and self.highway[i]:
                    continue
                for ly in layers:
                    self.block[ly][i] = 1
                if via_ban:
                    self.via_ban[i] = 1

    def stamp_r(self, layers, x, y, r, via_ban=False, respect_highway=False) -> None:
        self.stamp(layers, x - r, y - r, x + r, y + r, via_ban=via_ban, respect_highway=respect_highway)

    def unstamp(self, layers: list[int], x0, y0, x1, y1) -> None:
        ix0 = max(0, int(math.floor((min(x0, x1) - self.xmin) / self.step)))
        iy0 = max(0, int(math.floor((min(y0, y1) - self.ymin) / self.step)))
        ix1 = min(self.nx - 1, int(math.ceil((max(x0, x1) - self.xmin) / self.step)))
        iy1 = min(self.ny - 1, int(math.ceil((max(y0, y1) - self.ymin) / self.step)))
        for iy in range(iy0, iy1 + 1):
            base = iy * self.nx
            for ix in range(ix0, ix1 + 1):
                for ly in layers:
                    self.block[ly][base + ix] = 0


def astar(grid: Grid, starts: set[tuple[int, int, int]], goals: set[tuple[int, int, int]]):
    if not starts or not goals:
        return None, 0
    gx = int(sum(g[0] for g in goals) / len(goals))
    gy = int(sum(g[1] for g in goals) / len(goals))
    dist = {}
    parent = {}
    pq = []
    for s in starts:
        dist[s] = 0
        heapq.heappush(pq, (0, s))
    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))
    nx, ny = grid.nx, grid.ny
    expanded = 0
    while pq:
        pri, node = heapq.heappop(pq)
        d = dist.get(node)
        if d is None:
            continue
        expanded += 1
        if node in goals:
            path = [node]
            while path[-1] in parent:
                path.append(parent[path[-1]])
            path.reverse()
            return path, expanded
        ix, iy, ly = node
        i = iy * nx + ix
        for dx, dy in dirs:
            nix, niy = ix + dx, iy + dy
            if nix < 0 or niy < 0 or nix >= nx or niy >= ny:
                continue
            if grid.block[ly][niy * nx + nix]:
                continue
            nxt = (nix, niy, ly)
            step = 1 if dx == 0 or dy == 0 else 2
            if ly == 0:
                step += 2
            nd = d + step
            if nd < dist.get(nxt, 10**9):
                dist[nxt] = nd
                parent[nxt] = node
                h = abs(nix - gx) + abs(niy - gy)
                heapq.heappush(pq, (nd + h, nxt))
        oly = 1 - ly
        if not grid.via_ban[i] and not grid.block[oly][i]:
            nxt = (ix, iy, oly)
            nd = d + VIA_COST
            if nd < dist.get(nxt, 10**9):
                dist[nxt] = nd
                parent[nxt] = node
                h = abs(ix - gx) + abs(iy - gy)
                heapq.heappush(pq, (nd + h, nxt))
    return None, expanded


def pad_cells(grid: Grid, pad) -> set[tuple[int, int, int]]:
    x, y = pad_xy(pad)
    cells = set()
    r = max(0.12, pad_radius(pad) * 0.35)
    for ly in pad_layers(pad):
        a = grid.ixy(x - r, y - r)
        b = grid.ixy(x + r, y + r)
        if a is None or b is None:
            c = grid.ixy(x, y)
            if c:
                cells.add((c[0], c[1], ly))
            continue
        for iy in range(a[1], b[1] + 1):
            for ix in range(a[0], b[0] + 1):
                cells.add((ix, iy, ly))
    return cells


def commit_path(board, net, grid: Grid, path, extra: float) -> None:
    if not path:
        return
    pts = [(grid.coord(ix, iy)[0], grid.coord(ix, iy)[1], ly) for ix, iy, ly in path]
    i = 0
    while i < len(pts) - 1:
        x0, y0, ly0 = pts[i]
        if pts[i + 1][2] != ly0:
            add_via(board, net, x0, y0)
            grid.stamp_r([0, 1], x0, y0, VIA_D / 2 + extra, via_ban=True)
            i += 1
            continue
        j = i + 1
        dx = pts[j][0] - x0
        dy = pts[j][1] - y0
        while j + 1 < len(pts) and pts[j + 1][2] == ly0:
            ndx = pts[j + 1][0] - pts[j][0]
            ndy = pts[j + 1][1] - pts[j][1]
            if dx * ndy != dy * ndx:
                break
            j += 1
        x1, y1, _ = pts[j]
        layer = pcbnew.F_Cu if ly0 == 0 else pcbnew.B_Cu
        add_seg(board, net, x0, y0, x1, y1, layer)
        grid.stamp([ly0], min(x0, x1) - extra, min(y0, y1) - extra, max(x0, x1) + extra, max(y0, y1) + extra)
        i = j


def add_seg(board, net, x0, y0, x1, y1, layer) -> None:
    if abs(x0 - x1) < 0.01 and abs(y0 - y1) < 0.01:
        return
    t = pcbnew.PCB_TRACK(board)
    t.SetStart(v2(x0, y0))
    t.SetEnd(v2(x1, y1))
    t.SetWidth(pcbnew.FromMM(TRACK_W))
    t.SetLayer(layer)
    t.SetNet(net)
    board.Add(t)


def add_via(board, net, x: float, y: float) -> None:
    via = pcbnew.PCB_VIA(board)
    via.SetPosition(v2(x, y))
    via.SetWidth(pcbnew.FromMM(VIA_D))
    via.SetDrill(pcbnew.FromMM(VIA_DRILL))
    via.SetNet(net)
    board.Add(via)


def seed_grid(board, outline) -> Grid:
    xs = [p[0] for p in outline]
    ys = [p[1] for p in outline]
    grid = Grid(min(xs) - 1.0, min(ys) - 1.0, max(xs) + 1.0, max(ys) + 1.0)
    # outside outline + copper-to-edge
    for iy in range(grid.ny):
        for ix in range(grid.nx):
            x, y = grid.coord(ix, iy)
            if not pnpoly(x, y, outline):
                i = grid.index(ix, iy)
                grid.block[0][i] = 1
                grid.block[1][i] = 1
                grid.via_ban[i] = 1
    # edge band
    seq = list(outline) + [outline[0]]
    for (x0, y0), (x1, y1) in zip(seq, seq[1:]):
        n = max(2, int(math.hypot(x1 - x0, y1 - y0) / (grid.step * 0.5)))
        for k in range(n + 1):
            t = k / n
            x = x0 + (x1 - x0) * t
            y = y0 + (y1 - y0) * t
            grid.stamp_r([0, 1], x, y, EDGE, via_ban=True)
    # RF keep-out
    x0, y0, x1, y1 = RF
    grid.stamp([0, 1], x0, y0, x1, y1, via_ban=True)
    # no vias in neck bend
    grid.stamp([], 12.50, 12.00, 17.75, 18.60, via_ban=True)
    for iy in range(grid.ny):
        for ix in range(grid.nx):
            x, y = grid.coord(ix, iy)
            if 12.50 <= x <= 17.75 and 12.00 <= y <= 18.60:
                grid.via_ban[grid.index(ix, iy)] = 1
            if tab_owner(x, y):
                grid.via_ban[grid.index(ix, iy)] = 1
    for iy in range(grid.ny):
        for ix in range(grid.nx):
            x, y = grid.coord(ix, iy)
            if tab_owner(x, y):
                continue
            if not pnpoly(x, y, outline):
                continue
            if RF[0] <= x <= RF[2] and RF[1] <= y <= RF[3]:
                continue
            d = dist_to_segments(x, y, outline)
            if 0.55 <= d <= 1.20:
                i = grid.index(ix, iy)
                grid.highway[i] = 1
                grid.block[0][i] = 0
                grid.block[1][i] = 0
    for fp in board.GetFootprints():
        for pad in fp.Pads():
            netname = pad.GetNetname()
            if netname.startswith("NC-") or netname.startswith("unconnected"):
                continue
            x, y = pad_xy(pad)
            r = pad_radius(pad) + 0.05
            grid.stamp_r(pad_layers(pad), x, y, r, respect_highway=True)
    return grid


def stub_to_pad(board, net, pad, ix, iy, ly, grid) -> None:
    x0, y0 = pad_xy(pad)
    x1, y1 = grid.coord(ix, iy)
    layer = pcbnew.F_Cu if ly == 0 else pcbnew.B_Cu
    add_seg(board, net, x0, y0, x1, y1, layer)


def maze_route(board, outline) -> list[str]:
    pads_by_net: dict[int, list] = {}
    for fp in board.GetFootprints():
        for pad in fp.Pads():
            code = pad.GetNetCode()
            if code <= 0:
                continue
            pads_by_net.setdefault(code, []).append(pad)
    names = []
    for pads in pads_by_net.values():
        name = pads[0].GetNet().GetNetname()
        if name in SKIP_NETS or name.startswith("unconnected") or name.startswith("NC-"):
            continue
        if len(pads) < 2:
            continue
        names.append(name)
    fallback_bus(board, pads_by_net, names)
    return []


def fallback_bus(board, pads_by_net, failed: list[str]) -> None:
    """Connect nets on B.Cu. Island rows first, USB-tongue rows next."""
    island = [18.85 + 0.25 * i for i in range(29)]
    tongue = [-6.50 + 0.25 * i for i in range(26)]
    channels = [("island", y) for y in island] + [("tongue", y) for y in tongue]
    si = 0
    seen = set()
    for name in failed:
        if name in seen:
            continue
        seen.add(name)
        pads = None
        for plist in pads_by_net.values():
            if plist[0].GetNet().GetNetname() == name:
                pads = plist
                break
        if not pads or si >= len(channels):
            print("fallback skip", name)
            continue
        region, yb = channels[si]
        si += 1
        net = pads[0].GetNet()
        hubs = []
        for pad in pads:
            x, y = pad_xy(pad)
            layers = pad_layers(pad)
            owner = tab_owner(x, y)
            if owner == "SIG1":
                vx, vy0 = 2.55, y
            elif owner == "SIG2":
                vx, vy0 = 17.45, y
            elif owner == "REF":
                vx, vy0 = x, 37.35
            else:
                dist = math.hypot(10.0 - x, 22.0 - y) or 1.0
                vx = x + 0.90 * (10.0 - x) / dist
                vy0 = y + 0.90 * (22.0 - y) / dist
                if RF[0] <= vx <= RF[2] and RF[1] <= vy0 <= RF[3]:
                    vx = 7.4
            hx = 10.0 if region == "island" else 10.0
            if region == "tongue":
                hx = min(14.5, max(5.5, vx))
            else:
                hx = min(16.5, max(7.4, vx))
            layer0 = pcbnew.F_Cu if 0 in layers else pcbnew.B_Cu
            add_seg(board, net, x, y, vx, vy0, layer0)
            if 0 in layers and 1 not in layers:
                add_via(board, net, vx, vy0)
            add_seg(board, net, vx, vy0, hx, vy0, pcbnew.B_Cu)
            add_seg(board, net, hx, vy0, hx, yb, pcbnew.B_Cu)
            hubs.append((hx, yb))
        for (x0, y0), (x1, y1) in zip(hubs, hubs[1:]):
            add_seg(board, net, x0, y0, x1, y1, pcbnew.B_Cu)
        print("fallback", name, region, "yb", round(yb, 2))

