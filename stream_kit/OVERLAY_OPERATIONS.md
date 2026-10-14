# Stream panels: operating contract for the build AI

Updated 2026-10-14. Read this when preparing the stream, extending a stage, or
repairing its presentation. The [runbook](STREAM_RUNBOOK.md) owns the show order;
the [B-pack](prompts/brock/README.md) owns capability gates. This document describes
working commands, not permission to start gameplay, restore a state or broadcast.

## From the first minute, before the gameplay package

The presentation kit now has an explicit **view-only** server. It uses Python's
standard library, needs no pip install, Pillow, OpenCV, pokemon_ai package, model,
SQLite database, Lua bridge or emulator. Missing stores show waiting/unknown/zero,
never an invented map, party, completed goal or gameplay attempt. Test Lab clearly
disables all controls. Its embedded Actions/Goal panels still update normally.

The public starter already includes this presentation subset. When copying it to
a separate clean STREAM workspace, preserve the `stream_kit/` folder name:

```text
stream_kit/__init__.py
stream_kit/serve.py
stream_kit/check.py
stream_kit/telemetry.py
stream_kit/managed_goals.py
stream_kit/queued_goals.py
stream_kit/world_map.py
stream_kit/qwen_gallery.py
stream_kit/actions.html
stream_kit/goal.html
stream_kit/dashboard.html
stream_kit/vision.html
stream_kit/test_lab.html
stream_kit/architecture.html
stream_kit/OVERLAY_OPERATIONS.md
```

The `.png` diagram exports are optional for serving pages, useful as OBS images.
Do not copy another workspace's `runtime/`, `local/`,
learned databases, credentials, saves or legacy gameplay modules merely to launch
the panels. Separately bring the initial prompt and requested stage prompt. This is
a prepared presentation seed; disclose that reuse on stream. Later stages connect
to these same panels rather than creating disposable replacements.

From the STREAM workspace root, with an installed Python on PATH:

```powershell
python .\stream_kit\serve.py --view-only --port 8765
```

The equivalent package command is `python -m stream_kit.serve --view-only`.
With this starter, omitting `--view-only` also selects viewer mode because no
operator module is shipped. Keep the explicit flag for predictable viewer-only
operation after gameplay is added. If Python is not on PATH, use its installed
executable or the Windows Python launcher (`py -3`). For a second viewer:

```powershell
python .\stream_kit\serve.py --view-only --port 8766
```

8766 allows a separate viewer alongside an already-running server on 8765.
Each workspace must have its own stores and future bridge/controller ownership.
A viewer cannot move the game and does not acquire a bridge lease. The default
read sources are its own `stream_kit/runtime/status.json` and
`local/goals/goals.sqlite3`. These are not created by serving a page.

Custom read-only sources are supported only with `--view-only`, for example:

```powershell
python .\stream_kit\serve.py --view-only --port 8766 --status-path .\local\stream-view\status.json --goal-db .\local\stream-view\goals.sqlite3
```

Choose paths inside the intended workspace; missing paths remain missing. The
trusted event publisher and canonical gameplay stores own writes, not the server.
An empty custom source is useful for layout review without displaying LAB history.

## Connect OBS and verify the service

Replace the port consistently when using 8766. These are OBS **Browser Source URLs**:

| URL on `http://127.0.0.1:8765` | Purpose | Size to start with |
|---|---|---|
| `/actions` | Controller, map, max five current goals, newest activity first | 480 x 1080, or wider |
| `/goal` | Independent current goal and outcome | Game-column width x 180 |
| `/dashboard?game=55` | Combined panels and transparent game column | 1920 x 1080; 2560 x 1440 also supported |
| `/test-lab` | Operator surface; view-only until controls are loaded | 1920 x 1080 |
| `/vision` | Optional semantic-observation/check explanation | 1280 x 720 |
| `/architecture?clean=1` | Component diagram | 1920 x 1080 |
| `/architecture?view=roadmap&clean=1` | Build order / playable milestones | 1920 x 1080 |

Use the HTTP URLs for runtime panels; opening their HTML as Local file cannot fetch
the endpoints. Architecture is the exception: it works as Local file without a
server. For a static OBS Image Source use `architecture.png` or `build_order.png`.
Diagram selection changes presentation only, never readiness or runtime state.

Put the native mGBA capture **below** Dashboard in the OBS source stack. The game
column accepts `game=40` through `game=60`; default 55. Keep OBS transparency and
do not add screenshots/placeholders to that region. A normal browser screenshot
may composite transparent pixels onto white or black; that is not a game frame.
The ten bounded model-source thumbnails belong in the action feed.

Health check, without loading gameplay:

```powershell
Invoke-RestMethod http://127.0.0.1:8765/health
Invoke-RestMethod http://127.0.0.1:8765/status
```

`/health` identifies `service: pokemon-stream-kit`, server `instance_id` and PID,
`mode: view-only|operator`, controls availability, and whether its data files exist.
It verifies the presentation service only, not mGBA connectivity or model quality.
Missing files plus waiting panels are the expected fresh-start state. Viewer GETs
are read-only; they do not migrate/initialize databases or goal lifecycle.

`?demo=1` on Actions, Goal or Dashboard displays explicitly labelled sample events
without writing history or touching the game. Remove it for real telemetry.
Refresh the OBS browser source after HTML/JS changes. A Python/server change needs
an owned server restart; an old running process cannot pick it up automatically.

## Once the operator runtime exists

The starter contains no `test_lab.py` gameplay runner, `pokemon_ai` package, Lua
bridge or executable game objective. The supplied Test Lab page is presentation:
its inputs remain disabled until a trusted local operator adapter is implemented
and tested in the appropriate build stage. An editable-looking field is not a tool.

The server retains an optional adapter boundary for later stages: an adjacent
`test_lab.py` may provide `LabRunner`, `catalog` and `compile_command`. The runner
owns its token, state, start/stop, preview, queue and bounded continuation methods;
the server transports validated requests, not arbitrary commands. Build only the
capabilities authorized by the current stage and keep one controller owner.
There is no need to implement all controls simply to launch the stream panels.

When that trusted module exists, a launch without `--view-only` selects operator
mode. An installed but broken dependency fails with guidance rather than silently
switching controllers. Startup itself must never start gameplay. Custom data paths
remain rejected without `--view-only`, so an operator cannot display one store
while controlling another. Every new tool needs capability/precondition and native
completion checks before the panel advertises it. Do not copy a workflow catalog
from a more advanced workspace into a build that cannot execute those workflows.

The operator POST routes require bounded JSON, exact local host/origin and the
per-server console token. Never put that token in documentation or reuse it across
servers. The viewer-only server rejects all control POSTs even if a token is sent.
Do not add shell commands, model code, credentials or writable DB selectors to a UI.

## Keep it running without taking control of unrelated work

1. Read `/health` first. If a matching server is healthy, reuse it. A 404 on `/health`
   may mean the pre-upgrade server; inspect its known launch/owner before restarting.
2. In operator mode read `/test-lab/status`. An owned job marked `running` or
   `stopping`, or non-null `external_busy`, means do not restart or start a second
   controller. Stop only a specifically authorized owned run through its controls.
3. To restart an idle foreground server you started, use Ctrl+C in its terminal,
   then rerun its exact command. For an AI-launched background server use
   `Start-Process -WindowStyle Hidden`, retain the owned command/instance/PID, and
   verify the process identity before stopping it. Windows venv launchers can have
   a different PID from `/health`; never guess by process name or kill all Python.
4. After restart check `/health`, refresh the OBS source, and check waiting/live
   status. Keep original data; do not “repair” a display by deleting DBs/history.
5. If only the feed is stale, inspect its publisher/run state and data path. The
   UI's no-recent-events warning does not prove the agent is dead; model calls can
   take time. No timestamp heartbeat should flood the action feed.

When the presentation fails, controls must continue to obey their independent
ownership, bounds and release rules. Restoring the panel must not restore keys or
silently resume a stopped run. No background auto-relaunch of gameplay is provided.

## Publishing from the first implementation stage

Use `stream_kit.telemetry.Publisher` from trusted Python application/check code.
It is standard-library only and accepts a custom status path. Its atomic snapshot
writes are presentation output; they grant no gameplay authority. Keep one active
publisher per status file. Connect each future stage's event adapter to this
publisher and manage actual model-image attribution through the same event flow.

```python
from datetime import datetime, timezone
from stream_kit.telemetry import Publisher

feed = Publisher(keep_feed=True)
feed.publish({
    "event": "activity",
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "kind": "system",
    "title": "Stream panels connected",
    "summary": "Setup only; no gameplay has started",
    "source": "SETUP - presentation check",
}, "B01-setup")
```

Only emit that setup event after actually checking the panels. It is not a test
PASS or goal completion. Retain the same publisher for a run and a new run identity
for a new run. `keep_feed=True` preserves bounded history, not old pressed keys.

| Event / store | Meaning and rule |
|---|---|
| `run_started`, `run_stopped` | Actual run boundaries; not UI page loading. Use `count_attempt=False` when no gameplay attempt starts. |
| `decision`, `action_started`, feedback | Bounded selected/sent input and measured outcome; feedback updates its own action row. |
| `activity` | Changed plan, recovery, learning, model request/reply or real setup activity; concise title and one-line summary. |
| `checkpoint`, `attempt_started/finished` | Real checks/attempts, labelled mock/recorded/native. PASS/FAIL/INTERRUPTED remain distinct from objective success. |
| Canonical `gm/hy/gq` stores | Managed goals, current root/subgoals and queue; renderer never creates/completes them. |
| Canonical `wm_*` store | Actual measured world, pose, route and candidates; unknown position stays unknown. |
| `QwenGallery` / stage event adapter | Last 10 actual source images linked by call ID to request/reply. Cached replies create no new image. |

Keep the latest 60 meaningful feed events with source/timestamp. Do not emit polling,
unchanged stability, repeated premapping counts or artificial button activity.
Goal cards use a shared current-session projection, capped at five; compact retries
for display while retaining raw history. Do not use legacy `goals_updated` to fake
the eight-state GoalManager lifecycle or bypass its trusted completion verifiers.

## Verified baseline and maintenance checks

On 2026-10-14 a copied kit ran under Python with site packages and environment
overrides disabled, without `pokemon_ai` or `test_lab.py`. All six HTML panels and
empty read endpoints worked; all six control POSTs rejected with 503. Viewer reads
created no local/runtime directory or database. Malformed status JSON fell back
to waiting without modifying the source. Non-object retained snapshots also leave
the publisher ready before server startup, without rewriting that source. Maintainer
regression checks additionally cover attribution, retention and data projections.
Those private LAB tests are not part of the public gameplay-free starter.

All six panel scripts compiled. Empty Actions, Goal, Dashboard, Test Lab and Vision
were rendered and reviewed; a narrow Actions controller clipping issue was fixed
so A/B remain visible. Architecture is reviewed separately with its current diagram.
These checks establish presentation/bootstrap behavior, not gameplay success.

The public presentation smoke check needs only Python and uses a temporary data
directory plus an ephemeral loopback port. It does not publish to the active feed,
import a gameplay controller or send emulator input:

```powershell
python .\stream_kit\check.py
```

`python -m stream_kit.check` is equivalent. A successful result verifies page
delivery, empty data projections, rejected control requests, temporary fixture
events and private-file isolation. It does not verify browser layout, OBS capture
or gameplay. Also inspect the actual Browser Sources and their transparent column.
Once a stage has a visible check publisher, run its checks with exclusive feed and
bridge ownership. Do not import another project's gameplay solely to run its
historical test harness. Keep this guide and runnable commands current.
