# Full OOP Port Execution Plan

Status: active, incomplete  
Goal: a healthy working game with every existing logical feature preserved and one authoritative owner for every mutable state domain.

## Binding rules

1. Live `.rpy` behavior is the runtime authority. Devdocs define architecture. Git and TXT references preserve existing wording, choices, numbers, gates, and flow.
2. Do not redesign screens, menus, navigation, story flow, prices, schedules, quests, reputation, or content while changing ownership.
3. Work one complete vertical slice at a time. Do not begin the next slice until the current slice passes its deletion and behavior gates.
4. A new owner is not complete while an old writer, mirror, compatibility alias, synchronization path, duplicate registry, wrapper, dispatcher, or test remains.
5. Event labels own `vscene`, dialogue, native `menu:`, consequences, and thread advancement. Screens are UI-only. The main HUD remains persistent.
6. `call` is for returnable procedures. `jump` is for story or location continuation. Navigation must not be used as submenu refresh.
7. Tests must exercise preserved behavior. A source-shape test cannot prove a screen, event, purchase, schedule, or navigation path works.

## Completion gate for every task

A task is complete only when all answers are yes:

- Is the original feature behavior mapped from live code, Git, devdocs, and relevant TXT?
- Does exactly one object own every mutable value touched by the slice?
- Were all old writers and obsolete state containers deleted?
- Were derived collections changed to computed views instead of saved mirrors?
- Were wrappers, rebuild/refresh labels, dispatchers, recursive menu loops, and hidden fallbacks removed?
- Are text, menu order, gates, costs, rewards, schedules, pictures, quests, and navigation unchanged?
- Do focused source tests pass?
- Does the real Ren'Py click/dialogue path pass?
- Does Ren'Py compile and lint pass?
- Does the residual scan return zero forbidden references for the completed slice?

Failure of any gate keeps the task in progress.

## Task 0 - Regression recovery and baseline

Purpose: stop further architectural work from hiding existing damage.

- [x] Restore Hunter Club purchase/sell screen flow and preserve reputation/challenges.
- [x] Restore first Market entry event execution.
- [x] Remove synthetic Hunter and Market objects.
- [x] Prevent duplicated simultaneous HUD/dialogue text.
- [x] Verify full source suite and Ren'Py lint.
- [ ] Run the complete click-play suite and record every failing gameplay path.
- [ ] Classify each failure by owner; do not patch it from an unrelated layer.

## Task 1 - MC ownership freeze

Owner: `player = Player()`.

- [x] Economy, condition, stats, inventory, equipment, appearance, intimacy, chores, tavern management, horse, combat membership, and history are Player-owned.
- [x] Scalar MC state defaults and reverse synchronization are absent.
- [x] Navigation does not stack previous room calls.
- [x] Room exits charge their exact declared time.
- [x] Exploration progression uses Player state.
- [ ] Run save/load/new-game MC parity paths before declaring the slice frozen.

Do not change Player structure after freeze unless a failing preserved feature proves the owner is incomplete.

## Task 2 - People registry cutover

Owner: `people = PeopleRegistry()`.

Current accidental parallel surfaces: `peopleData`, `peopleInfo`, `girls`, `secondary_npcs`, individual registration blocks, and SaveSync reconstruction.

Execution order:

1. Implement `PeopleRegistry` with one runtime-object map and one static-definition map.
2. Make girl/secondary group queries computed views of the runtime map; never save separate membership lists.
3. Give the registry one `register(static_data, runtime_object)` operation.
4. Migrate lookup APIs (`getPersonInfo`, `getPeopleData`, location queries, cards, schedules, debug tools) to the registry.
5. Migrate every NPC initializer to one registration call.
6. Migrate direct `peopleInfo[...]` and `peopleData[...]` consumers.
7. Migrate daily loops from saved `girls`/`secondary_npcs` lists to computed registry views.
8. Change save repair to validate the registry, not rebuild parallel collections.
9. Delete `peopleData`, `peopleInfo`, `girls`, `secondary_npcs`, their reconstruction helpers, and tests that require them.
10. Residual gate: zero runtime references to the four deleted globals.

Runtime acceptance:

- New game initializes every NPC exactly once.
- Save/load preserves object state and class type.
- NPC cards and right-side actions open correctly.
- `getLocation`, room visibility, and schedules agree at boundary hours.
- Girl and secondary daily processing includes every intended NPC exactly once.

## Task 3 - NPC vertical slices

Complete in this order because later stories depend on earlier household state:

1. Sandra
2. Melissa
3. Amanda
4. Clara
5. Becky and Inga
6. Liza and Georgett
7. Irma
8. Eddie
9. Mongol, Robin, Zimmer, Alber, Draupnir, Francheska
10. Gerhard, Luisa, Sergio, Lucas, Clara's fiance, Sergio's pet, dog, werecat

For each NPC, map and preserve:

- identity and static data;
- relationships, openness/corruption, skills, clothing, pregnancy, children, and daily counters;
- schedule intervals and conditional locations;
- talk topics and native menu order;
- room presence and action entry points;
- quests, reputation effects, event conditions, thread stages, and consequences;
- save/load behavior.

Delete in the same NPC slice:

- `*Var` or secondary state maps;
- schedule JSON/runtime duplication;
- simple boolean story mirrors when a thread stage or owned value already represents the fact;
- compatibility properties and reverse synchronization;
- wrapper/apply/refresh/dispatcher labels;
- tests that assert obsolete architecture.

## Task 4 - Room registry cutover

Owner: `rooms = RoomRegistry()`.

1. Register every Room once by `code_name`.
2. Migrate room lookup, movement, current-room restoration, debug, and save code.
3. Keep `CurrentRoom` only as transient UI/navigation context, never a second room-state owner.
4. Migrate global `*Room` state access to registry lookup or a local room reference.
5. Delete duplicate room maps, reconstruction, and compatibility lookup paths.
6. Residual gate: one registered instance per room code and no duplicate mutable room state.

## Task 5 - Location vertical slices

Complete each location independently:

1. Tavern main floor and bar
2. Kitchen, hearth, cauldron, breakfast, and Sunday dinner
3. Player room, attic, upstairs bedrooms, storage, stable, shed, backyard
4. Street and Market
5. Grocery, wine, Hunter Club, City Guard
6. Artisans Quarter, Irma's shop, barber, carpenter
7. Church and temple
8. Port streets and homes
9. Forest and every subroom

For each location preserve exact descriptions, objects, exits, time costs, schedules, events, NPC actions, pictures, purchases, and navigation. Remove only objects or menus proven to be synthetic redundancy.

## Task 6 - Event ownership

Owners: `events = StoryEventRuntimeState()` and `daily_events = DailyEventRuntime()` with distinct responsibilities and no duplicate progress facts.

1. Inventory every event condition, thread stage, daily schedule, and boolean flag.
2. Replace boolean mirrors with the authoritative thread stage or entity-owned value.
3. Keep authored story flow inside labels using native menus.
4. Remove detached event screens, action queues, handler labels, and return-to-room jumps used as refresh.
5. Ensure an event fires, advances, completes, and retries exactly as before.
6. Verify first-entry, daily, breakfast, household, dance, harassment, pregnancy, and quest event families.

## Task 7 - System roots

Complete and freeze one system at a time:

1. `calendar_v2 = Calendar()` - sole time/date authority; no hour/week/day mirrors.
2. `fight = FightInfo()` and `hunt = HuntInfo()` - combat/hunt state and outcomes.
3. `household = HouseholdInfo()` - household AI decisions and morning issues.
4. `crafting = CraftingInfo()` - recipes, batches, resources, and completion state.
5. `tractir_progress = TractirProgressRuntimeState()` - achievements/endings/progress.

For every system: migrate all readers/writers, delete mirrors and compatibility synchronization, then run its complete gameplay family before proceeding.

## Task 8 - UI, menus, and navigation audit

- Native authored menus appear inside the persistent main UI action area.
- Room/object panels use `current_action_items`; story choices do not.
- No unexpected overlay, replacement catalog, vertical scrolling, or screen redesign remains unless it existed in the approved design.
- Dialogue outcomes do not jump into a location merely to refresh UI.
- Submenu Back actions restore the current context without re-entering the room or charging time.
- Introduction and Irma screens remain unchanged unless a separately reproduced defect requires a surgical fix.

## Task 9 - Final deletion and release gate

Run residual searches for:

- legacy scalar authorities;
- `*Var` and duplicate state maps;
- `peopleData`, `peopleInfo`, `girls`, `secondary_npcs`;
- duplicate room/event registries;
- reverse sync and compatibility aliases;
- rebuild/refresh/apply/handler/dispatcher wrappers;
- recursive menu loops;
- detached contexts;
- dynamic global evaluation;
- duplicate object IDs and redundant menu objects.

Final acceptance:

1. Full source suite passes.
2. Full click-play suite passes.
3. Ren'Py compile and lint pass.
4. New game, representative mid-game save, and after-load repair pass.
5. Hunter purchases/reputation/quests, Market first entry, Irma purchases, breakfast, schedules, combat, crafting, household events, and representative NPC story threads pass visually.
6. Residual scans are zero or contain only explicitly documented Ren'Py UI context variables—not second gameplay authorities.
7. Only then may the full OOP goal be marked complete.
