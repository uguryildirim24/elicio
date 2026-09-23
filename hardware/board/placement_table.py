"""Parse packing pin tables with a copper side column.

§5c uses ``ref | side | u | s | rot``. Pin table v2 is the same plus a
folded-site table (ignored) and J4 hole keep-outs. Pin table v3 is §5e:
66 rows (R9/R10 out) plus channel keep-out rows. ``face`` is an alias
only when its cell is ``top`` or ``bottom`` (pocket/floor are regions).
Flat PCB columns ``x`` / ``y`` alias ``u`` / ``s``.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

SIDES = frozenset({"top", "bottom"})
BACK_LAYERS = frozenset({"both", "bottom", "b.cu", "bcu", "*.cu"})


@dataclass(frozen=True)
class PlacementRow:
    ref: str
    u: float
    s: float
    rot: float
    side: str


@dataclass(frozen=True)
class KeepoutZone:
    """Named keep-out for J4 holes (and any later both-side hole zone)."""

    name: str
    u: float
    s: float
    radius: float
    layers: str


@dataclass(frozen=True)
class ChannelBox:
    """Q98 routing channel as a rectangle in packing (u, s)."""

    name: str
    u0: float
    s0: float
    u1: float
    s1: float


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


def _heading_before(lines: list[str], idx: int) -> str:
    for i in range(idx - 1, -1, -1):
        raw = lines[i].strip()
        if not raw:
            continue
        if raw.startswith("|"):
            continue
        return raw.lstrip("#").strip().lower()
    return ""


def iter_markdown_tables(text: str) -> list[tuple[str, list[str], list[list[str]]]]:
    """Return (heading, header_cells, data_rows) for each markdown table."""
    lines = text.splitlines()
    tables: list[tuple[str, list[str], list[list[str]]]] = []
    i = 0
    while i < len(lines):
        if not lines[i].strip().startswith("|"):
            i += 1
            continue
        heading = _heading_before(lines, i)
        block: list[str] = []
        while i < len(lines) and lines[i].strip().startswith("|"):
            block.append(lines[i].strip())
            i += 1
        if len(block) < 2:
            continue
        header = [c.lower() for c in _cells(block[0])]
        rows: list[list[str]] = []
        for line in block[1:]:
            if _is_separator(line):
                continue
            rows.append(_cells(line))
        tables.append((heading, header, rows))
    return tables


def _is_folded_table(heading: str, header: list[str]) -> bool:
    if header and header[0] in {"pad", "net"}:
        return True
    keys = set(header)
    return "y" in keys and "u" in keys and "s" in keys and "rot" not in keys


def _is_keepout_table(heading: str, header: list[str]) -> bool:
    blob = heading + " " + " ".join(header)
    if "keep-out" in blob or "keepout" in blob:
        return True
    if "j4" in blob and "hole" in blob:
        return True
    keys = set(header)
    if {"u0", "s0", "u1", "s1"} <= keys:
        return True
    if "keep" in keys and "drill" in keys:
        return True
    return "radius" in keys or ("clearance" in keys and "diameter" in keys)


def _is_pin_table(header: list[str]) -> bool:
    keys = set(header)
    has_xy = ("u" in keys and "s" in keys) or ("x" in keys and "y" in keys)
    return "ref" in keys and has_xy


def _coord(rec: dict[str, str], *names: str) -> str:
    for name in names:
        value = rec.get(name, "").strip()
        if value:
            return value
    return ""


def _row_from_rec(rec: dict[str, str]) -> PlacementRow | None:
    ref = rec.get("ref", "").strip()
    if not ref or ref.lower() == "ref":
        return None
    u_raw = _coord(rec, "u", "x")
    s_raw = _coord(rec, "s", "y")
    if not u_raw or not s_raw:
        return None
    side_raw = rec.get("side") or rec.get("face") or "top"
    if side_raw.strip().lower() in SIDES:
        side = normalize_side(side_raw)
    else:
        side = "top"
    return PlacementRow(
        ref=ref,
        u=float(u_raw),
        s=float(s_raw),
        rot=float(rec.get("rot") or 0.0),
        side=side,
    )


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
        row = _row_from_rec(rec)
        if row is not None:
            rows.append(row)
    return rows


def parse_pin_table_v2(text: str) -> list[PlacementRow]:
    """Flat-coordinate pin table. Skip the folded shell-site table."""
    rows: list[PlacementRow] = []
    for heading, header, data in iter_markdown_tables(text):
        if not _is_pin_table(header):
            continue
        if _is_folded_table(heading, header):
            continue
        for cells in data:
            rec = {key: cells[i] if i < len(cells) else "" for i, key in enumerate(header)}
            row = _row_from_rec(rec)
            if row is not None:
                rows.append(row)
    if not rows:
        raise ValueError("pin table v2 has no flat-coordinate footprint rows")
    return rows


def parse_j4_keepouts(text: str) -> list[KeepoutZone]:
    """J4 NPTH keep-outs: centre plus radius, both sides unless stated."""
    zones: list[KeepoutZone] = []
    for heading, header, data in iter_markdown_tables(text):
        if not _is_keepout_table(heading, header):
            continue
        keys = set(header)
        if "ref" in keys and "hole" not in keys:
            continue
        for cells in data:
            rec = {key: cells[i] if i < len(cells) else "" for i, key in enumerate(header)}
            name = (rec.get("name") or rec.get("hole") or rec.get("keepout") or rec.get("ref") or "j4_holes").strip()
            if not name or name.lower() in {"name", "hole", "keepout", "ref"}:
                continue
            layers = (rec.get("layers") or rec.get("sides") or rec.get("side") or "both").strip().lower()
            if {"u0", "s0", "u1", "s1"} <= keys:
                u0, s0, u1, s1 = (float(rec[k]) for k in ("u0", "s0", "u1", "s1"))
                zones.append(
                    KeepoutZone(
                        name=name,
                        u=(u0 + u1) / 2,
                        s=(s0 + s1) / 2,
                        radius=max(abs(u1 - u0), abs(s1 - s0)) / 2,
                        layers=layers,
                    )
                )
                continue
            u_raw = _coord(rec, "u", "x")
            s_raw = _coord(rec, "s", "y")
            if not u_raw or not s_raw:
                continue
            if rec.get("keep"):
                radius = float(rec["keep"]) / 2.0
            elif rec.get("radius"):
                radius = float(rec["radius"])
            else:
                diameter = float(rec.get("diameter") or rec.get("drill") or 0.0)
                clearance = float(rec.get("clearance") or 0.0)
                radius = diameter / 2.0 + clearance
            zones.append(
                KeepoutZone(name=name, u=float(u_raw), s=float(s_raw), radius=radius, layers=layers)
            )
    return zones


def forbids_back_copper(zone: KeepoutZone) -> bool:
    """True when the keep-out bans B.Cu footprints (J4 holes, both sides)."""
    blob = zone.layers.replace(" ", "")
    if "b.cu" in blob:
        return True
    return blob in BACK_LAYERS


def _section_from(text: str, *markers: str) -> str | None:
    lower = text.lower()
    for marker in markers:
        idx = lower.find(marker.lower())
        if idx < 0:
            continue
        rest = text[idx:]
        nxt = rest.find("\n## ", 4)
        if nxt < 0:
            nxt = rest.find("\n# ", 4)
        return rest if nxt < 0 else rest[:nxt]
    return None


def extract_section5e(text: str) -> str | None:
    """Return packing-v2.md §5e (pin table v3) or None if it has not landed."""
    return _section_from(
        text,
        "## 5e",
        "### 5e",
        "### pin table v3",
        "## pin table v3",
    )


def parse_pin_table_v3(text: str) -> list[PlacementRow]:
    """§5e pin table v3. Same columns as v2; 66 footprint rows when complete."""
    section = extract_section5e(text) or text
    rows = parse_pin_table_v2(section)
    if not rows:
        raise ValueError("pin table v3 has no flat-coordinate footprint rows")
    return rows


def _channel_box_from_rec(rec: dict[str, str], keys: set[str]) -> tuple[float, float, float, float] | None:
    for u0k, s0k, u1k, s1k in (
        ("u0", "s0", "u1", "s1"),
        ("u_min", "s_min", "u_max", "s_max"),
    ):
        if {u0k, s0k, u1k, s1k} <= keys:
            u0, s0, u1, s1 = (float(rec[k]) for k in (u0k, s0k, u1k, s1k))
            return (min(u0, u1), min(s0, s1), max(u0, u1), max(s0, s1))
    u_raw = _coord(rec, "u", "x")
    s_raw = _coord(rec, "s", "y")
    if not u_raw or not s_raw:
        return None
    if rec.get("width") and rec.get("height"):
        w, h = float(rec["width"]), float(rec["height"])
        u, s = float(u_raw), float(s_raw)
        return (u - w / 2.0, s - h / 2.0, u + w / 2.0, s + h / 2.0)
    return None


def parse_channel_keepouts(text: str) -> list[ChannelBox]:
    """Q98 channel rows in §5e: heading contains channel or Q98."""
    section = extract_section5e(text) or text
    zones: list[ChannelBox] = []
    for heading, header, data in iter_markdown_tables(section):
        blob = heading + " " + " ".join(header)
        if "channel" not in blob and "q98" not in blob:
            continue
        keys = set(header)
        for cells in data:
            rec = {key: cells[i] if i < len(cells) else "" for i, key in enumerate(header)}
            name = (rec.get("name") or rec.get("channel") or rec.get("keepout") or rec.get("ref") or "").strip()
            if not name or name.lower() in {"name", "channel", "keepout", "ref"}:
                continue
            box = _channel_box_from_rec(rec, keys)
            if box is None:
                continue
            zones.append(ChannelBox(name=name, u0=box[0], s0=box[1], u1=box[2], s1=box[3]))
    return zones


def vendor_pin_table(packing_doc: str, dest: Path, source_sha: str = "") -> bool:
    """Write packing_v2_flat.md from §5e when that section exists. Return True if written."""
    section = extract_section5e(packing_doc)
    if section is None:
        return False
    rows = parse_pin_table_v3(packing_doc)
    if len(rows) < 66:
        raise ValueError(f"pin table v3 has {len(rows)} rows, need 66")
    header = (
        "# Pin table v3 — flat PCB coordinates (WP12i)\n\n"
        "Copied from packing-v2.md §5e"
        + (f" at `{source_sha}`" if source_sha else "")
        + ".\n"
        "Board pins this table. The folded-site table is the shell's and is not copied.\n"
        "§5d in packing-v2.md is the frozen v2.1 table. §5e is live.\n\n"
    )
    dest.write_text(header + section.strip() + "\n", encoding="utf-8")
    return True


def wants_back_copper(row: PlacementRow) -> bool:
    """True when the row must sit on B.Cu (KiCad flipped footprint)."""
    return row.side == "bottom"
