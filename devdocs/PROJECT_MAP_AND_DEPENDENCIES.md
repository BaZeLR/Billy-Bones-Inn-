# Tractir Project Map

Scope: `C:/Users/blank/Documents/RenPy_Projects/Tractir`

This is a current map for code ownership. It is not a migration log.

## Runtime Roots

- `game/script.rpy`: startup defaults and calendar class.
- `game/Utilities/General/Screens/main_layout.rpy`: persistent `main_ui`
  rendering only.
- `game/Utilities/General/Classes/RoomTemplate.rpy`: room, object, exit,
  schedule, and action data classes.
- `game/Utilities/General/Common/Actions.rpy`: direct basic action labels.
- `game/Utilities/General/Events/`: event/thread runtime.
- `game/Utilities/General/Classes/StoryEventRuntime.rpy`: current thread/event
  data rows.
- `game/Utilities/General/NPC/PeopleRuntime.rpy`: people data/info registration.
- `game/Utilities/General/NPC/NPCScheduleModel.rpy`: NPC schedule runtime.

## Room Ownership

- `game/Inn/`: tavern rooms and tavern-owned object/action labels.
- `game/Town/`: town rooms, shops, church, market, and town-owned object/action
  labels.
- `game/Forest/`: forest rooms, travel, hunt, gathering, and forest-owned
  object/action labels.

Room files own their local room label, objects, navigation, visible text,
picture selection, and room-specific actions.

## NPC Ownership

- `game/NPC/Girls/<Name>/Init<Name>.rpy`: girl data/info initialization.
- `game/NPC/Girls/<Name>/Int<Name>Talk.rpy`: girl talk flow.
- `game/NPC/Secondary/Init<Name>.rpy`: secondary NPC data/info initialization.
- `game/NPC/Secondary/Int<Name>Talk.rpy`: secondary NPC talk flow.
- `game/NPC/Schedules/`: interval schedule JSON where used.

NPC-specific state belongs on the NPC info object and its `.var` store.

## Event Ownership

- Event rows define availability: location, action, day/hour window,
  conditions, target label, and priority.
- Event labels define content: `vscene`, text, menu choices, consequences, time
  cost, and thread progression.
- Repeated event availability should be blocked by event/thread state or the
  event runtime's once-per-day fired key where appropriate.

## Time Ownership

- `calendar_v2` owns day, week, hour, and minute.
- Room open hours, NPC schedules, event rows, and sleep gates should use
  `calendar_v2.hour` and `calendar_v2.minute`, or explicit `start` / `end`
  clock intervals.
- Display slots are UI display only.

## Forbidden Patterns

Do not add:

- refresh, rebuild, restore, apply, renew, bridge, shim, or fallback labels
- central dispatchers for one action
- generic NPC action dictionaries
- Python methods that duplicate simple Ren'Py labels
- `globals()` or `renpy.store` when an owning object exists
- authored event choices built through the room action panel

## Verification

Use these from project root:

```powershell
python -m pytest -q
powershell -ExecutionPolicy Bypass -File tools\renpy_compile.ps1 compile
powershell -ExecutionPolicy Bypass -File tools\renpy_compile.ps1 lint
```

Only call a behavior click-tested after launching the game and clicking that
actual room, event, or action path.
