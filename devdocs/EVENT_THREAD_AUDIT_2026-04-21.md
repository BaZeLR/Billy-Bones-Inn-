# Event / Thread Audit

> REFERENCE ONLY / HISTORICAL AUDIT.
>
> Do not use this as implementation authority. Current event/thread rules live
> in `devdocs/EventThreadInstruction/*` and
> `devdocs/implementation_models/EVENT_THREAD_MODEL_AND_TEMPLATE.md`.

Date: 2026-04-21

Scope:

- canonical project architecture from `devdocs/agent.txt`
- canonical scene presentation from `game/01vscene.rpy`
- current event/thread runtime in `game/Inn/StoryEventRuntime.rpy`

This note tracks the highest-signal discrepancies between the declared project model and current implementation.

## Fixed In This Pass

1. `TavernStorage` now uses the shared `_story_enter` dispatch path instead of manual room-local story dispatch.

File:

- [game/Inn/TavernStorage.rpy](../game/Inn/TavernStorage.rpy)

Reason:

- all room-entry story checks should go through `CheckDailyEvent("", "_story_enter", CurLoc, time)` unless there is a very explicit reason not to
- `TavernStorage` was the only room-entry outlier still manually calling `story_event_available(..., "enter")` and `checkTriggers(...)`

## Current High-Signal Discrepancies

### 1. MarketPlace blind-pirate story bypasses the event/thread runtime

Files:

- [game/Inn/MarketPlace.rpy](../game/Inn/MarketPlace.rpy:187)
- [game/Inn/MarketPlace.rpy](../game/Inn/MarketPlace.rpy:232)

Current behavior:

- `MarketPlace` directly checks `marketplace_blind_pirate_event_available()`
- then directly calls `MarketPlaceBlindPirateEvent`
- follow-up state is kept in `BlindPirateMarketEventSeen` and `BlindPirateBreakfastPending`

Why this is a discrepancy:

- it is room-entry story content
- it has state progression
- it is not represented as a canonical thread/event target
- it bypasses `Event`, `ThreadData`, `ThreadInfo`, and `target`

Additional note:

- no matching source text entry was found in `textLocRef/MarketPlace.txt`
- this appears to be newer story content, so it should either be explicitly accepted as a new canonical thread-based story or documented as an intentional non-thread exception

### 2. Blind-pirate breakfast follow-up is a second parallel story path

Files:

- [game/Inn/TavernKitchen.rpy](../game/Inn/TavernKitchen.rpy:1111)
- [game/Inn/TavernKitchen.rpy](../game/Inn/TavernKitchen.rpy:1141)

Current behavior:

- breakfast talk checks `BlindPirateBreakfastPending`
- directly calls `TavernKitchenBreakfastBlindPirateStory`

Why this is a discrepancy:

- this is effectively step 2 of the same story
- progression is tracked by free flags instead of thread progression
- it duplicates story sequencing outside the event/thread system

### 3. Household breakfast/request stories still bypass per-NPC thread ownership

Files:

- [game/Inn/TavernMain.rpy](../game/Inn/TavernMain.rpy:382)
- [game/Inn/TavernMain.rpy](../game/Inn/TavernMain.rpy:384)
- [game/Inn/TavernMain.rpy](../game/Inn/TavernMain.rpy:389)
- [game/Inn/TavernKitchen.rpy](../game/Inn/TavernKitchen.rpy:930)
- [game/Inn/TavernKitchen.rpy](../game/Inn/TavernKitchen.rpy:935)
- [game/Inn/TavernKitchen.rpy](../game/Inn/TavernKitchen.rpy:1060)
- [game/Inn/TavernKitchen.rpy](../game/Inn/TavernKitchen.rpy:1063)
- [game/Inn/TavernKitchen.rpy](../game/Inn/TavernKitchen.rpy:1066)
- [game/Inn/HouseholdRuntimeEvents.rpy](../game/Inn/HouseholdRuntimeEvents.rpy:460)
- [game/Inn/HouseholdRuntimeEvents.rpy](../game/Inn/HouseholdRuntimeEvents.rpy:476)
- [game/Inn/HouseholdRuntimeEvents.rpy](../game/Inn/HouseholdRuntimeEvents.rpy:491)

Examples:

- `SandraDressInitiativeEvent`
- `MelissaDressRequestEvent`
- `AmandaDressRequestEvent`
- `HouseholdSoapRequestEvent`
- `HouseholdBarberRequestEvent`

Why this is a discrepancy:

- these are NPC-owned story beats
- they are called directly from room/breakfast menu flow
- they are not declared in the corresponding per-NPC thread lists
- they use free flags instead of thread progression where a thread would fit better

Important nuance:

- these may still be acceptable as runtime household incidents if intentionally modeled that way
- but if they are story progression beats, they should migrate to per-NPC thread/event ownership

### 4. Some new story scenes still use panel/menu UI state instead of canonical scene-label flow

Files:

- [game/Inn/HouseholdRuntimeEvents.rpy](../game/Inn/HouseholdRuntimeEvents.rpy:533)
- [game/Inn/MarketPlace.rpy](../game/Inn/MarketPlace.rpy:232)

Current behavior:

- scene image is pushed through `_layout_last_picture`
- text is pushed into `MainTxt` / `CurLocDesc`
- choices are pushed through `current_action_title` / `current_action_items`
- flow returns through `main_ui`

Why this is a discrepancy:

- canonical project scene flow is explicit label-based presentation
- canonical media display is `vscene`
- canonical progression should be readable directly in the scene label

Clarification:

- this does not mean the main UI is forbidden
- it means story scenes should not default to panel-state transport when an explicit label + `vscene` + menu pattern is clearer and canonical

### 5. New story flags exist outside thread progress for multi-step arcs

Files:

- [game/Inn/MarketPlace.rpy](../game/Inn/MarketPlace.rpy:124)
- [game/Inn/TavernKitchen.rpy](../game/Inn/TavernKitchen.rpy:20)
- [game/Inn/BarberShop.rpy](../game/Inn/BarberShop.rpy:3)
- [game/Inn/SoapCraftAndAtticItems.rpy](../game/Inn/SoapCraftAndAtticItems.rpy:7)

Examples:

- `BlindPirateMarketEventSeen`
- `BlindPirateBreakfastPending`
- `TavernBreakfastGeorgetteLizaPending`
- `BarberInvitePending`
- `SoapRequestQueue`

Why this matters:

- some are valid support/runtime flags
- some are acting like surrogate thread steps
- each case must be classified:
  - support state only
  - or narrative progression state that belongs in a thread

## Recommended Remediation Order

1. Keep room-entry dispatch unified through `_story_enter` and `CheckDailyEvent`.
2. Identify which non-thread story beats are true narrative arcs versus pure household/runtime prompts.
3. Migrate true narrative arcs into per-NPC thread lists first.
4. Leave pure support/runtime prompts alone unless they duplicate existing thread-owned progression.
5. Normalize scene presentation of migrated arcs toward explicit label + `vscene` + thread method flow.

## Questions To Resolve Before Bigger Refactors

1. Should `BlindPirate` be treated as:
   - a new canonical story thread
   - or an intentional world-event exception?

2. Should household request scenes like soap/barber/dress be treated as:
   - full NPC story beats in thread lists
   - or lightweight household prompts outside the formal thread system?

3. For newer Melissa/Sandra/Clarissa content, should every multi-step arc be required to use explicit thread progression by default?

Until those answers are fixed, low-risk normalization should focus on:

- dispatch consistency
- removing duplicate entry paths
- preserving content
- avoiding architecture drift
