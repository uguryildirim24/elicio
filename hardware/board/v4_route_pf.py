#!/usr/bin/env python3
"""Route elicio-v4 with negotiated congestion (PathFinder) on the board text.

Keeps every locked item (the Contact, charge, reset and +VDD pre-routes and
the U1 bridges), drops every unlocked track and via, then routes each net as
a tree of 0.10 tracks and 0.40/0.15 vias. Nets may overlap early on; the
overlap cost and a per-cell history rise each round until no two nets share
clearance. Grid, rules and keep-outs are those of v4_route_fix.py.

  .venv/bin/python hardware/board/v4_route_pf.py --pcb IN --out OUT [--rounds N]
"""
from __future__ import annotations

import argparse
import heapq
import math
import time
from pathlib import Path

import numpy as np

from v4_route_fix import (
    CLEAR,
    LAYERS,
    MARGIN,
    STEP,
    TRACK_W,
    VIA_COST,
    VIA_D,
    Grid,
    Shape,
    blocks,
    components,
    parse_board,
    seed_cells,
    seg_text,
    sval,
)

import uuid

R_T_TRACK = TRACK_W / 2 + CLEAR + TRACK_W / 2 + MARGIN  # track copper -> other track centrelines
R_V_TRACK = TRACK_W / 2 + CLEAR + VIA_D / 2  # track copper -> other via centres
R_T_VIA = VIA_D / 2 + CLEAR + TRACK_W / 2 + MARGIN
R_V_VIA = VIA_D / 2 + CLEAR + VIA_D / 2


def disk_offsets(r: float, nx: int) -> dict[int, np.ndarray]:
    n = int(math.ceil(r / STEP))
    di, dj = np.meshgrid(np.arange(-n, n + 1), np.arange(-n, n + 1))
    keep = np.hypot(di, dj) * STEP < r
    return di[keep], dj[keep]


class Router:
    def __init__(self, grid: Grid):
        self.g = grid
        self.nx, self.ny = grid.nx, grid.ny
        self.plane = self.nx * self.ny
        # Hard passability per net is (owner == -1) | (owner == k).
        self.count_t = np.zeros((2, self.ny, self.nx), np.int16)
        self.count_v = np.zeros((2, self.ny, self.nx), np.int16)
        self.hist = np.zeros((2, self.ny, self.nx), np.float32)
        self.occ: dict[str, tuple[np.ndarray, np.ndarray]] = {}
        self.paths: dict[str, list[list[int]]] = {}
        # Cells inside a net's own fixed copper (pads, locked tracks): a path
        # there adds no clearance claim; the pad copper is already there and
        # the hard grid keeps other nets off it.
        self.own: dict[str, set[int]] = {}
        self.state: dict[str, dict] = {}
        self.center: dict[str, tuple[np.ndarray, np.ndarray]] = {}
        self.fr_occ: dict[str, np.ndarray] = {}
        self.offs = {r: disk_offsets(r, self.nx) for r in (R_T_TRACK, R_V_TRACK, R_T_VIA, R_V_VIA)}

    # -- occupancy -------------------------------------------------------

    def _disk(self, l: int, i: int, j: int, r: float) -> np.ndarray:
        di, dj = self.offs[r]
        ii, jj = i + di, j + dj
        ok = (ii >= 0) & (ii < self.nx) & (jj >= 0) & (jj < self.ny)
        return l * self.plane + jj[ok] * self.nx + ii[ok]

    def occupancy(self, paths: list[list[int]], own: set[int]) -> tuple[np.ndarray, np.ndarray]:
        t_cells, v_cells = [], []
        for path in paths:
            for a, b in zip(path, path[1:]):
                if b in own and a // self.plane == b // self.plane:
                    continue
                la, ra = divmod(a, self.plane)
                lb, rb = divmod(b, self.plane)
                ja, ia = divmod(ra, self.nx)
                jb, ib = divmod(rb, self.nx)
                if la != lb:
                    for l in (0, 1):
                        t_cells.append(self._disk(l, ia, ja, R_T_VIA))
                        v_cells.append(self._disk(l, ia, ja, R_V_VIA))
                else:
                    t_cells.append(self._disk(la, ib, jb, R_T_TRACK))
                    v_cells.append(self._disk(la, ib, jb, R_V_TRACK))
            if path and path[0] not in own:
                l0, r0 = divmod(path[0], self.plane)
                j0, i0 = divmod(r0, self.nx)
                t_cells.append(self._disk(l0, i0, j0, R_T_TRACK))
                v_cells.append(self._disk(l0, i0, j0, R_V_TRACK))
        t = np.unique(np.concatenate(t_cells)) if t_cells else np.zeros(0, np.int64)
        v = np.unique(np.concatenate(v_cells)) if v_cells else np.zeros(0, np.int64)
        return t, v

    def occupancy_items(self, items: list[Shape], own: set[int]) -> tuple[np.ndarray, np.ndarray]:
        """Occupancy of final (pulled) geometry: segments sampled at half a cell."""
        g = self.g
        t_cells, v_cells = [], []
        for s in items:
            (x0, y0), (x1, y1) = s.seg
            if s.kind == "via":
                i, j = g.cell(x0, y0)
                for l in (0, 1):
                    t_cells.append(self._disk(l, i, j, R_T_VIA))
                    v_cells.append(self._disk(l, i, j, R_V_VIA))
                continue
            l = LAYERS.index(next(iter(s.layers)))
            n = int(math.hypot(x1 - x0, y1 - y0) / (STEP / 2)) + 1
            for t in np.linspace(0, 1, n + 1):
                i, j = g.cell(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t)
                if l * self.plane + j * self.nx + i in own:
                    continue
                t_cells.append(self._disk(l, i, j, R_T_TRACK))
                v_cells.append(self._disk(l, i, j, R_V_TRACK))
        t = np.unique(np.concatenate(t_cells)) if t_cells else np.zeros(0, np.int64)
        v = np.unique(np.concatenate(v_cells)) if v_cells else np.zeros(0, np.int64)
        return t, v

    def add(self, net: str, sign: int) -> None:
        t, v = self.occ.get(net, (np.zeros(0, np.int64), np.zeros(0, np.int64)))
        self.count_t.reshape(-1)[t] += sign
        self.count_v.reshape(-1)[v] += sign

    # -- search ----------------------------------------------------------

    def route_net(self, net: str, comps: list[list[Shape]], pres: float) -> list[list[int]] | None:
        g = self.g
        k = g.nid(net)
        ok_t = np.stack([np.isin(g.track[l], (-1, k)) for l in LAYERS])
        ok_v = np.isin(g.via[LAYERS[0]], (-1, k)) & np.isin(g.via[LAYERS[1]], (-1, k)) & ok_t[0] & ok_t[1]
        mult = ((1.0 + self.hist) * (1.0 + pres * self.count_t)).reshape(-1)
        vmult = (1.0 + pres * (self.count_v[0] + self.count_v[1])).reshape(-1)
        okt = ok_t.reshape(-1).tolist()
        okv = ok_v.reshape(-1).tolist()
        mult = mult.tolist()
        vmult = vmult.tolist()
        nx, plane = self.nx, self.plane
        via_base = VIA_COST / STEP

        def cells_of(comp) -> set[int]:
            return {l * plane + j * nx + i for l, i, j in seed_cells(g, comp, k)}

        comp_cells = [cells_of(c) for c in comps]
        if any(not c for c in comp_cells):
            return None
        order = sorted(range(len(comps)), key=lambda x: -len(comp_cells[x]))
        tree = set(comp_cells[order[0]])
        remaining = {x: comp_cells[x] for x in order[1:]}
        paths: list[list[int]] = []
        moves = [(1, 0, 1.0), (-1, 0, 1.0), (0, 1, 1.0), (0, -1, 1.0),
                 (1, 1, 1.4142), (1, -1, 1.4142), (-1, 1, 1.4142), (-1, -1, 1.4142)]
        while remaining:
            goal_owner = {}
            for x, cs in remaining.items():
                for c in cs:
                    goal_owner[c] = x
            gi = np.array([c % plane % nx for c in goal_owner])
            gj = np.array([c % plane // nx for c in goal_owner])
            gb = (gi.min(), gj.min(), gi.max(), gj.max())

            def h(i, j):
                dx = gb[0] - i if i < gb[0] else (i - gb[2] if i > gb[2] else 0)
                dy = gb[1] - j if j < gb[1] else (j - gb[3] if j > gb[3] else 0)
                return math.sqrt(dx * dx + dy * dy)

            best = {}
            prev = {}
            heap = []
            for c in tree:
                if okt[c]:
                    best[c] = 0.0
                    r = c % plane
                    heap.append((h(r % nx, r // nx), 0.0, c))
            heapq.heapify(heap)
            found = None
            pops = 0
            while heap:
                f, gc, c = heapq.heappop(heap)
                if gc > best.get(c, 1e18):
                    continue
                if c in goal_owner:
                    found = c
                    break
                pops += 1
                if pops > 2_000_000:
                    break
                l, r = divmod(c, plane)
                j, i = divmod(r, nx)
                for di, dj, w in moves:
                    ni, nj = i + di, j + dj
                    if ni < 0 or nj < 0 or ni >= nx or nj >= self.ny:
                        continue
                    n = l * plane + nj * nx + ni
                    if not okt[n]:
                        continue
                    ng = gc + w * mult[n]
                    if ng < best.get(n, 1e18):
                        best[n] = ng
                        prev[n] = c
                        heapq.heappush(heap, (ng + h(ni, nj), ng, n))
                if okv[r]:
                    n = (1 - l) * plane + r
                    ng = gc + via_base * vmult[r] + mult[n]
                    if ng < best.get(n, 1e18):
                        best[n] = ng
                        prev[n] = c
                        heapq.heappush(heap, (ng + h(i, j), ng, n))
            if found is None:
                return None
            path = [found]
            while path[-1] in prev:
                path.append(prev[path[-1]])
            path.reverse()
            paths.append(path)
            x = goal_owner[found]
            tree |= remaining.pop(x)
            tree |= set(path)
        return paths

    def own_cells(self, net: str, fixed_comps: list[list[Shape]]) -> set[int]:
        k = self.g.nid(net)
        return {l * self.plane + j * self.nx + i for cp in fixed_comps for l, i, j in seed_cells(self.g, cp, k)}

    def sample_cells(self, items: list[Shape], own: set[int]) -> tuple[list[int], list[int]]:
        """Centreline cells of track items and via cells (both layers), outside own copper."""
        g = self.g
        ct, cv = [], []
        for s in items:
            (x0, y0), (x1, y1) = s.seg
            if s.kind == "via":
                i, j = g.cell(x0, y0)
                for l in (0, 1):
                    c = l * self.plane + j * self.nx + i
                    cv.append(c)
                    ct.append(c)
                continue
            l = LAYERS.index(next(iter(s.layers)))
            n = int(math.hypot(x1 - x0, y1 - y0) / (STEP / 2)) + 1
            for t in np.linspace(0, 1, n + 1):
                i, j = g.cell(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t)
                c = l * self.plane + j * self.nx + i
                if c not in own:
                    ct.append(c)
        return ct, cv

    def occupancy_exact(self, items: list[Shape]) -> tuple[np.ndarray, np.ndarray]:
        """Clearance claim of warm-start copper, from exact distances (as the hard grid)."""
        g = self.g
        t_cells, v_cells = [], []
        for s in items:
            win = g._window(s.bbox(CLEAR + VIA_D / 2))
            i0, i1, j0, j1 = win
            if i0 >= i1 or j0 >= j1:
                continue
            gx, gy = np.meshgrid(g.xs[i0:i1], g.ys[j0:j1])
            d = s.dist(gx, gy)
            jj, ii = np.nonzero(d < CLEAR + TRACK_W / 2 + MARGIN)
            jv, iv = np.nonzero(d < CLEAR + VIA_D / 2)
            for l in (LAYERS.index(x) for x in s.layers):
                t_cells.append(l * self.plane + (j0 + jj) * self.nx + (i0 + ii))
                v_cells.append(l * self.plane + (j0 + jv) * self.nx + (i0 + iv))
        t = np.unique(np.concatenate(t_cells)) if t_cells else np.zeros(0, np.int64)
        v = np.unique(np.concatenate(v_cells)) if v_cells else np.zeros(0, np.int64)
        return t, v

    def refresh(self, net: str) -> None:
        """Recompute a net's occupancy and centre cells from its FR items and grid paths."""
        own = self.own[net]
        st = self.state[net]
        t1, v1 = self.occupancy_exact(st["fr"])
        t2, v2 = self.occupancy(st["paths"], own)
        self.occ[net] = (np.union1d(t1, t2), np.union1d(v1, v2))
        # Warm-start copper is DRC-clean against other warm-start copper, so
        # only grid-routed centrelines are checked; a clash with warm-start
        # copper flags its net through fr_hits().
        self.fr_occ[net] = t1
        ct, cv = [], []
        for path in st["paths"]:
            for a, b in zip(path, path[1:]):
                if a // self.plane != b // self.plane:
                    r = a % self.plane
                    cv += [r, self.plane + r]
            ct += [c for c in path if c not in own]
        self.center[net] = (np.unique(np.array(ct, np.int64)), np.unique(np.array(cv, np.int64)))

    def fr_hits(self, bad: dict[str, int]) -> set[str]:
        """Warm-start nets whose clearance a conflicted grid path enters."""
        hot = set()
        for net in bad:
            ct, _ = self.center[net]
            hot |= set(ct[self.count_t.reshape(-1)[ct] > 1].tolist())
        out = set()
        for net, occ in self.fr_occ.items():
            if occ.size and hot & set(occ.tolist()):
                out.add(net)
        return out

    def conflicts(self, net: str) -> int:
        """Centre/via cells of this net inside another net's clearance (own adds exactly 1)."""
        ct, cv = self.center[net]
        return int(np.count_nonzero(self.count_t.reshape(-1)[ct] > 1) + np.count_nonzero(self.count_v.reshape(-1)[cv] > 1))

    def mark_history(self, net: str, amount: float) -> None:
        ct, _ = self.center[net]
        hot = ct[self.count_t.reshape(-1)[ct] > 1]
        self.hist.reshape(-1)[hot] += amount


def to_items(router: Router, net: str, paths: list[list[int]]) -> list[Shape]:
    g = router.g
    plane, nx = router.plane, router.nx
    k = g.nid(net)
    out: list[Shape] = []
    for path in paths:
        runs = [[path[0]]]
        for a, b in zip(path, path[1:]):
            if a // plane != b // plane:
                r = b % plane
                at = g.pos(r % nx, r // nx)
                out.append(Shape(net, set(LAYERS), seg=(at, at), r=VIA_D / 2, uid=str(uuid.uuid4()), kind="via"))
                runs.append([b])
            else:
                runs[-1].append(b)
        for run in runs:
            if len(run) < 2:
                continue
            l = run[0] // plane
            own = np.zeros(plane, bool)
            own_idx = np.fromiter((c - l * plane for c in router.own[net] if c // plane == l), np.int64)
            own[own_idx] = True
            ok = np.isin(g.track[LAYERS[l]], (-1, k)) & ((router.count_t[l] == 0) | own.reshape(router.ny, nx))
            cells = [((c % plane) % nx, (c % plane) // nx) for c in run]
            pts = [0]
            i = 0
            while i < len(cells) - 1:
                j = len(cells) - 1
                while j > i + 1 and not line_ok(ok, cells[i], cells[j]):
                    j -= 1
                pts.append(j)
                i = j
            for a, b in zip(pts, pts[1:]):
                out.append(Shape(net, {LAYERS[l]}, seg=(g.pos(*cells[a]), g.pos(*cells[b])), r=TRACK_W / 2,
                                 uid=str(uuid.uuid4()), kind="track"))
    return out


def line_ok(ok, a, b) -> bool:
    (i0, j0), (i1, j1) = a, b
    n = int(max(abs(i1 - i0), abs(j1 - j0)) * 2) + 1
    for t in np.linspace(0, 1, n + 1):
        i, j = i0 + (i1 - i0) * t, j0 + (j1 - j0) * t
        for ii in {math.floor(i), math.ceil(i)}:
            for jj in {math.floor(j), math.ceil(j)}:
                if not ok[jj, ii]:
                    return False
    return True


def dump_conflicts(router: Router, bad: dict[str, int], path: Path) -> None:
    import json
    sets = {n: set(o[0].tolist()) for n, o in router.occ.items()}
    out = []
    for net in bad:
        ct, _ = router.center[net]
        for c in ct[router.count_t.reshape(-1)[ct] > 1].tolist():
            others = [m for m, s in sets.items() if m != net and c in s]
            l, r = divmod(c, router.plane)
            x, y = router.g.pos(r % router.nx, r // router.nx)
            out.append({"net": net, "layer": LAYERS[l], "x": x, "y": y, "others": others})
    path.write_text(json.dumps(out))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pcb", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--rounds", type=int, default=40)
    ap.add_argument("--fresh", action="store_true", help="drop every unlocked item first (no warm start)")
    ap.add_argument("--drop-drc", type=Path, help="DRC json: drop unlocked items named in clearance errors")
    ap.add_argument("--debug", type=Path, help="write the last round's conflict cells here (json)")
    ap.add_argument("--skip", nargs="*", default=[], help="nets not routed here (e.g. GND, left to pours)")
    ap.add_argument("--rip-near", type=Path,
                    help="a previous run's --debug json: rip up every net with unlocked copper within --radius "
                         "of a conflict cell and re-route those together (a knot needs a third net to move)")
    ap.add_argument("--radius", type=float, default=1.0)
    ap.add_argument("--all-after", type=int, default=0,
                    help="from this round on, rip up and re-route every live net each round (PathFinder proper), "
                         "not only the nets in conflict; slower, but a conflict can then be solved by a third net moving")
    args = ap.parse_args()
    text = args.pcb.read_text(encoding="utf-8")
    drop: set[str] = set()
    if args.drop_drc:
        import json
        for v in json.loads(args.drop_drc.read_text()).get("violations", []):
            if v["severity"] == "error" and v["type"] in ("clearance", "shorting_items", "tracks_crossing",
                                                          "hole_clearance", "copper_edge_clearance"):
                drop |= {i["uuid"] for i in v["items"] if i["description"].startswith(("Track", "Via"))}
    ripnets: set[str] = set()
    if args.rip_near:
        import json
        cells = json.loads(args.rip_near.read_text())
        pre_shapes, _, _, _ = parse_board(text)
        cx = np.array([c["x"] for c in cells]); cy = np.array([c["y"] for c in cells])
        for s in pre_shapes:
            if s.kind == "pad" or s.locked or not s.net or s.net in args.skip:
                continue
            (x0, y0), (x1, y1) = s.seg
            n = max(2, int(math.hypot(x1 - x0, y1 - y0) / 0.1) + 1)
            px, py = np.linspace(x0, x1, n), np.linspace(y0, y1, n)
            d = np.hypot(px[:, None] - cx[None, :], py[:, None] - cy[None, :]).min()
            if d <= args.radius:
                ripnets.add(s.net)
        print("rip-near:", len(cells), "conflict cells;", len(ripnets), "nets ripped:", " ".join(sorted(ripnets)), flush=True)
    for kind in ("segment", "via"):
        for b in blocks(text, kind):
            if "(locked yes)" not in b and (args.fresh or sval(b, "uuid") in drop or sval(b, "net") in args.skip
                                           or sval(b, "net") in ripnets):
                text = text.replace(f"\n\t({kind}{b}", "", 1)
    shapes, holes, edges, zones = parse_board(text)
    fixed = [s for s in shapes if s.kind == "pad" or s.locked]
    grid = Grid(fixed, holes, edges, zones)
    router = Router(grid)
    nets = sorted({s.net for s in shapes if s.net and not s.net.startswith("unconnected")})
    fixed_comps, fr_items = {}, {}
    for net in nets:
        fixed_comps[net] = components(fixed, net)
        fr_items[net] = [s for s in shapes if s.net == net and not s.locked and s.kind != "pad"]
        router.own[net] = router.own_cells(net, fixed_comps[net])
        router.state[net] = {"fr": fr_items[net], "paths": []}
    live = [n for n in nets if (len(fixed_comps[n]) > 1 or fr_items[n]) and n not in args.skip]
    for net in live:
        router.refresh(net)
        router.add(net, +1)

    def span(net):
        pts = [s.center() for cp in fixed_comps[net] for s in cp]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        return (max(xs) - min(xs)) + (max(ys) - min(ys))

    # Round 0 routes only what the warm start leaves open, keeping its copper.
    missing = {}
    for net in live:
        comps = components(fixed + router.state[net]["fr"], net)
        if len(comps) > 1:
            missing[net] = comps
    print(len(missing), "nets with open connections:", " ".join(sorted(missing)), flush=True)
    pres, hist_step = 0.5, 0.3
    failed: set[str] = set()
    ripped: set[str] = set()
    bad: dict[str, int] = {}
    dirty = sorted(missing, key=span)
    for rnd in range(args.rounds):
        t0 = time.time()
        for net in dirty:
            router.add(net, -1)
            if rnd == 0:
                comps = missing[net]
            else:
                router.state[net]["fr"] = []
                ripped.add(net)
                comps = fixed_comps[net]
            paths = router.route_net(net, comps, pres)
            if paths is None:
                failed.add(net)
                paths = []
            else:
                failed.discard(net)
            router.state[net]["paths"] = paths
            router.refresh(net)
            router.add(net, +1)
        bad = {n: router.conflicts(n) for n in live}
        bad = {n: c for n, c in bad.items() if c}
        for n in router.fr_hits(bad):
            bad.setdefault(n, 1)
        print(f"round {rnd}: pres {pres:.2f}, {len(bad)} nets in conflict ({sum(bad.values())} cells) "
              f"{sorted(bad)[:12]}, failed {sorted(failed)}, {time.time() - t0:.1f} s", flush=True)
        if (not bad and not failed) or rnd == args.rounds - 1:
            break
        for net in bad:
            router.mark_history(net, hist_step)
        dirty = sorted(set(bad) | failed, key=span)
        if args.all_after and rnd + 1 >= args.all_after:
            dirty = sorted(live, key=span)
        pres *= 1.3
    if args.debug:
        dump_conflicts(router, bad, args.debug)
    drop_uids = {s.uid for n in ripped for s in fr_items[n]}
    for kind in ("segment", "via"):
        for b in blocks(text, kind):
            if sval(b, "uuid") in drop_uids:
                text = text.replace(f"\n\t({kind}{b}", "", 1)
    added: list[Shape] = []
    for net in sorted(live, key=span):
        if not router.state[net]["paths"]:
            continue
        router.add(net, -1)
        items = to_items(router, net, router.state[net]["paths"])
        added += items
        own = router.own[net]
        t1, v1 = router.occupancy_items(router.state[net]["fr"] + items, own)
        router.occ[net] = (t1, v1)
        router.add(net, +1)
    body = text.rstrip()
    out = body[:-1] + "".join(seg_text(s) for s in added) + ")\n"
    args.out.write_text(out, encoding="utf-8")
    print("wrote", args.out, "items", len(added), "ripped", len(ripped), "failed", sorted(failed),
          "conflicted", sorted(bad))
    return 0 if not bad and not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
