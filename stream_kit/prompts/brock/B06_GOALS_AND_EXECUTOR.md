# B06 — One goal graph and a general trusted executor

Recommended coding model: **GPT-6.1 Sol · Extra High · Standard speed**.
Lifecycle, evidence authority and single-owner dispatch are cross-module contracts.
See [model guidance](MODEL_GUIDANCE.md).

Status: TARGET IMPLEMENTATION PROMPT; general execution is not implemented yet.
Dependencies: B00–B05. Implement only this checkpoint when requested.
Playable order: R3 supporting step; early B07a can already exist without this executor.
LAB may reuse an inventoried GoalManager, completion windows and persistent queue.
Verify their behavior; recipe dispatch alone is not general step-graph execution.
STREAM builds the general executor directly; do not recreate recipe-only admission.

## Copy-ready implementation prompt

Read the foundation contracts and current capability inventory. Preserve existing
canonical history, manual blockers and original policies. Implement one rolling
goal graph beneath the operator's major objective, initially usable with existing
registered local tools. Do not implement a separate Brock runner or second goal DB.

Implement GoalManager create/get/get_ready/select/activate/block/suspend/resume/
complete/fail/cancel operations, adapting existing LAB names where needed. Statuses
are proposed, ready, active, blocked, paused, completed, failed and cancelled.
Each goal has a unique ID, type/target, source, priority, status, dependencies and
blockers, registered success criteria, created/updated timestamps, retry limits,
failure reasons and optional parent. Validate schemas, reject parent/dependency
cycles and invalid transitions, and default unadmitted proposals to proposed.
Parent grouping is not completion. Persist lifecycle/selection/evidence events.
Keep one canonical persistent operator-intent queue and one owned consumer. A queued
objective must not reset context or start another bridge owner during gameplay.

Extend B00's single code-owned ToolSpec catalog with supported game/UI profiles,
preconditions, effect hypotheses, cancellation/resource ownership, result schemas
and allowed completion-rule IDs; preserve its stable IDs/versioned strict arguments.
Add admission and execution against this catalog, never another registry. Publish
capabilities from it; remove duplicated availability booleans through LAB adapters.
Availability requires the implementation, verifier and current environment profile.

Use a bounded proposal envelope: schema_version, root_id, context_id, revision,
assumption_refs, steps. Each step carries local_id, goal_type, typed target,
tool_id, arguments, depends_on, completion={rule_id,parameters}, retry_policy.
Reject extra authority/code fields, unknown tools, arguments outside schemas,
dependency cycles, foreign roots/contexts and unsupported verifier parameters.
Maximum proposed horizon defaults to 12 nodes; expand only as execution needs it.
Model text supplies proposals, never Python, SQL, callbacks, trusted proof or status.

Expose adapters with these semantics; adapt names to repository conventions:
`admit_plan(root, proposal, capability_version) -> admission_report`;
`tick(root, run_context) -> dispatch_or_hold`;
`execute(tool_call, lease, run_context) -> ToolResult`;
`resume(tool_session, observation) -> ToolResult`.
ToolResult contains status, context/session IDs, observation/evidence references,
measured effects, failure_code, retryability and next safe owner. A success boolean
alone never completes a goal. Completion goes through the registered native verifier.

Persist dispatch intent before input, bounded session progress and the resulting
receipt afterward. Restart reconciliation observes the current UI before deciding
whether to resume; an ambiguous dispatch must not be blindly repeated. Make graph
admission/idempotency transactional and migrations additive with rollback tests.
Reuse existing tables where appropriate; supplementary executor tables are adjuncts
in the canonical DB, not duplicate goals/maps. Retain complete plan lineage.

Distinguish missing capability, missing knowledge, stale state, recoverable control
failure, tactical failure and infrastructure error. Missing knowledge may request
an advisory step; missing native tools remain blocked. Do not ask a model to invent
a completion rule when the catalog lacks one. Unknown pose invokes B03 recovery
before navigation or new strategic planning, while the active native UI owner may
finish its supported release protocol without pretending it has a world pose.

Keep three bounded ordinary continuations with changed evidence/recovery; identical
retries without progress exhaust visibly. Operator stop and bridge failure stop
input. Model cancellation/auth/config errors do not trigger blind retry loops.
Replanning supersedes only owned eligible AI children; preserve human blockers,
completed evidence and independent goals. A changed plan cannot erase failures.

Code-owned health/emergency admission can suspend a graph and later resume it.
Curiosity gets a bounded share only while prerequisites/safety permit; aging must
not let low-priority curiosity displace a ready major-goal step or emergency.
Register a deterministic scheduler policy and record selection reasons.

Reuse B00/B04's trusted direct invocation beneath dispatch, preserving one control
boundary. Initially a human may supply a bounded validated tool graph; general
AI-generated goals arrive in B14. The first graph uses available local navigation
and observation tools, not future bag/travel/battle placeholders marked available.

LAB: wrap working recipes as compatibility tools, keep their original roots and
proof receipts. The new executor must also execute real composite registered calls;
do not merely translate text back into old recipes. STREAM omits those
temporary coordinators; reusable tools, registry and graph executor are canonical.
Carry B05 mode, immutable policy references and actual write accounting through
every dispatch and resumption. This checkpoint itself adds no learned scheduler.

Show the major goal, selected child, blockers and at most five current cards.
Compact repeated/cancelled display entries without deleting raw records. Feed only
changed decisions, tool calls/outcomes, recovery and proofs; no scheduler polling.

## Verification and gate

Test dependency/parent cycles, malformed proposals, unsupported capabilities,
manual blockers, stale/cross-attempt evidence, idempotent admission and crash after
dispatch-before-receipt. Test composite execution, owner exclusion, emergency
pause/resume, curiosity starvation protection and resumed evaluation write denial.
Test a proposed Pikachu objective blocked by unavailable capture, never faked done.
Use recorded/mocked tool results with truthful labels; run stream_checks visibly.
Gate: one composite graph executes two registered tools, resumes across restart,
and completes only from fresh verified receipts. No live restore is implicit.
Cue: “One objective now selects reusable tools and keeps its place when interrupted.”
Update registry documentation and current status; stop after this gate.
