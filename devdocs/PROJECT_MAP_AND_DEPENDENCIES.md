# Project Map And Dependencies

Scope: `C:/Users/blank/Documents/Ren'Py_Projects/Tractir`

Generated from local inspection on 2026-04-27.

## Project Shape

Top-level folders:

- `game/` - active Ren'Py project runtime.
- `game/Inn/` - main gameplay port; most labels, room logic, events, schedules, items, character systems.
- `game/images/` - active media assets.
- `game/json/` - JSON data/assets, currently mostly reference/fallback data.
- `devdocs/` - migration docs, audits, knowledge base, reference engine fragments.
- `textLocRef/` - original/source TXT/QSP-style reference files.
- `Inn_rpy_backup/` - backup of previous `.rpy` work.
- `renpy_mcp_server/` - local MCP tooling, separate Python project.
- `workspace/` - extra workspace/tooling area.

Current rough counts:

- `game/**/*.rpy`: 302 files.
- `game/Inn/**/*.rpy`: 290 files.
- labels: 897.
- screens: 52.
- defaults: 417.
- defines: 177.
- init blocks: 216.
- `game/json`: 13 JSON files.
- `game/images`: about 1,071 image/media files.
- `textLocRef`: 232 reference TXT files.
- `devdocs`: 58 doc/reference files.

## Runtime Entry Flow

Main project config:

- `game/options.rpy`: game name/version/build/save config.
- `game/gui.rpy`: 1920x1080 GUI sizing and default GUI constants.
- `game/screens.rpy`: default Ren'Py screens plus project `MenuItem` and `choice_panel`.
- `game/script.rpy`: intro helpers, calendar engine, splash/intro, `label start`.

Boot path:

```text
label start
  -> jump Intro
label Intro
  -> initializes core stores and characters
  -> calls InitSecondaryNPC, InitDressDesc, InitAmanda, InitSandra, InitMelissa,
     InitGeorgett, InitLiza, InitBecky, InitInga, InitIrma, InitClara
  -> initializes story runtime
  -> enters first playable location flow
```

`game/Inn/Intro.rpy` owns most core `default` state:

- current location: `CurLoc`, `location`, `PrevLoc`;
- UI text/media: `MainTxt`, `CurLocDesc`, `_layout_last_picture`, `GraphicsOn`;
- time/economy: `time`, `hour`, `minute`, `day`, `month`, `week`, `year`, `money`, etc.;
- player stats and inventory;
- relationship/social maps;
- pregnancy/sex-state maps;
- `DailyEventsList`;
- roster list `AllGirlNames`.

## Core Runtime Dependencies

### UI

```text
game/screens.rpy
  -> MenuItem
  -> choice_panel
game/Inn/my_layouts/main_layout.rpy
  -> screen main_ui
  -> screen current_action_panel
  -> main_ui_set_action_panel
  -> main_ui_restore_room_scene_state
  -> main_ui_call_label
```

Dependency direction:

```text
rooms/events/talk labels
  -> set MainTxt / CurLocDesc / scene_image / current_action_items
  -> show screen main_ui
  -> current_action_panel renders choice_panel/current_action_content/action_menu_specs
```

Preservation rule: gameplay should feed the existing `main_ui`, not replace it.

### Media

```text
game/01vscene.rpy
  -> custom vscene statement
  -> clears master layer and shows image/video

game/Inn/ShowImage.rpy
  -> legacy media resolver
  -> alias/path/extension fallback
  -> resolve_main_ui_picture
```

High-use media dependency targets:

- `ShowImage`: 347 detected call/action references.
- `ShowImageSeq`: 62 detected call/action references.

### Rooms And Movement

```text
game/Inn/RoomTemplate.rpy
  -> Room
  -> RoomExit
  -> RoomDescription
  -> RoomScene
  -> RoomTrigger
  -> RoomSchedule
  -> MoveToRoom

game/Inn/Loc.rpy
  -> EnterLocation

game/Inn/TimeTurnSystem.rpy
  -> AdvanceMovementTime

game/Inn/AdvanceTime.rpy
  -> AdvanceTime
```

Typical room dependency:

```text
Room file
  -> Room(...)
  -> label RoomName
      -> call EnterLocation("RoomName")
      -> call CheckDailyEvent("", "_story_enter", CurLoc, time) when applicable
      -> call RoomNameBuildActions
      -> jump RoomNameView
  -> label RoomNameBuildActions
      -> current_action_items = [MenuItem(...)]
  -> label RoomNameView
      -> show screen main_ui
```

Examples: `TavernMain`, `TavernKitchen`, `TavernMyRoom`, `PortStreets`, `MarketPlace`, `Church`, `WineStore`, forest locations.

### Actions

```text
game/Inn/Actions.rpy
  -> RefreshCurrentActionMenu
  -> ReturnToMainUI
  -> ApplyActionResultToUI
  -> Examine / Take / Drop / Drink / Eat / Wash / DoChore / Sleep / Rest / MakeFire / Clean / Chop / BoilWater

game/Inn/my_layouts/build_room_action_items.rpy
  -> generic room object/exit item builder

game/Inn/SceneActionPanel.rpy
  -> reusable event/right-panel action scene helper
```

High-use action dependency targets:

- `SlutFriendsIncrease`: 164 detected references.
- `stat`: 91 detected references.
- `ShowCurrentSex`: 62 detected references.
- `CleanScreenOverflow`: 44 detected references.
- `EnterLocation`: 40 detected references.
- `ReturnToMainUI`: 35 detected references.
- `AdvanceMovementTime`: 18 detected references.
- `CheckDailyEvent`: 17 detected references.

### NPCs And Schedules

```text
game/Inn/NPCScheduleModel.rpy
  -> NPCSchedules
  -> NPCScheduleEntry
  -> npc_schedule_set
  -> npc_schedule_location
  -> npc_schedule_sync_currentloc
  -> npc_schedule_sync_all
  -> getLocation
  -> getNPCids

game/Inn/CharacterActionHub.rpy
  -> NPC_META
  -> npc_room_interaction_visible
  -> npc_action_data_for_room
  -> open_entity_action_menu_state
  -> character grid entries
```

Character initialization labels define active schedules:

- `InitAmanda.rpy`
- `InitSandra.rpy`
- `InitMelissa.rpy`
- `InitBecky.rpy`
- `InitClara.rpy`
- `InitGeorgett.rpy`
- `InitLiza.rpy`
- `InitInga.rpy`
- `InitIrma.rpy`
- `InitSecondaryNPC.rpy`
- `WerecatNPC.rpy`

Dependency direction:

```text
Init*.rpy / WerecatNPC.rpy
  -> npc_schedule_set(...)
Time advancement / NextDay
  -> npc_schedule_sync_all()
Room.visible_npcs()
  -> getNPCids(room_code)
  -> npc_action_data_for_room(...)
main_ui character grid
  -> open_entity_action_menu_state(...)
```

### Events

Daily queue:

```text
game/Inn/CheckDailyEvent.rpy
  -> DailyEventsList_Add
  -> CheckDailyEventExists
  -> DailyEventsList_PopMatch
  -> DailyEventsList_EndDayUpdate
  -> label CheckDailyEvent
```

Story threads:

```text
game/Inn/StoryEventRuntime.rpy
  -> ThreadData / LThreadData / RThreadData / UThreadData
  -> ThreadInfo
  -> Event
  -> threadData
  -> threads
  -> findAvailableEvents
  -> story_event_available
  -> checkTriggers
```

Dependency direction:

```text
Room entry
  -> CheckDailyEvent("", "_story_enter", CurLoc, time)
  -> checkTriggers(CurLoc, "enter", 0)
  -> StoryEventRuntime target label

Scheduled day/time event
  -> DailyEventsList
  -> CheckDailyEvent(girl, event_type, location, time)
  -> target event label
```

These systems are separate and should remain separate.

### Tavern/Home Systems

Important runtime clusters:

- `TavernMain.rpy`: tavern hall and main work/event hub.
- `TavernKitchen.rpy`: breakfast, dinner, food/drink/perk flows, kitchen room.
- `TavernMyRoom.rpy`: player room, sleep, table/crafting, chest/dress storage.
- `TavernAmandaRoom.rpy`, `TavernMelissaRoom.rpy`, `TavernSandraRoom.rpy`: bedroom logic and room-specific actions.
- `TavernUpstairs.rpy`, `TavernStorage.rpy`, `TavernAtic.rpy`, `Backyard.rpy`, `Shed.rpy`, `TavernStable.rpy`: home sublocations and utility work.
- `PlayerCard.rpy`, `GirlCard.rpy`, `DogCompanion.rpy`, `WerecatNPC.rpy`, `menu_tavernstat.rpy`: UI panels and companion/report systems.

### Town And External Locations

Main town clusters:

- `StreetTavern.rpy`
- `MarketPlace.rpy`
- `PortStreets.rpy`
- `Church.rpy`
- `CityGuard.rpy`
- `WineStore.rpy`
- `DressShop.rpy`
- `BarberShop.rpy`
- `GroceryStore.rpy`
- `HunterClub.rpy`
- `ArtisansQuarter.rpy`
- `StolyarWorkshop.rpy`
- `BeckyHome.rpy`
- `EllonaTemple.rpy`

Forest/hunt clusters:

- `Forest.rpy`
- `ForestClearing.rpy`
- `ForestLake.rpy`
- `ForestSpring.rpy`
- `ForestHiddenPath.rpy`
- `ForestDarkWoods.rpy`
- `ForestCave.rpy`
- `ForestWaterfall.rpy`
- `FightSystemRuntime.rpy`
- `HunterClub.rpy`

## Data Dependencies

Active JSON files:

- `game/json/intro_sequence.json`
- `game/json/tavern_events.json`
- `game/json/npcs/*.json`

Important finding:

- `game/script.rpy` actively loads `json/intro_sequence.json`.
- `devdocs/engine/data_loader.rpy` contains JSON loader functions for people/items/tavern events, but it lives under `devdocs`, not active `game`.
- `devdocs/people.rpy` consumes `load_people_dataset()`, but also lives under `devdocs`.
- The active game currently relies on explicit `Init*.rpy` labels and `NPCScheduleEntry` schedules, not JSON NPC files.

So `game/json/npcs/*.json` is currently reference/portable data unless moved into `game` runtime and wired deliberately.

## Tooling Dependencies

Ren'Py SDK:

- Active SDK used for lint: `C:/Users/blank/renpy/renpy-8.5.2-sdk/renpy.exe`
- Lint command used:

```powershell
& 'C:\Users\blank\renpy\renpy-8.5.2-sdk\renpy.exe' '.' lint
```

Lint result:

- Exit code `0`.
- No lint output.

Ren'Py MCP server:

- Folder: `renpy_mcp_server/`
- Separate Python project.
- Python requirement: `>=3.10,<3.12`.
- Dependencies:
  - `fastmcp`
  - `mcp`
  - `pydantic`
  - `structlog`
  - `google-genai`
  - `pillow`
  - `rembg`
  - `onnxruntime`
  - optional `boto3`
  - optional `python-on-whales`

## Current Coupling Risks

1. `main_ui` is central. Breaking `current_action_items`, `current_action_content`, `action_menu_specs`, `UI_mode`, or `CurrentRoom` affects most rooms.
2. `ShowImage` is heavily used. Media path changes should go through its resolver or update aliases.
3. Schedule truth is split between `NPCSchedules` and legacy/current maps such as `CurrentLoc`; keep syncing after time changes.
4. `DailyEventsList` and story threads both trigger events but are not interchangeable.
5. JSON NPC data exists but is not the active source of truth.
6. The worktree is dirty with many unrelated modified/deleted files; future edits must stay scoped and avoid reverting user changes.

## Practical Dependency Direction For New Work

For a room action:

```text
Room file -> current_action_items -> MenuItem -> label/function -> stat -> room restore/main_ui
```

For an NPC action:

```text
Init schedule -> NPCScheduleModel -> Room.visible_npcs -> CharacterActionHub -> right-panel action menu -> talk/look label
```

For a scheduled event:

```text
DailyEventsList_Add -> CheckDailyEvent -> target label -> restore UI/location
```

For a story arc:

```text
ThreadData -> StoryEventRuntime -> room entry/action check -> checkTriggers -> target label -> story_thread_advance_current
```

For a right-panel event scene:

```text
Event label -> SceneActionPanel -> vscene + MainTxt + current_action_items -> action labels/functions -> restore room
```
