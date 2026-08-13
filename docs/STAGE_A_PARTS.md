# Stage A parts list

Order list for the Stage A bench amplifier in
[`EARPIECE_DESIGN.md`](EARPIECE_DESIGN.md), prepared 2026-08-13 at the
owner's request and given verified links the same day. Purchasing remains
the owner's explicit decision.

Stage A is deliberately zero-solder: DIP-package ICs on a breadboard and
pre-soldered breakout modules. A soldering iron becomes necessary at the
protoboard rebuild and Stage B, not before.

## Where to buy

**DigiKey for everything electronic, one cart.** It stocks genuine Texas
Instruments parts, resells Adafruit boards, and carries the passives,
breadboards, and batteries, so the whole electronic side ships together.
This matters most for the INA128: instrumentation amplifiers are a
commonly counterfeited part, and a fake one fails as a confusing noise
problem rather than an obvious dead part, which is the worst possible bug
to hit during first bring-up.

**Amazon for the electrode interface only.** DigiKey does not carry
pre-gelled medical electrodes or TENS snap leads. Those are the one
unavoidable second order.

Do not buy the INA128P or TL072CP from a marketplace seller to save a few
dollars. Everything else on this list is commodity and safe to buy
wherever is cheapest.

## DigiKey cart

Unit prices and stock read from DigiKey product pages on 2026-08-13.
Verify at checkout.

| Item | Part | DigiKey # | Qty | Unit price | Link |
| --- | --- | --- | --- | --- | --- |
| Instrumentation amplifier | TI INA128P, 8-DIP | INA128P-ND | 2 | $22.35 | [product page](https://www.digikey.com/en/products/detail/texas-instruments/INA128P/251085) |
| Dual op-amp | TI TL072CP, 8-PDIP | 296-1775-5-ND | 3 | $1.20 | [product page](https://www.digikey.com/en/products/detail/texas-instruments/TL072CP/277421) |
| Small-signal diode | onsemi 1N4148, DO-35 | see page | 20 | $0.10 | [product page](https://www.digikey.com/en/products/detail/onsemi/1N4148/458603) |
| Multi-turn trimmer | Bourns 3296W-1-104LF, 100 kOhm | 3296W-104LF-ND | 3 | $2.38 | [product page](https://www.digikey.com/en/products/detail/bourns-inc/3296W-1-104LF/3296W-104LF-ND/1088046) |
| ADC breakout | Adafruit 1085, ADS1115 16-bit 860 SPS | 1528-1085-ND | 1 | $14.95 | [product page](https://www.digikey.com/en/products/detail/adafruit-industries-llc/1085/5761229) |
| Microcontroller | Espressif ESP32-DEVKITC-32E | 1965-ESP32-DEVKITC-32E-ND | 1 | $10.00 | [product page](https://www.digikey.com/en/products/detail/espressif-systems/ESP32-DEVKITC-32E/12091810) |

**Verified subtotal: $82.39** for the six rows above at the listed
quantities. That figure is arithmetic on prices actually read from the
product pages; the rows below were not priced individually.

### Passives, by exact value

Buy the specific values the circuit needs rather than an assortment kit.
The design calls for eight resistor values and a kit is a quality
lottery; individually they run roughly $0.10 each, so ten of each value
is a few dollars and every one is a known 1% metal film part.

Yageo MFR-25FBF52 series, 1% metal film, 1/4 W. Order 10 each of:
**4.7k, 5.6k, 10k, 22k, 82k, 100k, 220k, 1M**.

- [MFR-25FBF52-10K](https://www.digikey.com/en/products/detail/yageo/MFR-25FBF52-10K/13219) and
  [MFR-25FBF52-1M](https://www.digikey.com/en/products/detail/yageo/MFR-25FBF52-1M/13714)
  are confirmed live; the remaining values follow the same part-number
  pattern and are found by searching the series name on DigiKey.

Capacitors, from the [DigiKey capacitor category](https://www.digikey.com/en/products/filter/capacitors/3):
**100 nF film** (high-pass), **10 nF and 22 nF film** (Sallen-Key),
**100 nF ceramic** (supply decoupling, 10 pcs), **10 uF electrolytic**
(2 pcs). Values not priced individually here.

### Bench items

Not priced individually; buy on DigiKey with the rest or wherever is
cheaper.

| Item | Spec | Qty |
| --- | --- | --- |
| Breadboard | Full-size solderless | 2 |
| Jumper wire kit | Pre-formed, assorted lengths | 1 |
| 9 V batteries | Alkaline | 4 |
| 9 V snap clips | With flying leads | 2 |

## Amazon cart

| Item | Spec | Qty | Est. price | Link |
| --- | --- | --- | --- | --- |
| Pre-gelled electrodes | Dealmed snap Ag/AgCl, 35 mm, 50 count | 1 pack | ~$11 | [listing](https://www.amazon.com/Dealmed-Disposable-Electrodes-Pregelled-Adhesive/dp/B0CNJ1Z35V) |
| Snap lead wires | TENS-style snap leads, or snap-to-alligator | 2 sets | ~$8-10 | search "TENS snap lead wires" |

Electrodes are the ground truth for Stage A. Printed conductive-TPU
electrodes come at Stage B and are compared against these, not instead
of them.

## Price correction, 2026-08-13

The first version of this list estimated the INA128P at $10-13 and a
core total of roughly $90-110. Checked against the DigiKey product page,
the INA128P is **$22.35** at quantity one. It is the single largest line
item and the earlier estimate was low by roughly half.

Consequences worth knowing before ordering:

- Two INA128P is $44.70, over half the verified subtotal. Buying one
  saves $22.35 and is the obvious place to economise, but the
  instrumentation amplifier is both the heart of the circuit and the part
  most likely to die from a breadboard wiring mistake. A week of shipping
  in the middle of first bring-up costs more than the spare does.
- The natural cheaper substitute, the INA126P, is **discontinued** at
  DigiKey and is not an option. Any substitution would change the gain
  equation and the noise floor, so it is a design decision, not a
  shopping decision, and belongs in `EARPIECE_DESIGN.md` first.

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
