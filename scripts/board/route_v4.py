#!/usr/bin/env python3
"""elicio-v4 route: DSN export and class check, Freerouting 2.4.1, SES import.

Locked pre-routes (Contact strips and branches, charge runs, nRESET, +VDD)
export as fixed wires, so Freerouting routes around them. One router at
a time, with the heap capped at 4 GB.

  route_v4.py --work DIR --dsn-check     export and check the DSN only
  route_v4.py --work DIR --route         route, import into a copy in DIR
  route_v4.py --work DIR --import-owned  import DIR/elicio-v4.ses into the board
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

from route_v2 import FREEROUTE_FLAGS, JAR, JAVA, KICAD_PY, paste_dsn_rules, run, sanitize_dsn

ROOT = Path(__file__).resolve().parents[2]
BOARD_DIR = ROOT / "hardware" / "board"
PCB = BOARD_DIR / "elicio-v4.kicad_pcb"
BUILD = BOARD_DIR / "build_v4.py"

DSN_VIA = "Via[0-1]_400:150_um"
CLASSES = {"kicad_default": ("100", "100"), "Contact": ("150", "200")}


def check_dsn(path: Path) -> list[str]:
    text = path.read_text()
    missing: list[str] = []
    for name, (width, clear) in CLASSES.items():
        rule = re.search(r"\(class " + name + r"\s[\s\S]*?\(circuit\s*\(use_via [^)]*\)\s*\)\s*\(rule\s*"
                         r"\(width (\d+)\)\s*\(clearance (\d+)\)", text)
        if not rule or rule.groups() != (width, clear):
            missing.append(f"{name} {width}/{clear} um (found {rule.groups() if rule else None})")
    if DSN_VIA not in text:
        missing.append(DSN_VIA)
    if "(type fix)" not in text:
        missing.append("locked pre-routes as fixed wires")
    return missing


def kicad(*args: str) -> None:
    proc = run([str(KICAD_PY), str(BUILD), *args], check=False)
    sys.stdout.write("\n".join(line for line in proc.stdout.splitlines() if "Debug:" not in line) + "\n")
    if proc.returncode:
        sys.stderr.write(proc.stderr[-2000:])
        raise SystemExit(proc.returncode)


# Freerouting's defaults allow analytics and telemetry; this job contacts no one.
PRIVATE_FLAGS = ["--usage_and_diagnostic_data.disable_analytics=true", "--profile.allow_telemetry=false"]


def freeroute(dsn: Path, ses: Path, passes: int) -> None:
    home = dsn.parent / "fr-home"
    home.mkdir(parents=True, exist_ok=True)
    flags = list(FREEROUTE_FLAGS)
    flags[flags.index("-mp") + 1] = str(passes)
    flags = [f if not f.startswith("--router.job_timeout=") else "--router.job_timeout=00:40:00" for f in flags]
    cmd = [str(JAVA), "-Djava.awt.headless=true", "-Xmx4g", "-jar", str(JAR), f"--user_data_path={home}",
           "-de", str(dsn), "-do", str(ses), *flags, *PRIVATE_FLAGS]
    print(" ".join(cmd), flush=True)
    if subprocess.run(cmd, text=True).returncode:
        raise SystemExit("freerouting failed")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--dsn-check", action="store_true")
    parser.add_argument("--route", action="store_true")
    parser.add_argument("--import-owned", action="store_true")
    parser.add_argument("--passes", type=int, default=20)
    args = parser.parse_args()
    work = args.work.resolve()
    work.mkdir(parents=True, exist_ok=True)
    dsn, ses = work / "elicio-v4.dsn", work / "elicio-v4.ses"
    if args.import_owned:
        if not ses.is_file():
            sys.stderr.write(f"missing {ses}\n")
            return 1
        kicad("--import-ses", str(ses))
        return 0
    kicad("--export-dsn", str(dsn))
    sanitize_dsn(dsn)
    paste_dsn_rules(dsn)
    missing = check_dsn(dsn)
    if missing:
        sys.stderr.write("DSN check failed: " + "; ".join(missing) + "\n")
        return 1
    print("DSN check OK: Default 100/100 um, Contact 150/200 um, via 400:150 um, pre-routes fixed")
    if args.route:
        freeroute(dsn, ses, args.passes)
        copy = work / "elicio-v4.kicad_pcb"
        for suffix in (".kicad_pcb", ".kicad_pro", ".kicad_dru"):
            src = PCB.with_suffix(suffix)
            if src.is_file():
                shutil.copy2(src, copy.with_suffix(suffix))
        kicad("--import-ses", str(ses), str(copy))
        print("routed copy", copy)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
