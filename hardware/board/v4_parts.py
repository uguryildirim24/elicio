"""Elicio board v4: the part list and nets (docs/fab/board-v4-design.md §2).

Circuit = elicio-v2 (board-v2.md, G2 table) with these changes only:

- U1 Raytac MDBT50Q -> Insight SiP ISP1807-LR (same nRF52840). The SiP has
  no VDDH, so U5 (TPS7A0230, 25 nA Iq) makes +VDD 3.0 V from VBAT and L1
  (DCCH) leaves. VBUS/D+/D- sit on inner pads and stay unconnected; firmware
  reads VBUS from VBUS_DET (R18/R19, kept) instead of USBREGSTATUS.
- DNP Q5, R9, R10, R29, R30 and the BAT_MEAS_EN net leave the schematic.
- Smaller packages: U4 X2SON-4, Q1-Q4 SOT-723, SW1 Omron B3U, J2 Molex
  Pico-EZmate Slim (top entry, mated 1.20), non-Contact passives 0201,
  10 uF / 4.7 uF in 0402. R1-R3 stay 0402 220 kOhm (C881401).

LCSC codes marked "" are filled from the research lanes (§9 of the note)
and stay UNVERIFIED until a page read is recorded there.
"""
from __future__ import annotations

from sch_gen import Part

R0402 = "Resistor_SMD:R_0402_1005Metric"
C0402 = "Capacitor_SMD:C_0402_1005Metric"
R0201 = "Resistor_SMD:R_0201_0603Metric"
C0201 = "Capacitor_SMD:C_0201_0603Metric"
SOT723 = "Package_TO_SOT_SMD:SOT-723"

# (value, size) -> (LCSC, MPN). Filled from research; "" = not yet read.
LCSC: dict[tuple[str, str], tuple[str, str]] = {
    ("220k", "0402"): ("C881401", ""),
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
    # Top row, pads facing +u toward the posterior strip (§4, pin map §7).
    "48": "AFE_CS",  # P0.28
    "46": "AFE_MISO",  # P0.29
    "44": "AFE_START",  # P0.30
    "42": "CHG_MON",  # P0.31 AIN7 (v2)
    "40": "VBAT_SENSE",  # P0.02 AIN0 (v2)
    "38": "AFE_RESET",  # P0.03
    "36": "VBUS_DET",  # P0.05
    "34": "AFE_MOSI",  # P0.06 (v2)
    "32": "AFE_SCLK",  # P0.08 (v2)
    # Left edge, facing the neck half.
    "6": "AFE_DRDY",  # P0.26
    "4": "LED_EN",  # P0.10/NFC2 (needs NFCT pins as GPIO)
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
            "U3", "elicio:BQ25100", "BQ25100YFPR", "elicio:Texas_YFP0006",
            {"A1": "VBAT", "A2": "VBUS", "B1": "TS", "B2": "ISET", "C1": "PRETERM", "C2": "GND"},
            lcsc="C527572", mpn="BQ25100YFPR",
        ),
        Part(
            "U4", "elicio:TLV71330PDQN", "TLV71330PDQNR", "Package_SON:Texas_X2SON-4_1x1mm_P0.65mm",
            {"4": "AFE_VIN", "3": "AFE_VIN", "1": "+3V0", "2": "GND", "5": "GND"},
            lcsc="", mpn="TLV71330PDQNR",
        ),
        Part(
            "U5", "elicio:TPS7A0230PDQN", "TPS7A0230PDQNR", "Package_SON:Texas_X2SON-4_1x1mm_P0.65mm",
            {"4": "VBAT", "3": "VBAT", "1": "+VDD", "2": "GND", "5": "GND"},
            lcsc="", mpn="TPS7A0230PDQNR",
        ),
        Part("Q1", "elicio:AO3401A", "PMOS", SOT723, {"1": "AFE_GATE", "2": "VBAT", "3": "AFE_VIN"}),
        Part("Q2", "elicio:2N7002", "NMOS", SOT723, {"1": "Q2_G", "2": "GND", "3": "AFE_EN_HW"}),
        Part("Q3", "elicio:2N7002", "NMOS", SOT723, {"1": "AFE_EN_HW", "2": "GND", "3": "AFE_GATE"}),
        Part("Q4", "elicio:2N7002", "NMOS", SOT723, {"1": "LED_EN", "2": "GND", "3": "CHG_LED_K"}),
        Part("D1", "elicio:PESD5V0L1UL", "PESD5V0L1UL", "Diode_SMD:D_SOD-523",
             {"1": "VBUS", "2": "GND"}, lcsc="C24109", mpn="PESD5V0L1UL"),
        Part("D2", "Device:LED", "LED-0402", "LED_SMD:LED_0402_1005Metric",
             {"1": "CHG_LED_K", "2": "D2_A"}, lcsc="C72043", mpn="19-217/GHC-YR1S2/3T"),
        Part("J2", "Connector:Conn_01x02_Pin", "202656-0021",
             "Connector_Molex:Molex_Pico-EZmate_Slim_202656-0021_1x02-1MP_P1.20mm_Vertical",
             {"1": "VBAT", "2": "GND"}, lcsc="", mpn="202656-0021"),
        Part("J3", "Connector:Conn_01x03_Pin", "HDR-3-RA",
             "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Horizontal",
             {"1": "SIG1", "2": "SIG2", "3": "REF"}, lcsc="C49257"),
        Part("J4", "Connector:TC2030", "TC2030-NL",
             "Connector:Tag-Connect_TC2030-IDC-NL_2x03_P1.27mm_Vertical",
             {"1": "+VDD", "2": "SWDIO", "3": "GND", "4": "SWDCLK", "5": "GND", "6": "nRESET"},
             in_bom=False),
        Part("SW1", "Switch:SW_Push", "B3U-1000P", "Button_Switch_SMD:SW_SPST_B3U-1000P",
             {"1": "nRESET", "2": "GND"}, lcsc="", mpn="B3U-1000P"),
        Part("P1", "elicio:PAD_8x8", "SIG1", "elicio:RING_PAD_D5_H2.7", {"1": "SIG1"}, in_bom=False),
        Part("P2", "elicio:PAD_8x8", "SIG2", "elicio:RING_PAD_D5_H2.7", {"1": "SIG2"}, in_bom=False),
        Part("P3", "elicio:PAD_8x8", "REF", "elicio:RING_PAD_D5_H2.7", {"1": "REF"}, in_bom=False),
        Part("P4", "elicio:PAD_8x8", "CHARGE_VBUS", "elicio:RING_PAD_D4.6_H2.7", {"1": "VBUS"}, in_bom=False),
        Part("P5", "elicio:PAD_8x8", "CHARGE_GND", "elicio:RING_PAD_D4.6_H2.7", {"1": "GND"}, in_bom=False),
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
        r("R26", "10k", "nRESET", "+VDD"),
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
