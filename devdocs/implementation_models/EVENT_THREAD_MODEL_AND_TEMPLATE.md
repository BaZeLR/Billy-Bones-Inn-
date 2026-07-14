# Event And Thread Model And Template

This document defines the intended event/thread implementation model.

## Purpose

Events and threads own story availability, story progress, story choices,
outcomes, and story return flow.

Events include:

- room-entry story scenes
- explicit room actions such as search/explore when story-driven
- object-triggered scenes
- NPC talk events
- tavern events
- random town events
- thread milestones
- fight-start scenes
- sex-start scenes

## Source Of Truth

Event/thread objects are the source of truth for story availability and story
progress.

Story labels are the source of truth for authored story flow.

Save/load rule: runtime `threads` and their `ThreadInfo` instances must contain
the current story state at a checkpoint: `num`, `done`, `completed`, `aborted`,
`blocked`, `blocks`, `day`, and active conditions. Loading a save restores that
state; it must not be reconstructed from separate progress dicts.

The event object owns event availability parameters. `Event.canTrigger()` checks
those parameters one by one through the event methods. Do not wrap this in an
extra `*_ready()` function that repeats the same event checks.

Classes remain authoritative for character and system state. Event conditions
may reference class state or class methods only when they express a real domain
rule that belongs to that class, not when they duplicate event availability.
For NPC stories, flags and counters live on the NPC instance, usually through
`NPC.var`, `NPC.var_int(...)`, and `NPC.set_var_int(...)`. Event/thread code
must not read or write NPC story state through `globals()`, `renpy.store`,
`store.*`, old `*Var` dicts, relationship maps such as `Friends[...]`, or
duplicated parallel state dictionaries.

Screens are not event authority. Event labels author text, pictures, choices,
and consequences. Screens may render HUD/menu areas, but do not decide event
availability, thread state, or story outcome.

## Runtime Files

Current split:

- `game/Utilities/General/Events/conditions.rpy`
  Condition parsing and checking.
- `game/Utilities/General/Events/threads.rpy`
  `ThreadData`, `LThreadData`, `RThreadData`, `UThreadData`,
  `ThreadInfo`, `LThreadInfo`, `RThreadInfo`, `UThreadInfo`,
  `loadThreadData()`, `createThreads()`, `initThreads()`.
- `game/Utilities/General/Events/events.rpy`
  `Event`, `initEvents()`, `findAvailableEvents()`,
  `initStoryEventRuntime()`, `story_event_available()`,
  `checkTriggers`, `preEvent`.
- `game/Utilities/General/Classes/StoryEventRuntime.rpy`
  Authored thread lists and event labels for now.

## Definition Flow

Event definition flow:

```text
threadList
  -> loadThreadData(threadList)
  -> threadData
  -> createThreads()
  -> threads
```

Runtime availability flow:

```text
initStoryEventRuntime()
  -> initThreads()
  -> initEvents()
  -> findBlockedThreads(threads)
  -> findAvailableEvents(True)
```

Trigger flow:

```text
room/object/NPC calls checkTriggers(location, action, numpop)
  -> findAvailableEvents(False)
  -> select availEvents[location][action]
  -> set active_event
  -> preEvent(thread_name)
  -> set thread if event is threaded
  -> jump target label
```

## Initialization Rules

Thread data is defined with `define`. Runtime thread state is defined with
`default`.

```renpy
define threadList = (
    amandaThreadList
    + melissaThreadList
    + franThreadList
)

define threadData = loadThreadData(threadList)
default threads = createThreads()
```

Runtime initialization must call:

```renpy
$ initStoryEventRuntime(True)
```

This is already called from:

```renpy
label before_main_menu:
    $ initStoryEventRuntime(True)
    return
```

and through the after-load callback.

Do not create another event initialization path. If event availability is wrong,
fix the thread definition, condition, location/action binding, or owner method.

## Thread Types

Use the correct thread type:

- `LThreadData`: linear thread. Only current step is available.
- `RThreadData`: random-order thread. One randomized step is active at a time.
- `UThreadData`: unordered thread. Any unfinished eligible step can appear.

Linear example:

```renpy
define exampleThreadList = [
    LThreadData(0, "example", "Intro", None, [
        (
            "story_example_intro_0",
            None, None, None,
            1,
            None,
            ["#not Example.intro_seen"],
            None,
            "ExampleRoom",
            "enter",
            10,
        ),
        (
            "story_example_intro_1",
            None, None, None,
            1,
            None,
            ["#Example.intro_seen", "#not Example.object_story_seen"],
            None,
            "ExampleRoom",
            "example_object",
            10,
        ),
    ], highlight=True, threaded=True),
]
```

Thread name is built as:

```text
person + subname
```

For the example above:

```text
exampleIntro
```

## New Thread Definition Procedure

When adding a new thread:

1. Choose owner key:
   - NPC key for NPC story, such as `"fran"`.
   - system key for system story, such as `"tavern"`, `"city"`, `"birth"`.
2. Create `define <owner><StoryName>ThreadList = [...]` or append to the
   existing owner thread list.
3. Add the list to `threadListsByGirl` when it should appear under that owner in
   story reports/boards.
4. Add the list to combined `threadList`.
5. Define story labels in the same story domain file or existing event label
   file.
6. Run/init through existing runtime only:

```renpy
$ initStoryEventRuntime(True)
```

Do not create a second `threads` dict, second event list, custom cache, or
parallel enabled/complete variables.

## Event Tuple

Tuple order is fixed:

```text
target, day, hour, delay, probability, requirements, conditions, item, location, action, priority
```

Thread definitions may pass either the fixed tuple above or an instance of the
existing runtime `Event` class. Use `Event(...)` only when a blueprint/catalog
needs explicit event objects; do not create wrapper event classes or dict row
schemas.

```renpy
Event(
    (
        "story_amanda_example_0",
        None, None, None,
        1,
        None,
        "amanda_example_ready()",
        None,
        "TavernMain",
        "talk",
        10,
    ),
    "",
    True,
)
```

`ThreadData` will attach the owning thread name and threaded flag when it loads
the row. Availability remains the `Event` object's job.

Field meaning:

- `target`: Ren'Py label to jump to.
- `day`: allowed weekday or weekday collection, or `None`.
- `hour`: allowed hour or hour range, or `None`.
- `delay`: day/delay gate checked against thread day.
- `probability`: `1` for guaranteed, float for chance.
- `requirements`: numeric requirements, or `None`.
- `conditions`: owner-method conditions, usually list of `"#..."` strings.
- `item`: required item id, or `None`.
- `location`: trigger location key.
- `action`: trigger action key.
- `priority`: lower number wins when several events bind same location/action.

## Event Checking Order

`Event.canTrigger()` checks:

1. event did not already fire today
2. weekday/day gate
3. hour gate
4. conditions
5. delay/day dependency
6. requirements
7. probability
8. location is open

Item is checked when the event is selected for `availEvents[location][action]`
and again in `checkTriggers()`.

If two ready events bind to the same location/action, lower `priority` wins. If
the highest-priority event needs a missing item, runtime looks for the first
ready event in that binding whose item check passes.

## Condition Rules

The event tuple is the first availability model. Use the tuple fields before
adding condition expressions:

- use `day` for weekday gates.
- use `hour` for time gates.
- use `delay` for thread-day delay gates.
- use `probability` for chance.
- use `requirements` for numeric requirements.
- use `item` for required inventory item.
- use `location` and `action` for trigger binding.
- use `priority` for conflict ordering.

The `conditions` collection is only for extra rules that do not fit those fields.
Each condition should be an atomic rule or a real owner method. It must not be a
wrapper around `Event.canTrigger()` or a repeated bundle of day/hour/item/priority
checks.

Condition owner rule:

- NPC state: `Amanda.var_int("alberfriends", 0)`,
  `Amanda.sex_stat("sexacts", 0)`, `Amanda.pregnancy_days()`,
  `Melissa.mana`, `Sandra.anger_reason`.
- Player state: Player/MC class fields or methods.
- Room/object/item state: that room/object/item owner.
- Thread state: the existing thread condition syntax or `thread` object.

Do not use old maps or store lookups as condition authority. If an old map still
exists in code, it is migration debt, not a valid model for new event/thread
definitions.

Correct:

```renpy
day=7
hour=(8, 12)
item="temple_key"
conditions=["#Francheska.visible_now()"]
```

Also correct when the method is a real class/domain rule:

```renpy
["#getPersonInfo('fran').visible_now()"]
["#ExampleObject.can_be_searched()"]
["#Clara.paintings_thread_not_aborted()"]
["#Amanda.var_int('alberfriends', 0) >= 5"]
["#Amanda.pregnancy_days() >= 120"]
```

Wrong:

```renpy
["#Francheska.sunday_stories_available()"]  # wrong if it repeats day/hour/location/event-fired checks
["#ExampleEventReady()"]                    # wrong if it duplicates Event.canTrigger()
["#FranBusy.get(time, 0) == 0"]
["#CurrentLoc.get('fran') == 'EllonaTemple'"]
["#SomeLegacyDict['stage'] > 2"]
```

Legacy dicts may appear only as temporary compatibility reads while their owner
class is not converted yet. New work must use class fields or class methods, and
converted owners must not keep a parallel old dict as authority.

If an event became unavailable because of a player choice or story outcome, put
that state on the thread or owning class and let the event condition check that
specific state. Do not add a second availability wrapper around the event.

## Location And Action Binding

Location/action binding must match the caller.

Room entry event:

```renpy
("story_example_enter_0", None, None, None, 1, None,
 ["#not Example.enter_story_seen"], None, "ExampleRoom", "enter", 10)
```

Explicit room action event:

```renpy
("story_example_search_0", None, None, None, 1, None,
 ["#ExampleRoomState.search_points >= 1", "#not ExampleRoomState.searched"], None, "ExampleRoom", "room_search", 10)
```

Object action event:

```renpy
("story_example_chest_0", None, None, None, 1, None,
 ["#ExampleChest.locked", "#not ExampleChest.story_seen"], None, "ExampleRoom", "example_chest", 10)
```

NPC talk event:

```renpy
("story_example_talk_0", None, None, None, 1, None,
 ["#Example.met", "#not Example.talk_intro_seen"], None, "talk_example", "intro", 10)
```

Alternative talk style already used in places:

```renpy
("story_example_talk_0", None, None, None, 1, None,
 ["#Example.met", "#not Example.talk_intro_seen"], None, "talk", "example", 10)
```

Pick one binding for a thread and keep it consistent with the label that calls
`checkTriggers()`.

## Checking Controls

Room entry check:

```renpy
label ExampleRoom:
    $ CurrentRoom = ExampleRoom
    $ CurLoc = CurrentRoom.code_name
    $ location = CurLoc
    $ scene_image = CurrentRoom.bg_picture or None
    if scene_image:
        vscene scene_image
    $ MainTxt = CurrentRoom.current_description_text(CurrentRoom.display_name)
    call RoomEnterEventGate(CurLoc, False)
    call screen main_ui
    return
```

Direct check when room action is story-driven:

```renpy
label ExampleRoomSearch:
    $ findAvailableEvents(True)
    call checkTriggers("ExampleRoom", "room_search", 0)
    "You search the room but find nothing unusual."
    jump ExampleRoom
```

Code after `checkTriggers()` is the fallback path for when no event fires. If an
event fires, `checkTriggers()` jumps to the event target label.

Object action check:

```renpy
label ExampleChestOpen:
    $ findAvailableEvents(True)
    call checkTriggers("ExampleRoom", "example_chest", 0)
    call ExampleChestNormalOpen
    jump ExampleRoom
```

NPC talk menu check:

```renpy
label IntExampleTalk:
    $ Example.mark_met()
    $ findAvailableEvents(True)
    call checkTriggers("talk_example", "intro", 0)

    "Normal talk text."

    menu:
        "Ask about work":
            $ Example.asked_work = 1
            jump IntExampleTalk

        "Leave":
            jump expression CurLoc
```

Use `story_event_available(location, action)` only to show/hide a button or
hint. It is a UI/projection check. The event still runs through
`checkTriggers(location, action, numpop)`, which selects the actual event.

```renpy
if story_event_available("ExampleRoom", "room_search"):
    $ current_action_items.append(MenuItem("Search the room", Call("ExampleRoomSearch")))
```

## Story Label Template

The story label owns picture, text, menu choices, consequences, thread movement,
and return.

```renpy
label story_example_intro_0:
    vscene "images/example/intro_0.png"

    "Story text."

    menu:
        "Help":
            $ Example.helped_intro = True
            call SlutFriendsIncrease("amanda", 4, 1, 1, 18, 1, 1)
            $ calendar_advance_minutes(20)
            $ thread.advance()
            $ findAvailableEvents(True)
            jump ExampleRoom

        "Refuse":
            $ Example.refused_intro = True
            $ calendar_advance_minutes(5)
            $ thread.abort()
            $ findAvailableEvents(True)
            jump ExampleRoom
```

Rules:

- Use `vscene` for event pictures.
- Use normal Ren'Py text and `menu`.
- Mutate class instances or correct system owners directly.
- Use `call` for returnable helper procedures.
- Use `jump` for continuation or room return.
- Use `thread.advance()` only when this thread step is completed.
- Use `thread.complete()` only when whole thread is completed.
- Use `thread.abort()` only when branch ends the thread.
- Refresh availability after changing thread state when player remains in UI.

## Multi-Beat Story Label

Use authored beats, not queued text wrappers.

```renpy
label story_example_intro_1:
    vscene "images/example/intro_1_a.png"
    "First beat."

    menu:
        "Continue":
            pass

    vscene "images/example/intro_1_b.png"
    "Second beat."

    menu:
        "Continue":
            pass

    vscene "images/example/intro_1_c.png"
    "Final beat."

    $ Example.intro_seen = True
    $ thread.advance()
    $ findAvailableEvents(True)
    jump ExampleRoom
```

## Fight Start Event Template

Event label owns story lead-in. Fight system owns fight state.

```renpy
label story_example_ambush:
    vscene "images/example/ambush.png"
    "Story text leading to combat."

    menu:
        "Fight":
            $ fight_begin("street_crook", 2, "ExampleRoom", "images/example/ambush.png", "Combat intro text.")
            $ thread.advance()
            $ findAvailableEvents(True)
            jump ExampleRoom

        "Run":
            $ Example.ambush_escaped = True
            $ calendar_advance_minutes(10)
            jump ExampleRoom
```

## Sex Start Event Template

Event label owns story lead-in and consent/choice. Sex engine owns sex state.
Use the real sex label for that character or the paid-sex module that already
exists for that context. Do not invent a generic sex dispatcher in the event
thread layer.

```renpy
label story_melissa_sex_start_example:
    vscene "images/example/sex_start.png"
    "Story text."

    menu:
        "Continue":
            $ Melissa.story_flags["event_sex_started"] = True
            call IntMelissaSex("melissa", CurLoc)
            $ thread.advance()
            $ findAvailableEvents(True)
            jump expression CurLoc

        "Stop":
            jump expression CurLoc
```

## Projection And Reports

`findAvailableEvents()` also updates read-only projection values:

- `eventLocations`
- `eventPeople`
- `eventTalk`
- `eventOptions`
- `eventItems`
- `eventPath`
- `eventProjectionRows`
- `eventRouteHints`

These are for HUD hints, story board, reports, and debug. They must not become
state owners.

## Highlighting Maps And Status Signals

The game also keeps visual highlighting/status data that says what can be
started, what is active, what is completed, and what is blocked or aborted by
player/story choices.

These signals are derived from thread/event state. They are not separate story
state.

Current projection/highlight maps:

- `eventLocations`: locations with currently available projected events.
- `eventPeople`: people connected to currently available events.
- `eventTalk`: people with currently available talk-style events.
- `eventOptions`: currently available non-enter actions.
- `eventItems`: missing required items for projected events.
- `eventPath`: first route steps toward available event locations.
- `eventRouteHints`: target location to first route step.
- `eventProjectionRows`: readable rows for HUD/report/story-board use.

Thread status is derived from:

- `thread.completed`
- `thread.aborted`
- `thread.blocked`
- `thread.checkActive()`
- `thread.num`
- `thread.done[index]`
- `thread.blocks[index]`

Story board color map:

```python
STORY_BOARD_COLORS = {
    "done": green,
    "active": blue,
    "available": white,
    "waiting": gold,
    "future": gray,
    "blocked": purple,
    "aborted": red,
    "complete": green,
}
```

Meaning:

- `available`: current event step can be triggered now.
- `active`: thread is active but current event may still wait on event fields.
- `done`: event step is completed.
- `complete`: whole thread is completed.
- `blocked`: event/thread is blocked by dependency or story condition.
- `aborted`: player/story choice ended the thread.
- `waiting`: current step exists but event fields are not all true yet.
- `future`: later step or inactive future thread.

Do not manually set color/status maps to fake progress. Change the owning state:

- use `thread.advance()` to complete current step.
- use `thread.complete()` to complete whole thread.
- use `thread.abort()` when player/story choice aborts it.
- change the owning class/system field when story condition changes.
- call `findAvailableEvents(True)` afterward when UI should refresh.

## Explicit State Checks

Thread state is checked in `game/Utilities/General/Events/threads.rpy`.

Thread-level state:

- `ThreadInfo.checkActive()`
  Checks thread level/person gate, thread conditions, aborted state, and
  completed state.
- `ThreadInfo.checkBlocks()`
  Checks whether thread-level or event-level conditions block future progress.
- `ThreadInfo.statusText()`
  Returns thread status text from thread state.
- `ThreadInfo.currentTarget()`
  Returns the current event target for the current thread index.

Event-step state:

- `LThreadInfo.getAvailableEvents()`
  Checks only current `thread.num` event list.
- `RThreadInfo.getAvailableEvents()`
  Checks randomized current event list.
- `UThreadInfo.getAvailableEvents()`
  Checks every unfinished event list.

Each of those calls `evt.canTrigger(thread.day)`. That is the explicit event
availability check.

Event object checks are in `game/Utilities/General/Events/events.rpy`:

- `Event.canTrigger(evtDay)`
- `Event.checkDay()`
- `Event.checkHour()`
- `Event.checkConditions()`
- `Event.checkNumDay(evtDay)`
- `Event.checkReqs()`
- `Event.checkProb()`
- `Event.checkItem()`
- location-open check

`findAvailableEvents()` connects thread state to event selection:

```text
for each thread_info in threads:
    tmp_events += thread_info.getAvailableEvents()

group by event.location/event.action
sort by priority
choose first event whose item check passes
write availEvents
project read-only board/report rows
```

## Visual Story Board Connection

Visual story board lives in:

```text
game/Utilities/General/Screens/StoryThreadBoard.rpy
```

It does not own thread or event state. It reads `threads`, `threadData`,
`threadListsByGirl`, and `eventProjectionRows`.

Refresh path:

```text
story_board_refresh()
  -> initStoryEventRuntime(True)
  -> findBlockedThreads(threads)
  -> findAvailableEvents(True)
```

Thread rows:

```text
story_board_rows(person)
  -> threadListsByGirl/person order
  -> threads[name]
```

Thread color/status:

```text
story_board_thread_status(tinfo)
  -> completed
  -> aborted
  -> blocked
  -> tinfo.checkActive()
  -> future
```

Event cell color/status:

```text
story_board_event_status(tinfo, index)
  -> tinfo.done[index]
  -> tinfo.aborted
  -> tinfo.blocks[index]
  -> tinfo.completed
  -> index == tinfo.num and tinfo.checkActive()
       -> story_board_event_available(tinfo, index)
            -> evt.canTrigger(tinfo.day)
  -> future/waiting
```

Hover details:

```text
story_event_screen(tinfo, index, evt)
  displays evt.target
  displays evt.location / evt.action
  displays evt.item
  displays evt.evtDay / evt.day / evt.hour
  displays evt.reqs
  displays evt.conds
  displays evt.prob
```

The story board is therefore a read-only control/inspection surface. It should
not change `thread.num`, `thread.done`, `thread.completed`, event fields, or NPC
state. Actual progression happens only in story labels through
`thread.advance()`, `thread.complete()`, `thread.abort()`, or explicit thread
methods.

## Utilities

Allowed event/thread utilities:

- `initThreads()`
- `initEvents()`
- `initStoryEventRuntime(force)`
- `findAvailableEvents(forced)`
- `story_event_available(location, action)`
- `checkTriggers(location, action, numpop)`
- `RoomEnterEventGate(location, force)`
- story board/projection read-only helpers
- returnable helper labels for shared consequences

Utilities must not:

- hide story consequences.
- replace authored Ren'Py menus.
- create generic apply handlers for one event.
- own story text.
- own event pictures.
- own room/NPC/player state beyond calling public methods.

## Controls

Event controls are player choices inside event flow.

Examples:

- accept
- refuse
- help
- attack
- escape
- flirt
- search
- continue
- finish scene

Event controls mutate the correct owner:

- NPC state through NPC class instance.
- player state through player model.
- room-object state through object.
- time through calendar/time system.
- fight start through fight system.
- sex start through sex engine.
- thread progress through thread object.

## Forbidden Patterns

Do not implement events through:

- screens owning story logic.
- refresh/rebuild labels.
- handler labels for one button.
- generic event dispatcher when direct label is enough.
- queued text systems replacing authored labels.
- room-owned event consequences.
- duplicate thread state in dicts.
- legacy NPC dicts as condition authority.
- hidden fallbacks that mask broken event conditions.

## Implementation Checklist

For each event/thread:

- [ ] Thread owner is clear.
- [ ] Thread type is correct: linear, random, or unordered.
- [ ] Thread name is predictable from `person + subname`.
- [ ] Event tuple fields are in exact order.
- [ ] Location/action match the actual `checkTriggers()` call.
- [ ] Condition calls real owner methods.
- [ ] Required item is explicit or `None`.
- [ ] Priority is intentional.
- [ ] Event label exists.
- [ ] Event label uses `vscene` for event picture.
- [ ] Event label owns text and choices.
- [ ] Consequences mutate correct owner.
- [ ] Shared helper calls use `call`.
- [ ] Continuation/return uses `jump`.
- [ ] Thread advances/completes/aborts only at real outcome.
- [ ] Availability refresh happens after thread state changes if needed.
- [ ] Screen only displays.
- [ ] Projection/report data stays read-only.
- [ ] No wrapper/dispatcher/rebuild layer.
