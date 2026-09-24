"""Insight SiP ISP1807-LR land pattern and pin table (board-v4-design.md §3.1).

Source: isp_ble_DS1807_R19 (insightsip.com, read 2026-09-23): pin table §3
pages 10-11, top-view pad map page 12, dimensional drawing §4.1 page 13
(tolerance +/-0.03), keep-out §4.3 page 14. Recommended land = module pads.
Pad centres below are in the datasheet's top view, origin at the module's
top-left corner, x right, y down (the antenna half is y 4-8). Every centre
is snapped to the drawing's stated dimensions (0.513/0.5125, 1.725, 2.375,
2.7, 3.6, 3.8, 6.55, 7.488 in y; 6.275, 6.5, 6.6, 7.05 in x; pitch 0.65 in
the dense half, 1.0 in the antenna half); a pixel measurement of the page-13
drawing agrees within 0.02 mm.
"""
from __future__ import annotations

A = (0.775, 0.775)  # corners 1, 31, 68, 75
B = (0.775, 0.8)  # 7, 25
C = (0.4, 0.375)  # top and bottom rows
D = (0.4, 0.4)  # inner grid and row 6
E = (0.375, 0.4)  # left/right edges

X9 = [1.4 + 0.65 * k for k in range(9)]  # 1.40 .. 6.60
X8 = [1.725 + 0.65 * k for k in range(8)]  # 1.725 .. 6.275
XB = [1.5 + 1.0 * k for k in range(6)]  # 1.5 .. 6.5


def pads() -> dict[str, tuple[float, float, float, float]]:
    """pad number -> (x, y, w, h) in datasheet top-view mm."""
    p: dict[str, tuple[float, float, float, float]] = {}

    def put(num, x, y, size):
        p[str(num)] = (round(x, 4), round(y, 4), size[0], size[1])

    put(1, 0.5125, 0.5125, A)
    put(31, 7.4875, 0.5125, A)
    put(68, 0.5125, 7.4875, A)
    put(75, 7.4875, 7.4875, A)
    put(7, 0.5125, 3.6, B)
    put(25, 7.4875, 3.6, B)
    for num, x in zip((48, 46, 44, 42, 40, 38, 36, 34, 32), X9):
        put(num, x, 0.3125, C)
    for num, x in zip((47, 45, 43, 41, 39, 37, 35, 33), X8):
        put(num, x, 0.9625, D)
    for num, y in zip((2, 4, 6), (1.4, 2.05, 2.7)):
        put(num, 0.3125, y, E)
    for num, y in zip((30, 28, 26), (1.4, 2.05, 2.7)):
        put(num, 7.6875, y, E)
    put(3, 0.95, 1.725, D)
    put(29, 7.05, 1.725, D)
    put(5, 0.95, 2.375, D)
    put(27, 7.05, 2.375, D)
    for num, x in zip(range(56, 48, -1), X8):
        put(num, x, 1.725, D)
    for num, x in zip(range(64, 56, -1), X8):
        put(num, x, 2.375, D)
    for num, x in zip(range(9, 24, 2), X8):
        put(num, x, 3.15, D)
    for num, x in zip(range(8, 25, 2), X9):
        put(num, x, 3.8, D)
    for num, y in zip((65, 66, 67), (4.55, 5.55, 6.55)):
        put(num, 0.3125, y, E)
    for num, y in zip((78, 77, 76), (4.55, 5.55, 6.55)):
        put(num, 7.6875, y, E)
    for num, x in zip(range(69, 75), XB):
        put(num, x, 7.6875, C)
    assert len(p) == 78, len(p)
    return p


# Datasheet §3 pin table (pads 65-78 are NC mechanical pads).
PIN_NAMES = {
    1: "VSS", 2: "P0.09/NFC1", 3: "P0.12", 4: "P0.10/NFC2", 5: "P0.14", 6: "P0.26",
    7: "VSS", 8: "D+", 9: "P0.16", 10: "D-", 11: "P0.21", 12: "VBUS", 13: "P0.18/RESET",
    14: "VSS", 15: "P0.20", 16: "VSS", 17: "P0.22", 18: "VSS", 19: "P0.24", 20: "OUT_ANT",
    21: "VSS", 22: "OUT_MOD", 23: "VSS", 24: "VSS", 25: "VSS", 26: "VCC_nRF", 27: "P0.17",
    28: "SWDIO", 29: "P0.13", 30: "SWDCLK", 31: "VSS", 32: "P0.08", 33: "P0.07",
    34: "P0.06", 35: "P0.04/AIN2", 36: "P0.05/AIN3", 37: "P0.15", 38: "P0.03/AIN1",
    39: "P0.27", 40: "P0.02/AIN0", 41: "P0.25", 42: "P0.31/AIN7", 43: "P0.11",
    44: "P0.30/AIN6", 45: "P0.19", 46: "P0.29/AIN5", 47: "P0.23", 48: "P0.28/AIN4",
    49: "P1.02", 50: "P1.06", 51: "P1.15", 52: "P1.14", 53: "P1.13", 54: "P1.05",
    55: "P1.08", 56: "P1.09", 57: "P1.00", 58: "P1.03", 59: "P1.12", 60: "P1.10",
    61: "P1.11", 62: "P1.07", 63: "P1.04", 64: "P1.01",
}
PIN_NAMES.update({n: "NC" for n in range(65, 79)})

# Pads a 2-layer flex without via-in-pad can reach (§3.1 of the design note):
# the outer ring above the antenna half, plus pad 13 through the row-4/5
# channel from the left, VSS 21/23 from pad 25, VSS 24 bridged to 25, and the
# OUT_ANT-OUT_MOD bridge (20-22) the datasheet requires.
REACHABLE = {
    1, 2, 4, 6, 7, 13, 20, 21, 22, 23, 24, 25, 26, 28, 30, 31,
    32, 34, 36, 38, 40, 42, 44, 46, 48,
}
