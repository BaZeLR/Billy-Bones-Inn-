# Room Model And Template

This document defines the intended room implementation model.

## Purpose

Rooms are physical or logical locations the player can enter.

Examples:

- tavern main room
- kitchen
- market place
- port streets
- church
- Ellona temple
- hunter club
- forest clearing

## Source Of Truth

The room object is the source of truth for room structure.

A room owns:

- code name
- display name
- room group
- optional open/closed schedule for venues only
- hidden/locked/open booleans
- default room picture
- time-dependent room picture rules
- default room description
- first-visit description
- situational descriptions that can append to or replace the default
- navigation exits
- placed game objects/items
- explicit custom room actions, only when the room itself is the target
- hosted event checks

A room does not own NPC presence, normal gameplay actions, object/item actions,
or story flow. Actions belong to objects, game items, NPCs, or events.

## Room Features

Every room should define:

- `code_name`: stable room id.
- `display_name`: player-facing name.
- `group_name`: tavern, city, forest, or other.
- `schedule`: open hours or always-open state.
- `is_hidden`: direct boolean; hidden rooms do not expose navigation links.
- `is_locked`: direct boolean; locked rooms block entry or expose lock-specific text/menu.
- `open_override`: direct boolean-or-None only when a room needs a runtime open/closed override.
- `bg_picture`: default picture.
- `descriptions`: conditional text.
- `exits`: navigation targets.
- `game_items` or `objects`: visible interactable objects.

Rooms have an empty action list by default. Add a room-owned action only when this
specific room is itself the target of that action, and document the reason in
the room file near the action definition.

## Schedule Rules

Use explicit clock intervals. Do not use old time-slot lists for room schedule.

Always-open rooms do not define a schedule. Streets, alleys, upstairs corridors,
and other physical navigation rooms are open by default:

```renpy
schedule=None
```

Preferred open-hours room schedule:

```renpy
RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6], start="06:00", end="17:59", closed_text="Closed text.")
```

Use named arguments:

```text
weekdays, closed_text, condition, start, end
```

## Room Template

```renpy
init python:
    ExampleRoom = Room(
        code_name="ExampleRoom",
        display_name="Example Room",
        bg_picture="images/example/default.png",
        group_name=ROOM_GROUP_CITY,
        schedule=RoomSchedule(weekdays=[1, 2, 3, 4, 5, 6, 7], start="00:00", end="23:59"),
        descriptions=[
            RoomDescription("Room description text."),
        ],
        exits=[
            RoomExit("Back", "MarketPlace", minutes_to_pass=5),
        ],
        game_items=[
            "example_object_001",
        ],
    )
    register_room_runtime(ExampleRoom)
```

## Room Entry Label Template

Room entry label sets current location, checks room-entry events/spawns, chooses
the room picture/text, and calls the UI. It does not own object, item, NPC, or
event actions.

Main UI invariant:

- Room labels, object labels, and event labels that happen inside a location
  must preserve the main UI composition: left title/media/text plus the intact
  right HUD/actions/characters panel.
- Do not `hide screen main_ui` for room-like interaction labels.
- Do not create a second full-screen UI or modal action hub for ordinary room,
  object, NPC, or event choices.
- Returning to the owning room label redraws the room. No refresh/rebuild/restore
  label is part of the architecture.

```renpy
label ExampleRoom:
    $ CurrentRoom = ExampleRoom
    $ CurLoc = CurrentRoom.code_name
    $ location = CurLoc
    call RoomEnterEventGate(CurLoc, False)
    $ ExampleRoom.check_spawns()
    $ scene_image = CurrentRoom.bg_picture or None
    if scene_image:
        vscene scene_image
    $ MainTxt = CurrentRoom.current_description_text(CurrentRoom.display_name)
    call screen main_ui
    return
```

## Visible Objects

Room lists objects. Object owns actions.

Correct:

```renpy
game_items=["example_chest_001"]
```

Then object menu owns:

- open
- search
- take
- clean
- use

Object menu labels use direct Ren'Py action lists in the right-side action
section. The object label sets `current_action_title`, `MainTxt`, optional
`_layout_last_picture`, and `current_action_items` directly. Each choice calls
or jumps to the owning object/item/event label. Do not route object choices
through generic hubs, handler labels, or rebuild wrappers.

Wrong:

- room has action `Open chest`.
- room label mutates chest state directly.

Exception: room can own custom actions only when the room itself is acted on.
These actions must be explicit and rare.

Allowed room-owned action examples:

- clean this room
- search this room
- examine this room
- explore this area

These actions may be gated by chores, exploration points, event flags, or story
state. If the action targets an object, NPC, or event, it does not belong to the
room.

Examples:

- upstairs rooms can expose `clean room` as a chore.
- a suspicious room can expose `search room` gated by exploration points.
- an event can expose `search` inside its own label when the search is part of
  that story event.

## NPC Presence

Room does not own NPCs.

NPC presence is derived from NPC class instances and schedule/event location
state:

```python
getLocation("fran") == current_location
```

The HUD/visible NPC panel builds the current NPC list from the current location:

Correct:

```python
getNPCids(current_location)
```

Selecting an NPC in the HUD opens that NPC's interaction menu. The room does not
own this action; the NPC or its talk/event label owns it.

NPCs in events are authored by the event label. If an event plays in a room with
some NPC, the event label owns that NPC's story flow for that event.

If a room-entry event temporarily moves or reveals an NPC, it must do so through
the NPC/event state that affects `getLocation()`, not by adding the NPC to a room
list.

Wrong:

- room lists NPC ids as authoritative contents.
- room writes `CurrentLoc["fran"]`.
- room sets `FranVar["meet"]`.
- room derives NPC identity from dicts.
- room treats legacy NPC dicts as authoritative.
- room exposes a `visible_npcs()` method as NPC authority.

## Hosted Events

Room may host event checks, but event/thread system owns story availability and
event labels own flow.

Room entry can call:

```renpy
call RoomEnterEventGate(CurLoc, False)
```

Room object action can call a specific event check when object action is the
trigger.

## Utilities

Allowed room utilities:

- `register_room_runtime(room)`
- `get_registered_room(room_code)`
- `room_group(room_code)`
- `room_in_group(room_code, group_name)`
- `RoomSchedule.is_open(week_value, time_value)`
- `Room.current_description_text(...)`
- `Room.visible_objects()`

Utilities must not:

- rebuild room action state through refresh labels.
- create recursive menu loops.
- mutate NPC story state.
- compute NPC presence from room-owned NPC lists as authority.
- own object action consequences.
- own event story flow.

## Controls

Room controls are:

- navigation exits
- visible object buttons
- explicit room action buttons, only when room itself is target
- visible hosted event entry if event system says available

Controls should be rendered by screens from room state. Screens must not decide
room state.

NPC buttons are HUD/panel controls derived from NPC class state, not room
controls.

Returning to the room label is enough to redraw the location after a mutation.
Do not introduce refresh/rebuild/apply/renew/restore labels to redisplay room
state.

## Forbidden Patterns

Do not implement rooms through:

- room-owned NPC actions.
- room-owned NPC presence as authority.
- room-owned object actions.
- old `time_slots=[...]` room schedule.
- named schedule arguments when constructor order is required.
- refresh/rebuild labels.
- restore/apply/renew labels.
- wrapper labels whose only job is to redisplay same room menu.
- bridge/shim/fallback maps between old dict state and class state.
- duplicated location variables that drift.
- direct NPC state mutation in room labels.
- screens mutating room/game state.

## Implementation Checklist

For each room:

- [ ] Room object exists.
- [ ] Room registered once.
- [ ] Schedule uses clock interval.
- [ ] Closed text exists if room can close.
- [ ] Room entry label sets current room/location.
- [ ] Room picture uses room picture for browsing.
- [ ] Event images are in event labels, not room browsing.
- [ ] Exits are navigation only.
- [ ] Objects are listed as objects.
- [ ] NPC presence comes from NPC class `getLocation()`/visibility.
- [ ] No normal gameplay action belongs to room.
- [ ] Room custom actions are explicit and target the room itself.
- [ ] No room rebuild/refresh wrapper.
