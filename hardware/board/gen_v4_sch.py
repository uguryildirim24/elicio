#!/usr/bin/env python3
"""Write elicio-v4.kicad_sch (and the v4 project files) from v4_parts.py.

Library symbols: every elicio:* symbol comes from lib/elicio.kicad_sym
(make_v4_lib.lib_blocks); stock KiCad symbols come from the blocks already
embedded in elicio-v2.kicad_sch, which pass ERC with no lib_symbol_mismatch.

Run: python3 hardware/board/gen_v4_sch.py  (then kicad-cli sch erc)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from make_v4_lib import lib_blocks  # noqa: E402
from sch_gen import write_schematic  # noqa: E402
from sexpr_util import lib_symbol_blocks  # noqa: E402
from v4_parts import parts  # noqa: E402

V2 = HERE / "elicio-v2"
V4 = HERE / "elicio-v4"


def blocks() -> dict[str, str]:
    v2 = lib_symbol_blocks((V2.with_suffix(".kicad_sch")).read_text(encoding="utf-8"), "lib_symbols")
    out = {k: v for k, v in v2.items() if not k.startswith("elicio:")}
    out.update(lib_blocks())
    return out


def write_project() -> None:
    pro = json.loads(V2.with_suffix(".kicad_pro").read_text(encoding="utf-8"))
    pro["meta"]["filename"] = "elicio-v4.kicad_pro"
    V4.with_suffix(".kicad_pro").write_text(json.dumps(pro, indent=2) + "\n", encoding="utf-8")
    dru = V2.with_suffix(".kicad_dru").read_text(encoding="utf-8")
    V4.with_suffix(".kicad_dru").write_text(dru, encoding="utf-8")


def main() -> None:
    write_project()
    write_schematic(
        V4.with_suffix(".kicad_sch"),
        "elicio-v4",
        "Elicio board v4 (ISP1807, W17 body)",
        "Design record docs/fab/board-v4-design.md. Not for order.",
        parts(),
        blocks(),
    )
    print("wrote", V4.with_suffix(".kicad_sch"))


if __name__ == "__main__":
    main()
