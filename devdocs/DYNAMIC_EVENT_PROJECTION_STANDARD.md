# Dynamic Event Projection Standard

Tractir keeps its existing OOP thread/event definitions, but now projects available story events into runtime UI/debug signals after `findAvailableEvents()`.

The source of truth is still:

- `threadList`
- `threadData`
- `threads`
- `StoryEventRuntime.Event`
- `StoryEventRuntime.ThreadInfo`

The dynamic projection layer derives:

- `eventLocations`: rooms where currently available story events can happen
- `eventPeople`: people connected to available story events
- `eventTalk`: people with available talk-style story events
- `eventOptions`: non-enter actions exposed by active story events
- `eventItems`: missing items required by active story events
- `eventPath`: first navigation steps toward active event locations
- `eventProjectionRows`: readable rows for story board and runtime tests
- `eventRouteHints`: mapping from target event location to first route step

This follows the useful FamilyLife pattern without replacing Tractir's current thread classes.

## Practical Use

After adding a thread event:

1. Keep the event tuple explicit: target, condition, item, location, action, priority.
2. Run lint.
3. Open the story board.
4. Check `ACTIVE EVENT PROJECTION`.
5. Run `python tools/runtime_logic_tests.py`.

If an event is ready but does not show in projection, its `location` or `action` is probably too vague or its condition is not actually true in the current game state.

## Naming Guidance

Use direct room codes for room events:

```renpy
("some_label", None, None, None, 1, None, some_ready_fn, None, "TavernKitchen", "enter", 0)
```

Use `*_talk` actions for talk events tied to a real room:

```renpy
("some_talk_label", None, None, None, 1, None, some_ready_fn, None, "TavernMain", "melissa_talk", 6)
```

Use non-`enter` action names for explicit menu actions:

```renpy
("some_label", None, None, None, 1, None, some_ready_fn, None, "TavernAtic", "melissa_bats", 2)
```
