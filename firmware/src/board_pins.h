#ifndef ELICIO_BOARD_PINS_H
#define ELICIO_BOARD_PINS_H

/*
 * Product GPIO map from docs/fab/board-v2.md §9 (MDBT50Q pin → nRF).
 * Values are nRF P0.n numbers (P0.13 → 13). Read 2026-09-17; same table
 * on lane/w2. The Feather FQBN compile still treats these as Arduino
 * digital numbers. That is not a product wiring claim.
 *
 * SPI MOSI/MISO/SCK are listed here for the map. The stand-in sketch
 * still uses the variant SPI object.
 * Recovery is nRESET (P0.18), the bootloader's own reset path.
 */

#define ELICIO_PIN_ADS_SCLK 8 /* P0.08 */
#define ELICIO_PIN_ADS_MOSI 6 /* P0.06 */
#define ELICIO_PIN_ADS_MISO 15 /* P0.15 */
#define ELICIO_PIN_ADS_CS 13 /* P0.13 */
#define ELICIO_PIN_ADS_DRDY 17 /* P0.17 */
#define ELICIO_PIN_ADS_START 20 /* P0.20 */
#define ELICIO_PIN_ADS_PWDN 22 /* P0.22 */
#define ELICIO_PIN_VBUS_DET 24 /* P0.24 */
#define ELICIO_PIN_CHG_MON 31 /* P0.31 */
#define ELICIO_PIN_VBAT_SENSE 2 /* P0.02 */
#define ELICIO_PIN_BAT_MEAS_EN 3 /* P0.03 */
#define ELICIO_PIN_LED_EN 4 /* P0.04 */
#define ELICIO_PIN_LED_STREAM ELICIO_PIN_LED_EN
#define ELICIO_PIN_NRESET 18 /* P0.18 */
#define ELICIO_PIN_RECOVERY ELICIO_PIN_NRESET

#endif
