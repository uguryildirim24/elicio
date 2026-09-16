# Elicio earpiece — fabrication brief

Rolf, 2026-09-16:

> we design the airpiece in blender or something and i get it custom made in
> china or something

He also set the working rule for this phase: every web search runs as an
Antigravity (`agy`, Gemini) lane in herdr, per the round-table skill.

## Where this starts from

`docs/EARPIECE_DESIGN.md` (decided 2026-08-13) is the design record and stays
authoritative. What matters for fabrication:

- One device at one site: a behind-the-ear pod, plausible as a normal
  earpiece. Nothing about the act of commanding may be visible.
- Primary channel: auricular EMG. Three skin contacts: two signal contacts
  over the posterior/superior auricular muscles, one reference on the mastoid
  or another bony site. Jaw clench (masseter/temporalis) is the confirmation
  channel from the same region.
- Skin contacts are nickel-free: printed carbon-TPU or stainless steel.
- Everything touching skin runs on battery. Every electrode lead carries a
  series resistor and clamps. Measurement only.
- Staged: A = bench amplifier on a breadboard (parts listed in
  `docs/STAGE_A_PARTS.md`, not yet bought); B = the behind-ear pod
  (outsourced PCB, shell, dry contacts, battery, BLE MCU); C = a sealed canal
  tip with a MEMS barometer and a piezo mic; D = integration.
- Rolf owns no 3D printer. The design record lists three no-printer routes:
  outsourced conductive-TPU printing (Palmiga), off-the-shelf stainless
  contacts, and hand-shaping the shell in moldable PCL.

This brief replaces "shape it by hand" with: model the shell in CAD (Blender,
or a better tool if one exists for this job) and have a Chinese, or
comparable, manufacturing service make it from the file.

## Phase 0 (this session): research, then a plan

Research lanes, one `agy` worker each, reports in `docs/fab/`:

| lane | report | question |
|---|---|---|
| L1 cad | `docs/fab/L1-cad.md` | which CAD tool, how to capture Rolf's ear geometry, what starting models exist, what the manufacturers' design rules are |
| L2 vendors | `docs/fab/L2-vendors.md` | which Chinese and comparable services make a one-off skin-contact shell, in what materials, at what cost and lead time, shipped to Massachusetts |
| L3 contacts | `docs/fab/L3-contacts.md` | auricular anatomy for contact placement, and how nickel-free dry contacts get built into a manufactured shell |
| L4 pod | `docs/fab/L4-pod.md` | the Stage B electronics that must fit inside, their envelope, and one-off PCB fabrication and assembly |

Output of Phase 0: `docs/fab/plan.md`, a synthesis naming the tool, the
vendor, the route, the cost, the first order, and the decisions only Rolf
can make.

## Fixed facts for every lane

- Machine: MacBook Pro, Apple M5 Pro, 24 GB, macOS 27. Python via `uv`.
- Phone: iPhone, model unknown. Cover TrueDepth, LiDAR and plain-camera paths.
- Ships to: Massachusetts, USA.
- Budget: prototype scale. Flag any single line item over $200.
- No purchase, sign-up, quote request, or vendor contact by any agent.
  Purchases need Rolf's explicit approval (`docs/CLAUDE_SCIENCE_HANDOFF.md`).
- Rolf is not at the keyboard during this phase. Write for him to read later.
