#ifndef ELICIO_BOARD_PINS_H
#define ELICIO_BOARD_PINS_H

/*
 * v4 ISP1807-LR pad -> nRF52840 P0.xx (not Feather digital pin numbers).
 * Source: ISP1807 datasheet R19 §3 pin table, pp. 10-11,
 * https://www.insightsip.com/fichiers_insightsip/pdf/ble/ISP1807/isp_ble_DS1807.pdf
 * read 2026-09-25; net assignments: committed elicio-v4.kicad_sch/pcb.
 * A product Arduino variant must map these physical pins to its digital pins;
 * the Feather SPI object and digital-pin indices are NOT the product variant.
 */
#define ELICIO_PIN_ADS_SCLK 6 /* P0.06, U1.34 AFE_SCLK */
#define ELICIO_PIN_ADS_MOSI 5 /* P0.05, U1.36 AFE_MOSI */
#define ELICIO_PIN_ADS_MISO 8 /* P0.08, U1.32 AFE_MISO */
#define ELICIO_PIN_ADS_CS 28 /* P0.28, U1.48 AFE_CS; LF only */
#define ELICIO_PIN_ADS_DRDY 29 /* P0.29, U1.46 AFE_DRDY; LF only */
#define ELICIO_PIN_ADS_START 10 /* P0.10, U1.4 AFE_START; NFC2 as GPIO */
#define ELICIO_PIN_ADS_PWDN 26 /* P0.26, U1.6 AFE_RESET (ADS PWDN/RESET) */
#define ELICIO_PIN_VBUS_DET 2 /* P0.02, U1.40 VBUS_DET; LF only */
#define ELICIO_PIN_CHG_MON 30 /* P0.30, U1.44 CHG_MON; AIN6, LF only */
#define ELICIO_PIN_VBAT_SENSE 31 /* P0.31, U1.42 VBAT_SENSE; AIN7, LF only */
#define ELICIO_PIN_LED_EN 3 /* P0.03, U1.38 LED_EN; LF only */
#define ELICIO_PIN_NRESET 18 /* P0.18, U1.13 nRESET; configure UICR PSELRESET */

/* U1.28 SWDIO and U1.30 SWDCLK are dedicated debug signals, not GPIO.
 * U1.26 +VDD comes from U5; U1.20/22 RF_ANT, VSS pads 1,7,14,16,18,
 * 21,23,24,25,31. U1.8/10 USB and U1.12 VBUS are not connected.
 * BAT_MEAS_EN / Q5 were removed; AFE_EN_HW is a hardware charge interlock,
 * not MCU GPIO. Charge status is the ADC CHG_MON net (no separate STAT pin).
 */
#endif
