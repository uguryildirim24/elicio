# Turn 03 — fable

Answers `tasks/plan/turns/02-pro.md` (commit fbe51ee, 15 findings, NOT
SIGNED OFF). All fifteen accepted; none rejected, none carried. `plan.md`
was rebuilt rather than patched. No web search by me; every page `pro`
checked is now cited as verified by `pro` with its date, and everything
else stays UNVERIFIED.

## Findings

1. Accepted. §3.2 defines a shell frame and a body frame with the preload as
   the rotation between them; the medial face is a plane in the body frame
   and every contact axis is −Y there; `P(u, s, y)` maps path coordinates;
   BODY_CHORD is a chord and arc length is derived; the cavity is swept along
   the path; the hook has a root coordinate and starts inside the body; the
   lid takes the body transform; left side is a mirror across X = 0 with
   the axis meaning stated. Checks in §3.3 cover connected solids, walls,
   lid intersection at −0.3, keep-outs, and contact axes.
2. Accepted. §3.3 publishes reference-ear values for M1–M8, null handling
   (default plus a REF mark), design checks versus ear checks, the supported
   domain (REF_SITE tail for M1 ≥ 52, hook tip below, fail under 41), and the
   assembled span 10.35 mm against M3. The battery-pocket shrink is gone;
   the domain is widened by moving the reference, not by assumption. §3.7
   calls the gauge provisional; claim 15 is dropped.
3. Accepted. The sign was wrong; contact 2 is now contact 1 + pitch ×
   (sin, +cos). Positions were re-derived from the full keep-out (Ø7.1)
   against rib, walls, and end wall: u 5.9/10.4, s 22.0/33.1 at 22°. Only
   that pair angle fits a 14 mm cavity; the body grew to 17 wide. The
   keep-out check in §3.3 tests all three stacks against everything.
4. Accepted. The floating stack is dropped (§2 row 10). Rigid mount: M2.5 × 4
   screw, lug, thin nut, 2.5 mm stack, board pads at 2.8 above the floor.
   The lug is clamped positively. Wire and terminal now match (28 AWG,
   26–28 AWG barrel). "Cut pocket" versus free volume is separated: body
   contacts get a through-hole and a keep-out; only the tail gets a cut
   pocket. Per-contact suspension returns only if the active gate in WP7
   shows dropout.
5. Accepted. Closure redesigned with nothing inside the cavity: external lip
   at the top (t 1.0, L 5.0, y 0.4, 2.4 % strain), tongue at the tail tip,
   two nubs at the rib; nylon screw named as fallback. Walls 1.5 per JLC's
   pages (±0.3, 1 mm wall, > 1.5 for snap features, 0.8 emboss, 0.2–0.4
   clearance), which replace L1's numbers in §3.6. Thin cavity depth stated
   directly (y 1.5–6.0). Worst case −0.2 interference is stated and a coupon
   is added to order 1. One lid fits all three bodies because no feature
   depends on cavity depth beyond 0.8 mm.
6. Accepted. §5 now carries a packing budget at maximum dimensions (Raytac
   15.8 × 10.8 × 2.3, ADS1292 7 × 7 lead span, clamps, charger, passives):
   about 105 mm² available on the medial side against about 111 required.
   The plan says so and names the three escalation options and who decides.
   9.0 mm is labelled a design value pending WP6. Board clearances and
   retention are explicit.
7. Accepted. §4 labels force and pressure exploratory. WP7 now holds the
   montage test, a bench force/travel/continuity characterization of the
   real stack, and the active-contact gate: baseline, SNR, dropout under jaw
   motion, and the design record's three-day re-donning at a fixed
   threshold. WP8's acceptance includes passing that gate before Stage B
   wear. Impedance measurement is battery-powered only (§6).
8. Accepted. Stainless removed everywhere; titanium by grade with supplier
   material evidence; "0 %" replaced by the supplier's specification; DMG
   demoted to a reject screen with the Thyssen limitation cited; all other
   metal is under the lid or potted; Open for Rolf no longer offers 316.
9. Accepted. HP statement cited with its scope as verified by `pro`; natural
   grey default; superlatives removed; wear progression 15 min, 1 h, 4 h
   with removal on any reaction; observations are observations.
10. Accepted. Charge window removed; charging is off-ear with the lid off,
    stated as procedural; the debug hole is a lead exit, not a safety claim;
    Kapton discs, solder-mask rule, and per-contact protected paths
    reserved; active wear gated on schematic review and a battery-powered
    leakage check.
11. Accepted. 93625A110 struck and named as an M8 locknut. Contacts are
    specified by standard and grade; WP5 verifies SKUs with live pages
    before purchase. Hardware moved to M2.5 (turn 02 did not object to M3;
    M2.5 saves 2.4 mm of length, M3 stays a parameter switch).
12. Accepted. §2 row 5 corrected: Palmiga offers conductive TPU printing;
    titanium remains primary for assembly, area, and supplier reasons; TPU
    is a conditional alternative needing Rolf's authorization for contact.
13. Accepted. §7 shows dated planning allowances by line, with hardware
    shipping and Massachusetts tax lines, the correct tariff FAQ URL, DDP
    policy marked verified by `pro`, the 40 % rate unverified, Nickel Alert
    at $24.99 and unavailable, and a checkout gate for Rolf with stop
    thresholds.
14. Accepted. §9 reordered: WP1 is a versioned mechanical interface written
    before any production-intent geometry; WP6 confirms or bumps it; a
    change re-runs the CAD checks and any fit check whose inputs changed.
    Order 1 is explicitly provisional with its rework cost. Open items now
    hold only single-package items; cross-package questions are listed
    under interface decisions.
15. Accepted. §3.6 has a file-to-quantity manifest: five files, six parts.

## Changes to plan.md

Rebuilt. Frame and construction rewritten (§3.2, 3.5); parameters re-derived
(§3.3) with a new width of 17 mm, thickness 9.0/7.0, chord 48.4, M2.5
hardware, a 22° pair, a hook-tip reference variant, and a coupon; JLC print
rules from the live pages (§3.6); passive acceptance split from the active
gate (§3.7, WP7); contacts rewritten around specification-based sourcing
with the wrong SKU struck (§4); packing budget added (§5); safety section
rewritten as enforceable constraints plus stated procedural rules (§6);
orders as allowances with a checkout gate (§7); claims table updated with
`pro`'s verifications (§8); work packages reordered around the interface
(§9); open items reduced to single-package items and Rolf's list revised
(§10). Word count stays under 6,000.

## Still unsettled

Whether Rolf's M1 is 52 or more; whether the medial side packs (WP6); the
titanium SKU and its material evidence (WP5); the 40 % collection rate and
shipping ranges (JLC checkout); the lip snap under ±0.3 (coupon).
