# Packing v2 — which architectures close

WP11 analysis. The plan is not changed. Nothing is ordered.
Architecture C is out (plan v2 turn 02). Interface I is turn 07/09:
no springs, no pins; board underside on three brass standoff tops;
8 × 8 gold pad per site; bosses 0.5 lower than the standoff tops;
cell under the board only with positive nominal clearance and no load
after the board bends onto the bosses. Standoffs 3.0, 3.5 and 4.0.
A 0.5-deep floor recess (web 1.0 remaining) is run at 3.5 and 4.0.
Interface II is the flex-tab fallback.
Arc-plus was not run: layouts already close at BODY_ARC 48.4.

## 1. Every run at BODY_ARC 48.4

| arch | iface | standoff | recess | cell | layout | width | lid | closes | first conflict | nom clr | def clr | stack | outer0 | outer@lid | free mm² | TOTAL_CHORD | M1 gate |
|---|---|---:|---:|---|---|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A | I | 3 | 0 | dtp | series | 18 | 6 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 7.0 | 98.0 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 18 | 6 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 7.0 | 98.0 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 18 | 6 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 7.0 | 98.0 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 18 | 6 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 7.0 | 98.0 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 18 | 6 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 7.0 | 98.0 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 18 | 6 | no | module top 7.62 > LID_Y 6 | -0.7 | -1.2 | 6.1 | 8.6 | 7.0 | 5.8 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 18 | 6.5 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 7.5 | 98.0 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 18 | 6.5 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 7.5 | 98.0 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 18 | 6.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 7.5 | 98.0 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 18 | 6.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 7.5 | 98.0 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 18 | 6.5 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 7.5 | 98.0 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 18 | 6.5 | no | module top 7.62 > LID_Y 6.5 | -0.7 | -1.2 | 6.1 | 8.6 | 7.5 | 5.8 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 18 | 7 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 8.0 | 98.0 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 18 | 7 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 8.0 | 98.0 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 18 | 7 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 8.0 | 98.0 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 18 | 7 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 8.0 | 98.0 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 18 | 7 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 8.0 | 98.0 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 18 | 7 | no | module top 7.62 > LID_Y 7 | -0.7 | -1.2 | 6.1 | 8.6 | 8.0 | 5.8 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 18 | 8 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 9.0 | 98.0 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 18 | 8 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 9.0 | 98.0 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 18 | 8 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 9.0 | 98.0 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 18 | 8 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 9.0 | 98.0 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 18 | 8 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 9.0 | 98.0 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 18 | 8 | no | JST_SH top 8.22 > LID_Y 8 | -0.7 | -1.2 | 6.1 | 8.6 | 9.0 | 5.8 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 18 | 8.5 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 9.5 | 98.0 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 18 | 8.5 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 9.5 | 98.0 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 18 | 8.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 9.5 | 98.0 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 18 | 8.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 9.5 | 98.0 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 18 | 8.5 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 9.5 | 98.0 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 18 | 8.5 | no | module 10.50×15.50 at (7.50,29.85) outside the board | -0.7 | -1.2 | 6.1 | 8.6 | 9.5 | 5.8 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 18 | 9 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 10.0 | 98.0 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 18 | 9 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 10.0 | 98.0 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 18 | 9 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 10.0 | 98.0 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 18 | 9 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 10.0 | 98.0 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 18 | 9 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 10.0 | 98.0 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 18 | 9 | no | module 10.50×15.50 at (7.50,29.85) outside the board | -0.7 | -1.2 | 6.1 | 8.6 | 10.0 | 5.8 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 19 | 6 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 7.0 | 145.4 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 19 | 6 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 7.0 | 145.4 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 19 | 6 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 7.0 | 145.4 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 19 | 6 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 7.0 | 145.4 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 19 | 6 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 7.0 | 145.4 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 19 | 6 | no | module top 7.62 > LID_Y 6 | -0.7 | -1.2 | 6.1 | 8.6 | 7.0 | 15.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 19 | 6.5 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 7.5 | 145.4 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 19 | 6.5 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 7.5 | 145.4 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 19 | 6.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 7.5 | 145.4 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 19 | 6.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 7.5 | 145.4 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 19 | 6.5 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 7.5 | 145.4 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 19 | 6.5 | no | module top 7.62 > LID_Y 6.5 | -0.7 | -1.2 | 6.1 | 8.6 | 7.5 | 15.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 19 | 7 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 8.0 | 145.4 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 19 | 7 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 8.0 | 145.4 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 19 | 7 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 8.0 | 145.4 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 19 | 7 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 8.0 | 145.4 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 19 | 7 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 8.0 | 145.4 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 19 | 7 | no | module top 7.62 > LID_Y 7 | -0.7 | -1.2 | 6.1 | 8.6 | 8.0 | 15.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 19 | 8 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 9.0 | 145.4 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 19 | 8 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 9.0 | 145.4 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 19 | 8 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 9.0 | 145.4 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 19 | 8 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 9.0 | 145.4 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 19 | 8 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 9.0 | 145.4 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 19 | 8 | no | JST_SH top 8.22 > LID_Y 8 | -0.7 | -1.2 | 6.1 | 8.6 | 9.0 | 15.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 19 | 8.5 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 9.5 | 145.4 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 19 | 8.5 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 9.5 | 145.4 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 19 | 8.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 9.5 | 145.4 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 19 | 8.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 9.5 | 145.4 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 19 | 8.5 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 9.5 | 145.4 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 19 | 8.5 | no | module 10.50×15.50 at (7.50,29.85) outside the board | -0.7 | -1.2 | 6.1 | 8.6 | 9.5 | 15.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 19 | 9 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 10.0 | 145.4 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 19 | 9 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 10.0 | 145.4 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 19 | 9 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 10.0 | 145.4 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 19 | 9 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 10.0 | 145.4 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 19 | 9 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 10.0 | 145.4 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 19 | 9 | no | module 10.50×15.50 at (7.50,29.85) outside the board | -0.7 | -1.2 | 6.1 | 8.6 | 10.0 | 15.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 20 | 6 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 7.0 | 203.8 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 20 | 6 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 7.0 | 203.8 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 20 | 6 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 7.0 | 203.8 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 20 | 6 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 7.0 | 203.8 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 20 | 6 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 7.0 | 203.8 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 20 | 6 | no | module top 7.62 > LID_Y 6 | -0.7 | -1.2 | 6.1 | 8.6 | 7.0 | 6.0 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 20 | 6.5 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 7.5 | 203.8 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 20 | 6.5 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 7.5 | 203.8 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 20 | 6.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 7.5 | 203.8 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 20 | 6.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 7.5 | 203.8 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 20 | 6.5 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 7.5 | 203.8 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 20 | 6.5 | no | module top 7.62 > LID_Y 6.5 | -0.7 | -1.2 | 6.1 | 8.6 | 7.5 | 6.0 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 20 | 7 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 8.0 | 203.8 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 20 | 7 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 8.0 | 203.8 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 20 | 7 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 8.0 | 203.8 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 20 | 7 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 8.0 | 203.8 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 20 | 7 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 8.0 | 203.8 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 20 | 7 | no | module top 7.62 > LID_Y 7 | -0.7 | -1.2 | 6.1 | 8.6 | 8.0 | 6.0 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 20 | 8 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 9.0 | 203.8 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 20 | 8 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 9.0 | 203.8 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 20 | 8 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 9.0 | 203.8 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 20 | 8 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 9.0 | 203.8 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 20 | 8 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 9.0 | 203.8 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 20 | 8 | no | cell to antenna zone 2.65 < 5 mm | -0.7 | -1.2 | 6.1 | 8.6 | 9.0 | 6.0 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 20 | 8.5 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 9.5 | 203.8 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 20 | 8.5 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 9.5 | 203.8 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 20 | 8.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 9.5 | 203.8 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 20 | 8.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 9.5 | 203.8 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 20 | 8.5 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 9.5 | 203.8 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 20 | 8.5 | no | cell to antenna zone 2.65 < 5 mm | -0.7 | -1.2 | 6.1 | 8.6 | 9.5 | 6.0 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 20 | 9 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 10.0 | 203.8 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 20 | 9 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 10.0 | 203.8 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 20 | 9 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 10.0 | 203.8 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 20 | 9 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 10.0 | 203.8 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 20 | 9 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 10.0 | 203.8 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 20 | 9 | no | cell to antenna zone 2.65 < 5 mm | -0.7 | -1.2 | 6.1 | 8.6 | 10.0 | 6.0 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 18 | 6 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 7.0 | 161.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 18 | 6 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 7.0 | 161.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 18 | 6 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 7.0 | 161.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 18 | 6 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 7.0 | 161.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 18 | 6 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 7.0 | 161.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 18 | 6 | no | module top 7.62 > LID_Y 6 | -0.7 | -1.2 | 6.1 | 8.6 | 7.0 | 144.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 18 | 6.5 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 7.5 | 161.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 18 | 6.5 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 7.5 | 161.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 18 | 6.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 7.5 | 161.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 18 | 6.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 7.5 | 161.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 18 | 6.5 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 7.5 | 161.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 18 | 6.5 | no | module top 7.62 > LID_Y 6.5 | -0.7 | -1.2 | 6.1 | 8.6 | 7.5 | 144.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 18 | 7 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 8.0 | 161.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 18 | 7 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 8.0 | 161.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 18 | 7 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 8.0 | 161.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 18 | 7 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 8.0 | 161.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 18 | 7 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 8.0 | 161.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 18 | 7 | no | module top 7.62 > LID_Y 7 | -0.7 | -1.2 | 6.1 | 8.6 | 8.0 | 144.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 18 | 8 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 9.0 | 161.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 18 | 8 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 9.0 | 161.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 18 | 8 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 9.0 | 161.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 18 | 8 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 9.0 | 161.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 18 | 8 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 9.0 | 161.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 18 | 8 | no | cell top 11.32 > LID_Y 8 | -0.7 | -1.2 | 6.1 | 8.6 | 9.0 | 144.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 18 | 8.5 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 9.5 | 161.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 18 | 8.5 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 9.5 | 161.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 18 | 8.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 9.5 | 161.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 18 | 8.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 9.5 | 161.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 18 | 8.5 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 9.5 | 161.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 18 | 8.5 | no | cell top 11.32 > LID_Y 8.5 | -0.7 | -1.2 | 6.1 | 8.6 | 9.5 | 144.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 18 | 9 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 10.0 | 161.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 18 | 9 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 10.0 | 161.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 18 | 9 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 10.0 | 161.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 18 | 9 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 10.0 | 161.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 18 | 9 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 10.0 | 161.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 18 | 9 | no | cell top 11.32 > LID_Y 9 | -0.7 | -1.2 | 6.1 | 8.6 | 10.0 | 144.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 19 | 6 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 7.0 | 197.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 19 | 6 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 7.0 | 197.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 19 | 6 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 7.0 | 197.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 19 | 6 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 7.0 | 197.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 19 | 6 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 7.0 | 197.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 19 | 6 | no | module top 7.62 > LID_Y 6 | -0.7 | -1.2 | 6.1 | 8.6 | 7.0 | 168.3 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 19 | 6.5 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 7.5 | 197.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 19 | 6.5 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 7.5 | 197.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 19 | 6.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 7.5 | 197.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 19 | 6.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 7.5 | 197.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 19 | 6.5 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 7.5 | 197.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 19 | 6.5 | no | module top 7.62 > LID_Y 6.5 | -0.7 | -1.2 | 6.1 | 8.6 | 7.5 | 168.3 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 19 | 7 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 8.0 | 197.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 19 | 7 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 8.0 | 197.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 19 | 7 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 8.0 | 197.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 19 | 7 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 8.0 | 197.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 19 | 7 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 8.0 | 197.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 19 | 7 | no | module top 7.62 > LID_Y 7 | -0.7 | -1.2 | 6.1 | 8.6 | 8.0 | 168.3 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 19 | 8 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 9.0 | 197.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 19 | 8 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 9.0 | 197.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 19 | 8 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 9.0 | 197.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 19 | 8 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 9.0 | 197.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 19 | 8 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 9.0 | 197.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 19 | 8 | no | cell top 11.32 > LID_Y 8 | -0.7 | -1.2 | 6.1 | 8.6 | 9.0 | 168.3 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 19 | 8.5 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 9.5 | 197.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 19 | 8.5 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 9.5 | 197.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 19 | 8.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 9.5 | 197.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 19 | 8.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 9.5 | 197.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 19 | 8.5 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 9.5 | 197.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 19 | 8.5 | no | cell top 11.32 > LID_Y 8.5 | -0.7 | -1.2 | 6.1 | 8.6 | 9.5 | 168.3 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 19 | 9 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 10.0 | 197.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 19 | 9 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 10.0 | 197.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 19 | 9 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 10.0 | 197.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 19 | 9 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 10.0 | 197.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 19 | 9 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 10.0 | 197.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 19 | 9 | no | cell top 11.32 > LID_Y 9 | -0.7 | -1.2 | 6.1 | 8.6 | 10.0 | 168.3 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 20 | 6 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 7.0 | 232.4 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 20 | 6 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 7.0 | 232.4 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 20 | 6 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 7.0 | 232.4 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 20 | 6 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 7.0 | 232.4 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 20 | 6 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 7.0 | 232.4 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 20 | 6 | no | module top 7.62 > LID_Y 6 | -0.7 | -1.2 | 6.1 | 8.6 | 7.0 | 174.4 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 20 | 6.5 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 7.5 | 232.4 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 20 | 6.5 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 7.5 | 232.4 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 20 | 6.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 7.5 | 232.4 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 20 | 6.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 7.5 | 232.4 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 20 | 6.5 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 7.5 | 232.4 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 20 | 6.5 | no | module top 7.62 > LID_Y 6.5 | -0.7 | -1.2 | 6.1 | 8.6 | 7.5 | 174.4 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 20 | 7 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 8.0 | 232.4 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 20 | 7 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 8.0 | 232.4 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 20 | 7 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 8.0 | 232.4 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 20 | 7 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 8.0 | 232.4 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 20 | 7 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 8.0 | 232.4 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 20 | 7 | no | module top 7.62 > LID_Y 7 | -0.7 | -1.2 | 6.1 | 8.6 | 8.0 | 174.4 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 20 | 8 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 9.0 | 232.4 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 20 | 8 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 9.0 | 232.4 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 20 | 8 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 9.0 | 232.4 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 20 | 8 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 9.0 | 232.4 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 20 | 8 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 9.0 | 232.4 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 20 | 8 | no | cell top 11.32 > LID_Y 8 | -0.7 | -1.2 | 6.1 | 8.6 | 9.0 | 174.4 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 20 | 8.5 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 9.5 | 232.4 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 20 | 8.5 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 9.5 | 232.4 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 20 | 8.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 9.5 | 232.4 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 20 | 8.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 9.5 | 232.4 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 20 | 8.5 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 9.5 | 232.4 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 20 | 8.5 | no | cell top 11.32 > LID_Y 8.5 | -0.7 | -1.2 | 6.1 | 8.6 | 9.5 | 174.4 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 20 | 9 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.3 | 8.8 | 10.0 | 232.4 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 20 | 9 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.8 | 9.3 | 10.0 | 232.4 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 20 | 9 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.3 | 9.8 | 10.0 | 232.4 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 20 | 9 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.8 | 9.3 | 10.0 | 232.4 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 20 | 9 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +0.8 | +0.3 | 7.3 | 9.8 | 10.0 | 232.4 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 20 | 9 | no | cell top 11.32 > LID_Y 9 | -0.7 | -1.2 | 6.1 | 8.6 | 10.0 | 174.4 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 18 | 6 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 7.0 | 147.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 18 | 6 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 7.0 | 147.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 18 | 6 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 7.0 | 147.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 18 | 6 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 7.0 | 147.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 18 | 6 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 7.0 | 147.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 18 | 6 | no | module top 7.62 > LID_Y 6 | -2.7 | -3.2 | 6.1 | 8.6 | 7.0 | 34.2 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 18 | 6.5 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 7.5 | 147.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 18 | 6.5 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 7.5 | 147.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 18 | 6.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 7.5 | 147.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 18 | 6.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 7.5 | 147.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 18 | 6.5 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 7.5 | 147.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 18 | 6.5 | no | module top 7.62 > LID_Y 6.5 | -2.7 | -3.2 | 6.1 | 8.6 | 7.5 | 34.2 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 18 | 7 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 8.0 | 147.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 18 | 7 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 8.0 | 147.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 18 | 7 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 8.0 | 147.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 18 | 7 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 8.0 | 147.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 18 | 7 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 8.0 | 147.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 18 | 7 | no | module top 7.62 > LID_Y 7 | -2.7 | -3.2 | 6.1 | 8.6 | 8.0 | 34.2 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 18 | 8 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 9.0 | 147.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 18 | 8 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 9.0 | 147.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 18 | 8 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 9.0 | 147.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 18 | 8 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 9.0 | 147.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 18 | 8 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 9.0 | 147.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 18 | 8 | no | JST_SH top 8.22 > LID_Y 8 | -2.7 | -3.2 | 6.1 | 8.6 | 9.0 | 34.2 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 18 | 8.5 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 9.5 | 147.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 18 | 8.5 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 9.5 | 147.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 18 | 8.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 9.5 | 147.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 18 | 8.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 9.5 | 147.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 18 | 8.5 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 9.5 | 147.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 18 | 8.5 | no | module overlaps ADS1292_RSM | -2.7 | -3.2 | 6.1 | 8.6 | 9.5 | 34.2 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 18 | 9 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 10.0 | 147.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 18 | 9 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 10.0 | 147.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 18 | 9 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 10.0 | 147.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 18 | 9 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 10.0 | 147.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 18 | 9 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 10.0 | 147.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 18 | 9 | no | module overlaps ADS1292_RSM | -2.7 | -3.2 | 6.1 | 8.6 | 10.0 | 34.2 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 19 | 6 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 7.0 | 182.0 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 19 | 6 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 7.0 | 182.0 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 19 | 6 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 7.0 | 182.0 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 19 | 6 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 7.0 | 182.0 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 19 | 6 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 7.0 | 182.0 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 19 | 6 | no | module top 7.62 > LID_Y 6 | -2.7 | -3.2 | 6.1 | 8.6 | 7.0 | 43.5 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 19 | 6.5 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 7.5 | 182.0 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 19 | 6.5 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 7.5 | 182.0 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 19 | 6.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 7.5 | 182.0 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 19 | 6.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 7.5 | 182.0 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 19 | 6.5 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 7.5 | 182.0 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 19 | 6.5 | no | module top 7.62 > LID_Y 6.5 | -2.7 | -3.2 | 6.1 | 8.6 | 7.5 | 43.5 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 19 | 7 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 8.0 | 182.0 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 19 | 7 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 8.0 | 182.0 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 19 | 7 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 8.0 | 182.0 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 19 | 7 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 8.0 | 182.0 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 19 | 7 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 8.0 | 182.0 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 19 | 7 | no | module top 7.62 > LID_Y 7 | -2.7 | -3.2 | 6.1 | 8.6 | 8.0 | 43.5 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 19 | 8 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 9.0 | 182.0 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 19 | 8 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 9.0 | 182.0 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 19 | 8 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 9.0 | 182.0 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 19 | 8 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 9.0 | 182.0 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 19 | 8 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 9.0 | 182.0 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 19 | 8 | no | module overlaps ADS1292_RSM | -2.7 | -3.2 | 6.1 | 8.6 | 9.0 | 43.5 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 19 | 8.5 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 9.5 | 182.0 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 19 | 8.5 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 9.5 | 182.0 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 19 | 8.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 9.5 | 182.0 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 19 | 8.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 9.5 | 182.0 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 19 | 8.5 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 9.5 | 182.0 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 19 | 8.5 | no | module overlaps ADS1292_RSM | -2.7 | -3.2 | 6.1 | 8.6 | 9.5 | 43.5 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 19 | 9 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 10.0 | 182.0 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 19 | 9 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 10.0 | 182.0 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 19 | 9 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 10.0 | 182.0 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 19 | 9 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 10.0 | 182.0 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 19 | 9 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 10.0 | 182.0 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 19 | 9 | no | module overlaps ADS1292_RSM | -2.7 | -3.2 | 6.1 | 8.6 | 10.0 | 43.5 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 20 | 6 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 7.0 | 202.2 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 20 | 6 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 7.0 | 202.2 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 20 | 6 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 7.0 | 202.2 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 20 | 6 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 7.0 | 202.2 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 20 | 6 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 7.0 | 202.2 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 20 | 6 | no | module top 7.62 > LID_Y 6 | -2.7 | -3.2 | 6.1 | 8.6 | 7.0 | 41.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 20 | 6.5 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 7.5 | 202.2 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 20 | 6.5 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 7.5 | 202.2 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 20 | 6.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 7.5 | 202.2 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 20 | 6.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 7.5 | 202.2 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 20 | 6.5 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 7.5 | 202.2 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 20 | 6.5 | no | module top 7.62 > LID_Y 6.5 | -2.7 | -3.2 | 6.1 | 8.6 | 7.5 | 41.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 20 | 7 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 8.0 | 202.2 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 20 | 7 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 8.0 | 202.2 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 20 | 7 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 8.0 | 202.2 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 20 | 7 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 8.0 | 202.2 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 20 | 7 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 8.0 | 202.2 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 20 | 7 | no | module top 7.62 > LID_Y 7 | -2.7 | -3.2 | 6.1 | 8.6 | 8.0 | 41.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 20 | 8 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 9.0 | 202.2 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 20 | 8 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 9.0 | 202.2 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 20 | 8 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 9.0 | 202.2 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 20 | 8 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 9.0 | 202.2 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 20 | 8 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 9.0 | 202.2 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 20 | 8 | yes | — | -2.7 | -3.2 | 6.1 | 8.6 | 9.0 | 41.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 20 | 8.5 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 9.5 | 202.2 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 20 | 8.5 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 9.5 | 202.2 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 20 | 8.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 9.5 | 202.2 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 20 | 8.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 9.5 | 202.2 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 20 | 8.5 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 9.5 | 202.2 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 20 | 8.5 | yes | — | -2.7 | -3.2 | 6.1 | 8.6 | 9.5 | 41.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 20 | 9 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 10.0 | 202.2 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 20 | 9 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 10.0 | 202.2 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 20 | 9 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 10.0 | 202.2 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 20 | 9 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 10.0 | 202.2 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 20 | 9 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 10.0 | 202.2 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 20 | 9 | yes | — | -2.7 | -3.2 | 6.1 | 8.6 | 10.0 | 41.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 18 | 6 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 7.0 | 161.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 18 | 6 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 7.0 | 161.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 18 | 6 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 7.0 | 161.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 18 | 6 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 7.0 | 161.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 18 | 6 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 7.0 | 161.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 18 | 6 | no | module top 7.62 > LID_Y 6 | -2.7 | -3.2 | 6.1 | 8.6 | 7.0 | 161.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 18 | 6.5 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 7.5 | 161.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 18 | 6.5 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 7.5 | 161.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 18 | 6.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 7.5 | 161.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 18 | 6.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 7.5 | 161.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 18 | 6.5 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 7.5 | 161.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 18 | 6.5 | no | module top 7.62 > LID_Y 6.5 | -2.7 | -3.2 | 6.1 | 8.6 | 7.5 | 161.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 18 | 7 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 8.0 | 161.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 18 | 7 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 8.0 | 161.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 18 | 7 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 8.0 | 161.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 18 | 7 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 8.0 | 161.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 18 | 7 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 8.0 | 161.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 18 | 7 | no | module top 7.62 > LID_Y 7 | -2.7 | -3.2 | 6.1 | 8.6 | 8.0 | 161.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 18 | 8 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 9.0 | 161.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 18 | 8 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 9.0 | 161.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 18 | 8 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 9.0 | 161.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 18 | 8 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 9.0 | 161.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 18 | 8 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 9.0 | 161.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 18 | 8 | no | cell top 13.32 > LID_Y 8 | -2.7 | -3.2 | 6.1 | 8.6 | 9.0 | 161.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 18 | 8.5 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 9.5 | 161.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 18 | 8.5 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 9.5 | 161.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 18 | 8.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 9.5 | 161.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 18 | 8.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 9.5 | 161.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 18 | 8.5 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 9.5 | 161.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 18 | 8.5 | no | cell top 13.32 > LID_Y 8.5 | -2.7 | -3.2 | 6.1 | 8.6 | 9.5 | 161.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 18 | 9 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 10.0 | 161.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 18 | 9 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 10.0 | 161.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 18 | 9 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 10.0 | 161.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 18 | 9 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 10.0 | 161.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 18 | 9 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 10.0 | 161.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 18 | 9 | no | cell top 13.32 > LID_Y 9 | -2.7 | -3.2 | 6.1 | 8.6 | 10.0 | 161.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 19 | 6 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 7.0 | 197.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 19 | 6 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 7.0 | 197.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 19 | 6 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 7.0 | 197.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 19 | 6 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 7.0 | 197.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 19 | 6 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 7.0 | 197.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 19 | 6 | no | module top 7.62 > LID_Y 6 | -2.7 | -3.2 | 6.1 | 8.6 | 7.0 | 197.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 19 | 6.5 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 7.5 | 197.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 19 | 6.5 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 7.5 | 197.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 19 | 6.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 7.5 | 197.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 19 | 6.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 7.5 | 197.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 19 | 6.5 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 7.5 | 197.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 19 | 6.5 | no | module top 7.62 > LID_Y 6.5 | -2.7 | -3.2 | 6.1 | 8.6 | 7.5 | 197.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 19 | 7 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 8.0 | 197.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 19 | 7 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 8.0 | 197.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 19 | 7 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 8.0 | 197.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 19 | 7 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 8.0 | 197.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 19 | 7 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 8.0 | 197.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 19 | 7 | no | module top 7.62 > LID_Y 7 | -2.7 | -3.2 | 6.1 | 8.6 | 8.0 | 197.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 19 | 8 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 9.0 | 197.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 19 | 8 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 9.0 | 197.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 19 | 8 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 9.0 | 197.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 19 | 8 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 9.0 | 197.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 19 | 8 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 9.0 | 197.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 19 | 8 | no | cell top 13.32 > LID_Y 8 | -2.7 | -3.2 | 6.1 | 8.6 | 9.0 | 197.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 19 | 8.5 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 9.5 | 197.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 19 | 8.5 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 9.5 | 197.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 19 | 8.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 9.5 | 197.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 19 | 8.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 9.5 | 197.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 19 | 8.5 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 9.5 | 197.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 19 | 8.5 | no | cell top 13.32 > LID_Y 8.5 | -2.7 | -3.2 | 6.1 | 8.6 | 9.5 | 197.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 19 | 9 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 10.0 | 197.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 19 | 9 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 10.0 | 197.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 19 | 9 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 10.0 | 197.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 19 | 9 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 10.0 | 197.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 19 | 9 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 10.0 | 197.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 19 | 9 | no | cell top 13.32 > LID_Y 9 | -2.7 | -3.2 | 6.1 | 8.6 | 10.0 | 197.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 20 | 6 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 7.0 | 231.7 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 20 | 6 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 7.0 | 231.7 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 20 | 6 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 7.0 | 231.7 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 20 | 6 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 7.0 | 231.7 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 20 | 6 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 7.0 | 231.7 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 20 | 6 | no | module top 7.62 > LID_Y 6 | -2.7 | -3.2 | 6.1 | 8.6 | 7.0 | 200.3 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 20 | 6.5 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 7.5 | 231.7 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 20 | 6.5 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 7.5 | 231.7 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 20 | 6.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 7.5 | 231.7 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 20 | 6.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 7.5 | 231.7 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 20 | 6.5 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 7.5 | 231.7 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 20 | 6.5 | no | module top 7.62 > LID_Y 6.5 | -2.7 | -3.2 | 6.1 | 8.6 | 7.5 | 200.3 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 20 | 7 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 8.0 | 231.7 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 20 | 7 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 8.0 | 231.7 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 20 | 7 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 8.0 | 231.7 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 20 | 7 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 8.0 | 231.7 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 20 | 7 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 8.0 | 231.7 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 20 | 7 | no | module top 7.62 > LID_Y 7 | -2.7 | -3.2 | 6.1 | 8.6 | 8.0 | 200.3 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 20 | 8 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 9.0 | 231.7 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 20 | 8 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 9.0 | 231.7 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 20 | 8 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 9.0 | 231.7 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 20 | 8 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 9.0 | 231.7 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 20 | 8 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 9.0 | 231.7 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 20 | 8 | no | cell top 13.32 > LID_Y 8 | -2.7 | -3.2 | 6.1 | 8.6 | 9.0 | 200.3 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 20 | 8.5 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 9.5 | 231.7 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 20 | 8.5 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 9.5 | 231.7 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 20 | 8.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 9.5 | 231.7 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 20 | 8.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 9.5 | 231.7 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 20 | 8.5 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 9.5 | 231.7 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 20 | 8.5 | no | cell top 13.32 > LID_Y 8.5 | -2.7 | -3.2 | 6.1 | 8.6 | 9.5 | 200.3 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 20 | 9 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.3 | 8.8 | 10.0 | 231.7 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 20 | 9 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.8 | 9.3 | 10.0 | 231.7 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 20 | 9 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.3 | 9.8 | 10.0 | 231.7 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 20 | 9 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.8 | 9.3 | 10.0 | 231.7 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 20 | 9 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.3 | 9.8 | 10.0 | 231.7 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 20 | 9 | no | cell top 13.32 > LID_Y 9 | -2.7 | -3.2 | 6.1 | 8.6 | 10.0 | 200.3 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 18 | 6 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 7.0 | 70.7 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 18 | 6 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 7.0 | 70.7 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 18 | 6 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 7.0 | 70.7 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 18 | 6 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 7.0 | 70.7 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 18 | 6 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 7.0 | 70.7 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 18 | 6 | no | module top 7.32 > LID_Y 6 | -0.7 | -1.2 | 5.8 | 8.3 | 7.0 | 6.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 18 | 6.5 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 7.5 | 70.7 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 18 | 6.5 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 7.5 | 70.7 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 18 | 6.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 7.5 | 70.7 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 18 | 6.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 7.5 | 70.7 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 18 | 6.5 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 7.5 | 70.7 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 18 | 6.5 | no | module top 7.32 > LID_Y 6.5 | -0.7 | -1.2 | 5.8 | 8.3 | 7.5 | 6.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 18 | 7 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 8.0 | 70.7 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 18 | 7 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 8.0 | 70.7 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 18 | 7 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 8.0 | 70.7 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 18 | 7 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 8.0 | 70.7 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 18 | 7 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 8.0 | 70.7 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 18 | 7 | no | module top 7.32 > LID_Y 7 | -0.7 | -1.2 | 5.8 | 8.3 | 8.0 | 6.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 18 | 8 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 9.0 | 70.7 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 18 | 8 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 9.0 | 70.7 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 18 | 8 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 9.0 | 70.7 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 18 | 8 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 9.0 | 70.7 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 18 | 8 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 9.0 | 70.7 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 18 | 8 | no | JST_SH top 8.22 > LID_Y 8 | -0.7 | -1.2 | 5.8 | 8.3 | 9.0 | 6.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 18 | 8.5 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 9.5 | 70.7 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 18 | 8.5 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 9.5 | 70.7 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 18 | 8.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 9.5 | 70.7 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 18 | 8.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 9.5 | 70.7 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 18 | 8.5 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 9.5 | 70.7 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 18 | 8.5 | no | module 13.00×18.00 at (9.00,28.60) outside the board | -0.7 | -1.2 | 5.8 | 8.3 | 9.5 | 6.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 18 | 9 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 10.0 | 70.7 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 18 | 9 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 10.0 | 70.7 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 18 | 9 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 10.0 | 70.7 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 18 | 9 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 10.0 | 70.7 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 18 | 9 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 10.0 | 70.7 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 18 | 9 | no | module 13.00×18.00 at (9.00,28.60) outside the board | -0.7 | -1.2 | 5.8 | 8.3 | 10.0 | 6.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 19 | 6 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 7.0 | 86.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 19 | 6 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 7.0 | 86.2 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 19 | 6 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 7.0 | 86.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 19 | 6 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 7.0 | 86.2 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 19 | 6 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 7.0 | 86.2 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 19 | 6 | no | module top 7.32 > LID_Y 6 | -0.7 | -1.2 | 5.8 | 8.3 | 7.0 | 14.5 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 19 | 6.5 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 7.5 | 86.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 19 | 6.5 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 7.5 | 86.2 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 19 | 6.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 7.5 | 86.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 19 | 6.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 7.5 | 86.2 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 19 | 6.5 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 7.5 | 86.2 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 19 | 6.5 | no | module top 7.32 > LID_Y 6.5 | -0.7 | -1.2 | 5.8 | 8.3 | 7.5 | 14.5 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 19 | 7 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 8.0 | 86.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 19 | 7 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 8.0 | 86.2 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 19 | 7 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 8.0 | 86.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 19 | 7 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 8.0 | 86.2 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 19 | 7 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 8.0 | 86.2 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 19 | 7 | no | module top 7.32 > LID_Y 7 | -0.7 | -1.2 | 5.8 | 8.3 | 8.0 | 14.5 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 19 | 8 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 9.0 | 86.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 19 | 8 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 9.0 | 86.2 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 19 | 8 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 9.0 | 86.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 19 | 8 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 9.0 | 86.2 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 19 | 8 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 9.0 | 86.2 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 19 | 8 | no | JST_SH top 8.22 > LID_Y 8 | -0.7 | -1.2 | 5.8 | 8.3 | 9.0 | 14.5 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 19 | 8.5 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 9.5 | 86.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 19 | 8.5 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 9.5 | 86.2 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 19 | 8.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 9.5 | 86.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 19 | 8.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 9.5 | 86.2 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 19 | 8.5 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 9.5 | 86.2 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 19 | 8.5 | no | module 13.00×18.00 at (9.50,28.60) outside the board | -0.7 | -1.2 | 5.8 | 8.3 | 9.5 | 14.5 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 19 | 9 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 10.0 | 86.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 19 | 9 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 10.0 | 86.2 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 19 | 9 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 10.0 | 86.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 19 | 9 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 10.0 | 86.2 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 19 | 9 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 10.0 | 86.2 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 19 | 9 | no | module 13.00×18.00 at (9.50,28.60) outside the board | -0.7 | -1.2 | 5.8 | 8.3 | 10.0 | 14.5 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 20 | 6 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 7.0 | 136.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 20 | 6 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 7.0 | 136.8 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 20 | 6 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 7.0 | 136.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 20 | 6 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 7.0 | 136.8 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 20 | 6 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 7.0 | 136.8 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 20 | 6 | no | module top 7.32 > LID_Y 6 | -0.7 | -1.2 | 5.8 | 8.3 | 7.0 | 18.6 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 20 | 6.5 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 7.5 | 136.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 20 | 6.5 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 7.5 | 136.8 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 20 | 6.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 7.5 | 136.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 20 | 6.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 7.5 | 136.8 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 20 | 6.5 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 7.5 | 136.8 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 20 | 6.5 | no | module top 7.32 > LID_Y 6.5 | -0.7 | -1.2 | 5.8 | 8.3 | 7.5 | 18.6 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 20 | 7 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 8.0 | 136.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 20 | 7 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 8.0 | 136.8 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 20 | 7 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 8.0 | 136.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 20 | 7 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 8.0 | 136.8 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 20 | 7 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 8.0 | 136.8 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 20 | 7 | no | module top 7.32 > LID_Y 7 | -0.7 | -1.2 | 5.8 | 8.3 | 8.0 | 18.6 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 20 | 8 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 9.0 | 136.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 20 | 8 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 9.0 | 136.8 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 20 | 8 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 9.0 | 136.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 20 | 8 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 9.0 | 136.8 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 20 | 8 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 9.0 | 136.8 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 20 | 8 | no | module 13.00×18.00 at (8.75,28.60) outside the board | -0.7 | -1.2 | 5.8 | 8.3 | 9.0 | 18.6 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 20 | 8.5 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 9.5 | 136.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 20 | 8.5 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 9.5 | 136.8 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 20 | 8.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 9.5 | 136.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 20 | 8.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 9.5 | 136.8 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 20 | 8.5 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 9.5 | 136.8 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 20 | 8.5 | no | module 13.00×18.00 at (8.75,28.60) outside the board | -0.7 | -1.2 | 5.8 | 8.3 | 9.5 | 18.6 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 20 | 9 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 10.0 | 136.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 20 | 9 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 10.0 | 136.8 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 20 | 9 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 10.0 | 136.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 20 | 9 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 10.0 | 136.8 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 20 | 9 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 10.0 | 136.8 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 20 | 9 | no | module 13.00×18.00 at (8.75,28.60) outside the board | -0.7 | -1.2 | 5.8 | 8.3 | 10.0 | 18.6 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 18 | 6 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 7.0 | 91.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 18 | 6 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 7.0 | 91.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 18 | 6 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 7.0 | 91.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 18 | 6 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 7.0 | 91.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 18 | 6 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 7.0 | 91.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 18 | 6 | no | module top 7.32 > LID_Y 6 | -0.7 | -1.2 | 5.8 | 8.3 | 7.0 | 97.1 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 18 | 6.5 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 7.5 | 91.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 18 | 6.5 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 7.5 | 91.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 18 | 6.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 7.5 | 91.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 18 | 6.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 7.5 | 91.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 18 | 6.5 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 7.5 | 91.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 18 | 6.5 | no | module top 7.32 > LID_Y 6.5 | -0.7 | -1.2 | 5.8 | 8.3 | 7.5 | 97.1 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 18 | 7 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 8.0 | 91.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 18 | 7 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 8.0 | 91.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 18 | 7 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 8.0 | 91.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 18 | 7 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 8.0 | 91.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 18 | 7 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 8.0 | 91.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 18 | 7 | no | module top 7.32 > LID_Y 7 | -0.7 | -1.2 | 5.8 | 8.3 | 8.0 | 97.1 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 18 | 8 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 9.0 | 91.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 18 | 8 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 9.0 | 91.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 18 | 8 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 9.0 | 91.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 18 | 8 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 9.0 | 91.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 18 | 8 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 9.0 | 91.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 18 | 8 | no | cell top 11.02 > LID_Y 8 | -0.7 | -1.2 | 5.8 | 8.3 | 9.0 | 97.1 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 18 | 8.5 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 9.5 | 91.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 18 | 8.5 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 9.5 | 91.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 18 | 8.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 9.5 | 91.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 18 | 8.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 9.5 | 91.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 18 | 8.5 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 9.5 | 91.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 18 | 8.5 | no | cell top 11.02 > LID_Y 8.5 | -0.7 | -1.2 | 5.8 | 8.3 | 9.5 | 97.1 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 18 | 9 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 10.0 | 91.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 18 | 9 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 10.0 | 91.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 18 | 9 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 10.0 | 91.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 18 | 9 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 10.0 | 91.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 18 | 9 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 10.0 | 91.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 18 | 9 | no | cell top 11.02 > LID_Y 9 | -0.7 | -1.2 | 5.8 | 8.3 | 10.0 | 97.1 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 19 | 6 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 7.0 | 127.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 19 | 6 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 7.0 | 127.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 19 | 6 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 7.0 | 127.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 19 | 6 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 7.0 | 127.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 19 | 6 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 7.0 | 127.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 19 | 6 | no | module top 7.32 > LID_Y 6 | -0.7 | -1.2 | 5.8 | 8.3 | 7.0 | 130.1 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 19 | 6.5 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 7.5 | 127.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 19 | 6.5 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 7.5 | 127.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 19 | 6.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 7.5 | 127.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 19 | 6.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 7.5 | 127.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 19 | 6.5 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 7.5 | 127.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 19 | 6.5 | no | module top 7.32 > LID_Y 6.5 | -0.7 | -1.2 | 5.8 | 8.3 | 7.5 | 130.1 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 19 | 7 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 8.0 | 127.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 19 | 7 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 8.0 | 127.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 19 | 7 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 8.0 | 127.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 19 | 7 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 8.0 | 127.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 19 | 7 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 8.0 | 127.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 19 | 7 | no | module top 7.32 > LID_Y 7 | -0.7 | -1.2 | 5.8 | 8.3 | 8.0 | 130.1 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 19 | 8 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 9.0 | 127.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 19 | 8 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 9.0 | 127.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 19 | 8 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 9.0 | 127.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 19 | 8 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 9.0 | 127.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 19 | 8 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 9.0 | 127.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 19 | 8 | no | cell top 11.02 > LID_Y 8 | -0.7 | -1.2 | 5.8 | 8.3 | 9.0 | 130.1 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 19 | 8.5 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 9.5 | 127.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 19 | 8.5 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 9.5 | 127.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 19 | 8.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 9.5 | 127.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 19 | 8.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 9.5 | 127.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 19 | 8.5 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 9.5 | 127.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 19 | 8.5 | no | cell top 11.02 > LID_Y 8.5 | -0.7 | -1.2 | 5.8 | 8.3 | 9.5 | 130.1 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 19 | 9 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 10.0 | 127.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 19 | 9 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 10.0 | 127.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 19 | 9 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 10.0 | 127.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 19 | 9 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 10.0 | 127.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 19 | 9 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 10.0 | 127.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 19 | 9 | no | cell top 11.02 > LID_Y 9 | -0.7 | -1.2 | 5.8 | 8.3 | 10.0 | 130.1 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 20 | 6 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 7.0 | 163.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 20 | 6 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 7.0 | 163.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 20 | 6 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 7.0 | 163.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 20 | 6 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 7.0 | 163.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 20 | 6 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 7.0 | 163.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 20 | 6 | no | module top 7.32 > LID_Y 6 | -0.7 | -1.2 | 5.8 | 8.3 | 7.0 | 153.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 20 | 6.5 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 7.5 | 163.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 20 | 6.5 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 7.5 | 163.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 20 | 6.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 7.5 | 163.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 20 | 6.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 7.5 | 163.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 20 | 6.5 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 7.5 | 163.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 20 | 6.5 | no | module top 7.32 > LID_Y 6.5 | -0.7 | -1.2 | 5.8 | 8.3 | 7.5 | 153.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 20 | 7 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 8.0 | 163.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 20 | 7 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 8.0 | 163.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 20 | 7 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 8.0 | 163.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 20 | 7 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 8.0 | 163.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 20 | 7 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 8.0 | 163.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 20 | 7 | no | module top 7.32 > LID_Y 7 | -0.7 | -1.2 | 5.8 | 8.3 | 8.0 | 153.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 20 | 8 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 9.0 | 163.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 20 | 8 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 9.0 | 163.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 20 | 8 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 9.0 | 163.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 20 | 8 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 9.0 | 163.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 20 | 8 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 9.0 | 163.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 20 | 8 | no | cell top 11.02 > LID_Y 8 | -0.7 | -1.2 | 5.8 | 8.3 | 9.0 | 153.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 20 | 8.5 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 9.5 | 163.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 20 | 8.5 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 9.5 | 163.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 20 | 8.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 9.5 | 163.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 20 | 8.5 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 9.5 | 163.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 20 | 8.5 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 9.5 | 163.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 20 | 8.5 | no | cell top 11.02 > LID_Y 8.5 | -0.7 | -1.2 | 5.8 | 8.3 | 9.5 | 153.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 20 | 9 | no | nominal cell clearance -0.7 is not positive (cell 3.7 under standoff 3) | -0.7 | -1.2 | 6.0 | 8.5 | 10.0 | 163.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 20 | 9 | no | nominal cell clearance -0.2 is not positive (cell 3.7 under standoff 3.5) | -0.2 | -0.7 | 6.5 | 9.0 | 10.0 | 163.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 20 | 9 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 7.0 | 9.5 | 10.0 | 163.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 20 | 9 | no | cell would carry board load (deformed clearance -0.2; bosses 0.5 below standoff tops) | +0.3 | -0.2 | 6.5 | 9.0 | 10.0 | 163.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 20 | 9 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +0.8 | +0.3 | 7.0 | 9.5 | 10.0 | 163.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 20 | 9 | no | cell top 11.02 > LID_Y 9 | -0.7 | -1.2 | 5.8 | 8.3 | 10.0 | 153.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 18 | 6 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 7.0 | 125.4 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 18 | 6 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 7.0 | 125.4 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 18 | 6 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 7.0 | 125.4 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 18 | 6 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 7.0 | 125.4 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 18 | 6 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 7.0 | 125.4 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 18 | 6 | no | module top 7.32 > LID_Y 6 | -2.7 | -3.2 | 5.8 | 8.3 | 7.0 | 12.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 18 | 6.5 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 7.5 | 125.4 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 18 | 6.5 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 7.5 | 125.4 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 18 | 6.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 7.5 | 125.4 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 18 | 6.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 7.5 | 125.4 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 18 | 6.5 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 7.5 | 125.4 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 18 | 6.5 | no | module top 7.32 > LID_Y 6.5 | -2.7 | -3.2 | 5.8 | 8.3 | 7.5 | 12.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 18 | 7 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 8.0 | 125.4 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 18 | 7 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 8.0 | 125.4 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 18 | 7 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 8.0 | 125.4 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 18 | 7 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 8.0 | 125.4 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 18 | 7 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 8.0 | 125.4 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 18 | 7 | no | module top 7.32 > LID_Y 7 | -2.7 | -3.2 | 5.8 | 8.3 | 8.0 | 12.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 18 | 8 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 9.0 | 125.4 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 18 | 8 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 9.0 | 125.4 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 18 | 8 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 9.0 | 125.4 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 18 | 8 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 9.0 | 125.4 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 18 | 8 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 9.0 | 125.4 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 18 | 8 | no | JST_SH top 8.22 > LID_Y 8 | -2.7 | -3.2 | 5.8 | 8.3 | 9.0 | 12.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 18 | 8.5 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 9.5 | 125.4 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 18 | 8.5 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 9.5 | 125.4 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 18 | 8.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 9.5 | 125.4 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 18 | 8.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 9.5 | 125.4 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 18 | 8.5 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 9.5 | 125.4 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 18 | 8.5 | no | module overlaps ADS1292_RSM | -2.7 | -3.2 | 5.8 | 8.3 | 9.5 | 12.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 18 | 9 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 10.0 | 125.4 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 18 | 9 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 10.0 | 125.4 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 18 | 9 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 10.0 | 125.4 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 18 | 9 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 10.0 | 125.4 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 18 | 9 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 10.0 | 125.4 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 18 | 9 | no | module overlaps ADS1292_RSM | -2.7 | -3.2 | 5.8 | 8.3 | 10.0 | 12.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 19 | 6 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 7.0 | 151.3 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 19 | 6 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 7.0 | 151.3 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 19 | 6 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 7.0 | 151.3 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 19 | 6 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 7.0 | 151.3 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 19 | 6 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 7.0 | 151.3 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 19 | 6 | no | module top 7.32 > LID_Y 6 | -2.7 | -3.2 | 5.8 | 8.3 | 7.0 | 28.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 19 | 6.5 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 7.5 | 151.3 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 19 | 6.5 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 7.5 | 151.3 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 19 | 6.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 7.5 | 151.3 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 19 | 6.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 7.5 | 151.3 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 19 | 6.5 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 7.5 | 151.3 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 19 | 6.5 | no | module top 7.32 > LID_Y 6.5 | -2.7 | -3.2 | 5.8 | 8.3 | 7.5 | 28.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 19 | 7 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 8.0 | 151.3 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 19 | 7 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 8.0 | 151.3 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 19 | 7 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 8.0 | 151.3 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 19 | 7 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 8.0 | 151.3 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 19 | 7 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 8.0 | 151.3 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 19 | 7 | no | module top 7.32 > LID_Y 7 | -2.7 | -3.2 | 5.8 | 8.3 | 8.0 | 28.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 19 | 8 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 9.0 | 151.3 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 19 | 8 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 9.0 | 151.3 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 19 | 8 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 9.0 | 151.3 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 19 | 8 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 9.0 | 151.3 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 19 | 8 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 9.0 | 151.3 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 19 | 8 | no | module overlaps ADS1292_RSM | -2.7 | -3.2 | 5.8 | 8.3 | 9.0 | 28.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 19 | 8.5 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 9.5 | 151.3 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 19 | 8.5 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 9.5 | 151.3 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 19 | 8.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 9.5 | 151.3 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 19 | 8.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 9.5 | 151.3 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 19 | 8.5 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 9.5 | 151.3 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 19 | 8.5 | no | module overlaps ADS1292_RSM | -2.7 | -3.2 | 5.8 | 8.3 | 9.5 | 28.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 19 | 9 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 10.0 | 151.3 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 19 | 9 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 10.0 | 151.3 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 19 | 9 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 10.0 | 151.3 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 19 | 9 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 10.0 | 151.3 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 19 | 9 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 10.0 | 151.3 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 19 | 9 | no | module overlaps ADS1292_RSM | -2.7 | -3.2 | 5.8 | 8.3 | 10.0 | 28.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 20 | 6 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 7.0 | 160.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 20 | 6 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 7.0 | 160.8 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 20 | 6 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 7.0 | 160.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 20 | 6 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 7.0 | 160.8 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 20 | 6 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 7.0 | 160.8 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 20 | 6 | no | module top 7.32 > LID_Y 6 | -2.7 | -3.2 | 5.8 | 8.3 | 7.0 | 35.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 20 | 6.5 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 7.5 | 160.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 20 | 6.5 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 7.5 | 160.8 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 20 | 6.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 7.5 | 160.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 20 | 6.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 7.5 | 160.8 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 20 | 6.5 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 7.5 | 160.8 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 20 | 6.5 | no | module top 7.32 > LID_Y 6.5 | -2.7 | -3.2 | 5.8 | 8.3 | 7.5 | 35.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 20 | 7 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 8.0 | 160.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 20 | 7 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 8.0 | 160.8 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 20 | 7 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 8.0 | 160.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 20 | 7 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 8.0 | 160.8 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 20 | 7 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 8.0 | 160.8 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 20 | 7 | no | module top 7.32 > LID_Y 7 | -2.7 | -3.2 | 5.8 | 8.3 | 8.0 | 35.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 20 | 8 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 9.0 | 160.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 20 | 8 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 9.0 | 160.8 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 20 | 8 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 9.0 | 160.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 20 | 8 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 9.0 | 160.8 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 20 | 8 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 9.0 | 160.8 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 20 | 8 | no | JST_SH top 8.22 > LID_Y 8 | -2.7 | -3.2 | 5.8 | 8.3 | 9.0 | 35.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 20 | 8.5 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 9.5 | 160.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 20 | 8.5 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 9.5 | 160.8 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 20 | 8.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 9.5 | 160.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 20 | 8.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 9.5 | 160.8 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 20 | 8.5 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 9.5 | 160.8 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 20 | 8.5 | no | module overlaps JST_SH | -2.7 | -3.2 | 5.8 | 8.3 | 9.5 | 35.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 20 | 9 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 10.0 | 160.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 20 | 9 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 10.0 | 160.8 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 20 | 9 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 10.0 | 160.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 20 | 9 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 10.0 | 160.8 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 20 | 9 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 10.0 | 160.8 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 20 | 9 | no | module overlaps JST_SH | -2.7 | -3.2 | 5.8 | 8.3 | 10.0 | 35.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 18 | 6 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 7.0 | 91.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 18 | 6 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 7.0 | 91.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 18 | 6 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 7.0 | 91.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 18 | 6 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 7.0 | 91.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 18 | 6 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 7.0 | 91.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 18 | 6 | no | module top 7.32 > LID_Y 6 | -2.7 | -3.2 | 5.8 | 8.3 | 7.0 | 91.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 18 | 6.5 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 7.5 | 91.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 18 | 6.5 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 7.5 | 91.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 18 | 6.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 7.5 | 91.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 18 | 6.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 7.5 | 91.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 18 | 6.5 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 7.5 | 91.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 18 | 6.5 | no | module top 7.32 > LID_Y 6.5 | -2.7 | -3.2 | 5.8 | 8.3 | 7.5 | 91.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 18 | 7 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 8.0 | 91.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 18 | 7 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 8.0 | 91.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 18 | 7 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 8.0 | 91.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 18 | 7 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 8.0 | 91.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 18 | 7 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 8.0 | 91.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 18 | 7 | no | module top 7.32 > LID_Y 7 | -2.7 | -3.2 | 5.8 | 8.3 | 8.0 | 91.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 18 | 8 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 9.0 | 91.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 18 | 8 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 9.0 | 91.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 18 | 8 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 9.0 | 91.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 18 | 8 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 9.0 | 91.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 18 | 8 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 9.0 | 91.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 18 | 8 | no | cell top 13.02 > LID_Y 8 | -2.7 | -3.2 | 5.8 | 8.3 | 9.0 | 91.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 18 | 8.5 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 9.5 | 91.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 18 | 8.5 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 9.5 | 91.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 18 | 8.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 9.5 | 91.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 18 | 8.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 9.5 | 91.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 18 | 8.5 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 9.5 | 91.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 18 | 8.5 | no | cell top 13.02 > LID_Y 8.5 | -2.7 | -3.2 | 5.8 | 8.3 | 9.5 | 91.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 18 | 9 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 10.0 | 91.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 18 | 9 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 10.0 | 91.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 18 | 9 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 10.0 | 91.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 18 | 9 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 10.0 | 91.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 18 | 9 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 10.0 | 91.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 18 | 9 | no | cell top 13.02 > LID_Y 9 | -2.7 | -3.2 | 5.8 | 8.3 | 10.0 | 91.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 19 | 6 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 7.0 | 127.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 19 | 6 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 7.0 | 127.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 19 | 6 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 7.0 | 127.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 19 | 6 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 7.0 | 127.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 19 | 6 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 7.0 | 127.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 19 | 6 | no | module top 7.32 > LID_Y 6 | -2.7 | -3.2 | 5.8 | 8.3 | 7.0 | 127.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 19 | 6.5 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 7.5 | 127.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 19 | 6.5 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 7.5 | 127.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 19 | 6.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 7.5 | 127.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 19 | 6.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 7.5 | 127.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 19 | 6.5 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 7.5 | 127.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 19 | 6.5 | no | module top 7.32 > LID_Y 6.5 | -2.7 | -3.2 | 5.8 | 8.3 | 7.5 | 127.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 19 | 7 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 8.0 | 127.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 19 | 7 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 8.0 | 127.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 19 | 7 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 8.0 | 127.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 19 | 7 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 8.0 | 127.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 19 | 7 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 8.0 | 127.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 19 | 7 | no | module top 7.32 > LID_Y 7 | -2.7 | -3.2 | 5.8 | 8.3 | 8.0 | 127.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 19 | 8 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 9.0 | 127.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 19 | 8 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 9.0 | 127.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 19 | 8 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 9.0 | 127.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 19 | 8 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 9.0 | 127.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 19 | 8 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 9.0 | 127.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 19 | 8 | no | cell top 13.02 > LID_Y 8 | -2.7 | -3.2 | 5.8 | 8.3 | 9.0 | 127.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 19 | 8.5 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 9.5 | 127.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 19 | 8.5 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 9.5 | 127.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 19 | 8.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 9.5 | 127.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 19 | 8.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 9.5 | 127.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 19 | 8.5 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 9.5 | 127.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 19 | 8.5 | no | cell top 13.02 > LID_Y 8.5 | -2.7 | -3.2 | 5.8 | 8.3 | 9.5 | 127.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 19 | 9 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 10.0 | 127.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 19 | 9 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 10.0 | 127.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 19 | 9 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 10.0 | 127.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 19 | 9 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 10.0 | 127.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 19 | 9 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 10.0 | 127.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 19 | 9 | no | cell top 13.02 > LID_Y 9 | -2.7 | -3.2 | 5.8 | 8.3 | 10.0 | 127.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 20 | 6 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 7.0 | 163.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 20 | 6 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 7.0 | 163.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 20 | 6 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 7.0 | 163.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 20 | 6 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 7.0 | 163.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 20 | 6 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 7.0 | 163.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 20 | 6 | no | module top 7.32 > LID_Y 6 | -2.7 | -3.2 | 5.8 | 8.3 | 7.0 | 163.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 20 | 6.5 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 7.5 | 163.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 20 | 6.5 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 7.5 | 163.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 20 | 6.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 7.5 | 163.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 20 | 6.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 7.5 | 163.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 20 | 6.5 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 7.5 | 163.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 20 | 6.5 | no | module top 7.32 > LID_Y 6.5 | -2.7 | -3.2 | 5.8 | 8.3 | 7.5 | 163.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 20 | 7 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 8.0 | 163.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 20 | 7 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 8.0 | 163.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 20 | 7 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 8.0 | 163.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 20 | 7 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 8.0 | 163.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 20 | 7 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 8.0 | 163.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 20 | 7 | no | module top 7.32 > LID_Y 7 | -2.7 | -3.2 | 5.8 | 8.3 | 8.0 | 163.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 20 | 8 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 9.0 | 163.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 20 | 8 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 9.0 | 163.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 20 | 8 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 9.0 | 163.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 20 | 8 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 9.0 | 163.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 20 | 8 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 9.0 | 163.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 20 | 8 | no | cell top 13.02 > LID_Y 8 | -2.7 | -3.2 | 5.8 | 8.3 | 9.0 | 163.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 20 | 8.5 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 9.5 | 163.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 20 | 8.5 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 9.5 | 163.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 20 | 8.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 9.5 | 163.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 20 | 8.5 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 9.5 | 163.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 20 | 8.5 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 9.5 | 163.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 20 | 8.5 | no | cell top 13.02 > LID_Y 8.5 | -2.7 | -3.2 | 5.8 | 8.3 | 9.5 | 163.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 20 | 9 | no | nominal cell clearance -2.7 is not positive (cell 5.7 under standoff 3) | -2.7 | -3.2 | 6.0 | 8.5 | 10.0 | 163.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 20 | 9 | no | nominal cell clearance -2.2 is not positive (cell 5.7 under standoff 3.5) | -2.2 | -2.7 | 6.5 | 9.0 | 10.0 | 163.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 20 | 9 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 4) | -1.7 | -2.2 | 7.0 | 9.5 | 10.0 | 163.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 20 | 9 | no | nominal cell clearance -1.7 is not positive (cell 5.7 under standoff 3.5 recess 0.5) | -1.7 | -2.2 | 6.5 | 9.0 | 10.0 | 163.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 20 | 9 | no | nominal cell clearance -1.2 is not positive (cell 5.7 under standoff 4 recess 0.5) | -1.2 | -1.7 | 7.0 | 9.5 | 10.0 | 163.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 20 | 9 | no | cell top 13.02 > LID_Y 9 | -2.7 | -3.2 | 5.8 | 8.3 | 10.0 | 163.9 | 47.90 | 50.90 |

## 2. Clearance, stack, and first-conflict families

Cell packed height = body + foam 0.5: DTP301120 3.2 + 0.5 = 3.7; 501015 5.2 + 0.5 = 5.7.
Foam 0.5 is plan v1 §5's number and the one the order-1 Stage B `CELL_envelope` measures on the solid. Plan v2 §3 says 0.3; this file and Stage B use one number (review r5, decision 57).
Nominal clearance = standoff − (packed − recess). The board underside is at the standoff top (rigid).
Deformed clearance = (standoff − 0.5) − (packed − recess). The board bends down onto the bosses.
The cell may lie under the board only with positive nominal clearance and must carry no load (positive deformed clearance). C15 for a 0.5 recess (web 1.0) is NOT_MEASURED.

| cell | standoff | recess | nom | def | under-board? | load? |
|---|---:|---:|---:|---:|---|---|
| dtp | 3 | 0 | -0.7 | -1.2 | no | carries load |
| dtp | 3 | 0.5 | -0.2 | -0.7 | no | carries load |
| dtp | 3.5 | 0 | -0.2 | -0.7 | no | carries load |
| dtp | 3.5 | 0.5 | +0.3 | -0.2 | yes | carries load |
| dtp | 4 | 0 | +0.3 | -0.2 | yes | carries load |
| dtp | 4 | 0.5 | +0.8 | +0.3 | yes | no load |
| 501015 | 3 | 0 | -2.7 | -3.2 | no | carries load |
| 501015 | 3 | 0.5 | -2.2 | -2.7 | no | carries load |
| 501015 | 3.5 | 0 | -2.2 | -2.7 | no | carries load |
| 501015 | 3.5 | 0.5 | -1.7 | -2.2 | no | carries load |
| 501015 | 4 | 0 | -1.7 | -2.2 | no | carries load |
| 501015 | 4 | 0.5 | -1.2 | -1.7 | no | carries load |

Positive deformed clearance: DTP301120 standoff 4 recess 0.5.

Module stack above the inner floor. Interface I: standoff + rigid board 1 + module. Interface II: ring 0.31 (PI 0.11 + FR4 0.2) + standoff + board 0.51 (PI 0.11 + FR4 0.4) + module. Outer at zero added clearance = 1.5 floor + stack + 1 lid.

| arch | iface | standoff | stack | outer0 | ≤ 9.0? |
|---|---|---:|---:|---:|---|
| A | I | 3 | 6.30 | 8.80 | yes |
| A | I | 3.5 | 6.80 | 9.30 | no |
| A | I | 4 | 7.30 | 9.80 | no |
| A | II | 3 | 6.12 | 8.62 | yes |
| A | II | 3.5 | 6.62 | 9.12 | no |
| A | II | 4 | 7.12 | 9.62 | no |
| B | I | 3 | 6.00 | 8.50 | yes |
| B | I | 3.5 | 6.50 | 9.00 | yes |
| B | I | 4 | 7.00 | 9.50 | no |
| B | II | 3 | 5.82 | 8.32 | yes |
| B | II | 3.5 | 6.32 | 8.82 | yes |
| B | II | 4 | 6.82 | 9.32 | no |

outer@lid in the run table is LID_Y + 1.0 (the candidate body at that lid). For the Stage B winner the module-to-lid gap is also probed on the solid (`V2_STACK`, §6).

Interface I (720 runs): 0 close.
Also in 720 of 720: pad_SIG1 8×8 at (5.90,22.00) is off the rigid board (u 2.25–15.75, s 1.80–37.90) (review r5 check).
Also in 720 of 720: pad_REF 8×8 at (8.50,43.00) is off the rigid board (u 2.25–15.75, s 1.80–37.90) (review r5 check).
Interface II (144 runs): 3 close: `A_501015_series_w20_y8_iII_s3`, `A_501015_series_w20_y8.5_iII_s3`, `A_501015_series_w20_y9_iII_s3`.

First-conflict families (numbers masked), failing runs:

| family | runs |
|---|---:|
| nominal cell clearance # is not positive (cell # under standoff #) | 360 |
| cell would carry board load (deformed clearance #; bosses # below standoff tops) | 144 |
| nominal cell clearance # is not positive (cell # under standoff # recess #) | 144 |
| module top # > LID_Y # | 72 |
| outer height # > # at zero added clearance (standoff #+board #+module #+floor #+lid #) | 72 |
| cell top # > LID_Y # | 36 |
| module #×# at (#,#) outside the board | 11 |
| module overlaps ADS#_RSM | 10 |
| JST_SH top # > LID_Y # | 7 |
| cell to antenna zone # < # mm | 3 |
| module overlaps JST_SH | 2 |

Adjustment region per site (Interface I, formula only): 4 − 2.9 − 0.3 = ±0.8 mm. NOT_MEASURED on the solid.

## 3. Plan v2 §4 rule, line by line

Rule (1) closes ≤ 9.0 high and 20 wide, checks on the built solid, TOTAL_CHORD ≤ M1−3.

3 layouts close in packing: `A_501015_series_w20_y8_iII_s3`, `A_501015_series_w20_y8.5_iII_s3`, `A_501015_series_w20_y9_iII_s3`. TOTAL_CHORD 47.90 ≤ 49.00 (M1 = 52 from default.toml; Q34 blank). USB-C: hook-end end face (fallback); the medial opening is not cut on the order-1 solid.
On the built solid (§6) `A_501015_series_w20_y8_iII_s3` still fails `V2_TAB_envelope`, `REF_WIRE_envelope`, so rule (1) is not met on the solid yet.
Architecture B does not close.
Architecture C does not close (out, plan v2 turn 02).
Interface I does not close.

Rule (2) parts orderable. The closer uses Raytac MDBT50Q-1MV2, cell 501015, ADS1292, BQ25100, TLV71330 (SOT-23-5), USBLC6-2SC6 and PESD5V0L1UL at the USB, JST-SH, USB-C 16-pin, a 4.5 × 4.5 × 1.6 recovery switch, a 7.6 × 2.5 × 2.5 bench header, brass M2.5 hex standoffs 5 AF, ISO 7380 M2.5×4 screws and a flex board with FR4 stiffeners. No BAV199 (board-v2.md: 220 kΩ series and the ADS1292's own input diodes). Page prices are NOT_MEASURED (no vendor contact).

Rule (3) fewest Rolf steps. Interface I would skip tabs (board on standoff tops). It does not close, so the only closers are Interface II (rings under the standoffs). No decision.

Rule (4) lowest page price. NOT_MEASURED.

Ties go to A. The only architecture that closes is A.

## 4. Smallest body per architecture

- **A**: packing-smallest `A_501015_series_w20_y8_iII_s3`. BODY_WIDTH 20, LID_Y 8, BODY_THICK 9, TOTAL_CHORD 47.90, USB wall: hook-end end face (fallback).
  It is the Stage B winner (`scripts/cad/params/stageb_v2.toml`).
- **B**: does not close.
- **C**: does not close.

## 5. Layout for the board lane (architectures that close)

Hand `A_501015_series_w20_y8_iII_s3` to the board lane. Interface II. Board 0.51 at parts (PI 0.11 + FR4 0.4), 0.31 at the rings (PI 0.11 + FR4 0.2).
Board zone u 2.25–17.75, s 18.60–37.60. Underside y 4.81 (the standoff tops), top y 5.32.

- Cell 501015 + foam 0.5 10.4 × 15.6 × 5.70, centre (7.00, 9.30), y 1.50–7.20 (floor).
- Module Raytac MDBT50Q-1MV2 15.5 × 10.5 × 2.30, centre (10.00, 32.35), y 5.32–7.62 (top), length along u.
- Antenna keep-out (no copper, every layer) u 2.25–6.05, s 26.15–38.55 (3.8 × 12.4; Raytac Spec K p.9/p.13, interface §6.3; height 2.3 plan v2 §3).
- ADS1292 VQFN-32 5 × 5 × 1.00, centre (4.90, 21.25), y 5.32–6.32 (top).
- BQ25100 2.1 × 1.4 × 0.50, centre (3.45, 24.85), y 5.32–5.82 (top).
- TLV71330 SOT-23-5 3.3 × 2.9 × 1.45, centre (9.45, 20.20), y 5.32–6.77 (top).
- USBLC6-2SC6 SOT-23-6 3.3 × 2.9 × 1.45, centre (14.05, 3.10), y 2.01–3.46 (pocket).
- PESD5V0L1UL 2.2 × 1 × 0.70, centre (13.50, 5.30), y 2.01–2.71 (pocket).
- JST-SH 4 × 6 × 2.90, centre (14.40, 9.15), y 2.01–4.91 (pocket).
- Recovery switch 4.5 × 4.5 × 1.60, centre (10.10, 24.20), y 5.32–6.92 (top).
- Bench header 2.5 × 7.6 × 2.50, centre (14.05, 22.60), y 5.32–7.82 (top).
- SWD test pads 1.0 × 1.0: (5.15, 24.65), (6.50, 24.65), (6.95, 26.00), (11.90, 19.25), (11.90, 20.60).
- USB-C 8.9 × 7.3 × 3.20, centre (10.00, -2.15), y 1.00–4.20 (top). It would cut the **hook-end end face (fallback)**. Recess 1, ligaments 1.5, plug volume 12 × 6.5 × 15. No decision.
- 25 of 25 0402 courtyards placed (4 on the board, 21 in the pocket).

Flex tabs (ring Ø5, hole Ø2.7, strip 2.5, bend R ≥ 1):
- SIG1: (5.90, 22.00) → (5.90, 29.00).
- SIG2: (10.40, 33.10) → (10.40, 26.10).
- REF: (8.50, 43.00) → (8.50, 36.80).

Stack at each site: floor 1.5, ring 0.31, brass standoff 3 (5 AF, circumradius 2.9) from y 1.81 to 4.81 = board underside. ISO 7380 M2.5×4 from outside projects 2.5 past the floor and ends 0.81 below the standoff top. No nut: the standoff's female thread takes the screw (plan v2 §5.3). The flex over the standoffs is not fastened to them; its retention is WP14's.
Harness 100 ± 3 mm: NOT_MEASURED (routed length, not a solid).

B and C do not close. There is no board-lane layout for them.

## 6. Winners sent to Stage B (at most six)

- `A_501015_series_w20_y8_iII_s3` — Stage B winner (`scripts/cad/params/stageb_v2.toml`)
- `A_501015_series_w20_y8.5_iII_s3`
- `A_501015_series_w20_y9_iII_s3`

Construction is the order-1 path with packing C (width 20, arc 48.4). No fork. Build (writes only into the temp dir; exit 3 = files written, not every check passed):

```bash
.venv/bin/python scripts/cad/bte_fit_shell.py --params scripts/cad/params/stageb_v2.toml --out /tmp/elicio-stageb-v2/
```

Measured on the built `A_501015_series_w20_y8_iII_s3` solid (review r5; `tests/test_cad.py` checks these rows against a fresh build):

| check | result | numbers |
|---|---|---|
| `V2_CELL_envelope` | pass | body_mm3 0, lid_mm3 0, y1 7.2 |
| `V2_MODULE_envelope` | pass | body_mm3 0, lid_mm3 0, y1 7.62 |
| `V2_BOARD_envelope` | pass | body_mm3 0, lid_mm3 0, underside 4.81, top 5.32 |
| `V2_TAB_envelope` | fail | REF_body_mm3 1.194, SIG1_body_mm3 0, SIG2_body_mm3 0; the floor-level REF tab crosses the cavity end wall (s 38.2 to the Ø7.5 pocket at 39.25); needs a slot in that wall (WP14, decision 59) |
| `REF_WIRE_envelope` | fail | body_mm3 1.1902, lid_mm3 0; same end-wall crossing |
| `V2_CONTACT_STACK` | pass | stack_top_y 4.81, board_underside 4.81, tip_below_top 0.81 |
| `V2_STANDOFF` | pass | standoff_SIG1_body_mm3 0, standoff_SIG2_body_mm3 0, standoff_REF_body_mm3 0 |
| `Q21_REF_lug` | pass | stack_top_y 4.81, pocket_r 3.75, standoff_circumr 2.9 |
| `V2_LID_band` | pass | lid_underside_y 8 |
| `V2_STACK` | pass | module_top_y 7.62, lid_over_module 8, module_lid_gap 0.38 |
| `V2_WALL_minima` | pass | anterior_wall 1.5, posterior_wall 1.5 |
| `V2_TOTAL_CHORD` | pass | TOTAL_CHORD 47.9005, packing_TOTAL_CHORD 47.9005 |
| `V2_M1_gate` | pass | gate 50.9005, M1 52 |
| `V2_CELL_CLEARANCE` | pass | cell_s1 17.1, board_s0 18.6; cell beside the board |
| `TAB_envelope_air` | NOT_MEASURED | the TE 31428 tab envelope is not the v2 flex tab; V2_TAB_envelope measures the tabs |
| `V2_ADJUSTMENT` | NOT_MEASURED | region_mm 0.8; ±0.8 is the Interface I pad/standoff formula, not a solid probe |
| `V2_BOSS` | NOT_MEASURED | Interface II has no board bosses; flex retention is WP14's and G7's |
| `V2_RECESS` | NOT_MEASURED | the 0.5 floor recess and 1.0 web (C15) are not on the order-1 solid |
| `V2_USB_medial` | NOT_MEASURED | the order-1 solid has no USB cut; packing reports the hook-end end face |
| `V2_HARNESS` | NOT_MEASURED | 100 ± 3 mm is a routed length |

## 7. Numbers taken as given

| Item | Number | Source |
|---|---|---|
| Raytac MDBT50Q-1MV2 | 10.5 × 15.5 × 2.3 | plan v2 §3 |
| Raytac MDBT50Q-1MV2 antenna keep-out | 12.4 × 3.8 | Raytac Spec K p.9/p.13, interface §6.3; height 2.3 plan v2 §3 |
| Ebyte E73-2G4M08S1C | 13 × 18 × 2 | plan v2 §3 |
| Ebyte E73-2G4M08S1C antenna keep-out | 12.4 × 3.8 | sheet unreachable; v1 rule interface §6.3 |
| Seeed XIAO nRF52840 | 17.5 × 21 × 4.5 | out, plan v2 turn 02 |
| Seeed XIAO nRF52840 antenna keep-out | 12.4 × 3.8 | sheet unreachable; v1 rule interface §6.3; C is out |
| DTP301120 | 22 × 11.5 × 3.2 | SparkFun PRT-25270 drawing p.9, L5-research-v2.md §1 |
| 501015 | 15.6 × 10.4 × 5.2 | v1 CELL_BODY_MAX (plan v1 §3.3) |
| Foam on the cell | 0.5 | plan v1 §5 and order-1 CELL_envelope; plan v2 §3 says 0.3 (decision 57) |
| Interface I board | FR4 1, 4-layer | plan v2 §5.2 |
| Interface I pad | 8 × 8 ENIG | turn 07 |
| Standoff | M2.5 hex 5 AF, circumradius 2.9, heights 3, 3.5, 4 | plan v2 §3; C14 |
| Boss drop | 0.5 | turn 07/09 |
| Cell floor recess | 0.5, web 1.0 | turn 09; C15 NOT_MEASURED |
| Placement tolerance | 0.3 | JLC printed floor ±0.3 |
| Flex board | PI 0.11 + FR4 0.4 = 0.51 at parts, PI 0.11 + FR4 0.2 = 0.31 at rings | JLC FPC stiffener list (0.1/0.2/0.4 …, no 0.3), read by WP12 2026-09-17 |
| ADS1292 VQFN-32 courtyard | 5 × 5 × 1 | WP11 brief |
| BQ25100 | 2.1 × 1.4 × 0.5 | WP11 brief |
| TLV71330 SOT-23-5 / USBLC6-2SC6 SOT-23-6 | 3.3 × 2.9 × 1.45 | board BOM; placement.py SOT-23 occupied area; TI DBV max height |
| PESD5V0L1UL | 2.2 × 1 × 0.7 | board land D_SOD-523 |
| Recovery switch | 4.5 × 4.5 × 1.6 | coordinator note 3 |
| Bench header | 7.6 × 2.5 × 2.5 | plan v2 §5.6 |
| USB-C 16-pin | 8.9 × 7.3 × 3.2 | WP11 brief |
| USB opening / recess / ligament | 9 × 3.5 / 1 / 1.5 | coordinator note 1 |
| Plug volume | 12 × 6.5 × 15 | plan v2 §5.4 |
| JST-SH | 4 × 6 × 2.9 side entry | WP11 brief |
| Ring pad | Ø5, hole Ø2.7, strip 2.5 | plan v2 §5.3 interface II |
| Screw ISO 7380 M2.5×4 | projects 2.5 past the floor | v1 |
| Harness | 100 ± 3 mm | plan v2; NOT_MEASURED as a solid |
| BODY_WIDTH / LID_Y / BODY_ARC | 18–20 / 6–9 / 48.4 | coordinator note 1; other params stageb_provisional.toml |
| M1 | 52 | default.toml; Q34 blank |
| Floor | 1.5 | v1 |

## 8. What could not be measured

- `TAB_envelope_air`: the TE 31428 tab envelope is not the v2 flex tab; V2_TAB_envelope measures the tabs
- `V2_ADJUSTMENT`: ±0.8 is the Interface I pad/standoff formula, not a solid probe
- `V2_BOSS`: Interface II has no board bosses; flex retention is WP14's and G7's
- `V2_RECESS`: the 0.5 floor recess and 1.0 web (C15) are not on the order-1 solid
- `V2_USB_medial`: the order-1 solid has no USB cut; packing reports the hook-end end face
- `V2_HARNESS`: 100 ± 3 mm is a routed length
- Nominal and deformed cell clearance for Interface I: packing arithmetic, not a solid probe. G5/G7 remain open.
- E73 antenna sheet: unreachable; v1 12.4 × 3.8 used.
- M1 on Rolf (Q34): default 52 used for the gate.

## 9. Drawings in the repo

Q56: the repo keeps only the drawings of the runs that close, the Stage B winner (`scripts/cad/params/stageb_v2.toml`) and the first run, in table order, of each first-conflict family (the first conflict with its numbers masked). `placement.py --all` writes the closers, `--kept-drawings` this set, and `--all-drawings --out-dir <tmp>` every run (never committed). All under `docs/fab/cad/v1/`.

| drawing | why kept |
|---|---|
| `placement_v2_A_501015_series_w20_y8_iII_s3.svg` | closes; Stage B winner |
| `placement_v2_A_501015_series_w20_y8.5_iII_s3.svg` | closes |
| `placement_v2_A_501015_series_w20_y9_iII_s3.svg` | closes |
| `placement_v2_A_dtp_series_w18_y6_iI_s3.svg` | family: nominal cell clearance # is not positive (cell # under standoff #) |
| `placement_v2_A_dtp_series_w18_y6_iI_s4.svg` | family: cell would carry board load (deformed clearance #; bosses # below standoff tops) |
| `placement_v2_A_dtp_series_w18_y6_iI_s4_r0.5.svg` | family: outer height # > # at zero added clearance (standoff #+board #+module #+floor #+lid #) |
| `placement_v2_A_dtp_series_w18_y6_iII_s3.svg` | family: module top # > LID_Y # |
| `placement_v2_A_dtp_series_w18_y8_iII_s3.svg` | family: JST_SH top # > LID_Y # |
| `placement_v2_A_dtp_series_w18_y8.5_iII_s3.svg` | family: module #×# at (#,#) outside the board |
| `placement_v2_A_dtp_series_w20_y8_iII_s3.svg` | family: cell to antenna zone # < # mm |
| `placement_v2_A_dtp_stacked_w18_y8_iII_s3.svg` | family: cell top # > LID_Y # |
| `placement_v2_A_501015_series_w18_y6_iI_s3.5_r0.5.svg` | family: nominal cell clearance # is not positive (cell # under standoff # recess #) |
| `placement_v2_A_501015_series_w18_y8.5_iII_s3.svg` | family: module overlaps ADS#_RSM |
| `placement_v2_B_501015_series_w20_y8.5_iII_s3.svg` | family: module overlaps JST_SH |

