# Packing v2 — which architectures close

WP11 analysis. The plan is not changed. Nothing is ordered.
Architecture C is out (plan v2 turn 02). Interface I is turn 07/09:
no springs, no pins; board underside on three brass standoff tops;
8 × 8 gold pad per site; bosses 0.5 lower than the standoff tops;
cell under the board only with positive nominal clearance and no load
after the board bends onto the bosses. Standoffs 3.0, 3.5 and 4.0.
A 0.5-deep floor recess (web 1.0 remaining) is run at 3.5 and 4.0.
Interface II is the flex-tab fallback.
Arc-plus for the DTP301120 under interface II is §1b (WP11b, Q55).
The Jauch LP501218JH under interface II is §1c (WP11b, L7-research-v4.md §2).
A bigger lid and width for the two buyable cells is §1d (WP11b note 2).
The 501015 pack (17.0 mm with PCM) and 501012 pack are §1e (WP11b note 3, L7 §7).
The REF tab route search is in §5 (WP11b, Q59).
The board-lane layout with real courtyards is §5b (WP11c).
Round 6 decisions 70–74 (`tasks/reviews/code-r6.md`) are in §5b.

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

## 1b. DTP301120 arc-plus under interface II (WP11b)

DTP301120 22.0 × 11.5 × 3.2, foam 0.5 (Q57), series, interface II, architecture A. Widths 18 to 20, LID_Y 7 to 9 (the v2 lid steps in that range), standoffs 3 and 4. Conflict logic is the round 5 checker (no new constants). 48 runs.

| arch | standoff | width | lid | arc+ | closes | first conflict | TOTAL_CHORD | M1 gate |
|---|---:|---:|---:|---:|---|---|---:|---:|
| A | 3 | 18 | 7 | 1.5 | no | module top 7.62 > LID_Y 7 | 49.42 | 52.42 |
| A | 3 | 18 | 7 | 3 | no | module top 7.62 > LID_Y 7 | 50.93 | 53.93 |
| A | 4 | 18 | 7 | 1.5 | no | module top 8.62 > LID_Y 7 | 49.42 | 52.42 |
| A | 4 | 18 | 7 | 3 | no | module top 8.62 > LID_Y 7 | 50.93 | 53.93 |
| A | 3 | 18 | 8 | 1.5 | no | JST_SH top 8.22 > LID_Y 8 | 49.42 | 52.42 |
| A | 3 | 18 | 8 | 3 | no | JST_SH top 8.22 > LID_Y 8 | 50.93 | 53.93 |
| A | 4 | 18 | 8 | 1.5 | no | module top 8.62 > LID_Y 8 | 49.42 | 52.42 |
| A | 4 | 18 | 8 | 3 | no | module top 8.62 > LID_Y 8 | 50.93 | 53.93 |
| A | 3 | 18 | 8.5 | 1.5 | no | module 10.50×15.50 at (7.50,31.35) outside the board | 49.42 | 52.42 |
| A | 3 | 18 | 8.5 | 3 | no | module overlaps ADS1292_RSM | 50.93 | 53.93 |
| A | 4 | 18 | 8.5 | 1.5 | no | module top 8.62 > LID_Y 8.5 | 49.42 | 52.42 |
| A | 4 | 18 | 8.5 | 3 | no | module top 8.62 > LID_Y 8.5 | 50.93 | 53.93 |
| A | 3 | 18 | 9 | 1.5 | no | module 10.50×15.50 at (7.50,31.35) outside the board | 49.42 | 52.42 |
| A | 3 | 18 | 9 | 3 | no | module overlaps ADS1292_RSM | 50.93 | 53.93 |
| A | 4 | 18 | 9 | 1.5 | no | JST_SH top 9.22 > LID_Y 9 | 49.42 | 52.42 |
| A | 4 | 18 | 9 | 3 | no | JST_SH top 9.22 > LID_Y 9 | 50.93 | 53.93 |
| A | 3 | 19 | 7 | 1.5 | no | module top 7.62 > LID_Y 7 | 49.42 | 52.42 |
| A | 3 | 19 | 7 | 3 | no | module top 7.62 > LID_Y 7 | 50.93 | 53.93 |
| A | 4 | 19 | 7 | 1.5 | no | module top 8.62 > LID_Y 7 | 49.42 | 52.42 |
| A | 4 | 19 | 7 | 3 | no | module top 8.62 > LID_Y 7 | 50.93 | 53.93 |
| A | 3 | 19 | 8 | 1.5 | no | JST_SH top 8.22 > LID_Y 8 | 49.42 | 52.42 |
| A | 3 | 19 | 8 | 3 | no | JST_SH top 8.22 > LID_Y 8 | 50.93 | 53.93 |
| A | 4 | 19 | 8 | 1.5 | no | module top 8.62 > LID_Y 8 | 49.42 | 52.42 |
| A | 4 | 19 | 8 | 3 | no | module top 8.62 > LID_Y 8 | 50.93 | 53.93 |
| A | 3 | 19 | 8.5 | 1.5 | no | module 10.50×15.50 at (7.50,31.35) outside the board | 49.42 | 52.42 |
| A | 3 | 19 | 8.5 | 3 | no | module overlaps ADS1292_RSM | 50.93 | 53.93 |
| A | 4 | 19 | 8.5 | 1.5 | no | module top 8.62 > LID_Y 8.5 | 49.42 | 52.42 |
| A | 4 | 19 | 8.5 | 3 | no | module top 8.62 > LID_Y 8.5 | 50.93 | 53.93 |
| A | 3 | 19 | 9 | 1.5 | no | module 10.50×15.50 at (7.50,31.35) outside the board | 49.42 | 52.42 |
| A | 3 | 19 | 9 | 3 | no | module overlaps ADS1292_RSM | 50.93 | 53.93 |
| A | 4 | 19 | 9 | 1.5 | no | JST_SH top 9.22 > LID_Y 9 | 49.42 | 52.42 |
| A | 4 | 19 | 9 | 3 | no | JST_SH top 9.22 > LID_Y 9 | 50.93 | 53.93 |
| A | 3 | 20 | 7 | 1.5 | no | module top 7.62 > LID_Y 7 | 49.42 | 52.42 |
| A | 3 | 20 | 7 | 3 | no | module top 7.62 > LID_Y 7 | 50.93 | 53.93 |
| A | 4 | 20 | 7 | 1.5 | no | module top 8.62 > LID_Y 7 | 49.42 | 52.42 |
| A | 4 | 20 | 7 | 3 | no | module top 8.62 > LID_Y 7 | 50.93 | 53.93 |
| A | 3 | 20 | 8 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| A | 3 | 20 | 8 | 3 | no | ADS1292_RSM in the antenna keep-out | 50.93 | 53.93 |
| A | 4 | 20 | 8 | 1.5 | no | module top 8.62 > LID_Y 8 | 49.42 | 52.42 |
| A | 4 | 20 | 8 | 3 | no | module top 8.62 > LID_Y 8 | 50.93 | 53.93 |
| A | 3 | 20 | 8.5 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| A | 3 | 20 | 8.5 | 3 | no | ADS1292_RSM in the antenna keep-out | 50.93 | 53.93 |
| A | 4 | 20 | 8.5 | 1.5 | no | module top 8.62 > LID_Y 8.5 | 49.42 | 52.42 |
| A | 4 | 20 | 8.5 | 3 | no | module top 8.62 > LID_Y 8.5 | 50.93 | 53.93 |
| A | 3 | 20 | 9 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| A | 3 | 20 | 9 | 3 | no | ADS1292_RSM in the antenna keep-out | 50.93 | 53.93 |
| A | 4 | 20 | 9 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| A | 4 | 20 | 9 | 3 | no | ADS1292_RSM in the antenna keep-out | 50.93 | 53.93 |

0 of 48 close at +1.5 or +3.0. There is no DTP body that closes. At +1.5 mm of arc, TOTAL_CHORD 49.42 against M1−3 = 49.00 (M1 = 52, Q34 blank, default.toml). At +3.0 mm of arc, TOTAL_CHORD 50.93 (M1 gate 53.93). Length cost versus the 501015 winner chord 47.90 is not a closer: +3.0 mm of arc is +3.03 mm of chord. First conflict of each run is in the table.

First-conflict families (numbers masked), failing DTP arc-plus runs:

| family | runs |
|---|---:|
| module top # > LID_Y # | 24 |
| JST_SH top # > LID_Y # | 8 |
| ADS#_RSM in the antenna keep-out | 4 |
| cell to antenna zone # < # mm | 4 |
| module #×# at (#,#) outside the board | 4 |
| module overlaps ADS#_RSM | 4 |

## 1c. Jauch LP501218JH under interface II (WP11b, L7 §2)

Jauch Quartz LP501218JH+PCM 5.4 × 12.5 × 20, foam 0.5 (Q57), series, interface II, architecture A. Widths 18 to 20, LID_Y 7 to 9, standoffs 3 and 4, BODY_ARC 48.4 and arc-plus +1.5 and +3.0. Conflict logic is the round 5 checker (no new constants). 72 runs. Source: `docs/fab/L7-research-v4.md` §2 (DigiKey `1908-LP501218JH+PCM+2WIRE50MM-ND`, 60 mAh, page price and stock on 2026-09-17).

Bare 2-wire leads (28 AWG, 50 ± 3 mm, no connector) per L7 §2. Plan v2 R2: Rolf solders nothing (no soldering, glue, crimping or wire stripping). This cell is a packing candidate only if the assembler or the seller terminates the leads.

| arch | standoff | width | lid | arc+ | closes | first conflict | TOTAL_CHORD | M1 gate |
|---|---:|---:|---:|---:|---|---|---:|---:|
| A | 3 | 18 | 7 | 0 | no | module top 7.62 > LID_Y 7 | 47.90 | 50.90 |
| A | 3 | 18 | 7 | 1.5 | no | module top 7.62 > LID_Y 7 | 49.42 | 52.42 |
| A | 3 | 18 | 7 | 3 | no | module top 7.62 > LID_Y 7 | 50.93 | 53.93 |
| A | 4 | 18 | 7 | 0 | no | module top 8.62 > LID_Y 7 | 47.90 | 50.90 |
| A | 4 | 18 | 7 | 1.5 | no | module top 8.62 > LID_Y 7 | 49.42 | 52.42 |
| A | 4 | 18 | 7 | 3 | no | module top 8.62 > LID_Y 7 | 50.93 | 53.93 |
| A | 3 | 18 | 8 | 0 | no | JST_SH top 8.22 > LID_Y 8 | 47.90 | 50.90 |
| A | 3 | 18 | 8 | 1.5 | no | JST_SH top 8.22 > LID_Y 8 | 49.42 | 52.42 |
| A | 3 | 18 | 8 | 3 | no | JST_SH top 8.22 > LID_Y 8 | 50.93 | 53.93 |
| A | 4 | 18 | 8 | 0 | no | module top 8.62 > LID_Y 8 | 47.90 | 50.90 |
| A | 4 | 18 | 8 | 1.5 | no | module top 8.62 > LID_Y 8 | 49.42 | 52.42 |
| A | 4 | 18 | 8 | 3 | no | module top 8.62 > LID_Y 8 | 50.93 | 53.93 |
| A | 3 | 18 | 8.5 | 0 | no | module 10.50×15.50 at (7.50,29.85) outside the board | 47.90 | 50.90 |
| A | 3 | 18 | 8.5 | 1.5 | no | module overlaps ADS1292_RSM | 49.42 | 52.42 |
| A | 3 | 18 | 8.5 | 3 | no | module overlaps ADS1292_RSM | 50.93 | 53.93 |
| A | 4 | 18 | 8.5 | 0 | no | module top 8.62 > LID_Y 8.5 | 47.90 | 50.90 |
| A | 4 | 18 | 8.5 | 1.5 | no | module top 8.62 > LID_Y 8.5 | 49.42 | 52.42 |
| A | 4 | 18 | 8.5 | 3 | no | module top 8.62 > LID_Y 8.5 | 50.93 | 53.93 |
| A | 3 | 18 | 9 | 0 | no | module 10.50×15.50 at (7.50,29.85) outside the board | 47.90 | 50.90 |
| A | 3 | 18 | 9 | 1.5 | no | module overlaps ADS1292_RSM | 49.42 | 52.42 |
| A | 3 | 18 | 9 | 3 | no | module overlaps ADS1292_RSM | 50.93 | 53.93 |
| A | 4 | 18 | 9 | 0 | no | JST_SH top 9.22 > LID_Y 9 | 47.90 | 50.90 |
| A | 4 | 18 | 9 | 1.5 | no | JST_SH top 9.22 > LID_Y 9 | 49.42 | 52.42 |
| A | 4 | 18 | 9 | 3 | no | JST_SH top 9.22 > LID_Y 9 | 50.93 | 53.93 |
| A | 3 | 19 | 7 | 0 | no | module top 7.62 > LID_Y 7 | 47.90 | 50.90 |
| A | 3 | 19 | 7 | 1.5 | no | module top 7.62 > LID_Y 7 | 49.42 | 52.42 |
| A | 3 | 19 | 7 | 3 | no | module top 7.62 > LID_Y 7 | 50.93 | 53.93 |
| A | 4 | 19 | 7 | 0 | no | module top 8.62 > LID_Y 7 | 47.90 | 50.90 |
| A | 4 | 19 | 7 | 1.5 | no | module top 8.62 > LID_Y 7 | 49.42 | 52.42 |
| A | 4 | 19 | 7 | 3 | no | module top 8.62 > LID_Y 7 | 50.93 | 53.93 |
| A | 3 | 19 | 8 | 0 | no | JST_SH top 8.22 > LID_Y 8 | 47.90 | 50.90 |
| A | 3 | 19 | 8 | 1.5 | no | JST_SH top 8.22 > LID_Y 8 | 49.42 | 52.42 |
| A | 3 | 19 | 8 | 3 | no | JST_SH top 8.22 > LID_Y 8 | 50.93 | 53.93 |
| A | 4 | 19 | 8 | 0 | no | module top 8.62 > LID_Y 8 | 47.90 | 50.90 |
| A | 4 | 19 | 8 | 1.5 | no | module top 8.62 > LID_Y 8 | 49.42 | 52.42 |
| A | 4 | 19 | 8 | 3 | no | module top 8.62 > LID_Y 8 | 50.93 | 53.93 |
| A | 3 | 19 | 8.5 | 0 | no | module 10.50×15.50 at (7.50,29.85) outside the board | 47.90 | 50.90 |
| A | 3 | 19 | 8.5 | 1.5 | no | module overlaps ADS1292_RSM | 49.42 | 52.42 |
| A | 3 | 19 | 8.5 | 3 | no | module overlaps ADS1292_RSM | 50.93 | 53.93 |
| A | 4 | 19 | 8.5 | 0 | no | module top 8.62 > LID_Y 8.5 | 47.90 | 50.90 |
| A | 4 | 19 | 8.5 | 1.5 | no | module top 8.62 > LID_Y 8.5 | 49.42 | 52.42 |
| A | 4 | 19 | 8.5 | 3 | no | module top 8.62 > LID_Y 8.5 | 50.93 | 53.93 |
| A | 3 | 19 | 9 | 0 | no | module 10.50×15.50 at (7.50,29.85) outside the board | 47.90 | 50.90 |
| A | 3 | 19 | 9 | 1.5 | no | module overlaps ADS1292_RSM | 49.42 | 52.42 |
| A | 3 | 19 | 9 | 3 | no | module overlaps ADS1292_RSM | 50.93 | 53.93 |
| A | 4 | 19 | 9 | 0 | no | JST_SH top 9.22 > LID_Y 9 | 47.90 | 50.90 |
| A | 4 | 19 | 9 | 1.5 | no | JST_SH top 9.22 > LID_Y 9 | 49.42 | 52.42 |
| A | 4 | 19 | 9 | 3 | no | JST_SH top 9.22 > LID_Y 9 | 50.93 | 53.93 |
| A | 3 | 20 | 7 | 0 | no | module top 7.62 > LID_Y 7 | 47.90 | 50.90 |
| A | 3 | 20 | 7 | 1.5 | no | module top 7.62 > LID_Y 7 | 49.42 | 52.42 |
| A | 3 | 20 | 7 | 3 | no | module top 7.62 > LID_Y 7 | 50.93 | 53.93 |
| A | 4 | 20 | 7 | 0 | no | module top 8.62 > LID_Y 7 | 47.90 | 50.90 |
| A | 4 | 20 | 7 | 1.5 | no | module top 8.62 > LID_Y 7 | 49.42 | 52.42 |
| A | 4 | 20 | 7 | 3 | no | module top 8.62 > LID_Y 7 | 50.93 | 53.93 |
| A | 3 | 20 | 8 | 0 | no | JST_SH top 8.22 > LID_Y 8 | 47.90 | 50.90 |
| A | 3 | 20 | 8 | 1.5 | no | JST_SH top 8.22 > LID_Y 8 | 49.42 | 52.42 |
| A | 3 | 20 | 8 | 3 | no | JST_SH top 8.22 > LID_Y 8 | 50.93 | 53.93 |
| A | 4 | 20 | 8 | 0 | no | module top 8.62 > LID_Y 8 | 47.90 | 50.90 |
| A | 4 | 20 | 8 | 1.5 | no | module top 8.62 > LID_Y 8 | 49.42 | 52.42 |
| A | 4 | 20 | 8 | 3 | no | module top 8.62 > LID_Y 8 | 50.93 | 53.93 |
| A | 3 | 20 | 8.5 | 0 | no | cell to antenna zone 4.65 < 5 mm | 47.90 | 50.90 |
| A | 3 | 20 | 8.5 | 1.5 | no | JST_SH in the antenna keep-out | 49.42 | 52.42 |
| A | 3 | 20 | 8.5 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| A | 4 | 20 | 8.5 | 0 | no | module top 8.62 > LID_Y 8.5 | 47.90 | 50.90 |
| A | 4 | 20 | 8.5 | 1.5 | no | module top 8.62 > LID_Y 8.5 | 49.42 | 52.42 |
| A | 4 | 20 | 8.5 | 3 | no | module top 8.62 > LID_Y 8.5 | 50.93 | 53.93 |
| A | 3 | 20 | 9 | 0 | no | cell to antenna zone 4.65 < 5 mm | 47.90 | 50.90 |
| A | 3 | 20 | 9 | 1.5 | no | JST_SH in the antenna keep-out | 49.42 | 52.42 |
| A | 3 | 20 | 9 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| A | 4 | 20 | 9 | 0 | no | JST_SH top 9.22 > LID_Y 9 | 47.90 | 50.90 |
| A | 4 | 20 | 9 | 1.5 | no | JST_SH top 9.22 > LID_Y 9 | 49.42 | 52.42 |
| A | 4 | 20 | 9 | 3 | no | JST_SH top 9.22 > LID_Y 9 | 50.93 | 53.93 |

0 of 72 close at BODY_ARC or +1.5 or +3.0. There is no Jauch body that closes. At BODY_ARC, TOTAL_CHORD 47.90 against M1−3 = 49.00. At +3.0 mm of arc, TOTAL_CHORD 50.93 (+3.03 mm of chord versus the 501015 winner). First conflict of each run is in the table.

First-conflict families (numbers masked), failing Jauch runs:

| family | runs |
|---|---:|
| module top # > LID_Y # | 36 |
| JST_SH top # > LID_Y # | 18 |
| module overlaps ADS#_RSM | 8 |
| module #×# at (#,#) outside the board | 4 |
| JST_SH in the antenna keep-out | 2 |
| cell overlaps standoff_SIG# | 2 |
| cell to antenna zone # < # mm | 2 |

## 1d. Bigger body for the two buyable cells (WP11b note 2)

DTP301120 and LP501218JH only. Series, interface II, architecture A, foam 0.5, standoffs 3 and 4, BODY_ARC and arc-plus +1.5 and +3.0. LID_Y 9.5, 10.0 and 10.5; widths 20, 21 and 22. Conflict logic is the round 5 checker (no new constants). 108 runs. The plan's ≤ 9.0 high and 20 wide cap still records a conflict; a run packs here if that cap is the only remaining conflict, so the table can answer how much bigger a buyable cell needs.

| cell | standoff | width | lid | outer | arc+ | packs | first packing conflict | TOTAL_CHORD | M1 gate |
|---|---:|---:|---:|---:|---:|---|---|---:|---:|
| DTP301120 | 3 | 20 | 9.5 | 10.5 | 0 | no | cell to antenna zone 2.65 < 5 mm | 47.90 | 50.90 |
| DTP301120 | 3 | 20 | 9.5 | 10.5 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| DTP301120 | 3 | 20 | 9.5 | 10.5 | 3 | no | ADS1292_RSM in the antenna keep-out | 50.93 | 53.93 |
| DTP301120 | 4 | 20 | 9.5 | 10.5 | 0 | no | cell to antenna zone 2.65 < 5 mm | 47.90 | 50.90 |
| DTP301120 | 4 | 20 | 9.5 | 10.5 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| DTP301120 | 4 | 20 | 9.5 | 10.5 | 3 | no | ADS1292_RSM in the antenna keep-out | 50.93 | 53.93 |
| DTP301120 | 3 | 20 | 10 | 11.0 | 0 | no | cell to antenna zone 2.65 < 5 mm | 47.90 | 50.90 |
| DTP301120 | 3 | 20 | 10 | 11.0 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| DTP301120 | 3 | 20 | 10 | 11.0 | 3 | no | ADS1292_RSM in the antenna keep-out | 50.93 | 53.93 |
| DTP301120 | 4 | 20 | 10 | 11.0 | 0 | no | cell to antenna zone 2.65 < 5 mm | 47.90 | 50.90 |
| DTP301120 | 4 | 20 | 10 | 11.0 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| DTP301120 | 4 | 20 | 10 | 11.0 | 3 | no | ADS1292_RSM in the antenna keep-out | 50.93 | 53.93 |
| DTP301120 | 3 | 20 | 10.5 | 11.5 | 0 | no | cell to antenna zone 2.65 < 5 mm | 47.90 | 50.90 |
| DTP301120 | 3 | 20 | 10.5 | 11.5 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| DTP301120 | 3 | 20 | 10.5 | 11.5 | 3 | no | ADS1292_RSM in the antenna keep-out | 50.93 | 53.93 |
| DTP301120 | 4 | 20 | 10.5 | 11.5 | 0 | no | cell to antenna zone 2.65 < 5 mm | 47.90 | 50.90 |
| DTP301120 | 4 | 20 | 10.5 | 11.5 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| DTP301120 | 4 | 20 | 10.5 | 11.5 | 3 | no | ADS1292_RSM in the antenna keep-out | 50.93 | 53.93 |
| DTP301120 | 3 | 21 | 9.5 | 10.5 | 0 | no | cell to antenna zone 2.65 < 5 mm | 47.90 | 50.90 |
| DTP301120 | 3 | 21 | 9.5 | 10.5 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| DTP301120 | 3 | 21 | 9.5 | 10.5 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| DTP301120 | 4 | 21 | 9.5 | 10.5 | 0 | no | cell to antenna zone 2.65 < 5 mm | 47.90 | 50.90 |
| DTP301120 | 4 | 21 | 9.5 | 10.5 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| DTP301120 | 4 | 21 | 9.5 | 10.5 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| DTP301120 | 3 | 21 | 10 | 11.0 | 0 | no | cell to antenna zone 2.65 < 5 mm | 47.90 | 50.90 |
| DTP301120 | 3 | 21 | 10 | 11.0 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| DTP301120 | 3 | 21 | 10 | 11.0 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| DTP301120 | 4 | 21 | 10 | 11.0 | 0 | no | cell to antenna zone 2.65 < 5 mm | 47.90 | 50.90 |
| DTP301120 | 4 | 21 | 10 | 11.0 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| DTP301120 | 4 | 21 | 10 | 11.0 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| DTP301120 | 3 | 21 | 10.5 | 11.5 | 0 | no | cell to antenna zone 2.65 < 5 mm | 47.90 | 50.90 |
| DTP301120 | 3 | 21 | 10.5 | 11.5 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| DTP301120 | 3 | 21 | 10.5 | 11.5 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| DTP301120 | 4 | 21 | 10.5 | 11.5 | 0 | no | cell to antenna zone 2.65 < 5 mm | 47.90 | 50.90 |
| DTP301120 | 4 | 21 | 10.5 | 11.5 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| DTP301120 | 4 | 21 | 10.5 | 11.5 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| DTP301120 | 3 | 22 | 9.5 | 10.5 | 0 | no | cell to antenna zone 2.65 < 5 mm | 47.90 | 50.90 |
| DTP301120 | 3 | 22 | 9.5 | 10.5 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| DTP301120 | 3 | 22 | 9.5 | 10.5 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| DTP301120 | 4 | 22 | 9.5 | 10.5 | 0 | no | cell to antenna zone 2.65 < 5 mm | 47.90 | 50.90 |
| DTP301120 | 4 | 22 | 9.5 | 10.5 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| DTP301120 | 4 | 22 | 9.5 | 10.5 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| DTP301120 | 3 | 22 | 10 | 11.0 | 0 | no | cell to antenna zone 2.65 < 5 mm | 47.90 | 50.90 |
| DTP301120 | 3 | 22 | 10 | 11.0 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| DTP301120 | 3 | 22 | 10 | 11.0 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| DTP301120 | 4 | 22 | 10 | 11.0 | 0 | no | cell to antenna zone 2.65 < 5 mm | 47.90 | 50.90 |
| DTP301120 | 4 | 22 | 10 | 11.0 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| DTP301120 | 4 | 22 | 10 | 11.0 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| DTP301120 | 3 | 22 | 10.5 | 11.5 | 0 | no | cell to antenna zone 2.65 < 5 mm | 47.90 | 50.90 |
| DTP301120 | 3 | 22 | 10.5 | 11.5 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| DTP301120 | 3 | 22 | 10.5 | 11.5 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| DTP301120 | 4 | 22 | 10.5 | 11.5 | 0 | no | cell to antenna zone 2.65 < 5 mm | 47.90 | 50.90 |
| DTP301120 | 4 | 22 | 10.5 | 11.5 | 1.5 | no | cell to antenna zone 4.15 < 5 mm | 49.42 | 52.42 |
| DTP301120 | 4 | 22 | 10.5 | 11.5 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| LP501218JH | 3 | 20 | 9.5 | 10.5 | 0 | no | cell to antenna zone 4.65 < 5 mm | 47.90 | 50.90 |
| LP501218JH | 3 | 20 | 9.5 | 10.5 | 1.5 | no | JST_SH in the antenna keep-out | 49.42 | 52.42 |
| LP501218JH | 3 | 20 | 9.5 | 10.5 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| LP501218JH | 4 | 20 | 9.5 | 10.5 | 0 | no | cell to antenna zone 4.65 < 5 mm | 47.90 | 50.90 |
| LP501218JH | 4 | 20 | 9.5 | 10.5 | 1.5 | no | JST_SH in the antenna keep-out | 49.42 | 52.42 |
| LP501218JH | 4 | 20 | 9.5 | 10.5 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| LP501218JH | 3 | 20 | 10 | 11.0 | 0 | no | cell to antenna zone 4.65 < 5 mm | 47.90 | 50.90 |
| LP501218JH | 3 | 20 | 10 | 11.0 | 1.5 | no | JST_SH in the antenna keep-out | 49.42 | 52.42 |
| LP501218JH | 3 | 20 | 10 | 11.0 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| LP501218JH | 4 | 20 | 10 | 11.0 | 0 | no | cell to antenna zone 4.65 < 5 mm | 47.90 | 50.90 |
| LP501218JH | 4 | 20 | 10 | 11.0 | 1.5 | no | JST_SH in the antenna keep-out | 49.42 | 52.42 |
| LP501218JH | 4 | 20 | 10 | 11.0 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| LP501218JH | 3 | 20 | 10.5 | 11.5 | 0 | no | cell to antenna zone 4.65 < 5 mm | 47.90 | 50.90 |
| LP501218JH | 3 | 20 | 10.5 | 11.5 | 1.5 | no | JST_SH in the antenna keep-out | 49.42 | 52.42 |
| LP501218JH | 3 | 20 | 10.5 | 11.5 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| LP501218JH | 4 | 20 | 10.5 | 11.5 | 0 | no | cell to antenna zone 4.65 < 5 mm | 47.90 | 50.90 |
| LP501218JH | 4 | 20 | 10.5 | 11.5 | 1.5 | no | JST_SH in the antenna keep-out | 49.42 | 52.42 |
| LP501218JH | 4 | 20 | 10.5 | 11.5 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| LP501218JH | 3 | 21 | 9.5 | 10.5 | 0 | no | cell to antenna zone 4.65 < 5 mm | 47.90 | 50.90 |
| LP501218JH | 3 | 21 | 9.5 | 10.5 | 1.5 | no | switch in the antenna keep-out | 49.42 | 52.42 |
| LP501218JH | 3 | 21 | 9.5 | 10.5 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| LP501218JH | 4 | 21 | 9.5 | 10.5 | 0 | no | cell to antenna zone 4.65 < 5 mm | 47.90 | 50.90 |
| LP501218JH | 4 | 21 | 9.5 | 10.5 | 1.5 | no | switch in the antenna keep-out | 49.42 | 52.42 |
| LP501218JH | 4 | 21 | 9.5 | 10.5 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| LP501218JH | 3 | 21 | 10 | 11.0 | 0 | no | cell to antenna zone 4.65 < 5 mm | 47.90 | 50.90 |
| LP501218JH | 3 | 21 | 10 | 11.0 | 1.5 | no | switch in the antenna keep-out | 49.42 | 52.42 |
| LP501218JH | 3 | 21 | 10 | 11.0 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| LP501218JH | 4 | 21 | 10 | 11.0 | 0 | no | cell to antenna zone 4.65 < 5 mm | 47.90 | 50.90 |
| LP501218JH | 4 | 21 | 10 | 11.0 | 1.5 | no | switch in the antenna keep-out | 49.42 | 52.42 |
| LP501218JH | 4 | 21 | 10 | 11.0 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| LP501218JH | 3 | 21 | 10.5 | 11.5 | 0 | no | cell to antenna zone 4.65 < 5 mm | 47.90 | 50.90 |
| LP501218JH | 3 | 21 | 10.5 | 11.5 | 1.5 | no | switch in the antenna keep-out | 49.42 | 52.42 |
| LP501218JH | 3 | 21 | 10.5 | 11.5 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| LP501218JH | 4 | 21 | 10.5 | 11.5 | 0 | no | cell to antenna zone 4.65 < 5 mm | 47.90 | 50.90 |
| LP501218JH | 4 | 21 | 10.5 | 11.5 | 1.5 | no | switch in the antenna keep-out | 49.42 | 52.42 |
| LP501218JH | 4 | 21 | 10.5 | 11.5 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| LP501218JH | 3 | 22 | 9.5 | 10.5 | 0 | no | cell to antenna zone 4.65 < 5 mm | 47.90 | 50.90 |
| LP501218JH | 3 | 22 | 9.5 | 10.5 | 1.5 | no | switch in the antenna keep-out | 49.42 | 52.42 |
| LP501218JH | 3 | 22 | 9.5 | 10.5 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| LP501218JH | 4 | 22 | 9.5 | 10.5 | 0 | no | cell to antenna zone 4.65 < 5 mm | 47.90 | 50.90 |
| LP501218JH | 4 | 22 | 9.5 | 10.5 | 1.5 | no | switch in the antenna keep-out | 49.42 | 52.42 |
| LP501218JH | 4 | 22 | 9.5 | 10.5 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| LP501218JH | 3 | 22 | 10 | 11.0 | 0 | no | cell to antenna zone 4.65 < 5 mm | 47.90 | 50.90 |
| LP501218JH | 3 | 22 | 10 | 11.0 | 1.5 | no | switch in the antenna keep-out | 49.42 | 52.42 |
| LP501218JH | 3 | 22 | 10 | 11.0 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| LP501218JH | 4 | 22 | 10 | 11.0 | 0 | no | cell to antenna zone 4.65 < 5 mm | 47.90 | 50.90 |
| LP501218JH | 4 | 22 | 10 | 11.0 | 1.5 | no | switch in the antenna keep-out | 49.42 | 52.42 |
| LP501218JH | 4 | 22 | 10 | 11.0 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| LP501218JH | 3 | 22 | 10.5 | 11.5 | 0 | no | cell to antenna zone 4.65 < 5 mm | 47.90 | 50.90 |
| LP501218JH | 3 | 22 | 10.5 | 11.5 | 1.5 | no | switch in the antenna keep-out | 49.42 | 52.42 |
| LP501218JH | 3 | 22 | 10.5 | 11.5 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |
| LP501218JH | 4 | 22 | 10.5 | 11.5 | 0 | no | cell to antenna zone 4.65 < 5 mm | 47.90 | 50.90 |
| LP501218JH | 4 | 22 | 10.5 | 11.5 | 1.5 | no | switch in the antenna keep-out | 49.42 | 52.42 |
| LP501218JH | 4 | 22 | 10.5 | 11.5 | 3 | no | cell overlaps standoff_SIG1 | 50.93 | 53.93 |

0 of 108 close under every round-5 check (including the ≤9×20 cap). 0 of 108 pack if that cap is set aside. No new drawing: Q56 keeps closers only.

- **DTP301120**: no body packs. Family that never clears: `SIG# tab crosses boss_# courtyard`, `cell overlaps standoff_SIG#`. Height cost: no closer; the search reaches LID_Y 10.5, outer 11.5 (+2.5 mm vs winner outer 9.0). Chord cost: no closer; BODY_ARC TOTAL_CHORD 47.90 (same as the 501015 winner 47.90); +3.0 mm of arc is 50.93 (+3.03 mm) and fails M1−3 = 49.00.

- **LP501218JH**: no body packs. Family that never clears: `cell overlaps standoff_SIG#`. Height cost: no closer; the search reaches LID_Y 10.5, outer 11.5 (+2.5 mm vs winner outer 9.0). Chord cost: no closer; BODY_ARC TOTAL_CHORD 47.90 (same as the 501015 winner 47.90); +3.0 mm of arc is 50.93 (+3.03 mm) and fails M1−3 = 49.00.

First packing-conflict families (numbers masked), failing bigger-box runs:

| family | runs |
|---|---:|
| cell to antenna zone # < # mm | 54 |
| cell overlaps standoff_SIG# | 30 |
| switch in the antenna keep-out | 12 |
| ADS#_RSM in the antenna keep-out | 6 |
| JST_SH in the antenna keep-out | 6 |

## 1e. 501015 pack and 501012 pack under interface II (WP11b note 3, L7 §7)

L7-research-v4.md §7 and §7.8: a 501015 pack **with** its protection board is 17.0 × 10.0 × 5.0 mm on the manufacturers' sheets (DNK Power DNK501015 'Dimensions: 17 × 10 × 5.0 mm', Benzo '5mm x 10mm x 17mm'). The plan's envelope 15.6 × 10.4 × 5.2 is a bare cell, not a pack. Packs that fit under 16 mm exist only as marketplace listings. This search uses the 501012 pack 13.0 × 10.1 × 5.1 with PCM, 40 mAh (eBay quote 'approx 13.0mm x 10.1mm x 5.1mm'). The 401012 listing is not run here.

Series, interface II, architecture A, foam 0.5, standoffs 3.0 and 4.0, widths 18 to 20, LID_Y 7 to 9, BODY_ARC and arc-plus +1.5 and +3.0. Conflict logic is the round 5 checker (no new constants). 144 runs. Neither cell is in the 864-run matrix.

The current winner `A_501015_series_w20_y8_iII_s3` with the real 17.0 mm pack (`A_pack501015_series_w20_y8_iII_s3`) does **not** close. First conflict: `BQ25100 overlaps header`. The 17.0 mm body length moves the pocket and shortens the board from s 18.6–37.6 (bare 15.6 mm cell) to 20.0–37.6. Packed height 5.0 + 0.5 = 5.5 (cell top 7.0). No body in this grid closes for the 17.0 mm pack. No first-conflict family is present on every run. On the winner body, BODY_ARC fails first as `BQ25100 overlaps header` (also TLV713 and switch overlap the header). Arc-plus +1.5 on that body leaves only `TOTAL_CHORD 49.42 > M1−3 (49.00)`; the overlap clears, the M1 gate does not.

| arch | cell | standoff | width | lid | arc+ | closes | first conflict | TOTAL_CHORD | M1 gate | outer |
|---|---|---:|---:|---:|---:|---|---|---:|---:|---:|
| A | 501015 pack | 3 | 18 | 7 | 0 | no | module top 7.62 > LID_Y 7 | 47.90 | 50.90 | 8.0 |
| A | 501015 pack | 3 | 18 | 7 | 1.5 | no | module top 7.62 > LID_Y 7 | 49.42 | 52.42 | 8.0 |
| A | 501015 pack | 3 | 18 | 7 | 3 | no | module top 7.62 > LID_Y 7 | 50.93 | 53.93 | 8.0 |
| A | 501015 pack | 4 | 18 | 7 | 0 | no | module top 8.62 > LID_Y 7 | 47.90 | 50.90 | 8.0 |
| A | 501015 pack | 4 | 18 | 7 | 1.5 | no | module top 8.62 > LID_Y 7 | 49.42 | 52.42 | 8.0 |
| A | 501015 pack | 4 | 18 | 7 | 3 | no | module top 8.62 > LID_Y 7 | 50.93 | 53.93 | 8.0 |
| A | 501015 pack | 3 | 18 | 8 | 0 | no | module overlaps ADS1292_RSM | 47.90 | 50.90 | 9.0 |
| A | 501015 pack | 3 | 18 | 8 | 1.5 | no | module overlaps ADS1292_RSM | 49.42 | 52.42 | 9.0 |
| A | 501015 pack | 3 | 18 | 8 | 3 | no | module overlaps ADS1292_RSM | 50.93 | 53.93 | 9.0 |
| A | 501015 pack | 4 | 18 | 8 | 0 | no | module top 8.62 > LID_Y 8 | 47.90 | 50.90 | 9.0 |
| A | 501015 pack | 4 | 18 | 8 | 1.5 | no | module top 8.62 > LID_Y 8 | 49.42 | 52.42 | 9.0 |
| A | 501015 pack | 4 | 18 | 8 | 3 | no | module top 8.62 > LID_Y 8 | 50.93 | 53.93 | 9.0 |
| A | 501015 pack | 3 | 18 | 8.5 | 0 | no | module overlaps ADS1292_RSM | 47.90 | 50.90 | 9.5 |
| A | 501015 pack | 3 | 18 | 8.5 | 1.5 | no | module overlaps ADS1292_RSM | 49.42 | 52.42 | 9.5 |
| A | 501015 pack | 3 | 18 | 8.5 | 3 | no | module overlaps ADS1292_RSM | 50.93 | 53.93 | 9.5 |
| A | 501015 pack | 4 | 18 | 8.5 | 0 | no | module top 8.62 > LID_Y 8.5 | 47.90 | 50.90 | 9.5 |
| A | 501015 pack | 4 | 18 | 8.5 | 1.5 | no | module top 8.62 > LID_Y 8.5 | 49.42 | 52.42 | 9.5 |
| A | 501015 pack | 4 | 18 | 8.5 | 3 | no | module top 8.62 > LID_Y 8.5 | 50.93 | 53.93 | 9.5 |
| A | 501015 pack | 3 | 18 | 9 | 0 | no | module overlaps ADS1292_RSM | 47.90 | 50.90 | 10.0 |
| A | 501015 pack | 3 | 18 | 9 | 1.5 | no | module overlaps ADS1292_RSM | 49.42 | 52.42 | 10.0 |
| A | 501015 pack | 3 | 18 | 9 | 3 | no | module overlaps ADS1292_RSM | 50.93 | 53.93 | 10.0 |
| A | 501015 pack | 4 | 18 | 9 | 0 | no | module overlaps ADS1292_RSM | 47.90 | 50.90 | 10.0 |
| A | 501015 pack | 4 | 18 | 9 | 1.5 | no | module overlaps ADS1292_RSM | 49.42 | 52.42 | 10.0 |
| A | 501015 pack | 4 | 18 | 9 | 3 | no | module overlaps ADS1292_RSM | 50.93 | 53.93 | 10.0 |
| A | 501015 pack | 3 | 19 | 7 | 0 | no | module top 7.62 > LID_Y 7 | 47.90 | 50.90 | 8.0 |
| A | 501015 pack | 3 | 19 | 7 | 1.5 | no | module top 7.62 > LID_Y 7 | 49.42 | 52.42 | 8.0 |
| A | 501015 pack | 3 | 19 | 7 | 3 | no | module top 7.62 > LID_Y 7 | 50.93 | 53.93 | 8.0 |
| A | 501015 pack | 4 | 19 | 7 | 0 | no | module top 8.62 > LID_Y 7 | 47.90 | 50.90 | 8.0 |
| A | 501015 pack | 4 | 19 | 7 | 1.5 | no | module top 8.62 > LID_Y 7 | 49.42 | 52.42 | 8.0 |
| A | 501015 pack | 4 | 19 | 7 | 3 | no | module top 8.62 > LID_Y 7 | 50.93 | 53.93 | 8.0 |
| A | 501015 pack | 3 | 19 | 8 | 0 | no | module overlaps switch | 47.90 | 50.90 | 9.0 |
| A | 501015 pack | 3 | 19 | 8 | 1.5 | no | module overlaps switch | 49.42 | 52.42 | 9.0 |
| A | 501015 pack | 3 | 19 | 8 | 3 | no | TOTAL_CHORD 50.93 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 50.93 | 53.93 | 9.0 |
| A | 501015 pack | 4 | 19 | 8 | 0 | no | module top 8.62 > LID_Y 8 | 47.90 | 50.90 | 9.0 |
| A | 501015 pack | 4 | 19 | 8 | 1.5 | no | module top 8.62 > LID_Y 8 | 49.42 | 52.42 | 9.0 |
| A | 501015 pack | 4 | 19 | 8 | 3 | no | module top 8.62 > LID_Y 8 | 50.93 | 53.93 | 9.0 |
| A | 501015 pack | 3 | 19 | 8.5 | 0 | no | module overlaps switch | 47.90 | 50.90 | 9.5 |
| A | 501015 pack | 3 | 19 | 8.5 | 1.5 | no | module overlaps switch | 49.42 | 52.42 | 9.5 |
| A | 501015 pack | 3 | 19 | 8.5 | 3 | no | TOTAL_CHORD 50.93 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 50.93 | 53.93 | 9.5 |
| A | 501015 pack | 4 | 19 | 8.5 | 0 | no | module top 8.62 > LID_Y 8.5 | 47.90 | 50.90 | 9.5 |
| A | 501015 pack | 4 | 19 | 8.5 | 1.5 | no | module top 8.62 > LID_Y 8.5 | 49.42 | 52.42 | 9.5 |
| A | 501015 pack | 4 | 19 | 8.5 | 3 | no | module top 8.62 > LID_Y 8.5 | 50.93 | 53.93 | 9.5 |
| A | 501015 pack | 3 | 19 | 9 | 0 | no | module overlaps switch | 47.90 | 50.90 | 10.0 |
| A | 501015 pack | 3 | 19 | 9 | 1.5 | no | module overlaps switch | 49.42 | 52.42 | 10.0 |
| A | 501015 pack | 3 | 19 | 9 | 3 | no | TOTAL_CHORD 50.93 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 50.93 | 53.93 | 10.0 |
| A | 501015 pack | 4 | 19 | 9 | 0 | no | module overlaps switch | 47.90 | 50.90 | 10.0 |
| A | 501015 pack | 4 | 19 | 9 | 1.5 | no | module overlaps switch | 49.42 | 52.42 | 10.0 |
| A | 501015 pack | 4 | 19 | 9 | 3 | no | TOTAL_CHORD 50.93 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 50.93 | 53.93 | 10.0 |
| A | 501015 pack | 3 | 20 | 7 | 0 | no | module top 7.62 > LID_Y 7 | 47.90 | 50.90 | 8.0 |
| A | 501015 pack | 3 | 20 | 7 | 1.5 | no | module top 7.62 > LID_Y 7 | 49.42 | 52.42 | 8.0 |
| A | 501015 pack | 3 | 20 | 7 | 3 | no | module top 7.62 > LID_Y 7 | 50.93 | 53.93 | 8.0 |
| A | 501015 pack | 4 | 20 | 7 | 0 | no | module top 8.62 > LID_Y 7 | 47.90 | 50.90 | 8.0 |
| A | 501015 pack | 4 | 20 | 7 | 1.5 | no | module top 8.62 > LID_Y 7 | 49.42 | 52.42 | 8.0 |
| A | 501015 pack | 4 | 20 | 7 | 3 | no | module top 8.62 > LID_Y 7 | 50.93 | 53.93 | 8.0 |
| A | 501015 pack | 3 | 20 | 8 | 0 | no | BQ25100 overlaps header | 47.90 | 50.90 | 9.0 |
| A | 501015 pack | 3 | 20 | 8 | 1.5 | no | TOTAL_CHORD 49.42 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 49.42 | 52.42 | 9.0 |
| A | 501015 pack | 3 | 20 | 8 | 3 | no | TOTAL_CHORD 50.93 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 50.93 | 53.93 | 9.0 |
| A | 501015 pack | 4 | 20 | 8 | 0 | no | module top 8.62 > LID_Y 8 | 47.90 | 50.90 | 9.0 |
| A | 501015 pack | 4 | 20 | 8 | 1.5 | no | module top 8.62 > LID_Y 8 | 49.42 | 52.42 | 9.0 |
| A | 501015 pack | 4 | 20 | 8 | 3 | no | module top 8.62 > LID_Y 8 | 50.93 | 53.93 | 9.0 |
| A | 501015 pack | 3 | 20 | 8.5 | 0 | no | BQ25100 overlaps header | 47.90 | 50.90 | 9.5 |
| A | 501015 pack | 3 | 20 | 8.5 | 1.5 | no | TOTAL_CHORD 49.42 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 49.42 | 52.42 | 9.5 |
| A | 501015 pack | 3 | 20 | 8.5 | 3 | no | TOTAL_CHORD 50.93 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 50.93 | 53.93 | 9.5 |
| A | 501015 pack | 4 | 20 | 8.5 | 0 | no | module top 8.62 > LID_Y 8.5 | 47.90 | 50.90 | 9.5 |
| A | 501015 pack | 4 | 20 | 8.5 | 1.5 | no | module top 8.62 > LID_Y 8.5 | 49.42 | 52.42 | 9.5 |
| A | 501015 pack | 4 | 20 | 8.5 | 3 | no | module top 8.62 > LID_Y 8.5 | 50.93 | 53.93 | 9.5 |
| A | 501015 pack | 3 | 20 | 9 | 0 | no | BQ25100 overlaps header | 47.90 | 50.90 | 10.0 |
| A | 501015 pack | 3 | 20 | 9 | 1.5 | no | TOTAL_CHORD 49.42 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 49.42 | 52.42 | 10.0 |
| A | 501015 pack | 3 | 20 | 9 | 3 | no | TOTAL_CHORD 50.93 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 50.93 | 53.93 | 10.0 |
| A | 501015 pack | 4 | 20 | 9 | 0 | no | BQ25100 overlaps header | 47.90 | 50.90 | 10.0 |
| A | 501015 pack | 4 | 20 | 9 | 1.5 | no | TOTAL_CHORD 49.42 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 49.42 | 52.42 | 10.0 |
| A | 501015 pack | 4 | 20 | 9 | 3 | no | TOTAL_CHORD 50.93 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 50.93 | 53.93 | 10.0 |
| A | 501012 pack | 3 | 18 | 7 | 0 | no | module top 7.62 > LID_Y 7 | 47.90 | 50.90 | 8.0 |
| A | 501012 pack | 3 | 18 | 7 | 1.5 | no | module top 7.62 > LID_Y 7 | 49.42 | 52.42 | 8.0 |
| A | 501012 pack | 3 | 18 | 7 | 3 | no | module top 7.62 > LID_Y 7 | 50.93 | 53.93 | 8.0 |
| A | 501012 pack | 4 | 18 | 7 | 0 | no | module top 8.62 > LID_Y 7 | 47.90 | 50.90 | 8.0 |
| A | 501012 pack | 4 | 18 | 7 | 1.5 | no | module top 8.62 > LID_Y 7 | 49.42 | 52.42 | 8.0 |
| A | 501012 pack | 4 | 18 | 7 | 3 | no | module top 8.62 > LID_Y 7 | 50.93 | 53.93 | 8.0 |
| A | 501012 pack | 3 | 18 | 8 | 0 | no | ADS1292_RSM overlaps switch | 47.90 | 50.90 | 9.0 |
| A | 501012 pack | 3 | 18 | 8 | 1.5 | no | ADS1292_RSM overlaps switch | 49.42 | 52.42 | 9.0 |
| A | 501012 pack | 3 | 18 | 8 | 3 | no | TOTAL_CHORD 50.93 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 50.93 | 53.93 | 9.0 |
| A | 501012 pack | 4 | 18 | 8 | 0 | no | module top 8.62 > LID_Y 8 | 47.90 | 50.90 | 9.0 |
| A | 501012 pack | 4 | 18 | 8 | 1.5 | no | module top 8.62 > LID_Y 8 | 49.42 | 52.42 | 9.0 |
| A | 501012 pack | 4 | 18 | 8 | 3 | no | module top 8.62 > LID_Y 8 | 50.93 | 53.93 | 9.0 |
| A | 501012 pack | 3 | 18 | 8.5 | 0 | no | ADS1292_RSM overlaps switch | 47.90 | 50.90 | 9.5 |
| A | 501012 pack | 3 | 18 | 8.5 | 1.5 | no | ADS1292_RSM overlaps switch | 49.42 | 52.42 | 9.5 |
| A | 501012 pack | 3 | 18 | 8.5 | 3 | no | TOTAL_CHORD 50.93 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 50.93 | 53.93 | 9.5 |
| A | 501012 pack | 4 | 18 | 8.5 | 0 | no | module top 8.62 > LID_Y 8.5 | 47.90 | 50.90 | 9.5 |
| A | 501012 pack | 4 | 18 | 8.5 | 1.5 | no | module top 8.62 > LID_Y 8.5 | 49.42 | 52.42 | 9.5 |
| A | 501012 pack | 4 | 18 | 8.5 | 3 | no | module top 8.62 > LID_Y 8.5 | 50.93 | 53.93 | 9.5 |
| A | 501012 pack | 3 | 18 | 9 | 0 | no | ADS1292_RSM overlaps switch | 47.90 | 50.90 | 10.0 |
| A | 501012 pack | 3 | 18 | 9 | 1.5 | no | ADS1292_RSM overlaps switch | 49.42 | 52.42 | 10.0 |
| A | 501012 pack | 3 | 18 | 9 | 3 | no | TOTAL_CHORD 50.93 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 50.93 | 53.93 | 10.0 |
| A | 501012 pack | 4 | 18 | 9 | 0 | no | ADS1292_RSM overlaps switch | 47.90 | 50.90 | 10.0 |
| A | 501012 pack | 4 | 18 | 9 | 1.5 | no | ADS1292_RSM overlaps switch | 49.42 | 52.42 | 10.0 |
| A | 501012 pack | 4 | 18 | 9 | 3 | no | TOTAL_CHORD 50.93 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 50.93 | 53.93 | 10.0 |
| A | 501012 pack | 3 | 19 | 7 | 0 | no | module top 7.62 > LID_Y 7 | 47.90 | 50.90 | 8.0 |
| A | 501012 pack | 3 | 19 | 7 | 1.5 | no | module top 7.62 > LID_Y 7 | 49.42 | 52.42 | 8.0 |
| A | 501012 pack | 3 | 19 | 7 | 3 | no | module top 7.62 > LID_Y 7 | 50.93 | 53.93 | 8.0 |
| A | 501012 pack | 4 | 19 | 7 | 0 | no | module top 8.62 > LID_Y 7 | 47.90 | 50.90 | 8.0 |
| A | 501012 pack | 4 | 19 | 7 | 1.5 | no | module top 8.62 > LID_Y 7 | 49.42 | 52.42 | 8.0 |
| A | 501012 pack | 4 | 19 | 7 | 3 | no | module top 8.62 > LID_Y 7 | 50.93 | 53.93 | 8.0 |
| A | 501012 pack | 3 | 19 | 8 | 0 | yes | — | 47.90 | 50.90 | 9.0 |
| A | 501012 pack | 3 | 19 | 8 | 1.5 | no | TOTAL_CHORD 49.42 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 49.42 | 52.42 | 9.0 |
| A | 501012 pack | 3 | 19 | 8 | 3 | no | TOTAL_CHORD 50.93 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 50.93 | 53.93 | 9.0 |
| A | 501012 pack | 4 | 19 | 8 | 0 | no | module top 8.62 > LID_Y 8 | 47.90 | 50.90 | 9.0 |
| A | 501012 pack | 4 | 19 | 8 | 1.5 | no | module top 8.62 > LID_Y 8 | 49.42 | 52.42 | 9.0 |
| A | 501012 pack | 4 | 19 | 8 | 3 | no | module top 8.62 > LID_Y 8 | 50.93 | 53.93 | 9.0 |
| A | 501012 pack | 3 | 19 | 8.5 | 0 | yes | — | 47.90 | 50.90 | 9.5 |
| A | 501012 pack | 3 | 19 | 8.5 | 1.5 | no | TOTAL_CHORD 49.42 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 49.42 | 52.42 | 9.5 |
| A | 501012 pack | 3 | 19 | 8.5 | 3 | no | TOTAL_CHORD 50.93 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 50.93 | 53.93 | 9.5 |
| A | 501012 pack | 4 | 19 | 8.5 | 0 | no | module top 8.62 > LID_Y 8.5 | 47.90 | 50.90 | 9.5 |
| A | 501012 pack | 4 | 19 | 8.5 | 1.5 | no | module top 8.62 > LID_Y 8.5 | 49.42 | 52.42 | 9.5 |
| A | 501012 pack | 4 | 19 | 8.5 | 3 | no | module top 8.62 > LID_Y 8.5 | 50.93 | 53.93 | 9.5 |
| A | 501012 pack | 3 | 19 | 9 | 0 | yes | — | 47.90 | 50.90 | 10.0 |
| A | 501012 pack | 3 | 19 | 9 | 1.5 | no | TOTAL_CHORD 49.42 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 49.42 | 52.42 | 10.0 |
| A | 501012 pack | 3 | 19 | 9 | 3 | no | TOTAL_CHORD 50.93 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 50.93 | 53.93 | 10.0 |
| A | 501012 pack | 4 | 19 | 9 | 0 | yes | — | 47.90 | 50.90 | 10.0 |
| A | 501012 pack | 4 | 19 | 9 | 1.5 | no | TOTAL_CHORD 49.42 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 49.42 | 52.42 | 10.0 |
| A | 501012 pack | 4 | 19 | 9 | 3 | no | TOTAL_CHORD 50.93 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 50.93 | 53.93 | 10.0 |
| A | 501012 pack | 3 | 20 | 7 | 0 | no | module top 7.62 > LID_Y 7 | 47.90 | 50.90 | 8.0 |
| A | 501012 pack | 3 | 20 | 7 | 1.5 | no | module top 7.62 > LID_Y 7 | 49.42 | 52.42 | 8.0 |
| A | 501012 pack | 3 | 20 | 7 | 3 | no | module top 7.62 > LID_Y 7 | 50.93 | 53.93 | 8.0 |
| A | 501012 pack | 4 | 20 | 7 | 0 | no | module top 8.62 > LID_Y 7 | 47.90 | 50.90 | 8.0 |
| A | 501012 pack | 4 | 20 | 7 | 1.5 | no | module top 8.62 > LID_Y 7 | 49.42 | 52.42 | 8.0 |
| A | 501012 pack | 4 | 20 | 7 | 3 | no | module top 8.62 > LID_Y 7 | 50.93 | 53.93 | 8.0 |
| A | 501012 pack | 3 | 20 | 8 | 0 | yes | — | 47.90 | 50.90 | 9.0 |
| A | 501012 pack | 3 | 20 | 8 | 1.5 | no | TOTAL_CHORD 49.42 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 49.42 | 52.42 | 9.0 |
| A | 501012 pack | 3 | 20 | 8 | 3 | no | TOTAL_CHORD 50.93 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 50.93 | 53.93 | 9.0 |
| A | 501012 pack | 4 | 20 | 8 | 0 | no | module top 8.62 > LID_Y 8 | 47.90 | 50.90 | 9.0 |
| A | 501012 pack | 4 | 20 | 8 | 1.5 | no | module top 8.62 > LID_Y 8 | 49.42 | 52.42 | 9.0 |
| A | 501012 pack | 4 | 20 | 8 | 3 | no | module top 8.62 > LID_Y 8 | 50.93 | 53.93 | 9.0 |
| A | 501012 pack | 3 | 20 | 8.5 | 0 | yes | — | 47.90 | 50.90 | 9.5 |
| A | 501012 pack | 3 | 20 | 8.5 | 1.5 | no | TOTAL_CHORD 49.42 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 49.42 | 52.42 | 9.5 |
| A | 501012 pack | 3 | 20 | 8.5 | 3 | no | TOTAL_CHORD 50.93 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 50.93 | 53.93 | 9.5 |
| A | 501012 pack | 4 | 20 | 8.5 | 0 | no | module top 8.62 > LID_Y 8.5 | 47.90 | 50.90 | 9.5 |
| A | 501012 pack | 4 | 20 | 8.5 | 1.5 | no | module top 8.62 > LID_Y 8.5 | 49.42 | 52.42 | 9.5 |
| A | 501012 pack | 4 | 20 | 8.5 | 3 | no | module top 8.62 > LID_Y 8.5 | 50.93 | 53.93 | 9.5 |
| A | 501012 pack | 3 | 20 | 9 | 0 | yes | — | 47.90 | 50.90 | 10.0 |
| A | 501012 pack | 3 | 20 | 9 | 1.5 | no | TOTAL_CHORD 49.42 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 49.42 | 52.42 | 10.0 |
| A | 501012 pack | 3 | 20 | 9 | 3 | no | TOTAL_CHORD 50.93 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 50.93 | 53.93 | 10.0 |
| A | 501012 pack | 4 | 20 | 9 | 0 | yes | — | 47.90 | 50.90 | 10.0 |
| A | 501012 pack | 4 | 20 | 9 | 1.5 | no | TOTAL_CHORD 49.42 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 49.42 | 52.42 | 10.0 |
| A | 501012 pack | 4 | 20 | 9 | 3 | no | TOTAL_CHORD 50.93 > M1−3 (49.00); M1=52 (Q34 blank, default.toml) | 50.93 | 53.93 | 10.0 |

8 of 144 close under every round-5 check. Drawings of those closers are not added under `docs/fab/cad/v1/`: the round-5 14-file kept set is pinned (`placement_v2_*.svg` = `kept_drawing_specs` of the 864-run matrix), and 14 + 8 would exceed the WP11b Q56 cap of 20.

- **501015 pack**: no body closes. Family that never clears: none (first conflict rotates). Winner-body first conflict: `BQ25100 overlaps header`. BODY_ARC TOTAL_CHORD 47.90 (same as the 501015 winner 47.90). +1.5 mm of arc on the winner body is 49.42 and fails M1−3 = 49.00. +3.0 mm of arc is 50.93 (+3.03 mm).

- **501012 pack**: smallest closer `A_pack501012_series_w19_y8_iII_s3`. Width 19 (-1 mm vs winner 20), LID_Y 8, standoff 3, arc+ 0. TOTAL_CHORD 47.90 against M1−3 = 49.00 (+0.00 mm vs winner 47.90). Outer thickness 9.0 (+0.0 mm vs winner 9.0).

First-conflict families (numbers masked), failing pack-cell runs:

| family | runs |
|---|---:|
| module top # > LID_Y # | 72 |
| TOTAL_CHORD # > M#−# (#); M#=# (Q# blank, default.toml) | 32 |
| module overlaps ADS#_RSM | 12 |
| ADS#_RSM overlaps switch | 8 |
| module overlaps switch | 8 |
| BQ# overlaps header | 4 |

### Smallest body per buyable cell (WP11b, L7 §2)

L7-research-v4.md §2 found no 501015-class cell sold in ones. The two buyable packs with page price, stock and a drawing are DTP301120 and LP501218JH.

| cell | sold in ones | smallest closer | width | lid | standoff | arc+ | TOTAL_CHORD | vs 501015 winner |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 501015 | no (L7 §2) | `A_501015_series_w20_y8_iII_s3` | 20 | 8 | 3 | 0 | 47.90 | — |
| DTP301120 | yes, SparkFun PRT-25270 | none | — | — | — | — | — | no closer |
| LP501218JH | yes, DigiKey (bare leads; needs a terminator) | none | — | — | — | — | — | no closer |
| 501015 pack | sheets (DNK/Benzo with PCM; L7 §7.8); not sold as a verified one-off here | none | — | — | — | — | — | no closer |
| 501012 pack | marketplace listing (eBay quote with PCM; L7 §7) | `A_pack501012_series_w19_y8_iII_s3` | 19 | 8 | 3 | 0 | 47.90 | — |

Extended (WP11b note 2): LID_Y 9.5, 10.0 and 10.5; widths 20, 21 and 22. A run packs if the only extra conflict is the plan's ≤ 9.0 high and 20 wide cap.

| cell | box | smallest closer | width | lid | outer | TOTAL_CHORD | height vs winner | chord vs winner | never-clears family |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 501015 | ≤9×20 | `A_501015_series_w20_y8_iII_s3` | 20 | 8 | 9.0 | 47.90 | — | — | — |
| DTP301120 | lid 9.5–10.5, w 20–22 | none | — | — | 11.5 | — | +2.5 mm still open | +0 / +3.03 mm, no closer | `SIG# tab crosses boss_# courtyard`, `cell overlaps standoff_SIG#` |
| LP501218JH | lid 9.5–10.5, w 20–22 | none | — | — | 11.5 | — | +2.5 mm still open | +0 / +3.03 mm, no closer | `cell overlaps standoff_SIG#` |
| 501015 pack | ≤9×20 II series (L7 §7) | none | — | — | 9.0 | 47.90 | — | — | `BQ25100 overlaps header` on winner body; none (first conflict rotates) |
| 501012 pack | ≤9×20 II series (L7 §7) | `A_pack501012_series_w19_y8_iII_s3` | 19 | 8 | 9.0 | 47.90 | +0.0 mm | +0.00 mm | — |

## 2. Clearance, stack, and first-conflict families

Cell packed height = body + foam 0.5: DTP301120 3.2 + 0.5 = 3.7; 501015 5.2 + 0.5 = 5.7; LP501218JH 5.4 + 0.5 = 5.9 (WP11b Jauch series, not in the 864-run matrix); 501015 pack 5 + 0.5 = 5.5; 501012 pack 5.1 + 0.5 = 5.6 (WP11b note 3, L7 §7, not in the 864-run matrix).
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

### REF tab route (WP11b, Q59)

Winner board `A_501015_series_w20_y8_iII_s3`, tail site CONTACT_REF (8.50, 43.00). Flex at the tab 0.31 (PI 0.11 + FR4 0.2). Bend R 1.5 (board-v2.md §11). The packing tab itself is unchanged (Stage B still measures the straight floor path).

| name | y | points | length | added | min wall | side wall | end wall | in cavity | bend R 1.5 |
|---|---|---|---:|---:|---:|---:|---|---|---|
| `along_floor` | 1.50–1.81 | (8.50, 43.00) → (8.50, 36.80) | 6.20 | +0.00 | 0.00 | 5.75 | s 38.20–39.25 at u 8.50 | no | yes |
| `along_lateral_wall` | 1.50–1.81 | (8.50, 43.00) → (2.75, 43.00) → (2.75, 36.80) → (8.50, 36.80) | 17.70 | +11.50 | 0.00 | 0.00 | s 38.20–39.25 at u 2.75 | no | yes |
| `over_pocket_air` | 7.30–7.61 | (8.50, 43.00) → (8.50, 36.80) | 6.20 | +0.00 | 0.00 | 5.75 | s 38.20–39.25 at u 8.50 | no | yes |

- `along_floor`: current packing tab, ring to board along s at u 8.50; cavity ends at s 38.20; Ø7.5 pocket starts at s 39.25; 1.05 mm of nylon between them
- `along_lateral_wall`: hug posterior inner wall at u 2.75, then to the ring; the ring is past the cavity, so the high-s leg leaves cavity air; cavity ends at s 38.20; Ø7.5 pocket starts at s 39.25; 1.05 mm of nylon between them
- `over_pocket_air`: same (u, s) as along_floor at y 7.30–7.61 (cell top 7.20 + 0.10, lid 8); cell-pocket free air at low s does not reach the tail site without the end wall; cavity ends at s 38.20; Ø7.5 pocket starts at s 39.25; 1.05 mm of nylon between them

No in-cavity route exists. The Ø7.5 tail pocket starts at s 39.25 and the cavity ends at s 38.20, so 1.05 mm of nylon sits between them. Every searched path crosses that wall. WP14 cuts a slot that contains the straight floor tab:

| item | number |
|---|---|
| name | `REF_end_wall_slot` |
| u | 7.25–9.75 (centre 8.50) |
| s | 38.20–39.25 (centre 38.73) |
| y | 1.50–1.81 |
| width | 2.50 |
| through (s) | 1.05 |
| height (y) | 0.31 |
| volume (rect) | 0.814 mm³ |


Stack at each site: floor 1.5, ring 0.31, brass standoff 3 (5 AF, circumradius 2.9) from y 1.81 to 4.81 = board underside. ISO 7380 M2.5×4 from outside projects 2.5 past the floor and ends 0.81 below the standoff top. No nut: the standoff's female thread takes the screw (plan v2 §5.3). The flex over the standoffs is not fastened to them; its retention is WP14's.
Harness 100 ± 3 mm: NOT_MEASURED (routed length, not a solid).

B and C do not close. There is no board-lane layout for them.

## 5b. Layout for the board lane, v2 (WP11c)

Real F.CrtYd and pad extents from `git show 845bac7:hardware/board/elicio-v2.kicad_pcb` (WP12b after dropping the shorting copper). Round-5 packing envelopes stay in the 864-run table. Courtyard-to-courtyard uses a 0.05 mm solder-mask-to-copper margin (DRC; two expansions = 0.10 mm pad-to-pad). Contact netclass clearance is 1.0 mm (WP12b `elicio-v2.kicad_pro`, nets SIG1/SIG2/REF).

### Part table — KiCad courtyard vs round 5

| ref | footprint | courtyard w × h | pad extent w × h | round-5 packing | Δw | Δh |
|---|---|---:|---:|---:|---:|---:|
| C1 | C_0402_1005Metric | 1.820 × 0.920 | 1.520 × 0.620 | — | — | — |
| C2 | C_0402_1005Metric | 1.820 × 0.920 | 1.520 × 0.620 | — | — | — |
| C3 | C_0402_1005Metric | 1.820 × 0.920 | 1.520 × 0.620 | — | — | — |
| C4 | C_0402_1005Metric | 1.820 × 0.920 | 1.520 × 0.620 | — | — | — |
| C5 | C_0402_1005Metric | 1.820 × 0.920 | 1.520 × 0.620 | — | — | — |
| C6 | C_0603_1608Metric | 2.960 × 1.460 | 2.450 × 0.950 | — | — | — |
| C7 | C_0603_1608Metric | 2.960 × 1.460 | 2.450 × 0.950 | — | — | — |
| C8 | C_0603_1608Metric | 2.960 × 1.460 | 2.450 × 0.950 | — | — | — |
| C9 | C_0603_1608Metric | 2.960 × 1.460 | 2.450 × 0.950 | — | — | — |
| C10 | C_0402_1005Metric | 1.820 × 0.920 | 1.520 × 0.620 | — | — | — |
| C11 | C_0402_1005Metric | 1.820 × 0.920 | 1.520 × 0.620 | — | — | — |
| C12 | C_0402_1005Metric | 1.820 × 0.920 | 1.520 × 0.620 | — | — | — |
| C13 | C_0402_1005Metric | 1.820 × 0.920 | 1.520 × 0.620 | — | — | — |
| C14 | C_0402_1005Metric | 1.820 × 0.920 | 1.520 × 0.620 | — | — | — |
| C15 | C_0603_1608Metric | 2.960 × 1.460 | 2.450 × 0.950 | — | — | — |
| D1 | D_SOD-523 | 2.500 × 1.400 | 2.100 × 0.600 | 2.20 × 1.00 | +0.30 | +0.40 |
| D2 | LED_0402_1005Metric | 1.860 × 0.940 | 1.560 × 0.640 | — | — | — |
| J1 | USB_C_Receptacle_HRO_TYPE-C-31-M-12 | 10.640 × 9.420 | 9.640 × 6.620 | 8.90 × 7.30 | +1.74 | +2.12 |
| J2 | JST_SH_SM02B-SRSS-TB_1x02-1MP_P1.00mm_Horizontal | 5.800 × 6.560 | 5.400 × 4.775 | 4.00 × 6.00 | +1.80 | +0.56 |
| J3 | PinHeader_1x03_P2.54mm_Horizontal | 12.310 × 8.620 | 1.700 × 6.780 | 7.60 × 2.50 | +4.71 | +6.12 |
| J4 | Tag-Connect_TC2030-IDC-NL_2x03_P1.27mm_Vertical | 7.000 × 4.000 | 6.071 × 3.023 | — | — | — |
| L1 | L_0603_1608Metric | 2.960 × 1.460 | 2.450 × 0.950 | — | — | — |
| P1 | RING_PAD_D5_H2.7 | 6.400 × 6.400 | 5.000 × 5.000 | — | — | — |
| P2 | RING_PAD_D5_H2.7 | 6.400 × 6.400 | 5.000 × 5.000 | — | — | — |
| P3 | RING_PAD_D5_H2.7 | 6.400 × 6.400 | 5.000 × 5.000 | — | — | — |
| Q1 | SOT-23 | 3.860 × 3.400 | 2.475 × 3.375 | — | — | — |
| Q2 | SOT-23 | 3.860 × 3.400 | 2.475 × 3.375 | — | — | — |
| Q3 | SOT-23 | 3.860 × 3.400 | 2.475 × 3.375 | — | — | — |
| Q4 | SOT-23 | 3.860 × 3.400 | 2.475 × 3.375 | — | — | — |
| Q5 | SOT-23 | 3.860 × 3.400 | 2.475 × 3.375 | — | — | — |
| R1 | R_0402_1005Metric | 1.860 × 0.940 | 1.660 × 0.540 | 1.80 × 0.90 | +0.06 | +0.04 |
| R2 | R_0402_1005Metric | 1.860 × 0.940 | 1.660 × 0.540 | 1.80 × 0.90 | +0.06 | +0.04 |
| R3 | R_0402_1005Metric | 1.860 × 0.940 | 1.560 × 0.640 | 1.80 × 0.90 | +0.06 | +0.04 |
| R4 | R_0402_1005Metric | 1.860 × 0.940 | 1.560 × 0.640 | — | — | — |
| R5 | R_0402_1005Metric | 1.860 × 0.940 | 1.560 × 0.640 | — | — | — |
| R6 | R_0402_1005Metric | 1.860 × 0.940 | 1.560 × 0.640 | — | — | — |
| R7 | R_0402_1005Metric | 1.860 × 0.940 | 1.560 × 0.640 | — | — | — |
| R8 | R_0402_1005Metric | 1.860 × 0.940 | 1.560 × 0.640 | — | — | — |
| R9 | R_0402_1005Metric | 1.860 × 0.940 | 1.660 × 0.540 | — | — | — |
| R10 | R_0402_1005Metric | 1.860 × 0.940 | 1.660 × 0.540 | — | — | — |
| R11 | R_0402_1005Metric | 1.860 × 0.940 | 1.560 × 0.640 | — | — | — |
| R12 | R_0402_1005Metric | 1.860 × 0.940 | 1.560 × 0.640 | — | — | — |
| R13 | R_0402_1005Metric | 1.860 × 0.940 | 1.560 × 0.640 | — | — | — |
| R14 | R_0402_1005Metric | 1.860 × 0.940 | 1.560 × 0.640 | — | — | — |
| R15 | R_0402_1005Metric | 1.860 × 0.940 | 1.560 × 0.640 | — | — | — |
| R16 | R_0402_1005Metric | 1.860 × 0.940 | 1.560 × 0.640 | — | — | — |
| R17 | R_0402_1005Metric | 1.860 × 0.940 | 1.560 × 0.640 | — | — | — |
| R18 | R_0402_1005Metric | 1.860 × 0.940 | 1.660 × 0.540 | — | — | — |
| R19 | R_0402_1005Metric | 1.860 × 0.940 | 1.660 × 0.540 | — | — | — |
| R20 | R_0402_1005Metric | 1.860 × 0.940 | 1.560 × 0.640 | — | — | — |
| R21 | R_0402_1005Metric | 1.860 × 0.940 | 1.560 × 0.640 | — | — | — |
| R22 | R_0402_1005Metric | 1.860 × 0.940 | 1.560 × 0.640 | — | — | — |
| R23 | R_0402_1005Metric | 1.860 × 0.940 | 1.560 × 0.640 | — | — | — |
| R24 | R_0402_1005Metric | 1.860 × 0.940 | 1.560 × 0.640 | — | — | — |
| R25 | R_0402_1005Metric | 1.860 × 0.940 | 1.560 × 0.640 | — | — | — |
| R26 | R_0402_1005Metric | 1.860 × 0.940 | 1.560 × 0.640 | — | — | — |
| R27 | R_0402_1005Metric | 1.860 × 0.940 | 1.560 × 0.640 | — | — | — |
| R28 | R_0402_1005Metric | 1.860 × 0.940 | 1.560 × 0.640 | — | — | — |
| R29 | R_0402_1005Metric | 1.860 × 0.940 | 1.560 × 0.640 | — | — | — |
| R30 | R_0402_1005Metric | 1.860 × 0.940 | 1.560 × 0.640 | — | — | — |
| SW1 | SW_Push_1P1T_XKB_TS-1187A | 7.500 × 5.600 | 7.000 × 4.500 | 4.50 × 4.50 | +3.00 | +1.10 |
| U1 | Raytac_MDBT50Q | 11.500 × 16.500 | 10.200 × 11.400 | 10.50 × 15.50 | +1.00 | +1.00 |
| U2 | VQFN-32-1EP_4x4mm_P0.4mm_EP2.8x2.8mm | 5.260 × 5.260 | 4.750 × 4.750 | 5.00 × 5.00 | +0.26 | +0.26 |
| U3 | Texas_YFP0006 | 2.960 × 3.500 | 0.650 × 1.050 | 2.10 × 1.40 | +0.86 | +2.10 |
| U4 | SOT-23-5 | 4.100 × 3.400 | 3.600 × 2.500 | 3.30 × 2.90 | +0.80 | +0.50 |
| U5 | SOT-23-6 | 4.100 × 3.400 | 3.600 × 2.500 | 3.30 × 2.90 | +0.80 | +0.50 |

Keep-outs on that board (zone bbox from the same KiCad file):

| name | x0 | y0 | x1 | y1 |
|---|---:|---:|---:|---:|
| J4_USB_C_keepout | 14.46 | 4.13 | 15.73 | 6.67 |
| RF_FEED_NOTCH | 6.05 | 33.05 | 7.25 | 34.65 |
| RF_NO_COPPER | 2.25 | 26.15 | 6.05 | 38.55 |
| RING_REF_CLEAR | 5.00 | 39.50 | 12.00 | 46.50 |
| RING_SIG1_CLEAR | -8.25 | 18.50 | -1.25 | 25.50 |
| RING_SIG2_CLEAR | 21.25 | 29.60 | 28.25 | 36.60 |
| unnamed_keepout_2 | 6.05 | 33.05 | 7.25 | 34.65 |
| unnamed_keepout_3 | 2.25 | 26.15 | 6.00 | 38.55 |

### Rules the search must meet

| rule | source |
|---|---|
| JLC FPC assembly, body to board edge ≥ 2.5 mm | board-v2.md §12 / L6 |
| copper to outline ≥ 0.30 mm | board-v2.md §12; DRC min_copper_edge_clearance |
| courtyard-to-courtyard ≥ 0, with solder-mask bridge margin 0.10 mm | WP11c brief; DRC solder_mask_to_copper_clearance 0.05 mm |
| Contact netclass clearance 1.0 mm | WP12b elicio-v2.kicad_pro |
| module keep-out empty of everything | Raytac Spec K; RF_NO_COPPER |
| J4 on the hook-end end face with its plug volume | packing-v2.md §5; plan v2 §5.4 |
| SW1 under the lid recess | packing-v2.md §5 |
| J3 and TC2030 reachable | WP11c brief |
| USB-C real body inside the outline behind the end face | tasks/reviews/code-r6.md decision 70 |
| three FR4 0.2 ring stiffener pieces on the tabs; ring 0.31 stays | tasks/reviews/code-r6.md decision 72 |
| two island mounting holes at the boss sites, Ø2.7, courtyard-clear | tasks/reviews/code-r6.md decision 73 |
| SIG1/SIG2 fold 180° at R 1.5; neck-end or side-wall pockets | tasks/reviews/code-r6.md decision 74 |

### 501012 pack, w20 × y8, BODY_ARC, interface II, standoff 3 (the shell as built)

Spec `A_pack501012_series_w20_y8_iII_s3`. TOTAL_CHORD 47.90. Board u 2.25–17.75, s 16.00–37.60.

**First rule that cannot be met:** JLC FPC assembly edge 2.5 mm (board-v2.md §12 / L6): U1 body 10.5×15.5 at the packing pose (long along u) sits 0.00 mm from the island edge u 2.25–17.75 (width 15.50). JLC wants 2.5 mm. Turning U1 long-along-s needs island 15.5×20.5; this island is 15.50×21.60, so U1 can meet 2.5 mm on the short sides only if nothing else shares that 10.5 mm strip. U2 courtyard 5.26 cannot sit beside U1 under that rule. First rule that cannot be met.

| rule | met | detail |
|---|---|---|
| JLC FPC assembly edge 2.5 mm (board-v2.md §12 / L6) | no | U1 body 10.5×15.5 at the packing pose (long along u) sits 0.00 mm from the island edge u 2.25–17.75 (width 15.50). JLC wants 2.5 mm. Turning U1 long-along-s needs island 15.5×20.5; this island is 15.50×21.60, so U1 can meet 2.5 mm on the short sides only if nothing else shares that 10.5 mm strip. U2 courtyard 5.26 cannot sit beside U1 under that rule. First rule that cannot be met. |
| copper-to-edge 0.30 (board-v2.md §12) | no | U1 pad-edge 0.150 < 0.30 |
| courtyard-to-courtyard ≥ 0 with solder-mask bridge margin 0.10 | yes | no courtyard overlap among placed parts |
| Contact netclass 1.0 mm (WP12b elicio-v2.kicad_pro) | no | R1/R2/R3 0402 pad gap 0.48 mm < 1.0 mm (SIG1–AFE_IN1P, SIG2–AFE_IN1N, REF–RLD_FB). A 2.5 mm tab cannot hold the 0402 and that clearance. See variants A and B. |
| module keep-out empty (RF_NO_COPPER / U1 antenna) | yes | no non-U1 footprint in RF_NO_COPPER |
| J4 on the hook-end end face with its plug volume | no | J4 not placed |
| SW1 under the lid recess | no | SW1 not placed |
| J3 and TC2030 reachable | no | missing J4 |
| every WP12b footprint placed | no | unplaced: SW1, J4, Q1, Q2, Q3, Q4, Q5, R30 |
| USB-C real body inside the outline behind the end face (code-r6.md decision 70) | no | J1 F.CrtYd 10.64×9.42×3.2; packing hang 4.80 mm, courtyard hang 5.86 mm past s=-1.00 (J1 s0=-6.86). Opening u0=5.50 vs hook root u≤6.39 (overlap 0.89 mm). Longer body needs +7.32 mm of arc, M1 ≥ 58.29 (default 52); hook-root shift 2.4 mm clears the opening only. What closes it: nothing. |
| three FR4 0.2 ring stiffener pieces on the tabs; ring 0.31 stays (code-r6.md decision 72) | yes | 3 pieces FR4 0.2 at SIG1, SIG2 and REF; ring stack PI 0.11 + FR4 0.2 = 0.31 stays. Island Eco1 still 2× FR4 0.4. FR4 piece count 5 (JLC extra-fee threshold 4). |
| two island mounting holes at the boss sites, Ø2.7, courtyard-clear (code-r6.md decision 73) | no | holes at (14.85, 21.50) and (14.85, 28.10), Ø2.7, keep box 3.30. U1 covers (14.85, 28.10) |
| SIG1/SIG2 fold 180° at R 1.5; neck-end or side-wall pockets (code-r6.md decision 74) | yes | R 1.5, arc 4.71 mm, stand-out 1.6 mm. Neck-end: SIG1 10.71 mm, SIG2 21.81 mm; pocket s 14.40–16.00 × 3.50 × 3.00. Side-wall: SIG1 8.36 mm, SIG2 12.06 mm; pocket 0.85 × 3.50 × 3.00, wall left 0.65 mm. Same numbers for PCB, packing table and shell. |

- Contact 1.0 mm (WP12b netclass Contact) cannot hold on a 2.5 mm tab with an 0402 across it (pad gap 0.48 mm). Variant A: R1/R2/R3 on the island at the tab root; each tab carries one Contact trace.
- Variant B: widen each tab to 4.0 mm so an 0402 can sit on the tab with 1.0 mm to other copper. The 0402 pad gap 0.48 mm still violates Contact-to-Default 1.0 mm; that needs a larger package or a DRC exception.
- Decision 70 (`tasks/reviews/code-r6.md`): USB-C J1 real body 10.64×9.42×3.2 (F.CrtYd from 845bac7; height from packing / plan v2 §5.4; the amendment names the J4 land, which is TC2030). Packing hang 4.80 mm past s=-1.00; real courtyard hang 5.86 mm. Opening u0=5.50 overlaps hook root u≤6.39 by 0.89 mm. A longer body that seats the body behind the face needs +7.32 mm of arc (cell moved back); chord 55.29, M1 ≥ 58.29 vs default 52. Hook-root shift 2.4 mm clears the opening and the 1.5 mm ligament; it does not pull the body inside. **What closes it: nothing.**
- Decision 74 (`tasks/reviews/code-r6.md`): SIG1/SIG2 fold 180° at R 1.5 (arc 4.71 mm, stand-out 1.6 mm). Same numbers for the PCB, the packing table and the shell. Neck-end variant: SIG1 strip 10.71 mm, SIG2 strip 21.81 mm; fold pocket in the neck drop s 14.40–16.00, 3.50 × 3.00 (no side-wall cut). Side-wall variant: SIG1 strip 8.36 mm, SIG2 strip 12.06 mm; fold pocket 0.85 deep × 3.50 along s × 3.00 along y in each side wall (remaining wall 0.65 mm).

Contact sites are unchanged: SIG1 (5.90, 22.00), SIG2 (10.40, 33.10), REF (8.50, 43.00). REF tab (8.50, 43.00) → (8.50, 36.80); `REF_end_wall_slot` is cut.

| ref | u | s | rot | courtyard wu × ws | face | notes |
|---|---:|---:|---:|---:|---|---|
| C1 | 8.31 | 17.61 | 0 | 1.82 × 0.92 | top | passive grid |
| C2 | 8.81 | 16.61 | 0 | 1.82 × 0.92 | top | passive grid |
| C3 | 10.81 | 25.11 | 0 | 1.82 × 0.92 | top | passive grid |
| C4 | 12.81 | 24.11 | 0 | 1.82 × 0.92 | top | passive grid |
| C5 | 12.81 | 25.11 | 0 | 1.82 × 0.92 | top | passive grid |
| C6 | 15.38 | 24.38 | 0 | 2.96 × 1.46 | top | passive grid |
| C7 | 13.58 | 3.88 | 0 | 2.96 × 1.46 | pocket | passive grid |
| C8 | 13.58 | 3.38 | 0 | 2.96 × 1.46 | pocket | passive grid, pocket |
| C9 | 13.58 | 5.38 | 0 | 2.96 × 1.46 | pocket | passive grid, pocket |
| C10 | 15.31 | 16.61 | 0 | 1.82 × 0.92 | top | passive grid |
| C11 | 15.31 | 19.11 | 0 | 1.82 × 0.92 | top | passive grid |
| C12 | 13.01 | 2.11 | 0 | 1.82 × 0.92 | pocket | passive grid |
| C13 | 16.51 | 3.61 | 0 | 1.82 × 0.92 | pocket | passive grid |
| C14 | 16.51 | 4.61 | 0 | 1.82 × 0.92 | pocket | passive grid |
| C15 | 13.58 | 7.38 | 0 | 2.96 × 1.46 | pocket | passive grid, pocket |
| D1 | 15.50 | 2.35 | 0 | 2.50 × 1.40 | pocket | PESD VBUS |
| D2 | 6.83 | 16.62 | 0 | 1.86 × 0.94 | top | LED |
| J1 | 10.00 | -2.15 | 0 | 10.64 × 9.42 | top | USB hook-end end face (fallback) |
| J2 | 20.40 | 8.00 | 0 | 5.80 × 6.56 | pocket | JST-SH; hangs off the pocket high-u wall |
| J3 | 24.75 | 21.32 | 0 | 12.31 × 8.62 | top | bench header; pins hang off the high-u outline |
| L1 | 3.88 | 16.88 | 0 | 2.96 × 1.46 | top | 10 µH |
| P1 | 5.90 | 22.00 | 0 | 6.40 × 6.40 | floor | SIG1 folded site |
| P2 | 10.40 | 33.10 | 0 | 6.40 × 6.40 | floor | SIG2 folded site |
| P3 | 8.50 | 43.00 | 0 | 6.40 × 6.40 | floor | REF site; REF_end_wall_slot |
| R1 | 6.40 | 17.62 | 0 | 1.86 × 0.94 | top | 220 kΩ variant A: island at tab root |
| R2 | 15.60 | 17.65 | 0 | 1.86 × 0.94 | top | 220 kΩ variant A: island at tab root |
| R3 | 10.50 | 24.12 | 0 | 1.86 × 0.94 | top | 220 kΩ variant A: island at tab root |
| R4 | 17.57 | 12.58 | 90 | 0.94 × 1.86 | pocket | passive grid |
| R5 | 13.03 | 9.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R6 | 13.03 | 10.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R7 | 13.03 | 11.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R8 | 13.03 | 12.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R9 | 13.03 | 13.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R10 | 13.03 | 14.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R11 | 15.03 | 9.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R12 | 15.03 | 10.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R13 | 15.03 | 11.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R14 | 15.03 | 12.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R15 | 15.03 | 13.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R16 | 15.03 | 14.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R17 | 16.53 | 2.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R18 | 16.53 | 3.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R19 | 16.53 | 4.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R20 | 16.53 | 5.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R21 | 16.53 | 6.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R22 | 16.53 | 7.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R23 | 16.53 | 8.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R24 | 17.03 | 9.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R25 | 17.03 | 10.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R26 | 17.03 | 11.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R27 | 17.03 | 12.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R28 | 17.03 | 13.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R29 | 17.03 | 14.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| U1 | 10.00 | 32.35 | 90 | 16.50 × 11.50 | top | packing centre; courtyard 11.5×16.5 at rot 90 |
| U2 | 14.73 | 8.00 | 0 | 5.26 × 5.26 | pocket | ADS1292 |
| U3 | 11.38 | 21.40 | 0 | 2.96 × 3.50 | top | BQ25100 |
| U4 | 11.95 | 17.85 | 0 | 4.10 × 3.40 | top | TLV71330 |
| U5 | 15.00 | 12.50 | 0 | 4.10 × 3.40 | pocket | USBLC6 |

Tab exits (unchanged): SIG1 (5.90, 22.00) → (5.90, 29.00); SIG2 (10.40, 33.10) → (10.40, 26.10); REF (8.50, 43.00) → (8.50, 36.80). Island outline u 2.25–17.75, s as in the spec row. WP12d places from this table and tests within 0.1 mm.

### 501015 pack 17.0×10.0×5.0 at +1.5 mm of arc (valid only if M1 ≥ 52.5)

Spec `A_pack501015_series_w20_y8_iII_s3_a1.5`. TOTAL_CHORD 49.42. Board u 2.25–17.75, s 20.00–39.10.

**First rule that cannot be met:** M1 ≥ TOTAL_CHORD + 3 (Q34); 17 mm pack at +1.5 only if M1 ≥ 52.5: TOTAL_CHORD 49.42, need M1 ≥ 52.42; default.toml M1=52

| rule | met | detail |
|---|---|---|
| M1 ≥ TOTAL_CHORD + 3 (Q34); 17 mm pack at +1.5 only if M1 ≥ 52.5 | no | TOTAL_CHORD 49.42, need M1 ≥ 52.42; default.toml M1=52 |
| JLC FPC assembly edge 2.5 mm (board-v2.md §12 / L6) | no | U1 body 10.5×15.5 at the packing pose (long along u) sits 0.00 mm from the island edge u 2.25–17.75 (width 15.50). JLC wants 2.5 mm. Turning U1 long-along-s needs island 15.5×20.5; this island is 15.50×19.10, so U1 can meet 2.5 mm on the short sides only if nothing else shares that 10.5 mm strip. U2 courtyard 5.26 cannot sit beside U1 under that rule. First rule that cannot be met. |
| copper-to-edge 0.30 (board-v2.md §12) | no | U1 pad-edge 0.150 < 0.30 |
| courtyard-to-courtyard ≥ 0 with solder-mask bridge margin 0.10 | yes | no courtyard overlap among placed parts |
| Contact netclass 1.0 mm (WP12b elicio-v2.kicad_pro) | no | R1/R2/R3 0402 pad gap 0.48 mm < 1.0 mm (SIG1–AFE_IN1P, SIG2–AFE_IN1N, REF–RLD_FB). A 2.5 mm tab cannot hold the 0402 and that clearance. See variants A and B. |
| module keep-out empty (RF_NO_COPPER / U1 antenna) | no | inside RF_NO_COPPER: P3 |
| J4 on the hook-end end face with its plug volume | no | J1 USB wall hook-end end face (fallback) (USB courtyard 10.64×9.42 fills that face). J4 at (15.10, 15.25) rot 90 face pocket |
| SW1 under the lid recess | no | SW1 not placed |
| J3 and TC2030 reachable | no | missing J3 |
| every WP12b footprint placed | no | unplaced: SW1, U5, J3, Q1, Q2, Q3, Q4, Q5 |
| USB-C real body inside the outline behind the end face (code-r6.md decision 70) | no | J1 F.CrtYd 10.64×9.42×3.2; packing hang 4.80 mm, courtyard hang 5.86 mm past s=-1.00 (J1 s0=-6.86). Opening u0=5.50 vs hook root u≤6.39 (overlap 0.89 mm). Longer body needs +7.32 mm of arc, M1 ≥ 59.80 (default 52); hook-root shift 2.4 mm clears the opening only. What closes it: nothing. |
| three FR4 0.2 ring stiffener pieces on the tabs; ring 0.31 stays (code-r6.md decision 72) | yes | 3 pieces FR4 0.2 at SIG1, SIG2 and REF; ring stack PI 0.11 + FR4 0.2 = 0.31 stays. Island Eco1 still 2× FR4 0.4. FR4 piece count 5 (JLC extra-fee threshold 4). |
| two island mounting holes at the boss sites, Ø2.7, courtyard-clear (code-r6.md decision 73) | no | holes at (14.85, 21.50) and (14.85, 28.10), Ø2.7, keep box 3.30. U1 covers (14.85, 28.10) |
| SIG1/SIG2 fold 180° at R 1.5; neck-end or side-wall pockets (code-r6.md decision 74) | yes | R 1.5, arc 4.71 mm, stand-out 1.6 mm. Neck-end: SIG1 6.71 mm, SIG2 17.81 mm; pocket s 18.40–20.00 × 3.50 × 3.00. Side-wall: SIG1 8.36 mm, SIG2 12.06 mm; pocket 0.85 × 3.50 × 3.00, wall left 0.65 mm. Same numbers for PCB, packing table and shell. |

- Contact 1.0 mm (WP12b netclass Contact) cannot hold on a 2.5 mm tab with an 0402 across it (pad gap 0.48 mm). Variant A: R1/R2/R3 on the island at the tab root; each tab carries one Contact trace.
- Variant B: widen each tab to 4.0 mm so an 0402 can sit on the tab with 1.0 mm to other copper. The 0402 pad gap 0.48 mm still violates Contact-to-Default 1.0 mm; that needs a larger package or a DRC exception.
- Decision 70 (`tasks/reviews/code-r6.md`): USB-C J1 real body 10.64×9.42×3.2 (F.CrtYd from 845bac7; height from packing / plan v2 §5.4; the amendment names the J4 land, which is TC2030). Packing hang 4.80 mm past s=-1.00; real courtyard hang 5.86 mm. Opening u0=5.50 overlaps hook root u≤6.39 by 0.89 mm. A longer body that seats the body behind the face needs +7.32 mm of arc (cell moved back); chord 56.80, M1 ≥ 59.80 vs default 52. Hook-root shift 2.4 mm clears the opening and the 1.5 mm ligament; it does not pull the body inside. **What closes it: nothing.**
- Decision 74 (`tasks/reviews/code-r6.md`): SIG1/SIG2 fold 180° at R 1.5 (arc 4.71 mm, stand-out 1.6 mm). Same numbers for the PCB, the packing table and the shell. Neck-end variant: SIG1 strip 6.71 mm, SIG2 strip 17.81 mm; fold pocket in the neck drop s 18.40–20.00, 3.50 × 3.00 (no side-wall cut). Side-wall variant: SIG1 strip 8.36 mm, SIG2 strip 12.06 mm; fold pocket 0.85 deep × 3.50 along s × 3.00 along y in each side wall (remaining wall 0.65 mm).

Contact sites are unchanged: SIG1 (5.90, 22.00), SIG2 (10.40, 33.10), REF (8.50, 43.00). REF tab (8.50, 43.00) → (8.50, 36.80); `REF_end_wall_slot` is cut.

| ref | u | s | rot | courtyard wu × ws | face | notes |
|---|---:|---:|---:|---:|---|---|
| C1 | 8.81 | 26.11 | 0 | 1.82 × 0.92 | top | passive grid |
| C2 | 10.81 | 24.61 | 0 | 1.82 × 0.92 | top | passive grid |
| C3 | 10.81 | 25.61 | 0 | 1.82 × 0.92 | top | passive grid |
| C4 | 10.81 | 26.61 | 0 | 1.82 × 0.92 | top | passive grid |
| C5 | 12.81 | 25.61 | 0 | 1.82 × 0.92 | top | passive grid |
| C6 | 13.48 | 3.38 | 0 | 2.96 × 1.46 | pocket | passive grid, pocket |
| C7 | 13.48 | 5.38 | 0 | 2.96 × 1.46 | pocket | passive grid, pocket |
| C8 | 13.48 | 7.38 | 0 | 2.96 × 1.46 | pocket | passive grid, pocket |
| C9 | 13.48 | 9.38 | 0 | 2.96 × 1.46 | pocket | passive grid, pocket |
| C10 | 12.36 | 27.06 | 90 | 0.92 × 1.82 | top | passive grid |
| C11 | 12.46 | 12.06 | 90 | 0.92 × 1.82 | pocket | passive grid |
| C12 | 12.46 | 14.06 | 90 | 0.92 × 1.82 | pocket | passive grid |
| C13 | 12.46 | 16.06 | 90 | 0.92 × 1.82 | pocket | passive grid |
| C14 | 17.46 | 2.56 | 90 | 0.92 × 1.82 | pocket | passive grid |
| C15 | 13.48 | 11.38 | 0 | 2.96 × 1.46 | pocket | passive grid, pocket |
| D1 | 15.00 | 24.35 | 0 | 2.50 × 1.40 | top | PESD VBUS |
| D2 | 6.83 | 26.12 | 0 | 1.86 × 0.94 | top | LED |
| J1 | 10.00 | -2.15 | 0 | 10.64 × 9.42 | top | USB hook-end end face (fallback) |
| J2 | 20.40 | 8.00 | 0 | 5.80 × 6.56 | pocket | JST-SH; hangs off the pocket high-u wall |
| J4 | 15.10 | 15.25 | 90 | 4.00 × 7.00 | pocket | TC2030; reachable from the leftover high-u edge |
| L1 | 3.88 | 26.38 | 0 | 2.96 × 1.46 | top | 10 µH |
| P1 | 5.90 | 22.00 | 0 | 6.40 × 6.40 | floor | SIG1 folded site |
| P2 | 10.40 | 33.10 | 0 | 6.40 × 6.40 | floor | SIG2 folded site |
| P3 | 8.50 | 43.00 | 0 | 6.40 × 6.40 | floor | REF site; REF_end_wall_slot |
| R1 | 6.40 | 27.12 | 0 | 1.86 × 0.94 | top | 220 kΩ variant A: island at tab root |
| R2 | 15.60 | 25.65 | 0 | 1.86 × 0.94 | top | 220 kΩ variant A: island at tab root |
| R3 | 8.50 | 27.50 | 0 | 1.86 × 0.94 | top | 220 kΩ variant A: island at tab root |
| R4 | 12.93 | 13.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R5 | 12.93 | 14.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R6 | 12.93 | 15.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R7 | 12.93 | 16.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R8 | 12.93 | 17.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R9 | 12.93 | 18.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R10 | 14.93 | 13.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R11 | 14.93 | 14.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R12 | 14.93 | 15.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R13 | 14.93 | 16.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R14 | 14.93 | 17.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R15 | 14.93 | 18.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R16 | 16.43 | 2.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R17 | 16.43 | 3.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R18 | 16.43 | 4.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R19 | 16.43 | 5.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R20 | 16.43 | 6.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R21 | 16.43 | 7.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R22 | 16.43 | 8.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R23 | 16.43 | 9.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R24 | 16.43 | 10.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R25 | 16.43 | 11.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R26 | 16.43 | 12.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R27 | 16.93 | 13.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R28 | 16.93 | 14.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R29 | 16.93 | 15.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| R30 | 16.93 | 16.12 | 0 | 1.86 × 0.94 | pocket | passive grid, pocket |
| U1 | 10.00 | 33.85 | 90 | 16.50 × 11.50 | top | packing centre; courtyard 11.5×16.5 at rot 90 |
| U2 | 14.63 | 8.00 | 0 | 5.26 × 5.26 | pocket | ADS1292 |
| U3 | 11.38 | 21.90 | 0 | 2.96 × 3.50 | top | BQ25100 |
| U4 | 14.55 | 3.35 | 0 | 4.10 × 3.40 | pocket | TLV71330 |

Tab exits (unchanged): SIG1 (5.90, 22.00) → (5.90, 29.00); SIG2 (10.40, 33.10) → (10.40, 26.10); REF (8.50, 43.00) → (8.50, 36.80). Island outline u 2.25–17.75, s as in the spec row. WP12d places from this table and tests within 0.1 mm.

### Round 6 decisions 70–74 (`tasks/reviews/code-r6.md`)

These rules were added after the first WP11c close. The USB-C land on 845bac7 is J1 (`USB_C_Receptacle_HRO_TYPE-C-31-M-12`). J4 is TC2030. Height 3.2 mm is packing `USB` / plan v2 §5.4 (board-v2.md §12 is the stackup, not a 3D size).

**Decision 70.** Real body 10.64 × 9.42 × 3.2. Packing hangs 4.80 mm past the outer face s=-1.00; the courtyard hangs 5.86 mm. The hook root occupies u up to 6.39 on that face; the opening starts at u=5.50 (overlap 0.89 mm) so the opening cannot sit there without a 2.4 mm posterior move of the hook root (overlap + 1.5 mm ligament). Seating the body behind the face needs +7.32 mm of arc with the cell moved back: chord 55.29, M1 ≥ 58.29 against default.toml M1=52. The hook-root move does not pull the body inside. **What closes it: nothing.**

**Decision 72.** Three FR4 0.2 ring stiffener pieces exist on the tabs (SIG1, SIG2, REF). Ring stack 0.31 stays (PI 0.11 + FR4 0.2). Island Eco1 still has 2 pieces of FR4 0.4. FR4 piece count 5 (JLC extra-fee threshold 4).

**Decision 73.** Two mounting holes in the island at the boss sites (14.85, 21.50) and (14.85, 28.10), Ø2.7, courtyard keep 3.30 mm. Courtyard hits: U1 covers (14.85, 28.10).

**Decision 74.** SIG1/SIG2 fold 180° at R 1.5. Either they leave the island at its neck end, or the side walls get fold pockets and the strips grow. The same number is used for the PCB, the packing table and the shell.

| pack | variant | SIG1 strip | SIG2 strip | pocket |
|---|---|---:|---:|---|
| 501012 BODY_ARC | neck-end | 10.71 | 21.81 | s 14.40–16.00, 3.50 × 3.00 (neck drop; no side-wall cut) |
| 501012 BODY_ARC | side-wall pockets | 8.36 | 12.06 | 0.85 deep × 3.50 along s × 3.00 along y; wall left 0.65 |
| 501015 +1.5 mm arc | neck-end | 6.71 | 17.81 | s 18.40–20.00, 3.50 × 3.00 (neck drop; no side-wall cut) |
| 501015 +1.5 mm arc | side-wall pockets | 8.36 | 12.06 | 0.85 deep × 3.50 along s × 3.00 along y; wall left 0.65 |

Drawings: this layout does not add `placement_v2_*.svg` under `docs/fab/cad/v1/`. The round-5 14-file kept set is pinned, and the layout does not fully close every rule (Q56).

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
| LP501218JH | 20 × 12.5 × 5.4 | Jauch LP501218JH+PCM+2 WIRE 50MM; DigiKey 1908-LP501218JH+PCM+2WIRE50MM-ND; L7-research-v4.md §2 |
| 501015 pack | 17 × 10 × 5 | DNK Power DNK501015 'Dimensions: 17 × 10 × 5.0 mm'; Benzo '5mm x 10mm x 17mm'; L7-research-v4.md §7 and §7.8 |
| 501012 pack | 13 × 10.1 × 5.1 | eBay quote 'approx 13.0mm x 10.1mm x 5.1mm' with PCM, 40 mAh; L7-research-v4.md §7 |
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
| Flex tab bend (WP11b REF search) | R 1.5 | board-v2.md §11 |
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
- REF tab lid-to-wall gap: packing treats the cavity end wall as solid from floor 1.5 to LID_Y 8.0; a gap under the lid was not probed on the solid.
- 501015 pack in ones: none found (`docs/fab/L7-research-v4.md` §2). DTP301120 is sold in ones (SparkFun PRT-25270). LP501218JH is sold in ones (DigiKey 1908-LP501218JH+PCM+2WIRE50MM-ND) with bare 2-wire leads; plan v2 R2, Rolf solders nothing, so it is a candidate only if the assembler or the seller terminates the leads. This package does not order.
- 501015 pack with PCM: DNK/Benzo sheets give 17 × 10 × 5.0 (L7-research-v4.md §7 and §7.8). The 17.0 mm pack was not probed on a solid; packing arithmetic only. The 501012 13.0 × 10.1 × 5.1 figure is an eBay marketplace quote (L7 §7), not a manufacturer sheet.

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

