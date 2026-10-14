# B01 — Native controls and stream observability from the beginning

Recommended coding model: **GPT-6.1 Sol · High · Standard speed**.
Escalate a diagnosed ownership/protocol failure to Extra High without widening scope.
See [model guidance](MODEL_GUIDANCE.md).

Playable order: R0. Dependencies: B00. Next: B02.
Status: implementation prompt; supplied overlays are presentation only. Native
I/O must be built and checked. No broadcast or state restore is authorized here.
Copy with the canonical restart prompt. Implement this stage only.

## Reuse and clean construction

LAB: inventory and adapt an existing native bridge/event publisher if present,
without changing working gameplay policies. Preserve independent /actions and /goal.
STREAM: create the Python bridge and scripts/mgba_bridge.lua against the final I/O
contracts, and connect the supplied panels. Do not require late gameplay modules
just to show a panel; the starter does not include a gameplay controller.
Serve an early operator surface backed by B00's single ToolSpec catalog; unavailable
tools stay disabled with the missing stage visible. Expand it in place later.
Attach the visual feed renderer to B00's existing DomainEvent/check receipts;
do not replace the offline check CLI or add another capability registry.
The copied stream kit's stdlib-only `python stream_kit/serve.py --view-only`
can show honest empty panels before this stage; see ../../OVERLAY_OPERATIONS.md.
Keep /health and disabled operator controls in that mode. B01 integrates live
event publishing and bounded native I/O; displaying a panel alone does not pass it.

## Native bridge contract

Use native mGBA Lua screenshots and bounded button input; no game RAM or ROM flags.
Handshake reports protocol version and supported commands/buttons before input.
Expose observe, bounded press, direction-only walk, release/stop, save and load.
The latter two use validated owned checkpoint names; load needs the operator's
explicit state selection for that run. No recovery path may silently restore.
Every command carries a unique ID and bounded argument range; consume each reply
once. Reject stale/malformed/mismatched replies and fail closed on timeout.

Python owns the controller lease; Lua enforces a watchdog and releases keys when
input expires, a stop arrives or its session becomes invalid. A stop survives a
pending vision/model call; no unbounded press or queued blind navigation sequence.
Retain ordinary press settling and expose walk1's shorter direction-only settling
as a distinct capability. B04 decides when smooth walking is physically justified.
Do not assert that a fixed frame count equals one tile.

Fresh captures get immutable IDs, context and timestamps. Read and consume owned
PNG replies into RAM; optional preview replaces one diagnostic file. A filename
reuse must never make stale pixels fresh. Keep bridge health distinct from game
state: missing screenshots are infrastructure failure, not collision or defeat.
Do not launch a second controller from a second browser tab or test suite.

## Stream presentation contract

Retain sixty meaningful feed events across launches with source and timestamp.
Reset transient controller/status state at each launch; old actions stay history.
Show all supported buttons, active press/release and newest activity nearest them.
Update movement outcomes on their own row; never overwrite a newer model event.
Show input, changed route, learning, recovery, memory, model call/reply and checks.
Deduplicate heartbeat, stability, cache and unchanged premapping messages.

/goal shows current intention and evidence-aware status in readable stream text.
/dashboard composes the actual Actions/Goal panels around a transparent 40–60%
game column for OBS's native mGBA capture. No screenshot placeholder in that space.
Reserve fixed checkpoint cards and at most five current major/subgoal/emergency
cards; no viewer scrolling required. Empty real data says idle, never fake success.
The model is one feed source, not the dashboard's central subject.

Provide /test-lab with profile, run mode, objective, bounded repetitions, explicit
checkpoint choice and Stop. For this stage only ready I/O diagnostics can execute.
Display actual effective values and the single current owner. Later B06 provides
goal admission/queue; no temporary arbitrary command endpoint or eval execution.
Viewer GET requests are read-only, including no DB initialization/migrations.
Operator POSTs retain token, origin/Host and bounded-schema validation.

## Model image retention interface, not a model dependency

Reserve call IDs for future semantic requests. Retain at most ten actual source
images linked to request and one-line response; cache hits create no new image.
Evicted images display an explanation. Do not fabricate model traffic here.
Checkpoint PASS/FAIL/INTERRUPTED counts remain separate from goal completion,
actions and inference counts. Render mocks/recorded/live checks truthfully.

## Acceptance and handoff

Visible offline checks: stale response, request timeout, rejected command, expired
lease, queued Stop, release on exception, no key latch, capture consumption,
cross-profile isolation and read-only viewer requests. Test event retention and
source-row identity; verify panel markup/styles in a representative OBS layout.
Use stream_checks as the sole publisher; wait if gameplay owns the feed/bridge.

An operator-requested live check may observe/release and send one bounded input
at the current position. It is not implied by installing the bridge. A Lua reload
may require the operator; provide the exact dofile path from their actual profile.
Observe capability acknowledgment after reload; do not repeatedly guess success.

Observable gate: native capture freshness, bounded input/release and Stop are
demonstrated, and the same trace is readable on the stream panels. Mark offline
and live gates separately. No mapper or AI success may be claimed at this stage.
Narration: “You can see every control and every decision from the first test.”
Document the bridge protocol and operator startup commands; hand fresh in-RAM
observations plus typed events to B02. Stop before adding perception or a run.
