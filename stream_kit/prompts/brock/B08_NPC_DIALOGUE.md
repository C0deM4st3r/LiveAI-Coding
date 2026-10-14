# B08 — General NPC interaction and conversation knowledge

Recommended coding model: **GPT-6.1 Sol · High · Standard speed**.
Use Extra High for a diagnosed identity or UI-ownership problem; retain the same gate.
See [model guidance](MODEL_GUIDANCE.md).

Status: NPC implementation prompt; named identity requires its own verified evidence.
Dependencies: B00–B06 plus B07a/b. Playable order: R3.
Hosted semantics remain optional until B13; no inventory/battle dependency.
LAB reuse, if present: NPC/native text tools and canonical entity/knowledge memory.
STREAM builds one reusable interaction tool, not one player class per NPC.
Non-NPC world-object/choice interaction belongs to B07b's shared interactable tool;
reuse its UI primitives without inventing an NPC identity for a starter object.

## Copy-ready implementation prompt

Implement an identity-scoped, resumable NPC interaction over the prior native tools.
Preserve any reviewed identity evidence without extending it to matching sprites
elsewhere. Keep shared spatial entities and canonical knowledge storage; do not
introduce a parallel NPC map, vector service or game-state oracle.

Register `player.npc.interact` with target entity/place references, intent from a
bounded enum, optional typed choice policy, required closure and requested fact
fields. Inputs are game data, never executable instructions. Require a current
localized chart, grounded candidate entity and available approach/interaction UI.
`observe_entity`, `approach`, `face`, `open`, `read`, `choose`, `close`, `release`
are internal phases with persisted session and observation references.

NpcIdentity carries entity_id, chart/grounded place, role/name claims, support
observations, review/native status and last_seen. A sprite match is class evidence;
name text is scoped dialogue evidence. Neither alone identifies every repeated
sprite or proves a particular service. Moving entities update fresh positions,
not permanent wall tiles. Lost/occluded NPCs require re-observation, not A-spam.

Approach through B04 A* to a currently free adjacent measured tile; face using
native cues and bounded input. Stop before collision/portal/NPC thresholds.
Opening evidence must be causally linked to this interaction session and source
entity. A previously open textbox or unrelated event is not interaction success.
Direction or A inputs during script motion remain forbidden under B07 ownership.

DialogueSession stores context, goal, entity candidate/identity, fresh opening,
deduplicated page text with capture provenance, choices/options, dispatch receipts,
closure and control-release evidence. Wait for text to settle before advancing.
Normalize repeated pages for storage while retaining ordering and evidence refs;
do not erase different conversations merely because their first page matches.

Recognized choices expose typed option IDs and observed labels. Service-specific
tools may choose registered options; generic dialogue cannot invent a purchase,
healing, irreversible release or item-use decision. Unknown choices hold with a
missing-capability reason. Explicit bounded skip/decline policies need observation.

Completion requires fresh opening plus observed end of this conversation and safe
handoff. Register interaction_finished with scoped identity/role requirements.
Item received, healed party and story advancement require their own later native
receipts; conversation closure alone proves none of them. Generic speech cannot
complete Talk to Mom or other named targets without independent identity support.

Knowledge claims use subject, predicate, object/value, scope, provenance_refs,
source_kind, confidence/status, first_seen, last_seen and contradiction links.
Use the canonical knowledge store with additive schema versions; retain historical claims. Distinguish
native text transcription, semantic interpretation, reviewed fact and external
advice. Contradictions become explicit alternatives until independently resolved.
Deduplicate by scoped normalized content and semantic claim, not full-frame hash.

Novel relevant facts include service availability, directions, story prerequisites
and opponent hints. Flavor/repeated text need not create permanent fact records.
Store a compact dialogue digest/receipt even when no useful fact is retained.
An optional semantic analyzer returns strict relevance/claims JSON; no provider
is required for literal text/closure. Unavailable analysis queues a bounded pending
item or conservatively stores provenance, never blocks safe UI release forever.

Expose `knowledge.retrieve(query, scope, limit)` with bounded lexical/structured
retrieval first. Return reliability and evidence references, not flattened truth.
Subsequent B13 can improve inference/retrieval without changing proof authority.
No model or NPC text may change code, tools, priorities or verifier registration.

LAB: preserve any reviewed interaction trials and original source data; widen only
through tested adapter profiles. STREAM omits Mom-specific orchestration and keeps
Mom as a reviewed identity fixture inside the general entity/interaction contract.
Propagate B05 modes; evaluation writes go to the episode overlay, not training facts.
Feed meaningful approach/open/choice/closure and one-line new knowledge summaries.
No per-page screenshots or repeated full transcripts on the action overlay.

## Verification and gate

Test repeated sprites in different rooms, mobile NPCs, occlusion, unrelated existing
textboxes, repeated pages, multi-page ending, script motion and unknown choice.
Test irrelevant/duplicate/new/contradictory facts, malformed semantic JSON and
restart between choice dispatch and receipt. Keep named and generic proof separate.
Run stream_checks visibly; fixture identity labels are not new live named proofs.
Gate: two distinct recorded NPC interactions use the same tool, finish correctly,
and retain only novel relevant claims with provenance; a misidentified NPC holds.
A requested live demo uses the current position or an explicitly selected state.
Cue: “Talking is a complete interaction; useful information has a source.”
Update native coverage and capabilities; stop before adding services automatically.
