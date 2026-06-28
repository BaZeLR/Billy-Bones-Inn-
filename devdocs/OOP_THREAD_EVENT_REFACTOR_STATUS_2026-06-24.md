# OOP Thread/Event Refactor Status

Date: 2026-06-24
Project root audited: `C:\Users\blank\Documents\RenPy_Projects\Tractir`

Update: 2026-06-28

This document is now being updated from live code changes, not from planned
claims. It is a working status document: it tracks the current refactor stage
and known evidence, but it is not a complete per-file ownership index yet. That
index is still listed as Phase 2 work below.

Recent committed/runtime-data update:

- `c631876 Commit OOP runtime JSON data cleanup`
- committed only game JSON source data, not saves or compiled files;
- moved Alber and Eddie whore-visit schedule locations to
  `PortStreetsBackAlley`;
- removed old NPC custom-map JSON blobs for Becky and renamed Georgett/Liza
  custom story data to `story_vars`;
- removed the obsolete `Loc` mapping entry from `game/location_args_map.json`;
- left generated `game/saves/navigation.json` uncommitted.

Recent source cleanup in progress:

- `game/Inn/TavernKitchen.rpy` now routes the Sandra tea/breakfast/client
  request state changes through Sandra class methods instead of direct
  `Friends`, `Talked`, `AskedToday`, or `sluttiness` writes;
- `game/Inn/TavernKitchen.rpy` no longer imports Python `random`; kitchen
  picture and food-effect rolls use `procedural_choice` /
  `procedural_randint`;
- this kitchen source cleanup is not committed yet.

Becky vertical-slice cleanup started on 2026-06-28:

- `IngaVar` is no longer created or used in the Becky/Inga/BeckyHome files.
  Inga story state now belongs to `Inga.var` through `Inga.ensure_story_defaults()`,
  `Inga.var_int(...)`, `Inga.set_var_int(...)`, and
  `Inga.set_story_value_min(...)`.
- Becky home/front/dinner labels keep their authored story text and menu flow,
  but now read/write Inga recognition and Lucas-sex discovery state through the
  Inga object.
- Becky/Eddie bedroom and dinner consequence labels now mutate Eddie through
  `Eddie.change_social(...)` instead of `Friends["eddie"]`.
- Becky/Georgett/Inga dinner crossover social consequences now use
  `Inga.apply_social_chance(...)` and `Georgett.apply_social_chance(...)`.
- Becky class social rolls no longer import Python `random`; they use
  `procedural_randint(...)`.
- Becky class profile publication no longer mirrors social/daily state into
  old maps such as `Friends`, `sluttiness`, `Talked`, `AskedToday`,
  `TalkedToday`, `FlirtedToday`, `GiftedToday`, or `FuckedToday`.
- Robin state referenced by Becky Blackwood labels now uses `Robin.var`;
  `InitRobin.rpy` owns Robin defaults directly instead of `RobinVar`.
- Focused source search for this slice returned no hits for:
  `IngaVar`, `RobinVar`, `Friends[`, `sluttiness[`, `Talked[`,
  `AskedToday[`, `otkroven[`, `TalkedToday[`, `FlirtedToday[`,
  `GiftedToday[`, `FuckedToday[`, `Drunk[`, `Drunk.get`, `GetGirlDrunk`,
  `import random`, `random.`, or `SlutFriendsIncrease`.
- `renpy.exe . compile` passed after this slice.
- This source cleanup is not committed yet.

Becky/Grocery adjacent status:

- Eddie and Becky talk labels already use `vscene grocery_store_grocer_picture(...)`
  when `CurLoc == "GroceryStore"`.
- GroceryStore remains structurally mixed and is not fully converted:
  `GroceryStoreBuildActions`, `current_action_items`, `while _grocery_ui_return is None`,
  and `jump GroceryStore` loops remain.
- Existing `tests/test_grocery_store_source.py` is partially stale: it correctly
  flags the build/loop/store-menu problems, but still expects screen-state
  function wrappers such as `grocery_store_open_object_menu_state`, which
  conflicts with the current direct label/menu rule. Do not satisfy that test by
  adding wrapper state functions; update the test when the store is converted to
  simple Ren'Py menu labels.

Liza vertical-slice cleanup completed on 2026-06-28:

- All six live Liza source files were covered:
  `InitLiza.rpy`, `IntLizaTalk.rpy`, `IntLizaSex.rpy`,
  `IntLizaDressChange.rpy`, `IntLizettAfterCermon.rpy`, and
  `ShowLizaPortrait.rpy`.
- Liza social, daily, job, pregnancy, sex, arousal, cum, cock-position,
  visibility, and dress decisions now read/write the `Liza` object through
  class fields or methods such as `Liza.var`, `Liza.stats`, `Liza.jobs`,
  `Liza.sex_state`, `Liza.pregnancy_days()`, `Liza.cum_state(...)`,
  `Liza.job_value(...)`, `Liza.set_job_value(...)`, and
  `Liza.publish_visibility_state()`.
- `InitLiza.rpy` no longer imports relationship/job/stat/sex state from old
  external maps and no longer publishes Liza social/daily/job/stat state back
  into those maps. The remaining clothing projection maps in `sync_shared_state`
  are render-facing wardrobe projections for shared clothes helpers, not Liza
  state ownership.
- Liza sex flow now uses class-owned partner state and player arousal state for
  menu conditions and consequences.
- Liza portrait and church-after-sermon flow no longer read old visibility/cum
  or pregnancy maps.
- Liza tavern special-work adjacency now reads/writes class job values in
  `TavernMain.rpy`, `TavernRandomEvents.rpy`, `menu_tavernstat.rpy`,
  `ChangeTommorowWhoreJob.rpy`, and `NextDay_TavernDaily.rpy`.
- Amanda/Liza talk and Georgett/Liza birth text adjacency now check `Liza`
  directly instead of old global maps.
- Focused source searches returned no remaining Liza external ownership hits
  for `Friends`, `sluttiness`, `pregnancy`, `Arousal`, `Talked`,
  `jobwhore`, `jobgloryhole`, `CumInside`, `CockIn`, `PussyVisible`, or
  `TitsVisible`.
- `renpy.exe . compile` passed after this slice.
- Not yet claimed: full real click-route QA and old-save migration for every
  Liza route.

Clara/Robin vertical-slice cleanup completed on 2026-06-28:

- Clara source files and direct Clara thread files were checked:
  `InitClara.rpy`, `IntClaraTalk.rpy`, `ClaraBookletMarketThread.rpy`,
  `ClaraTavernVisitThread.rpy`, and `ClaraPaintingsThread.rpy`.
- Clara no longer imports Python `random` or uses `renpy.store` in her runtime
  helper logic. Wine-store and forest image selection now use
  `procedural_choice(...)`.
- Clara/Melissa visit and tavern visit checks now read Robin safety state from
  `Robin.var_int("MongolSafePass")` rather than any old `RobinVar` map.
- Clara talk flow now uses `IntClaraTalkMenu` as the direct talk-menu owner.
  The former `IntClaraTalkRefresh` name was removed from Clara call paths.
- Clara talk and tavern visit media beats now use `vscene`, including dynamic
  Clara picture paths.
- The Clara market/Mongol release thread now mutates Zimmer through
  `Zimmer.change_social(...)` instead of `Friends["zimmer"]`.
- Robin source and direct Blackwood adjacency were checked:
  `InitRobin.rpy`, `IntRobinTalk.rpy`, `SherwoodTravel.rpy`,
  `BeckyEvents.rpy`, `IntZimmerTalk.rpy`, and Clara helper adjacency.
- `RobinInfo` now owns explicit integer story-state methods:
  `var_int(...)`, `set_var_int(...)`, `add_var_int(...)`, and
  `set_var_min(...)`.
- Robin talk, Blackwood road events, Becky Blackwood followups, Zimmer complaint
  availability, and Clara/Melissa visit checks now read/write Robin story state
  through those methods instead of direct `Robin.var[...]` / `Robin.var.get(...)`
  code.
- Focused source searches returned no remaining Clara/Robin external ownership
  hits for `ClaraVar`, `ClarissaVar`, `RobinVar`, `Friends`, `sluttiness`,
  `pregnancy`, `Arousal`, `Talked`, old visibility/cum/cock-position maps,
  `renpy.store`, or Python `random` in the checked Clara/Robin files.
- `renpy.exe . compile` passed after this slice.
- Not yet claimed: full real click-route QA and old-save migration for every
  Clara/Robin route.

Earlier cleanup stage removed the werecat story globals:

- `WerecatVar` was removed as an external story-state dict.
- Werecat story flags now live on `peopleInfo["werecat"].var`.
- Werecat pet interaction counters now live on `peopleInfo["werecat"].stats`.
- Werecat event/thread conditions, breakfast checks, daily rat-food loss, Clara
  gift checks, Melissa rat hooks, and werecat forest trap labels read/write the
  werecat NPC state owner.
- `game/NPC/Secondary/MelissaWerecatQuest.rpy` no longer imports Python
  `random`; search/trap rolls use the project deterministic random helper.
- The external click-test harness was adjusted to use `werecat_state()` instead
  of the deleted global dict.

Validation for the werecat stage:

- `rg -n "WerecatVar|WerecatNPCState" game tests tools -g "*.rpy" -g "*.py"`
  returned no hits.
- `renpy.exe . compile` passed after the conversion.

This is the corrected status report for the OOP/thread/event refactor. It
updates the previous report where it overstated several points.

The audit uses live `.rpy` code, current `devdocs`, direct source searches, and
focused validation where available. The document must be corrected whenever
source checks contradict a previous claim.

## Corrected Verdict

The refactor is real and significant, but not complete.

The following systems are already in the intended shape or close to it:

- NPC visibility is not room-owned. It is derived from NPC class/schedule state
  through `getLocation()` / `getNPCids(current_location)` and rendered by the
  screen.
- Core people/NPC classes exist and are used.
- Class-owned dictionaries such as `self.var`, `self.stats`, `self.jobs`, and
  `self.sex_state` are valid OOP state. They must not be counted as legacy just
  because they are dictionary-shaped.
- Event/thread runtime exists and has real condition checking.
- Room template runtime exists and rooms use `CurrentRoom` / `CurLoc` as the
  current player-location state.

The project is still mixed because some old external globals, bridges,
dispatchers, and compatibility paths remain. Tavern business variables are an
explicit temporary exception and should not be treated as a blocker in this
report unless they leak into NPC/event/room ownership.

## Intended Architecture

### People And NPCs

`PeopleData` is person definition data: display name, code name, portrait,
description, default location/schedule, preferences, and other mostly-static
definition fields.

`PeopleInfo`, `Girl`, and NPC subclasses are runtime state: relationship stats,
jobs, variables, sex state, daily counters, schedule/location logic, and methods.

Valid converted state includes:

- `Amanda.var`
- `Amanda.stats`
- `Amanda.jobs`
- `Georgett.var`
- `Georgett.sex_state`
- `Liza.jobs`
- `npc.getLocation(...)`
- `npc.reset_daily(...)`

Invalid old ownership is external state that still owns or mirrors an NPC after
that NPC has a class owner, such as old `Friends[...]`, `sluttiness[...]`,
`AmandaVar`, `HadSex`, or other global maps used as the authoritative source.

### Rooms And NPC Visibility

Rooms do not own NPC presence.

The live intended flow is:

1. Room label sets `CurrentRoom` and `CurLoc`.
2. Screen determines the current location from `CurLoc` / `CurrentRoom`.
3. Screen calls `getNPCids(current_location)`.
4. `getNPCids(...)` iterates `peopleInfo`.
5. Each NPC instance answers through `info.getLocation(...)`.
6. The screen renders the matching NPCs in the visible NPC area.
7. Clicking an NPC opens that NPC interaction/card/talk flow.

Concrete live-code evidence:

- `RoomTemplate.rpy` defines `Room` as room structure, not NPC ownership.
- `RoomTemplate.rpy` drops stale saved `npcs` state with `state.pop("npcs", None)`.
- `PeopleRuntime.rpy` defines `PeopleData.getLocation(...)`.
- `PeopleRuntime.rpy` defines `PeopleInfo.getLocation(...)`.
- `PeopleRuntime.rpy` defines `getNPCids(location, ...)` by comparing each
  `info.getLocation(...)` result to the current room code.
- `main_layout.rpy` builds visible NPC rows from `getNPCids(current_location)`.

This part should be marked done as an architecture target. Bugs in individual
NPC schedules or story-state overrides are per-NPC issues, not evidence that
rooms own NPCs.

### Events And Threads

Event/thread availability belongs to the event/thread runtime.

Event labels own:

- authored text;
- `vscene` or explicit media beats;
- menu choices;
- state mutation;
- time cost;
- `thread.advance()`, `thread.complete()`, or `thread.abort()`;
- return or jump to the next real owner.

Screens render UI only. They do not own story logic.

### Tavern Variable Exception

Tavern business variables may remain globals for now. They should not be listed
as refactor blockers in this report unless they are used as a substitute for
NPC class state, event/thread state, room state, or object/item state.

## Done So Far

### NPC Visibility Pipeline

Done at the architecture level.

Live code uses `getNPCids(current_location)` and `getLocation()` rather than a
room-owned NPC list. The report should no longer say that visible NPCs are an
unresolved room ownership target.

Remaining work here is local:

- fix wrong NPC schedule/location results;
- fix story flags that temporarily move or hide an NPC;
- fix talk/card buttons for a visible NPC;
- fix port/back-alley sublocation logic where an NPC should be in `BackAlley`
  and not visible in `PortStreets`.

Those are implementation bugs, not architecture absence.

### Core Class Runtime

Done as foundation.

Preserve these systems:

- `game/Utilities/General/NPC/PeopleRuntime.rpy`
  - `peopleData`
  - `peopleInfo`
  - `PeopleData`
  - `PeopleInfo`
  - `BaseNPC`
  - `Girl`
  - `getLocation(...)`
  - `getNPCids(...)`
  - class-owned `var`, `stats`, `jobs`, `sex_state`
- `game/Utilities/General/Player/Player.rpy`
  - player state classes for inventory, equipment, appearance, intimacy,
    combat, chores, and tavern management
- `game/Utilities/General/Classes/RoomTemplate.rpy`
  - `Room`
  - `RoomSchedule`
  - `RoomExit`
  - `RoomDescription`
  - room registration
- `game/Utilities/General/Events/`
  - `Event`
  - `ThreadData`
  - `ThreadInfo`
  - event conditions
  - thread progress
  - event selection

### Character Class Definitions

The following class surfaces exist and are part of the real refactor:

- Amanda: `game/NPC/Girls/Amanda/InitAmanda.rpy`
- Becky: `game/NPC/Girls/Becky/InitBecky.rpy`
- Melissa: `game/NPC/Girls/Melissa/InitMelissa.rpy`
- Sandra: `game/NPC/Girls/Sandra/InitSandra.rpy`
- Clara: `game/NPC/Girls/Clara/InitClara.rpy`
- Georgett: `game/NPC/Girls/Georgett/InitGeorgett.rpy`
- Liza: `game/NPC/Girls/Liza/InitLiza.rpy`
- Irma: `game/NPC/Girls/Irma/InitIrma.rpy`
- Inga: `game/NPC/Girls/Inga/InitInga.rpy`
- Eddie: `game/NPC/Secondary/InitEddie.rpy`
- Eddie talk: `game/NPC/Secondary/InitEddieTalk.rpy`
- Alber: `game/NPC/Secondary/InitAlber.rpy`
- Zimmer: `game/NPC/Secondary/InitZimmer.rpy`
- Mongol: `game/NPC/Secondary/InitMongol.rpy`
- Robin: `game/NPC/Secondary/InitRobin.rpy`
- Draupnir: `game/NPC/Secondary/InitDraupnir.rpy`
- Francheska: `game/NPC/Secondary/InitFrancheska.rpy`

Class existence is completed foundation work. Final conversion for each NPC
still requires verifying that adjacent story/talk/sex/event labels mutate the
class owner, not an external old map.

### Amanda Runtime State

Amanda's active runtime source is now ahead of the older report text:

- `AmandaDynamicCommonBlocks.rpy` was removed from active source;
- active Amanda `.rpy` files use the `AmandaInfo` / `AmandaData` model;
- Amanda story counters and flags are owned by `Amanda.var`;
- Amanda social and sex state mutations route through Amanda methods;
- Amanda active files no longer contain `AmandaVar`, `Friends[...]`,
  `sluttiness[...]`, `Talked[...]`, `AskedToday[...]`, `globals()`, or
  `renpy.store` references.

Remaining Amanda work is no longer "remove the old dynamic common blocks".
The remaining work is stricter gameplay verification:

- verify each Amanda event label advances the correct event/thread stage;
- verify every Amanda talk, dance, room, Liza/glory, pregnancy, and sex route
  returns through the intended visible UI path;
- verify save/load keeps `Amanda.var`, pregnancy, sex, mana, and thread state
  intact without reinitializing or needing compatibility bridges.

### Event/Thread Runtime

Done as foundation.

Live code contains:

- `Event.canTrigger(...)`;
- event condition checks;
- `ThreadData`;
- `ThreadInfo`;
- thread progress and available-event selection;
- condition helpers such as `makeCondition(...)` and
  `_story_conditions_met(...)`.

This is not a missing system. Remaining work is moving old parallel event paths
onto the existing system and keeping authored labels direct.

## Still Not Complete

### External Global Bridges

This is still a real problem.

Concrete examples from live code:

- `PeopleRuntime.initPeople()` can attach legacy `AmandaVar`-style dicts as
  `.var` unless an object opts out.
- `InitLiza.rpy` has been cleaned for Liza-owned relationship/job/stat/sex
  state; do not list Liza as evidence for this blocker unless a new source
  search finds a specific external owner.
- some sex/daily flows still read or mutate old globals such as `HadSex`,
  `Friends`, `sluttiness`, `CockPosition`, and daily stat maps.

Correct rule: if the dict is inside the class instance, it is valid OOP state.
If the dict is external global ownership or a compatibility mirror, it must be
removed or bypassed.

### Parallel Event Paths

Event/thread runtime exists, but not all event-like systems use it.

Known remaining surfaces:

- `CheckDailyEvent.rpy` still dispatches from daily event lists.
- `RoomEnterEventGate` still combines `checkTriggers` with daily/household
  hooks.
- some tavern/household/random town paths still behave like separate event
  schedulers.
- `ShowImage` compatibility labels still exist and are used by some story/event
  content instead of authored `vscene` beats.

### Procedural Random Source

The project has `procedural_choice(...)` and `procedural_randint(...)`, but not
all active code uses them yet.

Kitchen was cleaned in the current source pass, but direct Python random calls
still remain in active surfaces such as:

- `game/Utilities/Fight/FightSystemRuntime.rpy`;
- `game/Utilities/Fight/FightResult.rpy`;
- `game/Forest/Forest.rpy`;
- `game/NPC/Secondary/DogCompanion.rpy`;
- `game/NPC/Girls/Common/MorningSickness.rpy`;
- `game/Inn/HouseholdRuntimeEvents.rpy`;
- `game/Inn/TavernGloryHole.rpy`;
- `game/Inn/TavernKitchenBreakfast.rpy`;
- `game/Inn/menu_tavernstat.rpy`;
- `game/Town/BeckyHome.rpy`;
- `game/Town/Temple/GiveBirth.rpy`;
- `game/Utilities/General/Screens/stat.rpy`;
- `game/NPC/Girls/Clara/InitClara.rpy`;
- `game/NPC/Girls/Becky/BeckyEvents.rpy`;
- `game/NPC/Girls/Becky/InitBecky.rpy`.

These are not all equivalent in risk. Fight, forest, sex/pregnancy, and
schedule/visit paths should be converted before claiming deterministic
procedural random compliance.

Tavern business globals are allowed temporarily, but tavern story events should
still move toward the canonical event/thread path.

### Room/Object Action Cleanup

Room template exists. The remaining issue is not that rooms own NPCs; they do
not. The issue is that many rooms still contain old action-building patterns
that need classification.

Examples of surfaces to classify:

- `TavernMainBuildActions`
- `TavernKitchenBuildActions`
- `TavernAmandaRoomBuildActions`
- `TavernMyRoomBuildActions`
- `GroceryStoreBuildActions`
- `ForestBuildActions`

Do not delete these blindly. Some contain real room action menus. For every
touched label:

- KEEP: real room entry, object menu, object action, NPC interaction,
  event/story label, returnable procedure.
- REMOVE/BYPASS: refresh, rebuild, wrapper, handler-for-one-action,
  dispatcher, duplicate Python method, recursive menu self-loop, label made
  only for room redraw.

### Sex System

The sex system is partially converted but not clean.

Correct class-owned pieces:

- `PeopleInfo.sex_state`;
- NPC-specific `self.sex_state`;
- class-owned sex stats and story flags.

Remaining old pieces:

- old globals such as `HadSex`;
- old helper state such as `CockPosition`;
- story labels that still mutate old maps;
- some screens/labels that do not preserve the intended full main UI flow;
- Georgett port-street sex flow still needs complete event-driven,
  class-owned verification against TXT flow.
- Liza sex flow has been moved to class-owned partner/player state, but still
  needs real click-route verification and save/load verification before being
  marked fully complete.

### Fight System

The fight system still needs a separate completion audit and click verification.

This report does not claim fight is complete. Completion requires:

- fight session ownership;
- enemy/player stats visible;
- move-by-move flow;
- escape/loss/victory consequences;
- loot updates;
- time cost;
- save/load stability;
- real click test through the gameplay entry points.

### Save/Load Migration

Still not solved at project level.

Required direction:

- do not recreate saved NPC/item/room instances blindly after load;
- add missing attributes to existing saved objects through owner migration;
- do not duplicate objects such as the shed axe;
- verify old save load after source changes.

## Updated Work Plan

### Phase 1: Correct The Report And Docs

Done by this document:

- mark visible NPC rendering as class/schedule/getLocation driven;
- stop treating class-owned dicts as unconverted;
- keep tavern business globals as temporary exception;
- flag only concrete external bridge/fallback ownership.

### Phase 2: Build A Live Ownership Index

Create a small index with one row per subsystem:

- NPC state;
- NPC location/visibility;
- event/thread;
- room;
- object/game item;
- sex engine;
- fight session;
- save/load migration;
- shops;
- tavern business globals.

Each row should say:

- source owner;
- live files;
- legacy external owners still present;
- next file to convert;
- click/save-load test path.

### Phase 3: Finish One Vertical Slice

Recommended first slice: `PortStreets` + `BackAlley` + Georgett/Liza.

Acceptance:

- `PortStreets` and `BackAlley` use room template correctly.
- Georgett and Liza visibility comes from class `getLocation()`.
- Back Alley is a real sublocation, not a text-only branch.
- Eddie/Alber whore visits use NPC/event state and are visible only in the
  correct location.
- Georgett sex flow must use class-owned partner state and player state.
- Liza sex/dress source no longer contains focused old-map ownership hits, but
  the real PortStreets/BackAlley click route still needs verification.
- Original TXT flow/content is preserved.
- Menus render through the intended full main UI event flow.
- Daily seen/client flags reset through class/event owner.
- Time cost is applied.
- Save/load does not corrupt menus or duplicate objects.
- External click test covers the real route.

### Phase 4: Convert NPCs One At A Time

For each NPC:

1. Confirm class exists.
2. Confirm class-owned `var`, `stats`, `jobs`, `sex_state`, and daily counters.
3. Remove external old global mirrors for that NPC.
4. Convert talk/event/sex/dress/schedule labels to mutate the class owner.
5. Remove old tests that prove only global dict compatibility.
6. Add or run a real UI click path.

### Phase 5: Move Parallel Events Into Canonical Runtime

Use existing event/thread classes; do not invent another event engine.

Move daily/household/random/story paths into event availability checks and
direct authored event labels.

### Phase 6: Save/Load Migration

Add owner-level after-load migration. This is required before the project can
be considered stable for normal development.

## Current Completion State

Completed or mostly completed:

- NPC visibility architecture.
- Core people/NPC class foundation.
- Player class foundation.
- Room class foundation.
- Event/thread class foundation.
- Many NPC class definitions.
- Some event labels using `thread.advance()` / `thread.complete()`.
- Amanda active source class ownership, after deletion of old dynamic common
  blocks.

Partially completed:

- Amanda full story/event/sex/dance click-route verification.
- Tavern kitchen Sandra request labels and food-effect random source cleanup.
- Becky full class/event conversion.
- Melissa/Sandra events and tavern flows.
- Clara church/dress/sex/event flow.
- Georgett port-street and sex flows.
- Liza source OOP conversion, pending real click-route/save-load verification.
- Clara source OOP cleanup for talk, image random, tavern/market/paintings
  adjacency, pending real click-route/save-load verification.
- Robin source OOP cleanup for Blackwood story state and direct adjacency,
  pending real click-route/save-load verification.
- secondary NPC class conversion.
- object/game-item catalog.
- shop menus and item ownership.
- room/object action cleanup.
- event-label media conversion to `vscene`.

Not completed:

- full removal of external NPC legacy globals/bridges;
- full removal/bypass of refresh/rebuild/apply/compat dispatchers;
- full canonical event/thread conversion;
- full sex engine class ownership;
- full fight system completion;
- full save/load migration;
- full real click-route QA matrix.

## Acceptance Rule Going Forward

Do not claim a module is converted because a class file exists.

A module is converted only when:

- state belongs to the class/room/event/item owner;
- no external old map owns the same state;
- no wrapper/bridge/fallback is required for normal flow;
- labels are direct and readable;
- event labels own their own text/media/menu/consequence;
- visible NPCs resolve through `getLocation()` / `getNPCids(...)`;
- the real UI click path works;
- save/load works if saved state is touched.
