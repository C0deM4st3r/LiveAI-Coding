# B03 — One visual world, persistent passages and reliable recovery

Recommended coding model: **GPT-6.1 Sol · Extra High · Standard speed**.
Mapping identity, evidence freshness and recovery need one coherent implementation.
See [model guidance](MODEL_GUIDANCE.md).

Playable order: support for R1. Dependencies: B00–B02. Next: B04.
Status: implementation prompt; passing isolated recovery does not establish a
clean route replay or prove that separately recorded charts share coordinates.
Copy with the canonical restart prompt. Implement this stage only.

## Shared memory and ownership

Implement this final shared world in B00's canonical SQLite memory; no temporary per-room tile store,
duplicate navigator map or model-owned world DB. Version schemas transactionally.
All later tools/director/policies retrieve the same world through typed queries.
Preserve captures, charts, measured transforms, passages and failed evidence as
this build accumulates them. The starter supplies neither mapped rooms nor charts.

## Measurement and chart identity

Record immutable capture identity, context, observed grid transform, fractional
pixel odometry and masked directional sprite measurements. Pose is measured or
null. Persist distinctions between seen candidate floor, occupied/traversed floor,
confirmed obstacles, uncertain graphics, NPC occupancy and portal hypotheses.
Only full measured occupation can promote floor to walked. Strong straight pixel
odometry may confirm crossed intermediate centres; commands, endpoints and anchor
correction cannot invent them. Dynamic blockage does not become a permanent wall.

Recover saved charts before creating fragments. Compare static masked geometry
and measured overlap/scale/phase; ambiguous origins remain unresolved. Names and
semantic labels narrow candidates but never merge coordinates. Track chart ID
separately from a hypothesized place identity; one town can have multiple charts.
Only measured transform provenance supports an atlas connection/merge. Preserve
source coordinates and evidence; do not implement “same name means same map.”

Keep bounded connected keyframes at coverage edges with old/new overlap and
measured trajectory. Solved covered views do not need repeated model screenshots.
Camera scroll expands the chart only when the transform is justified. A failed
recovery may produce a separate chart after bounded fresh stable observations,
but never while a known directed destination is pinned. A reset proves no passage.

## Passage and recovery precedence — include this from the start

A fresh source full pose plus measured departure action and stable destination
evidence records a directed passage. Mark actual supported portal/arrival cells;
do not invent a tile behind the sprite or an untraversed reverse direction.
Unknown coordinates remain null. Record multiple entrances independently.

Source chart + exact measured tile + action selects the unique strongest verified
destination. Its saved arrival coordinate is only a candidate. That physical pin
outranks every goal expected_scene, including future blocked Oak objectives.
Two NEW stable full localized views establish current arrival pose; do not copy
the historical spawn into current state. Ties/mismatch hold, with no global guess,
new fragment or goal fallback beyond the pin. Persist the descriptor across restart.

Source evidence must match current context and capture, with no partial sprite.
Incomplete departure events may nominate a chart only from the last measured source
with no later localized observation. They provide neither coordinates nor a new
proof. Native expected-scene hints require an eligible current-session script
window; blocked future goals cannot supply a destination. Pass exact session IDs.

Mandatory recovery runs after cutscenes or invalid pose, before navigation or new
strategy planning. Require stable world and two new matching localized captures.
Script/fade frames never map. While unlocalized, release input and use neutral
sensing; no blind reversal of the last five commands. Persist a clear held cause.
Recovery may retry within its bounded budget; Stop/bridge error ends its ownership.

## Acceptance and handoff

Visible offline checks cover chart reuse, animation/camera changes, occlusion,
duplicate rooms, source freshness, old-session hints, multiple entrances, ties,
spawn candidate mismatch, persistence and no interpolated walked cells.
Create a regression where a known stairs passage conflicts with a future
Professor Oak laboratory goal: the measured passage must win. Test recovery after scripted
movement and a restart without assigning saved coordinates. No chart deletion.

An explicitly requested live gate is a bounded known passage out/return plus a
fresh neutral recovery. Count chart creation, matching errors and measured pose;
two screenshots that pass a fixture do not establish a completed route.
At bootstrap, chart origin is a local coordinate convention backed
by a fresh capture, not a claim to a global town coordinate or known destination.

Observable gate: measured movement updates the same chart; a known crossing pins
the right saved destination and recovers from two fresh views without duplication.
Narration: “It remembers where an entrance leads, then verifies where it arrived.”
Expose pose, measured graph, candidate frontiers, passage candidates and recovery
status to B04. Update reliability evidence and stop before autonomous exploration.
