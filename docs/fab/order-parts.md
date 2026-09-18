# Order the small parts (v2)

Phone sheet. Order 3 is screws, standoffs, cell, tools, foam, plugs,
leads, electrodes, and the nickel kit or your written waiver. The
conditional first-load kit is a separate cart if G4 falls to you.
No agent places these orders. You pay only after every box in the
checkout gate is ticked.

I wrote this from `docs/fab/plan-v2.md` §9, `docs/fab/orders-v2.md`,
and `docs/fab/L6-research-v3.md` §6–§7. Destination Massachusetts,
USA, assumed until you confirm (plan v2 §9, D-8). Each purchased pack
is its own parcel (plan v2 §9).

---

## Gate G8 first

Do not open a vendor cart until this ledger check is done.
`docs/fab/orders-v2.md` must show all of the following before you pay.

| Must show | Tick |
|---|---|
| Order 2 reserved maximum $50–90 is present (plan v2 §9) | [ ] |
| Ceiling row has a number you wrote (Q33). G8 is not passed while that row is blank | [ ] |
| Live lines for these parcels, once filled, sit under that ceiling with the shell reserve | [ ] |
| The $80–130 small-parts allowance is not treated as a verified total for the 100-pack standoff route | [ ] |
| Cell line is still open (Q55) unless a 501015-class pack with a page price is on the ledger | [ ] |
| Probe kit is not in the cart unless G4 has named the kit (Q64) | [ ] |

Named cuts if R8 fails (plan v2 §9): no programming kit if the factory
programs.

---

## Do not order if

Stop. Do not pay if any line is true.

1. G8 above is not ticked.
2. M1 is below 50.90 mm (`measure.md`).
3. The cell SKU is still blank (Q55, gate G1) and you are buying a cell.
4. The first-load probe is in the cart and G4 has not named the kit
   (Q64).
5. A line I left as "the agent fills this after WP12b/WP14" is the
   thing you are about to buy.

---

## Parcels

One line per parcel, copied from `docs/fab/orders-v2.md`. Shipping,
tax, and import collection stay blank until that checkout shows them.
Do not sum these into a total.

| Parcel | Qty | Status | Unit price as displayed | Source | Ship to |
|---|---|---|---|---|---|
| Sortafast SF-BH2504-10, Grade 5 Ti ISO 7380 M2.5×4 button heads | 1 pack of 10 | catalogue | $17.50 per 10-pack | sortafast.com/products/sortafast-titanium-screws-button-head-10pk-m2-5 , 2026-09-17 (`L6-research-v3.md` §7.1, `orders-v2.md`) | Massachusetts |
| Spacer Express LAI-FF-M2.5-SW5-L3-100, 3.0 mm female-female M2.5, 5 mm A/F | 1 pack of 100 as sold | catalogue | €91.08 ex VAT per 100; shipping to Massachusetts unverified | spacer-express.com … L3-100 , 2026-09-17 (plan v2 §12 C14, `orders-v2.md`) | Massachusetts |
| Harwin R25-1000402 4.0 mm standoff | do not buy for this winner | catalogue | $0.57 at qty-1 on DigiKey 2026-09-17 | Winner standoff is 3.0 mm (`packing-v2.md` §5). 4.0 mm stays on the ledger as the unused candidate | — |
| Cell 501015-class | 1 | allowance | blank | Q55; no verified page price in ones on the ledger | Massachusetts |
| Data Power DTP301120 (SparkFun PRT-25270) | do not buy unless WP11b closes a longer body | catalogue | $7.39 | sparkfun.com/products/25270 , 2026-09-17 | — |
| 1.5 mm hex key | 1 | allowance | blank | plan v2 §9 | Massachusetts |
| USB-C cable | 1 | allowance | blank | plan v2 §9 | Massachusetts |
| Pre-cut foam pads | blank | allowance | blank | plan v2 §9 | Massachusetts |
| Silicone port plugs | 3 | allowance | blank | plan v2 §9 | Massachusetts |
| Snap-electrode leads with 2.54 mm pin sockets | 3 | allowance | blank | plan v2 §9, §5.6 | Massachusetts |
| Gel electrodes | blank | allowance | blank | plan v2 §9 | Massachusetts |
| Nickel test kit, or your written waiver | blank | allowance | blank | plan v2 §9 | Massachusetts |
| Multimeter | 1 when needed | allowance | blank | plan v2 §9, R2b, assembly step 6 | Massachusetts |

Exact SKUs for the hex key, USB-C cable, foam, plugs, leads, gel, and
nickel kit: the agent fills this after WP12b/WP14. Foam thickness on
the winner is 0.5 mm (Q57, `packing-v2.md` §5).

Winner standoff is 3.0 mm (`packing-v2.md` §5). The 100-pack is the
catalogue route. It is not a verified delivered total (plan v2 §9).

---

## Conditional first-load kit (Q64)

In only if G4 falls to you (plan v2 §8, §9, Q48). US sellers. Listed
prices are not a complete kit price. Allowance $50–70 (plan v2 §9).

The cable is decided. The probe is not.

| Parcel | Qty | Status | Unit price as displayed | Source |
|---|---|---|---|---|
| Tag-Connect TC2030-IDC-NL | 1 | catalogue | $33.95 listed | tag-connect.com/product/tc2030-idc-nl , 2026-09-17 (plan v2 turn 04 and 06) |
| Jumpers | blank | allowance | blank | plan v2 §9 |

Two probe options exist (Q64). G4 is not passable with option 1 on
paper. I name one of these before you buy. I do not name one in this
sheet. You buy nothing until G4 names the kit (Q64).

| Option | What it is | Source |
|---|---|---|
| 1. Raspberry Pi Debug Probe | $12.00 listed; page states 3.3 V nominal I/O only; no target-voltage sensing | plan v2 §8 and §9; raspberrypi.com/documentation/microcontrollers/debug-probe.html ; `board-v2.md` §4; `L6-research-v3.md` §6.1 |
| 2. Target-voltage-sensing probe or a level shifter | J-Link EDU Mini class, page price, or an external bidirectional level shifter; verified by the next research package | Q64; `L6-research-v3.md` §6.1 (1.8 V targets need a shifter) |

Factory programming that sets REGOUT0 can drop the kit (Q64, plan v2
§9 named cut). That service is quote-only (plan v2 §12 C6).

Kit shipment is its own parcel. Massachusetts. Tax blank until
checkout.

---

## Checkout gate

Tick each box per parcel. Stop on any miss. Write the live numbers
into `docs/fab/orders-v2.md`. Then pay that parcel, or do not pay.

| Parcel | Live delivered $ | Tax $ | Duties $ | Tick |
|---|---|---|---|---|
| Sortafast screws | $________ | $________ | $________ | [ ] |
| Spacer Express 3.0 mm 100-pack | $________ | $________ | $________ | [ ] |
| Cell (only if Q55 closed) | $________ | $________ | $________ | [ ] |
| Hex key | $________ | $________ | $________ | [ ] |
| USB-C cable | $________ | $________ | $________ | [ ] |
| Foam | $________ | $________ | $________ | [ ] |
| Port plugs | $________ | $________ | $________ | [ ] |
| Snap leads | $________ | $________ | $________ | [ ] |
| Gel electrodes | $________ | $________ | $________ | [ ] |
| Nickel kit or waiver on file | $________ | $________ | — | [ ] |
| Multimeter if needed | $________ | $________ | $________ | [ ] |
| TC2030-IDC-NL only if G4 named the kit | $________ | $________ | $________ | [ ] |
| Named probe only if G4 named the kit | $________ | $________ | $________ | [ ] |

Duties: write what that checkout shows. JLC DDP does not apply to
these domestic and EU parcels. Spacer Express shipping to Massachusetts
is unverified (`orders-v2.md`).

---

## Write back

```
date                      ________
G8 ticked                 ________
parcels paid              ________
cell SKU (Q55)            ________
nickel kit or waiver      ________
G4 named kit              ________  (yes / no)
probe I named before buy  ________
delivered $ per parcel    (copy into the ledger; no total)
```
