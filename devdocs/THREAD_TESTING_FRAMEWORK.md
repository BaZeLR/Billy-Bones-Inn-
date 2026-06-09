# Thread Testing Framework (Exact Pattern / Style — NOT Exact Names)

**Critical rule from the request:**
> "this is framework not exact names use it for our threads and names"

This document + the code in `tests/ThreadTesting.rpy` capture the **framework** (the deep Python introspection style, structure validation, event tuple field access by index 0-10, `canTrigger()` calls, `active`/`blocked`/`condStr`/`requirement` checks, printing of `__dict__`, prerequisite flag handling, world context (day/hour/location), generic walker pattern, etc.).

**It does NOT hard-code the Johnny example names** (johnnyLola, johnnyMeet, specific "len==4", Johnny event data, `johnnyStripclubDone` as the only prereq, etc.).

All concrete tests must use **our real thread and event names** from this Tractir project:
- `BeckyHomeVisits` + its atomic stages (`becky_home_dinner_arrival`, `becky_home_dinner_grope`, `becky_home_georgett_visit`, `becky_home_kids_watching`, `becky_home_dinner_poproshchatysya`, `becky_blackwood_quest_start`, etc.)
- `BeckyDanceHome`, `BeckyStoreTalks`, `BeckyEddie`, `BeckySandraInfluence`, etc.
- Future full ports: Amanda* threads, Liza*, Georgett*, LegareConflict, etc.

The Johnny labels in the original paste are just an example of the *shape* of a good test. They have been generalized in `tests/ThreadTesting.rpy`.

See the actual test file for the current working implementation using our names.

## 1. Global Structures

- `threadList`: A list/tuple of thread objects (the primary thing the tests iterate over).
- `threads` (in some contexts): Runtime dict of active ThreadInfo objects (from `createThreads()` / `initThreads()` in StoryEventRuntime.rpy).
- `threadListsByGirl`: Dict used by StoryThreadBoard.

## 2. Thread Object Shape (what tests expect on items in threadList)

A thread object must support (via `hasattr` + `getattr`):

| Attribute     | Expected Type / Meaning                                      | Notes from tests |
|---------------|--------------------------------------------------------------|------------------|
| `level`       | int (0 = repeatable/base, 1 = story/quest)                  | Used to filter Johnny Lola (level 1) vs Johnny Meet (level 0) |
| `person`      | str (e.g. "johnny", "becky")                                | Key filter |
| `name`        | str (e.g. "johnnyLola", "johnnyMeet", "BeckyHomeVisits")    | Unique within person |
| `requirement` | str or None (older name for prerequisite flag)              | Test checks `johnny_meet_thread.requirement is None` |
| `condStr`     | str or None (condition string, e.g. variable name)          | "Requirement check (condStr/conds)" |
| `conds`       | list (parsed conditions)                                    | Printed for debugging |
| `active`      | bool                                                        | If False → "Thread is not active!" warning |
| `blocked`     | bool                                                        | If True → "Thread is blocked!" warning |
| `events`      | list of lists/tuples of event objects (or raw tuples)       | Core data structure (see Event below) |

Other attributes that tests print for completeness:
- `triggers`, `event`, `event_list`, `eventdata` (fallback search for event data)
- Full `dir()` and `__dict__` are dumped for diagnosis.

## 3. Event Object / Tuple Shape

Events are accessed via `thread.events` (list of lists or flat list).

Each event item supports both tuple positional access **and** object attributes (the tests do both):

**Positional tuple indices (critical — tests use event[ N ] directly):**

- `event[0]`  → target / label name (str)               e.g. "johnnyMeet_0"
- `event[1]`  → day (int or None)
- `event[2]`  → hour / time window (tuple or int)       e.g. (21,23) or (17,22)
- `event[3]`  → week / evtDay parameter (int)
- `event[4]`  → probability (float/int)
- `event[5]`  → reqs (dict or None)
- `event[6]`  → condStr (str or None)
- `event[7]`  → item (str or None)
- `event[8]`  → location (str)                          e.g. "pool", "adams_pool", "BeckyHome"
- `event[9]`  → action (str)                            e.g. "enter"
- `event[10]` → priority (int)

**Object attributes the tests also inspect on Event instances:**

- `target`, `day`, `hour`, `evtDay`, `prob`, `reqs`, `condStr`, `item`, `location`, `action`, `priority`, `thread_name`, `threaded`
- `canTrigger()` method (must exist and be callable; returns bool or raises)

If an event is a raw tuple, the tests still treat it positionally. If it is an `Event` object (from StoryEventRuntime), it has the attributes + `canTrigger()`.

## 4. Test Patterns (exact usage)

The framework performs these checks in order:

1. **Existence** — find thread by `level + person + name`
2. **Basic properties** — print level/person/name/condStr/conds/active/blocked + full dir/__dict__
3. **Requirement** — inspect `condStr` / `requirement`, check if the global var it names is True
4. **Events** — locate events via several attribute names, then for every event dump all fields + call `canTrigger()` if present
5. **Activation state** — warn on `active==False` or `blocked==True`
6. **World state** — print current `day`, `hour`, `location`
7. **Assertions** — hard `assert` on structure (used in `test_johnny_meet_thread` and validation)

There are also pure-debug labels (`debug_johnny_*`) that just print without asserts.

## 5. Prerequisites & Flags

- Many level-1 threads use a flag such as `johnnyStripclubDone = True` as a hard gate (set via debug menu in the provided code).
- Tests explicitly set/check this flag.

## 6. How to Add New Threads to Be Testable With This Framework

To make a new thread (e.g. BeckyHomeVisits, BeckyBlackwood, Amanda arcs, etc.) testable with the exact same labels:

- It must appear in the global `threadList` (or a compatible list the test walker can find).
- It must expose the attributes listed in section 2.
- Its `.events` must be a list of items that support both the 11 positional indices **and** the attribute names + `canTrigger()`.
- Use the same `LThreadData` / `Event` construction (or provide a compatibility shim) so the existing StoryEventRuntime machinery produces objects the tests understand.

The current `LThreadData` + `Event` classes (StoryEventRuntime.rpy:522+) are already **very close** to this shape:
- `ThreadData` gives `level`, `person`, `name`, `condStr`, `conds`
- `Event` is initialized from exactly the 11-element tuple and has all the named fields + `canTrigger()`
- Runtime `ThreadInfo` instances have `blocked`, `enabled`, etc.

A thin adapter (or making `threadList` contain the runtime `ThreadInfo` objects instead of just the data objects) makes the pasted test framework work without modification.

## 7. Running the Tests

Use the provided runner:

```renpy
call run_all_johnny_tests
```

Or call individual `test_*` / `debug_*` labels.

For Becky (and all previous exhaustive ports), create parallel labels following the exact same structure:
- `test_becky_home_visits_thread`
- `test_becky_blackwood_quest_start`
- `test_becky_all_threads_validation`
- `run_all_becky_tests`
- Debug variants

## 8. Current Project Mapping (as of 2026)

- Source of truth for thread data: `beckyThreadList`, `amandaThreadList`, etc. (lists of LThreadData / RThreadData)
- Runtime: `threadData` dict + `threads` dict (ThreadInfo objects) created by `createThreads()` / `initThreads()`
- Event objects already match the 11-field + `canTrigger()` contract.
- The main gap for the exact test framework is that `threadList` in the test code expects the final runtime-shaped objects with a `.events` attribute (instead of `.data.triggers`).

## 9. Recommended Implementation Steps

1. Document this file (done).
2. Add the exact test labels the user provided into `tests/ThreadTesting.rpy` (or equivalent).
3. Ensure `threadList` (or a new `allThreadsForTesting` list) contains objects that satisfy the attribute expectations.
4. Add `.events` as an alias/property on ThreadInfo pointing to the flattened triggers if needed.
5. Add `requirement` as an alias for `condStr` for older test compatibility.
6. Create matching `test_becky_*` labels using identical Python introspection patterns.
7. Run the full test suite regularly during porting.

This framework is the **canonical way** to validate that story threads (Becky home guest multi-visit, Blackwood, Amanda/Liza/Legare, Johnny, etc.) are correctly registered, have the right gates, fire under the expected day/hour/location conditions, and expose proper state for the StoryThreadBoard.

---

**Status**: This document is the single source of truth for the testing shape. All future thread work (including completing Becky exhaustion + Blackwood) must remain compatible with it.