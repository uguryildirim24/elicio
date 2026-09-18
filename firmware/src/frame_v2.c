#include "frame_v2.h"

#include <string.h>

static void wr_u16(uint8_t *p, uint16_t v) {
    p[0] = (uint8_t)(v & 0xffu);
    p[1] = (uint8_t)((v >> 8) & 0xffu);
}

static void wr_u32(uint8_t *p, uint32_t v) {
    p[0] = (uint8_t)(v & 0xffu);
    p[1] = (uint8_t)((v >> 8) & 0xffu);
    p[2] = (uint8_t)((v >> 16) & 0xffu);
    p[3] = (uint8_t)((v >> 24) & 0xffu);
}

uint32_t frame_v2_crc32(const uint8_t *data, size_t len) {
    uint32_t c = 0xffffffffu;
    for (size_t i = 0; i < len; i++) {
        c ^= data[i];
        for (int b = 0; b < 8; b++) {
            uint32_t mask = (uint32_t)-(int)(c & 1u);
            c = (c >> 1) ^ (0xedb88320u & mask);
        }
    }
    return ~c;
}

static int finish_crc(uint8_t *out, size_t body_len, size_t out_cap, size_t *out_len) {
    if (body_len + FRAME_V2_CRC_LEN > out_cap) {
        return -1;
    }
    uint32_t crc = frame_v2_crc32(out, body_len);
    wr_u32(out + body_len, crc);
    if (out_len != NULL) {
        *out_len = body_len + FRAME_V2_CRC_LEN;
    }
    return 0;
}

int frame_v2_pack_stream(uint8_t *out, size_t out_cap, const FrameV2StreamMeta *meta,
                         const uint8_t *samples, size_t *out_len) {
    if (out == NULL || meta == NULL) {
        return -1;
    }
    if (meta->sample_count > FRAME_V2_MAX_SAMPLES) {
        return -1;
    }
    if (meta->sample_bytes != FRAME_V2_SAMPLE_BYTES) {
        return -1;
    }
    if (meta->payload_bytes != (uint16_t)(meta->sample_count * FRAME_V2_SAMPLE_BYTES)) {
        return -1;
    }
    size_t body = FRAME_V2_STREAM_HDR + (size_t)meta->payload_bytes;
    if (body + FRAME_V2_CRC_LEN > out_cap) {
        return -1;
    }
    wr_u16(out + 0, meta->session_id);
    wr_u16(out + 2, meta->frame_seq);
    wr_u16(out + 4, meta->acq_index);
    wr_u16(out + 6, meta->sample_count);
    out[8] = meta->flags;
    out[9] = meta->stop_reason;
    out[10] = meta->gain;
    out[11] = meta->rate_id;
    out[12] = meta->vref_id;
    out[13] = meta->sample_bytes;
    wr_u16(out + 14, meta->payload_bytes);
    if (meta->payload_bytes > 0) {
        if (samples == NULL) {
            return -1;
        }
        memcpy(out + FRAME_V2_STREAM_HDR, samples, meta->payload_bytes);
    }
    return finish_crc(out, body, out_cap, out_len);
}

int frame_v2_pack_hello(uint8_t *out, size_t out_cap, const FrameV2HelloMeta *meta, size_t *out_len) {
    if (out == NULL || meta == NULL) {
        return -1;
    }
    if (FRAME_V2_HELLO_LEN + FRAME_V2_CRC_LEN > out_cap) {
        return -1;
    }
    wr_u16(out + 0, meta->session_id);
    wr_u16(out + 2, meta->epoch_id);
    wr_u16(out + 4, meta->acq_index);
    wr_u16(out + 6, meta->nus_payload);
    out[8] = meta->flags;
    out[9] = meta->stop_reason;
    out[10] = meta->gain;
    out[11] = meta->rate_id;
    out[12] = meta->vref_id;
    out[13] = meta->sample_bytes;
    wr_u16(out + 14, meta->reserved);
    return finish_crc(out, FRAME_V2_HELLO_LEN, out_cap, out_len);
}

int frame_v2_pack_battery(uint8_t *out, size_t out_cap, const FrameV2BatteryMeta *meta,
                          size_t *out_len) {
    if (out == NULL || meta == NULL) {
        return -1;
    }
    if (FRAME_V2_BATTERY_LEN + FRAME_V2_CRC_LEN > out_cap) {
        return -1;
    }
    wr_u16(out + 0, meta->session_id);
    wr_u16(out + 2, meta->msg_seq);
    wr_u16(out + 4, meta->millivolts);
    out[6] = meta->flags;
    out[7] = meta->stop_reason;
    wr_u32(out + 8, meta->reserved);
    return finish_crc(out, FRAME_V2_BATTERY_LEN, out_cap, out_len);
}

uint16_t frame_v2_samples_for_nus(uint16_t nus_payload) {
    if (nus_payload <= FRAME_V2_FRAG_HDR) {
        return 0;
    }
    uint16_t data = (uint16_t)(nus_payload - FRAME_V2_FRAG_HDR);
    /* Prefer one fragment: logical = 16 + 9N + 4 must fit in data. */
    if (data < FRAME_V2_STREAM_HDR + FRAME_V2_CRC_LEN) {
        return 1;
    }
    uint16_t n = (uint16_t)((data - FRAME_V2_STREAM_HDR - FRAME_V2_CRC_LEN) / FRAME_V2_SAMPLE_BYTES);
    if (n > FRAME_V2_MAX_SAMPLES) {
        n = FRAME_V2_MAX_SAMPLES;
    }
    if (n == 0) {
        /* Small MTU: still send at least one sample using several fragments. */
        n = 1;
    }
    return n;
}

int frame_v2_fragment(uint8_t msg_type, uint16_t session_id, uint16_t frame_seq,
                      const uint8_t *logical, size_t logical_len, uint16_t nus_payload,
                      uint8_t *out, size_t out_cap, uint16_t *frag_lens, uint8_t frag_lens_cap,
                      uint8_t *frag_count) {
    if (logical == NULL || out == NULL || frag_lens == NULL || frag_count == NULL) {
        return -1;
    }
    if (nus_payload <= FRAME_V2_FRAG_HDR) {
        return -1;
    }
    size_t chunk = (size_t)nus_payload - FRAME_V2_FRAG_HDR;
    size_t nfrag = (logical_len + chunk - 1u) / chunk;
    if (nfrag == 0) {
        nfrag = 1;
    }
    if (nfrag > 255u || nfrag > frag_lens_cap) {
        return -1;
    }
    size_t cursor = 0;
    size_t written = 0;
    for (size_t i = 0; i < nfrag; i++) {
        size_t remain = logical_len - cursor;
        size_t take = remain < chunk ? remain : chunk;
        size_t pkt = FRAME_V2_FRAG_HDR + take;
        if (written + pkt > out_cap) {
            return -1;
        }
        uint8_t *p = out + written;
        p[0] = (uint8_t)FRAME_V2_VERSION;
        p[1] = msg_type;
        wr_u16(p + 2, session_id);
        wr_u16(p + 4, frame_seq);
        p[6] = (uint8_t)i;
        p[7] = (uint8_t)nfrag;
        if (take > 0) {
            memcpy(p + FRAME_V2_FRAG_HDR, logical + cursor, take);
        }
        frag_lens[i] = (uint16_t)pkt;
        written += pkt;
        cursor += take;
    }
    *frag_count = (uint8_t)nfrag;
    return 0;
}
