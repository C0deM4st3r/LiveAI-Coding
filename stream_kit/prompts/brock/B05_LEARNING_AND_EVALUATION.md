# B05 — Real decision learning and honest evaluation

Recommended coding model: **GPT-6.1 Sol · Extra High · Standard speed**.
Evaluation isolation and policy-write accounting are required at this setting too.
See [model guidance](MODEL_GUIDANCE.md).

Playable order: R3 learning/support, after R1 and optionally the first B07a event.
Dependencies: B00–B04; B07a is not required for navigation learning. Next: B06.
Status: target implementation. A route-learning flag alone is not a full freeze;
evaluation is available only after every relevant write path is isolated.
Copy with the canonical restart prompt. Implement this stage only.

## Build the final learner; preserve any existing LAB baseline

LAB: inventory every policy/replay/map/prototype/fact write and every launcher,
including goal repeat, queue, resumed tools and dedicated batches. Adapt existing
learners behind one mode/storage contract; preserve their original data unchanged.
STREAM: start directly with goal-conditioned option learning. Do not recreate
legacy screenshot-hash Q policies or room-specific training flags as production paths.
Keep old LAB policy snapshots as labeled baselines, never silently migrate Q-values
into states with different meaning. B11 extends the shared machinery to battles.

## Concrete first learning policy

Implement a small interpretable semi-Markov option-value learner over registered
navigation/exploration options, using masked epsilon-greedy training and frozen
greedy execution. State includes goal type/relative target, verified place/pose,
local occupancy/frontier features, UI and resource-risk buckets; unknowns explicit.
Version the abstraction. Keep absolute map IDs as retrieval/context, not the only
feature, so repeated geometric situations can share experience where justified.
An option is a bounded Navigate/Explore invocation with a known legal precondition;
it is not a free-form model instruction or an uncontrolled button sequence.

Update from measured transitions (s, option, rewards, duration, s', terminal) with
duration-aware discounting and legal-next-option mask. Keep real and replay update
counts separate. Replay only recorded verified transitions; deduplicate identities.
Use Q(s,o) <- Q(s,o) + alpha * [R + gamma^tau * max_legal Q(s',o') - Q(s,o)].
R is the discounted sum of primitive-step rewards; tau uses the same documented
step unit, never wall-clock model latency. Terminal success/failure has zero
bootstrap; truncation is explicit. Start with configurable alpha=.1, gamma=.99,
epsilon=.2 and deterministic tie-breaking; these are baseline settings to measure,
not tuned guarantees. Persist effective settings and any declared decay schedule.
Skip or separately classify uncertain execution/perception failures rather than
teaching that a screenshot timeout means the tactical choice was wrong.
Learn expected option cost/risk from measured attempts; A* still executes routes.
Use only nonnegative bounded route costs, with geometric distance as an admissible
heuristic where valid. Learned values cannot bypass B04's committed-path guards.

Define versioned rewards before training: trusted completion, verified new coverage,
measured progress, elapsed steps/time, repeated stalls and observed resource loss.
At this stage use B04's code-owned measured-arrival/coverage validators over B03
evidence, not the future B06 goal lifecycle. Carry those validators forward into
the completion catalog; never create a second goal system to calculate reward.
Use bounded potential-based shaping when progress potential is well-defined.
Cap novelty reward per episode/evidence identity; circling, chart fragmentation,
revisiting, model claims and self-generated subgoals cannot farm reward.
Keep terminal success distinct from truncation, operator Stop and infrastructure
failure. Do not reward an unverified goal just because a tool returned success.

## Enforced modes across every entrypoint

- Train: candidate policy/replay updates allowed from accepted experience; world
  knowledge accumulates with provenance. Log exploration settings and real writes.
- Execute: promoted frozen policy, no optimizer/replay updates; fresh world/fact
  knowledge and episode evidence can be recorded. Exploration follows an explicit
  execution setting, never a hidden training default.
- Evaluate: immutable snapshot of policy, maps/facts, retrieval/prototypes and
  relevant configuration. Each independent episode starts with a fresh isolated
  overlay for current pose, new observations, proofs and telemetry. No evaluation
  discovery leaks to the next episode or back into the training snapshot.

Enforce permissions at repositories/transactions, not scattered if-statements.
Propagate EpisodeContext through CLI, panel, queue, retries and every nested tool.
Mode cannot change mid-episode; display effective mode before starting. Do not
silently interpret old --frozen-routes/learn_routes=False as Evaluate; explicit
compatibility mode reports legacy semantics until operator selects the new mode.
Hash frozen artifacts before/after; reject policy writes and record attempted
violations. Evaluation still senses, localizes and recovers in its transient layer.

## Metrics, promotion and regression gates

Persist policy lineage, state/reward version, seed, environment/checkpoint hash,
capability/perception/config manifest, model identity/cache policy and all attempts.
Report stage reached, verified success, held/failure reasons, interventions, inputs,
time, route agreement, localization faults, novel walked cells, real/replay updates,
resource use and model calls/cost. Later battles add turns/HP/PP/native outcomes.
Same emulator state plus same seed is repeated exposure, not independent evidence;
predeclare held-out starting variants/seeds and separate training/evaluation sets.

Compare candidate with a frozen rule/legacy baseline on matched authorized starts.
Use a predeclared sample, initially at least twenty episodes per condition where
feasible, and report counts/uncertainty instead of promising significance. Five
clean runs are a smoke gate only. Promote an immutable policy artifact only after
the stated held-out gate; keep rollback, failed candidates and evaluation history.
If no measurable improvement, report that honestly and inspect state/reward/tool
failures. More updates or a single lucky win is not a learning result.

Run visible tests for state abstraction, masks, duration discount, reward abuse,
replay deduplication, all launcher modes, nested write denial, per-episode snapshot
isolation, reproducibility and original-data hashes. Use recorded/mock outcomes.
Live training/evaluation requires an explicit operator run/checkpoint selection;
this implementation prompt does not authorize automatic restores or twenty runs.

Observable gate: Train changes only its candidate from verified experience;
Execute leaves policy unchanged; Evaluate leaves all frozen artifacts unchanged.
Narration: “Now we can measure what it learned against the same frozen baseline.”
Hand B06 a policy/experience API, effective mode and evidence-aware episode reports.
Record implementation separately from live learning improvement, then stop.
