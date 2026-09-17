# Turn 08 — pro

Reviewed: `docs/fab/plan.md` **as committed at `cbcb265`**, retrieved with `git show cbcb265:docs/fab/plan.md`. Review and public-page verification date: 2026-09-16. The working-tree plan was not substituted for the requested blob.

Read for this turn: the pinned plan, `tasks/plan/turns/07-fable.md`, `tasks/plan/protocol.md`, and the complete `tasks/plan/turns/06-pro.md`. The fabrication brief, design record, L1–L4, and earlier reviews remain supporting context from the preceding turns. This is a specification review with numerical coordinate checks, not a CAD build, manufactured-part inspection, or electrical/wear-test result.

Fable accepted both preceding findings and applied the chord-gate note; none was rejected. No rejected finding is being re-argued. The per-interface fit policy resolves the previous blanket-clearance objection. The enlarged reference channel has a genuine opening into the pocket; the upright reference-terminal arrangement, actual wire sweep, and pad positions are explicitly subject to the accepted interface-v2 gate. The computed chord check, rather than a universal 51 mm cutoff, governs the measurement sheet. Those corrections are accepted; resolved findings are not repeated below.

There is **one minor finding, numbered 23; no blockers or majors remain**. Under the protocol, the minor does not require another review round. Sign-off is for the stated provisional-gauge-first Phase 1 workflow, with the existing sourcing, packaging, fabrication and validation gates intact—not a claim that an active device has already been proved to fit or be safe.

Public-source recheck: [JLC's PA12-HP page](https://jlc3dp.com/help/article/pa12-hp-nylon), updated July 30, 2026, continues to list ±0.3 mm below 100 mm and a 1 mm wall. Its [design guideline](https://jlc3dp.com/help/article/3d-printing-design-guideline), updated August 24, 2026, recommends more than 1.5 mm for protrusions, positioning features, snaps and fasteners, and lists 0.2–0.4 mm assembly clearance for nylon. These remain general supplier guidance, not approval of this particular closure. The plan's experimental exceptions, inspection, rejection and passive tape fallback remain necessary.

## Findings

### 23. The channel now connects, but its quoted overlap still uses unwrapped coordinates

**Severity:** minor. **Plan:** §3.3 `WIRE_CHANNEL`, §5 reference route. **Relationship:** residual numerical annotation from finding 21, not a recurrence of its disconnected-channel blocker. **Disposition:** correct in the author's final pass, or carry to WP2's geometry-report work; no interface dimension change is requested by this finding.

**What is wrong.** The revised channel extends to `s = 40.5`, which remedies the previous disconnection. However, the description still says the pocket edge is at `s = 39.34` and that overlap is at least 1.1 mm across the channel width. Those figures treat the `(u, s)` coordinates as an unwrapped Cartesian plane. The pocket is a physical Ø7.5 mm circle placed through `P`, and an offset path does not have the same length scale as the base arc.

For a fixed `u`, the physical distance `d` to the pocket centre at `P(8.5, 43)` satisfies:

`d² = (R + u)² + (R + 8.5)² − 2(R + u)(R + 8.5) cos((43 − s)/R)`.

Solving `d = 3.75` gives the first circle intersection along that offset path. At the posterior channel edge, `u = 9.3`, the numerical results are:

| CREASE_BOW | Circle-entry s at u = 9.3 | Channel end minus entry, in s | Corresponding physical distance along the offset path |
|---|---:|---:|---:|
| 1.0 mm | 39.4444 mm | 1.0556 mm | 1.0891 mm |
| 3.0 mm, default | 39.6437 mm | 0.8563 mm | 0.9383 mm |
| 8.0 mm | 40.0750 mm | 0.4250 mm | 0.5373 mm |

These are evaluations at the stated channel edge and three permitted bow values, not a fabricated-part measurement or a complete CAD sweep test. At defaults, `C = 47.9005234 mm` and `R = 97.1025059 mm`; the physical offset-path distance is `(1 + u/R) × (40.5 − s_entry)`.

**Why this is minor.** Unlike the previous revision, the nominal cuts overlap by a finite amount. At defaults, both edges of the channel's terminal cross-section at `s = 40.5` are inside the pocket: their distances from its centre are approximately 2.8241 and 2.8439 mm, below the 3.75 mm radius. The remaining error is the claimed overlap magnitude, not an instruction to force the terminal through a disconnected or undersized passage. The plan now separately requires body-frame containment of the actual terminal and swept insulated wire, and acceptance of the final route at interface v2 before order 2. Those checks—not the unsupported 1.1 mm annotation—must govern release.

**Evidence.** The pinned plan's §§3.2–3.3 supply the arc, circle and channel geometry. `07-fable.md`, lines 12–15, repeats the 1.1 mm and 39.34 mm figures; lines 19–23 specify physical-frame checks and the coordinated interface-v2 route. The calculations above use those exact dimensions. No new vendor or material assumption is involved.

**Concrete fix and closure check.** Replace the unwrapped edge/overlap figures with a report derived from the actual body-frame geometry, explicitly naming the distance being reported. Keep the present channel dimensions unless the required containment and wall checks demand a revision. WP2's geometry-report implementation should record the computed intersection and positive opening for the supported geometry; the existing Stage B checks must still establish the continuous Ø1.3 mm wire envelope, 3 mm bend allowance, terminal containment and preserved walls. If those checks require changed geometry, use the existing interface-version and revalidation rules rather than treating this review as permission to bypass them. Correcting this annotation alone does not change another work package's dimensional contract.

## For Rolf

The plan is signed off for its stated Phase 1 sequence. Fable can make the final pass and record the minor correction above without another adversarial round. The next work is the versioned interface and checked gauge files, followed by your render approval and the existing order-1 checkout gate. Your ear-length decision should use the script's computed chord gate, not a rounded 51 mm promise.

The first order remains a passive experiment. An experimental snap that fails may use the recorded tape fallback for the remaining passive observations; that result does not qualify the closure for an active pod. The titanium SKU, complete terminal assembly, cell, packing and final lead route still need their existing WP5/WP6 and S1 approvals. In particular, the upright reference tab and its wire transition must be checked as installed geometry, not inferred from the screw/nut stack height alone. Controlled validation wear remains S3, after the S2 checks; routine use remains S4, after the frozen protocol passes.

No purchase, supplier contact, quote request or design upload was made. No new titanium SKU, shipping quote or tariff rate was authenticated. Only this review file was written; no plan, code, brief, lane report or previous turn was changed.

SIGNED OFF
