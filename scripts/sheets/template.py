#!/usr/bin/env python3
"""1:1 paper template and M1–M8 measurement drawings (WP15).

Winner outline: packing-v2.md §5 ``A_501015_series_w20_y8_iII_s3``.
Chord and M1 gate: packing-v2.md §6 ``V2_TOTAL_CHORD`` / ``V2_M1_gate``.
Contact sites (u, s) mm: packing-v2.md §5 flex tabs.

    .venv/bin/python scripts/sheets/template.py --out docs/fab

Writes ``template.pdf`` and ``sheets/m1.svg`` … ``m8.svg``. PDF metadata
dates and SVG ``dc:date`` are pinned so a second run is byte-identical.
"""

from __future__ import annotations

import argparse
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FONT_PATH = ROOT / "scripts" / "cad" / "fonts" / "LiberationSans-Regular.ttf"

# packing-v2.md §5 winner A_501015_series_w20_y8_iII_s3
BODY_WIDTH = 20.0
BODY_ARC = 48.4
LID_Y = 8.0
BODY_THICK = 9.0
STANDOFF = 3.0
CREASE_BOW = 3.0
# packing-v2.md §6 measured on the built solid
TOTAL_CHORD = 47.90
M1_GATE = 50.90
# packing-v2.md §5 flex-tab sites (folded)
CONTACT_1 = (5.9, 22.0)
CONTACT_2 = (10.4, 33.1)
CONTACT_REF = (8.5, 43.0)
# Q7 / plan v1 §3.3 CAD keeps 4.7 × 1.35
CONTACT_DOME_D = 4.7
# plan v2 §7 medial skin face R0.5; outline uses WALL_SIDE 1.5 (default.toml)
CORNER_R = 1.5

PIN_DATE = "2026-09-16T00:00:00Z"
PDF_DATE = "D:20260916000000Z"
SVG_HASH = "elicio-sheets-v2"
PDF_IDENT = b"elicio-sheets-v2pdf"

LETTER_W_IN = 8.5
LETTER_H_IN = 11.0
MM_PER_IN = 25.4

SHEET_NAMES = ("m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8")

INK = "#1a1a1a"
RULE = "#333333"
FILL = "#f4f4f4"
SITE = "#b03a2e"
REF_SITE = "#1a5276"
HINT = "#555555"


class SheetError(RuntimeError):
    """Template or drawing failed."""


def configure_matplotlib() -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager

    if not FONT_PATH.is_file():
        raise SheetError(f"font missing: {FONT_PATH}")
    font_manager.fontManager.addfont(str(FONT_PATH))
    name = font_manager.FontProperties(fname=str(FONT_PATH)).get_name()
    plt.rcParams["font.family"] = name
    plt.rcParams.update(
        {
            "figure.autolayout": False,
            "path.simplify": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.hashsalt": SVG_HASH,
            "axes.unicode_minus": False,
        }
    )


def pin_pdf(data: bytes) -> bytes:
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import ArrayObject, ByteStringObject

    reader = PdfReader(io.BytesIO(data))
    writer = PdfWriter()
    writer.append(reader)
    writer.add_metadata(
        {
            "/Title": "Elicio v2 1:1 paper template",
            "/Creator": "elicio-sheets",
            "/Producer": "elicio-sheets",
            "/CreationDate": PDF_DATE,
            "/ModDate": PDF_DATE,
        }
    )
    writer._ID = ArrayObject([ByteStringObject(PDF_IDENT), ByteStringObject(PDF_IDENT)])
    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()


def pin_svg(data: bytes) -> bytes:
    text = data.decode("utf-8")
    text = re.sub(
        r"<dc:date>.*?</dc:date>",
        f"<dc:date>{PIN_DATE}</dc:date>",
        text,
        flags=re.DOTALL,
    )
    return text.encode("utf-8")


def mm_axes(fig, left_mm: float, bottom_mm: float, width_mm: float, height_mm: float):
    """Axes where 1 data unit is 1 mm on a printed US-letter page."""
    fw, fh = fig.get_size_inches()
    ax = fig.add_axes(
        [
            left_mm / (fw * MM_PER_IN),
            bottom_mm / (fh * MM_PER_IN),
            width_mm / (fw * MM_PER_IN),
            height_mm / (fh * MM_PER_IN),
        ]
    )
    ax.set_xlim(0.0, width_mm)
    ax.set_ylim(0.0, height_mm)
    ax.set_aspect("equal", adjustable="box")
    ax.set_axis_off()
    return ax


def add_rounded_rect(ax, x: float, y: float, w: float, h: float, r: float, **kwargs):
    from matplotlib.patches import FancyBboxPatch

    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0,rounding_size={r}",
        mutation_aspect=1.0,
        **kwargs,
    )
    ax.add_patch(patch)
    return patch


def body_xy(origin: tuple[float, float], u: float, s: float) -> tuple[float, float]:
    """Map packing (u, s) onto the paper: hook at the top of the outline."""
    ox, oy = origin
    return ox + u, oy + BODY_ARC - s


def draw_winner_outline(ax, origin: tuple[float, float]) -> None:
    from matplotlib.patches import Circle

    ox, oy = origin
    add_rounded_rect(
        ax,
        ox,
        oy,
        BODY_WIDTH,
        BODY_ARC,
        CORNER_R,
        facecolor=FILL,
        edgecolor=INK,
        linewidth=1.2,
        zorder=1,
    )
    for (u, s), color, label in (
        (CONTACT_1, SITE, "C1"),
        (CONTACT_2, SITE, "C2"),
        (CONTACT_REF, REF_SITE, "REF"),
    ):
        x, y = body_xy(origin, u, s)
        ax.add_patch(
            Circle(
                (x, y),
                CONTACT_DOME_D / 2.0,
                facecolor="white",
                edgecolor=color,
                linewidth=1.1,
                zorder=2,
            )
        )
        ax.plot(x, y, marker="+", color=color, markersize=5, zorder=3)
        ax.text(
            x + 3.2,
            y,
            label,
            color=color,
            fontsize=7,
            ha="left",
            va="center",
            zorder=3,
        )


def write_template_pdf(path: Path) -> None:
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(LETTER_W_IN, LETTER_H_IN), dpi=72)
    fig.set_facecolor("white")

    fig.text(
        0.08,
        0.96,
        "Elicio v2 paper template  —  print at 100 %. Do not fit to page.",
        fontsize=12,
        color=INK,
        va="top",
    )
    fig.text(
        0.08,
        0.935,
        "Winner A_501015_series_w20_y8_iII_s3  (packing-v2.md §5).  Right ear (Q28).  Do not flip.",
        fontsize=8,
        color=HINT,
        va="top",
    )

    bar = mm_axes(fig, left_mm=20.0, bottom_mm=232.0, width_mm=70.0, height_mm=18.0)
    bar.plot([10.0, 60.0], [8.0, 8.0], color=INK, linewidth=1.6, solid_capstyle="butt")
    bar.plot([10.0, 10.0], [5.5, 10.5], color=INK, linewidth=1.6)
    bar.plot([60.0, 60.0], [5.5, 10.5], color=INK, linewidth=1.6)
    bar.text(35.0, 12.0, "50 mm", fontsize=8, ha="center", va="bottom", color=INK)
    bar.text(10.0, 2.0, "0", fontsize=7, ha="center", va="bottom", color=HINT)
    bar.text(60.0, 2.0, "50", fontsize=7, ha="center", va="bottom", color=HINT)

    fig.text(
        0.08,
        0.88,
        "Measure the 50 mm bar before you trust this template.",
        fontsize=10,
        color=INK,
        va="top",
    )
    fig.text(
        0.08,
        0.855,
        "If the bar is not 50 mm on the paper, throw this print away. Print again at 100 %.",
        fontsize=8,
        color=HINT,
        va="top",
    )

    outline = mm_axes(fig, left_mm=20.0, bottom_mm=92.0, width_mm=90.0, height_mm=130.0)
    origin = (12.0, 38.0)
    draw_winner_outline(outline, origin)
    ox, oy = origin
    outline.annotate(
        "",
        xy=(ox, oy + BODY_ARC + 4.0),
        xytext=(ox + BODY_WIDTH, oy + BODY_ARC + 4.0),
        arrowprops=dict(arrowstyle="<->", color=RULE, lw=0.8),
    )
    outline.text(
        ox + BODY_WIDTH / 2.0,
        oy + BODY_ARC + 6.5,
        f"{BODY_WIDTH:.0f} mm width",
        fontsize=7,
        ha="center",
        color=HINT,
    )
    outline.annotate(
        "",
        xy=(ox - 6.0, oy),
        xytext=(ox - 6.0, oy + BODY_ARC),
        arrowprops=dict(arrowstyle="<->", color=RULE, lw=0.8),
    )
    outline.text(
        ox - 8.5,
        oy + BODY_ARC / 2.0,
        f"{BODY_ARC:.1f} mm arc",
        fontsize=7,
        ha="center",
        va="center",
        color=HINT,
        rotation=90,
    )
    outline.text(ox + BODY_WIDTH / 2.0, oy + BODY_ARC + 12.0, "HOOK", fontsize=8, ha="center", color=INK)
    outline.text(ox + BODY_WIDTH / 2.0, oy - 6.0, "TAIL", fontsize=8, ha="center", color=INK)
    outline.text(ox - 1.0, oy + BODY_ARC / 2.0, "ANT", fontsize=7, ha="right", va="center", color=HINT)
    outline.text(
        ox + BODY_WIDTH + 1.0,
        oy + BODY_ARC / 2.0,
        "POST",
        fontsize=7,
        ha="left",
        va="center",
        color=HINT,
    )

    fig.text(
        0.08,
        0.30,
        "Cut on the outline. Hold the paper behind the right ear, hook at the top, printed face to the skin.",
        fontsize=8,
        color=INK,
        va="top",
    )
    fig.text(
        0.08,
        0.275,
        "C1 SIG1 (5.9, 22.0)   C2 SIG2 (10.4, 33.1)   REF (8.5, 43.0)  — packing-v2.md §5, mm (u, s).",
        fontsize=8,
        color=INK,
        va="top",
    )
    fig.text(
        0.08,
        0.25,
        "On-bone check (Q17): the REF mark must sit on bone, not on soft tissue. Write that on measure.md.",
        fontsize=8,
        color=INK,
        va="top",
    )
    fig.text(
        0.08,
        0.20,
        "Numbers on this page",
        fontsize=9,
        color=INK,
        va="top",
    )
    fig.text(
        0.08,
        0.175,
        f"BODY_WIDTH {BODY_WIDTH:.0f} mm, BODY_ARC {BODY_ARC:.1f} mm, LID_Y {LID_Y:.0f} mm, "
        f"BODY_THICK {BODY_THICK:.0f} mm, standoff {STANDOFF:.0f} mm (packing-v2.md §5).",
        fontsize=8,
        color=HINT,
        va="top",
    )
    fig.text(
        0.08,
        0.15,
        f"TOTAL_CHORD {TOTAL_CHORD:.2f} mm, M1 gate {M1_GATE:.2f} mm at bow {CREASE_BOW:.0f} "
        "(packing-v2.md §6 V2_TOTAL_CHORD / V2_M1_gate).",
        fontsize=8,
        color=HINT,
        va="top",
    )
    fig.text(
        0.08,
        0.125,
        "Dome circles are Ø 4.7 mm (plan v1 §3.3 / Q7 CAD keep). They are marks, not a printed gauge.",
        fontsize=8,
        color=HINT,
        va="top",
    )
    fig.text(
        0.08,
        0.08,
        "Generated by scripts/sheets/template.py. Not a quote. Not an order.",
        fontsize=7,
        color=HINT,
        va="top",
    )

    buf = io.BytesIO()
    fig.savefig(buf, format="pdf", facecolor="white", edgecolor="none")
    plt.close(fig)
    path.write_bytes(pin_pdf(buf.getvalue()))


def _sheet_fig():
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(90 / MM_PER_IN, 70 / MM_PER_IN), dpi=72)
    fig.set_facecolor("white")
    ax = fig.add_axes([0.06, 0.10, 0.88, 0.78])
    ax.set_xlim(0.0, 80.0)
    ax.set_ylim(0.0, 56.0)
    ax.set_aspect("equal", adjustable="box")
    ax.set_axis_off()
    return fig, ax


def _title(fig, text: str) -> None:
    fig.text(0.06, 0.92, text, fontsize=8, color=INK, va="top")


def draw_m1(fig, ax) -> None:
    _title(fig, "M1  ear-root chord  (caliper, through the air)")
    ax.plot([12, 22, 28, 32, 36, 40, 48, 58], [42, 46, 48, 48.5, 48, 46, 40, 28], color=INK, lw=1.4)
    ax.plot([12, 58], [38, 22], color=SITE, lw=1.6)
    ax.plot([12, 12], [36, 40], color=SITE, lw=1.2)
    ax.plot([58, 58], [20, 24], color=SITE, lw=1.2)
    ax.text(35, 26, "50.90 mm gate", fontsize=7, color=SITE, ha="center")
    ax.text(12, 12, "helix root", fontsize=7, color=HINT)
    ax.text(50, 12, "mastoid join", fontsize=7, color=HINT)
    ax.text(8, 4, "packing-v2.md §6 V2_M1_gate at bow 3", fontsize=6, color=HINT)


def draw_m2(fig, ax) -> None:
    _title(fig, "M2  crease arc  (string in the groove, then caliper)")
    xs = [12, 20, 28, 36, 44, 52, 60]
    ys = [40, 46, 48, 47, 42, 34, 24]
    ax.plot(xs, ys, color=INK, lw=1.6)
    ax.plot(xs, ys, "o", color=SITE, ms=3)
    ax.text(36, 20, "along the crease", fontsize=7, color=HINT, ha="center")
    ax.text(8, 4, "v1 M2 definition. Typical 50–65 mm.", fontsize=6, color=HINT)


def draw_m3(fig, ax) -> None:
    _title(fig, "M3  sulcus clearance  (caliper depth rod)")
    add_rounded_rect(ax, 18, 16, 10, 28, 1.0, facecolor=FILL, edgecolor=INK, lw=1.1)
    ax.annotate("", xy=(36, 30), xytext=(28, 30), arrowprops=dict(arrowstyle="->", color=SITE, lw=1.2))
    ax.plot([36, 36], [18, 42], color=RULE, lw=1.0)
    ax.text(40, 30, "rim to skull", fontsize=7, color=SITE, va="center")
    ax.text(8, 4, "Do not press the ear flat. Typical 8–14 mm.", fontsize=6, color=HINT)


def draw_m4(fig, ax) -> None:
    from matplotlib.patches import Ellipse

    _title(fig, "M4  helix-root thickness  (caliper, head to outside)")
    ax.add_patch(Ellipse((32, 30), 18, 12, facecolor=FILL, edgecolor=INK, lw=1.1))
    ax.annotate("", xy=(22, 30), xytext=(42, 30), arrowprops=dict(arrowstyle="<->", color=SITE, lw=1.2))
    ax.text(32, 14, "jaws close sideways", fontsize=7, color=HINT, ha="center")
    ax.text(8, 4, "Hook sits here. Typical 4.5–7.5 mm.", fontsize=6, color=HINT)


def draw_m5(fig, ax) -> None:
    _title(fig, "M5  glasses temple  (caliper, or write 0)")
    ax.plot([14, 66], [30, 30], color=INK, lw=3.0, solid_capstyle="round")
    ax.annotate("", xy=(40, 24), xytext=(40, 36), arrowprops=dict(arrowstyle="<->", color=SITE, lw=1.2))
    ax.text(44, 30, "temple", fontsize=7, color=HINT, va="center")
    ax.text(8, 4, "No glasses: write 0. Typical 1.8–3.2 mm.", fontsize=6, color=HINT)


def draw_m6(fig, ax) -> None:
    _title(fig, "M6  mastoid offset  (caliper) and REF on-bone (Q17)")
    ax.plot([16, 30, 40, 52], [36, 40, 38, 28], color=INK, lw=1.4)
    ax.plot([40, 58], [38, 24], color=SITE, lw=1.5)
    ax.plot(52, 28, "o", color=REF_SITE, ms=8)
    ax.text(56, 30, "REF", fontsize=7, color=REF_SITE)
    ax.text(8, 10, "Paper template at REF is the on-bone check, not a printed gauge (Q17).", fontsize=6, color=HINT)
    ax.text(8, 4, "Typical M6 12–18 mm.", fontsize=6, color=HINT)


def draw_m7(fig, ax) -> None:
    _title(fig, "M7  crease top to mid-concha  (string, then caliper)")
    ax.plot([18, 28, 36, 44, 52], [46, 44, 38, 30, 22], color=INK, lw=1.4)
    ax.plot([18, 18], [44, 48], color=SITE, lw=1.2)
    ax.plot([36, 44], [38, 30], color=SITE, lw=2.0)
    ax.text(22, 50, "helix root", fontsize=6, color=HINT)
    ax.text(46, 26, "canal height", fontsize=6, color=HINT)
    ax.text(8, 4, "Typical 18–26 mm.", fontsize=6, color=HINT)


def draw_m8(fig, ax) -> None:
    _title(fig, "M8  helix rise  (caliper, straight up)")
    ax.plot([24, 36, 44, 52, 58], [22, 28, 40, 46, 44], color=INK, lw=1.4)
    ax.annotate("", xy=(36, 28), xytext=(52, 46), arrowprops=dict(arrowstyle="<->", color=SITE, lw=1.2))
    ax.text(40, 16, "attachment to rim top", fontsize=7, color=HINT)
    ax.text(8, 4, "Feeds HOOK_RADIUS. Typical 8–14 mm.", fontsize=6, color=HINT)


DRAWERS = {
    "m1": draw_m1,
    "m2": draw_m2,
    "m3": draw_m3,
    "m4": draw_m4,
    "m5": draw_m5,
    "m6": draw_m6,
    "m7": draw_m7,
    "m8": draw_m8,
}


def write_sheet_svg(path: Path, name: str) -> None:
    import matplotlib.pyplot as plt

    fig, ax = _sheet_fig()
    DRAWERS[name](fig, ax)
    buf = io.BytesIO()
    fig.savefig(buf, format="svg", facecolor="white", edgecolor="none")
    plt.close(fig)
    path.write_bytes(pin_svg(buf.getvalue()))


def write_all(out_dir: Path) -> list[Path]:
    configure_matplotlib()
    out_dir = out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    sheets = out_dir / "sheets"
    sheets.mkdir(exist_ok=True)
    written = [out_dir / "template.pdf"]
    write_template_pdf(written[0])
    for name in SHEET_NAMES:
        path = sheets / f"{name}.svg"
        write_sheet_svg(path, name)
        written.append(path)
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write the v2 1:1 template and M1–M8 drawings.")
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "docs" / "fab",
        help="Output directory (default: docs/fab)",
    )
    args = parser.parse_args(argv)
    try:
        paths = write_all(args.out)
    except SheetError as exc:
        sys.stderr.write(f"{exc}\n")
        return 1
    for path in paths:
        sys.stdout.write(f"{path}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
