# Order the board (v2)

Phone sheet. Order 1 is the assembled flex board. It is not the shell.
No agent places this order. You pay only after every box in the
checkout gate is ticked.

I wrote this from `docs/fab/plan-v2.md` §9, `docs/fab/board-v2.md` §18,
and the ledger `docs/fab/orders-v2.md`. Destination Massachusetts, USA,
assumed until you confirm (plan v2 §9, D-8).

Site: [jlcpcb.com](https://jlcpcb.com) (default route, Q44). US
quote-only route: MacroFab or Screaming Circuits (plan v2 §9). No quote
was requested.

---

## Gate G8 first

Do not open a vendor cart until this ledger check is done.
`docs/fab/orders-v2.md` must show all of the following before you pay.

| Must show | Tick |
|---|---|
| Order 2 reserved maximum $50–90 is present (plan v2 §9; reserved before order 1 is paid) | [ ] |
| Ceiling row has a number you wrote (Q33). G8 is not passed while that row is blank | [ ] |
| Live checkout for this board, once filled, sits under that ceiling with the shell reserve and the other live lines | [ ] |
| Every line is marked quoted, catalogue, or allowance | [ ] |
| No all-in total is claimed (plan v2 §9) | [ ] |
| Flex assembly fixture $49.25 for two fixtures is on the ledger (`board-v2.md` §18) | [ ] |
| FPC extra-stiffener fee is a named blank or a checkout figure, not a guess (`board-v2.md` §18) | [ ] |
| Duties are the DDP figure the JLC checkout shows, or a documented reserve, not a percentage used as a total (plan v2 §9, §12 C13) | [ ] |

Named cuts if R8 fails (plan v2 §9): grey instead of dyed, no spare
lid, two boards instead of five, no programming kit if the factory
programs.

---

## Do not order if

Stop. Do not pay if any line is true.

1. G8 above is not ticked.
2. `hardware/board/release/summary.json` is missing, or `"routed"` is
   not true (expected from WP12b; `scripts/board/release.py --routed`).
3. You have not approved the two renders in `docs/fab/cad/v2/`
   (expected from WP14).
4. M1 is below 50.90 mm (`measure.md`, `packing-v2.md` §6).
5. The Raytac route (Q67) is not picked on this sheet with the two
   prices in front of you at G3.
6. A checkout field I left as "the agent fills this after WP12b/WP14"
   is still blank.

---

## Files to upload

Expected from WP12b. Marked expected until that package writes them.

| File | Where | Use |
|---|---|---|
| Gerbers and drill | `hardware/board/release/gerbers/` (written by `scripts/board/release.py`; not committed) | JLC flex PCB |
| BOM | `hardware/board/release/bom.csv` (expected; WP12b) | PCBA |
| CPL | `hardware/board/release/cpl.csv` (expected; WP12b) | PCBA |
| Board STEP | `hardware/board/release/elicio-v2.step` (expected; WP12b) | 3D / DFM |
| Release summary | `hardware/board/release/summary.json` (expected; WP12b) | you read it; do not upload unless the checkout asks |

Gerber names as `release.py` writes them on this tree: `elicio-v2-F_Cu.gbr`,
`-B_Cu`, `-F_Mask`, `-B_Mask`, `-F_Paste`, `-B_Paste`, `-F_Silkscreen`,
`-B_Silkscreen`, `-Edge_Cuts`, `-User_Eco1` (stiffeners), `-User_Eco2`,
`-User_Drawings`, `-User_Comments` (all `.gbr`), `elicio-v2-PTH.drl`,
`elicio-v2-NPTH.drl`, `elicio-v2-job.gbrjob`. The copper is not routed:
`--routed` is refused (1293 DRC errors, 31 unconnected; review r6).

From `docs/fab/cad/v2/` (expected; WP14): nothing is uploaded to JLC
PCB. Those files are the shell order.

---

## JLC service and options

Set every line I filled. Do not substitute. Where I wrote "the agent
fills this after WP12b/WP14", wait.

| Option | Set this | Source |
|---|---|---|
| Service | JLCPCB PCB + standard PCBA | plan v2 §9 |
| Board type | 2-layer polyimide flex with FR4 stiffeners (interface II, Q50) | `board-v2.md` §12, §18; `orders-v2.md` |
| Quantity | 2 to 5 assembled boards. Named cut: two if R8 fails | plan v2 §9 |
| Surface | ENIG, 1 u" or 2 u" as the checkout offers (HASL is not offered on FPC) | plan v2 §9; `board-v2.md` §11 |
| Copper / stack | PI 0.11 mm, FR4 0.4 mm at parts, FR4 0.2 mm at the rings | `packing-v2.md` §5 |
| Coverlay | Yellow; opening 0.1 mm one-sided | `board-v2.md` §12 |
| Stiffeners | 2 × FR4 0.4 (Eco1: parts island, USB/pocket). Three FR4 0.2 ring pieces would make 5 and cross the fee threshold of 4 (decision 72) | `board-v2.md` §12, §18 |
| Extra-stiffener fee | none at 2 pieces; at 5, the figure the checkout shows | `board-v2.md` §18 |
| Assembly | Standard PCBA, sides per placement (two-sided assumed) | plan v2 §9 |
| Fixture | Flexible PCB, 2 fixtures for 1–29 pcs, $24.63 each, $49.25 | `board-v2.md` §18, jlcpcb.com/help/article/pcb-assembly-price read 2026-09-17 |
| X-ray | Module X-ray if the checkout offers it in the 1–10 bracket, $1.64 per inspected part | plan v2 §9 |
| Feeder | Standard tier $1.53 per part line. Not the economic $3.07 | plan v2 §9 |
| Setup | $25.56 one side or $51.12 two sides | plan v2 §9 |
| Stencil | $8.21 one side or $16.42 two sides | plan v2 §9 |
| Electrical test | No power-on test (JLC FPC assembly terms, `board-v2.md` §18) | `board-v2.md` §18 |
| Bootloader programming | the agent fills this after WP12b/WP17b (plan v2 §12 C6, quote-only) | plan v2 §9 |
| Ship to | Massachusetts, USA | plan v2 §9 |
| Shipping | DDP as the JLC checkout shows it. Do not pick CPT | plan v2 §9; JLC US tariff FAQ |
| Duties | Write the DDP figure the checkout shows. Do not invent a percentage total | plan v2 §9, §12 C13 |

Allowance for this order: $160–240 (plan v2 §9, 2026-09-17). That is
an allowance, not a delivered total. The $160–240 band was set for the
rigid board and is not re-derived for flex (Q61, `orders-v2.md`).

---

## Raytac route (Q67)

Pick one at G3 with both prices in front of you. I do not pick for you.

| Route | What it is | Source |
|---|---|---|
| JLC global sourcing | JLC buys MDBT50Q-1MV2 if it quotes that without a request on the day | Q54, Q67; `orders-v2.md` |
| Consignment | You buy the modules at DigiKey or Mouser, ship one parcel to JLC, and pay JLC's consignment fee | Q54, Q67 |

Both prices: the agent fills this after WP12b (library stock and the
consignment fee on the day).

**Write the route you pick.** ________

---

## Checkout gate

Tick each box. Stop on any miss. Write the live numbers into
`docs/fab/orders-v2.md`. Then pay, or do not pay.

| Must show | Live number | Tick |
|---|---|---|
| Parts match the flex stack above | $________ | [ ] |
| Fixture $49.25 or the live fixture line | $________ | [ ] |
| Extra-stiffener fee as shown, or written "none" | $________ | [ ] |
| Raytac line as the route you picked | $________ | [ ] |
| Shipping DDP | $________ | [ ] |
| Tax collected, or Massachusetts 6.25 % use tax noted | $________ | [ ] |
| Import collection as DDP shows it | $________ | [ ] |
| Delivered line for this cart | $________ | [ ] |
| Delivered line sits under your Q33 ceiling with the $50–90 shell reserve | — | [ ] |

US quote-only (MacroFab or Screaming Circuits): no quote was requested.
Do not open that cart unless you ask me to fill it after WP12b.

---

## Write back

```
date                 ________
G8 ticked            ________
M1 mm                ________
Raytac route (Q67)   ________
qty boards           ________
fixture live $       ________
extra-stiffener $    ________
DDP duties $         ________
tax $                ________
delivered $          ________
paid                 ________  (yes / no)
```
