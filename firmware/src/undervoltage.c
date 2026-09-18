#include "undervoltage.h"

#include "frame_v2.h"

void uv_init(UvMachine *m) {
    m->state = UV_RUN;
    m->vbus_present = 0;
    m->stop_reason = FRAME_V2_STOP_NONE;
    m->flags = 0;
}

void uv_update(UvMachine *m, uint16_t millivolts, uint8_t vbus_present) {
    m->vbus_present = vbus_present ? 1u : 0u;
    m->flags = 0;
    if (vbus_present) {
        m->state = UV_STOPPED;
        m->stop_reason = FRAME_V2_STOP_VBUS;
        m->flags = (uint8_t)(FRAME_V2_FLAG_VBUS | FRAME_V2_FLAG_STOPPED | FRAME_V2_FLAG_INVALID);
        return;
    }
    if (m->state == UV_RUN) {
        if (millivolts <= V_STOP_MV) {
            m->state = UV_STOPPED;
            m->stop_reason = FRAME_V2_STOP_UNDERVOLTAGE;
            m->flags = (uint8_t)(FRAME_V2_FLAG_STOPPED | FRAME_V2_FLAG_INVALID);
        } else {
            m->stop_reason = FRAME_V2_STOP_NONE;
            m->flags = 0;
        }
        return;
    }
    /* UV_STOPPED */
    if (millivolts >= V_START_MV) {
        m->state = UV_RUN;
        m->stop_reason = FRAME_V2_STOP_NONE;
        m->flags = FRAME_V2_FLAG_RESTART;
    } else {
        m->stop_reason = FRAME_V2_STOP_UNDERVOLTAGE;
        m->flags = (uint8_t)(FRAME_V2_FLAG_STOPPED | FRAME_V2_FLAG_INVALID);
    }
}
