#ifndef ELICIO_UNDERVOLTAGE_H
#define ELICIO_UNDERVOLTAGE_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Pack-voltage thresholds from WP12, docs/fab/board-v2.md §6 (V_STOP_V 3.00,
 * V_START_V 3.20). Plan v2 §5.5: inhibit acquisition at V_STOP so AVDD
 * stays above the ADS1292's 2.7 V minimum through the TLV71330's dropout
 * (150 mV bound), sense error and radio transients; resume only above
 * V_START after rail and reference settling. Computed, not measured.
 */
#ifndef V_STOP_MV
#define V_STOP_MV 3000u
#endif
#ifndef V_START_MV
#define V_START_MV 3200u
#endif

typedef enum {
    UV_RUN = 0,
    UV_STOPPED = 1
} UvState;

typedef struct {
    UvState state;
    uint8_t vbus_present;
    uint8_t stop_reason;
    uint8_t flags;
} UvMachine;

void uv_init(UvMachine *m);
void uv_update(UvMachine *m, uint16_t millivolts, uint8_t vbus_present);

#ifdef __cplusplus
}
#endif

#endif
