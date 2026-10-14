# One AI. Every Pokémon Game. — canonical restart

Updated 2026-10-14. Active components: **B00–B16**, built through playable gates
**R0–R10**. B numbers identify parts, not strict execution order; old 01–57 is history.
[Index and current next prompts](stream_kit/prompts/brock/README.md) ·
[Architecture](BROCK_ARCHITECTURE.md) · [Stream walkthrough](STREAM_GUIDE.md).

This public starter ships prompts, guides and overlays only. Gameplay code and
Lua bridge are created by the builder. The maintainer's stream begins after a
verified B16 release in the separate LAB; this pack does not claim that release.
Use the coding model recommended in each requested stage. Standard speed is the
default recommendation; these settings are guidance, not an automatic model switch.

## Initial prompt — paste once

Build a visual learning Pokémon agent whose first complete campaign is:
**one human macro goal, Defeat Brock, with autonomous prerequisites and recovery.**
The agent must improve explicit policies from experience and show that improvement
under frozen evaluation. A larger language model or a script that wins once is
insufficient. Use pretrained models selectively for semantic interpretation and
strategy; train our navigation/skill and battle policies from verified outcomes.

Use the target architecture in BROCK_ARCHITECTURE.md and ONE requested prompt from
stream_kit/prompts/brock/. Build final interfaces from the beginning; add supported
capabilities behind them. Do not recreate legacy bedroom-only Q demos, overlapping
planners, starter-only coordinators or manual-per-goal completion as intermediate
production systems. In an existing LAB, preserve old code/data as baselines and evidence.

Alternate supporting implementation with bounded playable gates. R1 runs measured
navigation after B04 through a permanent trusted direct-tool entry, before goals
or a director exist. Unknown events hold. B07a then adds script/dialogue ownership;
B07b adds menus/choices/world interactables/team behind the same interface. B10a
admits the first battle without waiting for inventory; B10b widens that executor.
No early slice claims all future profiles. Do not automatically advance stages.

At the start choose MODE from the user's context:
- LAB means an existing testing project: inventory/reuse first, additive migration,
  adapters and parity checks. Never discard working components or learned history.
- STREAM means a clean starter checkout: create gameplay code from the requested
  target prompt, with isolated writable data/bridge ownership and fresh experience
  unless an explicitly labelled snapshot is imported. Recheck each gate locally.
  For the maintainer's stream use LAB-validated prompt versions. Other builders
  validate their own build; private LAB artifacts are not prerequisites to cloning.

Use Windows/Python>=3.11/.venv, mGBA Lua native captures, Pillow/OpenCV, SQLite,
local stream panels and OBS. Keep machine-specific paths configurable. Game files
are supplied locally; no game RAM/ROM flags as runtime perception. Credentials
stay ignored and never enter prompts, logs, diagrams or reports.

Canonical flow: native capture → perception/UI state → shared world/state →
Director and GoalManager → registered tool executor → bounded motor → native
outcome/evidence → memory and trainable policy. Use one world map, goal lifecycle
and controller owner. Specialized tools handle navigation, cutscenes, menus/party,
NPCs, bag/healing, battle and capture. No arbitrary LLM code or button sequences.

Model proposals are typed bounded data. The application owns available actions,
preconditions, completions and emergency authority. Generate a rolling dependency
graph below the macro; resume interrupted work after supported recovery. Learn
from failure when the observed outcome is valid; distinguish UI/localization faults
from poor tactics. A missing capability stays blocked, never silently skipped.

Native evidence grounds state and completion. Unknown position/HP/PP/identity stays
unknown. Physical source+tile+direction pins a verified map destination ahead of
future story hints; saved spawn is only a candidate. Require two fresh stable full
localized views after crossing/cutscene/invalid pose. No mapping/presses during
scripted motion; settled dialogue uses its owned tool. Names never merge charts.

A* prioritizes measured floor; candidate edges need sensed probes. Commit to a
route, track five measured moves and replan repeated cycles toward the same target.
Known straight strides need calibrated speed/pose, max 2 cells/30 frames, with sensing;
no blind turns, NPCs or portal crossings. Detectors/geometry are versioned profiles,
not a new hardcoded button route for each story objective.

B05 defines enforced train/evaluate/execute modes and goal-conditioned skill learning;
B11 extends outcome-driven learning to combat. Version policies/rewards/features,
retain baselines, and isolate each evaluation episode from training and other eval
knowledge. Record all failures/interventions, real versus replay updates, stage
success, cost and uncertainty. Never call the current learn_routes flag a full freeze.

Show Actions, Goal and transparent Dashboard from the first stage, using the copied
kit's stdlib-only view-only mode before gameplay dependencies exist. Follow
stream_kit/OVERLAY_OPERATIONS.md; controls stay disabled until their tools are ready.
Keep meaningful inputs/decisions/model request+summary/recovery/learning/check events. Frames stay in
RAM; bounded connected map references, last 10 actual model images and 60 feed events.
Max 5 current goal/subgoal cards, fixed attempt summaries. /test-lab owns controls;
viewer and architecture diagram are read-only. No polling noise or frame archive.

Each requested stage ends with a concise change summary, exact checks/observations,
remaining limits and dependency receipt. Promote to STREAM only a stage version
that passed its LAB gate; do not claim future gates or run the next stage implicitly.
Run feasible checks visibly via stream_checks with exclusive feed/bridge ownership.
No implicit restore, deletion, broadcast, commit/push or reuse of historical approval.
Keep initial/index/walkthrough and affected stage prompts updated. Record the
builder's actual receipts locally; never turn the starter's target diagram into
an unsupported claim of implementation or gameplay success.

## Which prompt next

**Fresh clone:** follow STREAM_GUIDE.md, start the overlays, then request B00.
Do not run gameplay package commands before the relevant stage creates them.
Each stage must supply the exact verified command or panel operation for its demo.

**Existing LAB:** inventory/contracts at B00, verify/repair B01–B04, then B07a.
Continue through the same dependency schedule while preserving working components.
Read operator-supplied local context/status if present; current LAB capabilities
and historical run approvals are not contained in this public prompt.

**On stream from scratch:** follow [the playable index](stream_kit/prompts/brock/README.md):
R0 screens, R1 walking, R2 events, R3 interactions, R4 one-goal starter, R5 first
battle, R6 battle learning, R7 healing, R8 travel, optional R9 capture, R10 Brock.
Build the supporting steps listed at each gate, run a useful bounded demonstration,
then continue only when requested. Use LAB-released versions and verify them again
in STREAM; a prompt alone cannot guarantee a working generated implementation.

The starter includes no gameplay implementation or trained experience. Only the
presentation kit runs before B00. Past assisted wins in another workspace cannot
certify this build. Historical LAB construction prompts are not distributed;
the B pack carries forward the technical contracts needed for the final build.
Model recommendation: [GPT-6.1 Sol guidance](stream_kit/prompts/brock/MODEL_GUIDANCE.md).
