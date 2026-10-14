# B14 — One major objective, adaptive subgoals and learned skill choice

Recommended coding model: **GPT-6.1 Sol · Extra High · Standard speed**.
Director planning, verified completions and resumable execution must remain separate.
See [model guidance](MODEL_GUIDANCE.md).

Status: general-director implementation prompt; narrow recipe planning is insufficient.
Dependencies: B00–B08 plus B13. Playable order: R4, before battle/inventory work.
B09/B10/B11/B12/B15 capabilities are absent until their own gates pass.
Use B06's executor/GoalManager/queue, not another scheduler or battle coordinator.
Build this rolling director directly; prior gameplay tools remain independently callable.

## Copy-ready implementation prompt

Implement a general strategic director receiving one typed operator objective,
for example Defeat Brock. It reasons over observed progress, retrieved game
knowledge, learned costs/outcomes and the current registered capability catalog.
The same architecture must support different objectives without a new Python
runner for each. A Brock-specific fact adapter/verifier is allowed; a fixed
button route or mandatory scripted subgoal chain is not the target architecture.

Expose `propose(root, state_projection, knowledge, capabilities) -> PlanProposal`,
`validate(proposal) -> admission`, `observe_result(receipt) -> revision_reason`,
and `request_replan(reason, evidence_refs)`. Delegate dispatch/lifecycle to B06.
The input projection includes goal evidence, current UI/pose freshness, team,
inventory, relevant grounded places/passages, failures, resource/health limits,
mode/policy versions and a compact view of live child tasks.

PlanProposal uses B06's bounded schema and horizon (default at most 12 nodes).
Include assumptions with reliability, missing knowledge, candidate alternatives,
registered completion conditions and estimated cost/risk with uncertainty.
Every executable step needs valid typed arguments, capability support, accessible
state/preconditions and a trusted completion rule. Unknown location is a recovery
need, not permission to fill a coordinate. No model claim grants emergency rights.

The operator enters only the major goal; director selects intermediate objectives
from evidence. For Brock it may need starter/story travel, training, healing or
optional capture, but the chosen sequence depends on actual progress/team/tools.
Already verified progress may satisfy prerequisites under their current rule;
historical receipts cannot certify a fresh acquisition/encounter episode.
Before B15, missing named travel/story tools visibly block the relevant branch.

The first playable root is Get the first Pokémon, using current grounded local
B04 targets/frontiers, B07a event handoff, B07b interactable/choice/team receipts
and B08 NPC support. B13 can propose a grounded next probe from current evidence;
it cannot invent a known named-place route. Local tools may cross measured nearby
passages with fresh recovery, but general named travel stays a B15 capability.
Require an actual clean native starter trial before calling R4 live-ready.
If an unimplemented battle begins, transfer to a held missing-capability state;
add B10a to the same registry later, then explicitly reconcile/resume. Do not build
a new first-rival director. Root acquisition and battle outcome remain distinct.

Do not repeatedly regenerate identical child tasks. Stable semantic keys and
assumption/evidence revisions reconcile eligible owned tasks, retain successful
skills and preserve prior failure lineage. Root completion is the independent
root verifier, not “all model-proposed children are done.” Manual goals/blockers
remain untouched by plan reconciliation. Current UI owners finish safe handoffs.

Trigger replanning on verified step outcome, changed capability/assumption,
unresolvable route failure, resource/health emergency or contradictory knowledge.
No per-frame replanning, heartbeat requests or unconditional request after every
button. B03 recovery precedes new strategy when world pose is invalid; active
native battle/dialogue owners may handle their UI before any world navigation.
Unknown mechanics request bounded B13 advice; missing execution stays blocked.

Add genuine learned strategic selection using B05's option-value machinery and
verified B06 skill transitions: state abstraction includes goal/progress, observed
team/resources, place/route uncertainty and capability availability. Actions are
admitted alternative skills/targets, not arbitrary text. Learn duration/cost/risk
and outcome values; legal/admission masks always override learned preferences.
Store explicit real/replay updates and policy version. Model-generated plans are
proposals, not learned weights; identify their separate contribution in metrics.

Curiosity operates only within an explicit resource/time share and chooses useful
unknowns supporting present/future goals. Penalize repeated known dead ends via
measured failures; do not rewrite geometry into walls or exclude emergency routes.
Code-owned health interrupts suspend the active major plan and use available
verified recovery tools. Resume its persisted target after recovery, not from zero.

Enforce operator-configured elapsed/action/model-cost limits, cancellation and
three ordinary no-progress recoveries with distinct evidence. Continuous mode
means continue while progress/recovery is viable, not infinite identical failures.
Resource limits are run controls, not a reason to abandon an otherwise valid local
action early. At an actual boundary persist a resumable hold and precise cause.

Use only the general director/executor and final reusable tools; no
starter-specific or first-rival-specific control plane. Preserve game adapters,
completion validators and native evidence. No autonomous code generation/plugin
installation when a capability is absent. Propagate B05 modes through every layer.

## Verification and gate

Test the same director across different mocked major goals, changing team/resources,
completed prerequisites, missing tools/knowledge, contradiction, health interrupt,
restart and unsupported requests. Verify no child spam, no model completion and
no eval learning writes. Test learned option values can change a legal selection.
Use adversarial proposals with injected code/authority/foreign roots; reject them.
Gate: a multi-step simulated campaign replans after a genuine changed assumption,
resumes after emergency and stops on missing travel rather than faking Brock.
Any real current-tool demo is separately requested; the full campaign waits for B16.
R4's live gate is one requested clean first-Pokémon root using these same tools,
with fresh acquisition/team/world evidence and no repair or special macro dispatch.
Battle, item and long-travel requests must remain blocked until their own gates;
the simulated emergency test does not claim live healing before B09.
Cue: “One objective stays fixed while the agent changes its plan from experience.”
Update status and capability dependencies; stop after this checkpoint.
