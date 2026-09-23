#!/usr/bin/env python3
"""Run independent A/B/C routing trials on copies; never writes the source PCB.

Use KiCad's bundled Python (wx/pcbnew). Outputs go only to --work, not git.
The experimental placement changes only the four SPI resistors and four
resistors whose old sites they take; all mechanical sites remain pinned.
"""
from __future__ import annotations

import argparse
import collections
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

import wx

_APP = wx.App(False)
import pcbnew

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "hardware/board/elicio-v2.kicad_pcb"
HAND = ROOT / "hardware/board/hand_route.py"
JAVA = "/opt/homebrew/opt/openjdk@25/bin/java"
JAR = Path.home() / ".local/opt/freerouting/freerouting-2.4.1.jar"
KICAD_PY = sys.executable
# Swaps place the ADS SPI series parts at s=9.52..13.12 rather than s=23..36.
SWAPS = (("R5", "R27"), ("R6", "R28"), ("R7", "R29"), ("R8", "R30"))
J2_TRIAL = (14.30, 11.35)  # mm: 0.85 inward; P5 shell gap exactly 0.30
GROUPS = ("j3", "vbus", "j4", "u2", "stitch")


def run(cmd: list[str], log: Path, *, allow_failure: bool = False) -> int:
    with log.open("w") as out:
        p = subprocess.run(cmd, stdout=out, stderr=subprocess.STDOUT, text=True)
    if p.returncode and not allow_failure:
        raise RuntimeError(f"exit {p.returncode}: {' '.join(cmd)}; see {log}")
    return p.returncode


def drc(pcb: Path, path: Path) -> dict:
    p = subprocess.run(["kicad-cli", "pcb", "drc", "--format", "json", "-o", str(path), str(pcb)], capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(p.stderr)
    report = json.loads(path.read_text())
    types = collections.Counter((v["type"], v["severity"]) for v in report.get("violations", []))
    result = {"errors": sum(n for (t, sev), n in types.items() if sev == "error"),
              "warnings": sum(n for (t, sev), n in types.items() if sev == "warning"),
              "shorts": sum(n for (t, sev), n in types.items() if t == "shorting_items"),
              "unconnected": len(report.get("unconnected_items", [])),
              "types": {f"{t}/{sev}": n for (t, sev), n in sorted(types.items())}}
    print(path.stem, result, flush=True)
    return result


def prepare(option: str, work: Path) -> Path:
    work.mkdir(parents=True, exist_ok=True)
    pcb = work / "trial.kicad_pcb"
    for suffix in (".kicad_pro", ".kicad_dru"):
        shutil.copy2(SOURCE.with_suffix(suffix), pcb.with_suffix(suffix))
    board = pcbnew.LoadBoard(str(SOURCE))
    if option in ("A", "C"):
        fps = {fp.GetReference(): fp for fp in board.GetFootprints()}
        positions = {ref: fp.GetPosition() for ref, fp in fps.items()}
        for a, b in SWAPS:
            fps[a].SetPosition(positions[b])
            fps[b].SetPosition(positions[a])
        fps["J2"].SetPosition(pcbnew.VECTOR2I(*(pcbnew.FromMM(x) for x in J2_TRIAL)))
        fps["J2"].SetOrientationDegrees(0)  # search clear pad/outline and shell gap
        # Same 2D AABB formula and dimensions as shell t-0001
        # bte_fit_shell.py V2_CAVITY_v3; P5 fixed at (20.50,12.35).
        du = abs(J2_TRIAL[0] - 19.0) - (5.80 + 3.0) / 2
        ds = abs(J2_TRIAL[1] - 12.35) - (6.56 + 5.30) / 2
        gap = math.hypot(max(du, 0), max(ds, 0)) if du >= 0 and ds >= 0 else (du if du >= 0 else ds if ds >= 0 else min(du, ds))
        if gap < 0.30 - 1e-6:
            raise ValueError(f"J2/P5 shell standoff gap {gap:.3f} < 0.30 mm")
        print("J2/P5 shell courtyard gap", round(gap, 3), "mm", flush=True)
    if option in ("B", "C"):
        board.SetCopperLayerCount(4)
        board.GetDesignSettings().SetBoardThickness(pcbnew.FromMM(0.20))
        # Inner layers are signal-accessible until all pads are connected;
        # unverified solid planes would conceal rats and alter Contact safety.
        # GND / +3V0 inner pours may only follow a clean DRC route.
    board.SetFileName(str(pcb))
    board.Save(str(pcb))
    if option in ("A", "C"):
        # Isolate KiCad 10's SWIG Remove()/LoadBoard invalidation in a child.
        run([KICAD_PY, str(Path(__file__)), "--strip-only", str(pcb)], work / "strip.log")
    return pcb


def route(option: str, work: Path) -> None:
    pcb = prepare(option, work)
    results = {"option": option, "source": str(SOURCE), "before": drc(pcb, work / "before.json")}
    (work / "measure.json").write_text(json.dumps(results, indent=2) + "\n")
    board = pcbnew.LoadBoard(str(pcb))
    dsn = work / "trial.dsn"
    pcbnew.ExportSpecctraDSN(board, str(dsn))
    from route_v2 import DSN_VIA, FREEROUTE_FLAGS, check_dsn_classes, sanitize_dsn
    sanitize_dsn(dsn)
    missing = check_dsn_classes(dsn)
    if option in ("B", "C"):
        # The shared checker expects a two-layer Via[0-1] padstack. A through
        # via in this four-layer trial spans layers 0..3 instead.
        missing = [fact for fact in missing if fact != DSN_VIA]
        if not re.search(r"Via\[0-3\]_550:300_um", dsn.read_text()):
            missing.append("four-layer regular through-via 550:300 um")
    if missing:
        raise RuntimeError(f"DSN classes: {missing}")
    cmd = [JAVA, "-Djava.awt.headless=true", "-Xmx4g", "-jar", str(JAR),
           f"--user_data_path={work / 'fr-home'}", "-de", str(dsn),
           "-do", str(work / "trial.ses"), *FREEROUTE_FLAGS]
    run(cmd, work / "freerouting.log")
    # Import on the copy. Do not use build_v2b.import_ses: its configure_rules
    # resets the four-layer trial's thickness and two-layer via rules.
    board = pcbnew.LoadBoard(str(pcb))
    pcbnew.ImportSpecctraSES(board, str(work / "trial.ses"))
    for t in board.GetTracks():
        if t.GetClass() in ("PCB_TRACK", "PCB_ARC") and t.GetWidth() < pcbnew.FromMM(0.10):
            t.SetWidth(pcbnew.FromMM(0.10))
    board.SetFileName(str(pcb))
    board.Save(str(pcb))
    results["router"] = drc(pcb, work / "router.json")
    (work / "measure.json").write_text(json.dumps(results, indent=2) + "\n")
    hand_pass(work, results)
    if option in ("B", "C"):
        planes(work, results)


def planes(work: Path, results: dict) -> None:
    """Measure copper with actual inner GND/+3V0 planes; keep SIG/REF strips free."""
    sys.path.insert(0, str(ROOT / "hardware/board"))
    from build_v2b import add_copper_zone
    source = work / "trial.kicad_pcb"
    pcb = work / "with-planes.kicad_pcb"
    shutil.copy2(source, pcb)
    for suffix in (".kicad_pro", ".kicad_dru"):
        shutil.copy2(source.with_suffix(suffix), pcb.with_suffix(suffix))
    board = pcbnew.LoadBoard(str(pcb))
    # Both rectangles stay inside the island/pocket; tabs, rings, folds and
    # the break-off J3 tab are omitted. Other nets get normal plane clearance.
    # Keep 0.30 mm off U1 antenna no-copper region u2.25..6.05,
    # s26.15..38.55 on BOTH inner layers (board-v2 §11).
    island = [(2.75, 16.50), (19.25, 16.50), (19.25, 37.10),
              (6.35, 37.10), (6.35, 25.85), (2.75, 25.85)]
    pocket = [(12.50, 1.85), (19.75, 1.85), (19.75, 15.50), (12.50, 15.50)]
    for layer, name in ((pcbnew.In1_Cu, "GND"), (pcbnew.In2_Cu, "+3V0")):
        for label, points in (("island", island), ("pocket", pocket)):
            add_copper_zone(board, f"STUDY_{name}_{label}", board.FindNet(name), points, layer)
    for zone in board.Zones():
        if zone.GetZoneName().startswith("STUDY_"):
            zone.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())
    board.SetFileName(str(pcb))
    board.Save(str(pcb))
    results["planes"] = drc(pcb, work / "planes.json")
    (work / "measure.json").write_text(json.dumps(results, indent=2) + "\n")


def hand_pass(work: Path, results: dict) -> None:
    pcb = work / "trial.kicad_pcb"
    # Same five groups and rollback policy as WP12i. A failed candidate
    # returns 1 if DRC already has errors; keep its full log and DRC results.
    for group in GROUPS:
        if group in results:
            continue
        log = work / f"hand-{group}.log"
        status = run([KICAD_PY, str(HAND), "--pcb", str(pcb), "--group", group],
                     log, allow_failure=True)
        # hand_route returns 1 for rejected paths on an already-invalid board;
        # any other failure or an incomplete pass is not a measurement.
        if status not in (0, 1) or f"group {group} routed " not in log.read_text():
            raise RuntimeError(f"hand route failed (exit {status}); see {log}")
        results[group] = drc(pcb, work / f"after-{group}.json")
        (work / "measure.json").write_text(json.dumps(results, indent=2) + "\n")
    print("DONE", work / "measure.json", flush=True)


def width_screen(option: str, width: int, work: Path) -> None:
    """Necessary outline/courtyard screen, not a solved placement or routed board.

    Preserve the narrow mechanical tabs, move the posterior edge, charge
    rings, bosses and J2 with it. Failures here need packing redesign before
    another router run can have any meaning.
    """
    if width not in (18, 20):
        raise ValueError(width)
    pcb = prepare(option, work)
    board = pcbnew.LoadBoard(str(pcb))
    shift = 22 - width
    for d in board.GetDrawings():
        if d.GetLayer() != pcbnew.Edge_Cuts or not hasattr(d, "GetStart"):
            continue
        for getter, setter in ((d.GetStart, d.SetStart), (d.GetEnd, d.SetEnd)):
            pos = getter()
            x, y = pcbnew.ToMM(pos.x), pcbnew.ToMM(pos.y)
            if (abs(x - 19.75) < 0.001 and y >= 16.0 or
                abs(x - 20.50) < 0.001 or abs(x - 26.14) < 0.001):
                setter(pcbnew.VECTOR2I(pcbnew.FromMM(x - shift), pos.y))
    for fp in board.GetFootprints():
        if fp.GetReference() in ("P4", "P5", "H1", "H2", "J2"):
            pos = fp.GetPosition()
            if fp.GetReference() == "J2":
                new_x = 14.30 - shift  # shell's P5 well follows the wall
            else:
                new_x = pcbnew.ToMM(pos.x) - shift
            fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(new_x), pos.y))
    board.SetFileName(str(pcb))
    board.Save(str(pcb))
    result = drc(pcb, work / "width-screen.json")
    (work / "width-screen-summary.json").write_text(json.dumps(
        {"option": option, "body_width_mm": width, "note": "geometry screen only; not routed",
         "j2_shell_p5_gap_mm": 0.30, "drc": result}, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("option", nargs="?", choices=("A", "B", "C"))
    parser.add_argument("--strip-only", type=Path)
    parser.add_argument("--work", type=Path)
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--resume-hand", action="store_true")
    parser.add_argument("--planes-only", action="store_true")
    parser.add_argument("--width-screen", type=int, choices=(18, 20))
    args = parser.parse_args()
    if args.strip_only:
        copy = args.strip_only.resolve()
        if copy.name != "trial.kicad_pcb" or copy == SOURCE or ROOT in copy.parents:
            raise ValueError("--strip-only requires an outside-repository trial.kicad_pcb")
        board = pcbnew.LoadBoard(str(copy))
        for track in list(board.GetTracks()):
            if track.IsLocked() and track.GetNetname() in ("SIG1", "SIG2", "REF"):
                continue
            board.Remove(track)
        board.Save(str(copy))
        return
    if args.option is None or args.work is None:
        parser.error("option and --work required")
    if args.work.resolve() == SOURCE.parent.resolve() or ROOT in args.work.resolve().parents:
        raise ValueError("work must be outside the repository")
    if args.width_screen:
        width_screen(args.option, args.width_screen, args.work.resolve())
    elif args.planes_only:
        work = args.work.resolve()
        planes(work, json.loads((work / "measure.json").read_text()))
    elif args.resume_hand:
        work = args.work.resolve()
        hand_pass(work, json.loads((work / "measure.json").read_text()))
    elif args.prepare_only:
        pcb = prepare(args.option, args.work.resolve())
        drc(pcb, args.work.resolve() / "before.json")
    else:
        route(args.option, args.work.resolve())


if __name__ == "__main__":
    main()
