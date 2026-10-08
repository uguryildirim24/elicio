# Retained engineering source pointers

These pointers index key sources from the retained historical L1 to L8 technical surveys. The surveys preserve their literature tables, supplier evidence and design assumptions. Private task and review dialogue is omitted. Neither the index nor the surveys establish current stock, pricing, supplier acceptance or independently checked safety results. Recheck maker documents and fabrication terms before any order. The board remains unfinished, unordered and unmeasured.

## Front end, radio and power

- TI ADS1292 datasheet, SBAS502C: https://www.ti.com/lit/ds/symlink/ads1292.pdf
- TI BQ25100 family datasheet, SLUSBV8C: https://www.ti.com/lit/ds/symlink/bq25100.pdf
- Insight SiP ISP1807 module datasheet: https://www.insightsip.com/fichiers_insightsip/pdf/ble/ISP1807/isp_ble_DS1807.pdf
- TI TLV713 datasheet: https://www.ti.com/lit/ds/symlink/tlv713p.pdf
- TI TPS7A02 datasheet: https://www.ti.com/lit/ds/symlink/tps7a02.pdf
- Nexperia PESD5V0L1UL datasheet: https://assets.nexperia.com/documents/data-sheet/PESD5V0L1UL.pdf

The current circuit, courtyard tables and unresolved reference checks are in `board-v4-design.md` and `board-v4-refcheck.md`. The latter is a historical schematic review, not validation of the latest copper.

## Battery envelope assumptions retained by packing studies

The `placement_v2.py` reference matrix contains several rejected cell envelopes. Listing dimensions do not qualify a cell, a PCM, a factory-fitted connector or charge limits.

- SparkFun PRT-25270 reference: https://www.sparkfun.com/products/25270
- DTP301120 reference drawing: https://cdn.sparkfun.com/datasheets/Prototyping/SPE-00-301120-40mah-en-1.0ver.pdf
- Jauch LP501218JH+PCM reference: https://www.digikey.com/en/products/detail/jauch-quartz/LP501218JH-PCM-2-WIRE-50MM/15233155
- DNK501015 pack reference: https://www.dnkpower.com/product/dnk501015-3-7v-50mah-lipo-battery-pack/
- Benzo pack supplier reference: https://benzoenergy.com

Historical packing tables distinguish bare cells from protected packs. The fitted protected pack for the current board is still unverified. Do not use a generic listing as a substitute.

## Historical contact envelope

The v1 generator and placement checks retain a TE 31428 lug envelope. It is not the current flex-tab contact assembly. The drawing pointer recorded in the earlier contact study was TE Customer Drawing C-31428 revision D4:

https://www.te.com/commerce/DocumentDelivery/DDEController?Action=showdoc&DocId=Customer+Drawing%7F31428%7FD4%7Fpdf%7FEnglish%7FENG_CD_31428_D4.pdf%7F31428

This pointer preserves provenance only. Dimensions, finish, wire range and supplier identity need fresh review before any new use. See `contacts.md` for current limits.

## Fabrication constraints

- Flex capabilities: https://jlcpcb.com/capabilities/flex-pcb-capabilities
- Assembly capabilities: https://jlcpcb.com/capabilities/pcb-assembly-capabilities
- Flex panel design: https://jlcpcb.com/blog/design-guidelines-flex-pcb-panels
- Stiffener design: https://jlcpcb.com/help/article/fpc-stiffener-design-guide
- PA12 print-process reference: https://jlc3dp.com/help/article/pa12-hp-nylon

Process rails, finished outlines, stiffeners, bend regions and two-sided assembly are separate constraints. No accepted manufacturing order or printed material result exists.
