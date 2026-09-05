# ================================================================================
# FamilyLife-style story event runtime split.
# Engine code lives in conditions.rpy, threads.rpy, and events.rpy.
# Authored thread definitions and event labels stay in StoryEventRuntime.rpy for now.
# ================================================================================

define amandaRevealingDressRequestConditions = [
    "#bool(str(Sandra.revealing_dress_code or '').strip())",
    "#bool(str(Melissa.revealing_dress_code or '').strip())",
    "#not str(Amanda.revealing_dress_code or '').strip()",
    "#daily_events.exists('', 'BuyDressTom', '') == 0",
    "#daily_events.exists('amanda', 'BuyDress', '') == 0",
    "#int(Amanda.rel or 0) >= 5",
    "#int(Amanda.talked_today or 0) == 0",
]

define amandaThreadList = [
    LThreadData(0, "amanda", "RevealingDressRequest", None, [[
        (
            "AmandaDressRequestEvent",
            None, None, None,
            1, None, amandaRevealingDressRequestConditions, None,
            "TavernMain", "amanda_dress_request", 0,
        ),
        (
            "AmandaDressRequestEvent",
            None, None, None,
            1, None, amandaRevealingDressRequestConditions, None,
            "TavernKitchen", "amanda_dress_request", 0,
        ),
    ]], highlight=False, threaded=True),
    LThreadData(0, "amanda", "LegareDance", None, [
        AmandaLegareDanceIntro,
        AmandaLegareDanceTalking,
        AmandaLegareDanceGroping,
        AmandaLegareDanceKissing,
        AmandaLegareDanceAfter,
    ], highlight=False, threaded=True),
    LThreadData(0, "amanda", "FridayDanceMC", None, [
        AmandaFridayDanceMC,
    ], highlight=False, threaded=False),
    LThreadData(0, "amanda", "FridayDanceLegare", None, [
        AmandaFridayDanceLegare,
    ], highlight=False, threaded=False),
    LThreadData(0, "amanda", "TavernSeductions", None, [
        AmandaTavernSeduction,
    ], highlight=False, threaded=False),
    LThreadData(0, "amanda", "RoomNightApproach", None, [
        AmandaRoomNightApproach,
    ], highlight=False, threaded=False),
    LThreadData(0, "amanda", "GloryHoleTry", None, [
        AmandaGloryHoleTry,
    ], highlight=False, threaded=False),
    LThreadData(0, "amanda", "MorningWindowEpisode", None, [
        AmandaMorningWindowEpisode,
    ], highlight=False, threaded=False),
    LThreadData(0, "amanda", "KitchenWindowFavor", None, [
        AmandaKitchenWindowFavor,
    ], highlight=False, threaded=False),
    LThreadData(0, "amanda", "NightBowlWindow", None, [
        AmandaNightBowlWindow,
    ], highlight=False, threaded=False),
    LThreadData(0, "amanda", "Birth", None, [
        AmandaBirth,
    ], highlight=False, threaded=False),
    LThreadData(0, "amanda", "LegareTavernVisits", None, [
        AmandaLegareTavernVisit,
    ], highlight=False, threaded=False),
    LThreadData(0, "amanda", "StreetLegareSightings", None, [
        [AmandaStreetLegareSightingStreet, AmandaStreetLegareSightingMarket],
    ], highlight=False, threaded=False),
    LThreadData(0, "amanda", "StreetLoverEncounters", None, [
        [AmandaStreetLoverEncounterStreet, AmandaStreetLoverEncounterMarket],
    ], highlight=False, threaded=False),
]

define melissaRevealingDressRequestConditions = [
    "#bool(str(Sandra.revealing_dress_code or '').strip())",
    "#not str(Melissa.revealing_dress_code or '').strip()",
    "#daily_events.exists('', 'BuyDressTom', '') == 0",
    "#daily_events.exists('melissa', 'BuyDress', '') == 0",
    "#int(Melissa.rel or 0) >= 6",
    "#int(Melissa.talked_today or 0) == 0",
]

define melissaCourtshipBaseConditions = [
    "#Melissa.intimacy_story_ready()",
]

define melissaCourtshipOpeningConditions = melissaCourtshipBaseConditions + [
    "#Melissa.relationship_stage() >= 2",
    "#Liza.can_work_tavern()",
    "#Liza.is_working()",
    "#int(Amanda.var_int('lizafriends', 0)) > 0",
    "#int(Amanda.sex_stat('sexacts', 0) or 0) > 0",
]

define melissaThreadList = [
    LThreadData(0, "melissa", "AmandaRoomShare", None, [[
        MelissaAmandaRoomShare,
    ]], highlight=False, threaded=False),
    LThreadData(0, "melissa", "RevealingDressRequest", None, [[
        (
            "MelissaDressRequestEvent",
            None, None, None,
            1, None, melissaRevealingDressRequestConditions, None,
            "TavernMain", "melissa_dress_request", 0,
        ),
        (
            "MelissaDressRequestEvent",
            None, None, None,
            1, None, melissaRevealingDressRequestConditions, None,
            "TavernKitchen", "melissa_dress_request", 0,
        ),
    ]], highlight=False, threaded=True),
    LThreadData(0, "melissa", "Courtship", None, [
        [
            (
                "story_melissa_courtship_amanda_talk_0",
                (1, 6), (12, 18), None,
                0.25, None,
                melissaCourtshipOpeningConditions + [
                    "#str(people.location('amanda') or '') == 'TavernMain'",
                    "#str(people.location('melissa') or '') == 'TavernMain'",
                    "#str(people.location('liza') or '') == 'TavernMain'",
                ],
                None,
                "TavernMain", "enter", 15,
            ),
            (
                "story_melissa_courtship_amanda_talk_0",
                (1, 6), (12, 18), None,
                0.25, None,
                melissaCourtshipOpeningConditions + [
                    "#str(people.location('amanda') or '') == 'TavernKitchen'",
                    "#str(people.location('melissa') or '') == 'TavernKitchen'",
                    "#str(people.location('liza') or '') == 'TavernMain'",
                ],
                None,
                "TavernKitchen", "enter", 15,
            ),
        ],
        (
            "story_melissa_courtship_storm_1",
            None, (20, 23), 1,
            0.25, None, melissaCourtshipBaseConditions, None,
            "TavernMyRoom", "sleep", 0,
        ),
        (
            "story_melissa_courtship_mutual_2",
            None, (20, 23), 1,
            1, None, melissaCourtshipBaseConditions, None,
            "TavernMyRoom", "sleep", 0,
        ),
        (
            "story_melissa_courtship_touch_him_3",
            None, (20, 23), 1,
            1, None, melissaCourtshipBaseConditions, None,
            "TavernMyRoom", "sleep", 0,
        ),
        (
            "story_melissa_courtship_taste_4",
            None, (20, 23), 1,
            1, None, melissaCourtshipBaseConditions, None,
            "TavernMyRoom", "sleep", 0,
        ),
    ], highlight=False, threaded=True),
    #
    # melissa_rat_problem
    #
    # Event tuple columns:
    # (target, day, hour, delay, probability, reqs, condition, item, location, action, priority)
    #
    LThreadData(0, "melissa", "RatProblem", None, [
        (
            "story_melissa_storage_rat_0",
            (1, 6), (6, 7), None,
            1,
            None,
            [
                "#people_to_int(Melissa.storage_rat_help_day, -1) < 0",
                "#str(people.location('melissa') or '') == 'TavernStorage'",
                "#not household_runtime_event_seen_today('melissa_storage_rat')",
            ],
            None,
            "TavernStorage",
            "enter",
            0,
        ),
    ], highlight=False, threaded=True),
    #
    # melissa_werecat_problem
    #
    LThreadData(0, "melissa", "WerecatProblem", None, [
        (
            "story_melissa_werecat_intro_0",
            (1, 7), (6, 7), None,
            1,
            None,
            [
                "#int(werecat_state().get('rats_problem_active', 0) or 0) == 1",
                "#not bool(player.tavern_management.breakfast.today)",
            ],
            None,
            "TavernKitchen",
            "enter",
            0,
        ),
        (
            "story_melissa_werecat_rumor_0",
            None, None, None,
            1,
            None,
            [
                "#not (int(werecat_state().get('sold', 0) or 0) == 0 and int(werecat_state().get('adopted_count', 0) or 0) >= 1)",
                "#int(werecat_state().get('rats_problem_active', 0) or 0) == 1",
                "#people_to_int(Melissa.storage_rat_help_day, -1) >= 0",
                "#int(werecat_state().get('adopted', 0) or 0) == 0",
                "#int(werecat_state().get('sold', 0) or 0) == 0",
                "#int(werecat_state().get('hunter_tease_day', -1) or -1) < 0",
            ],
            None,
            "HunterClub",
            "overheard",
            1,
        ),
        (
            "story_melissa_werecat_home_0",
            (1, 7), (6, 7), None,
            1,
            None,
            [
                "#int(werecat_state().get('adopted', 0) or 0) == 1",
                "#int(werecat_state().get('adoption_breakfast_seen', 0) or 0) == 0",
                "#int(werecat_state().get('adopted_day', -1) or -1) >= 0",
                "#day_delta_ready(werecat_state().get('adopted_day', -1), 1)",
                "#not bool(player.tavern_management.breakfast.today)",
            ],
            None,
            "TavernKitchen",
            "enter",
            2,
        ),
        (
            "story_melissa_werecat_home_1",
            (1, 7), (6, 7), None,
            1,
            None,
            [
                "#int(werecat_state().get('adopted', 0) or 0) == 1",
                "#int(werecat_state().get('adoption_breakfast_seen', 0) or 0) == 1",
                "#int(werecat_state().get('adopted_day', -1) or -1) >= 0",
                "#day_delta_ready(werecat_state().get('adopted_day', -1), 30)",
                "#int(werecat_state().get('first_month_thanks_day', -1) or -1) < int(werecat_state().get('adopted_day', -1) or -1) + 30",
                "#not bool(player.tavern_management.breakfast.today)",
            ],
            None,
            "TavernKitchen",
            "enter",
            3,
        ),
    ], highlight=False, threaded=True),
    # bats_problem_thread
    # Rat cleanup in storage is the household trigger; this ordered bat problem
    # starts at the next available breakfast.
    LThreadData(0, "melissa", "BatProblem", "melissaRatProblem_0", [
        (
            "story_melissa_bat_problem_0",
            (1, 7), (6, 7), None,
            1,
            None,
            [
                "#people_to_int(Melissa.storage_rat_help_day, -1) >= 0",
                "#day_delta_ready(Melissa.storage_rat_help_day, 2)",
                "#not bool(player.tavern_management.breakfast.today)",
            ],
            None,
            "TavernKitchen",
            "enter",
            0,
        ),
        (
            "story_melissa_bat_problem_1",
            None, (16, 17), None,
            1,
            None,
            None,
            None,
            "TavernUpstairs",
            "enter",
            1,
        ),
        (
            "story_melissa_bat_problem_room_inspect",
            None, None, None,
            1,
            None,
            [
                "#int(effective_player_exploration() or 0) >= 100",
            ],
            None,
            "TavernMelissaRoom",
            "room_search",
            2,
        ),
        (
            "story_melissa_bat_problem_2",
            None, None, None,
            1,
            None,
            [
                "#int(current_game_day() or 0) >= people_to_int(Melissa.bat_attic_check_day, -1)",
            ],
            None,
            "TavernAtic",
            "melissa_bats",
            2,
        ),
        (
            "story_melissa_bat_problem_3",
            None, None, None,
            1,
            None,
            None,
            None,
            "TavernAtic",
            "melissa_bats",
            3,
        ),
        (
            "story_melissa_bat_problem_fall",
            None, None, None,
            1,
            None,
            None,
            None,
            "TavernAtic",
            "melissa_bats",
            4,
        ),
        (
            "story_melissa_bat_problem_4",
            None, None, None,
            1,
            None,
            None,
            None,
            "TavernAtic",
            "melissa_bats",
            5,
        ),
        [
            (
                "story_melissa_bat_problem_roof",
                None, None, None,
                1,
                None,
                [
                    "#people_to_int(Melissa.roof_repair_complete_day, -1) < 0",
                ],
                None,
                "TavernAtic",
                "melissa_bats",
                6,
            ),
            (
                "story_melissa_bat_problem_breakfast_invite",
                None, None, None,
                1,
                None,
                [
                    "#people_to_int(Melissa.roof_repair_complete_day, -1) >= 0",
                    "#int(current_game_day() or 0) >= people_to_int(Melissa.roof_repair_complete_day, -1)",
                ],
                None,
                "talk_melissa",
                "melissa_breakfast_invite",
                7,
            ),
        ],
        (
            "story_melissa_bat_problem_breakfast_argument",
            (1, 7), (6, 11), 1,
            1,
            None,
            [
                "#not bool(player.tavern_management.breakfast.today)",
            ],
            None,
            "TavernKitchen",
            "enter",
            8,
        ),
        (
            "story_melissa_bat_problem_5",
            None, None, None,
            1,
            None,
            [
                "#people_to_int(Melissa.roof_repair_complete_day, -1) >= 0",
                "#int(current_game_day() or 0) >= people_to_int(Melissa.roof_repair_complete_day, -1)",
            ],
            None,
            "TavernAmandaRoom",
            "melissa_bats",
            9,
        ),
        (
            "story_melissa_bat_problem_booklet_search",
            None, None, None,
            1,
            None,
            [
                "#not bool(Melissa.drawings_found)",
            ],
            None,
            "TavernMelissaRoom",
            "room_search",
            10,
        ),
        (
            "story_melissa_bat_problem_6",
            None, None, None,
            1,
            None,
            [
                "#bool(Melissa.drawings_returned)",
            ],
            None,
            "TavernMain",
            "melissa_talk",
            11,
        ),
    ], highlight=False, threaded=True),
]

define sandraThreadList = [
    LThreadData(0, "sandra", "WeeklyEvaluation", "sandraWeeklyEvaluationEnabled", [
        ("sandraWeeklyEvaluation_0", None, None, 0, 1, None, None, None, "TavernMyRoom", "sleep", 0),
        ("sandraWeeklyEvaluation_1", None, None, 0, 1, None, None, None, "TavernMyRoom", "sleep", 1),
        ("sandraWeeklyEvaluation_2", None, None, 0, 1, None, None, None, "TavernMyRoom", "sleep", 2),
        ("sandraWeeklyEvaluation_3", None, None, 0, 1, None, None, None, "TavernMyRoom", "sleep", 3),
        ("TavernSandraNightThanksScene", None, (22, 23), 0, 1, None, None, None, "TavernSandraRoom", "sandra_night_thanks", 0),
    ], highlight=False, threaded=True),
    LThreadData(0, "sandra", "RevealingDressInitiative", None, [
        (
            "SandraDressInitiativeEvent",
            None, None, None,
            1,
            None,
            [
                "#threads['beckyHome'].completed",
                "#not str(Sandra.revealing_dress_code or '').strip()",
                "#daily_events.exists('', 'BuyDressTom', '') == 0",
                "#daily_events.exists('sandra', 'BuyDress', '') == 0",
                "#int(Sandra.rel or 0) >= 7",
                "#int(Sandra.talked_today or 0) == 0",
            ],
            None,
            "TavernKitchen",
            "sandra_dress_initiative",
            0,
        ),
    ], highlight=False, threaded=True),
    LThreadData(0, "sandra", "KitchenHouseholdRespect", None, [
        (
            "story_sandra_kitchen_household_respect_0",
            None, (6, 10), None,
            1,
            None,
            [
                "#threads['sandraWeeklyEvaluation'].completed",
                "#household_morning_issue_type('sandra') == ''",
                "#household_morning_issue_type('melissa') == ''",
                "#household_morning_issue_type('amanda') == ''",
            ],
            None,
            "TavernKitchen",
            "enter",
            5,
        ),
    ], highlight=False, threaded=True),
]
define claraThreadList = [
    LThreadData(0, "clara", "BookletMarket", None, [
        (
            "story_clara_market_booklet_0",
            [1, 2, 3, 4, 5, 6], (11, 12), None,
            1,
            None,
            [
                "#people_to_int(Clara.market_day_roll_day, -1) == int(calendar_v2.daysInGame or 0)",
                "#bool(Clara.market_day_roll)",
                "#not (people_to_int(Clara.market_follow_failed_day, -1) == int(calendar_v2.daysInGame or 0) and people_to_int(Clara.market_follow_failed_hour, -1) == int(calendar_v2.hour or 0))",
            ],
            None,
            "MarketPlace",
            "enter",
            0,
        ),
        (
            "story_clara_market_booklet_2",
            [1, 2, 3, 4, 6], (18, 22), None,
            1,
            None,
            [
                "#people_to_int(Clara.market_evening_roll_day, -1) == int(calendar_v2.daysInGame or 0)",
                "#bool(Clara.market_evening_roll)",
            ],
            None,
            "MarketPlace",
            "enter",
            1,
        ),
        (
            "story_clara_market_booklet_3",
            [1, 2, 3, 4, 6], (18, 22), None,
            1,
            None,
            [
                "#people_to_int(Clara.market_evening_roll_day, -1) == int(calendar_v2.daysInGame or 0)",
                "#bool(Clara.market_evening_roll)",
            ],
            None,
            "MarketPlace",
            "enter",
            2,
        ),
        (
            "story_clara_market_booklet_5",
            None, None, None,
            1,
            None,
            None,
            None,
            "HunterClub",
            "overheard",
            3,
        ),
        (
            "story_clara_market_booklet_6",
            None, None, None,
            1,
            None,
            None,
            None,
            "menu_CityGuard",
            "mongol_stocks",
            4,
        ),
        (
            "story_clara_market_booklet_7",
            None, (21, 23), None,
            1,
            None,
            None,
            None,
            "menu_CityGuard",
            "mongol_stocks",
            5,
        ),
        (
            "story_clara_market_booklet_8",
            (1, 6), (6, 12), None,
            1,
            None,
            [
                "#Draupnir.mongol_lockpick_order_day < 0",
            ],
            None,
            "StolyarWorkshop",
            "enter",
            6,
        ),
        (
            "story_clara_market_booklet_9",
            None, (21, 23), None,
            1,
            None,
            [
                "#Draupnir.mongol_lockpick_order_day >= 0",
                "#int(current_game_day() or 0) > Mongol.stocks_food_day",
                "#int(player.tavern_management.productnum or 0) > 0",
                "#int(player.tavern_management.winenum or 0) > 0",
            ],
            None,
            "menu_CityGuard",
            "mongol_stocks",
            7,
        ),
        (
            "story_clara_market_booklet_10",
            None, None, None,
            1,
            None,
            None,
            None,
            "HunterClub",
            "overheard",
            8,
        ),
    ], highlight=False, threaded=True),
    #
    # clara_paintings_path
    #
    # Event tuple columns:
    # (target, day, hour, delay, probability, reqs, condition, item, location, action, priority)
    #
    LThreadData(1, "clara", "PaintingsPath", None, [
        (
            "story_clara_paintings_melissa_0",
            None, None, None,
            1,
            None,
            [
                "#bool(Melissa.drawings_found)",
                "#people_to_int(Melissa.asked_today, 0) == 0",
            ],
            None,
            "talk_melissa",
            "clara_paintings",
            0,
        ),
        (
            "story_clara_paintings_cellar_1",
            None, (8, 12), None,
            1,
            None,
            [
                "#int(Clara.flirt_count or 0) > 0",
            ],
            None,
            "WineStore",
            "clara_paintings",
            1,
        ),
        (
            "story_clara_paintings_comfort_2",
            None, (6, 7), None,
            1,
            None,
            [
                "#str(people.location('clara') or '') == 'WineStore'",
            ],
            None,
            "WineStore",
            "clara_paintings",
            2,
        ),
        (
            "story_clara_paintings_first_ask_3",
            None, None, None,
            1,
            None,
            None,
            None,
            "WineStore",
            "clara_paintings",
            3,
        ),
        (
            "story_clara_paintings_second_ask_4",
            None, None, None,
            1,
            None,
            None,
            None,
            "WineStore",
            "clara_paintings",
            4,
        ),
        (
            "story_clara_paintings_legare_5",
            None, None, None,
            1,
            None,
            None,
            None,
            "WineStore",
            "clara_paintings",
            5,
        ),
        (
            "story_clara_paintings_church_6",
            7, (6, 12), None,
            1,
            None,
            None,
            None,
            "Church",
            "clara_paintings",
            6,
        ),
        (
            "story_clara_paintings_barber_7",
            None, (8, 10), None,
            1,
            None,
            None,
            None,
            "BarberShop",
            "clara_fiance",
            7,
        ),
        (
            "story_clara_paintings_commission_8",
            None, None, None,
            1,
            None,
            [
                "#str(people.location('clara') or '') == 'TavernMain'",
            ],
            None,
            "TavernMain",
            "clara_paintings",
            8,
        ),
        (
            "story_clara_paintings_commission_followup_9",
            None, (6, 7), None,
            1,
            None,
            [
                "#int(current_game_day() or 0) >= people_to_int(Clara.commission_followup_day, 999999)",
                "#str(people.location('clara') or '') == 'WineStore'",
            ],
            None,
            "WineStore",
            "clara_paintings",
            9,
        ),
        (
            "story_clara_paintings_evening_peek_10",
            None, (19, 21), None,
            1,
            None,
            None,
            None,
            "ArtisansQuarter",
            "enter",
            10,
        ),
        (
            "story_clara_paintings_confession_11",
            None, None, None,
            1,
            None,
            [
                "#str(people.location('clara') or '') == 'TavernMelissaRoom'",
                "#str(people.location('melissa') or '') == 'TavernMelissaRoom'",
            ],
            None,
            "TavernMelissaRoom",
            "enter",
            11,
        ),
        (
            "story_clara_paintings_murder_12",
            None, None, None,
            1,
            None,
            [
                "#int(current_game_day() or 0) >= people_to_int(Clara.murder_day, 999999)",
                "#int(threads['claraForestSofa'].num or 0) >= 6",
                "#not bool(threads['claraForestSofa'].aborted)",
            ],
            None,
            "CityGuard",
            "enter",
            12,
        ),
    ], highlight=False, threaded=True),
    #
    # clara_forest_sofa
    #
    # The thread owns only ordered story availability. The clue and shovel are
    # inventory items, the installed sofa belongs to TavernMain, and the final
    # capacity reward belongs to PlayerIntimacy.
    LThreadData(1, "clara", "ForestSofa", [
        "#threads['claraBookletMarket'].completed",
    ], [
        (
            "story_clara_forest_follow_0",
            [1, 2, 3, 4, 5, 6], (12, 19), None,
            1,
            None,
            [
                "#int(player.stats.exploration or 0) >= 100",
            ],
            None,
            "ForestClearing",
            "clara_follow",
            3,
        ),
        (
            "story_clara_forest_horse_prank_1",
            [1, 2, 3, 4, 5, 6], (12, 19), 1,
            1,
            None,
            [
                "#player.horse.owns_horse()",
            ],
            None,
            "ForestLake",
            "clara_horse_prank",
            3,
        ),
        (
            "story_clara_forest_shared_bath_2",
            [1, 2, 3, 4, 5, 6], (12, 19), 1,
            1,
            None,
            None,
            None,
            "ForestLake",
            "clara_bath",
            3,
        ),
        (
            "story_clara_grocery_dirt_3",
            [1, 2, 3, 4, 5, 6], (6, 17), 1,
            1,
            None,
            None,
            None,
            "GroceryStore",
            "enter",
            0,
        ),
        (
            "story_clara_forest_sofa_stash_4",
            None, (6, 19), None,
            1,
            None,
            [
                "#int(player.item_count('clara_pantaloons_001') or 0) > 0",
                "#int(player.item_count('shovel_001') or 0) > 0",
                "#bool(dog.owned)",
                "#'dog' in player.combat.party",
                "#bool(dog.is_alive())",
            ],
            None,
            "ForestHiddenPath",
            "clara_stash",
            1,
        ),
        (
            "story_clara_forest_confession_5",
            None, None, None,
            1,
            None,
            None,
            None,
            "WineStore",
            "clara_truth",
            5,
        ),
        (
            "story_clara_sofa_first_talk_6",
            None, None, None,
            1,
            None,
            [
                "#'cursed_sofa_001' in rooms.get('TavernMain').game_items",
            ],
            None,
            "CursedSofa",
            "talk",
            0,
        ),
        (
            "story_clara_sofa_ritual_7",
            None, None, None,
            1,
            None,
            [
                "#'cursed_sofa_001' in rooms.get('TavernMain').game_items",
                "#threads['claraPaintingsPath'].completed",
                "#bool(Clara.sex_stat('virginity', True))",
                "#bool(Melissa.sex_stat('virginity', True))",
                "#int(player.tavern_management.client_room_hole or 0) > 0",
                "#int(player.tavern_management.glory_hole or 0) == 2",
                "#str(people.location('clara') or '') == 'TavernMain'",
                "#str(people.location('melissa') or '') == 'TavernMain'",
            ],
            None,
            "CursedSofa",
            "talk",
            0,
        ),
    ], highlight=False, threaded=True),
    #
    # clara_tavern_visit
    #
    # Clara owns her visits with Melissa. Tavern rooms only expose the trigger
    # action; they do not register visits, choose pictures, or lock doors.
    LThreadData(2, "clara", "TavernVisit", None, [
        (
            "story_clara_tavern_visit_bar_0",
            [1, 2, 3, 4, 5, 6], (12, 17), None,
            1,
            None,
            [
                "#str(people.location('clara') or '') == 'TavernMain'",
                "#str(people.location('melissa') or '') == 'TavernMain'",
                "#not household_runtime_event_seen_today('clara_tavern_visit')",
            ],
            None,
            "TavernMain",
            "bar_001",
            0,
        ),
        (
            "story_clara_tavern_visit_bar_1",
            [1, 2, 3, 4, 5, 6], (12, 17), None,
            1,
            None,
            [
                "#str(people.location('clara') or '') == 'TavernMain'",
                "#str(people.location('melissa') or '') == 'TavernMain'",
                "#threads['melissaBatProblem'].num >= 6",
                "#not household_runtime_event_seen_today('clara_tavern_visit')",
            ],
            None,
            "TavernMain",
            "bar_001",
            1,
        ),
        (
            "story_clara_tavern_visit_bar_2",
            [1, 2, 3, 4, 5, 6], (12, 17), None,
            1,
            None,
            [
                "#str(people.location('clara') or '') == 'TavernMain'",
                "#str(people.location('melissa') or '') == 'TavernMain'",
                "#int(player.item_count('melissa_drawings_booklet_001') or 0) > 0 or bool(Melissa.drawings_booklet_read) or bool(Melissa.drawings_booklet_left)",
                "#not household_runtime_event_seen_today('clara_tavern_visit')",
            ],
            None,
            "TavernMain",
            "bar_001",
            2,
        ),
        (
            "story_clara_melissa_room_visit_0",
            None, (16, 22), None,
            1,
            None,
            [
                "#str(people.location('clara') or '') == 'TavernMelissaRoom'",
                "#str(people.location('melissa') or '') == 'TavernMelissaRoom'",
                "#threads['melissaBatProblem'].num >= 11",
                "#bool(Melissa.drawings_found)",
                "#not household_runtime_event_seen_today('clara_melissa_room_visit')",
            ],
            None,
            "TavernMelissaRoom",
            "enter",
            3,
        ),
        (
            "story_clara_melissa_room_visit_1",
            None, (16, 22), None,
            1,
            None,
            [
                "#str(people.location('clara') or '') == 'TavernMelissaRoom'",
                "#str(people.location('melissa') or '') == 'TavernMelissaRoom'",
                "#threads['melissaBatProblem'].num >= 11",
                "#not household_runtime_event_seen_today('clara_melissa_room_visit')",
            ],
            None,
            "TavernMelissaRoom",
            "enter",
            4,
        ),
        (
            "story_clara_melissa_room_visit_2",
            None, (16, 22), None,
            1,
            None,
            [
                "#str(people.location('clara') or '') == 'TavernMelissaRoom'",
                "#str(people.location('melissa') or '') == 'TavernMelissaRoom'",
                "#threads['melissaBatProblem'].num >= 11",
                "#not household_runtime_event_seen_today('clara_melissa_room_visit')",
            ],
            None,
            "TavernMelissaRoom",
            "enter",
            5,
        ),
        (
            "story_clara_tavern_protection_lessons_6",
            [1, 2, 3, 4, 5, 6], (12, 17), None,
            1,
            None,
            [
                "#int(threads['claraForestSofa'].num or 0) >= 6",
                "#not bool(threads['claraForestSofa'].aborted)",
                "#str(people.location('clara') or '') == 'TavernMain'",
                "#str(people.location('melissa') or '') == 'TavernMain'",
            ],
            None,
            "TavernMain",
            "bar_001",
            6,
        ),
    ], highlight=False, threaded=True),
]
define beckyThreadList = [
    LThreadData(0, "becky", "FridayDanceMC", None, [
        BeckyFridayDanceMC,
    ], highlight=False, threaded=False),
    # The Becky home route has two procedure-owned milestones followed by one
    # authored talk event.  Empty cells deliberately avoid registering a
    # second action for scenes already owned by BeckyHomeFront/IntBeckySex.
    LThreadData(0, "becky", "Home", None, [
        (
            "story_becky_home_arrival_0",
            None, None, None,
            1,
            None,
            [
                "#str(rooms.get('BeckyHomeFront').state.get('arrival_mode', '') or '') == 'FromDances'",
            ],
            None,
            "BeckyHomeFront",
            "enter",
            10,
        ),
        [],
        (
            "story_becky_home_invite_talk_0",
            None, None, None,
            1,
            None,
            [
                "#Becky.rel > 12",
                "#Becky.talk_count() < 2",
            ],
            None,
            "talk_becky",
            "becky_home_invite",
            100,
        ),
    ], highlight=False, threaded=True),
    # Dinner stages are advanced only by their authored outcomes inside
    # IntBeckyGuest.  The final Georgette crossover is a scheduled event.
    LThreadData(0, "becky", "Dinner", None, [
        [],
        [],
        (
            "GeorgettBeckyVisit",
            None, (18, 23), None,
            1,
            None,
            [
                "#int(Becky.eddie_home_visit_state or 0) == 4",
                "#int(threads['beckySex'].num or 0) >= 1",
                "#Eddie.saw_mother_sex",
                "#CheckIfSexEventExist('georgett', 99, 'EddieHomeVisit') > 0",
            ],
            None,
            "BeckyHome",
            "georgett_home_visit",
            350,
        ),
    ], highlight=False, threaded=True),
    # These are procedure-owned unlock milestones, not duplicate menu events.
    LThreadData(0, "becky", "Sex", None, [
        [],
        [],
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "EddieSex", None, [
        (
            "IntEddieTalkMomHelper",
            None, None, None,
            1, None,
            ["#eddie_talk_can_mom_helper('eddie')"],
            None,
            "talk_eddie",
            "becky_eddie_sex",
            120,
        ),
        (
            "BeckyEddieJoinFirst",
            None, None, None,
            1, None,
            [
                "#str(rooms.get('BeckyHomeFront').state.get('arrival_mode', '') or '') == 'FromDinner'",
            ],
            None,
            "BeckyHome",
            "enter",
            120,
        ),
        (
            "IntEddieTalkMomHelper",
            None, None, None,
            1, None,
            ["#eddie_talk_can_mom_helper('eddie')"],
            None,
            "talk_eddie",
            "becky_eddie_sex",
            120,
        ),
        (
            "IntEddieTalkMomHelper",
            None, None, None,
            1, None,
            ["#eddie_talk_can_mom_helper('eddie')"],
            None,
            "talk_eddie",
            "becky_eddie_sex",
            120,
        ),
        # The first shared bedroom scene has happened. The final cursor is
        # completed by the later Becky church follow-up, formerly visitedhome 7.
        [],
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "IngaLucasPath", None, [
        ("becky_homefront_share_with_becky", None, None, None, 1, None, [
            "#str(rooms.get('BeckyHomeFront').state.get('arrival_mode', '') or '') == 'FromDances'",
        ], None, "BeckyHomeFront", "inga_discovery", 10),
        ("story_becky_talk_inga_0", None, None, None, 1, None, [
            "#Becky.talk_count() < 2",
        ], None, "talk_becky", "becky_talk_inga1", 20),
        ("story_becky_talk_inga_1", None, None, None, 1, None, [
            "#Becky.talk_count() < 2",
        ], None, "talk_becky", "becky_talk_inga2", 30),
        ("story_becky_talk_lucas_0", None, None, None, 1, None, [
            "#Becky.talk_count() < 2",
        ], None, "talk_becky", "becky_talk_lucas", 40),
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "HusbandBackstory", [
        "#int(Becky.stats.get('orgasms_given', 0) or 0) > 0",
        "#int(Becky.stats.get('sexacts', 0) or 0) > 0",
    ], [
        ("story_becky_talk_husband_0", None, None, None, 1, None, [
            "#Becky.rel > 13",
            "#Becky.talk_count() < 2",
        ], None, "talk_becky", "becky_talk_husband1", 40),
        ("story_becky_talk_husband_1", None, None, None, 1, None, [
            "#Becky.talk_count() < 2",
        ], None, "talk_becky", "becky_talk_husband2", 50),
        ("story_becky_talk_husband_2", None, None, None, 1, None, [
            "#Becky.talk_count() < 2",
        ], None, "talk_becky", "becky_talk_husband3", 60),
        ("story_becky_talk_husband_3", None, None, None, 1, None, [
            "#Becky.talk_count() < 2",
        ], None, "talk_becky", "becky_talk_husband4", 70),
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "EddieBackstory", None, [
        ("story_becky_talk_eddie_0", None, None, None, 1, None, [
            "#Becky.rel > 6",
            "#Becky.talk_count() < 2",
        ], None, "talk_becky", "becky_talk_eddie1", 80),
        ("story_becky_talk_eddie_georgett_0", None, None, None, 1, None, [
            "#Eddie.talked_about_georgett",
            "#(threads.get('beckyHusbandBackstory', None) is not None and (threads['beckyHusbandBackstory'].checkActive() or int(threads['beckyHusbandBackstory'].num or 0) > 0))",
            "#Becky.rel > 8",
            "#Becky.talk_count() < 2",
        ], None, "talk_becky", "becky_talk_eddie2", 90),
    ], highlight=False, threaded=True),
    LThreadData(0, "becky", "ChurchAfterSermon", None, [
        (
            "story_becky_church_after_sermon",
            7, (11, 12), None,
            1,
            None,
            [
                "#Becky.church_after_sermon_event_available()",
            ],
            None,
            "Church",
            "after_cermon_walk",
            130,
        ),
    ], highlight=False, threaded=False),
]
define eddieThreadList = []
define irmaThreadList = []
define churchThreadList = []
define mongolThreadList = []
define cityGuardThreadList = []
define robinThreadList = [
    LThreadData(0, "robin", "BlackwoodRoadAmbush", None, [
        (
            "story_robin_blackwood_ambush_0",
            None, (6, 17), None,
            1,
            None,
            [
                "#int(Becky.trade_offer_stage or 0) == 1",
                "#str(rooms.current_code or '') == 'BlackwoodRoad'",
            ],
            None,
            "BlackwoodRoad",
            "enter",
            0,
        ),
    ], highlight=False, threaded=False),
]
define sherwoodThreadList = []
define tavernThreadList = [
    RThreadData(0, "tavern", "SundayDinner", None, [1, [
        (
            "TavernKitchenSundayDinnerMenu", 7, (12, 13), None,
            1,
            None,
            tavern_sunday_dinner_available,
            None,
            "TavernKitchen",
            "enter",
            -50,
            True,
        ),
    ]], highlight=False, threaded=False),
    RThreadData(0, "tavern", "WorkRandomEvents", None, [1, [
        # (target, day, hour, delay, probability, reqs, condition, item, location, action, priority, repeatable)
        (
            "TavernWorkEventTrigger", None, None, None,
            1,
            None,
            [
                "#tavern_work_planned_for('', 'TavernMain', calendar_v2.time_slot())",
            ],
            None,
            "TavernMain",
            "enter",
            200,
            True,
        ),
    ]], highlight=False, threaded=False),
]
define cityThreadList = [
    LThreadData(0, "city", "BlindPirateFall", None, [
        (
            "story_city_blind_pirate_fall_0",
            None, None, None,
            1,
            None,
            marketplace_blind_pirate_event_ready,
            None,
            "MarketPlace",
            "enter",
            -100,
        ),
        (
            "TavernKitchenBreakfastBlindPirateStory",
            None, None, None,
            1,
            None,
            None,
            None,
            "Breakfast",
            "market_talk",
            0,
        ),
    ], highlight=False, threaded=True),
    RThreadData(0, "city", "StreetChronicles", None, [1, [
        # (target, day, hour, delay, probability, reqs, condition, item, location, action, priority)
        (
            "TownStreetPatrolEvent", None, None, None,
            1,
            None,
            [
                "#TownStreet.patrol_allowed(rooms.current_code)",
            ],
            None,
            "StreetTavern",
            "enter",
            700,
        ),
        (
            "TownStreetThugsEvent", None, None, None,
            1,
            None,
            [
                "#TownStreet.thug_allowed(rooms.current_code)",
            ],
            None,
            "StreetTavern",
            "enter",
            710,
        ),
        (
            "TownStreetHelpEvent", None, None, None,
            1,
            None,
            [
                "#TownStreet.help_allowed(rooms.current_code)",
            ],
            None,
            "StreetTavern",
            "enter",
            720,
        ),
        (
            "TownRandomChronicleEvent", None, None, None,
            1,
            None,
            [
                "#TownStreet.chronicle_allowed(rooms.current_code)",
            ],
            None,
            "StreetTavern",
            "enter",
            900,
        ),
        (
            "TownStreetPatrolEvent", None, None, None,
            1,
            None,
            [
                "#TownStreet.patrol_allowed(rooms.current_code)",
            ],
            None,
            "MarketPlace",
            "enter",
            700,
        ),
        (
            "TownStreetThugsEvent", None, None, None,
            1,
            None,
            [
                "#TownStreet.thug_allowed(rooms.current_code)",
            ],
            None,
            "MarketPlace",
            "enter",
            710,
        ),
        (
            "TownStreetHelpEvent", None, None, None,
            1,
            None,
            [
                "#TownStreet.help_allowed(rooms.current_code)",
            ],
            None,
            "MarketPlace",
            "enter",
            720,
        ),
        (
            "TownRandomChronicleEvent", None, None, None,
            1,
            None,
            [
                "#TownStreet.chronicle_allowed(rooms.current_code)",
            ],
            None,
            "MarketPlace",
            "enter",
            900,
        ),
        (
            "TownStreetPatrolEvent", None, None, None,
            1,
            None,
            [
                "#TownStreet.patrol_allowed(rooms.current_code)",
            ],
            None,
            "PortStreets",
            "enter",
            700,
        ),
        (
            "TownStreetThugsEvent", None, None, None,
            1,
            None,
            [
                "#TownStreet.thug_allowed(rooms.current_code)",
            ],
            None,
            "PortStreets",
            "enter",
            710,
        ),
        (
            "TownStreetHelpEvent", None, None, None,
            1,
            None,
            [
                "#TownStreet.help_allowed(rooms.current_code)",
            ],
            None,
            "PortStreets",
            "enter",
            720,
        ),
        (
            "TownRandomChronicleEvent", None, None, None,
            1,
            None,
            [
                "#TownStreet.chronicle_allowed(rooms.current_code)",
            ],
            None,
            "PortStreets",
            "enter",
            900,
        ),
        (
            "TownStreetPatrolEvent", None, None, None,
            1,
            None,
            [
                "#TownStreet.patrol_allowed(rooms.current_code)",
            ],
            None,
            "ArtisansQuarter",
            "enter",
            700,
        ),
        (
            "TownStreetThugsEvent", None, None, None,
            1,
            None,
            [
                "#TownStreet.thug_allowed(rooms.current_code)",
            ],
            None,
            "ArtisansQuarter",
            "enter",
            710,
        ),
        (
            "TownStreetHelpEvent", None, None, None,
            1,
            None,
            [
                "#TownStreet.help_allowed(rooms.current_code)",
            ],
            None,
            "ArtisansQuarter",
            "enter",
            720,
        ),
        (
            "TownRandomChronicleEvent", None, None, None,
            1,
            None,
            [
                "#TownStreet.chronicle_allowed(rooms.current_code)",
            ],
            None,
            "ArtisansQuarter",
            "enter",
            900,
        ),
    ]], highlight=False, threaded=False),
]
define lizaThreadList = [
    LThreadData(0, "liza", "PortStreetClients", None, [
        (
            "story_liza_portstreet_clients",
            None, None, None,
            1,
            None,
            [
                "#Liza.portstreet_client_event_available()",
            ],
            None,
            "PortStreets",
            "street_clients",
            110,
        ),
    ], highlight=False, threaded=False),
    LThreadData(0, "liza", "TavernClientRoom", None, [
        (
            "TavernProstClients",
            None, (13, 15), None,
            1,
            None,
            [
                "#Liza.can_work_tavern()",
                "#str(rooms.get('TavernMain').state.get('client_room_girl', '') or '') == 'liza'",
                "#int(player.tavern_management.client_room_hole or 0) > 0",
                "#CheckIfSexEventExist('liza', 3, 'Prostitution') > 0",
            ],
            None,
            "TavernEmptyRoom",
            "tavern_client_room",
            110,
        ),
    ], highlight=False, threaded=False),
    LThreadData(0, "liza", "ChurchAfterSermon", None, [
        (
            "story_liza_church_after_sermon",
            7, (11, 12), None,
            1,
            None,
            [
                "#Liza.church_after_sermon_event_available()",
            ],
            None,
            "Church",
            "after_cermon_walk",
            120,
        ),
    ], highlight=False, threaded=False),
]
define georgettThreadList = [
    UThreadData(0, "georgett", "PortStreet", None, [
        (
            "story_georgett_portstreet_first_meet",
            None, None, None,
            1,
            None,
            [
                "#not bool(Georgett.known)",
                "#str(Georgett.getLocation() or '') == 'PortStreets'",
            ],
            None,
            "talk_georgett",
            "intro",
            10,
        ),
        (
            "story_georgett_portstreet_clients",
            None, None, None,
            1,
            None,
            [
                "#bool(Georgett.known)",
                "#int(Georgett.story_value('seeclients', 0) or 0) == 0",
                "#Georgett.portstreet_client_event_available()",
            ],
            None,
            "PortStreets",
            "street_clients",
            100,
        ),
        (
            "IntGeorgettAskClients",
            None, None, None,
            1,
            None,
            [
                "#Georgett.can_talk_today()",
                "#int(Georgett.story_value('seeclients', 0) or 0) > 0",
                "#int(Georgett.story_value('askclients', 0) or 0) == 0",
                "#int(Georgett.rel or 0) >= 7",
            ],
            None,
            "talk_georgett",
            "ask_clients",
            20,
        ),
        (
            "IntGeorgettAskSex",
            None, None, None,
            1,
            None,
            [
                "#Georgett.can_talk_today()",
                "#int(Georgett.story_value('askclients', 0) or 0) > 0",
                "#int(Georgett.story_value('asksex', 0) or 0) == 0",
                "#int(Georgett.rel or 0) >= 7",
                "#int(Georgett.sex_stat('orgasms_given', 0) or 0) >= 3",
            ],
            None,
            "talk_georgett",
            "ask_sex",
            21,
        ),
        (
            "IntGeorgettAskFamily",
            None, None, None,
            1,
            None,
            [
                "#Georgett.can_talk_today()",
                "#int(Georgett.story_value('asksex', 0) or 0) > 0",
                "#int(Georgett.story_value('askparents', 0) or 0) == 0",
                "#int(Georgett.rel or 0) >= 7",
                "#int(Georgett.sex_stat('orgasms_given', 0) or 0) >= 4",
            ],
            None,
            "talk_georgett",
            "ask_family",
            22,
        ),
        (
            "IntGeorgettAskPregnancy",
            None, None, None,
            1,
            None,
            [
                "#Georgett.can_talk_today()",
                "#int(Georgett.story_value('askparents', 0) or 0) > 0",
                "#int(Georgett.story_value('askpregnancy', 0) or 0) == 0",
                "#int(Georgett.rel or 0) >= 7",
                "#int(Georgett.sex_stat('orgasms_given', 0) or 0) >= 4",
            ],
            None,
            "talk_georgett",
            "ask_pregnancy",
            23,
        ),
        (
            "IntGeorgettAskKids",
            None, None, None,
            1,
            None,
            [
                "#Georgett.can_talk_today()",
                "#int(Georgett.story_value('askpregnancy', 0) or 0) > 0",
                "#int(Georgett.story_value('askkids', 0) or 0) == 0",
                "#int(Georgett.rel or 0) >= 7",
                "#int(Georgett.sex_stat('orgasms_given', 0) or 0) >= 5",
            ],
            None,
            "talk_georgett",
            "ask_kids",
            24,
        ),
        (
            "IntGeorgettInviteTavern",
            None, None, None,
            1,
            None,
            [
                "#Georgett.can_talk_today()",
                "#Georgett.can_invite_to_tavern()",
                "#not Georgett.can_work_tavern()",
                "#int(Georgett.rel or 0) >= 10",
                "#int(Liza.rel or 0) >= 8",
            ],
            None,
            "talk_georgett",
            "invite_tavern",
            30,
        ),
    ], highlight=False, threaded=True),
    UThreadData(0, "georgett", "Tavern", [
        "#Georgett.can_work_tavern()",
    ], [
        (
            "IntGeorgettAskPirate",
            None, None, None,
            1,
            None,
            [
                "#Georgett.can_talk_today()",
                "#bool(Liza.glory_hole_asked)",
                "#int(Georgett.story_value('GloryHoleExplained', 0) or 0) == 0",
            ],
            None,
            "talk_georgett",
            "explain_gloryhole",
            20,
        ),
        (
            "IntGeorgettGloryholeTerms",
            None, None, None,
            1,
            None,
            [
                "#Georgett.can_talk_today()",
                "#int(player.tavern_management.glory_hole or 0) == 2",
                "#int(Georgett.story_value('GloryHoleAgreed', 0) or 0) == 0",
            ],
            None,
            "talk_georgett",
            "agree_gloryhole_terms",
            21,
        ),
    ], highlight=False, threaded=True),
    UThreadData(0, "georgett", "Church", [
        "#bool(Georgett.known)",
    ], [
        (
            "ChurchServiceGeorgett",
            7, (8, 9), None,
            1,
            None,
            [
                "#church_service_action_visible()",
                "#str(people.location('georgett') or '') == 'Church'",
                "#int(Georgett.rel or 0) >= 2",
            ],
            None,
            "Church",
            "georgett_service",
            20,
        ),
        (
            "ChurchGeorgettQuickSex",
            7, (8, 9), None,
            1,
            None,
            [
                "#church_service_action_visible()",
                "#int(Georgett.story_value('foundinchurch', 0) or 0) > 0",
                "#int(Georgett.story_value('fuckinchurch', 0) or 0) == 0",
                "#player.intimacy.can_cum()",
                "#Georgett.can_have_sex_today()",
                "#int(Georgett.rel or 0) >= 6",
                "#int(Georgett.sex_stat('sexacts', 0) or 0) >= 3",
                "#int(player.economy.money or 0) >= 15",
            ],
            None,
            "Church",
            "georgett_quick_sex",
            21,
        ),
        (
            "story_georgett_church_confession_regular",
            7, (9, 10), None,
            1,
            None,
            [
                "#church_confession_action_visible()",
                "#int(Georgett.sex_stat('sexacts', 0) or 0) > 0",
                "#int(Georgett.story_value('georgettadmit', 0) or 0) == 0",
            ],
            None,
            "Church",
            "georgett_regular_confession",
            22,
        ),
        (
            "story_georgett_church_confession_service",
            7, (9, 10), None,
            1,
            None,
            [
                "#church_confession_action_visible()",
                "#int(Georgett.sex_stat('sexacts', 0) or 0) > 0",
                "#int(Georgett.story_value('fuckinchurch', 0) or 0) > 0",
                "#int(Georgett.story_value('georgettadmit', 0) or 0) > 0",
                "#int(Georgett.story_value('churchgeorgettadmit', 0) or 0) == 0",
            ],
            None,
            "Church",
            "georgett_service_confession",
            23,
        ),
        (
            "story_georgett_church_after_sermon",
            7, (11, 12), None,
            1,
            None,
            [
                "#Georgett.church_after_sermon_event_available()",
                "#int(Georgett.story_value('SawChurchAfterCermon', 0) or 0) == 0",
            ],
            None,
            "Church",
            "after_cermon_walk",
            110,
        ),
        (
            "IntGeorgettAskGerhard",
            None, None, None,
            1,
            None,
            [
                "#Georgett.can_talk_today()",
                "#int(Georgett.story_value('SawChurchAfterCermon', 0) or 0) > 0",
                "#int(Georgett.story_value('TalkChurchAfterCermon', 0) or 0) == 0",
            ],
            None,
            "talk_georgett",
            "ask_gerhard",
            30,
        ),
    ], highlight=False, threaded=True),
]

define franThreadList = [
    UThreadData(0, "fran", "TempleStories", None, [
        (
            "story_ellona_temple_sunday_stories",
            7, (8, 12), None,
            1,
            None,
            [
                "#Francheska.sunday_stories_available()",
            ],
            None,
            "EllonaTemple",
            "enter",
            20,
        ),
    ], highlight=False, threaded=False),
]

define birthThreadList = [
    UThreadData(0, "system", "GiveBirth", None, [
        ("story_give_birth_sandra", None, None, None, 1, None, ["#int(current_game_day() or 0) > 0", "#Sandra.pregnancy_days() >= 240", "#str(Sandra.sex_stat('pregfather', '') or '') != ''"], None, "TavernMain", "enter", 5),
        ("story_give_birth_melissa", None, None, None, 1, None, ["#int(current_game_day() or 0) > 0", "#Melissa.pregnancy_days() >= 240", "#str(Melissa.sex_stat('pregfather', '') or '') != ''"], None, "TavernMain", "enter", 6),
        ("story_give_birth_becky", None, None, None, 1, None, ["#int(current_game_day() or 0) > 0", "#Becky.pregnancy_days() >= 240", "#str(Becky.stats.get('pregfather', '') or '') != ''"], None, "BeckyHome", "enter", 5),
        ("story_give_birth_inga", None, None, None, 1, None, ["#int(current_game_day() or 0) > 0", "#Inga.pregnancy_days() >= 240", "#str(Inga.sex_stat('pregfather', '') or '') != ''"], None, "BeckyHome", "enter", 6),
        ("story_give_birth_georgett", None, None, None, 1, None, ["#int(current_game_day() or 0) > 0", "#Georgett.pregnancy_days() >= 240", "#str(Georgett.sex_stat('pregfather', '') or '') != ''"], None, "PortStreets", "enter", 5),
        ("story_give_birth_liza", None, None, None, 1, None, ["#int(current_game_day() or 0) > 0", "#Liza.pregnancy_days() >= 240", "#str(Liza.sex_stat('pregfather', '') or '') != ''"], None, "PortStreets", "enter", 6),
    ], highlight=False, threaded=True),
]

define threadListsByGirl = {
    "amanda": amandaThreadList,
    "melissa": melissaThreadList,
    "sandra": sandraThreadList,
    "clara": claraThreadList,
    "mongol": mongolThreadList,
    "cityguard": cityGuardThreadList,
    "robin": robinThreadList,
    "sherwood": sherwoodThreadList,
    "becky": beckyThreadList,
    "eddie": eddieThreadList,
    "irma": irmaThreadList,
    "church": churchThreadList,
    "liza": lizaThreadList,
    "georgett": georgettThreadList,
    "fran": franThreadList,
    "tavern": tavernThreadList,
    "city": cityThreadList,
    "birth": birthThreadList,
}

define threadList = (
    amandaThreadList
    + melissaThreadList
    + sandraThreadList
    + claraThreadList
    + mongolThreadList
    + cityGuardThreadList
    + robinThreadList
    + sherwoodThreadList
    + beckyThreadList
    + eddieThreadList
    + irmaThreadList
    + churchThreadList
    + lizaThreadList
    + georgettThreadList
    + franThreadList
    + tavernThreadList
    + cityThreadList
    + birthThreadList
)

define threadData = loadThreadData(threadList)
default threads = createThreads()
