# Turn 01 — fable (plan v2)

First draft of `docs/fab/plan-v2.md`, a delta over the signed-off plan v1,
written from Rolf's answer sheet of 2026-09-17 (open questions Q28 to Q36),
the merged code of rounds 1 to 4, and the WP10 research on `lane/w5`
(`832ef28`, unreviewed). No web search by me: the research lane searched;
Pro verifies.

## Decisions and why

1. **One order per thing, and the gauge is gone.** Rolf cannot pay for
   versions. The provisional gauge existed to de-risk the shell; v2 buys
   that risk down with his measurements, a paper template and the check
   suite that four rounds built. The board is ordered first because the
   bench on it gives the contact sites the shell needs.
2. **Thin is refused with arithmetic, not opinion.** §3 sums every
   module and cell on file; nothing gets under a 4.5 mm cavity. Saying so
   now costs one sentence; finding out after the one order costs the
   order.
3. **Custom board, but with the radio inside a module.** "Works first
   try" and "designed by agents" only coexist if RF, crystals and USB are
   somebody else's tested work. Three candidates, one rule, WP11's
   measured layouts decide.
4. **Flex tabs under the nuts.** The only way "no soldering" and "three
   contacts through a wall" meet. It also deletes the lug, the 28 AWG
   problem (Q23) and the wire crossing (Q20).
5. **Charging is the one safety knot.** v1 hid the port under the lid;
   the XIAO makes that hard. D-5 offers a covered external port with a
   firmware interlock for C and the v1 arrangement for A/B, and asks Pro
   to attack it.
6. **Budget is stated as a range with cuts named**, because Rolf gave no
   ceiling yet and the estimate must survive his number when it comes.

## Not settled

1. Whether the DTP301120 tolerates 50 mA charge (C3). If not, the XIAO
   route needs the 501015 and the height argument shifts.
2. Whether any assembler programs an nRF52840 as a service (C6). If not,
   A and B cost Rolf an SWD session with a clip, which strains R2.
3. Whether JLCPCB assembles a flex this small with stiffeners (C7). If
   not, D-3's fallback (rigid board plus flex jumpers) needs its own price.
4. JLC's skin-contact statement for MJF PA12 was quoted by an agy lane
   whose earlier citations failed verification (rounds 2 and 3). C1 is the
   first thing to check.
5. The port and interlock (D-5). I am not sure a covered USB-C with a
   firmware interlock is acceptable for a device with skin electrodes.
6. Rolf's country, ceiling, look and M1 are still blank; the plan is
   written to survive any answer except a very short ear.
