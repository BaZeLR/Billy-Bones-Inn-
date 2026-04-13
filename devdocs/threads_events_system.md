# Event System Structure And Procedure

This document describes the event/thread system that already exists in this project, the exact event data model it expects, the runtime flow, and the correct procedure for adding or initializing new events.

## 1. Purpose

The project uses a tuple-driven event engine built around:

- `Event` objects in `game/events.rpy`
- `ThreadData` and `ThreadInfo` objects in `game/threads.rpy`
- dynamic event discovery through `findAvailableEvents()`
- event execution through `checkTriggers()` and label jumps

This is the canonical event model in the codebase.

The newer tavern popup code in `game/random_tavern_events.rpy` is separate from this system and does not follow the same model.

## 2. Core Files

- `game/events.rpy`
  Defines `Event`, `initEvents()`, `checkTriggers`, `preEvent`, and `findAvailableEvents()`.
- `game/threads.rpy`
  Defines `ThreadData`, `LThreadData`, `RThreadData`, `UThreadData`, their runtime `ThreadInfo` classes, and the global `threadList`, `threadData`, and `threads`.
- `game/locations.rpy`
  Contains location labels where location-entry actions may trigger events.
- `game/ev_tavern_daily.txt`
  Contains example event labels that show how threaded event labels advance or complete threads.
- `game/random_tavern_events.rpy`
  Contains a separate ad hoc random event popup system. It is not integrated with the tuple/thread event engine.

## 3. Exact Event Model

Each event is defined as an 11-field tuple. The tuple order is fixed.

```python
(
    target,    # 0: label name to jump to
    day,       # 1: allowed weekday or weekday range/list
    hour,      # 2: allowed hour or hour range/list
    evtDay,    # 3: day gate or dependency gate
    prob,      # 4: probability; 1 means guaranteed
    reqs,      # 5: stat requirements dict
    condStr,   # 6: extra conditions for makeConditions()
    item,      # 7: required inventory item, or None
    location,  # 8: event location key
    action,    # 9: event action key
    priority   # 10: lower value wins
)
```

The `Event` initializer in `game/events.rpy` unpacks this tuple directly by index. If the tuple order is wrong, the event is wrong.

## 4. Meaning Of Each Field

- `target`
  The Ren'Py label that should run when the event fires.
- `day`
  Used by `checkDay()`. Can be `None`, a single value, or a range/list accepted by `checkEventTime()`.
- `hour`
  Used by `checkHour()`. Can be `None`, a single hour, or a range/list accepted by `checkEventTime()`.
- `evtDay`
  Used by `checkNumDay()`.
  Supported forms:
  - `None`: no day restriction
  - `int`: require `numDay >= evt_numDay + int`
  - `str`: reference a named day source
  - `(name, delta)`: reference a named day source plus offset

  If a string or tuple is used, the code first tries `threads[evtDay[:-3]].day`, then falls back to `globals()[evtDay]`.
- `prob`
  Used by `checkProb()`.
  - `1` means always available
  - any other numeric value is used by `random(prob) < 1`
- `reqs`
  Dictionary of requirements. Example:

```python
{"money": 2000, "power": 80}
```

  The code checks:
  - `peopleInfo[stat].rel` when `stat` is a person key
  - `globals()[stat]` for normal numeric globals
- `condStr`
  Passed to `makeConditions()` and evaluated by `cond.eval()`.
- `item`
  Required inventory item for the event to be selected when competing with other events at the same `location` and `action`.
- `location`
  Key used in `availEvents[location]`.
- `action`
  Key used in `availEvents[location][action]`.
- `priority`
  Lower values are preferred when multiple events compete for the same `location` and `action`.

## 5. Thread Model

Events are not defined on their own. They are wrapped inside thread definitions in `game/threads.rpy`.

### 5.1 `ThreadData`

`ThreadData` stores:

- `level`
- `person`
- `subname`
- `condStr`
- `triggers`
- `highlight`
- `threaded`

`self.name` is built as:

```python
self.name = self.person + self.subname
```

So:

```python
LThreadData(0, "event", "TavernDaily", ...)
```

creates a thread named:

```python
"eventTavernDaily"
```

### 5.2 Thread Types

- `LThreadData`
  Linear thread. Only the current step is available.
- `RThreadData`
  Random-order thread. One event from a shuffled order is active at a time.
- `UThreadData`
  Unordered thread. Any unfinished eligible event may be available.

### 5.3 Runtime Thread Objects

At runtime, `ThreadData` becomes one of:

- `LThreadInfo`
- `RThreadInfo`
- `UThreadInfo`

These runtime objects track:

- `done`
- `enabled`
- `metconds`
- `aborted`
- `completed`
- `blocked`
- `day`
- `num`

`day` is important because event day gating often depends on when a thread was enabled or last updated.

## 6. How Events Are Built

Thread definitions live in:

- `define threadList = [...]`

Then the code builds:

```python
define threadData = loadThreadData(threadList)
default threads = createThreads()
```

This means:

1. `threadList` is the source definition.
2. `threadData` is a dictionary keyed by thread name.
3. `threads` is the runtime dictionary of `ThreadInfo` instances.

When `ThreadData` is constructed, every raw event tuple is converted into:

```python
Event(evt, self.name, threaded)
```

This is the actual moment where the tuple becomes an `Event` object.

## 7. Initialization Procedure

This is the intended initialization procedure for the event engine.

### 7.1 Data Definition

Define all event threads in `threadList`.

### 7.2 Runtime Thread Creation

The existing code already declares:

```python
define threadData = loadThreadData(threadList)
default threads = createThreads()
```

### 7.3 Thread Initialization

Call:

```python
$ initThreads()
```

This does two things:

- ensures every runtime thread exists
- compiles thread-level conditions with `tdata.initConditions()`

### 7.4 Event Initialization

Call:

```python
$ initEvents()
```

This does two things:

- calls `evt.initConditions()` for every event
- creates dynamic jump nodes for all event labels in `jumpList`

### 7.5 Important Current Repo State

In the current project snapshot, `initThreads()` and `initEvents()` are defined, but there is no obvious startup call wiring them into the main game flow.

That means the intended procedure exists in code, but the initialization hook is incomplete or missing from the visible startup path.

## 8. Runtime Procedure

This is the normal runtime flow once the system is initialized.

### Step 1. Location Or Menu Context Changes

When the player enters a place or opens a context where events matter, the game should refresh available events:

```python
$ findAvailableEvents(forced=True)
```

### Step 2. Threads Offer Candidate Events

`findAvailableEvents()` loops through every thread:

```python
for name, thread in threads.items():
    tmp_events.extend(thread.getAvailableEvents())
```

Each thread class decides which event set is eligible:

- `LThreadInfo.getAvailableEvents()`
  Returns candidates only from the current linear step.
- `RThreadInfo.getAvailableEvents()`
  Returns candidates from the current shuffled random step.
- `UThreadInfo.getAvailableEvents()`
  Returns all unfinished eligible events.

### Step 3. Event Eligibility Check

Every candidate event must pass:

```python
evt.canTrigger(self.day)
```

That checks:

1. day
2. hour
3. extra conditions
4. day offset / dependency
5. stat requirements
6. probability
7. location open state

### Step 4. Candidate Events Are Grouped

`findAvailableEvents()` builds:

```python
availEvents[location][action]
```

So events compete inside the same location/action bucket.

### Step 5. Priority And Item Selection

For each `location` and `action`:

1. events are sorted by `priority`
2. the first event that passes `evt.checkItem()` is selected
3. if none pass item requirements, the first event in the sorted list is kept

This means `priority` is the primary ordering rule and `item` can change which event is actually selected.

### Step 6. UI/Label Calls `checkTriggers`

When the game wants to actually fire the selected event, it calls:

```renpy
call checkTriggers(location, action, numpop)
```

Inside `checkTriggers`:

1. it looks up `availEvents[location][action]`
2. rejects empty or invalid targets
3. checks special gift logic
4. checks item presence again
5. pops calls from the stack if needed
6. calls `preEvent(thread_name if evt.threaded else None)`
7. jumps to `evt.target`

### Step 7. `preEvent`

`preEvent` does two important things:

- resets `evalTime` so event discovery will refresh after the event
- sets `thread = threads[thread_name]` and updates `thread.day`

This makes the active thread available to the destination label.

### Step 8. Event Label Must Advance Or Complete The Thread

The event label itself is responsible for thread progression.

Examples from `game/ev_tavern_daily.txt`:

```renpy
$ thread.advance()
```

or:

```renpy
if (thread):
    $ thread.complete()
```

If the label never advances or completes the thread, the thread may stay stuck on the same event.

## 9. Exact Definition Pattern For New Events

Use the existing thread system, not a standalone random dict, if you want a new event to follow the project model.

### 9.1 Single Linear Event

```renpy
LThreadData(0, "event", "TavernHarassment", None, [
    ("eventTavernHarassment", None, [12, 22], None, 0.25, None, None, None, "main_hall", "enter", 0),
], highlight=False),
```

### 9.2 Multi-Step Linear Event Chain

```renpy
LThreadData(0, "event", "TavernChain", None, [
    ("eventTavernChain_0", None, [12, 22], None, 1, None, None, None, "main_hall", "enter", 0),
    ("eventTavernChain_1", None, [12, 22], 1,    1, None, None, None, "main_hall", "enter", 1),
], highlight=False),
```

The first label should call `thread.advance()`. The second may call `thread.complete()`.

### 9.3 Random Pool Thread

```renpy
RThreadData(0, "event", "TavernDaily", None, (3,
[
    ("eventTavernBusy",       None, [12, 22], None, 0.30, None, None, None, "main_hall", "enter", 10),
    ("eventTavernHarassment", None, [12, 22], None, 0.20, {"amanda": 10}, None, None, "main_hall", "enter", 20),
    ("eventTavernFight",      None, [18, 23], None, 0.15, None, None, None, "main_hall", "enter", 30),
]), highlight=False),
```

This creates a random-order thread with three event slots.

## 10. Exact Label Pattern

The destination label should assume `thread` may already be set by `preEvent`.

Example:

```renpy
label eventTavernHarassment:
    "A drunk customer is getting handsy with Amanda."
    menu:
        "Interrupt":
            $ Amanda.rel += 5
        "Do nothing":
            $ Amanda.rel -= 5

    if thread:
        $ thread.complete()
    jump main_hall
```

For a multi-step chain:

```renpy
label eventTavernChain_0:
    "The tavern is unusually crowded."
    if thread:
        $ thread.advance()
    jump main_hall
```

## 11. Correct Location Trigger Procedure

If `main_hall` should trigger event-engine events on entry, the flow should look like this:

```renpy
label main_hall:
    $ current_location = "main_hall"
    $ findAvailableEvents(forced=True)
    call checkTriggers("main_hall", "enter", 1)

    "Normal main hall content."
    return
```

Important:

- use the same exact location key in event definitions and in `checkTriggers`
- use the same exact action key in event definitions and in `checkTriggers`

## 12. Current Tavern Popup Mismatch

The tavern popup code in `game/random_tavern_events.rpy` does not follow the event-thread model.

Current problems:

1. It stores event text in a dict instead of event tuples.
2. It does not create `Event` objects.
3. It does not use `threadList`, `threadData`, or `threads`.
4. It does not use `findAvailableEvents()`.
5. It does not use `checkTriggers()`.
6. It does not use `preEvent`.
7. It does not advance or complete threads.
8. It compares `current_location == "main_hall"` while `game/locations.rpy` currently sets `"Main Hall"`, so the current condition does not match.

## 13. Recommended Procedure For Tavern Events In This Project

If tavern incidents are supposed to be part of the game's real event system, the correct procedure is:

1. Define tavern incidents in `threadList` using `LThreadData`, `RThreadData`, or `UThreadData`.
2. Use the 11-field event tuple exactly.
3. Ensure startup calls `initThreads()` and `initEvents()`.
4. On location entry, call `findAvailableEvents(forced=True)`.
5. Call `checkTriggers("main_hall", "enter", numpop)`.
6. Implement each event label as a real Ren'Py label.
7. In each event label, call `thread.advance()` or `thread.complete()`.
8. Return or jump back to the normal location flow.

## 14. Minimal Wiring Checklist

Use this checklist when integrating a new event with the canonical model.

- Event is defined in `threadList`
- Event tuple has exactly 11 fields in the right order
- `location` and `action` keys match the caller
- target label exists
- `initThreads()` is called during startup/load
- `initEvents()` is called during startup/load
- `findAvailableEvents(forced=True)` is called before checking triggers
- `checkTriggers(location, action, numpop)` is called from the correct place
- event label advances or completes the thread

## 15. Short Conclusion

The real event architecture in this project is:

```text
threadList
-> threadData
-> threads
-> Event objects
-> findAvailableEvents()
-> availEvents[location][action]
-> checkTriggers()
-> preEvent()
-> jump to event label
-> thread.advance() / thread.complete()
```

If you want a new event to be "according to model", it must be defined and run through that pipeline.
