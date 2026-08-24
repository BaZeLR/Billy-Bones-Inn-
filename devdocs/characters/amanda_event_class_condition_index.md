# Amanda Event Class / Condition Index

This file is an index and correction target for Amanda events.

Current runtime status:

- Amanda's non-dance story events are named `AmandaEvent` subclasses in `AmandaEventModel.rpy`.
- Common day/hour/probability/location/action checks remain owned by `Event.canTrigger()`; subclasses contain only Amanda-specific facts.
- `event_runtime.fired_keys_today` owns once-per-day event identity. Retired `*_seen_day` mirrors are removed during save repair.
- `AmandaLegareDance.num` is the only ordered Legare-dance stage. The former parallel stage/cache values are retired.
- Alternative events that belong to the same ordered stage are nested together in one trigger stage, matching the Family Life thread model.

The remaining audit target is Amanda's dance-event factory and non-story action predicates. Keep genuine action availability methods, but do not reintroduce external event-ready wrappers or parallel progress state.

## Source Authority

Amanda source authority is mixed:

- Original TXT/reference content remains source material for scene content and event intent. It must be ported without changing meaning or context unless new content is explicitly being added.
- Live `.rpy` files are the current executable runtime and must be checked before claiming that an event is wired.
- New Amanda development can add new scenes, conditions, and continuations, but new code must follow the OOP character/event model.

## Required Event Object Shape

Amanda event records should use the project's event object contract. The runtime reference is `Event` in `game/Utilities/General/Events/events.rpy`.

Existing event methods:

- `Event.canTrigger(evtDay=0)`
- `Event.auditChecks(evtDay=0, include_item=True, roll_probability=False)`
- `Event.checkDay()`
- `Event.checkHour()`
- `Event.checkNumDay(evt_numDay)`
- `Event.checkReqs()`
- `Event.checkConditions()`
- `Event.checkProb()`
- `Event.checkItem()`
- `Event.checkBlocks()`

Existing thread status methods/state:

- `ThreadInfo.checkActive()`
- `ThreadInfo.complete()`
- `ThreadInfo.abort()`
- `ThreadInfo.enable()`
- `ThreadInfo.forceEnable()`
- `ThreadInfo.advanceTo(...)`
- `ThreadInfo.setDay(...)`
- `ThreadInfo.checkBlocks()`
- `ThreadInfo.statusText()`
- `ThreadInfo.currentTarget()`
- `LThreadInfo.advance()`
- `LThreadInfo.reactivate(...)`
- `LThreadInfo.reset()`
- `LThreadInfo.getAvailableEvents()`

Story board status terms already used by code:

- thread: `active`, `complete`, `aborted`, `blocked`, `future`
- event step: `done`, `aborted`, `blocked`, `available`, `waiting`, `future`, `unknown`

Minimum semantic class shape for Amanda-specific event data:

```renpy
init python:
    class AmandaEventData(Event):
        def __init__(
            self,
            evt,
            thread_name,
            threaded,
            code_name="",
            source_refs=None,
        ):
            super(AmandaEventData, self).__init__(evt, thread_name, threaded)
            self.code_name = str(code_name or self.target or "")
            self.source_refs = list(source_refs or [])

        def checkConditions(self):
            if not super(AmandaEventData, self).checkConditions():
                return False
            return self.checkAmandaConditions()

        def checkAmandaConditions(self):
            return True
```

The exact subclass can vary, but the semantics must stay aligned with the reference:

- event availability is checked by `Event.canTrigger()`;
- day/hour/delay/requirements/probability/item/location/action/priority are event fields, not custom wrappers;
- Amanda-specific state belongs to Amanda through `Amanda.var` and Amanda methods;
- stage movement uses the thread status methods (`thread.advance()`, `thread.complete()`, `thread.abort()`, `thread.advanceTo(...)`) at the real outcome point;
- no `globals()`, `renpy.store`, tuple-only logic, bridge wrappers, refresh/rebuild labels, or hidden fallback claims.

## Amanda Events As Event Classes

The list below describes the desired event-class records. `Current runtime` names the live label/tuple hook when one exists. It does not mean the event is already architecturally clean.

### AmandaLegareDance_0

- Thread: `AmandaLegareDance`
- Current runtime: `story_amanda_legare_dance_0`
- Start binding: `FridayDance / enter`
- Time gate: Friday, `18..21`
- `Event.canTrigger()` fields plus Amanda-specific conditions:
  - weekday is Friday;
  - current hour is inside `18..21`;
  - Clara/Clarissa is not at `FridayDance`;
  - Amanda is at `FridayDance`;
  - `Amanda.var["leftdances"] == 0`;
  - Amanda/Legare dance thread is still at sequence `0`;
  - Amanda has no active Legare prohibition.
- Start:
  - show Friday dance scene;
  - mark Legare interest as seen through Amanda state;
  - advance `AmandaLegareDance` from event `0` to event `1`.
- Current cleanup need:
  - remove vague `Amanda.legare_intro_ready()` as a wrapper name;
  - put the full condition list on the `AmandaLegareDance_0` event object;
  - do not leave this as an anonymous tuple condition list.

### AmandaLegareDance_1

- Thread: `AmandaLegareDance`
- Current runtime: `story_amanda_legare_dance_1`
- Start binding: `FridayDance / amanda_dance_legare`
- Time gate: Friday, `18..21`
- `Event.canTrigger()` fields plus Amanda-specific conditions:
  - weekday is Friday;
  - current hour is inside `18..21`;
  - Clara/Clarissa is not at `FridayDance`;
  - Friday dance slot is active;
  - `FridayDancesCount < 5`;
  - `DanceStep == 0`;
  - `Amanda.var["leftdances"] == 0`;
  - dance table gives Amanda to Legare for current dance count;
  - Amanda/Legare relationship is low enough for early-stage public dancing.
- Start:
  - create Amanda/Legare dance stage: talking while dancing;
  - set `Amanda.var["albernowdances"] = 1`;
  - increment dance count;
  - set `DanceStep = 1`;
  - set Amanda thread sequence/stage to `1`;
  - open `IntAmandaDance`.
- Current cleanup need:
  - stage advance should be owned by the event/thread object, not loose tuple plus label side effects.

### AmandaLegareDance_2

- Thread: `AmandaLegareDance`
- Current runtime: `story_amanda_legare_dance_2`
- Start binding: `FridayDance / amanda_dance_legare`
- Time gate: Friday, `18..21`
- `Event.canTrigger()` fields plus Amanda-specific conditions:
  - weekday is Friday;
  - current hour is inside `18..21`;
  - Clara/Clarissa is not at `FridayDance`;
  - same base dance-count and `DanceStep` conditions as `AmandaLegareDance_1`;
  - Amanda friendship/trust with Legare is high enough for closer dancing;
  - Amanda corruption is high enough to allow public groping, or friendship is high enough that she tolerates it.
- Start:
  - create Amanda/Legare dance stage: closer dancing and groping;
  - set Amanda thread sequence/stage to `2`;
  - open `IntAmandaDance`.

### AmandaLegareDance_3

- Thread: `AmandaLegareDance`
- Current runtime: `story_amanda_legare_dance_3`
- Start binding: `FridayDance / amanda_dance_legare`
- Time gate: Friday, `18..21`
- `Event.canTrigger()` fields plus Amanda-specific conditions:
  - weekday is Friday;
  - current hour is inside `18..21`;
  - Clara/Clarissa is not at `FridayDance`;
  - same base dance-count and `DanceStep` conditions as `AmandaLegareDance_1`;
  - Amanda friendship/trust with Legare is high enough for an intimate public stage;
  - Amanda corruption is high enough for kissing, or the Legare friendship path has reached that stage.
- Start:
  - create Amanda/Legare dance stage: kissing;
  - mark the private/intimate Legare dance stage as seen;
  - change Amanda mana for Legare pressure;
  - set Amanda thread sequence/stage to `3`;
  - open `IntAmandaDance`.

### AmandaLegareDance_4

- Thread: `AmandaLegareDance`
- Current runtime: not cleanly separated as its own event object yet; currently handled through dance/after-dance labels.
- Start binding: after Amanda/Legare dance completion.
- Time gate: Friday evening dance context.
- `Event.canTrigger()` fields plus Amanda-specific conditions:
  - Amanda/Legare dance stage `3` has completed;
  - Amanda decides to continue after the dance;
  - decision depends on Amanda-owned friendship/trust, corruption, mana, and current prohibition state.
- Start:
  - after-dance Legare continuation;
  - Amanda may leave with Legare, resist, or create a player-intervention branch.

### AmandaLegareDance Stage Model

The thread is `AmandaLegareDance`.
Events are sequence-numbered:

- `AmandaLegareDance_0`: intro/Legare notices Amanda.
- `AmandaLegareDance_1`: talking while dancing.
- `AmandaLegareDance_2`: closer dancing/groping.
- `AmandaLegareDance_3`: kissing.
- `AmandaLegareDance_4`: after-dance continuation if Amanda decides to go further.

The event object checks all its own gates through `Event.canTrigger()`.
The thread advances only when the real stage outcome is reached.
Amanda-owned state used by these checks must come from `Amanda.var` and Amanda methods, not `AmandaVar`, `story_value`, or external ready-wrapper functions.

### AmandaFridayDanceMCEvent

- Thread: `AmandaFridayDanceMC`
- Current runtime: `story_amanda_friday_dance_mc_0`
- Start binding: `FridayDance / amanda_dance_mc`
- Time gate: Friday, `18..21`
- `Event.canTrigger()` fields plus Amanda-specific conditions:
  - weekday is Friday;
  - current hour is inside `18..21`;
  - Friday dance slot active;
  - `FridayDancesCount < 5`;
  - `DanceStep == 0`;
  - Amanda has not left the dance;
  - dance table does not give Amanda to Legare for current dance count.
- Start:
  - set Amanda as dancing with MC through Amanda-owned dance state;
  - increment dance count;
  - set `DanceStep = 1`;
  - open `IntAmandaDance`.
- Continuations:
  - `AmandaAfterDanceMC`;
  - `AmandaAfterDanceMCMakeOut`;
  - `AmandaAfterDanceMCWalkHome`;
  - `AmandaSexDanceStreet`.

### AmandaFridayDanceLegareEvent

- Thread: `AmandaFridayDanceLegare`
- Current runtime: `story_amanda_friday_dance_legare_0`
- Start binding: `FridayDance / amanda_dance_legare`
- Time gate: Friday, `18..21`
- `Event.canTrigger()` fields plus Amanda-specific conditions:
  - weekday is Friday;
  - current hour is inside `18..21`;
  - Clara/Clarissa is not at `FridayDance`;
  - Friday dance slot active;
  - `FridayDancesCount < 5`;
  - `DanceStep == 0`;
  - Amanda has not left the dance;
  - dance table gives Amanda to Legare for current dance count.
- Start:
  - set Amanda as dancing with Legare through Amanda-owned dance state;
  - create Legare dance;
  - increment dance count;
  - handle `EscapeUnnoticed`;
  - open `IntAmandaDance`.

### AmandaTavernSeductionEvent

- Thread: `TavernSeductions`
- Current runtime: `story_amanda_tavern_seduction_0`
- Start binding: `TavernMain / enter`
- Time gate: Monday, Tuesday, Wednesday, Thursday, Saturday; `12..21`
- Probability: `0.35`
- `Event.canTrigger()` fields plus Amanda-specific conditions:
  - Amanda is in `TavernMain`;
  - not seen today;
  - Amanda friendship is at least `8`;
  - Amanda sluttiness is at least `25`;
  - Amanda has not kicked MC from her room.
- Start:
  - tavern flirt/seduction menu;
  - outcomes update Amanda mana and relationship stats or route to Amanda room/work consequence.
- Current cleanup need:
  - replace `amanda_tavern_seduction_ready()` with event fields plus `AmandaTavernSeductionEvent.checkAmandaConditions()`, without duplicating `Event.canTrigger()`.

### AmandaLizaWorkTalkEvent

- Thread: `LizaWorkTalk`
- Current runtime: `story_amanda_liza_talk_work_0`
- Start binding: `TavernMain / tavern_work`
- Time gate: Monday through Saturday; `12..17`
- `Event.canTrigger()` fields plus Amanda-specific conditions:
  - tavern work planner has an Amanda/Liza talk row for current location/time.
- Start:
  - pop the planned tavern-work event;
  - call the Amanda/Lizett talk scene.
- Source:
  - original Amanda/Lizett talk content must remain aligned with source text unless explicitly rewritten.

### AmandaTalkHubEvent

- Thread: `TalkHub`
- Current runtime: `story_amanda_talk_hub_0`
- Start binding: `talk / amanda`
- Time gate: none
- `Event.canTrigger()` fields plus Amanda-specific conditions:
  - Amanda's current location equals MC current location.
- Start:
  - call `IntAmandaTalk("amanda")`.
- Current cleanup need:
  - talk hub can stay as event entry, but refresh/apply/restore style labels should not be treated as model architecture.

### AmandaDressChangeEvent

- Thread: `DressChange`
- Current runtime: `story_amanda_dress_change_0`
- Start binding: `talk_amanda / dress_change`
- Time gate: none
- `Event.canTrigger()` fields plus Amanda-specific conditions:
  - Amanda has dress-change options.
- Start:
  - call Amanda dress-change interaction.

### AmandaRoomNightApproachEvent

- Thread: `RoomNightApproach`
- Current runtime: `story_amanda_room_grope_0`
- Start binding: `TavernAmandaRoom / amanda_grope`
- Time gate: any day, `18..23`
- `Event.canTrigger()` fields plus Amanda-specific conditions:
  - current time is night;
  - MC has not exceeded daily cum/action limit.
- Start:
  - call `TavernAmandaRoomGropeAction`.
- Current cleanup need:
  - condition currently lives in `tavern_amanda_bed_action_available()`;
  - final form should make it the event object's condition or an Amanda room/bed object method, not a floating wrapper.

### AmandaGloryHoleTryEvent

- Thread: `GloryHoleTry`
- Current runtime: `story_amanda_gloryhole_try_0`
- Start binding: `TavernGloryHole / amanda_gloryhole_try`
- Time gate: any day, `12..21`
- `Event.canTrigger()` fields plus Amanda-specific conditions:
  - current room is `TavernGloryHole`;
  - Amanda glory current state is at least `1`.
- Start:
  - call `AmandaAtGloryHole`.

### Removed External Intent Mini-Events

- Status: removed from Amanda runtime.
- Reason: the external intent layer duplicated Amanda state and bypassed the class/event model.
- Replacement:
  - Amanda decisions use `GirlDecisionModel`;
  - Amanda class owns `mana`, `rebellion`, cycle/body state, and need reactions;
  - bad outcome probability is `1 - Amanda.mana / 100`;
  - fulfilled needs call Amanda mana gain methods;
  - unmet needs call Amanda mana loss methods.
- Future Amanda room or breakfast story beats must be normal Amanda event/thread entries with explicit conditions, stage numbers, and labels.

### AmandaBirthEvent

- Thread: `Birth`
- Current runtime: `story_amanda_give_birth_0`
- Start binding: `TavernMain / enter`
- Time gate: none
- `Event.canTrigger()` fields plus Amanda-specific conditions:
  - `dayspassed > 0`;
  - Amanda pregnancy counter is at least `240`;
  - Amanda pregnancy father is set.
- Start:
  - call `GiveBirth("amanda")`.
- Current cleanup need:
  - birth state belongs to Amanda's data/info object; no separate global pregnancy authority for Amanda in final form.

### AmandaLegareTavernVisitEvent

- Thread: `LegareTavernVisits`
- Current runtime: `story_amanda_legare_tavern_visit_0`
- Start binding: `TavernMain / enter`
- Time gate: Monday, Tuesday, Wednesday, Thursday, Saturday; `18..21`
- Probability: `0.5`
- `Event.canTrigger()` fields plus Amanda-specific conditions:
  - Amanda is in `TavernMain`;
  - Alber/Legare is in `TavernMain`;
  - event not seen today;
  - Amanda Legare friendship is at least `5`;
  - Amanda is not prohibited from Alber/Legare.
- Start:
  - Legare visits Amanda at the tavern;
  - choices update Amanda/Legare relationship state and Amanda mana.

### AmandaStreetLegareSightingEvent

- Thread: `StreetLegareSightings`
- Current runtime: `story_amanda_street_legare_sighting_0`
- Start bindings:
  - `StreetTavern / enter`
  - `MarketPlace / enter`
- Time gate: Monday, Tuesday, Wednesday, Thursday, Saturday; `12..21`
- Probability: `0.25`
- `Event.canTrigger()` fields plus Amanda-specific conditions:
  - current location is `StreetTavern` or `MarketPlace`;
  - event not seen today;
  - Amanda has a `legarerun` sex-event row for current time.
- Start:
  - player sees Amanda sneaking toward Legare;
  - choices can follow into `AfterDanceSexLegare`, let her go, or send her back to work.

### AmandaStreetLoverEncounterEvent

- Thread: `StreetLoverEncounters`
- Current runtime: `story_amanda_street_lover_encounter_0`
- Start bindings:
  - `StreetTavern / enter`
  - `MarketPlace / enter`
- Time gate: Monday, Tuesday, Wednesday, Thursday, Saturday; `12..21`
- Probability: `0.2`
- `Event.canTrigger()` fields plus Amanda-specific conditions:
  - current location is `StreetTavern` or `MarketPlace`;
  - event not seen today;
  - Amanda has a `lovermeet` sex-event row for current time.
- Start:
  - player sees Amanda with another young man;
  - choices can approach into `AmandaLoverSex`, send her back to work, or ignore it.

## Continuations, Not Independent Event Classes

These labels are currently continuations/outcomes. They should not be listed as independent scheduled event classes until they receive their own event object.

- `IntAmandaDance`
- `AmandaAfterDanceMC`
- `AmandaAfterDanceMCMakeOut`
- `AmandaAfterDanceMCWalkHome`
- `AmandaAfterDanceMCReturn`
- `AmandaAfterDanceMCFinish`
- `AmandaSexDanceStreet`
- `AfterDanceLegare`
- `AfterDanceLegare_Fight`
- `AfterDanceLegare_Police`
- `AfterDanceSexLegare`
- `AmandaLoverSex`
- `EventAmandaLizettTalk`
- `EventAmandaLizettTalk2`
- `AmandaAtGloryHole`
- `TavernAmandaRoomGropeAction`

## Current Runtime Gaps To Fix Before Claiming Completion

- Event objects are not yet first-class Amanda classes in runtime; many are still tuple entries inside `amandaThreadList`.
- Several event conditions still live as external `*_ready()` wrapper functions.
- Some stage movement is implicit in labels and `thread.advance()` instead of explicit event/thread methods.
- Amanda AI mini-event queue and some night-bowl helper state still use global/store-style patterns and need ownership cleanup.
- TXT/reference content has not been exhaustively cross-checked in this index; this file only maps live runtime labels and intended OOP conversion targets.
