Every fitted v4 board part has a supply route, but you cannot order a fully JLC-stocked board yet: JLC has stock for 60 of 63 positions; the radio module (U1), exact 4.2 V charger (U3) and battery connector (J2) still must be sent to the board maker. TI publicly marks U3 in stock, but the other two external stock counts and the maker's consignment acceptance are unverified.

## Implementation
- Merged t-0056 with `--no-edit` (merge conflict in the design note reconciled with Rolf's off-ear charging decision); merge commit `703e0e8`.
- Chose stock-backed 0201 resistors R11/R18/R19, 0201 C2, exact SOD882 TVS D1, reel variant U4, exact U5, 0402 green LED D2, and Murata tape-suffix 0402 capacitors C3/C14/C18/C19. Changed only LCSC/MPN fields in `hardware/board/v4_parts.py`, `elicio-v4.kicad_pcb` and `elicio-v4.kicad_sch`. No geometry, net, footprint or placement edits. Release BOM confirms the same fields.
- TI SLUSBV8C §5 says the stocked BQ25100A is a 4.30 V charger, unsafe as a drop-in for this 4.2 V cell; JLC's B listing shows 4.284 V and only six in stock, and B is absent from that TI variant table. U3 remains exact YFPR, consigned from TI's public `InStock` product offer; quantity not shown. See `docs/fab/bom-v4-orderable.md` for every query/code, price, stock, snapshot date, electrical checks and the approximate $9.64 JLC-component-only cost per board.
- Three open external routes: U1 ISP1807-LR-RS (JLC 0), U3 BQ25100YFPR (JLC 0), J2 Molex 202656-0021 (no JLC result). Need to confirm actual distributor stock, terminated battery plug, and consignment fees/acceptance before spending.

## Verification
- `python3 scripts/board/release.py --board elicio-v4 --routed`: exit 0; ERC 0 errors / 0 warnings; DRC 0 errors / 28 warnings / 0 unconnected; 63 BOM and 63 CPL rows; 17 Gerber/drill/job outputs. Generated release files were not committed.
- `.venv/bin/python -m unittest discover -s tests -v`: **OK**, 287 tests, 61 skipped, Python 3.13 (3.11 executable unavailable locally). Base dependencies installed in local ignored `.venv`.
- Public pages only; no vendor contact, purchase, upload or cart. No pcbnew mutation scripts. KiCad files differ only in LCSC and MPN property strings.

Remaining hardware caveat: passing DRC and DC-bias-capacitance arithmetic are not a contact-level ESD test; D1 is physically distant from U3 IN, and the OUT bypasses are distant. No order or fabrication approval follows from this release alone.
