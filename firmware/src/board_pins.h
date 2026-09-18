#ifndef ELICIO_BOARD_PINS_H
#define ELICIO_BOARD_PINS_H

/*
 * Stand-in pin map: Adafruit Feather nRF52840 Express variant
 * (FQBN adafruit:nrf52:feather52840). The WP12 product PCB is not released.
 * These Arduino digital numbers are the Feather header, not the earpiece.
 *
 * SPI MOSI/MISO/SCK use the variant SPI object.
 * Recovery is the Feather DFU switch (D7 / P1.02), which is the Adafruit
 * bootloader's own double-reset / hold-on-reset entry.
 */

#define ELICIO_PIN_ADS_CS 10
#define ELICIO_PIN_ADS_DRDY 6
#define ELICIO_PIN_ADS_PWDN 5
#define ELICIO_PIN_ADS_START 11
#define ELICIO_PIN_LED_STREAM 3 /* LED_RED on the Feather */
#define ELICIO_PIN_RECOVERY 7 /* D7 DFU, bootloader entry */

#endif
