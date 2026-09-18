#ifndef ELICIO_ADS1292_H
#define ELICIO_ADS1292_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Worn-session register set, ADS1292 non-R. TI SBAS502C, read 2026-09-17. */

#define ADS1292_REG_ID 0x00u
#define ADS1292_REG_CONFIG1 0x01u
#define ADS1292_REG_CONFIG2 0x02u
#define ADS1292_REG_LOFF 0x03u
#define ADS1292_REG_CH1SET 0x04u
#define ADS1292_REG_CH2SET 0x05u
#define ADS1292_REG_RLD_SENS 0x06u
#define ADS1292_REG_LOFF_SENS 0x07u
#define ADS1292_REG_LOFF_STAT 0x08u
#define ADS1292_REG_RESP1 0x09u
#define ADS1292_REG_RESP2 0x0au
#define ADS1292_REG_GPIO 0x0bu

/* CONFIG1: continuous, DR[2:0]=100 → 2 kSPS (Table 18). */
#define ADS1292_CONFIG1_2000SPS 0x04u
/* CONFIG2: bit7=1, PDB_REFBUF=1, VREF_4V=0, lead-off comparators off.
   TI example "WREG CONFIG2 A0h" for internal reference. */
#define ADS1292_CONFIG2_INTREF 0xa0u
#define ADS1292_LOFF_DEFAULT 0x10u
/* CH1SET/CH2SET: GAIN=110 (12), MUX=0000 normal electrode. */
#define ADS1292_CHnSET_GAIN12 0x60u
/* RLD_SENS: PDB_RLD=1, RLD1P+RLD1N connected. */
#define ADS1292_RLD_SENS_ON 0x23u
#define ADS1292_LOFF_SENS_OFF 0x00u
/* RESP1 must be 02h on non-R ADS1292 (datasheet §8.6.1.10). */
#define ADS1292_RESP1_NONR 0x02u
/* RESP2 reset: RLDREF_INT=1. */
#define ADS1292_RESP2_RLDREF_INT 0x02u

#define ADS1292_CMD_WAKEUP 0x02u
#define ADS1292_CMD_STANDBY 0x04u
#define ADS1292_CMD_RESET 0x06u
#define ADS1292_CMD_START 0x08u
#define ADS1292_CMD_STOP 0x0au
#define ADS1292_CMD_RDATAC 0x10u
#define ADS1292_CMD_SDATAC 0x11u
#define ADS1292_CMD_RDATA 0x12u
#define ADS1292_CMD_RREG 0x20u
#define ADS1292_CMD_WREG 0x40u

#define ADS1292_SAMPLE_BYTES 9u

typedef struct {
    uint8_t addr;
    uint8_t value;
} Ads1292Reg;

typedef struct {
    void (*select)(int asserted);
    void (*xfer)(const uint8_t *tx, uint8_t *rx, size_t n);
    void (*delay_us)(unsigned us);
    void (*pwdn)(int high);
    void (*start_pin)(int high);
} Ads1292Bus;

extern const Ads1292Reg ADS1292_WORN_REGS[];
extern const unsigned ADS1292_WORN_REG_COUNT;

int ads1292_apply_worn_regs(const Ads1292Bus *bus);
int ads1292_start_rdatac(const Ads1292Bus *bus);
int ads1292_stop(const Ads1292Bus *bus);
int ads1292_read_sample(const Ads1292Bus *bus, uint8_t out[ADS1292_SAMPLE_BYTES]);

#ifdef __cplusplus
}
#endif

#endif
