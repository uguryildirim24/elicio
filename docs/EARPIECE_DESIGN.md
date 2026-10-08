# Earpiece design status

Elicio is Rolf's unfinished behind-the-ear EMG earpiece. The board has not been ordered. No assembled hardware, real recording, on-body result or validated charging interface exists.

## Current candidate

| Part | Files | Evidence and limits |
| --- | --- | --- |
| Two-layer flex board | `hardware/board/elicio-v4.kicad_sch`, `.kicad_pcb`, `.kicad_pro`, `.kicad_dru` | Routed design snapshot. Manufacturing, electrical and supply checks remain open. |
| Shell | `docs/fab/cad/v4-snap/` | STEP, STL, 3MF, preview and nominal geometry checks. No printed fit or retention test. |
| Base shell | `docs/fab/cad/v4/` | Reference geometry with a hinge only. It does not retain the lid. |
| Firmware | `firmware/elicio_stream/elicio_stream.ino`, `firmware/src/` | ADS1292 acquisition, binary BLE framing and undervoltage logic. Product Arduino pin variant is missing. |
| Receiver | `src/elicio/receiver_v2.py` | Synthetic frame decoding, loss handling and session output. No live radio validation. |
| Action gate | `src/elicio/harness/` | Synthetic event and replay demonstrations with a real local file action. No AI adapter. |

The proposed board uses an ISP1807-LR radio module, ADS1292 front end, BQ25100 charger and a fitted protected cell. The selected shell has a nominal 18 mm body width and 8.1 mm body thickness. These are CAD dimensions, not measurements of a worn device. See [board design](fab/board-v4-design.md) and [snap-shell status](fab/shell-v4.md).

## Engineering constraints

Rolf selected discreet auricular muscle input rather than an overt forearm gesture as the intended product interface. Forearm data remains a research and bench-development path, not a validation of the earpiece.

The contact hardware is specified as titanium. Material, finish, pressure, insulation and retention still need review. Shell parameters are reference examples, not personal anatomy measurements. Keep any later measurements under ignored `measurements/`.

Charging is intended to happen off-ear only. The proposed fixed TS resistor disables cell-temperature sensing. Firmware inhibits are not galvanic isolation. Series resistors alone do not establish safe fault currents or medical compliance. Do not connect unvalidated electronics to a body. Bench electrical checks and qualified safety review must precede on-body work.

## What is not implemented

- A product-specific Arduino variant and verified bootloader/programming path.
- Validated battery pack, polarity, charge cable, temperature conditions and transient protection.
- Physical shell fit, repeated snap operation, contact stability and RF range.
- A trained auricular decoder or a measured independent confirmation channel.
- Ear-canal pressure sensing or EEG acquisition. These were exploratory ideas, not built subsystems.
- Real AI execution. Only the local marker adapter changes a file.

## Next steps

1. Review the actual routed board, component supply, charging protection and fabrication constraints. Re-run KiCad release validation after any change. Resolve the blockers in [open questions](fab/open-questions.md).
2. Implement the ISP1807 product firmware variant. Verify GPIO mapping, first-load voltage levels, acquisition timing and the hardware interlock on the bench.
3. Evaluate a passive shell print. Check fit, latch access, repeated retention and contact positions before including powered electronics.
4. After electrical and physical review, preserve a real raw recording in ignored `recordings/`. Show one contraction producing one harmless marker action with linked audit records.

Historical v1/v2 geometry and packing tables remain because the current generator and existing checks depend on them. They are references, not alternative checkout instructions. Superseded order sheets have been removed. Rejected M1.6 closure code and exports remain as diagnostic evidence, not a fabrication candidate.
