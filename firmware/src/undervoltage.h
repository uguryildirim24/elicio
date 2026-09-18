#ifndef ELICIO_UNDERVOLTAGE_H
#define ELICIO_UNDERVOLTAGE_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/*
 * V_STOP and V_START are from WP12.
 * Plan v2 §5.5: inhibit acquisition when the monitored voltage falls to
 * V_STOP, chosen so AVDD stays valid (ADS1292 AVDD min 2.7 V, TI SBAS502C
 * 2026-09-17 read of the public datasheet). Resume only above V_START > V_STOP
 * after rail and reference settling. WP12 has not published the computed
 * millivolt values (LDO dropout, sense error, radio transients). These
 * placeholders let the state machine compile; they are not measured.
 */
#ifndef V_STOP_MV
#define V_STOP_MV 2700u /* from WP12 */
#endif
#ifndef V_START_MV
#define V_START_MV 2800u /* from WP12 */
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
