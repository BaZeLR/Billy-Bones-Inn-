# Script, Time, UI Pattern Notes

Reference project inspected:

`C:\Users\blank\Documents\RenPy_Projects\FamilyLife-0.1.1-base+Event0\game`

## FamilyLife Structure

FamilyLife keeps the sandbox loop centralized.

- `script.rpy`
  - Defines location groups: `homeLocations`, `cityLocations`, `mallLocations`, `upstairsLocations`, `allLocations`.
  - Defines calendar/time defaults: `year`, `month`, `mday`, `hour`, `minute`, `wday`, `numDay`, `datestr`.
  - Defines event cache state: `availEvents`, `eventLocations`, `eventPeople`, `eventTalk`, `eventOptions`, `eventItems`, `eventPath`.
  - `after_load` and `before_main_menu` call `initPeople()`, `initThreads()`, `initEvents()`.
  - `startLocation(newloc)` is the standard entry gate for each room:
    - clears scene state with `vscene`
    - validates stats/time
    - calls `findAvailableEvents()`
    - sets `location`
    - checks open/closed state
    - checks automatic enter triggers
    - calls `setEventPath()`

- `events.rpy`
  - `Event` objects own target label, day/hour conditions, requirements, location, action, priority, and thread binding.
  - `findAvailableEvents()` builds the current event/action map and highlight sets.
  - `checkTriggers(location, action, numpop)` jumps to the correct event.
  - `preEvent()` marks threaded event progress and disables time skip while an event is running.

- `people.rpy`
  - `PeopleData` is static person data and schedule location logic.
  - `PeopleInfo` is runtime relationship/talk/gift state.
  - UI asks people data for icons and current locations instead of hardcoding room membership.

- `01vscene.rpy`
  - Adds a custom `vscene` statement.
  - One command clears the old scene and shows an image/video in the configured visual area.
  - The source supports `.webm`; Tractir has already been extended for `.mp4`/`.m4v`.

## FamilyLife Time Loop

FamilyLife uses real clock time.

- `advanceTime(minutes)` adds minutes.
- `validateStats()` normalizes minutes into hours, hours into days, weekdays, months, years, and updates derived stats.
- `skipHour` advances one hour, then returns to the current location.
- `goToSleep()` handles night wrap, weekly evaluation, daily decay/reset, and morning placement.
- Open hours are checked by `isOpen(location)`.

The important part is the ownership model:

- `startLocation(newloc)` is the location-entry gate.
  - It clears the visual scene.
  - It calls `validateStats()`.
  - It rebuilds available events with `findAvailableEvents()`.
  - It sets `location`.
  - It rejects closed locations through `isOpen(location)`.
  - It checks automatic enter triggers through `checkTriggers(...)`.
  - It updates the visible event path with `setEventPath()`.

- `advanceTime(minutes)` is only a delta-time helper.
  - It mutates `minute`.
  - It immediately calls `validateStats()`.
  - It does not own daily consequences or story cleanup.

- `validateStats()` is a normalization and derived-stat pass.
  - It rolls minutes into hours, hours into days, and days into month/year counters.
  - It updates weekday and always-increasing day number.
  - It rebuilds date text.
  - It clamps money, relationship, and player stats.
  - It recalculates derived stats like beauty/fashion/charisma.
  - It should stay mostly pure and should not hide story progression.

- `goToSleep()` is the daily checkpoint.
  - It calls `weeklyEvaluation()` before the night reset.
  - It checks long-term failure/success conditions and calls endings.
  - It advances the clock to morning.
  - It applies nightly stat decay and daily counter resets.
  - It resets per-NPC daily interaction state.
  - It applies overdue-promise consequences.
  - It applies thread-completion achievement activation.
  - It checks bedtime triggers.
  - It shows pending achievements/dreams.
  - It checks morning triggers.

- `weeklyEvaluation()` is guarded by a concrete week/time condition.
  - It returns immediately if the current day/time is not the evaluation window.
  - It scores weekly chores.
  - It applies relationship gains/losses.
  - It resets weekly counters only when the evaluation actually runs.

- Achievements are registry-driven.
  - `activated` stores achievements earned but not yet shown.
  - `achieved` stores achievements already presented/unlocked.
  - `achievementOrder` controls display order.
  - `achievements` stores title/body text.
  - `screen achievements()` displays only unlocked achievements unless the hidden-toggle is enabled.
  - `showDreams()` drains newly activated achievements into `achieved` by calling `showDream(...)`.

- Endings are registry-driven.
  - `endings` stores endings already reached.
  - `endingDesc` stores result category and description.
  - `screen endings()` displays unlocked endings with the same hidden-toggle pattern.
  - `showEnding(ending)` records the ending, shows its media/text, then returns to the sandbox instead of destroying the save.

Tractir uses slot time plus calendar helpers.

- Canonical calendar lives in `game/script.rpy` as `calendar_*` functions.
- `game/time_calendar.rpy` is now a wrapper.
- `game/Inn/AdvanceTime.rpy` advances one slot or calls `NextDay`.
- `game/Inn/TimeTurnSystem.rpy` handles movement cost in minutes and refuses to roll movement into the next day.
- `game/Utilities/Time/NextDay.rpy` is Tractir's daily checkpoint.
- `game/Utilities/Time/NextDay_FinishDayEvents.rpy` owns finish-day consequences and daily interaction resets.
- `game/Utilities/Time/NextDay_TavernDaily.rpy` owns tavern economy/resource simulation for the completed day.
- `game/Utilities/Time/NextDay_NewDayEvents.rpy` owns new-day random scheduling and daily event creation.
- `game/Inn/PlayerChoresSystem.rpy` owns the weekly chores evaluation and already follows the FamilyLife guard pattern.

Practical rule for Tractir:

- Use `calendar_*` helpers for actual time math.
- Use `time` slots for event conditions and schedules.
- Use `movement_actions(target, minutes)` for room buttons. It applies the time
  mutation, then jumps to the destination.
- Use `AdvanceTime` or `NextDay` for deliberate waiting/rest.
- Schedule location is projected directly from each `PeopleData` owner. Do not
  synchronize or copy it into NPC instances after time changes.

Tractir's equivalent daily flow should be:

1. Finish current day consequences.
   - Process queued sex/event consequences.
   - Reset daily talk/flirt/gift/ask state.
   - Clamp friendship and temporary state.
   - Decrement temporary curses, stolen-horse timers, clothing/hair/soap timers.

2. Simulate tavern day.
   - Visitors, wine, products, revenue, fixed costs, fame, food shortages.
   - Apply dog, werecat, rat, chore, and service-quality effects here.

3. Roll calendar.
   - Use `calendar_advance_days(1)`.
   - Set slot to morning with `calendar_set_time_slot(0)`.
   - Do not manually mutate `day/month/week/hour/minute` outside the calendar helpers unless the helper is being fixed.

4. Create new-day events.
   - Random daily events belong here.
   - NPC schedules should be synced here.
   - Story threads should not be advanced here unless the new day itself is the explicit event.

5. Evaluate weekly/monthly systems at guarded checkpoints.
   - Weekly chores: Sunday evening/night guard.
   - Monthly contacts: use a stable `year * 100 + month` stamp or equivalent.
   - Achievement/ending checks should be explicit functions called from this checkpoint.

6. Return through the main UI.
   - Show the day report as a card/screen.
   - Return to the correct location or post-sleep story event.
   - Avoid room-local hidden reset code.

Missing Tractir piece compared with FamilyLife:

- Implemented in `game/Utilities/General/Common/AchievementsEndings.rpy`.
- Current registry shape:
  - `default tractir_activated_achievements = set()`
  - `default tractir_achieved = set()`
  - `default tractir_endings = set()`
  - `define tractir_achievement_order = [...]`
  - `define tractir_achievements = {...}`
  - `define tractir_ending_desc = {...}`
  - `label TractirCheckAchievements`
  - `label TractirShowPendingAchievements`
  - `label TractirShowEnding(ending_id)`
  - `label TractirCheckEndings`
  - `screen tractir_progress_panel`
- The right HUD opens this through the `Итоги` overlay.
- `NextDay.rpy` calls achievement and ending checks at the daily checkpoint.
- Current first-pass achievements:
  - first month survived
  - Sandra secured her future
  - notoriety thresholds at 25, 50, and 75
- Current first-pass endings:
  - bankruptcy
  - empty tavern
  - maid revenge hook
  - fatal boss fight hook
- Future content can arm the non-economic endings through:
  - `tractir_mark_maid_revenge_ready(reason)`
  - `tractir_mark_boss_fatal_loss(enemy_id)`
- Sandra's first-month thanks can mark `SandraVar["SecuredFuture"]` and reduce `cancumdaily` by one, minimum one. This uses the existing sex-time cap instead of adding a parallel counter.

Achievement checks should depend on explicit thread/event state, for example:

```renpy
if threads["melissaBatProblem"].completed:
    $ tractir_activated_achievements.add("melissa_bat_problem_solved")
```

Ending checks should depend on stable economy/story conditions, for example:

```renpy
if money == 0:
    call TractirShowEnding("bankrupt")
```

## FamilyLife UI Pattern

FamilyLife has two UI layers.

- Standard `screens.rpy`
  - `choice(items, label=None, menu_name=None)` calls `updateMenu()` and `highlightMenu()` before drawing buttons.
  - Menu entries can be mutated by active event triggers.

- Sandbox HUD in `status.rpy`
  - Always-on right panel.
  - Shows date/time, player stats, relationship rows, chores, shortcuts, locate menu, thread board.
  - `locateMenu()` uses `peopleData[pname].getLocation(wday, hour)`.

- Location menus in `locate.rpy`
  - `locmenu(items, icons={}, menu_name=None)` is a native Ren'Py menu screen.
  - Shows action choices plus current NPC icons.
  - `getNPCicons(location)` loops through `peopleData` and asks each person if they are in the room.
  - `highlightMenu()` colors menu/path/person entries when active event sets contain them.

- Room files like `home.rpy`, `city.rpy`, `mall.rpy`, `upstairs.rpy`
  - Each room label calls `startLocation("room_id")`.
  - Shows one `vscene`.
  - Uses a compact `menu (screen="locmenu", icons=getNPCicons(location), menu_name="menu_"+location):`.
  - Menu actions call an event/action label, then jump back to the same room.

## Tractir Match

Tractir already has a different UI contract that should be preserved.

- `game/Inn/my_layouts/main_layout.rpy`
  - Persistent `main_ui` with left scene panel and right action/person panel.
  - `current_action_panel()` displays either explicit action items, custom content, NPC action specs, or room-derived actions.
  - `main_ui_set_action_panel()` is the safe way to replace right-panel content for an event/submenu.
  - `main_ui_restore_room_scene_state()` returns to normal room actions without destroying the UI.

- `game/Inn/my_layouts/build_room_action_items.rpy`
  - Builds object and exit actions from room data.
  - Movement exits use `movement_actions()` so the old room is not retained on
    Ren'Py's return stack.

- `game/Inn/StoryEventRuntime.rpy`
  - Now matches the FamilyLife style better: event/thread classes are the blueprint, conditions are constructed into event rows, and availability is checked through thread/event methods.

- `game/Inn/PeopleRuntime.rpy`
  - New FamilyLife-style people layer.
  - Bridges existing Tractir maps and schedules into `peopleData` and `peopleInfo`.

## Implementation Standard For New Tractir Content

For a readable room/event label:

```renpy
label SomeRoomEvent:
    $ main_ui_begin_native_scene_state("Событие")
    show screen main_ui
    vscene "images/path/to/picture.jpg"
    "Scene text."

    menu:
        "Продолжить":
            call SomeRoomEventContinue
        "Вернуться":
            pass

    $ main_ui_end_native_scene_state()
    return
```

For a clean condition:

```renpy
$ amanda = getPersonInfo("amanda")
if amanda.isInLocation("TavernAmandaRoom") and amanda.corruption >= 20:
    call SomeAmandaEvent
```

For thread/event construction:

- Put real conditions in the event/thread rows.
- Use person/location helpers instead of duplicating `CurrentLoc` checks everywhere.
- Use named callable conditions when the condition is complex.
- Keep the label focused on display, text, menu choices, and mutations.

## What To Borrow

Borrow from FamilyLife:

- One standard room-entry gate.
- One event availability cache.
- Clear `PeopleData`/`PeopleInfo`.
- `vscene` for single-line image/video changes.
- Event-derived highlighting for locations, people, and action menu entries.
- Menu/action mutation through one helper layer.

Do not copy directly:

- FamilyLife's native `locmenu` should not replace Tractir's right panel.
- FamilyLife's real-hour calendar should not replace Tractir's slot calendar.
- FamilyLife's status HUD should not replace `main_ui`.

Correct direction for Tractir:

- Feed `main_ui` from the same clean data that FamilyLife feeds into `locmenu`.
- Keep room labels readable: `enter room`, `vscene`, `text`, `main_ui_set_action_panel`, `return/jump`.
- Keep event logic visible in event/thread rows and named condition functions.
