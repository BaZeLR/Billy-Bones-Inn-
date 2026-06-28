# Ren'Py Engine And Tractir Project Knowledge Base

Purpose: preserve the current Tractir UI, mechanics, logic, and content while using Ren'Py structures correctly for backgrounds, `vscene`, labels, right-panel actions, events, schedules, and NPC data.

This file is based on local inspection of:

- Ren'Py SDK: `C:/Users/blank/renpy/renpy-8.5.2-sdk/renpy`
- Ren'Py docs: `C:/Users/blank/renpy/renpy-8.5.2-sdk/doc`
- Project runtime: `game/`
- Reference NPC file: `devdocs/people.rpy`

## 1. Local Ren'Py Engine Facts

Ren'Py script flow is label-driven:

- Engine AST classes exist for `Show`, `Scene`, `Call`, `Return`, and `Jump` in `renpy/ast.py`.
- Screen actions exist for `Call()`, `Jump()`, `Return()`, `SetVariable()`, and `Function()` in Ren'Py common code and documented screen actions.
- Dynamic labels are valid through `call expression` and `jump expression`, which this project already uses.

Scene and image behavior:

- `renpy.scene(layer="master")` clears a layer.
- A full `scene` statement is equivalent to `renpy.scene()` followed by `renpy.show(...)`.
- `show` and `scene` display on layers. Screens are separate UI layers, so clearing `master` does not remove a shown screen unless that screen is hidden separately.

Screen behavior:

- Screens can include other screens with `use` and dynamic screens with `use expression`.
- Screen state changes from Python should call `renpy.restart_interaction()` when the visible UI must refresh immediately.
- This project wraps that as `main_ui_restart_interaction()`.

Threading:

- Ren'Py has `renpy.invoke_in_thread()`, but the web port does not support multithreading.
- Gameplay events, room actions, and UI state should not depend on Python threads.
- Use Ren'Py labels, screen actions, event queues, and explicit schedule checks for gameplay flow.

## 2. Project Display Model

### `vscene`

File: `game/01vscene.rpy`

`vscene` is a creator-defined Ren'Py statement:

```renpy
vscene "images/path/to/picture.png"
vscene "images/path/to/movie.webm" fullscreen
```

Its runtime does this:

- calls `renpy.scene()` to clear the master layer;
- shows a black background displayable;
- shows the requested image or movie on the master layer using the project `master` transform;
- handles movie channel playback and controller screen for fullscreen movies.

Preservation rule:

- Keep using `vscene` for full scene/background media when the right panel must remain available.
- Do not replace `vscene` with ad hoc `scene` or raw `renpy.show()` in event code unless there is a specific reason.
- `vscene` affects the scene layer; the `main_ui` screen is separate and should stay intact.

### `ShowImage`

File: `game/Inn/ShowImage.rpy`

`ShowImage` is the legacy/media resolver layer. It resolves image aliases, file extensions, old path variants, and video/image refs. Many ported scenes call:

```renpy
call ShowImage("", "", picture_path)
call ShowImage("amanda", "tavern", "some_image")
```

Preservation rule:

- Use `ShowImage` only when ported legacy content still relies on folder/name
  resolution.
- Use direct picture paths with `vscene` for new or refactored authored
  event/scene media.

## 3. Main UI And Right Panel

File: `game/Inn/my_layouts/main_layout.rpy`

The project's main UI is `screen main_ui()`.

It preserves the current arrangement:

- left area: location name, text, and picture;
- right upper block: location/time/tavern controls;
- right middle block: current action panel;
- right lower block: character grid.

The current action panel is controlled by these store variables:

- `current_action_title`
- `current_action_items`
- `current_action_content`
- `action_menu_specs`
- `UI_mode`
- `UI_selected_char`
- `current_girl_key`

`screen current_action_panel()` resolves in this order:

1. If `action_menu_specs` exists, use `npc_action_menu(action_menu_specs)`.
2. Else if `current_action_content` exists, `use expression current_action_content`.
3. Else if `current_action_items` exists, use `choice_panel(current_action_items)`.
4. Else if the current mode is a non-room mode, show no fallback.
5. Else build room actions from `CurrentRoom`.

Preservation rule:

- Do not replace `main_ui`.
- Do not build separate full-screen menus for normal gameplay actions.
- Use `current_action_items` plus `MenuItem` for right-panel choices.
- Use `current_action_content` only for a custom screen inside the right panel.
- Do not route authored events, talk choices, or one-off object actions through
  generic panel setter wrappers. The owning room, object, NPC, or event label
  owns the choices and consequences.

## 4. Menu And Action Shape

File: `game/screens.rpy`

The project has a small `MenuItem` wrapper:

```renpy
MenuItem(caption, action)
```

`screen choice_panel(items)` renders each item as:

```renpy
textbutton i.caption action i.action
```

Valid actions are normal Ren'Py actions:

- `Call("LabelName", args...)`
- `Jump("LabelName")`
- `Function(function_name, args...)`
- action lists such as `[SetVariable(...), Call(...)]`

Preservation rule:

- Right-panel actions should be `MenuItem` objects.
- Mutating actions should call direct labels/functions that update variables,
  call `stat` if needed, then return to the owning room/object/NPC flow.
- Authored story/talk choices should use normal Ren'Py `menu:` in the label.

## 5. Room Model

File: `game/Inn/RoomTemplate.rpy`

`Room` is the top-level location container. It contains:

- `code_name`
- `display_name`
- `group_name`
- `bg_picture`
- default, first-visit, and situational descriptions
- exits
- game objects/items
- explicit room-owned actions only when the room itself is the target
- optional schedule for venues
- hidden/locked/open state booleans
- custom properties

Related classes:

- `RoomExit`
- `RoomDescription`
- `RoomSchedule`

Important methods:

- `visible_descriptions()`
- `visible_exits()`
- `visible_objects()`
- `visible_actions()`
- `build_menu_sections()`

Movement:

- `RoomExit` becomes a `MenuItem`.
- `MoveToRoom` and `AdvanceMovementTime` handle time cost and label jumping.

Preservation rule:

- Keep room content bound to room files.
- Do not move all actions into one global router.
- Room files may add special local actions only when the room itself owns the
  action. Object/item, NPC, and event actions stay with their owners.
- Room files should still respect `CurrentRoom`, `CurLoc`, `MainTxt`,
  `scene_image`, and the right-panel variables.

## 6. Generic Room Action Builder

File: `game/Inn/my_layouts/build_room_action_items.rpy`

`build_room_action_items(room)` builds generic right-panel items from:

- visible room objects;
- visible exits.

It uses:

- object access: `Call(object_menu_label, obj.object_id)`
- movement: `Call("AdvanceMovementTime", exit_obj.target)`

Preservation rule:

- Use this as fallback only.
- More complex room files can build richer menus, but should use the same `MenuItem` and Ren'Py action style.

## 7. NPC Visibility And Interaction

NPC presence is not room-owned. It is driven by NPC class/schedule/event
location state:

- current room/location is `CurLoc`/`current_location`;
- the visible NPC section calls `getNPCids(current_location)`;
- `getNPCids` compares each NPC `getLocation(...)` result to that location;
- NPC data/info classes for identity, portraits, info cards, and state;
- NPC talk/info labels for talk, examine, gift, flirt, and NPC-specific actions.

Common NPC interactions:

- info/examine card
- talk
- NPC-specific action labels
- event-owned contextual interactions

Preservation rule:

- If an NPC is present but has no interaction, check the NPC's data/info class,
  talk label, info-card/examine label, schedule location, and room visibility.
- Do not invent hidden schedules. Use `NPCScheduleModel.rpy`, `getLocation`,
  and current room visibility checks.
- New NPC actions belong to the NPC talk/info labels or the owning room.
- Do not recreate a generic character action hub, action dictionary, spec
  dispatcher, or Python menu layer.

## 8. NPC Schedule Model

File: `game/Inn/NPCScheduleModel.rpy`

The active project schedule system is `NPCSchedules`.

Main data class:

```renpy
NPCScheduleEntry(
    location="TavernMain",
    weekdays=[1, 2, 3, 4, 5, 6, 7],
    start="08:00",
    end="17:59",
    awake=True,
    talkable=True,
    condition=None,
    priority=0,
    label=""
)
```

Main APIs:

- `npc_schedule_set(npc_id, entries)`
- `npc_schedule_add(npc_id, entry)`
- `npc_schedule_resolve(npc_id, weekday_value, time_value)`
- `npc_schedule_location(npc_id, weekday_value, time_value)`
- `npc_schedule_state(npc_id, weekday_value, time_value)`
- `npc_schedule_sync_currentloc(npc_id, weekday_value, time_value)`
- `npc_schedule_sync_all(weekday_value, time_value)`
- `getLocation(person, weekday_value, time_value)`
- `getNPCids(location, weekday_value, time_value)`

The model supports conditional schedule rules:

- `tavern_team_match`
- `werecat_active`
- `werecat_roam_match`

Preservation rule:

- `NPCSchedules` is the schedule source.
- `CurrentLoc[npc_id]` is a synced projection plus explicit overrides.
- Room/NPC visibility should call `getLocation`, `getNPCids`, or `npc_schedule_location`, not hand-rolled checks.
- Events that change where somebody is should sync schedule state or make a deliberate override.
- New or touched schedules should use real clock intervals (`start` / `end`) or
  `calendar_v2.hour` / `calendar_v2.minute` checks. Display slots are UI
  display only and should not decide gameplay availability.

## 9. `people.rpy` Comparison

Reference file: `devdocs/people.rpy`

`people.rpy` is a JSON-per-NPC infrastructure pattern:

- `PeopleData` wraps a JSON entry.
- It stores static identity, stats, skills, jobs, clothes, relationships, age, virginity, and icon metadata.
- It normalizes `schedule.weekday` and `schedule.weekend` into 24-slot arrays.
- `getLocation(week_day, hour)` returns the current array slot.
- `isInLocation(location, week_day, hour)` compares the array slot.
- `PeopleInfo` stores runtime relationship/talk/flirt/gift state.

Current Tractir runtime differs:

- NPC identity belongs to `PeopleData` subclasses.
- NPC runtime state belongs to info-class instances such as `Girl` or secondary
  NPC info classes.
- NPC-specific state belongs on the owning object, for example `Amanda.var`,
  `Melissa.var`, or the secondary NPC info object's var store.
- Schedules are conditional objects or interval rows, not simple 24-slot arrays.
- Presence is resolved by priority, weekday, clock interval, and conditions.
- Talk/look/info-card actions belong to the NPC's own talk/info labels and
  methods, not a global action dispatcher.

How to combine safely:

- Treat `people.rpy` as a data-loading/reference model, not a replacement for
  Tractir UI/action flow.
- If importing JSON NPC data, convert schedule rows into interval schedule
  rows or `NPCScheduleEntry` objects that use real clock ranges.
- Do not add old global dict/action-hub dependencies when the NPC data/info
  class can own the state or behavior.

## 10. Daily Events Versus Story Threads

### Daily event queue

File: `game/Inn/CheckDailyEvent.rpy`

`DailyEventsList` rows contain:

- `GirlName`
- `Location`
- `Time`
- `TimeCheckExpr`
- `ChanceToMeet`
- `KeepNextDay`
- `EventType`
- `EventCode`

Main APIs:

- `DailyEventsList_Add(...)`
- `CheckDailyEventExists(...)`
- `DailyEventsList_Delete(...)`
- `DailyEventsList_PopMatch(...)`
- `DailyEventsList_EndDayUpdate(...)`
- label `CheckDailyEvent(...)`

This is for scheduled daily/one-off events such as dress-buy events, sickness events, or location-time meetings.

### Story thread runtime

File: `game/Inn/StoryEventRuntime.rpy`

Story threads use:

- `ThreadData`
- `LThreadData`
- `RThreadData`
- `UThreadData`
- `ThreadInfo`
- `Event`
- `threads`
- `availEvents`

Main APIs:

- `initStoryEventRuntime(force=False)`
- `findAvailableEvents(forced=False)`
- `story_event_available(location_name, action_name)`
- `story_thread_advance_current()`

Story events are keyed by location and action, for example:

- location: `TavernStorage`
- action: `enter`
- target label: `story_melissa_storage_rat_0`

`CheckDailyEvent("", "_story_enter", CurLoc, time)` bridges room-entry checks into story trigger handling.

Preservation rule:

- Do not merge `DailyEventsList` and `StoryEventRuntime`.
- Use `DailyEventsList` for scheduled date/time events.
- Use story threads for arcs that advance by event sequence and availability conditions.
- Use `_story_enter` for room entry story checks where the room already follows that pattern.

## 11. Removed Panel/Wrapper Patterns

Do not use these as current architecture:

- `SceneActionPanel`
- `main_ui_set_action_panel` as an event/talk/object-choice dispatcher
- refresh/rebuild/restore/apply/renew labels
- generic scene queues or paged-panel engines for authored story scenes
- Python dispatchers that hide which label owns a choice or consequence

Correct event shape:

```renpy
label story_example_event:
    vscene "images/example/event.jpg"
    "Event text."

    menu:
        "Act":
            $ SomeNpc.var["example_seen"] = 1
            $ thread.advance()
            jump expression CurLoc

        "Leave":
            jump expression CurLoc
```

## 12. Implementation Rules Going Forward

For new rooms:

1. Define/update a `Room`.
2. Set `CurLoc`, `location`, `CurrentRoom`, `scene_image`, and `MainTxt`.
3. Show media with `ShowImage` or `vscene`.
4. Populate `current_action_items` with `MenuItem`.
5. Call `screen main_ui` through the room's normal entry flow.

For new event scenes:

1. Put event text in the label, not in a hidden dispatcher.
2. Use `vscene`, text, and normal Ren'Py `menu:`.
3. Mutate vars directly at the choice branch or call a real shared helper label.
4. Advance time with `calendar_v2.advance_minutes(...)` where appropriate.
5. Return to the owning room label with `jump expression CurLoc` or a direct
   room label.

For NPC presence:

1. Add/adjust NPC schedule rows using real clock ranges where possible.
2. Ensure `npc_schedule_sync_currentloc()` or `npc_schedule_sync_all()` runs after time/location changes.
3. Ensure the NPC data/info class has the right talk/info/examine ownership.
4. Let `getLocation()`/`getNPCids(current_location)` and the character grid
   expose the visible NPC.

For events:

1. Use `CheckDailyEvent` for scheduled/daily queue events.
2. Use `StoryEventRuntime` for thread arcs.
3. Do not use Python threads for gameplay events.
4. Do not replace the right panel with a separate screen unless `current_action_content` is intentionally used.

## 13. Hard Preservation Rules

- Preserve `screen main_ui()`.
- Preserve the right-panel variables and `current_action_panel()` flow.
- Preserve `vscene` behavior for scene media.
- Preserve room-bound action modeling.
- Preserve `NPCSchedules` as canonical schedule truth.
- Preserve the separation between daily events and story threads.
- Add content in local feature/room/event files unless there is a clear shared abstraction already present.
- Do not preserve generic action hubs, dispatchers, or wrapper labels as target
  architecture when touching affected code.
