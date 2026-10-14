# Instructions for the build assistant

## Scope and reading order

This public starter contains prompts, guides, diagrams and presentation code.
Do not assume gameplay code, Lua bridge, assets, policies, stores or completed
checkpoints exist in a fresh clone. Every prompt assumes this clean starting
point, then builds on the stages completed in this same project. The earlier
completed stages supply each gameplay dependency.

Read LIVE_RESTART_PROMPT.md, STREAM_GUIDE.md and only the requested B prompt.
The prompt index defines R0–R10 order; B00–B16 are component IDs, with B07a/b and
B10a/b slices. Follow dependencies, not numeric order. Model recommendations are
guidance; do not change account/model settings implicitly.

Implement final interfaces incrementally. Direct navigation remains a permanent
trusted tool; later events, menus, battles and strategy widen those interfaces.
Implement only the requested stage. Do not advance, run gameplay, restore,
broadcast, commit or push implicitly. An explicit batch authorizes only its
named starts/count/scope. Stopped runs remain stopped unless requested.

## Architecture and evidence

- One shared world memory, goal lifecycle, trusted tool/completion catalog and
  emulator owner. Model/chat content is bounded data, never executable code,
  raw button sequences, authority or independent completion evidence.
- Native screenshots ground state. Unknown pose/HP/PP/identity stays unknown.
  Model labels and game knowledge are hypotheses, not runtime RAM/ROM flags.
- Seen/candidate tiles are not measured walkability. Persist capture provenance,
  grid transforms, fractional odometry, anchors and directed passages. Names only
  narrow candidates; chart merging requires measured overlap/transform proof.
- Known source+tile+direction pins a verified destination; saved spawn is a
  candidate. Require two fresh stable full localized views after transitions,
  cutscenes or invalid pose. Never invent reverse passages or walked cells.
- A* intent takes priority while fresh guards permit. Track five measured moves,
  detect cycles and replan the same target with temporary exclusions. Unknown
  edges need sensed probes. Smooth strides require calibrated pose/speed and
  straight known cells, max two cells/30 frames, no blind turns/NPCs/portals.
- Release keys and suspend mapping during scripted motion. Supported settled
  dialogue uses its owned tool; unknown UI holds. Resume after fresh recovery.
- Generic textboxes, scene changes or model claims cannot prove named NPC,
  starter, item, battle or Brock completion. Use scoped fresh native registered
  evidence. Conversations require closure; battle result and post-battle
  team/UI/world closure are separate.
- SQLite suffices initially. Use transactional versioned migrations; preserve
  experience, failures, proofs and policy lineage. Do not add parallel maps.
- Train/evaluate/execute modes enforce writes. Frozen evaluation isolates policy
  and knowledge across episodes/conditions. Retain failures/interventions; more
  memory rows or one repaired win do not demonstrate learning.
- Selective model calls use bounded versioned structured output. Pending semantic
  vision holds input until reply/error, without movement timeout fallback.
  Secrets never enter prompts, logs, reports or stream screens.

## Presentation and checks

Read stream_kit/OVERLAY_OPERATIONS.md before changing or starting panels. The
stdlib viewer must work before gameplay exists. Missing stores show waiting,
not invented progress. Viewer GETs create no stores/lifecycle transitions.
Operator endpoints remain disabled until trusted backend, capability validation
and single-owner controls exist.

Keep /actions and /goal independent. /dashboard combines them with a transparent
40–60% game column, fixed history/attempt cards and max five current major/subgoal/
emergency cards. OBS supplies native capture. Feed meaningful input, decisions,
model request/reply, learning/recovery and checks; omit polling noise. Retain
60 events and ten actual model source images with linked IDs; caches create no
captures. Movement updates its own row. Frames stay in RAM with bounded diagnostic
references, not per-frame archives.

Use English narration and one observable gate per checkpoint. Run feasible checks
visibly after gameplay releases the feed/bridge. Initially use the supplied
overlay smoke check, then the runner built in B00/B01. Label mocks, fixtures,
native observations and inference honestly. Do not weaken proof rules for tests.

Maintain affected prompts, index, walkthrough and operations when contracts change.
Keep planned, implemented, fixture-tested and live-verified states distinct.
Diagrams are presentation, not release evidence. Preserve accumulated data until explicit
cleanup authorization.

For the maintained public starter, keep Git within STARTER_CONTENTS.md. Gameplay
implementation belongs to the builder's project/branch. Back up source and learned
data as the build progresses. B16 evaluates and qualifies this implementation;
never infer a release from the prompt pack itself.
