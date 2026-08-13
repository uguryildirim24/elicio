# Stage A parts list

Order list for the Stage A bench amplifier in
[`EARPIECE_DESIGN.md`](EARPIECE_DESIGN.md), prepared 2026-08-13 at the
owner's request. Prices are US estimates checked against distributor and
retailer listings on that date; verify at checkout. Purchasing remains the
owner's explicit decision.

Stage A is deliberately zero-solder: DIP-package ICs on a breadboard and
pre-soldered breakout modules. A soldering iron becomes necessary at the
protoboard rebuild and Stage B, not before.

## Core electronics

| Item | Spec | Qty | Est. price | Source |
| --- | --- | --- | --- | --- |
| Instrumentation amplifier | TI INA128P, DIP-8 | 2 (one spare) | $10-13 each | DigiKey / Mouser |
| Dual op-amp | TL072CP or TL072IP, DIP-8 | 3 | ~$1 each | DigiKey / Mouser (add to same order) |
| Small-signal diodes | 1N4148 | 20 | ~$2 total | Same order |
| Multi-turn trimmer | 100 kOhm, 3296W style | 10-pack | $6-8 | Same order or Amazon |
| Resistor kit | 1% metal film assortment (must include 4.7k, 5.6k, 10k, 22k, 82k, 100k, 220k, 1M) | 1 kit | $10-15 | Amazon |
| Capacitor kit | Film + ceramic assortment (must include 10 nF, 22 nF, 100 nF film; 100 nF ceramic; 10 uF electrolytic) | 1 kit | $10-15 | Amazon |

## Data path

| Item | Spec | Qty | Est. price | Source |
| --- | --- | --- | --- | --- |
| ADC breakout | ADS1115, 16-bit, 860 SPS, I2C; buy pre-soldered headers | 1 | $15 genuine Adafruit #1085; $8-10 generic | Adafruit / Amazon |
| Microcontroller | Any ESP32 dev board with USB (ESP32-WROOM DevKitC class) | 1 | $8-12 | Amazon / Adafruit |
| USB data cable | Match the dev board's connector | 1 | $5 if not owned | Anywhere |

## Electrodes and interface

| Item | Spec | Qty | Est. price | Source |
| --- | --- | --- | --- | --- |
| Pre-gelled electrodes | Ag/AgCl snap, ~35 mm, 50-pack (ground truth; printed electrodes come later) | 1 pack | $10-13 | Amazon (e.g. Dealmed 50-count) |
| Snap lead wires | TENS-style snap leads, or snap-to-alligator | 2 sets | $8-10 | Amazon |

## Power and bench

| Item | Spec | Qty | Est. price | Source |
| --- | --- | --- | --- | --- |
| 9 V batteries | Alkaline | 4 | ~$10 | Anywhere |
| 9 V snap clips | With flying leads | 2 | ~$3 | Amazon / same distributor order |
| Breadboards | Full-size, with a jumper-wire kit | 2 + kit | $12-15 | Amazon |

**Core total: roughly $90-110** all-new; less if kits or a dev board are
already owned.

## Only if not already owned

| Item | Spec | Est. price |
| --- | --- | --- |
| Multimeter | Basic DMM with DC millivolt range | $15-30 |

## Deliberately not on this list yet

Do not buy these until their stage is reached: conductive TPU filament
(Stage B printed electrodes), regular TPU for the pod, a MEMS barometer and
piezo discs (Stage C canal tip), any ADS1299 or custom PCB work, and any
soldering equipment. Stage A must prove the channel first.

## Safety, restated

Everything touching skin runs from the 9 V batteries only. Never connect
mains-powered equipment to the electrode side; during tethered debugging the
laptop runs on battery. The 220 kOhm series resistors and clamp diodes go in
before the first electrode is ever worn.
