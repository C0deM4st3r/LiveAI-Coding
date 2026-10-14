# B00 — Target architecture and isolated build profiles

Recommended coding model: **GPT-6.1 Sol · Extra High · Standard speed**.
Use Astra Ultra only for an optional bounded independent architecture audit.
This is an engineering recommendation; see [model guidance](MODEL_GUIDANCE.md).

Playable order: supporting step for R0. Dependencies: none. Next: B01.
Status: specification for the final build, not an implemented Brock capability.
Copy this prompt with the canonical restart prompt. Implement this stage only.

## Intent and starting evidence

Build a visual agent that learns reusable decisions and can eventually complete
the operator's single objective “Defeat Brock” without step-by-step intervention.
Learning must change a versioned policy from measured outcomes; persistent maps
and pretrained-model advice are valuable but are not that policy training.
The public starter contains prompts, guides and presentation code only. No gameplay
implementation, learned policy, recorded game fixture or live success is included.
Begin from a fresh checkout of this starter. Inventory its presentation files;
create gameplay components in the stages below and claim only gates actually passed.

## Start the implementation in this workspace

- Build this clean checkout in the index's R0–R10 playable order. Implement the
  final interfaces directly, not one-off runners,
  hardcoded room macros or screenshot-hash Q policies that later get replaced.
- Profile configuration resolves absolute owned runtime/data/bridge paths before
  any mutation. Training, evaluation and execution profiles must isolate writable
  stores and bridge mailboxes. An active emulator has exactly one controller across
  profiles. Evaluation snapshots and per-episode overlays are defined in B05.
- The supplied panels contain no trained agent, learned map or game evidence.
  Create these through the implementation and authorized observations; do not
  import hidden dependencies or pre-trained memories to satisfy a build gate.
- Do not create a second emulator, restore state or launch a gameplay episode here.

## Stable boundaries to implement now

Use small typed interfaces whose payloads are versioned bounded data:

1. Observation: capture_id, timestamp, game adapter, context/episode, native UI,
   pose or null, measured features, uncertainty and immutable evidence references.
2. StateSnapshot: observation IDs, revision, world/place references, current UI,
   team/inventory/story facts with freshness, goal context and legal tool mask.
   Unknown fields remain unknown; later modules add facts via versioned schemas.
3. ToolSpec: tool ID/version, typed arguments, preconditions, legal UI/context,
   owned resources, cancellation boundary, possible results and evidence types.
4. ToolResult: required request/episode IDs, optional goal ID for direct operator
   invocation, succeeded/blocked/held/failed/cancelled,
   reason code, observed state delta, native evidence IDs and next safe handoff.
   Tool execution success is not automatic goal completion.
5. EpisodeContext: profile, mode, IDs, seed, checkpoint authorization, capability
   manifest, policy/config/perception/schema versions and cancellation token.
6. PolicyDecision: candidate IDs, legal mask, chosen option, value/confidence,
   policy version and exploration/exploitation reason; never executable model code.
7. DomainEvent: monotonic sequence plus UTC time, correlation/source/severity,
   concise English message and bounded typed payload; exclude credentials/frames.

Implement these contracts directly; do not fabricate empty
“supported” tools. Unimplemented capabilities are absent or explicitly blocked.

Own the single minimal code-owned ToolSpec catalog now: bounded schema validation,
versioned registration, lookup and capability projection. Later stages register
their tested tools here; B06 extends this same catalog with graph execution and
admission, never creates a second registry. Catalog entries grant no input before
the corresponding executor, profile and ownership checks exist.

Create the gameplay package and its minimal event/check CLI now; use
`python -m pokemon_ai.stream_checks` (or document the equivalent package command).
Emit DomainEvent receipts and bounded PASS/FAIL/INTERRUPTED results to the
console/offline record sink. Display the supplied stream kit immediately in
read-only/view-only mode;
see ../../OVERLAY_OPERATIONS.md. Missing runtime/DB means an honest empty state,
not a dependency on future gameplay modules. B01 attaches this same renderer to
events. Later stages extend this same check runner. No supplied
panel may import a missing executor or enable controls just to start the display.

Define the trusted direct-tool invocation seam here: validated ToolSpec arguments,
EpisodeContext, ownership/precondition checks, cancellation and typed receipt.
B04 implements its operator CLI/control entry for registered Navigate/Explore;
B06 later dispatches through that same seam. This permanent diagnostic capability
needs neither an LLM nor a throwaway room/story coordinator. Never admit raw model
commands, arbitrary Python or unsupported tools through it.

## Ownership, persistence and failure rules

Keep SQLite as the authoritative shared memory. Define canonical module-owned
schema boundaries for goals, world, team, battles, knowledge and the intent queue;
create each module's tables only when its stage is built. Share stable IDs across
modules. Migrations are transactional, version checked and tested on temporary
database copies; preserve records as this build evolves. The supplied panels use
a read-only presentation projection, not authority to choose gameplay table names.
Document the projection schema and adapt canonical records at that boundary.
No runtime dependency on Redis, a separate vector DB or an LLM is required here.

One supervisor owns the emulator lease and delegates bounded tool invocations.
Use an emulator-instance-wide named mutex/lease identity shared across profiles,
plus a bridge session/fencing token that rejects commands from stale owners.
Separate profile lock files are insufficient: all profiles contend for the same
mGBA instance even while their writable data/mailboxes stay isolated. Prove that
cross-profile ownership cannot overlap before admitting input from any profile.
UI/mapping/planning cannot issue concurrent input. Stop cancels the whole owned
batch, releases keys and records a terminal stop; a checkpoint budget is separate
from an infrastructure failure. Lease recovery must prove the prior owner ended.
Persist resumable intent, not in-flight key presses; restart begins with sensing.

Separate permanent experience/proofs, mutable policy candidates, frozen artifacts
and per-episode transient state. Define train/evaluate/execute in the envelope now;
B05 enforces all writes before claiming evaluation support. Model/chat payloads
cannot register tools/verifiers, grant emergency priority or bypass this boundary.

## Acceptance and handoff

Run the minimal offline check CLI and retain its receipts;
visual publication begins in B01. No missing-panel import is a B00 dependency.
Test schema/catalog bounds/version rejection, path isolation, one-owner conflict, restart
with stale lease, cancellation propagation and transactional migration rollback.
Tests must use temporary stores and mock I/O; no live restore or model request.
Record test-store fingerprints and schema versions without exposing configuration secrets.

Observable gate: two isolated profiles can load the same contracts, reject unsafe
cross-profile writes, and emit a truthful idle/check event with zero game input.
Narration: “One agent owns the controls; every decision and result has a trace.”
Update the manifest as implemented/fixture-tested, not live-verified. Export the
interface/schema inventory and profile commands for B01. Stop at this gate.
