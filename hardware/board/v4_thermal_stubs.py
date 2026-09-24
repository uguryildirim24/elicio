#!/usr/bin/env python3
"""Give every starved-thermal pad of a DRC report a second physical connection (design note §9.3):
a straight 0.10 track from inside the pad, through the thermal gap, into the same-layer pour of its
net (fill cells >= 0.20 from the pad copper), clear on the finisher's track grid.

  .venv/bin/python hardware/board/v4_thermal_stubs.py PCB DRC.json OUT [maxlen]
"""
import sys, math, uuid, json, re
import numpy as np
from v4_route_fix import parse_board, Grid, LAYERS, STEP, TRACK_W, clear_line, Shape, seg_text
from v4_tables import footprints
pcb, drc, out = sys.argv[1], sys.argv[2], sys.argv[3]
maxlen = float(sys.argv[4]) if len(sys.argv) > 4 else 0.8
text = open(pcb).read()
d = json.load(open(drc))
starved = []
for v in d['violations']:
    if v['type'] == 'starved_thermal':
        m = re.match(r'Pad (\S+) \[(\S+)\] of (\S+) on (\S+)', v['items'][1]['description'])
        starved.append((m.group(3), m.group(1), m.group(2), m.group(4)))
shapes, holes, edges, zones = parse_board(text)
grid = Grid(shapes, holes, edges, zones)
pads = {}
for f in footprints(text):
    for pnum, kind, ax, ay, n in f['pads']:
        pads[(round(ax, 3), round(ay, 3))] = f"{f['ref']}.{pnum}"
byname = {}
for s in shapes:
    if s.kind == 'pad':
        cx, cy = s.center()
        byname.setdefault(pads.get((round(cx, 3), round(cy, 3))), []).append(s)
def cells_of(members, l, window, ok):
    i0, i1, j0, j1 = window
    outc = []
    gx, gy = np.meshgrid(grid.xs[i0:i1], grid.ys[j0:j1])
    for m in members:
        if l not in m.layers: continue
        inside = (m.dist(gx, gy) <= 1e-9) & ok[j0:j1, i0:i1]
        for jj, ii in zip(*np.nonzero(inside)): outc.append((i0 + ii, j0 + jj))
    return outc
added = []
for ref, pn, net, layer in starved:
    k = grid.nid(net)
    ok = np.isin(grid.track[layer], (-1, k))
    pad = [s for s in byname.get(f'{ref}.{pn}', []) if layer in s.layers]
    fills = [s for s in shapes if s.kind == 'fill' and s.net == net and layer in s.layers]
    if not pad:
        print(f'{ref}.{pn}: pad not found'); continue
    b = pad[0].bbox(maxlen)
    win = grid._window(b)
    a_cells = cells_of(pad, layer, win, ok)
    # Pour proper only: fill cells at least 0.20 from the pad copper (beyond the 0.15 thermal gap and its spoke).
    m_cells = [c for c in cells_of(fills, layer, win, ok)
               if float(pad[0].dist(np.array([grid.pos(*c)[0]]), np.array([grid.pos(*c)[1]]))[0]) >= 0.20]
    best = None
    pairs = sorted(((math.hypot(a[0] - m[0], a[1] - m[1]) * STEP, a, m) for a in a_cells for m in m_cells))
    for dist, a, m in pairs:
        if dist > maxlen: break
        if clear_line(ok, a, m):
            best = (dist, a, m); break
    if best is None:
        print(f'{ref}.{pn} {layer}: NO STUB within {maxlen} mm ({len(a_cells)} pad cells, {len(m_cells)} fill cells)')
        continue
    dist, a, m = best
    s = Shape(net, {layer}, seg=(grid.pos(*a), grid.pos(*m)), r=TRACK_W / 2, uid=str(uuid.uuid4()), kind='track')
    grid.stamp(s); added.append(s)
    print(f'{ref}.{pn} {layer}: stub ({grid.pos(*a)[0]:.3f}, {grid.pos(*a)[1]:.3f}) -> ({grid.pos(*m)[0]:.3f}, {grid.pos(*m)[1]:.3f}) {dist:.3f} mm')
body = text.rstrip(); assert body.endswith(')')
open(out, 'w').write(body[:-1] + ''.join(seg_text(s) for s in added) + ')\n')
print('added', len(added), 'of', len(starved), '->', out)
