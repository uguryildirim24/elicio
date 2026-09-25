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

The archived v2 map is `firmware/src/board_pins_v2.h` (MDBT50Q nRF P0.xx). The active `board_pins.h` is v4; it must not be built with the Feather variant. The historical Feather compile above was for the original v2 stand-in, **not** a v4 build.

## Frozen v4 pin map (WP13 / ISP1807-LR)

This table comes from committed `hardware/board/elicio-v4.kicad_sch` and
`elicio-v4.kicad_pcb`, U1's pad nets, checked against Insight SiP's ISP1807
R19 datasheet §3 pin table (pp. 10–11),
https://www.insightsip.com/fichiers_insightsip/pdf/ble/ISP1807/isp_ble_DS1807.pdf
(read 2026-09-25). Relevant rows (datasheet's `Pin` and `Name` cells; names use underscores):
"4 P0_10 NFC2", "6 P0_26", "13 P0_18 RESET", "32 P0_08",
"34 P0_06", "36 P0_05 AIN3", "38 P0_03 AIN1", "40 P0_02 AIN0",
"42 P0_31 AIN7", "44 P0_30 AIN6", "46 P0_29 AIN5",
"48 P0_28 AIN4". These are module **pad numbers**, not Arduino pins.

| U1 net | Pad | nRF pin | Direction at nRF | Constraint |
|---|---:|---|---|---|
| AFE_SCLK | 34 | P0.06 | out | SPIM3 SCK, 1 MHz; full-speed |
| AFE_MOSI | 36 | P0.05 | out | SPIM3 MOSI, full-speed |
| AFE_MISO | 32 | P0.08 | in | SPIM3 MISO, full-speed |
| AFE_CS | 48 | P0.28 | out | LF ≤10 kHz, standard drive; high-Z while U2 unpowered |
| AFE_DRDY | 46 | P0.29 | in | LF ≤10 kHz (2 kSPS DRDY) |
| AFE_START | 4 | P0.10/NFC2 | out | LF only; disable UICR NFCPINS protection; high-Z while U2 unpowered |
| AFE_RESET (ADS PWDN/RESET) | 6 | P0.26 | out | High-Z while U2 unpowered |
| CHG_MON | 44 | P0.30/AIN6 | analog in | ISET via R25; no separate /CHG status output |
| VBAT_SENSE | 42 | P0.31/AIN7 | analog in | R20/R21 1 MΩ/1 MΩ divider, LF |
| VBUS_DET | 40 | P0.02 | digital in | R18/R19 divider, LF; **not** USBREGSTATUS (U1 USB unconnected) |
| LED_EN | 38 | P0.03 | out | LF; Q4 gate/10 kΩ pull-down, LED powered from VBUS; not a stream LED |
| nRESET | 13 | P0.18/RESET | in | SW1 + SWD J4; configure UICR PSELRESET[0/1]=18; no external pull-up |
| SWDIO / SWDCLK | 28 / 30 | SWDIO / SWDCLK | bidirectional / in | J4 factory programming; not application GPIO |
| +VDD | 26 | VCC_nRF | power in | 3.0 V from U5; no v2 REGOUT0/VDDH first-boot programming |
| RF_ANT | 20, 22 | OUT_ANT, OUT_MOD | RF | antenna path, not GPIO |
| GND | 1, 7, 14, 16, 18, 21, 23, 24, 25, 31 | VSS | power | VSS 14/16/18 use via pair between pads |

All other U1 pads are unconnected, including USB D± pads 8/10 and VBUS pad
12; the U1 pad 2 P0.09/NFC1 is open. BAT_MEAS_EN/Q5 is removed: no MCU AFE
power-enable line exists. Q2/Q3/Q1 gate AFE power **in hardware** on charging;
the GPIOs to U2 must be high-Z while off. R26 (external reset pull-up) was
removed; SW1 only resets after PSELRESET is provisioned. P0.09 and P0.10
must be driven to the same level before sleep with NFC reassigned to GPIO.
P0.28/29/30/31/02/03/10 are low-frequency-only; none should carry SPI data.

The sketch now reads VBUS_DET and VBAT_SENSE and uses a dedicated SPIM3
object wired to the table, but it **requires an ISP1807 v4 Arduino variant**
that maps digital numbers to these actual pins and configures SAADC reference;
UICR NFC/reset must be provisioned over J4 as below. There is no such
product variant in this tree: a Feather compile is deliberately rejected
rather than claiming the wrong
wiring works. `CHG_MON` is mapped but its charge/termination thresholds are
not characterized; until they are, LED_EN stays off (not an acquisition
indicator). No bootloader flash, physical board, BLE link or charge-state
validation was performed for v4. The earlier v2 build and flash instructions
above are historical and are **not** v4 release instructions.

### v4 circuit-review actions (board-v4-refcheck, 2026-09-25)

1. **NFC2 / first flash:** Pad 4 is P0.10/NFC2; it will not reliably drive
   AFE_START as a GPIO with NFC protection enabled. On a blank module, connect
   J4 SWDIO/SWDCLK/GND at the measured target voltage and use the SWD
   programmer to set **UICR NFCPINS.PROTECT = Disabled** (Zephyr equivalent
   `CONFIG_NFCT_PINS_AS_GPIOS=y`), verify readback, then reset/power-cycle
   before the application sets P0.10 as an output. Never assume an Arduino
   upload, a fresh erased UICR, or a Feather bootloader makes this change.
   Pad 2 P0.09/NFC1 is unconnected; before any low-power mode, drive NFC1
   to START's level or disable NFC functions consistently as specified in the
   nRF52840 product specification §6.14.3. There is no v4 provisioning image
   or low-power implementation yet; **first flash is not ready**.
2. **Reset / first flash:** In the same J4 SWD provisioning step program
   **both UICR PSELRESET[0] and [1] = 18** (P0.18), read back both values,
   reset/power-cycle, then confirm SW1 pulls module reset low and SWD still
   works. No external reset pull-up exists. This is not a command to drive
   P0.18 from the application; the first programming can use SWD without a
   working reset pin. No first-flash script or factory verification exists here.

   **Exact J4 provisioning example (Nordic `nrfjprog` + J-Link, nRF52840):**
   On an unprovisioned module, connect J4.1 to VTref (+VDD), J4.2 to SWDIO,
   J4.3 or J4.5 to GND and J4.4 to SWDCLK; J4.6 is nRESET and need not
   work yet. Power the board at its measured 3.0 V target voltage, with no
   electrode or wearer attached. First read all three words; **stop if any
   is not `0xFFFFFFFF`**. Do not mass-erase a programmed device to make
   these commands work: UICR writes can clear bits but cannot restore them
   without an erase, which may destroy a bootloader or other provisioning.

   ```sh
   nrfjprog --family NRF52 --memrd 0x1000120C --w 32 --n 4  # NFCPINS
   nrfjprog --family NRF52 --memrd 0x10001200 --w 32 --n 4  # PSELRESET[0]
   nrfjprog --family NRF52 --memrd 0x10001204 --w 32 --n 4  # PSELRESET[1]
   # Each preflight read above must report FFFFFFFF at its address.
   nrfjprog --family NRF52 --memwr 0x1000120C --val 0xFFFFFFFE
   nrfjprog --family NRF52 --memwr 0x10001200 --val 0x7FFFFFD2
   nrfjprog --family NRF52 --memwr 0x10001204 --val 0x7FFFFFD2
   nrfjprog --family NRF52 --memrd 0x1000120C --w 32 --n 4  # expect FFFFFFFE
   nrfjprog --family NRF52 --memrd 0x10001200 --w 32 --n 4  # expect 7FFFFFD2
   nrfjprog --family NRF52 --memrd 0x10001204 --w 32 --n 4  # expect 7FFFFFD2
   nrfjprog --family NRF52 --reset
   nrfjprog --family NRF52 --memrd 0x1000120C --w 32 --n 4  # FFFFFFFE
   nrfjprog --family NRF52 --memrd 0x10001200 --w 32 --n 4  # 7FFFFFD2
   nrfjprog --family NRF52 --memrd 0x10001204 --w 32 --n 4  # 7FFFFFD2
   ```

   The addresses are UICR base `0x10001000` plus offsets `0x20C`, `0x200`
   and `0x204` (nRF52840 MDK `nrf52840.h`). `NFCPINS.PROTECT=0` disables
   NFC protection so P0.10 can be a GPIO; both PSELRESET words select
   `CONNECT=0`, `PORT=0`, `PIN=18` while leaving reserved bits erased
   (`0x7FFFFFD2`; MDK `nrf52840_bitfields.h`). If the values differ or
   cannot be read, **stop before running the sketch**. The application must
   not overwrite UICR, and any later erase requires this step again. After
   reset, verify SW1 resets U1 and SWD remains accessible. These are
   specified commands, not a tested factory flash or an available v4 image.
   Without the NFCPINS step, **AFE_START on P0.10 will not work**.

3. **Internal clock/data rate:** U2 CLKSEL is tied to +3V0, CLK is open,
   CONFIG2.CLK_EN=0. With the default internal oscillator at nominal
   fCLK=512 kHz, fMOD=128 kHz, CONFIG1 DR[2:0]=100 gives fMOD/64 = 2000
   samples/s (nominal 500 µs between DRDY). A 1 MHz SPI clock is below the
   2×fCLK register-access limit at nominal frequency. Frequency varies with
   temperature; frame timestamps and an exactly constant 2 kHz rate have
   **not** been validated on silicon. TI ADS1292 SBAS502C §§8.3.7,
   8.6.1.2, Fig. 44.
4. **Power ramp/POR:** R23/R24 hold U2 PWDN/RESET and START low before MCU
   setup. The sketch now holds both low until acquisition. After AFE power
   is available the driver releases PWDN, waits 1 second (TI Fig. 44),
   drives it low for 20 µs for a separate RESET pulse, releases it, waits
   100 µs (>18 internal tCLK at nominal frequency), then sends SDATAC and
   configures registers with START still low. TI §10.1/Table 29 requires
   all digital and analog inputs low during the rail ramp: **the board has
   no rail-good feedback or pull-downs on every SPI input**, so CS/SCLK/MOSI
   during the actual ramp and supply settling remain to be checked and, if
   needed, corrected by the board session. A firmware delay does not prove
   the analog rail is stable.
5. **Unused GPIO and ADC limits:** U2 GPIO register is written `0x0C` after
   every reset, keeping GPIO1/2 configured as inputs (TI §8.5.1.7); the
   board session must fit pull-down resistors because they float during POR
   otherwise. For *unused ISP1807 GPIOs*, the future product variant must
   configure unconnected P0/P1 pads to non-driving, defined low-leakage
   states and avoid conflicting with radio/SWD/NFC; this sketch cannot
   safely enumerate them without that variant. P0.09's NFC leakage is
   separately called out above. VBAT_SENSE is VBAT/2 via 1 MΩ+1 MΩ:
   at a 4.2 V cell it is 2.1 V, below 3.0 V VDD (but measure divider
   tolerance, leakage and ADC settling). CHG_MON is ISET through 10 kΩ:
   verify its maximum at all charger states and transients remains within
   the nRF input absolute rating relative to 3.0 V VDD; its range is **not
   qualified** yet. Confirm SAADC reference/gain and acquisition time for
   the 500 kΩ divider source on the actual variant before trusting battery
   millivolts or applying undervoltage cutoffs.
6. **LED and charge indication:** BQ25100 has no PG or /CHG status output.
   D2/Q4 (LED_EN) is powered from VBUS and may be controlled by firmware,
   but neither it nor a single ISET voltage read is an independent,
   verified charge-status signal. The sketch leaves LED_EN off and does not
   decode CHG_MON into a charging/full indication. If charge status is
   essential, it needs a charger/status circuit change and validation.
7. **Board GPIO pull-downs:** U2 GPIO1/2 input setting is explicit in the
   driver; firmware will not drive them high or use them for respiration.
   Board pull-downs are an order blocker, not a software substitute.
