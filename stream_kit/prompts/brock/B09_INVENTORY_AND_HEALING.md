# B09 — Inventory, item use and verified healing services

Recommended coding model: **GPT-6.1 Sol · Extra High · Standard speed**.
Inventory freshness, consumable reconciliation and emergency handoffs need careful checks.
See [model guidance](MODEL_GUIDANCE.md).

Status: inventory/healing implementation prompt; a health blocker is not a healing tool.
Dependencies: B00–B08. Cross-map named travel arrives in B15, not this checkpoint.
Playable order: R7, after the optional first-battle learning demonstration. B10a/B11
are not prerequisites; local inventory/healing can be implemented earlier if needed.
Use a known grounded local service endpoint for this gate; remote access may block.
LAB extends the canonical shared DB; STREAM starts with these final typed tools.

## Copy-ready implementation prompt

Implement native bag inspection, bounded item actions and a reusable healing
service. Extend existing registry, menu/NPC tools and memory without replacing
historical team/battle/goals. No inventory assumptions from roadmap knowledge.

Define InventorySnapshot with ID/context/session, capture refs, pocket coverage,
item ID/observed label, quantity or presence semantics, uncertainty and timestamps.
Key items may have presence rather than quantity. Unknown/unreadable pockets are
not empty. Store supplementary versioned inventory tables in the canonical DB;
preserve snapshots, actions and receipts. Transactions/migrations must be additive.

Expose `player.bag.inspect(pockets, required_items)`,
`player.item.use(item_ref, target_member_ref, context_kind)`, and
`player.service.heal(entity_ref, requirements)` via B06 ToolSpec schemas.
Item execution admits only known supported item/context/target combinations;
throwing balls belongs to B12, and battle item turns to B10's battle ownership.
Dropping/tossing/selling items is outside this checkpoint and absent from registry.

Navigate visible pockets and list entries by sensed labels/highlights/page state.
Check item availability before A, confirm the intended target and observe the
native effect afterward. Persist input/receipt reconciliation so restart cannot
repeat a possibly consumed potion without inspecting inventory and current team.
Do not assume a single press consumed an item or that quantities cannot change.

Use Receipt{action_id,context,session,item,target,before_refs,after_refs,effect,
consumption,outcome,uncertainty}. Separate actual consumption, no-effect/rejected
use, ambiguous UI and verified recovery. A missing quantity decrement is not
automatically failure for nonconsumable items; apply the item profile's semantics.
Restore HP/status evidence from fresh native reads, not animation or dialogue.

Register item_received and item_delivered with item identity, fresh before/after
inventory plus recognized native receipt when available and same-session context.
A pre-existing parcel does not satisfy a newly requested receipt event. Delivery
requires an observed handoff/outcome, not disappearance through an unknown menu.
Schema presence alone cannot prove native item correctness.

HealingService accepts a grounded entity/service reference and requirements such
as minimum safe HP, remove poison or full restoration. B08 owns dialogue/choices;
B07 owns fresh complete-party inspection. Require service-specific native evidence
and a fresh team meeting the requested condition before recording that service.
Healing by a home NPC and a Center are separate service identities with common
effects; do not claim Center use just because HP becomes full.

Implement code-owned health interruption using fresh HP/status, remaining usable
party, observed resource supply and measured route/risk estimates. Unknown team
state requests inspection. Poison in the overworld, fainting and blackout demand
supported UI handling/recovery or a clear blocked capability, never aimless travel.
Thresholds are configuration, logged with the decision, not LLM emergency authority.

Choose among only available service/item options. Route cost may be unknown;
do not declare a remote Center reachable from its name. Until B15, local known
geometry can reach an endpoint, while missing travel capability remains blocked.
Suspend the parent, preserve its target and resume only after fresh recovery.
Clear only the exact automatically generated health blocker whose condition is
verified; never remove manual blockers or treat partial healing as full restoration.

Keep planned resources distinct from observed inventory. Record expected versus
actual cost/effect for future learning, without claiming this deterministic chooser
already learns. Integrate with B05 frozen evaluation and immutable policy/memory
snapshots; current episode observations belong in its isolated overlay.

LAB retains inventoried health-decision/emergency APIs through adapters and
replaces their missing-tool blocker only when capabilities pass gates. STREAM does
not build the earlier permanent healing dead end. Expose bag/service coverage in
the operator panel and publish concise action/effect/emergency rows to the feed.
Frames remain in RAM with bounded diagnostic references, no item-frame archive.

## Verification and gate

Test pockets/pagination, unreadable counts, key-item presence, unsupported items,
wrong/full-HP target, status cure, insufficient quantity and consumed-but-unrecorded
restart. Test old parcel versus fresh receipt, rejected use and ambiguous effect.
Test low HP/poison interruption, missing route/service, manual blockers, partial
healing and verified full-party recovery. Infrastructure failure never heals.
Run visible stream_checks; label mocks/recorded observations accurately.
Gate: native fixtures complete bag-read/use/effect and known-local-service/team
refresh with receipts, and resume the suspended parent only when its blocker clears.
Any live item/service test is separately bounded and explicitly requested.
Cue: “Recovery is a verified change in health and resources, not hopeful dialogue.”
Update capabilities and storage documentation; stop after this gate.
