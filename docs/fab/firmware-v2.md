# Firmware v2 (WP13)

Host-only this round. No board was programmed. No ADS1292 was
clocked. Nothing here is a hardware result.

Stand-in target: Adafruit Feather nRF52840 Express
(`adafruit:nrf52:feather52840`). Pin map is `firmware/src/board_pins.h`,
stated as the Feather header, not the earpiece. WP12's product PCB is
not released.

## Toolchain (Q45, Q46)

Chose Arduino-cli plus the Adafruit nRF52 core, not Zephyr.

Why: the stand-in FQBN is already in that core; BLE NUS is `BLEUart`;
the factory image is the Adafruit UF2 bootloader either way (Q45); no
Nordic account; the tree is smaller than nRF Connect SDK. Plan v2 §6
names Zephyr. That gap is in the WP13 report under "Needs a decision".

Installed on this Mac (free software, no accounts):

| Item | How | Size on disk |
|---|---|---|
| arduino-cli 1.5.1 | Homebrew formula | 25 MB |
| Adafruit nRF52 core 1.7.0 and its tools | `arduino-cli core install adafruit:nrf52` from `https://adafruit.github.io/arduino-board-index/package_adafruit_index.json` | 892 MB (`~/Library/Arduino15/packages/adafruit`); Arduino15 total 1.3 GB |
| Arm GNU Toolchain 15.3.rel1 darwin-arm64 | Homebrew cask `gcc-arm-embedded` | 1019 MB under `/Applications/ArmGNUToolchain/15.3.rel1` |
| `arm-none-eabi-gcc` 16.2.0 | Homebrew formula (tried first) | 540 MB |
| `arm-none-eabi-binutils` 2.47 | Homebrew formula | 19 MB |
| Rosetta 2 | `softwareupdate --install-rosetta --agree-to-license` | needed so Arduino's x86_64 `ctags` 5.8-arduino11 and the Adafruit gcc 9-2019q4 binary run |

gcc 16.2.0 from Homebrew has no newlib or libstdc++. It did not compile
the core. It is unused. The passing compiles used Adafruit gcc 9-2019q4
(Rosetta) and Arm GNU 15.3.1 (native arm64).

Zephyr / `west` was not installed.

## Build

From the worktree root. Adafruit gcc 9-2019q4 (the core's default;
Rosetta on this Mac):

```bash
arduino-cli compile --fqbn adafruit:nrf52:feather52840 \
  --library firmware \
  --output-dir /tmp/elicio-firmware-build \
  firmware/elicio_stream
```

Result on 2026-09-17: exit 0. Sketch uses 133276 bytes (16 %) of 815104.
Global variables use 18472 bytes (7 %) of 237568.

Same sketch with Arm GNU 15.3.1:

```bash
arduino-cli compile --fqbn adafruit:nrf52:feather52840 \
  --library firmware \
  --build-property compiler.path=/Applications/ArmGNUToolchain/15.3.rel1/arm-none-eabi/bin/ \
  --output-dir /tmp/elicio-firmware-build \
  firmware/elicio_stream
```

Result on 2026-09-17: exit 0. Sketch uses 125408 bytes (15 %) of 815104.
Global variables use 18764 bytes (7 %) of 237568. Linker warns that
newlib-nano stubs `_close`, `_fstat`, `_getpid`, `_isatty`, `_kill`,
`_lseek`, `_read` are not implemented. Those are unused syscalls.

The portable C modules (`frame_v2.c`, `undervoltage.c`, `ads1292.c`)
also compile on the host with clang through `tests/native/framer_cli.c`,
driven by `tests/test_frame_v2.py`.

## Flash (documented, not run)

Application update after the bootloader is present: copy the UF2 from
the compile output to the `FTHR840BOOT` volume. Arduino-cli can also
upload over the serial 1200-bps touch if a Feather is plugged in. Neither
was run.

First load of the merged bootloader plus SoftDevice, only when G4 uses
the kit (Q48): Raspberry Pi Debug Probe (CMSIS-DAP, 3.3 V I/O listed)
and Tag-Connect TC2030-IDC-NL. Net map is WP15 / `assemble.md`. Ground
first. Target powered from its own cell, off-body, electrodes off.

pyOCD (not installed this round):

```bash
pyocd flash -t nrf52840 \
  feather_nrf52840_express_bootloader-0.11.0_s140_6.1.1.hex
```

OpenOCD (not installed this round), using the Adafruit core's DAPLink
script:

```bash
openocd -f interface/cmsis-dap.cfg \
  -f "$HOME/Library/Arduino15/packages/adafruit/hardware/nrf52/1.7.0/scripts/openocd/daplink_nrf52.cfg" \
  -c "program feather_nrf52840_express_bootloader-0.11.0_s140_6.1.1.hex verify reset exit"
```

Compatibility of probe I/O with the actual target voltage is a G4 check.
It is never inferred from the 3.3 V nominal figure.

## Merged bootloader image (not downloaded)

Release: Adafruit nRF52 Bootloader **0.11.0**, SoftDevice **S140 6.1.1**.

URL (read 2026-09-17, no download):

https://github.com/adafruit/Adafruit_nRF52_Bootloader/releases/tag/0.11.0

Factory hex for this stand-in:

`feather_nrf52840_express_bootloader-0.11.0_s140_6.1.1.hex`

UF2 update (bootloader only, no SoftDevice):

`update-feather_nrf52840_express_bootloader-0.11.0_nosd.uf2`

Board header in that tag
(`src/boards/feather_nrf52840_express/board.h`, read 2026-09-17):

| Item | Value |
|---|---|
| UF2 volume | `FTHR840BOOT` |
| USB VID | `0x239A` |
| Bootloader UF2 PID | `0x0029` |
| Bootloader CDC-only PID | `0x002A` |
| DFU button | P1.02 (Feather D7) |
| UF2 board id | `nRF52840-Feather-revE` |

Application USB from the Adafruit core `boards.txt` (same date): VID
`0x239A`, PID `0x8029`, product string `Feather nRF52840 Express`, UF2
family `0xADA52840`. Extra PID pair `0x802A` / `0x002A` is the core's
other USB mode. Maximum application size 815104 bytes.

Flash map used by the application linker
`nrf52840_s140_v6.ld` in Adafruit nRF52 1.7.0:

| Region | Origin | End / length |
|---|---|---|
| MBR | `0x00000` | SoftDevice start |
| SoftDevice S140 6.1.1 | `0x01000` | application start |
| Application | `0x26000` | `0xED000` (815104 bytes) |
| Bootloader | `0xED000` | rest of flash, including settings pages at the top |

The product module (E73 / Raytac class) needs its own board id and a
rebuild of that hex. That image is not this round. The application
origin `0x26000` and the 815104-byte cap are what the streaming app
links against.

Recovery is the bootloader's own double-reset / hold-on-reset on the DFU
pin (Feather D7). A bad application image leaves `FTHR840BOOT` reachable
the same way. R2b lists the lid-off double-press.

## Undervoltage constants

`V_STOP_MV` 3000 and `V_START_MV` 3200 in `firmware/src/undervoltage.h`
are WP12's pack thresholds (`docs/fab/board-v2.md` §6: AVDD minimum 2.7 V
plus a 150 mV LDO dropout bound gives 2.85 V, plus sense error, a radio
transient and margin). Computed, not measured on a pack. The WP13 lane
had 2700/2800 placeholders; review r5 aligned them.

## ADS1292 register set

`firmware/src/ads1292.c`, checked against TI SBAS502C §8.6.1 (review r5):

| Register | Value | Why |
|---|---|---|
| CONFIG1 | `0x04` | continuous, DR 100 = 2000 SPS |
| CONFIG2 | `0xA0` | bit 7 set, PDB_REFBUF on, VREF_4V 0 = 2.42 V |
| LOFF | `0x10` | reset value, lead-off off when worn |
| CH1SET | `0x60` | gain 12, normal electrode input |
| CH2SET | `0x81` | unused: PD2 = 1 with the input short Table 22 note (1) asks for (IN2 is tied to AVDD on the board) |
| RLD_SENS | `0x23` | PDB_RLD, RLD from IN1P and IN1N |
| LOFF_SENS | `0x00` | off |
| RESP1 | `0x02` | required on the non-R ADS1292 |
| RESP2 | `0x07` | bit 2 RESP_FREQ must be written 1 on the ADS1292, bit 1 RLDREF_INT internal, bit 0 must be 1 (the lane wrote `0x02`) |

## Product nRF supply (REGOUT0)

On the product board the module runs in high-voltage mode (VDDH = VBAT)
and REG0 makes +VDD (`board-v2.md` §2). REG0's output is set by UICR
REGOUT0, and an erased UICR gives 1.8 V. The ADS1292 digital inputs need
VIH ≥ 0.8 × DVDD = 2.4 V at DVDD 3.0 V, so the product image must write
REGOUT0 = 3.0 V (the `REGOUT0_VOUT_3V0` value) on first boot and reset.
The Feather stand-in has its own 3.3 V regulator and does not need it.
Not coded this round (no product board id yet).

## VBUS and the AFE pins

With VBUS present the board turns the AFE rail off. The sketch then stops
acquisition without talking to the ADS1292 and puts SCK, MOSI, CS, PWDN
and START in high-impedance input mode, so no output back-feeds the
unpowered AFE through its input clamps. They are driven again when
acquisition restarts.

## G4 tests WP13 owns

Paper tests. None were run on hardware.

1. **First load.** With the kit connected ground-first, program the
   0.11.0 merged hex. Pass: `FTHR840BOOT` appears over USB, VID `0x239A`,
   PID `0x0029`, volume label `FTHR840BOOT`. Fail: no drive, or a
   different USB id. Probe/target I/O limits must be measured at the
   actual powered target voltage before this step counts (G4).
2. **Application update.** Copy a UF2 built by the command above onto
   that drive. Pass: the drive unmounts; the board enumerates as VID
   `0x239A` PID `0x8029`; a BLE central sees `elicio-v2` and receives a
   HELLO on connect.
3. **Recovery.** Double-press the DFU switch (D7 / P1.02). Pass:
   `FTHR840BOOT` appears again. Copy the same UF2. Pass: the board
   returns to the application USB id.
4. **Bad application.** Copy a truncated UF2, or abort the copy. Pass:
   double-press still reaches `FTHR840BOOT`. The bootloader region is
   not overwritten by a failed application copy.

## What was not exercised

No Feather, no Debug Probe, no Tag-Connect, no ADS1292, no cell, no
VBUS, no BLE peer. pyOCD and OpenOCD are not installed. The merged hex
was not downloaded. DRDY, SPI, NUS throughput at 2000 SPS, MTU
negotiation on air, the undervoltage thresholds on a pack, and the
hardware VBUS gate (R7/G2) were not run. The sketch reads
`NRF_POWER->USBREGSTATUS` for VBUS and `PIN_VBAT` for millivolts; those
are Feather stand-ins. LED_RED is the stream indicator, not the product
LED net. Acquisition continues while BLE is down; ring overflow is
overrun, not transport loss. A STREAM frame stops at the first gap in the
ring's acquisition indices, so its samples are always consecutive DRDYs,
and the frame after a gap carries OVERRUN. That behaviour is coded, not
measured.

## Pin header (WP13b, 2026-09-17)

`firmware/src/board_pins.h` now follows `docs/fab/board-v2.md` §9 (MDBT50Q nRF P0.xx), not the Feather header numbers. The Feather FQBN still compiles; those integers are not the product wiring on a Feather.
