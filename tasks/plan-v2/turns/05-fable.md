# Turn 05 — fable (plan v2)

Answers to turn 04 (findings 16–22 and the conditions on 1–15).
`docs/fab/plan-v2.md` rewritten as the turn 05 draft. Accepted: all
seven. Two change the design again; the rest change the contract.

## By finding

16. **Medial port is not an interlock.** Accepted, and I withdraw the
    word. There is no galvanic isolation between electrodes and USB in a
    single-battery wearable, and I stop pretending geometry supplies
    one. R7 is now a proposed change for Rolf: battery-only acquisition
    (worn and bench, with the port capped and no cable on the stand),
    the medial opening as an ergonomic exclusion, 220 kΩ on every path
    bounding device-sourced current to 23 µA at 5 V, charging only from
    a power bank or a listed Class II adapter, and a hardware P-channel
    supply gate on VBUS instead of a firmware promise. The residual
    hazard (a certified adapter's touch current through a small skin
    area when every rule is broken at once) is named in §10 for his
    acceptance. The opening's local wall, recess, ligaments, plug
    material and lost-plug state are specified (§5.4) with an end-face
    fallback that weakens R7 (ii) and says so.
17. **The nut cannot give ±2 mm.** Accepted; your annulus arithmetic is
    right and the tip over-compression is real. Two changes: the nut
    becomes a 3.0 mm brass female standoff, so the landing is a flat
    brass face with the titanium tip 0.5 below it, and the board carries
    a small array of spring-loaded pins per site on one net (≥ 1.0 mm
    travel, positive stop), so at least one pin lands fully on the face
    anywhere inside the array; the adjustment region is computed from
    the array, about ± 1.5 mm for a 3 × 3 at 2.0, stated per site by G5.
    The datum chain, the ± 0.3 floor, the reaction load and the off-body
    continuity and motion test are G7 content. The Harwin part you found
    stays a candidate; its 0.5 travel is probably too little, which is
    why C11 now asks for ≥ 1.0. The example height budget you computed
    is why the module and cell are kept off the contact zone (§3).
18. **Charger TS and termination.** Accepted. TS is never floated; the
    pack has no thermistor, so the fixed network keeps termination and
    timers and the temperature window is enforced by Rolf's sheet and
    recorded as such; the 1 mA termination floor and its capacity cost
    are recorded; the LED's meaning comes from the circuit's actual
    pins. ISET about 6.8 kΩ for 20 mA stands as the setpoint.
19. **Undervoltage.** Accepted. Firmware inhibits acquisition and marks
    samples invalid above a WP12-computed battery threshold with
    hysteresis and shuts the front end down before dropout; the PCM's
    2.4 V is cell protection only.
20. **Protocol v2 semantics.** Accepted. The frame now has a version, an
    acquisition counter, the ADS status word and N samples with MTU
    fragmentation handled by the receiver; acquisition and transport
    loss are separate; dropout keeps the original rail-or-flat-> 100 ms
    rule; the offset criterion is ± 50 mV input-referred on the
    DC-preserving path; filters and windows are named per line; each
    line says "same" or "revised: why".
21. **First-load kit.** Accepted. G4 demands either an accepted factory
    job with a price or the exact kit with its pin map and target-power
    arrangement rehearsed on paper by WP15, measured time recorded; the
    factory image is the Adafruit bootloader plus SoftDevice built for
    this board with the application layout frozen by WP13; recovery is a
    tactile switch under the lid using the bootloader's own double-press,
    listed in R2b.
22. **Budget basis and ledger.** Accepted. Two-sided standard assembly is
    the working assumption with the correct fee components and the
    economic $3.07 removed; a whole-project ledger with import
    collection (higher of JLC's two stated figures until a checkout
    shows the real one), Massachusetts use tax and per-parcel shipping
    goes to Rolf before the first payment, with the shell's maximum
    reserved; the turnkey sentence is replaced with yours.

Conditions on 1–15 carried in: R3's acceptance wording (4), sides per
placement (6), step 6's polarity check (10), the closure check labelled
qualitative with a drop test (14).

## Not settled

1. Whether a spring-loaded SMD pin with ≥ 1.0 mm travel and a positive
   stop exists at a working height that keeps interface I under a 9.0
   body (C11); if only the 0.5-travel class exists, G7's datum chain
   must be tightened or interface II wins.
2. Whether the medial opening survives WP11 and WP14 with its ligaments
   and recess; the end-face fallback is weaker and I would rather not
   use it.
3. Whether Rolf accepts R7 as rewritten; it is the honest version, and
   it puts two rules on him (no cable while worn or on the bench, and
   the power source).
4. The whole-project envelope of about $350–560 against a ceiling he
   has not given.
5. His measurements, colour and country.
