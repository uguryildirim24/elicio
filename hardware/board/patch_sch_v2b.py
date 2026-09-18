#!/usr/bin/env python3
"""WP12b schematic edits: Q68 ADS decoupling and LCSC fills (2026-09-17 pages)."""
from __future__ import annotations

import re
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCH = ROOT / "hardware" / "board" / "elicio-v2.kicad_sch"

# Pages read 2026-09-17 on jlcpcb.com/partdetail/<id>. Stock quantity was not
# displayed on those pages (tier only). Price was not displayed.
LCSC = {
    "C2": "C91601",  # 10 nF 0402 Murata GCM155R71H103KA55D
    "C6": "C19702",  # 10 µF 0603 Samsung CL10A106KP8NNNC
    "C7": "C14663",  # 100 nF 0603 YAGEO
    "C8": "C19702",
    "C9": "C19702",  # was C15850 = 0805 10 µF; footprint is 0603
    "C11": "C1525",  # 100 nF 0402 Samsung CL05B104KO5NNNC Basic
    "C12": "C1525",
    "C15": "C14663",
    "R1": "C881401",
    "R2": "C881401",
    "R3": "C881401",
    "R4": "C2782127",
    "R14": "C25741",
    "R15": "C25741",
    "R16": "C25741",
    "R17": "C2782127",
    "R20": "C2782127",
    "R21": "C2782127",
    "R22": "C11702",
    "R23": "C25741",
    "R24": "C25741",
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
