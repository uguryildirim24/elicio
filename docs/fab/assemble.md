# Assemble and first load (v2)

Phone sheet. Eight steps, one 1.5 mm hex key (plan v2 §8). No
soldering. No glue. No crimping. No wire stripping. Off-body until
step 8 says otherwise. Electrodes stay off for first load.

I wrote this from `docs/fab/plan-v2.md` §7 and §8, `docs/fab/board-v2.md`
§4, and `docs/fab/firmware-v2.md`. Pictures named below are expected
from WP14. If a file is missing, stop. Write me one line.

If a step fails: stop. Write me one line with the step number and what
you saw.

---

## Before you start

M1 passed (`measure.md`). Board, shell, and parts are on the desk.
G1b pack and connector revision are the ones WP17 verified. If G1b is
still open, stop before step 6.

Tool: 1.5 mm hex key (plan v2 §8). Multimeter for step 6 (R2b).

---

## Step 1

Peel the pre-cut foam pad and lay the cell in its pocket; route its
lead in the channel to the connector. (plan v2 §8)

**Tool.** Fingers. No hex key yet.
**Part.** Pre-cut foam 0.5 mm (Q57) and the G1b cell. The pocket is
the 501015 bare-cell envelope, centre (7.00, 9.30) mm; the record cell
is the 501012 pack, 2.6 mm shorter along the pocket, and foam fills the
gap (`packing-v2.md` §5; the route is decision 69).
**Check.** Foam is down. Cell sits in the pocket. Lead lies in the
channel and is not pinched.
**Picture.** `docs/fab/cad/v2/drawing.pdf` cell-pocket view (expected;
WP14).

---

## Step 2

Push the three titanium screws through the dome holes from outside.
(plan v2 §8)

**Tool.** Fingers.
**Part.** Three Sortafast SF-BH2504-10 Grade 5 titanium ISO 7380
M2.5×4 button heads (`L6-research-v3.md` §7.1). Sites C1, C2, REF on
the template.
**Check.** Each head is on the outside. Threads show inside the three
hex pockets. Nothing is started on the thread yet.
**Picture.** `docs/fab/cad/v2/render_lateral.png` (expected; WP14).

---

## Step 3

Drop a brass standoff into each hex pocket inside; turn each screw
with the hex key until the head seats. Stop. (plan v2 §8)

**Tool.** 1.5 mm hex key.
**Part.** Three 3.0 mm female-female M2.5 standoffs, 5 mm across flats
(winner `V2_STANDOFF` 3.0, `packing-v2.md` §5). Spacer Express
LAI-FF-M2.5-SW5-L3-100 is the catalogue pack (`orders-v2.md`).
**Check.** Each standoff sits in its hex pocket. Each screw head is
seated on the dome face. Stop. Do not keep turning.
**Picture.** `docs/fab/cad/v2/drawing.pdf` contact-stack section
(expected; WP14). Q58: no nut. The standoff's female thread takes the
screw.

---

## Step 4

Set the board on the three standoff tops, pads down, holes over the
bosses. (plan v2 §8)

**Tool.** Fingers. Board powered off. Electrodes off.
**Part.** The assembled flex from order 1, tabs already at the rings.
**Check.** Board underside rests on the standoff tops. Pads face
the standoffs. USB-C is at the hook-end end face (`packing-v2.md` §5).
The board has no mounting holes, and the REF standoff sits past the
board's end, so the island rests on two standoffs. The shell's two
printed bosses have nothing to screw into (review r6, decision 74).
**Picture.** `docs/fab/cad/v2/drawing.pdf` board-on-standoffs view
(expected; WP14).

---

## Step 5

Turn the board screws with the hex key until they seat. (plan v2 §8)

**Tool.** 1.5 mm hex key.
**Part.** The board screws WP14 names. On this tree it names none
(decision 74). Stop here. Write me one line.
**Check.** Screws seat. Board does not rock. Tabs are not folded
against the cavity end wall (Q59). If a tab fights the wall, stop.
**Picture.** `docs/fab/cad/v2/render_medial.png` (expected; WP14).

---

## Step 6

Mate only the G1b-qualified pack and connector revision. Before
plugging it in, verify electrical polarity at the identified connector
contacts with the sheet's off-body method (a multimeter on the
connector's contacts, or the supplier's documented test); neither
keying nor insulation colour proves polarity (the legacy drawing even
labels black as positive). The meter is in R2b and order 3.
(plan v2 §8)

**Tool.** Multimeter, DC volts, off-body.
**Part.** Only the G1b-qualified pack and connector revision.
**Check.** Meter on the connector contacts. Write plus and minus as
the meter reads them. Then plug. If G1b is still open (`board-v2.md`
§19 item 1), stop. Do not plug.
**Picture.** `docs/fab/cad/v2/drawing.pdf` connector view (expected;
WP14).

**Write polarity.** + at ________   − at ________

---

## Step 7

Close the lid per WP14's closure. (plan v2 §8)

**Tool.** Fingers. Hex key only if WP14's closure is the concealed tail
screw (plan v2 §7). On this tree the lid has no undercut and lifts off
(`V2_CLOSURE`, decision 72). Stop until that is decided.
**Part.** The lid from order 2.
**Check.** Lid is seated. Seam is the one WP14 drew. No screw shows on
the lateral face (plan v2 §7).
**Picture.** `docs/fab/cad/v2/render_lateral.png` seated lid (expected;
WP14). Closure drawing: `docs/fab/cad/v2/drawing.pdf` (expected;
WP14).

---

## Step 8

Lay the device medial side up on the desk, plug USB-C from a power
bank or a listed adapter, read the LED as the sheet defines it.
(plan v2 §8)

**Tool.** USB-C cable from a power bank that is not itself plugged in,
or a listed Class II adapter (Q41 / plan v2 R7). Device stays on the
desk. Electrodes off.
**Part.** The closed device from step 7.
**Check.** LED meaning (`board-v2.md` §5): the LED can light only with
USB VBUS present. It draws nothing from VBAT. Firmware drives LED_EN.
If no firmware is loaded, write "LED dark" or "LED lit" as seen. That
is a note, not a pass.
**Picture.** `docs/fab/cad/v2/render_medial.png` USB-C at the hook
(expected; WP14).

Firmware after a bootloader is present: copy the UF2 file to the drive
that appears (`firmware-v2.md`; plan v2 §8). Recovery: lid off,
double-press the small switch, copy again (plan v2 §8; Adafruit
double-reset within 500 ms, `L6-research-v3.md` §6.3).

---

## Closure check (plan v2 §7, qualitative)

The lid does not open under a firm two-finger pull.

**Write pull.** ________ (stayed closed / opened)

## Drop check (plan v2 §7, qualitative)

0.5 m drop onto a wooden table with the lid staying closed. Labelled
qualitative. Device off. Cell plugged. Electrodes off.

**Write drop.** ________ (lid stayed closed / lid opened / other)

---

## First load (only if G4 falls to you)

Once, before assembly. Rehearse this section on paper first. Physical
completion time is recorded at the first off-body execution. It is
measured, not promised (plan v2 §8).

Target runs from its own cell, off-body, electrodes disconnected
(`board-v2.md` §4). Ground first (`L6-research-v3.md` §6.1).

Kit on paper (plan v2 §8): Tag-Connect TC2030-IDC-NL, $33.95 listed,
keyed orientation, plus a probe. Plan v2 §8 names the Raspberry Pi Debug
Probe; it is not the probe for an erased part (3.3 V nominal I/O, no
VTref sensing, target at 1.8 V with a 2.1 V absolute maximum; Q64).
`L7-research-v4.md` §1.3 lists three VTref-sensing probes (ST-LINK
V3MINIE, Black Magic Probe V2.3, J-Link EDU Mini); none is picked here.
Do not run this section until G4 names the kit (`order-parts.md`).

### Net map (`board-v2.md` §4)

TC2030-IDC-NL contacts 1–6 map one-for-one to IDC 1–6 (plan v2 §8,
Tag-Connect Rev. B).

| IDC | TC2030 pin | Net | Probe lead (kit named at G4) | Rule |
|---|---|---|---|---|
| 1 | 1 | +VDD | VTref sense only | No power feed from the probe |
| 2 | 2 | SWDIO | SWDIO | Module pin 51 |
| 3 | 3 | GND | GND | Ground first |
| 4 | 4 | SWDCLK | SWCLK | Module pin 53 |
| 5 | 5 | GND | GND | |
| 6 | 6 | nRESET | nRESET | Module pin 40 (P0.18), shared with SW1 |

### REGOUT0 (`board-v2.md` §4)

+VDD is 3.0 V only once firmware has written UICR REGOUT0 = 3.0 V. An
erased nRF52840 in high-voltage mode starts REG0 at 1.8 V, so on first
load the target is at 1.8 V (`firmware-v2.md`). Compatibility is not
inferred from the probe's 3.3 V nominal I/O. G4 verifies both
directions at the powered target's actual voltage.

### Commands (`firmware-v2.md`, documented, not run on this tree)

Application update after the bootloader is present: copy the UF2 from
the compile output to the `FTHR840BOOT` volume.

Merged bootloader plus SoftDevice, only when G4 uses the kit.
Stand-in image: `feather_nrf52840_express_bootloader-0.11.0_s140_6.1.1.hex`
(Adafruit nRF52 Bootloader 0.11.0, SoftDevice S140 6.1.1,
`firmware-v2.md`). Product hex: the agent fills this after WP13b.

pyOCD (not installed on the firmware lane's round):

```
pyocd flash -t nrf52840 \
  feather_nrf52840_express_bootloader-0.11.0_s140_6.1.1.hex
```

OpenOCD (not installed on that round), Adafruit core DAPLink script:

```
openocd -f interface/cmsis-dap.cfg \
  -f "$HOME/Library/Arduino15/packages/adafruit/hardware/nrf52/1.7.0/scripts/openocd/daplink_nrf52.cfg" \
  -c "program feather_nrf52840_express_bootloader-0.11.0_s140_6.1.1.hex verify reset exit"
```

The drive appearing over USB is the check (plan v2 §8).

**Write first-load time.** ________ (measured at the first off-body
execution, not promised)

**Write VTref at pin 1.** ________ V (meter; G4)

---

## Write back

```
date                 ________
step that stopped    ________  (none / number)
polarity + / −       ________
pull check           ________
drop check           ________
LED on USB           ________
UF2 drive seen       ________
first-load time      ________  (measured, not promised)
VTref V              ________
one line to me if a step failed:
________
```
