# Pin table v3 — flat PCB coordinates (WP12i)

Copied from packing-v2.md §5e at `ab9ce95`.
Board pins this table. The folded-site table is the shell's and is not copied.
§5d in packing-v2.md is the frozen v2.1 table. §5e is live.

## 5e. Flat pattern v3 and pin table v3 (WP11g, Q90–Q95, Q97, Q98)

Build cell: process-edge, width 22, chord 47.90, two sides, fold neck, no receptacle (Q81). Island u 2.25–19.75, s 16.00–37.60. Leftover s 16.05–20.90. The flex board is drawn flat. Pin table v3 below is what the board lane pins.

Posterior wall: u 20.50–22.00. montage.md §2.1: u is the posterior offset from the body's anterior edge (u = 0). shell-v2.md: the hook root sits at low u on the hook-end face and the hook curves forward over the top of the ear. params/default.toml HOOK_ROOT_X = 4.0. packing-v2.md: the hook root occupies u up to 6.39. The far wall from that root is the posterior edge hidden behind the ear, so P4/P5 go there (Q90). The anterior wall u 0–1.50 is not used. The hook-end end-face fallback is not used.

Fold allowance: inner R 1.5 mm, stack 0.31 mm (PI 0.11 + FR4 0.2). Arc at R for a 180° SIG fold is πR = 4.71 mm. Midplane arc π(R + t/2) = 5.20 mm. Q83 strip lengths use πR, so SIG1 10.71 mm and SIG2 21.81 mm stay. The CHARGE tab uses one 90° at R 1.5: πR/2 = 2.36 mm plus wall run 0.46 mm (island underside 4.81 to pad y 4.35).

Flat-to-folded mapping (neck-end, Q83): each SIG strip leaves the island at (contact u, s=16.00) toward −s. The ring centre in PCB coordinates is (contact u, s0 − L_flat). A 180° fold at R 1.5 at the neck puts the ring on the floor at the contact site. REF does not take that fold: it already leaves the island high-s end (s=37.60) through the end-wall slot, so P3 flat = P3 folded. P4 and P5 cannot sit on that tail (largest tail pair Ø2.1) and they cannot sit on the skin face (Q90). The CHARGE tab leaves the pocket island's high-u edge (the inner face of the posterior wall), folds 90° at R 1.5 onto that wall's inner face, and carries RING_PAD_D5_H2.7 clamped button-heads: head through the 1.50 wall, ring on the inner face, 3.0 standoff into the bay. It does not use J2's hang and it does not use the leftover rib slot (Q92). P4 flat (23.32, 4.35); P5 flat (23.32, 12.35).

| strip | attach (u, s) | flat ring (u, s) | flat rectangle centre wu × ws | folded run | L_flat |
|---|---|---|---|---:|---:|
| SIG1 | (5.90, 16.00) | (5.90, 5.29) | (5.90, 10.64) 2.50 × 10.71 | 6.00 | 10.71 |
| SIG2 | (10.40, 16.00) | (10.40, -5.81) | (10.40, 5.09) 2.50 × 21.81 | 17.10 | 21.81 |
| REF | (8.50, 37.60) | (8.50, 43.00) | (8.50, 40.30) 2.50 × 5.40 | 5.40 | 5.40 |
| CHARGE | pocket high-u edge (20.50, s 4.35–12.35) | P4 (23.32, 4.35); P5 (23.32, 12.35) | (23.32, 8.35) 5.64 × 13.64 | wall run 0.46 | 2.82 |

2D check: the flat pattern does not self-overlap. No SIG, REF or CHARGE strip crosses a part on either side of the leftover or the pocket. P1–P5 flat centres sit outside every other courtyard. Neck-end is the SIG exit. Side-wall pockets stay refused (remaining wall 0.65 mm < 1.0).

Cavity test: every courtyard, hang and folded-board region lies inside the cavity (u 1.50–20.50) or on a declared exterior. Declared exteriors: the SIG strips before folding, and the J3 break-off tab. Remove the J3 break-off tab after programming and before closing the shell.

J2 (JST-SH) is inside the cavity at (15.15, 11.35) rot 0; the cell connector is reachable from that site.
J3 sits on a break-off tab at (28.41, 26.80) rot 0, joined by a 2.5 mm neck. Cut line at u = 22.25, s = 26.80. Remove the J3 break-off tab after programming and before closing the shell.

Flat-pattern drawing: `docs/fab/cad/v2c/placement_v2c_process_norec_w22_c47.90_two.svg` (strips, CHARGE rectangle, J3 cut line; at most four drawings, Q56).

### Pin table v3 — flat PCB coordinates (width 22, chord 47.90, two sides, fold neck)

66 rows (64 parts including P4/P5, plus H1 and H2). R9 and R10 are DNP without the receptacle (Q95); they return with the USB-C variant (Q81). Side column as in §5c. Pad-to-outline ≥ 0.30. Holes at the Q82/Q98 sites, keep 3.30; the keep-out gap takes three Default tracks. SW1 in the lid recess. Contact variant A. P1, P2, P4 and P5 are the FLAT ring centres (not the folded sites). P4 and P5 keep RING_PAD_D5_H2.7 courtyards. Second-side height ≤ 3.31 mm. Q97: no other courtyard inside a land 7 × 7 zone. The board lane pins this table within 0.1 mm. The shell lane takes the wall-site table.

| ref | side | u | s | rot | courtyard wu × ws | notes |
|---|---|---:|---:|---:|---:|---|
| C1 | top | 10.41 | 18.11 | 0 | 1.82 × 0.92 | passive |
| C2 | top | 12.81 | 20.11 | 0 | 1.82 × 0.92 | passive |
| C3 | top | 18.96 | 8.56 | 90 | 0.92 × 1.82 | passive |
| C4 | top | 18.96 | 10.56 | 90 | 0.92 × 1.82 | passive |
| C5 | top | 18.96 | 12.56 | 90 | 0.92 × 1.82 | passive |
| C6 | bottom | 11.03 | 23.83 | 0 | 2.96 × 1.46 | passive, second side |
| C7 | bottom | 12.03 | 25.43 | 0 | 2.96 × 1.46 | passive, second side |
| C8 | bottom | 12.03 | 27.03 | 0 | 2.96 × 1.46 | passive, second side |
| C9 | bottom | 12.03 | 28.63 | 0 | 2.96 × 1.46 | passive, second side |
| C10 | bottom | 3.46 | 16.76 | 0 | 1.82 × 0.92 | passive, second side |
| C11 | bottom | 10.46 | 18.76 | 0 | 1.82 × 0.92 | passive, second side |
| C12 | bottom | 14.66 | 19.96 | 0 | 1.82 × 0.92 | passive, second side |
| C13 | bottom | 14.66 | 28.76 | 0 | 1.82 × 0.92 | passive, second side |
| C14 | bottom | 15.06 | 29.96 | 0 | 1.82 × 0.92 | passive, second side |
| C15 | bottom | 15.63 | 31.43 | 0 | 2.96 × 1.46 | passive, second side |
| D1 | top | 3.95 | 17.15 | 0 | 2.50 × 1.40 | PESD VBUS |
| D2 | top | 9.63 | 16.92 | 0 | 1.86 × 0.94 | LED |
| J2 | top | 15.15 | 11.35 | 0 | 5.80 × 6.56 | JST-SH; cell connector reachable; inside cavity (Q91) |
| J3 | top | 28.41 | 26.80 | 0 | 12.31 × 8.62 | bench header; break-off tab, cut before closing (Q91) |
| J4 | top | 16.52 | 24.60 | 90 | 4.00 × 7.00 | TC2030 leftover; via slot west of J4; NPTH keep-out both sides (Q85, Q98) |
| L1 | top | 6.98 | 17.18 | 0 | 2.96 × 1.46 | 10 µH |
| P1 | floor | 5.90 | 5.29 | 0 | 6.40 × 6.40 | SIG1 ring; Q79 tab carries one Contact trace; FLAT PCB (Q85); folded site in the shell table |
| P2 | floor | 10.40 | -5.81 | 0 | 6.40 × 6.40 | SIG2 ring; FLAT PCB (Q85); folded site in the shell table |
| P3 | floor | 8.50 | 43.00 | 0 | 6.40 × 6.40 | REF ring; REF_end_wall_slot |
| P4 | wall | 23.32 | 4.35 | 0 | 6.40 × 6.40 | CHARGE_VBUS clamped button-head (Q90); posterior side wall u 20.50–22.00; head +u; RING_PAD_D5_H2.7; FLAT PCB (Q85); folded site in the shell table |
| P5 | wall | 23.32 | 12.35 | 0 | 6.40 × 6.40 | CHARGE_GND clamped button-head (Q90); posterior side wall u 20.50–22.00; head +u; RING_PAD_D5_H2.7; FLAT PCB (Q85); folded site in the shell table |
| Q1 | bottom | 4.48 | 27.60 | 0 | 3.86 × 3.40 | SOT-23 |
| Q2 | bottom | 4.48 | 31.20 | 0 | 3.86 × 3.40 | SOT-23 |
| Q3 | bottom | 4.48 | 34.80 | 0 | 3.86 × 3.40 | SOT-23 |
| Q4 | bottom | 8.48 | 27.60 | 0 | 3.86 × 3.40 | SOT-23 |
| Q5 | bottom | 11.68 | 21.20 | 0 | 3.86 × 3.40 | SOT-23 |
| R1 | top | 10.70 | 20.12 | 0 | 1.86 × 0.94 | 220 kΩ variant A: island at tab root |
| R2 | top | 19.07 | 32.83 | 90 | 0.94 × 1.86 | 220 kΩ variant A: island at tab root |
| R3 | top | 19.07 | 30.83 | 90 | 0.94 × 1.86 | 220 kΩ variant A: island at tab root |
| R4 | bottom | 15.08 | 32.77 | 0 | 1.86 × 0.94 | passive, second side |
| R5 | bottom | 15.08 | 33.97 | 0 | 1.86 × 0.94 | passive, second side |
| R6 | bottom | 15.08 | 35.17 | 0 | 1.86 × 0.94 | passive, second side |
| R7 | bottom | 15.08 | 36.37 | 0 | 1.86 × 0.94 | passive, second side |
| R8 | bottom | 15.68 | 23.37 | 0 | 1.86 × 0.94 | passive, second side |
| R11 | bottom | 15.68 | 24.57 | 0 | 1.86 × 0.94 | passive, second side |
| R12 | bottom | 15.68 | 25.77 | 0 | 1.86 × 0.94 | passive, second side |
| R13 | bottom | 16.68 | 19.97 | 0 | 1.86 × 0.94 | passive, second side |
| R14 | bottom | 16.68 | 28.57 | 0 | 1.86 × 0.94 | passive, second side |
| R15 | bottom | 17.08 | 29.77 | 0 | 1.86 × 0.94 | passive, second side |
| R16 | bottom | 17.08 | 32.77 | 0 | 1.86 × 0.94 | passive, second side |
| R17 | bottom | 17.08 | 33.97 | 0 | 1.86 × 0.94 | passive, second side |
| R18 | bottom | 17.08 | 35.17 | 0 | 1.86 × 0.94 | passive, second side |
| R19 | bottom | 17.08 | 36.37 | 0 | 1.86 × 0.94 | passive, second side |
| R20 | bottom | 18.28 | 30.97 | 0 | 1.86 × 0.94 | passive, second side |
| R21 | bottom | 7.82 | 17.23 | 90 | 0.94 × 1.86 | passive, second side |
| R22 | bottom | 17.22 | 23.83 | 90 | 0.94 × 1.86 | passive, second side |
| R23 | bottom | 18.54 | 20.03 | 0 | 1.86 × 0.94 | passive, second side |
| R24 | bottom | 17.59 | 21.04 | 0 | 1.86 × 0.94 | passive, second side |
| R25 | bottom | 18.62 | 34.63 | 90 | 0.94 × 1.86 | passive, second side |
| R26 | bottom | 15.46 | 21.04 | 0 | 1.86 × 0.94 | passive, second side |
| R27 | bottom | 13.23 | 9.52 | 0 | 1.86 × 0.94 | passive, second side |
| R28 | bottom | 13.23 | 10.72 | 0 | 1.86 × 0.94 | passive, second side |
| R29 | bottom | 13.23 | 11.92 | 0 | 1.86 × 0.94 | passive, second side |
| R30 | bottom | 13.23 | 13.12 | 0 | 1.86 × 0.94 | passive, second side |
| SW1 | top | 15.97 | 4.45 | 0 | 7.50 × 5.60 | lid, pocket island |
| U1 | top | 8.00 | 29.35 | 0 | 11.50 × 16.50 | process pose; courtyard 11.50×16.50 |
| U2 | bottom | 14.85 | 4.45 | 0 | 5.26 × 5.26 | ADS1292 under SW1, second side |
| U3 | top | 16.08 | 31.25 | 0 | 2.96 × 3.50 | BQ25100 |
| U4 | top | 16.65 | 35.60 | 0 | 4.10 × 3.40 | TLV71330 |
| H1 | both | 13.23 | 17.70 | 0 | 3.30 × 3.30 | Ø2.7 island hole (Q82, Q98); keep 3.30; both sides; shell bosses follow |
| H2 | both | 17.95 | 17.70 | 0 | 3.30 × 3.30 | Ø2.7 island hole (Q82, Q98); keep 3.30; both sides; shell bosses follow |

### Shell table — floor sites and wall sites

P1–P3 floor sites are unchanged from §5. y is the ring seat on the inner floor (1.50 mm); head axis +y through the 1.50 medial wall. P4 and P5 are clamped button-heads in the posterior side wall (u 20.50–22.00): ring on the inner face, head through the 1.50 wall (+u), 3.0 standoff into the bay. Nylon between heads ≥ 3 mm. Wall around each seat ≥ 1.5 mm. Clear of the hinge lip (s 1.00–1.48, y 7.25–7.70, u 7.5–14.5) and of the cell pocket (u 1.80–11.90, s 1.50–14.50).

| pad | net | u | s | y | wall | head axis | courtyard | notes |
|---|---|---:|---:|---:|---|---|---|---|
| P1 | SIG1 | 5.90 | 22.00 | 1.50 | medial floor | +y | 6.40 × 6.40 | folded seat after the neck 180° fold |
| P2 | SIG2 | 10.40 | 33.10 | 1.50 | medial floor | +y | 6.40 × 6.40 | folded seat after the neck 180° fold |
| P3 | REF | 8.50 | 43.00 | 1.50 | medial floor | +y | 6.40 × 6.40 | folded seat after the neck 180° fold |
| P4 | CHARGE_VBUS | 20.50 | 4.35 | 4.35 | posterior side wall (u 20.50–22.00) | +u | 6.40 × 6.40 | clamped button-head; RING_PAD_D5_H2.7; 3.0 standoff into the bay (Q90) |
| P5 | CHARGE_GND | 20.50 | 12.35 | 4.35 | posterior side wall (u 20.50–22.00) | +u | 6.40 × 6.40 | clamped button-head; RING_PAD_D5_H2.7; 3.0 standoff into the bay (Q90) |

### Shell extras

Ø5 holes through the posterior wall at the wall sites (20.50, 4.35, y 4.35) and (20.50, 12.35, y 4.35), head axis +u. Rib slot s 14.90–15.70, u 11.90–20.50, height 0.31 mm: unused; leave it. Drop channel at leftover s=16.00: unused; leave it. REF_end_wall_slot is unchanged. Medial M2.5 well (WP14f): head at (16.50, 41.00), screw M2.5×8, tail boss OD 9.94 mm (moved from 14.50, 41.00 to clear the REF pocket). J3 break-off cut at u = 22.25. Remove the J3 break-off tab after programming and before closing the shell.

### J4 NPTH keep-out both sides (Q85)

Tag-Connect TC2030-IDC-NL from `git show 30ca79d:hardware/board/elicio-v2.kicad_pcb`: 3 NPTH, drill 0.9906 mm. `elicio-v2.kicad_pro` min_hole_clearance 0.20 mm. Keep-out diameter = drill + 2 × clearance = 1.39 mm. KiCad canvas Y increases down; at rot 90 the map is (u + py, s − px). No B.Cu pad may enter that zone. Same-face courtyard keep-out on F.Cu stands.

| hole | u | s | drill | keep | sides |
|---|---:|---:|---:|---:|---|
| J4-NPTH1 | 16.525 | 27.140 | 0.9906 | 1.39 | F.Cu and B.Cu |
| J4-NPTH2 | 15.509 | 22.060 | 0.9906 | 1.39 | F.Cu and B.Cu |
| J4-NPTH3 | 17.541 | 22.060 | 0.9906 | 1.39 | F.Cu and B.Cu |

### Routing channels (Q98)

WP12h could not close 63 rats on the island and named the millimetres in route.md §12. Those channels are packing constraints. Default track 0.10 + 2 × 0.10 clearance = 0.30 mm per track; three tracks between keep-outs need 0.70 mm. The H1/H2 keep-out gap was 1.20 mm; it is now 1.42 mm (0.12 more plus 0.10 mm margin). The shell's bosses follow H1/H2. The J4 via slot sits beside J4 on the west face, east of the locked SIG2 run at u 13.50 (west of that run is U1 copper). The east 0402 row (R16 and neighbours) stays out of that approach and out of the J4 holes. A 0.6 mm channel stays free on both sides around U2, U3 and J4 (U2/SW1 may share XY on opposite faces). The board tests this table.

| name | u_min | s_min | u_max | s_max | note |
|---|---:|---:|---:|---:|---|
| HOLE_CH | 14.880 | 16.050 | 16.300 | 19.350 | three Default tracks between H1/H2 keep-outs; gap 1.42 mm (need 1.42; 3×0.10+4×0.10=0.70) |
| U2_CH | 11.620 | 1.220 | 18.080 | 7.680 | 0.6 mm around U2 (B.Cu escape) |
| U3_CH | 14.000 | 28.900 | 18.160 | 33.600 | 0.6 mm around U3 (F.Cu escape) |
| J4_CH | 13.925 | 20.500 | 19.125 | 28.700 | 0.6 mm around J4, both sides |
| J4_VIA_SLOT | 13.775 | 21.100 | 14.525 | 28.100 | via slot beside J4, east of the SIG2 run at u 13.50 (west face of J4); width 0.75 mm, need 0.75 |
| J4_APPROACH_EAST | 18.525 | 20.500 | 21.025 | 28.700 | east 0402 row stays out of the J4 approach (R16 and neighbours) |


Drawings (at most four, Q56) live under `docs/fab/cad/v2c/` so the round-5 14-file `placement_v2_*.svg` set in `docs/fab/cad/v1/` stays pinned.
This package keeps `placement_v2c_process_usb_w22_c47.90_two.svg`, `placement_v2c_body_usb_w22_c47.90_two.svg`, `placement_v2c_process_norec_w22_c47.90_two.svg`, `placement_v2c_body_norec_w20_c47.90_two.svg`.
