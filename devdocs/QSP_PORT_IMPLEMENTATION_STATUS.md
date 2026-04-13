# QSP Port Implementation Status

Purpose: summarize the current Ren'Py project from a QSP-port perspective.

This is not a generic Ren'Py review. It answers:

1. Which QSP-style systems already exist here.
2. Which parts are only partial or inconsistent.
3. Which old assumptions/docs are now stale.
4. Which style to use for future actions, quests, and helper logic.

---

## Overall Assessment

This is no longer a raw skeleton.

The project already has:

- a real location-entry layer
- a room/exits/items/NPC model
- reusable action labels
- reusable helper labels
- many implemented world/location labels
- report/card/image helpers
- daily event and time systems

So from a QSP perspective, this is already a functioning port framework, not just a prototype.

The main remaining issue is not "nothing is implemented".
The main issue is that the QSP compatibility logic is now spread across many focused `.rpy` files instead of one clearly centralized bridge, and some docs still describe older missing pieces that are already implemented.

---

## Implemented QSP-Style Foundations

### 1. Location entry model: implemented

Files:

- `game/Inn/Loc.rpy`
- many location files under `game/Inn/*.rpy`

What exists:

- `prepare_location_entry(loc_name="")`
- `label LOC(loc_name="")`
- `label EnterLocation(loc_name="")`

This is already the closest Ren'Py equivalent of QSP location-entry normalization:

- set current location
- decide whether time advance is blocked
- synchronize `CurLoc` / `location`
- run entry checks

QSP perspective:

- equivalent to a standardized `gt` entry contract
- good foundation
- should stay the canonical location-entry path

Status: implemented and important.

### 2. Room graph / world-node model: implemented

File:

- `game/Inn/RoomTemplate.rpy`

What exists:

- `RoomExit`
- `RoomDescription`
- `RoomScene`
- `RoomTrigger`
- `RoomSchedule`
- `Room`

This already gives the project a structured replacement for loose QSP location text:

- descriptions
- exits
- objects/items
- NPC presence
- schedules
- triggers

QSP perspective:

- this is the strongest current replacement for raw `act ... gt ...`
- it is already suitable as the authoritative room/navigation layer

Status: implemented.

### 3. Lookup tables are already ported to dict-style data: implemented

Important correction:

The original QSP/TXT project may still contain table-like source data, but in this Ren'Py project the active runtime lookup layer is already dict-based.

Examples visible in the current code:

- `RealName`
- `RealName2`
- `Talked`
- `Friends`
- `HadSex`
- `DraupnirVar`
- `ShortDressName`
- `DressDesc`
- `FullDressDesc`
- dress/body/character maps used by `GirlsDesc.rpy`

QSP perspective:

- TXT files should be treated as source reference only
- runtime tables are no longer supposed to stay in TXT form
- for current Ren'Py behavior, dicts are the real lookup tables

This matters because future analysis should not describe lookup tables as "still left in TXT files" unless the code actually reads them dynamically at runtime.

Status: implemented and already adopted as project style.

### 4. World/navigation labels: implemented in the starter scope

Files/examples:

- `game/Inn/TavernMain.rpy`
- `game/Inn/StreetTavern.rpy`
- `game/Inn/MarketPlace.rpy`
- `game/Inn/GroceryStore.rpy`
- `game/Inn/WineStore.rpy`
- `game/Inn/Church.rpy`
- `game/Inn/EllonaTemple.rpy`
- `game/Inn/PortStreets.rpy`
- `game/Inn/ArtisansQuarter.rpy`
- `game/Inn/StolyarWorkshop.rpy`
- `game/Inn/DressShop.rpy`
- `game/Inn/SherwoodTravel.rpy`
- `game/Inn/BeckyHomeFront.rpy`
- `game/Inn/BeckyHome.rpy`
- `game/Inn/CityGuard.rpy`
- `game/Inn/FridayDance.rpy`

The starter world-location set described in docs is mostly real code now, not planned code.

QSP perspective:

- core location graph exists
- location files are no longer just placeholders
- major world hubs are implemented as labels

Status: implemented in meaningful scope.

### 5. Generic action labels: implemented

File:

- `game/Inn/Actions.rpy`

Confirmed generic action labels:

- `label Examine(...)`
- `label Take(...)`
- `label Drop(...)`
- `label Drink(...)`
- `label MakeFire(...)`
- `label Clean(...)`
- `label Chop(...)`

These are exactly the kind of reusable action endpoints a QSP-style port needs.

QSP perspective:

- this is the correct direction
- these labels should be preferred over burying action logic inside long menu blocks

Status: implemented and should be expanded.

Important clarification:

These generic labels are support endpoints, not the primary action architecture.

The actual runtime model is:

- room as container
- room contents (`game_items`, `npcs`, `exits`) as action owners
- room-exposed MC self-actions as another action category
- room/object/NPC builders assemble the visible action list

So this project should not be described as "a central catalog of action methods".
It is a contextual action system assembled from current room state.

### 6. Character interaction hub: implemented

File:

- `game/Inn/CharacterActionHub.rpy`

What exists:

- `label CharacterActionHub(...)`
- inspect path through `GirlsDesc`
- talk path through a passed-in talk label

QSP perspective:

- equivalent to a standardized NPC action menu
- already follows a label-first call pattern
- good model for future NPC interaction expansion

Status: implemented.

### 7. Image helper layer: implemented

File:

- `game/Inn/ShowImage.rpy`

What exists:

- python helper `show_image(...)`
- compatibility function `ShowImage(...)`
- compatibility function `ShowImageSeq(...)`
- labels:
  - `ShowImage`
  - `ShowImageSeq`
  - `show_image`
  - `show_image_seq`

QSP perspective:

- this already replaces a big part of legacy `gs "ShowImage"` style behavior
- both function and label entry points exist

Status: implemented.

### 8. Character description/report layer: implemented

Files:

- `game/Inn/GirlsDesc.rpy`
- `game/Inn/PlayerCard.rpy`
- `game/Inn/menu_tavernstat.rpy`

What exists:

- actual descriptive assembly for NPCs
- player card screen/label
- tavern report labels

QSP perspective:

- report/stat/card assembly is not missing
- it already lives in dedicated files
- this is usable for further extension

Status: implemented.

### 9. Time / turn system: implemented

Files:

- `game/script.rpy`
- `game/Inn/TimeTurnSystem.rpy`
- `game/Inn/TimeChangeMenu.rpy`
- `game/Inn/AdvanceTime.rpy`
- `game/Inn/NextDay.rpy`

What exists:

- calendar engine
- time slot names
- minute-based advance
- next-day flow
- movement-time label
- time change menu

QSP perspective:

- time system is real and active
- not missing

Status: implemented.

### 10. Daily event / scheduled content layer: implemented

Files:

- `game/Inn/CheckDailyEvent.rpy`
- `game/Inn/CreateMandatoryEvents.rpy`
- `game/Inn/CreateTavernEvents.rpy`
- `game/Inn/CreateTavernEventsPeriod.rpy`
- `game/Inn/DisplayTavernEventShort.rpy`

QSP perspective:

- event scheduling and day-cycle logic already exist as real labels/helpers
- this is not a stubbed area anymore

Status: implemented.

---

## Implemented But Structurally Inconsistent

These parts work, but from a QSP-port perspective they are not yet normalized enough.

### 1. Location entry is implemented, but not perfectly normalized

Many world labels now call `EnterLocation(...)`, which is good.

But some files also manually repeat:

- `CurLoc = ...`
- `location = CurLoc`

after the entry call.

QSP perspective:

- this is redundant
- location entry should be standardized through one contract
- duplicated location-state assignment creates maintenance risk

Recommended direction:

- keep `EnterLocation(...)` as canonical
- avoid repeating manual location sync unless there is a specific exception

### 2. Compatibility logic exists, but is scattered

File:

- `game/Inn/RuntimeCompat.rpy`

Current status:

- old central compatibility bridge is retired
- wrappers were moved into many dedicated files

QSP perspective:

- this is workable
- but it makes the port harder to reason about
- there is no single "QSP compatibility surface" anymore

Recommended direction:

- keep actual logic in dedicated files
- but add one documentation map of which QSP primitive/helper now lives where

### 3. Docs about missing functions are stale

File:

- `game/Inn/missing_functions.rpy`

This file still suggests things like these are missing:

- `GirlsDesc`
- `ShowImage`
- `NamesSet`
- `CreateDonationsList`
- `SexEventsTableCode`
- `OtherFunctionsCode`
- `CreateMandatoryEvents`
- `CreateTavernEventsPeriod`

But those now exist as real `.rpy` files.

QSP perspective:

- this file is stale
- it can mislead future work

Recommended direction:

- either remove it
- or rewrite it as a historical note / resolved stub list

### 4. Alias/canonical naming is still mixed

Docs still mention alias issues like:

- `city_guard` vs `CityGuard`
- `friday_dance` vs `FridayDance`
- `becky_home_front` vs `BeckyHomeFront`
- `becky_home` vs `BeckyHome`

The actual codebase now uses more canonical PascalCase labels in many places.

QSP perspective:

- alias compatibility is useful
- but canonical names should be stable and documented

Recommended direction:

- pick one canonical label per location
- keep alias entry points only as compatibility shims

---

## Not Yet Fully Implemented Or Still Risky

This section is the real "what is not done yet" list.

### 1. Single authoritative QSP mapping document is still incomplete

There are already strong docs:

- `devdocs/LOCATION_WORKLIST.md`
- `devdocs/TXT_TO_RPY_NAV_MATRIX.md`

But they are partly stale relative to the code.

What is still missing:

- one up-to-date source-to-runtime status sheet
- one clean list of resolved vs unresolved QSP helpers
- one current canonical alias map that matches runtime code

Status: partial.

### 2. Some old blocker notes in docs are outdated and need re-validation

Example:

- `WhoreNextDayClients` is described in older docs as missing
- but `game/Inn/WhoreNextDayClients.rpy` now exists

QSP perspective:

- blockers should be re-audited from the current code, not inherited from old notes

Status: documentation debt.

### 3. Movement-time semantics may diverge from intended QSP behavior

File:

- `game/Inn/TimeTurnSystem.rpy`

Current behavior:

- `AdvanceMovementTime` applies a default movement cost of `30` minutes

Older worklist note says movement should likely default to `0` unless explicitly advanced by source logic.

QSP perspective:

- this is a real design/parity question
- not just formatting

If original QSP movement usually did not auto-advance time, then the current Ren'Py behavior is a mechanic change.

Status: implemented, but parity should be reviewed.

### 4. Some action/menu logic is still embedded in location files instead of extracted

Many location files already follow a good pattern:

- main location label
- `BuildActions`
- `ObjectMenu`
- `ObjectText`
- local specialized labels

But some location/event files still keep too much custom flow inline.

QSP perspective:

- this makes conversion harder to audit
- reusable action blocks should be extracted into dedicated labels where possible

Status: partial normalization.

### 5. No single centralized "gs-equivalent service registry"

Instead of one clear service-dispatch surface, helper behavior is distributed across many dedicated `.rpy` files.

That is not wrong, but from a QSP port-maintenance perspective it means:

- helper discovery is slower
- port parity checking is slower
- action conversion choices are less obvious

Status: architecturally workable, but not yet neat.

### 6. TXT source remains reference material, not runtime authority

This project should be understood as:

- TXT/QSP files = original source reference
- Ren'Py dicts / labels / room objects = actual runtime authority

That especially applies to:

- lookup tables
- relationship/state maps
- dress/item descriptors
- schedule/event tables that have already been rewritten into Python/Ren'Py structures

So for future work:

- do not preserve TXT lookup tables just for parity
- preserve meaning, not original container format
- use dicts when the data is already converted and stable

---

## What Is Clearly Already Better Than A Skeleton

The following areas should not be treated as "missing":

- `GirlsDesc`
- `ShowImage`
- `PlayerCard`
- `WhoreNextDayClients`
- `CreateMandatoryEvents`
- `CreateTavernEventsPeriod`
- `OtherFunctionsCode`
- `SexEventsTableCode`
- `NamesSet`
- multiple world hub labels
- generic action labels
- location entry helpers

These are real and active now.

---

## Recommended Action Style For Future Work

User preference: some action `.rpy` files should behave like labels for simplicity.

That preference is correct.

### Preferred style

For new functionality, prefer:

1. one dedicated `.rpy` file per reusable action/domain block
2. one or more explicit labels as the entry points
3. optional python helper functions only when the logic is truly data-like

Good existing examples:

- `Actions.rpy`
- `ShowImage.rpy`
- `CharacterActionHub.rpy`
- `CreateDonationsList.rpy`
- `WhoreNextDayClients.rpy`
- `TimeChangeMenu.rpy`

### Why label-first is better here

From a QSP perspective, labels are the cleanest equivalent of:

- `gt`
- `gs`
- named action blocks
- reusable event blocks

Benefits:

- easier call graph
- easier traceability from source TXT/QSP logic
- easier aliasing
- easier debugging in Ren'Py
- easier documentation

### Recommended split

Use labels for:

- actions
- event branches
- reusable menu handlers
- object interaction flows
- NPC interaction endpoints
- shop/buy/sell/apply actions

Use python functions for:

- pure calculations
- text assembly helpers
- lookup tables
- filter/schedule checks
- state normalization helpers

### Practical rule

If something is "a thing the player can do" or "a branch that QSP would call by name", prefer a label.

If something is "a pure helper that computes data", prefer python.

---

## Recommended Refactor Direction

### 1. Keep location labels canonical

One canonical label per location.
Aliases only as wrappers if needed.

### 2. Keep action files label-first

Examples to preserve as style:

- `Take`
- `Drop`
- `Drink`
- `CharacterActionHub`
- `ShowImage`

### 3. Normalize location entry

Make every world/location label rely on:

- `call EnterLocation("...")`

and avoid duplicating state sync unless necessary.

### 4. Replace stale missing-function docs

`missing_functions.rpy` should no longer define the team’s understanding of port status.

### 5. Audit parity, not just existence

The next useful audits are:

- movement time parity
- alias/canonical label parity
- world label entry consistency
- event dispatch parity
- extracted action coverage vs inline logic

---

## Bottom Line

From a QSP perspective, the project already implements the core port architecture:

- locations
- entry normalization
- actions
- reports
- images
- cards
- event/day logic
- many world labels

What is still lacking is not the foundation.
What is still lacking is normalization, parity cleanup, and clearer canonical structure.

So the correct reading is:

- base QSP-to-Ren'Py runtime: implemented
- starter world graph: implemented
- helper/action ecosystem: implemented
- consistency/canonicalization: still incomplete
- old status docs: partly stale

And yes: future action `.rpy` files should stay label-oriented for simplicity and source parity.
