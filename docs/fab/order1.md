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
2. The CAD manifest records a failed §3.3 check.
3. M1 is below the chord gate in `measure.md` (50.9 mm at the default bow).
4. The quote page shows a wall-thickness DFM warning. That goes back to WP2.
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

Six parts, five files. If `manifest.json` lists different quantities, use
the manifest.

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
| Parts: MJF PA12-HP natural grey, 3 bodies, 2 lids, 1 coupon | $17–24 | $________ | [ ] |
| Import collection at checkout, 40 % of parts | $7–10 UNVERIFIED | $________ | [ ] |
| Global Standard DDP 10–14 d | $6–10 UNVERIFIED | $________ | [ ] |
| or DHL DDP 3–5 d | $22–28 UNVERIFIED | $________ | [ ] |
| Delivered total, Standard | $30–44 allowance; gate $55 | $________ | [ ] |
| Delivered total, DHL | $46–62 allowance; gate $75 | $________ | [ ] |

**Rule for a price outside the allowance.** Do not pay. Write the live
number in `orders.md`. No line may exceed $200. If you chose Standard, the
delivered total must be at most $55. If you chose DHL, the delivered total
must be at most $75. A total inside the gate but outside the allowance
band still stops; do not pay.

The quote page must also show, before you pay:

| Must show | Tick |
|---|---|
| Parts and finish match the manifest (MJF, PA12-HP, natural grey, quantities above) | [ ] |
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

1. Tape the hook of `body_full_p15` to a table so the hook cannot move. The
   tail hangs free.
2. Hang the 100 g mass from the tail tip.
3. Measure how far the tail tip dropped. Write millimetres.

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
Write the number in `orders.md`. Stop changing the hook.

### Closure (plan §3.7 item 7)

First lid on the first full body. Lid on and off ten times. Lip, web,
tongue, and nubs intact. If the lip fails, two wraps of paper medical tape
at s 10 and s 40 for the remaining wear items. Record that fallback. Tape
does not qualify the snap for an active pod.

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
