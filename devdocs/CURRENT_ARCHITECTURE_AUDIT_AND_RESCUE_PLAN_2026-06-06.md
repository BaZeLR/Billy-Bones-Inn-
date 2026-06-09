# Tractir Current Architecture Audit And Rescue Plan

Date: 2026-06-06

Status: evidence-backed architecture proposal, updated with the Family Life-style findings from the follow-up audit. No gameplay code was changed during this audit.

## 1. Executive Assessment

Tractir is recoverable. Its authored content, navigable rooms, shops, item definitions, selected schedules, combat prototype, and several event threads still work. The failure is not absence of features. The failure is that features have been added through multiple competing runtime paths without completing ownership replacement.

The project currently has reusable OOP foundations:

- `Room`, `RoomExit`, `RoomDescription`
- `GameItem`, `GameObject`
- `PeopleData`, `PeopleInfo`, `BaseNPC`, `Girl`
- `Event`, `ThreadData`, `ThreadInfo`
- `FightEnemyDefinition`
- `Calendar`

However, most of these objects are not the single source of truth. They coexist with legacy maps, scalar mirrors, generated caches, wrapper labels, dispatcher layers, room-specific rebuild labels, and direct store mutations.

The result is a hybrid where:

- an object may exist but not own its state;
- a map may be called legacy but still control runtime behavior;
- a screen may display one source while labels mutate another;
- a schedule may be defined in JSON, `.rpy`, daily plans, and `CurrentLoc`;
- an event may be represented by a thread tuple, a daily event row, household AI, an NPC mini-event selector, or a tavern event queue;
- compile and narrow tests pass while ordinary click navigation still reaches undefined state.

This is not solved by adding adapters. It requires controlled replacement, one subsystem at a time, with deletion of the displaced path in the same phase.

Follow-up design correction:

- Do not rescue the project by consolidating wrappers into cleaner wrappers.
- Do not preserve refresh/apply/renew/rebuild labels as architecture.
- Do not preserve Python dispatcher methods that duplicate simple Ren'Py labels.
- Use the Family Life-style semantic model: real room labels, real object/action labels, real NPC talk labels, real event labels, direct state mutation at the choice/action point, and screens that display state.
- Current compatibility layers may remain only until their owning slice is migrated.

## 2. Verified Baseline

### Project size and structural signals

- 327 `.rpy` files in the audited `game/` and supporting paths.
- 751 class/default/define declarations.
- 1,049 labels.
- 2,210 Python function definitions.
- 916 matches involving `globals()`, `renpy.store`, `store`, or `setdefault`.
- 171 empty dictionary definitions.
- `script.rpy` alone owns 149 `default` declarations.
- 98 room-flow labels named as `BuildActions`, `ObjectMenu`, `ObjectText`, `Restore`, or `Refresh`.
- 382 direct `renpy.random` calls remain outside the intended shared random helpers.

### QA baseline

- Ren'Py compile: passed.
- `pytest -q`: 17 passed.
- `tools/runtime_logic_tests.py`: 0 failures, 3 warnings.
- `tools/random_town_event_flow_test.py`: passed.
- Representative external click tests passed for people objects, schedule/room agreement, event tuple audit, random town event click, fight flow, and debug builder surfaces.
- `external_room_action_dispatch` failed during actual navigation with:

```text
NameError: name 'DanceSponsor' is not defined
game/Inn/TavernKitchen.rpy:1104
```

Conclusion: current tests prove selected code paths, not a complete playable initialization contract. Compile success is not sufficient.

## 3. Reference Model: Family Life

The useful Family Life architecture is simple:

```text
define static definitions
default saved runtime objects
derived registries rebuilt from named runtime objects
central deterministic schedule lookup
static thread/event definitions
saved thread progress
central eligibility checking
labels present scenes and explicitly advance thread state
screens display and return intent
```

Relevant reference patterns:

- `PeopleData`: static NPC definition.
- `PeopleInfo`: saved mutable NPC state.
- Named `default` NPC runtime instances.
- `peopleInfo` rebuilt as a lookup collection referencing those same instances.
- `PeopleData.getLocation()` is the schedule path.
- `Event.canTrigger()` is the eligibility pipeline.
- `ThreadData` is static structure; `ThreadInfo` is saved progress.
- Event labels explicitly advance, complete, or abort the active thread.

Tractir should use these ownership principles, not copy Family Life's game-specific data or its old procedural limitations.

Additional Family Life findings now considered binding:

- Family Life basic actions are labels. They show/select pictures, write text, mutate stats/time/items/state, then return to the caller.
- Family Life does not use refresh/apply/renew labels for basic actions.
- Family Life event files keep choices in classic `menu:` blocks inside the event label. The picture/text stays visible while choices are made.
- Multi-picture events are repeated authored beats in the same label or real branch labels, using explicit `Continue`/`Продолжить` menus only when the author wants a pause.
- Family Life sets the active `thread` in `preEvent(thread_name)`; content labels then use `thread.advance()`, `thread.complete()`, or `thread.abort()` directly.
- Dialogue/talk actions are event-like NPC labels. Talk/flirt/gift/questions are visible choices in the NPC talk label or real sublabels called by it.

## 4. Current Source-Of-Truth Matrix

| System | Claimed/intended owner | Actual current owners | Assessment |
|---|---|---|---|
| Player | none | many scalar defaults and global maps | No OOP owner |
| NPC static identity | `PeopleData` | `RealName*`, `age_girls`, descriptions, init labels, secondary profiles, `PeopleData` | Multiple sources |
| NPC runtime | `PeopleInfo`/`Girl` | `PeopleInfo` plus legacy maps and `*Var` dictionaries | Maps remain operational source |
| NPC location | schedule resolver | JSON intervals, daily plans, `.rpy` schedules, `CurrentLoc`, default location, scene mutations | Multiple competing paths |
| Rooms | `Room` objects | `Room` plus room labels, build/restore labels, action dispatcher, four location variables | Partial OOP |
| Items | `GameItem` | `GameItem`, duplicate `GameObject`, catalog dictionaries, ID lists | Duplicate object models |
| Inventory | `playerItems` | `playerItems`, unused `inventory`, room contents, clothing ownership lists | Partial single source |
| Calendar | `calendar_v2` (`Calendar`) | `calendar_v2` plus scalar mirrors | Saved object is source; scalar mirrors remain compatibility debt |
| Events/threads | `Event`/`ThreadInfo` | canonical threads plus daily events, household AI, Amanda mini-events, tavern event queues, random-town runtime | Parallel systems |
| Combat | `FightEnemyDefinition` plus runtime globals | static enemy definitions and many global session maps/scalars | Enemies OOP, session/player not OOP |
| UI | `main_ui` screens | screens plus many persistent UI state globals, refresh/restore labels, action dispatchers | Too much flow/state |
| Persistence | Ren'Py defaults and migrations | defaults, custom reducers, many after-load callbacks, runtime sync functions | Distributed and incomplete |
| Basic actions | real Ren'Py labels | `Actions.rpy` labels plus refresh/apply/dispatcher helpers and social item logic | Label actions recoverable; wrappers are bloat |
| NPC dialogue | real `Int<Npc>Talk` labels | talk labels plus `Int<Npc>TalkRefresh`, `Int<Npc>TalkApply`, `SocialTalkTopics`, `social_core_action_items` | Event-like labels intended; generic builders are compatibility |

## 5. Player / MC Audit

### Current exhaustive feature groups

The MC currently has no `Player`, `MC`, `PlayerData`, or `PlayerState` class.

#### Identity and core condition

- age
- health
- energy
- fun
- money
- tavern fame
- charisma
- reputation
- notoriety
- exploration
- look
- costume condition
- hair condition
- hygiene
- sickness and forest restriction state

Primary location: `game/script.rpy`.

#### Inventory and equipment

- `playerItems`: effective inventory count map by item ID.
- `inventory`: unused legacy list.
- `EquippedWeapon`
- `EquippedArmor`
- clothing ownership and current dress
- dress wear/depreciation tracking
- haircut and wash state

Definitions use `GameItem`, but player ownership is not an object feature.

#### Combat and hunting

- health and energy are player globals.
- fight level is derived into `FightLevel["you"]`.
- hunt unlocked mirrors exploration.
- player fight supplies mirror `playerItems`.
- loaded weapon state has multiple mirrors.
- combat status and active fight session are global maps/lists.

#### Intimacy and history

- arousal
- daily orgasm/cum limits
- last sex/cum day
- aggregate sexual history maps
- per-girl history repository
- pregnancy-related partner records
- children records

Several overlapping repositories represent the same history.

#### Chores, work, and tavern management

- weekly chore counters
- UI chore projection
- unused scalar chore counters
- visitor tracking
- tavern cleanliness and room dirt
- worker assignment maps
- tomorrow assignment maps
- tavern reports and economy state

#### Social relationship impact

MC relationship effects are spread through NPC maps and direct story-label mutations. There is no player-facing relationship service or method boundary.

### Player duplication and drift

- `inventory` duplicates the actual `playerItems` concept and appears unused.
- `look`, `charisma`, `reputation`, and costume condition are persisted mirrors of derived calculations.
- `PlayerFightSupply` duplicates inventory.
- `FightLevel["you"]` and `HuntUnlocked` duplicate exploration-derived state.
- loaded weapon state is duplicated.
- `PlayerChoresWeek`, `UI_chores`, and scalar chore variables overlap.
- sexual history exists as detailed rows and multiple aggregate maps.
- `KidsList` and `kids[mother]` overlap.
- `"You"` and `"you"` appear as duplicate identity keys in intimacy-related stores.

### Target Player OOP model

The player must become one saved runtime object:

```renpy
default mc = PlayerState()
```

Recommended ownership:

```text
PlayerState
  code_name = "you"
  identity
  condition
  stats
  skills
  economy
  inventory
  equipment
  appearance
  intimacy
  chores
  tavern_management
  history
```

This does not require a class for every integer. It requires one authoritative object and clear feature components where behavior exists.

Required methods include:

- add/remove/spend money
- add/remove/count item
- equip/unequip
- apply damage/heal/spend energy
- change notoriety/reputation/exploration
- record intimacy/history
- register/reset/evaluate chores
- expose derived look/charisma/reputation without saving duplicate mirrors

Removal rule: after a feature is moved to `mc`, its old scalar/map source is deleted in the same phase. A temporary conversion function may read old saves once, but gameplay must not keep both paths.

## 6. NPC Audit

### Current OOP layer

`PeopleRuntime.rpy` defines:

- `PeopleData`: intended static/semi-static data.
- `PeopleInfo`: intended saved mutable state.
- `BaseNPC`: secondary NPC runtime extension.
- `Girl`: girl runtime extension.
- `peopleData`, `peopleInfo`, `girls`, `secondary_npcs`.

Audit classification:

- KEEP concept: Family Life-style `PeopleData` and `PeopleInfo`, simple registries, and named saved NPC instances.
- KEEP where useful: per-NPC `Girl`/`BaseNPC` subclasses when they remove real repeated behavior or hold explicit NPC-owned state.
- REMOVE/BYPASS as architecture: `PeopleRuntime.rpy` as a large runtime compatibility bridge that keeps object fields synchronized with legacy maps.
- REMOVE/BYPASS as architecture: bidirectional map/object sync, fallback construction from loose globals, and object shells that do not own state.

Family Life does not require a large people runtime service. Its useful model is a simple `people.rpy` shape: static person data, saved mutable person info, and a lookup rebuilt from named objects.

### Current NPC feature groups

#### Static identity

- canonical ID
- display and grammatical names
- full name
- description
- age and birth date
- portrait/card picture
- gift preferences
- topics/dialog references
- default location
- schedule references
- role/type

#### Runtime social state

- relationship
- openness
- corruption/sluttiness
- known/unknown
- mood/reaction state
- talk/flirt/gift/ask/fuck daily counters
- drunk state
- personal gifts and topics

#### Runtime work and schedule state

- current resolved location
- awake/talkable state
- jobs and assignments
- conditional schedule branches
- random daily schedule selections
- monthly counters

#### Story state

- per-NPC `*Var` dictionaries
- thread progress
- direct one-off flags
- event memories and cooldowns
- AI/intent state for Amanda and household systems

#### Girl-specific body and family state

- clothing/body layers
- visibility/insertion state
- pregnancy
- fertility
- conception chance
- children
- virginity
- detailed and aggregate intimacy history
- lactation/breastfeeding state

#### NPC presentation

- cards
- portraits
- visible NPC HUD entries
- action menus
- talk/flirt/gift flows

### Current NPC initialization problems

- `PeopleData` is rebuilt from legacy maps rather than being the static authority.
- `PeopleInfo.sync_from_maps()` makes maps authoritative.
- `PeopleInfo.apply_to_maps()` exists but has no observed callers.
- Amanda has no `Amanda(Girl)` class and is initialized as plain `PeopleInfo`.
- several `Girl`/`BaseNPC` object feature fields exist but are unused containers.
- `peopleData`, `peopleInfo`, `girls`, and `secondary_npcs` are saved defaults even though some should be derived registries.
- names and descriptions are initialized repeatedly.
- secondary NPCs have class construction, profile maps, registration labels, auto-registration labels, and `initPeople()` fallback construction.
- Gerhard, werecat, and dog do not follow one common declared NPC ownership contract.
- mixed-case IDs such as `Clara`/`clara` and `Alber`/`alber` create duplicate logical identities.
- every NPC class must have a `code_name`/`c_name` field used by code, for example `code_name = "clara"`; `Clara` is a display name, not the gameplay key.
- current NPC event files are mostly flat under `game/NPC/Girls/<NpcName>/`; the target folder structure is `game/NPC/Girls/<NpcName>/<NpcName>Events/` for that NPC's story/event labels.
- devdocs trial/v2 NPC object class files are planning references. They are useful only if converted into the simple runtime ownership model, not copied as another parallel layer.
### Schedule problem

Current resolution precedence is:

1. JSON interval schedule.
2. Generated daily schedule plan.
3. `.rpy` schedule entries.
4. compatibility/default location paths.

For NPCs with JSON schedules, `.rpy` schedules and daily plans can become inactive definitions. `CurrentLoc` is also directly mutated. This means there is no single editable schedule truth.

### Target NPC model

Static definitions:

```renpy
define AmandaData = PeopleData(code_name="amanda", ...)
```

Saved runtime instances:

```renpy
default Amanda = AmandaGirl("amanda", AmandaData)
default Melissa = MelissaGirl("melissa", MelissaData)
default Alber = SecondaryNPC("alber", AlberData)
```

Derived runtime registries:

```text
peopleInfo: code_name -> the named saved instance
girls: references to GirlInfo instances
secondary_npcs: references to NPCInfo instances
```

These registries contain references, not duplicated state, and are rebuilt on new game/load.

Required runtime ownership:

```text
NPCInfo / BaseNPC
  code_name
  data reference
  relationship/social state
  schedule runtime state
  job state
  story flags
  daily/weekly state
  mood/mana/reaction state

Girl / GirlInfo(NPCInfo)
  body/clothing state
  fertility/pregnancy state
  intimacy history
  children/family state
```

Target rules:

- one lowercase canonical `code_name` everywhere;
- `PeopleData` owns static identity and schedule definition reference;
- runtime instance owns mutable state;
- the code name is the gameplay key; display name is presentation only;
- `npc.get_location(calendar)` is the only location path;
- HUD, locate screen, event checks, and room visibility call the same method;
- NPC cards read the object only;
- `*Var` content is promoted into explicit object-owned story fields or one `story_flags` dictionary during that NPC's conversion;
- after promotion, the old top-level `*Var` dictionary is removed from gameplay;
- each NPC keeps its main init/class file under `game/NPC/Girls/<NpcName>/`;
- each NPC's authored event labels move under `game/NPC/Girls/<NpcName>/<NpcName>Events/`;
- NPC dialogue labels remain real labels, not Python menu builders.

## 7. Rooms, Objects, Items, And UI Audit

### Intended architecture

- `Room` owns room identity, descriptions, exits, and contained objects.
- `GameObject`/`GameItem` owns object/item data, picture, state, contents, and object-specific actions.
- location labels are flow anchors.
- screens display prepared state.

### Current violations

- `CurLoc`, `location`, `CurrentRoom`, and `current_room_code` all represent current location.
- room labels repeatedly assign all location mirrors.
- room object data is duplicated by room-specific build, object-menu, object-text, restore, and refresh labels.
- `ROOM_ACTION_REFRESH` and `RefreshCurrentActionMenu` form a central workaround dispatcher.
- `main_ui_restore_room_scene_state()` knows room-specific refresh behavior.
- `Room.action_menus` and `Room.build_extra_action_items()` contradict the requested rule that rooms do not own actions.
- `GameObject` and `GameItem` implement almost identical models and serialization.
- item definitions are converted into catalog dictionaries, registries, ID lists, and category lists.
- incomplete alternate soap/item code expects undefined runtime structures.
- `game/Utilities/General/Common/Actions.rpy` mixes real basic action labels with inventory helpers, social item rules, NPC gift/talk effects, UI refresh routing, and result apply wrappers.
- `RefreshCurrentActionMenu`, `ApplyActionResultToUI`, `ApplyItemAction`, and room refresh dispatch tables are compatibility/bloat, not target design.

### Target room and object schema

```text
Room definition
  code_name
  display_name
  picture
  descriptions
  exits
  contained object IDs
  schedule/open state

GameObject/GameItem definition
  code_name
  display_name
  description variants
  picture/media
  object state
  contents
  actions
```

Important rule: the room owns objects and exits, not action logic. Object actions belong to objects. Special room activities belong to direct labels/methods referenced by a clear room-entry label or object.

Basic action rule:

```text
room/object/NPC menu
-> real action label
-> label shows/selects picture and description
-> label mutates stats/time/items/state directly or calls a tiny named helper
-> return to the owning room/object/NPC flow
```

KEEP action labels after simplification:

- `Examine`
- `Take`
- `Drop`
- `Drink`
- `Eat`
- `Wash`
- `DoChore`
- `Sleep`
- `Rest`
- `MakeFire`
- `Clean`
- `Chop`
- `BoilWater`

REMOVE/BYPASS in the action rescue:

- refresh/rebuild/restore labels;
- generic apply/renew labels;
- dispatcher labels for one action;
- Python methods that duplicate simple Ren'Py label mutation;
- social gift/talk/flirt logic embedded in generic basic actions.

Canonical location state:

```renpy
default CurLoc = "TavernMain"
```

`CurrentRoom` must be derived from `CurLoc`. `location` and `current_room_code` must be removed after their callers are converted.

Canonical room-label shape:

```renpy
label TavernKitchen:
    $ CurLoc = "TavernKitchen"
    $ CurrentRoom = roomRegistry[CurLoc]
    call check_room_enter_event(CurLoc)
    call screen main_ui
    return
```

No room-specific refresh/rebuild/restore label is part of the target model.

### UI target

The current three right-side sections remain:

1. status/calendar/chores;
2. navigation and actions;
3. visible NPCs.

Screens display current state and return intent. They do not:

- decide event eligibility;
- change schedules;
- rebuild room logic;
- dispatch story progression;
- own purchases;
- repair runtime state.

UI selection state should be temporary and minimal. Room and gameplay state must not be stored in `current_action_*`.

## 8. Calendar Audit

### Current state

The runtime now declares `calendar_v2 = Calendar(...)` as canonical.

Removed in the first calendar cleanup:

- `CalendarV2` class name
- separate unsaved calendar helper object
- old script-only scalar mutation helpers

Remaining compatibility debt:

- `day`, `month`, `year`, `week`
- `hour`, `minute`, `time`
- `dayspassed`, `clock_minutes`
- display-name mirrors
- direct consumers of both slots and clock values

The scalar values above are mirrors from `calendar_v2`, but many current
callers still read them directly. They are not allowed to become independent
calendar owners again.

### Target calendar schema

One saved object:

```renpy
default calendar = CalendarState(...)
```

Owned mutable fields:

- minute
- hour
- day in period
- weekday
- period
- cycle
- days in game

Derived, not saved separately:

- clock minutes
- time-of-day slot
- weekday name
- period name
- cycle display
- moon phase
- formatted date

Methods:

- advance minutes
- advance day
- set clock/date for debug
- derive time slot
- derive moon phase
- run/call daily, weekly, period, and cycle hooks exactly once

Schedules and venue hours use hour/minute. HUD displays only the fantasy time slot and fantasy calendar names.

Removal rule: the replacement phase must delete the old scalar mutation path. Read-only compatibility properties may exist only during save conversion, not normal gameplay.

## 9. Event And Thread Audit

### Canonical system that should survive

```text
Event tuple definitions
  -> ThreadData
  -> threadData static registry
  -> ThreadInfo saved progress
  -> centralized availability check
  -> selected event target
  -> authored event label
  -> explicit thread.advance/complete/abort
```

### Critical current defects

- fresh-game conditions may not be initialized because event/thread condition initialization is tied to after-load rather than guaranteed new-game initialization;
- the normal story board exposes force-enable/reset/abort controls;
- `findBlockedThreads()` can loop forever;
- Becky thread definitions are not registered in the canonical thread list;
- room entry can fire canonical, household, daily, and NPC mini-event paths in sequence;
- event labels do not consistently return truthy, so room entry may continue into another event system;
- event labels reached through calls often jump back into rooms, leaving recursive call stacks;
- probabilistic availability can reroll between discovery and dispatch;
- town chronicle cooldowns are checked for three days but cleared daily;
- random town events are implemented outside the canonical event/thread system;
- daily events, household AI, Amanda mini-events, tavern incidents, and town events are parallel event schedulers.

### Target event architecture

Static definitions:

```renpy
define threadData = {...}
```

Saved progress:

```renpy
default threads = createThreads()
```

Single checking path:

```text
event eligibility checks:
  enabled/active thread
  current step
  day/weekday
  exact clock interval
  location
  action
  requirements
  conditions
  item
  cooldown
  daily fired flag
  probability selected once
  venue/open state
```

Single dispatch path:

```text
room/action calls event manager
event manager returns zero or one selected event
preEvent(thread_name) sets active thread when threaded
jump event label
event label owns scene, choices, state mutation, and thread progression
event label jumps/calls the next real room/label or returns only when it is a called procedure
```

Random events, household events, mandatory events, and repeatable events remain different categories, but all are `Event` definitions checked by the same eligibility pipeline.

Randomness is resolved once when a daily/cooldown event is selected. Refreshing UI or checking availability again must not reroll it.

### Event label contract

Event label owns:

- media using the explicit project media path;
- authored text/dialogue;
- player choices;
- immediate result text;
- domain method calls/state mutation;
- explicit thread progression;
- return/jump flow to the next real owner.

Event label does not:

- duplicate eligibility checks;
- rebuild room menus;
- dispatch another story label through wrappers;
- jump back into a called room-entry stack;
- own event availability state.

Event choice display contract:

- Choices are authored in the event label, preferably with classic `menu:`.
- Choices display while the event picture/text remains visible.
- In Tractir `main_ui`, those choices belong in the right event/action panel, not in a detached overlay.
- Multi-picture events remain authored beats in the label: repeated `vscene`/text blocks and optional `menu: "Продолжить": pass`.
- Thread state changes happen only at the real outcome beat.
- Do not use `QueuePagedPanelText`, `AdvancePagedPanelText`, refresh/apply/renew labels, or generic paging engines for authored story/sex sequences.

NPC dialogue contract:

- `talk` opens the NPC's real `Int<Npc>Talk` label.
- Talk/flirt/gift/questions are event-like choices in that label or real sublabels called by it.
- The chosen branch mutates `Talked`, `TalkedToday`, `FlirtedToday`, `GiftedToday`, `AskedToday`, relationship stats, and NPC-specific vars directly.
- Daily social counters reset in the new-day/sleep reset layer.
- Amanda, Melissa, Sandra, and Clarissa currently share talk-theme/gift mechanics; that data may be reused as scoring/preference data, but menu ownership and consequences belong to the talk label.
- `SocialTalkTopicMenu`, `SocialTalkTopicApply`, `social_core_action_items()`, `Int<Npc>TalkRefresh`, `Int<Npc>TalkApply`, and `main_ui_call_label` are compatibility/bloat for authored dialogue.

## 10. Combat Audit

### Current strengths

- enemy definitions are real objects with health, attack, defence, moves, skills, weapons, tactics, company size, loot, money, and exploration rewards;
- fight click flow passed the representative external test;
- hunting tables and enemy parties exist.

### Current weaknesses

- player combat state is global;
- active fight session is many globals/maps/lists;
- enemy definition objects are converted into runtime dictionaries;
- random logic uses direct Python/random calls;
- fight UI functions directly rewrite shared UI globals;
- supply, level, unlock, and weapon-load mirrors duplicate other state.

### Target

```text
EnemyDefinition: static enemy template
CombatantState: one participant's mutable fight state
FightSession: saved/current encounter state
CombatService: calculations and turn resolution
Fight labels: presentation and flow
Fight screen: display and player intent
```

The player combatant references `mc`. Enemy combatants reference `EnemyDefinition`. Fight rewards call player inventory/economy methods.

## 11. Persistence And Ren'Py Rules

Target Ren'Py persistence contract:

- `define`: immutable/static definitions and registries.
- `default`: save-backed runtime objects and progress.
- `persistent`: cross-playthrough preferences only.
- after-load: migrate save version and rebind runtime objects to current static definitions.
- derived registries/caches: rebuilt after load, not treated as saved truth.

Do not save duplicate references as separate state owners.

Named saved NPC objects are preferred:

```renpy
default Amanda = GirlInfo("amanda")
```

`peopleInfo["amanda"]` may reference `Amanda`, but it must not copy Amanda's fields.

Current persistence risks:

- many distributed after-load callbacks;
- custom object reducers with partial payload restoration;
- save migration only synchronizes selected runtime state;
- referenced but undefined `sync_item_runtime_state`;
- dynamically created save variables without `default`;
- UI state repair during after-load;
- static objects and saved mutable objects are not consistently separated.

## 12. Intended Architecture Versus Accidental Bloat

### Keep

- authored text, dialogue, media references, and label names where they are real content units;
- navigable room labels;
- `Room`, `RoomExit`, and room definitions after action ownership is corrected;
- one unified item/object model based on existing definitions;
- `PeopleData` and `PeopleInfo` concept;
- named NPC subclasses only where behavior is truly specialized;
- event/thread classes and tuple model after checking/dispatch defects are corrected;
- fight enemy definitions and working combat calculations;
- main three-section HUD layout;
- debug builder as a direct testing tool;
- exact canonical IDs and existing content context.

### Remove or bypass during owning subsystem replacement

- sync-both-directions object/map compatibility;
- room refresh/rebuild/restore labels;
- central room action refresh dispatcher;
- duplicate `GameObject`/`GameItem` model;
- unused `inventory`;
- duplicate schedule formats for the same NPC;
- `CurrentLoc` as an independent location owner;
- parallel event schedulers;
- event wrapper labels and one-action handlers;
- recursive debug/menu loops;
- player-facing debug mutation controls;
- duplicate calendar objects and scalar mutation path;
- silent `try/except: pass` used to hide missing state;
- `globals()`/`renpy.store` access where an owning object is available.

## 13. Target Data Architecture

```text
STATIC DEFINITIONS (define)
  peopleData: code_name -> PeopleData
  rooms: code_name -> Room
  items: object_id -> GameItem/GameObject
  enemyDefinitions: enemy_id -> EnemyDefinition
  threadData: thread_id -> ThreadData
  calendar constants

SAVED GAME STATE (default)
  mc: PlayerState
  Amanda, Melissa, Sandra, ...: GirlInfo/NPCInfo
  calendar: CalendarState
  threads: thread_id -> ThreadInfo
  fight: FightSession or None
  CurLoc: current room code
  room_state: mutable per-room state only

DERIVED RUNTIME REGISTRIES (rebuilt)
  peopleInfo
  girls
  secondary_npcs
  roomRegistry
  item registry/category indexes
  available event index

DOMAIN SERVICES / METHODS
  schedule resolution
  event eligibility and dispatch
  combat resolution
  inventory/equipment
  calendar advancement
  relationship/social rules

REN'PY LABELS
  room entry flow
  authored events/scenes
  interaction presentation
  call methods, show result, return

SCREENS
  display prepared state
  return player intent
```

## 14. Exhaustive Rescue Plan

Every phase follows the same rule:

```text
inventory current behavior
write ownership contract
add/repair authoritative object
convert all callers in the selected feature slice
delete displaced runtime path
compile
unit test
external click test
save/load test
```

No phase may finish with both old and new gameplay mutation paths active.

### Phase 0: Freeze and establish recovery baseline

Deliverables:

- create a recovery branch and preserve the current dirty worktree;
- record current playable journeys and known failures;
- list every required default/define used by those journeys;
- add a mandatory initialization-contract test;
- make compile, unit, and selected external click tests one repeatable QA command.
- mark contradictory old roadmaps as superseded when they recommend adding dispatchers, refresh labels, rebuild labels, result apply wrappers, or Python methods that duplicate simple labels.
- classify every touched label/function before editing as KEEP or REMOVE/BYPASS:
  real room entry, object menu, object action, NPC interaction, event/story label, returnable procedure vs refresh, rebuild, wrapper, handler-for-one-action, dispatcher, duplicate Python method, menu self-loop, or label made only for room attribute.

Acceptance:

- ordinary new game can enter all currently reachable rooms without undefined-variable crashes;
- current known `DanceSponsor` initialization failure is represented by a failing test before repair;
- no architecture refactor begins before baseline journeys are recorded.

### Phase 1: Repair event/thread initialization and dispatch

Why first: broken event eligibility can corrupt every later gameplay test.

Work:

- guarantee canonical thread/event condition initialization on new game and load;
- remove player access to debug thread mutations;
- fix blocked-thread termination;
- make selected event probability stable;
- enforce zero-or-one event per room/action check;
- enforce direct event-label flow: `preEvent(thread_name)` sets `thread`, the selected event label is jumped to, and the event label returns/jumps only to the next real owner;
- register real Becky definitions or explicitly classify them as non-canonical content;
- move random town, household, and NPC mini-event candidates into the canonical checking path;
- preserve mandatory events outside random daily selection while using the same eligibility checks.

Delete in this phase:

- redundant event wrappers;
- duplicate forced refresh calls;
- dead daily-event wrappers;
- random-town daily planning layer after canonical definitions replace it;
- parallel dispatch from room entry.

Acceptance tests:

- fresh-game conditions are active;
- all tuple fields are checked;
- no event rerolls on UI refresh;
- no event repeats in the same day unless explicitly repeatable;
- cooldowns survive day changes;
- room-entry event returns cleanly;
- authored event choices remain visible with picture/text in the active event layout;
- multi-picture/proceed events use authored beats, not queue/paging/apply machinery;
- random event combat invokes fight;
- mandatory market event remains mandatory;
- click tests for each converted event category.

### Phase 2: Establish PlayerState

Work slices:

1. identity/core stats/economy;
2. inventory/equipment;
3. appearance/clothing/depreciation;
4. combat-facing state;
5. intimacy/history;
6. chores/tavern management.

For each slice:

- add fields and methods to `mc`;
- migrate old save values once;
- convert all readers/writers;
- remove old defaults/maps/mirrors;
- update cards and HUD to read `mc`.

Acceptance:

- no direct gameplay mutation of removed player globals;
- no duplicate inventory, supply, chore, or derived-stat stores;
- save/load and rollback preserve the object;
- all existing player card and action click tests pass.

### Phase 3: Establish authoritative NPC objects

Order:

1. Amanda as the first complete `GirlInfo` conversion;
2. Melissa;
3. Sandra;
4. Clara;
5. Becky;
6. remaining girls;
7. secondary NPCs;
8. dog and werecat under explicit pet/NPC contracts.

For each NPC:

- define static `PeopleData`;
- define one named saved runtime object;
- keep the NPC class/init under `game/NPC/Girls/<NpcName>/`;
- place that NPC's event labels under `game/NPC/Girls/<NpcName>/<NpcName>Events/`;
- promote current init-map values and `*Var` flags;
- convert social, card, schedule, pregnancy/history, dialogue, and event callers;
- convert `Int<Npc>Talk` toward an event-like label with visible talk/flirt/gift/question choices;
- remove that NPC's legacy map ownership;
- keep only a derived registry reference.

Acceptance:

- card values equal current object state;
- HUD name and presence come from the object;
- talk/flirt/gift daily reset mutates the object;
- talk/flirt/gift choices are visible in the talk label and mutate state at the choice point;
- story events read object state;
- no mixed-case ID;
- no map/object synchronization for the converted NPC.

### Phase 4: Replace schedule stack

Work:

- choose one schedule definition format;
- recommended: static schedule definitions referenced by `PeopleData`, using exact minute intervals and named condition callables;
- store only daily resolved random choice when a probabilistic branch must remain stable;
- `npc.get_location(calendar)` is the only resolver;
- remove JSON/`.rpy`/daily-plan competition for each converted NPC;
- remove `CurrentLoc` as independent truth.

Acceptance:

- HUD, locate board, event checks, and room visibility agree;
- exact interval boundaries pass;
- conditional and probability schedules remain stable for the day;
- NPC appears in one location only;
- venue opening hours use the same calendar clock.

### Phase 5: Replace calendar completely

Work:

- create one saved calendar instance;
- convert schedules, rooms, events, HUD, and next-day flow;
- convert reset hooks;
- delete remaining mutable scalar mirrors after callers are converted;
- expose derived read-only values through methods/properties only.

Acceptance:

- one method advances time;
- day/week/period/cycle rollover tests pass;
- daily and weekly hooks fire once;
- HUD reads the calendar object;
- schedule boundaries use hour/minute;
- no direct mutation of old scalar time fields.

### Phase 6: Simplify rooms and object actions

Convert one room at a time, starting with a representative set:

1. TavernKitchen;
2. TavernMain;
3. DressShop;
4. WineStore;
5. MarketPlace;
6. remaining rooms.

For each room:

- retain one room definition and one entry label;
- ensure room owns descriptions, exits, and objects;
- ensure objects own object actions, pictures, and texts;
- convert basic actions to real labels that present pictures/text and mutate stats/time/items/state directly;
- remove build/restore/refresh/object-text dispatcher labels;
- remove central action refresh mapping entries;
- keep HUD screen placement unchanged.

Acceptance:

- every visible action click works;
- event return restores normal room state without refresh labels;
- actions return to the owning room/object/NPC flow instead of calling refresh/apply/renew labels;
- no duplicate room description/exits/object list;
- no recursive `call screen main_ui` stack growth.

### Phase 7: Unify items, inventory, shops, and crafting

Work:

- choose one `GameItem`/`GameObject` base model;
- make static objects the definition source;
- make item indexes/category lists derived;
- use player inventory methods;
- make shop containers hold item IDs/definitions and screens display them;
- remove incomplete alternate soap/item system or complete it through the canonical item path;
- remove manually duplicated tailor catalogs.

Acceptance:

- male/female tailor racks display their contained clothing objects;
- item description, price, bonuses, depreciation, ownership, and buy action come from item definition/state;
- buy/use/equip/craft flows mutate one inventory;
- all item IDs resolve.

### Phase 8: Encapsulate combat and enemies

Work:

- retain enemy definitions;
- create combatant/session state;
- connect player and pets;
- move fight session globals into `FightSession`;
- use shared random service;
- make fight labels/screens presentation-only around combat methods.

Acceptance:

- animals, crooks, thieves, bandits, and patrol groups use the same enemy/combat contract;
- fight, run, loot, health, weapon, dog support, and return flow click tests pass;
- no fight UI state leaks into rooms.

### Phase 9: UI, cards, debug, and documentation cleanup

Work:

- remove duplicate card presentation paths;
- cards read objects only;
- retain three-section HUD;
- keep debug builder as isolated developer tooling;
- remove alias labels, recursive loops, and gameplay mutation access from normal UI;
- make debug notes/report generation explicit;
- update architecture docs to match actual runtime, deleting contradictory standards.
- keep the Family Life-derived standards aligned across `ARCHITECTURE.md`, `STORY_LABEL_EVENT_FLOW_STANDARD.md`, `ACTION_ITEM_STANDARD.md`, `LOCATION_LOCATE_TALK_RESET_STANDARD.md`, and this rescue plan.

Acceptance:

- every player/NPC card renders current object values and correct picture;
- debug room directly tests rooms, objects, schedules, events, fights, media, and cards;
- normal UI cannot force story progress;
- documentation names one owner for every system.

## 15. QA Gate For Every Phase

### Static checks

- no undefined referenced defaults/defines in the converted slice;
- no duplicate canonical ID;
- no forbidden direct old-state writes;
- no new `globals()`/`renpy.store` access where an owner exists;
- no wrapper/rebuild/refresh labels added;
- no direct `renpy.random` where shared random service is required.

### Unit/domain tests

- methods mutate only their owning object;
- derived values are not saved as competing truth;
- schedule interval and probability selection;
- event eligibility field coverage;
- calendar rollover/reset hooks;
- inventory/equipment operations;
- combat resolution.

### External click tests

- start new game;
- navigate every converted room;
- click every visible room/object/NPC action;
- trigger each event result branch;
- verify event returns and HUD;
- verify NPC cards and locate board;
- verify shop buy/use/equip;
- verify fight and return;
- sleep/new day;
- save/load and repeat representative actions.

### Test integrity rule

Tests must exercise the real UI and runtime path. They must not pass by calling internal labels in a new context when the actual click path is broken.

## 16. Immediate Next Work

The first implementation stage should not be a broad OOP rewrite.

It should be:

1. preserve the current branch/worktree;
2. mark superseded roadmap items that recommend refresh/apply/renew/rebuild wrappers or central dispatcher consolidation;
3. add the initialization-contract and core navigation/action smoke suite;
4. repair the confirmed undefined-state failures;
5. repair canonical event/thread initialization and zero-or-one dispatch using direct event labels and active `thread`;
6. select one basic action slice in `Actions.rpy` and simplify it toward direct label execution;
7. select one NPC dialogue slice, preferably Amanda or Melissa, and convert talk/flirt/gift/questions toward a direct event-like talk label;
8. select Amanda as the first complete NPC object replacement;
9. select one representative player feature slice, inventory/equipment, for the first `PlayerState` replacement;
10. delete displaced legacy ownership in each converted slice;
11. verify with compile, unit, external click, and save/load tests.

This creates a proven replacement pattern before applying it to the rest of the project.

## 17. Final Architecture Rule

```text
Static definitions describe what exists.
Saved runtime objects own mutable game state.
Derived registries provide lookup, never duplicate ownership.
Methods apply domain logic.
The event manager decides availability.
Labels present authored flow and call methods.
Screens display state and return intent.
Debug tools test isolated features.
When a new owner replaces an old owner, the old gameplay path is removed.
```
