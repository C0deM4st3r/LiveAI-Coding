# B02 — Native perception, uncertainty and UI ownership

Recommended coding model: **GPT-6.1 Sol · Extra High · Standard speed**.
Use the same acceptance gate for fixture geometry and uncertain UI ownership.
See [model guidance](MODEL_GUIDANCE.md).

Playable order: support for R1. Dependencies: B00–B01. Next: B03.
Status: perception implementation prompt; a supplied panel is not a native detector.
Coverage is limited to the game/UI profiles actually built and verified here.
Copy with the canonical restart prompt. Implement this stage only.

## Build on native observations

Implement a single PerceptionAdapter producing B00 observations from B01 captures. Keep
FireRed templates/rules separate from generic ownership, freshness and schema.
Do not build a screenshot-hash game controller or require Qwen before mapping.
Other Pokémon games need their own tested adapter; an interface is not support.

## Structured observation

Each observation references exactly one fresh capture with adapter/version,
context, timestamp and native pixel dimensions. Preserve enough scale metadata
to map image coordinates correctly. Never resize silently and reuse old geometry.
Return native UI class, stability, control eligibility, sprite matches, grid
candidate, camera/background motion, dialogue/menu regions and uncertainties.
Supported UI classes include world, dialogue, choice, menu, party, battle,
script/fade and unknown; only implement positively recognized subclasses.
Unsupported or ambiguous UI is unknown/held, not world by exclusion.

Sprite coordinates carry full/partial/occluded status and match ambiguity.
Partial head matches cannot yield confident foot coordinates or traversed cells.
Reject duplicate matches; mask the actual sprite and dynamic NPC regions when
comparing static geometry. Animation must not create a different place or state.
Grid scale/phase comes from measured cues or matching capture-backed anchors;
unavailable scale means unavailable tile coordinates. Keep fractional motion.
Color alone cannot identify outside, a room, a walkable tile or a successful goal.

Use native visible text/template/OCR evidence with confidence and region/capture
provenance. OCR and pretrained semantic descriptions are fallible observations.
Critical verifiers must reject ambiguous values, wrong windows and stale text;
a general transcript cannot grant named-NPC/item/battle completion authority.
Store compact prototypes and bounded diagnostic disagreements, not every frame.

## Control and mapping gate

A central observation gate routes the single owner to the appropriate registered
tool. During script motion/fades, release keys and suspend map writes; observe
neutrally until stable UI is recognized. At B02, dialogue/menu/battle can hold:
their handlers arrive in B07a/B07b/B10 slices, not improvised A presses in the mapper.
Script exit or invalid pose latches mandatory B03 recovery. Neither a visually
stable world frame nor a planner's desired location clears that latch alone.
Pending future semantic vision holds input until reply/error, with one call at
a time; implement that contract without making a model call in this stage.

Separate visual observation identity from abstract learning state. Digest aids
capture/cache integrity; the learner later consumes grounded state features.
Similar animations should yield the same stable feature representation while
different UI modes or genuinely distinct geometry remain distinguishable.
Unknowns remain explicit; do not average inconsistent readings into certainty.

## Fixtures and metrics

Collect authorized samples through B01, or explicitly supplied fixtures with
provenance; no game screenshots are included in the starter. Preserve source
evidence. Maintain labeled samples for each supported UI, animation, occlusion, duplicate
sprite, scrolling, stale capture, fade and look-alike place. Add fixtures only
when needed; record what was human-labeled versus inferred.
Test invariance on animation and camera motion, freshness rejection and gating.
Report a confusion table and unknown/rejection rate for the fixture corpus.
Every supported detector must have false-positive examples, not just happy paths.
No arbitrary “95% confidence” constant counts as calibrated probability.

Visible stream_checks prove fixture behavior; they do not prove live semantic
accuracy. When explicitly requested, perform a neutral current-position check
and compare its labels to the native frame; never restore solely for this check.
Do not consume the bridge while another owned run/check is active.

## Acceptance and handoff

Observable gate: world/script/dialogue distinctions and pose uncertainty survive
recorded adversarial cases, controls release for unsupported UI, and no map tile
or goal is created from a detector label alone. List supported FireRed UI scope.
Narration: “The agent first decides what it can reliably see and when it can act.”
Export typed observations, detector versions and freshness rules to B03.
Record implemented/fixture/live evidence separately; keep unresolved cases visible.
Stop before adding automatic dialogue handling, semantic calls or strategic goals.
