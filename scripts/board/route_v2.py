#!/usr/bin/env python3
"""Repeatable WP12f route: DSN class check, Freerouting 2.4.1, SES import.

Uses KiCad's Python (pcbnew) for DSN/SES. Freerouting on OpenJDK 25.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BOARD_DIR = ROOT / "hardware" / "board"
PCB = BOARD_DIR / "elicio-v2.kicad_pcb"
BUILD = BOARD_DIR / "build_v2b.py"
KICAD_PY = Path(
    "/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3"
)
JAVA = Path("/opt/homebrew/opt/openjdk@25/bin/java")
JAR = Path.home() / ".local" / "opt" / "freerouting" / "freerouting-2.4.1.jar"

DSN_DEFAULT_WIDTH = "100"
DSN_DEFAULT_CLEAR = "100"
DSN_CONTACT_WIDTH = "150"
DSN_CONTACT_CLEAR = "200"
DSN_VIA = "Via[0-1]_700:300_um"

FREEROUTE_FLAGS = [
    "--gui.enabled=false",
    "-mp",
    "12",
    "-mt",
    "4",
    "--router.job_timeout=00:10:00",
    "--router.automatic_neckdown=false",
    "--router.strict_drc=true",
    "--router.neck_width_um=100",
    "--router.copper_to_edge_clearance_um=300",
    "--router.hole_clearance_um=200",
    "--router.fanout.enabled=true",
    "--router.fanout.max_passes=40",
    "--router.fanout.ripup_allowed=true",
]


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=check, text=True, capture_output=True)


def sanitize_dsn(path: Path) -> None:
    """Drop the 25 um smd_smd clearance (below the 0.10 mm board floor)."""
    text = path.read_text()
    text = re.sub(r"\n\s*\(clearance 25 \(type smd_smd\)\)", "", text)
    path.write_text(text)


def check_dsn_classes(path: Path) -> list[str]:
    """Return missing DSN facts. Empty list means the class blocks match §12."""
    text = path.read_text()
    missing: list[str] = []
    if not re.search(r"\(class kicad_default[\s\S]*?\(width " + DSN_DEFAULT_WIDTH + r"\)", text):
        missing.append(f"Default class width {DSN_DEFAULT_WIDTH} um")
    if not re.search(r"\(class kicad_default[\s\S]*?\(clearance " + DSN_DEFAULT_CLEAR + r"\)", text):
        missing.append(f"Default class clearance {DSN_DEFAULT_CLEAR} um")
    if not re.search(r"\(class Contact[\s\S]*?\(width " + DSN_CONTACT_WIDTH + r"\)", text):
        missing.append(f"Contact class width {DSN_CONTACT_WIDTH} um")
    if not re.search(r"\(class Contact[\s\S]*?\(clearance " + DSN_CONTACT_CLEAR + r"\)", text):
        missing.append(f"Contact class clearance {DSN_CONTACT_CLEAR} um")
    if DSN_VIA not in text:
        missing.append(DSN_VIA)
    if re.search(r"\(clearance 25 \(type smd_smd\)\)", text):
        missing.append("smd_smd clearance 25 um still present")
    return missing


def paste_dsn_rules(path: Path) -> None:
    text = path.read_text()
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("(class ") or s.startswith("(width ") or s.startswith("(clearance ") or s.startswith("(via "):
            print("DSN", s)


def export_dsn(dsn: Path) -> None:
    dsn.parent.mkdir(parents=True, exist_ok=True)
    proc = run([str(KICAD_PY), str(BUILD), "--export-dsn", str(dsn)])
    sys.stdout.write(proc.stdout)
    if proc.returncode:
        sys.stderr.write(proc.stderr)
        raise SystemExit(proc.returncode)
    sanitize_dsn(dsn)


def write_fr_home(home: Path) -> None:
    home.mkdir(parents=True, exist_ok=True)
    cfg = home / "freerouting.json"
    cfg.write_text(
        """{
  "gui": {"enabled": false, "exitWhenFinished": true},
  "router": {
    "automaticNeckdown": false,
    "strictDrc": true,
    "neckWidthUm": 100.0,
    "copperToEdgeClearanceUm": 300.0,
    "holeClearanceUm": 200.0,
    "maxPasses": 12,
    "viasAllowed": true,
    "fanout": {
      "enabled": true,
      "maxPasses": 40,
      "ripupAllowed": true
    }
  },
  "logging": {
    "console": {"enabled": true, "level": "INFO"},
    "file": {"enabled": true, "level": "INFO"}
  }
}
""",
        encoding="utf-8",
    )


def freeroute(dsn: Path, ses: Path) -> None:
    home = dsn.parent / "fr-home"
    write_fr_home(home)
    cmd = [
        str(JAVA),
        "-Djava.awt.headless=true",
        "-jar",
        str(JAR),
        f"--user_data_path={home}",
        "-de",
        str(dsn),
        "-do",
        str(ses),
        *FREEROUTE_FLAGS,
    ]
    print(" ".join(cmd))
    proc = subprocess.run(cmd, text=True)
    if proc.returncode:
        raise SystemExit(proc.returncode)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, default=Path("/tmp/wp12f"))
    parser.add_argument("--dsn-check", action="store_true")
    parser.add_argument("--route", action="store_true")
    parser.add_argument("--import-owned", action="store_true")
    args = parser.parse_args()
    work = args.work
    work.mkdir(parents=True, exist_ok=True)
    dsn = work / "elicio-v2.dsn"
    ses = work / "elicio-v2.ses"
    export_dsn(dsn)
    missing = check_dsn_classes(dsn)
    print("dsn", dsn, "bytes", dsn.stat().st_size)
    paste_dsn_rules(dsn)
    if missing:
        sys.stderr.write("DSN class check failed: " + "; ".join(missing) + "\n")
        return 1
    print("DSN class check OK: Default 100/100 um, Contact 150/200 um, via 700:300 um")
    if args.dsn_check and not args.route and not args.import_owned:
        return 0
    if args.route:
        freeroute(dsn, ses)
        copy = work / "elicio-v2-copy.kicad_pcb"
        shutil.copy2(PCB, copy)
        proc = run([str(KICAD_PY), str(BUILD), "--import-ses", str(ses), str(copy)])
        sys.stdout.write(proc.stdout)
        if proc.returncode:
            sys.stderr.write(proc.stderr)
            return proc.returncode
        print("copy pcb", copy)
        return 0
    if args.import_owned:
        if not ses.is_file():
            sys.stderr.write(f"missing {ses}\n")
            return 1
        proc = run([str(KICAD_PY), str(BUILD), "--import-ses", str(ses), str(PCB)])
        sys.stdout.write(proc.stdout)
        return proc.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
