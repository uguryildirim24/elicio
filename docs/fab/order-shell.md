# Order the shell (v2)

Phone sheet. Order 2 is the printed body and lid. It is not the board.
No agent places this order. You pay only after every box in the
checkout gate is ticked.

I wrote this from `docs/fab/plan-v2.md` §7 and §9 and from the ledger
`docs/fab/orders-v2.md`. Destination Massachusetts, USA, assumed until
you confirm (plan v2 §9, D-8).

Site: [jlcpcb.com/3d-printing](https://jlcpcb.com/3d-printing) (JLC3DP,
default). Material page: [PA12-HP Nylon](https://jlc3dp.com/help/article/pa12-hp-nylon)
(plan v2 §9, §12). US quote-only route: Xometry (plan v2 §9). No quote
was requested.

---

## Gate G8 first

Do not open a vendor cart until this ledger check is done.
`docs/fab/orders-v2.md` must show all of the following before you pay.

| Must show | Tick |
|---|---|
| This order's reserved maximum $50–90 is present (plan v2 §9) | [ ] |
| That reserve was in place before order 1 was paid | [ ] |
| Ceiling row has a number you wrote (Q33). G8 is not passed while that row is blank | [ ] |
| Live checkout for this shell, once filled, sits inside the $50–90 reserved maximum | [ ] |
| Live checkout plus the other live lines sits under your ceiling | [ ] |
| Duties are the DDP figure the JLC checkout shows, or a documented reserve | [ ] |
| Colour is grey, or dyed black only if you already chose Q30 in writing | [ ] |

Named cuts if R8 fails (plan v2 §9): grey instead of dyed, no spare
lid.

S3 (plan v2 §10): pay this order after S2, inside the reserved
maximum. Do not pay it before the board is ordered unless you write
that change.

---

## Do not order if

Stop. Do not pay if any line is true.

1. G8 above is not ticked.
2. `docs/fab/cad/v2/manifest.json` is missing, or its
   `stage_b_failing` list is not empty. On this tree it lists
   `V2_CLOSURE`, `V2_EDGE_radii`, `V2_USB_end`, `V2_WALL_minima`
   (review r6, decisions 71 and 72). Rows marked NOT_MEASURED are named
   in `shell-v2.md` §6 and are not a pass.
3. You have not approved both renders (`render_medial.png` and
   `render_lateral.png` in `docs/fab/cad/v2/`, expected from WP14).
4. M1 is below 50.90 mm (`measure.md`, `packing-v2.md` §6).
5. The 50 mm bar on the paper template was not 50 mm.
6. A checkout field I left as "the agent fills this after WP14" is
   still blank.

---

## Files to upload

From `docs/fab/cad/v2/` (WP14; manifest `parts`: `body_full_p15`,
`lid`). Plan v2 §9 contents: body, lid, spare lid, stand if printed.

| File | Quantity | Notes |
|---|---:|---|
| `body_full_p15.stl` | 1 | body with hook |
| `lid.stl` | 2 | Named cut if R8 fails: 1 |
| Stand | 0 | WP14 drew no stand |
| `body_full_p15.step`, `.3mf`, `lid.step`, `.3mf` | — | keep; upload only if the vendor page asks |

JLC3DP takes STL on the 3D page (v1 order sheet).

---

## JLC3DP service and options

Set every line I filled. Do not substitute. Where I wrote "the agent
fills this after WP14", wait.

| Option | Set this | Source |
|---|---|---|
| Service | JLC3DP 3D printing | plan v2 §9 |
| Process | MJF (Nylon) | plan v2 §9 |
| Material | PA12-HP | plan v2 §9; jlc3dp.com/help/article/pa12-hp-nylon |
| Colour | Natural Grey default. Dyed Black only if you already wrote Q30 | plan v2 §7, Q30; option names from `L7-research-v4.md` §5 |
| Finish | Standard (as printed, bead-blasted). Not Chemical Vapor Smoothing unless the vendor's page states skin-contact testing of the smoothed part | plan v2 §7 R3; C1 open; option names from `L7-research-v4.md` §5 |
| Ship to | Massachusetts, USA | plan v2 §9 |
| Shipping | DDP as the JLC checkout shows it. Do not pick CPT | plan v2 §9 |
| Duties | Write the DDP figure the checkout shows | plan v2 §9, §12 C13 |

JLC "from $1.00, 72 h" is a starting price only (plan v2 §9). It is not
this part's price.

Allowance and reserved maximum: $50–90 (plan v2 §9, 2026-09-17). If
the live delivered total is above $90, stop. Do not pay. Write me one
line.

US quote-only (Xometry): no quote was requested. Do not open that cart
unless you ask me to fill it after WP14.

---

## Checkout gate

Tick each box. Stop on any miss. Write the live numbers into
`docs/fab/orders-v2.md`. Then pay, or do not pay.

| Must show | Live number | Tick |
|---|---|---|
| Process MJF, material PA12-HP, colour as above | $________ | [ ] |
| Quantities match the manifest | — | [ ] |
| Shipping DDP | $________ | [ ] |
| Tax collected, or Massachusetts 6.25 % use tax noted | $________ | [ ] |
| Import collection as DDP shows it | $________ | [ ] |
| Delivered line for this cart | $________ | [ ] |
| Delivered line ≤ $90 reserved maximum | — | [ ] |
| Both renders approved | — | [ ] |

---

## Write back

```
date                 ________
G8 ticked            ________
renders approved     ________
colour (Q30)         ________
spare lid            ________  (yes / no)
DDP duties $         ________
tax $                ________
delivered $          ________
paid                 ________  (yes / no)
```
