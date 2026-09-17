# Order 1 — fit gauge checkout

Phone sheet. Order 1 is a passive nylon gauge for the ear. It is not the
electronics. No agent places this order. You pay only after every box in
the checkout gate is ticked.

Site: [jlcpcb.com/3d-printing](https://jlcpcb.com/3d-printing) (read
2026-09-16). Material page: [PA12-HP Nylon](https://jlc3dp.com/help/article/pa12-hp-nylon)
(updated 2026-07-30). Tariff FAQ:
[US tariff policy](https://jlcpcb.com/help/article/us-tariff-policy-faq)
(updated 2026-09-09, read 2026-09-16). Vendor notes: `docs/fab/L2-vendors.md`.

Allowances below are dated 2026-09-16. They are not quotes. Where a line
is marked UNVERIFIED, read the live number on the checkout page and write
it in `orders.md`.

---

## Do not order if

Stop. Do not pay if any line is true.

1. You have not approved both renders (`render_medial.png` and
   `render_lateral.png` in `docs/fab/cad/v1/`).
2. `docs/fab/cad/v1/manifest.json` is missing, or any entry in its
   `checks` list has `"passed": false`.
3. Your M1 is below `chord_gate.gate` in `manifest.json` (50.901 mm at the
   default bow 3; `measure.md` gives the caliper number for your bow).
4. The quote page shows a wall-thickness DFM warning on a feature that is
   not one of the five deliberate thin features: lid tongue 0.5 mm (E1),
   body rib 0.8 (E2), lid nubs 0.8 (E3), coupon rib 0.4 (E4), lid lip 1.0
   and its bump 0.5 (E5). Write down what the warning names. A warning on
   any other wall goes back to WP2.
5. The colour is black, or any dye, unless you already have a JLC finishing
   statement for that finish (plan §10 item 7). Order 1 is natural grey.

---

## Files to upload

From `docs/fab/cad/v1/`, upload these five `.stl` files (plan §3.6 names).
Each part also exists as `.step` and `.3mf`. The JLC 3D page takes the STL.

| File | Quantity |
|---|---:|
| `body_full_p15.stl` | 1 |
| `body_thin_p15.stl` | 1 |
| `body_full_p25.stl` | 1 |
| `lid.stl` | 2 |
| `coupon.stl` | 1 |

Six parts, five files. These match `parts` and `quantities` in
`manifest.json`; if they ever differ, do not order.

There is one lid design. It closes all three bodies: on the thin body it
sits 2.0 mm lower. The CAD script checks the lid seated on each body.

---

## JLC service and options

Set every line. Do not substitute.

| Option | Set this |
|---|---|
| Service | JLC3DP 3D printing |
| Process | MJF (Nylon) |
| Material | PA12-HP |
| Colour | Natural gray (JLC label; plan says natural grey) |
| Finish | As printed for PA12-HP. No dye. No black. |
| Ship to | Massachusetts, USA |
| Shipping | Global Standard DDP. If that option is absent, DHL DDP |

US individual orders ship DDP on this FAQ (claim 2, verified). Do not pick
CPT.

---

## Checkout gate

Tick each box. Stop on any miss. Write the live numbers. Then pay, or do
not pay.

Plan allowances and the rule if a live number sits outside them:

| Line | Allowance | Live number | Tick |
|---|---|---|---|
| Parts: MJF PA12-HP natural grey, 3 bodies, 2 lids, 1 coupon | $17–24 | $________ | written |
| Import collection at checkout, 40 % of parts | $7–10 UNVERIFIED | $________ | written |
| Global Standard DDP 10–14 d | $6–10 UNVERIFIED | $________ | written |
| or DHL DDP 3–5 d | $22–28 UNVERIFIED | $________ | written |
| Delivered total, Standard | $30–44 allowance; **gate $55** | $________ | [ ] at most $55 |
| Delivered total, DHL | $46–62 allowance; **gate $75** | $________ | [ ] at most $75 |

**Rule for a number outside the allowance.** The allowances are estimates
(plan §7), not the gate. A line outside its band is not a stop by itself:
write the live number in `orders.md`. The stops are these:

- any single line above $200;
- delivered total above $55 with Standard, or above $75 with DHL.

The quote page must also show, before you pay:

| Must show | Tick |
|---|---|
| Parts and finish match the manifest (MJF, PA12-HP, natural grey, quantities above) | [ ] |
| Delivered total at or under the gate above | [ ] |
| DDP, or a tariff line, is shown | [ ] |
| A delivery date is shown | [ ] |
| Both renders approved | [ ] |

40 % collection and the two shipping bands are UNVERIFIED (plan §8 claims
1 and 4). The PA12-HP unit price is not a quote (claim 3; JLC page "from
$1.00", 2026-07-30). The checkout page closes those numbers. Copy what it
shows.

---

## After you pay

Write one row in `docs/fab/orders.md`. Fill date, vendor, file names and
hashes from `manifest.json`, quantities, quoted and charged price by line,
duty, shipping, lead time, tracking. Leave inspection blank until the
parcel arrives.

Order number: ________
Charged total: $________

---

## When the parcel arrives

### Receipt

Count six parts: three bodies, two lids, one coupon. Write the inspection
in `orders.md`. Wear order for the bodies: full/1.5, then thin/1.5, then
full/2.5.

### Hook test (100 g at the tail tip)

Plan §3.7 does not list this test. Plan §9 row WP4 does. Do it on the
printed `body_full_p15` before the four-hour wear.

The plan estimate is 0.9 N at 1.5 mm hook preload (claim 13). Pass band
0.5 N to 1.5 N (plan §10 interface item 3). If the result is outside that
band, record it. Do not reprint. Do not change HOOK_DIA. WP6 decides.

**Tool.** Tape, thread, digital caliper, a 100 g mass. If you have no 100 g
weight, hang 100 ml of water in a thin bag. 100 ml of water is 100 g. 100 g
weighs 0.98 N (standard gravity).

The hook is held the way your ear holds it, and the load pushes the tail
tip the way your head does: at right angles to the dome face. You need a
box or a stack of books at least 10 cm tall.

1. Hold `body_full_p15` with the domes facing up. Tape the top of the hook
   arc (the curve that sits over your ear) to the top of the box at its
   edge, with two strips. The body sticks out level past the edge, domes
   up. Only the hook is taped.
2. Tie the thread round the tail tip. Do not hang anything yet.
3. Stand the caliper's depth rod on the table under the tail tip and
   measure up to the underside of the tip. Write it.

   Before: ________ mm

4. Hang the 100 g mass from the thread, clear of the table. Wait ten
   seconds. Measure the same way again.

   After: ________ mm

5. Drop = Before − After. Write it.

Tail drop: ________ mm

Force at 1.5 mm preload = `1.47 / drop_mm` newtons (0.98 N × 1.5 mm).

| Tail drop | Force at 1.5 mm |
|---|---|
| 1.0 mm | 1.5 N (stiff limit) |
| 1.6 mm | 0.9 N (plan estimate) |
| 2.9 mm | 0.5 N (soft limit) |

Force: ________ N

Pass: 0.5 N to 1.5 N. That is a drop from 1.0 mm through 2.9 mm.
Outside: too stiff (drop under 1.0 mm) or too soft (drop over 2.9 mm).
Write the number in `orders.md`. Keep wearing the parts as printed; the
hook is not changed in this order.

### Closure (plan §3.7 item 7)

First lid on the first full body. Lid on and off ten times. Lip, web,
tongue, and nubs intact. If the lip fails, wrap paper medical tape twice
round body and lid at two places: 10 mm and 40 mm from the hook end,
measured along the body's back edge with the caliper. Use the tape for the
remaining wear items and record that fallback. Tape does not qualify the
snap for an active pod.

Closure: pass / fail / tape ________

### Wear (plan §3.7)

About 4 g in the cavity (two M6 nuts) for the shake test. Remove at once
on pain, numbness, or skin reaction and write it. A red mark that lasts
more than 15 minutes after removal fails that variant.

For each body, in order full/1.5, thin/1.5, full/2.5:

1. On and off one-handed in under five seconds, no pulling the ear. ________
2. Stays put through ten head shakes, five hard clenches, three yawns, one
   flight of stairs, lid retained. ________
3. Wear 15 minutes, then one hour, then four hours. Inspect the skin each
   time. ________
4. Photos: front, side, back, with and without glasses. Front: nothing
   visible. Side: no more than a hearing aid. Back: your call. ________
5. Paper strip under each dome, pinched, head left, right, chin down. ________
6. Glasses on and off ten times. No lift. ________

Item 8 is an observation, not a biocompatibility claim. Item 9: mark dome
positions on the skin, photograph; that feeds WP7a.

### After §3.7 (plan §10 item 5)

Accepted thickness (full 9.0 mm or thin 7.0 mm): ________
Accepted preload (1.5 mm or 2.5 mm): ________
Back view, your call: ________
