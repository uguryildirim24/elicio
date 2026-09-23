"""Elicio board v4: the part list and nets (docs/fab/board-v4-design.md §2).

Circuit = elicio-v2 (board-v2.md, G2 table) with these changes only:

- U1 Raytac MDBT50Q -> Insight SiP ISP1807-LR (same nRF52840). The SiP has
  no VDDH, so U5 (TPS7A0230, 25 nA Iq) makes +VDD 3.0 V from VBAT and L1
  (DCCH) leaves. VBUS/D+/D- sit on inner pads and stay unconnected; firmware
  reads VBUS from VBUS_DET (R18/R19, kept) instead of USBREGSTATUS.
- DNP Q5, R9, R10, R29, R30 and the BAT_MEAS_EN net leave the schematic.
- R26 (nRESET 10 k pull-up) leaves: P0.18 configured as RESET has its own
  pull-up (design note §2, §8); firmware must set UICR PSELRESET.
- Smaller packages: U4 X2SON-4, Q1-Q4 DFN1006-3 (KiCad SOT-883 land),
  SW1 HRO 1TS015A (3.0 x 2.0 x 0.6), J2 Molex Pico-EZmate Slim (top entry,
  mated 1.20), non-Contact passives 0201, 10 uF / 4.7 uF in 0402. R1-R3
  stay 0402 220 kOhm (C881401).

LCSC codes come from jlcpcb.com part pages read 2026-09-23 (design note
§11). A blank code is UNVERIFIED: no page was read for that value.
"""
from __future__ import annotations

from sch_gen import Part

R0402 = "Resistor_SMD:R_0402_1005Metric"
C0402 = "Capacitor_SMD:C_0402_1005Metric"
R0201 = "Resistor_SMD:R_0201_0603Metric"
C0201 = "Capacitor_SMD:C_0201_0603Metric"
DFN1006 = "Package_TO_SOT_SMD:SOT-883"  # DFN1006-3: 1 G, 2 S, 3 D

# (value, size) -> (LCSC, MPN). Filled from research; "" = not yet read.
LCSC: dict[tuple[str, str], tuple[str, str]] = {
    ("220k", "0402"): ("C881401", ""),
    ("10uF", "0402"): ("C15525", "CL05A106MQ5NUNC"),
    ("1uF", "0201"): ("C5142566", "TCC0201X5R105K6R3ZT"),
    ("100nF", "0201"): ("C307380", "CL03A104KO3NNNC"),
    ("10nF", "0201"): ("C43380", "0201B103K500NT"),
    ("1.5nF", "0201"): ("C285104", "0201B152K500NT"),
    ("10k", "0201"): ("C473048", "0201WMF1002TEE"),
    ("100k", "0201"): ("C270364", "0201WMF1003TEE"),
    ("1k", "0201"): ("C270365", "0201WMF1001TEE"),
    ("1M", "0201"): ("C473482", "0201WMF1004TEE"),
    ("6.8k", "0201"): ("C4104700", "ERJ-1GNF6801C"),
    ("6.04k", "0201"): ("C270341", "0201WMF6041TEE"),
}


def _code(value: str, size: str) -> tuple[str, str]:
    return LCSC.get((value, size), ("", ""))


def r(ref: str, value: str, a: str, b: str, size: str = "0201") -> Part:
    lcsc, mpn = _code(value, size)
    fp = R0402 if size == "0402" else R0201
    return Part(ref, "Device:R", value, fp, {"1": a, "2": b}, lcsc=lcsc, mpn=mpn)


def c(ref: str, value: str, a: str, b: str, size: str = "0201") -> Part:
    lcsc, mpn = _code(value, size)
    fp = C0402 if size == "0402" else C0201
    return Part(ref, "Device:C", value, fp, {"1": a, "2": b}, lcsc=lcsc, mpn=mpn)


# ISP1807 pad -> net. Every other pad is a no-connect (pads 65-78 are the
# mechanical NC pads; 14/16/18 are the isolated row-6 VSS, §3.1).
U1_NETS = {
    "26": "+VDD",
    "28": "SWDIO",
    "30": "SWDCLK",
    "13": "nRESET",
    "20": "RF_ANT",
    "22": "RF_ANT",
    "1": "GND",
    "7": "GND",
    "21": "GND",
    "23": "GND",
    "24": "GND",
    "25": "GND",
    "31": "GND",
    # East column, pads facing +u toward U2 and the corner (§4, pin map §8).
    # P0.28-P0.31, P0.02, P0.03 are "low frequency I/O only" (nRF52840 PS
    # v1.11 pin table): CS, DRDY and the slow nets there; the three SPI data
    # lines on the HF pins P0.05/P0.06/P0.08, in U2's pad order (no crossing).
    "48": "AFE_CS",  # P0.28
    "46": "AFE_DRDY",  # P0.29 (input)
    "44": "CHG_MON",  # P0.30 AIN6
    "42": "VBAT_SENSE",  # P0.31 AIN7
    "40": "VBUS_DET",  # P0.02 AIN0
    "38": "LED_EN",  # P0.03
    "36": "AFE_MOSI",  # P0.05
    "34": "AFE_SCLK",  # P0.06
    "32": "AFE_MISO",  # P0.08 (input)
    # -s edge, facing U2's west pads 15/16.
    "6": "AFE_RESET",  # P0.26
    "4": "AFE_START",  # P0.10/NFC2 (NFCT pins as GPIO; pad 2 NFC1 left open)
}


def parts() -> list[Part]:
    u1 = {str(n): None for n in range(1, 79)}
    u1.update(U1_NETS)
    out = [
        Part("U1", "elicio:ISP1807", "ISP1807-LR", "elicio:InsightSiP_ISP1807", u1,
             lcsc="", mpn="ISP1807-LR-RS"),
        Part(
            "U2", "elicio:ADS1292", "ADS1292IRSMT", "elicio:Texas_RSM0032",
            {
                "1": None, "2": None, "3": "AFE_IN1N", "4": "AFE_IN1P", "5": "+3V0", "6": "+3V0",
                "7": None, "8": None, "9": "VREFP", "10": "GND", "11": "VCAP1", "12": "+3V0",
                "13": "GND", "14": "+3V0", "15": "AFE_RESET", "16": "AFE_START", "17": None,
                "18": "AFE_CS_AFE", "19": "AFE_MOSI_AFE", "20": "AFE_SCLK_AFE",
                "21": "AFE_MISO_AFE", "22": "AFE_DRDY_AFE", "23": "+3V0", "24": "GND",
                "25": None, "26": None, "27": "VCAP2", "28": "RLDINV", "29": "RLD_FB",
                "30": "RLD_FB", "31": "+3V0", "32": "+3V0", "33": "GND",
            },
            lcsc="C89288", mpn="ADS1292IRSMT",
        ),
        Part(
            "U3", "elicio:BQ25100", "BQ25100YFPR", "elicio:Texas_YFP0006_V4",
            {"A1": "VBAT", "A2": "VBUS", "B1": "TS", "B2": "ISET", "C1": "PRETERM", "C2": "GND"},
            lcsc="C527572", mpn="BQ25100YFPR",
        ),
        Part(
            "U4", "elicio:TLV71330PDQN", "TLV71330PDQNT", "Package_SON:Texas_X2SON-4_1x1mm_P0.65mm",
            {"4": "AFE_VIN", "3": "AFE_VIN", "1": "+3V0", "2": "GND", "5": "GND"},
            lcsc="C3071062", mpn="TLV71330PDQNT",
        ),
        Part(
            "U5", "elicio:TPS7A0230PDQN", "TPS7A0230PDQNR", "Package_SON:Texas_X2SON-4_1x1mm_P0.65mm",
            {"4": "VBAT", "3": "VBAT", "1": "+VDD", "2": "GND", "5": "GND"},
            lcsc="", mpn="TPS7A0230PDQNR",
        ),
        Part("Q1", "elicio:AO3401A", "WPM3027-3", DFN1006, {"1": "AFE_GATE", "2": "VBAT", "3": "AFE_VIN"},
             lcsc="C240195", mpn="WPM3027-3/TR"),
        # N-FET, DFN1006-3, Vgs(th) max <= 1.0 V: part UNVERIFIED (no page read).
        Part("Q2", "elicio:2N7002", "NMOS", DFN1006, {"1": "Q2_G", "2": "GND", "3": "AFE_EN_HW"}),
        Part("Q3", "elicio:2N7002", "NMOS", DFN1006, {"1": "AFE_EN_HW", "2": "GND", "3": "AFE_GATE"}),
        Part("Q4", "elicio:2N7002", "NMOS", DFN1006, {"1": "LED_EN", "2": "GND", "3": "CHG_LED_K"}),
        Part("D1", "elicio:PESD5V0L1UL", "PESD5V0L1UL", "Diode_SMD:D_SOD-523",
             {"1": "VBUS", "2": "GND"}, lcsc="C24109", mpn="PESD5V0L1UL"),
        Part("D2", "Device:LED", "LED-0402", "LED_SMD:LED_0402_1005Metric",
             {"1": "CHG_LED_K", "2": "D2_A"}, lcsc="C72043", mpn="19-217/GHC-YR1S2/3T"),
        Part("J2", "Connector:Conn_01x02_Pin", "202656-0021",
             "Connector_Molex:Molex_Pico-EZmate_Slim_202656-0021_1x02-1MP_P1.20mm_Vertical",
             {"1": "VBAT", "2": "GND"}, lcsc="", mpn="202656-0021"),
        Part("J3", "Connector:Conn_01x03_Pin", "HDR-3-RA",
             "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Horizontal",
             # Symmetric header, reversed so the branches don't cross (§5.4).
             {"1": "REF", "2": "SIG2", "3": "SIG1"}, lcsc="C49257"),
        Part("J4", "Connector:TC2030", "TC2030-NL",
             "Connector:Tag-Connect_TC2030-IDC-NL_2x03_P1.27mm_Vertical",
             {"1": "+VDD", "2": "SWDIO", "3": "GND", "4": "SWDCLK", "5": "GND", "6": "nRESET"},
             in_bom=False),
        Part("SW1", "Switch:SW_Push", "1TS015A", "elicio:SW_HRO_1TS015A",
             {"1": "nRESET", "2": "GND"}, lcsc="C398746", mpn="1TS015A-1200-0600-CT"),
        Part("P1", "elicio:PAD_8x8", "SIG1", "elicio:RING_PAD_D5_H2.7", {"1": "SIG1"}, in_bom=False),
        Part("P2", "elicio:PAD_8x8", "SIG2", "elicio:RING_PAD_D5_H2.7", {"1": "SIG2"}, in_bom=False),
        Part("P3", "elicio:PAD_8x8", "REF", "elicio:RING_PAD_D5_H2.7", {"1": "REF"}, in_bom=False),
        # One-face wall rings (B side): VBUS passes P5 on F (design note §5.4).
        Part("P4", "elicio:PAD_8x8", "CHARGE_VBUS", "elicio:RING_1S_D4.6_NPTH2.7", {"1": "VBUS"}, in_bom=False),
        Part("P5", "elicio:PAD_8x8", "CHARGE_GND", "elicio:RING_1S_D4.6_NPTH2.7", {"1": "GND"}, in_bom=False),
        # Contact: 220 kOhm per electrode path, 0402 (Q79, R7).
        r("R1", "220k", "SIG1", "AFE_IN1P", "0402"),
        r("R2", "220k", "SIG2", "AFE_IN1N", "0402"),
        r("R3", "220k", "REF", "RLD_FB", "0402"),
        r("R4", "1M", "RLD_FB", "RLDINV"),
        r("R5", "10k", "AFE_SCLK", "AFE_SCLK_AFE"),
        r("R6", "10k", "AFE_MOSI", "AFE_MOSI_AFE"),
        r("R7", "10k", "AFE_CS", "AFE_CS_AFE"),
        r("R8", "10k", "AFE_MISO_AFE", "AFE_MISO"),
        r("R11", "6.8k", "ISET", "GND"),
        r("R12", "6.04k", "PRETERM", "GND"),
        r("R13", "10k", "TS", "GND"),
        r("R14", "100k", "VBAT", "AFE_GATE"),
        r("R15", "100k", "VBAT", "AFE_EN_HW"),
        r("R16", "100k", "VBUS", "Q2_G"),
        r("R17", "1M", "Q2_G", "GND"),
        r("R18", "47k", "VBUS", "VBUS_DET"),
        r("R19", "27k", "VBUS_DET", "GND"),
        r("R20", "1M", "VBAT", "VBAT_SENSE"),
        r("R21", "1M", "VBAT_SENSE", "GND"),
        r("R22", "1k", "VBUS", "D2_A"),
        r("R23", "100k", "AFE_RESET", "GND"),
        r("R24", "100k", "AFE_START", "GND"),
        r("R25", "10k", "ISET", "CHG_MON"),
        r("R27", "10k", "AFE_DRDY_AFE", "AFE_DRDY"),
        r("R28", "10k", "LED_EN", "GND"),
        c("C1", "1.5nF", "RLD_FB", "RLDINV"),
        c("C2", "10nF", "ISET", "GND"),
        c("C3", "1uF", "VBUS", "GND"),
        c("C4", "1uF", "VBAT", "GND"),
        c("C5", "1uF", "AFE_VIN", "GND"),
        c("C6", "10uF", "+3V0", "GND", "0402"),
        c("C7", "100nF", "+3V0", "GND"),
        c("C8", "10uF", "+3V0", "GND", "0402"),
        c("C9", "10uF", "VREFP", "GND", "0402"),
        c("C10", "1uF", "VCAP1", "GND"),
        c("C11", "100nF", "VCAP2", "GND"),
        c("C12", "100nF", "+VDD", "GND"),
        c("C13", "1uF", "+VDD", "GND"),
        c("C14", "4.7uF", "VBAT", "GND", "0402"),
        c("C15", "100nF", "+3V0", "GND"),
        c("C16", "1uF", "VBAT", "GND"),
    ]
    flags = [("PF1", "GND"), ("PF2", "VBAT"), ("PF3", "VBUS"), ("PF5", "AFE_VIN")]
    out += [
        Part(ref, "power:PWR_FLAG", "PWR_FLAG", "", {"1": net}, in_bom=False, on_board=False)
        for ref, net in flags
    ]
    return out
