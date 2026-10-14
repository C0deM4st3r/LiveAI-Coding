# B11 — Outcome-trained battle decisions and measured improvement

Recommended coding model: **GPT-6.1 Sol · Extra High · Standard speed**.
Separate control faults from tactical outcomes and compare immutable policies.
See [model guidance](MODEL_GUIDANCE.md).

Status: battle-learning implementation prompt; B10's deterministic baseline is not learning.
Dependencies: B05, B06, B07b and B10a (with their transitive dependencies).
Playable order: R6; B09/B10b are not required to learn the admitted first-battle profile.
Reuse B05 learner/version/experiment machinery; keep a separate battle policy.
Neither this prompt nor repeated fixed tactics alone constitute learning.

Start with B10a's actual legal action/reader coverage; switch/item/wild/new-move
states remain unavailable until B09/B10b pass. Keep the final state/action schema
extensible and profile-versioned. Later widening requires fresh mask/abstraction
compatibility and evaluation checks, not a second learner or automatic generality.

## Copy-ready implementation prompt

Implement an interpretable goal-conditioned battle decision learner over B10's
legal actions. Start with tabular/context-conditioned action values and measured
outcome statistics, not pretrained-model fine-tuning or an unbounded deep-RL job.
The final agent combines learned decisions with trusted controls and game advice.

Define versioned BattleState abstraction: encounter class, opponent/type knowledge
reliability, own member/move capabilities, level/damage estimates, discretized
HP/status, PP/resource bands, observed stat changes, team alternatives and objective
(win, survive, escape or later capture). Use compact meaningful categories rather
than screenshot hashes. Unknowns get explicit bins; do not backfill guessed values.
Retain raw evidence refs so future abstractions can reprocess valid transitions.

Define battle actions by skill semantics plus concrete validated target bindings:
damage/status move, switch, supported item, run and later capture. Generalization
must not merge moves with materially different effects or treat unknown mechanics
as known. Use current legal-action masks at selection and bootstrap; no zero-PP
action becomes attractive because it was legal in an old observation.

Expose `choose(state, legal_actions, mode, policy_ref) -> decision`,
`record_transition(before, executed_action, after, outcome_refs) -> transition_id`,
`update(transition_id, training_run) -> update_receipt`, and
`evaluate(candidate_ref, frozen_manifest) -> report` using B05 interfaces.
Record behavior policy, action probability/exploration seed, state/adapter versions,
real/replay update counts and parent policy. Store supplemental policy/experience
records in canonical SQLite with immutable released artifacts and additive schema.

Use B05's masked Q-learning equation with a battle-specific state/action/reward
version. One accepted resolved turn is the primitive unit; use duration-aware
discount when an option spans multiple verified turns. Specify learning rate, discount, epsilon schedule,
initialization, tie handling and deterministic seeds. No silent parameter changes.
Baseline mechanics/rules may initialize or constrain choices, but retained values
must actually change from measured experience and affect subsequent decisions.

Rewards prioritize native objective outcome, survival and useful measured effects.
Register bounded shaping for HP/resource cost and wasted legal turns; avoid rewards
for pressing buttons, opening a menu, reading the same textbox or repeated heals.
If using progress potential, document terminal/reset treatment to avoid reward loops.
Exploration stays within safety/legal masks and configurable health/resource limits.
No guarantee that every episode improves; retain failed tactics and uncertainty.

Only observed accepted actions with reliable before/after/terminal evidence update
the tactical learner. UI faults/timeouts/unknown outcomes are separately retained
for engineering metrics, not mislabeled defeats or attack damage. If an interrupted
transition lacks a next state, quarantine it; do not invent reward or bootstrap.
Deduplicate receipts so resume/replay cannot double count a physical turn. Replay
may reuse eligible records with provenance and explicit separate update counters.

Train permits registered updates; execute selects frozen values without updates;
evaluate uses B05 immutable policy/map/fact/perception manifests plus fresh isolated
episode overlays. Reset transients and RNG/seed according to the experiment plan;
evaluation evidence must not leak into training or later evaluation episodes.
Compare against the preserved deterministic baseline, not a deliberately weak
replacement. Keep configuration, starts, verifier and action/resource limits equal.

Register metrics: wins/losses/unknown/control failures, completed/attempted episodes,
turns, HP/resources remaining, interventions, model cost and legal-action violations.
Report conditional tactical metrics separately from end-to-end success, with all
failures in the relevant denominator. Predeclare sample sizes and confidence
intervals; do not select only favorable episodes or tune on the evaluation set.

Policy promotion requires passing regression/safety gates and the declared frozen
comparison; save candidate even when rejected. Full held-out Brock success belongs
to B16, not a rival-only improvement. Keep at least the previous released policy
and its manifest for rollback. No automatic deployment to STREAM from LAB training.

LAB preserves existing movement policies and battle history; never reinterpret old scripted
battles as proof the new policy learned. STREAM builds this learner once with the
same tests and loads only an explicitly promoted compatible artifact, or trains
from a declared fresh baseline if the stream narrative chooses that experiment.

## Verification and gate

Test an evidence-backed synthetic environment where different rewards lead to
different chosen legal actions, terminal/bootstrap math, masks, unknown values,
duplicate rejection, seed reproducibility, replay accounting and no eval writes.
Test reward-loop prevention, UI failures excluded from tactic updates and policy
serialization/rollback. A synthetic learning pass is not a real-game win.
Gate: reproducible value/decision change plus a frozen recorded comparison report;
then an explicitly authorized native training/evaluation experiment before promotion.
Cue: “Past outcomes now change decisions; a separate test checks whether that helps.”
Publish truthful learning metrics and stop at the requested experiment boundary.
