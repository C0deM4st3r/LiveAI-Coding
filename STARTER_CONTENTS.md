# Public starter contents

This repository is the guide and presentation seed for building the player.
Its initial commit contains only this maintained material:

| Path | Purpose |
|---|---|
| `.gitignore` | Ignore secrets, environments, captures and learned runtime data |
| `README.md`, `AGENTS.md`, `STARTER_CONTENTS.md` | Entry point, assistant rules and this boundary |
| `LIVE_RESTART_PROMPT.md` | Compact initial context and one-stage workflow |
| `STREAM_GUIDE.md` | Preparation/build/demo/session walkthrough |
| `BROCK_ARCHITECTURE.md` | Target architecture and learning/evidence contracts |
| `stream_kit/prompts/README.md` | Active prompt entry point |
| `stream_kit/prompts/brock/*.md` | B00–B16, dependencies and model recommendations |
| `stream_kit/STREAM_RUNBOOK.md`, `stream_kit/OVERLAY_OPERATIONS.md` | Stream operation |
| `stream_kit/*.html` | Actions, Goal, Dashboard, Vision, Test Lab and architecture |
| `stream_kit/architecture.png`, `stream_kit/build_order.png` | OBS diagram exports |
| `stream_kit/__init__.py`, `serve.py`, `telemetry.py` | Presentation server and event projection |
| `stream_kit/managed_goals.py`, `queued_goals.py`, `world_map.py`, `qwen_gallery.py` | Display projections and bounded gallery support |
| `stream_kit/check.py` | Isolated presentation smoke check; no emulator input |

All Python filenames above are under `stream_kit/`. There is no gameplay
`src/`, `scripts/`, Lua bridge, controller backend, gameplay test suite,
packaged gameplay dependencies, native game assets, historical rehearsal
transcript, save, ROM, policy or database. Test Lab HTML is supplied; its
gameplay backend is built in the checkpoints.

## For builders

Clone into a new folder and create your own branch before writing the player.
The public `.gitignore` permits source/tests you create; commit those in your
own project. Runtime stores and secrets remain excluded. Keep recorded fixtures
deliberate, minimal and documented.

Display projections define integration contracts, not a prebuilt game agent.
B00/B01 create the typed event adapter. A displayed goal is not automatically
executable or verified.

## Maintaining the starter

Keep the maintained starter limited to the presentation and documents above.
Builders add their own gameplay implementation in their working branch or fork.
Review `git diff --cached --name-only` before publishing. Exclude runtime data,
credentials and game files. Do not force-add ignored secrets or saves.

Each guide begins with the supplied files and its named preceding stages.
Back up your implementation and experience as you
progress. A local commit does not publish anything or change repository visibility.
