# L-r2 — datasheet facts for the round 2 review (agy lane `r2ds`)

Parent: herdr agent `rev2` (the round 2 reviewer). Read-only lane. You
edit nothing in the repository and commit nothing. You write one answer
file and push DONE.

Worktree to read from: `/home/user/projects/elicio/.worktrees/review`
(branch `review/r2`). Context: `docs/fab/interface.md` §5, §6.3, §6.4,
§8 cite these datasheets. Rules: web only to read the named datasheet or
product page; no vendor contact, sign-up, cart, quote or purchase. Every
answer quotes the exact line or table cell, with URL, page number, and
the document's revision date, plus the date you read it.

## Questions

1. **TI ADS1292 (not ADS1292R), VQFN-32 package `RSM`.**
   https://www.ti.com/lit/ds/symlink/ads1292.pdf. (a) Does the ADS1292
   (non-R) ship in RSM? Quote the Package/Ordering or Device Information
   row and the orderable part number. (b) RSM body size nominal and
   maximum (X, Y, height) from the mechanical drawing, with the drawing
   number. (c) TQFP-32 `PBS` body and lead span maximum, drawing number.
2. **Nexperia BAV199S-Q.**
   https://assets.nexperia.com/documents/data-sheet/BAV199S-Q.pdf. (a) How
   many diodes and how many independent diode pairs are in one package?
   Quote the pinning table (pin number → function) and the internal
   circuit description. (b) Can one package clamp three separate signal
   lines each with its own series pair (three independent pairs, no pin
   shared between lines)? Answer yes or no from the pinning. (c) Package
   name and the reflow "occupied area" or footprint figure dimensions.
   (d) Same pinning question for plain BAV199 (SOT23):
   https://assets.nexperia.com/documents/data-sheet/BAV199.pdf.
3. **DNK 501015 cell.**
   https://www.fpbattery.com/wp-content/uploads/2024/06/fpbattery-501015-3.7V-50mAh-Lithium-Polymer-Battery-Specification.pdf.
   Quote the dimension table: T, W, L, BL (with tolerances), tab spacing,
   and where the PCM sits. Page number.
4. **Raytac MDBT50Q-1MV2, Spec K.**
   https://cdn.sparkfun.com/assets/4/7/4/3/8/_nRF52840__MDBT50Q-1MV2___MDBT50Q-P1MV2_Ver.K_spec.pdf.
   (a) Module L × W × H nominal and tolerance, page. (b) The antenna
   keep-out / no-ground zone dimensions and where they sit relative to
   the module, pages. (c) Any stated distance to keep metal, batteries or
   components away from the antenna (quote it, or say none is stated).

## Output

Write `/home/user/projects/elicio/.worktrees/review/.reports/r2-datasheets.md`
(the `.reports/` folder is git-ignored) with one section per question,
quotes verbatim. If a page cannot be fetched, say so and give the HTTP
status. Then run:

    herdr pane report-metadata "$HERDR_PANE_ID" --source lane --token lane=r2ds --token done=1
    herdr agent prompt rev2 "DONE r2ds .reports/r2-datasheets.md" || herdr agent prompt rev2 "DONE r2ds .reports/r2-datasheets.md"
