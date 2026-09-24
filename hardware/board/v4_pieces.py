#!/usr/bin/env python3
"""List every unjoined piece of NET with its members and its gap in mm to the biggest piece,
per layer (design note §9; the honest list when GND will not close).

  .venv/bin/python hardware/board/v4_pieces.py PCB NET
"""
import sys, math
sys.path.insert(0, '/home/user/projects/elicio/.worktrees/t-0014/hardware/board')
import numpy as np
from v4_route_fix import parse_board, components
from v4_tables import footprints
pcb, net = sys.argv[1], sys.argv[2]
text = open(pcb).read()
shapes, holes, edges, zones = parse_board(text)
pads = {}
for f in footprints(text):
    for pnum, kind, ax, ay, n in f['pads']:
        pads[(round(ax, 3), round(ay, 3))] = f"{f['ref']}.{pnum}"
comps = sorted(components(shapes, net), key=len, reverse=True)
main = comps[0]
def samples(s):
    if s.poly is not None:
        return s.edges[:, 0], s.edges[:, 1], 0.0
    if s.seg is not None:
        (x0, y0), (x1, y1) = s.seg
        n = max(2, int(math.hypot(x1 - x0, y1 - y0) / 0.02) + 1)
        return np.linspace(x0, x1, n), np.linspace(y0, y1, n), s.r
    cx, cy, hw, hh, ang = s.box
    c, sn = math.cos(ang), math.sin(ang)
    xs, ys = [], []
    for lx in np.linspace(-hw, hw, 9):
        for ly in np.linspace(-hh, hh, 9):
            xs.append(cx + lx * c + ly * sn); ys.append(cy - lx * sn + ly * c)
    return np.array(xs), np.array(ys), 0.0
def describe(c):
    out = []
    for s in c:
        cx, cy = s.center()
        if s.kind == 'pad':
            out.append(pads.get((round(cx, 3), round(cy, 3)), f'pad@({cx:.2f},{cy:.2f})') + '/' + '+'.join(sorted(l[0] for l in s.layers)))
        elif s.kind == 'fill':
            b = s.bbox(0)
            out.append(f"fill{'/'.join(sorted(l[0] for l in s.layers))}[{b[0]:.2f}-{b[2]:.2f},{b[1]:.2f}-{b[3]:.2f}]")
        elif s.kind == 'via':
            out.append(f'via({cx:.3f},{cy:.3f})')
        else:
            (x0, y0), (x1, y1) = s.seg
            out.append(f"trk{s.layers.pop()[0]}({x0:.3f},{y0:.3f})-({x1:.3f},{y1:.3f})" + ('L' if s.locked else ''))
    return out
print(f'{net}: {len(comps)} pieces; main has {len(main)} members')
for ci, c in enumerate(comps[1:], 1):
    best = {}
    for s in c:
        xs, ys, r = samples(s)
        for m in main:
            if not (m.layers & s.layers):
                continue
            d = float(np.min(m.dist(xs, ys))) - r
            lay = '+'.join(sorted(l[0] for l in (m.layers & s.layers)))
            if d < best.get(lay, (9e9,))[0]:
                mc = m.center()
                best[lay] = (round(max(d, 0), 3), pads.get((round(mc[0], 3), round(mc[1], 3)), m.kind), (round(mc[0], 2), round(mc[1], 2)))
    print(f'piece {ci} ({len(c)}): ' + ', '.join(describe(c)[:8]) + (' ...' if len(c) > 8 else ''))
    print('     gap to main per layer:', best)
