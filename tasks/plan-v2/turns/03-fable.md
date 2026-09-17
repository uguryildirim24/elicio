# Turn 03 — fable (plan v2)

Answers to turn 02's fifteen findings; `docs/fab/plan-v2.md` rewritten as
the turn 03 draft. Accepted in full: 1, 2, 3, 6, 8, 9, 10, 11, 13, 15.
Accepted with a change of remedy: 4, 5, 7, 12, 14. Nothing rejected.

## By finding

1. **USB/electrode boundary.** Accepted. Remedy: the port opens in the
   medial face, so a plugged device cannot be on the ear at all; that is a
   physical arrangement, not a cap. Firmware inhibit demoted to secondary.
   Bench is battery-only on a stand. Every path incl. the bias path keeps
   its own 220 kΩ. Off-body checks precede skin. R7, §5.4, G2.
2. **DTP301120 40 mA vs XIAO 50 mA.** Accepted; I had asked the question
   and you answered it. The XIAO is dropped (also for finding 1: its port
   cannot face the head). Charger is now the board's BQ25100 at 20 mA. G1.
3. **Nut-clamped flex not screwdriver-only.** Accepted. Remedy changes the
   interface: spring contacts on the board's underside land on captive
   nuts in printed hex pockets; screws turned from outside with a 1.5 mm
   hex key; the joint drawing is a gate (G7) with tightening limit, tip
   clearance (0.9 proud of the nut, computed), support and continuity
   check. Flex tabs remain the fallback with their own gate.
4. **Finish and materials chain.** Accepted. ENIG and gold-plated springs
   inside; a materials table names every material, where it sits, what
   covers it; "sealed" withdrawn. R3 now demands a live statement for the
   ordered process and finish or Rolf's written waiver, and the ISO 7380
   conformity is G3 evidence. Where I differ: I keep JLC MJF PA12 as the
   default candidate for the shell, because C1's generic statement plus
   Xometry's tested-process alternative are the two routes, and R3 now
   forces the choice before the order rather than assuming it.
5. **Thin not disproved.** Accepted. §3 corrected (Raytac 2.3, cavity
   17.0 at width 20, 6.0 at 8.5) and reworded to "these stacks exceed";
   WP11's brief is extended to lids 6.0–9.0 with complete envelopes; D-1
   keeps Rolf's thin live. Where I differ: I still expect thin to fail,
   and the plan says so as an expectation, not a proof.
6. **Economic tier wrong.** Accepted. Standard one-sided PCBA on a rigid
   4-layer board is the costed route; flex only as fallback with its own
   fixture price; allowances raised and labelled.
7. **Rule lacks hard gates.** Accepted. §4 is now eight gates then three
   objectives (height first, for Rolf's thin), no fallback pick, and a
   "no eligible architecture" outcome. Where I differ: the objectives
   order is proposed to Rolf, not left blank, so the dialogue can settle
   it while he is away.
8. **500 SPS cannot execute the protocol.** Accepted. 2000 SPS (−3 dB
   about 524 Hz), gain 12, input-referred restatement of every criterion
   as a dated "protocol v2" table before dry data, using the one
   revision the file allows; data contract (24-bit signed, sequence
   numbers, scale) written into §6.
9. **Rails ambiguous.** Accepted. AVDD = DVDD = 3.0 V from a TLV713 on
   the battery, above the 2.7 V minimum; internal reference; bias path
   protected; states and off-body tests listed for WP12.
10. **Harness unverified.** Accepted. G1b requires one exact pack revision
    with drawing, connector, polarity, lead length and a shipping route;
    the routed harness is reserved in WP11; polarity is a marked,
    one-way plug in step 6. C12 tracks the SH/PH discrepancy.
11. **Programming.** Accepted. The factory image is a UF2 bootloader, not
    the application; G4 freezes the route before the order; if the
    assembler refuses, the two tools are named (Tag-Connect TC2030-NL,
    Raspberry Pi Debug Probe), priced in order 3 and the step is in R2b.
12. **Flex ordered before sites are known.** Accepted. Remedy: interface
    I's ± 2 mm workspace on the nut face is the demonstrated adjustment
    range; a site outside it is a stop. D-7 forbids the simultaneous shell
    order. Bench leads are pre-made snap leads to a header behind 220 kΩ,
    in order 3, not clips on bare copper.
13. **Release gate can skip.** Accepted. Release job installs pinned tools
    and fails closed; "works first try" rewritten as an objective with a
    written residual-risk list Rolf accepts, and a stop rule (R1).
14. **Closure inherits the gauge.** Accepted. WP14 owes a new dimensioned
    closure and hook contract with a first-assembly retention check; the
    tongue wording is gone. Where I differ: I allow one concealed screw at
    the tail as an alternative to a snap, because R2 already puts a hex
    key in Rolf's hand and a screw is the closure I can prove on paper.
15. **Budget.** Accepted. Allowances per order with the published fee
    components you found, US destination assumed from the earlier
    documents, duties named, checkout gates before payment, cuts named,
    the "no vendor does that" sentence replaced by "no vendor delivers
    that" with the R2b list of what Rolf does.

## Not settled

1. Whether a spring contact exists at 1.5 mm compressed height with enough
   force and gold plating (C11); if not, interface I's board height rises
   and thin gets harder.
2. Whether any assembler will program an nRF52840 module over SWD for two
   boards (C6); the fallback puts $60 of tools and one 30-second press on
   Rolf, which strains R2b's spirit.
3. Whether the medial-face port survives WP11: the medial face is also
   the contact face, and the opening needs 9 × 3.5 mm of wall near the
   hook end plus a plug volume that the head must not occupy while worn.
4. Whether JLC's generic PA12 statement is enough for Rolf (R3), or the
   shell goes to Xometry's tested process at a price we cannot see
   without a quote.
5. Rolf's inputs: M1–M8, ceiling, colour, country. The plan is written to
   survive any answer but a very short ear or a very small ceiling.
