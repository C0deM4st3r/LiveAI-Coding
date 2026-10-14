# Stream runbook — the operator's short checklist

Updated 2026-10-14. For the full beginner walkthrough use
[STREAM_GUIDE](../STREAM_GUIDE.md). For the next prompt/model/dependency use the
[R0–R10 index](prompts/brock/README.md). B numbers identify components, not order.
This public repository supplies presentation and instructions; gameplay code is
built during the project. The maintainer's stream starts after a separate LAB
passes the Brock release gate; that result is currently pending.

## Before going live

1. Select one LAB-validated prompt version and its dependency receipts. Set the
   recommended coding model in the index. Do not read the entire prompt pack into
   every coding request.
2. Open the separate STREAM checkout, its own runtime data and the selected game
   instance. Never share a writable database, bridge mailbox or controller with LAB.
3. Start the provided display server from the repository root:

   ```powershell
   python .\stream_kit\serve.py --view-only --port 8765
   ```

   If 8765 already belongs to another project, use 8766 and change all URLs
   consistently. Do not terminate an unknown listener. Use the installed Python
   executable if `python` is unavailable.
4. Run `python .\stream_kit\check.py` and check
   `http://127.0.0.1:8765/health`. View-only/waiting is correct before runtime
   code and data exist. Configure OBS using [OVERLAY_OPERATIONS](OVERLAY_OPERATIONS.md).
5. Use `/dashboard?game=55` at 1920×1080 above the native mGBA capture. Keep the
   game column transparent. Keep `/test-lab` on the operator's screen; its controls
   remain disabled until implemented and admitted. Check stream-size readability.
6. Show `/architecture?view=roadmap&clean=1` or [build_order.png](build_order.png).
   State today's stage, working capabilities and honest stop boundary. Prepared
   overlays are reused; the gameplay implementation is being built on stream.

Starting a server is not starting a broadcast or a game run. Full operator startup
must come from the implementation's verified instructions; this starter provides
no gameplay launch command.

## Build, demonstrate, pause

| Gate | Build | Demonstration cue |
|---|---|---|
| R0 | B00 → B01 | “The screen tells us what the player actually observed and did.” |
| R1 | B02 → B03 → B04 | “It remembers measured floor and follows a route.” |
| R2 | B07a | “It waits during scripted motion, then finds itself again.” |
| R3 | B05 → B06 → B07b → B08 | “Tools own interactions; native evidence closes the task.” |
| R4 | B13 → B14 | “One objective becomes supported, verifiable smaller jobs.” |
| R5 | B10a | “The first battle uses legal actions and a verified result.” |
| R6 | B11 | “We compare learned decisions with the same frozen baseline.” |
| R7 | B09 | “Low health interrupts the objective and recovery is checked.” |
| R8 | B10b → B15 | “Travel survives battles and map changes without losing the goal.” |
| R9 | B12 if needed | “A capture is complete when the new Pokémon is verified.” |
| R10 | B16 | “One Brock objective is judged by independent complete runs.” |

For **every component/slice**, not just each R gate:

1. Paste the restart prompt once, then request one stage with mode, exact prompt
   file and dependency receipts. Choose the model listed in the index and use
   Standard speed. The full walkthrough supplies a reusable request template.
2. Let the coding agent implement and run focused checks. Gameplay must first
   release controller/feed ownership. Label mock, recorded and live checks.
3. Read the result and its limits. A schema test is not a live navigation win;
   policy updates alone are not improvement.
4. At a playable gate, request the exact implemented command/panel operation,
   starting context, bounded budget and stop behavior. Explicitly authorize that
   demonstration. A named restore is permission for the requested run only.
5. Observe input, path, model request/reply, recovery, learning and checks in the
   feed. Show the latest native result. Keep five current goal/subgoal cards and
   fixed attempt summaries; do not flood the display with polling.
6. Save the receipt: versions, checks, runs, interventions, remaining gaps and
   next safe action. Continue only when requested.

A held run stays held while its missing handler is built. Run offline checks with
exclusive ownership, then explicitly request resume. Resume must reconcile fresh
native UI, pose and lease before input. A restore or new batch is a separate choice.
Unknown battle/menu/dialogue must never turn into improvised presses.

## Display maintenance while coding

Use `/actions` and `/goal` independently or the combined dashboard. Architecture
views are `/architecture?view=parts&clean=1` and
`/architecture?view=roadmap&stage=B07a&clean=1`; stage selection is presentation
only. HTML works as an OBS Local file only for Architecture; runtime panels use
HTTP. [architecture.png](architecture.png) and [build_order.png](build_order.png)
are alternatives for static scenes.

Refresh the OBS source after HTML/JS edits. Python server changes need an orderly
restart of the owned idle process. Reuse a healthy matching server, never kill
all Python processes, and never restart an active operator controller to fix the
display. Read `/health` and the guide's ownership checks first. Keep data intact;
a missing feed is not permission to delete memory or replay a run.

Keep maps, proof and learning distinct in narration: maps retain measured spatial
experience; B05/B11 update explicit policies; A* and native control guards are
algorithms; runtime language models supply hypotheses/plans. B16 measures whether
the assembled agent improves and completes the declared Brock campaign reliably.
