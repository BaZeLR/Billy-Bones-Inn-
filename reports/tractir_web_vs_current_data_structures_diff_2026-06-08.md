# Data Structure Diff: Tractir Web Snapshot vs Current Development

Generated: 2026-06-08T13:48:15

## Scope

- Current development: `C:\Users\blank\Documents\Ren'Py_Projects\Tractir\game`
- Web snapshot: `C:\Users\blank\Documents\Ren'Py_Projects\Tractir-dists\Tractir-web\game`
- Includes `.rpy`, `.rpym`, `.py`, `.json`, `.csv`, `.tsv` files that appear to own data structures, defaults, definitions, classes, registries, schedules, or managers.
- Excludes compiled/cache/save/translation noise: `cache/`, `saves/`, `__pycache__/`, `tl/`, `.rpyc`, `.rpymc`, `.pyc`.
- Full CSV: `C:\Users\blank\Documents\Ren'Py_Projects\Tractir\reports\tractir_web_vs_current_data_structures_diff_2026-06-08.csv`

## Summary

| Status | Count |
|---|---:|
| modified | 300 |
| current_only | 21 |
| web_only | 5 |

## Category Counts

| Category | Modified | Current only | Web only |
|---|---:|---:|---:|
| people_npc | 163 | 16 | 4 |
| schedules | 49 | 12 | 1 |
| events_threads | 86 | 10 | 4 |
| rooms_objects | 170 | 16 | 1 |
| items_inventory_clothes | 108 | 4 | 0 |
| calendar_time | 32 | 1 | 2 |
| player_state | 123 | 5 | 2 |
| combat_enemies | 36 | 0 | 1 |
| media_display_data | 64 | 2 | 2 |
| json_data | 6 | 11 | 0 |
| other_structure | 7 | 1 | 1 |

## Priority Data-Structure Differences

| Status | Categories | Path | Current size | Web size | Symbol additions in current | Symbols only in web |
|---|---|---|---:|---:|---|---|
| modified | calendar_time;people_npc;player_state;rooms_objects | `Inn/PlayerChoresSystem.rpy` | 27446 | 25572 |  |  |
| current_only | events_threads;rooms_objects;schedules | `Inn/TavernRandomEvents.rpy` | 11360 |  | class:TavernWorkEventDefinition;default:TavernEventReportRows;default:TavernPlayedEventsToday;define:tavern_work_events_by_type;define:tavern_work_random_type_order;define:tavern_work_type_chances;function:__init__;function:can_schedule;fun |  |
| modified | items_inventory_clothes | `Items/Clothes/InitDressDesc.rpy` | 15995 | 15887 | default:bottomdress;default:bottomdressdef;default:bottomraised;default:bra;default:bradef;default:dressdefault;default:legs;default:legsdef;default:panties;default:pantiesdef;default:shoes;default:shoesdef;default:topdress;default:topdress |  |
| modified | items_inventory_clothes;rooms_objects | `Items/Core/GameItem.rpy` | 4911 | 4499 |  |  |
| modified | combat_enemies;items_inventory_clothes;rooms_objects | `Items/Core/GameItems.rpy` | 5204 | 4848 |  |  |
| modified | calendar_time;events_threads;people_npc;player_state | `NPC/Girls/Amanda/InitAmanda.rpy` | 12285 | 11230 |  |  |
| modified | people_npc;player_state;rooms_objects | `NPC/Girls/Amanda/InitAmandaLizaTalkItems.rpy` | 39971 | 39584 |  |  |
| modified | calendar_time;items_inventory_clothes;people_npc;player_state;rooms_objects;schedules | `NPC/Girls/Becky/InitBecky.rpy` | 9951 | 8847 | class:Becky;function:__init__ |  |
| modified | combat_enemies;events_threads;people_npc;rooms_objects | `NPC/Girls/Clara/InitClara.rpy` | 27244 | 27104 | class:Clara;function:__init__ | function:clara_booklet_market_thread_num;function:clara_market_spy_day_available;function:clara_market_spy_night_available;function:clara_market_story_caption;function:clara_market_story_label |
| modified | items_inventory_clothes;people_npc;player_state | `NPC/Girls/Irma/InitIrma.rpy` | 6444 | 7328 | class:Irma;function:__init__ |  |
| modified | people_npc;rooms_objects;schedules | `NPC/Girls/Melissa/InitMelissa.rpy` | 18289 | 9273 | class:MelissaData;class:MelissaInfo;default:Melissa;define:MelissaStaticData;function:__init__;function:ensure_story_defaults;function:initialize_new_game_state;function:install_schedule;function:melissa_story_defaults;function:reset_daily; |  |
| modified | calendar_time;items_inventory_clothes;people_npc;player_state;rooms_objects;schedules | `NPC/Girls/Sandra/InitSandra.rpy` | 31973 | 6492 | class:SandraData;class:SandraInfo;default:Sandra;define:SandraStaticData;function:__init__;function:change_fear;function:change_mana;function:daily_mana_update;function:ensure_story_defaults;function:final_reward_done;function:first_month_p |  |
| current_only | events_threads;people_npc;player_state;rooms_objects | `NPC/Girls/Sandra/SandraEvents.rpy` | 11648 |  | label:SandraSexEngine;label:SandraWeek5WakeEvent;label:SandraWeeklyEvaluationScene;label:TavernSandraNightThanksScene;label:sandraWeeklyEvaluation_0;label:sandraWeeklyEvaluation_1;label:sandraWeeklyEvaluation_2;label:sandraWeeklyEvaluation_ |  |
| web_only | events_threads;people_npc | `NPC/Girls/Sandra/SandraWeek5WakeEvent.rpy` |  | 10984 |  | function:sandra_week5_apply_step_gains;function:sandra_week5_scene_picture_path;function:sandra_week5_talk_picture_path;function:sandra_weekly_wake_step;function:sandra_weekly_wake_target_label;function:sandra_weekly_wake_thread;label:Sandr |
| modified | people_npc;player_state | `NPC/Secondary/InitSecondaryNPC.rpy` | 22903 | 13833 | class:Alber;class:Draupnir;class:Eddie;class:Francheska;class:Luisa;class:Mongol;class:Robin;class:Sergio;class:Zimmer;default:LuisaVar;default:SergioVar;function:__init__;function:init_secondary_npc_profiles;function:secondary_npc_default_ | default:alber;default:draupnir;default:eddie;default:fran;default:gerhard;default:mongol;default:robin;default:zimmer;function:eddie_grocery_morning_active;function:register_secondary_npc_object;function:register_secondary_npc_objects;funct |
| modified | combat_enemies;events_threads;rooms_objects | `Town/RandomTownEvents.rpy` | 44236 | 36917 | default:TownStreetCooldowns;default:TownStreetDailyPlan;default:TownStreetFiredLabelsToday;default:TownStreetFiredLocationsToday;function:_screen_text;function:beggar_chance;function:chronicle_allowed;function:chronicle_chance;function:curf |  |
| modified | items_inventory_clothes;player_state;rooms_objects | `Utilities/General/Classes/GameObjects.rpy` | 1083 | 672 |  |  |
| modified | combat_enemies;items_inventory_clothes;rooms_objects | `Utilities/General/Classes/RoomTemplate.rpy` | 18270 | 18002 | function:_minute_value | function:room_hour_in_ranges |
| modified | combat_enemies;events_threads;people_npc;rooms_objects;schedules | `Utilities/General/Classes/StoryEventRuntime.rpy` | 65467 | 69374 | define:melissaThreadList;define:tavernThreadList;label:melissaClaraOverheard_0;label:melissaClaraOverheard_1;label:story_clara_market_booklet_0;label:story_clara_market_booklet_2;label:story_clara_market_booklet_2_direct_follow;label:story_ | class:Event;class:LThreadData;class:LThreadInfo;class:RThreadData;class:RThreadInfo;class:StoryCondition;class:StoryConditionAborted;class:StoryConditionAt;class:StoryConditionCallable;class:StoryConditionCompleted;class:StoryConditionEnabl |
| modified | calendar_time;events_threads;rooms_objects | `Utilities/General/Common/DebugTools.rpy` | 78072 | 26170 | default:DebugBuilderRepairNotesPath;define:DebugBuilderRoomObject;function:_dbg_calendar_set_fields;function:_dbg_calendar_set_weekday;function:debug_builder_correction_notes;function:debug_builder_escape_text;function:debug_builder_event_c |  |
| modified | calendar_time;people_npc;schedules | `Utilities/General/NPC/NPCScheduleModel.rpy` | 41314 | 23995 | class:NPCIntervalScheduleEntry;default:NPCIntervalScheduleLoadErrors;default:NPCIntervalScheduleLoaded;default:NPCIntervalSchedules;function:_npc_interval_schedule_store;function:npc_interval_condition_from_json;function:npc_interval_locati | function:npc_daily_schedule_hour_ranges_for_slot;function:npc_hour_in_ranges |
| modified | items_inventory_clothes;people_npc;rooms_objects;schedules | `Utilities/General/NPC/PeopleRuntime.rpy` | 26552 | 20278 | class:BaseNPC;class:Girl;default:girls;default:secondary_npcs;function:_register_people_lists;function:people_initial_location;function:promote_from_var;function:social_action_allowed;label:InitGameNPCs | function:canFlirt;function:canGift;function:canInteract;function:canTalk;function:friends;function:talkedToday |
| current_only | items_inventory_clothes;player_state | `Utilities/General/Player/Player.rpy` | 32629 |  | class:Player;class:PlayerAppearance;class:PlayerChores;class:PlayerCombat;class:PlayerCondition;class:PlayerEconomy;class:PlayerEquipment;class:PlayerIdentity;class:PlayerIntimacy;class:PlayerInventory;class:PlayerStats;class:PlayerTavernMa |  |
| modified | combat_enemies;items_inventory_clothes;player_state;rooms_objects | `Utilities/General/Screens/PlayerCard.rpy` | 61891 | 60286 | function:player_card_effective_exploration;function:player_card_equipped_armor;function:player_card_equipped_weapon;function:player_card_inventory_count;function:player_card_inventory_ids;function:player_card_owned_dresses;function:player_c | label:PlayerCardReturnToActiveTalk |
| modified | media_display_data | `Utilities/General/Screens/ShowImage.rpy` | 20061 | 25640 |  | function:_media_casefold_lookup |
| modified | items_inventory_clothes;media_display_data;people_npc;player_state;rooms_objects | `Utilities/General/Sex/HarassShowImage.rpy` | 2760 | 4757 |  | function:harass_image_path;function:harass_player_reaction_image_path |
| modified | calendar_time;items_inventory_clothes;player_state;rooms_objects | `Utilities/General/Sex/PlayerIntimacyState.rpy` | 15632 | 16315 |  | default:LastDaySex;default:PlayerArousalReasons;default:PlayerLastCumDay;default:PlayerLastHelpResult;default:PlayerMorningArousalDay;default:PlayerObservedNakedNpcDay;default:PlayerRoomLightClosed;default:PlayerSleepBottomLayer;default:Pla |
| modified | calendar_time;events_threads;people_npc;player_state | `Utilities/General/Sex/WhoreNextDayClients.rpy` | 3405 | 2712 |  |  |
| modified | calendar_time;combat_enemies;rooms_objects;schedules | `Utilities/Time/AdvanceTime.rpy` | 1970 | 2080 | function:advance_time_runtime;label:AdvanceTimeAndRestore | default:LastAdvancedTimeSlots;default:LastTimeAdvanceKind;default:LastTimeAdvanceSource;function:advance_time_slot_runtime;function:mark_time_advance |
| modified | calendar_time | `Utilities/Time/DayToText.rpy` | 678 | 260 |  |  |
| modified | calendar_time;events_threads;items_inventory_clothes;player_state;rooms_objects | `Utilities/Time/NextDay.rpy` | 16425 | 16274 |  | default:SleepWakeHourOverride;default:SleepWakeMinuteOverride |
| modified | calendar_time;combat_enemies;events_threads;people_npc;player_state | `Utilities/Time/NextDay_FinishDayEvents.rpy` | 9894 | 9181 |  |  |
| modified | calendar_time;combat_enemies;events_threads;player_state;rooms_objects | `Utilities/Time/NextDay_NewDayEvents.rpy` | 12972 | 12450 |  |  |
| modified | calendar_time;combat_enemies;events_threads;people_npc;rooms_objects | `Utilities/Time/NextDay_TavernDaily.rpy` | 8480 | 8314 |  |  |
| modified | calendar_time;rooms_objects | `Utilities/Time/TimeChangeMenu.rpy` | 6395 | 7207 | function:_time_current_slot;label:ApplyTimePeriodChange | function:_time_label;label:ApplyHudTimeSkipDays;label:ApplyHudTimeSkipToSlot;label:ApplyTimeSlotChange |
| modified | calendar_time;rooms_objects | `Utilities/Time/TimeTurnSystem.rpy` | 2690 | 2066 | default:BlockTimeAdvance |  |
| modified | calendar_time;events_threads;items_inventory_clothes;json_data;people_npc;player_state;rooms_objects | `script.rpy` | 28540 | 26979 | class:Calendar;default:AmandaVar;default:Arousal;default:AskedToday;default:BeckyVar;default:Breastfeed;default:ChurchDonatedAmount;default:ClaraVar;default:ClientsDayTotal;default:CockInAss;default:CockInMouth;default:CockInPussy;default:C | class:MoonCalendar;function:_cal_advance_date_one_day;function:_cal_apply_counters_and_names;function:_cal_days_before_cycle;function:_cal_days_before_month;function:_cal_days_in_cycle;function:_cal_days_in_month;function:_cal_increment_age |

## Current-Only Structure Files

- `Inn/TavernRandomEvents.rpy` categories=`events_threads;rooms_objects;schedules` size=11360 symbols=`class:TavernWorkEventDefinition;default:TavernEventReportRows;default:TavernPlayedEventsToday;define:tavern_work_events_by_type;define:tavern_work_random_type_order;define:tavern_work_type_chances;function:__init__;funct`
- `Items/Crafting/SoapCrafting.rpy` categories=`events_threads;items_inventory_clothes;people_npc;player_state;rooms_objects` size=17291 symbols=`function:get_available_soap_aromas;label:CraftSoapFinalize;label:CraftSoapPlayerChoice;label:GirlSoapFavorNegotiation;label:GirlSoapRequest;label:RoomTableStartSoap;label:SoapChooseAromas;label:SoapSecondStageFinalize;la`
- `NPC/Girls/Becky/BeckyEvents.rpy` categories=`calendar_time;events_threads;people_npc;player_state;rooms_objects` size=52245 symbols=`class:LThreadData;function:__init__;function:rand_int;label:becky_blackwood_quest_start;label:becky_blackwood_talk_reveal;label:becky_eddie_black_eye;label:becky_home_georgett_visit;label:becky_home_georgett_visit_cum_me`
- `NPC/Girls/Irma/IrmaTailorEvents.rpy` categories=`events_threads;items_inventory_clothes;media_display_data;people_npc;player_state;rooms_objects` size=12074 symbols=`label:IrmaClaraFittingScene;label:IrmaMeasureEndScene;label:IrmaMeasureRoomMenu;label:IrmaMeasureRoomStage;label:IrmaSexSequence;label:IrmaShopFlirtScene`
- `NPC/Girls/Sandra/SandraEvents.rpy` categories=`events_threads;people_npc;player_state;rooms_objects` size=11648 symbols=`label:SandraSexEngine;label:SandraWeek5WakeEvent;label:SandraWeeklyEvaluationScene;label:TavernSandraNightThanksScene;label:sandraWeeklyEvaluation_0;label:sandraWeeklyEvaluation_1;label:sandraWeeklyEvaluation_2;label:san`
- `NPC/Schedules/alber.json` categories=`json_data;people_npc;rooms_objects;schedules` size=1779 symbols=``
- `NPC/Schedules/amanda.json` categories=`json_data;people_npc;rooms_objects;schedules` size=2828 symbols=``
- `NPC/Schedules/becky.json` categories=`json_data;people_npc;rooms_objects;schedules` size=1773 symbols=``
- `NPC/Schedules/clara.json` categories=`events_threads;json_data;people_npc;rooms_objects;schedules` size=2324 symbols=``
- `NPC/Schedules/eddie.json` categories=`json_data;people_npc;schedules` size=1510 symbols=``
- `NPC/Schedules/georgett.json` categories=`json_data;people_npc;rooms_objects;schedules` size=1533 symbols=``
- `NPC/Schedules/irma.json` categories=`items_inventory_clothes;json_data;people_npc;rooms_objects;schedules` size=702 symbols=``
- `NPC/Schedules/liza.json` categories=`json_data;people_npc;rooms_objects;schedules` size=1627 symbols=``
- `NPC/Schedules/melissa.json` categories=`json_data;people_npc;rooms_objects;schedules` size=2708 symbols=``
- `NPC/Schedules/sandra.json` categories=`json_data;people_npc;rooms_objects;schedules` size=3530 symbols=``
- `NPC/Schedules/sergio.json` categories=`json_data;people_npc;schedules` size=721 symbols=``
- `Utilities/General/Events/conditions.rpy` categories=`events_threads` size=19021 symbols=`class:StoryCondition;class:StoryConditionAborted;class:StoryConditionAt;class:StoryConditionCallable;class:StoryConditionCompleted;class:StoryConditionEnabled;class:StoryConditionExpression;class:StoryConditionNotAt;clas`
- `Utilities/General/Events/events.rpy` categories=`events_threads;people_npc;rooms_objects` size=18364 symbols=`class:Event;default:active_event;default:availEvents;default:evalTime;default:eventItems;default:eventLocations;default:eventOptions;default:eventPath;default:eventPeople;default:eventProjectionRows;default:eventRouteHin`
- `Utilities/General/Events/threads.rpy` categories=`events_threads` size=14338 symbols=`class:LThreadData;class:LThreadInfo;class:RThreadData;class:RThreadInfo;class:ThreadData;class:ThreadInfo;class:UThreadData;class:UThreadInfo;function:__init__;function:abort;function:adjustLen;function:advance;function:`
- `Utilities/General/Player/Player.rpy` categories=`items_inventory_clothes;player_state` size=32629 symbols=`class:Player;class:PlayerAppearance;class:PlayerChores;class:PlayerCombat;class:PlayerCondition;class:PlayerEconomy;class:PlayerEquipment;class:PlayerIdentity;class:PlayerIntimacy;class:PlayerInventory;class:PlayerStats;`
- `Utilities/General/Screens/SceneActionPanel.rpy` categories=`events_threads;media_display_data;other_structure;rooms_objects` size=6718 symbols=`function:scene_panel_add_item;function:scene_panel_call_item;function:scene_panel_item;function:scene_panel_jump_item;function:scene_panel_mutate;function:scene_panel_return_item;function:scene_panel_set_item;label:Scene`

## Web-Only Structure Files

- `NPC/Girls/Clara/ClaraEvents.rpy` categories=`calendar_time;events_threads;media_display_data;people_npc;player_state;rooms_objects` size=13528 symbols=`label:ClaraMarketCloakTalk;label:ClaraMarketSecretMerchantBuy;label:ClaraMarketSecretMerchantMenu;label:ClaraMarketSpyDay_0;label:ClaraMarketSpyNight_1;label:ClaraMarketSpyNight_2;label:ClaraMarketSpyNight_2_Mongol`
- `NPC/Girls/Sandra/SandraWeek5WakeEvent.rpy` categories=`events_threads;people_npc` size=10984 symbols=`function:sandra_week5_apply_step_gains;function:sandra_week5_scene_picture_path;function:sandra_week5_talk_picture_path;function:sandra_weekly_wake_step;function:sandra_weekly_wake_target_label;function:sandra_weekly_wak`
- `NPC/Secondary/MongolEvents.rpy` categories=`combat_enemies;events_threads;media_display_data;people_npc` size=12994 symbols=`label:mongolArest_0;label:mongolArest_1;label:mongolArest_2;label:mongolArest_3;label:mongolArest_4`
- `Utilities/General/Common/RandomEngine.rpy` categories=`events_threads;other_structure` size=3249 symbols=`function:procedural_choice;function:procedural_index;function:procedural_randint;function:procedural_seed;function:rand_chance;function:rand_choice;function:rand_event;function:rand_float;function:rand_int;function:rand_`
- `Utilities/General/NPC/GirlObjectRuntime.rpy` categories=`calendar_time;people_npc;player_state;schedules` size=35567 symbols=`class:GirlData;class:GirlInfo;default:clara;default:clarissa;default:georgett;default:girls_data;default:girls_info;default:irma;default:melissa;default:sandra;function:__init__;function:add_corruption;function:add_frien`

## Modified Structure Files

- `Forest/Forest.rpy` categories=`rooms_objects` current=28467 web=33353 current_symbols_only=`function:forest_after_dusk;function:forest_after_dusk_return_text;function:forest_apply_after_dusk_message;function:forest_can_depart_now;function:forest_depart` web_symbols_only=`function:forest_room_has_exit;function:forest_room_has_spawned_item;function:forest_room_spawn_units;function:forest_spawn_menu_caption;label:ForestMenu;label:F`
- `Forest/ForestCave.rpy` categories=`media_display_data;rooms_objects;schedules` current=2995 web=2339 current_symbols_only=`` web_symbols_only=``
- `Forest/ForestClearing.rpy` categories=`media_display_data;rooms_objects;schedules` current=3372 web=2697 current_symbols_only=`` web_symbols_only=``
- `Forest/ForestDarkWoods.rpy` categories=`media_display_data;rooms_objects;schedules` current=2901 web=2218 current_symbols_only=`` web_symbols_only=``
- `Forest/ForestHiddenPath.rpy` categories=`media_display_data;rooms_objects;schedules` current=2846 web=2158 current_symbols_only=`` web_symbols_only=``
- `Forest/ForestLake.rpy` categories=`media_display_data;rooms_objects;schedules` current=3199 web=2544 current_symbols_only=`` web_symbols_only=``
- `Forest/ForestSpring.rpy` categories=`media_display_data;rooms_objects;schedules` current=3264 web=2599 current_symbols_only=`` web_symbols_only=``
- `Forest/ForestWaterfall.rpy` categories=`media_display_data;rooms_objects;schedules` current=2854 web=2174 current_symbols_only=`` web_symbols_only=``
- `Inn/Backyard.rpy` categories=`combat_enemies;rooms_objects;schedules` current=16128 web=17463 current_symbols_only=`label:BackyardBuildActions;label:BackyardObjectMenu;label:BackyardObjectText;label:BackyardRestore` web_symbols_only=`label:BackyardMenu;label:BackyardNativeObjectMenu;label:BackyardNativeObjectText`
- `Inn/CreateTavernEvents.rpy` categories=`combat_enemies;events_threads;rooms_objects` current=1820 web=3003 current_symbols_only=`` web_symbols_only=``
- `Inn/CreateTavernEventsPeriod.rpy` categories=`combat_enemies;events_threads;rooms_objects` current=619 web=1700 current_symbols_only=`` web_symbols_only=``
- `Inn/EventWineForDance.rpy` categories=`events_threads;rooms_objects;schedules` current=7258 web=7282 current_symbols_only=`` web_symbols_only=``
- `Inn/HouseholdMiniEvents.rpy` categories=`combat_enemies;events_threads;people_npc;rooms_objects` current=7024 web=10478 current_symbols_only=`` web_symbols_only=``
- `Inn/HouseholdRuntimeEvents.rpy` categories=`events_threads;people_npc;rooms_objects` current=65205 web=65372 current_symbols_only=`` web_symbols_only=``
- `Inn/Intro.rpy` categories=`calendar_time;combat_enemies;events_threads;items_inventory_clothes;media_display_data;people_npc;player_state;rooms_objects` current=3701 web=15992 current_symbols_only=`` web_symbols_only=`default:AllGirlNames;default:AmandaVar;default:Arousal;default:AskedToday;default:BeckyVar;default:BlessedByEllona;default:BlockGloryHoleMenu;default:BlockTimeA`
- `Inn/Loc.rpy` categories=`events_threads;items_inventory_clothes;player_state;rooms_objects` current=2972 web=2623 current_symbols_only=`` web_symbols_only=``
- `Inn/PlayerChoresSystem.rpy` categories=`calendar_time;people_npc;player_state;rooms_objects` current=27446 web=25572 current_symbols_only=`` web_symbols_only=``
- `Inn/Shed.rpy` categories=`player_state;rooms_objects;schedules` current=11253 web=10631 current_symbols_only=`function:build_shed_action_items;label:ShedRoomActions` web_symbols_only=`function:shed_chopped_wood_count;function:shed_has_any_lumber;function:shed_player_lumber_count;label:ShedMenu;label:ShedSplitWood`
- `Inn/TavernAmandaBed001.rpy` categories=`rooms_objects` current=1496 web=1083 current_symbols_only=`` web_symbols_only=``
- `Inn/TavernAmandaRoom.rpy` categories=`items_inventory_clothes;rooms_objects;schedules` current=30057 web=30517 current_symbols_only=`label:TavernAmandaRoomRestore` web_symbols_only=``
- `Inn/TavernAtic.rpy` categories=`events_threads;media_display_data;rooms_objects;schedules` current=17134 web=16928 current_symbols_only=`label:TavernAticRestore` web_symbols_only=``
- `Inn/TavernBedroomDoors.rpy` categories=`rooms_objects` current=4596 web=4305 current_symbols_only=`` web_symbols_only=``
- `Inn/TavernEmptyRoom.rpy` categories=`media_display_data;rooms_objects;schedules` current=2603 web=2257 current_symbols_only=`` web_symbols_only=``
- `Inn/TavernGloryHole.rpy` categories=`events_threads;people_npc;player_state;rooms_objects` current=26332 web=26088 current_symbols_only=`` web_symbols_only=``
- `Inn/TavernHelp.rpy` categories=`media_display_data;rooms_objects` current=5893 web=5656 current_symbols_only=`` web_symbols_only=``
- `Inn/TavernKitchen.rpy` categories=`events_threads;rooms_objects;schedules` current=158850 web=165404 current_symbols_only=`label:TavernKitchenRefreshBreakfastEvent;label:TavernKitchenRestore` web_symbols_only=`function:tavern_breakfast_call_candidate_ids;function:tavern_breakfast_call_reaction;function:tavern_breakfast_call_result_text;function:tavern_breakfast_called`
- `Inn/TavernKitchenCauldron001.rpy` categories=`rooms_objects` current=1537 web=1125 current_symbols_only=`` web_symbols_only=``
- `Inn/TavernKitchenHearth001.rpy` categories=`player_state;rooms_objects` current=4864 web=4952 current_symbols_only=`` web_symbols_only=``
- `Inn/TavernMain.rpy` categories=`events_threads;people_npc;rooms_objects;schedules` current=32276 web=31217 current_symbols_only=`function:tavern_main_closed_text;function:tavern_main_friday_dance_closed;function:tavern_main_late_closed;function:tavern_main_open_hours_visible;function:tave` web_symbols_only=``
- `Inn/TavernMainBar001.rpy` categories=`calendar_time;events_threads;rooms_objects;schedules` current=6941 web=9248 current_symbols_only=`` web_symbols_only=`function:tavern_bar_clara_melissa_gossip_target;function:tavern_bar_clara_melissa_story_event_available;function:tavern_bar_prepare_clara_melissa_gossip_thread;`
- `Inn/TavernMainBook001.rpy` categories=`rooms_objects` current=7322 web=6910 current_symbols_only=`` web_symbols_only=``
- `Inn/TavernMainFireplace001.rpy` categories=`player_state;rooms_objects` current=4974 web=5068 current_symbols_only=`` web_symbols_only=``
- `Inn/TavernMelissaRoom.rpy` categories=`combat_enemies;events_threads;rooms_objects;schedules` current=13578 web=13158 current_symbols_only=`label:TavernMelissaRoomRestore` web_symbols_only=``
- `Inn/TavernMyRoom.rpy` categories=`combat_enemies;items_inventory_clothes;player_state;rooms_objects;schedules` current=25810 web=26704 current_symbols_only=`label:TavernMyRoomRestore` web_symbols_only=`label:TavernMyRoomToggleLight`
- `Inn/TavernMyRoomAtticHatch001.rpy` categories=`rooms_objects` current=3234 web=2858 current_symbols_only=`` web_symbols_only=``
- `Inn/TavernMyRoomBed001.rpy` categories=`player_state;rooms_objects` current=1930 web=1518 current_symbols_only=`` web_symbols_only=``
- `Inn/TavernMyRoomChest001.rpy` categories=`player_state;rooms_objects` current=2065 web=1653 current_symbols_only=`` web_symbols_only=``
- `Inn/TavernMyRoomWindow001.rpy` categories=`events_threads;rooms_objects` current=3509 web=3261 current_symbols_only=`` web_symbols_only=``
- `Inn/TavernProstClients.rpy` categories=`events_threads;media_display_data;people_npc;player_state;rooms_objects` current=9077 web=8629 current_symbols_only=`` web_symbols_only=``
- `Inn/TavernRooms.rpy` categories=`rooms_objects` current=812 web=400 current_symbols_only=`` web_symbols_only=``
- `Inn/TavernSandraRoom.rpy` categories=`media_display_data;player_state;rooms_objects;schedules` current=13110 web=15382 current_symbols_only=`label:TavernSandraRoomRestore` web_symbols_only=`label:TavernSandraNightThanksScene`
- `Inn/TavernStable.rpy` categories=`rooms_objects` current=15076 web=14799 current_symbols_only=`label:TavernStableRestore` web_symbols_only=``
- `Inn/TavernStorage.rpy` categories=`combat_enemies;events_threads;media_display_data;rooms_objects;schedules` current=3511 web=3190 current_symbols_only=`` web_symbols_only=``
- `Inn/TavernUpstairs.rpy` categories=`events_threads;media_display_data;player_state;rooms_objects;schedules` current=4097 web=3778 current_symbols_only=`` web_symbols_only=``
- `Inn/menu_tavernstat.rpy` categories=`rooms_objects` current=44963 web=42199 current_symbols_only=`function:ensure_default_tavern_jobs` web_symbols_only=``
- `Items/Clothes/BanditCostumeItem.rpy` categories=`items_inventory_clothes;player_state` current=1275 web=863 current_symbols_only=`` web_symbols_only=``
- `Items/Clothes/BlackStockingsItem.rpy` categories=`items_inventory_clothes` current=913 web=501 current_symbols_only=`` web_symbols_only=``
- `Items/Clothes/BourgeoisCostumeItem.rpy` categories=`items_inventory_clothes;player_state` current=1159 web=747 current_symbols_only=`` web_symbols_only=``
- `Items/Clothes/GreenWorkDressItem.rpy` categories=`items_inventory_clothes` current=1371 web=959 current_symbols_only=`` web_symbols_only=``
- `Items/Clothes/InitDressDesc.rpy` categories=`items_inventory_clothes` current=15995 web=15887 current_symbols_only=`default:bottomdress;default:bottomdressdef;default:bottomraised;default:bra;default:bradef;default:dressdefault;default:legs;default:legsdef;default:panties;def` web_symbols_only=``
- `Items/Clothes/MiniDressItem.rpy` categories=`items_inventory_clothes` current=1267 web=855 current_symbols_only=`` web_symbols_only=``
- `Items/Clothes/ModestNiceDressItem.rpy` categories=`items_inventory_clothes` current=1173 web=761 current_symbols_only=`` web_symbols_only=``
- `Items/Clothes/ModestWorkDressItem.rpy` categories=`items_inventory_clothes` current=1427 web=1015 current_symbols_only=`` web_symbols_only=``
- `Items/Clothes/NightshirtItem.rpy` categories=`items_inventory_clothes` current=915 web=503 current_symbols_only=`` web_symbols_only=``
- `Items/Clothes/NobleCostumeItem.rpy` categories=`items_inventory_clothes;player_state` current=1502 web=1090 current_symbols_only=`` web_symbols_only=``
- `Items/Clothes/OpenWorkDressItem.rpy` categories=`items_inventory_clothes` current=1374 web=962 current_symbols_only=`` web_symbols_only=``
- `Items/Clothes/PeasantCostumeItem.rpy` categories=`items_inventory_clothes;player_state` current=1088 web=676 current_symbols_only=`` web_symbols_only=``
- `Items/Clothes/RedStockingsItem.rpy` categories=`items_inventory_clothes` current=927 web=515 current_symbols_only=`` web_symbols_only=``
- `Items/Clothes/SailorCostumeItem.rpy` categories=`items_inventory_clothes;player_state` current=1257 web=845 current_symbols_only=`` web_symbols_only=``
- `Items/Clothes/SimpleBraItem.rpy` categories=`items_inventory_clothes` current=837 web=425 current_symbols_only=`` web_symbols_only=``
- `Items/Clothes/SimplePantiesItem.rpy` categories=`items_inventory_clothes` current=874 web=462 current_symbols_only=`` web_symbols_only=``
- `Items/Clothes/SlutDressItem.rpy` categories=`items_inventory_clothes` current=1486 web=1074 current_symbols_only=`` web_symbols_only=``
- `Items/Clothes/WhiteStockingsItem.rpy` categories=`items_inventory_clothes` current=903 web=491 current_symbols_only=`` web_symbols_only=``
- `Items/Clothes/WorkDressItem.rpy` categories=`items_inventory_clothes` current=1339 web=927 current_symbols_only=`` web_symbols_only=``
- `Items/Clothes/WorkDressZhiletItem.rpy` categories=`items_inventory_clothes` current=1464 web=1052 current_symbols_only=`` web_symbols_only=``
- `Items/Core/CraftingRecipes.rpy` categories=`events_threads;items_inventory_clothes;player_state;rooms_objects` current=35844 web=36765 current_symbols_only=`` web_symbols_only=``
- `Items/Core/GameItem.rpy` categories=`items_inventory_clothes;rooms_objects` current=4911 web=4499 current_symbols_only=`` web_symbols_only=``
- `Items/Core/GameItems.rpy` categories=`combat_enemies;items_inventory_clothes;rooms_objects` current=5204 web=4848 current_symbols_only=`` web_symbols_only=``
- `Items/Crafting/SoapCraftAndAtticItems.rpy` categories=`combat_enemies;items_inventory_clothes;player_state;rooms_objects` current=92717 web=95499 current_symbols_only=`` web_symbols_only=``
- `Items/Resources/BerriesItem.rpy` categories=`items_inventory_clothes` current=1637 web=1225 current_symbols_only=`` web_symbols_only=``
- `Items/Resources/ChoppedWoodItem.rpy` categories=`items_inventory_clothes;rooms_objects` current=1576 web=1514 current_symbols_only=`` web_symbols_only=``
- `Items/Resources/FoodBaleItem.rpy` categories=`items_inventory_clothes` current=901 web=489 current_symbols_only=`` web_symbols_only=``
- `Items/Resources/HoneyCombItem.rpy` categories=`items_inventory_clothes;player_state` current=2143 web=1824 current_symbols_only=`` web_symbols_only=``
- `Items/Resources/LumberItem.rpy` categories=`items_inventory_clothes;player_state;rooms_objects` current=1628 web=1553 current_symbols_only=`` web_symbols_only=``
- `Items/Resources/MushroomItem.rpy` categories=`items_inventory_clothes;rooms_objects` current=1674 web=1262 current_symbols_only=`` web_symbols_only=``
- `Items/Resources/OldAxeItem.rpy` categories=`items_inventory_clothes` current=1279 web=1281 current_symbols_only=`` web_symbols_only=``
- `Items/Resources/TavernHelpBookItem.rpy` categories=`items_inventory_clothes;rooms_objects` current=6915 web=6503 current_symbols_only=`` web_symbols_only=``
- `Items/Resources/WineBarrelItem.rpy` categories=`items_inventory_clothes` current=876 web=464 current_symbols_only=`` web_symbols_only=``
- `Items/Shops/GroceryStoreItems.rpy` categories=`items_inventory_clothes` current=941 web=529 current_symbols_only=`` web_symbols_only=``
- `Items/Shops/HunterClubItems.rpy` categories=`combat_enemies;items_inventory_clothes` current=16880 web=16703 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Amanda/AfterDanceLegare.rpy` categories=`events_threads;people_npc;player_state` current=20738 web=20395 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Amanda/AfterDanceSexLegare.rpy` categories=`media_display_data;people_npc;player_state` current=32683 web=32890 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Amanda/AmandaAI_Bridge.rpy` categories=`events_threads;people_npc;rooms_objects` current=94898 web=95058 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Amanda/AmandaAtGloryHole.rpy` categories=`people_npc;rooms_objects` current=33939 web=34220 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Amanda/AmandaAtHomeCode.rpy` categories=`items_inventory_clothes;people_npc;player_state;rooms_objects` current=32897 web=33486 current_symbols_only=`label:AmandaAtHomeStateDefaults` web_symbols_only=``
- `NPC/Girls/Amanda/AmandaDynamicCommonBlocks.rpy` categories=`people_npc;player_state` current=18785 web=18239 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Amanda/AmandaLegareDanceSequence.rpy` categories=`events_threads;people_npc;player_state` current=8085 web=7600 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Amanda/AmandaLoverSex.rpy` categories=`people_npc;player_state;rooms_objects` current=25481 web=25102 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Amanda/AmandaSexDanceStreet.rpy` categories=`people_npc;player_state;rooms_objects` current=2787 web=2504 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Amanda/EventAmandaLegareCreateDance.rpy` categories=`events_threads;people_npc` current=4620 web=4196 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Amanda/EventAmandaLizettTalk.rpy` categories=`events_threads;people_npc` current=8424 web=8082 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Amanda/EventAmandaLizettTalk2.rpy` categories=`events_threads;people_npc;rooms_objects` current=4252 web=3950 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Amanda/InitAmanda.rpy` categories=`calendar_time;events_threads;people_npc;player_state` current=12285 web=11230 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Amanda/InitAmandaLizaTalkItems.rpy` categories=`people_npc;player_state;rooms_objects` current=39971 web=39584 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Amanda/IntAmandaDance.rpy` categories=`events_threads;media_display_data;people_npc` current=22313 web=23419 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Amanda/IntAmandaDressChange.rpy` categories=`events_threads;items_inventory_clothes;people_npc;rooms_objects;schedules` current=26216 web=26142 current_symbols_only=`label:IntAmandaDressChangeRefresh` web_symbols_only=``
- `NPC/Girls/Amanda/IntAmandaSex.rpy` categories=`items_inventory_clothes;people_npc;player_state` current=57035 web=57896 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Amanda/IntAmandaTalk.rpy` categories=`items_inventory_clothes;people_npc;player_state` current=27585 web=27540 current_symbols_only=`label:IntAmandaTalkRefresh;label:IntAmandaTalkRestore` web_symbols_only=``
- `NPC/Girls/Amanda/ShowAmandaPortrait.rpy` categories=`media_display_data;people_npc;player_state;rooms_objects` current=1072 web=709 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Becky/BeckyEddieJoinFirst.rpy` categories=`media_display_data;people_npc;player_state` current=12626 web=12849 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Becky/BeckyInviteHome.rpy` categories=`people_npc;player_state` current=2079 web=1627 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Becky/BeckyLoversInStore.rpy` categories=`events_threads;people_npc;player_state` current=7037 web=6629 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Becky/BeckyQuestInit.rpy` categories=`events_threads;people_npc` current=4564 web=4186 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Becky/GeorgettBeckyVisit.rpy` categories=`media_display_data;people_npc;player_state` current=14490 web=14422 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Becky/InitBecky.rpy` categories=`calendar_time;items_inventory_clothes;people_npc;player_state;rooms_objects;schedules` current=9951 web=8847 current_symbols_only=`class:Becky;function:__init__` web_symbols_only=``
- `NPC/Girls/Becky/IntBeckyAfterCermon.rpy` categories=`events_threads;people_npc;player_state` current=22198 web=22112 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Becky/IntBeckyDance.rpy` categories=`events_threads;media_display_data;people_npc` current=18144 web=18821 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Becky/IntBeckyDressChange.rpy` categories=`events_threads;items_inventory_clothes;people_npc` current=19455 web=18994 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Becky/IntBeckyGuest.rpy` categories=`media_display_data;people_npc;player_state` current=19045 web=19406 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Becky/IntBeckySex.rpy` categories=`items_inventory_clothes;people_npc;player_state` current=51177 web=52142 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Becky/IntBeckyTalk.rpy` categories=`items_inventory_clothes;media_display_data;people_npc` current=11326 web=10952 current_symbols_only=`label:IntBeckyTalkRefresh` web_symbols_only=``
- `NPC/Girls/Becky/IntBeckyTalkSherwood.rpy` categories=`people_npc;player_state` current=10843 web=9980 current_symbols_only=`label:IntBeckyTalkSherwoodRefresh` web_symbols_only=``
- `NPC/Girls/Becky/IntBeckyTalkTopics.rpy` categories=`people_npc` current=39892 web=40148 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Becky/ShowBeckyPortrait.rpy` categories=`media_display_data;people_npc` current=1156 web=796 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Clara/ClaraPaintingsThread.rpy` categories=`events_threads;people_npc;rooms_objects;schedules` current=28879 web=29588 current_symbols_only=`function:clara_paintings_flag;function:clara_paintings_set` web_symbols_only=`function:clara_paintings_barber_morning_time;function:clara_paintings_barber_night_roll_active;function:clara_paintings_barber_night_time;function:clara_paintin`
- `NPC/Girls/Clara/InitClara.rpy` categories=`combat_enemies;events_threads;people_npc;rooms_objects` current=27244 web=27104 current_symbols_only=`class:Clara;function:__init__` web_symbols_only=`function:clara_booklet_market_thread_num;function:clara_market_spy_day_available;function:clara_market_spy_night_available;function:clara_market_story_caption;f`
- `NPC/Girls/Clara/IntClaraTalk.rpy` categories=`events_threads;media_display_data;people_npc` current=20958 web=22096 current_symbols_only=`label:IntClaraTalkRefresh` web_symbols_only=`label:ClaraMarketFollow`
- `NPC/Girls/Common/EventCleaningHarrassPart2.rpy` categories=`events_threads;items_inventory_clothes;media_display_data;people_npc;rooms_objects` current=8948 web=9137 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Common/EventWaitressHarrassPart2.rpy` categories=`events_threads;items_inventory_clothes;media_display_data;people_npc;rooms_objects` current=6362 web=6566 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Common/GetGirlDrunk.rpy` categories=`people_npc` current=895 web=596 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Common/GetRandomGirlByJob.rpy` categories=`people_npc` current=1452 web=1032 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Common/GirlCard.rpy` categories=`items_inventory_clothes;people_npc` current=14847 web=11621 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Common/GirlDressBuy.rpy` categories=`events_threads;items_inventory_clothes;media_display_data;people_npc` current=6041 web=5828 current_symbols_only=`label:GirlDressBuyRefresh` web_symbols_only=`label:GirlDressBuyMenuState`
- `NPC/Girls/Common/GirlDressSuggest.rpy` categories=`items_inventory_clothes;people_npc;player_state` current=18188 web=19092 current_symbols_only=`label:GirlDressSuggestRestore` web_symbols_only=``
- `NPC/Girls/Common/GirlSuggestDressFunc.rpy` categories=`items_inventory_clothes;people_npc` current=21799 web=22403 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Common/GirlsDesc.rpy` categories=`items_inventory_clothes;people_npc` current=22003 web=21846 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Common/IntHarrassmentDiscuss.rpy` categories=`people_npc` current=9546 web=9427 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Common/MomDressComplaint.rpy` categories=`events_threads;items_inventory_clothes;media_display_data;people_npc;player_state;rooms_objects;schedules` current=27240 web=27617 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Common/MorningSickness.rpy` categories=`events_threads;people_npc;player_state;rooms_objects;schedules` current=12183 web=12127 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Common/PartEventGirlHarrassmentReaction.rpy` categories=`events_threads;media_display_data;people_npc` current=10119 web=9670 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Common/PartEventGirlReactionTalk.rpy` categories=`events_threads;people_npc` current=4779 web=4251 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Common/PregnancyCheck.rpy` categories=`events_threads;people_npc;player_state;rooms_objects` current=8491 web=8381 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Common/ShowGirlSexHistory.rpy` categories=`calendar_time;people_npc;player_state` current=2446 web=2028 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Common/SlutFriendsIncrease.rpy` categories=`people_npc;player_state;rooms_objects` current=2644 web=3161 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Common/ZaletOpinionCalc.rpy` categories=`people_npc;player_state` current=20214 web=19646 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Francheska/FrancheskaTalk.rpy` categories=`people_npc;rooms_objects` current=15263 web=14513 current_symbols_only=`function:_fran_clean` web_symbols_only=``
- `NPC/Girls/Georgett/InitGeorgett.rpy` categories=`calendar_time;items_inventory_clothes;people_npc;player_state` current=5474 web=4205 current_symbols_only=`class:Georgett;function:__init__` web_symbols_only=``
- `NPC/Girls/Georgett/IntGeorgettAfterCermon.rpy` categories=`events_threads;media_display_data;people_npc;player_state` current=9925 web=9831 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Georgett/IntGeorgettDressChange.rpy` categories=`events_threads;items_inventory_clothes;people_npc` current=4368 web=3982 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Georgett/IntGeorgettSex.rpy` categories=`items_inventory_clothes;people_npc;player_state;rooms_objects` current=26348 web=27802 current_symbols_only=`label:int_georgett_sex_menu` web_symbols_only=`label:sexGeorgette`
- `NPC/Girls/Georgett/IntGeorgettTalk.rpy` categories=`items_inventory_clothes;media_display_data;people_npc;player_state;rooms_objects` current=41193 web=51304 current_symbols_only=`label:IntGeorgettTalkRefresh;label:IntGeorgettTalkRestore` web_symbols_only=`function:georgett_item_caption;function:georgett_native_gift_item_ids;function:georgett_native_share_item_ids;label:IntGeorgettGiftApply;label:IntGeorgettGiftMe`
- `NPC/Girls/Georgett/ShowGeorgettPortrait.rpy` categories=`media_display_data;people_npc` current=1872 web=1623 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Inga/InitInga.rpy` categories=`calendar_time;items_inventory_clothes;people_npc;player_state;schedules` current=5081 web=3914 current_symbols_only=`class:Inga;function:__init__` web_symbols_only=``
- `NPC/Girls/Inga/IntIngaTalk.rpy` categories=`media_display_data;people_npc` current=1338 web=977 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Irma/InitIrma.rpy` categories=`items_inventory_clothes;people_npc;player_state` current=6444 web=7328 current_symbols_only=`class:Irma;function:__init__` web_symbols_only=``
- `NPC/Girls/Irma/IntIrmaTalk.rpy` categories=`items_inventory_clothes;media_display_data;people_npc;player_state` current=8857 web=8030 current_symbols_only=`label:IntIrmaTalkRefresh` web_symbols_only=``
- `NPC/Girls/Irma/IrmaShortStories.rpy` categories=`people_npc` current=5729 web=5293 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Liza/InitLiza.rpy` categories=`calendar_time;items_inventory_clothes;people_npc;player_state` current=4159 web=2941 current_symbols_only=`class:Liza;function:__init__` web_symbols_only=``
- `NPC/Girls/Liza/IntLizaDressChange.rpy` categories=`events_threads;items_inventory_clothes;people_npc;rooms_objects` current=14677 web=14256 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Liza/IntLizaSex.rpy` categories=`items_inventory_clothes;people_npc;player_state;rooms_objects` current=22696 web=23760 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Liza/IntLizaTalk.rpy` categories=`people_npc;player_state;rooms_objects` current=20192 web=19802 current_symbols_only=`label:IntLizaTalkRefresh` web_symbols_only=``
- `NPC/Girls/Liza/IntLizettAfterCermon.rpy` categories=`events_threads;media_display_data;people_npc;player_state` current=13910 web=13828 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Liza/ShowLizaPortrait.rpy` categories=`media_display_data;people_npc` current=1432 web=1133 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Melissa/InitMelissa.rpy` categories=`people_npc;rooms_objects;schedules` current=18289 web=9273 current_symbols_only=`class:MelissaData;class:MelissaInfo;default:Melissa;define:MelissaStaticData;function:__init__;function:ensure_story_defaults;function:initialize_new_game_state` web_symbols_only=``
- `NPC/Girls/Melissa/IntMelissaDressChange.rpy` categories=`events_threads;items_inventory_clothes;people_npc` current=1925 web=1559 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Melissa/IntMelissaSex.rpy` categories=`items_inventory_clothes;people_npc;player_state;rooms_objects` current=30755 web=31402 current_symbols_only=`default:SexTimesToday` web_symbols_only=``
- `NPC/Girls/Melissa/IntMelissaTalk.rpy` categories=`people_npc;player_state;rooms_objects` current=37944 web=38102 current_symbols_only=`label:IntMelissaTalkRefresh;label:IntMelissaTalkRestore` web_symbols_only=``
- `NPC/Girls/Melissa/MelissaBatsQuest.rpy` categories=`people_npc;player_state;rooms_objects;schedules` current=33487 web=34219 current_symbols_only=`` web_symbols_only=``
- `NPC/Girls/Melissa/MelissaEvents.rpy` categories=`combat_enemies;events_threads;media_display_data;people_npc;rooms_objects;schedules` current=21300 web=30294 current_symbols_only=`label:story_melissa_bat_problem_0;label:story_melissa_bat_problem_1;label:story_melissa_bat_problem_2;label:story_melissa_bat_problem_3;label:story_melissa_bat_` web_symbols_only=`define:melissaThreadList;label:melissaBat_0;label:melissaBat_1;label:melissaBat_2;label:melissaBat_3;label:melissaBat_4;label:melissaBat_5;label:melissaBat_6;la`
- `NPC/Girls/Sandra/InitSandra.rpy` categories=`calendar_time;items_inventory_clothes;people_npc;player_state;rooms_objects;schedules` current=31973 web=6492 current_symbols_only=`class:SandraData;class:SandraInfo;default:Sandra;define:SandraStaticData;function:__init__;function:change_fear;function:change_mana;function:daily_mana_update;` web_symbols_only=``
- `NPC/Girls/Sandra/IntSandraDressChange.rpy` categories=`events_threads;items_inventory_clothes;people_npc` current=2629 web=2365 current_symbols_only=`label:IntSandraOfferBuyDress` web_symbols_only=`label:IntSandraDressChange;label:IntSandraDressChangeApply;label:int_sandra_dress_change`
- `NPC/Girls/Sandra/IntSandraTalk.rpy` categories=`items_inventory_clothes;people_npc;player_state;rooms_objects` current=7761 web=6456 current_symbols_only=`label:IntSandraHouseholdInsight;label:IntSandraHouseholdPriorities;label:IntSandraReconcile` web_symbols_only=`label:IntSandraTalkApply`
- `NPC/Secondary/DogCompanion.rpy` categories=`combat_enemies;people_npc;player_state;rooms_objects` current=43576 web=48865 current_symbols_only=`label:IntDogTalkRefresh` web_symbols_only=`function:action_data;function:appearance_code;function:card_lines;function:card_stat_rows;function:card_title;function:display_name;function:fight_stats;functio`
- `NPC/Secondary/InitAlberTalk.rpy` categories=`combat_enemies;people_npc` current=7235 web=6787 current_symbols_only=`` web_symbols_only=``
- `NPC/Secondary/InitSecondaryNPC.rpy` categories=`people_npc;player_state` current=22903 web=13833 current_symbols_only=`class:Alber;class:Draupnir;class:Eddie;class:Francheska;class:Luisa;class:Mongol;class:Robin;class:Sergio;class:Zimmer;default:LuisaVar;default:SergioVar;functi` web_symbols_only=`default:alber;default:draupnir;default:eddie;default:fran;default:gerhard;default:mongol;default:robin;default:zimmer;function:eddie_grocery_morning_active;func`
- `NPC/Secondary/IntAlberTalk.rpy` categories=`combat_enemies;media_display_data;people_npc` current=10440 web=10137 current_symbols_only=`label:IntAlberTalkRefresh` web_symbols_only=`label:IntAlberTalkMenuState`
- `NPC/Secondary/IntEddieBeckySex.rpy` categories=`items_inventory_clothes;media_display_data;people_npc;player_state` current=21440 web=21856 current_symbols_only=`` web_symbols_only=``
- `NPC/Secondary/IntEddieTalk.rpy` categories=`media_display_data;people_npc;player_state;rooms_objects;schedules` current=18365 web=18213 current_symbols_only=`` web_symbols_only=``
- `NPC/Secondary/IntRobinTalk.rpy` categories=`media_display_data;people_npc` current=9560 web=9103 current_symbols_only=`` web_symbols_only=``
- `NPC/Secondary/IntZimmerTalk.rpy` categories=`media_display_data;people_npc` current=16797 web=16680 current_symbols_only=`label:IntZimmerTalkRefresh` web_symbols_only=`label:IntZimmerTalkMenuState`
- `NPC/Secondary/MelissaWerecatQuest.rpy` categories=`combat_enemies;people_npc;rooms_objects` current=28524 web=30835 current_symbols_only=`` web_symbols_only=`function:werecat_apply_adoption_effects;function:werecat_apply_household_team_state;function:werecat_tavern_team_keys`
- `NPC/Secondary/MongolTalk.rpy` categories=`media_display_data;people_npc;player_state;rooms_objects` current=14254 web=10771 current_symbols_only=`label:ClaraSecretMerchantBuy;label:ClaraSecretMerchantMenu;label:MongolTalkApply` web_symbols_only=`label:MongolHorseBuy;label:MongolHorseDiscount;label:MongolTalkMenu`
- `NPC/Secondary/SherwoodTravel.rpy` categories=`calendar_time;media_display_data;people_npc;rooms_objects` current=14445 web=14196 current_symbols_only=`` web_symbols_only=``
- `NPC/Secondary/WerecatNPC.rpy` categories=`combat_enemies;people_npc;rooms_objects;schedules` current=32749 web=36918 current_symbols_only=`label:IntWerecatTalkRefresh` web_symbols_only=`class:WerecatCompanion;default:werecat;function:action_caption;function:action_data;function:add_comfort;function:add_trust;function:ambient_text;function:card_`
- `Town/Arts/ArtisansQuarter.rpy` categories=`items_inventory_clothes;media_display_data;people_npc;rooms_objects` current=9142 web=8865 current_symbols_only=`label:ArtisansQuarterRestore` web_symbols_only=``
- `Town/Arts/BarberShop.rpy` categories=`people_npc;player_state;rooms_objects` current=20049 web=20802 current_symbols_only=`` web_symbols_only=``
- `Town/Arts/Dress/DressShop.rpy` categories=`items_inventory_clothes;player_state;rooms_objects;schedules` current=14784 web=40085 current_symbols_only=`default:DressBuyer;default:DressProduced;function:dress_shop_buy_male_item;function:dress_shop_clara_present;function:dress_shop_irma_working_idle;function:dres` web_symbols_only=`default:DressShopCatalogDressCode;default:DressShopCatalogRack;default:DressShopFemaleCatalogItemIds;default:DressShopMaleCatalogItemIds;default:DressShopSavedT`
- `Town/Arts/Dress/DressShopDressItems.rpy` categories=`items_inventory_clothes;player_state;rooms_objects` current=4734 web=4171 current_symbols_only=`function:dress_shop_item_depreciated;function:dress_shop_prepare_dress_item` web_symbols_only=`function:dress_shop_build_dress_item;function:dress_shop_get_item`
- `Town/Arts/Dress/DressShopFemaleSamples001.rpy` categories=`items_inventory_clothes;rooms_objects` current=1139 web=427 current_symbols_only=`` web_symbols_only=``
- `Town/Arts/Dress/DressShopMaleSamples001.rpy` categories=`items_inventory_clothes;rooms_objects` current=1118 web=407 current_symbols_only=`` web_symbols_only=``

## Recovery Interpretation

- This report identifies structural drift; it is not a patch plan by itself.
- For each subsystem, choose one canonical owner before importing from web or preserving current development.
- A `web_only` file can be a recovery candidate only if its matching assets/content are confirmed newer and it does not reintroduce obsolete wrappers or duplicate source-of-truth state.
- A `current_only` file can be legitimate new architecture or accidental bloat; classify before keeping it.
- Modified files with many new symbols are the highest risk for duplicate state, especially NPC init, event/thread runtime, schedule, calendar/time, item catalogs, and room/object files.
