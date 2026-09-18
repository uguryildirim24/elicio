# Pin table for WP12d (no receptacle)

Copied from packing-v2.md §5c on lane/w3 at
`c6bd2fec1e10050b1f9f9261fc9d54086d8ad3cf`:
WP12d pin table — smallest all-64 with no receptacle
(width 22, chord 47.90, two sides, fold neck).

`floor` is a packing region, not a copper side. The parser maps it to top.
P4/P5 use RING_PAD_D5_H2.7. Island holes (Q82): (13.45, 17.70);
(17.95, 17.70). Neck-end strips (Q83): SIG1 10.71 mm, SIG2 21.81 mm.

| ref | side | u | s | rot | courtyard wu × ws | notes |
|---|---|---:|---:|---:|---:|---|
| C1 | top | 10.41 | 18.11 | 0 | 1.82 × 0.92 | passive |
| C2 | top | 19.06 | 30.01 | 90 | 0.92 × 1.82 | passive |
| C3 | top | 19.06 | 32.01 | 90 | 0.92 × 1.82 | passive |
| C4 | top | 13.41 | 13.71 | 0 | 1.82 × 0.92 | passive |
| C5 | top | 15.41 | 13.71 | 0 | 1.82 × 0.92 | passive |
| C6 | bottom | 11.23 | 23.83 | 0 | 2.96 × 1.46 | passive, second side |
| C7 | bottom | 12.03 | 25.43 | 0 | 2.96 × 1.46 | passive, second side |
| C8 | bottom | 12.03 | 27.03 | 0 | 2.96 × 1.46 | passive, second side |
| C9 | bottom | 12.03 | 28.63 | 0 | 2.96 × 1.46 | passive, second side |
| C10 | top | 17.41 | 13.71 | 0 | 1.82 × 0.92 | passive |
| C11 | top | 18.56 | 8.56 | 90 | 0.92 × 1.82 | passive |
| C12 | top | 18.56 | 10.56 | 90 | 0.92 × 1.82 | passive |
| C13 | bottom | 3.46 | 16.76 | 0 | 1.82 × 0.92 | passive, second side |
| C14 | bottom | 10.66 | 18.76 | 0 | 1.82 × 0.92 | passive, second side |
| C15 | bottom | 14.43 | 23.83 | 0 | 2.96 × 1.46 | passive, second side |
| D1 | top | 3.95 | 16.75 | 0 | 2.50 × 1.40 | PESD VBUS |
| D2 | top | 9.63 | 16.92 | 0 | 1.86 × 0.94 | LED |
| J2 | top | 22.40 | 10.93 | 0 | 5.80 × 6.56 | JST-SH |
| J3 | top | 26.11 | 20.31 | 0 | 12.31 × 8.62 | bench header; pins hang off the high-u outline |
| J4 | top | 16.25 | 24.60 | 90 | 4.00 × 7.00 | TC2030 leftover; keep-out is a board no-part zone |
| L1 | top | 6.98 | 16.78 | 0 | 2.96 × 1.46 | 10 µH |
| P1 | floor | 5.90 | 22.00 | 0 | 6.40 × 6.40 | SIG1 ring; Q79 tab carries one Contact trace |
| P2 | floor | 10.40 | 33.10 | 0 | 6.40 × 6.40 | SIG2 ring |
| P3 | floor | 8.50 | 43.00 | 0 | 6.40 × 6.40 | REF ring; REF_end_wall_slot |
| P4 | floor | 0.75 | 44.00 | 0 | 6.40 × 6.40 | CHARGE_VBUS tail pad (Q81); RING_PAD_D5_H2.7 |
| P5 | floor | 21.25 | 44.00 | 0 | 6.40 × 6.40 | CHARGE_GND tail pad (Q81); RING_PAD_D5_H2.7 |
| Q1 | bottom | 4.48 | 27.60 | 0 | 3.86 × 3.40 | SOT-23 |
| Q2 | bottom | 4.48 | 31.20 | 0 | 3.86 × 3.40 | SOT-23 |
| Q3 | bottom | 4.48 | 34.80 | 0 | 3.86 × 3.40 | SOT-23 |
| Q4 | bottom | 8.48 | 27.60 | 0 | 3.86 × 3.40 | SOT-23 |
| Q5 | bottom | 11.68 | 21.20 | 0 | 3.86 × 3.40 | SOT-23 |
| R1 | top | 10.70 | 20.12 | 0 | 1.86 × 0.94 | 220 kΩ variant A: island at tab root |
| R2 | top | 17.87 | 32.03 | 90 | 0.94 × 1.86 | 220 kΩ variant A: island at tab root |
| R3 | top | 17.87 | 30.03 | 90 | 0.94 × 1.86 | 220 kΩ variant A: island at tab root |
| R4 | bottom | 14.68 | 19.97 | 0 | 1.86 × 0.94 | passive, second side |
| R5 | bottom | 14.68 | 21.17 | 0 | 1.86 × 0.94 | passive, second side |
| R6 | bottom | 14.68 | 22.37 | 0 | 1.86 × 0.94 | passive, second side |
| R7 | bottom | 14.68 | 25.17 | 0 | 1.86 × 0.94 | passive, second side |
| R8 | bottom | 14.68 | 26.37 | 0 | 1.86 × 0.94 | passive, second side |
| R9 | bottom | 14.68 | 27.57 | 0 | 1.86 × 0.94 | passive, second side |
| R10 | bottom | 14.68 | 28.77 | 0 | 1.86 × 0.94 | passive, second side |
| R11 | bottom | 15.08 | 29.97 | 0 | 1.86 × 0.94 | passive, second side |
| R12 | bottom | 15.08 | 31.17 | 0 | 1.86 × 0.94 | passive, second side |
| R13 | bottom | 15.08 | 32.37 | 0 | 1.86 × 0.94 | passive, second side |
| R14 | bottom | 15.08 | 33.57 | 0 | 1.86 × 0.94 | passive, second side |
| R15 | bottom | 15.08 | 34.77 | 0 | 1.86 × 0.94 | passive, second side |
| R16 | bottom | 15.08 | 35.97 | 0 | 1.86 × 0.94 | passive, second side |
| R17 | bottom | 16.68 | 19.97 | 0 | 1.86 × 0.94 | passive, second side |
| R18 | bottom | 16.68 | 21.17 | 0 | 1.86 × 0.94 | passive, second side |
| R19 | bottom | 16.68 | 22.37 | 0 | 1.86 × 0.94 | passive, second side |
| R20 | bottom | 16.68 | 25.17 | 0 | 1.86 × 0.94 | passive, second side |
| R21 | bottom | 16.68 | 26.37 | 0 | 1.86 × 0.94 | passive, second side |
| R22 | bottom | 16.68 | 27.57 | 0 | 1.86 × 0.94 | passive, second side |
| R23 | bottom | 16.68 | 28.77 | 0 | 1.86 × 0.94 | passive, second side |
| R24 | bottom | 17.08 | 23.57 | 0 | 1.86 × 0.94 | passive, second side |
| R25 | bottom | 17.08 | 29.97 | 0 | 1.86 × 0.94 | passive, second side |
| R26 | bottom | 17.08 | 31.17 | 0 | 1.86 × 0.94 | passive, second side |
| R27 | bottom | 17.08 | 32.37 | 0 | 1.86 × 0.94 | passive, second side |
| R28 | bottom | 17.08 | 33.57 | 0 | 1.86 × 0.94 | passive, second side |
| R29 | bottom | 17.08 | 34.77 | 0 | 1.86 × 0.94 | passive, second side |
| R30 | bottom | 17.08 | 35.97 | 0 | 1.86 × 0.94 | passive, second side |
| SW1 | top | 16.25 | 4.45 | 0 | 7.50 × 5.60 | lid, pocket island |
| U1 | top | 8.00 | 29.35 | 0 | 11.50 × 16.50 | process pose; courtyard 11.50×16.50 |
| U2 | top | 15.13 | 10.28 | 0 | 5.26 × 5.26 | ADS1292 |
| U3 | top | 15.68 | 30.85 | 0 | 2.96 × 3.50 | BQ25100 |
| U4 | top | 16.65 | 34.80 | 0 | 4.10 × 3.40 | TLV71330 |
