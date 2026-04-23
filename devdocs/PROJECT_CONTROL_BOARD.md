# Project Control Board

Last updated: 2026-04-23

This file is the working control board for current stabilization work.

Use it for:
- active canonical TODOs that still block correct gameplay behavior;
- verified fixes from the current pass;
- files already staged to git for control.

Rules:
- do not treat old regression expectations as canonical if they conflict with current templates/rules;
- when behavior changes intentionally, update the targeted test coverage for that behavior;
- when a fix is verified, add it here and stage it;
- do not mix unrelated dirty worktree changes into the staged set.

## Active Priority TODO

- [ ] NPC scheduling audit and normalization.
Problem:
NPC presence is still inconsistent across the project because some locations read old derived state, some read `CurrentLoc`, some read schedule helpers, and some still depend on legacy assumptions.
What must be normalized:
- every room that surfaces NPCs must resolve presence from the canonical scheduler/current-location model;
- room text, visible NPC buttons, event conditions, and action menus must agree on the same active NPC set;
- special overrides such as tavern temporary room logic, breakfast attendance, church attendance, market/store shifts, and Friday/Sunday special cases must remain explicit but route through the same truth model;
- targeted regression coverage must be updated to match the canonical behavior after each verified schedule fix.
Initial hotspots already identified:
- `GroceryStore`
- `PortStreets`
- tavern household rooms and shared areas
- church/market roundtrip cases

- [ ] Port Streets NPC routing audit.
Problem:
Character buttons there still use custom/manual action building instead of the canonical room/NPC action path everywhere.
Known symptom:
- Melissa route from Port Streets was reported as returning to `TavernMain`.
- Georgett unknown-woman lower-grid route used to bypass room-specific restore and could drop the player into the wrong post-talk state.

- [ ] Player card and inventory back-flow audit.
Problem:
Back behavior must respect entry context consistently:
- inventory opened from player card returns to player card;
- inventory opened from room HUD returns to the current room UI;
- player card `Назад` returns to current location UI.
Open follow-up:
- several older player-room tests still assume the chest opens inventory directly; those tests need to be migrated to the current player-card/HUD inventory entry flow.

- [ ] Object menu behavior audit.
Problem:
Only `Назад` should return from `game_item` / object screens to the room screen.
Scope:
- main hall fireplace
- kitchen hearth/cauldron
- other room-local object menus using custom return logic

- [ ] UI action panel placement audit.
Problem:
Action/event menus should respect the canonical right HUD panel placement and avoid overlaying the upper screen unnecessarily.
Current target:
- keep action menus effectively centered in the right action HUD area, near `xalign 0.5`, lower-aligned.

- [ ] Continue variable overlap audit by system after the age collision cleanup.
Problem:
The first real declaration collision is removed, but the project still needs ongoing overlap audits before adding new variables.
Current state:
- `age` is the player scalar;
- `age_girls[npc_id]` and `DateOfBirth[npc_id]` are the canonical NPC age/birthday model;
- declared-variable index now reports `0` exact duplicates and `0` case-collision groups;
- future overlap audits should use `GAME_VARIABLES_INDEX.md` before adding new names.
What must be normalized:
- no new capitalized `Age` usage;
- no new duplicate or case-colliding declarations;
- new variable additions must be checked against the index and glossaries first.

## Verified This Pass

- [x] Clara/Mongol market-conspiracy chain now continues past the daytime booklet scene into evening theft, Clara’s confession, Mongol’s arrest, night food, lockpick order, and rescue.
Files:
- `game/Inn/StoryEventRuntime.rpy`
- `game/Inn/InitClara.rpy`
- `game/Inn/InitSecondaryNPC.rpy`
- `game/Inn/IntClaraTalk.rpy`
- `game/Inn/CityGuard.rpy`
- `game/Inn/StolyarWorkshop.rpy`
- `game/Inn/MarketPlace.rpy`
- `game/UiRegressionTests.rpy`
Verification:
- targeted Ren'Py UI tests passed:
  - `ui_regressions::clara_market_booklet_event_unlocked_after_melissa_drawings`
  - `ui_regressions::clara_market_booklet_event_triggers_outside_old_market_parity`
  - `ui_regressions::clara_mongol_horse_theft_and_rescue_live_path`
  - `ui_regressions::melissa_clara_sandra_werecat_full_live_click_path`
- Ren'Py `compile` passed.
Result:
- the old two-event Clara market thread now advances through the full conspiracy/rescue chain instead of stopping after the daytime scene;
- the evening follow step uses a higher exploration threshold and can keep retrying until the player succeeds;
- Clara’s deeper confession is now surfaced through her live talk menu in the wine store;
- the night guard-building path is reachable even after the market closes;
- rescuing Mongol now sets a persistent pass flag for later Sherwood/outlaw content.

- [x] Melissa bat arc progression is now thread-owned instead of room/talk hybrid.
Files:
- `game/Inn/MelissaBatsQuest.rpy`
- `game/Inn/StoryEventRuntime.rpy`
- `game/Inn/TavernAtic.rpy`
- `game/Inn/TavernAmandaRoom.rpy`
- `game/Inn/TavernUpstairs.rpy`
- `game/Inn/IntMelissaTalk.rpy`
- `game/UiRegressionTests.rpy`
Verification:
- targeted Ren'Py UI tests passed:
  - `ui_regressions::melissa_bats_can_progress_from_night_noise_to_colony_and_completion`
  - `ui_regressions::melissa_post_bats_talk_unlocks_sex_engine_entry`
  - `ui_regressions::melissa_clara_sandra_werecat_full_live_click_path`
- Ren'Py `lint` passed.
- Ren'Py `compile` passed.
Result:
- `melissaBatProblem` now contains explicit attic, drawings, cleanup, and completion steps instead of stopping at three events;
- attic/Amanda-room/TavernMain Melissa buttons now route through `checkTriggers(...)` into the current thread event;
- Melissa’s bat progression no longer depends on direct room or talk handlers mutating `bats_episode` outside the active thread;
- Melissa bat regressions now assert stage/thread progress instead of dead checklist flags.

- [x] Room runtime restore now preserves live room item state across save/reload code paths.
Files:
- `game/Inn/RoomTemplate.rpy`
- `game/UiRegressionTests.rpy`
Verification:
- targeted Ren'Py UI tests passed:
  - `ui_regressions::room_runtime_restore_keeps_taken_shed_axe_out_of_room`
  - `ui_regressions::taking_shed_axe_moves_it_from_room_to_player_inventory`
  - `ui_regressions::save_smoke_with_lumber_item_registry_does_not_pickle_item_conditions`
- Ren'Py `lint` passed.
- Ren'Py `compile` passed.
Result:
- taking the shed axe now survives room runtime restore instead of reappearing after code reload;
- room mutable `game_items` are restored onto the current code-defined room object instead of being discarded.

- [x] Grocery store shift visibility now resolves from the active schedule/current-location truth instead of stale tavern-only room checks.
Files:
- `game/Inn/GroceryStore.rpy`
Verification:
- Ren'Py `lint` passed.
- Ren'Py `compile` passed.

- [x] Main hall fireplace object flow now matches the kitchen object-menu pattern.
Files:
- `game/Inn/TavernMain.rpy`
Verification:
- Ren'Py `lint` passed.
- Ren'Py `compile` passed.
Result:
- object actions stay inside the object menu;
- only `Назад` returns to the hall.

- [x] Inventory back-routing now respects open context.
Files:
- `game/Inn/PlayerCard.rpy`
- `game/Inn/my_layouts/main_layout.rpy`
Verification:
- Ren'Py `lint` passed.
- Ren'Py `compile` passed.
Result:
- room HUD inventory returns to room UI;
- player-card inventory returns to player card.

- [x] Long room-click smoke path updated to current canonical labels and room flow.
Files:
- `game/UiRegressionTests.rpy`
Verification:
- targeted Ren'Py UI test `ui_regressions::gameplay_long_smoke_path_room_sleep_attic_recipe_backyard_forest` passed.
Result:
- Melissa room transition no longer appears frozen in the suite;
- attic recipe-book segment now reflects the current room/object flow instead of removed inventory shortcuts.

- [x] Outdated attic / player-room inventory regression cluster partially normalized to current canonical flows.
Files:
- `game/UiRegressionTests.rpy`
Verification:
- targeted Ren'Py UI tests passed:
  - `ui_regressions::attic_recipe_book_can_be_read_from_inventory_menu`
  - `ui_regressions::attic_rifle_and_cuirass_can_be_equipped_and_unequipped`
  - `ui_regressions::attic_equipped_armor_caption_does_not_use_text_interpolation_brackets`
  - `ui_regressions::attic_items_can_be_dropped_from_attic_inventory_menu`
  - `ui_regressions::my_room_dropped_book_changes_room_picture_and_description`
  - `ui_regressions::my_room_dropped_rifle_changes_room_picture_and_can_be_taken_back`
Result:
- stale chest-only inventory assumptions were removed from this cluster;
- player-room storage tests now follow the current room + player-card contracts;
- attic-specific drop behavior is now tested through the attic inventory path instead of the removed chest route.

- [x] Canonical method and variable glossaries added for naming consistency control.
Files:
- `devdocs/METHODS_GLOSSARY.md`
- `devdocs/VARIABLES_GLOSSARY.md`
- `devdocs/agent.txt`
Result:
- core method names now have one project glossary;
- core runtime variables now have one project glossary;
- future additions should update these docs to make redundancy easier to spot.

- [x] Exhaustive declared game-variable index added for overlap and redundancy audits.
Files:
- `devdocs/GAME_VARIABLES_INDEX.md`
- `devdocs/agent.txt`
Result:
- active `.rpy` `default` and `define` declarations now have one full index;
- exact duplicate names and case-collision groups are surfaced at the top;
- future variable additions should be checked against this index before adding new names.

- [x] First real variable collision pass completed for age naming.
Files:
- `devdocs/GAME_VARIABLES_INDEX.md`
- `devdocs/VARIABLES_GLOSSARY.md`
- `game/Inn/BeckyHomeFront.rpy`
- `game/Inn/InitAmandaLizaTalkItems.rpy`
- `game/Inn/GiveBirth.rpy`
Verification:
- declared-variable index now reports `0` exact duplicates and `0` case-collision groups;
- active code search excluding `game/saves/` finds no remaining `Age[...]` or NPC `age[...]` usage.
Result:
- `Age[...]` is removed as an active declaration pattern;
- canonical NPC age naming is now `age_girls[npc_id]`;
- player age remains the scalar `age`.

- [ ] Live bug confirmed: player-card rifle load/unload path still fails to surface the `Зарядить дробью` action after clean + oil.
Files:
- `game/UiRegressionTests.rpy`
Observed via:
- targeted Ren'Py UI test `ui_regressions::attic_rifle_can_be_cleaned_oiled_loaded_and_unloaded`
Current symptom:
- after `PlayerCardRifleCleanRust` and `PlayerCardRifleOil`, the player-card rifle item menu still does not expose the load action, so the test times out on `Зарядить дробью`.

- [ ] Live bug confirmed: player-card item menu still does not expose soap / cork use actions.
Files:
- `game/UiRegressionTests.rpy`
Observed via:
- targeted Ren'Py UI tests
  - `ui_regressions::soap_can_be_used_from_inventory_menu`
  - `ui_regressions::cork_can_be_used_from_inventory_menu_to_seal_bottle`
Current symptom:
- the player-card item screen opens, but `Использовать мыло` / `Использовать пробку` are not available there.

- [x] Port Streets lower-grid unknown-woman talk roundtrip now stays in Port Streets and restores the canonical room action menu.
Files:
- `game/Inn/Actions.rpy`
- `game/Inn/my_layouts/main_layout.rpy`
- `game/UiRegressionTests.rpy`
Verification:
- targeted Ren'Py UI test `ui_regressions::georgette_unknown_lower_grid_talk_roundtrip_stays_in_port_streets` passed;
- Ren'Py `lint` passed;
- Ren'Py `compile` passed.
Result:
- scene-mode restore now respects room-specific `BuildActions` refresh targets;
- Port Streets lower-grid NPC interaction no longer falls through to generic room reconstruction;
- after first unknown talk, Georgett stays accessible in the room UI as `Жоржетта`.

- [x] Port Streets Georgette lower-grid talk now keeps explicit street context instead of relying on inferred room state.
Files:
- `game/Inn/CharacterActionHub.rpy`
- `game/Inn/PortStreets.rpy`
- `game/Inn/TavernMain.rpy`
- `game/Inn/my_layouts/main_layout.rpy`
- `game/UiRegressionTests.rpy`
Verification:
- targeted Ren'Py UI test `ui_regressions::georgette_unknown_lower_grid_talk_roundtrip_stays_in_port_streets` passed;
- targeted Ren'Py UI test `ui_regressions::georgette_known_lower_grid_talk_roundtrip_stays_in_port_streets` passed;
- Ren'Py `lint` passed;
- Ren'Py `compile` passed.
Result:
- lower-grid NPC menu now preserves room-specific NPC data through open, talk, and look handlers;
- Georgette in `PortStreets` explicitly opens `IntGeorgettTalk("georgett", "street")`;
- Georgette in `TavernMain` explicitly opens `IntGeorgettTalk("georgett", "tavern")`;
- the known-name lower-grid path no longer has to guess whether it should restore to street or tavern.

- [x] Port Streets NPC actions are now bottom-panel-owned instead of duplicated in the top room action list.
Files:
- `game/Inn/PortStreets.rpy`
- `game/UiRegressionTests.rpy`
Verification:
- targeted Ren'Py UI test `ui_regressions::georgette_action_is_visible_on_port_streets_when_she_is_present` passed;
- targeted Ren'Py UI test `ui_regressions::georgette_talk_from_port_streets_returns_to_port_streets` passed;
- targeted Ren'Py UI test `ui_regressions::georgette_unknown_first_talk_action_is_visible_on_port_streets` passed;
- targeted Ren'Py UI test `ui_regressions::georgette_unknown_lower_grid_talk_roundtrip_stays_in_port_streets` passed;
- targeted Ren'Py UI test `ui_regressions::georgette_known_lower_grid_talk_roundtrip_stays_in_port_streets` passed;
- Ren'Py `lint` passed.
Result:
- Georgette and Lizetta no longer appear as duplicate top action buttons in Port Streets;
- their interaction entry there is the bottom visual NPC panel only;
- the room action list now stays for room objects, exits, dog, and special street events.

- [x] Tavern Main room-object return now restores the current room UI instead of re-entering the Tavern Main label.
Files:
- `game/Inn/Actions.rpy`
- `game/Inn/TavernMain.rpy`
- `game/UiRegressionTests.rpy`
Verification:
- targeted Ren'Py UI test `ui_regressions::tavern_main_restore_rebuilds_current_room_ui` passed;
- targeted Ren'Py UI test `ui_regressions::georgette_known_lower_grid_talk_roundtrip_stays_in_port_streets` passed;
- targeted Ren'Py UI test `ui_regressions::dog_lower_grid_talk_roundtrip_stays_in_backyard` passed;
- Ren'Py `lint` passed;
- Ren'Py `compile` passed.
Result:
- `TavernMainRestore` no longer does `jump TavernMain`;
- Tavern Main now uses an explicit `TavernMainBuildActions` room-action builder;
- Tavern Main now uses a dedicated `TavernMainView` loop like the Kitchen view flow, so object menus are no longer overwritten by a full room rerun after each click;
- back from Tavern Main object context restores the current room action layer instead of rerunning the whole room label.

- [x] Breakfast barber invites now respect actual breakfast attendance.
Files:
- `game/Inn/HouseholdRuntimeEvents.rpy`
- `game/UiRegressionTests.rpy`
Verification:
- targeted Ren'Py UI test `ui_regressions::tavern_breakfast_barber_invite_hidden_for_absent_melissa` passed;
- Ren'Py `lint` passed;
- Ren'Py `compile` passed.
Result:
- `household_barber_request_ready(..., "breakfast")` now rejects absent household members;
- breakfast-only barber options no longer appear for Melissa, Sandra, or Amanda when they are not actually at the table.

- [x] Georgette generic back/restore now returns to the current room UI instead of hard-jumping by legacy location labels.
Files:
- `game/Inn/IntGeorgettTalk.rpy`
- `game/UiRegressionTests.rpy`
Verification:
- targeted Ren'Py UI test `ui_regressions::georgette_known_lower_grid_talk_roundtrip_stays_in_port_streets` passed;
- targeted Ren'Py UI test `ui_regressions::georgette_legacy_restore_returns_to_current_room_not_tavern_main` passed;
- Ren'Py `lint` passed;
- Ren'Py `compile` passed.
Result:
- Georgette's legacy restore path no longer jumps to `PortStreets` or `TavernMain`;
- generic back semantics now match the project rule: return to the current location UI.

## Currently Staged

- [x] `game/Inn/GroceryStore.rpy`
- [x] `game/Inn/PlayerCard.rpy`
- [x] `game/Inn/TavernMain.rpy`
- [x] `game/Inn/my_layouts/main_layout.rpy`
- [x] `game/UiRegressionTests.rpy`
- [x] `devdocs/METHODS_GLOSSARY.md`
- [x] `devdocs/VARIABLES_GLOSSARY.md`
- [x] `devdocs/GAME_VARIABLES_INDEX.md`

## Next Required Test Updates

- [x] Add/update a targeted regression for grocery shift visibility by active grocer.
- [ ] Add/update a targeted regression for room-HUD inventory back routing.
- [ ] Add/update a targeted regression for player-card inventory back routing.
- [ ] Add/update a targeted regression for Tavern Main fireplace object-menu stay-in-object behavior.
- [ ] Finish migrating the remaining inventory tests that still expect unsupported chest/player-card item-use paths.
- [ ] After the player-card item-use bugs are fixed, re-enable direct regression coverage for soap use, cork use, and rifle loading from the player-card inventory item menu.

## Latest Verified Pass

- Melissa / Clara / Sandra thread coverage pass:
- `marketplace_blind_pirate_event_available()` is now limited to daytime market hours, so the blind-pirate crowd scene no longer steals late-evening market thread space from Clara.
- Sandra's weekly gratitude scene is no longer driven by a fake `TavernMyRoom` room-entry story thread.
- `NextDay` now resolves Sandra's weekly gratitude scene through the real post-sleep wake flow, after the next-day report and before returning to the room.
- `SandraWeek5WakeEvent` now uses the Sandra-specific still assets under `images/sandra/` and `images/sandra/thanks/`, and it switches to `images/sandra/talk_0.png` when available for the speaking portion of the scene.
- Melissa's rat thread, bats thread, and post-bats talk unlock now have direct UI regression coverage against the live scene labels and their click choices instead of stale room-wrapper assumptions.
- werecat sequencing is now explicit: the Hunter Club rumor must be heard before forest track discovery unlocks, and the first eligible post-rumor forest search now reveals the tracks deterministically instead of behind a random skip.
- targeted Ren'Py UI test `ui_regressions::clara_market_booklet_event_unlocked_after_melissa_drawings` passed.
- targeted Ren'Py UI test `ui_regressions::melissa_rat_trigger_starts_werecat_first_and_bats_after_two_days` passed.
- targeted Ren'Py UI test `ui_regressions::melissa_bats_can_progress_from_night_noise_to_colony_and_completion` passed.
- targeted Ren'Py UI test `ui_regressions::melissa_post_bats_talk_unlocks_sex_engine_entry` passed.
- targeted Ren'Py UI test `ui_regressions::sandra_week5_thanks_scene_uses_sandra_assets_after_post_sleep` passed.
- targeted Ren'Py UI test `ui_regressions::werecat_hunter_rumor_precedes_forest_tracks` passed.
- targeted Ren'Py UI test `ui_regressions::werecat_hunter_rumor_precedes_forest_tracks_click_path` passed.
- `Forest` now refreshes through `ForestBuildActions` after werecat search narration, so the room keeps its live werecat action items instead of falling back to the generic room menu.
- targeted Ren'Py UI test `ui_regressions::melissa_clara_sandra_werecat_full_live_click_path` passed.
- Ren'Py `lint` passed.
- Ren'Py `compile` passed.

- Sandra wake follow-up pass:
- `nextday_pick_post_sleep_event_label()` is now live and returns `SandraWeek5WakeEvent` for the Monday-morning pending gratitude case.
- Sandra now uses a real four-step `sandraWeeklyEvaluation` thread for the first month of successful weekly chore checks.
- each weekly Monday wake step now has its own numbered event label, escalating text, and escalating Sandra state gains, including `sluttiness["sandra"]`.
- the final monthly step now resolves to the explicit Sandra video if it is present.
- targeted Ren'Py UI test `ui_regressions::melissa_clara_sandra_werecat_full_live_click_path` passed.
- targeted Ren'Py UI test `ui_regressions::sandra_week5_thanks_scene_uses_sandra_assets_after_post_sleep` passed.
- targeted Ren'Py UI test `ui_regressions::sandra_weekly_wake_thread_progresses_through_month_steps` passed.
- Ren'Py `lint` passed.
- Ren'Py `compile` passed.

- Grocery store active staff selection now uses the scheduled slot before any fallback room state, so stale `CurrentLoc["eddie"]` no longer hides Becky during day shift.
- targeted Ren'Py UI test `ui_regressions::grocery_store_day_prefers_becky_schedule_over_stale_eddie_currentloc` passed.
- targeted Ren'Py UI test `ui_regressions::grocery_store_uses_new_eddie_and_becky_pictures` passed.
- Ren'Py `lint` passed.
- Ren'Py `compile` passed.

- Sandra weekly wake / Melissa thread visibility pass:
- `story_melissa_storage_rat_0` now returns to `TavernStorageView` instead of rerunning `TavernStorage`, so the rat scene is not overwritten on entry.
- `melissaClaraOverheard_0` now owns its own current-room action item and returns to `TavernMainView` instead of falling back into normal hall flow immediately.
- Ren'Py `lint` passed.
- Ren'Py `compile` passed.

- Shed item pass:
- if the player already has `old_axe_001`, entering the shed now removes the wall copy from `ShedRoom.game_items`, so there is no second axe in the room action list.
- carried `lumber_001` is now deposited into the shed as one stack action, moving the full carried count into the shed pile in a single click.
- targeted Ren'Py UI test `ui_regressions::shed_drop_carried_lumber_updates_room_and_inventory` passed.
- targeted Ren'Py UI test `ui_regressions::shed_hides_wall_axe_when_player_already_has_it` passed.
- Ren'Py `lint` passed.
- Ren'Py `compile` passed.
