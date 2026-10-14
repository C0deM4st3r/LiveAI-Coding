# B15 — Grounded travel, outdoor continuity and story interactions

Recommended coding model: **GPT-6.1 Sol · Extra High · Standard speed**.
Cross-chart identity, interruption recovery and story evidence need integrated checks.
See [model guidance](MODEL_GUIDANCE.md).

Status: travel implementation prompt; recorded charts alone do not provide named-place travel.
Dependencies: B09, B10b and B14, including their transitive dependencies.
Playable order: R8 after general battle coverage; B12 capture is optional, not required.
This completes transport/story tools for longer campaign trials.
Reuse B03's shared geometry/passage store, local A*, UI ownership and goal graph.
Extend those tools; do not rebuild house-only navigation or hardcode a route to Brock.

## Copy-ready implementation prompt

Implement cross-chart travel and grounded story steps over the existing world.
Expose `player.travel(destination_ref, constraints)`,
`player.explore_region(region_ref, information_need, limits)`, and generic
interaction/item/story tools already admitted by B08–B10. Place names must resolve
to grounded entities/chart candidates or an explicit exploration objective.

PlaceIdentity stores stable place ID, aliases/role hypotheses, chart memberships,
support observations and directed entrances. Names narrow candidates; they never
merge charts. Shared world remains canonical. A city may have several charts and
entrances until measured overlap proves a compatible transform. Persist proposed,
accepted and rejected transforms with evidence; conflicting geometry stays separate.

A travel plan combines known directed passage graph edges and B04 local routes.
Store source/destination chart, exact departure tile/action, arrival candidate,
support/cost/risk and observation lineage. Reverse edges require their own actual
crossing evidence. Known source+tile+action pins the strongest unique verified
destination; ties/mismatch hold. Saved spawn is never blindly copied as current pose.

Recover each arrival with two fresh stable localized views. Distinguish legitimate
camera scrolling, area transition, script/blackout relocation and mere coordinate
reset. Preserve B03's known-destination precedence over goal hints and recovery
before navigation/planning. A return entrance into a known city reuses identity
through verified links/anchors; it must not create a city just because view differs.

For unmapped extensions, request connected edge captures with meaningful existing
overlap plus new area. Confirm scale/transform from measured anchor/odometry and
reject ambiguity. Candidate floor stays a proposal until physically traversed.
Use frontier utility/cost and B05 learned options, not exhaustive corner walking
or repeatedly traversing only known tiles. Solved/covered views skip new captures.

Travel is resumable: persist current graph leg, local target, assumptions and goal.
Wild/trainer battles interrupt navigation immediately through B10; no queued
direction continues into a battle/menu. Finish battle/team/world recovery, update
risk/resources, handle health emergency, then replan or resume the same destination.
Dialogue/scripts similarly transfer ownership. A defeated trainer can change a
route assumption only through observed current evidence, not generic win text.

Update route costs from measured duration, obstruction and encounter frequency
with context/version provenance. Keep geometry proof separate from empirical risk.
Evaluate against immutable map/policy/fact snapshots and fresh episode overlays;
discovery during one evaluation cannot improve the next. Record localization
failure/control intervention separately from strategic route cost.

Register named_place_reached from grounded place/entrance identity and fresh pose,
not the model's city label. Story progress requires event-specific native item,
interaction or encounter receipts selected from the catalog. Unknown story flags
stay unknown; no ROM/RAM/save parsing or invented hidden progression state.

Build the FireRed route knowledge as versioned declarative facts with sources:
starter access, observed rival/story prerequisites, Viridian Mart parcel receipt,
delivery to Oak, onward Route 2/forest/Pewter/gym access. Verify references when
implementing; do not hardcode unverified coordinates or assume every run lacks
the parcel. Mart receipt may trigger on entry; delivery is a distinct objective.
The director decides which prerequisites remain and invokes existing typed tools.
Knowledge references: [Mart entry script](https://github.com/pret/pokefirered/blob/master/data/maps/ViridianCity_Mart/scripts.inc)
and [Oak's laboratory script](https://github.com/pret/pokefirered/blob/master/data/maps/PalletTown_ProfessorOaksLab/scripts.inc).
These inform roadmap design only; script/ROM/RAM flags cannot prove live progress.

Explore/retrieve knowledge when a required entrance/service is unknown; keep a
bounded search budget, alternatives and clear no-progress cause. Missing traversal
mechanics (ledge direction, door interaction or unsupported UI) are capabilities
to implement/test, not guessed walkability. Do not add all future game mechanics.
Never choose a long risky detour just to satisfy an old fixed story recipe.

Preserve chart fragments and passages built through B03; validated identity/overlap
adds provenance without destructive merging. Keep previously measured local routes
as regression cases. Reuse B03's measured world/recovery and add this routing layer
once. Feed current destination, meaningful leg/route changes and interruption
outcomes; dashboard keeps transparent game and bounded current goal cards.

## Verification and gate

Test same city/multiple entrances, wrong goal destination hint, ambiguous overlap,
camera scroll, null pose, no reverse-edge inference and incompatible chart names.
Test battle/poison/blackout interruption, resume destination, changed obstruction,
item receipt versus pre-existing item, distinct parcel delivery and missing story UI.
Run visible stream_checks with measured/recorded fixture provenance.
Gate: bounded requested live legs recover known destinations without new duplicate
charts, survive an encounter handoff and verify a real story/service receipt.
Stage long routes gradually; a successful house exit is not city continuity proof.
Cue: “Places connect through journeys the agent verified, and interruptions keep the destination.”
Record live limitations; do not launch the Brock campaign until B16 admission.
