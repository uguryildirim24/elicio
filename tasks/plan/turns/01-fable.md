# Turn 01 — fable

First draft of `docs/fab/plan.md`, all ten sections, 5,846 words. Read in the
order the brief gave: protocol, fabrication brief, design record, the
"Safety and authority" section of the handoff, then L1–L4. No web search was
used: Rolf's standing rule routes every search through an Antigravity lane,
and the protocol gives `pro` the verification job, so every number that a
lane gave without a page is marked UNVERIFIED and listed in plan section 8.

## Decisions and why

1. **build123d, not Blender.** L1's case is sound: headless, deterministic,
   native STEP, exact booleans for pockets and snaps. Blender stays as the
   fallback for a scan mesh that does not exist yet.
2. **No scan, no impression for order 1.** L1 §4.3 (generic BTE fit) plus
   the fact that a passive fit gauge is cheap ($33) and answers the same
   question a scan would, on Rolf's actual ear. The $12–15 putty impression is
   deferred to Stage C where a canal tip needs it anyway.
3. **Eight measurements, all optional.** L1's M1–M7 plus M8 (helix rise),
   which L1 lacked but the hook radius needs. Defaults print a valid shell if
   Rolf measures nothing.
4. **JLC3DP, MJF PA12, dyed black, DDP.** L2's cheapest and fastest option
   with the safest uncertified polymer. Domestic alternatives (Xometry $34
   all-in) match for one part but not for iterations. DDP because L2's tariff
   section says non-DDP parcels add $25–35 in courier fees.
5. **PA12 for the fit-check too, not resin.** The fit check is four hours on
   skin; L2 flags acrylate irritation from resin; and printing the gauge in
   the Stage B material makes the snap lid and feel tests real.
6. **Contacts: three Grade 2 titanium M3 button heads.** Titanium because the
   design record says nickel-free and 316L is 10–14 % nickel; L3's concrete
   part (McMaster 93625A110) is exactly this screw. 316 is the fallback.
7. **Contact size 5.7 mm, not L3's 7–9 mm.** L3's own force budget
   (0.3–0.4 N per contact) over a 7 mm dome gives 8–10 kPa, below L3's own
   10–25 kPa window; over 5.7 mm it gives 12–16 kPa. M3 hardware also intrudes
   less into the cavity than M4. L3's "15–20 kPa across a 7 mm dome" is a 2×
   arithmetic slip, flagged in plan section 2 row 4.
8. **Suspension: foam washer plus floating nut, plus 1.5 mm hook preload.**
   L3's mechanism, L4's preload. The intrusion this costs (3.6 mm under the
   signal contacts) is what makes the body 9.2 mm thick rather than a
   hearing aid's 6.6. I kept it because L3's argument about jaw motion
   breaking rigid contacts is the failure mode Stage B's exit criterion
   (three days, same threshold) will hit first.
9. **Envelope derived from parts, not from a lane.** 501015 cell in a
   16.8 × 10.6 × 5.4 pocket at the top; an 18 × 12.5 × 3.3 board zone at the
   bottom sitting on 3.6 mm pads above the two contact pockets; 1.2 medial
   wall, 1.0 lid. Outer 38 × 15 × 9.2 plus a 10 mm tail and the hook. Two
   variants are printed so Rolf feels the difference between the guaranteed
   thickness and a hearing-aid-class 7.6.
10. **Reference contact on a tail.** The body cannot hold three contacts and
    a 15 mm battery in tandem: the battery cannot sit over a contact pocket
    (5.0 in a 5.4 space), and three contacts along 38 mm leave no 17 mm
    stretch free. A 10 mm solid tail carrying the reference over the mastoid
    surface solves it, at 48 mm total length. Total length needs M1 ≥ 51;
    plan open item 8 says what to do if Rolf's ear is smaller.
11. **Contact pair at 30° from the body axis, 12 mm pitch.** L3 wants the
    pair along the PAM fibres (oblique, mastoid to concha). A 15 mm wide
    medial face allows 6 mm of posterior offset; 12 mm pitch at 30° uses
    it. The positions are parameters and the Stage A bench with gel
    electrodes picks the final ones before order 2 (WP6).
12. **Three contacts, not five.** Design record and L3 agree; the clench
    signal is 3–5× larger on the same pair, so one channel plus reference is
    enough. L4's spare ADS1292 channel is a board matter.
13. **Snap lid, tabs only in the battery zone.** Boards are 12.5 wide and
    would collide with tabs along the board zone; the battery (10.6) leaves
    room. Tongue at the tail end. L1's strain numbers reused as given.
14. **One-piece PA12 hook.** A cantilever estimate (Ø3.5, 40 mm, E ≈ 1.7 GPa)
    gives about 0.9 N at 1.5 mm deflection and 0.5 % strain, inside L3's
    0.8–1.2 N. WP3 measures it on the printed part.
15. **Outputs committed under `docs/fab/cad/v1/`** so Rolf can download STLs
    to his phone and upload from there.
16. **Orders.** Order 1: three bodies (full/1.5, thin/1.5, full/2.5) and two
    lids, about $33 standard DDP. Order 2 after the fit check, the montage
    test, and the board designer's envelope sign-off: about $105 including
    hardware and a nickel test kit. Every price is a lane range with its page
    and date, or UNVERIFIED.
17. **Work packages** ordered so WP1 and WP2 produce the order 1 files
    first; WP6 (montage) is blocked on Stage A parts, which Rolf has not
    bought.

## Conflicts and picks

All sixteen are in plan section 2 with reasons. The ones the protocol named:
battery 50 mAh (row 1); envelope 38 × 15 × 9.2 derived from parts, L4's
33 × 10.5 × 6.8 shown not to contain its own parts (row 2); titanium over
316L over gold-plated (row 3); conductive TPU dropped (row 5); snap lid over
screws (row 6); nylon over resin for the fit check (row 7). Added: contact
diameter (row 4), montage geometry (row 8), contact count (row 9),
suspension (row 10), capture method (row 11), shipping (row 12), parcel
consolidation (row 13), hook material (row 14), gasket (row 15), charging
port (row 16).

Lane numbers I called wrong: L4's rigid-flex islands (16 × 9.5) cannot carry
the module it names (15.5 × 10.5); L4's envelope cannot hold a 17 mm battery
pocket plus 16 mm of boards in 33 mm; L1's battery "401020, 22 × 10 × 4.2" is
not that cell's size (4 × 10 × 20); L3's dome-pressure arithmetic (above).

## Not settled

1. Whether HP's PA12 biocompatibility statement (USP Class VI, intact skin)
   applies to JLC's PA12-HP and to the black dye. My recollection, no page;
   plan claims 6 and 7. If false, order 1 goes natural grey and the four-hour
   wear test is the only evidence.
2. The real intrusion of the M3 nut, lug, and screw tip stack; 3.6 mm is
   arithmetic. WP4 measures it; every 0.5 mm over adds 0.5 mm to the body.
3. Every JLC price, the 40 % tariff rate, and the de minimis status. Lane
   ranges only. `pro` verifies or the JLC checkout page does.
4. McMaster part numbers, prices, and whether certificates come with them;
   the thin nut, ring lug, and foam sources have no part numbers yet.
5. Whether the pair position on the body (30°, 12 mm, 4.5–6 mm posterior of
   the crease edge) actually sees the posterior auricular muscle. Only the
   Stage A bench answers that, and Stage A parts are unbought.
6. Rolf's ear size: if M1 < 51 the 48 mm total length is too long and the
   tail shortens.
7. Whether 9.2 mm is acceptable to Rolf at all. The thin gauge exists to make
   that a felt comparison, not a guess.
