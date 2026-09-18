#!/usr/bin/env python3
"""WP12d schematic: J1 and U5 out; P4/P5 RING_PAD charging pads on VBUS/GND."""
from __future__ import annotations

import re
import uuid
from pathlib import Path

SCH = Path(__file__).resolve().parent / "elicio-v2.kicad_sch"
OUT = {"J1", "U5"}
USB_NETS = {"USB_DP", "USB_DN"}


def _match_paren(text: str, start: int) -> int:
    depth = 0
    i = start
    while i < len(text):
        ch = text[i]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise ValueError("unbalanced sexpr")


def _symbol_ref(block: str) -> str | None:
    m = re.search(r'\(property "Reference" "([^"]+)"', block)
    return m.group(1) if m else None


def _iter_top_symbols(text: str) -> list[tuple[int, int, str]]:
    """Top-level (symbol …) instances after lib_symbols, not lib definitions."""
    lib_end = text.find("(embedded_fonts")
    if lib_end < 0:
        lib_end = text.find("\t(symbol\n\t\t(lib_id")
    start = text.find("\t(symbol\n\t\t(lib_id", lib_end if lib_end > 0 else 0)
    out: list[tuple[int, int, str]] = []
    i = start
    while i >= 0:
        if not text.startswith("\t(symbol", i):
            nxt = text.find("\t(symbol\n\t\t(lib_id", i + 1)
            i = nxt
            continue
        end = _match_paren(text, i)
        block = text[i:end]
        if "(lib_id" in block[:80]:
            out.append((i, end, block))
        i = text.find("\t(symbol\n\t\t(lib_id", end)
    return out


def _pad_instance(ref: str, value: str, x: float, y: float, net: str) -> str:
    uid = str(uuid.uuid4())
    pin_uid = str(uuid.uuid4())
    lab_uid = str(uuid.uuid4())
    return f"""	(symbol
		(lib_id "elicio:PAD_8x8")
		(at {x} {y} 0)
		(unit 1)
		(body_style 1)
		(exclude_from_sim no)
		(in_bom no)
		(on_board yes)
		(in_pos_files yes)
		(dnp no)
		(uuid "{uid}")
		(property "Reference" "{ref}"
			(at {x} {y} 0)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Value" "{value}"
			(at {x} {y} 0)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Footprint" "elicio:RING_PAD_D5_H2.7"
			(at {x} {y} 0)
			(show_name no)
			(do_not_autoplace no)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Datasheet" "~"
			(at {x} {y} 0)
			(show_name no)
			(do_not_autoplace no)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "LCSC" ""
			(at {x} {y} 0)
			(show_name no)
			(do_not_autoplace no)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(pin "1"
			(uuid "{pin_uid}")
		)
		(instances
			(project "elicio-v2"
				(path "/420b5650-2bf7-4a1a-b8d9-f0e848e2539f"
					(reference "{ref}")
					(unit 1)
				)
			)
		)
	)
	(global_label "{net}"
		(shape input)
		(at {x} {y - 6.35} 270)
		(fields_autoplaced yes)
		(effects
			(font
				(size 1.27 1.27)
			)
			(justify left)
		)
		(uuid "{lab_uid}")
	)
"""


def _replace_usb_labels(text: str) -> str:
    out: list[str] = []
    i = 0
    token = '\t(global_label "'
    while True:
        j = text.find(token, i)
        if j < 0:
            out.append(text[i:])
            break
        out.append(text[i:j])
        end = _match_paren(text, j)
        block = text[j:end]
        name_m = re.search(r'\(global_label "([^"]+)"', block)
        at_m = re.search(r"\(at ([0-9.]+) ([0-9.]+)", block)
        name = name_m.group(1) if name_m else ""
        if name in USB_NETS and at_m:
            uid = str(uuid.uuid4())
            out.append(
                f'\t(no_connect\n\t\t(at {at_m.group(1)} {at_m.group(2)})\n'
                f'\t\t(uuid "{uid}")\n\t)\n'
            )
        else:
            out.append(block)
        i = end
    return "".join(out)


def patch() -> None:
    text = SCH.read_text()
    if '(property "Reference" "P4"' in text:
        print("already patched", SCH)
        return
    text = text.replace(
        "WP12 board v2. Interface II flex, packing A_501015_series_w20. Schematic contract unchanged. Not for order.",
        "WP12d board v2d. No USB-C receptacle (Q81). P4/P5 tail pads feed VBUS/GND. D1 PESD on VBUS. Not for order.",
    )
    symbols = _iter_top_symbols(text)
    drop: list[tuple[int, int]] = []
    for start, end, block in symbols:
        ref = _symbol_ref(block)
        if ref in OUT:
            drop.append((start, end))
    for start, end in reversed(drop):
        text = text[:start] + text[end:]
    insert_at = text.find('\t(property "Reference" "P3"')
    if insert_at < 0:
        raise SystemExit("P3 not found")
    # After the P3 symbol + REF label: find the next Device:R (R1).
    r1 = text.find('\t(symbol\n\t\t(lib_id "Device:R")', insert_at)
    if r1 < 0:
        raise SystemExit("R1 not found after P3")
    pads = _pad_instance("P4", "CHARGE_VBUS", 279.4, 50.8, "VBUS")
    pads += _pad_instance("P5", "CHARGE_GND", 279.4, 76.2, "GND")
    text = text[:r1] + pads + text[r1:]
    text = _replace_usb_labels(text)
    SCH.write_text(text)
    print("patched", SCH)


if __name__ == "__main__":
    patch()
