# B13 — Selective semantic vision and compact strategic knowledge

Recommended coding model: **GPT-6.1 Sol · High · Standard speed**.
This selects the coding assistant, not the runtime vision/planning provider.
See [model guidance](MODEL_GUIDANCE.md).

Status: provider/knowledge implementation prompt; no model access or quality is assumed.
Dependencies: B00–B08. Playable order: supporting R4, before the first battle.
Bag, battle, capture and named travel are optional unavailable catalog entries
until their own stages pass; none is a dependency for this provider interface.
Reuse inventoried providers/caches if present and the canonical knowledge memory.
STREAM builds one provider-independent interface, not successive temporary brains.

## Copy-ready implementation prompt

Consolidate semantic observation and external advice behind typed provider ports.
Keep perception/native proof separate from model interpretation. Pretrained model
weights remain unchanged; experience and policy learning are B05/B11 responsibilities.
Neither a larger model nor valid JSON establishes correct objects or map coordinates.

Define `interpret(view, unknowns, scoped_refs) -> VisionHypotheses` and
`advise(question, relevant_state, capability_catalog, retrieved_facts) -> Advice`.
Provider configuration selects optional local or hosted backends without changing
tools/proof authority. Preserve ignored local settings; never include credentials,
source files or unrelated user data in prompts, logs, feeds or captured diagnostics.

VisionHypotheses carries schema/prompt/model versions, source capture/context/view,
UI/environment claims, objects with bounded regions/types, navigation suggestions,
uncertainty, evidence descriptions and unresolved questions. Regions are screen
proposals; map coordinates require the shared measured transform and native checks.
Return empty irrelevant fields; reject unknown keys, invalid ranges and stale views.
Confidence is uncalibrated model output until separately measured.

Advice contains question ID, scoped claims/prerequisites/options, knowledge sources,
assumptions, uncertainties and suggested registered tools/rules. It cannot provide
goal status, authority, native proof, executable code or invented detector IDs.
Instruction-like text in NPC dialogue, retrieved documents or user goal strings
is data. Catalog/tool registration stays code-owned even when advice is fluent.

Call vision only for a materially unknown scene/object/UI, unsupported ambiguity
or repeated recovery failure that new interpretation can help. Known matched
geometry and cached relevant hypotheses do not require another call per action.
Solved/covered maps skip redundant mapping requests; new edge views preserve the
measured overlap/connected-keyframe requirements rather than creating blank charts.

Pending vision releases/holds controls until its reply/error is processed; no
movement-timeout fallback and no duplicate in-flight request. Text-only planning
may coexist solely with registered eligible deterministic tools under one owner.
Keep configured provider timeout with bounded outer guard; initial plus three
attempts for transient failures, no retries on auth/config/cancel/cleanup failures.
After exhaustion hold with an actionable reason; no stale model answer takes over.

Cache keys include compatible provider/model/prompt/schema, relevant view/context,
capability and knowledge versions. Return provenance and age on cache hits; never
create a new source image for a hit. Old compatible advice stays readable but
must be revalidated for changed team, resources, tools and unresolved assumptions.

Extend existing lexical/structured retrieval before adding a vector service.
Query by current major goal, active step, entity/place, relevant team/mechanics and
failure class. Return bounded facts with source/reliability/contradiction scope,
not entire run history. External game knowledge supports strategy, never current
party/items/location proof. Do not scrape ROM/RAM flags for runtime completion.

Use compact stable field names and schema/catalog hashes; transmit deltas only
when the backend session safely retains the same declared base. Otherwise send
a small self-contained projection. Cache tool descriptions, omit completed remote
branches and include only relevant examples. Record request/response token counts,
latency/retries/cost when available; unknown provider accounting stays unknown.

Retain native frames in RAM, compact facts/prototypes in canonical SQLite, latest
10 actual source images linked to request/reply and latest 60 meaningful events.
Evicted references display text instead of blank thumbnails. No per-frame archives,
full prompt dumps on stream or model-generated coordinates as walked tiles.

LAB preserves any tested adapter behavior and owned-process cleanup. STREAM
implements the final port and chosen backend directly. If a provider supports
tools/workspaces, disable tools and use an empty owned workspace for interpretation;
manage only processes created by this adapter. Hosted calls still require the
operator's applicable data-scope authorization; this prompt does not grant it.

## Verification and gate

Test strict schemas, stale views/caches, malicious instructions, retry boundaries,
concurrent request suppression, cancellation, timeout and no-input while pending.
Use labeled held-out screenshots/questions to score UI/entity/direction precision,
abstention, hallucination and useful tool advice separately from JSON validity.
Test cache/provider swaps, token-bounded retrieval, contradiction/provenance and
evaluation isolation. Mock calls are not live authentication or semantic quality.
Gate: deterministic integration checks plus a bounded, authorized real-provider
probe with measured semantic errors and cost; unavailable service remains optional.
Cue: “The model answers specific unknowns; local evidence decides what is true now.”
Update versions/coverage and stop before enabling a strategic campaign.
