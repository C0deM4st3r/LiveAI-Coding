# B16 — Brock curriculum, independent evaluation and stream promotion

Recommended coding model: **GPT-6.1 Sol · Extra High · Standard speed**.
Optional final audit: Astra Ultra for bounded independent evidence/release review.
Neither model replaces native trials or the release gate. See [model guidance](MODEL_GUIDANCE.md).

Status: TARGET RELEASE GATE; no autonomous Brock win exists from this prompt.
Playable order: R10. Dependencies: B00–B11 (including B07a/b and B10a/b), B13,
B14 and B15. Add B12 only if the admitted strategy needs capture. Every actually
selected tool/profile and verifier must have passed its own gate; an early slice
receipt never qualifies untested later branches.
LAB is the testing/training ground; STREAM receives only declared promoted results.

## Copy-ready implementation prompt

Implement experiment profiles and the final Defeat Brock objective using B06/B14,
not a new scripted Brock runner. The operator supplies the major objective; the
director discovers required subgoals from current evidence, knowledge and tools.
Keep original game files, skills, shared charts, failures and history protected.

Admission checks capability/adapter coverage, policy and knowledge versions,
single ownership, supported UI, current evidence freshness and missing prerequisites.
Register a typed named-trainer objective and independent native completion rule.
Brock identity must be scoped to this encounter via reviewed native name/profile
evidence; a generic battle win or another trainer's defeat cannot complete it.

Support fresh named encounter victory with terminal evidence or an independently
read new badge/reward receipt tied to this encounter and prior state. Use explicit
rules for what each receipt proves; an already-owned badge is not a new victory.
Separate objective success from post-battle team/UI/world closure; require both
for a clean campaign run. Unknown/ambiguous result stays unresolved, never won.
No manual confirmation is required on supported verified native branches; missing
reader coverage remains blocked rather than substituting an LLM claim.
The [Pewter Gym script](https://github.com/pret/pokefirered/blob/master/data/maps/PewterCity_Gym/scripts.inc)
is knowledge for verifier design, not a runtime flag/ROM/RAM source. Reward each
scoped encounter outcome once; rereading a badge cannot produce another win/reward.

Define ExperimentProfile: ID/version, major objective, mode, start provenance,
policy/map/fact/perception/config/capability hashes, seed scheme, authorized episode
count, resource/time limits, curriculum stage, verifier version and stop policy.
Named checkpoints are operator-selected test fixtures, not free reset permissions.
Each requested batch explicitly authorizes its starts/repeats; exhausted retries
cannot silently create additional episodes or restore outside that batch.

Stage curriculum by observable gates: local route/return; starter/UI; first rival;
local bag/healing and wild fight; travel/story/parcel; forest/Pewter/gym access;
named Brock fight; complete one-root campaign. These are engineering experiments,
not mandatory runtime subgoals if the actual episode already satisfies them.
Capture is an optional separate gate only when the chosen strategy calls for it.
If a perception/control fault repeats, fix it before accumulating useless batches.

Train mode updates registered movement, battle and strategic policies from native
eligible transitions. Preserve all candidate lineage, rejection and failure reasons.
Periodic snapshots are immutable. Knowledge/maps may grow in training with existing
proof rules; model inference remains pretrained. Do not describe one repaired win
or more database rows as demonstrated learning.

Evaluate baseline and candidate using equivalent explicit starts, budgets, seeds,
capabilities/verifiers and identical immutable map/fact/perception snapshots.
Each episode uses a fresh isolated overlay for live pose/evidence/discovery; no
evaluation discoveries or policy updates leak into another episode or baseline.
Include more than one entry/camera/party condition before claiming transfer.
Held-out campaign episodes must not be used to tune the candidate being evaluated.
An identical save-state and emulator RNG replay is not an independent sample just
because the policy seed changed; report repeated-start reliability separately and
document the independent start/encounter variants used for broader comparisons.

Predeclare sample size and success threshold appropriate to cost. A practical
initial comparison is at least 20 independent episodes per condition, but report
counts and uncertainty; that number alone proves no improvement or reliability.
Preserve every attempted episode and distinguish verified win, tactical loss,
control/perception failure, missing capability, operator stop and infrastructure
error. Report both all-attempt and applicable stage/tactical denominators.

Metrics include stage reached, root/subgoal outcomes, interventions, actions/time,
route/cycle/localization failures, native battle turns/HP/resources, model calls/
tokens/cost, real/replay updates and policy versions. Assisted resumes are labeled
assisted and excluded from clean-autonomy success, while remaining in full history.
Timeout is not a tactical defeat; full campaign failure still counts in end-to-end
reliability. Operator Stop/emergency-stop ends the batch. An in-game low-health
emergency suspends the current objective, uses supported recovery tools and resumes
after verified recovery; unresolved recovery holds rather than silently ending or
restarting the batch. Allowed gameplay failure can advance only to the next already
authorized episode. Infrastructure failure never acts blind.

Create PromotionManifest with immutable code/config/schema/model/prompt/adapter
versions, policy artifacts/hashes, declared knowledge/map seeding, fixture/test and
live reports, known limitations, rollback manifest and explicit approval record.
Do not copy credentials, ROMs, unsanctioned saves or all LAB mutable history into
STREAM. Artifact transfer is explicit; never overwrite working stream policies
mid-run or silently seed a “learning from nothing” demonstration with trained data.

STREAM rebuilding from the canonical prompts implements this final architecture
once. It can start fresh learning or load a declared promoted policy/knowledge set;
state which on screen. LAB experimentation continues independently; promotion
requires its gate and operator action. No commit/push/broadcast/deletion is implied.

## Verification and gate

Test profile propagation, explicit-start authorization, episode limits, stop/error
semantics, evaluation isolation, denominator accounting, stale/wrong Brock/badge
proof, post-battle closure, manifest integrity and rollback compatibility.
Run serial visible stream_checks; then the explicitly requested staged native
experiments. Record fixture, live-assisted and live-unassisted evidence separately.
Release gate: supported full objective completes without manual steering in the
declared independent evaluation, meets its predeclared reliability/performance
threshold, and demonstrates actual outcome-driven policy change without regression.
Cue: “The agent receives one objective; independent runs measure whether learning helps it finish.”
Publish the report and proposed manifest; do not auto-start another milestone.
