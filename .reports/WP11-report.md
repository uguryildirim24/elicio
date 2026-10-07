# WP11 report — packing v2, turn 09 (fourth DONE)

Lane `w1`, branch `lane/w1`, package WP11. Coordinator note 4 / plan v2
turn 09: standoffs 3.0, 3.5 and 4.0; cell under the board only with
positive nominal clearance; board bends 0.5 onto the bosses; 0.5 floor
recess at 3.5 and 4.0 (web 1.0); cell carries no load; report module
stack and outer height. The plan file was not edited.

## What was built

864 runs (720 Interface I including recess variants, 144 Interface II).
Table and sources: `docs/fab/packing-v2.md`.

### DTP 3.2 + foam 0.3 = 3.5 under the board

| standoff | recess | nominal | deformed | under-board | load |
|---|---:|---:|---:|---|---|
| 3.0 | 0 | −0.5 | −1.0 | no | carries load |
| 3.5 | 0 | 0.0 | −0.5 | no | carries load |
| 4.0 | 0 | +0.5 | 0.0 | yes | carries load |
| 3.5 | 0.5 | +0.5 | 0.0 | yes | carries load |
| 4.0 | 0.5 | +1.0 | +0.5 | yes | no load |

Turn 09: 4.0 with no recess, deformed clearance 0.0. 3.5 with no recess, deformed −0.5.
Only DTP + 4.0 + recess 0.5 has positive deformed clearance. It still hits SIG1 (22 mm cell from s 1.5). 501015 packed 5.5 never has positive clearance.

### Module stack (standoff + board 1.0 + module) and outer at zero added clearance

Floor 1.5 + lid 1.0.

| arch | standoff | stack | outer0 |
|---|---:|---:|---:|
| A | 3.0 | 6.3 | 8.8 |
| A | 3.5 | 6.8 | 9.3 |
| A | 4.0 | 7.3 | 9.8 |
| B | 3.0 | 6.0 | 8.5 |
| B | 3.5 | 6.5 | 9.0 |
| B | 4.0 | 7.0 | 9.5 |

outer@lid in the run table is LID_Y + 1.0. Module-to-lid is packing, not a solid probe. C15 residual web is NOT_MEASURED.

Interface I: 0/720 close. Interface II: same four A 501015 series w20 closers. Stage B toml unchanged (`A_501015_series_w20_y8_iII_s3`).

## Gates

`.venv/bin/python -m unittest discover -s tests -v` — OK (full suite after 864 drawings). Order 1 identity and two consecutive Stage B still green from CadRegenTests / CadStageBV2BuildTests in that run.

## Needs a decision

1. Interface I still does not close: clearance/load, outer 9.3–9.8 on 3.5/4.0 for A, and DTP vs SIG1.
2. G5/G7 must still prove worst-case clearance to the deformed board. WP11 numbers are packing arithmetic.
3. C15 does not approve the 0.5 recess.
4. USB remains hook-end end face (fallback).

## Final commit sha

`7df78b5`
