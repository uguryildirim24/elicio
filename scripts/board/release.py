#!/usr/bin/env python3
"""Run the elicio-v2 board release job (ERC, DRC, BOM, CPL, gerbers, STEP).

Fails closed on any ERC error or any missing output. DRC errors are recorded
and do not fail the job (routing is not required this round).
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BOARD_DIR = ROOT / "hardware" / "board"
KICAD_SHARE = Path("/Applications/KiCad/KiCad.app/Contents/SharedSupport")

REQUIRED_ENV = {
    "KICAD10_SYMBOL_DIR": KICAD_SHARE / "symbols",
    "KICAD10_FOOTPRINT_DIR": KICAD_SHARE / "footprints",
    "KICAD10_3DMODEL_DIR": KICAD_SHARE / "3dmodels",
}

GERBER_LAYERS = (
    "F.Cu,B.Cu,"
    "F.SilkS,B.SilkS,F.Mask,B.Mask,F.Paste,B.Paste,Edge.Cuts,"
    "Eco1.User,Eco2.User,Dwgs.User,Cmts.User"
)


def configure_kicad_env() -> None:
    for key, path in REQUIRED_ENV.items():
        os.environ.setdefault(key, str(path))
    brew_cli = Path("/opt/homebrew/bin")
    if brew_cli.is_dir():
        os.environ["PATH"] = f"{brew_cli}{os.pathsep}{os.environ.get('PATH', '')}"


def kicad_cli() -> str:
    exe = shutil.which("kicad-cli")
    if not exe:
        sys.stderr.write(
            "kicad-cli is absent; install with: brew install --cask kicad\n"
        )
        raise SystemExit(2)
    return exe


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=check, text=True, capture_output=True)


def count_severity(payload: dict, bucket: str, severity: str) -> int:
    items = payload.get(bucket) or payload.get("violations") or []
    if bucket == "violations" and "sheets" in payload:
        items = []
        for sheet in payload["sheets"]:
            items.extend(sheet.get("violations") or [])
    return sum(1 for item in items if str(item.get("severity", "")).lower() == severity)


def erc_counts(payload: dict) -> tuple[int, int]:
    items: list[dict] = []
    for sheet in payload.get("sheets") or []:
        items.extend(sheet.get("violations") or [])
    errors = sum(1 for item in items if str(item.get("severity", "")).lower() == "error")
    warnings = sum(1 for item in items if str(item.get("severity", "")).lower() == "warning")
    return errors, warnings


def write_jlc_cpl(pos_csv: Path, out_csv: Path) -> int:
    """Rewrite KiCad pos CSV into JLCPCB CPL columns."""
    text = pos_csv.read_text()
    # KiCad csv may start with comment lines.
    lines = [ln for ln in text.splitlines() if ln.strip() and not ln.startswith("#")]
    if not lines:
        out_csv.write_text("Designator,Val,Package,Mid X,Mid Y,Rotation,Layer\n")
        return 0
    reader = csv.DictReader(lines)
    rows = []
    for row in reader:
        # KiCad 10 pos headers: Ref, Val, Package, PosX, PosY, Rot, Side
        ref = row.get("Ref") or row.get("Designator") or ""
        val = row.get("Val") or row.get("Value") or ""
        pkg = row.get("Package") or row.get("Footprint") or ""
        x = row.get("PosX") or row.get("Mid X") or ""
        y = row.get("PosY") or row.get("Mid Y") or ""
        rot = row.get("Rot") or row.get("Rotation") or "0"
        side = (row.get("Side") or row.get("Layer") or "top").strip().lower()
        layer = "bottom" if side in {"bottom", "back"} else "top"
        rows.append((ref, val, pkg, x, y, rot, layer))
    with out_csv.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["Designator", "Val", "Package", "Mid X", "Mid Y", "Rotation", "Layer"])
        writer.writerows(rows)
    return len(rows)


def count_placed_parts(sch: Path) -> int:
    """Count schematic symbol instances that are on the board, in the BOM, not DNP."""
    text = sch.read_text()
    count = 0
    for match in re.finditer(r"\(symbol\n\t\t\(lib_id", text):
        chunk = text[match.start() : match.start() + 1200]
        if "(in_bom yes)" in chunk and "(dnp no)" in chunk and "(on_board yes)" in chunk:
            count += 1
    return count


def bom_row_count(path: Path) -> int:
    with path.open(newline="") as fh:
        reader = csv.reader(fh)
        rows = [r for r in reader if any(cell.strip() for cell in r)]
    return max(0, len(rows) - 1)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--board-dir",
        type=Path,
        default=BOARD_DIR,
        help="Directory that holds elicio-v2.kicad_*",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Release output directory (default: <board-dir>/release)",
    )
    args = parser.parse_args()
    configure_kicad_env()
    cli = kicad_cli()
    board_dir = args.board_dir.resolve()
    sch = board_dir / "elicio-v2.kicad_sch"
    pcb = board_dir / "elicio-v2.kicad_pcb"
    out = (args.out or (board_dir / "release")).resolve()
    out.mkdir(parents=True, exist_ok=True)
    gerber_dir = out / "gerbers"
    gerber_dir.mkdir(exist_ok=True)

    missing = [p for p in (sch, pcb) if not p.is_file()]
    if missing:
        sys.stderr.write("missing input: " + ", ".join(str(p) for p in missing) + "\n")
        return 1

    erc_json = out / "erc.json"
    drc_json = out / "drc.json"
    bom_csv = out / "bom.csv"
    pos_csv = out / "pos.csv"
    cpl_csv = out / "cpl.csv"
    step = out / "elicio-v2.step"
    summary = out / "summary.json"

    erc = run(
        [cli, "sch", "erc", "--format", "json", "-o", str(erc_json), str(sch)],
        check=False,
    )
    if not erc_json.is_file():
        sys.stderr.write(erc.stderr or erc.stdout or "ERC produced no report\n")
        return 1
    erc_payload = json.loads(erc_json.read_text())
    erc_errors, erc_warnings = erc_counts(erc_payload)

    drc = run(
        [cli, "pcb", "drc", "--format", "json", "-o", str(drc_json), str(pcb)],
        check=False,
    )
    if not drc_json.is_file():
        sys.stderr.write(drc.stderr or drc.stdout or "DRC produced no report\n")
        return 1
    drc_payload = json.loads(drc_json.read_text())
    drc_errors = count_severity(drc_payload, "violations", "error")
    drc_warnings = count_severity(drc_payload, "violations", "warning")
    unconnected = len(drc_payload.get("unconnected_items") or [])

    bom = run(
        [
            cli,
            "sch",
            "export",
            "bom",
            "--fields",
            "Reference,Value,Footprint,LCSC,MPN",
            "--labels",
            "Designator,Comment,Footprint,LCSC Part #,MPN",
            "--exclude-dnp",
            "-o",
            str(bom_csv),
            str(sch),
        ],
        check=False,
    )
    pos = run(
        [
            cli,
            "pcb",
            "export",
            "pos",
            "--format",
            "csv",
            "--units",
            "mm",
            "--side",
            "both",
            "--smd-only",
            "--exclude-dnp",
            "-o",
            str(pos_csv),
            str(pcb),
        ],
        check=False,
    )
    gerbers = run(
        [
            cli,
            "pcb",
            "export",
            "gerbers",
            "-o",
            str(gerber_dir),
            "--layers",
            GERBER_LAYERS,
            "--no-protel-ext",
            str(pcb),
        ],
        check=False,
    )
    drill = run(
        [
            cli,
            "pcb",
            "export",
            "drill",
            "-o",
            str(gerber_dir),
            "--format",
            "excellon",
            "--excellon-units",
            "mm",
            "--excellon-separate-th",
            str(pcb),
        ],
        check=False,
    )
    step_run = run(
        [
            cli,
            "pcb",
            "export",
            "step",
            "--force",
            "--board-only",
            "-o",
            str(step),
            str(pcb),
        ],
        check=False,
    )

    cpl_rows = 0
    if pos_csv.is_file():
        cpl_rows = write_jlc_cpl(pos_csv, cpl_csv)

    gerber_files = sorted(p.name for p in gerber_dir.iterdir() if p.is_file()) if gerber_dir.is_dir() else []
    bom_rows = bom_row_count(bom_csv) if bom_csv.is_file() else 0
    placed_parts = count_placed_parts(sch)

    outputs = {
        "erc.json": erc_json.is_file(),
        "drc.json": drc_json.is_file(),
        "bom.csv": bom_csv.is_file(),
        "cpl.csv": cpl_csv.is_file(),
        "elicio-v2.step": step.is_file() and step.stat().st_size > 0,
        "gerbers": len(gerber_files) > 0,
    }
    payload = {
        "erc_errors": erc_errors,
        "erc_warnings": erc_warnings,
        "drc_errors": drc_errors,
        "drc_warnings": drc_warnings,
        "unconnected_items": unconnected,
        "bom_rows": bom_rows,
        "placed_parts": placed_parts,
        "cpl_rows": cpl_rows,
        "gerber_files": gerber_files,
        "outputs": outputs,
        "commands": {
            "erc": erc.returncode,
            "drc": drc.returncode,
            "bom": bom.returncode,
            "pos": pos.returncode,
            "gerbers": gerbers.returncode,
            "drill": drill.returncode,
            "step": step_run.returncode,
        },
    }
    summary.write_text(json.dumps(payload, indent=2) + "\n")

    missing_outputs = [name for name, ok in outputs.items() if not ok]
    if erc_errors:
        sys.stderr.write(f"ERC errors: {erc_errors}\n")
        return 1
    if missing_outputs:
        sys.stderr.write("missing outputs: " + ", ".join(missing_outputs) + "\n")
        return 1
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
