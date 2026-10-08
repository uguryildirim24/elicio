#!/usr/bin/env python3
"""Print the v4 flat PCB table, or the folded shell-site table (markdown).

Plain python: reads elicio-v4.kicad_pcb as text, no pcbnew. The flat table
is what the Gerber carries (PCB x, y = packing u, s). The folded table
(docs/fab/board-v4-design.md §10.2) maps every courtyard, ring, strip root
and tab root to the shell frame (u, s, y) and tests it against the v4
target body: the r9 shell (branch t-0001, 1f5c8e4) with the §7 changes on
paper. The body numbers below mirror build_v4.py and the design note.

Run: python3 hardware/board/v4_tables.py [--pads] [--folded] [--pcb PCB]
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PCB = HERE / "elicio-v4.kicad_pcb"

# Pads listed pad by pad (connectors, rings, test header).
PAD_REFS = ("P1", "P2", "P3", "P4", "P5", "J2", "J3", "J4", "SW1")

# --- v4 target body (design note §1.2, §4, §5.3, §7; shell r9 values) ---
CAVITY_U = (1.50, 16.50)       # W18 walls
FLOOR_Y, LID_Y = 1.50, 7.10
RIB_S = (14.90, 15.70)         # rib between the cell pocket and the bay
BAY_S = (RIB_S[1], 38.20)      # bay: rib face to the end wall
ISLAND = (2.25, 16.00, 15.75, 37.60)
PI_TOP, PI_BOTTOM, STIFF_BOTTOM = 5.12, 5.01, 4.81
LANDS = {"P1": (5.90, 22.00), "P2": (10.40, 33.10)}   # standoff tops under the island, R 3.2
LAND_R = 3.20
COLLAR_AF, COLLAR_R, COLLAR_TOP = 8.40, 4.85, 3.50     # EMG hex collars on the floor, flats facing ±u
POSTS = {"P1": (5.90, 23.00), "P2": (9.40, 32.10)}    # lid posts Ø2.0 onto the island's F side
POST_R = 1.00
P5_STANDOFF_END_U = 15.09 + 1.10 - 3.00                # 13.19: folded plate face 16.19, standoff 3.0
P5_WELL_S = (12.10 - 3.06, 12.10 + 3.06)               # AF 5.30 hex well, corner r 3.06
J2_WELL_GAP = 0.30
# Fold math (design note §4.4): joint bend from u 15.09, neutral R 1.155,
# folded plane at u 16.245, y = 3.905 + (16.904 - u_flat).
BEND_U0, BEND_U1, PLANE_U, PLANE_Y0 = 15.09, 16.904, 16.245, 3.905
STRIPS = {  # strip u span, island edge s, folded ring site (u, s), ring copper face y
    "SIG1": ((4.65, 7.15), 16.00, (5.90, 22.00), "floor 1.50-1.81 under the P1 standoff"),
    "SIG2": ((9.15, 11.65), 16.00, (10.40, 33.10), "floor 1.50-1.81 under the P2 standoff"),
    "REF": ((7.25, 9.75), 37.60, (8.50, 43.00), "floor 1.50-1.81 in the REF pocket"),
}
SIG_POCKET = ((14.40, 16.00), 3.50, 3.00)  # r9 fold pocket s span, width in u, height (packing-v2 decision 74)
REF_SLOT = ((7.05, 9.95), (38.20, 39.25), (1.50, 1.96))  # r9 end-wall slot with its clearances
J3_STUB_U, J3_NECK_S = (15.75, 16.20), (19.90, 22.40)
TAB_REFS = {"J3", "R31", "R32", "R33"}
RING_REFS = {"P1", "P2", "P3", "P4", "P5"}
# Part heights in mm above the board face (max). Sources: design note §1.2
# (U1, J2, SW1); TI outlines listed in §11.2 (U2 RSM 1.00, U4/U5 DQN 0.40,
# U3 YFP 0.63); package maxima otherwise (UNVERIFIED, no page read here).
HEIGHTS = {
    "U1": (1.00, "§1.2"), "U2": (1.00, "TI RSM"), "U3": (0.63, "TI YFP, UNVERIFIED"),
    "U4": (0.40, "TI DQN"), "U5": (0.40, "TI DQN"), "J2": (1.20, "§1.2 mated"), "SW1": (0.60, "§1.2"),
    "J4": (0.00, "pads only"), "D1": (0.50, "Nexperia SOD882 body 0.5"), "D2": (0.55, "0402 LED, UNVERIFIED"),
}
HEIGHT_BY_FP = {"SOT-883": (0.40, "DFN1006 max, UNVERIFIED"), "0201": (0.35, "0201 max, UNVERIFIED"),
                "R_0402": (0.45, "0402 R max, UNVERIFIED"), "C_0402": (0.60, "0402 C max, UNVERIFIED")}


def footprints(text: str) -> list[dict]:
    out = []
    for chunk in text.split("\n\t(footprint ")[1:]:
        name = chunk.split("\n", 1)[0].strip().strip('"')
        ref = re.search(r'\(property "Reference" "([^"]+)"', chunk).group(1)
        layer = re.search(r'\n\t\t\(layer "([^"]+)"\)', chunk).group(1)
        at = re.search(r"\n\t\t\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)", chunk)
        x, y, rot = float(at.group(1)), float(at.group(2)), float(at.group(3) or 0)
        pads = []
        for pad in re.finditer(r'\n\t\t\(pad "([^"]*)" (\w+) (\w+)\s+\(at ([-\d.]+) ([-\d.]+)', chunk):
            num, kind = pad.group(1), pad.group(2)
            px, py = float(pad.group(4)), float(pad.group(5))
            th = math.radians(rot)
            ax = x + px * math.cos(th) + py * math.sin(th)
            ay = y - px * math.sin(th) + py * math.cos(th)
            tail = chunk[pad.end(): pad.end() + 1500]
            net = re.search(r'\(net "([^"]*)"\)', tail.split("\n\t\t(pad ", 1)[0])
            pads.append((num, kind, round(ax, 3), round(ay, 3), net.group(1) if net else ""))
        out.append({"ref": ref, "fp": name, "side": "bottom" if layer == "B.Cu" else "top",
                    "x": x, "y": y, "rot": rot, "pads": pads})
    return sorted(out, key=lambda f: (re.sub(r"\d", "", f["ref"]), int(re.sub(r"\D", "", f["ref"]) or 0)))


def courtyards(text: str) -> dict[str, tuple[str, float, float, float, float]]:
    """ref -> (layer F/B, u0, s0, u1, s1): the courtyard's bounding box in board coordinates."""
    out = {}
    for chunk in text.split("\n\t(footprint ")[1:]:
        ref = re.search(r'\(property "Reference" "([^"]+)"', chunk).group(1)
        at = re.search(r"\n\t\t\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)", chunk)
        x, y, th = float(at.group(1)), float(at.group(2)), math.radians(float(at.group(3) or 0))
        pts: dict[str, list[tuple[float, float]]] = {}
        for m in re.finditer(r"\n\t\t\(fp_(rect|line|poly|circle)\s([\s\S]*?)\(layer \"([FB])\.CrtYd\"\)", chunk):
            kind, body, layer = m.group(1), m.group(2), m.group(3)
            local = [(float(a), float(b)) for a, b in re.findall(r"\((?:start|end|xy|center) ([-\d.]+) ([-\d.]+)\)", body)]
            if kind == "circle":
                (cx, cy), (ex, ey) = local[0], local[1]
                r = math.hypot(ex - cx, ey - cy)
                local = [(cx - r, cy - r), (cx + r, cy + r), (cx - r, cy + r), (cx + r, cy - r)]
            for px, py in local:
                pts.setdefault(layer, []).append((x + px * math.cos(th) + py * math.sin(th),
                                                  y - px * math.sin(th) + py * math.cos(th)))
        for layer, p in pts.items():
            us, ss = [q[0] for q in p], [q[1] for q in p]
            out[ref] = (layer, min(us), min(ss), max(us), max(ss))
    return out


def height(ref: str, fp: str) -> tuple[float, str]:
    if ref in HEIGHTS:
        return HEIGHTS[ref]
    for key, val in HEIGHT_BY_FP.items():
        if key in fp:
            return val
    return (0.0, "no height: UNVERIFIED")


def box_gap(box: tuple[float, float, float, float], cx: float, cy: float, r: float) -> float:
    """Gap between an axis-aligned box and a circle (negative = overlap)."""
    dx = max(box[0] - cx, 0.0, cx - box[2])
    dy = max(box[1] - cy, 0.0, cy - box[3])
    return math.hypot(dx, dy) - r


def collar_box(land: tuple[float, float]) -> tuple[float, float, float, float]:
    return (land[0] - COLLAR_AF / 2, land[1] - COLLAR_R, land[0] + COLLAR_AF / 2, land[1] + COLLAR_R)


def overlaps(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> bool:
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def folded(fps: list[dict], text: str) -> int:
    cy = courtyards(text)
    worst = 9.9
    print("#### Courtyards on the island (flat u, s = shell u, s; y from the fold math)")
    print()
    print("| ref | side | courtyard u | courtyard s | h (source) | y | wall u | rib/end s | lid or floor y | lid post | landing | test |")
    print("|---|---|---:|---:|---|---|---:|---:|---:|---:|---:|---|")
    for f in fps:
        ref = f["ref"]
        if ref in RING_REFS or ref not in cy:
            continue
        layer, u0, s0, u1, s1 = cy[ref]
        box = (u0, s0, u1, s1)
        h, src = height(ref, f["fp"])
        if ref in TAB_REFS:
            print(f"| {ref} | {f['side']} | {u0:.2f}-{u1:.2f} | {s0:.2f}-{s1:.2f} | {h:.2f} ({src}) | cut off with the tab (Q91) | - | - | - | - | - | exterior |")
            continue
        wall = min(u0 - CAVITY_U[0], CAVITY_U[1] - u1)
        along = min(s0 - BAY_S[0], BAY_S[1] - s1)
        if f["side"] == "top":
            y0, y1 = PI_TOP, PI_TOP + h
            ymargin = LID_Y - y1
            floor_name = "lid"
            post = min(box_gap(box, *POSTS[k], POST_R) for k in POSTS)
            post_txt = f"{post:.2f}" if post >= 0 else f"{post:.2f} (post on the part)"
            land_txt = "-"
        else:
            y1, y0 = PI_BOTTOM, PI_BOTTOM - h
            over_collar = any(overlaps(box, collar_box(LANDS[k])) for k in LANDS)
            base = COLLAR_TOP if over_collar else FLOOR_Y
            ymargin = y0 - base
            floor_name = "collar" if over_collar else "floor"
            post_txt = "-"
            land = min(box_gap(box, *LANDS[k], LAND_R) for k in LANDS)
            land_txt = f"{land:.2f}"
        m = min(wall, along, ymargin)
        ok = m >= 0 and (f["side"] != "top" or ref == "U1" or post >= 0)
        worst = min(worst, m)
        print(f"| {ref} | {f['side']} | {u0:.2f}-{u1:.2f} | {s0:.2f}-{s1:.2f} | {h:.2f} ({src}) | {y0:.2f}-{y1:.2f} | {wall:.2f} | {along:.2f} | {ymargin:.2f} ({floor_name}) | {post_txt} | {land_txt} | {'ok' if ok else 'FAIL'} |")
    print()
    print(f"Smallest courtyard margin: {worst:.2f} mm.")
    print()
    print("#### Rings, strip roots and tab roots")
    print()
    print("| item | flat (u, s) | folded site (u, s, y) | body feature | margin | test |")
    print("|---|---|---|---|---|---|")
    ring_flat = {f["ref"]: (f["x"], f["y"]) for f in fps if f["ref"] in RING_REFS}
    for net, (span, edge, site, face) in STRIPS.items():
        ref = {"SIG1": "P1", "SIG2": "P2", "REF": "P3"}[net]
        fx, fy = ring_flat[ref]
        print(f"| {ref} ring ({net}) | ({fx:.2f}, {fy:.2f}) | ({site[0]:.2f}, {site[1]:.2f}), {face} | "
              f"{'standoff R 3.2 landing under the island' if net != 'REF' else 'REF pocket Ø7.5'} | site as §4.5 | ok |")
        if net != "REF":
            pocket_u = (site[0] - SIG_POCKET[1] / 2, site[0] + SIG_POCKET[1] / 2)
            mu = min(span[0] - pocket_u[0], pocket_u[1] - span[1])
            print(f"| {net} root | u {span[0]:.2f}-{span[1]:.2f} at s {edge:.2f} | 180° fold R 1.5 under the island, stand-out to s {edge - 1.60:.2f}, drop {STIFF_BOTTOM - FLOOR_Y:.2f} | "
                  f"r9 fold pocket u {pocket_u[0]:.2f}-{pocket_u[1]:.2f} × s {SIG_POCKET[0][0]:.2f}-{SIG_POCKET[0][1]:.2f} × {SIG_POCKET[2]:.2f} tall (decision 74) | "
                  f"u {mu:.2f} each side, s {SIG_POCKET[0][1] - edge:.2f} at the island, stand-out {edge - 1.60 - SIG_POCKET[0][0]:.2f} | ok |")
        else:
            mu = min(span[0] - REF_SLOT[0][0], REF_SLOT[0][1] - span[1])
            print(f"| REF root | u {span[0]:.2f}-{span[1]:.2f} at s {edge:.2f} | drops {PI_BOTTOM - FLOOR_Y - 0.31:.2f} to the floor in the {BAY_S[1] - edge:.2f} gap before the end wall (bare PI, v2 geometry) | "
                  f"r9 end-wall slot u {REF_SLOT[0][0]:.2f}-{REF_SLOT[0][1]:.2f} × s {REF_SLOT[1][0]:.2f}-{REF_SLOT[1][1]:.2f} × y {REF_SLOT[2][0]:.2f}-{REF_SLOT[2][1]:.2f} | "
                  f"u {mu:.2f} each side, y {REF_SLOT[2][1] - 1.81:.2f} over the 0.31 ring stack | ok (drop UNVERIFIED) |")
    for ref in ("P4", "P5"):
        fx, fy = ring_flat[ref]
        y = PLANE_Y0 + (BEND_U1 - fx)
        print(f"| {ref} ring ({'VBUS' if ref == 'P4' else 'GND'}) | ({fx:.2f}, {fy:.2f}) | ({PLANE_U:.3f}, {fy:.2f}, {y:.3f}), copper on B facing the standoff | "
              f"wall face u 16.19-16.50, standoff u {P5_STANDOFF_END_U:.2f}-16.19 | plate y 1.695-6.895: lid {LID_Y - 6.895:.3f}, floor {1.695 - FLOOR_Y:.3f} | ok |")
    print(f"| P4/P5 joint root | u {BEND_U0:.2f}-{BEND_U1:.3f}, s 16.30-19.30 | bend to u 16.30 (outer), y 3.80-5.12 | wall face 16.50; rib s {RIB_S[0]:.2f}-{RIB_S[1]:.2f} | "
          f"wall 0.20 (FR4 side on the wall by design), rib {16.30 - RIB_S[1]:.2f} | ok |")
    print(f"| P4/P5 flap | u 16.904-19.114, s 14.85-19.30 | on the wall face, y 1.695-3.905 | crosses the rib s {RIB_S[0]:.2f}-{RIB_S[1]:.2f} (rib y {FLOOR_Y:.2f}-4.50) | "
          f"none without a slot: cut the rib back 0.50 from the wall (u 16.00-16.50, full rib height) | shell change (§7) |")
    j2 = cy["J2"]
    gap_u = P5_STANDOFF_END_U - j2[3]
    gap_s = j2[2] - P5_WELL_S[1]
    print(f"| J2 against the P5 well | courtyard u {j2[1]:.2f}-{j2[3]:.2f}, s {j2[2]:.2f}-{j2[4]:.2f} | y {PI_TOP:.2f}-{PI_TOP + HEIGHTS['J2'][0]:.2f} | "
          f"standoff end u {P5_STANDOFF_END_U:.2f}, well s {P5_WELL_S[0]:.2f}-{P5_WELL_S[1]:.2f} | u {gap_u:.2f}, s {gap_s:.2f} (need ≥ {J2_WELL_GAP:.1f}) | {'ok' if gap_u >= J2_WELL_GAP else 'FAIL'} |")
    print(f"| J3 stub after the cut | u {J3_STUB_U[0]:.2f}-{J3_STUB_U[1]:.2f}, s {J3_NECK_S[0]:.2f}-{J3_NECK_S[1]:.2f} | island plane y {PI_BOTTOM:.2f}-{PI_TOP:.2f} | wall face 16.50 | u {CAVITY_U[1] - J3_STUB_U[1]:.2f}; no Contact copper on the stub (§5.4) | ok |")
    print(f"| Island edges | u {ISLAND[0]:.2f}-{ISLAND[2]:.2f}, s {ISLAND[1]:.2f}-{ISLAND[3]:.2f} | y {STIFF_BOTTOM:.2f}-{PI_TOP:.2f} on the P1/P2 standoffs | walls u {CAVITY_U[0]:.2f}/{CAVITY_U[1]:.2f}, rib face {BAY_S[0]:.2f}, end wall {BAY_S[1]:.2f} | "
          f"u {ISLAND[0] - CAVITY_U[0]:.2f}/{CAVITY_U[1] - ISLAND[2]:.2f}, s {ISLAND[1] - BAY_S[0]:.2f}/{BAY_S[1] - ISLAND[3]:.2f} | ok |")
    for k, post in POSTS.items():
        print(f"| Lid post {k} | ({post[0]:.2f}, {post[1]:.2f}) Ø2.0 | from the lid {LID_Y:.2f} onto {'U1 (top 6.12, 0.98 long; load UNVERIFIED)' if k == 'P2' else f'the island F face {PI_TOP:.2f} (1.98 long)'} | over the {k} standoff | see the lid-post column above | ok |")
    return 0


def main() -> int:
    pcb = Path(sys.argv[sys.argv.index("--pcb") + 1]) if "--pcb" in sys.argv else PCB
    text = pcb.read_text(encoding="utf-8")
    fps = footprints(text)
    if "--folded" in sys.argv:
        return folded(fps, text)
    print("| ref | side | x (u) | y (s) | rot | footprint |")
    print("|---|---|---:|---:|---:|---|")
    for f in fps:
        print(f"| {f['ref']} | {f['side']} | {f['x']:.2f} | {f['y']:.2f} | {f['rot']:.0f} | `{f['fp']}` |")
    if "--pads" in sys.argv:
        print()
        print("| pad | kind | net | x (u) | y (s) |")
        print("|---|---|---|---:|---:|")
        for f in fps:
            if f["ref"] not in PAD_REFS:
                continue
            for num, kind, ax, ay, net in f["pads"]:
                if not num:
                    continue
                print(f"| {f['ref']}.{num} | {kind} | {net} | {ax:.2f} | {ay:.2f} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
