#!/usr/bin/env python3
"""Incremental A* on the WP12g copper. Does not wipe tracks.

JLC flex via (https://jlcpcb.com/capabilities/flex-pcb-capabilities,
read 2026-09-18): regular 0.30/0.55 mm; extreme 2-layer 0.10/0.30 mm
(extra cost). Default here is regular. Extreme is --via-extreme.
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import wx

_APP = wx.App(False)

import pcbnew  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_v2b import (  # noqa: E402
    BOARD_DIR,
    CHARGE_U0,
    CONTACT_CLEAR,
    CONTACT_TRACK,
    FLEX_CLEAR,
    FLEX_TRACK,
    outline_points,
)
from maze_route import Grid, add_seg, astar, pnpoly  # noqa: E402

# maze_route.add_via uses VIA_D from that module. Patch after import.
import maze_route as maze  # noqa: E402

PCB = BOARD_DIR / "elicio-v2.kicad_pcb"
KICAD_CLI = "kicad-cli"
CONTACT = {"SIG1", "SIG2", "REF"}
STEP = 0.10
ASTAR_CAP = 400000
EDGE = 0.35
VIA_REG = (0.55, 0.30)
VIA_EXTREME = (0.30, 0.10)
BEND = (4.65, 14.40, 11.65, 16.00)

GROUPS = {
    "vbus": ("VBUS",),
    "j4": ("SWDIO", "SWDCLK", "nRESET", "+VDD"),
    "j3": ("SIG1", "SIG2", "REF"),
    "u2": (
        "AFE_IN1N",
        "AFE_IN1P",
        "VREFP",
        "AFE_RESET",
        "AFE_START",
        "AFE_CS_AFE",
        "AFE_MOSI_AFE",
        "AFE_SCLK_AFE",
        "AFE_MISO_AFE",
        "RLDINV",
        "+3V0",
    ),
    "stitch": (),  # remaining nets
}


def set_via(dia: float, drill: float) -> None:
    maze.VIA_D = dia
    maze.VIA_DRILL = drill
    maze.ASTAR_CAP = ASTAR_CAP
    maze.STEP = STEP


def layer_of(desc: str) -> list[int]:
    if "PTH" in desc:
        return [0, 1]
    if "B.Cu" in desc:
        return [1]
    return [0]


def net_of(desc: str) -> str:
    i = desc.find("[")
    j = desc.find("]", i + 1)
    if i >= 0 and j > i:
        return desc[i + 1 : j]
    return ""


def pad_xy(board, ref: str, num: str) -> tuple[float, float]:
    fp = next(f for f in board.GetFootprints() if f.GetReference() == ref)
    for pad in fp.Pads():
        if pad.GetNumber() == num:
            p = pad.GetPosition()
            return pcbnew.ToMM(p.x), pcbnew.ToMM(p.y)
    raise KeyError(f"{ref}.{num}")


def lock_new(board, before: set[int]) -> None:
    for t in board.GetTracks():
        if id(t) in before:
            continue
        try:
            t.SetLocked(True)
        except Exception:
            pass


def lock_path(board, net, pts, layer, width: float) -> None:
    before = {id(t) for t in board.GetTracks()}
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        maze.add_seg(board, net, x0, y0, x1, y1, layer, width)
    lock_new(board, before)


def lock_via(board, net, x: float, y: float) -> None:
    before = {id(t) for t in board.GetTracks()}
    maze.add_via(board, net, x, y)
    lock_new(board, before)


def route_vbus_p4(board) -> None:
    """Do not add copper. Hole gap and east neck cannot take VBUS. See report."""
    print(
        "VBUS P4->island not closed: H1/H2 gap 1.20 mm has RLD_FB at x=15.263 "
        "and AFE_DRDY_AFE at x=15.742 (0.179 mm left; 0.10+2*0.10=0.30 needed). "
        "East neck 19.60 keep to 19.75 edge is 0.15 mm (need 0.35 to edge). "
        "F.Cu hang GND at y=7.80 vs hang south 7.40 (track centre min 7.75)."
    )


def route_j4(board) -> None:
    """SWDIO/SWDCLK: F.Cu cannot cross SIG2 at x=13.50 without a via slot.

    J4 keep bans vias in (14.25-18.25, 21.10-28.10). SIG2 0.15 at x=13.50
    plus via 0.55 needs 0.55 mm; keep left 14.25 leaves 0.175 mm. Skip copper.
    """
    print(
        "J4 SWDIO/SWDCLK not closed: SIG2 Contact 0.15 at x=13.500 y=19.50-28.20; "
        "AFE_IN1P 0.10 at x=13.173 y=22.08-29.01; J4 keep vias=False to x=14.25. "
        "Via centre needs >=13.50+0.075+0.20+0.275=14.050 and <=14.25-0.275=13.975."
    )


def route_j3(board) -> None:
    """J3 SIG1/SIG2 hang is blocked on both layers. REF already reaches J3."""
    print(
        "J3 SIG1 not closed: Contact 0.15+2*0.20=0.55 vs R4.1 RLD_FB "
        "(15.190,19.970) and GND B.Cu at y=20.578 x=16.78-18.31 (0.228 mm "
        "window). SIG2 not closed: LED_EN B.Cu x=19.327 y=28.45-35.00 vs "
        "GND B.Cu x=18.972 y=22.54-26.37 (0.355 mm; two 0.10 tracks need 0.40)."
    )


def pair_key(r: dict) -> tuple:
    return (r["net"], round(r["ax"], 3), round(r["ay"], 3), round(r["bx"], 3), round(r["by"], 3))


def pair_sort_key(r: dict) -> tuple:
    # P4 CHARGE stub first (east, low s).
    p4 = 0 if r["net"] == "VBUS" and max(r["ax"], r["bx"]) > 22 else 1
    return (p4, -(max(r["ax"], r["bx"])))


def extra_for(name: str) -> tuple[float, float]:
    if name in CONTACT:
        return CONTACT_TRACK / 2.0 + CONTACT_CLEAR, CONTACT_TRACK
    return FLEX_TRACK / 2.0 + FLEX_CLEAR, FLEX_TRACK


def stamp_seg(grid: Grid, x0, y0, x1, y1, layers: list[int], r: float, via_ban=False) -> None:
    length = math.hypot(x1 - x0, y1 - y0)
    n = max(1, int(length / (grid.step * 0.4)))
    for k in range(n + 1):
        t = k / n
        grid.stamp_r(layers, x0 + t * (x1 - x0), y0 + t * (y1 - y0), r, via_ban=via_ban)


def seed(board, skip_net: str | None) -> Grid:
    outline = outline_points()
    xs = [p[0] for p in outline]
    ys = [p[1] for p in outline]
    grid = Grid(min(xs) - 1.0, min(ys) - 1.0, max(xs) + 1.0, max(ys) + 1.0, step=STEP)
    for iy in range(grid.ny):
        for ix in range(grid.nx):
            x, y = grid.coord(ix, iy)
            i = grid.index(ix, iy)
            if not pnpoly(x, y, outline):
                grid.block[0][i] = 1
                grid.block[1][i] = 1
                grid.via_ban[i] = 1
            if BEND[0] <= x <= BEND[2] and BEND[1] <= y <= BEND[3]:
                grid.via_ban[i] = 1
    seq = list(outline) + [outline[0]]
    for (x0, y0), (x1, y1) in zip(seq, seq[1:]):
        stamp_seg(grid, x0, y0, x1, y1, [0, 1], EDGE, via_ban=True)
    for z in board.Zones():
        if not z.GetIsRuleArea():
            continue
        name = z.GetZoneName()
        bb = z.GetBoundingBox()
        x0, y0 = pcbnew.ToMM(bb.GetLeft()), pcbnew.ToMM(bb.GetTop())
        x1, y1 = pcbnew.ToMM(bb.GetRight()), pcbnew.ToMM(bb.GetBottom())
        if z.GetDoNotAllowTracks():
            lys = []
            if z.IsOnLayer(pcbnew.F_Cu):
                lys.append(0)
            if z.IsOnLayer(pcbnew.B_Cu):
                lys.append(1)
            if not lys:
                lys = [0, 1]
            grid.stamp(lys, x0, y0, x1, y1, via_ban=True)
        if name.startswith("strip_") or name.startswith("RING_"):
            grid.stamp([], x0, y0, x1, y1, via_ban=True)
            for iy in range(grid.ny):
                for ix in range(grid.nx):
                    x, y = grid.coord(ix, iy)
                    if x0 <= x <= x1 and y0 <= y <= y1:
                        grid.via_ban[grid.index(ix, iy)] = 1
    extra_def = FLEX_TRACK / 2.0 + FLEX_CLEAR
    extra_con = CONTACT_TRACK / 2.0 + CONTACT_CLEAR
    via_r = maze.VIA_D / 2.0 + extra_def
    for t in board.GetTracks():
        cls = t.GetClass()
        name = t.GetNetname()
        if skip_net and name == skip_net:
            continue
        ex = extra_con if name in CONTACT else extra_def
        if cls == "PCB_VIA":
            p = t.GetPosition()
            grid.stamp_r([0, 1], pcbnew.ToMM(p.x), pcbnew.ToMM(p.y), via_r, via_ban=True)
            continue
        if cls not in {"PCB_TRACK", "PCB_ARC"}:
            continue
        s, e = t.GetStart(), t.GetEnd()
        ly = 0 if t.GetLayer() == pcbnew.F_Cu else 1
        r = pcbnew.ToMM(t.GetWidth()) / 2.0 + (CONTACT_CLEAR if name in CONTACT else FLEX_CLEAR)
        stamp_seg(grid, pcbnew.ToMM(s.x), pcbnew.ToMM(s.y), pcbnew.ToMM(e.x), pcbnew.ToMM(e.y), [ly], r)
    for fp in board.GetFootprints():
        for pad in fp.Pads():
            name = pad.GetNetname()
            if skip_net and name == skip_net:
                continue
            if name.startswith("unconnected"):
                p = pad.GetPosition()
                sz = pad.GetSize()
                r = 0.5 * max(pcbnew.ToMM(sz.x), pcbnew.ToMM(sz.y)) + extra_def
                lys = []
                if pad.IsOnLayer(pcbnew.F_Cu):
                    lys.append(0)
                if pad.IsOnLayer(pcbnew.B_Cu):
                    lys.append(1)
                grid.stamp_r(lys or [0], pcbnew.ToMM(p.x), pcbnew.ToMM(p.y), r)
                continue
            p = pad.GetPosition()
            sz = pad.GetSize()
            r = 0.5 * max(pcbnew.ToMM(sz.x), pcbnew.ToMM(sz.y)) + (
                extra_con if name in CONTACT else extra_def
            )
            lys = []
            if pad.IsOnLayer(pcbnew.F_Cu):
                lys.append(0)
            if pad.IsOnLayer(pcbnew.B_Cu):
                lys.append(1)
            try:
                if pad.GetAttribute() == pcbnew.PAD_ATTRIB_NPTH:
                    grid.stamp_r([0, 1], pcbnew.ToMM(p.x), pcbnew.ToMM(p.y), r + 0.20, via_ban=True)
                    continue
            except Exception:
                pass
            grid.stamp_r(lys or [0], pcbnew.ToMM(p.x), pcbnew.ToMM(p.y), r)
    return grid


def cells_at(grid: Grid, x: float, y: float, layers: list[int], r: float = 0.20) -> set[tuple[int, int, int]]:
    out = set()
    for ly in layers:
        a = grid.ixy(x - r, y - r)
        b = grid.ixy(x + r, y + r)
        if a is None or b is None:
            c = grid.ixy(x, y)
            if c:
                out.add((c[0], c[1], ly))
            continue
        for iy in range(a[1], b[1] + 1):
            for ix in range(a[0], b[0] + 1):
                i = grid.index(ix, iy)
                if grid.block[ly][i]:
                    continue
                out.add((ix, iy, ly))
        if not out:
            c = grid.ixy(x, y)
            if c and not grid.block[ly][grid.index(c[0], c[1])]:
                out.add((c[0], c[1], ly))
            elif c:
                # sit on copper of this net: force-open a 3x3
                for dy in range(-2, 3):
                    for dx in range(-2, 3):
                        ix, iy = c[0] + dx, c[1] + dy
                        if 0 <= ix < grid.nx and 0 <= iy < grid.ny:
                            grid.block[ly][grid.index(ix, iy)] = 0
                            out.add((ix, iy, ly))
    return out


def route_pair(board, net, x0, y0, lys0, x1, y1, lys1) -> bool:
    name = net.GetNetname()
    extra, width = extra_for(name)
    grid = seed(board, skip_net=name)
    starts = cells_at(grid, x0, y0, lys0)
    goals = cells_at(grid, x1, y1, lys1)
    if not starts or not goals:
        print("no cells", name, (x0, y0, lys0), (x1, y1, lys1), "starts", len(starts), "goals", len(goals))
        return False
    path, expanded = astar(grid, starts, goals)
    if not path:
        print("astar fail", name, "expanded", expanded, f"{x0:.3f},{y0:.3f} -> {x1:.3f},{y1:.3f}")
        return False
    n_before = len(list(board.GetTracks()))
    maze.commit_path(board, net, grid, path, extra, width)
    # stub to the requested ends
    ix0, iy0, ly0 = path[0]
    ix1, iy1, ly1 = path[-1]
    sx, sy = grid.coord(ix0, iy0)
    ex, ey = grid.coord(ix1, iy1)
    maze.add_seg(board, net, x0, y0, sx, sy, pcbnew.F_Cu if ly0 == 0 else pcbnew.B_Cu, width)
    maze.add_seg(board, net, x1, y1, ex, ey, pcbnew.F_Cu if ly1 == 0 else pcbnew.B_Cu, width)
    added = 0
    for t in list(board.GetTracks())[n_before:]:
        try:
            t.SetLocked(True)
            added += 1
        except Exception:
            pass
    print("routed", name, f"{x0:.3f},{y0:.3f}->{x1:.3f},{y1:.3f}", "segs", added, "exp", expanded)
    return True


def drc_report(pcb: Path) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "drc.json"
        subprocess.run(
            [KICAD_CLI, "pcb", "drc", "--format", "json", "-o", str(out), str(pcb)],
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(out.read_text())


def rats_from(report: dict) -> list[dict]:
    rows = []
    for u in report.get("unconnected_items") or []:
        items = u.get("items") or []
        if len(items) < 2:
            continue
        a, b = items[0], items[1]
        da, db = a.get("description") or "", b.get("description") or ""
        pa, pb = a.get("pos") or {}, b.get("pos") or {}
        name = net_of(da) or net_of(db)
        rows.append(
            {
                "net": name,
                "a": da,
                "b": db,
                "ax": float(pa.get("x", 0)),
                "ay": float(pa.get("y", 0)),
                "bx": float(pb.get("x", 0)),
                "by": float(pb.get("y", 0)),
                "al": layer_of(da),
                "bl": layer_of(db),
            }
        )
    return rows


def group_nets(group: str) -> set[str] | None:
    if group == "stitch":
        return None
    return set(GROUPS[group])


def run_group(board, pcb: Path, group: str) -> tuple[int, int, list[str]]:
    wanted = group_nets(group)
    failed: list[str] = []
    skipped: set[tuple] = set()
    routed = 0
    if group == "vbus":
        route_vbus_p4(board)
    if group == "j4":
        route_j4(board)
    if group == "j3":
        route_j3(board)
    for _ in range(80):
        board.Save(str(pcb))
        report = drc_report(pcb)
        errs_before = sum(1 for v in (report.get("violations") or []) if v.get("severity") == "error")
        rats = rats_from(report)
        if wanted is not None:
            rats = [r for r in rats if r["net"] in wanted]
        rats = [r for r in rats if pair_key(r) not in skipped]
        rats.sort(key=pair_sort_key)
        if not rats:
            break
        r = rats[0]
        net = board.FindNet(r["net"])
        if net is None:
            failed.append(f"{r['net']} missing net")
            skipped.add(pair_key(r))
            continue
        good = pcb.with_name(pcb.stem + ".good.kicad_pcb")
        board.Save(str(pcb))
        shutil.copy2(pcb, good)
        ok = route_pair(board, net, r["ax"], r["ay"], r["al"], r["bx"], r["by"], r["bl"])
        if not ok:
            failed.append(
                f"{r['net']} {r['a']} @({r['ax']:.3f},{r['ay']:.3f}) -> {r['b']} @({r['bx']:.3f},{r['by']:.3f})"
            )
            skipped.add(pair_key(r))
            continue
        board.Save(str(pcb))
        report2 = drc_report(pcb)
        errs_after = sum(1 for v in (report2.get("violations") or []) if v.get("severity") == "error")
        if errs_after > errs_before:
            shutil.copy2(good, pcb)
            board = pcbnew.LoadBoard(str(pcb))
            failed.append(
                f"{r['net']} DRC {errs_before}->{errs_after} {r['a'][:40]} @({r['ax']:.3f},{r['ay']:.3f})"
            )
            skipped.add(pair_key(r))
            continue
        routed += 1
    board.Save(str(pcb))
    report = drc_report(pcb)
    errs = sum(1 for v in (report.get("violations") or []) if v.get("severity") == "error")
    nrat = len(report.get("unconnected_items") or [])
    print("group", group, "routed", routed, "failed", len(failed), "drc_errors", errs, "unconnected", nrat)
    return errs, nrat, failed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--group", choices=list(GROUPS), required=True)
    parser.add_argument("--via-extreme", action="store_true")
    parser.add_argument("--pcb", type=Path, default=PCB)
    args = parser.parse_args()
    dia, drill = VIA_EXTREME if args.via_extreme else VIA_REG
    set_via(dia, drill)
    print("via", dia, drill, "group", args.group)
    board = pcbnew.LoadBoard(str(args.pcb))
    errs, nrat, failed = run_group(board, args.pcb, args.group)
    for f in failed:
        print("FAIL", f)
    return 1 if failed and errs else 0


if __name__ == "__main__":
    raise SystemExit(main())
