# Coding model and usage budget for the stream build

Checked 2026-10-14 against official OpenAI documentation. This document selects
the coding assistant, not the runtime game's vision/planning provider. Access,
limits and available controls vary by account/client; no subscription is required
by the architecture itself. Recheck the official links before budgeting a later build.

## Recommended working settings

| Setting | Use in this project |
|---|---|
| GPT-6.1 Sol High, Standard speed | Default: bounded implementation, tests, overlays, documentation and routine repairs |
| GPT-6.1 Sol Extra High, Standard speed | Map recovery, learning/evaluation, executor ownership, battle learning and director integration |
| GPT-6 Astra Ultra, Standard speed | Occasional difficult architecture review or independent investigations that benefit from parallel agents |

OpenAI recommends Sol for complex coding when available. The allocation above is
an engineering recommendation, not a measured equivalence to Astra on this project.
High and Extra High have no fixed published task-cost multiplier. Extra reasoning
can consume more tokens/time, and an inadequate lower setting can waste usage on
repairs. Ultra delegates work to subagents; it is distinct from the Ultrafast speed
setting. Keep one owner for shared interfaces and avoid duplicate agent reviews.
[Models](https://learn.chatgpt.com/docs/models),
[subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).

## Recommendation on every build step

All entries use **GPT-6.1 Sol at Standard speed**. B IDs identify components;
follow the [R0–R10 playable order](README.md), not numerical B order.

| Component or slice | Effort | Reason |
|---|---|---|
| B00 contracts/profiles | Extra High | Ownership, schema and persistence boundaries |
| B01 native I/O/overlays | High | Bounded protocol and presentation integration |
| B02 perception | Extra High | Native geometry, uncertainty and UI classification |
| B03 world/recovery | Extra High | Chart identity, provenance and fresh localization |
| B04 navigation | Extra High | A* commitment, measured strides and cycle recovery |
| B05 learning/evaluation | Extra High | State abstraction and isolation of all learning writes |
| B06 goals/executor | Extra High | Lifecycle, completion authority and restart ownership |
| B07a events/dialogue | Extra High | No-input script handling and safe world handback |
| B07b menus/party/choices | Extra High | Native evidence, resumable UI and team state |
| B08 NPC interaction | High | Reuse prior navigation/UI contracts with scoped identity |
| B09 inventory/healing | Extra High | Consumable reconciliation and emergency resumption |
| B10a first battle | Extra High | Native legal actions, result and post-battle closure |
| B10b wider battles | Extra High | Switching, new UI cases and broader legal-action masks |
| B11 battle learning | Extra High | Outcome eligibility and controlled policy comparisons |
| B12 optional capture | High | Extend verified bag/battle/team tools |
| B13 semantics/knowledge | High | Bounded providers, caches and retrieval |
| B14 director | Extra High | Rolling plans, learned choices and executor reconciliation |
| B15 travel/story | Extra High | Multiple charts, interrupts and verified story receipts |
| B16 campaign/release | Extra High | Independent evaluation and reproducible promotion |

An optional Astra Ultra review can audit the bounded B00 architecture or B16
release evidence. It is not a prerequisite. On High stages, escalate a specific
diagnosed protocol, identity or ownership problem to Extra High; do not restart
the whole project. If these models are unavailable, use an available coding
assistant and keep the same tests and native gates. A recommendation is not a
guarantee that generated code works, and changing the model does not satisfy a gate.

## Pro allowance versus purchased credits

A US$100 Pro subscription is not a balance of 100 purchased credits. As of the
check date, Pro has no five-hour limit; weekly limits may apply. Workspaces using
the same account share usage. Check that account's Usage dashboard; API prices
cannot predict included tasks. [Plan usage](https://learn.chatgpt.com/docs/pricing).

For purchased credits at Standard speed, per million tokens:

| Model | Uncached input | Cached input | Billed output |
|---|---:|---:|---:|
| Astra | 250 | 25 | 1,250 |
| Sol 6.1 | 50 | 2.5 | 250 |

For identical 100k uncached input + 20k billed output, that is 50 versus 10 credits.
This is not a Pro-allowance conversion or a fivefold guarantee per completed task.
[Credit rates](https://learn.chatgpt.com/docs/pricing#token-rates).

Use Standard speed to conserve usage. Faster service has a separate usage premium;
Ultra reasoning is not a request for Ultrafast service.
[Speed settings](https://learn.chatgpt.com/docs/agent-configuration/speed).

## Measure a budget for your build

Do not infer a number of stream hours from a plan name. Measure three
representative bounded tasks: a normal implementation, a map/ownership repair,
and a learning/evaluation change. Record account Usage immediately before/after,
model/effort/speed, time, tests, repairs and interventions. Keep other account work
quiet during each sample so the difference is interpretable. Do not expose account
pages, billing details or credentials on OBS.

Use the median observed allowance change per comparable task to plan the remaining
work before reset. A practical initial budget is 50% LAB, 30% reserved for stream
coding and 20% for unexpected repairs; these are suggested allocations, not plan
limits. Re-estimate after the first playable slice. If the meter does not provide a
usable exact delta, retain approximate samples and uncertainty instead of inventing
credit conversions. Do not repeatedly switch models and rerun entire histories.

Give the coding agent the initial prompt, ONE requested stage/slice, its dependency
receipt, relevant files and the failing check if present. The starter includes no
gameplay source or private LAB evidence: create the requested stage in a clean build,
or inventory the operator's existing LAB before reusing anything. Do not paste all
prompts, entire maps or every run log. Preserve the same acceptance
gate at cheaper settings. Escalate a bounded diagnosed issue rather than an entire
project rebuild. [Model selection](https://developers.openai.com/api/docs/guides/model-selection).

Running local Python/OpenCV/SQLite gameplay does not itself invoke the coding
assistant. Any configured runtime Cursor/other model calls use their own service
and billing. OpenAI API usage is separately billed; reasoning tokens there count
as output. [API reasoning](https://developers.openai.com/api/docs/guides/reasoning#how-reasoning-works).

API effort names differ from the app: Sol supports low, medium, high, xhigh and max;
`ultra` is not an API reasoning.effort value.
[Sol API](https://developers.openai.com/api/docs/models/gpt-6.1-sol).
