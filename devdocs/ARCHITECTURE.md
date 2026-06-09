# Billy Bones Inn — Event/UI/Media Architecture Rules

## Purpose

This document defines the canonical architecture rules for:

* story events
* thread initialization
* HUD/UI behavior
* media/picture handling
* room flow
* debug/testing procedures
* code readability expectations

These rules exist to:

* prevent duplicate systems
* prevent wrapper/helper explosions
* keep event debugging deterministic
* preserve readable authored Ren'Py flow
* stabilize Codex behavior
* reduce recursive UI loops
* preserve maintainable architecture

---

# 1. Canonical Story Event Pipeline

The ONLY canonical story-event pipeline is:

```text
threadList
→ loadThreadData()
→ threadData
→ createThreads()
→ threads
→ initThreads()
→ initEvents()
→ find_available_events()
→ availEvents[location][action]
→ checkStoryTrigger()
→ preEvent()
→ jump event label
→ thread.advance() / thread.complete()
```

No second runtime event engine may be introduced.

---

# 2. Required Story Event Structure

Canonical structure:

```text
game/Utilities/General/Classes/
├── StoryEventRuntime.rpy
├── StoryEventManager.rpy
├── StoryConditions.rpy
└── CharacterThreadList.rpy
```

---

# 3. StoryEventRuntime.rpy Responsibilities

This file is canonical and owns:

* Event
* ThreadData
* LThreadData
* RThreadData
* UThreadData
* ThreadInfo
* LThreadInfo
* RThreadInfo
* UThreadInfo
* loadThreadData()
* createThreads()
* initThreads()
* initEvents()

Do NOT duplicate these classes elsewhere.

---

# 4. StoryEventManager.rpy Responsibilities

StoryEventManager is ONLY:

* debug inspector
* runtime comparison helper
* event selector
* available-event cache helper

It must NOT:

* own runtime threads
* duplicate threadData
* create Event objects
* perform Ren'Py call/jump inside Python methods

Correct responsibilities:

```python
story_manager.list_all_raw_threads()
story_manager.get_original_tuple(label)
story_manager.compare_original_vs_runtime(label)
story_manager.find_available_events(forced=True)
story_manager.get_trigger_event(location, action)
```

---

# 5. Canonical Trigger Flow

Use a Ren'Py label for trigger execution.

Correct pattern:

```renpy
label checkStoryTrigger(location="", action="", numpop=0):
    $ evt = story_manager.get_trigger_event(location, action)

    if not evt:
        return False

    $ active_event = evt

    if getattr(evt, "threaded", False):
        call preEvent(evt.thread_name)
    else:
        call preEvent(None)

    jump expression evt.target
```

Do NOT perform jumps/calls inside Python helper methods.

---

# 6. Thread List Rules

Thread list files define DATA ONLY.

Example:

```python
init python:
    newCharacterThreadList = [
        LThreadData(1, "NewCharacter", "Introduction", "true", [
            [
                ("NewCharIntro001", 0, 0, 0, 1.0, None, "true", None, "TavernMain", "talk", 100)
            ],
            [
                ("NewCharIntro002", 0, 0, 1, 1.0, None, "flag_NewCharMet", None, "TavernMain", "talk", 90)
            ],
        ], True, True),
    ]
```

---

# 7. Tuple Format Is Fixed

Tuple format:

```python
(
    target_label,    # 0
    day,             # 1
    hour/time,       # 2
    evtDay delay,    # 3
    probability,     # 4
    requirements,    # 5
    condition,       # 6
    required_item,   # 7
    location,        # 8
    action,          # 9
    priority         # 10
)
```

Never:

* reorder tuple fields
* add hidden fields
* silently reinterpret indexes

---

# 8. Explicit Thread Registration

Use explicit thread registration.

Correct:

```python
init python:
    threadList = []
    threadList += AmandaThreadList
    threadList += MelissaThreadList
    threadList += SandraThreadList
    threadList += newCharacterThreadList
```

Avoid dynamic global scanning for thread lists.

Explicit registration is easier to debug.

---

# 9. Runtime Initialization Rules

Canonical initialization:

```renpy
label initStoryEventRuntime(force=False):

    $ story_manager.init_from_tuples(threadList, force=force)

    if threadData is None or force:
        $ threadData = loadThreadData(threadList)
        $ threads = createThreads()
        $ initThreads()
        $ initEvents()

    $ findBlockedThreads(threads)

    $ story_manager.find_available_events(forced=True)

    return
```

---

# 10. Debug Framework Rules

Before modifying event logic, ALWAYS debug using:

```python
story_manager.list_all_raw_threads()
story_manager.get_original_tuple(label)
story_manager.compare_original_vs_runtime(label)
story_manager.find_available_events(forced=True)
availEvents[location][action]
```

Codex must NOT guess why an event failed.

---

# 11. Debug/Test Questions

The framework must answer:

* Is the tuple loaded?
* Was it converted into runtime Event?
* Is the thread active?
* Are conditions passing?
* Is the location/action correct?
* Is priority selecting the correct event?
* Is required item blocking it?
* Is probability blocking it?
* Is time/day blocking it?

---

# 12. HUD/UI Rules

Canonical gameplay shell:

```text
main_ui
```

HUD should remain visible during:

* normal room flow
* NPC interactions
* ordinary story events

Current-room NPC display should remain visible unless intentionally hidden.

---

# 13. main_ui Rules

Ordinary story events should display through main_ui by setting:

```python
UI_mode
MainTxt
CurLocDesc
current_picture_mode
current_scene_picture
current_action_title
current_action_items
```

Avoid raw Ren'Py fullscreen menus for ordinary gameplay.

---

# 14. Menu Builder Rules

Menu builders are ONLY for repeatable/default room actions.

Canonical room builder:

```python
Room.build_menu_sections()
```

Special authored events may directly define:

```python
current_action_items
```

Do NOT force special scripted scenes into generic menu builders.

---

# 15. Wrapper Reduction Rules

Preferred:

```renpy
MenuItem("Kitchen", Call("MoveToRoom", "TavernKitchen", 5))
MenuItem("Look", Jump("LookAtBooklet"))
```

Avoid:

```text
button
→ wrapper
→ compatibility helper
→ rebuild helper
→ another helper
→ real label
```

Readable code is more important than over-abstraction.

---

# 16. Helper Rules

Helpers may:

* calculate
* validate
* fetch data
* mutate isolated state

Labels own:

* flow
* jumps
* scene progression
* event transitions

Screens only display.

---

# 17. Movement Rules

Canonical movement:

```renpy
MoveToRoom(target, minutes)
```

Compatibility-only:

```renpy
AdvanceMovementTime
```

Avoid maintaining multiple movement systems.

---

# 18. Location Label Rules

Original location labels remain the real flow anchors.

Examples:

```text
TavernMain
TavernKitchen
Backyard
Forest
```

Do NOT create:

* refresh labels
* rebuild labels
* restore labels

Returning to the location label IS the refresh.

---

# 19. Loop Prevention Rules

Never create:

```text
label → call screen → immediate jump same label
```

Correct flow:

```text
setup state
call screen main_ui
user action
jump/call next label
```

---

# 20. Media System Split

There are THREE separate picture categories.

---

## A) Location Backgrounds

Purpose:
default room background.

Depends on:

* room
* time of day
* random variant

Suggested naming:

```text
images/locations/<Room>/<Room>_<time>_<variant>.<ext>
```

Examples:

```text
TavernKitchen_day_01.png
Forest_night_02.jpg
```

Allowed extensions:

```text
png
jpg
jpeg
webp
```

Location entry resets:

```python
current_picture_mode = "location"
current_scene_picture = ""
```

---

## B) Room Scene Pictures

Special picture inside a room while HUD remains active.

Examples:

* searching furniture
* examining objects
* looking through windows

Use:

```python
current_picture_mode = "scene"
current_scene_picture = "path"
```

Returning to location clears it.

---

## C) Event / Character Scene Pictures

These are variable-dependent and event-specific.

Do NOT force universal naming.

Examples:

```text
images/melissa/grope/reaction_angry_0.png
images/melissa/amandaroom/scene1.png
images/melissa/bedroom_search/page2.jpg
```

Event labels may directly choose paths based on state.

This is acceptable and preferred.

---

# 21. vscene Rules

`vscene` is ONLY for:

* cinematic moments
* fullscreen sequences
* intentionally immersive scenes

Do NOT use vscene as the default room background system.

Ordinary gameplay should use:

* current_scene_picture
* main_ui

---

# 22. Event Scene Rules

Authored event labels may directly:

* mutate variables
* select picture paths
* write classic `menu:` choices in the label
* use event-owned `current_action_items` only when rendering those choices in the active `main_ui` event panel
* branch by state
* advance/complete threads

This is preferred for story readability.

Do NOT over-abstract authored scenes.

Event consequences must stay readable at the choice point:

* Direct stat/flag mutation is preferred for simple effects.
* Use `call SomeHelperLabel(...)` for established shared consequence labels,
  such as `SlutFriendsIncrease`, `PregnancyCheck`, or other real Ren'Py labels.
* Do not `jump` to a helper merely to compute or apply a consequence.
* Do not hide choice consequences in Python evaluator methods, dispatcher
  methods, or distant apply handlers.
* If a story label has meaningful choices, add a short comment block before the
  label explaining what the label does and which state/thread outcome it owns.

Correct shape:

```renpy
# Event: Clara sees the player interfere at the market.
# Choices:
# - follow: increases suspicion, advances the Clara market thread
# - ignore: leaves the thread available for later
label story_clara_market_choice:
    vscene "images/clara/market.jpg"
    "You spot Clara in the market crowd."

    menu:
        "Follow her":
            $ ClaraVar["market_followed"] = 1
            $ exploration += 1
            $ thread.advance()
            jump MarketPlace

        "Do not interfere":
            $ ClaraVar["market_ignored"] = 1
            jump MarketPlace
```

Correct shared helper use:

```renpy
menu:
    "Encourage her":
        call SlutFriendsIncrease("amanda", 8, 1, 1, 20, 1, 1)
        $ AmandaVar["encouraged"] = 1
        jump TavernMain
```

---

# 23. Multi-Picture Event Beats

Events with multiple pictures must stay as authored event beats inside the
event label.

Family Life uses this shape:

```renpy
vscene "images/event/scene_1.jpg"
"Beat text."

vscene "images/event/scene_2.jpg"
"Next beat text."

menu:
    "Continue":
        pass

vscene "images/event/scene_3.jpg"
"Next beat after the explicit proceed."
```

Rules:

* Use repeated `vscene` plus text for linear picture progression.
* Use a simple classic `menu: "Continue": pass` only when an explicit proceed
  button is needed.
* Keep the sequence in the event label. Do not split one authored sequence into
  queue/paging/apply/advance labels.
* If a proceed button is rendered through Tractir `main_ui`, it must still be a
  direct event-label proceed beat, not a generic paging engine.
* Do not mutate story/thread state on a pure proceed beat unless that beat is
  the actual consequence point.
* Mutate state and call `thread.advance()`, `thread.complete()`, or
  `thread.abort()` only at the real outcome beat.

Current Tractir comparison:

* `QueuePagedPanelText`, `AdvancePagedPanelText`, and related paged-panel labels
  are compatibility/bloat for authored events when they replace a simple
  multi-picture label sequence.
* Long text may be split manually into meaningful event beats with pictures.
  It should not be hidden in an automatic paragraph queue if the scene is an
  authored story/sex event.

---

# 24. Event Choice Display Rule

Event choices must be visible inside the active event scene layout.

The visual target is the Tractir `main_ui` event layout:

```text
left/center: event picture and authored event text
right panel top: location/time/player status
right panel middle: event menu choices
right panel bottom: visible character area, when applicable
```

This is the same design principle as Family Life:

```renpy
vscene "images/event0/Nikki/Sex/0. Sex neighbor/1.jpg"
menu:
    "Buy":
        $ hour += 1
        $ thread.advance()
        jump adams_pool
    "Not a chance":
        jump nikkiSex_End
```

Family Life sex-event files keep the menu choices in the authored event label.
The menu appears while the event picture/text remains the current scene. The
chosen branch mutates state and jumps onward directly.

Tractir must preserve that behavior visually. If Tractir uses `main_ui` instead
of Family Life's native `locmenu`, the event choices still belong in the middle
action panel during the event, exactly like the in-game event screenshot.

Do NOT move event choices into:

* a separate overlay detached from the event picture/text
* a popup that hides the event layout
* a queued/paged panel that changes the authored flow
* refresh/apply/renew wrapper labels
* Python-built dispatcher menus far away from the event label

Current Tractir comparison:

* Some files already follow the desired authored pattern, such as
  `game/NPC/Girls/Becky/BeckyEvents.rpy`, which explicitly says classic menu
  only and uses `menu:` inside event labels.
* Other current files push choices into `current_action_items` or
  `main_ui_set_action_panel`, for example Clara thread scenes. This can match
  the desired visual layout only when the choices are authored at the event
  point and rendered in the active event panel. It is not acceptable when it
  becomes a generic UI queue, rebuild, refresh, or dispatcher layer.
* Event choice authorship should move toward Family Life-style `menu:` in the
  event label. Tractir's screen layer may render that menu in the right event
  panel, but the content ownership stays with the label.

---

# 25. NPC Dialogue And Social Actions

NPC dialogue is event-like content.

The clicked `talk` NPC action must open the real dialogue label:

```renpy
label IntMelissaTalk:
    show screen main_ui
    "Melissa waits for you to speak."

    menu:
        "Talk about safety":
            $ Talked["melissa"] = int(Talked.get("melissa", 0) or 0) + 1
            $ TalkedToday["melissa"] = int(TalkedToday.get("melissa", 0) or 0) + 1
            $ Friends["melissa"] = min(20, int(Friends.get("melissa", 0) or 0) + 1)
            jump IntMelissaTalk

        "Flirt" if int(FlirtedToday.get("melissa", 0) or 0) == 0:
            $ FlirtedToday["melissa"] = 1
            call SlutFriendsIncrease("melissa", 4, 1, 1, 5, 1, 0)
            jump IntMelissaTalk

        "Gift":
            call IntMelissaGiftMenu
            jump IntMelissaTalk

        "End conversation":
            jump expression CurLoc
```

Talk, flirt, gift, apology, question, and NPC-specific dialogue choices belong
inside the NPC talk label or in real sublabels called by that label. They are
not generic room actions.

Rules:

* The talk label owns the picture, text, visible choices, consequences, and
  return flow.
* Dialogue choices must be presented in the active event/talk scene layout,
  like story-event choices.
* Direct mutation is preferred in the branch where the player chose the line:
  `Talked`, `TalkedToday`, `FlirtedToday`, `GiftedToday`, `AskedToday`,
  friendship, openness, sluttiness, trust, and NPC-specific vars.
* Daily counters reset centrally during the new-day/sleep flow. They are not
  reset by dialogue labels.
* Topic preferences and gift preferences belong to the NPC data/init/object.
* Shared helper functions may score a topic or gift, but must not hide the
  authored choice or state consequence.

Current Tractir comparison:

* `game/Utilities/General/NPC/CharacterActionHub.rpy` currently stores central
  `NPC_META` action lists and talk labels.
* `game/Utilities/General/NPC/SocialTalkTopics.rpy` currently owns shared topic
  packs, topic profiles, gift affinity, `SocialTalkTopicMenu`,
  `SocialTalkTopicApply`, and `social_core_action_items()`.
* Amanda, Melissa, Sandra, and Clarissa currently use shared talk theme/gift
  mechanics.
* `game/NPC/Girls/Amanda/IntAmandaTalk.rpy`,
  `game/NPC/Girls/Melissa/IntMelissaTalk.rpy`,
  `game/NPC/Girls/Sandra/IntSandraTalk.rpy`, and
  `game/NPC/Girls/Clara/IntClaraTalk.rpy` currently route many choices through
  `Int<Npc>TalkRefresh`, `Int<Npc>TalkApply`, `main_ui_call_label`, and shared
  social action item builders.
* Those refresh/apply/dispatcher layers are compatibility/bloat to reduce.
  They are not the design to copy for new content.
* NPCs with their own direct talk procedures can remain direct until migrated.

Correct migration direction:

```text
NPC action click
-> Int<Npc>Talk
-> authored picture/text/menu
-> branch mutates daily/social/story state directly
-> optional call to a real helper label for shared mechanics
-> return to Int<Npc>Talk or CurLoc
```

Do NOT add:

* dialogue refresh labels
* dialogue apply labels for one menu choice
* Python menu dispatchers
* `social_core_action_items()`-style builders for authored choices
* hidden topic/gift handlers that obscure the consequence point

---

# 26. Popup/Event System Rules

Standalone popup dict systems are NOT canonical story-event systems.

If an event is:

* story relevant
* state dependent
* replay sensitive
* conditional
* chain based

then it belongs inside:

* threadList
* StoryEventRuntime
* canonical event pipeline

---

# 27. Canonical Architecture Direction

Target architecture:

```text
Location labels
→ stable room anchors

RoomTemplate
→ reusable room/menu logic

StoryEventRuntime
→ canonical runtime event engine

StoryEventManager
→ debugging + selection helper

main_ui
→ universal gameplay shell

vscene
→ cinematic fullscreen mode

Direct event labels
→ authored story flow
```

---

# 28. Basic Actions, Screens, And UI Return Flow

The canonical reference is Family Life's simple action pattern:

```text
room/location label
-> normal Ren'Py menu or Tractir main_ui action button
-> call a real action label
-> action label shows/selects picture, writes text, mutates stats/time/items/state
-> return
-> owning room/location explicitly jumps/calls back to itself
```

Family Life does use screens, but only for normal UI surfaces:

* map imagemaps, such as `call screen homemap()`
* persistent HUD, such as `show screen status`
* menu rendering, such as `menu (screen="locmenu", ...)`
* inventory/store screens in their specific contexts

Family Life basic action labels do NOT use refresh/apply/renew wrapper labels.

Correct action-label style:

```renpy
label wash:
    if restrictions():
        return
    vscene "images/hero/hero.jpg"
    "I wash my hands and clean my teeth."
    $ minute += 10
    $ fun += 5
    $ washedToday = True
    return
```

Correct room/location style:

```renpy
menu (screen="locmenu", icons=getNPCicons(location), menu_name="menu_"+location):
    "Wash":
        call wash
        jump bathroom
```

For Tractir, `main_ui` remains the gameplay shell instead of Family Life's
`locmenu`, but the ownership rule is the same:

* room/object/NPC/action definition owns availability and display metadata
* the real action label owns the effect
* picture and description may be attached to the room/object/action definition
* stat/time/item mutations must remain visible in the action label or in a tiny, clearly named helper
* the caller returns to the owning room/object/NPC flow directly

Do NOT preserve or add these as architecture:

* `RefreshCurrentActionMenu`
* `ApplyActionResultToUI`
* generic apply/renew/refresh/rebuild labels
* room refresh dispatch tables
* wrapper labels whose only job is to redraw the same menu
* Python methods that duplicate simple Ren'Py label mutations

Current Tractir comparison:

* `game/Utilities/General/Common/Actions.rpy` currently mixes action labels,
  inventory helpers, social item rules, NPC-specific gift effects, UI refresh
  routing, and result-application wrappers.
* `ROOM_ACTION_REFRESH`, `RefreshCurrentActionMenu`, `ApplyActionResultToUI`,
  and generic `ApplyItemAction` are compatibility/bloat, not desired design.
* Real basic labels such as `Wash`, `Sleep`, `Rest`, `Eat`, `Drink`, `Clean`,
  `Chop`, `MakeFire`, `Take`, `Drop`, and `Examine` are the pieces to keep and
  simplify toward direct Family Life-style execution.

Screens are allowed when they are the actual UI surface. Screens are not a
reason to introduce refresh/apply/renew layers between a clicked action and the
label that performs that action.

---

# 29. Final Goal

The architecture should provide:

* readable Ren'Py flow
* deterministic debugging
* stable HUD behavior
* fewer wrappers
* fewer recursion loops
* explicit media behavior
* clean event progression
* maintainable authored story scenes
* predictable Codex modifications
