#include "frame_v2.h"
#include "undervoltage.h"
#include "ads1292.h"

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void die(const char *msg) {
    fprintf(stderr, "%s\n", msg);
    exit(2);
}

static uint16_t rd_u16(const uint8_t *p) { return (uint16_t)(p[0] | ((uint16_t)p[1] << 8)); }

int main(int argc, char **argv) {
    uint8_t in[4096];
    size_t nread = fread(in, 1, sizeof(in), stdin);
    if (nread < 1) {
        die("empty stdin");
    }
    uint8_t op = in[0];
    uint8_t out[4096];
    size_t out_len = 0;
    if (op == 1) {
        /* pack stream: 1 + StreamMeta 16 + samples */
        if (nread < 1 + 16) {
            die("short stream meta");
        }
        FrameV2StreamMeta meta;
        meta.session_id = rd_u16(in + 1);
        meta.frame_seq = rd_u16(in + 3);
        meta.acq_index = rd_u16(in + 5);
        meta.sample_count = rd_u16(in + 7);
        meta.flags = in[9];
        meta.stop_reason = in[10];
        meta.gain = in[11];
        meta.rate_id = in[12];
        meta.vref_id = in[13];
        meta.sample_bytes = in[14];
        meta.payload_bytes = rd_u16(in + 15);
        const uint8_t *samples = in + 17;
        size_t sample_bytes = nread - 17;
        if (sample_bytes != meta.payload_bytes) {
            die("sample length");
        }
        if (frame_v2_pack_stream(out, sizeof(out), &meta, samples, &out_len) != 0) {
            die("pack_stream");
        }
    } else if (op == 2) {
        if (nread != 1 + 16) {
            die("hello size");
        }
        FrameV2HelloMeta meta;
        meta.session_id = rd_u16(in + 1);
        meta.epoch_id = rd_u16(in + 3);
        meta.acq_index = rd_u16(in + 5);
        meta.nus_payload = rd_u16(in + 7);
        meta.flags = in[9];
        meta.stop_reason = in[10];
        meta.gain = in[11];
        meta.rate_id = in[12];
        meta.vref_id = in[13];
        meta.sample_bytes = in[14];
        meta.reserved = rd_u16(in + 15);
        if (frame_v2_pack_hello(out, sizeof(out), &meta, &out_len) != 0) {
            die("pack_hello");
        }
    } else if (op == 3) {
        if (nread != 1 + 12) {
            die("battery size");
        }
        FrameV2BatteryMeta meta;
        meta.session_id = rd_u16(in + 1);
        meta.msg_seq = rd_u16(in + 3);
        meta.millivolts = rd_u16(in + 5);
        meta.flags = in[7];
        meta.stop_reason = in[8];
        meta.reserved = (uint32_t)in[9] | ((uint32_t)in[10] << 8) | ((uint32_t)in[11] << 16) |
                        ((uint32_t)in[12] << 24);
        if (frame_v2_pack_battery(out, sizeof(out), &meta, &out_len) != 0) {
            die("pack_battery");
        }
    } else if (op == 4) {
        /* fragment: 1, msg, session u16, seq u16, nus u16, logical... */
        if (nread < 8) {
            die("short fragment request");
        }
        uint8_t msg = in[1];
        uint16_t session = rd_u16(in + 2);
        uint16_t seq = rd_u16(in + 4);
        uint16_t nus = rd_u16(in + 6);
        const uint8_t *logical = in + 8;
        size_t logical_len = nread - 8;
        uint16_t lens[16];
        uint8_t count = 0;
        uint8_t packed[4096];
        if (frame_v2_fragment(msg, session, seq, logical, logical_len, nus, packed, sizeof(packed),
                              lens, 16, &count) != 0) {
            die("fragment");
        }
        out[0] = count;
        size_t o = 1;
        size_t src = 0;
        for (uint8_t i = 0; i < count; i++) {
            out[o++] = (uint8_t)(lens[i] & 0xffu);
            out[o++] = (uint8_t)((lens[i] >> 8) & 0xffu);
            memcpy(out + o, packed + src, lens[i]);
            o += lens[i];
            src += lens[i];
        }
        out_len = o;
    } else if (op == 5) {
        /* uv: 1, mv u16, vbus u8 → state, flags, reason */
        if (nread < 4) {
            die("uv size");
        }
        UvMachine m;
        uv_init(&m);
        uint16_t mv = rd_u16(in + 1);
        uv_update(&m, mv, in[3]);
        out[0] = (uint8_t)m.state;
        out[1] = m.flags;
        out[2] = m.stop_reason;
        out_len = 3;
        if (nread >= 7) {
            mv = rd_u16(in + 4);
            uv_update(&m, mv, in[6]);
            out[3] = (uint8_t)m.state;
            out[4] = m.flags;
            out[5] = m.stop_reason;
            out_len = 6;
        }
    } else if (op == 6) {
        out[0] = (uint8_t)ADS1292_WORN_REG_COUNT;
        for (unsigned i = 0; i < ADS1292_WORN_REG_COUNT; i++) {
            out[1 + 2 * i] = ADS1292_WORN_REGS[i].addr;
            out[2 + 2 * i] = ADS1292_WORN_REGS[i].value;
        }
        out_len = 1u + 2u * ADS1292_WORN_REG_COUNT;
    } else {
        die("unknown op");
    }
    if (fwrite(out, 1, out_len, stdout) != out_len) {
        die("write");
    }
    return 0;
}
