# Fabrication plan: current scope

The former v2 delegation plan is superseded by the v4 board and snap-shell candidate. The board is unfinished and has not been ordered. This file keeps the engineering constraints, not private dialogue or cancelled checkout instructions.

## Constraints

- Design around a custom assembled board, a printed body/lid and qualified small parts.
- Minimize order count and validate the complete design before payment. No passive-gauge order sequence is active.
- Rolf selected a compact earpiece, titanium contact hardware and limited final mechanical assembly without soldering or crimping.
- Charge off-ear only. Do not present firmware inhibits or per-path resistors as isolation or certification.
- Keep raw recordings as source records in ignored `recordings/`.
- Keep anatomy parameters in ignored `measurements/`. Tracked CAD uses reference defaults only.

## Gates

Before fabrication, review actual routed copper, package identity, effective decoupling, charger protection, cell limits, assembly acceptance, RF keep-out and the programming path. Run release validation after changes. See [open questions](open-questions.md).

Before on-body evaluation, complete qualified electrical review, bench acquisition, passive printed fit, contact installation and repeated latch checks. No present file demonstrates that these gates passed.

The first end-to-end target is one real contraction, one decoded event and one harmless marker action with intent/result audit records. Do not attach consequential actions or an AI adapter before that evidence exists.

## Design references

- [Board v4 design](board-v4-design.md): circuit, placement, routing snapshot and limits.
- [Shell v4](shell-v4.md): selected snap and rejected closure rationale.
- [Firmware](firmware-v2.md), [binary frame](frame-v2.md), [receiver](receiver-v2.md): implementation contract and missing product variant.
- [Research and fabrication sources](references.md): source pointers retained from earlier engineering studies.

`plan.md`, `interface.md`, `packing-v2.md`, `board-v2.md` and v1/v2 CAD exports remain reference inputs for the current generator and existing checks. They do not define a current purchasing route. The historical cost worksheet is not a quote or an authorization to order.
