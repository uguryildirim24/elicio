#!/usr/bin/env python3
"""WP12b schematic edits: Q68 ADS decoupling and LCSC fills (2026-09-17 pages)."""
from __future__ import annotations

import re
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCH = ROOT / "hardware" / "board" / "elicio-v2.kicad_sch"

# Pages re-read 2026-09-17 on jlcpcb.com/partdetail/<id> after L7 §4.1.
# L7 SKUs that did not match the page are not used (see board-v2.md §13).
LCSC = {
    "C2": "C1524",  # 10 nF 0402 X7R; L7 §4.1. JLC page: Extended, not Basic
    "C6": "C19702",  # 10 µF 0603 Q68
    "C7": "C14663",  # 100 nF 0603 Q68
    "C8": "C19702",
    "C9": "C19702",
    "C11": "C1525",  # 100 nF 0402 Basic
    "C12": "C1525",
    "C15": "C14663",
    "J2": "C160402",  # SM02B-SRSS-TB 2P; C160404 is 4P (L7 §4.1, page)
    "R1": "C881401",  # 220 kΩ 0402; L7 C18001/C25768 fail the page
    "R2": "C881401",
    "R3": "C881401",
    "R4": "C26083",  # 1 MΩ 0402 Basic; L7 C15609 empty on JLC
    "R5": "C25744",  # 10 kΩ 0402 Basic; C25792 is 47 kΩ
    "R6": "C25744",
    "R7": "C25744",
    "R8": "C25744",
    "R11": "C25917",  # 6.80 kΩ 0402; C25848 is 8.2 kΩ 0201
    "R12": "C966759",  # 6.04 kΩ 0402; C25841 is 2.2 kΩ 0201
    "R13": "C25744",
    "R14": "C25741",  # 100 kΩ 0402 Basic; L7 C25744 is 10 kΩ
    "R15": "C25741",
    "R16": "C25741",
    "R17": "C26083",
    "R18": "C25792",  # 47 kΩ 0402 Basic; C25780 is 348 kΩ
    "R20": "C26083",
    "R21": "C26083",
    "R22": "C11702",  # 1 kΩ 0402 Basic; L7 C15672 empty on JLC
    "R23": "C25741",
    "R24": "C25741",
    "R25": "C25744",
    "R26": "C25744",
    "R27": "C25744",
    "R28": "C25744",
    "R29": "C26082",  # 10 MΩ DNP; was C25741 100 kΩ
    "R30": "C26082",
}

Q68_CAPS = {
    "C6": ("10uF", "Capacitor_SMD:C_0603_1608Metric"),
    "C7": ("100nF", "Capacitor_SMD:C_0603_1608Metric"),
    "C8": ("10uF", "Capacitor_SMD:C_0603_1608Metric"),
}

C15_BLOCK = """	(symbol
		(lib_id "Device:C")
		(at 165.1 177.8 0)
		(unit 1)
		(body_style 1)
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(in_pos_files yes)
		(dnp no)
		(uuid "{uuid_sym}")
		(property "Reference" "C15"
			(at 165.1 177.8 0)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Value" "100nF"
			(at 165.1 177.8 0)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Footprint" "Capacitor_SMD:C_0603_1608Metric"
			(at 165.1 177.8 0)
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
			(at 165.1 177.8 0)
			(show_name no)
			(do_not_autoplace no)
			(hide yes)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "LCSC" "C14663"
			(at 165.1 177.8 0)
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
			(uuid "{uuid_p1}")
		)
		(pin "2"
			(uuid "{uuid_p2}")
		)
		(instances
			(project "elicio-v2"
				(path "/420b5650-2bf7-4a1a-b8d9-f0e848e2539f"
					(reference "C15")
					(unit 1)
				)
			)
		)
	)
	(global_label "+3V0"
		(shape input)
		(at 165.1 173.99 270)
		(fields_autoplaced yes)
		(effects
			(font
				(size 1.27 1.27)
			)
			(justify left)
		)
		(uuid "{uuid_l1}")
	)
	(global_label "GND"
		(shape input)
		(at 165.1 181.61 90)
		(fields_autoplaced yes)
		(effects
			(font
				(size 1.27 1.27)
			)
			(justify left)
		)
		(uuid "{uuid_l2}")
	)
"""


def patch_symbol_props(text: str, ref: str, *, value: str | None = None, footprint: str | None = None, lcsc: str | None = None) -> str:
    pattern = rf'(\(symbol\n\t\t\(lib_id "Device:C"\)|\(symbol\n\t\t\(lib_id "Device:R"\))[\s\S]*?\(property "Reference" "{ref}"[\s\S]*?\n\t\)\n'
    # Too greedy across symbols. Split on "(symbol\n" and edit the matching block.

    parts = text.split("\n\t(symbol\n")
    out = [parts[0]]
    for i, part in enumerate(parts[1:], 1):
        block = "\n\t(symbol\n" + part
        # Only the first property Reference in the block.
        m = re.search(r'\(property "Reference" "([^"]+)"', block)
        if m and m.group(1) == ref:
            if value is not None:
                block = re.sub(
                    r'\(property "Value" "[^"]*"',
                    f'(property "Value" "{value}"',
                    block,
                    count=1,
                )
            if footprint is not None:
                block = re.sub(
                    r'\(property "Footprint" "[^"]*"',
                    f'(property "Footprint" "{footprint}"',
                    block,
                    count=1,
                )
            if lcsc is not None:
                block = re.sub(
                    r'\(property "LCSC" "[^"]*"',
                    f'(property "LCSC" "{lcsc}"',
                    block,
                    count=1,
                )
        out.append(block[len("\n\t(symbol\n") :] if i else block)
    # reconstruct
    rebuilt = parts[0]
    for part, original in zip(out[1:], parts[1:]):
        # out[i] is the inner part possibly edited; use the edited full-block reconstruction instead
        pass
    # Simpler second pass:
    chunks = text.split("\n\t(symbol\n")
    rebuilt = chunks[0]
    for chunk in chunks[1:]:
        block = "\n\t(symbol\n" + chunk
        m = re.search(r'\(property "Reference" "([^"]+)"', block)
        if m and m.group(1) == ref:
            if value is not None:
                block = re.sub(
                    r'\(property "Value" "[^"]*"',
                    f'(property "Value" "{value}"',
                    block,
                    count=1,
                )
            if footprint is not None:
                block = re.sub(
                    r'\(property "Footprint" "[^"]*"',
                    f'(property "Footprint" "{footprint}"',
                    block,
                    count=1,
                )
            if lcsc is not None:
                if '(property "LCSC"' in block:
                    block = re.sub(
                        r'\(property "LCSC" "[^"]*"',
                        f'(property "LCSC" "{lcsc}"',
                        block,
                        count=1,
                    )
        rebuilt += block if rebuilt == chunks[0] else block
    # The loop above mishandles the first join. Do it cleanly:
    return None  # replaced below


def patch_all(text: str) -> str:
    chunks = text.split("\n\t(symbol\n")
    rebuilt = [chunks[0]]
    for chunk in chunks[1:]:
        block = "\n\t(symbol\n" + chunk
        m = re.search(r'\(property "Reference" "([^"]+)"', block)
        ref = m.group(1) if m else None
        if ref in Q68_CAPS:
            value, fp = Q68_CAPS[ref]
            block = re.sub(r'\(property "Value" "[^"]*"', f'(property "Value" "{value}"', block, count=1)
            block = re.sub(r'\(property "Footprint" "[^"]*"', f'(property "Footprint" "{fp}"', block, count=1)
        if ref in LCSC:
            if '(property "LCSC"' in block:
                block = re.sub(
                    r'\(property "LCSC" "[^"]*"',
                    f'(property "LCSC" "{LCSC[ref]}"',
                    block,
                    count=1,
                )
        rebuilt.append(block)
    return "".join(rebuilt[:1] + rebuilt[1:])


def insert_c15(text: str) -> str:
    if '(property "Reference" "C15"' in text:
        return text
    marker = '\t(symbol\n\t\t(lib_id "Device:C")\n\t\t(at 215.9 114.3 0)'
    if marker not in text:
        raise SystemExit("C9 insertion marker missing")
    block = C15_BLOCK.format(
        uuid_sym=str(uuid.uuid4()),
        uuid_p1=str(uuid.uuid4()),
        uuid_p2=str(uuid.uuid4()),
        uuid_l1=str(uuid.uuid4()),
        uuid_l2=str(uuid.uuid4()),
    )
    return text.replace(marker, block + marker, 1)


def main() -> None:
    text = SCH.read_text()
    text = patch_all(text)
    text = insert_c15(text)
    SCH.write_text(text)
    print("patched", SCH)


if __name__ == "__main__":
    main()
