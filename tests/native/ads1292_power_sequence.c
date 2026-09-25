/* Verify physical RESET occurs after POR and GPIO1/2 remain inputs. */
#include "ads1292.h"
#include <assert.h>
#include <stddef.h>
#include <stdint.h>

static char trace[128];
static unsigned count;
static unsigned n_regs;
static void put(char c) { assert(count < sizeof(trace)); trace[count++] = c; }
static void select_bus(int on) { (void)on; }
static void xfer(const uint8_t *tx, uint8_t *rx, size_t n) {
    (void)rx;
    if (n == 3 && tx[0] == (ADS1292_CMD_WREG | ADS1292_REG_GPIO)) {
        assert(tx[2] == 0x0cu);
        put('G');
    } else if (n == 3) {
        n_regs++;
    } else if (n == 1 && tx[0] == ADS1292_CMD_SDATAC) {
        put('S');
    }
}
static void wait_us(unsigned us) {
    if (us == 1000000u) put('P');
    if (us == 20u) put('W');
    if (us == 100u) put('R');
}
static void reset_pin(int high) { put(high ? 'H' : 'L'); }
static void start_pin(int high) { assert(!high); put('T'); }
int main(void) {
    const Ads1292Bus bus = {select_bus, xfer, wait_us, reset_pin, start_pin};
    assert(ads1292_apply_worn_regs(&bus) == 0);
    /* START low, release PWDN, POR wait, reset pulse, settle, SDATAC,
       normal configuration, then explicit GPIO inputs. */
    assert(count == 9);
    const char expected[] = {'T','H','P','L','W','H','R','S','G'};
    for (unsigned i = 0; i < count; i++) assert(trace[i] == expected[i]);
    assert(n_regs == ADS1292_WORN_REG_COUNT);
    return 0;
}
