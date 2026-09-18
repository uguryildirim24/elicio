# Pin table v2 — flat PCB coordinates (WP12e)

Copied from packing-v2.md §5d at `408a476`.
Board pins this table. The folded-site table is the shell's and is not copied.
P4/P5 flat centres (37.47, 2.80) and (30.05, 5.80) through the rib-slot fold.
CHARGE rectangle centre (33.02, 4.30) 14.50 × 8.60 is part of the flat outline.
J4 NPTH keep-out Ø1.39 both sides.

## 5d. Flat pattern and pin table v2 (WP11e, Q85)

Build cell: process-edge, width 22, chord 47.90, two sides, fold neck, no receptacle (Q81). Island u 2.25–19.75, s 16.00–37.60. Leftover s 16.05–20.90. The flex board is drawn flat. The §5c pin table still lists P1–P3 at the folded (shell) sites; pin table v2 below is what the board lane pins.

Fold allowance: inner R 1.5 mm, stack 0.31 mm (PI 0.11 + FR4 0.2). Arc at R is πR = 4.71 mm. Midplane arc π(R + t/2) = 5.20 mm. Q83 strip lengths use πR, so SIG1 10.71 mm and SIG2 21.81 mm stay. Flat length = folded run + πR. Folded run SIG1 = 6.00 mm, SIG2 = 17.10 mm.

Flat-to-folded mapping (neck-end, Q83): each SIG strip leaves the island at (contact u, s=16.00) toward −s. The ring centre in PCB coordinates is (contact u, s0 − L_flat). A 180° fold at R 1.5 at the neck puts the ring on the floor at the contact site. REF does not take that fold: it already leaves the island high-s end (s=37.60) through the end-wall slot, so P3 flat = P3 folded. P4 and P5 cannot sit on that tail: TOTAL_CHORD 47.90, loft s 45.5, Ø5 copper would need s ≤ 43.0, and the slot/REF dome/screw well leave no pair of Ø5 sites (largest tail pair Ø2.1). Folded sites stay on the hook-end medial floor beside the cell (Q86). The pocket island (SW1, U2) shares that XY at board height, so flat is not folded. The flex leaves leftover s=16.00 through the rib slot (s 14.90–15.70, u 11.90–20.50, height 0.31). Drop height 3.31 mm (underside 4.81 to floor 1.50). Two 90° bends at inner R 1.5 mm; allowance πR + 0.31 vertical = 5.02 mm, plus 1.00 mm past J2. A 90° unfold at the leftover corner maps 3D −s onto +u. P4 flat (37.47, 2.80); P5 flat (30.05, 5.80). The cell-side drop at u 11.90 is refused: SIG2's flat strip occupies u 9.15–11.65 through that s.

| strip | attach (u, s) | flat ring (u, s) | flat rectangle centre wu × ws | folded run | L_flat |
|---|---|---|---|---:|---:|
| SIG1 | (5.90, 16.00) | (5.90, 5.29) | (5.90, 10.64) 2.50 × 10.71 | 6.00 | 10.71 |
| SIG2 | (10.40, 16.00) | (10.40, -5.81) | (10.40, 5.09) 2.50 × 21.81 | 17.10 | 21.81 |
| REF | (8.50, 37.60) | (8.50, 43.00) | (8.50, 40.30) 2.50 × 5.40 | 5.40 | 5.40 |
| CHARGE | leftover s=16.00, u 11.90–20.50 | P4 (37.47, 2.80); P5 (30.05, 5.80) | (33.02, 4.30) 14.50 × 8.60 | P4 11.70; P5 4.28 | P4 17.72; P5 10.30 |

2D check: the flat pattern does not self-overlap. No SIG, REF or CHARGE strip crosses a part on either side of the leftover or the pocket. P1–P5 flat centres sit outside every other courtyard. Neck-end is the SIG exit. Side-wall pockets stay refused (remaining wall 0.65 mm < 1.0).

Flat-pattern drawing: `docs/fab/cad/v2c/placement_v2c_process_norec_w22_c47.90_two.svg` (strips and ring pads in PCB coordinates; at most four drawings, Q56).

### Pin table v2 — flat PCB coordinates (width 22, chord 47.90, two sides, fold neck)

68 rows (66 footprints including P4/P5, plus H1 and H2). Side column as in §5c. Pad-to-outline ≥ 0.30. Holes at the Q82 sites. SW1 in the lid recess. Contact variant A. P1, P2, P4 and P5 are the FLAT ring centres (not the folded sites). P4 and P5 keep RING_PAD_D5_H2.7 courtyards. Folded they sit on the hook-end medial floor inside the cavity, with pad-to-outline ≥ 0.30. They replace the side-wall sites (0.75, 44.00) and (21.25, 44.00) and the off-body tail sites (5.05, 49.50) and (16.95, 49.50). The board lane pins this table within 0.1 mm. The shell lane ignores it and takes the folded-site table.

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
| D1 | top | 3.95 | 17.15 | 0 | 2.50 × 1.40 | PESD VBUS |
| D2 | top | 9.63 | 16.92 | 0 | 1.86 × 0.94 | LED |
| J2 | top | 22.40 | 10.93 | 0 | 5.80 × 6.56 | JST-SH |
| J3 | top | 26.11 | 20.31 | 0 | 12.31 × 8.62 | bench header; pins hang off the high-u outline |
| J4 | top | 16.25 | 24.60 | 90 | 4.00 × 7.00 | TC2030 leftover; NPTH keep-out both sides (Q85) |
| L1 | top | 6.98 | 17.18 | 0 | 2.96 × 1.46 | 10 µH |
| P1 | floor | 5.90 | 5.29 | 0 | 6.40 × 6.40 | SIG1 ring; Q79 tab carries one Contact trace; FLAT PCB (Q85); folded site in the shell table |
| P2 | floor | 10.40 | -5.81 | 0 | 6.40 × 6.40 | SIG2 ring; FLAT PCB (Q85); folded site in the shell table |
| P3 | floor | 8.50 | 43.00 | 0 | 6.40 × 6.40 | REF ring; REF_end_wall_slot |
| P4 | floor | 37.47 | 2.80 | 0 | 6.40 × 6.40 | CHARGE_VBUS hook-end floor pad (Q81); RING_PAD_D5_H2.7; FLAT PCB (Q85); folded site in the shell table |
| P5 | floor | 30.05 | 5.80 | 0 | 6.40 × 6.40 | CHARGE_GND hook-end floor pad (Q81); RING_PAD_D5_H2.7; FLAT PCB (Q85); folded site in the shell table |
| Q1 | bottom | 4.48 | 27.60 | 0 | 3.86 × 3.40 | SOT-23 |
| Q2 | bottom | 4.48 | 31.20 | 0 | 3.86 × 3.40 | SOT-23 |
| Q3 | bottom | 4.48 | 34.80 | 0 | 3.86 × 3.40 | SOT-23 |
| Q4 | bottom | 8.48 | 27.60 | 0 | 3.86 × 3.40 | SOT-23 |
| Q5 | bottom | 11.68 | 21.20 | 0 | 3.86 × 3.40 | SOT-23 |
| R1 | top | 10.70 | 20.12 | 0 | 1.86 × 0.94 | 220 kΩ variant A: island at tab root |
| R2 | top | 17.87 | 32.03 | 90 | 0.94 × 1.86 | 220 kΩ variant A: island at tab root |
| R3 | top | 17.87 | 30.03 | 90 | 0.94 × 1.86 | 220 kΩ variant A: island at tab root |
| R4 | bottom | 14.68 | 19.97 | 0 | 1.86 × 0.94 | passive, second side |
| R5 | bottom | 14.68 | 25.17 | 0 | 1.86 × 0.94 | passive, second side |
| R6 | bottom | 14.68 | 28.77 | 0 | 1.86 × 0.94 | passive, second side |
| R7 | bottom | 15.08 | 29.97 | 0 | 1.86 × 0.94 | passive, second side |
| R8 | bottom | 15.08 | 31.17 | 0 | 1.86 × 0.94 | passive, second side |
| R9 | bottom | 15.08 | 32.37 | 0 | 1.86 × 0.94 | passive, second side |
| R10 | bottom | 15.08 | 33.57 | 0 | 1.86 × 0.94 | passive, second side |
| R11 | bottom | 15.08 | 34.77 | 0 | 1.86 × 0.94 | passive, second side |
| R12 | bottom | 15.08 | 35.97 | 0 | 1.86 × 0.94 | passive, second side |
| R13 | bottom | 16.68 | 19.97 | 0 | 1.86 × 0.94 | passive, second side |
| R14 | bottom | 16.68 | 25.17 | 0 | 1.86 × 0.94 | passive, second side |
| R15 | bottom | 16.68 | 28.77 | 0 | 1.86 × 0.94 | passive, second side |
| R16 | bottom | 17.08 | 23.57 | 0 | 1.86 × 0.94 | passive, second side |
| R17 | bottom | 17.08 | 29.97 | 0 | 1.86 × 0.94 | passive, second side |
| R18 | bottom | 17.08 | 31.17 | 0 | 1.86 × 0.94 | passive, second side |
| R19 | bottom | 17.08 | 32.37 | 0 | 1.86 × 0.94 | passive, second side |
| R20 | bottom | 17.08 | 33.57 | 0 | 1.86 × 0.94 | passive, second side |
| R21 | bottom | 17.08 | 34.77 | 0 | 1.86 × 0.94 | passive, second side |
| R22 | bottom | 17.08 | 35.97 | 0 | 1.86 × 0.94 | passive, second side |
| R23 | bottom | 18.28 | 21.17 | 0 | 1.86 × 0.94 | passive, second side |
| R24 | bottom | 18.28 | 22.37 | 0 | 1.86 × 0.94 | passive, second side |
| R25 | bottom | 7.82 | 17.23 | 90 | 0.94 × 1.86 | passive, second side |
| R26 | bottom | 14.22 | 21.63 | 90 | 0.94 × 1.86 | passive, second side |
| R27 | bottom | 18.22 | 25.23 | 90 | 0.94 × 1.86 | passive, second side |
| R28 | bottom | 18.62 | 27.23 | 90 | 0.94 × 1.86 | passive, second side |
| R29 | bottom | 18.62 | 29.23 | 90 | 0.94 × 1.86 | passive, second side |
| R30 | bottom | 18.62 | 31.23 | 90 | 0.94 × 1.86 | passive, second side |
| SW1 | top | 16.25 | 4.45 | 0 | 7.50 × 5.60 | lid, pocket island |
| U1 | top | 8.00 | 29.35 | 0 | 11.50 × 16.50 | process pose; courtyard 11.50×16.50 |
| U2 | top | 15.13 | 10.28 | 0 | 5.26 × 5.26 | ADS1292 |
| U3 | top | 15.68 | 30.85 | 0 | 2.96 × 3.50 | BQ25100 |
| U4 | top | 16.65 | 34.80 | 0 | 4.10 × 3.40 | TLV71330 |
| H1 | both | 13.45 | 17.70 | 0 | 3.30 × 3.30 | Ø2.7 island hole (Q82); keep 3.30; both sides |
| H2 | both | 17.95 | 17.70 | 0 | 3.30 × 3.30 | Ø2.7 island hole (Q82); keep 3.30; both sides |

### J4 NPTH keep-out both sides (Q85)

Tag-Connect TC2030-IDC-NL in `hardware/board/elicio-v2.kicad_pcb`: 3 NPTH, drill 0.9906 mm. `elicio-v2.kicad_pro` min_hole_clearance 0.20 mm. Keep-out diameter = drill + 2 × clearance = 1.39 mm. No B.Cu footprint may enter that zone. Same-face courtyard keep-out on F.Cu stands.

| hole | u | s | drill | keep | sides |
|---|---:|---:|---:|---:|---|
| J4-NPTH1 | 16.25 | 22.06 | 0.9906 | 1.39 | F.Cu and B.Cu |
| J4-NPTH2 | 17.27 | 27.14 | 0.9906 | 1.39 | F.Cu and B.Cu |
| J4-NPTH3 | 15.23 | 27.14 | 0.9906 | 1.39 | F.Cu and B.Cu |

Drawings (at most four, Q56) live under `docs/fab/cad/v2c/` so the round-5 14-file `placement_v2_*.svg` set in `docs/fab/cad/v1/` stays pinned.
This package keeps `placement_v2c_process_usb_w22_c47.90_two.svg`, `placement_v2c_body_usb_w22_c47.90_two.svg`, `placement_v2c_process_norec_w22_c47.90_two.svg`, `placement_v2c_body_norec_w22_c47.90_two.svg`.
