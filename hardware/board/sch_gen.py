"""Write a flat, label-connected KiCad 10 schematic from a part list.

Every pin end gets a global label with its net name (as in elicio-v2); an
unconnected pin gets a no-connect flag. Library symbols are embedded exactly
as the libraries hold them, so ERC sees no lib_symbol_mismatch.
"""
from __future__ import annotations

import re
import uuid
from dataclasses import dataclass, field

PIN_RE = re.compile(
    r'\(pin (\w+) (\w+)\s*\(at ([-\d.]+) ([-\d.]+) (\d+)\)\s*\(length ([\d.]+)\)'
    r'[\s\S]*?\(name "([^"]*)"[\s\S]*?\(number "([^"]*)"'
)


@dataclass(frozen=True, slots=True)
class Part:
    ref: str
    lib_id: str
    value: str
    footprint: str
    nets: dict[str, str | None]
    lcsc: str = ""
    mpn: str = ""
    in_bom: bool = True
    on_board: bool = True
    dnp: bool = False
    note: str = ""


@dataclass(slots=True)
class SymPin:
    number: str
    name: str
    etype: str
    x: float
    y: float
    angle: int


@dataclass(slots=True)
class Placed:
    part: Part
    x: float
    y: float
    pins: list[SymPin] = field(default_factory=list)


def symbol_pins(block: str) -> list[SymPin]:
    return [
        SymPin(num, name, etype, float(x), float(y), int(ang))
        for etype, _shape, x, y, ang, _ln, name, num in PIN_RE.findall(block)
    ]


def _uid() -> str:
    return str(uuid.uuid4())


def _prop(name: str, value: str, x: float, y: float, hide: bool) -> str:
    hide_s = "\n\t\t\t(hide yes)" if hide else ""
    return f"""		(property "{name}" "{value}"
			(at {x:.2f} {y:.2f} 0)
			(show_name no)
			(do_not_autoplace no){hide_s}
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
"""


def symbol_instance(p: Placed, project: str, root: str) -> str:
    part = p.part
    yn = lambda b: "yes" if b else "no"  # noqa: E731
    props = _prop("Reference", part.ref, p.x, p.y - 2.54, False)
    props += _prop("Value", part.value, p.x, p.y + 2.54, False)
    props += _prop("Footprint", part.footprint, p.x, p.y, True)
    props += _prop("Datasheet", "~", p.x, p.y, True)
    props += _prop("LCSC", part.lcsc, p.x, p.y, True)
    if part.mpn:
        props += _prop("MPN", part.mpn, p.x, p.y, True)
    pins = "".join(
        f"""		(pin "{sp.number}"
			(uuid "{_uid()}")
		)
"""
        for sp in p.pins
    )
    return f"""	(symbol
		(lib_id "{part.lib_id}")
		(at {p.x:.2f} {p.y:.2f} 0)
		(unit 1)
		(body_style 1)
		(exclude_from_sim no)
		(in_bom {yn(part.in_bom)})
		(on_board {yn(part.on_board)})
		(in_pos_files yes)
		(dnp {yn(part.dnp)})
		(uuid "{_uid()}")
{props}{pins}		(instances
			(project "{project}"
				(path "/{root}"
					(reference "{part.ref}")
					(unit 1)
				)
			)
		)
	)
"""


def global_label(net: str, x: float, y: float, angle: int) -> str:
    return f"""	(global_label "{net}"
		(shape input)
		(at {x:.2f} {y:.2f} {angle})
		(fields_autoplaced yes)
		(effects
			(font
				(size 1.27 1.27)
			)
			(justify left)
		)
		(uuid "{_uid()}")
	)
"""


def no_connect(x: float, y: float) -> str:
    return f"""	(no_connect
		(at {x:.2f} {y:.2f})
		(uuid "{_uid()}")
	)
"""


def layout(parts: list[Part], lib_blocks: dict[str, str], width: float = 540.0) -> list[Placed]:
    """Shelf-pack symbols left to right with room for labels; no two pin ends meet."""
    placed: list[Placed] = []
    x0, y0 = 25.4, 25.4
    x, y, row_h = x0, y0, 0.0
    for part in parts:
        pins = symbol_pins(lib_blocks[part.lib_id])
        xs = [sp.x for sp in pins] or [0.0]
        ys = [-sp.y for sp in pins] or [0.0]
        margin = 22.86  # label text room on each side
        w = (max(xs) - min(xs)) + 2 * margin
        h = (max(ys) - min(ys)) + 2 * 12.7
        if x + w > width:
            x = x0
            y += row_h
            row_h = 0.0
        cx = round((x + margin - min(xs)) / 2.54) * 2.54
        cy = round((y + 12.7 - min(ys)) / 2.54) * 2.54
        placed.append(Placed(part, cx, cy, pins))
        x += w
        row_h = max(row_h, h)
    ends: dict[tuple[float, float], str] = {}
    for pl in placed:
        for sp in pl.pins:
            key = (round(pl.x + sp.x, 2), round(pl.y - sp.y, 2))
            if key in ends:
                raise ValueError(f"pin ends meet: {pl.part.ref}.{sp.number} and {ends[key]}")
            ends[key] = f"{pl.part.ref}.{sp.number}"
    return placed


def write_schematic(
    path,
    project: str,
    title: str,
    comment: str,
    parts: list[Part],
    lib_blocks: dict[str, str],
    paper: str = "A1",
    date: str = "2026-09-23",
) -> None:
    root = _uid()
    used = []
    for part in parts:
        if part.lib_id not in used:
            used.append(part.lib_id)
    missing = [u for u in used if u not in lib_blocks]
    if missing:
        raise KeyError("library symbols missing: " + ", ".join(missing))
    placed = layout(parts, lib_blocks)
    body = []
    for pl in placed:
        pin_nums = {sp.number for sp in pl.pins}
        extra = set(pl.part.nets) - pin_nums
        if extra:
            raise KeyError(f"{pl.part.ref}: nets on unknown pins {sorted(extra)}")
        missing_pins = pin_nums - set(pl.part.nets)
        if missing_pins:
            raise KeyError(f"{pl.part.ref}: pins without a net or None: {sorted(missing_pins)}")
        body.append(symbol_instance(pl, project, root))
        for sp in pl.pins:
            ax, ay = pl.x + sp.x, pl.y - sp.y
            net = pl.part.nets[sp.number]
            if net is None:
                body.append(no_connect(ax, ay))
            else:
                body.append(global_label(net, ax, ay, sp.angle))
    libs = "".join("\t" + lib_blocks[u].rstrip() + "\n" for u in used)
    text = f"""(kicad_sch
	(version 20260306)
	(generator "eeschema")
	(generator_version "10.0")
	(uuid "{root}")
	(paper "{paper}")
	(title_block
		(title "{title}")
		(date "{date}")
		(rev "0")
		(comment 1 "{comment}")
	)
	(lib_symbols
{libs}	)
{''.join(body)}	(embedded_fonts no)
	(sheet_instances
		(path "/"
			(page "1")
		)
	)
)
"""
    from pathlib import Path

    Path(path).write_text(text, encoding="utf-8")


def box_symbol(
    lib: str,
    name: str,
    ref_prefix: str,
    description: str,
    left: list[tuple[str, str, str]],
    right: list[tuple[str, str, str]],
    footprint: str = "",
    bottom: list[tuple[str, str, str]] | None = None,
) -> str:
    """A rectangle symbol; each pin is (number, name, electrical type)."""
    bottom = bottom or []
    rows = max(len(left), len(right), 1)
    half_h = (rows + 1) * 2.54 / 2
    half_h = round(half_h / 2.54 + 0.5) * 2.54
    half_w = 12.7 if max((len(p[1]) for p in left + right), default=4) < 8 else 17.78
    if bottom:
        half_w = max(half_w, (len(bottom) + 1) * 2.54 / 2 + 2.54)
        half_w = round(half_w / 2.54 + 0.5) * 2.54
    pins = []

    def pin(num, pname, etype, x, y, ang):
        pins.append(
            f"""			(pin {etype} line
				(at {x:.2f} {y:.2f} {ang})
				(length 2.54)
				(name "{pname}"
					(effects
						(font
							(size 1.016 1.016)
						)
					)
				)
				(number "{num}"
					(effects
						(font
							(size 1.016 1.016)
						)
					)
				)
			)
"""
        )

    top = half_h - 2.54
    for i, (num, pname, etype) in enumerate(left):
        pin(num, pname, etype, -half_w - 2.54, top - i * 2.54, 0)
    for i, (num, pname, etype) in enumerate(right):
        pin(num, pname, etype, half_w + 2.54, top - i * 2.54, 180)
    for i, (num, pname, etype) in enumerate(bottom):
        pin(num, pname, etype, -half_w + 2.54 + i * 2.54, -half_h - 2.54, 90)

    def p(pname, val, y, hide):
        hide_s = "\n\t\t\t(hide yes)" if hide else ""
        return f"""		(property "{pname}" "{val}"
			(at 0 {y:.2f} 0)
			(show_name no)
			(do_not_autoplace no){hide_s}
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
"""

    full = f"{lib}:{name}" if lib else name
    return (
        f"""(symbol "{full}"
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(in_pos_files yes)
		(duplicate_pin_numbers_are_jumpers no)
"""
        + p("Reference", ref_prefix, half_h + 1.27, False)
        + p("Value", name, -half_h - 1.27 - (5.08 if bottom else 0), False)
        + p("Footprint", footprint, 0, True)
        + p("Datasheet", "", 0, True)
        + p("Description", description, 0, True)
        + f"""		(symbol "{name}_0_1"
			(rectangle
				(start {-half_w:.2f} {half_h:.2f})
				(end {half_w:.2f} {-half_h:.2f})
				(stroke
					(width 0.254)
					(type default)
				)
				(fill
					(type background)
				)
			)
		)
		(symbol "{name}_1_1"
{''.join(pins)}		)
		(embedded_fonts no)
	)"""
    )
