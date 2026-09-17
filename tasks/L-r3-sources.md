# L-r3 — source spot-checks for the round 3 review (agy lane `r3src`)

Parent: herdr agent `rev3` (the round 3 reviewer). Read-only lane. You
edit nothing in the repository and commit nothing. You write one answer
file and push DONE.

Worktree to read from: `/Users/rolfie/projects/elicio/.worktrees/review`
(branch `review/r3`). Context: `docs/fab/contacts.md` §8 (written by lane
w5 on 2026-09-17) cites the pages below. Rules: web only to open the named
URL (or, if it 404s, the same vendor's page for the same SKU); no vendor
contact, sign-up, cart, quote or purchase. Every answer quotes the exact
line, table cell or drawing callout, with the URL you actually loaded, the
HTTP status or "loaded", the document revision/date if shown, and the date
you read it. If a number is not on the page, write NOT ON PAGE. Do not
copy numbers from contacts.md; I am checking them.

## Questions

1. **TE 31428 customer drawing C-31428 rev D4.**
   https://www.te.com/commerce/DocumentDelivery/DDEController?Action=showdoc&DocId=Customer+Drawing%7F31428%7FD4%7Fpdf%7FEnglish%7FENG_CD_31428_D4.pdf%7F31428
   Quote: revision letter; stock thickness; stud hole; ring (tongue)
   width/OD; every length dimension with what it runs between (hole centre
   to barrel end? tongue edge to barrel end? overall length) and its
   tolerance or max; barrel outside diameter or width AND barrel height if
   given; wire range in AWG and mm²; material and plating (any nickel
   underplate?). Also the TE product page for 31428 (te.com or DigiKey
   https://www.digikey.com/en/products/detail/te-connectivity-amp-connectors/31428/292150):
   wire size range, and whether 28 AWG is inside it.
2. **Panduit P22-4R-C drawing 102215.**
   https://www.panduit.com/content/dam/panduit/en/products/media/5/15/215/2215/102215.pdf
   Stock thickness, hole centre to barrel end, overall length, barrel OD,
   wire range.
3. **Nichifu R0.3-3** in
   https://www.nichifu.co.jp/en/pdf/catalog/NICHIFU_TERMINALS_CATALOG_2023.pdf
   (or Nichifu's current R-type page): thickness, hole, width, length
   figures and what they run between, wire range, page.
4. **TME Bossard BN 146 M2.5, order no. 1090798.**
   https://www.tme.eu/en/details/b2.5_bn146/hex-nuts/bossard/1090798/
   Material and surface/coating text verbatim (zinc? trivalent/Cr(III)?
   passivation colour? any nickel, zinc-nickel?), standard (DIN 439 /
   ISO 4035), height m if given, across flats, price and currency as
   shown, pack/multiple and minimum order quantity. Bossard's own BN 146
   page if linked: m for M2.5.
5. **TME Bossard BN 147 M2.5, order no. 1159550.**
   https://www.tme.eu/en/details/b2.5_bn147/hex-nuts/bossard/1159550/
   Same fields as 4.
6. **Fastenright titanium DIN 439 M2.5** (`M2.5-DIN439-TI`,
   https://www.fastenright.com): does a product page for a titanium DIN 439
   M2.5 thin nut exist? URL, price or "quote", material and certificate
   text.
7. **Titanium Webshop DIN 934 Grade 2 M2.5, SKU 663701003.**
   https://www.titanium-webshop.eu/en/titanium-nuts/titanium-hex-nut-din-934-grade-2-m2-5.html
   Price, currency, per piece or pack, SKU, m, s, material, certificate.
8. **Westfield Fasteners M2.5 ISO 7380-1 drawing.**
   https://www.westfieldfasteners.co.uk/Images/Drawings/M2.5-ISO-7380-1-Button-Head-Socket-Screws.png
   (or Westfield's M2.5 ISO 7380 product page): dk, k, s with min/max.
9. **Accu ISO 7380-1 M2.5.** https://accu.co.uk/iso-7380-1-button-head-screws
   (or an Accu M2.5 ISO 7380 product page): dk, k, socket, min/max.
10. **Sortafast SF-BH2504-10.**
    https://sortafast.com/products/sortafast-titanium-screws-button-head-10pk-m2-5
    Price, pack size, length options (is 4 mm offered), grade, any dk/k.
11. **RJXHOBBY RJX3995 M2.5.**
    https://www.rjxhobby.com/Accessories/screw-washer-ball-linkage/screw/titanium-screws/rjx-50pcs-m2-5-4-20mm-ta2-button-head-titanium-screws
    Price, pack size, is 4 mm a selectable length, material, dk/k text.
12. **Titane Services** https://www.titane-services.eu/vis-titane-ISO7380-G5-M2.5
    Price per piece, lengths offered (is 4 mm offered?), grade.

## Output

Write `/Users/rolfie/projects/elicio/.worktrees/review/.reports/r3-sources.md`
(the `.reports/` folder is git-ignored) with one section per question,
quotes verbatim. Then run:

    herdr pane report-metadata "$HERDR_PANE_ID" --source lane --token lane=r3src --token done=1
    herdr agent prompt rev3 "DONE r3src .reports/r3-sources.md" || herdr agent prompt rev3 "DONE r3src .reports/r3-sources.md"
