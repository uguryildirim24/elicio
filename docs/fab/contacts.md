# Contact hardware: current constraints and reference inputs

Rolf selected titanium skin-contact hardware. No hardware has been ordered, assembled, screened or worn. Material, finish, pressure, retention and electrical behavior are unverified. The current candidate is the v4 flex board with the snap shell, not the old ring-lug assembly.

## Current candidate

The board and shell design use contact branches, ring lands and threaded standoffs. The historical cost worksheet assumes M2.5 contact screws and 3 mm standoffs with 5 mm across-flats geometry. Those catalogue assumptions do not qualify the actual parts or the folded assembly.

Before fabrication, resolve:

- Exact screw material, finish, head dimensions, length and thread engagement.
- Standoff material, geometry and contact with the board ring land.
- Skin-contact pressure, surface condition and retention.
- Insulation from foreign copper, the battery and charging hardware.
- Changes under printing tolerance, flex bending and repeated assembly.
- Electrical protection and charging behavior on the actual routed board.

The proposed charging contacts are on the posterior wall and charging is off-ear only. Neither the location nor a software inhibit establishes isolation or a safe fault current. Qualified electrical review and bench validation must precede on-body evaluation.

## Retained v1 reference dimensions

The older generator and placement checks still use the TE 31428 ring-lug envelope. That is a reference fixture, not a part selected for the current flex-tab assembly.

| Reference input | Dimension used by the existing scripts |
| --- | ---: |
| Lug thickness | approximately 0.46 mm |
| Barrel width | 1.96 mm |
| Ring-centre to barrel-end distance | 8.85 mm |
| Lead bend radius | 3 mm |
| Original contact-head reservation | 4.7 mm diameter, 1.35 mm crown |

These values explain the v1 placement drawings and stack checks. They do not certify a supplier part, crimp, nickel content or skin compatibility. Do not reuse the cancelled lug/nut shopping basket or assembly recipe for v4.

The historical source was TE Customer Drawing C-31428 revision D4. Source pointers are retained in [references](references.md). Recheck the maker drawing and actual supplied part before using a dimension in a new design.

## Evidence limits

Nominal continuity and geometry are different from measured contact stability. No adhesion, force, sweat, cleaning, fault-current or repeated-wear result exists. An agent-written material claim or a home screening suggestion is not qualification of a wearable part.

Keep any future material certificates and engineering measurements distinct from personal health records. Personal recordings and anatomy information belong in ignored local directories. See [open hardware gates](open-questions.md), [board design](board-v4-design.md) and [shell limits](shell-v4.md).
