#!/bin/zsh
# v4_finish.sh ROUTED.kicad_pcb TAG — from v4_route_pf.py's output (GND groups still live, pours unfilled) to a
# filled, DRC'd board <dir of ROUTED>/TAG_final.kicad_pcb (design note §9.5). One router or KiCad batch at a time.
#   1. DRC, drop the conflicting copper, reconnect every net (the GND groups included), rip-up 4
#   2. GND names restored, refill, GND finisher with the pours as copper, stitching vias/tracks, twice
#   3. thermal stubs, then the soft-fill finisher for what is still open, GND again
#   4. final DRC with the project rules and --schematic-parity
set -e
HERE=${0:A:h}
PY=$HERE/../../.venv/bin/python
IN=$1; T=$2; W=${IN:h}
prep() { cp $HERE/elicio-v4.kicad_pro $W/$1.kicad_pro; cp $HERE/elicio-v4.kicad_dru $W/$1.kicad_dru; cp $HERE/elicio-v4.kicad_sch $W/$1.kicad_sch; }
drc() { prep $1; kicad-cli pcb drc --refill-zones --save-board --format json $2 -o $W/$1_drc.json $W/$1.kicad_pcb >/dev/null 2>&1 || true; $PY $HERE/v4_drcsum.py $W/$1_drc.json | head -3; }
cp $IN $W/${T}0.kicad_pcb; prep ${T}0
kicad-cli pcb drc --format json -o $W/${T}0_drc.json $W/${T}0.kicad_pcb >/dev/null 2>&1 || true
$PY -u $HERE/v4_route_fix.py --pcb $W/${T}0.kicad_pcb --drop-drc $W/${T}0_drc.json --ripup 4 --out $W/${T}1.kicad_pcb | grep -v '^  ' | tail -3
$PY $HERE/v4_gnd_split.py --back $W/${T}1.kicad_pcb $W/${T}2.kicad_pcb
drc ${T}2
$PY -u $HERE/v4_route_fix.py --pcb $W/${T}2.kicad_pcb --nets GND --ripup 4 --out $W/${T}3.kicad_pcb | grep -v '^  ' | tail -2
$PY $HERE/v4_stitch.py $W/${T}3.kicad_pcb GND $W/${T}4.kicad_pcb 1.5 | grep -v '^   OPEN' | tail -3
drc ${T}4
$PY -u $HERE/v4_route_fix.py --pcb $W/${T}4.kicad_pcb --nets GND --ripup 4 --out $W/${T}5.kicad_pcb | grep -v '^  ' | tail -2
$PY $HERE/v4_stitch.py $W/${T}5.kicad_pcb GND $W/${T}6.kicad_pcb 1.5 | grep -v '^   OPEN' | tail -3
drc ${T}6
$PY $HERE/v4_thermal_stubs.py $W/${T}6.kicad_pcb $W/${T}6_drc.json $W/${T}7.kicad_pcb 0.8 | tail -1
drc ${T}7
$PY -u $HERE/v4_route_fix.py --pcb $W/${T}7.kicad_pcb --soft-fills --ripup 8 --pen 6 --out $W/${T}8.kicad_pcb | grep -v '^  ' | tail -3
drc ${T}8
$PY -u $HERE/v4_route_fix.py --pcb $W/${T}8.kicad_pcb --soft-fills --nets GND --ripup 4 --pen 6 --out $W/${T}9.kicad_pcb | grep -v '^  ' | tail -2
$PY $HERE/v4_stitch.py $W/${T}9.kicad_pcb GND $W/${T}10.kicad_pcb 1.5 | grep -v '^   OPEN' | tail -3
drc ${T}10
$PY $HERE/v4_thermal_stubs.py $W/${T}10.kicad_pcb $W/${T}10_drc.json $W/${T}11.kicad_pcb 0.8 | tail -1
prep ${T}11
kicad-cli pcb drc --refill-zones --save-board --format json --schematic-parity -o $W/${T}11_drc.json $W/${T}11.kicad_pcb 2>&1 | grep -i found
$PY $HERE/v4_drcsum.py $W/${T}11_drc.json
cp $W/${T}11.kicad_pcb $W/${T}_final.kicad_pcb
echo "final at $W/${T}_final.kicad_pcb (saved with filled zones)"
