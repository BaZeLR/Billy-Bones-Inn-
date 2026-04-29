# Engine-Style Event And Thread Standard

Use the reference-engine shape for new story content:

1. A thread row declares the start point directly.
2. The target label owns the media, text, menus, state mutation, and thread advance.
3. Room code only offers or calls the trigger. It must not hide extra story conditions.

## Thread Row Shape

Use the existing `LThreadData` / `RThreadData` / `UThreadData` classes in `game/Inn/StoryEventRuntime.rpy`.

```renpy
LThreadData(0, "melissa", "ExampleArc", None, [
    (
        "story_melissa_example_0",
        None, None, None,
        1,
        None,
        melissa_example_ready,
        None,
        "TavernKitchen",
        "enter",
        0,
    ),
], highlight=False, threaded=True)
```

Do not add wrapper classes for events or threads. `ThreadData.__init__()` already initializes the runtime `Event` objects and gives them the owning thread name and `threaded` flag.

Event tuple order:

`target, day, hour, delay, probability, reqs, condition, item, location, action, priority`

Keep condition logic in named callable readiness methods when a condition becomes long.

## Readiness Conditions

Use the FamilyLife-style condition system already supported by the runtime:

- `#expression` for plain Python expression checks.
- `threadNameDone` / `!threadNameDone`.
- `threadNameAborted`.
- `threadNameEnabled`, optionally with an enabler tuple.
- `threadName_3` / `!threadName_3` for event-step progress.
- `threadNameNum == 3` / `threadNameNum != 3` for current linear step.
- Callable readiness helpers when a condition becomes too long for a readable row.

Good condition value inside the existing tuple:

```renpy
("story_clara_market_booklet_4", None, None, None, 1, None, clara_market_booklet_4_ready, None, "WineStore", "clara_talk", 4)
```

Avoid:

```renpy
condition="str(_story_current_location() or '') == 'WineStore' and int(ClaraVar.get('mongol_theft_seen', 0) or 0) == 1 and ..."
```

Long strings hide mistakes, especially wrong room names and missing helper functions.

If multiple event alternatives are grouped in one thread step, that step is blocked only when all alternatives are blocked. This matches the FamilyLife `checkBlocksList` behavior.

## Story Flags As Chapters

Use story flags and counters as readable chapter markers, not as scattered one-off booleans.

Good examples:

- `MelissaVar["bats_episode"]`: ordered chapter number for the bat problem.
- `WerecatVar["rat_breakfast_seen"]`: one-shot scene gate.
- `WerecatVar["adopted_count"]`: repeatable progression counter.
- `ClaraVar["paintings_stage"]`: ordered investigation branch stage.

When adding an arc, prefer:

```renpy
SomeVar["arc_stage"] = 0
SomeVar["arc_scene_seen"] = 0
SomeVar["arc_repeat_count"] = 0
SomeVar["arc_last_day"] = -1
```

Then point thread rows at those markers through explicit readiness helpers:

```renpy
def some_arc_scene_2_ready():
    return SomeVar["arc_stage"] == 2 and SomeVar["arc_last_day"] != dayspassed
```

This makes the story board act like a chapter map. A human should be able to read the flags and understand which scene is next, which scenes repeat, and which branch has already locked or completed.

## Event Label Shape

The label should be a stable content unit:

```renpy
label story_person_arc_0:
    vscene "images/person/arc/scene_0.jpg"
    "Narrative text."

    menu:
        "Player choice text."

        "Choice A":
            $ SomeVar["state"] = 1
            jump story_person_arc_0_choice_a

        "Leave":
            $ story_thread_advance_current()
            jump TavernKitchen
```

For right-panel UI events, keep the same ownership:

```renpy
label story_person_arc_panel_0:
    $ MainTxt = "Text visible in the left panel."
    $ CurLocDesc = MainTxt
    $ current_action_items = [
        MenuItem("Continue", Call("story_person_arc_panel_0_continue")),
        MenuItem("Return", Call("TavernKitchenRestore")),
    ]
    call ShowImage("", "", "images/person/arc/scene_0.jpg")
    call ReturnToMainUI
    return
```

## Advance And Complete

Advance the active thread in the event label, after the player has accepted the consequence:

```renpy
$ story_thread_advance_current()
```

Do not advance in the room entry code. Room entry only triggers:

```renpy
call checkTriggers("TavernKitchen", "enter", 0)
```

## Room Consistency

Rooms should use their registered room picture for normal browsing and `vscene` or `ShowImage` only inside an event label. If an event changes the picture, that label must also set the text/menu state it expects. This prevents stale text and wrong pictures from leaking between rooms.
