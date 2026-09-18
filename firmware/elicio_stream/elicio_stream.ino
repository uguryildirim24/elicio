#include <SPI.h>
#include <bluefruit.h>

#include "board_pins.h"
#include "ads1292.h"
#include "frame_v2.h"
#include "undervoltage.h"

BLEUart bleuart;

#define RING_LEN 256

static uint8_t ring_samples[RING_LEN][ADS1292_SAMPLE_BYTES];
static uint16_t ring_acq[RING_LEN];
static volatile uint16_t ring_w;
static volatile uint16_t ring_r;
static volatile uint16_t acq_index;
static volatile uint8_t overrun_sticky;

static uint16_t session_id = 1;
static uint16_t epoch_id = 1;
static uint16_t frame_seq;
static uint16_t battery_seq;
static uint16_t nus_payload = 20;
static uint8_t streaming;
static uint8_t sent_stop;
static uint8_t pending_restart;
static UvMachine uv;
static uint32_t last_battery_ms;
static uint16_t next_acq;
static uint8_t have_next_acq;
static uint8_t afe_safe;

static void ads_select(int asserted) {
    digitalWrite(ELICIO_PIN_ADS_CS, asserted ? LOW : HIGH);
}

static void ads_xfer(const uint8_t *tx, uint8_t *rx, size_t n) {
    for (size_t i = 0; i < n; i++) {
        uint8_t b = SPI.transfer(tx ? tx[i] : 0);
        if (rx != NULL) {
            rx[i] = b;
        }
    }
}

static void ads_delay_us(unsigned us) { delayMicroseconds(us); }

static void ads_pwdn(int high) { digitalWrite(ELICIO_PIN_ADS_PWDN, high ? HIGH : LOW); }

static void ads_start_pin(int high) { digitalWrite(ELICIO_PIN_ADS_START, high ? HIGH : LOW); }

static const Ads1292Bus ADS_BUS = {
    ads_select, ads_xfer, ads_delay_us, ads_pwdn, ads_start_pin,
};

static uint8_t vbus_present(void) {
    return (NRF_POWER->USBREGSTATUS & POWER_USBREGSTATUS_VBUSDETECT_Msk) ? 1 : 0;
}

static uint16_t battery_mv(void) {
    /* Feather PIN_VBAT divider. WP12 replaces this with the product sense net. */
    float vbat = analogRead(PIN_VBAT) * 2.0f * 3.6f / 4096.0f;
    if (vbat < 0) {
        vbat = 0;
    }
    return (uint16_t)(vbat * 1000.0f);
}

static void drdy_isr(void) {
    uint16_t next = (uint16_t)((ring_w + 1u) % RING_LEN);
    uint16_t idx = acq_index;
    acq_index = (uint16_t)(acq_index + 1u);
    if (next == ring_r) {
        overrun_sticky = 1;
        return;
    }
    uint8_t sample[ADS1292_SAMPLE_BYTES];
    if (ads1292_read_sample(&ADS_BUS, sample) != 0) {
        overrun_sticky = 1;
        return;
    }
    memcpy(ring_samples[ring_w], sample, ADS1292_SAMPLE_BYTES);
    ring_acq[ring_w] = idx;
    ring_w = next;
}

static void send_packet(const uint8_t *p, uint16_t n) {
    if (!Bluefruit.connected()) {
        return;
    }
    bleuart.write(p, n);
}

static void send_logical(uint8_t msg, uint16_t seq, const uint8_t *logical, size_t logical_len) {
    uint8_t packed[512];
    uint16_t lens[16];
    uint8_t count = 0;
    if (frame_v2_fragment(msg, session_id, seq, logical, logical_len, nus_payload, packed,
                          sizeof(packed), lens, 16, &count) != 0) {
        return;
    }
    size_t off = 0;
    for (uint8_t i = 0; i < count; i++) {
        send_packet(packed + off, lens[i]);
        off += lens[i];
    }
}

static void send_hello(uint8_t flags, uint8_t reason) {
    FrameV2HelloMeta meta;
    memset(&meta, 0, sizeof(meta));
    meta.session_id = session_id;
    meta.epoch_id = epoch_id;
    meta.acq_index = acq_index;
    meta.nus_payload = nus_payload;
    meta.flags = flags;
    meta.stop_reason = reason;
    meta.gain = FRAME_V2_GAIN;
    meta.rate_id = FRAME_V2_RATE_2000;
    meta.vref_id = FRAME_V2_VREF_INT_242;
    meta.sample_bytes = FRAME_V2_SAMPLE_BYTES;
    uint8_t logical[FRAME_V2_HELLO_LEN + FRAME_V2_CRC_LEN];
    size_t n = 0;
    if (frame_v2_pack_hello(logical, sizeof(logical), &meta, &n) != 0) {
        return;
    }
    send_logical(FRAME_V2_MSG_HELLO, 0, logical, n);
}

static void send_battery(void) {
    FrameV2BatteryMeta meta;
    memset(&meta, 0, sizeof(meta));
    meta.session_id = session_id;
    meta.msg_seq = battery_seq++;
    meta.millivolts = battery_mv();
    meta.flags = uv.flags;
    meta.stop_reason = uv.stop_reason;
    uint8_t logical[FRAME_V2_BATTERY_LEN + FRAME_V2_CRC_LEN];
    size_t n = 0;
    if (frame_v2_pack_battery(logical, sizeof(logical), &meta, &n) != 0) {
        return;
    }
    send_logical(FRAME_V2_MSG_BATTERY, meta.msg_seq, logical, n);
}

static void send_stream(const FrameV2StreamMeta *meta, const uint8_t *samples) {
    uint8_t logical[FRAME_V2_MAX_LOGICAL];
    size_t n = 0;
    if (frame_v2_pack_stream(logical, sizeof(logical), meta, samples, &n) != 0) {
        return;
    }
    send_logical(FRAME_V2_MSG_STREAM, meta->frame_seq, logical, n);
    frame_seq = (uint16_t)(frame_seq + 1u);
}

/*
 * With VBUS present the board switches the AFE rail off (Q2 turns the P-FET
 * off, board-v2.md §4). An output left high into the unpowered ADS1292
 * would feed its rail through the input clamps, so the control and SPI
 * pins go high-impedance until VBUS is gone (review r5).
 */
static void afe_pins_safe(void) {
    if (afe_safe) {
        return;
    }
    SPI.endTransaction();
    SPI.end();
    pinMode(PIN_SPI_SCK, INPUT);
    pinMode(PIN_SPI_MOSI, INPUT);
    pinMode(ELICIO_PIN_ADS_CS, INPUT);
    pinMode(ELICIO_PIN_ADS_PWDN, INPUT);
    pinMode(ELICIO_PIN_ADS_START, INPUT);
    afe_safe = 1;
}

static void afe_pins_active(void) {
    pinMode(ELICIO_PIN_ADS_CS, OUTPUT);
    pinMode(ELICIO_PIN_ADS_PWDN, OUTPUT);
    pinMode(ELICIO_PIN_ADS_START, OUTPUT);
    digitalWrite(ELICIO_PIN_ADS_CS, HIGH);
    digitalWrite(ELICIO_PIN_ADS_PWDN, HIGH);
    digitalWrite(ELICIO_PIN_ADS_START, LOW);
    SPI.begin();
    SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE1));
    afe_safe = 0;
}

static void start_acquisition(void) {
    if (afe_safe) {
        afe_pins_active();
    }
    have_next_acq = 0;
    ring_w = 0;
    ring_r = 0;
    overrun_sticky = 0;
    ads1292_apply_worn_regs(&ADS_BUS);
    ads1292_start_rdatac(&ADS_BUS);
    attachInterrupt(digitalPinToInterrupt(ELICIO_PIN_ADS_DRDY), drdy_isr, FALLING);
    streaming = 1;
    sent_stop = 0;
    digitalWrite(ELICIO_PIN_LED_STREAM, HIGH);
}

static void stop_acquisition(void) {
    detachInterrupt(digitalPinToInterrupt(ELICIO_PIN_ADS_DRDY));
    ads1292_stop(&ADS_BUS);
    streaming = 0;
    digitalWrite(ELICIO_PIN_LED_STREAM, LOW);
}

static void connect_cb(uint16_t handle) {
    BLEConnection *conn = Bluefruit.Connection(handle);
    if (conn != NULL) {
        conn->requestMtuExchange(247);
        delay(20);
        uint16_t mtu = conn->getMtu();
        if (mtu > 3) {
            nus_payload = (uint16_t)(mtu - 3);
        }
    }
    send_hello(uv.flags, uv.stop_reason == FRAME_V2_STOP_NONE ? FRAME_V2_STOP_RESET : uv.stop_reason);
}

void setup() {
    pinMode(ELICIO_PIN_ADS_DRDY, INPUT);
    pinMode(ELICIO_PIN_LED_STREAM, OUTPUT);
    digitalWrite(ELICIO_PIN_LED_STREAM, LOW);
    afe_pins_active();

    uv_init(&uv);
    analogReadResolution(12);

    Bluefruit.configPrphBandwidth(BANDWIDTH_MAX);
    Bluefruit.begin();
    Bluefruit.setName("elicio-v2");
    Bluefruit.Periph.setConnectCallback(connect_cb);
    bleuart.begin();
    Bluefruit.Advertising.addFlags(BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE);
    Bluefruit.Advertising.addTxPower();
    Bluefruit.Advertising.addService(bleuart);
    Bluefruit.ScanResponse.addName();
    Bluefruit.Advertising.restartOnDisconnect(true);
    Bluefruit.Advertising.start(0);

    last_battery_ms = millis();
    if (vbus_present()) {
        afe_pins_safe();
    } else {
        start_acquisition();
    }
}

void loop() {
    uint8_t vbus = vbus_present();
    uint8_t was_stopped = (uv.state == UV_STOPPED);
    uv_update(&uv, battery_mv(), vbus);

    if (uv.flags & FRAME_V2_FLAG_VBUS) {
        if (streaming) {
            /* The AFE rail is already off: no SPI to it, pins high-Z. */
            detachInterrupt(digitalPinToInterrupt(ELICIO_PIN_ADS_DRDY));
            streaming = 0;
            digitalWrite(ELICIO_PIN_LED_STREAM, LOW);
        }
        afe_pins_safe();
        if (Bluefruit.connected() && !sent_stop) {
            FrameV2StreamMeta meta;
            memset(&meta, 0, sizeof(meta));
            meta.session_id = session_id;
            meta.frame_seq = frame_seq;
            meta.acq_index = acq_index;
            meta.sample_count = 0;
            meta.flags = uv.flags;
            meta.stop_reason = FRAME_V2_STOP_VBUS;
            meta.gain = FRAME_V2_GAIN;
            meta.sample_bytes = FRAME_V2_SAMPLE_BYTES;
            send_stream(&meta, NULL);
            sent_stop = 1;
        }
    } else if (uv.state == UV_STOPPED) {
        if (streaming) {
            stop_acquisition();
        }
        if (Bluefruit.connected() && !sent_stop) {
            FrameV2StreamMeta meta;
            memset(&meta, 0, sizeof(meta));
            meta.session_id = session_id;
            meta.frame_seq = frame_seq;
            meta.acq_index = acq_index;
            meta.sample_count = 0;
            meta.flags = uv.flags;
            meta.stop_reason = FRAME_V2_STOP_UNDERVOLTAGE;
            meta.gain = FRAME_V2_GAIN;
            meta.sample_bytes = FRAME_V2_SAMPLE_BYTES;
            send_stream(&meta, NULL);
            sent_stop = 1;
        }
    } else {
        if (was_stopped) {
            pending_restart = 1;
        }
        if (!streaming) {
            start_acquisition();
        }
    }

    if (streaming && Bluefruit.connected()) {
        uint16_t n = frame_v2_samples_for_nus(nus_payload);
        if (n == 0) {
            n = 1;
        }
        uint16_t avail = (uint16_t)((ring_w + RING_LEN - ring_r) % RING_LEN);
        if (avail >= n) {
            uint8_t payload[FRAME_V2_MAX_SAMPLES * ADS1292_SAMPLE_BYTES];
            uint16_t first = ring_acq[ring_r];
            noInterrupts();
            uint8_t over = overrun_sticky;
            overrun_sticky = 0;
            /* A frame's samples are consecutive DRDYs from acq_index
               (frame-v2.md): stop at the first gap the ring overrun left. */
            uint16_t k = 0;
            while (k < n && ring_r != ring_w && ring_acq[ring_r] == (uint16_t)(first + k)) {
                memcpy(payload + k * ADS1292_SAMPLE_BYTES, ring_samples[ring_r], ADS1292_SAMPLE_BYTES);
                ring_r = (uint16_t)((ring_r + 1u) % RING_LEN);
                k++;
            }
            interrupts();
            n = k;
            if (have_next_acq && first != next_acq) {
                over = 1;
            }
            next_acq = (uint16_t)(first + n);
            have_next_acq = 1;
            FrameV2StreamMeta meta;
            memset(&meta, 0, sizeof(meta));
            meta.session_id = session_id;
            meta.frame_seq = frame_seq;
            meta.acq_index = first;
            meta.sample_count = n;
            meta.payload_bytes = (uint16_t)(n * ADS1292_SAMPLE_BYTES);
            meta.flags = (uint8_t)((over ? FRAME_V2_FLAG_OVERRUN : 0) |
                                   (pending_restart ? FRAME_V2_FLAG_RESTART : 0));
            meta.stop_reason = FRAME_V2_STOP_NONE;
            meta.gain = FRAME_V2_GAIN;
            meta.rate_id = FRAME_V2_RATE_2000;
            meta.vref_id = FRAME_V2_VREF_INT_242;
            meta.sample_bytes = FRAME_V2_SAMPLE_BYTES;
            send_stream(&meta, payload);
            pending_restart = 0;
        }
    }

    uint32_t now = millis();
    if (Bluefruit.connected() && (now - last_battery_ms) >= 10000u) {
        last_battery_ms = now;
        send_battery();
    }
}
