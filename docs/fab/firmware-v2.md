# Firmware status: v4 hardware, frame-v2 transport

The board is unfinished and unordered. No product firmware has been flashed or tested with a real ADS1292 stream. A historical Feather compile was a development stand-in, not a v4 build. Its build/flash instructions have been removed.

## Sources

| Path | Purpose |
| --- | --- |
| `firmware/elicio_stream/elicio_stream.ino` | ADS1292 stream orchestration and Nordic UART Service notifications |
| `firmware/src/ads1292.c`, `.h` | ADS1292 commands, acquisition setup and power sequencing |
| `firmware/src/frame_v2.c`, `.h` | Logical messages, fragmentation and checksums |
| `firmware/src/undervoltage.c`, `.h` | Battery stop/restart state machine |
| `firmware/src/board_pins.h` | Current ISP1807 physical nRF GPIO assignments |
| `firmware/src/board_pins_v2.h` | Historical map retained as an input to existing reference checks, not a product variant |

The sketch requires SPI and Bluefruit APIs. It deliberately stops compilation unless `ELICIO_V4_PIN_VARIANT` is supplied by a real product-specific Arduino variant. Defining the macro alone is not a valid variant implementation. The variant must map the physical GPIO numbers correctly and reserve the SPIM3 pins.

## Missing product work

- Implement the ISP1807 Arduino variant and verify every GPIO against the actual board.
- Select and verify a bootloader, image, debug probe and first-load voltage sequence.
- Verify reset/NFC configuration, ADC scaling, clocks, interrupts, SPI timing and AFE power sequencing on the bench.
- Measure battery thresholds under radio load and validate acquisition stop/restart behavior.
- Verify the hardware charging interlock and transient protection. A software inhibit is not isolation or a substitute for electrical review.

The fixed TS resistor in the proposed board is not a cell thermistor. Charging is intended to occur off-ear only. No firmware behavior establishes a safe charging or on-body procedure.

## What can be checked without the board

The existing unittest suite compiles native C acquisition/framing checks when a compiler is present, exercises Python frame decoding and replays synthetic receiver faults. Run it from the root after the base install:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

This is not a product build or radio test. No manufacturing-ready build command is offered until the missing variant and image are implemented.

For synthetic reception commands, see the root README. Frame-v2 transport is documented in [frame-v2.md](frame-v2.md); acquisition checks and their limits are in [receiver-v2.md](receiver-v2.md). The current circuit and pin tables are in [board-v4-design.md](board-v4-design.md).
