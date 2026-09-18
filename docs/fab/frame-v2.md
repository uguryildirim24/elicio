# Frame contract v2

Byte-level streaming format for the Stage B ADS1292 path. Frozen before S0
(plan v2 §6). Little-endian. Version byte `2`.

Nominal scale, metadata only, not applied by the decoder:

`2.42 V / (12 × (2^23 − 1)) ≈ 24.04 nV` per code; differential full scale
about `± 201.7 mV`.

16-bit `acq_index` at 2000 SPS wraps every 32.768 s. Width stays 16 bits
because that is the plan's wrap. The receiver extends it in software by
counting wraps in one session.

N (sample count) is transmitted in every STREAM header. It follows the
negotiated NUS payload (`ATT MTU − 3`): as many 9-byte samples as fit in
one fragment when that is at least one sample; otherwise one sample split
across fragments. N is not fixed by the version.

## Packets on BLE NUS

Every NUS write is one fragment:

| Offset | Size | Field |
|---|---:|---|
| 0 | 1 | version = 2 |
| 1 | 1 | message type |
| 2 | 2 | session_id |
| 4 | 2 | frame_seq (per type) |
| 6 | 1 | frag_index, 0-based |
| 7 | 1 | frag_count, ≥ 1 |
| 8 | … | slice of the logical message |

A truncated NUS write is a partial frame. Drop it. Do not emit samples
from an incomplete fragment set. Fragments of one logical message may
arrive in any order. Reassemble by `(session_id, type, frame_seq)`.

CRC-32/ISO-HDLC (poly `0xEDB88320`, zlib) covers the logical message
only, not the fragment header. It occupies the last four bytes of the
logical message.

## Message types

| Type | Name | Logical body before CRC |
|---|---|---|
| 0x00 | HELLO | 16 bytes |
| 0x01 | STREAM | 16-byte header + `N × 9` sample bytes |
| 0x02 | BATTERY | 12 bytes |

### HELLO (on connect, and after a device reset)

| Offset | Size | Field |
|---|---:|---|
| 0 | 2 | session_id |
| 2 | 2 | epoch_id (same as session_id in this version; new value after reset) |
| 4 | 2 | acq_index now |
| 6 | 2 | negotiated NUS payload in bytes |
| 8 | 1 | flags |
| 9 | 1 | stop_reason |
| 10 | 1 | gain (12) |
| 11 | 1 | rate_id (0 = 2000 SPS) |
| 12 | 1 | vref_id (0 = internal 2.42 V) |
| 13 | 1 | sample_bytes (9) |
| 14 | 2 | reserved 0 |
| 16 | 4 | CRC32 |

### STREAM

| Offset | Size | Field |
|---|---:|---|
| 0 | 2 | session_id |
| 2 | 2 | frame_seq |
| 4 | 2 | acq_index of the first sample (DRDY count, not successful-read count) |
| 6 | 2 | sample_count N |
| 8 | 1 | flags |
| 9 | 1 | stop_reason |
| 10 | 1 | gain (12) |
| 11 | 1 | rate_id (0 = 2000 SPS) |
| 12 | 1 | vref_id (0 = internal 2.42 V) |
| 13 | 1 | sample_bytes (9) |
| 14 | 2 | payload_bytes = N × 9 |
| 16 | N × 9 | samples |
| 16 + N×9 | 4 | CRC32 |

Each sample is the ADS1292 DOUT word (TI SBAS502C, read 2026-09-17): 24-bit
status, 24-bit channel 1, 24-bit channel 2. Status format is
`(1100 + LOFF_STAT + GPIO)` as the datasheet's data-output protocol. Lead-off
is off when worn; those status bits are stored and ignored.

`acq_index` increments on every DRDY, including conversions that are not
stored because the ring is full. A jump larger than N, or flag bit 1, is
acquisition overrun. A gap in `frame_seq` is transport loss. They are
never the same bit.

### BATTERY (every 10 s; not the protective-monitor cadence)

| Offset | Size | Field |
|---|---:|---|
| 0 | 2 | session_id |
| 2 | 2 | msg_seq |
| 4 | 2 | millivolts |
| 6 | 1 | flags |
| 7 | 1 | stop_reason |
| 8 | 4 | reserved 0 |
| 12 | 4 | CRC32 |

## Flags and stop reasons

| Bit | Flag |
|---:|---|
| 0 | INVALID samples (undervoltage inhibit) |
| 1 | OVERRUN (acquisition ring) |
| 2 | STOPPED |
| 3 | RESTART (crossed V_START) |
| 4 | VBUS present |

| Value | stop_reason |
|---:|---|
| 0 | none |
| 1 | undervoltage (V_STOP) |
| 2 | VBUS |
| 3 | reset |
| 4 | host |

## Reconnect and reset

- Power-on reset: `session_id` and `epoch_id` take a new value, `acq_index`
  and `frame_seq` are 0, HELLO carries `stop_reason = reset`.
- BLE reconnect without reset: same `session_id`, `acq_index` and
  `frame_seq` continue, HELLO is sent again so the receiver resyncs.
  Acquisition keeps running while disconnected; ring overrun is still
  overrun, not transport loss.
- VBUS present: streaming refused. One STREAM with N = 0 and flags VBUS |
  STOPPED | INVALID, then no further STREAM until VBUS is gone. Battery
  messages continue.
- V_STOP: acquisition stops. STREAM N = 0 with INVALID | STOPPED and
  reason undervoltage. Resume only above V_START with RESTART set on the
  first STREAM that carries samples again.

Partial frames are rejected. Version ≠ 2 is a version mismatch. Bad CRC
drops the logical message.

## Receiver fixtures

Golden bytes live in `tests/fixtures/frame_v2/` for normal, wrap,
fragment, reorder, loss, overrun, partial, reconnect, bad CRC, and
version mismatch. `elicio.frame_v2` and the C framer must match them.
