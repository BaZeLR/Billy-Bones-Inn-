# Engine-Style Event And Thread Standard

Use the reference-engine shape for new story content:

1. A thread row declares the start point directly.
2. The target label owns the media, text, menus, state mutation, and thread advance.
3. Room code only offers or calls the trigger. It must not hide extra story conditions.

For the content-authoring form of this rule, including ordinary Ren'Py menus, direct variable updates, room-entry checks, and anger/apology examples, see `devdocs/EventThreadInstruction/STORY_LABEL_EVENT_FLOW_STANDARD.md`.

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
            $ thread.advance()
            jump TavernKitchen
```

For events that must keep the right-side HUD visible, keep the same authored
label ownership and let the screen layer place the Ren'Py menu in the right
action area:

```renpy
label story_person_arc_0:
    vscene "images/person/arc/scene_0.jpg"
    "Narrative text."

    menu:
        "Continue":
            $ thread.advance()
            jump TavernKitchen

        "Leave":
            jump TavernKitchen
```

Do not replace this with `current_action_items`, `main_ui_set_action_panel`,
`SceneActionPanel`, queued panels, refresh/apply/renew labels, or distant
dispatchers.

## Consequence Visibility

Threaded event labels must keep consequences visible in the label.

Preferred:

- direct assignment for simple stats, flags, counters, and thread state
- `call` to established helper labels for shared mechanics such as
  `SlutFriendsIncrease` or `PregnancyCheck`
- a short comment block before choice-heavy labels explaining the event purpose
  and branch outcomes

Avoid:

- `jump` to helper labels that only apply a consequence
- Python evaluator methods that hide the outcome
- generic apply handlers for one event choice
- dispatcher labels that obscure which branch changed which stat

The reader should be able to inspect the event label and understand what each
choice changes without chasing a handler chain.

## Multi-Picture Beats

Threaded events may contain several pictures. Keep those pictures as authored
beats in the target label:

```renpy
label story_person_arc_1:
    vscene "images/person/arc/1.jpg"
    "Beat one."

    vscene "images/person/arc/2.jpg"
    "Beat two."

    menu:
        "Continue":
            pass

    vscene "images/person/arc/3.jpg"
    "Beat three."

    $ thread.advance()
    jump TavernKitchen
```

Do not use a queue/paging/proceed subsystem for authored story or sex scenes
when a direct sequence of `vscene`, text, and a simple `Continue` menu is enough.

## Advance And Complete

Family Life sets the active `thread` in `preEvent(thread_name)` before jumping
to the event label. Advance, complete, or abort that active thread directly in
the event label, after the player has accepted the consequence:

```renpy
$ thread.advance()
```

```renpy
$ thread.complete()
```

```renpy
$ thread.abort()
```

Do not advance in the room entry code. Room entry only triggers:

```renpy
call checkTriggers("TavernKitchen", "enter", 0)
```

## Room Consistency

Rooms should use their registered room picture for normal browsing and `vscene` or `ShowImage` only inside an event label. If an event changes the picture, that label must also set the text/menu state it expects. This prevents stale text and wrong pictures from leaking between rooms.
