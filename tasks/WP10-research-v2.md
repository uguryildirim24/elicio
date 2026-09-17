# WP10 — Research for plan v2 (lane w5, web only)

Read `tasks/phase1-common.md` first. Lane `w5`, worktree
`/home/user/projects/elicio/.worktrees/w5`, branch `lane/w5`.
Start line (coordinator restarts you by copy-paste):

    herdr agent start w5 --kind agy --pane <pane> --parent w1B:p1 -- --dangerously-skip-permissions --add-dir /home/user/projects/elicio --effort high --model gemini-3.8-flash-high

Why: Rolf's answers of 2026-09-17 (`docs/fab/open-questions.md` Q28 to
Q34) change the plan: every physical thing is ordered once, the body is
thin, the shell must look good, and a custom assembled board replaces the
breadboard bench. Plan v2 needs facts before it is drafted. You search the
web and report. You design nothing, contact nobody, buy nothing, request no
quote, sign up nowhere, upload nothing, and never put anything in a cart.

Owns: `docs/fab/L5-research-v2.md` (new). Nothing else but your report.

Deliver `docs/fab/L5-research-v2.md` with the six sections below. Every
number carries the page URL, the date you read it, and a verbatim quote of
the sentence it came from, or the tag UNVERIFIED with the search you tried.
A dead, login-walled or paywalled page is named as such. Never paraphrase a
number into a quote; earlier rounds retagged half a lane's citations for
that.

1. **Thin cells.** LiPo cells 3.2 mm thick or less (target 3.0 or less)
   with a protection circuit, width 12 or less, length 20 or less, capacity
   20 mAh or more, buyable in ones from a stocked seller (DigiKey, Mouser,
   Adafruit, Pimoroni, PowerStream, LiPol Battery, DNK Power, Amazon;
   AliExpress last). For each: model code, nominal dimensions and
   tolerances from the datasheet, thickness with the protection circuit as
   the sheet states it, capacity, lead type and length, price for one,
   page. Mark which ones have a real drawing.
2. **Finishes for a skin-worn part at JLC3DP.** MJF PA12 grey and dyed
   black, any smoothing or vapour-polish option, SLS nylon, and any resin
   JLC lists as skin-safe or biocompatible with the certificate's name. For
   each: the process page, a price for a 40 × 20 × 8 mm part only if a page
   or table states one (do not upload a file), lead time, and what the page
   says about skin contact or certification. Then one alternative vendor
   with polished or dyed nylon and a skin statement (Xometry, Craftcloud,
   Sculpteo, or another), prices only from pages.
3. **The board, assembled once.** JLCPCB PCBA: economic versus standard
   assembly, minimum quantity, setup and stencil fees, per-joint fees, a
   4-layer 20 × 16 mm board price for 5 pieces if a page states it,
   shipping options. Availability in the JLCPCB/LCSC library with LCSC part
   numbers, stock and unit price: TI ADS1292R, TI ADS1292, BQ25100,
   TLV713 3.3 V, Raytac MDBT50Q-1MV2, Seeed XIAO nRF52840 module, Ebyte
   E73-2G4M08S1C, Fanstel BT840, INA128. Say for each whether JLC lists it
   as basic, extended, or global sourcing/consigned, and what that costs.
4. **The XIAO route.** Seeed XIAO nRF52840: board dimensions including the
   USB-C height, weight, built-in charger and its charge current, battery
   pads, price, stock at DigiKey, Mouser and Seeed; whether the schematic
   and Zephyr or Arduino support are public. Purpose: a carrier board that
   holds only the analog front end is lower first-spin risk than a
   bare-module board; plan v2 decides.
5. **Contact hardware in ones.** Brass DIN 439 M2.5 thin nuts (Bossard
   BN 147 or any brass DIN 439 M2.5), titanium ISO 7380 M2.5 × 4 (repeat the
   SKU from `docs/fab/contacts.md` §8 only if its page still lives), TE
   31428 ring lug; each with a live page, a price, and the minimum
   quantity.
6. **Fit without a printed gauge.** Any published 1:1 paper or card sizing
   template for behind-the-ear devices (hearing-aid BTE size gauges,
   ear-hook templates, sports-earphone fit cards), with pages. Two
   sentences on whether a paper profile cut from our `docs/fab/cad/v1/drawing.pdf`
   is a reasonable stand-in, and what it cannot check.

Rules: read-only web; no login; no calculator that needs an upload; no
cart; no email. Plain sentences and tables, under 2,500 words. Commit as
`docs(fab): L5 research for plan v2` on `lane/w5`. Do not push; the hook
does. Report `.reports/WP10-report.md` (keep it untracked): what you found,
what you could not, every UNVERIFIED. Closing steps per the common file
with `<PKG>` = `WP10`, `<lane>` = `w5`.
