# One AI. Every Pokémon Game.

A public **build-it-yourself starter** for a visual learning Pokémon agent.
The first campaign target is one human objective: **Defeat Brock**, with the
agent choosing its prerequisites and learning from verified outcomes.

This checkout contains prompts, stream overlays, diagrams and guides. You write
the gameplay code while following the checkpoints. It contains no working bot,
Lua bridge, trained policies, game assets, saves or API keys. The overlays are
the only supplied application code and run immediately.

## Start here

1. Follow [STREAM_GUIDE.md](STREAM_GUIDE.md), the step-by-step walkthrough: setup,
   what to paste, what to demonstrate and when to stop at every playable gate.
2. Give your coding assistant [LIVE_RESTART_PROMPT.md](LIVE_RESTART_PROMPT.md) once,
   then **one** stage/slice from the [prompt index](stream_kit/prompts/brock/README.md).
3. Use the coding model recommended at the top of that stage. These are starting
   settings, not guarantees. See [model guidance](stream_kit/prompts/brock/MODEL_GUIDANCE.md).
4. Build, check and demonstrate that stage before requesting the next. Each
   implementation must report its actual runnable command or panel operation.

Use Python 3.11 or newer for the supplied display kit. The gameplay build targets
Python, mGBA with Lua, SQLite, Pillow/OpenCV and OBS; later stages add selective
model providers. Supply game files locally. No model account, gameplay package
or emulator is needed to start the overlays.

```powershell
python .\stream_kit\serve.py --view-only
```

Open <http://127.0.0.1:8765/dashboard?game=55>. Put native mGBA capture beneath
that Browser Source in OBS; the game column is transparent. Also available:
`/actions`, `/goal`, `/test-lab`, `/vision` and `/architecture`. Test Lab controls
stay disabled until you implement and connect the trusted operator backend.

Check the supplied presentation without moving a game:

```powershell
python .\stream_kit\check.py
```

Read [overlay operations](stream_kit/OVERLAY_OPERATIONS.md) for sizes, ports,
event integration, empty states and server maintenance.

## Build a little, play a little

| Gate | Build steps | Observable result after the gate passes |
|---|---|---|
| R0 | B00 → B01 | Screens, checks and bounded native I/O |
| R1 | B02 → B03 → B04 | Measured maps, recovery, A* routes and exploration |
| R2 | B07a | Scripted motion/dialogue, then map recovery |
| R3 | B05 → B06, then B07b → B08 | Learning modes, execution, interactions and team inspection |
| R4 | B13 → B14 | One first-Pokémon goal decomposed into available tools |
| R5 | B10a | First admitted rival battle and verified closure |
| R6 | B11 | Battle learning compared with a frozen baseline |
| R7 | B09 | Inventory, supported items and local healing |
| R8 | B10b → B15 | Wider battles and travel/story objectives |
| R9 | B12, if needed | Optional capture with native acquisition proof |
| R10 | B16 | Independent Brock campaign evaluation and release |

B numbers identify components; R numbers define the schedule. B07a/b and B10a/b
widen the same permanent tools. Supporting stages enable the next demo; a prompt
or passing schema test does not establish gameplay success.

## What learns

The agent records measured world knowledge and trains explicit navigation/skill
and battle policies from outcomes. A* and legal-action guards remain deterministic.
Pretrained models propose bounded interpretations/plans; they cannot execute
arbitrary code or certify success. Frozen comparisons measure whether policy
changes help, retaining failures and interventions.

See [the architecture](BROCK_ARCHITECTURE.md) and the OBS-ready
[playable diagram](stream_kit/build_order.png). Diagrams show the target design,
not live completion status.

## Your build and its release

Start from a fresh checkout and build through the guides. Every prompt assumes
only the supplied overlays and the earlier stages you have completed here.
Create each gameplay component as its step requests it. Verify each gate in your
workspace; B16 evaluates the player you have built.

Create your own branch before building. Source you write can be committed in
your fork; runtime data and secrets stay ignored. See
[STARTER_CONTENTS.md](STARTER_CONTENTS.md) for the public boundary and
[STREAM_GUIDE.md](STREAM_GUIDE.md) for session handoffs and release checks.
