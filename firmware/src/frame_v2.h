#ifndef ELICIO_FRAME_V2_H
#define ELICIO_FRAME_V2_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Byte contract frozen in docs/fab/frame-v2.md. Little-endian. */

#define FRAME_V2_VERSION 2u
#define FRAME_V2_SPS 2000u
#define FRAME_V2_GAIN 12u
#define FRAME_V2_SAMPLE_BYTES 9u
#define FRAME_V2_FRAG_HDR 8u
#define FRAME_V2_STREAM_HDR 16u
#define FRAME_V2_HELLO_LEN 16u
#define FRAME_V2_BATTERY_LEN 12u
#define FRAME_V2_CRC_LEN 4u
#define FRAME_V2_MAX_SAMPLES 40u
#define FRAME_V2_MAX_LOGICAL \
    (FRAME_V2_STREAM_HDR + (size_t)FRAME_V2_MAX_SAMPLES * FRAME_V2_SAMPLE_BYTES + FRAME_V2_CRC_LEN)

#define FRAME_V2_MSG_HELLO 0x00u
#define FRAME_V2_MSG_STREAM 0x01u
#define FRAME_V2_MSG_BATTERY 0x02u

#define FRAME_V2_FLAG_INVALID 0x01u
#define FRAME_V2_FLAG_OVERRUN 0x02u
#define FRAME_V2_FLAG_STOPPED 0x04u
#define FRAME_V2_FLAG_RESTART 0x08u
#define FRAME_V2_FLAG_VBUS 0x10u

#define FRAME_V2_STOP_NONE 0u
#define FRAME_V2_STOP_UNDERVOLTAGE 1u
#define FRAME_V2_STOP_VBUS 2u
#define FRAME_V2_STOP_RESET 3u
#define FRAME_V2_STOP_HOST 4u

#define FRAME_V2_RATE_2000 0u
#define FRAME_V2_VREF_INT_242 0u

typedef struct {
    uint16_t session_id;
    uint16_t frame_seq;
    uint16_t acq_index;
    uint16_t sample_count;
    uint8_t flags;
    uint8_t stop_reason;
    uint8_t gain;
    uint8_t rate_id;
    uint8_t vref_id;
    uint8_t sample_bytes;
    uint16_t payload_bytes;
} FrameV2StreamMeta;

typedef struct {
    uint16_t session_id;
    uint16_t epoch_id;
    uint16_t acq_index;
    uint16_t nus_payload;
    uint8_t flags;
    uint8_t stop_reason;
    uint8_t gain;
    uint8_t rate_id;
    uint8_t vref_id;
    uint8_t sample_bytes;
    uint16_t reserved;
} FrameV2HelloMeta;

typedef struct {
    uint16_t session_id;
    uint16_t msg_seq;
    uint16_t millivolts;
    uint8_t flags;
    uint8_t stop_reason;
    uint32_t reserved;
} FrameV2BatteryMeta;

uint32_t frame_v2_crc32(const uint8_t *data, size_t len);

int frame_v2_pack_stream(uint8_t *out, size_t out_cap, const FrameV2StreamMeta *meta,
                         const uint8_t *samples, size_t *out_len);

int frame_v2_pack_hello(uint8_t *out, size_t out_cap, const FrameV2HelloMeta *meta,
                        size_t *out_len);

int frame_v2_pack_battery(uint8_t *out, size_t out_cap, const FrameV2BatteryMeta *meta,
                          size_t *out_len);

int frame_v2_fragment(uint8_t msg_type, uint16_t session_id, uint16_t frame_seq,
                      const uint8_t *logical, size_t logical_len, uint16_t nus_payload,
                      uint8_t *out, size_t out_cap, uint16_t *frag_lens, uint8_t frag_lens_cap,
                      uint8_t *frag_count);

uint16_t frame_v2_samples_for_nus(uint16_t nus_payload);

#ifdef __cplusplus
}
#endif

#endif
