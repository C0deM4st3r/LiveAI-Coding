# Build the Pokémon agent on stream, step by step

This is a public **starter and build guide**, not a downloadable Pokémon-playing
bot. The repository provides prompts, stream overlays and diagrams. You write
the gameplay code with the coding assistant, demonstrate one useful capability,
then extend the same architecture. The first complete campaign is one objective:
**Defeat Brock**, with prerequisites, recovery and learning handled by the agent.
See [STARTER_CONTENTS](STARTER_CONTENTS.md) for exactly what is included.

The maintainer is validating this architecture in a separate LAB before starting
the stream. **Full Brock readiness is still pending.** The planned stream starts
only after LAB meets B16's declared independent release gate. An assisted win is
not that gate. Distinguish an available prompt from a validated capability.

## 1. Prepare a clean workspace

Install Git, a code editor, Python 3.11 or newer, mGBA and OBS. Supply your own game
locally; the starter does not include a ROM, save, learned policy, map or API key.
Build the FireRed profile first; other versions require their own tested adapters.
The architecture is reusable, but native UI readers are not automatically portable.

Copy this repository's clone URL from its hosting page. In PowerShell, replace
`<repository-url>` before running:

```powershell
git clone <repository-url> pokemon-ai-stream
Set-Location pokemon-ai-stream
git switch -c my-stream-build
python --version
python -m venv .venv
```

Open this folder in your editor. If `python` is not found, use your installed
Python executable's full path. A quoted executable path in PowerShell needs `&`
before it. Do not copy another person's machine-specific path.

Use `.\.venv\Scripts\python.exe` for this build's Python commands. The overlays
need only the standard library. Each later stage must add and document its actual
dependencies; there is no gameplay package to install yet. SQLite comes with
Python and needs no separate server. Create your own commits as you build; review
`git status` so keys, runtime data and game files remain local.

Keep LAB and STREAM in different directories with separate writable data, bridge
mailboxes and checkpoints. B00 implements ownership enforcement. Until then, do
not run two controllers against the same emulator.

## 2. Put the prepared displays on OBS

Run the starter's isolated presentation checks:

```powershell
.\.venv\Scripts\python.exe .\stream_kit\check.py
```

These check the overlay server and fixture events, not gameplay. Then leave this
server running in its terminal:

```powershell
.\.venv\Scripts\python.exe .\stream_kit\serve.py --view-only --port 8765
```

If another project owns 8765, use 8766 consistently; do not terminate an unknown
listener. In a second terminal inspect the service:

```powershell
Invoke-RestMethod http://127.0.0.1:8765/health
Invoke-RestMethod http://127.0.0.1:8765/status
```

The expected first state is view-only, disabled controls and waiting data. It
checks presentation, not emulator connectivity, and invents no goals or maps.

In OBS, create a 1920×1080 scene with:

1. A native mGBA capture for the game.
2. A Browser Source **above it** using
   `http://127.0.0.1:8765/dashboard?game=55`, width 1920, height 1080.
3. The game positioned behind the transparent column. `game=40` through `game=60`
   selects its width. The dashboard supplies no game screenshot in that space.

Create an explanation scene using
`http://127.0.0.1:8765/architecture?view=roadmap&clean=1`, or add
`stream_kit/build_order.png` as an Image Source. `/actions` and `/goal` support
separate layouts. Open `/test-lab` in your browser; controls stay disabled until
their runtime is implemented. Check readability at actual stream resolution.

[OVERLAY_OPERATIONS](stream_kit/OVERLAY_OPERATIONS.md) has all endpoints, event
contracts and maintenance instructions. Disclose the prepared overlay seed: the
gameplay code is built from scratch. Starting panels does not start a broadcast,
emulator script or game run.

## 3. Request one implementation step

Read [LIVE_RESTART_PROMPT](LIVE_RESTART_PROMPT.md) and the
[prompt/dependency index](stream_kit/prompts/brock/README.md). B00–B16 identify
parts; follow **R0–R10**, not numeric order. Give the coding AI access to this
checkout and only the current step's relevant context.

Use **GPT-6.1 Sol, Standard speed**. Every prompt names its recommended effort:
High for B01/B08/B12/B13; Extra High for the other components and a/b slices.
This is the coding assistant, not the runtime vision/planning model. See
[MODEL_GUIDANCE](stream_kit/prompts/brock/MODEL_GUIDANCE.md) for usage tradeoffs.

For B00, set Extra High and paste:

```text
Read LIVE_RESTART_PROMPT.md. Mode STREAM, stage B00.
Apply stream_kit/prompts/brock/B00_FOUNDATION_CONTRACTS.md.
This is the public starter: build the gameplay interfaces from scratch.
Keep the prepared overlays working. Implement and test this stage only.
Give me the exact check command, result, limitations and dependency receipt for B01.
Do not restore, start gameplay, broadcast or advance automatically.
```

For each later component, replace all angle-bracket fields in this template:

```text
Mode STREAM. Implement only <B ID and slice, if any> from <exact prompt path>.
Use LIVE_RESTART_PROMPT.md and these dependency receipts: <relevant receipts>.
Reuse our existing final interfaces. Keep overlays working and publish actual
checks through the feed when that integration exists. Stop after this stage.
Provide the implemented check command and, if this reaches a playable gate, the
exact bounded command/panel operation, preconditions and evidence for its demo.
No implicit run, restore, retry batch or next milestone.
```

The index links every exact file. Name `B07a`, `B07b`, `B10a` or `B10b` explicitly.
The implementation produces its actual CLI/panel operation; **do not invent future
gameplay commands**. Until code and checks exist, that control stays unavailable.

## 4. Build, demonstrate, extend

Request each component separately. After checks pass, explicitly start a bounded
demo using the generated command. Supply a grounded target/current context or a
named start state for that specific run. If position is unknown, recover first.
The table below is a schedule, not automatic authorization to restore or run.

All model settings below are Sol at Standard speed:

| Gate | Requests and effort, in order | Narration cue | Observable gate |
|---|---|---|---|
| **R0: screens and input** | B00 Extra High → B01 High | “Every action has one owner and an observable result.” | Contract/path/ownership checks, native capture, bounded calibration and released keys. No autonomous walking yet. |
| **R1: walk and remember** | B02 → B03 → B04, all Extra High | “It remembers measured floor and follows a route.” | Stable localization, existing-map recovery and bounded A* route/frontier demo. Unknown events hold; losing pose does not create a duplicate map. |
| **R2: first event** | B07a Extra High | “It waits while the game takes control, then finds itself again.” | No presses/mapping during scripted motion; supported settled dialogue advances; two fresh localized views restore navigation. |
| **R3: interaction and team** | B05 Extra High → B06 Extra High → B07b Extra High → B08 High | “Tools own interactions; native evidence closes the task.” | Enforced training/evaluation writes, general executor, supported choice, native team snapshot and complete NPC conversation. Human still supplies bounded targets. |
| **R4: one goal, first Pokémon** | B13 High → B14 Extra High | “One objective becomes smaller jobs the player can perform.” | One macro becomes typed supported subgoals and fresh native starter proof. No recipe-only dispatch, manual steering or model-claimed success. |
| **R5: first rival battle** | B10a Extra High | “A legal baseline fights, then checks what happened.” | Admitted battle profile, native legal actions/PP, result, updated team and world handback. Unsupported branches hold. |
| **R6: learn battle decisions** | B11 Extra High | “We test whether experience improves decisions.” | Eligible outcomes update a versioned policy; frozen baseline/candidate comparison retains failures and reports uncertainty. One win is insufficient. |
| **R7: inventory and health** | B09 Extra High | “Recovery interrupts the goal, then returns to it.” | Native bag/item evidence, supported local healing, fresh team recovery and resumption. Unknown items/services remain blocked. |
| **R8: travel and broader battles** | B10b Extra High → B15 Extra High | “The goal survives maps, fights and interruptions.” | Tested wild/multi-opponent branches, portal continuity and bounded Viridian/parcel/delivery legs with item/story receipts. |
| **R9: optional capture** | B12 High, if needed | “A new teammate needs native acquisition evidence.” | Supported legal capture and verified species/possession. Full-party/storage branches require their own reader coverage. |
| **R10: autonomous Brock** | B16 Extra High | “One objective; independent complete runs judge it.” | Required tools admitted, scoped Brock result plus closure, declared independent evaluation, policy change and release manifest. |

B07a/b share **B07_UI_MENU_PARTY.md**; B10a/b share **B10_BATTLE_EXECUTION.md**.
They extend the same final modules. B10a supports a narrow profile before bag
support; wider B10b requires B09. B12 is optional when the declared strategy needs
no capture. R4's director cannot call future tools just because a model knows
their names.

B05/B06 are supporting work: they prevent ambiguous training modes, competing
controllers and invented completion. Show their real check receipts. A* and native
guards remain trusted algorithms; B05/B11 train explicit policies. Models provide
hypotheses/plans rather than independently certifying successful gameplay.

## 5. Record the result and resume safely

Ask for a compact receipt in the build's manifest format after every step:

```text
Step/slice; prompt/code/schema/profile versions; dependency receipts:
State: implemented | offline_passed | live_passed | released
Exact checks/results, labelled mock / recorded / native:
Native run IDs, start context, admitted tools and completion evidence:
Interventions, failures, remaining limits:
Policy versions, real/replay updates, evaluation isolation:
Exact next safe command or panel operation:
```

Claim only the strongest established state; `released` requires the declared
review/approval. Keep assisted and failed attempts. A learned map, more policy
updates and better evaluated decisions are different results.

Gameplay releases its feed/bridge before checks need them. If a run holds on an
unsupported event, keep it held, build/test the handler, then explicitly request
resume. Resume must reconcile fresh UI/pose and single ownership before input.
A restore or new batch is a separate operator choice, never an automatic repair.

For display faults, follow [OVERLAY_OPERATIONS](stream_kit/OVERLAY_OPERATIONS.md).
Refresh after HTML edits; restart only an owned idle server after Python changes.
Keep learned data and game position. Do not restart gameplay to repair a panel.

## 6. Finish LAB, then start this stream

In an existing testing workspace use **Mode LAB** and the same R sequence:
inventory/adapt B00; verify B01–B04 and B07a; then missing B05/B06, B07b/B08,
B13/B14, B10a/B11, B09/B10b/B15, optional B12 and B16. Retain working baselines,
maps, policies and failure evidence until a validated cutover exists.

B16's native campaign/evaluation report decides Brock readiness. Prompt completion,
an assisted starter or a battle fixture does not. Record supported starts, native
verifier coverage, policy/map seeding, evidence, limitations and rollback version.
Preserve the exact prompt versions that produced the validated implementation.

Then build those proven slices in a separate STREAM checkout of this starter.
The gameplay code is written there on stream; do not silently copy the LAB bot.
Explicitly label any later import of trained experience. Recheck each generated
slice: the same prompt does not guarantee the same code. Start broadcasting only
when you choose to do so.

Keep [STREAM_RUNBOOK](stream_kit/STREAM_RUNBOOK.md) open for the short on-air
checklist. Use [BROCK_ARCHITECTURE](BROCK_ARCHITECTURE.md) and the diagrams for
explanation. Update the affected prompt and guide when LAB evidence changes the
final build.
