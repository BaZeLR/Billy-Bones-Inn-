# Story Label Event Flow Standard

This is the preferred content-authoring standard for story scenes, NPC interactions, and threaded events.

The goal is to make game content easy to write and debug: event availability is checked by the existing thread/event engine, while the actual story label uses ordinary Ren'Py text, menus, direct state updates, and explicit thread progression.

## Core Rule

- The thread/event tuple decides whether a scene is available.
- The room checks available events when the player enters or uses a room action.
- The story label owns the text, pictures, menus, consequences, and return flow.
- The story label advances or completes the thread only when the story condition is actually met.

Do not add wrapper labels, handler methods, refresh labels, rebuild labels, dispatcher layers, or Python methods that duplicate a simple Ren'Py menu.

This rule prevents repetitive bugs. If a label, room, or event does not work, fix the direct owner of that behavior instead of adding a fallback path around it. A fallback or wrapper may appear to solve the immediate click, but it creates a second hidden flow that later goes stale and makes the next bug harder to trace.

## Room Event Check

On room entry, refresh available events and let the event engine choose the highest priority event for that location/action.

```renpy
label TavernKitchen:
    $ CurLoc = "TavernKitchen"
    $ findAvailableEvents(forced=True)
    call checkTriggers("TavernKitchen", "enter", 0)

    "Normal room text."

    menu:
        "Look around":
            jump TavernKitchen

        "Leave":
            jump TavernMainHall
```

For object actions, use the same pattern with a clear action key:

```renpy
label TavernMainHallBar:
    $ findAvailableEvents(forced=True)
    call checkTriggers("TavernMainHall", "bar", 0)

    menu:
        "Listen to story":
            jump TavernMainHallBarListen

        "Back":
            jump TavernMainHall
```

The location/action values in the tuple must match the values used by `checkTriggers()`.

## Event Tuple

Define the event through `LThreadData`, `RThreadData`, or `UThreadData`.

```renpy
LThreadData(0, "melissa", "Rat", None, [
    (
        "MelissaRat_0",
        None,
        None,
        None,
        1,
        None,
        melissa_rat_0_ready,
        None,
        "TavernKitchen",
        "enter",
        0,
    ),
], highlight=False, threaded=True)
```

Tuple order:

```text
target, day, hour, delay, probability, requirements, conditions, item, location, action, priority
```

Use explicit values. If the event depends on time, weekday, location, flags, or another thread, put that condition in the tuple or in a readable readiness function. Do not hide important gates inside unrelated wrappers.

## Label Shape

Use direct Ren'Py story flow.

```renpy
label MelissaRat_0:
    show screen main_ui

    "You hear Melissa scream from the basement."

    menu:
        "Check it out":
            $ minutes += 5
            jump MelissaRat_1

        "Ignore it":
            "You decide not to get involved."
            $ minutes += 5
            $ melissa.anger_reason = "ignored_basement_scream"
            $ melissa.anger_days = 2
            $ melissa.friends["you"] -= 10
            jump expression CurLoc
```

## Event Menu Display

Event menus must stay visible inside the active event scene. This rule is
mandatory for story events and sex events.

Reference pattern from Family Life sex-event files:

```renpy
label nikkiSex_0:
    vscene "images/event0/Nikki/Sex/0. Sex neighbor/1.jpg"
    "Event text."

    menu:
        "Buy":
            $ hour += 1
            $ thread.advance()
            jump adams_pool

        "Not a chance":
            jump nikkiSex_End
```

For Tractir, the visual result must match the event layout shown in gameplay:

```text
event picture + event text remain visible
event choices appear in the right-side event/action area
status and character panels remain in their normal places
```

Do not move choices to a detached overlay, queued panel, refresh label, apply
label, or Python dispatcher. If `main_ui` is used to render choices, those
choices must still be authored at the event point and must appear in the event
panel while the event picture/text remains visible.

## Multi-Picture Events

For linear events with several pictures, keep the scene as a sequence of
authored beats in one label or in real branch sublabels.

Family Life pattern:

```renpy
label some_sex_event_1:
    vscene "images/event/part_1.jpg"
    "First beat."

    vscene "images/event/part_2.jpg"
    "Second beat."

    menu:
        "Continue":
            pass

    vscene "images/event/part_3.jpg"
    "Third beat."

    $ thread.advance()
    jump SomeRoom
```

Use a `Continue` / `Продолжить` menu only as an explicit authored pause between
beats. The selected branch should usually just `pass`, then the label continues.

Do not replace this with:

- automatic text queues
- `QueuePagedPanelText`
- `AdvancePagedPanelText`
- generic proceed/apply labels
- handler labels whose only job is to show the next paragraph

If Tractir must render the proceed button through `main_ui`, it must still
represent the next authored beat of the same event, not a generic paging system.

## Consequence Ownership

Event labels own their consequences.

For simple effects, mutate the state directly inside the branch where the
choice happens:

```renpy
menu:
    "Help her":
        $ Clara.rel = min(20, int(Clara.rel or 0) + 1)
        $ Clara.set_var_int("helped_market", 1)
        $ Player.fun = max(0, int(Player.fun or 0) - 5)
        $ calendar_v2.advance_minutes(20)
        $ thread.advance()
        jump MarketPlace
```

For established shared mechanics, call the real Ren'Py helper label directly:

```renpy
menu:
    "Praise Amanda":
        call SlutFriendsIncrease("amanda", 4, 1, 1, 18, 1, 1)
        $ Amanda.set_var_int("praised_after_dance", 1)
        jump TavernMain
```

Use `call`, not `jump`, for helper labels that calculate or apply consequences.
The event branch must remain the visible owner of why the helper was called.

The owner class is the state authority. Event labels may call shared mechanics,
but normal state writes must go to the object that owns the state:

```renpy
$ Amanda.set_var_int("legare_dance_private_seen", 1)
$ Amanda.rel = min(20, int(Amanda.rel or 0) + 1)
$ Amanda.mana = min(100, int(Amanda.mana or 0) + 5)
$ Player.fun = min(100, int(Player.fun or 0) + 5)
```

Do not use `globals()`, `renpy.store`, `store.*`, old `*Var` dicts, old
relationship maps such as `Friends[...]`, or duplicated state mirrors as normal
event/talk state.

Do not hide consequences behind:

- Python evaluator methods
- dispatcher methods
- generic apply handlers
- refresh/rebuild labels
- labels whose only job is to route to one other consequence

If a story label has meaningful choices, place a short comment block before the
label:

```renpy
# Event: Amanda reacts after Legare's dance invitation.
# Choices:
# - defend Amanda: raises Amanda.rel, lowers Legare cooperation, advances thread
# - pressure Amanda: raises Amanda.corruption through the Amanda/shared sex mechanic
# - refuse involvement: leaves follow-up available tomorrow
label event_amanda_legare_dance_choice:
    ...
```

Submenus and sublabels are fine when they are real story branches:

```renpy
label MelissaRat_1:
    show screen main_ui

    "In the basement, Melissa is backed against a wall while something moves in the dark."

    menu:
        "Kill the rat":
            "You deal with the rat before it can hurt anyone."
            $ minutes += 20
            $ fun += 5
            $ thread.advance()
            jump expression CurLoc

        "Leave it":
            "Melissa stares at you in disbelief."
            $ minutes += 5
            $ melissa.anger_reason = "left_rat_problem"
            $ melissa.anger_days = 2
            $ melissa.friends["you"] -= 10
            jump expression CurLoc
```

## Thread Progression

Family Life's event engine calls `preEvent(thread_name)` before jumping to the
event label. `preEvent` sets the active `thread` object:

```renpy
if thread_name:
    $ thread = threads[thread_name]
    $ thread.setDay()
else:
    $ thread = None
```

The content label then advances, completes, or aborts that active thread
directly after the player reaches the relevant beat.

```renpy
$ thread.advance()
```

or:

```renpy
$ thread.complete()
```

or:

```renpy
$ thread.abort()
```

Do not advance or complete the thread in room entry code. Room entry only discovers and triggers events.

Repeatable investigation scenes should not advance until the success gate is met:

```renpy
label ClaraMarketSpy_0:
    show screen main_ui

    if explorations < 100:
        "You try to follow Clarissa, but she disappears into the market crowd."
        $ minutes += 30
        $ explorations += 1
        $ fun += 10
        jump MarketPlace

    "You follow Clarissa to a merchant at the far end of the market."
    $ Clara.set_var_int("booklet_flag", 1)
    $ Mongol.set_var_int("conspiration_flag", 1)
    $ thread.complete()
    jump MarketPlace
```

## NPC Menus

NPC interaction labels should be ordinary event-like menus with direct checks.
The `talk` room/NPC action opens this label; the label owns the visible
conversation choices, pictures, text, consequences, and return flow.

```renpy
label MelissaTalk:
    show screen main_ui

    if melissa.anger_reason:
        jump MelissaComplaintMenu

    "Melissa waits for you to speak."

    menu:
        "Talk about safety" if not social_topic_already_seen("melissa", "talk", "melissa_safety"):
            $ Melissa.talked = int(Melissa.talked or 0) + 1
            $ Melissa.talked_today = int(Melissa.talked_today or 0) + 1
            $ Melissa.set_var_int("talk_topic_melissa_safety_seen", 1)
            $ Melissa.rel = min(20, int(Melissa.rel or 0) + 1)
            jump MelissaTalk

        "Flirt" if Melissa.rel >= 10 and Melissa.var_int("flirted_today", 0) == 0:
            $ Melissa.set_var_int("flirted_today", 1)
            call SlutFriendsIncrease("melissa", 4, 1, 1, 5, 1, 0)
            jump MelissaTalk

        "Gift" if Melissa.rel >= 10:
            jump MelissaGiftMenu

        "Back":
            jump expression CurLoc
```

Use a shared class method only for a real universal rule, for example
`melissa.needs_apology("you")` or a small topic/gift scoring helper. Do not
replace readable scene choices with dispatchers.

Dialogue rules:

- Talk, flirt, gift, apology, questions, and story-specific dialogue are choices in the NPC talk label or real sublabels called by it.
- The visual result is the same as a story event: picture/text remain visible, and choices appear in the active event/talk choice area.
- Direct mutations happen in the chosen branch on the NPC class: talked counters,
  flirt/gift/asked daily counters, relationship stats, mana, and `NPC.var`.
- Daily counters reset in the new-day/sleep layer, not in the talk label.
- Topic preferences and gift preferences belong to the NPC's data/init/object.
- Amanda, Melissa, Sandra, and Clarissa currently share talk theme and gift mechanics; that data may be reused, but the authored talk label still owns the menu and the consequence point.
- Other NPCs with their own direct talk procedures can stay direct until migrated.

Current Tractir comparison:

- `CharacterActionHub.rpy` centrally maps NPCs to talk labels and action lists.
- `SocialTalkTopics.rpy` centrally builds topic/gift action items through `social_core_action_items()`, `SocialTalkTopicMenu`, and `SocialTalkTopicApply`.
- `IntAmandaTalk.rpy`, `IntMelissaTalk.rpy`, `IntSandraTalk.rpy`, and `IntClaraTalk.rpy` currently use `Int<Npc>TalkRefresh`, `Int<Npc>TalkApply`, and `main_ui_call_label` for many authored choices.
- These are compatibility layers to reduce, not patterns for new dialogue content.

## Anger And Apology

Anger should come from authored causes, not from anonymous random state.

Good reasons:

- player ignored a tavern problem
- player was absent during a harassment incident
- player watched and did nothing
- player missed a promise
- player scolded or insulted a girl
- player overworked girls while not helping

The event label sets the reason directly:

```renpy
$ melissa.anger_reason = "harassment_player_watched"
$ melissa.anger_days = 3
$ melissa.rel = max(0, int(melissa.rel or 0) - 2)
```

The next NPC interaction can branch into the correct complaint:

```renpy
label MelissaComplaintMenu:
    show screen main_ui

    if melissa.anger_reason == "harassment_player_watched":
        "\"How could you just stand there and watch? Do you even care?\""
    elif melissa.anger_reason == "harassment_player_absent":
        "\"Where were you? I needed help and you were nowhere.\""

    menu:
        "Apologize":
            "\"You are right. I should have helped.\""
            $ melissa.anger_reason = None
            $ melissa.anger_days = 0
            $ melissa.rel = min(20, int(melissa.rel or 0) + 1)
            jump MelissaTalk

        "Dismiss it":
            "\"You are overreacting.\""
            $ melissa.anger_days += 2
            $ melissa.rel = max(0, int(melissa.rel or 0) - 1)
            jump expression CurLoc
```

## Keep And Remove

Keep:

- real room entry labels
- object menus
- object actions
- NPC interaction labels
- event/story labels
- returnable procedures that are genuinely reused
- readiness functions that make event tuples readable

Remove or bypass:

- refresh labels
- rebuild labels
- wrapper labels
- handler-for-one-action methods
- dispatcher layers
- duplicate Python methods for simple Ren'Py choices
- recursive menu loops
- labels made only to mirror a room attribute
- fallback routes that hide a missing condition, wrong label name, wrong room key, or broken menu owner

## Fix The Direct Owner

When a scene or interaction fails, patch the source of truth:

- If an event does not appear, fix its tuple, readiness condition, room `checkTriggers()` call, or priority.
- If a click opens the wrong thing, fix the NPC/object menu label that owns the interaction.
- If a thread repeats incorrectly, fix the content label's `thread.advance()` or `thread.complete()` point.
- If a room shows the wrong choices, fix that room or object menu directly.
- If relationship state is wrong, update the NPC object state in the event label that caused it.

Do not add a second path that tries to guess or recover from the broken path. There should be one clear source for room events, one clear source for each NPC menu, and one clear label that applies each story consequence.

## Practical Checklist

Before adding a content scene:

- The owner NPC/thread is clear.
- The event tuple uses the correct `location` and `action`.
- Room code calls `findAvailableEvents(forced=True)` before `checkTriggers()`.
- The label shows the story directly.
- Choices update variables directly.
- `thread.advance()` or `thread.complete()` happens only after success.
- The label returns to `CurLoc` or jumps to the next real room.
- No new wrapper, dispatcher, refresh, or rebuild layer was added.
- No fallback was added to hide a broken tuple, label, room key, condition, or owner.

## Copy-Ready Templates

Use these as starting points for new content. Keep them readable and edit the story text, choices, flags, and thread calls directly.

### Default NPC Talk Menu

```renpy
label PersonTalk:
    show screen main_ui

    if person.anger_reason:
        jump PersonComplaintMenu

    "She waits for you to speak."

    menu:
        "Talk about work":
            if "job_routine" in person.talk_preferences:
                "She enjoys talking about the rhythm of the tavern work."
                $ person.rel = min(20, int(person.rel or 0) + 1)
            else:
                "She answers politely, but the topic does not catch her interest."
            $ person.talked = int(person.talked or 0) + 1
            $ person.talked_today = int(person.talked_today or 0) + 1
            $ calendar_v2.advance_minutes(3)
            jump PersonTalk

        "Flirt" if person.rel >= 10:
            "You try a warmer tone."
            $ person.set_var_int("flirted_today", person.var_int("flirted_today", 0) + 1)
            $ calendar_v2.advance_minutes(3)
            jump PersonTalk

        "Gift" if person.rel >= 10:
            jump PersonGiftMenu

        "Back":
            jump expression CurLoc
```

### Talk Topics Menu

Use a separate talk-topic sublabel only when it is a real readable submenu.
It must still own the visible choices and consequences directly.

```renpy
label PersonTalkTopics:
    show screen main_ui

    "You choose what to talk about."

    menu:
        "Work":
            if "job_routine" in person.talk_preferences:
                "She enjoys talking about the rhythm of the tavern work."
                $ person.rel = min(20, int(person.rel or 0) + 1)
            else:
                "She answers politely, but the topic does not catch her interest."
            $ calendar_v2.advance_minutes(3)
            jump PersonTalkTopics

        "Gossip":
            if "gossip" in person.talk_preferences:
                "Her expression brightens as the conversation turns lively."
                $ person.rel = min(20, int(person.rel or 0) + 1)
            else:
                "She listens, but gives little back."
            $ calendar_v2.advance_minutes(3)
            jump PersonTalkTopics

        "End conversation":
            $ calendar_v2.advance_minutes(30)
            $ Player.fun = min(100, int(Player.fun or 0) + 15)
            jump PersonTalk
```

For the real ten-topic talk session, keep the same shape: each topic is a direct menu choice, favorite topics are read from the NPC object, and the label updates time, fun, and relationship values directly.

### Complaint And Apology Menu

```renpy
label PersonComplaintMenu:
    show screen main_ui

    if person.anger_reason == "harassment_player_watched":
        "\"How could you just stand there and watch? Do you even care?\""
    elif person.anger_reason == "harassment_player_absent":
        "\"Where were you? I needed help and you were nowhere.\""
    elif person.anger_reason == "ignored_tavern_problem":
        "\"You left this problem for us again. Are we supposed to handle everything ourselves?\""
    else:
        "\"I am still angry with you.\""

    menu:
        "Apologize":
            "\"You are right. I should have handled it better.\""
            $ person.anger_reason = None
            $ person.anger_days = 0
            $ person.rel = min(20, int(person.rel or 0) + 1)
            $ calendar_v2.advance_minutes(10)
            jump PersonTalk

        "Dismiss it":
            "\"You are overreacting.\""
            "She goes quiet. That hurt more than shouting."
            $ person.anger_days += 2
            $ person.rel = max(0, int(person.rel or 0) - 1)
            $ calendar_v2.advance_minutes(5)
            jump expression CurLoc
```

### Simple Event Label

```renpy
label PersonEvent_0:
    show screen main_ui

    "Something happens in the room."

    menu:
        "Help":
            "You step in and deal with it."
            $ calendar_v2.advance_minutes(20)
            $ Player.fun = min(100, int(Player.fun or 0) + 5)
            $ person.rel = min(20, int(person.rel or 0) + 1)
            $ thread.advance()
            jump expression CurLoc

        "Leave it":
            "You decide not to get involved."
            $ calendar_v2.advance_minutes(5)
            $ person.anger_reason = "ignored_tavern_problem"
            $ person.anger_days = 2
            $ person.rel = max(0, int(person.rel or 0) - 1)
            jump expression CurLoc
```

### Repeatable Investigation Until Success

```renpy
label ClaraMarketSpy_0:
    show screen main_ui

    if explorations < 100:
        vscene "images/clara/market/day_failed.jpg"

        "You see Clarissa. She quickly pulls her cloak hood over her head and disappears into the noisy market crowd."

        menu:
            "Follow her":
                $ calendar_v2.advance_minutes(30)
                $ Player.explorations = int(Player.explorations or 0) + 1
                $ Player.fun = min(100, int(Player.fun or 0) + 10)
                jump MarketPlace

            "Leave her to her business":
                "You decide not to disturb her and give her some privacy."
                $ calendar_v2.advance_minutes(5)
                jump MarketPlace

    vscene "images/clara/market/day_success.jpg"

    "You follow her to one of the stalls at the far end of the market, where she meets a strange-looking merchant."

    menu:
        "Approach them":
            "You approach Clarissa and the merchant."
            $ Clara.set_var_int("booklet_flag", 1)
            $ Mongol.set_var_int("conspiration_flag", 1)
            $ thread.complete()
            jump MongolMerchantList

        "Decide to talk to Clarissa later":
            $ calendar_v2.advance_minutes(20)
            jump MarketPlace
```

### Thread Tuple For The Event

```renpy
LThreadData(0, "clara", "MarketSpy", None, [
    (
        "ClaraMarketSpy_0",
        [2, 3],
        [8, 18],
        14,
        1,
        None,
        clara_market_spy_ready,
        None,
        "MarketPlace",
        "enter",
        0,
    ),
], highlight=False, threaded=True)
```

The label name keeps its explicit event number. The thread's `num` controls which ordered event is active, and the label itself decides whether to repeat, advance, or complete.
