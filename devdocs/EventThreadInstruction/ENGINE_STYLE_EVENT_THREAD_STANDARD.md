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

When a blueprint or generated catalog needs to name the event object directly,
instantiate the existing runtime `Event` class. Do not invent a parallel event
row class, dict schema, wrapper, or fallback mapper. The `Event` constructor
still receives the same ordered fields:

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

`ThreadData` may later attach the real thread name and threaded flag. The
availability fields remain owned by the event object, not by a second helper.

## Readiness Conditions

Use the FamilyLife-style condition system already supported by the runtime:

- `#expression` for plain Python expression checks.
- `threadNameDone` / `!threadNameDone`.
- `threadNameAborted`.
- `threadNameEnabled`, optionally with an enabler tuple.
- `threadName_3` / `!threadName_3` for event-step progress.
- `threadNameNum == 3` / `threadNameNum != 3` for current linear step.
- Callable readiness helpers when a condition becomes too long for a readable row.

Readiness helpers must read the authoritative OOP owner:

- NPC story flags and counters from the NPC instance, for example
  `Amanda.var_int("alberfriends", 0)` or `Amanda.var.get("some_key", 0)`.
- NPC attributes from the NPC instance, for example `Amanda.corruption`,
  `Amanda.rel`, `Melissa.mana`, or `Sandra.anger_reason`.
- NPC mechanics through class methods, for example
  `Amanda.pregnancy_days()`, `Amanda.sex_stat("sexacts", 0)`, or
  `Amanda.getLocation()`.
- Player state through the Player/MC owner when the state belongs to the
  player.
- Room/object/item state through that room/object/item owner when the state
  belongs there.

Do not read story state through `globals()`, `renpy.store`, `store.*`, old
`*Var` dicts, old relationship maps such as `Friends[...]`, or duplicated
parallel dictionaries. If the state is already represented by an OOP class, the
event condition must use that class. If a helper is needed, the helper belongs
on the owner class or in the event file as a readable condition that calls owner
methods; it must not become a compatibility bridge to old global state.

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

## Thread Num As Chapters

For every ordered story thread, `thread.num` is the chapter/stage. Do not mirror
that number in `NPC.var["arc_stage"]` or another progress map.

NPC/system fields record facts that the thread does not contain, for example:

- `Werecat.var["rat_breakfast_seen"]`: a one-shot outcome used outside its thread;
- `Werecat.var["adopted_count"]`: a repeatable gameplay counter;
- `Melissa.var["temp_room"]`: the temporary room selected by the player;
- `Melissa.var["roof_repair_complete_day"]`: the day a timed repair completes.

Multiple available actions may share one ordered stage by placing multiple event
tuples in the same `LThreadData` trigger list. Only the real stage-changing
outcome calls `thread.advance()`.

Event conditions at the current step check only real facts such as location,
hour, items, outcome flags, or elapsed days. The `LThreadInfo` cursor already
selects `thread.num`; repeating that stage check in an NPC field is redundant.

This makes the story board act like a chapter map: `thread.num` identifies the
current scene group, while named facts explain why an event is waiting.

## Event Label Shape

The label should be a stable content unit:

```renpy
label story_person_arc_0:
    vscene "images/person/arc/scene_0.jpg"
    "Narrative text."

    menu:
        "Player choice text."

        "Choice A":
            $ Person.set_var_int("state", 1)
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

- direct assignment to the owner class for simple stats, flags, counters, and
  thread state
- `call` to established helper labels for shared mechanics such as
  `SlutFriendsIncrease` or `PregnancyCheck`
- a short comment block before choice-heavy labels explaining the event purpose
  and branch outcomes

Use the owner object at the point of consequence:

```renpy
$ Amanda.set_var_int("praised_after_dance", 1)
$ Amanda.rel = min(20, int(Amanda.rel or 0) + 1)
$ Amanda.mana = min(100, int(Amanda.mana or 0) + 5)
$ Player.fun = min(100, int(Player.fun or 0) + 5)
$ thread.advance()
```

If the change belongs to an NPC, it goes on that NPC class. If it belongs to the
player, it goes on the Player/MC owner. If it belongs to a room, object, or
item, it goes on that owner. The event label owns why the consequence happened;
the class owner owns the state.

Avoid:

- `jump` to helper labels that only apply a consequence
- Python evaluator methods that hide the outcome
- generic apply handlers for one event choice
- dispatcher labels that obscure which branch changed which stat
- `globals()`, `renpy.store`, `store.*`, old `*Var` dicts, old relationship
  maps, or duplicated state mirrors as normal event state

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
