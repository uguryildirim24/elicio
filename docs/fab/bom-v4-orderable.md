# V4 BOM — supply snapshot, 2026-09-25 UTC

**All 63 fitted BOM positions now have a supply route: 60 use stocked JLC codes, and U1, U3 and J2 need customer-supplied consignment.** This is not a purchase approval. Public stock can change; prices below are USD per component at JLC's first price tier, not assembled-board prices. No cart, quote, upload, purchase or vendor contact was made. Each JLC row below comes from the public [JLC component search](https://jlcpcb.com/parts) POST endpoint `shoppingCart/smtGood/selectSmtComponentList` with `keyword` equal to the listed code, `currentPage=1`, `pageSize=25`, `searchSource=search`, read **2026-09-25 UTC**. Follow the linked code to the public part listing. Stock is units available at that time, not reserved units; check again before production. All are Extended except C15525 (Basic).

| Reference(s) | JLC code / query | MPN (search result) | Stock | USD each | Supply |
|---|---|---|---:|---:|---|
| U1 | — | ISP1807-LR-RS | 0 (JLC C5264268) | — | CONSIGNED: no JLC stock; [Mouser product](https://www.mouser.com/ProductDetail/Insight-SiP/ISP1807-LR-RS); external live stock/price unverified |
| U2 | [C89288](https://jlcpcb.com/partdetail/C89288) | ADS1292IRSMT | 97 | 6.4422 | JLC |
| U3 | — | BQ25100YFPR | 0 (JLC C527572) | — | CONSIGNED: exact 4.20 V charger; [TI Store product](https://www.ti.com/product/BQ25100/part-details/BQ25100YFPR) public JSON-LD says `InStock`, $0.744, but no public count; obtain enough for assembly before ordering |
| U4 | [C2863576](https://jlcpcb.com/partdetail/C2863576) | TLV71330PDQNR | 990 | 0.0959 | JLC |
| U5 | [C2867950](https://jlcpcb.com/partdetail/C2867950) | TPS7A0230PDQNR | 385 | 0.8201 | JLC |
| Q1 | [C240195](https://jlcpcb.com/partdetail/C240195) | WPM3027-3/TR | 9,846 | 0.0400 | JLC |
| Q2, Q3, Q4 | [C478155](https://jlcpcb.com/partdetail/C478155) | PMZ290UNE2YL | 2,712 | 0.0553 | JLC |
| D1 | [C3001948](https://jlcpcb.com/partdetail/C3001948) | PESD5V0L1UL | 7,525 | 0.0281 | JLC |
| D2 | [C364549](https://jlcpcb.com/partdetail/C364549) | LTST-C281TGKT-5A | 7,490 | 0.0761 | JLC |
| J2 | — | Molex 202656-0021 | no JLC result | — | CONSIGNED: no JLC listing; source exact [Molex product](https://www.molex.com/en-us/products/part-detail/2026560021), stock/price at distributor unverified; mating battery plug still needed |
| J3 | [C49257](https://jlcpcb.com/partdetail/C49257) | 2.54-1*3PPin | 225,530 | 0.0275 | JLC |
| SW1 | [C398746](https://jlcpcb.com/partdetail/C398746) | 1TS015A-1200-0600-CT | 233 | 0.0835 | JLC |
| R1–R3, R31–R33 | [C881401](https://jlcpcb.com/partdetail/C881401) | CR0402F220KQ10Z | 9,884 | 0.0012 | JLC |
| R4, R17, R20, R21 | [C473482](https://jlcpcb.com/partdetail/C473482) | 0201WMF1004TEE | 357,802 | 0.0015 | JLC |
| R5–R8, R13, R25, R27, R28, R34, R35 | [C473048](https://jlcpcb.com/partdetail/C473048) | 0201WMF1002TEE | 10,079,955 | 0.0014 | JLC |
| R11 | [C423451](https://jlcpcb.com/partdetail/C423451) | 0201WMF6801TEE | 3,602 | 0.0016 | JLC |
| R12 | [C270341](https://jlcpcb.com/partdetail/C270341) | 0201WMF6041TEE | 149,721 | 0.0014 | JLC |
| R14–R16, R23, R24 | [C270364](https://jlcpcb.com/partdetail/C270364) | 0201WMF1003TEE | 518,206 | 0.0015 | JLC |
| R18 | [C270345](https://jlcpcb.com/partdetail/C270345) | 0201WMF4702TEE | 163,838 | 0.0015 | JLC |
| R19 | [C270351](https://jlcpcb.com/partdetail/C270351) | 0201WMF2702TEE | 63,170 | 0.0013 | JLC |
| R22 | [C270365](https://jlcpcb.com/partdetail/C270365) | 0201WMF1001TEE | 1,858,760 | 0.0013 | JLC |
| C1 | [C285104](https://jlcpcb.com/partdetail/C285104) | 0201B152K500NT | 26,563 | 0.0014 | JLC |
| C2 | [C5142551](https://jlcpcb.com/partdetail/C5142551) | TCC0201X7R103K500ZT | 2,003,754 | 0.0012 | JLC |
| C3, C14, C18, C19 | [C36626211](https://jlcpcb.com/partdetail/C36626211) | GRM155R61A106ME18D | 137 | 0.4216 | JLC |
| C4, C5, C10, C11, C13, C16 | [C5142566](https://jlcpcb.com/partdetail/C5142566) | TCC0201X5R105K6R3ZT | 347,988 | 0.0052 | JLC |
| C6, C8, C9 | [C15525](https://jlcpcb.com/partdetail/C15525) | CL05A106MQ5NUNC | 8,666,050 | 0.0255 | JLC Basic |
| C7, C12, C15, C17 | [C307380](https://jlcpcb.com/partdetail/C307380) | CL03A104KO3NNNC | 995,573 | 0.0061 | JLC |

## Substitution checks

- **R11, R18, R19:** the three selected 0201 parts are 1% thick-film, 25 V / 50 mW, the same resistance and footprint as their original design values. Search queries `0201 6.8k`, `0201 47k`, `0201 27k` respectively. R18 is on the 5.5 V VBUS divider; 25 V suffices. No resistor network change.
- **C2:** query `0201 10nF 50V`: the selected part is 10 nF, ±10%, 50 V, X7R, 0201, matching the original 0201B103K500NT. The original C43380 had only 10 units in stock and a 20-piece minimum placement plus 10 loss units.
- **D1:** query `PESD5V0L1UL` returned the **same** PESD5V0L1UL in SOD-882, C3001948. Original vs selected: standoff **5 V / 5 V**, clamping **12 V / 12 V** (JLC listing), capacitance **25 pF / 25 pF**; same part/pad orientation, not a family substitution. The old C24109 was an unrelated codec.
- **U4:** query `TLV71330` returned C2863576, TLV71330PDQNR. PDQNR vs PDQNT is reel/tape ordering; both 3.0 V, 150 mA, 230 mV dropout at 150 mA, 5.5 V input and 50 µA quiescent per JLC; same X2SON-4-EP 1×1 land and pinout. U5's exact TPS7A0230PDQNR also surfaced under query `TPS7A0230PDQNR`.
- **U3:** [TI SLUSBV8C comparison table](https://www.ti.com/lit/ds/symlink/bq25100.pdf) §5: YFPR is **4.20 V**, A is **4.30 V**. With the 4.2 V cell, A is **not** a drop-in even though JLC has 85 of C2871910 at $2.2752. The B variant is not defined in that datasheet; JLC lists 4.284 V and only **6** of C2871905, below the 10-unit floor, so B is not qualified either. Charging off-ear with fixed TS does not change cell-voltage compatibility. Keep YFPR consigned. Its 30 V IN rating and the §2.1 effective IN/TS/OUT capacitor checks remain those of the exact part; these are not proof of a contact-level ESD test.
- **D2:** query `0402 525nm`: Lite-On green LTST-C281TGKT-5A is **0402**, not the old C72043 0603. At 5.0–5.5 V VBUS, 2.5–3.1 V forward range and 1 kΩ R22, current is **(VBUS − Vf)/1000 = 1.9–3.0 mA**; below its listed 20 mA rating. Pad 1 is cathode, pad 2 anode as wired. No 0402 land alteration.
- **C3/C14/C18/C19:** query `GRM155R61A106ME18` found GRM155R61A106ME18**D**. [Murata's exact base-part specification](https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM155R61A106ME18-01A.pdf) identifies **D** as 180 mm reel paper tape, not an electrical change. The [Murata SimSurfing DC-bias graph](https://ds.murata.com/simserve/characteristics?callback=nothing&ReqType=Characteristics&ReqChara=%5B%7B%22partnumber%22%3A%22GRM155R61A106ME18%22%2C%22chara_type%22%3A%22c_dcbias_capacitance%22%2C%22parameter%22%3A%7B%22tc%22%3A%2225%22%2C%22ac%22%3A%220.1%22%7D%2C%22WorkInfo%22%3A%7B%7D%7D%5D&WorkInfo=test) for this 0402 10 V X5R part yields (after ×0.8 tolerance and ×0.85 temperature allowance) **1.55 µF IN at 5 V, 1.38 µF TS at 5.5 V, 3.78 µF combined OUT at 4.2 V**; all exceed TI's 1/1/2 µF conditions. See `board-v4-design.md` §2.1 for graph values and layout caveats. Four parts × five boards = 20; JLC's 137 units exceed its 5-piece minimum + 2 loss units.

**Component cost estimate:** the 60 stocked JLC positions total **$9.6422 per board** at the displayed first price tier (**$48.211 for five**), excluding JLC setup/assembly and the three consigned lines. The exact U3 TI public offer is $0.744 per chip, and an earlier Mouser U1-RS observation was $13.65 each (2026-09-23); neither is a confirmed five-board consignment quote. J2 and assembly fees are still unknown.

The assembly site's acceptance of consigned U1/U3/J2, their fees and availability of the correctly terminated battery remain **unverified**. A passing routed release verifies board files, not vendor acceptance or physical ESD performance.
