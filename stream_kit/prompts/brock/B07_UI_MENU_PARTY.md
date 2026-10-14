# B07 — One native UI layer, delivered in two playable slices

Recommended coding model: **B07a and B07b: GPT-6.1 Sol · Extra High · Standard speed**.
Each slice owns fresh native UI evidence and safe return to world navigation.
See [model guidance](MODEL_GUIDANCE.md).

Status: UI implementation prompt; build and validate only the requested slice.
**B07a dependencies: B00–B04. B07b dependencies: B00–B06 plus B07a.**
Request exactly one slice. Apply the common contracts and that slice's work/gate;
do not implement B07b automatically when building B07a at the first Oak event.
Build the final UI interfaces over B02 perception and B03 recovery, without a
starter-specific runner. Earlier slices' tested readers remain canonical.

## Common copy-ready contract

Preserve native readers, reviewed cues and all team/proof history. Use one typed
UI ownership machine from fresh native screenshots. Keep FireRed rendering/readers
in a profile; menus, fonts, identities and controls are not universal Pokémon facts.

UiObservation carries capture_id, context_id, session_id, profile_version, kind,
stability, fields, uncertainty and source_refs. Kinds can include world, script,
dialogue, choice, start_menu, party, summary, bag, battle, learn_move, evolution,
blackout and unknown. Declaring a kind does not register its executor.
Unknown/conflicting values stay null; model labels cannot become native facts.

Expose ui.classify/acquire/release and resumable typed player tools through B00's
one catalog and control lease. All calls carry its EpisodeContext and immutable
request/session identity. B06 later dispatches these same tools, not parallel loops.
Only the current owner may press keys. Stop releases keys immediately and preserves
honest resumable UI state. Persist dispatch intent before input and reconcile the
fresh screen on resume; never blindly repeat a possibly consumed A press.

B07a uses the permanent trusted direct-tool entry from B04 before B06 exists.
It returns a ToolResult and native evidence; no GoalManager lifecycle is needed.
Before B05, label policy mode as execute-only baseline and do not advertise frozen
evaluation. Once B05 is available propagate its mode/storage permissions. B07b
requires B05/B06 and registers its tested completions in their existing catalog.

Feed one meaningful row per UI handoff, dialogue change or completed inspection.
Keep raw frames in RAM and compact provenance in SQLite; no per-page/frame archive.

## B07a — Script/dialogue events at the first encounter

Build only event ownership, bounded settled-dialogue advancement and world handback.
During scripted motion/fades release keys and suspend mapping. Observe neutrally;
never force a transition because enough time passed. Advance only recognized
settled dialogue whose UI profile explicitly permits it. Unknown choice/menu/battle
returns held with the missing capability and zero improvised input.

Persist ScriptSession with native opening/capture lineage, observed phases,
dialogue advancement receipts, current eligible completion window and release.
Expected destination hints require current-session script evidence, not a future
Oak goal or text-only plan. Existing physical passage evidence retains precedence.
After control release, require B03's two NEW stable full matching localized views
before navigation or new strategy planning. Reuse the same saved world store.

Provide typed event/control-release validators with scoped native evidence.
They can later support reusable goal rules, but “Oak:” text alone does not prove
starter acquisition, laboratory pose or an entire objective. An Oak fixture may identify
a covered event profile; it must not encode an unconditional button route.

Test no presses/map writes in motion, settled text versus animation, unknown choice,
stale session hint, Stop/resume and mandatory two-view recovery. A requested native
demonstration starts from the current event or an explicitly selected setup; no
automatic restore. Gate: supported event/dialogue finishes and fresh world control
recovers without duplicate charts. Unsupported branches visibly hold.
Cue: “When the game takes control, the player waits, then finds itself again.”
Record only B07a coverage; stop. R2 does not mean all menus or B07 are complete.

## B07b — Menus, choices, world interactables and complete team

Reuse B07a ownership; add player.menu.open/select/close_to_world,
player.choice.select and player.party.inspect as sensed operations. Read actual
options/highlights, select one bounded typed option and verify the effect.
Recognize paging/cursor wrap. Do not assume a fixed Down count or B-spam unknown UI.

Add reusable player.interactable.use(target_ref, intent, choice_policy) over a
grounded non-NPC world entity, with measured adjacent approach/facing, bounded A,
causally linked native opening and complete UI closure. Reuse ChoicePlayer/profile
readers for supported starter-object confirmation, yes/no and explicit nickname
decline. This is a general entity/choice tool, not a hardcoded starter route.
B08 owns NPC identity/conversations; the two tools share UI/dialogue primitives
without falsely labeling a Poké Ball as an NPC or inheriting another entity's identity.
Unknown object effects/choices stay unavailable until their profile is tested.

A starter choice must produce a fresh native acquisition receipt plus compatible
current-party evidence after supported closure. A generic yes/no box, old party
snapshot or a tool success boolean cannot certify a new Pokémon. Register native
validators in B06: team_inspected, party_contains and the tested acquisition rule,
with distinct observed-possession versus new-acquisition semantics.

Create or extend canonical TeamSnapshot storage: context/session/captures, reader/profile/source,
roster completeness, member/slot identity, species/dex/name, level, HP/max HP,
status, moves/PP/max PP and uncertainty. Unknown fields are null, never full/healthy.
Require paired stable native reads for completion/safety fields. Retain lineage.

Define six-slot-capable storage now, but R3/R4 may admit a tested single-member
native profile first: inspect the roster sufficiently to verify the other slots
are empty, identify the current member and read the acquisition-required fields.
Do not require all summary/status/PP/multi-party readers before that first demo.
Unreadable slots stay unresolved, never empty; unread fields stay unknown. A profile
cannot claim complete team information beyond what its native reads established.
Widen egg/fainted/multi-member/summary coverage before B10b admits those branches.
Track duplicate species through compatible attributes/acquisition lineage; ambiguous
identity holds. Recognize move-learning/evolution and hand off only to an available
executor. B07b does not claim battle support merely by recognizing those screens.

Observe current native UI before every resumption; distinguish team observation
from safely closed/localized world handback. No party screen alone completes
NPC/battle/major goals. Stale/partial team snapshots cannot clear healing blockers.
Keep manual blockers and prior snapshots. No game RAM/save-file parsing.

Use this ownership layer from the first menu/object;
NPC/battle/director add tools without replacing it. Evaluation observations go only
to the fresh episode overlay, never frozen training memory.

Test menu wrap, page changes, unknown choices, repeated dispatch, partial rosters,
duplicate species, faint/status/PP, native acquisition versus old possession,
grounded object approach, starter confirmation and nickname branches. Test
object/NPC identity separation and B07a interruption/recovery regressions.
Run stream_checks serially after gameplay releases ownership.

Gate: a supported native object/choice/complete-party/close cycle produces fresh
scoped evidence and returns a localized world. Recorded fixtures alone do not
establish current live support. A requested bounded native starter test verifies
the admitted profile; it stops before an unsupported rival battle.
Cue: “Each screen has one owner, and a new teammate is verified from the game.”
Update capability coverage and B07b receipt; stop after this slice.
