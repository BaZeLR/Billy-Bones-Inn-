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

- Use `ShowImage` when ported legacy content relies on folder/name resolution.
- Use `vscene` or `SceneActionPanel` when building a new self-contained right-panel event.

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

The helper `main_ui_set_action_panel(...)` is the correct central API for changing this panel:

```renpy
$ main_ui_set_action_panel("Title", items, None, "scene")
```

Preservation rule:

- Do not replace `main_ui`.
- Do not build separate full-screen menus for normal gameplay actions.
- Use `current_action_items` plus `MenuItem` for right-panel choices.
- Use `current_action_content` only for a custom screen inside the right panel.
- Use `main_ui_set_action_panel()` when changing panel title/items/content from Python or labels.

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
- Mutating actions should call labels/functions that update variables, call `stat` if needed, then restore/rebuild UI.
- Avoid blocking native `menu:` statements for actions that must live in the right panel.

## 5. Room Model

File: `game/Inn/RoomTemplate.rpy`

`Room` is the top-level location container. It contains:

- `code_name`
- `display_name`
- `bg_picture`
- descriptions
- exits
- game objects/items
- action menus
- schedule
- scenes
- triggers
- custom properties

Related classes:

- `RoomExit`
- `RoomDescription`
- `RoomScene`
- `RoomTrigger`
- `RoomSchedule`

Important methods:

- `visible_descriptions()`
- `visible_exits()`
- `visible_objects()`
- `visible_npcs()`
- `visible_actions()`
- `visible_scenes()`
- `ready_triggers()`
- `build_menu_sections()`

Movement:

- `RoomExit` becomes a `MenuItem`.
- `MoveToRoom` and `AdvanceMovementTime` handle time cost and label jumping.

Preservation rule:

- Keep room content bound to room files.
- Do not move all actions into one global router.
- Room files may add special local actions, but should still respect `CurrentRoom`, `CurLoc`, `MainTxt`, `scene_image`, and the right-panel variables.

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

## 7. NPC Action Model

File: `game/Inn/CharacterActionHub.rpy`

NPC actions are not hidden or magic. They are driven by:

- `NPC_META`: per-NPC talk labels, examine labels, known/unknown names, supported actions.
- schedule/location presence through `getLocation()` and `getNPCids()`.
- `Room.visible_npcs()`, which asks `npc_action_data_for_room(...)`.
- right-panel menu building through `open_entity_action_menu_state(...)`.

Common NPC actions:

- look/examine
- talk
- dog talk/look
- player card

Preservation rule:

- If an NPC is present but has no action menu, check `NPC_META`, `npc_room_interaction_visible`, schedule location, and `npc_social_actions_available_in_room`.
- Do not invent hidden schedules. Use `NPCScheduleModel.rpy` and current room visibility checks.
- New NPC actions should extend `NPC_META` or the room-specific action builder, not bypass the character grid/right panel.

## 8. NPC Schedule Model

File: `game/Inn/NPCScheduleModel.rpy`

The active project schedule system is `NPCSchedules`.

Main data class:

```renpy
NPCScheduleEntry(
    location="TavernMain",
    weekdays=[1, 2, 3, 4, 5, 6, 7],
    time_slots=[0, 1, 2, 3, 4],
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

- Schedules are conditional objects (`NPCScheduleEntry`), not simple 24-slot arrays.
- Presence is resolved by priority, weekday, time slot, and conditions.
- Talk/look actions are in `CharacterActionHub.rpy`, not in `people.rpy`.
- Runtime social state is spread across project maps such as `Friends`, `Talked`, character var dicts, and action hubs.

How to combine safely:

- Treat `people.rpy` as a data-loading/reference model, not a replacement for Tractir UI/action flow.
- If importing JSON NPC data, convert schedule rows into `NPCScheduleEntry` objects or load them into `NPCSchedules`.
- Keep `CharacterActionHub.rpy` as the action-menu layer.
- Keep relationship/talk state compatible with existing project vars unless doing a planned migration.

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

## 11. Scene Action Panel Template

File: `game/Inn/SceneActionPanel.rpy`

This project now has a reusable right-panel scene/event helper:

```renpy
label some_event:
    $ _items = [
        scene_panel_call_item("Talk", "SomeTalkLabel", minutes=5),
        scene_panel_add_item("Take item", "money", 1, text="You take a coin."),
        scene_panel_jump_item("Go outside", "StreetTavern", minutes=10),
        scene_panel_return_item("Back"),
    ]
    call SceneActionPanel("images/path/to/picture.png", "Event text.", "Actions", _items)
    return
```

It does:

- optional `vscene picture`;
- sets `MainTxt` and `CurLocDesc`;
- sets right-panel items through `main_ui_set_action_panel`;
- applies variable mutations;
- advances time;
- supports `call`, `jump`, `panel`, and return/current-room modes.

Preservation rule:

- Use this for new text-game events where the player should see picture/text and choose from the right panel.
- This is the correct replacement for ad hoc blocking `menu:` when the UI must remain intact.
- It is also the correct pattern for "label + vscene path + text + actions with mutating/advancing/jump/current lock".

## 12. Implementation Rules Going Forward

For new rooms:

1. Define/update a `Room`.
2. Set `CurLoc`, `location`, `CurrentRoom`, `scene_image`, and `MainTxt`.
3. Show media with `ShowImage` or `vscene`.
4. Populate `current_action_items` with `MenuItem`.
5. Call `ReturnToMainUI` or restore the main UI state.

For new event scenes:

1. Put event text in the label, not in a hidden dispatcher.
2. Use `SceneActionPanel` for right-panel choices.
3. Mutate vars through labels/functions or `scene_panel_*_item` helpers.
4. Advance time with `calendar_advance_minutes` through the helper or explicit labels.
5. Return to room state through `main_ui_restore_room_scene_state()` or `scene_panel_return_item()`.

For NPC presence:

1. Add/adjust `NPCScheduleEntry` rows.
2. Ensure `npc_schedule_sync_currentloc()` or `npc_schedule_sync_all()` runs after time/location changes.
3. Ensure `NPC_META` has talk/look labels and actions.
4. Let `Room.visible_npcs()` and the character grid expose the action menu.

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
- Preserve `CharacterActionHub` as the NPC action menu layer.
- Preserve the separation between daily events and story threads.
- Add content in local feature/room/event files unless there is a clear shared abstraction already present.
