#!/usr/bin/env python3
"""WP12i board-owned edits on the existing copper. Does not wipe tracks."""
from __future__ import annotations

from pathlib import Path

import wx

_APP = wx.App(False)

import pcbnew  # noqa: E402

from build_v2b import (  # noqa: E402
    BOARD_DIR,
    apply_u2_rsm_land,
    draw_q94_stiffeners,
    remove_dnp_footprints,
)


def main() -> None:
    pcb_path = BOARD_DIR / "elicio-v2.kicad_pcb"
    board = pcbnew.LoadBoard(str(pcb_path))
    ntracks = len([t for t in board.GetTracks() if t.GetClass() in {"PCB_TRACK", "PCB_ARC"}])
    refs = {fp.GetReference() for fp in board.GetFootprints()}
    if "U2" in refs:
        apply_u2_rsm_land(board)
    gone: list[str] = []
    if {"R9", "R10"} & refs:
        gone = remove_dnp_footprints(board, {"R9", "R10"})
        board.SetFileName(str(pcb_path))
        board.Save(str(pcb_path))
        board = pcbnew.LoadBoard(str(pcb_path))
        ntracks = len([t for t in board.GetTracks() if t.GetClass() in {"PCB_TRACK", "PCB_ARC"}])
    nstiff = draw_q94_stiffeners(board)
    board.SetFileName(str(pcb_path))
    board.Save(str(pcb_path))
    saved = pcb_path.read_text(encoding="utf-8")
    saved_tracks = saved.count("\n\t(segment") + saved.count("\n\t(arc")
    print("removed", sorted(gone), "stiffeners", nstiff, "tracks", ntracks, "->", saved_tracks)
    if saved_tracks != ntracks:
        raise SystemExit("track count changed; refuse to keep the save")


if __name__ == "__main__":
    main()
