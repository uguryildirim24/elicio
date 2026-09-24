#!/usr/bin/env python3
"""Join the pieces of one net by hand-style stitching (design note §9.1): a via where two pieces
overlap through the board (free on the finisher's via grid on both layers, ring >= 0.05 mm into
copper of both pieces) or a straight 0.10 track (<= maxlen mm, clear on the track grid). Greedy:
applies the best candidate, stamps it, merges, repeats; writes OUT and lists what is still open.

Unlike the routers, a stitching via may sit inside an own-net pad: fully inside a big one (an
exposed or mounting pad, 0.20 mm in from its edge; U2's exposed pad is the bridge between the
top-side GND island under U2 and the GND pads below it) or touching a small pad's edge with its
hole 0.05 mm outside the copper. It never enters another net's pad.

  .venv/bin/python hardware/board/v4_stitch.py PCB NET OUT [maxlen]
"""
import sys, math, uuid
sys.path.insert(0, '/home/user/projects/elicio/.worktrees/t-0014/hardware/board')
import numpy as np
from v4_route_fix import parse_board, Grid, components, LAYERS, STEP, VIA_D, TRACK_W, clear_line, Shape, seg_text
import v4_route_fix
from v4_tables import footprints
pcb, net, out = sys.argv[1], sys.argv[2], sys.argv[3]
maxlen = float(sys.argv[4]) if len(sys.argv) > 4 else 1.5
text = open(pcb).read()
shapes, holes, edges, zones = parse_board(text)
v4_route_fix.VIA_IN_OWN_PAD = {net}
grid = Grid(shapes, holes, edges, zones)
k = grid.nid(net)
pads = {}
for f in footprints(text):
    for pnum, kind, ax, ay, n in f['pads']:
        pads[(round(ax, 3), round(ay, 3))] = f"{f['ref']}.{pnum}"
def name(s):
    cx, cy = s.center()
    if s.kind == 'pad': return pads.get((round(cx, 3), round(cy, 3)), 'pad')
    if s.kind == 'fill':
        b = s.bbox(0); return f"fill{''.join(sorted(l[0] for l in s.layers))}({(b[0]+b[2])/2:.1f},{(b[1]+b[3])/2:.1f})"
    return s.kind
comps = sorted(components(shapes, net), key=len, reverse=True)
owner = list(range(len(comps)))
def find(i):
    while owner[i] != i: owner[i] = owner[owner[i]]; i = owner[i]
    return i
def label(ci):
    c = comps[ci]
    return ', '.join(name(m) for m in c if m.kind == 'pad')[:60] or name(c[0])
INTRUDE = 0.05
def touch(members, l, x, y):
    best = None
    for m in members:
        if l not in m.layers: continue
        d = float(m.dist(np.array([x]), np.array([y]))[0])
        if d <= VIA_D / 2 - INTRUDE and (best is None or d < best[0]): best = (d, m)
    return best
def bbox_of(c):
    b = [9e9, 9e9, -9e9, -9e9]
    for m in c:
        bb = m.bbox(0); b = [min(b[0], bb[0]), min(b[1], bb[1]), max(b[2], bb[2]), max(b[3], bb[3])]
    return b
def cells_of(members, l, window):
    i0, i1, j0, j1 = window
    out = []
    gx, gy = np.meshgrid(grid.xs[i0:i1], grid.ys[j0:j1])
    ok = np.isin(grid.track[l][j0:j1, i0:i1], (-1, k))
    x0, y0 = grid.pos(i0, j0); x1, y1 = grid.pos(i1, j1)
    for m in members:
        if l not in m.layers: continue
        bb = m.bbox(0)
        if bb[2] < x0 or bb[0] > x1 or bb[3] < y0 or bb[1] > y1: continue
        inside = (m.dist(gx, gy) <= 1e-9) & ok
        for jj, ii in zip(*np.nonzero(inside)): out.append((i0 + ii, j0 + jj))
    return out
def masks(members, win):
    """Per layer over the window: cells whose via ring reaches >= INTRUDE into the piece's copper,
    and the distance to the nearest member there."""
    i0, i1, j0, j1 = win
    x0, y0 = grid.pos(i0, j0); x1, y1 = grid.pos(i1, j1)
    gx, gy = np.meshgrid(grid.xs[i0:i1], grid.ys[j0:j1])
    out = {}
    for l in LAYERS:
        hit = np.zeros(gx.shape, bool)
        dmin = np.full(gx.shape, 9e9)
        for m in members:
            if l not in m.layers: continue
            bb = m.bbox(VIA_D)
            if bb[2] < x0 or bb[0] > x1 or bb[3] < y0 or bb[1] > y1: continue
            d = m.dist(gx, gy)
            hit |= d <= VIA_D / 2 - INTRUDE
            dmin = np.minimum(dmin, d)
        out[l] = (hit, dmin)
    return out
def candidates(ci):
    """Best via and best track joining piece ci to any other piece (by current owner)."""
    c = comps[ci]
    b = bbox_of(c)
    win = grid._window((b[0] - maxlen, b[1] - maxlen, b[2] + maxlen, b[3] + maxlen))
    i0, i1, j0, j1 = win
    via_ok = np.isin(grid.via['F.Cu'], (-1, k)) & np.isin(grid.via['B.Cu'], (-1, k))
    best_via = None
    others = [(cj, comps[cj]) for cj in range(len(comps)) if find(cj) != find(ci)]
    # pre-filter other pieces by bbox overlap with the window
    ob = []
    for cj, oc in others:
        bb = bbox_of(oc)
        if bb[2] < b[0] - maxlen or bb[0] > b[2] + maxlen or bb[3] < b[1] - maxlen or bb[1] > b[3] + maxlen: continue
        ob.append((cj, oc))
    mc = masks(c, win)
    reach = (mc['F.Cu'][0] | mc['B.Cu'][0]) & via_ok[j0:j1, i0:i1]
    if reach.any():
        for cj, oc in ob:
            mo = masks(oc, win)
            for lm in LAYERS:
                both = reach & mo[lm][0]
                for jj, ii in zip(*np.nonzero(both)):
                    i, j = i0 + ii, j0 + jj
                    x, y = grid.pos(i, j)
                    r = 0
                    for rr in range(1, 4):
                        good = all(via_ok[j + dj, i + di] for di in range(-rr, rr + 1) for dj in range(-rr, rr + 1)
                                   if di * di + dj * dj <= rr * rr and 0 <= i + di < grid.nx and 0 <= j + dj < grid.ny)
                        if not good: break
                        r = rr
                    dc = min(float(mc[l][1][jj, ii]) for l in LAYERS if mc[l][0][jj, ii])
                    score = (r, -dc - float(mo[lm][1][jj, ii]))
                    if best_via is None or score > best_via[0]:
                        best_via = (score, x, y, cj, [l[0] for l in LAYERS if mc[l][0][jj, ii]], lm[0])
    best_trk = None
    for l in LAYERS:
        a_cells = cells_of(c, l, win)[::2]
        if not a_cells: continue
        ok = np.isin(grid.track[l], (-1, k))
        A = np.array(a_cells, float)
        for cj, oc in ob:
            m_cells = cells_of(oc, l, win)[::2]
            if not m_cells: continue
            M = np.array(m_cells, float)
            # nearest pairs by array arithmetic, then the straight-line test on the closest few hundred
            d2 = ((A[:, None, 0] - M[None, :, 0]) ** 2 + (A[:, None, 1] - M[None, :, 1]) ** 2).ravel()
            n = min(400, d2.size)
            idx = np.argpartition(d2, n - 1)[:n]
            for f in idx[np.argsort(d2[idx])]:
                d = math.sqrt(float(d2[f])) * STEP
                if d > maxlen or (best_trk and d >= best_trk[0]): break
                if d < 0.05: continue  # coincident cells are a false split, not a join
                a, m = a_cells[f // len(m_cells)], m_cells[f % len(m_cells)]
                if clear_line(ok, a, m):
                    best_trk = (d, l, grid.pos(*a), grid.pos(*m), cj)
                    break
    return best_via, best_trk
added = []
progress = True
while progress:
    progress = False
    roots = sorted({find(i) for i in range(len(comps))}, key=lambda r: -len(comps[r]))
    main_root = roots[0]
    for r in roots[1:]:
        members_idx = [i for i in range(len(comps)) if find(i) == r]
        best = None
        for ci in members_idx:
            bv, bt = candidates(ci)
            if bv and (best is None or best[0] == 'trk' or bv[0] > best[1][0]): best = ('via', bv)
            if bt and best is None: best = ('trk', bt)
        if not best: continue
        if best[0] == 'via':
            (score, x, y, cj, lp, lm) = best[1]
            s = Shape(net, set(LAYERS), seg=((x, y), (x, y)), r=VIA_D / 2, uid=str(uuid.uuid4()), kind='via')
            print(f'via ({x:.3f}, {y:.3f}) margin {score[0]*STEP:.3f}: [{label(members_idx[0])}] {lp} <-> [{label(cj)}] {lm}')
        else:
            (d, l, a, b, cj) = best[1]
            s = Shape(net, {l}, seg=(a, b), r=TRACK_W / 2, uid=str(uuid.uuid4()), kind='track')
            print(f'track {l} {a} -> {b} {d:.3f} mm: [{label(members_idx[0])}] <-> [{label(cj)}]')
        grid.stamp(s); added.append(s); comps[r].append(s)
        owner[find(cj)] = find(r)
        progress = True
        break
roots = sorted({find(i) for i in range(len(comps))}, key=lambda r: -len(comps[r]))
print('added', len(added), 'still open pieces:', len(roots) - 1)
for r in roots[1:]:
    print('   OPEN', label(r), [round(v, 2) for v in bbox_of(comps[r])])
body = text.rstrip(); assert body.endswith(')')
open(out, 'w').write(body[:-1] + ''.join(seg_text(s) for s in added) + ')\n')
print('wrote', out)
