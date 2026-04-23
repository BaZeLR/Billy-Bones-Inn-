# Game Variables Index

Last updated: 2026-04-21

This file is the exhaustive current-project variable declaration index for active `.rpy` files under `game/`.

Purpose:
- prevent invention of new overlapping variables;
- make duplicate or inconsistent naming visible;
- give one place to audit declared store/config/runtime names before adding more.

Scope:
- includes active `.rpy` files only;
- includes both `default` and `define` declarations;
- excludes backups, disabled files, saves, and generated artifacts.

Important interpretation notes:
- `age` is the player age scalar.
- `age_girls[npc_id]` is the intended NPC age store already used by initialization and birthday logic.
- `DateOfBirth[npc_id]` is the intended NPC birthday record.
- capitalized `Age[...]` should not be used as a project pattern.

Summary:
- total declarations: 561
- exact duplicate names: 0
- case-collision groups: 0
- files with declarations: 54

## Exact Duplicate Names

- none

## Case-Collision Groups

- none

## Declaration Count By File

- `game\01vscene.rpy`: 2
- `game\gui.rpy`: 135
- `game\Inn\Actions.rpy`: 1
- `game\Inn\AmandaAtGloryHole.rpy`: 1
- `game\Inn\AmandaDynamicCommonBlocks.rpy`: 2
- `game\Inn\AutosaveSupport.rpy`: 2
- `game\Inn\Backyard.rpy`: 1
- `game\Inn\BarberShop.rpy`: 4
- `game\Inn\BeckyHomeFront.rpy`: 5
- `game\Inn\BodyInteractionModel.rpy`: 1
- `game\Inn\CharacterActionHub.rpy`: 9
- `game\Inn\Church.rpy`: 2
- `game\Inn\CraftingRecipes.rpy`: 6
- `game\Inn\DogCompanion.rpy`: 2
- `game\Inn\DressShop.rpy`: 5
- `game\Inn\DressTry.rpy`: 1
- `game\Inn\EllonaTemple.rpy`: 2
- `game\Inn\FightSystemRuntime.rpy`: 2
- `game\Inn\Forest.rpy`: 3
- `game\Inn\GameItems.rpy`: 5
- `game\Inn\HouseholdRuntimeEvents.rpy`: 5
- `game\Inn\HunterClub.rpy`: 2
- `game\Inn\IncreaseSkill.rpy`: 3
- `game\Inn\InitSecondaryNPC.rpy`: 13
- `game\Inn\Intro.rpy`: 191
- `game\Inn\MarketPlace.rpy`: 2
- `game\Inn\MelissaWerecatQuest.rpy`: 1
- `game\Inn\menu_tavernstat.rpy`: 2
- `game\Inn\ModuleRuntime.rpy`: 4
- `game\Inn\my_layouts\main_layout.rpy`: 11
- `game\Inn\NavigationOnlyMode.rpy`: 1
- `game\Inn\NextDay.rpy`: 2
- `game\Inn\NPCRelationshipLevels.rpy`: 1
- `game\Inn\NPCScheduleModel.rpy`: 1
- `game\Inn\PartEventGirlReactionTalk.rpy`: 1
- `game\Inn\PartEventYourFirstReaction.rpy`: 15
- `game\Inn\PlayerCard.rpy`: 4
- `game\Inn\PortStreets.rpy`: 2
- `game\Inn\PregnancyCheck.rpy`: 5
- `game\Inn\RoomTemplate.rpy`: 1
- `game\Inn\Shed.rpy`: 3
- `game\Inn\SoapCraftAndAtticItems.rpy`: 14
- `game\Inn\StoryEventRuntime.rpy`: 26
- `game\Inn\TavernBedroomDoors.rpy`: 1
- `game\Inn\TavernHelp.rpy`: 1
- `game\Inn\TavernKitchen.rpy`: 19
- `game\Inn\TavernMain.rpy`: 6
- `game\Inn\TavernMyRoomAtticHatch001.rpy`: 1
- `game\Inn\TavernRooms.rpy`: 1
- `game\Inn\TavernStable.rpy`: 2
- `game\Inn\TownRooms.rpy`: 1
- `game\Inn\WerecatNPC.rpy`: 1
- `game\options.rpy`: 23
- `game\screens.rpy`: 4

## Full Alphabetical Index

| Name | Kind | Source |
| --- | --- | --- |
| `_amanda_dynamic_blocks_initialized` | `default` | `game\Inn\AmandaDynamicCommonBlocks.rpy:1` |
| `_becky_home_front_resume` | `default` | `game\Inn\BeckyHomeFront.rpy:9` |
| `_kids_functions_initialized` | `default` | `game\Inn\Intro.rpy:125` |
| `_layout_last_picture` | `default` | `game\Inn\Intro.rpy:13` |
| `_tractir_last_autosave_reason` | `default` | `game\Inn\AutosaveSupport.rpy:2` |
| `_tractir_progress_revision` | `default` | `game\Inn\AutosaveSupport.rpy:1` |
| `action_menu_actions` | `default` | `game\Inn\CharacterActionHub.rpy:8` |
| `action_menu_entity_data` | `default` | `game\Inn\CharacterActionHub.rpy:7` |
| `action_menu_entity_id` | `default` | `game\Inn\CharacterActionHub.rpy:4` |
| `action_menu_entity_type` | `default` | `game\Inn\CharacterActionHub.rpy:3` |
| `action_menu_selected` | `default` | `game\Inn\CharacterActionHub.rpy:10` |
| `action_menu_specs` | `default` | `game\Inn\CharacterActionHub.rpy:9` |
| `action_menu_title` | `default` | `game\Inn\CharacterActionHub.rpy:6` |
| `action_menu_where` | `default` | `game\Inn\CharacterActionHub.rpy:5` |
| `action_override_text` | `default` | `game\Inn\Actions.rpy:1` |
| `active_event` | `default` | `game\Inn\StoryEventRuntime.rpy:3` |
| `active_module_actor` | `default` | `game\Inn\ModuleRuntime.rpy:4` |
| `active_module_kind` | `default` | `game\Inn\ModuleRuntime.rpy:1` |
| `active_module_return_label` | `default` | `game\Inn\ModuleRuntime.rpy:2` |
| `active_module_return_room` | `default` | `game\Inn\ModuleRuntime.rpy:3` |
| `age` | `default` | `game\Inn\Intro.rpy:24` |
| `age_girls` | `default` | `game\Inn\Intro.rpy:56` |
| `AlberVar` | `default` | `game\Inn\InitSecondaryNPC.rpy:2` |
| `AllGirlNames` | `default` | `game\Inn\Intro.rpy:155` |
| `amanda` | `default` | `game\Inn\Intro.rpy:169` |
| `amanda_story_pending` | `default` | `game\Inn\StoryEventRuntime.rpy:17` |
| `AmandaDynamicNextJump` | `default` | `game\Inn\AmandaDynamicCommonBlocks.rpy:2` |
| `amandaEvents` | `default` | `game\Inn\Intro.rpy:171` |
| `AmandaGloryCurState` | `default` | `game\Inn\AmandaAtGloryHole.rpy:1` |
| `amandaThreadList` | `define` | `game\Inn\StoryEventRuntime.rpy:819` |
| `AmandaVar` | `default` | `game\Inn\Intro.rpy:170` |
| `Arousal` | `default` | `game\Inn\Intro.rpy:42` |
| `ArriveMode` | `default` | `game\Inn\BeckyHomeFront.rpy:7` |
| `ashesdirtydays` | `default` | `game\Inn\Intro.rpy:39` |
| `AskedToday` | `default` | `game\Inn\Intro.rpy:183` |
| `AtticLootFound` | `default` | `game\Inn\SoapCraftAndAtticItems.rpy:11` |
| `AtticSupplyLootFound` | `default` | `game\Inn\SoapCraftAndAtticItems.rpy:12` |
| `availEvents` | `default` | `game\Inn\StoryEventRuntime.rpy:8` |
| `BackyardToiletBusy` | `default` | `game\Inn\Backyard.rpy:151` |
| `BarberFirstTipSeen` | `default` | `game\Inn\BarberShop.rpy:2` |
| `BarberInvitePending` | `default` | `game\Inn\BarberShop.rpy:3` |
| `BarberShopSavedText` | `default` | `game\Inn\BarberShop.rpy:1` |
| `BarberVisitLastDay` | `default` | `game\Inn\BarberShop.rpy:4` |
| `beauty` | `default` | `game\Inn\Intro.rpy:58` |
| `BeckyKitchenVisitActive` | `default` | `game\Inn\TavernKitchen.rpy:7` |
| `beckyThreadList` | `define` | `game\Inn\StoryEventRuntime.rpy:883` |
| `BeckyVar` | `default` | `game\Inn\Intro.rpy:172` |
| `BedroomDoorStates` | `default` | `game\Inn\TavernBedroomDoors.rpy:1` |
| `BlessedByEllona` | `default` | `game\Inn\Intro.rpy:91` |
| `BlindPirateBreakfastPending` | `default` | `game\Inn\MarketPlace.rpy:125` |
| `BlindPirateMarketEventSeen` | `default` | `game\Inn\MarketPlace.rpy:124` |
| `BlockGloryHoleMenu` | `default` | `game\Inn\Intro.rpy:144` |
| `BlockTimeAdvance` | `default` | `game\Inn\Intro.rpy:133` |
| `BodyInteractionProfiles` | `default` | `game\Inn\BodyInteractionModel.rpy:1` |
| `bottomdress` | `default` | `game\Inn\Intro.rpy:45` |
| `bottomdressdef` | `default` | `game\Inn\Intro.rpy:192` |
| `bottomraised` | `default` | `game\Inn\Intro.rpy:51` |
| `bra` | `default` | `game\Inn\Intro.rpy:46` |
| `bradef` | `default` | `game\Inn\Intro.rpy:193` |
| `BreakfastToday` | `default` | `game\Inn\TavernKitchen.rpy:8` |
| `Breastfeed` | `default` | `game\Inn\Intro.rpy:129` |
| `build.name` | `define` | `game\options.rpy:41` |
| `cametoday` | `default` | `game\Inn\Intro.rpy:90` |
| `cametoday_npc` | `default` | `game\Inn\PregnancyCheck.rpy:8` |
| `cancumdaily` | `default` | `game\Inn\Intro.rpy:89` |
| `cancumdaily_npc` | `default` | `game\Inn\InitSecondaryNPC.rpy:11` |
| `charisma` | `default` | `game\Inn\Intro.rpy:31` |
| `CheatMoneyGrab` | `default` | `game\Inn\Intro.rpy:146` |
| `ChurchAfterCermon` | `default` | `game\Inn\Church.rpy:1` |
| `claraThreadList` | `define` | `game\Inn\StoryEventRuntime.rpy:878` |
| `ClaraVar` | `default` | `game\Inn\Intro.rpy:173` |
| `cleanincr` | `default` | `game\Inn\IncreaseSkill.rpy:3` |
| `cleaning` | `default` | `game\Inn\Intro.rpy:63` |
| `ClientsDayTotal` | `default` | `game\Inn\Intro.rpy:88` |
| `CockInGloryHole` | `default` | `game\Inn\Intro.rpy:145` |
| `CockInMouth` | `default` | `game\Inn\Intro.rpy:73` |
| `CockInPussy` | `default` | `game\Inn\Intro.rpy:74` |
| `CockInTits` | `default` | `game\Inn\Intro.rpy:75` |
| `company_list` | `default` | `game\Inn\Intro.rpy:99` |
| `ConceptionChance` | `default` | `game\Inn\PregnancyCheck.rpy:7` |
| `config.after_load_transition` | `define` | `game\options.rpy:91` |
| `config.autosave_frequency` | `define` | `game\options.rpy:53` |
| `config.autosave_on_choice` | `define` | `game\options.rpy:54` |
| `config.autosave_on_input` | `define` | `game\options.rpy:55` |
| `config.check_conflicting_properties` | `define` | `game\gui.rpy:15` |
| `config.end_game_transition` | `define` | `game\options.rpy:96` |
| `config.enter_transition` | `define` | `game\options.rpy:80` |
| `config.exit_transition` | `define` | `game\options.rpy:81` |
| `config.has_music` | `define` | `game\options.rpy:51` |
| `config.has_sound` | `define` | `game\options.rpy:50` |
| `config.has_voice` | `define` | `game\options.rpy:52` |
| `config.history_length` | `define` | `game\gui.rpy:341` |
| `config.intra_transition` | `define` | `game\options.rpy:86` |
| `config.name` | `define` | `game\options.rpy:15` |
| `config.narrator_menu` | `define` | `game\screens.rpy:310` |
| `config.nvl_list_length` | `define` | `game\screens.rpy:1524` |
| `config.save_directory` | `define` | `game\options.rpy:150` |
| `config.thumbnail_height` | `define` | `game\gui.rpy:238` |
| `config.thumbnail_width` | `define` | `game\gui.rpy:237` |
| `config.version` | `define` | `game\options.rpy:27` |
| `config.window` | `define` | `game\options.rpy:113` |
| `config.window_hide_transition` | `define` | `game\options.rpy:119` |
| `config.window_icon` | `define` | `game\options.rpy:157` |
| `config.window_show_transition` | `define` | `game\options.rpy:118` |
| `cookincr` | `default` | `game\Inn\IncreaseSkill.rpy:2` |
| `cooking` | `default` | `game\Inn\Intro.rpy:62` |
| `costumecondition` | `default` | `game\Inn\Intro.rpy:34` |
| `CumFaceOthers` | `default` | `game\Inn\Intro.rpy:80` |
| `CumFaceYou` | `default` | `game\Inn\Intro.rpy:79` |
| `cuminside` | `default` | `game\Inn\PregnancyCheck.rpy:10` |
| `CumInsideOthers` | `default` | `game\Inn\Intro.rpy:84` |
| `CumInsideYou` | `default` | `game\Inn\Intro.rpy:83` |
| `CumTitsOthers` | `default` | `game\Inn\Intro.rpy:82` |
| `CumTitsYou` | `default` | `game\Inn\Intro.rpy:81` |
| `CurDay` | `default` | `game\Inn\Intro.rpy:151` |
| `CurLoc` | `default` | `game\Inn\Intro.rpy:6` |
| `CurLocDesc` | `default` | `game\Inn\Intro.rpy:10` |
| `current_action_content` | `default` | `game\Inn\my_layouts\main_layout.rpy:3` |
| `current_action_items` | `default` | `game\Inn\my_layouts\main_layout.rpy:4` |
| `current_action_title` | `default` | `game\Inn\my_layouts\main_layout.rpy:2` |
| `current_girl_key` | `default` | `game\Inn\my_layouts\main_layout.rpy:5` |
| `current_object_id` | `default` | `game\Inn\my_layouts\main_layout.rpy:6` |
| `current_room_code` | `default` | `game\Inn\my_layouts\main_layout.rpy:7` |
| `CurrentActions` | `default` | `game\Inn\Intro.rpy:121` |
| `CurrentLoc` | `default` | `game\Inn\Intro.rpy:60` |
| `CurrentRoom` | `default` | `game\Inn\my_layouts\main_layout.rpy:1` |
| `CursedByEllona` | `default` | `game\Inn\Intro.rpy:92` |
| `CursedByEllonaDays` | `default` | `game\Inn\Intro.rpy:93` |
| `CursedByEllonaReduce` | `default` | `game\Inn\Intro.rpy:94` |
| `DailyEventsList` | `default` | `game\Inn\Intro.rpy:122` |
| `DanceSponsor` | `default` | `game\Inn\Intro.rpy:114` |
| `DanceStep` | `default` | `game\Inn\Intro.rpy:117` |
| `DanceWatchLine` | `default` | `game\Inn\Intro.rpy:115` |
| `DateOfBirth` | `default` | `game\Inn\Intro.rpy:55` |
| `day` | `default` | `game\Inn\Intro.rpy:20` |
| `dayspassed` | `default` | `game\Inn\StoryEventRuntime.rpy:1` |
| `dayssincehaircut` | `default` | `game\Inn\Intro.rpy:35` |
| `dayssincewash` | `default` | `game\Inn\Intro.rpy:38` |
| `DebugFlag` | `default` | `game\Inn\Intro.rpy:12` |
| `dog` | `default` | `game\Inn\DogCompanion.rpy:621` |
| `DraupnirVar` | `default` | `game\Inn\InitSecondaryNPC.rpy:5` |
| `DressBuyer` | `default` | `game\Inn\Intro.rpy:112` |
| `dressdefault` | `default` | `game\Inn\Intro.rpy:190` |
| `DressProduced` | `default` | `game\Inn\Intro.rpy:111` |
| `DressShopCatalogDressCode` | `default` | `game\Inn\DressShop.rpy:2` |
| `DressShopCatalogRack` | `default` | `game\Inn\DressShop.rpy:1` |
| `DressShopFemaleCatalogItemIds` | `default` | `game\Inn\DressShop.rpy:4` |
| `DressShopMaleCatalogItemIds` | `default` | `game\Inn\DressShop.rpy:3` |
| `DressShopSavedText` | `default` | `game\Inn\DressShop.rpy:5` |
| `DressTryStep` | `default` | `game\Inn\DressTry.rpy:1` |
| `Drunk` | `default` | `game\Inn\Intro.rpy:66` |
| `EddieCockInMouth` | `default` | `game\Inn\Intro.rpy:76` |
| `EddieCockInPussy` | `default` | `game\Inn\Intro.rpy:77` |
| `EddieCockInTits` | `default` | `game\Inn\Intro.rpy:78` |
| `EddieVar` | `default` | `game\Inn\InitSecondaryNPC.rpy:1` |
| `ellona_room_object_menu_object_id` | `default` | `game\Inn\EllonaTemple.rpy:121` |
| `ellona_room_object_menu_room_code` | `default` | `game\Inn\EllonaTemple.rpy:120` |
| `energy` | `default` | `game\Inn\Intro.rpy:27` |
| `EquippedArmor` | `default` | `game\Inn\Intro.rpy:98` |
| `EquippedWeapon` | `default` | `game\Inn\Intro.rpy:97` |
| `evalTime` | `default` | `game\Inn\StoryEventRuntime.rpy:9` |
| `eventItems` | `default` | `game\Inn\StoryEventRuntime.rpy:15` |
| `eventLocations` | `default` | `game\Inn\StoryEventRuntime.rpy:11` |
| `eventOptions` | `default` | `game\Inn\StoryEventRuntime.rpy:14` |
| `eventPeople` | `default` | `game\Inn\StoryEventRuntime.rpy:12` |
| `eventTalk` | `default` | `game\Inn\StoryEventRuntime.rpy:13` |
| `exploration` | `default` | `game\Inn\Intro.rpy:30` |
| `ExtraEvents` | `default` | `game\Inn\Intro.rpy:153` |
| `FightEnemyId` | `default` | `game\Inn\Intro.rpy:109` |
| `FightEnemyParty` | `default` | `game\Inn\Intro.rpy:108` |
| `FightEnemyState` | `default` | `game\Inn\Intro.rpy:104` |
| `FightLevel` | `default` | `game\Inn\Intro.rpy:187` |
| `FightLoadedAmmo` | `default` | `game\Inn\FightSystemRuntime.rpy:1` |
| `FightRetreatUsed` | `default` | `game\Inn\Intro.rpy:102` |
| `FightSideLog` | `default` | `game\Inn\Intro.rpy:107` |
| `FightTargetIndex` | `default` | `game\Inn\FightSystemRuntime.rpy:2` |
| `FightWeaponLoaded` | `default` | `game\Inn\Intro.rpy:101` |
| `fire_state` | `default` | `game\Inn\TavernKitchen.rpy:1` |
| `FlirtedToday` | `default` | `game\Inn\Intro.rpy:181` |
| `ForestReturnTarget` | `default` | `game\Inn\Forest.rpy:211` |
| `ForestSavedText` | `default` | `game\Inn\Forest.rpy:210` |
| `ForestSubroomSavedText` | `default` | `game\Inn\Forest.rpy:212` |
| `FranBusy` | `default` | `game\Inn\InitSecondaryNPC.rpy:4` |
| `FranVar` | `default` | `game\Inn\InitSecondaryNPC.rpy:3` |
| `FridayDancesCount` | `default` | `game\Inn\Intro.rpy:113` |
| `Friends` | `default` | `game\Inn\Intro.rpy:179` |
| `fun` | `default` | `game\Inn\Intro.rpy:26` |
| `game_item_registry` | `define` | `game\Inn\GameItems.rpy:3` |
| `game_items` | `define` | `game\Inn\GameItems.rpy:2` |
| `GeorgettAvail` | `default` | `game\Inn\TavernMain.rpy:4` |
| `georgettThreadList` | `define` | `game\Inn\StoryEventRuntime.rpy:885` |
| `GeorgettVar` | `default` | `game\Inn\Intro.rpy:174` |
| `GiftedToday` | `default` | `game\Inn\Intro.rpy:182` |
| `GiftPreferences` | `default` | `game\Inn\Intro.rpy:184` |
| `GirlDance` | `default` | `game\Inn\Intro.rpy:116` |
| `girltextdesc` | `default` | `game\Inn\Intro.rpy:61` |
| `GloryHoleCurrentStep` | `default` | `game\Inn\Intro.rpy:143` |
| `GloryHoleLook` | `default` | `game\Inn\Intro.rpy:142` |
| `GraphicsOn` | `default` | `game\Inn\Intro.rpy:14` |
| `GrupenSex` | `default` | `game\Inn\Intro.rpy:70` |
| `gui.about` | `define` | `game\options.rpy:33` |
| `gui.accent_color` | `define` | `game\gui.rpy:28` |
| `gui.bar_borders` | `define` | `game\gui.rpy:322` |
| `gui.bar_size` | `define` | `game\gui.rpy:312` |
| `gui.bar_tile` | `define` | `game\gui.rpy:317` |
| `gui.button_borders` | `define` | `game\gui.rpy:154` |
| `gui.button_height` | `define` | `game\gui.rpy:151` |
| `gui.button_text_font` | `define` | `game\gui.rpy:161` |
| `gui.button_text_hover_color` | `define` | `game\gui.rpy:168` |
| `gui.button_text_idle_color` | `define` | `game\gui.rpy:167` |
| `gui.button_text_insensitive_color` | `define` | `game\gui.rpy:170` |
| `gui.button_text_selected_color` | `define` | `game\gui.rpy:169` |
| `gui.button_text_size` | `define` | `game\gui.rpy:164` |
| `gui.button_text_xalign` | `define` | `game\gui.rpy:174` |
| `gui.button_tile` | `define` | `game\gui.rpy:158` |
| `gui.button_width` | `define` | `game\gui.rpy:150` |
| `gui.check_button_borders` | `define` | `game\gui.rpy:185` |
| `gui.choice_button_borders` | `define` | `game\gui.rpy:210` |
| `gui.choice_button_height` | `define` | `game\gui.rpy:208` |
| `gui.choice_button_text_font` | `define` | `game\gui.rpy:211` |
| `gui.choice_button_text_hover_color` | `define` | `game\gui.rpy:215` |
| `gui.choice_button_text_idle_color` | `define` | `game\gui.rpy:214` |
| `gui.choice_button_text_insensitive_color` | `define` | `game\gui.rpy:216` |
| `gui.choice_button_text_size` | `define` | `game\gui.rpy:212` |
| `gui.choice_button_text_xalign` | `define` | `game\gui.rpy:213` |
| `gui.choice_button_tile` | `define` | `game\gui.rpy:209` |
| `gui.choice_button_width` | `define` | `game\gui.rpy:207` |
| `gui.choice_spacing` | `define` | `game\gui.rpy:261` |
| `gui.confirm_button_text_xalign` | `define` | `game\gui.rpy:187` |
| `gui.confirm_frame_borders` | `define` | `game\gui.rpy:291` |
| `gui.dialogue_text_xalign` | `define` | `game\gui.rpy:141` |
| `gui.dialogue_width` | `define` | `game\gui.rpy:137` |
| `gui.dialogue_xpos` | `define` | `game\gui.rpy:133` |
| `gui.dialogue_ypos` | `define` | `game\gui.rpy:134` |
| `gui.file_slot_cols` | `define` | `game\gui.rpy:241` |
| `gui.file_slot_rows` | `define` | `game\gui.rpy:242` |
| `gui.frame_borders` | `define` | `game\gui.rpy:288` |
| `gui.frame_tile` | `define` | `game\gui.rpy:300` |
| `gui.game_menu_background` | `define` | `game\gui.rpy:91` |
| `gui.history_allow_tags` | `define` | `game\screens.rpy:1103` |
| `gui.history_height` | `define` | `game\gui.rpy:345` |
| `gui.history_name_width` | `define` | `game\gui.rpy:354` |
| `gui.history_name_xalign` | `define` | `game\gui.rpy:355` |
| `gui.history_name_xpos` | `define` | `game\gui.rpy:352` |
| `gui.history_name_ypos` | `define` | `game\gui.rpy:353` |
| `gui.history_spacing` | `define` | `game\gui.rpy:348` |
| `gui.history_text_width` | `define` | `game\gui.rpy:360` |
| `gui.history_text_xalign` | `define` | `game\gui.rpy:361` |
| `gui.history_text_xpos` | `define` | `game\gui.rpy:358` |
| `gui.history_text_ypos` | `define` | `game\gui.rpy:359` |
| `gui.hover_color` | `define` | `game\gui.rpy:38` |
| `gui.hover_muted_color` | `define` | `game\gui.rpy:50` |
| `gui.idle_color` | `define` | `game\gui.rpy:31` |
| `gui.idle_small_color` | `define` | `game\gui.rpy:35` |
| `gui.insensitive_color` | `define` | `game\gui.rpy:45` |
| `gui.interface_text_color` | `define` | `game\gui.rpy:54` |
| `gui.interface_text_font` | `define` | `game\gui.rpy:66` |
| `gui.interface_text_size` | `define` | `game\gui.rpy:75` |
| `gui.label_text_size` | `define` | `game\gui.rpy:78` |
| `gui.language` | `define` | `game\gui.rpy:414` |
| `gui.main_menu_background` | `define` | `game\gui.rpy:90` |
| `gui.main_menu_text_xalign` | `define` | `game\gui.rpy:279` |
| `gui.muted_color` | `define` | `game\gui.rpy:49` |
| `gui.name_text_font` | `define` | `game\gui.rpy:63` |
| `gui.name_text_size` | `define` | `game\gui.rpy:72` |
| `gui.name_xalign` | `define` | `game\gui.rpy:114` |
| `gui.name_xpos` | `define` | `game\gui.rpy:109` |
| `gui.name_ypos` | `define` | `game\gui.rpy:110` |
| `gui.namebox_borders` | `define` | `game\gui.rpy:123` |
| `gui.namebox_height` | `define` | `game\gui.rpy:119` |
| `gui.namebox_tile` | `define` | `game\gui.rpy:127` |
| `gui.namebox_width` | `define` | `game\gui.rpy:118` |
| `gui.navigation_spacing` | `define` | `game\gui.rpy:264` |
| `gui.navigation_xpos` | `define` | `game\gui.rpy:252` |
| `gui.notify_frame_borders` | `define` | `game\gui.rpy:297` |
| `gui.notify_text_size` | `define` | `game\gui.rpy:81` |
| `gui.notify_ypos` | `define` | `game\gui.rpy:258` |
| `gui.nvl_borders` | `define` | `game\gui.rpy:369` |
| `gui.nvl_button_xalign` | `define` | `game\gui.rpy:405` |
| `gui.nvl_button_xpos` | `define` | `game\gui.rpy:404` |
| `gui.nvl_height` | `define` | `game\gui.rpy:377` |
| `gui.nvl_list_length` | `define` | `game\gui.rpy:373` |
| `gui.nvl_name_width` | `define` | `game\gui.rpy:387` |
| `gui.nvl_name_xalign` | `define` | `game\gui.rpy:388` |
| `gui.nvl_name_xpos` | `define` | `game\gui.rpy:385` |
| `gui.nvl_name_ypos` | `define` | `game\gui.rpy:386` |
| `gui.nvl_spacing` | `define` | `game\gui.rpy:381` |
| `gui.nvl_text_width` | `define` | `game\gui.rpy:393` |
| `gui.nvl_text_xalign` | `define` | `game\gui.rpy:394` |
| `gui.nvl_text_xpos` | `define` | `game\gui.rpy:391` |
| `gui.nvl_text_ypos` | `define` | `game\gui.rpy:392` |
| `gui.nvl_thought_width` | `define` | `game\gui.rpy:400` |
| `gui.nvl_thought_xalign` | `define` | `game\gui.rpy:401` |
| `gui.nvl_thought_xpos` | `define` | `game\gui.rpy:398` |
| `gui.nvl_thought_ypos` | `define` | `game\gui.rpy:399` |
| `gui.page_button_borders` | `define` | `game\gui.rpy:189` |
| `gui.page_spacing` | `define` | `game\gui.rpy:273` |
| `gui.pref_button_spacing` | `define` | `game\gui.rpy:270` |
| `gui.pref_spacing` | `define` | `game\gui.rpy:267` |
| `gui.quick_button_borders` | `define` | `game\gui.rpy:191` |
| `gui.quick_button_text_idle_color` | `define` | `game\gui.rpy:193` |
| `gui.quick_button_text_selected_color` | `define` | `game\gui.rpy:194` |
| `gui.quick_button_text_size` | `define` | `game\gui.rpy:192` |
| `gui.radio_button_borders` | `define` | `game\gui.rpy:183` |
| `gui.scrollbar_borders` | `define` | `game\gui.rpy:323` |
| `gui.scrollbar_size` | `define` | `game\gui.rpy:313` |
| `gui.scrollbar_tile` | `define` | `game\gui.rpy:318` |
| `gui.selected_color` | `define` | `game\gui.rpy:42` |
| `gui.show_name` | `define` | `game\options.rpy:22` |
| `gui.skip_frame_borders` | `define` | `game\gui.rpy:294` |
| `gui.skip_ypos` | `define` | `game\gui.rpy:255` |
| `gui.slider_borders` | `define` | `game\gui.rpy:324` |
| `gui.slider_size` | `define` | `game\gui.rpy:314` |
| `gui.slider_tile` | `define` | `game\gui.rpy:319` |
| `gui.slot_button_borders` | `define` | `game\gui.rpy:228` |
| `gui.slot_button_height` | `define` | `game\gui.rpy:227` |
| `gui.slot_button_text_idle_color` | `define` | `game\gui.rpy:232` |
| `gui.slot_button_text_selected_hover_color` | `define` | `game\gui.rpy:234` |
| `gui.slot_button_text_selected_idle_color` | `define` | `game\gui.rpy:233` |
| `gui.slot_button_text_size` | `define` | `game\gui.rpy:229` |
| `gui.slot_button_text_xalign` | `define` | `game\gui.rpy:231` |
| `gui.slot_button_width` | `define` | `game\gui.rpy:226` |
| `gui.slot_spacing` | `define` | `game\gui.rpy:276` |
| `gui.status_button_text_size` | `define` | `game\gui.rpy:230` |
| `gui.text_color` | `define` | `game\gui.rpy:53` |
| `gui.text_font` | `define` | `game\gui.rpy:60` |
| `gui.text_size` | `define` | `game\gui.rpy:69` |
| `gui.textbox_height` | `define` | `game\gui.rpy:100` |
| `gui.textbox_yalign` | `define` | `game\gui.rpy:104` |
| `gui.title_text_size` | `define` | `game\gui.rpy:84` |
| `gui.unscrollable` | `define` | `game\gui.rpy:333` |
| `gui.vbar_borders` | `define` | `game\gui.rpy:327` |
| `gui.vscrollbar_borders` | `define` | `game\gui.rpy:328` |
| `gui.vslider_borders` | `define` | `game\gui.rpy:329` |
| `HadSex` | `default` | `game\Inn\Intro.rpy:43` |
| `HandsDance` | `default` | `game\Inn\Intro.rpy:118` |
| `HarassInstructions` | `default` | `game\Inn\Intro.rpy:188` |
| `health` | `default` | `game\Inn\Intro.rpy:28` |
| `HorsePurchasePrice` | `default` | `game\Inn\TavernStable.rpy:2` |
| `HorseSaddled` | `default` | `game\Inn\TavernStable.rpy:1` |
| `hot_water_state` | `default` | `game\Inn\TavernKitchen.rpy:2` |
| `hour` | `default` | `game\Inn\Intro.rpy:18` |
| `HouseholdBarberRequestLastDay` | `default` | `game\Inn\HouseholdRuntimeEvents.rpy:4` |
| `HouseholdInsightState` | `default` | `game\Inn\HouseholdRuntimeEvents.rpy:2` |
| `householdmembers` | `default` | `game\Inn\Intro.rpy:134` |
| `HouseholdMorningState` | `default` | `game\Inn\menu_tavernstat.rpy:1` |
| `HouseholdRuntimeEventSeen` | `default` | `game\Inn\HouseholdRuntimeEvents.rpy:1` |
| `HouseholdSoapLastBatchProfile` | `default` | `game\Inn\SoapCraftAndAtticItems.rpy:10` |
| `HouseholdSoapRequestLastDay` | `default` | `game\Inn\HouseholdRuntimeEvents.rpy:3` |
| `HouseholdSoapSampleGiven` | `default` | `game\Inn\SoapCraftAndAtticItems.rpy:9` |
| `HouseholdSoapSampleIntroDone` | `default` | `game\Inn\SoapCraftAndAtticItems.rpy:8` |
| `HouseholdWarmDrinkLastDay` | `default` | `game\Inn\HouseholdRuntimeEvents.rpy:5` |
| `HunterClubTradeMode` | `default` | `game\Inn\HunterClub.rpy:350` |
| `HunterClubTradeSelection` | `default` | `game\Inn\HunterClub.rpy:351` |
| `HuntLastResult` | `default` | `game\Inn\Intro.rpy:106` |
| `HuntUnlocked` | `default` | `game\Inn\Intro.rpy:105` |
| `IngaVar` | `default` | `game\Inn\BeckyHomeFront.rpy:10` |
| `IrmaVar` | `default` | `game\Inn\Intro.rpy:178` |
| `item_catalog` | `define` | `game\Inn\GameItems.rpy:1` |
| `jobcleaning` | `default` | `game\Inn\Intro.rpy:199` |
| `jobcleaningtomorrow` | `default` | `game\Inn\Intro.rpy:202` |
| `jobgloryhole` | `default` | `game\Inn\Intro.rpy:207` |
| `jobGloryHoleAvail` | `default` | `game\Inn\Intro.rpy:205` |
| `jobgloryholeTommorow` | `default` | `game\Inn\Intro.rpy:209` |
| `jobHallAvail` | `default` | `game\Inn\Intro.rpy:197` |
| `jobkitchen` | `default` | `game\Inn\Intro.rpy:198` |
| `jobkitchentomorrow` | `default` | `game\Inn\Intro.rpy:201` |
| `jobwaitress` | `default` | `game\Inn\Intro.rpy:200` |
| `jobwaitresstomorrow` | `default` | `game\Inn\Intro.rpy:203` |
| `jobwhore` | `default` | `game\Inn\Intro.rpy:206` |
| `jobWhoreAvail` | `default` | `game\Inn\Intro.rpy:204` |
| `jobwhoreTommorow` | `default` | `game\Inn\Intro.rpy:208` |
| `KidBirthPosobie` | `default` | `game\Inn\Intro.rpy:127` |
| `kids` | `default` | `game\Inn\Intro.rpy:57` |
| `KidsList` | `default` | `game\Inn\Intro.rpy:123` |
| `KidsListNextId` | `default` | `game\Inn\Intro.rpy:124` |
| `KidsPosobie` | `default` | `game\Inn\Intro.rpy:126` |
| `KissDance` | `default` | `game\Inn\Intro.rpy:119` |
| `KitchenFoodEffects` | `default` | `game\Inn\TavernKitchen.rpy:19` |
| `KitchenWildFoodStock` | `default` | `game\Inn\TavernKitchen.rpy:18` |
| `KnowMongol` | `default` | `game\Inn\InitSecondaryNPC.rpy:12` |
| `knowsMC` | `default` | `game\Inn\CharacterActionHub.rpy:1` |
| `Lactate` | `default` | `game\Inn\Intro.rpy:130` |
| `legs` | `default` | `game\Inn\Intro.rpy:48` |
| `legsdef` | `default` | `game\Inn\Intro.rpy:195` |
| `LickPussy` | `default` | `game\Inn\Intro.rpy:67` |
| `LizaAvail` | `default` | `game\Inn\TavernMain.rpy:5` |
| `lizaThreadList` | `define` | `game\Inn\StoryEventRuntime.rpy:884` |
| `LizaVar` | `default` | `game\Inn\Intro.rpy:175` |
| `location` | `default` | `game\Inn\Intro.rpy:7` |
| `look` | `default` | `game\Inn\Intro.rpy:33` |
| `main_ui_inventory_dropdown_open` | `default` | `game\Inn\my_layouts\main_layout.rpy:11` |
| `MainTxt` | `default` | `game\Inn\Intro.rpy:9` |
| `MaxCounterToClean` | `default` | `game\Inn\Intro.rpy:11` |
| `melissaThreadList` | `define` | `game\Inn\StoryEventRuntime.rpy:837` |
| `MelissaVar` | `default` | `game\Inn\Intro.rpy:177` |
| `menDress` | `define` | `game\Inn\GameItems.rpy:4` |
| `minute` | `default` | `game\Inn\Intro.rpy:19` |
| `money` | `default` | `game\Inn\Intro.rpy:25` |
| `MongolVar` | `default` | `game\Inn\InitSecondaryNPC.rpy:6` |
| `month` | `default` | `game\Inn\Intro.rpy:21` |
| `MyCurDress` | `default` | `game\Inn\Intro.rpy:96` |
| `MyDresses` | `default` | `game\Inn\Intro.rpy:95` |
| `NAVIGATION_ONLY_MODE` | `default` | `game\Inn\NavigationOnlyMode.rpy:1` |
| `neshlush` | `default` | `game\Inn\Intro.rpy:186` |
| `NextDayReportBody` | `default` | `game\Inn\NextDay.rpy:3` |
| `NextDayReportTitle` | `default` | `game\Inn\NextDay.rpy:2` |
| `notoriety` | `default` | `game\Inn\Intro.rpy:29` |
| `NPCSchedules` | `default` | `game\Inn\NPCScheduleModel.rpy:1` |
| `ONGLOAD` | `default` | `game\Inn\Intro.rpy:2` |
| `ONGSAVE` | `default` | `game\Inn\Intro.rpy:3` |
| `ONNEWLOC` | `default` | `game\Inn\Intro.rpy:4` |
| `otkroven` | `default` | `game\Inn\Intro.rpy:185` |
| `panel_paged_next_items` | `default` | `game\Inn\PartEventYourFirstReaction.rpy:10` |
| `panel_paged_next_title` | `default` | `game\Inn\PartEventYourFirstReaction.rpy:9` |
| `panel_paged_page_index` | `default` | `game\Inn\PartEventYourFirstReaction.rpy:8` |
| `panel_paged_pages` | `default` | `game\Inn\PartEventYourFirstReaction.rpy:7` |
| `panel_paged_pending_items` | `default` | `game\Inn\PartEventYourFirstReaction.rpy:14` |
| `panel_paged_pending_style` | `default` | `game\Inn\PartEventYourFirstReaction.rpy:15` |
| `panel_paged_pending_text` | `default` | `game\Inn\PartEventYourFirstReaction.rpy:12` |
| `panel_paged_pending_title` | `default` | `game\Inn\PartEventYourFirstReaction.rpy:13` |
| `panel_paged_raw_text` | `default` | `game\Inn\PartEventYourFirstReaction.rpy:6` |
| `panel_paged_style` | `default` | `game\Inn\PartEventYourFirstReaction.rpy:11` |
| `panties` | `default` | `game\Inn\Intro.rpy:47` |
| `pantiesdef` | `default` | `game\Inn\Intro.rpy:194` |
| `player_card_inventory_origin` | `default` | `game\Inn\PlayerCard.rpy:4` |
| `player_company` | `default` | `game\Inn\DogCompanion.rpy:1` |
| `player_inventory_view_item` | `default` | `game\Inn\PlayerCard.rpy:3` |
| `player_inventory_view_mode` | `default` | `game\Inn\PlayerCard.rpy:1` |
| `player_inventory_view_section` | `default` | `game\Inn\PlayerCard.rpy:2` |
| `PlayerChoresWeek` | `default` | `game\Inn\Intro.rpy:147` |
| `PlayerDressDaySt` | `default` | `game\Inn\Intro.rpy:37` |
| `PlayerFightSupply` | `default` | `game\Inn\Intro.rpy:100` |
| `PlayerHaircutDaySt` | `default` | `game\Inn\Intro.rpy:36` |
| `playerItems` | `default` | `game\Inn\Intro.rpy:110` |
| `PortStreetsBottlePresent` | `default` | `game\Inn\PortStreets.rpy:3` |
| `PortStreetsBottleSpawnDay` | `default` | `game\Inn\PortStreets.rpy:2` |
| `preferences.afm_time` | `default` | `game\options.rpy:133` |
| `preferences.text_cps` | `default` | `game\options.rpy:127` |
| `pregfather` | `default` | `game\Inn\Intro.rpy:59` |
| `pregnancy` | `default` | `game\Inn\Intro.rpy:68` |
| `PregTotalSuspects` | `default` | `game\Inn\Intro.rpy:131` |
| `PrevLoc` | `default` | `game\Inn\Intro.rpy:8` |
| `PriestIncestAgree` | `default` | `game\Inn\Church.rpy:2` |
| `productnum` | `default` | `game\Inn\Intro.rpy:136` |
| `ProstitutesKids` | `default` | `game\Inn\Intro.rpy:128` |
| `PussyVisible` | `default` | `game\Inn\Intro.rpy:71` |
| `PussyWetStart` | `default` | `game\Inn\Intro.rpy:65` |
| `quick_menu` | `define` | `game\screens.rpy:370` |
| `RandIngaFuck` | `default` | `game\Inn\BeckyHomeFront.rpy:8` |
| `random_events` | `default` | `game\Inn\StoryEventRuntime.rpy:4` |
| `RealName` | `default` | `game\Inn\Intro.rpy:52` |
| `RealName2` | `default` | `game\Inn\Intro.rpy:53` |
| `RealName3` | `default` | `game\Inn\Intro.rpy:54` |
| `rebellion` | `default` | `game\Inn\Intro.rpy:32` |
| `recipe_names` | `define` | `game\Inn\CraftingRecipes.rpy:1` |
| `recipe_pages` | `define` | `game\Inn\CraftingRecipes.rpy:2` |
| `RecipeBookReturnObjectId` | `default` | `game\Inn\CraftingRecipes.rpy:5` |
| `RecipeBookReturnPicture` | `default` | `game\Inn\CraftingRecipes.rpy:6` |
| `RecipeBookReturnRoomCode` | `default` | `game\Inn\CraftingRecipes.rpy:4` |
| `RecipeBookSelectedId` | `default` | `game\Inn\CraftingRecipes.rpy:3` |
| `RelationshipLevels` | `default` | `game\Inn\NPCRelationshipLevels.rpy:1` |
| `Result` | `default` | `game\Inn\PartEventGirlReactionTalk.rpy:1` |
| `RobbersHeadNameTmp` | `default` | `game\Inn\InitSecondaryNPC.rpy:9` |
| `RobinVar` | `default` | `game\Inn\InitSecondaryNPC.rpy:8` |
| `roomFirstVisit` | `default` | `game\Inn\RoomTemplate.rpy:1` |
| `RustyHunterRifleLoadedAmmo` | `default` | `game\Inn\SoapCraftAndAtticItems.rpy:14` |
| `sandraThreadList` | `define` | `game\Inn\StoryEventRuntime.rpy:868` |
| `SandraVar` | `default` | `game\Inn\Intro.rpy:176` |
| `scene_image` | `default` | `game\Inn\my_layouts\main_layout.rpy:8` |
| `sceneFullScreen` | `default` | `game\01vscene.rpy:24` |
| `sceneMovie` | `default` | `game\01vscene.rpy:23` |
| `sex_history_by_girl` | `default` | `game\Inn\Intro.rpy:86` |
| `sex_history_next_id` | `default` | `game\Inn\Intro.rpy:87` |
| `sexacts` | `default` | `game\Inn\PregnancyCheck.rpy:6` |
| `ShedBucketFound` | `default` | `game\Inn\Shed.rpy:3` |
| `ShedNoticePending` | `default` | `game\Inn\Shed.rpy:2` |
| `ShedNoticeText` | `default` | `game\Inn\Shed.rpy:1` |
| `shoes` | `default` | `game\Inn\Intro.rpy:49` |
| `shoesdef` | `default` | `game\Inn\Intro.rpy:196` |
| `ShortSkirtNoPanties` | `default` | `game\Inn\Intro.rpy:72` |
| `SickDays` | `default` | `game\Inn\Intro.rpy:103` |
| `SloganFixed` | `default` | `game\Inn\Intro.rpy:139` |
| `sluttiness` | `default` | `game\Inn\PregnancyCheck.rpy:9` |
| `SoapAshBarrelInstalled` | `default` | `game\Inn\SoapCraftAndAtticItems.rpy:2` |
| `SoapAshBarrelReadyDay` | `default` | `game\Inn\SoapCraftAndAtticItems.rpy:3` |
| `SoapExpireDay` | `default` | `game\Inn\SoapCraftAndAtticItems.rpy:1` |
| `SoapLookBonusUntilDay` | `default` | `game\Inn\SoapCraftAndAtticItems.rpy:6` |
| `SoapPendingBatches` | `default` | `game\Inn\SoapCraftAndAtticItems.rpy:4` |
| `SoapRequestQueue` | `default` | `game\Inn\SoapCraftAndAtticItems.rpy:7` |
| `SoapStoredBatches` | `default` | `game\Inn\SoapCraftAndAtticItems.rpy:5` |
| `StolenHorseDays` | `default` | `game\Inn\InitSecondaryNPC.rpy:13` |
| `story_events` | `default` | `game\Inn\StoryEventRuntime.rpy:5` |
| `story_thread_levels` | `default` | `game\Inn\StoryEventRuntime.rpy:16` |
| `Talked` | `default` | `game\Inn\InitSecondaryNPC.rpy:10` |
| `TalkedToday` | `default` | `game\Inn\Intro.rpy:180` |
| `tavern_event_next_items` | `default` | `game\Inn\PartEventYourFirstReaction.rpy:5` |
| `tavern_event_next_title` | `default` | `game\Inn\PartEventYourFirstReaction.rpy:4` |
| `tavern_event_page_index` | `default` | `game\Inn\PartEventYourFirstReaction.rpy:3` |
| `tavern_event_pages` | `default` | `game\Inn\PartEventYourFirstReaction.rpy:2` |
| `tavern_event_panel_raw_text` | `default` | `game\Inn\PartEventYourFirstReaction.rpy:1` |
| `tavern_work_events` | `default` | `game\Inn\StoryEventRuntime.rpy:6` |
| `TavernBreakfastBarberTalkDay` | `default` | `game\Inn\TavernKitchen.rpy:12` |
| `TavernBreakfastDay` | `default` | `game\Inn\TavernKitchen.rpy:10` |
| `TavernBreakfastEventActive` | `default` | `game\Inn\TavernKitchen.rpy:13` |
| `TavernBreakfastGeorgetteLizaPending` | `default` | `game\Inn\TavernKitchen.rpy:20` |
| `TavernBreakfastLastDay` | `default` | `game\Inn\TavernKitchen.rpy:9` |
| `TavernBreakfastSoapAnnouncedDay` | `default` | `game\Inn\TavernKitchen.rpy:11` |
| `TavernBreakfastSpicyDrinkDay` | `default` | `game\Inn\TavernKitchen.rpy:16` |
| `taverncleanliness` | `default` | `game\Inn\Intro.rpy:41` |
| `TavernClosed` | `default` | `game\Inn\TavernMain.rpy:1` |
| `TavernEventOngoing` | `default` | `game\Inn\TavernMain.rpy:3` |
| `tavernfame` | `default` | `game\Inn\Intro.rpy:138` |
| `TavernGloryHole` | `default` | `game\Inn\Intro.rpy:141` |
| `TavernHelpPage` | `default` | `game\Inn\TavernHelp.rpy:40` |
| `TavernHole` | `default` | `game\Inn\Intro.rpy:140` |
| `TavernKitchenNoticePending` | `default` | `game\Inn\TavernKitchen.rpy:5` |
| `TavernKitchenNoticeText` | `default` | `game\Inn\TavernKitchen.rpy:4` |
| `TavernKitchenSavedText` | `default` | `game\Inn\TavernKitchen.rpy:6` |
| `TavernMainBlockEvents` | `default` | `game\Inn\TavernMain.rpy:171` |
| `TavernMainObjectMenuId` | `default` | `game\Inn\TavernMain.rpy:172` |
| `TavernMyRoomAtticHatchFound` | `default` | `game\Inn\TavernMyRoomAtticHatch001.rpy:1` |
| `TavernReportSelectedPerson` | `default` | `game\Inn\menu_tavernstat.rpy:764` |
| `TavernRooms` | `default` | `game\Inn\TavernRooms.rpy:1` |
| `TavernSundayDinnerBarberTalkDay` | `default` | `game\Inn\TavernKitchen.rpy:15` |
| `TavernSundayDinnerLastDay` | `default` | `game\Inn\TavernKitchen.rpy:14` |
| `TavernSundayDinnerSpicyDrinkDay` | `default` | `game\Inn\TavernKitchen.rpy:17` |
| `tavernvisitors` | `default` | `game\Inn\Intro.rpy:135` |
| `thread` | `default` | `game\Inn\StoryEventRuntime.rpy:10` |
| `threadData` | `define` | `game\Inn\StoryEventRuntime.rpy:907` |
| `threadList` | `define` | `game\Inn\StoryEventRuntime.rpy:897` |
| `threadListsByGirl` | `define` | `game\Inn\StoryEventRuntime.rpy:887` |
| `threads` | `default` | `game\Inn\StoryEventRuntime.rpy:908` |
| `time` | `default` | `game\Inn\Intro.rpy:17` |
| `TitsDance` | `default` | `game\Inn\Intro.rpy:120` |
| `TitsVisible` | `default` | `game\Inn\Intro.rpy:69` |
| `TodaySexEvents` | `default` | `game\Inn\Intro.rpy:85` |
| `topdress` | `default` | `game\Inn\Intro.rpy:44` |
| `topdressdef` | `default` | `game\Inn\Intro.rpy:191` |
| `topraised` | `default` | `game\Inn\Intro.rpy:50` |
| `TotalDay` | `default` | `game\Inn\Intro.rpy:152` |
| `TownRooms` | `default` | `game\Inn\TownRooms.rpy:1` |
| `UI_chores` | `default` | `game\Inn\Intro.rpy:148` |
| `UI_mode` | `default` | `game\Inn\my_layouts\main_layout.rpy:9` |
| `UI_selected_char` | `default` | `game\Inn\my_layouts\main_layout.rpy:10` |
| `upstairsroomsdirty` | `default` | `game\Inn\Intro.rpy:40` |
| `UpstairsRoomSearchState` | `default` | `game\Inn\SoapCraftAndAtticItems.rpy:13` |
| `ViewIngaSex` | `default` | `game\Inn\BeckyHomeFront.rpy:6` |
| `virginity` | `default` | `game\Inn\Intro.rpy:64` |
| `waitress` | `default` | `game\Inn\Intro.rpy:189` |
| `waitressincr` | `default` | `game\Inn\IncreaseSkill.rpy:4` |
| `week` | `default` | `game\Inn\Intro.rpy:22` |
| `WeeklyChoresLastEvalStamp` | `default` | `game\Inn\Intro.rpy:150` |
| `WeeklyVisitorsTrack` | `default` | `game\Inn\Intro.rpy:149` |
| `WerecatNPCState` | `default` | `game\Inn\WerecatNPC.rpy:1` |
| `WerecatVar` | `default` | `game\Inn\MelissaWerecatQuest.rpy:1` |
| `winenum` | `default` | `game\Inn\Intro.rpy:137` |
| `womenDress` | `define` | `game\Inn\GameItems.rpy:5` |
| `year` | `default` | `game\Inn\Intro.rpy:23` |
| `ZaletSuspectFinal` | `default` | `game\Inn\Intro.rpy:132` |
| `ZimmerVar` | `default` | `game\Inn\InitSecondaryNPC.rpy:7` |

## Raw Declaration Appendix

| Kind | Name | File | Line | Raw |
| --- | --- | --- | --- | --- |
| `default` | `sceneMovie` | `game\01vscene.rpy` | `23` | `default sceneMovie = False` |
| `default` | `sceneFullScreen` | `game\01vscene.rpy` | `24` | `default sceneFullScreen = False` |
| `define` | `config.check_conflicting_properties` | `game\gui.rpy` | `15` | `define config.check_conflicting_properties = True` |
| `define` | `gui.accent_color` | `game\gui.rpy` | `28` | `define gui.accent_color = '#99ccff'` |
| `define` | `gui.idle_color` | `game\gui.rpy` | `31` | `define gui.idle_color = '#888888'` |
| `define` | `gui.idle_small_color` | `game\gui.rpy` | `35` | `define gui.idle_small_color = '#aaaaaa'` |
| `define` | `gui.hover_color` | `game\gui.rpy` | `38` | `define gui.hover_color = '#c1e0ff'` |
| `define` | `gui.selected_color` | `game\gui.rpy` | `42` | `define gui.selected_color = '#ffffff'` |
| `define` | `gui.insensitive_color` | `game\gui.rpy` | `45` | `define gui.insensitive_color = '#8888887f'` |
| `define` | `gui.muted_color` | `game\gui.rpy` | `49` | `define gui.muted_color = '#3d5166'` |
| `define` | `gui.hover_muted_color` | `game\gui.rpy` | `50` | `define gui.hover_muted_color = '#5b7a99'` |
| `define` | `gui.text_color` | `game\gui.rpy` | `53` | `define gui.text_color = '#ffffff'` |
| `define` | `gui.interface_text_color` | `game\gui.rpy` | `54` | `define gui.interface_text_color = '#ffffff'` |
| `define` | `gui.text_font` | `game\gui.rpy` | `60` | `define gui.text_font = "DejaVuSans.ttf"` |
| `define` | `gui.name_text_font` | `game\gui.rpy` | `63` | `define gui.name_text_font = "DejaVuSans.ttf"` |
| `define` | `gui.interface_text_font` | `game\gui.rpy` | `66` | `define gui.interface_text_font = "DejaVuSans.ttf"` |
| `define` | `gui.text_size` | `game\gui.rpy` | `69` | `define gui.text_size = 33` |
| `define` | `gui.name_text_size` | `game\gui.rpy` | `72` | `define gui.name_text_size = 45` |
| `define` | `gui.interface_text_size` | `game\gui.rpy` | `75` | `define gui.interface_text_size = 33` |
| `define` | `gui.label_text_size` | `game\gui.rpy` | `78` | `define gui.label_text_size = 36` |
| `define` | `gui.notify_text_size` | `game\gui.rpy` | `81` | `define gui.notify_text_size = 24` |
| `define` | `gui.title_text_size` | `game\gui.rpy` | `84` | `define gui.title_text_size = 75` |
| `define` | `gui.main_menu_background` | `game\gui.rpy` | `90` | `define gui.main_menu_background = "gui/main_menu.png"` |
| `define` | `gui.game_menu_background` | `game\gui.rpy` | `91` | `define gui.game_menu_background = "gui/game_menu.png"` |
| `define` | `gui.textbox_height` | `game\gui.rpy` | `100` | `define gui.textbox_height = 270` |
| `define` | `gui.textbox_yalign` | `game\gui.rpy` | `104` | `define gui.textbox_yalign = 1.0` |
| `define` | `gui.name_xpos` | `game\gui.rpy` | `109` | `define gui.name_xpos = 360` |
| `define` | `gui.name_ypos` | `game\gui.rpy` | `110` | `define gui.name_ypos = 0` |
| `define` | `gui.name_xalign` | `game\gui.rpy` | `114` | `define gui.name_xalign = 0.0` |
| `define` | `gui.namebox_width` | `game\gui.rpy` | `118` | `define gui.namebox_width = None` |
| `define` | `gui.namebox_height` | `game\gui.rpy` | `119` | `define gui.namebox_height = None` |
| `define` | `gui.namebox_borders` | `game\gui.rpy` | `123` | `define gui.namebox_borders = Borders(5, 5, 5, 5)` |
| `define` | `gui.namebox_tile` | `game\gui.rpy` | `127` | `define gui.namebox_tile = False` |
| `define` | `gui.dialogue_xpos` | `game\gui.rpy` | `133` | `define gui.dialogue_xpos = 402` |
| `define` | `gui.dialogue_ypos` | `game\gui.rpy` | `134` | `define gui.dialogue_ypos = 75` |
| `define` | `gui.dialogue_width` | `game\gui.rpy` | `137` | `define gui.dialogue_width = 1116` |
| `define` | `gui.dialogue_text_xalign` | `game\gui.rpy` | `141` | `define gui.dialogue_text_xalign = 0.0` |
| `define` | `gui.button_width` | `game\gui.rpy` | `150` | `define gui.button_width = None` |
| `define` | `gui.button_height` | `game\gui.rpy` | `151` | `define gui.button_height = None` |
| `define` | `gui.button_borders` | `game\gui.rpy` | `154` | `define gui.button_borders = Borders(6, 6, 6, 6)` |
| `define` | `gui.button_tile` | `game\gui.rpy` | `158` | `define gui.button_tile = False` |
| `define` | `gui.button_text_font` | `game\gui.rpy` | `161` | `define gui.button_text_font = gui.interface_text_font` |
| `define` | `gui.button_text_size` | `game\gui.rpy` | `164` | `define gui.button_text_size = gui.interface_text_size` |
| `define` | `gui.button_text_idle_color` | `game\gui.rpy` | `167` | `define gui.button_text_idle_color = gui.idle_color` |
| `define` | `gui.button_text_hover_color` | `game\gui.rpy` | `168` | `define gui.button_text_hover_color = gui.hover_color` |
| `define` | `gui.button_text_selected_color` | `game\gui.rpy` | `169` | `define gui.button_text_selected_color = gui.selected_color` |
| `define` | `gui.button_text_insensitive_color` | `game\gui.rpy` | `170` | `define gui.button_text_insensitive_color = gui.insensitive_color` |
| `define` | `gui.button_text_xalign` | `game\gui.rpy` | `174` | `define gui.button_text_xalign = 0.0` |
| `define` | `gui.radio_button_borders` | `game\gui.rpy` | `183` | `define gui.radio_button_borders = Borders(27, 6, 6, 6)` |
| `define` | `gui.check_button_borders` | `game\gui.rpy` | `185` | `define gui.check_button_borders = Borders(27, 6, 6, 6)` |
| `define` | `gui.confirm_button_text_xalign` | `game\gui.rpy` | `187` | `define gui.confirm_button_text_xalign = 0.5` |
| `define` | `gui.page_button_borders` | `game\gui.rpy` | `189` | `define gui.page_button_borders = Borders(15, 6, 15, 6)` |
| `define` | `gui.quick_button_borders` | `game\gui.rpy` | `191` | `define gui.quick_button_borders = Borders(15, 6, 15, 0)` |
| `define` | `gui.quick_button_text_size` | `game\gui.rpy` | `192` | `define gui.quick_button_text_size = 21` |
| `define` | `gui.quick_button_text_idle_color` | `game\gui.rpy` | `193` | `define gui.quick_button_text_idle_color = gui.idle_small_color` |
| `define` | `gui.quick_button_text_selected_color` | `game\gui.rpy` | `194` | `define gui.quick_button_text_selected_color = gui.accent_color` |
| `define` | `gui.choice_button_width` | `game\gui.rpy` | `207` | `define gui.choice_button_width = 452` |
| `define` | `gui.choice_button_height` | `game\gui.rpy` | `208` | `define gui.choice_button_height = None` |
| `define` | `gui.choice_button_tile` | `game\gui.rpy` | `209` | `define gui.choice_button_tile = False` |
| `define` | `gui.choice_button_borders` | `game\gui.rpy` | `210` | `define gui.choice_button_borders = Borders(20, 8, 20, 8)` |
| `define` | `gui.choice_button_text_font` | `game\gui.rpy` | `211` | `define gui.choice_button_text_font = gui.text_font` |
| `define` | `gui.choice_button_text_size` | `game\gui.rpy` | `212` | `define gui.choice_button_text_size = gui.text_size` |
| `define` | `gui.choice_button_text_xalign` | `game\gui.rpy` | `213` | `define gui.choice_button_text_xalign = 0.0` |
| `define` | `gui.choice_button_text_idle_color` | `game\gui.rpy` | `214` | `define gui.choice_button_text_idle_color = '#888888'` |
| `define` | `gui.choice_button_text_hover_color` | `game\gui.rpy` | `215` | `define gui.choice_button_text_hover_color = "#ffffff"` |
| `define` | `gui.choice_button_text_insensitive_color` | `game\gui.rpy` | `216` | `define gui.choice_button_text_insensitive_color = '#8888887f'` |
| `define` | `gui.slot_button_width` | `game\gui.rpy` | `226` | `define gui.slot_button_width = 414` |
| `define` | `gui.slot_button_height` | `game\gui.rpy` | `227` | `define gui.slot_button_height = 309` |
| `define` | `gui.slot_button_borders` | `game\gui.rpy` | `228` | `define gui.slot_button_borders = Borders(15, 15, 15, 15)` |
| `define` | `gui.slot_button_text_size` | `game\gui.rpy` | `229` | `define gui.slot_button_text_size = 21` |
| `define` | `gui.status_button_text_size` | `game\gui.rpy` | `230` | `define gui.status_button_text_size = gui.slot_button_text_size` |
| `define` | `gui.slot_button_text_xalign` | `game\gui.rpy` | `231` | `define gui.slot_button_text_xalign = 0.5` |
| `define` | `gui.slot_button_text_idle_color` | `game\gui.rpy` | `232` | `define gui.slot_button_text_idle_color = gui.idle_small_color` |
| `define` | `gui.slot_button_text_selected_idle_color` | `game\gui.rpy` | `233` | `define gui.slot_button_text_selected_idle_color = gui.selected_color` |
| `define` | `gui.slot_button_text_selected_hover_color` | `game\gui.rpy` | `234` | `define gui.slot_button_text_selected_hover_color = gui.hover_color` |
| `define` | `config.thumbnail_width` | `game\gui.rpy` | `237` | `define config.thumbnail_width = 384` |
| `define` | `config.thumbnail_height` | `game\gui.rpy` | `238` | `define config.thumbnail_height = 216` |
| `define` | `gui.file_slot_cols` | `game\gui.rpy` | `241` | `define gui.file_slot_cols = 3` |
| `define` | `gui.file_slot_rows` | `game\gui.rpy` | `242` | `define gui.file_slot_rows = 2` |
| `define` | `gui.navigation_xpos` | `game\gui.rpy` | `252` | `define gui.navigation_xpos = 60` |
| `define` | `gui.skip_ypos` | `game\gui.rpy` | `255` | `define gui.skip_ypos = 15` |
| `define` | `gui.notify_ypos` | `game\gui.rpy` | `258` | `define gui.notify_ypos = 68` |
| `define` | `gui.choice_spacing` | `game\gui.rpy` | `261` | `define gui.choice_spacing = 33` |
| `define` | `gui.navigation_spacing` | `game\gui.rpy` | `264` | `define gui.navigation_spacing = 6` |
| `define` | `gui.pref_spacing` | `game\gui.rpy` | `267` | `define gui.pref_spacing = 15` |
| `define` | `gui.pref_button_spacing` | `game\gui.rpy` | `270` | `define gui.pref_button_spacing = 0` |
| `define` | `gui.page_spacing` | `game\gui.rpy` | `273` | `define gui.page_spacing = 0` |
| `define` | `gui.slot_spacing` | `game\gui.rpy` | `276` | `define gui.slot_spacing = 15` |
| `define` | `gui.main_menu_text_xalign` | `game\gui.rpy` | `279` | `define gui.main_menu_text_xalign = 1.0` |
| `define` | `gui.frame_borders` | `game\gui.rpy` | `288` | `define gui.frame_borders = Borders(6, 6, 6, 6)` |
| `define` | `gui.confirm_frame_borders` | `game\gui.rpy` | `291` | `define gui.confirm_frame_borders = Borders(60, 60, 60, 60)` |
| `define` | `gui.skip_frame_borders` | `game\gui.rpy` | `294` | `define gui.skip_frame_borders = Borders(24, 8, 75, 8)` |
| `define` | `gui.notify_frame_borders` | `game\gui.rpy` | `297` | `define gui.notify_frame_borders = Borders(24, 8, 60, 8)` |
| `define` | `gui.frame_tile` | `game\gui.rpy` | `300` | `define gui.frame_tile = False` |
| `define` | `gui.bar_size` | `game\gui.rpy` | `312` | `define gui.bar_size = 38` |
| `define` | `gui.scrollbar_size` | `game\gui.rpy` | `313` | `define gui.scrollbar_size = 18` |
| `define` | `gui.slider_size` | `game\gui.rpy` | `314` | `define gui.slider_size = 38` |
| `define` | `gui.bar_tile` | `game\gui.rpy` | `317` | `define gui.bar_tile = False` |
| `define` | `gui.scrollbar_tile` | `game\gui.rpy` | `318` | `define gui.scrollbar_tile = False` |
| `define` | `gui.slider_tile` | `game\gui.rpy` | `319` | `define gui.slider_tile = False` |
| `define` | `gui.bar_borders` | `game\gui.rpy` | `322` | `define gui.bar_borders = Borders(6, 6, 6, 6)` |
| `define` | `gui.scrollbar_borders` | `game\gui.rpy` | `323` | `define gui.scrollbar_borders = Borders(6, 6, 6, 6)` |
| `define` | `gui.slider_borders` | `game\gui.rpy` | `324` | `define gui.slider_borders = Borders(6, 6, 6, 6)` |
| `define` | `gui.vbar_borders` | `game\gui.rpy` | `327` | `define gui.vbar_borders = Borders(6, 6, 6, 6)` |
| `define` | `gui.vscrollbar_borders` | `game\gui.rpy` | `328` | `define gui.vscrollbar_borders = Borders(6, 6, 6, 6)` |
| `define` | `gui.vslider_borders` | `game\gui.rpy` | `329` | `define gui.vslider_borders = Borders(6, 6, 6, 6)` |
| `define` | `gui.unscrollable` | `game\gui.rpy` | `333` | `define gui.unscrollable = "hide"` |
| `define` | `config.history_length` | `game\gui.rpy` | `341` | `define config.history_length = 250` |
| `define` | `gui.history_height` | `game\gui.rpy` | `345` | `define gui.history_height = 210` |
| `define` | `gui.history_spacing` | `game\gui.rpy` | `348` | `define gui.history_spacing = 0` |
| `define` | `gui.history_name_xpos` | `game\gui.rpy` | `352` | `define gui.history_name_xpos = 233` |
| `define` | `gui.history_name_ypos` | `game\gui.rpy` | `353` | `define gui.history_name_ypos = 0` |
| `define` | `gui.history_name_width` | `game\gui.rpy` | `354` | `define gui.history_name_width = 233` |
| `define` | `gui.history_name_xalign` | `game\gui.rpy` | `355` | `define gui.history_name_xalign = 1.0` |
| `define` | `gui.history_text_xpos` | `game\gui.rpy` | `358` | `define gui.history_text_xpos = 255` |
| `define` | `gui.history_text_ypos` | `game\gui.rpy` | `359` | `define gui.history_text_ypos = 3` |
| `define` | `gui.history_text_width` | `game\gui.rpy` | `360` | `define gui.history_text_width = 1110` |
| `define` | `gui.history_text_xalign` | `game\gui.rpy` | `361` | `define gui.history_text_xalign = 0.0` |
| `define` | `gui.nvl_borders` | `game\gui.rpy` | `369` | `define gui.nvl_borders = Borders(0, 15, 0, 30)` |
| `define` | `gui.nvl_list_length` | `game\gui.rpy` | `373` | `define gui.nvl_list_length = 6` |
| `define` | `gui.nvl_height` | `game\gui.rpy` | `377` | `define gui.nvl_height = 173` |
| `define` | `gui.nvl_spacing` | `game\gui.rpy` | `381` | `define gui.nvl_spacing = 15` |
| `define` | `gui.nvl_name_xpos` | `game\gui.rpy` | `385` | `define gui.nvl_name_xpos = 645` |
| `define` | `gui.nvl_name_ypos` | `game\gui.rpy` | `386` | `define gui.nvl_name_ypos = 0` |
| `define` | `gui.nvl_name_width` | `game\gui.rpy` | `387` | `define gui.nvl_name_width = 225` |
| `define` | `gui.nvl_name_xalign` | `game\gui.rpy` | `388` | `define gui.nvl_name_xalign = 1.0` |
| `define` | `gui.nvl_text_xpos` | `game\gui.rpy` | `391` | `define gui.nvl_text_xpos = 675` |
| `define` | `gui.nvl_text_ypos` | `game\gui.rpy` | `392` | `define gui.nvl_text_ypos = 12` |
| `define` | `gui.nvl_text_width` | `game\gui.rpy` | `393` | `define gui.nvl_text_width = 885` |
| `define` | `gui.nvl_text_xalign` | `game\gui.rpy` | `394` | `define gui.nvl_text_xalign = 0.0` |
| `define` | `gui.nvl_thought_xpos` | `game\gui.rpy` | `398` | `define gui.nvl_thought_xpos = 360` |
| `define` | `gui.nvl_thought_ypos` | `game\gui.rpy` | `399` | `define gui.nvl_thought_ypos = 0` |
| `define` | `gui.nvl_thought_width` | `game\gui.rpy` | `400` | `define gui.nvl_thought_width = 1170` |
| `define` | `gui.nvl_thought_xalign` | `game\gui.rpy` | `401` | `define gui.nvl_thought_xalign = 0.0` |
| `define` | `gui.nvl_button_xpos` | `game\gui.rpy` | `404` | `define gui.nvl_button_xpos = 675` |
| `define` | `gui.nvl_button_xalign` | `game\gui.rpy` | `405` | `define gui.nvl_button_xalign = 0.0` |
| `define` | `gui.language` | `game\gui.rpy` | `414` | `define gui.language = "unicode"` |
| `default` | `action_override_text` | `game\Inn\Actions.rpy` | `1` | `default action_override_text = ""` |
| `default` | `AmandaGloryCurState` | `game\Inn\AmandaAtGloryHole.rpy` | `1` | `default AmandaGloryCurState = 0` |
| `default` | `_amanda_dynamic_blocks_initialized` | `game\Inn\AmandaDynamicCommonBlocks.rpy` | `1` | `default _amanda_dynamic_blocks_initialized = True` |
| `default` | `AmandaDynamicNextJump` | `game\Inn\AmandaDynamicCommonBlocks.rpy` | `2` | `default AmandaDynamicNextJump = ""` |
| `default` | `_tractir_progress_revision` | `game\Inn\AutosaveSupport.rpy` | `1` | `default _tractir_progress_revision = 0` |
| `default` | `_tractir_last_autosave_reason` | `game\Inn\AutosaveSupport.rpy` | `2` | `default _tractir_last_autosave_reason = ""` |
| `default` | `BackyardToiletBusy` | `game\Inn\Backyard.rpy` | `151` | `default BackyardToiletBusy = 0` |
| `default` | `BarberShopSavedText` | `game\Inn\BarberShop.rpy` | `1` | `default BarberShopSavedText = ""` |
| `default` | `BarberFirstTipSeen` | `game\Inn\BarberShop.rpy` | `2` | `default BarberFirstTipSeen = 0` |
| `default` | `BarberInvitePending` | `game\Inn\BarberShop.rpy` | `3` | `default BarberInvitePending = {}` |
| `default` | `BarberVisitLastDay` | `game\Inn\BarberShop.rpy` | `4` | `default BarberVisitLastDay = {}` |
| `default` | `ViewIngaSex` | `game\Inn\BeckyHomeFront.rpy` | `6` | `default ViewIngaSex = 0` |
| `default` | `ArriveMode` | `game\Inn\BeckyHomeFront.rpy` | `7` | `default ArriveMode = ""` |
| `default` | `RandIngaFuck` | `game\Inn\BeckyHomeFront.rpy` | `8` | `default RandIngaFuck = 1` |
| `default` | `_becky_home_front_resume` | `game\Inn\BeckyHomeFront.rpy` | `9` | `default _becky_home_front_resume = False` |
| `default` | `IngaVar` | `game\Inn\BeckyHomeFront.rpy` | `10` | `default IngaVar = {"SawLucassex": 0, "Knowher": 0}` |
| `default` | `BodyInteractionProfiles` | `game\Inn\BodyInteractionModel.rpy` | `1` | `default BodyInteractionProfiles = {}` |
| `default` | `knowsMC` | `game\Inn\CharacterActionHub.rpy` | `1` | `default knowsMC = {}` |
| `default` | `action_menu_entity_type` | `game\Inn\CharacterActionHub.rpy` | `3` | `default action_menu_entity_type = ""` |
| `default` | `action_menu_entity_id` | `game\Inn\CharacterActionHub.rpy` | `4` | `default action_menu_entity_id = ""` |
| `default` | `action_menu_where` | `game\Inn\CharacterActionHub.rpy` | `5` | `default action_menu_where = ""` |
| `default` | `action_menu_title` | `game\Inn\CharacterActionHub.rpy` | `6` | `default action_menu_title = ""` |
| `default` | `action_menu_entity_data` | `game\Inn\CharacterActionHub.rpy` | `7` | `default action_menu_entity_data = {}` |
| `default` | `action_menu_actions` | `game\Inn\CharacterActionHub.rpy` | `8` | `default action_menu_actions = []` |
| `default` | `action_menu_specs` | `game\Inn\CharacterActionHub.rpy` | `9` | `default action_menu_specs = []` |
| `default` | `action_menu_selected` | `game\Inn\CharacterActionHub.rpy` | `10` | `default action_menu_selected = ""` |
| `default` | `ChurchAfterCermon` | `game\Inn\Church.rpy` | `1` | `default ChurchAfterCermon = {}` |
| `default` | `PriestIncestAgree` | `game\Inn\Church.rpy` | `2` | `default PriestIncestAgree = 0` |
| `define` | `recipe_names` | `game\Inn\CraftingRecipes.rpy` | `1` | `define recipe_names = []` |
| `define` | `recipe_pages` | `game\Inn\CraftingRecipes.rpy` | `2` | `define recipe_pages = {}` |
| `default` | `RecipeBookSelectedId` | `game\Inn\CraftingRecipes.rpy` | `3` | `default RecipeBookSelectedId = ""` |
| `default` | `RecipeBookReturnRoomCode` | `game\Inn\CraftingRecipes.rpy` | `4` | `default RecipeBookReturnRoomCode = ""` |
| `default` | `RecipeBookReturnObjectId` | `game\Inn\CraftingRecipes.rpy` | `5` | `default RecipeBookReturnObjectId = ""` |
| `default` | `RecipeBookReturnPicture` | `game\Inn\CraftingRecipes.rpy` | `6` | `default RecipeBookReturnPicture = ""` |
| `default` | `player_company` | `game\Inn\DogCompanion.rpy` | `1` | `default player_company = []` |
| `default` | `dog` | `game\Inn\DogCompanion.rpy` | `621` | `default dog = DogCompanion()` |
| `default` | `DressShopCatalogRack` | `game\Inn\DressShop.rpy` | `1` | `default DressShopCatalogRack = ""` |
| `default` | `DressShopCatalogDressCode` | `game\Inn\DressShop.rpy` | `2` | `default DressShopCatalogDressCode = ""` |
| `default` | `DressShopMaleCatalogItemIds` | `game\Inn\DressShop.rpy` | `3` | `default DressShopMaleCatalogItemIds = []` |
| `default` | `DressShopFemaleCatalogItemIds` | `game\Inn\DressShop.rpy` | `4` | `default DressShopFemaleCatalogItemIds = []` |
| `default` | `DressShopSavedText` | `game\Inn\DressShop.rpy` | `5` | `default DressShopSavedText = ""` |
| `default` | `DressTryStep` | `game\Inn\DressTry.rpy` | `1` | `default DressTryStep = 0` |
| `default` | `ellona_room_object_menu_room_code` | `game\Inn\EllonaTemple.rpy` | `120` | `default ellona_room_object_menu_room_code = "EllonaTemple"` |
| `default` | `ellona_room_object_menu_object_id` | `game\Inn\EllonaTemple.rpy` | `121` | `default ellona_room_object_menu_object_id = ""` |
| `default` | `FightLoadedAmmo` | `game\Inn\FightSystemRuntime.rpy` | `1` | `default FightLoadedAmmo = ""` |
| `default` | `FightTargetIndex` | `game\Inn\FightSystemRuntime.rpy` | `2` | `default FightTargetIndex = 1` |
| `default` | `ForestSavedText` | `game\Inn\Forest.rpy` | `210` | `default ForestSavedText = ""` |
| `default` | `ForestReturnTarget` | `game\Inn\Forest.rpy` | `211` | `default ForestReturnTarget = "StreetTavern"` |
| `default` | `ForestSubroomSavedText` | `game\Inn\Forest.rpy` | `212` | `default ForestSubroomSavedText = ""` |
| `define` | `item_catalog` | `game\Inn\GameItems.rpy` | `1` | `define item_catalog = {}` |
| `define` | `game_items` | `game\Inn\GameItems.rpy` | `2` | `define game_items = []` |
| `define` | `game_item_registry` | `game\Inn\GameItems.rpy` | `3` | `define game_item_registry = {}` |
| `define` | `menDress` | `game\Inn\GameItems.rpy` | `4` | `define menDress = []` |
| `define` | `womenDress` | `game\Inn\GameItems.rpy` | `5` | `define womenDress = []` |
| `default` | `HouseholdRuntimeEventSeen` | `game\Inn\HouseholdRuntimeEvents.rpy` | `1` | `default HouseholdRuntimeEventSeen = {}` |
| `default` | `HouseholdInsightState` | `game\Inn\HouseholdRuntimeEvents.rpy` | `2` | `default HouseholdInsightState = {}` |
| `default` | `HouseholdSoapRequestLastDay` | `game\Inn\HouseholdRuntimeEvents.rpy` | `3` | `default HouseholdSoapRequestLastDay = {}` |
| `default` | `HouseholdBarberRequestLastDay` | `game\Inn\HouseholdRuntimeEvents.rpy` | `4` | `default HouseholdBarberRequestLastDay = {}` |
| `default` | `HouseholdWarmDrinkLastDay` | `game\Inn\HouseholdRuntimeEvents.rpy` | `5` | `default HouseholdWarmDrinkLastDay = {}` |
| `default` | `HunterClubTradeMode` | `game\Inn\HunterClub.rpy` | `350` | `default HunterClubTradeMode = ""` |
| `default` | `HunterClubTradeSelection` | `game\Inn\HunterClub.rpy` | `351` | `default HunterClubTradeSelection = {}` |
| `default` | `cookincr` | `game\Inn\IncreaseSkill.rpy` | `2` | `default cookincr = {}` |
| `default` | `cleanincr` | `game\Inn\IncreaseSkill.rpy` | `3` | `default cleanincr = {}` |
| `default` | `waitressincr` | `game\Inn\IncreaseSkill.rpy` | `4` | `default waitressincr = {}` |
| `default` | `EddieVar` | `game\Inn\InitSecondaryNPC.rpy` | `1` | `default EddieVar = {}` |
| `default` | `AlberVar` | `game\Inn\InitSecondaryNPC.rpy` | `2` | `default AlberVar = {}` |
| `default` | `FranVar` | `game\Inn\InitSecondaryNPC.rpy` | `3` | `default FranVar = {}` |
| `default` | `FranBusy` | `game\Inn\InitSecondaryNPC.rpy` | `4` | `default FranBusy = {}` |
| `default` | `DraupnirVar` | `game\Inn\InitSecondaryNPC.rpy` | `5` | `default DraupnirVar = {}` |
| `default` | `MongolVar` | `game\Inn\InitSecondaryNPC.rpy` | `6` | `default MongolVar = {}` |
| `default` | `ZimmerVar` | `game\Inn\InitSecondaryNPC.rpy` | `7` | `default ZimmerVar = {}` |
| `default` | `RobinVar` | `game\Inn\InitSecondaryNPC.rpy` | `8` | `default RobinVar = {}` |
| `default` | `RobbersHeadNameTmp` | `game\Inn\InitSecondaryNPC.rpy` | `9` | `default RobbersHeadNameTmp = ""` |
| `default` | `Talked` | `game\Inn\InitSecondaryNPC.rpy` | `10` | `default Talked = {}` |
| `default` | `cancumdaily_npc` | `game\Inn\InitSecondaryNPC.rpy` | `11` | `default cancumdaily_npc = {}` |
| `default` | `KnowMongol` | `game\Inn\InitSecondaryNPC.rpy` | `12` | `default KnowMongol = 0` |
| `default` | `StolenHorseDays` | `game\Inn\InitSecondaryNPC.rpy` | `13` | `default StolenHorseDays = 0` |
| `default` | `ONGLOAD` | `game\Inn\Intro.rpy` | `2` | `default ONGLOAD = "loadg"` |
| `default` | `ONGSAVE` | `game\Inn\Intro.rpy` | `3` | `default ONGSAVE = "saveg"` |
| `default` | `ONNEWLOC` | `game\Inn\Intro.rpy` | `4` | `default ONNEWLOC = "LOC"` |
| `default` | `CurLoc` | `game\Inn\Intro.rpy` | `6` | `default CurLoc = "Intro"` |
| `default` | `location` | `game\Inn\Intro.rpy` | `7` | `default location = "Intro"` |
| `default` | `PrevLoc` | `game\Inn\Intro.rpy` | `8` | `default PrevLoc = ""` |
| `default` | `MainTxt` | `game\Inn\Intro.rpy` | `9` | `default MainTxt = ""` |
| `default` | `CurLocDesc` | `game\Inn\Intro.rpy` | `10` | `default CurLocDesc = ""` |
| `default` | `MaxCounterToClean` | `game\Inn\Intro.rpy` | `11` | `default MaxCounterToClean = 4` |
| `default` | `DebugFlag` | `game\Inn\Intro.rpy` | `12` | `default DebugFlag = 0` |
| `default` | `_layout_last_picture` | `game\Inn\Intro.rpy` | `13` | `default _layout_last_picture = ""` |
| `default` | `GraphicsOn` | `game\Inn\Intro.rpy` | `14` | `default GraphicsOn = 1` |
| `default` | `time` | `game\Inn\Intro.rpy` | `17` | `default time = 0` |
| `default` | `hour` | `game\Inn\Intro.rpy` | `18` | `default hour = 8` |
| `default` | `minute` | `game\Inn\Intro.rpy` | `19` | `default minute = 0` |
| `default` | `day` | `game\Inn\Intro.rpy` | `20` | `default day = 1` |
| `default` | `month` | `game\Inn\Intro.rpy` | `21` | `default month = 1` |
| `default` | `week` | `game\Inn\Intro.rpy` | `22` | `default week = 1` |
| `default` | `year` | `game\Inn\Intro.rpy` | `23` | `default year = 1100` |
| `default` | `age` | `game\Inn\Intro.rpy` | `24` | `default age = 20` |
| `default` | `money` | `game\Inn\Intro.rpy` | `25` | `default money = 10000` |
| `default` | `fun` | `game\Inn\Intro.rpy` | `26` | `default fun = 50` |
| `default` | `energy` | `game\Inn\Intro.rpy` | `27` | `default energy = 100` |
| `default` | `health` | `game\Inn\Intro.rpy` | `28` | `default health = 100` |
| `default` | `notoriety` | `game\Inn\Intro.rpy` | `29` | `default notoriety = 0` |
| `default` | `exploration` | `game\Inn\Intro.rpy` | `30` | `default exploration = 0` |
| `default` | `charisma` | `game\Inn\Intro.rpy` | `31` | `default charisma = 0` |
| `default` | `rebellion` | `game\Inn\Intro.rpy` | `32` | `default rebellion = 0` |
| `default` | `look` | `game\Inn\Intro.rpy` | `33` | `default look = 100` |
| `default` | `costumecondition` | `game\Inn\Intro.rpy` | `34` | `default costumecondition = 100` |
| `default` | `dayssincehaircut` | `game\Inn\Intro.rpy` | `35` | `default dayssincehaircut = 0` |
| `default` | `PlayerHaircutDaySt` | `game\Inn\Intro.rpy` | `36` | `default PlayerHaircutDaySt = 0` |
| `default` | `PlayerDressDaySt` | `game\Inn\Intro.rpy` | `37` | `default PlayerDressDaySt = {"villagedress": 0}` |
| `default` | `dayssincewash` | `game\Inn\Intro.rpy` | `38` | `default dayssincewash = 0` |
| `default` | `ashesdirtydays` | `game\Inn\Intro.rpy` | `39` | `default ashesdirtydays = 0` |
| `default` | `upstairsroomsdirty` | `game\Inn\Intro.rpy` | `40` | `default upstairsroomsdirty = 0` |
| `default` | `taverncleanliness` | `game\Inn\Intro.rpy` | `41` | `default taverncleanliness = 60` |
| `default` | `Arousal` | `game\Inn\Intro.rpy` | `42` | `default Arousal = {"You": 0}` |
| `default` | `HadSex` | `game\Inn\Intro.rpy` | `43` | `default HadSex = {"You": 0}` |
| `default` | `topdress` | `game\Inn\Intro.rpy` | `44` | `default topdress = {}` |
| `default` | `bottomdress` | `game\Inn\Intro.rpy` | `45` | `default bottomdress = {}` |
| `default` | `bra` | `game\Inn\Intro.rpy` | `46` | `default bra = {}` |
| `default` | `panties` | `game\Inn\Intro.rpy` | `47` | `default panties = {}` |
| `default` | `legs` | `game\Inn\Intro.rpy` | `48` | `default legs = {}` |
| `default` | `shoes` | `game\Inn\Intro.rpy` | `49` | `default shoes = {}` |
| `default` | `topraised` | `game\Inn\Intro.rpy` | `50` | `default topraised = {}` |
| `default` | `bottomraised` | `game\Inn\Intro.rpy` | `51` | `default bottomraised = {}` |
| `default` | `RealName` | `game\Inn\Intro.rpy` | `52` | `default RealName = {}` |
| `default` | `RealName2` | `game\Inn\Intro.rpy` | `53` | `default RealName2 = {}` |
| `default` | `RealName3` | `game\Inn\Intro.rpy` | `54` | `default RealName3 = {}` |
| `default` | `DateOfBirth` | `game\Inn\Intro.rpy` | `55` | `default DateOfBirth = {}` |
| `default` | `age_girls` | `game\Inn\Intro.rpy` | `56` | `default age_girls = {}` |
| `default` | `kids` | `game\Inn\Intro.rpy` | `57` | `default kids = {}` |
| `default` | `beauty` | `game\Inn\Intro.rpy` | `58` | `default beauty = {}` |
| `default` | `pregfather` | `game\Inn\Intro.rpy` | `59` | `default pregfather = {}` |
| `default` | `CurrentLoc` | `game\Inn\Intro.rpy` | `60` | `default CurrentLoc = {}` |
| `default` | `girltextdesc` | `game\Inn\Intro.rpy` | `61` | `default girltextdesc = {}` |
| `default` | `cooking` | `game\Inn\Intro.rpy` | `62` | `default cooking = {}` |
| `default` | `cleaning` | `game\Inn\Intro.rpy` | `63` | `default cleaning = {}` |
| `default` | `virginity` | `game\Inn\Intro.rpy` | `64` | `default virginity = {}` |
| `default` | `PussyWetStart` | `game\Inn\Intro.rpy` | `65` | `default PussyWetStart = {}` |
| `default` | `Drunk` | `game\Inn\Intro.rpy` | `66` | `default Drunk = {}` |
| `default` | `LickPussy` | `game\Inn\Intro.rpy` | `67` | `default LickPussy = {}` |
| `default` | `pregnancy` | `game\Inn\Intro.rpy` | `68` | `default pregnancy = {}` |
| `default` | `TitsVisible` | `game\Inn\Intro.rpy` | `69` | `default TitsVisible = {}` |
| `default` | `GrupenSex` | `game\Inn\Intro.rpy` | `70` | `default GrupenSex = {}` |
| `default` | `PussyVisible` | `game\Inn\Intro.rpy` | `71` | `default PussyVisible = {}` |
| `default` | `ShortSkirtNoPanties` | `game\Inn\Intro.rpy` | `72` | `default ShortSkirtNoPanties = {}` |
| `default` | `CockInMouth` | `game\Inn\Intro.rpy` | `73` | `default CockInMouth = {}` |
| `default` | `CockInPussy` | `game\Inn\Intro.rpy` | `74` | `default CockInPussy = {}` |
| `default` | `CockInTits` | `game\Inn\Intro.rpy` | `75` | `default CockInTits = {}` |
| `default` | `EddieCockInMouth` | `game\Inn\Intro.rpy` | `76` | `default EddieCockInMouth = {}` |
| `default` | `EddieCockInPussy` | `game\Inn\Intro.rpy` | `77` | `default EddieCockInPussy = {}` |
| `default` | `EddieCockInTits` | `game\Inn\Intro.rpy` | `78` | `default EddieCockInTits = {}` |
| `default` | `CumFaceYou` | `game\Inn\Intro.rpy` | `79` | `default CumFaceYou = {}` |
| `default` | `CumFaceOthers` | `game\Inn\Intro.rpy` | `80` | `default CumFaceOthers = {}` |
| `default` | `CumTitsYou` | `game\Inn\Intro.rpy` | `81` | `default CumTitsYou = {}` |
| `default` | `CumTitsOthers` | `game\Inn\Intro.rpy` | `82` | `default CumTitsOthers = {}` |
| `default` | `CumInsideYou` | `game\Inn\Intro.rpy` | `83` | `default CumInsideYou = {}` |
| `default` | `CumInsideOthers` | `game\Inn\Intro.rpy` | `84` | `default CumInsideOthers = {}` |
| `default` | `TodaySexEvents` | `game\Inn\Intro.rpy` | `85` | `default TodaySexEvents = []` |
| `default` | `sex_history_by_girl` | `game\Inn\Intro.rpy` | `86` | `default sex_history_by_girl = {}` |
| `default` | `sex_history_next_id` | `game\Inn\Intro.rpy` | `87` | `default sex_history_next_id = {}` |
| `default` | `ClientsDayTotal` | `game\Inn\Intro.rpy` | `88` | `default ClientsDayTotal = {}` |
| `default` | `cancumdaily` | `game\Inn\Intro.rpy` | `89` | `default cancumdaily = 2` |
| `default` | `cametoday` | `game\Inn\Intro.rpy` | `90` | `default cametoday = 0` |
| `default` | `BlessedByEllona` | `game\Inn\Intro.rpy` | `91` | `default BlessedByEllona = 0` |
| `default` | `CursedByEllona` | `game\Inn\Intro.rpy` | `92` | `default CursedByEllona = 0` |
| `default` | `CursedByEllonaDays` | `game\Inn\Intro.rpy` | `93` | `default CursedByEllonaDays = 0` |
| `default` | `CursedByEllonaReduce` | `game\Inn\Intro.rpy` | `94` | `default CursedByEllonaReduce = 0` |
| `default` | `MyDresses` | `game\Inn\Intro.rpy` | `95` | `default MyDresses = ["villagedress"]` |
| `default` | `MyCurDress` | `game\Inn\Intro.rpy` | `96` | `default MyCurDress = "villagedress"` |
| `default` | `EquippedWeapon` | `game\Inn\Intro.rpy` | `97` | `default EquippedWeapon = ""` |
| `default` | `EquippedArmor` | `game\Inn\Intro.rpy` | `98` | `default EquippedArmor = ""` |
| `default` | `company_list` | `game\Inn\Intro.rpy` | `99` | `default company_list = []` |
| `default` | `PlayerFightSupply` | `game\Inn\Intro.rpy` | `100` | `default PlayerFightSupply = {}` |
| `default` | `FightWeaponLoaded` | `game\Inn\Intro.rpy` | `101` | `default FightWeaponLoaded = 0` |
| `default` | `FightRetreatUsed` | `game\Inn\Intro.rpy` | `102` | `default FightRetreatUsed = 0` |
| `default` | `SickDays` | `game\Inn\Intro.rpy` | `103` | `default SickDays = 0` |
| `default` | `FightEnemyState` | `game\Inn\Intro.rpy` | `104` | `default FightEnemyState = {}` |
| `default` | `HuntUnlocked` | `game\Inn\Intro.rpy` | `105` | `default HuntUnlocked = False` |
| `default` | `HuntLastResult` | `game\Inn\Intro.rpy` | `106` | `default HuntLastResult = {}` |
| `default` | `FightSideLog` | `game\Inn\Intro.rpy` | `107` | `default FightSideLog = []` |
| `default` | `FightEnemyParty` | `game\Inn\Intro.rpy` | `108` | `default FightEnemyParty = []` |
| `default` | `FightEnemyId` | `game\Inn\Intro.rpy` | `109` | `default FightEnemyId = ""` |
| `default` | `playerItems` | `game\Inn\Intro.rpy` | `110` | `default playerItems = {}` |
| `default` | `DressProduced` | `game\Inn\Intro.rpy` | `111` | `default DressProduced = ""` |
| `default` | `DressBuyer` | `game\Inn\Intro.rpy` | `112` | `default DressBuyer = ""` |
| `default` | `FridayDancesCount` | `game\Inn\Intro.rpy` | `113` | `default FridayDancesCount = 0` |
| `default` | `DanceSponsor` | `game\Inn\Intro.rpy` | `114` | `default DanceSponsor = 0` |
| `default` | `DanceWatchLine` | `game\Inn\Intro.rpy` | `115` | `default DanceWatchLine = {}` |
| `default` | `GirlDance` | `game\Inn\Intro.rpy` | `116` | `default GirlDance = []` |
| `default` | `DanceStep` | `game\Inn\Intro.rpy` | `117` | `default DanceStep = 0` |
| `default` | `HandsDance` | `game\Inn\Intro.rpy` | `118` | `default HandsDance = ""` |
| `default` | `KissDance` | `game\Inn\Intro.rpy` | `119` | `default KissDance = 0` |
| `default` | `TitsDance` | `game\Inn\Intro.rpy` | `120` | `default TitsDance = 0` |
| `default` | `CurrentActions` | `game\Inn\Intro.rpy` | `121` | `default CurrentActions = ""` |
| `default` | `DailyEventsList` | `game\Inn\Intro.rpy` | `122` | `default DailyEventsList = []` |
| `default` | `KidsList` | `game\Inn\Intro.rpy` | `123` | `default KidsList = []` |
| `default` | `KidsListNextId` | `game\Inn\Intro.rpy` | `124` | `default KidsListNextId = 1` |
| `default` | `_kids_functions_initialized` | `game\Inn\Intro.rpy` | `125` | `default _kids_functions_initialized = False` |
| `default` | `KidsPosobie` | `game\Inn\Intro.rpy` | `126` | `default KidsPosobie = 0` |
| `default` | `KidBirthPosobie` | `game\Inn\Intro.rpy` | `127` | `default KidBirthPosobie = ""` |
| `default` | `ProstitutesKids` | `game\Inn\Intro.rpy` | `128` | `default ProstitutesKids = 0` |
| `default` | `Breastfeed` | `game\Inn\Intro.rpy` | `129` | `default Breastfeed = {}` |
| `default` | `Lactate` | `game\Inn\Intro.rpy` | `130` | `default Lactate = {}` |
| `default` | `PregTotalSuspects` | `game\Inn\Intro.rpy` | `131` | `default PregTotalSuspects = {}` |
| `default` | `ZaletSuspectFinal` | `game\Inn\Intro.rpy` | `132` | `default ZaletSuspectFinal = {}` |
| `default` | `BlockTimeAdvance` | `game\Inn\Intro.rpy` | `133` | `default BlockTimeAdvance = 0` |
| `default` | `householdmembers` | `game\Inn\Intro.rpy` | `134` | `default householdmembers = 4` |
| `default` | `tavernvisitors` | `game\Inn\Intro.rpy` | `135` | `default tavernvisitors = 40` |
| `default` | `productnum` | `game\Inn\Intro.rpy` | `136` | `default productnum = 200` |
| `default` | `winenum` | `game\Inn\Intro.rpy` | `137` | `default winenum = 100` |
| `default` | `tavernfame` | `game\Inn\Intro.rpy` | `138` | `default tavernfame = 0` |
| `default` | `SloganFixed` | `game\Inn\Intro.rpy` | `139` | `default SloganFixed = 0` |
| `default` | `TavernHole` | `game\Inn\Intro.rpy` | `140` | `default TavernHole = 0` |
| `default` | `TavernGloryHole` | `game\Inn\Intro.rpy` | `141` | `default TavernGloryHole = 0` |
| `default` | `GloryHoleLook` | `game\Inn\Intro.rpy` | `142` | `default GloryHoleLook = 0` |
| `default` | `GloryHoleCurrentStep` | `game\Inn\Intro.rpy` | `143` | `default GloryHoleCurrentStep = 0` |
| `default` | `BlockGloryHoleMenu` | `game\Inn\Intro.rpy` | `144` | `default BlockGloryHoleMenu = 0` |
| `default` | `CockInGloryHole` | `game\Inn\Intro.rpy` | `145` | `default CockInGloryHole = 0` |
| `default` | `CheatMoneyGrab` | `game\Inn\Intro.rpy` | `146` | `default CheatMoneyGrab = 0` |
| `default` | `PlayerChoresWeek` | `game\Inn\Intro.rpy` | `147` | `default PlayerChoresWeek = {}` |
| `default` | `UI_chores` | `game\Inn\Intro.rpy` | `148` | `default UI_chores = {}` |
| `default` | `WeeklyVisitorsTrack` | `game\Inn\Intro.rpy` | `149` | `default WeeklyVisitorsTrack = {}` |
| `default` | `WeeklyChoresLastEvalStamp` | `game\Inn\Intro.rpy` | `150` | `default WeeklyChoresLastEvalStamp = ""` |
| `default` | `CurDay` | `game\Inn\Intro.rpy` | `151` | `default CurDay = {}` |
| `default` | `TotalDay` | `game\Inn\Intro.rpy` | `152` | `default TotalDay = {}` |
| `default` | `ExtraEvents` | `game\Inn\Intro.rpy` | `153` | `default ExtraEvents = ""` |
| `default` | `AllGirlNames` | `game\Inn\Intro.rpy` | `155` | `default AllGirlNames = [` |
| `default` | `amanda` | `game\Inn\Intro.rpy` | `169` | `default amanda = {}` |
| `default` | `AmandaVar` | `game\Inn\Intro.rpy` | `170` | `default AmandaVar = {}` |
| `default` | `amandaEvents` | `game\Inn\Intro.rpy` | `171` | `default amandaEvents = []` |
| `default` | `BeckyVar` | `game\Inn\Intro.rpy` | `172` | `default BeckyVar = {}` |
| `default` | `ClaraVar` | `game\Inn\Intro.rpy` | `173` | `default ClaraVar = {}` |
| `default` | `GeorgettVar` | `game\Inn\Intro.rpy` | `174` | `default GeorgettVar = {}` |
| `default` | `LizaVar` | `game\Inn\Intro.rpy` | `175` | `default LizaVar = {}` |
| `default` | `SandraVar` | `game\Inn\Intro.rpy` | `176` | `default SandraVar = {}` |
| `default` | `MelissaVar` | `game\Inn\Intro.rpy` | `177` | `default MelissaVar = {}` |
| `default` | `IrmaVar` | `game\Inn\Intro.rpy` | `178` | `default IrmaVar = {}` |
| `default` | `Friends` | `game\Inn\Intro.rpy` | `179` | `default Friends = {}` |
| `default` | `TalkedToday` | `game\Inn\Intro.rpy` | `180` | `default TalkedToday = {}` |
| `default` | `FlirtedToday` | `game\Inn\Intro.rpy` | `181` | `default FlirtedToday = {}` |
| `default` | `GiftedToday` | `game\Inn\Intro.rpy` | `182` | `default GiftedToday = {}` |
| `default` | `AskedToday` | `game\Inn\Intro.rpy` | `183` | `default AskedToday = {}` |
| `default` | `GiftPreferences` | `game\Inn\Intro.rpy` | `184` | `default GiftPreferences = {}` |
| `default` | `otkroven` | `game\Inn\Intro.rpy` | `185` | `default otkroven = {}` |
| `default` | `neshlush` | `game\Inn\Intro.rpy` | `186` | `default neshlush = {}` |
| `default` | `FightLevel` | `game\Inn\Intro.rpy` | `187` | `default FightLevel = {"you": 1}` |
| `default` | `HarassInstructions` | `game\Inn\Intro.rpy` | `188` | `default HarassInstructions = {}` |
| `default` | `waitress` | `game\Inn\Intro.rpy` | `189` | `default waitress = {}` |
| `default` | `dressdefault` | `game\Inn\Intro.rpy` | `190` | `default dressdefault = {}` |
| `default` | `topdressdef` | `game\Inn\Intro.rpy` | `191` | `default topdressdef = {}` |
| `default` | `bottomdressdef` | `game\Inn\Intro.rpy` | `192` | `default bottomdressdef = {}` |
| `default` | `bradef` | `game\Inn\Intro.rpy` | `193` | `default bradef = {}` |
| `default` | `pantiesdef` | `game\Inn\Intro.rpy` | `194` | `default pantiesdef = {}` |
| `default` | `legsdef` | `game\Inn\Intro.rpy` | `195` | `default legsdef = {}` |
| `default` | `shoesdef` | `game\Inn\Intro.rpy` | `196` | `default shoesdef = {}` |
| `default` | `jobHallAvail` | `game\Inn\Intro.rpy` | `197` | `default jobHallAvail = {}` |
| `default` | `jobkitchen` | `game\Inn\Intro.rpy` | `198` | `default jobkitchen = {}` |
| `default` | `jobcleaning` | `game\Inn\Intro.rpy` | `199` | `default jobcleaning = {}` |
| `default` | `jobwaitress` | `game\Inn\Intro.rpy` | `200` | `default jobwaitress = {}` |
| `default` | `jobkitchentomorrow` | `game\Inn\Intro.rpy` | `201` | `default jobkitchentomorrow = {}` |
| `default` | `jobcleaningtomorrow` | `game\Inn\Intro.rpy` | `202` | `default jobcleaningtomorrow = {}` |
| `default` | `jobwaitresstomorrow` | `game\Inn\Intro.rpy` | `203` | `default jobwaitresstomorrow = {}` |
| `default` | `jobWhoreAvail` | `game\Inn\Intro.rpy` | `204` | `default jobWhoreAvail = {}` |
| `default` | `jobGloryHoleAvail` | `game\Inn\Intro.rpy` | `205` | `default jobGloryHoleAvail = {}` |
| `default` | `jobwhore` | `game\Inn\Intro.rpy` | `206` | `default jobwhore = {}` |
| `default` | `jobgloryhole` | `game\Inn\Intro.rpy` | `207` | `default jobgloryhole = {}` |
| `default` | `jobwhoreTommorow` | `game\Inn\Intro.rpy` | `208` | `default jobwhoreTommorow = {}` |
| `default` | `jobgloryholeTommorow` | `game\Inn\Intro.rpy` | `209` | `default jobgloryholeTommorow = {}` |
| `default` | `BlindPirateMarketEventSeen` | `game\Inn\MarketPlace.rpy` | `124` | `default BlindPirateMarketEventSeen = 0` |
| `default` | `BlindPirateBreakfastPending` | `game\Inn\MarketPlace.rpy` | `125` | `default BlindPirateBreakfastPending = 0` |
| `default` | `WerecatVar` | `game\Inn\MelissaWerecatQuest.rpy` | `1` | `default WerecatVar = {` |
| `default` | `HouseholdMorningState` | `game\Inn\menu_tavernstat.rpy` | `1` | `default HouseholdMorningState = {}` |
| `default` | `TavernReportSelectedPerson` | `game\Inn\menu_tavernstat.rpy` | `764` | `default TavernReportSelectedPerson = ""` |
| `default` | `active_module_kind` | `game\Inn\ModuleRuntime.rpy` | `1` | `default active_module_kind = ""` |
| `default` | `active_module_return_label` | `game\Inn\ModuleRuntime.rpy` | `2` | `default active_module_return_label = ""` |
| `default` | `active_module_return_room` | `game\Inn\ModuleRuntime.rpy` | `3` | `default active_module_return_room = ""` |
| `default` | `active_module_actor` | `game\Inn\ModuleRuntime.rpy` | `4` | `default active_module_actor = ""` |
| `default` | `CurrentRoom` | `game\Inn\my_layouts\main_layout.rpy` | `1` | `default CurrentRoom = None` |
| `default` | `current_action_title` | `game\Inn\my_layouts\main_layout.rpy` | `2` | `default current_action_title = "Actions"` |
| `default` | `current_action_content` | `game\Inn\my_layouts\main_layout.rpy` | `3` | `default current_action_content = None` |
| `default` | `current_action_items` | `game\Inn\my_layouts\main_layout.rpy` | `4` | `default current_action_items = []` |
| `default` | `current_girl_key` | `game\Inn\my_layouts\main_layout.rpy` | `5` | `default current_girl_key = ""` |
| `default` | `current_object_id` | `game\Inn\my_layouts\main_layout.rpy` | `6` | `default current_object_id = ""` |
| `default` | `current_room_code` | `game\Inn\my_layouts\main_layout.rpy` | `7` | `default current_room_code = ""` |
| `default` | `scene_image` | `game\Inn\my_layouts\main_layout.rpy` | `8` | `default scene_image = ""` |
| `default` | `UI_mode` | `game\Inn\my_layouts\main_layout.rpy` | `9` | `default UI_mode = "scene"` |
| `default` | `UI_selected_char` | `game\Inn\my_layouts\main_layout.rpy` | `10` | `default UI_selected_char = ""` |
| `default` | `main_ui_inventory_dropdown_open` | `game\Inn\my_layouts\main_layout.rpy` | `11` | `default main_ui_inventory_dropdown_open = False` |
| `default` | `NAVIGATION_ONLY_MODE` | `game\Inn\NavigationOnlyMode.rpy` | `1` | `default NAVIGATION_ONLY_MODE = False` |
| `default` | `NextDayReportTitle` | `game\Inn\NextDay.rpy` | `2` | `default NextDayReportTitle = ""` |
| `default` | `NextDayReportBody` | `game\Inn\NextDay.rpy` | `3` | `default NextDayReportBody = ""` |
| `default` | `RelationshipLevels` | `game\Inn\NPCRelationshipLevels.rpy` | `1` | `default RelationshipLevels = {}` |
| `default` | `NPCSchedules` | `game\Inn\NPCScheduleModel.rpy` | `1` | `default NPCSchedules = {}` |
| `default` | `Result` | `game\Inn\PartEventGirlReactionTalk.rpy` | `1` | `default Result = ""` |
| `default` | `tavern_event_panel_raw_text` | `game\Inn\PartEventYourFirstReaction.rpy` | `1` | `default tavern_event_panel_raw_text = ""` |
| `default` | `tavern_event_pages` | `game\Inn\PartEventYourFirstReaction.rpy` | `2` | `default tavern_event_pages = []` |
| `default` | `tavern_event_page_index` | `game\Inn\PartEventYourFirstReaction.rpy` | `3` | `default tavern_event_page_index = 0` |
| `default` | `tavern_event_next_title` | `game\Inn\PartEventYourFirstReaction.rpy` | `4` | `default tavern_event_next_title = ""` |
| `default` | `tavern_event_next_items` | `game\Inn\PartEventYourFirstReaction.rpy` | `5` | `default tavern_event_next_items = []` |
| `default` | `panel_paged_raw_text` | `game\Inn\PartEventYourFirstReaction.rpy` | `6` | `default panel_paged_raw_text = ""` |
| `default` | `panel_paged_pages` | `game\Inn\PartEventYourFirstReaction.rpy` | `7` | `default panel_paged_pages = []` |
| `default` | `panel_paged_page_index` | `game\Inn\PartEventYourFirstReaction.rpy` | `8` | `default panel_paged_page_index = 0` |
| `default` | `panel_paged_next_title` | `game\Inn\PartEventYourFirstReaction.rpy` | `9` | `default panel_paged_next_title = ""` |
| `default` | `panel_paged_next_items` | `game\Inn\PartEventYourFirstReaction.rpy` | `10` | `default panel_paged_next_items = []` |
| `default` | `panel_paged_style` | `game\Inn\PartEventYourFirstReaction.rpy` | `11` | `default panel_paged_style = "plain"` |
| `default` | `panel_paged_pending_text` | `game\Inn\PartEventYourFirstReaction.rpy` | `12` | `default panel_paged_pending_text = ""` |
| `default` | `panel_paged_pending_title` | `game\Inn\PartEventYourFirstReaction.rpy` | `13` | `default panel_paged_pending_title = ""` |
| `default` | `panel_paged_pending_items` | `game\Inn\PartEventYourFirstReaction.rpy` | `14` | `default panel_paged_pending_items = []` |
| `default` | `panel_paged_pending_style` | `game\Inn\PartEventYourFirstReaction.rpy` | `15` | `default panel_paged_pending_style = "plain"` |
| `default` | `player_inventory_view_mode` | `game\Inn\PlayerCard.rpy` | `1` | `default player_inventory_view_mode = "profile"` |
| `default` | `player_inventory_view_section` | `game\Inn\PlayerCard.rpy` | `2` | `default player_inventory_view_section = ""` |
| `default` | `player_inventory_view_item` | `game\Inn\PlayerCard.rpy` | `3` | `default player_inventory_view_item = ""` |
| `default` | `player_card_inventory_origin` | `game\Inn\PlayerCard.rpy` | `4` | `default player_card_inventory_origin = "profile"` |
| `default` | `PortStreetsBottleSpawnDay` | `game\Inn\PortStreets.rpy` | `2` | `default PortStreetsBottleSpawnDay = -1` |
| `default` | `PortStreetsBottlePresent` | `game\Inn\PortStreets.rpy` | `3` | `default PortStreetsBottlePresent = 0` |
| `default` | `sexacts` | `game\Inn\PregnancyCheck.rpy` | `6` | `default sexacts = {}` |
| `default` | `ConceptionChance` | `game\Inn\PregnancyCheck.rpy` | `7` | `default ConceptionChance = {}` |
| `default` | `cametoday_npc` | `game\Inn\PregnancyCheck.rpy` | `8` | `default cametoday_npc = {}` |
| `default` | `sluttiness` | `game\Inn\PregnancyCheck.rpy` | `9` | `default sluttiness = {}` |
| `default` | `cuminside` | `game\Inn\PregnancyCheck.rpy` | `10` | `default cuminside = {}` |
| `default` | `roomFirstVisit` | `game\Inn\RoomTemplate.rpy` | `1` | `default roomFirstVisit = {}` |
| `default` | `ShedNoticeText` | `game\Inn\Shed.rpy` | `1` | `default ShedNoticeText = ""` |
| `default` | `ShedNoticePending` | `game\Inn\Shed.rpy` | `2` | `default ShedNoticePending = False` |
| `default` | `ShedBucketFound` | `game\Inn\Shed.rpy` | `3` | `default ShedBucketFound = 0` |
| `default` | `SoapExpireDay` | `game\Inn\SoapCraftAndAtticItems.rpy` | `1` | `default SoapExpireDay = 0` |
| `default` | `SoapAshBarrelInstalled` | `game\Inn\SoapCraftAndAtticItems.rpy` | `2` | `default SoapAshBarrelInstalled = 0` |
| `default` | `SoapAshBarrelReadyDay` | `game\Inn\SoapCraftAndAtticItems.rpy` | `3` | `default SoapAshBarrelReadyDay = 0` |
| `default` | `SoapPendingBatches` | `game\Inn\SoapCraftAndAtticItems.rpy` | `4` | `default SoapPendingBatches = []` |
| `default` | `SoapStoredBatches` | `game\Inn\SoapCraftAndAtticItems.rpy` | `5` | `default SoapStoredBatches = []` |
| `default` | `SoapLookBonusUntilDay` | `game\Inn\SoapCraftAndAtticItems.rpy` | `6` | `default SoapLookBonusUntilDay = -1` |
| `default` | `SoapRequestQueue` | `game\Inn\SoapCraftAndAtticItems.rpy` | `7` | `default SoapRequestQueue = {}` |
| `default` | `HouseholdSoapSampleIntroDone` | `game\Inn\SoapCraftAndAtticItems.rpy` | `8` | `default HouseholdSoapSampleIntroDone = 0` |
| `default` | `HouseholdSoapSampleGiven` | `game\Inn\SoapCraftAndAtticItems.rpy` | `9` | `default HouseholdSoapSampleGiven = {}` |
| `default` | `HouseholdSoapLastBatchProfile` | `game\Inn\SoapCraftAndAtticItems.rpy` | `10` | `default HouseholdSoapLastBatchProfile = {}` |
| `default` | `AtticLootFound` | `game\Inn\SoapCraftAndAtticItems.rpy` | `11` | `default AtticLootFound = 0` |
| `default` | `AtticSupplyLootFound` | `game\Inn\SoapCraftAndAtticItems.rpy` | `12` | `default AtticSupplyLootFound = 0` |
| `default` | `UpstairsRoomSearchState` | `game\Inn\SoapCraftAndAtticItems.rpy` | `13` | `default UpstairsRoomSearchState = {}` |
| `default` | `RustyHunterRifleLoadedAmmo` | `game\Inn\SoapCraftAndAtticItems.rpy` | `14` | `default RustyHunterRifleLoadedAmmo = ""` |
| `default` | `dayspassed` | `game\Inn\StoryEventRuntime.rpy` | `1` | `default dayspassed = 0` |
| `default` | `active_event` | `game\Inn\StoryEventRuntime.rpy` | `3` | `default active_event = None` |
| `default` | `random_events` | `game\Inn\StoryEventRuntime.rpy` | `4` | `default random_events = []` |
| `default` | `story_events` | `game\Inn\StoryEventRuntime.rpy` | `5` | `default story_events = []` |
| `default` | `tavern_work_events` | `game\Inn\StoryEventRuntime.rpy` | `6` | `default tavern_work_events = []` |
| `default` | `availEvents` | `game\Inn\StoryEventRuntime.rpy` | `8` | `default availEvents = {}` |
| `default` | `evalTime` | `game\Inn\StoryEventRuntime.rpy` | `9` | `default evalTime = None` |
| `default` | `thread` | `game\Inn\StoryEventRuntime.rpy` | `10` | `default thread = None` |
| `default` | `eventLocations` | `game\Inn\StoryEventRuntime.rpy` | `11` | `default eventLocations = set()` |
| `default` | `eventPeople` | `game\Inn\StoryEventRuntime.rpy` | `12` | `default eventPeople = set()` |
| `default` | `eventTalk` | `game\Inn\StoryEventRuntime.rpy` | `13` | `default eventTalk = set()` |
| `default` | `eventOptions` | `game\Inn\StoryEventRuntime.rpy` | `14` | `default eventOptions = set()` |
| `default` | `eventItems` | `game\Inn\StoryEventRuntime.rpy` | `15` | `default eventItems = set()` |
| `default` | `story_thread_levels` | `game\Inn\StoryEventRuntime.rpy` | `16` | `default story_thread_levels = {}` |
| `default` | `amanda_story_pending` | `game\Inn\StoryEventRuntime.rpy` | `17` | `default amanda_story_pending = ""` |
| `define` | `amandaThreadList` | `game\Inn\StoryEventRuntime.rpy` | `819` | `define amandaThreadList = [` |
| `define` | `melissaThreadList` | `game\Inn\StoryEventRuntime.rpy` | `837` | `define melissaThreadList = [` |
| `define` | `sandraThreadList` | `game\Inn\StoryEventRuntime.rpy` | `868` | `define sandraThreadList = [` |
| `define` | `claraThreadList` | `game\Inn\StoryEventRuntime.rpy` | `878` | `define claraThreadList = [` |
| `define` | `beckyThreadList` | `game\Inn\StoryEventRuntime.rpy` | `883` | `define beckyThreadList = []` |
| `define` | `lizaThreadList` | `game\Inn\StoryEventRuntime.rpy` | `884` | `define lizaThreadList = []` |
| `define` | `georgettThreadList` | `game\Inn\StoryEventRuntime.rpy` | `885` | `define georgettThreadList = []` |
| `define` | `threadListsByGirl` | `game\Inn\StoryEventRuntime.rpy` | `887` | `define threadListsByGirl = {` |
| `define` | `threadList` | `game\Inn\StoryEventRuntime.rpy` | `897` | `define threadList = (` |
| `define` | `threadData` | `game\Inn\StoryEventRuntime.rpy` | `907` | `define threadData = loadThreadData(threadList)` |
| `default` | `threads` | `game\Inn\StoryEventRuntime.rpy` | `908` | `default threads = createThreads()` |
| `default` | `BedroomDoorStates` | `game\Inn\TavernBedroomDoors.rpy` | `1` | `default BedroomDoorStates = {}` |
| `default` | `TavernHelpPage` | `game\Inn\TavernHelp.rpy` | `40` | `default TavernHelpPage = 0` |
| `default` | `fire_state` | `game\Inn\TavernKitchen.rpy` | `1` | `default fire_state = 0` |
| `default` | `hot_water_state` | `game\Inn\TavernKitchen.rpy` | `2` | `default hot_water_state = 0` |
| `default` | `TavernKitchenNoticeText` | `game\Inn\TavernKitchen.rpy` | `4` | `default TavernKitchenNoticeText = ""` |
| `default` | `TavernKitchenNoticePending` | `game\Inn\TavernKitchen.rpy` | `5` | `default TavernKitchenNoticePending = False` |
| `default` | `TavernKitchenSavedText` | `game\Inn\TavernKitchen.rpy` | `6` | `default TavernKitchenSavedText = ""` |
| `default` | `BeckyKitchenVisitActive` | `game\Inn\TavernKitchen.rpy` | `7` | `default BeckyKitchenVisitActive = 0` |
| `default` | `BreakfastToday` | `game\Inn\TavernKitchen.rpy` | `8` | `default BreakfastToday = False` |
| `default` | `TavernBreakfastLastDay` | `game\Inn\TavernKitchen.rpy` | `9` | `default TavernBreakfastLastDay = -1` |
| `default` | `TavernBreakfastDay` | `game\Inn\TavernKitchen.rpy` | `10` | `default TavernBreakfastDay = -1` |
| `default` | `TavernBreakfastSoapAnnouncedDay` | `game\Inn\TavernKitchen.rpy` | `11` | `default TavernBreakfastSoapAnnouncedDay = -1` |
| `default` | `TavernBreakfastBarberTalkDay` | `game\Inn\TavernKitchen.rpy` | `12` | `default TavernBreakfastBarberTalkDay = -1` |
| `default` | `TavernBreakfastEventActive` | `game\Inn\TavernKitchen.rpy` | `13` | `default TavernBreakfastEventActive = False` |
| `default` | `TavernSundayDinnerLastDay` | `game\Inn\TavernKitchen.rpy` | `14` | `default TavernSundayDinnerLastDay = -1` |
| `default` | `TavernSundayDinnerBarberTalkDay` | `game\Inn\TavernKitchen.rpy` | `15` | `default TavernSundayDinnerBarberTalkDay = -1` |
| `default` | `TavernBreakfastSpicyDrinkDay` | `game\Inn\TavernKitchen.rpy` | `16` | `default TavernBreakfastSpicyDrinkDay = -1` |
| `default` | `TavernSundayDinnerSpicyDrinkDay` | `game\Inn\TavernKitchen.rpy` | `17` | `default TavernSundayDinnerSpicyDrinkDay = -1` |
| `default` | `KitchenWildFoodStock` | `game\Inn\TavernKitchen.rpy` | `18` | `default KitchenWildFoodStock = {}` |
| `default` | `KitchenFoodEffects` | `game\Inn\TavernKitchen.rpy` | `19` | `default KitchenFoodEffects = {}` |
| `default` | `TavernBreakfastGeorgetteLizaPending` | `game\Inn\TavernKitchen.rpy` | `20` | `default TavernBreakfastGeorgetteLizaPending = 0` |
| `default` | `TavernClosed` | `game\Inn\TavernMain.rpy` | `1` | `default TavernClosed = ""` |
| `default` | `TavernEventOngoing` | `game\Inn\TavernMain.rpy` | `3` | `default TavernEventOngoing = ""` |
| `default` | `GeorgettAvail` | `game\Inn\TavernMain.rpy` | `4` | `default GeorgettAvail = 0` |
| `default` | `LizaAvail` | `game\Inn\TavernMain.rpy` | `5` | `default LizaAvail = 0` |
| `default` | `TavernMainBlockEvents` | `game\Inn\TavernMain.rpy` | `171` | `default TavernMainBlockEvents = 0` |
| `default` | `TavernMainObjectMenuId` | `game\Inn\TavernMain.rpy` | `172` | `default TavernMainObjectMenuId = ""` |
| `default` | `TavernMyRoomAtticHatchFound` | `game\Inn\TavernMyRoomAtticHatch001.rpy` | `1` | `default TavernMyRoomAtticHatchFound = 0` |
| `default` | `TavernRooms` | `game\Inn\TavernRooms.rpy` | `1` | `default TavernRooms = []` |
| `default` | `HorseSaddled` | `game\Inn\TavernStable.rpy` | `1` | `default HorseSaddled = 0` |
| `default` | `HorsePurchasePrice` | `game\Inn\TavernStable.rpy` | `2` | `default HorsePurchasePrice = 0` |
| `default` | `TownRooms` | `game\Inn\TownRooms.rpy` | `1` | `default TownRooms = []` |
| `default` | `WerecatNPCState` | `game\Inn\WerecatNPC.rpy` | `1` | `default WerecatNPCState = {` |
| `define` | `config.name` | `game\options.rpy` | `15` | `define config.name = _("Tractir")` |
| `define` | `gui.show_name` | `game\options.rpy` | `22` | `define gui.show_name = True` |
| `define` | `config.version` | `game\options.rpy` | `27` | `define config.version = "1.0"` |
| `define` | `gui.about` | `game\options.rpy` | `33` | `define gui.about = _p("""` |
| `define` | `build.name` | `game\options.rpy` | `41` | `define build.name = "Tractir"` |
| `define` | `config.has_sound` | `game\options.rpy` | `50` | `define config.has_sound = True` |
| `define` | `config.has_music` | `game\options.rpy` | `51` | `define config.has_music = True` |
| `define` | `config.has_voice` | `game\options.rpy` | `52` | `define config.has_voice = True` |
| `define` | `config.autosave_frequency` | `game\options.rpy` | `53` | `define config.autosave_frequency = 15` |
| `define` | `config.autosave_on_choice` | `game\options.rpy` | `54` | `define config.autosave_on_choice = True` |
| `define` | `config.autosave_on_input` | `game\options.rpy` | `55` | `define config.autosave_on_input = True` |
| `define` | `config.enter_transition` | `game\options.rpy` | `80` | `define config.enter_transition = dissolve` |
| `define` | `config.exit_transition` | `game\options.rpy` | `81` | `define config.exit_transition = dissolve` |
| `define` | `config.intra_transition` | `game\options.rpy` | `86` | `define config.intra_transition = dissolve` |
| `define` | `config.after_load_transition` | `game\options.rpy` | `91` | `define config.after_load_transition = None` |
| `define` | `config.end_game_transition` | `game\options.rpy` | `96` | `define config.end_game_transition = None` |
| `define` | `config.window` | `game\options.rpy` | `113` | `define config.window = "auto"` |
| `define` | `config.window_show_transition` | `game\options.rpy` | `118` | `define config.window_show_transition = Dissolve(.2)` |
| `define` | `config.window_hide_transition` | `game\options.rpy` | `119` | `define config.window_hide_transition = Dissolve(.2)` |
| `default` | `preferences.text_cps` | `game\options.rpy` | `127` | `default preferences.text_cps = 0` |
| `default` | `preferences.afm_time` | `game\options.rpy` | `133` | `default preferences.afm_time = 15` |
| `define` | `config.save_directory` | `game\options.rpy` | `150` | `define config.save_directory = "Tractir-1748029397"` |
| `define` | `config.window_icon` | `game\options.rpy` | `157` | `define config.window_icon = "gui/window_icon.png"` |
| `define` | `config.narrator_menu` | `game\screens.rpy` | `310` | `define config.narrator_menu = True` |
| `define` | `quick_menu` | `game\screens.rpy` | `370` | `define quick_menu = False` |
| `define` | `gui.history_allow_tags` | `game\screens.rpy` | `1103` | `define gui.history_allow_tags = set()` |
| `define` | `config.nvl_list_length` | `game\screens.rpy` | `1524` | `define config.nvl_list_length = gui.nvl_list_length` |
