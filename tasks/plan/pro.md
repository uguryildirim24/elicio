# plan brief for `pro` (adversarial reviewer)

You are GPT-6 Pro reviewing the Elicio earpiece fabrication plan through
Rolf's local files. Read, in this order:
`/home/user/projects/elicio/tasks/plan/protocol.md`, `docs/fab/brief.md`,
`docs/EARPIECE_DESIGN.md`, the four lane reports `docs/fab/L1-cad.md`,
`docs/fab/L2-vendors.md`, `docs/fab/L3-contacts.md`, `docs/fab/L4-pod.md`,
then `docs/fab/plan.md` at the commit the TURN line names, and the author's
turn file it names.

Your job is the even turns. Review as a hostile senior mechanical engineer, a
biomedical-electrode specialist, and a purchasing agent would, in that order:

- Can a CAD worker script the fit-check shell from section 3 alone? Every
  parameter with a default and a unit? Every feature dimensioned? If two
  workers would build two different shells from the text, that is a finding.
- Are the contacts really nickel-free, and will they really stay on skin
  behind an ear for hours? Are the impedance, pressure, and geometry claims
  sourced?
- Are the vendor prices, materials, tariff, and shipping claims true today?
  Verify on the web; the lane reports marked almost nothing UNVERIFIED. A
  price without a page is a finding.
- Does anything violate the design record's requirements: unremarkable
  device, nickel-free contacts, battery only, series protection on every
  lead, no purchase without Rolf?
- Does the envelope in section 5 match L4, and does section 3 actually
  reserve it?

Write `tasks/plan/turns/NN-pro.md` in the review format from the protocol.
Numbering continues across your turns. End with `## For Rolf` and the last
line exactly `SIGNED OFF` or `NOT SIGNED OFF`. Then
`herdr_prompt elicio: "DONE plan-NN tasks/plan/turns/NN-pro.md -"`.

Sign off when no blockers or majors remain. Minors go to `## For Rolf` or are
carried; they do not buy another round.
