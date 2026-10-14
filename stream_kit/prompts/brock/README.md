# Build a little, play a little — the Brock prompt sequence

Updated 2026-10-14. This public starter contains prompts, guides and prepared stream
overlays. **It contains no gameplay agent.** Build that code by following one prompt
at a time. B00–B16 are component IDs; **R0–R10 below is the execution order**.
The [stream guide](../../../STREAM_GUIDE.md) covers setup and each demonstration;
read [LIVE_RESTART_PROMPT](../../../LIVE_RESTART_PROMPT.md) once before implementation.

A playable gate means a capability may run **after its implementation and checks
pass**. A supporting step builds contracts, evidence or learning controls and shows
check receipts instead of claiming new gameplay. The diagrams describe the target;
they do not certify readiness. Start from a fresh checkout and implement each
stage in the order below. Later stages reuse the interfaces, experience and
verified receipts created by earlier stages in your build.

## Playable stream order

| Gate | Build now, in this order | What viewers can see running | Honest stopping boundary |
|---|---|---|---|
| R0 — Screens first | **B00 → B01** | Waiting panels, real check events, native capture and bounded I/O calibration | No autonomous walking; unavailable controls stay disabled |
| R1 — Walk and remember | **B02 → B03 → B04** | A measured route or bounded exploration, map reuse and displayed A* path | Human supplies a grounded target; unknown UI/events hold |
| R2 — Handle the event | **B07a** | Supported Oak motion/dialogue, then fresh localized world handback | Unknown choice/menu/battle holds; no starter acquisition claim |
| R3 — Interact and inspect | **B05 → B06** (support), then **B07b → B08** | Learning comparison, registered interaction, supported choice and native team inspection | Human supplies bounded tool targets/graph; general AI strategy comes next |
| R4 — One goal finds a starter | **B13 → B14** | “Get the first Pokémon” becomes supported subgoals/tools and verified acquisition | Battle remains unavailable until R5 |
| R5 — First battle | **B10a** | First admitted rival battle, legal baseline tactic and verified result/team/world closure | Narrow admitted profile; unknown battle branches hold |
| R6 — Learn battle choices | **B11** | Outcome-driven training plus frozen baseline/candidate comparison | A fixture pass or one win is not measured learning improvement |
| R7 — Recover health | **B09** | Bag inspection, supported items and a known local healing service | Remote service access waits for travel; unknown items/services block |
| R8 — Leave the starter area | **B10b → B15** | Broader battles and cross-map travel; bounded Viridian/parcel/delivery tests | Verify native branches and route legs before long campaigns |
| R9 — Optional new teammate | **B12**, if the strategy needs capture | Supported wild capture with native acquisition evidence | Optional for starter-only Brock; unsupported party/storage states hold |
| R10 — Brock campaign | **B16** | One macro goal, autonomous prerequisites, learning comparison and named Brock proof | All required tool profiles and independent release gates must pass |

B07a/b and B10a/b are slices within the same files and final interfaces. Request
the exact slice; passing B07a does not pass all of B07. B04's trusted direct tool
entry remains available after the general executor/director is built. There is no
temporary room runner or replacement battle controller in this sequence.

When an event blocks a demo, stop safely and keep that run held. Build its missing
tool, run checks with exclusive ownership, then explicitly request supported
resume after fresh UI/pose reconciliation. Do not press blindly while coding,
auto-restore a save or start a second controller.

## Prompt catalog, model and dependencies

All recommendations below are **GPT-6.1 Sol at Standard speed**, for the coding
assistant, not the agent's runtime model. “Extra High” is the app's reasoning
setting. Routine documentation/UI repairs can use High; keep the same acceptance
gate. [Model guidance](MODEL_GUIDANCE.md) explains the tradeoffs.

| Step | Prompt | Recommended effort | Required contracts/slices | Kind |
|---|---|---|---|---|
| B00 | [Foundation](B00_FOUNDATION_CONTRACTS.md) | Extra High | None | Support for R0 |
| B01 | [Native I/O and stream](B01_NATIVE_IO_AND_STREAM.md) | High | B00 | Playable R0 |
| B02 | [Perception](B02_PERCEPTION.md) | Extra High | B00–B01 | Support for movement |
| B03 | [Shared world/recovery](B03_WORLD_AND_RECOVERY.md) | Extra High | B00–B02 | Support and neutral recovery |
| B04 | [Navigation/exploration](B04_NAVIGATION.md) | Extra High | B00–B03 | Playable R1 |
| B05 | [Learning/evaluation](B05_LEARNING_AND_EVALUATION.md) | Extra High | B00–B04 | Learning experiment/support |
| B06 | [Goals/general executor](B06_GOALS_AND_EXECUTOR.md) | Extra High | B00–B05 | Support and composite demo |
| B07a | [Script/dialogue ownership](B07_UI_MENU_PARTY.md) | Extra High | B00–B04 | Playable R2 |
| B07b | [Menus/choices/interactables/team](B07_UI_MENU_PARTY.md) | Extra High | B00–B06 + B07a | Playable R3 |
| B08 | [NPC dialogue/knowledge](B08_NPC_DIALOGUE.md) | High | B00–B06 + B07a/b | Playable R3 |
| B09 | [Inventory/healing](B09_INVENTORY_AND_HEALING.md) | Extra High | B00–B08 | Playable R7 |
| B10a | [First admitted battle](B10_BATTLE_EXECUTION.md) | Extra High | B00–B08 | Playable R5; B09 not required |
| B10b | [Broader early-game battles](B10_BATTLE_EXECUTION.md) | Extra High | B10a + B09 | Playable R8 combat |
| B11 | [Battle learning](B11_BATTLE_LEARNING.md) | Extra High | B05 + B06 + B07b + B10a | Playable R6; widen after B10b |
| B12 | [Optional capture](B12_CAPTURE.md) | High | B09 + B10b + B11 | Playable R9 |
| B13 | [Selective vision/knowledge](B13_VISION_AND_KNOWLEDGE.md) | High | B00–B08 | Support for R4 |
| B14 | [Strategic director](B14_STRATEGIC_DIRECTOR.md) | Extra High | B00–B08 + B13 | Playable R4 |
| B15 | [Travel/story](B15_TRAVEL_AND_STORY.md) | Extra High | B09 + B10b + B14 | Playable R8 travel |
| B16 | [Brock training/release](B16_BROCK_TRAINING_RELEASE.md) | Extra High | All required gates; B12 if capture is used | Playable R10 after admission |

Dependencies are transitive. B13/B14 may start before battle/bag/travel: their tool
catalog must show those capabilities as unavailable. External advice cannot make
an unimplemented action executable. Optional Astra Ultra review at B00/B16 is a
bounded extra review, not a requirement to build this project.

## Start here

Clone the starter and complete [STREAM_GUIDE](../../../STREAM_GUIDE.md) setup.
Set Sol Extra High, Standard, then paste:

```text
Read LIVE_RESTART_PROMPT.md. Implement stage B00.
Apply stream_kit/prompts/brock/B00_FOUNDATION_CONTRACTS.md.
This checkout contains the presentation starter, not gameplay code. Implement the
final interfaces for this stage from scratch, keep the overlays working, and test
this stage only. Publish the exact commands, results, limitations and dependency
receipt for B01. Do not restore, start gameplay or advance automatically.
```

For each later step, replace B00 and the filename with the requested row, supply
only its dependency receipts and relevant files, and name slice `B07a`, `B07b`,
`B10a` or `B10b` explicitly. Ask for the generated command or panel action before
the demonstration; gameplay commands do not exist in this starter.

Between sessions, continue from your recorded receipts and the next unmet gate.
Do not restart the build or discard its maps and learning. A changed executor or
policy needs relevant checks even when an earlier version passed.

## Record each handoff

Record prompt/code/schema/profile/fixture versions, dependency receipts, exact
tests, live run IDs/interventions, admitted tool profiles and the next safe
command. Use `not_started|implemented|offline_passed|live_passed|released` with
evidence, not a checked box alone. B00/B16 implement the manifest; this index
awards no receipts. Keep failures in denominators and report learning separately
from execution success.

Use [OVERLAY_OPERATIONS](../../OVERLAY_OPERATIONS.md) for working presentation
commands, [STREAM_RUNBOOK](../../STREAM_RUNBOOK.md) for live operation and
[BROCK_ARCHITECTURE](../../../BROCK_ARCHITECTURE.md) for the final interfaces.
The source diagram and PNGs are prepared display assets, not runtime telemetry.
