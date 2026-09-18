# Packing v2 — which architectures close

WP11 analysis. The plan is not changed. Nothing is ordered.
Architecture C is out (plan v2 turn 02). Interface I is turn 07:
no springs, no pins; board underside on three brass standoff tops;
8 × 8 gold pad per site; bosses 0.5 lower than the standoff tops;
cell under the board on the floor. Interface II is the flex-tab fallback.
Arc-plus was not run: layouts already close at BODY_ARC 48.4.

## 1. Every run at BODY_ARC 48.4

| arch | iface | standoff | cell | layout | width | lid | closes | first conflict | free mm² | TOTAL_CHORD | M1 gate |
|---|---|---:|---|---|---:|---:|---|---|---:|---:|---:|
| A | I | 3 | dtp | series | 18 | 6 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | series | 18 | 6 | no | cell hits SIG1 standoff (circumradius 2.9) | 358.1 | 47.90 | 50.90 |
| A | II | 3 | dtp | series | 18 | 6 | no | module top 6.70 > LID_Y 6 | 89.8 | 47.90 | 50.90 |
| A | I | 3 | dtp | series | 18 | 6.5 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | series | 18 | 6.5 | no | cell hits SIG1 standoff (circumradius 2.9) | 358.1 | 47.90 | 50.90 |
| A | II | 3 | dtp | series | 18 | 6.5 | no | module top 6.70 > LID_Y 6.5 | 89.8 | 47.90 | 50.90 |
| A | I | 3 | dtp | series | 18 | 7 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | series | 18 | 7 | no | cell hits SIG1 standoff (circumradius 2.9) | 358.1 | 47.90 | 50.90 |
| A | II | 3 | dtp | series | 18 | 7 | no | JST_SH top 7.30 > LID_Y 7 | 89.8 | 47.90 | 50.90 |
| A | I | 3 | dtp | series | 18 | 8 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | series | 18 | 8 | no | cell hits SIG1 standoff (circumradius 2.9) | 358.1 | 47.90 | 50.90 |
| A | II | 3 | dtp | series | 18 | 8 | no | module 10.50×15.50 at (7.50,29.85) outside the board | 89.8 | 47.90 | 50.90 |
| A | I | 3 | dtp | series | 18 | 8.5 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | series | 18 | 8.5 | no | cell hits SIG1 standoff (circumradius 2.9) | 358.1 | 47.90 | 50.90 |
| A | II | 3 | dtp | series | 18 | 8.5 | no | module 10.50×15.50 at (7.50,29.85) outside the board | 89.8 | 47.90 | 50.90 |
| A | I | 3 | dtp | series | 18 | 9 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | series | 18 | 9 | no | cell hits SIG1 standoff (circumradius 2.9) | 358.1 | 47.90 | 50.90 |
| A | II | 3 | dtp | series | 18 | 9 | no | module 10.50×15.50 at (7.50,29.85) outside the board | 89.8 | 47.90 | 50.90 |
| A | I | 3 | dtp | series | 19 | 6 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | series | 19 | 6 | no | cell hits SIG1 standoff (circumradius 2.9) | 394.1 | 47.90 | 50.90 |
| A | II | 3 | dtp | series | 19 | 6 | no | module top 6.70 > LID_Y 6 | 102.3 | 47.90 | 50.90 |
| A | I | 3 | dtp | series | 19 | 6.5 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | series | 19 | 6.5 | no | cell hits SIG1 standoff (circumradius 2.9) | 394.1 | 47.90 | 50.90 |
| A | II | 3 | dtp | series | 19 | 6.5 | no | module top 6.70 > LID_Y 6.5 | 102.3 | 47.90 | 50.90 |
| A | I | 3 | dtp | series | 19 | 7 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | series | 19 | 7 | no | cell hits SIG1 standoff (circumradius 2.9) | 394.1 | 47.90 | 50.90 |
| A | II | 3 | dtp | series | 19 | 7 | no | JST_SH top 7.30 > LID_Y 7 | 102.3 | 47.90 | 50.90 |
| A | I | 3 | dtp | series | 19 | 8 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | series | 19 | 8 | no | cell hits SIG1 standoff (circumradius 2.9) | 394.1 | 47.90 | 50.90 |
| A | II | 3 | dtp | series | 19 | 8 | no | module 10.50×15.50 at (7.50,29.85) outside the board | 102.3 | 47.90 | 50.90 |
| A | I | 3 | dtp | series | 19 | 8.5 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | series | 19 | 8.5 | no | cell hits SIG1 standoff (circumradius 2.9) | 394.1 | 47.90 | 50.90 |
| A | II | 3 | dtp | series | 19 | 8.5 | no | module 10.50×15.50 at (7.50,29.85) outside the board | 102.3 | 47.90 | 50.90 |
| A | I | 3 | dtp | series | 19 | 9 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | series | 19 | 9 | no | cell hits SIG1 standoff (circumradius 2.9) | 394.1 | 47.90 | 50.90 |
| A | II | 3 | dtp | series | 19 | 9 | no | module 10.50×15.50 at (7.50,29.85) outside the board | 102.3 | 47.90 | 50.90 |
| A | I | 3 | dtp | series | 20 | 6 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | series | 20 | 6 | no | cell hits SIG1 standoff (circumradius 2.9) | 426.9 | 47.90 | 50.90 |
| A | II | 3 | dtp | series | 20 | 6 | no | module top 6.70 > LID_Y 6 | 111.8 | 47.90 | 50.90 |
| A | I | 3 | dtp | series | 20 | 6.5 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | series | 20 | 6.5 | no | cell hits SIG1 standoff (circumradius 2.9) | 426.9 | 47.90 | 50.90 |
| A | II | 3 | dtp | series | 20 | 6.5 | no | module top 6.70 > LID_Y 6.5 | 111.8 | 47.90 | 50.90 |
| A | I | 3 | dtp | series | 20 | 7 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | series | 20 | 7 | no | cell hits SIG1 standoff (circumradius 2.9) | 426.9 | 47.90 | 50.90 |
| A | II | 3 | dtp | series | 20 | 7 | no | module overlaps ADS1292_RSM | 111.8 | 47.90 | 50.90 |
| A | I | 3 | dtp | series | 20 | 8 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | series | 20 | 8 | no | cell hits SIG1 standoff (circumradius 2.9) | 426.9 | 47.90 | 50.90 |
| A | II | 3 | dtp | series | 20 | 8 | no | module overlaps ADS1292_RSM | 111.8 | 47.90 | 50.90 |
| A | I | 3 | dtp | series | 20 | 8.5 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | series | 20 | 8.5 | no | cell hits SIG1 standoff (circumradius 2.9) | 426.9 | 47.90 | 50.90 |
| A | II | 3 | dtp | series | 20 | 8.5 | no | module overlaps ADS1292_RSM | 111.8 | 47.90 | 50.90 |
| A | I | 3 | dtp | series | 20 | 9 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | series | 20 | 9 | no | cell hits SIG1 standoff (circumradius 2.9) | 426.9 | 47.90 | 50.90 |
| A | II | 3 | dtp | series | 20 | 9 | no | module overlaps ADS1292_RSM | 111.8 | 47.90 | 50.90 |
| A | I | 3 | dtp | stacked | 18 | 6 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | stacked | 18 | 6 | no | cell hits SIG1 standoff (circumradius 2.9) | 337.6 | 47.90 | 50.90 |
| A | II | 3 | dtp | stacked | 18 | 6 | no | cell top 7.70 > LID_Y 6 | 337.6 | 47.90 | 50.90 |
| A | I | 3 | dtp | stacked | 18 | 6.5 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | stacked | 18 | 6.5 | no | cell hits SIG1 standoff (circumradius 2.9) | 337.6 | 47.90 | 50.90 |
| A | II | 3 | dtp | stacked | 18 | 6.5 | no | cell top 7.70 > LID_Y 6.5 | 337.6 | 47.90 | 50.90 |
| A | I | 3 | dtp | stacked | 18 | 7 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | stacked | 18 | 7 | no | cell hits SIG1 standoff (circumradius 2.9) | 337.6 | 47.90 | 50.90 |
| A | II | 3 | dtp | stacked | 18 | 7 | no | cell top 7.70 > LID_Y 7 | 337.6 | 47.90 | 50.90 |
| A | I | 3 | dtp | stacked | 18 | 8 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | stacked | 18 | 8 | no | cell hits SIG1 standoff (circumradius 2.9) | 337.6 | 47.90 | 50.90 |
| A | II | 3 | dtp | stacked | 18 | 8 | no | JST_SH enters SIG1 keep-out + 0.5 | 337.6 | 47.90 | 50.90 |
| A | I | 3 | dtp | stacked | 18 | 8.5 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | stacked | 18 | 8.5 | no | cell hits SIG1 standoff (circumradius 2.9) | 337.6 | 47.90 | 50.90 |
| A | II | 3 | dtp | stacked | 18 | 8.5 | no | JST_SH enters SIG1 keep-out + 0.5 | 337.6 | 47.90 | 50.90 |
| A | I | 3 | dtp | stacked | 18 | 9 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | stacked | 18 | 9 | no | cell hits SIG1 standoff (circumradius 2.9) | 337.6 | 47.90 | 50.90 |
| A | II | 3 | dtp | stacked | 18 | 9 | no | JST_SH enters SIG1 keep-out + 0.5 | 337.6 | 47.90 | 50.90 |
| A | I | 3 | dtp | stacked | 19 | 6 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | stacked | 19 | 6 | no | cell hits SIG1 standoff (circumradius 2.9) | 373.6 | 47.90 | 50.90 |
| A | II | 3 | dtp | stacked | 19 | 6 | no | cell top 7.70 > LID_Y 6 | 373.6 | 47.90 | 50.90 |
| A | I | 3 | dtp | stacked | 19 | 6.5 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | stacked | 19 | 6.5 | no | cell hits SIG1 standoff (circumradius 2.9) | 373.6 | 47.90 | 50.90 |
| A | II | 3 | dtp | stacked | 19 | 6.5 | no | cell top 7.70 > LID_Y 6.5 | 373.6 | 47.90 | 50.90 |
| A | I | 3 | dtp | stacked | 19 | 7 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | stacked | 19 | 7 | no | cell hits SIG1 standoff (circumradius 2.9) | 373.6 | 47.90 | 50.90 |
| A | II | 3 | dtp | stacked | 19 | 7 | no | cell top 7.70 > LID_Y 7 | 373.6 | 47.90 | 50.90 |
| A | I | 3 | dtp | stacked | 19 | 8 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | stacked | 19 | 8 | no | cell hits SIG1 standoff (circumradius 2.9) | 373.6 | 47.90 | 50.90 |
| A | II | 3 | dtp | stacked | 19 | 8 | no | JST_SH enters SIG1 keep-out + 0.5 | 373.6 | 47.90 | 50.90 |
| A | I | 3 | dtp | stacked | 19 | 8.5 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | stacked | 19 | 8.5 | no | cell hits SIG1 standoff (circumradius 2.9) | 373.6 | 47.90 | 50.90 |
| A | II | 3 | dtp | stacked | 19 | 8.5 | no | JST_SH enters SIG1 keep-out + 0.5 | 373.6 | 47.90 | 50.90 |
| A | I | 3 | dtp | stacked | 19 | 9 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | stacked | 19 | 9 | no | cell hits SIG1 standoff (circumradius 2.9) | 373.6 | 47.90 | 50.90 |
| A | II | 3 | dtp | stacked | 19 | 9 | no | JST_SH enters SIG1 keep-out + 0.5 | 373.6 | 47.90 | 50.90 |
| A | I | 3 | dtp | stacked | 20 | 6 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | stacked | 20 | 6 | no | cell hits SIG1 standoff (circumradius 2.9) | 405.6 | 47.90 | 50.90 |
| A | II | 3 | dtp | stacked | 20 | 6 | no | cell top 7.70 > LID_Y 6 | 405.6 | 47.90 | 50.90 |
| A | I | 3 | dtp | stacked | 20 | 6.5 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | stacked | 20 | 6.5 | no | cell hits SIG1 standoff (circumradius 2.9) | 405.6 | 47.90 | 50.90 |
| A | II | 3 | dtp | stacked | 20 | 6.5 | no | cell top 7.70 > LID_Y 6.5 | 405.6 | 47.90 | 50.90 |
| A | I | 3 | dtp | stacked | 20 | 7 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | stacked | 20 | 7 | no | cell hits SIG1 standoff (circumradius 2.9) | 405.6 | 47.90 | 50.90 |
| A | II | 3 | dtp | stacked | 20 | 7 | no | cell top 7.70 > LID_Y 7 | 405.6 | 47.90 | 50.90 |
| A | I | 3 | dtp | stacked | 20 | 8 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | stacked | 20 | 8 | no | cell hits SIG1 standoff (circumradius 2.9) | 405.6 | 47.90 | 50.90 |
| A | II | 3 | dtp | stacked | 20 | 8 | no | JST_SH enters SIG1 keep-out + 0.5 | 405.6 | 47.90 | 50.90 |
| A | I | 3 | dtp | stacked | 20 | 8.5 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | stacked | 20 | 8.5 | no | cell hits SIG1 standoff (circumradius 2.9) | 405.6 | 47.90 | 50.90 |
| A | II | 3 | dtp | stacked | 20 | 8.5 | no | JST_SH enters SIG1 keep-out + 0.5 | 405.6 | 47.90 | 50.90 |
| A | I | 3 | dtp | stacked | 20 | 9 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | dtp | stacked | 20 | 9 | no | cell hits SIG1 standoff (circumradius 2.9) | 405.6 | 47.90 | 50.90 |
| A | II | 3 | dtp | stacked | 20 | 9 | no | JST_SH enters SIG1 keep-out + 0.5 | 405.6 | 47.90 | 50.90 |
| A | I | 3 | 501015 | series | 18 | 6 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | series | 18 | 6 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 358.1 | 47.90 | 50.90 |
| A | II | 3 | 501015 | series | 18 | 6 | no | module top 6.70 > LID_Y 6 | 132.1 | 47.90 | 50.90 |
| A | I | 3 | 501015 | series | 18 | 6.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | series | 18 | 6.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 358.1 | 47.90 | 50.90 |
| A | II | 3 | 501015 | series | 18 | 6.5 | no | module top 6.70 > LID_Y 6.5 | 132.1 | 47.90 | 50.90 |
| A | I | 3 | 501015 | series | 18 | 7 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | series | 18 | 7 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 358.1 | 47.90 | 50.90 |
| A | II | 3 | 501015 | series | 18 | 7 | no | JST_SH top 7.30 > LID_Y 7 | 132.1 | 47.90 | 50.90 |
| A | I | 3 | 501015 | series | 18 | 8 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | series | 18 | 8 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 358.1 | 47.90 | 50.90 |
| A | II | 3 | 501015 | series | 18 | 8 | no | SWD_4 in the antenna keep-out | 132.1 | 47.90 | 50.90 |
| A | I | 3 | 501015 | series | 18 | 8.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | series | 18 | 8.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 358.1 | 47.90 | 50.90 |
| A | II | 3 | 501015 | series | 18 | 8.5 | no | SWD_4 in the antenna keep-out | 132.1 | 47.90 | 50.90 |
| A | I | 3 | 501015 | series | 18 | 9 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | series | 18 | 9 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 358.1 | 47.90 | 50.90 |
| A | II | 3 | 501015 | series | 18 | 9 | no | SWD_4 in the antenna keep-out | 132.1 | 47.90 | 50.90 |
| A | I | 3 | 501015 | series | 19 | 6 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | series | 19 | 6 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 394.1 | 47.90 | 50.90 |
| A | II | 3 | 501015 | series | 19 | 6 | no | module top 6.70 > LID_Y 6 | 151.1 | 47.90 | 50.90 |
| A | I | 3 | 501015 | series | 19 | 6.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | series | 19 | 6.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 394.1 | 47.90 | 50.90 |
| A | II | 3 | 501015 | series | 19 | 6.5 | no | module top 6.70 > LID_Y 6.5 | 151.1 | 47.90 | 50.90 |
| A | I | 3 | 501015 | series | 19 | 7 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | series | 19 | 7 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 394.1 | 47.90 | 50.90 |
| A | II | 3 | 501015 | series | 19 | 7 | no | module overlaps ADS1292_RSM | 151.1 | 47.90 | 50.90 |
| A | I | 3 | 501015 | series | 19 | 8 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | series | 19 | 8 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 394.1 | 47.90 | 50.90 |
| A | II | 3 | 501015 | series | 19 | 8 | no | module overlaps ADS1292_RSM | 151.1 | 47.90 | 50.90 |
| A | I | 3 | 501015 | series | 19 | 8.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | series | 19 | 8.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 394.1 | 47.90 | 50.90 |
| A | II | 3 | 501015 | series | 19 | 8.5 | no | module overlaps ADS1292_RSM | 151.1 | 47.90 | 50.90 |
| A | I | 3 | 501015 | series | 19 | 9 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | series | 19 | 9 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 394.1 | 47.90 | 50.90 |
| A | II | 3 | 501015 | series | 19 | 9 | no | module overlaps ADS1292_RSM | 151.1 | 47.90 | 50.90 |
| A | I | 3 | 501015 | series | 20 | 6 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | series | 20 | 6 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 426.9 | 47.90 | 50.90 |
| A | II | 3 | 501015 | series | 20 | 6 | no | module top 6.70 > LID_Y 6 | 166.8 | 47.90 | 50.90 |
| A | I | 3 | 501015 | series | 20 | 6.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | series | 20 | 6.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 426.9 | 47.90 | 50.90 |
| A | II | 3 | 501015 | series | 20 | 6.5 | no | module top 6.70 > LID_Y 6.5 | 166.8 | 47.90 | 50.90 |
| A | I | 3 | 501015 | series | 20 | 7 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | series | 20 | 7 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 426.9 | 47.90 | 50.90 |
| A | II | 3 | 501015 | series | 20 | 7 | yes | — | 166.8 | 47.90 | 50.90 |
| A | I | 3 | 501015 | series | 20 | 8 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | series | 20 | 8 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 426.9 | 47.90 | 50.90 |
| A | II | 3 | 501015 | series | 20 | 8 | yes | — | 166.8 | 47.90 | 50.90 |
| A | I | 3 | 501015 | series | 20 | 8.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | series | 20 | 8.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 426.9 | 47.90 | 50.90 |
| A | II | 3 | 501015 | series | 20 | 8.5 | yes | — | 166.8 | 47.90 | 50.90 |
| A | I | 3 | 501015 | series | 20 | 9 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | series | 20 | 9 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 426.9 | 47.90 | 50.90 |
| A | II | 3 | 501015 | series | 20 | 9 | yes | — | 166.8 | 47.90 | 50.90 |
| A | I | 3 | 501015 | stacked | 18 | 6 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | stacked | 18 | 6 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 337.6 | 47.90 | 50.90 |
| A | II | 3 | 501015 | stacked | 18 | 6 | no | cell top 9.70 > LID_Y 6 | 337.6 | 47.90 | 50.90 |
| A | I | 3 | 501015 | stacked | 18 | 6.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | stacked | 18 | 6.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 337.6 | 47.90 | 50.90 |
| A | II | 3 | 501015 | stacked | 18 | 6.5 | no | cell top 9.70 > LID_Y 6.5 | 337.6 | 47.90 | 50.90 |
| A | I | 3 | 501015 | stacked | 18 | 7 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | stacked | 18 | 7 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 337.6 | 47.90 | 50.90 |
| A | II | 3 | 501015 | stacked | 18 | 7 | no | cell top 9.70 > LID_Y 7 | 337.6 | 47.90 | 50.90 |
| A | I | 3 | 501015 | stacked | 18 | 8 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | stacked | 18 | 8 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 337.6 | 47.90 | 50.90 |
| A | II | 3 | 501015 | stacked | 18 | 8 | no | cell top 9.70 > LID_Y 8 | 337.6 | 47.90 | 50.90 |
| A | I | 3 | 501015 | stacked | 18 | 8.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | stacked | 18 | 8.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 337.6 | 47.90 | 50.90 |
| A | II | 3 | 501015 | stacked | 18 | 8.5 | no | cell top 9.70 > LID_Y 8.5 | 337.6 | 47.90 | 50.90 |
| A | I | 3 | 501015 | stacked | 18 | 9 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | stacked | 18 | 9 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 337.6 | 47.90 | 50.90 |
| A | II | 3 | 501015 | stacked | 18 | 9 | no | cell top 9.70 > LID_Y 9 | 337.6 | 47.90 | 50.90 |
| A | I | 3 | 501015 | stacked | 19 | 6 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | stacked | 19 | 6 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 373.6 | 47.90 | 50.90 |
| A | II | 3 | 501015 | stacked | 19 | 6 | no | cell top 9.70 > LID_Y 6 | 373.6 | 47.90 | 50.90 |
| A | I | 3 | 501015 | stacked | 19 | 6.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | stacked | 19 | 6.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 373.6 | 47.90 | 50.90 |
| A | II | 3 | 501015 | stacked | 19 | 6.5 | no | cell top 9.70 > LID_Y 6.5 | 373.6 | 47.90 | 50.90 |
| A | I | 3 | 501015 | stacked | 19 | 7 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | stacked | 19 | 7 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 373.6 | 47.90 | 50.90 |
| A | II | 3 | 501015 | stacked | 19 | 7 | no | cell top 9.70 > LID_Y 7 | 373.6 | 47.90 | 50.90 |
| A | I | 3 | 501015 | stacked | 19 | 8 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | stacked | 19 | 8 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 373.6 | 47.90 | 50.90 |
| A | II | 3 | 501015 | stacked | 19 | 8 | no | cell top 9.70 > LID_Y 8 | 373.6 | 47.90 | 50.90 |
| A | I | 3 | 501015 | stacked | 19 | 8.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | stacked | 19 | 8.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 373.6 | 47.90 | 50.90 |
| A | II | 3 | 501015 | stacked | 19 | 8.5 | no | cell top 9.70 > LID_Y 8.5 | 373.6 | 47.90 | 50.90 |
| A | I | 3 | 501015 | stacked | 19 | 9 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | stacked | 19 | 9 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 373.6 | 47.90 | 50.90 |
| A | II | 3 | 501015 | stacked | 19 | 9 | no | cell top 9.70 > LID_Y 9 | 373.6 | 47.90 | 50.90 |
| A | I | 3 | 501015 | stacked | 20 | 6 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | stacked | 20 | 6 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 405.6 | 47.90 | 50.90 |
| A | II | 3 | 501015 | stacked | 20 | 6 | no | cell top 9.70 > LID_Y 6 | 405.6 | 47.90 | 50.90 |
| A | I | 3 | 501015 | stacked | 20 | 6.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | stacked | 20 | 6.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 405.6 | 47.90 | 50.90 |
| A | II | 3 | 501015 | stacked | 20 | 6.5 | no | cell top 9.70 > LID_Y 6.5 | 405.6 | 47.90 | 50.90 |
| A | I | 3 | 501015 | stacked | 20 | 7 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | stacked | 20 | 7 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 405.6 | 47.90 | 50.90 |
| A | II | 3 | 501015 | stacked | 20 | 7 | no | cell top 9.70 > LID_Y 7 | 405.6 | 47.90 | 50.90 |
| A | I | 3 | 501015 | stacked | 20 | 8 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | stacked | 20 | 8 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 405.6 | 47.90 | 50.90 |
| A | II | 3 | 501015 | stacked | 20 | 8 | no | cell top 9.70 > LID_Y 8 | 405.6 | 47.90 | 50.90 |
| A | I | 3 | 501015 | stacked | 20 | 8.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | stacked | 20 | 8.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 405.6 | 47.90 | 50.90 |
| A | II | 3 | 501015 | stacked | 20 | 8.5 | no | cell top 9.70 > LID_Y 8.5 | 405.6 | 47.90 | 50.90 |
| A | I | 3 | 501015 | stacked | 20 | 9 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 501015 | stacked | 20 | 9 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 405.6 | 47.90 | 50.90 |
| A | II | 3 | 501015 | stacked | 20 | 9 | no | cell top 9.70 > LID_Y 9 | 405.6 | 47.90 | 50.90 |
| B | I | 3 | dtp | series | 18 | 6 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | series | 18 | 6 | no | cell hits SIG1 standoff (circumradius 2.9) | 354.9 | 47.90 | 50.90 |
| B | II | 3 | dtp | series | 18 | 6 | no | module top 6.40 > LID_Y 6 | 86.8 | 47.90 | 50.90 |
| B | I | 3 | dtp | series | 18 | 6.5 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | series | 18 | 6.5 | no | cell hits SIG1 standoff (circumradius 2.9) | 354.9 | 47.90 | 50.90 |
| B | II | 3 | dtp | series | 18 | 6.5 | no | JST_SH top 7.30 > LID_Y 6.5 | 86.8 | 47.90 | 50.90 |
| B | I | 3 | dtp | series | 18 | 7 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | series | 18 | 7 | no | cell hits SIG1 standoff (circumradius 2.9) | 354.9 | 47.90 | 50.90 |
| B | II | 3 | dtp | series | 18 | 7 | no | JST_SH top 7.30 > LID_Y 7 | 86.8 | 47.90 | 50.90 |
| B | I | 3 | dtp | series | 18 | 8 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | series | 18 | 8 | no | cell hits SIG1 standoff (circumradius 2.9) | 354.9 | 47.90 | 50.90 |
| B | II | 3 | dtp | series | 18 | 8 | no | module 13.00×18.00 at (9.00,28.60) outside the board | 86.8 | 47.90 | 50.90 |
| B | I | 3 | dtp | series | 18 | 8.5 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | series | 18 | 8.5 | no | cell hits SIG1 standoff (circumradius 2.9) | 354.9 | 47.90 | 50.90 |
| B | II | 3 | dtp | series | 18 | 8.5 | no | module 13.00×18.00 at (9.00,28.60) outside the board | 86.8 | 47.90 | 50.90 |
| B | I | 3 | dtp | series | 18 | 9 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | series | 18 | 9 | no | cell hits SIG1 standoff (circumradius 2.9) | 354.9 | 47.90 | 50.90 |
| B | II | 3 | dtp | series | 18 | 9 | no | module 13.00×18.00 at (9.00,28.60) outside the board | 86.8 | 47.90 | 50.90 |
| B | I | 3 | dtp | series | 19 | 6 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | series | 19 | 6 | no | cell hits SIG1 standoff (circumradius 2.9) | 390.9 | 47.90 | 50.90 |
| B | II | 3 | dtp | series | 19 | 6 | no | module top 6.40 > LID_Y 6 | 99.2 | 47.90 | 50.90 |
| B | I | 3 | dtp | series | 19 | 6.5 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | series | 19 | 6.5 | no | cell hits SIG1 standoff (circumradius 2.9) | 390.9 | 47.90 | 50.90 |
| B | II | 3 | dtp | series | 19 | 6.5 | no | JST_SH top 7.30 > LID_Y 6.5 | 99.2 | 47.90 | 50.90 |
| B | I | 3 | dtp | series | 19 | 7 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | series | 19 | 7 | no | cell hits SIG1 standoff (circumradius 2.9) | 390.9 | 47.90 | 50.90 |
| B | II | 3 | dtp | series | 19 | 7 | no | JST_SH top 7.30 > LID_Y 7 | 99.2 | 47.90 | 50.90 |
| B | I | 3 | dtp | series | 19 | 8 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | series | 19 | 8 | no | cell hits SIG1 standoff (circumradius 2.9) | 390.9 | 47.90 | 50.90 |
| B | II | 3 | dtp | series | 19 | 8 | no | module 13.00×18.00 at (9.50,28.60) outside the board | 99.2 | 47.90 | 50.90 |
| B | I | 3 | dtp | series | 19 | 8.5 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | series | 19 | 8.5 | no | cell hits SIG1 standoff (circumradius 2.9) | 390.9 | 47.90 | 50.90 |
| B | II | 3 | dtp | series | 19 | 8.5 | no | module 13.00×18.00 at (9.50,28.60) outside the board | 99.2 | 47.90 | 50.90 |
| B | I | 3 | dtp | series | 19 | 9 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | series | 19 | 9 | no | cell hits SIG1 standoff (circumradius 2.9) | 390.9 | 47.90 | 50.90 |
| B | II | 3 | dtp | series | 19 | 9 | no | module 13.00×18.00 at (9.50,28.60) outside the board | 99.2 | 47.90 | 50.90 |
| B | I | 3 | dtp | series | 20 | 6 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | series | 20 | 6 | no | cell hits SIG1 standoff (circumradius 2.9) | 426.9 | 47.90 | 50.90 |
| B | II | 3 | dtp | series | 20 | 6 | no | module top 6.40 > LID_Y 6 | 111.8 | 47.90 | 50.90 |
| B | I | 3 | dtp | series | 20 | 6.5 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | series | 20 | 6.5 | no | cell hits SIG1 standoff (circumradius 2.9) | 426.9 | 47.90 | 50.90 |
| B | II | 3 | dtp | series | 20 | 6.5 | no | header top 6.90 > LID_Y 6.5 | 111.8 | 47.90 | 50.90 |
| B | I | 3 | dtp | series | 20 | 7 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | series | 20 | 7 | no | cell hits SIG1 standoff (circumradius 2.9) | 426.9 | 47.90 | 50.90 |
| B | II | 3 | dtp | series | 20 | 7 | no | module 13.00×18.00 at (8.75,28.60) outside the board | 111.8 | 47.90 | 50.90 |
| B | I | 3 | dtp | series | 20 | 8 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | series | 20 | 8 | no | cell hits SIG1 standoff (circumradius 2.9) | 426.9 | 47.90 | 50.90 |
| B | II | 3 | dtp | series | 20 | 8 | no | module 13.00×18.00 at (8.75,28.60) outside the board | 111.8 | 47.90 | 50.90 |
| B | I | 3 | dtp | series | 20 | 8.5 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | series | 20 | 8.5 | no | cell hits SIG1 standoff (circumradius 2.9) | 426.9 | 47.90 | 50.90 |
| B | II | 3 | dtp | series | 20 | 8.5 | no | module 13.00×18.00 at (8.75,28.60) outside the board | 111.8 | 47.90 | 50.90 |
| B | I | 3 | dtp | series | 20 | 9 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | series | 20 | 9 | no | cell hits SIG1 standoff (circumradius 2.9) | 426.9 | 47.90 | 50.90 |
| B | II | 3 | dtp | series | 20 | 9 | no | module 13.00×18.00 at (8.75,28.60) outside the board | 111.8 | 47.90 | 50.90 |
| B | I | 3 | dtp | stacked | 18 | 6 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | stacked | 18 | 6 | no | cell hits SIG1 standoff (circumradius 2.9) | 345.8 | 47.90 | 50.90 |
| B | II | 3 | dtp | stacked | 18 | 6 | no | cell top 7.63 > LID_Y 6 | 345.8 | 47.90 | 50.90 |
| B | I | 3 | dtp | stacked | 18 | 6.5 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | stacked | 18 | 6.5 | no | cell hits SIG1 standoff (circumradius 2.9) | 345.8 | 47.90 | 50.90 |
| B | II | 3 | dtp | stacked | 18 | 6.5 | no | cell top 7.63 > LID_Y 6.5 | 345.8 | 47.90 | 50.90 |
| B | I | 3 | dtp | stacked | 18 | 7 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | stacked | 18 | 7 | no | cell hits SIG1 standoff (circumradius 2.9) | 345.8 | 47.90 | 50.90 |
| B | II | 3 | dtp | stacked | 18 | 7 | no | cell top 7.63 > LID_Y 7 | 345.8 | 47.90 | 50.90 |
| B | I | 3 | dtp | stacked | 18 | 8 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | stacked | 18 | 8 | no | cell hits SIG1 standoff (circumradius 2.9) | 345.8 | 47.90 | 50.90 |
| B | II | 3 | dtp | stacked | 18 | 8 | no | module enters SIG1 keep-out + 0.5 | 345.8 | 47.90 | 50.90 |
| B | I | 3 | dtp | stacked | 18 | 8.5 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | stacked | 18 | 8.5 | no | cell hits SIG1 standoff (circumradius 2.9) | 345.8 | 47.90 | 50.90 |
| B | II | 3 | dtp | stacked | 18 | 8.5 | no | module enters SIG1 keep-out + 0.5 | 345.8 | 47.90 | 50.90 |
| B | I | 3 | dtp | stacked | 18 | 9 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | stacked | 18 | 9 | no | cell hits SIG1 standoff (circumradius 2.9) | 345.8 | 47.90 | 50.90 |
| B | II | 3 | dtp | stacked | 18 | 9 | no | module enters SIG1 keep-out + 0.5 | 345.8 | 47.90 | 50.90 |
| B | I | 3 | dtp | stacked | 19 | 6 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | stacked | 19 | 6 | no | cell hits SIG1 standoff (circumradius 2.9) | 381.2 | 47.90 | 50.90 |
| B | II | 3 | dtp | stacked | 19 | 6 | no | cell top 7.63 > LID_Y 6 | 381.2 | 47.90 | 50.90 |
| B | I | 3 | dtp | stacked | 19 | 6.5 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | stacked | 19 | 6.5 | no | cell hits SIG1 standoff (circumradius 2.9) | 381.2 | 47.90 | 50.90 |
| B | II | 3 | dtp | stacked | 19 | 6.5 | no | cell top 7.63 > LID_Y 6.5 | 381.2 | 47.90 | 50.90 |
| B | I | 3 | dtp | stacked | 19 | 7 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | stacked | 19 | 7 | no | cell hits SIG1 standoff (circumradius 2.9) | 381.2 | 47.90 | 50.90 |
| B | II | 3 | dtp | stacked | 19 | 7 | no | cell top 7.63 > LID_Y 7 | 381.2 | 47.90 | 50.90 |
| B | I | 3 | dtp | stacked | 19 | 8 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | stacked | 19 | 8 | no | cell hits SIG1 standoff (circumradius 2.9) | 381.2 | 47.90 | 50.90 |
| B | II | 3 | dtp | stacked | 19 | 8 | no | module enters SIG1 keep-out + 0.5 | 381.2 | 47.90 | 50.90 |
| B | I | 3 | dtp | stacked | 19 | 8.5 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | stacked | 19 | 8.5 | no | cell hits SIG1 standoff (circumradius 2.9) | 381.2 | 47.90 | 50.90 |
| B | II | 3 | dtp | stacked | 19 | 8.5 | no | module enters SIG1 keep-out + 0.5 | 381.2 | 47.90 | 50.90 |
| B | I | 3 | dtp | stacked | 19 | 9 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | stacked | 19 | 9 | no | cell hits SIG1 standoff (circumradius 2.9) | 381.2 | 47.90 | 50.90 |
| B | II | 3 | dtp | stacked | 19 | 9 | no | module enters SIG1 keep-out + 0.5 | 381.2 | 47.90 | 50.90 |
| B | I | 3 | dtp | stacked | 20 | 6 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | stacked | 20 | 6 | no | cell hits SIG1 standoff (circumradius 2.9) | 417.9 | 47.90 | 50.90 |
| B | II | 3 | dtp | stacked | 20 | 6 | no | cell top 7.63 > LID_Y 6 | 417.9 | 47.90 | 50.90 |
| B | I | 3 | dtp | stacked | 20 | 6.5 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | stacked | 20 | 6.5 | no | cell hits SIG1 standoff (circumradius 2.9) | 417.9 | 47.90 | 50.90 |
| B | II | 3 | dtp | stacked | 20 | 6.5 | no | cell top 7.63 > LID_Y 6.5 | 417.9 | 47.90 | 50.90 |
| B | I | 3 | dtp | stacked | 20 | 7 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | stacked | 20 | 7 | no | cell hits SIG1 standoff (circumradius 2.9) | 417.9 | 47.90 | 50.90 |
| B | II | 3 | dtp | stacked | 20 | 7 | no | cell top 7.63 > LID_Y 7 | 417.9 | 47.90 | 50.90 |
| B | I | 3 | dtp | stacked | 20 | 8 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | stacked | 20 | 8 | no | cell hits SIG1 standoff (circumradius 2.9) | 417.9 | 47.90 | 50.90 |
| B | II | 3 | dtp | stacked | 20 | 8 | no | module enters SIG1 keep-out + 0.5 | 417.9 | 47.90 | 50.90 |
| B | I | 3 | dtp | stacked | 20 | 8.5 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | stacked | 20 | 8.5 | no | cell hits SIG1 standoff (circumradius 2.9) | 417.9 | 47.90 | 50.90 |
| B | II | 3 | dtp | stacked | 20 | 8.5 | no | module enters SIG1 keep-out + 0.5 | 417.9 | 47.90 | 50.90 |
| B | I | 3 | dtp | stacked | 20 | 9 | no | cell 3.2+0.3=3.5 does not fit under standoff 3 (board underside y 4.50) | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | dtp | stacked | 20 | 9 | no | cell hits SIG1 standoff (circumradius 2.9) | 417.9 | 47.90 | 50.90 |
| B | II | 3 | dtp | stacked | 20 | 9 | no | module enters SIG1 keep-out + 0.5 | 417.9 | 47.90 | 50.90 |
| B | I | 3 | 501015 | series | 18 | 6 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | series | 18 | 6 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 354.9 | 47.90 | 50.90 |
| B | II | 3 | 501015 | series | 18 | 6 | no | module top 6.40 > LID_Y 6 | 128.8 | 47.90 | 50.90 |
| B | I | 3 | 501015 | series | 18 | 6.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | series | 18 | 6.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 354.9 | 47.90 | 50.90 |
| B | II | 3 | 501015 | series | 18 | 6.5 | no | cell top 7.00 > LID_Y 6.5 | 128.8 | 47.90 | 50.90 |
| B | I | 3 | 501015 | series | 18 | 7 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | series | 18 | 7 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 354.9 | 47.90 | 50.90 |
| B | II | 3 | 501015 | series | 18 | 7 | no | JST_SH top 7.30 > LID_Y 7 | 128.8 | 47.90 | 50.90 |
| B | I | 3 | 501015 | series | 18 | 8 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | series | 18 | 8 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 354.9 | 47.90 | 50.90 |
| B | II | 3 | 501015 | series | 18 | 8 | no | module overlaps ADS1292_RSM | 128.8 | 47.90 | 50.90 |
| B | I | 3 | 501015 | series | 18 | 8.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | series | 18 | 8.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 354.9 | 47.90 | 50.90 |
| B | II | 3 | 501015 | series | 18 | 8.5 | no | module overlaps ADS1292_RSM | 128.8 | 47.90 | 50.90 |
| B | I | 3 | 501015 | series | 18 | 9 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | series | 18 | 9 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 354.9 | 47.90 | 50.90 |
| B | II | 3 | 501015 | series | 18 | 9 | no | module overlaps ADS1292_RSM | 128.8 | 47.90 | 50.90 |
| B | I | 3 | 501015 | series | 19 | 6 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | series | 19 | 6 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 390.9 | 47.90 | 50.90 |
| B | II | 3 | 501015 | series | 19 | 6 | no | module top 6.40 > LID_Y 6 | 147.8 | 47.90 | 50.90 |
| B | I | 3 | 501015 | series | 19 | 6.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | series | 19 | 6.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 390.9 | 47.90 | 50.90 |
| B | II | 3 | 501015 | series | 19 | 6.5 | no | cell top 7.00 > LID_Y 6.5 | 147.8 | 47.90 | 50.90 |
| B | I | 3 | 501015 | series | 19 | 7 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | series | 19 | 7 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 390.9 | 47.90 | 50.90 |
| B | II | 3 | 501015 | series | 19 | 7 | no | module overlaps ADS1292_RSM | 147.8 | 47.90 | 50.90 |
| B | I | 3 | 501015 | series | 19 | 8 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | series | 19 | 8 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 390.9 | 47.90 | 50.90 |
| B | II | 3 | 501015 | series | 19 | 8 | no | module overlaps ADS1292_RSM | 147.8 | 47.90 | 50.90 |
| B | I | 3 | 501015 | series | 19 | 8.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | series | 19 | 8.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 390.9 | 47.90 | 50.90 |
| B | II | 3 | 501015 | series | 19 | 8.5 | no | module overlaps ADS1292_RSM | 147.8 | 47.90 | 50.90 |
| B | I | 3 | 501015 | series | 19 | 9 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | series | 19 | 9 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 390.9 | 47.90 | 50.90 |
| B | II | 3 | 501015 | series | 19 | 9 | no | module overlaps ADS1292_RSM | 147.8 | 47.90 | 50.90 |
| B | I | 3 | 501015 | series | 20 | 6 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | series | 20 | 6 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 426.9 | 47.90 | 50.90 |
| B | II | 3 | 501015 | series | 20 | 6 | no | module top 6.40 > LID_Y 6 | 166.8 | 47.90 | 50.90 |
| B | I | 3 | 501015 | series | 20 | 6.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | series | 20 | 6.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 426.9 | 47.90 | 50.90 |
| B | II | 3 | 501015 | series | 20 | 6.5 | no | cell top 7.00 > LID_Y 6.5 | 166.8 | 47.90 | 50.90 |
| B | I | 3 | 501015 | series | 20 | 7 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | series | 20 | 7 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 426.9 | 47.90 | 50.90 |
| B | II | 3 | 501015 | series | 20 | 7 | no | module overlaps switch | 166.8 | 47.90 | 50.90 |
| B | I | 3 | 501015 | series | 20 | 8 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | series | 20 | 8 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 426.9 | 47.90 | 50.90 |
| B | II | 3 | 501015 | series | 20 | 8 | no | module overlaps switch | 166.8 | 47.90 | 50.90 |
| B | I | 3 | 501015 | series | 20 | 8.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | series | 20 | 8.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 426.9 | 47.90 | 50.90 |
| B | II | 3 | 501015 | series | 20 | 8.5 | no | module overlaps switch | 166.8 | 47.90 | 50.90 |
| B | I | 3 | 501015 | series | 20 | 9 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | series | 20 | 9 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 426.9 | 47.90 | 50.90 |
| B | II | 3 | 501015 | series | 20 | 9 | no | module overlaps switch | 166.8 | 47.90 | 50.90 |
| B | I | 3 | 501015 | stacked | 18 | 6 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | stacked | 18 | 6 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 345.8 | 47.90 | 50.90 |
| B | II | 3 | 501015 | stacked | 18 | 6 | no | cell top 9.40 > LID_Y 6 | 345.8 | 47.90 | 50.90 |
| B | I | 3 | 501015 | stacked | 18 | 6.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | stacked | 18 | 6.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 345.8 | 47.90 | 50.90 |
| B | II | 3 | 501015 | stacked | 18 | 6.5 | no | cell top 9.40 > LID_Y 6.5 | 345.8 | 47.90 | 50.90 |
| B | I | 3 | 501015 | stacked | 18 | 7 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | stacked | 18 | 7 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 345.8 | 47.90 | 50.90 |
| B | II | 3 | 501015 | stacked | 18 | 7 | no | cell top 9.40 > LID_Y 7 | 345.8 | 47.90 | 50.90 |
| B | I | 3 | 501015 | stacked | 18 | 8 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | stacked | 18 | 8 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 345.8 | 47.90 | 50.90 |
| B | II | 3 | 501015 | stacked | 18 | 8 | no | cell top 9.40 > LID_Y 8 | 345.8 | 47.90 | 50.90 |
| B | I | 3 | 501015 | stacked | 18 | 8.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | stacked | 18 | 8.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 345.8 | 47.90 | 50.90 |
| B | II | 3 | 501015 | stacked | 18 | 8.5 | no | cell top 9.40 > LID_Y 8.5 | 345.8 | 47.90 | 50.90 |
| B | I | 3 | 501015 | stacked | 18 | 9 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | stacked | 18 | 9 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 345.8 | 47.90 | 50.90 |
| B | II | 3 | 501015 | stacked | 18 | 9 | no | cell top 9.40 > LID_Y 9 | 345.8 | 47.90 | 50.90 |
| B | I | 3 | 501015 | stacked | 19 | 6 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | stacked | 19 | 6 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 381.2 | 47.90 | 50.90 |
| B | II | 3 | 501015 | stacked | 19 | 6 | no | cell top 9.40 > LID_Y 6 | 381.2 | 47.90 | 50.90 |
| B | I | 3 | 501015 | stacked | 19 | 6.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | stacked | 19 | 6.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 381.2 | 47.90 | 50.90 |
| B | II | 3 | 501015 | stacked | 19 | 6.5 | no | cell top 9.40 > LID_Y 6.5 | 381.2 | 47.90 | 50.90 |
| B | I | 3 | 501015 | stacked | 19 | 7 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | stacked | 19 | 7 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 381.2 | 47.90 | 50.90 |
| B | II | 3 | 501015 | stacked | 19 | 7 | no | cell top 9.40 > LID_Y 7 | 381.2 | 47.90 | 50.90 |
| B | I | 3 | 501015 | stacked | 19 | 8 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | stacked | 19 | 8 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 381.2 | 47.90 | 50.90 |
| B | II | 3 | 501015 | stacked | 19 | 8 | no | cell top 9.40 > LID_Y 8 | 381.2 | 47.90 | 50.90 |
| B | I | 3 | 501015 | stacked | 19 | 8.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | stacked | 19 | 8.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 381.2 | 47.90 | 50.90 |
| B | II | 3 | 501015 | stacked | 19 | 8.5 | no | cell top 9.40 > LID_Y 8.5 | 381.2 | 47.90 | 50.90 |
| B | I | 3 | 501015 | stacked | 19 | 9 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | stacked | 19 | 9 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 381.2 | 47.90 | 50.90 |
| B | II | 3 | 501015 | stacked | 19 | 9 | no | cell top 9.40 > LID_Y 9 | 381.2 | 47.90 | 50.90 |
| B | I | 3 | 501015 | stacked | 20 | 6 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | stacked | 20 | 6 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 417.9 | 47.90 | 50.90 |
| B | II | 3 | 501015 | stacked | 20 | 6 | no | cell top 9.40 > LID_Y 6 | 417.9 | 47.90 | 50.90 |
| B | I | 3 | 501015 | stacked | 20 | 6.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | stacked | 20 | 6.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 417.9 | 47.90 | 50.90 |
| B | II | 3 | 501015 | stacked | 20 | 6.5 | no | cell top 9.40 > LID_Y 6.5 | 417.9 | 47.90 | 50.90 |
| B | I | 3 | 501015 | stacked | 20 | 7 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | stacked | 20 | 7 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 417.9 | 47.90 | 50.90 |
| B | II | 3 | 501015 | stacked | 20 | 7 | no | cell top 9.40 > LID_Y 7 | 417.9 | 47.90 | 50.90 |
| B | I | 3 | 501015 | stacked | 20 | 8 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | stacked | 20 | 8 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 417.9 | 47.90 | 50.90 |
| B | II | 3 | 501015 | stacked | 20 | 8 | no | cell top 9.40 > LID_Y 8 | 417.9 | 47.90 | 50.90 |
| B | I | 3 | 501015 | stacked | 20 | 8.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | stacked | 20 | 8.5 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 417.9 | 47.90 | 50.90 |
| B | II | 3 | 501015 | stacked | 20 | 8.5 | no | cell top 9.40 > LID_Y 8.5 | 417.9 | 47.90 | 50.90 |
| B | I | 3 | 501015 | stacked | 20 | 9 | no | cell 5.2+0.3=5.5 does not fit under standoff 3 (board underside y 4.50) | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 501015 | stacked | 20 | 9 | no | cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00) | 417.9 | 47.90 | 50.90 |
| B | II | 3 | 501015 | stacked | 20 | 9 | no | cell top 9.40 > LID_Y 9 | 417.9 | 47.90 | 50.90 |

## 2. First-conflict families

Interface I (288 runs): none close.

- DTP301120 + standoff 3.0 (72): cell 3.2+0.3=3.5 does not fit under standoff 3.0 (board underside y 4.50).
- DTP301120 + standoff 3.5 (72): cell hits SIG1 standoff (circumradius 2.9). The 22.0 mm cell on the floor reaches s of SIG1 at 22.0.
- 501015 + standoff 3.0 (72): cell 5.2+0.3=5.5 does not fit under standoff 3.0.
- 501015 + standoff 3.5 (72): cell 5.2+0.3=5.5 does not fit under standoff 3.5 (board underside y 5.00). The cell fits a 3.5 standoff only when its packed height is ≤ 3.5; 501015 is 5.5.

Adjustment region per site (Interface I, formula only): 4.0 − 2.9 − 0.3 = ±0.8 mm. NOT_MEASURED on the solid.

Interface II (144 runs): four close, all A 501015 series width 20.

## 3. Plan v2 §4 rule, line by line

Rule (1) closes ≤ 9.0 high and 20 wide, checks on the built solid, TOTAL_CHORD ≤ M1−3.

Four layouts close in packing: A_501015_series_w20_y7_iII_s3, A_501015_series_w20_y8_iII_s3, A_501015_series_w20_y8.5_iII_s3, A_501015_series_w20_y9_iII_s3. TOTAL_CHORD 47.90 ≤ 49.00 (M1=52 from default.toml; Q34 blank). USB-C hangs off the hook-end end face (fallback); the medial opening is not cut on the order-1 solid.
Architecture B does not close. Architecture C is out.
Interface I does not close.

Rule (2) parts orderable. The closer uses Raytac MDBT50Q-1MV2, cell 501015, ADS1292, BQ25100, TLV713, JST-SH, USB-C 16-pin, BAV199S arrays, a 4.5 × 4.5 × 1.6 recovery switch, a 7.6 × 2.5 × 2.5 bench header, DIN 439 M2.5 nuts and ISO 7380 M2.5×4 screws, flex tabs. Page prices are NOT_MEASURED (no vendor contact).

Rule (3) fewest Rolf steps. Interface I would skip tabs (board on standoff tops). It does not close, so the only closer is Interface II (tabs under standoffs). No decision.

Rule (4) lowest page price. NOT_MEASURED.

Ties go to A. The only architecture that closes is A.

## 4. Smallest body per architecture

- **A**: packing-smallest `A_501015_series_w20_y7_iII_s3`. BODY_WIDTH 20, LID_Y 7, BODY_THICK 8, TOTAL_CHORD 47.90, USB wall: hook-end end face (fallback).
  Stage B of the order-1 path uses LID_Y 8.0: CELL_envelope is the v1 5.2+0.5 foam box, and LID_Y 7.0 fails that check by 0.2 mm before the solid is written.
- **B**: does not close.
- **C**: does not close.

## 5. Layout for the board lane (architectures that close)

Hand `A_501015_series_w20_y7_iII_s3` to the board lane. Interface II. Flex 0.4 at parts, 0.2 at tabs.
Board zone u 2.25–17.75, s 18.60–37.60. Underside y 4.00, top y 4.40.
Cell 501015 10.4 × 15.6 × 5.2 plus foam 0.3 in the pocket, centre (7.00, 9.30), y 1.50–7.00.
Module Raytac 15.50 × 10.50 × 2.3, centre (10.00, 32.35), y 4.40–6.70 (length along u). Antenna keep-out 12.4 × 3.8 at s 33.80–37.60, u 3.80–16.20 (Raytac Spec K / interface §6.3).
Recovery switch 4.5 × 4.5 × 1.6 on the board top, centre (4.80, 21.15), y 4.40–6.00.
Bench header 2.5 × 7.6 × 2.5 on the board top, centre (15.40, 22.60), y 4.40–6.90.
ADS1292 5.0 × 5.0 × 1.0 at (11.20, 21.25). BAV199S_1 (9.95, 25.32), BAV199S_2 (12.65, 25.32). BQ25100 (3.45, 25.30). TLV713 (5.40, 25.35). JST-SH 4.0 × 6.0 × 2.9 in the pocket at (14.40, 4.65), y 1.90–4.80.
USB-C 8.9 × 7.3 × 3.2 at (10.00, −2.15), y 1.00–4.20. It would cut the **hook-end end face (fallback)**. Recess 1.0, ligaments 1.5, plug volume 12 × 6.5 × 15. No decision.
Flex tabs (ring Ø5.0, hole Ø2.7, strip 2.5, bend R ≥ 1.0):
- SIG1: (5.90, 22.00) → (5.90, 29.00).
- SIG2: (10.40, 33.10) → (10.40, 26.10).
- REF: (8.50, 43.00) → (8.50, 36.80). REF runs to the tail pocket. Q28 allows the pocket to grow.
Stack inside the wall: tab 0.2 + nut 1.6 + screw tip past the nut 0.70 = 2.50. Screw ISO 7380 M2.5×4. Nut DIN 439 M2.5, m 1.6, s 5.0.
Standoffs 5 AF from the floor to y 4.50 (height 3.0 above the inner floor). Bosses 0.5 lower are NOT_MEASURED on the order-1 solid.
Harness 100 ± 3 mm: NOT_MEASURED (routed length, not a solid).
25 of 25 0402 courtyards placed (6 on the board, 19 in the pocket).

B and C do not close. There is no board-lane layout for them.

## 6. Winners sent to Stage B (at most six)

- `A_501015_series_w20_y7_iII_s3` — packing-closes; Stage B CELL_envelope uses foam 0.5 and fails at LID_Y 7.0 (clear_y −0.2)
- `A_501015_series_w20_y8_iII_s3` (`scripts/cad/params/stageb_v2.toml`; smallest LID_Y the order-1 CELL_envelope accepts)
- `A_501015_series_w20_y8.5_iII_s3`
- `A_501015_series_w20_y9_iII_s3`
Construction is the order-1 path with packing C (width 20, arc 48.4). No fork.

## 7. Numbers taken as given

| Item | Number | Source |
|---|---|---|
| Raytac MDBT50Q-1MV2 | 10.5 × 15.5 × 2.3 | coordinator note 3 / plan v2 §3 reserve; Spec K footprint 10.5 × 15.5 × 2.0 |
| Raytac antenna keep-out | 12.4 × 3.8 | Raytac Spec K p.9/p.13, interface.md §6.3 |
| Ebyte E73-2G4M08S1C | 13 × 18 × 2.0 | brief; plan v2 §3 |
| E73 antenna keep-out | 12.4 × 3.8 | sheet unreachable; v1 rule interface §6.3 |
| Seeed XIAO nRF52840 | out | plan v2 turn 02 findings 1 and 2 |
| DTP301120 with protection | 22.0 × 11.5 × 3.2 | SparkFun PRT-25270 drawing, L5-research-v2.md §1 |
| 501015 | 5.2 × 10.4 × 15.6 | v1 CELL_BODY_MAX; plan v2 §3 quotes 5.4 thick |
| Foam under a cell | 0.3 | brief; plan v2 §3 |
| Interface I board | FR4 1.0, 4-layer | plan v2 turn 07 |
| Interface I pad | 8 × 8 ENIG, half-size 4.0 | turn 07 |
| Standoff | M2.5 hex 5 AF, circumradius 2.9, heights 3.0 and 3.5 | turn 07; coordinator note 3 |
| Boss drop | 0.5 | turn 07 |
| Placement tolerance | 0.3 | JLC floor ±0.3, turn 07 G7 |
| Adjustment region | ±0.8 | 4.0 − 2.9 − 0.3 |
| Flex + stiffener | 0.11 + 0.3 = 0.4 at parts, 0.2 at tabs | brief |
| ADS1292 VQFN-32 courtyard | 5.0 × 5.0 × 1.0 | brief |
| Recovery switch | 4.5 × 4.5 × 1.6 | coordinator note 3 |
| Bench header | 7.6 × 2.5 × 2.5 | plan v2 §5.6 |
| USB-C 16-pin | 8.9 × 7.3 × 3.2 | brief |
| USB opening / recess / ligament | 9.0 × 3.5 / 1.0 / 1.5 | coordinator note 1 |
| Plug volume | 12 × 6.5 × 15 | plan v2 §5.4 |
| JST-SH | 4.0 × 6.0 × 2.9 side entry | brief |
| Ring pad | Ø5.0, hole Ø2.7, strip 2.5 | brief; Interface II |
| Nut DIN 439 M2.5 | m 1.6, s 5.0 | brief |
| Screw ISO 7380 M2.5×4 | length 4.0 | v1; brief |
| Stack inside the wall | 2.50 | 0.2 + 1.6 + 0.70 |
| Harness | 100 ± 3 mm | plan v2; NOT_MEASURED as a solid |
| BODY_WIDTH / LID_Y / BODY_ARC | 18–20 / 6.0–9.0 / 48.4 | coordinator note 1; other params stageb_provisional.toml |
| M1 | 52 | default.toml; Q34 blank |
| PATH_RADIUS | 97.1025 | v1 |
| Floor | 1.5 | v1 |

## 8. What could not be measured

- TAB_envelope_air pre-CAD for PACKING=v2: the TE 31428 pad-gap search is not the flex tab.
- V2_WALL_minima inner face at y 0.75: the probe returned the outer skin (~0.20), not 1.5.
- V2_ADJUSTMENT: ±0.8 is a pad/standoff formula, not a solid probe.
- V2_USB_medial: the order-1 solid has no medial USB cut.
- V2_HARNESS: 100 ± 3 mm is a routed length.
- V2_BOSS: printed bosses 0.5 below the standoff top are not on the order-1 solid.
- E73 antenna sheet: unreachable; v1 12.4 × 3.8 used.
- M1 on Rolf (Q34): default 52 used for the gate.

