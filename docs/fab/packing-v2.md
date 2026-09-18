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
| A | I | 3 | 0 | dtp | series | 18 | 6 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 7.0 | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 18 | 6 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 7.0 | 358.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 18 | 6 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 7.0 | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 18 | 6 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 7.0 | 358.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 18 | 6 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 7.0 | 358.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 18 | 6 | no | module top 6.70 > LID_Y 6 | -0.5 | -1.0 | 6.3 | 8.8 | 7.0 | 89.8 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 18 | 6.5 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 7.5 | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 18 | 6.5 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 7.5 | 358.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 18 | 6.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 7.5 | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 18 | 6.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 7.5 | 358.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 18 | 6.5 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 7.5 | 358.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 18 | 6.5 | no | module top 6.70 > LID_Y 6.5 | -0.5 | -1.0 | 6.3 | 8.8 | 7.5 | 89.8 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 18 | 7 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 8.0 | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 18 | 7 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 8.0 | 358.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 18 | 7 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 8.0 | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 18 | 7 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 8.0 | 358.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 18 | 7 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 8.0 | 358.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 18 | 7 | no | JST_SH top 7.30 > LID_Y 7 | -0.5 | -1.0 | 6.3 | 8.8 | 8.0 | 89.8 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 18 | 8 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 9.0 | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 18 | 8 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 9.0 | 358.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 18 | 8 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 9.0 | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 18 | 8 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 9.0 | 358.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 18 | 8 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 9.0 | 358.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 18 | 8 | no | module 10.50×15.50 at (7.50,29.85) outside the board | -0.5 | -1.0 | 6.3 | 8.8 | 9.0 | 89.8 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 18 | 8.5 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 9.5 | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 18 | 8.5 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 9.5 | 358.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 18 | 8.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 9.5 | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 18 | 8.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 9.5 | 358.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 18 | 8.5 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 9.5 | 358.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 18 | 8.5 | no | module 10.50×15.50 at (7.50,29.85) outside the board | -0.5 | -1.0 | 6.3 | 8.8 | 9.5 | 89.8 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 18 | 9 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 10.0 | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 18 | 9 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 10.0 | 358.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 18 | 9 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 10.0 | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 18 | 9 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 10.0 | 358.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 18 | 9 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 10.0 | 358.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 18 | 9 | no | module 10.50×15.50 at (7.50,29.85) outside the board | -0.5 | -1.0 | 6.3 | 8.8 | 10.0 | 89.8 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 19 | 6 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 7.0 | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 19 | 6 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 7.0 | 394.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 19 | 6 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 7.0 | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 19 | 6 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 7.0 | 394.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 19 | 6 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 7.0 | 394.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 19 | 6 | no | module top 6.70 > LID_Y 6 | -0.5 | -1.0 | 6.3 | 8.8 | 7.0 | 102.3 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 19 | 6.5 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 7.5 | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 19 | 6.5 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 7.5 | 394.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 19 | 6.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 7.5 | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 19 | 6.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 7.5 | 394.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 19 | 6.5 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 7.5 | 394.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 19 | 6.5 | no | module top 6.70 > LID_Y 6.5 | -0.5 | -1.0 | 6.3 | 8.8 | 7.5 | 102.3 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 19 | 7 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 8.0 | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 19 | 7 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 8.0 | 394.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 19 | 7 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 8.0 | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 19 | 7 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 8.0 | 394.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 19 | 7 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 8.0 | 394.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 19 | 7 | no | JST_SH top 7.30 > LID_Y 7 | -0.5 | -1.0 | 6.3 | 8.8 | 8.0 | 102.3 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 19 | 8 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 9.0 | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 19 | 8 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 9.0 | 394.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 19 | 8 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 9.0 | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 19 | 8 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 9.0 | 394.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 19 | 8 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 9.0 | 394.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 19 | 8 | no | module 10.50×15.50 at (7.50,29.85) outside the board | -0.5 | -1.0 | 6.3 | 8.8 | 9.0 | 102.3 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 19 | 8.5 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 9.5 | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 19 | 8.5 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 9.5 | 394.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 19 | 8.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 9.5 | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 19 | 8.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 9.5 | 394.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 19 | 8.5 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 9.5 | 394.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 19 | 8.5 | no | module 10.50×15.50 at (7.50,29.85) outside the board | -0.5 | -1.0 | 6.3 | 8.8 | 9.5 | 102.3 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 19 | 9 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 10.0 | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 19 | 9 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 10.0 | 394.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 19 | 9 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 10.0 | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 19 | 9 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 10.0 | 394.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 19 | 9 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 10.0 | 394.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 19 | 9 | no | module 10.50×15.50 at (7.50,29.85) outside the board | -0.5 | -1.0 | 6.3 | 8.8 | 10.0 | 102.3 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 20 | 6 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 7.0 | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 20 | 6 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 7.0 | 426.9 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 20 | 6 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 7.0 | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 20 | 6 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 7.0 | 426.9 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 20 | 6 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 7.0 | 426.9 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 20 | 6 | no | module top 6.70 > LID_Y 6 | -0.5 | -1.0 | 6.3 | 8.8 | 7.0 | 111.8 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 20 | 6.5 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 7.5 | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 20 | 6.5 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 7.5 | 426.9 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 20 | 6.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 7.5 | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 20 | 6.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 7.5 | 426.9 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 20 | 6.5 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 7.5 | 426.9 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 20 | 6.5 | no | module top 6.70 > LID_Y 6.5 | -0.5 | -1.0 | 6.3 | 8.8 | 7.5 | 111.8 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 20 | 7 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 8.0 | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 20 | 7 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 8.0 | 426.9 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 20 | 7 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 8.0 | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 20 | 7 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 8.0 | 426.9 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 20 | 7 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 8.0 | 426.9 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 20 | 7 | no | module overlaps ADS1292_RSM | -0.5 | -1.0 | 6.3 | 8.8 | 8.0 | 111.8 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 20 | 8 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 9.0 | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 20 | 8 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 9.0 | 426.9 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 20 | 8 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 9.0 | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 20 | 8 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 9.0 | 426.9 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 20 | 8 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 9.0 | 426.9 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 20 | 8 | no | module overlaps ADS1292_RSM | -0.5 | -1.0 | 6.3 | 8.8 | 9.0 | 111.8 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 20 | 8.5 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 9.5 | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 20 | 8.5 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 9.5 | 426.9 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 20 | 8.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 9.5 | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 20 | 8.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 9.5 | 426.9 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 20 | 8.5 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 9.5 | 426.9 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 20 | 8.5 | no | module overlaps ADS1292_RSM | -0.5 | -1.0 | 6.3 | 8.8 | 9.5 | 111.8 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | series | 20 | 9 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 10.0 | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | series | 20 | 9 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 10.0 | 426.9 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | series | 20 | 9 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 10.0 | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | series | 20 | 9 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 10.0 | 426.9 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | series | 20 | 9 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 10.0 | 426.9 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | series | 20 | 9 | no | module overlaps ADS1292_RSM | -0.5 | -1.0 | 6.3 | 8.8 | 10.0 | 111.8 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 18 | 6 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 7.0 | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 18 | 6 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 7.0 | 337.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 18 | 6 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 7.0 | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 18 | 6 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 7.0 | 337.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 18 | 6 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 7.0 | 337.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 18 | 6 | no | cell top 7.70 > LID_Y 6 | -0.5 | -1.0 | 6.3 | 8.8 | 7.0 | 337.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 18 | 6.5 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 7.5 | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 18 | 6.5 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 7.5 | 337.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 18 | 6.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 7.5 | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 18 | 6.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 7.5 | 337.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 18 | 6.5 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 7.5 | 337.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 18 | 6.5 | no | cell top 7.70 > LID_Y 6.5 | -0.5 | -1.0 | 6.3 | 8.8 | 7.5 | 337.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 18 | 7 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 8.0 | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 18 | 7 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 8.0 | 337.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 18 | 7 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 8.0 | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 18 | 7 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 8.0 | 337.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 18 | 7 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 8.0 | 337.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 18 | 7 | no | cell top 7.70 > LID_Y 7 | -0.5 | -1.0 | 6.3 | 8.8 | 8.0 | 337.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 18 | 8 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 9.0 | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 18 | 8 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 9.0 | 337.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 18 | 8 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 9.0 | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 18 | 8 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 9.0 | 337.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 18 | 8 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 9.0 | 337.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 18 | 8 | no | JST_SH enters SIG1 keep-out + 0.5 | -0.5 | -1.0 | 6.3 | 8.8 | 9.0 | 337.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 18 | 8.5 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 9.5 | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 18 | 8.5 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 9.5 | 337.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 18 | 8.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 9.5 | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 18 | 8.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 9.5 | 337.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 18 | 8.5 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 9.5 | 337.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 18 | 8.5 | no | JST_SH enters SIG1 keep-out + 0.5 | -0.5 | -1.0 | 6.3 | 8.8 | 9.5 | 337.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 18 | 9 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 10.0 | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 18 | 9 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 10.0 | 337.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 18 | 9 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 10.0 | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 18 | 9 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 10.0 | 337.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 18 | 9 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 10.0 | 337.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 18 | 9 | no | JST_SH enters SIG1 keep-out + 0.5 | -0.5 | -1.0 | 6.3 | 8.8 | 10.0 | 337.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 19 | 6 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 7.0 | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 19 | 6 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 7.0 | 373.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 19 | 6 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 7.0 | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 19 | 6 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 7.0 | 373.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 19 | 6 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 7.0 | 373.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 19 | 6 | no | cell top 7.70 > LID_Y 6 | -0.5 | -1.0 | 6.3 | 8.8 | 7.0 | 373.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 19 | 6.5 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 7.5 | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 19 | 6.5 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 7.5 | 373.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 19 | 6.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 7.5 | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 19 | 6.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 7.5 | 373.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 19 | 6.5 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 7.5 | 373.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 19 | 6.5 | no | cell top 7.70 > LID_Y 6.5 | -0.5 | -1.0 | 6.3 | 8.8 | 7.5 | 373.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 19 | 7 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 8.0 | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 19 | 7 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 8.0 | 373.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 19 | 7 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 8.0 | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 19 | 7 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 8.0 | 373.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 19 | 7 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 8.0 | 373.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 19 | 7 | no | cell top 7.70 > LID_Y 7 | -0.5 | -1.0 | 6.3 | 8.8 | 8.0 | 373.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 19 | 8 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 9.0 | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 19 | 8 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 9.0 | 373.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 19 | 8 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 9.0 | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 19 | 8 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 9.0 | 373.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 19 | 8 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 9.0 | 373.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 19 | 8 | no | JST_SH enters SIG1 keep-out + 0.5 | -0.5 | -1.0 | 6.3 | 8.8 | 9.0 | 373.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 19 | 8.5 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 9.5 | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 19 | 8.5 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 9.5 | 373.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 19 | 8.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 9.5 | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 19 | 8.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 9.5 | 373.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 19 | 8.5 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 9.5 | 373.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 19 | 8.5 | no | JST_SH enters SIG1 keep-out + 0.5 | -0.5 | -1.0 | 6.3 | 8.8 | 9.5 | 373.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 19 | 9 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 10.0 | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 19 | 9 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 10.0 | 373.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 19 | 9 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 10.0 | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 19 | 9 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 10.0 | 373.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 19 | 9 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 10.0 | 373.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 19 | 9 | no | JST_SH enters SIG1 keep-out + 0.5 | -0.5 | -1.0 | 6.3 | 8.8 | 10.0 | 373.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 20 | 6 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 7.0 | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 20 | 6 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 7.0 | 405.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 20 | 6 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 7.0 | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 20 | 6 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 7.0 | 405.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 20 | 6 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 7.0 | 405.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 20 | 6 | no | cell top 7.70 > LID_Y 6 | -0.5 | -1.0 | 6.3 | 8.8 | 7.0 | 405.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 20 | 6.5 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 7.5 | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 20 | 6.5 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 7.5 | 405.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 20 | 6.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 7.5 | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 20 | 6.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 7.5 | 405.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 20 | 6.5 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 7.5 | 405.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 20 | 6.5 | no | cell top 7.70 > LID_Y 6.5 | -0.5 | -1.0 | 6.3 | 8.8 | 7.5 | 405.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 20 | 7 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 8.0 | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 20 | 7 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 8.0 | 405.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 20 | 7 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 8.0 | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 20 | 7 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 8.0 | 405.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 20 | 7 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 8.0 | 405.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 20 | 7 | no | cell top 7.70 > LID_Y 7 | -0.5 | -1.0 | 6.3 | 8.8 | 8.0 | 405.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 20 | 8 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 9.0 | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 20 | 8 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 9.0 | 405.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 20 | 8 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 9.0 | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 20 | 8 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 9.0 | 405.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 20 | 8 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 9.0 | 405.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 20 | 8 | no | JST_SH enters SIG1 keep-out + 0.5 | -0.5 | -1.0 | 6.3 | 8.8 | 9.0 | 405.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 20 | 8.5 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 9.5 | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 20 | 8.5 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 9.5 | 405.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 20 | 8.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 9.5 | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 20 | 8.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 9.5 | 405.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 20 | 8.5 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 9.5 | 405.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 20 | 8.5 | no | JST_SH enters SIG1 keep-out + 0.5 | -0.5 | -1.0 | 6.3 | 8.8 | 9.5 | 405.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | dtp | stacked | 20 | 9 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.3 | 8.8 | 10.0 | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | dtp | stacked | 20 | 9 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.8 | 9.3 | 10.0 | 405.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | dtp | stacked | 20 | 9 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.3 | 9.8 | 10.0 | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | dtp | stacked | 20 | 9 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.8 | 9.3 | 10.0 | 405.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | dtp | stacked | 20 | 9 | no | outer height 9.8 > 9.0 at zero added clearance (standoff 4+board 1+module 2.3+floor 1.5+lid 1) | +1.0 | +0.5 | 7.3 | 9.8 | 10.0 | 405.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | dtp | stacked | 20 | 9 | no | JST_SH enters SIG1 keep-out + 0.5 | -0.5 | -1.0 | 6.3 | 8.8 | 10.0 | 405.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 18 | 6 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 7.0 | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 18 | 6 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 7.0 | 358.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 18 | 6 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 7.0 | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 18 | 6 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 7.0 | 358.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 18 | 6 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 7.0 | 358.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 18 | 6 | no | module top 6.70 > LID_Y 6 | -2.5 | -3.0 | 6.3 | 8.8 | 7.0 | 132.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 18 | 6.5 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 7.5 | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 18 | 6.5 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 7.5 | 358.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 18 | 6.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 7.5 | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 18 | 6.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 7.5 | 358.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 18 | 6.5 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 7.5 | 358.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 18 | 6.5 | no | module top 6.70 > LID_Y 6.5 | -2.5 | -3.0 | 6.3 | 8.8 | 7.5 | 132.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 18 | 7 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 8.0 | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 18 | 7 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 8.0 | 358.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 18 | 7 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 8.0 | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 18 | 7 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 8.0 | 358.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 18 | 7 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 8.0 | 358.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 18 | 7 | no | JST_SH top 7.30 > LID_Y 7 | -2.5 | -3.0 | 6.3 | 8.8 | 8.0 | 132.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 18 | 8 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 9.0 | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 18 | 8 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 9.0 | 358.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 18 | 8 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 9.0 | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 18 | 8 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 9.0 | 358.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 18 | 8 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 9.0 | 358.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 18 | 8 | no | SWD_4 in the antenna keep-out | -2.5 | -3.0 | 6.3 | 8.8 | 9.0 | 132.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 18 | 8.5 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 9.5 | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 18 | 8.5 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 9.5 | 358.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 18 | 8.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 9.5 | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 18 | 8.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 9.5 | 358.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 18 | 8.5 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 9.5 | 358.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 18 | 8.5 | no | SWD_4 in the antenna keep-out | -2.5 | -3.0 | 6.3 | 8.8 | 9.5 | 132.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 18 | 9 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 10.0 | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 18 | 9 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 10.0 | 358.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 18 | 9 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 10.0 | 358.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 18 | 9 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 10.0 | 358.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 18 | 9 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 10.0 | 358.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 18 | 9 | no | SWD_4 in the antenna keep-out | -2.5 | -3.0 | 6.3 | 8.8 | 10.0 | 132.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 19 | 6 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 7.0 | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 19 | 6 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 7.0 | 394.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 19 | 6 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 7.0 | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 19 | 6 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 7.0 | 394.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 19 | 6 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 7.0 | 394.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 19 | 6 | no | module top 6.70 > LID_Y 6 | -2.5 | -3.0 | 6.3 | 8.8 | 7.0 | 151.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 19 | 6.5 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 7.5 | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 19 | 6.5 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 7.5 | 394.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 19 | 6.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 7.5 | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 19 | 6.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 7.5 | 394.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 19 | 6.5 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 7.5 | 394.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 19 | 6.5 | no | module top 6.70 > LID_Y 6.5 | -2.5 | -3.0 | 6.3 | 8.8 | 7.5 | 151.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 19 | 7 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 8.0 | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 19 | 7 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 8.0 | 394.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 19 | 7 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 8.0 | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 19 | 7 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 8.0 | 394.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 19 | 7 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 8.0 | 394.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 19 | 7 | no | module overlaps ADS1292_RSM | -2.5 | -3.0 | 6.3 | 8.8 | 8.0 | 151.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 19 | 8 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 9.0 | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 19 | 8 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 9.0 | 394.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 19 | 8 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 9.0 | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 19 | 8 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 9.0 | 394.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 19 | 8 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 9.0 | 394.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 19 | 8 | no | module overlaps ADS1292_RSM | -2.5 | -3.0 | 6.3 | 8.8 | 9.0 | 151.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 19 | 8.5 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 9.5 | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 19 | 8.5 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 9.5 | 394.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 19 | 8.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 9.5 | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 19 | 8.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 9.5 | 394.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 19 | 8.5 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 9.5 | 394.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 19 | 8.5 | no | module overlaps ADS1292_RSM | -2.5 | -3.0 | 6.3 | 8.8 | 9.5 | 151.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 19 | 9 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 10.0 | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 19 | 9 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 10.0 | 394.1 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 19 | 9 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 10.0 | 394.1 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 19 | 9 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 10.0 | 394.1 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 19 | 9 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 10.0 | 394.1 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 19 | 9 | no | module overlaps ADS1292_RSM | -2.5 | -3.0 | 6.3 | 8.8 | 10.0 | 151.1 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 20 | 6 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 7.0 | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 20 | 6 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 7.0 | 426.9 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 20 | 6 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 7.0 | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 20 | 6 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 7.0 | 426.9 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 20 | 6 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 7.0 | 426.9 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 20 | 6 | no | module top 6.70 > LID_Y 6 | -2.5 | -3.0 | 6.3 | 8.8 | 7.0 | 166.8 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 20 | 6.5 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 7.5 | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 20 | 6.5 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 7.5 | 426.9 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 20 | 6.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 7.5 | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 20 | 6.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 7.5 | 426.9 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 20 | 6.5 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 7.5 | 426.9 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 20 | 6.5 | no | module top 6.70 > LID_Y 6.5 | -2.5 | -3.0 | 6.3 | 8.8 | 7.5 | 166.8 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 20 | 7 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 8.0 | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 20 | 7 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 8.0 | 426.9 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 20 | 7 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 8.0 | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 20 | 7 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 8.0 | 426.9 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 20 | 7 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 8.0 | 426.9 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 20 | 7 | yes | — | -2.5 | -3.0 | 6.3 | 8.8 | 8.0 | 166.8 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 20 | 8 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 9.0 | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 20 | 8 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 9.0 | 426.9 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 20 | 8 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 9.0 | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 20 | 8 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 9.0 | 426.9 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 20 | 8 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 9.0 | 426.9 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 20 | 8 | yes | — | -2.5 | -3.0 | 6.3 | 8.8 | 9.0 | 166.8 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 20 | 8.5 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 9.5 | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 20 | 8.5 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 9.5 | 426.9 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 20 | 8.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 9.5 | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 20 | 8.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 9.5 | 426.9 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 20 | 8.5 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 9.5 | 426.9 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 20 | 8.5 | yes | — | -2.5 | -3.0 | 6.3 | 8.8 | 9.5 | 166.8 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | series | 20 | 9 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 10.0 | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | series | 20 | 9 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 10.0 | 426.9 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | series | 20 | 9 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 10.0 | 426.9 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | series | 20 | 9 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 10.0 | 426.9 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | series | 20 | 9 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 10.0 | 426.9 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | series | 20 | 9 | yes | — | -2.5 | -3.0 | 6.3 | 8.8 | 10.0 | 166.8 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 18 | 6 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 7.0 | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 18 | 6 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 7.0 | 337.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 18 | 6 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 7.0 | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 18 | 6 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 7.0 | 337.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 18 | 6 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 7.0 | 337.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 18 | 6 | no | cell top 9.70 > LID_Y 6 | -2.5 | -3.0 | 6.3 | 8.8 | 7.0 | 337.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 18 | 6.5 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 7.5 | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 18 | 6.5 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 7.5 | 337.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 18 | 6.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 7.5 | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 18 | 6.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 7.5 | 337.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 18 | 6.5 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 7.5 | 337.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 18 | 6.5 | no | cell top 9.70 > LID_Y 6.5 | -2.5 | -3.0 | 6.3 | 8.8 | 7.5 | 337.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 18 | 7 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 8.0 | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 18 | 7 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 8.0 | 337.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 18 | 7 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 8.0 | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 18 | 7 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 8.0 | 337.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 18 | 7 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 8.0 | 337.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 18 | 7 | no | cell top 9.70 > LID_Y 7 | -2.5 | -3.0 | 6.3 | 8.8 | 8.0 | 337.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 18 | 8 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 9.0 | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 18 | 8 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 9.0 | 337.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 18 | 8 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 9.0 | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 18 | 8 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 9.0 | 337.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 18 | 8 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 9.0 | 337.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 18 | 8 | no | cell top 9.70 > LID_Y 8 | -2.5 | -3.0 | 6.3 | 8.8 | 9.0 | 337.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 18 | 8.5 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 9.5 | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 18 | 8.5 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 9.5 | 337.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 18 | 8.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 9.5 | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 18 | 8.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 9.5 | 337.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 18 | 8.5 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 9.5 | 337.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 18 | 8.5 | no | cell top 9.70 > LID_Y 8.5 | -2.5 | -3.0 | 6.3 | 8.8 | 9.5 | 337.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 18 | 9 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 10.0 | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 18 | 9 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 10.0 | 337.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 18 | 9 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 10.0 | 337.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 18 | 9 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 10.0 | 337.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 18 | 9 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 10.0 | 337.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 18 | 9 | no | cell top 9.70 > LID_Y 9 | -2.5 | -3.0 | 6.3 | 8.8 | 10.0 | 337.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 19 | 6 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 7.0 | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 19 | 6 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 7.0 | 373.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 19 | 6 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 7.0 | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 19 | 6 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 7.0 | 373.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 19 | 6 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 7.0 | 373.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 19 | 6 | no | cell top 9.70 > LID_Y 6 | -2.5 | -3.0 | 6.3 | 8.8 | 7.0 | 373.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 19 | 6.5 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 7.5 | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 19 | 6.5 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 7.5 | 373.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 19 | 6.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 7.5 | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 19 | 6.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 7.5 | 373.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 19 | 6.5 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 7.5 | 373.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 19 | 6.5 | no | cell top 9.70 > LID_Y 6.5 | -2.5 | -3.0 | 6.3 | 8.8 | 7.5 | 373.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 19 | 7 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 8.0 | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 19 | 7 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 8.0 | 373.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 19 | 7 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 8.0 | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 19 | 7 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 8.0 | 373.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 19 | 7 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 8.0 | 373.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 19 | 7 | no | cell top 9.70 > LID_Y 7 | -2.5 | -3.0 | 6.3 | 8.8 | 8.0 | 373.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 19 | 8 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 9.0 | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 19 | 8 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 9.0 | 373.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 19 | 8 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 9.0 | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 19 | 8 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 9.0 | 373.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 19 | 8 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 9.0 | 373.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 19 | 8 | no | cell top 9.70 > LID_Y 8 | -2.5 | -3.0 | 6.3 | 8.8 | 9.0 | 373.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 19 | 8.5 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 9.5 | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 19 | 8.5 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 9.5 | 373.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 19 | 8.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 9.5 | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 19 | 8.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 9.5 | 373.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 19 | 8.5 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 9.5 | 373.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 19 | 8.5 | no | cell top 9.70 > LID_Y 8.5 | -2.5 | -3.0 | 6.3 | 8.8 | 9.5 | 373.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 19 | 9 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 10.0 | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 19 | 9 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 10.0 | 373.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 19 | 9 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 10.0 | 373.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 19 | 9 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 10.0 | 373.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 19 | 9 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 10.0 | 373.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 19 | 9 | no | cell top 9.70 > LID_Y 9 | -2.5 | -3.0 | 6.3 | 8.8 | 10.0 | 373.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 20 | 6 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 7.0 | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 20 | 6 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 7.0 | 405.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 20 | 6 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 7.0 | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 20 | 6 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 7.0 | 405.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 20 | 6 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 7.0 | 405.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 20 | 6 | no | cell top 9.70 > LID_Y 6 | -2.5 | -3.0 | 6.3 | 8.8 | 7.0 | 405.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 20 | 6.5 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 7.5 | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 20 | 6.5 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 7.5 | 405.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 20 | 6.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 7.5 | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 20 | 6.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 7.5 | 405.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 20 | 6.5 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 7.5 | 405.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 20 | 6.5 | no | cell top 9.70 > LID_Y 6.5 | -2.5 | -3.0 | 6.3 | 8.8 | 7.5 | 405.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 20 | 7 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 8.0 | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 20 | 7 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 8.0 | 405.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 20 | 7 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 8.0 | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 20 | 7 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 8.0 | 405.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 20 | 7 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 8.0 | 405.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 20 | 7 | no | cell top 9.70 > LID_Y 7 | -2.5 | -3.0 | 6.3 | 8.8 | 8.0 | 405.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 20 | 8 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 9.0 | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 20 | 8 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 9.0 | 405.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 20 | 8 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 9.0 | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 20 | 8 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 9.0 | 405.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 20 | 8 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 9.0 | 405.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 20 | 8 | no | cell top 9.70 > LID_Y 8 | -2.5 | -3.0 | 6.3 | 8.8 | 9.0 | 405.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 20 | 8.5 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 9.5 | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 20 | 8.5 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 9.5 | 405.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 20 | 8.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 9.5 | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 20 | 8.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 9.5 | 405.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 20 | 8.5 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 9.5 | 405.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 20 | 8.5 | no | cell top 9.70 > LID_Y 8.5 | -2.5 | -3.0 | 6.3 | 8.8 | 9.5 | 405.6 | 47.90 | 50.90 |
| A | I | 3 | 0 | 501015 | stacked | 20 | 9 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.3 | 8.8 | 10.0 | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0 | 501015 | stacked | 20 | 9 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.8 | 9.3 | 10.0 | 405.6 | 47.90 | 50.90 |
| A | I | 4 | 0 | 501015 | stacked | 20 | 9 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.3 | 9.8 | 10.0 | 405.6 | 47.90 | 50.90 |
| A | I | 3.5 | 0.5 | 501015 | stacked | 20 | 9 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.8 | 9.3 | 10.0 | 405.6 | 47.90 | 50.90 |
| A | I | 4 | 0.5 | 501015 | stacked | 20 | 9 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.3 | 9.8 | 10.0 | 405.6 | 47.90 | 50.90 |
| A | II | 3 | 0 | 501015 | stacked | 20 | 9 | no | cell top 9.70 > LID_Y 9 | -2.5 | -3.0 | 6.3 | 8.8 | 10.0 | 405.6 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 18 | 6 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 7.0 | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 18 | 6 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 7.0 | 354.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 18 | 6 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 7.0 | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 18 | 6 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 7.0 | 354.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 18 | 6 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 7.0 | 354.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 18 | 6 | no | module top 6.40 > LID_Y 6 | -0.5 | -1.0 | 6.0 | 8.5 | 7.0 | 86.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 18 | 6.5 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 7.5 | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 18 | 6.5 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 7.5 | 354.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 18 | 6.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 7.5 | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 18 | 6.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 7.5 | 354.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 18 | 6.5 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 7.5 | 354.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 18 | 6.5 | no | JST_SH top 7.30 > LID_Y 6.5 | -0.5 | -1.0 | 6.0 | 8.5 | 7.5 | 86.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 18 | 7 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 8.0 | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 18 | 7 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 8.0 | 354.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 18 | 7 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 8.0 | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 18 | 7 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 8.0 | 354.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 18 | 7 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 8.0 | 354.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 18 | 7 | no | JST_SH top 7.30 > LID_Y 7 | -0.5 | -1.0 | 6.0 | 8.5 | 8.0 | 86.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 18 | 8 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 9.0 | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 18 | 8 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 9.0 | 354.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 18 | 8 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 9.0 | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 18 | 8 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 9.0 | 354.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 18 | 8 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 9.0 | 354.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 18 | 8 | no | module 13.00×18.00 at (9.00,28.60) outside the board | -0.5 | -1.0 | 6.0 | 8.5 | 9.0 | 86.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 18 | 8.5 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 9.5 | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 18 | 8.5 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 9.5 | 354.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 18 | 8.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 9.5 | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 18 | 8.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 9.5 | 354.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 18 | 8.5 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 9.5 | 354.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 18 | 8.5 | no | module 13.00×18.00 at (9.00,28.60) outside the board | -0.5 | -1.0 | 6.0 | 8.5 | 9.5 | 86.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 18 | 9 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 10.0 | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 18 | 9 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 10.0 | 354.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 18 | 9 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 10.0 | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 18 | 9 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 10.0 | 354.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 18 | 9 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 10.0 | 354.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 18 | 9 | no | module 13.00×18.00 at (9.00,28.60) outside the board | -0.5 | -1.0 | 6.0 | 8.5 | 10.0 | 86.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 19 | 6 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 7.0 | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 19 | 6 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 7.0 | 390.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 19 | 6 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 7.0 | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 19 | 6 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 7.0 | 390.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 19 | 6 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 7.0 | 390.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 19 | 6 | no | module top 6.40 > LID_Y 6 | -0.5 | -1.0 | 6.0 | 8.5 | 7.0 | 99.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 19 | 6.5 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 7.5 | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 19 | 6.5 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 7.5 | 390.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 19 | 6.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 7.5 | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 19 | 6.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 7.5 | 390.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 19 | 6.5 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 7.5 | 390.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 19 | 6.5 | no | JST_SH top 7.30 > LID_Y 6.5 | -0.5 | -1.0 | 6.0 | 8.5 | 7.5 | 99.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 19 | 7 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 8.0 | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 19 | 7 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 8.0 | 390.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 19 | 7 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 8.0 | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 19 | 7 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 8.0 | 390.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 19 | 7 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 8.0 | 390.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 19 | 7 | no | JST_SH top 7.30 > LID_Y 7 | -0.5 | -1.0 | 6.0 | 8.5 | 8.0 | 99.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 19 | 8 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 9.0 | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 19 | 8 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 9.0 | 390.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 19 | 8 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 9.0 | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 19 | 8 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 9.0 | 390.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 19 | 8 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 9.0 | 390.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 19 | 8 | no | module 13.00×18.00 at (9.50,28.60) outside the board | -0.5 | -1.0 | 6.0 | 8.5 | 9.0 | 99.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 19 | 8.5 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 9.5 | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 19 | 8.5 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 9.5 | 390.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 19 | 8.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 9.5 | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 19 | 8.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 9.5 | 390.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 19 | 8.5 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 9.5 | 390.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 19 | 8.5 | no | module 13.00×18.00 at (9.50,28.60) outside the board | -0.5 | -1.0 | 6.0 | 8.5 | 9.5 | 99.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 19 | 9 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 10.0 | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 19 | 9 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 10.0 | 390.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 19 | 9 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 10.0 | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 19 | 9 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 10.0 | 390.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 19 | 9 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 10.0 | 390.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 19 | 9 | no | module 13.00×18.00 at (9.50,28.60) outside the board | -0.5 | -1.0 | 6.0 | 8.5 | 10.0 | 99.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 20 | 6 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 7.0 | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 20 | 6 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 7.0 | 426.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 20 | 6 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 7.0 | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 20 | 6 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 7.0 | 426.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 20 | 6 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 7.0 | 426.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 20 | 6 | no | module top 6.40 > LID_Y 6 | -0.5 | -1.0 | 6.0 | 8.5 | 7.0 | 111.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 20 | 6.5 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 7.5 | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 20 | 6.5 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 7.5 | 426.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 20 | 6.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 7.5 | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 20 | 6.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 7.5 | 426.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 20 | 6.5 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 7.5 | 426.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 20 | 6.5 | no | header top 6.90 > LID_Y 6.5 | -0.5 | -1.0 | 6.0 | 8.5 | 7.5 | 111.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 20 | 7 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 8.0 | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 20 | 7 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 8.0 | 426.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 20 | 7 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 8.0 | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 20 | 7 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 8.0 | 426.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 20 | 7 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 8.0 | 426.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 20 | 7 | no | module 13.00×18.00 at (8.75,28.60) outside the board | -0.5 | -1.0 | 6.0 | 8.5 | 8.0 | 111.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 20 | 8 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 9.0 | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 20 | 8 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 9.0 | 426.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 20 | 8 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 9.0 | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 20 | 8 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 9.0 | 426.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 20 | 8 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 9.0 | 426.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 20 | 8 | no | module 13.00×18.00 at (8.75,28.60) outside the board | -0.5 | -1.0 | 6.0 | 8.5 | 9.0 | 111.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 20 | 8.5 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 9.5 | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 20 | 8.5 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 9.5 | 426.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 20 | 8.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 9.5 | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 20 | 8.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 9.5 | 426.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 20 | 8.5 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 9.5 | 426.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 20 | 8.5 | no | module 13.00×18.00 at (8.75,28.60) outside the board | -0.5 | -1.0 | 6.0 | 8.5 | 9.5 | 111.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | series | 20 | 9 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 10.0 | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | series | 20 | 9 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 10.0 | 426.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | series | 20 | 9 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 10.0 | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | series | 20 | 9 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 10.0 | 426.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | series | 20 | 9 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 10.0 | 426.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | series | 20 | 9 | no | module 13.00×18.00 at (8.75,28.60) outside the board | -0.5 | -1.0 | 6.0 | 8.5 | 10.0 | 111.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 18 | 6 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 7.0 | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 18 | 6 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 7.0 | 345.8 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 18 | 6 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 7.0 | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 18 | 6 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 7.0 | 345.8 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 18 | 6 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 7.0 | 345.8 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 18 | 6 | no | cell top 7.63 > LID_Y 6 | -0.5 | -1.0 | 6.0 | 8.5 | 7.0 | 345.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 18 | 6.5 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 7.5 | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 18 | 6.5 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 7.5 | 345.8 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 18 | 6.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 7.5 | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 18 | 6.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 7.5 | 345.8 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 18 | 6.5 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 7.5 | 345.8 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 18 | 6.5 | no | cell top 7.63 > LID_Y 6.5 | -0.5 | -1.0 | 6.0 | 8.5 | 7.5 | 345.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 18 | 7 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 8.0 | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 18 | 7 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 8.0 | 345.8 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 18 | 7 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 8.0 | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 18 | 7 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 8.0 | 345.8 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 18 | 7 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 8.0 | 345.8 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 18 | 7 | no | cell top 7.63 > LID_Y 7 | -0.5 | -1.0 | 6.0 | 8.5 | 8.0 | 345.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 18 | 8 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 9.0 | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 18 | 8 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 9.0 | 345.8 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 18 | 8 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 9.0 | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 18 | 8 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 9.0 | 345.8 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 18 | 8 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 9.0 | 345.8 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 18 | 8 | no | module enters SIG1 keep-out + 0.5 | -0.5 | -1.0 | 6.0 | 8.5 | 9.0 | 345.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 18 | 8.5 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 9.5 | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 18 | 8.5 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 9.5 | 345.8 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 18 | 8.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 9.5 | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 18 | 8.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 9.5 | 345.8 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 18 | 8.5 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 9.5 | 345.8 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 18 | 8.5 | no | module enters SIG1 keep-out + 0.5 | -0.5 | -1.0 | 6.0 | 8.5 | 9.5 | 345.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 18 | 9 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 10.0 | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 18 | 9 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 10.0 | 345.8 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 18 | 9 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 10.0 | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 18 | 9 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 10.0 | 345.8 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 18 | 9 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 10.0 | 345.8 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 18 | 9 | no | module enters SIG1 keep-out + 0.5 | -0.5 | -1.0 | 6.0 | 8.5 | 10.0 | 345.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 19 | 6 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 7.0 | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 19 | 6 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 7.0 | 381.2 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 19 | 6 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 7.0 | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 19 | 6 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 7.0 | 381.2 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 19 | 6 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 7.0 | 381.2 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 19 | 6 | no | cell top 7.63 > LID_Y 6 | -0.5 | -1.0 | 6.0 | 8.5 | 7.0 | 381.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 19 | 6.5 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 7.5 | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 19 | 6.5 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 7.5 | 381.2 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 19 | 6.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 7.5 | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 19 | 6.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 7.5 | 381.2 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 19 | 6.5 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 7.5 | 381.2 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 19 | 6.5 | no | cell top 7.63 > LID_Y 6.5 | -0.5 | -1.0 | 6.0 | 8.5 | 7.5 | 381.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 19 | 7 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 8.0 | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 19 | 7 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 8.0 | 381.2 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 19 | 7 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 8.0 | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 19 | 7 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 8.0 | 381.2 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 19 | 7 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 8.0 | 381.2 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 19 | 7 | no | cell top 7.63 > LID_Y 7 | -0.5 | -1.0 | 6.0 | 8.5 | 8.0 | 381.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 19 | 8 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 9.0 | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 19 | 8 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 9.0 | 381.2 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 19 | 8 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 9.0 | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 19 | 8 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 9.0 | 381.2 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 19 | 8 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 9.0 | 381.2 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 19 | 8 | no | module enters SIG1 keep-out + 0.5 | -0.5 | -1.0 | 6.0 | 8.5 | 9.0 | 381.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 19 | 8.5 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 9.5 | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 19 | 8.5 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 9.5 | 381.2 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 19 | 8.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 9.5 | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 19 | 8.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 9.5 | 381.2 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 19 | 8.5 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 9.5 | 381.2 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 19 | 8.5 | no | module enters SIG1 keep-out + 0.5 | -0.5 | -1.0 | 6.0 | 8.5 | 9.5 | 381.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 19 | 9 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 10.0 | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 19 | 9 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 10.0 | 381.2 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 19 | 9 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 10.0 | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 19 | 9 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 10.0 | 381.2 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 19 | 9 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 10.0 | 381.2 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 19 | 9 | no | module enters SIG1 keep-out + 0.5 | -0.5 | -1.0 | 6.0 | 8.5 | 10.0 | 381.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 20 | 6 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 7.0 | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 20 | 6 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 7.0 | 417.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 20 | 6 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 7.0 | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 20 | 6 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 7.0 | 417.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 20 | 6 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 7.0 | 417.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 20 | 6 | no | cell top 7.63 > LID_Y 6 | -0.5 | -1.0 | 6.0 | 8.5 | 7.0 | 417.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 20 | 6.5 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 7.5 | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 20 | 6.5 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 7.5 | 417.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 20 | 6.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 7.5 | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 20 | 6.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 7.5 | 417.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 20 | 6.5 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 7.5 | 417.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 20 | 6.5 | no | cell top 7.63 > LID_Y 6.5 | -0.5 | -1.0 | 6.0 | 8.5 | 7.5 | 417.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 20 | 7 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 8.0 | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 20 | 7 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 8.0 | 417.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 20 | 7 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 8.0 | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 20 | 7 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 8.0 | 417.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 20 | 7 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 8.0 | 417.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 20 | 7 | no | cell top 7.63 > LID_Y 7 | -0.5 | -1.0 | 6.0 | 8.5 | 8.0 | 417.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 20 | 8 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 9.0 | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 20 | 8 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 9.0 | 417.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 20 | 8 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 9.0 | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 20 | 8 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 9.0 | 417.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 20 | 8 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 9.0 | 417.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 20 | 8 | no | module enters SIG1 keep-out + 0.5 | -0.5 | -1.0 | 6.0 | 8.5 | 9.0 | 417.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 20 | 8.5 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 9.5 | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 20 | 8.5 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 9.5 | 417.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 20 | 8.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 9.5 | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 20 | 8.5 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 9.5 | 417.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 20 | 8.5 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 9.5 | 417.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 20 | 8.5 | no | module enters SIG1 keep-out + 0.5 | -0.5 | -1.0 | 6.0 | 8.5 | 9.5 | 417.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | dtp | stacked | 20 | 9 | no | nominal cell clearance -0.5 is not positive (cell 3.5 under standoff 3) | -0.5 | -1.0 | 6.0 | 8.5 | 10.0 | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | dtp | stacked | 20 | 9 | no | nominal cell clearance +0.0 is not positive (cell 3.5 under standoff 3.5) | +0.0 | -0.5 | 6.5 | 9.0 | 10.0 | 417.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | dtp | stacked | 20 | 9 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 7.0 | 9.5 | 10.0 | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | dtp | stacked | 20 | 9 | no | cell would carry board load (deformed clearance +0.0; bosses 0.5 below standoff tops) | +0.5 | +0.0 | 6.5 | 9.0 | 10.0 | 417.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | dtp | stacked | 20 | 9 | no | outer height 9.5 > 9.0 at zero added clearance (standoff 4+board 1+module 2+floor 1.5+lid 1) | +1.0 | +0.5 | 7.0 | 9.5 | 10.0 | 417.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | dtp | stacked | 20 | 9 | no | module enters SIG1 keep-out + 0.5 | -0.5 | -1.0 | 6.0 | 8.5 | 10.0 | 417.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 18 | 6 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 7.0 | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 18 | 6 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 7.0 | 354.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 18 | 6 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 7.0 | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 18 | 6 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 7.0 | 354.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 18 | 6 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 7.0 | 354.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 18 | 6 | no | module top 6.40 > LID_Y 6 | -2.5 | -3.0 | 6.0 | 8.5 | 7.0 | 128.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 18 | 6.5 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 7.5 | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 18 | 6.5 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 7.5 | 354.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 18 | 6.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 7.5 | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 18 | 6.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 7.5 | 354.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 18 | 6.5 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 7.5 | 354.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 18 | 6.5 | no | cell top 7.00 > LID_Y 6.5 | -2.5 | -3.0 | 6.0 | 8.5 | 7.5 | 128.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 18 | 7 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 8.0 | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 18 | 7 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 8.0 | 354.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 18 | 7 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 8.0 | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 18 | 7 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 8.0 | 354.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 18 | 7 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 8.0 | 354.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 18 | 7 | no | JST_SH top 7.30 > LID_Y 7 | -2.5 | -3.0 | 6.0 | 8.5 | 8.0 | 128.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 18 | 8 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 9.0 | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 18 | 8 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 9.0 | 354.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 18 | 8 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 9.0 | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 18 | 8 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 9.0 | 354.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 18 | 8 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 9.0 | 354.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 18 | 8 | no | module overlaps ADS1292_RSM | -2.5 | -3.0 | 6.0 | 8.5 | 9.0 | 128.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 18 | 8.5 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 9.5 | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 18 | 8.5 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 9.5 | 354.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 18 | 8.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 9.5 | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 18 | 8.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 9.5 | 354.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 18 | 8.5 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 9.5 | 354.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 18 | 8.5 | no | module overlaps ADS1292_RSM | -2.5 | -3.0 | 6.0 | 8.5 | 9.5 | 128.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 18 | 9 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 10.0 | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 18 | 9 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 10.0 | 354.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 18 | 9 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 10.0 | 354.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 18 | 9 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 10.0 | 354.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 18 | 9 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 10.0 | 354.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 18 | 9 | no | module overlaps ADS1292_RSM | -2.5 | -3.0 | 6.0 | 8.5 | 10.0 | 128.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 19 | 6 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 7.0 | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 19 | 6 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 7.0 | 390.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 19 | 6 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 7.0 | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 19 | 6 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 7.0 | 390.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 19 | 6 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 7.0 | 390.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 19 | 6 | no | module top 6.40 > LID_Y 6 | -2.5 | -3.0 | 6.0 | 8.5 | 7.0 | 147.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 19 | 6.5 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 7.5 | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 19 | 6.5 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 7.5 | 390.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 19 | 6.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 7.5 | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 19 | 6.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 7.5 | 390.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 19 | 6.5 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 7.5 | 390.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 19 | 6.5 | no | cell top 7.00 > LID_Y 6.5 | -2.5 | -3.0 | 6.0 | 8.5 | 7.5 | 147.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 19 | 7 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 8.0 | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 19 | 7 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 8.0 | 390.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 19 | 7 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 8.0 | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 19 | 7 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 8.0 | 390.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 19 | 7 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 8.0 | 390.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 19 | 7 | no | module overlaps ADS1292_RSM | -2.5 | -3.0 | 6.0 | 8.5 | 8.0 | 147.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 19 | 8 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 9.0 | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 19 | 8 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 9.0 | 390.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 19 | 8 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 9.0 | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 19 | 8 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 9.0 | 390.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 19 | 8 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 9.0 | 390.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 19 | 8 | no | module overlaps ADS1292_RSM | -2.5 | -3.0 | 6.0 | 8.5 | 9.0 | 147.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 19 | 8.5 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 9.5 | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 19 | 8.5 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 9.5 | 390.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 19 | 8.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 9.5 | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 19 | 8.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 9.5 | 390.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 19 | 8.5 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 9.5 | 390.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 19 | 8.5 | no | module overlaps ADS1292_RSM | -2.5 | -3.0 | 6.0 | 8.5 | 9.5 | 147.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 19 | 9 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 10.0 | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 19 | 9 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 10.0 | 390.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 19 | 9 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 10.0 | 390.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 19 | 9 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 10.0 | 390.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 19 | 9 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 10.0 | 390.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 19 | 9 | no | module overlaps ADS1292_RSM | -2.5 | -3.0 | 6.0 | 8.5 | 10.0 | 147.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 20 | 6 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 7.0 | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 20 | 6 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 7.0 | 426.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 20 | 6 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 7.0 | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 20 | 6 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 7.0 | 426.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 20 | 6 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 7.0 | 426.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 20 | 6 | no | module top 6.40 > LID_Y 6 | -2.5 | -3.0 | 6.0 | 8.5 | 7.0 | 166.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 20 | 6.5 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 7.5 | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 20 | 6.5 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 7.5 | 426.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 20 | 6.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 7.5 | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 20 | 6.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 7.5 | 426.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 20 | 6.5 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 7.5 | 426.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 20 | 6.5 | no | cell top 7.00 > LID_Y 6.5 | -2.5 | -3.0 | 6.0 | 8.5 | 7.5 | 166.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 20 | 7 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 8.0 | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 20 | 7 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 8.0 | 426.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 20 | 7 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 8.0 | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 20 | 7 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 8.0 | 426.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 20 | 7 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 8.0 | 426.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 20 | 7 | no | module overlaps switch | -2.5 | -3.0 | 6.0 | 8.5 | 8.0 | 166.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 20 | 8 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 9.0 | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 20 | 8 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 9.0 | 426.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 20 | 8 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 9.0 | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 20 | 8 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 9.0 | 426.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 20 | 8 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 9.0 | 426.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 20 | 8 | no | module overlaps switch | -2.5 | -3.0 | 6.0 | 8.5 | 9.0 | 166.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 20 | 8.5 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 9.5 | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 20 | 8.5 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 9.5 | 426.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 20 | 8.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 9.5 | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 20 | 8.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 9.5 | 426.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 20 | 8.5 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 9.5 | 426.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 20 | 8.5 | no | module overlaps switch | -2.5 | -3.0 | 6.0 | 8.5 | 9.5 | 166.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | series | 20 | 9 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 10.0 | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | series | 20 | 9 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 10.0 | 426.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | series | 20 | 9 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 10.0 | 426.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | series | 20 | 9 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 10.0 | 426.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | series | 20 | 9 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 10.0 | 426.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | series | 20 | 9 | no | module overlaps switch | -2.5 | -3.0 | 6.0 | 8.5 | 10.0 | 166.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 18 | 6 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 7.0 | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 18 | 6 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 7.0 | 345.8 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 18 | 6 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 7.0 | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 18 | 6 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 7.0 | 345.8 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 18 | 6 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 7.0 | 345.8 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 18 | 6 | no | cell top 9.40 > LID_Y 6 | -2.5 | -3.0 | 6.0 | 8.5 | 7.0 | 345.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 18 | 6.5 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 7.5 | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 18 | 6.5 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 7.5 | 345.8 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 18 | 6.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 7.5 | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 18 | 6.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 7.5 | 345.8 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 18 | 6.5 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 7.5 | 345.8 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 18 | 6.5 | no | cell top 9.40 > LID_Y 6.5 | -2.5 | -3.0 | 6.0 | 8.5 | 7.5 | 345.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 18 | 7 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 8.0 | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 18 | 7 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 8.0 | 345.8 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 18 | 7 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 8.0 | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 18 | 7 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 8.0 | 345.8 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 18 | 7 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 8.0 | 345.8 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 18 | 7 | no | cell top 9.40 > LID_Y 7 | -2.5 | -3.0 | 6.0 | 8.5 | 8.0 | 345.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 18 | 8 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 9.0 | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 18 | 8 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 9.0 | 345.8 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 18 | 8 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 9.0 | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 18 | 8 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 9.0 | 345.8 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 18 | 8 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 9.0 | 345.8 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 18 | 8 | no | cell top 9.40 > LID_Y 8 | -2.5 | -3.0 | 6.0 | 8.5 | 9.0 | 345.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 18 | 8.5 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 9.5 | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 18 | 8.5 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 9.5 | 345.8 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 18 | 8.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 9.5 | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 18 | 8.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 9.5 | 345.8 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 18 | 8.5 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 9.5 | 345.8 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 18 | 8.5 | no | cell top 9.40 > LID_Y 8.5 | -2.5 | -3.0 | 6.0 | 8.5 | 9.5 | 345.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 18 | 9 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 10.0 | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 18 | 9 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 10.0 | 345.8 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 18 | 9 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 10.0 | 345.8 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 18 | 9 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 10.0 | 345.8 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 18 | 9 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 10.0 | 345.8 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 18 | 9 | no | cell top 9.40 > LID_Y 9 | -2.5 | -3.0 | 6.0 | 8.5 | 10.0 | 345.8 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 19 | 6 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 7.0 | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 19 | 6 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 7.0 | 381.2 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 19 | 6 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 7.0 | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 19 | 6 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 7.0 | 381.2 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 19 | 6 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 7.0 | 381.2 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 19 | 6 | no | cell top 9.40 > LID_Y 6 | -2.5 | -3.0 | 6.0 | 8.5 | 7.0 | 381.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 19 | 6.5 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 7.5 | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 19 | 6.5 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 7.5 | 381.2 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 19 | 6.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 7.5 | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 19 | 6.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 7.5 | 381.2 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 19 | 6.5 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 7.5 | 381.2 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 19 | 6.5 | no | cell top 9.40 > LID_Y 6.5 | -2.5 | -3.0 | 6.0 | 8.5 | 7.5 | 381.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 19 | 7 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 8.0 | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 19 | 7 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 8.0 | 381.2 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 19 | 7 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 8.0 | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 19 | 7 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 8.0 | 381.2 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 19 | 7 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 8.0 | 381.2 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 19 | 7 | no | cell top 9.40 > LID_Y 7 | -2.5 | -3.0 | 6.0 | 8.5 | 8.0 | 381.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 19 | 8 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 9.0 | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 19 | 8 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 9.0 | 381.2 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 19 | 8 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 9.0 | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 19 | 8 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 9.0 | 381.2 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 19 | 8 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 9.0 | 381.2 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 19 | 8 | no | cell top 9.40 > LID_Y 8 | -2.5 | -3.0 | 6.0 | 8.5 | 9.0 | 381.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 19 | 8.5 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 9.5 | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 19 | 8.5 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 9.5 | 381.2 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 19 | 8.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 9.5 | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 19 | 8.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 9.5 | 381.2 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 19 | 8.5 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 9.5 | 381.2 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 19 | 8.5 | no | cell top 9.40 > LID_Y 8.5 | -2.5 | -3.0 | 6.0 | 8.5 | 9.5 | 381.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 19 | 9 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 10.0 | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 19 | 9 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 10.0 | 381.2 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 19 | 9 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 10.0 | 381.2 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 19 | 9 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 10.0 | 381.2 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 19 | 9 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 10.0 | 381.2 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 19 | 9 | no | cell top 9.40 > LID_Y 9 | -2.5 | -3.0 | 6.0 | 8.5 | 10.0 | 381.2 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 20 | 6 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 7.0 | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 20 | 6 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 7.0 | 417.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 20 | 6 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 7.0 | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 20 | 6 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 7.0 | 417.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 20 | 6 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 7.0 | 417.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 20 | 6 | no | cell top 9.40 > LID_Y 6 | -2.5 | -3.0 | 6.0 | 8.5 | 7.0 | 417.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 20 | 6.5 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 7.5 | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 20 | 6.5 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 7.5 | 417.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 20 | 6.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 7.5 | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 20 | 6.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 7.5 | 417.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 20 | 6.5 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 7.5 | 417.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 20 | 6.5 | no | cell top 9.40 > LID_Y 6.5 | -2.5 | -3.0 | 6.0 | 8.5 | 7.5 | 417.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 20 | 7 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 8.0 | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 20 | 7 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 8.0 | 417.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 20 | 7 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 8.0 | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 20 | 7 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 8.0 | 417.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 20 | 7 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 8.0 | 417.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 20 | 7 | no | cell top 9.40 > LID_Y 7 | -2.5 | -3.0 | 6.0 | 8.5 | 8.0 | 417.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 20 | 8 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 9.0 | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 20 | 8 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 9.0 | 417.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 20 | 8 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 9.0 | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 20 | 8 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 9.0 | 417.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 20 | 8 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 9.0 | 417.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 20 | 8 | no | cell top 9.40 > LID_Y 8 | -2.5 | -3.0 | 6.0 | 8.5 | 9.0 | 417.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 20 | 8.5 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 9.5 | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 20 | 8.5 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 9.5 | 417.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 20 | 8.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 9.5 | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 20 | 8.5 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 9.5 | 417.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 20 | 8.5 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 9.5 | 417.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 20 | 8.5 | no | cell top 9.40 > LID_Y 8.5 | -2.5 | -3.0 | 6.0 | 8.5 | 9.5 | 417.9 | 47.90 | 50.90 |
| B | I | 3 | 0 | 501015 | stacked | 20 | 9 | no | nominal cell clearance -2.5 is not positive (cell 5.5 under standoff 3) | -2.5 | -3.0 | 6.0 | 8.5 | 10.0 | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0 | 501015 | stacked | 20 | 9 | no | nominal cell clearance -2.0 is not positive (cell 5.5 under standoff 3.5) | -2.0 | -2.5 | 6.5 | 9.0 | 10.0 | 417.9 | 47.90 | 50.90 |
| B | I | 4 | 0 | 501015 | stacked | 20 | 9 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 4) | -1.5 | -2.0 | 7.0 | 9.5 | 10.0 | 417.9 | 47.90 | 50.90 |
| B | I | 3.5 | 0.5 | 501015 | stacked | 20 | 9 | no | nominal cell clearance -1.5 is not positive (cell 5.5 under standoff 3.5 recess 0.5) | -1.5 | -2.0 | 6.5 | 9.0 | 10.0 | 417.9 | 47.90 | 50.90 |
| B | I | 4 | 0.5 | 501015 | stacked | 20 | 9 | no | nominal cell clearance -1.0 is not positive (cell 5.5 under standoff 4 recess 0.5) | -1.0 | -1.5 | 7.0 | 9.5 | 10.0 | 417.9 | 47.90 | 50.90 |
| B | II | 3 | 0 | 501015 | stacked | 20 | 9 | no | cell top 9.40 > LID_Y 9 | -2.5 | -3.0 | 6.0 | 8.5 | 10.0 | 417.9 | 47.90 | 50.90 |

## 2. Clearance, stack, and first-conflict families

Cell packed height = body + foam. DTP 3.2+0.3=3.5. 501015 5.2+0.3=5.5.
Nominal clearance = standoff − (packed − recess). The board underside is at the standoff top (rigid).
Deformed clearance = (standoff − 0.5) − (packed − recess). The board bends down onto the bosses.
The cell may lie under the board only with positive nominal clearance. The cell must carry no load (deformed clearance must be positive). C15 for a 0.5 recess (web 1.0) is NOT_MEASURED.

| cell | standoff | recess | nom | def | under-board? | load? |
|---|---:|---:|---:|---:|---|---|
| dtp | 3 | 0 | -0.5 | -1.0 | no | carries load |
| dtp | 3.5 | 0 | +0.0 | -0.5 | no | carries load |
| dtp | 4 | 0 | +0.5 | +0.0 | yes | carries load |
| dtp | 3.5 | 0.5 | +0.5 | +0.0 | yes | carries load |
| dtp | 4 | 0.5 | +1.0 | +0.5 | yes | no load |
| dtp | 3 | 0.5 | +0.0 | -0.5 | no | carries load |
| 501015 | 3 | 0 | -2.5 | -3.0 | no | carries load |
| 501015 | 3.5 | 0 | -2.0 | -2.5 | no | carries load |
| 501015 | 4 | 0 | -1.5 | -2.0 | no | carries load |
| 501015 | 3.5 | 0.5 | -1.5 | -2.0 | no | carries load |
| 501015 | 4 | 0.5 | -1.0 | -1.5 | no | carries load |

Turn 09 numbers: 4.0 with no recess, deformed clearance 0.0. 3.5 with no recess, deformed clearance −0.5.
4.0 with no recess or 3.5 with a 0.5 recess: nominal +0.5. 3.0 with that recess: nominal 0.0.
Only DTP + standoff 4.0 + recess 0.5 has positive deformed clearance (+0.5). It still hits SIG1 (cell 22 mm from s 1.5).

Module stack = standoff + board 1.0 + module (A 2.3, B 2.0). Outer at zero added clearance = 1.5 floor + stack + 1.0 lid.

| arch | standoff | stack | outer0 |
|---|---:|---:|---:|
| A | 3 | 6.3 | 8.8 |
| A | 3.5 | 6.8 | 9.3 |
| A | 4 | 7.3 | 9.8 |
| B | 3 | 6.0 | 8.5 |
| B | 3.5 | 6.5 | 9.0 |
| B | 4 | 7.0 | 9.5 |

A at 3.5 and 4.0 exceeds outer 9.0 at zero added clearance (9.3 and 9.8). B at 4.0 is 9.5. B at 3.5 is 9.0. A at 3.0 is 8.8. B at 3.0 is 8.5.
outer@lid in the run table is LID_Y + 1.0 (the candidate body at that lid). module-to-lid is packing, not a solid probe.

Interface I (720 runs): none close. First conflicts are the clearance or load rule, outer height, or the 22 mm DTP hitting SIG1.

Interface II (144 runs): four close, all A 501015 series width 20.

Adjustment region per site (Interface I, formula only): 4.0 − 2.9 − 0.3 = ±0.8 mm. NOT_MEASURED on the solid.

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
| Standoff | M2.5 hex 5 AF, circumradius 2.9, heights 3.0, 3.5 and 4.0 | turn 09; C14 3.0 Spacer Express, 4.0 Harwin R25-1000402; no 3.5 page |
| Boss drop | 0.5 | turn 07/09 |
| Cell floor recess | 0.5, remaining web 1.0 | turn 09; C15 NOT_MEASURED |
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
- V2_RECESS / C15: the 0.5 floor recess and 1.0 residual web are not on the order-1 solid.
- V2_CELL_CLEARANCE: nominal and deformed numbers are packing arithmetic, not a solid probe. G5/G7 remain open.
- Deformed board envelope: NOT_MEASURED on the order-1 solid.
- E73 antenna sheet: unreachable; v1 12.4 × 3.8 used.
- M1 on Rolf (Q34): default 52 used for the gate.

## 9. Drawings in the repo

Q56: the repo keeps only the drawings of the runs that close, the Stage B winner (`scripts/cad/params/stageb_v2.toml`) and the first run, in table order, of each first-conflict family (the first conflict with its numbers masked). `placement.py --all` writes the closers, `--kept-drawings` this set, and `--all-drawings --out-dir <tmp>` every run (never committed). All under `docs/fab/cad/v1/`.

| drawing | why kept |
|---|---|
| `placement_v2_A_501015_series_w20_y7_iII_s3.svg` | closes |
| `placement_v2_A_501015_series_w20_y8_iII_s3.svg` | closes; Stage B winner |
| `placement_v2_A_501015_series_w20_y8.5_iII_s3.svg` | closes |
| `placement_v2_A_501015_series_w20_y9_iII_s3.svg` | closes |
| `placement_v2_A_dtp_series_w18_y6_iI_s3.svg` | family: nominal cell clearance # is not positive (cell # under standoff #) |
| `placement_v2_A_dtp_series_w18_y6_iI_s4.svg` | family: cell would carry board load (deformed clearance #; bosses # below standoff tops) |
| `placement_v2_A_dtp_series_w18_y6_iI_s4_r0.5.svg` | family: outer height # > # at zero added clearance (standoff #+board #+module #+floor #+lid #) |
| `placement_v2_A_dtp_series_w18_y6_iII_s3.svg` | family: module top # > LID_Y # |
| `placement_v2_A_dtp_series_w18_y7_iII_s3.svg` | family: JST_SH top # > LID_Y # |
| `placement_v2_A_dtp_series_w18_y8_iII_s3.svg` | family: module #×# at (#,#) outside the board |
| `placement_v2_A_dtp_series_w20_y7_iII_s3.svg` | family: module overlaps ADS#_RSM |
| `placement_v2_A_dtp_stacked_w18_y6_iII_s3.svg` | family: cell top # > LID_Y # |
| `placement_v2_A_dtp_stacked_w18_y8_iII_s3.svg` | family: JST_SH enters SIG# keep-out + # |
| `placement_v2_A_501015_series_w18_y6_iI_s3.5_r0.5.svg` | family: nominal cell clearance # is not positive (cell # under standoff # recess #) |
| `placement_v2_A_501015_series_w18_y8_iII_s3.svg` | family: SWD_# in the antenna keep-out |
| `placement_v2_B_dtp_series_w20_y6.5_iII_s3.svg` | family: header top # > LID_Y # |
| `placement_v2_B_dtp_stacked_w18_y8_iII_s3.svg` | family: module enters SIG# keep-out + # |
| `placement_v2_B_501015_series_w20_y7_iII_s3.svg` | family: module overlaps switch |

