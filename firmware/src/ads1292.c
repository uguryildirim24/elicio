#include "ads1292.h"

#include <string.h>

const Ads1292Reg ADS1292_WORN_REGS[] = {
    {ADS1292_REG_CONFIG1, ADS1292_CONFIG1_2000SPS},
    {ADS1292_REG_CONFIG2, ADS1292_CONFIG2_INTREF},
    {ADS1292_REG_LOFF, ADS1292_LOFF_DEFAULT},
    {ADS1292_REG_CH1SET, ADS1292_CHnSET_GAIN12},
    {ADS1292_REG_CH2SET, ADS1292_CH2SET_OFF},
    {ADS1292_REG_RLD_SENS, ADS1292_RLD_SENS_ON},
    {ADS1292_REG_LOFF_SENS, ADS1292_LOFF_SENS_OFF},
    {ADS1292_REG_RESP1, ADS1292_RESP1_NONR},
    {ADS1292_REG_RESP2, ADS1292_RESP2_RLDREF_INT},
};

const unsigned ADS1292_WORN_REG_COUNT =
    (unsigned)(sizeof(ADS1292_WORN_REGS) / sizeof(ADS1292_WORN_REGS[0]));

static void cmd(const Ads1292Bus *bus, uint8_t c) {
    bus->select(1);
    bus->xfer(&c, NULL, 1);
    bus->select(0);
    /* 4 tCLK command decode and 2 tCLK CS-high at 512 kHz. */
    bus->delay_us(12);
}

static void wreg(const Ads1292Bus *bus, uint8_t addr, uint8_t value) {
    uint8_t tx[3];
    tx[0] = (uint8_t)(ADS1292_CMD_WREG | (addr & 0x1fu));
    tx[1] = 0x00u;
    tx[2] = value;
    bus->select(1);
    bus->xfer(tx, NULL, 3);
    bus->select(0);
    bus->delay_us(12);
}

int ads1292_apply_worn_regs(const Ads1292Bus *bus) {
    unsigned i;
    if (bus == NULL || bus->select == NULL || bus->xfer == NULL || bus->delay_us == NULL) {
        return -1;
    }
    if (bus->start_pin != NULL) {
        bus->start_pin(0);
    }
    if (bus->pwdn != NULL) {
        /* R23 holds PWDN/RESET low during the rail ramp. Release only
           when the rail is on; Figure 44 allows 1 s for POR/oscillator. */
        bus->pwdn(1);
        bus->delay_us(1000000);
        /* TI §10.1: RESET after POR. 20 us > 1 tMOD at 128 kHz;
           100 us > 18 tCLK at the slow end of the internal clock. */
        bus->pwdn(0);
        bus->delay_us(20);
        bus->pwdn(1);
        bus->delay_us(100);
    }
    cmd(bus, ADS1292_CMD_SDATAC);
    for (i = 0; i < ADS1292_WORN_REG_COUNT; i++) {
        wreg(bus, ADS1292_WORN_REGS[i].addr, ADS1292_WORN_REGS[i].value);
    }
    /* GPIOC2/GPIOC1 = 1: U2 GPIO2/GPIO1 stay inputs. Board pull-downs
       must be fitted; firmware cannot prevent floating during POR. */
    wreg(bus, ADS1292_REG_GPIO, 0x0cu);
    return 0;
}

int ads1292_start_rdatac(const Ads1292Bus *bus) {
    if (bus == NULL) {
        return -1;
    }
    if (bus->start_pin != NULL) {
        bus->start_pin(1);
    } else {
        cmd(bus, ADS1292_CMD_START);
    }
    cmd(bus, ADS1292_CMD_RDATAC);
    return 0;
}

int ads1292_stop(const Ads1292Bus *bus) {
    if (bus == NULL) {
        return -1;
    }
    cmd(bus, ADS1292_CMD_SDATAC);
    if (bus->start_pin != NULL) {
        bus->start_pin(0);
    } else {
        cmd(bus, ADS1292_CMD_STOP);
    }
    return 0;
}

int ads1292_read_sample(const Ads1292Bus *bus, uint8_t out[ADS1292_SAMPLE_BYTES]) {
    uint8_t tx[ADS1292_SAMPLE_BYTES];
    if (bus == NULL || out == NULL) {
        return -1;
    }
    memset(tx, 0, sizeof(tx));
    bus->select(1);
    bus->xfer(tx, out, ADS1292_SAMPLE_BYTES);
    bus->select(0);
    return 0;
}
