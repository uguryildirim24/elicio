# Delivered-spend ledger v2

Skeleton for plan v2 §9 and R8. Not quotes. Review r5 filled the source
URLs the repo already cites, added the interface II flex lines (Q50) and
the Raytac sourcing line (Q54), made the cell an open line (Q55) and
renamed the per-order rows to allowances. Destination Massachusetts,
USA, assumed until Rolf confirms (D-8). No agent buys, quotes, uploads,
or contacts a vendor. Fill later order sheets into these tables. Every
number here is already in `docs/fab/plan-v2.md` §9 or §12 or in
`docs/fab/board-v2.md` §18 (the flex fixture), or is the word allowance,
or is a named blank.

Columns: item; quantity; status (`quoted` / `catalogue` / `allowance`);
unit price as displayed on the cited page or in the plan; source URL and
date; shipping; tax; import collection; delivered line total.

## Rules

No all-in total is claimed until every line is quoted or catalogue.

The shell's delivered maximum is reserved before order 1 is paid. Plan
v2 §9 allowance for order 2 is $50–90. If an adequate supported reserve
cannot be established, G8 is not passed.

Massachusetts use tax is 6.25 % where the seller does not collect it
(plan v2 §9). Amounts stay blank until a checkout shows whether tax was
collected.

Duties are a configured DDP figure or a documented reserve. CBP CSMS
69326983 is primary evidence for a 12.5 % component under 9903.05.31
for China-origin goods (plan v2 §12 C13, guidance dated 2026-07-24).
JLC's FAQ lists Section 301 at 25 % and its own advance collection
(plan v2 §9). None of that is a product-level total. A percentage for
one trade-remedy component is not the total import reserve.

Base allowances sum to $290–460, plus $50–70 for the programming kit if
needed (plan v2 §9). That sum is an allowance, not a delivered total.

Named cuts if R8 fails (plan v2 §9): grey instead of dyed, no spare
lid, two boards instead of five, no programming kit if the factory
programs.

## Order 1 — board

Contents (plan v2 §9): 2 to 5 boards, standard PCBA, sides per
placement (two-sided assumed), 4-layer ENIG, X-ray for the module,
bootloader programming if accepted. Default route JLCPCB. US quote-only
route MacroFab or Screaming Circuits. Order allowance $160–240
(allowance, plan v2 §9, 2026-09-17).

| Item | Quantity | Status | Unit price as displayed | Source URL and date | Shipping | Tax | Import collection | Delivered line total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Standard PCBA setup, one side | 1 | catalogue | $25.56 | https://jlcpcb.com/help/article/pcb-assembly-price , 2026-09-17 (page updated 2026-09-09; plan v2 turn 04 and 06) | blank | blank | blank | blank |
| Standard PCBA setup, two sides (assumed) | 1 | catalogue | $51.12 | https://jlcpcb.com/help/article/pcb-assembly-price , 2026-09-17 (page updated 2026-09-09; plan v2 turn 04 and 06) | blank | blank | blank | blank |
| Stencil, one side | 1 | catalogue | $8.21 | https://jlcpcb.com/help/article/pcb-assembly-price , 2026-09-17 (page updated 2026-09-09; plan v2 turn 04 and 06) | blank | blank | blank | blank |
| Stencil, two sides | 1 | catalogue | $16.42 | https://jlcpcb.com/help/article/pcb-assembly-price , 2026-09-17 (page updated 2026-09-09; plan v2 turn 04 and 06) | blank | blank | blank | blank |
| Feeder, standard tier (not economic $3.07) | blank (per part line) | catalogue | $1.53 per part line | https://jlcpcb.com/help/article/pcb-assembly-price , 2026-09-17 (page updated 2026-09-09; plan v2 turn 04 and 06) | blank | blank | blank | blank |
| X-ray, 1–10 inspected-part bracket | blank (per inspected part) | catalogue | $1.64 per inspected part | https://jlcpcb.com/help/article/pcb-assembly-price , 2026-09-17 (page updated 2026-09-09; plan v2 turn 04 and 06) | blank | blank | blank | blank |
| Two-fixture, rigid PCB, where applicable | blank | catalogue | $16.42 | https://jlcpcb.com/help/article/pcb-assembly-price , 2026-09-17 (page updated 2026-09-09; plan v2 turn 04 and 06) | blank | blank | blank | blank |
| Assembled boards, 4-layer 1.0 mm ENIG (plan v2 §9 wording; superseded by Q50) | 2 to 5 | allowance | blank (inside $160–240 order allowance) | plan v2 §9, 2026-09-17 | blank | blank | blank | blank |
| Assembled boards, 2-layer polyimide flex with FR4 stiffeners (interface II, Q50) | 2 to 5 | allowance | blank; the $160–240 allowance was set for the rigid board and is not re-derived for flex | `docs/fab/board-v2.md` §12, §18 | blank | blank | blank | blank |
| Flex assembly fixture | 2 (1–29 pcs) | catalogue | $24.63 per fixture, $49.25 for two | https://jlcpcb.com/help/article/pcb-assembly-price , 2026-09-17 (page updated 2026-09-09; `board-v2.md` §18) | blank | blank | blank | blank |
| FPC extra-stiffener fee (4 or more stiffeners; this drawing has 6) | blank | quoted | blank; the page names the fee, not an amount for this board | https://jlcpcb.com/help/article/fpc-extra-charges , 2026-09-17 (updated 2026-08-18; `board-v2.md` §18) | blank | blank | blank | blank |
| Raytac MDBT50Q-1MV2, JLC global sourcing or consignment (Q54) | 1 per board | allowance | blank; consignment adds Rolf's purchase at DigiKey or Mouser, one parcel to JLC and JLC's consignment fee | `docs/EARPIECE_DESIGN.md` Q54 | blank | blank | blank | blank |
| Module X-ray and handling | blank | allowance | blank | plan v2 §9; C5 and G3c open | blank | blank | blank | blank |
| Factory bootloader programming | blank | quoted | blank | plan v2 §12 C6, quote-only, Rolf-authorized | blank | blank | blank | blank |
| US quote-only assembly (MacroFab or Screaming Circuits) | blank | quoted | blank | plan v2 §9; no quote requested | blank | blank | blank | blank |
| Board shipment | 1 | allowance | blank | plan v2 §9 | blank | blank | blank | blank |
| Massachusetts use tax 6.25 % if not collected | blank | allowance | blank | plan v2 §9 | — | 6.25 % where not collected | — | blank |
| Import collection, China-origin PCBA | blank | allowance | blank | plan v2 §12 C13; not a product-level total | — | — | DDP or documented reserve | blank |
| Order 1 allowance (not a delivered total) | — | allowance | $160–240 | plan v2 §9, 2026-09-17 | blank | blank | blank | blank |

## Order 2 — shell

Contents (plan v2 §9): body, lid, spare lid, stand if printed; MJF
PA12; finish per R3. Default route JLC3DP. US quote-only route Xometry.
Allowance $50–90, reserved as a maximum before order 1 is paid.

| Item | Quantity | Status | Unit price as displayed | Source URL and date | Shipping | Tax | Import collection | Delivered line total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MJF PA12 starting price | blank | catalogue | from $1.00, 72 h (starting price only) | https://jlc3dp.com/help/article/pa12-hp-nylon , 2026-09-17 (plan v2 §9, §12) | blank | blank | blank | blank |
| Body | 1 | allowance | blank (inside $50–90 reserved maximum) | plan v2 §9 | blank | blank | blank | blank |
| Lid | 1 | allowance | blank | plan v2 §9 | blank | blank | blank | blank |
| Spare lid | 1 | allowance | blank | plan v2 §9; named cut if R8 fails | blank | blank | blank | blank |
| Stand if printed | blank | allowance | blank | plan v2 §9 | blank | blank | blank | blank |
| Finish per R3 (grey default; dyed black is Q30) | blank | allowance | blank | plan v2 §7, §9; C1 open | blank | blank | blank | blank |
| US quote-only print (Xometry) | blank | quoted | blank | plan v2 §9; no quote requested | blank | blank | blank | blank |
| Shell shipment | 1 | allowance | blank | plan v2 §9 | blank | blank | blank | blank |
| Massachusetts use tax 6.25 % if not collected | blank | allowance | blank | plan v2 §9 | — | 6.25 % where not collected | — | blank |
| Import collection, China-origin prints | blank | allowance | blank | plan v2 §12 C13; not a product-level total | — | — | DDP or documented reserve | blank |
| Order 2 reserved maximum (allowance, reserved before order 1 is paid) | — | allowance | $50–90 | plan v2 §9, 2026-09-17 | blank | blank | blank | blank |

## Order 3 — small parts

Contents (plan v2 §9): titanium screws, M2.5 standoffs, cell, 1.5 mm hex
key, USB-C cable, pre-cut foam pads, three silicone port plugs, three
snap-electrode leads with pin sockets, gel electrodes, a nickel test
kit or Rolf's written waiver. Selected suppliers, potentially domestic
and international, with each purchased pack and parcel costed
separately. The $80–130 allowance is not a verified total for the
100-pack route. Screws and cell are page-priced; the rest are
allowances.

| Item | Quantity | Status | Unit price as displayed | Source URL and date | Shipping | Tax | Import collection | Delivered line total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Titanium ISO 7380 M2.5 screws (Sortafast SF-BH2504-10) | 10 | catalogue | $17.50 per 10-pack | https://sortafast.com/products/sortafast-titanium-screws-button-head-10pk-m2-5 , 2026-09-17 (`contacts.md`, `L6-research-v3.md`) | blank | blank | blank | blank |
| Standoff 3.0 mm Spacer Express LAI-FF-M2.5-SW5-L3-100 | 100-pack as sold | catalogue | €91.08 ex VAT per 100; delivery 5–10 working days; shipping to Massachusetts unverified | https://spacer-express.com/female-female/875-hexagonal-female-female-threaded-spacer-nickel-plated-brass-m2-5-5-mm-across-flats.html , 2026-09-17 (plan v2 §12 C14) | unverified | blank | blank | blank |
| Standoff 4.0 mm Harwin R25-1000402 | blank (needed count); DigiKey showed qty-1 | catalogue | $0.57 at 1; "In-Stock: 3,847" on that date; 5.50 mm hex field conflicts with Harwin 5.00 A/F max, drawing governs | https://www.digikey.com/en/products/detail/harwin-inc/R25-1000402/3728140 , 2026-09-17; drawing https://content.harwin.com/asset/6e059b82-0a88-4a5e-8a59-36c0928fbfd1/DRG-01991-Technical-Drawing-Datasheet-R25-100-pdf.pdf , 2026-09-17 (plan v2 §12 C14) | blank | blank | blank | blank |
| Standoff 3.5 mm | blank | allowance | blank | plan v2 §12 C14: exact 3.5 mm match unverified | blank | blank | blank | blank |
| Cell — open (Q55, gate G1) | 1 | allowance | blank | Q55: the closing layouts use a 501015-class cell with no verified page price in ones; the page-priced DTP301120 below closes in no layout | blank | blank | blank | blank |
| Cell Data Power DTP301120 (SparkFun PRT-25270), only if WP11b closes a longer body | 1 | catalogue | $7.39 | https://www.sparkfun.com/products/25270 , 2026-09-17 (`L5-research-v2.md` §1) | blank | blank | blank | blank |
| 1.5 mm hex key | blank | allowance | blank | plan v2 §9 | blank | blank | blank | blank |
| USB-C cable | blank | allowance | blank | plan v2 §9 | blank | blank | blank | blank |
| Pre-cut foam pads | blank | allowance | blank | plan v2 §9 | blank | blank | blank | blank |
| Silicone port plugs | 3 | allowance | blank | plan v2 §9; three spares in order 3 | blank | blank | blank | blank |
| Snap-electrode leads with 2.54 mm pin sockets | 3 | allowance | blank | plan v2 §9, §5.6 | blank | blank | blank | blank |
| Gel electrodes | blank | allowance | blank | plan v2 §9 | blank | blank | blank | blank |
| Nickel test kit, or Rolf's written waiver | blank | allowance | blank | plan v2 §9 | blank | blank | blank | blank |
| Small-parts shipments (each pack and parcel separate) | blank | allowance | blank | plan v2 §9 | blank | blank | blank | blank |
| Massachusetts use tax 6.25 % if not collected | blank | allowance | blank | plan v2 §9 | — | 6.25 % where not collected | — | blank |
| Order 3 allowance (not a delivered total) | — | allowance | $80–130 | plan v2 §9, 2026-09-17; not a verified total for the 100-pack route | blank | blank | blank | blank |

## Conditional — first-load kit

In when G4 falls to Rolf (plan v2 §8, §9, Q48). US sellers. Listed
prices, not a complete kit price. Allowance $50–70.

| Item | Quantity | Status | Unit price as displayed | Source URL and date | Shipping | Tax | Import collection | Delivered line total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Tag-Connect TC2030-IDC-NL | 1 | catalogue | $33.95 listed | https://www.tag-connect.com/product/tc2030-idc-nl , 2026-09-17 (plan v2 turn 04 and 06) | blank | blank | blank | blank |
| Raspberry Pi Debug Probe | 1 | catalogue | $12.00 listed | plan v2 §8 and §9, 2026-09-17; seller URL not in the repo (docs: https://www.raspberrypi.com/documentation/microcontrollers/debug-probe.html ) | blank | blank | blank | blank |
| Jumpers | blank | allowance | blank | plan v2 §9 | blank | blank | blank | blank |
| Kit shipment | 1 | allowance | blank | plan v2 §9 | blank | blank | blank | blank |
| Massachusetts use tax 6.25 % if not collected | blank | allowance | blank | plan v2 §9 | — | 6.25 % where not collected | — | blank |
| Conditional kit allowance (not a delivered total) | — | allowance | $50–70 | plan v2 §9, 2026-09-17 | blank | blank | blank | blank |

A multimeter is in when needed (plan v2 §9, R2b, assembly step 6).
Price blank.

## Whole-project gate (R8, G8)

| Item | Quantity | Status | Unit price as displayed | Source URL and date | Shipping | Tax | Import collection | Delivered line total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Ceiling | — | allowance | blank | Q33; Rolf writes the ceiling here. Blank until he does. | — | — | — | blank |
| Three orders plus kit if needed | — | allowance | $290–460 plus $50–70 if the kit is needed | plan v2 §9, 2026-09-17 | blank | blank | blank | blank |
| All-in delivered total | — | — | not claimed | plan v2 §9: no all-in figure until this ledger reproduces one from quoted or catalogue lines | blank | blank | blank | blank |
