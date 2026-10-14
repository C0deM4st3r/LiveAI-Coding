# B12 — Optional capture as a reusable strategy tool

Recommended coding model: **GPT-6.1 Sol · High · Standard speed**.
Build over verified bag/battle/team tools; use Extra High for ambiguous result handoffs.
See [model guidance](MODEL_GUIDANCE.md).

Status: TARGET NEW CAPABILITY; catching is not required by every Brock strategy.
Dependencies: B09, B10b and B11, including their transitive dependencies.
Playable order: optional R9. Named-area travel is available only if B15 passed;
capture itself can be tested in an already grounded local encounter without B15.
Inventory actual capture capability first; preserve all earlier acquisition proofs.
STREAM adds capture to general battle/tool contracts, not a Pikachu-specific script.

## Copy-ready implementation prompt

Implement a typed capture option over the existing battle, bag, team, goal and
evidence interfaces. Expose it only after native wild identity, ball selection and
capture/result readers pass their gates. The director may choose it when team
capability/cost evidence justifies it; never force a catch before every Brock run.

Register `player.capture.attempt(encounter_ref, target_spec, ball_policy, limits)`.
Target_spec is any eligible species or a bounded species/property constraint, not
a screen coordinate or generated button script. Limits include balls, turns,
health threshold and stop reasons. Actual bounds come from run/operator policy;
an LLM cannot silently spend unlimited resources or alter emergency authority.

Require a fresh native WILD encounter, grounded observed target identity when
the request names a species, observed usable ball inventory and a legal battle UI.
Trainer and unknown encounters must reject capture before any bag input. A model
label, overworld grass or advice about spawn tables is not wild identity evidence.
Unsupported encounter/ball/game profiles remain blocked with missing capability.

Capture decisions reuse B11 state/actions with capture objective. Before capture
experience exists, use a declared conservative baseline over legal damage/status/
ball/escape choices. Do not assume lower HP, status or a ball type helps without
versioned mechanics knowledge. Avoid lethal weakening when measured uncertainty
makes it unsafe; a failed/fainted target is a real failed attempt, not success.

Delegate bag selection to B09 under battle ownership. Verify the intended ball,
accepted throw, observed inventory change and native outcome. Handle break-out,
no stock, rejected item, target faint, own faint, escape, capture and unknown.
Deduplicate dispatch receipts so a resumed uncertain throw first reconciles the
screen/inventory; it must not consume another ball just to obtain certainty.

Snapshot the fresh pre-encounter roster. CaptureReceipt includes encounter/session/
context, target identity evidence, throw/outcome captures, bag consumption,
post-capture UI branches and new member/storage evidence. Species already owned
does not make another capture impossible, but requires distinct acquisition lineage.
Starter possession is not a wild-capture receipt. Old captures cannot prove this run.

Handle recognized Pokédex registration and nickname choice through B07. Default
nickname behavior is explicit and observed; unknown choice layouts hold. A full
party/PC transfer requires a dedicated native storage verifier before completion;
until implemented, mark that branch unsupported and hold safely without fake
party evidence. Do not claim the party contains a member sent to unverified storage.

Register captured_member/acquired_species with fresh native capture result and
roster change or supported storage receipt. Complete the goal only after supported
UI closure, native team refresh where applicable and B03 safe world recovery.
Store new member fields in TeamMemory with provenance; partial stats remain unknown.
BattleMemory retains capture outcome and post-battle closure as separate evidence.

Record encounters, balls/turns, health cost, target misses/faints, captures, unknowns
and control failures. Feed eligible measured transitions to B11 only in train mode;
terminal capture rewards cannot be earned twice from the same receipt. Evaluate
with isolated state and immutable snapshots. Do not claim a larger team is always
better or use encounter count alone as proof of improved capture strategy.

Keep search separate from capture: B04 can explore a currently grounded area;
B15 supplies named travel only after its gate. Unknown habitat can request B13
advice if that provider is available; otherwise it remains missing knowledge. Neither prerequisite
permits a new parallel map or guessing an unobserved species from external text.

LAB adds this tool beside starter/first-rival paths; preserve historical failures
and source data. STREAM registers capture as an optional capability and reuses
the shared ownership/state machine. Do not add a mandatory capture dependency to
the Defeat Brock root merely because this checkpoint has been implemented.

Show short rows for target/ball decision, actual throw outcome, resources and
verified acquisition. Retain bounded source images only for actual semantic calls,
not every throw or animation frame. A failed throw is not a failed tool infrastructure.

## Verification and gate

Test trainer/unknown rejection, wrong species, empty inventory, failed throws,
target faint, duplicated throw receipt, repeated owned species, new member identity,
nickname/Pokédex branches, full roster unsupported hold and stale capture evidence.
Test evaluation no-writes and health interruption. Run stream_checks visibly.
Gate: recorded eligible wild capture yields a fresh acquisition receipt; full
party without a storage verifier and trainer balls never produce false success.
An explicit native test demonstrates the covered profile before live admission.
Cue: “Catching is one available strategy, justified by the team and the objective.”
Update capability coverage and stop; no automatic capture or Brock run follows.
