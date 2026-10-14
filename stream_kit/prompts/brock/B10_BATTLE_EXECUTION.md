# B10 — One battle executor, from the first rival to wider encounters

Recommended coding model: **B10a and B10b: GPT-6.1 Sol · Extra High · Standard speed**.
Use the same evidence and ownership bar for the narrow and wider battle profiles.
See [model guidance](MODEL_GUIDANCE.md).

Status: battle implementation prompt; build and validate the requested profile slice.
**B10a dependencies: B00–B08. B10b dependencies: B10a plus B09.**
Request one slice. Apply the shared contract and its slice; do not require inventory
or all wild/trainer cases before demonstrating the first admitted battle profile.
B11 trains decisions; B10 makes those decisions execute and verifies actual results.
LAB inventories and reuses verified battle/post-battle and native team readers, if any.
STREAM builds one encounter tool with incremental profiles, never a rival coordinator.

## Shared copy-ready executor contract

Separate BattlePolicy from native BattleExecutor. Use the canonical battle history
and tool/completion registries; add schemas without rewriting earlier result semantics.
Expose player.battle.observe, legal_actions, execute(action,expected_state_id),
resume(encounter) and close(encounter). Every call uses B06's single lease/session.

BattleObservation includes encounter/context/session, fresh captures, profile,
encounter kind and identity evidence, acting member/opponent, HP/status/level,
observed moves/PP, options/highlight, phase, switch requirements and uncertainty.
Unknown fields remain null. Type/mechanics knowledge is versioned advice; native
move text does not supply an unknown damage formula or named-opponent identity.

BattleAction is a tagged union: fight(move_ref), switch(member_ref), item(item_ref,
target_ref), run or a supported progression choice. Register only implemented
variants/profiles; the existence of a tag is not capability. Mask zero PP, stale
state, unreadable targets, absent items, fainted switches and trainer escape/capture.
Never execute raw model button sequences or arbitrary menu labels.

Dispatch rechecks native state, selects sensed highlights, verifies acceptance,
then observes actual turn phases. A key press is not a resolved turn. Persist
intent before input and reconcile current UI after interrupted dispatch.
Record before/after/action/legal mask/policy version and native outcome references
for B11; UI/control failures are not tactical defeats or guessed damage.

Use challenge → command → execution → resolution → progression/terminal →
team_refresh → world_release phases with evidence-based transitions and deadlines.
Wins, losses, escaped, captured, interrupted and unknown remain distinct outcomes.
BattleMemory result and safe closure stay separate. PostBattlePlayer handles only
supported dialogue, refreshes the native team, then obtains B03 two-view recovery.
Unknown resolution remains held; it must never complete the goal as a win.

The baseline is a transparent selector over currently legal observed actions,
not a universal two-Growl script. Use known mechanics/resources with bounded risk;
no-PP Growl selects another legal supported move when available. If no legal
supported action exists, hold with exact missing coverage rather than loop.
B11 may replace selection with learned values without changing execution/evidence.

Propagate B05 train/execute/evaluate permissions. Feed changed state, chosen legal
action, observed result and closure; no speculative success rows or frame archive.
A model/planner cannot widen coverage or override the legal mask at runtime.

## B10a — First admitted battle, immediately after the starter

Implement/test the limited first-rival profile behind the general executor:
supported one-member/one-opponent encounter, recognized attack/status moves,
accurate PP/current menu, native turn resolution and fresh terminal evidence.
Scope reader/move coverage explicitly; reuse tested native cues, not a fixed battle
button trace. New recognized move data uses the general move interface.

B10a does not depend on B09. Item/run/switch/capture and untested progression choices
remain unavailable. It must recognize their screens as boundaries, release input
and return held instead of misclassifying them as an attack menu.
A first-battle loss is recorded from native loss evidence. Unsupported blackout
relocation stays held; it is not a fake world closure or implicit state restore.

Register encounter_finished/battle_won for this covered profile with fresh
same-attempt native terminal evidence. Named identities require their own native
opening/result support. One faint cannot be generalized to multi-opponent victory.
Brock/named badge coverage is unavailable. Fresh post-battle team and localized
world handback complete the session closure, separately from recording the result.

If B14 exists, it can request this tool through the unchanged registry. The director
may move toward a grounded observed encounter trigger, then transfer ownership;
there is no new first-rival macro runner. If the trigger/identity is unknown,
use supported observation/advice or hold rather than execute a hidden route.

Tests: legal-mask/PP fallback, sensed highlight, unexpected UI/choice, stale/duplicate
outcome, unknown versus loss, interruption/resume, team refresh and two-view handback.
Gate: recorded profile closes honestly, then a separately requested native rival
test verifies the admitted scope. A loss can verify execution without claiming a win.
Cue: “The first battle uses the same tool that will later handle larger encounters.”
Record B10a coverage only; stop. B11 can now train this profile before B10b exists.

## B10b — Wild, multi-opponent and progression coverage

Extend the SAME executor to early FireRed wild/trainer encounters, multiple own/
opponent members, switching/faint, status, PP, supported items and progression.
B09 provides inventory/item semantics; battle retains turn ownership during use.
B12 capture remains unavailable until separately gated.

Support data-driven recognized move identities rather than a growing special-case
Tackle/Scratch/Pound list. Handle enemy turns, misses/failed effects, forced/optional
switch, next trainer member, experience, level-up, new-move and evolution screens.
New-move replacement needs a typed admitted choice and observed known slots.
Explicit conservative decline/evolution policies must read and verify the branch,
record the skipped opportunity and inspect any resulting team/member changes.
Unknown screens still hold; a safe decline is not knowledge of an unseen option.

Support no-PP/Struggle where the profile is tested. Legal run requires observed
wild context; trainer/unknown context cannot escape or capture. Item actions need
native before/effect/consumption evidence; no-effect and ambiguous use stay distinct.

Verify full multi-opponent resolution before battle_won. Register named trainer
results only for native identity/result profiles actually covered. Generic trainer
victory never proves Brock; final named-result/badge coverage is B16's admission.

Handle supported blackout relocation with native loss/relocation evidence. Do not
pin the old battle chart or invent a passage when blackout changes location.
Perform fresh team/world recovery; hold safely if destination cannot be grounded.
A resume cannot replay the last attack/consumed item merely because its receipt
was interrupted. Reconcile the screen/resources first.

Widen B11 legal action/state bindings only after these branches pass. Preserve the
same learner/episode/policy lineage with explicit action-schema versions and
compatibility checks; a first-rival learned policy does not automatically cover
unseen switches/items/moves. Retain its frozen baseline for matched comparison.

Tests: wild/trainer identity, zero PP/four moves, forced switch, multi-opponent,
poison/faint, item/no-effect, escape, move-learning, evolution, blackout relocation,
wrong trainer, unknown outcome and crash after accepted dispatch.
Run focused stream_checks visibly after gameplay releases ownership.
Gate: recorded wild/multi-opponent encounters and all admitted interruption paths
close correctly; explicitly requested native tests then qualify their profiles.
Cue: “New battle situations add tested actions, while the same guards stay in charge.”
Update coverage and receipts; do not launch longer travel or training implicitly.
