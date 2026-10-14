# B04 — Committed A*, measured exploration and progressive walking

Recommended coding model: **GPT-6.1 Sol · Extra High · Standard speed**.
Keep route intent, measured movement and recovery guards consistent.
See [model guidance](MODEL_GUIDANCE.md).

Playable order: R1. Dependencies: B00–B03. Next at a script event: B07a;
otherwise B05 learning support. B06/Director are not prerequisites for this demo.
Status: navigation implementation prompt. A local walking gate does not establish
reliable outdoor campaign traversal.
Copy with the canonical restart prompt. Implement this stage only.

## Build on the shared world

Implement one Navigate/Explore tool over B03's shared graph and recovery.
Do not construct a frozen bedroom controller followed by a replacement house
controller. A goal's target is data; the motor contract is the same in each room.
Deterministic routing is an actuator for learned decisions, not itself a Q learner.

## Tool and route contract

Navigate accepts a grounded chart/tile/entity/entrance reference, stop condition,
bounded action budget and risk profile. Reject ungrounded model coordinates.
Explore accepts a scoped area/frontier objective and return constraint, not raw
arbitrary buttons. Return typed results with measured movement/evidence and cause.
Neither completes a major goal directly; B06's trusted verifier does that.
Now provide small code-owned measured-arrival/coverage validators over B03 evidence
for this tool's receipts and B05 rewards. They need no GoalManager lifecycle;
B06 later registers the same validators in its general completion catalog.

Expose B00's permanent trusted direct-tool entry as a bounded operator command
and capability-aware Test Lab action. Accept a grounded target selected from the
current shared map or a bounded frontier objective, explicit budget and current
position or operator-selected authorized setup. Validate schema, UI, localization
and the single controller lease; return ToolResult/native measured-arrival evidence.
Document the EXACT generated CLI/panel operation at this gate; do not publish a
future command as already runnable. Missing tools are disabled with their cause.
This lets R1 walk/map before B06/B14. It is not a parallel goal lifecycle or a
hardcoded bedroom-to-house route. Later executor calls reuse this same tool.
At unknown script/dialogue/menu/battle, release controls, suspend mapping and hold.
Do not automatically advance Oak, acquire a starter or improvise A presses.

Plan A* over measured traversable graph, with explicit costs and directed passage
constraints. Candidate floor may support a proposed continuation, but only a safe
near-side approach then sensed short probe may test it. Unknown isn't confirmed
walkable. No path is preferable to silently cutting through uncertain walls.
Persist route ID, target, graph revision, next expected measured position and
reason for replan. Show the actual committed path on the map; distinguish proposed
unverified segments visually. Inputs must correspond to that next legal segment.
Existing path intent outranks curiosity or fallback Q choices while guards hold.

Guard every step against changed pose, UI, dynamic NPC, portal, collision evidence
and goal interruption. A new obstacle replans the same target; it does not choose
an unrelated direction. Apply failed directed-edge exclusions at every A* node,
not merely the first step. Exclusions expire/scoped by evidence and never erase
the physical map or convert repeated uncertainty into an invented wall.

Keep the last five MEASURED movement IDs, start/end poses, target distance and
result. Detect A-B-A cycles, zero progress and stale route execution. Replan with
temporary exclusions, choose another legal approach or return a useful held cause.
No repeat budget may cause blind recovery. If pose is null, B03 takes ownership.
Backtracking is allowed only along freshly localized known floor; remembered
commands alone cannot safely reverse an unknown position.

## Exploration and smooth movement

Exploration candidates are measured-reachable frontiers/entrances with information
gain, travel cost, safety and revisit counts. Before B05, use a clearly labeled
deterministic baseline ranking. B05 will learn option values without changing
the execution safety contract. Exhaustion is reported, not an infinite walk loop.

Smooth strides require calibrated speed, fresh full pose, stable world, same-facing
straight measured floor and clearance from NPCs/thresholds. Maximum two cells and
thirty frames; use direction-only walk capability with shorter settling. Turns,
unknown tiles, entrances and uncertainty require observation and shorter controls.
Recalibrate after disagreement; command duration never proves traversed distance.
Measure wall time and actual displacement; faster animation is not route progress.

Goal-scoped return avoidance can discourage an unnecessary upstairs loop while
leaving emergency/required destinations available. It cannot write walls/proofs.
Physical passage identity and B03's fresh recovery remain mandatory at transitions.
Known paths may become faster through confidence and better cost estimates, but
speed is never purchased by lowering localization or completion requirements.

## Acceptance and handoff

Visible tests: first input matches A*, every-node exclusions, cycle recovery,
stale pose/graph, candidate probe, NPC/portal guards, cancellation during stride,
maximum bounds, measured intermediate cells and intentional return-goal exception.
Report path agreement, unnecessary reversals, recovery holds, actual distance,
inputs and elapsed time. Test learning suggestions cannot bypass the legal mask.
No tests alongside a live owner; no restore without explicit episode selection.

Suggested live smoke gate when requested: five independent known-route arrivals
with no manual repair, chart duplication or unexplained path deviation. Include
both directions/entrances where supported; this is not statistical generality.
Preserve failures in the denominator and record the exact selected start states.

Observable gate: displayed committed path and measured inputs agree, stalls cause
replanning, and eligible known corridors walk faster without losing position.
Narration: “The planner chooses a destination; the navigator follows and checks it.”
Export registered navigation options, legal masks and measured outcomes to B05.
Stop before policy training, new story objectives or an unattended campaign.
For the stream, offer the bounded route/frontier demo after its gate passes;
execute only the operator's requested demonstration scope.
When an event blocks progress, retain the held session and apply B07a; do not wait
until all B stages exist to show movement, and do not resume without reconciliation.
