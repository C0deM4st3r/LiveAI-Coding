# One AI. Every Pokémon Game. — initial build prompt

Updated 2026-10-14. Start from a **fresh checkout** containing prompts, guides and
overlays only. Gameplay code, native bridge, policies and stores do not exist yet.
Use [STREAM_GUIDE.md](STREAM_GUIDE.md), the [R0–R10 index](stream_kit/prompts/brock/README.md)
and [architecture](BROCK_ARCHITECTURE.md). B00–B16 are component IDs, not numeric
execution order. Every prompt assumes only this starter and completed dependencies.

## Initial prompt — paste once

Build a visual learning Pokémon agent whose first full campaign is one human
macro goal: **Defeat Brock**, with autonomous prerequisites and recovery.
Train explicit navigation/skill and battle policies from verified outcomes and
measure improvements under frozen evaluation. Pretrained models provide selective
semantic interpretation/strategy; bigger models or a script winning once are
not evidence of policy learning.

Create the final interfaces from the beginning, adding supported capabilities
behind them through the requested B-stage/slice. Reuse only components already
built and tested in this project. Do not introduce temporary room-only controllers,
stacked planners or starter-only coordinators that later need replacement.
The earlier completed stages provide each gameplay dependency.

Alternate supporting work with playable gates. B04 provides measured navigation
through a permanent trusted direct-tool entry before goals/director exist.
Unknown events hold; B07a adds script/dialogue ownership, B07b menus/choices/world
interactables/team, and B08 NPC interactions. B10a admits a narrow battle profile;
B10b extends the same executor. A slice never certifies untested future profiles.
Implement only the requested step and do not advance automatically.

Use Windows, Python>=3.11/.venv, mGBA Lua native captures, Pillow/OpenCV, SQLite,
the supplied stream panels and OBS. Make machine paths configurable. The operator
supplies game files locally. Do not use game RAM/ROM state flags as runtime
perception. Credentials stay ignored and out of prompts/logs/reports/screens.

Canonical flow: capture → perception/UI state → shared world/state →
Director/GoalManager → registered tool executor → bounded motor →
native outcome/evidence → memory and trainable policy.
There is one world map, goal lifecycle and controller owner. Specialized tools
handle navigation, cutscenes, menu/party, NPCs, inventory/healing, battle and capture.
Each later stage registers tools in the B00 catalog instead of adding another one.

Model proposals are typed bounded data. Trusted application code owns legal
actions, preconditions, completion rules and emergency authority. Neither model
nor chat content can execute code or independently certify completion.
Plan a rolling dependency graph under the macro; resume interrupted tasks after
supported recovery. Missing capabilities stay blocked. Separate control/perception
failure from tactical failure before assigning rewards.

Native evidence grounds state. Unknown pose/HP/PP/identity stays unknown. Verified
source+tile+direction pins map destination; saved spawn is only a candidate.
Require two fresh stable full localized views after transitions/cutscenes/invalid
pose. No mapping/input during scripted motion; settled dialogue uses its owned
tool. Names alone never merge charts. Persist measured transforms and provenance.

A* prefers measured floor; candidate edges require sensed probes. Commit to routes,
track five measured moves, and replan cycles toward the same target. Smooth
straight movement requires calibrated speed/pose and known cells, at most two
cells/30 frames with sensing. No blind turns, NPCs or portal crossings. Detectors
are versioned game profiles, not a hardcoded button route per story objective.

B05 enforces train/evaluate/execute writes and goal-conditioned skill learning;
B11 adds outcome-trained combat. Version features/rewards/policies, retain
baselines and isolate evaluation episodes from training and each other. Record
failures/interventions, real/replay updates, stage success and uncertainty.
Repeated runs alone do not prove improvement.

Use the supplied Actions, Goal and transparent Dashboard immediately. Follow
stream_kit/OVERLAY_OPERATIONS.md. Viewer mode needs only standard-library Python;
unimplemented operator controls stay disabled. Keep meaningful input/decision/
model request+summary/recovery/learning/check events. Frames stay in RAM, with
bounded map references, ten actual model images and sixty feed events. Show at
most five current goal/subgoal cards and fixed attempt summaries. OBS supplies
native game capture beneath the transparent game column.

Each requested stage ends with exact checks, observed results, remaining limits,
dependency receipts and the real command/panel operation for its demonstration.
Do not suggest gameplay commands before implementing and verifying them.
Label fixture checks, assisted runs and unassisted native results separately.
Use the stage's recommended coding model; it is guidance, not permission to
change account settings or a guarantee of correctness.

Tests needing feed/bridge run after gameplay releases ownership. A stopped run
stays stopped until explicitly resumed. No implicit restore, deletion, broadcast,
commit/push or retry batch. Preserve accumulated code/data/history. Keep this
prompt, index, affected stage and guide current as the build evolves.

## Start the build

Follow STREAM_GUIDE.md setup, start the overlays, then request **B00**.
Continue in R0–R10 order: screens, walking, events, interaction/team, one-goal
starter, first battle, battle learning, healing, travel, optional capture, Brock.
After each gate, demonstrate only supported capabilities before requesting more.

B16 evaluates the player built in this checkout; a diagram or prompt is not its
release evidence. Read [model guidance](stream_kit/prompts/brock/MODEL_GUIDANCE.md)
for coding settings and use one stage prompt at a time.
