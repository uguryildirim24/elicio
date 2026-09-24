"""Small s-expression helpers for KiCad text files (no parsing into objects)."""
from __future__ import annotations


def match_paren(text: str, start: int) -> int:
    """Index one past the ')' that closes the '(' at ``start``. Skips quoted strings."""
    depth = 0
    i = start
    in_str = False
    while i < len(text):
        ch = text[i]
        if in_str:
            if ch == "\\":
                i += 2
                continue
            if ch == '"':
                in_str = False
        elif ch == '"':
            in_str = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise ValueError("unbalanced s-expression")


def children(text: str, start: int) -> list[tuple[int, int]]:
    """(begin, end) spans of the direct child lists of the list opening at ``start``."""
    end = match_paren(text, start)
    out: list[tuple[int, int]] = []
    i = start + 1
    in_str = False
    while i < end - 1:
        ch = text[i]
        if in_str:
            if ch == "\\":
                i += 2
                continue
            if ch == '"':
                in_str = False
        elif ch == '"':
            in_str = True
        elif ch == "(":
            j = match_paren(text, i)
            out.append((i, j))
            i = j
            continue
        i += 1
    return out


def lib_symbol_blocks(sch_or_lib: str, container: str) -> dict[str, str]:
    """Top-level ``(symbol "name" ...)`` blocks inside ``(lib_symbols`` or ``(kicad_symbol_lib``."""
    start = sch_or_lib.find("(" + container)
    if start < 0:
        raise ValueError(container + " not found")
    blocks: dict[str, str] = {}
    for b, e in children(sch_or_lib, start):
        block = sch_or_lib[b:e]
        if not block.startswith("(symbol"):
            continue
        name = block.split('"', 2)[1]
        blocks[name] = block
    return blocks
