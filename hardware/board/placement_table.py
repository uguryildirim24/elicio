"""Parse a packing placement table with a copper side column.

§5c uses columns ``ref | side | u | s | rot | courtyard | notes``.
This parser takes a ``side`` column of ``top`` or ``bottom`` so WP12d can pin
two-sided rows. ``face`` is accepted as an alias only when its cell is
``top`` or ``bottom`` (pocket/floor are regions, not copper sides).
"""
from __future__ import annotations

from dataclasses import dataclass

SIDES = frozenset({"top", "bottom"})


@dataclass(frozen=True)
class PlacementRow:
    ref: str
    u: float
    s: float
    rot: float
    side: str


def normalize_side(raw: str) -> str:
    value = raw.strip().lower()
    if value not in SIDES:
        raise ValueError(f"side must be top or bottom, got {raw!r}")
    return value


def _cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _is_separator(line: str) -> bool:
    body = line.replace("|", "").replace(":", "").replace("-", "").replace(" ", "")
    return body == ""


def parse_placement_markdown(text: str) -> list[PlacementRow]:
    """Return rows from a markdown table that pins packing (u, s) and side."""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip().startswith("|")]
    if len(lines) < 2:
        raise ValueError("placement table needs a header and at least one row")
    header = [cell.lower() for cell in _cells(lines[0])]
    needed = {"ref", "u", "s"}
    if not needed.issubset(header):
        raise ValueError(f"placement table needs columns {sorted(needed)}, got {header}")
    rows: list[PlacementRow] = []
    for line in lines[1:]:
        if _is_separator(line):
            continue
        cells = _cells(line)
        rec = {key: cells[i] if i < len(cells) else "" for i, key in enumerate(header)}
        ref = rec.get("ref", "").strip()
        if not ref or ref.lower() == "ref":
            continue
        side_raw = rec.get("side") or rec.get("face") or "top"
        if side_raw.strip().lower() in SIDES:
            side = normalize_side(side_raw)
        else:
            side = "top"
        rows.append(
            PlacementRow(
                ref=ref,
                u=float(rec["u"]),
                s=float(rec["s"]),
                rot=float(rec.get("rot") or 0.0),
                side=side,
            )
        )
    return rows


def wants_back_copper(row: PlacementRow) -> bool:
    """True when the row must sit on B.Cu (KiCad flipped footprint)."""
    return row.side == "bottom"
